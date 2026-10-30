"""Shared authoring helpers for original, book-aligned applied courses."""

import re
from math import ceil


def q(prompt, options, answer, explanation):
    return dict(question=prompt, options=options, answer=answer, explanation=explanation)


def format_bullet_lists(text):
    """Ensure any bullet lists (•) are converted to properly separated numbered lists so they do not collapse into single paragraphs in CommonMark."""
    if not text or "•" not in text:
        return text

    lines = text.split("\n")
    new_lines = []
    bullet_counter = 0
    in_bullet_list = False

    for i, line in enumerate(lines):
        match = re.match(r"^([ \t]*)•[ \t]*(.*)$", line)
        if match:
            indent, rest = match.groups()
            if not in_bullet_list:
                in_bullet_list = True
                bullet_counter = 1
                if new_lines and new_lines[-1].strip() != "":
                    new_lines.append("")
            else:
                bullet_counter += 1
            new_lines.append(f"{indent}{bullet_counter}. {rest}")
        else:
            if in_bullet_list:
                if line.strip() == "":
                    next_has_bullet = False
                    for future_line in lines[i + 1 :]:
                        if future_line.strip() == "":
                            continue
                        if re.match(r"^[ \t]*•", future_line):
                            next_has_bullet = True
                        break
                    if not next_has_bullet:
                        in_bullet_list = False
                        bullet_counter = 0
                    new_lines.append(line)
                elif re.match(r"^[ \t]+", line) or line.strip().startswith("$$") or line.strip().startswith("- "):
                    new_lines.append(line)
                else:
                    in_bullet_list = False
                    bullet_counter = 0
                    new_lines.append(line)
            else:
                new_lines.append(line)

    return "\n".join(new_lines)


def lesson(id, part, title, objective, reading, content, formula, code, task, solution, questions):
    """Two practice items and a separate transfer item for the final exam."""
    assert len(questions) == 3
    if "$$" not in content:
        content = content.replace(
            "## A worked example", f"$$\n{formula}\n$$\n\n## A worked example"
        )
    # Convert bullet lists (•) to numbered lists so they do not collapse into a single paragraph
    content = format_bullet_lists(content)

    def normalize_math(match):
        inner = match[1].strip()
        # Escape any unescaped dollar signs in LaTeX math mode (e.g. $30{,}874 -> \$30{,}874)
        inner = re.sub(r"(?<!\\)\$", r"\$", inner)

        # Escape & and % inside \text{...} macros
        def replace_text(tmatch):
            text_body = tmatch.group(1)
            text_body = re.sub(r"(?<!\\)&", r"\&", text_body)
            text_body = re.sub(r"(?<!\\)%", r"\%", text_body)
            return r"\text{" + text_body + "}"

        inner = re.sub(r"\\text\{([^}]*)\}", replace_text, inner)
        return "\n\n$$\n" + inner + "\n$$\n\n"

    # Markdown math blocks require delimiters on their own lines.
    content = re.sub(
        r"[ \t]*\$\$(.*?)\$\$", normalize_math, content, flags=re.S
    )
    content = re.sub(r"\n{3,}", "\n\n", content)
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


def finish(track, checkpoints, version=2):
    modules = track["modules"]
    final_id = f"{track['id']}-final"
    final = {
        "id": final_id,
        "title": f"{track['title']} final exam",
        "kind": "final",
        "version": version,
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
