"""Backtests through the shared engine, plus the metrics a research report needs.

`evaluate` is the only entry point to execution in this package. It calls
`analytics.backtest` unchanged and derives volatility, turnover, exposure and
the daily return series from its output, so every figure here is consistent
with the sandbox and the courses.
"""

from __future__ import annotations

import math

import numpy as np

from quanta.domain.analytics import backtest

PERIODS = 252
RISK_FREE = 0.03
RISK_FREE_DAILY = (1 + RISK_FREE) ** (1 / PERIODS) - 1
CURVE_POINTS = 600

# The metrics a comparison table shows, in order (PRD 8.5).
HEADLINE = (
    "total_return",
    "cagr",
    "sharpe",
    "sortino",
    "max_drawdown",
    "calmar",
    "volatility",
    "turnover",
    "win_rate",
    "profit_factor",
    "exposure",
    "trades",
)


def finite(value):
    """JSON-safe number: None for undefined or non-finite values."""
    if value is None:
        return None
    value = float(value)
    return value if math.isfinite(value) else None


def evaluate(bars, signals, costs, *, prior_signal=False, commission_bps=None, slippage_bps=None):
    """Backtest one signal series and return metrics, daily returns and the raw result.

    `costs` supplies capital and the default commission/slippage; the keyword
    overrides let a stress test change friction without copying the spec.
    """
    capital = costs.capital
    result = backtest(
        bars,
        signals,
        capital,
        costs.commission_bps if commission_bps is None else commission_bps,
        costs.slippage_bps if slippage_bps is None else slippage_bps,
        prior_signal=prior_signal,
    )
    equity = np.array([p["equity"] for p in result["equity_curve"]], dtype=float)
    curve = np.r_[capital, equity]
    returns = np.diff(curve) / curve[:-1]
    metrics = {key: finite(value) for key, value in result["metrics"].items()}
    metrics["trades"] = int(result["metrics"]["trades"])
    metrics["round_trips"] = sum(1 for t in result["trades"] if t["pnl"] is not None)
    metrics["volatility"] = (
        float(np.std(returns, ddof=1) * math.sqrt(PERIODS)) if len(returns) > 1 else None
    )
    held = [bool(prior_signal)] + [bool(s) for s in signals[: len(bars) - 1]]
    metrics["exposure"] = sum(held) / len(held)
    years = len(bars) / PERIODS
    average_equity = float(np.mean(curve))
    traded = sum(t["price"] * t["quantity"] for t in result["trades"])
    metrics["turnover"] = traded / average_equity / years if average_equity > 0 else None
    return {"metrics": metrics, "returns": returns, "result": result}


def sharpe_of(metrics) -> float:
    """Sharpe for ranking: an undefined ratio (no variation) never wins."""
    value = metrics.get("sharpe")
    return -math.inf if value is None else value


def per_period_sharpe(returns) -> float | None:
    returns = np.asarray(returns, dtype=float)
    if len(returns) < 2:
        return None
    deviation = float(np.std(returns, ddof=1))
    if deviation <= 1e-14:
        return None
    return float((np.mean(returns) - RISK_FREE_DAILY) / deviation)


def downsample(curve: list[dict], points: int = CURVE_POINTS) -> list[dict]:
    """Keep at most `points` observations, always including the first and last."""
    if len(curve) <= points:
        return curve
    step = (len(curve) - 1) / (points - 1)
    picked = sorted({round(i * step) for i in range(points)})
    return [curve[i] for i in picked]


def compact_curve(result: dict) -> list[dict]:
    return [
        {
            "time": p["time"],
            "equity": round(p["equity"], 2),
            "benchmark": round(p["benchmark"], 2),
            "drawdown": round(p["drawdown"], 6),
        }
        for p in downsample(result["equity_curve"])
    ]


def yearly_pnl(result: dict, capital: float) -> list[dict]:
    """Profit and loss per calendar year from the marked equity curve."""
    years, previous = {}, capital
    for point in result["equity_curve"]:
        year = point["time"][:4]
        entry = years.setdefault(year, {"start": previous, "end": point["equity"]})
        entry["end"] = point["equity"]
        previous = point["equity"]
    return [
        {
            "year": year,
            "pnl": round(v["end"] - v["start"], 2),
            "return": round(v["end"] / v["start"] - 1, 6) if v["start"] else None,
        }
        for year, v in years.items()
    ]


def risk_free_reference(bars, capital) -> dict:
    years = len(bars) / PERIODS
    return {
        "total_return": (1 + RISK_FREE) ** years - 1,
        "cagr": RISK_FREE,
        "sharpe": None,
        "sortino": None,
        "max_drawdown": 0.0,
        "calmar": None,
        "volatility": 0.0,
        "turnover": 0.0,
        "win_rate": None,
        "profit_factor": None,
        "exposure": 0.0,
        "trades": 0,
        "final_equity": capital * (1 + RISK_FREE) ** years,
    }
