import uuid

from quanta.domain.analytics import DatasetParams, generate


def signup(client):
    result = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test Researcher",
            "email": f"{uuid.uuid4().hex}@example.com",
            "password": "a-long-test-password",
        },
    )
    assert result.status_code == 201, result.text
    assert "HttpOnly" in result.headers["set-cookie"]
    return result.json()


def test_health_content_and_validation(client):
    assert client.get("/api/v1/health").json()["status"] == "ok"
    catalog = client.get("/api/v1/courses").json()
    assert len(catalog) == 15
    assert catalog[0]["id"] == "trading-fundamentals"
    assert sum(len(c["modules"]) for c in catalog) == 344
    news = next(course for course in catalog if course["id"] == "news-to-markets")
    lesson = client.get("/api/v1/courses/lessons/8.3").json()
    case = next(item for item in news["caseStudies"] if item["id"] == lesson["realWorld"]["caseId"])
    assert case["id"] == "bps_growth" and case["references"][0]["scope"]
    assert lesson["realWorld"]["task"] and lesson["realWorld"]["walkthrough"]
    assert client.get("/api/v1/courses/lessons/missing").status_code == 404
    assert client.post("/api/v1/data/synthetic/generate", json={"years": 0}).status_code == 422
    assert client.post("/api/v1/analytics/valuation", json={"shares": 0}).status_code == 422
    assert client.post("/api/v1/analytics/amm", json={"lower_ratio": 2}).status_code == 422


def test_auth_workspace_revocation_and_ownership(client):
    assert client.get("/api/v1/workspace").status_code == 401
    first = signup(client)
    assert client.get("/api/v1/auth/me").json()["id"] == first["id"]
    assert client.get("/api/v1/workspace").json() == {"version": 0, "state": {}}
    state = {"completed": ["1.1"], "notes": [{"title": "Private note"}]}
    assert (
        client.put("/api/v1/workspace", json={"version": 0, "state": state}).json()["version"] == 1
    )
    assert (
        client.put("/api/v1/workspace", json={"version": 0, "state": {"completed": []}}).status_code
        == 409
    )
    assert client.get("/api/v1/workspace").json()["state"] == state
    cookie = client.cookies.get("quanta_session")
    assert client.post("/api/v1/auth/logout").status_code == 200
    assert (
        client.get("/api/v1/auth/me", headers={"Cookie": f"quanta_session={cookie}"}).json() is None
    )
    second = signup(client)
    assert first["id"] != second["id"]
    assert client.get("/api/v1/workspace").json()["state"] == {}


def test_login_wrong_password_and_origin(client):
    user = signup(client)
    client.post("/api/v1/auth/logout")
    assert (
        client.post(
            "/api/v1/auth/login",
            json={"email": user["email"], "password": "wrong-password"},
        ).status_code
        == 401
    )
    assert (
        client.post(
            "/api/v1/auth/login",
            json={"email": user["email"], "password": "a-long-test-password"},
        ).status_code
        == 200
    )
    assert (
        client.post(
            "/api/v1/auth/logout", headers={"Origin": "https://attacker.example"}
        ).status_code
        == 403
    )


def test_exercise_checks_on_server(client):
    assert (
        client.post("/api/v1/exercises/1.1/submit", json={"answer": 0}).json()["correct"] is False
    )
    signup(client)
    assert client.post("/api/v1/exercises/1.1/submit", json={"answer": 1}).json()["correct"] is True
    assert client.post("/api/v1/exercises/1.1/submit", json={"answer": 9}).status_code == 422


def test_sandbox_pipeline_and_unknown_historical_data(client):
    body = {
        "code": 'print("research")\ndef strategy(data):\n    return data["close"] > data["sma_50"]',
        "dataset_params": {"years": 5, "model": "heston"},
    }
    result = client.post("/api/v1/sandbox/execute", json=body)
    assert result.status_code == 200, result.text
    out = result.json()
    assert len(out["bars"]) == 1260
    assert out["stdout"] == "research\n"
    assert out["execution_ms"] < 2000
    assert out["dataset_type"] == "synthetic"
    assert len(out["monthly_returns"]) > 50
    body["dataset_type"] = "real"
    assert client.post("/api/v1/sandbox/execute", json=body).status_code == 422
    body["dataset_type"] = "synthetic"
    body["code"] = "import os"
    assert client.post("/api/v1/sandbox/execute", json=body).status_code == 422


def test_compute_rate_limit(client):
    for _ in range(30):
        assert client.post("/api/v1/data/synthetic/generate", json={"years": 1}).status_code == 200
    response = client.post("/api/v1/data/synthetic/generate", json={"years": 1})
    assert response.status_code == 429
    assert response.headers["retry-after"] == "60"


def test_historical_import_reader(client, tmp_path):
    import duckdb
    import pandas as pd
    from quanta.services.data_store import DATA_DIR

    DATA_DIR.mkdir(exist_ok=True, parents=True)
    df = pd.DataFrame(generate(DatasetParams(years=1)))
    # Test fixture is synthetic and only verifies the storage pipeline.
    with duckdb.connect() as db:
        db.register("fixture", df)
        db.execute("COPY fixture TO ? (FORMAT PARQUET)", [str(DATA_DIR / "TEST.parquet")])
    try:
        assert client.get("/api/v1/data/catalog").json()["datasets"][0]["symbol"] == "TEST"
        out = client.post(
            "/api/v1/sandbox/execute",
            json={
                "dataset_type": "real",
                "dataset_params": {"symbol": "TEST", "years": 1},
                "code": "def strategy(data): return True",
            },
        )
        assert out.status_code == 200, out.text
        assert out.json()["dataset_type"] == "real"
    finally:
        (DATA_DIR / "TEST.parquet").unlink()
