"""ASGI composition root. Business behavior lives in services and domain modules."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from quanta.api.routes import accounts, catalog, health, learning, research, simulator, workspace
from quanta.core.http import request_guards
from quanta.db.session import initialize
from quanta.domain.errors import DomainError


@asynccontextmanager
async def lifespan(app):
    initialize()
    yield


app = FastAPI(title="Quanta API", version="0.1.0", lifespan=lifespan)
app.middleware("http")(request_guards)
for routes in (health, accounts, catalog, learning, workspace, research, simulator):
    app.include_router(routes.router)


@app.exception_handler(DomainError)
async def domain_error_response(request: Request, error: DomainError):
    return JSONResponse({"detail": error.detail}, status_code=409 if error.conflict else 422)
