"""Learning assessment grading. Catalog answers are public for open-book study."""

from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel, Field, StrictInt


class ExamAnswers(BaseModel):
    id: UUID
    version: StrictInt = Field(ge=1)
    startedAt: datetime
    answers: dict[str, StrictInt] = Field(max_length=80)


def grade(exam: dict, payload: ExamAnswers) -> dict:
    if payload.version != exam["version"]:
        raise HTTPException(409, "This exam has changed. Start a new attempt.")
    questions = exam["questions"]
    if set(payload.answers) != {q["id"] for q in questions}:
        raise HTTPException(422, "Submit exactly one answer for every exam question.")
    if any(not 0 <= payload.answers[q["id"]] < len(q["options"]) for q in questions):
        raise HTTPException(422, "Invalid answer option.")
    correct = sum(payload.answers[q["id"]] == q["answer"] for q in questions)
    return {
        "id": str(payload.id),
        "examId": exam["id"],
        "version": exam["version"],
        "startedAt": payload.startedAt.isoformat(),
        "submittedAt": datetime.now(timezone.utc).isoformat(),
        "answers": payload.answers,
        "correctCount": correct,
        "total": len(questions),
        "score": round(correct / len(questions) * 100, 2),
        "passed": correct * 100 >= exam["passingScore"] * len(questions),
        "grading": "server",
    }
