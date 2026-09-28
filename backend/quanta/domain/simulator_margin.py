"""Margin arithmetic for accounts allowed to sell short.

A cash account can only sell what it owns, and nothing in here applies to one.
A margin account may sell borrowed shares, which changes three things: cash is no
longer the constraint on buying, a position can carry a liability rather than an
asset, and a borrowed position costs something to keep open.

The rules used are the ordinary American ones, stated plainly so a learner can
check the arithmetic rather than take the number on trust: 50% of a new position
has to be covered by the account's own equity, the account is called if equity
falls under 30% of what it is carrying, and borrowed stock accrues a fee every
session it stays borrowed. Real borrow is quoted per name and moves daily; one
flat rate here keeps the cost visible without pretending to a precision the rest
of the simulation does not have.
"""

from decimal import ROUND_HALF_UP, Decimal

from quanta.domain.simulator import CENT, dec, money

INITIAL_MARGIN = Decimal("0.5")
MAINTENANCE_MARGIN = Decimal("0.3")
# 5% a year on the value of what is borrowed, accrued once a session.
BORROW_RATE = Decimal("0.05")
SESSIONS_A_YEAR = 252


def is_margin(state) -> bool:
    """Runs created before margin existed are cash accounts, as they were."""
    return state["config"].get("account") == "margin"


def marks(data, cursor):
    return {symbol: dec(rows[cursor]["close"]) for symbol, rows in data.items()}


def exposure(state, prices):
    """Account equity and the gross value of everything it is carrying.

    Gross counts a short at the value of the stock owed, not at minus that value:
    a $10,000 short is $10,000 of market risk in exactly the way a $10,000 long
    is, and netting them would say an account holding both has no risk at all.
    """
    equity = dec(state["cash"])
    gross = Decimal(0)
    for symbol, position in state["positions"].items():
        quantity = position["quantity"]
        if not quantity or symbol not in prices:
            continue
        value = prices[symbol] * quantity
        equity += value
        gross += abs(value)
    return equity, gross


def buying_power(state, prices):
    """What the account can still buy, at 50% initial margin.

    Twice equity, less what is already carried. A cash account is bounded by its
    cash instead, because short proceeds sitting in it are owed back and spending
    them would be spending someone else's stock.
    """
    equity, gross = exposure(state, prices)
    if not is_margin(state):
        return dec(state["cash"])
    return max(Decimal(0), equity * 2 - gross)


def shorts(state):
    return {
        symbol: position["quantity"]
        for symbol, position in state["positions"].items()
        if position["quantity"] < 0
    }


def borrow_fee(state, prices):
    """One session's cost of borrowing every short the account is carrying."""
    total = Decimal(0)
    for symbol, quantity in shorts(state).items():
        if symbol in prices:
            total += prices[symbol] * -quantity * BORROW_RATE / SESSIONS_A_YEAR
    return total.quantize(CENT, rounding=ROUND_HALF_UP)


def charge_borrow(state, prices, time):
    """Debit the session's borrow cost, as its own line in the ledger.

    It is a ledger entry rather than an adjustment to a position's cost, because
    it is a financing charge and not part of what the trade was worth. The ledger
    is also where the performance curve reads the cash path from.
    """
    fee = borrow_fee(state, prices)
    if fee <= 0:
        return None
    state["cash"] = money(dec(state["cash"]) - fee)
    entry = {
        "id": f"borrow:{state['cursor']}",
        "time": time,
        "type": "borrow_fee",
        "description": "Stock borrow fee on short positions",
        "amount": money(-fee),
        "cash": state["cash"],
    }
    state["ledger"].append(entry)
    return entry


def called(state, prices):
    """True when equity has fallen below the maintenance requirement.

    A flat or long-only account is never called here: without a short, the worst
    case is a position worth nothing, and nothing is owed to anyone.
    """
    if not is_margin(state) or not shorts(state):
        return False
    equity, gross = exposure(state, prices)
    return gross > 0 and equity < MAINTENANCE_MARGIN * gross
