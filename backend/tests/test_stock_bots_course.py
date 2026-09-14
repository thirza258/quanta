"""Independent accounting and evaluation checks for the original offline course lab."""

import importlib.util
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Barrier

import pytest
from quanta.main import LESSONS
from quanta.runner import run

LAB_PATH = Path(__file__).resolve().parents[2] / "public/course-assets/stock-bots/paper_bot_lab.py"
spec = importlib.util.spec_from_file_location("paper_bot_lab", LAB_PATH)
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


@pytest.fixture
def bot(tmp_path):
    instance = lab.PaperBot(tmp_path / "test.sqlite")
    yield instance
    instance.close()


def buy(bot, id="buy", quantity=10, price=10000, **changes):
    args = dict(quote=price, event_time=0, now=0)
    args.update(changes)
    return bot.place(id, "buy", quantity, price, **args)


def test_default_replay_independently_reconciles_money_and_restart(tmp_path):
    result = lab.run_demo(tmp_path / "demo.sqlite")
    assert result["paper"] == {
        "cash_cents": 920939,
        "shares": 8,
        "equity_cents": 1002539,
        "pnl_cents": 2539,
        "fees_cents": 61,
        "fills": 3,
        "open_orders": 0,
        "halt_reason": "incident rehearsal",
    }
    assert result["halt_rejected_entry"] is True
    with pytest.raises(ValueError, match="unused database"):
        lab.run_demo(tmp_path / "demo.sqlite")


def test_cancel_releases_only_unfilled_reservation(tmp_path):
    bot = lab.PaperBot(tmp_path / "small.sqlite", initial_cash=100100)
    try:
        buy(bot)
        bot.market("one", 10000, 4, event_time=1000, now=1000)
        with pytest.raises(ValueError, match="cash"):
            buy(bot, "another", quantity=1, event_time=1000, now=1000)
        bot.cancel("buy")
        buy(bot, "replacement", quantity=6, event_time=1000, now=1000)
        assert bot.report()["cash_cents"] == 60080
        assert bot.report()["shares"] == 4
    finally:
        bot.close()


def test_identity_replays_and_conflicts_preserve_state(bot):
    buy(bot)
    buy(bot)
    bot.market("one", 10000, 4, event_time=1000, now=1000)
    before = bot.report()
    assert bot.market("one", 10000, 4, event_time=1000, now=1000) == 0
    assert bot.replay_fill("one/buy", "buy", 4, 10000) is False
    for action in (
        lambda: buy(bot, quantity=11),
        lambda: bot.market("one", 9900, 4, event_time=1000, now=1000),
        lambda: bot.replay_fill("one/buy", "buy", 5, 10000),
    ):
        with pytest.raises(ValueError, match="conflict"):
            action()
        assert bot.report() == before


def test_next_event_limit_and_shared_volume(bot):
    buy(bot, "first", quantity=2)
    buy(bot, "second", quantity=2)
    assert bot.market("same-time", 10000, 9, event_time=0, now=0) == 0
    assert bot.market("too-expensive", 10100, 9, event_time=1000, now=1000) == 0
    assert bot.market("eligible", 10000, 3, event_time=2000, now=2000) == 3
    assert bot.report()["shares"] == 3
    assert bot.report()["open_orders"] == 1
    assert bot.report()["fees_cents"] == 15
    with pytest.raises(ValueError, match="out-of-order"):
        bot.market("late", 10000, 3, event_time=1500, now=1500)


@pytest.mark.parametrize(
    "changes, message",
    [
        ({"now": 501}, "stale"),
        ({"now": -1}, "future"),
        ({"session_open": False}, "closed"),
        ({"quantity": 0}, "positive integer"),
        ({"quantity": True}, "positive integer"),
        ({"price": 0}, "positive integer"),
        ({"quantity": 101, "price": 1000}, "share cap"),
        ({"quantity": 60}, "notional cap"),
    ],
)
def test_invalid_new_orders_have_no_effect(bot, changes, message):
    before = bot.report()
    with pytest.raises(ValueError, match=message):
        buy(bot, **changes)
    assert bot.report() == before
    assert bot.db.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0


def test_halt_survives_reopen_and_allows_only_valid_reduction(tmp_path):
    path = tmp_path / "halt.sqlite"
    bot = lab.PaperBot(path)
    buy(bot, quantity=3)
    bot.market("one", 10000, 3, event_time=1000, now=1000)
    bot.halt("data incident")
    bot.close()
    bot = lab.PaperBot(path)
    try:
        with pytest.raises(ValueError, match="halted"):
            buy(bot, "blocked", quantity=1, event_time=1000, now=1000)
        with pytest.raises(ValueError, match="shares"):
            bot.place("oversell", "sell", 4, 10000, quote=10000, event_time=1000, now=1000)
        bot.place("reduce", "sell", 2, 10000, quote=10000, event_time=1000, now=1000)
        bot.market("two", 10000, 2, event_time=2000, now=2000)
        assert bot.report()["shares"] == 1
        assert bot.report()["halt_reason"] == "data incident"
        bot.resume("reconciled and reviewed")
        buy(bot, "resumed", quantity=1, event_time=2000, now=2000)
    finally:
        bot.close()


def test_failed_transaction_rolls_back_fill_event_and_account(bot, monkeypatch):
    buy(bot)
    before = bot.report()

    def fail():
        raise ValueError("injected failure after fill")

    with monkeypatch.context() as patch:
        patch.setattr(bot, "reconcile", fail)
        with pytest.raises(ValueError, match="injected"):
            bot.market("rollback", 10000, 4, event_time=1000, now=1000)
    assert bot.report() == before
    assert bot.db.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 0
    assert bot.market("rollback", 10000, 4, event_time=1000, now=1000) == 4


def test_two_writers_cannot_spend_the_same_cash(tmp_path):
    path = tmp_path / "writers.sqlite"
    initial = lab.PaperBot(path, initial_cash=100100)
    initial.close()
    barrier = Barrier(2)

    def submit(index):
        bot = lab.PaperBot(path)
        try:
            barrier.wait(timeout=5)
            try:
                buy(bot, str(index), quantity=6)
                return True
            except ValueError as error:
                assert "cash" in str(error)
                return False
        finally:
            bot.close()

    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(submit, [1, 2])) == [False, True]


def test_ridge_uses_training_only_means_and_matches_independent_values():
    result = lab.ridge_walkforward()
    first, second = result["folds"]
    assert [first["training_rows"], second["training_rows"]] == [4, 5]
    assert first["prediction"] == pytest.approx(25 / 6)
    assert second["prediction"] == pytest.approx(71 / 11)
    assert result["model_mse"] == pytest.approx(((5 / 6) ** 2 + (6 / 11) ** 2) / 2)
    assert result["baseline_mse"] == 30.5


@pytest.mark.parametrize(
    "change",
    [
        {"source_id": "invented"},
        {"issuer": "OTHER"},
        {"unit": "USD thousand"},
        {"value": float("nan")},
        {"value": True},
        {"value": 121},
        {"execute_order": "buy everything"},
        {"period": "2024"},
    ],
)
def test_invalid_ai_candidate_is_rejected(change):
    with pytest.raises(ValueError):
        lab.validate_fact({**lab.CANDIDATE, **change}, lab.EVIDENCE, 20)


def test_ai_availability_missing_fields_and_zero_denominator():
    assert lab.validate_fact(lab.CANDIDATE, lab.EVIDENCE, 20)["growth"] == pytest.approx(0.2)
    with pytest.raises(ValueError, match="unavailable"):
        lab.validate_fact(lab.CANDIDATE, lab.EVIDENCE, 10)
    incomplete = {key: value for key, value in lab.CANDIDATE.items() if key != "unit"}
    with pytest.raises(ValueError, match="missing"):
        lab.validate_fact(incomplete, lab.EVIDENCE, 20)
    evidence = {"HBR-2025-v1": {**lab.EVIDENCE["HBR-2025-v1"], "prior_revenue": 0}}
    with pytest.raises(ValueError, match="denominator"):
        lab.validate_fact(lab.CANDIDATE, evidence, 20)


@pytest.mark.parametrize(
    "lesson_id, expected",
    [
        ("5.1", "Distinct intents: 2"),
        ("5.2", "Residual buy shares: 30"),
        ("5.13", "Actual holding: 55"),
        ("5.29", "Project equity: 10025.39"),
        ("5.30", "Baseline MSE: 30.5"),
        ("5.32", "Dossier accepted: False"),
    ],
)
def test_course_worksheets_reconcile_with_project(lesson_id, expected):
    result = run(LESSONS[lesson_id]["code"], {"close": [100, 101, 99]})
    assert result["signals"] == [False, False, False]
    assert expected in result["stdout"]


@pytest.mark.parametrize("id, answer", [("5.1", 1), ("5.2", 2), ("5.3", 1), ("5.4", 0), ("5.5", 1)])
def test_legacy_bot_exercise_answer_keys_are_preserved(client, id, answer):
    result = client.post(f"/api/v1/exercises/{id}/submit", json={"answer": answer})
    assert result.status_code == 200
    assert result.json()["correct"] is True


def test_order_cannot_be_backdated_into_processed_market_state(bot):
    bot.market("observed", 10000, 10, event_time=1000, now=1000)
    before = bot.report()
    with pytest.raises(ValueError, match="predates"):
        buy(bot, "late-decision", event_time=500, now=500)
    assert bot.report() == before
