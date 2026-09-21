"""Invented financial statements for the simulator's fictional companies.

Every figure is generated. No filing, issuer or reported result is described, and
nothing here is derived from real company accounts.

A company's structural identity — shares outstanding, sector margins, the
valuation it starts from — is a stable function of its ticker, so the same
fictional company looks like the same business in every run. What varies with the
run seed is how it then performs: each reported quarter carries its own growth,
margin and surprise, and the newsroom releases it on the bar where the price
reacts to it.

Statements are built to tie together: the balance sheet balances because equity
is the residual, and each quarter's closing cash is the prior quarter's cash plus
that quarter's modeled cash flows.
"""

import hashlib

import numpy as np

# Per sector: price/earnings anchor, gross margin, operating margin, revenue
# growth, capital intensity, leverage and payout. Ranges, sampled per company.
PROFILES = {
    "Semiconductors": dict(
        pe=(20, 34),
        gross=(0.46, 0.60),
        operating=(0.20, 0.31),
        growth=(0.06, 0.26),
        capex=(0.08, 0.15),
        leverage=(0.10, 0.30),
        payout=(0.0, 0.25),
        seasonality=0.07,
    ),
    "Software": dict(
        pe=(26, 48),
        gross=(0.70, 0.86),
        operating=(0.16, 0.30),
        growth=(0.08, 0.28),
        capex=(0.03, 0.07),
        leverage=(0.05, 0.28),
        payout=(0.0, 0.15),
        seasonality=0.05,
    ),
    "Hardware & robotics": dict(
        pe=(16, 28),
        gross=(0.34, 0.46),
        operating=(0.09, 0.18),
        growth=(0.04, 0.18),
        capex=(0.06, 0.12),
        leverage=(0.15, 0.38),
        payout=(0.0, 0.25),
        seasonality=0.08,
    ),
    "Media & telecom": dict(
        pe=(12, 22),
        gross=(0.42, 0.58),
        operating=(0.12, 0.22),
        growth=(0.0, 0.10),
        capex=(0.10, 0.20),
        leverage=(0.25, 0.50),
        payout=(0.15, 0.45),
        seasonality=0.09,
    ),
    "Consumer staples": dict(
        pe=(16, 24),
        gross=(0.32, 0.44),
        operating=(0.11, 0.18),
        growth=(0.01, 0.07),
        capex=(0.04, 0.08),
        leverage=(0.20, 0.42),
        payout=(0.35, 0.65),
        seasonality=0.06,
    ),
    "Consumer discretionary": dict(
        pe=(14, 30),
        gross=(0.28, 0.44),
        operating=(0.07, 0.16),
        growth=(0.02, 0.18),
        capex=(0.05, 0.12),
        leverage=(0.18, 0.44),
        payout=(0.05, 0.35),
        seasonality=0.14,
    ),
    "Healthcare": dict(
        pe=(15, 30),
        gross=(0.52, 0.74),
        operating=(0.12, 0.26),
        growth=(0.03, 0.16),
        capex=(0.04, 0.09),
        leverage=(0.15, 0.38),
        payout=(0.10, 0.40),
        seasonality=0.05,
    ),
    "Financials": dict(
        pe=(9, 16),
        gross=(0.60, 0.78),
        operating=(0.28, 0.42),
        growth=(0.01, 0.11),
        capex=(0.02, 0.05),
        leverage=(0.35, 0.60),
        payout=(0.25, 0.55),
        seasonality=0.04,
    ),
    "Energy": dict(
        pe=(8, 16),
        gross=(0.26, 0.42),
        operating=(0.10, 0.24),
        growth=(-0.06, 0.16),
        capex=(0.12, 0.24),
        leverage=(0.22, 0.46),
        payout=(0.20, 0.55),
        seasonality=0.11,
    ),
    "Industrials": dict(
        pe=(14, 24),
        gross=(0.26, 0.38),
        operating=(0.09, 0.17),
        growth=(0.01, 0.11),
        capex=(0.05, 0.11),
        leverage=(0.22, 0.45),
        payout=(0.20, 0.45),
        seasonality=0.08,
    ),
    "Materials": dict(
        pe=(9, 18),
        gross=(0.20, 0.34),
        operating=(0.08, 0.18),
        growth=(-0.05, 0.14),
        capex=(0.10, 0.20),
        leverage=(0.25, 0.48),
        payout=(0.15, 0.45),
        seasonality=0.10,
    ),
    "Real estate & utilities": dict(
        pe=(14, 22),
        gross=(0.50, 0.68),
        operating=(0.24, 0.38),
        growth=(0.0, 0.06),
        capex=(0.14, 0.26),
        leverage=(0.40, 0.62),
        payout=(0.45, 0.80),
        seasonality=0.05,
    ),
}
# Companies still investing ahead of profit. Priced on revenue, not earnings.
DEVELOPMENT_STAGE = {"QBIT", "ZEPH", "PRNA", "HLXB", "HLSP"}
HISTORY = 8
# The run opens in January 2025, so the eight quarters already on file end with
# Q3 2024, and the quarter reported during the run is Q4 2024.
QUARTER_LABELS = [
    "Q4 2022",
    "Q1 2023",
    "Q2 2023",
    "Q3 2023",
    "Q4 2023",
    "Q1 2024",
    "Q2 2024",
    "Q3 2024",
    "Q4 2024",
    "Q1 2025",
    "Q2 2025",
    "Q3 2025",
]


def _stable(symbol: str) -> np.random.Generator:
    """A company's structure is the same in every run; only its results vary."""
    digest = hashlib.sha256(f"quanta-fundamentals:{symbol}".encode()).hexdigest()
    return np.random.default_rng(int(digest[:16], 16))


def structure(company) -> dict:
    """Shares outstanding, margin profile and starting valuation for a company."""
    rng = _stable(company.symbol)
    profile = PROFILES[company.sector]
    development = company.symbol in DEVELOPMENT_STAGE
    capitalization = float(np.exp(rng.uniform(np.log(1800), np.log(210000))))
    shares = round(capitalization / company.price, 1)
    gross = float(rng.uniform(*profile["gross"]))
    operating = float(rng.uniform(*profile["operating"]))
    growth = float(rng.uniform(*profile["growth"]))
    if development:
        # Priced on sales while operating margin is still negative.
        sales_multiple = float(rng.uniform(4.0, 14.0))
        revenue = capitalization / sales_multiple / 4
        operating = -float(rng.uniform(0.05, 0.38))
        growth = float(rng.uniform(0.18, 0.55))
    else:
        earnings_multiple = float(rng.uniform(*profile["pe"]))
        revenue = capitalization / earnings_multiple / (operating * 0.76) / 4
    return {
        "shares": shares,
        "revenue": revenue,
        "gross_margin": gross,
        "operating_margin": operating,
        "growth": growth,
        "capex_intensity": float(rng.uniform(*profile["capex"])),
        "leverage": float(rng.uniform(*profile["leverage"])),
        "payout": 0.0 if development else float(rng.uniform(*profile["payout"])),
        "seasonality": profile["seasonality"],
        "tax_rate": 0.0 if development else float(rng.uniform(0.15, 0.26)),
        "development_stage": development,
        "fiscal_year_end": "31 December",
        "employees": int(rng.integers(900, 145000)),
    }


def _quarter(company, shape, index, label, revenue, margin, previous, released):
    """One consistent set of statements. Equity is the residual, so it balances."""
    shares = shape["shares"]
    gross = revenue * shape["gross_margin"]
    operating = revenue * margin
    overhead = gross - operating
    research = overhead * (0.42 if shape["gross_margin"] > 0.55 else 0.22)
    depreciation = revenue * shape["capex_intensity"] * 0.7
    ebitda = operating + depreciation
    debt = max(0.0, revenue * 4 * shape["leverage"] * 1.4)
    interest = debt * 0.0125
    pretax = operating - interest
    tax = max(0.0, pretax) * shape["tax_rate"]
    net = pretax - tax
    eps = net / shares

    receivables = revenue * 0.82
    inventory = revenue * (0.55 if shape["gross_margin"] < 0.5 else 0.18)
    payables = revenue * 0.36
    ppe = revenue * 4 * shape["capex_intensity"] * 2.6
    goodwill = revenue * 4 * 0.35
    capex = revenue * shape["capex_intensity"]
    working_capital_change = (
        (receivables - previous["receivables"])
        + (inventory - previous["inventory"])
        - (payables - previous["payables"])
        if previous
        else 0.0
    )
    operating_cash = net + depreciation - working_capital_change
    free_cash = operating_cash - capex
    dividends = max(0.0, net) * shape["payout"]
    buybacks = max(0.0, free_cash - dividends) * (0.35 if not shape["development_stage"] else 0.0)
    opening_cash = previous["cash"] if previous else revenue * 1.8
    # A company that would fall below a working cash minimum raises the shortfall
    # rather than finding it. The borrowing is on the balance sheet and on the
    # financing line, so closing cash still equals the roll-forward exactly.
    unfinanced = opening_cash + operating_cash - capex - dividends - buybacks
    external = max(0.0, revenue * 0.15 - unfinanced)
    financing = external - dividends - buybacks
    cash = unfinanced + external

    current_assets = cash + receivables + inventory
    total_assets = current_assets + ppe + goodwill
    # Drawn at the quarter end, so it carries no interest in this period.
    short_debt = debt * 0.22 + external
    current_liabilities = payables + short_debt + revenue * 0.14
    long_debt = debt - debt * 0.22
    total_debt = debt + external
    total_liabilities = current_liabilities + long_debt + revenue * 0.25
    return {
        "label": label,
        "index": index,
        "released": released,
        "revenue": revenue,
        "cost_of_revenue": revenue - gross,
        "gross_profit": gross,
        "research_development": research,
        "selling_general_admin": overhead - research,
        "depreciation": depreciation,
        "operating_income": operating,
        "ebitda": ebitda,
        "interest_expense": interest,
        "pretax_income": pretax,
        "tax_expense": tax,
        "net_income": net,
        "eps": eps,
        "shares": shares,
        "cash": cash,
        "receivables": receivables,
        "inventory": inventory,
        "current_assets": current_assets,
        "property_plant_equipment": ppe,
        "goodwill": goodwill,
        "total_assets": total_assets,
        "payables": payables,
        "short_term_debt": short_debt,
        "current_liabilities": current_liabilities,
        "long_term_debt": long_debt,
        "total_debt": total_debt,
        "total_liabilities": total_liabilities,
        "equity": total_assets - total_liabilities,
        "operating_cash_flow": operating_cash,
        "capital_expenditure": capex,
        "free_cash_flow": free_cash,
        "dividends_paid": dividends,
        "buybacks": buybacks,
        "external_financing": external,
        "financing_cash_flow": financing,
        "opening_cash": opening_cash,
    }


def opening_book(company, rng) -> list[dict]:
    """Quarters already reported when a run begins. Always available to read."""
    shape = structure(company)
    quarters, previous = [], None
    revenue = shape["revenue"] / (1 + shape["growth"]) ** (HISTORY / 4)
    for step in range(HISTORY):
        seasonal = 1 + shape["seasonality"] * np.sin((step % 4) * np.pi / 2)
        revenue *= (1 + shape["growth"]) ** 0.25 * float(rng.normal(1, 0.022))
        margin = shape["operating_margin"] * float(rng.normal(1, 0.05))
        quarter = _quarter(
            company, shape, -1, QUARTER_LABELS[step], revenue * seasonal, margin, previous, True
        )
        quarters.append(quarter)
        previous = quarter
    return quarters


def next_report(company, book, rng, surprise, index, position) -> dict:
    """The quarter the newsroom releases during the run, on the bar that reacts."""
    shape = structure(company)
    previous = book[-1]
    # The same quarter a year earlier already carries this quarter's seasonality,
    # so growth applies to it directly rather than seasonalizing a second time.
    year_ago = book[-4] if len(book) >= 4 else book[0]
    base = year_ago["revenue"] * (1 + shape["growth"])
    revenue = base * (1 + 0.55 * surprise) * float(rng.normal(1, 0.012))
    margin = shape["operating_margin"] * (1 + 0.9 * surprise)
    quarter = _quarter(
        company,
        shape,
        index,
        QUARTER_LABELS[min(len(book), len(QUARTER_LABELS) - 1)],
        revenue,
        margin,
        previous,
        False,
    )
    # Consensus is what the simulated street expected before the print, so a
    # learner can compute the surprise from published numbers alone. It carries
    # its own dispersion rather than being an exact inverse of the reported
    # figures, so the unreleased result cannot be solved for in advance.
    reported = quarter["eps"]
    consensus_revenue = revenue / (1 + 0.55 * surprise) * (1 + float(rng.normal(0, 0.014)))
    # Stated as a distance from the reported figure, so a beat is above consensus
    # whether the company earns or loses money.
    step = abs(reported) if abs(reported) > 1e-6 else abs(revenue * 0.02 / shape["shares"])
    consensus_eps = reported - surprise * step * (1 + float(rng.normal(0, 0.06)))
    quarter["consensus_revenue"] = consensus_revenue
    quarter["consensus_eps"] = consensus_eps
    quarter["revenue_surprise"] = revenue / consensus_revenue - 1
    quarter["eps_surprise"] = (
        (reported - consensus_eps) / abs(consensus_eps) if abs(consensus_eps) > 1e-9 else None
    )
    quarter["position"] = position
    return quarter


def _trailing(book, key):
    return sum(q[key] for q in book[-4:])


def valuation(company, book, price) -> dict:
    """Ratios a learner would compute from the released statements and the mark."""
    latest = book[-1]
    shares = latest["shares"]
    capitalization = price * shares
    net_debt = latest["total_debt"] - latest["cash"]
    enterprise = capitalization + net_debt
    revenue = _trailing(book, "revenue")
    earnings = _trailing(book, "net_income")
    ebitda = _trailing(book, "ebitda")
    free_cash = _trailing(book, "free_cash_flow")
    dividends = _trailing(book, "dividends_paid")
    equity = latest["equity"]
    prior_year = book[-5] if len(book) >= 5 else None
    prior_revenue = sum(q["revenue"] for q in book[-8:-4]) if len(book) >= 8 else None
    prior_earnings = sum(q["net_income"] for q in book[-8:-4]) if len(book) >= 8 else None
    working = latest["current_assets"] - latest["current_liabilities"]
    quick = latest["cash"] + latest["receivables"]
    net_current = (latest["current_assets"] - latest["total_liabilities"]) / shares

    def ratio(numerator, denominator, positive=True):
        if denominator is None or denominator == 0 or (positive and denominator <= 0):
            return None
        return numerator / denominator

    return {
        "price": price,
        "market_capitalization": capitalization,
        "enterprise_value": enterprise,
        "shares": shares,
        "net_debt": net_debt,
        "trailing_revenue": revenue,
        "trailing_net_income": earnings,
        "trailing_ebitda": ebitda,
        "trailing_free_cash_flow": free_cash,
        "trailing_eps": earnings / shares,
        "price_earnings": ratio(capitalization, earnings),
        "price_sales": ratio(capitalization, revenue),
        "price_book": ratio(capitalization, equity),
        "enterprise_sales": ratio(enterprise, revenue),
        "enterprise_ebitda": ratio(enterprise, ebitda),
        "free_cash_flow_yield": ratio(free_cash, capitalization),
        "dividend_yield": ratio(dividends, capitalization),
        "payout_ratio": ratio(dividends, earnings),
        "gross_margin": ratio(_trailing(book, "gross_profit"), revenue),
        "operating_margin": ratio(_trailing(book, "operating_income"), revenue, positive=False),
        "net_margin": ratio(earnings, revenue, positive=False),
        "return_on_equity": ratio(earnings, equity),
        "return_on_assets": ratio(earnings, latest["total_assets"], positive=False),
        "revenue_growth": ratio(revenue, prior_revenue) - 1 if prior_revenue else None,
        "earnings_growth": (
            earnings / prior_earnings - 1 if prior_earnings and prior_earnings > 0 else None
        ),
        "current_ratio": ratio(latest["current_assets"], latest["current_liabilities"]),
        "quick_ratio": ratio(quick, latest["current_liabilities"]),
        "working_capital": working,
        "debt_equity": ratio(latest["total_debt"], equity),
        "net_debt_ebitda": ratio(net_debt, ebitda),
        "interest_coverage": ratio(
            _trailing(book, "operating_income"), _trailing(book, "interest_expense")
        ),
        # Graham's screens, the same arithmetic the value courses teach.
        "net_current_asset_value": net_current,
        "graham_number": (
            float(np.sqrt(22.5 * max(earnings / shares, 0) * max(equity / shares, 0)))
            if earnings > 0 and equity > 0
            else None
        ),
        "book_value_per_share": equity / shares,
        "prior_year_quarter": prior_year["label"] if prior_year else None,
    }
