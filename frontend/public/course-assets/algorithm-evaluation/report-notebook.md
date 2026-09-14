# Algorithm evaluation dossier

## 1. Question and acceptance criteria

Strategy/source version, research hypothesis, eligible universe, signal availability, fill rule, cost model, benchmark, metrics, rejection thresholds, intended reader. Write these before examining the final test result.

## 2. Evidence ledger

Dataset/source hashes, date range, calendar and frequency, initial valuation, net/gross basis, external cash flows, corporate actions, missing/duplicate records, aligned benchmark, train/validation/test definitions, every configuration tried, any test-set reuse. Identify what is declared versus independently verified.

## 3. Results and diagnostics

Attach metrics.json, full-period wealth/drawdown charts and selected trade/execution diagnostics. Explain absolute return, cumulative benchmark difference, risk, drawdown duration/recovery and cost sensitivity. A return difference is not automatically factor-adjusted alpha. Undefined ratios stay undefined.

## 4. Robustness

Chronological holdout, walk-forward folds, parameter neighborhoods, delayed signals, higher costs, missing bars, regime/sector concentration and small-sample uncertainty. State which analyses were actually executed. The supplied block interval is descriptive and does not correct a selected winner's bias.

## 5. Computing and operations

Correctness parity, workload size, seeds, serial/parallel timing boundaries, five or more paired repetitions, medians/spread, CPU/OS/compiler/flags, data freshness, queue limits, failure recovery. Faster computation is a separate result from trading performance.

## 6. One-page conclusion

Decision: reject, revise, or proceed to a bounded paper study. State the strongest supporting observation, strongest contrary observation, what remains unknown, the next falsification test and a review trigger. Link each factual claim to a table, figure, source or test artifact. Complete this manually; the generator intentionally leaves the conclusion marked REVIEW REQUIRED.

## Capstone rubric (separate from the concept exam)

| Area | Points |
| --- | --- |
| Reproducible inputs, source hashes and timing/cost contract | 20 |
| Correct and reconciled return/risk/benchmark calculations | 25 |
| Holdout, selection disclosure, stress and uncertainty | 25 |
| Clear charts/tables and balanced written interpretation | 20 |
| Computing/operational evidence and next-step decision | 10 |

Target 80/100. Any unresolved look-ahead, mismatched benchmark, hidden cash flow, fabricated result or missing loss period requires revision regardless of the score. No certification or production approval is implied.
