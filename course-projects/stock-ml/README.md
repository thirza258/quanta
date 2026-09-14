# Machine learning for stocks: 12-hour lifecycle project

Original Quanta course and local project. Default stock data are synthetic, with deliberately invalid, duplicated, missing, and late rows. No market-data credentials, GPU, model service, or trading account is required.

## Study schedule

24 lessons × 30 minutes = **12 hours**, organized as six two-hour units. Each session allocates eight minutes to the explanation and primary reading, eight to the guided calculation, and fourteen to its project assignment and review. This is estimated active study and lab time; the five checkpoints and final add assessment time. There are no claimed prerecorded video hours.

| Unit | Lessons | Work product |
| --- | --- | --- |
| Problem and data quality | 7.1–7.4 | Prediction contract, source manifest, schema checks, repair policies |
| Features, labels, splits | 7.5–7.8 | Feature lineage, maturity endpoints, purged date partitions, preprocessing |
| Training | 7.9–7.12 | Baselines, ridge/logistic/forest trials, bounded neural extension design |
| Selection and evaluation | 7.13–7.16 | Search ledger, walk-forward extension plan, metrics, calibration, costs |
| Diagnosis and improvement | 7.17–7.20 | Error slices, feature inspection, stress/uncertainty plan, controlled repair |
| Inference and monitoring | 7.21–7.24 | Saved pipelines, batch parity, mature-label monitoring, complete dossier |

## Run the complete default lifecycle

Use Python 3.12+ in a fresh environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python stock_ml_lab.py --output ml-run-001
python -m unittest -v
```

The output directory must be new, so previous evidence is not silently overwritten. The run fits real scikit-learn models; guided in-app worksheets perform only their stated small calculations and keep the market sandbox in cash.

The pipeline:

1. Generates three synthetic symbols across a business-day grid, plus seeded data faults.
2. Validates identity, positive prices, volume, duplicate conflicts, and availability by a synthetic 21:00 UTC cutoff. It removes exact duplicates, excludes bad prices and late observations, and retains optional missing volume.
3. Reindexes each symbol to the observed global date grid. It requires complete price windows for five-period momentum and volatility; log-volume may be imputed later.
4. Defines features after close t, target `open(t+2)/open(t+1)-1`, and the binary positive-sign label. Training requires matured outcomes.
5. Splits globally by date at approximately 60/20/20 and purges labels ending at or beyond the next boundary.
6. Fits median imputation and scaling inside each training pipeline. It compares ridge penalties .1/1/10 and a bounded random forest by validation MSE; logistic C values .1/1/10 use validation Brier loss.
7. Refits selected configurations on eligible pre-test development rows and evaluates the frozen held-out test. The single validation split is not a nested walk-forward evaluation; lesson 7.13 specifies that extension.
8. Reports mean/prior baselines, MSE, MAE, R², Brier loss, log loss, ROC AUC where defined, average precision, confusion counts at a prespecified .55 threshold, reliability bins, and descriptive input monitoring.
9. Saves complete pipelines and checks save/load prediction parity for its own artifacts.

## Artifacts

- `raw.csv`, `clean.csv`, `dataset.csv`: source fixture, retained observations, dated features and labels.
- `report.json`: exclusions, split boundaries, trials, selected parameters, held-out metrics, versions, data/model hashes, monitoring, and limitations.
- `predictions.csv`: dated held-out regression predictions and sign probabilities.
- `opportunities.json`: a declared next-open daily opportunity proxy with full round-trip costs and per-name .4 weight cap. It omits a full broker ledger, queues, settlement, and borrow.
- `regressor.joblib`, `classifier.joblib`: fitted preprocessing and estimators.
- `MODEL_CARD.md`: intended task, evidence, limits, and pending release review.

No positive return is required or promised. A baseline may outperform the trained model. Preserve that finding.

## Batch inference with your own trusted artifact

```sh
python stock_ml_lab.py --score-run ml-run-001 --csv ml-run-001/raw.csv --trust-local-model --output score-run-001
```

The scorer verifies feature schema, environment versions, and model hashes, and emits `batch_predictions.csv` and `inference_audit.json`. It also scores eligible latest rows without requiring future labels. Historical rows should match the same frozen model's saved predictions; additional latest rows have pending outcomes.

Joblib serialization can execute Python during loading. The explicit flag is for your own trusted locally generated run, not arbitrary downloaded model files. Hash matching establishes consistency with a manifest, not trust in an unknown author. No scoring command submits orders.

## Optional CSV contract

`--csv input.csv` replaces the synthetic input. Required columns: `date` (UTC calendar date), `symbol` (stable nonempty identifier), positive numeric `open`/`close`, nonnegative `volume` or missing, and `available_at` (UTC timestamp). Conflicting same-date/symbol records reject until a revision policy is supplied. The model uses a synthetic fixed 21:00 UTC cutoff and the globally observed date grid; it does not infer a real exchange's holidays, sessions, corporate actions, delisted membership, or entirely absent market dates. Actual market research requires adapting and verifying those conventions, provenance, and rights first. Do not mix currencies or raw and adjusted price conventions silently.

## Required capstone and explicit extensions

Reproduce the run and tests, introduce and repair one known data fault in a new run, add error slices, verify historical batch parity and latest-row inference, and write the monitoring/decision memo. Preserve all trial and data versions. Grade the dossier with the course rubric; the automatic exam does not inspect local files.

The course also teaches neural/boosting candidates, nested walk-forward evaluation, post-hoc calibration, feature permutation, dependent bootstrap, and paper-bot integration. These are specified extension assignments; they are not falsely claimed as default trained components. They require their own implementation evidence and evaluation boundaries.

Primary sources: [pandas missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html), [as-of joins](https://pandas.pydata.org/docs/reference/api/pandas.merge_asof.html), [scikit-learn pipelines](https://scikit-learn.org/stable/modules/compose.html), [model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html), [calibration](https://scikit-learn.org/stable/modules/calibration.html), [model persistence](https://scikit-learn.org/stable/model_persistence.html). The lessons, synthetic cases, and project orchestration are original; dependencies retain their own authorship and licenses.
