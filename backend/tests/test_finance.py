import json
import math
from pathlib import Path

import numpy as np
import pytest
from quanta.analytics import (
    AmmRequest,
    DatasetParams,
    ValuationRequest,
    amm,
    backtest,
    generate,
    strategy_data,
    summarize,
    valuation,
)
from quanta.broker import BrokerState, OrderRequest, place
from quanta.econometrics import FactorRequest, PortfolioRequest, factor_model, portfolio
from quanta.runner import ExecutionError, run


@pytest.mark.parametrize("model", ["gbm", "merton", "heston", "regime"])
def test_seeded_processes_valid_ohlc(model):
    params = DatasetParams(model=model, years=1, seed=12)
    bars = generate(params)
    assert bars == generate(params)
    assert bars != generate(params.model_copy(update={"seed": 13}))
    assert len(bars) == 252
    assert len({b["time"] for b in bars}) == 252
    for b in bars:
        assert 0 < b["low"] <= min(b["open"], b["close"]) <= max(b["open"], b["close"]) <= b["high"]
        assert b["volume"] > 0


@pytest.mark.parametrize(
    "scenario",
    [
        "1929_crash",
        "1970s_stagflation",
        "2008_liquidity_crisis",
        "flash_crash",
        "pure_random_walk",
    ],
)
def test_stress_scenarios_have_finite_prices(scenario):
    bars = generate(DatasetParams(scenario=scenario, years=2))
    assert all(math.isfinite(b["close"]) and b["close"] > 0 for b in bars)


def test_flash_crash_is_exact_same_seed_counterfactual():
    params = DatasetParams(years=1)
    base = generate(params)
    crash = generate(params.model_copy(update={"scenario": "flash_crash"}))
    assert crash[125]["close"] == base[125]["close"]
    assert crash[126]["close"] == pytest.approx(base[126]["close"] / 2)


def test_gbm_log_returns_mean_and_variance():
    p = DatasetParams(years=30, sigma=0.2, mu=0.08, seed=9)
    returns = np.diff(np.log([100] + [b["close"] for b in generate(p)]))
    assert returns.std() == pytest.approx(0.2 / math.sqrt(252), rel=0.04)
    assert returns.mean() == pytest.approx((0.08 - 0.2**2 / 2) / 252, abs=0.0004)


def test_execution_uses_next_open_not_current_bar():
    bars = [
        {"time": "2020-01-02", "open": 100, "close": 200},
        {"time": "2020-01-03", "open": 220, "close": 220},
        {"time": "2020-01-06", "open": 110, "close": 110},
    ]
    out = backtest(bars, [True, False, True], 1000, 0, 0)
    assert out["trades"][0]["time"] == "2020-01-03"
    assert out["trades"][0]["price"] == 220
    assert out["equity_curve"][0]["equity"] == 1000
    assert out["metrics"]["final_equity"] == pytest.approx(500)
    assert out["metrics"]["max_drawdown"] == pytest.approx(-0.5)
    assert out["metrics"]["win_rate"] == 0


def test_costs_reduce_equity_and_cash_only_ratios_undefined():
    bars = generate(DatasetParams(years=1))
    gross = backtest(bars, [True] * 252, 100000, 0, 0)
    net = backtest(bars, [True] * 252, 100000, 20, 20)
    assert net["metrics"]["final_equity"] < gross["metrics"]["final_equity"]
    cash = backtest(bars, [False] * 252, 100000, 5, 3)
    assert cash["metrics"]["total_return"] == 0
    assert cash["metrics"]["sharpe"] is None
    assert cash["metrics"]["win_rate"] is None
    assert cash["trades"] == []


def test_first_loss_counts_in_drawdown_and_monthly_return():
    metrics = summarize([900, 990], [1000, 1100], [], 1000)
    assert metrics["max_drawdown"] == pytest.approx(-0.1)
    bars = [
        {"time": "2020-01-02", "open": 100, "close": 100},
        {"time": "2020-02-03", "open": 100, "close": 90},
    ]
    out = backtest(bars, [True, True], 1000, 0, 0)
    assert out["monthly_returns"][0]["return"] == 0
    assert out["monthly_returns"][1]["return"] == pytest.approx(-0.1)


def test_textbook_valuation():
    out = valuation(ValuationRequest())
    assert out["ncav"] == 11
    assert out["adjusted_ncav"] == pytest.approx(6.9)
    assert out["screen_price"] == pytest.approx(22 / 3)
    assert out["graham_value"] == 74
    assert out["passes_screen"]


def test_amm_invariant_fees_il_and_range_boundaries():
    out = amm(AmmRequest(fee=0))
    assert out["output"] == pytest.approx(20000 / 11)
    assert out["reserves_after"]["x"] * out["reserves_after"]["y"] == pytest.approx(200000)
    assert out["impermanent_loss"] == pytest.approx(2 * math.sqrt(2) / 3 - 1)
    fee = amm(AmmRequest())
    assert fee["reserves_after"]["x"] * fee["reserves_after"]["y"] > 200000
    flat = amm(AmmRequest(price_ratio=1))
    assert flat["impermanent_loss"] == 0
    assert flat["concentrated_loss"] == pytest.approx(0)
    assert not amm(AmmRequest(price_ratio=4))["in_range"]


def test_paper_broker_partial_fill_fees_and_risk_guards():
    out = place(OrderRequest(quantity=150, volume=1000))
    assert out["status"] == "partially_filled"
    assert out["filled"] == 100
    assert out["remaining"] == 50
    assert out["state"]["quantity"] == 100
    assert out["state"]["cash"] == pytest.approx(100000 - 100 * out["price"] - out["commission"])
    assert place(OrderRequest(side="sell"))["status"] == "rejected"
    assert place(OrderRequest(data_age_seconds=61))["reason"] == "Price data is stale."
    assert place(OrderRequest(spread_bps=101))["status"] == "rejected"
    assert place(OrderRequest(state=BrokerState(cash=97000)))["state"]["halted"]
    assert place(OrderRequest(state=BrokerState(halted=True)))["status"] == "rejected"


def test_factor_recovery_and_time_split():
    result = factor_model(FactorRequest(model="ff5", observations=5000, noise=0.001))
    betas = [r["coefficient"] for r in result["coefficients"]]
    assert betas[1:] == pytest.approx([1.1, 0.25, 0.4, 0.15, -0.1], abs=0.01)
    assert result["r_squared"] > 0.98
    assert result["ridge_oos_r_squared"] > 0.95
    assert result["train_observations"] == 3750
    with pytest.raises(ValueError):
        factor_model(FactorRequest(rows=[[0.01, 0.02, 0.02, 0.02]] * 100))


def test_portfolio_constraints():
    rng = np.random.default_rng(23)
    data = rng.normal(0, [0.01, 0.02, 0.03], (500, 3)).tolist()
    result = portfolio(PortfolioRequest(returns=data, max_weight=0.5))
    assert sum(result["weights"]) == pytest.approx(1)
    assert all(-1e-8 <= w <= 0.500001 for w in result["weights"])
    assert result["volatility"] > 0


CATALOG = json.loads((Path(__file__).resolve().parents[2] / "src/data/curriculum.json").read_text())
LESSONS = [m for t in CATALOG for m in t["modules"]]


@pytest.mark.parametrize("lesson", LESSONS, ids=[lesson["id"] for lesson in LESSONS])
def test_every_lesson_template_runs(lesson):
    bars = generate(DatasetParams(years=1))
    result = run(lesson["code"], strategy_data(bars, 50))
    assert len(result["signals"]) == 252
    assert all(type(x) is bool for x in result["signals"])


@pytest.mark.parametrize(
    "code",
    [
        "import os\ndef strategy(data): return True",
        "import socket\ndef strategy(data): return True",
        "x = (1).__class__\ndef strategy(data): return True",
        'x = open("/etc/passwd")\ndef strategy(data): return True',
        "while True: pass\ndef strategy(data): return True",
        'x = "a" * 1000000000\ndef strategy(data): return True',
        "x = 10 ** 1000000\ndef strategy(data): return True",
        "x = list(range(1000000000))\ndef strategy(data): return True",
        "def strategy(data): return [1,2,3]",
        'def strategy(data): return data["close"]',
    ],
)
def test_unsafe_or_invalid_python_fails_closed(code):
    with pytest.raises(ExecutionError):
        run(code, {"close": [100, 101]})


def test_computation_budget_and_vector_operations():
    code = "import numpy as np\nprint(np.mean(data))"  # undefined data at module scope
    with pytest.raises(ExecutionError):
        run(code, {"close": [100, 101]})
    out = run(
        'import numpy as np\ndef strategy(data):\n    return np.where(data["close"] > 100, True, False)',
        {"close": [99, 101]},
    )
    assert out["signals"] == [False, True]
    with pytest.raises(ExecutionError):
        run(
            "for i in range(10000):\n    for j in range(10000):\n        a = i + j\ndef strategy(data): return True",
            {"close": [1, 2]},
        )
