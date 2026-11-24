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
            "formula": r"\text{Executed Return} \approx \text{Spreadsheet Return} - \text{Friction} - \text{Lag}",
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
                "2. **Neglected Frictions (Costs & Slippage)**: Spreadsheets rarely model bid-ask spreads, exchange fees, or execution slippage. A strategy executing 150 trades a year with an apparent 24% gross gain might look stellar in Excel, but after realistic 30 bps round-trip friction ($150 \\times 30\\text{ bps} = 45\\% = 0.45$), transaction costs wipe out all profits and produce a severe net loss.\n"
                "3. **Formula Drift & Overfitting**: Cell drag-and-drop easily introduces copy-paste formula errors that go unnoticed in large sheets.\n\n"
                "$$\n"
                r"\text{Executed Return} \approx \text{Spreadsheet Return} - \text{Friction} - \text{Lag}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "An analyst tests a 10-day momentum rule on a stock trading at $100. In Excel, the sheet assumes buying at the exact closing price whenever the day's close exceeds yesterday's high, generating a 24.0% annual gross return across 150 trades.\n\n"
                "When ported to Strategy Lab's causal engine with realistic 15 bps commissions and 15 bps slippage (30 bps total round-trip friction), two things happen: first, orders execute on the open of the following bar; second, 150 round-trip trades generate $150 \\times 30\\text{ bps} = 45.0\\%$ in direct transaction friction. Subtracting 45.0% friction from 24.0% gross return yields a net result of −21.0%. The spreadsheet did not find alpha; it found accounting friction.\n\n"
                "## Work through it yourself\n\n"
                "1. Audit your spreadsheet formulas: verify whether any trade decision references closing prices of the same bar it claims to fill on.\n"
                "2. Subtract a minimum 30 bps (0.30%) round-trip fee from every single transaction row in your sheet.\n"
                "3. Observe whether your perceived edge survives before risking capital.\n\n"
                "### In the sandbox\n\n"
                "Run the Python snippet to see how naive same-bar calculation differs from real delayed execution."
            ),
            "exercise": question(
                "Which error is the most common cause of unrealistic profitability in spreadsheet trading backtests?",
                [
                    "Formatting cells with Calibri font rather than monospace Courier New in workbook reports",
                    "Look-ahead bias where a buy signal at today's close is assumed to fill at today's close with zero lag or fees",
                    "Entering more than two decimal precision places across historical financial asset price columns",
                ],
                1,
                "Look-ahead bias occurs when a backtest uses data from the future or assumes instant execution at the signal price without friction or delay.",
            ),
            "exercises": [
                question(
                    "Which error causes unrealistic profitability in spreadsheet backtests?",
                    [
                        "Selecting Calibri font rather than Courier New across all spreadsheet workbook reporting sheets",
                        "Look-ahead bias assuming instant same-bar execution without fees or delay",
                        "Storing prices with three decimal places instead of rounding to whole dollar integers in cells",
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
                {"title": "CFA Institute · A Primer on Machine Learning and Backtesting", "url": "https://www.cfainstitute.org/research/foundation/publications"},
                {"title": "U.S. SEC · Staff Report on Algorithmic Trading in U.S. Capital Markets", "url": "https://www.sec.gov/files/tm-sts-algo-trading-market-structure-2020.pdf"},
            ],
        },
        {
            "id": "24.2",
            "part": "1",
            "title": "Mapping columns: from your sheet to the Strategy Lab data model",
            "subtitle": "Translate rows and columns into standardized OHLCV bar structures.",
            "minutes": 12,
            "objective": "Map spreadsheet columns (time, open, high, low, close, volume) into Strategy Lab's structured data model.",
            "kind": "fundamentals",
            "formula": r"\text{Bar}_t = \{\text{time}, \text{open}, \text{high}, \text{low}, \text{close}, \text{volume}\}",
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
                "To port your dataset into Strategy Lab, your tabular data must include the required columns:\n"
                "- `time`: ISO-8601 format (`YYYY-MM-DD` or timestamp). Avoid locale-dependent strings like `03/04/25`.\n"
                "- `open`: The price of the first transaction in the bar.\n"
                "- `high` and `low`: The highest and lowest transaction prices during the interval.\n"
                "- `close`: The final recorded transaction price for the bar.\n"
                "- `volume`: Total number of shares or contracts traded.\n\n"
                "$$\n"
                r"\mathrm{Bar}_t = (\tau_t, O_t, H_t, L_t, C_t, V_t) \quad \text{where } L_t \le \min(O_t, C_t) \le \max(O_t, C_t) \le H_t"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A spreadsheet user exports daily prices from Yahoo Finance where columns are named `Date`, `Open`, `High`, `Low`, `Close`, `Adj Close`, and `Volume`. Strategy Lab requires `time`, `open`, `high`, `low`, `close`, `volume`.\n\n"
                "Mapping these requires confirming that `high` is always $\\ge$ both `open` and `close`, and that `low` is always $\\le$ both. Any row where $H_t < L_t$ is rejected during CSV import with an actionable validation error, preventing corrupt data from entering the engine.\n\n"
                "## Work through it yourself\n\n"
                "1. Open your exported CSV in a text editor or spreadsheet.\n"
                "2. Standardize column headers to: `time`, `open`, `high`, `low`, `close`, `volume`.\n"
                "3. Ensure dates are sorted chronologically from earliest to latest.\n\n"
                "### In the sandbox\n\n"
                "Inspect how the Python script converts a raw dictionary row into a validated bar structure."
            ),
            "exercise": question(
                "Which invariant must ALWAYS hold true for a valid price bar (OHLC)?",
                [
                    "Close must equal Open on every trading bar regardless of intra-session volatility or order volume",
                    "Low <= Open, Close <= High (High is maximum, Low is minimum)",
                    "Trading volume must be zero during trend reversals to confirm price directional continuity",
                ],
                1,
                "The High must be the highest price of the interval and the Low must be the lowest, enclosing both Open and Close.",
            ),
            "exercises": [
                question(
                    "Which invariant must hold true for a valid OHLC bar?",
                    [
                        "Close must equal Open on every trading bar regardless of intra-session volatility or order volume",
                        "Low <= min(Open, Close) and High >= max(Open, Close)",
                        "Trading volume must be zero during trend reversals to confirm price directional continuity",
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
                "When simulating data or importing via the platform CLI (`backend/scripts/import_data.py`), Strategy Lab loads a simulation horizon of `years × 252` bars (standard international equity calendar). Note that the Indonesia Stock Exchange (IDX) typically has ~239 trading days per year due to statutory holidays and joint leave (*cuti bersama*).\n\n"
                "Upon uploading to Strategy Lab, the summary card displays: `252 bars | 2026-01-02 to 2026-12-30 | Last: 10,250`. Because the row count and terminal close match exactly, you have verified data parity. If the row count showed 248 instead, 4 bars were lost during import—often caused by blank lines or malformed commas.\n\n"
                "## Work through it yourself\n\n"
                "1. Note the exact row count and last closing price of your spreadsheet.\n"
                "2. Load the dataset in Strategy Lab or import via `backend/scripts/import_data.py`.\n"
                "3. Verify that both numbers agree before writing strategy code.\n\n"
                "### In the sandbox\n\n"
                "Run the verification script to inspect how start date, end date, and terminal close are checked."
            ),
            "exercise": question(
                "Why must you verify the terminal closing price and row count after importing data into Strategy Lab?",
                [
                    "To customize chart line colors and grid background shading in the visual reporting dashboard",
                    "To confirm that no bars were dropped, corrupted, or misaligned during CSV ingestion",
                    "To trigger automated margin leverage expansion protocols with institutional clearing brokers",
                ],
                1,
                "Reconciling row count and the last closing price proves that the backtest engine is operating on the exact same data as your spreadsheet.",
            ),
            "exercises": [
                question(
                    "Why verify terminal closing price and row count after importing data?",
                    [
                        "To customize visual chart line colors and grid background shading in the reporting dashboard",
                        "To confirm no bars were dropped or misaligned during ingestion",
                        "To trigger automated margin leverage expansion protocols with institutional clearing brokers",
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
            "subtitle": "Translate =AVERAGE(C32:C51) into a clean, testable Strategy Lab signal.",
            "minutes": 15,
            "objective": "Translate a classic 20-day/50-day moving average crossover rule from spreadsheet formulas into a Strategy Lab signal function.",
            "kind": "fundamentals",
            "formula": r"\text{Signal}_t = \begin{cases} 1 & \text{if } \text{SMA}_{20}(t) > \text{SMA}_{50}(t) \\ 0 & \text{otherwise} \end{cases}",
            "code": (
                "# Translating Excel =IF(AVERAGE(C32:C51) > AVERAGE(C2:C51), 1, 0)\n"
                "# In Strategy Lab, built-in indicators evaluate causally without NaN during warm-up\n"
                "def strategy(data):\n"
                "    return sma(data['close'], 20) > sma(data['close'], 50)\n"
                "\n"
                "print('Strategy logic defined cleanly with built-in sma indicator!')\n"
            ),
            "content": (
                "## The idea\n\n"
                "In a spreadsheet, calculating a 20-day Simple Moving Average at row 51 requires `=AVERAGE(C32:C51)`, while a 50-day average requires `=AVERAGE(C2:C51)`. A crossover is coded as `=IF(AVERAGE(C32:C51)>AVERAGE(C2:C51), 1, 0)`. If someone drags or sorts the sheet, formulas corrupt silently.\n\n"
                "In Strategy Lab, the same logic is expressed as a **declarative signal function**. You define the logic once, and the engine evaluates it across all time periods with strict chronological ordering:\n\n"
                "```python\n"
                "def strategy(data):\n"
                "    return sma(data['close'], 20) > sma(data['close'], 50)\n"
                "```\n\n"
                "Strategy Lab's in-app `sma` averages available historical bars causally without producing `NaN` errors during warm-up.\n\n"
                "$$\n"
                r"\mathrm{SMA}_k(t) = \frac{1}{k}\sum_{i=0}^{k-1} C_{t-i}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "Consider a 20-day and 50-day moving average crossover. In Excel, row 51 evaluates `=IF(AVERAGE(C32:C51)>AVERAGE(C2:C51), 1, 0)`.\n\n"
                "In Strategy Lab, `sma(data['close'], 20) > sma(data['close'], 50)` produces the exact same boolean array. The crucial difference is execution: Strategy Lab automatically executes the position on the **next open** ($t+1$), removing the execution look-ahead leakage that plagues spreadsheet models. Full-sample look-ahead leaks (such as fitting hyperparameters across the full dataset) are validated separately in the Research Registry.\n\n"
                "## Work through it yourself\n\n"
                "1. Inspect your moving average formula in Excel.\n"
                "2. Rewrite it in Strategy Lab using `sma(data['close'], 20) > sma(data['close'], 50)`.\n"
                "3. Click **Run experiment** and compare the equity curve.\n\n"
                "### In the sandbox\n\n"
                "Run the Python strategy function template and verify that the signal produces clean true/false values."
            ),
            "exercise": question(
                "What is the key advantage of writing a strategy function in Strategy Lab compared to dragging formulas in Excel?",
                [
                    "Spreadsheet calculation engines crash when processing rolling statistical window averages exceeding ten rows",
                    "Strategy Lab enforces chronological execution and causal separation between signal and execution automatically",
                    "Strategy Lab guarantees positive risk-adjusted returns and eliminates all drawdown risk across market conditions",
                ],
                1,
                "Strategy Lab evaluates rules chronologically and fills orders at the next bar's open, eliminating accidental formula dragging errors and same-bar execution leakage.",
            ),
            "exercises": [
                question(
                    "What is the advantage of Strategy Lab over dragging formulas in Excel?",
                    [
                        "Spreadsheet calculation engines crash when processing rolling statistical window averages exceeding ten rows",
                        "Strategy Lab enforces chronological order and causal execution automatically",
                        "Strategy Lab guarantees positive risk-adjusted returns and eliminates all drawdown risk across market conditions",
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
                "Strategy Lab models execution costs in **basis points per fill**. By default, the engine applies 5 bps commission and 3 bps slippage (8 bps total per fill, meaning 16 bps per complete entry-and-exit round trip). Strategy Lab operates on an all-in long or cash basis.\n\n"
                "There are three mathematical drivers of this difference:\n"
                "1. **Execution Timing**: Spreadsheets assume you enter at the signal bar's close ($P_t$). Strategy Lab enters at the open of bar $t+1$ ($O_{t+1}$). If prices gap up on the open, your actual entry price is higher.\n"
                "2. **Transaction Drag (Fills vs Round-Trips)**: Strategy Lab deducts broker commissions and bid-ask spread costs on every fill (entry and exit).\n"
                "3. **Position Sizing Caps**: Spreadsheets often reinvest 100% of capital with infinite compounding, ignoring cash reserves.\n\n"
                "$$\n"
                r"\Delta_{\text{pnl}} = \sum_{i=1}^M \left[(P_{\text{sheet, fill}} - P_{\text{actual, fill}}) - \text{commission}_i - \text{slippage}_i\right]"
                "\n$$\n\n"
                "## A worked example\n\n"
                "In Excel, a breakout strategy takes 60 round-trip trades (120 fills) a year and reports $1,500 in total gross profit. The spreadsheet assumes zero friction.\n\n"
                "In Strategy Lab, the engine applies standard institutional assumptions: $12.50 commission and $7.50 estimated slippage per round trip ($20 total per round trip). Across 60 round trips, friction consumes:\n"
                "$$\\text{Friction} = 60 \\times (\\$12.50 + \\$7.50) = 60 \\times \\$20 = \\$1,200$$\n"
                "The actual net profit in Strategy Lab is $\\$1,500 - \\$1,200 = \\$300$. Strategy Lab prevents you from deploying an unprofitable high-churn strategy with real capital.\n\n"
                "## Work through it yourself\n\n"
                "1. Check the trade count in your Strategy Lab backtest summary.\n"
                "2. Multiply the fill count by your broker's actual fee schedule (e.g. 8 bps per fill = 16 bps round trip).\n"
                "3. Reconcile the net Sharpe ratio after costs.\n\n"
                "### In the sandbox\n\n"
                "Run the script to see how 60 trades of friction erase 80% of naive spreadsheet profit."
            ),
            "exercise": question(
                "If a strategy generates $1,500 gross profit across 60 trades, but fees and slippage cost $20 per trade, what is the true net profit?",
                [
                    "Gross profits reported by spreadsheet backtests remain unchanged because broker rebates offset transaction costs",
                    "$300",
                    "-$500",
                ],
                1,
                "Total friction = 60 * $20 = $1,200. Net profit = $1,500 − $1,200 = $300.",
            ),
            "exercises": [
                question(
                    "Gross profit is $1,500 across 60 trades. Frictions cost $20 per trade. What is net profit?",
                    [
                        "Gross profits reported by spreadsheet backtests remain unchanged because broker rebates offset transaction costs",
                        "$300",
                        "-$500",
                    ],
                    1,
                    "Total friction = 60 * $20 = $1,200. Net profit = $1,500 − $1,200 = $300.",
                ),
            ],
            "terms": [
                {"term": "Adverse Selection", "definition": "The tendency for market orders to execute at unfavorable prices when liquidity providers adjust quotes ahead of incoming flow."},
                {"term": "Net Return", "definition": "The true economic return realized after subtracting all commissions, financing costs, and market impact."},
            ],
            "references": [
                {"title": "FINRA · Rule 5310 Best Execution and Interpositioning", "url": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/5310"},
            ],
        },
        {
            "id": "24.6",
            "part": "2",
            "title": "Saving, naming, and re-running",
            "subtitle": "Persist your strategy code, record audit metadata, and version your experiments.",
            "minutes": 10,
            "objective": "Save and name your strategy in Strategy Lab as a named snapshot, and manage experiment versions in the Research Registry.",
            "kind": "fundamentals",
            "formula": r"\text{Strategy Snapshot} \to \text{Workspace Record} \quad \land \quad \text{Experiment Lineage} \in \text{/research}",
            "code": (
                "# Simulating Strategy Lab's snapshot naming and registry tracking\n"
                "strategy_record = {\n"
                "    'name': 'SMA-20-Crossover',\n"
                "    'snapshot_id': 'snap_c8f309a1',\n"
                "    'registry_path': '/research',\n"
                "    'created_at': '2026-11-22T10:00:00Z',\n"
                "}\n"
                "print('Persisted Strategy Snapshot:', strategy_record['name'], 'id:', strategy_record['snapshot_id'])\n"
                "print('Research Registry lineage path:', strategy_record['registry_path'])\n"
            ),
            "content": (
                "## The idea\n\n"
                "In traditional spreadsheets, maintaining versions usually means messy file names like `strategy_v2_final_FINAL_edit3.xlsx`. You can never be sure which file produced which result.\n\n"
                "Strategy Lab replaces this with **named snapshots** and the **Research Registry ([/research](/research))**:\n"
                "- In Strategy Lab, clicking **Save** creates a named snapshot of your current code and parameters in your workspace.\n"
                "- Full experiment versioning, parameter lineage, and automated look-ahead testing live in the **Research Registry** at [/research](/research).\n"
                "- You can re-run past versions anytime, ensuring 100% scientific reproducibility.\n\n"
                "$$\n"
                r"\mathrm{SnapshotID} = \mathrm{SHA256}(\mathrm{Code} \parallel \mathrm{Parameters})"
                "\n$$\n\n"
                "## A worked example\n\n"
                "You build a 20-day trend-following strategy and name it `SMA-20-Crossover`. In Strategy Lab, you click **Save**.\n\n"
                "The system creates a named snapshot in your workspace. When you want to publish or systematically compare variations (e.g. testing 20-day vs 50-day windows), the Research Registry at `/research` tracks each experiment run, logs backtest metrics, and checks for data snooping across iterations.\n\n"
                "## Work through it yourself\n\n"
                "1. Open the Strategy Lab code editor.\n"
                "2. Name your strategy `My-First-Lab-Strategy`.\n"
                "3. Click **Save** to persist the snapshot in your workspace.\n"
                "4. Visit [/research](/research) to view your experiment registry.\n\n"
                "### In the sandbox\n\n"
                "Run the script to observe how strategy snapshots and registry paths are structured."
            ),
            "exercise": question(
                "What is the function of saving a strategy snapshot in Strategy Lab and managing it in the Research Registry (/research)?",
                [
                    "To permanently overwrite all prior strategy iterations and immediately purge local workspace historical backtest database records",
                    "To record a named snapshot in your workspace and track experiment lineage and reproducibility in /research",
                    "To automatically submit the quantitative strategy source code to financial regulatory filing portals",
                ],
                1,
                "Saving in Strategy Lab creates a named snapshot, while /research tracks experiment lineage and parameter reproducibility.",
            ),
            "exercises": [
                question(
                    "What is the function of saving a strategy snapshot and managing it in /research?",
                    [
                        "To permanently overwrite all prior strategy iterations and immediately purge local workspace historical backtest database records",
                        "To record a named snapshot in your workspace and track experiment lineage and reproducibility in /research",
                        "To automatically submit the quantitative strategy source code to financial regulatory filing portals",
                    ],
                    1,
                    "Saving creates a named snapshot, while /research tracks experiment lineage and reproducibility.",
                ),
            ],
            "terms": [
                {"term": "Named Snapshot", "definition": "A persisted state of strategy code and configuration captured at a specific point in time in your workspace."},
                {"term": "Research Registry", "definition": "Quanta's central repository (/research) for tracking quantitative experiment lineage, backtest metrics, and reproducibility."},
            ],
            "references": [
                {"title": "National Academies of Sciences · Reproducibility and Replicability in Science", "url": "https://nap.nationalacademies.org/catalog/25303/reproducibility-and-replicability-in-science"},
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
            "formula": r"\text{Factor Studio: } \text{/lab?tool=factors} \quad \land \quad \text{AMM Simulator: } \text{/lab?tool=amm}",
            "code": (
                "# Orientation: Factor Studio (/lab?tool=factors) and AMM Simulator (/lab?tool=amm)\n"
                "factor_tool_url = '/lab?tool=factors'\n"
                "amm_tool_url = '/lab?tool=amm'\n"
                "paper_trading_url = '/simulator'\n"
                "print('Factor Studio (regressions with HAC errors):', factor_tool_url)\n"
                "print('AMM Simulator (constant-product curves):     ', amm_tool_url)\n"
                "print('Paper Trading Terminal:                      ', paper_trading_url)\n"
            ),
            "content": (
                "## The idea\n\n"
                "Congratulations! You have bridged from static spreadsheets into programmatic strategy testing. Now three specialized environments in Quanta await your exploration:\n\n"
                "1. **Factor Studio ([/lab?tool=factors](/lab?tool=factors))**: Fit multi-factor cross-sectional regressions with HAC (Heteroskedasticity and Autocorrelation Consistent) standard errors on synthetic returns, ranking assets by Value, Quality, and Momentum.\n"
                "2. **AMM Simulator ([/lab?tool=amm](/lab?tool=amm))**: Explore decentralized automated market maker (AMM) mechanics governed by constant product invariants ($x \\cdot y = k$). Simulate dynamic slippage, pool reserves, fee yields, and impermanent loss under shifting trade sizes.\n"
                "3. **Paper Trading Terminal ([/simulator](/simulator))**: Forward test your strategies in a simulated market execution environment before allocating real capital.\n\n"
                "$$\n"
                r"\text{Factor Studio: } R_p = \alpha + \sum \beta_j F_j \quad \longleftrightarrow \quad \text{AMM: } x \cdot y = k"
                "\n$$\n\n"
                "## A worked example\n\n"
                "In Factor Studio ([/lab?tool=factors](/lab?tool=factors)), you run factor regressions on a universe of equity assets, evaluating statistical significance using HAC-adjusted standard errors.\n\n"
                "In the AMM Simulator ([/lab?tool=amm](/lab?tool=amm)), you deposit 50 ETH and 100,000 USDC into a pool. When external price shocks occur, arbitrageurs trade against the constant-product curve, altering reserves and generating fees. You observe the exact trade-off between fee yield and impermanent loss.\n\n"
                "## Work through it yourself\n\n"
                "1. Explore Factor Studio at [/lab?tool=factors](/lab?tool=factors).\n"
                "2. Explore the AMM simulator at [/lab?tool=amm](/lab?tool=amm).\n"
                "3. Forward-test execution in the paper trading terminal at [/simulator](/simulator).\n"
                "4. Proceed to the 32-lesson [The strategy lab](/curriculum/strategy-lab) track.\n\n"
                "### In the sandbox\n\n"
                "Run the script to review the URLs and roles of Factor Studio, AMM Simulator, and Paper Trading."
            ),
            "exercise": question(
                "Where in Quanta do you fit multi-factor regressions with HAC standard errors, and where do you simulate AMM liquidity curves?",
                [
                    "Factor regressions run at /lab?tool=factors, while AMM pool simulations run at /lab?tool=amm",
                    "Both factor regressions and AMM liquidity curve simulations run exclusively inside the /simulator paper trading terminal",
                    "All multi-factor and automated market maker analytics require exporting CSV files into commercial spreadsheet software",
                ],
                0,
                "Factor Studio is located at /lab?tool=factors (regressions with HAC errors), while AMM simulation is at /lab?tool=amm.",
            ),
            "exercises": [
                question(
                    "Where do you fit factor regressions with HAC errors and where do you simulate AMMs?",
                    [
                        "Factor regressions run at /lab?tool=factors, while AMM pool simulations run at /lab?tool=amm",
                        "Both factor regressions and AMM liquidity curve simulations run exclusively inside the /simulator paper trading terminal",
                        "All multi-factor and automated market maker analytics require exporting CSV files into commercial spreadsheet software",
                    ],
                    0,
                    "Factor Studio is at /lab?tool=factors, AMM Simulator is at /lab?tool=amm, and /simulator is paper trading.",
                ),
            ],
            "terms": [
                {"term": "Factor Studio", "definition": "Quanta's tool (/lab?tool=factors) for multi-factor cross-sectional regressions with HAC standard errors."},
                {"term": "AMM Simulator", "definition": "Quanta's decentralized liquidity simulator (/lab?tool=amm) modeling constant product reserves (x * y = k) and impermanent loss."},
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
            "version": 3,
            "description": "Comprehensive assessment on translating spreadsheet workflows into systematic code, causal ordering, and Strategy Lab tools.",
            "moduleIds": [m["id"] for m in modules],
            "questions": [
                {
                    "id": "spreadsheet-final-q1",
                    "lessonId": "24.1",
                    "question": "In algorithmic backtesting, why does look-ahead bias invalidate historical trading performance?",
                    "options": [
                        "It compresses the time index of the output chart, causing candlestick bars to render out of chronological sequence",
                        "It calculates trading decisions using price or volume data that was not yet observable at the trade execution bar",
                        "It requires excessive memory on the server, causing background processes to abort without saving backtest logs",
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
                        "Open must always equal High, while Close must always equal Low to maintain symmetry across daily price ranges",
                        "Close must always be higher than Open to prevent the calculation engine from encountering negative variance values",
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
                        "Because terminal closing prices fluctuate with live streaming ticks even after historical session markets close",
                        "Because total bar row count is completely ignored by quantitative backtest engines during data ingestion routines",
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
                        "It artificially doubles all moving average values to compensate for commercial clearinghouse settlement lag across holiday weekend sessions",
                        "It rounds all historical prices to whole dollar integers to eliminate fractional penny discrepancies during trade execution",
                    ],
                    "answer": 0,
                    "explanation": "Causal execution enforces realistic chronological lag: an indicator evaluated at the close of day t cannot trade until the open of day t+1.",
                },
                {
                    "id": "spreadsheet-final-q5",
                    "lessonId": "24.5",
                    "question": "A strategy executes 200 round-trip trades per year with an average gross gain of 15 bps per trade. If brokerage commissions and slippage total 25 bps per round trip, what is the strategy's annual net result?",
                    "options": [
                        "A profit of 300 bps across annual turnover periods",
                        "A net loss of 2,000 bps (-10 bps per trade x 200 trades)",
                        "Break-even at zero bps after applying automated broker volume rebate credits",
                    ],
                    "answer": 1,
                    "explanation": "Net return per trade = Gross gain (15 bps) - Total friction (25 bps) = -10 bps. Over 200 trades, the cumulative loss is 2,000 bps (-20%), turning an apparent winner into a loss.",
                },
                {
                    "id": "spreadsheet-final-q6",
                    "lessonId": "24.6",
                    "question": "What is the function of saving a strategy snapshot in Strategy Lab and managing it in the Research Registry (/research)?",
                    "options": [
                        "It permanently overwrites all prior strategy iterations and immediately purges local workspace historical backtest database records",
                        "It records a named snapshot in your workspace and tracks experiment lineage and reproducibility in /research",
                        "It prevents other network users from inspecting public visual charts by enforcing local browser encryption keys",
                    ],
                    "answer": 1,
                    "explanation": "Saving in Strategy Lab creates a named snapshot, while /research tracks experiment lineage and parameter reproducibility.",
                },
                {
                    "id": "spreadsheet-final-q7",
                    "lessonId": "24.7",
                    "question": "Where are multi-factor regressions with HAC errors and AMM liquidity curve simulations located in Quanta?",
                    "options": [
                        "Factor Studio is at /lab?tool=factors, AMM Simulator is at /lab?tool=amm, and /simulator is paper trading",
                        "Both Factor Studio regressions and AMM constant product simulations are accessed exclusively inside the /simulator terminal",
                        "All multi-factor and automated market maker features require running local offline Python notebooks without web access",
                    ],
                    "answer": 0,
                    "explanation": "Factor Studio is at /lab?tool=factors, AMM Simulator is at /lab?tool=amm, and /simulator is the paper-trading terminal.",
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
            {"title": "CFA Institute · Code of Ethics and Standards of Professional Conduct", "url": "https://www.cfainstitute.org/ethics-standards/codes/code-of-ethics-standards-of-professional-conduct"},
            {"title": "FINRA · Rule 5310 Best Execution and Interpositioning", "url": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/5310"},
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
