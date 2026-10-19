"""Lesson-linked practice missions for the trading simulator.

A mission is a fixed starting point — a seed, a cursor and a company — plus a
short brief and a handful of objectives. The objectives describe *process*: what
the learner did and recorded, not whether the trade made money. A profitable
breach of a rule is still a breach, and a loss taken while following the rules is
not evidence the rules were wrong, so nothing here is scored on P&L.

Every objective is decided from the run's own stored state, so progress is the
same on any device and cannot be claimed by the browser.
"""

from dataclasses import dataclass

from quanta.services.simulator_universe import BY_SYMBOL


@dataclass(frozen=True)
class Objective:
    id: str
    title: str
    detail: str
    check: str
    target: dict


@dataclass(frozen=True)
class Mission:
    id: str
    title: str
    subtitle: str
    lessons: tuple
    brief: str
    seed: int
    cursor: int
    symbol: str
    objectives: tuple


def _o(id, title, detail, check, **target):
    return Objective(id, title, detail, check, target)


MISSIONS = {
    mission.id: mission
    for mission in [
        Mission(
            "first-order",
            "Place your first paper order",
            "Read a quote, choose an order type, and write down why",
            ("0.4", "0.5"),
            "Novara Microsystems is quoted in the watchlist. Decide what you are willing "
            "to pay before you look at the chart again, enter a limit order at that "
            "price, and write the reason in the ticket's thesis box. Then advance the "
            "replay and watch what the order does. A limit that never fills is a "
            "result too: it tells you the market did not come to your price.",
            9001,
            499,
            "NVRA",
            (
                _o(
                    "limit-entry",
                    "Enter with a limit order",
                    "At least one buy order priced with a limit rather than taken at market.",
                    "order_kind",
                    side="buy",
                    kinds=["limit", "stop_limit"],
                    count=1,
                ),
                _o(
                    "thesis",
                    "Record a thesis on every order",
                    "Every order you place carries a written reason.",
                    "thesis_on_every_order",
                ),
                _o(
                    "observe",
                    "Advance the replay to see the outcome",
                    "Move the clock on by at least one full session after your first order.",
                    "bars_after_first_order",
                    bars=390,
                ),
            ),
        ),
        Mission(
            "position-size",
            "Size a position you could survive",
            "Put a limit on one idea before the market tests it",
            ("0.7",),
            "Pick any company and decide, before buying, the largest share of the "
            "account you would accept losing on it. Keep every position under 5% of "
            "your opening equity, place at least three orders so the limit has to hold "
            "more than once, and advance a full week. The objective is the rule, not "
            "the return: a position that stayed inside the limit and lost money still "
            "passes.",
            9002,
            499,
            "ZEPH",
            (
                _o(
                    "cap",
                    "Keep every position under 5% of opening equity",
                    "No holding's cost basis exceeded $5,000 at any point.",
                    "position_cap",
                    percent=5,
                ),
                _o(
                    "repeat",
                    "Place at least three orders",
                    "A limit you apply once is a decision; applied repeatedly it is a rule.",
                    "order_count",
                    count=3,
                ),
                _o(
                    "week",
                    "Advance a full week",
                    "Carry the positions through five modeled sessions.",
                    "bars_after_first_order",
                    bars=1950,
                ),
            ),
        ),
        Mission(
            "earnings-gap",
            "Hold a company through its results",
            "Meet a scheduled print and the gap it opens",
            ("8.1", "8.2"),
            "Novara Microsystems reports this quarter. The Company tab shows the "
            "consensus the simulated street has published; the result itself does not "
            "exist until the clock reaches the print. Take a position before it, hold "
            "through the open that carries the result, and write what you expected "
            "beforehand so you can compare it afterwards.",
            9003,
            499,
            "NVRA",
            (
                _o(
                    "before",
                    "Open a position before the print",
                    "Hold at least 25 shares when the quarterly result is released.",
                    "held_through_report",
                    shares=25,
                ),
                _o(
                    "thesis",
                    "Write what you expected first",
                    "Every order you place carries a written reason.",
                    "thesis_on_every_order",
                ),
                _o(
                    "after",
                    "Stay for the session after the result",
                    "Advance at least one session past the print rather than reacting to the gap alone.",
                    "bars_after_report",
                    bars=390,
                ),
            ),
        ),
        Mission(
            "read-the-tape",
            "Trade what the tape actually said",
            "Act on a scored headline, not on a hunch",
            ("8.3", "8.4"),
            "Every headline in the newsroom carries a score: one point is one basis "
            "point of modeled move, and routine chatter scores zero. Wait for an item "
            "worth at least 150 points on the company you are watching, then enter "
            "within the session that follows and name the headline in your thesis. "
            "Chatter is there to tempt you; it moves nothing.",
            9004,
            499,
            "VLOC",
            (
                _o(
                    "scored",
                    "Enter after a scored headline",
                    "Your first entry followed an item worth 150 points or more on that company, within one session.",
                    "entry_after_scored_news",
                    points=150,
                    within=390,
                ),
                _o(
                    "thesis",
                    "Name the headline in your thesis",
                    "Every order you place carries a written reason.",
                    "thesis_on_every_order",
                ),
                _o(
                    "cap",
                    "Keep the position under 10% of opening equity",
                    "Conviction from one headline is still one headline.",
                    "position_cap",
                    percent=10,
                ),
            ),
        ),
        Mission(
            "stop-discipline",
            "Protect a position before you need to",
            "Attach the exit while the entry is still calm",
            ("0.4", "0.7"),
            "Open a position, then place the sell stop that defines how much of it you "
            "are prepared to lose — while the price is still where you bought it, not "
            "after it has moved against you. A stop is a decision made in advance; "
            "placing one during a decline is a different decision under worse "
            "conditions.",
            9005,
            499,
            "QBIT",
            (
                _o(
                    "entry",
                    "Open a position",
                    "At least one buy order filled.",
                    "filled_buy",
                ),
                _o(
                    "stop",
                    "Place a protective sell stop",
                    "A sell stop, stop-limit or trailing stop — including one attached to "
                    "the entry as a bracket. What counts is that the exit was decided "
                    "before it was needed.",
                    "order_kind",
                    side="sell",
                    kinds=["stop", "stop_limit", "trailing_stop"],
                    count=1,
                ),
                _o(
                    "thesis",
                    "Record a thesis on every order",
                    "Every order you place carries a written reason.",
                    "thesis_on_every_order",
                ),
            ),
        ),
        Mission(
            "charter",
            "Trade inside your written limits",
            "The rules you wrote, applied for a week",
            ("12.16", "12.13"),
            "This mission checks the charter from the ethics course rather than a "
            "result. Keep every position under 5% of opening equity, write a thesis on "
            "every order, and close everything before you finish, so the account ends "
            "flat and the record is complete. Nothing here rewards a profit or "
            "punishes a loss.",
            9006,
            499,
            "MRDN",
            (
                _o(
                    "cap",
                    "Keep every position under 5% of opening equity",
                    "No holding's cost basis exceeded $5,000 at any point.",
                    "position_cap",
                    percent=5,
                ),
                _o(
                    "thesis",
                    "Record a thesis on every order",
                    "Every order you place carries a written reason.",
                    "thesis_on_every_order",
                ),
                _o(
                    "flat",
                    "Close every position before finishing",
                    "End the mission holding no shares, so the record is complete.",
                    "flat_after",
                    bars=1950,
                ),
            ),
        ),
    ]
}

BY_LESSON = {}
for mission in MISSIONS.values():
    for lesson in mission.lessons:
        BY_LESSON.setdefault(lesson, mission.id)


def listing():
    """The catalog, for the lesson pages and the mission picker."""
    return [
        {
            "id": mission.id,
            "title": mission.title,
            "subtitle": mission.subtitle,
            "lessons": list(mission.lessons),
            "brief": mission.brief,
            "symbol": mission.symbol,
            "name": BY_SYMBOL[mission.symbol].name,
            "objectives": [
                {"id": o.id, "title": o.title, "detail": o.detail} for o in mission.objectives
            ],
        }
        for mission in MISSIONS.values()
    ]


def _first_order_bar(state, times):
    """Bar index of the earliest order, or None if nothing has been placed."""
    stamps = [order["time"] for order in state["orders"]]
    if not stamps:
        return None
    earliest = min(stamps)
    for index, moment in enumerate(times):
        if moment >= earliest:
            return index
    return None


def _cost_history(state, symbol=None):
    """Running cost basis per company, in the order the fills were recorded."""
    running, peak = {}, {}
    for fill in sorted(state["fills"], key=lambda f: f["time"]):
        if symbol and fill["symbol"] != symbol:
            continue
        held = running.get(fill["symbol"], 0.0)
        if fill["side"] == "buy":
            held += float(fill["price"]) * fill["quantity"] + float(fill["fee"])
        else:
            held = max(0.0, held - float(fill["price"]) * fill["quantity"])
        running[fill["symbol"]] = held
        peak[fill["symbol"]] = max(peak.get(fill["symbol"], 0.0), held)
    return peak


def _report_bar(room, symbol):
    """Bar the company's in-run quarter printed on, if it has been scheduled."""
    quarters = [q for q in room.books.get(symbol, []) if q["index"] >= 0]
    return quarters[0]["index"] if quarters else None


CHECKS = {}


def check(name):
    def register(function):
        CHECKS[name] = function
        return function

    return register


def entries(state):
    """Orders the learner placed, not the exits an entry carried with it.

    A bracket reaches the blotter as three rows, but it was one decision. Counting
    its legs separately would ask for a thesis the learner already wrote and make
    a single order look like three.
    """
    return [order for order in state["orders"] if not order.get("parent_id")]


@check("thesis_on_every_order")
def _thesis(state, mission, target, room, times):
    orders = entries(state)
    if not orders:
        return False, "No orders placed yet."
    missing = [o for o in orders if not o.get("note", "").strip()]
    if missing:
        return False, f"{len(missing)} of {len(orders)} orders have no written reason."
    return True, f"All {len(orders)} orders carry a thesis."


@check("order_kind")
def _order_kind(state, mission, target, room, times):
    matches = [
        o for o in state["orders"] if o["side"] == target["side"] and o["kind"] in target["kinds"]
    ]
    needed = target["count"]
    kinds = " or ".join(target["kinds"]).replace("_", "-")
    if len(matches) >= needed:
        return True, f"{len(matches)} {target['side']} {kinds} order(s) placed."
    return False, f"{len(matches)} of {needed} {target['side']} {kinds} order(s) placed."


@check("order_count")
def _order_count(state, mission, target, room, times):
    placed = len(entries(state))
    return placed >= target["count"], f"{placed} of {target['count']} orders placed."


@check("filled_buy")
def _filled_buy(state, mission, target, room, times):
    fills = [f for f in state["fills"] if f["side"] == "buy"]
    return bool(fills), (
        f"{len(fills)} buy fill(s) recorded." if fills else "No buy order has filled yet."
    )


@check("position_cap")
def _position_cap(state, mission, target, room, times):
    opening = float(state["ledger"][0]["cash"]) if state["ledger"] else 100000.0
    ceiling = opening * target["percent"] / 100
    peaks = _cost_history(state)
    if not peaks:
        return False, "No position has been opened yet."
    worst = max(peaks.values())
    breached = [s for s, value in peaks.items() if value > ceiling + 0.005]
    if breached:
        return False, (
            f"{', '.join(sorted(breached))} exceeded the ${ceiling:,.0f} limit "
            f"(largest ${worst:,.0f})."
        )
    return True, f"Largest position reached ${worst:,.0f} against a ${ceiling:,.0f} limit."


@check("bars_after_first_order")
def _bars_after_first_order(state, mission, target, room, times):
    start = _first_order_bar(state, times)
    if start is None:
        return False, "No order placed yet."
    moved = state["cursor"] - start
    return moved >= target["bars"], (
        f"{max(0, moved):,} of {target['bars']:,} observations advanced since the first order."
    )


@check("held_through_report")
def _held_through_report(state, mission, target, room, times):
    index = _report_bar(room, mission.symbol)
    if index is None:
        return False, f"{mission.symbol}'s quarter has not been scheduled yet."
    if state["cursor"] < index:
        return False, f"The print is {index - state['cursor']:,} observations ahead."
    held = 0
    for fill in sorted(state["fills"], key=lambda f: f["time"]):
        if fill["symbol"] != mission.symbol or fill["time"] > int(times[index]):
            continue
        held += fill["quantity"] if fill["side"] == "buy" else -fill["quantity"]
    if held >= target["shares"]:
        return True, f"Held {held} shares through the print."
    return False, f"Held {held} shares at the print; {target['shares']} were needed."


@check("bars_after_report")
def _bars_after_report(state, mission, target, room, times):
    index = _report_bar(room, mission.symbol)
    if index is None or state["cursor"] < index:
        return False, "The result has not been released yet."
    moved = state["cursor"] - index
    return moved >= target["bars"], (
        f"{moved:,} of {target['bars']:,} observations advanced since the result."
    )


@check("entry_after_scored_news")
def _entry_after_scored_news(state, mission, target, room, times):
    buys = [f for f in state["fills"] if f["symbol"] == mission.symbol and f["side"] == "buy"]
    if not buys:
        return False, f"No {mission.symbol} position opened yet."
    first = min(f["time"] for f in buys)
    for event in room.events:
        if event["symbol"] != mission.symbol or abs(event["points"]) < target["points"]:
            continue
        if event["index"] >= len(times):
            continue
        moment = int(times[event["index"]])
        if moment <= first <= moment + target["within"] * 60:
            return True, (
                f"Entry followed a {event['points']:+d} point item: {event['headline'][:60]}."
            )
    return False, (
        f"The first {mission.symbol} entry did not follow an item worth "
        f"{target['points']} points within a session."
    )


@check("flat_after")
def _flat_after(state, mission, target, room, times):
    start = _first_order_bar(state, times)
    if start is None:
        return False, "No order placed yet."
    if state["cursor"] - start < target["bars"]:
        return False, (
            f"{max(0, state['cursor'] - start):,} of {target['bars']:,} observations advanced."
        )
    open_shares = {s: p["quantity"] for s, p in state["positions"].items() if p["quantity"]}
    if open_shares:
        return False, "Still holding " + ", ".join(
            f"{quantity} {symbol}" for symbol, quantity in sorted(open_shares.items())
        )
    return True, "Every position closed and the record is complete."


def progress(mission, state, room, times):
    """Each objective decided from the run's stored state, never from P&L."""
    results = []
    for objective in mission.objectives:
        met, detail = CHECKS[objective.check](state, mission, objective.target, room, times)
        results.append(
            {
                "id": objective.id,
                "title": objective.title,
                "detail": objective.detail,
                "met": met,
                "progress": detail,
            }
        )
    return results
