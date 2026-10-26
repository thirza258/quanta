"""Desk analytics computed in the API rather than in the browser.

Screening, technical indicators, risk statistics and portfolio performance are
all derived here from the bars the run has already observed. The client renders
what this returns; it does not recompute any of it. Nothing beyond the run's
cursor is read, so no figure can depend on a price the learner has not seen.
"""

import math

import numpy as np

from quanta import engine
from quanta.domain.analytics import summarize
from quanta.domain.simulator import dec
from quanta.services.simulator_fundamentals import quarter_label
from quanta.services.simulator_missions import MISSIONS
from quanta.services.simulator_news import report_slot, sentiment
from quanta.services.simulator_queries import prior_session_close
from quanta.services.simulator_universe import UNIVERSE_ID, profile

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


def _listed(values):
    """An engine series as the API returns it: warm-up positions are None."""
    return [None if math.isnan(value) else value for value in values.tolist()]


def sma_series(values, period):
    """Rolling mean, with no value until the window is full."""
    return _listed(engine.sma(values, period))


def ema_series(values, period):
    """Seeded with the first full simple average, then exponentially smoothed."""
    return _listed(engine.ema(values, period))


def rsi_series(values, period=14):
    """Wilder smoothing, matching the definition the courses teach."""
    return _listed(engine.rsi(values, period))


def macd_series(values, fast=12, slow=26, signal=9):
    line, smoothed, histogram = engine.macd(values, fast, slow, signal)
    return {"line": _listed(line), "signal": _listed(smoothed), "histogram": _listed(histogram)}


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


def start_cursor(state, data):
    """The bar the account opened on, so performance is measured from arrival."""
    config = state["config"]
    if "start_cursor" in config:
        return int(config["start_cursor"])
    # Runs created before the start cursor was recorded used fixed defaults.
    if config["mode"] == "historical":
        return min(30, len(next(iter(data.values()))) - 2)
    mission = MISSIONS.get(config.get("mission") or "")
    return mission.cursor if mission else 499


def benchmark_name(state):
    """Generated runs are measured against the generated index, by its own name.

    An imported replay gets a descriptive label instead: an equal-weighted
    average of imported closes is not the QX-200, and calling it that would
    dress real prices in a fictional index's name.
    """
    config = state["config"]
    if config["mode"] == "historical":
        return "Equal-weighted imported average"
    return "QX-200" if config.get("universe") == UNIVERSE_ID else "Equal-weighted run average"


def _session_ends(series, cursor, start=0):
    """Offsets of each session's last observation, within the window from `start`.

    Annualized statistics need one observation per session, not per minute; 390
    intraday returns a day would inflate any figure scaled by 252.
    """
    if not hasattr(series, "session"):
        # An imported daily replay already has one observation per session.
        return np.arange(cursor + 1 - start)
    sessions = np.asarray(series.session[start : cursor + 1])
    if len(sessions) < 2:
        return np.array([len(sessions) - 1]) if len(sessions) else np.array([], dtype=int)
    changes = np.flatnonzero(np.diff(sessions))
    return np.append(changes, len(sessions) - 1)


def _window(series, start, cursor):
    """Closes over [start, cursor], as _closes(series, cursor)[start:] reads them."""
    if hasattr(series, "cents"):
        return series.cents[3][start : cursor + 1] / 100.0
    return _closes(series, cursor)[start:]


def _times(series, cursor):
    if hasattr(series, "time"):
        return np.asarray(series.time[: cursor + 1], dtype=np.int64)
    return np.array([row["time"] for row in series[: cursor + 1]], dtype=np.int64)


def marked(state, data, start, cursor):
    """The account and the market valued on every bar of [start, cursor].

    The mark-to-market runs in the engine: the cash balance in force on each bar,
    every fill's position valued at that bar's close in fill order, and gross
    exposure. It also returns the equal-weighted level of every listed company,
    rebased to `start`, the bar the account opened on. That is the QX-200 the
    newsroom refers to: an index a learner can be measured against, so a result
    separates into the market's move and their own. The market's drift before
    anyone was trading is neither alpha nor beta; it simply was not theirs.
    """
    first = next(iter(data.values()))
    times = _times(first, cursor)[start:]
    opening = float(state["ledger"][0]["cash"]) if state["ledger"] else 100000.0
    cash_events = [entry for entry in state["ledger"] if entry["time"] is not None]
    fills = [fill for fill in state["fills"] if fill["symbol"] in data]
    columns = {symbol: position for position, symbol in enumerate(data)}
    closes = [_window(series, start, cursor) for series in data.values()]
    equity, gross, level = engine.mark_to_market(
        times,
        opening,
        [entry["time"] for entry in cash_events],
        [float(entry["cash"]) for entry in cash_events],
        [columns[fill["symbol"]] for fill in fills],
        [fill["quantity"] * (1 if fill["side"] == "buy" else -1) for fill in fills],
        [fill["time"] for fill in fills],
        closes,
    )
    return times, opening, equity, gross, level, closes, columns, fills


def performance(state, data, points=180):
    """Mark the account to market on every observed bar and summarize the path."""
    cursor = state["cursor"]
    first = next(iter(data.values()))
    # Only the bars since the account opened. The market's move before anyone was
    # trading is not the learner's result, and averaging exposure over bars where
    # nothing could be held would understate every position they did take.
    start = min(start_cursor(state, data), cursor)
    times, opening, equity, gross, level, closes, columns, fills = marked(
        state, data, start, cursor
    )

    attribution = {}
    landed = np.searchsorted(times, np.array([fill["time"] for fill in fills], dtype=np.int64))
    for fill, at in zip(fills, landed.tolist(), strict=True):
        if at >= len(times):
            continue
        book = attribution.setdefault(
            fill["symbol"], {"symbol": fill["symbol"], "realized": 0.0, "fills": 0, "quantity": 0}
        )
        book["realized"] += float(fill["realized"])
        book["fills"] += 1
        book["quantity"] += fill["quantity"] * (1 if fill["side"] == "buy" else -1)

    peak = np.maximum.accumulate(equity)
    drawdown = equity / peak - 1
    step = max(1, len(equity) // points)
    for symbol, book in attribution.items():
        mark = float(closes[columns[symbol]][-1])
        position = state["positions"].get(symbol, {})
        book["short"] = position.get("quantity", 0) < 0
        book["unrealized"] = round(
            mark * position.get("quantity", 0) - float(position.get("cost", 0)), 2
        )
        book["realized"] = round(book["realized"], 2)
        book["total"] = round(book["realized"] + book["unrealized"], 2)
        book["quantity"] = position.get("quantity", 0)

    # A closing trade is one that realized something, whichever side it was on.
    # A short realizes its result when it is bought back, and its opening sale
    # realizes nothing; counting sells would score both backwards.
    round_trips = [float(f["realized"]) for f in state["fills"] if float(f["realized"]) != 0]
    wins = [value for value in round_trips if value > 0]
    losses = [value for value in round_trips if value < 0]
    # Gross, so a short counts as exposure rather than cancelling a long.
    exposure = float(np.mean(gross / np.where(equity == 0, 1, equity))) if len(equity) else 0.0

    # Against the market, not just against zero. The account and the index are
    # sampled at session closes so the annualized figures mean what they say.
    benchmark = opening * level
    ends = _session_ends(first, cursor, start)
    sessions = len(ends)
    against = summarize(
        equity[ends].tolist(),
        benchmark[ends].tolist(),
        [{"pnl": value} for value in round_trips],
        opening,
    )
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
        "gross_exposure": round(float(gross[-1]), 2) if len(gross) else 0.0,
        "trades": len(round_trips),
        "win_rate": round(len(wins) / len(round_trips), 4) if round_trips else None,
        "profit_factor": round(sum(wins) / -sum(losses), 3) if losses else None,
        "average_win": round(float(np.mean(wins)), 2) if wins else None,
        "average_loss": round(float(np.mean(losses)), 2) if losses else None,
        "attribution": sorted(attribution.values(), key=lambda b: -abs(b["total"])),
        "bars_observed": len(equity),
        "benchmark": {
            "name": benchmark_name(state),
            "equity": round(float(benchmark[-1]), 2) if len(benchmark) else opening,
            "total_return": round(float(level[-1] - 1), 6) if len(level) else 0.0,
            "curve": [
                {"time": int(times[index]), "equity": round(float(benchmark[index]), 2)}
                for index in range(0, len(benchmark), step)
            ]
            + (
                [{"time": int(times[-1]), "equity": round(float(benchmark[-1]), 2)}]
                if len(benchmark)
                else []
            ),
        },
        # Risk and market-relative figures over session closes, from the same
        # summary the research courses use.
        "sessions": sessions,
        "risk": {
            key: (round(value, 6) if isinstance(value, float) else value)
            for key, value in against.items()
            if key
            in (
                "cagr",
                "sharpe",
                "sortino",
                "calmar",
                "alpha",
                "beta",
                "var_95",
                "cvar_95",
                "max_drawdown",
            )
        },
        # Annualizing a handful of sessions produces a number, not a measurement.
        "risk_is_meaningful": sessions >= 20,
    }


# Twenty sessions ahead. The market is generated in blocks that always run at
# least this far past the cursor, so the diary covers a fixed window rather than
# however much of the market happens to have been generated — two learners on the
# same bar see the same calendar, and its length reveals nothing about the engine.
CALENDAR_AHEAD = SESSION * 20


def calendar(state, data, room, ahead=None):
    """Scheduled releases either side of the cursor.

    A calendar names what is coming and when. For anything still ahead of the
    run's clock that is all it carries: the release's name and its date, plus the
    published consensus for a company's results. The outcome is attached only
    once the cursor has reached the bar that prints it.
    """
    cursor = state["cursor"]
    series = next(iter(data.values()))
    times = series.time
    limit = min(len(series) - 1, cursor + (CALENDAR_AHEAD if ahead is None else ahead))

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

    # An appointment book: every company's next print, plus the ones that landed
    # recently enough to still be worth reading against what was expected. The
    # dates come from the reporting cycle rather than from the generated blocks,
    # so the board does not lengthen as the engine runs further ahead.
    earnings = []
    tag = state["config"].get("universe")
    seed = state["config"]["seed"]
    # Quarters carried in from before the run began sit at negative indices: they
    # are opening history for the statements, not appointments on this diary.
    recent = max(0, cursor - CALENDAR_AHEAD)
    for symbol, book in room.books.items():
        position, index = report_slot(seed, symbol, cursor, SESSION)
        scheduled = next((q for q in book if q["index"] == index), None)
        prior = sum(1 for quarter in book if quarter["index"] < 0)
        if index < len(times):
            earnings.append(
                {
                    "symbol": symbol,
                    **profile(symbol, tag),
                    "label": scheduled["label"]
                    if scheduled
                    else quarter_label(position + prior),
                    "index": index,
                    "time": int(times[index]),
                    "bars_away": index - cursor,
                    "released": False,
                    # The street sets its estimate once the quarter is scheduled.
                    "consensus_eps": scheduled["consensus_eps"] if scheduled else None,
                    "consensus_revenue": scheduled["consensus_revenue"] if scheduled else None,
                }
            )
        printed = [q for q in book if recent <= q["index"] <= cursor]
        for quarter in printed:
            earnings.append(
                {
                    "symbol": symbol,
                    **profile(symbol, tag),
                    "label": quarter["label"],
                    "index": quarter["index"],
                    "time": int(times[quarter["index"]]),
                    "bars_away": quarter["index"] - cursor,
                    "released": True,
                    "consensus_eps": quarter["consensus_eps"],
                    "consensus_revenue": quarter["consensus_revenue"],
                    "eps": quarter["eps"],
                    "revenue": quarter["revenue"],
                    "eps_surprise": quarter["eps_surprise"],
                    "revenue_surprise": quarter["revenue_surprise"],
                }
            )

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
