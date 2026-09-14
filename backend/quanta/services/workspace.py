from __future__ import annotations

import json
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from quanta.db.models import User, Workspace
from quanta.domain.accounts import WorkspacePayload


def workspace(user: User, db: Session):
    item = db.get(Workspace, user.id)
    return {"version": item.version, "state": item.state} if item else {"version": 0, "state": {}}


def save_workspace(payload: WorkspacePayload, user: User, db: Session):
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
