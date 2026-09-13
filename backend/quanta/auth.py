import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, Request, Response
from pwdlib import PasswordHash
from sqlmodel import Session

from .database import STORAGE, AuthSession, User, get_session

hasher = PasswordHash.recommended()
secret_path = STORAGE / "jwt-secret"
if os.getenv("JWT_SECRET"):
    SECRET = os.environ["JWT_SECRET"]
else:
    try:
        fd = os.open(secret_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w") as file:
            file.write(secrets.token_urlsafe(48))
    except FileExistsError:
        pass
    SECRET = secret_path.read_text()
if len(SECRET) < 32:
    raise RuntimeError("JWT_SECRET must contain at least 32 characters.")
DUMMY_HASH = hasher.hash(secrets.token_urlsafe(24))
COOKIE = "quanta_session"


def issue(user: User, response: Response, db: Session):
    expires = datetime.now(timezone.utc) + timedelta(days=7)
    sid = secrets.token_urlsafe(32)
    db.add(AuthSession(id=sid, user_id=user.id, expires_at=int(expires.timestamp())))
    db.commit()
    token = jwt.encode(
        {
            "sub": user.id,
            "jti": sid,
            "exp": expires,
            "iss": "quanta",
            "aud": "quanta-web",
        },
        SECRET,
        algorithm="HS256",
    )
    response.set_cookie(
        COOKIE,
        token,
        httponly=True,
        secure=os.getenv("COOKIE_SECURE", "false").lower() == "true",
        samesite="strict",
        max_age=7 * 86400,
        path="/",
    )


def optional_user(request: Request, db: Session = Depends(get_session)) -> User | None:
    token = request.cookies.get(COOKIE)
    if not token:
        return None
    try:
        claims = jwt.decode(
            token,
            SECRET,
            algorithms=["HS256"],
            issuer="quanta",
            audience="quanta-web",
            options={"require": ["exp", "sub", "jti"]},
        )
        session = db.get(AuthSession, claims["jti"])
        if (
            not session
            or session.user_id != claims["sub"]
            or session.expires_at < int(datetime.now(timezone.utc).timestamp())
        ):
            return None
        return db.get(User, claims["sub"])
    except jwt.PyJWTError:
        return None


def require_user(user: User | None = Depends(optional_user)) -> User:
    if not user:
        raise HTTPException(401, "Sign in to access your saved account workspace.")
    return user


def logout(request: Request, response: Response, db: Session):
    try:
        claims = jwt.decode(
            request.cookies.get(COOKIE, ""),
            SECRET,
            algorithms=["HS256"],
            issuer="quanta",
            audience="quanta-web",
        )
        session = db.get(AuthSession, claims["jti"])
        if session:
            db.delete(session)
            db.commit()
    except jwt.PyJWTError:
        pass
    response.delete_cookie(COOKIE, path="/")


def profile(user: User):
    return {"id": user.id, "email": user.email, "name": user.name}
