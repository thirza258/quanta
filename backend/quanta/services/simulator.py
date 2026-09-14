import copy
import hashlib
import json
from datetime import datetime
from typing import Literal
from uuid import uuid4
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from quanta.db.models import TradingDataset, TradingRun
from quanta.domain.simulator import (
    OPEN,
    advance_state,
    bar_at,
    money,
    validate_order,
)
from quanta.domain.simulator_models import (
    Advance,
    Amendment,
    Journal,
    Mutation,
    OrderCreate,
    Preferences,
    RunCreate,
)
from quanta.services import data_store
from quanta.services.simulator_market import SYMBOLS, markets
from quanta.services.simulator_queries import latest, run_for, snapshot


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


def bootstrap(account: str, db: Session):
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


def create_run(payload: RunCreate, account: str, db: Session):
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


def get_run(run_id: str, account: str, db: Session):
    return snapshot(run_for(db, run_id, account), db)


def market(
    run_id: str,
    symbol: str,
    interval: Literal["1m", "5m", "15m", "1h", "1D"],
    cursor: int | None,
    account: str,
    db: Session,
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


def order_create(run_id: str, payload: OrderCreate, account: str, db: Session):
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

    return mutate(db, run_id, account, payload, "order", operation)


def advance(run_id: str, payload: Advance, account: str, db: Session):
    return mutate(
        db,
        run_id,
        account,
        payload,
        "advance",
        lambda state, data: advance_state(state, data, payload.steps),
    )


def cancel(run_id: str, order_id: str, payload: Mutation, account: str, db: Session):
    def operation(state, data):
        order = next((o for o in state["orders"] if o["id"] == order_id), None)
        if not order:
            raise HTTPException(404, "Order not found.")
        if order["status"] in OPEN:
            order.update(status="canceled", reason="Unfilled remainder canceled by learner.")

    return mutate(db, run_id, account, payload, "cancel:" + order_id, operation)


def amend(run_id: str, order_id: str, payload: Amendment, account: str, db: Session):
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


def preferences(run_id: str, payload: Preferences, account: str, db: Session):
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


def journal(run_id: str, order_id: str, payload: Journal, account: str, db: Session):
    def operation(state, data):
        order = next((o for o in state["orders"] if o["id"] == order_id), None)
        if not order:
            raise HTTPException(404, "Order not found.")
        order.update(note=payload.note, lesson=payload.lesson)
        for fill in state["fills"]:
            if fill["order_id"] == order_id:
                fill.update(note=payload.note, lesson=payload.lesson)

    return mutate(db, run_id, account, payload, "journal:" + order_id, operation)
