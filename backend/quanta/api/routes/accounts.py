from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response
from sqlmodel import Session

from quanta.api.dependencies import key
from quanta.core import auth
from quanta.core.limits import limiter
from quanta.db.models import User
from quanta.db.session import get_session
from quanta.domain.accounts import Credentials
from quanta.services import accounts as service

router = APIRouter(tags=["Accounts"])


@router.post("/api/v1/auth/register", status_code=201)
def register(
    payload: Credentials,
    request: Request,
    response: Response,
    db: Session = Depends(get_session),
):
    limiter.check(key(request, "auth"), 10, 60)
    return service.register(payload, request, response, db)


@router.post("/api/v1/auth/login")
def login(
    payload: Credentials,
    request: Request,
    response: Response,
    db: Session = Depends(get_session),
):
    limiter.check(key(request, "auth"), 10, 60)
    return service.login(payload, request, response, db)


@router.get("/api/v1/auth/me")
def me(user: User | None = Depends(auth.optional_user)):
    return service.me(user)


@router.post("/api/v1/auth/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_session)):
    return service.logout(request, response, db)
