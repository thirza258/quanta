from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from quanta.api.dependencies import owner
from quanta.core.limits import limiter
from quanta.db.session import get_session
from quanta.domain.simulator_models import (
    Advance,
    Amendment,
    Journal,
    Mutation,
    OrderCreate,
    Preferences,
    RunCreate,
)
from quanta.services import simulator as service

router = APIRouter(prefix="/api/v1/simulator", tags=["Stock simulator"])


@router.get("")
def bootstrap(account: str = Depends(owner), db: Session = Depends(get_session)):
    return service.bootstrap(account, db)


@router.get("/missions")
def missions():
    return service.missions()


@router.post("/runs")
def create_run(
    payload: RunCreate, account: str = Depends(owner), db: Session = Depends(get_session)
):
    limiter.check(f"sim-create:{account}", 30, 60)
    return service.create_run(payload, account, db)


@router.get("/runs/{run_id}")
def get_run(run_id: str, account: str = Depends(owner), db: Session = Depends(get_session)):
    return service.get_run(run_id, account, db)


@router.get("/runs/{run_id}/market")
def market(
    run_id: str,
    symbol: str,
    interval: Literal["1m", "5m", "15m", "1h", "1D"] = "1m",
    cursor: int | None = Query(default=None, ge=0),
    indicators: str | None = Query(default=None, max_length=200),
    limit: int = Query(default=1500, ge=50, le=5000),
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    return service.market(run_id, symbol, interval, cursor, indicators, limit, account, db)


@router.get("/runs/{run_id}/news")
def news(
    run_id: str,
    symbol: str | None = Query(default=None, max_length=20),
    limit: int = Query(default=60, ge=1, le=200),
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    return service.news(run_id, symbol, limit, account, db)


@router.get("/runs/{run_id}/fundamentals")
def fundamentals(
    run_id: str,
    symbol: str = Query(max_length=20),
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    return service.fundamentals(run_id, symbol, account, db)


@router.get("/runs/{run_id}/mission")
def mission(run_id: str, account: str = Depends(owner), db: Session = Depends(get_session)):
    return service.mission(run_id, account, db)


@router.get("/runs/{run_id}/calendar")
def calendar(
    run_id: str,
    ahead: int | None = Query(default=None, ge=1, le=7800),
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    return service.calendar(run_id, ahead, account, db)


@router.get("/runs/{run_id}/desk")
def desk_view(run_id: str, account: str = Depends(owner), db: Session = Depends(get_session)):
    return service.desk_view(run_id, account, db)


@router.get("/runs/{run_id}/monitor")
def monitor(
    run_id: str,
    panes: str = Query(max_length=120),
    symbol: str = Query(max_length=20),
    screen: str = Query(default="all", max_length=20),
    limit: int = Query(default=40, ge=1, le=200),
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    return service.monitor(run_id, panes, symbol, screen, limit, account, db)


@router.get("/runs/{run_id}/analytics")
def analytics(
    run_id: str,
    symbol: str = Query(max_length=20),
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    return service.analytics(run_id, symbol, account, db)


@router.post("/runs/{run_id}/orders")
def order_create(
    run_id: str,
    payload: OrderCreate,
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    limiter.check(f"sim-order:{account}", 120, 60)
    return service.order_create(run_id, payload, account, db)


@router.post("/runs/{run_id}/advance")
def advance(
    run_id: str, payload: Advance, account: str = Depends(owner), db: Session = Depends(get_session)
):
    limiter.check(f"sim-advance:{account}", 600, 60)
    return service.advance(run_id, payload, account, db)


@router.post("/runs/{run_id}/orders/{order_id}/cancel")
def cancel(
    run_id: str,
    order_id: str,
    payload: Mutation,
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    return service.cancel(run_id, order_id, payload, account, db)


@router.post("/runs/{run_id}/orders/{order_id}/amend")
def amend(
    run_id: str,
    order_id: str,
    payload: Amendment,
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    return service.amend(run_id, order_id, payload, account, db)


@router.put("/runs/{run_id}/preferences")
def preferences(
    run_id: str,
    payload: Preferences,
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    return service.preferences(run_id, payload, account, db)


@router.put("/runs/{run_id}/orders/{order_id}/journal")
def journal(
    run_id: str,
    order_id: str,
    payload: Journal,
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    return service.journal(run_id, order_id, payload, account, db)
