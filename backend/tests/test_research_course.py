"""Independent numerical and timing invariants for the downloadable research lab."""

import importlib.util
from pathlib import Path

import numpy as np
import pytest

path = Path(__file__).resolve().parents[2] / "public/course-assets/research/quant_research_lab.py"
spec = importlib.util.spec_from_file_location("research_lab", path)
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


def test_ols_coefficients_and_hac_do_not_use_heldout_outcomes():
    rows = lab.sample_factors()
    result = lab.factor_research(rows)
    design = np.column_stack([np.ones(270), rows[:270, 1:]])
    expected = np.linalg.lstsq(design, rows[:270, 0], rcond=None)[0]
    assert result["coefficients"] == pytest.approx(expected)
    altered = rows.copy()
    altered[270:, 0] += 1
    changed = lab.factor_research(altered)
    for name in ["coefficients", "classical_se", "hac_se", "prediction"]:
        assert changed[name] == result[name]
    assert changed["mse"] > result["mse"]
    assert not np.allclose(result["classical_se"], result["hac_se"])


def test_cointegration_reports_a_diagnostic_with_finite_inference():
    result = lab.cointegration_research()
    assert result["null"] == "no cointegration"
    assert np.isfinite(result["statistic"])
    assert 0 <= result["p_value"] <= 1
    assert 1.3 < result["hedge_slope"] < 1.7
    assert result["estimated_spread_ar"]["half_life"] > 0


def test_garch_forecast_precedes_its_innovation_and_covariance_math():
    assert lab.garch_variances([0.3, -0.2, 0.1], 0.01, 0.1, 0.8, 0.04) == pytest.approx(
        [0.04, 0.051, 0.0548]
    )
    assert lab.garch_variances([99], 0.01, 0.1, 0.8, 0.04) == [0.04]
    with pytest.raises(ValueError):
        lab.garch_variances([0.1], 0.01, 0.2, 0.8, 0.04)
    result = lab.covariance_review()
    assert result["sample_variance"] == pytest.approx(0.0415)
    assert result["shrunk_variance"] == pytest.approx(0.037)
    assert result["stress_volatility"] == pytest.approx(0.25)


def test_irregular_label_purging_removes_early_overlapping_target():
    ends = [2, 3, 4, 5, 9, 7, 8, 10, 10, 11, 12, 13]
    fold = lab.purged_forward_splits(ends, [8])[0]
    assert fold["train"] == [0, 1, 2, 3, 5]
    assert fold["test"] == [8, 9, 10]
    assert all(ends[i] < 8 for i in fold["train"])


def test_price_time_queue_partial_fill_and_limit():
    asks = [
        {"id": "expensive", "price": 101, "quantity": 10},
        {"id": "early", "price": 100, "quantity": 3},
        {"id": "later", "price": 100, "quantity": 4},
    ]
    result = lab.match_asks(asks, 10, 100)
    assert result["fills"] == [
        {"order_id": "early", "quantity": 3, "price": 100},
        {"order_id": "later", "quantity": 4, "price": 100},
    ]
    assert result["unfilled"] == 3
    assert result["vwap"] == 100
    assert lab.match_asks(asks, 10, 101)["vwap"] == pytest.approx(100.3)


def test_ranked_universe_cap_and_cash_residual():
    result = lab.rank_targets({"A": 0.1, "B": 0.2, "C": 0.9}, ["A", "B"])
    assert result["weights"] == {"B": 0.4, "A": 0.4}
    assert result["cash_weight"] == pytest.approx(0.2)
    assert lab.rank_targets({"A": 0.1}, ["A"])["cash_weight"] == pytest.approx(0.6)
    assert lab.rank_targets({"A": 0.1}, [])["cash_weight"] == 1


def test_next_open_execution_and_constant_price_cost_conservation():
    result = lab.lagged_backtest([[100], [110], [120]], [[1], [0]], fee_bps=0, capital=1100)
    assert result["equity"] == 1200
    assert result["trace"][0]["shares"] == [10]
    assert result["trace"][0]["execution"] == 1
    rotation = lab.lagged_backtest([[10, 20]] * 4, [[1, 0], [0, 1], [0, 0]], fee_bps=10)
    assert rotation["equity"] == pytest.approx(10000 - rotation["fees"])
    assert all(event["cash"] >= -1e-8 for event in rotation["trace"])
    assert rotation["trace"][-1]["shares"] == pytest.approx([0, 0])
    with pytest.raises(ValueError):
        lab.lagged_backtest([[10], [0]], [[1]])


def test_evidence_scoring_preserves_undefined_denominators():
    score = lab.evidence_scores(["a", "b", "c", "d"], ["a", "a", "b", "fake"])
    assert score["precision"] == pytest.approx(2 / 3)
    assert score["recall"] == 0.5
    assert lab.evidence_scores(["a"], [])["precision"] is None
    assert lab.evidence_scores([], [])["recall"] is None
