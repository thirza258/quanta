from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response
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


@router.get("/api/v1/certificates/{identifier}/pdf")
def download_pdf(identifier: str, request: Request, db: Session = Depends(get_session)):
    limiter.check(key(request, "certificate-pdf", None), 60, 60)
    pdf_bytes, filename = service.generate_pdf(identifier, db)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/api/v1/certificates/{identifier}/privacy")
def set_privacy(
    identifier: str,
    payload: dict,
    user: User = Depends(auth.require_user),
    db: Session = Depends(get_session),
):
    opt_out = bool(payload.get("publicVerificationOptOut", False))
    return service.set_privacy(identifier, opt_out, user, db)

