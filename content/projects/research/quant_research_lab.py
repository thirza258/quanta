"""Quanta original research lab: actual estimators and transparent execution fixtures.

Install requirements.txt, then run: python quant_research_lab.py
All default observations are synthetic. No market feed, broker, or AI service is called.
See README.md and each function's scope before interpreting the report.
"""

import json
import math

import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint


def sample_factors(seed=42, observations=360):
    rng = np.random.default_rng(seed)
    factors = rng.normal(0.0002, 0.01, (observations, 2))
    noise = rng.normal(0, 0.003, observations)
    for i in range(1, observations):
        noise[i] += 0.45 * noise[i - 1]
    outcome = 0.0002 + factors @ np.array([1.1, 0.3]) + noise
    return np.column_stack([outcome, factors])


def factor_research(rows, train_rows=270, hac_lags=4):
    """Conditional held-out explanation using realized factors, not ex-ante forecasting."""
    rows = np.asarray(rows, dtype=float)
    if rows.ndim != 2 or rows.shape[1] < 2 or not np.isfinite(rows).all():
        raise ValueError("use finite rows: outcome followed by factors")
    if type(train_rows) is not int or not rows.shape[1] + 2 < train_rows < len(rows):
        raise ValueError("leave enough independent training rows and a nonempty test")
    if type(hac_lags) is not int or not 0 <= hac_lags < train_rows:
        raise ValueError("invalid HAC lag count")
    design = sm.add_constant(rows[:, 1:], has_constant="add")
    if np.linalg.matrix_rank(design[:train_rows]) != design.shape[1]:
        raise ValueError("rank-deficient training design")
    fit = sm.OLS(rows[:train_rows, 0], design[:train_rows]).fit()
    robust = fit.get_robustcov_results(
        cov_type="HAC", maxlags=hac_lags, use_correction=True, use_t=False
    )
    prediction = fit.predict(design[train_rows:])
    test = rows[train_rows:, 0]
    mse = float(np.mean((test - prediction) ** 2))
    baseline = float(np.mean((test - rows[:train_rows, 0].mean()) ** 2))
    return {
        "scope": "synthetic conditional return explanation; future factor values are supplied",
        "training_rows": train_rows,
        "test_rows": len(test),
        "coefficients": fit.params.tolist(),
        "classical_se": fit.bse.tolist(),
        "hac_se": robust.bse.tolist(),
        "hac_normal_95_interval": robust.conf_int().tolist(),
        "hac_lags": hac_lags,
        "mse": mse,
        "baseline_mse": baseline,
        "oos_improvement": 1 - mse / baseline if baseline > 0 else None,
        "prediction": prediction.tolist(),
    }


def estimate_ar(values):
    values = np.asarray(values, dtype=float)
    if values.ndim != 1 or len(values) < 5 or not np.isfinite(values).all():
        raise ValueError("supply at least five finite series observations")
    design = sm.add_constant(values[:-1], has_constant="add")
    if np.linalg.matrix_rank(design) != 2:
        raise ValueError("constant AR regressor")
    fit = sm.OLS(values[1:], design).fit()
    intercept, phi = map(float, fit.params)
    return {
        "intercept": intercept,
        "phi": phi,
        "half_life": math.log(0.5) / math.log(phi) if 0 < phi < 1 else None,
    }


def cointegration_research(seed=7, observations=360):
    """Full-sample diagnostics on a planted relation; not a pair-trading backtest."""
    rng = np.random.default_rng(seed)
    x = 100 + np.cumsum(rng.normal(0, 1, observations))
    spread = rng.normal(0, 0.5, observations)
    for i in range(1, observations):
        spread[i] += 0.6 * spread[i - 1]
    y = 1.5 * x + spread
    fit = sm.OLS(y, sm.add_constant(x)).fit()
    statistic, pvalue, critical = coint(y, x, trend="c", maxlag=4, autolag="aic")
    return {
        "scope": "full-sample synthetic diagnostic with planted I(1) levels and stationary spread",
        "hedge_intercept": float(fit.params[0]),
        "hedge_slope": float(fit.params[1]),
        "null": "no cointegration",
        "statistic": float(statistic),
        "p_value": float(pvalue),
        "critical_values": critical.tolist(),
        "estimated_spread_ar": estimate_ar(fit.resid),
    }


def garch_variances(innovations, omega, alpha, beta, initial):
    """Fixed-parameter stationary GARCH fixture, not parameter estimation.

    Output t is computed before observing innovation t; observations update the next forecast.
    """
    values = np.asarray(innovations, dtype=float)
    params = [omega, alpha, beta, initial]
    if (
        values.ndim != 1
        or not np.isfinite(values).all()
        or not all(math.isfinite(p) for p in params)
    ):
        raise ValueError("finite one-dimensional innovations and parameters required")
    if omega <= 0 or initial <= 0 or alpha < 0 or beta < 0 or alpha + beta >= 1:
        raise ValueError("this fixture requires positive stationary variance parameters")
    result = []
    variance = initial
    for shock in values:
        result.append(float(variance))
        variance = omega + alpha * shock**2 + beta * variance
        if not math.isfinite(variance) or variance <= 0:
            raise ValueError("invalid variance path")
    return result


def purged_forward_splits(label_ends, origins, width=3):
    """Indices are availability times; strict label end < test origin, no future training."""
    if type(width) is not int or width <= 0:
        raise ValueError("positive test width required")
    if any(type(end) is not int or end < i for i, end in enumerate(label_ends)):
        raise ValueError("label ends must be integer times at or after observation")
    splits = []
    for origin in origins:
        if type(origin) is not int or not 0 < origin < len(label_ends):
            raise ValueError("invalid test origin")
        training = [i for i in range(origin) if label_ends[i] < origin]
        if not training:
            raise ValueError("no eligible training labels")
        splits.append(
            {
                "origin": origin,
                "train": training,
                "test": list(range(origin, min(origin + width, len(label_ends)))),
            }
        )
    return splits


def rank_targets(scores, eligible, slots=2, cap=0.4):
    """Long-only target weights; deterministic symbol tie-breaking; unallocated weight is cash."""
    if type(slots) is not int or slots <= 0 or not math.isfinite(cap) or not 0 < cap <= 1:
        raise ValueError("invalid slot count or name cap")
    allowed = set(eligible)
    candidates = []
    for symbol, score in scores.items():
        if symbol in allowed:
            if not isinstance(symbol, str) or not math.isfinite(score):
                raise ValueError("eligible scores must be finite and symbols textual")
            candidates.append((symbol, score))
    selected = sorted(candidates, key=lambda pair: (-pair[1], pair[0]))[:slots]
    weight = min(1 / len(selected), cap) if selected else 0
    return {
        "weights": {symbol: weight for symbol, _ in selected},
        "cash_weight": 1 - weight * len(selected),
    }


def match_asks(asks, quantity, limit):
    """Toy ask-side price/time matcher. Order-list position supplies arrival priority."""
    if type(quantity) is not int or quantity <= 0 or not math.isfinite(limit) or limit <= 0:
        raise ValueError("positive taker quantity and limit required")
    if len({order["id"] for order in asks}) != len(asks):
        raise ValueError("duplicate resting order ID")
    for order in asks:
        if (
            not math.isfinite(order["price"])
            or order["price"] <= 0
            or type(order["quantity"]) is not int
            or order["quantity"] <= 0
        ):
            raise ValueError("invalid resting order")
    remaining = quantity
    fills = []
    for _, order in sorted(enumerate(asks), key=lambda pair: (pair[1]["price"], pair[0])):
        if order["price"] > limit or remaining == 0:
            break
        size = min(remaining, order["quantity"])
        fills.append({"order_id": order["id"], "quantity": size, "price": order["price"]})
        remaining -= size
    return {
        "fills": fills,
        "unfilled": remaining,
        "vwap": sum(f["price"] * f["quantity"] for f in fills) / (quantity - remaining)
        if quantity > remaining
        else None,
    }


def lagged_backtest(opens, close_decision_weights, fee_bps=5, capital=10000):
    """Fractional-share long/cash replay. Decision row t executes at open row t+1.

    Unlimited liquidity, synchronous fills, no taxes/borrow/corporate actions. Conservative
    fee budget reduces nominal targets; this is a declared educational execution model.
    """
    prices = np.asarray(opens, dtype=float)
    weights = np.asarray(close_decision_weights, dtype=float)
    if prices.ndim != 2 or len(prices) < 2 or not np.isfinite(prices).all() or (prices <= 0).any():
        raise ValueError("positive finite open-price matrix required")
    if weights.shape != (len(prices) - 1, prices.shape[1]) or not np.isfinite(weights).all():
        raise ValueError("one weight row per prior-close decision required")
    if (weights < 0).any() or (weights.sum(axis=1) > 1 + 1e-12).any():
        raise ValueError("long-only weights cannot exceed total capital")
    if (
        not math.isfinite(fee_bps)
        or not 0 <= fee_bps <= 100
        or not math.isfinite(capital)
        or capital <= 0
    ):
        raise ValueError("invalid fee or capital")
    fee = fee_bps / 10000
    cash, total_fees = float(capital), 0.0
    shares = np.zeros(prices.shape[1])
    trace = []
    for event in range(1, len(prices)):
        price = prices[event]
        before = cash + float(shares @ price)
        budget = before * (1 - fee) / (1 + fee)
        target = weights[event - 1] * budget / price
        delta = target - shares
        # All reductions precede entries; fee budget covers worst-case complete turnover.
        for side in (-1, 1):
            for asset in range(len(shares)):
                if delta[asset] * side > 0:
                    notional = float(delta[asset] * price[asset])
                    cost = abs(notional) * fee
                    cash -= notional + cost
                    total_fees += cost
                    shares[asset] += delta[asset]
        if cash < -1e-8 or (shares < -1e-10).any():
            raise ValueError("account conservation failure")
        trace.append(
            {
                "decision": event - 1,
                "execution": event,
                "cash": cash,
                "shares": shares.tolist(),
                "equity": cash + float(shares @ price),
            }
        )
    return {"equity": trace[-1]["equity"], "fees": total_fees, "trace": trace}


def evidence_scores(expected, accepted):
    expected, accepted = set(expected), set(accepted)
    true = len(expected & accepted)
    return {
        "supported": true,
        "unsupported": len(accepted - expected),
        "missed": len(expected - accepted),
        "precision": true / len(accepted) if accepted else None,
        "recall": true / len(expected) if expected else None,
    }


def covariance_review():
    """Declared two-asset sample, half-shrinkage, and correlation-stress comparison."""
    weights = np.array([0.5, 0.5])
    sample = np.array([[0.04, 0.018], [0.018, 0.09]])
    shrunk = 0.5 * sample + 0.5 * np.diag(np.diag(sample))
    stress = np.array([[0.04, 0.06], [0.06, 0.09]])
    return {
        "sample_variance": float(weights @ sample @ weights),
        "shrunk_variance": float(weights @ shrunk @ weights),
        "stress_variance": float(weights @ stress @ weights),
        "stress_volatility": float(np.sqrt(weights @ stress @ weights)),
        "scope": "stipulated covariance comparison; no portfolio optimization or parameter estimation",
    }


def main():
    report = {
        "factor": factor_research(sample_factors()),
        "covariance": covariance_review(),
        "cointegration": cointegration_research(),
        "garch": garch_variances([0.3, -0.2, 0.1], 0.01, 0.1, 0.8, 0.04),
        "purged_splits": purged_forward_splits([i + 2 for i in range(12)], [6, 9]),
        "ranked_targets": rank_targets({"A": 0.1, "B": 0.2, "C": 0.9}, ["A", "B"]),
        "queue": match_asks(
            [
                {"id": "early", "price": 100, "quantity": 3},
                {"id": "later", "price": 100, "quantity": 4},
                {"id": "higher", "price": 101, "quantity": 9},
            ],
            5,
            100,
        ),
        "lagged_execution": lagged_backtest(
            [[100], [110], [120]], [[1], [0]], fee_bps=0, capital=1100
        ),
        "evidence": evidence_scores(["a", "b", "c", "d"], ["a", "b", "invented"]),
    }
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
