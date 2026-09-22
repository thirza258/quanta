"""Course arithmetic, source archive behavior, and reporting interoperability."""

import json
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

import pytest
from quanta.domain.catalog import CATALOG, LESSONS
from quanta.execution.runner import run

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    "lesson_id,expected",
    [
        ("4.1", {"Raw NCAV": 11, "Adjusted screen ceiling": 4.4}),
        ("4.28", {"Cash after buy": 798, "Round-trip final equity": 1015.8, "Total fees": 4.2}),
        (
            "4.32",
            {
                "Round-trip final equity": 1015.8,
                "Strategy rubric total": 100,
                "Planned study hours": 16,
            },
        ),
        ("11.8", {"Conservative margin": 1 / 7, "Maximum price under the fictional rule": 52.5}),
        ("11.10", {"Drifted equity weight": 9 / 14, "Equity sale before costs": 4.8}),
        (
            "11.16",
            {
                "Long-horizon capital": 66,
                "Case maximum price": 52.5,
                "Investor plan rubric total": 100,
            },
        ),
    ],
)
def test_original_worksheets_match_independent_arithmetic(lesson_id, expected):
    result = run(LESSONS[lesson_id]["code"], {"close": [100, 102, 98]})
    assert result["signals"] == [False, False, False]
    values = dict(line.split(": ", 1) for line in result["stdout"].splitlines())
    for label, value in expected.items():
        assert float(values[label]) == pytest.approx(value)


def test_order_and_legacy_strategy_subjects():
    assert [c["id"] for c in CATALOG[:5]] == [
        "trading-fundamentals",
        "trading-ethics",
        "intelligent-investor",
        "security-analysis",
        "news-to-markets",
    ]
    assert CATALOG[-1]["id"] == "algorithm-evaluation"
    for id, answer in [("4.1", 1), ("4.2", 1), ("4.3", 1), ("4.4", 2)]:
        assert LESSONS[id]["exercises"][0] == LESSONS[id]["exercise"]
        assert LESSONS[id]["exercise"]["answer"] == answer


def test_downloaded_strategy_lab_and_reporting_contract(tmp_path):
    with ZipFile(
        ROOT / "frontend/public/course-assets/strategy-lab/strategy-research-lab.zip"
    ) as bundle:
        bundle.extractall(tmp_path)
    tests = subprocess.run(
        [sys.executable, "-m", "unittest", "-v"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert tests.returncode == 0, tests.stdout + tests.stderr
    assert "Ran 11 tests" in tests.stderr
    command = [sys.executable, "strategy_lab.py"]
    result = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stderr
    output = tmp_path / "strategy-output"
    ledger = json.loads((output / "experiments.json").read_text())
    assert len(ledger["validation_trials"]) == 3
    assert len(ledger["post_selection_stresses"]) == 2
    winner = max(ledger["validation_trials"], key=lambda row: row["metrics"]["total_return"])
    assert ledger["selected_strategy"] == winner["strategy"]
    original = (output / "experiments.json").read_bytes()
    duplicate = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True, timeout=15)
    assert duplicate.returncode == 2
    assert "new or empty" in duplicate.stderr
    assert (output / "experiments.json").read_bytes() == original
    report = subprocess.run(
        [
            sys.executable,
            str(ROOT / "content/projects/algorithm-evaluation/evaluate.py"),
            "--equity",
            str(output / "test/equity.csv"),
            "--manifest",
            str(output / "test/manifest.json"),
            "--out",
            str(tmp_path / "report"),
            "--no-charts",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert report.returncode == 0, report.stderr
    metrics = json.loads((tmp_path / "report/metrics.json").read_text())
    assert metrics["metrics"]["total_return"] == pytest.approx(
        ledger["selected_test"]["total_return"]
    )
    assert metrics["metrics"]["maximum_drawdown"] == pytest.approx(
        ledger["selected_test"]["maximum_drawdown"]
    )
    assert (tmp_path / "report/report.html").is_file()
