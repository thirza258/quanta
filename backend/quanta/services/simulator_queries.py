from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from sqlmodel import select

from quanta.db.models import TradingRun
from quanta.domain.simulator import account
from quanta.services.simulator_market import markets
from quanta.services.simulator_universe import disclosure, profile, universe


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


def prior_session_close(rows, cursor, bar):
    """Close of the last bar in an earlier session, or the first opening print."""
    if hasattr(rows, "prior_session_close"):
        return rows.prior_session_close(cursor)
    day = datetime.fromtimestamp(bar["time"], ZoneInfo("America/New_York")).date()
    for index in range(cursor - 1, -1, -1):
        row = rows[index]
        if datetime.fromtimestamp(row["time"], ZoneInfo("America/New_York")).date() < day:
            return row["close"]
    return rows[0]["open"]


def snapshot(run, db):
    state = run.state
    data = markets(state, db)
    # Reservations, equity, exposure, buying power and every position's figures
    # come from the engine that keeps the ledger, so the panel and the fills
    # cannot disagree about what the account holds.
    figures = account(state, data)
    tag = universe(state["config"])
    quotes = []
    for symbol, rows in data.items():
        bar = rows[state["cursor"]]
        prior = prior_session_close(rows, state["cursor"], bar)
        quotes.append(
            {
                "symbol": symbol,
                **profile(symbol, tag),
                **bar,
                "change": round(bar["close"] - prior, 2),
                "change_pct": round((bar["close"] / prior - 1) * 100, 2),
            }
        )
    # A short is market risk of the same size as the long it mirrors, so gross
    # adds what is owed rather than subtracting it. "closable" is what a close
    # button should act on, whichever way the position is facing: shares free to
    # sell, or borrowed shares still to buy back after any cover already working.
    held = {row["symbol"]: row for row in figures["positions"]}
    positions = [
        {
            "symbol": symbol,
            **position,
            **{key: value for key, value in held[symbol].items() if key != "symbol"},
        }
        for symbol, position in state["positions"].items()
        if position["quantity"]
    ]
    return {
        "id": run.id,
        "version": run.version,
        "created_at": run.created_at,
        "guest": run.owner.startswith("guest:"),
        "cursor": state["cursor"],
        "total_bars": len(next(iter(data.values()))),
        # A generated market keeps producing sessions as the clock reaches them;
        # an imported replay is bounded by the dataset that was imported.
        "endless": universe(state["config"]) is not None,
        "session": int(state["cursor"] // 390) + 1 if universe(state["config"]) else None,
        "clock": quotes[0]["time"],
        "config": state["config"],
        "cash": state["cash"],
        "reserved": figures["reserved"],
        "available": figures["available"],
        "equity": figures["equity"],
        # What the account is carrying and what it could still buy. On a cash
        # account buying power is simply the cash it has not committed.
        "gross_exposure": figures["gross_exposure"],
        "buying_power": figures["buying_power"],
        "account": state["config"].get("account", "cash"),
        "realized": state["realized"],
        # Why the last jump stopped short, if it did. Older runs have no key.
        "interrupted": state.get("interrupted"),
        "decisions": state.get("decisions", []),
        "quotes": quotes,
        "positions": positions,
        "orders": state["orders"],
        "fills": state["fills"],
        "ledger": state["ledger"],
        "preferences": state.get("preferences", {}),
        "universe": tag,
        "disclosure": disclosure(state["config"]),
    }
