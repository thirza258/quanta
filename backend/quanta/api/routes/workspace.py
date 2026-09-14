from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import Session

from quanta.core import auth
from quanta.db.models import User
from quanta.db.session import get_session
from quanta.domain.accounts import WorkspacePayload
from quanta.services import workspace as service

router = APIRouter(tags=["Workspace"])


@router.get("/api/v1/workspace")
def workspace(user: User = Depends(auth.require_user), db: Session = Depends(get_session)):
    return service.workspace(user, db)


@router.put("/api/v1/workspace")
def save_workspace(
    payload: WorkspacePayload,
    user: User = Depends(auth.require_user),
    db: Session = Depends(get_session),
):
    return service.save_workspace(payload, user, db)
