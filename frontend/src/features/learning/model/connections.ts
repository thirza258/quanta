import { tracks } from "@/features/learning/model/catalog";
import { trackProgress } from "@/features/learning/model/progress";
import type { Track } from "@/features/learning/model/types";
import type { WorkspaceState } from "@/features/workspace/model/types";

export type CourseDomain =
  "fundamentals" | "value" | "quant" | "systems" | "specialized" | "crypto";

export type CourseStage = 1 | 2 | 3 | 4;

export type CourseConnection = {
  id: string;
  stage: CourseStage;
  stageName: string;
  domain: CourseDomain;
  domainLabel: string;
  prerequisites: string[];
  recommendedBefore: string[];
  unlocks: string[];
  whyPrerequisites: string;
  whyUnlocks: string;
  focusSummary: string;
  skillsGained: string[];
};

export type LearningPathway = {
  id: string;
  title: string;
  subtitle: string;
  targetRole: string;
  badge: string;
  description: string;
  steps: {
    step: number;
    trackId: string;
    whyThisStep: string;
    keyDeliverable: string;
  }[];
};

export const STAGE_CONFIG: Record<
  CourseStage,
  { name: string; subtitle: string; badge: string }
> = {
  1: {
    name: "Stage 1: Foundations & Market Mechanics",
    subtitle:
      "Core market microstructure, order books, execution mechanics, and trading ethics.",
    badge: "Foundations",
  },
  2: {
    name: "Stage 2: Core Analysis & Quantitative Modeling",
    subtitle:
      "Classical fundamental valuation principles, statistical tools, and decentralized ledgers.",
    badge: "Core Tools",
  },
  3: {
    name: "Stage 3: Applied Research & Strategy Formulation",
    subtitle:
      "Econometric factor modeling, news sentiment analysis, algorithmic bots, and backtesting.",
    badge: "Applied Research",
  },
  4: {
    name: "Stage 4: Specialized Deep Dives & Systems Architecture",
    subtitle:
      "Forensic accounting, credit distress, C/HPC low latency, machine learning, and capstone audits.",
    badge: "Specialized & Capstones",
  },
};

export const DOMAIN_CONFIG: Record<
  CourseDomain,
  { label: string; color: string }
> = {
  fundamentals: { label: "Foundations & Ethics", color: "var(--accent)" },
  value: { label: "Fundamental & Value", color: "#2563eb" },
  quant: { label: "Quantitative & Econometrics", color: "#7c3aed" },
  systems: { label: "Systems & Algorithmic Bots", color: "#ea580c" },
  specialized: { label: "Advanced Security Analysis", color: "#0891b2" },
  crypto: { label: "Web3 & Cryptography", color: "#d97706" },
};

export const courseConnections: CourseConnection[] = [
  // STAGE 1: FOUNDATIONS & MECHANICS
  {
    id: "trading-fundamentals",
    stage: 1,
    stageName: "Foundations & Market Mechanics",
    domain: "fundamentals",
    domainLabel: "Foundations & Ethics",
    prerequisites: [],
    recommendedBefore: [],
    unlocks: [
      "trading-ethics",
      "simulator-workshop",
      "lab-workshop",
      "intelligent-investor",
      "security-analysis",
      "statistical-foundations",
      "web3",
    ],
    whyPrerequisites:
      "The universal starting point of the Quanta curriculum. No prerequisites required.",
    whyUnlocks:
      "Establishes order book depth, market vs limit orders, slippage, and compounding returns without which subsequent modeling is abstract or prone to naive execution assumptions.",
    focusSummary:
      "Market microstructure, bid-ask spreads, order execution types, and compounding arithmetic.",
    skillsGained: [
      "Order books & execution queues",
      "Market, limit & stop orders",
      "Bid-ask spreads & transaction slippage",
      "Compounding & portfolio arithmetic",
    ],
  },
  {
    id: "trading-ethics",
    stage: 1,
    stageName: "Foundations & Market Mechanics",
    domain: "fundamentals",
    domainLabel: "Foundations & Ethics",
    prerequisites: ["trading-fundamentals"],
    recommendedBefore: [],
    unlocks: ["simulator-workshop"],
    whyPrerequisites:
      "Requires basic familiarity with order submission and execution to recognize illegal market conduct.",
    whyUnlocks:
      "Teaches market integrity regulations (spoofing, wash sales, front-running, material non-public info) before you operate with simulated capital or design automated execution bots.",
    focusSummary:
      "Regulatory compliance, market abuse prohibitions, information barriers, and professional fiduciary duties.",
    skillsGained: [
      "Market manipulation detection",
      "Wash trading & spoofing rules",
      "Information barriers & MNPI",
      "Fiduciary obligations & licensing",
    ],
  },
  {
    id: "simulator-workshop",
    stage: 1,
    stageName: "Foundations & Market Mechanics",
    domain: "systems",
    domainLabel: "Systems & Algorithmic Bots",
    prerequisites: ["trading-fundamentals", "trading-ethics"],
    recommendedBefore: [],
    unlocks: ["stock-bots"],
    whyPrerequisites:
      "Combines order mechanics from Fundamentals with ethical execution constraints from Ethics.",
    whyUnlocks:
      "Provides hands-on terminal experience managing order flow and tracking real-time slippage, establishing essential intuition for building automated trading bots.",
    focusSummary:
      "Live order flow simulation, order book manipulation safeguards, and portfolio management.",
    skillsGained: [
      "Live order-flow entry & monitoring",
      "Fill price slippage tracking",
      "Paper portfolio position sizing",
      "Execution speed & latency intuition",
    ],
  },
  {
    id: "lab-workshop",
    stage: 1,
    stageName: "Foundations & Market Mechanics",
    domain: "quant",
    domainLabel: "Quantitative & Econometrics",
    prerequisites: ["trading-fundamentals"],
    recommendedBefore: [],
    unlocks: ["strategy-lab"],
    whyPrerequisites:
      "Builds directly upon fundamental asset pricing and return metrics to introduce Python scripting.",
    whyUnlocks:
      "Provides a gentle on-ramp to factor regression and strategy mechanics from scratch, preparing you for the advanced Strategy Lab.",
    focusSummary:
      "Hands-on Python arithmetic, data structures, and introductory factor regressions.",
    skillsGained: [
      "Financial data wrangling in Python",
      "Simple factor regression lines",
      "Strategy returns aggregation",
      "Benchmark comparison math",
    ],
  },

  // STAGE 2: CORE ANALYSIS & QUANTITATIVE MODELING
  {
    id: "intelligent-investor",
    stage: 2,
    stageName: "Core Analysis & Quantitative Modeling",
    domain: "value",
    domainLabel: "Fundamental & Value",
    prerequisites: ["trading-fundamentals"],
    recommendedBefore: [],
    unlocks: ["security-analysis"],
    whyPrerequisites:
      "Requires understanding basic shares, bonds, yields, and orders to appreciate Graham's philosophy.",
    whyUnlocks:
      "Instills the emotional discipline (Mr. Market) and margin of safety necessary before undertaking rigorous mathematical statement adjustments in Security Analysis.",
    focusSummary:
      "Graham & Dodd value philosophy, margin of safety, and defensive vs enterprising allocation.",
    skillsGained: [
      "Margin of safety calculation",
      "Mr. Market psychological discipline",
      "Defensive investor asset allocation",
      "Inflation protection & bond analysis",
    ],
  },
  {
    id: "security-analysis",
    stage: 2,
    stageName: "Core Analysis & Quantitative Modeling",
    domain: "value",
    domainLabel: "Fundamental & Value",
    prerequisites: ["trading-fundamentals"],
    recommendedBefore: ["intelligent-investor"],
    unlocks: [
      "news-to-markets",
      "forensic-accounting",
      "credit-distress",
      "quality-moats",
      "bank-analysis",
      "valuation-uncertainty",
      "cyclical-industrials",
      "tech-intangibles",
      "real-world-casebook",
      "strategy-lab",
    ],
    whyPrerequisites:
      "Draws upon corporate equity structures and market pricing to deconstruct financial reports.",
    whyUnlocks:
      "The foundational cornerstone for all 8 specialized fundamental deep-dives and fundamental factor screening in the Strategy Lab.",
    focusSummary:
      "Three-statement financial analysis, earnings power normalization, and balance-sheet solvency.",
    skillsGained: [
      "Income statement & cash flow audits",
      "Balance sheet asset-debt quality",
      "Normalized earnings power",
      "Fixed charge & debt coverage ratios",
    ],
  },
  {
    id: "statistical-foundations",
    stage: 2,
    stageName: "Core Analysis & Quantitative Modeling",
    domain: "quant",
    domainLabel: "Quantitative & Econometrics",
    prerequisites: ["trading-fundamentals"],
    recommendedBefore: [],
    unlocks: [
      "econometrics",
      "strategy-lab",
      "stock-bots",
      "stock-machine-learning",
      "valuation-uncertainty",
    ],
    whyPrerequisites:
      "Grounds mathematical probability and distribution theories in actual asset returns and market variables.",
    whyUnlocks:
      "The rigorous mathematical engine required for multi-factor econometrics, machine learning, algorithmic bots, and quantitative backtesting.",
    focusSummary:
      "Probability distributions, hypothesis testing, OLS regression, time series, and Value at Risk.",
    skillsGained: [
      "Probability distributions & central limit theorem",
      "Hypothesis testing & p-values",
      "OLS & multiple regression diagnostics",
      "Time-series stationarity & Value at Risk",
    ],
  },
  {
    id: "web3",
    stage: 2,
    stageName: "Core Analysis & Quantitative Modeling",
    domain: "crypto",
    domainLabel: "Web3 & Cryptography",
    prerequisites: ["trading-fundamentals"],
    recommendedBefore: [],
    unlocks: ["strategy-lab"],
    whyPrerequisites:
      "Contrasts centralized exchange order routing with cryptographic peer-to-peer ledger mechanics.",
    whyUnlocks:
      "Enables students to explore decentralized liquidity pool strategies (x*y=k) and tokenomics models in the Strategy Lab.",
    focusSummary:
      "Public-key cryptography, distributed ledgers, automated market makers (AMMs), and smart contracts.",
    skillsGained: [
      "SHA-256 & secp256k1 elliptic curve math",
      "Automated Market Maker (AMM) invariant equations",
      "Solidity smart contract mechanics",
      "Liquidity pool impermanent loss modeling",
    ],
  },

  // STAGE 3: APPLIED RESEARCH & STRATEGY FORMULATION
  {
    id: "news-to-markets",
    stage: 3,
    stageName: "Applied Research & Strategy Formulation",
    domain: "value",
    domainLabel: "Fundamental & Value",
    prerequisites: ["trading-fundamentals", "security-analysis"],
    recommendedBefore: [],
    unlocks: ["real-world-casebook"],
    whyPrerequisites:
      "Requires financial statement literacy to separate media headlines and PR spin from real economic value.",
    whyUnlocks:
      "Feeds into real-world investment memos and corporate event-driven dossiers in the Real-World Casebook.",
    focusSummary:
      "SEC 10-K/10-Q filings, earnings surprise decomposition, and macroeconomic transmission channels.",
    skillsGained: [
      "Translating headlines to earnings revisions",
      "Decomposing earnings calls & 8-K filings",
      "Macro interest-rate transmission",
      "Event-driven valuation impact modeling",
    ],
  },
  {
    id: "econometrics",
    stage: 3,
    stageName: "Applied Research & Strategy Formulation",
    domain: "quant",
    domainLabel: "Quantitative & Econometrics",
    prerequisites: ["statistical-foundations"],
    recommendedBefore: [],
    unlocks: ["strategy-lab", "stock-machine-learning", "algorithm-evaluation"],
    whyPrerequisites:
      "Extends statistical foundations into multi-factor regression, cointegration, and heteroskedastic time-series.",
    whyUnlocks:
      "Directly provides the Fama-French multi-factor alpha models, volatility estimators (GARCH), and pairs models implemented in the Strategy Lab.",
    focusSummary:
      "CAPM, Fama-French multi-factor asset pricing, cointegration pairs, and ARCH/GARCH volatility.",
    skillsGained: [
      "Fama-French 3- and 5-factor regressions",
      "Cointegration & statistical arbitrage pairs",
      "GARCH conditional volatility forecasting",
      "Panel regression & fixed effects",
    ],
  },
  {
    id: "strategy-lab",
    stage: 3,
    stageName: "Applied Research & Strategy Formulation",
    domain: "quant",
    domainLabel: "Quantitative & Econometrics",
    prerequisites: ["statistical-foundations", "econometrics"],
    recommendedBefore: ["lab-workshop", "security-analysis"],
    unlocks: ["stock-bots", "algorithm-evaluation"],
    whyPrerequisites:
      "Synthesizes statistical distributions and econometric factor models into systematic portfolio construction.",
    whyUnlocks:
      "Outputs systematic trading rules, factor weights, and rebalancing signals ready to be automated by Stock Bots or audited by Algorithm Evaluation.",
    focusSummary:
      "Systematic factor portfolios, momentum & value screening, and realistic transaction cost backtesting.",
    skillsGained: [
      "Factor scoring & cross-sectional ranking",
      "Turnover, transaction cost & friction stress tests",
      "Long-short portfolio construction",
      "Sharpe, Sortino & max drawdown optimization",
    ],
  },
  {
    id: "stock-bots",
    stage: 3,
    stageName: "Applied Research & Strategy Formulation",
    domain: "systems",
    domainLabel: "Systems & Algorithmic Bots",
    prerequisites: ["trading-fundamentals", "statistical-foundations"],
    recommendedBefore: ["simulator-workshop", "strategy-lab"],
    unlocks: ["c-hpc-trading", "algorithm-evaluation"],
    whyPrerequisites:
      "Merges market microstructure principles with statistical logic into production software code.",
    whyUnlocks:
      "Provides the asynchronous event loops and execution logic that are upgraded to bare-metal speed in C/HPC and audited in Algorithm Evaluation.",
    focusSummary:
      "Asynchronous Python trading engines, WebSocket feeds, state machines, and risk kill-switches.",
    skillsGained: [
      "Event-driven architectural loops",
      "WebSocket streaming & order state machines",
      "Execution safety & drawdown kill-switches",
      "Automated paper trading integration",
    ],
  },

  // STAGE 4: SPECIALIZED DEEP DIVES & SYSTEMS ARCHITECTURE
  {
    id: "forensic-accounting",
    stage: 4,
    stageName: "Specialized Deep Dives & Systems Architecture",
    domain: "specialized",
    domainLabel: "Advanced Security Analysis",
    prerequisites: ["security-analysis"],
    recommendedBefore: [],
    unlocks: ["real-world-casebook"],
    whyPrerequisites:
      "Relies on deep familiarity with the three financial statements to spot subtle balance sheet manipulations.",
    whyUnlocks:
      "Supplies critical accounting manipulation filters for building fraud-resistant valuation cases in the Real-World Casebook.",
    focusSummary:
      "Earnings quality forensic tests, Beneish M-Score, aggressive revenue recognition, and cash-flow red flags.",
    skillsGained: [
      "Beneish M-Score accruals analysis",
      "Channel stuffing & revenue manipulation detection",
      "Operating vs financing cash flow reclassification",
      "Off-balance-sheet commitment auditing",
    ],
  },
  {
    id: "credit-distress",
    stage: 4,
    stageName: "Specialized Deep Dives & Systems Architecture",
    domain: "specialized",
    domainLabel: "Advanced Security Analysis",
    prerequisites: ["security-analysis"],
    recommendedBefore: [],
    unlocks: ["real-world-casebook"],
    whyPrerequisites:
      "Uses capital structure and fixed-charge coverage foundations from Security Analysis to dissect debt instruments.",
    whyUnlocks:
      "Powers distressed debt turnaround evaluations and recovery waterfall models in the Real-World Casebook.",
    focusSummary:
      "High-yield credit analysis, structural default modeling (Merton, Altman Z), debt covenants, and restructuring.",
    skillsGained: [
      "Altman Z-Score & Merton structural default model",
      "Bond indentures & covenant compliance analysis",
      "Seniority waterfalls & recovery estimation",
      "Distressed debt & chapter 11 reorganization",
    ],
  },
  {
    id: "quality-moats",
    stage: 4,
    stageName: "Specialized Deep Dives & Systems Architecture",
    domain: "specialized",
    domainLabel: "Advanced Security Analysis",
    prerequisites: ["security-analysis"],
    recommendedBefore: [],
    unlocks: ["real-world-casebook"],
    whyPrerequisites:
      "Expands ROIC and capital deployment metrics learned in Security Analysis into long-term strategic competitive moats.",
    whyUnlocks:
      "Provides the core qualitative and quantitative moat framework for high-conviction compounder theses in the Casebook.",
    focusSummary:
      "ROIC vs WACC persistence, economic moats, capital allocation, and competitive advantages.",
    skillsGained: [
      "ROIC and incremental invested capital runways",
      "Switching costs, network effects & intangible assets",
      "Management capital allocation scorecards",
      "Pricing power durability through inflation",
    ],
  },
  {
    id: "bank-analysis",
    stage: 4,
    stageName: "Specialized Deep Dives & Systems Architecture",
    domain: "specialized",
    domainLabel: "Advanced Security Analysis",
    prerequisites: ["security-analysis"],
    recommendedBefore: [],
    unlocks: ["real-world-casebook"],
    whyPrerequisites:
      "Adapts corporate financial analysis to the balance sheet of financial intermediaries where loans are assets and deposits are debt.",
    whyUnlocks:
      "Crucial for analyzing financial institutions, credit crises, and liquidity runs in the Real-World Casebook.",
    focusSummary:
      "Bank financial statements, Net Interest Margin (NIM), Basel III capital tiers, and CECL credit loss provisioning.",
    skillsGained: [
      "Net Interest Margin (NIM) decomposition",
      "Common Equity Tier 1 (CET1) & Basel III compliance",
      "Current Expected Credit Losses (CECL) modeling",
      "Asset-Liability Management (ALM) & interest rate duration risk",
    ],
  },
  {
    id: "valuation-uncertainty",
    stage: 4,
    stageName: "Specialized Deep Dives & Systems Architecture",
    domain: "specialized",
    domainLabel: "Advanced Security Analysis",
    prerequisites: ["security-analysis", "statistical-foundations"],
    recommendedBefore: [],
    unlocks: ["real-world-casebook"],
    whyPrerequisites:
      "Combines DCF valuation mechanics with probability distributions to model businesses with negative or volatile earnings.",
    whyUnlocks:
      "Supplies probabilistic valuation ranges and reverse-DCF hurdle models for complex valuation dossiers in the Casebook.",
    focusSummary:
      "Valuation of early-stage, distressed, or high-growth firms using reverse DCF and real options.",
    skillsGained: [
      "Reverse DCF market expectation pricing",
      "Monte Carlo valuation distributions",
      "Real options in capital expenditures",
      "Negative earnings normalization pathways",
    ],
  },
  {
    id: "cyclical-industrials",
    stage: 4,
    stageName: "Specialized Deep Dives & Systems Architecture",
    domain: "specialized",
    domainLabel: "Advanced Security Analysis",
    prerequisites: ["security-analysis"],
    recommendedBefore: [],
    unlocks: ["real-world-casebook"],
    whyPrerequisites:
      "Uses fixed-cost and margin concepts from Security Analysis to isolate underlying earnings power from business cycle swings.",
    whyUnlocks:
      "Enables analyzing capital-intensive commodities, transport, and manufacturing dossiers in the Casebook.",
    focusSummary:
      "Mid-cycle normalized earnings, operating leverage, capex replacement cycles, and commodity margins.",
    skillsGained: [
      "Mid-cycle earnings power normalization",
      "Operating leverage & fixed cost breakeven",
      "Capex maintenance vs growth accounting",
      "Commodity price curve transmission",
    ],
  },
  {
    id: "tech-intangibles",
    stage: 4,
    stageName: "Specialized Deep Dives & Systems Architecture",
    domain: "specialized",
    domainLabel: "Advanced Security Analysis",
    prerequisites: ["security-analysis"],
    recommendedBefore: [],
    unlocks: ["real-world-casebook"],
    whyPrerequisites:
      "Adapts standard GAAP/IFRS accounting from Security Analysis to capitalize intangibles, software R&D, and user cohorts.",
    whyUnlocks:
      "Powers software, platform, and subscription ecosystem investment theses in the Casebook.",
    focusSummary:
      "SaaS unit economics (CAC, LTV, NRR), capitalizing R&D, and platform network effects.",
    skillsGained: [
      "Customer Acquisition Cost (CAC) & Lifetime Value (LTV)",
      "Net Retention Rate (NRR) cohort waterfall analysis",
      "Software R&D capitalization adjustments",
      "Multi-sided platform take-rate economics",
    ],
  },
  {
    id: "real-world-casebook",
    stage: 4,
    stageName: "Specialized Deep Dives & Systems Architecture",
    domain: "specialized",
    domainLabel: "Advanced Security Analysis",
    prerequisites: ["security-analysis"],
    recommendedBefore: [
      "forensic-accounting",
      "credit-distress",
      "bank-analysis",
      "quality-moats",
      "news-to-markets",
    ],
    unlocks: [],
    whyPrerequisites:
      "Requires Security Analysis and specialized deep-dive topics to analyze complex real-world SEC filings and autopsies.",
    whyUnlocks:
      "The definitive fundamental analysis capstone: demonstrates synthesis of forensic audits, debt seniority, and intrinsic valuation on real corporate histories.",
    focusSummary:
      "Comprehensive investment memos, forensic company autopsies, and turnaround investment theses.",
    skillsGained: [
      "End-to-end investment memo creation",
      "Forensic balance sheet adjustments on live filings",
      "Defensible margin-of-safety valuation bounds",
      "Catalyst & thesis risk verification",
    ],
  },
  {
    id: "stock-machine-learning",
    stage: 4,
    stageName: "Specialized Deep Dives & Systems Architecture",
    domain: "quant",
    domainLabel: "Quantitative & Econometrics",
    prerequisites: ["statistical-foundations", "econometrics"],
    recommendedBefore: [],
    unlocks: ["algorithm-evaluation"],
    whyPrerequisites:
      "Builds upon linear factor regressions using non-linear decision trees, gradient boosting, and temporal sequences.",
    whyUnlocks:
      "Generates predictive ML signals and alpha weights that require rigorous validation in Algorithm Evaluation.",
    focusSummary:
      "Non-linear machine learning models (XGBoost, LightGBM, LSTM) for financial time-series prediction.",
    skillsGained: [
      "Purged & embargoed k-fold cross-validation",
      "Tree-based gradient boosting for returns",
      "Sequence modeling & recurrent architectures",
      "Feature engineering & lookahead leakage prevention",
    ],
  },
  {
    id: "c-hpc-trading",
    stage: 4,
    stageName: "Specialized Deep Dives & Systems Architecture",
    domain: "systems",
    domainLabel: "Systems & Algorithmic Bots",
    prerequisites: ["stock-bots"],
    recommendedBefore: [],
    unlocks: ["algorithm-evaluation"],
    whyPrerequisites:
      "Re-implements the event-driven bot architecture from Python Stock Bots into ultra-low-latency modern C17.",
    whyUnlocks:
      "Outputs deterministic, high-throughput execution engines ready for sub-microsecond latency profiling and audit in Algorithm Evaluation.",
    focusSummary:
      "Ultra-low-latency algorithmic trading in modern C17, lock-free data structures, and POSIX threads.",
    skillsGained: [
      "Modern C17 memory management & ownership",
      "Lock-free single-producer single-consumer queues",
      "Zero-copy networking & cache-line alignment",
      "SIMD vectorization for order book processing",
    ],
  },
  {
    id: "msme-financial-literacy",
    stage: 1,
    stageName: "Foundations & Market Mechanics",
    domain: "fundamentals",
    domainLabel: "Foundations & Ethics",
    prerequisites: [],
    recommendedBefore: [],
    unlocks: ["intelligent-investor", "data-hygiene"],
    whyPrerequisites:
      "The dedicated on-ramp for small business owners and non-technical adults. No prerequisites required.",
    whyUnlocks:
      "Builds the cash-flow awareness and accounting discipline needed to evaluate public equities and maintain clean financial records.",
    focusSummary:
      "Cash flow vs accounting profit, 12-month cash forecast capstone, break-even unit analysis, working capital cycles, and Indonesian UMKM tax obligations.",
    skillsGained: [
      "12-month cash flow forecasting",
      "Segregating personal & business accounts",
      "Single-product break-even calculations",
      "Indonesian UMKM tax compliance (PP 55/2022)",
    ],
  },
  {
    id: "spreadsheet-to-strategy-lab",
    stage: 2,
    stageName: "Core Analysis & Quantitative Modeling",
    domain: "quant",
    domainLabel: "Quantitative & Factor Methods",
    prerequisites: [],
    recommendedBefore: ["trading-fundamentals"],
    unlocks: ["strategy-lab", "stock-bots"],
    whyPrerequisites:
      "Designed for spreadsheet users; requires no programming background or prior platform experience.",
    whyUnlocks:
      "Bridges tabular spreadsheet thinking directly into Strategy Lab's 32-lesson track, Factor Studio, and automated stock bots.",
    focusSummary:
      "Translating spreadsheet models to OHLCV bar dictionaries, eliminating look-ahead bias, accounting for transaction friction, and saving versioned strategies.",
    skillsGained: [
      "Spreadsheet-to-code translation",
      "Causal execution & lag modeling",
      "Transaction friction & slippage accounting",
      "Strategy versioning & Factor Studio navigation",
    ],
  },
  {
    id: "data-hygiene",
    stage: 1,
    stageName: "Foundations & Market Mechanics",
    domain: "fundamentals",
    domainLabel: "Foundations & Ethics",
    prerequisites: [],
    recommendedBefore: [],
    unlocks: ["statistical-foundations", "econometrics"],
    whyPrerequisites:
      "Zero prerequisites. Open to spreadsheet investors, small bookkeepers, and curious analysts.",
    whyUnlocks:
      "Clean, tidy data is the foundation of institutional research, protecting subsequent econometric models from garbage-in garbage-out artifacts.",
    focusSummary:
      "Tidy data rules, detecting and repairing the 5 common tabular defects, eliminating survivorship and look-ahead biases, and reproducible pipelines.",
    skillsGained: [
      "Tidy data rectangular architecture",
      "Detecting 5 tabular defect classes",
      "Survivorship & look-ahead bias elimination",
      "Reproducible data cleaning pipelines",
    ],
  },
  {
    id: "conduct-compliance-essentials",
    stage: 1,
    stageName: "Foundations & Market Mechanics",
    domain: "fundamentals",
    domainLabel: "Foundations & Ethics",
    prerequisites: [],
    recommendedBefore: ["trading-fundamentals"],
    unlocks: ["security-analysis", "algorithm-evaluation"],
    whyPrerequisites:
      "No prerequisites. Suitable for MSME founders, junior corporate finance staff, and quantitative researchers.",
    whyUnlocks:
      "Yields a verifiable compliance certificate and grounds pre-trade risk controls and GIPS standards before algorithmic execution.",
    focusSummary:
      "Fiduciary duty of loyalty, client asset segregation, MNPI vs Mosaic Theory, market manipulation defense, SEC Rule 15c3-5 risk firewalls, and GIPS standards.",
    skillsGained: [
      "Fiduciary duty of loyalty & asset segregation",
      "MNPI & Mosaic Theory compliance",
      "Pre-trade risk controls & emergency kill switches",
      "GIPS compliant net-of-fee performance presentation",
    ],
  },
  {
    id: "python-reluctant-investor",
    stage: 1,
    stageName: "Foundations & Market Mechanics",
    domain: "quant",
    domainLabel: "Quantitative & Factor Methods",
    prerequisites: [],
    recommendedBefore: [],
    unlocks: ["spreadsheet-to-strategy-lab", "stock-bots"],
    whyPrerequisites:
      "Zero programming, finance, or advanced math required. Designed for non-coders and high-school students.",
    whyUnlocks:
      "Removes the fear of code, enabling learners to confidently enter the Strategy Lab and automated stock bot tracks.",
    focusSummary:
      "Zero-install Python execution, pandas CSV manipulation, rolling moving averages, trend charting, parameterization, and confident traceback debugging.",
    skillsGained: [
      "Interactive browser-based Python execution",
      "pandas DataFrame inspection & slicing",
      "Rolling moving average calculation",
      "Python traceback reading & error resolution",
    ],
  },
  {
    id: "algorithm-evaluation",
    stage: 4,
    stageName: "Specialized Deep Dives & Systems Architecture",
    domain: "systems",
    domainLabel: "Systems & Algorithmic Bots",
    prerequisites: ["stock-bots"],
    recommendedBefore: [
      "statistical-foundations",
      "econometrics",
      "strategy-lab",
      "c-hpc-trading",
      "stock-machine-learning",
    ],
    unlocks: [],
    whyPrerequisites:
      "Demands an operational algorithmic trading engine or factor model to evaluate and stress-test.",
    whyUnlocks:
      "The definitive quantitative capstone: certifies that a strategy is mathematically resilient against p-hacking, overfitting, and transaction slippage.",
    focusSummary:
      "Deflated Sharpe Ratio, combinatorial cross-validation, White's Reality Check, and institutional audit reporting.",
    skillsGained: [
      "Deflated Sharpe Ratio (DSR) & selection bias correction",
      "White's Reality Check for data-mining snooping",
      "Combinatorial Purged Cross-Validation (CPCV)",
      "Standardized institutional strategy audit reports",
    ],
  },
];

export const learningPathways: LearningPathway[] = [
  {
    id: "fundamental-analyst",
    title: "Fundamental Equity & Value Investor",
    subtitle:
      "From market basics to balance-sheet forensics and comprehensive company dossiers.",
    targetRole:
      "Equity Analyst · Value Fund Portfolio Manager · Buy-Side Researcher",
    badge: "Most Popular for Value",
    description:
      "Designed for investors who want to master Graham & Dodd valuation, deconstruct financial statements, identify durable moats, and build audit-grade investment memos.",
    steps: [
      {
        step: 1,
        trackId: "trading-fundamentals",
        whyThisStep:
          "Understand how shares, bid-ask spreads, and transaction costs work in the real market.",
        keyDeliverable:
          "Market microstructure fluency and compounding arithmetic mastery.",
      },
      {
        step: 2,
        trackId: "intelligent-investor",
        whyThisStep:
          "Build the psychological framework of Mr. Market and the discipline of margin of safety.",
        keyDeliverable:
          "Defensive vs enterprising asset allocation rules and valuation attitude.",
      },
      {
        step: 3,
        trackId: "security-analysis",
        whyThisStep:
          "The foundation of financial statement teardowns: income statements, balance sheets, and debt capacity.",
        keyDeliverable:
          "Comprehensive normalized earnings power and solvency models.",
      },
      {
        step: 4,
        trackId: "news-to-markets",
        whyThisStep:
          "Connect company news releases, SEC 8-K filings, and earnings surprises to market reactions.",
        keyDeliverable:
          "Ability to evaluate market sentiment against real corporate disclosures.",
      },
      {
        step: 5,
        trackId: "quality-moats",
        whyThisStep:
          "Identify structural competitive advantages that allow companies to sustain high ROIC.",
        keyDeliverable:
          "Moat durability scorecard and capital allocation evaluation.",
      },
      {
        step: 6,
        trackId: "forensic-accounting",
        whyThisStep:
          "Protect your capital by detecting aggressive accounting, accrual manipulation, and deceptive cash flows.",
        keyDeliverable: "Beneish M-Score and forensic earnings quality screen.",
      },
      {
        step: 7,
        trackId: "valuation-uncertainty",
        whyThisStep:
          "Learn reverse-DCF and probabilistic scenario modeling when valuing high-growth or volatile assets.",
        keyDeliverable:
          "Reverse DCF expectations model with margin-of-safety bounds.",
      },
      {
        step: 8,
        trackId: "real-world-casebook",
        whyThisStep:
          "Capstone: Synthesize forensic, debt, and quality analysis into complete investment dossiers.",
        keyDeliverable:
          "Professional investment thesis and forensic autopsy dossier.",
      },
    ],
  },
  {
    id: "quantitative-researcher",
    title: "Quantitative Researcher & Alpha Modeler",
    subtitle:
      "Mathematical modeling, multi-factor econometrics, machine learning, and strategy stress-testing.",
    targetRole: "Quantitative Researcher · Factor Strategist · Risk Modeler",
    badge: "Quant & Math Track",
    description:
      "For mathematically-minded researchers looking to build statistical rigor, formulate multi-factor asset pricing models, harness machine learning, and test alpha under transaction friction.",
    steps: [
      {
        step: 1,
        trackId: "trading-fundamentals",
        whyThisStep:
          "Ground mathematical concepts in market realities like liquidity, spreads, and order queues.",
        keyDeliverable:
          "Return calculation and execution friction understanding.",
      },
      {
        step: 2,
        trackId: "statistical-foundations",
        whyThisStep:
          "Master probability distributions, hypothesis testing, OLS regression, and stationarity diagnostics.",
        keyDeliverable:
          "Statistical toolkit and hypothesis testing framework for asset prices.",
      },
      {
        step: 3,
        trackId: "econometrics",
        whyThisStep:
          "Develop multi-factor asset pricing models (CAPM, Fama-French), GARCH volatility, and cointegration.",
        keyDeliverable:
          "Factor regression models and statistical arbitrage pair engines.",
      },
      {
        step: 4,
        trackId: "lab-workshop",
        whyThisStep:
          "Transition theory into practical Python worksheets and basic factor regressions.",
        keyDeliverable:
          "Scripted factor screening and return attribution code.",
      },
      {
        step: 5,
        trackId: "strategy-lab",
        whyThisStep:
          "Formulate systematic investment strategies, optimize factor weights, and model turnover friction.",
        keyDeliverable:
          "Multi-factor backtested portfolio with Sharpe and drawdown diagnostics.",
      },
      {
        step: 6,
        trackId: "stock-machine-learning",
        whyThisStep:
          "Apply gradient boosted trees and temporal sequence networks to capture non-linear market patterns.",
        keyDeliverable:
          "Purged cross-validated machine learning alpha pipeline.",
      },
      {
        step: 7,
        trackId: "algorithm-evaluation",
        whyThisStep:
          "Capstone: Conduct Deflated Sharpe Ratio audits to prove alpha is not a byproduct of data mining.",
        keyDeliverable:
          "Institutional algorithm verification and audit report.",
      },
    ],
  },
  {
    id: "algorithmic-systems",
    title: "Algorithmic Trader & High-Performance Systems Engineer",
    subtitle:
      "From execution ethics and paper simulators to Python bot architectures and bare-metal C17 pipelines.",
    targetRole:
      "Algorithmic Trader · Execution Quant · Low-Latency Systems Architect",
    badge: "Engineering & Bots",
    description:
      "Focuses on the engineering architecture of automated trading: asynchronous event loops, real-time WebSocket feeds, risk kill-switches, and nanosecond C execution.",
    steps: [
      {
        step: 1,
        trackId: "trading-fundamentals",
        whyThisStep:
          "Internalize order book priorities, fill types, and transaction fees.",
        keyDeliverable: "Exact understanding of exchange mechanics.",
      },
      {
        step: 2,
        trackId: "trading-ethics",
        whyThisStep:
          "Study regulatory boundaries (spoofing, wash trades, front-running) before deploying bot logic.",
        keyDeliverable:
          "Compliance ruleset to embed into automated trading code.",
      },
      {
        step: 3,
        trackId: "simulator-workshop",
        whyThisStep:
          "Gain muscle memory managing order flow and watching slippage in the interactive simulator.",
        keyDeliverable:
          "Empirical grasp of live order queues and book dynamics.",
      },
      {
        step: 4,
        trackId: "statistical-foundations",
        whyThisStep:
          "Learn the quantitative metrics needed to evaluate signal significance and manage position risk.",
        keyDeliverable:
          "Quantitative risk management rules (Value at Risk, volatility sizing).",
      },
      {
        step: 5,
        trackId: "stock-bots",
        whyThisStep:
          "Construct an asynchronous Python bot with live WebSocket streaming, state management, and safety kill-switches.",
        keyDeliverable:
          "Fully functional automated trading bot with paper execution.",
      },
      {
        step: 6,
        trackId: "c-hpc-trading",
        whyThisStep:
          "Re-engineer the bot in modern C17 for deterministic microsecond latency, zero-copy queues, and SIMD speed.",
        keyDeliverable:
          "High-performance C17 matching engine and execution pipeline.",
      },
      {
        step: 7,
        trackId: "algorithm-evaluation",
        whyThisStep:
          "Capstone: Subject the system to institutional audit: stress test against slippage, regime shifts, and latency delays.",
        keyDeliverable:
          "Complete institutional execution and algorithm performance dossier.",
      },
    ],
  },
  {
    id: "credit-special-situations",
    title: "Credit Analyst & Distressed Securities Specialist",
    subtitle:
      "Master debt structures, default risk modeling, bank solvency, and distressed restructurings.",
    targetRole:
      "Credit Analyst · Distressed Debt Researcher · Turnaround Specialist",
    badge: "Fixed Income & Credit",
    description:
      "For analysts focused on credit risk, debt recovery waterfalls, bank regulatory capital, and cyclical industrial companies.",
    steps: [
      {
        step: 1,
        trackId: "trading-fundamentals",
        whyThisStep:
          "Foundational asset mechanics, debt yields, and return arithmetic.",
        keyDeliverable: "Yield and interest compounding fluency.",
      },
      {
        step: 2,
        trackId: "security-analysis",
        whyThisStep:
          "Deconstruct corporate balance sheets, debt service capacity, and normalized earnings.",
        keyDeliverable: "Solvency and interest coverage models.",
      },
      {
        step: 3,
        trackId: "credit-distress",
        whyThisStep:
          "Model structural default risk (Merton, Altman Z) and map out bankruptcy recovery waterfalls.",
        keyDeliverable:
          "Debt seniority waterfall and covenant compliance assessment.",
      },
      {
        step: 4,
        trackId: "bank-analysis",
        whyThisStep:
          "Analyze financial intermediaries where debt is raw material: Net Interest Margin, CECL, and Basel III.",
        keyDeliverable: "Bank capital tier and asset-liability duration model.",
      },
      {
        step: 5,
        trackId: "cyclical-industrials",
        whyThisStep:
          "Examine capital-intensive, cyclical companies where operating leverage stresses debt capacity.",
        keyDeliverable:
          "Mid-cycle operating leverage and cash flow breakeven model.",
      },
      {
        step: 6,
        trackId: "forensic-accounting",
        whyThisStep:
          "Detect accounting maneuvers used by distressed firms to conceal covenant breaches.",
        keyDeliverable:
          "Forensic audit for hidden liabilities and aggressive capitalization.",
      },
      {
        step: 7,
        trackId: "real-world-casebook",
        whyThisStep:
          "Capstone: Build complete distressed restructuring and turnaround investment memos.",
        keyDeliverable:
          "Comprehensive distressed credit and reorganization memo.",
      },
    ],
  },
  {
    id: "web3-crypto-markets",
    title: "Decentralized Finance & Blockchain Microstructure",
    subtitle:
      "Cryptographic trust, automated market makers (AMMs), token economics, and smart contract architecture.",
    targetRole: "Web3 Researcher · Crypto Quant · Protocol Strategist",
    badge: "Crypto & Web3",
    description:
      "Explore the intersection of public ledger cryptography, automated liquidity pool equations, and multi-asset quantitative strategy testing.",
    steps: [
      {
        step: 1,
        trackId: "trading-fundamentals",
        whyThisStep:
          "Understand how traditional order books and bid-ask spreads operate to contrast with AMMs.",
        keyDeliverable: "Order book mechanics and market friction baseline.",
      },
      {
        step: 2,
        trackId: "web3",
        whyThisStep:
          "Dive deep into cryptography (secp256k1), blockchain state, AMM invariant curves (x*y=k), and token creation.",
        keyDeliverable:
          "Custom token implementation and AMM liquidity pool simulation.",
      },
      {
        step: 3,
        trackId: "lab-workshop",
        whyThisStep:
          "Write Python scripts to parse token trades, fee distributions, and pool returns.",
        keyDeliverable: "Data wrangling scripts for liquidity pool history.",
      },
      {
        step: 4,
        trackId: "strategy-lab",
        whyThisStep:
          "Construct and stress-test systematic strategies across traditional and crypto asset factors.",
        keyDeliverable:
          "Systematic multi-asset portfolio with impermanent loss hedging.",
      },
    ],
  },
];

const connectionMap = new Map<string, CourseConnection>(
  courseConnections.map((c) => [c.id, c]),
);

export function getConnection(trackId: string): CourseConnection | undefined {
  return connectionMap.get(trackId);
}

export function arePrerequisitesMet(
  trackId: string,
  state: WorkspaceState,
): boolean {
  const conn = connectionMap.get(trackId);
  if (!conn || conn.prerequisites.length === 0) return true;
  return conn.prerequisites.every((prereqId) => {
    const track = tracks.find((t) => t.id === prereqId);
    return track ? trackProgress(track, state).complete : false;
  });
}

export function getMissingPrerequisites(
  trackId: string,
  state: WorkspaceState,
): Track[] {
  const conn = connectionMap.get(trackId);
  if (!conn) return [];
  return conn.prerequisites
    .map((prereqId) => tracks.find((t) => t.id === prereqId))
    .filter(
      (track): track is Track =>
        track !== undefined && !trackProgress(track, state).complete,
    );
}

export type CourseReadiness = "completed" | "in_progress" | "ready" | "locked";

export function getCourseReadiness(
  track: Track,
  state: WorkspaceState,
): CourseReadiness {
  const progress = trackProgress(track, state);
  if (progress.complete) return "completed";
  if (progress.percent > 0) return "in_progress";
  const met = arePrerequisitesMet(track.id, state);
  return met ? "ready" : "locked";
}

export function getRecommendedNextTracks(state: WorkspaceState): Track[] {
  // 1. Any track currently in progress
  const inProgress = tracks.filter((t) => {
    const p = trackProgress(t, state);
    return p.percent > 0 && !p.complete;
  });
  if (inProgress.length > 0) return inProgress.slice(0, 3);

  // 2. Otherwise, tracks that are ready to start (prerequisites met, not started)
  const ready = tracks.filter((t) => {
    const p = trackProgress(t, state);
    return p.percent === 0 && arePrerequisitesMet(t.id, state);
  });
  if (ready.length > 0) {
    // Sort so Stage 1 comes before Stage 2 etc.
    return ready
      .sort((a, b) => {
        const connA = getConnection(a.id)?.stage ?? 4;
        const connB = getConnection(b.id)?.stage ?? 4;
        return connA - connB;
      })
      .slice(0, 3);
  }

  // 3. Fallback: Stage 1 tracks
  return tracks.filter((t) => t.id === "trading-fundamentals");
}
