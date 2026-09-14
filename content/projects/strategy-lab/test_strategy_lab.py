"""Independent arithmetic, causality and input-contract checks for the source archive."""

import copy
import tempfile
import unittest
from dataclasses import replace
from datetime import date, timedelta
from pathlib import Path

from strategy_lab import (
    Config,
    available_filing,
    backtest,
    fill_orders,
    load_inputs,
    rank_scores,
    run_research,
)


def panel(open_price, close_price, volume=1000):
    return {"AAA": {"open": open_price, "close": close_price, "volume": volume}}


def sessions(values):
    return [(date(2025, 1, 1) + timedelta(days=i), panel(o, c)) for i, (o, c) in enumerate(values)]


def filing(period="2024-12-31", available="2025-01-02", ncav=200):
    return {
        "symbol": "AAA",
        "period_end": date.fromisoformat(period),
        "available": date.fromisoformat(available),
        "ncav_per_share": ncav,
        "earnings_yield": 0.1,
        "roic": 0.2,
        "coverage": 3,
    }


class StrategyLabTests(unittest.TestCase):
    def test_independent_round_trip_cash_and_fees(self):
        config = Config(initial_cash=1000, cost_bps=100, participation=1)
        holdings = {"AAA": 0}
        cash, buys = fill_orders(
            1000,
            holdings,
            {"AAA": 2},
            panel(100, 105),
            panel(90, 95),
            config,
            date(2025, 1, 1),
            date(2025, 1, 2),
        )
        self.assertEqual(cash, 798)
        self.assertEqual(holdings, {"AAA": 2})
        cash, sells = fill_orders(
            cash,
            holdings,
            {"AAA": 0},
            panel(110, 109),
            panel(105, 105),
            config,
            date(2025, 1, 2),
            date(2025, 1, 3),
        )
        self.assertAlmostEqual(cash, 1015.8)
        self.assertAlmostEqual(buys[0]["fee"] + sells[0]["fee"], 4.2)
        self.assertEqual(holdings["AAA"], 0)

    def test_signal_uses_completed_close_and_never_fills_last_close(self):
        data = sessions([(100, 100), (110, 120), (130, 140)])
        result = backtest(
            data,
            [],
            "equal-weight",
            0,
            2,
            Config(initial_cash=1000, cost_bps=0, target_cap=0.2, participation=1),
        )
        self.assertEqual(result["trades"][0]["price"], 110)
        self.assertEqual(result["trades"][0]["filled"], 2)
        self.assertEqual(result["equity"][1]["equity"], 1020)
        self.assertTrue(all(t["signal_date"] < t["date"] for t in result["trades"]))
        self.assertEqual(max(t["date"] for t in result["signals"]), data[1][0].isoformat())

    def test_future_prices_and_revisions_cannot_change_past_events(self):
        data, filings = load_inputs("prices.csv", "fundamentals.csv")
        before = backtest(data, filings, "value-quality", 20, 60, Config())
        changed = copy.deepcopy(data)
        for _, bars in changed[50:]:
            for bar in bars.values():
                bar["open"] *= 2
                bar["close"] *= 3
        future = {**filings[0], "available": data[50][0], "ncav_per_share": 9999}
        after = backtest(changed, [*filings, future], "value-quality", 20, 60, Config())
        boundary = data[50][0].isoformat()
        for field in ("trades", "equity", "positions"):
            self.assertEqual(
                [r for r in before[field] if r["date"] < boundary],
                [r for r in after[field] if r["date"] < boundary],
            )

    def test_as_of_join_respects_release_revision_and_reporting_period(self):
        original = filing()
        amended = filing(available="2025-02-01", ncav=100)
        newer = filing(period="2025-01-31", available="2025-02-10", ncav=300)
        late_old = filing(available="2025-02-20", ncav=400)
        rows = [late_old, newer, original, amended]
        self.assertIsNone(available_filing(rows, "AAA", date(2025, 1, 2), 180))
        self.assertEqual(available_filing(rows, "AAA", date(2025, 1, 3), 180), original)
        self.assertEqual(available_filing(rows, "AAA", date(2025, 2, 2), 180), amended)
        self.assertEqual(available_filing(rows, "AAA", date(2025, 2, 21), 180), newer)
        self.assertIsNone(available_filing(rows, "AAA", date(2026, 2, 21), 180))

    def test_momentum_endpoints_skip_the_current_observation(self):
        data = sessions([(100, 100), (102, 102), (110, 110), (200, 200)])
        config = Config(lookback=2, skip=1)
        self.assertEqual(rank_scores(data, [], 2, "momentum", config), {})
        self.assertAlmostEqual(rank_scores(data, [], 3, "momentum", config)["AAA"], 0.1)
        changed = copy.deepcopy(data)
        changed[3][1]["AAA"]["close"] = 1
        self.assertEqual(
            rank_scores(data, [], 3, "momentum", config),
            rank_scores(changed, [], 3, "momentum", config),
        )

    def test_prior_volume_caps_and_cash_constraints_leave_no_negative_cash(self):
        holdings = {"AAA": 0}
        config = Config(cost_bps=100, participation=0.05)
        cash, orders = fill_orders(
            1000,
            holdings,
            {"AAA": 300},
            panel(100, 100, 1_000_000),
            panel(100, 100, 100),
            config,
            date(2025, 1, 1),
            date(2025, 1, 2),
        )
        self.assertEqual(orders[0]["filled"], 5)
        self.assertEqual(orders[0]["unfilled"], 295)
        self.assertEqual(cash, 495)
        cash, orders = fill_orders(
            100,
            {"AAA": 0},
            {"AAA": 3},
            panel(100, 100),
            panel(100, 100),
            config,
            date(2025, 1, 1),
            date(2025, 1, 2),
        )
        self.assertEqual(cash, 100)
        self.assertEqual(orders[0]["status"], "unfilled")

    def test_sells_fund_buys_and_target_ties_are_deterministic(self):
        holdings = {"AAA": 0, "BBB": 2}
        bars = {
            "AAA": {"open": 10, "close": 10, "volume": 1000},
            "BBB": {"open": 10, "close": 10, "volume": 1000},
        }
        cash, orders = fill_orders(
            0,
            holdings,
            {"AAA": 2, "BBB": 0},
            bars,
            bars,
            Config(cost_bps=0, participation=1),
            date(2025, 1, 1),
            date(2025, 1, 2),
        )
        self.assertEqual([r["symbol"] for r in orders], ["BBB", "AAA"])
        self.assertEqual(holdings, {"AAA": 2, "BBB": 0})
        self.assertEqual(cash, 0)
        data = [(date(2025, 1, 3), bars)]
        rows = [filing(), {**filing(), "symbol": "BBB"}]
        self.assertEqual(
            rank_scores(data, rows, 0, "value-quality", Config()), {"AAA": 1.0, "BBB": 1.0}
        )

    def test_every_position_row_reconciles_and_flat_market_only_loses_costs(self):
        result = backtest(
            sessions([(100, 100)] * 6),
            [],
            "equal-weight",
            0,
            5,
            Config(cost_bps=100, target_cap=0.4, participation=1),
        )
        for row in result["positions"]:
            value = sum(v for k, v in row.items() if k.startswith("value_"))
            self.assertAlmostEqual(row["equity"], row["cash"] + value)
            self.assertGreaterEqual(row["cash"], 0)
        self.assertAlmostEqual(result["equity"][-1]["equity"], 10000 - result["metrics"]["fees"])
        self.assertEqual(result["metrics"]["benchmark_return"], 0)

    def test_selection_does_not_consume_future_test_prices(self):
        data, filings = load_inputs("prices.csv", "fundamentals.csv")
        validation, selected = run_research(data, filings, 30, 60, Config())
        changed = copy.deepcopy(data)
        for _, bars in changed[60:]:
            bars["CEDAR"]["open"] *= 2
            bars["CEDAR"]["close"] *= 2
        later_validation, later = run_research(changed, filings, 30, 60, Config())
        self.assertEqual(validation, later_validation)
        self.assertEqual(selected["strategy"], later["strategy"])
        self.assertEqual(selected["equity"][0]["equity"], 10000)
        self.assertEqual(selected["equity"][0]["date"], data[59][0].isoformat())

    def test_loader_rejects_nonfinite_duplicate_unsorted_and_incomplete_prices(self):
        original = Path("prices.csv").read_text()
        lines = original.splitlines()
        bad_number = lines[1].split(",")
        bad_number[2] = "nan"
        samples = [
            "\n".join([lines[0], ",".join(bad_number), *lines[2:]]),
            "\n".join([lines[0], lines[1], *lines[1:]]),
            "\n".join([lines[0], lines[2], lines[1], *lines[3:]]),
            "\n".join([lines[0], *lines[2:]]),
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "prices.csv"
            for sample in samples:
                with self.subTest(sample=sample[:100]):
                    path.write_text(sample + "\n")
                    with self.assertRaises(ValueError):
                        load_inputs(path, "fundamentals.csv")

    def test_config_bounds_and_sample_boundaries(self):
        for values in (
            {"cost_bps": -1},
            {"participation": 2},
            {"top_n": True},
            {"initial_cash": float("nan")},
            {"lookback": 0},
            {"target_cap": 1.1},
        ):
            with self.subTest(values=values), self.assertRaises(ValueError):
                replace(Config(), **values).validate()
        data = sessions([(100, 100)] * 9)
        with self.assertRaises(ValueError):
            run_research(data, [], 3, 5, Config())


if __name__ == "__main__":
    unittest.main()
