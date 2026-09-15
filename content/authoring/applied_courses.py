"""Original applied lessons with runnable worksheets and independent assessments."""

from book_courses import lesson, q


def study(
    id,
    part,
    title,
    objective,
    principle,
    case,
    workflow,
    formula,
    code,
    task,
    solution,
    questions,
    references,
):
    """Four distinct questions: two practice, one final, and one unit checkpoint."""
    item = lesson(
        id,
        str(part),
        title,
        objective,
        f"This lesson belongs to Unit {part}. Read the explanation and work through the example before trying the assignment. Use the linked sources to check the underlying method, then write your calculation and what it means in your notebook.",
        f"## Model and assumptions\n\n{principle}\n\n## A worked example\n\n{case}\n\n## Implementation and interpretation\n\n{workflow}",
        formula,
        code,
        task,
        solution,
        [q(*row) for row in questions[:3]],
    )
    item["kind"] = "applied-study"
    item["references"] = [{"title": title, "url": url} for title, url in references]
    item["_checkpoint"] = q(*questions[3])
    item["code"] = item["code"].replace(
        "valuation or statistical claim", "model or strategy's performance"
    )
    return item


def checkpoints_for(modules, parts, count):
    questions = {item["id"]: item.pop("_checkpoint") for item in modules}
    return [
        (
            f"Unit {i + 1}: {parts[i][0]}",
            [(item["id"], questions[item["id"]]) for item in modules[i * 4 : (i + 1) * 4]],
        )
        for i in range(count)
    ]
