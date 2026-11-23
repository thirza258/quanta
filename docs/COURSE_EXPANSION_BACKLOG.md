# Expansion courses — work not yet implemented

Status: November 23, 2026, after `13594ff`.

This is the implementation plan for every finding in [the review](COURSE_EXPANSION_REVIEW.md) that is still open. Each item gives what is wrong, where to change it, how to fix it, and how to check it.

**Already done.** Answer-position rebalancing at build time, exams moved to version 2, the `conduct-final-scenario-3` key, the 26.3 figures, `sma_50` in 24.4, `lookback_window` in 27.5, the 25.6 CSV quoting, and f-string format specs in the sandbox (with width ≤ 200 and precision ≤ 50).

## How to work on these courses

- **Edit source, not output.**
  - Lesson text, code, exercises and exams live in `content/authoring/<course>_course.py`.
  - Real-world sections are the `APPLICATIONS` tuples in `content/authoring/case_applications_expansion.py`.
  - Shared case studies are in `content/authoring/real_world_cases.py`.
  - Course descriptions and glossary terms are in `content/authoring/learning_guidance.py`.
- **Regenerate** with `python3 content/authoring/curriculum.py`. `npm run content:build` also rewrites the sitemap's `lastmod` dates; use it only when that's wanted.
- **Check** with `cd backend && .venv/bin/python ../.research-work/course-fix/check_courses.py [course-id]`. The script lives in the git-excluded `.research-work/`; copy it into `backend/scripts/` if it should be shared. It reports duplicate IDs, dead internal links, code that fails in the guided runtime, answer keys out of range, `lessonId`s outside the course, and position and length bias.
- **Exam versions.** When an exam's questions or keys change, bump its `version` so stale drafts are not resumed.
- **The guided runtime.** Lesson code runs in `backend/quanta/execution/sandbox_worker.py`:
  - Allowed: variables, numbers, lists, dicts, functions with positional arguments, `if`, bounded `for` loops, `print`, f-strings, `math`, a small numpy subset, and the helpers `sma ema highest lowest change shift stdev zscore`.
  - Not allowed: no pandas, no matplotlib, no keyword arguments, no attribute access on lists (no `.append`), no tracebacks (errors are one line).
  - `data` columns: `open high low close volume returns sma_50 sma_200`.
- **What the app actually does.** Write lessons to this; several current lessons contradict it.
  - **Strategy lab** is `/lab` with tools `?tool=market|valuation|factors|broker|amm`. Its button is "Run experiment". Signals fill at the next open. Costs are basis points of notional per fill (default 5 bps commission, 3 bps slippage). It is long or cash and all-in, with 252 sessions a year and Sharpe measured over a 3% risk-free rate. It loads the *earliest* `years × 252` bars of a dataset.
  - **Historical import** is command-line only: `backend/scripts/import_data.py prices.csv SYMBOL`, with columns `time,open,high,low,close,volume`. There is no upload page.
  - **Saved experiments** are named snapshots with no versions. Versioning (SHA-256 of the source, numbered when a run is queued) and the look-ahead test live in the research registry at `/research` ([guide](RESEARCH_PLATFORM.md)).
  - **Factor studio** fits CAPM/FF3/Carhart/FF5 regressions with HAC errors. It does not rank stocks into quintiles.
  - **The AMM simulator** covers swap output, price impact, fees and impermanent loss, including concentrated ranges. There is no routing or arbitrage. `/simulator` is the paper-trading terminal.
  - **Capstones.** Validators exist at `POST /api/v1/courses/{id}/capstone`, but no page calls them.

---

## P0 — must fix before these courses issue certificates

### P0-1. The correct option is usually the longest (all five courses)

- **Now:** after the position fix, the correct option is still the longest in MSME 18/21, Spreadsheet 13/14, Data Hygiene 12/12, Conduct 43/43 and Python 9/12, counting practice questions and exams together. Picking the longest option passes every final.
- **Fix:**
  - Rewrite the distractors in every `question(...)` call and exam entry in the five authoring files. They should be plausible and specific, of similar length to the key, and wrong for a reason a learner who skipped the lesson would not spot.
  - Keep exactly one defensible answer, and make each explanation say why the others are wrong.
- **Optional guard:** in `curriculum.py`, fail the build when the key is the longest option in more than 45% of a course's questions.
- **Check:** `check_courses.py` reports no length problems, which means at most 45% per course.

### P0-2. Conduct & Compliance lessons 26.9–26.17 are template stubs

- **Where:** the `extra_titles` loop in `conduct_compliance_course.py` (about lines 565–655), which generates the same ~1,000-character text, the formula "Compliance Metric = 100%" and the code `rule_verified = True` for nine lessons. Exam questions `conduct-final-q9`…`q17` test material those lessons never teach.
- **Fix:**
  - Write nine real lessons, preferably in a new module (`conduct_compliance_part4.py` returning modules and exam questions), and replace the loop and q9–q17 with them.
  - Each lesson needs:
    - an accurate worked example;
    - guided-runtime code that computes something meaningful;
    - two or more practice questions;
    - 2–4 glossary terms;
    - 2–4 primary references (rule pages, not homepages);
    - a realWorld tuple that fits.
- **Content per lesson** (verify each rule against its primary source before writing):

  | Lesson | Teach | Primary sources |
  | --- | --- | --- |
  | 26.9 Best execution | FINRA 5310(a)(1) factors versus the .09 regular-and-rigorous review; implementation shortfall in bps against the arrival price | finra.org Rule 5310 |
  | 26.10 P-hacking | Family-wise error 1−(1−α)^N, false discovery rate, the deflated Sharpe idea; link `/research` | Bailey & López de Prado (2014); `docs/RESEARCH_PLATFORM.md` |
  | 26.11 Point-in-time data | Restatements, corporate actions, availability timestamps | SEC EDGAR, vendor methodology pages |
  | 26.12 Risk capacity versus tolerance | FINRA 2111 suitability; the Reg BI care obligation; OJK consumer-protection rules | finra.org 2111; 17 CFR 240.15l-1; ojk.go.id |
  | 26.13 Scam red flags | Guaranteed returns, unregistered offerings; OJK Satgas PASTI | Investor.gov alerts; ojk.go.id |
  | 26.14 Audit trails and whistleblowing | Record-keeping; Exchange Act §21F; anti-retaliation requires reporting to the SEC (*Digital Realty v. Somers*, 2018) | sec.gov/whistleblower; LII |
  | 26.15 Cybersecurity | MFA, least privilege, API-key hygiene; Reg S-P 2024 amendments; UU 27/2022 (PDP) | sec.gov release; peraturan.bpk.go.id |
  | 26.16 Supervision | FINRA 3110 binds member firms; what an individual can borrow from it | finra.org Rule 3110 |
  | 26.17 Greenwashing | SEC Names Rule 2023; EU SFDR; OJK Taksonomi Keuangan Berkelanjutan Indonesia | sec.gov; eur-lex; ojk.go.id |

- **Check:**
  - `check_courses.py conduct-compliance-essentials` is clean.
  - The exam keeps 26 questions, and each q9–q17 `lessonId` points to its lesson.
  - The exam version is bumped.

### P0-3. False platform claims and impossible instructions

| Lesson | Problem | Fix |
| --- | --- | --- |
| 24.2 | Says to name the date column `timestamp`/`date`; the importer requires `time` | Teach `time,open,high,low,close,volume` |
| 24.3 | "Upon uploading … the summary card displays …"; there is no upload page or summary card | Teach the command-line import, the "Imported N bars" output, and parity checks on the first `years × 252` bars |
| 24.4 | "Run backtest" button; "completely removing look-ahead" | Use "Run experiment"; next-open fills remove *execution* look-ahead only, and full-sample statistics still leak, which the research registry's look-ahead test catches |
| 24.5 | "$12.50 round-trip commission … $7.50 slippage" and "position sizing caps" | Basis points of notional per fill; all-in, long or cash |
| 24.6 | A Strategy-lab "Save strategy" button with SHA-256, "Version 2" and a version toggle; none exists | Rewrite around saved snapshots, and teach versioning in `/research`; rewrite the exercise, practice question and exam q6 |
| 24.7 | Factor studio described as quintile ranking; `/simulator` linked as the AMM | Describe the regressions; link `/lab?tool=factors` and `/lab?tool=amm`; fix the term, exercise, realWorld and course outcome; rewrite exam q7 (swap output is one formula) |
| 25.6 | "Upload for automated grading" and a "Downloads bar" | Describe a self-check against the rules and the reference file; files are on the course page |
| 23.5 | "Wajib … mengunggah" (upload required) | Same: self-check |
| 27.2 | `import pandas`, `df.head()`, `prices.csv` | Teach in-app lists and variables; keep pandas as a clearly labelled "on your own computer" block that runs in CPython |
| 27.3 | Change `window=3`; look for NaN | No keyword arguments; in-app `sma` uses partial windows, so there is no NaN. Teach the warm-up rule |
| 27.4 | Draw and save charts | No matplotlib in either runtime; show printed values in-app and keep matplotlib as an offline block (with `plt.legend()` and defined variables) |
| 27.5 | "38 vs 24 buy signals" can't be reproduced | Make the code count and print signals for both windows, or remove the claim |
| 27.6 | Teaches tracebacks with line numbers | The guided runtime shows one-line errors (line numbers only for SyntaxError); teach reading those, and show a CPython traceback as an aside. Add broken code to fix |
| 27.x | "Runs in your browser in under 5 ms"; "every lesson has an expected output" | Code runs on the server (~40–65 ms); only 27.1 has an expected output |
| 27 resources | "Python Beginner Cheat Sheet" links to the Strategy Lab README | Link a real cheat sheet or remove it (`python_reluctant_investor_course.py` ~line 569) |

- **Check:** follow each lesson's instructions in the running app and make sure every step can be done.

### P0-4. Wrong legal facts (Conduct & Compliance, and 12.x)

| Lesson | Wrong | Correct |
| --- | --- | --- |
| 26.2 | FINRA 5210 cited for front-running; Reg BI cited for order priority | Front running is FINRA 5270; trading ahead of customer orders is 5320; Reg BI covers recommendations only. Keep CFA VI(B) |
| 26.4 | MNPI = material ∩ non-public ∩ breach; the classifier skips materiality | MNPI = material ∧ non-public, possession-based (CFA II(A), MAR Art. 8(4)). Breach and personal benefit are US 10b-5 *liability* elements |
| 26.5 | "Under the Dodd-Frank Act and FINRA Rule 2020, spoofing is an explicit felony" | FINRA 2020 is a self-regulatory rule enforced by discipline. Dodd-Frank §747 (CEA 4c(a)(5)(C)) covers CFTC markets. Equity spoofing falls under the Exchange Act |
| 26.6 | Knight lost $440M and went bankrupt | Over $460M (SEC 2013-222); rescued with about $400M, then merged into KCG |
| 26.6, scenario-2, 12.x line 509 | Kill switch presented as a Rule 15c3-5 requirement | 15c3-5 requires credit/capital thresholds, erroneous-order controls and regulatory controls. A kill switch is industry practice. The rule binds broker-dealers with market access, not individuals |
| 26.7 | GIPS composite = "all five funds", 3.8% with no data; net of custody | Composites are defined by strategy. Net-of-fees deducts the management fee, not custody. "Net whenever gross is shown" is the SEC Marketing Rule |
| 26.1 | Prepayments described as client money creditors cannot seize | Segregation duties are sector-specific; reword as prudent ring-fencing |
| Exam q6 | "Executed prior to order entry, without broker-dealer discretion" | Rule (d)/(d)(1) allows allocating some controls; (c)(2)(iv) requires post-trade reports |
| Exam q9 | The listed best-execution factors | Use the FINRA 5310(a)(1) factors |
| Scenarios 7–9 | Test certificate trivia | Replace with compliance scenarios from 26.1–26.8 |
| Scenario 1 | The tipper's relationship is unstated | "A relative who works at the company" |

Also:
- Add an "educational, not legal advice; rules differ by jurisdiction" note to the course.
- Add Indonesian anchors where insider trading, manipulation and disclosure are taught: UU 8/1995 as amended by UU 4/2023 (P2SK), and OJK rules. Verify article numbers on peraturan.bpk.go.id.
- Fix `source`, which claims "ESMA frameworks" though the `MARKET_ABUSE` constant is unused.
- Reword the conduct description in `learning_guidance.py` (about lines 111–112) so it doesn't promise GIPS compliance.
- Add to the shared `ojk_scam` case that lenders agreed to restructure, including waivers (OJK SP 94/DHMS/OJK/XII/2022).

### P0-5. MSME 23.10 tax rules predate PP 20/2026

- **Fix:**
  - Confirm PP 20/2026 against the primary text or DJP's own pages before editing; the review relied on secondary sources (DDTC, hukumonline, pajakku, katadata).
  - Expected changes, to verify:
    - no time limit for individuals;
    - going forward, only a single-founder *perseroan perorangan* and *koperasi* qualify as entities;
    - existing CV, firma, PT and BUMDes keep the rate until their PP 55 period ends;
    - *pekerjaan bebas* income is excluded from the base but counts toward Rp4.8B.
  - Rewrite points 1 and 4, and cite "PP 55/2022 s.t.d.d. PP 20/2026".
  - Remove "Ditinjau oleh Kantor Akuntan Publik & Konsultan Pajak Terdaftar, November 2026" unless a named reviewer signs off.
  - Add PKP/PPN at Rp4.8B and marketplace PPh 22 (PMK 37/2025), if verified.
- **Unchanged and correct:** the 0.5% rate, the Rp4.8B threshold, and the Rp500M non-taxable portion for individuals.

---

## P1 — accuracy and consistency

### P1-1. Arithmetic

| Lesson | Now | Fix |
| --- | --- | --- |
| 24.1 | "150 × 30 bps = 4.5%" and "+24% → −3.2%" | 150 × 30 bps = 45%; choose numbers that reconcile |
| 24.1 | "200 trades … 0.3% gain guarantees a 100% loss" | False: gross +60%. Rewrite with a correct example |
| 24.1 realWorld | 15 bps contradicts the lesson's 30 bps | Align |
| 23.9 | "1.3× gives a 30% buffer" | Cash flow can fall 1 − 1/1.3 ≈ 23%. A revenue fall is not a cash-flow fall. Call 1.3× a bank rule of thumb |
| 23.6 | "Every sale after break-even is pure profit" | Only the contribution margin (Rp12,000 of Rp25,000) is profit |
| 23.6 code | Divides by 26 days | Use 25, to match the text |
| 23.8 | The "net" margin is really a gross margin; "eats almost the entire margin" | Say gross; the fee takes 65% of profit. Add a fee-inclusive price HPP/(1 − margin − fee) |
| MSME exam Q9 | DSCR ratio inverted; "1.25× = 25% cushion" | Cash flow ÷ debt service ≥ about 1.3×; the cushion at 1.25× is 20% |
| 26.5 | Ten orders over three prices crossing the spoofer's own $50 offer | Fix the order ladder |
| 26.1 code | Comment says a 2% trailer, but returns differ by 4 percentage points | Align |
| 25.4 | "Buys below the 52-week low" can never trigger; Enron (2001) falls outside 2006–2026; "alpha" | Fix the rule, the date and the term (survivorship bias) |
| 24.4 Excel | `AVERAGE(C2:C21)` vs `AVERAGE(C2:C51)` end on different rows | `AVERAGE(C32:C51)` vs `AVERAGE(C2:C51)` |
| 24.5 | Trade count multiplied by a round-trip fee | Count round trips (fills ÷ 2) |
| 24.3 | 252 trading days for IDX | IDX has about 239; don't claim 252 |

### P1-2. Data Hygiene capstone (25.6) and its validator

- Make the practice file actually contain the "five defect classes": a currency defect, a genuine day/month ambiguity, and a real missing period (the balances are currently continuous).
- Regenerate `cleaned_transactions_reference.csv` to match. Add the `currency` column if 25.2 keeps calling it mandatory.
- Keep `content/templates/` and `frontend/public/templates/` identical.
- **Validator** (`backend/quanta/services/learning.py`, `validate_capstone`): it reports "taxonomy: passed" and "all 5 defect classes" while checking only ISO dates, an `amount` column the template lacks, and repeated IDs. Make it check:
  - ISO dates;
  - the allowed category taxonomy;
  - numeric amounts with no currency text;
  - composite-key duplicates;
  - the template's columns.
  It must not report checks it doesn't run. Update `backend/tests/test_course_expansion.py`.

### P1-3. MSME capstone (23.5) validator

- Report a negative closing balance as a cash-gap warning instead of rejecting it; the lesson's aim is to reveal cash gaps.
- Accept `50.000.000` and `Rp 50.000.000` (the current parser only strips commas).
- Document closing = opening + inflow − outflow in the lesson.
- Make the template show a seasonal dip if realWorld promises one.

### P1-4. Exam `lessonId` tags

- Data Hygiene q3–q6 point one lesson too high, and 25.6 has no question. These tags drive "Review lesson" links on results pages.
- All nine Conduct scenarios are mapped by `modules[min(j, …)]`. Point each to the lesson it tests.
- MSME Q4 tests 23.3 but is tagged 23.4.

### P1-5. Duplicate and composite-key teaching (25.3)

`=COUNTIF(A:A,A2)>1` and `df.duplicated()` ignore the composite key. Teach `COUNTIFS` and `duplicated(subset=[…], keep=False)`.

### P1-6. Exam questions on untaught material

- Conduct: q8 (pre-clearance, restricted lists), q12, q14 (audit logs) and q16 (restricted list).
- MSME: Q7 (DSO/DPO).
- Python: q6 (IndexError).

Either teach the material in the lesson or replace the question.

---

## P2 — sourcing, language, metadata

### P2-1. References

Replace bare homepages and invented document titles with specific pages:

- **MSME:** four Kemenkop UKM titles pointing at `kemenkopukm.go.id`; four BI titles pointing at the BI UMKM landing page; "OJK · Buku Saku … UMKM"; DJP/Kemenkeu homepages; the OECD URL that returns 403.
- **Conduct:** "U.S. SEC · Regulatory Guidance and Compliance Policies" → sec.gov on 26.9–26.17; 26.4, 26.5, 26.6 and 26.8 homepages; the 26.3 title that doesn't match its page.
- **24.x:** cfainstitute.org, sec.gov, acm.org and finra.org homepages; FINRA 5310's title is "Best Execution and Interpositioning".
- **27.6:** AddressSanitizer (a C tool) and a non-existent "Software Carpentry … Modular Design".

Also note that Kemenkop UKM was split in October 2024; use the current ministry names.

### P2-2. Real-world pairings

Change the case IDs in `case_applications_expansion.py`, or rewrite the connection text, where the case does not fit:

| Lessons | Current case |
| --- | --- |
| 23.4, 23.10 | `bps_growth` |
| 23.2 | `household` |
| 23.9 | `ojk_scam` |
| 23.7, 23.8 | `warung` |
| 24.x | statsmodels, GIPS, EDGAR, Knight, AWS |
| 26.2 | BCA split |
| 26.5 | Flash Crash as spoofing |
| 26.8 | SQLite |
| 26.12 | SVB |
| 26.14 | OWASP |
| 26.15 | EIP-155 |
| 26.16 | Super Micro with FINRA 3110 |
| 26.17 | Enron as greenwashing |

### P2-3. Language (MSME)

The content is Indonesian, but titles, objectives, realWorld text and glossary terms are English. Translate them. Add an MSME override for the shared glossary term *Liquidity*: it currently gives the market sense, and the course needs business liquidity.

### P2-4. Metadata and small slips

| Course | Lesson minutes | `estimated_minutes` |
| --- | --- | --- |
| MSME | 190 | 180 |
| Data Hygiene | 67 | 60 |
| Conduct | 460 | 420 |

Reconcile them. Other slips:
- `exercise` duplicates `exercises[0]`, and most lessons have only one practice question; older courses have 2–3.
- The Conduct docstring says "25-question".
- MSME "5 kolom" is followed by 6 names.
- Inconsistent time claims.
- "Terbuka, tanpa batasan waktu" vs `minutes: 30`.
- "a opening float".
- Mixed decimal separators.

### P2-5. `docs/MSME_COURSE_OUTLINE.md`

Make it match the lessons. Currently:
- every worked example differs, and the 23.2 numbers don't add up;
- template names are wrong;
- "Graham & Dodd" is credited for *The Intelligent Investor*;
- "SPT 1770 Lampiran III" is outdated;
- PMK 164/2023 is cited for marketplace withholding;
- the "Completed & Formally Verified" sign-off names no reviewer.

---

## P3 — platform and tests

### P3-1. E2E specs broken by the expansion

The full run had 136 pass and 12 fail; a rerun of the six affected files had 51 pass and 16 fail and took 1.2 hours. Diagnose each failure and decide whether the spec or the app should change:

- `applied-courses.spec.ts`: simulator-workshop and intelligent-investor units/downloads; mobile course cards (count 0).
- `book-courses.spec.ts`: Trading fundamentals (expected 4, got 0); Security Analysis worksheet output ("Expected value per share: 11.08"); mobile; every expanded lesson (expected 2, got 3 practice cards).
- `c-lab.spec.ts`: edits, download and reset.
- `certifications.spec.ts`: single-page print.
- `course-readability.spec.ts`: `.prose ol` now matches 2 elements; curriculum search and mobile navigation.
- `workspace.spec.ts:21`: lesson 1.1 now prints "Base margin of safety: 40.0 %".

The econometrics, strategy-lab and c-hpc "every lesson renders" loops time out under load but pass when the machine is quiet. Run e2e alone, or raise those tests' timeouts.

### P3-2. `/pathways` overflows on phones

31 px of horizontal scroll at 390 px wide (`frontend/src/features/learning/pages/CourseMap.tsx`, `course-map.css`).

### P3-3. Capstone upload UI (optional)

The validators have an API but no page. Either build a minimal upload on the course page for MSME and Data Hygiene, or keep the lessons' self-check wording (see P0-3).

---

## Definition of done

1. `check_courses.py` reports 0 problems for all five courses.
2. `python3 content/authoring/curriculum.py` gives no diff after a fresh regeneration.
3. Every exam changed since `13594ff` has a bumped `version`.
4. The backend suite passes, run alone: `make -s -C backend/engine && backend/.venv/bin/python -m pytest backend/tests -q`.
5. Frontend: `npx tsc -b`, `npx vitest run` and `npx vite build` pass.
6. The full e2e suite passes on a quiet machine.
7. A reader of each lesson can do every instruction in the running app.
8. Every legal and tax claim cites a specific primary page.
