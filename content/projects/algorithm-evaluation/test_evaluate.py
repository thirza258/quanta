import json
import tempfile
import unittest
from pathlib import Path

from evaluate import (
    block_interval,
    drawdowns,
    evaluate,
    load_equity,
    load_manifest,
    load_timings,
    main,
    write_reports,
)

ROOT = Path(__file__).resolve().parent


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.manifest = load_manifest(ROOT / "manifest.example.json")
        self.rows = load_equity(ROOT / "equity.example.csv")

    def test_independent_fixture_reconciles_returns_and_initial_drawdown(self):
        metrics = evaluate(self.rows, self.manifest)["metrics"]
        self.assertEqual(metrics["observations"], 12)
        self.assertAlmostEqual(metrics["total_return"], 0.10)
        self.assertAlmostEqual(metrics["benchmark_total_return"], 0.08)
        self.assertAlmostEqual(metrics["cumulative_return_difference"], 0.02)
        self.assertAlmostEqual(metrics["maximum_drawdown"], 1 - 9800 / 10500)
        self.assertAlmostEqual(metrics["annualized_geometric_return"], 0.10)
        self.assertEqual(
            drawdowns([100, 80, 90, 110]), [0, -0.19999999999999996, -0.09999999999999998, 0]
        )

    def test_constant_cash_does_not_fabricate_zero_risk_ratios(self):
        rows = [{**row, "equity": 100, "benchmark": 100} for row in self.rows]
        metrics = evaluate(rows, {**self.manifest, "annual_risk_free": 0})["metrics"]
        for name in ("sharpe", "sortino", "information_ratio"):
            self.assertIsNone(metrics[name])
        self.assertEqual(metrics["active_mean_block_interval"], [0, 0])

    def test_short_history_and_test_selection_are_disclosed(self):
        report = evaluate(self.rows[:4], {**self.manifest, "test_used_for_selection": True})
        self.assertIsNone(report["metrics"]["annualized_geometric_return"])
        self.assertIsNone(report["metrics"]["active_mean_block_interval"])
        self.assertTrue(any("cannot be presented as untouched" in w for w in report["warnings"]))

    def test_block_interval_is_reproducible_and_preserves_constant_series(self):
        values = [0.01, -0.02, 0.03, 0.01, -0.01, 0.02]
        self.assertEqual(block_interval(values), block_interval(values))
        self.assertEqual(block_interval([0.02] * 12), [0.02, 0.02])

    def test_bad_input_is_rejected_without_silent_sorting_or_repair(self):
        for body in (
            "date,equity,benchmark\n2024-01-01,100,100\n2024-01-01,101,102\n2024-02-01,102,103\n",
            "date,equity,benchmark\n2024-01-01,100,100\n2024-02-01,nan,102\n2024-03-01,102,103\n",
            "date,equity,benchmark\n2024-01-01,100,100\n2024-02-01,0,102\n2024-03-01,102,103\n",
            "date,equity,benchmark\n2024-01-01,100,100,extra\n2024-02-01,102,102\n2024-03-01,102,103\n",
            "date,equity,benchmark\n2024-01-01,1e-300,100\n2024-02-01,1e300,102\n2024-03-01,102,103\n",
        ):
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / "bad.csv"
                path.write_text(body)
                with self.assertRaises(ValueError):
                    evaluate(load_equity(path), self.manifest)

    def test_manifest_rejects_boolean_frequency_and_unclear_cost_basis(self):
        for change in (
            {"periods_per_year": True},
            {"equity_basis": "gross"},
            {"annual_risk_free": "nan"},
            {"test_used_for_selection": "false"},
        ):
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / "manifest.json"
                path.write_text(json.dumps({**self.manifest, **change}))
                with self.assertRaises(ValueError):
                    load_manifest(path)

    def test_paired_timings_reconcile(self):
        timings = load_timings(ROOT / "timings.example.csv")
        self.assertEqual(timings["repetitions"], 5)
        self.assertEqual(timings["median_serial_ms"], 30)
        self.assertEqual(timings["median_parallel_ms"], 10)
        self.assertEqual(timings["median_paired_speedup"], 3)

    def test_report_escapes_input_and_preserves_review_requirement(self):
        report = evaluate(self.rows, {**self.manifest, "strategy": "<script>alert(1)</script>"})
        report["sha256"] = {}
        with tempfile.TemporaryDirectory() as folder:
            write_reports(report, Path(folder), False)
            text = (Path(folder) / "report.html").read_text()
            self.assertNotIn("<script>", text)
            self.assertIn("&lt;script&gt;", text)
            self.assertIn("REVIEW REQUIRED", text)
            self.assertIn("CFA Institute", text)
            json.loads((Path(folder) / "metrics.json").read_text())

    def test_cli_produces_traceable_reports_without_chart_dependencies(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(
                main(
                    [
                        "--equity",
                        str(ROOT / "equity.example.csv"),
                        "--manifest",
                        str(ROOT / "manifest.example.json"),
                        "--out",
                        folder,
                        "--no-charts",
                    ]
                ),
                0,
            )
            report = json.loads((Path(folder) / "metrics.json").read_text())
            self.assertEqual(set(report["sha256"]), {"equity", "manifest", "evaluator"})
            self.assertTrue(all(len(digest) == 64 for digest in report["sha256"].values()))
            self.assertEqual(report["period"]["end"], "2025-01-01")


if __name__ == "__main__":
    unittest.main()
