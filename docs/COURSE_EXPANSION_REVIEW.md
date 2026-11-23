# Review of the five expansion courses — November 23, 2026

Scope: the five courses added in `f36a357` ("implement 5 expansion courses and certificate subsystem"), pulled to `feat/courses` at `07395e7`.

| Course | ID | Lessons | Final exam |
| --- | --- | --- | --- |
| Financial Literacy for MSMEs | `msme-financial-literacy` | 23.1–23.10 | 10 questions, pass 70 |
| From Spreadsheet to Strategy Lab | `spreadsheet-to-strategy-lab` | 24.1–24.7 | 7 questions, pass 70 |
| Data Hygiene for Investors | `data-hygiene` | 25.1–25.6 | 6 questions, pass 70 |
| Conduct & Compliance Essentials | `conduct-compliance-essentials` | 26.1–26.17 | 26 questions, pass 80 |
| Python for the Reluctant Investor | `python-reluctant-investor` | 27.1–27.6 | 6 questions, pass 70 |

Fixes belong in the authoring files, then `npm run content:build`:

- Lesson text and exams: `content/authoring/msme_course.py`, `spreadsheet_to_strategy_course.py`, `data_hygiene_course.py`, `conduct_compliance_course.py`, `python_reluctant_investor_course.py`.
- Real-world sections: `content/authoring/case_applications_expansion.py`.
- Shared glossary and course descriptions: `content/authoring/learning_guidance.py`.

Evidence tags: **[P]** primary source fetched, **[S]** secondary source, **[R]** reviewer knowledge (not fetched; treat as unverified), **[C]** recomputed or executed locally.

## Resolution status — November 23, 2026

Fixed:
- Answer positions are rebalanced at build time (`content/authoring/curriculum.py`, `_rebalance`). Each question's options are rotated deterministically so the key's slot depends on the question, and every new exam spreads its keys across options A–C. All five exams moved to `version: 2`.
- `conduct-final-scenario-3`: the key now points to the correct option, and the premise is reworded.
- The 26.3 figures now read $951,838, $542,713, $409,125 and about 43%.
- 24.4: `sma_20` changed to `sma_50`.
- 27.5: `LOOKBACK_WINDOW` changed to the code's `lookback_window`.
- The 25.6 practice CSV has its unquoted date quoted.
- The sandbox now applies f-string format specs with CPython semantics (bounded width; numbers and text only).

Still open (§8 items 2–10, except the parts above):
- correct option being the longest
- false platform claims and impossible instructions in 24.x, 25.6 and 27.x
- stub lessons 26.9–26.17
- legal and tax corrections (26.2, 26.4–26.6, kill switch, 23.10)
- the remaining arithmetic fixes
- `lessonId` tags, references and pairings
- e2e specs and the `/pathways` overflow

## Verdict

The courses build, render and pass the existing automated tests. They are not ready to stand behind a certificate:

- **Assessments are guessable.** Answer keys are positional, and the correct option is almost always the longest.
- **Several lessons are wrong.**
  - Wrong answer key: Conduct & Compliance scenario-3.
  - Wrong arithmetic in worked examples: 24.1, 26.3, 23.9.
  - Misstated law: FINRA 5210, Reg BI, a FINRA rule called a "felony", the kill switch, Knight Capital.
  - Out-of-date Indonesian tax rules: 23.10 vs PP 20/2026.
- **Platform claims are false.** Several lessons describe app features that do not exist, such as Strategy-lab versioning, a quintile Factor Studio, or CSV upload, or tell learners to run code the sandbox rejects.
- **Nine lessons have no content.** Conduct & Compliance 26.9–26.17 are template stubs, but the exam still tests them.

## 1. Automated checks

| Check | Result |
| --- | --- |
| Backend suite (alone, engine built) | 1,160 passed, 0 failed |
| Catalog regeneration (`content/authoring/curriculum.py`) | Byte-identical to the committed `curriculum.json` |
| Frontend | `tsc -b`, 130 vitest tests and the Vite production build passed |
| Structure | Lesson and question IDs unique. Every answer key is in range with distinct options. Internal links resolve. All 46 lesson code blocks run in the guided runtime [C] |
| Page render (Chrome, 1440 px and 390 px) | All 60 new-course routes load with no page errors and no horizontal overflow: course pages, lessons, exams and certificate pages. Outside the new courses, `/pathways` (the new course map) overflows by 31 px at 390 px |
| Full e2e suite | 136 passed, 12 failed. Most failures come from the expansion changing shared lesson pages without updating the specs: extra practice cards (expected 2, got 3), a second `.prose ol` (strict-mode violation), changed worksheet output text and missing counts. `workspace.spec.ts` was already failing (lesson 1.1 text). A rerun of the failing files also showed timeouts on lesson titles, so some failures may be timing; see the appendix |

## 2. Cross-cutting problems

### 2.1 Guessable assessments (all five courses)

Measured over each course's exercises and final exam [C]. The established courses spread answers roughly a third per position.

| Course | Exercise answer positions | Exam answer positions | Correct option is the longest |
| --- | --- | --- | --- |
| MSME | 1× A, 9× B, 1× C | 4× A, 6× B | 17 / 21 |
| Spreadsheet to Strategy | 7× B | 4× A, 3× B | 13 / 14 |
| Data Hygiene | 6× B | 6× A | 12 / 12 |
| Conduct & Compliance | 16× B, 1× C | 19× A, 5× B, 2× C | 42 / 43 |
| Python for the Reluctant Investor | 6× B | 6× A | 9 / 12 |
| *Reference: Strategy lab* | 20 / 22 / 22 | 22 / 21 / 21 | — |

"Always A" scores 100% on the Data Hygiene and Python finals. "Always the longest option" passes every new final. These finals now feed the certificate pipeline.

Fix:
- Rebalance option order deterministically per question.
- Rewrite distractors so length carries no signal.
- Add the missing practice questions: one per lesson, where older courses have two or three.

### 2.2 The sandbox silently ignores f-string format specs

`backend/quanta/execution/sandbox_worker.py` (the `ast.JoinedStr` branch, about lines 430–432) converts each value with `str()` and drops the format spec. `f"{8000000:,}"` prints `8000000`, and `f"{2.03125:.2f}"` prints `2.03125` [C]. The module says unsupported syntax fails closed, but this fails open.

The older courses avoid format specs. The new ones use them in 12 modules, so printed output disagrees with the lesson text:
- 23.1: `Rp 8000000`
- 23.6: `19.23076923076923 porsi/hari`
- 26.3: `$951837.5320273875`
- 27.1: expected `Rp 2,500`

Fix: apply `format(value, spec)` with a bounded spec, or refuse format specs with a clear error.

### 2.3 Real-world sections and references

- **Language.** Case sections and glossary terms are in English inside Indonesian lessons (MSME course).
- **Cases that don't fit.** Several cases are attached to unrelated lessons:
  - GDP release → cash-flow buckets and tax
  - consumer-loan fraud → DSCR
  - BCA stock split → front-running
  - SQLite atomic commit → conduct charter
  - Enron → greenwashing
- **Homepage-only citations.** Many references point to a bare homepage (`kemenkopukm.go.id`, `bi.go.id/id/umkm`, `sec.gov`, `cfainstitute.org`, `finra.org`, `acm.org`) and carry document titles that do not exist there. For example, "U.S. SEC · Regulatory Guidance and Compliance Policies" is cited by 26.9–26.17.
- **Wrong sense.** The shared glossary entry *Liquidity* gives the market-trading sense, but the MSME lessons mean business liquidity.

### 2.4 Metadata drift

| Course | Lesson minutes | `estimated_minutes` |
| --- | --- | --- |
| MSME | 190 | 180 |
| Data Hygiene | 67 | 60 |
| Conduct & Compliance | 460 | 420 |

Other metadata issues:
- Each lesson's `exercise` and `exercises` hold the same single question.
- The Conduct docstring says "25-question" while the exam has 26.

## 3. Financial Literacy for MSMEs (23.x)

Arithmetic, code and every answer key check out [C]. The problems are tax currency, two reasoning errors and sourcing.

### Wrong

1. **23.10 tax rules predate PP 20/2026** (`msme_course.py` ≈ lines 690–732, 915, 946; course description and outcomes; `docs/MSME_COURSE_OUTLINE.md` §4).
   - What changed:
     - PP 20/2026, reported in force from 22 April 2026, amends PP 55/2022.
     - Individuals no longer have a time limit for the 0.5% final rate.
     - Among entities, only a single-founder *perseroan perorangan* and *koperasi* qualify going forward.
     - Existing CV, firma, ordinary PT and BUMDes keep the rate only until their PP 55 period ends.
     - Income from *pekerjaan bebas* is excluded from the 0.5% base but counts toward the Rp4.8B threshold.
   - Where the lesson is wrong:
     - Point 4, "untuk badan usaha, PPh Final 0,5% tetap berlaku dari rupiah pertama", is wrong for a new CV or PT.
     - Point 1 is too broad for service providers.
     - The callout "Ditinjau oleh Kantor Akuntan Publik & Konsultan Pajak Terdaftar, November 2026" names no reviewer and should be removed until one signs off.
   - Sources: [S] DDTC, hukumonline, pajakku and katadata; DJP article "PP 20/2026: Tarif PPh 0,5% bagi UMKM Orang Pribadi Berlaku Selamanya" (search result only). The primary PDF on jdih.kemenkeu.go.id is a scanned image and could not be read. **Confirm against the primary text before editing.**
   - Unverified: the koperasi transition and spouse aggregation details.
   - Still correct: the 0.5% rate, the Rp4.8B threshold and the Rp500M non-taxable portion for individuals (PP 55 Pasal 60(2); UU PPh Pasal 7(2a) as amended by UU HPP).
2. **23.9 "30% buffer".**
   - At DSCR 1.3×, operating cash flow can fall 1 − 1/1.3 = 23.1% before the instalment is uncovered, not 30% [C].
   - The worked example also treats a 30% *revenue* fall as a 30% *cash-flow* fall.
   - The 1.3× threshold is a bank rule of thumb, not a "prudential threshold".
3. **23.6.** "Setelah biaya tetap tertutup, penjualan berikutnya adalah murni laba bersih." Only the contribution margin (Rp12,000 of each Rp25,000 sale) is profit.

### Misleading or outdated

- **23.6:** the code divides by 26 working days (19.2 per day); the text uses 25 (20 per day).
- **23.8:** the "net" margin that must cover rent and platform fees is a gross margin; exam Q8 repeats this. "Memakan hampir seluruh margin" overstates it: the fee takes 65% of profit [C]. Add a fee-inclusive price, e.g. HPP / (1 − margin − fee).
- **Exam Q9:** the DSCR ratio is inverted in the option and contradicts the lesson's 1.3×. The explanation's "1.25× = 25% cushion" is wrong; the real cushion is 20%.
- **23.10:** says tax compliance unlocks the NIB. The NIB is issued at OSS registration and does not depend on tax compliance.
- **23.10:** the sandbox blurb promises a month-of-crossing calculation the code doesn't perform.
- **23.4:** the code shows positive operating cash flow, undercutting the lesson's −3 / −2 / +25 example.
- **23.1:** "rasio kas cepat (quick cash ratio)" describes days of cash on hand, not the quick ratio.
- **23.5 capstone:**
  - The lesson says "wajib … mengunggah", but no frontend calls `POST /api/v1/courses/{id}/capstone`.
  - The validator rejects any negative closing balance, which contradicts the lesson's aim of revealing cash gaps.
  - The validator parses amounts with `.replace(",", "")`, so Indonesian-format "50.000.000" is rejected.
- **Ministry name:** "Kemenkop UKM" was split into the Ministry of Cooperatives and the Ministry of MSMEs in October 2024.

### Gaps for the stated audience

- PPN/PKP registration on crossing Rp4.8B.
- Marketplace PPh 22 withholding under PMK 37/2025, postponed to 1 November 2026.
- KUR rates and limits.

### Outline drift

`docs/MSME_COURSE_OUTLINE.md` no longer matches the course:
- Every worked example differs from the lessons, and the 23.2 outline numbers don't add up.
- Template file names differ.
- *The Intelligent Investor* is credited to "Graham & Dodd".
- "SPT 1770 Lampiran III" is outdated from tax year 2025.
- "PMK 164/2023 marketplace withholding" is garbled: marketplace collection is PMK 37/2025.
- The "Completed & Formally Verified" sign-off names no reviewer.

## 4. Conduct & Compliance Essentials (26.x)

### Wrong

1. **`conduct-final-scenario-3` answer key is wrong** [C].
   - The stored key is `answer: 1`, "Because computing gross returns requires advanced calculus". It should be `0`.
   - The premise is also off. GIPS net-of-fees deducts the investment management fee, not custody [S: GIPS Q&A]. The "net whenever gross is shown" rule comes from the SEC Marketing Rule, 17 CFR 275.206(4)-1(d)(1), whose net definition may *exclude* custodian fees [P].
2. **26.3 worked example.**
   - The text says $935,000 / $516,000 / $419,000, "over 45%".
   - Recomputed: 100,000 × 1.078³⁰ = $951,838 and 100,000 × 1.058³⁰ = $542,713, a difference of $409,125, or 43.0% [C]. The lesson's own code prints these recomputed values.
3. **26.4 MNPI is defined with a "breach of duty" element.**
   - The formula reads "Material ∩ Non-Public ∩ Breach".
   - The classifier returns "PERMISSIBLE" for any undisclosed tip obtained without a breach, and never tests materiality.
   - CFA Standard II(A) is possession-based [P]; EU MAR Art. 8(4) is similar [S]. Breach is a US 10b-5 liability element, not part of the definition.
   - This contradicts the verified trading-ethics course (`trading_ethics.py:332`).
4. **26.2 cites FINRA Rule 5210 for front-running.**
   - Rule 5210 is "Publication of Transactions and Quotations" [P].
   - Front running is Rule 5270, and trading ahead of customer orders is Rule 5320 [P].
   - This contradicts 12.x, which uses 5210 correctly.
5. **26.2 attributes order priority to Reg BI.**
   - Reg BI (17 CFR 240.15l-1) governs recommendations to retail customers and has no trade-sequencing rule [P].
   - Keep CFA VI(B); cite FINRA 5320 and 5270.
6. **26.5: "Under the Dodd-Frank Act and FINRA Rule 2020, spoofing is an explicit felony."**
   - FINRA 2020 is an SRO conduct rule enforced by FINRA discipline, not a crime [P].
   - Dodd-Frank §747 (CEA 4c(a)(5)(C)) covers CFTC-regulated markets [P]. The lesson's example is an equity order, which falls under the Exchange Act [R].
7. **26.6 Knight Capital.**
   - "Losing $440 million and bankrupting the firm" is wrong twice.
     - The SEC says more than $460 million [P].
     - Knight was rescued with about $400M of investor capital and merged into KCG, not bankrupted [S].
   - This contradicts the shared `knight` case, which says more than $460M.
8. **The kill switch is presented as a Rule 15c3-5 requirement.** This affects 26.6 and `conduct-final-scenario-2`.
   - 17 CFR 240.15c3-5 requires credit and capital thresholds, erroneous-order price and size controls, and regulatory controls. It has no kill-switch or under-one-second requirement [P].
   - The trading-ethics course (12.x, line 509) makes the same implied overstatement.

### Missing content

- **26.9–26.17 are template stubs** (`conduct_compliance_course.py` ≈ lines 586–652).
  - All nine share identical boilerplate (~1,000 characters each), the formula "Compliance Metric = … = 100%" and the code `rule_verified = True` [C].
  - Their subtitles promise FINRA 5310, whistleblower protection, FINRA 3110 and greenwashing; none is taught.
  - Exam questions q9–q17 test this untaught material.

### Misleading or outdated

- **Wrong jurisdiction.** The audience tags are Indonesian MSMEs (Rp and BBCA examples, `language: ["en","id"]`), yet there is no Indonesian law at all:
  - none of POJK, UU 8/1995 / UU 4/2023 (P2SK), PPATK, APU-PPT or FATF;
  - no 10b5-1, Reg FD, MAR, record-keeping or whistleblowing rules;
  - no "educational, not legal advice" disclaimer.
  - The `source` claims "ESMA frameworks", but the `MARKET_ABUSE` constant is unused.
- **q9:** the best-execution factors match the FINRA 5310.09 review factors and MiFID wording ("settlement"), not the 5310(a)(1) factors [P].
- **q6:** misreads 15c3-5. Rule (d)(1) allows allocating some controls to a broker-dealer customer, and (c)(2)(iv) requires *post*-trade reports [P].
- **26.6:** applies 15c3-5 to individual traders. The rule binds broker-dealers with market access [P].
- **26.7 GIPS example:** composites are "all five funds combined", and the 3.8% figure has no data behind it. The fee definition includes custody.
- **26.1:** treats an ordinary customer prepayment as client money held in custody that creditors cannot seize. Segregation duties are sector-specific [R].
- **Exam lesson tags:** all nine scenario questions carry the wrong `lessonId`, because of the `modules[min(j, …)]` mapping.
- **Scenarios 7–9** test the certificate platform (pass mark, score bands, opt-out), not compliance. Their keys do match `services/certificates.py`.
- **Real-world pairings:**
  - Super Micro (an issuer) is paired with FINRA 3110, which binds member firms.
  - The Flash Crash report is used as a spoofing example; it is about liquidity.
  - A high order-to-cancel ratio is called a violation, whereas 12.x correctly requires assessing intent.
- **Shared `ojk_scam` case:** omits that the OJK release says lenders agreed to restructure, including waivers [P].

### Weak

- Many 26.x references are homepages with non-existent document titles.
- The 26.3 reference title doesn't match its page.
- 26.2's code prints "Client priority strictly respected" with no fill data.
- 26.5's example has ten orders spread over three prices, which would cross the spoofer's own offer.
- 26.1's code comment says 2% but the returns differ by 4 percentage points.
- 26.6 states a counterfactual as fact.
- q8, q12, q14 and q16 test material their lessons never teach.
- Universal "musts" that are jurisdiction-specific: WORM-only audit logs, annual penetration tests, a blanket restricted-list ban.
- Wording that reads as legal advice: "explicit felony", "immediate grounds for termination".

### Checked and correct

- 26.1 arithmetic.
- The 26.3 code output and its exercise's "over 40%".
- CFA VI(B) and the mosaic-theory wording.
- Materiality as "reasonable investor / total mix".
- The spoofing definition (CEA wording).
- Keys q1, q2, q4, q5, q7, q10, q11, q13 and scenarios 4–6.
- The 15c3-5 credit and price controls.
- GIPS composite completeness.
- Knight's 45 minutes and more than 4M orders.
- The Super Micro penalty and date.
- The certificate score bands and opt-out behaviour.

## 5. From Spreadsheet to Strategy Lab (24.x)

### Wrong

- **24.1 worked example.**
  - "150 × 30 bps = 4.5%" is 45% [C], and neither figure gets from +24% to the stated −3.2%.
  - "200 trades … average gross gain 0.3% … guarantees a 100% loss after fees" is false: gross is +60%, and net stays positive at 15–25 bps per round trip [C].
  - The real-world section's 15 bps contradicts the lesson's 30 bps.
- **24.2:** tells learners to name the date column `timestamp`/`date`. `backend/scripts/import_data.py` requires `time` ("Missing required OHLCV columns") [C].
- **24.3:** "Upon uploading … the summary card displays `252 bars | … | Last: 10,250`."
  - There is no upload in the UI; import is a command-line script, and no such card exists.
  - IDX has about 239 trading days, not 252 [S].
- **24.4:** `data['close'] > data['sma_20']` fails with `KeyError: 'sma_20'`; only `sma_50` and `sma_200` exist [C]. The button is "Run experiment", not "Run backtest". The Excel comparison averages windows ending on different rows.
- **24.5:** says Strategy Lab applies "$12.50 round-trip commission … $7.50 slippage". The engine charges basis points of notional per fill (5 bps commission, 3 bps slippage by default). "Position sizing caps" don't exist: the lab is all-in, long or cash.
- **24.6 versioning:** describes a Strategy-lab "Save strategy" button with SHA-256 on edit, "Version 2" and a version toggle. None exists. Saving stores a named snapshot. Real versioning lives in the research registry (`/research`), which hashes only the source text when a run is queued. The exercise, practice question and exam q6 rest on this.
- **24.7:** describes Factor Studio as ranking stocks into quintile portfolios. It fits CAPM and Fama-French regressions on synthetic returns. `/simulator` is the paper-trading terminal; the AMM is at `/lab?tool=amm` and Factor Studio at `/lab?tool=factors`.

### Misleading

- **24.7 AMM:** routing, arbitrage and fee yield aren't simulated. Exam q7's "cannot be replicated in a spreadsheet" is false.
- **24.1:** the objective names survivorship bias, which the body never covers.
- **24.4:** "completely removing look-ahead" overclaims. The sandbox accepts full-sample statistics; only the research registry's look-ahead test catches them.
- **24.3:** Strategy Lab loads the *earliest* years × 252 bars, so a longer file's last close won't match the spreadsheet.
- **24.5:** the trade count includes both buy and sell fills, so multiplying it by a round-trip fee double-counts.

## 6. Data Hygiene for Investors (25.x)

### Wrong

- **The 25.6 capstone file is malformed.** `messy_transactions_practice.csv` line 5 (`Feb 04, 2026,…`) has an unquoted comma. pandas raises "Expected 7 fields in line 5, saw 8" [C], and spreadsheets shift that row one column right.
- **25.6 claims "five defect classes", but not all are present:**
  - there is no currency defect;
  - the date gap is not a missing period, since balances are continuous;
  - the only slash date can't show day/month confusion.
- **25.6 tells learners to upload for automated grading.** No frontend calls the capstone endpoint, and there is no "Downloads bar".
- **Exam lesson tags:** q3–q6 point one lesson too high, so "Review lesson" links go to the wrong lesson. 25.6 has no exam question.
- **Exam q3:** the keyed option says "remove all punctuation", which turns $1,200.50 into 120050.

### Misleading

- **Capstone validator:** it reports "taxonomy: passed" and "all 5 defect classes" while checking only ISO dates, an `amount` column the template doesn't have, and repeated IDs. Files with unfixed `OpEx`, `Rp 5.000.000` amounts or exact duplicate rows pass [C].
- **25.3 duplicates:** `=COUNTIF(A:A,A2)>1` and `df.duplicated()` ignore the composite key. Use `COUNTIFS` and `subset=[…], keep=False`.
- **25.4:**
  - "buys stocks below their 52-week low" can never trigger;
  - Enron (2001) falls outside the 2006–2026 window;
  - the 7.5% gap is survivorship bias, not alpha.
- **Unsourced statistics:** 80% (25.1) and over 50% (25.2).
- **25.6 vs 25.2:** the cleaned reference lacks the `currency` column that 25.2 calls mandatory.

### Checked and correct

Applying the course's own cleaning rules reproduces `cleaned_transactions_reference.csv` byte for byte, and its balances are continuous [C].

## 7. Python for the Reluctant Investor (27.x)

### Wrong (instructions learners cannot follow in the app)

- **27.2:** `import pandas` is rejected ("Imports are limited to math and the guided numpy subset"). There is no `df.head()` to change and no `prices.csv` [C].
- **27.3:** there's no `window=3` to change; keyword arguments are rejected. The in-app `sma` never produces the NaN the lesson tells learners to look for.
- **27.4:** charts can't be drawn or saved; there is no matplotlib in either runtime.
- **27.5:** "Change line 3 to `LOOKBACK_WINDOW = 30`" breaks the script, because the code only has a lowercase `lookback_window` [C]. The "38 vs 24 buy signals" example can't be reproduced, since no signals are printed.
- **27.1:** the expected output "Rp 2,500" prints as "Rp 2500" (see 2.2).
- **The course resource "Python Beginner Cheat Sheet"** links to the Strategy Lab project README.

### Misleading

- **27.6:** the sandbox shows one-line errors without tracebacks or line numbers, except for SyntaxError.
- **"Runs in your browser in under 5 ms":** code runs on the server, measured at 38–65 ms.
- **Reading guide:** "every lesson has an expected output" is false; only 27.1 has one, and the UI does not show it.

### Checked and correct

The arithmetic (25% / 50%, 105.4 / 110 / 109.0, 106.71) and keys q1–q5 [C].

## 8. Recommended fix order

1. **Wrong answer key:** fix `conduct-final-scenario-3`.
2. **Answer bias:** rebalance option order and distractor length in all five courses.
3. **Certificates:** keep these courses off certificates until steps 1–5 are done.
4. **Technical courses:** rewrite every false platform claim and impossible instruction (24.2–24.7, 25.6, 27.2–27.6). Fix the malformed 25.6 practice CSV.
5. **Content:** write 26.9–26.17 or drop them along with exam questions q9–q17.
6. **Legal and tax facts:** correct 26.2, 26.4, 26.5, 26.6 and the kill switch (also in 12.x line 509). Bring 23.10 up to PP 20/2026 after checking the primary text.
7. **Arithmetic:** fix 24.1, 26.3, 23.9, 23.6 and 23.8.
8. **Sandbox:** support or refuse f-string format specs (`sandbox_worker.py`).
9. **Labels and links:** fix exam `lessonId` tags (25.x q3–q6, 26.x scenarios), references and real-world pairings.
10. **E2E:** update the specs broken by the expansion, then fix the `/pathways` overflow at 390 px.

---

## Appendix A — e2e failures

First full run: 136 passed, 12 failed in 16.2 minutes.

A rerun of the six affected spec files took 1.2 hours (51 passed, 16 failed). Several tests hit the 45-second timeout, so some failures may be timing rather than content. The rerun shows the following:

- **Specs asserting old content:**
  - expected 2 practice cards, got 3;
  - `.prose ol` resolves to 2 elements;
  - changed worksheet output ("Expected value per share: 11.08");
  - card counts of 0.
- **Not found within the timeout:** lesson titles in the econometrics, strategy-lab and c-hpc "every lesson renders" loops.
- **Assertions returning false:** C lab download and reset, and certificate single-page print.
- **Already failing:** `workspace.spec.ts` (lesson 1.1 text changed in `36a8c4b`).

## Appendix B — full audit of courses 24, 25 and 27

### Audit of courses 24, 25 and 27

**Scope.** I edited no files and ran no test suites. The catalog JSON matches the authoring builders for content, code and exams. Only `references`, `terms` and `realWorld` differ, because the pipeline adds them.

**Method.** Every lesson's `code` was run through `quanta.execution.runner.run` on `strategy_data(generate(DatasetParams()),50)`. I also ran negative snippets for each instruction a learner is told to follow. The templates were loaded with real pandas. The capstone validator was re-implemented inline.

**Convention.** "Guided runtime" means the default sandbox. Its run bar shows "Guided Python · 2s limit".

---

### Course 24: From Spreadsheet to Strategy Lab

#### WRONG

**W1 · 24.1 worked example**
- Text: "150 round-trip trades generate $150 \times 30\text{ bps} = 4.5\%$ … net return collapses from +24% to −3.2%."
- Problem: 150 × 30 bps = 4,500 bps = **45%**, not 4.5%. Neither figure gets you from +24% to −3.2%: 24 − 45 ≈ −21%, and 24 − 4.5 = +19.5%.
- Fix: "150 × 30 bps = 45% of friction. +24% gross becomes roughly −21% net, before any next-open timing effect." Alternatively, change the trade count or the costs until the numbers reconcile.

**W2 · 24.1 idea #2**
- Text: "200 trades a year with an average gross gain of 0.3% … guarantees a 100% loss after trading fees."
- Problem: gross is 200 × 0.30% = 60%. Net stays positive at the course's own costs: 15 bps gives +30%, 25 bps gives +10%, 30 bps gives 0%. Fees of this size cannot produce a 100% loss.
- Fix: "average gross gain 0.10%, round-trip cost 0.15% → −0.05% per trade ≈ −10% a year."

**W3 · 24.1 realWorld walkthrough**
- Text: "deducting 15 bps round-trip friction reduces gross return from +24% to negative."
- Problem: 150 × 15 bps = 22.5%, which leaves about +1.5%. The walkthrough also contradicts the lesson body's 30 bps.
- Fix: align on a single cost figure and recompute.

**W4 · 24.2 column names**
- Text: "`timestamp` (or `date`)". Work-through step 2: "Standardize column headers to lowercase: `date`, `open`, …".
- Problem: the importer requires a column named `time` (`backend/scripts/import_data.py:2,25-27`). A learner who follows the lesson gets "Missing required OHLCV columns." The lesson's own code maps the date to `'time'`.
- Fix: tell learners to name the column `time`, in ISO YYYY-MM-DD.

**W5 · 24.3 import and summary card**
- Text: "Upon uploading to Strategy Lab, the summary card displays: `252 bars | 2026-01-02 to 2026-12-30 | Last: 10,250`." Step 2: "Load the dataset in Strategy Lab."
- Problem: the UI has no upload. Import is the CLI `import_data.py`, and the sandbox only says "Import an OHLCV CSV using the instructions in How Quanta works" (`Sandbox.tsx:247`). The importer prints only `Imported N bars to <path>`. The only summary is the Console line "N bars · M fills · final equity" (`Sandbox.tsx:665`), which shows no date span and no last close.
- Fix: describe the real flow:
  1. Run the import CLI, or have an operator run it.
  2. Choose Data source → Historical data and pick the symbol.
  3. Read the bar count from the Console tab and the last close from the Market tab.

**W6 · 24.3 trading-day count**
- Text: "252 trading days of BBCA prices … 2026-01-02 to 2026-12-30."
- Problem: the IDX 2026 calendar has **239** trading days according to media reports of the BEI calendar (Bisnis.com, Tirto). I did not fetch the official BEI PDF. 252 is the US annualization convention.
- Fix: use 239 rows, or make the example a US stock.

**W7 · 24.4 `sma_20`**
- Text (worked example): "In Strategy Lab, `data['close'] > data['sma_20']` produces the exact same boolean array."
- Run result: `SandboxError: KeyError: 'sma_20'. … (available: 'close','high','low','open','returns','sma_200','sma_50','volume')`.
- Fix: `data['close'] > sma(data['close'], 20)`.

**W8 · 24.4 button label**
- Text: "Click **Run backtest**."
- Problem: the button is **Run experiment** (`Sandbox.tsx:464`).

**W9 · 24.4 Excel formula in the code comment**
- Text: `=IF(AVERAGE(C2:C21) > AVERAGE(C2:C51), 1, 0)`.
- Problem: the two windows end on different rows (rows 2–21 versus rows 2–51). This is not a 20/50 crossover at any single date.
- Fix: in row 51, `=IF(AVERAGE(C32:C51)>AVERAGE(C2:C51),1,0)`, dragged down.

**W10 · 24.5 cost model**
- Text: "In Strategy Lab, the engine applies standard institutional assumptions: $12.50 round-trip commission per trade and $7.50 estimated slippage." The code also labels its result "Strategy Lab Net PnL".
- Problem: the engine charges **bps of notional on every fill**, with defaults of commission 5 bps and slippage 3 bps (`analytics.py:44-45, 209-236`). It has no flat-dollar costs.
- Fix: present the $1,500/$60 example as a generic spreadsheet calculation. Then show the Lab's version, for example 8 bps per fill × 2 fills on $10,000 ≈ $16 per round trip.

**W11 · 24.5 driver #3**
- Text: "Position Sizing Caps: Spreadsheets often reinvest 100% of capital … ignoring cash reserves and borrow fees."
- Problem: Strategy Lab also commits all cash at each entry (`analytics.py:215-217`; `RESEARCH_PLATFORM.md:151`). It is long/cash only, so there are no borrow fees. This cannot explain a difference between the sheet and the Lab.
- Fix: drop driver #3, or reword it as "the Lab is long/cash only."

**W12 · 24.6 versioning (content, code comments and formula)**
- Text:
  - "When you edit the code, Strategy Lab generates an immutable SHA-256 hash"
  - "you click **Save strategy**. The system creates Version 1 … Saving again automatically produces Version 2 … toggle between Version 1 and Version 2 with a single click"
  - the formula `SHA256(Code ∥ Parameters)`
- Problem:
  - Strategy Lab's **Save** (`Sandbox.tsx:730-741, 772-796`) opens "Keep this experiment" with an "Experiment name" field. It stores a snapshot in workspace `experiments` (listed at `/experiments`).
  - The snapshot id is the open experiment's id or a random UUID. Re-saving an opened experiment overwrites it. There is no hash, no version number and no toggle.
  - Content-addressed versions exist only in the **research registry** (`/research`). There, a `StrategyVersion` is keyed by (owner, name, sha256) and created **when a run is queued**. "Editing code without running it creates no version" (`RESEARCH_PLATFORM.md:503`).
  - The hash covers the **source text only** (`:483`). Config is hashed separately as `config_sha256`, so `Code ∥ Parameters` is wrong.
- Fix:
  1. Save = a named experiment snapshot.
  2. For versioned reproducibility, click **Validate in research**, which takes you to `/research/new`.
  3. Each run with new source text gets v1, v2, …
  4. Use **Reproduce** to compare fingerprints.

**W13 · 24.6 exercise, practice question and exam q6 (false premise; the key itself is fine)**
- Text: "Why does Strategy Lab use content-addressed versioning for saved strategies instead of overwriting files?"
- Problem: Strategy Lab's save does overwrite, by experiment id.
- Fix: rewrite the questions around the research registry.

**W14 · 24.7 Factor Studio description, term, exercise, practice question, realWorld and outcome**
- Text: "Rank hundreds of stocks by Value (P/E), Quality (ROE), and Momentum, constructing long/short market-neutral quintile portfolios"; "which 20% of Indonesian banking stocks have the highest deposit growth…". The term reads "Quanta's institutional tool for ranking asset universes … quintile spread returns", and the keyed answer is "ranks an entire universe cross-sectionally".
- Problem: FactorLab fits CAPM / FF3 / Carhart / FF5 **time-series regressions on synthetic returns with known exposures** (`FactorLab.tsx:35-60`: "Fit a model to synthetic returns with known factor exposures"). It reports betas, HAC standard errors and ridge out-of-sample R². It has no stock universe, no ranking, no quintiles and no Indonesian bank data.
- Fix: describe it as a factor-regression studio. Rewrite the exercise and practice question (the premise is false).

**W15 · 24.7 links**
- Text: "Factor Studio ([/lab](/lab))", "AMM Simulator ([/simulator](/simulator))", and work-through step 2 "Bookmark the Factor Studio in /lab".
- Problem: `/simulator` is the paper-trading simulator (`App.tsx:73`). The AMM is at `/lab?tool=amm`, and Factor Studio is at `/lab?tool=factors` (`StrategyLab.tsx:16-22`). Plain `/lab` opens the Market sandbox.
- Fix: use the `?tool=` URLs.

#### MISLEADING / OUTDATED

**M1 · 24.7 AMM description**
- Text: "Simulate impermanent loss, liquidity pool fee generation, and routing slippage"; "arbitrageurs trade against the pool … observe the exact trade-off between fee yield and impermanent loss."
- Problem: AmmLab (`analytics.py amm()`) computes one swap's output, its price impact and its fee (`fee_x`), plus impermanent loss versus price ratio and loss inside a concentrated range. It has no routing, no arbitrage simulation and no accumulated fee yield.
- Note: the 50 ETH / 100,000 USDC inputs can be entered.

**M2 · 24.7 exam q7 (false premise; the key is the best option)**
- Text: "What unique capability … cannot be replicated in a standard spreadsheet cell?" The explanation adds "impermanent loss dynamically across trade sizes".
- Problem: swap output is one spreadsheet formula, `=y*dx*(1-f)/(x+dx*(1-f))`. Impermanent loss depends on the price ratio, not on trade size (IL = 2√r/(1+r) − 1).
- Fix: rewrite the question.

**M3 · 24.1 objective versus body**
- The objective lists "survivorship bias" as one of the three blind spots. The body's third item is "Formula Drift & Overfitting", and survivorship is never discussed.

**M4 · 24.1 formula**
- Text: `Spreadsheet Return ≠ Executed Return − Friction − Lag`.
- Problem: this states the relationship the wrong way round.
- Fix: `Executed ≈ Spreadsheet − Friction − Lag`.

**M5 · 24.1 sandbox text**
- Text: "see how naive same-bar calculation differs from real delayed execution."
- Problem: the code prints a single number, 8.0, which is the sum of every positive next-bar move (perfect foresight). There is no delayed-execution comparison.

**M6 · 24.2 adjustment and validation claims**
- Text: "Strategy Lab uses split-adjusted `close` … raw `volume`" and "Any row where H<L … will cause backtest crashes."
- Problem: the app does no adjustment and asks for pre-adjusted data ("Supply properly adjusted, licensed data", `import_data.py:3`). Yahoo's Close and Volume are already split-adjusted. A bar with H < L is **rejected at import** with "OHLC bounds are inconsistent." (`:38-42`); it does not crash a backtest.

**M7 · 24.3 parity claim**
- Text: "Because the row count and terminal close match exactly, you have verified data parity."
- Problem: exam q3 correctly calls the same check "necessary but not sufficient". The lesson contradicts its own exam.

**M8 · 24.3 platform: which bars are loaded**
- Problem: `data_store.historical()` loads the **earliest** `years×252` bars (`ORDER BY time LIMIT years*252`, `data_store.py:26-29`). The default is 3 years, or 756 bars, set by the "Simulation horizon" selector in the Parameters tab. For any file longer than 756 rows, the Lab's last close will not match the spreadsheet unless the learner raises the horizon. The lesson never mentions this.

**M9 · 24.3 sandbox text**
- Text: "inspect how pandas checks start date, end date, and terminal close."
- Problem: the code uses plain lists, and the guided runtime cannot import pandas.

**M10 · 24.4 look-ahead claim**
- Text: "completely removing the accidental look-ahead leakage."
- Problem: next-open fills remove only the same-bar fill leak. The guided runtime still accepts full-sample look-ahead: `data['close'] < max(data['close'])*0.9` and `np.mean(data['close'])` both ran and were accepted. Negative `shift` is blocked. The registry's truncated-history look-ahead test exists precisely for this case.

**M11 · 24.4 "exact same boolean array" as Excel**
- Problem: Quanta's `sma` averages whatever bars exist for the first k−1 bars (the `strategy_data` sma uses `start=max(0,…)`). Excel would leave those rows blank, so the first 19 rows differ.

**M12 · 24.5 work-through step 2**
- Text: "Multiply the trade count by your broker's actual fee schedule."
- Problem: the Lab's `trades` metric counts BUY and SELL **fills** separately (`summarize: len(trades)`; the Console says "fills"). A per-round-trip fee multiplied by fills double-counts.

**M13 · 24.5 reference**
- Text: "FINRA · Rule 5310 Best Execution and Spread Costs".
- Problem: the official title is "5310. Best Execution and Interpositioning" (fetched). The rule mentions transaction costs only in .09(b), and nothing about spread or slippage. A best-execution rule does not support a backtest-friction lesson.

#### WEAK

**K1 · Homepage-only references whose titles do not exist at the URL**
- 24.1: "CFA Institute · Backtesting Pitfalls and Survivorship Bias" (`cfainstitute.org`) and "SEC · Quantitative Trading and Systematic Execution Risks" (`sec.gov`).
- 24.6: "ACM · Reproducibility and Replicability in Computational Science" (`acm.org`).
- Course level: "CFA Institute · Quantitative Methods…" and "FINRA · Algorithmic Trading Rules…".

**K2 · Loosely matched lesson references**
- 24.3: "Ken French Data Library · Documentation and Reconciliation". The page exists but has no reconciliation section (fetched).
- 24.2: OpenFIGI covers instrument identifiers, not OHLCV mapping.

**K3 · Unrelated case-study mappings and the references they inject**
- 24.1 forecasting maps to statsmodels state-space forecasting.
- 24.2 reporting maps to GIPS.
- 24.3 edgar maps to the EDGAR APIs.
- 24.5 knight maps to Knight Capital, a deployment/control failure under Rule 15c3-5 with a $12M penalty (fetched). It has nothing to do with friction.
- 24.6 idempotency maps to AWS retries.
- Each realWorld walkthrough just restates the lesson's own example.

#### STYLE

- 24.3 formula uses a decimal comma, `0{,}00`, and mixes "Rp10.250" with "10,250" in an English lesson.
- 24.7 says "Click the primary button below", but the funnel CTA renders as a text link (`LessonReader.tsx:396-409`).
- The Uniswap whitepaper URL 301-redirects to `app.uniswap.org/whitepaper.pdf` (the v2 Core paper, Adams/Zinsmeister/Robinson 2020). The v2 pools docs 301-redirect to `developers.uniswap.org`. Both still work.

#### CHECKED AND CORRECT

- **24.1:** code prints 8.0 (2.5 + 3.0 + 2.5). The same-bar versus next-open framing is right.
- **24.2:** the invariant L ≤ min(O,C) ≤ max(O,C) ≤ H, the code output and both exercise keys are correct.
- **24.3:** code output is correct (4 rows, 2026-01-02 to 2026-01-07, 153.75).
- **24.4:** code runs on the default synthetic data with 289 of 756 bars long. The SMA formula is correct.
- **24.5:** code gives $1,200 friction and $300 net, so 80% is erased. The exercise ($300) and exam q5 (−10 bps × 200 = −2,000 bps ≈ −20%) are correct.
- **24.7:** code gives k = 5,000,000; AAPL 0.85 and MSFT 0.72 pass the 0.70 threshold.
- **Exam:** q1, q2 and q4 keys are correct.
- **Platform facts verified in code:**
  - next-open fills
  - 5/3 bps defaults
  - 252 sessions
  - Sharpe in excess of 3% (`1.03^(1/252)−1`)
  - the strategy-lab course has 32 lessons
  - funnel targets exist
- **References confirmed by fetch:** Ken French data_library and f-f_factors pages; SEC 2013-222.

---

### Course 25: Data Hygiene for Investors

#### WRONG

**W1 · Exam lessonIds shifted by one for q3–q6**
- Mapping:
  - q3 is about currency notation, tagged 25.3 but taught in 25.2.
  - q4 is about composite keys, tagged 25.4 but taught in 25.3.
  - q5 is about survivorship, tagged 25.5 but taught in 25.4.
  - q6 is about raw immutability, tagged 25.6 but taught in 25.5.
- Impact: learners see these ids. `ExamRoom.tsx:576-590` builds "Topics to revisit" from them, and `:633-634` renders "Review <lesson title>" links, so learners are sent to the wrong lesson. 25.6 (category drift) has no exam question.
- Fix: retag q3→25.2, q4→25.3, q5→25.4, q6→25.5, and add a 25.6 question.

**W2 · Exam q3 keyed option wording (still the best of the three options)**
- Text: "Remove all punctuation and symbols, convert the value to a standardized numeric column…"
- Problem: applied literally, '$1,200.50' becomes 120050, a 100× error. 'Rp 18.000.000' uses '.' as the thousands separator.
- Fix: "Strip the currency symbol or code, parse using the source's decimal and thousands separators, store the numeric amount plus an ISO-4217 `currency` column."

**W3 · 25.6 template: practice file cannot be parsed**
- Problem: line 5 is `Feb 04, 2026,TXN-2004,…`. The unquoted comma gives 8 fields against a 7-column header.
- `pd.read_csv` fails with: `ParserError: Error tokenizing data. C error: Expected 7 fields in line 5, saw 8`.
- In a spreadsheet, that row shifts one column right ("Feb 04" | " 2026" | "TXN-2004" …).
- The course never teaches CSV quoting, so the Python route fails at step 1.
- Fix: write `"Feb 04, 2026"` in quotes, or use `04 Feb 2026`.

**W4 · 25.6 claim that the file "contains exactly the five defect classes"**
- **Currency (#2) is absent.** `inflow` and `outflow` are plain integers, with no symbols or strings.
- **The "missing period" is not a defect.** It is only a date gap from 02-06 to 02-21. The running balance is continuous: every row's balance equals cumulative inflow − outflow, which I verified, ending at 8,000,000. No transaction is missing, and the reference leaves the gap unchanged.
- **No date ambiguity.** The only slash date, `02/02/2026`, has day = month, so it cannot exhibit DD/MM versus MM/DD confusion.
- **Unlisted date format.** `2026/02/03` (YYYY/MM/DD) is not among the formats the lesson lists.
- **Drift examples do not match the file.** The lesson lists `operasional`, but the file has lowercase `penjualan` instead.
- Fix:
  1. Add an ambiguous date such as `05/02/2026`.
  2. Add amounts like `Rp 1.800.000` or `$` values.
  3. Either insert a real gap (a balance break) or drop "missing periods".

**W5 · 25.6 instruction a learner cannot follow**
- Text: "Upload or submit your cleaned CSV for automated grading." The reading guide adds: "submit the cleaned CSV capstone in lesson 6."
- Problem: no frontend code calls `POST /api/v1/courses/{id}/capstone`. The route exists only in the backend (`api/routes/learning.py:66`), and a grep of `frontend/src` finds no caller.
- Fix: add an upload UI, or remove the instruction.

**W6 · 25.6 "downloads bar"**
- Text: "Download `messy_transactions_practice.csv` from the downloads bar."
- Problem: the files appear only on the course page under "Course downloads" (`TrackDetail.tsx:243-245`). The lesson has no downloads bar.

#### MISLEADING / OUTDATED

**M1 · Capstone validator overclaims (backend `learning.py:192-230`, which backs W5)**
- What it checks:
  - the date format of a `date`, `Date` or `tanggal` column
  - currency symbols in an `amount`, `Amount` or `nominal` column (the template has `inflow`/`outflow`, so this check never runs)
  - repeated `transaction_id`
- What it returns: `taxonomy: passed` and "verified against all 5 defect classes", although it never checks taxonomy or gaps.
- Re-implementation results — every one of these **passes**:
  - the reference file
  - the reference with `OpEx` and `penjualan` left unfixed
  - `Rp 5.000.000` in `inflow`
  - exact duplicate rows in a file with no id column
- The messy file fails on row 2 (`02/02/2026`).

**M2 · 25.3 duplicate-detection formulas**
- Text: "`=COUNTIF(A:A, A2) > 1` in Excel or `df.duplicated()` in Python."
- Problem: COUNTIF checks one column, not the composite key from step 1. `df.duplicated()` defaults to all columns with `keep='first'`, so it flags only the repeat (1 row for TXN-2005), while COUNTIF>1 flags both copies (2 rows).
- Fix: `=COUNTIFS(A:A,A2,B:B,B2)>1` and `df.duplicated(subset=['date','transaction_id'], keep=False)`.

**M3 · 25.3 sandbox text**
- Text: "see how pandas detects and drops duplicate composite keys."
- Problem: the code is a nested loop that drops nothing, and pandas is unavailable in the guided runtime.

**M4 · Exam q4 wording**
- Text: "prevents the database or dataframe from accepting duplicate entries"; "double-entry errors".
- Problem: a pandas DataFrame enforces no uniqueness; only a database PRIMARY KEY or UNIQUE constraint rejects duplicates. "Double-entry" is the accounting term of art for something else.
- Fix: "database table" and "duplicate entries".

**M5 · 25.4 look-ahead market example**
- Text: "buys stocks trading below their 52-week low, but calculating that low using the full calendar year's closing prices."
- Problem: a price can never be below a minimum that includes it, so the rule never fires.
- Fix: "buys at the calendar-year low, where that low is computed from the full year in advance."

**M6 · 25.4 survivorship example**
- Text: "today's S&P 500 members over the past 20 years, ignoring … Enron, Lehman Brothers."
- Problem: from 2026 the window starts in 2006. Enron filed in December 2001, outside it; Lehman (September 2008) is inside.
- Also: the objective promises a personal-finance and a market example for each bias, but **selection bias** gets neither.

**M7 · 25.4 worked example**
- Text: "The apparent 7.5% 'alpha' was entirely an illusion."
- Problem: the 7.5 percentage-point gap is survivorship bias, not alpha, since there is no benchmark. The strategy still earns 8.5%.

**M8 · Sandbox descriptions the code does not deliver**
- 25.1: "how pandas represents clean atomic rows". The code uses plain dicts.
- 25.2: "how python handles ISO 8601 formatting". The code parses nothing; the canonical date is hard-coded.
- 25.5: "how hashing validates raw data immutability". The code prints a hard-coded 10-character `4b82d91f0a` labelled SHA-256, which is 64 hex characters long. Nothing is hashed.
- 25.6: "inspect automated validation checks". The code only prints a list.

**M9 · Unsourced statistics (unverified)**
- 25.1: "Most spreadsheet analysts spend 80% of their time fighting messy spreadsheets".
- 25.2: "Two silent data killers account for over 50% of financial analysis blunders".
- Fix: cite a source or remove.

**M10 · 25.6 reference file versus 25.2's rule**
- Problem: 25.2 says hygiene "requires two distinct columns: `amount` … and `currency`". The cleaned reference has no `currency` column.

#### WEAK

**K1 · Homepage-only references**
- 25.3: "CFA Institute · Financial Statement Analysis and Reconciliation Principles" (`cfainstitute.org`).
- 25.4: "CFA Institute · Research Foundations: Survivorship Bias in Backtesting" (`cfainstitute.org`). The title does not resolve at that URL.

**K2 · Case-study mappings inject unrelated references**
- 25.1 and 25.6: warung, which brings in the SEC beginners' financial-statements guide.
- 25.3: atomic_ledger, which brings in SQLite atomic commit.
- 25.4: causal, which brings in World Bank impact evaluation. Its context is a training programme, while the realWorld text describes a small-cap screen.
- 25.5: idempotency, which brings in AWS retries.

**K3 · Turing Way references**
- `https://the-turing-way.netlify.app` 301-redirects to `book.the-turing-way.org`. It still works but is outdated.
- 25.6 cites "Data Cleaning and Preprocessing Best Practices" but links only to the book's home page.

**K4 · ISO 8601 page**
- Unverified: it returned 403 to automated fetch. It is the known official URL.

**K5 · 25.1 code**
- A DIV row stores dividend per share in the `price` column, so one column carries two meanings. This sits uneasily with "one variable per column".

#### STYLE

- 25.2 exercise says ISO 8601 is "universally mandated in quantitative finance", which overclaims.
- 25.3 uses a decimal comma, `0{,}00`, and mixes "brokerage statement" with "bank statement" in one example.
- 25.5 says "set the folder to read-only", which also blocks adding new raw files. Read-only files would be better.

#### CHECKED AND CORRECT

- **25.2:** 50,000,000 + 1,500 = 50,001,500. The "one third flipped" figure holds: 132 of 365 dates have day ≤ 12 and day ≠ month, which is 36%. 04/05/2026 means 5 April in the US and 4 May in Indonesia and the UK. ISO dates sort correctly as text.
- **25.3:** code reports 1 duplicate pair. $13,200 − $750 = $12,450. 20 calendar days ≈ 14.3 weekdays.
- **25.4:** code prints 17.5 and −21.7. 16 − 8.5 = 7.5 percentage points.
- **Exam:** q1 is correct; "column headers are values" matches Wickham 2014, whose three rules I confirmed by fetch. q2, q5 and q6 keys are correct.
- **Cleaned reference = the messy file after the course's rules:** ISO dates, dropping the exact duplicate TXN-2005, and mapping OpEx/Operations→Operasional and penjualan→Penjualan. My pandas re-implementation reproduces it byte for byte.
- **Templates:** balances are continuous. `content/templates` and `frontend/public/templates` are byte-identical.
- **Reference:** the JSS v059i10 URL is correct.

---

### Course 27: Python for the Reluctant Investor

#### WRONG

**W1 · 27.2 pandas instructions**
- Text: step 2 "Click **Run in sandbox** to load the virtual CSV and view the formatted DataFrame table"; step 3 "Try changing `df.head()` to `df.tail(2)`."
- Problem: the code card contains no `df` and no `head()`. `import pandas as pd` fails with `SandboxError: Imports are limited to math and the guided numpy subset.`
- Even under the optional Docker runtime (which has pandas but **no matplotlib** in `requirements.txt`), `pd.read_csv('prices.csv')` finds no file: the container is `--read-only` with `--network none`.
- Fix: say that pandas needs local Python, or rewrite the steps using the guided subset.

**W2 · 27.3 steps**
- Text: step 2 "Change `window=3` to `window=5`"; "Notice that the first 2 days show `NaN`."
- Problems:
  - The code has no `window=3`; the SMA is hard-coded as `prices[-1]+prices[-2]+prices[-3]`.
  - Keyword arguments are rejected: `Use positional arguments in the guided runtime.`
  - No series is printed. The guided `sma` never returns NaN, because it averages the bars available (verified: `sma[0] == close[0]`).
- Fix: use `sma(data['close'], 3)` with positional arguments, and note that the guided runtime does not produce NaN.

**W3 · 27.4 objective**
- Text: "Generate a clear line chart … save the output, and render it inline."
- Problem: no runtime in the app has matplotlib. The code prints only integers.
- Fix: reword the objective as an exercise to do locally.

**W4 · 27.5 instructions break the script**
- Text: the body uses `LOOKBACK_WINDOW = 7`; step 2 "Change line 3 to `LOOKBACK_WINDOW = 30`"; step 3 "compare the number of bullish signals".
- Problems:
  - The code defines lowercase `lookback_window`. Following step 2 gives `SandboxError: Name 'lookback_window' is not available.`
  - Setting the lowercase name to 30 silently averages all 10 prices (`[10-30:]` is `[-20:]`) and prints 105.1 with no warning.
  - The script prints no signals at all.
  - The worked example's "38 buy signals vs 24" over 60 days cannot be reproduced, and 38 crossovers in 60 days is implausible; it looks like a count of days above the MA.
- Fix:
  1. Use one name consistently.
  2. Guard with `len(prices) >= window`.
  3. Compute and print a signal count.

**W5 · 27.1 `expectedOutput`**
- Text: "Keuntungan: Rp 2,500 (25.0%)".
- Problem: the guided runtime prints `Keuntungan: Rp 2500 (25.0%)`. The guided interpreter drops f-string format specs without warning: the `JoinedStr` branch in `sandbox_worker.py` calls `str()` on each value. This contradicts the module's "unsupported syntax fails closed" docstring, and any lesson using `:,` or `:.2f` prints the raw value. `expectedOutput` is passed to the AI assistant (`services/assistant.py:153`), so the assistant may contradict what the learner sees.
- Fix: implement `format_spec` or reject it, and correct `expectedOutput`.

**W6 · Course resource**
- Text: "Python Beginner Cheat Sheet (Markdown)" linking to `/course-assets/strategy-lab/README.md`.
- Problem: that file is "Strategy Lab: reproducible investment research", the README of the 32-lesson project, not a cheat sheet.

#### MISLEADING / OUTDATED

**M1 · 27.6 tracebacks versus the platform**
- Text: "Look at the line number just above it … (`File "script.py", line 7`)" and "Inspect the pre-broken examples in the code card. Fix the KeyError."
- Problem: the guided runtime shows **no traceback and no line numbers for runtime errors**:
  - `print(data['Close'])` gives `SandboxError: KeyError: 'Close'. The parameter or field was not found (available: 'close', 'volume')`.
  - `1/0` gives `ZeroDivisionError: division by zero`.
  - Only SyntaxError reports a line ("'(' was never closed (<unknown>, line 1)").
- The code card also has nothing to fix: the bugs appear only in comments, and the code already uses `data['close']`.
- Fix: include a deliberately broken line, and explain the guided error format.

**M2 · Course description, 27.1 and the module docstring**
- Text: "execute Python code right here in your browser"; "executes … in less than 5 milliseconds".
- Problem: the code is edited in the browser but executed on the server (`POST /api/v1/sandbox/execute`, which spawns a subprocess). The displayed `execution_ms` covers subprocess startup, data generation and the backtest; locally I measured 38–65 ms.

**M3 · Reading guide**
- Text: "Every lesson ends with a runnable script and an expected output."
- Problem: only 27.1 has `expectedOutput`. The UI shows `expectedOutput` only in LocalCodeLab, which is used for C lessons (`LocalCodeLab.tsx:63-66`), so Python learners never see it.

**M4 · 27.4 chart claims**
- Text: "see the price trend rendered in the console"; "With three lines of code".
- Problems:
  - The console shows "Tingkat: n" integers, not bars.
  - The snippet has 4 lines, sets `label=` without `plt.legend()` (so labels never appear), and uses `df['sma_20']` without creating it.

**M5 · 27.2 performance claim (unverified)**
- Text: "Loading a million rows … takes less than one second."
- Problem: the time depends on width and dtypes.

#### WEAK

**K1 · Exam q6 tests material the lesson does not teach**
- q6 asks about IndexError; 27.6 covers SyntaxError, KeyError and ZeroDivisionError. The key and explanation are correct.

**K2 · Irrelevant references injected by case mappings**
- 27.6: "LLVM/Clang · AddressSanitizer", a C memory-error tool attached to a Python-traceback lesson.
- 27.1: Investor.gov asset allocation.
- 27.2: SEC financial-statements guide.
- 27.3: Ken French factors.
- 27.4: statsmodels state-space.
- 27.5: scikit-learn pitfalls.

**K3 · 27.5 Software Carpentry reference**
- Text: "Software Carpentry · Programming with Python: Modular Design" linking to `/lessons/`.
- Problem: that is the lessons index. It lists "Programming with Python", but no lesson called "Modular Design" exists (fetched).

#### STYLE

- 27.1 worked example writes `10000`, while the code uses `10_000`.
- Exam q4's explanation generalises "golden cross", which strictly means the 50-day average crossing the 200-day.

#### CHECKED AND CORRECT

- **27.1:** 2,500 and 25.0% are right, and changing the sale price to 15,000 gives 50%.
- **27.2:** code output is correct (5 rows, first and last rows).
- **27.3:** mean 105.4 (1054/10), maximum 110, SMA3 109.0. The pandas NaN explanation and `min_periods` default are confirmed against the pandas docs.
- **27.4:** the computed levels are right.
- **27.5:** the 7-day mean is 747/7 = 106.71.
- **Exam:** q1–q5 keys are correct.
- **References confirmed by fetch:** python.org gettingstarted; docs.python errors (it does say "The last line of the error message indicates what happened"); pandas getting_started and rolling; matplotlib tutorials index.
