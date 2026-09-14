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
│   │   │   ├── research/           # Sandbox, valuation, factors, broker, AMM
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
│   │   ├── db/                     # SQLModel tables, engine, session lifecycle
│   │   ├── core/                   # Configuration, auth, limits, request guards
│   │   └── execution/              # Isolated runner and guided/native workers
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

The sidebar has a bounded `100dvh` container, a scrollable navigation region, and a fixed-size search/account region. Mobile navigation is inert while closed so offscreen controls cannot receive focus.

Course code carries an optional language field. Existing lessons default to Python and use the research sandbox; C lessons lazy-load the learning feature's local code lab, reuse the shared editor in C mode and save source drafts through the workspace provider. C compilation is a learner-side local workflow, not a new backend execution mode. Global CSS loads before course overrides so responsive card rules preserve their bottom spacing.

## Backend boundaries

`main.py` registers routers, lifecycle initialization, middleware, and domain-error translation. Routers declare HTTP paths, input models, identity/session dependencies, and rate limits. Services orchestrate use cases and version-checked transactions. Database models and session creation are separate from those operations.

Domain modules perform deterministic analytics, exam grading, and paper-account execution. Their rule errors are independent of FastAPI and translated to the existing HTTP response contract. The simulator separates its Decimal-based ledger engine from market generation/loading, snapshot queries, and persistent mutations. Isolated workers stay self-contained because they execute with Python's `-I` flag.

The backend reads `content/catalog/curriculum.json` directly. It does not load frontend source or require Node at runtime. Path defaults derive from the module's repository location rather than the process working directory. SQLite, the JWT secret, and historical datasets remain under `backend/storage/` and `backend/data/`; environment overrides and Compose volumes retain their existing meanings.

## Content ownership

Edit course builders in `content/authoring/` and project originals in `content/projects/`, then run:

```sh
npm run content:build
```

The catalog is generated once and consumed by both applications. Project downloads are copied or packaged into `frontend/public/course-assets/`. ZIP packaging includes only named source files, never dependencies, caches, data stores, or secrets. Generated files remain committed so a normal checkout builds without authoring tools.

Course ordering is independent of stable lesson IDs. The news course appears after Security Analysis and uses new `8.x` IDs; the C/HPC bot course follows Python bots using `9.x` IDs. Older courses, saved exercises, and exam versions keep their existing identifiers. Displayed track labels follow catalog order.

Algorithm evaluation/reporting closes the catalog with new `10.x` IDs. Its Python/Matplotlib report generator is a downloadable educational project under `content/projects/`, not a dependency of the running API or frontend. The generator accepts a language-independent valuation/timing export contract.

## Commands and deployment

From the root, `npm run setup`, `npm run dev`, `npm run build`, `npm test`, `npm run test:api`, and `npm run test:e2e` remain available. Frontend commands forward to the npm workspace. Dependencies are installed from the single root lock; do not introduce a second frontend lockfile.

The development launcher resolves paths from its own location, waits for API health, assigns the API proxy and allowed origin, and watches backend code plus the generated catalog. See the application-specific [frontend guide](../frontend/README.md) and [backend guide](../backend/README.md).

Compose uses the root build context with `frontend/Dockerfile` and `backend/Dockerfile`. The web image includes only the built static application at runtime; the API image includes Python code and the canonical catalog. The optional sandbox image copies `backend/quanta/execution/native_worker.py`. Rebuild without removing volumes:

```sh
docker compose up -d --build web api
```
