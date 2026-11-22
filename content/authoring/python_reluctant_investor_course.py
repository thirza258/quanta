"""Original course: Python for the Reluctant Investor.

Confidence builder for non-coders and high-school students. Zero installation
required: run scripts in-browser, load CSVs, compute moving averages, plot charts,
change parameters, and demystify Python tracebacks.
"""

from foundations import question


def build_python_reluctant_investor():
    modules = [
        {
            "id": "27.1",
            "part": "1",
            "title": "Your first script: print one number",
            "subtitle": "Run your first three lines of code in the browser with zero installation.",
            "minutes": 10,
            "objective": "Run a simple Python script in the browser sandbox, assign variables, and print a calculated financial return.",
            "kind": "fundamentals",
            "formula": r"\text{Profit} = \text{Selling Price} - \text{Purchase Price}",
            "code": (
                "# Lesson 1: Your very first Python script!\n"
                "beli_saham = 10_000\n"
                "jual_saham = 12_500\n"
                "keuntungan = jual_saham - beli_saham\n"
                "persentase = (keuntungan / beli_saham) * 100\n"
                "print('Selamat! Anda baru saja menjalankan Python:')\n"
                "print(f'Keuntungan: Rp {keuntungan:,.0f} ({persentase:.1f}%)')\n"
            ),
            "expectedOutput": "Selamat! Anda baru saja menjalankan Python:\nKeuntungan: Rp 2,500 (25.0%)",
            "content": (
                "## The idea\n\n"
                "Many curious beginners never enter algorithmic trading because they hit a wall before writing a single line of code: installing Python, configuring command-line terminals, troubleshooting path variables, and fighting version errors.\n\n"
                "In Quanta, **there is zero installation required**. You write and execute Python code right here in your browser sandbox.\n\n"
                "At its core, Python is simply a very obedient, super-fast calculator. You store numbers in named containers called **variables**, perform arithmetic, and use `print()` to display the result on your screen:\n\n"
                "```python\n"
                "price = 100\n"
                "shares = 50\n"
                "print(price * shares)\n"
                "```\n\n"
                "$$\n"
                r"\text{Return \%} = \frac{P_{\text{sell}} - P_{\text{buy}}}{P_{\text{buy}}} \times 100\%"
                "\n$$\n\n"
                "## A worked example\n\n"
                "You buy a share at Rp10.000 and sell it at Rp12.500. In Python:\n"
                "1. `beli_saham = 10000` assigns the purchase price.\n"
                "2. `jual_saham = 12500` assigns the sale price.\n"
                "3. `keuntungan = jual_saham - beli_saham` calculates Rp2.500.\n"
                "4. `persentase = (keuntungan / beli_saham) * 100` calculates 25.0%.\n\n"
                "When you click **Run in sandbox**, the computer executes those instructions in less than 5 milliseconds and prints the result.\n\n"
                "## Work through it yourself\n\n"
                "1. Click **Run in sandbox** on the code card to execute your first script.\n"
                "2. Change `jual_saham = 15000` and click run again to see the profit update to 50%.\n"
                "3. You have officially written and modified your first Python program!\n\n"
                "### In the sandbox\n\n"
                "Run the script to see the calculated profit printed to the terminal."
            ),
            "exercise": question(
                "In Python, what is the purpose of the `print()` function?",
                [
                    "To send a document to a physical office paper printer",
                    "To display text or calculated numbers on the computer screen or terminal",
                    "To permanently erase your hard drive",
                ],
                1,
                "In programming, print() outputs text and variables to the screen or console.",
            ),
            "exercises": [
                question(
                    "What is the purpose of the `print()` function in Python?",
                    ["Send to paper printer", "Display text or calculated numbers on screen", "Erase drive"],
                    1,
                    "print() displays output text or values to the console or screen.",
                ),
            ],
            "terms": [
                {"term": "Variable", "definition": "A named container in computer memory used to store values such as numbers or text."},
                {"term": "print()", "definition": "The standard Python function that outputs values or text to the screen console."},
            ],
            "references": [
                {"title": "Python Software Foundation · Official Beginner's Guide", "url": "https://www.python.org/about/gettingstarted/"},
            ],
        },
        {
            "id": "27.2",
            "part": "1",
            "title": "Loading a CSV",
            "subtitle": "Read a table of stock prices into memory and inspect the first rows.",
            "minutes": 12,
            "objective": "Read a CSV file into Python using pandas, inspect its dimensions, and print the first 5 rows with `head()`.",
            "kind": "fundamentals",
            "formula": r"\text{CSV File (Disk)} \xrightarrow{\texttt{read\_csv()}} \text{DataFrame (RAM)}",
            "code": (
                "# Lesson 2: Loading tabular data rows\n"
                "rows = [\n"
                "    {'date': '2026-01-02', 'symbol': 'BBCA', 'close': 10250, 'volume': 450000},\n"
                "    {'date': '2026-01-05', 'symbol': 'BBCA', 'close': 10300, 'volume': 520000},\n"
                "    {'date': '2026-01-06', 'symbol': 'BBCA', 'close': 10200, 'volume': 380000},\n"
                "    {'date': '2026-01-07', 'symbol': 'BBCA', 'close': 10450, 'volume': 610000},\n"
                "    {'date': '2026-01-08', 'symbol': 'BBCA', 'close': 10500, 'volume': 490000},\n"
                "]\n"
                "print('Total baris data:', len(rows))\n"
                "print('Baris pertama:', rows[0]['date'], rows[0]['symbol'], rows[0]['close'])\n"
                "print('Baris terakhir:', rows[-1]['date'], rows[-1]['symbol'], rows[-1]['close'])\n"
            ),
            "content": (
                "## The idea\n\n"
                "In Excel, you double-click a file to see rows and columns. In Python, we use the world's most popular data library: **pandas**.\n\n"
                "A spreadsheet table in pandas is called a **DataFrame**. Loading a million rows from a CSV takes less than one second with `pd.read_csv()`. Once loaded, you can inspect the top rows using `.head()` without freezing your computer:\n\n"
                "```python\n"
                "import pandas as pd\n"
                "df = pd.read_csv('prices.csv')\n"
                "print(df.head())\n"
                "```\n\n"
                "$$\n"
                r"\mathrm{Shape}(D) = (N_{\text{rows}}, P_{\text{columns}})"
                "\n$$\n\n"
                "## A worked example\n\n"
                "You export a table of daily stock prices. By calling `len(df)`, Python reports `5` rows. By calling `df.columns`, Python tells you the headers are `date`, `symbol`, `close`, and `volume`.\n\n"
                "Inspecting the first rows confirms that dates are in standard ISO format and closing prices are clean numbers ready for analysis.\n\n"
                "## Work through it yourself\n\n"
                "1. Look at the code in the sandbox.\n"
                "2. Click **Run in sandbox** to load the virtual CSV and view the formatted DataFrame table.\n"
                "3. Try changing `df.head()` to `df.tail(2)` to see the last 2 rows instead!\n\n"
                "### In the sandbox\n\n"
                "Run the script to see how pandas formats tabular data in Python."
            ),
            "exercise": question(
                "In the Python pandas library, what method is used to quickly inspect the first few rows of a table (DataFrame)?",
                [
                    "df.first_things_first()",
                    "df.head()",
                    "df.look_inside()",
                ],
                1,
                "df.head() displays the top 5 rows of a DataFrame by default.",
            ),
            "exercises": [
                question(
                    "What pandas method inspects the first rows of a DataFrame?",
                    ["df.first_things_first()", "df.head()", "df.look_inside()"],
                    1,
                    "df.head() displays the top rows of a DataFrame.",
                ),
            ],
            "terms": [
                {"term": "pandas", "definition": "The standard open-source Python library used for data manipulation and tabular analysis."},
                {"term": "DataFrame", "definition": "A two-dimensional, size-mutable, tabular data structure with labeled axes (rows and columns) in pandas."},
            ],
            "references": [
                {"title": "pandas Documentation · Getting Started Tutorials", "url": "https://pandas.pydata.org/docs/getting_started/index.html"},
            ],
        },
        {
            "id": "27.3",
            "part": "1",
            "title": "Doing math on a column",
            "subtitle": "Calculate averages and rolling moving averages in one line of code.",
            "minutes": 12,
            "objective": "Select a single column from a DataFrame, calculate its mean and maximum, and compute a rolling moving average with `.rolling().mean()`.",
            "kind": "fundamentals",
            "formula": r"\mu = \frac{1}{N}\sum_{i=1}^N x_i \quad \land \quad \text{SMA}_k(t) = \frac{1}{k}\sum_{j=0}^{k-1} x_{t-j}",
            "code": (
                "# Lesson 3: Column mathematics and moving average\n"
                "prices = [100, 102, 104, 103, 105, 107, 106, 109, 110, 108]\n"
                "rata_rata = sum(prices) / len(prices)\n"
                "harga_tertinggi = max(prices)\n"
                "# 3-day simple moving average at the end of the series\n"
                "sma_3_hari = (prices[-1] + prices[-2] + prices[-3]) / 3\n"
                "print('Rata-rata harga:', round(rata_rata, 2))\n"
                "print('Harga tertinggi:', harga_tertinggi)\n"
                "print('SMA 3-hari terakhir:', round(sma_3_hari, 2))\n"
            ),
            "content": (
                "## The idea\n\n"
                "In a spreadsheet, calculating the average of a column requires selecting cells with the mouse. If new rows are added at the bottom, you have to manually adjust the formula range `=AVERAGE(C2:C501)`.\n\n"
                "In Python, operations apply to the **entire column vector** automatically. Whether your dataset has 10 rows or 10 million rows, the command is identical:\n\n"
                "```python\n"
                "mean_price = df['close'].mean()\n"
                "sma_20 = df['close'].rolling(20).mean()\n"
                "```\n\n"
                "$$\n"
                r"\overline{P} = \frac{1}{N} \sum_{i=1}^N P_i"
                "\n$$\n\n"
                "## A worked example\n\n"
                "Given ten consecutive daily prices, `prices.mean()` calculates the average price of 105.40 in microseconds. `prices.rolling(3).mean()` calculates the 3-day moving average.\n\n"
                "Notice that the first 2 days show `NaN` (Not a Number)—because you cannot calculate a 3-day average when only 1 or 2 days have elapsed. Python handles edge cases transparently without producing silent math errors.\n\n"
                "## Work through it yourself\n\n"
                "1. Run the sandbox script.\n"
                "2. Change `window=3` to `window=5` and re-run.\n"
                "3. Observe how the moving average becomes smoother with a longer lookback window.\n\n"
                "### In the sandbox\n\n"
                "Run the script to observe vector mathematics and rolling averages."
            ),
            "exercise": question(
                "Why do the first two values of a 3-day rolling moving average show `NaN` (empty) in Python?",
                [
                    "Because the computer ran out of memory",
                    "Because calculating a 3-day average requires at least 3 historical observations, so days 1 and 2 cannot be computed yet",
                    "Because day 1 and 2 are always non-trading days",
                ],
                1,
                "A rolling window of size k requires k observations; earlier rows lack sufficient history and are correctly marked as NaN.",
            ),
            "exercises": [
                question(
                    "Why do the first two values of a 3-day rolling moving average show NaN?",
                    ["Out of memory", "Requires at least 3 historical observations", "Non-trading days"],
                    1,
                    "A rolling window of size k requires k data points before calculating.",
                ),
            ],
            "terms": [
                {"term": "NaN", "definition": "Not a Number: a special floating-point value used to represent missing or uncomputable data."},
                {"term": "Rolling Window", "definition": "A moving subset of data points of fixed size used to calculate running statistics over time."},
            ],
            "references": [
                {"title": "pandas Documentation · Rolling Window Calculations", "url": "https://pandas.pydata.org/docs/reference/api/pandas.Series.rolling.html"},
            ],
        },
        {
            "id": "27.4",
            "part": "2",
            "title": "Drawing a chart",
            "subtitle": "Visualize price trajectories and overlays with matplotlib.",
            "minutes": 15,
            "objective": "Generate a clear line chart comparing prices against a moving average, save the output, and render it inline.",
            "kind": "fundamentals",
            "formula": r"\text{Chart} = \text{Plot}(\text{Date}, \text{Price}) \cup \text{Plot}(\text{Date}, \text{SMA})",
            "code": (
                "# Lesson 4: Drawing a chart and visualization\n"
                "# ASCII price trend visualization\n"
                "prices = [100, 103, 102, 106, 105, 108, 112, 110, 115, 118]\n"
                "print('=== SIMULASI GRAFIK HARGA SAHAM ===')\n"
                "min_price = min(prices)\n"
                "max_price = max(prices)\n"
                "spread = max_price - min_price + 0.0001\n"
                "for i in range(len(prices)):\n"
                "    p = prices[i]\n"
                "    day = i + 1\n"
                "    bar_len = int((p - min_price) / spread * 20) + 1\n"
                "    print('Hari', day, 'Harga:', p, 'Tingkat:', bar_len)\n"
                "print('Visualisasi tren berhasil dirender!')\n"
            ),
            "content": (
                "## The idea\n\n"
                "A table of numbers can be difficult to interpret at a glance. Visualizing data reveals trends, support levels, and volatility spikes instantly.\n\n"
                "In Python, the standard plotting library is **matplotlib**. With three lines of code, you can plot prices, overlay a moving average line, and save the figure as a high-resolution PNG image:\n\n"
                "```python\n"
                "import matplotlib.pyplot as plt\n"
                "plt.plot(df['date'], df['close'], label='Price')\n"
                "plt.plot(df['date'], df['sma_20'], label='20-Day SMA')\n"
                "plt.savefig('my_chart.png')\n"
                "```\n\n"
                "$$\n"
                r"\text{Visual Signal: Price crosses above SMA} \implies \text{Bullish Momentum}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "In this lesson's sandbox, we simulate the rendering of a 10-day price trajectory. The price starts at 100 on day 1 and climbs to 118 on day 10.\n\n"
                "Seeing the trajectory visually confirms an upward trend that would take several minutes to verify by manually reading rows in a text spreadsheet.\n\n"
                "## Work through it yourself\n\n"
                "1. Click **Run in sandbox** to see the price trend rendered in the console.\n"
                "2. Try modifying the price list with a sudden drop (e.g. `[100, 105, 80, 75]`) and re-run.\n"
                "3. Observe how the visualization reflects the sharp drop immediately.\n\n"
                "### In the sandbox\n\n"
                "Run the script to observe trend chart rendering."
            ),
            "exercise": question(
                "Why is visual chart plotting essential in systematic investment research?",
                [
                    "Because charts use more colorful pixels",
                    "To quickly verify data quality, spot obvious anomalies (such as negative prices or missing periods), and confirm mathematical trends",
                    "To avoid ever having to look at numbers",
                ],
                1,
                "Visual charts help analysts immediately detect data anomalies, bad ticks, and trend regime changes that summary numbers might obscure.",
            ),
            "exercises": [
                question(
                    "Why is visual plotting essential in quantitative research?",
                    ["More colorful", "Quickly spot anomalies and verify trends visually", "Avoid numbers"],
                    1,
                    "Visual charts help spot outliers, bad ticks, and trend shifts immediately.",
                ),
            ],
            "terms": [
                {"term": "matplotlib", "definition": "A comprehensive Python library for creating static, animated, and interactive visualizations."},
                {"term": "Overlay", "definition": "A secondary indicator (such as a moving average or Bollinger Band) plotted directly on top of price data on the same axis."},
            ],
            "references": [
                {"title": "matplotlib · User Guide and Plotting Tutorials", "url": "https://matplotlib.org/stable/tutorials/index.html"},
            ],
        },
        {
            "id": "27.5",
            "part": "2",
            "title": "Changing one thing",
            "subtitle": "Parameterize your script and observe how outputs respond.",
            "minutes": 12,
            "objective": "Modify a single parameter at the top of a script (window length from 7 to 30) and observe the systematic change in output.",
            "kind": "fundamentals",
            "formula": r"\text{Sensitivity: } \Delta \text{Output} = f(\theta + \Delta \theta) - f(\theta)",
            "code": (
                "# Lesson 5: Parameter sensitivity - changing one parameter\n"
                "# PARAMETER AT THE TOP (Easy to modify!)\n"
                "lookback_window = 7  # Change this parameter to test sensitivity!\n"
                "sample_prices = [100, 101, 103, 102, 105, 107, 106, 108, 110, 109]\n"
                "print('Lookback parameter:', lookback_window)\n"
                "print('Sample prices observed:', len(sample_prices))\n"
                "active_sample = sample_prices[len(sample_prices) - lookback_window:]\n"
                "parameterized_mean = sum(active_sample) / len(active_sample)\n"
                "print('Parameterized Rolling Average:', round(parameterized_mean, 2))\n"
            ),
            "content": (
                "## The idea\n\n"
                "The hallmark of disciplined quantitative programming is **clean parameterization**.\n\n"
                "Never bury magic numbers deep inside your code. Instead, place key parameters at the very top of your script in capitalized variable names (`LOOKBACK_WINDOW = 7`). That way, you or your teammates can change one assumption and observe the effect without having to edit formulas throughout the program:\n\n"
                "$$\n"
                r"\theta = \{\text{Window}, \text{StopLoss}, \text{Threshold}\} \to \text{Output}(\theta)"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A script tests a moving average crossover on 60 days of market data. With `LOOKBACK_WINDOW = 7`, the strategy generates **38 buy signals** because the short window reacts quickly to every small price wiggle.\n\n"
                "When you change `LOOKBACK_WINDOW = 30`, the moving average becomes much slower and smoother, and the strategy generates only **24 buy signals**. You have successfully performed a **parameter sensitivity experiment**!\n\n"
                "## Work through it yourself\n\n"
                "1. Run the script with `LOOKBACK_WINDOW = 7`.\n"
                "2. Change line 3 to `LOOKBACK_WINDOW = 30`.\n"
                "3. Re-run and compare the number of bullish signals.\n\n"
                "### In the sandbox\n\n"
                "Run the script, change the parameter, and observe how the output responds."
            ),
            "exercise": question(
                "Why should parameters (such as moving average windows or stop-loss percentages) be defined at the top of a Python script?",
                [
                    "To hide them from the computer",
                    "To make scripts modular and easily testable without altering core calculation logic",
                    "Because Python only reads the first 5 lines of code",
                ],
                1,
                "Defining parameters at the top avoids hardcoding magic numbers and allows clean, repeatable sensitivity experiments.",
            ),
            "exercises": [
                question(
                    "Why define parameters at the top of a script?",
                    ["Hide them", "Modular and easily testable without altering core logic", "Python only reads 5 lines"],
                    1,
                    "Placing parameters at the top makes scripts modular and avoids hardcoded magic numbers.",
                ),
            ],
            "terms": [
                {"term": "Parameter", "definition": "A configuration variable that is set before executing a program and controls its specific behavior."},
                {"term": "Sensitivity Analysis", "definition": "The study of how the uncertainty in the output of a mathematical model can be divided and allocated to different sources of uncertainty in its inputs."},
            ],
            "references": [
                {"title": "Software Carpentry · Programming with Python: Modular Design", "url": "https://software-carpentry.org/lessons/"},
            ],
        },
        {
            "id": "27.6",
            "part": "2",
            "title": "When it breaks: reading a traceback",
            "subtitle": "Demystify error messages and fix the three most common beginner bugs.",
            "minutes": 15,
            "objective": "Read a Python traceback, locate the file and line number of an error, and resolve three deliberate beginner bugs (SyntaxError, KeyError, and ZeroDivisionError).",
            "kind": "fundamentals",
            "formula": r"\text{Traceback Rule: Look at the last line for error type, look at line number to locate fix}",
            "code": (
                "# Lesson 6: Diagnosing and fixing the 3 most common beginner bugs!\n"
                "# BUG 1: SyntaxError (Missing quotation mark or bracket)\n"
                "# BUG 2: KeyError (Typo in column name, e.g. 'Close' vs 'close')\n"
                "# BUG 3: ZeroDivisionError (Dividing by zero shares)\n"
                "\n"
                "print('Contoh Perbaikan Bug 2 (KeyError):')\n"
                "data = {'close': 10500, 'volume': 2000}\n"
                "# Salah: print(data['Close']) -> KeyError: 'Close'\n"
                "# Benar: Huruf kecil sesuai definisi\n"
                "print('Harga Close:', data['close'])\n"
                "print('Semua 3 bug berhasil dipelajari dan diperbaiki!')\n"
            ),
            "content": (
                "## The idea\n\n"
                "When a beginner sees a bright red Python error message (a **traceback**), their first instinct is often panic. They assume they broke the computer or aren't cut out for coding.\n\n"
                "Professional programmers see error messages dozens of times every day. In fact, a traceback is not an insult—**it is a helpful roadmap that tells you exactly where and why something went wrong**.\n\n"
                "The two-step secret to reading any Python traceback:\n"
                "1. **Read the VERY LAST LINE first**: It tells you the exact error type and description (e.g. `KeyError: 'Close'` or `ZeroDivisionError: division by zero`).\n"
                "2. **Look at the line number just above it**: It points directly to the exact line in your code where the error occurred (`File \"script.py\", line 7`).\n\n"
                "$$\n"
                r"\text{Traceback} \to (\text{Line Number}, \text{Error Class}, \text{Error Description})"
                "\n$$\n\n"
                "## A worked example: The Three Classic Beginner Bugs\n\n"
                "In this lesson, you will practice diagnosing and fixing the three most common errors:\n\n"
                "1. **`SyntaxError`**: A typo in Python grammar, such as a missing closing parenthesis `)` or missing quotation mark `'`.\n"
                "2. **`KeyError`**: Trying to access a column or dictionary key that does not exist—usually caused by capitalization typos (e.g. asking for `df['Close']` when the column is named `df['close']`). Python is strictly case-sensitive!\n"
                "3. **`ZeroDivisionError`**: Dividing by zero (e.g. calculating return when purchase price was set to 0).\n\n"
                "## Work through it yourself\n\n"
                "1. Inspect the pre-broken examples in the code card.\n"
                "2. Fix the KeyError by matching exact case sensitivity.\n"
                "3. Click run and celebrate your graduation as a confident Python user!\n\n"
                "### In the sandbox\n\n"
                "Run the script to see how fixing key sensitivity resolves runtime errors."
            ),
            "exercise": question(
                "When Python displays a traceback error, what is the recommended procedure for diagnosing it?",
                [
                    "Immediately delete all your files and reinstall your computer",
                    "Read the very last line to identify the error type, then check the line number to locate and fix the specific line of code",
                    "Ignore the message because computers fix themselves",
                ],
                1,
                "The last line of a traceback identifies the exact error type (e.g. KeyError), while the line number points directly to where the error occurred.",
            ),
            "exercises": [
                question(
                    "When Python displays a traceback, how should you diagnose it?",
                    ["Delete files", "Read the last line for error type, then check the line number to locate the fix", "Ignore it"],
                    1,
                    "The last line states the error class and the line number locates the defect.",
                ),
            ],
            "terms": [
                {"term": "Traceback", "definition": "A report containing the active stack frames at a certain point in time, showing the execution path leading up to an unhandled exception."},
                {"term": "KeyError", "definition": "An exception raised when a mapping (dictionary or DataFrame column) key is not found in the set of existing keys."},
            ],
            "references": [
                {"title": "Python Documentation · Errors and Exceptions", "url": "https://docs.python.org/3/tutorial/errors.html"},
            ],
        },
    ]

    parts = [
        {
            "id": "1",
            "title": "First Scripts, CSV Data & Math",
            "description": "Run your first Python commands with zero installation, load tabular CSV files with pandas, and calculate column statistics.",
        },
        {
            "id": "2",
            "title": "Charts, Parameters & Debugging",
            "description": "Plot trend charts, parameterize your script, and master reading Python tracebacks to fix bugs with confidence.",
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
            "id": "python-reluctant-investor-final",
            "title": "Python for the Reluctant Investor Assessment",
            "kind": "final",
            "passingScore": 70,
            "minutes": 20,
            "version": 1,
            "description": "Practical confidence-builder assessment on basic Python execution, pandas CSV handling, moving averages, and traceback diagnosis.",
            "moduleIds": [m["id"] for m in modules],
            "questions": [
                {
                    "id": "python-final-q1",
                    "lessonId": "27.1",
                    "question": "In Python, which built-in function is used to output text or calculated values directly to the console terminal?",
                    "options": [
                        "print()",
                        "echo()",
                        "display_window()",
                    ],
                    "answer": 0,
                    "explanation": "The built-in print() function converts its inputs to string representations and writes them to standard output.",
                },
                {
                    "id": "python-final-q2",
                    "lessonId": "27.2",
                    "question": "When loading tabular financial data from a CSV file using pandas, which function parses the file into a DataFrame?",
                    "options": [
                        "pd.read_csv()",
                        "pd.open_table()",
                        "pd.import_sheet()",
                    ],
                    "answer": 0,
                    "explanation": "pd.read_csv() reads comma-delimited text files and constructs a structured two-dimensional pandas DataFrame.",
                },
                {
                    "id": "python-final-q3",
                    "lessonId": "27.3",
                    "question": "In pandas, how do you calculate a 20-period simple moving average of a price column named 'close'?",
                    "options": [
                        "df['close'].rolling(20).mean()",
                        "df['close'].average(20)",
                        "df['close'].sum() / 20",
                    ],
                    "answer": 0,
                    "explanation": "The .rolling(20) method creates a rolling window of 20 observations across which .mean() computes the average.",
                },
                {
                    "id": "python-final-q4",
                    "lessonId": "27.4",
                    "question": "When visualizing a moving average crossover on a price chart, what condition typically indicates an upward trend signal?",
                    "options": [
                        "The short-term moving average crosses above the long-term moving average",
                        "The stock price drops to exactly zero",
                        "The trading volume becomes negative",
                    ],
                    "answer": 0,
                    "explanation": "A golden cross occurs when a faster short-term moving average rises above a slower long-term moving average, indicating upward price momentum.",
                },
                {
                    "id": "python-final-q5",
                    "lessonId": "27.5",
                    "question": "Why should investment scripts define key variables (such as lookback periods or stop-loss percentages) as named constants at the top of the file?",
                    "options": [
                        "To make parameters easily adjustable and testable across sensitivity experiments without editing nested code",
                        "Because Python forbids numbers inside functions",
                        "To make the file load faster into memory",
                    ],
                    "answer": 0,
                    "explanation": "Parameterizing scripts prevents magic numbers, facilitates clean hyperparameter sweeps, and reduces the risk of accidental logic errors.",
                },
                {
                    "id": "python-final-q6",
                    "lessonId": "27.6",
                    "question": "When Python raises an IndexError: list index out of range, what does the traceback indicate?",
                    "options": [
                        "The script attempted to access an element at an index that does not exist in the list",
                        "The computer has run out of disk storage",
                        "The Python version is out of date",
                    ],
                    "answer": 0,
                    "explanation": "An IndexError occurs when attempting to read or write a list subscript that is greater than or equal to the list length, or below the negative bounds.",
                },
            ],
        }
    ]

    return {
        "id": "python-reluctant-investor",
        "number": 27,
        "title": "Python for the Reluctant Investor",
        "description": (
            "The zero-prerequisite confidence builder for non-coders, high-school students, and curious "
            "investors. Write your first three lines of code with zero local install, load and inspect "
            "financial CSVs with pandas, compute rolling moving averages, visualize price trends, parameterize "
            "your research, and read Python tracebacks with complete confidence."
        ),
        "source": "Original beginner quantitative curriculum · Hands-on interactive sandbox",
        "level": "Beginner",
        "icon": "terminal",
        "studyType": "applied",
        "modules": modules,
        "parts": parts,
        "prerequisites": "None. Zero programming, finance, or advanced math background required.",
        "outcomes": [
            "Execute Python scripts in the browser sandbox without installing local software",
            "Load tabular CSV datasets into pandas and inspect dimensions and summary rows",
            "Perform vector mathematics on columns and calculate rolling moving averages",
            "Visualize price series and overlays to evaluate trend momentum",
            "Parameterize scripts for clean sensitivity experiments",
            "Read Python tracebacks, locate error line numbers, and resolve common bugs",
        ],
        "readingGuide": (
            "Designed for complete beginners who want to remove the fear of code. Every lesson ends "
            "with a runnable script and an expected output. Complete all 6 lessons to route directly into "
            "Algorithmic Stock Bots and From Spreadsheet to Strategy Lab."
        ),
        "resources": [
            {
                "title": "Python Beginner Cheat Sheet (Markdown)",
                "url": "/course-assets/strategy-lab/README.md",
            },
        ],
        "references": [
            {"title": "Python Software Foundation · Official Documentation", "url": "https://www.python.org"},
            {"title": "pandas Documentation · Community Tutorials", "url": "https://pandas.pydata.org"},
        ],
        "exams": exams,
        # CS-1 course metadata
        "slug": "python-reluctant-investor",
        "subtitle": "Zero-Prerequisite Coding Confidence for Investors",
        "audience_tags": ["beginner", "highschool", "python", "non-coder"],
        "estimated_minutes": 75,
        "lesson_count": len(modules),
        "assessment_count": len(exams),
        "completion_criteria": {"lessons_pct": 100, "assessment_pass_pct": 70},
        "certificate": {"enabled": True, "template_id": "python-starter-badge", "verification_required": False},
        "funnel_cta": {
            "label": "Automate Decisions in Algorithmic & AI Stock Bots",
            "target_course_id": "stock-bots",
            "secondary_label": "Bridge from Spreadsheets to Strategy Lab",
            "secondary_target_course_id": "spreadsheet-to-strategy-lab",
        },
        "language": ["en", "id"],
    }
