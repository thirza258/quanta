# Strategy Lab expansion

`/curriculum/strategy-lab` now contains 32 original lessons across eight units,
budgeting 16 hours of guided reading, calculations and assignments. Each lesson
has a worked example, equation, runnable Python worksheet, two practice questions,
a research task, worked solution and named primary references. Exam time is additional.

| Unit | Coverage |
| --- | --- |
| Research specification | Falsifiable mechanisms, benchmarks, event clock and experiment manifests |
| Trustworthy data | Available filings and revisions, historical universes, corporate actions, cleaning and label overlap |
| Value and quality | NCAV haircuts, quality composites, catalysts, exclusions and fundamental portfolios |
| Trend and reversal | Time-series trend, cross-sectional momentum/skip periods, bid–ask bounce and rebalance buffers |
| Relative value | Hedge units, cointegration, half-life, borrow, two-leg failures and relationship breaks |
| ML signals | Baselines, fitted preprocessing, nested chronological selection, IC and ablations |
| Implementation | Sizing, covariance, exposure caps, turnover, liquidity and cash accounting |
| Validation and capstone | Frozen selection, uncertainty, multiple testing, adverse assumptions and reporting handoff |

Eight four-question checkpoints require 75% (3/4). The 32-question final requires
80% (26/32). Its version increases from 1 to 2; historical attempts remain visible
but do not satisfy the expanded final. Original lessons `4.1`–`4.4` retain their
subjects, URLs and first practice question/answer keys. New modules use `4.5`–`4.32`
and the curriculum orders them by teaching unit rather than numeric suffix.

The [source project](../content/projects/strategy-lab/README.md) is a real offline,
standard-library Python lab. It runs equal-weight, value-quality and momentum
portfolios on an original 90-session three-stock fixture. Available filings,
next-open fills, per-side fees, whole shares, prior-volume caps, cash constraints,
deterministic allocation and reconcilable holdings are explicit. Validation chooses
one candidate before its later synthetic test; cost and liquidity stresses preserve
the selected rule. Archives include eleven independent engineering tests.

Outputs include signals, trades, positions, aligned valuations, metrics, source/data
hashes and all validation/stress results. The final reporting course accepts the
selected `test/equity.csv` and `test/manifest.json` directly. Segment accounts reset
to cash; this is not a continuous walk-forward portfolio. The benchmark index is
frictionless and separately labeled from the executable equal-weight candidate.

The written dossier has its own 100-point self-assessed rubric. Pairs/borrow engines,
fitted ML, corporate actions, external market adapters, impact and live execution
are explicit extensions; their full implementation is not inferred from lesson
coverage. Browser worksheets remain in cash and calculate the lesson cases.
