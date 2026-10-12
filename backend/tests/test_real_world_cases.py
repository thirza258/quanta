"""Coverage and authoring regressions for sourced lesson applications."""

import importlib
from copy import deepcopy
from pathlib import Path
from urllib.parse import urlparse

import pytest

from quanta.domain.catalog import CATALOG, LESSONS


@pytest.mark.parametrize("course", CATALOG, ids=lambda course: course["id"])
def test_every_lesson_and_unit_has_a_sourced_specific_application(course):
    cases = {item["id"]: item for item in course["caseStudies"]}
    assert len(cases) == len(course["caseStudies"])
    assert set(cases) == {lesson["realWorld"]["caseId"] for lesson in course["modules"]}
    for lesson in course["modules"]:
        application = lesson["realWorld"]
        case = cases[application["caseId"]]
        assert all(application[key].strip() for key in ("connection", "task", "walkthrough"))
        assert case["kind"] in {"documented", "implementation", "illustrative"}
        assert case["context"] and case["setting"] and case["period"] and case["boundary"]
        assert case["references"]
        for reference in case["references"]:
            parsed = urlparse(reference["url"])
            assert parsed.scheme == "https" and parsed.netloc
            assert reference["scope"].strip()
            # Existing bibliography labels may differ; the source's URL is its identity.
            assert reference["url"] in {ref["url"] for ref in lesson["references"]}
            assert reference["url"] in {ref["url"] for ref in course["references"]}
        for item in (lesson, course):
            urls = [ref["url"] for ref in item["references"]]
            assert len(urls) == len(set(urls))
    for part in course.get("parts", []):
        modules = [lesson for lesson in course["modules"] if lesson.get("part") == part["id"]]
        assert modules and all(lesson["realWorld"]["caseId"] in cases for lesson in modules)


def test_applications_are_individual_and_mix_local_context_with_global_methods():
    applications = [lesson["realWorld"] for lesson in LESSONS.values()]
    assert len(applications) == 340
    for key in ("connection", "task", "walkthrough"):
        assert len({application[key] for application in applications}) == len(applications)
    cases = {item["id"]: item for course in CATALOG for item in course["caseStudies"]}
    assert len(cases) == 35
    assert {"bca_split", "bi_rate", "bps_growth", "ojk_scam", "warung", "household"} <= cases.keys()
    assert {"knight", "svb", "bitcoin", "ml_pipeline", "gpu", "reporting"} <= cases.keys()
    assert "5 February 2025" in cases["bps_growth"]["period"]
    assert "not today's" in cases["bi_rate"]["context"]
    assert "not establish GIPS compliance" in cases["reporting"]["context"]


@pytest.fixture
def authoring(monkeypatch):
    root = Path(__file__).resolve().parents[2]
    monkeypatch.syspath_prepend(str(root / "content/authoring"))
    return importlib.import_module("real_world_cases")


@pytest.mark.parametrize("fault,match", [
    ("missing", "coverage mismatch"),
    ("duplicate", "Duplicate real-world"),
    ("unknown", "Unknown case"),
    ("empty", "Incomplete real-world"),
])
def test_builder_rejects_incomplete_or_ambiguous_authorship(authoring, monkeypatch, fault, match):
    investing = importlib.import_module("case_applications_investing")
    rows = deepcopy(investing.APPLICATIONS)
    if fault == "missing":
        rows.pop()
    elif fault == "duplicate":
        rows.append(rows[0])
    else:
        row = list(rows[0])
        row[1 if fault == "unknown" else 3] = "missing-case" if fault == "unknown" else " "
        rows[0] = tuple(row)
    monkeypatch.setattr(investing, "APPLICATIONS", rows)
    with pytest.raises(ValueError, match=match):
        authoring.attach_real_world_cases(deepcopy(CATALOG))


def test_regeneration_does_not_duplicate_references_or_change_existing_content(authoring):
    rebuilt = deepcopy(CATALOG)
    authoring.attach_real_world_cases(rebuilt)
    assert rebuilt == CATALOG


def test_split_walkthrough_uses_ownership_value_instead_of_raw_price_change():
    # Independently solve the quantities stated in the learner-facing task.
    application = LESSONS["2.7"]["realWorld"]
    assert "100 shares at 50" in application["task"]
    assert "500 at 10.2" in application["task"]
    ownership_return = (500 * 10.2) / (100 * 50) - 1
    raw_price_loss = 1 - 10.2 / 50
    assert ownership_return == pytest.approx(0.02)
    assert f"{ownership_return:.0%} return" in application["walkthrough"]
    assert f"{raw_price_loss:.1%} loss" in application["walkthrough"]


def test_pool_walkthrough_uses_constant_product_output_not_the_spot_ratio():
    application = LESSONS["6.2"]["realWorld"]
    assert "100 units of A and 10,000 of B" in application["task"]
    assert "Add 10 A" in application["task"]
    output = 10_000 - 100 * 10_000 / (100 + 10)
    assert f"{output:.2f} B" in application["walkthrough"]
    assert f"{output / 10:.2f} B per A" in application["walkthrough"]


def test_cash_flow_walkthrough_does_not_call_a_deposit_a_return():
    application = LESSONS["10.4"]["realWorld"]
    assert "starts at 100" in application["task"] and "contribution of 50" in application["task"]
    assert "finishes at 160" in application["task"]
    performance = (160 - 50) / 100 - 1
    assert f"pre-flow return is {performance:.0%}" in application["walkthrough"]
