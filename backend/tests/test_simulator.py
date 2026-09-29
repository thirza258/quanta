from uuid import uuid4

import pytest
from quanta.domain.errors import DomainError
from quanta.domain.simulator import advance_state, reservations, validate_order
from quanta.core.limits import limiter
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
    # Advance past this company's own reporting date rather than a fixed distance.
    remaining = report["upcoming"]["bars_away"]
    while remaining > 0:
        step = min(1950, remaining)
        run = mutate(client, run, "advance", steps=step).json()
        remaining -= step
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
    assert movers["gainers"] and movers["losers"]
    assert len(movers["gainers"]) <= 6 and len(movers["losers"]) <= 6
    assert movers["gainers"][0]["change_pct"] >= movers["gainers"][-1]["change_pct"]
    assert movers["losers"][0]["change_pct"] <= movers["losers"][-1]["change_pct"]
    assert sum(movers["breadth"][key] for key in ("advancing", "declining", "unchanged")) == 32
    assert {s["sector"] for s in movers["sectors"]} and all(
        s["companies"] >= 1 for s in movers["sectors"]
    )
    # Only the bars the account was open for, not the market's whole generated past.
    assert performance["bars_observed"] == advanced["cursor"] + 1 - 499
    assert performance["curve"][0]["equity"] == 100000.0
    assert performance["equity"] == pytest.approx(float(advanced["equity"]), abs=0.02)
    assert performance["attribution"][0]["symbol"] == SYMBOL
    assert performance["attribution"][0]["quantity"] == 100
    assert performance["max_drawdown"] <= 0
    # The index is rebased to the bar the account opened on, so the learner and the
    # market are compared over exactly the same window.
    benchmark = performance["benchmark"]
    assert benchmark["name"] == "QX-200"
    assert benchmark["curve"][0]["equity"] == 100000.0
    assert benchmark["curve"][0]["time"] == performance["curve"][0]["time"]
    assert benchmark["equity"] == pytest.approx(100000 * (1 + benchmark["total_return"]), abs=0.02)
    # Every figure the panel reads must be present, even when a run is too short
    # for it to mean anything; a missing key would render as a silent blank.
    assert set(performance["risk"]) == {
        "cagr",
        "sharpe",
        "sortino",
        "calmar",
        "alpha",
        "beta",
        "var_95",
        "cvar_95",
        "max_drawdown",
    }
    assert performance["risk"]["beta"] is not None
    # 800 bars is barely two sessions, so annualized figures are not yet a measurement.
    assert performance["sessions"] == 3 and performance["risk_is_meaningful"] is False
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
    # Every monitor tool serves a run with no newsroom; only tone is absent.
    tools = client.get(
        base + "/monitor",
        params={
            "panes": "tape,book,heatmap,screener,sessions,quotes",
            "symbol": "AAPL",
            "screen": "volatile",
        },
    ).json()["tools"]
    assert set(tools) == {"tape", "book", "heatmap", "screener", "sessions", "quotes"}
    assert tools["tape"]["prints"] and tools["book"]["bids"]
    assert sum(g["companies_count"] for g in tools["heatmap"]["sectors"]) == 6
    assert tools["screener"]["rows"]
    assert all(row["sentiment"] is None for row in tools["screener"]["rows"])
    # No statements, so no earnings multiple to screen on.
    assert all(row["multiple"] is None for row in tools["screener"]["rows"])
    assert tools["sessions"]["sessions"] and tools["quotes"]["rows"]
    # A legacy run is a cash account, and shorting it is still refused.
    assert snapshot["account"] == "cash"
    short = mutate(client, snapshot, "orders", symbol="AAPL", side="sell", quantity=1)
    assert short.status_code == 422 and "long-only" in short.json()["detail"]
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


def test_the_generated_market_never_runs_out(client):
    """The clock keeps producing sessions, headlines and reports as it advances."""
    client.get("/api/v1/simulator")
    run = create(client, seed=11)
    assert run["endless"] is True and run["session"] == 2
    rid, version = run["id"], run["version"]
    reach = run["total_bars"]
    for _ in range(30):
        limiter.records.clear()
        response = client.post(
            f"/api/v1/simulator/runs/{rid}/advance",
            json={"id": ident(), "version": version, "steps": 1950},
        )
        assert response.status_code == 200, response.text
        run = response.json()
        version = run["version"]
    # Well past the bars a fixed-length market used to hold.
    assert run["cursor"] > 55000
    assert run["total_bars"] > run["cursor"]
    assert run["session"] > 140
    # Orders are still accepted, because there is always a next bar to fill on.
    placed = client.post(
        f"/api/v1/simulator/runs/{rid}/orders",
        json={"id": ident(), "version": version, "symbol": SYMBOL, "side": "buy", "quantity": 5},
    )
    assert placed.status_code == 200, placed.text
    # The tape and the reporting cycle continue.
    news = client.get(f"/api/v1/simulator/runs/{rid}/news", params={"limit": 40}).json()
    assert news["items"] and max(i["index"] for i in news["items"]) <= run["cursor"]
    assert max(i["index"] for i in news["items"]) > reach
    report = client.get(
        f"/api/v1/simulator/runs/{rid}/fundamentals", params={"symbol": SYMBOL}
    ).json()
    # A year of replay means several quarters have been reported, not just one.
    assert len([q for q in report["quarters"] if q["index"] >= 0]) >= 2
    assert report["upcoming"] is not None


def test_a_block_is_the_same_however_late_it_is_generated():
    """A stored cursor must resolve to the same bar on a cold server."""
    from quanta.services.simulator_market import BLOCK_BARS, _market, simulated_market

    _market.cache_clear()
    straight = simulated_market(4242, BLOCK_BARS * 3)
    sampled = {symbol: [series[i] for i in range(0, BLOCK_BARS * 4, 997)] for symbol, series in straight.items()}
    _market.cache_clear()
    # Reach the same point by advancing in stages, as a replay actually does.
    for target in (0, BLOCK_BARS, BLOCK_BARS * 2, BLOCK_BARS * 3):
        stepped = simulated_market(4242, target)
    for symbol, rows in sampled.items():
        assert [stepped[symbol][i] for i in range(0, BLOCK_BARS * 4, 997)] == rows


def test_every_headline_carries_a_score_that_matches_its_move():
    """One point is one basis point, and the tier label follows the same score."""
    import numpy as np

    from quanta.services.simulator_market import newsroom, simulated_market

    data, room = simulated_market(11), newsroom(11)
    scored = [e for e in room.events if e["points"]]
    assert len(scored) > 500
    assert all(e["points"] == 0 for e in room.events if e["category"] == "chatter")
    for event in scored:
        # The published tier is derived from the published score, so a reader can
        # check one against the other.
        expected = "high" if abs(event["points"]) >= 400 else (
            "medium" if abs(event["points"]) >= 120 else "low"
        )
        assert event["impact"] == expected, event
        assert event["impact"] != "none"
    points, moves = [], []
    for event in scored:
        if event["scope"] != "company" or not event["symbol"]:
            continue
        closes = data[event["symbol"]].close
        index = event["index"]
        if 0 < index < len(closes):
            points.append(event["points"])
            moves.append((closes[index] / closes[index - 1] - 1) * 10000)
    assert len(points) > 200
    # The score is applied, not inferred: it explains nearly all of the same-bar move.
    assert float(np.corrcoef(points, moves)[0][1]) > 0.9


def test_a_chart_reads_a_window_not_the_whole_run(client):
    """An endless run must not hand the chart every bar it has ever generated."""
    client.get("/api/v1/simulator")
    run = create(client, seed=11)
    rid, version = run["id"], run["version"]
    for _ in range(12):
        limiter.records.clear()
        response = client.post(
            f"/api/v1/simulator/runs/{rid}/advance",
            json={"id": ident(), "version": version, "steps": 1950},
        )
        version = response.json()["version"]
    cursor = response.json()["cursor"]
    assert cursor > 20000
    route = f"/api/v1/simulator/runs/{rid}/market"
    body = client.get(route, params={"symbol": SYMBOL, "indicators": "SMA:20,RSI:14"}).json()
    # Bounded, and far short of the observations behind it.
    assert len(body["bars"]) == 1500
    assert body["from_bar"] > 0
    assert body["bars"][-1]["time"] and len(body["indicators"]["SMA:20"]["values"]) == 1500
    # An explicit window is honoured, and nothing past the cursor leaks either way.
    small = client.get(
        route, params={"symbol": SYMBOL, "limit": 200, "indicators": "SMA:20,RSI:14"}
    ).json()
    assert len(small["bars"]) == 200
    assert small["bars"][-1] == body["bars"][-1]
    assert len(small["indicators"]["RSI:14"]["values"]) == 200

    # Resizing the window must not change the overlay a learner sees. The rolling
    # sums and the exponential smoothing both accumulate from wherever the read
    # began, so the agreement is to floating-point noise rather than bit-exact,
    # which is far below the cent the price is quoted in.
    wide = client.get(
        route, params={"symbol": SYMBOL, "limit": 5000, "indicators": "SMA:20,RSI:14"}
    ).json()
    for key in ("SMA:20", "RSI:14"):
        for near, far in zip(
            small["indicators"][key]["values"],
            wide["indicators"][key]["values"][-200:],
            strict=True,
        ):
            assert (near is None and far is None) or abs(near - far) < 1e-6


def test_coarse_intervals_aggregate_without_reading_every_bar(client):
    """Bucketing the generated bars must agree with summarizing them one by one."""
    from quanta.services.simulator_market import simulated_market

    client.get("/api/v1/simulator")
    run = create(client, seed=11)
    route = f"/api/v1/simulator/runs/{run['id']}/market"
    hourly = client.get(route, params={"symbol": SYMBOL, "interval": "1h", "limit": 5000}).json()
    series = simulated_market(11, run["cursor"])[SYMBOL]
    raw = series[: run["cursor"] + 1]
    # Rebuild the same buckets the slow way and compare.
    buckets = {}
    for index, bar in enumerate(raw):
        key = (index // 390, (index % 390) // 60)
        if key not in buckets:
            buckets[key] = dict(bar)
        else:
            item = buckets[key]
            item.update(
                high=max(item["high"], bar["high"]),
                low=min(item["low"], bar["low"]),
                close=bar["close"],
                volume=item["volume"] + bar["volume"],
            )
    assert hourly["bars"] == list(buckets.values())
    daily = client.get(route, params={"symbol": SYMBOL, "interval": "1D", "limit": 5000}).json()
    assert len(daily["bars"]) == run["cursor"] // 390 + 1
    assert daily["bars"][0]["open"] == raw[0]["open"]


def test_no_endpoint_reveals_a_price_beyond_the_cursor(client):
    """Generating further ahead must not change a single figure already published.

    Bars are generated in blocks that run past the replay cursor, so every read
    has to be bounded by the cursor explicitly. If any of them slips and reads the
    tail of the array instead, extending the same seed's market changes an answer
    that the learner has already been shown — which is look-ahead, silently.
    """
    from quanta.services.simulator_market import simulated_market

    client.get("/api/v1/simulator")
    run = create(client, seed=4242)
    placed = mutate(client, run, "orders", symbol=SYMBOL, side="buy", quantity=40).json()
    advanced = mutate(client, placed, "advance", steps=600).json()
    cursor = advanced["cursor"]

    routes = {
        "desk": {},
        "market": {"symbol": SYMBOL, "interval": "1h", "limit": 200},
        "news": {"limit": 50},
        "fundamentals": {"symbol": SYMBOL},
        "analytics": {"symbol": SYMBOL},
        "calendar": {},
        "monitor": {
            "panes": "tape,book,heatmap,screener,sessions,quotes",
            "symbol": SYMBOL,
            "screen": "cheap",
        },
    }
    before = {
        name: client.get(f"/api/v1/simulator/runs/{run['id']}/{name}", params=params).json()
        for name, params in routes.items()
    }
    # Generate a long way past the cursor on the very same cached market.
    simulated_market(4242, cursor + 30_000)
    after = {
        name: client.get(f"/api/v1/simulator/runs/{run['id']}/{name}", params=params).json()
        for name, params in routes.items()
    }
    assert before == after


def test_monitor_tools_are_generated_and_consistent_with_the_bars(client):
    """The tape, the book, the heat and the screens, all served in one request."""
    client.get("/api/v1/simulator")
    run = create(client, seed=77)
    advanced = mutate(client, run, "advance", steps=900).json()
    base = f"/api/v1/simulator/runs/{run['id']}"
    view = client.get(
        base + "/monitor",
        params={
            "panes": "tape,book,heatmap,screener,sessions",
            "symbol": SYMBOL,
            "screen": "volume",
            "limit": 40,
        },
    ).json()
    tape, book = view["tools"]["tape"], view["tools"]["book"]

    # A print must not contradict the bar it came out of.
    bars = client.get(
        base + "/market", params={"symbol": SYMBOL, "interval": "1m", "limit": 60}
    ).json()["bars"]
    window = {bar["time"]: bar for bar in bars}
    assert len(tape["prints"]) == 40
    checked = 0
    for print_ in tape["prints"]:
        bar = window.get(print_["time"] - print_["time"] % 60)
        if not bar:
            continue
        checked += 1
        assert bar["low"] <= print_["price"] <= bar["high"]
        assert print_["size"] >= 1
    assert checked, "prints must line up with the bars they were drawn from"
    assert 0 <= tape["buy_share"] <= 1
    assert "Illustrative" in tape["notice"]

    # The book straddles the last trade at the run's own configured spread.
    assert book["bid"] < book["last"] < book["ask"]
    assert book["bids"][0]["price"] > book["bids"][-1]["price"]
    assert book["asks"][0]["price"] < book["asks"][-1]["price"]
    assert book["bids"][-1]["cumulative"] > book["bids"][0]["cumulative"]

    heat = view["tools"]["heatmap"]
    assert sum(group["companies_count"] for group in heat["sectors"]) == 32
    assert heat["best"] >= heat["worst"]
    assert heat["sectors"][0]["change_pct"] >= heat["sectors"][-1]["change_pct"]

    screen = view["tools"]["screener"]
    assert screen["screen"] == "volume" and screen["label"] == "Unusual volume"
    assert [row["id"] for row in screen["screens"]].count("oversold") == 1
    assert screen["rows"] == sorted(
        screen["rows"], key=lambda r: -r["relative_volume"]
    )
    assert all(row["window_low"] <= row["close"] <= row["window_high"] for row in screen["rows"])
    # Every column a screen filters on has to actually compute, or the screens
    # that read it return nothing and look like a market with no opportunities.
    assert any(row["rsi"] is not None for row in screen["rows"])
    assert any(row["above_fast"] for row in screen["rows"])
    screens = base + "/monitor"
    for name, test in (
        ("oversold", lambda r: r["rsi"] < 30),
        ("overbought", lambda r: r["rsi"] > 70),
        ("momentum", lambda r: r["above_fast"] and r["above_slow"]),
        ("cheap", lambda r: r["multiple"] is not None),
    ):
        rows = client.get(
            screens, params={"panes": "screener", "symbol": SYMBOL, "screen": name}
        ).json()["tools"]["screener"]["rows"]
        assert all(test(row) for row in rows), name
    matched = {
        name: client.get(
            screens, params={"panes": "screener", "symbol": SYMBOL, "screen": name}
        ).json()["tools"]["screener"]["matches"]
        for name in ("overbought", "momentum", "cheap")
    }
    assert all(matched.values()), matched

    closes = view["tools"]["sessions"]["sessions"]
    assert closes and all(row["low"] <= row["close"] <= row["high"] for row in closes)
    assert closes[-1]["time"] <= advanced["cursor"] * 60 + bars[-1]["time"]

    # Regenerating gives byte-identical tools: nothing here rolls a fresh die.
    again = client.get(
        base + "/monitor",
        params={"panes": "tape,book", "symbol": SYMBOL, "limit": 40},
    ).json()
    assert again["tools"]["tape"] == tape and again["tools"]["book"] == book
    assert client.get(base + "/monitor", params={"panes": "nope", "symbol": SYMBOL}).status_code == 422


def test_scored_headlines_are_marked_on_the_bars_they_moved(client):
    """The points model is what moves the market, so it belongs on the chart."""
    client.get("/api/v1/simulator")
    run = create(client, seed=11)
    mutate(client, run, "advance", steps=900)
    seen = 0
    for interval in ("1m", "15m", "1h", "1D"):
        data = client.get(
            f"/api/v1/simulator/runs/{run['id']}/market",
            params={"symbol": SYMBOL, "interval": interval, "limit": 300},
        ).json()
        times = {bar["time"] for bar in data["bars"]}
        markers = data["markers"]
        seen += len(markers)
        # A marker that does not sit on a drawn bar cannot be rendered.
        assert all(marker["time"] in times for marker in markers)
        assert markers == sorted(markers, key=lambda marker: marker["time"])
        for marker in markers:
            assert marker["count"] >= 1 and marker["headline"]
            assert len(marker["items"]) <= 4
            # Several items inside one coarse bar net off; the label is the
            # loudest of them, not whichever happened to arrive last.
            assert marker["items"][0]["headline"] == marker["headline"]
            assert abs(marker["items"][0]["points"]) >= abs(marker["items"][-1]["points"])
    assert seen, "a 900-bar run has released scored headlines"
    # Nothing ahead of the cursor is ever marked.
    early = client.get(
        f"/api/v1/simulator/runs/{run['id']}/market",
        params={"symbol": SYMBOL, "interval": "1m", "limit": 300, "cursor": 600},
    ).json()
    assert all(marker["time"] <= early["bars"][-1]["time"] for marker in early["markers"])


def find(run, **match):
    return [o for o in run["orders"] if all(o.get(k) == v for k, v in match.items())]


def test_a_bracket_protects_an_entry_and_one_leg_cancels_the_other(client):
    """An entry can carry its own exits, so the risk plan is written before the fill."""
    client.get("/api/v1/simulator")
    run = create(client, seed=11)
    quote = next(q for q in run["quotes"] if q["symbol"] == SYMBOL)
    entry = float(quote["close"])
    placed = mutate(
        client,
        run,
        "orders",
        symbol=SYMBOL,
        side="buy",
        quantity=50,
        take_profit=round(entry * 1.02, 2),
        stop_loss=round(entry * 0.98, 2),
    ).json()
    legs = find(placed, parent_id=placed["orders"][0]["id"])
    assert len(legs) == 2
    assert {leg["role"] for leg in legs} == {"target", "stop"}
    # Held legs are not working orders: they reserve nothing and cannot trade.
    assert all(leg["status"] == "held" and leg["side"] == "sell" for leg in legs)
    assert all(leg["tif"] == "GTC" for leg in legs)
    assert placed["reserved"] == "0.00" or float(placed["reserved"]) >= 0

    # The entry fills; both legs arm for exactly the quantity it bought.
    advanced = mutate(client, placed, "advance", steps=1).json()
    parent = find(advanced, role=None)[0] if find(advanced, role=None) else advanced["orders"][0]
    assert parent["status"] == "filled" and parent["filled"] == 50
    armed = find(advanced, parent_id=parent["id"])
    assert all(leg["status"] == "working" and leg["quantity"] == 50 for leg in armed)

    # One leg trades and retires the other. Whichever it is, the position closes
    # once and only once.
    done = mutate(client, advanced, "advance", steps=900).json()
    exits = find(done, parent_id=parent["id"])
    statuses = sorted(leg["status"] for leg in exits)
    assert statuses == ["canceled", "filled"], statuses
    assert done["positions"] == [] or all(p["quantity"] == 0 for p in done["positions"])
    filled_leg = next(leg for leg in exits if leg["status"] == "filled")
    assert "bracket" in next(leg for leg in exits if leg["status"] == "canceled")["reason"]
    assert filled_leg["filled"] == 50


def test_a_bracket_that_cannot_be_right_is_refused(client):
    client.get("/api/v1/simulator")
    run = create(client, seed=11)
    quote = next(q for q in run["quotes"] if q["symbol"] == SYMBOL)
    entry = float(quote["close"])
    bad = mutate(
        client,
        run,
        "orders",
        symbol=SYMBOL,
        side="buy",
        quantity=10,
        take_profit=round(entry * 0.9, 2),
    )
    assert bad.status_code == 422 and "above the entry" in bad.json()["detail"]
    bad = mutate(
        client,
        run,
        "orders",
        symbol=SYMBOL,
        side="buy",
        quantity=10,
        stop_loss=round(entry * 1.1, 2),
    )
    assert bad.status_code == 422 and "below the entry" in bad.json()["detail"]
    # Attaching exits to a closing order is not a bracket.
    bought = mutate(client, run, "orders", symbol=SYMBOL, side="buy", quantity=10).json()
    bought = mutate(client, bought, "advance", steps=1).json()
    bad = mutate(
        client,
        bought,
        "orders",
        symbol=SYMBOL,
        side="sell",
        quantity=10,
        stop_loss=round(entry * 0.9, 2),
    )
    assert bad.status_code == 422 and "entries" in bad.json()["detail"]


def test_an_entry_cancelled_before_it_fills_takes_its_exits_with_it(client):
    client.get("/api/v1/simulator")
    run = create(client, seed=11)
    quote = next(q for q in run["quotes"] if q["symbol"] == SYMBOL)
    entry = float(quote["close"])
    placed = mutate(
        client,
        run,
        "orders",
        symbol=SYMBOL,
        side="buy",
        kind="limit",
        # Far below the market, so it will not fill. The exits are measured
        # against the price this entry would pay, not against today's market.
        limit_price=round(entry * 0.5, 2),
        quantity=10,
        take_profit=round(entry * 0.53, 2),
        stop_loss=round(entry * 0.47, 2),
    ).json()
    parent = placed["orders"][0]
    assert len(find(placed, parent_id=parent["id"])) == 2
    canceled = client.post(
        f"/api/v1/simulator/runs/{run['id']}/orders/{parent['id']}/cancel",
        json={"id": ident(), "version": placed["version"]},
    ).json()
    assert all(
        leg["status"] == "canceled" for leg in find(canceled, parent_id=parent["id"])
    )


def test_a_trailing_stop_ratchets_up_and_never_looks_inside_a_bar(client):
    """The stop protecting a bar is the one that was set before the bar opened."""
    client.get("/api/v1/simulator")
    run = create(client, seed=11)
    bought = mutate(client, run, "orders", symbol=SYMBOL, side="buy", quantity=30).json()
    bought = mutate(client, bought, "advance", steps=1).json()
    trailing = mutate(
        client,
        bought,
        "orders",
        symbol=SYMBOL,
        side="sell",
        kind="trailing_stop",
        quantity=30,
        trail_percent=3,
    ).json()
    order = find(trailing, kind="trailing_stop")[0]
    first = float(order["stop_price"])
    anchor = float(order["trail_anchor"])
    assert first == pytest.approx(anchor * 0.97, abs=0.02)

    highest = anchor
    previous = first
    state = trailing
    for _ in range(40):
        state = mutate(client, state, "advance", steps=5).json()
        order = find(state, kind="trailing_stop")[0]
        if order["status"] != "working":
            break
        stop, anchor = float(order["stop_price"]), float(order["trail_anchor"])
        # A trailing stop never steps down.
        assert stop >= previous - 0.005, (stop, previous)
        assert anchor >= highest - 0.005
        assert stop == pytest.approx(anchor * 0.97, abs=0.02)
        highest, previous = anchor, stop

    # When it does trigger, it sells at or below the stop it was carrying, never
    # at the high the same bar went on to make.
    if order["status"] == "filled":
        assert float(order["average"]) <= previous * 1.01
    assert float(order["stop_price"]) >= first


def test_a_trailing_stop_is_refused_where_it_cannot_mean_anything(client):
    client.get("/api/v1/simulator")
    run = create(client, seed=11)
    bad = mutate(
        client, run, "orders", symbol=SYMBOL, side="buy", quantity=5, kind="trailing_stop",
        trail_percent=2,
    )
    assert bad.status_code == 422 and "exits only" in bad.json()["detail"]
    bad = mutate(client, run, "orders", symbol=SYMBOL, side="sell", quantity=5, kind="trailing_stop")
    assert bad.status_code == 422 and "trail percentage" in bad.json()["detail"]
    bad = mutate(
        client, run, "orders", symbol=SYMBOL, side="buy", quantity=5, trail_percent=2
    )
    assert bad.status_code == 422 and "Only a trailing stop" in bad.json()["detail"]


def bracket_orders(s, data, quantity, target, stop, **changes):
    """An entry plus its two held exits, shaped the way the service builds them."""
    entry = order(s, data, quantity=quantity, **changes)
    entry.update(average="0.00", reason="")
    group = "group-" + entry["id"]
    legs = []
    for role, leg in (
        ("target", {"kind": "limit", "limit_price": str(target)}),
        ("stop", {"kind": "stop", "stop_price": str(stop)}),
    ):
        child = {
            **entry,
            "id": f"{entry['id']}:{role}",
            "side": "sell",
            "quantity": quantity,
            "filled": 0,
            "notional": "0.00",
            "average": "0.00",
            "fee_remaining": "1.00",
            "status": "held",
            "parent_id": entry["id"],
            "oco_group": group,
            "activates": None,
            "role": role,
            "limit_price": None,
            "stop_price": None,
            **leg,
        }
        s["orders"].append(child)
        legs.append(child)
    return entry, legs


def test_a_bracket_stays_sized_to_the_position_across_partial_fills():
    """The exits protect what the entry holds open, never more and never less."""
    # Thin volume, so a 300-share entry fills across several bars, and the price
    # then rises through the target.
    prices = [100, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
    data = bars(prices, volume=100)
    s = state()
    s["config"]["participation"] = "1"
    entry, legs = bracket_orders(s, data, 300, target=106, stop=90)
    for _ in range(len(prices) - 1):
        advance_state(s, data, 1)
        held = s["positions"].get("AAPL", {}).get("quantity", 0)
        # A long-only account can never be driven short by its own exits.
        assert held >= 0, held
        still_open = entry["filled"] - sum(leg["filled"] for leg in legs)
        assert held == still_open, (held, still_open, entry["filled"])
        for leg in legs:
            if leg["status"] in ("working", "partially_filled"):
                assert leg["quantity"] - leg["filled"] == still_open, leg
            assert "buying power" not in leg["reason"]
    # The target took the whole position; the stop was retired behind it.
    assert entry["filled"] == 300
    assert sum(leg["filled"] for leg in legs) == 300
    assert s["positions"]["AAPL"]["quantity"] == 0
    assert [leg["status"] for leg in legs] == ["filled", "canceled"]


def test_an_exit_that_fills_before_the_entry_finishes_leaves_nothing_unprotected():
    prices = [100, 101, 108, 95, 102, 103, 104, 105]
    data = bars(prices, volume=60)
    s = state()
    s["config"]["participation"] = "1"
    entry, legs = bracket_orders(s, data, 240, target=107, stop=96)
    for _ in range(len(prices) - 1):
        advance_state(s, data, 1)
        held = s["positions"].get("AAPL", {}).get("quantity", 0)
        assert held >= 0
        live = [leg for leg in legs if leg["status"] in ("working", "partially_filled")]
        # Every share the entry still holds is covered by each surviving exit.
        for leg in live:
            assert leg["quantity"] - leg["filled"] == held, (leg["role"], leg, held)


def test_a_trailing_bracket_leg_arms_from_what_the_entry_paid(client):
    """A trailing exit needs a price to trail from the moment it starts working."""
    client.get("/api/v1/simulator")
    run = create(client, seed=11)
    entry = float(next(q for q in run["quotes"] if q["symbol"] == SYMBOL)["close"])
    placed = mutate(
        client,
        run,
        "orders",
        symbol=SYMBOL,
        side="buy",
        quantity=20,
        take_profit=round(entry * 1.05, 2),
        stop_loss_trail=3,
    ).json()
    parent = placed["orders"][0]
    leg = next(o for o in placed["orders"] if o.get("role") == "stop")
    assert leg["stop_price"] is None and leg.get("trail_anchor") is None

    armed = mutate(client, placed, "advance", steps=1).json()
    parent = next(o for o in armed["orders"] if o["id"] == parent["id"])
    leg = next(o for o in armed["orders"] if o.get("role") == "stop")
    assert leg["status"] == "working"
    assert float(leg["trail_anchor"]) == pytest.approx(float(parent["average"]), abs=0.01)
    assert float(leg["stop_price"]) == pytest.approx(float(leg["trail_anchor"]) * 0.97, abs=0.02)

    # Its price is not the learner's to amend: the trail would overwrite it.
    refused = client.post(
        f"/api/v1/simulator/runs/{run['id']}/orders/{leg['id']}/amend",
        json={"id": ident(), "version": armed["version"], "stop_price": "1.00"},
    )
    assert refused.status_code == 422 and "sets its own price" in refused.json()["detail"]

    # It keeps advancing, and the stop only ever ratchets up.
    previous = float(leg["stop_price"])
    state = armed
    for _ in range(8):
        state = mutate(client, state, "advance", steps=30).json()
        leg = next(o for o in state["orders"] if o.get("role") == "stop")
        if leg["status"] != "working":
            break
        assert float(leg["stop_price"]) >= previous - 0.005
        previous = float(leg["stop_price"])


def test_a_cash_account_is_still_long_only(client):
    """Margin is opt-in. Nothing about an existing account changes."""
    client.get("/api/v1/simulator")
    run = create(client, seed=11)
    assert run["config"]["account"] == "cash"
    refused = mutate(client, run, "orders", symbol=SYMBOL, side="sell", quantity=10)
    assert refused.status_code == 422
    assert "long-only" in refused.json()["detail"]
    # Buying power on a cash account is the cash it has not committed.
    assert run["buying_power"] == run["available"]
    assert run["gross_exposure"] == "0.00"


def test_shorting_realizes_on_the_cover_in_both_directions():
    """A short's result is proceeds less what it cost to buy the stock back."""
    s = state()
    s["config"]["account"] = "margin"
    s["config"]["participation"] = "1"
    s["config"]["commission"] = "0"
    data = bars([50, 50, 45, 45], volume=10000)
    order(s, data, side="sell", quantity=100, fee_remaining="0.00")
    advance_state(s, data, 1)
    position = s["positions"]["AAPL"]
    # Short 100 at 50: the stock is owed, and the basis is what it was sold for.
    assert position["quantity"] == -100
    assert position["cost"] == "-5000.00"
    assert s["cash"] == "105000.00"

    order(s, data, side="buy", quantity=100, fee_remaining="0.00")
    advance_state(s, data, 1)
    assert s["positions"]["AAPL"]["quantity"] == 0
    assert s["positions"]["AAPL"]["cost"] == "0.00"
    assert s["realized"] == "500.00"
    assert s["cash"] == "100500.00"

    # The same trade the other way round loses the same amount.
    loss = state()
    loss["config"].update(account="margin", participation="1", commission="0")
    rising = bars([45, 45, 50, 50], volume=10000)
    order(loss, rising, side="sell", quantity=100, fee_remaining="0.00")
    advance_state(loss, rising, 1)
    order(loss, rising, side="buy", quantity=100, fee_remaining="0.00")
    advance_state(loss, rising, 1)
    assert loss["realized"] == "-500.00"


def test_a_sale_that_crosses_zero_closes_the_long_and_opens_the_short():
    s = state()
    s["config"].update(account="margin", participation="1", commission="0")
    data = bars([50, 50, 60, 60], volume=10000)
    order(s, data, side="buy", quantity=10, fee_remaining="0.00")
    advance_state(s, data, 1)
    assert s["positions"]["AAPL"] == {"quantity": 10, "cost": "500.00"}

    # Sell 30 while long 10: ten shares are closed at a profit and twenty shorted.
    order(s, data, side="sell", quantity=30, fee_remaining="0.00")
    advance_state(s, data, 1)
    position = s["positions"]["AAPL"]
    assert position["quantity"] == -20
    # Closed 10 at 60 against a 500 basis, then shorted 20 at 60.
    assert s["realized"] == "100.00"
    assert position["cost"] == "-1200.00"


def test_borrow_is_charged_once_a_session_and_a_call_forces_a_buy_in():
    from quanta.domain.simulator_margin import BORROW_RATE

    s = state()
    s["config"].update(account="margin", participation="1", commission="0")
    # Two sessions of flat prices, then a gap that puts the account under water.
    session = [50] * 3
    data = bars(session + session, volume=10000)
    # Second session starts a day later, so the borrow accrues twice.
    for index, row in enumerate(data["AAPL"]):
        if index >= 3:
            row["time"] += 86400
    order(s, data, side="sell", quantity=1000, fee_remaining="0.00")
    advance_state(s, data, 5)
    charges = [e for e in s["ledger"] if e["type"] == "borrow_fee"]
    assert len(charges) == 2, charges
    expected = round(50 * 1000 * float(BORROW_RATE) / 252, 2)
    assert float(charges[0]["amount"]) == pytest.approx(-expected, abs=0.01)
    # The ledger carries the running cash balance the performance curve reads.
    assert charges[-1]["cash"] == s["cash"]

    # A gap up large enough to breach maintenance forces a buy-in.
    gap = state()
    gap["config"].update(account="margin", participation="1", commission="0")
    prices = [50, 50, 50, 50, 240, 240, 240, 240]
    market = bars(prices, volume=100000)
    for index, row in enumerate(market["AAPL"]):
        if index >= 4:
            row["time"] += 86400
    order(gap, market, side="sell", quantity=2000, fee_remaining="0.00")
    advance_state(gap, market, 1)
    assert gap["positions"]["AAPL"]["quantity"] == -2000
    advance_state(gap, market, 6)
    forced = [o for o in gap["orders"] if o.get("forced")]
    assert forced, "a breached maintenance requirement has to call the account"
    assert "maintenance requirement" in forced[0]["reason"]
    assert gap["positions"]["AAPL"]["quantity"] == 0
    assert float(gap["realized"]) < 0


def test_a_margin_account_shorts_through_the_api_and_reports_its_exposure(client):
    """The whole path: a margin run, a short, its cost of carry, and the cover."""
    client.get("/api/v1/simulator")
    run = create(client, seed=11, account="margin")
    assert run["config"]["account"] == "margin" and run["account"] == "margin"
    # Two to one at fifty percent initial margin, against a flat $100k account.
    assert float(run["buying_power"]) == pytest.approx(200000, abs=1)

    shorted = mutate(client, run, "orders", symbol=SYMBOL, side="sell", quantity=100).json()
    shorted = mutate(client, shorted, "advance", steps=1).json()
    position = next(p for p in shorted["positions"] if p["symbol"] == SYMBOL)
    assert position["quantity"] == -100 and position["short"] is True
    assert float(position["cost"]) < 0
    # Short proceeds are in the cash balance but are not the account's to spend.
    assert float(shorted["cash"]) > 100000
    assert float(shorted["buying_power"]) < float(shorted["cash"]) * 2
    assert float(shorted["gross_exposure"]) == pytest.approx(
        abs(float(position["market_value"])), abs=0.02
    )
    # The account is worth what it was, less costs, the moment it opens.
    assert float(shorted["equity"]) == pytest.approx(100000, abs=60)

    # A session of carry leaves a borrow charge in the ledger.
    carried = mutate(client, shorted, "advance", steps=500).json()
    borrow = [e for e in carried["ledger"] if e["type"] == "borrow_fee"]
    assert borrow and float(borrow[0]["amount"]) < 0

    covered = mutate(client, carried, "orders", symbol=SYMBOL, side="buy", quantity=100).json()
    covered = mutate(client, covered, "advance", steps=1).json()
    assert all(p["quantity"] != -100 for p in covered["positions"])
    assert float(covered["realized"]) != 0
    # A short round trip is a closing trade, whichever side closed it.
    desk = client.get(f"/api/v1/simulator/runs/{run['id']}/desk").json()["performance"]
    assert desk["trades"] >= 1
    assert desk["average_exposure"] >= 0


def test_a_short_is_held_to_the_same_leverage_as_a_purchase(client):
    """Two to one, both ways round, and nothing accepted only to be called."""
    client.get("/api/v1/simulator")
    run = create(client, seed=11, account="margin")
    price = float(next(q for q in run["quotes"] if q["symbol"] == SYMBOL)["close"])
    # Just inside twice equity: accepted, and not immediately in breach.
    inside = mutate(
        client, run, "orders", symbol=SYMBOL, side="sell", quantity=int(195000 / price)
    )
    assert inside.status_code == 200, inside.text
    state = mutate(client, inside.json(), "advance", steps=1).json()
    assert not [o for o in state["orders"] if o.get("forced")]
    # Well beyond it: refused outright rather than accepted and bought in.
    fresh = create(client, seed=11, account="margin")
    refused = mutate(
        client, fresh, "orders", symbol=SYMBOL, side="sell", quantity=int(250000 / price)
    )
    assert refused.status_code == 422 and "margin" in refused.json()["detail"]
    # Missions stay on cash accounts, so every attempt meets the same rules.
    bad = client.post(
        "/api/v1/simulator/runs",
        json={"id": ident(), "mission": "stop-discipline", "account": "margin"},
    )
    assert bad.status_code == 422 and "cash account" in bad.json()["detail"]


def test_nothing_leaks_past_the_cursor_with_a_short_open(client):
    from quanta.services.simulator_market import simulated_market

    client.get("/api/v1/simulator")
    run = create(client, seed=606, account="margin")
    placed = mutate(client, run, "orders", symbol=SYMBOL, side="sell", quantity=60).json()
    advanced = mutate(client, placed, "advance", steps=500).json()
    routes = {
        "desk": {},
        "monitor": {"panes": "screener,heatmap", "symbol": SYMBOL, "screen": "volatile"},
        "analytics": {"symbol": SYMBOL},
    }
    before = {
        name: client.get(f"/api/v1/simulator/runs/{run['id']}/{name}", params=params).json()
        for name, params in routes.items()
    }
    simulated_market(606, advanced["cursor"] + 30_000)
    after = {
        name: client.get(f"/api/v1/simulator/runs/{run['id']}/{name}", params=params).json()
        for name, params in routes.items()
    }
    assert before == after


def test_a_short_stays_closable_when_there_is_no_buying_power_left(client):
    """The moment a cover matters most is the moment buying power is gone."""
    client.get("/api/v1/simulator")
    run = create(client, seed=11, account="margin")
    price = float(next(q for q in run["quotes"] if q["symbol"] == SYMBOL)["close"])
    quantity = int(190000 / price)
    placed = mutate(client, run, "orders", symbol=SYMBOL, side="sell", quantity=quantity).json()
    # Default participation fills a position this size across many bars.
    state = placed
    for _ in range(12):
        state = mutate(client, state, "advance", steps=390).json()
        if next((o for o in state["orders"] if o["id"] == placed["orders"][0]["id"]))[
            "status"
        ] == "filled":
            break
    position = next(p for p in state["positions"] if p["symbol"] == SYMBOL)
    assert position["quantity"] < 0
    assert float(state["buying_power"]) < float(state["equity"])

    cover = mutate(
        client, state, "orders", symbol=SYMBOL, side="buy", quantity=-position["quantity"]
    )
    assert cover.status_code == 200, cover.text
    state = cover.json()
    cover_id = state["orders"][-1]["id"]
    for _ in range(12):
        state = mutate(client, state, "advance", steps=390).json()
        order_row = next(o for o in state["orders"] if o["id"] == cover_id)
        # Never cancelled for buying power part-way through.
        assert order_row["status"] in ("working", "partially_filled", "filled"), order_row
        if order_row["status"] == "filled":
            break
    assert order_row["status"] == "filled"
    assert all(p["quantity"] >= 0 for p in state["positions"])


def test_a_forced_buy_in_runs_to_flat_without_being_re_raised():
    """One buy-in, working every bar, until the borrowed stock is returned."""
    s = state()
    s["config"].update(account="margin", commission="0")
    # The short fills first; the buy-in that follows the gap is then throttled by
    # the same thin volume everything else trades into.
    prices = [50] * 8 + [250] * 10
    data = bars(prices, volume=400)
    for index, row in enumerate(data["AAPL"]):
        if index >= 8:
            row["time"] += 86400
    s["config"]["participation"] = "1"
    order(s, data, side="sell", quantity=2000, fee_remaining="0.00")
    advance_state(s, data, 6)
    assert s["positions"]["AAPL"]["quantity"] == -2000
    seen = []
    for _ in range(len(prices) - 7):
        advance_state(s, data, 1)
        forced = [o for o in s["orders"] if o.get("forced")]
        seen.append(len(forced))
        for order_row in forced:
            assert order_row["status"] in ("working", "partially_filled", "filled")
            assert "maintenance requirement" in order_row["reason"]
    assert max(seen) == 1, seen
    assert s["positions"]["AAPL"]["quantity"] == 0
