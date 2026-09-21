"""The trading-ethics course: structure, sourcing, and the limits it states."""

from pathlib import Path

from quanta.domain.catalog import CATALOG

COURSE = next(course for course in CATALOG if course["id"] == "trading-ethics")
LESSONS = COURSE["modules"]


def test_conduct_is_taught_before_valuation_and_automation():
    order = [course["id"] for course in CATALOG]
    assert order.index("trading-ethics") == order.index("trading-fundamentals") + 1
    assert order.index("trading-ethics") < order.index("security-analysis")
    assert order.index("trading-ethics") < order.index("stock-bots")
    assert COURSE["number"] == 12
    assert [lesson["id"] for lesson in LESSONS] == [f"12.{i}" for i in range(1, 17)]
    assert len(COURSE["parts"]) == 4
    assert sum(lesson["minutes"] for lesson in LESSONS) == 480


def test_every_lesson_states_a_checkable_rule_and_names_its_sources():
    for lesson in LESSONS:
        assert "### Do and do not" in lesson["content"]
        assert "- **Do not**" in lesson["content"]
        assert "Add it to your charter" in lesson["content"]
        assert len(lesson["content"].split()) > 250
        assert len(lesson["references"]) >= 2
        assert all(ref["url"].startswith("https://") for ref in lesson["references"])
        assert all(len(ref["title"]) > 10 for ref in lesson["references"])
        assert len(lesson["exercises"]) == 2
        assert lesson["assignment"]["prompt"] and lesson["assignment"]["solution"]
        assert lesson["formula"] and lesson["code"]


def test_the_course_says_plainly_that_it_is_not_advice():
    assert "not legal or compliance advice" in COURSE["prerequisites"]
    assert "jurisdiction" in COURSE["readingGuide"]
    assert "invented" in COURSE["readingGuide"]
    for lesson in LESSONS:
        # Each reading note repeats the boundary, because lessons are read alone.
        assert "invented" in lesson["reading"]
        assert "not legal, compliance or investment advice" in lesson["reading"]


def test_each_lesson_reuses_a_sourced_case_anchor():
    anchors = {case["id"]: case for case in COURSE["caseStudies"]}
    assert len(anchors) == 16
    for lesson in LESSONS:
        case = lesson["realWorld"]
        assert case["caseId"] in anchors
        assert case["connection"] and case["task"] and case["walkthrough"]
        anchor = anchors[case["caseId"]]
        assert anchor["boundary"]
        assert anchor["references"] and all(ref["scope"] for ref in anchor["references"])


def test_assessments_are_complete_and_distinct():
    checkpoints = [exam for exam in COURSE["exams"] if exam["kind"] == "checkpoint"]
    final = next(exam for exam in COURSE["exams"] if exam["kind"] == "final")
    assert len(checkpoints) == 4 and len(final["questions"]) == 16
    assert final["moduleIds"] == [lesson["id"] for lesson in LESSONS]
    for index, checkpoint in enumerate(checkpoints):
        assert checkpoint["moduleIds"] == [
            lesson["id"] for lesson in LESSONS[index * 4 : index * 4 + 4]
        ]
        assert len(checkpoint["questions"]) == 4
    prompts = [q["question"] for exam in COURSE["exams"] for q in exam["questions"]]
    prompts += [q["question"] for lesson in LESSONS for q in lesson["exercises"]]
    assert len(prompts) == 64 and len(set(prompts)) == 64
    for exam in COURSE["exams"]:
        for question in exam["questions"]:
            assert 0 <= question["answer"] < len(question["options"])
            assert len(set(question["options"])) == len(question["options"])


def test_the_authoring_module_cites_only_primary_sources():
    source = (
        Path(__file__).resolve().parents[2] / "content/authoring/trading_ethics.py"
    ).read_text(encoding="utf-8")
    for host in (
        "cfainstitute.org",
        "sec.gov",
        "finra.org",
        "esma.europa.eu",
        "gipsstandards.org",
        "investor.gov",
    ):
        assert host in source
    assert "http://" not in source
