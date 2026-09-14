"""Persistent, deterministic long/cash paper trading. Monetary ledger uses Decimal."""

import copy
import hashlib
import json
import math
import os
import random
from datetime import datetime, timedelta, timezone
from decimal import ROUND_CEILING, ROUND_DOWN, ROUND_HALF_UP, Decimal
from functools import lru_cache
from typing import Literal
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

import jwt
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from pydantic import BaseModel, ConfigDict, Field, StrictInt
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from . import auth, data_store
from .database import TradingDataset, TradingRun, User, get_session
from .limits import limiter

router = APIRouter(prefix="/api/v1/simulator", tags=["Stock simulator"])
SYMBOLS = {
    "AAPL": ("Apple", 224),
    "MSFT": ("Microsoft", 418),
    "NVDA": ("NVIDIA", 128),
    "TSLA": ("Tesla", 245),
    "AMZN": ("Amazon", 195),
    "META": ("Meta Platforms", 530),
}
OPEN = {"working", "partially_filled"}
CENT = Decimal("0.01")


def dec(value):
    return Decimal(str(value))


def money(value):
    return str(dec(value).quantize(CENT, rounding=ROUND_HALF_UP))


def now():
    return datetime.now(timezone.utc).isoformat()


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RunCreate(Model):
    id: UUID
    mode: Literal["synthetic", "historical"] = "synthetic"
    seed: StrictInt = Field(default=42, ge=0, le=1000000)
    symbol: str | None = Field(default=None, max_length=20)
    commission: Decimal = Field(default=Decimal("1"), ge=0, le=100, decimal_places=2)
    slippage_bps: Decimal = Field(default=Decimal("2"), ge=0, le=100)
    spread_bps: Decimal = Field(default=Decimal("2"), ge=0, le=100)
    participation: Decimal = Field(default=Decimal("0.01"), gt=0, le=1)


class Mutation(Model):
    id: UUID
    version: StrictInt = Field(ge=0)


class OrderCreate(Mutation):
    symbol: str = Field(max_length=20)
    side: Literal["buy", "sell"]
    kind: Literal["market", "limit", "stop", "stop_limit"] = "market"
    quantity: StrictInt = Field(gt=0, le=1000000)
    limit_price: Decimal | None = Field(default=None, gt=0, le=100000000, decimal_places=2)
    stop_price: Decimal | None = Field(default=None, gt=0, le=100000000, decimal_places=2)
    tif: Literal["DAY", "GTC"] = "GTC"
    note: str = Field(default="", max_length=2000)
    lesson: str = Field(default="", max_length=40)


class Advance(Mutation):
    steps: StrictInt = Field(default=1, ge=1, le=390)


class Amendment(Mutation):
    limit_price: Decimal | None = Field(default=None, gt=0, le=100000000, decimal_places=2)
    stop_price: Decimal | None = Field(default=None, gt=0, le=100000000, decimal_places=2)


class Preferences(Mutation):
    preferences: dict


class Journal(Mutation):
    note: str = Field(max_length=2000)
    lesson: str = Field(default="", max_length=40)


def owner(request: Request, response: Response, user: User | None = Depends(auth.optional_user)):
    if user:
        return user.id
    token = request.cookies.get("quanta_trading_guest", "")
    try:
        claims = jwt.decode(
            token,
            auth.SECRET,
            algorithms=["HS256"],
            audience="quanta-trading-guest",
            issuer="quanta",
            options={"require": ["exp", "sub"]},
        )
        return "guest:" + str(UUID(claims["sub"]))
    except jwt.PyJWTError, ValueError, KeyError:
        guest = str(uuid4())
        token = jwt.encode(
            {
                "sub": guest,
                "iss": "quanta",
                "aud": "quanta-trading-guest",
                "exp": datetime.now(timezone.utc) + timedelta(days=30),
            },
            auth.SECRET,
            algorithm="HS256",
        )
        response.set_cookie(
            "quanta_trading_guest",
            token,
            max_age=30 * 86400,
            httponly=True,
            samesite="strict",
            path="/",
            secure=os.getenv("COOKIE_SECURE", "false").lower() == "true",
        )
        return "guest:" + guest


@lru_cache(maxsize=12)
def synthetic(seed):
    """Six fictional price paths, 6,000 minute observations, weekday-only calendar."""
    start = datetime(2025, 1, 6, 9, 30, tzinfo=ZoneInfo("America/New_York"))
    times = []
    date = start
    while len(times) < 6000:
        if date.weekday() < 5:
            times.extend(int((date + timedelta(minutes=i)).timestamp()) for i in range(390))
        date += timedelta(days=1)
    times = times[:6000]
    output = {}
    for number, (symbol, (_, initial)) in enumerate(SYMBOLS.items()):
        rng = random.Random(seed + number * 100003)
        price = initial
        rows = []
        for i, stamp in enumerate(times):
            opening = price * math.exp(rng.gauss(0, 0.0008 if i % 390 else 0.006))
            closing = opening * math.exp(rng.gauss(0.000015, 0.0018))
            high = max(opening, closing) * (1 + rng.random() * 0.0015)
            low = min(opening, closing) * (1 - rng.random() * 0.0015)
            rows.append(
                {
                    "time": stamp,
                    "open": round(opening, 2),
                    "high": round(high, 2),
                    "low": round(low, 2),
                    "close": round(closing, 2),
                    "volume": rng.randint(2000, 30000),
                }
            )
            price = closing
        output[symbol] = rows
    return output


def markets(state, db):
    config = state["config"]
    if config["mode"] == "synthetic":
        return synthetic(config["seed"])
    dataset = db.get(TradingDataset, config["dataset_id"])
    if not dataset:
        raise HTTPException(503, "The run's historical data snapshot is unavailable.")
    return {config["symbol"]: dataset.bars}


def run_for(db, run_id, account):
    run = db.get(TradingRun, run_id)
    if not run or run.owner != account:
        raise HTTPException(404, "Trading run not found.")
    return run


def latest(db, account):
    return db.exec(
        select(TradingRun)
        .where(TradingRun.owner == account)
        .order_by(TradingRun.created_at.desc(), TradingRun.id.desc())
    ).first()


def bar_at(data, symbol, index):
    if symbol not in data:
        raise HTTPException(422, "This stock is unavailable in this run.")
    return data[symbol][index]


def reservations(state, exclude=None):
    cash = Decimal(0)
    shares = {}
    for order in state["orders"]:
        if order["id"] == exclude or order["status"] not in OPEN:
            continue
        remaining = order["quantity"] - order["filled"]
        if order["side"] == "buy":
            cash += dec(order["reserve_price"]) * remaining + dec(order["fee_remaining"])
        else:
            shares[order["symbol"]] = shares.get(order["symbol"], 0) + remaining
    return cash, shares


def snapshot(run, db):
    state = run.state
    data = markets(state, db)
    reserved, share_reservations = reservations(state)
    quotes = []
    for symbol, rows in data.items():
        bar = rows[state["cursor"]]
        # Change against the prior session close, or the first available opening.
        day = datetime.fromtimestamp(bar["time"], ZoneInfo("America/New_York")).date()
        prior = next(
            (
                row["close"]
                for row in reversed(rows[: state["cursor"]])
                if datetime.fromtimestamp(row["time"], ZoneInfo("America/New_York")).date() < day
            ),
            rows[0]["open"],
        )
        quotes.append(
            {
                "symbol": symbol,
                "name": SYMBOLS.get(symbol, (symbol,))[0],
                **bar,
                "change": round(bar["close"] - prior, 2),
                "change_pct": round((bar["close"] / prior - 1) * 100, 2),
            }
        )
    positions = []
    equity = dec(state["cash"])
    for symbol, position in state["positions"].items():
        if not position["quantity"]:
            continue
        mark = dec(bar_at(data, symbol, state["cursor"])["close"])
        value = mark * position["quantity"]
        equity += value
        positions.append(
            {
                "symbol": symbol,
                **position,
                "mark": money(mark),
                "market_value": money(value),
                "average": money(dec(position["cost"]) / position["quantity"]),
                "unrealized": money(value - dec(position["cost"])),
                "available": position["quantity"] - share_reservations.get(symbol, 0),
            }
        )
    return {
        "id": run.id,
        "version": run.version,
        "created_at": run.created_at,
        "guest": run.owner.startswith("guest:"),
        "cursor": state["cursor"],
        "total_bars": len(next(iter(data.values()))),
        "clock": quotes[0]["time"],
        "config": state["config"],
        "cash": state["cash"],
        "reserved": money(reserved),
        "available": money(dec(state["cash"]) - reserved),
        "equity": money(equity),
        "realized": state["realized"],
        "quotes": quotes,
        "positions": positions,
        "orders": state["orders"],
        "fills": state["fills"],
        "ledger": state["ledger"],
        "preferences": state.get("preferences", {}),
    }


def validate_order(state, data, order, exclude=None):
    mark = dec(bar_at(data, order["symbol"], state["cursor"])["close"])
    if order["kind"] in ("limit", "stop_limit") and not order.get("limit_price"):
        raise HTTPException(422, "A limit price is required.")
    if order["kind"] in ("stop", "stop_limit") and not order.get("stop_price"):
        raise HTTPException(422, "A stop trigger price is required.")
    if order["kind"] not in ("limit", "stop_limit") and order.get("limit_price"):
        raise HTTPException(422, "This order type does not accept a limit price.")
    if order["kind"] not in ("stop", "stop_limit") and order.get("stop_price"):
        raise HTTPException(422, "This order type does not accept a stop price.")
    reserve_price = dec(order.get("limit_price") or max(mark, dec(order.get("stop_price") or mark)))
    if order["kind"] not in ("limit", "stop_limit"):
        reserve_price *= (
            1
            + (dec(state["config"]["slippage_bps"]) + dec(state["config"]["spread_bps"]) / 2)
            / 10000
        )
    reserve_price = reserve_price.quantize(CENT, rounding=ROUND_CEILING)
    order["reserve_price"] = money(reserve_price)
    cash, shares = reservations(state, exclude)
    remaining = order["quantity"] - order["filled"]
    if (
        order["side"] == "buy"
        and reserve_price * remaining + dec(order["fee_remaining"]) > dec(state["cash"]) - cash
    ):
        raise HTTPException(
            422, "Insufficient available cash, including fees and other working orders."
        )
    if order["side"] == "sell" and remaining > state["positions"].get(order["symbol"], {}).get(
        "quantity", 0
    ) - shares.get(order["symbol"], 0):
        raise HTTPException(422, "Insufficient available shares. This paper account is long-only.")


def execution_price(order, bar):
    buy = order["side"] == "buy"
    kind = order["kind"]
    opening, high, low = (dec(bar[key]) for key in ("open", "high", "low"))
    if kind in ("stop", "stop_limit") and not order["triggered"]:
        stop = dec(order["stop_price"])
        if high < stop if buy else low > stop:
            return None
        order["triggered"] = True
        if kind == "stop_limit":
            # The intrabar path is unknown. Trigger now; earliest fill next bar.
            return None
        return max(opening, stop) if buy else min(opening, stop)
    if kind in ("limit", "stop_limit"):
        limit = dec(order["limit_price"])
        # A touch alone does not fill a passive order in this conservative bar model.
        if opening <= limit if buy else opening >= limit:
            return min(opening, limit) if buy else max(opening, limit)
        if low < limit if buy else high > limit:
            return limit
        return None
    return opening


def advance_state(state, data, steps):
    last = len(next(iter(data.values()))) - 1
    for _ in range(min(steps, last - state["cursor"])):
        state["cursor"] += 1
        used = {}
        for order in state["orders"]:
            if order["status"] not in OPEN:
                continue
            bar = bar_at(data, order["symbol"], state["cursor"])
            day = (
                datetime.fromtimestamp(bar["time"], ZoneInfo("America/New_York")).date().isoformat()
            )
            if order["tif"] == "DAY" and order["day"] != day:
                order.update(status="expired", reason="DAY order expired at the session boundary.")
                continue
            price = execution_price(order, bar)
            if price is None:
                continue
            friction = (
                dec(state["config"]["slippage_bps"]) + dec(state["config"]["spread_bps"]) / 2
            ) / 10000
            price *= 1 + friction if order["side"] == "buy" else 1 - friction
            if order["kind"] in ("limit", "stop_limit"):
                price = (
                    min(price, dec(order["limit_price"]))
                    if order["side"] == "buy"
                    else max(price, dec(order["limit_price"]))
                )
            price = max(CENT, dec(money(price)))
            capacity = int(dec(bar["volume"]) * dec(state["config"]["participation"]))
            quantity = min(
                order["quantity"] - order["filled"], max(0, capacity - used.get(order["symbol"], 0))
            )
            if not quantity:
                continue
            fee = dec(order["fee_remaining"])
            if order["side"] == "buy":
                reserved, _ = reservations(state, order["id"])
                affordable = max(
                    0,
                    int(
                        ((dec(state["cash"]) - reserved - fee) / price).to_integral_value(
                            rounding=ROUND_DOWN
                        )
                    ),
                )
                quantity = min(quantity, affordable)
                if quantity == 0:
                    order.update(
                        status="rejected", reason="The execution price gap exceeded available cash."
                    )
                    continue
            if order["side"] == "sell":
                reserved, _ = reservations(state, order["id"])
                if dec(state["cash"]) + price * quantity - fee < reserved:
                    order.update(
                        status="rejected",
                        reason="Sale proceeds and available cash cannot cover the commission.",
                    )
                    continue
            position = state["positions"].setdefault(
                order["symbol"], {"quantity": 0, "cost": "0.00"}
            )
            notional = price * quantity
            realized = Decimal(0)
            if order["side"] == "buy":
                change = -notional - fee
                position["quantity"] += quantity
                position["cost"] = money(dec(position["cost"]) + notional + fee)
            else:
                # All cost is allocated on the final exit so rounding cannot leave a residue.
                basis = (
                    dec(position["cost"])
                    if quantity == position["quantity"]
                    else dec(money(dec(position["cost"]) * quantity / position["quantity"]))
                )
                change = notional - fee
                realized = change - basis
                position["quantity"] -= quantity
                position["cost"] = money(dec(position["cost"]) - basis)
                state["realized"] = money(dec(state["realized"]) + realized)
            state["cash"] = money(dec(state["cash"]) + change)
            order["notional"] = money(dec(order["notional"]) + notional)
            order["filled"] += quantity
            order["average"] = money(dec(order["notional"]) / order["filled"])
            order["fee_remaining"] = "0.00"
            order["status"] = (
                "filled" if order["filled"] == order["quantity"] else "partially_filled"
            )
            order["reason"] = (
                "Filled on the next eligible bar, subject to shared volume participation."
            )
            used[order["symbol"]] = used.get(order["symbol"], 0) + quantity
            fill = {
                "id": str(uuid4()),
                "order_id": order["id"],
                "symbol": order["symbol"],
                "side": order["side"],
                "quantity": quantity,
                "price": money(price),
                "fee": money(fee),
                "realized": money(realized),
                "time": bar["time"],
                "note": order["note"],
                "lesson": order["lesson"],
            }
            state["fills"].append(fill)
            state["ledger"].append(
                {
                    "id": fill["id"],
                    "time": bar["time"],
                    "type": "trade_fill",
                    "description": f"{order['side'].title()} {quantity} {order['symbol']}",
                    "amount": money(change),
                    "cash": state["cash"],
                }
            )
            # Reserve the remaining quantity at the current estimate; close if no longer affordable.
            if order["status"] in OPEN:
                try:
                    validate_order(state, data, order, order["id"])
                except HTTPException:
                    order.update(
                        status="canceled",
                        reason="Remaining quantity canceled: insufficient buying power after the gap fill.",
                    )
    # At a session's last known bar, DAY orders cannot remain working overnight.
    cursor = state["cursor"]
    for order in state["orders"]:
        if order["status"] in OPEN and order["tif"] == "DAY":
            rows = data[order["symbol"]]
            if (
                cursor == last
                or datetime.fromtimestamp(rows[cursor]["time"], ZoneInfo("America/New_York")).date()
                != datetime.fromtimestamp(
                    rows[cursor + 1]["time"], ZoneInfo("America/New_York")
                ).date()
            ):
                order.update(
                    status="expired", reason="DAY order expired at the end of its session."
                )


def mutate(db, run_id, account, payload, action, operation):
    run = run_for(db, run_id, account)
    digest = hashlib.sha256(
        json.dumps(
            {"action": action, **payload.model_dump(mode="json", exclude={"version"})},
            sort_keys=True,
        ).encode()
    ).hexdigest()
    previous = run.state["requests"].get(str(payload.id))
    if previous:
        if previous != digest:
            raise HTTPException(
                409, "This request identifier was already used for a different action."
            )
        return snapshot(run, db)
    active = latest(db, account)
    if active.id != run.id:
        raise HTTPException(409, "This run is archived. Open the current run to trade.")
    if run.version != payload.version:
        raise HTTPException(
            409, "This account changed in another session. Refresh before retrying."
        )
    if len(run.state["requests"]) >= 20000:
        raise HTTPException(
            422, "This run reached its action limit. Export it and start a new run."
        )
    state = copy.deepcopy(run.state)
    operation(state, markets(state, db))
    state["requests"][str(payload.id)] = digest
    changed = db.execute(
        update(TradingRun)
        .where(TradingRun.id == run.id, TradingRun.version == payload.version)
        .values(state=state, version=payload.version + 1)
    )
    if changed.rowcount != 1:
        db.rollback()
        raise HTTPException(
            409, "A concurrent action updated this account. Refresh before retrying."
        )
    db.commit()
    db.refresh(run)
    return snapshot(run, db)


@router.get("")
def bootstrap(account: str = Depends(owner), db: Session = Depends(get_session)):
    runs = db.exec(
        select(TradingRun)
        .where(TradingRun.owner == account)
        .order_by(TradingRun.created_at.desc(), TradingRun.id.desc())
    ).all()
    return {
        "run": snapshot(runs[0], db) if runs else None,
        "runs": [
            {"id": r.id, "created_at": r.created_at, "mode": r.state["config"]["mode"]}
            for r in runs
        ],
        "historical": data_store.catalog(),
        "symbols": [{"symbol": s, "name": value[0]} for s, value in SYMBOLS.items()],
    }


@router.post("/runs")
def create_run(
    payload: RunCreate, account: str = Depends(owner), db: Session = Depends(get_session)
):
    limiter.check(f"sim-create:{account}", 30, 60)
    existing = db.get(TradingRun, str(payload.id))
    config = payload.model_dump(mode="json", exclude={"id"})
    if existing:
        if existing.owner != account or existing.state["requested_config"] != config:
            raise HTTPException(409, "Run identifier is already in use.")
        return snapshot(existing, db)
    requested_config = copy.deepcopy(config)
    config["execution_profile"] = "cash-whole-shares-v1"
    if payload.mode == "historical":
        try:
            bars = data_store.historical(payload.symbol, 40)
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from None
        bars = [
            {
                **{key: float(bar[key]) for key in ("open", "high", "low", "close", "volume")},
                "time": int(
                    datetime.fromisoformat(bar["time"])
                    .replace(hour=16, minute=0, second=0, tzinfo=ZoneInfo("America/New_York"))
                    .timestamp()
                ),
            }
            for bar in bars
        ]
        dataset_id = hashlib.sha256(json.dumps(bars, sort_keys=True).encode()).hexdigest()
        if not db.get(TradingDataset, dataset_id):
            db.add(TradingDataset(id=dataset_id, bars=bars))
            try:
                db.commit()
            except IntegrityError:
                db.rollback()
        config.update(
            dataset_id=dataset_id,
            base_interval="1D",
            source="Imported OHLCV · corporate-action treatment undeclared · prices used as supplied; no split or dividend adjustments applied by this engine",
        )
        cursor = min(30, len(bars) - 2)
    else:
        config.update(
            base_interval="1m",
            source="Seeded synthetic prices · fictional market paths · weekday-only calendar",
        )
        cursor = 499
    state = {
        "config": config,
        "requested_config": requested_config,
        "cursor": cursor,
        "cash": "100000.00",
        "realized": "0.00",
        "positions": {},
        "orders": [],
        "fills": [],
        "ledger": [
            {
                "id": str(uuid4()),
                "type": "opening_balance",
                "description": "Virtual opening balance",
                "amount": "100000.00",
                "cash": "100000.00",
                "time": None,
            }
        ],
        "requests": {},
        "preferences": {},
    }
    prior = latest(db, account)
    if prior:
        # Reset and order writes contend on the same version in one transaction.
        # This also works on SQLite, where SELECT FOR UPDATE is ignored.
        changed = db.execute(
            update(TradingRun)
            .where(TradingRun.id == prior.id, TradingRun.version == prior.version)
            .values(version=prior.version + 1)
        )
        if changed.rowcount != 1:
            db.rollback()
            raise HTTPException(409, "Account changed during reset. Retry the new run.")
        state["preferences"] = copy.deepcopy(prior.state.get("preferences", {}))
        state["preferences"].pop("drawings", None)
        state["preferences"].pop("ticket", None)
    run = TradingRun(id=str(payload.id), owner=account, state=state)
    db.add(run)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Run created concurrently. Reload the terminal.") from None
    db.refresh(run)
    return snapshot(run, db)


@router.get("/runs/{run_id}")
def get_run(run_id: str, account: str = Depends(owner), db: Session = Depends(get_session)):
    return snapshot(run_for(db, run_id, account), db)


@router.get("/runs/{run_id}/market")
def market(
    run_id: str,
    symbol: str,
    interval: Literal["1m", "5m", "15m", "1h", "1D"] = "1m",
    cursor: int | None = Query(default=None, ge=0),
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    run = run_for(db, run_id, account)
    state = run.state
    data = markets(state, db)
    bar_at(data, symbol, state["cursor"])
    if state["config"]["base_interval"] == "1D" and interval != "1D":
        raise HTTPException(422, "This dataset only supports daily bars.")
    cursor = state["cursor"] if cursor is None else min(cursor, state["cursor"])
    rows = data[symbol][: cursor + 1]
    if interval != "1m" and state["config"]["base_interval"] != "1D":
        grouped = {}
        size = {"5m": 300, "15m": 900, "1h": 3600, "1D": 86400}[interval]
        for bar in rows:
            session_start = datetime.fromtimestamp(
                bar["time"], ZoneInfo("America/New_York")
            ).replace(hour=9, minute=30, second=0)
            anchor = int(session_start.timestamp())
            timestamp = (
                anchor if interval == "1D" else anchor + (bar["time"] - anchor) // size * size
            )
            if timestamp not in grouped:
                grouped[timestamp] = {**bar, "time": timestamp}
            else:
                item = grouped[timestamp]
                item.update(
                    high=max(item["high"], bar["high"]),
                    low=min(item["low"], bar["low"]),
                    close=bar["close"],
                    volume=item["volume"] + bar["volume"],
                )
        rows = list(grouped.values())
    return {
        "bars": rows,
        "version": run.version,
        "cursor": cursor,
        "symbol": symbol,
        "interval": interval,
    }


@router.post("/runs/{run_id}/orders")
def order_create(
    run_id: str,
    payload: OrderCreate,
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    def operation(state, data):
        if state["cursor"] >= len(next(iter(data.values()))) - 1:
            raise HTTPException(422, "Replay is complete. Start a new run to place orders.")
        if len(state["orders"]) >= 2000:
            raise HTTPException(422, "Order limit reached. Export and start a new run.")
        stamp = bar_at(data, payload.symbol, state["cursor"])["time"]
        next_stamp = data[payload.symbol][state["cursor"] + 1]["time"]
        # Orders entered after a session's final bar belong to the next session.
        order = {
            **payload.model_dump(mode="json", exclude={"version"}),
            "id": str(payload.id),
            "filled": 0,
            "status": "working",
            "average": "0.00",
            "notional": "0.00",
            "fee_remaining": money(state["config"]["commission"]),
            "triggered": False,
            "time": stamp,
            "day": datetime.fromtimestamp(next_stamp, ZoneInfo("America/New_York"))
            .date()
            .isoformat(),
            "reason": "Accepted. Waiting for the next eligible bar.",
        }
        validate_order(state, data, order)
        state["orders"].append(order)

    limiter.check(f"sim-order:{account}", 120, 60)
    return mutate(db, run_id, account, payload, "order", operation)


@router.post("/runs/{run_id}/advance")
def advance(
    run_id: str, payload: Advance, account: str = Depends(owner), db: Session = Depends(get_session)
):
    limiter.check(f"sim-advance:{account}", 600, 60)
    return mutate(
        db,
        run_id,
        account,
        payload,
        "advance",
        lambda state, data: advance_state(state, data, payload.steps),
    )


@router.post("/runs/{run_id}/orders/{order_id}/cancel")
def cancel(
    run_id: str,
    order_id: str,
    payload: Mutation,
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    def operation(state, data):
        order = next((o for o in state["orders"] if o["id"] == order_id), None)
        if not order:
            raise HTTPException(404, "Order not found.")
        if order["status"] in OPEN:
            order.update(status="canceled", reason="Unfilled remainder canceled by learner.")

    return mutate(db, run_id, account, payload, "cancel:" + order_id, operation)


@router.post("/runs/{run_id}/orders/{order_id}/amend")
def amend(
    run_id: str,
    order_id: str,
    payload: Amendment,
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    def operation(state, data):
        order = next((o for o in state["orders"] if o["id"] == order_id), None)
        if not order or order["status"] not in OPEN:
            raise HTTPException(409, "Only a working order can be amended.")
        for key in ("limit_price", "stop_price"):
            value = getattr(payload, key)
            if value is not None:
                order[key] = str(value)
        validate_order(state, data, order, order_id)
        order["reason"] = "Amendment confirmed. Waiting for the next eligible bar."

    return mutate(db, run_id, account, payload, "amend:" + order_id, operation)


@router.put("/runs/{run_id}/preferences")
def preferences(
    run_id: str,
    payload: Preferences,
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    if len(json.dumps(payload.preferences)) > 200000:
        raise HTTPException(422, "Chart workspace exceeds 200 KB. Remove unused drawings.")
    return mutate(
        db,
        run_id,
        account,
        payload,
        "preferences",
        lambda state, data: state.update(preferences=payload.preferences),
    )


@router.put("/runs/{run_id}/orders/{order_id}/journal")
def journal(
    run_id: str,
    order_id: str,
    payload: Journal,
    account: str = Depends(owner),
    db: Session = Depends(get_session),
):
    def operation(state, data):
        order = next((o for o in state["orders"] if o["id"] == order_id), None)
        if not order:
            raise HTTPException(404, "Order not found.")
        order.update(note=payload.note, lesson=payload.lesson)
        for fill in state["fills"]:
            if fill["order_id"] == order_id:
                fill.update(note=payload.note, lesson=payload.lesson)

    return mutate(db, run_id, account, payload, "journal:" + order_id, operation)
