from uuid import uuid4

import pytest
from quanta.domain.errors import DomainError
from quanta.domain.simulator import advance_state, reservations, validate_order
from test_api import signup


# A fictional company from the simulator's generated universe.
SYMBOL = "NVRA"


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
    response = client.get(f"/api/v1/simulator/runs/{run['id']}/market?symbol={SYMBOL}&interval=1m")
    assert response.status_code == 200
    assert len(response.json()["bars"]) == run["cursor"] + 1
    assert max(b["time"] for b in response.json()["bars"]) == run["clock"]
    body = {
        "id": ident(),
        "version": run["version"],
        "symbol": SYMBOL,
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
    body = {"symbol": SYMBOL, "side": "buy", "quantity": 10, field: value}
    assert mutate(client, run, "orders", **body).status_code == 422


def test_amend_cancel_and_missing_historical_dataset(client):
    client.get("/api/v1/simulator")
    run = create(client)
    placed = mutate(
        client, run, "orders", symbol=SYMBOL, side="buy", kind="limit", limit_price="1", quantity=10
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
        return mutate(client, run, "orders", symbol=SYMBOL, side="buy", quantity=400)

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
    assert mutate(client, old, "orders", symbol=SYMBOL, side="buy", quantity=1).status_code == 409
    assert len(client.get("/api/v1/simulator").json()["runs"]) == 2


def test_market_reads_can_pin_clock_and_never_request_future(client):
    client.get("/api/v1/simulator")
    run = create(client)
    path = f"/api/v1/simulator/runs/{run['id']}/market"
    before = client.get(
        path, params={"symbol": SYMBOL, "interval": "1h", "cursor": run["cursor"]}
    ).json()["bars"]
    assert mutate(client, run, "advance", steps=30).status_code == 200
    assert (
        client.get(
            path, params={"symbol": SYMBOL, "interval": "1h", "cursor": run["cursor"]}
        ).json()["bars"]
        == before
    )
    current = client.get(path, params={"symbol": SYMBOL, "cursor": 999999}).json()
    assert current["cursor"] == run["cursor"] + 30
    assert len(current["bars"]) == run["cursor"] + 31


def test_generated_market_is_reproducible_and_differs_between_runs(client):
    client.get("/api/v1/simulator")
    first, second = create(client), create(client)
    assert first["config"]["universe"] == "quanta-sim-v2"
    # A run with no requested seed derives one from its identifier, so two paper
    # accounts get different markets while a retry of either reproduces its own.
    assert first["config"]["seed"] != second["config"]["seed"]
    route = f"/api/v1/simulator/runs/{second['id']}/market"
    bars = client.get(route, params={"symbol": SYMBOL}).json()["bars"]
    assert bars == client.get(route, params={"symbol": SYMBOL}).json()["bars"]
    assert len(second["quotes"]) == 32
    assert all(q["sector"] for q in second["quotes"])
    for bar in bars[::97]:
        assert bar["low"] <= min(bar["open"], bar["close"])
        assert bar["high"] >= max(bar["open"], bar["close"])
        assert bar["low"] > 0 and bar["volume"] > 0
    pinned = create(client, seed=4242)
    assert pinned["config"]["seed"] == 4242
    other = create(client, seed=4242)
    assert [q["close"] for q in pinned["quotes"]] == [q["close"] for q in other["quotes"]]


def test_news_streams_with_the_clock_and_never_releases_future_headlines(client):
    client.get("/api/v1/simulator")
    run = create(client, seed=11)
    route = f"/api/v1/simulator/runs/{run['id']}/news"
    opening = client.get(route).json()
    assert opening["available"] and opening["items"]
    assert max(item["index"] for item in opening["items"]) <= run["cursor"]
    assert {item["scope"] for item in opening["items"]} <= {"company", "sector", "macro", "market"}
    advanced = mutate(client, run, "advance", steps=390).json()
    later = client.get(route).json()
    assert max(item["index"] for item in later["items"]) <= advanced["cursor"]
    assert later["items"][0]["index"] > opening["items"][0]["index"]
    filtered = client.get(route, params={"symbol": "VLOC", "limit": 200}).json()["items"]
    assert filtered and all(
        item["symbol"] == "VLOC" or item["scope"] in ("macro", "market", "sector")
        for item in filtered
    )
    assert client.get(route, params={"symbol": "NOPE"}).status_code == 404


def test_simulated_news_moves_the_generated_prices():
    import numpy as np
    from quanta.services.simulator_market import newsroom, simulated_market

    data, room = simulated_market(11), newsroom(11)
    ratios = []
    for symbol in {e["symbol"] for e in room.events if e["impact"] == "high" and e["symbol"]}:
        moves = np.abs(np.diff(np.log(data[symbol].close)))
        bars = [
            e["index"]
            for e in room.events
            if e["symbol"] == symbol and e["impact"] == "high" and 0 < e["index"] < len(moves)
        ]
        if bars:
            ratios.append(float(np.mean(moves[bars]) / moves.mean()))
    # A high-impact headline is visible in its own bar, not merely printed beside it.
    assert len(ratios) >= 5
    assert float(np.mean(ratios)) > 1.8


def test_reported_quarters_are_released_by_the_newsroom_and_tie_together(client):
    client.get("/api/v1/simulator")
    run = create(client, seed=11)
    route = f"/api/v1/simulator/runs/{run['id']}/fundamentals"
    report = client.get(route, params={"symbol": SYMBOL}).json()
    assert [q["label"] for q in report["quarters"]][-1] == "Q3 2024"
    assert report["upcoming"]["label"] == "Q4 2024"
    # Before the print, only the expectation is published.
    assert set(report["upcoming"]) == {
        "label",
        "time",
        "bars_away",
        "consensus_eps",
        "consensus_revenue",
    }
    # Only descriptive facts are published. The margin, growth and leverage
    # assumptions that generate a quarter would make an unreleased result solvable.
    assert set(report["structure"]) == {
        "shares",
        "employees",
        "fiscal_year_end",
        "development_stage",
    }
    previous = None
    for quarter in report["quarters"]:
        assert abs(quarter["total_assets"] - quarter["total_liabilities"] - quarter["equity"]) < 1e-6
        assert quarter["gross_profit"] == pytest.approx(
            quarter["revenue"] - quarter["cost_of_revenue"]
        )
        assert quarter["free_cash_flow"] == pytest.approx(
            quarter["operating_cash_flow"] - quarter["capital_expenditure"]
        )
        # Closing cash is the roll-forward, with any shortfall raised as financing.
        assert quarter["cash"] == pytest.approx(
            quarter["opening_cash"]
            + quarter["operating_cash_flow"]
            - quarter["capital_expenditure"]
            - quarter["dividends_paid"]
            - quarter["buybacks"]
            + quarter["external_financing"]
        )
        if previous:
            assert quarter["opening_cash"] == pytest.approx(previous["cash"])
        previous = quarter
    assert report["valuation"]["price_earnings"] > 0
    assert report["valuation"]["market_capitalization"] == pytest.approx(
        report["valuation"]["price"] * report["valuation"]["shares"]
    )
    run = mutate(client, run, "advance", steps=1950).json()
    after = client.get(route, params={"symbol": SYMBOL}).json()
    assert [q["label"] for q in after["quarters"]][-1] == "Q4 2024"
    assert after["quarters"][-1]["index"] <= run["cursor"]
    assert after["quarters"][-1]["consensus_eps"]
    assert client.get(route, params={"symbol": "NOPE"}).status_code == 404


def test_imported_historical_prices_never_receive_invented_news(client, monkeypatch, tmp_path):
    import duckdb
    from quanta.services import data_store

    monkeypatch.setattr(data_store, "DATA_DIR", tmp_path)
    with duckdb.connect() as db:
        db.execute(
            "COPY (SELECT DATE '2025-01-06' + CAST(i AS INTEGER) AS time, 100.0 AS open, "
            "101.0 AS high, 99.0 AS low, 100.0 AS close, 10000 AS volume FROM range(40) t(i)) "
            "TO ? (FORMAT PARQUET)",
            [str(tmp_path / "TEST.parquet")],
        )
    client.get("/api/v1/simulator")
    run = create(client, mode="historical", symbol="TEST")
    news = client.get(f"/api/v1/simulator/runs/{run['id']}/news").json()
    assert news["available"] is False and news["items"] == []
    assert "historical" in news["notice"]
    assert (
        client.get(
            f"/api/v1/simulator/runs/{run['id']}/fundamentals", params={"symbol": "TEST"}
        ).status_code
        == 422
    )


def test_runs_created_before_the_fictional_universe_replay_the_original_paths():
    from quanta.services.simulator_market import markets

    data = markets({"config": {"mode": "synthetic", "seed": 42}}, None)
    assert list(data) == ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "META"]
    assert data["AAPL"][0] == {
        "time": 1736173800,
        "open": 223.81,
        "high": 223.9,
        "low": 223.67,
        "close": 223.74,
        "volume": 26132,
    }
    assert data["META"][5]["close"] == 530.53


def test_indicator_series_match_the_definitions_the_courses_teach():
    from quanta.services.simulator_desk import (
        ema_series,
        macd_series,
        rsi_series,
        sma_series,
    )

    assert sma_series([1, 2, 3, 4, 5], 3) == [None, None, 2, 3, 4]
    assert ema_series([1, 2, 3, 4, 8], 3) == [None, None, 2, 3, 5.5]
    assert ema_series([1, 2], 3) == [None, None]
    assert rsi_series([1, 2, 3, 4], 3) == [None, None, None, 100]
    assert rsi_series([4, 3, 2, 1], 3) == [None, None, None, 0]
    assert rsi_series([2, 2, 2, 2], 3) == [None, None, None, 50]
    assert rsi_series([1, 3, 2, 4, 3], 3)[4] == pytest.approx(61.5384615385)
    computed = macd_series([1, 2, 3, 4, 5, 6], 2, 3, 2)
    assert computed["line"] == [None, None, 0.5, 0.5, 0.5, 0.5]
    assert computed["signal"] == [None, None, None, 0.5, 0.5, 0.5]
    assert computed["histogram"] == [None, None, None, 0, 0, 0]
    # A later observation never rewrites an earlier indicator value.
    values = [101, 103, 99, 98, 105, 104, 109, 102]
    for series in (sma_series, ema_series, rsi_series):
        assert series(values, 3)[:6] == series(values[:6], 3)


def test_market_endpoint_computes_the_overlays_the_chart_draws(client):
    client.get("/api/v1/simulator")
    run = create(client, seed=11)
    route = f"/api/v1/simulator/runs/{run['id']}/market"
    body = client.get(
        route, params={"symbol": SYMBOL, "indicators": "SMA:20,RSI:14,MACD:12:26:9,BOGUS:5"}
    ).json()
    overlays = body["indicators"]
    assert set(overlays) == {"SMA:20", "RSI:14", "MACD:12:26:9"}
    assert len(overlays["SMA:20"]["values"]) == len(body["bars"])
    assert overlays["SMA:20"]["values"][:19] == [None] * 19
    assert overlays["SMA:20"]["values"][19] == pytest.approx(
        sum(b["close"] for b in body["bars"][:20]) / 20
    )
    assert set(overlays["MACD:12:26:9"]) == {"kind", "line", "signal", "histogram"}
    # Overlays follow the aggregated bars a coarser interval returns.
    hourly = client.get(
        route, params={"symbol": SYMBOL, "interval": "1h", "indicators": "SMA:20"}
    ).json()
    assert len(hourly["indicators"]["SMA:20"]["values"]) == len(hourly["bars"])


def test_desk_and_analytics_are_calculated_by_the_api(client):
    client.get("/api/v1/simulator")
    run = create(client, seed=11)
    placed = mutate(client, run, "orders", symbol=SYMBOL, side="buy", quantity=100).json()
    advanced = mutate(client, placed, "advance", steps=800).json()
    view = client.get(f"/api/v1/simulator/runs/{run['id']}/desk").json()
    movers, performance = view["movers"], view["performance"]
    assert len(movers["gainers"]) == 6 and len(movers["losers"]) == 6
    assert movers["gainers"][0]["change_pct"] >= movers["gainers"][-1]["change_pct"]
    assert movers["losers"][0]["change_pct"] <= movers["losers"][-1]["change_pct"]
    assert sum(movers["breadth"][key] for key in ("advancing", "declining", "unchanged")) == 32
    assert {s["sector"] for s in movers["sectors"]} and all(
        s["companies"] >= 1 for s in movers["sectors"]
    )
    assert performance["bars_observed"] == advanced["cursor"] + 1
    assert performance["curve"][0]["equity"] == 100000.0
    assert performance["equity"] == pytest.approx(float(advanced["equity"]), abs=0.02)
    assert performance["attribution"][0]["symbol"] == SYMBOL
    assert performance["attribution"][0]["quantity"] == 100
    assert performance["max_drawdown"] <= 0
    stats = client.get(
        f"/api/v1/simulator/runs/{run['id']}/analytics", params={"symbol": SYMBOL}
    ).json()
    assert stats["indicators"]["sma_20"] and 0 <= stats["indicators"]["rsi_14"] <= 100
    assert stats["risk"]["beta"] is not None and stats["risk"]["observations"] > 100
    assert stats["sentiment"]["session"]["window_bars"] <= 390
    assert (
        client.get(
            f"/api/v1/simulator/runs/{run['id']}/analytics", params={"symbol": "NOPE"}
        ).status_code
        == 404
    )


def test_a_run_from_before_the_universe_still_serves_every_new_endpoint(client):
    """An account created before the fictional companies keeps working."""
    from sqlalchemy.orm.attributes import flag_modified
    from sqlmodel import Session

    from quanta.db.models import TradingRun
    from quanta.db.session import engine

    client.get("/api/v1/simulator")
    run = create(client, seed=42)
    with Session(engine) as db:
        row = db.get(TradingRun, run["id"])
        state = dict(row.state)
        state["config"] = {key: value for key, value in state["config"].items() if key != "universe"}
        row.state = state
        flag_modified(row, "state")
        db.add(row)
        db.commit()
    base = f"/api/v1/simulator/runs/{run['id']}"
    snapshot = client.get(base).json()
    assert [q["symbol"] for q in snapshot["quotes"]] == [
        "AAPL",
        "MSFT",
        "NVDA",
        "TSLA",
        "AMZN",
        "META",
    ]
    assert snapshot["universe"] is None
    market = client.get(base + "/market", params={"symbol": "AAPL", "indicators": "SMA:20"}).json()
    assert len(market["indicators"]["SMA:20"]["values"]) == len(market["bars"])
    news = client.get(base + "/news").json()
    assert news["available"] is False and "predates" in news["notice"]
    assert client.get(base + "/fundamentals", params={"symbol": "AAPL"}).status_code == 422
    # Screening and risk still work; only the tone blocks are absent.
    desk = client.get(base + "/desk").json()
    movers = desk["movers"]
    assert all(row["sentiment"] is None for row in movers["gainers"] + movers["losers"])
    assert desk["performance"]["equity"] == 100000.0
    stats = client.get(base + "/analytics", params={"symbol": "AAPL"}).json()
    assert stats["sentiment"] is None and stats["risk"]["beta"] is not None
    # The screener must measure change exactly as the watchlist does.
    watchlist = {q["symbol"]: q["change_pct"] for q in snapshot["quotes"]}
    for row in movers["gainers"] + movers["losers"] + movers["active"]:
        assert row["change_pct"] == watchlist[row["symbol"]]
    assert all(row["change_pct"] > 0 for row in movers["gainers"])
    assert all(row["change_pct"] < 0 for row in movers["losers"])
    assert not {r["symbol"] for r in movers["gainers"]} & {r["symbol"] for r in movers["losers"]}
    # A generated run names fictional companies; this one prints real names.
    assert "fictional companies" not in snapshot["disclosure"]
    assert "not observed market data" in snapshot["disclosure"]



def test_a_beat_is_above_consensus_even_when_the_company_loses_money():
    """A development-stage print must not invert the direction of its surprise."""
    from quanta.services.simulator_market import newsroom

    losses = beats = 0
    for seed in (1, 11, 424242, 999983):
        room = newsroom(seed)
        for book in room.books.values():
            quarter = book[-1]
            if quarter.get("eps_surprise") is None:
                continue
            above = quarter["eps"] > quarter["consensus_eps"]
            assert above == (quarter["eps_surprise"] > 0)
            if quarter["eps"] < 0:
                losses += 1
                beats += above
    assert losses >= 8 and 0 < beats < losses


def test_an_unreleased_quarter_cannot_be_solved_for_from_its_consensus(client):
    """Nothing published before a print reduces to the result it will report."""
    import statistics

    from quanta.services.simulator_market import newsroom

    client.get("/api/v1/simulator")
    run = create(client, seed=11)
    report = client.get(
        f"/api/v1/simulator/runs/{run['id']}/fundamentals", params={"symbol": SYMBOL}
    ).json()
    # Before the print a learner sees the expectation and its date, nothing else.
    assert set(report["upcoming"]) == {
        "label",
        "time",
        "bars_away",
        "consensus_eps",
        "consensus_revenue",
    }
    assert all(q["index"] < 0 for q in report["quarters"])
    # The revenue and earnings estimates carry independent error, so neither the
    # surprise nor the other estimate can be derived from one of them.
    room = newsroom(11)
    ratios = []
    for book in room.books.values():
        quarter = book[-1]
        if quarter.get("eps_surprise") is None or abs(quarter["revenue_surprise"]) < 1e-9:
            continue
        ratios.append(quarter["eps_surprise"] / quarter["revenue_surprise"])
    assert len(ratios) >= 20
    assert statistics.pstdev(ratios) > 0.2


def test_a_daily_replay_is_annualized_over_days_not_minutes(client, monkeypatch, tmp_path):
    import duckdb
    from quanta.services import data_store

    monkeypatch.setattr(data_store, "DATA_DIR", tmp_path)
    with duckdb.connect() as db:
        db.execute(
            "COPY (SELECT DATE '2025-01-06' + CAST(i AS INTEGER) AS time, 100.0 AS open, "
            "101.5 AS high, 99.0 AS low, CASE WHEN i % 2 = 0 THEN 100.0 ELSE 101.0 END AS close, "
            "10000 AS volume FROM range(40) t(i)) TO ? (FORMAT PARQUET)",
            [str(tmp_path / "DAILY.parquet")],
        )
    client.get("/api/v1/simulator")
    run = create(client, mode="historical", symbol="DAILY")
    stats = client.get(
        f"/api/v1/simulator/runs/{run['id']}/analytics", params={"symbol": "DAILY"}
    ).json()
    # Alternating 1% daily closes annualize to roughly 16%, not 16% x sqrt(390).
    assert 0.10 < stats["risk"]["volatility_short"] < 0.25
    assert stats["risk"]["short_window_bars"] == 20
    assert stats["momentum"]["session"] is not None
    # One instrument is not a market to measure a beta against.
    assert stats["risk"]["beta"] is None
    desk = client.get(f"/api/v1/simulator/runs/{run['id']}/desk").json()
    rows = desk["movers"]["gainers"] + desk["movers"]["losers"]
    assert len(rows) == 1 and 0.10 < rows[0]["volatility"] < 0.25
    # Imported prices are never described as fictional companies.
    for text in (stats["disclosure"], desk["disclosure"], run["disclosure"]):
        assert "Imported historical" in text and "fictional" not in text


def test_the_calendar_names_what_is_coming_without_revealing_it(client):
    client.get("/api/v1/simulator")
    run = create(client, seed=11)
    base = f"/api/v1/simulator/runs/{run['id']}"
    board = client.get(base + "/calendar").json()
    assert board["economic"] and board["earnings"]
    scheduled = [item for item in board["economic"] if not item["released"]]
    assert scheduled, "a fresh run has releases still ahead of it"
    # An appointment is public; its result is not.
    assert all(item["headline"] is None and item["sentiment"] is None for item in scheduled)
    assert all(item["name"] and item["time"] for item in scheduled)
    assert all(item["headline"] for item in board["economic"] if item["released"])
    pending = [item for item in board["earnings"] if not item["released"]]
    assert len(pending) == 32
    for item in pending:
        assert item["consensus_eps"] and item["bars_away"] > 0
        assert "eps" not in item and "eps_surprise" not in item
    # Advancing releases them, outcome and all.
    run = mutate(client, run, "advance", steps=1950).json()
    later = client.get(base + "/calendar").json()
    reported = [item for item in later["earnings"] if item["released"]]
    assert reported and all(
        item["eps"] is not None and item["eps_surprise"] is not None for item in reported
    )
    assert all(item["index"] <= run["cursor"] for item in later["earnings"] if item["released"])
    # A horizon keeps the board short without letting anything extra through.
    near = client.get(base + "/calendar", params={"ahead": 400}).json()
    assert all(item["index"] <= run["cursor"] + 400 for item in near["economic"])
    assert len(near["economic"]) < len(later["economic"])


def test_peers_compare_a_company_with_its_sector(client):
    client.get("/api/v1/simulator")
    run = create(client, seed=11)
    report = client.get(
        f"/api/v1/simulator/runs/{run['id']}/fundamentals", params={"symbol": SYMBOL}
    ).json()
    peers = report["peers"]
    assert peers["sector"] == "Semiconductors"
    symbols = {row["symbol"] for row in peers["rows"]}
    assert symbols == {"NVRA", "SILQ"}
    assert sum(row["self"] for row in peers["rows"]) == 1
    # Ranked by size, and each row is priced at that company's own mark.
    caps = [row["market_capitalization"] for row in peers["rows"]]
    assert caps == sorted(caps, reverse=True)
    assert all(row["reported_quarters"] == 8 for row in peers["rows"])
    assert peers["median"]["price_earnings"] > 0
    # A development-stage company has no P/E, and the median skips it rather than
    # treating the gap as a zero.
    other = client.get(
        f"/api/v1/simulator/runs/{run['id']}/fundamentals", params={"symbol": "QBIT"}
    ).json()["peers"]
    assert other["sector"] == "Software"
    assert any(row["price_earnings"] is None for row in other["rows"])
    assert other["median"]["price_earnings"] > 0


def test_a_run_without_a_newsroom_has_no_calendar(client, monkeypatch, tmp_path):
    import duckdb

    from quanta.services import data_store

    monkeypatch.setattr(data_store, "DATA_DIR", tmp_path)
    with duckdb.connect() as db:
        db.execute(
            "COPY (SELECT DATE '2025-01-06' + CAST(i AS INTEGER) AS time, 100.0 AS open, "
            "101.0 AS high, 99.0 AS low, 100.0 AS close, 10000 AS volume FROM range(40) t(i)) "
            "TO ? (FORMAT PARQUET)",
            [str(tmp_path / "CAL.parquet")],
        )
    client.get("/api/v1/simulator")
    run = create(client, mode="historical", symbol="CAL")
    assert client.get(f"/api/v1/simulator/runs/{run['id']}/calendar").status_code == 422
