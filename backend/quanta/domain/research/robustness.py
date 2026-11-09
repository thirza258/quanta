"""Parameter surfaces, transaction-cost stress and alternative synthetic paths."""

from __future__ import annotations

import math
import statistics

import numpy as np

from quanta.domain.research.metrics import evaluate, sharpe_of
from quanta.domain.research.validation import subset

COST_LEVELS = (0, 2, 5, 10, 15, 20, 30, 40, 50, 75, 100)
BREAK_EVEN_CEILING = 1000.0
ROBUST, SENSITIVE = 70, 40


def neighbors(index: int, shape: list[int]) -> list[int]:
    """Grid points one step away along exactly one parameter (row-major order)."""
    if not shape:
        return []
    coords = list(np.unravel_index(index, shape))
    out = []
    for axis, size in enumerate(shape):
        for step in (-1, 1):
            moved = coords[axis] + step
            if 0 <= moved < size:
                point = coords.copy()
                point[axis] = moved
                out.append(int(np.ravel_multi_index(point, shape)))
    return out


def stability(center: int, metrics: list[dict], shape: list[int]) -> dict:
    """Median share of the centre's Sharpe that its neighbours keep, as 0-100.

    A ratio is clipped to [0, 1]: a better neighbour cannot make the centre
    more robust than a plateau, and a losing one counts as keeping nothing.
    """
    around = neighbors(center, shape)
    sharpe = metrics[center].get("sharpe")
    if not around:
        return {
            "score": None,
            "class": "untested",
            "neighbors": 0,
            "reason": "Only one configuration was tested, so sensitivity is unknown.",
        }
    if sharpe is None or sharpe <= 0:
        return {
            "score": None,
            "class": "no-edge",
            "neighbors": len(around),
            "reason": "The configuration has no positive Sharpe ratio to be robust about.",
        }
    kept = [min(1.0, max(0.0, (metrics[i].get("sharpe") or 0.0) / sharpe)) for i in around]
    score = round(100 * statistics.median(kept))
    return {
        "score": score,
        "class": "robust" if score >= ROBUST else "sensitive" if score >= SENSITIVE else "fragile",
        "neighbors": len(around),
        "reason": f"Neighbouring configurations keep a median {score}% of its Sharpe ratio.",
    }


def surface(configs, metrics, parameters, base_index) -> dict:
    shape = [len(p.values) for p in parameters]
    n = len(configs)
    order = sorted(range(n), key=lambda i: (-sharpe_of(metrics[i]), i))
    defined = [m["sharpe"] for m in metrics if m.get("sharpe") is not None]
    influence = []
    for axis, parameter in enumerate(parameters):
        means = []
        for value in parameter.values:
            group = [
                metrics[i]["sharpe"]
                for i, config in enumerate(configs)
                if config[parameter.name] == value and metrics[i].get("sharpe") is not None
            ]
            means.append(statistics.fmean(group) if group else None)
        present = [m for m in means if m is not None]
        influence.append(
            {
                "name": parameter.name,
                "values": parameter.values,
                "mean_sharpe": means,
                "spread": max(present) - min(present) if len(present) > 1 else 0.0,
            }
        )
    influence.sort(key=lambda item: -item["spread"])
    return {
        "configurations": n,
        "parameters": [{"name": p.name, "values": p.values} for p in parameters],
        "points": [{"index": i, "params": configs[i], **subset(metrics[i])} for i in range(n)],
        "base": base_index,
        "best": order[0],
        "median": order[n // 2],
        "worst": order[-1],
        "base_rank": order.index(base_index) + 1,
        "positive_share": sum(1 for s in defined if s > 0) / n,
        "sharpe_distribution": {
            "min": min(defined) if defined else None,
            "median": statistics.median(defined) if defined else None,
            "max": max(defined) if defined else None,
            "std": statistics.stdev(defined) if len(defined) > 1 else None,
        },
        "influence": influence,
        "stability": stability(base_index, metrics, shape),
        "best_stability": stability(order[0], metrics, shape),
    }


def cost_weights(costs) -> tuple[float, float]:
    total = costs.commission_bps + costs.slippage_bps
    if total <= 0:
        return 0.5, 0.5
    return costs.commission_bps / total, costs.slippage_bps / total


def at_cost(bars, signals, costs, level):
    commission, slippage = cost_weights(costs)
    return evaluate(
        bars, signals, costs, commission_bps=level * commission, slippage_bps=level * slippage
    )["metrics"]


def cost_stress(bars, signals, costs) -> dict:
    """Sharpe and returns as the one-way cost rises, and the cost where Sharpe reaches zero.

    Each level sets commission plus slippage to that many basis points per
    fill, split in the proportion the experiment configured. Sharpe is excess
    of the 3% risk-free rate, so break-even is the cost at which the strategy
    stops beating cash.
    """
    levels, trades = [], 0
    for level in COST_LEVELS:
        metrics = at_cost(bars, signals, costs, level)
        if level == 0:
            trades = metrics["trades"]
        levels.append(
            {
                "cost_bps": level,
                "sharpe": metrics["sharpe"],
                "cagr": metrics["cagr"],
                "total_return": metrics["total_return"],
                "final_equity": metrics["final_equity"],
            }
        )
    current = costs.commission_bps + costs.slippage_bps
    out = {"levels": levels, "current_bps": current, "break_even_bps": None}
    zero = levels[0]["sharpe"]
    if trades == 0:
        out["reason"] = "The strategy never trades, so transaction costs do not apply."
        return out
    if zero is None or zero <= 0:
        out["reason"] = "There is no positive excess return even before costs."
        return out
    ceiling = at_cost(bars, signals, costs, BREAK_EVEN_CEILING)["sharpe"]
    if ceiling is not None and ceiling > 0:
        out["break_even_above"] = BREAK_EVEN_CEILING
        out["reason"] = f"Sharpe stays positive even at {BREAK_EVEN_CEILING:.0f} bps per fill."
        return out
    low, high = 0.0, BREAK_EVEN_CEILING
    for _ in range(24):
        middle = (low + high) / 2
        value = at_cost(bars, signals, costs, middle)["sharpe"]
        if value is not None and value > 0:
            low = middle
        else:
            high = middle
    out["break_even_bps"] = round((low + high) / 2, 2)
    out["margin"] = out["break_even_bps"] / current if current > 0 else None
    return out


def seed_dispersion(original: dict, alternates: list[dict]) -> dict:
    """How the same rule fares on other draws of the same synthetic market."""
    if not alternates:
        return {"status": "skipped", "reason": "No alternative paths were requested."}

    def sharpe(entry, key):
        value = entry[key]["sharpe"]
        return -math.inf if value is None else value

    beats = sum(1 for p in alternates if sharpe(p, "strategy") > sharpe(p, "benchmark"))
    values = [p["strategy"]["sharpe"] for p in alternates if p["strategy"]["sharpe"] is not None]
    mean = statistics.fmean(values) if values else None
    deviation = statistics.stdev(values) if len(values) > 1 else None
    first = original["strategy"]["sharpe"]
    return {
        "status": "completed",
        "original": original,
        "paths": alternates,
        "beats_benchmark_share": beats / len(alternates),
        "original_beats_benchmark": sharpe(original, "strategy") > sharpe(original, "benchmark"),
        "mean_sharpe": mean,
        "std_sharpe": deviation,
        "positive_share": sum(1 for v in values if v > 0) / len(alternates),
        "original_z": (first - mean) / deviation
        if first is not None and mean is not None and deviation
        else None,
    }
