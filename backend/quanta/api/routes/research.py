from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from quanta.api.dependencies import key
from quanta.core import auth
from quanta.core.limits import limiter
from quanta.db.models import User
from quanta.domain import analytics, broker
from quanta.domain.econometrics import FactorRequest, PortfolioRequest
from quanta.services import research as service

router = APIRouter(tags=["Research"])


@router.get("/api/v1/data/catalog")
def datasets():
    return service.datasets()


@router.post("/api/v1/data/synthetic/generate")
def generate(
    payload: analytics.DatasetParams,
    request: Request,
    user: User | None = Depends(auth.optional_user),
):
    limiter.check(key(request, "compute", user))
    return service.generate(payload)


@router.post("/api/v1/sandbox/execute")
def execute(
    payload: analytics.ExecuteRequest,
    request: Request,
    user: User | None = Depends(auth.optional_user),
):
    limiter.check(key(request, "compute", user))
    return service.execute(payload)


@router.post("/api/v1/analytics/valuation")
def valuation(payload: analytics.ValuationRequest):
    return service.valuation(payload)


@router.post("/api/v1/analytics/amm")
def amm(payload: analytics.AmmRequest):
    return service.amm(payload)


@router.post("/api/v1/broker/order")
def order(payload: broker.OrderRequest):
    return service.order(payload)


@router.post("/api/v1/analytics/factors")
def factors(
    payload: FactorRequest,
    request: Request,
    user: User | None = Depends(auth.optional_user),
):
    limiter.check(key(request, "compute", user))
    return service.factors(payload)


@router.post("/api/v1/analytics/portfolio")
def optimize(
    payload: PortfolioRequest,
    request: Request,
    user: User | None = Depends(auth.optional_user),
):
    limiter.check(key(request, "compute", user))
    return service.optimize(payload)
