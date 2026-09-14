from fastapi import APIRouter, Depends, Request, Response

from quanta.api.dependencies import key
from quanta.core import auth
from quanta.core.limits import limiter
from quanta.db.models import User
from quanta.domain.assistant import AssistantBundle, AssistantReply, AssistantRequest
from quanta.services import assistant as service

router = APIRouter(prefix="/api/v1/assistant", tags=["Course assistant"])


@router.get("/status")
def status():
    return service.status()


@router.post("/chat", response_model=AssistantReply)
async def chat(payload: AssistantRequest, request: Request, user: User | None = Depends(auth.optional_user)):
    limiter.check(key(request, "assistant-minute", user), maximum=10)
    limiter.check(key(request, "assistant-hour", user), maximum=40, seconds=3600)
    limiter.check(key(request, "assistant-ip"), maximum=60, seconds=3600)
    return await service.reply(payload)


@router.post("/bundle")
def bundle(payload: AssistantBundle, request: Request, user: User | None = Depends(auth.optional_user)):
    limiter.check(key(request, "assistant-download", user), maximum=30)
    return Response(
        service.bundle(payload), media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="quanta-project.zip"'},
    )
