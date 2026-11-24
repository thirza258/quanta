from __future__ import annotations

import csv
import io
import re

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from quanta.db.models import AnalyticsEvent, CapstoneSubmission, ExamSubmission, Submission, User
from quanta.domain.assessments import Answer, ExamAnswers, grade
from quanta.domain.catalog import EXAMS, LESSONS


def submit(lesson_id: str, payload: Answer, user: User | None, db: Session):
    if lesson_id not in LESSONS:
        raise HTTPException(404, "Exercise not found.")
    lesson = LESSONS[lesson_id]
    exercises = lesson.get("exercises", [lesson["exercise"]])
    if payload.question >= len(exercises):
        raise HTTPException(422, "Invalid exercise question.")
    exercise = exercises[payload.question]
    if payload.answer >= len(exercise["options"]):
        raise HTTPException(422, "Invalid answer option.")
    correct = payload.answer == exercise["answer"]
    if user:
        db.add(
            Submission(
                user_id=user.id,
                lesson_id=lesson_id
                if payload.question == 0
                else f"{lesson_id}:q{payload.question + 1}",
                answer=payload.answer,
                correct=correct,
            )
        )
        db.commit()
    return {"correct": correct, "explanation": exercise["explanation"]}


def submit_exam(exam_id: str, payload: ExamAnswers, user: User | None, db: Session):
    if exam_id not in EXAMS:
        raise HTTPException(404, "Exam not found.")
    result = grade(EXAMS[exam_id], payload)
    if not user:
        return result

    def existing_result(existing):
        if (
            existing.user_id != user.id
            or existing.exam_id != exam_id
            or existing.result["answers"] != payload.answers
            or existing.result["version"] != payload.version
        ):
            raise HTTPException(
                409, "This attempt identifier has already been used. Start a new attempt."
            )
        return existing.result

    existing = db.get(ExamSubmission, str(payload.id))
    if existing:
        return existing_result(existing)
    db.add(ExamSubmission(id=str(payload.id), user_id=user.id, exam_id=exam_id, result=result))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.get(ExamSubmission, str(payload.id))
        if existing:
            return existing_result(existing)
        raise
    return result


def exam_attempts(exam_id: str, user: User, db: Session):
    if exam_id not in EXAMS:
        raise HTTPException(404, "Exam not found.")
    attempts = db.exec(
        select(ExamSubmission)
        .where(ExamSubmission.user_id == user.id, ExamSubmission.exam_id == exam_id)
        .order_by(ExamSubmission.created_at.desc())
        .limit(50)
    ).all()
    return {"attempts": [attempt.result for attempt in attempts]}


def record_analytics_event(payload: dict, user: User | None, db: Session):
    event_type = payload.get("event_type")
    course_id = payload.get("course_id")
    if not event_type or not course_id:
        raise HTTPException(422, "event_type and course_id are required.")
    event = AnalyticsEvent(
        user_id=user.id if user else None,
        session_id=payload.get("session_id"),
        event_type=event_type,
        course_id=course_id,
        lesson_id=payload.get("lesson_id"),
        metadata_json=payload.get("metadata", {}),
    )
    db.add(event)
    db.commit()
    return {"status": "ok", "event_id": event.id}


def list_analytics_events(course_id: str | None, event_type: str | None, db: Session):
    query = select(AnalyticsEvent)
    if course_id:
        query = query.where(AnalyticsEvent.course_id == course_id)
    if event_type:
        query = query.where(AnalyticsEvent.event_type == event_type)
    query = query.order_by(AnalyticsEvent.created_at.desc()).limit(100)
    events = db.exec(query).all()
    return {"events": [e.model_dump() for e in events]}


def parse_idr_amount(val) -> float:
    if val is None:
        return 0.0
    s = str(val).strip()
    if not s:
        return 0.0
    # Strip currency prefixes and suffixes
    s = re.sub(r"^[Rr][Pp]\.?\s*", "", s)
    s = re.sub(r"^[\$€£]\s*", "", s)
    s = re.sub(r"\s*(IDR|USD|SGD|EUR|GBP)$", "", s, flags=re.IGNORECASE).strip()
    # Normalize IDR / European dot-as-thousands vs comma-as-thousands
    if "." in s and "," in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "." in s:
        parts = s.split(".")
        if len(parts) > 2 or (len(parts) == 2 and len(parts[1]) == 3):
            s = s.replace(".", "")
    elif "," in s:
        parts = s.split(",")
        if len(parts) > 2 or (len(parts) == 2 and len(parts[1]) == 3):
            s = s.replace(",", "")
        else:
            s = s.replace(",", ".")
    return float(s)


def validate_capstone(course_id: str, csv_content: str, user: User | None, db: Session):
    if course_id == "msme-financial-literacy":
        f = io.StringIO(csv_content.strip())
        reader = csv.DictReader(f)
        aliases = {
            "opening": "opening_balance",
            "saldo_awal": "opening_balance",
            "inflows": "cash_inflows",
            "kas_masuk": "cash_inflows",
            "outflows": "cash_outflows",
            "kas_keluar": "cash_outflows",
            "closing": "closing_balance",
            "saldo_akhir": "closing_balance",
        }
        required_cols = {"opening_balance", "cash_inflows", "cash_outflows", "closing_balance"}
        rows = list(reader)
        if len(rows) != 12:
            raise HTTPException(422, f"Capstone requires exactly 12 monthly rows, found {len(rows)}.")

        prev_closing = None
        has_negative_balance = False
        negative_months = []
        for i, raw_row in enumerate(rows):
            normalized = {}
            for k, v in raw_row.items():
                if k is None:
                    continue
                k_clean = k.strip().lower()
                canonical = aliases.get(k_clean, k_clean)
                normalized[canonical] = v.strip() if v else "0"

            for col in required_cols:
                if col not in normalized:
                    raise HTTPException(422, f"Missing required column '{col}' in row {i+1}.")

            try:
                op = parse_idr_amount(normalized["opening_balance"])
                inf = parse_idr_amount(normalized["cash_inflows"])
                out = parse_idr_amount(normalized["cash_outflows"])
                cl = parse_idr_amount(normalized["closing_balance"])
            except ValueError:
                raise HTTPException(422, f"Non-numeric cash value in row {i+1}.")

            if prev_closing is not None and abs(op - prev_closing) > 0.05:
                raise HTTPException(
                    422,
                    f"Row {i+1} opening balance ({op}) does not match previous month closing balance ({prev_closing}). Balance continuity violated.",
                )
            expected_closing = round(op + inf - out, 2)
            if abs(cl - expected_closing) > 0.05:
                raise HTTPException(
                    422,
                    f"Row {i+1} closing balance error: expected opening ({op}) + inflows ({inf}) - outflows ({out}) = {expected_closing}, but found {cl}.",
                )
            if cl < 0:
                has_negative_balance = True
                negative_months.append(i + 1)
            prev_closing = cl

        rubric = {
            "continuity_check": "passed",
            "twelve_months_check": "passed",
            "liquidity_check": "warning" if has_negative_balance else "passed",
            "summary": (
                f"12-month cash forecast verified with strict balance continuity. Cash gap warning in month(s) {negative_months}: working capital buffer required."
                if has_negative_balance
                else "12-month cash forecast verified with strict balance continuity and positive liquidity."
            ),
        }
        if has_negative_balance:
            rubric["cash_gap_warning"] = f"Month(s) {negative_months} show a cash deficit; working capital financing needed."

        submission = CapstoneSubmission(
            user_id=user.id if user else None,
            course_id=course_id,
            status="passed",
            score=100.0,
            rubric_feedback=rubric,
            submission_data=csv_content[:5000],
        )
        db.add(submission)
        db.commit()
        return {
            "status": "passed",
            "message": "12-month cash flow forecast validated and accepted." + (
                " Note: seasonal cash gap detected." if has_negative_balance else ""
            ),
        }

    elif course_id == "data-hygiene":
        f = io.StringIO(csv_content.strip())
        reader = csv.DictReader(f)
        rows = list(reader)
        if not rows:
            raise HTTPException(422, "Uploaded CSV file is empty.")

        # Canonical category taxonomy
        allowed_taxonomy = {
            "penjualan",
            "persediaan",
            "operasional",
            "gaji",
            "modal",
            "utilitas",
            "bahan baku",
            "langganan saas",
            "langganan",
            "software",
            "beban",
            "pendapatan",
            "konsultasi",
        }

        # Check required columns
        fieldnames = [fn.strip().lower() for fn in (reader.fieldnames or [])]
        has_date = any(c in fieldnames for c in ("date", "tanggal"))
        has_id = any(c in fieldnames for c in ("id", "tx_id", "transaction_id"))
        has_category = any(c in fieldnames for c in ("category", "kategori"))
        has_amounts = (
            any(c in fieldnames for c in ("amount", "nominal"))
            or (any(c in fieldnames for c in ("inflow", "kas_masuk")) and any(c in fieldnames for c in ("outflow", "kas_keluar")))
        )
        if not (has_date and has_id and has_category and has_amounts):
            raise HTTPException(
                422,
                "CSV must contain required columns: date, transaction_id, category, and numeric amount fields.",
            )

        seen_keys = set()
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        currency_symbols = ["$", "Rp", "rp", "€", "EUR", "USD", "IDR", "SGD", "GBP"]

        for idx, row in enumerate(rows):
            # 1. Date format check
            date_val = row.get("date") or row.get("Date") or row.get("tanggal")
            if not date_val or not date_pattern.match(date_val.strip()):
                raise HTTPException(
                    422, f"Row {idx+1} invalid date '{date_val}': must follow ISO-8601 'YYYY-MM-DD'."
                )

            # 2. Category taxonomy check
            cat_val = row.get("category") or row.get("Category") or row.get("kategori")
            if not cat_val or cat_val.strip().lower() not in allowed_taxonomy:
                raise HTTPException(
                    422,
                    f"Row {idx+1} invalid category '{cat_val}': category must map to canonical taxonomy {sorted(allowed_taxonomy)}.",
                )

            # 3. Numeric amounts and isolated currencies
            amount_cols = ["amount", "Amount", "nominal", "inflow", "outflow", "balance"]
            for col in amount_cols:
                if col in row and row[col] is not None and str(row[col]).strip() != "":
                    val_str = str(row[col]).strip()
                    if any(sym in val_str for sym in currency_symbols):
                        raise HTTPException(
                            422,
                            f"Row {idx+1} contains uncleaned currency symbol in column '{col}': '{val_str}'. Currency must be isolated in a dedicated 'currency' column.",
                        )
                    try:
                        float(val_str.replace(",", ""))
                    except ValueError:
                        raise HTTPException(
                            422,
                            f"Row {idx+1} contains non-numeric amount in column '{col}': '{val_str}'.",
                        )

            # 4. Duplicate checks (composite key: date + transaction_id)
            tx_id = row.get("id") or row.get("tx_id") or row.get("transaction_id")
            if tx_id:
                composite_key = (date_val.strip(), tx_id.strip())
                if composite_key in seen_keys:
                    raise HTTPException(
                        422,
                        f"Duplicate composite key (date='{date_val}', id='{tx_id}') detected at row {idx+1}.",
                    )
                seen_keys.add(composite_key)

        submission = CapstoneSubmission(
            user_id=user.id if user else None,
            course_id=course_id,
            status="passed",
            score=100.0,
            rubric_feedback={
                "iso_dates": "passed",
                "isolated_currencies": "passed",
                "deduplicated": "passed",
                "taxonomy": "passed",
                "required_columns": "passed",
                "summary": "Cleaned dataset verified: valid ISO dates, isolated currencies, deduplicated composite keys, and normalized taxonomy.",
            },
            submission_data=csv_content[:5000],
        )
        db.add(submission)
        db.commit()
        return {"status": "passed", "message": "Cleaned dataset verified against data hygiene requirements."}

    else:
        submission = CapstoneSubmission(
            user_id=user.id if user else None,
            course_id=course_id,
            status="passed",
            score=100.0,
            rubric_feedback={"summary": "Capstone submission received."},
            submission_data=csv_content[:5000],
        )
        db.add(submission)
        db.commit()
        return {"status": "passed", "message": "Capstone submission received."}

