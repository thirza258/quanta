"""Independent course arithmetic and tests from the actual downloadable reporting lab."""

import json
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

import pytest
from quanta.domain.catalog import CATALOG, LESSONS
from quanta.execution.runner import run

ROOT = Path(__file__).resolve().parents[2]


def test_reporting_course_closes_the_catalog_with_complete_unit_coverage():
    course = CATALOG[-1]
    assert course["id"] == "algorithm-evaluation"
    assert len(course["modules"]) == 16
    assert len(course["exams"]) == 5
    assert sum(lesson["minutes"] for lesson in course["modules"]) == 480
    assert {q["lessonId"] for exam in course["exams"][:-1] for q in exam["questions"]} == {
        lesson["id"] for lesson in course["modules"]
    }


def test_reporting_capstone_matches_the_independent_wealth_fixture():
    result = run(LESSONS["10.16"]["code"], {"close": [100, 101, 99]})
    assert result["signals"] == [False, False, False]
    values = dict(line.split(": ", 1) for line in result["stdout"].splitlines())
    assert float(values["Strategy total return"]) == pytest.approx(0.10)
    assert float(values["Benchmark total return"]) == pytest.approx(0.08)
    assert float(values["Maximum drawdown"]) == pytest.approx(1 / 15)
    assert float(values["Report rubric total"]) == 100


def test_downloaded_reporting_project_validates_metrics_inputs_and_exports(tmp_path):
    archive = ROOT / "frontend/public/course-assets/algorithm-evaluation/algorithm-report-lab.zip"
    with ZipFile(archive) as bundle:
        bundle.extractall(tmp_path)
    tests = subprocess.run(
        [sys.executable, "-m", "unittest", "-v"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert tests.returncode == 0, tests.stdout + tests.stderr
    assert "Ran 9 tests" in tests.stderr
    result = subprocess.run(
        [sys.executable, "evaluate.py", "--timings", "timings.example.csv", "--no-charts"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads((tmp_path / "report-output/metrics.json").read_text())
    assert report["metrics"]["total_return"] == pytest.approx(0.1)
    assert report["metrics"]["maximum_drawdown"] == pytest.approx(1 / 15)
    assert report["timings"]["median_paired_speedup"] == 3
    assert len(report["sha256"]["evaluator"]) == 64
