"""Shared authoring helpers for original, book-aligned applied courses."""

import re
from math import ceil


def q(prompt, options, answer, explanation):
    return dict(question=prompt, options=options, answer=answer, explanation=explanation)


def lesson(id, part, title, objective, reading, content, formula, code, task, solution, questions):
    """Two practice items and a separate transfer item for the final exam."""
    assert len(questions) == 3
    if "$$" not in content:
        content = content.replace(
            "## A worked example", f"$$\n{formula}\n$$\n\n## A worked example"
        )
    # Markdown math blocks require delimiters on their own lines.
    content = re.sub(
        r"\$\$(.*?)\$\$", lambda match: "$$\n" + match[1].strip() + "\n$$", content, flags=re.S
    )
    return {
        "id": id,
        "part": part,
        "title": title,
        "subtitle": objective,
        "objective": objective,
        "reading": reading,
        "minutes": max(12, ceil(len(content.split()) / 160) + 10),
        "kind": "book-study",
        "content": content.strip(),
        "formula": formula,
        "code": code.strip()
        + '\n\n# This worksheet computes the case above. The price sandbox stays in cash.\n# Its equity curve is not evidence for the valuation or statistical claim.\ndef strategy(data):\n    return data["close"] < 0\n',
        "assignment": {"prompt": task, "solution": solution},
        "exercise": questions[0],
        "exercises": questions[:2],
        "_final": questions[2],
    }


def finish(track, checkpoints):
    modules = track["modules"]
    final_id = f"{track['id']}-final"
    final = {
        "id": final_id,
        "title": f"{track['title']} final exam",
        "kind": "final",
        "version": 2,
        "description": "Open-book, untimed assessment with new cases from every module. Budget about three minutes per question. Answers and explanations appear after submission. Pass at 80%; retries remain available. The written capstone is self-assessed separately.",
        "minutes": len(modules) * 3,
        "passingScore": 80,
        "moduleIds": [m["id"] for m in modules],
        "questions": [
            {"id": f"{final_id}-{m['id']}", "lessonId": m["id"], **m.pop("_final")} for m in modules
        ],
    }
    track["exams"] = []
    for index, (title, rows) in enumerate(checkpoints, 1):
        exam_id = f"{track['id']}-checkpoint-{index}"
        track["exams"].append(
            {
                "id": exam_id,
                "title": title,
                "kind": "checkpoint",
                "version": 1,
                "description": "Four original transfer questions. Use your notes, show calculations, and review the explanations after submitting. This checkpoint samples the preceding unit; the final covers every module.",
                "minutes": 16,
                "passingScore": 75,
                "moduleIds": [id for id, _ in rows],
                "questions": [
                    {"id": f"{exam_id}-q{i}", "lessonId": id, **question}
                    for i, (id, question) in enumerate(rows, 1)
                ],
            }
        )
    track["exams"].append(final)
    return track
