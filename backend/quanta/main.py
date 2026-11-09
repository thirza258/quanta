"""ASGI composition root. Business behavior lives in services and domain modules."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import quanta
from quanta.api.routes import (
    accounts,
    assistant,
    catalog,
    certificates,
    experiments,
    health,
    learning,
    research,
    simulator,
    workspace,
)
from quanta.core.http import request_guards
from quanta.db.session import initialize
from quanta.domain.errors import DomainError


@asynccontextmanager
async def lifespan(app):
    initialize()
    yield


app = FastAPI(title="Quanta API", version=quanta.__version__, lifespan=lifespan)
app.middleware("http")(request_guards)
for routes in (
    health,
    accounts,
    catalog,
    learning,
    workspace,
    research,
    experiments,
    simulator,
    assistant,
    certificates,
):
    app.include_router(routes.router)


@app.exception_handler(DomainError)
async def domain_error_response(request: Request, error: DomainError):
    return JSONResponse({"detail": error.detail}, status_code=409 if error.conflict else 422)
