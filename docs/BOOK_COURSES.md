# Book-aligned investment courses

The expanded courses are available at `/curriculum/security-analysis` and `/curriculum/statistical-foundations`. Existing lesson URLs remain valid, including `1.1`–`1.5` and `2.1`–`2.5`; their subjects and original first-question keys are retained. Course order follows the reading plan, so lesson identifiers are not sequential within every unit.

| Course | Lessons | Reading units | Practice questions | Checkpoints | Final questions |
| --- | ---: | ---: | ---: | ---: | ---: |
| Security Analysis | 31 | 7 book parts + 2 extensions | 62 | 4 × 4 questions | 31 |
| Quantitative Investment Analysis | 28 | 14 book chapters | 56 | 4 × 4 questions | 28 |

Both courses contain original explanations and fictional cases. Each lesson supplies an objective, reading connection, worked example, equation, runnable Python worksheet, two practice items, and a written task with a collapsible worked solution. Notebook assignments are prefilled with the task and space for evidence, assumptions, and a decision. The overall catalog now contains 425 lessons, 858 practice questions, and 789 exam questions across 111 assessments.

## Reading references

Security Analysis uses Graham & Dodd’s [1940 edition](https://www.mheducation.com/highered/mhp/product/security-analysis-classic-1940-edition.html). Its seven-part study map is consistent with the historical organization shown in the publisher’s [sixth-edition contents](https://www.mheducation.com/highered/mhp/product/security-analysis-sixth-edition-foreword-warren-buffett.html?viewOption=student). The map uses parts rather than unverified page numbers. Students read the relevant passages in their own copy. Later commentary and contemporary reporting conventions are not attributed to the 1940 authors.

Quantitative Investment Analysis follows the [fourth-edition publisher contents](https://www.wiley-vch.de/en/areas-interest/finance-economics-law/finance-investments-13fi/investments-securities-13fi3/quantitative-investment-analysis-978-1-119-74362-0), with at least two course lessons for each of its fourteen chapters, plus advanced extension lessons placed inside the chapters they build on. Earlier editions organize topics differently. This is an independent companion course, not an official CFA credential or a reproduction of the publisher’s workbook.

## Course coverage

Security Analysis progresses through evidence and value ranges; bond coverage, claims, covenants, and yields; cumulative preferred shares and conversion; dividends, retention, and repurchases; normalized earnings, depreciation, inventory, and cash conversion; NCAV, recoveries, hidden claims, cash burn, and intangible assets; peer comparison, event outcomes, and monitored decisions. Unit VIII separately critiques the later Graham growth worksheet and introduces contemporary operating cash-flow valuation before the Alder committee capstone. Unit IX adds accrual forensics, manipulation screening, hidden liabilities, segment concentration, cyclical normalization, dilution and contingent claims, and an advanced red-team capstone. Eight further case-driven courses extend the subject after the core curriculum: forensic accounting, credit and distress, quality and capital allocation, banks, valuation under uncertainty, cyclicals and commodities, technology and intangibles, and a documented real-world casebook.

Quantitative Investment Analysis progresses through discounting and project value; return measurement and dispersion; Bayesian updates and covariance; normal/lognormal and binomial models; confidence intervals and block resampling; hypothesis tests and multiple comparisons; simple and multiple regression with diagnostics; stationarity, forecasting, and volatility; regularization, classification, and unsupervised methods; point-in-time joins and text data; factor attribution and active risk; VaR, expected shortfall, stress and liquidity; chronological backtests and a research-report capstone. Advanced extensions sit in their chapters: spot and forward rates (chapter 1), Monte Carlo variance reduction (4), Bayesian and James–Stein shrinkage (5), permutation and rank tests (6), logistic regression (8), the fundamental law of active management and Black–Litterman (12), and Kupiec/Christoffersen VaR backtests (13).

The quantitative examples use small inspectable calculations. They teach model interpretation and experimental design; they do not claim to implement a large-data production ML or forecasting pipeline. Security Analysis worksheets use fictional statements and stipulated claim terms, not automated live-company recommendations.

## Assessment and persistence

Checkpoints sample the preceding units and pass at 75%. Their continuation links lead to the next module after the checkpoint boundary. The final exams cover every lesson, use questions distinct from practice and checkpoints, and pass at 80%: 25/31 for Security Analysis and 23/28 for Quantitative Investment Analysis. Security Analysis retains its existing final ID and is now version 3; Quantitative Investment Analysis remains version 2. Old attempts remain in workspace history but do not count as a pass for the new version.

Legacy lesson completions, notes, saved code, and first-question submissions remain intact. New practice uses the existing `:q2` key convention. A newly completed lesson requires both practice answers; an old completion is not silently erased. Undoing an old completion requires finishing the expanded practice before marking it complete again.

The capstones provide a five-criterion, 20-point self-review rubric and a suggested target of 15 with no zero. Written work is stored in the notebook and is not automatically marked or certified. Graded final-exam scores remain separate from that self-review.

The displayed minutes estimate guided in-app study. Reading the source books, completing assignments, and writing the 600–1,000-word capstone reports require additional time. The price sandbox stays in cash for these book worksheets; its equity curve is not evidence for the calculation’s economic or statistical validity.

## Authoring and verification

Authoritative course sources are `content/authoring/security_analysis.py`, `content/authoring/quantitative_analysis.py`, and shared helpers in `content/authoring/book_courses.py`. Regenerate the client/server catalog with:

```sh
python3 content/authoring/curriculum.py
```

The generator preserves legacy first questions from the original catalog definitions. Both the frontend and API consume the generated `content/catalog/curriculum.json`; restart or rebuild the API after catalog changes. Production Compose builds include the catalog in both images.

Verification includes catalog integrity, all lesson templates in the restricted guided runtime, golden capstone arithmetic, all practice keys, exact exam thresholds, stale-version rejection, browser reading/assignment/quiz/exam persistence, unit continuation, mobile layout, and mathematical rendering across all 52 expanded lessons. See [verification results](VERIFICATION.md).
