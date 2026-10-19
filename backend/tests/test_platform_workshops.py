"""The two tool workshops: placement, structure, working links and runnable worksheets."""

import re

import pytest
from quanta.domain.catalog import CATALOG
from quanta.execution.runner import run
from quanta.services.simulator_missions import MISSIONS

COURSES = {course["id"]: course for course in CATALOG}
LAB_TOOLS = {"market", "valuation", "factors", "broker", "amm"}


def test_workshops_follow_the_conduct_course_in_the_learning_sequence():
    order = [course["id"] for course in CATALOG]
    assert order.index("trading-ethics") + 1 == order.index("simulator-workshop")
    assert order.index("simulator-workshop") + 1 == order.index("lab-workshop")


@pytest.mark.parametrize(
    "course_id,prefix,lessons", [("simulator-workshop", "13", 16), ("lab-workshop", "14", 12)]
)
def test_each_workshop_is_a_complete_applied_course(course_id, prefix, lessons):
    course = COURSES[course_id]
    assert course["studyType"] == "applied"
    # Units of four lessons, a checkpoint each, one question per lesson in the
    # final, and half an hour a lesson. A course grows by whole units or not at
    # all, so a workshop never ends mid-unit or with a unit nobody checks.
    assert lessons % 4 == 0
    units = lessons // 4
    assert [lesson["id"] for lesson in course["modules"]] == [
        f"{prefix}.{i}" for i in range(1, lessons + 1)
    ]
    assert [part["id"] for part in course["parts"]] == [str(i) for i in range(1, units + 1)]
    assert sum(lesson["minutes"] for lesson in course["modules"]) == lessons * 30
    assert "exam time is additional" in course["readingGuide"]
    kinds = [exam["kind"] for exam in course["exams"]]
    assert kinds == ["checkpoint"] * units + ["final"]
    assert len(course["exams"][-1]["questions"]) == lessons
    prompts = [q["question"] for exam in course["exams"] for q in exam["questions"]]
    prompts += [q["question"] for lesson in course["modules"] for q in lesson["exercises"]]
    assert len(prompts) == len(set(prompts))
    for lesson in course["modules"]:
        assert lesson["content"].count("$$") >= 2
        assert len(lesson["assignment"]["solution"]) > 120
        assert len(lesson["references"]) >= 2


def test_simulator_lessons_link_only_real_missions():
    linked = set()
    for lesson in COURSES["simulator-workshop"]["modules"]:
        linked |= set(re.findall(r"/simulator\?mission=([a-z-]+)", lesson["content"]))
    assert linked <= MISSIONS.keys()
    # Every mission is reachable from the workshop, including the previously unlinked stop drill.
    assert linked == set(MISSIONS)


def test_lab_lessons_link_only_real_tools():
    for lesson in COURSES["lab-workshop"]["modules"]:
        tools = set(re.findall(r"/lab\?tool=([a-z]+)", lesson["content"]))
        assert tools and tools <= LAB_TOOLS, lesson["id"]
    used = {tool for lesson in COURSES["lab-workshop"]["modules"]
            for tool in re.findall(r"/lab\?tool=([a-z]+)", lesson["content"])}
    assert used == LAB_TOOLS


# The capstone is named rather than taken from the end of the course: the
# simulator workshop now carries a unit after it, and a positional lookup would
# silently start testing whichever lesson happened to be last.
@pytest.mark.parametrize("course_id,lesson_id,line", [
    ("simulator-workshop", "13.12", "Simulator review checklist: 12 of 12"),
    ("lab-workshop", "14.12", "Lab research loop steps: 12 of 12"),
])
def test_capstone_worksheets_run_in_the_guided_runtime(course_id, lesson_id, line):
    capstone = next(m for m in COURSES[course_id]["modules"] if m["id"] == lesson_id)
    assert "Capstone" in capstone["title"]
    result = run(capstone["code"], {"close": [100, 101, 99]})
    assert line in result["stdout"]
    assert result["signals"] == [False, False, False]


def test_simulator_worked_examples_match_independent_arithmetic():
    friction = (2 + 2 / 2) / 10_000
    # A sell stop gapped through at 142.00 fills at the open less friction, rounded to the cent.
    assert round(142.00 * (1 - friction), 2) == 141.96
    # A 600-share short of $90,000 on $100,000 is bought in above 190,000 / 780.
    assert round(190_000 / 780, 2) == 243.59
    stops = COURSES["simulator-workshop"]["modules"][6]["content"]
    assert "141.96" in stops and "145.35" in stops
    margin = COURSES["simulator-workshop"]["modules"][7]["content"]
    assert "243.59" in margin
