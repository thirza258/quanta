"""Original local stock-ML lifecycle lab. Synthetic data; no market API or order submission."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    log_loss,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ["momentum_5", "volatility_5", "log_volume"]
SEED = 42


def synthetic_bars(days=320, seed=SEED):
    """Known synthetic design, with bad/missing/duplicate rows to exercise data controls."""
    if days < 100:
        raise ValueError("At least 100 synthetic dates are required")
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2023-01-02", periods=days, tz="UTC")
    rows = []
    for j, symbol in enumerate(["CEDA", "CEDB", "CEDC"]):
        previous = 50.0 + 20 * j
        prior_return = 0.0
        for date in dates:
            opening = previous * np.exp(rng.normal(0, 0.003))
            daily = 0.15 * prior_return + rng.normal(0.0002, 0.012)
            close = opening * np.exp(daily)
            rows.append(
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "symbol": symbol,
                    "open": opening,
                    "close": close,
                    "volume": int(rng.integers(1000, 100000)),
                    "available_at": (date + pd.Timedelta(hours=21)).isoformat(),
                }
            )
            previous, prior_return = close, daily
    frame = pd.DataFrame(rows)
    frame.loc[20, "close"] = -1
    frame.loc[40, "volume"] = np.nan
    frame.loc[60, "available_at"] = "2099-01-01T00:00:00+00:00"
    return pd.concat([frame, frame.iloc[[10]]], ignore_index=True)


def clean_bars(raw):
    required = {"date", "symbol", "open", "close", "volume", "available_at"}
    if not required.issubset(raw.columns):
        raise ValueError(f"Missing required columns: {sorted(required - set(raw.columns))}")
    frame = raw[list(sorted(required))].copy()
    audit = {"raw_rows": len(frame)}
    frame["date"] = pd.to_datetime(frame["date"], utc=True, errors="coerce")
    frame["available_at"] = pd.to_datetime(frame["available_at"], utc=True, errors="coerce")
    for name in ["open", "close", "volume"]:
        frame[name] = pd.to_numeric(frame[name], errors="coerce")
    valid_identity = frame["date"].notna() & frame["symbol"].map(
        lambda x: isinstance(x, str) and bool(x.strip())
    )
    valid_identity &= frame["date"].eq(frame["date"].dt.normalize())
    audit["invalid_identity_rows"] = int((~valid_identity).sum())
    frame = frame.loc[valid_identity].copy()
    # Preserve the observed global date grid so removing a bad price does not bridge a label gap.
    calendar = pd.DatetimeIndex(sorted(frame["date"].unique()))
    before = len(frame)
    frame = frame.drop_duplicates()
    audit["exact_duplicates_removed"] = before - len(frame)
    if frame.duplicated(["date", "symbol"]).any():
        raise ValueError("Conflicting date/symbol rows require an explicit revision policy")
    price_ok = np.isfinite(frame[["open", "close"]]).all(axis=1) & (
        frame[["open", "close"]] > 0
    ).all(axis=1)
    available = frame["available_at"].notna() & (
        frame["available_at"] <= frame["date"] + pd.Timedelta(hours=21)
    )
    audit["invalid_price_rows"] = int((~price_ok).sum())
    audit["late_or_unknown_availability_rows"] = int((~available).sum())
    volume_ok = np.isfinite(frame["volume"]) & (frame["volume"] >= 0)
    audit["volume_values_marked_missing"] = int((~volume_ok).sum())
    frame.loc[~volume_ok, "volume"] = np.nan
    frame = frame.loc[price_ok & available].sort_values(["date", "symbol"]).reset_index(drop=True)
    audit["clean_rows"] = len(frame)
    if len(calendar) < 60 or frame.empty:
        raise ValueError("Insufficient dated observations after cleaning")
    return frame, calendar, audit


def build_dataset(clean, calendar, require_labels=True):
    outputs = []
    for symbol, group in clean.groupby("symbol", sort=True):
        grid = group.set_index("date").reindex(calendar)
        returns = grid["close"].pct_change(fill_method=None)
        features = pd.DataFrame(index=calendar)
        features["symbol"] = symbol
        features["momentum_5"] = grid["close"] / grid["close"].shift(5) - 1
        features["volatility_5"] = returns.rolling(5, min_periods=5).std(ddof=1)
        features["log_volume"] = np.log1p(grid["volume"])
        features["target"] = grid["open"].shift(-2) / grid["open"].shift(-1) - 1
        features["label_end"] = pd.Series(calendar, index=calendar).shift(-2)
        features["date"] = calendar
        # No imputation of tradable prices or outcome labels. Optional volume is imputed in training.
        eligible = grid["close"].rolling(6, min_periods=6).count().eq(6)
        required_features = ["momentum_5", "volatility_5"] + (["target"] if require_labels else [])
        eligible &= np.isfinite(features[required_features]).all(axis=1)
        outputs.append(features.loc[eligible])
    dataset = (
        pd.concat(outputs, ignore_index=True).sort_values(["date", "symbol"]).reset_index(drop=True)
    )
    if dataset.empty:
        raise ValueError("No complete feature/label windows")
    return dataset


def chronological_split(dataset):
    dates = sorted(dataset["date"].unique())
    if len(dates) < 50:
        raise ValueError("At least fifty eligible dates are required")
    validation_start, test_start = dates[int(len(dates) * 0.6)], dates[int(len(dates) * 0.8)]
    train = dataset[
        (dataset["date"] < validation_start) & (dataset["label_end"] < validation_start)
    ].copy()
    validation = dataset[
        (dataset["date"] >= validation_start)
        & (dataset["date"] < test_start)
        & (dataset["label_end"] < test_start)
    ].copy()
    test = dataset[dataset["date"] >= test_start].copy()
    development = dataset[
        (dataset["date"] < test_start) & (dataset["label_end"] < test_start)
    ].copy()
    if min(len(train), len(validation), len(test)) < 20:
        raise ValueError("Insufficient split sizes")
    return train, validation, test, development


def pipeline(estimator):
    return Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median", keep_empty_features=True)),
            ("scaler", StandardScaler()),
            ("model", estimator),
        ]
    )


def fit_models(dataset):
    train, validation, test, development = chronological_split(dataset)
    trials = []
    candidates = [(f"ridge-{alpha}", Ridge(alpha=alpha)) for alpha in [0.1, 1.0, 10.0]]
    candidates.append(
        (
            "forest-depth-3",
            RandomForestRegressor(
                n_estimators=60, max_depth=3, min_samples_leaf=12, random_state=SEED, n_jobs=1
            ),
        )
    )
    for name, estimator in candidates:
        model = pipeline(estimator).fit(train[FEATURES], train["target"])
        loss = mean_squared_error(validation["target"], model.predict(validation[FEATURES]))
        trials.append({"task": "regression", "name": name, "validation_mse": float(loss)})
    chosen = min(range(len(candidates)), key=lambda i: trials[i]["validation_mse"])
    reg_name, estimator = candidates[chosen]
    regressor = pipeline(estimator).fit(development[FEATURES], development["target"])
    if (train["target"] > 0).nunique() < 2 or (development["target"] > 0).nunique() < 2:
        raise ValueError("Classification training needs both outcome classes")
    classification = []
    for c in [0.1, 1.0, 10.0]:
        model = pipeline(LogisticRegression(C=c, max_iter=1000, random_state=SEED)).fit(
            train[FEATURES], train["target"] > 0
        )
        loss = brier_score_loss(
            validation["target"] > 0, model.predict_proba(validation[FEATURES])[:, 1]
        )
        classification.append({"task": "classification", "C": c, "validation_brier": float(loss)})
    c = min(classification, key=lambda row: row["validation_brier"])["C"]
    classifier = pipeline(LogisticRegression(C=c, max_iter=1000, random_state=SEED)).fit(
        development[FEATURES], development["target"] > 0
    )
    return {
        "regressor": regressor,
        "classifier": classifier,
        "regression_name": reg_name,
        "classification_C": c,
        "trials": trials + classification,
        "test": test,
        "train": train,
        "validation": validation,
        "development": development,
    }


def evaluate(fitted, roundtrip_bps=10):
    if not np.isfinite(roundtrip_bps) or not 0 <= roundtrip_bps <= 1000:
        raise ValueError("Round-trip cost must be between 0 and 1,000 basis points")
    test, development = fitted["test"], fitted["development"]
    prediction = fitted["regressor"].predict(test[FEATURES])
    probability = fitted["classifier"].predict_proba(test[FEATURES])[:, 1]
    actual, label = test["target"].to_numpy(), (test["target"] > 0).to_numpy()
    prior = float((development["target"] > 0).mean())
    baseline = np.full(len(test), float(development["target"].mean()))
    binary = probability >= 0.55  # Declared before test inspection; not optimized on test returns.
    tn, fp, fn, tp = confusion_matrix(label, binary, labels=[False, True]).ravel()
    calibration = []
    for lower, upper in [(0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0)]:
        mask = (probability >= lower) & (
            (probability < upper) if upper < 1 else (probability <= upper)
        )
        calibration.append(
            {
                "lower": lower,
                "upper": upper,
                "count": int(mask.sum()),
                "mean_probability": float(probability[mask].mean()) if mask.any() else None,
                "positive_rate": float(label[mask].mean()) if mask.any() else None,
            }
        )
    predictions = test[["date", "symbol", "label_end", "target"]].copy()
    predictions["prediction"] = prediction
    predictions["up_probability"] = probability
    # Opportunity-level proxy: close decision, next open entry, following open exit.
    # Each selected daily round trip pays the full stated cost; no broker, queues, or borrow model.
    cost = roundtrip_bps / 10000
    daily = []
    for date, group in predictions.groupby("date", sort=True):
        selected = group[group["prediction"] > cost]
        weight = min(0.4, 1 / len(selected)) if len(selected) else 0
        gross = float(weight * selected["target"].sum())
        fees = float(weight * len(selected) * cost)
        daily.append(
            {
                "date": date.isoformat(),
                "selected": len(selected),
                "invested_weight": weight * len(selected),
                "gross": gross,
                "cost": fees,
                "net": gross - fees,
            }
        )
    metrics = {
        "test_rows": len(test),
        "mse": float(mean_squared_error(actual, prediction)),
        "mae": float(mean_absolute_error(actual, prediction)),
        "r2": float(r2_score(actual, prediction)),
        "mean_baseline_mse": float(mean_squared_error(actual, baseline)),
        "brier": float(brier_score_loss(label, probability)),
        "prior_baseline_brier": float(brier_score_loss(label, np.full(len(label), prior))),
        "log_loss": float(log_loss(label, probability, labels=[False, True])),
        "roc_auc": float(roc_auc_score(label, probability)) if len(np.unique(label)) == 2 else None,
        "average_precision": float(average_precision_score(label, probability))
        if label.any()
        else None,
        "classification_threshold": 0.55,
        "confusion": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
        "precision": float(tp / (tp + fp)) if tp + fp else None,
        "recall": float(tp / (tp + fn)) if tp + fn else None,
        "calibration_bins": calibration,
        "roundtrip_bps": roundtrip_bps,
        "opportunity_proxy_return": float(np.prod([1 + row["net"] for row in daily]) - 1),
    }
    return metrics, predictions, daily


def monitoring(fitted):
    reference, current = fitted["development"], fitted["test"]
    mean = reference[FEATURES].mean()
    scale = reference[FEATURES].std(ddof=0).replace(0, np.nan)
    shift = ((current[FEATURES].mean() - mean) / scale).replace([np.inf, -np.inf], np.nan)
    return {
        "reference_rows": len(reference),
        "current_rows": len(current),
        "reference_missing_rate": reference[FEATURES].isna().mean().to_dict(),
        "current_missing_rate": current[FEATURES].isna().mean().to_dict(),
        "standardized_mean_shift": {k: None if pd.isna(v) else float(v) for k, v in shift.items()},
        "interpretation": "descriptive input monitoring; no automatic drift significance test or retraining decision",
    }


def run(output, csv=None):
    output = Path(output)
    # A fresh output directory prevents silently overwriting another experiment's evidence.
    output.mkdir(parents=True, exist_ok=False)
    raw = pd.read_csv(csv) if csv else synthetic_bars()
    clean, calendar, audit = clean_bars(raw)
    dataset = build_dataset(clean, calendar)
    fitted = fit_models(dataset)
    metrics, predictions, daily = evaluate(fitted)
    raw.to_csv(output / "raw.csv", index=False)
    clean.to_csv(output / "clean.csv", index=False)
    dataset.to_csv(output / "dataset.csv", index=False)
    predictions.to_csv(output / "predictions.csv", index=False)
    for name in ["regressor", "classifier"]:
        path = output / f"{name}.joblib"
        joblib.dump(fitted[name], path)
        # Load only the exact artifact this process just wrote. Never load an untrusted pickle.
        restored = joblib.load(path)
        np.testing.assert_allclose(
            restored.predict(fitted["test"][FEATURES]),
            fitted[name].predict(fitted["test"][FEATURES]),
        )
    split_manifest = {}
    for name in ["train", "validation", "test", "development"]:
        frame = fitted[name]
        split_manifest[name] = {
            "rows": len(frame),
            "first_decision": frame["date"].min().isoformat(),
            "last_decision": frame["date"].max().isoformat(),
            "last_label_end": frame["label_end"].max().isoformat(),
        }
    report = {
        "scope": "synthetic educational demonstration"
        if csv is None
        else "user-provided data under the declared CSV timing contract",
        "task": "features at close t; predict open(t+2)/open(t+1)-1; classify its positive sign",
        "features": FEATURES,
        "seed": SEED,
        "audit": audit,
        "splits": split_manifest,
        "selected": {
            "regression": fitted["regression_name"],
            "classification_C": fitted["classification_C"],
        },
        "trials": fitted["trials"],
        "metrics": metrics,
        "monitoring": monitoring(fitted),
        "versions": {
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "sklearn": sklearn.__version__,
        },
        "data_sha256": hashlib.sha256((output / "raw.csv").read_bytes()).hexdigest(),
        "model_sha256": {
            name: hashlib.sha256((output / f"{name}.joblib").read_bytes()).hexdigest()
            for name in ["regressor", "classifier"]
        },
        "limitations": [
            "Synthetic business-day grid is not an exchange calendar",
            "No actual corporate actions, point-in-time fundamentals, or delisted universe",
            "No public market/order connection",
            "Opportunity return proxy omits queues, spreads beyond stated cost, and full broker cash accounting",
            "Test results cannot be reused as untouched evidence after further tuning",
            "Joblib artifacts are executable Python serialization; load only your own trusted files in the matching environment",
        ],
    }
    (output / "report.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    (output / "opportunities.json").write_text(json.dumps(daily, indent=2, allow_nan=False) + "\n")
    (output / "MODEL_CARD.md").write_text(
        "# Local stock-ML model card\n\n"
        + report["scope"]
        + ".\n\n"
        + "Task: "
        + report["task"]
        + ".\n\n"
        + "The report contains data exclusions, split boundaries, validation trials, held-out metrics, input monitoring, versions, and artifact hashes. "
        + "Selection uses validation only; final models refit eligible development rows before a fixed test. Baselines and unsuccessful results remain visible.\n\n"
        + "## Release review\n\nThis run creates local artifacts only. Review data provenance, errors, cost sensitivity, feature parity, and mature-label monitoring before any separate paper integration. "
        + "The default acceptance decision is research review pending; no metric automatically authorizes trading.\n\n"
        + "## Limits\n\n"
        + "\n".join("- " + item for item in report["limitations"])
        + "\n"
    )
    return report


def score(model_run, csv, output):
    """Batch inference for an explicitly trusted local artifact, including unmatured rows."""
    model_run, output = Path(model_run), Path(output)
    report = json.loads((model_run / "report.json").read_text())
    versions = {"numpy": np.__version__, "pandas": pd.__version__, "sklearn": sklearn.__version__}
    if report["versions"] != versions or report["features"] != FEATURES:
        raise ValueError("Model environment or feature schema mismatch")
    raw = pd.read_csv(csv)
    clean, calendar, audit = clean_bars(raw)
    features = build_dataset(clean, calendar, require_labels=False)
    predictions = features[["date", "symbol"]].copy()
    for name in ["regressor", "classifier"]:
        path = model_run / f"{name}.joblib"
        if hashlib.sha256(path.read_bytes()).hexdigest() != report["model_sha256"][name]:
            raise ValueError("Artifact does not match its local run manifest")
        # Hash matching is integrity evidence, not trust: caller must trust this run's origin.
        model = joblib.load(path)
        predictions[name] = (
            model.predict(features[FEATURES])
            if name == "regressor"
            else model.predict_proba(features[FEATURES])[:, 1]
        )
    output.mkdir(parents=True, exist_ok=False)
    predictions.to_csv(output / "batch_predictions.csv", index=False)
    (output / "inference_audit.json").write_text(
        json.dumps(
            {
                "scope": "local batch inference; no orders",
                "audit": audit,
                "rows": len(predictions),
                "last_decision": predictions["date"].max().isoformat(),
            },
            indent=2,
        )
        + "\n"
    )
    return {
        "output": str(output),
        "rows": len(predictions),
        "scope": "local batch predictions; no orders",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="ml-run", help="New directory for this run's artifacts")
    parser.add_argument(
        "--csv", type=Path, help="Optional CSV conforming to the guide's timing and schema contract"
    )
    parser.add_argument(
        "--score-run", type=Path, help="Previously generated local model-run directory to score"
    )
    parser.add_argument(
        "--trust-local-model",
        action="store_true",
        help="Confirm this is your own trusted local serialization; never use untrusted model files",
    )
    args = parser.parse_args()
    if args.score_run:
        if not args.csv or not args.trust_local_model:
            parser.error(
                "Batch scoring requires --csv and --trust-local-model for your own trusted artifact"
            )
        summary = score(args.score_run, args.csv, args.output)
    else:
        result = run(args.output, args.csv)
        summary = {
            "output": args.output,
            "selected": result["selected"],
            "metrics": result["metrics"],
        }
    print(json.dumps(summary, indent=2, allow_nan=False))
