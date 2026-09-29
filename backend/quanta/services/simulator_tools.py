"""Monitor tools: the tape, the book, the heat and the screens.

A terminal is several windows onto one market at once. These build the windows
the chart does not: individual prints inside a bar, a book of resting size around
the last trade, sector heat across the whole listing, and named screens over the
statistics the desk already computes.

Everything here is generated from the run's seed and its cursor, so a tool is the
same on any device and keeps producing as the clock runs. Two of them — the tape
and the book — describe detail the execution model does not itself simulate: the
engine fills from a bar's open, high, low and close and treats the path between
them as unknown. They are labelled as illustrations for that reason, and nothing
in them feeds back into a fill.
"""

import hashlib

import numpy as np

from quanta.services.simulator_desk import (
    SESSION,
    _annualized,
    _closes,
    _column,
    _prior_close,
    quotes_table,
    rsi,
    sma,
    windows,
)
from quanta.services.simulator_universe import profile

# An illustration is not a measurement, and the difference has to travel with the
# data rather than live in the docs.
TAPE_NOTICE = (
    "Illustrative prints. The execution model fills from a bar's open, high, low "
    "and close and treats the path between them as unknown, so these are one "
    "consistent way the bar could have traded, not a path the engine simulated."
)
BOOK_NOTICE = (
    "Illustrative depth. This run fills against bar volume and a fixed spread, "
    "not against resting orders, so the sizes shown are indicative of liquidity "
    "rather than a book any order queues in."
)


def _stream(symbol: str) -> int:
    """A stable per-symbol stream key.

    Python's own string hash is salted per process, so using it here would give a
    different tape every time the server restarted.
    """
    return int(hashlib.sha256(symbol.encode()).hexdigest()[:8], 16)


def _prints(rng, bar, count):
    """One bar's trades: a path from open to close that reaches both extremes.

    The path is invented, but it is constrained by everything the bar actually
    states — it opens at the open, closes at the close, touches the high and the
    low exactly once each, stays inside the range, and its sizes sum to the bar's
    volume. A learner reading the tape against the candle sees no contradiction.
    """
    opening, high, low, closing = (bar["open"], bar["high"], bar["low"], bar["close"])
    count = max(4, count)
    # A drift from open to close, roughened, then folded back into the range.
    path = np.linspace(opening, closing, count)
    span = max(high - low, 0.01)
    path = path + rng.normal(0, span * 0.22, count)
    path = np.clip(path, low, high)
    path[0], path[-1] = opening, closing
    # The extremes are facts about the bar, so the tape has to contain them.
    reach = rng.choice(np.arange(1, count - 1), size=2, replace=False)
    path[reach[0]], path[reach[1]] = high, low

    weights = rng.random(count) + 0.35
    sizes = np.maximum(1, (weights / weights.sum() * bar["volume"]).astype(np.int64))
    sizes[-1] = max(1, int(bar["volume"]) - int(sizes[:-1].sum()))
    if sizes[-1] < 1:
        sizes[-1] = 1

    seconds = np.sort(rng.choice(np.arange(60), size=min(count, 60), replace=False))
    if len(seconds) < count:
        seconds = np.concatenate((seconds, np.full(count - len(seconds), 59)))
    return path, sizes, seconds


def tape(state, data, symbol, limit=60):
    """Time and sales: the most recent prints, newest first.

    The aggressor is read off the tick rule — a print above the last one is taken
    as a buyer lifting the offer — which is the same inference a real tape forces,
    and wrong for the same reasons often enough to be worth teaching.
    """
    cursor = state["cursor"]
    series = data[symbol]
    seed = int(state["config"]["seed"])
    rows = []
    index = cursor
    previous = None
    while index >= 0 and len(rows) < limit:
        bar = series[index]
        rng = np.random.default_rng([seed, index, _stream(symbol)])
        count = int(rng.integers(5, 13))
        path, sizes, seconds = _prints(rng, bar, count)
        block = []
        for position in range(len(path)):
            price = round(float(path[position]), 2)
            side = (
                "—"
                if previous is None or price == previous
                else ("buy" if price > previous else "sell")
            )
            previous = price
            block.append(
                {
                    "time": int(bar["time"]) + int(seconds[position]),
                    "price": price,
                    "size": int(sizes[position]),
                    "side": side,
                    "index": index,
                }
            )
        rows.extend(reversed(block))
        previous = None
        index -= 1
    rows = rows[:limit]
    volume = sum(row["size"] for row in rows)
    taken = sum(row["size"] for row in rows if row["side"] == "buy")
    return {
        "symbol": symbol,
        **profile(symbol, state["config"].get("universe")),
        "prints": rows,
        "volume": volume,
        # What share of the printed volume went out at the offer. Read as pressure,
        # not as fact: the tick rule mislabels a print that opens a new level.
        "buy_share": round(taken / volume, 4) if volume else None,
        "notice": TAPE_NOTICE,
    }


def book(state, data, symbol, levels=8):
    """Indicative resting size either side of the last trade.

    The spread comes from the run's own configuration, so the book agrees with
    what an order would actually pay, and size thins with distance the way a real
    one does. It is regenerated each bar from the cursor, so it moves with the
    market rather than sitting still.
    """
    cursor = state["cursor"]
    series = data[symbol]
    bar = series[cursor]
    last = bar["close"]
    spread = last * float(state["config"]["spread_bps"]) / 10000
    tick = max(0.01, round(spread / 2, 2))
    rng = np.random.default_rng([int(state["config"]["seed"]), cursor, _stream(symbol)])
    base = max(1, int(bar["volume"]) // 20)
    bids, asks = [], []
    bid_total = ask_total = 0
    for level in range(levels):
        decay = float(rng.uniform(0.75, 1.35)) * (1 + level * 0.45)
        bid_size = max(1, int(base * decay))
        ask_size = max(1, int(base * float(rng.uniform(0.75, 1.35)) * (1 + level * 0.45)))
        bid_total += bid_size
        ask_total += ask_size
        bids.append(
            {
                "price": round(last - spread / 2 - level * tick, 2),
                "size": bid_size,
                "cumulative": bid_total,
            }
        )
        asks.append(
            {
                "price": round(last + spread / 2 + level * tick, 2),
                "size": ask_size,
                "cumulative": ask_total,
            }
        )
    depth = bid_total + ask_total
    return {
        "symbol": symbol,
        "last": round(last, 2),
        "bid": bids[0]["price"],
        "ask": asks[0]["price"],
        "spread": round(asks[0]["price"] - bids[0]["price"], 2),
        "bids": bids,
        "asks": asks,
        # Above a half, more size is resting on the bid than on the offer.
        "imbalance": round(bid_total / depth, 4) if depth else None,
        "notice": BOOK_NOTICE,
    }


def heatmap(state, data, room):
    """Every listed company at once, grouped by sector and sized by turnover.

    A ranked table answers "what moved most"; a heat map answers "where did the
    market move", which is a different question and usually the more useful one
    when a macro print has pushed a whole sector one way.
    """
    rows = quotes_table(state, data, room)
    sectors = {}
    for row in rows:
        name = row["sector"] or "Unclassified"
        group = sectors.setdefault(name, {"sector": name, "companies": [], "notional": 0.0})
        group["companies"].append(
            {
                "symbol": row["symbol"],
                "name": row["name"],
                "close": round(row["close"], 2),
                "change_pct": row["change_pct"],
                "relative_volume": row["relative_volume"],
                "notional": row["notional"],
                "sentiment": row["sentiment"],
            }
        )
        group["notional"] += row["notional"]
    for group in sectors.values():
        group["companies"].sort(key=lambda c: -c["notional"])
        weights = [c["notional"] for c in group["companies"]]
        total = sum(weights) or 1
        # Weighted by turnover: a sector's colour should follow where the money
        # traded, not where the smallest name in it happened to close.
        group["change_pct"] = round(
            sum(c["change_pct"] * w for c, w in zip(group["companies"], weights)) / total, 2
        )
        group["companies_count"] = len(group["companies"])
        group["notional"] = round(group["notional"])
    ordered = sorted(sectors.values(), key=lambda g: -g["change_pct"])
    changes = [row["change_pct"] for row in rows]
    return {
        "sectors": ordered,
        "companies": len(rows),
        "best": max(changes) if changes else 0.0,
        "worst": min(changes) if changes else 0.0,
        "weighting": "turnover over the session window",
    }


# Screens are named rather than free-form. A learner who picks "oversold after a
# miss" is choosing a hypothesis they can be wrong about; one who dials in
# RSI < 31.4 is usually fitting the filter to the answer they already wanted.
SCREENS = {
    "momentum": {
        "label": "Trending up",
        "description": "Above both moving averages, leading the session.",
    },
    "oversold": {
        "label": "Oversold",
        "description": "RSI under 30 with the session against them.",
    },
    "overbought": {
        "label": "Overbought",
        "description": "RSI over 70 after an extended run.",
    },
    "volume": {
        "label": "Unusual volume",
        "description": "Trading well above their own recent average.",
    },
    "cheap": {
        "label": "Low earnings multiple",
        "description": "Lowest price to trailing earnings in the listing.",
    },
    "volatile": {
        "label": "Widest ranges",
        "description": "Highest annualized volatility over the window.",
    },
    "all": {"label": "Whole listing", "description": "Every company, unfiltered."},
}


def _multiple(symbol, room, cursor, close):
    """Trailing price to earnings, from released quarters only.

    Ranking on a quarter the learner has not been shown would hand back the very
    answer the screen is meant to search for, so the filter here is the same one
    the statements endpoint applies.
    """
    if not room or symbol not in room.books:
        return None
    quarters = [q for q in room.books[symbol] if q["index"] < 0 or q["index"] <= cursor]
    trailing = sum(q["eps"] for q in quarters[-4:]) if len(quarters) >= 4 else None
    if not trailing or trailing <= 0:
        return None
    return round(close / trailing, 1)


def screener(state, data, room, screen="all", limit=25):
    """A named screen over the desk's own statistics, ranked on the server.

    Every column here is computed from bars at or before the cursor, and the
    earnings multiple uses released quarters only — reading an unreported print to
    rank a company would hand back the answer the screen is supposed to search for.
    """
    cursor = state["cursor"]
    bars, short, _ = windows(state)
    rows = []
    # Conventional periods, in this run's own observations: twenty and fifty of
    # them, which on a minute market is the last twenty and fifty minutes and on
    # a daily replay the last twenty and fifty sessions.
    fast_period, slow_period = 20, 50
    for row in quotes_table(state, data, room):
        symbol = row["symbol"]
        closes = _closes(data[symbol], cursor)
        strength = rsi(closes, 14)
        fast = sma(closes, fast_period)
        slow = sma(closes, slow_period)
        last = row["close"]
        position = row["window_high"] - row["window_low"]
        rows.append(
            {
                **row,
                "close": round(last, 2),
                "rsi": round(strength, 1) if strength is not None else None,
                "above_fast": fast is not None and last > fast,
                "above_slow": slow is not None and last > slow,
                "sma_fast": round(fast, 2) if fast is not None else None,
                "sma_slow": round(slow, 2) if slow is not None else None,
                "range_position": round((last - row["window_low"]) / position, 3)
                if position
                else None,
                "multiple": _multiple(symbol, room, cursor, last),
                "window_high": round(row["window_high"], 2),
                "window_low": round(row["window_low"], 2),
            }
        )

    def has(row, key):
        return row[key] is not None

    if screen == "momentum":
        rows = [r for r in rows if r["above_fast"] and r["above_slow"]]
        rows.sort(key=lambda r: -r["change_pct"])
    elif screen == "oversold":
        rows = [r for r in rows if has(r, "rsi") and r["rsi"] < 30]
        rows.sort(key=lambda r: r["rsi"])
    elif screen == "overbought":
        rows = [r for r in rows if has(r, "rsi") and r["rsi"] > 70]
        rows.sort(key=lambda r: -r["rsi"])
    elif screen == "volume":
        rows = [r for r in rows if has(r, "relative_volume")]
        rows.sort(key=lambda r: -r["relative_volume"])
    elif screen == "cheap":
        rows = [r for r in rows if has(r, "multiple")]
        rows.sort(key=lambda r: r["multiple"])
    elif screen == "volatile":
        rows = [r for r in rows if has(r, "volatility")]
        rows.sort(key=lambda r: -r["volatility"])
    else:
        rows.sort(key=lambda r: -r["change_pct"])
    return {
        "screen": screen,
        **SCREENS.get(screen, SCREENS["all"]),
        "screens": [{"id": key, **value} for key, value in SCREENS.items()],
        "matches": len(rows),
        "rows": rows[:limit],
        "window_bars": short,
        "session_bars": bars,
        "fast_bars": fast_period,
        "slow_bars": slow_period,
    }


def sessions_summary(state, data, symbol, count=10):
    """The last few session closes for one company, oldest first.

    A minute chart makes a week hard to see. This is the same data the chart
    holds, aggregated to sessions so a learner can read the swing without
    changing interval and losing their place.
    """
    cursor = state["cursor"]
    series = data[symbol]
    closes = _closes(series, cursor)
    volumes = _column(series, cursor, "volume")
    if not hasattr(series, "session"):
        edges = np.arange(len(closes))
    else:
        sessions = np.asarray(series.session[: cursor + 1])
        edges = np.append(np.flatnonzero(np.diff(sessions)), len(closes) - 1)
    edges = edges[-count:]
    rows = []
    for position, end in enumerate(edges):
        start = int(edges[position - 1]) + 1 if position else max(0, int(end) - SESSION + 1)
        window = closes[start : int(end) + 1]
        if not len(window):
            continue
        prior = float(closes[start - 1]) if start else float(window[0])
        rows.append(
            {
                "time": int(series.time[int(end)])
                if hasattr(series, "time")
                else int(series[int(end)]["time"]),
                "open": round(float(window[0]), 2),
                "high": round(float(window.max()), 2),
                "low": round(float(window.min()), 2),
                "close": round(float(window[-1]), 2),
                "volume": int(volumes[start : int(end) + 1].sum()),
                "change_pct": round((float(window[-1]) / prior - 1) * 100, 2) if prior else 0.0,
            }
        )
    return {
        "symbol": symbol,
        "sessions": rows,
        "volatility": _annualized(closes, min(len(closes), SESSION * 5), SESSION),
        "prior_close": round(_prior_close(series, cursor), 2),
    }
