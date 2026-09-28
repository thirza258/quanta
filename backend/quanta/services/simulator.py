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
from quanta.services import simulator_desk as desk
from quanta.services.simulator_fundamentals import quarter_label, structure, valuation
from quanta.services.simulator_market import (
    SESSION_BARS,
    markets,
    newsroom,
    session_open,
)
from quanta.services.simulator_missions import MISSIONS
from quanta.services.simulator_missions import listing as mission_listing
from quanta.services.simulator_missions import progress as mission_progress
from quanta.services.simulator_news import QUARTER_SESSIONS, released, report_session, sentiment
from quanta.services.simulator_queries import latest, run_for, snapshot
from quanta.services.simulator_universe import (
    BY_SYMBOL,
    DEFAULT_WATCHLIST,
    DISCLOSURE,
    UNIVERSE_ID,
    disclosure,
    listing,
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
        "symbols": listing(UNIVERSE_ID),
        "watchlist": DEFAULT_WATCHLIST,
        "disclosure": DISCLOSURE,
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
    mission = None
    if config.get("mission"):
        mission = MISSIONS.get(config["mission"])
        if not mission:
            raise HTTPException(404, "That practice mission does not exist.")
        if payload.mode != "synthetic":
            raise HTTPException(422, "Practice missions run on the generated market.")
        # Everyone attempting a mission meets the same market and starts together.
        config["seed"] = mission.seed
    if config["seed"] is None:
        # No seed asked for: derive one from the run identifier so each new paper
        # account gets a different market, while an idempotent retry of the same
        # request still reproduces the same run rather than rolling a new one.
        config["seed"] = int(hashlib.sha256(str(payload.id).encode()).hexdigest(), 16) % 1000001
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
            universe=UNIVERSE_ID,
            source=(
                "Simulated market · fictional companies and headlines · prices generated "
                "from the run's simulated news, weekday-only calendar"
            ),
        )
        cursor = mission.cursor if mission else 499
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


# Raw observations behind one bar of each coarser interval.
BUCKET_BARS = {"5m": 5, "15m": 15, "1h": 60, "1D": SESSION_BARS}
# Extra bars read before the window so exponential overlays converge to the same
# values they would reach from the start of the run.
OVERLAY_WARMUP = 400
# A ceiling on observations read for one chart, so a very long run stays bounded.
MAX_OBSERVATIONS = 120_000


def market(
    run_id: str,
    symbol: str,
    interval: Literal["1m", "5m", "15m", "1h", "1D"],
    cursor: int | None,
    indicators: str | None,
    limit: int,
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
    # A generated run has no end, so a chart asks for a window rather than the
    # whole history. Read enough observations to fill it, plus a warm-up margin so
    # the smoothed overlays match the values full history would have produced.
    daily = state["config"]["base_interval"] == "1D"
    per_bucket = 1 if daily or interval == "1m" else BUCKET_BARS[interval]
    span = min(cursor + 1, (limit + OVERLAY_WARMUP) * per_bucket, MAX_OBSERVATIONS)
    start = cursor + 1 - span
    series = data[symbol]
    coarser = interval != "1m" and not daily
    if coarser and hasattr(series, "aggregate"):
        # Generated bars are columnar, so buckets are reduced without turning
        # every observation behind them into a dictionary first.
        rows = series.aggregate(start, cursor + 1, per_bucket)
    elif coarser:
        rows = series[start : cursor + 1]
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
    else:
        rows = series[start : cursor + 1]
    # Overlays are computed here, from the same observed bars that are returned,
    # so the client never recomputes them and no future price can reach them. They
    # are calculated across the warm-up margin and then trimmed with the bars.
    closes = [bar["close"] for bar in rows]
    computed = {}
    for spec in (indicators or "").split(",")[:8]:
        spec = spec.strip()
        if not spec or spec in computed:
            continue
        series = desk.indicator_series(closes, spec)
        if series:
            computed[spec] = series
    if len(rows) > limit:
        rows = rows[-limit:]
        for series in computed.values():
            for key, values in series.items():
                if isinstance(values, list):
                    series[key] = values[-limit:]
    return {
        "bars": rows,
        "version": run.version,
        "cursor": cursor,
        "symbol": symbol,
        "interval": interval,
        "indicators": computed,
        # The oldest observation in this window, so a client can tell whether more
        # history exists behind it.
        "from_bar": max(0, cursor + 1 - len(rows) * per_bucket),
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


def news(run_id: str, symbol: str | None, limit: int, account: str, db: Session):
    """Simulated headlines already released by the run's clock, newest first."""
    run = run_for(db, run_id, account)
    state = run.state
    config = state["config"]
    if config["mode"] != "synthetic" or config.get("universe") != UNIVERSE_ID:
        return {
            "items": [],
            "available": False,
            "cursor": state["cursor"],
            "version": run.version,
            "disclosure": disclosure(config),
            "sentiment": None,
            "notice": (
                "This run replays imported historical prices. No headlines are generated "
                "for it, because invented news must never be attached to real market data."
                if config["mode"] == "historical"
                else "This run predates the simulator's newsroom. Start a new run to trade "
                "a market whose prices respond to generated headlines."
            ),
        }
    data = markets(state, db)
    if symbol and symbol not in data:
        raise HTTPException(404, "This stock is unavailable in this run.")
    room = newsroom(config["seed"], state["cursor"])
    cursor = state["cursor"]
    times = next(iter(data.values())).time
    items = released(
        room,
        cursor,
        symbol=symbol,
        sector=BY_SYMBOL[symbol].sector if symbol in BY_SYMBOL else None,
        limit=limit,
    )
    sector = BY_SYMBOL[symbol].sector if symbol in BY_SYMBOL else None
    return {
        "items": [{**item, "time": int(times[item["index"]])} for item in items],
        "available": True,
        "cursor": cursor,
        "version": run.version,
        "disclosure": disclosure(config),
        "notice": "",
        # Sentiment over the last modeled session and the last modeled week.
        "sentiment": {
            "session": sentiment(room, cursor, SESSION_BARS, symbol, sector),
            "week": sentiment(room, cursor, SESSION_BARS * 5, symbol, sector),
            "market": sentiment(room, cursor, SESSION_BARS),
        },
    }


def fundamentals(run_id: str, symbol: str, account: str, db: Session):
    """Generated statements a company has already reported by the run's clock."""
    run = run_for(db, run_id, account)
    state = run.state
    config = state["config"]
    if config["mode"] != "synthetic" or config.get("universe") != UNIVERSE_ID:
        raise HTTPException(
            422,
            "This run replays imported historical prices. Financial statements are only "
            "generated for the simulator's fictional companies."
            if config["mode"] == "historical"
            else "This run predates the simulator's fictional companies, so it has no "
            "generated statements. Start a new run to read them.",
        )
    data = markets(state, db)
    if symbol not in data or symbol not in BY_SYMBOL:
        raise HTTPException(404, "This stock is unavailable in this run.")
    company = BY_SYMBOL[symbol]
    room = newsroom(config["seed"], state["cursor"])
    cursor = state["cursor"]
    series = data[symbol]
    book = room.books[symbol]
    released_quarters = [q for q in book if q["index"] < 0 or q["index"] <= cursor]
    times = series.time
    return {
        "symbol": symbol,
        "name": company.name,
        "sector": company.sector,
        "business": company.business,
        # Descriptive facts only. The margin, growth and leverage assumptions that
        # generate a quarter stay on the server: published, they would let an
        # unreleased result be solved for from its consensus.
        "structure": {
            key: structure(company)[key]
            for key in ("shares", "employees", "fiscal_year_end", "development_stage")
        },
        "currency": "USD",
        "units": "millions of USD except per-share amounts",
        "quarters": released_quarters,
        # Only the expectation is published ahead of a print, never the result.
        # The date is knowable from the calendar alone, so it is given even when
        # the quarter itself is further out than the market has been generated;
        # the street's estimate appears once that quarter has been scheduled.
        "upcoming": _upcoming(config["seed"], symbol, book, cursor, times),
        "valuation": valuation(company, released_quarters, series[cursor]["close"]),
        "peers": desk.peers(state, data, room, symbol, _peer_valuation),
        "cursor": cursor,
        "version": run.version,
        "disclosure": disclosure(config),
    }


def _room(state):
    """The run's newsroom, or None when the run replays imported prices."""
    config = state["config"]
    if config["mode"] != "synthetic" or config.get("universe") != UNIVERSE_ID:
        return None
    return newsroom(config["seed"], state["cursor"])


def desk_view(run_id: str, account: str, db: Session):
    """Screener, sector performance and portfolio analytics, computed server-side."""
    run = run_for(db, run_id, account)
    state = run.state
    data = markets(state, db)
    return {
        "movers": desk.movers(state, data, _room(state)),
        "performance": desk.performance(state, data),
        "cursor": state["cursor"],
        "version": run.version,
        "disclosure": disclosure(state["config"]),
    }


def analytics(run_id: str, symbol: str, account: str, db: Session):
    """Indicators, risk statistics and news tone for one company."""
    run = run_for(db, run_id, account)
    state = run.state
    data = markets(state, db)
    if symbol not in data:
        raise HTTPException(404, "This stock is unavailable in this run.")
    return {
        **desk.technicals(state, data, _room(state), symbol),
        "cursor": state["cursor"],
        "version": run.version,
        "disclosure": disclosure(state["config"]),
    }


def _peer_valuation(symbol, quarters, price):
    """Valuation for a comparable company, on the quarters it has reported."""
    return valuation(BY_SYMBOL[symbol], quarters, price)


def calendar(run_id: str, ahead: int | None, account: str, db: Session):
    """Scheduled economic releases and company results either side of the cursor."""
    run = run_for(db, run_id, account)
    state = run.state
    room = _room(state)
    if not room:
        raise HTTPException(
            422,
            "This run has no reporting calendar. Only the simulator's generated market "
            "schedules economic releases and company results.",
        )
    return {
        **desk.calendar(state, markets(state, db), room, ahead),
        "cursor": state["cursor"],
        "version": run.version,
        "disclosure": disclosure(state["config"]),
    }


def _upcoming(seed, symbol, book, cursor, times):
    """The next scheduled report: its date always, its consensus when published."""
    pending = next((q for q in book if q["index"] > cursor), None)
    if pending:
        return {
            "label": pending["label"],
            "time": int(times[pending["index"]]),
            "bars_away": pending["index"] - cursor,
            "consensus_eps": pending["consensus_eps"],
            "consensus_revenue": pending["consensus_revenue"],
        }
    # Nothing scheduled yet in the generated horizon. The cycle still fixes the
    # date, so publish it and leave the estimate open until the street sets it.
    first = report_session(seed, symbol)
    current = int(cursor) // SESSION_BARS
    elapsed = max(0, current - first)
    session = first + (elapsed // QUARTER_SESSIONS + 1) * QUARTER_SESSIONS
    index = session * SESSION_BARS
    return {
        "label": quarter_label(len(book)),
        "time": int(session_open(session).timestamp()),
        "bars_away": index - int(cursor),
        "consensus_eps": None,
        "consensus_revenue": None,
    }


def missions():
    """The practice catalog, for lesson pages and the mission picker."""
    return {"missions": mission_listing(), "disclosure": DISCLOSURE}


def mission(run_id: str, account: str, db: Session):
    """The run's mission and how far each of its objectives has been met."""
    run = run_for(db, run_id, account)
    state = run.state
    chosen = MISSIONS.get(state["config"].get("mission") or "")
    if not chosen:
        raise HTTPException(404, "This run was not started from a practice mission.")
    data = markets(state, db)
    room = _room(state)
    times = next(iter(data.values())).time
    objectives = mission_progress(chosen, state, room, times)
    return {
        "id": chosen.id,
        "title": chosen.title,
        "subtitle": chosen.subtitle,
        "brief": chosen.brief,
        "lessons": list(chosen.lessons),
        "symbol": chosen.symbol,
        "objectives": objectives,
        "met": sum(1 for o in objectives if o["met"]),
        "total": len(objectives),
        "complete": all(o["met"] for o in objectives),
        "cursor": state["cursor"],
        "version": run.version,
        "disclosure": DISCLOSURE,
    }
