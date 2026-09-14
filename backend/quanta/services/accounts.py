from __future__ import annotations

from fastapi import HTTPException, Request, Response
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from quanta.core import auth
from quanta.db.models import User
from quanta.domain.accounts import Credentials


def register(payload: Credentials, request: Request, response: Response, db: Session):
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


def login(payload: Credentials, request: Request, response: Response, db: Session):
    user = db.exec(select(User).where(User.email == str(payload.email).lower().strip())).first()
    valid = auth.hasher.verify(payload.password, user.hashed_password if user else auth.DUMMY_HASH)
    if not user or not valid:
        raise HTTPException(401, "Email or password is incorrect.")
    auth.issue(user, response, db)
    return auth.profile(user)


def me(user: User | None):
    return auth.profile(user) if user else None


def logout(request: Request, response: Response, db: Session):
    auth.logout(request, response, db)
    return {"ok": True}
