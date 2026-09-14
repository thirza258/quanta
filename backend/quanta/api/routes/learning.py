from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from quanta.api.dependencies import key
from quanta.core import auth
from quanta.core.limits import limiter
from quanta.db.models import User
from quanta.db.session import get_session
from quanta.domain.assessments import Answer, ExamAnswers
from quanta.services import learning as service

router = APIRouter(tags=["Learning"])


@router.post("/api/v1/exercises/{lesson_id}/submit")
def submit(
    lesson_id: str,
    payload: Answer,
    user: User | None = Depends(auth.optional_user),
    db: Session = Depends(get_session),
):
    return service.submit(lesson_id, payload, user, db)


@router.post("/api/v1/exams/{exam_id}/submit")
def submit_exam(
    exam_id: str,
    payload: ExamAnswers,
    request: Request,
    user: User | None = Depends(auth.optional_user),
    db: Session = Depends(get_session),
):
    limiter.check(key(request, "assessment", user), 60, 60)
    return service.submit_exam(exam_id, payload, user, db)


@router.get("/api/v1/exams/{exam_id}/attempts")
def exam_attempts(
    exam_id: str,
    user: User = Depends(auth.require_user),
    db: Session = Depends(get_session),
):
    return service.exam_attempts(exam_id, user, db)
