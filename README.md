# Quanta

A focused investment learning workspace built from [PRD.md](PRD.md). The local platform has **fifteen courses spanning market fundamentals, trading ethics, hands-on workshops for the trading simulator and strategy lab, careful investing, security analysis, news, econometrics, strategy research, Python and C/HPC bots, Web3, stock machine learning, and a final algorithm evaluation/reporting track**, with a Docker deployment that includes the web app, API, PostgreSQL, and Redis.

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

Node 22+ and Python 3.14 are the tested runtimes. The trading simulator's engine is C++17, so the API also needs a C++ compiler (`c++`: Clang or GCC) and make; `npm run setup` builds it, and the [engine guide](backend/engine/README.md) covers its tests and benchmarks. Course verification and the downloadable C/HPC lab also require a local C17 compiler (`cc`) and make; see the [C course build guide](content/projects/c-hpc-trading/README.md).

```sh
npm run setup
npm run dev
```

The launcher waits for API health, selects available ports, and prints both URLs. Defaults are `http://127.0.0.1:5173` and API port `8000`. It leaves other applications running on those ports alone. Set `VITE_PORT` and `API_PORT` to require particular ports. Local state uses SQLite in `backend/storage/` and an in-process rate limiter.

For separate terminals, use `npm run dev:api` and `npm run dev:client`. The Vite proxy defaults to port 8000; override `API_TARGET` if needed. Standalone API deployments also need `ALLOWED_ORIGINS` configured for the client’s exact origin.

## What works

- Fifteen courses and 340 original reading modules, beginning with **Trading & market fundamentals**: eight beginner lessons, worked examples, 24 practice questions, key-term glossaries, and optional Python examples.
- **[Real-world applications in every lesson](docs/REAL_WORLD_CASES.md)**: 300 distinct tasks and worked explanations built around 35 Indonesian and global cases, with primary references, dated event context, unit links, and notebook prompts. Documented events and illustrative exercise data are clearly distinguished.
- Seventy-seven open-book assessments with 572 original exam questions, including four checkpoints and a new final for each expanded book course.
- **Lesson-linked practice missions** in the simulator: six fixed scenarios reachable straight from the lessons they serve, each with a brief and three objectives judged on the server from the run's own state. Objectives describe process — a limit entry, a thesis on every order, a position cap, a session held through a print — and never read P&L, because a profitable breach of a rule is still a breach.
- **[Research extensions in lessons](content/README.md#research-extensions)**: a closing *Go deeper: what the research says* section that adds the mechanisms, findings and disagreements behind a lesson, written in Quanta's own words from 2–4 verified sources with at least one arXiv paper where a relevant one exists. 69 lessons carry one so far — every lesson of Trading & market fundamentals, Trading ethics and Algorithm evaluation, plus the first verified lessons of Intelligent investor, News, Strategy lab, Econometrics and Stock bots — drawing on 223 distinct sources (60 arXiv papers). Every cited paper is matched against arXiv or Crossref, and every figure against a verbatim snippet of its source, before it is merged; further lessons are added one by one as they pass.
- **[Trading simulator & strategy lab workshops](docs/TOOL_WORKSHOPS.md)**: two 12-lesson, 6-hour courses placed straight after trading ethics. The simulator workshop covers runs and seeds, the replay clock, the simulated newsroom, every order type, fill pricing, margin and short selling, company accounts, desk analytics, performance against the QX-200 and a charter-week capstone, and links all six practice missions. The lab workshop covers every Strategy lab tool — synthetic markets and scenarios, the guided Python runtime, backtest mechanics and metrics, valuation, the factor studio, robustness sweeps, the paper broker's guards, the AMM simulator, saved experiments and the notebook — with every default figure checked against the running engine.
- **[Learning resources](/resources)**: 52 books, courses, datasets and tools for going further, arranged from free to paid with topic filters and search, each linked to the Quanta courses it extends and checked against its provider's page.
- **[Trading ethics & market conduct](docs/TRADING_ETHICS.md)**: 16 lessons / 8 hours placed immediately after the fundamentals, so a learner settles whose interest a trade serves before learning to value or automate one. Four units cover duty and disclosure, market integrity, conduct in automated and quantitative work, and care, refusal and record. Every lesson ends in an explicit **do and do not** rule with a threshold and a check, and the course builds to a personal trading charter. 32 practice questions, four checkpoints and a 16-question final, referenced to CFA Institute, SEC, FINRA, ESMA and GIPS primary sources.
- **[The intelligent & careful investor](docs/INTELLIGENT_INVESTOR.md)**: 16 lessons / 8 hours directly before Security Analysis, inspired by Graham’s *The Intelligent Investor*. Covers temperament, speculation, liquidity, diversification, margin of safety, allocation, costs and independent judgment, with 32 practice questions, four checkpoints, a final and an original investor-plan workbook.
- **[Security Analysis](docs/BOOK_COURSES.md)**: 24 lessons following the 1940 book’s seven parts, separate modern extensions, 48 practice questions, and an investment committee capstone.
- **[Financial news to company & stock analysis](docs/NEWS_COURSE.md)**: 24 lessons immediately after Security Analysis, 12 hours of guided study, 48 practice questions, six checkpoints, and a final. Includes earnings, macro releases, rupiah/Bank Indonesia, commodity shocks, valuation, source verification, and a downloadable research memo pack.
- **[Quantitative Investment Analysis](docs/BOOK_COURSES.md)**: 40 lessons mapped to all 14 chapters of the fourth edition (including advanced extensions: term structure, Monte Carlo variance reduction, shrinkage, permutation tests, logistic regression, the fundamental law, Black–Litterman and VaR backtesting), 80 practice questions, and a reproducible research capstone. Both courses include reading plans, original worked cases, mathematical notation, executable worksheets, and notebook assignments with worked solutions.
- **[The strategy lab](docs/STRATEGY_LAB_COURSE.md)**: 32 lessons / 16 hours across eight units, 64 practice questions, eight checkpoints and a 32-question version-2 final. Includes value/quality, momentum/reversal, pairs, ML signals, portfolio construction and validation, plus a runnable multi-asset Python project with trade/position ledgers and exports for the reporting course.
- **[Algorithmic & AI stock bots](docs/STOCK_BOTS_COURSE.md)**: 48 lessons in twelve units, 96 practice questions, eleven checkpoints, a 48-question final, and a downloadable Python project with durable paper accounting, a small trained ridge model, and AI evidence-validation fixtures.
- **[Algorithmic trading II: C & high-performance computing](docs/C_HPC_COURSE.md)**: 24 lessons / 12 hours after the Python bot course, with 24 compiled C worksheets, a C editor, local downloads, six checkpoints and a final. The complete C/POSIX project includes a causal integer-cent ledger, deterministic serial/parallel sweeps, repeated timing and sanitizer tests; lessons also cover cache layout, SIMD, OpenMP, GPU and distributed design.
- **[Financial econometrics](docs/APPLIED_COURSES.md)**: 40 lessons covering OLS, robust inference, time series, volatility, factors, panel data, causal designs, maximum likelihood and GMM, asset-pricing tests, regime and state-space models, quantile regression and extreme value theory, with actual local regression and cointegration projects.
- **[Web3, cryptography & coin creation](docs/APPLIED_COURSES.md)**: 24 lessons and complete downloadable native-coin and ERC-20 projects, including signatures, Merkle proofs, atomic validation, local Solidity deployment, and supply/allowance tests.
- **[Machine learning for stocks](docs/APPLIED_COURSES.md)**: 24 thirty-minute lessons (12 hours of study and lab work) across the full data-to-monitoring lifecycle, with real ridge/forest/logistic training, held-out evaluation, saved pipelines, and batch inference.
- **[Algorithm evaluation & results reporting](docs/ALGORITHM_EVALUATION.md)** is the final track: 16 lessons / 8 hours, 32 practice questions, four checkpoints and a final. Its downloadable project produces JSON, Markdown, HTML, PNG and SVG results with net returns, benchmark comparison, risk, descriptive block uncertainty, C/HPC timing, provenance and a separate report rubric.
- Named references on every lesson and a shared source footer across all page types, a complete reference library, source-use guidance, and bundled dependency notices. Course cards wrap long text and use an open-book illustration.
- Untimed, open-book exams with exact pass thresholds, saved drafts, answer navigation, pre-submission review, explanations, topic-specific lesson links, retakes, and attempt history. Course progress includes both lesson completion and exam passes.
- Course completion certificates with eligibility checklists, server issuance, public verification by ID/link, saved learner names and issue dates, and a print layout for PDF export. Find them under **Certifications**.
- Online grading, account-owned submission logs, idempotent retries, and device grading when the API is unavailable. Existing lesson IDs and workspace progress remain compatible.
- Reading, split-pane, and full sandbox views; locally bundled Monaco Python editor with Cmd/Ctrl+Enter execution.
- A course AI assistant for lesson hints, debugging, and downloadable environment/code files, using the OpenAI Python package with OpenRouter. Optional editor/error context, file previews, project ZIPs, and code replacement with undo. See [assistant setup](docs/ASSISTANT.md).
- C lessons use a locally bundled C editor with saved drafts, reset, source download, expected-output reference and local compile commands. They do not send C to the Python runtime.
- Guest persistence and email/password accounts with Argon2 hashing, HttpOnly JWT session cookies, revocation, version-checked workspace sync, and recovery of unsynced drafts.
- Research notes, search, experiment snapshots, JSON/Markdown exports, responsive navigation, and persistent dark/light themes.
- Seeded GBM, Merton jump-diffusion, Heston variance, and Markov regime-switching paths; crash, stagflation, liquidity-crisis, random-walk, and flash-crash scenarios.
- A standalone [TradingView-style stock simulator](docs/SIMULATOR.md) at `/simulator`: persistent $100,000 paper accounts and 32 fictional companies across 12 sectors, whose one-minute prices are generated endlessly by a factor model driven by the run’s own simulated newsroom, where every headline carries a score of one basis point per point, with generated quarterly statements and consensus, imported historical replay, interactive charts/drawings/indicators, server-computed screening, risk and portfolio analytics computed by a C++17 engine that reproduces the original Python engine to the cent, four order types, partial fills, portfolio accounting, trade journals, exports, and mobile trading. Each new run draws a different market unless a seed is supplied. Imported historical prices never receive generated news or statements.
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

## Certifications

Open **Certifications** in the sidebar, or choose **View certificate** from a completed course or exam result. Complete every module and pass every current-version exam in a course, sign in, and enter the name to appear on its certificate. Creating an account carries over guest progress. Before issuance, the app syncs the workspace and the API checks its version, recorded module completion, and exam answers against the current catalog. Device attempts qualify after server regrading; client-supplied scores and pass flags are not trusted.

Certificates are stored separately from editable workspace data in an account-owned database table, created automatically on API startup. Each record keeps its original server-generated ID, name, issue date (displayed in UTC), course title, module IDs, exam versions, and study duration. A database constraint prevents duplicate issuance for the same account and course edition. Repeating a claim returns the original record, including after a lost response or workspace reset. Changed modules or exam versions require completing the updated requirements for a new certificate; earlier records remain verifiable. Workspace JSON exports contain learning progress; certificates are recovered separately from the issuer registry after sign-in.

Choose **Print / save PDF**, then **Save as PDF** in the browser print dialog to download a copy. Each certificate includes its public `/verify/{certificate-id}` link. **Copy verification link** shares that address; `/verify` also accepts a certificate ID. Public verification reads the original database record, without requiring sign-in or exposing account IDs, email addresses, or exam answers. Unknown IDs and temporarily unavailable verification have distinct states. Verification confirms issuer authenticity, not learner identity or professional accreditation: names and lesson completion are self-reported, and assessments are open book. The API must be reachable for issuance and verification; a downloaded PDF is usable offline.

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
| GET | `/api/v1/courses` | All fifteen courses, including exams, sourced real-world cases and research extensions |
| POST | `/api/v1/auth/register`, `/login`, `/logout` | Account lifecycle (same `/auth` prefix) |
| GET/POST/PUT | `/api/v1/simulator/...` | [Persistent trading account, observed prices and overlays, simulated news, generated statements, desk analytics, orders, replay, preferences, and journals](docs/SIMULATOR.md#http-interface) |
| GET | `/api/v1/auth/me` | Current session profile |
| GET / PUT | `/api/v1/workspace` | Account-owned, versioned state |
| POST | `/api/v1/exercises/{lesson_id}/submit` | Check `{answer, question}`; question defaults to zero for existing clients |
| POST | `/api/v1/exams/{exam_id}/submit` | Grade a complete versioned attempt; persist account submissions with retry deduplication |
| GET | `/api/v1/exams/{exam_id}/attempts` | Latest 50 submissions belonging to the signed-in account |
| GET / POST | `/api/v1/certificates` | List account-owned certificates / issue a certificate after checking course completion |
| GET | `/api/v1/certificates/{certificate_id}/verify` | Public lookup of an immutable issuer record |
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
npm run test:engine
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
backend/   API routes, services, domain rules, database, execution, C++ simulator engine, tests
content/   Original course builders, canonical catalog, and project sources
scripts/   Root development launcher
docs/      Architecture, course scope, and verification evidence
```

See [architecture](docs/ARCHITECTURE.md), [frontend development](frontend/README.md), and [backend development](backend/README.md). Root npm commands coordinate an npm workspace with dependencies declared in `frontend/package.json` and one root lockfile. Run `npm run content:build` after editing courses or downloadable projects. Compose builds `frontend/Dockerfile` and `backend/Dockerfile` with their shared content.

Implementation references: [FastAPI authentication](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/), [Vite](https://vite.dev/guide/), and [Lightweight Charts](https://tradingview.github.io/lightweight-charts/docs/series-types). Charts retain TradingView attribution. Fonts, Monaco, and math assets are served locally; the application needs no third-party CDN at runtime.
