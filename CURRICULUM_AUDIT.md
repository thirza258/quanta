# Quanta Curriculum Audit

**Scope:** the implemented catalog in `content/catalog/curriculum.json`, its authoring sources in `content/authoring/`, the API in `backend/quanta/`, and the learning UI in `frontend/src/features/learning/`.

**Date:** 2026-11-27

**Method:** read all 28 course records, their parts, 471 lesson titles/objectives, 116 exams, and the frontend prerequisite graph. Course counts, sequence values, and prerequisite claims below come from the generated catalog, not from prose alone. Lesson and exam IDs were treated as immutable content identifiers.

---

## 1. What existed before this audit

The catalog array was ordered like this:

| Position | Course | Legacy `number` | Level |
|---:|---|---:|---|
| 0 | `trading-fundamentals` | 0 | Beginner |
| 1 | `trading-ethics` | 12 | Foundational |
| 2 | `simulator-workshop` | 13 | Beginner → intermediate |
| 3 | `lab-workshop` | 14 | Beginner → intermediate |
| 4 | `intelligent-investor` | 11 | Foundational |
| 5 | `security-analysis` | 1 | Intermediate |
| 6 | `news-to-markets` | 8 | Intermediate |
| 7 | `statistical-foundations` | 2 | Foundational → advanced |
| 8 | `econometrics` | 3 | Intermediate → advanced |
| 9 | `strategy-lab` | 4 | Applied |
| 10 | `stock-bots` | 5 | Advanced |
| 11 | `c-hpc-trading` | 9 | Advanced |
| 12 | `web3` | 6 | Foundations → advanced |
| 13 | `stock-machine-learning` | 7 | Intermediate → advanced |
| 14–21 | `forensic-accounting`, `credit-distress`, `quality-moats`, `bank-analysis`, `valuation-uncertainty`, `cyclical-industrials`, `tech-intangibles`, `real-world-casebook` | 15–22 | Advanced |
| 22–26 | `msme-financial-literacy`, `spreadsheet-to-strategy-lab`, `data-hygiene`, `conduct-compliance-essentials`, `python-reluctant-investor` | 23–27 | Beginner / intermediate |
| 27 | `algorithm-evaluation` | 10 | Advanced |

Two independent orderings existed:

- the **catalog array order**, which the API returns and the UI displays;
- the legacy `number` field, which no longer matched that order.

The frontend additionally carried a third, hand-maintained 4-stage graph in `frontend/src/features/learning/model/connections.ts`. Its stages, prerequisites, unlocks, and pathway text were not derived from the catalog.

---

## 2. Sequencing problems found

### 2.1 Advanced practice before its theory

`lab-workshop` sat at position 3, before Quantitative Investment Analysis and Financial Econometrics. Its lessons teach backtest mechanics, factor regression, robust standard errors, seed and cost robustness, VaR/CVaR-adjacent metrics, and the Deflated Sharpe Ratio. The first occurrence of “Deflated Sharpe Ratio” and “AMM” in the catalog was therefore in a course a learner could reach immediately after market fundamentals.

**Impact:** hidden prerequisites in regression, sampling, and multiple testing; learners were asked to interpret factor coefficients and robustness sweeps before those concepts were taught.

### 2.2 Quantitative foundations arrived after the workshops that use them

`statistical-foundations` (Quantitative Investment Analysis) came after the lab workshop. Its Part 1–Part 14 sequence is internally coherent: time value → descriptive statistics → probability → distributions → sampling → inference → regression → time series → ML → data pipelines → factors → risk → backtesting. The course was simply placed too late relative to the tools that depend on it.

### 2.3 Machine learning and bots were reversed

`stock-bots` appeared before `stock-machine-learning`, although the bot course contains a machine-learning unit, an advanced ML/AI unit, and evaluation units that assume labels, splits, regularized models, and walk-forward thinking. The first “boosting” mention in the catalog was in `stock-bots`.

### 2.4 Advanced fundamental analysis was stranded after the systems courses

The eight case-driven fundamental courses (forensic accounting, credit, quality, banks, valuation, cyclicals, intangibles, casebook) appeared after ML, bots, HPC, and Web3. A learner following the fundamental branch had to pass through the entire quantitative and systems sequence, or jump arbitrarily. `valuation-uncertainty` additionally requires the time-value material from Quantitative Investment Analysis, so it could not simply be moved next to `security-analysis`.

### 2.5 Web3 interrupted the core quantitative path

`web3` sat between HPC and machine learning in the array. Its prerequisites are only basic programming and arithmetic; it is not a prerequisite for equity or algorithmic trading. Its position implied a central role it does not have.

### 2.6 Beginner on-ramps were placed at the end

`data-hygiene`, `python-reluctant-investor`, `spreadsheet-to-strategy-lab`, and the Indonesian MSME course were positions 22–26, after advanced systems material. A beginner needing data hygiene or Python had to scroll past the entire advanced curriculum.

### 2.7 Recommendation metadata drifted

`funnel_cta` targets were hand-authored and sometimes pointed at courses that had moved. `getRecommendedNextTracks` sorted ready courses by a 4-stage number, not by academic sequence. The course map’s stage model had only four buckets, so stages such as “econometrics” and “ML” could not be expressed.

### 2.8 No machine-readable prerequisite graph in the catalog

Prerequisites were prose strings such as “Complete Quantitative Investment Analysis and the core econometrics units.” The only structured graph was the duplicated TypeScript array. API consumers could not validate or explain ordering, and the catalog could not detect cycles or late prerequisites.

---

## 3. Content-level findings

The audit checked module order inside each course, not only course order.

### 3.1 Coherent internal progressions (no lesson renumbering needed)

- `statistical-foundations`: time value → descriptive statistics → probability → distributions → sampling → inference → regression → multiple regression → time series → ML → data engineering → factors → risk → backtesting → capstone.
- `econometrics`: question and estimand → dataset → OLS → inference → time series → cointegration/volatility → factors → panel/causal → risk/credibility → MLE/GMM/asset-pricing tests → state-space/tails → replication projects.
- `strategy-lab`: hypothesis → data → value/quality → momentum/reversal → pairs → ML signal → portfolio/implementation → validation.
- `stock-machine-learning`: task/data quality → features/labels/splits → model training → selection/evaluation → diagnosis → deployment/monitoring.
- `stock-bots`: specification/events/data → rules/backtests → execution/accounting → risk controls → ML decisions → LLM evidence → operations → advanced execution → strategy families → validation/capacity → projects.
- `c-hpc-trading`: C foundations → data/event engine → profiling/correctness → threads/OpenMP → SIMD/GPU/distributed → risk/recovery.
- `web3`: cryptography → native ledger → ERC-20 → tokenomics/AMM → execution/adversarial validation → policy/release.
- `security-analysis`: analyst method → senior claims → preferred/convertible → common equity → earnings quality → asset realizability → comparison → modern bridge/capstone → advanced forensic/valuation synthesis.
- `intelligent-investor`: temperament → risk capacity/diversification → allocation policy → independent judgment/policy capstone → security-selection extensions.

### 3.2 Intentional two-tier capstones

`security-analysis` has a core investment-committee capstone (`1.24`) and an advanced red-team capstone (`1.31`). `intelligent-investor` has a policy capstone (`11.16`) followed by a security-selection extension unit. These are deliberate extension structures, not misplaced final exams. The final exams cover all modules, and the terminal capstones remain last in each course. No lesson was moved or renumbered.

### 3.3 Overlap that should remain parallel, not sequential

| Overlap | Decision |
|---|---|
| `trading-ethics` vs `conduct-compliance-essentials` | Keep ethics as the core conduct course; compliance is a professional reference/specialization. Do not require one before the other. |
| `strategy-lab` ML unit vs `stock-machine-learning` | Strategy Lab uses ML as a signal within research methodology; the ML course is the deeper model-building course. Strategy Lab is the hard prerequisite for bots; ML is recommended, not hard-gated. |
| `lab-workshop` vs `strategy-lab` | Lab is the research-platform orientation; Strategy Lab is the full strategy-research course. Lab is recommended before Strategy Lab, not a hard prerequisite. |
| `security-analysis` vs advanced value courses | Security Analysis is the hard prerequisite; the advanced courses are parallel specializations. |
| `simulator-workshop` vs `stock-bots` execution units | Simulator teaches fills, margin, and short selling at workshop level; bots teach order state machines, TWAP/VWAP, and implementation shortfall. Simulator is recommended, not hard-gated. |

### 3.4 Advanced concepts and their first teaching locations

A keyword scan of all lesson content found these first teaching occurrences:

| Concept | First teaching course | Why it is acceptable |
|---|---|---|
| GARCH | `statistical-foundations` (2.18), deepened in `econometrics` (3.18) | QIA introduces changing volatility after inference and regression. |
| Cointegration | `statistical-foundations` (2.17), deepened in `econometrics` (3.2) | QIA introduces stationarity first; econometrics provides the full treatment. |
| Deflated Sharpe Ratio | `statistical-foundations` (2.27) | QIA teaches multiple testing and backtest hygiene before Strategy Lab and the capstone. |
| Black–Litterman | `statistical-foundations` (2.39) | QIA teaches Bayesian updates, factor risk, and portfolio views first. |
| AMM / impermanent loss | `lab-workshop` after reorder | Now appears after statistics and before the Web3 specialization; it is a tool tour, not a core prerequisite. |
| SIMD / OpenMP | `c-hpc-trading` | Only after the Python bot and strategy courses. |
| Boosting / forests | `stock-machine-learning` after reorder | Now precedes `stock-bots`, which uses ML decisions. |

Incidental literature citations (for example, an inflation study described as using cointegration in `intelligent-investor`) were not treated as teaching occurrences and were not moved.

---

## 4. Duplicated or missing prerequisite declarations

- `valuation-uncertainty` required time value from `statistical-foundations` in prose but the structured graph did not state it.
- `real-world-casebook` required “at least one of forensic accounting, credit analysis, or bank analysis” in prose; the graph listed only `security-analysis`.
- `algorithm-evaluation` was described as accepting a project from the Python bot, C/HPC, or stock-ML course; the graph required only `stock-bots`.
- `lab-workshop` used regression and robust errors but declared only `trading-fundamentals`.
- `stock-bots` used ML but declared only `trading-fundamentals` and `statistical-foundations`.
- `conduct-compliance-essentials` had no prerequisites, which is correct for a reference course, but its placement implied advanced status.

---

## 5. Specialization candidates

These courses do not belong in a single mandatory chain:

- Advanced fundamental analysis: `forensic-accounting`, `credit-distress`, `quality-moats`, `bank-analysis`, `cyclical-industrials`, `tech-intangibles`, `valuation-uncertainty`, `real-world-casebook`.
- Web3/DeFi: `web3`.
- Professional/reference: `conduct-compliance-essentials`.
- Alternative on-ramp: `msme-financial-literacy`.
- Foundation on-ramps: `data-hygiene`, `python-reluctant-investor`, `spreadsheet-to-strategy-lab`.

The core sequence remains: fundamentals → intelligent investor → security analysis → news → quantitative foundations → econometrics → research/strategy → ML → bots → HPC → capstone.

---

## 6. Audit conclusion

The implemented content was strong; the ordering and metadata were not. The main defects were the early lab workshop, late quantitative foundations, reversed ML/bots order, stranded fundamental specializations, and a duplicated frontend graph. The reorder proposal in `CURRICULUM_REORDER_PROPOSAL.md` addresses these without changing course IDs, lesson IDs, exam IDs, URLs, or progress keys.