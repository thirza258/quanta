# Algorithm evaluation and reporting lab

Original Quanta final-course project. Turn aligned algorithm and benchmark valuations into JSON metrics, Markdown and printable HTML reports with standalone PNG/SVG charts. Python is used for reporting; the algorithm being evaluated may be written in C, Python or another language.

## Run the complete sample

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest -v
.venv/bin/python evaluate.py --timings timings.example.csv --out report-output
```

Open `report-output/report.html` in a browser. It references the local SVG chart, so keep the report folder together. For a table-only report without third-party dependencies:

```sh
python3 evaluate.py --timings timings.example.csv --out report-output --no-charts
```

The initial report is deliberately marked **REVIEW REQUIRED**. Complete `report-notebook.md` with your interpretation, contradictory evidence, decision and next test. The generator calculates descriptive statistics; it does not decide whether the strategy should trade.

## Input contract

`equity.example.csv` uses exactly `date,equity,benchmark`. The first row is initial wealth, followed by aligned regular valuation periods. Values must be finite and strictly positive, dates unique and increasing. No external deposits or withdrawals are allowed in this ratio-return model; flow-adjusted returns require a separate adapter. A nonpositive balance is rejected explicitly and needs an insolvency convention, never deletion of the bad period.

Calendar completeness is an author check. `periods_per_year` is a declared frequency convention, not inferred from row count. Use an appropriate calendar and aligned periods before exporting. The example contains 12 monthly returns and one initial valuation over a year. It has strategy total return **10%**, benchmark **8%**, cumulative difference **2 percentage points**, and maximum strategy drawdown **6.6667%** from 10,500 to 9,800. These are fictional reporting fixtures.

`manifest.example.json` declares source/version, data provenance, benchmark, frequency, annual risk-free rate, net-cost basis, cost model, split, number of configurations tried, test-set reuse and computing environment. Input labels are not independently certified by the tool. Replace every illustrative field before using your own results. `timings.example.csv` is optional; it uses exactly `repeat,serial_ms,parallel_ms` with unique IDs and positive paired elapsed times.

The C/HPC lab's benchmark prints five paired timing rows; transcribe their `serial_ms` and `parallel_ms` into this timing schema with their repeat IDs. Keep `equal=yes` evidence and hardware/build metadata in the notebook. Its terminal window/equity/fill summary is NOT an equity path: do not invent Sharpe or drawdown from final values. Export a selected run's dated valuation history and aligned benchmark under this schema, or evaluate a separately supplied valid history.

## Calculations and boundaries

- Period return: current equity / previous equity − 1, including the initial valuation.
- Total return compounds the supplied path; cumulative strategy-minus-benchmark return is labeled as a percentage-point difference, not Jensen alpha.
- Geometric annualization is omitted below one declared year of observations. It uses the supplied period convention.
- Volatility and tracking error use sample standard deviation and square-root annualization. Sharpe subtracts the geometric per-period risk-free rate. Sortino uses root mean squared negative excess returns over ALL observations. Zero denominators stay undefined.
- Drawdown includes the initial capital peak. Charts show common dates and scales; wealth curves both start at 100.
- A seeded circular block bootstrap gives a descriptive 95% interval for mean periodic active return (three-observation blocks, 1,000 repetitions, seed 42). This is not an overfitting correction, a guarantee, or a reliable rare-tail model. Short histories are explicitly flagged.
- Timing reports show paired-speedup median and elapsed-time medians/range. The sample timings are illustrative, not measurements of your computer.

Input/evaluator SHA-256 hashes accompany output. Reports include primary references and disclose synthetic samples, short histories and reused test periods. They do not reconstruct trades, fit factors, estimate live market impact, certify GIPS compliance, or automatically run every stress test proposed in the course. These require separately supplied evidence. HTML escapes input text and runs offline without scripts.

## Primary references

- [CFA Institute: portfolio performance evaluation](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/portfolio-performance-evaluation)
- [CFA Institute: fair performance presentation](https://www.cfainstitute.org/standards/professionals/code-ethics-standards/standards-of-practice-iii-d)
- [Bailey, Borwein, López de Prado and Zhu: probability of backtest overfitting](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf)
- [scikit-learn: evaluation leakage](https://scikit-learn.org/stable/common_pitfalls.html)
- [Matplotlib: figure export](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html)

Cases and reporting code are original. Attribution does not imply endorsement or permission to reproduce a source work.
