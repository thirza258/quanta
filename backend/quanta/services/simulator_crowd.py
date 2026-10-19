"""Other participants in the generated market, and what they are doing.

A learner watching a terminal alone sees prices move with nobody moving them.
This module names the rest of the market: a handful of desks, each with one
stated style, whose orders and fills can be read bar by bar beside the chart.

Three rules keep them honest.

They are *derived from* the market, never causes of it. Prices come from the
factor model and the newsroom; a desk here is a reading of what the bars and
headlines already did, in the same way the tape is. Nothing a desk does feeds
back into a price, a fill or the account.

They trade under the learner's own rules. A desk that decides on one bar is
eligible on the next, its limit orders fill only when the price trades through
them, its market orders fill at the next open, and every fill it reports is one
of the prints the tape shows for that bar. A crowd that could act on the bar
it read would always win, which is look-ahead wearing a counterparty's clothes.

They are named for their style, not as firms. "Momentum desk" is what the
learner needs to know and cannot be mistaken for anyone real.
"""

from dataclasses import dataclass

import numpy as np

from quanta.services.simulator_tools import _stream

# How far back the flow is read, and how long an unfilled order stays working.
# Both are bounded so a bar's flow can be computed from that bar alone, without
# replaying the run and without depending on how much market has been generated.
WINDOW = 120
LIFETIME = 30

NOTICE = (
    "Generated participants. These desks are read off the same bars and "
    "headlines you can see; they do not move prices, and nothing they do "
    "reaches your account. Each is named for its style rather than as a firm."
)


@dataclass(frozen=True)
class Desk:
    id: str
    name: str
    style: str


DESKS = (
    Desk("momentum", "Momentum desk", "Buys strength and sells weakness over the short window."),
    Desk("value", "Value desk", "Leans against price when it runs far from its longer average."),
    Desk("maker", "Market-making desk", "Works both sides close to the touch, all session."),
    Desk("macro", "Macro desk", "Acts on the bar after a market-wide release."),
    Desk("event", "Event desk", "Acts on the bar after a scored company headline."),
    Desk("index", "Index tracker", "Trades only at a session's first and last bars."),
    Desk("retail", "Retail flow", "Arrives two to four bars behind the headline."),
)
BY_ID = {desk.id: desk for desk in DESKS}


def _facts(closes, highs, lows, volumes, index, short, long_):
    """What a desk could have known at the close of `index`, and nothing later."""
    window = closes[max(0, index - short + 1) : index + 1]
    trail = closes[max(0, index - long_ + 1) : index + 1]
    prior = closes[index - 1] if index else closes[index]
    return {
        "close": float(closes[index]),
        "change": float(closes[index] - prior),
        "short_mean": float(window.mean()),
        "long_mean": float(trail.mean()),
        "range": float(highs[index] - lows[index]),
        "volume": float(volumes[max(0, index - 20) : index + 1].mean()),
    }


def _intent(desk, facts, news, index, session_bars, rng):
    """One desk's decision at the close of a bar, or None if it stands aside.

    Each style reads one thing and ignores the rest. That is the point: a
    learner watching the flow should be able to predict what a desk will do
    from its stated style, and notice when the styles disagree.
    """
    if desk.id == "momentum":
        if abs(facts["close"] - facts["short_mean"]) < facts["range"] * 0.1:
            return None
        above = facts["close"] > facts["short_mean"]
        return (
            "buy" if above else "sell",
            "market",
            None,
            f"Price {'above' if above else 'below'} its short average.",
        )
    if desk.id == "value":
        gap = (facts["close"] - facts["long_mean"]) / max(facts["long_mean"], 0.01)
        if abs(gap) < 0.004:
            return None
        # Leaning against the move, so it waits at a price rather than paying up.
        side = "sell" if gap > 0 else "buy"
        edge = facts["range"] * 0.35 + 0.01
        limit = round(facts["close"] + (edge if side == "sell" else -edge), 2)
        return side, "limit", limit, f"{abs(gap) * 100:.1f}% from its longer average."
    if desk.id == "maker":
        side = "buy" if rng.random() < 0.5 else "sell"
        edge = max(0.01, round(facts["range"] * 0.18, 2))
        limit = round(facts["close"] + (edge if side == "sell" else -edge), 2)
        return side, "limit", limit, "Working the touch on both sides."
    if desk.id == "macro" and news.get("macro"):
        item = news["macro"]
        return (
            "buy" if item["points"] > 0 else "sell",
            "market",
            None,
            f"After the macro release: {item['headline']}",
        )
    if desk.id == "event" and news.get("company"):
        item = news["company"]
        return (
            "buy" if item["points"] > 0 else "sell",
            "market",
            None,
            f"After the company item: {item['headline']}",
        )
    if desk.id == "index":
        minute = index % session_bars
        if minute not in (0, session_bars - 1):
            return None
        return (
            "buy" if rng.random() < 0.55 else "sell",
            "market",
            None,
            "Session open rebalance." if minute == 0 else "Session close rebalance.",
        )
    if desk.id == "retail" and news.get("lagged"):
        item = news["lagged"]
        return (
            "buy" if item["points"] > 0 else "sell",
            "market",
            None,
            f"Following up on: {item['headline']}",
        )
    return None


def _headlines(room, symbol, sector, first, cursor):
    """Scored items per bar, split into the three a desk might react to."""
    from quanta.services.simulator_news import news_window

    macro, company = {}, {}
    for event in news_window(room, max(0, first - 6), cursor, symbol, sector):
        if not event.get("points"):
            continue
        target = macro if event["scope"] in ("macro", "market") else company
        at = event["index"]
        if at not in target or abs(event["points"]) > abs(target[at]["points"]):
            target[at] = event
    return macro, company


def _fill(order, index, highs, lows, opens, closes, cursor, offset):
    """The first bar after placement on which this order could trade.

    The learner's own rules: a market order takes the next open, a passive order
    waits for the price to trade through its limit, and nothing fills on the bar
    its desk read.
    """
    for bar in range(index + 1, min(index + LIFETIME, cursor) + 1):
        position = bar - offset
        if order["kind"] == "market":
            return bar, float(opens[position])
        limit = order["limit"]
        if order["side"] == "buy" and lows[position] < limit:
            return bar, min(float(opens[position]), limit)
        if order["side"] == "sell" and highs[position] > limit:
            return bar, max(float(opens[position]), limit)
    return None, None


def _size(rng, desk, average_volume):
    """Scaled to how much this name actually trades, by the desk's own style."""
    share = {
        "maker": 0.10,
        "momentum": 0.07,
        "value": 0.06,
        "macro": 0.05,
        "event": 0.08,
        "index": 0.12,
        "retail": 0.02,
    }[desk.id]
    size = average_volume * share * float(rng.uniform(0.55, 1.45))
    return max(1, int(size))


def flow(state, data, room, symbol, limit=60):
    """Every desk order placed in the window, newest first.

    Computed on each read from the bars and headlines at or before the cursor.
    Nothing is stored: the crowd never enters the run's state, so it cannot
    touch reservations, performance, missions or the account's history.
    """
    cursor = state["cursor"]
    series = data[symbol]
    seed = int(state["config"]["seed"])
    session_bars = 1 if state["config"].get("base_interval") == "1D" else 390
    short, long_ = max(5, session_bars // 26), max(20, session_bars)
    first = max(0, cursor - WINDOW + 1)
    # One slice covers both the facts a desk reads and the bars it can fill on.
    offset = max(0, first - long_)
    closes = np.asarray(series.close[offset : cursor + 1], dtype=float)
    highs = np.asarray(series.high[offset : cursor + 1], dtype=float)
    lows = np.asarray(series.low[offset : cursor + 1], dtype=float)
    opens = np.asarray(series.open[offset : cursor + 1], dtype=float)
    volumes = np.asarray(series.volume[offset : cursor + 1], dtype=float)
    times = np.asarray(series.time[offset : cursor + 1], dtype=np.int64)

    sector = None
    macro, company = {}, {}
    if room is not None:
        from quanta.services.simulator_universe import BY_SYMBOL

        sector = BY_SYMBOL[symbol].sector if symbol in BY_SYMBOL else None
        macro, company = _headlines(room, symbol, sector, first, cursor)

    orders = []
    for index in range(first, cursor + 1):
        position = index - offset
        facts = _facts(closes, highs, lows, volumes, position, short, long_)
        news = {
            "macro": macro.get(index),
            "company": company.get(index),
            # Retail arrives two to four bars behind the item it is following.
            "lagged": next(
                (company[index - lag] for lag in (2, 3, 4) if index - lag in company), None
            ),
        }
        for desk in DESKS:
            rng = np.random.default_rng([seed, index, _stream(desk.id), _stream(symbol)])
            decided = _intent(desk, facts, news, index, session_bars, rng)
            if not decided:
                continue
            side, kind, price, why = decided
            order = {"side": side, "kind": kind, "limit": price}
            at, fill = _fill(order, index, highs, lows, opens, closes, cursor, offset)
            quantity = _size(rng, desk, facts["volume"])
            orders.append(
                {
                    "desk": desk.name,
                    "style": desk.style,
                    "side": side,
                    "kind": kind,
                    "quantity": quantity,
                    "limit": price,
                    "placed": int(times[position]),
                    "index": index,
                    "status": "filled" if at is not None else "working",
                    "price": round(fill, 2) if fill is not None else None,
                    "filled_at": int(times[at - offset]) if at is not None else None,
                    "at": at,
                    "reason": why,
                }
            )
    # The desks cannot between them trade more of a bar than the bar traded.
    # Sizing each one against a rolling average lets a quiet bar be oversubscribed,
    # so the fills on such a bar are scaled back in proportion.
    traded = {}
    for order in orders:
        if order["at"] is not None:
            traded[order["at"]] = traded.get(order["at"], 0) + order["quantity"]
    for order in orders:
        at = order["at"]
        if at is None:
            continue
        capacity = float(volumes[at - offset])
        if traded[at] > capacity:
            order["quantity"] = max(1, int(order["quantity"] * capacity / traded[at]))
    for order in orders:
        order.pop("at", None)
    orders.sort(key=lambda o: (-o["index"], o["desk"]))
    shown = orders[:limit]
    bought = sum(o["quantity"] for o in shown if o["side"] == "buy")
    total = sum(o["quantity"] for o in shown)
    return {
        "symbol": symbol,
        "orders": shown,
        "window_bars": min(WINDOW, cursor + 1),
        "working": sum(1 for o in orders if o["status"] == "working"),
        "filled": sum(1 for o in orders if o["status"] == "filled"),
        # Which way the visible desks are leaning, by size rather than by count.
        "buy_share": round(bought / total, 4) if total else None,
        "desks": [{"id": d.id, "name": d.name, "style": d.style} for d in DESKS],
        "notice": NOTICE,
    }
