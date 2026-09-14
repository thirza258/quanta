"""Source attribution shared by generated course and lesson pages."""

import re

STOCKS = {
    "title": "U.S. SEC · Investor.gov: stocks and ownership",
    "url": "https://www.investor.gov/introduction-investing/investing-basics/investment-products/stocks",
}
FACTORS = {
    "title": "Kenneth R. French · Data Library and factor methodology",
    "url": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html",
}
VALIDATION = {
    "title": "scikit-learn contributors · Common pitfalls and recommended practices",
    "url": "https://scikit-learn.org/stable/common_pitfalls.html",
}


def attach_references(catalog):
    fallback = {
        "trading-fundamentals": [STOCKS],
        "econometrics": [FACTORS, VALIDATION],
        "strategy-lab": [VALIDATION, FACTORS],
        "web3": [
            {"title": "Uniswap Labs · Protocol documentation", "url": "https://docs.uniswap.org/"}
        ],
    }
    for track in catalog:
        track.setdefault("references", fallback.get(track["id"], [STOCKS]))
        for module in track["modules"]:
            sources = list(module.get("references", track["references"]))
            for title, url in re.findall(r"\[([^\]]+)\]\((https://[^\s)]+)\)", module["content"]):
                if not any(source["url"] == url for source in sources):
                    sources.append({"title": title, "url": url})
            module["references"] = sources
