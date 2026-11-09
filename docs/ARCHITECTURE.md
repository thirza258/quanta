# Project architecture

Quanta has two applications and one shared content source. Root files coordinate installation, local development, validation, and Compose. Public API paths, course/lesson IDs, browser storage keys, database tables, and persisted data locations remain stable.

```text
quanta/
├── frontend/
│   ├── src/
│   │   ├── app/                    # Routing and application composition
│   │   │   └── layout/             # Shell, sidebar, navigation, lesson search
│   │   ├── features/
│   │   │   ├── learning/           # Catalog, progression, course/lesson pages
│   │   │   ├── assessments/        # Exams, practice, assessment types
│   │   │   ├── research/           # Sandbox, valuation, factors, broker, AMM, experiment registry
│   │   │   ├── simulator/          # Terminal API, models, hooks, components
│   │   │   ├── workspace/          # Account UI, state, persistence, provider
│   │   │   ├── notebook/           # Notes and exports
│   │   │   └── references/         # Reference library and attribution
│   │   ├── shared/                 # HTTP client, generic widgets, formatting
│   │   └── styles/                 # Global design and responsive styles
│   ├── public/                     # Static assets and generated course downloads
│   ├── e2e/                        # Browser integration scenarios
│   ├── scripts/                    # Browser benchmark and dependency notices
│   ├── deploy/nginx.conf
│   ├── Dockerfile
│   └── package.json                # Frontend dependencies and scripts
├── backend/
│   ├── quanta/
│   │   ├── main.py                 # Stable ASGI composition root
│   │   ├── api/                    # HTTP dependencies and feature routers
│   │   ├── services/               # Use cases, transactions, data access
│   │   ├── domain/                 # Calculations, grading, execution rules, models
│   │   │   └── research/           # Research runs: validation, diagnostics, red team, provenance
│   │   ├── db/                     # SQLModel tables, engine, session lifecycle
│   │   ├── core/                   # Configuration, auth, limits, request guards
│   │   ├── engine/                 # ctypes binding to the C++ simulator engine
│   │   └── execution/              # Isolated runner and guided/native workers
│   ├── engine/                     # C++17 simulator engine: market, execution, analytics
│   │   ├── src/ include/           # Library sources and its C interface
│   │   ├── tests/ bench/           # Golden fixtures, sanitizer target, paired timing
│   │   └── Makefile                # make, make test, make sanitize, make bench
│   ├── scripts/                    # Historical import and native-runtime check
│   ├── tests/                      # API, numerical, execution, content invariants
│   ├── Dockerfile
│   └── Dockerfile.sandbox
├── content/
│   ├── authoring/                  # Original course builders and shared helpers
│   ├── catalog/curriculum.json     # Generated canonical catalog
│   ├── projects/                   # Original downloadable project sources
│   └── scripts/package_projects.py # Deterministic source-only downloads
├── scripts/dev.mjs                 # Starts both applications and connects ports
├── docs/
├── compose.yaml
├── package.json                    # npm workspace and common commands
└── package-lock.json               # One lock for the frontend workspace
```

## Frontend boundaries

`app/` assembles routes, providers, and the shell. Features own their pages, components, models, and hooks. Shared code provides generic facilities and does not import feature behavior. The `@/` alias points at frontend source; `@content/` points at the shared content directory. Existing route-level lazy loading is preserved.

The trading page composes a state/action hook, toolbar, chart workspace, status area, and market/order/run/help dialogs. Its HTTP client, typed state, preference normalization, indicators, order estimates, and export formatting have separate modules. Dialogs receive typed subsets of the ready terminal view. State and network effects remain outside the presentation components.

The previous combined lab file is divided into valuation, AMM, factor, and paper-broker components with a shared calculation hook. Workspace normalization and device-storage reads are separated from the provider that coordinates account synchronization. Course cards and illustrations belong to learning, while generic dialogs and loading states remain shared.

The research feature also holds the experiment registry. Its `ResearchHome`, `NewExperiment` and `ExperimentDetail` pages sit behind the lazily loaded `/research`, `/research/new` and `/research/:experimentId` routes. Their components are in `components/registry/` and `components/experiment/`, the pure, unit-tested helpers in `model/grid.ts` and `model/experiment.ts`, and the typed API contract in `model/registry.ts`. The registry is separate from the workspace's saved experiment snapshots at `/experiments`.

The sidebar has a bounded `100dvh` container, a scrollable navigation region, and a fixed-size search/account region. Mobile navigation is inert while closed so offscreen controls cannot receive focus.

Course code carries an optional language field. Existing lessons default to Python and use the research sandbox; C lessons lazy-load the learning feature's local code lab, reuse the shared editor in C mode and save source drafts through the workspace provider. C compilation is a learner-side local workflow, not a new backend execution mode. Global CSS loads before course overrides so responsive card rules preserve their bottom spacing.

## Backend boundaries

`main.py` registers routers, lifecycle initialization, middleware, and domain-error translation. Routers declare HTTP paths, input models, identity/session dependencies, and rate limits. Services orchestrate use cases and version-checked transactions. Database models and session creation are separate from those operations.

Domain modules perform deterministic analytics, exam grading, and paper-account execution. Their rule errors are independent of FastAPI and translated to the existing HTTP response contract. The trading simulator's computation runs in a C++17 engine, `backend/engine`, which the API loads in-process through `quanta.engine` (ctypes, no extra Python dependency): the generated market and the original six-path generator, the execution rules and their exact decimal ledger arithmetic, and the per-bar analytics (indicator series, chart bucketing, the account marked to market). `domain/simulator.py` keeps the interface the services always called and writes the engine's changes back into the stored run state; routes, persistence, idempotency, the newsroom's text, fundamentals and missions stay in Python. The engine reproduces the Python implementations it replaced to the cent and the character, and `backend/tests/reference/` keeps those implementations as the oracle its differential tests compare against. See the [engine guide](../backend/engine/README.md). Isolated workers stay self-contained because they execute with Python's `-I` flag.

The research registry follows the same layers:

- `api/routes/experiments.py` declares the `/api/v1/research` routes, the owner dependency and the `research` rate limit.
- `services/experiments.py` owns experiments, runs, strategy and dataset versions, the in-process background job queue and reproduction.
- `services/market_data.py` puts generated and imported bars behind one provider interface.
- `domain/research/` holds the pure computation: specification, metrics, validation, robustness, diagnostics, the red team, provenance and the research note. Every backtest it runs goes through `domain/analytics.py`.

Strategy code still runs only in the isolated workers, which now accept `strategy(data, params)` and provide causal trailing-window helpers. See the [research platform guide](RESEARCH_PLATFORM.md).

The backend reads `content/catalog/curriculum.json` directly. It does not load frontend source or require Node at runtime. Path defaults derive from the module's repository location rather than the process working directory. SQLite, the JWT secret, and historical datasets remain under `backend/storage/` and `backend/data/`; environment overrides and Compose volumes retain their existing meanings.

## Content ownership

Edit course builders in `content/authoring/` and project originals in `content/projects/`, then run:

```sh
npm run content:build
```

The catalog is generated once and consumed by both applications. Project downloads are copied or packaged into `frontend/public/course-assets/`. ZIP packaging includes only named source files, never dependencies, caches, data stores, or secrets. Generated files remain committed so a normal checkout builds without authoring tools. Catalog and download writers publish completed temporary files with atomic replacement, preventing readers from observing truncated files during regeneration. Complete generation before capturing a build snapshot across multiple assets.

Course ordering is independent of stable lesson IDs. The news course appears after Security Analysis and uses new `8.x` IDs; the C/HPC bot course follows Python bots using `9.x` IDs. The careful-investor companion precedes Security Analysis with `11.x` IDs. Security Analysis keeps `1.1`–`1.24` and adds an advanced Part IX with `1.25`–`1.31`; its final remains the same ID and moves to version 3. Eight case-driven advanced security-analysis courses use `15.x`–`22.x` and appear after the foundational, quantitative, and bot courses. Strategy Lab preserves `4.1`–`4.4` and their first exercise keys while expanding its final to version 2; prior attempts remain historical. Other courses and exam versions keep their existing identifiers. Displayed track labels follow catalog order.

Algorithm evaluation/reporting closes the catalog with new `10.x` IDs. Its Python/Matplotlib report generator is a downloadable educational project under `content/projects/`, not a dependency of the running API or frontend. The generator accepts a language-independent valuation/timing export contract.

## Commands and deployment

From the root, `npm run setup`, `npm run dev`, `npm run build`, `npm test`, `npm run test:api`, and `npm run test:e2e` remain available; `npm run build:engine` and `npm run test:engine` build and test the C++ engine, and `setup`, `dev`, `test:api` and `check` build it when it is out of date. Frontend commands forward to the npm workspace. Dependencies are installed from the single root lock; do not introduce a second frontend lockfile.

The development launcher resolves paths from its own location, builds the engine, waits for API health, assigns the API proxy and allowed origin, and watches backend code, the generated catalog and the built engine library, so `make -C backend/engine` after a C++ change restarts the API. See the application-specific [frontend guide](../frontend/README.md) and [backend guide](../backend/README.md).

Compose uses the root build context with `frontend/Dockerfile` and `backend/Dockerfile`. The web image includes only the built static application at runtime; the API image includes Python code, the canonical catalog and the engine library, which a separate build stage compiles and tests on the same Debian base before only the `.so` is copied across. The optional sandbox image copies `backend/quanta/execution/native_worker.py`. Rebuild without removing volumes:

```sh
docker compose up -d --build web api
```
