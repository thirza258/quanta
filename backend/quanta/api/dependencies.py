from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import jwt
from fastapi import Depends, Request, Response

from quanta.core import auth
from quanta.db.models import User


def key(request: Request, scope: str, user: User | None = None):
    return f"{scope}:{user.id if user else request.client.host if request.client else 'unknown'}"


def owner(request: Request, response: Response, user: User | None = Depends(auth.optional_user)):
    if user:
        return user.id
    token = request.cookies.get("quanta_trading_guest", "")
    try:
        claims = jwt.decode(
            token,
            auth.SECRET,
            algorithms=["HS256"],
            audience="quanta-trading-guest",
            issuer="quanta",
            options={"require": ["exp", "sub"]},
        )
        return "guest:" + str(UUID(claims["sub"]))
    except jwt.PyJWTError, ValueError, KeyError:
        guest = str(uuid4())
        token = jwt.encode(
            {
                "sub": guest,
                "iss": "quanta",
                "aud": "quanta-trading-guest",
                "exp": datetime.now(timezone.utc) + timedelta(days=30),
            },
            auth.SECRET,
            algorithm="HS256",
        )
        response.set_cookie(
            "quanta_trading_guest",
            token,
            max_age=30 * 86400,
            httponly=True,
            samesite="strict",
            path="/",
            secure=os.getenv("COOKIE_SECURE", "false").lower() == "true",
        )
        return "guest:" + guest
