from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from sqlmodel import select

from quanta.db.models import TradingRun
from quanta.domain.simulator import bar_at, dec, money, reservations
from quanta.services.simulator_market import SYMBOLS, markets


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
