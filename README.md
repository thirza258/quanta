# Quanta

A focused investment learning workspace built from [PRD.md](PRD.md). The local platform has **twelve courses spanning market fundamentals, careful investing, security analysis, news, econometrics, strategy research, Python and C/HPC bots, Web3, stock machine learning, and a final algorithm evaluation/reporting track**, with a Docker deployment that includes the web app, API, PostgreSQL, and Redis.

## Run with Docker

Requires Docker Engine/Desktop with Compose v2. From this directory:

```sh
cp .env.example .env
docker compose up --build -d
```

Open **http://localhost:8080**. No API keys or account are required for guest learning and synthetic experiments. Create an account in the app to sync your workspace to PostgreSQL.

```sh
docker compose ps
docker compose logs -f api web
docker compose stop        # keeps containers and data
docker compose down        # removes containers; named data volumes remain
```

The first build downloads Python/Node dependencies. The web service waits for the API, PostgreSQL, and Redis health checks. Only the web port is published, bound to loopback by default. If port 8080 is occupied, set `PORT` and update both origins in `ALLOWED_ORIGINS` in `.env`.

Persistent volumes:

| Volume | Contents |
| --- | --- |
| `postgres_data` | Accounts, revoked/active sessions, exercise and exam submissions, workspace state |
| `api_storage` | Automatically generated signing secret |
| `market_data` | Imported Parquet datasets |
| `redis_data` | Shared request counters |

Do not add `-v` to `docker compose down` unless you intend to delete these volumes. Back up PostgreSQL with `docker compose exec -T postgres pg_dump -U quanta quanta > quanta-backup.sql`.

For a public deployment, set a strong alphanumeric `POSTGRES_PASSWORD` **before the initial database creation**, configure the exact HTTPS origin in `ALLOWED_ORIGINS`, set `COOKIE_SECURE=true`, and terminate TLS at a reverse proxy. Publish only the web service. `JWT_SECRET` is optional (at least 32 characters); otherwise it is generated once in `api_storage`. Existing database passwords must be changed in PostgreSQL as well as the environment. The API trusts forwarded headers only within the private Compose network; keep its port unexposed.

## Run locally

Node 22+ and Python 3.14 are the tested runtimes. Course verification and the downloadable C/HPC lab also require a local C17 compiler (`cc`) and make; see the [C course build guide](content/projects/c-hpc-trading/README.md).

```sh
npm run setup
npm run dev
```

The launcher waits for API health, selects available ports, and prints both URLs. Defaults are `http://127.0.0.1:5173` and API port `8000`. It leaves other applications running on those ports alone. Set `VITE_PORT` and `API_PORT` to require particular ports. Local state uses SQLite in `backend/storage/` and an in-process rate limiter.

For separate terminals, use `npm run dev:api` and `npm run dev:client`. The Vite proxy defaults to port 8000; override `API_TARGET` if needed. Standalone API deployments also need `ALLOWED_ORIGINS` configured for the client’s exact origin.

## What works

- Twelve courses and 300 original reading modules, beginning with **Trading & market fundamentals**: eight beginner lessons, worked examples, 24 practice questions, key-term glossaries, and optional Python examples.
- **[Real-world applications in every lesson](docs/REAL_WORLD_CASES.md)**: 300 distinct tasks and worked explanations built around 35 Indonesian and global cases, with primary references, dated event context, unit links, and notebook prompts. Documented events and illustrative exercise data are clearly distinguished.
- Seventy-seven open-book assessments with 572 original exam questions, including four checkpoints and a new final for each expanded book course.
- **[The intelligent & careful investor](docs/INTELLIGENT_INVESTOR.md)**: 16 lessons / 8 hours directly before Security Analysis, inspired by Graham’s *The Intelligent Investor*. Covers temperament, speculation, liquidity, diversification, margin of safety, allocation, costs and independent judgment, with 32 practice questions, four checkpoints, a final and an original investor-plan workbook.
- **[Security Analysis](docs/BOOK_COURSES.md)**: 24 lessons following the 1940 book’s seven parts, separate modern extensions, 48 practice questions, and an investment committee capstone.
- **[Financial news to company & stock analysis](docs/NEWS_COURSE.md)**: 24 lessons immediately after Security Analysis, 12 hours of guided study, 48 practice questions, six checkpoints, and a final. Includes earnings, macro releases, rupiah/Bank Indonesia, commodity shocks, valuation, source verification, and a downloadable research memo pack.
- **[Quantitative Investment Analysis](docs/BOOK_COURSES.md)**: 28 lessons mapped to all 14 chapters of the fourth edition, 56 practice questions, and a reproducible research capstone. Both courses include reading plans, original worked cases, mathematical notation, executable worksheets, and notebook assignments with worked solutions.
- **[The strategy lab](docs/STRATEGY_LAB_COURSE.md)**: 32 lessons / 16 hours across eight units, 64 practice questions, eight checkpoints and a 32-question version-2 final. Includes value/quality, momentum/reversal, pairs, ML signals, portfolio construction and validation, plus a runnable multi-asset Python project with trade/position ledgers and exports for the reporting course.
- **[Algorithmic & AI stock bots](docs/STOCK_BOTS_COURSE.md)**: 48 lessons in twelve units, 96 practice questions, eleven checkpoints, a 48-question final, and a downloadable Python project with durable paper accounting, a small trained ridge model, and AI evidence-validation fixtures.
- **[Algorithmic trading II: C & high-performance computing](docs/C_HPC_COURSE.md)**: 24 lessons / 12 hours after the Python bot course, with 24 compiled C worksheets, a C editor, local downloads, six checkpoints and a final. The complete C/POSIX project includes a causal integer-cent ledger, deterministic serial/parallel sweeps, repeated timing and sanitizer tests; lessons also cover cache layout, SIMD, OpenMP, GPU and distributed design.
- **[Financial econometrics](docs/APPLIED_COURSES.md)**: 32 lessons covering OLS, robust inference, time series, volatility, factors, panel data, and causal designs, with actual local regression and cointegration projects.
- **[Web3, cryptography & coin creation](docs/APPLIED_COURSES.md)**: 24 lessons and complete downloadable native-coin and ERC-20 projects, including signatures, Merkle proofs, atomic validation, local Solidity deployment, and supply/allowance tests.
- **[Machine learning for stocks](docs/APPLIED_COURSES.md)**: 24 thirty-minute lessons (12 hours of study and lab work) across the full data-to-monitoring lifecycle, with real ridge/forest/logistic training, held-out evaluation, saved pipelines, and batch inference.
- **[Algorithm evaluation & results reporting](docs/ALGORITHM_EVALUATION.md)** is the final track: 16 lessons / 8 hours, 32 practice questions, four checkpoints and a final. Its downloadable project produces JSON, Markdown, HTML, PNG and SVG results with net returns, benchmark comparison, risk, descriptive block uncertainty, C/HPC timing, provenance and a separate report rubric.
- Named references on every lesson and a shared source footer across all page types, a complete reference library, source-use guidance, and bundled dependency notices. Course cards wrap long text and use an open-book illustration.
- Untimed, open-book exams with exact pass thresholds, saved drafts, answer navigation, pre-submission review, explanations, topic-specific lesson links, retakes, and attempt history. Course progress includes both lesson completion and exam passes.
- Online grading, account-owned submission logs, idempotent retries, and device grading when the API is unavailable. Existing lesson IDs and workspace progress remain compatible.
- Reading, split-pane, and full sandbox views; locally bundled Monaco Python editor with Cmd/Ctrl+Enter execution.
- A course AI assistant for lesson hints, debugging, and downloadable environment/code files, using the OpenAI Python package with OpenRouter. Optional editor/error context, file previews, project ZIPs, and code replacement with undo. See [assistant setup](docs/ASSISTANT.md).
- C lessons use a locally bundled C editor with saved drafts, reset, source download, expected-output reference and local compile commands. They do not send C to the Python runtime.
- Guest persistence and email/password accounts with Argon2 hashing, HttpOnly JWT session cookies, revocation, version-checked workspace sync, and recovery of unsynced drafts.
- Research notes, search, experiment snapshots, JSON/Markdown exports, responsive navigation, and persistent dark/light themes.
- Seeded GBM, Merton jump-diffusion, Heston variance, and Markov regime-switching paths; crash, stagflation, liquidity-crisis, random-walk, and flash-crash scenarios.
- A standalone [TradingView-style stock simulator](docs/SIMULATOR.md) at `/simulator`: persistent $100,000 paper accounts, six synthetic stocks, imported historical replay, interactive charts/drawings/indicators, four order types, partial fills, portfolio accounting, trade journals, exports, and mobile trading.
- Long/cash backtesting using previous-close signals and next-open fills, commissions, slippage, same-asset buy-and-hold comparison, equity/candlestick/drawdown charts, monthly returns, and trade logs.
- CAGR, Sharpe, Sortino, drawdown, win rate, profit factor, alpha, beta, VaR, CVaR, and Calmar analytics. Undefined ratios are explicitly represented by `null`.
- NCAV, asset-recovery haircuts, Graham valuation, full-range and concentrated-liquidity AMM analysis, and simulated order fills with liquidity/stale-data/spread/drawdown guards.
- CAPM/FF3/Carhart4/FF5 OLS fits with HAC errors, chronological ridge validation, and a constrained minimum-variance portfolio API.
- CSV validation and Parquet/DuckDB historical OHLCV import. Historical data is never silently replaced with generated data.

See [implementation scope](docs/IMPLEMENTATION.md) for the PRD mapping and boundaries.

## Start with market fundamentals

Choose **Start learning** on a fresh workspace, or open `/curriculum/trading-fundamentals`. The course covers investing versus trading, stock ownership, market participants, indexes and funds, quotes and orders, returns and costs, financial statements, diversification, leverage, and a written paper-trading plan. Lessons include Investor.gov and FINRA references and original fictional examples.

Complete all three practice questions in each beginner lesson. After lesson 0.4, the checkpoint requires **6 of 8 correct (75%)**. After lesson 0.8, the final requires **13 of 16 correct (at least 80%)**. Specialist finals require at least 80%; the expanded 32-question Strategy Lab final requires 26 correct. Each exam displays its exact required count.

Course completion requires all its modules and exams. Later tracks stay available for experienced learners. New lessons use IDs `0.1`–`0.8`; existing `1.1`–`6.5` links, code drafts, and progress retain their original meanings.

Exam drafts and up to 20 attempts per exam (recent attempts plus the best result for the current version) travel with workspace sync/export. A failed retake preserves a prior pass for that exam version. Account submission logs can restore missing online results from the latest 50 submissions. Device-graded attempts sync as workspace data, but are not retroactively added to the online submission log. These are open-book learning assessments: the shared catalog includes answer explanations and keys, and workspace completion is not a tamper-proof credential.

If grading saves a result but the response is lost, reopening the exam restores the submitted result and clears its unchanged draft. Answers edited afterward stay saved; choose **Continue as a new attempt** to submit those edits separately, or **Review submitted attempt** to discard the edits and view the recorded answers.

## Course AI assistant

Open **Ask AI assistant** on a course or lesson. Choose help with understanding, environment setup, or code. Setup requests create downloadable project files for macOS, Windows, or Linux; compatible lesson code can be reviewed and applied to the editor with undo.

Add these values to the root `.env` to enable AI responses:

```dotenv
OPENROUTER_API_KEY=your-openrouter-key
OPENROUTER_MODEL=openai/gpt-4.1-mini
```

Run `backend/.venv/bin/python -m pip install -r backend/requirements.txt` after updating an existing local install, then restart `npm run dev`. For Docker, run `docker compose up --build -d`. The backend uses `openai.AsyncOpenAI` with `https://openrouter.ai/api/v1`; no key is sent to the browser. Choose a model with structured-output support. Without a key, lessons and course downloads remain available and the assistant shows its connection status.

See [assistant configuration and behavior](docs/ASSISTANT.md) for context sharing, limits, and verification.

## Python execution

**Guided runtime (default, including Compose):** student code is parsed and interpreted by a capability-limited AST interpreter in a fresh subprocess. It never calls native `eval` or `exec`. OS imports, filesystem access, network APIs, private attribute introspection, unbounded loops, and unsupported syntax fail closed. There is a two-second process deadline, an operation budget, and bounded code, series, variables, output, and arithmetic. Linux additionally applies a 256 MiB address-space limit and CPU/file-descriptor limits. macOS uses the time/operation/size bounds; its memory limit is not advertised as equivalent to Linux cgroups.

Supported syntax: variables, numeric/list literals, positional functions, `if`, bounded `for`, arithmetic, comparisons, bitwise series conjunction/disjunction, indexing, `print`, and selected `math`/`numpy` functions. This is a documented Python subset, not a complete interpreter.

```python
from math import sqrt
print("Daily volatility:", 0.2 / sqrt(252))

def strategy(data):
    return data["close"] > data["sma_50"]
```

Available series: `open`, `high`, `low`, `close`, `volume`, `returns`, `sma_50`, `sma_200`. The moving-average slider controls the `sma_50` column. Returns are Boolean or 0/1 long/cash signals. Fractional weights, shorts, and multi-asset portfolio execution are outside this backtester.

**Optional full Python containers:** for a local API process with access to a trusted Docker engine:

```sh
docker compose build api
docker build -f backend/Dockerfile.sandbox -t quanta-sandbox:local .
QUANTA_SANDBOX=docker npm run dev
```

Each run starts a disposable non-root container with no network, a read-only root, no host mounts, dropped capabilities, 256 MiB RAM, a PID cap, and a two-second student-code alarm. Image startup/imports have a separate 15-second outer watchdog. The worker reuses the API image’s locked scientific packages. Set the build argument `QUANTA_API_IMAGE` if your API image uses a different tag. Large scientific workloads can exceed the memory cap. The container is the isolation boundary; the import/AST checks are defense in depth. Run `backend/.venv/bin/python backend/scripts/test_native.py` to exercise the native worker and its rejection paths. The app’s standard Compose deployment does **not** mount a Docker socket. A production unrestricted-code service needs a separately operated hardened execution host (for example gVisor), authentication, queueing, and infrastructure review.

## Import historical data

Provide a licensed CSV with unique ISO dates and positive, consistent OHLC prices:

```csv
time,open,high,low,close,volume
2024-01-02,100,102,99,101,1000000
2024-01-03,101,103,100,102,1200000
```

Locally:

```sh
backend/.venv/bin/python backend/scripts/import_data.py prices.csv SPY
```

Docker:

```sh
docker compose cp prices.csv api:/tmp/prices.csv
docker compose exec api python backend/scripts/import_data.py /tmp/prices.csv SPY
```

Refresh the sandbox and choose **Historical data → SPY**. Existing symbols are not overwritten. Imported data must supply its own corporate-action treatment, historical universe, and availability timestamps. The importer does not claim to resolve survivorship bias or provide the PRD’s complete historical SEC/funding datasets.

## API

Interactive API documentation is at `/docs` on the development API URL. The public web proxy exposes `/api/v1/…` routes only.

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/api/v1/health` | API/database/Redis readiness |
| GET | `/api/v1/courses` | All twelve courses, including exams and sourced real-world cases |
| POST | `/api/v1/auth/register`, `/login`, `/logout` | Account lifecycle (same `/auth` prefix) |
| GET/POST/PUT | `/api/v1/simulator/...` | [Persistent trading account, observed prices, orders, replay, preferences, and journals](docs/SIMULATOR.md#http-interface) |
| GET | `/api/v1/auth/me` | Current session profile |
| GET / PUT | `/api/v1/workspace` | Account-owned, versioned state |
| POST | `/api/v1/exercises/{lesson_id}/submit` | Check `{answer, question}`; question defaults to zero for existing clients |
| POST | `/api/v1/exams/{exam_id}/submit` | Grade a complete versioned attempt; persist account submissions with retry deduplication |
| GET | `/api/v1/exams/{exam_id}/attempts` | Latest 50 submissions belonging to the signed-in account |
| GET | `/api/v1/data/catalog` | Installed historical datasets |
| POST | `/api/v1/data/synthetic/generate` | Seeded OHLCV bars |
| POST | `/api/v1/sandbox/execute` | Code, dataset config, metrics, series, trades, output |
| GET / POST | `/api/v1/assistant/status`, `/chat`, `/bundle` | AI connection status, course-grounded help, and generated project ZIPs (same `/assistant` prefix) |
| POST | `/api/v1/analytics/valuation`, `/amm`, `/factors`, `/portfolio` | Financial calculations (same `/analytics` prefix) |
| POST | `/api/v1/broker/order` | Stateless paper-account transition and fill event |

Factor input can include `rows`, with asset excess return in the first column and the selected model’s factors in the remaining columns; units are decimal daily returns. Omit `rows` for explicitly synthetic observations with planted coefficients. Portfolio input takes rows of simultaneous asset returns and a `max_weight` bound. Broker state is client-supplied and has no financial authority.

## Verification

```sh
npm run build
npm test
npm run test:api
# With the app running, use the URL printed by npm run dev:
TEST_URL=http://127.0.0.1:5173 npm run test:e2e
# Or test the complete container deployment:
TEST_URL=http://127.0.0.1:8080 npm run test:e2e
```

Browser tests use installed Google Chrome locally; in CI install Playwright Chromium (`npx playwright install --with-deps chromium`) and set `CI=true`.

See [verification results](docs/VERIFICATION.md) for the checks performed during implementation. The tests cover financial edge cases, every lesson template, restricted-code rejection, access control, version conflicts, historical storage, account persistence, and browser flows.

## Development map

```text
frontend/  React app, feature modules, browser tests, assets, Vite, and web image
backend/   API routes, services, domain rules, database, execution, and API tests
content/   Original course builders, canonical catalog, and project sources
scripts/   Root development launcher
docs/      Architecture, course scope, and verification evidence
```

See [architecture](docs/ARCHITECTURE.md), [frontend development](frontend/README.md), and [backend development](backend/README.md). Root npm commands coordinate an npm workspace with dependencies declared in `frontend/package.json` and one root lockfile. Run `npm run content:build` after editing courses or downloadable projects. Compose builds `frontend/Dockerfile` and `backend/Dockerfile` with their shared content.

Implementation references: [FastAPI authentication](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/), [Vite](https://vite.dev/guide/), and [Lightweight Charts](https://tradingview.github.io/lightweight-charts/docs/series-types). Charts retain TradingView attribution. Fonts, Monaco, and math assets are served locally; the application needs no third-party CDN at runtime.
