"""The declared shape of an experiment: what is tested, on what, and how hard."""

from __future__ import annotations

import ast
import math
from itertools import product
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from quanta.domain.analytics import DatasetParams

MAX_PARAMETERS = 3
MAX_VALUES = 12
MAX_CONFIGURATIONS = 60

DEFAULT_CODE = """def strategy(data, params):
    # Trend rule: hold while the fast average is above the slow one.
    fast = sma(data["close"], params["fast"])
    slow = sma(data["close"], params["slow"])
    return fast > slow
"""

# Trailing-window helpers the guided runtime provides (execution/sandbox_worker.py).
INDICATORS = (
    ("sma", "sma(series, n)", "Mean of the last n values."),
    ("ema", "ema(series, n)", "Exponential average with weight 2 / (n + 1)."),
    ("highest", "highest(series, n)", "Highest of the last n values."),
    ("lowest", "lowest(series, n)", "Lowest of the last n values."),
    ("change", "change(series, n)", "Return over the last n bars: x / x[n bars ago] − 1."),
    ("shift", "shift(series, n)", "The value n bars ago (n ≥ 0; negative lags are refused)."),
    ("stdev", "stdev(series, n)", "Population standard deviation of the last n values."),
    ("zscore", "zscore(series, n)", "(x − sma) / stdev over the last n values; 0 when flat."),
)

TEMPLATES = (
    {
        "id": "trend",
        "label": "Moving-average crossover",
        "description": "Hold while a fast average is above a slow one.",
        "code": DEFAULT_CODE,
        "parameters": [
            {"name": "fast", "values": [10, 20, 30, 50]},
            {"name": "slow", "values": [100, 150, 200]},
        ],
        "base": {"fast": 20, "slow": 150},
    },
    {
        "id": "momentum",
        "label": "Time-series momentum",
        "description": "Hold while the trailing return beats a threshold.",
        "code": """def strategy(data, params):
    # Hold while the return over the lookback beats the threshold.
    return change(data["close"], params["lookback"]) > params["threshold"]
""",
        "parameters": [
            {"name": "lookback", "values": [21, 63, 126, 189, 252]},
            {"name": "threshold", "values": [0, 0.02, 0.05]},
        ],
        "base": {"lookback": 126, "threshold": 0},
    },
    {
        "id": "reversion",
        "label": "Z-score mean reversion",
        "description": "Hold while price is stretched below its trailing mean.",
        "code": """def strategy(data, params):
    # Hold while the close sits more than `entry` deviations below its mean.
    return zscore(data["close"], params["window"]) < -params["entry"]
""",
        "parameters": [
            {"name": "window", "values": [10, 20, 40, 60]},
            {"name": "entry", "values": [0.5, 1, 1.5, 2]},
        ],
        "base": {"window": 20, "entry": 1},
    },
    {
        "id": "channel",
        "label": "Donchian channel midline",
        "description": "Hold while the close is above the middle of its trailing range.",
        "code": """def strategy(data, params):
    # Hold while the close is above the midpoint of the trailing high-low channel.
    top = highest(data["high"], params["lookback"])
    bottom = lowest(data["low"], params["lookback"])
    return data["close"] > (top + bottom) / 2
""",
        "parameters": [{"name": "lookback", "values": [20, 40, 60, 100, 150]}],
        "base": {"lookback": 60},
    },
)


class GridParameter(BaseModel):
    name: str = Field(pattern=r"^[a-z][a-z0-9_]{0,23}$")
    values: list[int | float] = Field(min_length=1, max_length=MAX_VALUES)

    @field_validator("values")
    @classmethod
    def finite_distinct(cls, values):
        if any(not math.isfinite(v) or abs(v) > 1e6 for v in values):
            raise ValueError("Parameter values must be finite numbers within ±1,000,000.")
        if len(set(values)) != len(values):
            raise ValueError("Parameter values must be distinct.")
        return values


class StrategySpec(BaseModel):
    name: str = Field("Trend rule", min_length=1, max_length=80)
    code: str = Field(DEFAULT_CODE, min_length=1, max_length=20000)
    parameters: list[GridParameter] = Field(
        default_factory=lambda: [
            GridParameter(name="fast", values=[10, 20, 30, 50]),
            GridParameter(name="slow", values=[100, 150, 200]),
        ],
        max_length=MAX_PARAMETERS,
    )
    base: dict[str, int | float] = Field(default_factory=lambda: {"fast": 20, "slow": 150})

    @model_validator(mode="before")
    @classmethod
    def base_follows_grid(cls, data):
        # The default base names the default grid's parameters. A caller who sends
        # their own grid without a base gets each parameter's middle value instead.
        if isinstance(data, dict) and "parameters" in data and "base" not in data:
            return {**data, "base": {}}
        return data

    @model_validator(mode="after")
    def coherent_grid(self):
        names = [p.name for p in self.parameters]
        if len(set(names)) != len(names):
            raise ValueError("Parameter names must be distinct.")
        unknown = set(self.base) - set(names)
        if unknown:
            raise ValueError(f"Base values name unknown parameters: {', '.join(sorted(unknown))}.")
        base = {}
        for parameter in self.parameters:
            # Default to the middle of the declared values so the base is a grid point.
            value = self.base.get(parameter.name, parameter.values[len(parameter.values) // 2])
            if value not in parameter.values:
                raise ValueError(
                    f"The base value of {parameter.name} must be one of its grid values."
                )
            base[parameter.name] = parameter.values[parameter.values.index(value)]
        self.base = base
        if configuration_count(self.parameters) > MAX_CONFIGURATIONS:
            raise ValueError(
                f"The grid has {configuration_count(self.parameters)} configurations; "
                f"the limit is {MAX_CONFIGURATIONS}."
            )
        return self


class CostSpec(BaseModel):
    capital: float = Field(100000, ge=100, le=1e9, allow_inf_nan=False)
    commission_bps: float = Field(5, ge=0, le=500, allow_inf_nan=False)
    slippage_bps: float = Field(3, ge=0, le=500, allow_inf_nan=False)


class ValidationSpec(BaseModel):
    split: float = Field(0.7, ge=0.5, le=0.9, allow_inf_nan=False)
    walk_forward: bool = True
    train_bars: int = Field(252, ge=126, le=5040)
    test_bars: int = Field(126, ge=63, le=2520)
    anchored: bool = False
    permutations: int = Field(200, ge=0, le=500)
    seed_paths: int = Field(5, ge=0, le=10)


class DatasetSpec(BaseModel):
    kind: Literal["synthetic", "historical"] = "synthetic"
    params: DatasetParams = Field(default_factory=DatasetParams)

    @model_validator(mode="after")
    def historical_symbol(self):
        if self.kind == "historical" and not self.params.symbol:
            raise ValueError("Choose an imported dataset symbol for historical data.")
        return self


class ExperimentSpec(BaseModel):
    dataset: DatasetSpec = Field(default_factory=DatasetSpec)
    strategy: StrategySpec = Field(default_factory=StrategySpec)
    costs: CostSpec = Field(default_factory=CostSpec)
    validation: ValidationSpec = Field(default_factory=ValidationSpec)


def configuration_count(parameters: list[GridParameter]) -> int:
    count = 1
    for parameter in parameters:
        count *= len(parameter.values)
    return count


def expand_grid(parameters: list[GridParameter]) -> list[dict]:
    """Every configuration in row-major order: the last parameter varies fastest."""
    if not parameters:
        return [{}]
    names = [p.name for p in parameters]
    return [dict(zip(names, combo)) for combo in product(*(p.values for p in parameters))]


def grid_shape(parameters: list[GridParameter]) -> list[int]:
    return [len(p.values) for p in parameters]


def referenced_parameters(code: str) -> list[str]:
    """Parameter names subscripted on strategy's second argument: params['name']."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "strategy":
            if len(node.args.args) < 2:
                return []
            param_name = node.args.args[1].arg
            refs = []
            for child in ast.walk(node):
                if isinstance(child, ast.Subscript):
                    if (
                        isinstance(child.value, ast.Name)
                        and child.value.id == param_name
                        and isinstance(child.slice, ast.Constant)
                        and isinstance(child.slice.value, str)
                    ):
                        if child.slice.value not in refs:
                            refs.append(child.slice.value)
            return refs
    return []
