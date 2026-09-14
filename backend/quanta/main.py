from __future__ import annotations

import json
import os
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field, StrictInt
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from . import analytics, auth, broker, data_store, runner
from .assessments import ExamAnswers, grade
from .database import ExamSubmission, Submission, User, Workspace, get_session, initialize
from .econometrics import FactorRequest, PortfolioRequest, factor_model, portfolio
from .limits import limiter
from .simulator import router as simulator_router

CATALOG = json.loads((Path(__file__).resolve().parents[2] / "src/data/curriculum.json").read_text())
LESSONS = {m["id"]: m for c in CATALOG for m in c["modules"]}
EXAMS = {exam["id"]: exam for course in CATALOG for exam in course["exams"]}


@asynccontextmanager
async def lifespan(app):
    initialize()
    yield


app = FastAPI(title="Quanta API", version="0.1.0", lifespan=lifespan)
app.include_router(simulator_router)


@app.middleware("http")
async def request_guards(request: Request, call_next):
    if request.method in ("POST", "PUT", "PATCH", "DELETE"):
        origin = request.headers.get("origin")
        allowed = set(
            os.getenv(
                "ALLOWED_ORIGINS",
                "http://localhost:5173,http://127.0.0.1:5173,http://localhost:4173,http://127.0.0.1:4173,http://localhost:8080,http://127.0.0.1:8080",
            ).split(",")
        )
        if origin and origin not in allowed:
            return JSONResponse({"detail": "Origin is not allowed."}, status_code=403)
        if int(request.headers.get("content-length", "0") or 0) > 1500000:
            return JSONResponse({"detail": "Request is too large."}, status_code=413)
        body = await request.body()
        if len(body) > 1500000:
            return JSONResponse({"detail": "Request is too large."}, status_code=413)
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "same-origin"
    if request.url.path.startswith(
        ("/api/v1/auth", "/api/v1/workspace", "/api/v1/exams", "/api/v1/simulator")
    ):
        response.headers["Cache-Control"] = "no-store"
    return response


def key(request: Request, scope: str, user: User | None = None):
    return f"{scope}:{user.id if user else request.client.host if request.client else 'unknown'}"


@app.get("/api/v1/health")
def health(db: Session = Depends(get_session)):
    db.exec(select(User).limit(1)).first()
    if limiter.redis:
        limiter.redis.ping()
    return {
        "status": "ok",
        "sandbox": os.getenv("QUANTA_SANDBOX", "guided"),
        "historical_datasets": len(data_store.catalog()),
    }


@app.get("/api/v1/courses")
def courses():
    return CATALOG


@app.get("/api/v1/courses/lessons/{lesson_id}")
def lesson(lesson_id: str):
    if lesson_id not in LESSONS:
        raise HTTPException(404, "Lesson not found.")
    return LESSONS[lesson_id]


class Credentials(BaseModel):
    email: EmailStr = Field(max_length=254)
    password: str = Field(min_length=10, max_length=128)
    name: str = Field("Researcher", min_length=1, max_length=60)


@app.post("/api/v1/auth/register", status_code=201)
def register(
    payload: Credentials,
    request: Request,
    response: Response,
    db: Session = Depends(get_session),
):
    limiter.check(key(request, "auth"), 10, 60)
    email = str(payload.email).lower().strip()
    user = User(
        email=email,
        name=payload.name.strip() or "Researcher",
        hashed_password=auth.hasher.hash(payload.password),
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "An account with that email already exists.") from None
    auth.issue(user, response, db)
    return auth.profile(user)


@app.post("/api/v1/auth/login")
def login(
    payload: Credentials,
    request: Request,
    response: Response,
    db: Session = Depends(get_session),
):
    limiter.check(key(request, "auth"), 10, 60)
    user = db.exec(select(User).where(User.email == str(payload.email).lower().strip())).first()
    valid = auth.hasher.verify(payload.password, user.hashed_password if user else auth.DUMMY_HASH)
    if not user or not valid:
        raise HTTPException(401, "Email or password is incorrect.")
    auth.issue(user, response, db)
    return auth.profile(user)


@app.get("/api/v1/auth/me")
def me(user: User | None = Depends(auth.optional_user)):
    return auth.profile(user) if user else None


@app.post("/api/v1/auth/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_session)):
    auth.logout(request, response, db)
    return {"ok": True}


class WorkspacePayload(BaseModel):
    version: int = Field(ge=0)
    state: dict[str, Any]


@app.get("/api/v1/workspace")
def workspace(user: User = Depends(auth.require_user), db: Session = Depends(get_session)):
    item = db.get(Workspace, user.id)
    return {"version": item.version, "state": item.state} if item else {"version": 0, "state": {}}


@app.put("/api/v1/workspace")
def save_workspace(
    payload: WorkspacePayload,
    user: User = Depends(auth.require_user),
    db: Session = Depends(get_session),
):
    if len(json.dumps(payload.state)) > 1200000:
        raise HTTPException(413, "Workspace limit reached. Export or remove older experiments.")
    item = db.get(Workspace, user.id)
    if not item:
        if payload.version != 0:
            raise HTTPException(409, "Workspace version changed. Reload before saving.")
        try:
            item = Workspace(user_id=user.id, state=payload.state, version=1)
            db.add(item)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                409, "Workspace changed in another session. Reload before saving."
            ) from None
        return {"version": 1}
    result = db.execute(
        update(Workspace)
        .where(Workspace.user_id == user.id, Workspace.version == payload.version)
        .values(
            state=payload.state,
            version=payload.version + 1,
            updated_at=datetime.now(timezone.utc).isoformat(),
        )
    )
    if result.rowcount != 1:
        db.rollback()
        raise HTTPException(409, "Workspace changed in another session. Reload before saving.")
    db.commit()
    return {"version": payload.version + 1}


class Answer(BaseModel):
    answer: StrictInt = Field(ge=0, le=20)
    question: StrictInt = Field(default=0, ge=0, le=20)


@app.post("/api/v1/exercises/{lesson_id}/submit")
def submit(
    lesson_id: str,
    payload: Answer,
    user: User | None = Depends(auth.optional_user),
    db: Session = Depends(get_session),
):
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


@app.post("/api/v1/exams/{exam_id}/submit")
def submit_exam(
    exam_id: str,
    payload: ExamAnswers,
    request: Request,
    user: User | None = Depends(auth.optional_user),
    db: Session = Depends(get_session),
):
    if exam_id not in EXAMS:
        raise HTTPException(404, "Exam not found.")
    limiter.check(key(request, "assessment", user), 60, 60)
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


@app.get("/api/v1/exams/{exam_id}/attempts")
def exam_attempts(
    exam_id: str,
    user: User = Depends(auth.require_user),
    db: Session = Depends(get_session),
):
    if exam_id not in EXAMS:
        raise HTTPException(404, "Exam not found.")
    attempts = db.exec(
        select(ExamSubmission)
        .where(ExamSubmission.user_id == user.id, ExamSubmission.exam_id == exam_id)
        .order_by(ExamSubmission.created_at.desc())
        .limit(50)
    ).all()
    return {"attempts": [attempt.result for attempt in attempts]}


@app.get("/api/v1/data/catalog")
def datasets():
    return {
        "datasets": data_store.catalog(),
        "note": "No historical market data is bundled. Synthetic scenarios are counterfactual illustrations, not reconstructions of named periods.",
    }


@app.post("/api/v1/data/synthetic/generate")
def generate(
    payload: analytics.DatasetParams,
    request: Request,
    user: User | None = Depends(auth.optional_user),
):
    limiter.check(key(request, "compute", user))
    bars = analytics.generate(payload)
    return {
        "bars": bars,
        "params": payload.model_dump(),
        "provenance": "Synthetic · seeded stochastic model · weekday calendar (no holiday adjustment)",
    }


@app.post("/api/v1/sandbox/execute")
def execute(
    payload: analytics.ExecuteRequest,
    request: Request,
    user: User | None = Depends(auth.optional_user),
):
    limiter.check(key(request, "compute", user))
    start = time.perf_counter()
    try:
        bars = (
            analytics.generate(payload.dataset_params)
            if payload.dataset_type == "synthetic"
            else data_store.historical(payload.dataset_params.symbol, payload.dataset_params.years)
        )
        output = runner.run(
            payload.code, analytics.strategy_data(bars, payload.dataset_params.window)
        )
        result = analytics.backtest(
            bars,
            output["signals"],
            payload.capital,
            payload.commission_bps,
            payload.slippage_bps,
        )
    except (ValueError, ArithmeticError) as error:
        raise HTTPException(422, str(error)) from None
    return {
        **result,
        "stdout": output.get("stdout", ""),
        "stderr": output.get("stderr", ""),
        "execution_ms": round((time.perf_counter() - start) * 1000, 1),
        "dataset_type": payload.dataset_type,
        "params": payload.dataset_params.model_dump(),
        "runtime": os.getenv("QUANTA_SANDBOX", "guided"),
    }


@app.post("/api/v1/analytics/valuation")
def valuation(payload: analytics.ValuationRequest):
    return analytics.valuation(payload)


@app.post("/api/v1/analytics/amm")
def amm(payload: analytics.AmmRequest):
    return analytics.amm(payload)


@app.post("/api/v1/broker/order")
def order(payload: broker.OrderRequest):
    return broker.place(payload)


@app.post("/api/v1/analytics/factors")
def factors(
    payload: FactorRequest,
    request: Request,
    user: User | None = Depends(auth.optional_user),
):
    limiter.check(key(request, "compute", user))
    try:
        return factor_model(payload)
    except ValueError as error:
        raise HTTPException(422, str(error)) from None


@app.post("/api/v1/analytics/portfolio")
def optimize(
    payload: PortfolioRequest,
    request: Request,
    user: User | None = Depends(auth.optional_user),
):
    limiter.check(key(request, "compute", user))
    try:
        return portfolio(payload)
    except ValueError as error:
        raise HTTPException(422, str(error)) from None
