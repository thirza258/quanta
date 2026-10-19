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

PARTS = [
    (
        "Ownership & Financial Foundations",
        "Understand capital, distinguish saving and investing from short-term trading, and explore what owning a share of common equity really means.",
    ),
    (
        "Market Structure & Order Mechanics",
        "Trace how orders move through brokers and exchanges, read bid-ask quotes, and choose the right order type for your objective.",
    ),
    (
        "Returns, Costs & Financial Analysis",
        "Calculate real net returns and compounding effects, and learn how to read financial statements to evaluate a business before buying.",
    ),
    (
        "Risk Controls & Trading Plan Design",
        "Protect capital through diversification and position sizing, avoid cognitive traps, and build your first structured paper-trading plan.",
    ),
]


def build_foundations():
    modules = []

    def lesson(part, title, subtitle, objective, content, formula, code, practice, terms, source):
        lesson_id = f"0.{len(modules) + 1}"
        modules.append(
            {
                "id": lesson_id,
                "part": part,
                "title": title,
                "subtitle": subtitle,
                "minutes": 15,
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
        "1",
        "What investing and trading mean",
        "Start with goals, time horizons, and uncertainty",
        "Distinguish saving, investing, and trading; calculate a simple return and explain why a profit is uncertain.",
        r"""
## The idea

Every journey in financial markets begins with understanding the purpose of your money. Money can serve different functions depending on your life goals and when you will need it:

- **Saving**: Setting cash aside in low-risk, highly liquid accounts (such as insured bank deposits or short-term treasury bills) primarily to preserve your capital for emergency reserves or near-term expenses. Returns are modest, but the risk of losing principal is very low.
- **Investing**: Committing capital to productive assets (such as shares of growing businesses, index funds, or real estate) over longer time horizons—often years or decades. The goal is to participate in economic growth, corporate earnings expansion, and compounding wealth. An investor accepts temporary price fluctuations and market uncertainty in exchange for higher expected long-term returns.
- **Trading**: Actively buying and selling assets over shorter time horizons (weeks, days, or even minutes) seeking to profit from price fluctuations, technical momentum, or temporary market imbalances.

Their boundaries frequently overlap in practice: an investor still executes trades to enter or exit an investment, and a short-term trader must manage downside risk just like an investor. The key differences lie in your **purpose**, your **holding period (time horizon)**, and the **evidence** you rely on to make each decision.

A long-term investor might study a company's business model, competitive moat, and multi-year cash flow generation. A short-term trader might study daily price patterns, trading volume, or immediate order imbalances. Neither approach guarantees a profit, and neither eliminates market risk. Before putting any money at risk, always ask four foundational questions:
1. **What am I buying?** (Do I understand the underlying asset?)
2. **Why should it pay me?** (What is the economic thesis or catalyst for value creation?)
3. **When might I need this money?** (What is my time horizon?)
4. **How could I lose it, and how much can I afford to lose?** (What is the downside risk?)

## A worked example

Maya spends $200 on a fictional investment and later receives $220 when she sells it. Ignoring costs and distributions, the gain is $20 and the return is $20 / $200 = 10%. If the sale brings $170 instead, the return is −15%. A hoped-for 10% return is an expectation, not money already earned.

$$R = \frac{\text{ending value} - \text{starting value}}{\text{starting value}}$$

Always state the time period alongside any return figure. A 10% return earned over one month represents an annualized pace of over 200%, whereas a 10% return earned over five years is less than 2% per year. Comparing investments meaningfully requires evaluating them over matching time horizons and accounting for all transaction costs and fees before deciding which actually performed better.

## Build a thoughtful decision before taking a position

Disciplined investing requires writing down your plan before committing capital. Write down your specific goal, your intended time horizon, the core thesis supporting your investment, and—most importantly—the specific invalidating condition that would prove your thesis wrong. Money that you will need in the near future (e.g., for rent, tuition, or living expenses) cannot afford to be exposed to short-term market drawdowns, because you may be forced to sell at the worst possible time.

Be vigilant against unrealistic claims: any promise of "guaranteed high returns with zero risk" is a classic hallmark of financial fraud or extreme concealed leverage. In legitimate markets, risk and return are inseparable: higher potential returns always demand accepting greater uncertainty and downside risk.

For this course, you will use hypothetical paper money in a risk-free learning sandbox. No brokerage account, real funds, or prior coding experience are required. Clear thinking, basic arithmetic, and the ability to explain your reasoning in plain words are all you need. The accompanying Python code example lets you experiment with the arithmetic interactively; its synthetic trading rule is an illustrative code demonstration, not a live strategy recommendation.

## Connect to later courses

This distinction between price and underlying value forms the core of classical security analysis in the Graham & Dodd curriculum. Later tracks in statistical foundations will teach you how to quantify uncertainty rigorously, so you never mistake a string of lucky trades for repeatable skill.
""",
        r"R=(V_1-V_0)/V_0",
        'initial = 200\nending = 220\nprint("Simple return (%):", round((ending / initial - 1) * 100, 2))\n',
        [
            question(
                "An investment rises from $200 to $220 before costs. What is its return?",
                ["20%", "10%", "2%"],
                1,
                "The $20 dollar gain divided by the original $200 starting value is 0.10, which equals 10%.",
            ),
            question(
                "Which statement best distinguishes investing from short-term trading?",
                [
                    "Investors cannot lose money",
                    "Trading requires no research",
                    "Their goals, holding periods, and decision evidence can differ",
                ],
                2,
                "Both investing and trading involve uncertainty and capital risk; they differ fundamentally in their intended holding periods, strategic goals, and the types of evidence used to make decisions.",
            ),
            question(
                "What is missing from the claim ‘this strategy returned 12%’?",
                [
                    "The period, costs, and risk taken",
                    "A guarantee of next year's profit",
                    "The color of the chart",
                ],
                0,
                "A raw percentage return cannot be evaluated in a vacuum. You must know the timeframe over which it was earned, what transaction costs were paid, and what downside risks were taken to achieve it.",
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
        "1",
        "Stocks, shares, and business ownership",
        "Understand what a stockholder actually owns",
        "Explain equity ownership, market capitalization, dividends, and why share price alone does not measure value.",
        r"""
## The idea

When you purchase a share of stock, you are not merely buying a flickering digital ticker symbol on a screen—you are purchasing a fractional ownership interest in an operating business.

Common stock (equity) represents a **residual claim** on the company's assets and earnings. The term "residual" means common shareholders stand last in line:
- If a company generates profits, it pays its operating costs, employee wages, taxes, and loan interest first. What remains belongs to the equity owners.
- If a company liquidates or goes bankrupt, lenders, bondholders, and suppliers must be fully repaid before common shareholders receive a single dollar. If nothing is left over, shareholders lose their entire investment.

In exchange for taking this residual risk, shareholders participate in the company's financial upside. As an owner, you can benefit from:
1. **Capital appreciation**: The market price of the shares rising as the company grows its earning power.
2. **Dividends**: Direct cash payments distributed to shareholders out of corporate profits.
3. **Voting rights**: The ability to vote on major corporate matters, such as electing the board of directors (depending on the share class).

To evaluate stock prices intelligently, you must separate three fundamental quantities that beginners frequently confuse:
- **Share price ($P$)**: The current market price to buy or sell one individual share.
- **Shares outstanding ($N$)**: The total count of shares issued by the company and held by all investors.
- **Market capitalization ($\text{Market Cap} = P \times N$)**: The total market value of all the company's common equity combined.

A common beginner mistake is assuming a stock priced at $5 is "cheap" while a stock priced at $500 is "expensive." Share price alone tells you nothing about the company's size or value without knowing how many shares exist!

## A worked example

Fictional Harbor Foods has 1,000,000 shares outstanding at $20 each. Its equity market capitalization is $20 million. Owning 100 shares means owning 100 / 1,000,000 = 0.01% of that share class, worth $2,000 at the quote. A declared $0.50 dividend per share would pay $50 on those 100 shares before taxes.

$$\text{Market capitalization} = \text{price per share}\times\text{shares outstanding}$$

Another company has 100 million shares trading at $2, so its market capitalization is $200 million. Its lower share price does not make the entire business cheaper than Harbor Foods. In fact, the total market is valuing that second business at ten times the equity value of Harbor Foods ($200 million versus $20 million)!

## Splits, dilution, and dividends

Understanding corporate actions helps you see past optical illusions in stock prices:

- **Stock splits**: In a two-for-one stock split, an investor holding 100 shares at $20 will now hold 200 shares at a theoretical price of $10. Think of it like cutting a pizza into 8 slices instead of 4: you have twice as many pieces, but the total amount of pizza has not changed. Your total investment value remains $2,000, and your percentage ownership in the business is exactly the same.
- **Share issuance and dilution**: A company can issue brand-new shares to raise capital from the market or grant equity compensation to employees. If total shares increase while your share count remains unchanged, your fractional ownership percentage declines (known as **dilution**). Dilution is not necessarily harmful if the cash raised is invested into high-return projects that grow the overall business, but it must be carefully tracked.
- **Dividends**: A dividend is a distribution of company resources, not free additional wealth created out of thin air. When a company pays a cash dividend, money leaves the company's corporate bank account and enters shareholders' accounts. All else equal, distributing that cash reduces the company's assets and market value by the exact amount paid out. Total investment return must therefore measure both share price changes and cash dividends received.

## Connect to later courses

In security analysis, you will evaluate diluted shares, enterprise value, and the priority of senior debt claims when valuing common stock. Always keep per-share metrics and company-wide totals strictly aligned.
""",
        r"M=P\times N",
        'price = 20\nshares = 1000000\nowned = 100\nprint("Market capitalization:", price * shares)\nprint("Ownership (%):", owned / shares * 100)\n',
        [
            question(
                "A company has 2 million shares at $15. What is its market capitalization?",
                ["$30 million", "$2 million", "$15 million"],
                0,
                "Multiply 2,000,000 shares by $15 per share to get $30,000,000 ($30 million) of total equity market capitalization.",
            ),
            question(
                "You own 40 shares at $50 before a two-for-one split. What is the theoretical position immediately after the split?",
                ["40 shares at $25", "80 shares at $50", "80 shares at $25"],
                2,
                "In a 2-for-1 split, your share count doubles from 40 to 80, while the theoretical price halves from $50 to $25. Your total position value remains $2,000 (80 × $25 = $2,000).",
            ),
            question(
                "Who has the residual claim after creditors and preferred claims?",
                ["Common shareholders", "Customers", "The stock exchange"],
                0,
                "Common shareholders hold the residual equity claim: they are paid only after debt holders, lenders, and preferred claims have been satisfied in full.",
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
        "2",
        "How stock markets work",
        "Meet issuers, investors, brokers, exchanges, and indexes",
        "Trace a stock transaction and distinguish the primary market, secondary market, an index, and an ETF.",
        r"""
## The idea

A stock market is an organized network that brings together capital seekers (companies) and capital providers (investors). Trading takes place across two distinct arenas:

- **The Primary Market**: Where securities are born. A private company issues new shares to the public for the first time in an Initial Public Offering (IPO), or an existing public company issues additional shares through a seasoned offering. The cash raised in the primary market flows directly into the company's treasury to fund capital investments, research, hiring, or debt repayment.
- **The Secondary Market**: Where existing securities are traded among investors. Stock exchanges (such as the New York Stock Exchange, Nasdaq, or Indonesia Stock Exchange) are secondary markets. When you buy shares through your brokerage account, you are almost always purchasing them from another investor who wishes to sell. The issuing company receives zero proceeds from secondary trades.

### The lifecycle of a market order

When you click "Buy" in your trading application, several financial institutions work together to execute and settle the trade:
1. **Your Broker**: Validates your account balance, ensures risk limits are respected, and routes your order according to regulatory rules.
2. **The Exchange / Trading Venue**: Matches your buying interest with a willing seller's offer using automated electronic limit order books.
3. **Market Makers**: Professional liquidity providers who continuously quote both bid and ask prices, ensuring there is a counterparty available even when other retail investors are not active.
4. **Clearing and Settlement**: After the trade is executed (the "fill"), a central clearinghouse reconciles both sides. During **settlement** (typically T+1 in modern equity markets—one business day after the trade date), legal ownership of the shares transfers to your account, and cash transfers to the seller.

Always distinguish between **submitting an order** (sending instructions), receiving a **fill** (execution match), and completed **settlement** (final legal transfer of money and securities).

## A worked example

Harbor Foods issues 100,000 new shares at $20, raising $2 million before offering costs. Later, Maya buys 50 existing shares from Leo for $21 each through a broker. The $1,050 secondary-market payment goes to the selling side; Harbor Foods does not receive another $1,050 in capital from that trade.

$$\text{Issue proceeds}=\text{new shares}\times\text{issue price}$$

Harbor Foods benefited from the initial $2 million raised in the primary market. In Maya and Leo's secondary trade, the shares simply changed hands between two market participants.

## Indexes, funds, and asset classes

Understanding the different vehicles available prevents costly misconceptions:

- **An Index**: A mathematical calculation that measures the price performance of a defined basket of assets according to transparent rules (e.g., the S&P 500 tracks 500 leading U.S. companies). You cannot buy an index directly because it is an abstract benchmark calculation, much like a thermometer that records temperature.
- **An Exchange-Traded Fund (ETF)**: An investment fund whose shares trade on public exchanges throughout the day, just like individual stocks. Most ETFs hold a portfolio of securities designed to replicate the return of a specific index. When you buy an ETF, you own shares in the fund itself.
- **Mutual Funds & Pooled Vehicles**: Pooled investment funds that price once per day after market close at Net Asset Value (NAV).

| Instrument | Basic economic claim | A question to ask |
| --- | --- | --- |
| Stock | Business ownership | Can the business create durable value? |
| Bond | A debt claim with contractual terms | Can the issuer meet its obligations? |
| Fund / ETF | An interest in a pooled portfolio | What does it hold, and what does it cost? |
| Derivative | A contract tied to an underlying variable | What payoff and obligations does the contract create? |

Beware of overlapping exposures: buying three different "technology funds" does not give you triple diversification if all three hold the same five mega-cap companies! Furthermore, when an index moves up 2%, it does not mean every constituent stock rose—some may have plunged while others surged.

## Connect to later courses

Benchmark comparison is essential in quantitative research: factor models evaluate whether an active strategy beats its benchmark index, while algorithmic execution courses study how order routing and venue latencies affect fill prices.
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
                "In secondary-market trading, existing shares change hands between investors. The purchase funds go to the selling investor, not to the issuing company.",
            ),
            question(
                "Which statement about an index and an ETF is correct?",
                [
                    "They are the same legal product",
                    "Every ETF is diversified across all markets",
                    "An index is a measure; an ETF is an investable fund that may track one",
                ],
                2,
                "An index is a theoretical calculation and performance benchmark. An ETF is a tradable investment fund that holds actual assets and issues shares that trade on an exchange.",
            ),
            question(
                "What does an order confirmation saying ‘submitted’ establish?",
                [
                    "The order was received, but execution still needs confirmation",
                    "Settlement is finished",
                    "Every requested share filled",
                ],
                0,
                "Order submission merely indicates that the broker received your instruction. You still need an execution fill report to confirm whether the order matched, at what price, and for how many shares.",
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
        "2",
        "Prices, quotes, and order types",
        "Read a quote and understand the trade-off between price and execution",
        "Calculate a spread, interpret OHLCV, and choose between market, limit, stop, and stop-limit orders in a hypothetical scenario.",
        r"""
## The idea

To trade effectively, you must understand how prices are quoted in financial markets. When you view a trading terminal, you see two key prices quoted simultaneously:
- **The Bid**: The highest price a buyer in the market is currently willing to pay. If you want to **sell immediately**, you trade at the Bid.
- **The Ask (or Offer)**: The lowest price a seller in the market is currently willing to accept. If you want to **buy immediately**, you trade at the Ask.
- **The Bid-Ask Spread**: The gap between the Ask and the Bid ($\text{Spread} = \text{Ask} - \text{Bid}$). This spread represents the transaction cost paid to market makers for immediate execution.

Never confuse the **last traded price** with the price you will receive on your next trade. The last traded price is a historical record of a past transaction that has already concluded. If quotes have shifted, your next trade will fill at current available market quotes.

Furthermore, quotes always specify an **available size (depth)**: a quote showing 80 shares at $50.10 only guarantees that 80 shares are available at that price. If you attempt to buy 200 shares, your order will sweep through higher price levels on the order book, resulting in **slippage**.

### Reading price bars and OHLCV data

Financial charts summarize trading activity over standard intervals (e.g., 1 minute, 1 hour, 1 day) using **OHLCV**:
- **Open**: The price of the very first trade in the interval.
- **High**: The highest price reached during the interval.
- **Low**: The lowest price reached during the interval.
- **Close**: The price of the final trade in the interval.
- **Volume**: The total number of shares traded during that interval (not the number of individual traders).

## A worked example

A fictional quote shows bid $49.90 for 100 shares and ask $50.10 for 80 shares. The spread is $0.20. A small market buy may execute near $50.10; a market sell may execute near $49.90. An immediate buy and sell of 10 shares at those prices loses $2 before fees, even if the quotes do not change. A request for 200 shares cannot assume all 200 are available at the displayed ask.

$$\text{Spread}=\text{ask}-\text{bid}$$

In this example, buying 10 shares at the ask ($50.10) costs $501.00. Immediately selling those 10 shares at the bid ($49.90) yields $499.00. That instant $2.00 round-trip loss ($0.20 per share across 10 shares) is the cost of crossing the spread.

## Selecting the right order type: Price vs. Execution certainty

Every order type forces you to make a conscious trade-off between **guaranteeing execution** and **controlling price**:

| Order | Instruction | Main trade-off |
| --- | --- | --- |
| Market | Trade at available prices | Execution price is uncertain |
| Buy limit | Buy at the limit or lower | May fill partly or not at all |
| Sell limit | Sell at the limit or higher | May fill partly or not at all |
| Stop | Activate a market order when triggered | A gap can produce a worse fill than the stop |
| Stop-limit | Activate a limit order when triggered | The limit can prevent an exit |

### Detailed mechanics:
- **Market Order**: Instructs the broker: *"Fill my order right now at whatever prices are currently available."* You get immediate execution, but you have zero protection against bad prices or slippage in fast-moving markets.
- **Limit Order**: Instructs the broker: *"Only fill my order at my specified price or better."* A Buy Limit at $50 will never execute above $50; a Sell Limit at $50 will never execute below $50. You maintain strict price control, but if the market never reaches your limit price, your order will sit unfilled.
- **Stop Order (Stop-Loss)**: Remains dormant until the market trades at or through your chosen stop price. Once triggered, it instantly converts into an ordinary **market order**. Crucial insight: stop prices are **not guaranteed execution prices**! If a stock closes at $50, experiences catastrophic overnight news, and opens tomorrow at $40, a $45 stop order will trigger and sell at $40—resulting in a severe loss.
- **Stop-Limit Order**: Converts into a **limit order** once the stop trigger is reached. It prevents selling at a disastrously low gap price, but if the stock continues to drop, your limit order will remain unfilled and your losses will continue to compound.

## Connect to later courses

In the trading simulator and paper-trading lab, you will practice placing market and limit orders under real-time market depth. In algorithmic trading courses, you will design automated order routing rules and calculate transaction cost analysis (TCA).
""",
        r"s=a-b",
        'bid = 49.90\nask = 50.10\nquantity = 10\nprint("Spread:", round(ask - bid, 2))\nprint("Round-trip spread cost:", round((ask - bid) * quantity, 2))\n',
        [
            question(
                "The bid is $24.95 and the ask is $25.05. What is the spread?",
                ["$0.05", "$0.10", "$25.00"],
                1,
                "Subtract the bid from the ask: $25.05 − $24.95 = $0.10 per share spread.",
            ),
            question(
                "You will pay at most $30 per share. Which order expresses that constraint?",
                ["A market buy", "A sell stop at $30", "A buy limit at $30"],
                2,
                "A buy limit order specifies the maximum price you are willing to pay ($30 or lower). If the market stays above $30, the order will not execute.",
            ),
            question(
                "A sell stop at $45 triggers after the market gaps to $40. What can happen?",
                [
                    "It must fill at exactly $45",
                    "It may fill near $40 or another available price",
                    "It guarantees a profit",
                ],
                1,
                "Once a stop order's trigger price is reached, it converts into a market order. If the market gapped down to $40, it will fill at the best available bid near $40, not at the $45 stop price.",
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
        "3",
        "Returns, compounding, and trading costs",
        "Measure what you keep, over the time you hold",
        "Calculate profit after fees, total return with dividends, and compounded returns; distinguish realized from unrealized gains.",
        r"""
## The idea

Evaluating financial performance requires understanding the difference between raw dollar profit and percentage return, as well as distinguishing between paper gains and cash in hand:

- **Unrealized Gain ("Paper Profit")**: An increase in the quoted market value of a position you currently hold. It reflects current mark-to-market value, but it is not locked in—a sudden market drop can wipe it out before you exit.
- **Realized Gain**: The actual profit locked in when you close the position by selling your shares.

Calculating true net return requires accounting for every cash flow: your initial purchase amount, brokerage commissions, transaction fees, cash dividends received, and exit fees.

## A worked example

Buy 10 shares at $100 and pay a $2 entry fee: the cash outlay is $1,002. Receive $10 of dividends in total. Sell all 10 shares at $110 and pay a $2 exit fee: sale proceeds are $1,098. The net gain is $1,098 + $10 − $1,002 = $106. The return on the initial cash outlay is $106 / $1,002, approximately 10.58%, before taxes.

$$R_{\text{net}}=\frac{\text{net sale proceeds}+\text{distributions}-\text{initial outlay}}{\text{initial outlay}}$$

Zero commission does not mean zero trading cost. Bid-ask spreads, execution slippage, fund management fees, financing interest on margin loans, and applicable taxes all quietly erode investment performance over time. Avoid double counting a spread already embedded in the actual fill prices.

## Returns multiply through time

Investment returns do not add together—they multiply sequentially through **compounding**.

A $100 position gains 10%, reaching $110, then loses 10%, reaching $99. The combined return is −1%, although the arithmetic average of the two period returns is zero.

$$R_{\text{combined}}=(1+r_1)(1+r_2)-1 = (1 + 0.10)(1 - 0.10) - 1 = 1.10 \times 0.90 - 1 = 0.99 - 1 = -1\%$$

### The math of asymmetric losses

This compounding dynamic creates an essential rule of financial survival: **losses hurt more than equal percentage gains help**.
- If a $100 portfolio falls 20% to $80, recovering from $80 back to $100 requires a **25% gain** ($20 / $80 = 25%), because the new capital base is smaller.
- If a portfolio suffers a 50% loss (dropping from $100 to $50), it requires a massive **100% gain** (doubling your money) just to break even!

### Understanding basis points

In professional finance, rates and fees are frequently quoted in **basis points (bps)**:
- 1 basis point = $0.01\%$ = $0.0001$ in decimal form.
- 10 basis points = $0.10\%$ = $0.001$.
- 100 basis points = $1.00\%$ = $0.01$.

Using basis points avoids confusion between percentage points and relative percent changes. For example, a 10 bp fee on a $1,000 transaction equals $\$1,000 \times 0.001 = \$1.00$.

## Connect to later courses

In statistical foundations, you will learn to annualize compound growth rates (CAGR) and compute geometric means. In systematic strategy testing, you will account for execution friction and slippage drag on portfolio equity curves.
""",
        r"R=\prod_t(1+r_t)-1",
        'outlay = 10 * 100 + 2\nproceeds = 10 * 110 - 2\ndividends = 10\nprint("Net profit:", proceeds + dividends - outlay)\nprint("Net return (%):", round((proceeds + dividends - outlay) / outlay * 100, 2))\nprint("After +10% then -10%:", 100 * 1.10 * 0.90)\n',
        [
            question(
                "$100 gains 10% and then loses 10%. What remains?",
                ["$100", "$99", "$101"],
                1,
                "$100 × 1.10 = $110, and $110 × 0.90 = $99. Returns compound multiplicatively through time, resulting in a net 1% loss.",
            ),
            question(
                "A 10 basis point fee on $1,000 is:",
                ["$10", "$100", "$1"],
                2,
                "10 basis points equals 0.10%, which is 0.001 in decimal. Multiplying $1,000 by 0.001 yields exactly $1.00.",
            ),
            question(
                "A stock's quoted price gain is $50, with $8 total fees and $5 dividends. What is the net gain before taxes?",
                ["$47", "$50", "$63"],
                0,
                "Net gain = price gain ($50) + cash dividends received ($5) − total fees ($8) = $47. Always include all cash inflows and subtract transaction costs.",
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
        "3",
        "Reading a business before buying its stock",
        "Connect financial statements, earnings, cash, and valuation",
        "Identify the three main financial statements, calculate EPS and P/E, and distinguish a low price from evidence of value.",
        r"""
## The idea

Before buying shares in a company, you need to understand how the business actually makes money, what it owns and owes, and whether it generates real cash. Public companies publish three primary financial statements:

1. **The Income Statement (The Operating Movie)**: Summarizes sales revenue, cost of goods sold, operating expenses, interest, and taxes over a specific period (such as a quarter or a year). It culminates in **Net Income**—the accounting profit belonging to common shareholders.
2. **The Balance Sheet (The Financial Snapshot)**: A picture of the company's financial condition at a single moment in time (e.g., as of December 31). It obeys the fundamental accounting equation:
   $$\text{Assets} = \text{Liabilities} + \text{Shareholders' Equity}$$
   - **Assets**: What the company owns (cash, inventory, factories, intellectual property).
   - **Liabilities**: What the company owes to creditors (bank debt, accounts payable, leases).
   - **Equity (Book Value)**: The residual book value that belongs to shareholders after all liabilities are subtracted from assets ($\text{Equity} = \text{Assets} - \text{Liabilities}$).
3. **The Cash Flow Statement (The Reality Check)**: Tracks the physical cash entering and leaving the company across three activities:
   - **Operating Activities**: Cash generated from selling goods and running core daily business.
   - **Investing Activities**: Cash spent on purchasing equipment, factories, or acquisitions.
   - **Financing Activities**: Cash raised from issuing stock or debt, and cash paid out for dividends or loan repayments.

### Crucial distinction: Accounting profit versus cash flow

Accounting profit does not equal cash in the bank! Under standard accrual accounting:
- A company records **revenue** when it delivers a product, even if the customer hasn't paid yet (recording an account receivable).
- Borrowing $5 million from a bank increases cash and liabilities, but creates zero operating profit.
- Buying a $10 million manufacturing plant consumes $10 million in cash immediately, but the expense is spread out over 20 years through depreciation.

Always check whether reported profits are backed by actual cash collected from customers.

## A worked example

Fictional Cedar Tools reports $12 million revenue, $2 million net income available to common shareholders, and 1 million weighted-average diluted shares. Earnings per share (EPS) is $2. At a $30 share price, the price-to-earnings ratio (P/E) is 15. Its balance sheet shows $15 million assets and $9 million liabilities, leaving $6 million book equity.

$$\mathrm{EPS}=\frac{\text{net income available to common}}{\text{weighted-average diluted shares}},\qquad P/E=\frac{P}{\mathrm{EPS}}$$

Suppose operating cash flow is only $0.4 million because customers have not yet paid. That does not prove fraud, but it raises a useful question about collections and working capital. A second company with a P/E of 8 may be cheaper relative to reported earnings, or those earnings may be about to decline. The multiple alone cannot decide.

## Price, value, and available evidence

- **Price versus Value**: Market price is what you pay; intrinsic value is an estimate of what the business is actually worth based on future cash flows, competitive moat, and balance sheet safety. Book equity is an accounting residual, not a guaranteed liquidation payout.
- **The P/E Ratio**: A P/E of 15 means investors are paying $15 for every $1 of annual net earnings. A low P/E might indicate a genuine bargain, or it might indicate a troubled company whose earnings are about to collapse (a "value trap").
- **Look-Ahead Bias & Filing Dates**: When evaluating past investment decisions or backtesting strategies, you must strictly respect information availability dates. A financial report for the fourth quarter ending December 31 is usually published in late February or March. Any decision made in January could not possibly have known those figures. Always verify claims using audited regulatory filings rather than promotional social media posts.

## Connect to later courses

In Track 01 (Classical value investing), you will master normalized earning power, balance sheet liquidation tests (NCAV), debt coverage ratios, and the margin of safety.
""",
        r"\mathrm{Equity}=\mathrm{Assets}-\mathrm{Liabilities}",
        'net_income = 2000000\nshares = 1000000\neps = net_income / shares\nprint("EPS:", eps)\nprint("P/E:", 30 / eps)\nprint("Book equity:", 15000000 - 9000000)\n',
        [
            question(
                "Which statement shows assets and liabilities at a particular date?",
                ["Income statement", "Balance sheet", "A price chart"],
                1,
                "The balance sheet is a point-in-time financial snapshot of assets, liabilities, and equity; the income statement and cash flow statement cover activity over a period of time.",
            ),
            question(
                "Net income available to common is $6 million, with 3 million diluted shares. At a $20 price, what is P/E?",
                ["10", "20", "60"],
                0,
                "Earnings per share (EPS) is $6M / 3M shares = $2.00. The P/E ratio is share price / EPS = $20 / $2 = 10.",
            ),
            question(
                "A December report is published in March. Can a December backtest decision use it?",
                [
                    "Yes, because December is the reporting period",
                    "Yes, if the result improves",
                    "No, it was not yet publicly available",
                ],
                2,
                "A strategy cannot act on information before it is publicly released. Using March earnings data in a December trade is look-ahead bias and invalidates the backtest.",
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
        "4",
        "Risk, diversification, and position sizing",
        "Understand what can go wrong before choosing a quantity",
        "Distinguish company and market risk; calculate a hypothetical position size and explain why stops do not cap every loss.",
        r"""
## The idea

Risk is not simply the chance of price fluctuations—it is the possibility of permanent loss of capital or outcomes that compromise your financial plan. In financial markets, risk falls into two broad categories:

- **Company-Specific (Idiosyncratic) Risk**: Hazards specific to an individual issuer—such as a failed product launch, poor management decisions, a corporate scandal, or losing a major client.
- **Market-Wide (Systematic) Risk**: Macroeconomic forces that impact nearly all businesses simultaneously—such as recessions, unexpected interest rate hikes, inflation shocks, or geopolitical crises.

**Diversification** reduces company-specific risk by spreading capital across different businesses, industries, and asset classes. However, holding multiple assets only provides protection if their returns are not highly correlated. Owning ten different semiconductor stocks does not make you diversified—if the chip sector experiences a cyclical downturn, all ten will fall together!

### Volatility versus drawdown

- **Volatility**: Measures how wildly returns fluctuate around their average over time.
- **Drawdown**: Measures the percentage decline in portfolio value from its highest peak to its lowest subsequent trough. For example, if a portfolio grows from $10,000 to a peak of $12,000 and subsequently declines to $9,000, the drawdown is $(\$12,000 - \$9,000) / \$12,000 = 25\%$.

Neither metric captures every danger: illiquid assets can show little daily price movement simply because they rarely trade, yet be nearly impossible to sell during a crisis.

## A worked example

In a paper account with $10,000, a hypothetical plan allocates $100 to the loss between a $50 entry and a $48 exit trigger. Planned risk per share is $2. Dividing $100 by $2 gives 50 shares, a $2,500 position. The $100 budget is 1% of this example account; it is an illustration, not a universal sizing recommendation.

$$q=\left\lfloor\frac{\text{planned risk budget}}{\text{entry price}-\text{planned exit price}}\right\rfloor$$

Buying 50 shares at $50 requires committing $2,500 in capital (25% of the account), but the planned risk is capped at $100 (1% of the account) assuming an orderly exit at $48.

If a gap leads to an actual $45 exit, the loss is $250 before costs, not $100. Fees and slippage also change the result. The calculation describes a planned scenario, not a maximum loss guarantee. Check the cash required as well as the planned risk; a cash account must be able to fund the purchase.

## Borrowing and short selling

- **Margin & Leverage**: Margin involves borrowing money from a broker to purchase more securities than your own cash allows. Leverage multiplies both gains and losses. For example, if you invest $1,000 of your own money and borrow $1,000 (totaling $2,000 in stock):
  - A 10% gain ($200) produces a **+20% return** on your initial $1,000 equity.
  - A 10% loss ($200) produces a **−20% loss** on your initial $1,000 equity.
  - A 50% crash wipes out **100% of your equity** ($1,000 loss), leaving you with zero while you still owe interest to the broker!
  - If your equity falls below maintenance margin requirements, the broker issues a **margin call** and will forcibly liquidate your positions at market lows.
- **Short Selling**: Borrowing shares to sell them today with the obligation to buy them back later at a hopefully lower price. Unlike buying a stock (where the maximum loss is 100% of invested capital if the price drops to zero), a short position has theoretically **unlimited risk** because a stock's price can rise indefinitely.

## Connect to later courses

Portfolio theory explores correlation matrices and optimal asset allocation. Risk management courses examine value-at-risk (VaR), expected shortfall, and automated risk breakers that halt trading bots before losses spiral.
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
                "True diversification requires spreading capital across different, non-correlated economic drivers. Holding ten companies in one narrow sector leaves you exposed to industry and market downturns.",
            ),
            question(
                "A paper plan risks $120 between a $40 entry and a $37 exit, before costs. What quantity follows from that plan?",
                ["40 shares", "120 shares", "3 shares"],
                0,
                "Risk per share is $40 − $37 = $3. Dividing the $120 risk budget by $3 gives 40 shares. Remember that overnight market gaps or slippage can exceed this planned loss.",
            ),
            question(
                "$1,000 equity plus $1,000 borrowing buys $2,000 of stock. A 10% stock decline loses what fraction of initial equity, before costs?",
                ["5%", "20%", "10%"],
                1,
                "A 10% decline on the $2,000 asset represents a $200 loss. Because the $1,000 borrowed debt remains fixed, the entire $200 loss comes out of your $1,000 equity: $200 / $1,000 = 20% loss.",
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
        "4",
        "Build your first research and trading plan",
        "Bring the fundamentals together and prepare for the advanced tracks",
        "Write a testable paper-trading plan with an entry reason, order, sizing assumptions, exit conditions, costs, and review process.",
        r"""
## The idea

A trading plan transforms vague intuition into a testable, disciplined process. Writing your plan down **before** entering a position protects you from emotional decision-making when market prices fluctuate:

- **Outcome Bias**: The dangerous habit of judging a decision exclusively by whether it made or lost money. A reckless gamble can turn a lucky profit, and a well-researched, disciplined trade can hit an unexpected loss. If you evaluate your process only by the last trade's outcome, you will adopt bad habits during bull markets and abandon sound strategies during inevitable drawdowns.
- **Confirmation Bias**: The natural psychological tendency to search for, favor, and recall information that confirms your preexisting beliefs while ignoring contradictory evidence.
- **The Disposition Effect**: The behavioral urge to sell winning trades too quickly to lock in small emotional profits, while holding onto losing trades indefinitely hoping they will bounce back to break even.

A written plan establishes an objective contract with yourself: define your entry catalyst, the invalidating evidence that would prove you wrong, your position size, your stop-loss, and your scheduled review date.

## A worked example

In a fictional $5,000 paper account, Ari studies Harbor Foods after a published report. The hypothesis is that collections will recover; the invalidating evidence is another deterioration in receivables and operating cash flow. Ari considers 10 shares using a $20 buy limit, reserving roughly $200 plus costs. If the ask stays above $20, the order can remain unfilled.

$$\text{Planned loss}=q(P_{entry}-P_{exit})$$

The plan records an illustrative $18 exit trigger, a $20 planned price loss for 10 shares, and a gap scenario: an actual $15 exit would lose $50 before costs. Ari schedules a review after the next public report. There is no guarantee that the thesis works, the order fills, or the exit matches the trigger.

## Your research note

Use **Add a note** to record your own fictional plan:

1. Asset, source, and information availability date.
2. Hypothesis, holding period, and evidence against it.
3. Entry instruction, quantity, cash required, and cost assumptions.
4. Planned exit, a worse-fill scenario, and concentration check.
5. Benchmark, review date, and the result you will record even if it fails.

Always include explicit criteria for when to walk away or wait. In financial markets, having no position is an active, valid, and often wise position when clear evidence or favorable risk-reward setups are lacking.

## Choose what to study next

Congratulations on completing trading and market fundamentals! You now possess the foundational vocabulary of shares, markets, quotes, returns, financial statements, and risk management. Choose your next learning journey based on your specific interests:

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
            "The dollar loss is $50 relative to the $500 starting investment: −$50 / $500 = −0.10, or −10%.",
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
            "An 8% return in one year represents an 8% annual rate, whereas 8% over four years is less than 2% per year. Comparing performance requires annualizing returns over matching timeframes, as well as evaluating transaction costs and risk taken.",
        ),
        (
            "0.2",
            "A firm has 4 million shares at $12. What is its equity market value?",
            ["$3 million", "$16 million", "$48 million"],
            2,
            "4 million shares multiplied by $12 per share equals $48 million of equity market capitalization. This measures market value of equity, not cash in the company's bank account.",
        ),
        (
            "0.2",
            "You keep 100 shares while total shares rise from 1,000 to 2,000 in a new issuance. Your ownership changes from:",
            ["10% to 5%", "10% to 20%", "5% to 10%"],
            0,
            "Initially 100 / 1,000 = 10%; after the new share issuance, 100 / 2,000 = 5%. The fractional ownership slice is diluted by half.",
        ),
        (
            "0.3",
            "A company sells newly issued shares to fund a factory. Which market activity is this?",
            ["An index rebalance", "A primary-market issuance", "Only a secondary-market trade"],
            1,
            "Newly issued shares raise fresh capital for the company's treasury in the primary market.",
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
            "Different fund names and tickers can hold the exact same underlying assets. True diversification requires looking through fund labels into actual portfolio holdings.",
        ),
        (
            "0.4",
            "The bid is $79.80 and ask $80.20. Buying and immediately selling 5 shares at those prices costs how much in spread alone?",
            ["$0.40", "$2.00", "$4.00"],
            1,
            "The spread is $80.20 − $79.80 = $0.40 per share. Multiplying by 5 shares gives $2.00 of round-trip spread cost.",
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
            "A triggered stop-limit converts into a limit order. If market bids have fallen below your limit price, the order cannot execute and you remain exposed to further losses.",
        ),
        (
            "0.5",
            "$200 gains 20% and then loses 25%. What is the ending value?",
            ["$190", "$200", "$180"],
            2,
            "$200 × 1.20 = $240, and $240 × 0.75 = $180. Sequential percentage returns compound multiplicatively, resulting in a net 10% loss.",
        ),
        (
            "0.5",
            "Total entry outlay is $1,005; net sale proceeds are $1,050; dividends are $20. What is the net profit before tax?",
            ["$45", "$65", "$75"],
            1,
            "Total received = $1,050 + $20 = $1,070. Subtracting the initial outlay of $1,005 yields $1,070 − $1,005 = $65 net profit.",
        ),
        (
            "0.6",
            "Assets are $90 million and liabilities $55 million. What is book equity?",
            ["$35 million", "$145 million", "$55 million"],
            0,
            "From the balance sheet identity: Equity = Assets − Liabilities = $90 million − $55 million = $35 million.",
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
            "Accounting revenue can be recognized before cash is collected. Examining the cash flow statement and receivables aging reveals whether the company is actually collecting cash from customers.",
        ),
        (
            "0.7",
            "A paper risk budget is $150 with a $30 entry and $27 planned exit. What is the illustrative quantity before costs?",
            ["5 shares", "50 shares", "150 shares"],
            1,
            "Risk per share is $30 − $27 = $3. Dividing the $150 risk budget by $3 gives 50 shares. Remember that overnight market gaps can exceed this planned loss.",
        ),
        (
            "0.7",
            "A portfolio falls from a $12,000 peak to $9,000. What is its drawdown?",
            ["25%", "33.3%", "75%"],
            0,
            "The decline is $12,000 − $9,000 = $3,000. Measured against the previous peak of $12,000, drawdown is $3,000 / $12,000 = 25%.",
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
            "Cherry-picking the top performer out of 50 trials selects for random luck and backtest overfitting. An honest report must disclose all trials and validate the strategy on fresh, out-of-sample data.",
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
            "A disciplined plan specifies invalidating conditions in advance. When disconfirming evidence appears, reassess the thesis objectively according to your written rules.",
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
        "description": "Your starting point for financial markets: master shares, market mechanics, order execution, returns, business statements, and risk management.",
        "source": "Original lessons · Investor.gov & FINRA references",
        "level": "Beginner",
        "icon": "book",
        "parts": [
            {"id": str(i), "title": t, "description": d} for i, (t, d) in enumerate(PARTS, 1)
        ],
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
