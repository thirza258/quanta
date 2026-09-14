"""Build deterministic source-only course downloads; never include installed dependencies or keys."""

from pathlib import Path
from shutil import copyfile
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = [
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
    for slug, archive, names, standalone in PROJECTS:
        source = ROOT / "course-projects" / slug
        target = ROOT / "public/course-assets" / slug
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
