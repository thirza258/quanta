from uuid import uuid4

import pytest
from quanta.domain.errors import DomainError
from quanta.domain.simulator import advance_state, reservations, validate_order
from test_api import signup


def ident():
    return str(uuid4())


def create(client, **changes):
    response = client.post("/api/v1/simulator/runs", json={"id": ident(), **changes})
    assert response.status_code == 200, response.text
    return response.json()


def mutate(client, run, action, **changes):
    return client.post(
        f"/api/v1/simulator/runs/{run['id']}/{action}",
        json={"id": ident(), "version": run["version"], **changes},
    )


def state():
    return {
        "config": {"commission": "1", "slippage_bps": "0", "spread_bps": "0", "participation": "1"},
        "cursor": 0,
        "cash": "100000.00",
        "realized": "0.00",
        "positions": {},
        "orders": [],
        "fills": [],
        "ledger": [],
    }


def bars(prices, volume=1000):
    return {
        "AAPL": [
            {
                "time": 1736173800 + i * 60,
                "open": p,
                "high": p + 1,
                "low": p - 1,
                "close": p,
                "volume": volume,
            }
            for i, p in enumerate(prices)
        ]
    }


def order(s, data, **changes):
    o = {
        "id": ident(),
        "symbol": "AAPL",
        "side": "buy",
        "kind": "market",
        "quantity": 10,
        "filled": 0,
        "status": "working",
        "limit_price": None,
        "stop_price": None,
        "tif": "GTC",
        "fee_remaining": "1.00",
        "triggered": False,
        "notional": "0.00",
        "note": "",
        "lesson": "",
        "day": "2025-01-06",
        **changes,
    }
    validate_order(s, data, o)
    s["orders"].append(o)
    return o


def test_exact_cash_ledger_round_trip():
    s = state()
    data = bars([99, 100, 110])
    order(s, data)
    assert s["cash"] == "100000.00"
    advance_state(s, data, 1)
    assert s["cash"] == "98999.00"
    assert s["positions"]["AAPL"] == {"quantity": 10, "cost": "1001.00"}
    order(s, data, side="sell")
    advance_state(s, data, 1)
    assert s["cash"] == "100098.00"
    assert s["realized"] == "98.00"
    assert s["positions"]["AAPL"] == {"quantity": 0, "cost": "0.00"}
    assert len(s["fills"]) == 2


def test_partial_fills_shared_volume_fee_once_and_reservations():
    s = state()
    data = bars([100] * 5, volume=3)
    first = order(s, data)
    second = order(s, data, quantity=2)
    advance_state(s, data, 1)
    assert first["filled"] == 3 and second["filled"] == 0
    assert first["status"] == "partially_filled"
    assert s["cash"] == "99699.00"
    assert str(reservations(s)[0]) == "901.00"
    advance_state(s, data, 1)
    assert s["fills"][-1]["fee"] == "0.00"
    first["status"] = "canceled"
    advance_state(s, data, 1)
    assert first["filled"] == 6 and second["filled"] == 2
    assert reservations(s)[0] == 0


def test_cash_and_share_reservations_prevent_overspending_and_overselling():
    s = state()
    data = bars([100] * 3)
    order(s, data, quantity=999)
    with pytest.raises(DomainError):
        order(s, data, quantity=2)
    with pytest.raises(DomainError):
        order(s, data, side="sell")
    advance_state(s, data, 1)
    order(s, data, side="sell", quantity=999)
    with pytest.raises(DomainError):
        order(s, data, side="sell", quantity=1)


def test_gap_fill_never_creates_borrowing():
    s = state()
    data = bars([100, 120, 125])
    o = order(s, data, quantity=999)
    advance_state(s, data, 1)
    assert s["cash"] == "39.00"
    assert o["filled"] == 833 and o["status"] == "canceled"


def test_limit_touch_stop_gap_and_stop_limit_conservative_sequence():
    s = state()
    data = bars([100, 101, 99, 95, 90])
    o = order(s, data, kind="limit", limit_price="100")
    advance_state(s, data, 1)
    assert o["filled"] == 0  # low only touches limit
    advance_state(s, data, 1)
    assert o["average"] == "99.00"
    stop = order(s, data, side="sell", kind="stop", stop_price="97")
    advance_state(s, data, 1)
    assert stop["average"] == "95.00"
    s = state()
    data = bars([100, 105, 106, 104])
    o = order(s, data, kind="stop_limit", stop_price="103", limit_price="104")
    advance_state(s, data, 1)
    assert o["triggered"] and o["filled"] == 0
    advance_state(s, data, 1)
    assert o["filled"] == 0
    advance_state(s, data, 1)
    assert o["average"] == "104.00"


def test_api_ownership_no_future_prices_idempotency_and_archive(client):
    signup(client)
    run = create(client)
    response = client.get(f"/api/v1/simulator/runs/{run['id']}/market?symbol=AAPL&interval=1m")
    assert response.status_code == 200
    assert len(response.json()["bars"]) == run["cursor"] + 1
    assert max(b["time"] for b in response.json()["bars"]) == run["clock"]
    body = {
        "id": ident(),
        "version": run["version"],
        "symbol": "AAPL",
        "side": "buy",
        "quantity": 10,
    }
    path = f"/api/v1/simulator/runs/{run['id']}/orders"
    placed = client.post(path, json=body).json()
    assert len(placed["orders"]) == 1
    assert client.post(path, json=body).json()["version"] == placed["version"]
    assert client.post(path, json={**body, "quantity": 11}).status_code == 409
    assert mutate(client, run, "advance").status_code == 409
    run = mutate(client, placed, "advance").json()
    assert run["positions"][0]["quantity"] == 10
    archived = run["id"]
    new = create(client)
    assert client.get(f"/api/v1/simulator/runs/{archived}").json()["fills"] == run["fills"]
    assert mutate(client, run, "advance").status_code == 409
    client.post("/api/v1/auth/logout")
    assert client.get(f"/api/v1/simulator/runs/{archived}").status_code == 404
    assert client.get(f"/api/v1/simulator/runs/{new['id']}").status_code == 404


def test_guest_isolation_and_account_preferences_do_not_touch_learning(client):
    client.get("/api/v1/simulator")
    guest = create(client)
    guest_cookie = client.cookies.get("quanta_trading_guest")
    signup(client)
    assert client.get(f"/api/v1/simulator/runs/{guest['id']}").status_code == 404
    run = create(client)
    prefs = {"symbol": "MSFT", "drawings": {"MSFT": [{"id": "test"}]}}
    response = client.put(
        f"/api/v1/simulator/runs/{run['id']}/preferences",
        json={"id": ident(), "version": run["version"], "preferences": prefs},
    )
    assert response.json()["preferences"] == prefs
    assert client.get("/api/v1/workspace").json()["state"] == {}
    client.post("/api/v1/auth/logout")
    assert client.cookies.get("quanta_trading_guest") == guest_cookie
    assert client.get("/api/v1/simulator").json()["run"]["id"] == guest["id"]


@pytest.mark.parametrize(
    "field,value",
    [
        ("quantity", 1.5),
        ("quantity", True),
        ("quantity", 0),
        ("quantity", -1),
        ("kind", "bracket"),
        ("side", "short"),
        ("balance", 1e9),
    ],
)
def test_invalid_orders_rejected(client, field, value):
    client.get("/api/v1/simulator")
    run = create(client)
    body = {"symbol": "AAPL", "side": "buy", "quantity": 10, field: value}
    assert mutate(client, run, "orders", **body).status_code == 422


def test_amend_cancel_and_missing_historical_dataset(client):
    client.get("/api/v1/simulator")
    run = create(client)
    placed = mutate(
        client, run, "orders", symbol="AAPL", side="buy", kind="limit", limit_price="1", quantity=10
    ).json()
    oid = placed["orders"][0]["id"]
    rejected = mutate(client, placed, f"orders/{oid}/amend", limit_price="100000")
    assert rejected.status_code == 422
    assert (
        client.get(f"/api/v1/simulator/runs/{run['id']}").json()["orders"][0]["limit_price"] == "1"
    )
    canceled = mutate(client, placed, f"orders/{oid}/cancel").json()
    assert canceled["reserved"] == "0.00"
    assert canceled["orders"][0]["status"] == "canceled"
    assert (
        client.post(
            "/api/v1/simulator/runs",
            json={"id": ident(), "mode": "historical", "symbol": "MISSING"},
        ).status_code
        == 422
    )


def test_reserved_price_rounds_up_and_expiry_releases_only_remaining():
    s = state()
    s["config"]["slippage_bps"] = "0.1"
    data = bars([100] * 4, volume=3)
    o = order(s, data, tif="DAY")
    assert str(reservations(s)[0]) == "1001.10"
    advance_state(s, data, 1)
    assert o["filled"] == 3
    # Next observation is a new modeled session; the old DAY remainder expires.
    data["AAPL"][2]["time"] += 86400
    advance_state(s, data, 1)
    assert o["status"] == "expired" and o["filled"] == 3
    assert reservations(s)[0] == 0


def test_sell_commission_cannot_create_borrowing():
    s = state()
    s["positions"] = {"AAPL": {"quantity": 1, "cost": "10.00"}}
    s["cash"] = "0.00"
    data = bars([10, 0.5])
    o = order(s, data, side="sell", quantity=1)
    advance_state(s, data, 1)
    assert o["status"] == "rejected"
    assert s["cash"] == "0.00" and s["positions"]["AAPL"]["quantity"] == 1


def test_historical_snapshot_daily_only_next_session_and_immutable(client, monkeypatch, tmp_path):
    import duckdb
    from quanta.services import data_store

    monkeypatch.setattr(data_store, "DATA_DIR", tmp_path)
    path = tmp_path / "TEST.parquet"
    with duckdb.connect() as db:
        db.execute(
            "COPY (SELECT DATE '2025-01-06' + CAST(i AS INTEGER) AS time, 100.0 AS open, 101.0 AS high, 99.0 AS low, 100.0 AS close, 10000 AS volume FROM range(40) t(i)) TO ? (FORMAT PARQUET)",
            [str(path)],
        )
    client.get("/api/v1/simulator")
    run = create(client, mode="historical", symbol="TEST", slippage_bps="0", spread_bps="0")
    route = f"/api/v1/simulator/runs/{run['id']}/market"
    observed = client.get(route, params={"symbol": "TEST", "interval": "1D"}).json()["bars"]
    assert len(observed) == 31
    from datetime import datetime
    from zoneinfo import ZoneInfo

    assert (
        datetime.fromtimestamp(observed[-1]["time"], ZoneInfo("America/New_York")).isoformat()
        == "2025-02-05T16:00:00-05:00"
    )
    assert client.get(route, params={"symbol": "TEST", "interval": "1m"}).status_code == 422
    placed = mutate(client, run, "orders", symbol="TEST", side="buy", quantity=10, tif="DAY").json()
    filled = mutate(client, placed, "advance").json()
    assert filled["cash"] == "98999.00"
    assert filled["orders"][0]["status"] == "filled"
    path.unlink()
    assert client.get(route, params={"symbol": "TEST", "interval": "1D"}).status_code == 200


def test_concurrent_order_writes_produce_one_fillable_order(client):
    from concurrent.futures import ThreadPoolExecutor

    client.get("/api/v1/simulator")
    run = create(client)

    def submit(_):
        return mutate(client, run, "orders", symbol="AAPL", side="buy", quantity=400)

    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(submit, range(2)))
    assert sorted(r.status_code for r in responses) == [200, 409]
    current = client.get(f"/api/v1/simulator/runs/{run['id']}").json()
    assert len(current["orders"]) == 1 and float(current["available"]) >= 0


def test_reset_identifier_is_idempotent_and_old_version_cannot_trade(client):
    client.get("/api/v1/simulator")
    old = create(client)
    body = {"id": ident(), "seed": 13}
    new = client.post("/api/v1/simulator/runs", json=body).json()
    assert client.post("/api/v1/simulator/runs", json=body).json()["id"] == new["id"]
    assert mutate(client, old, "orders", symbol="AAPL", side="buy", quantity=1).status_code == 409
    assert len(client.get("/api/v1/simulator").json()["runs"]) == 2


def test_market_reads_can_pin_clock_and_never_request_future(client):
    client.get("/api/v1/simulator")
    run = create(client)
    path = f"/api/v1/simulator/runs/{run['id']}/market"
    before = client.get(
        path, params={"symbol": "AAPL", "interval": "1h", "cursor": run["cursor"]}
    ).json()["bars"]
    assert mutate(client, run, "advance", steps=30).status_code == 200
    assert (
        client.get(
            path, params={"symbol": "AAPL", "interval": "1h", "cursor": run["cursor"]}
        ).json()["bars"]
        == before
    )
    current = client.get(path, params={"symbol": "AAPL", "cursor": 999999}).json()
    assert current["cursor"] == run["cursor"] + 30
    assert len(current["bars"]) == run["cursor"] + 31
