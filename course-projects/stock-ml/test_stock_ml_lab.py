"""Run with python -m unittest -v in this extracted project directory."""

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
import stock_ml_lab as lab


class LifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = lab.synthetic_bars(days=160)
        cls.clean, cls.calendar, cls.audit = lab.clean_bars(cls.raw)
        cls.data = lab.build_dataset(cls.clean, cls.calendar)
        cls.fitted = lab.fit_models(cls.data)

    def test_cleaning_counts_and_conflicting_duplicates(self):
        self.assertEqual(self.audit["exact_duplicates_removed"], 1)
        self.assertEqual(self.audit["invalid_price_rows"], 1)
        self.assertEqual(self.audit["late_or_unknown_availability_rows"], 1)
        self.assertEqual(self.audit["volume_values_marked_missing"], 1)
        self.assertEqual(self.audit["clean_rows"], 478)
        conflict = self.raw.iloc[[0]].copy()
        conflict["close"] *= 2
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            lab.clean_bars(pd.concat([self.raw, conflict]))

    def test_missing_price_does_not_bridge_a_label_or_feature_window(self):
        bad_date = self.calendar[20]
        self.assertFalse(((self.data["symbol"] == "CEDA") & (self.data["date"] == bad_date)).any())
        prior = self.data[
            (self.data["symbol"] == "CEDA") & (self.data["date"] == self.calendar[19])
        ]
        self.assertTrue(prior.empty)  # Entry would require the excluded row's open.
        self.assertFalse(
            ((self.data["symbol"] == "CEDA") & self.data["date"].isin(self.calendar[20:26])).any()
        )

    def test_features_do_not_change_when_only_future_prices_change(self):
        cutoff = self.calendar[80]
        changed = self.clean.copy()
        changed.loc[changed["date"] > cutoff, ["open", "close"]] *= 3
        rebuilt = lab.build_dataset(changed, self.calendar, require_labels=False)
        original = lab.build_dataset(self.clean, self.calendar, require_labels=False)
        cols = ["date", "symbol"] + lab.FEATURES
        pd.testing.assert_frame_equal(
            original.loc[original["date"] <= cutoff, cols].reset_index(drop=True),
            rebuilt.loc[rebuilt["date"] <= cutoff, cols].reset_index(drop=True),
        )

    def test_label_matches_actual_next_two_opens(self):
        row = self.data.iloc[10]
        index = self.calendar.get_loc(row["date"])
        stock = self.clean[self.clean["symbol"] == row["symbol"]].set_index("date")
        expected = (
            stock.loc[self.calendar[index + 2], "open"]
            / stock.loc[self.calendar[index + 1], "open"]
            - 1
        )
        self.assertAlmostEqual(row["target"], expected)
        self.assertEqual(row["label_end"], self.calendar[index + 2])

    def test_date_partitions_and_label_endpoints_do_not_overlap(self):
        train, validation, test, development = lab.chronological_split(self.data)
        self.assertLess(train["label_end"].max(), validation["date"].min())
        self.assertLess(development["label_end"].max(), test["date"].min())
        self.assertFalse(set(train["date"]) & set(validation["date"]))
        self.assertFalse(set(validation["date"]) & set(test["date"]))

    def test_heldout_outcomes_do_not_change_selection_or_fitted_predictions(self):
        changed = self.data.copy()
        changed.loc[changed["date"] >= self.fitted["test"]["date"].min(), "target"] += 0.2
        refit = lab.fit_models(changed)
        self.assertEqual(refit["trials"], self.fitted["trials"])
        for name in ["regressor", "classifier"]:
            np.testing.assert_allclose(
                refit[name].predict(self.fitted["test"][lab.FEATURES]),
                self.fitted[name].predict(self.fitted["test"][lab.FEATURES]),
            )
        self.assertGreater(lab.evaluate(refit)[0]["mse"], lab.evaluate(self.fitted)[0]["mse"])

    def test_metrics_denominators_and_opportunity_accounting(self):
        metrics, predictions, daily = lab.evaluate(self.fitted)
        self.assertEqual(sum(metrics["confusion"].values()), len(predictions))
        self.assertEqual(sum(row["count"] for row in metrics["calibration_bins"]), len(predictions))
        for row in daily:
            self.assertAlmostEqual(row["net"], row["gross"] - row["cost"])
            self.assertLessEqual(row["invested_weight"], 1)
            self.assertAlmostEqual(row["cost"], 0.001 * row["invested_weight"])
        with self.assertRaises(ValueError):
            lab.evaluate(self.fitted, -1)

    def test_latest_rows_are_scoreable_without_labels(self):
        features = lab.build_dataset(self.clean, self.calendar, require_labels=False)
        self.assertEqual(features["date"].max(), self.calendar[-1])
        self.assertTrue(features.loc[features["date"] == self.calendar[-1], "target"].isna().all())
        values = self.fitted["regressor"].predict(features[lab.FEATURES])
        self.assertTrue(np.isfinite(values).all())

    def test_artifact_roundtrip_batch_parity_and_integrity_rejection(self):
        with tempfile.TemporaryDirectory() as directory:
            run_path, score_path = Path(directory) / "run", Path(directory) / "score"
            report = lab.run(run_path)
            lab.score(run_path, run_path / "raw.csv", score_path)
            historic = pd.read_csv(run_path / "predictions.csv")
            batch = pd.read_csv(score_path / "batch_predictions.csv")
            combined = historic.merge(batch, on=["date", "symbol"])
            self.assertEqual(len(combined), len(historic))
            np.testing.assert_allclose(combined["prediction"], combined["regressor"])
            np.testing.assert_allclose(combined["up_probability"], combined["classifier"])
            self.assertGreater(batch["date"].max(), historic["date"].max())
            self.assertEqual(
                json.loads((run_path / "report.json").read_text())["selected"], report["selected"]
            )
            with self.assertRaises(FileExistsError):
                lab.run(run_path)
            with (run_path / "regressor.joblib").open("ab") as artifact:
                artifact.write(b"changed")
            with self.assertRaisesRegex(ValueError, "manifest"):
                lab.score(run_path, run_path / "raw.csv", Path(directory) / "invalid")


if __name__ == "__main__":
    unittest.main()
