"""Checks for the sourced research extension added to lessons as each one is verified."""

import importlib
import re
from copy import deepcopy
from pathlib import Path

import pytest
from quanta.domain.catalog import CATALOG, LESSONS

HEADING = "## Go deeper: what the research says"
SOURCES = "### Sources for this section"
LINK = re.compile(r"\[([^\]]+)\]\((https://[^\s)]+)\)")
RESEARCHED = [lesson for lesson in LESSONS.values() if HEADING in lesson["content"]]


def research_section(lesson):
    return lesson["content"].split(HEADING, 1)[1]


@pytest.fixture
def research(monkeypatch):
    root = Path(__file__).resolve().parents[2]
    monkeypatch.syspath_prepend(str(root / "content/authoring"))
    return importlib.import_module("research_depth")


def test_every_saved_note_reaches_exactly_its_lesson(research):
    expected = set()
    for course in CATALOG:
        notes = research.load_notes(course["id"])
        assert notes.keys() <= {lesson["id"] for lesson in course["modules"]}, course["id"]
        expected |= notes.keys()
    assert {lesson["id"] for lesson in RESEARCHED} == expected
    assert all(lesson["content"].count(HEADING) == 1 for lesson in RESEARCHED)
    # Three complete courses anchor the feature; the rest are added lesson by lesson.
    for course_id in ("trading-fundamentals", "trading-ethics", "algorithm-evaluation"):
        course = next(c for c in CATALOG if c["id"] == course_id)
        assert all(HEADING in lesson["content"] for lesson in course["modules"]), course_id


def test_each_research_section_is_final_unique_and_sourced():
    bodies = set()
    for lesson in RESEARCHED:
        section = research_section(lesson)
        # The extension is the final section, after the lesson's own practice.
        assert "\n## " not in section, lesson["id"]
        body, marker, sources = section.partition(SOURCES)
        assert marker, lesson["id"]
        assert 150 <= len(body.split()) <= 480, lesson["id"]
        links = LINK.findall(sources)
        assert 2 <= len(links) <= 5, lesson["id"]
        footer = {ref["url"]: ref["title"] for ref in lesson["references"]}
        for title, url in links:
            # Each cited source reaches the lesson's reference footer and library.
            assert url in footer, (lesson["id"], url)
            assert len(title) > 10
        key = " ".join(body.split())
        assert key not in bodies, lesson["id"]
        bodies.add(key)


def test_research_links_are_canonical_and_lean_on_arxiv(research):
    with_arxiv = 0
    for lesson in RESEARCHED:
        links = [url for _, url in LINK.findall(research_section(lesson))]
        assert all("(" not in url and " " not in url for url in links)
        papers = [url for url in links if "arxiv.org" in url]
        assert all(research.ARXIV.fullmatch(url) for url in papers), lesson["id"]
        with_arxiv += bool(papers)
    assert with_arxiv >= len(RESEARCHED) * 3 // 4


def test_research_keeps_lesson_markdown_conventions():
    for lesson in RESEARCHED:
        body = research_section(lesson).split(SOURCES, 1)[0]
        assert "](" not in body, lesson["id"]
        assert body.count("$$") in (0, 2), lesson["id"]
        assert not re.search(r"^\s*(\||\d+[.)]\s)", body, re.M), lesson["id"]


VALID_SOURCES = [
    ("arxiv", "Gould et al.", 2010, "Limit Order Books", "https://arxiv.org/abs/1012.0349",
     "A survey of how limit order books match buyers and sellers."),
    ("paper", "Barber & Odean", 2000, "Trading Is Hazardous to Your Wealth",
     "https://doi.org/10.1111/0022-1082.00226", "Household evidence that heavy trading lowered returns."),
]


@pytest.mark.parametrize("fault,match", [
    ("short", "words"),
    ("link", "links"),
    ("table", "tables or numbered lists"),
    ("numbered", "tables or numbered lists"),
    ("equations", "at most one display equation"),
    ("one-source", "two to five sources"),
    ("versioned-arxiv", "version-free"),
    ("http", "plain https"),
    ("parentheses", "plain https"),
    ("duplicate", "cited twice"),
])
def test_validator_rejects_notes_that_would_render_badly(research, fault, match):
    body = " ".join(["Evidence matters before any decision is made."] * 30)
    sources = deepcopy(VALID_SOURCES)
    if fault == "short":
        body = "Too short."
    elif fault == "link":
        body += " See [this paper](https://arxiv.org/abs/1012.0349)."
    elif fault == "table":
        body += "\n\n| a | b |\n| --- | --- |"
    elif fault == "numbered":
        body += "\n\n1. First step"
    elif fault == "equations":
        body += "\n\n$$\nx\n$$\n\n$$\ny\n$$"
    elif fault == "one-source":
        sources = sources[:1]
    elif fault == "versioned-arxiv":
        sources[0] = sources[0][:4] + ("https://arxiv.org/abs/1012.0349v4",) + sources[0][5:]
    elif fault == "http":
        sources[1] = sources[1][:4] + ("http://doi.org/10.1111/0022-1082.00226",) + sources[1][5:]
    elif fault == "parentheses":
        sources[1] = sources[1][:4] + ("https://doi.org/10.1016/0304-405X(85)90044-3",) + sources[1][5:]
    else:
        sources.append(sources[1][:4] + ("https://ideas.repec.org/a/bla/jfinan/v55y2000i2p773-806.html",) + sources[1][5:])
    with pytest.raises(ValueError, match=match):
        research.validate("x.1", body, sources)


def test_validator_accepts_a_well_formed_note(research):
    body = " ".join(["Evidence matters before any decision is made."] * 30)
    research.validate("x.1", body + "\n\n$$\ng \\approx \\mu - \\tfrac{1}{2}\\sigma^2\n$$", VALID_SOURCES)


def test_builder_refuses_unknown_lessons_and_double_attachment(research, monkeypatch):
    with pytest.raises(ValueError, match="already attached"):
        research.attach_research_depth(deepcopy(CATALOG))
    original = research.load_notes

    def with_unknown(course_id):
        notes = dict(original(course_id))
        notes["99.99"] = next(iter(notes.values())) if notes else ("", [])
        return notes

    monkeypatch.setattr(research, "load_notes", with_unknown)
    with pytest.raises(ValueError, match="unknown lessons"):
        research.attach_research_depth(deepcopy(CATALOG))
