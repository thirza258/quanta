"""Check that every advertised project is downloadable and matches reviewed source."""

from pathlib import Path
from zipfile import ZipFile

from quanta.domain.catalog import CATALOG

ROOT = Path(__file__).resolve().parents[2]


def test_all_course_resources_exist_and_are_not_empty():
    for course in CATALOG:
        for resource in course.get("resources", []):
            path = ROOT / "frontend/public" / resource["url"].lstrip("/")
            assert path.is_file(), path
            assert path.stat().st_size > 20


def test_source_archives_match_reviewed_project_and_exclude_local_state():
    for slug, archive in [
        ("web3", "coin-lab.zip"),
        ("stock-ml", "stock-ml-lab.zip"),
        ("news-to-markets", "news-analysis-pack.zip"),
        ("c-hpc-trading", "c-hpc-bot-lab.zip"),
        ("algorithm-evaluation", "algorithm-report-lab.zip"),
        ("strategy-lab", "strategy-research-lab.zip"),
        ("intelligent-investor", "careful-investor-workbook.zip"),
    ]:
        with ZipFile(ROOT / "frontend/public/course-assets" / slug / archive) as bundle:
            assert "README.md" in bundle.namelist()
            for name in bundle.namelist():
                assert "/" not in name and not name.startswith(".")
                source = ROOT / "content/projects" / slug / name
                assert bundle.read(name) == source.read_bytes()
                if (ROOT / "frontend/public/course-assets" / slug / name).exists():
                    assert (
                        bundle.read(name)
                        == (ROOT / "frontend/public/course-assets" / slug / name).read_bytes()
                    )
