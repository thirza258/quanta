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

    Excluding an order excludes its whole group. Re-validating one leg while its
    sibling still reserves the same shares would cancel a bracket for lacking the
    very shares it is holding.
    """
    excluded = set()
    if exclude:
        excluded.add(exclude)
        target = next((o for o in state["orders"] if o["id"] == exclude), None)
        group = target.get("oco_group") if target else None
        if group:
            excluded |= {o["id"] for o in state["orders"] if o.get("oco_group") == group}
    cash = Decimal(0)
    shares = {}
    groups = {}
    prices = {}
    buys = {}
    for order in state["orders"]:
        if order["id"] in excluded or order["status"] not in OPEN:
            continue
        remaining = order["quantity"] - order["filled"]
        if order["side"] == "buy":
            # The commission is owed either way; the stock itself may not be.
            cash += dec(order["fee_remaining"])
            buys.setdefault(order["symbol"], []).append(
                (dec(order["reserve_price"]), remaining)
            )
        else:
            key = (order["symbol"], group_of(order))
            groups[key] = max(groups.get(key, 0), remaining)
            prices[order["symbol"]] = dec(order["reserve_price"])
    for symbol, legs in buys.items():
        # Buying back borrowed stock returns something the account already owes.
        # It commits no new capital, so it reserves none: a short that has moved
        # against the account must stay closable at the moment that matters most.
        owed = max(0, -state["positions"].get(symbol, {}).get("quantity", 0))
        for price, remaining in legs:
            covering = min(remaining, owed)
            owed -= covering
            cash += price * (remaining - covering)
    for (symbol, _), remaining in groups.items():
        # Only the part of a sale covered by stock already held reserves stock.
        # The rest is borrowed, and a borrowed position consumes buying power at
        # its full value, exactly as a purchase of the same size does.
        held = max(0, state["positions"].get(symbol, {}).get("quantity", 0))
        covered = min(remaining, max(0, held - shares.get(symbol, 0)))
        shares[symbol] = shares.get(symbol, 0) + covered
        borrowed = remaining - covered
        if borrowed:
            cash += prices[symbol] * borrowed
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
    margin = state["config"].get("account") == "margin"
    # A cash account can spend its cash. A margin account can spend its buying
    # power, which is not the same number: short proceeds are sitting in the cash
    # balance and are owed back, so cash overstates what is actually available.
    if margin:
        from quanta.domain.simulator_margin import buying_power, marks

        capacity = buying_power(state, marks(data, state["cursor"]))
    else:
        capacity = dec(state["cash"])
    held = state["positions"].get(order["symbol"], {}).get("quantity", 0)
    if order["side"] == "buy":
        queued = sum(
            other["quantity"] - other["filled"]
            for other in state["orders"]
            if other["id"] != order["id"]
            and other["side"] == "buy"
            and other["symbol"] == order["symbol"]
            and other["status"] in OPEN
        )
        # Returning borrowed stock is not a purchase of anything the account does
        # not already owe, so that part of the order needs no buying power.
        covering = min(remaining, max(0, -held - queued))
        opening = remaining - covering
        if reserve_price * opening + dec(order["fee_remaining"]) > capacity - cash:
            raise DomainError(
                "Insufficient buying power, including fees and other working orders."
                if margin
                else "Insufficient available cash, including fees and other working orders."
            )
        return
    available = max(0, held) - shares.get(order["symbol"], 0)
    borrowed = remaining - available
    if borrowed <= 0:
        return
    if not margin:
        raise DomainError("Insufficient available shares. This paper account is long-only.")
    # A short consumes buying power at the full value of the stock borrowed. The
    # 50% initial requirement is already what makes buying power twice equity;
    # applying it again here would let a short run at four times equity while a
    # purchase of the same size is held to two.
    if reserve_price * borrowed + dec(order["fee_remaining"]) > capacity - cash:
        raise DomainError(
            "Insufficient margin to borrow this stock, including other working orders."
        )


def validate_bracket(payload, mark):
    """An exit that cannot be right has to be refused before it is accepted.

    A take-profit below the market or a stop above it would trigger on the first
    bar and close the position the entry just opened, which reads as a bug rather
    than as the risk plan the learner wrote.
    """
    if payload.side != "buy":
        raise DomainError(
            "Attached exits are available on buy entries. A short entry cannot carry "
            "them yet; place its stop as a separate order."
        )
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


def arm(leg, parent, cursor):
    """Bring a held exit to life, on the bar after the entry it protects filled.

    The engine has no view inside a bar, so an exit that could trade on the same
    one would be trading on a price it never saw. A trailing leg takes its anchor
    from what the entry actually paid, once: a later fill on the same entry must
    not reset a stop that has already ratcheted up.
    """
    leg.update(
        status="working",
        activates=cursor + 1,
        reason="Working: the entry it protects has filled.",
    )
    if leg["kind"] == "trailing_stop" and not leg.get("trail_anchor"):
        anchor = dec(parent["average"])
        leg["trail_anchor"] = money(anchor)
        leg["stop_price"] = money(
            (anchor * (1 - dec(leg["trail_percent"]) / 100)).quantize(
                CENT, rounding=ROUND_HALF_UP
            )
        )


def rebalance(state, order, cursor):
    """Size a bracket's exits to the shares its entry is actually holding open.

    Recomputed from the whole group rather than stepped: an entry still filling,
    a leg that filled in part and a sibling that filled after it all move the same
    number, and adjusting each of them separately double-counts it.

    This is also what makes the group one-cancels-other. A leg that trades reduces
    what is left open, and its siblings shrink to match; when nothing is left open
    and the entry is done, they are cancelled. While the entry is still working
    they idle instead, because more shares are coming and will need protecting.
    """
    parent_id = order.get("parent_id") or order["id"]
    parent = next((o for o in state["orders"] if o["id"] == parent_id), None)
    legs = [o for o in state["orders"] if o.get("parent_id") == parent_id]
    if not parent or not legs:
        return
    still_open = parent["filled"] - sum(leg["filled"] for leg in legs)
    for leg in legs:
        if leg["status"] not in (HELD, *OPEN):
            continue
        if still_open > 0:
            leg["quantity"] = leg["filled"] + still_open
            if leg["status"] == HELD:
                arm(leg, parent, cursor)
        elif parent["status"] in OPEN:
            # Flat for now, but the entry is still working. Hold the leg at what
            # it has already done, so it reserves nothing and cannot trade, and
            # let it grow again when the rest of the entry arrives.
            leg["quantity"] = leg["filled"]
            leg["reason"] = "Idle: waiting for the rest of the entry to fill."
        else:
            leg.update(
                status="canceled",
                reason="Canceled: this bracket has nothing left to protect."
                if parent["filled"]
                else f"Canceled: the entry it was attached to was {parent['status']}.",
            )


def retire_orphans(state):
    """Re-sweep every bracket, so an entry that ended takes its exits with it.

    A held leg is invisible to reservations and to the fill loop, so one left
    behind by a cancelled or expired entry would sit in the blotter for the rest
    of the run with nothing to protect.
    """
    for parent_id in {o["parent_id"] for o in state["orders"] if o.get("parent_id")}:
        parent = next((o for o in state["orders"] if o["id"] == parent_id), None)
        if parent:
            rebalance(state, parent, state["cursor"])


def _sequence(state):
    """Orders in the sequence one bar should test them in.

    A stop leg goes before its take-profit sibling. When a bar's range covers
    both, the engine cannot know which came first, and the conservative reading —
    the one that does not flatter the learner — is that the stop went first.
    """
    return sorted(state["orders"], key=lambda order: 0 if order.get("role") == "stop" else 1)


def session_end(data, cursor):
    """True when the next bar belongs to a different session than this one."""
    rows = next(iter(data.values()))
    if cursor + 1 >= len(rows):
        return True
    zone = ZoneInfo("America/New_York")
    return (
        datetime.fromtimestamp(rows[cursor]["time"], zone).date()
        != datetime.fromtimestamp(rows[cursor + 1]["time"], zone).date()
    )


def buy_in(state, data, symbol, quantity, reason):
    """A market order the account did not ask for, to close a called position.

    It is an order rather than an instant adjustment so it queues, respects the
    same volume participation as everything else, and appears in the blotter with
    the reason it exists. A broker closing a position does not get a better fill
    than the learner would have.
    """
    bar = bar_at(data, symbol, state["cursor"])
    state["orders"].append(
        {
            "id": f"buyin:{symbol}:{state['cursor']}",
            "symbol": symbol,
            "side": "buy",
            "kind": "market",
            "quantity": quantity,
            "limit_price": None,
            "stop_price": None,
            "trail_percent": None,
            "tif": "GTC",
            "filled": 0,
            "status": "working",
            "average": "0.00",
            "notional": "0.00",
            "fee_remaining": money(state["config"]["commission"]),
            "reserve_price": money(bar["close"] * 2),
            "triggered": False,
            "forced": True,
            "activates": state["cursor"] + 1,
            "time": bar["time"],
            "day": datetime.fromtimestamp(bar["time"], ZoneInfo("America/New_York"))
            .date()
            .isoformat(),
            "note": "",
            "lesson": "",
            "reason": reason,
        }
    )


def settle_margin(state, data):
    """End-of-session financing and the maintenance check, in that order.

    The borrow is charged first, because it is one of the things that can push an
    account under its requirement, and an account should be called on the balance
    it actually has rather than on the one it had before it paid its bills.
    """
    from quanta.domain.simulator_margin import MAINTENANCE_MARGIN, called, charge_borrow, marks

    if state["config"].get("account") != "margin":
        return
    cursor = state["cursor"]
    prices = marks(data, cursor)
    if session_end(data, cursor):
        charge_borrow(state, prices, bar_at(data, next(iter(data)), cursor)["time"])
    if not called(state, prices):
        return
    percent = int(MAINTENANCE_MARGIN * 100)
    for symbol, quantity in list(
        (s, p["quantity"]) for s, p in state["positions"].items() if p["quantity"] < 0
    ):
        pending = sum(
            o["quantity"] - o["filled"]
            for o in state["orders"]
            if o.get("forced") and o["symbol"] == symbol and o["status"] in OPEN
        )
        outstanding = -quantity - pending
        if outstanding > 0:
            buy_in(
                state,
                data,
                symbol,
                outstanding,
                f"Bought in: account equity fell under the {percent}% maintenance "
                "requirement on its borrowed stock.",
            )


def capital(state, data):
    """What the account can put behind a purchase on this bar."""
    if state["config"].get("account") != "margin":
        return dec(state["cash"])
    from quanta.domain.simulator_margin import buying_power, marks

    return buying_power(state, marks(data, state["cursor"]))


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
            held = state["positions"].get(order["symbol"], {}).get("quantity", 0)
            if order["side"] == "buy":
                reserved, _ = reservations(state, order["id"])
                # Buying back borrowed stock is never refused for cash. A short
                # that gapped against the account has to be closable, and the
                # balance going negative is the debt the margin call answers.
                covering = max(0, min(quantity, -held))
                funds = capital(state, data) - reserved - fee
                # Covering shares cost no buying power, so they are not counted
                # against it; only what the order opens beyond the short is.
                opening = (
                    int((funds / price).to_integral_value(rounding=ROUND_DOWN))
                    if funds > 0
                    else 0
                )
                quantity = min(quantity, covering + max(0, opening))
                if quantity == 0:
                    order.update(
                        status="rejected",
                        reason="The execution price gap exceeded available buying power."
                        if order.get("forced")
                        else "The execution price gap exceeded available cash.",
                    )
                    continue
            if (
                order["side"] == "sell"
                and held >= quantity
                and state["config"].get("account") != "margin"
            ):
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
            # Cost is signed: what a long paid, or minus what a short was paid.
            # One sign convention makes `value - cost` the unrealized result and
            # `proceeds - basis` the realized one in both directions, instead of
            # two mirrored branches that have to be kept in agreement.
            held, cost = position["quantity"], dec(position["cost"])
            direction = 1 if order["side"] == "buy" else -1
            flow = -price if order["side"] == "buy" else price
            # A fill can close one position and open the opposite one. Selling 30
            # while long 10 realizes a result on those 10 and shorts 20; treating
            # it as one or the other misstates both.
            closing = min(quantity, abs(held)) if held and (held > 0) != (direction > 0) else 0
            opening = quantity - closing
            realized = Decimal(0)
            if closing:
                # All cost is allocated on the final exit so rounding cannot leave a residue.
                basis = (
                    cost
                    if closing == abs(held)
                    else dec(money(cost * closing / abs(held)))
                )
                realized = flow * closing - basis - fee
                cost -= basis
                held += direction * closing
                state["realized"] = money(dec(state["realized"]) + realized)
            if opening:
                # Opening carries the fee only when no closing leg already did.
                cost += -flow * opening + (fee if not closing else Decimal(0))
                held += direction * opening
            position["quantity"] = held
            position["cost"] = money(cost)
            notional = price * quantity
            change = flow * quantity - fee
            state["cash"] = money(dec(state["cash"]) + change)
            order["notional"] = money(dec(order["notional"]) + notional)
            order["filled"] += quantity
            order["average"] = money(dec(order["notional"]) / order["filled"])
            order["fee_remaining"] = "0.00"
            order["status"] = (
                "filled" if order["filled"] == order["quantity"] else "partially_filled"
            )
            if not order.get("forced"):
                # A buy-in keeps the reason it was raised for; it is the only
                # record of why the account bought something it never asked for.
                order["reason"] = (
                    "Filled on the next eligible bar, subject to shared volume participation."
                )
            used[order["symbol"]] = used.get(order["symbol"], 0) + quantity
            # An entry that filled arms its exits; an exit that filled resizes
            # its siblings. Both are the same recomputation over the group.
            rebalance(state, order, state["cursor"])
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
            if order["status"] in OPEN and not order.get("forced"):
                try:
                    validate_order(state, data, order, order["id"])
                except DomainError:
                    order.update(
                        status="canceled",
                        reason="Remaining quantity canceled: insufficient buying power after the gap fill.",
                    )
        settle_margin(state, data)
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
