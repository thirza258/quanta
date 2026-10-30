"""Shared helpers for the advanced, case-driven security-analysis courses."""

from book_courses import finish, lesson, q

READING = (
    "Advanced security analysis · original case study. Read the cited primary source "
    "beside this lesson, then repeat the method on a company you can inspect directly. "
    "The numbers in the worked example are teaching figures unless the lesson says otherwise."
)


def make_add(modules, reading=READING):
    def add(id, part, title, objective, content, formula, code, task, solution, questions):
        modules.append(
            lesson(
                id,
                part,
                title,
                objective,
                reading,
                content,
                formula,
                code,
                task,
                solution,
                questions,
            )
        )

    return add
