"""Build deterministic source-only course downloads; never include installed dependencies or keys."""

from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[2]
PROJECTS = [
    (
        "intelligent-investor",
        "careful-investor-workbook.zip",
        ["README.md", "investor-plan.md", "worked-cases.md"],
        ["README.md", "investor-plan.md"],
    ),
    (
        "strategy-lab",
        "strategy-research-lab.zip",
        [
            "README.md",
            "research-notebook.md",
            "strategy_lab.py",
            "test_strategy_lab.py",
            "prices.csv",
            "fundamentals.csv",
        ],
        ["README.md", "research-notebook.md"],
    ),
    (
        "algorithm-evaluation",
        "algorithm-report-lab.zip",
        [
            "README.md",
            "report-notebook.md",
            "evaluate.py",
            "test_evaluate.py",
            "requirements.txt",
            "manifest.example.json",
            "equity.example.csv",
            "timings.example.csv",
        ],
        ["README.md", "report-notebook.md"],
    ),
    (
        "c-hpc-trading",
        "c-hpc-bot-lab.zip",
        [
            "README.md",
            "performance-notebook.md",
            "quanta.h",
            "engine.c",
            "parallel.c",
            "main.c",
            "test.c",
            "Makefile",
        ],
        ["README.md", "performance-notebook.md"],
    ),
    (
        "news-to-markets",
        "news-analysis-pack.zip",
        ["README.md", "research-memo.md", "case-packet.md", "glossary.md", "case_analysis.py"],
        ["research-memo.md", "case-packet.md", "glossary.md"],
    ),
    (
        "web3",
        "coin-lab.zip",
        [
            "README.md",
            "LICENSE",
            "package.json",
            "package-lock.json",
            "CedarCoin.sol",
            "token-test.mjs",
            "native-chain.mjs",
            "native-chain.test.mjs",
        ],
        ["README.md", "CedarCoin.sol", "native-chain.mjs"],
    ),
    (
        "stock-ml",
        "stock-ml-lab.zip",
        ["README.md", "requirements.txt", "stock_ml_lab.py", "test_stock_ml_lab.py"],
        ["README.md", "requirements.txt", "stock_ml_lab.py"],
    ),
]


def package():
    # Standalone originals share the same ownership rule as zipped projects.
    for slug in ("research", "stock-bots"):
        source = ROOT / "content/projects" / slug
        target = ROOT / "frontend/public/course-assets" / slug
        target.mkdir(parents=True, exist_ok=True)
        for file in sorted(source.iterdir()):
            if file.is_file() and file.suffix in (".py", ".md", ".txt", ".csv"):
                publish_copy(file, target / file.name)
    for slug, archive, names, standalone in PROJECTS:
        source = ROOT / "content/projects" / slug
        target = ROOT / "frontend/public/course-assets" / slug
        target.mkdir(parents=True, exist_ok=True)
        with TemporaryDirectory(dir=target) as staging:
            pending = Path(staging) / archive
            with ZipFile(pending, "w") as bundle:
                for name in names:
                    entry = ZipInfo(name, date_time=(2026, 9, 14, 0, 0, 0))
                    entry.compress_type = ZIP_DEFLATED
                    entry.external_attr = 0o100644 << 16
                    bundle.writestr(entry, (source / name).read_bytes())
            pending.replace(target / archive)
        for name in standalone:
            publish_copy(source / name, target / name)


def publish_copy(source, target):
    with TemporaryDirectory(dir=target.parent) as staging:
        pending = Path(staging) / target.name
        copyfile(source, pending)
        pending.replace(target)


if __name__ == "__main__":
    package()
