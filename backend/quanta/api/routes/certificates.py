from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from quanta.api.dependencies import key
from quanta.core import auth
from quanta.core.limits import limiter
from quanta.db.models import User
from quanta.db.session import get_session
from quanta.services import certificates as service

router = APIRouter(tags=["Certifications"])


@router.get("/api/v1/certificates")
def list_certificates(user: User = Depends(auth.require_user), db: Session = Depends(get_session)):
    return service.list_certificates(user, db)


@router.post("/api/v1/certificates")
def claim(
    payload: service.CertificateClaim,
    request: Request,
    user: User = Depends(auth.require_user),
    db: Session = Depends(get_session),
):
    limiter.check(key(request, "certificate-claim", user), 20, 60)
    return service.claim(payload, user, db)


@router.get("/api/v1/certificates/{identifier}/verify")
def verify(identifier: str, request: Request, db: Session = Depends(get_session)):
    limiter.check(key(request, "certificate-verification", None), 120, 60)
    return service.verify(identifier, db)
