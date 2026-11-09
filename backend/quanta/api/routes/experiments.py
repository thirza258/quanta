from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, Request, Response
from sqlmodel import Session

from quanta.api.dependencies import key, owner
from quanta.core import auth
from quanta.core.limits import limiter
from quanta.db.models import User
from quanta.db.session import get_session
from quanta.services import experiments as service

router = APIRouter(prefix="/api/v1/research", tags=["Research registry"])


def _limit_runs(request: Request, user: User | None):
    # A run forks dozens of sandbox processes, so it has a stricter budget than `compute`.
    limiter.check(key(request, "research", user), maximum=6, seconds=60)


@router.get("/options")
def options():
    return service.options()


@router.get("/experiments")
def experiments(account: str = Depends(owner), db: Session = Depends(get_session)):
    return service.list_experiments(db, account)


@router.post("/experiments", status_code=201)
def create(
    payload: service.ExperimentCreate,
    request: Request,
    account: str = Depends(owner),
    user: User | None = Depends(auth.optional_user),
    db: Session = Depends(get_session),
):
    if payload.run:
        _limit_runs(request, user)
    return service.create(db, account, payload)


@router.get("/experiments/{experiment_id}")
def experiment(
    experiment_id: str, account: str = Depends(owner), db: Session = Depends(get_session)
):
    return service.get_experiment(db, account, experiment_id)


@router.patch("/experiments/{experiment_id}")
def update(
    experiment_id: str,
    payload: service.ExperimentUpdate,
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    return service.update(db, account, experiment_id, payload)


@router.delete("/experiments/{experiment_id}")
def delete(experiment_id: str, account: str = Depends(owner), db: Session = Depends(get_session)):
    return service.delete(db, account, experiment_id)


@router.post("/experiments/{experiment_id}/runs", status_code=202)
def start(
    experiment_id: str,
    request: Request,
    account: str = Depends(owner),
    user: User | None = Depends(auth.optional_user),
    db: Session = Depends(get_session),
):
    _limit_runs(request, user)
    return service.start_run(db, account, experiment_id)


@router.get("/runs/{run_id}")
def run(run_id: str, account: str = Depends(owner), db: Session = Depends(get_session)):
    return service.get_run(db, account, run_id)


@router.post("/runs/{run_id}/rerun", status_code=202)
def rerun(
    run_id: str,
    request: Request,
    account: str = Depends(owner),
    user: User | None = Depends(auth.optional_user),
    db: Session = Depends(get_session),
):
    _limit_runs(request, user)
    return service.rerun(db, account, run_id)


@router.get("/experiments/{experiment_id}/report")
def report(
    experiment_id: str,
    format: Literal["markdown", "html"] = "markdown",
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    content, media_type, filename = service.report_file(db, account, experiment_id, format)
    return Response(
        content,
        media_type=media_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'; img-src data:",
        },
    )
