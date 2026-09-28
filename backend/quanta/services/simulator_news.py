"""A deterministic simulated newsroom that drives the generated market.

Every headline, institution, broker and number below is invented. Events are
produced first; the price engine then applies their modeled shocks, so a move on
the chart has a story attached to the same bar rather than a caption added after
the fact.

The schedule is a pure function of the run seed, so replaying a run reproduces
the identical feed, and no item is ever released ahead of the run's cursor.
"""

import hashlib
from dataclasses import dataclass, field

import numpy as np

from quanta.services.simulator_fundamentals import next_report, opening_book
from quanta.services.simulator_universe import BY_SYMBOL, COMPANIES, SECTORS

# Every company reports once a quarter, on the same cycle however long a run runs.
QUARTER_SESSIONS = 63

WIRES = [
    "Quanta Newswire",
    "Harbor Point Wire",
    "Calder Market Report",
    "Tradewind Business Daily",
    "Meridian Tape",
    "Beacon Financial Press",
]
FILINGS = "Simulated Exchange Filings"
BROKERS = [
    "Ashcroft Partners",
    "Brightwater Securities",
    "Calder & Roe",
    "Dunmore Capital",
    "Eastgate Research",
    "Fairlane Equity",
    "Granville Advisors",
    "Halloway Markets",
]
ANALYSTS = [
    "R. Ellison",
    "M. Takahashi",
    "P. Oyelaran",
    "S. Varga",
    "N. Alcantara",
    "D. Whitfield",
    "L. Bergström",
    "A. Rahmawati",
]
REGIONS = ["the northern region", "the coastal markets", "overseas markets", "the domestic market"]
QUARTERS = ["the first quarter", "the second quarter", "the third quarter", "the fourth quarter"]
QUARTERS_ADJ = ["first-quarter", "second-quarter", "third-quarter", "fourth-quarter"]
SEGMENTS = {
    "Semiconductors": ["data-center", "automotive silicon", "foundry", "memory"],
    "Software": ["subscription", "platform", "licensing", "services"],
    "Hardware & robotics": ["automation", "components", "systems", "aftermarket"],
    "Media & telecom": ["advertising", "subscription", "network", "content"],
    "Consumer staples": ["packaged goods", "private label", "distribution", "export"],
    "Consumer discretionary": ["retail", "direct-to-consumer", "wholesale", "premium"],
    "Healthcare": ["clinical", "devices", "diagnostics", "specialty care"],
    "Financials": ["lending", "deposits", "fee income", "underwriting"],
    "Energy": ["upstream", "refining", "renewables", "transport"],
    "Industrials": ["equipment", "aftermarket", "defense", "infrastructure"],
    "Materials": ["mining", "processing", "aggregates", "specialty"],
    "Real estate & utilities": ["leasing", "development", "regulated", "generation"],
}
# Neutral names for a scheduled release, published on the calendar before the
# result exists. The headline that carries the outcome is released separately.
MACRO_LABELS = {
    "inflation": "Consumer price index",
    "labor": "Payrolls and unemployment",
    "policy": "Policy rate decision",
    "growth": "Output estimate",
    "trade": "Trade statistics",
}
# Invented institutions. No real agency, central bank or statistics office is meant.
MACRO_BODIES = {
    "inflation": "the Bureau of Price Statistics",
    "labor": "the National Labor Office",
    "policy": "the Reserve Board",
    "growth": "the Office of Economic Accounts",
    "trade": "the Trade Statistics Agency",
}
INDEX = "the QX-200 index"

# (template, sentiment sign, impact tier). {n}=name {t}=ticker {s}=segment and so on.
COMPANY_TEMPLATES = {
    "earnings": (
        [
            "{n} beats {qa} estimates as {s} revenue climbs {pct}%",
            "{n} reports {qa} profit above expectations on {s} strength",
            "{n} lifts margins in {q}; {s} orders accelerate",
            "{n} posts record {qa} revenue, raises {s} outlook",
        ],
        [
            "{n} misses {qa} estimates as {s} revenue falls {pct}%",
            "{n} reports weaker {qa} profit; {s} demand cools",
            "{n} margins narrow in {q} on higher {s} costs",
            "{n} posts {qa} shortfall, flags slower {s} bookings",
        ],
    ),
    "guidance": (
        [
            "{n} raises full-year guidance on {s} demand",
            "{n} guides {qa} revenue above consensus",
            "{n} lifts margin target after {s} pricing gains",
        ],
        [
            "{n} cuts full-year guidance on softer {s} demand",
            "{n} guides {qa} revenue below consensus, cites {s} pricing",
            "{n} withdraws margin target after {s} cost inflation",
        ],
    ),
    "analyst": (
        [
            "{b} raises {t} to Overweight, target {target}",
            "{b} upgrades {n}; analyst {a} sees {s} inflection",
            "{b} adds {t} to its conviction list, target {target}",
        ],
        [
            "{b} cuts {t} to Underweight, target {target}",
            "{b} downgrades {n}; analyst {a} questions {s} pricing",
            "{b} removes {t} from its focus list on valuation",
        ],
    ),
    "product": (
        [
            "{n} launches next-generation {s} line for {r}",
            "{n} wins a multi-year {s} contract in {r}",
            "{n} expands {s} capacity to meet backlog",
        ],
        [
            "{n} delays its {s} launch into {q}",
            "{n} recalls a {s} product line after quality review",
            "{n} pauses {s} expansion pending review",
        ],
    ),
    "regulatory": (
        [
            "{n} clears regulatory review for its {s} programme",
            "{n} receives approval to operate {s} facilities in {r}",
        ],
        [
            "Regulator opens a review of {p} {s} practices",
            "{n} discloses a compliance inquiry into {s} reporting",
            "{n} faces a proposed penalty over {s} disclosures",
        ],
    ),
    "legal": (
        [
            "{n} settles {s} litigation for {amount}, ending overhang",
            "Court dismisses the {s} claim against {n}",
        ],
        [
            "{n} sued over {s} contracts; {amount} claimed",
            "{n} takes a {amount} charge to resolve {s} claims",
        ],
    ),
    "supply": (
        [
            "{n} secures long-term {s} supply agreement",
            "{n} reopens capacity in {r} ahead of schedule",
        ],
        [
            "{n} flags a {s} supply constraint into {q}",
            "{n} halts a facility in {r} after an equipment failure",
        ],
    ),
    "capital": (
        [
            "{n} announces a {amount} share repurchase",
            "{n} raises its dividend by {pct}%",
            "{n} refinances debt at a lower coupon",
        ],
        [
            "{n} suspends its dividend to fund {s} investment",
            "{n} prices a {amount} equity offering below market",
            "{n} draws on its credit facility to bridge a working-capital gap",
        ],
    ),
    "deal": (
        [
            "{n} to acquire a {s} operator for {amount}",
            "{n} confirmed as a bidder for {s} assets in {r}",
        ],
        [
            "{n} walks away from its {s} acquisition",
            "{n} abandons the sale of its {s} unit",
        ],
    ),
    "leadership": (
        [
            "{n} names a new chief financial officer",
            "{n} appoints a {s} division president",
        ],
        [
            "{p} chief executive steps down, citing personal reasons",
            "{n} loses its {s} division head to a rival",
        ],
    ),
}
# Background items with no modeled price effect. They keep the tape moving.
CHATTER = [
    "{n} files its quarterly report with the exchange",
    "{n} schedules its {qa} results call",
    "{n} to present at a {sector} investor conference",
    "{b} publishes a {sector} primer including {t}",
    "{n} confirms its {s} capacity plan is unchanged",
    "Short interest in {t} little changed over the period",
    "{n} names {r} as a growth priority at an industry panel",
    "Options activity in {t} stays close to recent averages",
    "{n} updates its sustainability disclosures",
    "{b} keeps {t} at Neutral, target {target}",
]
SECTOR_TEMPLATES = (
    [
        "{sector} shares lead {index} higher on improving {s} demand",
        "Buyers return to {sector} after a stretch of outflows",
        "{sector} order books firm up, industry survey suggests",
    ],
    [
        "{sector} shares lag {index} as {s} pricing weakens",
        "Investors trim {sector} exposure on cost pressure",
        "{sector} inventories build, industry survey suggests",
    ],
)
MACRO_TEMPLATES = {
    "inflation": (
        ["Consumer prices rise {pct}%, below the expected pace, {body} reports"],
        ["Consumer prices rise {pct}%, above expectations, {body} reports"],
    ),
    "labor": (
        ["Payrolls add {jobs}k jobs, {body} says, easing growth concerns"],
        ["Payrolls add just {jobs}k jobs, {body} says, missing forecasts"],
    ),
    "policy": (
        ["{body} holds its policy rate and signals patience"],
        ["{body} raises its policy rate by {bps} basis points"],
    ),
    "growth": (
        ["Output grows {pct}% in {q}, {body} estimates"],
        ["Output growth slows to {pct}% in {q}, {body} estimates"],
    ),
    "trade": (
        ["Export volumes improve, {body} reports, helped by {r}"],
        ["Export volumes decline, {body} reports, weighed by {r}"],
    ),
}
OPEN_WRAP = "Opening bell: {index} starts the session {dir}"
CLOSE_WRAP = "Closing bell: {index} ends the session {dir}"

# Every item carries an integer score. One point moves the price it applies to by
# one basis point, so a +250 point headline is a modeled +2.50% move: 58% of it on
# the bar the item is dated, the rest drifting over the bars that follow. Nothing
# is inferred by a model at request time; the score is drawn here and the price
# engine simply applies it.
POINT = 0.0001

# category -> (probability weight, points low, points high, drift bars)
COMPANY_EVENTS = {
    "guidance": (0.13, 160, 550, 120),
    "analyst": (0.22, 40, 190, 45),
    "product": (0.14, 70, 320, 80),
    "regulatory": (0.08, 100, 480, 100),
    "legal": (0.06, 80, 380, 90),
    "supply": (0.10, 80, 300, 70),
    "capital": (0.10, 50, 240, 60),
    "deal": (0.05, 300, 1100, 140),
    "leadership": (0.05, 30, 170, 40),
}
TIERS = ((400, "high"), (120, "medium"), (0, "low"))


def _tier(points: int) -> str:
    """Impact tier from the absolute score, so the label and the number agree.

    A macroeconomic release reaches every company, but the tier describes what it
    does to one price, which is what the score measures.
    """
    for threshold, label in TIERS:
        if abs(points) >= threshold:
            return label
    return "low"


EARNINGS_TEMPLATES = (
    [
        "{n} beats {qa} estimates: revenue {growth}, EPS of {eps} against {consensus} expected",
        "{n} tops {qa} consensus with revenue {growth} and EPS of {eps}",
    ],
    [
        "{n} misses {qa} estimates: revenue {growth}, EPS of {eps} against {consensus} expected",
        "{n} falls short in {qa}: revenue {growth}, EPS of {eps}",
    ],
)
PREVIEW = "{b} previews {t} {qa} results; consensus EPS {consensus}"


@dataclass
class Newsroom:
    events: list = field(default_factory=list)
    books: dict = field(default_factory=dict)
    calendar: dict = field(default_factory=dict)
    market: np.ndarray = None
    sector: dict = field(default_factory=dict)
    company: dict = field(default_factory=dict)
    volatility: dict = field(default_factory=dict)
    volume: dict = field(default_factory=dict)

    def release(self):
        """Drop the price-shock arrays once the bars are built.

        They are scaffolding: the feed, the reporting calendar and the statements
        are what a run keeps, and they are a fraction of the size.
        """
        self.market = None
        self.sector = {}
        self.company = {}
        self.volatility = {}
        self.volume = {}
        return self


def _drift(target, start, span, amount):
    """Spread `amount` over an exponentially decaying window from `start`.

    Only the affected slice is touched. Building a full-length array per event
    dominated both generation time and peak memory when this ran per headline.
    """
    end = min(len(target), start + span)
    if end <= start:
        return
    weights = np.exp(-np.arange(end - start) / max(span / 3.0, 1.0))
    total = weights.sum()
    if total:
        target[start:end] += amount * (weights / total)


SECTOR_MEMBERS = {sector: [c.symbol for c in COMPANIES if c.sector == sector] for sector in SECTORS}


def _excite(room, index, magnitude, span, symbols, scale=1.0):
    """Raise modeled volatility and traded volume around a shock, then decay."""
    for symbol in symbols:
        series = room.volatility[symbol]
        window = slice(index, min(len(series), index + span))
        steps = np.arange(window.stop - window.start)
        weight = scale * magnitude / 0.02
        series[window] += min(3.0, weight) * np.exp(-steps / max(span / 4.0, 1))
        room.volume[symbol][window] += min(6.0, 2.2 * weight) * np.exp(-steps / max(span / 5.0, 1))


def _apply(room, index, points, sign, span, market=False, sector=None, symbol=None):
    """Split a scored shock into an immediate move and a decaying follow-through."""
    magnitude = abs(points) * POINT
    target = room.market if market else room.sector[sector] if sector else room.company[symbol]
    length = len(target)
    if index >= length:
        return
    target[index] += 0.58 * magnitude * sign
    _drift(target, index + 1, span, 0.42 * magnitude * sign)
    if symbol:
        _excite(room, index, magnitude, span, [symbol])
    elif sector:
        _excite(room, index, magnitude, span, SECTOR_MEMBERS[sector], 0.7)
    else:
        _excite(room, index, magnitude, min(span, 200), list(room.volume), 0.9)


def _pick(rng, values):
    return values[int(rng.integers(len(values)))]


def _possessive(name):
    return f"{name}'" if name.endswith("s") else f"{name}'s"


def _money(value):
    """Wire-style money: millions below a billion, billions above it."""
    return f"${value / 1000:.2f}bn" if value >= 1000 else f"${value}m"


def _fill(rng, template, company=None, sector=None, body=None, pct=(0.2, 14.0)):
    segments = SEGMENTS.get(sector or (company.sector if company else ""), ["core"])
    quarter = int(rng.integers(4))
    return template.format(
        n=company.name if company else "",
        p=_possessive(company.name) if company else "",
        t=company.symbol if company else "",
        s=_pick(rng, segments),
        sector=sector or (company.sector if company else ""),
        q=QUARTERS[quarter],
        qa=QUARTERS_ADJ[quarter],
        r=_pick(rng, REGIONS),
        b=_pick(rng, BROKERS),
        a=_pick(rng, ANALYSTS),
        body=body or "",
        index=INDEX,
        pct=round(float(rng.uniform(*pct)), 1),
        amount=_money(int(rng.integers(40, 4800))),
        jobs=int(rng.integers(20, 420)),
        bps=int(_pick(rng, [25, 50])),
        target=f"${company.price * rng.uniform(0.7, 1.4):,.2f}" if company else "",
        dir="",
    )


def _summary(rng, category, company, headline):
    if category == "chatter":
        return (
            f"Routine simulated disclosure for {company.name} "
            f"({company.symbol}). No modeled price impact."
        )
    return (
        f"Simulated {category} item for {company.name} ({company.symbol}), "
        f"a fictional {company.business} company in the {company.sector} sector. "
        "The generated price path reacts to this event on the same bar."
    )


def report_session(seed: int, symbol: str) -> int:
    """The first session in which a company reports. It repeats every quarter.

    Derived from the seed and the ticker alone, so the reporting calendar is the
    same however far into a run the sessions it covers are generated.
    """
    digest = hashlib.sha256(f"quanta-calendar:{seed}:{symbol}".encode()).hexdigest()
    # The first season falls inside the opening month so a new account meets
    # earnings early; after that each company reports on its own quarterly cycle.
    return 3 + int(digest[:8], 16) % 18


def schedule(
    seed: int, first_session: int, sessions: int, session_bars: int, books=None
) -> Newsroom:
    """Headlines and shocks for the sessions [first_session, first_session + sessions).

    A run has no fixed end, so the tape is produced a block of sessions at a time.
    Each block draws from a stream keyed to its own first session, and carries the
    reporting books forward, so a block generated later is identical to the same
    block generated earlier.
    """
    total = sessions * session_bars
    offset = first_session * session_bars
    rng = np.random.default_rng([seed, first_session])
    room = Newsroom(
        market=np.zeros(total),
        sector={name: np.zeros(total) for name in SECTORS},
        company={c.symbol: np.zeros(total) for c in COMPANIES},
        volatility={c.symbol: np.zeros(total) for c in COMPANIES},
        volume={c.symbol: np.zeros(total) for c in COMPANIES},
    )
    events = []
    categories = list(COMPANY_EVENTS)
    weights = np.array([COMPANY_EVENTS[c][0] for c in categories])
    weights = weights / weights.sum()

    def emit(index, **item):
        # Indices leave this function absolute; the shock arrays stay block-local.
        events.append({"index": int(offset + index), **item})

    # Reporting season. Every company publishes once a quarter, at a session open,
    # so the print lands with the gap it causes.
    room.books = books if books is not None else {c.symbol: opening_book(c, rng) for c in COMPANIES}
    room.calendar = {c.symbol: report_session(seed, c.symbol) for c in COMPANIES}
    reporting = {}
    for symbol, first in room.calendar.items():
        for session in range(sessions):
            absolute = first_session + session
            if absolute >= first and (absolute - first) % QUARTER_SESSIONS == 0:
                reporting.setdefault(session, []).append(symbol)

    for session in range(sessions):
        base = session * session_bars
        # Macro releases land near the open and mid-session, and move every name.
        for slot, minute in enumerate((0, int(session_bars * 0.52))):
            topic = _pick(rng, list(MACRO_TEMPLATES))
            good = bool(rng.random() < 0.5)
            points = int(rng.integers(20, 110))
            sign = 1 if good else -1
            index = min(total - 1, base + minute + int(rng.integers(0, 4)))
            headline = _fill(
                rng,
                MACRO_TEMPLATES[topic][0 if good else 1][0],
                body=MACRO_BODIES[topic],
                pct=(0.1, 4.5),
            )
            _apply(room, index, points, sign, int(session_bars * 1.2), market=True)
            emit(
                index,
                scope="macro",
                symbol=None,
                sector=None,
                category="macro",
                topic=topic,
                scheduled=MACRO_LABELS[topic],
                headline=headline,
                summary=(
                    "Simulated macroeconomic release from a fictional statistics body. "
                    "It moves every generated stock through its beta."
                ),
                source=_pick(rng, WIRES),
                sentiment="positive" if good else "negative",
                impact=_tier(points),
                points=sign * points,
                slot=slot,
            )
        # A session wrap at the open and the close keeps the tape populated.
        for minute, template in ((1, OPEN_WRAP), (session_bars - 2, CLOSE_WRAP)):
            index = min(total - 1, base + minute)
            emit(
                index,
                scope="market",
                symbol=None,
                sector=None,
                category="market",
                headline=template.format(
                    index=INDEX, dir=_pick(rng, ["mixed", "firmer", "softer"])
                ),
                summary="Simulated session summary for the generated market.",
                source=_pick(rng, WIRES),
                sentiment="neutral",
                impact="low",
                points=0,
                slot=0,
            )
        for sector in SECTORS:
            if rng.random() > 0.45:
                continue
            good = bool(rng.random() < 0.5)
            points = int(rng.integers(30, 180))
            index = min(total - 1, base + int(rng.integers(0, session_bars)))
            headline = _fill(rng, _pick(rng, SECTOR_TEMPLATES[0 if good else 1]), sector=sector)
            _apply(room, index, points, 1 if good else -1, 140, sector=sector)
            emit(
                index,
                scope="sector",
                symbol=None,
                sector=sector,
                category="sector",
                headline=headline,
                summary=(
                    f"Simulated {sector} sector move. Every fictional company in the "
                    "sector reacts through its sector loading."
                ),
                source=_pick(rng, WIRES),
                sentiment="positive" if good else "negative",
                impact=_tier(points),
                points=(1 if good else -1) * points,
                slot=0,
            )
        for symbol in reporting.get(session, []):
            company = BY_SYMBOL[symbol]
            book = room.books[symbol]
            surprise = float(np.clip(rng.normal(0.008, 0.062), -0.28, 0.28))
            index = min(total - 1, session * session_bars)
            quarter = next_report(company, book, rng, surprise, offset + index, len(book))
            book.append(quarter)
            growth = quarter["revenue"] / book[-5]["revenue"] - 1
            # A one-percentage-point surprise is worth about 62 points before the
            # company's own volatility scales it, and the print is capped at 1,400.
            points = min(
                1400,
                int(abs(surprise) * 6200 * min(1.8, max(0.5, company.volatility / 0.40))) + 40,
            )
            headline = EARNINGS_TEMPLATES[0 if surprise >= 0 else 1][int(rng.integers(2))].format(
                n=company.name,
                qa=quarter["label"],
                growth=f"{growth:+.1%} year on year",
                eps=f"${quarter['eps']:,.2f}",
                consensus=f"${quarter['consensus_eps']:,.2f}",
            )
            _apply(room, index, points, 1 if surprise >= 0 else -1, 170, symbol=symbol)
            emit(
                index,
                scope="company",
                symbol=symbol,
                sector=company.sector,
                category="earnings",
                headline=headline,
                summary=(
                    f"Simulated {quarter['label']} results for {company.name} "
                    f"({symbol}). The full generated income statement, balance sheet "
                    "and cash-flow statement are released with this item."
                ),
                source=FILINGS,
                sentiment="positive" if surprise >= 0 else "negative",
                impact=_tier(points),
                points=(1 if surprise >= 0 else -1) * points,
                slot=0,
            )
            # A preview two sessions earlier publishes only the expectation.
            preview = max(0, index - 2 * session_bars + int(rng.integers(20, 200)))
            emit(
                preview,
                scope="company",
                symbol=symbol,
                sector=company.sector,
                category="chatter",
                headline=PREVIEW.format(
                    b=_pick(rng, BROKERS),
                    t=symbol,
                    qa=quarter["label"],
                    consensus=f"${quarter['consensus_eps']:,.2f}",
                ),
                summary=(
                    "Simulated expectation published before the print. "
                    "No results are released by this item."
                ),
                source=_pick(rng, WIRES),
                sentiment="neutral",
                impact="none",
                points=0,
                slot=0,
            )
        for company in COMPANIES:
            for _ in range(int(rng.poisson(1.15 * company.news_rate))):
                category = categories[int(rng.choice(len(categories), p=weights))]
                _, low, high, span = COMPANY_EVENTS[category]
                good = bool(rng.random() < (0.40 if category in ("regulatory", "legal") else 0.51))
                # A utility does not move like a quantum-computing venture on the
                # same kind of headline, so scale the score to the company.
                points = int(
                    rng.integers(low, high) * min(1.8, max(0.45, company.volatility / 0.40))
                )
                index = min(total - 1, base + int(rng.integers(0, session_bars)))
                template = _pick(rng, COMPANY_TEMPLATES[category][0 if good else 1])
                headline = _fill(rng, template, company=company)
                _apply(room, index, points, 1 if good else -1, span, symbol=company.symbol)
                emit(
                    index,
                    scope="company",
                    symbol=company.symbol,
                    sector=company.sector,
                    category=category,
                    headline=headline,
                    summary=_summary(rng, category, company, headline),
                    source=FILINGS if category == "capital" else _pick(rng, WIRES),
                    sentiment="positive" if good else "negative",
                    impact=_tier(points),
                    points=(1 if good else -1) * points,
                    slot=0,
                )
            for _ in range(int(rng.poisson(0.75 * company.news_rate))):
                index = min(total - 1, base + int(rng.integers(0, session_bars)))
                headline = _fill(rng, _pick(rng, CHATTER), company=company)
                emit(
                    index,
                    scope="company",
                    symbol=company.symbol,
                    sector=company.sector,
                    category="chatter",
                    headline=headline,
                    summary=_summary(rng, "chatter", company, headline),
                    source=_pick(rng, WIRES),
                    sentiment="neutral",
                    impact="none",
                    points=0,
                    slot=0,
                )
    events.sort(key=lambda e: (e["index"], e["scope"], e["symbol"] or "", e["headline"]))
    for position, event in enumerate(events):
        event["id"] = f"{seed}-{event['index']}-{position}"
        event.pop("slot", None)
    room.events = events
    return room


def released(room: Newsroom, cursor: int, symbol=None, sector=None, limit=60) -> list[dict]:
    """Items at or before the run's cursor, newest first. Nothing ahead of it leaves.

    A symbol filter keeps that company's own items plus the sector and
    macroeconomic events that move it, which is what a desk would watch.
    """
    items = []
    for event in reversed(room.events):
        if event["index"] > cursor:
            continue
        if symbol and not (
            event["symbol"] == symbol
            or (event["scope"] == "sector" and event["sector"] == sector)
            or event["scope"] in ("macro", "market")
        ):
            continue
        items.append(event)
        if len(items) >= limit:
            break
    return items


IMPACT_WEIGHT = {"high": 3.0, "medium": 2.0, "low": 1.0, "none": 0.0}
DIRECTION = {"positive": 1.0, "negative": -1.0, "neutral": 0.0}


def sentiment(
    room: Newsroom, cursor: int, window: int, symbol=None, sector=None, macro=True
) -> dict:
    """Impact-weighted news sentiment over the bars the run has already observed.

    The score is the signed weight of released items divided by their total
    weight, so it sits in [-1, 1] and is unchanged by how chatty the tape is.
    Only items at or before the cursor are counted.

    Macro releases move every company, so including them shifts all tickers by the
    same amount. A screener that ranks companies against each other passes
    macro=False to keep the comparison company- and sector-specific.
    """
    start = max(0, cursor - window + 1)
    signed = weight = 0.0
    counts = {"positive": 0, "negative": 0, "neutral": 0}
    considered = 0
    for event in room.events:
        if event["index"] < start or event["index"] > cursor:
            continue
        if symbol and not (
            event["symbol"] == symbol
            or (event["scope"] == "sector" and event["sector"] == sector)
            or (macro and event["scope"] == "macro")
        ):
            continue
        considered += 1
        counts[event["sentiment"]] += 1
        size = IMPACT_WEIGHT[event["impact"]]
        weight += size
        signed += size * DIRECTION[event["sentiment"]]
    return {
        "score": round(signed / weight, 4) if weight else 0.0,
        "weight": round(weight, 2),
        "items": considered,
        "window_bars": min(window, cursor + 1),
        **counts,
    }
