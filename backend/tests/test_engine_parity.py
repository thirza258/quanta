"""The C++ simulator engine against the Python implementations it replaced.

Runs already stored in the database hold cursors, orders and fills against bars
the numpy generator produced and account states the Decimal engine wrote. The
engine is only a replacement if it reproduces both exactly, so these tests run
the same inputs through `reference/` (the original code, kept verbatim) and
through quanta.engine, and compare every cent, every string and the order of
every key. They also hold the engine to its own contract: identical results
for any worker count, and refusals rather than wrapped numbers on bad input.
"""

import copy
import json
import random
import uuid
from datetime import datetime
from decimal import ROUND_CEILING, ROUND_DOWN, ROUND_HALF_UP, Decimal, InvalidOperation
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import numpy as np
import pytest
from quanta import engine
from quanta.domain import simulator
from quanta.domain.errors import DomainError
from quanta.services import simulator_desk as desk
from quanta.services import simulator_market as market
from quanta.services import simulator_news as news
from quanta.services.simulator_universe import COMPANIES, LEGACY_SYMBOLS
from reference import desk as reference_desk
from reference import engine as reference
from reference import market as reference_market

EASTERN = ZoneInfo("America/New_York")
BRACKET = uuid.UUID("5d2f7f1c-7a5e-4a0d-8b39-2b3c8b4f9a11")


# ---------------------------------------------------------------------------
# Random streams and rounding


@pytest.mark.parametrize(
    "entropy", [[47, 0, 0x9E3779B9], [1000000, 21, 0x9E3779B9], [5, 2**40, 7], [0, 0]]
)
def test_the_normal_stream_is_numpys_draw_for_draw(entropy):
    words = np.array(entropy, dtype=np.uint64)
    drawn = np.empty(200_000)
    engine.check(
        engine.library().qs_standard_normals(
            engine.address(words), len(entropy), len(drawn), engine.address(drawn)
        )
    )
    assert np.array_equal(drawn, np.random.default_rng(entropy).standard_normal(len(drawn)))


@pytest.mark.parametrize("seed", [0, 47, 100003, 2**33 + 7])
def test_the_legacy_stream_is_cpythons_random(seed):
    count = 5000
    uniforms, gauss = np.empty(count), np.empty(count)
    integers = np.empty(count, dtype=np.int64)
    engine.check(
        engine.library().qs_python_random(
            seed, count, engine.address(uniforms), engine.address(gauss), engine.address(integers)
        )
    )
    stream = random.Random(seed)
    for i in range(count):
        assert uniforms[i] == stream.random()
        assert gauss[i] == stream.gauss(0.0, 1.0)
        assert integers[i] == stream.randint(2000, 30000)


def test_hundredths_round_like_python_round():
    import ctypes

    values = list(np.random.default_rng(3).uniform(0.001, 900, 50_000))
    values += [0.125, 0.375, 1.005, 2.675, 0.005, 1.115, 224.0, 123456.785]
    out = ctypes.c_int64()
    for value in values:
        engine.check(engine.library().qs_round_hundredths(float(value), ctypes.byref(out)))
        assert out.value / 100 == round(float(value), 2), value


# ---------------------------------------------------------------------------
# Decimal arithmetic

CENT = Decimal("0.01")


def _decimal_reference(op, a, b):
    x = Decimal(a)
    try:
        result = {
            "add": lambda: x + Decimal(b),
            "sub": lambda: x - Decimal(b),
            "mul": lambda: x * Decimal(b),
            "div": lambda: x / Decimal(b),
            "cmp": lambda: (x > Decimal(b)) - (x < Decimal(b)),
            "neg": lambda: -x,
            "abs": lambda: abs(x),
            "half_up": lambda: x.quantize(CENT, rounding=ROUND_HALF_UP),
            "ceiling": lambda: x.quantize(CENT, rounding=ROUND_CEILING),
            "down": lambda: x.quantize(CENT, rounding=ROUND_DOWN),
            "integral": lambda: x.to_integral_value(rounding=ROUND_DOWN),
        }[op]()
    except InvalidOperation, ZeroDivisionError, ArithmeticError:
        return "ERR"
    return str(result)


def _decimal_engine(op, a, b):
    import ctypes

    out = ctypes.create_string_buffer(512)
    code = engine.library().qs_decimal(
        op.encode(), a.encode(), b.encode() if b is not None else None, out, len(out)
    )
    return "ERR" if code else out.value.decode()


def _decimal_operand(rng):
    sign = "-" if rng.random() < 0.3 else ""
    kind = rng.random()
    if kind < 0.3:
        return f"{sign}{rng.randint(0, 10 ** rng.randint(1, 12))}.{rng.randint(0, 99):02d}"
    if kind < 0.5:
        return f"{sign}{rng.randint(0, 3000)}"
    if kind < 0.65:
        places = rng.randint(1, 12)
        return f"{sign}{rng.randint(0, 100)}.{rng.randint(0, 10**places - 1):0{places}d}"
    if kind < 0.75:
        return rng.choice(
            ["0", "-0", "0.00", "-0.00", "0E-5", "1E+3", "1.000", "0.005", "-0.005", "2.675"]
        )
    if kind < 0.9:
        digits = "".join(str(rng.randint(0, 9)) for _ in range(rng.randint(1, 38)))
        point = rng.randint(1, len(digits))
        return sign + digits[:point] + ("." + digits[point:] if point < len(digits) else "")
    return f"{sign}{rng.randint(1, 10 ** rng.randint(1, 20))}E{rng.randint(-40, 30):+d}"


def test_decimal_arithmetic_is_pythons_to_the_digit_and_the_sign_of_zero():
    """28 digits, the same rounding modes, the same exponents, the same -0.00."""
    rng = random.Random(7)
    binary = ["add", "sub", "mul", "div", "cmp"]
    unary = ["neg", "abs", "half_up", "ceiling", "down", "integral"]
    for _ in range(40_000):
        a = _decimal_operand(rng)
        if rng.random() < 0.6:
            op, b = rng.choice(binary), _decimal_operand(rng)
        else:
            op, b = rng.choice(unary), None
        assert _decimal_engine(op, a, b) == _decimal_reference(op, a, b), (op, a, b)


# ---------------------------------------------------------------------------
# Generated market


def _block(seed, first, carry, books):
    room = news.schedule(seed, first, market.BLOCK_SESSIONS, market.SESSION_BARS, books)
    return room


@pytest.mark.parametrize("seed", [47, 11, 0, 1000000, 31337])
def test_generated_blocks_are_the_numpy_generators_to_the_cent(seed):
    carry = {company.symbol: float(company.price) for company in COMPANIES}
    books = None
    for block in range(2):
        first = block * market.BLOCK_SESSIONS
        room = news.schedule(seed, first, market.BLOCK_SESSIONS, market.SESSION_BARS, books)
        books = room.books
        expected, expected_carry = reference_market._paths(
            seed, reference_market.shock_room(room.shocks), first, carry
        )
        actual, actual_carry = market._paths(seed, room, first, carry)
        for symbol, series in expected.items():
            assert np.array_equal(actual[symbol].cents, series.cents), (seed, block, symbol)
            assert np.array_equal(actual[symbol].volume, series.volume), (seed, block, symbol)
            assert np.array_equal(actual[symbol].time, series.time)
        assert actual_carry == expected_carry
        carry = expected_carry


def test_the_session_clock_matches_zoneinfo_for_a_century():
    for first in (0, 21, 57, 1000, 2700, 10_000, 26_000):
        assert np.array_equal(
            market.session_times(first, 21), reference_market.session_times(first, 21)
        ), first
    for session in (0, 4, 5, 46, 47, 216, 217, 5000):
        assert market.session_open(session) == reference_market.session_open(session)


@pytest.mark.parametrize("seed", [42, 47, 0, 1000000])
def test_runs_from_before_the_universe_get_the_original_six_paths(seed):
    expected = reference_market.legacy_synthetic(seed)
    actual = market.legacy_synthetic(seed)
    assert list(actual) == list(LEGACY_SYMBOLS)
    for symbol in LEGACY_SYMBOLS:
        assert actual[symbol] == expected[symbol], symbol


def test_bucketed_bars_match_the_python_bucketing():
    series = market.simulated_market(47, 0)["NVRA"]
    oracle = reference_market.BarSeries(series.time, series.cents, series.volume, series.session)
    rng = random.Random(5)
    for _ in range(60):
        start = rng.randint(0, 6000)
        stop = start + rng.randint(0, 6000)
        per_bucket = rng.choice([5, 15, 60, 390])
        assert series.aggregate(start, stop, per_bucket) == oracle.aggregate(
            start, stop, per_bucket
        )
    legacy = market.legacy_synthetic(42)
    sizes = {"5m": 5, "15m": 15, "1h": 60, "1D": 390}
    for _ in range(40):
        start = rng.randint(0, 5000)
        stop = min(6000, start + rng.randint(1, 3000))
        interval = rng.choice(list(sizes))
        assert market.legacy_buckets(legacy, "MSFT", start, stop, sizes[interval]) == (
            reference_desk.grouped(legacy["MSFT"][start:stop], interval)
        )


def test_block_generation_is_identical_for_any_worker_count(monkeypatch):
    room = news.schedule(2024, 0, market.BLOCK_SESSIONS, market.SESSION_BARS, None)
    carry = {company.symbol: float(company.price) for company in COMPANIES}
    results = []
    for workers in ("1", "2", "3", "8", "32"):
        monkeypatch.setenv("QUANTA_SIM_THREADS", workers)
        block, closing = market._paths(2024, room, 0, carry)
        results.append(([block[c.symbol].cents for c in COMPANIES], closing))
    for cents, closing in results[1:]:
        assert closing == results[0][1]
        assert all(np.array_equal(a, b) for a, b in zip(cents, results[0][0], strict=True))


# ---------------------------------------------------------------------------
# Indicators and the mark-to-market


def _walk(seed, count):
    rng = np.random.default_rng(seed)
    prices = np.round(100 * np.exp(np.cumsum(rng.normal(0, 0.01, count))), 2)
    prices[count // 3 : count // 3 + 40] = prices[count // 3]  # a flat stretch: zero changes
    return prices.tolist()


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_indicator_series_match_the_python_loops(seed):
    closes = _walk(seed, 3000)
    for period in (2, 9, 14, 20, 200):
        assert desk.sma_series(closes, period) == reference_desk.sma_series(closes, period)
        assert desk.ema_series(closes, period) == reference_desk.ema_series(closes, period)
        assert desk.rsi_series(closes, period) == reference_desk.rsi_series(closes, period)
    for fast, slow, signal in ((12, 26, 9), (5, 35, 5), (2, 3, 2)):
        assert desk.macd_series(closes, fast, slow, signal) == reference_desk.macd_series(
            closes, fast, slow, signal
        )
    short = closes[:10]
    assert desk.macd_series(short) == reference_desk.macd_series(short)
    assert desk.rsi_series(short, 14) == reference_desk.rsi_series(short, 14)


# ---------------------------------------------------------------------------
# Execution engine


class Ids:
    """uuid4 for fills, deterministic so two engines mint the same identifiers."""

    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return uuid.UUID(int=self.count)


def _day(data, symbol, cursor):
    stamp = data[symbol][cursor + 1]["time"]
    return datetime.fromtimestamp(stamp, EASTERN).date().isoformat()


def _place(module, state, data, payload):
    """order_create's operation, against one engine; all or nothing."""
    trial = copy.deepcopy(state)
    try:
        bar = module.bar_at(data, payload.symbol, trial["cursor"])
        order = {
            "id": payload.id,
            "symbol": payload.symbol,
            "side": payload.side,
            "kind": payload.kind,
            "quantity": payload.quantity,
            "limit_price": str(payload.limit_price) if payload.limit_price is not None else None,
            "stop_price": str(payload.stop_price) if payload.stop_price is not None else None,
            "trail_percent": str(payload.trail_percent)
            if payload.trail_percent is not None
            else None,
            "tif": payload.tif,
            "note": payload.note,
            "lesson": "",
            "filled": 0,
            "status": "working",
            "average": "0.00",
            "notional": "0.00",
            "fee_remaining": module.money(trial["config"]["commission"]),
            "triggered": False,
            "time": bar["time"],
            "day": _day(data, payload.symbol, trial["cursor"]),
            "reason": "Accepted. Waiting for the next eligible bar.",
        }
        module.validate_order(trial, data, order)
        bracket = payload.take_profit or payload.stop_loss or payload.stop_loss_trail
        if bracket:
            module.validate_bracket(payload, module.dec(bar["close"]))
        if order["kind"] == "trailing_stop":
            if module is simulator:
                order["trail_anchor"], order["stop_price"] = simulator.trailing_start(
                    bar["close"], payload.trail_percent
                )
            else:
                order["trail_anchor"] = reference.money(bar["close"])
                order["stop_price"] = reference.money(
                    reference.dec(bar["close"]) * (1 - reference.dec(payload.trail_percent) / 100)
                )
        trial["orders"].append(order)
        if bracket:
            group = str(uuid.uuid5(BRACKET, order["id"]))
            legs = []
            if payload.take_profit:
                legs.append(
                    {"role": "target", "kind": "limit", "limit_price": str(payload.take_profit)}
                )
            if payload.stop_loss or payload.stop_loss_trail:
                legs.append(
                    {
                        "role": "stop",
                        "kind": "trailing_stop" if payload.stop_loss_trail else "stop",
                        "stop_price": str(payload.stop_loss) if payload.stop_loss else None,
                        "trail_percent": str(payload.stop_loss_trail)
                        if payload.stop_loss_trail
                        else None,
                    }
                )
            for leg in legs:
                trial["orders"].append(
                    {
                        **order,
                        "id": str(uuid.uuid5(BRACKET, f"{order['id']}:{leg['role']}")),
                        "side": "sell",
                        "limit_price": None,
                        "stop_price": None,
                        "trail_percent": None,
                        "tif": "GTC",
                        "status": "held",
                        "parent_id": order["id"],
                        "oco_group": group,
                        "activates": None,
                        "note": order["note"],
                        "reason": "Held: waiting for the entry it protects to fill.",
                        **leg,
                    }
                )
    except DomainError as refusal:
        return ("refused", str(refusal))
    state.clear()
    state.update(trial)
    return ("accepted", order["reserve_price"])


def _amend(module, state, data, order_id, limit_price, stop_price):
    trial = copy.deepcopy(state)
    order = next(o for o in trial["orders"] if o["id"] == order_id)
    for key, value in (("limit_price", limit_price), ("stop_price", stop_price)):
        if value is not None:
            order[key] = str(value)
    try:
        module.validate_order(trial, data, order, order_id)
    except DomainError as refusal:
        return ("refused", str(refusal))
    order["reason"] = "Amendment confirmed. Waiting for the next eligible bar."
    state.clear()
    state.update(trial)
    return ("accepted", order["reserve_price"])


def _cancel(module, state, order_id):
    order = next(o for o in state["orders"] if o["id"] == order_id)
    if order["status"] in ("held", "working", "partially_filled"):
        order.update(status="canceled", reason="Unfilled remainder canceled by learner.")
    module.retire_orphans(state)


def _price(rng, close, spread):
    return Decimal(str(round(close * (1 + rng.uniform(-spread, spread)), rng.choice([0, 1, 2]))))


def _size(rng, state, symbol, side, close):
    """Mostly ordinary sizes, sometimes all-in, so a gap can outrun the reservation."""
    if rng.random() < 0.15:
        if side == "buy":
            free = Decimal(state["cash"]) - reference.reservations(state)[0]
            return max(1, int(free / Decimal(str(close))) - rng.randint(0, 2))
        held = state["positions"].get(symbol, {}).get("quantity", 0)
        return max(1, held + rng.choice([0, 0, 5]))
    return rng.choice([1, 3, 10, 25, 60, 150, 400, 2500, 90000])


def _payload(rng, data, state, symbols):
    symbol = rng.choice(symbols)
    close = data[symbol][state["cursor"]]["close"]
    side = "buy" if rng.random() < 0.62 else "sell"
    kind = rng.choices(
        ["market", "limit", "stop", "stop_limit", "trailing_stop"], weights=[4, 4, 2, 1, 1]
    )[0]
    payload = SimpleNamespace(
        id=str(uuid.UUID(int=rng.getrandbits(128))),
        symbol=symbol,
        side=side,
        kind=kind,
        quantity=_size(rng, state, symbol, side, close),
        limit_price=None,
        stop_price=None,
        trail_percent=None,
        take_profit=None,
        stop_loss=None,
        stop_loss_trail=None,
        tif=rng.choice(["GTC", "GTC", "DAY"]),
        note=rng.choice(["", "thesis", "Bergström's call — earnings"]),
    )
    if kind in ("limit", "stop_limit"):
        payload.limit_price = _price(rng, close, 0.03)
    if kind in ("stop", "stop_limit"):
        payload.stop_price = _price(rng, close, 0.03)
    if kind == "trailing_stop":
        payload.trail_percent = Decimal(rng.choice(["0.5", "2", "3.25", "10"]))
    if rng.random() < 0.08:
        # Deliberately malformed: a price the order type does not take.
        payload.stop_price = _price(rng, close, 0.02)
    if side == "buy" and rng.random() < 0.3:
        payload.take_profit = _price(rng, close * 1.04, 0.03)
        if rng.random() < 0.5:
            payload.stop_loss = _price(rng, close * 0.96, 0.03)
        else:
            payload.stop_loss_trail = Decimal(rng.choice(["1", "2.5", "5"]))
    return payload


def _same(theirs, ours, data):
    assert json.dumps(ours) == json.dumps(theirs)
    cash, shares = reference.reservations(theirs)
    engine_cash, engine_shares = simulator.reservations(ours)
    assert str(engine_cash) == str(cash) and engine_shares == shares
    assert simulator.account(ours, data) == reference.account(theirs, data)


def _scenario(seed, data, config, cursor, symbols, operations, monkeypatch):
    rng = random.Random(seed)
    monkeypatch.setattr(reference, "uuid4", Ids())
    monkeypatch.setattr(simulator, "uuid4", Ids())
    base = {
        "config": config,
        "cursor": cursor,
        "cash": "100000.00",
        "realized": "0.00",
        "positions": {},
        "orders": [],
        "fills": [],
        "ledger": [
            {
                "id": "opening",
                "type": "opening_balance",
                "description": "Virtual opening balance",
                "amount": "100000.00",
                "cash": "100000.00",
                "time": None,
            }
        ],
    }
    theirs, ours = copy.deepcopy(base), copy.deepcopy(base)
    last = len(next(iter(data.values()))) - 1
    outcomes = {"accepted": 0, "refused": 0, "stops": 0}
    for _ in range(operations):
        if theirs["cursor"] >= last - 1:
            break
        action = rng.choices(["order", "advance", "cancel", "amend"], weights=[5, 4, 1, 1])[0]
        live = [
            o for o in theirs["orders"] if o["status"] in ("held", "working", "partially_filled")
        ]
        if action == "order":
            payload = _payload(rng, data, theirs, symbols)
            expected = _place(reference, theirs, data, payload)
            assert _place(simulator, ours, data, payload) == expected
            outcomes[expected[0]] += 1
        elif action == "advance":
            steps = rng.choice([1, 1, 2, 3, 7, 30, 90])
            watch = set(
                rng.sample(
                    ["fill", "bracket", "margin_call", "earnings", "news"], rng.randint(0, 3)
                )
            )
            scheduled = {}
            if rng.random() < 0.3:
                for k in range(rng.randint(1, 3)):
                    scheduled[theirs["cursor"] + rng.randint(1, steps)] = (
                        f"Scheduled item {k}: Bergström"
                    )
            expected = reference.advance_state(theirs, data, steps, scheduled, watch)
            assert simulator.advance_state(ours, data, steps, scheduled, watch) == expected
            outcomes["stops"] += expected is not None
        elif action == "cancel" and live:
            target = rng.choice(live)["id"]
            _cancel(reference, theirs, target)
            _cancel(simulator, ours, target)
        elif action == "amend":
            working = [
                o
                for o in theirs["orders"]
                if o["status"] in ("working", "partially_filled") and o["kind"] != "trailing_stop"
            ]
            if working:
                order = rng.choice(working)
                close = data[order["symbol"]][theirs["cursor"]]["close"]
                limit = (
                    _price(rng, close, 0.05) if order["kind"] in ("limit", "stop_limit") else None
                )
                stop = _price(rng, close, 0.05) if order["kind"] in ("stop", "stop_limit") else None
                expected = _amend(reference, theirs, data, order["id"], limit, stop)
                assert _amend(simulator, ours, data, order["id"], limit, stop) == expected
        _same(theirs, ours, data)
    return theirs, ours, outcomes


def _config(rng, account):
    return {
        "mode": "synthetic",
        "commission": rng.choice(["1", "0", "2.50", "1.00"]),
        "slippage_bps": rng.choice(["2", "0", "3.75", "1.123456789"]),
        "spread_bps": rng.choice(["2", "0", "5", "2.5"]),
        "participation": rng.choice(["0.01", "1", "0.3333333", "0.05"]),
        "account": account,
    }


@pytest.mark.parametrize("seed", range(6))
@pytest.mark.parametrize("account", ["cash", "margin"])
def test_generated_markets_trade_identically_through_both_engines(seed, account, monkeypatch):
    data = market.simulated_market(47, 6000)
    config = _config(random.Random(seed), account)
    symbols = ["NVRA", "CLDS", "VLOC", "ZEPH"]
    theirs, ours, outcomes = _scenario(
        seed, data, config, 499 + seed * 211, symbols, 70, monkeypatch
    )
    assert outcomes["accepted"] and outcomes["refused"]
    # The desk marks the account on every bar from the same fills.
    start = 499
    times, _, equity, gross, level, *_ = desk.marked(ours, data, start, ours["cursor"])
    expected = reference_desk.holdings(theirs, data, theirs["cursor"], start)
    assert np.array_equal(equity, expected[0])
    assert np.array_equal(gross, expected[1])
    assert np.array_equal(level, expected[2])


def _choppy(seed, symbols=("AAA", "BBB", "CCC"), bars=420, floats=False):
    """Small fixtures with day boundaries, gaps, flat stretches and jumps."""
    rng = random.Random(seed)
    data = {}
    for number, symbol in enumerate(symbols):
        price = 40.0 + 30 * number
        rows = []
        stamp = 1736173800
        for i in range(bars):
            if i and i % 30 == 0:
                stamp += 86400 - 29 * 60  # the next bar opens a new trading day
            else:
                stamp += 60 if i else 0
            move = rng.choice(
                [0.0, 0.0, rng.gauss(0, 0.01), rng.gauss(0, 0.06), rng.choice([0.4, -0.3])]
            )
            price = max(0.5, price * (1 + move))
            opening = price * (1 + rng.gauss(0, 0.004))
            high = max(opening, price) * (1 + abs(rng.gauss(0, 0.01)))
            low = min(opening, price) * (1 - abs(rng.gauss(0, 0.01)))
            if floats:
                values = [round(v, 6) for v in (opening, high, low, price)]
                volume = round(rng.uniform(50, 5000), 1)
            else:
                values = [round(v, 2) for v in (opening, high, low, price)]
                volume = rng.choice([rng.randint(0, 40), rng.randint(100, 20000)])
            rows.append(
                {
                    "time": stamp,
                    "open": values[0],
                    "high": values[1],
                    "low": values[2],
                    "close": values[3],
                    "volume": volume,
                }
            )
        data[symbol] = rows
    return data


@pytest.mark.parametrize("seed", range(8))
@pytest.mark.parametrize("account", ["cash", "margin"])
def test_gaps_sessions_and_margin_calls_resolve_identically(seed, account, monkeypatch):
    data = _choppy(seed, floats=seed % 2 == 1)
    config = _config(random.Random(100 + seed), account)
    _scenario(1000 + seed, data, config, 0, list(data), 90, monkeypatch)


def _bars(symbol, rows):
    return {
        symbol: [
            {"time": 1736173800 + i * 60, "open": o, "high": h, "low": low, "close": c, "volume": v}
            for i, (o, h, low, c, v) in enumerate(rows)
        ]
    }


def _order(**fields):
    order = {
        "id": str(uuid.uuid4()),
        "symbol": "AAA",
        "side": "buy",
        "kind": "market",
        "quantity": 1,
        "limit_price": None,
        "stop_price": None,
        "trail_percent": None,
        "tif": "GTC",
        "note": "",
        "lesson": "",
        "filled": 0,
        "status": "working",
        "average": "0.00",
        "notional": "0.00",
        "fee_remaining": "1.00",
        "reserve_price": "1.00",
        "triggered": False,
        "time": 1736173800,
        "day": "2025-01-06",
        "reason": "",
    }
    order.update(fields)
    return order


def _account(cash, account="cash", positions=None, orders=(), commission="1"):
    return {
        "config": {
            "commission": commission,
            "slippage_bps": "0",
            "spread_bps": "0",
            "participation": "1",
            "account": account,
        },
        "cursor": 0,
        "cash": cash,
        "realized": "0.00",
        "positions": positions or {},
        "orders": list(orders),
        "fills": [],
        "ledger": [],
    }


REJECTIONS = {
    # A buy validated at 98 that opens at 120 cannot buy a single share.
    "gap beyond cash": (
        _account("100.00", orders=[_order(reserve_price="98.00")]),
        _bars("AAA", [(98, 99, 97, 98, 1000), (120, 121, 119, 120, 1000)]),
    ),
    # A sale whose commission the proceeds and free cash cannot cover.
    "commission beyond proceeds": (
        _account(
            "1.00",
            positions={"AAA": {"quantity": 1, "cost": "0.60"}},
            orders=[
                _order(
                    side="buy",
                    kind="limit",
                    limit_price="0.10",
                    reserve_price="0.10",
                    fee_remaining="0.90",
                ),
                _order(side="sell", reserve_price="0.50"),
            ],
        ),
        _bars("AAA", [(0.5, 0.5, 0.5, 0.5, 1000), (0.5, 0.5, 0.5, 0.5, 1000)]),
    ),
    # A buy-in whose short was already covered on the same bar buys nothing
    # it cannot fund.
    "forced order with nothing to cover": (
        _account(
            "50.00",
            account="margin",
            positions={"AAA": {"quantity": -10, "cost": "-500.00"}},
            orders=[
                _order(quantity=10, reserve_price="60.00", fee_remaining="0.00"),
                _order(
                    quantity=10,
                    forced=True,
                    activates=1,
                    reserve_price="120.00",
                    fee_remaining="0.00",
                ),
            ],
        ),
        _bars("AAA", [(50, 50, 50, 50, 1000), (60, 60, 60, 60, 1000), (60, 60, 60, 60, 1000)]),
    ),
}


@pytest.mark.parametrize("name", list(REJECTIONS))
def test_rejected_executions_agree(name, monkeypatch):
    state, data = REJECTIONS[name]
    theirs, ours = copy.deepcopy(state), copy.deepcopy(state)
    monkeypatch.setattr(reference, "uuid4", Ids())
    monkeypatch.setattr(simulator, "uuid4", Ids())
    expected = reference.advance_state(theirs, data, 2)
    assert simulator.advance_state(ours, data, 2) == expected
    assert any(o["status"] == "rejected" for o in theirs["orders"]), theirs["orders"]
    _same(theirs, ours, data)


def test_cost_assumptions_stay_within_the_digits_the_engine_computes_exactly(client):
    """A run's rates feed exact decimal arithmetic, so their precision is bounded."""
    client.get("/api/v1/simulator")
    refused = client.post(
        "/api/v1/simulator/runs",
        json={"id": str(uuid.uuid4()), "participation": "0.0100000000000000000000000000000000000001"},
    )
    assert refused.status_code == 422
    accepted = client.post(
        "/api/v1/simulator/runs",
        json={
            "id": str(uuid.uuid4()),
            "slippage_bps": "1.123456789",
            "spread_bps": "2.5",
            "participation": "0.3333333",
        },
    )
    assert accepted.status_code == 200, accepted.text
    run = accepted.json()
    placed = client.post(
        f"/api/v1/simulator/runs/{run['id']}/orders",
        json={"id": str(uuid.uuid4()), "version": run["version"], "symbol": "NVRA", "side": "buy", "quantity": 5},
    )
    assert placed.status_code == 200, placed.text
    advanced = client.post(
        f"/api/v1/simulator/runs/{run['id']}/advance",
        json={"id": str(uuid.uuid4()), "version": placed.json()["version"], "steps": 3},
    )
    assert advanced.status_code == 200, advanced.text
    assert advanced.json()["fills"]
