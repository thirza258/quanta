"""Source attribution shared by generated course and lesson pages."""

import re

STOCKS = {
    "title": "U.S. SEC · Investor.gov: stocks and ownership",
    "url": "https://www.investor.gov/introduction-investing/investing-basics/investment-products/stocks",
}
ORDERS = {
    "title": "U.S. SEC · Investor.gov: trading orders and execution",
    "url": "https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-14",
}
RESEARCH_FINRA = {
    "title": "FINRA · Evaluating stocks and business fundamentals",
    "url": "https://www.finra.org/investors/investing/investment-products/stocks/evaluating-stocks",
}
RISK_ALLOCATION = {
    "title": "U.S. SEC · Investor.gov: asset allocation and risk",
    "url": "https://www.investor.gov/introduction-investing/getting-started/asset-allocation",
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
        "trading-fundamentals": [STOCKS, ORDERS, RESEARCH_FINRA, RISK_ALLOCATION],
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
