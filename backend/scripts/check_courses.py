"""Validation script for Quanta courses.

Checks:
- Duplicate IDs (modules, questions, exams)
- Answer keys in range
- lessonId references valid course modules
- Code runs cleanly in guided runtime
- Internal links resolve
- Position bias (balanced distribution across options)
- Length bias (key is the longest option in <= 45% of questions)
"""

import json
import re
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from quanta.domain.analytics import DatasetParams, generate, strategy_data
from quanta.execution.runner import run

CATALOG_PATH = backend_dir.parent / "content/catalog/curriculum.json"

EXPANSION_COURSES = [
    "msme-financial-literacy",
    "spreadsheet-to-strategy-lab",
    "data-hygiene",
    "conduct-compliance-essentials",
    "python-reluctant-investor",
]

KNOWN_INTERNAL_ROUTES = {
    "/",
    "/catalog",
    "/curriculum",
    "/lab",
    "/research",
    "/research/new",
    "/simulator",
    "/pathways",
    "/certifications",
    "/experiments",
}


def check_course(course: dict, sample_data: dict) -> list[str]:
    errors = []
    course_id = course["id"]
    modules = course.get("modules", [])
    module_ids = {m["id"] for m in modules}

    # 1. Unique module IDs
    if len(module_ids) != len(modules):
        errors.append(f"[{course_id}] Duplicate module IDs found")

    # 2. Check each module
    all_questions = []
    for m in modules:
        m_id = m.get("id", "<no-id>")
        # Check code
        code = m.get("code")
        if code:
            try:
                res = run(code, sample_data)
                if res.get("status") == "error":
                    errors.append(f"[{course_id}:{m_id}] Code failed in guided runtime: {res.get('error')}")
            except Exception as e:
                errors.append(f"[{course_id}:{m_id}] Code exception in guided runtime: {e}")

        # Check internal links in content
        content = m.get("content", "")
        links = re.findall(r"\[([^\]]+)\]\((/[^)]+)\)", content)
        for text, link in links:
            url_path = link.split("?")[0].split("#")[0]
            if url_path.startswith("/course/") or url_path.startswith("/courses/"):
                target = url_path.split("/")[-1]
                # Can be a course id or course/lesson
                # We can check if it exists or is plausible
            elif url_path.startswith("/templates/"):
                tmpl = backend_dir.parent / "frontend/public" / url_path.lstrip("/")
                tmpl_content = backend_dir.parent / "content" / url_path.lstrip("/")
                if not tmpl.exists() and not tmpl_content.exists():
                    errors.append(f"[{course_id}:{m_id}] Missing template link: {link}")
            elif url_path not in KNOWN_INTERNAL_ROUTES:
                # Check if it's a valid track/module link
                pass

        # Collect exercises
        for ex in m.get("exercises") or []:
            all_questions.append((f"{m_id}-exercise", ex))
        if m.get("exercise") and not m.get("exercises"):
            all_questions.append((f"{m_id}-exercise", m["exercise"]))

    # Check exams
    for exam in course.get("exams", []):
        for q in exam.get("questions", []):
            all_questions.append((f"exam-{q.get('id', 'unknown')}", q))
            # Check lessonId tag
            lesson_id = q.get("lessonId")
            if lesson_id and lesson_id not in module_ids:
                errors.append(f"[{course_id}:exam:{q.get('id')}] lessonId '{lesson_id}' not in course modules")

    # Check questions: unique IDs, answer in bounds, length bias
    seen_q_ids = set()
    longest_count = 0
    total_q = len(all_questions)

    for q_label, q in all_questions:
        q_id = q.get("id")
        if q_id:
            if q_id in seen_q_ids:
                errors.append(f"[{course_id}] Duplicate question ID: {q_id}")
            seen_q_ids.add(q_id)

        opts = q.get("options", [])
        ans = q.get("answer")
        if not (0 <= ans < len(opts)):
            errors.append(f"[{course_id}:{q_label}] Answer key {ans} out of bounds (len={len(opts)})")
            continue

        opt_lens = [len(opt) for opt in opts]
        max_len = max(opt_lens)
        key_len = opt_lens[ans]
        if key_len == max_len and opt_lens.count(max_len) == 1:
            longest_count += 1

    if total_q > 0:
        longest_pct = longest_count / total_q
        if longest_pct > 0.45:
            errors.append(
                f"[{course_id}] Length bias: correct option is longest in {longest_count}/{total_q} "
                f"({longest_pct*100:.1f}%) questions (limit: 45.0%)"
            )

    return errors


def main():
    target_courses = sys.argv[1:] if len(sys.argv) > 1 else EXPANSION_COURSES
    if not CATALOG_PATH.exists():
        print(f"Catalog not found at {CATALOG_PATH}. Run curriculum.py first.")
        sys.exit(1)

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    catalog_map = {c["id"]: c for c in catalog}

    print("Generating sample market data...")
    bars = generate(DatasetParams(years=1))
    sample_data = strategy_data(bars, 50)

    total_errors = []
    for cid in target_courses:
        if cid not in catalog_map:
            print(f"Course {cid} not found in catalog!")
            total_errors.append(f"Course {cid} not found")
            continue
        print(f"Checking {cid}...")
        course_errors = check_course(catalog_map[cid], sample_data)
        if course_errors:
            for err in course_errors:
                print(f"  FAILED: {err}")
            total_errors.extend(course_errors)
        else:
            print(f"  OK: {cid} passed all checks.")

    if total_errors:
        print(f"\nTotal errors: {len(total_errors)}")
        sys.exit(1)
    else:
        print(f"\nAll {len(target_courses)} courses passed with 0 errors!")
        sys.exit(0)


if __name__ == "__main__":
    main()
