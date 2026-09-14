# Verification results

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
