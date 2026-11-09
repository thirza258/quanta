# Research platform

The research platform turns a backtest into a registered experiment. A learner states a hypothesis, declares the data, the strategy and a parameter grid, and runs it. The run then tries to disprove its own result with out-of-sample validation, parameter and cost stress, benchmarks, overfitting statistics and a look-ahead test, and a research red team summarizes what survived. Every run is fingerprinted so it can be repeated and compared, and an experiment exports as a Markdown or HTML research note. The platform's motto is *Don't just backtest it. Try to break it.*

Every backtest goes through the same long/cash engine the Strategy lab and the courses use, `domain/analytics.py::backtest`; nothing in the platform re-implements execution. Strategy code runs only in the existing sandbox. Results describe simulated, educational experiments. A run grades how thoroughly a claim was tested, not whether to invest in it: **research quality is not investment quality.**

The registry at `/research` is separate from **Saved experiments** at `/experiments`, which keeps Strategy lab snapshots in workspace state.

## The research loop

1. **Register.** Give a title and a hypothesis of 12 to 2,000 characters. The hypothesis is stamped with the time it was registered. It can be rewritten, and is re-stamped, until the first run completes; after that it is locked, so a claim cannot be refitted to its result. What was learned goes in the conclusion instead.
2. **Declare.** Choose the dataset, the strategy code and its parameter grid, costs, and validation settings (see [Experiment specification](#experiment-specification)).
3. **Run.** A background job runs every configuration and tries to break the result (see [What a run does](#what-a-run-does)).
4. **Read the red team.** Twelve checks each pass, warn, fail or are skipped, add up to a research-risk level, and name the lesson that teaches them.
5. **Document.** Record a conclusion, the limitations and a decision: `trust`, `reject` or `inconclusive`.
6. **Reproduce.** Rerun the current run's frozen specification. The platform compares the fingerprints of both runs and their outputs.
7. **Export.** Download the research note as Markdown or standalone HTML.

The frontend has three routes. **Experiment registry** in the sidebar's Research group opens the first.

| Route | Purpose |
| --- | --- |
| `/research` | The owner's experiments, most recently updated first, with lifecycle status, research risk and headline metrics |
| `/research/new` | Register an experiment: hypothesis, dataset, strategy code or a template, parameter grid, costs and validation settings. `?edit=<id>` reopens an existing experiment's specification; **Edit specification** on the experiment page links there. |
| `/research/:experimentId` | One experiment, in sections: Overview, Validation, Robustness, Red team, Notebook and Provenance. It shows an active run's progress, **Reproduce** reruns the current run, and the research note exports as Markdown or HTML. |

**Validate in research** carries a strategy from the Strategy lab into `/research/new`, with its code, dataset configuration and title. The link appears in the Strategy lab sandbox and on each saved experiment.

`frontend/src/features/research/model/registry.ts` holds the typed contract for the API those pages use.

## What a run does

The work happens in this order.

1. **Admission.** Starting a run (creating an experiment with `run: true`, `POST …/runs`, or a rerun) passes the `research` rate limit, the owner's one-active-run check and the process queue cap.
2. **Versioning.** The strategy source is registered as a strategy version. The prior-trial count is taken from the owner's earlier completed runs of the same strategy name, or copied from the original run for a rerun. The run is stored as `queued` with a frozen copy of the specification, and the request returns 202.
3. **Data** (stage `data`). The market-data provider describes and loads the bars. The bars are hashed, and the dataset version is registered or reused.
4. **Strategies** (stage `strategies`). The base configuration runs first, on its own. If it fails, the run fails with the sandbox's message. If the grid declares parameters but the code declares `strategy(data)`, the run fails with: `strategy(data) ignores the parameter grid. Declare strategy(data, params) and read values such as params["fast"].` The remaining jobs then run in parallel, in this order:
   - the base configuration on histories cut short, for the look-ahead test;
   - every other configuration on the full history;
   - the base configuration on each alternative synthetic path.

   An error in a configuration or on a path fails the run. An error on a shortened history counts as a look-ahead failure instead.
5. **Headline.** The look-ahead comparison runs first. Then the base configuration is backtested, with buy-and-hold and a trend baseline beside it.
6. **Validation** (stage `validation`). The train/test split runs, then walk-forward selection unless it is switched off.
7. **Robustness** (stage `robustness`). This stage covers the parameter surface and stability score, transaction-cost stress, and alternative market paths.
8. **Diagnostics** (stage `diagnostics`). This stage covers the trial count, the deflated Sharpe ratio, the probability of backtest overfitting, the random-timing test and profit concentration.
9. **Red team** (stage `red team`). The checks and the research-risk level are computed.
10. **Storage.** The run stores its results, provenance, summary and duration. A rerun also stores its comparison with the original run. The status becomes `completed`, and the process writes one structured log line.

Progress is reported as completed steps out of a total. The total is the number of configurations, plus the number of look-ahead cut points, plus the number of alternative paths, plus 4 (one step each for validation, robustness, diagnostics and the red team). The defaults give 12 + 3 + 5 + 4 = 24 steps.

Everything after the sandbox calls is deterministic. The same specification and the same data give the same results, byte for byte.

A run stores:

- its results as one JSON document. This includes every configuration's metrics, the headline equity curve and the stitched walk-forward curve, each downsampled to at most 600 points that always include the first and last bar. It also keeps the first 1,000 trades with the total trade count, and the base configuration's printed output, cut to 4,000 characters;
- its provenance;
- a summary of research risk, validity, the configuration count and five metrics (CAGR, Sharpe, maximum drawdown, turnover, total return).

Per-bar signals and daily return series are not stored. A rerun recomputes them.

## Writing strategies

A strategy is a Python function named `strategy`:

```python
def strategy(data, params):
    # Trend rule: hold while the fast average is above the slow one.
    fast = sma(data["close"], params["fast"])
    slow = sma(data["close"], params["slow"])
    return fast > slow
```

- **Signature.** Declare either `strategy(data)` or `strategy(data, params)`; any other number of arguments is refused. With a parameter grid, the function must accept `params`. In the Strategy lab sandbox, which has no grid, `params` is an empty dictionary.
- **Return value.** Return one Boolean (or 0/1) per bar, or a single Boolean for every bar. `True` means long and `False` means cash. Fractional weights, shorts and multiple assets are outside this backtester.
- **Timing.** A signal computed at a bar's close acts at the next bar's open, so using the current close is legitimate.
- **`data`.** These series are available: `open`, `high`, `low`, `close`, `volume`, `returns`, `sma_50` and `sma_200`.
  - `returns` is the close-to-close return, with 0 on the first bar.
  - `sma_50` is the trailing mean over the dataset's `window` setting, which defaults to 50.
  - `sma_200` is the 200-bar trailing mean.
  - Both averages use the partial-window warm-up described below.
- **`params`.** This is a dictionary with one number per grid parameter, for example `params["fast"]`. Parameter values must be finite numbers.
- **Runtimes.** In the guided runtime (the default), `data` maps names to numeric series, and the documented Python subset applies (see the [README](../README.md#python-execution)). In the optional Docker runtime, `data` is a pandas DataFrame, the helpers return pandas Series, and `np` and `pd` are predefined.

### Trailing-window helpers

Both runtimes provide eight helpers. Each reads only the current and earlier bars. On the first bars, before a full window exists, each uses the observations available so far. This partial-window warm-up matches the `sma_50` and `sma_200` columns. The window `n` must be a whole number from 1 to 10,000; `shift` also accepts 0.

| Helper | Value at bar *i* | First bars (fewer than *n* earlier values) |
| --- | --- | --- |
| `sma(series, n)` | Mean of the last *n* values | Mean of every value so far |
| `ema(series, n)` | `α·x[i] + (1 − α)·ema[i − 1]`, with `α = 2 / (n + 1)` | Seeded with the first value |
| `highest(series, n)` | Highest of the last *n* values | Highest so far |
| `lowest(series, n)` | Lowest of the last *n* values | Lowest so far |
| `change(series, n)` | `x[i] / x[i − n] − 1` | Measured from the first value, so 0 on the first bar |
| `shift(series, n)` | `x[i − n]`, the value *n* bars ago | The first value, repeated |
| `stdev(series, n)` | Population standard deviation of the last *n* values | Over the values so far; 0 on the first bar |
| `zscore(series, n)` | `(x − sma) / stdev` over the last *n* values, or 0 when that deviation is at most 1e-12 | Over the values so far, so 0 on the first bar |

A negative `shift` is refused, because it would read bars that have not happened yet. The guided message is `shift() only looks back: a negative lag would read bars that have not happened yet.` `change` refuses an earlier value of zero in both runtimes (`change() divides by an earlier value of zero.`). The helpers make a rule causal only if the rest of the code is causal too. A statistic computed over the whole series, such as its mean or maximum, still sees the future. The [look-ahead test](#look-ahead-truncation-test) exists to catch that.

### Templates

The options endpoint returns four templates. The first is also the default specification, named "Trend rule".

| Template | Rule | Grid | Base |
| --- | --- | --- | --- |
| `trend` · Moving-average crossover | `sma(close, fast) > sma(close, slow)` | fast ∈ {10, 20, 30, 50} × slow ∈ {100, 150, 200} (12) | fast 20, slow 150 |
| `momentum` · Time-series momentum | `change(close, lookback) > threshold` | lookback ∈ {21, 63, 126, 189, 252} × threshold ∈ {0, 0.02, 0.05} (15) | lookback 126, threshold 0 |
| `reversion` · Z-score mean reversion | `zscore(close, window) < −entry` | window ∈ {10, 20, 40, 60} × entry ∈ {0.5, 1, 1.5, 2} (16) | window 20, entry 1 |
| `channel` · Donchian channel midline | `close > (highest(high, lookback) + lowest(low, lookback)) / 2` | lookback ∈ {20, 40, 60, 100, 150} (5) | lookback 60 |

## Experiment specification

An experiment's specification has four parts. The API validates every field.

| Part | Field | Default | Bounds and rules |
| --- | --- | --- | --- |
| Dataset | `kind` | `synthetic` | `synthetic` or `historical`; historical requires `params.symbol` |
| | `params` | GBM, μ 8%, σ 20%, 3 years, seed 42, window 50 | The sandbox's dataset parameters: models `gbm`, `merton`, `heston`, `regime`; the five named scenarios; years 1–30; seed 0–2³²−1; window 2–252 |
| Strategy | `name` | `Trend rule` | 1–80 characters; strategy versions and the trial history are kept per name |
| | `code` | The trend template | 1–20,000 characters |
| | `parameters` | fast {10, 20, 30, 50}, slow {100, 150, 200} | At most 3 parameters, each named `^[a-z][a-z0-9_]{0,23}$`. Each has 1–12 distinct finite values within ±1,000,000. The grid is capped at 60 configurations. An empty list gives one configuration. |
| | `base` | fast 20, slow 150 | Must name grid parameters and use one of their values. A parameter left out takes its middle value, at index ⌊count/2⌋. Sending `parameters` without `base` gives every parameter its middle value; the `fast` 20 / `slow` 150 default applies only when neither is sent. |
| Costs | `capital` | 100,000 | 100 to 1e9 |
| | `commission_bps` | 5 | 0–500, per fill |
| | `slippage_bps` | 3 | 0–500, per fill |
| Validation | `split` | 0.7 | 0.5–0.9; the in-sample share of the train/test split |
| | `walk_forward` | `true` | |
| | `train_bars` | 252 | 126–5,040 |
| | `test_bars` | 126 | 63–2,520 |
| | `anchored` | `false` | Rolling or anchored training windows |
| | `permutations` | 200 | 0–500; random re-timings, where 0 switches the test off |
| | `seed_paths` | 5 | 0–10; alternative synthetic paths, where 0 switches them off |

The grid expands in row-major order: the last parameter varies fastest. Synthetic data uses the sandbox generators on a weekday calendar starting 2 January 2020, with 252 bars per year; a 3-year dataset has 756 bars. Historical data is the **first** `years × 252` bars of the imported Parquet file, ordered by time. It is not the most recent stretch.

Market data goes through one provider interface, so a strategy never knows where its bars came from:

- `MarketDataProvider` in `services/market_data.py` declares `kind`, `symbols()`, `describe(params)` and `bars(params)`.
- `SyntheticProvider` generates bars from their parameters.
- `ParquetProvider` reads imported files through DuckDB.

Imported history is never replaced with generated data.

## Execution and metrics

The backtester is long or cash.

- **Entries.** A buy commits all cash at the next open: `shares = cash / (open × (1 + slippage) × (1 + commission))`.
- **Exits.** A sell exits at `open × (1 − slippage)` less commission.
- **End of data.** The last position is marked to the final close and is not liquidated.
- **Full-history backtests** start in cash.
- **Buy-and-hold** starts invested at the first open and pays its entry costs.
- **Windows** cut from a longer history pass `prior_signal`, the signal from the close before the window. This is a keyword-only argument of `analytics.backtest`, and its default keeps the old behaviour. With it, the window's first open acts as the uncut backtest would have.

Metrics come from `analytics.summarize`, extended in `domain/research/metrics.py`.

**Return conventions.** Daily returns include the starting capital as the first point. There are 252 periods a year. Sharpe and Sortino are measured in excess of a 3% annual risk-free rate, which is `1.03^(1/252) − 1` per day. Undefined values are `null`.

| Metric | Definition |
| --- | --- |
| Total return, CAGR | Final equity against starting capital; CAGR over `bars / 252` years |
| Sharpe, Sortino | Annualized excess return over the standard deviation, or over the downside deviation |
| Maximum drawdown, Calmar | Largest fall from a running peak that includes the starting capital; CAGR divided by that drawdown |
| Volatility | Sample standard deviation of daily returns × √252 |
| Turnover | Notional traded (buys and sells) ÷ average equity ÷ years, in times per year |
| Win rate, profit factor | Over closed round trips |
| Exposure | Share of bars that hold a position, decided by the previous close's signal |
| Trades, round trips | Fills, and closed positions |

Each run compares four rows: the strategy, **Buy & hold (same asset)**, a **trend baseline (close > 200-day average)** built from the `sma_200` column, and **Cash at 3%**. Cash has a 3% CAGR, zero volatility and an undefined Sharpe, because Sharpe is already measured in excess of cash: cash is the zero line.

## Validation

Signals are computed once per configuration on the full history and then cut into windows. This is equivalent to re-running the strategy on each window only if the strategy is causal, which the look-ahead test checks. A run that fails it is marked invalid. Every window starts with fresh capital and acts at its first open on the signal from the close before it.

The *selection rule* is the same everywhere. The configuration with the highest in-sample Sharpe wins. An undefined Sharpe never wins, and ties go to the configuration that comes first in the grid.

### Train/test split

The cut is `round(n × split)`. The split needs at least 126 in-sample and 63 out-of-sample bars; otherwise it is skipped with a reason. Every configuration is evaluated in sample, and the selected configuration and the base configuration are then evaluated on the holdout. Both are reported with their in-sample and out-of-sample metrics and their decay. The default 70/30 split of 756 bars cuts at bar 529.

*Why:* an untouched holdout shows whether the configuration chosen on the past still works on later data.

### Walk-forward

- **Test windows.** The first test window starts at bar `train_bars`. The windows are consecutive and do not overlap. Each is `test_bars` long, except that the last may be shorter, but never shorter than 63 bars.
- **Training windows.** A rolling fold trains on the `train_bars` bars before its test window. An anchored fold trains on every bar from the start.
- **Fold count.** A run makes at most 40 folds. The test is skipped unless there are at least two, which needs `train_bars + test_bars + 63` bars.
- **Untested bars.** Bars after the fortieth fold are not tested, and neither is a final remainder shorter than 63 bars.
- **Default.** The defaults (252 training bars, 126 test bars, rolling) make four folds on 756 bars, with test windows starting at bars 252, 378, 504 and 630.

In each fold the selection rule picks a configuration on the training window, and that configuration is evaluated on the test window, with the base configuration beside it.

The **stitched out-of-sample account** is one continuous account across all the test windows, starting from fresh capital. On each bar its position comes from the configuration chosen for that bar's fold, evaluated at the previous close, when the choice was already known.

The aggregate reports:

- the mean training Sharpe of the chosen configurations;
- the stitched account's metrics and its equity curve;
- the base configuration evaluated continuously over the same span;
- the decay;
- the number of folds with a positive out-of-sample Sharpe;
- how many distinct configurations were chosen;
- `untested_tail_bars`: bars after the last full test window, fewer than 63, which no fold tests.

*Why:* repeating selection and testing through time makes a single lucky holdout less persuasive. The stitched account is what a researcher who re-selected on that schedule would have earned.

### Decay

```text
decay = 1 − out-of-sample Sharpe / in-sample Sharpe        (defined only when the in-sample Sharpe is positive)
```

A decay of 0 loses nothing, 0.5 loses half the Sharpe, and a value above 1 means the out-of-sample Sharpe was negative. A negative decay means it improved. Walk-forward decay compares the stitched account with the mean training Sharpe of the chosen configurations.

## Robustness

### Parameter surface and stability

Every configuration is backtested on the full history. The surface reports:

- each configuration's metrics;
- the best, median and worst configurations by Sharpe, where an undefined Sharpe ranks last;
- the base configuration's rank;
- the share of all configurations with a positive Sharpe;
- the minimum, median, maximum and standard deviation of the defined Sharpe ratios;
- for each parameter, the mean Sharpe at each of its values and the spread between the highest and lowest mean, with the largest spread first.

The **stability score** asks how much of a configuration's Sharpe its neighbours keep. A neighbour is a grid point one step away along exactly one parameter.

```text
kept(j) = clip(Sharpe(j) / Sharpe(centre), 0, 1)        an undefined neighbour Sharpe counts as 0
score   = round(100 × median over neighbours of kept(j))
class   = robust if score ≥ 70, sensitive if score ≥ 40, fragile otherwise
```

Two cases get no score:

- The class is `untested` when the grid has one configuration.
- The class is `no-edge` when the centre's Sharpe is undefined or not positive.

The clip has two effects. A better neighbour cannot make the centre more robust than a plateau would, and a losing neighbour counts as keeping nothing. The score is computed for the base configuration, which the red team uses, and for the best configuration.

*Why:* an edge on a sharp peak of the grid is more likely to be fitted noise than an edge on a plateau.

### Transaction-cost stress

The base configuration is backtested at one-way costs of 0, 2, 5, 10, 15, 20, 30, 40, 50, 75 and 100 bps per fill. Each level sets commission plus slippage to that total, split in the proportion the experiment configured, or in equal halves when both are zero. Every level reports Sharpe, CAGR, total return and final equity.

The **break-even cost** is the one-way cost at which Sharpe reaches zero. Because Sharpe is measured in excess of the 3% rate, this is where the rule stops beating cash.

- **Method.** It is found by 24 bisection steps between 0 and 1,000 bps and rounded to 0.01 bps.
- **Margin.** It is reported with its margin, the break-even cost divided by the assumed cost. The default assumed cost is 5 + 3 = 8 bps.
- **No break-even.** There is none when the rule never trades or has no positive Sharpe even at zero cost. If Sharpe is still positive at 1,000 bps, the result is `break_even_above: 1000` instead.

*Why:* many edges vanish under realistic friction. The break-even cost says how much friction the claim can bear.

### Alternative market paths

This test applies to synthetic data only. The base configuration runs on `seed_paths` other draws of the same generator, with seeds `(seed + k) mod 2³²` for `k = 1 … seed_paths`. The default seed 42 gives paths 43 to 47. On each path the strategy's Sharpe is compared with buy-and-hold's.

The test reports:

- the share of paths where the strategy's Sharpe is higher, where an undefined Sharpe counts as −∞;
- whether the original path beat buy-and-hold;
- the mean and standard deviation of the strategy's Sharpe across paths;
- the share of paths with a positive Sharpe;
- the original Sharpe's z-score against the paths.

Historical data has a single path, so the test is skipped and walk-forward carries the evidence.

*Why:* a rule that only works on one seed is describing that seed, not the market model.

## Diagnostics

### Deflated Sharpe ratio

The method follows Bailey & López de Prado (2014), "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality", *Journal of Portfolio Management* 40(5).

```text
SR   = (mean(r) − rf) / sd(r)            daily Sharpe of the reported (base) configuration; sd is the sample deviation
V    = sample variance of the daily Sharpe ratios of the run's configurations (undefined ones left out)
SR0  = √V · [ (1 − γ) · Φ⁻¹(1 − 1/N) + γ · Φ⁻¹(1 − 1/(N·e)) ]          γ = 0.5772156649… (Euler–Mascheroni)
z(k) = (SR − k) · √(T − 1) / √(1 − g3·SR + (g4 − 1)/4 · SR²)
DSR  = Φ(z(SR0))                         PSR = Φ(z(0))
```

The symbols are:

- `N` is every configuration tried for this strategy: this run's grid plus the frozen prior-trial count from earlier completed runs of the same strategy name. Undefined ones count toward `N` but not toward `V`.
- `V` comes from this run's grid only, because earlier runs' Sharpe ratios are not kept per configuration; it stands in for the spread of every trial.
- `T` is the number of daily returns.
- `g3` and `g4` are the skewness and the kurtosis (not excess, so a normal distribution has 3) of the reported strategy's daily returns, as population moments.
- `Φ` is the standard normal distribution function.

Conventions:

- **Units.** All quantities are daily. The reported `sharpe`, `expected_max_sharpe` and `trial_sharpe_std` are multiplied by √252 for display.
- **Edge cases.** `SR0` is 0 when `N < 2` or `V` is 0, and DSR then equals PSR. The DSR is undefined when the returns do not vary, when `T < 3`, or when the term under the square root is not positive.

Iterating on a strategy therefore raises the bar: each earlier run's configurations increase `N` and the expected best Sharpe from luck (see [Trial history](#trial-history)).

*Why:* the best of many tries looks good by chance. DSR is the probability that the true Sharpe exceeds what the luckiest of `N` skill-less tries would show, allowing for skewed and fat-tailed returns.

### Probability of backtest overfitting

This uses combinatorially symmetric cross-validation (CSCV), following Bailey, Borwein, López de Prado & Zhu (2017), "The Probability of Backtest Overfitting", *Journal of Computational Finance* 20(4).

```text
R       T × N matrix of daily returns minus rf, one column per configuration, on the full history
S       16 blocks if T ≥ 336, 12 if T ≥ 252, 8 if T ≥ 168; rows cut into S contiguous, near-equal blocks
for each of the C(S, S/2) choices of S/2 blocks as in-sample (the other half is out-of-sample):
    n*  = configuration with the highest in-sample Sharpe (first on ties; a zero-variance column ranks last)
    r   = (configurations with a lower out-of-sample Sharpe than n*)
          + ((configurations with an equal one, n* included) + 1) / 2
    ω   = r / (N + 1)
    λ   = ln(ω / (1 − ω))
PBO     = share of splits with λ ≤ 0, that is, where the in-sample winner ranks at or below the out-of-sample median
```

- **Sharpe in a split.** Within a split, Sharpe is the mean over the sample standard deviation of the pooled daily excess returns.
- **Block choice.** The block count keeps every block at least a month (21 observations) long. 16 blocks give 12,870 splits, 12 give 924, and 8 give 70.
- **When it is skipped.** The test needs at least four configurations and 168 observations.
- **Other outputs.** It also reports the median logit, the share of splits where the winner's out-of-sample Sharpe is below the risk-free rate, and the annualized median in-sample and out-of-sample Sharpe of the winners.

*Why:* PBO estimates how often picking the best configuration of the grid picks one that is below median on data it has not seen.

### Random-timing test

```text
K       = min(permutations, T − 1) distinct shifts s, drawn without replacement from 1 … T − 1
null(s) = Sharpe of the base signal series rotated circularly by s bars, backtested with the same costs
p       = (1 + number of shifts with null(s) ≥ actual Sharpe) / (1 + K)
```

A circular shift keeps the rule's exposure and its holding periods, apart from the wrap-around point, but removes its timing.

- **Seed.** The draw is seeded with the first 32 bits of the SHA-256 of the canonical experiment specification, which the run records as `seeds.random_timing`. The same specification therefore draws the same shifts.
- **Other outputs.** The test also reports the percentile of the actual Sharpe, the median of the null distribution, and its 5th and 95th percentiles.
- **When it is skipped.** It is skipped when `permutations` is 0, when the rule is always invested or always in cash, or when its Sharpe is undefined.

*Why:* a rule invested 60% of the time earns the market's drift 60% of the time whatever its timing. The test separates timing skill from exposure.

### Profit concentration

The equity curve is split into calendar years, and the first year starts from the starting capital. The test reports the best year's share of net profit and the number of losing years. It needs at least three calendar years and a net profit.

*Why:* a profit made in one year reflects one regime, not a repeatable pattern.

### Look-ahead truncation test

The cut points are the distinct values of `⌊n/3⌋`, `⌊n/2⌋` and `⌊3n/4⌋` that are at least 2; for 756 bars they are 252, 378 and 567.

1. For each cut `k`, the base configuration runs again on the first `k` bars. Every data column, including `sma_50`, `sma_200` and `returns`, is recomputed from those bars alone.
2. A causal rule must reproduce its first `k` signals exactly.
3. If any signal differs, the test fails and reports the first date that changed. An error on the shorter history also fails the test, because a rule that cannot run on a shorter history cannot be shown to be causal.

A failure has several effects:

- It marks the run's results invalid (`valid: false`).
- It makes the red team's look-ahead check fail, so the research risk is HIGH.
- It scores 0 for the bias component of research quality.
- It puts a warning above the research note's results.

For example, a rule that returns `data["close"] > np.mean(data["close"])` (after `import numpy as np`) fails, because the full-sample mean changes when later bars are removed.

The test has limits:

- It checks the base configuration only, at three points.
- A dependence on later bars that changes no Boolean signal before those points goes unnoticed.
- It cannot detect choices a researcher made after seeing the data. The hypothesis lock, the deflated Sharpe ratio and PBO address that.

*Why:* a rule that sees the future produces results that could never have been traded.

### Data integrity

Seven checks run on the bars the run used.

| Check | Rule | Status on failure |
| --- | --- | --- |
| `duplicates` | No duplicate timestamps | warn |
| `ordering` | No timestamp earlier than the one before it (a repeat counts only as a duplicate) | warn |
| `prices` | No zero or negative open, high, low or close | warn |
| `ohlc` | Low ≤ min(open, close) and high ≥ max(open, close) | warn |
| `volume` | Volume above zero on every bar | warn |
| `gaps` | No calendar gap over five days between consecutive bars | warn |
| `extreme` | No close-to-close move beyond ±25% (check splits and data errors) | info |

Each warning counts as an integrity issue; `info` does not. The dataset version stores the same checks, computed on the full imported file or the generated bars.

*Why:* bad bars create trades that never happened.

## Research red team

`domain/research/redteam.py` always produces twelve checks, in a fixed order. Each check has:

- a status: `pass`, `warn`, `fail` or `skip`;
- a severity, `medium` or `high`, on warnings only;
- a plain-language finding with its evidence;
- the id of the lesson that teaches the idea. Lessons open at `/learn/<id>`.

| Check | Passes when | Warns when (severity) | Fails or is skipped when | Lesson |
| --- | --- | --- | --- | --- |
| `lookahead` | Every truncated rerun reproduces its earlier signals | — | **Fails** on any changed signal or an error on a shorter history (no severity) | 2.27 Backtesting and simulation without hindsight |
| `oos` | Walk-forward completed with a stitched out-of-sample Sharpe above 0 and a decay of at most 0.5 (or undefined) | Out-of-sample Sharpe ≤ 0 or undefined: **high** if the mean in-sample Sharpe is positive, otherwise medium. Decay above 0.5: medium. No holdout possible at all: **high** ("Not validated out of sample") | — | 4.22 Walk-forward model selection and nested validation |
| `split` (replaces `oos` when walk-forward is off or skipped but the split ran) | The best in-sample configuration has a holdout Sharpe above 0 | Otherwise: medium | — | 4.29 Chronological validation and untouched evaluation |
| `multiple_testing` | DSR ≥ 0.95 | DSR < 0.95: **high** if DSR < 0.5, otherwise medium | Skipped when DSR is undefined | 4.30 Multiple testing, uncertainty and honest inference |
| `overfitting` | PBO ≤ 0.2 | PBO > 0.2: **high** if PBO ≥ 0.5, otherwise medium | Skipped with fewer than 4 configurations or 168 observations | 4.30 |
| `parameters` | Stability class `robust` (score ≥ 70) | `sensitive` (40–69): medium; `fragile` (below 40): **high**; `untested` (one configuration): medium | Skipped when `no-edge` (base Sharpe ≤ 0 or undefined) | 14.8 Robustness in the sandbox: costs, seeds and scenarios |
| `costs` | Break-even ≥ max(2 × assumed cost, 10 bps), or Sharpe still positive at 1,000 bps | Break-even ≤ assumed cost: **high**; break-even < max(2 × assumed, 10 bps): medium | Skipped when the rule never trades or has no positive Sharpe at zero cost | 14.8 |
| `sample` | At least 30 closed round trips and at least 3 years (`bars / 252`) | Otherwise: **high** with fewer than 10 round trips, otherwise medium | — | 10.10 Selection bias and uncertainty around a chosen algorithm |
| `concentration` | The best year contributes at most 50% of net profit | Above 50%: **high** above 80%, otherwise medium | Skipped with fewer than 3 calendar years or no net profit | 12.10 Honest backtests: search, selection and reporting |
| `benchmark` | Sharpe above 0 (beats cash) and strictly above the buy-and-hold and trend-baseline Sharpe ratios; an undefined baseline counts as beaten | Any baseline not beaten (a tie is not beaten): **high** if cash is not beaten, otherwise medium | — | 4.6 Benchmarks, null models and controlled comparisons |
| `timing` | Random-timing p ≤ 0.05 | p > 0.05: **high** if p > 0.5, otherwise medium | Skipped when switched off, when the signal never changes, or when Sharpe is undefined | 4.6 |
| `seeds` | Beats buy-and-hold on at least 60% of the alternative paths, with a positive mean Sharpe | Otherwise: **high** if it beat buy-and-hold on the original path but on fewer than 40% of the others, otherwise medium | Skipped for historical data or when `seed_paths` is 0 | 14.8 |
| `data` | No data-integrity warning | Any warning: medium | — | 12.11 The data you are allowed to use |

When walk-forward completed, the red team judges out-of-sample evidence by walk-forward alone. The train/test split is still reported, but no check reads it.

### Research risk

The checks add up to one level:

- **HIGH** when any check fails, when at least two warnings are high severity, or when there are at least five warnings;
- **MEDIUM** when there is at least one warning;
- **LOW** otherwise.

Skipped checks do not count. The summary also reports the number of checks that passed, warned, were high severity, failed and were skipped.

### Research quality

The research-quality score, 0 to 100, grades the process: how thoroughly the claim was tested and recorded. It does not grade the result, so a carefully documented losing strategy can score well. In the note's own words: *Research quality is not investment quality. This note describes a simulated, educational experiment; it is not investment advice.*

| Component | Weight | Score |
| --- | --- | --- |
| Reproducibility | 15 | 100 if a rerun of the current run was identical, 85 if equivalent, otherwise 50 (a `different` rerun scores the same as no rerun) |
| Out-of-sample validation | 20 | 100 with walk-forward over at least 3 folds, 80 with 2 folds, 50 with the holdout split only, 0 with neither |
| Cost testing | 10 | 100 when the cost levels were computed, which every completed run does |
| Robustness | 15 | 100 with at least 9 configurations, 60 with at least 3, 30 with 2, 0 with 1; plus 20 (capped at 100) when the alternative-path test completed |
| Bias controls | 15 | 100 if the look-ahead test passed, otherwise 0; minus 20 per data-integrity issue, at most 40 |
| Sample size | 10 | `50 × (min(1, round trips / 30) + min(1, years / 5))` |
| Documentation | 15 | Hypothesis 40 (always present) + conclusion 30 + limitations 20 + decision 10 |

Each component is clipped to 0–100 and rounded. The score is the weighted mean, rounded. It is computed whenever the experiment is read, from the current run, the current write-up and the latest rerun of the current run, so it is not frozen with a run.

**Example.** Measured on this checkout (macOS arm64, Python 3.14.4, NumPy 2.5.3), the default experiment is the trend template on the default synthetic market (seed 42, three years). It reports **HIGH** research risk: 2 checks pass, 7 warn (5 of them high), and 3 are skipped. Its walk-forward stitched Sharpe is −0.46. With only its hypothesis written, it scores 78 for research quality, because the process was thorough even though the strategy is not worth trading.

## Lifecycle

The *current run* is the experiment's most recent completed run of kind `run`. Reruns never become current, and a later run that fails does not replace it. The experiment's status follows from its runs and its write-up. The first matching row applies.

| Status | When |
| --- | --- |
| `RUNNING` | A run or rerun is queued or running |
| `CONFIGURED` | There is no run yet |
| `FAILED` | There is no current run, and the latest run failed or was interrupted |
| `REPRODUCIBLE` | Documented, and a completed rerun of the current run was identical or equivalent |
| `DOCUMENTED` | Conclusion, limitations and decision are all recorded for an experiment with a current run |
| `PASSED` | The current run's research risk is LOW |
| `WARNINGS` | The current run's research risk is MEDIUM or HIGH |

The experiment's lifecycle also lists five steps, each done or not: **Hypothesis registered**, **Backtested**, **Red-teamed**, **Documented** and **Reproduced**. A run's own status is `queued`, `running`, `completed`, `failed` or `interrupted`. Its stage is one of:

- `queued`, then `data`;
- the pipeline stages `strategies`, `validation`, `robustness`, `diagnostics` and `red team`;
- finally `completed` or `failed`.

Once a run has completed, the hypothesis is locked: `PATCH` with a different hypothesis returns 409. The title and the specification stay editable. `spec_changed` is true when the experiment's current specification differs from the one its current run used. Starting a run uses the current specification; a rerun uses the frozen one.

## Provenance and reproduction

### Fingerprints

Each run records SHA-256 digests. A digest of a structure is taken over canonical JSON: sorted keys, compact separators, UTF-8, and NaN or infinity refused.

| Field | Covers |
| --- | --- |
| `dataset.sha256` | The exact bars the run used (time and OHLCV), after the years limit |
| `dataset.version_sha256` | The dataset version's content. For synthetic data this is the same bars digest. For an import it is the bytes of the whole Parquet file. |
| `strategy.sha256` | The strategy source text (UTF-8), the same digest as its strategy version |
| `config_sha256` | The dataset kind and parameters, the grid and base, costs and validation settings. It excludes the strategy name and code, which `strategy.sha256` covers. |
| `engine.sha256` | Twelve source files, read in this order: `domain/analytics.py`, `domain/research/{__init__, diagnostics, metrics, pipeline, redteam, robustness, spec, validation}.py`, `execution/native_worker.py`, `execution/runner.py`, `execution/sandbox_worker.py`. Each file is hashed as its path, then its bytes, each followed by a NUL. |
| `environment.sha256` | The Python version and implementation, the NumPy version, and the operating system and machine |
| `result_sha256` | The whole results document |

The engine and environment digests are computed once, when the API process loads the research modules, so they describe the code that produced the result. The provenance also records:

- the engine name and version (`quanta-research` 1.0.0);
- the API version (`quanta.__version__`, currently 0.1.0);
- the sandbox runtime (`QUANTA_SANDBOX`: `guided` unless set to `docker`);
- the seeds: the dataset seed, the random-timing seed and the alternative-path seeds;
- the configuration count;
- the dataset key, label, source, version, bar count and date range;
- the strategy version reference.

The **git commit** comes from `QUANTA_GIT_COMMIT` when that variable is set, cut to 64 characters. Otherwise the API runs `git rev-parse HEAD` in the checkout (with a 2-second timeout) when a `.git` directory exists. When neither works, the note shows "not recorded". The Docker build context excludes `.git`, so a Compose deployment records a commit only when `QUANTA_GIT_COMMIT` is set in the shell or `.env` that runs Compose.

### Versions

A **strategy version** is content-addressed per owner and strategy name. Queuing a run with new source text registers the next version number (1, 2, …). Running the same text again, in any experiment, reuses its version, and editing code without running it creates no version.

A **dataset version** is content-addressed per dataset key:

- `synthetic:<first 16 hex characters of the settings digest>` for generated data. The settings exclude `symbol` and `window`.
- `historical:<SYMBOL>` for an import.

A new version is registered only when the same key's content changes. For an import, that means the Parquet file's bytes. The version stores the dataset's label, source, settings, bar count, date range, retrieval time (the file's modification time for imports) and integrity checks. Dataset versions are global, not owned. The options endpoint lists every registered version of each import.

### Trial history

When a run is queued, the platform counts the **distinct configurations** the owner tried in earlier **completed runs of the same strategy name**, across all experiments, leaving out the ones this run repeats. This count is the run's *prior trials*. A configuration is identified by the strategy source's SHA-256, the dataset specification (kind and generator or import settings) and its parameter values, so:

- running an unchanged specification again adds no trials, and its result digest matches the earlier run's;
- a code change, a new parameter value or different data adds the configurations it introduces;
- restoring earlier code or settings adds nothing for the configurations already tried;
- costs and validation settings are not part of a configuration's identity;
- reruns, failed runs and interrupted runs do not count;
- renaming the strategy starts a new count;
- deleting an experiment deletes its runs, so they stop counting.

The run reports `trials.run`, its own grid size, and `trials.strategy_configurations`, which is prior trials plus the run's own grid. The deflated Sharpe ratio uses `trials.strategy_configurations` as `N`, and the multiple-testing finding splits it into this run and earlier runs.

The count is history, not specification, so it is frozen with the run (`spec.prior_trials`, also recorded as `provenance.prior_trials` and compared as the input "Earlier trials counted"), and a rerun copies the original's count instead of recounting. The count appears in the results, and so in `result_sha256`. If it were recounted, every run completed in between would change the rerun's output, and a reproduction would be judged different for reasons that have nothing to do with the computation.

### Rerun verdicts

`POST /runs/{run_id}/rerun` re-executes the frozen specification of a completed run. A rerun of a rerun resolves to its original. When it completes, the rerun is compared with the original.

The comparison lists seven inputs, each marked the same or different:

- the dataset digest;
- the strategy digest;
- the configuration digest;
- the engine digest;
- the environment digest;
- the sandbox runtime;
- the frozen count of earlier trials (a rerun copies it, so it differs only for runs stored before it was recorded).

The git commit and API version are recorded but not compared.

| Verdict | Rule |
| --- | --- |
| `identical` | The two `result_sha256` digests are equal |
| `equivalent` | The digests differ, at least one headline metric differs, both values of every differing metric are numbers, and the largest relative difference, `abs(a − b) / max(abs(a), abs(b), 1e-12)`, is at most 1e-9 |
| `different` | Anything else. This includes a metric that is defined on one side and undefined (`null`) on the other, and outputs that differ only outside the headline metrics, which give an empty list of metric differences. |

The comparison returns up to 20 metric differences and names the inputs that changed, which is usually the explanation for a `different` verdict.

## Research note

`GET /experiments/{experiment_id}/report?format=markdown|html` exports the experiment with its current run. It returns 409 until a run has completed. The note's sections, in order, are:

1. Hypothesis, with its registration date.
2. Method: dataset and version, strategy and version with its base configuration, grid, execution and costs, validation settings, and stress settings.
3. Results: the four-row comparison table, under a warning when the look-ahead test failed.
4. Out-of-sample validation.
5. Robustness.
6. Research red team, with the overall research risk.
7. Conclusion and decision.
8. Limitations: the learner's own text, then every warning and failure finding, then a caveat about the data source.
9. Provenance: a fingerprint table.

The Markdown note also tabulates the holdout split, the grid summary and the break-even cost, and it ends with the rerun verdict when a rerun exists.

The HTML page is standalone:

- It contains no script, no external request, and inline styles only.
- It draws two SVG charts: the strategy's equity against buy-and-hold, and Sharpe by one-way cost.
- It has print styles, so the browser's print dialog saves it as a PDF.

Both formats end with the disclaimer quoted under [Research quality](#research-quality). The files are named `quanta-experiment-<number>.md` and `.html`.

## Data model

Four SQLModel tables are created by the normal startup initialization, alongside the existing tables. Timestamps are ISO-8601 UTC strings.

| Table | Fields | Notes |
| --- | --- | --- |
| `ResearchExperiment` | `id`, `owner`, `number`, `title`, `hypothesis`, `hypothesis_registered_at`, `spec` (JSON), `notebook` (JSON: conclusion, limitations, decision), `created_at`, `updated_at` | Numbered per owner; at most 200 per owner |
| `ResearchRun` | `id`, `experiment_id` (foreign key), `owner`, `number`, `kind` (`run` or `rerun`), `rerun_of`, `status`, `stage`, `progress` (JSON), `spec` (JSON: the frozen specification, `prior_trials` and the strategy version reference), `provenance` (JSON), `results` (JSON), `summary` (JSON), `reproduction` (JSON, reruns only), `error`, `created_at`, `started_at`, `finished_at`, `heartbeat_at` (Unix seconds), `duration_ms` | Numbered per experiment. List queries skip `results`. |
| `StrategyVersion` | `id`, `owner`, `name`, `version`, `sha256`, `code`, `created_at` | Unique on (owner, name, sha256) |
| `DatasetVersion` | `id`, `key`, `version`, `sha256`, `kind`, `meta` (JSON), `quality` (JSON), `created_at` | Unique on (key, sha256); global |

Deleting an experiment deletes its runs. Strategy and dataset versions remain.

## HTTP API

All paths start with `/api/v1/research`. Interactive schemas are at `/docs` on the API.

**Ownership.** Experiments and runs belong to the signed-in account or, for a guest, to the signed `quanta_trading_guest` cookie the simulator already uses. The cookie is issued when absent and is valid for 30 days. An experiment or run that belongs to someone else returns 404.

**Rate limit.** Requests that start work share the `research` budget of 6 per 60 seconds. The budget is keyed by account, or by client IP for guests, and an exceeded budget returns 429 with `Retry-After: 60`. With Redis configured, an unavailable limiter returns 503. The work-starting requests are creating an experiment with `run: true`, starting a run, and rerunning.

| Method | Path | Success | Purpose and errors |
| --- | --- | --- | --- |
| GET | `/options` | 200 | Default specification, limits, synthetic models and scenarios, imported symbols with their dataset versions, the helper list and the templates |
| GET | `/experiments` | 200 | The owner's experiments, most recently updated first, with status, research risk, five metrics and run count |
| POST | `/experiments` | 201 | Register `{title, hypothesis, spec, run}`. `run` defaults to `true`, which queues the first run. Returns 409 at 200 experiments; with `run: true`, also 409 while another run is active, 503 when the queue is full, and 429. A refused request registers nothing. |
| GET | `/experiments/{experiment_id}` | 200 | Detail: specification, write-up, lifecycle, research quality, strategy versions, runs, the active run, the full current run and the reproduction |
| PATCH | `/experiments/{experiment_id}` | 200 | Update `title`, `hypothesis`, `spec` and `notebook` (`conclusion` and `limitations` up to 8,000 characters; `decision` is `trust`, `reject`, `inconclusive` or empty). Returns 409 when changing a locked hypothesis |
| DELETE | `/experiments/{experiment_id}` | 200 | Delete the experiment and its runs. Returns 409 while a run is queued or running |
| POST | `/experiments/{experiment_id}/runs` | 202 | Queue a run of the current specification. Returns 409 with an active run, 503 when the queue is full, and 429 |
| GET | `/runs/{run_id}` | 200 | One run with its frozen specification, provenance and results |
| POST | `/runs/{run_id}/rerun` | 202 | Reproduce a completed run. Returns 409 when it has not completed or another run is active, 503 when the queue is full, and 429 |
| GET | `/experiments/{experiment_id}/report?format=markdown` or `html` | 200 | Download the research note. Returns 409 before the first completed run |

Invalid bodies return 422. The existing request guards still apply to writes: an unlisted `Origin` returns 403, and a body over 1,500,000 bytes returns 413. Every response under `/api/v1/research` carries `Cache-Control: no-store`.

A report is sent as an attachment, with `Content-Type: text/markdown; charset=utf-8` or `text/html; charset=utf-8`. It carries `Content-Security-Policy: default-src 'none'; style-src 'unsafe-inline'; img-src data:`.

## Operations

| Setting | Value |
| --- | --- |
| Runs executing at once | 2 per API process (the `quanta-research` thread pool) |
| Sandbox threads | `QUANTA_RESEARCH_WORKERS`, which defaults to the smaller of 4 and the CPU count (2 if the CPU count is unknown), with a minimum of 1. Compose sets 2. The threads are shared by every run in the process. |
| Queue cap | 8 runs queued or running per process; the next request gets 503 "The research queue is full. Try again in a minute." |
| Active runs per owner | 1; another start gets 409 |
| Stale running run | No heartbeat for 90 seconds: reported `interrupted` |
| Stale queued run | Queued for 600 seconds: reported `interrupted` |

Each strategy job is one sandbox subprocess under the same limits as the Strategy lab. A guided job has a 2-second process deadline, and an optional Docker job has a 15-second outer limit. A run makes one job per configuration, cut point and alternative path, 20 jobs with the defaults.

**Heartbeats and interrupted runs.** Status, stage, progress and a heartbeat are stored in the database, so any request can follow a run.

- **When heartbeats are written.** Progress writes refresh the heartbeat as each sandbox job finishes, at most once every 0.4 seconds within a stage, and at every stage change.
- **How staleness is applied.** It is applied lazily: any request that reads runs (listing, opening an experiment or a run, starting a run) marks stale runs `interrupted`, with the message "The server stopped before this run finished. Start it again." That is how a restart shows up, including a development `--reload`.
- **The risk on a slow host.** The validation, robustness and diagnostics stages write no intermediate progress. So a stage that computes for more than 90 seconds on a slow or overloaded host is reported interrupted while its worker continues. The worker then discards its result instead of overwriting the `interrupted` status, because the owner may already have started another run; start the run again.

**Logging.** Each run writes one JSON line to standard error through the `quanta.research` logger, which does not propagate to the root logger. Its fields are:

- `event` (`research_run`), `run_id`, `experiment_id`, `kind`;
- `strategy_version` and `dataset_version` (`key@vN`);
- `status`, which is `completed`; `failed` for a strategy, validation or arithmetic error, whose message is stored; or `error` for an unexpected exception, whose traceback is logged while the run stores a generic message;
- `risk`, `configurations`, `engine_version`, `result_sha256`, `verdict`, `error`, `duration_ms` and `workers`.

**Single-process assumption.** The run queue, the pending-run counter and the locks around run admission and version numbering live in the API process. Compose runs one uvicorn process. Several API processes would each keep their own queue and cap, and could admit two active runs for one owner at the same moment. Staleness still works across processes, because heartbeats are in the database, and version numbers stay unique because the tables also constrain `(owner, name, version)` and `(key, version)`: a process that loses the race retries with the next number.

## Security

- **Isolation.** Strategy code runs only in the configured sandbox, never in the API process. That is the guided interpreter in a fresh `python -I` subprocess, or the optional Docker worker; see the [README](../README.md#python-execution) for their limits. Each configuration, cut point and alternative path is a separate job. Code is limited to 20,000 characters.
- **Ownership.** Every experiment and run query is filtered by owner, and another owner's identifiers return 404. Guest experiments stay with the guest cookie and are not carried into an account on sign-in.
- **Load.** The `research` rate limit, the per-owner active-run rule, the process queue cap and the 200-experiment limit bound the work one client can start.
- **Headers.** Research responses carry `Cache-Control: no-store`, in addition to the `X-Content-Type-Options: nosniff` and `Referrer-Policy: same-origin` headers on every API response.
- **HTML export.** Every learner-entered string, and every finding, label and fingerprint, is escaped with `html.escape`, including the title, hypothesis and write-up. Only server-generated numbers and fixed status values, such as the risk level, are inserted unescaped. The page has no script and makes no network request. Its Content-Security-Policy protects the response when a browser renders it; a downloaded file opened later does not carry the header.
- **Markdown export.** The Markdown note inserts the title, hypothesis, conclusion and limitations as written, without escaping. Open it in a viewer that does not run embedded HTML.
- **Errors.** Error messages from the learner's own code are shown to the learner. Unexpected failures store a generic message, and the traceback goes only to the server log.

## PRD mapping

The Quanta Research Platform PRD is a separate document from [PRD.md](../PRD.md) and is not in this repository. The table maps the items of its MVP scope (§19), as given for this implementation, to the code. Paths are relative to `backend/quanta/` unless they start with `frontend/`.

| MVP item | Implemented in |
| --- | --- |
| Reproducible experiments with provenance | `services/experiments.py` (experiments, runs, ownership, queue, lifecycle); `domain/research/provenance.py`; `ResearchExperiment` and `ResearchRun` |
| Dataset versions | `DatasetVersion`; `services/experiments.py::_dataset_version`; `services/market_data.py` (provider interface, cited in code as PRD 8.4) |
| Strategy versions | `StrategyVersion`; `services/experiments.py::_strategy_version` |
| Rerun and reproduce | `POST /runs/{run_id}/rerun`; `provenance.compare`; frozen prior-trial count |
| Train/test split | `domain/research/validation.py::train_test` |
| Walk-forward validation | `validation.folds` and `validation.walk_forward`, rolling or anchored, with a stitched out-of-sample account |
| Benchmark comparison | Benchmark rows in `domain/research/pipeline.py`; comparison metrics in `metrics.HEADLINE` (cited in code as PRD 8.5); the `benchmark` red-team check |
| Parameter sweeps | Grid and limits in `domain/research/spec.py`; `robustness.surface` and `robustness.stability` |
| Transaction-cost stress | `robustness.cost_stress` |
| Overfitting diagnostics | `diagnostics.deflated_sharpe`, `diagnostics.probability_of_overfitting`, `diagnostics.random_timing`, `diagnostics.concentration`; `robustness.seed_dispersion` |
| Look-ahead check | `diagnostics.cut_points` and `diagnostics.lookahead`; causal helpers and the refusal of negative `shift` in `execution/sandbox_worker.py` and `execution/native_worker.py` |
| Research Red Team | `domain/research/redteam.py::checks` and `risk` |
| Research-quality score | `redteam.quality` |
| Structured research note with Markdown/HTML export | `domain/research/report.py`; `GET /experiments/{experiment_id}/report` |
| Registry interface | Routes in `frontend/src/app/App.tsx`; pages in `frontend/src/features/research/pages/`; contract in `frontend/src/features/research/model/registry.ts` |

### Not implemented

These Phase 2 and Phase 3 items are outside this release:

- **Point-in-time universes.** An experiment uses one symbol's bars. There are no historical constituent lists and no availability timestamps.
- **Corporate actions and survivorship protection.** Imported prices are used as supplied, with no split or dividend audit and no delisted securities. The ±25% integrity flag is only a hint.
- **Counterfactual replay.** It is not implemented. The nearest tool is the alternative-path test on synthetic data.
- **Behavioural trading analytics.** The registry does not analyse a learner's own trading, for example simulator journals.
- **Research copilot.** No AI assistant is connected to the registry. The course assistant is separate.
- **Richer event-driven strategy API.** Strategies remain vectorized long/cash signal functions, with no order callbacks, sizing, shorts or intrabar events.
- **PDF beyond browser print.** The HTML note prints to PDF in the browser. The server generates no PDF.
- **Normalized metric and trade tables.** Results are one JSON document per run, with at most 1,000 trades kept.
- **Distributed queue.** Runs use in-process thread pools, with no external broker or worker fleet.
- **Guest-to-account migration.** Guest experiments are not copied into an account on registration or sign-in.
- **Multi-asset portfolios.** One asset per experiment.
- **Paper and live trading.** A research result is not connected to the simulator, a broker or live orders.
