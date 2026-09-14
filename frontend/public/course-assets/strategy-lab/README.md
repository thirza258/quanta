# Strategy Lab: reproducible investment research

This original Quanta project accompanies the 32-lesson Strategy Lab course. It uses
fictional companies and deterministic daily observations. Python 3.10 or newer is
sufficient; no packages, market credentials or network access are required.

```sh
python3 -m unittest -v
python3 strategy_lab.py
```

The program requires a new or empty output directory. To preserve experiments:

```sh
python3 strategy_lab.py --output experiment-002
```

Complete `research-notebook.md` before using the final evaluation outcome to make
another research choice. The included 90 business-session fixture is a correctness
exercise, not evidence of real-market profitability.

## What actually runs

| Candidate | Selection rule | Allocation |
| --- | --- | --- |
| Equal-weight | Every fixture symbol | Equal target weights, capped at 40% |
| Value-quality | Available, nonstale filing; positive earnings yield and ROIC; coverage at least 2; close strictly below two-thirds NCAV | Top two by summed earnings-yield/ROIC midranks, up to 40% each |
| Momentum | Positive trailing return over five observations, skipping the latest observation | Top two, up to 40% each |

Exact final score ties use alphabetical symbol order. Insufficient candidates leave
cash. All three candidates use the same fill engine. The value-quality example's
NCAV is supplied per share: it is not a full balance-sheet parser. No fitted ML or
two-leg pairs engine is claimed. Those units provide calculations, protocols and
extension assignments, with further implementation in the econometrics and ML tracks.

## Data and accounting contract

- `prices.csv`: sorted unique date/symbol rows with positive finite open/close and
  nonnegative integer volume. Every session contains the same symbols. Missing
  prices and changing membership are rejected, not forward-filled.
- `fundamentals.csv`: period end, availability date and revision identity. A filing
  becomes usable strictly after its date-only availability date. Select the latest
  available reporting period, then its latest available revision; period age above
  180 days is excluded. A late old-quarter amendment cannot replace a newer quarter.
- The fictional universe has no splits, dividends, delistings or external flows.
  Real data need explicit adapters and action/terminal-value policies before use.
- Form whole-share targets from completed-close equity. Execute at the next open,
  sells before buys, alphabetical order when cash is scarce. Charge 20 basis points
  on each filled notional. Unfilled quantities expire after that open.
- Cap fill quantity at 5% of **prior-session** volume. This proxy is not an actual
  opening-auction or order-book liquidity estimate. Spread and impact are omitted.
- A target-weight cap applies at the decision close; gaps and drift can exceed it
  later. Cash constraints prevent undeclared borrowing. Fees use floating-point
  arithmetic with invariant tolerances; this is not production broker accounting.
- Mark holdings at each close. Ending positions remain open, so liquidation costs
  are omitted. Cash earns zero in the fixture.

The benchmark in each `equity.csv` is a frictionless daily-rebalanced equal-weight
close-to-close index. It is labeled separately from the executable equal-weight
candidate, which uses the same next-open costs and constraints as the other rules.

## Selection and exported evidence

The first third provides development/warm-up history. The middle third evaluates
all three predeclared candidates; maximum net total return selects the winner,
with fixed candidate order breaking ties. Only that frozen candidate runs on the
last third. Each segment resets to 10,000 cash at its initial decision close;
historical prices remain available for causal indicator warm-up. No positions
carry across segments. This is a reset evaluation, not a continuous walk-forward
portfolio and not a fitted-model training experiment.

The selected rule also runs with doubled costs and a five-times tighter prior-volume
cap. These are post-selection diagnostics, not new winners. `experiments.json`
retains all three validation outcomes, selected test outcome and both stresses.
Disclose additional manual trials and every repeat inspection of the final segment.

Each result directory contains:

- `signals.csv`: decision date, score and requested target shares for every symbol.
- `trades.csv`: requested, filled and expired quantities, fill prices, fees and dates.
- `positions.csv`: cash, quantities, closing position values and reconcilable equity.
- `equity.csv`: aligned initial-plus-subsequent strategy and benchmark valuations.
- `metrics.json`: total return, maximum drawdown, total fees, traded notional divided
  by decision equity, and nonzero fill count. No short-sample annual return is claimed.
- `manifest.json`: exact source/input hashes, sample bounds and implementation rules.

To use the final Algorithm Evaluation course, unpack its reporting archive and run:

```sh
python3 evaluate.py --equity /path/to/strategy-output/test/equity.csv \
  --manifest /path/to/strategy-output/test/manifest.json --no-charts
```

Install that course's optional plotting dependency to produce its charts. The
manifest labels this as synthetic and discloses selection; a hash identifies bytes,
not data correctness. Replacing the fixture requires updating the provenance and
evaluation design rather than relabeling synthetic results as market evidence.

## Independent checks and extensions

The eleven unit tests include a manually calculated two-share round trip: start
1,000, buy at 100 and sell at 110, charge 1% per side, finish at **1,015.8** with
**4.2** fees. Other checks cover future-data mutations, filing revisions, momentum
endpoints, prior-volume caps, cash, deterministic priorities, reconciliation,
validation-only selection and malformed input.

Choose one extension in the notebook: NCAV recovery haircuts, rebalance buffers,
time-series filters or an explicit execution delay. Pairs borrow/atomic execution,
trained ML, corporate actions, external datasets, impact and live order routing
require additional implementation and independent verification.

## References and authorship

All source code, synthetic data, examples and questions are original Quanta teaching
material. No book text, publisher exercises or third-party market dataset is bundled.
References provide further reading and do not imply affiliation or endorsement.

- [SEC EDGAR disclosure APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- [Kenneth French: five-factor construction](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_5_factors_2x3.html)
- [Kenneth French: momentum construction](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_mom_factor.html)
- [scikit-learn: data leakage](https://scikit-learn.org/stable/common_pitfalls.html)
- [Bailey et al.: backtest overfitting](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf)
