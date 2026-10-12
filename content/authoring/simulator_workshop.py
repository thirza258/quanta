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
    "The Trading simulator is a practice terminal with $100,000 of paper money and a market made entirely of fictional companies. Nothing in it is real, which is the point: you can make mistakes, repeat a situation and look closely at what you did without risking anything. This course shows you every part of the terminal one small step at a time, so the tools are familiar before you rely on them.\n\n"
    "Each lesson explains one idea, works through a short example with real numbers, and then gives you click-by-click steps that use the exact button names you will see on screen. Follow the steps in the terminal while you read, recompute the example in the worksheet, and write down what you expect before you press anything that moves the clock. Several lessons link to a practice mission. A mission judges what you did and wrote, never whether the trade made money, because a good result in a simulation is not evidence of skill.",
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
    """Join hard-wrapped source lines into paragraphs separated by one blank line."""
    return "\n\n".join(" ".join(part.split()) for part in value.strip().split("\n\n"))


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

    add(
        "Start a paper run: account type, seed and a fictional market",
        "Create a paper account whose settings you can explain, and know what a new run keeps, archives and replaces.",
        """
        A paper run is a small experiment, and its settings are the conditions of the experiment. The account
        type decides whether you can only sell shares you own or may also borrow shares to sell. The market seed
        is a whole number that fixes the entire generated world: with the same seed the terminal produces the same
        bars, headlines, reporting calendar and company accounts, so you can repeat a decision under identical
        conditions. Left empty, the seed is chosen for you and every new account meets a different market.

        The four cost fields turn trading friction into numbers you can inspect: a flat commission per order,
        slippage and spread in basis points (one basis point is 0.01%), and volume participation, the share of
        each bar's volume your orders may take. The defaults ($1, 2 bps, 2 bps and 1%) are teaching assumptions,
        not any broker's price list. A new run is always a new $100,000 account, never a reset in place, and
        earlier runs stay in the run history for review. Every company is fictional and every price is generated,
        so nothing in the terminal is a statement about a real security.
        """,
        """
        Suppose the next bar opens at 148.50 and you buy 10 shares at market with the default costs. Friction is
        (2 + 2 ÷ 2) ÷ 10,000 = 0.0003, which is 3 basis points. The buy fills at 148.50 × 1.0003 = 148.54455,
        rounded to the cent: 148.54. You pay 10 × 148.54 = $1,485.40 plus the $1 commission, so cash falls from
        $100,000.00 to $98,513.60.

        Now suppose the price has not moved when you sell. The sale fills at 148.50 × 0.9997 = 148.45545, which
        rounds to 148.46, so you receive $1,484.60 less the $1 commission and cash ends at $99,997.20. The price did
        not change, yet the round trip cost $2.80: $0.80 from the gap between the two fills on 10 shares, and $2.00
        in commissions.

        Raise slippage and spread to 10 bps each and friction becomes 0.0015. The same round trip now fills at
        148.72 and 148.28 and costs $6.40. The market is identical and only the settings differ, which is why a
        result means little unless its seed and costs are written beside it.
        """,
        """
        **Open the terminal.** Choose **Trading simulator** in the left navigation. On a first visit the terminal
        creates a default run for you: a cash account with $100,000, 32 fictional companies and a seed taken from
        the run's identifier. The account bar shows **PAPER TRADING**, **Equity**, **Cash** and **Realized P&L**.
        The replay bar should read "Day 2 · bar 110/390" with the clock at "Jan 7, 11:19 AM ET". In the status bar,
        "Guest · saved for this browser" means a 30-day browser cookie holds your run, and "Account synced" means
        it belongs to your signed-in account. Runs created as a guest never merge into an account later.

        **Open the dialog.** Click the **New simulation run** icon (the circular arrows) at the right end of the
        replay bar. The dialog **Start a new simulation** opens. Leave **Practice mission (optional)** on
        "No mission · free practice" for now.

        **Choose the account type.** **Account type** offers "Cash · long only" (the default) and
        "Margin · may sell short". Keep Cash for now; lesson 13.8 uses Margin. If the small print at the foot of the
        dialog still says long-only after you choose Margin, trust the help text under **Account type**, and the
        MARGIN badge that appears in the account bar once the run exists.

        **Choose the market.** **Market data** is "Seeded synthetic market". "Historical replay" is disabled and
        labelled "· no imported datasets", because no historical data ships with the course.

        **Set the seed.** In **Market seed (optional)** type a whole number from 0 to 1,000,000, such as 4242, or
        leave the box empty to see the placeholder "Automatic". A mission overrides this field with its own fixed
        seed.

        **Check the costs.** The four numeric fields start at **Commission / order ($)** 1, **Slippage (bps)** 2,
        **Spread (bps)** 2 and **Volume participation (0–1)** 0.01. They accept 0 to 100, 0 to 100, 0 to 100 and
        0.001 to 1. Leave them alone for this first run.

        **Create the account.** Click **Create new paper account**. The notice reads "New $100,000 paper account
        ready. Prior runs remain in your run history." and the status bar shows the seed you typed. If a creation
        attempt fails, the terminal keeps the saved request and resends it unchanged on your next click, so check
        the seed in the status bar and the costs under **Execution model** before you rely on the new run.

        **Find the old run.** Open the select **Simulation run history** in the status bar. The newest entry reads
        "Current · {date}" and the others "Archived · {date}". Choose an archived run and the terminal shows
        "Archived run · review and export only"; click **Return to current run** to trade again. A new run keeps
        your layout, symbol, indicators and watchlist, but not your drawings or your order ticket.

        **Check.** Create a second run with the same seed. The first chart and the watchlist prices should match the
        first run. Create a third run with the seed left empty and they should differ.
        """,
        """
        Create a run with seed 4242 and the default costs, and write the seed and the four cost settings in your
        notebook. Create a second run with seed 4242 and compare the watchlist prices with the first. Then create a
        third run with **Slippage (bps)** 10 and **Spread (bps)** 10 and keep it for lesson 13.5, where you will
        measure a round trip yourself. No practice mission is needed yet: missions start in the same dialog, and
        lessons 13.4, 13.5, 13.7, 13.9, 13.11 and 13.12 each link one.
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
        "With the defaults, friction is 0.0003: the buy fills at 96.43 and the sale at 96.37, so the round trip costs 2 × $1 plus 20 × $0.06 = $3.20. With Slippage 10 and Spread 10, friction is 0.0015: the fills are 96.54 and 96.26, so the cost is $2 plus 20 × $0.28 = $7.60. Neither setting is correct in itself. The defaults are mild teaching assumptions and the higher settings are a harsher test; whichever you choose, write the settings next to every result so that the numbers can be compared and repeated.",
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
        """
        A trading terminal shows several views of one account and one clock. Some panels carry information about
        the market (the chart, News, Company and Desk) and some carry the state of your account (Positions, Open
        orders, Order history, Trade history and Account history). Keep the two groups apart in your head: a chart
        can tempt you, but only the state panels tell you what you own, what is waiting and what you paid.
        Everything on screen is bounded by the replay clock, because the server never sends a bar, headline or
        result dated after it.

        The chart header says exactly what you are looking at: the symbol, the timeframe, the time zone (ET, the
        New York exchange clock), the label SYNTHETIC, and the open, high, low, close and volume of the bar under
        the pointer. Indicators are calculated by the server from the bars you can already see, and each one needs
        a warm-up, because a 20-bar average cannot exist until 20 bars have formed. An indicator's period counts bars
        of the timeframe you are viewing, so the same setting means 20 minutes on the 1m chart and 20 hours on the
        1h chart. The Command dialog is the keyboard route through all of this.
        """,
        """
        At the default start the market has 500 one-minute bars behind the clock: all 390 bars of Day 1 and the
        first 110 of Day 2. The 1m chart therefore holds 500 bars. Group them by the hour and the 1h chart holds 9
        bars: Day 1 gives six full hours and a last half hour (7 bars), and Day 2 gives 2 so far. The 1D chart holds
        just 2.

        A 20-bar simple moving average needs 20 bars. On the 1m chart it exists almost everywhere. On the 1h chart
        the legend shows "SMA 20 · warming up", because 9 bars are fewer than 20, and 11 more hourly bars are needed.
        On the 1D chart no value can exist for another 18 sessions.

        To see the arithmetic of an average, take five closes of 148.50, 148.56, 148.62, 148.58 and 148.64
        (illustrative). Their sum is 742.90 and a 5-bar average is 742.90 ÷ 5 = 148.58. An average lags the price by
        design: it tells you where the price has been, not where it will go.
        """,
        """
        **Open the Command dialog.** Click the symbol button at the left of the toolbar; it shows the current
        symbol, NVRA by default. The dialog **Command** opens with the box **Search stocks**. Type a ticker alone to
        choose a company, a function code alone to open a view, or both: `NVRA N` selects Novara Microsystems and opens
        its news. Press Enter. The codes are GP (chart), N or NEWS (news), MOV or DESK (the Desk tab), FA or DES
        (company financials), RV or PEER (the peer table), CAL, ECO or EARN (the calendar), PORT (performance),
        POS (positions), OMON (open orders), BLOT (trade history), W (watchlist), BUY and SELL (tickets) and HELP
        (the execution model). The code buttons in the dialog act on the current symbol. Tickers must match exactly:
        pressing Enter on a company name leaves the dialog open, so click a result instead.

        **Set the chart.** In the toolbar, the group **Chart timeframe** offers 1m, 5m, 15m, 1h and 1D, and the
        select **Chart type** offers Candles, OHLC bars and Line. Click 1h and notice how few bars the chart holds,
        then click 1m again. The icons **Fit chart** and **Return to latest bar** reset the view.

        **Read the header.** At the top left of the chart find "NVRA · 1m · ET · SYNTHETIC" followed by O, H, L, C and
        Vol for the bar under the pointer, or for the latest bar when the pointer is away. Vol matters later: it
        limits how many shares your orders can fill in one bar.

        **Add an indicator.** Click **Indicators**. The dialog starts with Volume and SMA 20 and says "At most eight
        indicators." Under **Add indicator** choose RSI, whose period starts at 14. The eye icon (**Hide SMA** or
        **Show SMA**) and the cross (**Remove SMA**) hide and remove an indicator. Periods run from 2 to 200, and
        MACD has a **Fast period**, a slow period and a signal period.

        **Draw on the chart.** In the left rail **Chart tools**, choose **Trend line** and click two points on the
        chart; the hint reads "Click two points on the chart · Esc to cancel". **Horizontal line** and
        **Text annotation** need one click, and **Rectangle** and **Price measurement** need two. **Undo drawing** and
        **Redo drawing** step back and forward, and so do Ctrl or Cmd with Z, plus Shift to redo, outside text
        boxes. **Objects** in the toolbar opens the Drawings tab, where a form edits a drawing by price and time; the
        form lists times in UTC while the chart uses ET.

        **Find the panels.** The right sidebar has five tabs: **Watchlist**, **News**, **Desk**, **Trade** and
        **Drawings**. The bottom panel has eight: **Positions**, **Open orders**, **Order history**, **Trade history**,
        **Account history**, **Company**, **Performance** and **Calendar**. Drag the separators **Watchlist width**
        and **Trading panel height**, or press the arrow keys while one has focus. **Collapse watchlist** and
        **Collapse trading panel** hide a panel, and **Open watchlist** and **Open trading panel** bring it back. On a
        narrow screen the same views appear as the tabs Chart, Watchlist, News, Trade and Portfolio.

        **Right-click for a limit ticket.** Right-click the chart at a price. The **Trade** tab opens with the ticket
        set to **Limit** at that price. Nothing is placed until you preview and confirm, as lesson 13.5 shows.

        **Open the guide.** The question-mark icon **Simulator walkthrough**, or the **Execution model** button in the
        status bar, opens a five-step guide and a collapsible description of the execution and accounting model. It
        never opens by itself.

        **Check.** Typing POS, OMON, BLOT and PORT should open four different bottom tabs, and the 1h chart should
        show SMA 20 as warming up until 20 hourly bars exist.
        """,
        """
        Run POS, OMON and BLOT from the Command dialog and note which tab each opens. Set the 1h timeframe and record
        how many bars you can see. Add RSI and write down its default period. Then write one line for each of the
        eight bottom tabs saying whether it shows market information or the state of your account. No practice
        mission fits this lesson, because it asks you to look rather than trade.
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
total = 0
for close in closes:
    total = total + close
print("Sum of the five closes:", round(total, 2))
print("5-bar simple moving average:", round(total / len(closes), 2))
''',
        "In your notebook, build a one-page map of the terminal: the five right-sidebar tabs and the eight bottom-panel tabs, the command code that opens each one you can reach by code, and whether each shows market information or the state of your account. Then work out how many bars the 1h chart holds when a run starts and how many more an SMA 20 needs.",
        "The right sidebar has Watchlist (W), News (N), Desk (MOV), Trade (BUY or SELL) and Drawings (opened with Objects). The bottom panel has Positions (POS), Open orders (OMON), Order history, Trade history (BLOT), Account history, Company (FA), Performance (PORT) and Calendar (CAL). Positions, Open orders, Order history, Trade history and Account history are the state of your account; News, Desk, Company and Calendar describe the market, and Performance compares the two. At the start the 1h chart holds 9 bars (7 from Day 1 and 2 from Day 2), so an SMA 20 needs 11 more hourly bars, a little under two sessions.",
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
        """
        In the terminal the replay clock is the only moment that exists. The server answers every request with
        data dated at or before the clock: bars, headlines, statements, calendar outcomes and analytics. That makes
        hindsight impossible inside the terminal, but not inside your head. Once you have advanced the clock you can
        no longer remember what you honestly thought before, so write the decision, the reason and what would change
        your mind first, and advance afterwards.

        The controls move the clock in bars, not in seconds. A session is 390 one-minute bars, from 09:30 to 16:00 ET,
        and a week is 5 sessions, 1,950 bars. The jump buttons 15m, 1h, 1D and 1W move 15, 60, 390 and 1,950 bars at
        once. Replay speed (1×, 5×, 30× and 390×) is the number of bars advanced about every 0.8 seconds while Play is
        on; it is a bar rate, not a time multiplier. A large jump is processed bar by bar on the server, so orders
        can fill and stops can trigger inside it, but you are not there to react, as if you had left your desk.
        """,
        """
        A new run starts at bar index 499, which the replay bar shows as Day 2, bar 110. For any index c, the session
        is c ÷ 390 rounded down, plus 1, and the bar number is the remainder of c ÷ 390, plus 1. The clock time is
        09:30 plus one minute for each bar after the first.

        Click Next replay bar: c = 500, so Day 2, bar 111, 11:20 AM ET. Then the 1h jump adds 60 bars: c = 560, which is
        Day 2, bar 171, 12:20 PM ET. The 1D jump adds 390: c = 950, which is Day 3, bar 171, the same time on the next
        day. The 1W jump adds 1,950, which is five sessions: c = 2,900, which is Day 8, bar 171. Day numbers count
        sessions, so weekends never appear as days.

        Speed works the same way. At 1× each tick advances 1 bar, so a session of 390 bars takes 390 × 0.8 = 312 seconds,
        about five minutes. At 30× a session takes 13 ticks, 10.4 seconds. At 390× a session passes in a single tick.
        """,
        """
        **Find the replay bar.** Under the chart, from left to right: **Play replay** (which becomes **Pause replay**),
        **Next replay bar**, the group **Jump replay** (15m, 1h, 1D and 1W, with hover text such as "Jump forward by one
        hour"), the newspaper icon **Mark scored headlines on the chart**, the group **Monitor windows** (1, 2, 3), the
        select **Replay speed**, the clock text, the bar **Progress through the session**, the counter ("Day 2 · bar
        110/390") and the **New simulation run** icon.

        **Write before you step.** In your notebook write one line: the company, what you expect over the next hour,
        and why. Then click **Next replay bar** once. The counter moves to bar 111, the clock to 11:20 AM ET, and the
        notice reads "Replay advanced by one bar."

        **Jump an hour.** Click **1h**. The notice reads "Replay advanced by one hour." and the counter reads bar 171,
        12:20 PM ET. Compare the chart with your line.

        **Play and pause.** Choose 5× in **Replay speed**, click **Play replay** and watch the counter move in steps of
        five bars. Click **Pause replay**, or press Esc, to stop. Esc also cancels a drawing tool. Opening an order
        preview, cancelling or editing an order, and any error message also pause the replay.

        **Cross the close.** Click **Next replay bar** until the clock reads 3:59 PM ET. The clock text now adds
        "Market closed · next session on step". One more click moves to 9:30 AM the next morning, where the price can
        open away from the previous close: an overnight gap.

        **Check.** After each jump, the counter and clock should match your own arithmetic, the News tab should list
        nothing dated after the clock, and your notebook line should have been written before the step.
        """,
        """
        Use a free-practice run. Before each of three jumps (**15m**, **1h** and **1D**), write your expected direction
        for NVRA at the end of the jump and one sentence of reasoning. After the jump, mark whether you were right and
        whether your reasoning was. Three notes prove nothing about skill. The aim is to notice how easily the
        reasoning rewrites itself once the answer is visible. No practice mission is needed here.
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
        "Next replay bar gives Day 2, bar 111 (11:20 AM ET). The 1h jump gives Day 2, bar 171 (12:20 PM). The 1D jump gives Day 3, bar 171 (12:20 PM). The 1W jump gives Day 8, bar 171 (12:20 PM), because each jump adds to the clock the one before left. Your decision note should name the company, the expected direction over a stated period, the reason and what would change your view, and it must be written before the jump. The comparison afterwards should judge the reasoning as well as the result: a correct guess for a poor reason is luck, and a wrong guess for a good reason may be fine.",
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
        """
        The simulated newsroom is generated before the prices, and the price engine then applies each headline's
        score. In this market, therefore, a move can be traced to a cause. One point is one basis point (0.01%), so a
        +250 point item is a modelled move of +2.50%, of which 58% lands on the bar the item is dated and the rest
        drifts over the bars that follow. A company item applies its score to one company. A sector item reaches its
        members through their sector loading and a macro release reaches every company through its beta, so the same
        score does not move every stock by the same amount. Each item is tagged by scope (CO for one company, SEC for
        a sector, ECO for a macroeconomic release, MKT for the whole market) and by impact: H for 400 points or more,
        M for 120 or more, L below that, and a dot for routine chatter, which carries no score and moves nothing.

        Real markets give you no such score. You never see how much a real headline is worth, and prices move for
        many reasons at once. Use this tool to practise asking what a headline implies and for whom, not to conclude
        that headlines predict prices. Not every candle has a story either, because noise moves prices on its own, and
        an invented headline is not evidence about any real company. Tone summarises the tape. It is the weight of the
        released items, counted as 3 for high, 2 for medium and 1 for low, signed plus or minus for positive or negative
        news, divided by the total weight. It therefore sits between −1 and +1 however much chatter there is.
        """,
        """
        Suppose a company item on NVRA is scored +250 points. That is a modelled move of 250 × 0.0001 = 2.50%. With the
        stock at 148.50 the total is about $3.71, of which 58% (about $2.15) lands on the dated bar and the other 42%
        (about $1.56) drifts over the following bars. Since 250 is at least 120 and below 400, the item is tagged M.

        Now read the tone. Suppose three scored items were released in the last session: a high positive item (weight
        3), a medium negative item (weight 2) and a low positive item (weight 1). The signed weight is 3 − 2 + 1 = 2 and
        the total weight is 3 + 2 + 1 = 6, so the tone is 2 ÷ 6 = +0.33, shown as a market tone of 33%. Add ten chatter
        items and the tone does not change, because chatter has weight zero, although the item count rises.

        One bar can hold several items. If a +250 item and a −130 item land in the same 5-minute bar, the chart marker
        shows their net, +120, followed by (2) for two items. A single circle on the chart can therefore hide two
        opposite stories.
        """,
        """
        **Open the newsroom.** In the right sidebar click **News**, or type `NVRA N` in the Command dialog. The panel
        is headed **Newsroom** with a **SIMULATED** badge. The group **News scope** has **All markets** and the current
        ticker. With the ticker selected you see that company's own items plus the sector and macro items that move it.

        **Read an item.** Each item shows a time, a scope tag (CO, SEC, ECO or MKT), the ticker if there is one, an
        impact letter (H, M, L or a dot), the headline, its source and category, and a score such as "+250 pts" or
        "0 pts". Hover the score for the arithmetic: one point is one basis point, 58% of it on this bar and the rest
        drifting.

        **Read the gauges.** The gauges **Session** (the last 390 bars) and **5 sessions** (the last 1,950) run from −1
        to +1 and read 0.00 when nothing has been released. Under them the text reads "N items this session · P positive
        · Q negative · R neutral · market tone X%". The scope buttons change the two gauges and the item counts, while
        the market tone always covers the whole market.

        **Use the headline strip.** Above the chart the **SIM NEWS** strip carries the 12 newest items. Click one to
        select its company and open the News tab.

        **See the markers.** On the chart, scored headlines appear as circles labelled with their points, for example
        "+250", or "+120 (2)" when two items fall in one bar and net to +120. Your own fills appear as arrows such as
        "BUY 10 @ 148.54". Click the newspaper icon **Mark scored headlines on the chart** to hide or show the circles.

        **Trace a move.** Step with **Next replay bar** or the **15m** jump until a new item appears for your company.
        Find its circle on the chart and compare the bar's move with the score. Remember that 58% of the modelled move
        lands on the dated bar, that noise is added to every bar, and that sector and macro items reach a company
        through loadings.

        **Check.** For one item write its scope, its impact tier, its points, the modelled percentage move (points ÷
        100) and the share on the dated bar (58%).
        """,
        """
        Try the mission [Trade what the tape actually said](/simulator?mission=read-the-tape). The link only
        preselects it: open the terminal, click the **New simulation run** icon, check that **Practice mission
        (optional)** shows "Trade what the tape actually said · VLOC", and click **Create new paper account**. Click
        the collapsed **Practice mission** bar under the toolbar to read the brief and the three objectives. VLOC is in
        your watchlist, but the terminal does not switch to a mission's company for you, so click VLOC yourself and
        select the VLOC scope in the News tab. The objectives are to make your first VLOC entry within one session
        after an item of 150 points or more on VLOC (the time must be within 390 clock minutes, and overnight does not
        count), to write a thesis on every order that names the headline, and to keep the position under 10% of opening
        equity, which is $10,000. A qualifying item can take a couple of sessions to appear, so move the clock in
        small steps and stop when one arrives. The objectives judge what you did and wrote, never your profit.
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
weight = 0
for i in range(3):
    signed = signed + weights[i] * directions[i]
    weight = weight + weights[i]
print("Signed weight:", signed)
print("Total weight:", weight)
print("Tone:", round(signed / weight, 2))
''',
        "Pick one scored headline from the News tab of a run you have advanced for a few sessions. Write its scope tag, impact letter and points, then compute its modelled percentage move and the share that lands on the dated bar. Find its circle on the chart, note the actual move of that bar, and write two reasons the bar might have moved by a different amount.",
        "For an illustrative +180 point company item tagged M, the modelled move is 180 ÷ 100 = 1.80%, and 58% of it, about 1.04%, lands on the dated bar. If the bar moved only 0.4%, noise or an opposing sector or macro item in the same bar may have offset it. If the bar moved 2.5%, noise or another item may have added to it, and the rest of the item's effect drifts over the following bars. The tag and the score tell you the size of one item, never the whole story of a bar.",
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

    add(
        "Market and limit orders: preview, reservations and the next bar",
        "Place, preview, amend and cancel a market order and a limit order, and explain why neither can fill until the next bar.",
        """
        An order is an instruction, not a trade. In the terminal it passes through states you can see: drafted on the
        ticket, previewed (nothing is committed yet), accepted (cash is reserved but nothing is owned) and filled on a
        later bar. The preview shows estimates built from the last close, while the fill uses the next bar's open. An
        order placed after bar c is first tested on bar c + 1, so acceptance never changes your holdings, and the gap
        between the two prices is the price of acting without knowing the next bar.

        A buy order reserves the estimated cost of its unfilled shares plus its unpaid commission, rounded up to the
        cent, so the same cash cannot be committed twice. If a gap makes a fill unaffordable, the order is cut back or
        rejected rather than creating debt. A market order accepts whatever the next bar offers, with slippage and half
        the spread against you. A limit order names the worst price you will accept. It fills at the open if the open is
        already at or better than the limit, and otherwise only if the price trades strictly through the limit. A touch
        alone is not enough, because the simulator never assumes your order was first in a queue. The price of that
        caution is that a limit may never fill, and that is a result too.
        """,
        """
        Suppose the last close is 148.50 and you preview a market buy of 10 shares with the default costs. The ticket
        prices it from the last close plus friction, rounded up: 148.50 × 1.0003 = 148.54455, which rounds up to 148.55.
        The estimated value is 10 × 148.55 = $1,485.50, and with the $1 commission the estimated debit is $1,486.50.
        After you place the order, Reserved cash shows $1,486.50 and Available cash falls to $98,513.50. You own
        nothing yet.

        Now suppose the next bar opens at 148.62. The order fills at 148.62 × 1.0003 = 148.66 after rounding to the
        nearest cent. That is 10 × 148.66 = $1,486.60, plus the $1 commission, so $1,487.60 leaves your cash, which
        becomes $98,512.40, and the reservation is released. Your average cost is $1,487.60 ÷ 10 = $148.76, because
        the commission is part of what you paid. The estimate was $1.10 too low because the market opened above the last
        close.

        Compare a buy limit at 148.20 for the same 10 shares. It reserves 148.20 × 10 + $1 = $1,483.00. If the next bar
        opens at 148.45 and trades down to 148.10, the price traded strictly through the limit, so the order fills at the
        limit: friction would make it 148.24, but a buy never pays more than its limit, so the fill is 148.20 and cash
        falls to $98,517.00. If that bar had traded down only to 148.20, the limit would have been touched but not
        passed, and nothing would fill. If the bar had opened at 148.10, the order would fill at the open plus
        friction, 148.14.
        """,
        """
        **Open a ticket.** Click **Trade** in the right sidebar, or use the quick **Buy** and **Sell** buttons under the
        selected company in the **Watchlist** tab, or type `NVRA BUY` in the Command dialog. The section **Order
        ticket** shows **Buy** and **Sell** buttons, **Order type** (Market by default), **Shares** (10) and **Duration**
        (GTC).

        **Write the reason first.** Open **Trade thesis & lesson** and, in **Trade thesis**, answer the prompt "Why this
        trade? What would change your view?" in a sentence or two. **Linked lesson** offers only 0.4, 0.5, 0.7 and 0.8,
        so leave it on "No lesson".

        **Preview.** Click **Preview buy order**. The preview pauses the replay and shows Estimated notional, Estimated
        debit, Available cash / reserved, Available shares and Position after full fill. If the button is disabled, read
        the line under the ticket, for example "Enter a positive whole number of shares." or "Insufficient available
        cash, including working orders and fees."

        **Place.** Click **Place buy order**. The panel jumps to **Open orders** and the notice reads "Order accepted.
        Advance replay to observe its fill." The ticket's **Reserved cash** now shows the reservation, and **Positions**
        is still empty because nothing has filled.

        **Advance.** Click **Next replay bar**. The order fills at that bar's open plus friction. **Trade history**
        shows Filled at, Symbol, Side, Shares, Fill price, Fee and Realized P&L. The chart marks the fill, for example
        "BUY 10 @ 148.66", **Positions** lists the shares with their Average cost, and a dashed line on the chart reads
        "LONG 10 · average 148.76".

        **Place a limit order.** Change **Order type** to **Limit**, type a **Limit price**, then preview and place as
        before. The row in **Open orders** offers **Cancel**, **Edit** and **Journal**, and the chart draws a draggable
        line such as "BUY 10 · LIMIT 148.20". **Edit**, or dragging that line, opens **Confirm order amendment** with
        **New limit price** and **Confirm amendment**. **Cancel** shows "Order remainder canceled." Market orders have no
        **Edit**, because they have no price to change.

        **Choose a duration.** **DAY** orders expire at the last bar of the session, and an order placed on that last
        bar belongs to the next session. **GTC** orders keep working until they fill or you cancel them.

        **If the notice says "Unconfirmed action saved; recover it before placing another trade."** the terminal could not
        confirm that the order reached the server. Click **Reconnect & retry action**. It reloads your account and
        resends the same request, so the order can exist only once. Do not place the order again by hand.

        **Check.** Compare the Estimated debit in the preview with the cash actually spent after the fill. They differ
        because the preview prices the order from the last close and the fill uses the next open.
        """,
        """
        Try the mission [Place your first paper order](/simulator?mission=first-order). The link only preselects it:
        open the terminal, click the **New simulation run** icon, check that **Practice mission (optional)** shows
        "Place your first paper order · NVRA", and click **Create new paper account**. Decide the price you are willing
        to pay before you look at the chart again, enter a buy limit at that price, and write your reason in **Trade
        thesis**; the box is already open on mission runs. Then advance by a full session with the **1D** jump. The
        three objectives are a limit entry, a thesis on every order and a session advanced after your first order. They
        say nothing about profit, and a limit that never fills is a result too: it tells you the market did not come to
        your price.
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
        "The market buy reserves a price of ceil(96.40 × 1.0003) = 96.43, so 20 × 96.43 + $1 = $1,929.60. The limit order reserves 20 × 95.90 + $1 = $1,919.00. If the next bar opens at 96.55, the market order fills at 96.55 × 1.0003 = 96.58 and costs 20 × 96.58 + $1 = $1,932.60, which is $3.00 more than it reserved. The limit does not fill: the open is above 95.90 and the low of 96.30 never traded below it, so the order keeps working and keeps its reservation of $1,919.00.",
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
        """
        The simulator cannot see an order book or the path of prices inside a minute, so it prices a fill from
        numbers in the bar (open, high, low and volume) and from four settings you chose. Slippage and half the spread
        move a market order's price against you. Participation sets how much of the bar's volume your orders may take:
        capacity is the whole-number part of volume × participation, shared by all your orders in that symbol in the
        order they arrived, and what does not fill keeps working on later bars. The commission is charged once, on an
        order's first fill.

        These rules are cautious on purpose, and they are still simplifications. A real fill depends on queue
        position, hidden liquidity and your own market impact, none of which is modelled here. The tape and order book
        windows in lesson 13.10 are illustrations that never touch a fill. Treat the rules as a way to see why size and
        liquidity matter: a 1% cap makes a large order take several bars, while a higher participation setting makes
        fills easier than a real market is likely to give you.
        """,
        """
        Suppose you place a 600-share market buy with the default costs, and the next three bars have opens of 148.50,
        148.60 and 148.55 and volumes of 26,000, 18,000 and 22,000 shares (hypothetical numbers). Capacity is the
        whole-number part of volume × 0.01: 260, 180 and 220 shares.

        Bar one fills 260 shares at 148.50 × 1.0003, which is 148.54, and charges the $1 commission. Bar two fills 180
        at 148.60 × 1.0003 = 148.64 with no commission. Bar three has room for 220 but only 160 shares remain, so it
        fills 160 at 148.55 × 1.0003 = 148.59. The total is 260 × 148.54 + 180 × 148.64 + 160 × 148.59 = 38,620.40 +
        26,755.20 + 23,774.40 = $89,150.00, an average of 148.58 per share, plus one commission: $89,151.00.

        A second order in the same stock queues behind yours and receives only the capacity left after yours has been
        served on each bar. In this example it would get nothing on bars one and two, and up to 60 shares on bar three.
        Arrival order decides, not size or urgency.
        """,
        """
        **Make capacity visible.** Click the **New simulation run** icon. Set **Volume participation (0–1)** to 0.001, its
        minimum, and leave the other fields at their defaults. Click **Create new paper account**.

        **Read the bar's volume.** Hover the latest bar, or look at the chart header with the pointer away from the
        chart: the readout ends with "Vol …". At 0.001 the capacity is the whole-number part of Vol × 0.001, so 26,000
        shares gives 26. The bar that fills your order will have its own volume, so treat this as a guide and check the
        fill bar afterwards.

        **Place an order that is too big for one bar.** Choose a liquid company such as NVRA, open the **Trade** tab,
        enter 100 in **Shares**, keep Market and GTC, write a short reason in **Trade thesis**, then click **Preview buy
        order** and **Place buy order**.

        **Step one bar at a time.** Click **Next replay bar**. In **Open orders** the row reads BUY · market, **Shares /
        filled** shows the order's quantity and what has filled, the status reads "partially filled", and the small text
        shows how many shares remain. Repeat until the order is filled, and watch **Reserved cash** shrink as it fills.

        **Read the fills.** Open **Trade history**. Each partial fill is its own row. Only the first row carries the Fee
        of $1.00, and each Fill price is that bar's open plus 3 basis points, rounded to the cent. Hover a fill bar on
        the chart and check that the shares filled equal the whole-number part of Vol × 0.001, or the shares that
        remained, whichever is smaller.

        **Queue a second order.** Place a second market buy of 10 shares in the same symbol straight after the first,
        before advancing. On the next bar the first order takes all the capacity, so the second shows 0 filled until the
        first is complete: first in, first out.

        **Cancel the rest.** Click **Cancel** on a partly filled order. The notice reads "Order remainder canceled." Only
        the unfilled part is released, and the shares already filled stay in **Positions**.

        **Check.** The sum of the filled shares in Trade history equals the quantity less the remainder, the Fee column
        has one non-zero entry per order, and the average price is the notional divided by the shares filled.
        """,
        """
        Repeat the exercise with the default participation of 0.01 and the same 100 shares. Note that the whole order now
        fills on the first bar whenever that bar has a volume of at least 10,000 shares. Write down the Fill price, the
        Fee and the average price for each run, and explain the difference using the participation setting. Then sell the
        shares again and check that sells fill at the open minus 3 basis points. No practice mission is needed for
        this lesson, because it changes a cost setting and a free-practice run keeps the market simple.
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
        "A 500-share market sell is placed with the default costs. The next three bars open at 96.40, 96.30 and 96.50 with volumes of 12,000, 20,000 and 25,000 shares. Work out each bar's capacity, the fill sizes and prices, the average price and the proceeds after one $1 commission.",
        "Capacity is 120, 200 and 250 shares. A sell fills at the open minus 3 basis points, so the prices are 96.37, 96.27 and 96.47. Bar one fills 120, bar two fills 200 and bar three fills the remaining 180. The notional is 120 × 96.37 + 200 × 96.27 + 180 × 96.47 = 11,564.40 + 19,254.00 + 17,364.60 = $48,183.00, an average of $96.37 per share. One commission is charged, on the first fill only, so the proceeds are $48,182.00.",
        [
            (
                "With the default settings a bar trades 40,000 shares. What is the most your orders in that symbol can fill on that bar?",
                "400 shares, the whole-number part of 40,000 × 1%",
                "40,000 shares, the whole volume of the bar",
                "40 shares, which is 0.1% of the volume",
                "Capacity is the whole-number part of volume × participation, shared by all your orders in the symbol. With 1%, that is 400 shares.",
            ),
            (
                "A 300-share market buy fills 100 shares on its first bar and 200 on its second. How many $1 commissions does it pay?",
                "One, charged on the first fill",
                "Two, one for each fill",
                "Three, one for every 100 shares",
                "The flat commission is charged once per order, on its first fill. Later partial fills of the same order carry a fee of $0.00.",
            ),
            (
                "Two market buys in the same stock are open: A for 500 shares, placed first, and B for 50 shares. The next bar's capacity is 120. What do they receive?",
                "A receives 120 shares and B receives none",
                "A receives 70 shares and B receives 50, so the smaller order completes",
                "A and B each receive 60 shares, split evenly",
                "Capacity is shared first in, first out. A arrived first and can absorb all 120 shares, so B waits until A has been served or cancelled.",
            ),
            (
                "A learner raises Volume participation from 0.01 to 1 so that every order fills at once. Which comment is most accurate?",
                "Fills become easier than a real market is likely to allow, so results will look better for a reason that will not repeat",
                "The change is harmless, because participation only affects the commission",
                "The change makes the whole simulated market more liquid for every other participant",
                "Participation is a limit on how much of a bar your orders can take. Raising it to the maximum removes a realistic constraint and flatters results.",
            ),
        ],
        [EXECUTING, BID_ASK, ORDER_BULLETIN],
        (7, 15, 8),
    )

    add(
        "Stops, trailing stops and attached exits",
        "Place stop, stop-limit, trailing-stop and attached-exit orders, and predict how each behaves when a price gaps.",
        """
        A stop order is a trigger, not a price. A sell stop waits until a bar trades at or below the stop price and then
        becomes a sell at the market, so when a bar opens below the stop the fill comes at that worse open. A stop-limit
        triggers in the same way but then needs a later bar inside its limit, so it can protect the price and still leave
        you holding the shares. A trailing stop, offered for sells only, starts from the close when you place it and sits
        a percentage below it; after each bar it moves up to follow the new high, and it never moves down.

        Attached exits let a buy carry its own plan out. Ticking **Attach exits to this entry** adds a take-profit above
        the entry, a stop-loss below it, or a trailing stop instead of the stop-loss. The exits wait, holding nothing in
        reserve, until the entry fills, then cover exactly the shares that filled. They are one-cancels-other: when one
        trades, the other shrinks or is cancelled. If a single bar reaches both, the terminal takes the stop first,
        because it cannot see the order of prices inside the bar and refuses to assume the flattering one.
        """,
        """
        You hold 10 shares and place a sell stop at 145.00 with the default 3 basis points of friction. The next bar
        opens at 146.10 and trades down to 144.80, which triggers the stop. The fill is the lower of the open and the
        stop, 145.00, less 3 basis points: 145.00 × 0.9997 = 144.9565, which rounds to 144.96.

        Now suppose bad news arrives overnight and the next bar opens at 142.00. The stop is still triggered, but the
        fill is the lower price, 142.00 × 0.9997 = 141.9574, which rounds to 141.96. That is 3.04 below your stop, or
        $30.40 on 10 shares. A stop decides when an exit is attempted, not the price it receives.

        A 5% trailing stop placed when the close is 150.00 starts at 150.00 × 0.95 = 142.50. The next bar trades
        between 149.00 and 153.00. It is tested against 142.50 and does not trigger, then the anchor rises to the 153.00
        high and the stop becomes 145.35. When the following bar opens at 146.00 and dips to 144.90, it triggers at
        145.35 and fills at 145.35 × 0.9997, rounded to 145.31.
        """,
        """
        **Protect shares you own.** Buy 10 shares of any company and advance one bar so that they fill. Open the
        **Trade** tab, click **Sell**, choose **Stop** in **Order type**, type a price below the last trade in **Stop
        price**, keep **Duration** at GTC and write why the stop sits there in **Trade thesis**. Click **Preview sell
        order**, read the estimates and click **Place sell order**. The working order draws a line on the chart that you
        can drag to a new price; dragging opens **Confirm order amendment**, where **Confirm amendment** applies it.

        **Compare a stop-limit.** Place a second sell with **Order type** Stop-limit and both **Stop price** and
        **Limit price** filled in. Note in your notebook that after it triggers it can fill only on a later bar, and only
        at your limit or better.

        **Use a trailing stop.** Choose **Trailing stop**, which appears for sells, and enter a percentage in **Trail (%
        below the high)** between 0.25 and 50. Advance a few bars with **Next replay bar** and watch the order's stop
        rise as new highs print.

        **Attach exits to an entry.** On a **Buy** ticket with Market or Limit, tick **Attach exits to this entry** and
        fill **Take profit** and **Stop loss**, or **Or trail the stop (%)** instead of the stop loss. The ticket shows
        "Risking $X to make $Y · R:1". A take-profit below the entry or a stop-loss above it is refused with "A
        take-profit has to sit above the entry it protects." or "A stop-loss has to sit below the entry it protects."
        In **Open orders** the legs show only a **Journal** button until the entry fills, and cancelling the entry
        cancels them.

        **Check.** In **Trade history**, a triggered stop's **Fill price** is never above the lower of the bar's open and
        the stop, less friction. A stop-limit that triggered on a bar has no fill on that same bar.
        """,
        """
        Try the mission [Protect a position before you need to](/simulator?mission=stop-discipline). No other lesson
        links it, so start it here: open the terminal, click the **New simulation run** icon, check that **Practice
        mission (optional)** shows "Protect a position before you need to · QBIT", and click **Create new paper
        account**. QBIT is not in the default watchlist, so click the symbol button, type QBIT and press Enter. Open a
        position, then place a protective sell stop while the price is still calm, writing a reason on every order. If
        you use attached exits, open **Journal** on each exit leg and write its reason too, then confirm in the mission
        panel that the thesis objective is met.
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
        "In the first case the bar trades through 95.00, so the fill is the lower of the open and the stop, 95.00, less 3 basis points: 95.00 × 0.9997 = 94.97 after rounding, a loss of (97.40 − 94.97) × 20 = $48.60 before commissions. In the second case the open is below the stop, so the fill is 93.50 × 0.9997 = 93.47, a loss of $78.60. A stop-limit at 95.00 / 94.90 would trigger on the gap bar but could only fill on a later bar at 94.90 or better, so if prices stayed lower it would leave all 20 shares unsold.",
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
        """
        A margin account lets you sell shares you do not own. You borrow them, sell them now, and must buy them back
        later; if the price rises in between, the loss has no ceiling, because a price has no upper limit. In the
        terminal a margin account is chosen when the run is created, with **Account type** set to "Margin · may sell
        short". Practice missions always use cash accounts so that every attempt meets the same rules.

        Three numbers govern the account. Buying power is twice equity less gross exposure, never below zero, and a short
        uses it at the full value of the shares borrowed, just like a purchase of the same size. Borrowed shares cost a
        fee of 5% a year, charged once per session as its own line in **Account history**. When equity falls below 30%
        of gross exposure, the terminal buys the short back with a real order that queues like any other. Buying back
        borrowed shares is never refused for lack of cash, because closing a short reduces risk. Dividends are not
        modelled, which a real short seller would have to pay.
        """,
        """
        Start a margin run with $100,000 and sell short 600 shares at a fill of 150.00, ignoring fees. The sale adds
        $90,000, so cash is $190,000, while you owe 600 shares worth $90,000. Equity is 190,000 − 90,000 = $100,000,
        gross exposure is $90,000 and buying power is 2 × 100,000 − 90,000 = $110,000.

        If the price rises to 200.00, the shares you owe are worth $120,000. Equity falls to 190,000 − 120,000 =
        $70,000, gross exposure is $120,000 and buying power shrinks to 2 × 70,000 − 120,000 = $20,000. The buy-in
        comes when equity is below 30% of gross: 190,000 − 600P < 0.3 × 600P, so P must exceed 190,000 ÷ 780 = 243.59,
        a rise of about 62% from the short price.

        While the position is open, the borrow fee at a price of 150.00 is 90,000 × 0.05 ÷ 252 ≈ $17.86 per session, or
        about $89.29 over a five-session week if the price does not move.
        """,
        """
        **Create a margin run.** Click the **New simulation run** icon, leave **Practice mission (optional)** on "No
        mission · free practice", set **Account type** to "Margin · may sell short" and click **Create new paper
        account**. Read the help text under **Account type** rather than the small print at the foot of the dialog. The
        account bar now shows **MARGIN**, **Buying power** and **Gross** next to **Equity** and **Cash**.

        **Sell short.** Choose a company you do not own, open the **Trade** tab and click **Sell**. Enter a small
        quantity in **Shares**, keep Market and GTC, and write why you expect the price to fall in **Trade thesis**. The
        preview shows **Buying power** where a cash account shows available cash. Click **Preview sell order** and then
        **Place sell order**, and advance one bar.

        **Watch the numbers.** After the fill, check that **Cash** rose by the proceeds less the commission and that
        **Gross** shows the value of the borrowed shares. Advance by a session with the **1D** jump, then open **Account
        history** and find the line "Stock borrow fee on short positions".

        **Cover.** In **Positions**, click **Close** on the short. It prefills a **Buy** ticket for the full quantity;
        preview and place it, then advance one bar.

        **Check.** Your realized result is the sale proceeds less the purchase cost, the two commissions and every borrow
        fee line, and the borrow fee lines match the formula above for the prices at which they were charged.
        """,
        """
        There is no practice mission for this lesson, because missions use cash accounts. In a free margin run, short
        100 shares of a calm company and record the fill, the buying power before and after, and each session's borrow
        fee for a week. Compute the buy-in price for your position with the formula in this lesson, and write down what
        you would do long before the price got near it. Then cover, and compare the total borrow fee with your estimate.
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
        "The sale raises cash to 50,000 + 24,000 = $74,000. At 120.00 equity is 74,000 − 24,000 = $50,000, gross is $24,000 and buying power is 2 × 50,000 − 24,000 = $76,000. At 150.00 the shares owed are worth $30,000, so equity is $44,000, gross is $30,000 and buying power is $58,000. A buy-in begins when 74,000 − 200P < 0.3 × 200P, so P > 74,000 ÷ 260 = 284.62. One session's borrow fee at 120.00 is 24,000 × 0.05 ÷ 252 ≈ $4.76.",
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
    add(
        "Company accounts, consensus and the earnings calendar",
        "Read a fictional company's statements, ratios, consensus and reporting date, and compute a surprise and a trailing P/E without hindsight.",
        """
        Every fictional company has generated quarterly accounts that tie together: equity is assets less liabilities,
        and each quarter's closing cash equals the previous cash plus that quarter's operating, investing and financing
        flows. A company that would run short of cash borrows the difference, so short-term debt and external financing
        tell you when a business needed help. Before a print you can see only the expectation: the quarter's label, its
        date and the published consensus. The reported figures leave the server only once the clock reaches the bar that
        prints them.

        Prints land at a session open, so the result arrives with the price gap it causes. The ratios are computed from
        quarters already reported and the current price, and a ratio whose denominator is zero or negative shows "—"
        rather than a misleading number. Five companies are development-stage businesses that lose money and are valued
        on sales, so their P/E is "—" by design. Nothing in these accounts describes a real company.
        """,
        """
        A company's consensus EPS for the quarter is $1.20 and it reports $1.26. The surprise, stated as a distance, is
        1.26 − 1.20 = +$0.06; as a share of consensus that is 0.06 ÷ 1.20 = 5.0%. Its last four quarters, including this
        one, are $1.10, $1.15, $1.18 and $1.26, so trailing EPS is $4.69. At a price of 148.50 the trailing P/E is
        148.50 ÷ 4.69 ≈ 31.66.

        The quarter's net income is $26.0 million but operating cash flow is only $18.5 million, so cash conversion is
        18.5 ÷ 26.0 ≈ 71%. If short-term debt also rose, the beat leaned partly on borrowing. All of these figures are
        illustrative; your run will show different ones.
        """,
        """
        **Open the accounts.** Click the symbol button and type `NVRA FA`, then press Enter; Enter works even though the
        dialog says "No matching stock is available in this run." for the combined text. The **Company** tab opens with
        the badge "SIMULATED" and either "Next report …" with consensus or "… reported" with the surprise.

        **Read the statements.** In the **Statements** group, start with **Ratios**: the groups are Valuation,
        Profitability, Growth & distribution, Balance sheet and Value screens. Then open **Income statement**, **Balance
        sheet** and **Cash flow**. Compare net income with operating cash flow, and look for rising short-term debt or
        external financing. **Peers** lists the sector's other companies with a **Sector median** row.

        **Find the date.** Open the **Calendar** tab. **Company results** shows When, Symbol, Period, Consensus EPS and
        Reported; before the print, Reported reads "in N bars", and Consensus EPS may read "not yet set" until it is
        published. **Economic releases** lists the macro calendar, marked "Scheduled" until each item is released.

        **Watch a print.** Write your expectation in your notebook, then advance with the **1D** jump until Reported
        changes to the EPS figure with its surprise in brackets. Look at the opening bar of that session on the chart.

        **Check.** Recompute the surprise from the published consensus and the reported EPS, and the trailing P/E from
        the last four reported quarters and the price, and compare them with the terminal.
        """,
        """
        Try the mission [Hold a company through its results](/simulator?mission=earnings-gap). The link only preselects
        it: open the terminal, click the **New simulation run** icon, check that **Practice mission (optional)** shows
        "Hold a company through its results · NVRA", and click **Create new paper account**. NVRA's print falls at the
        open of Day 5. Read the accounts and consensus first, write what you expect and why in **Trade thesis**, hold at
        least 25 shares into the print, and stay for the session after it. The mission judges the order of these steps,
        not whether the result made money.
        """,
        r"\text{surprise}=\text{EPS}_{\text{reported}}-\text{EPS}_{\text{consensus}},\qquad P/E=\frac{P}{\sum_{k=0}^{3}\text{EPS}_{t-k}}",
        '''
consensus = 1.20
reported = 1.26
surprise = reported - consensus
print("Surprise:", round(surprise, 2), "or", round(surprise / consensus * 100, 1), "% of consensus")
last_four = [1.10, 1.15, 1.18, 1.26]
trailing = 0
for eps in last_four:
    trailing = trailing + eps
print("Trailing EPS:", round(trailing, 2))
print("Trailing P/E at 148.50:", round(148.50 / trailing, 2))
net_income = 26.0
operating_cash = 18.5
print("Cash conversion:", round(operating_cash / net_income * 100, 1), "%")
''',
        "Pick a company in your run before its print. Record consensus EPS and revenue, the last four reported EPS figures, the price and operating cash flow against net income for the latest quarter. After the print, compute the surprise and the new trailing P/E, and describe the opening gap.",
        "A complete answer records the published expectation before the print and the reported figures after it, so nothing depends on hindsight. The surprise is reported EPS minus consensus EPS, stated as a distance (and optionally as a share of consensus). The trailing P/E divides the current price by the sum of the last four reported EPS figures; if that sum is zero or negative the ratio is undefined, as the terminal's '—' shows. A good answer also compares cash flow with net income, notes any new short-term debt, and treats the gap as one observation from a simulated market, not a rule.",
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
        """
        The **Desk** tab carries the badge "API CALCULATED": every figure on it is computed on the server from bars the
        clock has already reached, never from the future. The quant sheet for the selected company lists Last, SMA 20,
        SMA 50, EMA 20, RSI 14, MACD hist., Volatility (ann.), Beta, Correlation, Session move, Since open and Relative
        volume, and the lists below rank Top gainers, Top losers, Most active and Sectors.

        Monitor windows split the chart area into two or three panes, each showing a tool: Time & sales, Order book,
        Heat map, Screener, Sessions, Quotes or News. The tape in Time & sales is invented, but it is constrained by each
        bar: it opens at the open, closes at the close, touches the high and the low and its sizes add up to the volume.
        The order book shows indicative size at the run's spread. Neither ever affects a fill. The Screener offers named
        screens such as Oversold (RSI under 30) rather than adjustable thresholds, because a screen chosen in advance is a
        hypothesis, while a threshold tuned after seeing the winners simply fits the answer.
        """,
        """
        RSI compares average gains with average losses over 14 bars. With an average gain of 0.60 and an average loss of
        0.40, the ratio is 1.5 and RSI = 100 − 100 ÷ (1 + 1.5) = 60, comfortably between the Oversold (30) and Overbought
        (70) screens. A company trading 2,400,000 shares when its average is 1,600,000 has a relative volume of 1.5.

        Suppose you run the Oversold screen for several sessions and 9 of the 16 names it listed rose the next session,
        while 17 of 32 names in the Whole listing rose. That is 56% against 53%, a gap of three points on very few
        observations: not yet evidence that the screen picks winners. These numbers are illustrative.
        """,
        """
        **Read the desk.** Open the **Desk** tab in the right sidebar. Check the quant sheet for the selected company and
        click a name in **Top gainers** to select it everywhere in the terminal.

        **Split the chart.** In the replay bar's **Monitor windows** group, click **2** or **3**. Each new window has a
        select **Tool for monitor 2** or **Tool for monitor 3**; the defaults are Time & sales and Heat map. Windows are
        hidden when the screen is 900 pixels wide or less.

        **Read the tape.** With Time & sales showing, advance one bar. Its summary reads "N prints · M shares · X% lifted
        the offer"; check that the prints start at the bar's open and end at its close. Then switch the window to
        **Order book** and note that it shows indicative size, not a queue you can join.

        **Run a screen.** Set a window to **Screener** and choose a screen in **Screen**: Trending up, Oversold,
        Overbought, Unusual volume, Low earnings multiple, Widest ranges or Whole listing. The columns are Symbol, Last,
        Chg, RSI, Rel vol, P/E and Vol. Write your prediction for the listed names before you advance.

        **Check.** Click a symbol in any tool and confirm that the chart and ticket switch to it; then compare the RSI in
        the Screener with the quant sheet's RSI 14 for the same company.
        """,
        """
        There is no mission for this lesson. Choose one named screen, write down your prediction for its names, and
        advance one session at a time for at least ten sessions. Record how many of its names rose and how many in the
        Whole listing rose, and keep the screen unchanged throughout. At the end, decide whether the difference is large
        enough, over enough observations, to mean anything.
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
        "A good answer fixes the screen before the first session and keeps it unchanged, records the prediction before each advance, and reports both hit rates with their counts. With a few dozen observations in a generated market, a difference of a few percentage points is well within what chance alone produces, so the honest conclusion is usually that the screen is untested rather than proven. Tuning the RSI threshold after seeing which names rose would make the hit rate look better by construction and is not evidence.",
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
        """
        The **Performance** tab marks your account on every observed bar and compares it with the QX-200, an
        equal-weighted index of every company in the run rebased to the bar your account opened on. Measuring against the
        market rather than against zero separates what the market did from what your decisions added. Beta and alpha
        describe that split, and Sharpe, Sortino, Calmar, CAGR, daily VaR and CVaR come from session closes at 252
        sessions a year. Below 20 closed sessions the panel warns that annualizing so few returns "produces a number, not
        a measurement".

        The trade statistics are simple counts you can check: a closing trade is a fill that realized a gain or a loss,
        win rate is winning closing trades divided by all closing trades, and profit factor is gross wins divided by gross
        losses ("—" when there is no loss). Your journal, the thesis written on each order and its fills, is the other
        half of a review: it records what you expected before you knew the outcome. Exports keep both. CSV cells that
        start with =, +, − or @ gain an apostrophe so that a spreadsheet cannot run them as formulas.
        """,
        """
        Four closing trades realize +$120, +$80, −$50 and −$150. Two of four won, so the win rate is 50%. Gross wins are
        $200 and gross losses are $200, so the profit factor is 200 ÷ 200 = 1.00: the account broke even on its closed
        trades. The average win is $100 and the average loss is −$100.

        The equity path runs $100,000, $101,200, $99,800 and $100,600. The deepest fall from a peak is 101,200 − 99,800
        = $1,400, a maximum drawdown of 1,400 ÷ 101,200 ≈ 1.38%. If the account returned +0.6% while the QX-200 returned
        +0.9%, the excess return is −0.3 percentage points: the market did better than your choices over the same bars.
        """,
        """
        **Read performance.** Open the **Performance** tab in the bottom panel. Note **Equity**, **Total return**, **Max
        drawdown**, **Realized P&L** and **Unrealized P&L**, then **Closing trades**, **Win rate**, **Profit factor**,
        **Average win**, **Average loss**, **Average exposure**, **Bars observed** and **Sessions**. The chart **Equity
        path vs QX-200** sets your account against the benchmark, with **Your return**, **QX-200 return**, **Excess
        return**, **Beta** and **Alpha (annualized)** beside it. **Attribution by company** shows where results came
        from.

        **Journal an order.** In **Open orders**, **Order history** or **Trade history**, click **Journal** on a row. The
        **Trade journal** dialog has **Trade thesis** and **Linked lesson**; write what you expected and what would have
        changed your mind, then click **Save journal** and look for "Trade journal saved."

        **Export.** On any bottom-panel tab, click **Export table as CSV** to save it as a file such as
        quanta-open-orders.csv. For the whole run, click **Export simulation** in the status bar and choose "Run, chart
        settings & journal (JSON)".

        **Check.** Recompute win rate and profit factor from the realized P&L column of your exported trade history, and
        confirm that they match the panel.
        """,
        """
        Try the mission [Size a position you could survive](/simulator?mission=position-size). The link only preselects
        it: open the terminal, click the **New simulation run** icon, check that **Practice mission (optional)** shows
        "Size a position you could survive · ZEPH", and click **Create new paper account**. Keep every position under 5%
        of opening equity, place at least three orders and advance a full week. Then read the Performance tab, journal
        every order, export the trade history and recompute the statistics yourself.
        """,
        r"\text{win rate}=\frac{n_{\text{win}}}{n_{\text{closing}}},\qquad \text{PF}=\frac{\sum \text{wins}}{\left|\sum \text{losses}\right|},\qquad \text{excess}=R_p-R_{\text{QX-200}}",
        '''
trades = [120, 80, -50, -150]
wins = 0
gross_win = 0
gross_loss = 0
for result in trades:
    if result > 0:
        wins = wins + 1
        gross_win = gross_win + result
    if result < 0:
        gross_loss = gross_loss - result
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
        "The closing trades are the rows with a non-zero realized P&L. Win rate is the share of those rows that are positive; profit factor divides the sum of the positive results by the absolute sum of the negative ones and is undefined if there were no losses. A good comparison with the QX-200 states both returns over the same bars, the excess return, the beta, and the number of sessions, and adds that a week of a generated market is far too short to show skill. The journal entries explain whether the results followed the reasons written beforehand.",
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
        """
        A practice mission is a lesson's exercise carried into the terminal: a fixed seed, a fixed start, a named company,
        a short brief and three objectives. Everyone who attempts it meets the same market, and every objective is judged
        on the server from your orders, fills, positions and clock, never from your profit. That is deliberate. A rule
        broken profitably is still broken, and a loss taken while following your rules is not proof that the rules were
        wrong.

        The capstone mission, "Trade inside your written limits", asks you to trade a week inside the charter you wrote in
        the ethics course: every position under 5% of opening equity, a thesis on every order, and every position closed
        before you finish. A position cap is judged on the largest holding the run ever carried, so closing an oversized
        position afterwards does not undo the breach. Your review then turns the week into evidence another person could
        check: settings, sample, costs, benchmark and the limits of what the simulator models.
        """,
        """
        The 5% cap on $100,000 of opening equity is $5,000, including fees. If the next bar opens at 52.30, a market buy
        fills at 52.30 × 1.0003 = 52.31569, which rounds to 52.32. The largest whole number of shares within the cap is
        the whole-number part of (5,000 − 1) ÷ 52.32 = 95.55, so 95 shares, costing 95 × 52.32 + 1 = $4,971.40.

        A buy of 100 shares would cost 100 × 52.32 + 1 = $5,233.00 and breach the cap, even if you sold 5 shares a minute
        later. The review checklist in the worksheet has twelve items, from the seed and costs to the next experiment you
        would run; a complete review ticks all twelve.
        """,
        """
        **Start the mission.** Open [Trade inside your written limits](/simulator?mission=charter). The link only
        preselects it: click the **New simulation run** icon, check that **Practice mission (optional)** shows "Trade
        inside your written limits · MRDN", and click **Create new paper account**. The mission starts on Day 2 at
        11:19 ET in a cash account with $100,000.

        **Read the brief.** Open the **Practice mission** panel. It shows the title, "N of 3 objectives" and each
        objective with a note on how far it has come. Copy your written charter into your notebook before the first
        trade.

        **Trade the week.** Size every entry with the formula above before you preview it, write a **Trade thesis** on
        every order, and add a **Journal** entry on any order you placed without one. Advance through the week with the
        **1D** jump or the **1W** jump, which moves 1,950 bars.

        **Finish flat.** Close every position with **Close** in **Positions**, preview and place each order, and advance
        until they fill. The panel reads "All objectives met" only when no shares remain after a full week since your
        first order.

        **Deliver the review.** Click **Export simulation** and choose "Run, chart settings & journal (JSON)". Then
        write the review using the twelve items in the worksheet.

        **Check.** Every objective is met, the exported journal contains a thesis for every order, and your review states
        what the simulator does not model: dividends, queue position, market impact and real borrow availability.
        """,
        """
        This lesson is the mission. When it is complete, give your review to someone who did not trade the week and ask
        them to recompute one number from your export, such as the largest position's peak cost or the profit factor. A
        review is finished when another person can check it without asking you anything.
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
