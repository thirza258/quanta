"""Check that every advertised project is downloadable and matches reviewed source."""

from pathlib import Path
from zipfile import ZipFile

from quanta.main import CATALOG

ROOT = Path(__file__).resolve().parents[2]


def test_all_course_resources_exist_and_are_not_empty():
    for course in CATALOG:
        for resource in course.get("resources", []):
            path = ROOT / "public" / resource["url"].lstrip("/")
            assert path.is_file(), path
            assert path.stat().st_size > 20


def test_source_archives_match_reviewed_project_and_exclude_local_state():
    for slug, archive in [("web3", "coin-lab.zip"), ("stock-ml", "stock-ml-lab.zip")]:
        with ZipFile(ROOT / "public/course-assets" / slug / archive) as bundle:
            assert "README.md" in bundle.namelist()
            for name in bundle.namelist():
                assert "/" not in name and not name.startswith(".")
                source = ROOT / "course-projects" / slug / name
                assert bundle.read(name) == source.read_bytes()
                if (ROOT / "public/course-assets" / slug / name).exists():
                    assert (
                        bundle.read(name)
                        == (ROOT / "public/course-assets" / slug / name).read_bytes()
                    )
