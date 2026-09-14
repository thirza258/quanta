# Strategy Lab expansion and careful-investor prerequisite — September 14, 2026

The rebuilt application at **http://127.0.0.1:8088** includes **The intelligent & careful investor** directly before Security Analysis (16 lessons, 8 planned study hours) and the expanded **Strategy Lab** (32 lessons, 16 hours). The catalog contains **12 courses, 300 lessons, 608 practice questions and 572 exam questions across 77 exams**. Algorithm Evaluation remains last. Both development and Docker API catalogs exactly match the canonical JSON.

| Check | Result |
| --- | --- |
| TypeScript/Vite and Docker builds | Passed; all four Compose services healthy |
| Frontend model/progression tests | 42 passed |
| Backend API/domain/content/runtime tests | 536 passed, including all 276 Python worksheets and existing 24 C worksheets |
| Final production browser checks | 23 passed in 1.5 minutes: course ordering/search, every new/expanded lesson, downloads, practice, notebook, completion persistence, server checkpoint/final grading, existing book courses, mobile cards and five sidebar sizes |
| Development browser coverage | 32 of 33 applied-course scenarios passed initially; one worksheet-opening check overlapped content hot reload and passed on isolated rerun, alongside the new ordering/search scenario |
| Strategy source archive | Eleven independent tests pass after extraction: cash/fees, next-open causality, future mutations, filings/revisions, momentum skip, liquidity, cash, ties, reconciliation, selection boundaries and malformed inputs |
| Reporting interoperability | Actual selected test exports produce matching return/drawdown metrics through the final report project; HTML, Markdown, JSON, PNG and SVG created and the report/chart verified in a browser |
| Compatibility | All ten other existing course objects remain identical; original Strategy Lab subjects and first-practice keys survive at 4.1–4.4; old version-1 finals remain historical and do not satisfy version 2 |
| Content publication | All 32 catalog/download files regenerate identically from /tmp; concurrent reads observe complete files; served archives equal reviewed local bytes |
| Authoring | Ruff and diff whitespace checks pass |

An image refresh initially captured the catalog while the old generator was overwriting it, producing a truncated JSON file. Catalog and download publication now use temporary files followed by atomic replacement. Regeneration completed before the final image build; API startup and exact served-catalog equality pass. The related development hot reload interrupted one worksheet-opening test; its isolated rerun passes. No unresolved failures remain.

Strategy Lab uses an original 90-session three-stock fixture and a standard-library Python engine. It implements equal-weight, value-quality and momentum portfolios; the selected rule's synthetic test export flows directly into the reporting course. Pairs/borrow execution, fitted ML, corporate actions, market impact and live adapters remain explicitly labeled extensions. Both courses have original cases, lesson references, downloadable notebooks and separate written capstone rubrics.

Artifacts: `/tmp/quanta-careful-investor-mobile.png`, `/tmp/quanta-strategy-lab-mobile.png`, `/tmp/quanta-strategy-report-browser.png`, `/tmp/quanta-strategy-research-final/` and `/tmp/quanta-strategy-report-final/report.html`. Logs: `/tmp/quanta-investor-strategy-check-final.log`, `/tmp/quanta-courses-production-final.log`, `/tmp/quanta-course-recovery-browser.log`. Course scopes: [careful investor](INTELLIGENT_INVESTOR.md) and [Strategy Lab](STRATEGY_LAB_COURSE.md).

---

# Architecture, news analysis, C/HPC and final evaluation track — September 14, 2026

The final application is available at **http://127.0.0.1:8088**, with healthy web, API, PostgreSQL and Redis services and the existing volumes retained. The development launcher is also running the reorganized applications at **http://127.0.0.1:5173**, with API port 8000. Both API catalogs exactly equal the shared generated content.

The repository now separates `frontend/`, `backend/` and `content/`. Frontend application composition, feature models/hooks/pages/components and shared utilities are separate. Backend HTTP routes, services, domain rules, persistence, configuration and isolated execution are separate. All eight previous course objects remain identical as JSON data, preserving their lesson URLs, first-practice keys and exam versions.

Three courses were added: news-to-company/stock analysis after Security Analysis (24 lessons, 12 hours); C and high-performance algorithmic trading after Python bots (24 lessons, 12 hours); and algorithm evaluation/results reporting as the final track (16 lessons, 8 hours). The catalog now has **11 courses, 256 lessons, 516 practice questions and 480 exam questions across 64 exams**. Sources accompany every course/lesson and the shared page footer.

| Check | Result |
| --- | --- |
| TypeScript/Vite build | Passed locally and in the final Docker web build |
| Frontend model/progression/simulator tests | 38 passed |
| Backend API/domain/content/runtime tests | 469 passed; subsequent reporting/download recheck: 5 passed |
| Guided Python worksheets | All 232 templates execute in the restricted runtime |
| C17 worksheets | All 24 compile with warnings treated as errors and reproduce their expected output |
| C/POSIX download | Extracted, compiled and tested; golden causal ledger, risk/bounds rejection, seed identity, 1–32 requested workers and atomic result publication pass |
| C sanitizers | AddressSanitizer + UndefinedBehaviorSanitizer project target passes |
| C/HPC measurement | 200,000 bars × 64 windows, five paired repetitions, four workers: exact equality in every run; observed speedups approximately 3.56–3.78× on this Mac, not a portable performance guarantee |
| Reporting download | Nine independent project checks pass; actual JSON/Markdown/HTML/PNG/SVG generation verified with Python 3.14 and Matplotlib 3.11.2 |
| Browser regression | All 68 scenarios verified on the final app: 67 passed in the full run; both lost-response recovery variants passed twice after narrowing an ambiguous test alert selector (4 rechecks, 17.1 seconds) |
| Sidebar and course cards | Bounds, scrollable navigation, reachable search/account controls, mobile inert state and card footer spacing verified; 375px-high landscape and 390px-wide portrait cases pass |
| Native scientific worker | Rebuilt after relocation; numerical execution, forbidden import, timeout and memory-limit checks pass |
| Existing ML and coin projects | Nine ML lifecycle checks, six native-chain checks and real local ERC-20 compile/deploy/transfer/allowance/conservation checks pass after relocation |
| Content ownership | All 26 catalog/download files regenerate identically from `/tmp`; served C/report archives equal the reviewed source packages |
| Authoring | Ruff, formatting and diff whitespace checks pass |

The first full browser run exposed global CSS overriding the course card's bottom padding and a mobile test clicking the covered center of the navigation backdrop. Loading course overrides after the global baseline restores the spacing; the test now clicks the visible backdrop. Both fixes passed the 64-scenario regression run. C lessons now load a C editor with saved drafts, explicit reset, source download and local compiler instructions; no C is submitted to the Python sandbox.

The final 68-scenario run found one test selecting every page alert when a workspace synchronization warning and an exam submission error were both present. The assertion now targets the exam panel. Both lost-response scenarios, including preservation of later edits and server attempt history, passed twice against the same final application. No unresolved verification failures remain.

Independent reporting fixture: strategy return **10%**, benchmark **8%**, cumulative difference **2 percentage points**, maximum drawdown **6.6667%** and illustrative paired timing median **3×**. HTML shows the metrics, complete wealth/drawdown figure, assumptions, source hashes, references and a review-required conclusion. The report generator does not automatically certify strategy quality or run every proposed robustness analysis. C's optional GPU/OpenMP/distributed/gateway exercises remain explicitly distinguished from its runnable CPU/POSIX implementation.

Reviewed artifacts include `/tmp/quanta-report-course-final.png`, `/tmp/quanta-c-course-production.png`, `/tmp/quanta-c-editor-production.png`, `/tmp/quanta-c-editor-mobile.png`, `/tmp/quanta-sidebar-mobile-landscape.png`, and the actual report at `/tmp/quanta-evaluation-report/report.html`. Detailed scopes: [architecture](ARCHITECTURE.md), [news](NEWS_COURSE.md), [C/HPC](C_HPC_COURSE.md), [final evaluation course](ALGORITHM_EVALUATION.md).

---

# Applied courses and 12-hour stock ML — September 14, 2026

The rebuilt application runs at **http://127.0.0.1:8088** with healthy web, API, PostgreSQL, and Redis services. Existing data volumes were retained.

| Check | Result |
| --- | --- |
| TypeScript/Vite production build | Passed in the final rebuilt web image |
| Frontend catalog, progression, and simulator tests | 29 passed |
| Backend API, all guided templates, assessment versions, and project invariants | 367 cases verified across the full run and targeted rechecks |
| Browser scenarios | 50 verified: 48 passed in the full run; both affected scenarios passed after fixes (5.2 seconds) |
| New applied-course flows | All 13 scenarios passed: downloads, unit maps, capstone practice/notebook/worksheet, references, current-version exams, continuation, persistence, and mobile layout |
| Full expanded lesson rendering | All 128 bot/econometrics/Web3/ML lessons render equations, two practice items, assignments, and named references; the 52 book lessons also passed rendering checks |
| Guided Python runtime | All 192 catalog templates executed within the existing restricted runtime |
| ML lifecycle | Nine tests passed, including cleaning faults, label arithmetic, date purging, future-perturbation invariance, held-out outcome isolation, metric accounting, latest-row inference, and artifact/batch parity |
| Native coin and ERC-20 downloads | Source archive extracted into a fresh directory, installed with npm ci, and passed six native-chain tests plus actual local Solidity compile/deploy/transfer/allowance/conservation/runtime checks |
| Quantitative research project | Eight independent numerical/timing tests passed for OLS/HAC, cointegration diagnostics, GARCH/covariance arithmetic, irregular purging, queue priority, ranked caps, next-open accounting, and evidence denominators |
| Compatibility | All 106 prior lesson URLs and first-practice keys preserved; old expanded-final versions rejected while historical passes remain stored |
| Catalog and downloads | API equals generated catalog; source-only archives match reviewed files; generation and packaging deterministic |
| Authoring | Changed-file Ruff, Prettier, and diff whitespace checks passed |

The initial backend run passed 363 tests and found one outdated seven-course count. Updating it for the new eighth course and adding download/ML-threshold cases yielded 367 collected cases; all 69 affected API/assessment/download checks then passed. The browser run found an outdated six-unstarted-course expectation and a search regression caused by renaming the AMM lesson without retaining “impermanent loss.” The count now follows the catalog and the expanded AMM lesson retains its familiar title. Both affected browser flows passed on the final rebuilt app. No unresolved test failures remain.

The dedicated ML course has **24 lessons × 30 minutes = 720 minutes / 12 hours** of planned reading, worksheet, and project work, with exams additional. The actual local pipeline generates imperfect synthetic data, audits cleaning, constructs dated features and matured labels, purges chronological partitions, fits ridge/forest/logistic candidates, selects using validation, refits eligible development rows, scores held-out outcomes, persists full pipelines, and performs batch inference without requiring future labels. Reports preserve baselines, unsuccessful results, probability diagnostics, artifact hashes, and descriptive monitoring. Neural/boosting, nested evaluation, post-hoc calibration, and other advanced experiments remain explicitly identified learner extensions, not claimed default fits.

The native coin baseline reconciles balances **910/100** and supply **1,010** after its first block, with a **1,100** cap. Tests cover signatures, wrong domains, Merkle proofs, replay, insufficient funds, atomic rejection, forged headers/work/rewards, independent replay, and state isolation. The ERC-20 creates **1,000,000 whole tokens** on an in-process EVM; its main fixture gives a recipient **110 tokens** and finite remaining allowance **15**, followed by additional conservation steps. No public chain, token sale, exchange pool, or broker authority is created.

Manual screenshots reviewed: `/tmp/quanta-ml-course-desktop.png`, `/tmp/quanta-ml-course-mobile.png`, `/tmp/quanta-web3-course-mobile.png`, and `/tmp/quanta-expanded-amm-final.png`. New neural-network artwork and the retained crypto illustration render; mobile course content stays within the viewport. The source footer continues across all page types. At that release, the catalog contained **192 lessons, 388 practice questions, and 352 exam questions across 45 assessments**. See [course scope](APPLIED_COURSES.md) for exact study/project boundaries and commands.

---

# Bot course, attribution, and course layout — September 14, 2026

Verified the running Docker application at **http://127.0.0.1:8088**, retaining the existing PostgreSQL/Redis volumes and prior simulator and book-course work.

| Check | Result |
| --- | --- |
| TypeScript and Vite production build | Passed in the rebuilt web image |
| Frontend catalog, progression, and simulator tests | 24 passed |
| Backend API, all lesson templates, exams, paper project, and simulator tests | 246 passed (8.12 seconds) |
| Browser scenarios | 37 verified: 30 passed in the full run, followed by all 7 targeted rechecks passing (47.2 seconds) |
| Bot lesson rendering | All 32 lessons render display mathematics, two practice items, assignments, and their named sources |
| Reference coverage | Shared footer verified across 14 routes covering every page type, including not-found; every course and all 106 lessons have source metadata |
| Responsive course layout | No horizontal page overflow at 390, 768, and 1440 px; card footer spacing and minimum readable widths checked |
| Offline project | Downloaded through the browser; local replay, partial fills, duplicates/conflicts, cash reservations, two writers, rollback, restart/halts, and evidence validation tested |
| Catalog consistency | API response identical to the generated frontend catalog; generation deterministic |
| Authoring checks | Changed-file Prettier, Ruff, and whitespace checks pass |

The full browser run started before the rebuilt web container finished restarting, so its first five scenarios failed with connection-refused errors. Two new attribution scenarios also caught the shared footer's implicit landmark behavior when nested inside `main`. The footer now follows `main`, exposing a proper page-level content-information landmark. After the server was ready and the placement fixed, all seven affected scenarios passed. No unresolved browser failures remain.

The bot course has 32 original applied lessons, 64 practice questions, seven four-question checkpoints, and a 32-question version-2 final. Existing 5.1–5.5 first-answer keys are explicitly tested. Threshold tests reject old final versions and verify that 25/32 fails while 26/32 passes. Browser flows cover project download, assignment notebook prefill, both practice answers, completion persistence, runnable project arithmetic, checkpoint continuation, and server-graded final persistence. Existing beginner, book-course, workspace, and simulator scenarios also passed across the runs.

Independent project checks reconcile final cash **920939 cents**, **8 shares**, equity **1002539 cents**, fees **61 cents**, and **3 unique fills**, with the halt retained after reopening SQLite. Two expanding ridge fits produce MSE **0.495982553** against baseline **30.5** on artificial observations. AI fixture tests reject missing/future sources, unsupported facts, incorrect units/issuer/period, nonfinite or Boolean numeric values, missing fields, extra instruction fields, and a zero growth denominator. These are educational execution/evaluation fixtures; no broker or AI provider is connected.

Manual screenshots reviewed: `/tmp/quanta-header-final.png`, `/tmp/quanta-mobile-final.png`, and `/tmp/quanta-lesson-references-mobile.png`. The book illustration is now an open book; cards retain footer space with long descriptions and adapt to a single column on narrow screens. The reference library aggregates cited sources and links source-use guidance plus generated production dependency notices. Attribution does not constitute legal clearance or reproduction permission.

The complete catalog contains **106 lessons, 206 practice questions, and 182 exam questions across 23 assessments**. The in-app guided worksheets remain cash-only and do not imply trading-performance validation. The written/code capstone is self-assessed separately from the concept exam.

---

# Book-course expansion — September 14, 2026

The local app now includes 24 Security Analysis lessons and 28 Quantitative Investment Analysis lessons. The source reading maps, scope, and assessment rules are documented in [Book courses](BOOK_COURSES.md). The learner flow is course reading plan → lesson and assignment → online practice grading → saved notebook/progress → checkpoint or final → persisted result and continuation.

| Check | Result |
| --- | --- |
| TypeScript and Vite production build in Docker | Passed |
| Frontend catalog, progression, and simulator tests | 22 passed |
| Backend API, financial worksheets, accounts, exams, and simulator tests | 174 passed |
| Course, assessment, and workspace browser scenarios | 23 verified; all 8 book-course scenarios passed on the final Docker build |
| Expanded lesson rendering | All 52 lessons render equations, assignments, and two practice questions |
| Desktop and 390-pixel mobile review | Course plans and readers render; no page-level horizontal overflow |
| Client/server catalog consistency | Identical catalog served by the rebuilt API |
| Authoring | Deterministic catalog generation; Ruff, changed-file Prettier, and whitespace checks pass |

The browser suite initially passed 22 scenarios and found inline equation delimiters where display equations were intended. The shared course generator now emits standalone display delimiters. The targeted rendering check then passed across all 52 expanded lessons, followed by all eight book-course browser scenarios on the final Docker build (39.2 seconds). Verification also caught and corrected two numerical roundings in the quantitative worked examples and replaced unsupported Python comprehensions/generators with explicit guided-runtime loops.

Both course flows save written capstone notes, grade both practice items online, retain completion on reload, execute the capstone worksheets, submit version-2 finals, retain results, and link every answer explanation to its lesson. Checkpoint continuation now follows the course boundary rather than the first lesson omitted from a sampled question set. Existing beginner completion, offline exams, account history/recovery, and saved experiment flows passed regression checks.

Golden arithmetic checks independently verify the Alder claims bridge and conservative maximum price; the quantitative capstone mean, dispersion, interval, and cost sensitivity; the empirical tail convention; the compounded return after costs; and the Bayesian base-rate calculation. All 79 catalog templates run within the existing restricted Python runtime. The 52 new book worksheets remain in cash in the price sandbox, so their charts do not imply strategy validation.

Course assessment counts are 104 practice items and 84 distinct exam items across the two expanded courses. Across all seven courses the catalog contains 79 lessons, 147 practice questions, and 127 exam questions in 16 assessments. Written capstones are explicitly self-assessed, separately from the numerical final-exam grades.

---

# Verification results

## Stock trading terminal — September 14, 2026

The new `/simulator` implements the first-release terminal in PRD Section 6.3. The updated web and API containers run at **http://127.0.0.1:8088/simulator**, with the existing PostgreSQL, Redis, learning data, and data volumes retained. This release does not claim completion of the broader 18-week roadmap or the subsequent simulator features.

| Check | Result |
| --- | --- |
| TypeScript and Vite production build in Docker | Passed |
| Vitest learning, indicators, warm-up, and CSV tests | 21 passed |
| Pytest API, financial models, accounts, exams, and simulator | 117 passed |
| Simulator browser stories on the development app | 9 passed |
| Browser stories through Docker/Nginx/PostgreSQL/Redis | 24 scenarios verified; rate-limited account story passed on retry |
| Ruff, changed-file Prettier, and diff whitespace checks | Passed |
| Docker services | Web, API, PostgreSQL, and Redis healthy |

The expanded Docker run passed 23 stories; its final existing workspace-conflict story received the expected authentication rate-limit response after repeated test runs. That story passed after the limit window, and the final buy/reduce/close, journal, and export story also passed on the updated web image. The application’s authentication limit was retained. When running repeated browser suites against the same local deployment, allow the 60-second authentication window to reset before retrying rate-limited account tests.

### Acceptance coverage

| Criterion | Evidence |
| --- | --- |
| SIM-AC-01 | Navigation and beginner practice links; desktop chart dimensions asserted at 1440×900; dedicated desktop/tablet/mobile visual inspection; persistent paper/mode labels. |
| SIM-AC-02 | Stock search, timeframe, RSI, drawing creation/edit/lock/delete/undo, reload, and symbol/run isolation. Direct two-click creation and object dragging are verified; fullscreen dialogs work. |
| SIM-AC-03 | Decimal round-trip fixture asserts $98,999 after buying 10 at $100 with a $1 fee, then $100,098 and $98 realized after selling at $110 with a $1 fee. Browser buy/reduce/close verifies positions, fills, journal, history, and exports. |
| SIM-AC-04 | A nonmarketable limit remains unfilled, a confirmed amendment enables a volume-limited partial fill, cancellation releases the remainder, and later replay cannot fill it. |
| SIM-AC-05 | Next-bar execution, stop gap pricing, strict passive limit touch, conservative stop-limit sequence, and shared liquidity. Market API reads can pin the displayed clock; future cursor requests are capped. Historical snapshots remain usable after removing their source file; daily bars cannot become intraday data. |
| SIM-AC-06 | The browser loses a response only after the real service accepts the order, reloads, retries the stable UUID, and recovers exactly one order and position. A second signed-in browser recovers settings/positions; logout and guest ownership checks prevent access. Offline drafts remain intact. |
| SIM-AC-07 | Invalid orders, cash/share reservations, rejected form and dragged amendments, concurrent writes, immutable request identifiers, and archived resets. Simulator writes leave learning state separate. |
| SIM-AC-08 | Accessible order forms, keyboard submission, mobile buy/close/history, sticky Buy/Sell controls, internal table scrolling, and no page-level horizontal overflow at 390 pixels. |

Browser regression work also fixed a chart-hover readout error, fast successive drawing clicks, dialogs outside fullscreen, and an order click coinciding with a background layout save. A deliberate held-response test verifies that the order waits for the preference write and then submits once. CSV tests preserve negative ledger numbers while escaping executable journal text.

Agent-browser inspected the terminal in light and dark themes, at desktop, tablet, and mobile sizes. The deployed page has meaningful content, no error overlay, and no browser errors. Local screenshots: `artifacts/simulator-desktop.png`, `artifacts/simulator-tablet.png`, and `artifacts/simulator-mobile.png`.

### Simulator performance sample

Reference desktop: **Apple M2 Pro, 10 CPU cores, 16 GiB memory, Darwin 25.6.0**, headless **Chrome 152.0.7977.83**, 1440×900 viewport. The local deployment is the four-service Docker stack; the API is limited to two CPUs and 1 GiB. One benchmark client used seed 47 synthetic AAPL with **5,000 observed minute bars** and **Volume, SMA20, and RSI14** enabled.

| Measurement | Sample | Empirical p95 | PRD target |
| --- | --- | --- | --- |
| Order acknowledgement | 50 sequential HTTP orders through the web proxy, response body consumed; excludes waiting for a fill | **36.9 ms** | Below 500 ms |
| Pan/zoom frame interval | 891 `requestAnimationFrame` intervals during 360 iterations of Playwright drag/wheel input, after warm-up | **16.8 ms** | Below 33 ms |

Maximum acknowledgement was 114.9 ms; maximum sampled frame interval was 16.8 ms. Both targets were met for this documented local sample. Frame intervals measure browser scheduling during chart input; this is not a production concurrency test or a guarantee across devices. The headless browser reported no page errors.

Reproduce with `TEST_URL=http://127.0.0.1:8088 node frontend/scripts/benchmark-simulator.mjs`. The script creates an isolated guest run and writes `artifacts/simulator-performance.json` and `artifacts/simulator-5000-bars.png`.

Historical data still requires an installed import. Corporate-action treatment is explicitly undeclared for existing imports; prices are used as supplied and no split/dividend adjustments are added by the engine. The guide documents immediate settlement, weekday-only synthetic sessions, fees, FIFO volume sharing, and replay fill timing. Live feeds, Level 2, margin/shorts, bots, and bracket/OCO orders remain the PRD’s subsequent releases.

## Final beginner-course and exam review — September 14, 2026

The final review covered the eight beginner lessons, their worked arithmetic, checkpoint and final answer keys, and the six specialist exams. The beginner references resolve to the intended [Investor.gov stock overview](https://www.investor.gov/introduction-investing/investing-basics/investment-products/stocks), [order types](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-14), [diversification](https://www.investor.gov/introduction-investing/getting-started/asset-allocation), [FINRA stock overview](https://www.finra.org/investors/investing/investment-products/stocks), and [stock evaluation](https://www.finra.org/investors/investing/investment-products/stocks/evaluating-stocks) pages. Catalog regeneration from `/tmp` remains byte-for-byte identical, and Ruff passes across the backend and scripts.

The review found and fixed one remaining course-filter regression: a learner who submitted only the second or third practice question was incorrectly listed under **Not started**. Course activity now includes every practice-question key. The existing beginner browser story first reproduced the failure, then verified **In progress**, **Not started**, reload persistence, and module completion after the fix.

The web image rebuilt successfully with TypeScript and Vite, and all **15 browser stories passed in 50.4 seconds** against the updated Docker app at **http://127.0.0.1:8088**. Prettier and diff whitespace checks pass; all four services are healthy. The latest frontend and backend unit-suite results remain **14 passed** and **96 passed**, respectively, as recorded in the recovery follow-up below.

## Assessment recovery follow-up — September 14, 2026

A new browser regression reproduced a lost-response bug: the API had recorded a passing exam, but reloading left the submitted draft open and hid the result. History recovery now retires matching drafts and preserves later edits for an explicitly chosen new attempt. Submission conflicts refresh account history automatically.

| Check | Result |
| --- | --- |
| TypeScript and Vite production build in the rebuilt Docker web image | Passed |
| Vitest curriculum, grading, progression, and recovery tests | 14 passed |
| Pytest backend suite | 96 passed |
| Playwright stories through Docker/Nginx/PostgreSQL/Redis | 15 passed in 51.2 seconds |
| Changed TypeScript files: Prettier and diff whitespace checks | Passed |

The two added browser stories drop the response only after the real API has saved the attempt. They verify automatic recovery after reload and preservation of subsequent edits across a rejected retry, reload, and successful new submission. The original score remains unchanged, with exactly one or two account submissions as appropriate. Unit tests additionally check recovery when history was already merged, preservation of later retakes, version filtering, and unchanged-state handling.

Agent-browser inspected the recovery notice on desktop and at 390 pixels, then exercised **Review submitted attempt** and confirmed the original 100% score with no draft remaining. Neither viewport overflowed, and there were no page errors or error overlays. Screenshots are in `artifacts/exam-recovery-desktop.png` and `artifacts/exam-recovery-mobile.png`.

The web container at **http://127.0.0.1:8088** was rebuilt and updated. The API, PostgreSQL, Redis, and persistent volumes were retained.

## Trading fundamentals and assessment release — September 14, 2026

Verified locally with the running React/Vite client and FastAPI service:

| Check | Result |
| --- | --- |
| TypeScript and Vite production build | Passed |
| Vitest curriculum, grading, progression, migration, and history tests | 11 passed |
| Pytest API, financial models, execution, accounts, and assessments | 96 passed |
| Playwright browser stories against the local development app | 13 passed |
| Playwright browser stories through Docker/Nginx/PostgreSQL/Redis | 13 passed |
| Docker web/API image builds and four-service readiness | Passed; all services healthy |
| Ruff checks across backend and scripts | Passed |
| Catalog regeneration from a different working directory | Deterministic; identical output |

The catalog contains 37 modules, 53 practice questions, and 53 exam questions across eight assessments. The API tests run every Python lesson template and validate exact passing boundaries (12/16 fails, 13/16 passes; 6/8 passes the checkpoint). They reject incomplete, extraneous, invalid, non-integer, and stale-version answers. Account tests verify ownership, retry deduplication, score calculation independent of caller-supplied score/pass fields, and workspace round trips.

The seven added browser stories verify:

1. Beginner entry in reading view, incorrect-answer feedback, all-question completion requirements, reload persistence, and optional Python execution.
2. Exam draft recovery, incomplete-submission prevention, incorrect-answer review, topic links, retakes, attempt history, and a passing checkpoint's link to the next lesson.
3. All eight beginner lessons → checkpoint → final → 100% course completion → next specialist track, including the Completed curriculum filter.
4. Account grading and history in a fresh browser context, deduplicated request retries, recovery from a workspace missing its result, and guest isolation after sign-out.
5. A failed submission preserves the complete draft and can be retried after reload.
6. Device grading with every API route unavailable, plus 390-pixel exam navigation, dark theme persistence, and no horizontal overflow.
7. A delayed grading response after sign-out does not copy an account result into the guest workspace.

All six original browser stories also pass, covering research notes, saved experiments, account sync conflicts/recovery, finance tools, and mobile navigation. Agent-browser independently inspected the overview, beginner course, and exam room; desktop and mobile screenshots are in local `artifacts/`. No browser errors or Vite overlay appeared.

The existing Docker deployment was updated at **http://127.0.0.1:8088**, retaining its database and data volumes. PostgreSQL contains the additive `examsubmission` table. A transient registry metadata timeout interrupted the first web build; retrying the normal build succeeded. All 13 browser stories then passed through the rebuilt deployment in 41.7 seconds.

Known nonblocking output remains the existing large Monaco/chart chunk warning and upstream Starlette test-client deprecations. The new beginner reading view loads the editor only when a sandbox view is requested.

## Initial platform release — September 13, 2026

Verified on September 13, 2026, on an Apple Silicon Mac with Node 25.9.0, Python 3.14.4, Chrome, and Docker Engine 29.7.2. Docker builds use Node 22 Alpine and Python 3.14 slim.

## Automated checks

| Check | Result |
| --- | --- |
| TypeScript and Vite production build | Passed |
| Vitest curriculum/format integrity tests | 3 passed |
| Pytest financial, runtime, API, authentication, historical-store tests | 66 passed |
| Playwright end-to-end tests against the actual Docker deployment | 6 passed |
| Ruff Python checks | Passed |
| npm dependency audit after updating Vitest | 0 reported vulnerabilities |
| Docker Compose configuration | Valid |
| Docker web and API image builds | Passed |
| Docker native scientific-worker image build | Passed |
| Compose readiness | Web, API, PostgreSQL, Redis all healthy |

The backend tests execute all 29 lesson templates. They also check deterministic OHLCV, GBM moments, flash-crash counterfactuals, next-open fills, transaction costs, initial-capital drawdown, month boundaries, NCAV/Graham examples, AMM invariants, concentrated range accounting, broker guards, factor recovery, portfolio constraints, forbidden code, account ownership, JWT revocation, version conflicts, and compute rate limits.

The six browser stories verify:

1. Lesson → Python run → chart/returns → saved experiment → quiz completion → research note → reload and experiment restore.
2. Registration and persistence across separate browser contexts, then sign-out isolation.
3. Valuation, factor regression, partial paper fills, stale-price rejection, and AMM results.
4. 390-pixel mobile navigation/search, readable lesson view, no horizontal overflow, and dark-theme persistence.
5. Unsynced edits surviving a reload and retrying when storage recovers.
6. Concurrent account revisions preserving both copies until the user explicitly chooses the server copy.

Agent-browser separately checked the overview and lesson reader through the Nginx deployment. The page, local Monaco worker, math, and navigation rendered without browser console errors or a Vite error overlay. Desktop and mobile layouts were inspected.

## Native container execution

The optional Docker worker was exercised with a real Pandas rolling-mean strategy and NumPy statistics on 1,260 bars. It returned the complete signal vector in approximately 725 ms, including container startup.

| Native check | Result |
| --- | --- |
| Scientific Python / Pandas strategy | Passed |
| Forbidden `os` import | Rejected |
| Infinite loop | Worker interrupted after two seconds of student execution (about 2.7 seconds including startup) |
| Allocation beyond 256 MiB | Container stopped; API runner reported failure |
| Container cleanup | No `quanta-run-*` containers remained |

These checks verify the configured behavior, not a comprehensive container-security audit. The default guided interpreter and optional native Python runtime have different capabilities and trust boundaries, described in the README.

## Local performance sample

Twenty sequential HTTP requests through the Docker web proxy used the default long/cash moving-average rule on a seeded five-year Heston dataset, returning 1,260 bars and full output each time:

- Median end-to-end latency: **99.6 ms**.
- Empirical p95 (nearest-rank): **128.3 ms**.
- Maximum: **130.1 ms**.

This is a local warmed-service sample, not a concurrency/load-test result or a claim about production p95. The PRD’s 1,000-path Monte Carlo and large historical-data targets have not been benchmarked.

## Operational notes

The workspace’s `.env` uses port **8088** because another application occupied port 8080. The local development launcher selected web port 5174 and API port 8001 because the default ports were also occupied. Other projects were left running.

First-time Docker registry startup had a transient timeout. Retrying after engine readiness succeeded. The full worker reuses the API’s locked scientific package environment to avoid maintaining a duplicate dependency installation.

Known nonblocking output: Vite warns about the lazily loaded Monaco/charts chunk sizes; those chunks are excluded from initial overview loading. The installed Starlette test client emits upstream deprecation warnings. No test failed in the final runs.

The scope document lists remaining production integrations and validation work; this release does not claim completion of the entire 18-week PRD.
