import uuid
from typing import Literal

from pydantic import BaseModel, Field


class BrokerState(BaseModel):
    cash: float = Field(100000, ge=0, le=1e12, allow_inf_nan=False)
    quantity: float = Field(0, ge=0, le=1e12, allow_inf_nan=False)
    initial_equity: float = Field(100000, gt=0, le=1e12, allow_inf_nan=False)
    halted: bool = False


class OrderRequest(BaseModel):
    state: BrokerState = Field(default_factory=BrokerState)
    side: Literal["buy", "sell"] = "buy"
    quantity: float = Field(10, gt=0, le=1e8, allow_inf_nan=False)
    price: float = Field(100, gt=0, le=1e8, allow_inf_nan=False)
    volume: float = Field(1000, ge=0, le=1e12, allow_inf_nan=False)
    participation: float = Field(0.1, gt=0, le=1, allow_inf_nan=False)
    commission_bps: float = Field(5, ge=0, le=500, allow_inf_nan=False)
    slippage_bps: float = Field(3, ge=0, le=500, allow_inf_nan=False)
    spread_bps: float = Field(5, ge=0, le=10000, allow_inf_nan=False)
    data_age_seconds: float = Field(0, ge=0, le=1e9, allow_inf_nan=False)
    max_drawdown: float = Field(0.025, gt=0, le=1, allow_inf_nan=False)


def place(p: OrderRequest):
    state = p.state.model_copy()
    equity = state.cash + state.quantity * p.price
    reason = None
    if state.halted:
        reason = "Circuit breaker is halted. Reset the paper account after reviewing the event."
    elif equity < state.initial_equity * (1 - p.max_drawdown):
        state.halted = True
        reason = "Drawdown circuit breaker triggered."
    elif p.data_age_seconds > 60:
        reason = "Price data is stale."
    elif p.spread_bps > 100:
        reason = "Spread exceeds the 100 bps guard."
    fill = min(p.quantity, p.volume * p.participation)
    price = p.price * (
        1 + (p.slippage_bps + p.spread_bps / 2) / 10000 * (1 if p.side == "buy" else -1)
    )
    commission = fill * price * p.commission_bps / 10000
    if not reason and fill <= 0:
        reason = "No available liquidity."
    if not reason and p.side == "buy" and fill * price + commission > state.cash:
        reason = "Insufficient cash for the simulated fill and fees."
    if not reason and p.side == "sell" and fill > state.quantity:
        reason = "Insufficient shares. This broker is long-only."
    if reason:
        return {
            "id": uuid.uuid4().hex,
            "status": "rejected",
            "reason": reason,
            "filled": 0,
            "remaining": p.quantity,
            "price": price,
            "commission": 0,
            "state": state.model_dump(),
            "side": p.side,
        }
    if p.side == "buy":
        state.cash -= fill * price + commission
        state.quantity += fill
    else:
        state.cash += fill * price - commission
        state.quantity -= fill
    return {
        "id": uuid.uuid4().hex,
        "status": "filled" if fill == p.quantity else "partially_filled",
        "reason": None,
        "filled": fill,
        "remaining": p.quantity - fill,
        "price": price,
        "commission": commission,
        "state": state.model_dump(),
        "side": p.side,
    }
