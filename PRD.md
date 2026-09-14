# Product Requirements Document (PRD): Quanta LMS
**The Computational Finance Academy: An MBA & MFE-Grade Learning Management System**
*From Graham & Dodd Security Analysis to Quantitative Portfolio Engineering, Autonomous AI Stock Bots, and Cryptoeconomics*

---

## 1. Executive Summary & Academic Philosophy

### 1.1 Product Vision
**Quanta** is an open-source, university-accredited standard Learning Management System (LMS) engineered for computational finance, quantitative portfolio management, and automated algorithmic trading. The platform synthesizes the intellectual rigor of top-tier Master of Financial Engineering (MFE) and MBA curricula (such as Columbia Business School, Chicago Booth, Princeton BCF, Baruch MFE, and NYU Courant) with a live, sandboxed computational laboratory.

Quanta bridges four fundamental dimensions of financial economics and market practice:
1. **Classical Fundamental Valuation**: Rigorous balance sheet deconstruction, earnings power normalization, debt coverage covenants, and margin-of-safety principles anchored in Benjamin Graham & David Dodd’s *Security Analysis* (1934/1940 editions) and modern corporate finance theory (Penman, Greenwald).
2. **Quantitative Econometrics & Factor Investing**: Statistical inference, hypothesis testing, time-series econometrics (ARIMA, GARCH), multi-factor asset pricing (CAPM, Fama-French 3/5, Carhart), and risk management (VaR, CVaR, Deflated Sharpe Ratio) anchored in the CFA Institute’s *Quantitative Investment Analysis* (fourth edition, 2020).
3. **Autonomous Execution, Generative AI & Web3 Cryptoeconomics**: Production-grade algorithmic trading systems, market microstructure (order book dynamics, Almgren-Chriss optimal execution), Machine Learning alpha models (XGBoost, deep tabular learning), Multi-Agent LLM fundamental equity analysts, decentralized finance (DeFi) automated market makers (Constant Product & Concentrated Liquidity AMMs), tokenomics, and cross-venue arbitrage bots.
4. **Institutional Stock Buying & Selling Simulator**: A high-fidelity simulated brokerage and exchange matching engine supporting both manual graphical trading and programmatic API execution. Features continuous double-auction order matching, Level 2 Depth of Market (DOM), advanced order types (Market, Limit, Stop-Loss, Stop-Limit, Trailing Stop, OCO Bracket, TWAP/VWAP), Regulation T margin accounts with leverage, short selling with stock borrow locates and daily borrow fee accrual, forced margin liquidations, realistic queue priority fill probability, and real-time mark-to-market trade blotters.

### 1.2 Design Axiom: "Substance Over Decoration"
Modern educational software is saturated with cognitive noise—distracting gamification, cartoon mascots, marketing popups, and non-reproducible video lectures. Quanta operates on an institutional academic design ethos:
* **Academic Editorial Typography**: Clear typographic hierarchy using `Inter`/`Geist Sans` for long-form theoretical expositions, native `KaTeX` for crisp LaTeX mathematical proofs, and `JetBrains Mono` with tabular numeral alignment (`tabular-nums`) for code and financial statements.
* **Dual-Pane Computational Lecture Hall**: A synchronized split-screen reading and execution environment. The left pane provides university-level lecture chapters, derivations, historical filings, and footnotes. The right pane provides an embedded Python Monaco code editor, interactive TradingView financial charts, and an output console executing in $< 1.5$ seconds.
* **TradingView-Style Stock Trading Simulator**: A dedicated chart-first paper-trading workspace with a drawing toolbar, indicators, watchlist, buy/sell ticket, and tabbed positions/order-history panel. Learners practice manual stock trading from the beginner course onward. Section 6.3 defines the new terminal, its first-release scope, and acceptance criteria; advanced execution capabilities in Section 5.3 extend it in later releases.
* **Zero Marketing Bloat**: Restrained monochrome palette (Slate-950/Slate-50), with color reserved strictly for directional market data (Emerald positive yield, Rose drawdowns/losses, Indigo benchmark equity curves).

---

## 2. Target Audience, Personas & Academic Prerequisites

| Academic Persona | Academic & Professional Baseline | Target Learning Outcome | Recommended Entry Track |
| :--- | :--- | :--- | :--- |
| **MFE / Quantitative Finance Student** | Strong mathematics/programming (Linear algebra, multivariable calculus, Python); limited accounting and corporate financial reporting experience. | Master forensic accounting, balance sheet liquidation haircuts, point-in-time filing hygiene, and real market microstructure. | Track 1 (Deep-dive on *Security Analysis*) $\rightarrow$ Tracks 3, 5, 6 |
| **MBA Finance / CFA Candidate** | Corporate finance, financial reporting analysis, DCF modeling, Excel; minimal coding and statistical econometrics experience. | Transition to quantitative screening, systematic risk modeling, statistical arbitrage, and autonomous Python trading systems. | Track 1 $\rightarrow$ Track 2 (Statistical foundations) $\rightarrow$ Tracks 3, 4 |
| **Software Engineer / Systems Architect** | Distributed systems, Python/C++, databases; minimal financial economics background. | Understand capital allocation mathematics, factor risk premiums, financial time series, and market-neutral trading. | Full Curriculum (Track 1 through Track 6) |
| **Quantitative Researcher / Prop Trader** | Econometrics and strategy prototyping; seeking to build end-to-end autonomous AI and Web3 bots. | Master LLM-driven qualitative forensic analysis, MEV searcher architecture, and concentrated liquidity AMM modeling. | Tracks 4, 5, and 6 |

---

## 3. System Architecture & Technical Stack

```
                                  CLIENT BROWSER (REACT 18+)
+---------------------------------------------------------------------------------------------------+
|  Top Bar: [QUANTA]  Track > Chapter > Section  |  Kernel: Ready (Python 3.11)  |  Theme: Slate   |
+-----------------------------------------------------------------+---------------------------------+
|                      LEFT: THEORY & LECTURE                     |        RIGHT: EXECUTION LAB     |
|                                                                 | [Mode: Real Historical / Synth] |
| - University Lecture Notes & LaTeX Derivations (KaTeX)          |---------------------------------|
| - Historical SEC 10-K Excerpts & Interactive Filing Tables      | - Monaco Python Editor          |
| - Methodological Proofs & Case Studies                          | - Syntax Highlighting & Linting |
| - Graded Academic Exercises & Derivation Prompts                | - Preloaded Quanta SDK          |
|                                                                 |---------------------------------|
| [Transfer Formula to Sandbox ->]                                | [ > Run Simulation (Cmd+Enter)] |
|                                                                 |---------------------------------|
|                                                                 | - TradingView Lightweight Chart |
|                                                                 | - Drawdown & Distribution Plots |
|                                                                 | - Metrics Table & Log Stream    |
+-----------------------------------------------------------------+---------------------------------+
                                                  | HTTPS / WebSockets
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                    FASTAPI BACKEND SYSTEM                                         |
|  +--------------------------------+  +--------------------------------+  +---------------------+  |
|  |   Core Academic LMS Engine     |  |   Quantitative Analytics API   |  | Synthetic Generator |  |
|  |   - Auth & Role-Based Access   |  |   - Return & Risk Decomposition|  | - GBM & Heston Vol  |  |
|  |   - Progress & Exercise Grader |  |   - Factor Regression Engine   |  | - Jump-Diffusion    |  |
|  |   - Code Snapshot Versioning   |  |   - Mock Broker Matching Engine|  | - Markov Regimes    |  |
|  +--------------------------------+  +--------------------------------+  +---------------------+  |
+-----------------------------------+-----------------------------------+---------------------------+
                                    |                                   |
                                    v                                   v
+---------------------------------------------------+   +-------------------------------------------+
|               DATA STORAGE & OLAP                 |   |        SANDBOX EXECUTION RUNNER           |
| - PostgreSQL: Student State, Submissions, Notes   |   | - Isolated Subprocess / Container Worker  |
| - DuckDB / Parquet: 30+ Years US Equity OHLCV,    |   | - Strict Resource Bounds (256MB, 2.0s)    |
|   Point-in-Time Financials, Crypto & Macro Curves |   | - AST Filter (Blocks OS/Network Abuse)    |
| - Redis: Sessions, Task Queues, Rate-Limiting     |   | - Pre-warmed: NumPy, SciPy, Statsmodels   |
+---------------------------------------------------+   +-------------------------------------------+
```

### 3.1 Frontend Architecture (React + Vite)
* **Framework**: React 18+ bootstrapped with Vite, TypeScript 5.x.
* **Component Architecture**: Modular dual-pane layout using Radix UI primitives (`ResizablePanel`, `Accordion`, `Dialog`, `DropdownMenu`).
* **Code Editor**: `@monaco-editor/react` embedded with customized Python language server settings, auto-closing brackets, syntax validation, and theme token bindings to Tailwind grayscale.
* **Financial Charting**:
  * `lightweight-charts` (TradingView Canvas engine): High-frequency rendering of multi-year EOD and intraday candlesticks, volume bars, overlay moving averages, Bollinger bands, and order execution markers.
  * `recharts` & `d3`: Rendering probability density curves, underwater drawdown series, monthly return heatmaps, and factor correlation matrices.
* **Math & Typography**:
  * `KaTeX`: Accelerated client-side LaTeX math rendering with error-fallback boundaries.
  * Custom Markdown parser supporting GitHub Flavored Markdown (GFM), syntax-highlighted code fences, custom alerts (`[!NOTE]`, `[!WARNING]`, `[!TIP]`), and interactive data tables.

### 3.2 Backend Architecture (FastAPI + Async Python)
* **API Framework**: FastAPI 0.110+ leveraging Python 3.11 `asyncio` event loop.
* **Data Validation & Schemas**: Pydantic v2 for high-speed serialization/deserialization.
* **Relational Database**: PostgreSQL 16 managed via SQLModel (unifying SQLAlchemy 2.0 async engine and Pydantic).
* **OLAP Analytics Engine**: Embedded DuckDB querying compressed columnar Apache Parquet files for point-in-time financial statement items and historical price bars.
* **In-Memory Caching & Asynchronous Queues**: Redis 7.x utilized for session management, API rate-limiting, and background compute task queuing via ARQ / Celery.

### 3.3 Sandboxed Code Execution Worker
* **Security Isolation**: Execution of student Python code in an ephemeral, unprivileged worker environment with restricted OS permissions.
* **Abstract Syntax Tree (AST) Validation**: Student-submitted code is parsed via Python's `ast` module prior to execution. Any AST node attempting to import prohibited modules (`os`, `sys`, `subprocess`, `socket`, `shutil`, `ctypes`, `builtins.eval`, `builtins.exec`, `pty`) is rejected before compilation.
* **Resource Constraints**:
  * CPU execution timeout: 2.0 seconds hard ceiling enforced via `signal.SIGALRM` or Linux `prlimit`.
  * RAM ceiling: 256 MB per runner process enforced via OS `rlimit`.
  * Network egress: Completely disabled at the process level (sandbox has no outbound socket permissions; all market data is pre-mounted).
* **Preloaded Mathematical Stack**: Pre-warmed runtime environment containing `numpy`, `pandas`, `polars`, `scipy`, `statsmodels`, `vectorbt`, and the custom `quanta` client SDK.

### 3.4 Quanta Client SDK (`quanta.*`) Architecture & API Specification

The platform provides a first-class Python client library, `quanta`, exposed automatically to all student sandboxes. It standardizes data access, metrics computation, stochastic simulation, and mock broker interaction.

```
                                      QUANTA SDK MODULE HIERARCHY
+---------------------------------------------------------------------------------------------------+
| quanta                                                                                            |
|  ├── data                                                                                         |
|  │    ├── get_financial_statements(ticker: str, year: int) -> FinancialStatements                |
|  │    ├── get_point_in_time_bs(ticker: str, as_of_date: str) -> BalanceSheet                     |
|  │    ├── get_historical_ohlcv(ticker: str, start: str, end: str, adj: bool = True) -> DataFrame |
|  │    ├── get_macro(indicator: str, year_or_date: str | int) -> float                           |
|  │    └── get_universe(as_of_date: str) -> list[str]                                              |
|  ├── metrics                                                                                      |
|  │    ├── calculate_sharpe(returns: ndarray, rf: float = 0.0) -> float                            |
|  │    ├── calculate_sortino(returns: ndarray, target: float = 0.0) -> float                       |
|  │    ├── calculate_max_drawdown(equity_curve: ndarray) -> tuple[float, int, int]                 |
|  │    ├── calculate_var(returns: ndarray, alpha: float = 0.05, method: str = 'hist') -> float    |
|  │    ├── calculate_cvar(returns: ndarray, alpha: float = 0.05) -> float                          |
|  │    ├── calculate_dsr(sr: float, n_trials: int, var_trials: float, t: int) -> float            |
|  │    └── rank_information_coefficient(scores: Series, fwd_returns: Series) -> float             |
|  ├── synthetic                                                                                    |
|  │    ├── simulate_gbm(s0: float, mu: float, sigma: float, t: float, steps: int) -> ndarray      |
|  │    ├── simulate_merton_jump(s0, mu, sigma, lamb, mu_j, sigma_j, t, steps) -> ndarray          |
|  │    ├── simulate_heston(s0, v0, mu, kappa, theta, xi, rho, t, steps) -> ndarray                |
|  │    └── simulate_markov_regimes(p_matrix: ndarray, state_params: list, steps: int) -> ndarray  |
|  └── broker                                                                                       |
|       ├── PaperBroker(initial_cash: float = 100000.0, margin_multiplier: float = 2.0)             |
|       │    ├── buy(symbol, qty, order_type, limit_price, stop_price) -> Order                    |
|       │    ├── sell(symbol, qty, order_type, limit_price, stop_price) -> Order                   |
|       │    ├── short(symbol, qty, order_type, limit_price) -> Order                               |
|       │    ├── cover(symbol, qty, order_type, limit_price) -> Order                               |
|       │    ├── bracket_order(symbol, side, qty, entry, take_profit, stop_loss) -> tuple[Order]   |
|       │    ├── cancel_order(order_id: str) -> bool                                                |
|       │    ├── cancel_all_orders(symbol: str = None) -> int                                       |
|       │    ├── get_positions() -> dict[str, Position]                                             |
|       │    ├── get_account() -> AccountSummary                                                    |
|       │    ├── get_order_book(symbol: str, depth: int = 10) -> dict                               |
|       │    └── on_fill(callback: Callable[[Order], None]) -> None                                 |
+---------------------------------------------------------------------------------------------------+
```

#### Detailed Class & Function Signatures

```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict, Callable

class FinancialStatements:
    ticker: str
    fiscal_year: int
    filing_date: str
    sales: float
    gross_profit: float
    ebit: float
    net_income: float
    diluted_eps: float
    current_assets: float
    cash_and_equivalents: float
    receivables: float
    inventory: float
    total_assets: float
    current_liabilities: float
    long_term_debt: float
    total_debt: float
    total_liabilities: float
    shareholders_equity: float
    tangible_book_value: float
    operating_cash_flow: float
    capital_expenditures: float
    free_cash_flow: float
    shares_outstanding: float

class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_LOSS = "STOP_LOSS"
    STOP_LIMIT = "STOP_LIMIT"
    TRAILING_STOP = "TRAILING_STOP"
    BRACKET = "BRACKET"  # OCO Entry + Take Profit + Stop Loss
    TWAP = "TWAP"
    VWAP = "VWAP"

class TimeInForce(str, Enum):
    DAY = "DAY"
    GTC = "GTC"  # Good Till Canceled
    IOC = "IOC"  # Immediate Or Cancel
    FOK = "FOK"  # Fill Or Kill

@dataclass
class Order:
    order_id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    trailing_delta: Optional[float] = None  # in $ or %
    take_profit_price: Optional[float] = None
    stop_loss_price: Optional[float] = None
    time_in_force: TimeInForce = TimeInForce.GTC
    status: str = "PENDING"  # PENDING, FILLED, PARTIALLY_FILLED, CANCELLED, REJECTED
    filled_quantity: float = 0.0
    avg_fill_price: float = 0.0
    commission_usd: float = 0.0
    created_at: str = ""

@dataclass
class Position:
    symbol: str
    quantity: float  # Positive for long, negative for short
    avg_entry_price: float
    current_mark_price: float
    market_value: float
    unrealized_pnl: float
    realized_pnl: float
    borrow_rate_apr: float = 0.0  # Annualized borrow cost for shorted equities

@dataclass
class AccountSummary:
    cash_balance: float
    portfolio_equity: float
    long_market_value: float
    short_market_value: float
    initial_margin_requirement: float
    maintenance_margin_requirement: float
    excess_liquidity: float
    buying_power: float
    margin_utilization_pct: float
    is_margin_call: bool

class PaperBroker:
    """
    High-fidelity simulated brokerage client for manual and algorithmic trading.
    Supports continuous double-auction fill models, Reg T margining, and short selling.
    """
    def __init__(self, initial_cash: float = 100_000.0, margin_multiplier: float = 2.0, commission_bps: float = 5.0): ...
    def buy(self, symbol: str, quantity: float, order_type: OrderType = OrderType.MARKET, limit_price: Optional[float] = None, **kwargs) -> Order: ...
    def sell(self, symbol: str, quantity: float, order_type: OrderType = OrderType.MARKET, limit_price: Optional[float] = None, **kwargs) -> Order: ...
    def short(self, symbol: str, quantity: float, order_type: OrderType = OrderType.MARKET, limit_price: Optional[float] = None, **kwargs) -> Order: ...
    def cover(self, symbol: str, quantity: float, order_type: OrderType = OrderType.MARKET, limit_price: Optional[float] = None, **kwargs) -> Order: ...
    def bracket_order(self, symbol: str, side: OrderSide, quantity: float, entry_price: float, take_profit: float, stop_loss: float) -> tuple[Order, Order, Order]: ...
    def cancel_order(self, order_id: str) -> bool: ...
    def cancel_all_orders(self, symbol: Optional[str] = None) -> int: ...
    def get_open_orders(self, symbol: Optional[str] = None) -> List[Order]: ...
    def get_positions(self) -> Dict[str, Position]: ...
    def get_account(self) -> AccountSummary: ...
    def get_order_book(self, symbol: str, depth: int = 10) -> dict: ...
    def on_fill(self, callback: Callable[[Order], None]) -> None: ...
```

---

## 4. Comprehensive University & MBA Curriculum Syllabus

The curriculum is structured across **6 Academic Tracks**, comprising **28 Chapters** and **114 Granular Sections**, matching the scope and depth of a two-year Master of Financial Engineering sequence.

```mermaid
flowchart LR
    T1["Track 1: CBS-FIN 601<br/>Security Analysis & Valuation"] --> T2["Track 2: MFE-STAT 501<br/>Statistical Foundations"]
    T2 --> T3["Track 3: MFE-ECON 502<br/>Advanced Econometrics & Factors"]
    T3 --> T4["Track 4: MFE-LAB 601<br/>The Quantitative Strategy Lab"]
    T4 --> T5["Track 5: MFE-ENG 701<br/>Stock Bots & AI Systems"]
    T5 --> T6["Track 6: MFE-CRYPTO 801<br/>Web3, DeFi & Crypto Bots"]
```

---

### Book-course expansion — current learning requirements

The current Track 1 and Track 2 reading courses supersede the earlier five-module implementations. Preserve existing lesson URLs, saved code, notes, and first-question answer keys. Their detailed authoring map and edition references are in [Book courses](docs/BOOK_COURSES.md).

- **Security Analysis:** 24 substantial original lessons, organized around the 1940 edition’s seven parts: analytical method; fixed claims; preferred/convertible participation; common ownership; earnings; assets; comparisons and investment decisions. Keep the later growth heuristic and modern cash-flow models in a separately labeled extension unit. Include an original investment committee capstone with a reconciled claims schedule and valuation scenarios.
- **Quantitative Investment Analysis:** 28 original lessons, two for each of the fourth edition’s 14 chapters, spanning cash-flow mathematics, descriptive statistics, probability, distributions, estimation, tests, regression, time series, machine learning, data projects, factor models, risk, and backtesting. Include a reproducible research capstone with costs and uncertainty.
- Every lesson includes a measurable objective, book-reading connection, original worked example, equation, executable small-data worksheet, two practice questions, and a written assignment with a collapsible worked solution. Book-study lessons open in reading view; the sandbox remains available on demand.
- Each expanded course includes four four-question checkpoints at unit boundaries and one independent final covering every module (24 and 28 questions respectively). Checkpoints require 75%; finals require 80%. Keep final IDs and increment their version to 2 so earlier short-exam passes do not certify the expanded assessment.
- Reading plans show the edition, source links, prerequisites, outcomes, and linked units. Assignment drafts can be saved as lesson-linked notebook entries. Written capstones use an explicit self-review rubric; numerical exams are graded separately.
- These are independent original companion lessons, not reproduced book chapters or publisher question banks. The advanced automation examples in the roadmap below are separate implementation ambitions and should not be represented as quotations, methods, or completed labs from the historical book.

### TRACK 1: CBS-FIN 601 — Classical Security Analysis & Fundamental Equity Valuation
*Graduate-level corporate valuation anchored in Benjamin Graham & David Dodd’s Security Analysis (1934/1940 Editions), updated with modern financial reporting (US GAAP / IFRS).*

#### Chapter 1: The Epistemology of Value Investing & Market Psychology
* **Section 1.1: The Operational Definition of Investment vs. Speculation**
  * *Lecture Content*: Analysis of Graham & Dodd’s foundational definition: "An investment operation is one which, upon thorough analysis, promises safety of principal and an adequate return. Operations not meeting these requirements are speculative." Formalizing the distinction between intrinsic value-anchored cash flow expectations and speculative multi-period price multiple expansion.
  * *Required Readings*: Graham & Dodd (1934), Chapters 1 & 2; Seth Klarman, *Margin of Safety* (1991), Chapter 1.
  * *Mathematical Concept*: The price-to-value divergence dynamic:
    $$P_t = V_t + \epsilon_t, \quad \text{where } \epsilon_t \sim \text{Noise-Trader Sentiment Process}$$
* **Section 1.2: Market Psychology & The Limits to Arbitrage**
  * *Lecture Content*: The "Mr. Market" allegory formalized through behavioral economics. Shleifer & Vishny (1997) "Limits to Arbitrage": capital withdrawal risk, margin requirements, and divergence persistence.
  * *Required Readings*: Andrei Shleifer, *Inefficient Markets: An Introduction to Behavioral Finance* (2000).
* **Section 1.3: The Margin of Safety as a Non-Probabilistic Risk Paradigm**
  * *Lecture Content*: Contrasting modern portfolio theory’s variance-based risk ($\sigma$) with Graham’s margin of safety. Why volatility is not risk for the enterprise owner; structural discounts acting as buffers against future adverse business developments and forecasting errors.
* *Sandbox Lab 1: Historic Margin of Safety Band Calculator*
  * *Objective*: Compute dynamic historical margin-of-safety bands on industrial and consumer companies during major macroeconomic panics (1973–74, 2000–02, 2008–09).
  * *Starter Code*:
    ```python
    import numpy as np
    import pandas as pd
    import quanta as qn

    def calculate_margin_of_safety(ticker: str, fiscal_year: int) -> dict:
        fs = qn.data.get_financial_statements(ticker, fiscal_year)
        market_cap = qn.data.get_market_cap(ticker, fiscal_year)
        
        # Graham conservative enterprise valuation
        norm_earnings = np.mean([fs.history[yr].net_income for yr in range(fiscal_year-5, fiscal_year)])
        reproduction_assets = fs.balance_sheet.tangible_assets - fs.balance_sheet.total_liabilities
        intrinsic_val = 0.5 * (norm_earnings * 8.5) + 0.5 * reproduction_assets
        
        mos_pct = (intrinsic_val - market_cap) / intrinsic_val
        return {"intrinsic_value": intrinsic_val, "market_cap": market_cap, "margin_of_safety": mos_pct}
    ```
  * *Test Assertions*: Assert `margin_of_safety > 0.33` correctly identifies historically distressed bargains in 2008 without survivorship bias.

#### Chapter 2: Balance Sheet Deconstruction & Liquidation Value
* **Section 2.1: Going-Concern Book Value vs. Orderly Liquidation Value**
  * *Lecture Content*: Systematic balance sheet discounts and haircuts based on Graham & Dodd asset realization tables:
    * Cash & Cash Equivalents: $100\%$ of face value.
    * Trade Receivables: $75\% - 90\%$ (adjusting for days sales outstanding and doubtful allowance).
    * Inventories: $50\% - 75\%$ (raw materials vs. work-in-progress vs. finished goods; FIFO vs. LIFO reserves).
    * Fixed Assets (PP&E): $0\% - 25\%$ (specialized machinery vs. marketable commercial real estate).
* **Section 2.2: Net-Current-Asset Value (NCAV) & Net-Net Working Capital (NNWC)**
  * *Lecture Content*: Derivation and empirical performance of Graham's Net-Net formulas:
    $$\text{NCAV} = \text{Current Assets} - \text{Total Liabilities} - \text{Preferred Stock}$$
    $$\text{NNWC} = (\text{Cash} + 0.75 \times \text{Accounts Receivable} + 0.50 \times \text{Inventory}) - \text{Total Liabilities}$$
* **Section 2.3: Off-Balance-Sheet Liabilities & Contingent Claims**
  * *Lecture Content*: Capitalizing operating lease obligations (ASC 842 / IFRS 16 rules); calculating debt equivalents of multi-employer pension deficits, post-retirement healthcare liabilities, environmental cleanup reserves, and legal contingencies.
* **Section 2.4: Quantitative Insolvency Diagnostics: Altman Z-Score & Ohlson O-Score**
  * *Lecture Content*: The five-variable Altman Z-Score for public manufacturing corporations:
    $$Z = 1.2 X_1 + 1.4 X_2 + 3.3 X_3 + 0.6 X_4 + 0.999 X_5$$
    *(where $X_1 = \text{WC}/\text{TA}$, $X_2 = \text{RE}/\text{TA}$, $X_3 = \text{EBIT}/\text{TA}$, $X_4 = \text{MktEq}/\text{TotLiab}$, $X_5 = \text{Sales}/\text{TA}$).*
* *Sandbox Lab 2: Automated SEC 10-K Net-Net & Solvency Auditor*
  * *Objective*: Ingest raw point-in-time balance sheets from SEC EDGAR and compute NCAV, NNWC, and Altman Z-Score.
  * *Starter Code*:
    ```python
    import quanta as qn

    def audit_balance_sheet(ticker: str, filing_date: str) -> dict:
        bs = qn.data.get_point_in_time_bs(ticker, filing_date)
        ncav = bs.current_assets - bs.total_liabilities - bs.preferred_stock
        nnwc = (bs.cash + 0.75 * bs.receivables + 0.50 * bs.inventory) - bs.total_liabilities
        
        # Calculate Altman Z
        x1 = (bs.current_assets - bs.current_liabilities) / bs.total_assets
        x2 = bs.retained_earnings / bs.total_assets
        x3 = bs.ebit / bs.total_assets
        x4 = bs.market_equity / bs.total_liabilities
        x5 = bs.revenue / bs.total_assets
        z_score = 1.2*x1 + 1.4*x2 + 3.3*x3 + 0.6*x4 + 0.999*x5
        
        return {"ncav": ncav, "nnwc": nnwc, "altman_z": z_score, "is_distressed": z_score < 1.81}
    ```

#### Chapter 3: Income Statement Deconstruction & Quality of Earnings
* **Section 3.1: The Sloan Accrual Anomaly & Earnings Quality**
  * *Lecture Content*: Richard Sloan (1996): Decomposition of reported net operating income into cash flows from operations and accruals. Proving why firms with high accrual components experience negative forward return drift:
    $$\text{Accruals} = (\Delta\text{Current Assets} - \Delta\text{Cash}) - (\Delta\text{Current Liabilities} - \Delta\text{ST Debt} - \Delta\text{Taxes Payable}) - \text{Depreciation}$$
* **Section 3.2: Revenue Recognition & Manipulation Detection (Beneish M-Score)**
  * *Lecture Content*: Professor Messod Beneish (1999): Eight-variable probit model predicting financial statement manipulation:
    $$M = -4.84 + 0.920 \text{DSRI} + 0.528 \text{GMI} + 0.404 \text{AQI} + 0.892 \text{SGI} + 0.115 \text{DEPI} - 0.172 \text{SGAI} + 4.037 \text{TATA} + 0.0327 \text{LVGI}$$
    *Firms with $M > -1.78$ indicate high probability of earnings manipulation.*
* **Section 3.3: Inventory Accounting Under Price Shocks**
  * *Lecture Content*: LIFO reserve liquidation, phantom inventory profits, FIFO gross margin distortion during inflationary spikes, and Lower-of-Cost-or-Market (LCM) write-downs.
* **Section 3.4: Normalized Earning Power Across Economic Cycles**
  * *Lecture Content*: 7- to 10-year rolling cycle smoothing; adjustments for non-recurring restructuring charges, litigation settlements, and cyclical capacity utilization.
* *Sandbox Lab 3: Forensic Earnings Quality & Beneish M-Score Auditor*
  * *Objective*: Build an automated scanner calculating Sloan Accruals and the 8-variable Beneish M-Score on multi-year SEC 10-K filings.
  * *Starter Code*:
    ```python
    import numpy as np
    import quanta as qn

    def calculate_beneish_m_score(ticker: str, year: int) -> dict:
        curr = qn.data.get_financial_statements(ticker, year)
        prev = qn.data.get_financial_statements(ticker, year - 1)
        
        # 1. Days Sales in Receivables Index (DSRI)
        dsri = (curr.receivables / curr.sales) / (prev.receivables / prev.sales)
        # 2. Gross Margin Index (GMI)
        gmi = (prev.gross_margin) / (curr.gross_margin)
        # 3. Asset Quality Index (AQI)
        aqi_curr = 1 - (curr.current_assets + curr.ppne) / curr.total_assets
        aqi_prev = 1 - (prev.current_assets + prev.ppne) / prev.total_assets
        aqi = aqi_curr / aqi_prev if aqi_prev > 0 else 1.0
        # 4. Sales Growth Index (SGI)
        sgi = curr.sales / prev.sales
        # 5. Depreciation Index (DEPI)
        dep_rate_prev = prev.depreciation / (prev.depreciation + prev.ppne)
        dep_rate_curr = curr.depreciation / (curr.depreciation + curr.ppne)
        depi = dep_rate_prev / dep_rate_curr if dep_rate_curr > 0 else 1.0
        # 6. SG&A Expense Index (SGAI)
        sgai = (curr.sga / curr.sales) / (prev.sga / prev.sales)
        # 7. Total Accruals to Total Assets (TATA)
        tata = (curr.net_income - curr.operating_cash_flow) / curr.total_assets
        # 8. Leverage Index (LVGI)
        lvgi = (curr.total_debt / curr.total_assets) / (prev.total_debt / prev.total_assets)
        
        m_score = (-4.84 + 0.920*dsri + 0.528*gmi + 0.404*aqi + 0.892*sgi 
                   + 0.115*depi - 0.172*sgai + 4.037*tata + 0.0327*lvgi)
                   
        return {
            "m_score": float(m_score),
            "is_manipulator": m_score > -1.78,
            "sloan_accrual_ratio": float(tata),
            "components": {"dsri": dsri, "gmi": gmi, "sgi": sgi, "tata": tata}
        }
    ```
  * *Test Suite Assertions*:
    ```python
    def test_beneish_auditor():
        # Test on Enron FY2000 filing (classic historic failure)
        res = calculate_beneish_m_score("ENE", 2000)
        assert res["m_score"] > -1.78, "Enron FY2000 must flag as high manipulation probability"
        assert res["is_manipulator"] is True
    ```

#### Chapter 4: Fixed-Income & Senior Security Analysis
* **Section 4.1: The Protective Screening Criteria for Debt Securities**
  * *Lecture Content*: Graham & Dodd’s principles of bond selection: Negative art (exclusion over inclusion); adequacy of coverage under worst-case historical depression conditions rather than normal conditions.
* **Section 4.2: Fixed-Charge Coverage Ratios**
  * *Lecture Content*: Prior-deductions method vs. cumulative deductions method for subordinated debentures and holding company debt:
    $$\text{FCC} = \frac{\text{EBIT} + \text{Operating Lease Interest}}{\text{Gross Interest Expense} + \text{Operating Lease Interest} + \frac{\text{Preferred Dividends}}{1 - t}}$$
* **Section 4.3: Capital Structure Priority & Indenture Covenants**
  * *Lecture Content*: Restricted payments baskets, debt incurrence tests, maintenance covenants, springing liens, and structural subordination.
* *Sandbox Lab 4: Debt Covenant & Solvency Stress Test Simulator*
  * *Objective*: Ingest corporate credit profiles and simulate revenue drops to test debt service breach probabilities.
  * *Starter Code*:
    ```python
    import quanta as qn

    def stress_test_covenants(ticker: str, year: int, revenue_shock_pct: float = -0.30) -> dict:
        fs = qn.data.get_financial_statements(ticker, year)
        tax_rate = max(0.21, fs.income_tax_expense / fs.ebt) if fs.ebt > 0 else 0.21
        
        # Baseline coverage
        base_fcc = (fs.ebit + fs.lease_interest) / (fs.interest_expense + fs.lease_interest + fs.pref_dividends / (1 - tax_rate))
        
        # Stressed EBIT calculation (assuming operating leverage of 1.8x)
        ebit_drop_pct = revenue_shock_pct * 1.8
        stressed_ebit = fs.ebit * (1 + ebit_drop_pct)
        stressed_fcc = (stressed_ebit + fs.lease_interest) / (fs.interest_expense + fs.lease_interest + fs.pref_dividends / (1 - tax_rate))
        
        covenant_breached = stressed_fcc < 1.50  # Standard institutional high-yield threshold
        return {
            "baseline_fcc": float(base_fcc),
            "stressed_fcc": float(stressed_fcc),
            "breached": covenant_breached,
            "interest_coverage_cushion": float(base_fcc - 1.50)
        }
    ```

#### Chapter 5: Valuation Syntheses & Modern Adaptations
* **Section 5.1: The Classical and Revised Graham Growth Formulas**
  * *Lecture Content*: The original 1962 formula: $V = \text{EPS} \times (8.5 + 2g)$. The revised formula scaling by prevailing AAA corporate bond yield ($Y$):
    $$V = \frac{\text{EPS} \times (8.5 + 2g) \times 4.4}{Y}$$
* **Section 5.2: Bruce Greenwald’s Earnings Power Value (EPV) Framework**
  * *Lecture Content*: Calculating Normalized Sustainable NOPAT; Capitalized Cost of Capital ($WACC$); Reproduction Cost of Assets vs. EPV; evaluating franchise competitive moats when $\text{EPV} > \text{Reproduction Cost}$.
* **Section 5.3: Return on Invested Capital (ROIC) & Economic Moats**
  * *Lecture Content*: NOPAT / Invested Capital decomposition; identifying durable competitive advantages vs. mean-reverting industry returns.
* **Section 5.4: Accounting for Intangibles & R&D Capitalization**
  * *Lecture Content*: Treating R&D as capital expenditure: calculating amortizable R&D assets, adjusting invested capital, and recalculating adjusted ROIC and adjusted Book Value.
* *Sandbox Lab 5: Triangulated Fundamental Valuation Model*
  * *Objective*: Construct a model that simultaneously computes DCF, Greenwald EPV, and the Revised Graham Formula for any S&P 500 company.
  * *Starter Code*:
    ```python
    import quanta as qn

    def triangulate_valuation(ticker: str, year: int, wacc: float = 0.085, long_term_growth: float = 0.03) -> dict:
        fs = qn.data.get_financial_statements(ticker, year)
        bond_yield_aaa = qn.data.get_macro("AAA_BOND_YIELD", year)
        
        # 1. Revised Graham Formula
        eps = fs.diluted_eps
        growth_est = min(0.15, max(0.01, fs.historical_5yr_eps_growth))
        v_graham = (eps * (8.5 + 2 * (growth_est * 100)) * 4.4) / (bond_yield_aaa * 100)
        
        # 2. Greenwald Earnings Power Value (EPV)
        nopat = fs.ebit * (1 - 0.21)
        normalized_nopat = nopat * 0.95  # Conservative normalization haircut
        epv = (normalized_nopat / wacc) + fs.cash - fs.total_debt
        epv_per_share = epv / fs.shares_outstanding
        
        # 3. Two-Stage DCF
        fcf = fs.free_cash_flow
        pv_fcf = sum([fcf * ((1 + growth_est) ** t) / ((1 + wacc) ** t) for t in range(1, 6)])
        terminal_value = (fcf * ((1 + growth_est) ** 5) * (1 + long_term_growth)) / (wacc - long_term_growth)
        pv_tv = terminal_value / ((1 + wacc) ** 5)
        dcf_per_share = (pv_fcf + pv_tv + fs.cash - fs.total_debt) / fs.shares_outstanding
        
        return {
            "graham_fair_value": float(v_graham),
            "greenwald_epv": float(epv_per_share),
            "two_stage_dcf": float(dcf_per_share),
            "consensus_fair_value": float(np.median([v_graham, epv_per_share, dcf_per_share]))
        }
    ```

---

### TRACK 2: MFE-STAT 501 — Mathematical & Statistical Foundations of Finance
*Rigorous mathematical statistics and probability theory for financial engineering, covering CFA Institute Quantitative Investment Analysis (fourth edition) and master's level econometrics.*

#### Chapter 6: Time Value of Money, Discount Factors & Term Structure
* **Section 6.1: Compounding Limits & Instantaneous Discount Factors**
  * *Lecture Content*: Continuous compounding limit: $FV = PV \cdot e^{rt}$. Zero-coupon bond discount factors: $d(t) = \exp\left(-\int_0^t r(s)ds\right)$. Yield-to-maturity (YTM) and reinvestment risk.
* **Section 6.2: Fixed-Income Analytics: Duration, Convexity & Taylor Expansion**
  * *Lecture Content*: MacAulay duration, Modified duration ($D_{\text{mod}} = \frac{D_{\text{mac}}}{1 + y/m}$), and Convexity ($C$). Second-order Taylor series price approximation:
    $$\frac{\Delta P}{P} \approx -D_{\text{mod}} \Delta y + \frac{1}{2} C (\Delta y)^2$$
* **Section 6.3: Term Structure of Interest Rates & Yield Curve Bootstrapping**
  * *Lecture Content*: Spot rates, forward rates ($f(t_1, t_2) = \frac{r_2 t_2 - r_1 t_1}{t_2 - t_1}$), and bootstrapping continuous zero-coupon curves from Treasury coupon issues using cubic splines and Nelson-Siegel parameterization:
    $$y(m) = \beta_0 + \beta_1 \left(\frac{1 - e^{-m/\tau}}{m/\tau}\right) + \beta_2 \left(\frac{1 - e^{-m/\tau}}{m/\tau} - e^{-m/\tau}\right)$$
* *Sandbox Lab 6: Yield Curve Bootstrapper & Duration Immunizer*
  * *Objective*: Ingest on-the-run US Treasury coupon issues and bootstrap the zero-coupon curve, computing modified duration and convexity hedging ratios.
  * *Starter Code*:
    ```python
    import numpy as np
    from scipy.interpolate import CubicSpline

    def bootstrap_yield_curve(maturities: list[float], yields: list[float]) -> dict:
        cs = CubicSpline(maturities, yields, bc_type='natural')
        dense_maturities = np.linspace(0.25, 30.0, 120)
        zero_rates = cs(dense_maturities)
        discount_factors = np.exp(-zero_rates * dense_maturities)
        
        # Calculate duration of 10-year 5% coupon bond
        coupon_times = np.arange(0.5, 10.5, 0.5)
        coupon_payment = 2.5
        bond_cash_flows = np.full(len(coupon_times), coupon_payment)
        bond_cash_flows[-1] += 100.0  # Principal repayment
        
        c_dfs = np.exp(-cs(coupon_times) * coupon_times)
        pv_cash_flows = bond_cash_flows * c_dfs
        bond_price = np.sum(pv_cash_flows)
        
        mac_duration = np.sum(coupon_times * pv_cash_flows) / bond_price
        mod_duration = mac_duration / (1 + cs(10.0)/2)
        convexity = np.sum((coupon_times**2) * pv_cash_flows) / (bond_price * ((1 + cs(10.0)/2)**2))
        
        return {
            "bond_price": float(bond_price),
            "macaulay_duration": float(mac_duration),
            "modified_duration": float(mod_duration),
            "convexity": float(convexity)
        }
    ```

#### Chapter 7: Probability Theory & Financial Asset Distributions
* **Section 7.1: Random Variables, Moments & Probability Density Functions**
  * *Lecture Content*: First through fourth statistical moments: Mean ($\mu$), Variance ($\sigma^2$), Skewness ($S = \mathbb{E}[(X-\mu)^3]/\sigma^3$), and Kurtosis ($K = \mathbb{E}[(X-\mu)^4]/\sigma^4$).
* **Section 7.2: The Leptokurtic Reality of Financial Asset Returns**
  * *Lecture Content*: Empirical failure of the Gaussian random walk hypothesis (Bachelier, Fama 1965). Fat tails, peak excess kurtosis ($K - 3 > 0$), and power-law distribution tails.
* **Section 7.3: Parametric Probability Families in Finance**
  * *Lecture Content*: Normal, Lognormal, Student’s $t$-distribution (degrees of freedom $\nu$), and Generalized Pareto Distribution (GPD).
* **Section 7.4: Extreme Value Theory (EVT) & The Hill Estimator**
  * *Lecture Content*: Block Maxima method (Fisher-Tippett-Gnedenko theorem) and Peaks-Over-Threshold (POT) method. Estimating tail index $\alpha$ via the Hill Estimator:
    $$\hat{\alpha}_{\text{Hill}} = \left( \frac{1}{k} \sum_{i=1}^k \ln X_{(i)} - \ln X_{(k+1)} \right)^{-1}$$
* *Sandbox Lab 7: Non-Gaussian Tail Risk & EVT Modeling Engine*
  * *Objective*: Fit Normal, Student's $t$, and GPD distributions to daily S&P 500 returns from 1990 to present, evaluating empirical 99.9% value-at-risk breaches.
  * *Starter Code*:
    ```python
    import numpy as np
    from scipy import stats

    def evaluate_tail_risk(returns: np.ndarray, alpha_level: float = 0.01) -> dict:
        # Fit distributions
        mu_norm, sig_norm = stats.norm.fit(returns)
        df_t, loc_t, scale_t = stats.t.fit(returns)
        
        # Calculate VaR
        gaussian_var = -stats.norm.ppf(alpha_level, loc=mu_norm, scale=sig_norm)
        student_t_var = -stats.t.ppf(alpha_level, df=df_t, loc=loc_t, scale=scale_t)
        historical_var = -np.percentile(returns, alpha_level * 100)
        
        # Hill tail index estimator on negative losses
        losses = -returns[returns < 0]
        sorted_losses = np.sort(losses)[::-1]
        k = int(0.05 * len(losses))  # Top 5% tail threshold
        hill_alpha = 1.0 / (np.mean(np.log(sorted_losses[:k])) - np.log(sorted_losses[k]))
        
        return {
            "skewness": float(stats.skew(returns)),
            "excess_kurtosis": float(stats.kurtosis(returns)),
            "student_t_df": float(df_t),
            "gaussian_var_99": float(gaussian_var),
            "student_t_var_99": float(student_t_var),
            "historical_var_99": float(historical_var),
            "hill_tail_index": float(hill_alpha)
        }
    ```

#### Chapter 8: Sampling Theory, Estimation & Resampling
* **Section 8.1: Point Estimators & Finite-Sample Properties**
  * *Lecture Content*: Unbiasedness, Efficiency, Consistency, and Sufficiency. Cramér-Rao Lower Bound on estimator variance.
* **Section 8.2: The Central Limit Theorem & Financial Asynchrony**
  * *Lecture Content*: Lindeberg-Lévy CLT, Lyapunov conditions, and Berry-Esseen bounds on convergence rates in non-independent financial samples.
* **Section 8.3: Maximum Likelihood Estimation (MLE) in Financial Modeling**
  * *Lecture Content*: Formulating the log-likelihood function for Student's $t$ returns; numerical maximization via Newton-Raphson and BFGS algorithms.
* **Section 8.4: Non-Parametric Resampling: Bootstrap & Jackknife**
  * *Lecture Content*: Efron’s empirical bootstrap for confidence intervals on non-normal Sharpe ratios; stationary block bootstrap for autocorrelated time series (Politis & Romano).
* *Sandbox Lab 8: Resampling & Bootstrap Confidence Bounds*
  * *Objective*: Implement a block-bootstrap engine in Python to construct 95% confidence intervals for strategy Sharpe, Sortino, and Maximum Drawdown metrics.
  * *Starter Code*:
    ```python
    import numpy as np

    def stationary_block_bootstrap(returns: np.ndarray, avg_block_len: int = 10, n_bootstraps: int = 1000) -> dict:
        n = len(returns)
        p = 1.0 / avg_block_len
        bootstrapped_sharpes = []
        
        for _ in range(n_bootstraps):
            indices = []
            idx = np.random.randint(0, n)
            while len(indices) < n:
                if np.random.rand() < p:
                    idx = np.random.randint(0, n)
                else:
                    idx = (idx + 1) % n
                indices.append(idx)
            
            sample_ret = returns[indices]
            sr = (np.mean(sample_ret) / np.std(sample_ret, ddof=1)) * np.sqrt(252) if np.std(sample_ret) > 0 else 0
            bootstrapped_sharpes.append(sr)
            
        ci_lower = np.percentile(bootstrapped_sharpes, 2.5)
        ci_upper = np.percentile(bootstrapped_sharpes, 97.5)
        
        return {
            "point_estimate_sharpe": float((np.mean(returns)/np.std(returns, ddof=1))*np.sqrt(252)),
            "bootstrap_mean_sharpe": float(np.mean(bootstrapped_sharpes)),
            "ci_95_lower": float(ci_lower),
            "ci_95_upper": float(ci_upper)
        }
    ```

#### Chapter 9: Statistical Hypothesis Testing in Financial Markets
* **Section 9.1: The Neyman-Pearson Decision Framework**
  * *Lecture Content*: Null ($H_0$) vs. Alternative ($H_1$) hypotheses; significance level ($\alpha$), Type I error, Type II error ($\beta$), and test power ($1-\beta$).
* **Section 9.2: Parametric Tests: $t$-Tests and $F$-Tests on Returns**
  * *Lecture Content*: One-sample, two-sample, and paired $t$-tests on excess returns; Welch’s $t$-test for unequal variances; $F$-test for equality of return variances.
* **Section 9.3: Non-Parametric Tests in Quantitative Finance**
  * *Lecture Content*: Wilcoxon signed-rank test, Mann-Whitney $U$ test, and Kruskal-Wallis test for distribution-free performance comparison.
* **Section 9.4: The Data Snooping Crisis & Multiple Testing Corrections**
  * *Lecture Content*: Campbell Harvey, Yan Liu, and Caroline Zhu (2016): "...and the Cross-Section of Expected Returns." Multiple comparison problem; Family-Wise Error Rate (FWER); Bonferroni correction; Benjamini-Hochberg False Discovery Rate (FDR).
* *Sandbox Lab 9: Automated Data Snooping & P-Hacking Audit Suite*
  * *Objective*: Simulate testing candidate trading rules against asset returns, applying Benjamini-Hochberg FDR control to filter false discoveries.
  * *Starter Code*:
    ```python
    import numpy as np

    def benjamini_hochberg_fdr(p_values: list[float], alpha_fdr: float = 0.05) -> dict:
        m = len(p_values)
        sorted_indices = np.argsort(p_values)
        sorted_p = np.array(p_values)[sorted_indices]
        
        # Calculate critical values (k / m) * alpha
        k_values = np.arange(1, m + 1)
        critical_values = (k_values / m) * alpha_fdr
        
        # Find maximum k where p_k <= critical_value
        significant_mask = sorted_p <= critical_values
        if np.any(significant_mask):
            max_k = np.max(np.where(significant_mask)[0])
            rejected_indices = sorted_indices[:max_k + 1].tolist()
        else:
            rejected_indices = []
            
        return {
            "total_hypotheses_tested": m,
            "discoveries_accepted": len(rejected_indices),
            "accepted_indices": rejected_indices,
            "adjusted_p_threshold": float(critical_values[max_k]) if rejected_indices else 0.0
        }
    ```

#### Chapter 10: Simple Linear Regression & Single-Index Models
* **Section 10.1: Ordinary Least Squares (OLS) Derivation & The Gauss-Markov Theorem**
  * *Lecture Content*: Minimizing $\sum e_i^2$; Best Linear Unbiased Estimator (BLUE) properties under Gauss-Markov assumptions.
* **Section 10.2: Goodness of Fit & ANOVA Sum of Squares Decomposition**
  * *Lecture Content*: Decomposing Total Sum of Squares ($\text{TSS} = \text{ESS} + \text{RSS}$); interpreting $R^2$ and standard error of the regression ($s_e$).
* **Section 10.3: The Capital Asset Pricing Model (CAPM) as OLS Regression**
  * *Lecture Content*: Regressing asset excess returns against market excess returns:
    $$R_{it} - R_{ft} = \alpha_i + \beta_i (R_{mt} - R_{ft}) + \epsilon_{it}$$
    *Interpreting Jensen's Alpha ($\alpha$), Market Beta ($\beta$), and Idiosyncratic Risk ($\sigma_\epsilon^2$).*
* **Section 10.4: Hypothesis Testing on Slope & Intercept**
  * *Lecture Content*: $t$-tests on $\beta = 1$ and $\alpha = 0$; constructing confidence bands around the security characteristic line.
* *Sandbox Lab 10: Rolling Alpha & Beta Estimator with Robust Standard Errors*
  * *Objective*: Compute rolling 36-month market betas and Jensen's alphas across the S&P 500 universe with Newey-West HAC standard error bands.
  * *Starter Code*:
    ```python
    import numpy as np
    import statsmodels.api as sm

    def compute_rolling_capm(asset_returns: np.ndarray, market_returns: np.ndarray, window: int = 36) -> dict:
        n = len(asset_returns)
        alphas = []
        betas = []
        t_stats_alpha = []
        
        for i in range(window, n + 1):
            y = asset_returns[i-window:i]
            x = sm.add_constant(market_returns[i-window:i])
            model = sm.OLS(y, x).fit(cov_type='HAC', cov_kwds={'maxlags': 3})
            
            alphas.append(float(model.params[0] * 12))  # Annualized alpha
            betas.append(float(model.params[1]))
            t_stats_alpha.append(float(model.tvalues[0]))
            
        return {
            "latest_beta": betas[-1],
            "latest_annual_alpha": alphas[-1],
            "alpha_significant": abs(t_stats_alpha[-1]) > 2.0,
            "beta_history": betas,
            "alpha_history": alphas
        }
    ```

---

### TRACK 3: MFE-ECON 502 — Advanced Financial Econometrics & Multi-Factor Modeling
*Advanced econometric modeling, non-stationary time series, cointegration, time-varying volatility, and multi-factor portfolio theory (CFA QIA Volume 2 and Booth/Wharton PhD core).*

#### Chapter 11: Multiple Regression & Econometric Diagnostics
* **Section 11.1: Matrix Formulation of Multiple Linear Regression**
  * *Lecture Content*: Deriving OLS in matrix notation:
    $$\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\epsilon}, \quad \hat{\boldsymbol{\beta}} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$$
    *Properties of the projection matrix (Hat matrix $\mathbf{H} = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$) and residual maker matrix ($\mathbf{M} = \mathbf{I} - \mathbf{H}$). Expected value and covariance: $\text{Var}(\hat{\boldsymbol{\beta}}) = \sigma^2 (\mathbf{X}'\mathbf{X})^{-1}$.*
  * *Required Readings*: Greene, *Econometric Analysis* (8th Edition), Chapters 3 & 4; CFA QIA Vol 2, Chapter 1.
* **Section 11.2: Multicollinearity Diagnostics & Regularization**
  * *Lecture Content*: The condition number of $\mathbf{X}'\mathbf{X}$; Variance Inflation Factor:
    $$\text{VIF}_j = \frac{1}{1 - R_j^2}$$
    *When $\text{VIF}_j > 5$, standard errors explode. Remediation via Ridge Regression ($L_2$ penalty: $\hat{\boldsymbol{\beta}}_{\text{Ridge}} = (\mathbf{X}'\mathbf{X} + \lambda \mathbf{I})^{-1}\mathbf{X}'\mathbf{y}$) and Principal Component Regression (PCR).*
* **Section 11.3: Heteroskedasticity in Cross-Sectional Returns**
  * *Lecture Content*: The failure of constant error variance ($\mathbb{E}[\boldsymbol{\epsilon}\boldsymbol{\epsilon}'] = \boldsymbol{\Omega} \ne \sigma^2 \mathbf{I}$). Detection: Breusch-Pagan LM test and White’s general test. Correction: White-Huber Heteroskedasticity-Consistent (HC0 to HC3) standard errors:
    $$\widehat{\text{Var}}_{\text{HC3}}(\hat{\boldsymbol{\beta}}) = (\mathbf{X}'\mathbf{X})^{-1} \left( \sum_{i=1}^n \frac{e_i^2}{(1 - h_{ii})^2} \mathbf{x}_i \mathbf{x}_i' \right) (\mathbf{X}'\mathbf{X})^{-1}$$
* **Section 11.4: Serial Correlation in Factor Residuals**
  * *Lecture Content*: First-order autoregressive errors ($\epsilon_t = \rho \epsilon_{t-1} + u_t$). Detection: Durbin-Watson statistic ($d \approx 2(1 - \hat{\rho})$) and Breusch-Godfrey LM test. Correction: Newey-West Heteroskedasticity and Autocorrelation Consistent (HAC) covariance matrix with Bartlett kernel weights:
    $$w_l = 1 - \frac{l}{L+1}, \quad l = 1, \dots, L$$
* *Sandbox Lab 11: Automated Econometric Diagnostic & Model Repair Pipeline*
  * *Objective*: Build an automated diagnostic engine that tests factor regressions for multicollinearity, heteroskedasticity, and autocorrelation, dynamically applying HC3 or Newey-West corrections.
  * *Starter Code*:
    ```python
    import numpy as np
    import statsmodels.api as sm
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    from statsmodels.stats.diagnostic import het_breuschpagan

    def audit_factor_model(y: np.ndarray, X: np.ndarray, factor_names: list[str]) -> dict:
        X_with_const = sm.add_constant(X)
        model = sm.OLS(y, X_with_const).fit()
        
        # 1. Check Multicollinearity via VIF
        vifs = {factor_names[i]: variance_inflation_factor(X, i) for i in range(X.shape[1])}
        
        # 2. Check Heteroskedasticity via Breusch-Pagan
        bp_stat, bp_pval, _, _ = het_breuschpagan(model.resid, X_with_const)
        
        # 3. Robust correction if heteroskedastic
        if bp_pval < 0.05:
            robust_model = model.get_robustcov_results(cov_type='HC3')
        else:
            robust_model = model
            
        return {
            "vif": vifs,
            "heteroskedastic_pval": bp_pval,
            "params": robust_model.params.tolist(),
            "bse": robust_model.bse.tolist(),
            "tvalues": robust_model.tvalues.tolist()
        }
    ```

#### Chapter 12: Time-Series Econometrics: Stationarity & ARIMA Processes
* **Section 12.1: Covariance Stationarity & Autocovariance Structures**
  * *Lecture Content*: Conditions for weak stationarity: constant mean $\mathbb{E}[y_t] = \mu$, constant finite variance $\text{Var}(y_t) = \gamma_0 < \infty$, and autocovariance $\text{Cov}(y_t, y_{t-k}) = \gamma_k$ dependent solely on lag $k$. The Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF).
* **Section 12.2: Autoregressive Moving Average ($\text{ARMA}(p, q)$) Formulations**
  * *Lecture Content*:
    $$y_t = c + \sum_{i=1}^p \phi_i y_{t-i} + \epsilon_t + \sum_{j=1}^q \theta_j \epsilon_{t-j}$$
    *Lag operator notation: $\Phi(L)y_t = c + \Theta(L)\epsilon_t$. Invertibility and stationarity roots outside the complex unit circle. Model identification via AIC and BIC.*
* **Section 12.3: Unit Roots & Integrated Processes**
  * *Lecture Content*: The random walk with drift: $y_t = \mu + y_{t-1} + \epsilon_t$. Spurious regression problem in non-stationary series (Granger & Newbold 1974). Testing for unit roots: Dickey-Fuller, Augmented Dickey-Fuller (ADF) with trend specifications, and Phillips-Perron (PP) tests.
* **Section 12.4: Fractional Differentiation for Memory Preservation (López de Prado)**
  * *Lecture Content*: The fundamental dilemma of quantitative finance: Integer differencing ($d=1$) removes non-stationarity but obliterates all long-term price memory, while raw prices ($d=0$) retain memory but violate stationarity assumptions. Expanding $(1 - L)^d$ via binomial series:
    $$(1 - L)^d = \sum_{k=0}^\infty (-1)^k \binom{d}{k} L^k = 1 - d L + \frac{d(d-1)}{2!} L^2 - \frac{d(d-1)(d-2)}{3!} L^3 + \dots$$
    *Finding the minimum real degree $d^* \in (0, 1)$ such that the resulting series passes the ADF test ($p < 0.01$) while retaining maximal correlation with the original price series.*
* *Sandbox Lab 12: Marcos López de Prado Fractional Differentiation Engine*
  * *Objective*: Implement the expanding window fractional differentiation algorithm to determine optimal memory-preserving stationary features for asset prices.
  * *Starter Code*:
    ```python
    import numpy as np
    import pandas as pd
    from statsmodels.tsa.stattools import adfuller

    def get_fractional_weights(d: float, size: int) -> np.ndarray:
        w = [1.0]
        for k in range(1, size):
            w.append(-w[-1] / k * (d - k + 1))
        return np.array(w[::-1])

    def fractional_differentiation(series: pd.Series, d: float, thres: float = 1e-4) -> pd.Series:
        weights = get_fractional_weights(d, len(series))
        # Drop weights below threshold to avoid infinite memory window
        weights = weights[np.abs(weights) > thres]
        res = series.rolling(window=len(weights)).apply(lambda x: np.dot(x, weights), raw=True)
        return res.dropna()
    ```

#### Chapter 13: Cointegration, Vector Autoregressions (VAR) & Pairs Trading
* **Section 13.1: Spurious Correlation vs. Genuine Cointegration**
  * *Lecture Content*: Granger Representation Theorem. Two non-stationary $I(1)$ time series $x_t$ and $y_t$ are cointegrated of order $\text{CI}(1, 1)$ if there exists a linear combination $z_t = y_t - \beta x_t$ that is stationary $I(0)$.
* **Section 13.2: The Engle-Granger Two-Step Methodology**
  * *Lecture Content*: Step 1: Run cointegrating regression $y_t = \alpha + \beta x_t + \epsilon_t$. Step 2: Perform ADF test on residuals $\hat{\epsilon}_t$ using MacKinnon critical values.
* **Section 13.3: The Johansen Cointegration Test & Vector Error Correction (VECM)**
  * *Lecture Content*: Modeling cointegrating vectors in multi-asset baskets:
    $$\Delta \mathbf{y}_t = \boldsymbol{\Pi} \mathbf{y}_{t-1} + \sum_{i=1}^{p-1} \boldsymbol{\Gamma}_i \Delta \mathbf{y}_{t-i} + \boldsymbol{\epsilon}_t$$
    *Rank of $\boldsymbol{\Pi} = \boldsymbol{\alpha}\boldsymbol{\beta}'$. Trace test ($\lambda_{\text{trace}}$) and Maximum Eigenvalue test ($\lambda_{\max}$).*
* **Section 13.4: The Continuous-Time Ornstein-Uhlenbeck (OU) Mean-Reverting Process**
  * *Lecture Content*: Modeling the spread $x_t$:
    $$dx_t = \theta(\mu - x_t)dt + \sigma dW_t$$
    *Derivation of conditional expectation $\mathbb{E}[x_t \mid x_0] = \mu + (x_0 - \mu)e^{-\theta t}$, conditional variance $\text{Var}(x_t \mid x_0) = \frac{\sigma^2}{2\theta}(1 - e^{-2\theta t})$, and spread half-life: $\tau = \frac{\ln 2}{\theta}$.*
* **Section 13.5: Dynamic Hedge Ratio Tracking with the Kalman Filter**
  * *Lecture Content*: Formulating the time-varying cointegration problem as a state-space model:
    * State equation: $\boldsymbol{\beta}_t = \boldsymbol{\beta}_{t-1} + \mathbf{w}_t, \quad \mathbf{w}_t \sim \mathcal{N}(0, \mathbf{Q})$
    * Measurement equation: $y_t = \mathbf{x}_t' \boldsymbol{\beta}_t + v_t, \quad v_t \sim \mathcal{N}(0, R)$
    * Recursive Kalman update cycle: State prediction $\rightarrow$ Measurement innovation $\rightarrow$ Kalman gain $\mathbf{K}_t$ computation $\rightarrow$ State covariance update.
* *Sandbox Lab 13: Kalman Filter Dynamic Pairs Trading Engine*
  * *Objective*: Build an online Kalman Filter that continuously updates hedge ratios and trades the cointegrated spread between energy sector ETF pairs (e.g. XLE vs. CVX/XOM).
  * *Starter Code*:
    ```python
    import numpy as np

    class KalmanPairsTrader:
        def __init__(self, delta: float = 1e-4, vt: float = 1e-3):
            # State vector: [beta, alpha]^T
            self.theta = np.zeros(2)
            self.P = np.eye(2) * 1.0
            self.R = vt
            self.Q = delta / (1 - delta) * np.eye(2)

        def update(self, x_price: float, y_price: float) -> tuple[float, float]:
            """
            Online update step for new price pair (x_t, y_t).
            Returns (hedge_ratio_beta, spread_error).
            """
            F = np.array([x_price, 1.0])
            
            # Predict step
            P_pred = self.P + self.Q
            
            # Measurement innovation
            y_hat = np.dot(F, self.theta)
            e = y_price - y_hat
            Q_meas = np.dot(F, np.dot(P_pred, F)) + self.R
            
            # Kalman gain update
            K = np.dot(P_pred, F) / Q_meas
            self.theta = self.theta + K * e
            self.P = P_pred - np.outer(K, np.dot(F, P_pred))
            
            beta = float(self.theta[0])
            return beta, float(e)
    ```

#### Chapter 14: Volatility Modeling: ARCH, GARCH & Asymmetric Volatility
* **Section 14.1: Volatility Clustering & Stylized Empirical Facts**
  * *Lecture Content*: Mandelbrot's phenomenon; autocorrelation of squared returns vs. zero autocorrelation of raw returns; time-varying conditional heteroskedasticity.
* **Section 14.2: Engle’s $\text{ARCH}(q)$ Formulation**
  * *Lecture Content*: Robert Engle (1982, Nobel Prize 2003):
    $$r_t = \mu + \epsilon_t, \quad \epsilon_t = \sigma_t z_t, \quad z_t \sim \text{i.i.d. } \mathcal{N}(0, 1)$$
    $$\sigma_t^2 = \alpha_0 + \sum_{i=1}^q \alpha_i \epsilon_{t-i}^2 \quad (\alpha_0 > 0, \alpha_i \ge 0)$$
* **Section 14.3: Bollerslev’s Generalized ARCH ($\text{GARCH}(p, q)$)**
  * *Lecture Content*: Tim Bollerslev (1986):
    $$\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$$
    *Condition for covariance stationarity: $\alpha + \beta < 1$. Unconditional long-run variance: $\sigma_L^2 = \frac{\omega}{1 - \alpha - \beta}$. Multi-step volatility forecasting cones: $\mathbb{E}[\sigma_{t+k}^2 \mid \mathcal{F}_t] = \sigma_L^2 + (\alpha + \beta)^k (\sigma_t^2 - \sigma_L^2).*
* **Section 14.4: Asymmetric Volatility Models: GJR-GARCH & EGARCH**
  * *Lecture Content*: The Leverage Effect (Black 1976). Glosten, Jagannathan, and Runkle (1993) GJR-GARCH:
    $$\sigma_t^2 = \omega + (\alpha + \gamma \mathbb{I}_{\{\epsilon_{t-1} < 0\}}) \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$$
    *Nelson (1991) Exponential GARCH ($\text{EGARCH}$) modeling $\ln(\sigma_t^2)$ to ensure strictly positive variance without parameter constraints.*
* *Sandbox Lab 14: GARCH(1,1) Volatility Forecasting & Dynamic Value-at-Risk Engine*
  * *Objective*: Fit GARCH(1,1) and GJR-GARCH via Maximum Likelihood Estimation on historical S&P 500 returns; construct forward 30-day volatility cones and dynamic 99% VaR thresholds.
  * *Starter Code*:
    ```python
    import numpy as np
    from scipy.optimize import minimize

    def fit_garch11(returns: np.ndarray) -> dict:
        r = returns - np.mean(returns)
        var_sample = np.var(r)
        
        def garch_log_likelihood(params):
            omega, alpha, beta = params
            if omega <= 0 or alpha < 0 or beta < 0 or (alpha + beta) >= 1.0:
                return 1e10
            
            n = len(r)
            sigma2 = np.zeros(n)
            sigma2[0] = var_sample
            for t in range(1, n):
                sigma2[t] = omega + alpha * (r[t-1]**2) + beta * sigma2[t-1]
                
            ll = -0.5 * np.sum(np.log(2 * np.pi) + np.log(sigma2) + (r**2) / sigma2)
            return -ll  # Negative log-likelihood
            
        res = minimize(garch_log_likelihood, [var_sample * 0.05, 0.05, 0.90], method='L-BFGS-B',
                       bounds=[(1e-6, None), (0, 0.5), (0, 0.99)])
        
        omega, alpha, beta = res.x
        long_run_vol = np.sqrt(omega / (1 - alpha - beta) * 252)
        
        return {
            "omega": float(omega),
            "alpha": float(alpha),
            "beta": float(beta),
            "persistence": float(alpha + beta),
            "annualized_long_run_vol": float(long_run_vol)
        }
    ```

#### Chapter 15: Modern Portfolio Theory, Shrinkage & Asset Pricing Factor Models
* **Section 15.1: Markowitz Mean-Variance Optimization & Matrix Derivation**
  * *Lecture Content*: Minimizing portfolio variance subject to target expected return:
    $$\min_{\mathbf{w}} \mathbf{w}'\boldsymbol{\Sigma}\mathbf{w} \quad \text{s.t.} \quad \mathbf{w}'\boldsymbol{\mu} = \mu_{\text{target}}, \quad \mathbf{w}'\mathbf{1} = 1$$
    *Analytical solution via Lagrange multipliers; deriving the Efficient Frontier, Global Minimum Variance (GMV) portfolio, and Tangency Portfolio.*
* **Section 15.2: The "Error-Maximizer" Dilemma & Ledoit-Wolf Covariance Shrinkage**
  * *Lecture Content*: Richard Michaud (1989): "Markowitz optimization is an error-maximizer." Small estimation errors in $\boldsymbol{\mu}$ and $\boldsymbol{\Sigma}$ produce extreme, unstable weights. Olivier Ledoit and Michael Wolf (2004) optimal shrinkage estimator:
    $$\boldsymbol{\Sigma}_{\text{shrink}} = \delta^* \mathbf{F} + (1 - \delta^*) \mathbf{S}$$
    *(where $\mathbf{S}$ is the sample covariance matrix, $\mathbf{F}$ is the single-factor or constant-correlation target, and $\delta^* \in [0, 1]$ is the asymptotically optimal shrinkage intensity).*
* **Section 15.3: Risk Parity & Equal Risk Contribution (ERC) Portfolios**
  * *Lecture Content*: Qian (2005), Maillard, Roncalli & Teïletche (2010): Decomposing total portfolio volatility into asset risk contributions:
    $$\sigma_p = \sum_{i=1}^N w_i \frac{(\boldsymbol{\Sigma}\mathbf{w})_i}{\sigma_p}$$
    *Equal Risk Contribution condition: $w_i (\boldsymbol{\Sigma}\mathbf{w})_i = w_j (\boldsymbol{\Sigma}\mathbf{w})_j = \frac{1}{N}\sigma_p^2$ for all $i, j$. Numerical optimization using sequential quadratic programming (SQP).*
* **Section 15.4: The Fama-French 3-Factor & Carhart 4-Factor Models**
  * *Lecture Content*: Eugene Fama & Kenneth French (1992, 1993): Small-Minus-Big (SMB) and High-Minus-Low (HML). Mark Carhart (1997): Adding Up-Minus-Down (UMD) Momentum:
    $$R_{it} - R_{ft} = \alpha_i + \beta_{i1}(R_{mt} - R_{ft}) + \beta_{i2}\text{SMB}_t + \beta_{i3}\text{HML}_t + \beta_{i4}\text{UMD}_t + \epsilon_{it}$$
* **Section 15.5: The Fama-French 5-Factor Model & Factor Zoo Hygiene**
  * *Lecture Content*: Fama & French (2015): Adding Robust-Minus-Weak (RMW) profitability and Conservative-Minus-Aggressive (CMA) investment. The Fama-MacBeth (1973) two-pass cross-sectional regression methodology:
    * Pass 1: Time-series regressions to estimate factor loadings $\beta_{ij}$.
    * Pass 2: Cross-sectional regressions at each period $t$ to estimate factor risk premiums $\lambda_{jt}$.
* *Sandbox Lab 15: Institutional Fama-French 5-Factor Attribution & Risk Parity Engine*
  * *Objective*: Decompose an equity portfolio’s return history into 5 Fama-French factor exposures vs. genuine manager alpha, then construct an Equal Risk Contribution (ERC) multi-asset portfolio.
  * *Starter Code*:
    ```python
    import numpy as np
    from scipy.optimize import minimize

    def equal_risk_contribution_portfolio(cov_matrix: np.ndarray) -> np.ndarray:
        n = cov_matrix.shape[0]
        
        def risk_budget_objective(w):
            w = np.array(w)
            port_vol = np.sqrt(np.dot(w, np.dot(cov_matrix, w)))
            marginal_risk = np.dot(cov_matrix, w) / port_vol
            risk_contrib = w * marginal_risk
            # Minimize variance of risk contributions
            target_risk = port_vol / n
            return np.sum((risk_contrib - target_risk)**2)
            
        w0 = np.full(n, 1.0 / n)
        bounds = [(0.01, 1.0) for _ in range(n)]
        constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}]
        
        res = minimize(risk_budget_objective, w0, method='SLSQP', bounds=bounds, constraints=constraints)
        return res.x
    ```

#### Chapter 16: Downside Risk Management & Algorithmic Hygiene
* **Section 16.1: Value-at-Risk (VaR): Parametric, Historical & Monte Carlo**
  * *Lecture Content*:
    $$\text{VaR}_\alpha = -\inf \{ l \in \mathbb{R} : P(L > l) \le 1 - \alpha \}$$
    *Parametric Normal VaR: $\text{VaR}_\alpha = -(\mu + z_{1-\alpha}\sigma)W$. Historical simulation method; Monte Carlo VaR with Cholesky factorized correlated returns.*
* **Section 16.2: Conditional Value-at-Risk (CVaR / Expected Shortfall)**
  * *Lecture Content*: Artzner, Delbaen, Eber & Heath (1999): "Coherent Measures of Risk." Proof that VaR fails the subadditivity axiom ($\rho(X + Y) \le \rho(X) + \rho(Y)$), while CVaR is strictly coherent:
    $$\text{CVaR}_\alpha = -\frac{1}{1 - \alpha} \int_0^{1-\alpha} \text{VaR}_u du = -\mathbb{E}[R \mid R \le -\text{VaR}_\alpha]$$
* **Section 16.3: Drawdown Analytics & Path-Dependent Risk Metrics**
  * *Lecture Content*: High-water mark process $M_t = \max_{0 \le s \le t} W_s$; drawdown process $D_t = \frac{M_t - W_t}{M_t}$. Maximum Drawdown (MDD); Calmar Ratio ($\text{CAGR} / |\text{MDD}|$); Sterling Ratio; Ulcer Performance Index (UPI).
* **Section 16.4: The Deflated Sharpe Ratio (DSR) & Probabilistic Sharpe Ratio (PSR)**
  * *Lecture Content*: Marcos López de Prado and David Bailey (2014): Correcting the Sharpe ratio for skewness, kurtosis, sample length, and the selection bias of multiple backtest trials ($K$):
    $$\text{DSR} = \Phi\left( \frac{(\hat{\text{SR}} - \text{SR}^*) \sqrt{T-1}}{\sqrt{1 - \hat{\gamma}_3 \hat{\text{SR}} + \frac{\hat{\gamma}_4 - 1}{4}\hat{\text{SR}}^2}} \right)$$
    *(where $\text{SR}^* = \sqrt{\text{Var}(\{\hat{\text{SR}}_k\})} \left( (1-\gamma) \Phi^{-1}\left(1 - \frac{1}{K}\right) + \gamma \Phi^{-1}\left(1 - \frac{1}{Ke}\right) \right)$).*
* *Sandbox Lab 16: The Quant Backtest Auditor (DSR & MinTRL Suite)*
  * *Objective*: Build an audit module that accepts a strategy return series and trial count $K$, computing the Probabilistic Sharpe Ratio (PSR), Deflated Sharpe Ratio (DSR), and Minimum Track Record Length (MinTRL).
  * *Starter Code*:
    ```python
    import numpy as np
    from scipy import stats

    def calculate_dsr(sharpe_observed: float, n_trials: int, variance_trials: float, t_periods: int, skew: float = 0.0, kurt: float = 3.0) -> dict:
        # Expected maximum Sharpe under null hypothesis of no alpha across K trials
        euler_mascheroni = 0.5772156649
        z_k = (1 - euler_mascheroni) * stats.norm.ppf(1 - 1/n_trials) + euler_mascheroni * stats.norm.ppf(1 - 1/(n_trials * np.e))
        expected_max_sr = np.sqrt(variance_trials) * z_k
        
        # Standard error of Sharpe ratio
        sr_std_err = np.sqrt((1 - skew * sharpe_observed + (kurt - 1) / 4 * (sharpe_observed**2)) / (t_periods - 1))
        
        # Deflated Sharpe Ratio (DSR)
        z_stat = (sharpe_observed - expected_max_sr) / sr_std_err
        dsr_pvalue = stats.norm.cdf(z_stat)
        
        # Minimum Track Record Length (MinTRL)
        min_trl = 1 + (1 - skew * sharpe_observed + (kurt - 1) / 4 * (sharpe_observed**2)) * ((stats.norm.ppf(0.95) / (sharpe_observed - expected_max_sr))**2)
        
        return {
            "expected_max_null_sr": float(expected_max_sr),
            "deflated_sharpe_ratio": float(dsr_pvalue),
            "is_statistically_significant": dsr_pvalue > 0.95,
            "min_track_record_length_periods": float(min_trl) if sharpe_observed > expected_max_sr else float('inf')
        }
    ```

---

### TRACK 4: MFE-LAB 601 — The Quantitative Strategy Lab
*Empirical synthesis connecting Graham-Dodd fundamental criteria with CFA quantitative factor modeling across historical and synthetic datasets.*

#### Chapter 17: Systematic Fundamental Value Strategies
* **Section 17.1: The 30-Year Systematic Net-Net Backtest**
  * *Lecture Content*: Replicating Benjamin Graham’s classic deep-value NCAV screen across 30 years of cleaned point-in-time SEC Compustat data. Incorporating delisted and bankrupt companies to eliminate survivorship bias; analyzing performance during liquidity freezes (1998, 2008).
* **Section 17.2: The Piotroski 9-Point F-Score Engine**
  * *Lecture Content*: Joseph Piotroski (2000): Using fundamental financial statement ratios to separate winners from value traps among high book-to-market equities:
    * Profitability: Positive Net Income (1), Positive Operating Cash Flow (1), $\Delta\text{ROA} > 0$ (1), $\text{CFO} > \text{Net Income}$ (accrual check) (1).
    * Leverage & Liquidity: $\Delta\text{Long-Term Debt} < 0$ (1), $\Delta\text{Current Ratio} > 0$ (1), No equity dilution (1).
    * Operating Efficiency: $\Delta\text{Gross Margin} > 0$ (1), $\Delta\text{Asset Turnover} > 0$ (1).
* **Section 17.3: Joel Greenblatt’s Magic Formula & QARP Portfolios**
  * *Lecture Content*: Joel Greenblatt (2005): Cross-sectional ranking by Earnings Yield ($\text{EBIT} / \text{Enterprise Value}$) + Return on Capital ($\text{EBIT} / (\text{Net Fixed Assets} + \text{Net Working Capital})$). Analyzing factor cyclicality and multi-year tracking error vs. benchmark indices.
* *Sandbox Lab 17: Comprehensive Systematic Value Portfolio Backtester*
  * *Objective*: Backtest an automated quarterly rebalanced portfolio combining Graham's NCAV discount with Piotroski's F-Score ($F \ge 7$) from 1995 to present, incorporating realistic slippage and transaction costs.
  * *Starter Code*:
    ```python
    import quanta as qn
    import pandas as pd

    def backtest_systematic_ncav_fscore(start_year: int = 1995, end_year: int = 2023) -> pd.DataFrame:
        portfolio_records = []
        for year in range(start_year, end_year):
            candidates = qn.data.get_screener_universe(year)
            qualified = []
            
            for stock in candidates:
                fs = qn.data.get_point_in_time_fs(stock, f"{year}-03-31")
                ncav = fs.current_assets - fs.total_liabilities - fs.preferred_stock
                mkt_cap = qn.data.get_market_cap(stock, f"{year}-03-31")
                
                # Graham 2/3 NCAV condition + Piotroski F-score check
                if mkt_cap < (2/3) * ncav and fs.piotroski_f_score >= 7:
                    qualified.append(stock)
                    
            # Equally weighted annual rebalancing
            returns = qn.backtest.simulate_equal_weight_rebalance(qualified, f"{year}-04-01", f"{year+1}-03-31")
            portfolio_records.append({"year": year, "num_stocks": len(qualified), "annual_return": returns})
            
        return pd.DataFrame(portfolio_records)
    ```

#### Chapter 18: Cross-Sectional Factor Investing & Anomaly Exploitation
* **Section 18.1: Cross-Sectional Momentum & Momentum Crashes**
  * *Lecture Content*: Jegadeesh & Titman (1993): 12-minus-1 month lookback momentum. Kent Daniel & Tobias Moskowitz (2016): "Momentum Crashes." Why long-short momentum portfolios suffer catastrophic drawdowns during market rebounds due to short positions in distressed, high-beta options.
* **Section 18.2: The Low-Beta / Low-Volatility Anomaly**
  * *Lecture Content*: Andrea Frazzini & Lasse Pedersen (2014): "Betting Against Beta." Leverage-constrained investors bid up high-beta stocks, creating flat security market lines. Constructing zero-beta, leveraged long low-beta, short high-beta portfolios.
* **Section 18.3: Factor Neutralization, Outlier Winsorization & Information Coefficients (IC)**
  * *Lecture Content*: Factor engineering pipeline: Cross-sectional winsorization (3 standard deviations or 1st/99th percentiles); industry/sector neutralization via OLS dummy regression residuals; calculating Rank Information Coefficient (Spearman Rank Correlation between factor score at $t$ and forward return at $t+1$).
* *Sandbox Lab 18: Multi-Factor Equity Ranking & Neutralization Engine*
  * *Objective*: Build a production multi-factor pipeline (Value + Quality + Momentum), perform sector neutralization and winsorization, and compute rolling 12-month Information Coefficients (IC) and Information Ratios (IR).
  * *Starter Code*:
    ```python
    import numpy as np
    import pandas as pd
    import statsmodels.api as sm
    from scipy.stats import spearmanr

    def neutralize_and_rank_factors(raw_scores: pd.Series, sector_series: pd.Series) -> pd.Series:
        # 1. Winsorize at 3 sigma
        mu, std = raw_scores.mean(), raw_scores.std()
        winsorized = raw_scores.clip(lower=mu - 3*std, upper=mu + 3*std)
        
        # 2. Sector neutralization via regression residuals on sector dummies
        sector_dummies = pd.get_dummies(sector_series, drop_first=True, dtype=float)
        X = sm.add_constant(sector_dummies)
        model = sm.OLS(winsorized, X).fit()
        neutralized_residuals = model.resid
        
        # 3. Standardize to z-score
        z_scores = (neutralized_residuals - neutralized_residuals.mean()) / neutralized_residuals.std()
        return z_scores
    ```

### TRACK 5: MFE-ENG 701 — Algorithmic Execution Systems & Autonomous AI Stock Bots
*Production-grade engineering for automated trading systems, limit order book microstructure, optimal execution, machine learning alpha generators, and autonomous LLM forensic agents.*

#### Implemented applied course requirements — September 2026

The local learning release expands Track 5 to **32 original lessons in eight units**, 64 practice items, seven four-question checkpoints, and a 32-question version-2 final. Units cover specification/data/events, trading rules and evaluation, execution/accounting, risk, ML, LLM research, operations, and projects. Existing lesson IDs 5.1–5.5 and first-answer keys remain compatible; old final attempts remain historical and do not satisfy the expanded final.

Each lesson requires a concrete objective, substantive original explanation, worked case, rendered equation, executable guided worksheet, two practice questions, a notebook assignment with worked solution, and named primary references. Course pages expose unit navigation and downloadable project resources. The code and written dossier are self-assessed separately from the concept exam.

The downloadable standard-library project must actually run local SQLite order/fill accounting with integer-cent fees, bounded volume, partial fills, immutable identities, transactions, restart recovery, reservations, pre-trade gates, and a persistent new-risk halt. It also fits two chronological ridge folds on artificial data and tests structured AI response fixtures against fictional evidence. It makes no broker or AI-provider calls. Its synchronous matcher and immediate-settlement assumptions must be visible. The wider provider, asynchronous Redis, boosted-tree, and live-operation labs below remain extension requirements, not claims about this offline project.

Content must distinguish architecture from timing correctness, fitted constraints from economic laws, valid schemas from factual truth, and paper acceptance from live readiness. All pages require source attribution and links to source-use guidance; book explanations, examples, illustrations, and assignments should remain original. Attribution does not replace any license or permission needed for reused third-party material. See [course implementation and acceptance](docs/STOCK_BOTS_COURSE.md).

#### Chapter 19: High-Performance Trading Bot Architecture
* **Section 19.1: System Topologies: Vectorized Backtesters vs. Event-Driven Low-Latency Engines**
  * *Lecture Content*: Analysis of computational paradigms: How both vectorized and event-driven engines can introduce look-ahead when timestamps are wrong. Compare explicit models for execution latency, partial fills, queue priority, and event loops; neither architecture automatically guarantees timing correctness.
  * *Architecture Pattern*: State machine event loop:
    $$\text{Tick / Bar Event} \longrightarrow \text{Order Book / State Store} \longrightarrow \text{Alpha Generator} \longrightarrow \text{Risk / Position Sizer} \longrightarrow \text{OMS / Router} \longrightarrow \text{Broker Fill Event}$$
* **Section 19.2: Asynchronous Concurrency & Message Queues**
  * *Lecture Content*: Python `asyncio` non-blocking event loops; integrating Redis Streams and Pub/Sub for high-throughput tick data ingestion; decoupling strategy generation threads from execution routing threads to eliminate blocking I/O.
* **Section 19.3: Order Management System (OMS) & Execution Management System (EMS)**
  * *Lecture Content*: Explicit finite state machine modeling order lifecycles:
    $$\text{NEW} \longrightarrow \text{SUBMITTED} \longrightarrow \left[ \text{PARTIALLY\_FILLED} \longrightarrow \right] \text{FILLED} \quad \text{or} \quad \text{REJECTED} / \text{CANCELED}$$
    *Position reconciliation protocols, synthetic order management (Stop-Loss and Take-Profit brackets executed locally to avoid exchange order book information leakage).*
* *Sandbox Lab 19: Event-Driven Trading Bot Kernel with Redis State Persistence*
  * *Objective*: Build an asynchronous event-driven Python trading bot that consumes market bars, maintains position state in Redis, and handles failover recovery without duplicating orders.
  * *Starter Code*:
    ```python
    import asyncio
    import json
    from dataclasses import dataclass
    from enum import Enum

    class OrderState(Enum):
        PENDING = "PENDING"
        SUBMITTED = "SUBMITTED"
        FILLED = "FILLED"
        CANCELED = "CANCELED"

    @dataclass
    class Order:
        order_id: str
        symbol: str
        side: str
        quantity: float
        limit_price: float
        state: OrderState = OrderState.PENDING

    class EventDrivenBotCore:
        def __init__(self, broker_client):
            self.broker = broker_client
            self.active_orders: dict[str, Order] = {}
            self.positions: dict[str, float] = {}

        async def on_bar_event(self, bar: dict):
            # 1. Evaluate alpha signal
            signal = self.evaluate_signal(bar)
            if signal != 0:
                await self.rebalance_position(bar['symbol'], target_side="BUY" if signal > 0 else "SELL", price=bar['close'])

        async def rebalance_position(self, symbol: str, target_side: str, price: float):
            order = Order(order_id=f"ord_{symbol}_{asyncio.get_event_loop().time()}", symbol=symbol, side=target_side, quantity=100.0, limit_price=price)
            self.active_orders[order.order_id] = order
            # Submit non-blocking order to broker
            fill = await self.broker.submit_order(order)
            if fill['status'] == 'FILLED':
                order.state = OrderState.FILLED
                self.positions[symbol] = self.positions.get(symbol, 0.0) + (100.0 if target_side == "BUY" else -100.0)
    ```

#### Chapter 20: Market Microstructure & Optimal Execution
* **Section 20.1: Limit Order Books (LOB Level 1/2/3) & Order Mechanics**
  * *Lecture Content*: Order book dynamics: price priority, time priority (FIFO queueing), maker-taker fee models, iceberg orders, pegged orders, and fill probability under varying queue depths.
* **Section 20.2: Transaction Cost Analysis (TCA) & Market Impact Modeling**
  * *Lecture Content*: Decomposing total execution cost: Explicit costs (brokerage, exchange, regulatory fees) + Implicit costs (half-spread, price impact, delay/opportunity cost).
  * *The Square-Root Law of Market Impact*: Empirical foundation (Bouchaud 2008, Kyle 1985):
    $$I = Y \cdot \sigma \cdot \sqrt{\frac{Q}{V}}$$
    *(where $Q$ is order size, $V$ is average daily volume, $\sigma$ is daily volatility, and $Y \approx 0.5 - 0.7$).*
* **Section 20.3: Execution Trajectories: TWAP, VWAP & The Almgren-Chriss Model**
  * *Lecture Content*: Robert Almgren & Neil Chriss (2000): "Optimal Execution of Portfolio Transactions." Formulating the liquidation problem as an optimal control problem:
    $$\min_{x} \mathbb{E}[x] + \lambda \text{Var}(x)$$
    *Trading off temporary and permanent market impact against volatility risk over discrete intervals $t = 1, \dots, N$. Analytical hyperbolic trajectory solution.*
* *Sandbox Lab 20: Almgren-Chriss Optimal Liquidation Trajectory Simulator*
  * *Objective*: Implement the Almgren-Chriss optimal execution algorithm to liquidate 100,000 shares of stock under varying risk-aversion parameters ($\lambda$), comparing realized slippage against standard TWAP and VWAP baselines.
  * *Starter Code*:
    ```python
    import numpy as np

    def almgren_chriss_trajectory(total_shares: float, n_steps: int, sigma: float, gamma: float, eta: float, lambda_risk: float) -> np.ndarray:
        """
        sigma: daily volatility
        gamma: permanent market impact coefficient
        eta: temporary market impact coefficient
        lambda_risk: trader risk aversion
        """
        tau = 1.0  # Normalized time step
        # Calculate kappa (urgency parameter)
        kappa = np.arccosh(0.5 * (lambda_risk * (sigma**2) * (tau**2) / eta) + 1) / tau
        
        # Calculate optimal inventory holding at each step t
        t = np.arange(n_steps + 1)
        inventory = total_shares * np.sinh(kappa * (n_steps - t)) / np.sinh(kappa * n_steps)
        trade_sizes = -np.diff(inventory)
        return trade_sizes
    ```

#### Chapter 21: Machine Learning & Deep Tabular Learning for Alpha
* **Section 21.1: Financial Feature Engineering & Stationarity Transforms**
  * *Lecture Content*: Constructing candidate features from price/volume series and testing their stability; transformations do not automatically establish stationarity. Examples include rolling normalized $z$-scores, fractional differences, volatility-adjusted momentum, volume-weighted spread indicators, and fundamental accrual metrics.
* **Section 21.2: Gradient-Boosted Decision Trees (XGBoost / LightGBM) with Domain Constraints**
  * *Lecture Content*: Handling heterogeneous tabular financial data with tree ensembles. Evaluating optional monotonic constraints as testable model priors, such as a proposed nondecreasing relationship with a defined quality score. These constraints do not establish causality or a universal financial law; compare unconstrained and constrained models on valid development folds.
* **Section 21.3: Purged & Embargoed K-Fold Cross-Validation**
  * *Lecture Content*: Marcos López de Prado (2018): Why standard randomized $k$-fold cross-validation results in massive data leakage in financial time series due to overlapping label windows and serial correlation.
  * *Purging*: Removing training samples whose evaluation labels overlap with the test set.
  * *Embargoing*: Removing training samples immediately following the test set to eliminate autoregressive memory leakage.
* *Sandbox Lab 21: Walk-Forward Purged K-Fold XGBoost Stock Ranker*
  * *Objective*: Train an XGBoost model on fundamental and quantitative features using Purged K-Fold cross-validation, measuring out-of-sample Information Coefficients (IC) and Sharpe ratios.
  * *Starter Code*:
    ```python
    import numpy as np
    import pandas as pd
    import xgboost as xgb
    from scipy.stats import spearmanr

    # Partition sketch only: this does NOT purge overlapping label intervals or enforce
    # past-only training. A deployable splitter must accept label start/end times,
    # filter unavailable labels, and preserve chronological evaluation manifests.
    def embargoed_partition_sketch(n_samples: int, n_splits: int = 5, embargo_pct: float = 0.02) -> list[tuple[np.ndarray, np.ndarray]]:
        indices = np.arange(n_samples)
        fold_size = n_samples // n_splits
        embargo = int(n_samples * embargo_pct)
        splits = []
        
        for i in range(n_splits):
            test_start = i * fold_size
            test_end = (i + 1) * fold_size if i != n_splits - 1 else n_samples
            test_idx = indices[test_start:test_end]
            
            # Train indices excluding test set + post-test embargo period
            train_idx = np.setdiff1d(indices, indices[max(0, test_start):min(n_samples, test_end + embargo)])
            splits.append((train_idx, test_idx))
            
        return splits

    def train_xgboost_alpha_model(X: pd.DataFrame, y: pd.Series) -> dict:
        splits = embargoed_partition_sketch(len(X), n_splits=5)  # incomplete teaching sketch
        oos_predictions = np.zeros(len(X))
        
        for train_idx, test_idx in splits:
            dtrain = xgb.DMatrix(X.iloc[train_idx], label=y.iloc[train_idx])
            dtest = xgb.DMatrix(X.iloc[test_idx])
            
            # Monotonic constraint: 1 enforces positive correlation with target
            params = {
                'objective': 'reg:squarederror',
                'max_depth': 4,
                'learning_rate': 0.05,
                'monotone_constraints': '(1, 1, -1, 1)'  # (EarningsYield, Momentum, Volatility, ROIC)
            }
            bst = xgb.train(params, dtrain, num_boost_round=100)
            oos_predictions[test_idx] = bst.predict(dtest)
            
        ic, pval = spearmanr(oos_predictions, y)
        return {"out_of_sample_rank_ic": float(ic), "p_value": float(pval), "predictions": oos_predictions}
    ```

#### Chapter 22: Generative AI & Autonomous LLM Agents for Fundamental Analysis
* **Section 22.1: Large Language Models in Equity Research & SEC Filings**
  * *Lecture Content*: Limitations of bag-of-words sentiment (Loughran & McDonald); fine-tuning open financial LLMs vs. Retrieval-Augmented Generation (RAG) using vector stores over 10-K and 10-Q filings. Chunking financial reports by section (Item 1, Item 1A, Item 7, Item 8).
* **Section 22.2: The "Virtual Graham-Dodd Investment Committee" Multi-Agent Architecture**
  * *Lecture Content*: Designing a collaborative multi-agent autonomous system:
    * **Agent A (Forensic Accounting Auditor)**: Analyzes notes to consolidated financial statements, changes in accounting policies, revenue recognition timing, and contingent obligations.
    * **Agent B (Competitive Moat Specialist)**: Evaluates Item 1 and Item 7 against Porter's Five Forces, pricing power, customer concentration, and supplier leverage.
    * **Agent C (Chief Risk Officer)**: Evaluates Item 1A (Risk Factors) and macro exposure, holding absolute veto power over position entry.
* **Section 22.3: Deterministic Guardrails & Pydantic Function Calling**
  * *Lecture Content*: Reducing unsupported model output through strict schemas, provenance checks, explicit abstention, and deterministic numeric verification against eligible source records. Schema validity and confidence do not prove factual truth or grant trading permission.
* *Sandbox Lab 22: Multi-Agent SEC 10-K Forensic Accounting & Qualitative Risk Auditor*
  * *Objective*: Construct a functional multi-agent pipeline in Python using structured Pydantic schemas that analyzes raw SEC 10-K filings, detects red flags, and generates a structured quantitative-qualitative rating.
  * *Starter Code*:
    ```python
    from pydantic import BaseModel, Field
    from typing import List

    class ForensicAccountingAudit(BaseModel):
        ticker: str
        revenue_recognition_risk: int = Field(ge=1, le=5, description="1=Clean, 5=Aggressive channel stuffing")
        off_balance_sheet_debt_detected: bool
        accounting_policy_red_flags: List[str]
        normalized_earning_power_adjustment_pct: float
        governance_candor_score: int = Field(ge=1, le=10)
        investment_committee_verdict: str = Field(description="'APPROVE', 'VETO', or 'REQUIRES_MONITORING'")
        rationale: str

    # Agent execution prompt schema
    PROMPT_TEMPLATE = """
    You are the Chief Forensic Accounting Auditor on the Graham-Dodd Investment Committee.
    Analyze the following footnotes from the 10-K filing of {ticker}:
    {filing_text}
    Extract all accounting manipulations and return your audit strictly as structured JSON matching the schema.
    """
    ```

#### Chapter 23: Production Risk Controls, Sizing & Deployment
* **Section 23.1: Optimal Position Sizing: The Kelly Criterion & Volatility Targeting**
  * *Lecture Content*: Continuous Kelly allocation: $f^* = \frac{\mu - r}{\sigma^2}$. Why full Kelly leads to extreme drawdowns and bankruptcy under parameter uncertainty; the Fractional Kelly rule ($0.25 f^*$ to $0.50 f^*$). Volatility parity sizing ($w_i \propto \frac{\sigma_{\text{target}}}{\sigma_i}$).
* **Section 23.2: Automated Circuit Breakers & Kill-Switches**
  * *Lecture Content*: Designing fail-safe protection layers in trading code:
    * Intraday Portfolio Drawdown Halt: Triggering liquidation if portfolio drops $> 2.5\%$ in 24 hours.
    * Stale Feed & Latency Disconnect: Rejecting new orders if market data timestamps lag by $> 500$ms.
    * Spread Blowout & Liquidity Guard: Withdrawing limit orders if bid-ask spread widens $> 3\times$ historical median.
* **Section 23.3: Production DevOps: Docker Microservices, Prometheus & Alert Webhooks**
  * *Lecture Content*: Containerizing bots with Docker; exporting real-time execution telemetry to Prometheus/Grafana (order latency, open risk, slippage); automated webhook dispatch to Telegram/Discord for critical risk events.
* *Sandbox Lab 23: Paper-Trading Bot with Production Risk Circuit Breakers & Prometheus Metrics*
  * *Objective*: Deploy a complete paper-trading bot into the Quanta sandbox, connected to the Mock Broker with automated kill-switches and Prometheus latency/PnL exporters.
  * *Starter Code*:
    ```python
    import time

    class ProductionRiskController:
        def __init__(self, initial_capital: float, max_drawdown_pct: float = 0.025):
            self.initial_capital = initial_capital
            self.peak_capital = initial_capital
            self.current_capital = initial_capital
            self.max_drawdown_pct = max_drawdown_pct
            self.kill_switch_triggered = False

        def update_portfolio_value(self, current_value: float, last_feed_timestamp: float) -> bool:
            current_time = time.time()
            # 1. Latency Disconnect Check (stale price > 500ms)
            if current_time - last_feed_timestamp > 0.50:
                print("CIRCUIT BREAKER: Stale market data feed! Halting execution.")
                self.kill_switch_triggered = True
                return False
                
            # 2. Drawdown Check
            self.current_capital = current_value
            if self.current_capital > self.peak_capital:
                self.peak_capital = self.current_capital
                
            drawdown = (self.peak_capital - self.current_capital) / self.peak_capital
            if drawdown >= self.max_drawdown_pct:
                print(f"CIRCUIT BREAKER TRIGGERED: Intraday drawdown {drawdown*100:.2f}% exceeds {self.max_drawdown_pct*100}% limit! Liquidating.")
                self.kill_switch_triggered = True
                return False
                
            return True

        def execute_paper_trading_loop(self, broker, symbol: str, signal: int, price: float, timestamp: float):
            import quanta as qn
            # Evaluate risk controller before order submission
            current_equity = broker.get_account().portfolio_equity
            if not self.update_portfolio_value(current_equity, timestamp):
                print("ABORTING: Kill-switch active! Liquidating open inventory and canceling orders.")
                broker.cancel_all_orders(symbol)
                pos = broker.get_positions().get(symbol)
                if pos and pos.quantity > 0:
                    broker.sell(symbol, pos.quantity, order_type=qn.broker.OrderType.MARKET)
                elif pos and pos.quantity < 0:
                    broker.cover(symbol, abs(pos.quantity), order_type=qn.broker.OrderType.MARKET)
                return

            # Submit bracket order (Entry + Take Profit + Stop Loss OCO)
            account = broker.get_account()
            if signal == 1 and account.buying_power >= price * 100 * 0.50:
                broker.bracket_order(
                    symbol=symbol,
                    side=qn.broker.OrderSide.BUY,
                    quantity=100,
                    entry_price=price,
                    take_profit=round(price * 1.03, 2),  # +3.0% take-profit target
                    stop_loss=round(price * 0.98, 2)     # -2.0% stop-loss threshold
                )
    ```

---

### TRACK 6: MFE-CRYPTO 801 — Web3, Tokenomics, DeFi Microstructure & Crypto Bot Engineering
*Applying classical monetary economics, quantitative finance, and game theory to decentralized finance (DeFi), automated market makers, and on-chain bot engineering.*

#### Chapter 24: Cryptoeconomics, Tokenomics & Monetary Theory
* **Section 24.1: Classical Monetary Theory in Cryptoeconomics**
  * *Lecture Content*: Irving Fisher’s Equation of Exchange ($M \cdot V = P \cdot Y$) applied to utility tokens. The "Velocity Problem": Why transactional tokens without staking or cash-flow accrual experience velocity expansion and long-run price collapse.
* **Section 24.2: Programmatic Supply Curves & Game-Theoretic Issuance**
  * *Lecture Content*: Bitcoin disinflationary halving schedule: Stock-to-Flow dynamics. Ethereum EIP-1559 base fee burning:
    $$B_t = \sum_{i \in \text{Txs}} \text{GasUsed}_i \times \text{BaseFee}_t$$
    *Net issuance regimes: Deflationary vs. inflationary transition thresholds based on blob gas and L1 execution demand.*
* **Section 24.3: Proof-of-Stake Native Yield as the Digital Risk-Free Benchmark ($r_f^{\text{crypto}}$)**
  * *Lecture Content*: Validator economics: Consensus rewards, priority tips, and MEV extraction. Establishing Ethereum staking APR as the native digital risk-free benchmark ($r_f^{\text{crypto}}$); calculating the Equity Risk Premium (ERP) of protocol tokens and altcoins.
* **Section 24.4: Intrinsic Protocol Valuation & Fee Switches**
  * *Lecture Content*: Applying Graham & Dodd fundamental valuation to Web3: Discounted cash flow (DCF) models and Price-to-Fee ($P/F$) multiples applied to protocol fee-switches (Uniswap, Aave, MakerDAO/Sky protocol revenues vs. token buyback & burn mechanics).
* *Sandbox Lab 24: Protocol Tokenomics & Discounted Cash Flow Valuation Simulator*
  * *Objective*: Build an interactive tokenomics model that simulates programmatic token emission, burn rates, staking dilution, and DCF intrinsic protocol valuation under variable network activity.
  * *Starter Code*:
    ```python
    import numpy as np

    def simulate_tokenomics_dcf(initial_supply: float, emission_rate_annual: float, burn_rate_annual: float,
                                annual_fees_usd: float, fee_switch_pct: float, discount_rate: float, years: int = 10) -> dict:
        supply = initial_supply
        pv_cash_flows = 0.0
        
        for t in range(1, years + 1):
            net_issuance = supply * (emission_rate_annual - burn_rate_annual)
            supply += net_issuance
            
            # Protocol fee cash flow directed to token buyback / staking yield
            cash_flow_t = annual_fees_usd * fee_switch_pct * ((1 + 0.05)**t)  # Assuming 5% protocol fee growth
            pv_cash_flows += cash_flow_t / ((1 + discount_rate)**t)
            
        terminal_growth = 0.02
        terminal_cf = (annual_fees_usd * fee_switch_pct * ((1 + 0.05)**years)) * (1 + terminal_growth)
        terminal_value = terminal_cf / (discount_rate - terminal_growth)
        pv_tv = terminal_value / ((1 + discount_rate)**years)
        
        fair_market_cap = pv_cash_flows + pv_tv
        fair_token_price = fair_market_cap / supply
        
        return {
            "ending_supply": float(supply),
            "pv_protocol_fees_usd": float(pv_cash_flows),
            "terminal_value_usd": float(pv_tv),
            "fair_market_cap_usd": float(fair_market_cap),
            "fair_token_price_usd": float(fair_token_price)
        }
    ```

#### Chapter 25: Automated Market Makers (AMMs) & Liquidity Microstructure
* **Section 25.1: Constant Product Market Makers (CPMM: $x \cdot y = k$)**
  * *Lecture Content*: Uniswap v2 invariant. Deriving marginal price ($P = y / x$); exact price impact formula for trade size $\Delta x$ with fee $(1 - \gamma)$:
    $$\Delta y = \frac{y \cdot (1 - \gamma)\Delta x}{x + (1 - \gamma)\Delta x}, \quad \text{Slippage } = \frac{\Delta x}{x + \Delta x}$$
* **Section 25.2: Concentrated Liquidity (Uniswap v3)**
  * *Lecture Content*: Virtual reserves and concentrated capital efficiency. Liquidity density $L = \sqrt{x y}$; real reserves of token $X$ and $Y$ inside price interval $[p_a, p_b]$:
    $$x = L \left( \frac{1}{\sqrt{P}} - \frac{1}{\sqrt{p_b}} \right), \quad y = L (\sqrt{P} - \sqrt{p_a})$$
    *Tick spacing mathematics ($p(i) = 1.0001^i$), range orders, and capital multiplier vs. Uniswap v2.*
* **Section 25.3: Impermanent Loss (IL) Mathematical Derivation**
  * *Lecture Content*: Holding value vs. LP pool value:
    $$V_{\text{hold}}(k) = \frac{P_0 x_0 (1 + k)}{2}, \quad V_{\text{pool}}(k) = P_0 x_0 \sqrt{k} \quad \left(k = \frac{P}{P_0}\right)$$
    $$\text{IL}(k) = \frac{V_{\text{pool}} - V_{\text{hold}}}{V_{\text{hold}}} = \frac{2\sqrt{k}}{1 + k} - 1$$
* **Section 25.4: Loss-Versus-Rebalancing (LVR) & Toxic Order Flow**
  * *Lecture Content*: Milionis, Moallemi, Roughgarden (2022): Proving why passive LP yield is structurally negative against informed arbitrageurs who rebalance pools on external CEX price discovery. Quantifying LVR as an unhedged volatility option cost:
    $$\text{LVR}_t = \int_0^t \frac{\sigma^2}{8} V_u du$$
* **Section 25.5: Specialized AMM Invariants: The Curve Stableswap Invariant**
  * *Lecture Content*: Combining constant sum ($x + y = D$) for low slippage around peg with constant product ($x \cdot y = (D/n)^n$) for infinite liquidity:
    $$A n^n \sum x_i + D = A D n^n + \frac{D^{n+1}}{n^n \prod x_i}$$
* *Sandbox Lab 25: Uniswap v3 Concentrated Liquidity & LVR Backtester*
  * *Objective*: Backtest custom concentrated liquidity ranges on historical ETH/USDC 1-minute swap data, evaluating fee APR against realized impermanent loss and LVR.
  * *Starter Code*:
    ```python
    import numpy as np

    def calculate_uniswap_v3_position(P_current: float, P_lower: float, P_upper: float, capital_usd: float) -> dict:
        """
        Computes token allocation, liquidity L, and capital efficiency multiplier for Uniswap v3.
        """
        sqrt_P = np.sqrt(P_current)
        sqrt_Pa = np.sqrt(P_lower)
        sqrt_Pb = np.sqrt(P_upper)
        
        # Calculate capital efficiency multiplier vs v2
        multiplier = 1.0 / (1.0 - (sqrt_Pa / sqrt_Pb))
        
        # Determine token weights inside range
        delta_x_per_L = (1.0 / sqrt_P) - (1.0 / sqrt_Pb)
        delta_y_per_L = sqrt_P - sqrt_Pa
        
        cost_per_L = P_current * delta_x_per_L + delta_y_per_L
        L = capital_usd / cost_per_L
        
        x_reserves = L * delta_x_per_L
        y_reserves = L * delta_y_per_L
        
        return {
            "liquidity_L": L,
            "x_tokens": x_reserves,
            "y_tokens": y_reserves,
            "capital_efficiency_multiplier": multiplier
        }
    ```

#### Chapter 26: Quantitative Crypto Arbitrage & Market-Neutral Yield
* **Section 26.1: Perpetual Futures Mechanics & Funding Rate Dynamics**
  * *Lecture Content*: Index price (spot benchmark), Mark price (fair price avoiding scam wicks), and the 8-hour funding rate mechanism:
    $$F = \text{Clamp}\left( \text{Premium Index} + \text{Clamp}(r - \text{Premium Index}, -0.05\%, +0.05\%), -0.75\%, +0.75\% \right)$$
* **Section 26.2: Cash-and-Carry Basis Arbitrage (Delta-Neutral)**
  * *Lecture Content*: Constructing delta-neutral yield harvesting: Long spot asset + short perpetual futures contract when funding rate is positive ($F > 0$). Managing basis blowouts, liquidation risk buffers, margin collateral rebalancing, and exchange counterparty risk.
* **Section 26.3: Cross-Venue & Triangular Arbitrage**
  * *Lecture Content*: Latency arbitrage across centralized exchange (CEX) limit order books and decentralized automated market makers (DEX); triangular arbitrage across spot currency pairs.
* **Section 26.4: Maximal Extractable Value (MEV) & Mempool Economics**
  * *Lecture Content*: Priority Gas Auctions (PGA); Flashbots and Searcher-Builder Separation (SBS); atomic sandwich attacks, backrunning newly listed pools, and on-chain liquidation bots.
* *Sandbox Lab 26: Delta-Neutral Perpetual Funding Rate Arbitrage Engine*
  * *Objective*: Backtest an automated funding-rate cash-and-carry arbitrage strategy across historical perpetual swap data, verifying margin safety buffers during major flash-crash events.
  * *Starter Code*:
    ```python
    import numpy as np
    import pandas as pd

    def backtest_funding_rate_arbitrage(spot_prices: np.ndarray, perp_prices: np.ndarray, funding_rates_8h: np.ndarray,
                                        initial_margin_usd: float = 100000.0, leverage: float = 2.0) -> dict:
        """
        Delta-neutral: Long Spot $50k, Short Perp $50k (1x leverage for zero liquidation risk)
        or 2x leverage with margin buffer.
        """
        capital = initial_margin_usd
        n_periods = len(funding_rates_8h)
        cumulative_yield = 0.0
        margin_calls = 0
        
        position_notional = (capital / 2.0) * leverage
        
        for t in range(n_periods):
            f_rate = funding_rates_8h[t]
            # When funding is positive, longs pay shorts -> Short perp collects fee
            funding_collected = position_notional * f_rate
            cumulative_yield += funding_collected
            
            # Check margin health against basis divergence
            basis_loss = position_notional * ((perp_prices[t] - spot_prices[t]) / spot_prices[t])
            current_equity = capital + cumulative_yield - basis_loss
            if current_equity < capital * 0.20:
                margin_calls += 1  # Liquidated
                break
                
        annualized_apr = (cumulative_yield / initial_margin_usd) * (365 * 3 / n_periods)
        return {
            "ending_capital": float(current_equity),
            "cumulative_funding_usd": float(cumulative_yield),
            "annualized_apr": float(annualized_apr),
            "margin_calls": margin_calls
        }
    ```

#### Chapter 27: On-Chain Web3 Bot Engineering & Execution
* **Section 27.1: Connecting to the Blockchain: RPC Nodes, WebSockets & Web3.py**
  * *Lecture Content*: JSON-RPC node architecture (Infura, Alchemy, private Erigon/Reth nodes); subscribing to new pending transactions and contract event logs (`Swap`, `Sync`, `Transfer`) over WebSocket connections.
* **Section 27.2: EIP-1559 Dynamic Gas Bidding**
  * *Lecture Content*: Understanding base fee adjustments ($g_{t+1} = g_t \left(1 + \frac{1}{8} \frac{\text{GasUsed} - \text{GasTarget}}{\text{GasTarget}}\right)$); bidding `maxPriorityFeePerGas` (miner tip) to secure block priority; priority escalation algorithms for urgent fills.
* **Section 27.3: Nonce Management & Mempool Replacements**
  * *Lecture Content*: Managing local transaction nonces across concurrent async worker threads; replacing stuck transactions (`speedup` and `cancel`) using identical nonces with $> 12\%$ gas fee increments.
* **Section 27.4: Flash Loan Arbitrage Bot Anatomy**
  * *Lecture Content*: Architecting an atomic on-chain arbitrage system:
    $$\text{Off-Chain Python Monitor} \longrightarrow \text{Discrepancy Detected} \longrightarrow \text{Trigger Smart Contract} \longrightarrow \text{Flash Loan Borrow (Aave/Balancer)} \longrightarrow \text{Multi-DEX Swaps} \longrightarrow \text{Repay Loan} \longrightarrow \text{Keep Profit}$$
* *Sandbox Lab 27: Production Web3 Mempool Event Listener & Dynamic Gas Bidding Bot*
  * *Objective*: Construct a functional Python Web3 event listener bot monitoring Uniswap pools and executing simulated atomic swaps.
  * *Starter Code*:
    ```python
    import asyncio
    from web3 import AsyncWeb3
    from web3.providers import AsyncHTTPProvider

    class Web3ArbListener:
        def __init__(self, rpc_url: str, uniswap_pool_address: str):
            self.w3 = AsyncWeb3(AsyncHTTPProvider(rpc_url))
            self.pool_address = self.w3.to_checksum_address(uniswap_pool_address)
            
        async def estimate_eip1559_gas(self) -> dict:
            latest_block = await self.w3.eth.get_block('latest')
            base_fee = latest_block['baseFeePerGas']
            priority_tip = self.w3.to_wei(2, 'gwei')
            max_fee = int(base_fee * 1.25) + priority_tip
            return {"maxFeePerGas": max_fee, "maxPriorityFeePerGas": priority_tip}

        async def monitor_swaps(self):
            # Listening to Swap events
            print(f"Monitoring swaps on pool: {self.pool_address}")
            gas_params = await self.estimate_eip1559_gas()
            print(f"Dynamic gas estimate: {gas_params}")
    ```

#### Chapter 28: Crypto Sandbox: Stress Testing & Extreme Regime Simulation
* **Section 28.1: De-Pegging Mechanics & Run Dynamics**
  * *Lecture Content*: Simulating death-spiral dynamics (algorithmic stablecoins, collateral runs, reserve bank runs, Terra/LUNA collapse case study).
* **Section 28.2: Cascading Liquidation Simulators**
  * *Lecture Content*: Modeling collateralized lending protocols (Aave, MakerDAO) under instantaneous 50% collateral flash crashes with congested network block inclusion.
* **Section 28.3: Network Congestion & Gas Shock Survival**
  * *Lecture Content*: Simulating bot profitability and risk limits when gas prices spike from 15 Gwei to 1,500 Gwei.
* *Sandbox Lab 28: Leveraged Lending Liquidation & Collateral Health Shock Simulator*
  * *Objective*: Stress test a leveraged DeFi yield strategy against synthetic liquidity freeze and oracle latency shock scenarios.

## 5. Mock & Sandbox Engine Specifications

The centerpiece of Quanta is its **Dual-Mode Interactive Simulation Engine**, which allows learners to test their valuation formulas, factor rankings, and trading bots against both **Empirical Real Market Data** and **Synthetic Counterfactual Market Data**.

```
+---------------------------------------------------------------------------------------------------+
|                                        QUANTA SIMULATION ENGINE                                   |
+-------------------------------------------------+-------------------------------------------------+
|          MODE 1: REAL HISTORICAL ENGINE         |       MODE 2: SYNTHETIC GENERATIVE LAB          |
+-------------------------------------------------+-------------------------------------------------+
| • Point-in-Time SEC 10-K/10-Q (1990–Present)    | • 1. Geometric Brownian Motion (Null Model)     |
| • Full US Equities Universe (S&P 500, Russell)  | • 2. Merton Jump-Diffusion (Crash Model)        |
| • Delisted / Bankrupt Equities (Survivorship-Free)| • 3. Heston Stochastic Volatility Model       |
| • Corporate Actions (Splits, Dividend Reinvest) | • 4. Markov Regime-Switching Process            |
| • Macro Series (10Y Yield, Fed Funds, CPI)      | • 5. Concentrated Liquidity AMM Simulator       |
| • Crypto EOD & Hourly + Perp Funding Rates      | • 6. Cascading Liquidation & Gas Shock Model    |
+-------------------------------------------------+-------------------------------------------------+
```

---

### 5.1 Mode 1: Empirical Real Market Engine

#### 5.1.1 Point-in-Time Accounting Architecture
* **The Look-Ahead Problem**: Standard financial databases backfill accounting numbers to the fiscal period end date (e.g. December 31). However, companies do not publish their 10-K until 45–90 days later (e.g. March 15). Backtesting using period-end dates creates massive look-ahead bias.
* **Filing Date Keying**: In Quanta, all financial statement items are strictly indexed by their `sec_acceptance_datetime`. An algorithm running on February 1, 2021 cannot observe 2020 annual numbers if the 10-K was filed on February 25, 2021.
* **Restatements & Revisions**: The engine preserves both the as-reported filing and subsequent restatements, preventing future restatements from leaking into historical evaluation windows.

#### 5.1.2 Elimination of Survivorship Bias
* The database contains every stock traded on NYSE, NASDAQ, and AMEX from 1990 to present, specifically preserving:
  * Bankrupt corporations (e.g., Enron, Lehman Brothers, WorldCom).
  * Acquired and merged entities (e.g., Compaq, Merrill Lynch).
  * Delisted penny stocks failing exchange capitalization requirements.
* This is essential for Track 1 and Track 4: Graham's Net-Net screen produces illusory outperformance if distressed companies that subsequently went to zero are omitted.

#### 5.1.3 Institutional Transaction Cost & Fill Model
* Execution fills are modeled with configurable market friction:
  1. **Fixed Commission**: $\$0.005$ per share or $0.05\%$ notional fee.
  2. **Bid-Ask Half-Spread**: Modeled dynamically from historical daily volatility:
     $$\text{Half-Spread}_t \approx \max\left(0.0001, \ 0.05 \times \sigma_{\text{daily}, t}\right)$$
  3. **Square-Root Price Impact**:
     $$\Delta P = \text{Sign}(\text{Trade}) \cdot Y \cdot \sigma_t \cdot \sqrt{\frac{\text{Trade Volume}}{\text{Daily Volume}}}$$

---

### 5.2 Mode 2: Synthetic Market Generative Engines (Counterfactual Laboratory)

Synthetic data allows students to subject algorithms to stress regimes that may not have occurred in recent history, testing whether a strategy's performance is an empirical accident or mathematically robust.

#### 5.2.1 Generator 1: Geometric Brownian Motion (Null Hypothesis Benchmark)
* **Stochastic Differential Equation**:
  $$dS_t = \mu S_t dt + \sigma S_t dW_t$$
* **Euler-Maruyama Discretization**:
  $$S_{t+\Delta t} = S_t \exp\left( \left(\mu - \frac{1}{2}\sigma^2\right)\Delta t + \sigma \sqrt{\Delta t} Z_t \right), \quad Z_t \sim \mathcal{N}(0, 1)$$
* **Pedagogical Function**: The baseline for testing the Efficient Market Hypothesis (EMH). If a student's technical indicator or momentum rule generates positive Sharpe ratios on GBM series, it proves data snooping or backtest methodology leakage.
* **Python Generator Implementation**:
  ```python
  import numpy as np

  def generate_gbm(s0: float, mu: float, sigma: float, t_years: float, steps: int) -> np.ndarray:
      dt = t_years / steps
      z = np.random.standard_normal(steps)
      log_returns = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z
      price_path = np.zeros(steps + 1)
      price_path[0] = s0
      price_path[1:] = s0 * np.exp(np.cumsum(log_returns))
      return price_path
  ```

#### 5.2.2 Generator 2: Merton Jump-Diffusion (Catastrophic Liquidity Gaps)
* **Stochastic Differential Equation**:
  $$dS_t = (\mu - \lambda \kappa) S_t dt + \sigma S_t dW_t + (J - 1) S_t dN_t$$
  *(where $N_t$ is a Poisson process with jump intensity $\lambda$, and $\ln(J) \sim \mathcal{N}(\mu_J, \sigma_J^2)$ with $\kappa = \mathbb{E}[J - 1] = e^{\mu_J + \frac{1}{2}\sigma_J^2} - 1$).*
* **Pedagogical Function**: Stress tests risk controls, margin stop-losses, and options hedges against discontinuous overnight market gaps (e.g. 1987 Black Monday, 2020 COVID shock).
* **Python Generator Implementation**:
  ```python
  def generate_merton_jump(s0: float, mu: float, sigma: float, lamb: float, mu_j: float, sigma_j: float, t_years: float, steps: int) -> np.ndarray:
      dt = t_years / steps
      kappa = np.exp(mu_j + 0.5 * sigma_j**2) - 1.0
      
      n_jumps = np.random.poisson(lamb * dt, steps)
      z_diff = np.random.standard_normal(steps)
      
      # Log-returns component
      drift = (mu - lamb * kappa - 0.5 * sigma**2) * dt
      diffusion = sigma * np.sqrt(dt) * z_diff
      jumps = np.array([np.sum(np.random.normal(mu_j, sigma_j, n)) if n > 0 else 0.0 for n in n_jumps])
      
      log_returns = drift + diffusion + jumps
      price_path = np.zeros(steps + 1)
      price_path[0] = s0
      price_path[1:] = s0 * np.exp(np.cumsum(log_returns))
      return price_path
  ```

#### 5.2.3 Generator 3: Heston Stochastic Volatility Model
* **Coupled SDE System**:
  $$dS_t = \mu S_t dt + \sqrt{\nu_t} S_t dW_t^S$$
  $$d\nu_t = \kappa(\theta - \nu_t)dt + \xi \sqrt{\nu_t} dW_t^\nu, \quad \text{with } \mathbb{E}[dW_t^S dW_t^\nu] = \rho dt$$
  *(Parameters: $\kappa$ = mean reversion speed, $\theta$ = long-run variance, $\xi$ = volatility of volatility, $\rho$ = correlation between asset return and volatility, satisfying the Feller condition $2\kappa\theta > \xi^2$).*
* **Pedagogical Function**: Simulates realistic volatility clustering, leverage effects (asset drops generating volatility spikes), and non-constant variance smiles.

#### 5.2.4 Generator 4: Markov Regime-Switching Process
* **3-State Macroeconomic Markov Chain**:
  * **State 1 (Bull Market)**: $\mu_1 = +16\%$, $\sigma_1 = 11\%$
  * **State 2 (Sideways / Mean-Reverting)**: $\mu_2 = +2\%$, $\sigma_2 = 16\%$
  * **State 3 (Panic / Liquidity Crisis)**: $\mu_3 = -40\%$, $\sigma_3 = 48\%$
* **Transition Probability Matrix**:
  $$\mathbf{P} = \begin{pmatrix} 0.96 & 0.03 & 0.01 \\ 0.05 & 0.90 & 0.05 \\ 0.08 & 0.12 & 0.80 \end{pmatrix}$$
* **Pedagogical Function**: Tests whether systematic factor portfolios (Value, Momentum) or dynamic risk parity models survive regime transitions when correlations jump to 1.0.

#### 5.2.5 Generator 5: AMM Concentrated Liquidity & LVR Pool Simulator
* Models tick-level swaps against Uniswap v3 virtual reserve equations.
* Simulates external CEX prices driven by high-frequency jump processes; simulates arbitrage bots extracting value from pool stale quotes, computing real-time Loss-Versus-Rebalancing (LVR) vs. earned transaction fees.

#### 5.2.6 Generator 6: Cascading Liquidation & Network Congestion Simulator
* Simulates decentralized collateralized debt positions (CDPs) under sudden collateral drops.
* Models Ethereum / EVM gas price spikes from 20 Gwei to 2,000 Gwei, simulating mempool transaction dropping and failed liquidation executions.

---

### 5.3 Institutional Stock Buying & Selling Simulator (Virtual Brokerage & Order Matching Engine)

Quanta features an integrated institutional Paper Trading & Execution Simulator. Unlike naive backtesters that assume instantaneous fills at the bar's closing price with infinite liquidity, Quanta embeds an event-driven virtual brokerage matching engine. This engine enforces microstructural realism: Level 2 order book queues, slippage as a function of size and volatility, short locate borrow fees, and Regulation T margin accounting.

```
+---------------------------------------------------------------------------------------------------+
|                                QUANTA VIRTUAL BROKERAGE ARCHITECTURE                              |
+-------------------------------------------------+-------------------------------------------------+
|              MATCHING & ROUTING ENGINE          |           MARGIN & RISK CONTROL ENGINE          |
+-------------------------------------------------+-------------------------------------------------+
| • Price-Time Priority (FIFO) Limit Order Book   | • Regulation T Margining (50% Init / 25% Maint) |
| • Passive Queue Position Tracking               | • Short Locates: Easy vs Hard-to-Borrow (HTB)   |
| • Continuous Double Auction & Crossing Logic    | • Daily Borrow Fee Accrual (APR-Compounded)     |
| • Market, Limit, Stop, Trailing Stop, Bracket   | • Intraday 4:1 vs Overnight 2:1 Buying Power    |
| • TWAP & VWAP Child Order Slicing Algorithms    | • Forced Margin Call Liquidation Protocol       |
+-------------------------------------------------+-------------------------------------------------+
|                             EXECUTION FRICTION & COST MODELS                                      |
| • Kyle's Lambda & Almgren-Chriss Market Impact  | • SEC Section 31 Fee ($0.0000278 * Principal)   |
| • Bid-Ask Half-Spread Dynamic Elasticity        | • FINRA Trading Activity Fee (TAF) ($0.000166)  |
+---------------------------------------------------------------------------------------------------+
```

#### 5.3.1 Virtual Matching Engine & Microstructure Architecture
* **Order Book State Representation**: Modeled as an explicit two-sided priority queue:
  $$\mathcal{B} = \{(p_i^b, q_i^b, \tau_i^b)\}_{i=1}^{N_b} \quad \text{where } p_1^b > p_2^b > \dots, \quad \tau_i^b \text{ is arrival timestamp}$$
  $$\mathcal{A} = \{(p_j^a, q_j^a, \tau_j^a)\}_{j=1}^{N_a} \quad \text{where } p_1^a < p_2^a < \dots, \quad \tau_j^a \text{ is arrival timestamp}$$
* **Queue Priority & Fill Probability for Limit Orders**:
  * When a student submits a passive limit buy order at price $P_{\text{limit}} \le P_{\text{bid}}$, the order enters the back of the queue at that price level:
    $$Q_{\text{ahead}} = \text{Depth}(P_{\text{limit}})$$
  * In historical replay or synthetic simulation, the limit order fills only when cumulative traded volume at $P_{\text{limit}}$ exhausts the queue ahead:
    $$\sum_{k} V_k(P_{\text{limit}}) \ge Q_{\text{ahead}} + Q_{\text{order}}$$
  * For trade-throughs (where $P_{\text{trade}} < P_{\text{limit}}$), the order receives an immediate fill at $P_{\text{limit}}$ (price improvement).

#### 5.3.2 Comprehensive Order Types & State Machine
1. **Market Orders**:
   * Executed immediately against resting liquidity. If order size exceeds the Best Bid/Offer (BBO) depth, the order sweeps the book with adverse slippage according to the square-root impact model.
2. **Limit Orders**:
   * Supports `DAY` (expires at market close 16:00 EST), `GTC` (Good-Till-Canceled), `IOC` (Immediate-Or-Cancel), and `FOK` (Fill-Or-Kill).
3. **Stop-Loss & Stop-Limit Orders**:
   * Monitored on every tick/bar.
   * A Stop-Loss becomes a Market Order when $P_{\text{last}} \le P_{\text{stop}}$ (for sell stops) or $P_{\text{last}} \ge P_{\text{stop}}$ (for buy stops).
   * A Stop-Limit converts to a Limit Order at the specified limit price once triggered.
4. **Trailing Stop Orders**:
   * Maintains a dynamic stop threshold anchored to the extreme price reached since activation:
     * For long position protection: $P_{\text{stop}}(t) = \max_{s \le t} [P(s)] - \Delta_{\text{trail}}$ (or percentage trail: $\max_{s \le t} [P(s)] \cdot (1 - \delta_{\%})$).
5. **Bracket Orders (One-Cancels-the-Other / OCO)**:
   * Combines an entry order with two mutually exclusive child exit orders: a Take-Profit limit order and a Stop-Loss order. Execution of either child immediately cancels the other.
6. **Algorithmic Slicing Orders (TWAP & VWAP)**:
   * **TWAP**: Slices a parent order $Q$ across $N$ uniform time slices $\Delta t$: $q_k = Q/N$.
   * **VWAP**: Slices $Q$ dynamically weighted by historical volume profile: $q_k = Q \times \frac{\bar{V}_k}{\sum \bar{V}_i}$, with a strict participation cap ($\le 10\%$ of bar volume) to minimize price distortion.

#### 5.3.3 Real-Time Margin, Leverage & Short-Selling System (Reg T & Portfolio Margin)
* **Account Types**:
  * **Cash Account**: Purchases restricted to settled cash. Day trading proceeds subject to $T+1$ settlement rules; unauthorized re-use triggers Good Faith Violations (GFV).
  * **Margin Account (Reg T)**: Provides intraday $4:1$ purchasing power and overnight $2:1$ purchasing power. Enforces FINRA Rule 4210 and Pattern Day Trader (PDT) balance threshold ($\$25,000$).
* **Long Position Margining**:
  $$\text{Initial Margin Requirement} = 0.50 \times \sum (P_i \cdot Q_i^{\text{long}})$$
  $$\text{Maintenance Margin Requirement} = 0.25 \times \sum (P_i \cdot Q_i^{\text{long}})$$
* **Short Selling Mechanics**:
  1. **Borrow Locate Engine**: Before placing a short sale, the simulator queries the borrow registry. Equities are classified into:
     * *Easy-to-Borrow (ETB)*: General collateral rate, borrow fee $0.30\% - 0.75\%$ APR.
     * *Hard-to-Borrow (HTB)*: Limited supply, borrow fee ranging from $5\%$ to $>100\%$ APR.
     * *Threshold Securities (Reg SHO)*: Unavailable for shorting.
  2. **Short Collateral & Daily Borrow Fee Accrual**:
     * Short proceeds are credited to cash but locked as collateral.
     * Initial short margin: $150\%$ of short market value ($100\%$ short sale proceeds + $50\%$ cash equity).
     * Short maintenance margin: $130\%$ of short market value (or $\$5.00$/share minimum for stocks $<\$5.00$).
     * Daily borrow interest fee deducted continuously:
       $$\text{Fee}_{\text{borrow}} = \frac{|Q_{\text{short}}| \times P_t \times \text{APR}_{\text{borrow}}}{360}$$
  3. **Short Squeeze & Forced Buy-In Simulation**:
     * If short borrow availability drops to zero or regulatory threshold lists trigger buy-in notices, the simulator issues an involuntary buy-to-cover at the current market ask price.
* **Margin Call & Involuntary Liquidation Protocol**:
  * Total Portfolio Equity:
    $$E_t = \text{Cash}_t + \sum_{i \in \text{Longs}} (P_{i,t} \cdot Q_{i,t}) - \sum_{j \in \text{Shorts}} (P_{j,t} \cdot |Q_{j,t}|)$$
  * Maintenance Excess:
    $$\text{ME}_t = E_t - \left[ 0.25 \times \sum_{i \in \text{Longs}} (P_{i,t} \cdot Q_{i,t}) + 0.30 \times \sum_{j \in \text{Shorts}} (P_{j,t} \cdot |Q_{j,t}|) \right]$$
  * If $\text{ME}_t < 0$, a **Margin Call** is triggered. The student is given a configurable grace window (e.g., 2 virtual hours). If margin is not restored, the liquidation worker executes market orders, liquidating positions in order of descending liquidity until $\text{ME}_t \ge 0$.

#### 5.3.4 Execution Quality, Transaction Costs & Regulatory Fees
Every simulated trade logs institutional transaction costs:
* **Broker Commission**: Configurable from zero-commission retail ($0.00$) to institutional prime broker fee ($\$0.0035$/share or $3.5\text{ bps}$).
* **Exchange Fees & ECN Rebates**:
  * Maker rebate: $-\$0.0020$/share (credit for providing passive liquidity).
  * Taker fee: $+\$0.0030$/share (cost for removing active liquidity).
* **Regulatory Fees (US Equities)**:
  * **SEC Section 31 Transaction Fee**: $\$27.80$ per million dollars of gross sales ($0.0000278 \times \text{Principal}$).
  * **FINRA Trading Activity Fee (TAF)**: $\$0.000166$ per share sold (maximum $\$8.30$ per trade).

#### 5.3.5 Dual-Interface Trading Modes
1. **Interactive Manual GUI Trading Terminal**:
   * Point-and-click trade placement directly from the chart or DOM ladder.
   * Dynamic risk calculators: input risk percentage (e.g. $1.0\%$ of equity), and the ticket automatically calculates optimal share size based on entry and stop-loss levels.
   * Interactive chart dragging: adjust stop-loss or take-profit lines dynamically on the TradingView canvas.
2. **Programmatic Python Bot API**:
   * Full asynchronous programmatic control via `quanta.broker.PaperBroker`.
   * Real-time callbacks for trade events (`on_fill`, `on_order_status`, `on_margin_call`).
   * Seamless transition from historical vectorbt/backtesting to live paper trading execution against real-time WebSocket tick feeds.

#### 5.3.6 Continuous Mark-to-Market Accounting & Blotter Metrics
* Real-time computation of:
  * **Unrealized PnL**: $\sum Q_i \cdot (P_t - \bar{P}_{\text{entry}})$
  * **Realized PnL**: Cumulative cash delta from closed positions less commissions, SEC/TAF fees, and short borrow fees.
  * **Volume Weighted Average Price (VWAP) Slippage**: Difference between fill price and arrival midpoint price:
    $$\text{Slippage}_{\text{bps}} = \frac{|P_{\text{fill}} - P_{\text{arrival}}|}{P_{\text{arrival}}} \times 10,000$$

---

## 6. Interactive UI & UX Specifications

### 6.1 Split-Screen Lecture Hall Layout (ASCII Wireframe)

```
+-----------------------------------------------------------------------------------------------------------------------+
| [QUANTA]  Track 1: Security Analysis  >  Chapter 2: Balance Sheet  >  Sec 2.2: Net-Net (NCAV)   [Dark]  [Profile]     |
+-----------------------------------------------------------------+-----------------------------------------------------+
| LEFT PANE: ACADEMIC LECTURE & PROOFS (Scrollable)               | RIGHT PANE: COMPUTATIONAL LAB & SANDBOX             |
|                                                                 |                                                     |
| # 2.2 Net-Current-Asset Value (NCAV) & Liquidation              | [Mode: Real Historical v] [Ticker: TIKR v] [Run >]  |
|                                                                 |-----------------------------------------------------|
| In Chapter 43 of *Security Analysis*, Graham and Dodd state:    | 1  import numpy as np                               |
| > "A company's liquidation value may be determined by applying  | 2  import quanta as qn                              |
| > appropriate discounts to its current and fixed assets..."     | 3                                                   |
|                                                                 | 4  def evaluate_ncav(ticker, date):                 |
| ## The Formal Liquidation Haircut Model                         | 5      bs = qn.data.get_balance_sheet(ticker, date) |
| Let $A_{\text{curr}}$ be total current assets and $L$ be        | 6      ncav = bs.cash + 0.8*bs.ar + 0.5*bs.inv - bs.|
| total obligations. We define conservative Net-Net Capital:      | 7      price = qn.data.get_close_price(ticker, date)|
|                                                                 | 8      return price < (2/3) * ncav                  |
| $$NNWC = (\text{Cash} + 0.8 AR + 0.5 Inv) - L_{\text{total}}$$  |-----------------------------------------------------|
|                                                                 | [ > Execute Sandbox (Cmd+Enter) ]  [Reset Template] |
| > [!NOTE]                                                       |-----------------------------------------------------|
| > Empirical testing reveals that companies trading at           | PERFORMANCE & ATTRIBUTION METRICS                   |
| > $P < \frac{2}{3} NNWC$ exhibit significant positive alpha     | +-------------+-------------+------------+----------+ |
| > but carry severe idiosyncratic bankruptcy hazards.           | | Sharpe: 1.42| Sortino: 1.88| MaxDD: -18%| Alpha:+6%| |
|                                                                 | +-------------+-------------+------------+----------+ |
| [Transfer Code to Lab ->]                                       | FINANCIAL CHART PANEL (Lightweight-Charts)          |
|                                                                 |   Candlesticks + Equity Curve vs S&P 500            |
| ### Historical Case Study: 2008 Microcap Distressed Universe    |     /\_/\_/\_/\___ (Portfolio)                      |
| Below is the point-in-time balance sheet for Acme Mfg (2008):   |    /__/\___/\_____ (S&P 500)                        |
| [Interactive Filing Table: Cash: $12M | AR: $18M | Debt: $14M]  |                                                     |
+-----------------------------------------------------------------+-----------------------------------------------------+
```

### 6.2 Minimalist Design Tokens & Typography Hierarchy
* **Color Palette (Monochrome Focus)**:
  * Background Primary: `bg-slate-950` (Dark) / `bg-white` (Light)
  * Background Secondary / Panel: `bg-slate-900` / `bg-slate-50`
  * Borders & Dividers: `border-slate-800` / `border-slate-200`
  * Text Primary: `text-slate-100` / `text-slate-900`
  * Text Muted: `text-slate-400` / `text-slate-500`
  * Directional Accents:
    * Positive Returns / Yield: `text-emerald-500` / `bg-emerald-500/10`
    * Negative Returns / Drawdown: `text-rose-500` / `bg-rose-500/10`
    * Benchmark Curve: `text-indigo-400`
* **Typography**:
  * Headings & Prose: `font-sans` (`Inter`, `Geist Sans`) with line height `leading-relaxed` (1.65).
  * Mathematical Equations: `KaTeX` native serif fonts.
  * Code & Financial Tables: `font-mono` (`JetBrains Mono`, `Geist Mono`) with CSS `font-variant-numeric: tabular-nums`.

### 6.3 New Stock Trading Simulator — TradingView-Style Workspace

**Product requirement:** Build a new, standalone stock paper-trading workspace at `/simulator`, with a TradingView-style charting layout and interaction model. The main experience is selecting a stock, analyzing its chart, placing a simulated buy or sell order, and managing positions without writing code. Use Quanta branding, typography, and themes throughout.

This is a new learner-facing terminal. The existing small paper-order calculator in the research lab is a starting point for execution logic; it does not satisfy this requirement. Section 5.3 describes the broader execution-engine vision. The release scope below determines which capabilities the new terminal must initially expose.

#### 6.3.1 First-Release Scope & Learner Journey

* **Entry points:** Add **Trading simulator** to the main navigation and links from the beginner lessons on orders, returns, risk, and the paper-trading plan. The terminal must also work independently of lesson completion.
* **Default account:** Start with a virtual $100,000 USD cash account, whole shares, and long-only buy/sell trading. Show **Paper trading** persistently. Advanced margin, short selling, and bot execution remain subsequent releases under Section 5.3.
* **Market modes:** Support seeded synthetic markets and replay of installed historical stock datasets. Clearly display the mode, data source, interval, and simulation timestamp. Live or delayed feeds require a configured provider and are a later enhancement; neither synthetic nor replay prices may be labeled live.
* **Primary journey:** Open the terminal → choose a stock from search or the watchlist → inspect candles and indicators → open Buy/Sell → preview and place an order → follow its status and chart marker → review or close the position → inspect P&L and trade history.
* **Delivery sequence:** First deliver the chart workspace, then connect persistent paper orders and portfolio accounting, then complete replay, lesson integration, accessibility, and the acceptance scenarios in Section 6.3.5. The first release requires all three steps.

#### 6.3.2 Workspace Layout

Use the available viewport as a trading workspace, with a compact top toolbar, a narrow drawing toolbar on the left, the chart in the center, a watchlist/order-ticket sidebar on the right, and a resizable trading panel below the chart. Collapse the standard LMS sidebar while the terminal is open, while keeping an obvious way back to the learning workspace.

```text
+-----------------------------------------------------------------------------------------------------+
| QUANTA | Trading simulator | PAPER TRADING | Equity $100,000 | Cash $100,000 | Theme | Back to LMS  |
+-------+-------------------------------------------------------------------+-------------------------+
| Draw  | AAPL v | 1m 5m 15m 1h 1D | Candles v | Indicators | Replay | Full | WATCHLIST               |
+-------+-------------------------------------------------------------------+-------------------------+
| Cross | AAPL - Historical replay - As of [date/time] - O H L C            | Symbol   Last   Change  |
| Trend |                                                                   | AAPL     ...     ...    |
| H-line|                         MAIN PRICE CHART                          | MSFT     ...     ...    |
| Rect  |                candles, crosshair, price/time axes                | NVDA     ...     ...    |
| Text  |           position and working-order price lines                  | [+ Add symbol]          |
| Ruler |                                                                   |-------------------------|
| Erase |                                                                   | [BUY] [SELL]            |
|       | Volume histogram / optional RSI or MACD pane                      | Type: [Limit v]         |
|       | [Pause/Play] [Next bar] [Speed] [Simulation clock]                | Shares: [10]            |
|       |                                                                   | Limit: [$...]           |
|       |                                                                   | Est. total / fees       |
|       |                                                                   | [Preview order]         |
+-------+-------------------------------------------------------------------+-------------------------+
| [Positions] [Open orders] [Order history] [Trade history] [Account history]                         |
| Symbol | Quantity | Average entry | Last price | Market value | Unrealized P&L | Close / Reduce     |
+-----------------------------------------------------------------------------------------------------+
```

The chart is the dominant visual element. On a 1440 × 900 desktop viewport, its region must occupy at least 60% of the workspace width and 50% of the usable height with the default panels open. Watchlist and trading-panel sizes must be adjustable and collapsible. Avoid a dashboard of summary cards around a small chart.

#### 6.3.3 Required Terminal Features

| ID | Area | First-release requirement |
| :--- | :--- | :--- |
| **SIM-01** | Symbol search & watchlist | Search available stocks by ticker or company name; add, remove, and reorder watchlist entries. Show last available price, absolute change, percentage change, and data timestamp. Selecting a symbol synchronizes the chart and ticket. Missing prices display as unavailable, never zero. |
| **SIM-02** | Chart interaction | Provide candlestick, OHLC bar, and line views; mouse-wheel zoom, drag-to-pan, crosshair with price/time labels, OHLC/volume readout, auto-fit, and return-to-latest controls. Support touch pan/zoom. Changing symbols must not alter open orders or positions. |
| **SIM-03** | Timeframes | Offer 1m, 5m, 15m, 1h, and 1D when supported by the selected data. Disable unsupported intervals with an explanation. Aggregate only from sufficiently granular data; daily OHLCV must not be presented as observed intraday prices. |
| **SIM-04** | Drawing tools | Include trend line, horizontal line, rectangle, text annotation, and a price/percentage measurement tool. Learners can select, move, edit, lock, and delete drawings, with undo/redo. Save drawings per symbol and dataset/run context. |
| **SIM-05** | Indicators | Include configurable SMA, EMA, volume, RSI, and MACD. Allow adding, hiding, editing parameters, and removing indicators, using separate lower panes where appropriate. Explain insufficient warm-up data and calculate from observations available at the simulation clock. |
| **SIM-06** | Order ticket | Provide clear Buy/Sell tabs, quantity, Market/Limit/Stop/Stop-limit selection, required prices, and DAY/GTC duration. Preview estimated notional, costs, available cash/shares, and resulting exposure before explicit submission. Disable invalid orders and explain the reason next to the relevant field. |
| **SIM-07** | Trading on the chart | Show entry/fill markers, the current position's average entry, and labeled working-order lines. A chart context menu can open a ticket at the selected price. Dragging an order line previews an amendment and requires confirmation; a rejected amendment restores the confirmed line and order values. Provide equivalent form controls. |
| **SIM-08** | Portfolio & history | Provide bottom tabs for Positions, Open orders, Order history, Trade history, and Account history. Show filled/remaining quantities, order status, fill prices, costs, average cost, market value, and realized/unrealized P&L. Selecting a row opens its symbol on the chart. |
| **SIM-09** | Position management | Support canceling working orders and reducing or closing a position through a prefilled ticket. Preview quantity and costs; a close request remains pending until filled. Do not remove positions or mark orders filled merely because a request was accepted. |
| **SIM-10** | Market replay | Provide pause, play, next-bar, and speed controls with one simulation clock across chart, quotes, orders, and account valuation. Pausing stops market advancement while allowing order entry/cancellation. Restarting or moving backward creates a new run with fresh balances and preserves the prior run for review. |
| **SIM-11** | Saved workspace | Save selected symbol, watchlist, interval, indicators, drawings, panel layout, and theme. Signed-in users recover their account, working orders, fills, and trade journal after reload or sign-in on another device. Keep simulator accounts separate from lesson progress and experiment snapshots. |
| **SIM-12** | Learning & review | Offer a short optional first-trade walkthrough and contextual links to the beginner lessons. Allow a thesis/reason and lesson link on each trade journal entry. Export orders, fills, and account history as CSV, and export run configuration and journal as JSON. Learning credit rewards correct process and explanations, not profit alone. |

#### 6.3.4 Execution, Recovery & Interface Requirements

* **Consistent execution:** The manual terminal and future Python client must share the account and order service. Use persistent account-owned records and a server-authoritative cash/position ledger for signed-in trading. A browser must not supply its own accepted balance, fill price, or P&L. Retry the same order with a stable client identifier so double-clicks or lost responses do not create duplicate trades.
* **Cash and shares:** Reserve available cash, including estimated costs, for open buy orders and reserve shares for open sell orders. Revalidate affordability at execution; price gaps must not create unintended borrowing. Canceling or expiring an order releases only its unfilled reservation. Reject selling more unreserved shares than the account holds.
* **Fill assumptions:** Display the execution model and configured spread, slippage, commissions, and liquidity limits. In bar replay, orders placed after a bar closes become eligible on the next bar. Define gap handling, stop triggers, partial fills, and a deterministic conservative rule when a bar touches multiple order levels. A price touch must not imply guaranteed execution or unlimited liquidity. Level 2 queues must only be shown for datasets or synthetic models that provide depth.
* **Accounting:** Specify cost-basis and fee-allocation conventions, use decimal monetary arithmetic, and reconcile every fill to cash, position quantity, and realized P&L. Display available cash separately from reserved cash. The initial synthetic teaching profile uses immediate settlement and labels that simplification; market-specific settlement, margin, borrowing, and fee schedules belong to explicitly versioned profiles before they are offered. Historical datasets must declare corporate-action treatment so splits or dividends are neither omitted without disclosure nor counted twice.
* **Connection states:** Show loading, empty watchlist, unavailable symbol, market closed, replay complete, stale data, disconnected, pending, rejected, and recovered states. On reconnect, reconcile confirmed orders and fills before permitting another retry. Preserve the ticket draft during request failures. Do not invent fills while required data or execution services are unavailable.
* **Account reset:** Resetting creates a new simulation account/run after confirmation and leaves prior history available for review/export. Signing out isolates account data; it must not copy positions, balances, or pending responses into a guest workspace. A guest preview may use a separately labeled device-only account.
* **Visual system:** Use compact toolbars, thin panel dividers, aligned numeric columns, restrained chart gridlines, and the existing Quanta light/dark themes. Reserve directional colors for market information and accompany them with text or symbols. Buttons, chart tools, and status labels need accessible names and visible keyboard focus.
* **Responsive behavior:** At tablet widths, collapse the watchlist and ticket into a drawer. At 390-pixel mobile width, provide Chart, Watchlist, Trade, and Portfolio views with a sticky Buy/Sell entry point. The page must not overflow horizontally; dense history tables may scroll within their own container. Trading must remain possible without dragging chart elements.
* **Performance targets:** With 5,000 loaded bars and three enabled indicators, target p95 chart pan/zoom frame time below 33 ms on a documented reference desktop. Target p95 order acknowledgement below 500 ms on the documented local deployment, measured separately from waiting for a fill. Record hardware, dataset, concurrency, and measurement method with the release results.

#### 6.3.5 Acceptance Criteria

| ID | Scenario | Required result |
| :--- | :--- | :--- |
| **SIM-AC-01** | Open the new terminal from navigation or a beginner lesson. | `/simulator` displays the chart-first layout, drawing toolbar, right watchlist/ticket, bottom trading panel, and persistent paper-trading/data-mode labels. Desktop and mobile layouts satisfy Section 6.3.4. |
| **SIM-AC-02** | Select another stock, change an available timeframe, add an indicator, and draw a trend line. | Chart, readout, and ticket stay synchronized. Saved settings and drawings survive reload and remain associated with the correct symbol and run. Unsupported intervals cannot be selected. |
| **SIM-AC-03** | With $100,000 cash, buy 10 shares filled at $100 with a $1 fee; later sell all 10 at $110 with a $1 fee, with no other costs or cash flows. | Cash becomes $98,999 after entry and $100,098 after exit; the position closes and net realized P&L is $98. The chart and all history tabs agree with the ledger. |
| **SIM-AC-04** | Place a nonmarketable limit order, advance replay, partially fill it, then cancel the remainder. | The order remains working until eligible liquidity arrives. Filled quantity is retained, the canceled remainder cannot execute, and only unused cash or shares are released. |
| **SIM-AC-05** | Place a stop and replay a gap; also submit an order after viewing a completed candle. | Gap fills follow the documented model rather than the requested stop price. Newly submitted orders never fill in the already-observed candle. Future bars and indicator values are not exposed before the simulation clock. |
| **SIM-AC-06** | Retry an order after its server response is lost; reload, disconnect/reconnect, and open the same account on another device. | Exactly one economic order exists, confirmed fills and balances recover, pending drafts remain understandable, and another learner or guest cannot access the account. |
| **SIM-AC-07** | Try overspending, overselling, a rejected chart amendment, and a full account reset. | Invalid actions leave confirmed orders and balances unchanged. Reset produces a fresh run while prior history remains accessible and lesson/exam progress is preserved. |
| **SIM-AC-08** | Complete a manual buy/reduce/close workflow using keyboard controls and at mobile width. | Every action has an accessible form/control equivalent; the learner can reach and read order feedback, positions, and trade history without page-level horizontal scrolling. |

**Implementation status (September 14, 2026):** The first-release terminal is implemented at `/simulator`. See the [simulator guide and actual API contract](docs/SIMULATOR.md) and [acceptance and performance verification](docs/VERIFICATION.md).

**Subsequent releases:** Multi-chart layouts, custom indicators, server-side price alerts, licensed live/delayed feeds, Level 2 DOM, bracket/OCO and trailing orders, realistic margin/short borrowing, TWAP/VWAP, and Python bot control. These extend the new terminal after the first-release acceptance criteria pass.

---

## 7. REST & WebSocket API Specification

All backend endpoints are built using FastAPI with strict Pydantic v2 schemas and automated OpenAPI documentation.

### 7.1 Core Endpoints & Route Definitions

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | Register new student profile | No |
| `POST` | `/api/v1/auth/token` | OAuth2 Password Bearer JWT login | No |
| `GET` | `/api/v1/curriculum/tracks` | Fetch all 6 tracks with chapter hierarchies | Yes |
| `GET` | `/api/v1/curriculum/sections/{section_id}` | Fetch lecture content, math blocks, and code template | Yes |
| `POST` | `/api/v1/sandbox/execute` | Run user Python code in isolated sandbox | Yes |
| `POST` | `/api/v1/synthetic/generate` | Generate counterfactual stochastic price series | Yes |
| `POST` | `/api/v1/submissions/grade` | Run automated grading assertions on student exercise | Yes |
| `GET` | `/api/v1/market/point-in-time-fs` | Query point-in-time balance sheets and income statements | Yes |
| `POST` | `/api/v1/simulator/orders` | Submit paper trading order (Market, Limit, Stop, Bracket, TWAP) | Yes |
| `GET` | `/api/v1/simulator/orders` | Retrieve active working orders and execution history | Yes |
| `DELETE` | `/api/v1/simulator/orders/{order_id}` | Cancel pending or resting limit order | Yes |
| `GET` | `/api/v1/simulator/positions` | Query current active portfolio holdings and mark-to-market PnL | Yes |
| `POST` | `/api/v1/simulator/positions/{symbol}/close` | Market-liquidate or cover specific active position | Yes |
| `GET` | `/api/v1/simulator/account` | Retrieve cash balance, equity, buying power, and margin state | Yes |
| `POST` | `/api/v1/simulator/account/reset` | Reset paper trading account balance to initial cash | Yes |
| `WS` | `/api/v1/market/stream/{symbol}` | WebSocket live order book and tick streaming | Yes |
| `WS` | `/api/v1/simulator/stream/{account_id}` | WebSocket live order fills, trade blotter, and margin call events | Yes |

---

### 7.2 Request & Response Schemas (Pydantic Models)

#### 7.2.1 Sandbox Execution Contract
```python
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class DatasetConfig(BaseModel):
    mode: str = Field(description="'real' or 'synthetic'")
    ticker: Optional[str] = Field(default=None, description="Required for real mode (e.g. 'AAPL')")
    start_date: Optional[str] = Field(default=None, description="ISO format 'YYYY-MM-DD'")
    end_date: Optional[str] = Field(default=None, description="ISO format 'YYYY-MM-DD'")
    synthetic_model: Optional[str] = Field(default=None, description="'gbm', 'merton_jump', 'heston', 'markov'")
    synthetic_params: Optional[Dict[str, float]] = None

class PortfolioConfig(BaseModel):
    initial_cash: float = 100000.0
    commission_bps: float = 5.0
    slippage_model: str = Field(default="square_root", description="'zero', 'fixed', or 'square_root'")

class SandboxExecuteRequest(BaseModel):
    section_id: str
    code: str
    dataset: DatasetConfig
    portfolio: PortfolioConfig

class PerformanceMetrics(BaseModel):
    cagr: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    alpha: float
    beta: float
    var_95: float
    cvar_95: float
    deflated_sharpe_ratio: float

class SandboxExecuteResponse(BaseModel):
    status: str = Field(description="'success' or 'error'")
    execution_time_ms: float
    stdout: str
    stderr: Optional[str] = None
    metrics: Optional[PerformanceMetrics] = None
    equity_curve: List[float] = []
    timestamps: List[str] = []
    trade_log: List[Dict[str, Any]] = []
```

#### 7.2.2 Automated Exercise Grading Contract
```python
class GradeSubmissionRequest(BaseModel):
    exercise_id: str
    code: str

class TestResult(BaseModel):
    test_name: str
    passed: bool
    expected: Any
    actual: Any
    feedback: str

class GradeSubmissionResponse(BaseModel):
    exercise_id: str
    passed: bool
    score: float
    max_score: float
    test_results: List[TestResult]
    instructor_notes: str

#### 7.2.3 Synthetic Market Generator Contract
class SyntheticGenerateRequest(BaseModel):
    model: str = Field(description="'gbm', 'merton_jump', 'heston', 'markov', 'uniswap_v3'")
    s0: float = Field(default=100.0, description="Initial asset price")
    t_years: float = Field(default=1.0, description="Time horizon in years")
    steps: int = Field(default=252, description="Discretization time steps")
    params: Dict[str, float] = Field(description="Model-specific parameters (e.g. mu, sigma, kappa)")

class SyntheticGenerateResponse(BaseModel):
    model: str
    timestamps: List[int]
    prices: List[float]
    variances: Optional[List[float]] = None
    regimes: Optional[List[int]] = None
    summary_stats: Dict[str, float]

#### 7.2.4 Point-in-Time SEC Financials Query Contract
class FinancialStatementQueryRequest(BaseModel):
    ticker: str
    as_of_date: str = Field(description="ISO format 'YYYY-MM-DD' strictly filtering filings accepted prior")
    statement_type: str = Field(description="'balance_sheet', 'income_statement', or 'cash_flow'")
    lookback_periods: int = Field(default=5, description="Number of historical annual/quarterly reports")

class FinancialStatementQueryResponse(BaseModel):
    ticker: str
    as_of_date: str
    filings: List[Dict[str, Any]]

#### 7.2.5 Interactive Stock Simulator Order & Account Contracts
class SimulatorOrderCreateRequest(BaseModel):
    symbol: str
    side: str = Field(description="'BUY' or 'SELL'")
    order_type: str = Field(description="'MARKET', 'LIMIT', 'STOP_LOSS', 'STOP_LIMIT', 'TRAILING_STOP', 'BRACKET', 'TWAP'")
    quantity: float = Field(gt=0, description="Number of shares to trade")
    limit_price: Optional[float] = Field(default=None, description="Required for LIMIT and STOP_LIMIT")
    stop_price: Optional[float] = Field(default=None, description="Trigger price for STOP_LOSS and STOP_LIMIT")
    trailing_delta: Optional[float] = Field(default=None, description="Trailing distance in dollars or percentage")
    take_profit_price: Optional[float] = Field(default=None, description="OCO target price for BRACKET orders")
    stop_loss_price: Optional[float] = Field(default=None, description="OCO stop price for BRACKET orders")
    time_in_force: str = Field(default="GTC", description="'DAY', 'GTC', 'IOC', 'FOK'")
    twap_duration_minutes: Optional[int] = Field(default=None, description="Slicing duration for TWAP execution")

class SimulatorOrderResponse(BaseModel):
    order_id: str
    symbol: str
    side: str
    order_type: str
    quantity: float
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    status: str
    filled_quantity: float
    avg_fill_price: float
    commission: float
    slippage: float
    created_at: str

class SimulatorPositionResponse(BaseModel):
    symbol: str
    quantity: float
    avg_entry_price: float
    current_mark_price: float
    market_value: float
    unrealized_pnl: float
    unrealized_pnl_pct: float
    realized_pnl: float
    borrow_rate_apr: float

class SimulatorAccountSummaryResponse(BaseModel):
    account_id: str
    cash_balance: float
    portfolio_equity: float
    long_market_value: float
    short_market_value: float
    initial_margin_requirement: float
    maintenance_margin_requirement: float
    maintenance_excess: float
    buying_power: float
    margin_utilization_pct: float
    is_margin_call: bool
    day_pnl: float
```

---

### 7.3 Real-Time WebSocket Streaming Protocol

For live interactive coding labs, bot paper trading, and high-frequency order book visualization, the backend provides an asynchronous WebSocket connection at `/api/v1/market/stream`.

#### 7.3.1 Client-to-Server JSON Frame Protocol

```json
// 1. Subscribe to Bar Feed
{
  "action": "subscribe",
  "channel": "bars",
  "symbol": "AAPL",
  "timeframe": "1m"
}

// 2. Subscribe to Level 2 Order Book Depth
{
  "action": "subscribe",
  "channel": "orderbook_l2",
  "symbol": "BTC/USDT",
  "depth": 20
}

// 3. Submit Bot Execution Order
{
  "action": "place_order",
  "client_order_id": "bot_alpha_001_1726239100",
  "symbol": "ETH/USDC",
  "side": "BUY",
  "order_type": "LIMIT",
  "quantity": 2.5,
  "limit_price": 2845.50,
  "time_in_force": "GTC"
}

// 4. Cancel Existing Order
{
  "action": "cancel_order",
  "order_id": "ord_a9f82c"
}

// 5. Subscribe to Simulator Account Updates
{
  "action": "subscribe",
  "channel": "simulator_account",
  "account_id": "sim_88219"
}
```

#### 7.3.2 Server-to-Client Streaming Events

```json
// 1. Real-Time Bar Event
{
  "event": "bar",
  "symbol": "AAPL",
  "timestamp": 1726239120,
  "open": 224.50,
  "high": 224.85,
  "low": 224.30,
  "close": 224.75,
  "volume": 14250.0
}

// 2. Level 2 Book Snapshot / Delta
{
  "event": "book_l2",
  "symbol": "BTC/USDT",
  "timestamp": 1726239120150,
  "bids": [
    [58420.50, 1.45],
    [58419.00, 3.20],
    [58418.50, 0.85]
  ],
  "asks": [
    [58421.00, 0.95],
    [58422.50, 2.10],
    [58423.00, 5.00]
  ]
}

// 3. Execution Fill Report
{
  "event": "execution_fill",
  "order_id": "ord_a9f82c",
  "client_order_id": "bot_alpha_001_1726239100",
  "symbol": "ETH/USDC",
  "side": "BUY",
  "filled_quantity": 2.5,
  "fill_price": 2845.48,
  "slippage_bps": 0.07,
  "commission_usd": 3.55,
  "timestamp": 1726239121040,
  "status": "FILLED"
}

// 4. Circuit Breaker Warning / Kill-Switch Event
{
  "event": "circuit_breaker",
  "severity": "CRITICAL",
  "rule_triggered": "MAX_INTRADAY_DRAWDOWN",
  "portfolio_equity": 97420.00,
  "drawdown_pct": 0.0258,
  "action_taken": "ALL_ORDERS_CANCELED_POSITIONS_LIQUIDATED",
  "timestamp": 1726239125000
}

// 5. Simulator Margin Call & Liquidation Notice Event
{
  "event": "simulator_margin_alert",
  "account_id": "sim_88219",
  "severity": "WARNING",
  "maintenance_excess": -3420.50,
  "portfolio_equity": 21500.00,
  "maintenance_requirement": 24920.50,
  "liquidation_deadline_utc": "2026-09-13T16:00:00Z",
  "message": "Maintenance excess negative. Deposit funds or trim positions to prevent involuntary liquidation."
}
```

---

## 8. Relational Database Schema & Data Models

The persistence layer uses SQLModel, allowing identical class definitions to serve as both SQLAlchemy ORM models and Pydantic validation schemas.

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class Student(SQLModel, table=True):
    __tablename__ = "students"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    submissions: List["Submission"] = Relationship(back_populates="student")
    notebooks: List["SavedNotebook"] = Relationship(back_populates="student")

class Track(SQLModel, table=True):
    __tablename__ = "tracks"
    id: str = Field(primary_key=True)  # e.g. 'cbs-fin-601'
    track_number: int
    title: str
    academic_code: str  # e.g. 'CBS-FIN 601'
    description: str

class Chapter(SQLModel, table=True):
    __tablename__ = "chapters"
    id: str = Field(primary_key=True)  # e.g. 'track1_ch2'
    track_id: str = Field(foreign_key="tracks.id")
    chapter_number: int
    title: str

class Section(SQLModel, table=True):
    __tablename__ = "sections"
    id: str = Field(primary_key=True)  # e.g. 'track1_ch2_sec2'
    chapter_id: str = Field(foreign_key="chapters.id")
    section_number: int
    title: str
    content_markdown: str
    default_code_template: str

class Exercise(SQLModel, table=True):
    __tablename__ = "exercises"
    id: str = Field(primary_key=True)
    section_id: str = Field(foreign_key="sections.id")
    prompt: str
    test_suite_code: str  # Secret unit test assertions executed in sandbox
    max_points: float = 100.0

class Submission(SQLModel, table=True):
    __tablename__ = "submissions"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    student_id: uuid.UUID = Field(foreign_key="students.id")
    exercise_id: str = Field(foreign_key="exercises.id")
    submitted_code: str
    score: float
    passed: bool
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    
    student: Optional[Student] = Relationship(back_populates="submissions")

class SavedNotebook(SQLModel, table=True):
    __tablename__ = "saved_notebooks"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    student_id: uuid.UUID = Field(foreign_key="students.id")
    section_id: str = Field(foreign_key="sections.id")
    saved_code: str
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    student: Optional[Student] = Relationship(back_populates="notebooks")

class FinancialStatementPointInTime(SQLModel, table=True):
    __tablename__ = "financial_statements_pit"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    ticker: str = Field(index=True)
    fiscal_period: str  # e.g. 'FY2021' or 'Q3-2022'
    period_end_date: datetime
    sec_filing_date: datetime = Field(index=True)  # STRICT point-in-time acceptance date
    form_type: str  # '10-K' or '10-Q'
    
    # Balance Sheet Items
    cash_and_equivalents: float
    receivables: float
    inventory: float
    total_current_assets: float
    property_plant_equipment: float
    goodwill_and_intangibles: float
    total_assets: float
    current_liabilities: float
    short_term_debt: float
    long_term_debt: float
    total_liabilities: float
    preferred_stock: float
    shareholders_equity: float
    
    # Income Statement Items
    revenue: float
    cost_of_goods_sold: float
    gross_profit: float
    sga_expense: float
    operating_expenses: float
    operating_income_ebit: float
    interest_expense: float
    income_tax_expense: float
    net_income: float
    diluted_eps: float
    shares_outstanding: float
    
    # Cash Flow Items
    operating_cash_flow: float
    capital_expenditures: float
    free_cash_flow: float
    dividends_paid: float

class DailyPriceBar(SQLModel, table=True):
    __tablename__ = "daily_price_bars"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    ticker: str = Field(index=True)
    trade_date: datetime = Field(index=True)
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
    adjusted_close: float
    split_factor: float = 1.0
    dividend_amount: float = 0.0

class CryptoFundingRateRecord(SQLModel, table=True):
    __tablename__ = "crypto_funding_rates"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    exchange: str = Field(index=True)  # 'binance', 'bybit', 'dydx'
    symbol: str = Field(index=True)    # 'BTCUSDT', 'ETHUSDT'
    funding_time: datetime = Field(index=True)
    funding_rate_8h: float
    mark_price: float
    index_price: float

class PaperTradingAccount(SQLModel, table=True):
    __tablename__ = "paper_trading_accounts"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    student_id: uuid.UUID = Field(foreign_key="students.id", index=True)
    account_number: str = Field(unique=True, index=True)
    account_type: str = Field(default="MARGIN")  # 'MARGIN' or 'CASH'
    cash_balance: float = Field(default=100000.0)
    portfolio_equity: float = Field(default=100000.0)
    margin_multiplier: float = Field(default=2.0)
    buying_power: float = Field(default=200000.0)
    maintenance_requirement: float = Field(default=0.0)
    maintenance_excess: float = Field(default=100000.0)
    is_margin_call: bool = Field(default=False)
    margin_call_deadline: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PaperOrder(SQLModel, table=True):
    __tablename__ = "paper_orders"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    account_id: uuid.UUID = Field(foreign_key="paper_trading_accounts.id", index=True)
    client_order_id: str = Field(index=True)
    symbol: str = Field(index=True)
    side: str  # 'BUY', 'SELL', 'SHORT', 'COVER'
    order_type: str  # 'MARKET', 'LIMIT', 'STOP_LOSS', 'STOP_LIMIT', 'TRAILING_STOP', 'BRACKET', 'TWAP'
    quantity: float
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    trailing_delta: Optional[float] = None
    take_profit_price: Optional[float] = None
    stop_loss_price: Optional[float] = None
    time_in_force: str = "GTC"
    status: str = "PENDING"  # 'PENDING', 'FILLED', 'PARTIALLY_FILLED', 'CANCELED', 'REJECTED'
    filled_quantity: float = 0.0
    average_fill_price: float = 0.0
    commission_paid: float = 0.0
    slippage_incurred: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    filled_at: Optional[datetime] = None

class PaperPosition(SQLModel, table=True):
    __tablename__ = "paper_positions"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    account_id: uuid.UUID = Field(foreign_key="paper_trading_accounts.id", index=True)
    symbol: str = Field(index=True)
    quantity: float  # Positive for long, negative for short
    average_entry_price: float
    current_mark_price: float
    market_value: float
    unrealized_pnl: float
    realized_pnl: float = 0.0
    borrow_rate_apr: float = 0.0  # Annualized borrow cost for shorted equities
    accumulated_borrow_fees: float = 0.0
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PaperTradeFill(SQLModel, table=True):
    __tablename__ = "paper_trade_fills"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    order_id: uuid.UUID = Field(foreign_key="paper_orders.id", index=True)
    account_id: uuid.UUID = Field(foreign_key="paper_trading_accounts.id", index=True)
    symbol: str = Field(index=True)
    side: str
    fill_price: float
    fill_quantity: float
    commission: float
    sec_taf_fees: float
    slippage_bps: float
    realized_pnl: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MarginLedgerEntry(SQLModel, table=True):
    __tablename__ = "margin_ledger_entries"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    account_id: uuid.UUID = Field(foreign_key="paper_trading_accounts.id", index=True)
    entry_type: str  # 'DEPOSIT', 'WITHDRAWAL', 'TRADE_FILL', 'BORROW_FEE', 'DIVIDEND_ADJUSTMENT', 'LIQUIDATION'
    amount: float
    resulting_cash: float
    resulting_equity: float
    description: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SimulationRunRecord(SQLModel, table=True):
    __tablename__ = "simulation_runs"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    student_id: uuid.UUID = Field(foreign_key="students.id")
    section_id: str = Field(foreign_key="sections.id")
    dataset_mode: str  # 'real' or 'synthetic'
    execution_duration_ms: float
    sharpe_ratio: Optional[float] = None
    cagr: Optional[float] = None
    max_drawdown: Optional[float] = None
    deflated_sharpe_ratio: Optional[float] = None
    ran_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## 9. Security, AST Sandboxing & Production DevOps

### 9.1 The Python AST Security Validator
To guarantee that arbitrary user code execution cannot compromise the host environment or escape execution boundaries, code is analyzed via an Abstract Syntax Tree (AST) visitor before compilation.

```python
import ast

class SecurityViolation(Exception):
    pass

class QuantaSecurityASTVisitor(ast.NodeVisitor):
    FORBIDDEN_MODULES = {
        'os', 'sys', 'subprocess', 'socket', 'shutil', 'ctypes', 'pty',
        'requests', 'urllib', 'http', 'posix', 'builtins'
    }
    FORBIDDEN_BUILTINS = {'eval', 'exec', '__import__', 'compile', 'open'}

    def visit_Import(self, node):
        for alias in node.names:
            module_root = alias.name.split('.')[0]
            if module_root in self.FORBIDDEN_MODULES:
                raise SecurityViolation(f"Illegal module import detected: {alias.name}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            module_root = node.module.split('.')[0]
            if module_root in self.FORBIDDEN_MODULES:
                raise SecurityViolation(f"Illegal module import detected: {node.module}")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in self.FORBIDDEN_BUILTINS:
                raise SecurityViolation(f"Forbidden builtin call detected: {node.func.id}()")
        self.generic_visit(node)

def validate_student_code(code_str: str) -> None:
    tree = ast.parse(code_str)
    visitor = QuantaSecurityASTVisitor()
    visitor.visit(tree)
```

### 9.2 OS Resource Limiting (Linux cgroups / prlimit)
```python
import resource

def set_sandbox_resource_limits():
    # 2.0 seconds CPU time maximum
    resource.setrlimit(resource.RLIMIT_CPU, (2, 2))
    # 256 MB maximum resident set size (RAM)
    max_memory = 256 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (max_memory, max_memory))
    # Disable creation of core dumps
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    # Disable child subprocess forking
    resource.setrlimit(resource.RLIMIT_NPROC, (1, 1))
```

### 9.3 Containerized Architecture (`docker-compose.yml`)
```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://quanta:quanta_secret@postgres:5432/quanta_db
      - REDIS_URL=redis://redis:6379/0
      - PARQUET_DATA_PATH=/data/market_parquet
    volumes:
      - market_data:/data/market_parquet:ro
    depends_on:
      - postgres
      - redis

  sandbox-worker:
    build:
      context: .
      dockerfile: Dockerfile.sandbox
    network_mode: none  # Absolute network egress isolation
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp:size=32M,noexec,nosuid
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 512M

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: quanta
      POSTGRES_PASSWORD: quanta_secret
      POSTGRES_DB: quanta_db
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
  market_data:
```

---

## 10. 18-Week Academic Implementation Roadmap & Milestones

The platform is designed to be built across an 18-week engineering cycle broken into three 6-week semesters:

```
                                      18-WEEK IMPLEMENTATION TIMELINE
+-----------------------------+------------------------------------+------------------------------------+
|   SEMESTER 1: WEEKS 1–6     |       SEMESTER 2: WEEKS 7–12       |      SEMESTER 3: WEEKS 13–18       |
+-----------------------------+------------------------------------+------------------------------------+
| W1-2: Core LMS & Dual-Pane  | W7-8: Synthetic Market Generators  | W13-14: Event Bot Core & Almgren   |
| W3-4: Point-in-Time Parquet | W9-10: Econometrics (ARIMA/GARCH)  | W15-16: ML Alpha & LLM Committee   |
| W5-6: Track 1 (Sec Analysis)| W11-12: MPT, Factors & Track 3/4   | W17-18: Web3/Crypto Track 6 & Audit|
+-----------------------------+------------------------------------+------------------------------------+
```

### Semester 1: Foundations & Classical Valuation (Weeks 1–6)
* **Week 1–2: Framework Architecture & Dual-Pane UI**
  * Scaffold FastAPI asynchronous backend with SQLModel and JWT authentication.
  * Build React 18+ frontend using Vite, Tailwind CSS, KaTeX LaTeX math parser, and Monaco editor.
  * Implement split-screen resizable reading/coding panels with independent scroll locks.
* **Week 3–4: Point-in-Time Data Pipeline & DuckDB Integration**
  * Curate, clean, and convert 30 years of US equity daily OHLCV and SEC 10-K/10-Q statements into columnar Parquet format.
  * Index all financial statement tables strictly by SEC filing acceptance timestamps to eliminate look-ahead bias.
  * Integrate embedded DuckDB within FastAPI for low-latency SQL querying of multi-decade time series.
* **Week 5–6: Track 1 Authoring (Chapters 1–5: Security Analysis)**
  * Author interactive lecture notes, derivations, and historical case studies for Chapters 1 through 5.
  * Implement automated testing suites for Graham Net-Net, Altman Z-Score, and Greenwald EPV exercises.

### Semester 2: Econometrics, Factor Models & Strategy Lab (Weeks 7–12)
* **Week 7–8: Stochastic Market Generators & Charting Engine**
  * Implement the 4 mathematical market generators: GBM, Merton Jump-Diffusion, Heston Volatility, Markov Regimes.
  * Embed TradingView Lightweight Charts in React to render interactive candles, volumes, and trade execution markers.
  * Deploy AST security filter and Linux resource limits to guarantee secure student code execution.
* **Week 9–10: Time-Series Econometrics & Track 2 (Chapters 6–10)**
  * Implement Statsmodels calculation pipeline: ADF tests, AIC/BIC model selectors, GARCH MLE fitting, and López de Prado fractional differentiation.
  * Author complete content and labs for Track 2 (Statistical Foundations of Finance).
* **Week 11–12: Multi-Factor Portfolios & Strategy Lab (Chapters 11–18)**
  * Build Fama-French 5-factor attribution engine, Ledoit-Wolf covariance shrinkage, and Deflated Sharpe Ratio (DSR) auditor.
  * Author Track 3 (Advanced Econometrics) and Track 4 (The Strategy Lab).

### Semester 3: Autonomous AI Bots & Web3 Cryptoeconomics (Weeks 13–18)
* **Week 13–14: Event-Driven Trading Engine & Optimal Execution (Chapters 19–20)**
  * Build an asynchronous event-driven Mock Broker in FastAPI with Level 2 order books and realistic queue slippage.
  * Implement Almgren-Chriss optimal liquidation algorithms and TWAP/VWAP execution runners.
* **Week 15–16: Machine Learning Alpha & Multi-Agent LLM Committee (Chapters 21–23)**
  * Implement Purged K-Fold XGBoost tabular ranking engine.
  * Construct LangChain/LlamaIndex multi-agent forensic accounting auditor analyzing SEC 10-K filings with Pydantic guardrails.
  * Author complete content and labs for Track 5 (Stock Bots & AI Systems).
* **Week 17–18: Web3, Tokenomics & Crypto Bot Systems (Chapters 24–28)**
  * Build Uniswap v3 concentrated liquidity simulator and LVR backtester.
  * Ingest crypto spot, perpetual futures funding rates, and construct Web3.py execution templates.
  * Author Track 6 curriculum, perform end-to-end load testing, security auditing, and public platform release.

---

## 11. Academic Verification, Grading Rubrics & Quality Assurance

### 11.1 Automated Grading Pipeline & Assertion Matrix
Every computational lab includes a hidden test harness executed server-side. For a student to receive credit and unlock subsequent chapters, their code must satisfy three rigorous criteria:

```
+---------------------------------------------------------------------------------------------------+
|                                  GRADING VERIFICATION CRITERIA                                    |
+------------------------------+------------------------------+-------------------------------------+
| 1. Mathematical Correctness  | 2. Statistical Significance  | 3. Execution Hygiene                |
+------------------------------+------------------------------+-------------------------------------+
| Exact parity with textbook   | Strategy must reject null    | Zero look-ahead bias (strictly      |
| formulas (NCAV, duration,    | hypothesis ($p < 0.05$) after | point-in-time filing dates);        |
| GARCH, Kelly criterion)      | Benjamini-Hochberg & DSR     | realistic slippage & fee accounting |
+------------------------------+------------------------------+-------------------------------------+
```

### 11.2 Grading Rubric Example: Chapter 16 (Deflated Sharpe Ratio Lab)
* **Test 1 (Mathematical Parity)**: The calculated Sharpe ratio on sample data must match `scipy.stats` benchmark within $10^{-6}$ tolerance.
* **Test 2 (Skewness & Kurtosis Adjustment)**: Verify that negatively skewed return distributions correctly penalize the Probabilistic Sharpe Ratio (PSR).
* **Test 3 (Multiple Testing Penalty)**: Verify that when trial count $K$ increases from 1 to 100, the Deflated Sharpe Ratio decreases monotonically, correctly rejecting false-positive alphas.

### 11.3 Educational Efficacy & Graduation Standards
* **Institutional Benchmark**: Quanta's graduation standard requires students to pass all 28 chapter labs, culminating in a capstone project: deploying an autonomous stock bot or Web3 arbitrage strategy that generates statistically verifiable alpha across out-of-sample empirical data and counterfactual stress regimes.
* **Open Reproducibility**: All course lecture notes, derivations, and backtest codes are exportable to standalone Jupyter Notebooks with one click, preserving full open-source academic transparency.

---

---

## 12. Comprehensive Mathematical Appendix & Formal Proofs

This appendix details the underlying mathematical derivations and formal proofs implemented throughout the Quanta curriculum and simulation engines.

---

### Appendix A: Itô’s Lemma & Geometric Brownian Motion
Let the price process $S_t$ follow a Geometric Brownian Motion (GBM):
$$dS_t = \mu S_t dt + \sigma S_t dW_t$$

Let $f(t, S_t) = \ln S_t$. By Itô’s Lemma for a twice continuously differentiable function $f(t, x)$:
$$df(t, S_t) = \frac{\partial f}{\partial t} dt + \frac{\partial f}{\partial S} dS_t + \frac{1}{2} \frac{\partial^2 f}{\partial S^2} (dS_t)^2$$

Computing the partial derivatives:
$$\frac{\partial f}{\partial t} = 0, \quad \frac{\partial f}{\partial S} = \frac{1}{S_t}, \quad \frac{\partial^2 f}{\partial S^2} = -\frac{1}{S_t^2}$$

Using the Itô multiplication rules where $(dt)^2 = 0$, $dt \cdot dW_t = 0$, and $(dW_t)^2 = dt$:
$$(dS_t)^2 = (\mu S_t dt + \sigma S_t dW_t)^2 = \sigma^2 S_t^2 dt$$

Substituting back into the expansion:
$$d(\ln S_t) = 0 \cdot dt + \frac{1}{S_t} (\mu S_t dt + \sigma S_t dW_t) + \frac{1}{2} \left(-\frac{1}{S_t^2}\right) \sigma^2 S_t^2 dt$$
$$d(\ln S_t) = \left( \mu - \frac{1}{2}\sigma^2 \right) dt + \sigma dW_t$$

Integrating both sides from $0$ to $t$:
$$\ln S_t - \ln S_0 = \int_0^t \left( \mu - \frac{1}{2}\sigma^2 \right) ds + \int_0^t \sigma dW_s$$
$$\ln\left(\frac{S_t}{S_0}\right) = \left( \mu - \frac{1}{2}\sigma^2 \right) t + \sigma W_t$$

Exponentiating yields the exact analytical solution implemented in `quanta.synthetic.simulate_gbm`:
$$S_t = S_0 \exp\left( \left(\mu - \frac{1}{2}\sigma^2\right)t + \sigma W_t \right)$$

---

### Appendix B: Mathematical Derivation of the Discrete-Time Kalman Filter
The linear dynamic system is specified by state equation and measurement equation:
$$\mathbf{x}_t = \mathbf{F}_t \mathbf{x}_{t-1} + \mathbf{w}_t, \quad \mathbf{w}_t \sim \mathcal{N}(0, \mathbf{Q}_t)$$
$$\mathbf{y}_t = \mathbf{H}_t \mathbf{x}_t + \mathbf{v}_t, \quad \mathbf{v}_t \sim \mathcal{N}(0, \mathbf{R}_t)$$

#### 1. Prediction Step:
Given the prior estimate $\hat{\mathbf{x}}_{t-1|t-1}$ and error covariance $\mathbf{P}_{t-1|t-1}$:
$$\hat{\mathbf{x}}_{t|t-1} = \mathbf{F}_t \hat{\mathbf{x}}_{t-1|t-1}$$
$$\mathbf{P}_{t|t-1} = \mathbf{F}_t \mathbf{P}_{t-1|t-1} \mathbf{F}_t' + \mathbf{Q}_t$$

#### 2. Measurement Innovation:
$$\tilde{\mathbf{y}}_t = \mathbf{y}_t - \mathbf{H}_t \hat{\mathbf{x}}_{t|t-1}$$
$$\mathbf{S}_t = \mathbf{H}_t \mathbf{P}_{t|t-1} \mathbf{H}_t' + \mathbf{R}_t$$

#### 3. Optimal Kalman Gain Derivation:
We seek the optimal gain matrix $\mathbf{K}_t$ that minimizes the mean squared estimation error, i.e., minimizing the trace of the posterior covariance $\text{Tr}(\mathbf{P}_{t|t})$:
$$\hat{\mathbf{x}}_{t|t} = \hat{\mathbf{x}}_{t|t-1} + \mathbf{K}_t \tilde{\mathbf{y}}_t$$
$$\mathbf{e}_t = \mathbf{x}_t - \hat{\mathbf{x}}_{t|t} = (\mathbf{I} - \mathbf{K}_t \mathbf{H}_t)(\mathbf{x}_t - \hat{\mathbf{x}}_{t|t-1}) - \mathbf{K}_t \mathbf{v}_t$$

The posterior error covariance matrix is:
$$\mathbf{P}_{t|t} = (\mathbf{I} - \mathbf{K}_t \mathbf{H}_t) \mathbf{P}_{t|t-1} (\mathbf{I} - \mathbf{K}_t \mathbf{H}_t)' + \mathbf{K}_t \mathbf{R}_t \mathbf{K}_t'$$

Differentiating the trace $\text{Tr}(\mathbf{P}_{t|t})$ with respect to $\mathbf{K}_t$ and setting to zero:
$$\frac{\partial \text{Tr}(\mathbf{P}_{t|t})}{\partial \mathbf{K}_t} = -2(\mathbf{H}_t \mathbf{P}_{t|t-1})' + 2 \mathbf{K}_t (\mathbf{H}_t \mathbf{P}_{t|t-1} \mathbf{H}_t' + \mathbf{R}_t) = 0$$
$$\mathbf{K}_t (\mathbf{H}_t \mathbf{P}_{t|t-1} \mathbf{H}_t' + \mathbf{R}_t) = \mathbf{P}_{t|t-1} \mathbf{H}_t'$$
$$\mathbf{K}_t = \mathbf{P}_{t|t-1} \mathbf{H}_t' \mathbf{S}_t^{-1}$$

#### 4. Covariance Update:
$$\mathbf{P}_{t|t} = (\mathbf{I} - \mathbf{K}_t \mathbf{H}_t) \mathbf{P}_{t|t-1}$$

---

### Appendix C: The Almgren-Chriss Optimal Execution Variational Derivation
An institution desires to liquidate $X$ shares over time horizon $T$ divided into $N$ intervals $\tau = T/N$. Let $x_k$ be the shares remaining at time $t_k$, with trade size $n_k = x_{k-1} - x_k$.

The stock price process evolves as:
$$S_k = S_{k-1} + \sigma \tau^{1/2} \xi_k - \tau \gamma(n_k/\tau)$$
$$\tilde{S}_k = S_{k-1} - \eta(n_k/\tau)$$
*(where $\gamma$ is permanent market impact and $\eta$ is temporary market impact).*

The total capture from liquidation is:
$$\sum_{k=1}^N n_k \tilde{S}_k = X S_0 - \sum_{k=1}^N \tau \gamma(n_k/\tau) x_k - \sum_{k=1}^N \eta(n_k/\tau) n_k + \sum_{k=1}^N \sigma \tau^{1/2} \xi_k x_k$$

Under linear impact models $\gamma(v) = \gamma v$ and $\eta(v) = \eta v$:
$$\mathbb{E}[x] = \frac{1}{2} \gamma X^2 + \frac{\eta}{\tau} \sum_{k=1}^N (x_{k-1} - x_k)^2$$
$$V[x] = \sigma^2 \sum_{k=1}^N \tau x_k^2$$

The optimization objective under risk-aversion parameter $\lambda$:
$$\min_{\{x_k\}} U(x) = \mathbb{E}[x] + \lambda V[x] = \frac{1}{2}\gamma X^2 + \frac{\eta}{\tau} \sum_{k=1}^N (x_{k-1} - x_k)^2 + \lambda \sigma^2 \tau \sum_{k=1}^N x_k^2$$

Differentiating with respect to $x_j$ ($j = 1, \dots, N-1$):
$$\frac{\partial U}{\partial x_j} = \frac{2\eta}{\tau} (2x_j - x_{j-1} - x_{j+1}) + 2\lambda \sigma^2 \tau x_j = 0$$
$$\frac{x_{j+1} - 2x_j + x_{j-1}}{\tau^2} = \frac{\lambda \sigma^2}{\eta} x_j$$

Taking the continuous-time limit $\tau \to 0$, this difference equation becomes the second-order ordinary differential equation:
$$\frac{d^2 x}{dt^2} = \kappa^2 x(t), \quad \text{where } \kappa^2 = \frac{\lambda \sigma^2}{\eta}$$

Subject to boundary conditions $x(0) = X$ and $x(T) = 0$, the unique hyperbolic solution is:
$$x(t) = X \frac{\sinh(\kappa(T - t))}{\sinh(\kappa T)}$$

---

### Appendix D: Uniswap v3 Concentrated Liquidity & LVR Proof

#### 1. Concentrated Liquidity Invariant
In Uniswap v2, the curve is $x \cdot y = k = L^2$ from price $0$ to $\infty$.
In Uniswap v3, liquidity is concentrated in $[p_a, p_b]$. The virtual reserves $(x_{\text{virt}}, y_{\text{virt}})$ satisfy:
$$(x + x_{\text{offset}})(y + y_{\text{offset}}) = L^2$$

Where the offsets are determined such that $y = 0$ at $P = p_a$ and $x = 0$ at $P = p_b$:
$$x_{\text{offset}} = \frac{L}{\sqrt{p_b}}, \quad y_{\text{offset}} = L \sqrt{p_a}$$

Thus:
$$\left(x + \frac{L}{\sqrt{p_b}}\right)\left(y + L\sqrt{p_a}\right) = L^2$$

At any price $P \in [p_a, p_b]$:
$$x = L \left(\frac{1}{\sqrt{P}} - \frac{1}{\sqrt{p_b}}\right)$$
$$y = L \left(\sqrt{P} - \sqrt{p_a}\right)$$

#### 2. Loss-Versus-Rebalancing (LVR)
Milionis, Moallemi, Roughgarden (2022): Let the market price $P_t$ follow $dP_t = \sigma P_t dW_t$. At each instant, an external arbitrageur trades against the pool whenever $P_{\text{pool}} \ne P_{\text{market}}$.

The instantaneous profit extracted by the arbitrageur (which is the instantaneous loss incurred by the LP relative to a rebalanced benchmark holding the same inventory) is:
$$d\text{LVR}_t = \frac{1}{8} \sigma^2 V(P_t) dt = \frac{1}{8} \sigma^2 (x_t P_t + y_t) dt$$

For a constant product invariant with total value $V(P) = 2L\sqrt{P}$:
$$\text{LVR}_T = \frac{1}{4} \sigma^2 L \int_0^T \sqrt{P_t} dt$$
*This proves that LVR is independent of the price path drift $\mu$ and depends solely on quadratic variation $\sigma^2 dt$. For an LP to be profitable, accumulated swap fee revenue must exceed $\text{LVR}_T$.*

---

### Appendix E: Bailey & López de Prado Deflated Sharpe Ratio (DSR) Proof
Let $\hat{\text{SR}}$ be the estimated Sharpe ratio from a sample of length $T$, where returns exhibit skewness $\hat{\gamma}_3$ and kurtosis $\hat{\gamma}_4$.

Andrew Lo (2002) proved that the asymptotic variance of $\hat{\text{SR}}$ under non-normal returns is:
$$\text{Var}(\hat{\text{SR}}) = \frac{1}{T-1} \left( 1 - \hat{\gamma}_3 \hat{\text{SR}} + \frac{\hat{\gamma}_4 - 1}{4}\hat{\text{SR}}^2 \right)$$

When $K$ independent strategy trials are conducted, the expected maximum Sharpe ratio under the null hypothesis $H_0: \text{SR} = 0$ is the expected maximum of $K$ zero-mean Gaussian variables with variance $V = \text{Var}(\{\hat{\text{SR}}_k\})$:
$$\mathbb{E}\left[\max_{k=1,\dots,K} \hat{\text{SR}}_k\right] \approx \sqrt{V} \left( (1 - \gamma) \Phi^{-1}\left(1 - \frac{1}{K}\right) + \gamma \Phi^{-1}\left(1 - \frac{1}{Ke}\right) \right)$$
*(where $\gamma \approx 0.5772156649$ is the Euler-Mascheroni constant).*

Denoting this threshold $\text{SR}^*$, the Deflated Sharpe Ratio is the probability that the observed $\hat{\text{SR}}$ exceeds $\text{SR}^*$ under the asymptotic distribution:
$$\text{DSR} = \Phi\left( \frac{(\hat{\text{SR}} - \text{SR}^*)}{\sqrt{\text{Var}(\hat{\text{SR}})}} \right) = \Phi\left( \frac{(\hat{\text{SR}} - \text{SR}^*) \sqrt{T-1}}{\sqrt{1 - \hat{\gamma}_3 \hat{\text{SR}} + \frac{\hat{\gamma}_4 - 1}{4}\hat{\text{SR}}^2}} \right)$$

---

### Appendix F: Mathematical Formulation of Virtual Brokerage Matching & Execution Dynamics

#### 1. Continuous Double Auction & Queue Depletion Mechanics
Let the limit order book at time $t$ for price level $p$ have resting queue volume $Q(p, t)$. When a learner posts a passive limit order of size $q_{\text{order}}$ at price $p$, its initial position in the FIFO queue is:
$$x_0 = Q(p, t)$$

Let $v_k$ be the volume of incoming aggressive market orders that execute at price $p$ over discrete intervals $k = 1, 2, \dots$. The residual queue volume ahead of the learner's order evolves according to:
$$x_k = \max\left(0, \ x_{k-1} - v_k\right)$$

The fill event $\tau_{\text{fill}}$ occurs at the first time index $k^*$ such that:
$$k^* = \inf \left\{ k : \sum_{i=1}^k v_i \ge x_0 + q_{\text{order}} \right\}$$

If the market price trades through level $p$ (i.e., best bid drops below $p$ for buy limit orders, or best ask rises above $p$ for sell limit orders), the fill condition is satisfied unconditionally with fill price $P_{\text{fill}} = p$.

#### 2. Regulation T Margin Maintenance & Forced Liquidation Sizing
Let a learner hold long portfolio assets $\{Q_i^L\}_{i=1}^{M_L}$ with mark prices $\{P_i^L\}$ and short liabilities $\{Q_j^S\}_{j=1}^{M_S}$ with mark prices $\{P_j^S\}$, alongside cash balance $C_t$.

The total portfolio equity is:
$$E_t = C_t + \sum_{i=1}^{M_L} P_{i,t}^L Q_{i,t}^L - \sum_{j=1}^{M_S} P_{j,t}^S |Q_{j,t}^S|$$

Under Federal Reserve Regulation T and FINRA Rule 4210:
$$\text{Maintenance Margin Requirement } (MMR_t) = 0.25 \sum_{i=1}^{M_L} P_{i,t}^L Q_{i,t}^L + 0.30 \sum_{j=1}^{M_S} P_{j,t}^S |Q_{j,t}^S|$$

A **Margin Call** is triggered when Maintenance Excess breaches zero:
$$\text{ME}_t = E_t - MMR_t < 0$$

To restore margin compliance ($\text{ME} \ge 0$) via market liquidation of long asset $k$ (where each dollar sold reduces margin requirement by $\$0.25$ and yields $\$1.00$ in cash, producing a net cushion gain of $\$0.75$ per dollar liquidated), the minimum liquidation notional $\Delta N_k$ required is:
$$\Delta N_k \ge \frac{|\text{ME}_t|}{1 - 0.25} = \frac{|\text{ME}_t|}{0.75}$$

#### 3. Short Borrow Compounding & Hard-to-Borrow (HTB) Cost Model
For short positions held overnight across $D$ calendar days, the borrow fee is debited daily from cash according to the annualized borrow rate $r_{\text{borrow}}(t)$:
$$C_{t+1} = C_t - \sum_{j=1}^{M_S} \left( P_{j,t}^S |Q_{j,t}^S| \times \frac{r_{\text{borrow}, j}(t)}{360} \right)$$
Where $r_{\text{borrow}, j}(t)$ dynamically expands during short squeezes as available borrow inventory $I_{\text{avail}, j} \rightarrow 0$:
$$r_{\text{borrow}, j}(t) = r_{\text{base}} + \alpha \cdot \exp\left( -\beta \frac{I_{\text{avail}, j}(t)}{\text{Float}_j} \right)$$

---

### Appendix G: Complete Master Index of the 28 Computational Labs

| Track | Chapter | Lab Title | Primary Algorithms & SDK Modules |
| :--- | :--- | :--- | :--- |
| **Track 1** | Ch 1 | Margin of Safety Envelopes | `quanta.data`, historical drawdowns, intrinsic band modeling |
| **Track 1** | Ch 2 | SEC 10-K Net-Net & Altman Z Auditor | `quanta.data`, balance sheet haircuts, Altman Z-Score |
| **Track 1** | Ch 3 | Beneish M-Score & Sloan Accruals | Probit earnings manipulation detection, accrual anomaly |
| **Track 1** | Ch 4 | Debt Covenant & FCC Stress Tester | Operating leverage simulation, fixed-charge coverage |
| **Track 1** | Ch 5 | Triangulated Valuation Engine | DCF, Greenwald EPV, Revised Graham Formula |
| **Track 2** | Ch 6 | Yield Curve Bootstrapper & Immunizer | Cubic splines, Nelson-Siegel, MacAulay/Mod Duration, Convexity |
| **Track 2** | Ch 7 | Non-Gaussian Tail Risk & Hill Estimator | Student's $t$ MLE, Generalized Pareto, Hill Tail Index |
| **Track 2** | Ch 8 | Stationary Block Bootstrap Engine | Politis-Romano resampling, empirical Sharpe confidence intervals |
| **Track 2** | Ch 9 | Benjamini-Hochberg FDR Auditor | Multiple hypothesis testing, $p$-value rank corrections |
| **Track 2** | Ch 10 | Rolling CAPM Beta & Alpha with HAC | Single-index OLS, Newey-West HAC covariance matrices |
| **Track 3** | Ch 11 | Econometric Diagnostic & Repair Suite | VIF collinearity, Breusch-Pagan, White-Huber HC3 standard errors |
| **Track 3** | Ch 12 | López de Prado Fractional Differentiation | Binomial weight expansion, ADF test, price memory preservation |
| **Track 3** | Ch 13 | Kalman Filter Dynamic Pairs Trader | State-space recursive updates, Ornstein-Uhlenbeck half-life |
| **Track 3** | Ch 14 | GARCH(1,1) Volatility Forecasting | MLE log-likelihood optimization, forward volatility cones |
| **Track 3** | Ch 15 | Fama-French 5-Factor & Risk Parity | Factor regressions, Ledoit-Wolf shrinkage, Equal Risk Contribution |
| **Track 3** | Ch 16 | Deflated Sharpe Ratio (DSR) Auditor | Extreme value theory, Euler-Mascheroni correction, MinTRL |
| **Track 4** | Ch 17 | Systematic NCAV + Piotroski F-Score | Historical point-in-time annual rebalancer, liquidity filters |
| **Track 4** | Ch 18 | Multi-Factor Ranking & Neutralization | 3-sigma winsorization, sector dummy OLS, Spearman Rank IC |
| **Track 5** | Ch 19 | Event-Driven Bot Core with Redis State | Python `asyncio`, Redis state persistence, finite state machine |
| **Track 5** | Ch 20 | Almgren-Chriss Optimal Execution | Variational calculus, hyperbolic trajectory, market impact |
| **Track 5** | Ch 21 | Purged K-Fold XGBoost Stock Ranker | Purging & embargoing, monotonic constraints, out-of-sample IC |
| **Track 5** | Ch 22 | Multi-Agent LLM SEC Forensic Auditor | LangChain / LlamaIndex, Pydantic schemas, 10-K RAG pipeline |
| **Track 5** | Ch 23 | Stock Buying/Selling Simulator & Production Risk | `quanta.broker.PaperBroker`, bracket orders, margin checks, kill-switches |
| **Track 6** | Ch 24 | Tokenomics DCF & Supply Dilution Model | Equation of Exchange, programmatic emission, protocol fee switches |
| **Track 6** | Ch 25 | Uniswap v3 Concentrated Liquidity Backtester | Tick math, virtual reserves, capital multipliers, LVR quantification |
| **Track 6** | Ch 26 | Delta-Neutral Perp Funding Rate Arb | Basis drift, 8-hour funding cash-and-carry, liquidation buffers |
| **Track 6** | Ch 27 | Web3 Mempool Event Listener & Gas Bidder | `Web3.py`, WebSocket RPC, EIP-1559 priority fee escalation |
| **Track 6** | Ch 28 | Leveraged Lending Liquidation Stress Lab | Flash crash simulation, collateral health factors, oracle latency |

---

*This exhaustive Product Requirements Document is committed and available at [`/Users/imac/Documents/dev/quanta/PRD.md`](file:///Users/imac/Documents/dev/quanta/PRD.md).*





