from __future__ import annotations

import os

from fastapi import Request
from fastapi.responses import JSONResponse


async def request_guards(request: Request, call_next):
    if request.method in ("POST", "PUT", "PATCH", "DELETE"):
        origin = request.headers.get("origin")
        allowed = set(
            os.getenv(
                "ALLOWED_ORIGINS",
                "http://localhost:5173,http://127.0.0.1:5173,http://localhost:4173,http://127.0.0.1:4173,http://localhost:8080,http://127.0.0.1:8080",
            ).split(",")
        )
        if origin and origin not in allowed:
            return JSONResponse({"detail": "Origin is not allowed."}, status_code=403)
        if int(request.headers.get("content-length", "0") or 0) > 1500000:
            return JSONResponse({"detail": "Request is too large."}, status_code=413)
        body = await request.body()
        if len(body) > 1500000:
            return JSONResponse({"detail": "Request is too large."}, status_code=413)
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "same-origin"
    if request.url.path.startswith(
        ("/api/v1/auth", "/api/v1/workspace", "/api/v1/exams", "/api/v1/simulator", "/api/v1/assistant")
    ):
        response.headers["Cache-Control"] = "no-store"
    return response
