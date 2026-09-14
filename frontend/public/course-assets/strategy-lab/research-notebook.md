# Strategy research notebook

Name / date / source revision:

## 1. Hypothesis and data audit — 20 points

Write the mechanism, eligible universe, signal and two falsifying observations.
Declare the benchmark, information timestamps, filing revision policy, missing-data
policy and corporate-action convention. Reproduce the NCAV haircut case (raw 11,
adjusted 6.6, adjusted two-thirds ceiling 4.4). Attach an eligibility waterfall.

Evidence: specification, input hashes, data dictionary, exclusions and as-of table.

## 2. Timing and accounting — 25 points

Draw decision-close → next-open fill → close valuation. Reproduce the two-share
round trip: 1,000 → 798 cash plus two shares → 1,015.8 cash; fees 4.2.
Run the tests and explain why a last-close signal cannot fill. Reconcile cash plus
marked positions against every equity row. Explain partial fills, target caps,
alphabetical cash priority, unfilled expiration and terminal positions.

Evidence: test output, one annotated trade/position sequence, gap and cash cases.

## 3. Comparison and selection — 20 points

Before reading final results, record the three candidates, validation objective,
tie-break, segment dates and boundary state. Predict which mechanism might help and
what could refute it. Retain every validation result. Explain the costless index
versus executable equal-weight candidate. Record the winner and frozen test outcome,
including negative results. Log every additional local trial and test inspection.

| Trial | One changed assumption | Data segment | Net result | Turnover | Rejection evidence |
| --- | --- | --- | --- | --- | --- |
| Base | None | Validation | | | |

## 4. Stress and limitations — 20 points

Compare base, doubled costs and tighter liquidity for the same selected rule.
Document unfilled quantities and changed cash exposure. Propose one independent
extension with expected behavior, a falsifier and tests; label it proposed until
implemented. Distinguish a synthetic engine check from independent market evidence.

Optional specialist dossiers: pair hedge units/borrow/one-leg failures; ML label
purges/nested selection/frozen predictions; covariance/correlation stress. Do not
claim these run in the supplied long-only engine.

## 5. Reproducibility and communication — 15 points

Preserve source, inputs, manifest, ledger, signals, trades, positions and valuations.
Write a concise reject/revise/paper-study conclusion and an opposing interpretation.
Link each claim to evidence, cite primary references and hand aligned test exports
to the final Algorithm Evaluation course. Declare all omitted implementation costs.

## Acceptance

Target at least 80/100 on this self-assessed written project. The concept exam is
separate. Unresolved look-ahead, fabricated results, missing losses or unreconciled
cash require revision regardless of score. This rubric is not a professional credential.

References: see the original source list in README.md and each course lesson.
