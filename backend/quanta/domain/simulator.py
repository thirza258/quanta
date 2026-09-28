from datetime import datetime, timezone
from decimal import ROUND_CEILING, ROUND_DOWN, ROUND_HALF_UP, Decimal
from uuid import uuid4
from zoneinfo import ZoneInfo

from quanta.domain.errors import DomainError

OPEN = {"working", "partially_filled"}
# A bracket's exits exist from the moment the entry is placed, but they cannot
# trade until it fills — the shares they would sell do not exist yet. "held" is
# deliberately outside OPEN so nothing reserves against them meanwhile.
HELD = "held"
CENT = Decimal("0.01")


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


def reservations(state, exclude=None):
    """Cash and shares already committed to working orders.

    Legs of one OCO group are alternatives, not additions: only one of them can
    ever fill, so the group reserves the largest of its legs rather than their
    sum. Summing them would reject a perfectly fundable bracket.
    """
    cash = Decimal(0)
    shares = {}
    groups = {}
    for order in state["orders"]:
        if order["id"] == exclude or order["status"] not in OPEN:
            continue
        remaining = order["quantity"] - order["filled"]
        if order["side"] == "buy":
            cash += dec(order["reserve_price"]) * remaining + dec(order["fee_remaining"])
        else:
            key = (order["symbol"], group_of(order))
            groups[key] = max(groups.get(key, 0), remaining)
    for (symbol, _), remaining in groups.items():
        shares[symbol] = shares.get(symbol, 0) + remaining
    return cash, shares


def validate_order(state, data, order, exclude=None):
    mark = dec(bar_at(data, order["symbol"], state["cursor"])["close"])
    if order["kind"] in ("limit", "stop_limit") and not order.get("limit_price"):
        raise DomainError("A limit price is required.")
    if order["kind"] in ("stop", "stop_limit") and not order.get("stop_price"):
        raise DomainError("A stop trigger price is required.")
    if order["kind"] == "trailing_stop":
        if not order.get("trail_percent"):
            raise DomainError("A trailing stop needs a trail percentage.")
        if order["side"] != "sell":
            raise DomainError("This paper account trails stops on exits only.")
    elif order.get("trail_percent"):
        raise DomainError("Only a trailing stop accepts a trail percentage.")
    if order["kind"] not in ("limit", "stop_limit") and order.get("limit_price"):
        raise DomainError("This order type does not accept a limit price.")
    if order["kind"] not in ("stop", "stop_limit", "trailing_stop") and order.get("stop_price"):
        raise DomainError("This order type does not accept a stop price.")
    reserve_price = dec(order.get("limit_price") or max(mark, dec(order.get("stop_price") or mark)))
    if order["kind"] not in ("limit", "stop_limit"):
        reserve_price *= (
            1
            + (dec(state["config"]["slippage_bps"]) + dec(state["config"]["spread_bps"]) / 2)
            / 10000
        )
    reserve_price = reserve_price.quantize(CENT, rounding=ROUND_CEILING)
    order["reserve_price"] = money(reserve_price)
    cash, shares = reservations(state, exclude)
    remaining = order["quantity"] - order["filled"]
    if (
        order["side"] == "buy"
        and reserve_price * remaining + dec(order["fee_remaining"]) > dec(state["cash"]) - cash
    ):
        raise DomainError("Insufficient available cash, including fees and other working orders.")
    if order["side"] == "sell" and remaining > state["positions"].get(order["symbol"], {}).get(
        "quantity", 0
    ) - shares.get(order["symbol"], 0):
        raise DomainError("Insufficient available shares. This paper account is long-only.")


def validate_bracket(payload, mark):
    """An exit that cannot be right has to be refused before it is accepted.

    A take-profit below the market or a stop above it would trigger on the first
    bar and close the position the entry just opened, which reads as a bug rather
    than as the risk plan the learner wrote.
    """
    if payload.side != "buy":
        raise DomainError("Attached exits are available on entries, not on closing orders.")
    if payload.stop_loss and payload.stop_loss_trail:
        raise DomainError("A stop leg takes either a fixed price or a trail, not both.")
    reference = dec(payload.limit_price or payload.stop_price or mark)
    if payload.take_profit and dec(payload.take_profit) <= reference:
        raise DomainError("A take-profit has to sit above the entry it protects.")
    if payload.stop_loss and dec(payload.stop_loss) >= reference:
        raise DomainError("A stop-loss has to sit below the entry it protects.")


def trail(order, bar):
    """Ratchet a trailing stop, after this bar has been tested against the old one.

    The stop the learner is protected by on a bar is the one that was set before
    it opened. Moving the stop up on the same bar's high and then asking whether
    the low reached it would use a price from later in the bar to decide an exit
    earlier in it, which is look-ahead wearing a risk-management hat.
    """
    percent = dec(order["trail_percent"]) / 100
    anchor = max(dec(order.get("trail_anchor") or bar["close"]), dec(bar["high"]))
    order["trail_anchor"] = money(anchor)
    order["stop_price"] = money((anchor * (1 - percent)).quantize(CENT, rounding=ROUND_HALF_UP))


def execution_price(order, bar):
    buy = order["side"] == "buy"
    kind = order["kind"]
    opening, high, low = (dec(bar[key]) for key in ("open", "high", "low"))
    if kind == "trailing_stop":
        if not order["triggered"]:
            stop = dec(order["stop_price"])
            if low > stop:
                return None
            order["triggered"] = True
            return min(opening, stop)
        return opening
    if kind in ("stop", "stop_limit") and not order["triggered"]:
        stop = dec(order["stop_price"])
        if high < stop if buy else low > stop:
            return None
        order["triggered"] = True
        if kind == "stop_limit":
            # The intrabar path is unknown. Trigger now; earliest fill next bar.
            return None
        return max(opening, stop) if buy else min(opening, stop)
    if kind in ("limit", "stop_limit"):
        limit = dec(order["limit_price"])
        # A touch alone does not fill a passive order in this conservative bar model.
        if opening <= limit if buy else opening >= limit:
            return min(opening, limit) if buy else max(opening, limit)
        if low < limit if buy else high > limit:
            return limit
        return None
    return opening


def activate(state, parent):
    """Bring a filled entry's attached exits to life for the shares it bought.

    A child is sized to what the parent has actually filled, so a partial entry is
    protected for the part that exists and grows as the rest fills. It starts
    working on the next bar: the engine has no view inside a bar, so an exit that
    could trade on the same one would be trading on a price it never saw.
    """
    for child in state["orders"]:
        if child.get("parent_id") != parent["id"] or child["status"] not in (HELD, *OPEN):
            continue
        if not parent["filled"]:
            continue
        child["quantity"] = parent["filled"]
        if child["status"] == HELD:
            child.update(
                status="working",
                activates=state["cursor"] + 1,
                reason="Working: the entry it protects has filled.",
            )


def close_siblings(state, order):
    """One leg of an OCO group trading retires the others.

    Reducing rather than cancelling outright matters on a partial fill: the rest
    of the position is still open and still needs its other exit.
    """
    group = group_of(order)
    for other in state["orders"]:
        if other["id"] == order["id"] or group_of(other) != group:
            continue
        if other["status"] not in (HELD, *OPEN):
            continue
        remaining = other["quantity"] - order["filled"]
        if remaining <= other["filled"]:
            other.update(
                status="canceled",
                reason="Canceled: the other leg of this bracket filled.",
            )
        else:
            other["quantity"] = remaining
            other["reason"] = "Reduced: the other leg of this bracket filled in part."


def retire_orphans(state):
    """Cancel exits whose entry will never fill.

    A held leg is invisible to reservations and to the fill loop, so one left
    behind by a cancelled or expired entry would sit in the blotter for the rest
    of the run with nothing to protect.
    """
    parents = {order["id"]: order for order in state["orders"]}
    for order in state["orders"]:
        if order["status"] != HELD:
            continue
        parent = parents.get(order.get("parent_id") or "")
        if parent and parent["status"] not in OPEN and not parent["filled"]:
            order.update(
                status="canceled",
                reason=f"Canceled: the entry it was attached to was {parent['status']}.",
            )


def _sequence(state):
    """Orders in the sequence one bar should test them in.

    A stop leg goes before its take-profit sibling. When a bar's range covers
    both, the engine cannot know which came first, and the conservative reading —
    the one that does not flatter the learner — is that the stop went first.
    """
    return sorted(state["orders"], key=lambda order: 0 if order.get("role") == "stop" else 1)


def advance_state(state, data, steps):
    last = len(next(iter(data.values()))) - 1
    for _ in range(min(steps, last - state["cursor"])):
        state["cursor"] += 1
        used = {}
        for order in _sequence(state):
            if order["status"] not in OPEN:
                continue
            if order.get("activates") is not None and state["cursor"] < order["activates"]:
                continue
            bar = bar_at(data, order["symbol"], state["cursor"])
            day = (
                datetime.fromtimestamp(bar["time"], ZoneInfo("America/New_York")).date().isoformat()
            )
            if order["tif"] == "DAY" and order["day"] != day:
                order.update(status="expired", reason="DAY order expired at the session boundary.")
                continue
            price = execution_price(order, bar)
            if price is None:
                if order["kind"] == "trailing_stop":
                    trail(order, bar)
                continue
            friction = (
                dec(state["config"]["slippage_bps"]) + dec(state["config"]["spread_bps"]) / 2
            ) / 10000
            price *= 1 + friction if order["side"] == "buy" else 1 - friction
            if order["kind"] in ("limit", "stop_limit"):
                price = (
                    min(price, dec(order["limit_price"]))
                    if order["side"] == "buy"
                    else max(price, dec(order["limit_price"]))
                )
            price = max(CENT, dec(money(price)))
            capacity = int(dec(bar["volume"]) * dec(state["config"]["participation"]))
            quantity = min(
                order["quantity"] - order["filled"], max(0, capacity - used.get(order["symbol"], 0))
            )
            if not quantity:
                continue
            fee = dec(order["fee_remaining"])
            if order["side"] == "buy":
                reserved, _ = reservations(state, order["id"])
                affordable = max(
                    0,
                    int(
                        ((dec(state["cash"]) - reserved - fee) / price).to_integral_value(
                            rounding=ROUND_DOWN
                        )
                    ),
                )
                quantity = min(quantity, affordable)
                if quantity == 0:
                    order.update(
                        status="rejected", reason="The execution price gap exceeded available cash."
                    )
                    continue
            if order["side"] == "sell":
                reserved, _ = reservations(state, order["id"])
                if dec(state["cash"]) + price * quantity - fee < reserved:
                    order.update(
                        status="rejected",
                        reason="Sale proceeds and available cash cannot cover the commission.",
                    )
                    continue
            position = state["positions"].setdefault(
                order["symbol"], {"quantity": 0, "cost": "0.00"}
            )
            notional = price * quantity
            realized = Decimal(0)
            if order["side"] == "buy":
                change = -notional - fee
                position["quantity"] += quantity
                position["cost"] = money(dec(position["cost"]) + notional + fee)
            else:
                # All cost is allocated on the final exit so rounding cannot leave a residue.
                basis = (
                    dec(position["cost"])
                    if quantity == position["quantity"]
                    else dec(money(dec(position["cost"]) * quantity / position["quantity"]))
                )
                change = notional - fee
                realized = change - basis
                position["quantity"] -= quantity
                position["cost"] = money(dec(position["cost"]) - basis)
                state["realized"] = money(dec(state["realized"]) + realized)
            state["cash"] = money(dec(state["cash"]) + change)
            order["notional"] = money(dec(order["notional"]) + notional)
            order["filled"] += quantity
            order["average"] = money(dec(order["notional"]) / order["filled"])
            order["fee_remaining"] = "0.00"
            order["status"] = (
                "filled" if order["filled"] == order["quantity"] else "partially_filled"
            )
            order["reason"] = (
                "Filled on the next eligible bar, subject to shared volume participation."
            )
            used[order["symbol"]] = used.get(order["symbol"], 0) + quantity
            close_siblings(state, order)
            activate(state, order)
            fill = {
                "id": str(uuid4()),
                "order_id": order["id"],
                "symbol": order["symbol"],
                "side": order["side"],
                "quantity": quantity,
                "price": money(price),
                "fee": money(fee),
                "realized": money(realized),
                "time": bar["time"],
                "note": order["note"],
                "lesson": order["lesson"],
            }
            state["fills"].append(fill)
            state["ledger"].append(
                {
                    "id": fill["id"],
                    "time": bar["time"],
                    "type": "trade_fill",
                    "description": f"{order['side'].title()} {quantity} {order['symbol']}",
                    "amount": money(change),
                    "cash": state["cash"],
                }
            )
            # Reserve the remaining quantity at the current estimate; close if no longer affordable.
            if order["status"] in OPEN:
                try:
                    validate_order(state, data, order, order["id"])
                except DomainError:
                    order.update(
                        status="canceled",
                        reason="Remaining quantity canceled: insufficient buying power after the gap fill.",
                    )
    retire_orphans(state)
    # At a session's last known bar, DAY orders cannot remain working overnight.
    cursor = state["cursor"]
    for order in state["orders"]:
        if order["status"] in OPEN and order["tif"] == "DAY":
            rows = data[order["symbol"]]
            if (
                cursor == last
                or datetime.fromtimestamp(rows[cursor]["time"], ZoneInfo("America/New_York")).date()
                != datetime.fromtimestamp(
                    rows[cursor + 1]["time"], ZoneInfo("America/New_York")
                ).date()
            ):
                order.update(
                    status="expired", reason="DAY order expired at the end of its session."
                )
    retire_orphans(state)
