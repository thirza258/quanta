"""Compile actual learner downloads; check causal arithmetic and parallel execution."""

import shutil
import subprocess
from pathlib import Path
from zipfile import ZipFile

import pytest
from quanta.domain.catalog import CATALOG

ROOT = Path(__file__).resolve().parents[2]
COURSE = next(track for track in CATALOG if track["id"] == "c-hpc-trading")


def command(args, cwd):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


@pytest.fixture(scope="module")
def compiler():
    cc = shutil.which("cc")
    assert cc, "Install a C17 compiler (cc) to verify the C/HPC course."
    return cc


@pytest.mark.parametrize("lesson", COURSE["modules"], ids=lambda lesson: lesson["id"])
def test_every_c_worksheet_compiles_and_reproduces_its_expected_result(lesson, compiler, tmp_path):
    (tmp_path / "lesson.c").write_text(lesson["code"])
    command(
        [
            compiler,
            "-std=c17",
            "-Wall",
            "-Wextra",
            "-Werror",
            "-pedantic",
            "-O2",
            "lesson.c",
            "-o",
            "lesson",
        ],
        tmp_path,
    )
    assert lesson["expectedOutput"] in command([str(tmp_path / "lesson")], tmp_path)


@pytest.fixture(scope="module")
def project(tmp_path_factory, compiler):
    target = tmp_path_factory.mktemp("c-hpc-download")
    with ZipFile(ROOT / "frontend/public/course-assets/c-hpc-trading/c-hpc-bot-lab.zip") as archive:
        archive.extractall(target)
    command(["make", f"CC={compiler}", "all", "quanta-test"], target)
    return target


def test_downloaded_project_checks_causal_ledger_and_all_worker_counts(project):
    output = command([str(project / "quanta-test")], project)
    assert "PASS: ledger" in output
    assert "parallel equality and atomic publication" in output
    output = command([str(project / "quanta-bot"), "4", "2000"], project)
    assert output.count("equal=yes") == 5
    rows = output.split("window,equity_cents,fills\n")[1].strip().splitlines()
    assert len(rows) == 64
    # Fixed seeded fixture independent of elapsed-time noise.
    assert rows[0] == "2,994843,1011"
    assert [int(row.split(",")[0]) for row in rows] == list(range(2, 66))


def test_invalid_cli_values_fail_without_starting_a_benchmark(project):
    for args in (
        ["0"],
        ["33"],
        ["-1"],
        ["4oops"],
        ["4", "64"],
        ["4", "1000001"],
        ["4", "99999999999999999999999999"],
    ):
        result = subprocess.run(
            [str(project / "quanta-bot"), *args],
            cwd=project,
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 2
        assert "Usage:" in result.stderr
        assert "repeat=" not in result.stdout


def test_c_course_covers_all_units_and_follows_python_bots():
    index = next(i for i, track in enumerate(CATALOG) if track["id"] == "stock-bots")
    assert CATALOG[index + 1] == COURSE
    assert len(COURSE["modules"]) == 24
    assert len(COURSE["exams"]) == 7
    assert {
        question["lessonId"] for exam in COURSE["exams"][:-1] for question in exam["questions"]
    } == {lesson["id"] for lesson in COURSE["modules"]}
