"""Original course: Python for the Reluctant Investor.

Confidence builder for non-coders and high-school students. Zero installation
required: run scripts in the guided sandbox, load tabular data, compute moving averages,
inspect trend charts, change parameters, and demystify Python error messages.
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
                "When you click **Run in sandbox**, the server-side guided Python runtime executes those instructions securely in ~40–65 milliseconds and prints the result.\n\n"
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
                    "To route a formatted document to a physical office paper printer connected to the network",
                    "To display text or calculated numbers on the computer screen or terminal",
                    "To permanently delete historical calculation records from local computer storage",
                ],
                1,
                "In programming, print() outputs text and variables to the screen or console.",
            ),
            "exercises": [
                question(
                    "What is the purpose of the `print()` function in Python?",
                    [
                        "To route a formatted document to a physical office paper printer connected to the network",
                        "To display text or calculated numbers on the computer screen or terminal",
                        "To permanently delete historical calculation records from local computer storage",
                    ],
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
            "objective": "Inspect tabular data using Python lists and dictionaries, and understand how pandas loads DataFrames in offline CPython environments.",
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
                "In Excel, you double-click a file to see rows and columns. In Python, structured data is organized into sequences of rows and fields.\n\n"
                "In Quanta's guided runtime, we represent tabular records using clean Python lists and dictionaries:\n\n"
                "```python\n"
                "rows = [\n"
                "    {'date': '2026-01-02', 'close': 10250},\n"
                "    {'date': '2026-01-05', 'close': 10300},\n"
                "]\n"
                "```\n\n"
                "In a full desktop or offline CPython environment (such as Jupyter Notebooks), data scientists use the popular **pandas** library, where tabular datasets are called **DataFrames**:\n\n"
                "```python\n"
                "# (Offline CPython / Desktop environment)\n"
                "import pandas as pd\n"
                "df = pd.read_csv('prices.csv')\n"
                "print(df.head())\n"
                "```\n\n"
                "$$\n"
                r"\mathrm{Shape}(D) = (N_{\text{rows}}, P_{\text{columns}})"
                "\n$$\n\n"
                "## A worked example\n\n"
                "You export a table of daily stock prices. By calling `len(rows)`, Python reports `5` records. By reading `rows[0]`, you inspect the first recorded day.\n\n"
                "In an offline pandas environment, calling `df.head()` displays the top 5 rows of the DataFrame, while `df.tail(2)` displays the final two rows.\n\n"
                "## Work through it yourself\n\n"
                "1. Look at the code in the sandbox.\n"
                "2. Click **Run in sandbox** to inspect the first and last rows.\n"
                "3. Try changing `rows[0]` to `rows[1]` to see the second day's closing price.\n\n"
                "### In the sandbox\n\n"
                "Run the script to see how tabular data rows are inspected in Python."
            ),
            "exercise": question(
                "In the Python pandas library, what method is used to quickly inspect the first few rows of a table (DataFrame)?",
                [
                    "df.first_things_first() to display initial records",
                    "df.head()",
                    "df.look_inside() to print memory buffers",
                ],
                1,
                "df.head() displays the top 5 rows of a DataFrame by default.",
            ),
            "exercises": [
                question(
                    "What pandas method inspects the first rows of a DataFrame?",
                    [
                        "df.first_things_first() to display initial records",
                        "df.head()",
                        "df.look_inside() to print memory buffers",
                    ],
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
            "objective": "Calculate column means and simple moving averages using positional arguments and understand rolling warm-up behavior.",
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
                "In Python, operations apply across arrays and series automatically:\n\n"
                "```python\n"
                "# In Quanta guided runtime (positional arguments, partial warm-up without NaN):\n"
                "trend = sma(data['close'], 20)\n"
                "\n"
                "# In offline pandas environment:\n"
                "sma_20 = df['close'].rolling(20).mean()\n"
                "```\n\n"
                "In the guided runtime, `sma(data['close'], 20)` evaluates partial-window warm-up on the earliest bars (averaging available bars so far without producing `NaN`). In standard offline pandas, `df['close'].rolling(20).mean()` marks the first 19 observations as `NaN` (Not a Number) because 20 bars have not yet elapsed.\n\n"
                "$$\n"
                r"\overline{P} = \frac{1}{N} \sum_{i=1}^N P_i"
                "\n$$\n\n"
                "## A worked example\n\n"
                "Given ten consecutive daily prices, the average is calculated in microseconds. The 3-day trailing average sums the latest three bars and divides by 3.\n\n"
                "## Work through it yourself\n\n"
                "1. Run the sandbox script.\n"
                "2. Change `prices[-1] + prices[-2] + prices[-3]` to compute a 2-day average by using only the last two elements.\n"
                "3. Observe how the moving average reacts faster with a shorter lookback window.\n\n"
                "### In the sandbox\n\n"
                "Run the script to observe vector mathematics and moving averages."
            ),
            "exercise": question(
                "Why do the first two values of a 3-day rolling moving average show `NaN` (empty) in standard pandas?",
                [
                    "Because the computer's temporary memory buffer exhausts allocation space during the initial window calculation pass",
                    "Because calculating a 3-day average requires at least 3 historical observations, so days 1 and 2 cannot be computed yet",
                    "Because days 1 and 2 are designated statutory non-trading weekend sessions across all international securities exchanges",
                ],
                1,
                "A rolling window of size k requires k observations; earlier rows lack sufficient history and are correctly marked as NaN in pandas.",
            ),
            "exercises": [
                question(
                    "Why do the first two values of a 3-day rolling moving average show NaN in pandas?",
                    [
                        "Because the computer's temporary memory buffer exhausts allocation space during the initial window calculation pass",
                        "Because calculating a 3-day average requires at least 3 historical observations, so days 1 and 2 cannot be computed yet",
                        "Because days 1 and 2 are designated statutory non-trading weekend sessions across all international securities exchanges",
                    ],
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
            "objective": "Inspect trend levels in the console, and understand how matplotlib creates line charts with legends in offline CPython environments.",
            "kind": "fundamentals",
            "formula": r"\text{Chart} = \text{Plot}(\text{Date}, \text{Price}) \cup \text{Plot}(\text{Date}, \text{SMA})",
            "code": (
                "# Lesson 4: Drawing a chart and visualization\n"
                "# Visualizing price trend levels in the console\n"
                "prices = [100, 103, 102, 106, 105, 108, 112, 110, 115, 118]\n"
                "print('=== SIMULASI TREN HARGA SAHAM ===')\n"
                "min_p = min(prices)\n"
                "max_p = max(prices)\n"
                "spread = max_p - min_p + 0.0001\n"
                "for i in range(len(prices)):\n"
                "    p = prices[i]\n"
                "    day = i + 1\n"
                "    level = int((p - min_p) / spread * 10) + 1\n"
                "    print(f'Hari {day:2d} | Harga: {p} | Tingkat Tren: {level}')\n"
                "print('Visualisasi level harga berhasil dirender!')\n"
            ),
            "content": (
                "## The idea\n\n"
                "A table of numbers can be difficult to interpret at a glance. Visualizing data reveals trends, support levels, and volatility spikes instantly.\n\n"
                "In Quanta's guided runtime, trend levels are printed cleanly in the console terminal. In an offline desktop Python environment, data scientists use **matplotlib**:\n\n"
                "```python\n"
                "# (Offline CPython / Desktop environment)\n"
                "import matplotlib.pyplot as plt\n"
                "\n"
                "dates = ['2026-01-02', '2026-01-05', '2026-01-06', '2026-01-07']\n"
                "prices = [100.0, 102.5, 101.0, 104.0]\n"
                "sma_line = [100.0, 101.25, 101.17, 101.88]\n"
                "\n"
                "plt.plot(dates, prices, label='Close Price')\n"
                "plt.plot(dates, sma_line, label='Trend SMA', linestyle='--')\n"
                "plt.title('Stock Price Trajectory')\n"
                "plt.xlabel('Date')\n"
                "plt.ylabel('Price (IDR)')\n"
                "plt.legend()\n"
                "plt.savefig('my_chart.png')\n"
                "```\n\n"
                "$$\n"
                r"\text{Visual Signal: Price crosses above SMA} \implies \text{Bullish Momentum}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "In the sandbox, the script tracks a 10-day price trajectory from 100 to 118. Level indicators show rising numbers (from 1 up to 10), confirming an upward trend.\n\n"
                "## Work through it yourself\n\n"
                "1. Click **Run in sandbox** to see the trend levels printed in the console.\n"
                "2. Try modifying the price list with a sudden drop (e.g. `[100, 105, 80, 75]`) and re-run.\n"
                "3. Observe how the trend levels drop immediately.\n\n"
                "### In the sandbox\n\n"
                "Run the script to observe trend levels in the console terminal."
            ),
            "exercise": question(
                "Why is visual chart plotting essential in systematic investment research?",
                [
                    "Because graphic visualizations require substantially more computer memory and colorful display pixels than plain text logs",
                    "To quickly verify data quality, spot obvious anomalies (such as negative prices or missing periods), and confirm mathematical trends",
                    "To permanently replace numeric quantitative tables and eliminate the need to ever inspect raw mathematical trade execution log data files",
                ],
                1,
                "Visual charts help analysts immediately detect data anomalies, bad ticks, and trend regime changes that summary numbers might obscure.",
            ),
            "exercises": [
                question(
                    "Why is visual plotting essential in quantitative research?",
                    [
                        "Because graphic visualizations require substantially more computer memory and colorful display pixels than plain text logs",
                        "To quickly verify data quality, spot obvious anomalies (such as negative prices or missing periods), and confirm mathematical trends",
                        "To permanently replace numeric quantitative tables and eliminate the need to ever inspect raw mathematical trade execution log data files",
                    ],
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
            "objective": "Modify a single parameter at the top of a script (lookback_window) and observe the systematic change in signal counts.",
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
                "# Counting prices above the moving average threshold\n"
                "signal_count = 0\n"
                "for p in sample_prices:\n"
                "    if p > parameterized_mean:\n"
                "        signal_count = signal_count + 1\n"
                "print('Parameterized Rolling Average:', round(parameterized_mean, 2))\n"
                "print(f'Lookback window: {lookback_window} | Bullish signals: {signal_count}')\n"
            ),
            "content": (
                "## The idea\n\n"
                "The hallmark of disciplined quantitative programming is **clean parameterization**.\n\n"
                "Never bury magic numbers deep inside your code. Instead, place key parameters at the very top of your script in clearly named variables (`lookback_window = 7`). That way, you or your teammates can change one assumption and observe the effect without having to edit formulas throughout the program:\n\n"
                "$$\n"
                r"\theta = \{\text{lookback\_window}, \text{stop\_loss}\} \to \text{Output}(\theta)"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A script tests a moving average benchmark on market data. With `lookback_window = 7`, the average reflects recent prices and the script counts **5 prices above the benchmark**.\n\n"
                "When you change `lookback_window = 3`, the moving average reacts faster to the recent run-up, altering the benchmark threshold and changing the signal count. You have successfully performed a **parameter sensitivity experiment**!\n\n"
                "## Work through it yourself\n\n"
                "1. Run the script with `lookback_window = 7`.\n"
                "2. Change line 3 to `lookback_window = 3`.\n"
                "3. Re-run and observe how the moving average and signal count respond.\n\n"
                "### In the sandbox\n\n"
                "Run the script, change the parameter, and observe how the output responds."
            ),
            "exercise": question(
                "Why should parameters (such as moving average windows or stop-loss percentages) be defined at the top of a Python script?",
                [
                    "To conceal internal mathematical calculation variables from compiler memory analyzers",
                    "To make scripts modular and easily testable without altering core calculation logic",
                    "Because the Python programming language strictly prohibits embedding numeric literals inside user-defined functions",
                ],
                1,
                "Defining parameters at the top avoids hardcoding magic numbers and allows clean, repeatable sensitivity experiments.",
            ),
            "exercises": [
                question(
                    "Why define parameters at the top of a script?",
                    [
                        "To conceal internal mathematical calculation variables from compiler memory analyzers",
                        "To make scripts modular and easily testable without altering core calculation logic",
                        "Because the Python programming language strictly prohibits embedding numeric literals inside user-defined functions",
                    ],
                    1,
                    "Placing parameters at the top makes scripts modular and avoids hardcoded magic numbers.",
                ),
            ],
            "terms": [
                {"term": "Parameter", "definition": "A configuration variable that is set before executing a program and controls its specific behavior."},
                {"term": "Sensitivity Analysis", "definition": "The study of how the uncertainty in the output of a mathematical model can be divided and allocated to different sources of uncertainty in its inputs."},
            ],
            "references": [
                {"title": "Python Software Foundation · Defining Functions and Modular Design", "url": "https://docs.python.org/3/tutorial/controlflow.html#defining-functions"},
            ],
        },
        {
            "id": "27.6",
            "part": "2",
            "title": "When it breaks: reading a traceback",
            "subtitle": "Demystify error messages and fix the three most common beginner bugs.",
            "minutes": 15,
            "objective": "Read Python runtime errors and tracebacks, locate line numbers, and resolve SyntaxError, KeyError, and IndexError.",
            "kind": "fundamentals",
            "formula": r"\text{Error Rule: Read error class and locate line number to diagnose fix}",
            "code": (
                "# Lesson 6: Diagnosing and fixing the most common beginner bugs!\n"
                "# BUG 1: KeyError (Typo in column name, e.g. 'Close' vs 'close')\n"
                "# BUG 2: IndexError (Accessing an element past the list length)\n"
                "\n"
                "print('1. Fixing KeyError (matching exact case):')\n"
                "data = {'close': 10500, 'volume': 2000}\n"
                "# data['Close'] causes KeyError -> use exact lowercase 'close'\n"
                "print('Harga Close:', data['close'])\n"
                "\n"
                "print('2. Fixing IndexError (staying within list bounds):')\n"
                "symbols = ['BBCA', 'BBRI', 'TLKM']\n"
                "# symbols[5] causes IndexError -> valid indices are 0, 1, 2\n"
                "print('Valid symbol at index 0:', symbols[0])\n"
                "print('Semua bug berhasil dipelajari dan diperbaiki!')\n"
            ),
            "content": (
                "## The idea\n\n"
                "When a beginner sees an error message, their first instinct is often panic. They assume they broke the computer or aren't cut out for coding.\n\n"
                "Professional programmers see error messages dozens of times every day. An error message is not an insult—**it is a helpful roadmap that tells you exactly where and why something went wrong**.\n\n"
                "In Quanta's guided runtime, errors are displayed as concise, actionable messages (such as `KeyError: 'Close'` or `IndexError: list index out of range`). In an offline CPython environment, Python prints a multi-line stack trace called a **traceback**:\n"
                "1. **Read the error message first**: It states the error class and description.\n"
                "2. **Check the line number**: It points directly to the line of code that triggered the failure.\n\n"
                "$$\n"
                r"\text{Runtime Error} \to (\text{Line Number}, \text{Error Class}, \text{Error Description})"
                "\n$$\n\n"
                "## A worked example\n\n"
                "### The Four Classic Beginner Bugs\n\n"
                "1. **`SyntaxError`**: A typo in Python grammar, such as a missing closing parenthesis `)` or missing quotation mark `'`.\n"
                "2. **`KeyError`**: Trying to access a dictionary key that does not exist—usually caused by capitalization typos (e.g. asking for `data['Close']` when the key is `data['close']`). Python is strictly case-sensitive!\n"
                "3. **`IndexError`**: Attempting to read a list position that does not exist (e.g. `symbols[5]` when `symbols` only has 3 items). Remember Python is 0-indexed!\n"
                "4. **`ZeroDivisionError`**: Dividing by zero (e.g. calculating return when purchase price was set to 0).\n\n"
                "## Work through it yourself\n\n"
                "1. Inspect the code in the sandbox.\n"
                "2. Try temporarily changing `symbols[0]` to `symbols[10]` to see an `IndexError` occur.\n"
                "3. Fix it by choosing an index between 0 and 2, and re-run.\n\n"
                "### In the sandbox\n\n"
                "Run the script to see how fixing key names and indices resolves runtime errors."
            ),
            "exercise": question(
                "When Python displays a traceback error, what is the recommended procedure for diagnosing it?",
                [
                    "Immediately reformat the operating system disk partition and reinstall all commercial software packages",
                    "Read the very last line to identify the error type, then check the line number to locate and fix the specific line of code",
                    "Ignore the error message because modern cloud servers and operating systems automatically resolve all unhandled software exceptions",
                ],
                1,
                "The last line of a traceback identifies the exact error type (e.g. KeyError), while the line number points directly to where the error occurred.",
            ),
            "exercises": [
                question(
                    "When Python displays a traceback, how should you diagnose it?",
                    [
                        "Immediately reformat the operating system disk partition and reinstall all commercial software packages",
                        "Read the very last line to identify the error type, then check the line number to locate and fix the specific line of code",
                        "Ignore the error message because modern cloud servers and operating systems automatically resolve all unhandled software exceptions",
                    ],
                    1,
                    "The last line states the error class and the line number locates the defect.",
                ),
            ],
            "terms": [
                {"term": "Traceback", "definition": "A report containing the active stack frames at a certain point in time, showing the execution path leading up to an unhandled exception."},
                {"term": "IndexError", "definition": "An exception raised when attempting to access an index that is outside the bounds of a sequence such as a list."},
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
            "version": 3,
            "description": "Practical confidence-builder assessment on basic Python execution, pandas CSV handling, moving averages, and traceback diagnosis.",
            "moduleIds": [m["id"] for m in modules],
            "questions": [
                {
                    "id": "python-final-q1",
                    "lessonId": "27.1",
                    "question": "In Python, which built-in function is used to output text or calculated values directly to the console terminal?",
                    "options": [
                        "print()",
                        "echo() across terminal sessions",
                        "display_window() to graphical interfaces",
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
                        "pd.open_table() for spreadsheets",
                        "pd.import_sheet() for workbooks",
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
                        "df['close'].average(20) across all historical rows",
                        "df['close'].sum() / 20 with cumulative summation",
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
                        "The underlying asset price suddenly drops to exactly zero during regular exchange trading",
                        "The recorded trading volume becomes negative during afternoon sessions",
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
                        "Because the Python programming language strictly prohibits embedding numeric literals inside user-defined functions",
                        "To force the operating system kernel to allocate dedicated high-speed cache memory for script execution",
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
                        "The local computer hard drive has completely exhausted available physical storage capacity",
                        "The installed Python interpreter version is obsolete and incompatible with the current hardware",
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
                "title": "Python for Investors Reference Sheet",
                "url": "/course-assets/python-investor/cheat-sheet.md",
            },
        ],
        "references": [
            {"title": "Python Software Foundation · Official Documentation", "url": "https://docs.python.org/3/"},
            {"title": "pandas Documentation · Getting Started Tutorials", "url": "https://pandas.pydata.org/docs/getting_started/index.html"},
        ],
        "exams": exams,
        # CS-1 course metadata
        "slug": "python-reluctant-investor",
        "subtitle": "Zero-Prerequisite Coding Confidence for Investors",
        "audience_tags": ["beginner", "highschool", "python", "non-coder"],
        "estimated_minutes": sum(m["minutes"] for m in modules),
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
