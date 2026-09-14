# Algorithmic & AI stock bots

The course at `/curriculum/stock-bots` has 32 original applied lessons in eight units. Each lesson includes an objective, worked case, equation, runnable arithmetic worksheet, two practice questions, an assignment with a worked solution, and named primary references. The course has 64 practice questions, seven four-question checkpoints (75% threshold), and a 32-question final (80%, at least 26 correct). The automatic final is version 2; the written/code capstone is self-assessed separately.

| Unit | Topics | Lesson IDs in study order |
| --- | --- | --- |
| 1 | Specification, events, clocks, features | 5.6, 5.1, 5.7, 5.8 |
| 2 | Target reconciliation, trend, reversion, backtests | 5.2, 5.9, 5.10, 5.11 |
| 3 | Microstructure, order states, execution schedules, ledger | 5.12, 5.13, 5.14, 5.5 |
| 4 | Sizing, portfolio limits, pre-trade gates, halts | 5.4, 5.15, 5.16, 5.17 |
| 5 | Labels/splits, baselines, boosted-tree concepts, calibration | 5.18–5.21 |
| 6 | AI authority, filing evidence, structured validation, tools | 5.3, 5.22, 5.23, 5.24 |
| 7 | Async/backpressure, durability, incidents, release | 5.25–5.28 |
| 8 | Rule bot, fitted ridge, AI fixtures, acceptance dossier | 5.29–5.32 |

Original lesson identities 5.1–5.5 retain their original first practice questions and answer indices. Existing notes, drafts, and completion records stay addressable. The new final has new questions and a bumped version, so earlier passes do not silently certify expanded content.

## Runnable scope

Download `/course-assets/stock-bots/paper_bot_lab.py` and `/course-assets/stock-bots/README.md`. The standard-library project implements a local, one-symbol, long-only limit-order ledger with SQLite transactions, integer-cent accounting, partial fills, shared event volume, conservative reservations, duplicate/conflict handling, restart recovery, risk gates, cancellation, and persistent halts. The included guide defines its assumptions and expected output.

Two expanding-window ridge models actually fit artificial observations and evaluate later rows. AI examples are deterministic validation fixtures against fictional evidence; no provider is called. Boosted-tree training, live RAG, async broker integrations, actual short/borrow execution, and production deployment are explained as extensions, not falsely reported as implemented. The guided in-app worksheets print their case calculations and remain in cash in the price simulator.

## Source attribution and layout

`scripts/course_references.py` attaches named references to every course and lesson, preserving any lesson-specific links. `PageReferences` selects the current lesson/course sources for lessons, courses, and exams, and appropriate general or tool references for other routes, including the not-found page. The library exposes all cited publications, source-use guidance, independent-project attribution, and third-party software notices. Referenced book passages and question sets are not bundled.

`python3 scripts/third_party_notices.py` collects installed production dependency license/notice files after `npm ci`; the chart package's release notice is included explicitly because its npm distribution omits that file. TradingView's chart logo/link remains enabled. This work provides attribution and preserves supplied notices; it is not a legal clearance of every possible future use.

Course cards use responsive columns, readable text, flexible descriptions, aligned footers, and bottom spacing for assessment counts. The box-like book art is replaced with an open-book drawing, and course header art retains its proportions.

## Authoring and validation

```sh
python3 scripts/curriculum.py
python3 scripts/third_party_notices.py
python3 public/course-assets/stock-bots/paper_bot_lab.py
npm test
npm run test:api
TEST_URL=http://127.0.0.1:8088 npm run test:e2e
```

The shared catalog now contains 106 lessons, 206 practice questions, and 182 exam questions across 23 assessments. See [verification evidence](VERIFICATION.md) for the checks actually run.
