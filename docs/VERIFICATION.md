# Verification results

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
