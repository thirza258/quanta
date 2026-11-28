"""Canonical curriculum architecture: stages, sequence, difficulty, and prerequisites.

Lesson and exam identifiers are deliberately absent from this module. They are
stable content identifiers, not ordering devices. Reordering a course therefore
never renumbers its lessons, exams, progress keys, or URLs.

Run ``python3 content/authoring/curriculum.py`` after editing this file.
"""

from __future__ import annotations

# Stage numbers are the coarse academic phase. Sequence numbers are the global
# teaching order. A stage may contain courses whose sequence spans another
# stage when a prerequisite (for example time value of money) must come first.
STAGES = {
    1: {
        "slug": "orientation",
        "name": "Orientation & Market Mechanics",
        "subtitle": "Vocabulary, ownership, orders, returns, costs, and the first research plan.",
        "badge": "Orientation",
    },
    2: {
        "slug": "foundations",
        "name": "Financial & Investment Foundations",
        "subtitle": "Conduct, careful-investor principles, and supervised simulator practice.",
        "badge": "Foundations",
    },
    3: {
        "slug": "fundamental-analysis",
        "name": "Fundamental Analysis & Market Information",
        "subtitle": "Financial statements, security analysis, and verified news-to-valuation reasoning.",
        "badge": "Fundamental Core",
    },
    4: {
        "slug": "advanced-fundamental",
        "name": "Advanced Fundamental Analysis",
        "subtitle": "Forensics, credit, quality, banks, cyclicals, intangibles, and documented cases.",
        "badge": "Value Specializations",
    },
    5: {
        "slug": "quantitative-foundations",
        "name": "Quantitative Foundations & Applied Valuation",
        "subtitle": "Data hygiene, Python, probability, statistics, regression, risk, and valuation under uncertainty.",
        "badge": "Quant Foundations",
    },
    6: {
        "slug": "empirical-finance",
        "name": "Empirical Finance & Econometrics",
        "subtitle": "Identification, time series, volatility, factor tests, causal designs, and state-space models.",
        "badge": "Econometrics",
    },
    7: {
        "slug": "research-strategy",
        "name": "Research Methodology & Strategy Development",
        "subtitle": "Point-in-time data, backtest hygiene, strategy construction, portfolio constraints, and validation.",
        "badge": "Strategy Research",
    },
    8: {
        "slug": "machine-learning",
        "name": "Machine Learning for Markets",
        "subtitle": "Features, labels, purged validation, regularized and tree models, deployment, and monitoring.",
        "badge": "Machine Learning",
    },
    9: {
        "slug": "algorithmic-trading",
        "name": "Algorithmic & AI Trading",
        "subtitle": "Event-driven bots, execution, risk gates, AI evidence, operations, and capacity.",
        "badge": "Algorithmic Trading",
    },
    10: {
        "slug": "high-performance-computing",
        "name": "High-Performance Computing",
        "subtitle": "C17 systems, cache layout, profiling, threads, SIMD, GPUs, and distributed research.",
        "badge": "HPC",
    },
    11: {
        "slug": "specializations",
        "name": "Specializations & Professional Practice",
        "subtitle": "Web3/DeFi, conduct and compliance, and an alternative MSME financial-literacy on-ramp.",
        "badge": "Specializations",
    },
    12: {
        "slug": "capstone",
        "name": "Capstone: Research Evaluation",
        "subtitle": "Audit an algorithm's returns, risk, execution, uncertainty, and reproducibility in a final report.",
        "badge": "Capstone",
    },
}

# course_type values: core, foundation, specialization, workshop, capstone,
# reference, on-ramp. "core" means the default complete-quant path.
COURSES = {
    "trading-fundamentals": {
        "stage": 1,
        "sequence": 10,
        "difficulty": 0,
        "domain": "fundamentals",
        "course_type": "core",
        "is_core": True,
        "is_specialization": False,
        "is_capstone": False,
        "hard_prerequisites": [],
        "any_of_prerequisites": [],
        "soft_prerequisites": [],
        "focus_summary": "Market mechanics, ownership, order types, returns, costs, and the first research plan.",
        "skills": [
            "Order books, quotes, and execution",
            "Market, limit, and stop orders",
            "Returns, costs, and compounding",
            "Diversification and position sizing",
        ],
    },
    "trading-ethics": {
        "stage": 2,
        "sequence": 20,
        "difficulty": 1,
        "domain": "fundamentals",
        "course_type": "core",
        "is_core": True,
        "is_specialization": False,
        "is_capstone": False,
        "hard_prerequisites": ["trading-fundamentals"],
        "any_of_prerequisites": [],
        "soft_prerequisites": [],
        "focus_summary": "Duty, conflicts, market integrity, and conduct for automated and quantitative trading.",
        "skills": [
            "Fiduciary duty and client priority",
            "Material non-public information",
            "Spoofing, layering, and wash trading",
            "Conduct for automated strategies",
        ],
    },
    "simulator-workshop": {
        "stage": 2,
        "sequence": 30,
        "difficulty": 1,
        "domain": "systems",
        "course_type": "workshop",
        "is_core": True,
        "is_specialization": False,
        "is_capstone": False,
        "hard_prerequisites": ["trading-fundamentals", "trading-ethics"],
        "any_of_prerequisites": [],
        "soft_prerequisites": [],
        "focus_summary": "Hands-on paper trading: replay, order handling, fills, margin, analytics, and a charter week.",
        "skills": [
            "Replay clock and market reading",
            "Order handling and fill pricing",
            "Stops, margin, and short selling",
            "Journals and performance review",
        ],
    },
    "intelligent-investor": {
        "stage": 2,
        "sequence": 40,
        "difficulty": 1,
        "domain": "value",
        "course_type": "core",
        "is_core": True,
        "is_specialization": False,
        "is_capstone": False,
        "hard_prerequisites": ["trading-fundamentals"],
        "any_of_prerequisites": [],
        "soft_prerequisites": [],
        "focus_summary": "Careful-investor temperament, portfolio policy, diversification, costs, and independent judgment.",
        "skills": [
            "Investment versus speculation",
            "Allocation and diversification policy",
            "Margin of safety and impairment",
            "Decision journals and review rules",
        ],
    },
    "security-analysis": {
        "stage": 3,
        "sequence": 50,
        "difficulty": 2,
        "domain": "value",
        "course_type": "core",
        "is_core": True,
        "is_specialization": False,
        "is_capstone": False,
        "hard_prerequisites": ["trading-fundamentals"],
        "any_of_prerequisites": [],
        "soft_prerequisites": ["intelligent-investor"],
        "focus_summary": "Graham-Dodd analysis from statements and senior claims to normalized earnings, asset value, and forensic synthesis.",
        "skills": [
            "Financial statements and earnings quality",
            "Bond safety and priority",
            "Normalized earnings and NCAV",
            "Valuation ranges and forensic synthesis",
        ],
    },
    "news-to-markets": {
        "stage": 3,
        "sequence": 60,
        "difficulty": 2,
        "domain": "value",
        "course_type": "core",
        "is_core": True,
        "is_specialization": False,
        "is_capstone": False,
        "hard_prerequisites": ["security-analysis"],
        "any_of_prerequisites": [],
        "soft_prerequisites": ["trading-fundamentals"],
        "focus_summary": "Turn news and macro releases into verified company, cash-flow, and valuation implications.",
        "skills": [
            "Source verification and materiality",
            "Earnings and guidance analysis",
            "Macro transmission channels",
            "Event studies and research memos",
        ],
    },
    "forensic-accounting": {
        "stage": 4,
        "sequence": 70,
        "difficulty": 3,
        "domain": "specialized",
        "course_type": "specialization",
        "is_core": False,
        "is_specialization": True,
        "is_capstone": False,
        "hard_prerequisites": ["security-analysis"],
        "any_of_prerequisites": [],
        "soft_prerequisites": [],
        "focus_summary": "Detect aggressive accounting through accruals, revenue recognition, capitalization, reserves, and related parties.",
        "skills": [
            "Accrual-to-cash bridge",
            "Revenue-recognition red flags",
            "Capitalization and reserves",
            "Related parties and forensic scorecards",
        ],
    },
    "credit-distress": {
        "stage": 4,
        "sequence": 80,
        "difficulty": 3,
        "domain": "specialized",
        "course_type": "specialization",
        "is_core": False,
        "is_specialization": True,
        "is_capstone": False,
        "hard_prerequisites": ["security-analysis"],
        "any_of_prerequisites": [],
        "soft_prerequisites": [],
        "focus_summary": "Analyze debt safety, recovery waterfalls, covenants, and distressed securities.",
        "skills": [
            "Cash-flow coverage through cycles",
            "Capital structure and recovery",
            "Covenants and maturity walls",
            "Distressed valuation and catalysts",
        ],
    },
    "quality-moats": {
        "stage": 4,
        "sequence": 90,
        "difficulty": 3,
        "domain": "specialized",
        "course_type": "specialization",
        "is_core": False,
        "is_specialization": True,
        "is_capstone": False,
        "hard_prerequisites": ["security-analysis"],
        "any_of_prerequisites": [],
        "soft_prerequisites": [],
        "focus_summary": "Evaluate business quality, moat durability, reinvestment returns, and capital allocation.",
        "skills": [
            "ROIC, WACC, and economic profit",
            "Moat sources and durability",
            "Reinvestment runway",
            "Capital allocation and governance",
        ],
    },
    "bank-analysis": {
        "stage": 4,
        "sequence": 100,
        "difficulty": 3,
        "domain": "specialized",
        "course_type": "specialization",
        "is_core": False,
        "is_specialization": True,
        "is_capstone": False,
        "hard_prerequisites": ["security-analysis"],
        "any_of_prerequisites": [],
        "soft_prerequisites": [],
        "focus_summary": "Read bank balance sheets, credit quality, regulatory capital, liquidity, and bank valuation.",
        "skills": [
            "Net interest income and margins",
            "Asset quality and provisioning",
            "Capital adequacy and liquidity",
            "Bank valuation and run risk",
        ],
    },
    "cyclical-industrials": {
        "stage": 4,
        "sequence": 110,
        "difficulty": 3,
        "domain": "specialized",
        "course_type": "specialization",
        "is_core": False,
        "is_specialization": True,
        "is_capstone": False,
        "hard_prerequisites": ["security-analysis"],
        "any_of_prerequisites": [],
        "soft_prerequisites": [],
        "focus_summary": "Normalize cyclical earnings and test resilience through commodity, capacity, and working-capital cycles.",
        "skills": [
            "Mid-cycle normalization",
            "Commodity exposure and hedging",
            "Operating leverage and capacity",
            "Maintenance capex and resilience",
        ],
    },
    "tech-intangibles": {
        "stage": 4,
        "sequence": 120,
        "difficulty": 3,
        "domain": "specialized",
        "course_type": "specialization",
        "is_core": False,
        "is_specialization": True,
        "is_capstone": False,
        "hard_prerequisites": ["security-analysis"],
        "any_of_prerequisites": [],
        "soft_prerequisites": [],
        "focus_summary": "Value intangible-heavy platforms through unit economics, cohorts, comparables, and disciplined growth assumptions.",
        "skills": [
            "Capitalizing R&D and software",
            "Platform unit economics",
            "Network effects and cohort analysis",
            "Intangible comparables and growth discipline",
        ],
    },
    "real-world-casebook": {
        "stage": 4,
        "sequence": 130,
        "difficulty": 4,
        "domain": "specialized",
        "course_type": "capstone",
        "is_core": False,
        "is_specialization": True,
        "is_capstone": True,
        "hard_prerequisites": ["security-analysis"],
        "any_of_prerequisites": ["forensic-accounting", "credit-distress", "bank-analysis"],
        "soft_prerequisites": ["quality-moats", "news-to-markets"],
        "focus_summary": "Apply the full fundamental toolkit to documented accounting, solvency, and disclosure failures.",
        "skills": [
            "Accounting forensics on real cases",
            "Solvency and liquidity analysis",
            "Disclosure and governance evidence",
            "Investment-committee memos",
        ],
    },
    "data-hygiene": {
        "stage": 5,
        "sequence": 140,
        "difficulty": 1,
        "domain": "quant",
        "course_type": "foundation",
        "is_core": False,
        "is_specialization": False,
        "is_capstone": False,
        "hard_prerequisites": [],
        "any_of_prerequisites": [],
        "soft_prerequisites": ["trading-fundamentals"],
        "focus_summary": "Make datasets tidy, dated, reconciled, reproducible, and honest before analysis.",
        "skills": [
            "Tidy data and transaction grains",
            "Dates, currencies, and defect detection",
            "Duplicates, gaps, and reconciliation",
            "Bias, versioning, and reproducibility",
        ],
    },
    "python-reluctant-investor": {
        "stage": 5,
        "sequence": 150,
        "difficulty": 1,
        "domain": "quant",
        "course_type": "foundation",
        "is_core": False,
        "is_specialization": False,
        "is_capstone": False,
        "hard_prerequisites": [],
        "any_of_prerequisites": [],
        "soft_prerequisites": [],
        "focus_summary": "A zero-background Python on-ramp for loading data, calculating, charting, and debugging.",
        "skills": [
            "First scripts and print",
            "CSV loading and column math",
            "Charts and parameter changes",
            "Reading tracebacks",
        ],
    },
    "statistical-foundations": {
        "stage": 5,
        "sequence": 160,
        "difficulty": 3,
        "domain": "quant",
        "course_type": "core",
        "is_core": True,
        "is_specialization": False,
        "is_capstone": False,
        "hard_prerequisites": ["trading-fundamentals"],
        "any_of_prerequisites": [],
        "soft_prerequisites": [],
        "focus_summary": "The quantitative toolkit: time value, probability, inference, regression, factor models, risk, and backtesting.",
        "skills": [
            "Time value and return measurement",
            "Probability, sampling, and inference",
            "Regression and multiple regression",
            "Factor risk, VaR, and backtest hygiene",
        ],
    },
    "valuation-uncertainty": {
        "stage": 5,
        "sequence": 170,
        "difficulty": 3,
        "domain": "specialized",
        "course_type": "specialization",
        "is_core": False,
        "is_specialization": True,
        "is_capstone": False,
        "hard_prerequisites": ["security-analysis", "statistical-foundations"],
        "any_of_prerequisites": [],
        "soft_prerequisites": [],
        "focus_summary": "Value businesses under uncertainty with scenarios, sensitivity, real options, and market-implied expectations.",
        "skills": [
            "Scenario DCF and probability weighting",
            "Sensitivity and break-even analysis",
            "Real options and decision trees",
            "Reverse DCF and distress-adjusted value",
        ],
    },
    "econometrics": {
        "stage": 6,
        "sequence": 180,
        "difficulty": 4,
        "domain": "quant",
        "course_type": "core",
        "is_core": True,
        "is_specialization": False,
        "is_capstone": False,
        "hard_prerequisites": ["statistical-foundations"],
        "any_of_prerequisites": [],
        "soft_prerequisites": ["python-reluctant-investor"],
        "focus_summary": "Graduate empirical finance: identification, time series, volatility, factor tests, causal designs, and state-space models.",
        "skills": [
            "OLS, HAC inference, and specification",
            "Time series, cointegration, and GARCH",
            "Factor models and asset-pricing tests",
            "Panel, causal, GMM, and state-space methods",
        ],
    },
    "lab-workshop": {
        "stage": 7,
        "sequence": 190,
        "difficulty": 2,
        "domain": "quant",
        "course_type": "workshop",
        "is_core": True,
        "is_specialization": False,
        "is_capstone": False,
        "hard_prerequisites": ["statistical-foundations"],
        "any_of_prerequisites": [],
        "soft_prerequisites": ["econometrics"],
        "focus_summary": "Hands-on research platform: synthetic markets, backtests, valuation, factor studio, robustness, and notebooks.",
        "skills": [
            "Synthetic markets and scenarios",
            "Backtest mechanics and metrics",
            "Valuation and factor studio",
            "Robustness, paper trading, and notebooks",
        ],
    },
    "spreadsheet-to-strategy-lab": {
        "stage": 7,
        "sequence": 200,
        "difficulty": 2,
        "domain": "quant",
        "course_type": "workshop",
        "is_core": False,
        "is_specialization": False,
        "is_capstone": False,
        "hard_prerequisites": [],
        "any_of_prerequisites": [],
        "soft_prerequisites": ["trading-fundamentals", "python-reluctant-investor", "lab-workshop"],
        "focus_summary": "Translate spreadsheet rules into reproducible strategy-lab experiments.",
        "skills": [
            "Column mapping and import validation",
            "Rule translation to strategy code",
            "Costs, slippage, and look-ahead",
            "Saved, named, and repeatable runs",
        ],
    },
    "strategy-lab": {
        "stage": 7,
        "sequence": 210,
        "difficulty": 3,
        "domain": "quant",
        "course_type": "core",
        "is_core": True,
        "is_specialization": False,
        "is_capstone": False,
        "hard_prerequisites": ["statistical-foundations", "econometrics"],
        "any_of_prerequisites": [],
        "soft_prerequisites": ["lab-workshop", "security-analysis", "python-reluctant-investor"],
        "focus_summary": "Build, combine, and defend systematic strategies from hypothesis through validation.",
        "skills": [
            "Falsifiable research and benchmarks",
            "Point-in-time data and labels",
            "Value, quality, momentum, and pairs",
            "Portfolio construction and validation",
        ],
    },
    "stock-machine-learning": {
        "stage": 8,
        "sequence": 220,
        "difficulty": 4,
        "domain": "quant",
        "course_type": "core",
        "is_core": True,
        "is_specialization": False,
        "is_capstone": False,
        "hard_prerequisites": ["statistical-foundations", "econometrics"],
        "any_of_prerequisites": [],
        "soft_prerequisites": ["strategy-lab", "python-reluctant-investor"],
        "focus_summary": "The full stock-ML lifecycle from point-in-time data and labels to validation, deployment, and monitoring.",
        "skills": [
            "Point-in-time data and feature pipelines",
            "Labels, purged splits, and leakage control",
            "Regularized, tree, and sequence models",
            "Walk-forward evaluation and monitoring",
        ],
    },
    "stock-bots": {
        "stage": 9,
        "sequence": 230,
        "difficulty": 4,
        "domain": "systems",
        "course_type": "core",
        "is_core": True,
        "is_specialization": False,
        "is_capstone": False,
        "hard_prerequisites": ["strategy-lab"],
        "any_of_prerequisites": [],
        "soft_prerequisites": ["stock-machine-learning", "simulator-workshop"],
        "focus_summary": "Design, operate, and evaluate event-driven paper-trading bots with ML, AI evidence, and risk controls.",
        "skills": [
            "Event-driven bot architecture",
            "Execution, accounting, and risk gates",
            "ML decisions and bounded AI agents",
            "Operations, capacity, and incident response",
        ],
    },
    "c-hpc-trading": {
        "stage": 10,
        "sequence": 240,
        "difficulty": 5,
        "domain": "systems",
        "course_type": "core",
        "is_core": True,
        "is_specialization": False,
        "is_capstone": False,
        "hard_prerequisites": ["stock-bots"],
        "any_of_prerequisites": [],
        "soft_prerequisites": ["strategy-lab"],
        "focus_summary": "Re-engineer trading research in C17 and optimize it with profiling, parallelism, SIMD, and GPU batching.",
        "skills": [
            "C17 build, memory, and numeric safety",
            "Cache locality and streaming indicators",
            "Profiling, threads, and OpenMP",
            "SIMD, GPUs, and distributed research",
        ],
    },
    "web3": {
        "stage": 11,
        "sequence": 250,
        "difficulty": 3,
        "domain": "crypto",
        "course_type": "specialization",
        "is_core": False,
        "is_specialization": True,
        "is_capstone": False,
        "hard_prerequisites": ["trading-fundamentals"],
        "any_of_prerequisites": [],
        "soft_prerequisites": ["python-reluctant-investor"],
        "focus_summary": "Cryptography, blockchain ledgers, smart contracts, tokenomics, AMMs, and DeFi risk.",
        "skills": [
            "Hashes, Merkle proofs, and signatures",
            "Ledger and block validation",
            "EVM, ERC-20, and tokenomics",
            "AMMs, impermanent loss, and DeFi risk",
        ],
    },
    "conduct-compliance-essentials": {
        "stage": 11,
        "sequence": 260,
        "difficulty": 3,
        "domain": "professional",
        "course_type": "reference",
        "is_core": False,
        "is_specialization": True,
        "is_capstone": False,
        "hard_prerequisites": [],
        "any_of_prerequisites": [],
        "soft_prerequisites": ["trading-ethics", "strategy-lab"],
        "focus_summary": "A professional conduct and compliance reference for advisory, algorithmic, and reporting work.",
        "skills": [
            "Fiduciary duty and hidden costs",
            "Manipulation and information hygiene",
            "GIPS, pre-trade controls, and audit trails",
            "Cyber, supervision, and ESG integrity",
        ],
    },
    "msme-financial-literacy": {
        "stage": 11,
        "sequence": 270,
        "difficulty": 1,
        "domain": "fundamentals",
        "course_type": "on-ramp",
        "is_core": False,
        "is_specialization": True,
        "is_capstone": False,
        "hard_prerequisites": [],
        "any_of_prerequisites": [],
        "soft_prerequisites": [],
        "focus_summary": "An Indonesian-language, zero-prerequisite financial-literacy on-ramp for MSME owners.",
        "skills": [
            "Cash-flow separation and recording",
            "Twelve-month cash projections",
            "Break-even and working capital",
            "Pricing, lending, and tax basics",
        ],
    },
    "algorithm-evaluation": {
        "stage": 12,
        "sequence": 280,
        "difficulty": 4,
        "domain": "systems",
        "course_type": "capstone",
        "is_core": True,
        "is_specialization": False,
        "is_capstone": True,
        "hard_prerequisites": ["strategy-lab"],
        "any_of_prerequisites": ["stock-bots", "stock-machine-learning", "c-hpc-trading"],
        "soft_prerequisites": ["econometrics", "lab-workshop"],
        "focus_summary": "The capstone: audit, evaluate, and report an algorithm's returns, risk, execution, and uncertainty.",
        "skills": [
            "Evaluation contracts and provenance",
            "Benchmarks, costs, and risk metrics",
            "Chronological holdouts and robustness",
            "Attribution and honest reporting",
        ],
    },
}


def _validate(tracks: list[dict]) -> dict[str, dict]:
    by_id = {track["id"]: track for track in tracks}
    if len(by_id) != len(tracks):
        raise AssertionError("Duplicate course IDs in catalog")
    if set(by_id) != set(COURSES):
        missing = sorted(set(by_id) - set(COURSES))
        unknown = sorted(set(COURSES) - set(by_id))
        raise AssertionError(f"Curriculum metadata mismatch; missing={missing}, unknown={unknown}")

    sequences = [entry["sequence"] for entry in COURSES.values()]
    if len(sequences) != len(set(sequences)):
        raise AssertionError("Curriculum sequence numbers must be unique")
    if sorted(sequences) != [10 * (i + 1) for i in range(len(sequences))]:
        raise AssertionError("Curriculum sequences must be contiguous multiples of 10")

    for course_id, entry in COURSES.items():
        sequence = entry["sequence"]
        if entry["stage"] not in STAGES:
            raise AssertionError(f"{course_id}: unknown stage {entry['stage']}")
        if not 0 <= entry["difficulty"] <= 5:
            raise AssertionError(f"{course_id}: difficulty must be between 0 and 5")
        if not entry["focus_summary"].strip() or len(entry["skills"]) < 3:
            raise AssertionError(f"{course_id}: incomplete pedagogical metadata")
        for field in ("hard_prerequisites", "any_of_prerequisites", "soft_prerequisites"):
            for prerequisite in entry[field]:
                if prerequisite not in by_id:
                    raise AssertionError(f"{course_id}: unknown prerequisite {prerequisite}")
                if prerequisite == course_id:
                    raise AssertionError(f"{course_id}: cannot require itself")
                if COURSES[prerequisite]["sequence"] >= sequence:
                    raise AssertionError(
                        f"{course_id}: prerequisite {prerequisite} must appear earlier"
                    )
        if entry["is_core"] and entry["is_specialization"]:
            raise AssertionError(f"{course_id}: cannot be both core and a specialization")
        if entry["is_capstone"] and entry["course_type"] != "capstone":
            raise AssertionError(f"{course_id}: capstone flag requires course_type='capstone'")

    # Kahn's algorithm over hard and any-of edges. Any-of edges are still edges
    # for cycle detection because at least one option must precede the course.
    indegree = {course_id: 0 for course_id in COURSES}
    edges = {course_id: [] for course_id in COURSES}
    for course_id, entry in COURSES.items():
        for prerequisite in entry["hard_prerequisites"] + entry["any_of_prerequisites"]:
            edges[prerequisite].append(course_id)
            indegree[course_id] += 1
    ready = [course_id for course_id, degree in indegree.items() if degree == 0]
    visited = 0
    while ready:
        node = ready.pop()
        visited += 1
        for dependent in edges[node]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                ready.append(dependent)
    if visited != len(COURSES):
        blocked = sorted(course_id for course_id, degree in indegree.items() if degree)
        raise AssertionError(f"Prerequisite cycle detected among: {blocked}")
    return by_id


def attach_curriculum_metadata(tracks: list[dict]) -> None:
    """Attach ordering metadata, validate the dependency DAG, and sort the catalog."""
    by_id = _validate(tracks)
    for course_id, entry in COURSES.items():
        track = by_id[course_id]
        stage = STAGES[entry["stage"]]
        minutes = track.get("estimated_minutes") or sum(
            module.get("minutes", 15) for module in track.get("modules", [])
        )
        track["stage"] = stage["slug"]
        track["stage_number"] = entry["stage"]
        track["stage_name"] = stage["name"]
        track["sequence"] = entry["sequence"]
        track["difficulty"] = entry["difficulty"]
        track["estimated_hours"] = round(minutes / 60, 1)
        track["prerequisite_course_ids"] = list(entry["hard_prerequisites"])
        track["prerequisite_any_of"] = list(entry["any_of_prerequisites"])
        track["recommended_course_ids"] = list(entry["soft_prerequisites"])
        track["learning_outcomes"] = list(track.get("outcomes", []))
        track["skills"] = list(entry["skills"])
        track["focus_summary"] = entry["focus_summary"]
        track["domain"] = entry["domain"]
        track["course_type"] = entry["course_type"]
        track["is_core"] = entry["is_core"]
        track["is_specialization"] = entry["is_specialization"]
        track["is_capstone"] = entry["is_capstone"]

    tracks.sort(key=lambda item: item["sequence"])
    # The primary call to action always points at the next course in the
    # validated sequence, never at a course that now appears earlier.
    for index, track in enumerate(tracks):
        if index + 1 < len(tracks):
            following = tracks[index + 1]
            track["funnel_cta"] = {
                "label": f"Continue to {following['title']}",
                "target_course_id": following["id"],
            }
        else:
            track["funnel_cta"] = {
                "label": "Browse the completed curriculum",
                "target_course_id": "curriculum",
            }