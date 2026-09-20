import copy
import uuid

import pytest
from quanta.domain.catalog import CATALOG
from quanta.services import certificates
from test_api import signup
from test_assessments import payload as exam_payload

COURSE = CATALOG[0]


def ready_state(course=COURSE):
    return {
        "completed": [lesson["id"] for lesson in course["modules"]],
        "examAttempts": {exam["id"]: [exam_payload(exam["id"])] for exam in course["exams"]},
    }


def save(client, state):
    version = client.get("/api/v1/workspace").json()["version"]
    response = client.put("/api/v1/workspace", json={"version": version, "state": state})
    assert response.status_code == 200, response.text
    return response.json()["version"]


def claim(client, version, **extra):
    return client.post(
        "/api/v1/certificates",
        json={
            "trackId": COURSE["id"],
            "recipientName": "  Ayu   Pratama  ",
            "workspaceVersion": version,
            **extra,
        },
    )


def test_issue_requires_account_and_complete_current_course(client):
    assert claim(client, 0).status_code == 401
    assert client.get("/api/v1/certificates").status_code == 401
    signup(client)
    state = ready_state()
    state["completed"].pop()
    assert claim(client, save(client, state)).status_code == 422
    state = ready_state()
    version = save(client, state)
    assert claim(client, version - 1).status_code == 409
    assert claim(client, version, trackId="missing").status_code == 404
    assert claim(client, version, recipientName="   ").status_code == 422
    assert claim(client, version, recipientName="a" * 81).status_code == 422
    result = claim(client, version)
    assert result.status_code == 200, result.text
    assert result.json()["recipientName"] == "Ayu Pratama"


@pytest.mark.parametrize(
    "change", ["wrong-answers", "old-version", "missing-answer", "invalid-attempt", "invalid-map"]
)
def test_regrades_saved_answers_instead_of_trusting_pass_flags(client, change):
    signup(client)
    state = ready_state()
    exam = COURSE["exams"][0]
    attempt = state["examAttempts"][exam["id"]][0]
    attempt.update({"passed": True, "score": 100, "grading": "server"})
    if change == "wrong-answers":
        attempt["answers"] = {
            q["id"]: (q["answer"] + 1) % len(q["options"]) for q in exam["questions"]
        }
    elif change == "old-version":
        attempt["version"] += 1
    elif change == "missing-answer":
        attempt["answers"].pop(next(iter(attempt["answers"])))
    elif change == "invalid-attempt":
        state["examAttempts"][exam["id"]] = [None, {"passed": True}]
    else:
        state["examAttempts"] = []
    assert claim(client, save(client, state)).status_code == 422


def test_public_verification_is_immutable_and_does_not_expose_account_data(client):
    signup(client)
    version = save(client, ready_state())
    original = claim(client, version).json()
    assert claim(client, version, recipientName="Replacement").json() == original
    # Workspace imports and edits cannot alter the separately stored issuer record.
    save(client, {"certificates": [{**original, "recipientName": "Forged"}]})
    assert claim(client, 0).json() == original
    assert client.get("/api/v1/certificates").json() == {"certificates": [original]}
    client.post("/api/v1/auth/logout")
    verified = client.get(f"/api/v1/certificates/{original['id'].lower()}/verify")
    assert verified.status_code == 200
    assert verified.json() == {"status": "valid", "certificate": original}
    assert verified.headers["cache-control"] == "no-store"
    assert set(original) == {
        "id",
        "trackId",
        "courseTitle",
        "recipientName",
        "issuedAt",
        "lessonIds",
        "examVersions",
        "studyMinutes",
    }
    assert (
        "email" not in verified.text
        and "user_id" not in verified.text
        and "answers" not in verified.text
    )
    signup(client)
    assert client.get("/api/v1/certificates").json() == {"certificates": []}
    assert claim(client, save(client, {})).status_code == 422


def test_missing_or_fabricated_ids_are_not_verified(client):
    for identifier in ["missing", f"QTA-{uuid.uuid4()}", "QTA-" + "0" * 36]:
        assert client.get(f"/api/v1/certificates/{identifier}/verify").status_code == 404


def test_account_owned_online_passes_restore_missing_workspace_attempts(client):
    signup(client)
    for exam in COURSE["exams"]:
        assert (
            client.post(
                f"/api/v1/exams/{exam['id']}/submit", json=exam_payload(exam["id"])
            ).status_code
            == 200
        )
    state = ready_state()
    state["examAttempts"] = {}
    assert claim(client, save(client, state)).status_code == 200
    client.post("/api/v1/auth/logout")
    signup(client)
    assert claim(client, save(client, state)).status_code == 422


def test_new_course_edition_requires_current_passes_and_preserves_original(client, monkeypatch):
    signup(client)
    state = ready_state()
    original = claim(client, save(client, state)).json()
    revised = copy.deepcopy(COURSE)
    for exam in revised["exams"]:
        exam["version"] += 1
    monkeypatch.setattr(certificates, "CATALOG", [revised])
    version = save(client, state)
    assert claim(client, version).status_code == 422
    for exam in revised["exams"]:
        state["examAttempts"][exam["id"]][0]["version"] = exam["version"]
    updated = claim(client, save(client, state)).json()
    assert updated["id"] != original["id"]
    assert len(client.get("/api/v1/certificates").json()["certificates"]) == 2
    assert (
        client.get(f"/api/v1/certificates/{original['id']}/verify").json()["certificate"]
        == original
    )
