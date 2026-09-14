"""Independent arithmetic checks for news interpretation and its capstone."""

import importlib.util
import re
import sys
from pathlib import Path

import pytest
from quanta.domain.catalog import CATALOG, LESSONS
from quanta.execution.runner import run


def worksheet(lesson_id):
    result = run(LESSONS[lesson_id]["code"], {"close": [100, 101, 99]})
    assert result["signals"] == [False, False, False]
    return result["stdout"]


def number(output, label):
    line = next(line for line in output.splitlines() if line.startswith(label + ":"))
    return float(re.search(r"-?\d+(?:\.\d+)?(?:e[+-]?\d+)?", line.split(":", 1)[1])[0])


@pytest.mark.parametrize(
    "lesson_id,label,expected",
    [
        ("8.4", "Year-over-year growth", 0.20),
        ("8.4", "Estimate surprise", -1 / 13),
        ("8.5", "New EBIT", 25),
        ("8.6", "Cash after capex", 5),
        ("8.12", "Unhedged cost increase (IDR billion)", 10),
        ("8.12", "Half-hedged total cost (IDR billion)", 155),
        ("8.15", "Expected cost", 12),
        ("8.18", "Cumulative abnormal return", 0),
        ("8.20", "Posterior recovery probability", 3 / 7),
        ("8.23", "Forecast score", 0.89 / 3),
    ],
)
def test_news_worksheet_arithmetic(lesson_id, label, expected):
    assert number(worksheet(lesson_id), label) == pytest.approx(expected)


def test_capstone_reconciles_business_cash_flows_financing_and_price():
    output = worksheet("8.24")
    expected = {
        "Base EBIT": 190,
        "Base FCFF": 112.5,
        "Base value per share": 11.0625,
        "Downside EBIT": 182,
        "Downside FCFF": 91.5,
        "Downside value per share": 43 / 6,
        "Conditional 25% margin threshold": 5.375,
    }
    for label, value in expected.items():
        assert number(output, label) == pytest.approx(value)


def test_downloaded_case_analysis_matches_the_teaching_packet():
    path = Path(__file__).resolve().parents[2] / "content/projects/news-to-markets/case_analysis.py"
    spec = importlib.util.spec_from_file_location("news_case_analysis", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    base = module.analyze(module.Scenario("Base", 20, 20, 0.10))
    downside = module.analyze(module.Scenario("Downside", 0, 35, 0.11))
    assert base["Value per share"] == pytest.approx(11.0625)
    assert downside["Value per share"] == pytest.approx(43 / 6)
    with pytest.raises(ValueError, match="exceed growth"):
        module.analyze(module.Scenario("Invalid", 20, 20, 0.02))


def test_news_course_follows_security_analysis_and_covers_every_unit():
    index = next(i for i, course in enumerate(CATALOG) if course["id"] == "security-analysis")
    news = CATALOG[index + 1]
    assert news["id"] == "news-to-markets"
    assert len(news["modules"]) == 24
    assert sum(lesson["minutes"] for lesson in news["modules"]) == 720
    assert len(news["exams"]) == 7
    assert {q["lessonId"] for exam in news["exams"][:-1] for q in exam["questions"]} == {
        lesson["id"] for lesson in news["modules"]
    }
