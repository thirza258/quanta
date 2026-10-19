"""Lesson-linked practice missions: catalog, start-up and objective checking."""

from uuid import uuid4

from quanta.core.limits import limiter
from quanta.services.simulator_missions import CHECKS, MISSIONS


def ident():
    return str(uuid4())


def start(client, mission="first-order"):
    response = client.post(
        "/api/v1/simulator/runs", json={"id": ident(), "mission": mission}
    )
    assert response.status_code == 200, response.text
    return response.json()


def test_the_catalog_describes_every_mission(client):
    body = client.get("/api/v1/simulator/missions").json()
    assert len(body["missions"]) == len(MISSIONS) == 7
    for entry in body["missions"]:
        # A campaign carries its objectives on its stages rather than at the top.
        assert entry["lessons"] and entry["brief"]
        assert entry["objectives"] or entry["stages"]
        assert len(entry["brief"]) > 200
        assert entry["name"] and entry["symbol"]
        for objective in entry["objectives"]:
            assert objective["title"] and objective["detail"]
    # Every objective names a check that exists.
    for mission in MISSIONS.values():
        for objective in mission.objectives:
            assert objective.check in CHECKS


def test_a_mission_fixes_the_market_everyone_meets(client):
    client.get("/api/v1/simulator")
    first = start(client)
    second = start(client)
    assert first["config"]["seed"] == second["config"]["seed"] == MISSIONS["first-order"].seed
    assert first["config"]["mission"] == "first-order"
    assert first["cursor"] == second["cursor"]
    assert [q["close"] for q in first["quotes"]] == [q["close"] for q in second["quotes"]]
    assert client.post(
        "/api/v1/simulator/runs", json={"id": ident(), "mission": "no-such-mission"}
    ).status_code == 404
    # Missions describe the generated market, not an imported dataset.
    assert client.post(
        "/api/v1/simulator/runs",
        json={"id": ident(), "mission": "first-order", "mode": "historical", "symbol": "X"},
    ).status_code == 422


def test_objectives_are_decided_from_the_run_and_not_from_profit(client):
    client.get("/api/v1/simulator")
    run = start(client)
    rid, version = run["id"], run["version"]
    route = f"/api/v1/simulator/runs/{rid}/mission"
    opening = client.get(route).json()
    assert opening["met"] == 0 and opening["complete"] is False
    assert [o["id"] for o in opening["objectives"]] == ["limit-entry", "thesis", "observe"]

    # A market order with no thesis meets neither of the first two objectives.
    response = client.post(
        f"/api/v1/simulator/runs/{rid}/orders",
        json={"id": ident(), "version": version, "symbol": "NVRA", "side": "buy", "quantity": 5},
    )
    version = response.json()["version"]
    after = client.get(route).json()
    assert after["met"] == 0
    assert "no written reason" in dict((o["id"], o["progress"]) for o in after["objectives"])["thesis"]

    # A limit order with a thesis meets the first; the second still fails because
    # the earlier order has no reason recorded.
    response = client.post(
        f"/api/v1/simulator/runs/{rid}/orders",
        json={
            "id": ident(),
            "version": version,
            "symbol": "NVRA",
            "side": "buy",
            "kind": "limit",
            "limit_price": "100.00",
            "quantity": 5,
            "note": "Only interested at 100.",
        },
    )
    version = response.json()["version"]
    marked = {o["id"]: o["met"] for o in client.get(route).json()["objectives"]}
    assert marked["limit-entry"] is True and marked["thesis"] is False

    # Advancing a session completes the third, whatever the position is worth.
    limiter.records.clear()
    client.post(
        f"/api/v1/simulator/runs/{rid}/advance",
        json={"id": ident(), "version": version, "steps": 390},
    )
    final = client.get(route).json()
    marked = {o["id"]: o["met"] for o in final["objectives"]}
    assert marked["observe"] is True
    assert final["complete"] is False  # the missing thesis still stands


def test_a_position_cap_is_judged_on_the_largest_holding_not_the_last(client):
    client.get("/api/v1/simulator")
    run = start(client, "position-size")
    rid, version = run["id"], run["version"]
    route = f"/api/v1/simulator/runs/{rid}/mission"
    # ZEPH trades near $20, so 600 shares is comfortably over 5% of $100,000.
    response = client.post(
        f"/api/v1/simulator/runs/{rid}/orders",
        json={
            "id": ident(),
            "version": version,
            "symbol": "ZEPH",
            "side": "buy",
            "quantity": 600,
            "note": "Deliberately oversized.",
        },
    )
    version = response.json()["version"]
    limiter.records.clear()
    version = client.post(
        f"/api/v1/simulator/runs/{rid}/advance",
        json={"id": ident(), "version": version, "steps": 60},
    ).json()["version"]
    cap = next(o for o in client.get(route).json()["objectives"] if o["id"] == "cap")
    assert cap["met"] is False and "exceeded" in cap["progress"]
    # Selling afterwards does not undo the breach: the peak is what is judged.
    response = client.post(
        f"/api/v1/simulator/runs/{rid}/orders",
        json={
            "id": ident(),
            "version": version,
            "symbol": "ZEPH",
            "side": "sell",
            "quantity": 600,
            "note": "Closing it.",
        },
    )
    version = response.json()["version"]
    limiter.records.clear()
    client.post(
        f"/api/v1/simulator/runs/{rid}/advance",
        json={"id": ident(), "version": version, "steps": 60},
    )
    cap = next(o for o in client.get(route).json()["objectives"] if o["id"] == "cap")
    assert cap["met"] is False


def test_a_run_without_a_mission_has_none(client):
    client.get("/api/v1/simulator")
    plain = client.post("/api/v1/simulator/runs", json={"id": ident()}).json()
    assert plain["config"].get("mission") is None
    assert client.get(f"/api/v1/simulator/runs/{plain['id']}/mission").status_code == 404
