"""Inspectable statistical models with explicit synthetic-data provenance."""

import math
from typing import Literal

import numpy as np
from pydantic import BaseModel, Field
from scipy.optimize import minimize
from scipy.stats import t as student_t


class FactorRequest(BaseModel):
    model: Literal["capm", "ff3", "carhart4", "ff5"] = "ff3"
    observations: int = Field(756, ge=60, le=5000)
    seed: int = Field(42, ge=0, le=2**32 - 1)
    noise: float = Field(0.01, gt=0, le=0.1, allow_inf_nan=False)
    # Optional real excess-return observations: first column dependent return;
    # subsequent columns correspond exactly to the selected factor model.
    rows: list[list[float]] | None = Field(None, max_length=5000)


def factor_model(p: FactorRequest):
    names = {
        "capm": ["Market"],
        "ff3": ["Market", "SMB", "HML"],
        "carhart4": ["Market", "SMB", "HML", "MOM"],
        "ff5": ["Market", "SMB", "HML", "RMW", "CMA"],
    }[p.model]
    rng = np.random.default_rng(p.seed)
    if p.rows is not None:
        raw = np.asarray(p.rows, dtype=float)
        if (
            raw.ndim != 2
            or raw.shape[0] < 60
            or raw.shape[1] != len(names) + 1
            or not np.isfinite(raw).all()
            or np.max(np.abs(raw)) > 10
        ):
            raise ValueError(
                "Supply 60–5,000 finite rows: asset excess return followed by the selected factors, in decimal units."
            )
        y, X = raw[:, 0], raw[:, 1:]
    else:
        X = rng.normal(0.0002, 0.01, (p.observations, len(names)))
        true_beta = np.array([1.1, 0.25, 0.4, 0.15, -0.1])[: len(names)]
        y = 0.0001 + X @ true_beta + rng.normal(0, p.noise, len(X))
    design = np.column_stack([np.ones(len(X)), X])
    if np.linalg.matrix_rank(design) < design.shape[1]:
        raise ValueError("Factors are perfectly collinear. Remove duplicate or constant columns.")
    # QR/lstsq for stable coefficients; Newey-West HAC sandwich covariance.
    beta = np.linalg.lstsq(design, y, rcond=None)[0]
    residual = y - design @ beta
    n, k = design.shape
    lags = max(1, int(4 * (n / 100) ** (2 / 9)))
    score = design * residual[:, None]
    meat = score.T @ score
    for lag in range(1, lags + 1):
        gamma = score[lag:].T @ score[:-lag]
        meat += (1 - lag / (lags + 1)) * (gamma + gamma.T)
    bread = np.linalg.pinv(design.T @ design)
    covariance = bread @ meat @ bread * n / (n - k)
    se = np.sqrt(np.maximum(np.diag(covariance), 0))
    tstats = np.divide(beta, se, out=np.zeros_like(beta), where=se > 1e-15)
    pvalues = 2 * student_t.sf(np.abs(tstats), df=n - k)
    total = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1 - float(residual @ residual) / total if total > 1e-15 else 0
    coefficients = [
        {
            "factor": name,
            "coefficient": float(b),
            "standard_error": float(s),
            "t_stat": float(t),
            "p_value": float(pv),
            "lower": float(b - 1.96 * s),
            "upper": float(b + 1.96 * s),
        }
        for name, b, s, t, pv in zip(["Alpha (daily)"] + names, beta, se, tstats, pvalues)
    ]
    # Chronological ridge comparison. Standardization fits the training fold only.
    split = int(n * 0.75)
    mean, std = X[:split].mean(axis=0), X[:split].std(axis=0)
    std = np.where(std > 1e-12, std, 1)
    train = (X[:split] - mean) / std
    target = y[:split] - y[:split].mean()
    ridge = np.linalg.solve(train.T @ train + 10 * np.eye(len(names)), train.T @ target)
    prediction = (X[split:] - mean) / std @ ridge + y[:split].mean()
    mse = float(np.mean((prediction - y[split:]) ** 2))
    baseline = float(np.mean((y[:split].mean() - y[split:]) ** 2))
    return {
        "coefficients": coefficients,
        "r_squared": r2,
        "adjusted_r_squared": 1 - (1 - r2) * (n - 1) / (n - k),
        "observations": n,
        "condition_number": float(np.linalg.cond(design)),
        "hac_lags": lags,
        "ridge_oos_r_squared": 1 - mse / baseline if baseline > 1e-15 else None,
        "train_observations": split,
        "test_observations": n - split,
        "residuals": [
            {"index": i, "residual": float(v)} for i, v in enumerate(residual[:: max(1, n // 150)])
        ],
        "provenance": "Uploaded excess-return observations"
        if p.rows
        else "Synthetic factor observations with planted exposures; not historical Fama–French data",
    }


class PortfolioRequest(BaseModel):
    returns: list[list[float]] = Field(min_length=30, max_length=5000)
    max_weight: float = Field(1, gt=0, le=1, allow_inf_nan=False)


def portfolio(p: PortfolioRequest):
    data = np.asarray(p.returns, dtype=float)
    if (
        data.ndim != 2
        or not 2 <= data.shape[1] <= 20
        or not np.isfinite(data).all()
        or np.max(np.abs(data)) > 10
    ):
        raise ValueError("Use 2–20 assets with finite decimal returns.")
    n = data.shape[1]
    if n * p.max_weight < 1:
        raise ValueError("Weight cap cannot accommodate a fully invested portfolio.")
    covariance = np.cov(data, rowvar=False) * 252
    covariance = 0.9 * covariance + 0.1 * np.diag(np.diag(covariance))
    means = data.mean(axis=0) * 252
    result = minimize(
        lambda w: float(w @ covariance @ w),
        np.ones(n) / n,
        bounds=[(0, p.max_weight)] * n,
        constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}],
        method="SLSQP",
    )
    if not result.success:
        raise ValueError("Optimization did not converge.")
    return {
        "weights": result.x.tolist(),
        "expected_return": float(result.x @ means),
        "volatility": math.sqrt(float(result.fun)),
        "covariance_shrinkage": 0.1,
        "note": "Long-only minimum variance; estimates are annualized and in-sample.",
    }
