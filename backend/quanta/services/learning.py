from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from quanta.db.models import ExamSubmission, Submission, User
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
