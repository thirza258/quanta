import os
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
_tmp = tempfile.TemporaryDirectory(prefix="quanta-tests-")
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp.name}/test.db"
os.environ["QUANTA_STORAGE"] = _tmp.name
os.environ["QUANTA_DATA_DIR"] = f"{_tmp.name}/data"
os.environ.pop("REDIS_URL", None)
os.environ["QUANTA_SANDBOX"] = "guided"
from fastapi.testclient import TestClient
from quanta.limits import limiter
from quanta.main import app


@pytest.fixture
def client():
    limiter.records.clear()
    with TestClient(app) as instance:
        yield instance
