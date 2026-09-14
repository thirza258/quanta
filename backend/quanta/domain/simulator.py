from datetime import datetime, timezone
from decimal import ROUND_CEILING, ROUND_DOWN, ROUND_HALF_UP, Decimal
from uuid import uuid4
from zoneinfo import ZoneInfo

from quanta.domain.errors import DomainError

OPEN = {"working", "partially_filled"}
CENT = Decimal("0.01")


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
    cash = Decimal(0)
    shares = {}
    for order in state["orders"]:
        if order["id"] == exclude or order["status"] not in OPEN:
            continue
        remaining = order["quantity"] - order["filled"]
        if order["side"] == "buy":
            cash += dec(order["reserve_price"]) * remaining + dec(order["fee_remaining"])
        else:
            shares[order["symbol"]] = shares.get(order["symbol"], 0) + remaining
    return cash, shares


def validate_order(state, data, order, exclude=None):
    mark = dec(bar_at(data, order["symbol"], state["cursor"])["close"])
    if order["kind"] in ("limit", "stop_limit") and not order.get("limit_price"):
        raise DomainError("A limit price is required.")
    if order["kind"] in ("stop", "stop_limit") and not order.get("stop_price"):
        raise DomainError("A stop trigger price is required.")
    if order["kind"] not in ("limit", "stop_limit") and order.get("limit_price"):
        raise DomainError("This order type does not accept a limit price.")
    if order["kind"] not in ("stop", "stop_limit") and order.get("stop_price"):
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


def execution_price(order, bar):
    buy = order["side"] == "buy"
    kind = order["kind"]
    opening, high, low = (dec(bar[key]) for key in ("open", "high", "low"))
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


def advance_state(state, data, steps):
    last = len(next(iter(data.values()))) - 1
    for _ in range(min(steps, last - state["cursor"])):
        state["cursor"] += 1
        used = {}
        for order in state["orders"]:
            if order["status"] not in OPEN:
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
