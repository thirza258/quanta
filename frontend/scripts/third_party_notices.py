"""Collect installed production-package license and notice files for distribution.

Run after npm ci. This inventory preserves supplied notices; it is not a legal opinion.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
lock = json.loads((ROOT / "package-lock.json").read_text())
sections = [
    "Quanta — third-party software notices\n\nInstalled production dependency notices.\nCourse sources and source-use information: /library\n"
]
for relative, item in sorted(lock["packages"].items()):
    if not relative or item.get("dev") or item.get("link") or "node_modules/" not in relative:
        continue
    directory = ROOT / relative
    if not directory.is_dir():
        continue
    manifest_path = directory / "package.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    name = manifest.get("name", relative)
    section = f"\n{'=' * 72}\n{name} {item.get('version', '')}\nDeclared license: {manifest.get('license', item.get('license', 'See package distribution'))}\n"
    if name == "lightweight-charts":
        # NOTICE is absent from the npm 5.2.1 tarball; preserve the release's upstream notice.
        section += "\nTradingView Lightweight Charts™\nCopyright (с) 2025 TradingView, Inc. https://www.tradingview.com/\nSource: https://github.com/tradingview/lightweight-charts/blob/v5.2.1/NOTICE\n"
    files = sorted(
        path
        for path in directory.iterdir()
        if path.is_file()
        and path.name.lower().split(".")[0]
        in {"license", "licence", "notice", "copying", "copyright", "ofl", "license-mit"}
    )
    for path in files:
        section += f"\n--- {path.name} ---\n{path.read_text(errors='replace')}\n"
    if not files:
        section += "\nConsult the package distribution for additional license information.\n"
    sections.append(section)
output = ROOT / "frontend/public/third-party-notices.txt"
output.write_text("\n".join(sections))
print(f"Collected {len(sections) - 1} installed production package entries.")
