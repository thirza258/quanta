# Final track: algorithm evaluation & results reporting

Open `/curriculum/algorithm-evaluation`. This is the last catalog course, after stock machine learning; lessons use new `10.1`–`10.16` IDs. It synthesizes work from the Python bot, C/HPC, quantitative, econometric and ML courses without changing their content or progress identifiers.

**16 lessons × 30 minutes = 8 hours** of planned reading, calculation and report work; exam time is additional. Each lesson has an original explanation, worked case/equation, guided arithmetic worksheet, two practice questions, assignment/solution and primary references. Four checkpoints cover every unit; the version-1 final has 16 questions and requires 13 correct (80% threshold). The written report is assessed separately against a 100-point rubric.

| Unit | Lessons | Deliverable |
| --- | --- | --- |
| Define and audit evaluation | 10.1–10.4 | Hypothesis, acceptance criteria, export contract, source manifest, benchmark and cost/flow reconciliation |
| Measure return, risk and execution | 10.5–10.8 | Compounded return, risk ratios, drawdown analysis, execution and cost appendix |
| Challenge the result | 10.9–10.12 | Holdout/search disclosure, uncertainty, robustness matrix and C/HPC timing evidence |
| Create and defend the report | 10.13–10.16 | Clear tables/figures, attribution, executive conclusion and reproducible dossier |

## Reporting project

Sources are in `content/projects/algorithm-evaluation/`; the source-only archive and notebook are downloadable from the course. The report accepts outputs from algorithms in any language. Its implementation uses Python, with Matplotlib for exportable figures and a standard-library-only `--no-charts` mode for tables/reports.

```sh
cd content/projects/algorithm-evaluation
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest -v
.venv/bin/python evaluate.py --timings timings.example.csv --out report-output
```

The output folder contains `metrics.json`, `report.md`, printable `report.html`, `evaluation.png` and `evaluation.svg`. Keep it together so image references work. A browser can print the HTML to PDF. The report includes input/evaluator SHA-256 hashes, declared assumptions, runtime versions, metrics, limitations and references. Its conclusion remains **REVIEW REQUIRED** until the learner supplies their evidence-based interpretation and decision.

The fixture has 13 monthly valuations including initial capital: 12 returns, 10% net strategy return, 8% benchmark return, a **2 percentage-point** cumulative difference, and a **6.6667%** maximum drawdown from 10,500 to 9,800. Its paired timing fixture has five repetitions and a median paired speedup of **3×**. These numbers are original fictional examples, not real-market or local-hardware results.

Implemented metrics include total/geometric annualized return, sample volatility, Sharpe, Sortino, drawdown, tracking error, information ratio, mean active return and a descriptive seeded circular-block interval. Undefined denominators remain null; short-sample, synthetic and test-reuse limitations are surfaced. Input dates must be unique/increasing, values finite/positive, and equity already net of declared modeled costs with no external flows. Calendar completeness and source/split labels require author review. Annualization uses the declared observation frequency; the interval is not a selection-bias correction.

The optional timing file summarizes paired serial/parallel elapsed times with medians and range. Copy actual timing rows from the C/HPC lab and preserve equality/build/workload evidence. That lab's terminal equity summary is not a valuation path and cannot determine Sharpe or drawdown; a compatible dated valuation export is required.

## Evidence and boundaries

The project checks independent returns/drawdown arithmetic, undefined constant-series ratios, reproducible block intervals, malformed/nonfinite/overflowing inputs, duplicate dates, manifest conventions, paired timings, HTML escaping and traceable report generation. Root backend tests extract the actual learner archive and run its nine checks plus the CLI. Chart generation is verified separately using the declared Matplotlib dependency.

Reports describe supplied evidence. The project does not reconstruct missing trade events, fit factor attribution, execute every sensitivity/stress scenario, infer valid holdouts from labels, certify standards compliance or automatically approve a strategy. Those analyses and conclusions require the learner's separately recorded work. All in-browser worksheets are arithmetic aids; the full reporting pipeline runs locally.

Primary material includes [CFA Institute performance evaluation](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/portfolio-performance-evaluation), [fair presentation](https://www.cfainstitute.org/standards/professionals/code-ethics-standards/standards-of-practice-iii-d), [Bailey et al. on backtest overfitting](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf), [leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html), [circular block bootstrap documentation](https://arch.readthedocs.io/en/latest/bootstrap/generated/arch.bootstrap.CircularBlockBootstrap.html) and [Matplotlib export](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html). Cases, code and questions are original.
