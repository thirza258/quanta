"""Sourced research extensions: a deeper, cited section at the end of every lesson.

A course's data module (``research_<course>.py``) maps lesson IDs to an original
explanation and the papers, standards, and documentation behind it. Notes are added
lesson by lesson as each one is verified; a lesson without a note simply has no
extension yet. Rebuilds fail on unknown or duplicated lessons and on citations that
would not render as a clean, attributable link.
"""

import re
from importlib import import_module
from importlib.util import find_spec
from math import ceil

HEADING = "## Go deeper: what the research says"
KINDS = {
    "arxiv": "arXiv preprint",
    "paper": "Research paper",
    "book": "Book",
    "official": "Official source",
    "docs": "Technical documentation",
    "data": "Dataset documentation",
}
ARXIV = re.compile(r"https://arxiv\.org/abs/(\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?/\d{7})")
URL = re.compile(r"https://[^\s()<>\[\]]+")


def module_name(course_id):
    return "research_" + course_id.replace("-", "_")


def validate(lesson_id, body, sources):
    """Reject a note that would render badly or cite a source ambiguously."""
    words = len(body.split())
    if not 150 <= words <= 450:
        raise ValueError(f"Research body for {lesson_id} has {words} words; expected 150–450")
    if "](" in body or re.search(r"^#{1,2} ", body, re.M):
        raise ValueError(f"Research body for {lesson_id} must not contain links or top-level headings")
    # Lesson pages keep one table and one numbered list at most; sources carry the links.
    if re.search(r"^\s*(\||\d+[.)]\s)", body, re.M):
        raise ValueError(f"Research body for {lesson_id} must not add tables or numbered lists")
    if body.count("$$") not in (0, 2):
        raise ValueError(f"Research body for {lesson_id} may add at most one display equation")
    if not 2 <= len(sources) <= 5:
        raise ValueError(f"Research note for {lesson_id} needs two to five sources")
    urls, labels = set(), set()
    for source in sources:
        if len(source) != 6:
            raise ValueError(f"Malformed research source for {lesson_id}: {source!r}")
        kind, authors, year, title, url, note = source
        # Footer links are found by their visible name, so each must be unique.
        label = (authors.strip().lower(), title.strip().lower())
        if label in labels:
            raise ValueError(f"Research source cited twice for {lesson_id}: {title}")
        labels.add(label)
        if kind not in KINDS:
            raise ValueError(f"Unknown source kind for {lesson_id}: {kind}")
        if not (authors.strip() and len(title.strip()) >= 8 and 30 <= len(note) <= 400):
            raise ValueError(f"Incomplete research source for {lesson_id}: {url}")
        if year is not None and not (isinstance(year, int) and 1600 <= year <= 2026):
            raise ValueError(f"Implausible source year for {lesson_id}: {year!r}")
        if any(mark in authors + title for mark in "[]\n") or "](" in note:
            raise ValueError(f"Source label for {lesson_id} would break its Markdown link")
        if not URL.fullmatch(url):
            raise ValueError(f"Research source URL for {lesson_id} must be a plain https link: {url}")
        if (kind == "arxiv") != bool(ARXIV.fullmatch(url)):
            raise ValueError(f"arXiv sources for {lesson_id} need a version-free abs URL: {url}")
        if url in urls:
            raise ValueError(f"Duplicate research source for {lesson_id}: {url}")
        urls.add(url)


def render(body, sources):
    body = re.sub(
        r"\$\$(.*?)\$\$", lambda match: "$$\n" + match[1].strip() + "\n$$", body.strip(), flags=re.S
    )
    minutes = max(2, ceil(len(body.split()) / 150))
    lines = [
        HEADING,
        "",
        f"*Research extension · about {minutes} minutes. This summary is Quanta's own explanation; "
        "findings and figures belong to the cited authors and the samples they studied.*",
        "",
        body,
        "",
        "### Sources for this section",
        "",
    ]
    for kind, authors, year, title, url, note in sources:
        label = f"{authors} ({year}) · {title}" if year else f"{authors} · {title}"
        tag = f"arXiv {ARXIV.fullmatch(url)[1]}" if kind == "arxiv" else KINDS[kind]
        lines.append(f"- [{label}]({url}) — *{tag}.* {note.strip()}")
    return "\n".join(lines)


def load_notes(course_id):
    name = module_name(course_id)
    return import_module(name).NOTES if find_spec(name) else {}


def attach_research_depth(catalog):
    """Append each verified lesson's research section; run before references are collected."""
    bodies = {}
    for course in catalog:
        notes = load_notes(course["id"])
        lesson_ids = {module["id"] for module in course["modules"]}
        if unknown := sorted(notes.keys() - lesson_ids):
            raise ValueError(f"Research notes for unknown lessons in {course['id']}: {unknown}")
        for module in course["modules"]:
            if module["id"] not in notes:
                continue
            body, sources = notes[module["id"]]
            validate(module["id"], body, sources)
            key = " ".join(body.split())
            if key in bodies:
                raise ValueError(f"Research body for {module['id']} repeats {bodies[key]}")
            bodies[key] = module["id"]
            if HEADING in module["content"]:
                raise ValueError(f"Research section already attached to {module['id']}")
            module["content"] = module["content"].rstrip() + "\n\n" + render(body, sources)
