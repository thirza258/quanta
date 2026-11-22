"""Immutable issuer records for self-directed, open-book course completion."""

import hashlib
import json
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException
from pydantic import BaseModel, Field, StrictInt, ValidationError
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from quanta.db.models import Certificate, ExamSubmission, User, Workspace
from quanta.domain.assessments import ExamAnswers, grade
from quanta.domain.catalog import CATALOG
from quanta.domain.errors import DomainError
from quanta.services.pdf_certificate import generate_certificate_pdf


class CertificateClaim(BaseModel):
    trackId: str = Field(min_length=1, max_length=100)
    recipientName: str = Field(min_length=1, max_length=80)
    workspaceVersion: StrictInt = Field(ge=0)


def _passed(exam: dict, attempt: object) -> bool:
    # Device attempts are accepted only after regrading their answers here.
    # Caller-supplied score, passed, and grading fields have no authority.
    if not isinstance(attempt, dict):
        return False
    try:
        return grade(exam, ExamAnswers.model_validate(attempt))["passed"]
    except (ValidationError, DomainError):
        return False


def claim(payload: CertificateClaim, user: User, db: Session):
    course = next((item for item in CATALOG if item["id"] == payload.trackId), None)
    if not course:
        raise HTTPException(404, "Course not found.")
    name = " ".join(payload.recipientName.split())
    if not name:
        raise HTTPException(422, "Enter the name to appear on your certificate.")
    requirements = {
        "trackId": course["id"],
        "lessonIds": sorted(lesson["id"] for lesson in course["modules"]),
        "examVersions": {exam["id"]: exam["version"] for exam in course["exams"]},
    }
    course_key = hashlib.sha256(json.dumps(requirements, sort_keys=True).encode()).hexdigest()
    query = select(Certificate).where(
        Certificate.user_id == user.id, Certificate.course_key == course_key
    )
    existing = db.exec(query).first()
    if existing:
        return existing.record
    workspace = db.get(Workspace, user.id)
    if not workspace or workspace.version != payload.workspaceVersion:
        raise HTTPException(409, "Sync your latest workspace before claiming this certificate.")
    completed = workspace.state.get("completed", [])
    if not isinstance(completed, list) or not all(
        lesson in completed for lesson in requirements["lessonIds"]
    ):
        raise HTTPException(422, "Complete every course module before claiming its certificate.")
    device_attempts = workspace.state.get("examAttempts", {})
    if not isinstance(device_attempts, dict):
        device_attempts = {}

    all_attempts = []
    for exam in course["exams"]:
        online = db.exec(
            select(ExamSubmission).where(
                ExamSubmission.user_id == user.id, ExamSubmission.exam_id == exam["id"]
            )
        ).all()
        saved = device_attempts.get(exam["id"], [])
        attempts = [submission.result for submission in online] + (
            saved if isinstance(saved, list) else []
        )
        all_attempts.extend(attempts)
        if not any(_passed(exam, attempt) for attempt in attempts):
            raise HTTPException(
                422, f"Pass the current {exam['title']} before claiming this certificate."
            )

    # Compute score band if applicable (e.g. Conduct & Compliance Essentials)
    score_band = None
    best_pct = 0.0
    for a in all_attempts:
        if isinstance(a, dict):
            if "score" in a:
                best_pct = max(best_pct, float(a.get("score", 0)))
            elif "correct" in a and "total" in a and a.get("total", 0) > 0:
                best_pct = max(best_pct, float(a["correct"]) / float(a["total"]) * 100.0)

    cert_config = course.get("certificate", {})
    if payload.trackId == "conduct-compliance-essentials" or cert_config.get("verification_required"):
        if best_pct >= 95.0:
            score_band = "Distinction"
        elif best_pct >= 90.0:
            score_band = "Merit"
        else:
            score_band = "Pass"

    identifier = f"QTA-{str(uuid4()).upper()}"
    issued_at = datetime.now(timezone.utc).isoformat()
    record = {
        **requirements,
        "id": identifier,
        "courseTitle": course["title"],
        "recipientName": name,
        "issuedAt": issued_at,
        "studyMinutes": sum(lesson["minutes"] for lesson in course["modules"]),
    }
    if payload.trackId == "conduct-compliance-essentials" or cert_config.get("verification_required"):
        record["contentVersion"] = 1
        record["publicVerificationOptOut"] = False
        if score_band:
            record["scoreBand"] = score_band

    db.add(
        Certificate(
            id=identifier,
            user_id=user.id,
            course_key=course_key,
            record=record,
            created_at=issued_at,
        )
    )
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.exec(query).first()
        if existing:
            return existing.record
        raise
    return record


def list_certificates(user: User, db: Session):
    records = db.exec(
        select(Certificate)
        .where(Certificate.user_id == user.id)
        .order_by(Certificate.created_at.desc())
    ).all()
    return {"certificates": [record.record for record in records]}


def verify(identifier: str, db: Session):
    certificate = db.get(Certificate, identifier.upper()) if len(identifier) == 40 else None
    if not certificate:
        raise HTTPException(404, "No issued certificate matches this ID.")
    rec = dict(certificate.record)
    if rec.get("publicVerificationOptOut"):
        rec["recipientName"] = "Withheld by recipient (authentic certificate confirmed)"
    return {"status": "valid", "certificate": rec}


def set_privacy(identifier: str, opt_out: bool, user: User, db: Session):
    certificate = db.get(Certificate, identifier.upper()) if len(identifier) == 40 else None
    if not certificate:
        raise HTTPException(404, "No issued certificate matches this ID.")
    if certificate.user_id != user.id:
        raise HTTPException(403, "You do not have permission to modify this certificate.")
    rec = dict(certificate.record)
    rec["publicVerificationOptOut"] = opt_out
    certificate.record = rec
    db.add(certificate)
    db.commit()
    db.refresh(certificate)
    return {"status": "updated", "publicVerificationOptOut": opt_out}


def generate_pdf(identifier: str, db: Session) -> tuple[bytes, str]:
    certificate = db.get(Certificate, identifier.upper()) if len(identifier) == 40 else None
    if not certificate:
        raise HTTPException(404, "No issued certificate matches this ID.")
    pdf_bytes = generate_certificate_pdf(certificate.record)
    filename = f"certificate_{certificate.id}.pdf"
    return pdf_bytes, filename
