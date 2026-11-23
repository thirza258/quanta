"""Original course: From Spreadsheet to Strategy Lab.

Bridges spreadsheet-native users (Excel, Google Sheets) into programmatic
backtesting, causal execution, and systematic quantitative research.
"""

from foundations import question


def build_spreadsheet_to_strategy():
    modules = [
        {
            "id": "24.1",
            "part": "1",
            "title": "The spreadsheet you already trust — and its three blind spots",
            "subtitle": "Why formulas that look profitable in Excel fail in live markets.",
            "minutes": 12,
            "objective": "Identify the three structural blind spots of spreadsheet backtesting: look-ahead leakage, transaction friction neglect, and survivorship bias.",
            "kind": "fundamentals",
            "formula": r"\text{Spreadsheet Return} \ne \text{Executed Return} - \text{Friction} - \text{Lag}",
            "code": (
                "# Demonstrating why spreadsheet cells calculate look-ahead bias\n"
                "prices = [100.0, 102.5, 101.0, 104.0, 103.5, 106.0]\n"
                "# In Excel, row t often references close(t) to generate a trade filled at close(t)\n"
                "# Strategy Lab enforces causal ordering: signal at close(t), fill at open(t+1)\n"
                "print('Prices:', prices)\n"
                "excel_idealized_profit = 0.0\n"
                "for i in range(len(prices) - 1):\n"
                "    diff = prices[i + 1] - prices[i]\n"
                "    if diff > 0:\n"
                "        excel_idealized_profit = excel_idealized_profit + diff\n"
                "print('Naive Excel Profit (same-bar execution):', round(excel_idealized_profit, 2))\n"
            ),
            "content": (
                "## The idea\n\n"
                "Millions of traders build their first models in Excel or Google Sheets. Spreadsheets are intuitive, visual, and immediately responsive. But when translated to live execution, backtests built in spreadsheets almost always overstate returns. This occurs because of three structural blind spots:\n\n"
                "1. **Look-Ahead Bias (Causal Leakage)**: In a spreadsheet cell `=IF(C2>D2, E2, 0)`, it is trivial to accidentally reference data that became available only after the trade was supposed to occur. A rule that decides to buy at the close of day $t$ cannot realistically buy at that day's closing price without perfect foresight or immediate fill with zero market impact.\n"
                "2. **Neglected Frictions (Costs & Slippage)**: Spreadsheets rarely model bid-ask spreads, exchange fees, borrow fees for short positions, or price slippage on size. A strategy making 200 trades a year with an average gross gain of 0.3% is highly profitable in Excel, but guarantees a 100% loss after trading fees.\n"
                "3. **Formula Drift & Overfitting**: Cell drag-and-drop easily introduces copy-paste formula errors that go unnoticed in large sheets.\n\n"
                "$$\n"
                r"\text{Realized Return} = \text{Gross Return} - \text{Commissions} - \text{Spread/Slippage} - \text{Borrow Costs}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "An analyst tests a 10-day momentum rule on a stock trading at $100. In Excel, the sheet assumes buying at the exact closing price whenever the day's close exceeds yesterday's high, generating a 24% annual gross return across 150 trades.\n\n"
                "When ported to Strategy Lab's causal engine with realistic 10 bps commissions and 5 bps slippage, two things happen: first, orders execute on the open of the following bar; second, 150 round-trip trades generate $150 \\times 30\\text{ bps} = 4.5\\%$ in direct transaction friction. The strategy's net return collapses from +24% to −3.2%. The spreadsheet did not find alpha; it found accounting fiction.\n\n"
                "## Work through it yourself\n\n"
                "1. Audit your spreadsheet formulas: verify whether any trade decision references closing prices of the same bar it claims to fill on.\n"
                "2. Subtract a minimum 15 bps (0.15%) round-trip fee from every single transaction row in your sheet.\n"
                "3. Observe whether your perceived edge survives before risking capital.\n\n"
                "### In the sandbox\n\n"
                "Run the Python snippet to see how naive same-bar calculation differs from real delayed execution."
            ),
            "exercise": question(
                "Which error is the most common cause of unrealistic profitability in spreadsheet trading backtests?",
                [
                    "Using Arial font instead of Courier",
                    "Look-ahead bias where a buy signal at today's close is assumed to fill at today's close with zero lag or fees",
                    "Having too many decimal places in the formula",
                ],
                1,
                "Look-ahead bias occurs when a backtest uses data from the future or assumes instant execution at the signal price without friction or delay.",
            ),
            "exercises": [
                question(
                    "Which error causes unrealistic profitability in spreadsheet backtests?",
                    [
                        "Using Arial font",
                        "Look-ahead bias assuming instant same-bar execution without fees or delay",
                        "Having too many decimals",
                    ],
                    1,
                    "Look-ahead bias uses data from the future or assumes execution at signal price without lag.",
                ),
            ],
            "terms": [
                {"term": "Look-Ahead Bias", "definition": "A flaw in backtesting where future information or data not yet available at the decision point is used in generating trading signals."},
                {"term": "Slippage", "definition": "The difference between the expected execution price of an order and the actual price at which the order is filled in the market."},
            ],
            "references": [
                {"title": "CFA Institute · Backtesting Pitfalls and Survivorship Bias", "url": "https://www.cfainstitute.org"},
                {"title": "SEC · Quantitative Trading and Systematic Execution Risks", "url": "https://www.sec.gov"},
            ],
        },
        {
            "id": "24.2",
            "part": "1",
            "title": "Mapping columns: from your sheet to the Strategy Lab data model",
            "subtitle": "Translate rows and columns into standardized OHLCV bar structures.",
            "minutes": 12,
            "objective": "Map spreadsheet columns (Date, Open, High, Low, Close, Volume) into Strategy Lab's structured data dictionary format.",
            "kind": "fundamentals",
            "formula": r"\text{Bar}_t = \{\text{timestamp}, \text{open}, \text{high}, \text{low}, \text{close}, \text{volume}\}",
            "code": (
                "# Mapping raw tabular columns to Strategy Lab's data dictionary\n"
                "raw_sheet_row = {'Date': '2026-03-01', 'Open': 150.2, 'High': 152.0, 'Low': 149.5, 'Close': 151.8, 'Vol': 120500}\n"
                "standard_bar = {\n"
                "    'time': raw_sheet_row['Date'],\n"
                "    'open': float(raw_sheet_row['Open']),\n"
                "    'high': float(raw_sheet_row['High']),\n"
                "    'low': float(raw_sheet_row['Low']),\n"
                "    'close': float(raw_sheet_row['Close']),\n"
                "    'volume': int(raw_sheet_row['Vol']),\n"
                "}\n"
                "print('Standardized Strategy Lab Bar:', standard_bar)\n"
            ),
            "content": (
                "## The idea\n\n"
                "In Excel, each row is a disconnected table row. In quantitative engines like Strategy Lab, market history is structured as an immutable sequence of **OHLCV bars** (Open, High, Low, Close, Volume).\n\n"
                "To port your dataset into Strategy Lab, your tabular data must adhere to standard column definitions:\n"
                "- `timestamp` (or `date`): ISO-8601 format (`YYYY-MM-DD`). Avoid locale-dependent strings like `03/04/25`.\n"
                "- `open`: The price of the first transaction in the bar.\n"
                "- `high` and `low`: The highest and lowest transaction prices during the interval.\n"
                "- `close`: The final recorded transaction price for the bar.\n"
                "- `volume`: Total number of shares or contracts traded.\n\n"
                "$$\n"
                r"\mathrm{Bar}_t = (\tau_t, O_t, H_t, L_t, C_t, V_t) \quad \text{where } L_t \le \min(O_t, C_t) \le \max(O_t, C_t) \le H_t"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A spreadsheet user exports daily prices from Yahoo Finance where columns are named `Date`, `Open`, `High`, `Low`, `Close`, `Adj Close`, and `Volume`. Strategy Lab uses split-adjusted `close` for price signals and raw `volume` for liquidity checks.\n\n"
                "Mapping these requires confirming that `high` is always $\\ge$ both `open` and `close`, and that `low` is always $\\le$ both. Any row where $H_t < L_t$ indicates corrupt data or bad adjustment factors that will cause backtest crashes.\n\n"
                "## Work through it yourself\n\n"
                "1. Open your exported CSV in a text editor or spreadsheet.\n"
                "2. Standardize column headers to lowercase: `date`, `open`, `high`, `low`, `close`, `volume`.\n"
                "3. Ensure dates are sorted chronologically from earliest to latest.\n\n"
                "### In the sandbox\n\n"
                "Inspect how the Python script converts a raw dictionary row into a validated bar structure."
            ),
            "exercise": question(
                "Which invariant must ALWAYS hold true for a valid price bar (OHLC)?",
                [
                    "Close must always equal Open",
                    "Low <= Open, Close <= High (High is maximum, Low is minimum)",
                    "Volume must always be zero",
                ],
                1,
                "The High must be the highest price of the interval and the Low must be the lowest, enclosing both Open and Close.",
            ),
            "exercises": [
                question(
                    "Which invariant must hold true for a valid OHLC bar?",
                    [
                        "Close must equal Open",
                        "Low <= min(Open, Close) and High >= max(Open, Close)",
                        "Volume must be zero",
                    ],
                    1,
                    "High is the highest price of the period and Low is the lowest.",
                ),
            ],
            "terms": [
                {"term": "OHLCV", "definition": "Open, High, Low, Close, and Volume: the universal data representation for financial market bars."},
                {"term": "Data Invariant", "definition": "A mathematical condition that must remain true across all valid states of a dataset."},
            ],
            "references": [
                {"title": "OpenFIGI · Standardized Financial Instrument Identifiers", "url": "https://www.openfigi.com"},
            ],
        },
        {
            "id": "24.3",
            "part": "1",
            "title": "Importing and verifying your first series",
            "subtitle": "Confirm row count, date continuity, and reconcile the final closing value.",
            "minutes": 14,
            "objective": "Verify an imported price series against a spreadsheet reference by checking total row count, date alignment, and the last close value.",
            "kind": "fundamentals",
            "formula": r"\text{Match Verification: } N_{\text{Lab}} = N_{\text{Sheet}} \land C_{\text{last, Lab}} = C_{\text{last, Sheet}}",
            "code": (
                "# Verifying imported series integrity against spreadsheet reference\n"
                "rows = [\n"
                "    {'date': '2026-01-02', 'close': 150.50},\n"
                "    {'date': '2026-01-05', 'close': 152.00},\n"
                "    {'date': '2026-01-06', 'close': 151.25},\n"
                "    {'date': '2026-01-07', 'close': 153.75},\n"
                "]\n"
                "row_count = len(rows)\n"
                "first_date = rows[0]['date']\n"
                "last_date = rows[-1]['date']\n"
                "last_close = rows[-1]['close']\n"
                "print('Row count:', row_count)\n"
                "print('Date span:', first_date, 'to', last_date)\n"
                "print('Reconciled last close:', last_close)\n"
            ),
            "content": (
                "## The idea\n\n"
                "Never run a backtest on unverified data. Before testing any strategy rule in Strategy Lab, conduct a **three-point reconciliation** between your spreadsheet and the platform's data engine:\n\n"
                "1. **Row Count Match**: Ensure no trading days were dropped during CSV parsing (e.g. leap years or holiday handling).\n"
                "2. **Date Alignment**: Confirm the start date and end date coincide exactly.\n"
                "3. **Last Close Reconciled**: Check that the final bar's closing price in Strategy Lab matches your spreadsheet down to the cent.\n\n"
                "$$\n"
                r"\Delta C = |C_{\text{terminal, Strategy Lab}} - C_{\text{terminal, Spreadsheet}}| = 0{,}00"
                "\n$$\n\n"
                "## A worked example\n\n"
                "You export 252 trading days of BBCA prices from your research sheet. The last closing price on December 30, 2026 is Rp10.250.\n\n"
                "Upon uploading to Strategy Lab, the summary card displays: `252 bars | 2026-01-02 to 2026-12-30 | Last: 10,250`. Because the row count and terminal close match exactly, you have verified data parity. If the row count showed 248 instead, 4 bars were lost during import—often caused by blank lines or malformed commas.\n\n"
                "## Work through it yourself\n\n"
                "1. Note the exact row count and last closing price of your spreadsheet.\n"
                "2. Load the dataset in Strategy Lab.\n"
                "3. Verify that both numbers agree before writing strategy code.\n\n"
                "### In the sandbox\n\n"
                "Run the verification script to inspect how pandas checks start date, end date, and terminal close."
            ),
            "exercise": question(
                "Why must you verify the terminal closing price and row count after importing data into Strategy Lab?",
                [
                    "To change the color of the chart",
                    "To confirm that no bars were dropped, corrupted, or misaligned during CSV ingestion",
                    "To automatically double your portfolio return",
                ],
                1,
                "Reconciling row count and the last closing price proves that the backtest engine is operating on the exact same data as your spreadsheet.",
            ),
            "exercises": [
                question(
                    "Why verify terminal closing price and row count after importing data?",
                    [
                        "To change chart color",
                        "To confirm no bars were dropped or misaligned during ingestion",
                        "To double return",
                    ],
                    1,
                    "Reconciliation ensures the backtest engine operates on the exact intended data series.",
                ),
            ],
            "terms": [
                {"term": "Data Parity", "definition": "A verified state where two independent data systems contain identical records without omissions or discrepancies."},
            ],
            "references": [
                {"title": "Kenneth R. French Data Library · Documentation and Reconciliation", "url": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html"},
            ],
        },
        {
            "id": "24.4",
            "part": "2",
            "title": "Rebuilding your moving-average rule as a strategy",
            "subtitle": "Translate =AVERAGE(C2:C21) into a clean, testable Strategy Lab signal.",
            "minutes": 15,
            "objective": "Translate a classic 20-day/50-day moving average crossover rule from spreadsheet formulas into a Strategy Lab signal function.",
            "kind": "fundamentals",
            "formula": r"\text{Signal}_t = \begin{cases} 1 & \text{if } \text{SMA}_{20}(t) > \text{SMA}_{50}(t) \\ 0 & \text{otherwise} \end{cases}",
            "code": (
                "# Translating Excel =IF(AVERAGE(C2:C21) > AVERAGE(C2:C51), 1, 0)\n"
                "# In Strategy Lab, trailing moving averages are computed causally\n"
                "def strategy(data):\n"
                "    # The engine evaluates indicators with strict chronological ordering\n"
                "    return sma(data['close'], 20) > sma(data['close'], 50)\n"
                "\n"
                "print('Strategy logic defined cleanly with built-in sma indicator!')\n"
            ),
            "content": (
                "## The idea\n\n"
                "In a spreadsheet, calculating a 20-day Simple Moving Average requires writing `=AVERAGE(C2:C21)` in row 21, then dragging the formula down across 500 rows. If someone sorts the sheet by date descending, all formulas break silently.\n\n"
                "In Strategy Lab, the same logic is expressed as a **declarative signal function**. You define the logic once, and the engine evaluates it across all time periods with strict chronological ordering:\n\n"
                "```python\n"
                "def strategy(data):\n"
                "    return data['close'] > data['sma_50']\n"
                "```\n\n"
                "$$\n"
                r"\mathrm{SMA}_k(t) = \frac{1}{k}\sum_{i=0}^{k-1} C_{t-i}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "Consider a 20-day moving average. In Excel, column D contains `=AVERAGE(C2:C21)` and column E contains `=IF(C21>D21, 1, 0)`.\n\n"
                "In Strategy Lab, `data['close'] > data['sma_50']` produces the exact same boolean array. The crucial difference is execution: Strategy Lab automatically executes the position on the **next open** ($t+1$), completely removing the accidental look-ahead leakage that plagues spreadsheet models.\n\n"
                "## Work through it yourself\n\n"
                "1. Inspect your moving average formula in Excel.\n"
                "2. Rewrite it in Strategy Lab using `data['close'] > data['sma_50']`.\n"
                "3. Click **Run backtest** and compare the equity curve.\n\n"
                "### In the sandbox\n\n"
                "Run the Python strategy function template and verify that the signal produces clean true/false values."
            ),
            "exercise": question(
                "What is the key advantage of writing a strategy function in Strategy Lab compared to dragging formulas in Excel?",
                [
                    "Spreadsheets run out of colors",
                    "Strategy Lab enforces chronological execution and causal separation between signal and execution automatically",
                    "Strategy Lab guarantees 100% win rate on all trades",
                ],
                1,
                "Strategy Lab evaluates rules chronologically and fills orders at the next bar's open, eliminating accidental formula dragging errors and same-bar execution leakage.",
            ),
            "exercises": [
                question(
                    "What is the advantage of Strategy Lab over dragging formulas in Excel?",
                    [
                        "Spreadsheets run out of colors",
                        "Strategy Lab enforces chronological order and causal execution automatically",
                        "Strategy Lab guarantees 100% win rate",
                    ],
                    1,
                    "Strategy Lab guarantees chronological order and executes fills causally at the next open.",
                ),
            ],
            "terms": [
                {"term": "Simple Moving Average (SMA)", "definition": "The unweighted arithmetic mean of the previous k closing prices."},
                {"term": "Signal Function", "definition": "A pure function that consumes historical market data and outputs a desired target exposure."},
            ],
            "references": [
                {"title": "Kenneth R. French Data Library · Momentum and Trend Factor Research", "url": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html"},
            ],
        },
        {
            "id": "24.5",
            "part": "2",
            "title": "Why the numbers differ: costs, slippage, look-ahead",
            "subtitle": "Deconstruct the delta between your sheet's CAGR and Strategy Lab's backtest.",
            "minutes": 15,
            "objective": "Deconstruct a numeric worked example showing why Strategy Lab results differ from spreadsheet results due to frictions and timing.",
            "kind": "fundamentals",
            "formula": r"\text{CAGR}_{\text{real}} = \left(\prod_{t=1}^T (1 + R_t - c_t)\right)^{1/Y} - 1",
            "code": (
                "# Deconstructing the difference between Spreadsheet vs Strategy Lab\n"
                "gross_trade_pnl = 1500.0\n"
                "number_of_trades = 60\n"
                "commission_per_trade = 12.5\n"
                "slippage_estimate = 7.5\n"
                "total_friction = number_of_trades * (commission_per_trade + slippage_estimate)\n"
                "net_strategy_lab_pnl = gross_trade_pnl - total_friction\n"
                "print('Spreadsheet Reported PnL: $', gross_trade_pnl)\n"
                "print('Total Market Frictions:  $', total_friction)\n"
                "print('Strategy Lab Net PnL:     $', net_strategy_lab_pnl)\n"
            ),
            "content": (
                "## The idea\n\n"
                "When you run your strategy in Strategy Lab for the first time, your backtested returns will almost certainly look lower than your spreadsheet. Do not panic: **the spreadsheet was lying to you, and Strategy Lab is telling you the truth**.\n\n"
                "There are three mathematical drivers of this difference:\n"
                "1. **Execution Timing**: Spreadsheets assume you enter at the signal bar's close ($P_t$). Strategy Lab enters at the open of bar $t+1$ ($O_{t+1}$). If prices gap up on the open, your actual entry price is higher.\n"
                "2. **Transaction Drag**: Strategy Lab deducts broker commissions and bid-ask spread costs on every trade turnover.\n"
                "3. **Position Sizing Caps**: Spreadsheets often reinvest 100% of capital with infinite compounding, ignoring cash reserves and borrow fees.\n\n"
                "$$\n"
                r"\Delta_{\text{pnl}} = \sum_{i=1}^M \left[(P_{\text{sheet, fill}} - P_{\text{actual, fill}}) - \text{commission}_i - \text{slippage}_i\right]"
                "\n$$\n\n"
                "## A worked example\n\n"
                "In Excel, a breakout strategy takes 60 trades a year and reports $1,500 in total gross profit. The spreadsheet assumes zero friction.\n\n"
                "In Strategy Lab, the engine applies standard institutional assumptions: $12.50 round-trip commission per trade and $7.50 estimated slippage from crossing the spread. Across 60 trades, friction consumes:\n"
                "$$\\text{Friction} = 60 \\times (\\$12.50 + \\$7.50) = 60 \\times \\$20 = \\$1,200$$\n"
                "The actual net profit in Strategy Lab is $\\$1,500 - \\$1,200 = \\$300$. Strategy Lab prevents you from deploying an unprofitable high-churn strategy with real capital.\n\n"
                "## Work through it yourself\n\n"
                "1. Check the trade count in your Strategy Lab backtest summary.\n"
                "2. Multiply the trade count by your broker's actual fee schedule.\n"
                "3. Reconcile the net Sharpe ratio after costs.\n\n"
                "### In the sandbox\n\n"
                "Run the script to see how 60 trades of friction erase 80% of naive spreadsheet profit."
            ),
            "exercise": question(
                "If a strategy generates $1,500 gross profit across 60 trades, but fees and slippage cost $20 per trade, what is the true net profit?",
                [
                    "$1,500",
                    "$300",
                    "-$500",
                ],
                1,
                "Total friction = 60 * $20 = $1,200. Net profit = $1,500 − $1,200 = $300.",
            ),
            "exercises": [
                question(
                    "Gross profit is $1,500 across 60 trades. Frictions cost $20 per trade. What is net profit?",
                    ["$1,500", "$300", "-$500"],
                    1,
                    "Total friction = 60 * $20 = $1,200. Net profit = $1,500 − $1,200 = $300.",
                ),
            ],
            "terms": [
                {"term": "Adverse Selection", "definition": "The tendency for market orders to execute at unfavorable prices when liquidity providers adjust quotes ahead of incoming flow."},
                {"term": "Net Return", "definition": "The true economic return realized after subtracting all commissions, financing costs, and market impact."},
            ],
            "references": [
                {"title": "FINRA · Rule 5310 Best Execution and Spread Costs", "url": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/5310"},
            ],
        },
        {
            "id": "24.6",
            "part": "2",
            "title": "Saving, naming, and re-running",
            "subtitle": "Persist your strategy code, record audit metadata, and version your experiments.",
            "minutes": 10,
            "objective": "Save and name your strategy in Strategy Lab to create a persisted, content-addressed strategy version in your workspace.",
            "kind": "fundamentals",
            "formula": r"\text{Strategy Version} = \text{SHA256}(\text{source code}) \to \text{Workspace Record}",
            "code": (
                "# Simulating Strategy Lab's content-addressed versioning\n"
                "strategy_record = {\n"
                "    'name': 'SMA-20-Crossover',\n"
                "    'version': 1,\n"
                "    'hash': 'c8f309a12b4e',\n"
                "    'created_at': '2026-11-22T10:00:00Z',\n"
                "}\n"
                "print('Persisted Strategy Version:', strategy_record['name'], 'version:', strategy_record['version'])\n"
                "print('Content Hash Fingerprint:', strategy_record['hash'])\n"
            ),
            "content": (
                "## The idea\n\n"
                "In traditional spreadsheets, maintaining versions usually means messy file names like `strategy_v2_final_FINAL_edit3.xlsx`. You can never be sure which file produced which result.\n\n"
                "Strategy Lab replaces this with **persisted, content-addressed versioning**:\n"
                "- Every saved strategy is stored in your personal account workspace.\n"
                "- When you edit the code, Strategy Lab generates an immutable SHA-256 hash of your exact rules.\n"
                "- You can re-run past versions anytime, ensuring 100% scientific reproducibility.\n\n"
                "$$\n"
                r"\mathrm{VersionID} = \mathrm{SHA256}(\mathrm{Code} \parallel \mathrm{Parameters})"
                "\n$$\n\n"
                "## A worked example\n\n"
                "You build a 20-day trend-following strategy and name it `SMA-20-Crossover`. In Strategy Lab, you click **Save strategy**.\n\n"
                "The system creates Version 1 in your account dashboard. Later, you test changing the window from 20 days to 50 days. Saving again automatically produces Version 2. When presenting your research, you can toggle between Version 1 and Version 2 with a single click, viewing the exact historical backtest for each without confusing files.\n\n"
                "## Work through it yourself\n\n"
                "1. Open the Strategy Lab code editor.\n"
                "2. Name your strategy `My-First-Lab-Strategy`.\n"
                "3. Click **Save** to persist the strategy in your workspace account.\n\n"
                "### In the sandbox\n\n"
                "Run the script to observe how content hashing uniquely identifies your strategy source code."
            ),
            "exercise": question(
                "Why does Strategy Lab use content-addressed versioning for saved strategies instead of overwriting files?",
                [
                    "To fill up the database faster",
                    "To guarantee scientific reproducibility so past backtest results can always be verified against the exact code that produced them",
                    "To require users to re-type code every session",
                ],
                1,
                "Content-addressed versioning ensures that every backtest result is permanently linked to the exact immutable source code that created it.",
            ),
            "exercises": [
                question(
                    "Why does Strategy Lab use content-addressed versioning for saved strategies?",
                    [
                        "To fill up database",
                        "To guarantee scientific reproducibility linking results to exact code",
                        "To require re-typing",
                    ],
                    1,
                    "Content-addressed versioning guarantees results can be reproduced from exact source code.",
                ),
            ],
            "terms": [
                {"term": "Content-Addressed Storage", "definition": "A mechanism for storing data where the identifier is derived directly from the content's cryptographic hash."},
                {"term": "Reproducibility", "definition": "The ability of an independent researcher to achieve the identical research outcome using the original data and code."},
            ],
            "references": [
                {"title": "ACM · Reproducibility and Replicability in Computational Science", "url": "https://www.acm.org"},
            ],
        },
        {
            "id": "24.7",
            "part": "2",
            "title": "Where to go next: Factor Studio & AMM simulator orientation",
            "subtitle": "Expand beyond single-stock rules into multi-factor portfolios and on-chain liquidity.",
            "minutes": 12,
            "objective": "Locate Factor Studio and the AMM simulator in the platform and explain the purpose and core mechanics of each.",
            "kind": "fundamentals",
            "formula": r"\text{Factor Portfolio: } R_p = \alpha + \sum \beta_i F_i \quad \text{vs} \quad \text{AMM Curve: } x \cdot y = k",
            "code": (
                "# Orientation: Factor exposures vs AMM constant product curve\n"
                "# Factor ranking\n"
                "symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']\n"
                "scores = [0.85, 0.72, 0.64, 0.51]\n"
                "threshold = 0.70\n"
                "print('Factor scores exceeding threshold:')\n"
                "for i in range(len(symbols)):\n"
                "    if scores[i] > threshold:\n"
                "        print('Passed:', symbols[i], scores[i])\n"
                "\n"
                "# AMM swap constant product\n"
                "x_usdc = 100000\n"
                "y_eth = 50\n"
                "k = x_usdc * y_eth\n"
                "print('AMM Constant Product (k):', k)\n"
            ),
            "content": (
                "## The idea\n\n"
                "Congratulations! You have bridged from static spreadsheets into programmatic strategy testing. Now two flagship engines in Quanta await your exploration:\n\n"
                "1. **Factor Studio ([/lab](/lab))**: Move from single-asset timing rules to cross-sectional equity factor portfolios. Rank hundreds of stocks by Value (P/E), Quality (ROE), and Momentum, constructing long/short market-neutral quintile portfolios.\n"
                "2. **AMM Simulator ([/simulator](/simulator))**: Explore decentralized automated market maker (AMM) mechanics governed by constant product invariants ($x \\cdot y = k$). Simulate impermanent loss, liquidity pool fee generation, and routing slippage.\n\n"
                "$$\n"
                r"x \cdot y = k \quad \longleftrightarrow \quad R_{\text{portfolio}} = \sum_{j=1}^M w_j R_j"
                "\n$$\n\n"
                "## A worked example\n\n"
                "In Factor Studio, instead of asking 'should I buy BBCA today?', you ask 'which 20% of Indonesian banking stocks have the highest deposit growth and lowest non-performing loans?'. The platform ranks the entire universe and computes your factor spread.\n\n"
                "In the AMM Simulator, you deposit 50 ETH and 100,000 USDC into a pool. When external price shocks occur, arbitrageurs trade against the pool, altering pool balances and generating trading fees for you as a liquidity provider. You observe the exact trade-off between fee yield and impermanent loss.\n\n"
                "## Work through it yourself\n\n"
                "1. Click the primary button below to proceed directly into the 32-lesson [The strategy lab](/curriculum/strategy-lab) track.\n"
                "2. Bookmark the Factor Studio in [/lab](/lab).\n"
                "3. You have successfully graduated from spreadsheets to quantitative research!\n\n"
                "### In the sandbox\n\n"
                "Run the script to preview factor sorting logic and the constant product formula."
            ),
            "exercise": question(
                "What is the primary difference between single-stock technical analysis and Factor Studio research?",
                [
                    "Factor Studio uses more monitors",
                    "Factor Studio ranks an entire universe of securities cross-sectionally by systematic characteristics (Value, Quality, Momentum)",
                    "Factor Studio only works on weekends",
                ],
                1,
                "Factor Studio evaluates cross-sectional relative ranking across an entire investment universe rather than timing a single asset.",
            ),
            "exercises": [
                question(
                    "What is the difference between single-stock analysis and Factor Studio?",
                    [
                        "More monitors",
                        "Factor Studio ranks an entire universe cross-sectionally by systematic characteristics",
                        "Only works on weekends",
                    ],
                    1,
                    "Factor Studio evaluates cross-sectional relative ranking across an entire universe.",
                ),
            ],
            "terms": [
                {"term": "Factor Studio", "definition": "Quanta's institutional tool for ranking asset universes by multi-factor exposures and evaluating quintile spread returns."},
                {"term": "Automated Market Maker (AMM)", "definition": "A smart contract that holds liquidity reserves and prices trades algorithmically according to a mathematical formula (e.g. x * y = k)."},
            ],
            "references": [
                {"title": "Uniswap v2 Core Whitepaper · Constant Product Market Making", "url": "https://uniswap.org/whitepaper.pdf"},
                {"title": "Kenneth R. French Data Library · Fama-French Five Factor Model", "url": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html"},
            ],
        },
    ]

    parts = [
        {
            "id": "1",
            "title": "Spreadsheet Pitfalls & Data Alignment",
            "description": "Understand look-ahead bias and transaction friction, map sheet columns to OHLCV bars, and verify data parity.",
        },
        {
            "id": "2",
            "title": "Strategy Translation & Flagship Lab Tools",
            "description": "Rebuild moving averages as clean code, deconstruct cost differences, persist versions, and explore Factor Studio.",
        },
    ]

    STRATEGY_FOOTER = (
        "\n\n# The price sandbox stays in cash; its equity curve is not evidence for the strategy's performance.\n"
        "def strategy(data):\n"
        '    return data["close"] < 0\n'
    )
    for m in modules:
        if "def strategy(data)" not in m.get("code", ""):
            m["code"] = (m.get("code", "") + STRATEGY_FOOTER).strip()

    exams = [
        {
            "id": "spreadsheet-to-strategy-lab-final",
            "title": "From Spreadsheet to Strategy Lab Assessment",
            "kind": "final",
            "passingScore": 70,
            "minutes": 25,
            "version": 2,
            "description": "Comprehensive assessment on translating spreadsheet workflows into systematic code, causal ordering, and Strategy Lab tools.",
            "moduleIds": [m["id"] for m in modules],
            "questions": [
                {
                    "id": "spreadsheet-final-q1",
                    "lessonId": "24.1",
                    "question": "In algorithmic backtesting, why does look-ahead bias invalidate historical trading performance?",
                    "options": [
                        "It compresses the time index of the output chart",
                        "It calculates trading decisions using price or volume data that was not yet observable at the trade execution bar",
                        "It requires excessive memory on the server",
                    ],
                    "answer": 1,
                    "explanation": "Look-ahead bias leaks future bar data into current trading decisions, creating an unreplicable illusion of profitability that fails immediately in live trading.",
                },
                {
                    "id": "spreadsheet-final-q2",
                    "lessonId": "24.2",
                    "question": "In Strategy Lab's OHLCV bar dictionary, what relation must always hold between the High, Low, Open, and Close values of any single bar?",
                    "options": [
                        "High must be greater than or equal to Open, Low, and Close, while Low must be less than or equal to all three",
                        "Open must always equal High",
                        "Close must always be higher than Open",
                    ],
                    "answer": 0,
                    "explanation": "By definition, the High is the highest recorded trade and Low is the lowest recorded trade within that time bucket, bounding Open and Close.",
                },
                {
                    "id": "spreadsheet-final-q3",
                    "lessonId": "24.3",
                    "question": "When validating imported tabular data against an external reference, why is matching the terminal closing price and row count necessary but not sufficient?",
                    "options": [
                        "Because internal bars could still contain misaligned dates, missing days, or look-ahead price insertions",
                        "Because terminal closing prices change every minute",
                        "Because row count is ignored by backtest engines",
                    ],
                    "answer": 0,
                    "explanation": "Even if endpoints and row counts match, intervening timestamps could skip trading sessions, contain duplicate dates, or include interpolated prices.",
                },
                {
                    "id": "spreadsheet-final-q4",
                    "lessonId": "24.4",
                    "question": "How does Strategy Lab's moving average implementation guarantee causal trade execution compared to a naive spreadsheet formula?",
                    "options": [
                        "It calculates signals at bar t close and queues fills for bar t+1 open rather than assuming instantaneous fills at the signal close",
                        "It multiplies all moving averages by two",
                        "It rounds prices to the nearest dollar",
                    ],
                    "answer": 0,
                    "explanation": "Causal execution enforces realistic chronological lag: an indicator evaluated at the close of day t cannot trade until the open of day t+1.",
                },
                {
                    "id": "spreadsheet-final-q5",
                    "lessonId": "24.5",
                    "question": "A strategy executes 200 round-trip trades per year with an average gross gain of 15 bps per trade. If brokerage commissions and slippage total 25 bps per round trip, what is the strategy's annual net result?",
                    "options": [
                        "A profit of 300 bps",
                        "A net loss of 2,000 bps (-10 bps per trade x 200 trades)",
                        "Break-even at zero bps",
                    ],
                    "answer": 1,
                    "explanation": "Net return per trade = Gross gain (15 bps) - Total friction (25 bps) = -10 bps. Over 200 trades, the cumulative loss is 2,000 bps (-20%), turning an apparent winner into a loss.",
                },
                {
                    "id": "spreadsheet-final-q6",
                    "lessonId": "24.6",
                    "question": "What is the primary benefit of Strategy Lab's content-addressed versioning and strategy naming system?",
                    "options": [
                        "It makes the source code execute 10 times faster",
                        "It enables exact reproducibility and tracking of parameter revisions across multiple research sessions",
                        "It prevents other users on the network from viewing the web page",
                    ],
                    "answer": 1,
                    "explanation": "Content-addressed storage and parameter logging ensure that any published backtest can be reproduced bit-for-bit from its exact code and settings.",
                },
                {
                    "id": "spreadsheet-final-q7",
                    "lessonId": "24.7",
                    "question": "What unique capability does Strategy Lab's AMM Simulator provide that cannot be replicated in a standard spreadsheet cell?",
                    "options": [
                        "Dynamic non-linear slippage and constant-product liquidity pool reserve rebalancing under shifting order size",
                        "Spell-checking stock ticker symbols",
                        "Automatic tax deduction for overseas transactions",
                    ],
                    "answer": 0,
                    "explanation": "Strategy Lab's AMM simulator models constant product invariants (x * y = k), computing precise price impact and impermanent loss dynamically across trade sizes.",
                },
            ],
        }
    ]

    return {
        "id": "spreadsheet-to-strategy-lab",
        "number": 24,
        "title": "From Spreadsheet to Strategy Lab",
        "description": (
            "The bridge from Excel and Google Sheets into programmatic quantitative backtesting. "
            "Learn to avoid look-ahead bias and hidden frictions, map tabular data into Strategy Lab's "
            "causal engine, rebuild moving-average rules, persist versioned strategies, and navigate "
            "the Factor Studio and AMM simulator."
        ),
        "source": "Original bridge curriculum · Institutional quantitative methodology",
        "level": "Beginner → intermediate",
        "icon": "book",
        "studyType": "applied",
        "modules": modules,
        "parts": parts,
        "prerequisites": "None. Soft recommendation: basic familiarity with spreadsheet tables or formulas.",
        "outcomes": [
            "Translate spreadsheet workflows into Strategy Lab's structured data model",
            "Import price series and verify row count and terminal close against reference sheets",
            "Reproduce moving-average crossover strategies with causal chronological execution",
            "Quantify the impact of commissions, slippage, and execution lag on backtest returns",
            "Save, name, and version strategies and navigate Factor Studio and AMM simulators",
        ],
        "readingGuide": (
            "Designed specifically for Excel and spreadsheet users who want to transition to systematic investing. "
            "Every lesson past L2 includes direct interactive code and tool steps. Complete all lessons and the "
            "strategy persistence milestone to graduate into the flagship 32-lesson Strategy Lab track."
        ),
        "resources": [
            {
                "title": "Strategy Lab Research Guide (Markdown)",
                "url": "/course-assets/strategy-lab/README.md",
            },
            {
                "title": "Strategy Lab Research Notebook (Markdown)",
                "url": "/course-assets/strategy-lab/research-notebook.md",
            },
        ],
        "references": [
            {"title": "CFA Institute · Quantitative Methods in Investment Management", "url": "https://www.cfainstitute.org"},
            {"title": "FINRA · Algorithmic Trading Rules and Market Integrity", "url": "https://www.finra.org"},
        ],
        "exams": exams,
        # CS-1 course metadata
        "slug": "spreadsheet-to-strategy-lab",
        "subtitle": "Bridge from Excel into Systematic Quantitative Research",
        "audience_tags": ["spreadsheet", "beginner", "investor", "quant"],
        "estimated_minutes": 90,
        "lesson_count": len(modules),
        "assessment_count": len(exams),
        "completion_criteria": {"lessons_pct": 100, "assessment_pass_pct": 70},
        "certificate": {"enabled": True, "template_id": "strategy-bridge", "verification_required": False},
        "funnel_cta": {
            "label": "Enter The Strategy Lab (32-Lesson Track)",
            "target_course_id": "strategy-lab",
            "secondary_label": "Build Autonomous Stock Bots",
            "secondary_target_course_id": "stock-bots",
        },
        "language": ["en", "id"],
    }
