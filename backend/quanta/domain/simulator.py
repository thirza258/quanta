"""The paper-trading execution model, as the API calls it.

The rules themselves (order validation, cash and share reservations, bar-by-bar
fills, attached exits, trailing stops, margin financing, buy-ins and the events
that stop a replay) are implemented by the C++ engine in backend/engine. This
module keeps the interface the services and tests have always used: it hands
the engine the run state, then writes back exactly the fields the engine
changed, in the order a dictionary would have received them.

Money crosses the boundary as the decimal strings the run stores. Fill
identifiers are minted here, in fill order, so the ledger and the blotter keep
referring to each other the way they did.
"""

from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal
from uuid import uuid4

from quanta import engine
from quanta.domain.errors import DomainError
from quanta.domain.simulator_margin import BORROW_RATE, MAINTENANCE_MARGIN, SESSIONS_A_YEAR

OPEN = {"working", "partially_filled"}
# A bracket's exits exist from the moment the entry is placed, but they cannot
# trade until it fills — the shares they would sell do not exist yet. "held" is
# deliberately outside OPEN so nothing reserves against them meanwhile.
HELD = "held"
CENT = Decimal("0.01")
MARGIN_RULES = {
    "maintenance": str(MAINTENANCE_MARGIN),
    "borrow_rate": str(BORROW_RATE),
    "sessions_a_year": SESSIONS_A_YEAR,
}


def group_of(order):
    """The one-cancels-other group an order belongs to, or its own id."""
    return order.get("oco_group") or order["id"]


def dec(value):
    return Decimal(str(value))


def money(value):
    return str(dec(value).quantize(CENT, rounding=ROUND_HALF_UP))


def now():
    return datetime.now(timezone.utc).isoformat()


def bar_at(data, symbol, index):
    if symbol not in data:
        raise DomainError("This stock is unavailable in this run.")
    return data[symbol][index]


def _text(value):
    """A field the engine reads for its truthiness, as Decimal(str(value)) when set."""
    return str(value) if value else None


def _order(order):
    """The fields of an order the engine reads, keyed as the run stores them."""
    view = {
        "id": order["id"],
        "symbol": order["symbol"],
        "side": order["side"],
        "kind": order["kind"],
        "tif": order["tif"],
        "status": order["status"],
        "quantity": order["quantity"],
        "filled": order["filled"],
        "limit_price": _text(order.get("limit_price")),
        "stop_price": _text(order.get("stop_price")),
        "trail_percent": _text(order.get("trail_percent")),
        "trail_anchor": _text(order.get("trail_anchor")),
        "forced": bool(order.get("forced")),
        "activates": order.get("activates"),
        "day": order.get("day") if isinstance(order.get("day"), str) else None,
        "role": order.get("role") or None,
        "parent_id": order.get("parent_id") or None,
        "oco_group": order.get("oco_group") or None,
    }
    for key in ("average", "notional", "fee_remaining", "reserve_price"):
        if order.get(key) is not None:
            view[key] = str(order[key])
    if "triggered" in order:
        view["triggered"] = bool(order["triggered"])
    return view


def _request(op, state, **extra):
    config = state["config"]
    return {
        "op": op,
        "cursor": state["cursor"],
        "config": {
            **{
                key: str(config[key]) if config.get(key) is not None else None
                for key in ("commission", "slippage_bps", "spread_bps", "participation")
            },
            "account": config.get("account") if isinstance(config.get("account"), str) else None,
        },
        "margin": MARGIN_RULES,
        "cash": str(state["cash"]),
        "realized": str(state.get("realized", "0.00")),
        "positions": [
            [symbol, position["quantity"], str(position["cost"])]
            for symbol, position in state["positions"].items()
        ],
        "orders": [_order(order) for order in state["orders"]],
        **extra,
    }


def _refuse(response):
    if "error" in response:
        raise DomainError(response["error"])
    return response


def _apply(state, response):
    """Write the engine's changes back into the stored run state."""
    orders = state["orders"]
    for index, fields in response["orders"]:
        order = orders[index]
        for key, value in fields:
            order[key] = value
    orders.extend(response["raised"])
    state["cursor"] = response["cursor"]
    if response["cash"] is not None:
        state["cash"] = response["cash"]
    if response["realized"] is not None:
        state["realized"] = response["realized"]
    positions = state["positions"]
    for symbol, quantity, cost in response["positions"]:
        position = positions.setdefault(symbol, {"quantity": 0, "cost": "0.00"})
        position["quantity"] = quantity
        position["cost"] = cost
    fills = []
    for item in response["fills"]:
        order = orders[item["order"]]
        fill = {
            "id": str(uuid4()),
            "order_id": order["id"],
            "symbol": order["symbol"],
            "side": order["side"],
            "quantity": item["quantity"],
            "price": item["price"],
            "fee": item["fee"],
            "realized": item["realized"],
            "time": item["time"],
            "note": order["note"],
            "lesson": order["lesson"],
        }
        fills.append(fill)
        state["fills"].append(fill)
    for entry in response["ledger"]:
        if "fill" not in entry:
            state["ledger"].append(entry)
            continue
        fill = fills[entry["fill"]]
        state["ledger"].append(
            {
                "id": fill["id"],
                "time": fill["time"],
                "type": "trade_fill",
                "description": f"{fill['side'].title()} {fill['quantity']} {fill['symbol']}",
                "amount": entry["amount"],
                "cash": entry["cash"],
            }
        )


def reservations(state, exclude=None):
    """Cash and shares already committed to working orders.

    Legs of one OCO group are alternatives, not additions: only one of them can
    ever fill, so the group reserves the largest of its legs rather than their
    sum. Excluding an order excludes its whole group.
    """
    response = engine.call(_request("reservations", state, exclude=exclude))
    return Decimal(response["cash"]), dict(response["shares"])


def validate_order(state, data, order, exclude=None):
    """Price the order's reservation and refuse it if the account cannot carry it."""
    index = next((i for i, other in enumerate(state["orders"]) if other is order), None)
    response = engine.call(
        _request(
            "validate", state, order=index if index is not None else _order(order), exclude=exclude
        ),
        data,
    )
    if "reserve_price" in response:
        order["reserve_price"] = response["reserve_price"]
    _refuse(response)


def validate_bracket(payload, mark):
    """An exit that cannot be right has to be refused before it is accepted.

    A take-profit below the market or a stop above it would trigger on the first
    bar and close the position the entry just opened, which reads as a bug rather
    than as the risk plan the learner wrote.
    """
    _refuse(
        engine.call(
            {
                "op": "bracket",
                "side": payload.side,
                "limit_price": _text(payload.limit_price),
                "stop_price": _text(payload.stop_price),
                "take_profit": _text(payload.take_profit),
                "stop_loss": _text(payload.stop_loss),
                "stop_loss_trail": _text(payload.stop_loss_trail),
                "mark": str(mark),
            }
        )
    )


def trailing_start(close, trail_percent):
    """The anchor and first stop of a trailing order placed at `close`.

    The trail starts from where the market is now, not from a high it reached
    before the order existed.
    """
    response = engine.call(
        {"op": "trailing", "close": str(close), "trail_percent": str(trail_percent)}
    )
    return response["trail_anchor"], response["stop_price"]


def advance_state(state, data, steps, scheduled=None, watch=()):
    """Advance the replay, optionally stopping at the first event it crosses.

    `scheduled` maps a bar to the reason the clock should stop there; the caller
    builds it from the run's own calendar, so a stop never depends on how much
    market has been generated. `watch` names the events detected as they happen.
    With neither, the clock runs the whole jump, as it always has.
    """
    response = _refuse(
        engine.call(
            _request(
                "advance",
                state,
                steps=steps,
                watch=sorted(watch),
                scheduled=sorted([bar, reason] for bar, reason in (scheduled or {}).items()),
            ),
            data,
        )
    )
    _apply(state, response)
    return response["stop"]


def retire_orphans(state):
    """Re-sweep every bracket, so an entry that ended takes its exits with it."""
    _apply(state, engine.call(_request("retire", state)))


def account(state, data):
    """Reserved and available cash, equity, exposure and every position's figures."""
    return _refuse(engine.call(_request("account", state), data))
