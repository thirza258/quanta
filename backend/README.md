# Backend

FastAPI application on Python 3.14, with a layered package under `quanta/`. HTTP routers, use-case services, calculation rules, database models/sessions, shared configuration, and isolated workers have separate directories. See [architecture](../docs/ARCHITECTURE.md).

From this directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn quanta.main:app --reload --reload-dir quanta --reload-dir ../content/catalog --reload-include '*.json' --host 127.0.0.1 --port 8000
.venv/bin/python -m pytest tests -q
```

Root `npm run setup` installs both applications. Root `npm run dev` connects the frontend proxy and API origin automatically. API docs are at `/docs` on the direct API port; the public web proxy exposes `/api/v1/`.

Configuration is in `quanta/core/config.py`. The generated catalog is `../content/catalog/curriculum.json`, independent of frontend source. Local SQLite and signing-secret files remain in `storage/`; imported Parquet data remains in `data/`. `DATABASE_URL`, `QUANTA_STORAGE`, and `QUANTA_DATA_DIR` override those locations. Preserve these files or Compose volumes across upgrades.

Historical import from this directory:

```sh
.venv/bin/python scripts/import_data.py prices.csv SYMBOL
```

The native-runtime check is `scripts/test_native.py`; it requires the optional sandbox image and a trusted local Docker engine. Build Docker images from the repository root using `backend/Dockerfile` and `backend/Dockerfile.sandbox`. Guided worker execution remains the default.

Course verification additionally requires a local C17 compiler (`cc`) and make: tests compile the 24 C worksheets and build the downloadable C/POSIX project in temporary directories. API worker execution remains Python-only; learners compile the C course locally through the frontend's C lab instructions. The optional sanitizer check is `make -C ../content/projects/c-hpc-trading sanitize` with a compiler supporting ASan/UBSan.
