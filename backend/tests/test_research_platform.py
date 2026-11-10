"""Research platform: the experiment engine and the guided runtime's trailing-window helpers.

Expected values are recomputed independently (pandas, scipy, exact fractions or
brute-force loops written here), never by calling the code under test twice.
"""

import copy
import hashlib
import itertools
import json
import math
import re
from collections import Counter
from fractions import Fraction

import numpy as np
import pandas as pd
import pytest
from pydantic import ValidationError
from quanta.domain.analytics import DatasetParams, backtest, generate, strategy_data
from quanta.domain.research import (
    diagnostics,
    pipeline,
    provenance,
    redteam,
    robustness,
    validation,
)
from quanta.domain.research.metrics import (
    PERIODS,
    RISK_FREE_DAILY,
    downsample,
    evaluate,
    per_period_sharpe,
    yearly_pnl,
)
from quanta.domain.research.spec import INDICATORS as DOCUMENTED_HELPERS
from quanta.domain.research.spec import (
    MAX_CONFIGURATIONS,
    TEMPLATES,
    CostSpec,
    DatasetSpec,
    ExperimentSpec,
    GridParameter,
    StrategySpec,
    ValidationSpec,
    expand_grid,
)
from quanta.execution import native_worker, sandbox_worker
from quanta.execution.runner import ExecutionError, run
from scipy import integrate, stats

COSTS = CostSpec()  # $100,000 with 5 bps commission and 3 bps slippage per fill
CAPITAL, COMMISSION, SLIPPAGE = COSTS.capital, COSTS.commission_bps, COSTS.slippage_bps
HELPERS = sandbox_worker.INDICATORS
CROSSOVER = """def strategy(data, params):
    return sma(data["close"], params["fast"]) > sma(data["close"], params["slow"])
"""


@pytest.fixture(scope="module")
def bars():
    return generate(DatasetParams())  # three years of seed-42 GBM: 756 bars


@pytest.fixture(scope="module")
def data(bars):
    return strategy_data(bars, 50)


def closes(bars):
    return pd.Series([b["close"] for b in bars], dtype=float)


def crossover(bars, fast, slow):
    """Trend signals computed with pandas, independently of the guided runtime."""
    close = closes(bars)
    fast_mean = close.rolling(fast, min_periods=1).mean()
    slow_mean = close.rolling(slow, min_periods=1).mean()
    return [bool(v) for v in fast_mean > slow_mean]


def manual(bars, signals, prior=False, commission=COMMISSION, slippage=SLIPPAGE):
    return backtest(bars, signals, CAPITAL, commission, slippage, prior_signal=prior)["metrics"]


def guided(name, values, n):
    """One guided helper in process, on a fresh interpreter (its own fuel and deadline)."""
    return getattr(sandbox_worker.Interpreter(), name)([float(v) for v in values], n).values


def pandas_reference(name, values, n):
    """The documented helper semantics, written with pandas."""
    s = pd.Series(values, dtype=float)
    lagged = s.shift(n).fillna(s.iloc[0])
    if name == "shift":
        return lagged
    if name == "change":
        return s / lagged - 1
    if name == "ema":
        return s.ewm(span=n, adjust=False).mean()
    window = s.rolling(n, min_periods=1)
    if name == "sma":
        return window.mean()
    if name == "highest":
        return window.max()
    if name == "lowest":
        return window.min()
    deviation = window.std(ddof=0)
    if name == "stdev":
        return deviation
    assert name == "zscore"
    return ((s - window.mean()) / deviation).where(deviation > 1e-12, 0.0)


def exact_rolling(values, n):
    """Population deviation and z-score of each trailing window in exact rational arithmetic."""
    exact = [Fraction(v) for v in values]
    deviations, scores = [], []
    for i in range(len(values)):
        window = exact[max(0, i - n + 1) : i + 1]
        mean = sum(window, Fraction(0)) / len(window)
        deviation = math.sqrt(sum(((v - mean) ** 2 for v in window), Fraction(0)) / len(window))
        deviations.append(deviation)
        scores.append(float((exact[i] - mean) / Fraction(deviation)) if deviation > 1e-12 else 0.0)
    return deviations, scores


def serial(code):
    """run_many for pipeline.execute: one sandbox run per job, in submission order."""

    def run_many(jobs, on_done):
        results = []
        for job_data, params in jobs:
            try:
                results.append(run(code, job_data, params))
            except ExecutionError as error:
                results.append({"error": str(error)})
            on_done()
        return results

    return run_many


def execute(spec, progress=None):
    bars = generate(spec.dataset.params)
    return pipeline.execute(
        spec, bars, serial(spec.strategy.code), progress or (lambda stage, done, total: None)
    )


def single(code):
    """A one-configuration experiment for strategy(data), with cheap diagnostics."""
    return ExperimentSpec(
        strategy=StrategySpec(name="Probe", code=code, parameters=[], base={}),
        validation=ValidationSpec(permutations=20, seed_paths=0),
    )


@pytest.fixture(scope="module")
def default_run():
    spec = ExperimentSpec()  # the documented default: SMA crossover over a 12-point grid
    calls = []
    results = execute(spec, lambda stage, done, total: calls.append((stage, done, total)))
    return spec, results, calls


# 1. backtest(prior_signal=...)


def test_backtest_default_path_is_unchanged_by_the_prior_signal_keyword(bars, data):
    n = len(bars)
    signal_sets = {
        "trend": [c > s for c, s in zip(data["close"], data["sma_50"])],
        "always": [True] * n,
        "never": [False] * n,
        "random": [bool(v) for v in np.random.default_rng(3).integers(0, 2, n)],
    }
    for label, signals in signal_sets.items():
        for commission, slippage in ((0, 0), (5, 3), (40, 20)):
            implicit = backtest(bars, signals, CAPITAL, commission, slippage)
            explicit = backtest(bars, signals, CAPITAL, commission, slippage, prior_signal=False)
            assert json.dumps(implicit, sort_keys=True) == json.dumps(explicit, sort_keys=True)
            # The default starts in cash: nothing can be bought before the first close.
            assert implicit["equity_curve"][0]["equity"] == CAPITAL, label
            assert all(t["time"] != bars[0]["time"] for t in implicit["trades"]), label


def test_prior_signal_with_all_true_signals_is_the_buy_and_hold_benchmark(bars):
    n = len(bars)
    for commission, slippage in ((0, 0), (5, 3), (40, 20)):
        held = backtest(bars, [True] * n, CAPITAL, commission, slippage, prior_signal=True)
        equity = [p["equity"] for p in held["equity_curve"]]
        assert equity == [p["benchmark"] for p in held["equity_curve"]]
        assert [(t["time"], t["side"]) for t in held["trades"]] == [(bars[0]["time"], "BUY")]
        shares = CAPITAL / (bars[0]["open"] * (1 + slippage / 1e4) * (1 + commission / 1e4))
        assert equity[-1] == pytest.approx(shares * bars[-1]["close"], rel=1e-12)
        # Without the prior signal the same rule buys one bar later and misses the benchmark.
        late = backtest(bars, [True] * n, CAPITAL, commission, slippage)
        assert late["trades"][0]["time"] == bars[1]["time"]
        assert late["equity_curve"][-1]["equity"] != held["equity_curve"][-1]["equity"]


# 2. Guided helpers through the sandbox runner


@pytest.mark.parametrize("name", HELPERS)
def test_guided_helpers_match_pandas_through_the_sandbox(name, data):
    windows = ((0,) if name == "shift" else ()) + (1, 2, 3, 20, 200, 800)  # 800 > 756 bars
    payload = dict(data)
    lines = ["def strategy(data):"]
    for n in windows:
        payload[f"expected_{n}"] = pandas_reference(name, data["close"], n).tolist()
        lines.append(
            f'    print({n}, sum(abs({name}(data["close"], {n}) - data["expected_{n}"]) < 1e-9))'
        )
    lines.append('    return data["close"] > 0')
    out = run("\n".join(lines) + "\n", payload)
    matched = dict(map(int, line.split()) for line in out["stdout"].splitlines())
    assert matched == {n: len(data["close"]) for n in windows}


def test_guided_sma_reproduces_the_strategy_data_averages_exactly(data):
    code = """def strategy(data):
    print(sum(sma(data["close"], 200) == data["sma_200"]), sum(sma(data["close"], 49) == data["sma_50"]))
    return sma(data["close"], 50) == data["sma_50"]
"""
    out = run(code, data)
    assert out["signals"] == [True] * len(data["close"])
    full, shorter = map(int, out["stdout"].split())
    assert full == len(data["close"])
    # A 49-bar average agrees only while both windows still cover the same warm-up bars.
    assert shorter == 49


@pytest.mark.parametrize("lag", ["-1", "-0.5", "-1000"])
def test_negative_shift_is_refused(data, lag):
    with pytest.raises(ExecutionError, match="only looks back: a negative lag"):
        run(f'def strategy(data):\n    return shift(data["close"], {lag}) > 0\n', data)


@pytest.mark.parametrize(
    "call",
    [
        'sma(data["close"], 0)',
        'ema(data["close"], -3)',
        'highest(data["close"], 2.5)',
        'lowest(data["close"], 10001)',
        'change(data["close"], 0)',
        'stdev(data["close"], True)',
        'zscore(data["close"], "5")',
        'sma(data["close"], float("inf"))',
        'shift(data["close"], float("nan"))',
        'shift(data["close"], 0.5)',
    ],
)
def test_invalid_windows_are_refused(data, call):
    with pytest.raises(ExecutionError, match="needs a whole-number window"):
        run(f"def strategy(data):\n    return {call} > 0\n", data)


def test_helpers_require_a_numeric_series(data):
    for call in ("sma(5, 3)", "ema(data, 3)"):
        with pytest.raises(ExecutionError, match="takes a numeric series"):
            run(f"def strategy(data):\n    return {call} > 0\n", data)


def test_one_argument_strategy_reports_arity_one(data):
    code = 'def strategy(data):\n    return data["close"] > data["sma_50"]\n'
    expected = [c > s for c, s in zip(data["close"], data["sma_50"])]
    for params in (None, {"k": 2}):  # parameters offered to strategy(data) are not an error
        out = run(code, data, params)
        assert out["arity"] == 1
        assert out["signals"] == expected


def test_two_argument_strategy_receives_its_params(data):
    code = 'def strategy(data, params):\n    return data["close"] > data["sma_50"] * params["k"]\n'
    seen = set()
    for k in (0.97, 1, 1.03):
        out = run(code, data, {"k": k})
        assert out["arity"] == 2
        assert out["signals"] == [c > s * k for c, s in zip(data["close"], data["sma_50"])]
        seen.add(tuple(out["signals"]))
    assert len(seen) == 3
    with pytest.raises(ExecutionError, match="KeyError"):
        run(code, data)  # no params: the lookup fails inside the strategy
    with pytest.raises(ExecutionError, match=r"strategy\(data\) or strategy\(data, params\)"):
        run("def strategy(data, params, extra):\n    return True\n", data, {"k": 1})


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf"), True, "2", [1]])
def test_non_finite_or_non_numeric_params_are_refused(data, value):
    code = 'def strategy(data, params):\n    return data["close"] > params["k"]\n'
    with pytest.raises(ExecutionError, match="finite numbers"):
        run(code, data, {"k": value})


def test_operation_budget_still_trips_on_huge_loops(data):
    code = """def strategy(data):
    total = 0
    for i in range(10000):
        total = total + sma(data["close"], 5)[0]
    return data["close"] > total
"""
    # Through the runner the fuel, the wall-clock deadline or the CPU limit may fire first.
    with pytest.raises(ExecutionError):
        run(code, data)
    # In process, with no deadline, only the operation budget can stop it: each helper call
    # is charged for the length of its series.
    vm = sandbox_worker.Interpreter()
    vm.deadline = math.inf
    with pytest.raises(sandbox_worker.SandboxError, match="Execution limit reached"):
        vm.run(code, data)
    assert vm.fuel < 0


# 2b. Guided stdev and zscore against exact arithmetic


@pytest.mark.parametrize("n", [1, 2, 3, 5, 20])
def test_guided_stdev_and_zscore_match_exact_arithmetic(n, data):
    uniform = [float(v) for v in np.random.default_rng(5).uniform(1, 200, 300)]
    for values in (data["close"], uniform):
        deviations, scores = exact_rolling(values, n)
        np.testing.assert_allclose(guided("stdev", values, n), deviations, rtol=0, atol=1e-12)
        # A z-score inherits the rounding of the window mean (about 1e-14 at prices near
        # 100), divided by the smallest two-bar spread, hence the looser bound.
        np.testing.assert_allclose(guided("zscore", values, n), scores, rtol=0, atol=1e-10)


def test_flat_windows_have_exactly_zero_spread():
    rng = np.random.default_rng(1)
    values = [float(v) for v in rng.lognormal(4.6, 0.3, 80)] + [100.1] * 25 + [57.3] * 25
    for n in (1, 2, 5, 20):
        deviation, score = guided("stdev", values, n), guided("zscore", values, n)
        for i in range(len(values)):
            if len(set(values[max(0, i - n + 1) : i + 1])) == 1:
                assert deviation[i] == 0.0 and score[i] == 0.0, (n, i)
            else:
                assert deviation[i] > 0, (n, i)


# 3. Causality


@pytest.mark.parametrize("name", HELPERS)
def test_guided_helpers_are_causal(name, data):
    rng = np.random.default_rng(11)
    noisy = [float(v) for v in rng.lognormal(4, 0.5, 300)]
    inputs = {
        "close": data["close"],
        "lognormal": noisy,
        "flat": [100.1] * 30 + noisy[:40] + [57.3] * 30 + noisy[40:60],
    }
    for label, values in inputs.items():
        size = len(values)
        for n in (0 if name == "shift" else 1, 2, 5, 63, size + 3):
            full = guided(name, values, n)
            assert len(full) == size
            for k in sorted({1, 2, min(n, size) or 1, size // 3, size // 2, size - 1}):
                assert guided(name, values[:k], n) == full[:k], (label, n, k)


# 4. Docker-runtime (pandas) indicators against the guided helpers


def test_native_indicators_agree_with_the_guided_helpers():
    assert set(HELPERS) == set(native_worker.INDICATORS) == {h[0] for h in DOCUMENTED_HELPERS}
    rng = np.random.default_rng(2024)
    # iid positive series keep pandas' online rolling variance accurate; on trending prices
    # with 2-3 bar windows pandas itself drifts by up to ~1e-8 from the exact value.
    inputs = {
        "uniform": [float(v) for v in rng.uniform(1, 200, 500)],
        "lognormal": [float(v) for v in rng.lognormal(3, 1, 400)],
    }
    for label, values in inputs.items():
        for name in HELPERS:
            for n in (0 if name == "shift" else 1, 2, 3, 5, 20, 63, len(values), len(values) + 7):
                native = native_worker.INDICATORS[name](values, n).to_numpy(dtype=float)
                np.testing.assert_allclose(
                    guided(name, values, n),
                    native,
                    rtol=0,
                    atol=1e-9,
                    err_msg=f"{label} {name}({n})",
                )


def test_both_runtimes_refuse_negative_lags_and_empty_windows():
    values = [1.0, 2.0, 3.0]
    with pytest.raises(ValueError, match="negative lag"):
        native_worker.INDICATORS["shift"](values, -1)
    with pytest.raises(sandbox_worker.SandboxError, match="negative lag"):
        guided("shift", values, -1)
    for name in HELPERS:
        if name != "shift":
            with pytest.raises(ValueError, match="whole numbers"):
                native_worker.INDICATORS[name](values, 0)
            with pytest.raises(sandbox_worker.SandboxError, match="whole-number window"):
                guided(name, values, 0)


# 5. Deflated Sharpe ratio (Bailey and López de Prado, 2014)


def published_dsr(returns, trial_sharpes, trials):
    r = np.asarray(returns, dtype=float)
    sharpe = (r.mean() - RISK_FREE_DAILY) / r.std(ddof=1)
    skew = stats.skew(r, bias=True)
    kurt = stats.kurtosis(r, fisher=False, bias=True)
    variance = np.var([s for s in trial_sharpes if s is not None], ddof=1)
    gamma = np.euler_gamma
    sr0 = math.sqrt(variance) * (
        (1 - gamma) * stats.norm.ppf(1 - 1 / trials)
        + gamma * stats.norm.ppf(1 - 1 / (trials * math.e))
    )
    scale = math.sqrt(1 - skew * sharpe + (kurt - 1) / 4 * sharpe**2)
    root = math.sqrt(len(r) - 1)
    return {
        "dsr": stats.norm.cdf((sharpe - sr0) * root / scale),
        "psr": stats.norm.cdf(sharpe * root / scale),
        "sharpe": sharpe,
        "sr0": sr0,
        "variance": variance,
        "skewness": skew,
        "kurtosis": kurt,
    }


def skewed_returns(seed, size=756, mean=0.002, scale=0.01, df=4, crash_rate=0.03, crash=0.02):
    rng = np.random.default_rng(seed)
    returns = mean + scale * rng.standard_t(df, size)
    returns[rng.random(size) < crash_rate] -= crash  # gaps down: negative skew, fat tails
    return returns


def dsr_case(label):
    if label == "daily":
        # Three years of daily returns: realistic, but at a daily Sharpe near 0.08 the
        # skewness and kurtosis terms barely move the result.
        returns = skewed_returns(5)
        trials = [per_period_sharpe(returns), *np.random.default_rng(6).normal(0.02, 0.03, 9)]
        return returns, [*trials, None, None]
    # Three years of monthly returns with crashes: a per-period Sharpe near 0.2 lets the
    # higher moments change the answer.
    returns = skewed_returns(1, size=36, mean=0.03, scale=0.03, df=5, crash_rate=0.1, crash=0.1)
    return returns, [*np.random.default_rng(7).normal(0.1, 0.12, 11), None]


@pytest.mark.parametrize("label", ["daily", "monthly"])
def test_deflated_sharpe_matches_the_published_formula(label):
    returns, trial_sharpes = dsr_case(label)
    out = diagnostics.deflated_sharpe(returns, trial_sharpes, 12)
    ref = published_dsr(returns, trial_sharpes, 12)
    assert out["status"] == "completed"
    assert 0.05 < ref["dsr"] < ref["psr"] < 0.999  # informative, not saturated
    assert ref["skewness"] < -0.1 and ref["kurtosis"] > 4  # the moment terms are exercised
    assert out["dsr"] == pytest.approx(ref["dsr"], rel=1e-9)
    assert out["psr"] == pytest.approx(ref["psr"], rel=1e-9)
    assert out["skewness"] == pytest.approx(ref["skewness"], rel=1e-9)
    assert out["kurtosis"] == pytest.approx(ref["kurtosis"], rel=1e-9)
    assert out["sharpe"] == pytest.approx(ref["sharpe"] * math.sqrt(252), rel=1e-12)
    assert out["expected_max_sharpe"] == pytest.approx(ref["sr0"] * math.sqrt(252), rel=1e-9)
    assert out["trial_sharpe_std"] == pytest.approx(math.sqrt(ref["variance"] * 252), rel=1e-12)
    assert (out["trials"], out["observations"]) == (12, len(returns))
    if label == "monthly":
        normal = stats.norm.cdf(
            (ref["sharpe"] - ref["sr0"])
            * math.sqrt(len(returns) - 1)
            / math.sqrt(1 + ref["sharpe"] ** 2 / 2)
        )
        assert abs(normal - out["dsr"]) > 0.01  # assuming normality would change the answer


def test_one_trial_makes_dsr_equal_psr():
    returns = skewed_returns(8)
    for trial_sharpes in ([0.05], [0.01, 0.05, 0.09]):
        out = diagnostics.deflated_sharpe(returns, trial_sharpes, 1)
        assert out["expected_max_sharpe"] == 0.0
        assert out["dsr"] == out["psr"]
        assert out["psr"] == pytest.approx(published_dsr(returns, [0, 1], 2)["psr"], rel=1e-9)
    flat = diagnostics.deflated_sharpe([0.001] * 50, [0.1, 0.2], 2)
    assert flat["status"] == "undefined"


def test_expected_max_sharpe_grows_with_trials_and_approximates_the_true_maximum():
    values = [diagnostics.expected_max_sharpe(n, 1.0) for n in range(2, 1001)]
    assert all(b > a for a, b in zip(values, values[1:]))
    assert diagnostics.expected_max_sharpe(1, 1.0) == 0.0
    assert diagnostics.expected_max_sharpe(50, 0.0) == 0.0
    assert diagnostics.expected_max_sharpe(50, 4.0) == pytest.approx(
        2 * diagnostics.expected_max_sharpe(50, 1.0)
    )
    for n in (10, 100, 1000):
        # E[max of n standard normals] by quadrature: the formula is a close approximation.
        exact = integrate.quad(
            lambda x: x * n * stats.norm.pdf(x) * stats.norm.cdf(x) ** (n - 1), -12, 12, limit=200
        )[0]
        approx = diagnostics.expected_max_sharpe(n, 1.0)
        assert abs(approx / exact - 1) < 0.03


# 6. Probability of backtest overfitting (Bailey, Borwein, López de Prado and Zhu, 2017)


def brute_force_pbo(matrix, blocks):
    excess = np.asarray(matrix, dtype=float) - RISK_FREE_DAILY
    rows, configurations = excess.shape
    sizes = [rows // blocks + (1 if b < rows % blocks else 0) for b in range(blocks)]
    edges = np.cumsum([0, *sizes])
    logits = []
    for chosen in itertools.combinations(range(blocks), blocks // 2):
        inside = np.concatenate([np.arange(edges[b], edges[b + 1]) for b in chosen])
        outside = np.concatenate(
            [np.arange(edges[b], edges[b + 1]) for b in range(blocks) if b not in chosen]
        )

        def sharpe(index, j):
            column = excess[index, j]
            return column.mean() / column.std(ddof=1)

        in_sample = [sharpe(inside, j) for j in range(configurations)]
        out_of_sample = [sharpe(outside, j) for j in range(configurations)]
        best = max(range(configurations), key=lambda j: (in_sample[j], -j))
        target = out_of_sample[best]
        rank = (
            1
            + sum(o < target for o in out_of_sample)
            + 0.5 * (sum(o == target for o in out_of_sample) - 1)
        )
        omega = rank / (configurations + 1)
        logits.append(math.log(omega / (1 - omega)))
    return sum(1 for value in logits if value <= 0) / len(logits), logits


@pytest.mark.parametrize("rows,configurations", [(240, 6), (250, 5)])
def test_pbo_matches_a_brute_force_cscv(rows, configurations):
    rng = np.random.default_rng(rows)
    matrix = rng.normal(0.0003, 0.01, (rows, configurations))
    matrix += rng.normal(0, 0.0004, configurations)  # small, different drifts
    out = diagnostics.probability_of_overfitting(matrix)
    assert out["blocks"] == 8 and out["combinations"] == math.comb(8, 4)
    pbo, logits = brute_force_pbo(matrix, 8)
    assert out["pbo"] == pbo
    assert 0 < pbo < 1  # a mixed case, not a degenerate one
    assert out["median_logit"] == pytest.approx(float(np.median(logits)), rel=1e-12)
    assert out["configurations"] == configurations


def test_pbo_is_zero_when_one_configuration_dominates_every_block():
    rng = np.random.default_rng(4)
    matrix = rng.normal(0, 0.01, (240, 6))
    matrix[:, 2] += 0.01
    out = diagnostics.probability_of_overfitting(matrix)
    assert out["pbo"] == 0.0
    assert out["oos_below_risk_free"] == 0.0
    assert brute_force_pbo(matrix, 8)[0] == 0.0


def test_pbo_is_near_one_when_the_in_sample_winner_is_the_out_of_sample_loser():
    rng = np.random.default_rng(9)
    blocks, size, configurations = 8, 30, 6
    noise = rng.normal(0.0005, 0.01, blocks * size)  # shared by every configuration
    offsets = rng.normal(0, 0.001, (configurations, blocks))
    offsets -= offsets.mean(axis=1, keepdims=True)  # each configuration's offsets sum to zero
    matrix = noise[:, None] + np.repeat(offsets.T, size, axis=0)
    out = diagnostics.probability_of_overfitting(matrix, blocks=blocks)
    assert out["pbo"] >= 0.9
    assert out["pbo"] == brute_force_pbo(matrix, blocks)[0]


def test_pbo_skips_small_grids_and_short_histories():
    rng = np.random.default_rng(1)
    assert (
        diagnostics.probability_of_overfitting(rng.normal(0, 0.01, (400, 3)))["status"] == "skipped"
    )
    short = diagnostics.probability_of_overfitting(rng.normal(0, 0.01, (167, 4)))
    assert short["status"] == "skipped" and "168" in short["reason"]
    assert diagnostics.probability_of_overfitting(rng.normal(0, 0.01, (168, 4)))["blocks"] == 8
    boundaries = {167: None, 168: 8, 251: 8, 252: 12, 335: 12, 336: 16, 5000: 16}
    assert {n: diagnostics.block_count(n) for n in boundaries} == boundaries


# 7. Chronological validation


@pytest.mark.parametrize(
    "n,train,test",
    [
        (756, 252, 126),
        (700, 252, 126),
        (692, 252, 126),
        (1000, 126, 63),
        (5040, 126, 63),
        (900, 300, 250),
        (314, 252, 126),
        (378, 252, 126),
    ],
)
@pytest.mark.parametrize("anchored", [False, True])
def test_fold_geometry(n, train, test, anchored):
    windows = validation.folds(n, train, test, anchored)
    span = n - train
    count = min(40, span // test + (1 if span % test >= 63 else 0)) if span >= 0 else 0
    assert len(windows) == count
    for k, (a, b, c, d) in enumerate(windows):
        assert b == c  # training ends where testing starts
        assert a == (0 if anchored else c - train)
        assert 63 <= d - c <= test
        assert c == (train if k == 0 else windows[k - 1][3])  # contiguous test windows
        if k < len(windows) - 1:
            assert d - c == test
    if windows and len(windows) < 40:
        assert n - windows[-1][3] < 63  # what is left untested is shorter than a test window


def test_fold_examples():
    assert validation.folds(756, 252, 126, False) == [
        (0, 252, 252, 378),
        (126, 378, 378, 504),
        (252, 504, 504, 630),
        (378, 630, 630, 756),
    ]
    assert validation.folds(700, 252, 126, True)[-1] == (0, 630, 630, 700)
    assert validation.folds(692, 252, 126, False)[-1][3] == 630
    assert len(validation.folds(126 + 63 * 50, 126, 63, False)) == 40


@pytest.fixture(scope="module")
def grid(bars):
    configs = [{"fast": f, "slow": s} for f in (10, 20, 50) for s in (100, 200)]
    return configs, [crossover(bars, c["fast"], c["slow"]) for c in configs]


def test_train_test_equals_manual_backtests_on_each_slice(bars, grid):
    configs, signal_sets = grid
    n, base_index = len(bars), 3
    out = validation.train_test(bars, signal_sets, configs, base_index, COSTS, 0.7)
    cut = 529  # round(756 * 0.7)
    assert out["in_sample"] == {"start": bars[0]["time"], "end": bars[cut - 1]["time"], "bars": cut}
    assert out["out_of_sample"]["bars"] == n - cut
    assert {bool(s[cut - 1]) for s in signal_sets} == {True, False}  # both entry states occur
    in_sample = [manual(bars[:cut], s[:cut]) for s in signal_sets]
    ranked = [-math.inf if m["sharpe"] is None else m["sharpe"] for m in in_sample]
    chosen = ranked.index(max(ranked))
    assert out["selected"]["index"] == chosen
    for role, index in (("base", base_index), ("selected", chosen)):
        s = signal_sets[index]
        oos = manual(bars[cut:], s[cut:], prior=bool(s[cut - 1]))
        for key in ("sharpe", "total_return", "final_equity", "max_drawdown", "trades"):
            assert out[role]["in_sample"][key] == pytest.approx(in_sample[index][key], rel=1e-12)
            assert out[role]["out_of_sample"][key] == pytest.approx(oos[key], rel=1e-12)
        if s[cut - 1]:  # the holdout opens invested when the previous close said so
            assert oos["trades"] >= 1


@pytest.mark.parametrize("anchored", [False, True])
def test_walk_forward_stitched_account_is_rebuilt_independently(bars, grid, anchored):
    configs, signal_sets = grid
    settings = ValidationSpec(train_bars=252, test_bars=126, anchored=anchored)
    out = validation.walk_forward(bars, signal_sets, configs, 0, COSTS, settings)
    windows = validation.folds(len(bars), 252, 126, anchored)
    choices = []
    for row, (a, b, c, d) in zip(out["folds"], windows):
        in_sample = [manual(bars[a:b], s[a:b], prior=bool(a and s[a - 1])) for s in signal_sets]
        ranked = [-math.inf if m["sharpe"] is None else m["sharpe"] for m in in_sample]
        chosen = ranked.index(max(ranked))
        choices.append(chosen)
        assert row["chosen"] == chosen and row["params"] == configs[chosen]
        s = signal_sets[chosen]
        expected_sharpe = manual(bars[c:d], s[c:d], prior=bool(s[c - 1]))["sharpe"]
        if expected_sharpe is None:
            assert row["out_of_sample_sharpe"] is None
        else:
            assert row["out_of_sample_sharpe"] == pytest.approx(expected_sharpe, rel=1e-12)
    # The position held through bar t is the previous close's signal of the configuration
    # chosen for t's fold.
    position = [
        bool(signal_sets[chosen][t - 1])
        for (_, _, c, d), chosen in zip(windows, choices)
        for t in range(c, d)
    ]
    first, end = windows[0][2], windows[-1][3]
    stitched = manual(bars[first:end], position[1:] + [position[-1]], prior=position[0])
    aggregate = out["aggregate"]["out_of_sample"]
    for key in ("sharpe", "total_return", "final_equity", "max_drawdown", "trades"):
        assert aggregate[key] == pytest.approx(stitched[key], rel=1e-12)
    assert out["aggregate"]["distinct_choices"] == len(set(choices))


def test_single_configuration_walk_forward_equals_one_segment(bars, grid):
    signals = grid[1][2]
    settings = ValidationSpec(train_bars=252, test_bars=126)
    out = validation.walk_forward(bars, [signals], [{}], 0, COSTS, settings)
    assert out["status"] == "completed" and len(out["folds"]) == 4
    first, end = 252, 756
    segment = validation.subset(validation.segment(bars, signals, first, end, COSTS)["metrics"])
    assert out["aggregate"]["out_of_sample"] == segment
    assert out["aggregate"]["base_out_of_sample"] == segment
    direct = manual(bars[first:end], signals[first:end], prior=bool(signals[first - 1]))
    assert segment["sharpe"] == pytest.approx(direct["sharpe"], rel=1e-12)
    assert segment["final_equity"] == pytest.approx(direct["final_equity"], rel=1e-12)


def test_walk_forward_skip_reason_states_the_real_minimum(bars):
    settings = ValidationSpec(train_bars=252, test_bars=126)
    needed = 252 + 126 + 63
    short = bars[: needed - 1]
    out = validation.walk_forward(short, [[True] * len(short)], [{}], 0, COSTS, settings)
    assert out["status"] == "skipped"
    stated = int(re.search(r"at least (\d+) bars", out["reason"]).group(1))
    assert stated == needed > len(short)
    enough = validation.walk_forward(bars[:needed], [[True] * needed], [{}], 0, COSTS, settings)
    assert enough["status"] == "completed" and len(enough["folds"]) == 2


# 8. Transaction-cost stress


def at_level(bars, signals, level):
    # The configured split: 5 of 8 basis points are commission, 3 are slippage.
    return manual(bars, signals, commission=level * 5 / 8, slippage=level * 3 / 8)["sharpe"]


def test_cost_stress_is_monotone_and_its_break_even_brackets_zero():
    bars = generate(DatasetParams(seed=4))
    signals = crossover(bars, 20, 100)
    out = robustness.cost_stress(bars, signals, COSTS)
    assert [row["cost_bps"] for row in out["levels"]] == list(robustness.COST_LEVELS)
    sharpes = [row["sharpe"] for row in out["levels"]]
    assert all(b <= a for a, b in zip(sharpes, sharpes[1:]))
    for row in out["levels"]:
        assert row["sharpe"] == pytest.approx(at_level(bars, signals, row["cost_bps"]), rel=1e-12)
    be = out["break_even_bps"]
    assert 0 < be < robustness.BREAK_EVEN_CEILING
    assert at_level(bars, signals, be - 0.5) > 0 >= at_level(bars, signals, be + 0.5)
    assert out["current_bps"] == 8 and out["margin"] == pytest.approx(be / 8)


def test_cost_stress_reports_an_edge_beyond_the_ceiling():
    bars = generate(DatasetParams(seed=3, mu=0.25))
    signals = crossover(bars, 20, 100)
    out = robustness.cost_stress(bars, signals, COSTS)
    assert out["break_even_bps"] is None
    assert out["break_even_above"] == robustness.BREAK_EVEN_CEILING
    assert at_level(bars, signals, robustness.BREAK_EVEN_CEILING) > 0


def test_cost_stress_reasons_for_no_trades_and_no_edge(bars):
    idle = robustness.cost_stress(bars, [False] * len(bars), COSTS)
    assert idle["break_even_bps"] is None and "never trades" in idle["reason"]
    assert all(row["sharpe"] is None for row in idle["levels"])
    falling = generate(DatasetParams(seed=5, mu=-0.5))
    assert at_level(falling, [True] * len(falling), 0) < 0
    losing = robustness.cost_stress(falling, [True] * len(falling), COSTS)
    assert losing["break_even_bps"] is None
    assert "no positive excess return even before costs" in losing["reason"]


# 9. Parameter neighbourhoods and stability


def brute_neighbors(index, shape):
    coords = list(itertools.product(*(range(size) for size in shape)))  # row-major
    here = coords[index]
    return {j for j, c in enumerate(coords) if sum(abs(a - b) for a, b in zip(c, here)) == 1}


def test_neighbors_on_a_3_by_4_grid():
    shape = [3, 4]
    examples = {
        0: [1, 4],  # corners
        3: [2, 7],
        8: [4, 9],
        11: [7, 10],
        1: [0, 2, 5],  # edges
        4: [0, 5, 8],
        7: [3, 6, 11],
        5: [1, 4, 6, 9],  # interior
        6: [2, 5, 7, 10],
    }
    for index, expected in examples.items():
        assert sorted(robustness.neighbors(index, shape)) == expected
    sizes = Counter(len(robustness.neighbors(i, shape)) for i in range(12))
    assert sizes == {2: 4, 3: 6, 4: 2}
    for shape in ([3, 4], [5], [2, 3, 2], [1, 4], [1]):
        for index in range(math.prod(shape)):
            found = robustness.neighbors(index, shape)
            assert len(found) == len(set(found))
            assert set(found) == brute_neighbors(index, shape)
    assert robustness.neighbors(0, []) == []


def stability_of(centre, around):
    metrics = [{"sharpe": 0.0} for _ in range(9)]  # a 3 x 3 grid; the centre is index 4
    metrics[4]["sharpe"] = centre
    for index, value in zip((1, 3, 5, 7), around):
        metrics[index]["sharpe"] = value
    return robustness.stability(4, metrics, [3, 3])


@pytest.mark.parametrize(
    "centre,around,score,kind",
    [
        (1.0, [0.9, 0.8, 0.75, 1.4], 85, "robust"),  # median of 0.75, 0.8, 0.9, 1 (capped)
        (2.0, [1.4, 1.4, 1.4, 1.4], 70, "robust"),
        (1.0, [0.69, 0.69, 0.69, 0.69], 69, "sensitive"),
        (1.0, [None, None, 1.0, 1.0], 50, "sensitive"),  # an undefined neighbour keeps nothing
        (1.0, [0.4, 0.4, 0.4, 0.4], 40, "sensitive"),
        (1.0, [0.39, 0.39, 0.39, 0.39], 39, "fragile"),
        (1.0, [-1.0, -1.0, -1.0, 2.0], 0, "fragile"),  # losses clip to zero
    ],
)
def test_stability_classes(centre, around, score, kind):
    out = stability_of(centre, around)
    assert (out["score"], out["class"], out["neighbors"]) == (score, kind, 4)
    assert f"{score}%" in out["reason"]


def test_stability_without_an_edge_or_neighbours():
    for centre in (0.0, -0.3, None):
        out = stability_of(centre, [1.0, 1.0, 1.0, 1.0])
        assert (out["score"], out["class"]) == (None, "no-edge")
    alone = robustness.stability(0, [{"sharpe": 1.5}], [1])
    assert (alone["score"], alone["class"], alone["neighbors"]) == (None, "untested", 0)


# 10. Random timing


def test_random_timing_is_reproducible_and_bounded(bars):
    signals = crossover(bars, 20, 100)
    actual = evaluate(bars, signals, COSTS)["metrics"]["sharpe"]
    first = diagnostics.random_timing(bars, signals, COSTS, actual, 25, 123)
    again = diagnostics.random_timing(bars, signals, COSTS, actual, 25, 123)
    assert json.dumps(first, sort_keys=True) == json.dumps(again, sort_keys=True)
    assert first["status"] == "completed" and first["permutations"] == 25
    assert 1 / 26 <= first["p_value"] <= 1
    other = diagnostics.random_timing(bars, signals, COSTS, actual, 25, 124)
    assert other["null_median"] != first["null_median"]


def test_random_timing_with_every_shift_is_an_exact_permutation_test():
    bars = generate(DatasetParams(years=1, seed=8))
    n = len(bars)
    signals = crossover(bars, 10, 50)
    actual = manual(bars, signals)["sharpe"]
    assert actual is not None and 0 < sum(signals) < n
    null = []
    for shift in range(1, n):  # every circular shift, written out by hand
        value = manual(bars, signals[-shift:] + signals[:-shift])["sharpe"]
        null.append(-math.inf if value is None else value)
    p_value = (1 + sum(1 for v in null if v >= actual)) / n
    for seed in (1, 99):  # with every shift drawn, the seed cannot matter
        out = diagnostics.random_timing(bars, signals, COSTS, actual, 10 * n, seed)
        assert out["permutations"] == n - 1
        assert out["p_value"] == pytest.approx(p_value, rel=1e-12)
        assert out["percentile"] == pytest.approx(sum(1 for v in null if v < actual) / (n - 1))


def test_random_timing_skips():
    bars = generate(DatasetParams(years=1, seed=8))
    n = len(bars)
    signals = crossover(bars, 10, 50)
    for constant in ([True] * n, [False] * n):
        out = diagnostics.random_timing(bars, constant, COSTS, 0.5, 20, 1)
        assert out["status"] == "skipped" and "no timing" in out["reason"]
    assert diagnostics.random_timing(bars, signals, COSTS, 0.5, 0, 1)["status"] == "skipped"
    assert diagnostics.random_timing(bars, signals, COSTS, None, 20, 1)["status"] == "skipped"


# 11. Look-ahead through the pipeline

LOOKAHEAD = {
    "sample mean": 'from numpy import mean\ndef strategy(data):\n    return data["close"] > mean(data["close"])\n',
    "sample maximum": 'def strategy(data):\n    return data["close"] > max(data["close"]) * 0.8\n',
    "fails when shorter": """def strategy(data):
    if len(data["close"]) < 700:
        x = data["close"][100000]
    return data["close"] > data["sma_50"]
""",
}


@pytest.mark.parametrize("label", LOOKAHEAD)
def test_full_sample_statistics_fail_the_lookahead_test(label):
    results = execute(single(LOOKAHEAD[label]))
    look = results["lookahead"]
    assert look["status"] == "fail" and results["valid"] is False
    assert [c["bars"] for c in look["checks"]] == [252, 378, 567]
    if label == "fails when shorter":
        assert all(c["match"] is False and "IndexError" in c["error"] for c in look["checks"])
    else:
        assert any("first_difference" in c for c in look["checks"])
    check = next(c for c in results["redteam"]["checks"] if c["id"] == "lookahead")
    assert check["status"] == "fail" and "could not have had" in check["finding"]
    assert results["redteam"]["risk"]["level"] == "HIGH"
    json.dumps(results, allow_nan=False)


def test_default_crossover_passes_the_lookahead_test(default_run):
    _, results, _ = default_run
    look = results["lookahead"]
    assert look["status"] == "pass" and results["valid"] is True
    assert [(c["bars"], c["match"]) for c in look["checks"]] == [
        (252, True),
        (378, True),
        (567, True),
    ]
    check = next(c for c in results["redteam"]["checks"] if c["id"] == "lookahead")
    assert check["status"] == "pass"


# 12. Dataset integrity


def quality(bars):
    out = diagnostics.data_quality(bars)
    return {c["id"]: c["status"] for c in out["checks"]}, out["issues"]


def test_data_quality_catches_each_defect():
    clean = generate(DatasetParams(years=1, seed=3))
    statuses, issues = quality(clean)
    assert issues == 0 and set(statuses.values()) == {"pass"}

    def damaged(change):
        bars = copy.deepcopy(clean)
        change(bars)
        return quality(bars)

    def duplicate(bars):
        bars[6]["time"] = bars[5]["time"]

    def swap(bars):
        bars[10], bars[11] = bars[11], bars[10]

    def negative(bars):
        bars[20].update(open=-1.0, high=-1.0, low=-1.0, close=-1.0)

    def inverted(bars):
        bars[30]["high"] = bars[30]["low"] * 0.99

    def no_volume(bars):
        bars[40]["volume"] = 0
        del bars[41]["volume"]

    def gap(bars):
        bars[100]["time"] = "2030-01-01"
        for later in bars[101:]:
            later["time"] = "2030-" + later["time"][5:]

    cases = {
        # A repeated timestamp is a duplicate, not also an out-of-order bar.
        "duplicates": (duplicate, {"duplicates"}),
        "ordering": (swap, {"ordering"}),
        "prices": (negative, {"prices"}),
        "ohlc": (inverted, {"ohlc"}),
        "volume": (no_volume, {"volume"}),
        "gaps": (gap, {"gaps"}),
    }
    for label, (change, expected) in cases.items():
        statuses, issues = damaged(change)
        warned = {key for key, status in statuses.items() if status == "warn"}
        assert warned == expected, label
        assert issues == len(expected), label
    statuses, _ = damaged(negative)
    assert statuses["extreme"] == "info"  # a close of -1 after ~100 is also an extreme move


# 13. Determinism, serialization, templates and grid misuse


def test_pipeline_is_deterministic_and_json_safe(default_run):
    spec, first, calls = default_run
    json.dumps(first, allow_nan=False)
    second = execute(spec)
    assert provenance.digest(first) == provenance.digest(second)
    moved = spec.model_copy(update={"dataset": DatasetSpec(params=DatasetParams(seed=43))})
    assert provenance.digest(execute(moved)) != provenance.digest(first)
    # Progress: one tick per sandbox job (1 base + 3 cuts + 11 other configurations + 5
    # paths), then one per stage, ending at the total.
    total = 12 + 3 + 5 + 4
    assert calls[0] == ("strategies", 0, total) and calls[-1] == ("completed", total, total)
    assert [c for c in calls if c[0] == "strategies"][-1] == ("strategies", 20, total)
    stages = [stage for stage, _, _ in calls]
    assert list(dict.fromkeys(stages)) == [
        "strategies",
        "validation",
        "robustness",
        "diagnostics",
        "red team",
        "completed",
    ]
    assert all(b[1] >= a[1] for a, b in zip(calls, calls[1:]))


@pytest.mark.parametrize("template", TEMPLATES, ids=[t["id"] for t in TEMPLATES])
def test_every_template_runs_through_the_pipeline(template):
    spec = ExperimentSpec(
        strategy=StrategySpec(
            name=template["label"],
            code=template["code"],
            parameters=template["parameters"],
            base=template["base"],
        ),
        validation=ValidationSpec(permutations=20, seed_paths=1),
    )
    results = execute(spec)
    json.dumps(results, allow_nan=False)
    assert results["lookahead"]["status"] == "pass" and results["valid"] is True
    assert results["configurations"] == expand_grid(spec.strategy.parameters)
    assert results["validation"]["walk_forward"]["status"] == "completed"
    assert results["robustness"]["seeds"]["status"] == "completed"
    assert len(results["redteam"]["checks"]) == 12
    assert results["redteam"]["risk"]["level"] in {"LOW", "MEDIUM", "HIGH"}


def test_a_parameter_grid_needs_a_two_argument_strategy():
    spec = ExperimentSpec(
        strategy=StrategySpec(
            code='def strategy(data):\n    return data["close"] > data["sma_50"]\n'
        ),
        validation=ValidationSpec(permutations=0, seed_paths=0),
    )
    with pytest.raises(pipeline.StrategyFailure, match="ignores the parameter grid"):
        execute(spec)
    broken = spec.model_copy(
        update={
            "strategy": StrategySpec(
                code="def strategy(data, params):\n    while True:\n        pass\n"
            )
        }
    )
    with pytest.raises(pipeline.StrategyFailure, match="While is not supported"):
        execute(broken)


def test_grid_expansion_and_limits():
    grid = [
        GridParameter(name="fast", values=[10, 20]),
        GridParameter(name="slow", values=[100, 150, 200]),
    ]
    assert expand_grid(grid) == [
        {"fast": 10, "slow": 100},
        {"fast": 10, "slow": 150},
        {"fast": 10, "slow": 200},
        {"fast": 20, "slow": 100},
        {"fast": 20, "slow": 150},
        {"fast": 20, "slow": 200},
    ]
    assert expand_grid([]) == [{}]
    assert StrategySpec(code=CROSSOVER, parameters=grid, base={}).base == {"fast": 20, "slow": 150}
    widest = [{"name": "a", "values": list(range(6))}, {"name": "b", "values": list(range(10))}]
    assert (
        len(expand_grid(StrategySpec(parameters=widest, base={}).parameters)) == MAX_CONFIGURATIONS
    )
    too_wide = [{"name": "a", "values": list(range(7))}, {"name": "b", "values": list(range(9))}]
    with pytest.raises(ValidationError, match="limit is 60"):
        StrategySpec(parameters=too_wide, base={})
    for bad in ([1, 1], [float("nan")], [1e7]):
        with pytest.raises(ValidationError):
            GridParameter(name="a", values=bad)
    for base in ({"fast": 15}, {"other": 1}):
        with pytest.raises(ValidationError):
            StrategySpec(parameters=grid, base=base)


def test_evaluate_derives_its_metrics_from_the_backtest(bars):
    signals = crossover(bars, 20, 100)
    for prior in (False, True):
        out = evaluate(bars, signals, COSTS, prior_signal=prior)
        raw = backtest(bars, signals, CAPITAL, COMMISSION, SLIPPAGE, prior_signal=prior)
        curve = np.r_[CAPITAL, [p["equity"] for p in raw["equity_curve"]]]
        daily = curve[1:] / curve[:-1] - 1
        np.testing.assert_allclose(out["returns"], daily, rtol=1e-12)
        m = out["metrics"]
        assert m["volatility"] == pytest.approx(daily.std(ddof=1) * math.sqrt(252), rel=1e-12)
        sides = {t["time"]: t["side"] for t in raw["trades"]}
        holding, held = False, 0
        for bar in bars:  # a position is open from its BUY fill until its SELL fill
            holding = sides.get(bar["time"], "BUY" if holding else "SELL") == "BUY"
            held += holding
        assert m["exposure"] == pytest.approx(held / len(bars))
        traded = sum(t["price"] * t["quantity"] for t in raw["trades"])
        assert m["turnover"] == pytest.approx(traded / curve.mean() / (len(bars) / 252), rel=1e-12)
        assert m["round_trips"] == sum(1 for t in raw["trades"] if t["side"] == "SELL")
        assert m["sharpe"] == pytest.approx(
            per_period_sharpe(out["returns"]) * math.sqrt(PERIODS), rel=1e-12
        )
        years = yearly_pnl(raw, CAPITAL)
        assert [y["year"] for y in years] == sorted({b["time"][:4] for b in bars})
        assert sum(y["pnl"] for y in years) == pytest.approx(
            curve[-1] - CAPITAL, abs=0.01 * len(years)
        )
    sampled = downsample(raw["equity_curve"], 100)
    assert len(sampled) <= 100
    assert sampled[0] is raw["equity_curve"][0] and sampled[-1] is raw["equity_curve"][-1]
    assert [p["time"] for p in sampled] == sorted({p["time"] for p in sampled})
    assert downsample(raw["equity_curve"][:50], 100) == raw["equity_curve"][:50]


# 14. Red-team aggregation, research quality and provenance


def check(status, severity=None):
    return {"status": status, "severity": severity if status == "warn" else None}


@pytest.mark.parametrize(
    "items,level",
    [
        ([], "LOW"),
        ([check("pass"), check("skip"), check("pass")], "LOW"),
        ([check("pass"), check("warn", "medium")], "MEDIUM"),
        ([check("warn", "high")], "MEDIUM"),
        ([check("warn", "high"), check("warn", "high")], "HIGH"),
        ([check("warn", "medium")] * 4, "MEDIUM"),
        ([check("warn", "medium")] * 5, "HIGH"),
        ([check("fail")], "HIGH"),
        ([check("fail"), check("pass"), check("pass")], "HIGH"),
    ],
)
def test_red_team_risk_aggregation(items, level):
    out = redteam.risk(items)
    statuses = Counter(c["status"] for c in items)
    assert out == {
        "level": level,
        "passed": statuses["pass"],
        "warnings": statuses["warn"],
        "high": sum(1 for c in items if c["severity"] == "high"),
        "failed": statuses["fail"],
        "skipped": statuses["skip"],
    }


def test_research_quality_score_stays_within_bounds_and_rewards_the_process(default_run):
    _, results, _ = default_run
    notebooks = [
        {},
        {"hypothesis": "h"},
        {"hypothesis": "h", "conclusion": "c", "limitations": "l", "decision": "d"},
    ]
    reproductions = [
        None,
        {"verdict": "different"},
        {"verdict": "equivalent"},
        {"verdict": "identical"},
    ]
    scores = {}
    for i, notebook in enumerate(notebooks):
        for j, reproduction in enumerate(reproductions):
            out = redteam.quality(results, notebook, reproduction)
            assert 0 <= out["score"] <= 100
            assert all(0 <= c["score"] <= 100 for c in out["components"])
            assert sum(c["weight"] for c in out["components"]) == 100
            scores[i, j] = out["score"]
    assert scores[0, 3] < scores[1, 3] < scores[2, 3]
    assert scores[2, 0] == scores[2, 1] < scores[2, 2] < scores[2, 3]
    assert redteam.quality(None, {}, None) == {"score": None, "components": []}
    broken = copy.deepcopy(results)
    broken["lookahead"]["status"] = "fail"
    broken["dataset"]["quality"]["issues"] = 4
    bias = next(c for c in redteam.quality(broken, {}, None)["components"] if c["id"] == "bias")
    assert bias["score"] == 0  # clipped, never negative


def provenance_of(**changes):
    record = {
        "dataset": {"sha256": "d"},
        "strategy": {"sha256": "s"},
        "config_sha256": "c",
        "engine": {"sha256": "e"},
        "environment": {"sha256": "v"},
        "runtime": "3.14",
        "result_sha256": "r",
    }
    metrics = {"sharpe": 0.5, "cagr": 0.04, "trades": 10, "calmar": None}
    for key, value in changes.items():
        if key in metrics:
            metrics[key] = value
        elif key in ("dataset", "strategy", "engine", "environment"):
            record[key] = {"sha256": value}
        else:
            record[key] = value
    return {"provenance": record, "results": {"headline": {"metrics": metrics}}}


def test_canonical_json_and_digest():
    value = {"b": [1, 2.5, None], "a": {"y": "é", "x": True}}
    assert provenance.canonical(value) == '{"a":{"x":true,"y":"é"},"b":[1,2.5,null]}'.encode()
    assert provenance.digest(value) == hashlib.sha256(provenance.canonical(value)).hexdigest()
    assert provenance.digest({"x": 1, "y": 2}) == provenance.digest({"y": 2, "x": 1})
    assert provenance.digest(b"abc") == hashlib.sha256(b"abc").hexdigest()
    with pytest.raises(ValueError):
        provenance.canonical({"x": float("nan")})


def test_provenance_compare_verdicts():
    original = provenance_of()
    same = provenance.compare(original, provenance_of())
    assert same["verdict"] == "identical" and same["changed_inputs"] == []
    assert same["output_identical"] and same["metric_differences"] == []

    moved = provenance.compare(
        original, provenance_of(dataset="d2", result_sha256="r2", sharpe=0.7)
    )
    assert moved["verdict"] == "different" and moved["changed_inputs"] == ["Dataset"]
    assert moved["metric_differences"] == [{"metric": "sharpe", "original": 0.5, "rerun": 0.7}]
    assert moved["largest_relative_difference"] == pytest.approx(0.2 / 0.7)

    tiny = provenance.compare(
        original, provenance_of(environment="v2", result_sha256="r2", sharpe=0.5 * (1 + 1e-12))
    )
    assert tiny["verdict"] == "equivalent" and tiny["changed_inputs"] == ["Environment"]

    labels = {
        "strategy": "Strategy source",
        "config_sha256": "Configuration",
        "engine": "Research engine",
        "runtime": "Python runtime",
    }
    for key, label in labels.items():
        out = provenance.compare(
            original, provenance_of(**{key: "x", "result_sha256": "r2", "trades": 11})
        )
        assert out["verdict"] == "different" and out["changed_inputs"] == [label]
    # A different output with identical headline metrics is still not a reproduction.
    hidden = provenance.compare(original, provenance_of(result_sha256="r2"))
    assert hidden["verdict"] == "different" and hidden["metric_differences"] == []
    undefined = provenance.compare(original, provenance_of(result_sha256="r2", calmar=1.2))
    assert undefined["verdict"] == "different"


def test_every_red_team_lesson_link_exists_in_the_catalog():
    import json as _json
    from pathlib import Path as _Path

    from quanta.domain.research import redteam as _redteam

    catalog = _Path(__file__).resolve().parents[2] / "content/catalog/curriculum.json"
    lessons = {m["id"] for course in _json.loads(catalog.read_text()) for m in course["modules"]}
    assert set(_redteam.LESSONS.values()) <= lessons
