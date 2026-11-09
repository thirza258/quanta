# Backend

FastAPI application on Python 3.14, with a layered package under `quanta/`. HTTP routers, use-case services, calculation rules, database models/sessions, shared configuration, and isolated workers have separate directories. See [architecture](../docs/ARCHITECTURE.md).

From this directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
make -C engine
.venv/bin/python -m uvicorn quanta.main:app --reload --reload-dir quanta --reload-dir ../content/catalog --reload-include '*.json' --host 127.0.0.1 --port 8000
.venv/bin/python -m pytest tests -q
```

The trading simulator's computation (generated market, execution engine, per-bar analytics) is the C++17 library in `engine/`, loaded through `quanta/engine`. Build it with `make -C engine` before starting the API or running tests, and again after changing its sources; `make -C engine test`, `make -C engine sanitize` and `make -C engine bench` run its own tests, the AddressSanitizer/UndefinedBehaviorSanitizer build and the paired benchmark. `tests/test_engine_parity.py` holds it to the Python implementations it replaced, kept in `tests/reference/`. See the [engine guide](engine/README.md).

Root `npm run setup` installs both applications. Root `npm run dev` connects the frontend proxy and API origin automatically. API docs are at `/docs` on the direct API port; the public web proxy exposes `/api/v1/`.

Configuration is in `quanta/core/config.py`. The generated catalog is `../content/catalog/curriculum.json`, independent of frontend source. Local SQLite and signing-secret files remain in `storage/`; imported Parquet data remains in `data/`. `DATABASE_URL`, `QUANTA_STORAGE`, and `QUANTA_DATA_DIR` override those locations. Preserve these files or Compose volumes across upgrades.

Research registry runs (`/api/v1/research`) are background jobs inside the API process: two execute at once, eight may be queued or running, and each owner may have one active run. Their sandbox calls share `QUANTA_RESEARCH_WORKERS` threads (by default the smaller of 4 and the CPU count; Compose sets 2). Status and heartbeats are stored in the database, so after a restart or `--reload` the runs that were in flight are reported as interrupted once 90 seconds pass without a heartbeat (600 while queued). Provenance records the deployed commit from `QUANTA_GIT_COMMIT`, or from `git rev-parse HEAD` when the checkout has a `.git` directory; the Docker image has none, so set the variable there. See the [research platform guide](../docs/RESEARCH_PLATFORM.md).

Historical import from this directory:

```sh
.venv/bin/python scripts/import_data.py prices.csv SYMBOL
```

The native-runtime check is `scripts/test_native.py`; it requires the optional sandbox image and a trusted local Docker engine. Build Docker images from the repository root using `backend/Dockerfile` and `backend/Dockerfile.sandbox`. Guided worker execution remains the default.

Course verification additionally requires a local C17 compiler (`cc`) and make: tests compile the 24 C worksheets and build the downloadable C/POSIX project in temporary directories. API worker execution remains Python-only; learners compile the C course locally through the frontend's C lab instructions. The optional sanitizer check is `make -C ../content/projects/c-hpc-trading sanitize` with a compiler supporting ASan/UBSan.
