"""Build deterministic source-only course downloads; never include installed dependencies or keys."""

from pathlib import Path
from shutil import copyfile
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[2]
PROJECTS = [
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
                copyfile(file, target / file.name)
    for slug, archive, names, standalone in PROJECTS:
        source = ROOT / "content/projects" / slug
        target = ROOT / "frontend/public/course-assets" / slug
        target.mkdir(parents=True, exist_ok=True)
        with ZipFile(target / archive, "w") as bundle:
            for name in names:
                entry = ZipInfo(name, date_time=(2026, 9, 14, 0, 0, 0))
                entry.compress_type = ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                bundle.writestr(entry, (source / name).read_bytes())
        for name in standalone:
            copyfile(source / name, target / name)


if __name__ == "__main__":
    package()
