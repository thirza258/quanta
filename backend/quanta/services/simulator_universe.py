"""Fictional listed companies for the simulator's generated market.

Every name, ticker, sector and starting price here is invented for teaching. None
of it describes a real issuer, and no generated series or headline is ever
labeled as observed market history.

Runs created before this universe existed keep LEGACY_SYMBOLS so their stored
positions, fills and cursors continue to resolve against the same bars.
"""

from dataclasses import dataclass

UNIVERSE_ID = "quanta-sim-v2"

# Symbol -> (display name, starting price) for runs created before UNIVERSE_ID.
LEGACY_SYMBOLS = {
    "AAPL": ("Apple", 224),
    "MSFT": ("Microsoft", 418),
    "NVDA": ("NVIDIA", 128),
    "TSLA": ("Tesla", 245),
    "AMZN": ("Amazon", 195),
    "META": ("Meta Platforms", 530),
}


@dataclass(frozen=True)
class Company:
    symbol: str
    name: str
    sector: str
    business: str
    price: float
    beta: float
    volatility: float
    volume: int
    news_rate: float


def _c(symbol, name, sector, business, price, beta, volatility, volume, news_rate=1.0):
    return Company(symbol, name, sector, business, price, beta, volatility, volume, news_rate)


COMPANIES = [
    _c(
        "NVRA",
        "Novara Microsystems",
        "Semiconductors",
        "accelerator silicon for data centers",
        148.50,
        1.45,
        0.46,
        26000,
        1.4,
    ),
    _c(
        "SILQ",
        "Siliqua Labs",
        "Semiconductors",
        "analog and power chips",
        92.20,
        1.30,
        0.50,
        18000,
        1.1,
    ),
    _c(
        "CLDS",
        "Cloudspire Systems",
        "Software",
        "cloud infrastructure software",
        212.40,
        1.15,
        0.35,
        14000,
        1.2,
    ),
    _c(
        "VRTL",
        "Vertalis Software",
        "Software",
        "enterprise resource planning suites",
        88.60,
        1.20,
        0.40,
        15000,
        1.0,
    ),
    _c(
        "QBIT",
        "Qubit Dynamics",
        "Software",
        "quantum computing research services",
        44.10,
        1.60,
        0.66,
        21000,
        1.3,
    ),
    _c(
        "DTAS",
        "Datastrata Analytics",
        "Software",
        "data warehousing and analytics",
        134.75,
        1.28,
        0.43,
        12000,
        1.0,
    ),
    _c(
        "AXTN",
        "Axionics Devices",
        "Hardware & robotics",
        "industrial sensors and controllers",
        61.80,
        1.18,
        0.39,
        13000,
        0.9,
    ),
    _c(
        "ZEPH",
        "Zephyr Robotics",
        "Hardware & robotics",
        "warehouse automation robots",
        19.95,
        1.75,
        0.74,
        34000,
        1.3,
    ),
    _c(
        "STVL",
        "Streamvale Media",
        "Media & telecom",
        "streaming entertainment",
        57.30,
        1.10,
        0.38,
        16000,
        1.1,
    ),
    _c(
        "ORBN",
        "Orbital Communications",
        "Media & telecom",
        "satellite connectivity",
        39.90,
        0.85,
        0.30,
        19000,
        0.9,
    ),
    _c(
        "HRVS",
        "Harvest Fields Foods",
        "Consumer staples",
        "packaged foods",
        71.25,
        0.60,
        0.20,
        11000,
        0.7,
    ),
    _c(
        "BBRW",
        "Brightbrew Beverages",
        "Consumer staples",
        "non-alcoholic beverages",
        52.40,
        0.55,
        0.19,
        12000,
        0.7,
    ),
    _c(
        "LUMR",
        "Lumira Retail Group",
        "Consumer discretionary",
        "specialty retail",
        118.90,
        1.05,
        0.33,
        10000,
        1.0,
    ),
    _c(
        "VLOC",
        "Velocity Motorworks",
        "Consumer discretionary",
        "electric vehicles",
        176.20,
        1.70,
        0.60,
        24000,
        1.5,
    ),
    _c(
        "HLXB",
        "Helix Biosciences",
        "Healthcare",
        "clinical-stage therapeutics",
        83.60,
        1.10,
        0.56,
        17000,
        1.4,
    ),
    _c(
        "PRNA",
        "Prana Therapeutics",
        "Healthcare",
        "rare-disease medicines",
        27.80,
        1.22,
        0.70,
        22000,
        1.4,
    ),
    _c(
        "MDCR",
        "Medicore Health Systems",
        "Healthcare",
        "hospital services and devices",
        145.30,
        0.70,
        0.24,
        9000,
        0.8,
    ),
    _c(
        "MRDN",
        "Meridian Financial Group",
        "Financials",
        "commercial banking",
        96.40,
        1.05,
        0.28,
        13000,
        0.9,
    ),
    _c(
        "ANCB",
        "Anchor Trust Bancorp",
        "Financials",
        "regional banking",
        48.75,
        0.95,
        0.31,
        14000,
        0.9,
    ),
    _c(
        "PAYN",
        "Paynode Holdings",
        "Financials",
        "payment processing",
        152.60,
        1.35,
        0.44,
        11000,
        1.1,
    ),
    _c(
        "SFGD",
        "Safeguard Mutual Insurance",
        "Financials",
        "property and casualty insurance",
        88.15,
        0.65,
        0.22,
        8000,
        0.7,
    ),
    _c(
        "TRVT",
        "Terravolt Energy",
        "Energy",
        "oil and gas production",
        64.20,
        1.00,
        0.36,
        20000,
        1.0,
    ),
    _c("HLSP", "Heliostat Power", "Energy", "utility-scale solar", 33.45, 1.40, 0.56, 23000, 1.2),
    _c(
        "CRSM",
        "Crossroad Midstream",
        "Energy",
        "pipelines and storage",
        41.10,
        0.80,
        0.26,
        12000,
        0.7,
    ),
    _c(
        "IRNW",
        "Ironworks Manufacturing",
        "Industrials",
        "heavy equipment",
        110.30,
        1.10,
        0.30,
        9000,
        0.8,
    ),
    _c(
        "AERV",
        "Aeroverse Systems",
        "Industrials",
        "aerospace components",
        198.70,
        1.05,
        0.32,
        8000,
        0.9,
    ),
    _c(
        "FRTL",
        "Freightline Logistics",
        "Industrials",
        "freight and logistics",
        76.90,
        1.15,
        0.34,
        10000,
        0.9,
    ),
    _c(
        "NIMB",
        "Nimbus Climate Systems",
        "Industrials",
        "building climate equipment",
        58.65,
        1.00,
        0.33,
        9000,
        0.8,
    ),
    _c(
        "GRDM",
        "Granite Ridge Materials",
        "Materials",
        "cement and aggregates",
        59.60,
        1.00,
        0.31,
        10000,
        0.8,
    ),
    _c("CPRA", "Copperra Mining", "Materials", "copper mining", 28.35, 1.30, 0.48, 26000, 1.0),
    _c(
        "HRZP",
        "Horizon Properties Trust",
        "Real estate & utilities",
        "logistics real estate",
        67.80,
        0.90,
        0.26,
        9000,
        0.7,
    ),
    _c(
        "PLSR",
        "Pulsar Utilities",
        "Real estate & utilities",
        "regulated electricity",
        81.45,
        0.50,
        0.17,
        8000,
        0.6,
    ),
]

BY_SYMBOL = {company.symbol: company for company in COMPANIES}
SECTORS = list(dict.fromkeys(company.sector for company in COMPANIES))
DEFAULT_WATCHLIST = ["NVRA", "CLDS", "VLOC", "HLXB", "MRDN", "TRVT", "ZEPH", "PLSR"]

DISCLOSURE = (
    "Simulated market · fictional companies, fictional headlines · "
    "no real issuer, security, or news organization is described"
)
LEGACY_DISCLOSURE = (
    "Seeded synthetic prices · fictional price paths printed against real company "
    "names · not observed market data, and no news or accounts are generated"
)
IMPORTED_DISCLOSURE = (
    "Imported historical OHLCV · used as supplied · no headlines, statements, or "
    "other content is generated for it"
)


def disclosure(config) -> str:
    """The provenance line for this run. Only a generated market may claim one."""
    if config.get("mode") == "historical":
        return IMPORTED_DISCLOSURE
    return DISCLOSURE if config.get("universe") == UNIVERSE_ID else LEGACY_DISCLOSURE


def universe(config) -> str | None:
    """The universe tag stored on a run. Older runs have no tag and stay legacy."""
    return config.get("universe")


def profile(symbol: str, tag: str | None) -> dict:
    """Display metadata for a quote, for either universe."""
    if tag == UNIVERSE_ID and symbol in BY_SYMBOL:
        company = BY_SYMBOL[symbol]
        return {"name": company.name, "sector": company.sector, "business": company.business}
    return {"name": LEGACY_SYMBOLS.get(symbol, (symbol,))[0], "sector": None, "business": None}


def listing(tag: str | None) -> list[dict]:
    """Symbols offered for new runs, or the legacy set for an older run."""
    if tag == UNIVERSE_ID:
        return [
            {
                "symbol": c.symbol,
                "name": c.name,
                "sector": c.sector,
                "business": c.business,
                "simulated": True,
            }
            for c in COMPANIES
        ]
    return [
        {"symbol": s, "name": v[0], "sector": None, "business": None, "simulated": True}
        for s, v in LEGACY_SYMBOLS.items()
    ]
