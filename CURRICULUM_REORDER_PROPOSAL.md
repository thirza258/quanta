# Quanta Curriculum Reorder Proposal

**Status:** implemented in this change.

**Principles applied:** foundations before specialization; mathematical/statistical prerequisites before quantitative models; research methodology before strategy construction; strategy before algorithmic execution; algorithms before optimization; specializations off the core spine; stable content IDs; one machine-readable dependency graph.

---

## 1. Proposed order (implemented)

| New position | Course | Old position | Stage | Difficulty | Role |
|---:|---|---:|---:|---:|---|
| 1 | `trading-fundamentals` | 0 | 1 | 0 | Core orientation |
| 2 | `trading-ethics` | 1 | 2 | 1 | Core conduct |
| 3 | `simulator-workshop` | 2 | 2 | 1 | Core workshop |
| 4 | `intelligent-investor` | 4 | 2 | 1 | Core investing principles |
| 5 | `security-analysis` | 5 | 3 | 2 | Core fundamental analysis |
| 6 | `news-to-markets` | 6 | 3 | 2 | Core market information |
| 7 | `forensic-accounting` | 14 | 4 | 3 | Fundamental specialization |
| 8 | `credit-distress` | 15 | 4 | 3 | Fundamental specialization |
| 9 | `quality-moats` | 16 | 4 | 3 | Fundamental specialization |
| 10 | `bank-analysis` | 17 | 4 | 3 | Fundamental specialization |
| 11 | `cyclical-industrials` | 19 | 4 | 3 | Fundamental specialization |
| 12 | `tech-intangibles` | 20 | 4 | 3 | Fundamental specialization |
| 13 | `real-world-casebook` | 21 | 4 | 4 | Fundamental branch capstone |
| 14 | `data-hygiene` | 24 | 5 | 1 | Foundation workshop |
| 15 | `python-reluctant-investor` | 26 | 5 | 1 | Foundation workshop |
| 16 | `statistical-foundations` | 7 | 5 | 3 | Core quantitative foundations |
| 17 | `valuation-uncertainty` | 18 | 5 | 3 | Quantitative valuation specialization |
| 18 | `econometrics` | 8 | 6 | 4 | Core empirical finance |
| 19 | `lab-workshop` | 3 | 7 | 2 | Core research-platform workshop |
| 20 | `spreadsheet-to-strategy-lab` | 23 | 7 | 2 | Optional strategy bridge |
| 21 | `strategy-lab` | 9 | 7 | 3 | Core strategy research |
| 22 | `stock-machine-learning` | 13 | 8 | 4 | Core ML |
| 23 | `stock-bots` | 10 | 9 | 4 | Core algorithmic trading |
| 24 | `c-hpc-trading` | 11 | 10 | 5 | Core HPC |
| 25 | `web3` | 12 | 11 | 3 | Specialization |
| 26 | `conduct-compliance-essentials` | 25 | 11 | 3 | Professional reference |
| 27 | `msme-financial-literacy` | 22 | 11 | 1 | Alternative on-ramp |
| 28 | `algorithm-evaluation` | 27 | 12 | 4 | Capstone |

Positions are represented by `sequence` values 10, 20, …, 280. `stage` (slug), `stage_number`, `stage_name`, `difficulty`, `estimated_hours`, `prerequisite_course_ids`, `prerequisite_any_of`, `recommended_course_ids`, `learning_outcomes`, `skills`, `domain`, `course_type`, `is_core`, `is_specialization`, and `is_capstone` are attached to every catalog course.

---

## 2. Change-by-change rationale

### 2.1 `lab-workshop`: position 3 → 19

**Reason:** it teaches backtest mechanics, factor regression, robust errors, seed/cost robustness, and Deflated Sharpe concepts. Those require the sampling, inference, regression, and multiple-testing material in `statistical-foundations` and the time-series material in `econometrics`.

**Prerequisites:** hard `statistical-foundations`; soft `econometrics`.

**Affected:** the new Strategy Lab pathway and the research-platform recommendation logic. The course itself, its 14.x lesson IDs, and its exams are unchanged.

### 2.2 `statistical-foundations`: position 7 → 16

**Reason:** every quantitative course after it depends on its probability, inference, regression, factor, risk, and backtesting content. It now precedes the lab workshop, econometrics, valuation under uncertainty, Strategy Lab, ML, bots, and HPC.

**Prerequisites:** hard `trading-fundamentals` for market vocabulary; no finance specialization required.

**Trade-off:** learners reach quantitative material after six fundamental/market courses. This is intentional: the PRD’s “financial literacy → market fundamentals → investment principles → statements → security analysis” progression should not be skipped for learners who intend to interpret financial data.

### 2.3 `stock-machine-learning`: position 13 → 22

**Reason:** `stock-bots` contains ML decision units and advanced ML/AI evaluation units. The dedicated ML course now precedes the bot course, so labels, splits, regularized/tree models, walk-forward validation, and monitoring are taught before they are used.

**Prerequisites:** hard `statistical-foundations`, `econometrics`; soft `strategy-lab`.

**Trade-off:** ML remains after Strategy Lab because the ML course assumes cost-aware evaluation and research discipline. The ML course is not a hard prerequisite for bots; it is strongly recommended. This preserves a viable bot path for learners who already have ML elsewhere while removing the default-path reversal.

### 2.4 `stock-bots`: position 10 → 23

**Reason:** algorithmic trading comes after strategy research and ML. The bot course now has hard `strategy-lab` and soft `stock-machine-learning`/`simulator-workshop`.

**Affected:** bots still precede HPC, which is correct; C/HPC now follows both the Python bot and the strategy/ML foundations.

### 2.5 Advanced fundamental courses: positions 14–21 → 7–13

**Reason:** a fundamental investor should not pass through ML, bots, HPC, and Web3 to reach forensic accounting. The six advanced courses are parallel specializations after `security-analysis`; the casebook closes the branch with a one-of prerequisite among forensic/credit/bank.

**Trade-off:** `valuation-uncertainty` is not in this block. It requires the time-value material in `statistical-foundations`, so it moves to Stage 5 after QIA. This avoids a hidden prerequisite and keeps the fundamental branch free of an early quantitative dependency.

### 2.6 `web3`: position 12 → 25

**Reason:** Web3 is not a prerequisite for equity research, econometrics, strategy, ML, or bots. It is a specialization that can be taken after market fundamentals and basic programming. It now sits in Stage 11, after the core algorithmic/HPC sequence, so it cannot interrupt the quantitative spine.

**Affected:** the Web3 pathway now includes Python, data hygiene, statistics, and econometrics before the Web3 course, then Strategy Lab and the capstone for research validation.

### 2.7 Beginner on-ramps: positions 22–26 → 14–15 and 20

**Reason:** `data-hygiene` and `python-reluctant-investor` are needed before data work and scripting. They now sit at the start of Stage 5. `spreadsheet-to-strategy-lab` sits in Stage 7, next to the lab and Strategy Lab it bridges. `msme-financial-literacy` is an alternative audience on-ramp and sits in Stage 11 so it does not displace the main path’s second course.

**Trade-off:** MSME literacy is beginner-level but appears late in the catalog. It is marked `course_type: "on-ramp"` and `is_specialization: true`; the UI’s course map and pathway views make its independent role explicit. This is preferable to placing an Indonesian MSME course second in the default quantitative path.

### 2.8 `conduct-compliance-essentials`: position 25 → 26

**Reason:** it is a professional reference/specialization that overlaps `trading-ethics` but also covers GIPS, implementation shortfall, p-hacking, audit trails, cyber, and ESG. It is not a prerequisite for any core course and is best taken after some strategy/research context.

### 2.9 `algorithm-evaluation`: position 27 → 28

**Reason:** it remains the final capstone. It now requires `strategy-lab` and at least one of `stock-bots`, `stock-machine-learning`, or `c-hpc-trading`. This expresses the course’s real “any algorithm project” prerequisite instead of forcing the Python-bot branch.

### 2.10 `news-to-markets`: position 6 → 6 (unchanged)

**Reason:** it already followed `security-analysis`, which is academically correct. It now precedes the advanced fundamental specializations, so news analysis is learned before the learner branches into forensic/credit/quality work.

### 2.11 `simulator-workshop`: position 2 → 3

**Reason:** it follows both `trading-fundamentals` and `trading-ethics`. It remains early because the PRD wants the simulator available early enough to motivate practice; advanced execution topics are introduced as workshop material and deepened later in bots/HPC. The simulator’s advanced features are not a prerequisite for the research courses.

### 2.12 `trading-ethics` and `intelligent-investor`: positions 1/4 → 2/4

**Reason:** ethics remains immediately after fundamentals; the investor companion remains before Security Analysis. The change is that the simulator now sits between ethics and the investor course, matching its hard prerequisite pair.

---

## 3. What did not change

- **Course IDs** are unchanged.
- **Lesson IDs** are unchanged (`0.1`–`27.6`, including the non-sequential IDs such as `1.1`, `1.6`, `1.7`, `2.33`, `4.5`, `5.6`, `6.1`, `8.1`, `9.1`, `10.1`, `11.1`, `12.1`).
- **Exam IDs and versions** are unchanged.
- **URLs** `/curriculum/{course-id}` and `/learn/{lesson-id}` remain valid.
- **Progress keys** (lesson IDs and exam IDs) remain valid.
- **Saved code, notes, submissions, certificates, and workspace state** remain associated with the same content.
- **Lesson and exam counts** are unchanged.
- **Course content** was not deleted or rewritten to solve ordering problems.

The only new data is metadata. `number` is preserved as a legacy field; new code uses `sequence` and `stage_number`. `trackLabel` and the “START HERE” badge now key off the stable `trading-fundamentals` ID rather than the legacy number.

---

## 4. Migration considerations

### API

`GET /api/v1/courses` returns the same array of course objects in the new order, with additive metadata fields. Existing consumers that key by `id` are unaffected. Consumers that assumed array position should switch to `sequence`.

### Frontend

- `frontend/src/features/learning/model/connections.ts` is now derived from catalog metadata. It still exports `courseConnections`, `STAGE_CONFIG`, `DOMAIN_CONFIG`, `learningPathways`, `arePrerequisitesMet`, `getMissingPrerequisites`, `getCourseReadiness`, and `getRecommendedNextTracks`.
- `CourseConnection` adds `prerequisitesAnyOf`, `courseType`, `difficulty`, `sequence`, `isCore`, `isSpecialization`, and `isCapstone`.
- `CourseMap` renders all 12 stages and displays one-of prerequisites explicitly.
- `getRecommendedNextTracks` sorts by `sequence`, not by the old four-stage number.
- `funnel_cta` is regenerated to point at the next course in the validated sequence.

### Tests and build

- `content/authoring/curriculum_metadata.py` fails the build on missing metadata, duplicate sequences, unknown prerequisites, late prerequisites, or graph cycles.
- `backend/tests/test_curriculum_structure.py` validates the committed catalog.
- Frontend `connections.test.ts` validates the metadata-derived graph, sequence order, DAG property, roles, and pathways.
- Existing course-content tests were updated only where they asserted a positional order that the reorder intentionally changes.

---

## 5. Trade-offs documented

| Decision | Alternative | Why this order |
|---|---|---|
| Simulator workshop stays early (Stage 2) | Move it to Stage 8 after strategy | The PRD asks for early simulator access. Its advanced features are introduced as supervised workshop material; bots/HPC later deepen execution. Keeping it early maximises practice motivation without gating research courses. |
| `valuation-uncertainty` sits after QIA (Stage 5) | Keep it with the Stage 4 value specializations | Its own prerequisite text requires time value from QIA. Keeping it in Stage 4 would hide a quantitative prerequisite. |
| `stock-machine-learning` before `stock-bots` | Keep bots first because bots include ML | The default path should teach labels, splits, validation, and model monitoring before the bot uses them. Bots still has a viable path if a learner has equivalent ML elsewhere because ML is soft, not hard. |
| Advanced value branch before quantitative foundations | Move all value courses after QIA | The fundamental branch is a legitimate path and should not require econometrics/ML. Only valuation under uncertainty needs the quantitative bridge. |
| Web3 after HPC | Keep Web3 in the middle | Web3 is a specialization and not a prerequisite for the core. Placing it after the spine prevents it from interrupting the quant progression. |
| MSME on-ramp late | Place it second | It serves a different audience; placing it second would displace the main path. It is explicitly marked as an independent on-ramp. |
| Two capstones (`real-world-casebook`, `algorithm-evaluation`) | One capstone only | The casebook is the capstone of the fundamental specialization branch; algorithm evaluation is the capstone of the quantitative/algorithmic core. Both are terminal within their branch. |

---

## 6. Acceptance check

| PRD requirement | Result |
|---|---|
| Every core course has an explainable position | Each course has stage, sequence, difficulty, focus summary, skills, and prerequisites in metadata. |
| Advanced courses have earlier prerequisites | Build-time and test-time checks enforce earlier hard/one-of/soft prerequisites. |
| Math/statistics before dependent quantitative material | QIA precedes econometrics, lab workshop, valuation, Strategy Lab, ML, bots, HPC, and capstone. |
| ML after statistical/econometric foundations | `stock-machine-learning` follows QIA and econometrics. |
| Algorithmic trading after strategy and market foundations | `stock-bots` hard-requires `strategy-lab`; market fundamentals precede both. |
| HPC after the algorithms it optimizes | `c-hpc-trading` hard-requires `stock-bots`. |
| Web3 can run as a specialization | Web3 is Stage 11, after the core, with only market fundamentals as a hard prerequisite. |
| Existing IDs/URLs/progress remain compatible | No course, lesson, or exam ID changed. |
| API order matches frontend order | Both consume the same catalog array; frontend graph derives from its metadata. |
| Learner can answer “what next, and why?” | Course map shows stages, prerequisites, one-of options, unlocks, readiness, and five pathways. |