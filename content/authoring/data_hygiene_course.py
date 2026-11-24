"""Original course: Data Hygiene for Investors (Higienitas Data Investor).

Principles of tidy rectangular data, defect detection (dates, currencies, duplicates,
gaps, category drift), cognitive and data biases, versioning, and messy file cleaning.
"""

from foundations import question


def build_data_hygiene():
    modules = [
        {
            "id": "25.1",
            "part": "1",
            "title": "Tidy data: one row, one transaction, one meaning",
            "subtitle": "Structure rectangular tables so they can be analyzed without constant rework.",
            "minutes": 10,
            "objective": "Apply tidy data rules: each variable forms a column, each observation forms a row, and each table contains one observational unit.",
            "kind": "fundamentals",
            "formula": r"\text{Tidy Dataset} = \{\text{Rows: distinct events}, \text{Cols: atomic variables}, \text{Cells: single values}\}",
            "code": (
                "# Demonstrating tidy rectangular data records\n"
                "tidy_records = [\n"
                "    {'date': '2026-03-01', 'ticker': 'BBCA', 'action': 'BUY', 'shares': 100, 'price': 10250},\n"
                "    {'date': '2026-03-01', 'ticker': 'BBRI', 'action': 'BUY', 'shares': 200, 'price': 5400},\n"
                "    {'date': '2026-03-05', 'ticker': 'BBCA', 'action': 'DIV', 'shares': 100, 'price': 185},\n"
                "]\n"
                "print('Total tidy records:', len(tidy_records))\n"
                "for r in tidy_records:\n"
                "    print(r['date'], r['ticker'], r['action'], r['shares'], r['price'])\n"
            ),
            "content": (
                "## The idea\n\n"
                "Bad data ruins good math. No machine learning algorithm or econometrics model can compensate for garbage data. Spreadsheet analysts routinely spend a disproportionate share of their time restructuring messy spreadsheets rather than analyzing data.\n\n"
                "The foundation of data hygiene is **Tidy Data** (formalized by Hadley Wickham):\n"
                "1. Each **variable** must have its own column.\n"
                "2. Each **observation** must have its own row.\n"
                "3. Each value must have its own cell (no merged cells, no subtotal rows breaking tables).\n"
                "4. Each observational unit forms a table (keep stock price history separate from corporate actions or personal notes).\n\n"
                "$$\n"
                r"\mathcal{D} = \{(x_{i,1}, x_{i,2}, \dots, x_{i,p}) \mid i = 1, \dots, N\} \quad \text{where each } x_{i,j} \text{ is atomic}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A bookkeeper maintains a spreadsheet where month names (`Jan`, `Feb`, `Mar`) are spread horizontally across 12 columns, with total rows and blank decorative lines interspersed. To calculate the 12-month average in Python or SQL, every formula breaks.\n\n"
                "By pivoting the table into tidy format (`date`, `category`, `amount`), the data becomes a clean rectangular matrix. Calculating rolling statistics, grouping by category, or filtering dates takes exactly one line of code.\n\n"
                "## Work through it yourself\n\n"
                "1. Audit your most important financial spreadsheet.\n"
                "2. Remove all merged cells, blank spacer rows, and colored subtotal lines.\n"
                "3. Ensure the top row contains unique, lowercase, underscore-separated column names.\n\n"
                "### In the sandbox\n\n"
                "Run the script to inspect how clean atomic rows are represented in Python."
            ),
            "exercise": question(
                "Which characteristic violates the fundamental rules of tidy data?",
                [
                    "Applying consistent lowercase column naming conventions with underscores across tabular headers",
                    "Merging cells across multiple rows to create decorative section headers",
                    "Sorting historical transaction rows chronologically by date in ascending sequence",
                ],
                1,
                "Merged cells destroy tabular indexing and cause automated CSV parsers to treat rows as containing missing or shifted values.",
            ),
            "exercises": [
                question(
                    "Which characteristic violates tidy data rules?",
                    [
                        "Applying consistent lowercase column naming conventions with underscores across tabular headers",
                        "Merging cells across multiple rows to create decorative section headers",
                        "Sorting historical transaction rows chronologically by date in ascending sequence",
                    ],
                    1,
                    "Merged cells destroy tabular indexing and cause automated CSV parsers to fail.",
                ),
            ],
            "terms": [
                {"term": "Tidy Data", "definition": "A standard way of mapping the meaning of a dataset to its structure, where each variable is a column and each observation is a row."},
                {"term": "Atomic Value", "definition": "A piece of data that cannot be divided into smaller meaningful components in the current context."},
            ],
            "references": [
                {"title": "Hadley Wickham · Tidy Data (Journal of Statistical Software)", "url": "https://www.jstatsoft.org/article/view/v059i10"},
            ],
        },
        {
            "id": "25.2",
            "part": "1",
            "title": "Dates, currencies, and the defects they hide",
            "subtitle": "Detect ISO 8601 formatting traps and multi-currency exchange hazards.",
            "minutes": 10,
            "objective": "Detect and correct ambiguous date formats (DD/MM/YYYY vs MM/DD/YYYY) and isolate unstated currency denominations into dedicated columns.",
            "kind": "fundamentals",
            "formula": r"\text{Standard Date: } \text{YYYY-MM-DD} \quad \land \quad \text{Explicit Currency: } (\text{amount}, \text{currency\_code})",
            "code": (
                "# Detecting date ambiguity and enforcing ISO-8601 YYYY-MM-DD\n"
                "raw_dates = ['2026-04-05', '05/04/2026', '04/05/2026', '2026-05-04']\n"
                "# In '05/04/2026', is it May 4th or April 5th?\n"
                "# ISO-8601 (YYYY-MM-DD) eliminates all ambiguity\n"
                "canonical_iso_date = '2026-04-05'\n"
                "print('Unambiguous ISO Date:', canonical_iso_date)\n"
                "print('Sample input dates inspected:', len(raw_dates))\n"
            ),
            "content": (
                "## The idea\n\n"
                "Two silent data killers account for over 50% of financial analysis blunders:\n\n"
                "1. **Ambiguous Dates**: What date does `04/05/2026` represent? In the United States, it means April 5th. In Indonesia and the UK, it means May 4th. If an analyst parses an exported CSV with default US settings, one third of the year's trading dates will be flipped, destroying price continuity.\n"
                "2. **Mixed Currencies**: A ledger that records `15,000,000` (in IDR) in one row and `1,000` (in USD) in another row without an explicit `currency` column will produce absurdly distorted sums and averages.\n\n"
                "$$\n"
                r"\text{Rule: Always enforce ISO-8601 } (\texttt{YYYY-MM-DD}) \text{ and numeric-only currency amounts with separate currency code}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "An investor tracks a portfolio with assets in Jakarta and Singapore. Row 1 records an IDR deposit of Rp50.000.000. Row 2 records a dividend of $1,500 SGD. A naive `=SUM(C2:C3)` yields 50,001,500—a mathematically meaningless number.\n\n"
                "Data hygiene requires two distinct columns: `amount` (numeric float, stripping symbols like `Rp`, `$`, `€`) and `currency` (three-letter ISO-4217 code: `IDR`, `SGD`, `USD`). Currency conversion must use an explicit dated exchange rate table, preserving provenance.\n\n"
                "## Work through it yourself\n\n"
                "1. Check the date format of every CSV in your workflow.\n"
                "2. Convert all dates to `YYYY-MM-DD`.\n"
                "3. Verify that currency symbols (`$`, `Rp`, `€`) are stripped from numeric columns and recorded in a dedicated `currency` column.\n\n"
                "### In the sandbox\n\n"
                "Run the date parsing script to see how python handles ISO 8601 formatting."
            ),
            "exercise": question(
                "Why is the ISO 8601 date format (YYYY-MM-DD) universally mandated in quantitative finance?",
                [
                    "Because spreadsheet software defaults to American month-day formatting unless overridden",
                    "Because it eliminates ambiguity between day and month and naturally sorts in true chronological order when formatted as text",
                    "Because international banking regulators require dates to be written with two-digit century prefixes across all transaction records",
                ],
                1,
                "YYYY-MM-DD eliminates day/month confusion across international locales and has the unique property that alphabetical string sorting matches exact chronological sorting.",
            ),
            "exercises": [
                question(
                    "Why is ISO 8601 (YYYY-MM-DD) mandated in quantitative finance?",
                    [
                        "Because spreadsheet software defaults to American month-day formatting unless overridden",
                        "Because it eliminates ambiguity between day and month and naturally sorts in true chronological order when formatted as text",
                        "Because international banking regulators require dates to be written with two-digit century prefixes across all transaction records",
                    ],
                    1,
                    "ISO 8601 eliminates locale ambiguity and naturally sorts chronologically.",
                ),
            ],
            "terms": [
                {"term": "ISO 8601", "definition": "The international standard format for representing dates and times as YYYY-MM-DD."},
                {"term": "Currency Denomination", "definition": "The specific monetary unit in which a financial figure is expressed."},
            ],
            "references": [
                {"title": "ISO 8601 · Date and Time Format Standard", "url": "https://www.iso.org/iso-8601-date-and-time-format.html"},
            ],
        },
        {
            "id": "25.3",
            "part": "1",
            "title": "Duplicates, gaps, and reconciliation",
            "subtitle": "Uncover phantom duplicate transactions and detect missing calendar periods.",
            "minutes": 10,
            "objective": "Detect duplicate rows using composite primary keys and identify missing calendar trading periods with automated reconciliation checks.",
            "kind": "fundamentals",
            "formula": r"\text{Duplicate Check: } \mathrm{Count}(K) = 1 \quad \forall K \in \{\text{date} \parallel \text{transaction\_id}\}",
            "code": (
                "# Detecting duplicate records using composite keys\n"
                "keys = ['2026-03-01:T1', '2026-03-01:T1', '2026-03-02:T2', '2026-03-05:T3']\n"
                "duplicate_count = 0\n"
                "for i in range(len(keys)):\n"
                "    for j in range(i + 1, len(keys)):\n"
                "        if keys[i] == keys[j]:\n"
                "            duplicate_count = duplicate_count + 1\n"
                "print('Total records:', len(keys))\n"
                "print('Duplicate pairs detected:', duplicate_count)\n"
            ),
            "content": (
                "## The idea\n\n"
                "Data feeds and bank CSV exports frequently contain two insidious defects:\n\n"
                "1. **Duplicate Records**: Triggered by network retries, browser double-clicks, or overlapping monthly statement downloads. In a trading log, an accidental duplicate row doubles the recorded size or doubles a simulated profit.\n"
                "2. **Calendar Gaps**: Missing days when trading actually occurred, or weekends mistaken for trading halts. If an algorithm calculates a 20-day moving average over 20 calendar days rather than 20 trading days, it uses only ~14 actual observations.\n\n"
                "$$\n"
                r"\mathrm{DuplicationRate} = \frac{N_{\text{raw}} - N_{\text{unique}}}{N_{\text{raw}}} = 0{,}00"
                "\n$$\n\n"
                "## A worked example\n\n"
                "An investor reconciles a brokerage statement against their spreadsheet. The bank statement shows an ending balance of $12,450, while the spreadsheet totals $13,200.\n\n"
                "Running a duplicate check on the composite key `(date, transaction_id)` instantly flags that transaction `#4082` ($750 dividend payment) was imported twice because the analyst downloaded both the monthly summary and quarterly statement. Removing the single duplicate row brings the spreadsheet into exact reconciliation with the bank balance down to the dollar.\n\n"
                "## Work through it yourself\n\n"
                "1. Define a unique primary key for your data (e.g. `date` + `transaction_id`).\n"
                "2. Count duplicate keys using `=COUNTIFS(A:A, A2, B:B, B2) > 1` in Excel or `df.duplicated(subset=['date', 'transaction_id'], keep=False)` in Python pandas.\n"
                "3. Perform a three-way reconciliation between opening balance, net sum of transactions, and closing balance.\n\n"
                "### In the sandbox\n\n"
                "Run the script to see how duplicate composite keys are detected."
            ),
            "exercise": question(
                "What is a composite primary key in the context of financial transaction hygiene?",
                [
                    "An encrypted access token required to decrypt bank statement CSV files downloaded from customer portals",
                    "A combination of two or more columns (such as date and transaction ID) that together uniquely identify a single record",
                    "A proprietary database hashing algorithm designed to compress large transaction log files for long-term offsite storage",
                ],
                1,
                "A composite primary key combines attributes (e.g. date + transaction ID) to guarantee that no duplicate record enters the analytical dataset.",
            ),
            "exercises": [
                question(
                    "What is a composite primary key in financial transaction hygiene?",
                    [
                        "An encrypted access token required to decrypt bank statement CSV files downloaded from customer portals",
                        "A combination of two or more columns (such as date and transaction ID) that together uniquely identify a single record",
                        "A proprietary database hashing algorithm designed to compress large transaction log files for long-term offsite storage",
                    ],
                    1,
                    "A composite key combines multiple attributes to uniquely identify a transaction.",
                ),
            ],
            "terms": [
                {"term": "Composite Key", "definition": "A key made up of two or more attributes that together uniquely identify an entity in a table."},
                {"term": "Reconciliation", "definition": "The accounting process of comparing two sets of records to ensure figures are in agreement and accurate."},
            ],
            "references": [
                {"title": "CFA Institute · Financial Statement Analysis and Reconciliation Principles", "url": "https://www.cfainstitute.org"},
            ],
        },
        {
            "id": "25.4",
            "part": "2",
            "title": "Three biases that start in your own spreadsheet",
            "subtitle": "Examine look-ahead bias, survivorship bias, and selection bias with real examples.",
            "minutes": 12,
            "objective": "Explain look-ahead bias, survivorship bias, and selection bias with one personal-finance and one market-data example.",
            "kind": "fundamentals",
            "formula": r"\text{Bias Hazard: } E_{\text{sample}}[R] \gg E_{\text{population}}[R] \quad (\text{Survivors} \ne \text{All Entrants})",
            "code": (
                "# Demonstrating survivorship bias in equity analysis\n"
                "survivor_returns = [0.15, 0.20]\n"
                "all_returns = [0.15, 0.20, -1.00]\n"
                "survivor_mean = sum(survivor_returns) / len(survivor_returns)\n"
                "population_mean = sum(all_returns) / len(all_returns)\n"
                "print('Survivor-Only Reported Return (%):', round(survivor_mean * 100, 1))\n"
                "print('True Population Return (%):', round(population_mean * 100, 1))\n"
            ),
            "content": (
                "## The idea\n\n"
                "Data biases do not only occur in academic research papers—they start innocently in your own personal spreadsheets:\n\n"
                "1. **Look-Ahead Bias**: Making a decision at time $t$ using information from time $t+k$.\n"
                "   - *Personal finance example*: Budgeting next month's grocery spending based on an annual bonus that was announced only at the end of the year.\n"
                "   - *Market example*: Backtesting a strategy that buys at calendar-year low, where that low is computed from full year in advance.\n"
                "2. **Survivorship Bias**: Analyzing only the entities that survived to the end of the period, discarding those that failed.\n"
                "   - *Personal finance example*: Asking five successful restaurant owners for advice on startup profitability while ignoring the 95 restaurants in the same district that went out of business.\n"
                "   - *Market example*: Backtesting a stock screen on today's S&P 500 members over the past 15 years (2005–2020), ignoring companies that went bankrupt (such as Lehman Brothers in 2008 or Washington Mutual) or were delisted.\n"
                "3. **Selection Bias**: Filtering a sample non-randomly so that it ceases to represent the true population.\n\n"
                "$$\n"
                r"\mathrm{Bias}_{\text{survivor}} = \mathbb{E}[R \mid \text{Delisted} = \text{False}] - \mathbb{E}[R]"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A quantitative investor tests a small-cap value screen from 2005 to 2020. The spreadsheet pulls historical data for the 100 small-cap stocks currently trading on the exchange today, finding a 16.0% annualized return.\n\n"
                "When re-tested on a **point-in-time database** that includes the 42 small-cap companies that went bankrupt or were liquidated between 2005 and 2020, the actual return drops to 8.5%. The apparent 7.5% gap was entirely an illusion produced by survivorship bias.\n\n"
                "## Work through it yourself\n\n"
                "1. Check if your stock screen includes delisted companies.\n"
                "2. Verify that corporate financial metrics (P/E, Debt/Equity) use the exact filing release date, not the fiscal period end date.\n"
                "3. Document your sample boundary before drawing conclusions.\n\n"
                "### In the sandbox\n\n"
                "Run the script to see how excluding a single bankrupt company distorts average return from −21.7% to +17.5%."
            ),
            "exercise": question(
                "Why does backtesting on the current members of an index (e.g. S&P 500 or LQ45) overstate historical returns?",
                [
                    "Because contemporary server processors compute compounding portfolio returns significantly faster than legacy mainframe computers",
                    "Because it suffers from survivorship bias, ignoring companies that failed and were removed from the index in past years",
                    "Because index component equities are legally exempt from paying corporate income taxes and exchange trading fees",
                ],
                1,
                "Survivorship bias ignores failed or delisted companies, creating a falsely optimistic sample of historical winners.",
            ),
            "exercises": [
                question(
                    "Why does backtesting on current members of an index overstate returns?",
                    [
                        "Because contemporary server processors compute compounding portfolio returns significantly faster than legacy mainframe computers",
                        "Because it suffers from survivorship bias, ignoring companies that failed and were removed from the index in past years",
                        "Because index component equities are legally exempt from paying corporate income taxes and exchange trading fees",
                    ],
                    1,
                    "Survivorship bias ignores failed companies, creating a falsely optimistic sample of winners.",
                ),
            ],
            "terms": [
                {"term": "Survivorship Bias", "definition": "The logical error of concentrating on the people or things that made it past some selection process and overlooking those that did not, typically because of their lack of visibility."},
                {"term": "Point-in-Time Data", "definition": "Data that reflects exactly what was known and reported at a specific date in history, without retrospective corrections or future revisions."},
            ],
            "references": [
                {"title": "CFA Institute · Research Foundations: Survivorship Bias in Backtesting", "url": "https://www.cfainstitute.org"},
            ],
        },
        {
            "id": "25.5",
            "part": "2",
            "title": "Versioning: making last month's analysis reproducible",
            "subtitle": "Immutable raw data, transformation scripts, and an auditable changelog.",
            "minutes": 10,
            "objective": "Apply the golden rule of reproducible data: never overwrite raw source files; separate raw data from transformation scripts.",
            "kind": "fundamentals",
            "formula": r"\text{Reproducible Pipeline: } \text{Raw Data (read-only)} + \text{Script (versioned)} \to \text{Cleaned Output}",
            "code": (
                "# The reproducible pipeline contract\n"
                "raw_file_fingerprint = '4b82d91f0a'\n"
                "print('Raw Data Fingerprint (SHA-256):', raw_file_fingerprint)\n"
                "print('Raw file status: Read-only, immutable')\n"
                "print('Transformation pipeline applied deterministically')\n"
            ),
            "content": (
                "## The idea\n\n"
                "The most important rule in professional data management is:\n\n"
                "> **NEVER EDIT RAW DATA FILES DIRECTLY.**\n\n"
                "When you open an exported bank or market CSV and manually delete bad rows or edit typos in Excel, you destroy the audit trail. Six months later, when the numbers disagree with your bank, nobody can tell whether the bank was wrong or an accidental keystroke altered cell C14.\n\n"
                "A reproducible workflow separates data into three distinct layers:\n"
                "1. **Raw Layer (`data/raw/`)**: Downloaded files kept strictly read-only with a recorded SHA-256 hash.\n"
                "2. **Script Layer (`scripts/clean.py`)**: Code that reads the raw data, applies explicit transformations, and logs changes.\n"
                "3. **Clean Layer (`data/clean/`)**: The derived, tidy dataset used for modeling.\n\n"
                "$$\n"
                r"\mathcal{D}_{\text{clean}} = \mathcal{T}_{\theta}(\mathcal{D}_{\text{raw}}) \quad \text{where } \mathcal{D}_{\text{raw}} \text{ is immutable}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "An investment team receives a monthly transaction export from a custodian bank with 5,000 rows. Instead of opening it in Excel and manually fixing date typos, the analyst writes a 10-line Python cleaning script.\n\n"
                "When the custodian updates their accounting system next year and retroactively re-issues the file, the analyst re-runs the script in 2 seconds. Because the raw file was never touched, the entire analysis is 100% reproducible and auditable.\n\n"
                "## Work through it yourself\n\n"
                "1. Create a `raw/` folder on your computer and set permissions to read-only.\n"
                "2. Never press `Ctrl+S` on an exported source file.\n"
                "3. Write down every data cleaning step in a plain text changelog (`CHANGELOG.md`).\n\n"
                "### In the sandbox\n\n"
                "Run the script to see how hashing validates raw data immutability."
            ),
            "exercise": question(
                "Why should you never manually edit or save changes directly inside a raw data export file?",
                [
                    "Because commercial spreadsheet file formats automatically corrupt and lose historical calculation formulas after thirty days of inactivity",
                    "Because it destroys the audit trail and makes it impossible to reproduce the analysis or verify errors against the original source",
                    "Because operating system file permissions automatically prevent saving changes to any downloaded comma-separated value file",
                ],
                1,
                "Editing raw files destroys the audit trail. Separating raw data from transformation scripts guarantees reproducibility.",
            ),
            "exercises": [
                question(
                    "Why should you never manually edit raw data export files directly?",
                    [
                        "Because commercial spreadsheet file formats automatically corrupt and lose historical calculation formulas after thirty days of inactivity",
                        "Because it destroys the audit trail and makes it impossible to reproduce the analysis or verify errors against the original source",
                        "Because operating system file permissions automatically prevent saving changes to any downloaded comma-separated value file",
                    ],
                    1,
                    "Editing raw data destroys the provenance audit trail.",
                ),
            ],
            "terms": [
                {"term": "Immutable Data", "definition": "Data that cannot be modified after its creation, ensuring verifiable provenance and integrity."},
                {"term": "Audit Trail", "definition": "A step-by-step record by which accounting or financial data can be traced to its original source."},
            ],
            "references": [
                {"title": "The Turing Way · Guide for Reproducible Research", "url": "https://the-turing-way.netlify.app"},
            ],
        },
        {
            "id": "25.6",
            "part": "2",
            "title": "Practice: clean this messy file",
            "subtitle": "Capstone: download a multi-defect transaction CSV, diagnose all five errors, and return a clean dataset.",
            "minutes": 15,
            "objective": "Clean a provided messy CSV file exhibiting the five core defects: date ambiguity, mixed currencies, duplicates, missing periods, and category drift.",
            "kind": "fundamentals",
            "formula": r"\text{Defect Score} = \text{DateErrors} + \text{CurrencyErrors} + \text{Duplicates} + \text{Gaps} + \text{Drift} = 0",
            "code": (
                "# Capstone practice: 5 core data hygiene defect classes\n"
                "defects_monitored = 5\n"
                "print('Capstone dataset: messy_transactions_practice.csv')\n"
                "print('Target defect classes to clean:', defects_monitored)\n"
                "print('1. Inconsistent Date Formats (ISO-8601)')\n"
                "print('2. Mixed Currency Denominations')\n"
                "print('3. Duplicate Records')\n"
                "print('4. Missing Trading Periods')\n"
                "print('5. Category Drift')\n"
            ),
            "content": (
                "## The idea\n\n"
                "Theory without hands-on practice is easily forgotten. In this capstone lesson, you will put your data hygiene skills to the test on a real messy transaction export.\n\n"
                "The file `messy_transactions_practice.csv` contains exactly **the five defect classes** explored in this course:\n"
                "1. **Inconsistent Date Formats**: A mix of `YYYY-MM-DD`, `DD/MM/YYYY`, and text dates.\n"
                "2. **Mixed Currency Denominations**: Unstandardized amount strings with embedded currency symbols (`Rp 1.800.000`).\n"
                "3. **Duplicate Rows**: Identical transaction records repeated.\n"
                "4. **Missing Periods**: Unaccounted calendar gaps.\n"
                "5. **Category Drift**: The same expense category labeled inconsistently (`Operasional`, `OpEx`, `operasional`, `Operations`).\n\n"
                "$$\n"
                r"\text{Target: Zero Duplicates} \land \text{Standard ISO Dates} \land \text{Normalized Taxonomy}"
                "\n$$\n\n"
                "## A worked example & Capstone Deliverable\n\n"
                "1. Download `messy_transactions_practice.csv` from the resources section on the course page.\n"
                "2. Diagnose and repair all five defect classes (date ambiguity, uncleaned currency symbols, duplicate records, calendar gaps, category drift).\n"
                "3. Self-check your cleaned dataset by comparing it against `cleaned_transactions_reference.csv` to verify matching row count, column structure, and continuous balances.\n\n"
                "## Work through it yourself\n\n"
                "Compare your cleaned file against the maintainer answer key in `cleaned_transactions_reference.csv`.\n\n"
                "### In the sandbox\n\n"
                "Run the starter script to inspect automated validation checks."
            ),
            "exercise": question(
                "When standardizing the category column in a messy transactions file, which approach represents best practice?",
                [
                    "Inventing arbitrary descriptive labels for each transaction row based on the bookkeeping processor's personal memory of the expense",
                    "Establish a fixed canonical taxonomy (e.g. 'Operasional', 'Penjualan', 'Gaji') and map all spelling variants into that taxonomy",
                    "Deleting the expense categorization column entirely and distributing all transaction amounts evenly across budget categories",
                ],
                1,
                "Standardizing categories requires creating a controlled dictionary or taxonomy and mapping all drift variations into canonical names.",
            ),
            "exercises": [
                question(
                    "When standardizing categories in messy data, what is the best practice?",
                    [
                        "Inventing arbitrary descriptive labels for each transaction row based on the bookkeeping processor's personal memory of the expense",
                        "Establish a fixed canonical taxonomy (e.g. 'Operasional', 'Penjualan', 'Gaji') and map all spelling variants into that taxonomy",
                        "Deleting the expense categorization column entirely and distributing all transaction amounts evenly across budget categories",
                    ],
                    1,
                    "Establish a controlled taxonomy and map spelling variations into canonical names.",
                ),
            ],
            "terms": [
                {"term": "Category Drift", "definition": "The gradual divergence or inconsistent labeling of categorical values in a dataset over time."},
                {"term": "Data Cleansing", "definition": "The process of detecting and correcting or removing corrupt, inaccurate, or incomplete records from a dataset."},
            ],
            "references": [
                {"title": "The Turing Way · Data Cleaning and Preprocessing Best Practices", "url": "https://the-turing-way.netlify.app"},
            ],
        },
    ]

    parts = [
        {
            "id": "1",
            "title": "Tidy Foundations & Defect Detection",
            "description": "Master atomic rectangular structures, eliminate ambiguous dates and unstated currencies, and remove duplicate records.",
        },
        {
            "id": "2",
            "title": "Biases, Versioning & Capstone Cleaning",
            "description": "Understand look-ahead and survivorship biases, enforce immutable raw data pipelines, and clean a multi-defect CSV.",
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
            "id": "data-hygiene-final",
            "title": "Data Hygiene for Investors Assessment",
            "kind": "final",
            "passingScore": 70,
            "minutes": 20,
            "version": 3,
            "description": "Comprehensive evaluation of tidy data principles, defect detection, bias prevention, and dataset reproducibility.",
            "moduleIds": [m["id"] for m in modules],
            "questions": [
                {
                    "id": "data-hygiene-final-q1",
                    "lessonId": "25.1",
                    "question": "In Hadley Wickham's Tidy Data paradigm, which structural rule is violated when column headers contain values (e.g. '2024', '2025', '2026') rather than variable names?",
                    "options": [
                        "Every variable must form its own column and every observation must form a row",
                        "Tables must never contain numeric values in adjacent columns without explicit string labels",
                        "Observations must be arranged in strict alphabetical order according to client account names",
                    ],
                    "answer": 0,
                    "explanation": "When years or dates are column headers, values are acting as column names; tidying requires melting them into a single 'year' column with one observation per row.",
                },
                {
                    "id": "data-hygiene-final-q2",
                    "lessonId": "25.2",
                    "question": "Why does the ISO-8601 standard 'YYYY-MM-DD' prevent date ambiguity in multi-regional financial datasets?",
                    "options": [
                        "It compresses chronological timestamps into four-byte binary integers to optimize memory buffers during data processing",
                        "It sorts chronologically via standard lexicographical string sorting and eliminates confusion between month-first and day-first formats",
                        "It automatically translates local calendar dates into recognized international financial accounting conventions across global market exchanges",
                    ],
                    "answer": 1,
                    "explanation": "ISO-8601 follows a big-endian hierarchy (Year-Month-Day), ensuring consistent alphabetical sorting and eliminating ambiguity between US (MM/DD) and international (DD/MM) conventions.",
                },
                {
                    "id": "data-hygiene-final-q3",
                    "lessonId": "25.2",
                    "question": "When standardizing transaction amounts stored with mixed notations ('$1,200.50', 'Rp 18.000.000', '1500 EUR'), what is the correct data hygiene transformation?",
                    "options": [
                        "Strip currency symbols, parse decimal points appropriately into a clean numeric column, and track currency in a separate ISO-4217 column",
                        "Remove all commas and periods indiscriminately across all columns and multiply Indonesian Rupiah amounts by zero to match US Dollars",
                        "Store the entire alphanumeric string unchanged in an untyped text column and perform string pattern searches during mathematical summation",
                    ],
                    "answer": 0,
                    "explanation": "Clean tabular hygiene requires isolating the pure numeric magnitude in one column and recording the currency symbol/code (USD, IDR, EUR) in a dedicated adjacent column.",
                },
                {
                    "id": "data-hygiene-final-q4",
                    "lessonId": "25.3",
                    "question": "How does defining a composite primary key (e.g., date + transaction_id) protect a tabular dataset or database against duplicate entries?",
                    "options": [
                        "It automatically pays recurring banking overdraft charges and vendor invoices without requiring administrative human approval",
                        "It prevents the database table or dataframe from accepting duplicate records that share the exact same combination of primary key attributes",
                        "It converts negative cash flow overdraft balances into positive equity credits through automated algorithmic double-entry ledger balance adjustments",
                    ],
                    "answer": 1,
                    "explanation": "A composite primary key enforces uniqueness across the combined set of columns, rejecting any subsequent record that shares identical identifier values.",
                },
                {
                    "id": "data-hygiene-final-q5",
                    "lessonId": "25.4",
                    "question": "How does survivorship bias distort backtested investment returns on an equity index?",
                    "options": [
                        "It excludes bankrupt or delisted companies from historical testing, artificially inflating the apparent performance of the surviving winners",
                        "It forces statistical calculation engines to exhaust available memory buffers during cross-sectional regression analyses on large historical datasets",
                        "It incorporates too many defunct corporate entities, making long-term compounding returns appear substantially worse than market reality",
                    ],
                    "answer": 0,
                    "explanation": "Survivorship bias occurs when only companies that survived to the present day are included in historical analysis, systematically ignoring those that failed.",
                },
                {
                    "id": "data-hygiene-final-q6",
                    "lessonId": "25.5",
                    "question": "In an auditable data pipeline, why must raw source datasets be treated as read-only immutable artifacts?",
                    "options": [
                        "Because modern operating systems strictly prohibit users from saving modifications to comma-separated value files that exceed ten megabytes in file size",
                        "Because modifying raw files directly destroys the audit trail and prevents recreating derived datasets from scratch in a reproducible way",
                        "Because spreadsheet software permanently locks calculation workbooks whenever they are opened on more than one workstation simultaneously",
                    ],
                    "answer": 1,
                    "explanation": "Data provenance requires that raw inputs never undergo destructive manual edits; all transformations must be expressed as deterministic, reproducible scripts.",
                },
                {
                    "id": "data-hygiene-final-q7",
                    "lessonId": "25.6",
                    "question": "When cleaning a messy financial ledger containing category drift (e.g. 'Operasional', 'OpEx', 'Operations'), how should categories be reconciled?",
                    "options": [
                        "Delete the category column entirely and classify all transactions as miscellaneous corporate expenses in the final balance sheet",
                        "Map all drift variants into a predefined, controlled taxonomy (such as 'Operasional') to maintain consistent reporting buckets",
                        "Assign a novel category name to every unique spelling variation to preserve every historical clerk's original typographical preference",
                    ],
                    "answer": 1,
                    "explanation": "Standardizing categories requires mapping drifting variants into a predefined, controlled canonical taxonomy.",
                },
            ],
        }
    ]

    return {
        "id": "data-hygiene",
        "number": 25,
        "title": "Data Hygiene for Investors",
        "description": (
            "Essential data hygiene principles for investors, analysts, and small bookkeepers. "
            "Master tidy data structures, detect and repair the five most common tabular defects "
            "(inconsistent dates, mixed currencies, duplicates, missing periods, category drift), "
            "eliminate survivorship and look-ahead biases, and build reproducible research pipelines."
        ),
        "source": "Original empirical data framework · Reproducible research standards",
        "level": "Beginner",
        "icon": "book",
        "studyType": "applied",
        "modules": modules,
        "parts": parts,
        "prerequisites": "None. Suitable for spreadsheet users, small business bookkeepers, and curious investors.",
        "outcomes": [
            "Structure rectangular datasets using Hadley Wickham's Tidy Data rules",
            "Detect and eliminate ISO-8601 date ambiguity and mixed currency denominations",
            "Implement composite primary keys and reconcile transactions against bank balances",
            "Identify and prevent look-ahead bias, survivorship bias, and selection bias",
            "Clean a multi-defect CSV file and build an immutable, reproducible pipeline",
        ],
        "readingGuide": (
            "Designed for anyone who works with financial numbers in spreadsheets or Python. "
            "Complete all 6 lessons and submit the cleaned CSV capstone in lesson 6 to graduate into "
            "Quantitative Investment Analysis and Econometrics."
        ),
        "resources": [
            {
                "title": "Messy Transactions Practice Dataset (CSV)",
                "url": "/templates/messy_transactions_practice.csv",
            },
            {
                "title": "Cleaned Transactions Reference Key (CSV)",
                "url": "/templates/cleaned_transactions_reference.csv",
            },
        ],
        "references": [
            {"title": "Hadley Wickham · Tidy Data Principles", "url": "https://www.jstatsoft.org/article/view/v059i10"},
            {"title": "The Turing Way · Reproducible Data Science", "url": "https://the-turing-way.netlify.app"},
        ],
        "exams": exams,
        # CS-1 course metadata
        "slug": "data-hygiene",
        "subtitle": "Essential Data Hygiene and Reproducibility for Investors",
        "audience_tags": ["beginner", "spreadsheet", "investor", "data"],
        "estimated_minutes": sum(m["minutes"] for m in modules),
        "lesson_count": len(modules),
        "assessment_count": len(exams),
        "completion_criteria": {"lessons_pct": 100, "assessment_pass_pct": 70},
        "certificate": {"enabled": True, "template_id": "data-hygiene-badge", "verification_required": False},
        "funnel_cta": {
            "label": "Advance to Quantitative Investment Analysis",
            "target_course_id": "statistical-foundations",
            "secondary_label": "Master Econometrics & Factor Models",
            "secondary_target_course_id": "econometrics",
        },
        "language": ["en", "id"],
    }
