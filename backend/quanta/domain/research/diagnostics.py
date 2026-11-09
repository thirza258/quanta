"""Statistics that try to disprove a backtest.

- Deflated Sharpe ratio: Bailey and López de Prado (2014), "The Deflated
  Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and
  Non-Normality", Journal of Portfolio Management 40(5).
- Probability of backtest overfitting by combinatorially symmetric
  cross-validation: Bailey, Borwein, López de Prado and Zhu (2017), "The
  Probability of Backtest Overfitting", Journal of Computational Finance 20(4).
- Random timing: the rule's own signal series circularly shifted against the
  prices, which keeps its exposure and holding periods and removes its timing.
- Look-ahead: the rule re-run on histories cut short must reproduce its
  earlier signals exactly; a causal rule cannot see bars that do not exist.
"""

from __future__ import annotations

import itertools
import math
import statistics
from datetime import date
from statistics import NormalDist

import numpy as np

from quanta.domain.research.metrics import (
    PERIODS,
    RISK_FREE_DAILY,
    evaluate,
    per_period_sharpe,
)

EULER_GAMMA = 0.5772156649015329
NORMAL = NormalDist()


def expected_max_sharpe(trials: int, variance: float) -> float:
    """Expected maximum of `trials` Sharpe estimates whose true value is zero (per period)."""
    if trials < 2 or variance <= 0:
        return 0.0
    return math.sqrt(variance) * (
        (1 - EULER_GAMMA) * NORMAL.inv_cdf(1 - 1 / trials)
        + EULER_GAMMA * NORMAL.inv_cdf(1 - 1 / (trials * math.e))
    )


def moments(returns) -> tuple[float, float]:
    """Sample skewness and (non-excess) kurtosis; a normal distribution has 0 and 3."""
    centered = np.asarray(returns, dtype=float) - np.mean(returns)
    m2 = float(np.mean(centered**2))
    if m2 <= 0:
        return 0.0, 3.0
    return float(np.mean(centered**3) / m2**1.5), float(np.mean(centered**4) / m2**2)


def deflated_sharpe(returns, trial_sharpes, trials: int) -> dict:
    """Probability that the true Sharpe exceeds the best Sharpe luck alone would give.

    `returns` are the reported strategy's simple daily returns; `trial_sharpes`
    are the per-period Sharpe ratios of every configuration tried (None for
    undefined ones, which count as trials but carry no variance).
    """
    returns = np.asarray(returns, dtype=float)
    observations = len(returns)
    sharpe = per_period_sharpe(returns)
    if sharpe is None or observations < 3:
        return {"status": "undefined", "reason": "The strategy's returns do not vary."}
    defined = [s for s in trial_sharpes if s is not None]
    variance = statistics.variance(defined) if len(defined) > 1 else 0.0
    benchmark = expected_max_sharpe(trials, variance)
    skewness, kurtosis = moments(returns)
    scale = 1 - skewness * sharpe + (kurtosis - 1) / 4 * sharpe**2
    if scale <= 0:
        return {"status": "undefined", "reason": "The return distribution is too skewed."}

    def probability(threshold):
        return NORMAL.cdf((sharpe - threshold) * math.sqrt(observations - 1) / math.sqrt(scale))

    return {
        "status": "completed",
        "dsr": probability(benchmark),
        "psr": probability(0.0),
        "sharpe": sharpe * math.sqrt(PERIODS),
        "expected_max_sharpe": benchmark * math.sqrt(PERIODS),
        "trial_sharpe_std": math.sqrt(variance) * math.sqrt(PERIODS),
        "trials": trials,
        "observations": observations,
        "skewness": skewness,
        "kurtosis": kurtosis,
    }


def block_count(observations: int) -> int | None:
    for blocks in (16, 12, 8):
        if observations >= blocks * 21:
            return blocks
    return None


def probability_of_overfitting(matrix, blocks: int | None = None) -> dict:
    """CSCV estimate over a T x N matrix of daily returns (one column per configuration).

    The rows are cut into S contiguous blocks. Every way of choosing S/2 of
    them as in-sample picks the configuration with the best in-sample Sharpe
    and records its out-of-sample rank among all N. PBO is the share of splits
    where that rank is at or below the median (logit <= 0).
    """
    returns = np.asarray(matrix, dtype=float)
    observations, configurations = returns.shape
    if configurations < 4:
        return {
            "status": "skipped",
            "reason": "Needs at least four configurations to rank a selection.",
        }
    blocks = blocks or block_count(observations)
    if blocks is not None and (blocks < 2 or blocks % 2):
        raise ValueError("CSCV needs an even number of blocks, at least two.")
    if blocks is None:
        return {
            "status": "skipped",
            "reason": "Needs at least 168 observations for eight blocks of a month.",
        }
    excess = returns - RISK_FREE_DAILY
    parts = np.array_split(np.arange(observations), blocks)
    sums = np.stack([excess[p].sum(axis=0) for p in parts])
    squares = np.stack([(excess[p] ** 2).sum(axis=0) for p in parts])
    counts = np.array([len(p) for p in parts], dtype=float)
    combos = list(itertools.combinations(range(blocks), blocks // 2))
    mask = np.zeros((len(combos), blocks))
    for row, chosen in enumerate(combos):
        mask[row, list(chosen)] = 1.0

    def sharpe(selection):
        n = (selection @ counts)[:, None]
        mean = (selection @ sums) / n
        variance = ((selection @ squares) - n * mean**2) / (n - 1)
        with np.errstate(invalid="ignore", divide="ignore"):
            ratio = mean / np.sqrt(variance)
        return np.where(variance > 1e-20, ratio, -np.inf)

    in_sample, out_of_sample = sharpe(mask), sharpe(1.0 - mask)
    chosen = np.argmax(in_sample, axis=1)
    picked = out_of_sample[np.arange(len(combos)), chosen]
    below = (out_of_sample < picked[:, None]).sum(axis=1)
    tied = (out_of_sample == picked[:, None]).sum(axis=1)
    rank = below + (tied + 1) / 2
    omega = rank / (configurations + 1)
    logits = np.log(omega / (1 - omega))

    def annualized_median(values):
        values = values[np.isfinite(values)]
        return float(np.median(values) * math.sqrt(PERIODS)) if values.size else None

    return {
        "status": "completed",
        "pbo": float(np.mean(logits <= 0)),
        "blocks": blocks,
        "combinations": len(combos),
        "configurations": configurations,
        "median_logit": float(np.median(logits)),
        "oos_below_risk_free": float(np.mean(picked < 0)),
        "in_sample_sharpe_median": annualized_median(in_sample[np.arange(len(combos)), chosen]),
        "out_of_sample_sharpe_median": annualized_median(picked),
    }


def random_timing(bars, signals, costs, actual_sharpe, count: int, seed: int) -> dict:
    """Permutation p-value of the rule's Sharpe against its own exposure, re-timed at random."""
    if count <= 0:
        return {"status": "skipped", "reason": "The random-timing test was switched off."}
    series = np.asarray(signals, dtype=bool)
    if series.all() or not series.any():
        return {
            "status": "skipped",
            "reason": "The rule is always invested or always in cash, so it has no timing to test.",
        }
    if actual_sharpe is None:
        return {"status": "skipped", "reason": "The strategy's Sharpe ratio is undefined."}
    n = len(series)
    rng = np.random.default_rng(seed)
    shifts = rng.choice(np.arange(1, n), size=min(count, n - 1), replace=False)
    null = []
    for shift in shifts:
        value = evaluate(bars, np.roll(series, int(shift)).tolist(), costs)["metrics"]["sharpe"]
        null.append(-math.inf if value is None else value)
    exceed = sum(1 for value in null if value >= actual_sharpe)
    finite = sorted(v for v in null if math.isfinite(v))
    return {
        "status": "completed",
        "p_value": (1 + exceed) / (1 + len(null)),
        "permutations": len(null),
        "seed": seed,
        "actual_sharpe": actual_sharpe,
        "percentile": sum(1 for v in null if v < actual_sharpe) / len(null),
        "null_median": statistics.median(finite) if finite else None,
        "null_p05": float(np.quantile(finite, 0.05)) if finite else None,
        "null_p95": float(np.quantile(finite, 0.95)) if finite else None,
    }


def concentration(years: list[dict]) -> dict:
    if len(years) < 3:
        return {"status": "skipped", "reason": "Needs at least three calendar years."}
    total = sum(y["pnl"] for y in years)
    if total <= 0:
        return {"status": "skipped", "reason": "There is no net profit to attribute."}
    best = max(years, key=lambda y: y["pnl"])
    return {
        "status": "completed",
        "best_year": best["year"],
        "best_year_pnl": best["pnl"],
        "share": best["pnl"] / total,
        "years": len(years),
        "losing_years": sum(1 for y in years if y["pnl"] < 0),
    }


def cut_points(n: int) -> list[int]:
    return sorted({k for k in (n // 3, n // 2, (3 * n) // 4) if k >= 2})


def lookahead(bars, full: list[bool], truncated: list[dict]) -> dict:
    """Compare the full run's signals with runs on histories ending earlier.

    `truncated` holds {"bars": k, "signals": [...]} or {"bars": k, "error": "..."}.
    A rule that fails on a shorter history cannot be shown to be causal.
    """
    checks, failed = [], False
    for entry in truncated:
        k = entry["bars"]
        check = {"bars": k, "time": bars[k - 1]["time"]}
        if entry.get("error"):
            check.update(match=False, error=entry["error"])
            failed = True
        else:
            difference = next(
                (i for i in range(k) if bool(entry["signals"][i]) != bool(full[i])), None
            )
            check["match"] = difference is None
            if difference is not None:
                check["first_difference"] = bars[difference]["time"]
                failed = True
        checks.append(check)
    return {"status": "fail" if failed else "pass", "checks": checks}


def data_quality(bars: list[dict]) -> dict:
    """Integrity checks a historical import should pass before anyone trusts a backtest on it."""
    times = [b["time"] for b in bars]
    duplicates = len(times) - len(set(times))
    # Strictly earlier only: a repeated timestamp is already counted as a duplicate.
    unordered = sum(1 for a, b in zip(times, times[1:]) if b < a)
    non_positive = sum(1 for b in bars if min(b["open"], b["high"], b["low"], b["close"]) <= 0)
    inconsistent = sum(
        1
        for b in bars
        if b["low"] > min(b["open"], b["close"]) or b["high"] < max(b["open"], b["close"])
    )
    missing_volume = sum(1 for b in bars if not b.get("volume") or b["volume"] <= 0)
    gaps = 0
    for a, b in zip(times, times[1:]):
        try:
            days = (date.fromisoformat(b[:10]) - date.fromisoformat(a[:10])).days
        except ValueError:
            continue
        if days > 5:
            gaps += 1
    extreme = sum(
        1
        for a, b in zip(bars, bars[1:])
        if a["close"] > 0 and abs(b["close"] / a["close"] - 1) > 0.25
    )
    checks = [
        (
            "duplicates",
            "No duplicate timestamps",
            duplicates == 0,
            f"{duplicates} duplicate timestamps",
        ),
        (
            "ordering",
            "Timestamps strictly increase",
            unordered == 0,
            f"{unordered} out-of-order bars",
        ),
        (
            "prices",
            "No zero or negative prices",
            non_positive == 0,
            f"{non_positive} bars with a non-positive price",
        ),
        (
            "ohlc",
            "High and low bracket open and close",
            inconsistent == 0,
            f"{inconsistent} inconsistent bars",
        ),
        (
            "volume",
            "Volume reported on every bar",
            missing_volume == 0,
            f"{missing_volume / len(bars):.1%} of bars without volume",
        ),
        (
            "gaps",
            "No calendar gaps over five days",
            gaps == 0,
            f"{gaps} gaps longer than five days",
        ),
    ]
    out = [
        {
            "id": key,
            "label": label,
            "status": "pass" if ok else "warn",
            "detail": None if ok else detail,
        }
        for key, label, ok, detail in checks
    ]
    out.append(
        {
            "id": "extreme",
            "label": "Daily moves within ±25%",
            "status": "pass" if extreme == 0 else "info",
            "detail": None
            if extreme == 0
            else f"{extreme} close-to-close moves beyond ±25%; check splits and data errors",
        }
    )
    return {"checks": out, "issues": sum(1 for c in out if c["status"] == "warn")}
