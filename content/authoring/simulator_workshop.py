"""Trading simulator workshop: a step-by-step course for the Quanta paper-trading terminal.

Every company, headline and price in the terminal is fictional and the market is simulated.
The lessons teach the tool and the process of using it, never a claim about real securities.
"""

from applied_courses import checkpoints_for, study
from book_courses import finish

IG = "https://www.investor.gov/introduction-investing"

ORDER_TYPES = (
    "Investor.gov · Types of Orders",
    f"{IG}/investing-basics/how-stock-markets-work/types-orders",
)
ORDER_BULLETIN = (
    "Investor.gov · Investor Bulletin: Understanding Order Types",
    f"{IG}/general-resources/news-alerts/alerts-bulletins/investor-bulletins-14",
)
STOP_BULLETIN = (
    "Investor.gov · Investor Bulletin: Stop, Stop-Limit, and Trailing Stop Orders",
    f"{IG}/general-resources/news-alerts/alerts-bulletins/investor-bulletins-15",
)
STOP_GLOSSARY = (
    "Investor.gov · Glossary: Stop Order",
    f"{IG}/investing-basics/glossary/stop-order",
)
EXECUTING = (
    "Investor.gov · Executing an Order",
    f"{IG}/investing-basics/how-stock-markets-work/executing-order",
)
BID_ASK = (
    "Investor.gov · Glossary: Bid Price/Ask Price",
    f"{IG}/investing-basics/glossary/ask-price",
)
QUOTES = (
    "Investor.gov · Glossary: Stock Quotes",
    f"{IG}/investing-basics/glossary/stock-quotes",
)
BROKERAGE = (
    "Investor.gov · Types of Brokerage Accounts",
    f"{IG}/investing-basics/how-stock-markets-work/types-brokerage-accounts",
)
MARGIN_ACCOUNT = (
    "Investor.gov · Glossary: Margin Account",
    f"{IG}/investing-basics/glossary/margin-account",
)
MARGIN = (
    "Investor.gov · Investor Bulletin: Understanding Margin Accounts",
    f"{IG}/general-resources/news-alerts/alerts-bulletins/investor-bulletins-29",
)
MARGIN_INTEREST = (
    "Investor.gov · Investor Bulletin: Interested in Margin? Understand Interest",
    f"{IG}/general-resources/news-alerts/alerts-bulletins/investor-bulletins/investor-bulletin-interested-margin-understand-interest",
)
SHORT = (
    "Investor.gov · Investor Bulletin: An Introduction to Short Sales",
    f"{IG}/general-resources/news-alerts/alerts-bulletins/investor-bulletins-51",
)
READ_10K = (
    "Investor.gov · How to Read a 10-K/10-Q",
    f"{IG}/general-resources/news-alerts/alerts-bulletins/investor-bulletins/how-read",
)
READ_8K = (
    "Investor.gov · How to Read an 8-K",
    f"{IG}/general-resources/news-alerts/alerts-bulletins/investor-bulletins/how-read-8",
)
STATEMENTS = (
    "SEC · Beginners' Guide to Financial Statements",
    "https://www.sec.gov/about/reports-publications/investorpubsbegfinstmtguide",
)
RUMORS = (
    "Investor.gov · Updated Investor Alert: Social Media and Investing -- Stock Rumors",
    f"{IG}/general-resources/news-alerts/alerts-bulletins/investor-alerts/updated-1",
)
HOT_STOCK = (
    "Investor.gov · Investor Alert: The Latest Hot Stock and Short-Term Trading Based on Social Media",
    f"{IG}/general-resources/news-alerts/alerts-bulletins/investor-alerts/investor-alert-thinking-about-investing-latest-hot-stock-understand-significant-risks-short-term",
)
PERFORMANCE = (
    "Investor.gov · Investor Bulletin: Performance Claims",
    f"{IG}/general-resources/news-alerts/alerts-bulletins/investor-bulletins-47",
)
RISK_TOLERANCE = (
    "Investor.gov · Gauge Your Risk Tolerance",
    f"{IG}/investing-basics/save-and-invest/gauge-your-risk-tolerance",
)
GOALS = (
    "Investor.gov · Invest For Your Goals",
    f"{IG}/investing-basics/invest-your-goals",
)
NYSE = ("NYSE · Holidays & Trading Hours", "https://www.nyse.com/trade/hours-calendars")
NUMPY = (
    "NumPy · Random Generator",
    "https://numpy.org/doc/stable/reference/random/generator.html",
)
DECIMAL = (
    "Python · decimal: Decimal fixed-point and floating-point arithmetic",
    "https://docs.python.org/3/library/decimal.html",
)
EWM = (
    "pandas · DataFrame.ewm: exponentially weighted windows",
    "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html",
)
LEAKAGE = (
    "scikit-learn contributors · Common pitfalls and data leakage",
    "https://scikit-learn.org/stable/common_pitfalls.html",
)
CSV_SAFETY = (
    "OWASP · CSV Injection",
    "https://community.owasp.org/attacks/CSV_Injection",
)

COURSE_GUIDE = (
    "Learn to use the Quanta Trading simulator step by step: set up a paper account, read the market and its simulated news, place and manage orders, and review your own process.",
    "The Trading simulator is a professional flight simulator for your trading practice, equipped with a $100,000 virtual paper balance and an entire market of fictional companies. Nothing in it uses real money, which is exactly what makes it so valuable: you can make mistakes, test order types, experience market friction, and review your psychological decision-making in a safe sandbox before committing actual capital.\n\n"
    "This workshop guides you through every tool and panel in the terminal across three structured units:\n"
    "• Unit 1 (Set up and read the market): Configure reproducible paper runs with market seeds and cost parameters, navigate the multi-panel terminal interface, advance the chronological replay clock without hindsight bias, and interpret quantitative newsroom sentiment scores.\n"
    "• Unit 2 (Place and manage orders): Master market and limit orders with cash reservation safeguards, calculate execution friction (slippage, half-spread, and volume participation caps), set protective stops, trailing stops, and bracket exits, and operate margin accounts with short selling and borrow fee accounting.\n"
    "• Unit 3 (Research, review and discipline): Inspect company financial statements and earnings surprises, split charts into multi-pane analytics monitors, audit trading performance against the QX-200 market benchmark, and complete a rigorous 1-week capstone mission inside your personal trading charter.\n\n"
    "Every lesson pairs clear conceptual models with step-by-step arithmetic, runnable Python worksheets, and hands-on terminal walkthroughs. Six lessons link directly to interactive practice missions that evaluate your trading discipline, adherence to rules, and execution process rather than sheer paper profit.",
)

APPLICATIONS = [
    (
        "13.1",
        "idempotency",
        "A request to create a paper account carries its own identifier, so a retry after a lost reply returns the original run instead of opening a second account.",
        "A fictional learner clicks Create new paper account, loses the connection before the confirmation arrives, and clicks again after changing the Market seed (optional) field from 4242 to 5151 (illustrative values). Decide which run exists afterwards and what the learner should check.",
        "The terminal keeps the saved request and resends it unchanged, so the run keeps the original seed and cost settings rather than the edited form. Confirm the seed in the status bar and the costs in the Execution model panel before relying on the run. An identifier makes a retry safe, but it also means a changed intention needs a new request.",
    ),
    (
        "13.2",
        "oracle",
        "A price on a screen is only usable with its timestamp, units and source attached, which the chart header and the replay clock supply.",
        "A fictional learner pastes a chart screenshot that shows 148.62 and nothing else (illustrative). List the facts needed before that number can be treated as a price you could have traded at.",
        "The symbol and timeframe say which bar it belongs to, ET and the replay clock say when it applied, and the SYNTHETIC label says it is generated rather than recorded market data. Without those facts the figure could describe any bar of any company, so the header and clock text are part of the price.",
    ),
    (
        "13.3",
        "alfred",
        "The replay clock keeps the terminal on what was knowable at each moment, much as a vintage database keeps the values an analyst could actually see on a given date.",
        "A fictional learner decides at Day 2, bar 110 to buy, uses the 1D jump, and then writes that the decision was obvious all along (illustrative). Describe which record would show whether the reasoning really came first.",
        "A dated note written before the jump, naming the company, the expectation and what would change the view, is the only proof of foresight. The terminal never sends data beyond the clock, so any hindsight comes from rewriting the reasoning afterwards rather than from the data.",
    ),
    (
        "13.4",
        "gme",
        "A sharp move with a story attached can feel like proof that the story caused it, which is the habit the newsroom's scores let a learner test.",
        "A fictional stock rises 4% in one bar while one +250 point company headline and three zero-point chatter items sit on the tape (illustrative numbers). Estimate how much of the move the score explains and name two other things that could account for the rest.",
        "A +250 point item models +2.50% in total with 58% on the dated bar, about 1.45%. The remaining 2.55% would come from noise and from sector or macro items that reach the company through their loadings. A tidy story for the whole move is a hypothesis to check, not a measurement.",
    ),
    (
        "13.5",
        "knight",
        "A preview, a cash reservation and a next-bar rule work as order-level controls of the kind that Knight Capital's faulty release lacked.",
        "A fictional learner leaves Shares at 1,000 instead of 10 on a $100,000 account while the last price is near 148.50 (illustrative). Describe which control stops the order before it is accepted and what the learner sees.",
        "The reservation check compares an estimated debit of roughly $148,550 with available cash and blocks Preview, showing 'Insufficient available cash, including working orders and fees.' The control only helps because it runs before acceptance; a typo that still fits inside the account, such as 100 shares, would pass, so the written reason and the preview remain the learner's own checks.",
    ),
    (
        "13.6",
        "overload",
        "A bar's volume is a bounded resource shared in arrival order, so orders beyond its capacity wait for later bars the way work waits in an overloaded queue.",
        "Fictional orders A (300 shares) and B (100 shares) queue in one stock on a bar with volume 24,000 and the default 1% participation (illustrative). State how many shares each receives on that bar and on the next one, whose capacity is 180.",
        "Capacity on the first bar is 240, so A takes all of it and B receives nothing. On the next bar A needs 60 more and B then takes its 100 from the remaining 120. Arrival order, not size or urgency, decides who is served, and the unfilled part keeps working.",
    ),
    (
        "13.7",
        "flash_crash",
        "A stop is a trigger, not a price guarantee, a distinction that the thin and fast conditions of 6 May 2010 made visible.",
        "A fictional learner holds 10 shares with a sell stop at 145.00 and the next bar opens at 142.00 after a gap (illustrative). Compute the fill with the default 3 basis points of friction and compare it with the stop price.",
        "The fill is the lower of 142.00 and 145.00, less 3 basis points: 142.00 × 0.9997 = 141.96, which is 3.04 below the stop and about $30 on 10 shares. A stop controls when an exit is attempted, not the price obtained, and a stop-limit would have risked no fill at all.",
    ),
    (
        "13.8",
        "ldi",
        "A leveraged position can be forced to raise cash at the worst moment, as a short here is bought in when equity falls under 30% of gross exposure.",
        "A fictional margin account holds $100,000 and sells short 600 shares at a fill of 150.00 (illustrative, ignoring fees). Find the price at which equity falls under 30% of gross exposure.",
        "Cash is 100,000 + 90,000 = 190,000, so equity is 190,000 − 600P while 30% of gross is 180P. The buy-in comes when P exceeds 190,000 ÷ 780 = 243.59, a rise of about 62%. A smaller short sits further from the call, so size is the control the account actually has.",
    ),
    (
        "13.9",
        "ge_disclosure",
        "A headline earnings figure is not a full explanation, so the Company tab asks a learner to read the statements and ratios behind the surprise.",
        "A fictional company beats consensus EPS by 5% while its Cash flow tab shows operating cash flow falling and its balance sheet shows short-term debt rising (illustrative). List the statement lines to check before calling the quarter good.",
        "Compare Operating cash flow and Free cash flow with Net income, then look at Short-term debt and External financing raised, and at Receivables and Inventory for working-capital strain. A beat that rests on borrowing or unpaid invoices is a different quarter from one that rests on cash.",
    ),
    (
        "13.10",
        "ml_pipeline",
        "Choosing a screen's threshold after seeing which names rose is the screening version of leaking the answer into the features.",
        "A fictional learner runs the Oversold screen over five sessions and finds that 3 of 5 listed stocks rose the next session, then tightens the RSI threshold from 30 to 22 because it would have caught the winners (illustrative). Explain what is wrong and how to test the screen fairly.",
        "The new threshold was chosen after the outcomes were known, so a better-looking hit rate is expected by construction. Fix the screen first, write the prediction, record many sessions, and compare the hit rate with the Whole listing. Three of five is too few observations to separate a real pattern from luck.",
    ),
    (
        "13.11",
        "factors",
        "Beta and alpha against the QX-200 ask the same question as a factor audit: how much of a return came from the market and how much is left unexplained.",
        "A fictional account returns +3.0% in a week when the QX-200 rises 2.4% and the account's beta is 0.9 (illustrative, ignoring the risk-free rate). Compute the excess return and the part of the return that beta explains.",
        "Excess return is 3.0 − 2.4 = +0.6 percentage points. Beta explains 0.9 × 2.4 = 2.16 points, which leaves 0.84 points unexplained. That remainder is an estimate from one week of a generated market, not evidence of skill.",
    ),
    (
        "13.12",
        "reporting",
        "A review that another person can read names its settings, sample, costs and limitations, which the exported run and the capstone checklist record.",
        "A fictional learner ends a charter week with a total return of +0.35% (illustrative). Write the five facts that must sit beside that number in a review.",
        "State the seed and cost settings, the number of sessions and orders, the QX-200 return and the excess return, what the simulator does not model (dividends, queue position and real borrow availability), and that one generated week is too short to show skill. A reader can then judge the claim without trusting it blindly.",
    ),
]


def text(value):
    """Normalize indentation and whitespace for markdown text."""
    import textwrap

    return textwrap.dedent(value).strip()


CLOSING = (
    "Write down what you expect before you advance the clock, and what happened afterwards. "
    "Every company, headline and price in the terminal is fictional and the market is simulated, "
    "so a good result here is practice for a process, not evidence of skill."
)


def build_simulator_workshop():
    modules = []

    def add(
        title,
        objective,
        principle,
        case,
        workflow,
        practice,
        formula,
        code,
        task,
        solution,
        questions,
        refs,
        minutes,
    ):
        index = len(modules) + 1
        rows = []
        for offset, (prompt, correct, wrong1, wrong2, explanation) in enumerate(questions):
            options = [correct, wrong1, wrong2]
            shift = (index + offset) % 3
            options = options[shift:] + options[:shift]
            rows.append((prompt, options, options.index(correct), explanation))
        item = study(
            f"13.{index}",
            (index - 1) // 4 + 1,
            title,
            objective,
            text(principle),
            text(case),
            text(workflow) + "\n\n### Practise in the terminal\n\n" + text(practice) + "\n\n" + CLOSING,
            formula,
            code,
            task,
            solution,
            rows,
            refs,
        )
        item["minutes"] = 30
        reading, steps, notebook = minutes
        item["reading"] = (
            f"30-minute session: {reading} minutes reading the idea and the example, {steps} minutes "
            f"following the steps in the terminal and {notebook} minutes recomputing the worksheet and "
            "writing your notebook entry; all companies and prices are fictional and the market is simulated."
        )
        modules.append(item)

    # ---------------------------------------------------------------- Unit 1
    add(
        "Start a paper run: account type, seed and a fictional market",
        "Create a paper account whose settings you can explain, and know what a new run keeps, archives and replaces.",
        r"""
        A paper trading run is a controlled scientific experiment, and its parameters define the experimental conditions. When you practice trading, you need to know exactly how your account behaves and what market friction you are paying. In the Quanta Trading simulator, every run begins with $100,000 of virtual capital in a synthetic marketplace populated by 32 fictional companies.

        Two core settings configure your trading environment:
        1. Account Type: Choose between Cash (long-only, meaning you can only sell shares you already own) and Margin (which allows you to borrow shares from a broker to sell short, introducing leverage and borrowing fees).
        2. Market Seed: A seed is an integer that initializes the pseudo-random number generator. Because the generator is deterministic, the exact same seed reproduces the exact same price candles, trading volume, news headlines, and company earnings reports every time. This enables scientific benchmarking: you can test two different trading strategies against the exact same market sequence. If you leave the seed blank, the terminal selects an automatic random seed so every run experiences a unique market.

        Trading friction is modeled explicitly using four realistic parameters:
        $$f = \frac{s + \sigma / 2}{10{,}000},\qquad \text{Round-Trip Cost} = 2c + Q \cdot (P_{\text{buy}} - P_{\text{sell}})$$
        Here $c$ is the flat commission per order ($1 by default), $s$ is slippage in basis points (2 bps default), $\sigma$ is the bid-ask spread in basis points (2 bps default), and $\pi$ is the volume participation cap (0.01 or 1% default). One basis point (bps) equals 0.01% (1/10,000). Every new run creates a fresh $100,000 account; it never resets your existing account in place. Earlier runs are safely preserved in your run history for review and CSV export.
        """,
        r"""
        Suppose the next bar opens at $148.50 and you place a market order to buy 10 shares using the default cost settings.

        Step-by-step arithmetic:
        1. Calculate fractional friction:
           $$f = \frac{2 + 2 / 2}{10{,}000} = \frac{3}{10{,}000} = 0.0003 \quad (3\text{ basis points})$$
        2. Compute the buy fill price (open plus friction, rounded to the nearest cent):
           $$P_{\text{buy}} = 148.50 \times (1 + 0.0003) = 148.54455 \implies \$148.54$$
        3. Total cash debited on purchase:
           $$10 \times \$148.54 + \$1.00\text{ (commission)} = \$1{,}485.40 + \$1.00 = \$1{,}486.40$$
           Cash drops from $100,000.00 to $98,513.60.

        Now suppose the market price does not move at all, and you sell your 10 shares on the following bar at an unchanged open of $148.50:
        1. Compute the sell fill price (open minus friction, rounded to the cent):
           $$P_{\text{sell}} = 148.50 \times (1 - 0.0003) = 148.45545 \implies \$148.46$$
        2. Total cash credited on sale:
           $$10 \times \$148.46 - \$1.00\text{ (commission)} = \$1{,}484.60 - \$1.00 = \$1{,}483.60$$
           Final cash ends at $98,513.60 + $1,483.60 = $99,997.20.

        The market price did not change by a single cent, yet your round trip cost $2.80:
        • Spread and slippage drag: 10 × ($148.54 − $148.46) = $0.80.
        • Commission drag: 2 × $1.00 = $2.00.

        If you increase slippage and spread to 10 bps each, friction jumps to 15 bps (0.0015). The same round trip fills at $148.72 and $148.28, costing $6.40. This proves that a trading result is meaningless without recording the cost settings that produced it.
        """,
        """
        **Open the terminal.** Choose **Trading simulator** in the left navigation. On your first visit, the terminal creates a default run: a cash account with $100,000, 32 fictional companies, and a seed tied to your run identifier. The top account bar displays **PAPER TRADING**, **Equity**, **Cash**, and **Realized P&L**. The replay bar reads "Day 2 · bar 110/390" with the clock at "Jan 7, 11:19 AM ET". The status bar indicates whether your run is saved in your local browser cookie or synced with your authenticated account.

        **Open the run dialog.** Click the **New simulation run** icon (circular arrows) on the right side of the replay bar. In the dialog that appears, leave **Practice mission (optional)** on "No mission · free practice" for this introductory exploration.

        **Configure account settings.** Review **Account type**: "Cash · long only" (default) or "Margin · may sell short". Keep Cash selected for now; we will explore Margin accounts in lesson 13.8.

        **Examine market data.** The **Market data** selector displays "Seeded synthetic market". Historical replay is disabled because this course utilizes reproducible synthetic market models.

        **Set your market seed.** In **Market seed (optional)**, type an integer between 0 and 1,000,000 (such as 4242), or leave it empty to see the placeholder "Automatic". A fixed seed ensures that every candle and news event will be completely reproducible.

        **Check execution friction.** Review the four numeric fields: **Commission / order ($)** at 1, **Slippage (bps)** at 2, **Spread (bps)** at 2, and **Volume participation (0–1)** at 0.01. Leave these at their defaults for your initial baseline run.

        **Create the paper account.** Click **Create new paper account**. A confirmation notice will announce: "New $100,000 paper account ready. Prior runs remain in your run history." The status bar displays the active seed.

        **Inspect run history.** Click the **Simulation run history** dropdown in the status bar. The active run is tagged "Current · {date}" while prior sessions are preserved as "Archived · {date}". Selecting an archived run enters a read-only mode for review and data export. Click **Return to current run** to resume active trading.

        **Verify reproducibility.** Create a second run using the exact same seed (4242). Confirm that the opening chart bars and watchlist prices match your first run down to the penny.
        """,
        """
        Create a paper run with seed 4242 and default costs, and record the seed and cost settings in your trading notebook. Create a second run with seed 4242 and verify that prices are identical. Next, create a third run with **Slippage (bps)** set to 10 and **Spread (bps)** set to 10, keeping it ready for lesson 13.5 where you will execute orders under elevated friction.
        """,
        r"f=\frac{s+\sigma/2}{10^{4}},\qquad \text{round-trip cost}=2c+Q\,(P_{\text{buy}}-P_{\text{sell}})",
        '''
from math import floor

def to_cent(x):
    return floor(x * 100 + 0.5) / 100

def round_trip(open_price, shares, commission, slippage_bps, spread_bps):
    friction = (slippage_bps + spread_bps / 2) / 10000
    buy = to_cent(open_price * (1 + friction))
    sell = to_cent(open_price * (1 - friction))
    print("Friction:", friction)
    print("Buy fill:", buy)
    print("Cash after the buy:", round(100000 - shares * buy - commission, 2))
    print("Sell fill:", sell)
    print("Cash after the sale:", round(100000 - shares * buy - commission + shares * sell - commission, 2))
    print("Round-trip cost:", round(2 * commission + shares * (buy - sell), 2))

print("Default costs")
round_trip(148.50, 10, 1, 2, 2)
print("Slippage 10 bps and spread 10 bps")
round_trip(148.50, 10, 1, 10, 10)
''',
        "In your notebook, write the seed and the four cost settings of your run. Then compute the round-trip cost of buying and selling 20 shares at an unchanged open of 96.40, first with the default costs and then with Slippage 10 bps and Spread 10 bps, and say which settings you would use for a first week of practice and why.",
        "With default costs, friction is 0.0003: the buy fills at 96.43 and the sale at 96.37, resulting in a round-trip cost of 2 × $1.00 commission plus 20 × $0.06 spread drag = $3.20. With Slippage 10 bps and Spread 10 bps, friction rises to 0.0015: the buy fills at 96.54 and the sale at 96.26, yielding a cost of $2.00 plus 20 × $0.28 = $7.60. For an initial practice week, the default settings provide a clean baseline to master order mechanics, while elevated friction offers a realistic stress test for active strategies. Always document your cost settings beside performance reports.",
        [
            (
                "Two paper runs use the same Market seed (optional) value but different commission settings. What will be identical between them?",
                "The generated bars, headlines and reporting calendar",
                "Their equity curves, because the same seed produces the same trades",
                "Nothing, because every new run generates a fresh market",
                "The seed fixes the generated market. Your costs and your decisions, not the seed, decide what the account does inside it.",
            ),
            (
                "With the default costs, what friction does a market buy pay on top of the bar's open?",
                "3 basis points: slippage of 2 plus half of the 2 bps spread",
                "4 basis points: slippage plus the full spread",
                "2 basis points: slippage alone",
                "Friction is (slippage + spread ÷ 2) ÷ 10,000 = (2 + 1) ÷ 10,000 = 0.0003, so the spread is split between the buy and the sale.",
            ),
            (
                "What happens to an earlier run when you click New simulation run and then Create new paper account?",
                "It stays in the run history as an archived run that you can review and export but not trade",
                "Its cash is reset to $100,000 in place and its history is erased",
                "It is deleted together with its trade journal",
                "A new run is a new account. Earlier runs remain under Simulation run history as archived runs, open for review and export only.",
            ),
            (
                "Why does the course ask you to write the seed and the four cost settings beside every result?",
                "The same decisions can score differently under different settings, and the seed lets you rebuild the same market",
                "The terminal refuses to place orders until the settings have been written down",
                "The settings change the bars you see after each order is placed",
                "A result only means something under stated conditions. The seed and costs are the conditions, so recording them makes a result repeatable and comparable.",
            ),
        ],
        [BROKERAGE, MARGIN_ACCOUNT, NUMPY],
        (8, 14, 8),
    )

    add(
        "Read the terminal: chart, panels and command codes",
        "Find every panel and shortcut used in later lessons, and read the chart header, timeframes and indicators correctly.",
        r"""
        A professional trading terminal integrates multiple specialized views into a single workspace governed by a synchronized clock. To trade effectively, you must maintain a clear distinction between market observation panels and account state panels:
        • Market Information: The Chart, Newsroom, Company financials, Desk analytics, and Economic Calendar show what the external marketplace is doing.
        • Account State: Positions, Open orders, Order history, Trade blotter, and Account history track what you actually own, what cash is reserved, and what transactions have settled.

        The chart header provides vital metadata about the active instrument:
        $$\text{SMA}_n(t) = \frac{1}{n}\sum_{k=0}^{n-1} C_{t-k}$$
        The header specifies the Symbol (e.g. NVRA), Timeframe (1m, 5m, 15m, 1h, 1D), Time Zone (ET, Eastern Time, matching New York market hours), the label `SYNTHETIC` (confirming simulated market generation), and the Open, High, Low, Close, and Volume ($OHLCV$) of the candle under your pointer.

        Technical indicators require a historical lookback window. A 20-bar Simple Moving Average ($\text{SMA}_{20}$) computes the arithmetic mean of the last 20 closes. It cannot display a value until at least 20 bars have formed on that specific timeframe. If you switch to a 1-hour chart at the start of a run (which has formed only 9 hourly bars), the indicator will show `SMA 20 · warming up` until 11 more hourly candles develop. The Command dialog provides rapid keyboard navigation across every view.
        """,
        r"""
        Let us trace how historical bars populate across timeframes at the start of a standard simulation run:
        At the default starting point (Day 2, bar 110 at 11:19 AM ET), the simulator has generated 500 one-minute bars: all 390 bars from Day 1, plus 110 bars from Day 2 ($390 + 110 = 500$).

        How many bars appear on higher timeframes?
        • On the 1-minute chart: Exactly 500 candles are visible.
        • On the 1-hour chart: Day 1 contains 6 full hours and one 30-minute bar (7 bars), and Day 2 has formed 2 hourly bars so far. The 1h chart holds only 9 bars ($7 + 2 = 9$).
        • On the daily (1D) chart: Only 2 daily candles exist.

        $$742.90 / 5 = 148.58$$
        An $\text{SMA}_{20}$ on the 1-minute chart has 500 bars available, so it displays immediately. On the 1-hour chart, however, only 9 bars exist; it requires 11 additional hourly bars before it can compute its first 20-period average. Moving averages are inherently lagging filters: they summarize past historical price distribution rather than predicting future direction.
        """,
        """
        **Open the Command dialog.** Click the ticker button at the far left of the chart toolbar (showing NVRA by default). The **Command** dialog opens with an active search prompt. You can enter a ticker symbol alone, a function shortcut code alone, or both combined: typing `NVRA N` selects Novara Microsystems and immediately opens its Newsroom. Press Enter. Available function codes include `GP` (chart), `N` or `NEWS` (news), `MOV` or `DESK` (desk analytics), `FA` or `DES` (company fundamentals), `CAL` (economic calendar), `PORT` (portfolio performance), `POS` (positions), `OMON` (open orders), `BLOT` (trade history), and `BUY`/`SELL` (order tickets).

        **Adjust chart timeframes.** In the toolbar, locate the **Chart timeframe** selector: 1m, 5m, 15m, 1h, and 1D. Toggle to 1h and notice how sparse the candles appear, then toggle back to 1m. Use the **Fit chart** and **Return to latest bar** buttons to re-center your view.

        **Read OHLCV values.** Look at the chart header text: "NVRA · 1m · ET · SYNTHETIC" followed by O, H, L, C, and Vol for the candle under your pointer. Volume is especially critical because it bounds how many shares your orders can fill in a single bar.

        **Add an indicator.** Click **Indicators** in the toolbar. The modal opens showing active indicators (Volume and SMA 20). Under **Add indicator**, select RSI (Relative Strength Index). Use the eye icon to toggle visibility or the cross icon to remove an overlay.

        **Use drawing tools.** From the left drawing rail, select **Trend line** and click two points on the chart canvas. Use the Escape key to cancel a drawing tool. Test horizontal lines, rectangles, and price measurement annotations. Use Ctrl+Z (Cmd+Z on macOS) to undo drawings.

        **Organize workspace panels.** The right sidebar contains five primary tabs: **Watchlist**, **News**, **Desk**, **Trade**, and **Drawings**. The bottom panel contains eight operational tabs: **Positions**, **Open orders**, **Order history**, **Trade history**, **Account history**, **Company**, **Performance**, and **Calendar**. You can drag the panel divider lines to customize dimensions or collapse panels entirely to maximize chart area.

        **Quick ticket shortcut.** Right-click anywhere on the chart canvas at a specific price level. The **Trade** ticket opens automatically with **Order type** set to **Limit** and the price pre-filled to that exact level.
        """,
        """
        Open the Command dialog and practice navigating by entering POS, OMON, and BLOT. Toggle to the 1-hour chart and count how many bars have formed. Add an RSI indicator and note its default lookback period (14). In your notebook, list the eight bottom-panel tabs and categorize each as either Market Information or Account State.
        """,
        r"\text{SMA}_{n}(t)=\frac{1}{n}\sum_{k=0}^{n-1}C_{t-k}",
        '''
from math import ceil

day1 = 390
day2 = 110
hourly = ceil(day1 / 60) + ceil(day2 / 60)
print("One-minute bars at the start:", day1 + day2)
print("Hourly bars at the start:", hourly)
print("Daily bars at the start:", 2)
print("Hourly bars still needed for a 20-bar average:", 20 - hourly)

closes = [148.50, 148.56, 148.62, 148.58, 148.64]
total = sum(closes)
print("Sum of the five closes:", round(total, 2))
print("5-bar simple moving average:", round(total / len(closes), 2))
''',
        "In your notebook, build a one-page map of the terminal: the five right-sidebar tabs and the eight bottom-panel tabs, the command code that opens each one you can reach by code, and whether each shows market information or the state of your account. Then work out how many bars the 1h chart holds when a run starts and how many more an SMA 20 needs.",
        "The right sidebar includes Watchlist (W), News (N), Desk (MOV), Trade (BUY/SELL), and Drawings. The bottom panel includes Positions (POS), Open orders (OMON), Order history, Trade history (BLOT), Account history, Company (FA), Performance (PORT), and Calendar (CAL). Positions, Open orders, Order history, Trade history, and Account history represent your account state; News, Desk, Company, and Calendar describe the market; Performance links both. At the initial start, the 1-hour chart has only 9 bars (7 from Day 1 and 2 from Day 2), so an SMA 20 requires 11 more hourly candles before displaying.",
        [
            (
                "At the default start the clock shows Day 2, bar 110 of 390. How many one-minute bars can the 1m chart show?",
                "500: all of Day 1 plus 110 bars of Day 2",
                "390: only the bars of the current session",
                "110: only today's bars",
                "The first 500 observations are available at the start. Day 1 has 390 bars and 110 bars of Day 2 have formed, and 390 + 110 = 500.",
            ),
            (
                "Why can an SMA 20 show 'warming up' on the 1h chart right after a run starts, while the 1m chart does not?",
                "The 1h chart has only about nine bars, and the average needs 20",
                "Hourly averages are calculated only after the first order is placed",
                "The 1h chart reads a different data feed that loads later",
                "An indicator's period counts bars of the displayed timeframe. Nine hourly bars cannot form a 20-bar average, while 500 minute bars can.",
            ),
            (
                "You type NVRA FA in the Command dialog and press Enter. What happens?",
                "Novara is selected and the Company tab opens in the bottom panel",
                "A buy ticket for Novara opens in the Trade tab",
                "The dialog stays open because FA is not a valid code",
                "A ticker followed by a function code does both in turn. FA is the code for company financials, which live in the Company tab.",
            ),
            (
                "In the chart header, what does the label SYNTHETIC tell you?",
                "The bars are generated by the simulator, not recorded from a real market",
                "The prices are delayed by a few minutes",
                "The chart is showing a smoothed moving average instead of prices",
                "SYNTHETIC identifies the data source. A price needs its source, symbol, timeframe and time zone before you can interpret it.",
            ),
        ],
        [NYSE, QUOTES],
        (7, 15, 8),
    )

    add(
        "Move the replay clock without hindsight",
        "Advance the replay clock deliberately, convert bars into sessions, and write each decision down before every jump.",
        r"""
        In the Quanta simulator, the replay clock defines the boundary of what is knowable. The backend server strictly enforces chronological causality: it will never return a price candle, news headline, company financial filing, or economic release dated after the current clock cursor. This eliminates technical look-ahead bias from the data.

        However, the greater threat to learning is psychological hindsight bias inside your own head. Once you advance the replay clock and see a stock surge 8%, human psychology reflexively rationalizes that "the breakout was obvious from the chart pattern." To build disciplined trading habits, you must pre-commit: write down your thesis, expected price direction, and exit trigger in your notebook *before* clicking any replay button.

        The replay clock measures time in discrete 1-minute bars:
        $$\text{Session} = \left\lfloor \frac{c}{390}\right\rfloor + 1,\qquad \text{Bar} = (c \bmod 390) + 1$$
        A standard US equity trading session consists of 390 one-minute bars (09:30 AM to 04:00 PM Eastern Time). A 5-session trading week comprises $5 \times 390 = 1{,}950$ bars. The jump buttons (15m, 1h, 1D, 1W) advance time by 15, 60, 390, or 1,950 bars in a single request. When jumping forward, the server simulates order execution bar-by-bar throughout the interval. Replay speed (1x, 5x, 30x, 390x) governs how many bars advance per 0.8-second tick during continuous playback.
        """,
        r"""
        Let us calculate the exact clock position across consecutive jumps starting from the default cursor $c = 499$:
        1. Default Start: Cursor $c = 499$.
           $$\text{Session} = \lfloor 499 / 390 \rfloor + 1 = 1 + 1 = \text{Day 2}$$
           $$\text{Bar} = (499 \bmod 390) + 1 = 109 + 1 = \text{Bar 110}$$
           Clock time: 09:30 AM + 109 minutes = 11:19 AM ET.

        2. Single Step: Click **Next replay bar** ($c = 500$):
           $$\text{Session} = \lfloor 500 / 390 \rfloor + 1 = \text{Day 2},\quad \text{Bar} = (500 \bmod 390) + 1 = \text{Bar 111}$$
           Clock time: 11:20 AM ET.

        3. 1-Hour Jump: Click **1h** ($+60$ bars $\implies c = 560$):
           $$\text{Session} = \text{Day 2},\quad \text{Bar} = (560 \bmod 390) + 1 = \text{Bar 171}$$
           Clock time: 12:20 PM ET.

        4. 1-Day Jump: Click **1D** ($+390$ bars $\implies c = 950$):
           $$\text{Session} = \lfloor 950 / 390 \rfloor + 1 = 2 + 1 = \text{Day 3},\quad \text{Bar} = (950 \bmod 390) + 1 = \text{Bar 171}$$
           Clock time: 12:20 PM ET on Day 3.

        $$390 \times 0.8 = 312\text{ seconds}$$
        Playback duration: At 1x speed, playing one full 390-bar session requires $390 \times 0.8 = 312$ seconds (about 5.2 minutes). At 30x speed, a session completes in 13 ticks (10.4 seconds). At 390x, an entire session passes in a single tick.
        """,
        """
        **Locate the replay controls.** Beneath the chart canvas, find the replay control bar: **Play replay** / **Pause replay**, **Next replay bar** (single-step), the **Jump replay** group (15m, 1h, 1D, 1W), the **Mark scored headlines** button, **Monitor windows** toggles (1, 2, 3), the **Replay speed** dropdown, the live clock readout, and the session progress bar.

        **Practice pre-commitment.** Open your notebook. Before touching the clock, write down: symbol (NVRA), your expected price move over the next hour (e.g. "Consolidating near $148.50"), and what event would invalidate your view.

        **Step one bar.** Click **Next replay bar**. The counter updates to Day 2, bar 111, 11:20 AM ET, and a notice confirms "Replay advanced by one bar."

        **Execute an hourly jump.** Click **1h**. The clock jumps 60 bars to 12:20 PM ET (bar 171). Compare the newly formed price candles against your written pre-commitment note.

        **Test continuous playback.** Set **Replay speed** to 5x. Click **Play replay** and observe candles printing smoothly at 5 bars per tick. Click **Pause replay** (or press the Escape key) to halt the clock. The replay also pauses automatically whenever an order ticket preview is opened.

        **Observe overnight session gaps.** Step forward until the clock reaches 3:59 PM ET. The indicator reads "Market closed · next session on step". Clicking **Next replay bar** once more jumps to 09:30 AM ET the following morning. Notice how the opening price can gap away from yesterday's close due to simulated overnight news.
        """,
        """
        In a free-practice run, write down an explicit price forecast for NVRA before executing each of three jumps: **15m**, **1h**, and **1D**. After each jump, objectively assess whether your prediction was correct and whether the underlying rationale was sound. The objective is to train yourself to never rewrite your thesis after the fact.
        """,
        r"\text{session}=\left\lfloor \frac{c}{390}\right\rfloor+1,\qquad \text{bar}=(c \bmod 390)+1",
        '''
cursor = 499
print("Start: day", cursor // 390 + 1, "bar", cursor % 390 + 1)
cursor = cursor + 1
print("After Next replay bar: day", cursor // 390 + 1, "bar", cursor % 390 + 1)
cursor = cursor + 60
print("After the 1h jump: day", cursor // 390 + 1, "bar", cursor % 390 + 1)
cursor = cursor + 390
print("After the 1D jump: day", cursor // 390 + 1, "bar", cursor % 390 + 1)
cursor = cursor + 1950
print("After the 1W jump: day", cursor // 390 + 1, "bar", cursor % 390 + 1)
print("Seconds to play one session at 1x:", round(390 * 0.8, 1))
print("Seconds to play one session at 30x:", round(13 * 0.8, 1))
print("Ticks to play one session at 390x:", 1)
''',
        "Starting from Day 2, bar 110, write the day, bar and clock time after Next replay bar, then after the 1h jump, then the 1D jump, then the 1W jump. Then write a decision note for a jump you will make in the terminal, make the jump, and write one sentence comparing the outcome with your note.",
        "Next replay bar moves to Day 2, bar 111 (11:20 AM ET). The 1h jump advances to Day 2, bar 171 (12:20 PM ET). The 1D jump moves to Day 3, bar 171 (12:20 PM ET). The 1W jump reaches Day 8, bar 171 (12:20 PM ET), because each jump accumulates on the prior position. Your decision note must document the instrument, forecasted direction, and invalidation criteria prior to the jump. Afterward, evaluate the rationale rather than just the profit: being right for the wrong reason is luck, while a well-reasoned loss is a normal trading outcome.",
        [
            (
                "A learner clicks the 1D jump button on a minute run. How many bars does the clock advance?",
                "390 bars, one modelled session",
                "1,950 bars, one modelled week",
                "60 bars, one modelled hour",
                "On a minute run the jump buttons 15m, 1h, 1D and 1W advance 15, 60, 390 and 1,950 bars. A session has 390 one-minute bars.",
            ),
            (
                "What does choosing 30× in Replay speed do while Play is on?",
                "It advances 30 bars each tick of about 0.8 seconds, so it is a bar rate rather than a time multiplier",
                "It makes the market move 30 times as much on every bar",
                "It speeds up order fills only, while the chart still advances one bar at a time",
                "Replay speed sets how many bars each tick advances. It does not change how large the moves in the bars are or how fills work.",
            ),
            (
                "From Day 2, bar 110 a learner clicks Next replay bar and then 1h. Which counter should the replay bar show?",
                "Day 2, bar 171",
                "Day 2, bar 170",
                "Day 3, bar 110",
                "The step moves the clock from index 499 to 500 and the 1h jump to 560. Index 560 is Day 2, bar 171, because 560 mod 390 = 170 and the bar number adds 1.",
            ),
            (
                "Why does the course ask you to write your expectation before using a jump button?",
                "Once the outcome is on the chart you can rewrite your reasoning to fit it, so the earlier note is the honest record",
                "The terminal rejects orders placed without a written expectation",
                "A jump hides the market data until your note has been saved",
                "Hindsight does not come from the data, which the terminal limits to the clock, but from reinterpreting your earlier thinking. A dated note prevents that.",
            ),
        ],
        [LEAKAGE, PERFORMANCE],
        (8, 14, 8),
    )

    add(
        "Read the simulated newsroom: scores, tone and chart markers",
        "Read a headline's scope, impact tier and score, interpret the tone gauges, and trace a price move to its scored headline without over-reading the chart.",
        r"""
        In the simulated market, the newsroom engine generates narrative headlines with explicit quantitative impact scores. The simulation price engine translates each scored headline into a modeled price impulse. This design allows you to study cause-and-effect market dynamics in a transparent setting.

        Each score point represents exactly one basis point (0.01%) of modeled price impact:
        $$\frac{\Delta P}{P} = \frac{\text{Score}}{10{,}000},\qquad \text{Market Tone} = \frac{\sum w_i \cdot d_i}{\sum w_i}$$
        A headline scored at $+250$ points models an aggregate $+2.50\%$ price adjustment. In the engine, 58% of this impact is applied immediately to the candle on which the news is dated, while the remaining 42% drifts into the stock price across subsequent bars. In addition, stochastic price noise and broader sector/macro movements act simultaneously on the candle.

        Headlines are categorized by scope and impact tier:
        • Scope Tags: `CO` (single company), `SEC` (industry sector, distributed via sector loadings), `ECO` (macroeconomic report, reaching stocks through beta), and `MKT` (broad market index).
        • Impact Tiers: High (`H`, $\ge 400$ pts, weight 3), Medium (`M`, $\ge 120$ pts, weight 2), Low (`L`, $< 120$ pts, weight 1), and Chatter (dot `·`, 0 pts, weight 0).
        • Market Tone Gauges: Aggregate sentiment is computed as the signed direction ($d_i \in \{+1, -1\}$) multiplied by weight ($w_i$), normalized between $-1.00$ and $+1.00$. Unscored chatter carries zero weight and does not distort tone.
        """,
        r"""
        Suppose a company headline for Novara Microsystems (NVRA) is published with a score of $+250$ points when NVRA trades at $148.50.

        Step-by-step arithmetic:
        1. Total modeled price move:
           $$250 \times 0.0001 = 0.0250 = +2.50\%$$
        2. Expected dollar price impact on $148.50:
           $$\$148.50 \times 0.0250 = \$3.7125 \implies \$3.71$$
        3. Immediate impact on the dated bar (58%):
           $$\$3.7125 \times 0.58 = \$2.153 \implies \$2.15$$
        4. Post-announcement drift across subsequent bars (42%):
           $$\$3.7125 \times 0.42 = \$1.559 \implies \$1.56$$
        Because 250 points falls between 120 and 400, the item is tagged with impact tier `M` (Medium).

        Now calculate session tone across three released items: a high positive headline ($w = 3, d = +1$), a medium negative headline ($w = 2, d = -1$), and a low positive headline ($w = 1, d = +1$):
        $$\text{Signed Weight} = (3 \times 1) + (2 \times -1) + (1 \times 1) = 3 - 2 + 1 = +2$$
        $$\text{Total Weight} = 3 + 2 + 1 = 6$$
        $$\text{Tone} = \frac{+2}{6} = +0.33 \quad (+33\%)$$
        If 10 routine chatter items are published during the same session, the tone remains exactly $+0.33$ because chatter carries zero weight ($w = 0$).
        """,
        """
        **Open the Newsroom panel.** Click **News** in the right sidebar (or enter `NVRA N` in the Command dialog). The panel header displays **Newsroom** with a **SIMULATED** badge. Toggle **News scope** between **All markets** and the active ticker (NVRA).

        **Inspect headline metadata.** Each item displays a publication timestamp, a scope badge (`CO`, `SEC`, `ECO`, `MKT`), the associated ticker, an impact letter (`H`, `M`, `L`, or `·`), the headline text, and an explicit score (e.g. "+250 pts"). Hover over any score badge to view the formula breakdown.

        **Interpret sentiment gauges.** Examine the **Session** gauge (last 390 bars) and **5 sessions** gauge (last 1,950 bars). Below the gauges, note the summary line: "N items this session · P positive · Q negative · R neutral · market tone X%".

        **Use the live headline ticker.** Above the chart canvas, the **SIM NEWS** ticker displays the 12 most recent headlines. Clicking any item automatically selects that stock and switches the chart to it.

        **Inspect chart markers.** On the price chart, scored news items appear as circular badges showing their net point impact (e.g. "+250"). If multiple news items land in the same bar, the badge displays their net sum with the item count in parentheses, such as "+120 (2)". Click the newspaper icon on the replay bar to toggle these markers on or off.

        **Trace price reactions.** Step forward with **Next replay bar** until a fresh scored headline arrives. Compare the immediate candle move against the 58% modeled shock, keeping in mind that background market noise and sector factors also influence the bar.
        """,
        """
        Try the mission [Trade what the tape actually said](/simulator?mission=read-the-tape). The link only preselects it: open the terminal, click the **New simulation run** icon, verify that **Practice mission (optional)** displays "Trade what the tape actually said · VLOC", and click **Create new paper account**. Open the collapsed **Practice mission** panel beneath the toolbar to review your three objectives: enter your initial VLOC position within one session following a headline of 150 points or greater, record a trade thesis citing the headline, and keep position size under 10% of opening equity ($10,000). The mission assesses your analytical process and execution discipline, never your final profit.
        """,
        r"\frac{\Delta P}{P}=\frac{\text{points}}{10\,000},\qquad \text{tone}=\frac{\sum_{i} w_{i}\,d_{i}}{\sum_{i} w_{i}}",
        '''
points = 250
price = 148.50
move = points / 10000
total = price * move
print("Modelled move:", move)
print("Total move in dollars:", round(total, 2))
print("On the dated bar:", round(total * 0.58, 2))
print("Drifting afterwards:", round(total * (1 - 0.58), 2))

weights = [3, 2, 1]
directions = [1, -1, 1]
signed = 0
for i in range(len(weights)):
    signed = signed + weights[i] * directions[i]
total_weight = sum(weights)
print("Signed weight:", signed)
print("Total weight:", total_weight)
print("Tone:", round(signed / total_weight, 2))
''',
        "Pick one scored headline from the News tab of a run you have advanced for a few sessions. Write its scope tag, impact letter and points, then compute its modelled percentage move and the share that lands on the dated bar. Find its circle on the chart, note the actual move of that bar, and write two reasons the bar might have moved by a different amount.",
        "For an illustrative +180 point company headline tagged M, the modeled total move is 180 / 10,000 = 1.80%, with 58% (approximately 1.04%) landing on the dated bar and 42% drifting over subsequent candles. If the actual bar moved only 0.4%, random market noise or an offsetting negative macroeconomic release during the same minute may have dampened the reaction. If the bar moved 2.5%, positive sector sentiment or technical momentum may have amplified the shock. Scored headlines provide structural context, not deterministic predictions.",
        [
            (
                "A headline for one company is scored +300 points. What modelled price move does that represent?",
                "+3.00%, because one point is one basis point",
                "+0.30%, because 300 points is three tenths of one percent",
                "+30%, because 300 points is three tenths of the price",
                "One basis point is 0.01%, so 300 points is 300 × 0.01% = 3.00%.",
            ),
            (
                "A +250 point item is dated 10:00 for a company priced at 100. About how much of the modelled move lands on the 10:00 bar itself?",
                "About 58% of the 2.50% move, roughly $1.45",
                "All of it, $2.50",
                "None of it, because the whole move drifts over later bars",
                "The score models 2.50% in total. 58% lands on the dated bar and the other 42% drifts afterwards, so the bar gets 0.58 × $2.50 ≈ $1.45.",
            ),
            (
                "Two scored items are released, a high negative one and a low positive one, together with ten routine chatter items. What is the tone?",
                "−0.50, because (−3 + 1) ÷ (3 + 1) and chatter has weight zero",
                "−0.14, because each chatter item adds a weight of 1 to the total",
                "−2.00, because the signed weights add to −2",
                "Tone divides the signed weight by the total weight of scored items. Chatter has weight zero, so (−3 + 1) ÷ (3 + 1) = −0.50.",
            ),
            (
                "A learner buys right after a +400 point headline and the stock falls over the next hour. What does this show about the score?",
                "Nothing conclusive, because noise and other items also move prices and one trade is a tiny sample",
                "That the score is wrong, because the price must follow it on every bar",
                "That the item was chatter, because only chatter fails to move the price",
                "A score models one item's contribution. Noise, sector and macro items and drift also act on the price, and a single outcome cannot judge a model or a decision.",
            ),
        ],
        [HOT_STOCK, RUMORS],
        (8, 14, 8),
    )

    # ---------------------------------------------------------------- Unit 2
    add(
        "Market and limit orders: preview, reservations and the next bar",
        "Place, preview, amend and cancel a market order and a limit order, and explain why neither can fill until the next bar.",
        r"""
        In electronic trading, an order is an instruction submitted to an exchange, not an executed transaction. In the Quanta simulator, an order transitions through four distinct operational states:
        1. Drafted: Parameters (order type, shares, limit price) are configured on the ticket.
        2. Previewed: The simulator verifies risk checks, estimating required cash and fees; no funds are committed yet.
        3. Accepted: The order is validated by the gateway. Cash is reserved in your account, but you own no shares yet.
        4. Filled: The matching engine executes the order on a subsequent bar.

        The Next-Bar Execution Invariant:
        $$R = Q \cdot P_{\text{reserve}} + c,\qquad P_{\text{reserve}} = \begin{cases} \lceil P_{\text{last}}(1 + f)\rceil_{0.01} & \text{market buy} \\ L & \text{buy limit} \end{cases}$$
        An order placed while looking at bar $c$ is first evaluated by the matching engine on bar $c + 1$ using that bar's Open, High, Low, and Volume. Accepting an order never alters your share holdings on the current bar.

        Cash Reservation Protection:
        When a buy order is accepted, the system immediately places a hold on your cash equal to the estimated purchase cost plus commission. This pre-trade control prevents double-spending your available capital across multiple pending tickets.

        Market vs Limit Execution Mechanics:
        • Market Order: Guarantees execution speed over price certainty. It fills at the next bar's Open, with slippage and half the spread added against you.
        • Limit Order: Sets an absolute ceiling on the price you will pay (or floor on what you will accept). A buy limit fills at the Open if the Open is already at or below your limit. Otherwise, it fills only if the market trades strictly through your limit price ($Low < Limit$). A mere price touch ($Low = Limit$) will not fill because the simulator does not assume your order was first in the queue.
        """,
        r"""
        Suppose the last closed bar printed at $148.50, and you preview a market buy for 10 shares under default cost settings ($c = $1.00, $f = 0.0003$).

        1. Cash Reservation Calculation:
           The ticket estimates the maximum debit using the last close plus friction, rounded up to the cent:
           $$P_{\text{reserve}} = \lceil 148.50 \times 1.0003 \rceil_{0.01} = \lceil 148.54455 \rceil = \$148.55$$
           $$\text{Estimated Debit} = 10 \times \$148.55 + \$1.00 = \$1{,}485.50 + \$1.00 = \$1{,}486.50$$
           Upon clicking **Place buy order**, Reserved cash displays $1,486.50, and Available cash falls to $100,000 - $1,486.50 = $98,513.50. You own zero shares.

        2. Next-Bar Fill Execution:
           Suppose the next bar opens higher at $148.62. The market order executes at that open plus friction:
           $$P_{\text{fill}} = \operatorname{round}(148.62 \times 1.0003) = \operatorname{round}(148.6645) = \$148.66$$
           Total settled cost: 10 × $148.66 + $1.00 = $1,487.60.
           The $1,486.50 reservation is released, and your settled cash balance becomes:
           $$\$100{,}000 - \$1{,}487.60 = \$98{,}512.40$$
           Average cost per share recorded in your portfolio is $1,487.60 / 10 = $148.76 (including commission).

        3. Limit Order Comparison:
           Now place a buy limit order for 10 shares at $148.20. Reserved cash is 10 × $148.20 + $1.00 = $1,483.00.
           • Scenario A (Strict Penetration): Next bar opens at $148.45 and prints a low of $148.10. Because the price traded strictly below your limit ($148.10 < 148.20$), the order fills at your limit price of $148.20.
           • Scenario B (Touch Only): Next bar prints a low of exactly $148.20. The limit was touched but not penetrated. The order does not fill and remains active.
           • Scenario C (Gap Down Open): Next bar opens at $148.10. The order fills at the open plus friction: 148.10 × 1.0003 = $148.14 (saving you money below your $148.20 limit).
        """,
        """
        **Open an order ticket.** Click **Trade** in the right sidebar (or enter `NVRA BUY` in the Command dialog). The ticket interface provides **Buy** and **Sell** toggles, **Order type** (Market default), **Shares** (default 10), and **Duration** (GTC - Good 'Til Canceled).

        **Document your trade thesis.** Expand the **Trade thesis & lesson** drawer. In **Trade thesis**, write one clear sentence answering: "Why are you placing this trade, and what market observation would prove your thesis wrong?"

        **Generate preview.** Click **Preview buy order**. Generating a preview automatically pauses continuous replay. The modal displays Estimated notional, Estimated debit, Available cash, Reserved cash, and Projected position size.

        **Submit order.** Click **Place buy order**. The bottom panel switches to **Open orders**, and a confirmation appears: "Order accepted. Advance replay to observe its fill." Check that **Reserved cash** reflects the estimated hold while **Positions** remains empty.

        **Advance clock to observe fill.** Click **Next replay bar**. The order executes at the new bar's open price plus friction. Open **Trade history** to inspect the settled Fill price, execution Fee ($1.00), and timestamp. On the chart, notice the fill marker (e.g. "BUY 10 @ 148.66") and the position line showing your volume-weighted average cost.

        **Place and manage a limit order.** Switch **Order type** to **Limit**. Type a limit price below current market and place the order. In **Open orders**, notice the options to **Edit** (modify price), **Cancel**, or **Journal**. On the chart, a draggable horizontal limit line appears. Dragging the line opens **Confirm order amendment**.

        **Select order duration.** Review **DAY** (expires automatically at the final 3:59 PM bar of the session) versus **GTC** (remains active across sessions until filled or manually canceled).
        """,
        """
        Try the mission [Place your first paper order](/simulator?mission=first-order). The link only preselects it: open the terminal, click the **New simulation run** icon, verify that **Practice mission (optional)** shows "Place your first paper order · NVRA", and click **Create new paper account**. Establish the maximum price you are willing to pay, place a buy limit order at that price, and document your thesis in the mission journal. Then advance the clock by one full session with the **1D** jump. The three objectives verify that you submitted a limit order, recorded a thesis, and completed a session.
        """,
        r"R=q\,P_{\text{res}}+c,\qquad P_{\text{res}}=\begin{cases}\lceil P_{\text{last}}(1+f)\rceil_{0.01} & \text{market buy}\\ L & \text{buy limit}\end{cases}",
        '''
from math import ceil, floor

def to_cent(x):
    return floor(x * 100 + 0.5) / 100

def limit_buy_fill(open_price, low, limit, friction):
    if open_price <= limit:
        return min(to_cent(open_price * (1 + friction)), limit)
    if low < limit:
        return limit
    return 0

friction = (2 + 2 / 2) / 10000
shares = 10
commission = 1
last_close = 148.50

reserve_price = ceil(last_close * (1 + friction) * 100) / 100
reserved = round(shares * reserve_price + commission, 2)
print("Reserve price per share:", reserve_price)
print("Estimated debit and reserved cash:", reserved)
print("Available cash after placing:", round(100000 - reserved, 2))

next_open = 148.62
fill = to_cent(next_open * (1 + friction))
paid = round(shares * fill + commission, 2)
print("Fill price:", fill)
print("Cash after the fill:", round(100000 - paid, 2))
print("Average cost per share:", round(paid / shares, 2))

limit = 148.20
print("Cash reserved by the limit order:", round(limit * shares + commission, 2))
print("Bar trades through the limit:", limit_buy_fill(148.45, 148.10, limit, friction))
print("Bar only touches the limit (0 means no fill):", limit_buy_fill(148.45, 148.20, limit, friction))
print("Bar opens below the limit:", limit_buy_fill(148.10, 148.00, limit, friction))
''',
        "The last close is 96.40 and the costs are the defaults. Compute the reserve price and the reserved cash for a 20-share market buy and for a 20-share buy limit at 95.90. Then say what happens to each if the next bar opens at 96.55 and its low is 96.30.",
        "The market buy reserves a share price of ceil(96.40 × 1.0003) = 96.43, reserving 20 × 96.43 + $1.00 = $1,929.60. The buy limit order reserves 20 × $95.90 + $1.00 = $1,919.00. If the next bar opens at 96.55, the market order fills at 96.55 × 1.0003 = $96.58, costing 20 × $96.58 + $1.00 = $1,932.60 ($3.00 above the initial reserve). The limit order does not fill: the opening price of 96.55 is above 95.90, and the bar's low of 96.30 never traded through the 95.90 limit price. The limit order remains active in Open orders with its $1,919.00 reservation intact.",
        [
            (
                "A learner places a market buy after bar 120 has closed. When is the order first tested for a fill?",
                "On bar 121, the next bar",
                "Immediately, at bar 120's closing price",
                "At the end of the session",
                "An order placed after bar c is first tested on bar c + 1. Accepting an order never changes holdings.",
            ),
            (
                "A buy limit order at 148.20 meets a bar that opens at 148.45 and has a low of exactly 148.20. What happens?",
                "It does not fill, because a touch is not enough and the price must trade strictly below the limit",
                "It fills at 148.20, because the low reached the limit",
                "It fills at the open, 148.45, plus slippage",
                "This simulator never assumes your order was first in a queue, so the price must trade strictly through a limit before it fills. An open at or better than the limit is the other way to fill.",
            ),
            (
                "A learner previews a market buy and the ticket shows an Estimated debit. After Place buy order, what is true?",
                "That estimate is reserved as cash, and nothing is owned until a later bar fills the order",
                "Reserved cash stays at zero until the order fills, because it is not final",
                "The shares are owned immediately and the cash is spent",
                "Acceptance reserves the estimated cost and commission so the cash cannot be committed twice. Ownership changes only when a later bar fills the order.",
            ),
            (
                "The notice 'Unconfirmed action saved; recover it before placing another trade.' appears after Place buy order. What should the learner do?",
                "Click Reconnect & retry action so the saved request is resent once",
                "Place the order again at once in case the first was lost",
                "Start a new simulation run to clear the notice",
                "The terminal cannot tell whether the order arrived. Reloading the account and resending the same request keeps the order unique, while placing it again could double it.",
            ),
        ],
        [ORDER_TYPES, ORDER_BULLETIN, DECIMAL],
        (7, 15, 8),
    )

    add(
        "How fills are priced: slippage, spread, participation and partial fills",
        "Compute a fill from a bar's open and volume, and explain slippage, half the spread, the participation cap, first-in-first-out sharing and partial fills.",
        r"""
        In real financial markets, trading volume is a scarce, finite resource. You cannot purchase 50,000 shares in a single minute without drastically moving the market price against yourself. The Quanta simulator models this liquidity constraint through the Volume Participation cap ($\pi$):
        $$\text{Capacity}_t = \lfloor V_t \cdot \pi \rfloor,\qquad P_t = \operatorname{round}\big(O_t \cdot (1 \pm f)\big)$$
        Here $V_t$ is the total volume printed on bar $t$, and $\pi$ is your configured participation rate (0.01 or 1% by default). The maximum number of shares your orders can execute on that bar is strictly capped at $\lfloor V_t \times \pi \rfloor$.

        Partial Fills and Queue Allocation:
        If your order quantity exceeds a bar's execution capacity, the order is partially filled:
        $$\text{Fill}_t = \min\big(\text{Remaining Shares},\; \text{Capacity}_t\big)$$
        The remaining unfilled shares stay open in the matching engine, executing across subsequent bars as fresh volume arrives. If you have placed multiple working orders in the same ticker, the available capacity is shared strictly in First-In, First-Out (FIFO) arrival order. The order submitted first consumes capacity until fully satisfied before the second order receives a single share.

        Commission Handling on Partial Fills:
        The $1.00 broker commission is charged only once—on the order's initial partial fill. Subsequent fills for the same order carry zero additional commission, ensuring that liquidity fragmentation does not unfairly penalize execution.
        """,
        r"""
        Suppose you place a 600-share market buy order for NVRA with default cost settings ($c = $1.00, $f = 0.0003, \pi = 0.01$). Over the next three minutes, market bars print with the following opens and volumes:
        • Bar 1: Open = $148.50, Volume = 26,000 shares.
        • Bar 2: Open = $148.60, Volume = 18,000 shares.
        • Bar 3: Open = $148.55, Volume = 22,000 shares.

        Step-by-step multi-bar execution:
        1. Bar 1 Execution:
           Capacity is $\lfloor 26{,}000 \times 0.01 \rfloor = 260$ shares.
           Fill price: 148.50 × 1.0003 = $148.54.
           Shares filled: 260. Unfilled remainder: $600 - 260 = 340$ shares.
           Subtotal: 260 × $148.54 = $38,620.40 plus $1.00 commission.

        2. Bar 2 Execution:
           Capacity is $\lfloor 18{,}000 \times 0.01 \rfloor = 180$ shares.
           Fill price: 148.60 × 1.0003 = $148.64.
           Shares filled: 180. Unfilled remainder: $340 - 180 = 160$ shares.
           Subtotal: 180 × $148.64 = $26,755.20 (zero additional commission).

        3. Bar 3 Execution:
           Capacity is $\lfloor 22{,}000 \times 0.01 \rfloor = 220$ shares.
           Only 160 shares remain unfilled, so the order takes 160 shares.
           Fill price: 148.55 × 1.0003 = $148.59.
           Shares filled: 160. Unfilled remainder: $160 - 160 = 0$ (Order Complete).
           Subtotal: 160 × $148.59 = $23,774.40.

        Consolidated Order Outcome:
        $$\text{Total Shares} = 260 + 180 + 160 = 600 \text{ shares}$$
        $$\text{Total Notional} = \$38{,}620.40 + \$26{,}755.20 + \$23{,}774.40 = \$89{,}150.00$$
        $$\text{Volume-Weighted Average Price} = \frac{\$89{,}150.00}{600} = \$148.5833 \implies \$148.58$$
        $$\text{Total Cash Settled} = \$89{,}150.00 + \$1.00\text{ (single fee)} = \$89{,}151.00$$
        """,
        """
        **Demonstrate volume constraints.** Click **New simulation run**. Set **Volume participation (0–1)** to its minimum setting of 0.001 (0.10% of bar volume). Leave other parameters at defaults and create the run.

        **Inspect bar volume.** Hover over the latest candle in NVRA. Note the volume figure in the chart header: if volume is 26,000 shares, at a 0.001 participation rate the per-bar capacity is $\\lfloor 26{,}000 \\times 0.001 \\rfloor = 26$ shares.

        **Submit an oversized order.** Open the **Trade** ticket for NVRA. Enter 100 shares at Market, record a trade thesis, preview, and place the order.

        **Observe step-by-step partial fills.** Click **Next replay bar**. Open the **Open orders** tab: the status badge reads "partially filled", showing 26 of 100 shares filled and 74 shares remaining. Advance again: the next bar executes another partial tranche. Notice how **Reserved cash** decreases proportionately as shares execute.

        **Audit trade history blotter.** Open **Trade history**. Notice that each partial execution is recorded as an independent row with its own bar timestamp and fill price. Only the very first fill row carries the $1.00 commission fee; all subsequent tranches display $0.00 fee.

        **Test FIFO queue priority.** Submit two distinct buy orders in the same stock (Order 1 for 100 shares, Order 2 for 20 shares) before stepping the clock. Advance one bar: Order 1 consumes all available capacity, while Order 2 shows 0 shares filled until Order 1 is completely satisfied.

        **Cancel working remainder.** Click **Cancel** on a partially filled order. The notice confirms "Order remainder canceled." The unfilled portion is canceled and its cash reservation released, while already executed shares remain securely in **Positions**.
        """,
        """
        Create a new run with default participation of 0.01 (1%) and place the same 100-share buy order. Notice that whenever a bar prints at least 10,000 shares of volume, the entire 100-share order executes in a single candle. In your notebook, document how volume participation protects backtests from assuming unrealistic fill liquidity.
        """,
        r"\text{fill}_{t}=\min\big(\text{remaining}_{t},\ \lfloor V_{t}\,\pi\rfloor-\text{used}_{t}\big),\qquad P_{t}=\operatorname{round}\big(O_{t}\,(1\pm f)\big)",
        '''
from math import floor

def to_cent(x):
    return floor(x * 100 + 0.5) / 100

friction = (2 + 2 / 2) / 10000
opens = [148.50, 148.60, 148.55]
volumes = [26000, 18000, 22000]
remaining = 600
notional = 0
commission = 1
for i in range(3):
    capacity = volumes[i] // 100
    fill = min(remaining, capacity)
    price = to_cent(opens[i] * (1 + friction))
    notional = notional + fill * price
    remaining = remaining - fill
    print("Bar", i + 1, "capacity", capacity, "fill", fill, "price", price, "remaining", remaining)
print("Shares bought:", 600 - remaining)
print("Notional:", round(notional, 2))
print("Average price:", round(notional / 600, 2))
print("Total cash paid including one commission:", round(notional + commission, 2))
''',
        "Explain how the simulator prices an order across multiple bars when volume is constrained. State the capacity formula, how partial fills are recorded in Trade history, how commissions are assessed, and what happens to a second order queuing in the same symbol.",
        "When an order exceeds the participation cap (capacity = floor(volume × participation)), it partially fills across successive bars. In Trade history, each partial fill is recorded as a separate row with its own execution price (bar open plus friction). The $1.00 commission is billed only once on the first fill. Additional working orders in the same ticker queue in FIFO order, receiving zero capacity until the preceding order is fully filled or canceled.",
        [
            (
                "Why does an order for 600 shares take several bars to fill when volume is low?",
                "The volume participation cap limits each bar's fill to a percentage of that bar's volume",
                "The simulator pauses between fills to check your buying power",
                "Large orders are split into arbitrary 100-share lots by default",
                "The participation setting restricts how much of any single bar's volume your orders can consume, creating realistic partial fills.",
            ),
            (
                "A bar has a volume of 26,000 shares and participation is 0.01. What is its capacity?",
                "260 shares",
                "26 shares",
                "2,600 shares",
                "Capacity is the integer part of volume multiplied by participation: 26,000 × 0.01 = 260 shares.",
            ),
            (
                "When is the commission charged on an order that fills over several bars?",
                "Once, on the order's first partial fill",
                "On every partial fill separately",
                "At the end of the session, as a lump sum",
                "The broker commission is charged exactly once per order ticket upon the initial fill; subsequent partial tranches incur zero commission.",
            ),
            (
                "Why is raising participation to 1.0 an unrealistic test of a strategy?",
                "It assumes you could buy 100% of an exchange's volume without moving the price",
                "It causes the simulator to crash on large orders",
                "It prevents limit orders from working",
                "Participation is a limit on how much of a bar your orders can take. Raising it to the maximum removes a realistic constraint and flatters results.",
            ),
        ],
        [EXECUTING, BID_ASK, ORDER_BULLETIN],
        (7, 15, 8),
    )

    add(
        "Stops, trailing stops and attached exits",
        "Place stop, stop-limit, trailing-stop and attached-exit orders, and predict how each behaves when a price gaps.",
        r"""
        A stop order is a conditional trigger, not a price guarantee. When you place a sell stop order at $145.00, you are instructing the broker: "If the market trades at or below $145.00, immediately convert my order into a market order to sell." If a stock closes at $146.00 and gaps down overnight to open at $142.00, your stop triggers at the open and executes at $142.00 minus friction! A stop order controls when an exit is attempted, not the price you receive.

        Three advanced exit types provide structured risk management:
        1. Stop-Limit: Specifies two prices—a Stop trigger price and a Limit execution price. Once triggered, it converts into a limit order. If the market gaps below your limit price, the order will refuse to sell, leaving you holding plunging shares.
        2. Trailing Stop: Designed for dynamic profit preservation on long positions. It anchors to the highest price achieved after order placement and trails at a fixed percentage ($\tau$) below that peak:
        $$P_{\text{fill}} = \operatorname{round}\big(\min(O_t, S) \cdot (1 - f)\big),\qquad S_{t+1} = (1 - \tau) \cdot \max(A_t, H_t)$$
        As new highs print, the stop ratchets upward; it never moves downward.
        3. Attached Bracket Exits (OCO): You can attach a Take-Profit limit and a Stop-Loss directly to an entry order. They operate as One-Cancels-Other (OCO): when one leg executes, the other is automatically cancelled. If a single high-volatility bar spans both target and stop levels, the simulator conservatively triggers the stop first.
        """,
        r"""
        Let us work through exact price arithmetic under normal execution, overnight gaps, and trailing stops:

        Case 1: Standard Sell Stop Execution
        You hold 10 shares and place a sell stop at $145.00 ($f = 0.0003$). The next bar opens at $146.10 and trades down to an intraday low of $144.80. The low penetrates your $145.00 stop.
        Fill price: Lower of open and stop, less friction:
        $$145.00 \times (1 - 0.0003) = 145.00 \times 0.9997 = 144.9565 \implies \$144.96$$

        Case 2: Overnight Gap Through Stop
        Bad news breaks overnight, and the stock gaps down to open at $142.00. The stop triggers immediately at the open.
        Fill price: Lower of open and stop ($142.00 < 145.00$), less friction:
        $$142.00 \times 0.9997 = 141.9574 \implies 141.96$$
        You receive $141.96 per share—$3.04 below your stop price ($30.40 total slippage on 10 shares). This demonstrates why stops do not prevent gap slippage.

        Case 3: Trailing Stop Ratchet
        You place a 5% trailing stop ($\tau = 0.05$) when NVRA closes at $150.00. The initial stop sits at 150.00 × 0.95 = $142.50.
        On the next candle, the stock rallies to an intraday high of $153.00 (low $149.00). The stop does not trigger, and the anchor ratchets to the new high:
        $$\text{New Stop Level} = 153.00 \times (1 - 0.05) = 145.35$$
        When the subsequent candle opens at $146.00 and dips to $144.90, it penetrates $145.35, executing at 145.35 × 0.9997 = $145.31.
        """,
        """
        **Protect existing shares.** Buy 10 shares of any company and step one bar forward to ensure execution. Open the **Trade** tab, select **Sell**, choose **Stop** in **Order type**, type a stop price below current market in **Stop price**, keep Duration at GTC, and document your reason in **Trade thesis**.

        **Preview and place.** Click **Preview sell order** and **Place sell order**. The pending stop order draws an interactive stop line on the chart canvas. You can click and drag this line to adjust your stop level; releasing the line opens **Confirm order amendment**.

        **Compare stop-limit behavior.** Place a second sell order using **Stop-limit**, filling in both **Stop price** (trigger level) and **Limit price** (minimum acceptable fill). Note that if a price gaps below the limit, the order remains working and leaves you holding shares.

        **Deploy a trailing stop.** Select **Trailing stop** on a Sell ticket. Enter a trailing percentage (e.g. 5%) in **Trail (% below the high)**. Advance several bars using **Next replay bar** and observe the stop line ratcheting upward on the chart as new price peaks develop.

        **Configure attached bracket exits.** On a **Buy** ticket, check the box **Attach exits to this entry**. Enter target prices in **Take profit** and **Stop loss** (or select **Or trail the stop (%)**). The ticket displays your reward-to-risk ratio (e.g. "Risking $50 to make $150 · 3:1 R"). Attached legs activate automatically upon entry fill.
        """,
        """
        Try the mission [Protect a position before you need to](/simulator?mission=stop-discipline). No other lesson links it, so start it here: open the terminal, click the **New simulation run** icon, verify that **Practice mission (optional)** shows "Protect a position before you need to · QBIT", and click **Create new paper account**. Select QBIT using the Command dialog, enter an initial long position, and immediately attach a protective sell stop while market conditions are calm. Document your reasoning in every order journal.
        """,
        r"P_{\text{fill}}=\operatorname{round}\big(\min(O_t,S)\,(1-f)\big),\qquad S_{t+1}=(1-\tau)\,\max(A_t,H_t)",
        '''
from math import floor

def to_cent(x):
    return floor(x * 100 + 0.5) / 100

friction = (2 + 2 / 2) / 10000
stop = 145.00
for bar_open in [146.10, 142.00]:
    fill = to_cent(min(bar_open, stop) * (1 - friction))
    print("Open", bar_open, "-> stop fill", fill, "gap below stop", round(stop - fill, 2))

trail = 0.05
anchor = 150.00
trailing_stop = anchor * (1 - trail)
print("Trailing stop placed at", round(trailing_stop, 2))
anchor = max(anchor, 153.00)
trailing_stop = anchor * (1 - trail)
print("After a 153.00 high the stop is", round(trailing_stop, 2))
print("Fill when the next bar dips through it:", to_cent(trailing_stop * (1 - friction)))

entry = 148.54
risk = (entry - 144.00) * 10
reward = (156.00 - entry) * 10
print("Bracket risk:", round(risk, 2), "reward:", round(reward, 2), "R:", round(reward / risk, 2))
''',
        "You hold 20 shares bought at 97.40 and place a sell stop at 95.00 with default costs. Work out the fill if the next bar opens at 96.20 and trades to 94.80, and again if it opens at 93.50. Then say what a stop-limit at 95.00 / 94.90 would have done in the second case.",
        "In the first scenario, the bar opens at 96.20 and trades down through 95.00. The fill price is min(96.20, 95.00) × 0.9997 = 95.00 × 0.9997 = 94.97, yielding a loss of 20 × ($97.40 - $94.97) = $48.60 before commissions. In the second scenario, the market gaps down to open at 93.50. The stop triggers and fills at min(93.50, 95.00) × 0.9997 = 93.50 × 0.9997 = 93.47, resulting in a loss of 20 × ($97.40 - $93.47) = $78.60. A stop-limit at 95.00 / 94.90 would trigger on the gap bar but would refuse to execute below 94.90, leaving all 20 shares unsold.",
        [
            (
                "A sell stop at 145.00 is triggered by a bar that opens at 142.00. Before costs, at what price does it fill?",
                "142.00, the open, because a gap through the stop fills at the worse price",
                "145.00, the stop price, which is guaranteed once triggered",
                "Nothing fills, because the open is already below the stop",
                "A triggered stop fills at the lower of the bar's open and the stop for a sell. A gap below the stop therefore fills at the open, which is worse than the stop.",
            ),
            (
                "Which order can trigger and still not fill at all?",
                "A stop-limit, because after triggering it can only fill on a later bar within its limit",
                "A sell stop, because stops never fill when the price gaps",
                "A market order, because it waits for a better price",
                "A stop-limit converts into a limit order. If later bars never trade at the limit or better, the triggered order stays unfilled.",
            ),
            (
                "A 5% trailing stop is placed when the close is 150.00. The next bar's high is 153.00 and its low 149.00. Which stop does the following bar use?",
                "145.35, because the anchor rises to the 153.00 high after the bar is tested",
                "142.50, because a trailing stop's anchor never moves",
                "141.55, because the stop follows the bar's low",
                "Each bar is tested against the stop it opened with, then the anchor ratchets to the new high: 153.00 × 0.95 = 145.35.",
            ),
            (
                "An entry's take-profit and stop-loss are both inside one bar's range. Which does the terminal take?",
                "The stop-loss, because it cannot see the order of prices inside the bar and takes the less flattering reading",
                "The take-profit, because it is the better outcome for the account",
                "Both, so the position is sold twice",
                "Exits are one-cancels-other, and when one bar covers both the conservative rule takes the stop first.",
            ),
        ],
        [STOP_BULLETIN, STOP_GLOSSARY, ORDER_BULLETIN],
        (8, 14, 8),
    )

    add(
        "Margin accounts and short selling",
        "Open a margin run, sell short, and compute buying power, the borrow fee and the price at which a short is bought in.",
        r"""
        A margin account allows you to borrow capital and securities from a broker. In particular, it enables short selling: borrowing shares you do not own, selling them immediately at the prevailing market price, and committing to buy them back (cover) at a later date. If the stock falls, you buy back at a lower price and pocket the difference. However, if the stock surges, your potential loss is theoretically unlimited because a share price has no upper ceiling.

        Three key financial metrics govern a margin account:
        $$\text{Buying Power} = \max(0, 2E - G),\qquad P_{\text{buy-in}} = \frac{C}{Q_{\text{short}} \cdot 1.30}$$
        1. Equity ($E$): Cash balance minus the market value of all borrowed short shares ($E = \text{Cash} - G$).
        2. Gross Exposure ($G$): The total current market value of all open long and short positions.
        3. Buying Power ($\text{BP}$): Twice equity minus gross exposure, representing your maximum additional purchasing leverage.

        Borrow Fees and Forced Buy-Ins:
        Borrowed shares are not free. The simulator assesses an annualized borrow fee of 5%, calculated daily per trading session ($5\% / 252$ sessions) and billed directly to your account history ledger. Under regulatory maintenance margin rules, if account equity falls below 30% of gross exposure ($E < 0.30 \cdot G$), a margin call occurs, and the matching engine executes an automated buy-in order to liquidate the short position.
        """,
        r"""
        Suppose you initialize a margin account with $100,000 cash and execute a short sale of 600 shares at $150.00 per share (ignoring transaction fees for clarity).

        Step-by-step balance sheet accounting:
        1. Initial Short Execution:
           The short sale generates 600 × $150.00 = $90,000 in proceeds.
           Cash balance rises to: $100,000 + $90,000 = $190,000.
           You owe the broker 600 shares, representing a liability of 600 × $150 = $90,000.
           $$\text{Gross Exposure } G = \$90{,}000$$
           $$\text{Equity } E = \text{Cash} - G = \$190{,}000 - \$90{,}000 = \$100{,}000$$
           $$\text{Buying Power } \text{BP} = 2 \times \$100{,}000 - \$90{,}000 = \$200{,}000 - \$90{,}000 = \$110{,}000$$

        2. Stock Price Rallies to $200.00:
           The 600 borrowed shares are now worth 600 × $200 = $120,000.
           $$\text{Gross Exposure } G = \$120{,}000$$
           $$\text{Equity } E = \$190{,}000 - \$120{,}000 = \$70{,}000$$
           $$\text{Buying Power } \text{BP} = 2 \times \$70{,}000 - \$120{,}000 = \$140{,}000 - \$120{,}000 = \$20{,}000$$

        3. Calculating the Forced Buy-In Price ($P$):
           A forced buy-in triggers when equity falls below 30% of gross exposure:
           $$190{,}000 - 600P < 0.30 \times (600P) \implies 190{,}000 - 600P < 180P$$
           $$780P > 190{,}000 \implies P > \frac{190{,}000}{780} \approx 243.59$$
           If the stock rises to $243.59 (a 62.4% rally from $150.00), the broker triggers an automated market buy order to cover the position and prevent account insolvency.

        4. Borrow Fee Calculation:
           At $150.00, one session's borrow fee is $90,000 × 0.05 / 252 ≈ $17.86. Over a 5-day week, holding the short costs about $89.29 in financing fees.
        """,
        """
        **Create a margin simulation run.** Click **New simulation run**. In **Account type**, select "Margin · may sell short". Leave **Practice mission** on free practice and click **Create new paper account**. Notice that the account status bar now displays **MARGIN**, **Buying power**, and **Gross exposure** alongside **Equity** and **Cash**.

        **Execute a short sale.** Select a company you do not own. Open the **Trade** tab and click **Sell**. Enter 10 shares, keep Order type at Market, and write a bearish rationale in **Trade thesis**. Note that the preview displays **Buying power** consumption rather than available cash. Click **Place sell order** and advance one bar.

        **Audit margin balances.** After fill, confirm that **Cash** increased by the sale proceeds minus commission, and that **Gross** displays the liability value of the borrowed shares.

        **Observe daily borrow fees.** Use the **1D** jump button to advance through an entire session. Open the **Account history** ledger tab and locate the line item "Stock borrow fee on short positions".

        **Cover the short position.** In the **Positions** tab, click **Close** on your short position row. The ticket automatically pre-populates a **Buy** order for the exact quantity owed. Preview and submit the order, then step forward one bar to complete execution.
        """,
        """
        In a free margin run, short 100 shares of a stable company and track the position across five sessions. Record your buying power before and after, compute your theoretical buy-in liquidation price using the formula, and verify that the accrued borrow fees match your calculations.
        """,
        r"\text{BP}=\max\big(0,\;2E-G\big),\qquad \text{buy-in when } E<0.3\,G",
        '''
cash = 100000 + 600 * 150.00
shares_owed = 600
for price in [150.00, 200.00]:
    gross = shares_owed * price
    equity = cash - gross
    buying_power = max(0, 2 * equity - gross)
    print("Price", price, "equity", equity, "gross", gross, "buying power", buying_power)

buy_in_price = cash / (shares_owed * 1.3)
print("Buy-in once the price exceeds:", round(buy_in_price, 2))
fee_per_session = shares_owed * 150.00 * 0.05 / 252
print("Borrow fee per session at 150:", round(fee_per_session, 2))
print("Borrow fee over five sessions:", round(fee_per_session * 5, 2))
''',
        "A margin account with $50,000 shorts 200 shares at 120.00, ignoring fees. Compute equity, gross exposure and buying power at 120.00 and at 150.00, the price at which a buy-in begins, and one session's borrow fee at 120.00.",
        "Short proceeds add $24,000 to cash, bringing total cash to $74,000. At $120.00, gross exposure is $24,000, equity is $74,000 - $24,000 = $50,000, and buying power is 2 × $50,000 - $24,000 = $76,000. At $150.00, the shares owed are worth $30,000, reducing equity to $44,000, gross exposure to $30,000, and buying power to $58,000. A buy-in triggers when equity drops below 30% of gross (74,000 - 200P < 0.30 × 200P), meaning P > 74,000 / 260 = $284.62. One session's borrow fee at $120.00 is $24,000 × 0.05 / 252 ≈ $4.76.",
        [
            (
                "A margin account has equity of $80,000 and gross exposure of $100,000. What is its buying power?",
                "$60,000, which is 2 × 80,000 − 100,000",
                "$160,000, twice the equity",
                "$20,000, equity less exposure",
                "Buying power is twice equity less gross exposure: 160,000 − 100,000 = $60,000.",
            ),
            (
                "Why can a short position lose more than the money first received for it?",
                "The shares must be bought back later and a price has no upper limit",
                "The borrow fee always grows faster than the price",
                "Short positions are charged the commission twice on every fill",
                "A short profits only down to zero, but it must be covered at whatever price the stock reaches, so the potential loss is open-ended.",
            ),
            (
                "In the simulator, when is a short position bought in?",
                "When equity falls below 30% of gross exposure",
                "Whenever the stock rises 10% above the short price",
                "At the end of every session, automatically",
                "The maintenance rule compares equity with 30% of gross exposure; falling below it triggers a buy-in order that queues like any other.",
            ),
            (
                "What does the simulator charge for holding borrowed shares?",
                "A borrow fee of 5% a year, charged once per session as its own ledger line",
                "Nothing, because borrowing is free in paper trading",
                "The company's dividends, paid to the lender each quarter",
                "The fee appears in Account history once per session. Dividends are not modelled in either direction.",
            ),
        ],
        [MARGIN, SHORT, MARGIN_ACCOUNT],
        (8, 14, 8),
    )

    # ---------------------------------------------------------------- Unit 3
    add(
        "Company accounts, consensus and the earnings calendar",
        "Read a fictional company's statements, ratios, consensus and reporting date, and compute a surprise and a trailing P/E without hindsight.",
        r"""
        Fundamental analysis requires evaluating a business's economic health from its financial statements. In the Quanta simulator, every fictional corporation publishes cohesive, mathematically reconciled quarterly accounting reports:
        $$\text{Surprise} = \text{EPS}_{\text{reported}} - \text{EPS}_{\text{consensus}},\qquad P/E = \frac{P}{\sum_{k=0}^{3} \text{EPS}_{t-k}}$$
        On the balance sheet, Assets always equal Liabilities plus Stockholders' Equity. On the cash flow statement, ending cash reconciles exactly with operating, investing, and financing cash flows. If a company faces a operational cash deficit, it borrows the difference, which appears as rising short-term debt and financing cash inflows.

        Consensus Expectations and Earnings Gaps:
        Prior to an earnings announcement, the market only knows consensus analyst forecasts (published in the Calendar and Company tabs). Actual results are released strictly on the morning open of the scheduled reporting date. Because the release coincides with the session open, the earnings surprise is typically expressed as an overnight price gap.

        Valuation Ratios and Loss-Making Firms:
        Valuation multiples are computed using trailing twelve-month (TTM) data across the last four reported quarters. If trailing earnings are zero or negative (as is the case with five early-stage, development-stage companies in the simulator), the Price-to-Earnings ($P/E$) ratio is undefined and correctly displays as a dash (`—`).
        """,
        r"""
        Suppose a fictional company has a consensus quarterly EPS estimate of $1.20 and reports actual EPS of $1.26. Over the prior three quarters, the company reported EPS of $1.10, $1.15, and $1.18. The current share price is $148.50.

        Step-by-step arithmetic:
        1. Earnings Surprise Calculation:
           $$\text{Dollar Surprise} = \text{Reported EPS} - \text{Consensus EPS} = \$1.26 - \$1.20 = +\$0.06$$
           $$\text{Percentage Surprise} = \frac{+\$0.06}{\$1.20} \times 100\% = +5.0\%$$

        2. Trailing Twelve-Month (TTM) EPS:
           $$\text{TTM EPS} = \$1.10 + \$1.15 + \$1.18 + \$1.26 = \$4.69$$

        3. Trailing Price-to-Earnings Ratio ($P/E$):
           $$P/E = \frac{\$148.50}{\$4.69} \approx 31.66$$

        4. Cash Conversion Quality Audit:
           Suppose the company reported Net Income of $26.0 million for the quarter, but Operating Cash Flow was only $18.5 million.
           $$\text{Cash Conversion Ratio} = \frac{\$18.5\text{M}}{\$26.0\text{M}} \times 100\% = 71.15\% \approx 71.2\%$$
           If the balance sheet also reveals a $7.5 million surge in short-term debt and accounts receivable, the earnings beat was achieved with aggressive revenue accruals rather than cash collections. An informed analyst looks beyond the headline EPS beat to inspect cash conversion.
        """,
        """
        **Open company financials.** In the Command dialog, enter `NVRA FA` and press Enter. The **Company** tab opens with a **SIMULATED** badge. The header indicates whether the next report is scheduled ("Next report … with consensus") or recently released with its surprise.

        **Inspect financial statements.** In the **Statements** panel, review **Ratios** (Valuation, Profitability, Growth, Balance Sheet, Value Screens), **Income statement**, **Balance sheet**, and **Cash flow**. Compare Net Income against Operating Cash Flow.

        **Check peer comparisons.** Click the **Peers** sub-tab to view sector competitors alongside median benchmarks for operating margin, return on equity (ROE), and debt-to-equity ratios.

        **Track the corporate calendar.** Open the **Calendar** tab. The **Company results** table lists Scheduled reporting dates, Symbol, Period, Consensus EPS, and Reported EPS. Before the print, the column reads "in N bars".

        **Observe earnings gap.** Step forward with the **1D** jump button until an earnings report prints. Compare the actual reported EPS against consensus, compute the surprise, and inspect the resulting opening price candle on the chart.
        """,
        """
        Try the mission [Hold a company through its results](/simulator?mission=earnings-gap). The link only preselects it: open the terminal, click the **New simulation run** icon, verify that **Practice mission (optional)** shows "Hold a company through its results · NVRA", and click **Create new paper account**. NVRA reports earnings at the open of Day 5. Read the financial statements and consensus estimates beforehand, write your hypothesis in **Trade thesis**, hold at least 25 shares through the announcement, and hold through the following session.
        """,
        r"\text{surprise}=\text{EPS}_{\text{reported}}-\text{EPS}_{\text{consensus}},\qquad P/E=\frac{P}{\sum_{k=0}^{3}\text{EPS}_{t-k}}",
        '''
consensus = 1.20
reported = 1.26
surprise = reported - consensus
print("Surprise:", round(surprise, 2), "or", round(surprise / consensus * 100, 1), "% of consensus")
last_four = [1.10, 1.15, 1.18, 1.26]
trailing = sum(last_four)
print("Trailing EPS:", round(trailing, 2))
print("Trailing P/E at 148.50:", round(148.50 / trailing, 2))
net_income = 26.0
operating_cash = 18.5
print("Cash conversion:", round(operating_cash / net_income * 100, 1), "%")
''',
        "Pick a company in your run before its print. Record consensus EPS and revenue, the last four reported EPS figures, the price and operating cash flow against net income for the latest quarter. After the print, compute the surprise and the new trailing P/E, and describe the opening gap.",
        "A rigorous fundamental audit records consensus forecasts and prior trailing earnings before the print occurs. The earnings surprise is computed as reported EPS minus consensus EPS. The trailing P/E divides market price by the sum of the last four quarters of reported EPS (displaying '—' if aggregate earnings are zero or negative). In addition, checking cash conversion (operating cash flow divided by net income) and changes in short-term debt reveals whether the earnings beat was backed by actual cash collections or merely accrual accounting adjustments.",
        [
            (
                "Before a fictional company reports, what does its Company tab show about the coming quarter?",
                "The period label, the date and the published consensus, but not the result",
                "The reported figures, available one click early",
                "Nothing at all until the print arrives",
                "Only the expectation is published ahead of the print. The reported figures leave the server when the clock reaches the bar that prints them.",
            ),
            (
                "Consensus EPS is $0.80 and the company reports $0.86. What is the surprise stated as a distance?",
                "+$0.06 above consensus",
                "−$0.06 below consensus",
                "+$0.86, the reported figure itself",
                "The surprise is reported EPS minus consensus: 0.86 − 0.80 = +$0.06, a beat.",
            ),
            (
                "Why does P/E show '—' for some companies in the terminal?",
                "Its denominator is zero or negative, so a ratio would be misleading",
                "The company is hiding its earnings from the market",
                "Ratios are computed only for the largest companies",
                "A ratio with a zero or non-positive denominator is returned as null and shown as '—'. Development-stage companies with losses are an example.",
            ),
            (
                "When in the simulated session do company results arrive?",
                "At a session open, so the result arrives with the gap it causes",
                "At the close, after trading has finished",
                "At a random minute inside the session",
                "Prints land on a session open, which is why the first bar of that session carries most of the reaction.",
            ),
        ],
        [READ_10K, STATEMENTS, READ_8K],
        (8, 14, 8),
    )

    add(
        "Desk analytics and monitor windows",
        "Read the Desk tab's quant sheet and lists, split the chart into monitor windows, and use a named screen as a hypothesis you test before trusting.",
        r"""
        The **Desk** tab serves as an automated quantitative research terminal. Every metric displayed carries the badge `API CALCULATED`, confirming that it is computed on the server exclusively from historical bars already elapsed at the current replay clock.

        The quant tear sheet provides instant algorithmic analytics:
        $$\text{RSI} = 100 - \frac{100}{1 + RS},\qquad RS = \frac{\overline{\text{Gain}}_{14}}{\overline{\text{Loss}}_{14}}$$
        Metrics include 14-period Relative Strength Index ($\text{RSI}_{14}$), Moving Average Convergence Divergence ($\text{MACD}$), Exponential Moving Average ($\text{EMA}_{20}$), Annualized Historical Volatility, Market Beta, and Relative Volume ($\text{RVOL} = \text{Volume} / \text{Average Volume}$). Below the sheet, market rankings highlight Top Gainers, Top Losers, Most Active, and Sector Performance.

        Multi-Pane Monitor Windows:
        The monitor feature splits the chart canvas into up to three simultaneous windows: Time & Sales (live simulated tape), Order Book (indicative market depth), Heat Map, Screener, and Real-Time Quotes.

        Hypothesis Testing vs Data Snooping:
        The stock screener provides pre-set screens (such as Oversold: $\text{RSI} < 30$, or Unusual Volume: $\text{RVOL} > 2.0$) rather than arbitrary sliders. Fixing your screening rule in advance establishes a falsifiable scientific hypothesis. Tweaking criteria after seeing which stocks rallied is data snooping, which creates an illusion of predictive power.
        """,
        r"""
        Let us work through the calculation of Relative Strength Index (RSI) and Relative Volume:

        1. RSI Calculation over a 14-Bar Window:
           Suppose the average gain over the last 14 candles is $0.60 per share, and the average loss is $0.40 per share.
           $$RS = \frac{\overline{\text{Gain}}}{\overline{\text{Loss}}} = \frac{0.60}{0.40} = 1.50$$
           $$\text{RSI} = 100 - \frac{100}{1 + RS} = 100 - \frac{100}{1 + 1.50} = 100 - \frac{100}{2.50} = 100 - 40 = 60.0$$
           An RSI of 60.0 reflects moderate upward momentum, sitting comfortably between the Oversold boundary (30) and Overbought boundary (70).

        2. Relative Volume Calculation:
           If a company has traded 2,400,000 shares today compared to its 20-day historical average volume of 1,600,000 shares:
           $$\text{RVOL} = \frac{2{,}400{,}000}{1{,}600{,}000} = 1.50\times$$
           Volume is 50% above normal, confirming institutional participation.

        3. Screening Hit Rate Evaluation:
           Suppose you run the Oversold screen across 10 sessions. Out of 16 qualifying oversold stocks, 9 rose on the following day (a 56.3% hit rate). Across the same period, 17 of 32 stocks in the Whole Listing rose (a 53.1% hit rate). The screen outperformed the broad market by just 3.2 percentage points across a tiny sample of 16 names—statistically indistinguishable from random chance.
        """,
        """
        **Explore Desk analytics.** Click **Desk** in the right sidebar (or enter `MOV` in the Command dialog). Inspect the quant tear sheet for NVRA: compare RSI 14, Beta, and Relative Volume. Click a company in **Top gainers** to immediately load it across the terminal.

        **Configure multi-monitor layout.** On the replay bar, locate the **Monitor windows** toggles and click **2** or **3**. The chart splits into multiple synchronized panes. In each pane, select a tool: Time & sales, Order book, Heat map, Screener, Sessions, Quotes, or News.

        **Read the simulated tape.** Select **Time & sales** in Monitor 2 and step forward one bar. The summary reads "N prints · M shares · X% lifted the offer". Verify that prints open at the bar's open, trade within the bar's high/low range, and close at the bar's close.

        **Execute a structured screen.** Set Monitor 2 to **Screener** and choose **Oversold**. The table lists qualifying tickers with their Last price, Day Change, RSI, and RVOL. Document your forward predictions in your notebook before advancing the replay clock.
        """,
        """
        Select one named screen (such as Oversold or Trending Up) and track it across 10 consecutive trading sessions without altering any criteria. Record qualifying tickers and measure how many rose during the subsequent session compared to the broader market listing. Evaluate whether the screen demonstrated genuine predictive edge.
        """,
        r"\text{RSI}=100-\frac{100}{1+RS},\qquad RS=\frac{\overline{\text{gain}}_{14}}{\overline{\text{loss}}_{14}}",
        '''
average_gain = 0.60
average_loss = 0.40
rs = average_gain / average_loss
rsi = 100 - 100 / (1 + rs)
print("RS:", rs, "RSI:", round(rsi, 1))
print("Relative volume:", 2400000 / 1600000)
screen_hits = 9
screen_names = 16
listing_hits = 17
listing_names = 32
print("Screen hit rate:", round(screen_hits / screen_names * 100, 1), "%")
print("Whole listing hit rate:", round(listing_hits / listing_names * 100, 1), "%")
''',
        "Run one named screen for ten sessions without changing it. Record each session's listed names, how many rose the next session, and the same count for the Whole listing. Report both hit rates and explain whether the difference supports the screen.",
        "A disciplined quantitative test fixes screening rules prior to observation and maintains them across multiple sessions. Reporting the hit rate of screened names alongside the baseline hit rate of the entire listing reveals whether the filter provided genuine edge. In small sample sizes (e.g. 16 observations), a 3% outperformance is well within normal random variance. Tuning thresholds after inspecting results constitutes data snooping and invalidates the test.",
        [
            (
                "What does the badge 'API CALCULATED' on the Desk tab tell you?",
                "The figures are computed on the server from bars already observed at the clock",
                "The figures come from a real market-data vendor",
                "The figures are forecasts of future prices",
                "Desk figures are calculated by the API from the run's observed bars only, so none of them can depend on a price you have not seen.",
            ),
            (
                "Average gain is 0.60 and average loss is 0.40 over the RSI window. What is the RSI?",
                "60",
                "40",
                "150",
                "RS = 0.60 ÷ 0.40 = 1.5, so RSI = 100 − 100 ÷ 2.5 = 60.",
            ),
            (
                "How do the prints in the Time & sales window relate to your fills?",
                "They are an illustration consistent with the bar's open, high, low, close and volume, and never affect fills",
                "Your orders fill against those prints one by one",
                "They are the recorded tape of a real exchange",
                "The tape is generated inside each bar's limits for reading practice. Fills come only from the bar's prices under the execution rules.",
            ),
            (
                "Why does the Screener offer named screens such as Oversold rather than free-form thresholds?",
                "A named screen is a hypothesis fixed in advance, while tuning a threshold after seeing results fits the filter to the answer",
                "Free-form thresholds take too long for the server to compute",
                "Named screens guarantee that the listed stocks will rise",
                "Choosing the threshold after seeing which names rose builds the answer into the screen, which is the screening version of data snooping.",
            ),
        ],
        [QUOTES, EWM, LEAKAGE],
        (8, 14, 8),
    )

    add(
        "Performance against the QX-200, journals and exports",
        "Read the Performance tab against the QX-200 benchmark, journal each order's reasoning, and export your records safely.",
        r"""
        Evaluating trading performance against zero tells you nothing about investment skill. If broad equity markets rally 15% while your portfolio gains 4%, you have suffered an 11% opportunity loss despite your positive return. In the Quanta simulator, your portfolio is benchmarked directly against the QX-200:
        $$\text{Win Rate} = \frac{n_{\text{win}}}{n_{\text{closing}}},\qquad \text{Profit Factor} = \frac{\sum \text{Gross Wins}}{|\sum \text{Gross Losses}|},\qquad r_{\text{excess}} = r_p - r_{\text{QX-200}}$$
        The QX-200 is an equal-weighted benchmark index comprising all 32 synthetic companies, rebased to 100.0 on the exact bar your run was initialized. Measuring excess return ($r_{\text{excess}} = r_p - r_{\text{QX-200}}$) isolates your true alpha from market beta.

        Key Portfolio Analytics:
        • Win Rate: The percentage of closed round-trip trades that realized a net gain.
        • Profit Factor ($\text{PF}$): Gross winning dollars divided by gross losing dollars ($> 1.0$ indicates positive expectancy).
        • Maximum Drawdown: The peak-to-trough percentage decline in account equity.
        • Risk-Adjusted Metrics: Sharpe ratio, Sortino ratio, and Value at Risk (VaR) are annualized across 252 sessions. The panel issues an explicit statistical warning below 20 closed sessions because small samples produce noisy estimates.

        Journaling and CSV Export Security:
        A complete trading review requires inspecting both quantitative metrics and qualitative decision journals. When exporting tables to CSV, the terminal sanitizes data against CSV formula injection by prepending an apostrophe to cells starting with `=`, `+`, `-`, or `@`.
        """,
        r"""
        Suppose an account completes four round-trip closing trades with realized P&L of +$120, +$80, -$50, and -$150.

        Step-by-step performance metrics:
        1. Trade Counting and Win Rate:
           Total closed trades: 4. Winning trades: 2.
           $$\text{Win Rate} = \frac{2}{4} \times 100\% = 50.0\%$$

        2. Profit Factor:
           $$\text{Gross Wins} = \$120 + \$80 = \$200$$
           $$\text{Gross Losses} = |-\$50 + (-\$150)| = \$200$$
           $$\text{Profit Factor} = \frac{\$200}{\$200} = 1.00$$
           The account broke even across its closed trading activity. Average win is $100, and average loss is -$100.

        3. Maximum Drawdown Calculation:
           Suppose account equity traced the following values across four sessions:
           $$\text{Equity} = [\$100{,}000,\; \$101{,}200,\; \$99{,}800,\; \$100{,}600]$$
           Peak equity was reached at $101,200. The subsequent lowest trough was $99,800.
           $$\text{Dollar Drawdown} = \$101{,}200 - \$99{,}800 = \$1{,}400$$
           $$\text{Maximum Drawdown \%} = \frac{\$1{,}400}{\$101{,}200} \times 100\% \approx 1.38\%$$

        4. Excess Return Benchmarking:
           If your portfolio returned $+0.60\%$ over the week while the QX-200 index gained $+0.90\%$:
           $$r_{\text{excess}} = +0.60\% - (+0.90\%) = -0.30 \text{ percentage points}$$
           Your portfolio lagged the passive benchmark by 30 basis points.
        """,
        """
        **Open the Performance dashboard.** In the bottom panel, click the **Performance** tab (or enter `PORT` in the Command dialog). Review **Equity**, **Total return**, **Max drawdown**, **Realized P&L**, **Unrealized P&L**, **Win rate**, and **Profit factor**.

        **Inspect benchmark chart.** Examine the **Equity path vs QX-200** chart. Note your return alongside **QX-200 return**, **Excess return**, **Beta**, and **Alpha**. Review the **Attribution by company** table to see which holdings drove your results.

        **Record a trade journal entry.** In **Trade history** or **Order history**, click **Journal** on an order row. Enter a clear trade thesis and link it to a curriculum concept, then click **Save journal**.

        **Export audit records.** On any bottom-panel table, click **Export table as CSV** to download a spreadsheet audit file. To export the full simulation run (including trade history, chart drawings, and journal entries), click **Export simulation** in the bottom status bar and select "Run, chart settings & journal (JSON)".
        """,
        """
        Try the mission [Size a position you could survive](/simulator?mission=position-size). The link only preselects it: open the terminal, click the **New simulation run** icon, verify that **Practice mission (optional)** shows "Size a position you could survive · ZEPH", and click **Create new paper account**. Maintain all positions strictly under 5% of opening equity ($5,000), place at least three orders, and trade through a full simulated week. Document each trade in your journal and export the resulting trade history.
        """,
        r"\text{win rate}=\frac{n_{\text{win}}}{n_{\text{closing}}},\qquad \text{PF}=\frac{\sum \text{wins}}{\left|\sum \text{losses}\right|},\qquad \text{excess}=R_p-R_{\text{QX-200}}",
        '''
trades = [120, 80, -50, -150]
wins = 0
gross_win = 0
gross_loss = 0
for r in trades:
    if r > 0:
        wins = wins + 1
        gross_win = gross_win + r
    else:
        gross_loss = gross_loss + abs(r)
print("Win rate:", wins / len(trades) * 100, "%")
print("Profit factor:", gross_win / gross_loss)

equity = [100000, 101200, 99800, 100600]
peak = equity[0]
worst = 0
for value in equity:
    peak = max(peak, value)
    worst = max(worst, (peak - value) / peak)
print("Max drawdown:", round(worst * 100, 2), "%")
print("Excess return vs QX-200:", round(0.6 - 0.9, 1), "points")
''',
        "Export your trade history after a week of practice. From the CSV, compute the number of closing trades, win rate, profit factor and average win and loss, and compare them with the Performance tab. Then write one paragraph comparing your return with the QX-200.",
        "Closing trades are rows in Trade history that realized a non-zero P&L. Win rate is calculated as profitable closing trades divided by total closing trades. Profit factor is gross winning dollars divided by gross losing dollars (undefined if zero losses occur). When comparing performance against the QX-200, document portfolio return, benchmark return, excess return, and portfolio beta across identical trading bars. A one-week sample is too brief to establish statistical skill; journal entries provide the audit trail to confirm whether results reflected disciplined adherence to rules.",
        [
            (
                "Four closing trades realize +120, +80, −50 and −150. What is the profit factor?",
                "1.00, gross wins of 200 divided by gross losses of 200",
                "2.00, because there were two winners for every loser",
                "0.50, the win rate",
                "Profit factor divides gross wins by the absolute value of gross losses: 200 ÷ 200 = 1.00.",
            ),
            (
                "What is the QX-200 in the Performance tab?",
                "An equal-weighted index of every company in the run, rebased to the bar your account opened on",
                "A real stock-market index from a live feed",
                "The average of the companies you hold",
                "The benchmark is computed from the run's own fictional companies, so it measures the simulated market over exactly the bars your account existed.",
            ),
            (
                "Only 6 sessions have closed and the panel shows a Sharpe ratio of 3.1. What should you conclude?",
                "Very little: annualizing so few returns produces a number, not a measurement",
                "That the approach is excellent and should be scaled up",
                "That the account carried no risk during the period",
                "The panel warns below 20 closed sessions because annualized ratios from a handful of returns are dominated by noise.",
            ),
            (
                "Why does an exported CSV cell that begins with '=' gain an apostrophe?",
                "To stop a spreadsheet from executing it as a formula when the file is opened",
                "To mark values that changed after the export",
                "To show that the value is negative",
                "Cells starting with =, +, − or @ can be interpreted as formulas. The apostrophe keeps them as text.",
            ),
        ],
        [PERFORMANCE, CSV_SAFETY, RISK_TOLERANCE],
        (8, 14, 8),
    )

    add(
        "Capstone: practice missions and a week inside your trading charter",
        "Complete a week of practice inside written limits, judged by process rather than profit, and deliver a review another person could check.",
        r"""
        A practice mission translates curriculum theory into live operational discipline. In a mission, the market seed, start date, target instrument, and three explicit operational objectives are pre-set by the server. Every objective is verified server-side from your orders, executions, positions, and clock timestamps.

        Crucially, mission objectives never evaluate whether you made money. Profit is intentionally excluded as an assessment criterion. In trading, outcome bias is toxic: a rule broken profitably is still an operational violation, while a disciplined loss taken in accordance with your risk controls is a sound execution.

        The Capstone Mission ("Trade inside your written limits"):
        $$q_{\max} = \left\lfloor\frac{0.05 \cdot E_0 - c}{P_{\text{fill}}}\right\rfloor,\qquad \text{Position Cap} = 0.05 \times E_0$$
        The capstone requires executing an entire simulated week (1,950 bars) inside the trading charter established in the ethics course:
        1. Strict Position Sizing: No position may exceed 5% of opening equity ($5,000 on a $100,000 account). The server evaluates the peak holding ever carried during the run; closing an oversized position later does not erase the breach.
        2. Documented Trade Theses: Every single submitted order must carry an auditable written thesis.
        3. Flat Finish: All open positions must be fully closed before completing the week.
        """,
        r"""
        Let us calculate the maximum allowable position size under the 5% charter cap:
        Opening equity is $E_0 = $100,000.
        $$\text{Position Cap} = 0.05 \times \$100{,}000 = \$5{,}000.00$$
        This $5,000 cap is an all-inclusive limit encompassing share purchase cost and broker commissions ($c = $1.00).

        Suppose Meridian Power (MRDN) opens at $52.30 per share ($f = 0.0003$):
        1. Projected Fill Price:
           $$P_{\text{fill}} = 52.30 \times 1.0003 = 52.31569 \implies \$52.32$$

        2. Maximum Allowable Shares:
           $$q_{\max} = \left\lfloor \frac{\$5{,}000 - \$1.00}{\$52.32} \right\rfloor = \left\lfloor \frac{4{,}999.00}{52.32} \right\rfloor = \lfloor 95.546 \rfloor = 95\text{ shares}$$

        3. Total Outlay for 95 Shares:
           $$95 \times \$52.32 + \$1.00 = \$4{,}970.40 + \$1.00 = \$4{,}971.40 \quad (\text{Compliant: } < \$5{,}000)$$

        4. What happens if you buy 100 shares?
           $$100 \times \$52.32 + \$1.00 = \$5{,}232.00 + \$1.00 = \$5{,}233.00$$
           This purchase commits $5,233.00, exceeding the cap by $233.00. Even if the position gains 10% and you sell 5 shares one minute later, the server flags the run as breached because the cap is judged on peak exposure.
        """,
        """
        **Initialize the capstone mission.** Open [Trade inside your written limits](/simulator?mission=charter). The link preselects the configuration: click **New simulation run**, verify that **Practice mission (optional)** displays "Trade inside your written limits · MRDN", and click **Create new paper account**. The mission starts on Day 2 at 11:19 AM ET in a cash account with $100,000.

        **Review mission objectives.** Expand the **Practice mission** panel beneath the toolbar. Review the three objectives: (1) Keep every position under 5% of opening equity ($5,000), (2) Write a thesis on every order, and (3) Close all positions before finishing.

        **Execute your trading week.** Calculate your maximum share size before submitting any order. Enter a trade thesis in the ticket drawer for every single order. Advance through the week using the **1D** jump button (390 bars) or **1W** jump button (1,950 bars).

        **Close all positions flat.** In the **Positions** tab, click **Close** on every open holding. Preview, submit, and advance the clock until all closing orders fill. The mission panel displays "All objectives met" only after a full week (1,950 bars) has elapsed with zero remaining shares.

        **Export audit file.** Click **Export simulation** in the bottom status bar and download "Run, chart settings & journal (JSON)". Use the 12-item review checklist to prepare your capstone analysis.
        """,
        """
        Complete the charter mission and write a comprehensive one-page audit covering the twelve checklist items: seed, cost settings, sessions, orders, a thesis on every order, peak position versus cap, QX-200 benchmark return, excess return, maximum drawdown, unmodeled market frictions, key lessons learned, and the next falsifiable hypothesis.
        """,
        r"q_{\max}=\left\lfloor\frac{0.05\,E_0-c}{P_{\text{fill}}}\right\rfloor",
        '''
from math import floor

def to_cent(x):
    return floor(x * 100 + 0.5) / 100

opening_equity = 100000
cap = 0.05 * opening_equity
commission = 1
fill = to_cent(52.30 * (1 + (2 + 2 / 2) / 10000))
shares = floor((cap - commission) / fill)
print("Cap:", cap, "fill:", fill, "max shares:", shares, "cost:", round(shares * fill + commission, 2))
print("100 shares would cost:", round(100 * fill + commission, 2))

checklist = ["seed", "cost settings", "sessions", "orders", "thesis on every order",
             "largest position vs cap", "QX-200 return", "excess return", "max drawdown",
             "what is not modelled", "lesson learned", "next experiment"]
print("Simulator review checklist:", len(checklist), "of", 12)
''',
        "Complete the charter mission and write a one-page review covering the twelve checklist items: seed, cost settings, sessions, orders, a thesis on every order, the largest position against the cap, the QX-200 return, the excess return, the maximum drawdown, what the simulator does not model, the lesson you learned and the next experiment you would run.",
        "A complete review states the mission seed (9006) and the cost settings, the number of sessions and orders, and confirms a thesis on every order. It reports the largest position's peak cost against the $5,000 cap, the account's return beside the QX-200 return with the excess return, and the maximum drawdown. It lists what the simulator leaves out, such as dividends, queue position, market impact and real borrow availability, and it ends with one lesson and one falsifiable next experiment. It does not claim skill from a single generated week.",
        [
            (
                "What do practice missions judge?",
                "What you did and recorded, such as limit entries, theses and position caps, never profit",
                "Whether the run ended with a gain",
                "How many of your orders filled at the best price of the day",
                "Every objective describes process and is judged on the server from orders, fills, positions and the clock. None reads P&L.",
            ),
            (
                "The charter mission caps each position at 5% of $100,000 opening equity. Which purchase breaches it?",
                "100 shares at a fill of 52.32 plus the $1 commission",
                "95 shares at a fill of 52.32 plus the $1 commission",
                "50 shares at a fill of 52.32 plus the $1 commission",
                "100 × 52.32 + 1 = $5,233, above the $5,000 cap; 95 shares cost $4,971.40 and 50 shares $2,617.00.",
            ),
            (
                "A position breached the cap and was cut back the next bar at a profit. How does the cap objective treat it?",
                "As a breach, because the cap is judged on the largest holding the run ever carried",
                "As satisfied, because the position was reduced afterwards",
                "As satisfied, because the trade made money",
                "The cap looks at the peak holding, so reducing it later does not undo the breach, and profit does not excuse it.",
            ),
            (
                "What does the objective 'Close every position before finishing' require?",
                "No shares held once a full week of bars has passed since your first order",
                "Selling every position at a profit",
                "Closing all positions before the first session ends",
                "The objective is met when a full week (1,950 bars) has passed since your first order and the account holds no shares.",
            ),
        ],
        [RISK_TOLERANCE, GOALS, PERFORMANCE],
        (6, 16, 8),
    )

    parts = [
        (
            "Set up and read the market",
            "A reproducible paper run, the terminal layout, the replay clock and the simulated newsroom.",
        ),
        (
            "Place and manage orders",
            "Market, limit, stop and attached-exit orders, how fills are priced, and margin accounts with short selling.",
        ),
        (
            "Research, review and discipline",
            "Company accounts and the calendar, desk analytics and monitor windows, performance review, and a week inside your charter.",
        ),
    ]
    track = finish(
        {
            "id": "simulator-workshop",
            "number": 13,
            "title": "Trading simulator workshop",
            "description": COURSE_GUIDE[0],
            "source": "Original Quanta course · Quanta trading simulator documentation, Investor.gov, SEC, NYSE & software documentation",
            "level": "Beginner → intermediate",
            "icon": "factors",
            "studyType": "applied",
            "modules": modules,
            "prerequisites": "Complete Trading & market fundamentals and Trading ethics first.",
            "outcomes": [
                "Start a paper run with an account type, market seed and cost settings that you can explain and reproduce.",
                "Read the chart, the replay clock, the simulated newsroom and the command codes without using hindsight.",
                "Place, preview, amend and cancel market, limit, stop, trailing-stop and attached-exit orders, and predict how each fills, including partial fills and gaps.",
                "Use a margin account to sell short, and explain buying power, borrow fees and a forced buy-in.",
                "Research fictional companies with their statements, consensus, calendar, desk analytics and monitor windows.",
                "Review performance against the QX-200, journal your reasoning, export your records and complete a week of practice inside a written trading charter.",
            ],
            "readingGuide": "12 lessons × 30 minutes = 6 hours of planned study across three units: about 8 minutes of reading, 14 minutes following the steps in the terminal and 8 minutes on the worksheet and notebook in each lesson; exam time is additional. Includes 24 practice questions, three four-question checkpoints, a 12-question final and six practice missions linked from the lessons. Every company, headline and price in the terminal is fictional and the market is simulated, and a profitable simulated trade is not evidence of skill. The simulator does not model dividends, queue position, market impact, real borrow availability or any broker's rules.",
            "parts": [
                {"id": str(i), "title": t, "description": d} for i, (t, d) in enumerate(parts, 1)
            ],
            "references": [
                {"title": t, "url": u} for t, u in [ORDER_TYPES, STOP_BULLETIN, MARGIN, SHORT, PERFORMANCE]
            ],
            "resources": [],
        },
        checkpoints_for(modules, parts, 3),
    )
    track["exams"][-1]["version"] = 1
    return track
