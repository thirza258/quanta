# Performance and correctness notebook

## Reproduction manifest

Date, commit/source hash, compiler/version, flags, CPU, core count, OS, memory, power mode, background load, workload size, seed, parameter list, worker count. Record exact commands and standard output. Never include API keys.

## Before optimization

Write the contract: next-open fills, one-share long/cash target, five-cent fee, integer-cent ledger, final mark, warmup, failure publication. Hand-calculate the four-bar fixture: equity 999950 cents, two fills. Save `make test` and `make sanitize` output.

## Hypothesis

Which measured cost dominates? What change should reduce it? What will remain constant? Which result equality or numerical tolerance is required and why? Which boundary case could invalidate the change?

## Measurement table

| Bars | Workers | Build flags | Five serial times | Five candidate times | Median speedup | Equality | Notes |
|---|---|---|---|---|---|---|---|
| 2,000 | 1/2/4 | | | | | | |
| 200,000 | 1/2/4 | | | | | | |

The project prints five repetitions. Use the middle sorted observation as the median; report min/max too. A percentile from five observations is not a stable p99 estimate. Include thread setup cost consistently. A faster backtest does not validate a trading rule.

## Robustness and operational design

Run multiple seeds and windows including 1 and the full data length. Check zero and out-of-range arguments, insufficient cash, stale inputs, duplicate intent and queue saturation in your design notes. Separate what tests actually execute from features only proposed. Explain event ordering, ownership, restart/reconciliation and who can activate a kill switch in a future paper gateway.

## Capstone rubric (self-assessed, 100 points)

- 30: causal ledger and serial/parallel equality, independently calculated edge fixtures.
- 20: bounded input validation, ownership, sanitizer evidence and failure handling.
- 20: reproducible measurements with fair build/workload comparisons.
- 15: bottleneck explanation, uncertainty, overhead and rejected hypotheses.
- 15: deployment design, research holdout, explicit limits and primary references.

Require at least 80/100 AND no unresolved causality, corruption or duplicate-execution issue. The in-app multiple-choice final is separate and cannot certify performance or production readiness.
