"""Original beginner course, practice questions, and transfer assessments."""


def question(prompt, options, answer, explanation):
    return dict(question=prompt, options=options, answer=answer, explanation=explanation)


STOCKS = (
    "https://www.investor.gov/introduction-investing/investing-basics/investment-products/stocks"
)
ORDERS = "https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-14"
RISK = "https://www.investor.gov/introduction-investing/getting-started/asset-allocation"
RESEARCH = "https://www.finra.org/investors/investing/investment-products/stocks/evaluating-stocks"
MARKETS = "https://www.finra.org/investors/investing/investment-products/stocks"


def build_foundations():
    modules = []

    def lesson(title, subtitle, objective, content, formula, code, practice, terms, source):
        lesson_id = f"0.{len(modules) + 1}"
        modules.append(
            {
                "id": lesson_id,
                "title": title,
                "subtitle": subtitle,
                "minutes": 12,
                "objective": objective,
                "kind": "fundamentals",
                "content": content.strip()
                + f"\n\n### Further reading\n\n[Investor education reference]({source}). Examples in this lesson use fictional companies and simplified amounts.",
                "formula": formula,
                "code": code
                + '\n# An optional, separate demonstration using synthetic prices.\ndef strategy(data):\n    return data["close"] > data["sma_50"]\n',
                "exercise": practice[0],
                "exercises": practice,
                "terms": [{"term": term, "definition": definition} for term, definition in terms],
            }
        )

    lesson(
        "What investing and trading mean",
        "Start with goals, time horizons, and uncertainty",
        "Distinguish saving, investing, and trading; calculate a simple return and explain why a profit is uncertain.",
        r"""
## The idea

Saving sets money aside for future use. Investing commits capital to an asset with an uncertain future payoff. Trading buys and sells assets in an attempt to benefit from price changes. Their boundaries overlap: an investor still trades when entering or leaving a position. The useful distinction is the purpose, holding period, and evidence behind the decision.

A long-term investor might study a business's ability to generate cash over years. A short-term trader might study an order imbalance over minutes. Neither time horizon guarantees success. Start by asking: **What am I buying, why might it pay me, when might I need the money, and how could I lose it?**

## A worked example

Maya spends $200 on a fictional investment and later receives $220 when she sells it. Ignoring costs and distributions, the gain is $20 and the return is $20 / $200 = 10%. If the sale brings $170 instead, the return is −15%. A hoped-for 10% return is an expectation, not money already earned.

$$R = \frac{\text{ending value} - \text{starting value}}{\text{starting value}}$$

Always state the time period. A 10% return over one month and a 10% return over five years are different outcomes. Compare investments over matching periods and account for costs before deciding which performed better.

## Build a decision before a position

Write a goal, a time horizon, a reason for the investment, and a condition that would invalidate that reason. Money needed soon has less time to recover from a fall. A promise of high returns with no risk is a reason to investigate the claim, not a substitute for evidence.

For this course, use hypothetical money. No brokerage account or coding experience is needed. Reading, arithmetic, and explaining your choices are enough. The optional Python example lets you change the numbers; its separate synthetic trading rule is not a recommended strategy.

## Connect to later courses

Graham & Dodd develops the distinction between price and estimated value. Statistical foundations teaches how to express uncertainty instead of treating a successful outcome as proof of skill.
""",
        r"R=(V_1-V_0)/V_0",
        'initial = 200\nending = 220\nprint("Simple return (%):", round((ending / initial - 1) * 100, 2))\n',
        [
            question(
                "An investment rises from $200 to $220 before costs. What is its return?",
                ["20%", "10%", "2%"],
                1,
                "The $20 gain divided by the $200 starting value is 0.10, or 10%.",
            ),
            question(
                "Which statement best distinguishes investing from short-term trading?",
                [
                    "Investors cannot lose money",
                    "Trading requires no research",
                    "Their goals, holding periods, and decision evidence can differ",
                ],
                2,
                "Both involve uncertain payoffs; the intended horizon and evidence differ, not the existence of risk.",
            ),
            question(
                "What is missing from the claim ‘this strategy returned 12%’?",
                [
                    "The period, costs, and risk taken",
                    "A guarantee of next year's profit",
                    "The color of the chart",
                ],
                0,
                "A return needs a time period and information about costs and risk to be meaningfully compared.",
            ),
        ],
        [
            ("Capital", "Money committed to an investment or trading activity."),
            (
                "Return",
                "Gain or loss relative to the amount initially invested, over a stated period.",
            ),
            (
                "Time horizon",
                "The intended length of time before money is needed or a position is closed.",
            ),
        ],
        STOCKS,
    )
    lesson(
        "Stocks, shares, and business ownership",
        "Understand what a stockholder actually owns",
        "Explain equity ownership, market capitalization, dividends, and why share price alone does not measure value.",
        r"""
## The idea

A share of stock is an ownership interest in a company. Common equity is a residual claim: creditors and other senior claims come first. Owners can benefit from price appreciation and dividends, but dividends are not automatic and shareholders can lose their investment. Voting rights depend on the share class.

Separate three quantities: **share price** is the market price of one share; **shares outstanding** is the number issued and held; **market capitalization** is their product. Market capitalization describes the market value of equity, not the company's cash balance or an independent estimate of what the business is worth.

## A worked example

Fictional Harbor Foods has 1,000,000 shares outstanding at $20 each. Its equity market capitalization is $20 million. Owning 100 shares means owning 100 / 1,000,000 = 0.01% of that share class, worth $2,000 at the quote. A declared $0.50 dividend per share would pay $50 on those 100 shares before taxes.

$$\text{Market capitalization} = \text{price per share}\times\text{shares outstanding}$$

Another company has 100 million shares trading at $2, so its market capitalization is $200 million. Its lower share price does not make the entire business cheaper than Harbor Foods.

## Splits and dilution

In a two-for-one stock split, 100 shares become 200; a theoretical $20 price becomes $10. The split itself leaves the $2,000 position value and ownership fraction unchanged. Real market prices may also move that day. A new share issuance is different: if your share count stays fixed while total shares increase, your ownership percentage falls. The company may receive new capital in exchange.

A dividend is a distribution of company resources, not free additional wealth. All else equal, distributing cash reduces the company's value. Later return calculations include both price changes and cash distributions.

## Connect to later courses

Security analysis uses diluted shares and the priority of claims to calculate per-share value. Keep the denominator and the company-wide amounts consistent.
""",
        r"M=P\times N",
        'price = 20\nshares = 1000000\nowned = 100\nprint("Market capitalization:", price * shares)\nprint("Ownership (%):", owned / shares * 100)\n',
        [
            question(
                "A company has 2 million shares at $15. What is its market capitalization?",
                ["$30 million", "$2 million", "$15 million"],
                0,
                "Multiply 2 million shares by $15 per share to get $30 million of equity market value.",
            ),
            question(
                "You own 40 shares at $50 before a two-for-one split. What is the theoretical position immediately after the split?",
                ["40 shares at $25", "80 shares at $50", "80 shares at $25"],
                2,
                "The share count doubles and theoretical price halves; position value remains $2,000.",
            ),
            question(
                "Who has the residual claim after creditors and preferred claims?",
                ["Common shareholders", "Customers", "The stock exchange"],
                0,
                "Common equity receives what remains after senior claims, which can be nothing.",
            ),
        ],
        [
            ("Equity", "An ownership claim on a company's residual assets and earnings."),
            ("Dividend", "A distribution declared by a company for eligible shareholders."),
            ("Market capitalization", "Share price multiplied by shares outstanding."),
            (
                "Dilution",
                "A reduction in an existing holder's ownership fraction when additional shares are issued.",
            ),
        ],
        STOCKS,
    )
    lesson(
        "How stock markets work",
        "Meet issuers, investors, brokers, exchanges, and indexes",
        "Trace a stock transaction and distinguish the primary market, secondary market, an index, and an ETF.",
        r"""
## The idea

In a primary-market offering, a company issues new securities to raise money. In the secondary market, existing securities change hands between investors. When you buy already-issued shares from another investor, your payment generally goes to that seller, not to the company.

A broker receives and routes your order. An exchange or other trading venue brings together buying and selling interest. Market makers quote prices at which they are willing to trade, subject to available size. Clearing and settlement handle the obligations after execution. A submitted order, a filled trade, and completed settlement are different stages.

Hours, settlement schedules, lot sizes, currencies, and account rules vary by market and broker. A lesson using dollar amounts does not imply those conventions apply to every exchange.

## A worked example

Harbor Foods issues 100,000 new shares at $20, raising $2 million before offering costs. Later, Maya buys 50 existing shares from Leo for $21 each through a broker. The $1,050 secondary-market payment goes to the selling side; Harbor Foods does not receive another $1,050 in capital from that trade.

## Indexes, funds, and asset classes

An index is a rules-based measure of a basket of assets. An ETF is a fund whose shares trade on a market; it may seek to track an index, pursue an active strategy, or hold a narrow exposure. You buy fund shares, not the abstract index number. Fees and tracking differences can separate fund returns from index returns.

| Instrument | Basic economic claim | A question to ask |
| --- | --- | --- |
| Stock | Business ownership | Can the business create durable value? |
| Bond | A debt claim with contractual terms | Can the issuer meet its obligations? |
| Fund / ETF | An interest in a pooled portfolio | What does it hold, and what does it cost? |
| Derivative | A contract tied to an underlying variable | What payoff and obligations does the contract create? |

Owning several funds does not necessarily create different exposures: their largest holdings may overlap. Likewise, an index moving up does not mean every constituent rose.

## Connect to later courses

Factor models use benchmarks; portfolio courses examine the exposures inside funds; execution courses distinguish an order's intent from what actually fills.
""",
        r"\text{Issue proceeds}=\text{new shares}\times\text{issue price}",
        'new_shares = 100000\nissue_price = 20\nprint("Primary issue proceeds:", new_shares * issue_price)\nprint("Secondary trade value:", 50 * 21)\n',
        [
            question(
                "You buy existing shares from another investor. Who generally receives the purchase money?",
                [
                    "The company automatically",
                    "The selling investor, through the transaction process",
                    "The index provider",
                ],
                1,
                "A secondary-market trade transfers an existing security; it does not itself issue new company capital.",
            ),
            question(
                "Which statement about an index and an ETF is correct?",
                [
                    "They are the same legal product",
                    "Every ETF is diversified across all markets",
                    "An index is a measure; an ETF is an investable fund that may track one",
                ],
                2,
                "An index describes a basket under rules. An ETF has actual holdings, fees, and a trading price.",
            ),
            question(
                "What does an order confirmation saying ‘submitted’ establish?",
                [
                    "The order was received, but execution still needs confirmation",
                    "Settlement is finished",
                    "Every requested share filled",
                ],
                0,
                "Submission is not a fill. Check execution quantity and price separately from settlement.",
            ),
        ],
        [
            ("Primary market", "Issuance of new securities to investors."),
            ("Secondary market", "Trading of already-issued securities."),
            ("Broker", "A firm that receives and handles customer trading orders."),
            ("Index", "A calculated measure of a selected basket of assets."),
            ("ETF", "An exchange-traded fund whose shares represent an interest in its portfolio."),
        ],
        MARKETS,
    )
    lesson(
        "Prices, quotes, and order types",
        "Read a quote and understand the trade-off between price and execution",
        "Calculate a spread, interpret OHLCV, and choose between market, limit, stop, and stop-limit orders in a hypothetical scenario.",
        r"""
## The idea

The **bid** is a quoted buying price and the **ask** a quoted selling price. Their difference is the spread. The last traded price is a past transaction, so it is not a promise of your next fill. Available quantity matters: a large order can consume several price levels.

OHLCV records the open, high, low, close, and traded volume for a period. A candle summarizes that period; it does not reveal the sequence of every trade. Volume is shares traded, not the number of distinct people buying.

## A worked example

A fictional quote shows bid $49.90 for 100 shares and ask $50.10 for 80 shares. The spread is $0.20. A small market buy may execute near $50.10; a market sell may execute near $49.90. An immediate buy and sell of 10 shares at those prices loses $2 before fees, even if the quotes do not change. A request for 200 shares cannot assume all 200 are available at the displayed ask.

$$\text{Spread}=\text{ask}-\text{bid}$$

## Translate an intention into an order

| Order | Instruction | Main trade-off |
| --- | --- | --- |
| Market | Trade at available prices | Execution price is uncertain |
| Buy limit | Buy at the limit or lower | May fill partly or not at all |
| Sell limit | Sell at the limit or higher | May fill partly or not at all |
| Stop | Activate a market order when triggered | A gap can produce a worse fill than the stop |
| Stop-limit | Activate a limit order when triggered | The limit can prevent an exit |

For a buy limit of $50 with the best ask at $50.10, the instruction does not permit a $50.10 fill. If the market falls to $50, a fill still depends on available quantity and priority. Trigger conventions differ by venue and broker.

## Connect to later courses

The paper-trading lab demonstrates some order mechanics using hypothetical accounts. Strategy backtests use next-open fills and configurable costs. Neither a candle touching a price nor a stop instruction guarantees a fill at that price.
""",
        r"s=a-b",
        'bid = 49.90\nask = 50.10\nquantity = 10\nprint("Spread:", round(ask - bid, 2))\nprint("Round-trip spread cost:", round((ask - bid) * quantity, 2))\n',
        [
            question(
                "The bid is $24.95 and the ask is $25.05. What is the spread?",
                ["$0.05", "$0.10", "$25.00"],
                1,
                "$25.05 minus $24.95 is a $0.10 spread.",
            ),
            question(
                "You will pay at most $30 per share. Which order expresses that constraint?",
                ["A market buy", "A sell stop at $30", "A buy limit at $30"],
                2,
                "A buy limit sets a maximum purchase price; it does not guarantee execution.",
            ),
            question(
                "A sell stop at $45 triggers after the market gaps to $40. What can happen?",
                [
                    "It must fill at exactly $45",
                    "It may fill near $40 or another available price",
                    "It guarantees a profit",
                ],
                1,
                "A triggered stop becomes a market order; the stop price is not a guaranteed execution price.",
            ),
        ],
        [
            ("Bid–ask spread", "The difference between the quoted ask and bid."),
            ("Liquidity", "The ability to trade a quantity promptly without a large price impact."),
            ("Slippage", "The difference between an expected trade price and the actual fill."),
            ("OHLCV", "Open, high, low, close, and volume for a defined interval."),
        ],
        ORDERS,
    )
    lesson(
        "Returns, compounding, and trading costs",
        "Measure what you keep, over the time you hold",
        "Calculate profit after fees, total return with dividends, and compounded returns; distinguish realized from unrealized gains.",
        r"""
## The idea

Profit in money and return in percent answer different questions. Include the purchase cost, sale proceeds, distributions, and fees. An unrealized gain is a change in the marked value of an open position. A realized gain results from closing it. Both affect your economic wealth, and an unrealized gain can disappear before a sale.

## A worked example

Buy 10 shares at $100 and pay a $2 entry fee: the cash outlay is $1,002. Receive $10 of dividends in total. Sell all 10 shares at $110 and pay a $2 exit fee: sale proceeds are $1,098. The net gain is $1,098 + $10 − $1,002 = $106. The return on the initial cash outlay is $106 / $1,002, approximately 10.58%, before taxes.

$$R_{\text{net}}=\frac{\text{net sale proceeds}+\text{distributions}-\text{initial outlay}}{\text{initial outlay}}$$

Zero commission does not mean zero trading cost. Spreads, slippage, fund expenses, financing, and applicable taxes can affect the outcome. Avoid double counting a spread already embedded in the actual fill prices.

## Returns multiply through time

A $100 position gains 10%, reaching $110, then loses 10%, reaching $99. The combined return is −1%, although the arithmetic average of the two period returns is zero.

$$R_{\text{combined}}=(1+r_1)(1+r_2)-1$$

A decline from $100 to $80 is a 20% loss. Recovering from $80 to $100 requires a 25% gain because the new denominator is smaller. A basis point is 0.01 percentage points: 10 basis points equals 0.10%, or 0.001 as a decimal multiplier. A 10 bp fee on $1,000 is $1.

## Connect to later courses

Statistical foundations develops discounting and annualization. Backtests later separate the strategy return from the benchmark and charge costs at execution. Keep the time period, units, and cash-flow assumptions visible in every comparison.
""",
        r"R=\prod_t(1+r_t)-1",
        'outlay = 10 * 100 + 2\nproceeds = 10 * 110 - 2\ndividends = 10\nprint("Net profit:", proceeds + dividends - outlay)\nprint("Net return (%):", round((proceeds + dividends - outlay) / outlay * 100, 2))\nprint("After +10% then -10%:", 100 * 1.10 * 0.90)\n',
        [
            question(
                "$100 gains 10% and then loses 10%. What remains?",
                ["$100", "$99", "$101"],
                1,
                "$100 × 1.10 × 0.90 = $99. Sequential returns compound.",
            ),
            question(
                "A 10 basis point fee on $1,000 is:",
                ["$10", "$100", "$1"],
                2,
                "10 bp = 0.10% = 0.001. Multiply $1,000 by 0.001.",
            ),
            question(
                "A stock's quoted price gain is $50, with $8 total fees and $5 dividends. What is the net gain before taxes?",
                ["$47", "$50", "$63"],
                0,
                "$50 + $5 − $8 = $47. Include distributions and subtract transaction costs.",
            ),
        ],
        [
            ("Total return", "Price change plus distributions relative to the initial investment."),
            ("Compounding", "Applying each period's return to the value left by previous periods."),
            ("Basis point", "One hundredth of a percentage point, or 0.0001 as a decimal."),
            ("Unrealized gain", "A rise in the marked value of a position that is still open."),
        ],
        MARKETS,
    )
    lesson(
        "Reading a business before buying its stock",
        "Connect financial statements, earnings, cash, and valuation",
        "Identify the three main financial statements, calculate EPS and P/E, and distinguish a low price from evidence of value.",
        r"""
## The idea

The income statement describes revenues, expenses, and profit over a period. The balance sheet is a snapshot of assets, liabilities, and equity at a date. The cash-flow statement explains movements in cash from operating, investing, and financing activities. Profit and cash flow differ because recognition and payment need not happen together.

A sale on credit can increase revenue and receivables before cash arrives. Borrowing increases cash and debt without creating sales profit. Buying equipment uses cash immediately, while its accounting expense can be spread over years. Ask what caused each change before declaring the business stronger.

## A worked example

Fictional Cedar Tools reports $12 million revenue, $2 million net income available to common shareholders, and 1 million weighted-average diluted shares. Earnings per share (EPS) is $2. At a $30 share price, the price-to-earnings ratio (P/E) is 15. Its balance sheet shows $15 million assets and $9 million liabilities, leaving $6 million book equity.

$$\mathrm{EPS}=\frac{\text{net income available to common}}{\text{weighted-average diluted shares}},\qquad P/E=\frac{P}{\mathrm{EPS}}$$

Suppose operating cash flow is only $0.4 million because customers have not yet paid. That does not prove fraud, but it raises a useful question about collections and working capital. A second company with a P/E of 8 may be cheaper relative to reported earnings, or those earnings may be about to decline. The multiple alone cannot decide.

## Price, value, and available evidence

Price is a current quote. Value is an estimate based on future cash flows, assets, and risk. Book equity is an accounting residual, not a guaranteed sale value. Compare several periods, examine debt and one-time items, and read the company's published reports.

When simulating a past decision, use only information available at that time. A December reporting period does not make a report released in March available in December. Treat a promotional post as a lead to verify, not as a financial statement.

## Connect to later courses

These distinctions prepare you for normalized earnings, net-current-asset value, senior claims, and margin of safety in Track 01.
""",
        r"\mathrm{Equity}=\mathrm{Assets}-\mathrm{Liabilities}",
        'net_income = 2000000\nshares = 1000000\neps = net_income / shares\nprint("EPS:", eps)\nprint("P/E:", 30 / eps)\nprint("Book equity:", 15000000 - 9000000)\n',
        [
            question(
                "Which statement shows assets and liabilities at a particular date?",
                ["Income statement", "Balance sheet", "A price chart"],
                1,
                "The balance sheet is a dated snapshot; income and cash-flow statements cover periods.",
            ),
            question(
                "Net income available to common is $6 million, with 3 million diluted shares. At a $20 price, what is P/E?",
                ["10", "20", "60"],
                0,
                "EPS is $6m / 3m = $2. P/E is $20 / $2 = 10.",
            ),
            question(
                "A December report is published in March. Can a December backtest decision use it?",
                [
                    "Yes, because December is the reporting period",
                    "Yes, if the result improves",
                    "No, it was not yet publicly available",
                ],
                2,
                "Availability dates, not just reporting periods, determine whether information could have been used.",
            ),
        ],
        [
            ("Balance sheet", "A statement of assets, liabilities, and equity at a date."),
            (
                "EPS",
                "Earnings available to common shareholders divided by the corresponding share count.",
            ),
            ("P/E", "Share price divided by earnings per share for a stated period."),
            ("Intrinsic value", "An estimate of economic worth under explicit assumptions."),
        ],
        RESEARCH,
    )
    lesson(
        "Risk, diversification, and position sizing",
        "Understand what can go wrong before choosing a quantity",
        "Distinguish company and market risk; calculate a hypothetical position size and explain why stops do not cap every loss.",
        r"""
## The idea

Company risk comes from a particular issuer, such as a failed product. Market risk can affect many investments together, such as a broad repricing of discount rates. Diversification spreads exposure, but correlated holdings can decline at the same time. Ten companies in one narrow industry may share much of the same risk.

Volatility describes variability in returns. Drawdown measures the decline from a previous portfolio peak. Neither alone captures every risk: an illiquid asset can have infrequent price changes and still be hard to sell. Consider liquidity, debt, concentration, and the ability to tolerate losses.

## A worked example

In a paper account with $10,000, a hypothetical plan allocates $100 to the loss between a $50 entry and a $48 exit trigger. Planned risk per share is $2. Dividing $100 by $2 gives 50 shares, a $2,500 position. The $100 budget is 1% of this example account; it is an illustration, not a universal sizing recommendation.

$$q=\left\lfloor\frac{\text{planned risk budget}}{\text{entry price}-\text{planned exit price}}\right\rfloor$$

If a gap leads to an actual $45 exit, the loss is $250 before costs, not $100. Fees and slippage also change the result. The calculation describes a planned scenario, not a maximum loss guarantee. Check the cash required as well as the planned risk; a cash account must be able to fund the purchase.

## Borrowing and short selling

Margin uses borrowed money to increase exposure. If $1,000 of your money and $1,000 of borrowing buy $2,000 of stock, a 10% stock loss removes $200, or 20% of your initial equity, before financing costs. The debt still needs to be repaid. Short selling sells borrowed shares and requires buying them back; rising prices can create losses beyond the initial proceeds. Detailed rules vary by account and market.

## Connect to later courses

Portfolio construction measures co-movement. Risk management studies drawdowns and tail losses. Bot engineering turns exposure limits and stale-price checks into explicit controls.
""",
        r"q=\lfloor B/(P_{entry}-P_{exit})\rfloor",
        'budget = 100\nentry = 50\nplanned_exit = 48\nquantity = budget // (entry - planned_exit)\nprint("Illustrative shares:", quantity)\nprint("Capital required:", quantity * entry)\nprint("Loss if filled at 45:", quantity * (entry - 45))\n',
        [
            question(
                "Does owning ten stocks from the same narrow industry remove market risk?",
                [
                    "Yes, ten always means diversified",
                    "Yes, if each ticker differs",
                    "No, the holdings can share risks and fall together",
                ],
                2,
                "Count underlying exposures, not just ticker names. Diversification does not eliminate broad market losses.",
            ),
            question(
                "A paper plan risks $120 between a $40 entry and a $37 exit, before costs. What quantity follows from that plan?",
                ["40 shares", "120 shares", "3 shares"],
                0,
                "$120 / ($40 − $37) = 40 shares. Actual losses can exceed the plan after gaps and costs.",
            ),
            question(
                "$1,000 equity plus $1,000 borrowing buys $2,000 of stock. A 10% stock decline loses what fraction of initial equity, before costs?",
                ["5%", "20%", "10%"],
                1,
                "The asset loses $200 while the debt is unchanged: $200 / $1,000 = 20%.",
            ),
        ],
        [
            ("Drawdown", "A decline from a previous peak in portfolio value."),
            ("Diversification", "Spreading investments across exposures to reduce concentration."),
            (
                "Leverage",
                "Using borrowing or contracts to create exposure larger than the capital committed.",
            ),
            (
                "Position sizing",
                "Choosing the quantity to hold given capital and explicitly stated risk assumptions.",
            ),
        ],
        RISK,
    )
    lesson(
        "Build your first research and trading plan",
        "Bring the fundamentals together and prepare for the advanced tracks",
        "Write a testable paper-trading plan with an entry reason, order, sizing assumptions, exit conditions, costs, and review process.",
        r"""
## The idea

A plan makes a decision reviewable. Write it before observing the outcome. Specify the asset and source, the reason to enter, the evidence that would invalidate the reason, the intended holding period, the order instruction, the quantity, and the expected costs. Record actual fills separately from your intention.

Avoid evaluating a plan only by whether the last trade made money. A disciplined decision can lose; a poorly supported decision can profit by chance. Keep the record of losing trials as well as winners. Compare a strategy against a relevant benchmark over the same period using the same cost conventions.

## A worked example

In a fictional $5,000 paper account, Ari studies Harbor Foods after a published report. The hypothesis is that collections will recover; the invalidating evidence is another deterioration in receivables and operating cash flow. Ari considers 10 shares using a $20 buy limit, reserving roughly $200 plus costs. If the ask stays above $20, the order can remain unfilled.

The plan records an illustrative $18 exit trigger, a $20 planned price loss for 10 shares, and a gap scenario: an actual $15 exit would lose $50 before costs. Ari schedules a review after the next public report. There is no guarantee that the thesis works, the order fills, or the exit matches the trigger.

## Your research note

Use **Add a note** to record your own fictional plan:

1. Asset, source, and information availability date.
2. Hypothesis, holding period, and evidence against it.
3. Entry instruction, quantity, cash required, and cost assumptions.
4. Planned exit, a worse-fill scenario, and concentration check.
5. Benchmark, review date, and the result you will record even if it fails.

Confirmation bias means favoring supporting evidence and overlooking contradictions. Chasing a recent gain without checking the thesis is another common error. Add an explicit reason to wait when the evidence or data is insufficient.

## Choose what to study next

| What you want to understand | Continue with |
| --- | --- |
| Business value and a margin of safety | [Classical value investing](/curriculum/security-analysis) |
| Returns, probability, and evidence | [Statistical foundations](/curriculum/statistical-foundations) |
| Exposures and portfolio risk | [Econometrics & factor models](/curriculum/econometrics) after statistics |
| Testing repeatable rules | [Systematic strategies](/curriculum/strategy-lab) after valuation and statistics |
| Reliable automated execution | [Autonomous stock bots](/curriculum/stock-bots) after strategy testing |
| Tokens and liquidity pools | [Web3 & cryptoeconomics](/curriculum/web3) after risk fundamentals |

Complete the practice questions and final exam to check your readiness. You may revisit any lesson or retake an exam; later tracks remain available for learners who already know the basics.
""",
        r"\text{Planned loss}=q(P_{entry}-P_{exit})",
        'quantity = 10\nentry = 20\nprint("Position value:", quantity * entry)\nprint("Planned price loss:", quantity * (entry - 18))\nprint("Gap scenario loss:", quantity * (entry - 15))\n',
        [
            question(
                "Which plan is easiest to evaluate honestly?",
                [
                    "Buy because the price went up yesterday",
                    "Record the thesis, invalidating evidence, order, quantity, costs, and review date",
                    "Keep only profitable trades in the journal",
                ],
                1,
                "Explicit assumptions and a complete record let you compare the decision with what actually happened.",
            ),
            question(
                "A strategy earned a profit in one backtest. What follows?",
                [
                    "It will profit in live markets",
                    "It has no risk",
                    "It needs further testing for costs, bias, and performance on new data",
                ],
                2,
                "One result may reflect luck, unrealistic execution, or information leakage. It is not proof of a durable edge.",
            ),
            question(
                "Which behavior is confirmation bias?",
                [
                    "Recording evidence that contradicts your thesis",
                    "Keeping a losing trial in the journal",
                    "Reading only sources that agree with your position",
                ],
                2,
                "Seeking only agreement prevents a fair test of the hypothesis.",
            ),
        ],
        [
            (
                "Trading plan",
                "A written decision process covering evidence, execution, risk, and review.",
            ),
            ("Benchmark", "A comparison portfolio or measure selected for a stated evaluation."),
            ("Confirmation bias", "Favoring evidence that agrees with a prior belief."),
            (
                "Backtest",
                "A simulation of a rule on past or generated observations under explicit assumptions.",
            ),
        ],
        RESEARCH,
    )

    # Fresh scenarios assess transfer; no exam question duplicates lesson practice.
    exam_questions = [
        (
            "0.1",
            "An asset bought for $500 is sold for $450 with no costs or distributions. What is the return?",
            ["−10%", "−50%", "+10%"],
            0,
            "The loss is $50 relative to $500: −50 / 500 = −10%.",
        ),
        (
            "0.1",
            "Two investments each earned 8%, one in a year and one in four years. What should you do before comparing performance?",
            [
                "Treat their performance as identical",
                "Align periods and examine costs and risk",
                "Assume the longer holding was risk-free",
            ],
            1,
            "The same percentage over different periods is not the same rate of growth. Costs and risk also matter.",
        ),
        (
            "0.2",
            "A firm has 4 million shares at $12. What is its equity market value?",
            ["$3 million", "$16 million", "$48 million"],
            2,
            "4 million × $12 = $48 million. This is market capitalization, not company cash.",
        ),
        (
            "0.2",
            "You keep 100 shares while total shares rise from 1,000 to 2,000 in a new issuance. Your ownership changes from:",
            ["10% to 5%", "10% to 20%", "5% to 10%"],
            0,
            "100 / 1,000 = 10%; 100 / 2,000 = 5%. The ownership fraction is diluted.",
        ),
        (
            "0.3",
            "A company sells newly issued shares to fund a factory. Which market activity is this?",
            ["An index rebalance", "A primary-market issuance", "Only a secondary-market trade"],
            1,
            "Newly issued shares raise capital for the issuer in the primary market.",
        ),
        (
            "0.3",
            "Two ETFs both hold mostly the same large technology companies. What should a learner conclude?",
            [
                "Two fund names guarantee diversification",
                "Their returns must exactly match",
                "Their underlying exposures overlap",
            ],
            2,
            "Different fund labels can conceal similar holdings. Examine the portfolio rather than counting fund names.",
        ),
        (
            "0.4",
            "The bid is $79.80 and ask $80.20. Buying and immediately selling 5 shares at those prices costs how much in spread alone?",
            ["$0.40", "$2.00", "$4.00"],
            1,
            "The $0.40 per-share spread multiplied by 5 shares is $2.",
        ),
        (
            "0.4",
            "A sell stop-limit triggers, but all available bids fall below its limit. What can happen?",
            [
                "The position remains unsold",
                "The limit guarantees a fill",
                "The exchange refunds the loss",
            ],
            0,
            "A triggered limit order still requires a permitted price. It can fail to execute during a decline.",
        ),
        (
            "0.5",
            "$200 gains 20% and then loses 25%. What is the ending value?",
            ["$190", "$200", "$180"],
            2,
            "$200 × 1.20 × 0.75 = $180, a combined loss of 10%.",
        ),
        (
            "0.5",
            "Total entry outlay is $1,005; net sale proceeds are $1,050; dividends are $20. What is the net profit before tax?",
            ["$45", "$65", "$75"],
            1,
            "$1,050 + $20 − $1,005 = $65. The stated outlay and proceeds already include trading costs.",
        ),
        (
            "0.6",
            "Assets are $90 million and liabilities $55 million. What is book equity?",
            ["$35 million", "$145 million", "$55 million"],
            0,
            "The accounting identity gives equity = assets − liabilities = $35 million.",
        ),
        (
            "0.6",
            "A business reports a profit while customer receivables rise and cash collection is weak. What is the best next step?",
            [
                "Assume profit equals cash",
                "Buy because its share price is low",
                "Examine working capital and the cash-flow statement",
            ],
            2,
            "Profit recognition can precede cash collection. Investigate the cause before forming a conclusion.",
        ),
        (
            "0.7",
            "A paper risk budget is $150 with a $30 entry and $27 planned exit. What is the illustrative quantity before costs?",
            ["5 shares", "50 shares", "150 shares"],
            1,
            "$150 divided by $3 per share gives 50 shares; this does not cap losses after a gap.",
        ),
        (
            "0.7",
            "A portfolio falls from a $12,000 peak to $9,000. What is its drawdown?",
            ["25%", "33.3%", "75%"],
            0,
            "The $3,000 decline is measured against the $12,000 peak: 25%.",
        ),
        (
            "0.8",
            "After trying 50 rules, a researcher reports only the best one. What is missing?",
            [
                "A more colorful chart",
                "A guarantee from the broker",
                "The trial history and evaluation on data not used to select the rule",
            ],
            2,
            "Selecting the best of many trials can select luck. Preserve all trials and use new evaluation data.",
        ),
        (
            "0.8",
            "New published evidence contradicts your written thesis. Which response best follows a research plan?",
            [
                "Ignore it until the price recovers",
                "Reassess the thesis and apply the recorded review conditions",
                "Increase size solely to recover losses",
            ],
            1,
            "A plan includes evidence that can change the decision. Reassess instead of defending the original belief.",
        ),
    ]
    checkpoint_questions = [
        (
            "0.1",
            "Which description is an expectation rather than a realized outcome?",
            [
                "I sold for a $25 loss",
                "I hope this asset earns 6% next year",
                "The purchase fee was $2",
            ],
            1,
            "A hoped-for future return is uncertain; an executed sale and paid fee are observed outcomes.",
        ),
        (
            "0.1",
            "What belongs in a decision before committing hypothetical capital?",
            [
                "A purpose, horizon, and loss scenario",
                "Only last week's winner",
                "An assumed guaranteed return",
            ],
            0,
            "An explicit purpose, horizon, and downside scenario makes the decision reviewable.",
        ),
        (
            "0.2",
            "You hold 60 shares and a company declares $0.25 per share. What distribution is due before taxes?",
            ["$240", "$60", "$15"],
            2,
            "60 × $0.25 = $15. Future dividends are not guaranteed.",
        ),
        (
            "0.2",
            "A $3 stock must be cheaper than a $30 stock. Why is this reasoning incomplete?",
            [
                "Every stock has the same share count",
                "Share count, earnings, assets, and risks differ",
                "Market capitalization is always cash",
            ],
            1,
            "Price per share alone cannot compare whole-business value or economic worth.",
        ),
        (
            "0.3",
            "Which participant generally receives a customer's order and routes it for execution?",
            ["A broker", "An index number", "A company's customers"],
            0,
            "The broker handles the customer order and its execution routing.",
        ),
        (
            "0.3",
            "An index rises 2%. Must each company in it rise 2%?",
            [
                "Yes, by definition",
                "Yes, if the index is popular",
                "No, constituents contribute different returns and weights",
            ],
            2,
            "An index aggregates its constituents under a methodology; individual returns differ.",
        ),
        (
            "0.4",
            "A candle's high is $55 and low $48. What can you infer?",
            [
                "Every trader bought at $48",
                "These were the period's extreme traded prices, not guaranteed fills",
                "The high happened before the low",
            ],
            1,
            "OHLC does not reveal every trade's order or promise execution at an extreme.",
        ),
        (
            "0.4",
            "An order requests 200 shares but only 60 execute. How should it be recorded?",
            ["As 200 filled", "As no trade", "As a partial fill of 60, with 140 unfilled"],
            2,
            "Track executed quantity independently of requested quantity.",
        ),
    ]

    def exam(exam_id, title, kind, passing, rows, module_ids):
        return {
            "id": exam_id,
            "title": title,
            "kind": kind,
            "passingScore": passing,
            "minutes": len(rows) * 2,
            "moduleIds": module_ids,
            "version": 1,
            "description": "Apply the ideas to new scenarios. Untimed, open-book, with explanations after submission and unlimited retakes.",
            "questions": [
                {"id": f"{exam_id}-q{i}", "lessonId": row[0], **question(*row[1:])}
                for i, row in enumerate(rows, 1)
            ],
        }

    return {
        "id": "trading-fundamentals",
        "number": 0,
        "title": "Trading & market fundamentals",
        "description": "Your first course: understand stocks, markets, orders, returns, and risk before exploring investment strategies.",
        "source": "Original lessons · Investor.gov & FINRA references",
        "level": "Beginner",
        "icon": "book",
        "outcomes": [
            "Explain what stocks represent and how markets connect buyers and sellers",
            "Read quotes, select order instructions, and calculate returns after costs",
            "Interpret basic financial statements and plan for risk",
            "Write a testable paper-trading plan and choose your next course",
        ],
        "modules": modules,
        "exams": [
            exam(
                "fundamentals-checkpoint",
                "Market essentials checkpoint",
                "checkpoint",
                75,
                checkpoint_questions,
                [m["id"] for m in modules[:4]],
            ),
            exam(
                "fundamentals-final",
                "Trading fundamentals final exam",
                "final",
                80,
                exam_questions,
                [m["id"] for m in modules],
            ),
        ],
    }
