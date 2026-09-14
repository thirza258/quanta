import uuid

import pytest
from quanta.main import EXAMS, LESSONS
from test_api import signup


def payload(exam_id="fundamentals-final", correct=None):
    exam = EXAMS[exam_id]
    count = len(exam["questions"]) if correct is None else correct
    return {
        "id": str(uuid.uuid4()),
        "version": exam["version"],
        "startedAt": "2026-09-14T00:00:00Z",
        "answers": {
            q["id"]: q["answer"] if i < count else (q["answer"] + 1) % len(q["options"])
            for i, q in enumerate(exam["questions"])
        },
    }


@pytest.mark.parametrize("exam_id", EXAMS)
def test_every_exam_is_graded_on_server(client, exam_id):
    result = client.post(f"/api/v1/exams/{exam_id}/submit", json=payload(exam_id))
    assert result.status_code == 200, result.text
    assert result.json()["score"] == 100
    assert result.json()["passed"] is True
    assert result.json()["grading"] == "server"


@pytest.mark.parametrize("correct,passed,score", [(12, False, 75), (13, True, 81.25)])
def test_final_exact_threshold(client, correct, passed, score):
    result = client.post(
        "/api/v1/exams/fundamentals-final/submit", json=payload(correct=correct)
    ).json()
    assert result["passed"] is passed
    assert result["score"] == score
    assert result["correctCount"] == correct


def test_checkpoint_exact_threshold(client):
    result = client.post(
        "/api/v1/exams/fundamentals-checkpoint/submit", json=payload("fundamentals-checkpoint", 6)
    ).json()
    assert result["passed"] is True
    assert result["score"] == 75


@pytest.mark.parametrize(
    "change", ["missing", "extra", "negative", "fraction", "boolean", "string", "out-of-range"]
)
def test_exam_rejects_invalid_answers(client, change):
    body = payload()
    key = next(iter(body["answers"]))
    if change == "missing":
        del body["answers"][key]
    elif change == "extra":
        body["answers"]["not-a-question"] = 0
    else:
        body["answers"][key] = {
            "negative": -1,
            "fraction": 0.5,
            "boolean": True,
            "string": "0",
            "out-of-range": 99,
        }[change]
    assert client.post("/api/v1/exams/fundamentals-final/submit", json=body).status_code == 422


def test_exam_rejects_unknown_version_and_unknown_id(client):
    body = payload()
    body["version"] = 99
    assert client.post("/api/v1/exams/fundamentals-final/submit", json=body).status_code == 409
    assert client.post("/api/v1/exams/missing/submit", json=body).status_code == 404


def test_history_is_account_owned_and_submission_retry_is_idempotent(client):
    path = "/api/v1/exams/fundamentals-final"
    assert client.get(f"{path}/attempts").status_code == 401
    signup(client)
    body = payload()
    first = client.post(f"{path}/submit", json=body).json()
    assert client.post(f"{path}/submit", json=body).json() == first
    assert client.get(f"{path}/attempts").json()["attempts"] == [first]
    changed = {**body, "answers": {**body["answers"], next(iter(body["answers"])): 2}}
    assert client.post(f"{path}/submit", json=changed).status_code == 409
    # Caller-supplied score/pass values have no grading authority.
    failed = {**payload(correct=0), "score": 100, "passed": True}
    assert client.post(f"{path}/submit", json=failed).json()["passed"] is False
    client.post("/api/v1/auth/logout")
    signup(client)
    assert client.get(f"{path}/attempts").json() == {"attempts": []}
    assert client.post(f"{path}/submit", json=body).status_code == 409
    assert client.get("/api/v1/exams/missing/attempts").status_code == 404


def test_all_beginner_practice_questions_and_legacy_keys(client):
    signup(client)
    for lesson in (lesson for lesson in LESSONS.values() if lesson["kind"] == "fundamentals"):
        for index, question in enumerate(lesson["exercises"]):
            path = f"/api/v1/exercises/{lesson['id']}/submit"
            assert (
                client.post(path, json={"question": index, "answer": question["answer"]}).json()[
                    "correct"
                ]
                is True
            )
            assert (
                client.post(
                    path,
                    json={
                        "question": index,
                        "answer": (question["answer"] + 1) % len(question["options"]),
                    },
                ).json()["correct"]
                is False
            )
    assert (
        client.post("/api/v1/exercises/0.1/submit", json={"question": 3, "answer": 0}).status_code
        == 422
    )
    assert client.post("/api/v1/exercises/1.1/submit", json={"answer": 1}).json()["correct"] is True


def test_workspace_round_trips_exam_draft_and_results(client):
    signup(client)
    draft = payload()
    attempt = client.post("/api/v1/exams/fundamentals-final/submit", json=draft).json()
    state = {
        "examDrafts": {"fundamentals-checkpoint": payload("fundamentals-checkpoint")},
        "examAttempts": {"fundamentals-final": [attempt]},
    }
    assert client.put("/api/v1/workspace", json={"version": 0, "state": state}).status_code == 200
    assert client.get("/api/v1/workspace").json()["state"] == state


@pytest.mark.parametrize(
    "slug",
    [
        "security-analysis",
        "statistical-foundations",
        "stock-bots",
        "econometrics",
        "web3",
        "stock-machine-learning",
    ],
)
def test_expanded_final_rejects_old_version_and_grades_exact_threshold(client, slug):
    exam_id = f"{slug}-final"
    exam = EXAMS[exam_id]
    body = payload(exam_id)
    for old_version in range(1, exam["version"]):
        body["version"] = old_version
        assert client.post(f"/api/v1/exams/{exam_id}/submit", json=body).status_code == 409
    required = (len(exam["questions"]) * exam["passingScore"] + 99) // 100
    for correct, passed in [(required - 1, False), (required, True)]:
        result = client.post(f"/api/v1/exams/{exam_id}/submit", json=payload(exam_id, correct))
        assert result.status_code == 200, result.text
        assert result.json()["passed"] is passed


def test_book_course_practice_uses_both_question_keys(client):
    for lesson in (m for m in LESSONS.values() if m["kind"] in ("book-study", "applied-study")):
        for index, question in enumerate(lesson["exercises"]):
            path = f"/api/v1/exercises/{lesson['id']}/submit"
            result = client.post(path, json={"question": index, "answer": question["answer"]})
            assert result.status_code == 200, result.text
            assert result.json()["correct"] is True
