"""Canonical authored curriculum shared by the API and frontend build."""

import json

from quanta.core.config import CATALOG_PATH

CATALOG = json.loads(CATALOG_PATH.read_text())
LESSONS = {m["id"]: m for c in CATALOG for m in c["modules"]}
EXAMS = {exam["id"]: exam for course in CATALOG for exam in course["exams"]}
