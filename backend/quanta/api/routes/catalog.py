from __future__ import annotations

from fastapi import APIRouter, HTTPException

from quanta.domain.catalog import CATALOG, LESSONS

router = APIRouter()


@router.get("/api/v1/courses")
def courses():
    return CATALOG


@router.get("/api/v1/courses/lessons/{lesson_id}")
def lesson(lesson_id: str):
    if lesson_id not in LESSONS:
        raise HTTPException(404, "Lesson not found.")
    return LESSONS[lesson_id]
