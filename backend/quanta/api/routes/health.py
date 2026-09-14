from __future__ import annotations

import os

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quanta.core.limits import limiter
from quanta.db.models import User
from quanta.db.session import get_session
from quanta.services import data_store

router = APIRouter()


@router.get("/api/v1/health")
def health(db: Session = Depends(get_session)):
    db.exec(select(User).limit(1)).first()
    if limiter.redis:
        limiter.redis.ping()
    return {
        "status": "ok",
        "sandbox": os.getenv("QUANTA_SANDBOX", "guided"),
        "historical_datasets": len(data_store.catalog()),
    }
