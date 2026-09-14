"""Deterministic market simulation, causal execution, and financial analytics."""

from __future__ import annotations

import math
from datetime import date, timedelta
from typing import Literal

import numpy as np
from pydantic import BaseModel, Field, model_validator


class DatasetParams(BaseModel):
    model: Literal["gbm", "merton", "heston", "regime"] = "gbm"
    scenario: Literal[
        "custom",
        "pure_random_walk",
        "1929_crash",
        "1970s_stagflation",
        "2008_liquidity_crisis",
        "flash_crash",
    ] = "custom"
    mu: float = Field(0.08, ge=-1, le=1, allow_inf_nan=False)
    sigma: float = Field(0.2, ge=0.001, le=2, allow_inf_nan=False)
    years: int = Field(3, ge=1, le=30)
    seed: int = Field(42, ge=0, le=2**32 - 1)
    kappa: float = Field(2, gt=0, le=20, allow_inf_nan=False)
    theta: float = Field(0.04, gt=0, le=2, allow_inf_nan=False)
    xi: float = Field(0.3, ge=0, le=2, allow_inf_nan=False)
    rho: float = Field(-0.7, ge=-1, le=1, allow_inf_nan=False)
    jump_frequency: float = Field(1, ge=0, le=50, allow_inf_nan=False)
    window: int = Field(50, ge=2, le=252)
    symbol: str | None = Field(None, max_length=12, pattern=r"^[A-Z0-9.-]+$")


class ExecuteRequest(BaseModel):
    code: str = Field(
        max_length=20000,
        default='def strategy(data):\n    return data["close"] > data["sma_50"]',
    )
    dataset_type: Literal["synthetic", "real"] = "synthetic"
    dataset_params: DatasetParams = Field(default_factory=DatasetParams)
    capital: float = Field(100000, ge=100, le=1e9, allow_inf_nan=False)
    commission_bps: float = Field(5, ge=0, le=500, allow_inf_nan=False)
    slippage_bps: float = Field(3, ge=0, le=500, allow_inf_nan=False)


def generate(params: DatasetParams) -> list[dict]:
    rng = np.random.default_rng(params.seed)
    n, dt = params.years * 252, 1 / 252
    model, mu, sigma = params.model, params.mu, params.sigma
    jump_frequency = params.jump_frequency
    if params.scenario == "pure_random_walk":
        model, mu = "gbm", 0
    elif params.scenario == "1929_crash":
        model, mu, sigma, jump_frequency = "merton", -0.15, 0.38, 7
    elif params.scenario == "1970s_stagflation":
        model, mu, sigma = "gbm", 0.015, 0.32
    elif params.scenario == "2008_liquidity_crisis":
        model, mu, sigma = "heston", -0.18, 0.55
    z = rng.normal(size=n)
    returns = np.empty(n)
    variance = sigma * sigma
    state = 0
    states = [(0.14, 0.14), (0.01, 0.22), (-0.25, 0.5)]
    transition = np.array([[0.985, 0.012, 0.003], [0.02, 0.96, 0.02], [0.015, 0.035, 0.95]])
    for i in range(n):
        local_mu, vol = mu, sigma
        if model == "heston":
            vol = math.sqrt(max(variance, 0))
            correlated = params.rho * z[i] + math.sqrt(1 - params.rho**2) * rng.normal()
            variance = max(
                0,
                variance
                + params.kappa * (params.theta - variance) * dt
                + params.xi * vol * math.sqrt(dt) * correlated,
            )
        elif model == "regime":
            state = rng.choice(3, p=transition[state])
            local_mu, vol = states[state]
        log_return = (local_mu - 0.5 * vol * vol) * dt + vol * math.sqrt(dt) * z[i]
        if model == "merton":
            jump_mean, jump_std = -0.08, 0.12
            compensator = math.exp(jump_mean + 0.5 * jump_std**2) - 1
            log_return -= jump_frequency * compensator * dt
            count = rng.poisson(jump_frequency * dt)
            if count:
                log_return += rng.normal(count * jump_mean, math.sqrt(count) * jump_std)
        if params.scenario == "flash_crash" and i == n // 2:
            log_return += math.log(0.5)
        returns[i] = log_return
    closes = 100 * np.exp(np.cumsum(returns))
    # Split each daily return into overnight and intraday components, preserving close.
    previous = np.r_[100.0, closes[:-1]]
    opens = previous * np.exp(returns * 0.22)
    spreads = np.abs(rng.normal(0, sigma * math.sqrt(dt) * 0.3, n))
    highs = np.maximum(opens, closes) * (1 + spreads)
    lows = np.minimum(opens, closes) / (1 + spreads)
    day = date(2020, 1, 2)
    bars = []
    for i in range(n):
        while day.weekday() > 4:
            day += timedelta(days=1)
        bars.append(
            {
                "time": day.isoformat(),
                "open": float(opens[i]),
                "high": float(highs[i]),
                "low": float(lows[i]),
                "close": float(closes[i]),
                "volume": int(rng.integers(100000, 2000000)),
            }
        )
        day += timedelta(days=1)
    return bars


def strategy_data(bars: list[dict], window: int) -> dict:
    closes = np.array([b["close"] for b in bars])

    def sma(size):
        out = []
        cumulative = np.r_[0, np.cumsum(closes)]
        for i in range(len(closes)):
            start = max(0, i - size + 1)
            out.append(float((cumulative[i + 1] - cumulative[start]) / (i + 1 - start)))
        return out

    return {
        "close": closes.tolist(),
        "open": [b["open"] for b in bars],
        "high": [b["high"] for b in bars],
        "low": [b["low"] for b in bars],
        "volume": [b["volume"] for b in bars],
        "sma_50": sma(window),
        "sma_200": sma(200),
        "returns": np.r_[0, np.diff(closes) / closes[:-1]].tolist(),
    }


def summarize(
    equity: list[float], benchmark: list[float], trades: list[dict], initial: float
) -> dict:
    # Include initial capital so the first bar's costs and loss contribute to risk.
    curve = np.r_[initial, equity]
    market = np.r_[initial, benchmark]
    rets, bench_rets = np.diff(curve) / curve[:-1], np.diff(market) / market[:-1]
    mean, std = (
        float(np.mean(rets)),
        float(np.std(rets, ddof=1)) if len(rets) > 1 else 0,
    )
    risk_free_daily = (1.03) ** (1 / 252) - 1
    downside = float(np.sqrt(np.mean(np.minimum(rets - risk_free_daily, 0) ** 2)))
    dd = curve / np.maximum.accumulate(curve) - 1
    years = len(rets) / 252
    cagr = (curve[-1] / initial) ** (1 / years) - 1 if curve[-1] > 0 else -1
    losses = -rets
    var = float(np.quantile(losses, 0.95))
    tail = losses[losses >= var]
    round_trips = [t["pnl"] for t in trades if t.get("pnl") is not None]
    wins = [p for p in round_trips if p > 0]
    gross_loss = -sum(p for p in round_trips if p < 0)
    variance = float(np.var(bench_rets))
    beta = (
        float(np.mean((rets - mean) * (bench_rets - np.mean(bench_rets))) / variance)
        if variance > 1e-16
        else None
    )
    return {
        "total_return": float(curve[-1] / initial - 1),
        "cagr": float(cagr),
        "sharpe": (mean - risk_free_daily) / std * math.sqrt(252) if std > 1e-14 else None,
        "sortino": (mean - risk_free_daily) / downside * math.sqrt(252)
        if downside > 1e-14
        else None,
        "max_drawdown": float(np.min(dd)),
        "win_rate": len(wins) / len(round_trips) if round_trips else None,
        "profit_factor": sum(wins) / gross_loss if gross_loss else None,
        "alpha": float(
            (mean - risk_free_daily - beta * (np.mean(bench_rets) - risk_free_daily)) * 252
        )
        if beta is not None
        else None,
        "beta": beta,
        "var_95": max(0, var),
        "cvar_95": max(0, float(np.mean(tail))) if len(tail) else None,
        "calmar": float(cagr / -np.min(dd)) if np.min(dd) < 0 else None,
        "trades": len(trades),
        "final_equity": float(curve[-1]),
    }


def backtest(
    bars: list[dict],
    signals: list[float],
    capital: float,
    commission_bps: float,
    slippage_bps: float,
) -> dict:
    cash, shares, entry_cost = capital, 0.0, 0.0
    fee, slip = commission_bps / 10000, slippage_bps / 10000
    trades, values, benchmark, curve = [], [], [], []
    buy_hold_shares = capital / (bars[0]["open"] * (1 + slip) * (1 + fee))
    for i, bar in enumerate(bars):
        # Only the previous close's signal is visible at this open.
        target = bool(signals[i - 1]) if i > 0 else False
        if target and shares == 0:
            price = bar["open"] * (1 + slip)
            shares = cash / (price * (1 + fee))
            cost = shares * price
            commission = cost * fee
            entry_cost = cash
            cash = 0
            trades.append(
                {
                    "time": bar["time"],
                    "side": "BUY",
                    "price": price,
                    "quantity": shares,
                    "commission": commission,
                    "pnl": None,
                }
            )
        elif not target and shares > 0:
            price = bar["open"] * (1 - slip)
            proceeds = shares * price
            commission = proceeds * fee
            cash = proceeds - commission
            trades.append(
                {
                    "time": bar["time"],
                    "side": "SELL",
                    "price": price,
                    "quantity": shares,
                    "commission": commission,
                    "pnl": cash - entry_cost,
                }
            )
            shares, entry_cost = 0.0, 0.0
        value = cash + shares * bar["close"]
        values.append(value)
        benchmark.append(buy_hold_shares * bar["close"])
        curve.append({"time": bar["time"], "equity": value, "benchmark": benchmark[-1]})
    peak = capital
    for point in curve:
        peak = max(peak, point["equity"])
        point["drawdown"] = point["equity"] / peak - 1
    monthly = {}
    previous = capital
    for point in curve:
        month = point["time"][:7]
        if month not in monthly:
            monthly[month] = {"start": previous, "end": point["equity"]}
        monthly[month]["end"] = point["equity"]
        previous = point["equity"]
    return {
        "metrics": summarize(values, benchmark, trades, capital),
        "equity_curve": curve,
        "trades": trades,
        "monthly_returns": [
            {"month": m, "return": v["end"] / v["start"] - 1} for m, v in monthly.items()
        ],
        "bars": bars,
        "open_position": {"quantity": shares, "value": shares * bars[-1]["close"]},
        "assumptions": {
            "fill": "Next-bar open",
            "benchmark": "Buy & hold of the same dataset, including entry costs",
            "risk_free_rate": 0.03,
            "annualization": 252,
            "open_trades": "Marked to last close; excluded from win rate and profit factor",
        },
    }


class ValuationRequest(BaseModel):
    cash: float = Field(40, ge=0, le=1e12, allow_inf_nan=False)
    receivables: float = Field(60, ge=0, le=1e12, allow_inf_nan=False)
    inventory: float = Field(80, ge=0, le=1e12, allow_inf_nan=False)
    liabilities: float = Field(70, ge=0, le=1e12, allow_inf_nan=False)
    shares: float = Field(10, gt=0, le=1e12, allow_inf_nan=False)
    receivable_recovery: float = Field(0.85, ge=0, le=1, allow_inf_nan=False)
    inventory_recovery: float = Field(0.6, ge=0, le=1, allow_inf_nan=False)
    eps: float = Field(4, ge=-10000, le=10000, allow_inf_nan=False)
    growth: float = Field(5, ge=-4, le=30, allow_inf_nan=False)
    bond_yield: float = Field(4.4, gt=0, le=100, allow_inf_nan=False)
    price: float = Field(6, gt=0, le=1e7, allow_inf_nan=False)


def valuation(p: ValuationRequest) -> dict:
    ncav = (p.cash + p.receivables + p.inventory - p.liabilities) / p.shares
    adjusted = (
        p.cash
        + p.receivables * p.receivable_recovery
        + p.inventory * p.inventory_recovery
        - p.liabilities
    ) / p.shares
    graham = p.eps * (8.5 + 2 * p.growth) * 4.4 / p.bond_yield
    return {
        "ncav": ncav,
        "adjusted_ncav": adjusted,
        "screen_price": ncav * 2 / 3,
        "graham_value": graham,
        "margin_of_safety": 1 - p.price / adjusted if adjusted > 0 else None,
        "passes_screen": p.price < ncav * 2 / 3,
    }


class AmmRequest(BaseModel):
    x: float = Field(10, gt=0, le=1e12, allow_inf_nan=False)
    y: float = Field(20000, gt=0, le=1e12, allow_inf_nan=False)
    trade: float = Field(1, ge=0, le=1e12, allow_inf_nan=False)
    fee: float = Field(0.003, ge=0, le=0.1, allow_inf_nan=False)
    price_ratio: float = Field(2, gt=0.001, le=1000, allow_inf_nan=False)
    lower_ratio: float = Field(0.5, gt=0, le=1000, allow_inf_nan=False)
    upper_ratio: float = Field(2, gt=0, le=1000, allow_inf_nan=False)

    @model_validator(mode="after")
    def ordered(self):
        if not self.lower_ratio < 1 < self.upper_ratio:
            raise ValueError("The starting price must lie within the liquidity range.")
        return self


def amm(p: AmmRequest) -> dict:
    effective = p.trade * (1 - p.fee)
    output = p.y * effective / (p.x + effective)
    ratio = p.price_ratio
    lower, upper, price = (
        math.sqrt(p.lower_ratio),
        math.sqrt(p.upper_ratio),
        math.sqrt(ratio),
    )
    # Unit liquidity normalized to initial price=1; compare with holding initial inventory.
    initial_x, initial_y = 1 - 1 / upper, 1 - lower
    bounded = min(upper, max(lower, price))
    final_x, final_y = 1 / bounded - 1 / upper, bounded - lower
    concentrated_value = final_x * ratio + final_y
    hold_value = initial_x * ratio + initial_y
    return {
        "output": output,
        "spot_price": p.y / p.x,
        "execution_price": output / p.trade if p.trade else p.y / p.x,
        "price_impact": 1 - output / p.trade / (p.y / p.x) if p.trade else 0,
        "impermanent_loss": 2 * math.sqrt(ratio) / (1 + ratio) - 1,
        "concentrated_loss": concentrated_value / hold_value - 1,
        "in_range": p.lower_ratio <= ratio <= p.upper_ratio,
        "reserves_after": {"x": p.x + p.trade, "y": p.y - output},
        "fee_x": p.trade * p.fee,
    }
