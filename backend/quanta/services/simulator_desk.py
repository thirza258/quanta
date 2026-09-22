"""Desk analytics computed in the API rather than in the browser.

Screening, technical indicators, risk statistics and portfolio performance are
all derived here from the bars the run has already observed. The client renders
what this returns; it does not recompute any of it. Nothing beyond the run's
cursor is read, so no figure can depend on a price the learner has not seen.
"""

import math

import numpy as np

from quanta.domain.simulator import dec
from quanta.services.simulator_news import sentiment
from quanta.services.simulator_queries import prior_session_close
from quanta.services.simulator_universe import profile

SESSION = 390


def session_bars(state):
    """Observations in one trading session for this run's base interval."""
    return 1 if state["config"].get("base_interval") == "1D" else SESSION


def windows(state):
    """Short and long statistical windows, in this run's own observations.

    A minute market measures over a session and a week. A daily replay has one
    observation per session, so the same statistics are measured over a month and
    a quarter instead; the bar counts travel with the response.
    """
    bars = session_bars(state)
    return bars, max(bars, 20), max(bars * 5, 60)


def _closes(rows, cursor):
    if hasattr(rows, "close"):
        return np.asarray(rows.close[: cursor + 1], dtype=float)
    return np.array([row["close"] for row in rows[: cursor + 1]], dtype=float)


def _column(rows, cursor, key):
    if hasattr(rows, key):
        return np.asarray(getattr(rows, key)[: cursor + 1], dtype=float)
    return np.array([row[key] for row in rows[: cursor + 1]], dtype=float)


def _prior_close(rows, cursor):
    """The same reference the account snapshot uses, so both panels agree."""
    return prior_session_close(rows, cursor, rows[cursor])


def sma_series(values, period):
    """Rolling mean, with no value until the window is full."""
    out, total = [], 0.0
    for index, value in enumerate(values):
        total += float(value)
        if index >= period:
            total -= float(values[index - period])
        out.append(total / period if index >= period - 1 else None)
    return out


def ema_series(values, period):
    """Seeded with the first full simple average, then exponentially smoothed."""
    out, total, previous = [], 0.0, None
    alpha = 2 / (period + 1)
    for index, value in enumerate(values):
        total += float(value)
        if index < period - 1:
            out.append(None)
            continue
        previous = (
            total / period if previous is None else alpha * float(value) + (1 - alpha) * previous
        )
        out.append(previous)
    return out


def rsi_series(values, period=14):
    """Wilder smoothing, matching the definition the courses teach."""
    out, gain, loss = [], 0.0, 0.0
    for index, value in enumerate(values):
        if index == 0:
            out.append(None)
            continue
        change = float(value) - float(values[index - 1])
        if index <= period:
            gain += max(change, 0.0) / period
            loss += max(-change, 0.0) / period
        else:
            gain = (gain * (period - 1) + max(change, 0.0)) / period
            loss = (loss * (period - 1) + max(-change, 0.0)) / period
        if index < period:
            out.append(None)
        elif loss == 0:
            out.append(100.0 if gain else 50.0)
        else:
            out.append(100 - 100 / (1 + gain / loss))
    return out


def macd_series(values, fast=12, slow=26, signal=9):
    quick, slack = ema_series(values, fast), ema_series(values, slow)
    line = [None if a is None or b is None else a - b for a, b in zip(quick, slack, strict=True)]
    present = [value for value in line if value is not None]
    offset = len(line) - len(present)
    smoothed = [None] * offset + ema_series(present, signal)
    return {
        "line": line,
        "signal": smoothed,
        "histogram": [
            None if a is None or b is None else a - b for a, b in zip(line, smoothed, strict=True)
        ],
    }


def _last(series):
    for value in reversed(series):
        if value is not None:
            return value
    return None


def sma(values, period):
    return _last(sma_series(values, period)) if len(values) >= period else None


def ema(values, period):
    return _last(ema_series(values, period)) if len(values) >= period else None


def rsi(values, period=14):
    return _last(rsi_series(values, period)) if len(values) > period else None


def macd(values, fast=12, slow=26, signal=9):
    if len(values) < slow + signal:
        return None
    computed = macd_series(values, fast, slow, signal)
    if _last(computed["signal"]) is None:
        return None
    return {key: _last(series) for key, series in computed.items()}


SPEC_LIMITS = (2, 200)


def indicator_series(closes, spec: str):
    """Compute the requested overlays from the bars the client can already see."""
    parts = spec.split(":")
    kind = parts[0].upper()
    numbers = []
    for raw in parts[1:4]:
        try:
            numbers.append(max(SPEC_LIMITS[0], min(SPEC_LIMITS[1], int(raw))))
        except ValueError:
            return None
    if kind in ("SMA", "EMA", "RSI") and len(numbers) >= 1:
        period = numbers[0]
        values = {"SMA": sma_series, "EMA": ema_series, "RSI": rsi_series}[kind](closes, period)
        return {"kind": kind, "values": values}
    if kind == "MACD" and len(numbers) == 3:
        return {"kind": kind, **macd_series(closes, *numbers)}
    return None


def _annualized(values, window, bars):
    sample = values[-(window + 1) :]
    if len(sample) < 3:
        return None
    returns = np.diff(np.log(sample))
    return float(returns.std(ddof=1) * math.sqrt(252 * bars))


def quotes_table(state, data, room):
    """One row per listed company, with the statistics a screener sorts on."""
    cursor = state["cursor"]
    tag = state["config"].get("universe")
    bars, short, _ = windows(state)
    rows = []
    for symbol, series in data.items():
        closes = _closes(series, cursor)
        volumes = _column(series, cursor, "volume")
        prior = _prior_close(series, cursor)
        last = float(closes[-1])
        average_volume = float(volumes[-min(len(volumes), 20) :].mean())
        window = closes[-min(len(closes), short) :]
        rows.append(
            {
                "symbol": symbol,
                **profile(symbol, tag),
                "close": last,
                "change": round(last - prior, 2),
                "change_pct": round((last / prior - 1) * 100, 2) if prior else 0.0,
                "volume": int(volumes[-1]),
                "relative_volume": round(float(volumes[-1]) / average_volume, 2)
                if average_volume
                else None,
                "notional": round(last * float(volumes[-min(len(volumes), short) :].sum())),
                "window_bars": short,
                "window_high": float(window.max()),
                "window_low": float(window.min()),
                "volatility": _annualized(closes, short, bars),
                # Company and sector tone only: a shared macro print would push
                # every ticker the same way and flatten the ranking.
                "sentiment": (
                    sentiment(
                        room,
                        cursor,
                        SESSION,
                        symbol,
                        profile(symbol, tag)["sector"],
                        macro=False,
                    )["score"]
                    if room
                    else None
                ),
            }
        )
    return rows


def movers(state, data, room, limit=6):
    """Gainers, losers, turnover leaders, sector performance and breadth."""
    rows = quotes_table(state, data, room)
    ranked = sorted(rows, key=lambda r: r["change_pct"], reverse=True)
    gainers = [row for row in ranked if row["change_pct"] > 0][:limit]
    losers = [row for row in reversed(ranked) if row["change_pct"] < 0][:limit]
    sectors = {}
    for row in rows:
        name = row["sector"] or "Unclassified"
        bucket = sectors.setdefault(name, {"sector": name, "moves": [], "tone": []})
        bucket["moves"].append(row["change_pct"])
        if row["sentiment"] is not None:
            bucket["tone"].append(row["sentiment"])
    return {
        "gainers": gainers,
        "losers": losers,
        "active": sorted(rows, key=lambda r: -r["notional"])[:limit],
        "sectors": sorted(
            (
                {
                    "sector": bucket["sector"],
                    "companies": len(bucket["moves"]),
                    "change_pct": round(float(np.mean(bucket["moves"])), 2),
                    "sentiment": round(float(np.mean(bucket["tone"])), 3)
                    if bucket["tone"]
                    else None,
                }
                for bucket in sectors.values()
            ),
            key=lambda s: -s["change_pct"],
        ),
        "breadth": {
            "advancing": sum(1 for r in rows if r["change_pct"] > 0),
            "declining": sum(1 for r in rows if r["change_pct"] < 0),
            "unchanged": sum(1 for r in rows if r["change_pct"] == 0),
            "average_change_pct": round(float(np.mean([r["change_pct"] for r in rows])), 2),
        },
    }


def technicals(state, data, room, symbol):
    """Indicators, risk statistics and market sensitivity for one company."""
    cursor = state["cursor"]
    bars, short, long_ = windows(state)
    series = data[symbol]
    closes = _closes(series, cursor)
    volumes = _column(series, cursor, "volume")
    returns = np.diff(np.log(closes))
    span = min(len(returns), long_)
    beta = correlation = None
    # An imported replay holds one instrument, so there is no market to measure
    # against; reporting a beta of exactly 1.0 there would be meaningless.
    if len(data) > 1 and span > 10:
        market = np.mean([_closes(rows, cursor) for rows in data.values()], axis=0)
        market_returns = np.diff(np.log(market))
        own, index = returns[-span:], market_returns[-span:]
        variance = float(index.var())
        if variance > 1e-18:
            beta = round(float(np.cov(own, index)[0][1] / variance), 3)
        spread = float(own.std() * index.std())
        if spread > 1e-18:
            correlation = round(float(np.corrcoef(own, index)[0][1]), 3)

    def move(back):
        """Percentage change over the last `back` observations."""
        if len(closes) <= back:
            return None
        return round(float(closes[-1] / closes[-1 - back] - 1) * 100, 2)

    macd_value = macd(closes)
    tag = state["config"].get("universe")
    return {
        "symbol": symbol,
        **profile(symbol, tag),
        "close": float(closes[-1]),
        "indicators": {
            "sma_20": sma(closes, 20),
            "sma_50": sma(closes, 50),
            "ema_20": ema(closes, 20),
            "rsi_14": rsi(closes),
            "macd": macd_value,
        },
        "risk": {
            "volatility_short": _annualized(closes, short, bars),
            "volatility_long": _annualized(closes, long_, bars),
            "short_window_bars": short,
            "long_window_bars": long_,
            "beta": beta,
            "correlation": correlation,
            "observations": len(returns),
        },
        "momentum": {
            "session": move(bars),
            "week": move(bars * 5),
            "since_open": round(float(closes[-1] / closes[0] - 1) * 100, 2),
        },
        "range": {
            "high_20": float(closes[-min(len(closes), 20) :].max()),
            "low_20": float(closes[-min(len(closes), 20) :].min()),
            "high_window": float(closes[-min(len(closes), short) :].max()),
            "low_window": float(closes[-min(len(closes), short) :].min()),
            "high_run": float(closes.max()),
            "low_run": float(closes.min()),
        },
        "liquidity": {
            "volume": int(volumes[-1]),
            "average_volume_20": round(float(volumes[-min(len(volumes), 20) :].mean())),
            "average_volume_window": round(float(volumes[-min(len(volumes), short) :].mean())),
        },
        "sentiment": (
            {
                "session": sentiment(room, cursor, SESSION, symbol, profile(symbol, tag)["sector"]),
                "week": sentiment(
                    room, cursor, SESSION * 5, symbol, profile(symbol, tag)["sector"]
                ),
            }
            if room
            else None
        ),
    }


def _times(series, cursor):
    if hasattr(series, "time"):
        return np.asarray(series.time[: cursor + 1], dtype=np.int64)
    return np.array([row["time"] for row in series[: cursor + 1]], dtype=np.int64)


def performance(state, data, points=180):
    """Mark the account to market on every observed bar and summarize the path."""
    cursor = state["cursor"]
    first = next(iter(data.values()))
    times = _times(first, cursor)
    opening = float(state["ledger"][0]["cash"]) if state["ledger"] else 100000.0

    cash = np.full(len(times), opening)
    for entry in state["ledger"]:
        if entry["time"] is None:
            continue
        start = int(np.searchsorted(times, entry["time"]))
        if start < len(cash):
            cash[start:] = float(entry["cash"])

    holdings = np.zeros(len(times))
    attribution = {}
    marks = {}
    for fill in state["fills"]:
        symbol = fill["symbol"]
        if symbol not in data:
            continue
        if symbol not in marks:
            marks[symbol] = _closes(data[symbol], cursor)
        start = int(np.searchsorted(times, fill["time"]))
        if start >= len(times):
            continue
        quantity = fill["quantity"] * (1 if fill["side"] == "buy" else -1)
        holdings += quantity * np.concatenate((np.zeros(start), marks[symbol][start:]))
        book = attribution.setdefault(
            symbol, {"symbol": symbol, "realized": 0.0, "fills": 0, "quantity": 0}
        )
        book["realized"] += float(fill["realized"])
        book["fills"] += 1
        book["quantity"] += quantity

    equity = cash + holdings
    peak = np.maximum.accumulate(equity)
    drawdown = equity / peak - 1
    step = max(1, len(equity) // points)
    for symbol, book in attribution.items():
        mark = float(marks[symbol][-1])
        position = state["positions"].get(symbol, {})
        book["unrealized"] = round(
            mark * position.get("quantity", 0) - float(position.get("cost", 0)), 2
        )
        book["realized"] = round(book["realized"], 2)
        book["total"] = round(book["realized"] + book["unrealized"], 2)
        book["quantity"] = position.get("quantity", 0)

    round_trips = [float(f["realized"]) for f in state["fills"] if f["side"] == "sell"]
    wins = [value for value in round_trips if value > 0]
    losses = [value for value in round_trips if value < 0]
    exposure = float(np.mean(holdings / np.where(equity == 0, 1, equity))) if len(equity) else 0.0
    return {
        "curve": [
            {"time": int(times[index]), "equity": round(float(equity[index]), 2)}
            for index in range(0, len(equity), step)
        ]
        + (
            [{"time": int(times[-1]), "equity": round(float(equity[-1]), 2)}] if len(equity) else []
        ),
        "opening_equity": round(opening, 2),
        "equity": round(float(equity[-1]), 2) if len(equity) else opening,
        "total_return": round(float(equity[-1] / opening - 1), 6) if len(equity) else 0.0,
        "max_drawdown": round(float(drawdown.min()), 6) if len(drawdown) else 0.0,
        "realized": str(dec(state["realized"])),
        "unrealized": round(sum(book["unrealized"] for book in attribution.values()), 2),
        "average_exposure": round(exposure, 4),
        "trades": len(round_trips),
        "win_rate": round(len(wins) / len(round_trips), 4) if round_trips else None,
        "profit_factor": round(sum(wins) / -sum(losses), 3) if losses else None,
        "average_win": round(float(np.mean(wins)), 2) if wins else None,
        "average_loss": round(float(np.mean(losses)), 2) if losses else None,
        "attribution": sorted(attribution.values(), key=lambda b: -abs(b["total"])),
        "bars_observed": len(equity),
    }


def calendar(state, data, room, ahead=None):
    """Scheduled releases either side of the cursor.

    A calendar names what is coming and when. For anything still ahead of the
    run's clock that is all it carries: the release's name and its date, plus the
    published consensus for a company's results. The outcome is attached only
    once the cursor has reached the bar that prints it.
    """
    cursor = state["cursor"]
    series = next(iter(data.values()))
    times, horizon = series.time, len(series) - 1
    limit = horizon if ahead is None else min(horizon, cursor + ahead)

    economic = []
    for event in room.events:
        if event["category"] != "macro" or event["index"] > limit:
            continue
        released = event["index"] <= cursor
        economic.append(
            {
                "index": event["index"],
                "time": int(times[event["index"]]),
                "name": event["scheduled"],
                "topic": event["topic"],
                "released": released,
                # Before the print a calendar carries the appointment, not the number.
                "headline": event["headline"] if released else None,
                "sentiment": event["sentiment"] if released else None,
            }
        )

    earnings = []
    tag = state["config"].get("universe")
    for symbol, book in room.books.items():
        quarter = book[-1]
        if quarter["index"] < 0 or quarter["index"] > limit:
            continue
        released = quarter["index"] <= cursor
        entry = {
            "symbol": symbol,
            **profile(symbol, tag),
            "label": quarter["label"],
            "index": quarter["index"],
            "time": int(times[quarter["index"]]),
            "bars_away": quarter["index"] - cursor,
            "released": released,
            "consensus_eps": quarter["consensus_eps"],
            "consensus_revenue": quarter["consensus_revenue"],
        }
        if released:
            entry.update(
                eps=quarter["eps"],
                revenue=quarter["revenue"],
                eps_surprise=quarter["eps_surprise"],
                revenue_surprise=quarter["revenue_surprise"],
            )
        earnings.append(entry)

    economic.sort(key=lambda item: item["index"])
    earnings.sort(key=lambda item: (item["index"], item["symbol"]))
    return {"economic": economic, "earnings": earnings, "horizon_bars": limit - cursor}


def peers(state, data, room, symbol, valuation):
    """Comparable companies in the same sector, on the quarters each has reported."""
    tag = state["config"].get("universe")
    sector = profile(symbol, tag)["sector"]
    cursor = state["cursor"]
    rows = []
    for other, book in room.books.items():
        if other not in data or profile(other, tag)["sector"] != sector:
            continue
        reported = [q for q in book if q["index"] < 0 or q["index"] <= cursor]
        if not reported:
            continue
        mark = _closes(data[other], cursor)[-1]
        numbers = valuation(other, reported, float(mark))
        rows.append(
            {
                "symbol": other,
                **profile(other, tag),
                "price": float(mark),
                "market_capitalization": numbers["market_capitalization"],
                "price_earnings": numbers["price_earnings"],
                "price_sales": numbers["price_sales"],
                "price_book": numbers["price_book"],
                "enterprise_ebitda": numbers["enterprise_ebitda"],
                "operating_margin": numbers["operating_margin"],
                "return_on_equity": numbers["return_on_equity"],
                "revenue_growth": numbers["revenue_growth"],
                "debt_equity": numbers["debt_equity"],
                "free_cash_flow_yield": numbers["free_cash_flow_yield"],
                "reported_quarters": len(reported),
                "self": other == symbol,
            }
        )
    rows.sort(key=lambda row: -row["market_capitalization"])

    def median(key):
        """Sector median, skipping companies for which the ratio is undefined."""
        ordered = sorted(row[key] for row in rows if row[key] is not None)
        if not ordered:
            return None
        middle = len(ordered) // 2
        return ordered[middle] if len(ordered) % 2 else (ordered[middle - 1] + ordered[middle]) / 2

    return {
        "sector": sector,
        "rows": rows,
        "median": {
            key: median(key)
            for key in (
                "price_earnings",
                "price_sales",
                "price_book",
                "enterprise_ebitda",
                "operating_margin",
                "return_on_equity",
                "revenue_growth",
            )
        },
    }
