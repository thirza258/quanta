"""Golden arithmetic checks for the integrated, original course cases."""

import re

import pytest
from quanta.domain.catalog import LESSONS
from quanta.execution.runner import run


def worksheet(lesson_id):
    result = run(LESSONS[lesson_id]["code"], {"close": [100, 101, 99]})
    assert result["signals"] == [False, False, False]
    return result["stdout"]


def numbers(output, label):
    line = next(line for line in output.splitlines() if line.startswith(label + ":"))
    return [
        float(value)
        for value in re.findall(r"-?\d+(?:\.\d+)?(?:e[+-]?\d+)?", line.split(":", 1)[1])
    ]


def test_security_committee_reconciles_claims_and_conservative_price():
    output = worksheet("1.24")
    assert numbers(output, "Normalized coverage") == [4.0]
    assert numbers(output, "Weak coverage") == [2.4]
    assert numbers(output, "NCAV per share") == [5.0]
    assert numbers(output, "Adjusted realization") == [1.5]
    values = [
        float(line.split(":")[1])
        for line in output.splitlines()
        if line.startswith("Operating equity estimate:")
    ]
    assert values == [5.0, 8.0]
    assert numbers(output, "Maximum conservative price") == [3.5]


def test_quantitative_capstone_interval_and_cost_sensitivity():
    output = worksheet("2.28")
    assert numbers(output, "Mean active return (points)") == pytest.approx([0.225])
    assert numbers(output, "Sample standard deviation") == pytest.approx([0.8443663574])
    assert numbers(output, "t statistic") == pytest.approx([0.9230861185])
    assert numbers(output, "95% interval") == pytest.approx([-0.3114884057, 0.7614884057])
    assert numbers(output, "Mean with higher costs") == pytest.approx([0.025])
    assert "−0.311 to 0.761" in LESSONS["2.28"]["content"]


def test_tail_convention_and_compounded_cost_example():
    risk = worksheet("2.25")
    assert numbers(risk, "Nearest-rank 80% VaR") == [4]
    assert numbers(risk, "Worst-20% expected shortfall") == [9.5]
    backtest = worksheet("2.27")
    assert numbers(backtest, "Net terminal wealth") == [103.19]
    assert numbers(backtest, "Net arithmetic mean") == pytest.approx([0.008])


def test_probability_update_uses_base_rate():
    output = worksheet("2.9")
    assert numbers(output, "Warning probability") == pytest.approx([0.26])
    assert numbers(output, "Distress given warning") == pytest.approx([0.3076923077])
