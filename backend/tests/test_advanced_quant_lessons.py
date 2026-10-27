"""Independent recomputation of the advanced econometrics and QIA lessons (3.33-3.40, 2.33-2.40).

Each expected figure below is computed from its definition with numpy, scipy or statsmodels, not
copied from the lesson. The lesson's own worksheet runs in the guided runtime, exactly as the
"Run in sandbox" button does, and must print the same figures to the precision it prints them.
Checking a worksheet against the lesson around it proves nothing, because both can be wrong
together; checking it against an independent computation does."""

import re

import pytest
from quanta.domain.analytics import DatasetParams, generate, strategy_data
from quanta.domain.catalog import CATALOG, LESSONS
from quanta.execution.runner import run

NUMBER = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")


def _independent_3_33():
    """Every figure CODE prints, recomputed with scipy / statsmodels / numpy by other routes."""
    import numpy as np
    import statsmodels.api as sm
    from scipy import optimize, stats
    from statsmodels.stats.proportion import proportion_confint, proportions_ztest

    n, x, p0 = 200, 14, 0.04
    y = np.r_[np.ones(x), np.zeros(n - x)]

    def ll(p):  # Bernoulli log-likelihood of the 200 outcomes
        return stats.bernoulli.logpmf(y, p).sum()

    fit = optimize.minimize_scalar(lambda p: -ll(p), bounds=(1e-6, 0.5), method="bounded",
                                   options={"xatol": 1e-12})
    phat = fit.x
    h = 1e-5
    score0 = (ll(p0 + h) - ll(p0 - h)) / (2 * h)                       # numerical derivative
    obs_info0 = -(ll(p0 + h) - 2 * ll(p0) + ll(p0 - h)) / h ** 2         # numerical -Hessian

    def expected_info(p):  # n * E[score^2] over y in {0, 1}
        return n * sum(py * (yy / p - (1 - yy) / (1 - p)) ** 2 for yy, py in ((1, p), (0, 1 - p)))

    info0, info_hat = expected_info(p0), expected_info(phat)
    wald = (phat - p0) ** 2 * info_hat
    lr = 2 * (ll(phat) - ll(p0))
    lm = score0 ** 2 / info0
    # statsmodels routes: score and Wald z from proportions_ztest, log-odds Wald from an intercept-only Logit
    z_score = proportions_ztest(x, n, value=p0, prop_var=p0)[0]
    z_wald = proportions_ztest(x, n, value=p0)[0]
    logit = sm.Logit(y, np.ones((n, 1))).fit(disp=0)
    lg0 = np.log(p0 / (1 - p0))
    wald_logit = float(logit.wald_test(f"const = {lg0}", scalar=True).statistic)
    ci_wald = proportion_confint(x, n, alpha=0.05, method="normal")
    ci_wilson = proportion_confint(x, n, alpha=0.05, method="wilson")
    out = {
        "Default rate estimate:": phat,
        "Log-likelihood at the MLE:": ll(phat),
        "Log-likelihood at the null:": ll(p0),
        "Score at the null:": score0,
        "Expected information at the null:": info0,
        "Expected information at the MLE:": info_hat,
        "Bernoulli variance at the MLE:": phat * (1 - phat),
        "Bernoulli variance at the null:": p0 * (1 - p0),
        "Variance ratio, MLE over null:": phat * (1 - phat) / (p0 * (1 - p0)),
        "Expected defaults under the null:": n * p0,
        "Wald statistic:": z_wald ** 2,
        "LR statistic:": lr,
        "LM statistic:": z_score ** 2,
        "Wald p-value:": stats.chi2.sf(wald, 1),
        "LR p-value:": stats.chi2.sf(lr, 1),
        "LM p-value:": stats.chi2.sf(lm, 1),
        "Wald log-likelihood drop:": wald / 2,
        "Actual log-likelihood drop:": ll(phat) - ll(p0),
        "LM log-likelihood drop:": lm / 2,
        "Observed information at the null:": obs_info0,
        "LM statistic with observed information:": score0 ** 2 / obs_info0,
        "Log-odds estimate:": logit.params[0],
        "Log-odds null value:": lg0,
        "Wald statistic on log-odds scale:": wald_logit,
        "Wald p-value on log-odds scale:": stats.chi2.sf(wald_logit, 1),
        "Exact upper tail P(X >= 14):": stats.binom.sf(x - 1, n, p0),
        "Exact two-sided p, probability ordering:": stats.binomtest(x, n, p0).pvalue,
        "Exact two-sided p, doubled tail:": 2 * stats.binom.sf(x - 1, n, p0),
        "Wald interval lower:": ci_wald[0],
        "Wald interval upper:": ci_wald[1],
        "Score interval lower:": ci_wilson[0],
        "Score interval upper:": ci_wilson[1],
    }
    # Quasi-ML for a variance: build a symmetric four-point population with variance 4 and
    # kurtosis 6, then take A and B as exact expectations of numerical derivatives of the
    # per-observation normal log-likelihood at v = 4.
    v, kurt, m = 4.0, 6.0, 500
    pi = 0.1
    a2 = (8 + np.sqrt(64 + 4 * 704)) / 2          # solves pi*a2 + (1-pi)*b2 = 4, pi*a2^2 + (1-pi)*b2^2 = 96
    b2 = (v - pi * a2) / (1 - pi)
    r2 = np.array([a2, b2])
    w = np.array([pi, 1 - pi])
    assert abs((w * r2).sum() - v) < 1e-9 and abs((w * r2 ** 2).sum() / v ** 2 - kurt) < 1e-9

    def lli(vv, rr2):  # one observation's normal log-likelihood in the variance, mean zero
        return -0.5 * np.log(2 * np.pi * vv) - rr2 / (2 * vv)

    e = 1e-4
    s = (lli(v + e, r2) - lli(v - e, r2)) / (2 * e)
    d2 = (lli(v + e, r2) - 2 * lli(v, r2) + lli(v - e, r2)) / e ** 2
    A, B = -(w * d2).sum(), (w * s ** 2).sum()
    sandwich = B / A ** 2
    se_model, se_robust = np.sqrt(1 / A / m), np.sqrt(sandwich / m)
    out.update({
        "Hessian term A:": A,
        "Score variance B:": B,
        "B divided by A:": B / A,
        "Model-based variance per observation:": 1 / A,
        "Sandwich variance per observation:": sandwich,
        "Model-based SE of the variance:": se_model,
        "Sandwich SE of the variance:": se_robust,
        "SE inflation factor:": se_robust / se_model,
        "z-statistic, model-based SE:": (v - 3.4) / se_model,
        "z-statistic, sandwich SE:": (v - 3.4) / se_robust,
    })
    return out


def _independent_3_34():
    """Every figure CODE prints, recomputed with numpy / scipy by other routes: numerical
    minimization of the GMM objective, the general sandwich formula with G = -c, np.linalg.inv."""
    import numpy as np
    from scipy import optimize, stats

    n = 120
    a = np.array([0.60, 0.80])
    c = np.array([20.0, 10.0])
    G0 = np.array([[12.0, 1.5], [1.5, 3.0]])
    G1 = np.array([[4.0, 0.6], [0.4, 1.0]])
    L = 1
    S = G0 + sum((1 - j / (L + 1)) * (G1 + G1.T) for j in range(1, L + 1))
    G = -c.reshape(2, 1)                     # derivative of a - b c with respect to b

    def minimise(W):
        def obj(b):
            return (a - b * c) @ W @ (a - b * c)

        return optimize.minimize_scalar(obj, bounds=(-1, 1), method="bounded", options={"xatol": 1e-13}).x

    def avar(W, Sx):                         # (G'WG)^-1 G'W S W G (G'WG)^-1 / n
        A = np.linalg.inv(G.T @ W @ G)
        return float((A @ G.T @ W @ Sx @ W @ G @ A)[0, 0] / n)

    Si = np.linalg.inv(S)
    b1, b2 = minimise(np.eye(2)), minimise(Si)
    se1, se2 = np.sqrt(avar(np.eye(2), S)), np.sqrt(avar(Si, S))
    r1, r2 = a - b1 * c, a - b2 * c
    J = n * r2 @ Si @ r2
    perp = np.array([-c[1], c[0]])
    contrast = c[0] * a[1] - c[1] * a[0]
    cov_err = (S - G @ np.linalg.inv(G.T @ Si @ G) @ G.T) / n
    se_err = np.sqrt(np.diag(cov_err))
    S0i = np.linalg.inv(G0)
    b20 = minimise(S0i)
    r20 = a - b20 * c
    return {
        "S11:": S[0, 0], "S12:": S[0, 1], "S22:": S[1, 1],
        "First-step estimate:": b1,
        "First-step pricing error, portfolio 1:": r1[0],
        "First-step pricing error, portfolio 2:": r1[1],
        "First-step standard error:": se1,
        "First-step t-ratio:": b1 / se1,
        "Determinant of S:": np.linalg.det(S),
        "Efficient denominator:": c @ Si @ c,
        "Efficient numerator:": c @ Si @ a,
        "Estimate shift, efficient minus first step:": b2 - b1,
        "Implied SDF loading, portfolio 1:": a[0] / c[0],
        "Implied SDF loading, portfolio 2:": a[1] / c[1],
        "Efficient weight on moment 1:": (c @ Si)[0],
        "Efficient weight on moment 2:": (c @ Si)[1],
        "Efficient estimate:": b2,
        "Efficient standard error:": se2,
        "Efficient t-ratio:": b2 / se2,
        "SE ratio, efficient over first step:": se2 / se1,
        "Efficient pricing error, portfolio 1:": r2[0],
        "Efficient pricing error, portfolio 2:": r2[1],
        "Hansen J statistic:": J,
        "J p-value:": stats.chi2.sf(J, 1),
        "Contrast of the two moments:": contrast,
        "Contrast t-ratio:": contrast / np.sqrt(perp @ S @ perp / n),
        "Squared gap over variance difference:": (b1 - b2) ** 2 / (se1 ** 2 - se2 ** 2),
        "Pricing-error standard error, portfolio 1:": se_err[0],
        "Pricing-error standard error, portfolio 2:": se_err[1],
        "Pricing-error t-ratio, portfolio 1:": r2[0] / se_err[0],
        "Pricing-error t-ratio, portfolio 2:": r2[1] / se_err[1],
        "Naive t-ratio using S/n, portfolio 1:": r2[0] / np.sqrt(S[0, 0] / n),
        "Naive t-ratio using S/n, portfolio 2:": r2[1] / np.sqrt(S[1, 1] / n),
        "J using the lag-zero covariance only:": n * r20 @ S0i @ r20,
        "Quadratic form at the first-step estimate:": n * r1 @ Si @ r1,
    }


def _independent_3_35():
    """Every figure CODE prints, recomputed with numpy and scipy from the definitions."""
    import numpy as np
    from scipy import stats

    T, N, L = 60, 2, 1
    alpha = np.array([0.50, -0.30])
    Sigma = np.array([[4.00, 2.50], [2.50, 6.25]])
    mu_f, var_f = 0.60, 16.00
    quad = float(alpha @ np.linalg.inv(Sigma) @ alpha)
    theta = mu_f**2 / var_f
    # Sharpe-ratio identity: with betas 0.9 and 1.2 the joint covariance of (factor, assets) gives
    # theta_q^2 - theta_f^2 = alpha' Sigma^-1 alpha.
    beta = np.array([0.9, 1.2])
    V = np.zeros((3, 3))
    V[0, 0] = var_f
    V[0, 1:] = beta * var_f
    V[1:, 0] = beta * var_f
    V[1:, 1:] = np.outer(beta, beta) * var_f + Sigma
    mu = np.concatenate([[mu_f], alpha + beta * mu_f])
    theta_q = float(mu @ np.linalg.solve(V, mu))
    assert abs((theta_q - theta) - quad) < 1e-12
    m = T - N - L
    F = m / N * quad / (1 + theta)
    W = T * quad / (1 + theta)
    se = np.sqrt((1 + theta) * np.diag(Sigma) / (T - L - 1))
    t = alpha / se
    slopes = np.array([2.1, -0.8, 1.4, 0.3, 2.6, -1.5, 0.9, -0.2])
    n = len(slopes)
    lam = slopes.mean()
    s2 = slopes.var(ddof=1)
    se_fm = np.sqrt(s2 / n)
    kappa = lam**2 / 1.00
    noise = s2 - 1.00
    se_s = np.sqrt(((1 + kappa) * noise + 1.00) / n)
    se_c = se_fm * np.sqrt(1 + kappa)
    rel_p = 0.30**2 / (0.30**2 + 0.10**2)
    rel_s = 0.40**2 / (0.40**2 + 0.30**2)
    T2 = 600
    m2 = T2 - N - L
    # Simulation check of the attenuation claim in the failure-modes list: ten assets, betas from 0.5 to 1.5,
    # 60 months, factor mean 1.0 and volatility 1.0, residual volatility 4.0 (true price of risk 1.0).
    rng = np.random.default_rng(20261027)
    reps, Ts, Ns = 6000, 60, 10
    betas = np.linspace(0.5, 1.5, Ns)
    fs = rng.normal(1.0, 1.0, (reps, Ts))
    rets = fs[:, :, None] * betas[None, None, :] + rng.normal(0, 4.0, (reps, Ts, Ns))
    fd = fs - fs.mean(1, keepdims=True)
    bh = (fd[:, :, None] * (rets - rets.mean(1, keepdims=True))).sum(1) / (fd**2).sum(1)[:, None]
    bh = bh - bh.mean(1, keepdims=True)
    rbar = rets.mean(1)
    lam_hat = ((rbar - rbar.mean(1, keepdims=True)) * bh).sum(1) / (bh**2).sum(1)
    reliability = betas.var() / (betas.var() + 16.0 / Ts)
    assert abs(reliability - 0.28) < 0.01 and abs(lam_hat.mean() - 0.30) < 0.03

    return {
        "Determinant:": float(np.linalg.det(Sigma)),
        "Quadratic form numerator:": float(alpha @ np.array([[Sigma[1, 1], -Sigma[0, 1]], [-Sigma[1, 0], Sigma[0, 0]]]) @ alpha),
        "Squared Sharpe ratio gain:": quad,
        "Factor squared Sharpe ratio:": theta,
        "Squared Sharpe ratio with test assets:": theta_q,
        "GRS F statistic:": F,
        "GRS p-value:": float(stats.f.sf(F, N, m)),
        "GRS critical value:": float(stats.f.ppf(0.95, N, m)),
        "Wald statistic:": W,
        "Wald p-value:": float(stats.chi2.sf(W, N)),
        "Alpha t statistic, portfolio 1:": float(t[0]),
        "Alpha t statistic, portfolio 2:": float(t[1]),
        "Mean slope:": float(lam),
        "Sum of squared deviations:": float(((slopes - lam) ** 2).sum()),
        "Slope variance:": float(s2),
        "Slope standard deviation:": float(np.sqrt(s2)),
        "Fama-MacBeth standard error:": float(se_fm),
        "Fama-MacBeth t statistic:": float(lam / se_fm),
        "Shanken multiplier:": float(1 + kappa),
        "Cross-sectional noise variance:": float(noise),
        "Shanken variance:": float(se_s**2),
        "Shanken standard error:": float(se_s),
        "Shanken t statistic:": float(lam / se_s),
        "Shortcut standard error:": float(se_c),
        "Shortcut t statistic:": float(lam / se_c),
        "Standard error increase percent:": float((se_s / se_fm - 1) * 100),
        "Reliability ratio, portfolios:": rel_p,
        "Intercept bias, portfolios:": (1 - rel_p) * 0.60,
        "Reliability ratio, stocks:": rel_s,
        "Intercept bias, stocks:": (1 - rel_s) * 0.60,
        "Premium ratio, 60 months:": mu_f * np.sqrt(T) / np.sqrt(var_f),
        "Premium ratio, 600 months:": mu_f * np.sqrt(T2) / np.sqrt(var_f),
        "GRS F statistic, 600 months:": m2 / N * quad / (1 + theta),
        "GRS critical value, 600 months:": float(stats.f.ppf(0.95, N, m2)),
    }


def _independent_3_36():
    """Every figure CODE prints, recomputed with numpy from the definitions."""
    import numpy as np

    T, rho, gamma, beta_hat, se = 240, 0.95, -12.75, 0.70, 0.34
    rho_bias = -(1 + 3 * rho) / T
    bias = gamma * rho_bias
    t = beta_hat / se
    corr = beta_hat - bias
    r2_in = t**2 / (t**2 + T - 2)
    # R^2 = beta^2 Sxx / Syy, so replacing the slope rescales it by the squared ratio of slopes.
    r2_imp = r2_in * (corr / beta_hat) ** 2
    h = 12
    ks = np.arange(-(h - 1), h)
    vif = float(np.sum(rho ** np.abs(ks) * (1 - np.abs(ks) / h)))
    nwf = float(np.sum(rho ** np.abs(ks) * (1 - np.abs(ks) / h) ** 2))
    n = 120
    r2_os = 1 - 1862.0 / 1856.0
    # Expected squared forecast errors: OLS about s2 (1 + 2/n); historical mean about s2 / (1 - R2) (1 + 1/n).
    expected = 1 - (1 + 2 / n) * (1 - r2_imp) / (1 + 1 / n)

    # Persistence adjustment from the AR(1) covariance of the training window.
    idx = np.arange(n)
    a_sum = float(np.sum(rho ** np.abs(idx[:, None] - idx[None, :])))
    s_sum = float(np.sum(rho ** np.arange(1, n + 1)))
    n_eff = n - a_sum / n
    d_var = 1 - 2 * s_sum / n + a_sum / n**2
    q_imp = r2_imp / (1 - r2_imp)
    adjusted = 1 - (1 + 1 / n + d_var / n_eff) / (1 + 1 / n + q_imp * d_var)

    # Simulation check of the claim that the ratio-of-expectations break-even 1 / (n_eff + 1) is slightly
    # optimistic: train on x_0..x_{n-1}, forecast with the next predictor x_n.
    rng2 = np.random.default_rng(7)
    reps2 = 40000
    cur = np.zeros(reps2)
    for _ in range(300):
        cur = rho * cur + rng2.normal(size=reps2)
    path = np.zeros((reps2, n + 1))
    for s in range(n + 1):
        cur = rho * cur + rng2.normal(size=reps2)
        path[:, s] = cur
    train = path[:, :n]
    xbar = train.mean(1)
    sxx = ((train - xbar[:, None]) ** 2).sum(1)
    d2 = (path[:, n] - xbar) ** 2
    q_sim = (d2 / sxx).mean() / (d2.mean() * (1 - rho**2))
    be_sim = q_sim / (1 + q_sim)
    assert 0.0110 < be_sim < 0.0135 and be_sim > 1 / (n_eff + 1)

    # Simulation check of E[beta_hat - beta] = gamma E[rho_hat - rho] and of Kendall's approximation,
    # for a system with sigma_u = 4.5, sigma_v = 0.30 and corr(u, v) = -0.85, so gamma = -12.75.
    rng = np.random.default_rng(20261027)
    reps, burn, sd_v, sd_e = 4000, 200, 0.30, 4.5 * np.sqrt(1 - 0.85**2)
    v = rng.normal(0, sd_v, (reps, T + burn + 1))
    u = gamma * v + rng.normal(0, sd_e, (reps, T + burn + 1))
    x = np.zeros((reps, T + burn + 1))
    for s in range(T + burn):
        x[:, s + 1] = rho * x[:, s] + v[:, s + 1]
    x, u = x[:, burn:], u[:, burn:]
    xl, xn, y = x[:, :-1], x[:, 1:], u[:, 1:]
    xd = xl - xl.mean(1, keepdims=True)
    b_hat = (xd * (y - y.mean(1, keepdims=True))).sum(1) / (xd**2).sum(1)
    r_hat = (xd * (xn - xn.mean(1, keepdims=True))).sum(1) / (xd**2).sum(1)
    assert abs(b_hat.mean() - gamma * (r_hat.mean() - rho)) < 0.02
    assert abs((r_hat.mean() - rho) - rho_bias) < 0.003

    return {
        "Bias in rho-hat:": rho_bias,
        "Slope bias:": bias,
        "OLS t statistic:": t,
        "Bias in standard errors:": bias / se,
        "Corrected slope:": corr,
        "Corrected t statistic:": corr / se,
        "In-sample R-squared percent:": r2_in * 100,
        "Implied R-squared percent:": r2_imp * 100,
        "Overlap variance factor:": vif,
        "Overlap standard error factor:": vif**0.5,
        "Overlap-corrected t statistic:": 4.80 / vif**0.5,
        "Newey-West variance factor:": nwf,
        "Newey-West standard error factor:": nwf**0.5,
        "Newey-West corrected t statistic:": 4.80 / nwf**0.5,
        "Out-of-sample R-squared percent:": r2_os * 100,
        "Break-even R-squared percent:": 100 / (n + 2),
        "Expected out-of-sample R-squared percent:": expected * 100,
        "Effective window size:": n_eff,
        "Persistence-adjusted break-even R-squared percent:": 100 / (n_eff + 1),
        "Persistence-adjusted expected out-of-sample R-squared percent:": adjusted * 100,
    }


def _independent_3_37():
    """Chow quantities from the definitions with scipy; the regime filter and smoother by
    brute-force enumeration of every regime path (no recursion), ergodic law from the
    eigenvector of P, and the multi-step forecast from a matrix power."""
    import itertools
    import math

    import numpy as np
    from scipy.stats import f as fdist
    from scipy.stats import norm

    out = {}
    n, k = 120, 2
    ssr_u = 262.0 + 278.0
    chow = ((583.0 - ssr_u) / k) / (ssr_u / (n - 2 * k))
    out["Split SSR:"] = ssr_u
    out["Chow numerator:"] = (583.0 - ssr_u) / k
    out["Chow denominator:"] = ssr_u / (n - 2 * k)
    out["Chow F:"] = chow
    out["Known-date p-value:"] = float(fdist.sf(chow, k, n - 2 * k))
    out["F(2,116) 5% critical value:"] = float(fdist.ppf(0.95, k, n - 2 * k))
    out["Sup-F 5% critical value:"] = 5.9
    out["First scanned month:"] = math.ceil(0.15 * n)
    out["Last scanned month:"] = n - math.ceil(0.15 * n)
    out["Variance ratio:"] = (278.0 / 58) / (262.0 / 58)
    out["CUSUM bound at the last month:"] = 0.948 * math.sqrt(118) * (1 + 2 * 118 / 118)

    mu = np.array([1.0, -2.0])
    sd = np.array([2.0, 5.0])
    P = np.array([[0.95, 0.05], [0.20, 0.80]])
    y = np.array([1.0, -3.0, -5.0])
    values, vectors = np.linalg.eig(P.T)
    pi = np.real(vectors[:, np.argmax(np.real(values))])
    pi = pi / pi.sum()
    out["Ergodic stress probability:"] = float(pi[1])
    out["Expected calm duration:"] = 1 / (1 - P[0, 0])
    out["Expected stress duration:"] = 1 / (1 - P[1, 1])
    out["Persistence eigenvalue:"] = float(np.sort(np.real(values))[0])

    def densities(v):
        return norm.pdf(v, mu, sd)

    def path_weight(path, upto):
        w = pi[path[0]] * densities(y[0])[path[0]]
        for t in range(1, upto):
            w *= P[path[t - 1], path[t]] * densities(y[t])[path[t]]
        return w

    for upto in (1, 2, 3):
        paths = list(itertools.product((0, 1), repeat=upto))
        weights = {p: path_weight(p, upto) for p in paths}
        total = sum(weights.values())
        marginal = [sum(w for p, w in weights.items() if p[t] == 1) / total for t in range(upto)]
        out[f"Month {upto} filtered stress:"] = marginal[upto - 1]
        if upto == 3:
            out["Log-likelihood:"] = math.log(total)
            for t in (1, 2):
                out[f"Month {t} smoothed stress:"] = marginal[t - 1]
    # predicted stress, per-month densities, joints and likelihood, from the one-step law
    prior = pi.copy()
    for t in range(3):
        if t > 0:
            weights = {p: path_weight(p, t) for p in itertools.product((0, 1), repeat=t)}
            tot = sum(weights.values())
            filtered = np.array([sum(w for p, w in weights.items() if p[t - 1] == s) / tot for s in (0, 1)])
            prior = filtered @ P
        d = densities(y[t])
        joint = prior * d
        out[f"Month {t + 1} predicted stress:"] = float(prior[1])
        out[f"Month {t + 1} calm density:"] = float(d[0])
        out[f"Month {t + 1} stress density:"] = float(d[1])
        out[f"Month {t + 1} calm joint:"] = float(joint[0])
        out[f"Month {t + 1} stress joint:"] = float(joint[1])
        out[f"Month {t + 1} likelihood:"] = float(joint.sum())
    # month-2 smoothing ingredients, from the month-3 filtered and month-3 predicted laws
    paths2 = {p: path_weight(p, 2) for p in itertools.product((0, 1), repeat=2)}
    tot2 = sum(paths2.values())
    filt2 = np.array([sum(w for p, w in paths2.items() if p[1] == s) / tot2 for s in (0, 1)])
    pred3 = filt2 @ P
    paths3 = {p: path_weight(p, 3) for p in itertools.product((0, 1), repeat=3)}
    tot3 = sum(paths3.values())
    filt3 = np.array([sum(w for p, w in paths3.items() if p[2] == s) / tot3 for s in (0, 1)])
    ratio = filt3 / pred3
    out["Month 2 smoothing ratio calm:"] = float(ratio[0])
    out["Month 2 smoothing ratio stress:"] = float(ratio[1])
    out["Month 2 smoothing weight calm:"] = float(P[0] @ ratio)
    out["Month 2 smoothing weight stress:"] = float(P[1] @ ratio)
    out["Stress probability three months ahead:"] = float((filt3 @ np.linalg.matrix_power(P, 3))[1])
    return out


def _independent_3_38():
    """Every printed figure from batch Gaussian conditioning: the five months of states and
    returns form one multivariate normal, so filtered/predicted/smoothed laws, forecast
    variances, gains and likelihoods follow from conditioning formulas with no recursion.
    The log-likelihood is cross-checked against statsmodels' KalmanFilter."""
    import math

    import numpy as np
    from scipy.stats import multivariate_normal, norm

    f = np.array([2.0, -3.0, 4.0, 1.5, -2.5])
    r = np.array([2.2, -3.5, 5.3, 2.1, -3.7])
    b0, p0, se2, sn2 = 0.80, 0.0625, 1.0, 0.01
    n = len(f)

    def joint(sn):
        # beta_s, beta_t covariance: prior variance plus accumulated drift
        cov_b = np.array([[p0 + sn * (min(s, t) - 1) for t in range(1, n + 1)] for s in range(1, n + 1)])
        d = np.diag(f)
        cov_r = d @ cov_b @ d + se2 * np.eye(n)
        cov_br = cov_b @ d
        return cov_b, cov_r, cov_br

    cov_b, cov_r, cov_br = joint(sn2)
    mean_b = np.full(n, b0)
    mean_r = f * b0
    out = {}
    for t in range(n):
        past = slice(0, t)
        # laws given returns before month t+1 (index t)
        if t == 0:
            _e_b, v_b, e_r, v_r, c_br = b0, p0, f[0] * b0, f[0] ** 2 * p0 + se2, p0 * f[0]
        else:
            s_pp = cov_r[past, past]
            def solve(x):
                return np.linalg.solve(s_pp, x)
            mean_b[t] + cov_br[t, past] @ solve(r[past] - mean_r[past])
            v_b = cov_b[t, t] - cov_br[t, past] @ solve(cov_br[t, past])
            e_r = mean_r[t] + cov_r[t, past] @ solve(r[past] - mean_r[past])
            v_r = cov_r[t, t] - cov_r[t, past] @ solve(cov_r[t, past])
            c_br = cov_br[t, t] - cov_br[t, past] @ solve(cov_r[past, t])
        innovation = r[t] - e_r
        gain = c_br / v_r
        tag = f"Month {t + 1}"
        out[f"{tag} predicted variance:"] = v_b
        out[f"{tag} forecast variance:"] = v_r
        out[f"{tag} gain:"] = gain
        out[f"{tag} innovation:"] = innovation
        if t == 0:
            out["Month 1 predicted return:"] = e_r
        # filtered law: condition on returns through month t+1
        upto = slice(0, t + 1)
        s_uu = cov_r[upto, upto]
        post_mean = mean_b[t] + cov_br[t, upto] @ np.linalg.solve(s_uu, r[upto] - mean_r[upto])
        post_var = cov_b[t, t] - cov_br[t, upto] @ np.linalg.solve(s_uu, cov_br[t, upto])
        out[f"{tag} filtered beta:"] = post_mean
        out[f"{tag} filtered variance:"] = post_var
        if t == 0:
            out["Month 1 log-likelihood term:"] = norm.logpdf(r[0], e_r, math.sqrt(v_r))
        if t == 4:
            out["Filtered standard deviation, month 5:"] = math.sqrt(post_var)
    out["Log-likelihood:"] = multivariate_normal(mean_r, cov_r).logpdf(r)

    # statsmodels cross-check of the likelihood, with the prior stated for the first state
    from statsmodels.tsa.statespace.kalman_filter import KalmanFilter
    kf = KalmanFilter(k_endog=1, k_states=1)
    kf.bind(r.reshape(1, -1))
    kf["design"] = f.reshape(1, 1, -1)
    kf["transition"] = np.array([[[1.0]]])
    kf["selection"] = np.array([[[1.0]]])
    kf["obs_cov"] = np.array([[se2]])
    kf["state_cov"] = np.array([[sn2]])
    kf.initialize_known(np.array([b0]), np.array([[p0]]))
    assert abs(kf.filter().llf - out["Log-likelihood:"]) < 1e-9

    # OLS comparisons
    out["Rolling cross-product:"] = float(f[2:] @ r[2:])
    out["Rolling sum of squares:"] = float(f[2:] @ f[2:])
    out["Rolling OLS beta:"] = float(np.linalg.lstsq(f[2:, None], r[2:], rcond=None)[0][0])
    out["Full-sample cross-product:"] = float(f @ r)
    out["Full-sample sum of squares:"] = float(f @ f)
    out["Full-sample OLS beta:"] = float(np.linalg.lstsq(f[:, None], r, rcond=None)[0][0])

    # smoothed laws from conditioning on all five returns
    smoothed = mean_b + cov_br @ np.linalg.solve(cov_r, r - mean_r)
    for t in range(4):
        out[f"Smoothed beta, month {t + 1}:"] = smoothed[t]
    out["Month 1 smoothed minus filtered:"] = smoothed[0] - out["Month 1 filtered beta:"]
    # smoothing gain of month 4: filtered variance over the variance predicted for month 5
    s44 = cov_r[:4, :4]
    p44 = cov_b[3, 3] - cov_br[3, :4] @ np.linalg.solve(s44, cov_br[3, :4])
    p54 = cov_b[4, 4] - cov_br[4, :4] @ np.linalg.solve(s44, cov_br[4, :4])
    out["Smoothing gain, month 4:"] = p44 / p54

    # likelihood grid
    for q in (0.0, 0.01, 0.02, 0.05, 0.1):
        cb, cr, _ = joint(q)
        out[f"Log-likelihood at state variance {q}:"] = multivariate_normal(mean_r, cr).logpdf(r)

    # steady state for a factor of constant size: iterate the scalar recursion to its fixed point
    lam = sn2 * float(np.mean(f ** 2)) / se2
    out["Mean squared factor return:"] = float(np.mean(f ** 2))
    out["Signal-to-noise ratio:"] = lam
    fc2 = float(np.mean(f ** 2))
    pred = 1.0
    for _ in range(2000):
        filt = pred * se2 / (fc2 * pred + se2)
        pred = filt + sn2
    weight = fc2 * pred / (fc2 * pred + se2)
    out["Steady-state weight:"] = weight
    out["Equivalent window in months:"] = 2 / weight - 1
    out["Signal-to-noise ratio of a 36-month window:"] = 4 / (36 ** 2 - 1)
    return out


def _independent_3_39():
    """Every figure CODE prints, recomputed with scipy's exact LP solver and numpy."""
    from itertools import combinations

    import numpy as np
    from scipy.optimize import linprog
    from scipy.stats import norm

    x = np.array([0.8, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.4, 2.7, 3.1])
    r = np.array([-0.9, -0.5, 0.0, -0.3, 0.7, -2.6, 0.1, 1.0, -0.8, -4.1, -0.1])
    xh = np.array([1.0, 1.4, 1.8, 2.2, 2.8, 3.3])
    rh = np.array([0.6, 1.4, -1.4, -1.1, -1.2, -4.4])
    tau = 0.10

    def rho(u, t):
        return u * (t - (u < 0))

    def lp_fit(xv, rv, t):
        n = len(xv)
        cost = np.r_[0.0, 0.0, t * np.ones(n), (1 - t) * np.ones(n)]
        equality = np.c_[np.ones(n), xv, np.eye(n), -np.eye(n)]
        bounds = [(None, None)] * 2 + [(0, None)] * (2 * n)
        res = linprog(cost, A_eq=equality, b_eq=rv, bounds=bounds, method="highs")
        return float(res.x[0]), float(res.x[1])

    def mean_loss(a, b, xv, rv):
        return float(np.mean(rho(rv - a - b * xv, tau)))

    def below(a, b, xv, rv):
        return int(np.sum(rv < a + b * xv - 1e-9))

    a, b = lp_fit(x, r, tau)
    a50, b50 = lp_fit(x, r, 0.50)
    a90, b90 = lp_fit(x, r, 0.90)

    const = min(r, key=lambda c: rho(r - c, tau).sum())
    vertex_losses = sorted(
        mean_loss(r[j] - (r[j] - r[i]) / (x[j] - x[i]) * x[j], (r[j] - r[i]) / (x[j] - x[i]), x, r)
        for i, j in combinations(range(len(x)), 2)
    )
    xs_ = [norm.ppf(0.05), norm.ppf(0.01)]
    se5 = np.sqrt(0.05 * 0.95 / 250) / norm.pdf(xs_[0])
    se1 = np.sqrt(0.01 * 0.99 / 250) / norm.pdf(xs_[1])
    return {
        "Check loss at u=-2:": float(rho(-2.0, tau)),
        "Check loss at u=+2:": float(rho(2.0, tau)),
        "Constant 10% quantile:": float(const),
        "Mean pinball, constant line:": mean_loss(const, 0.0, x, r),
        "Days below the constant line:": below(const, 0.0, x, r),
        "Mean pinball, normal rule:": mean_loss(0.0, -1.2816, x, r),
        "Days below the normal rule:": below(0.0, -1.2816, x, r),
        "Fitted intercept:": a,
        "Fitted slope:": b,
        "Mean pinball, fitted line:": mean_loss(a, b, x, r),
        "Days below the fitted line:": below(a, b, x, r),
        "Mean pinball, runner-up line:": vertex_losses[1],
        "Median intercept:": a50,
        "Median slope:": b50,
        "90th percentile slope:": b90,
        "Lines cross at volatility:": (a - a50) / (b50 - b),
        "Fitted 90% VaR at volatility 2.0:": -(a + b * 2.0),
        "Normal-rule 90% VaR at volatility 2.0:": 1.2816 * 2.0,
        "Hold-out mean pinball, fitted line:": mean_loss(a, b, xh, rh),
        "Hold-out mean pinball, normal rule:": mean_loss(0.0, -1.2816, xh, rh),
        "Hold-out mean pinball, constant line:": mean_loss(const, 0.0, xh, rh),
        "Hold-out days below the fitted line:": below(a, b, xh, rh),
        "Hold-out days below the normal rule:": below(0.0, -1.2816, xh, rh),
        "Hold-out days below the constant line:": below(const, 0.0, xh, rh),
        "Chance of no breach in 6 days:": 0.9**6,
        "CAViaR VaR after a -3.0 return:": 0.05 + 0.90 * 2.0 + 0.30 * 3.0,
        "CAViaR VaR after a +0.5 return:": 0.05 + 0.90 * 2.0 + 0.30 * 0.5,
        "SE of a 5% quantile, 250 days:": float(se5),
        "SE of a 1% quantile, 250 days:": float(se1),
    }


def _independent_3_40():
    """Every figure CODE prints, recomputed with numpy and scipy's GPD quantile function."""
    import numpy as np
    from scipy.integrate import quad
    from scipy.stats import genpareto, norm

    top = np.array([6.1, 4.5, 3.6, 3.1, 3.0, 2.9, 2.8, 2.7, 2.6, 2.5, 2.5, 2.4, 2.4, 2.3, 2.2, 2.2, 2.1, 2.1, 2.1, 2.1, 2.1])
    n = 1000

    def hill(k):
        return float(np.mean(np.log(top[:k]) - np.log(top[k])))

    def weissman(k, p):
        # Solve P(X > x) = (k/n) (x / X_(k+1))^(-1/xi) for x at tail probability 1 - p.
        return float(top[k] * (k / (n * (1 - p))) ** hill(k))

    def me(v):
        return float(np.mean(top[top > v] - v))

    slope_me = (me(2.6) - me(2.2)) / (2.6 - 2.2)

    xi, beta, u, nu = 0.24, 0.50, 1.5, 50

    def gpd_var(p):
        return float(u + genpareto.ppf(1 - (n / nu) * (1 - p), xi, scale=beta))

    def gpd_es(p):
        # Definition: the average of the VaR over all tail levels from p to 1.
        total, _ = quad(gpd_var, p, 1)
        return total / (1 - p)

    # Runs declustering written as a day-by-day scan with a quiet-day counter.
    flags = np.zeros(100, dtype=bool)
    flags[[12, 13, 14, 20, 40, 41, 90]] = True
    clusters, quiet, inside = 0, 0, False
    for flag in flags:
        if flag:
            if not inside:
                clusters += 1
                inside = True
            quiet = 0
        else:
            quiet += 1
            if inside and quiet >= 5:
                inside = False
    theta = clusters / 7

    return {
        "Normal 99.9% loss quantile:": float(norm.ppf(0.999) * 1.00),
        "Second largest loss:": float(top[1]),
        "Hill estimate, k=10:": hill(10),
        "Hill estimate, k=20:": hill(20),
        "Hill standard error, k=10:": hill(10) / np.sqrt(10),
        "Hill standard error, k=20:": hill(20) / np.sqrt(20),
        "Mean excess over 2.2:": me(2.2),
        "Mean excess over 2.6:": me(2.6),
        "Mean-excess slope:": slope_me,
        "Shape implied by the mean-excess slope:": slope_me / (1 + slope_me),
        "Weissman 99.9% quantile, k=10:": weissman(10, 0.999),
        "Weissman 99.9% quantile, k=20:": weissman(20, 0.999),
        "Relative standard error, k=20:": hill(20) * np.log(20 / (n * 0.001)) / np.sqrt(20),
        "Chance of a 99.9% breach within 1,000 days:": 1 - 0.999**1000,
        "Sample 99% quantile, 11th largest:": float(np.sort(top)[::-1][10]),
        "GPD 99% VaR:": gpd_var(0.99),
        "GPD 99.9% VaR:": gpd_var(0.999),
        "GPD 99% expected shortfall:": gpd_es(0.99),
        "GPD 99.9% expected shortfall:": gpd_es(0.999),
        "Shape standard error, independent excesses:": (1 + xi) / np.sqrt(nu),
        "Shape half-width of a 95% interval:": 1.96 * (1 + xi) / np.sqrt(nu),
        "Clusters among seven exceedance days:": clusters,
        "Extremal index estimate:": theta,
        "Effective exceedances out of 50:": nu * theta,
        "Shape standard error, clustered:": (1 + xi) / np.sqrt(nu * theta),
    }


def _independent_2_33():
    import numpy as np
    from scipy.optimize import brentq

    par = np.array([0.02, 0.035, 0.045])

    def discount_factors(p):
        # lower-triangular system: p_T * (d_1 + ... + d_T) + d_T = 1
        n = len(p)
        A = np.zeros((n, n))
        for T in range(n):
            A[T, : T + 1] = p[T]
            A[T, T] += 1.0
        return np.linalg.solve(A, np.ones(n))

    d = discount_factors(par)
    t = np.array([1.0, 2.0, 3.0])
    s = (1.0 / d) ** (1.0 / t) - 1.0

    def fwd(a, b):
        # rate for the b years that start a years from now, from spot rates
        sa = s[int(a) - 1]
        sb = s[int(a + b) - 1]
        return ((1 + sb) ** (a + b) / (1 + sa) ** a) ** (1.0 / b) - 1.0

    cpn = 7.0
    cash = np.array([cpn, cpn, 100.0 + cpn])
    price = float(cash @ d)

    def pv(rate, c):
        return float(np.array([c, c, 100.0 + c]) @ (1 + rate) ** (-t))

    ytm = brentq(lambda y: pv(y, cpn) - price, -0.5, 1.0, xtol=1e-14)
    up = discount_factors(par + np.array([0.0, 0.0, 0.0001]))
    s_up = (1.0 / up) ** (1.0 / t) - 1.0
    f21 = fwd(2, 1)
    f21_up = (1 + s_up[2]) ** 3 / (1 + s[1]) ** 2 - 1.0
    # coupons reinvested at the implied one-year forwards, then at the 1y spot rate
    tv_fwd = cpn * (1 + fwd(1, 1)) * (1 + fwd(2, 1)) + cpn * (1 + fwd(2, 1)) + 100.0 + cpn
    tv_short = cpn * (1 + s[0]) ** 2 + cpn * (1 + s[0]) + 100.0 + cpn
    return {
        "Discount factor 1y:": d[0],
        "Discount factor 2y:": d[1],
        "Discount factor 3y:": d[2],
        "Spot rate 1y percent:": s[0] * 100,
        "Spot rate 2y percent:": s[1] * 100,
        "Spot rate 3y percent:": s[2] * 100,
        "Par yield recovered at 3y percent:": (1 - d[2]) / d.sum() * 100,
        "Forward 1y1y percent:": fwd(1, 1) * 100,
        "Forward 2y1y percent:": f21 * 100,
        "Forward 1y2y percent:": fwd(1, 2) * 100,
        "Spot 3y change for +1 bp par yield, bp:": (s_up[2] - s[2]) * 1e4,
        "Forward 2y1y change for +1 bp par yield, bp:": (f21_up - f21) * 1e4,
        "Bond price off the curve:": price,
        "Bond price at the flat 3y par yield:": pv(par[2], cpn),
        "Bond pricing gap:": price - pv(par[2], cpn),
        "Zero-coupon pricing gap:": 100.0 * d[2] - pv(par[2], 0.0),
        "Bond yield to maturity percent:": ytm * 100,
        "Forward-reinvested terminal value:": tv_fwd,
        "Terminal value times 3y discount factor:": tv_fwd * d[2],
        "Realized yield, forward reinvestment percent:": ((tv_fwd / price) ** (1 / 3) - 1) * 100,
        "Realized yield, reinvested at 1y spot percent:": ((tv_short / price) ** (1 / 3) - 1) * 100,
    }


def _independent_2_34():
    import numpy as np
    from scipy.stats import norm

    s0, strike, cap, rate, vol, years = 100.0, 100.0, 20.0, 0.03, 0.25, 1.0
    z = np.array([-0.802, -1.324, -0.248, 0.42, 1.136, 0.11, -0.553, -0.785, 0.749, 1.635])
    disc = np.exp(-rate * years)

    def terminal(draw):
        return s0 * np.exp((rate - 0.5 * vol**2) * years + vol * np.sqrt(years) * draw)

    def payoff(draw):
        return disc * np.minimum(np.maximum(terminal(draw) - strike, 0.0), cap)

    out = {"Sum of recorded draws:": z.sum()}
    out["Payoff starts above z:"] = (np.log(strike / s0) - (rate - 0.5 * vol**2) * years) / (vol * np.sqrt(years))
    out["Payoff reaches the cap at z:"] = (np.log((strike + cap) / s0) - (rate - 0.5 * vol**2) * years) / (vol * np.sqrt(years))
    y = payoff(z)
    for i, value in enumerate(y, start=1):
        out[f"Payoff draw {i}:"] = value
    se_plain = y.std(ddof=1) / np.sqrt(len(y))
    out["Plain estimate:"] = y.mean()
    out["Plain sample standard deviation:"] = y.std(ddof=1)
    out["Plain standard error:"] = se_plain

    half = z[:5]
    pair = 0.5 * (payoff(half) + payoff(-half))
    for i, value in enumerate(pair, start=1):
        out[f"Pair average {i}:"] = value
    se_anti = pair.std(ddof=1) / np.sqrt(len(pair))
    out["Antithetic estimate:"] = pair.mean()
    out["Antithetic standard error:"] = se_anti
    out["Antithetic variance ratio:"] = (se_anti / se_plain) ** 2

    x = disc * terminal(z)
    cov = np.cov(y, x, ddof=1)
    coef = -cov[0, 1] / cov[1, 1]
    rho = np.corrcoef(y, x)[0, 1]
    w = y + coef * (x - s0)
    se_control = w.std(ddof=1) / np.sqrt(len(w))
    out["Control sample mean:"] = x.mean()
    out["Control coefficient:"] = coef
    out["Sample correlation:"] = rho
    out["Variance factor:"] = 1 - rho**2
    out["Control variate estimate:"] = w.mean()
    out["Control variate standard error:"] = se_control
    out["Control adjustment:"] = w.mean() - y.mean()
    out["Control variance ratio:"] = (se_control / se_plain) ** 2

    def call(k):
        d1 = (np.log(s0 / k) + (rate + 0.5 * vol**2) * years) / (vol * np.sqrt(years))
        d2 = d1 - vol * np.sqrt(years)
        return s0 * norm.cdf(d1) - k * np.exp(-rate * years) * norm.cdf(d2)

    exact = call(strike) - call(strike + cap)
    out["Exact price:"] = exact
    out["Plain error:"] = y.mean() - exact
    out["Antithetic error:"] = pair.mean() - exact
    out["Control variate error:"] = w.mean() - exact
    out["Draws for standard error 0.1, plain:"] = np.ceil((y.std(ddof=1) / 0.1) ** 2)
    out["Draws for standard error 0.1, antithetic evaluations:"] = 2 * np.ceil((pair.std(ddof=1) / 0.1) ** 2)
    out["Draws for standard error 0.1, control variate:"] = np.ceil((w.std(ddof=1) / 0.1) ** 2)
    return out


def _independent_2_35():
    """Every figure the worksheet prints, recomputed with numpy and scipy from the definitions."""
    import numpy as np
    from scipy import integrate, stats
    from scipy.optimize import brentq

    x = np.array([8.0, 5.0, 3.0, 1.0, -1.0, -4.0])
    names = "ABCDEF"
    n, sigma, mu0, tau = x.size, 3.0, 0.0, 3.0
    xbar = x.mean()
    s = float(((x - xbar) ** 2).sum())

    def posterior_moments(xi, se):
        """Posterior mean and variance from integrating prior times likelihood numerically."""
        def kernel(t):
            return stats.norm.pdf(t, mu0, tau) * stats.norm.pdf(xi, t, se)
        z0 = integrate.quad(kernel, -80, 80)[0]
        m1 = integrate.quad(lambda t: t * kernel(t), -80, 80)[0] / z0
        m2 = integrate.quad(lambda t: t * t * kernel(t), -80, 80)[0] / z0
        return m1, m2 - m1 * m1

    mean_a, var_a = posterior_moments(8.0, sigma)
    # Weight on the estimate, read off the numerical posterior mean as its slope in x.
    w = posterior_moments(1.0, sigma)[0] - posterior_moments(0.0, sigma)[0]
    z = stats.norm.ppf(0.975)
    half = z * var_a**0.5

    out = {
        "Grand mean:": float(xbar),
        "Sum of squared deviations:": s,
        "Heterogeneity statistic Q:": s / sigma**2,
        "Heterogeneity p-value:": float(stats.chi2.sf(s / sigma**2, n - 1)),
        "Data precision:": 1 / sigma**2,
        "Prior precision:": 1 / tau**2,
        "Posterior precision:": 1 / var_a,
        "Weight on each estimate:": w,
        "Posterior variance:": var_a,
        "Posterior SD:": var_a**0.5,
    }
    for i in range(n):
        out[f"Posterior mean fund {names[i]}:"] = posterior_moments(float(x[i]), sigma)[0]

    out["Confidence interval fund A low:"] = x[0] - z * sigma
    out["Confidence interval fund A high:"] = x[0] + z * sigma
    out["Credible interval fund A low:"] = mean_a - half
    out["Credible interval fund A high:"] = mean_a + half

    # Repeated-sampling coverage: probability, over x ~ N(theta, sigma^2), that the interval
    # w*x + (1-w)*mu0 +/- half contains theta.
    def coverage(theta):
        lo = (theta - half - (1 - w) * mu0) / w
        hi = (theta + half - (1 - w) * mu0) / w
        return integrate.quad(lambda xv: stats.norm.pdf(xv, theta, sigma), lo, hi)[0]

    out["Credible interval coverage at true alpha 0 percent:"] = 100 * coverage(0.0)
    out["Credible interval coverage at true alpha 8 percent:"] = 100 * coverage(8.0)

    # James-Stein, positive part, straight from the definition.
    factor = max(0.0, 1 - (n - 3) * sigma**2 / s)
    out["Collapse threshold for the sum of squares:"] = (n - 3) * sigma**2
    out["James-Stein shrinkage factor:"] = factor
    out["Estimated shrinkage share:"] = 1 - factor
    for i in range(n):
        out[f"James-Stein fund {names[i]}:"] = xbar + factor * (x[i] - xbar)
    tau2_moment = s / (n - 1) - sigma**2
    out["Moment estimate of tau squared:"] = tau2_moment
    out["Plug-in shrinkage share:"] = sigma**2 / (sigma**2 + tau2_moment)

    # Expected total squared error averaged over the prior.  The posterior means attain the
    # posterior variance, summed over funds.  For the unfloored James-Stein rule the loss is
    # split into the grand-mean part (sigma^2) and the part orthogonal to it: given the centred
    # estimates y, the centred true alphas are normal around (1-B)y with variance (1-B)sigma^2
    # per coordinate, and |y|^2 / (sigma^2 + tau^2) is chi-square with n-1 degrees of freedom.
    B = sigma**2 / (sigma**2 + tau**2)
    p = n - 1
    scale = sigma**2 + tau**2
    def radial(u):
        return (B * u**0.5 - (n - 3) * sigma**2 / u**0.5) ** 2 * stats.chi2.pdf(u / scale, p) / scale
    js_total = sigma**2 + p * (1 - B) * sigma**2 + integrate.quad(radial, 0, np.inf)[0]
    bayes_total = n * var_a
    out["Expected total squared error, raw estimates:"] = n * sigma**2
    out["Expected total squared error, posterior means:"] = bayes_total
    out["Expected total squared error, James-Stein:"] = js_total
    out["Cost of learning the prior:"] = js_total - bayes_total

    # Mean squared error of the posterior-mean estimator at a fixed true alpha, integrating
    # (w*x + (1-w)*mu0 - theta)^2 against the sampling density of x.
    def mse(theta):
        def f(xv):
            return stats.norm.pdf(xv, theta, sigma) * (w * xv + (1 - w) * mu0 - theta) ** 2
        return integrate.quad(f, theta - 12 * sigma, theta + 12 * sigma)[0]

    out["Variance of the posterior mean over repeated samples:"] = (w * sigma) ** 2
    out["Posterior-mean MSE at true alpha 2:"] = mse(2.0)
    out["Posterior-mean MSE at true alpha 6:"] = mse(6.0)
    out["Raw-estimate MSE at any true alpha:"] = sigma**2
    out["Break-even true alpha:"] = brentq(lambda t: mse(t) - sigma**2, 1.0, 12.0, xtol=1e-12)

    # Unequal precision: the same integration with each estimate's own standard error.
    out["Posterior mean, estimate 6 with standard error 2:"] = posterior_moments(6.0, 2.0)[0]
    out["Posterior mean, estimate 8 with standard error 6:"] = posterior_moments(8.0, 6.0)[0]
    return out


def _independent_2_36():
    """Every figure the worksheet prints, recomputed with itertools, numpy and scipy."""
    import itertools
    import math

    import numpy as np
    from scipy import stats

    on = np.array([1.8, 2.4, 3.1, 14.0])
    off = np.array([-0.6, 0.4, 0.9, 1.5])
    pooled = np.concatenate([on, off])
    out = {
        "Mean excess return, flag on:": on.mean(),
        "Mean excess return, flag off:": off.mean(),
        "Mean difference:": on.mean() - off.mean(),
        "Sample SD flag on:": on.std(ddof=1),
        "Sample SD flag off:": off.std(ddof=1),
    }
    t = stats.ttest_ind(on, off, equal_var=True)
    out["Standard error of the difference:"] = (on.mean() - off.mean()) / t.statistic
    out["Student t statistic:"] = t.statistic
    out["Student t p-value:"] = t.pvalue

    # Direct enumeration of all C(8,4) relabellings, for the mean difference and for the rank sum.
    ranks = stats.rankdata(pooled)
    w_obs = ranks[:4].sum()
    count_mean = count_rank = splits = 0
    for chosen in itertools.combinations(range(8), 4):
        mask = np.zeros(8, dtype=bool)
        mask[list(chosen)] = True
        splits += 1
        gap = pooled[mask].mean() - pooled[~mask].mean()
        count_mean += abs(gap) >= abs(on.mean() - off.mean()) - 1e-9
        count_rank += abs(ranks[mask].sum() - 18) >= abs(w_obs - 18)
    perm = stats.permutation_test(
        (on, off), lambda a, b: a.mean() - b.mean(), permutation_type="independent",
        n_resamples=np.inf, alternative="two-sided",
    )
    assert abs(perm.pvalue - count_mean / splits) < 1e-12
    out["Splits enumerated:"] = splits
    out["Splits with a mean difference at least as extreme:"] = count_mean
    out["Exact permutation p-value:"] = count_mean / splits

    mw_exact = stats.mannwhitneyu(on, off, alternative="two-sided", method="exact")
    mw_asym = stats.mannwhitneyu(on, off, alternative="two-sided", method="asymptotic")
    u = float(mw_exact.statistic)
    null_sd = math.sqrt(4 * 4 * 9 / 12)
    out["Rank sum W for the flag-on months:"] = w_obs
    out["Mann-Whitney U:"] = u
    out["Null mean of W:"] = 4 * 9 / 2
    out["Null SD of W:"] = null_sd
    out["Normal approximation z with continuity correction:"] = (abs(u - 8) - 0.5) / null_sd
    out["Normal approximation p-value:"] = mw_asym.pvalue
    out["Splits with a rank sum at least as extreme:"] = count_rank
    out["Exact rank-sum p-value:"] = mw_exact.pvalue

    big = on.copy()
    big[3] = 140.0
    t_big = stats.ttest_ind(big, off, equal_var=True)
    out["Student t statistic with the outlier times ten:"] = t_big.statistic
    out["Student t p-value with the outlier times ten:"] = t_big.pvalue
    out["Rank sum W with the outlier times ten:"] = stats.rankdata(np.concatenate([big, off]))[:4].sum()

    for n in (3, 4, 5):
        out[f"Smallest two-sided exact p-value, {n} against {n}:"] = 2 / math.comb(2 * n, n)
    out["Smallest two-sided sign-test p-value, 5 pairs:"] = stats.binomtest(5, 5, 0.5).pvalue
    mc = (1 + 284) / (1 + 9999)
    out["Monte Carlo p-value from 284 hits in 9999 draws:"] = mc
    out["Monte Carlo standard error:"] = math.sqrt(mc * (1 - mc) / 9999)

    d = np.array([0.9, 0.4, 1.3, -0.2, 0.6, 2.1, 0.7, 5.8])
    k = int((d > 0).sum())
    abs_ranks = stats.rankdata(np.abs(d))
    out["Positive differences:"] = k
    out["Sign test p-value:"] = stats.binomtest(k, len(d), 0.5).pvalue
    out["Signed-rank statistic W plus:"] = abs_ranks[d > 0].sum()
    out["Signed-rank exact p-value:"] = stats.wilcoxon(d, method="exact").pvalue
    out["Paired t statistic:"] = stats.ttest_1samp(d, 0.0).statistic
    out["Critical t at 7 degrees of freedom:"] = stats.t.ppf(0.975, 7)

    # Long-run variance inflation of the mean of an AR(1) series: 1 + 2 * sum of rho^k.
    rho, months = 0.3, 60
    inflation = 1 + 2 * sum(rho**j for j in range(1, 400))
    out["Effective sample size at autocorrelation 0.3:"] = months / inflation
    out["Standard error understatement factor:"] = math.sqrt(inflation)
    return out


def _independent_2_37():
    """Every figure CODE prints, recomputed with numpy and statsmodels from the definitions."""
    import math

    import numpy as np
    import statsmodels.api as sm

    x = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0])
    y = np.array([0, 0, 0, 0, 1, 0, 1, 0, 1, 1], dtype=float)
    ysep = np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 1], dtype=float)
    X = sm.add_constant(x)
    out = {}

    ols = sm.OLS(y, X).fit()
    out["LPM slope:"] = ols.params[1]
    out["LPM fitted probability at leverage 1.0:"] = ols.params[0] + ols.params[1] * 1.0
    out["LPM fitted probability at leverage 7.0:"] = ols.params[0] + ols.params[1] * 7.0

    def ll(beta, labels):
        eta = X @ beta
        return float(np.sum(labels * eta - np.logaddexp(0.0, eta)))

    def newton(beta, labels):
        p = 1 / (1 + np.exp(-(X @ beta)))
        w = p * (1 - p)
        score = X.T @ (labels - p)
        info = X.T @ (X * w[:, None])
        return beta + np.linalg.solve(info, score), score, info

    start = np.array([math.log(0.4 / 0.6), 0.0])
    out["Intercept-only start:"] = start[0]
    out["Log-likelihood at the intercept-only start:"] = ll(start, y)
    out["Mean leverage:"] = x.mean()
    out["Sum of leverage:"] = x.sum()
    out["Sum of squared leverage:"] = (x ** 2).sum()
    out["Sum of leverage over defaults:"] = (x * y).sum()
    beta = start.copy()
    for k in range(1, 7):
        new, score, info = newton(beta, y)
        if k == 1:
            out["Score for slope at the start:"] = score[1]
            out["Information determinant at the start:"] = np.linalg.det(info)
            out["Newton step, intercept:"] = new[0] - beta[0]
            out["Newton step, slope:"] = new[1] - beta[1]
            out["LPM slope divided by ybar(1 - ybar):"] = ols.params[1] / (0.4 * 0.6)
            out["Step 1 intercept:"] = new[0]
        beta = new
        if k < 5:
            out[f"Iteration {k} slope:"] = beta[1]
            out[f"Iteration {k} log-likelihood:"] = ll(beta, y)

    res = sm.Logit(y, X).fit(disp=0, tol=1e-12)
    out["Converged intercept:"] = res.params[0]
    out["Converged slope:"] = res.params[1]
    out["Converged log-likelihood:"] = res.llf
    out["Slope standard error:"] = res.bse[1]
    out["Wald z:"] = res.params[1] / res.bse[1]
    out["Wald z squared:"] = (res.params[1] / res.bse[1]) ** 2
    out["LR statistic, teaching sample:"] = res.llr
    out["LR rejects at 5 percent (1 = yes):"] = 1 if res.llr_pvalue < 0.05 else 0
    out["Wald rejects at 5 percent (1 = yes):"] = 1 if res.pvalues[1] < 0.05 else 0
    p_hat = res.predict(X)
    out["Sum of fitted probabilities:"] = p_hat.sum()
    out["Odds ratio per turn of leverage:"] = math.exp(res.params[1])
    out["Average marginal effect:"] = res.get_margeff(at="overall").margeff[0]
    out["Marginal effect at mean leverage:"] = res.get_margeff(at="mean").margeff[0]

    beta = start.copy()
    previous = beta.copy()
    for _ in range(10):
        previous = beta
        beta, _, _ = newton(beta, ysep)
    _, _, info = newton(beta, ysep)
    out["Separated slope after 10 iterations:"] = beta[1]
    out["Separated slope gain in iteration 10:"] = beta[1] - previous[1]
    out["Separated log-likelihood after 10 iterations:"] = ll(beta, ysep)
    out["Separated Wald z after 10 iterations:"] = beta[1] / math.sqrt(np.linalg.inv(info)[1, 1])

    b = np.array([-3.80, 0.55, -0.35, 0.80])
    xa = np.array([1.0, 3.0, 4.0, 1.0])
    xb = np.array([1.0, 4.0, 4.0, 1.0])
    def sig(e):
        return 1 / (1 + math.exp(-e))
    pa, pb = sig(xa @ b), sig(xb @ b)
    out["Borrower A index:"] = xa @ b
    out["Borrower B index:"] = xb @ b
    out["Borrower A probability:"] = pa
    out["Borrower B probability:"] = pb
    out["Odds ratio, leverage:"] = math.exp(b[1])
    out["Odds ratio, interest cover:"] = math.exp(b[2])
    out["Odds ratio, concentration:"] = math.exp(b[3])
    out["Risk ratio, B to A:"] = pb / pa
    out["Marginal effect of leverage at A:"] = b[1] * pa * (1 - pa)
    out["Discrete change, A to B:"] = pb - pa
    out["Concentration effect at A:"] = pa - sig(xa @ b - b[3])

    ybar = 80 / 1000
    ll0 = 1000 * (ybar * math.log(ybar) + (1 - ybar) * math.log(1 - ybar))
    out["Events per slope, production model:"] = 80 / 3
    out["Null log-likelihood:"] = ll0
    out["LR statistic, three slopes:"] = 2 * (-241.60 - ll0)
    out["McFadden pseudo-R2:"] = 1 - (-241.60) / ll0
    out["LR statistic, concentration:"] = 2 * (-241.60 + 244.50)

    out["Cost-based threshold:"] = 2 / 42
    out["Log-odds threshold:"] = math.log(2 / 40)
    out["Expected cost of declining A:"] = (1 - pa) * 2
    out["Expected cost of approving A:"] = pa * 40
    shift = math.log((0.03 / 0.97) / (0.08 / 0.92))
    out["Intercept shift for a 3 percent default rate:"] = shift
    out["Borrower A probability after the shift:"] = sig(xa @ b + shift)
    return out


def _independent_2_38():
    """Every figure CODE prints, recomputed from the definitions with explicit portfolios and matrices."""
    import math

    import numpy as np
    from scipy.optimize import minimize_scalar

    ic, n_stocks, t_reb, rho, tc, z, omega_ann, lam = 0.04, 500, 4, 0.02, 0.6, 1.5, 0.25, 10.0
    out = {}

    # Law from an explicit optimal portfolio: scores standardised to Sum z^2 = N, uneven residual risks.
    rng = np.random.default_rng(7)
    zs = rng.standard_normal(n_stocks)
    zs = (zs - zs.mean()) / zs.std()
    omega = np.exp(rng.normal(-1.6, 0.4, n_stocks))
    alpha = ic * omega * zs
    h = alpha / (2 * lam * omega ** 2)
    ir_period = (h @ alpha) / math.sqrt(np.sum(h ** 2 * omega ** 2))
    ir_ideal = ir_period * math.sqrt(t_reb)
    out["Breadth with independent bets:"] = n_stocks * t_reb
    out["IR with independent bets:"] = ir_ideal

    # Correlated bets from the full covariance matrix of N equal-variance payoffs, mean-to-sd ratio equal to IC.
    cov = (1 - rho) * np.eye(n_stocks) + rho * np.ones((n_stocks, n_stocks))
    ones = np.ones(n_stocks)
    ir_corr_period = (n_stocks * ic) / math.sqrt(ones @ cov @ ones)
    ir_corr = ir_corr_period * math.sqrt(t_reb)
    n_eff = (ir_corr_period / ic) ** 2
    out["Effective bets per rebalance:"] = n_eff
    out["Ceiling on effective bets:"] = 1 / rho
    out["Effective breadth per year:"] = n_eff * t_reb
    out["IR with correlated bets:"] = ir_corr
    out["Share of the ideal IR kept after correlation:"] = ir_corr / ir_ideal

    # Transfer coefficient as the cosine between risk-scaled weights and risk-scaled alphas.
    a = alpha / omega
    u = rng.standard_normal(n_stocks)
    u -= (u @ a) / (a @ a) * a
    u /= np.linalg.norm(u)
    v = tc * a / np.linalg.norm(a) + math.sqrt(1 - tc ** 2) * u
    cos = (a @ v) / (np.linalg.norm(a) * np.linalg.norm(v))
    ir_tc = ir_corr * ((a @ v) / np.linalg.norm(v)) / np.linalg.norm(a)
    assert abs(cos - tc) < 1e-12
    out["IR with transfer coefficient:"] = ir_tc
    out["Share of the ideal IR kept in total:"] = ir_tc / ir_ideal

    # Forecasting rule by horizon.
    risk_q = omega_ann * math.sqrt(1 / t_reb)
    out["Quarterly residual risk (percent):"] = risk_q * 100
    out["Alpha per quarter (percent):"] = ic * risk_q * z * 100
    out["Alpha at an annual rate (percent):"] = ic * risk_q * z * t_reb * 100
    out["Alpha if annual risk meets a quarterly IC (percent):"] = ic * omega_ann * z * 100

    # Risk budget by direct maximisation of IR * w - lam * w^2.
    best = minimize_scalar(lambda w: -(ir_tc * w - lam * w ** 2), bounds=(0, 1), method="bounded", options={"xatol": 1e-12})
    out["Optimal active risk (percent):"] = best.x * 100
    out["Expected active return at the optimum (percent):"] = ir_tc * best.x * 100
    out["Value added at the optimum (percent):"] = -best.fun * 100
    w_naive = ir_ideal / (2 * lam)
    out["Active risk sized from the ideal IR (percent):"] = w_naive * 100
    out["Expected active return at that risk (percent):"] = ir_tc * w_naive * 100
    out["Risk penalty at that risk (percent):"] = lam * w_naive ** 2 * 100
    out["Value added at that risk (percent):"] = (ir_tc * w_naive - lam * w_naive ** 2) * 100

    # Scatter of the quarterly IC, the mean of N unit-variance payoffs, from the payoff covariance matrix.
    sd_corr = math.sqrt(ones @ cov @ ones) / n_stocks
    sd_ind = math.sqrt(ones @ np.eye(n_stocks) @ ones) / n_stocks
    out["IC scatter with independent bets:"] = sd_ind
    out["IC scatter with correlated bets:"] = sd_corr
    out["IC information ratio per quarter:"] = ic / sd_corr
    out["IC information ratio annualised:"] = ic / sd_corr * math.sqrt(t_reb)
    assert abs(ic / sd_corr * math.sqrt(t_reb) - ir_corr) < 1e-12
    out["IC t-statistic, one quarter:"] = ic / sd_corr
    out["IC t-statistic, 20 quarters:"] = ic / (sd_corr / math.sqrt(20))
    out["Years of record for a t-statistic of 2:"] = (2 / ir_tc) ** 2
    out["Independent bets needed for an IR of 0.5:"] = (0.5 / (tc * ic)) ** 2
    return out


def _independent_2_39():
    """Recompute every printed figure with numpy.linalg from the definitions."""
    import numpy as np

    S = np.array([[0.04, 0.01], [0.01, 0.0225]])
    w = np.array([0.6, 0.4])
    delta, tau = 2.5, 0.05
    P = np.array([[1.0, -1.0]])
    Q = np.array([0.05])
    pi = delta * (S @ w)
    Sinv = np.linalg.inv(S)
    se = 0.20 / np.sqrt(10)

    def posterior(omega):
        prior_precision = np.linalg.inv(tau * S)
        view_precision = P.T @ P / omega
        M = prior_precision + view_precision
        rhs = prior_precision @ pi + (P.T @ Q) / omega
        mean = np.linalg.solve(M, rhs)
        weights = np.linalg.solve(delta * S, mean)
        return prior_precision, M, rhs, mean, weights

    prior_precision, M, rhs, mean, weights = posterior(0.0004)
    low = posterior(0.0025)
    high = posterior(0.0001)
    view_var = tau * float((P @ S @ P.T)[0, 0])
    mid_omega = view_var
    mid = posterior(mid_omega)
    # Update form: pi + tau S P' (tau P S P' + omega)^-1 (Q - P pi)
    tS = tau * S
    shift = tS @ P.T @ np.linalg.solve(P @ tS @ P.T + 0.0004, Q - P @ pi)
    # Full-confidence limit: weights that make P E[R] = Q exactly, w = w_mkt + P' (Q - P pi) / (delta P S P')
    tilt = float((Q - P @ pi)[0] / (delta * (P @ S @ P.T)[0, 0]))
    posterior_cov = np.linalg.inv(M)
    market_premium = float(w @ pi)
    market_variance = float(w @ S @ w)
    return {
        "Inverse covariance AA:": float(Sinv[0, 0]),
        "Inverse covariance AB:": float(Sinv[0, 1]),
        "Inverse covariance BB:": float(Sinv[1, 1]),
        "Weight shift A per point of error:": float((Sinv @ np.array([0.01, 0.0]) / delta)[0]),
        "Weight shift B per point of error:": float((Sinv @ np.array([0.01, 0.0]) / delta)[1]),
        "Standard error of a ten-year mean:": float(se),
        "Weight shift A per standard error:": float((Sinv @ np.array([se, 0.0]) / delta)[0]),
        "Weight shift B per standard error:": float((Sinv @ np.array([se, 0.0]) / delta)[1]),
        "Prior return A:": float(pi[0]),
        "Prior return B:": float(pi[1]),
        "Market premium:": market_premium,
        "Market variance:": market_variance,
        "Implied risk aversion:": market_premium / market_variance,
        "Prior view return:": float((P @ pi)[0]),
        "Prior view variance:": view_var,
        "Precision weight on the view:": (1 / 0.0004) / (1 / 0.0004 + 1 / view_var),
        "Prior precision AA:": float(prior_precision[0, 0]),
        "Prior precision AB:": float(prior_precision[0, 1]),
        "Prior precision BB:": float(prior_precision[1, 1]),
        "Posterior precision AA:": float(M[0, 0]),
        "Posterior precision AB:": float(M[0, 1]),
        "Posterior precision BB:": float(M[1, 1]),
        "Right-hand side A:": float(rhs[0]),
        "Right-hand side B:": float(rhs[1]),
        "Determinant of posterior precision:": float(np.linalg.det(M)),
        "Posterior return A:": float(mean[0]),
        "Posterior return B:": float(mean[1]),
        "Posterior view return:": float(mean[0] - mean[1]),
        "Update form shift A:": float(shift[0]),
        "Update form shift B:": float(shift[1]),
        "Weight A:": float(weights[0]),
        "Weight B:": float(weights[1]),
        "Posterior variance of mean A:": float(posterior_cov[0, 0]),
        "Low confidence view return:": float(low[3][0] - low[3][1]),
        "Low confidence weight A:": float(low[4][0]),
        "Low confidence weight B:": float(low[4][1]),
        "High confidence view return:": float(high[3][0] - high[3][1]),
        "High confidence weight A:": float(high[4][0]),
        "High confidence weight B:": float(high[4][1]),
        "Full confidence weight A:": float(w[0] + tilt),
        "Full confidence weight B:": float(w[1] - tilt),
        "Default omega view return:": float(mid[3][0] - mid[3][1]),
        "Default omega weight A:": float(mid[4][0]),
        "Default omega weight B:": float(mid[4][1]),
    }


def _independent_2_40():
    """Recompute every printed figure with scipy from an explicit 250-day hit sequence."""
    import numpy as np
    from scipy.stats import bernoulli, binom, chi2

    T, p, x = 250, 0.01, 7
    # Clustered hits: a run of three, a run of two, two isolated days (1-indexed days).
    hits = np.zeros(T, dtype=int)
    for day in (60, 61, 62, 130, 131, 180, 220):
        hits[day - 1] = 1
    assert hits.sum() == x
    prev, cur = hits[:-1], hits[1:]
    n00 = int(np.sum((prev == 0) & (cur == 0)))
    n01 = int(np.sum((prev == 0) & (cur == 1)))
    n10 = int(np.sum((prev == 1) & (cur == 0)))
    n11 = int(np.sum((prev == 1) & (cur == 1)))
    assert (n00, n01, n10, n11) == (238, 4, 4, 3)

    def pof(k, n):
        ph = k / n
        return 2 * (binom.logpmf(k, n, ph) - binom.logpmf(k, n, p))

    def independence(sequence):
        a, b = sequence[:-1], sequence[1:]
        int(np.sum((a == 0) & (b == 0)))
        m01 = int(np.sum((a == 0) & (b == 1)))
        int(np.sum((a == 1) & (b == 0)))
        m11 = int(np.sum((a == 1) & (b == 1)))
        pooled = (m01 + m11) / (len(sequence) - 1)
        ll_null = bernoulli.logpmf(b, pooled).sum()
        after_calm = b[a == 0]
        after_hit = b[a == 1]
        ll_alt = bernoulli.logpmf(after_calm, after_calm.mean()).sum() + bernoulli.logpmf(after_hit, after_hit.mean()).sum()
        return -2 * (ll_null - ll_alt), ll_null, ll_alt, after_calm.mean(), after_hit.mean(), pooled

    lr_ind, ll_null, ll_alt, pi01, pi11, pooled = independence(hits)
    ll0 = bernoulli.logpmf(hits, p).sum()
    ll1 = bernoulli.logpmf(hits, hits.mean()).sum()
    lr_pof = pof(x, T)
    isolated = np.zeros(T, dtype=int)
    for day in (20, 60, 100, 140, 180, 210, 240):
        isolated[day - 1] = 1
    iso_ind = independence(isolated)[0]
    assert (int(np.sum((isolated[:-1] == 1) & (isolated[1:] == 1)))) == 0
    # The worksheet hard-codes the chi-square 5% critical values; confirm them and the three decisions.
    assert abs(chi2.ppf(0.95, 1) - 3.841) < 5e-4 and abs(chi2.ppf(0.95, 2) - 5.991) < 5e-4
    assert lr_pof > chi2.ppf(0.95, 1) and lr_ind > chi2.ppf(0.95, 1) and lr_pof + lr_ind > chi2.ppf(0.95, 2)
    assert lr_pof + iso_ind < chi2.ppf(0.95, 2)

    def reject_probability(n, true_rate):
        ks = np.arange(0, n + 1)
        stats = np.array([2 * (binom.logpmf(k, n, k / n) - binom.logpmf(k, n, p)) for k in ks])
        return float(binom.pmf(ks, n, true_rate)[stats > 3.841].sum())

    return {
        "Expected exceedances:": T * p,
        "Expected exceedances at 95 percent:": T * 0.05,
        "Exceedance standard deviation:": float(np.sqrt(T * p * (1 - p))),
        "Probability of zero exceedances:": float(binom.pmf(0, T, p)),
        "Exact probability of 7 or more:": float(binom.sf(6, T, p)),
        "Green zone probability:": float(binom.cdf(4, T, p)),
        "Yellow zone probability:": float(binom.cdf(9, T, p) - binom.cdf(4, T, p)),
        "Red zone probability:": float(binom.sf(9, T, p)),
        "Observed exceedance rate:": x / T,
        "Log-likelihood at correct coverage:": float(ll0),
        "Log-likelihood at observed rate:": float(ll1),
        "LR_pof:": float(lr_pof),
        "Hit probability after a calm day:": float(pi01),
        "Hit probability after a hit day:": float(pi11),
        "Pooled hit probability:": float(pooled),
        "Log-likelihood under independence:": float(ll_null),
        "Log-likelihood under Markov hits:": float(ll_alt),
        "LR_ind:": float(lr_ind),
        "LR_cc:": float(lr_pof + lr_ind),
        "LR_pof on 249 days:": float(pof(7, 249)),
        "Isolated LR_ind:": float(iso_ind),
        "Isolated LR_cc:": float(lr_pof + iso_ind),
        "Isolated conditional coverage rejects at 5 percent:": float(lr_pof + iso_ind > chi2.ppf(0.95, 2)),
        "Kupiec rejects at 5 percent:": float(lr_pof > chi2.ppf(0.95, 1)),
        "Independence test rejects at 5 percent:": float(lr_ind > chi2.ppf(0.95, 1)),
        "Conditional coverage rejects at 5 percent:": float(lr_pof + lr_ind > chi2.ppf(0.95, 2)),
        "LR_pof with no exceedances:": float(-2 * T * np.log(1 - p)),
        "Rejection probability when coverage is correct:": reject_probability(250, 0.01),
        "Power at true rate 2 percent, 250 days:": reject_probability(250, 0.02),
        "Green zone probability at true rate 2 percent:": float(binom.cdf(4, T, 0.02)),
        "Power at true rate 2 percent, 1250 days:": reject_probability(1250, 0.02),
    }


EXPECTED = {
    "3.33": _independent_3_33,
    "3.34": _independent_3_34,
    "3.35": _independent_3_35,
    "3.36": _independent_3_36,
    "3.37": _independent_3_37,
    "3.38": _independent_3_38,
    "3.39": _independent_3_39,
    "3.40": _independent_3_40,
    "2.33": _independent_2_33,
    "2.34": _independent_2_34,
    "2.35": _independent_2_35,
    "2.36": _independent_2_36,
    "2.37": _independent_2_37,
    "2.38": _independent_2_38,
    "2.39": _independent_2_39,
    "2.40": _independent_2_40,
}

QIA_ANCHORS = {'2.33': '2.6', '2.34': '2.11', '2.35': '2.12', '2.36': '2.29', '2.37': '2.16', '2.38': '2.24', '2.39': '2.38', '2.40': '2.26'}


@pytest.fixture(scope="module")
def data():
    return strategy_data(generate(DatasetParams(years=1)), 50)


@pytest.mark.parametrize("lesson_id", list(EXPECTED))
def test_advanced_worksheet_matches_independent_computation(lesson_id, data):
    stdout = run(LESSONS[lesson_id]["code"], data)["stdout"]
    lines = stdout.splitlines()
    for label, expected in EXPECTED[lesson_id]().items():
        line = next((line for line in lines if line.startswith(label)), None)
        assert line is not None, (lesson_id, label)
        printed = NUMBER.findall(line[len(label) :])[-1]
        decimals = len(printed.split(".")[1]) if "." in printed and "e" not in printed.lower() else 6
        tolerance = max(0.5 * 10**-decimals + 1e-12, abs(expected) * 1e-9)
        assert abs(float(printed) - expected) <= tolerance, (lesson_id, label, printed, expected)


def test_econometrics_places_two_advanced_units_before_the_projects():
    course = next(c for c in CATALOG if c["id"] == "econometrics")
    ids = [m["id"] for m in course["modules"]]
    advanced = [f"3.{i}" for i in range(33, 41)]
    assert ids[28:36] == advanced and ids[36:] == ["3.29", "3.30", "3.31", "3.32"]
    assert [p["id"] for p in course["parts"]] == [str(i) for i in range(1, 11)]
    for lesson in course["modules"]:
        expected = "8" if lesson["id"] in advanced[:4] else "9" if lesson["id"] in advanced[4:] else None
        if expected:
            assert lesson["part"] == expected, lesson["id"]
    assert [m["part"] for m in course["modules"][-4:]] == ["10"] * 4
    checkpoints = [e for e in course["exams"] if e["kind"] == "checkpoint"]
    assert len(checkpoints) == 9
    assert checkpoints[7]["moduleIds"] == advanced[:4] and checkpoints[8]["moduleIds"] == advanced[4:]
    assert course["exams"][-1]["version"] == 3


def test_quantitative_lessons_join_the_chapter_they_extend():
    course = next(c for c in CATALOG if c["id"] == "statistical-foundations")
    ids = [m["id"] for m in course["modules"]]
    parts = {m["id"]: m["part"] for m in course["modules"]}
    for lesson_id, anchor in QIA_ANCHORS.items():
        assert ids.index(lesson_id) == ids.index(anchor) + 1, lesson_id
        assert parts[lesson_id] == parts[anchor], lesson_id
    assert len(course["parts"]) == 14
    assert course["exams"][-1]["version"] == 4
