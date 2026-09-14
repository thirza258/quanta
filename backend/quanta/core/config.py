"""Filesystem defaults. Environment overrides preserve existing deployments."""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = PROJECT_ROOT / "backend"
STORAGE = Path(os.getenv("QUANTA_STORAGE", str(BACKEND_ROOT / "storage")))
DATA_DIR = Path(os.getenv("QUANTA_DATA_DIR", str(BACKEND_ROOT / "data")))
CATALOG_PATH = PROJECT_ROOT / "content/catalog/curriculum.json"
STORAGE.mkdir(parents=True, exist_ok=True)
