"""Margin rules for accounts allowed to sell short.

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

The engine (backend/engine/src/engine.cpp) applies them; these constants are the
values it is handed with every request. Buying power is twice equity less gross
exposure, which is what the 50% initial requirement means.
"""

from decimal import Decimal

INITIAL_MARGIN = Decimal("0.5")
MAINTENANCE_MARGIN = Decimal("0.3")
# 5% a year on the value of what is borrowed, accrued once a session.
BORROW_RATE = Decimal("0.05")
SESSIONS_A_YEAR = 252


def is_margin(state) -> bool:
    """Runs created before margin existed are cash accounts, as they were."""
    return state["config"].get("account") == "margin"
