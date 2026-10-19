from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StrictInt


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RunCreate(Model):
    id: UUID
    mode: Literal["synthetic", "historical"] = "synthetic"
    # Omitted: derived from the run identifier so every new account differs.
    seed: StrictInt | None = Field(default=None, ge=0, le=1000000)
    # A lesson-linked practice mission. It fixes the market so everyone attempting
    # the same mission meets the same one.
    mission: str | None = Field(default=None, max_length=40)
    # A cash account can only sell what it owns. A margin account can borrow
    # stock to sell, and pays for the privilege. Runs made before this existed
    # are cash accounts, which is what they always were.
    account: Literal["cash", "margin"] = "cash"
    symbol: str | None = Field(default=None, max_length=20)
    commission: Decimal = Field(default=Decimal("1"), ge=0, le=100, decimal_places=2)
    slippage_bps: Decimal = Field(default=Decimal("2"), ge=0, le=100)
    spread_bps: Decimal = Field(default=Decimal("2"), ge=0, le=100)
    participation: Decimal = Field(default=Decimal("0.01"), gt=0, le=1)


class Mutation(Model):
    id: UUID
    version: StrictInt = Field(ge=0)


class OrderCreate(Mutation):
    symbol: str = Field(max_length=20)
    side: Literal["buy", "sell"]
    kind: Literal["market", "limit", "stop", "stop_limit", "trailing_stop"] = "market"
    quantity: StrictInt = Field(gt=0, le=1000000)
    limit_price: Decimal | None = Field(default=None, gt=0, le=100000000, decimal_places=2)
    stop_price: Decimal | None = Field(default=None, gt=0, le=100000000, decimal_places=2)
    # A trailing stop follows the best price reached since it started working,
    # by a percentage rather than a fixed amount, so the same order behaves the
    # same way on a $9 stock and a $900 one.
    trail_percent: Decimal | None = Field(default=None, gt=0, le=50, decimal_places=2)
    # An exit attached to an entry. Both legs are created with the entry and
    # wait, held, until it fills; whichever triggers first cancels the other.
    take_profit: Decimal | None = Field(default=None, gt=0, le=100000000, decimal_places=2)
    stop_loss: Decimal | None = Field(default=None, gt=0, le=100000000, decimal_places=2)
    stop_loss_trail: Decimal | None = Field(default=None, gt=0, le=50, decimal_places=2)
    tif: Literal["DAY", "GTC"] = "GTC"
    note: str = Field(default="", max_length=2000)
    lesson: str = Field(default="", max_length=40)


class Advance(Mutation):
    # Up to five modeled sessions, so a learner can step a minute or jump a week
    # to see how a position behaves after a headline or a reported quarter.
    steps: StrictInt = Field(default=1, ge=1, le=1950)
    # Events that cut a jump short so the learner has to decide something while
    # the position is open. An empty list keeps the clock running to the end.
    stop_on: list[
        Literal["fill", "bracket", "margin_call", "earnings", "news"]
    ] = Field(default_factory=list, max_length=5)


class Amendment(Mutation):
    limit_price: Decimal | None = Field(default=None, gt=0, le=100000000, decimal_places=2)
    stop_price: Decimal | None = Field(default=None, gt=0, le=100000000, decimal_places=2)


class Preferences(Mutation):
    preferences: dict


class Decision(Mutation):
    # What the learner chose to do when the clock stopped, and why.
    choice: Literal["hold", "traded"]
    note: str = Field(default="", max_length=2000)


class Journal(Mutation):
    note: str = Field(max_length=2000)
    lesson: str = Field(default="", max_length=40)
