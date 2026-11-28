# Quanta Curriculum Dependency Graph

**Canonical source:** `content/authoring/curriculum_metadata.py`

This file defines stage, sequence, difficulty, hard prerequisites, one-of prerequisites, soft recommendations, course role, and skills. It is applied by `content/authoring/curriculum.py`; it does not contain lesson or exam IDs.

The frontend graph in `frontend/src/features/learning/model/connections.ts` is now derived from this metadata. The API returns the same catalog array, sorted by `sequence`.

---

## 1. Stages

| Stage | Slug | Academic phase | Typical difficulty |
|---:|---|---|---|
| 1 | `orientation` | Orientation and market mechanics | L0 |
| 2 | `foundations` | Financial and investment foundations | L1 |
| 3 | `fundamental-analysis` | Fundamental analysis and market information | L2 |
| 4 | `advanced-fundamental` | Advanced fundamental specializations | L3–L4 |
| 5 | `quantitative-foundations` | Quantitative foundations and applied valuation | L1–L3 |
| 6 | `empirical-finance` | Empirical finance and econometrics | L4 |
| 7 | `research-strategy` | Research methodology and strategy development | L2–L3 |
| 8 | `machine-learning` | Machine learning for markets | L4 |
| 9 | `algorithmic-trading` | Algorithmic and AI trading | L4 |
| 10 | `high-performance-computing` | High-performance computing | L5 |
| 11 | `specializations` | Specializations and professional practice | L1–L3 |
| 12 | `capstone` | Capstone research evaluation | L4 |

Difficulty uses the PRD scale: L0 orientation, L1 beginner, L2 intermediate, L3 advanced, L4 graduate, L5 research/specialist.

---

## 2. Course sequencing matrix

| # | Course | Stage | Difficulty | Core | Type | Hours | Hard prerequisites | One-of prerequisites | Soft prerequisites |
|---:|---|---:|---:|---|---|---:|---|---|---|
| 1 | `trading-fundamentals` | 1 | 0 | yes | core | 2.0 | — | — | — |
| 2 | `trading-ethics` | 2 | 1 | yes | core | 8.0 | trading-fundamentals | — | — |
| 3 | `simulator-workshop` | 2 | 1 | yes | workshop | 8.0 | trading-fundamentals, trading-ethics | — | — |
| 4 | `intelligent-investor` | 2 | 1 | yes | core | 10.0 | trading-fundamentals | — | — |
| 5 | `security-analysis` | 3 | 2 | yes | core | 7.6 | trading-fundamentals | — | intelligent-investor |
| 6 | `news-to-markets` | 3 | 2 | yes | core | 12.0 | security-analysis | — | trading-fundamentals |
| 7 | `forensic-accounting` | 4 | 3 | specialization | specialization | 1.3 | security-analysis | — | — |
| 8 | `credit-distress` | 4 | 3 | specialization | specialization | 1.3 | security-analysis | — | — |
| 9 | `quality-moats` | 4 | 3 | specialization | specialization | 1.3 | security-analysis | — | — |
| 10 | `bank-analysis` | 4 | 3 | specialization | specialization | 1.2 | security-analysis | — | — |
| 11 | `cyclical-industrials` | 4 | 3 | specialization | specialization | 1.2 | security-analysis | — | — |
| 12 | `tech-intangibles` | 4 | 3 | specialization | specialization | 1.2 | security-analysis | — | — |
| 13 | `real-world-casebook` | 4 | 4 | specialization | capstone | 1.7 | security-analysis | forensic-accounting, credit-distress, bank-analysis | quality-moats, news-to-markets |
| 14 | `data-hygiene` | 5 | 1 | no | foundation | 1.1 | — | — | trading-fundamentals |
| 15 | `python-reluctant-investor` | 5 | 1 | no | foundation | 1.3 | — | — | — |
| 16 | `statistical-foundations` | 5 | 3 | yes | core | 10.8 | trading-fundamentals | — | — |
| 17 | `valuation-uncertainty` | 5 | 3 | specialization | specialization | 1.2 | security-analysis, statistical-foundations | — | — |
| 18 | `econometrics` | 6 | 4 | yes | core | 10.5 | statistical-foundations | — | python-reluctant-investor |
| 19 | `lab-workshop` | 7 | 2 | yes | workshop | 6.0 | statistical-foundations | — | econometrics |
| 20 | `spreadsheet-to-strategy-lab` | 7 | 2 | no | workshop | 1.5 | — | — | trading-fundamentals, python-reluctant-investor, lab-workshop |
| 21 | `strategy-lab` | 7 | 3 | yes | core | 16.0 | statistical-foundations, econometrics | — | lab-workshop, security-analysis, python-reluctant-investor |
| 22 | `stock-machine-learning` | 8 | 4 | yes | core | 12.0 | statistical-foundations, econometrics | — | strategy-lab, python-reluctant-investor |
| 23 | `stock-bots` | 9 | 4 | yes | core | 9.7 | strategy-lab | — | stock-machine-learning, simulator-workshop |
| 24 | `c-hpc-trading` | 10 | 5 | yes | core | 12.0 | stock-bots | — | strategy-lab |
| 25 | `web3` | 11 | 3 | specialization | specialization | 4.8 | trading-fundamentals | — | python-reluctant-investor |
| 26 | `conduct-compliance-essentials` | 11 | 3 | specialization | reference | 7.1 | — | — | trading-ethics, strategy-lab |
| 27 | `msme-financial-literacy` | 11 | 1 | specialization | on-ramp | 3.2 | — | — | — |
| 28 | `algorithm-evaluation` | 12 | 4 | yes | capstone | 8.0 | strategy-lab | stock-bots, stock-machine-learning, c-hpc-trading | econometrics, lab-workshop |

---

## 3. Hard prerequisites

A hard prerequisite is required for readiness. The learner cannot start the dependent course until it is complete.

```text
trading-fundamentals
├── trading-ethics
│   └── simulator-workshop
├── intelligent-investor (soft for security-analysis)
├── security-analysis
│   ├── news-to-markets
│   ├── forensic-accounting
│   ├── credit-distress
│   ├── quality-moats
│   ├── bank-analysis
│   ├── cyclical-industrials
│   ├── tech-intangibles
│   ├── real-world-casebook  (plus one of forensic, credit, bank)
│   └── valuation-uncertainty (plus statistical-foundations)
├── statistical-foundations
│   ├── econometrics
│   │   ├── strategy-lab
│   │   │   ├── stock-machine-learning
│   │   │   ├── stock-bots
│   │   │   │   └── c-hpc-trading
│   │   │   └── algorithm-evaluation (plus one of bots, ML, HPC)
│   │   └── stock-machine-learning
│   ├── lab-workshop
│   └── valuation-uncertainty
└── web3
```

`algorithm-evaluation` additionally requires **at least one** of `stock-bots`, `stock-machine-learning`, or `c-hpc-trading`. `real-world-casebook` additionally requires **at least one** of `forensic-accounting`, `credit-distress`, or `bank-analysis`.

## 4. Soft prerequisites

Soft prerequisites are strongly recommended but do not lock the course.

| Course | Recommended before | Reason |
|---|---|---|
| `security-analysis` | `intelligent-investor` | Temperament and margin-of-safety vocabulary before statement analysis. |
| `news-to-markets` | `trading-fundamentals` | Market-reaction context for event studies. |
| `econometrics` | `python-reluctant-investor` | Worksheets assume basic scripting. |
| `lab-workshop` | `econometrics` | The factor studio and robust errors are easier after inference. |
| `strategy-lab` | `lab-workshop`, `security-analysis`, `python-reluctant-investor` | Platform familiarity, fundamental strategies, and Python. |
| `stock-machine-learning` | `strategy-lab`, `python-reluctant-investor` | Research methodology and scripting. |
| `stock-bots` | `stock-machine-learning`, `simulator-workshop` | ML decisions and execution intuition. |
| `c-hpc-trading` | `strategy-lab` | The algorithms being optimized. |
| `web3` | `python-reluctant-investor` | Guided labs and project setup. |
| `conduct-compliance-essentials` | `trading-ethics`, `strategy-lab` | Core conduct and backtest/reporting context. |
| `algorithm-evaluation` | `econometrics`, `lab-workshop` | Statistical context and reproducible research workflow. |
| `spreadsheet-to-strategy-lab` | `trading-fundamentals`, `python-reluctant-investor`, `lab-workshop` | Market context, scripting, and tool orientation. |

## 5. Parallel and elective relationships

These pairs do not require a strict order and are intentionally parallel:

- The six advanced fundamental courses after `security-analysis`: forensic accounting, credit, quality, banks, cyclicals, intangibles.
- `news-to-markets` and the advanced fundamental branch: both build on `security-analysis`; news is the market-information bridge, the others are deeper company analysis.
- `web3` is a specialization branch, not a core prerequisite for equity or algorithmic trading.
- `conduct-compliance-essentials` is a reference course; it overlaps `trading-ethics` but is not a duplicate prerequisite.
- `msme-financial-literacy` is an alternative on-ramp for a different audience; it is not part of the quant core.
- `data-hygiene`, `python-reluctant-investor`, and `spreadsheet-to-strategy-lab` are enabling workshops; they support the core but do not gate it, except where a course explicitly declares Python comfort.

## 6. Recommended learning pathways

The UI exposes five pathways. They are curated sequences, not additional prerequisites.

### Complete Quantitative Finance Path

`trading-fundamentals` → `trading-ethics` → `intelligent-investor` → `security-analysis` → `statistical-foundations` → `econometrics` → `lab-workshop` → `strategy-lab` → `stock-machine-learning` → `stock-bots` → `c-hpc-trading` → `algorithm-evaluation`

### Fundamental Equity & Value Investor

`trading-fundamentals` → `intelligent-investor` → `security-analysis` → `news-to-markets` → `forensic-accounting` → `credit-distress` → `quality-moats` → `bank-analysis` → `statistical-foundations` → `valuation-uncertainty` → `real-world-casebook`

### Quantitative Researcher & Alpha Modeler

`trading-fundamentals` → `statistical-foundations` → `econometrics` → `lab-workshop` → `strategy-lab` → `stock-machine-learning` → `algorithm-evaluation`

### Algorithmic Trading Engineer

`trading-fundamentals` → `trading-ethics` → `simulator-workshop` → `python-reluctant-investor` → `statistical-foundations` → `econometrics` → `strategy-lab` → `stock-bots` → `c-hpc-trading` → `algorithm-evaluation`

### Web3 & Decentralized Finance

`trading-fundamentals` → `python-reluctant-investor` → `data-hygiene` → `statistical-foundations` → `econometrics` → `web3` → `strategy-lab` → `algorithm-evaluation`

## 7. Validation rules enforced at build time

`attach_curriculum_metadata` fails the content build if any of these are false:

1. every course ID has exactly one metadata entry;
2. sequences are unique and contiguous;
3. every stage exists;
4. difficulty is within 0–5;
5. every hard, one-of, and soft prerequisite exists and appears earlier in the sequence;
6. no course requires itself;
7. the hard/one-of graph is acyclic (Kahn topological sort);
8. a course is not simultaneously core and a specialization;
9. a capstone flag implies `course_type == "capstone"`;
10. every course has a focus summary and at least three skills.

`backend/tests/test_curriculum_structure.py` repeats the structural checks against the committed JSON and adds order-specific assertions: QIA before econometrics, econometrics before Strategy Lab, ML before bots, bots before HPC, Web3 after core, and advanced concept phrases only after Quantitative Investment Analysis.

## 8. Why the graph is not one linear chain

A strict `Course 1 → Course 2 → ... → Course 28` would force a fundamental investor through HPC and a systems engineer through forensic accounting. The graph instead has:

- a **core spine** (fundamentals → fundamental analysis → quant foundations → econometrics → research/strategy → ML → bots → HPC → capstone);
- **specialization branches** (advanced fundamental, Web3/DeFi, professional compliance);
- **workshops** that practise already-taught concepts;
- **foundations/on-ramps** for learners who need data, Python, spreadsheet, or MSME literacy.

The sequence is a topological teaching order for the default path, not a claim that every learner must take every course.