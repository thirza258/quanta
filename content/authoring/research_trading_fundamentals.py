"""Research extensions for Trading & market fundamentals (0.x).

Each entry maps a lesson ID to (body, sources). A source is
(kind, authors, year, title, url, what it contributes); see research_depth.py.
"""

NOTES = {
    "0.1": (
        r"""Research on real brokerage accounts puts numbers on the difference between investing and trading. Barber and Odean followed 66,465 U.S. households at a large discount broker from 1991 to 1996. The households that traded most earned 11.4% a year while the market returned 17.9%. The average household turned over about 75% of its portfolio each year, and the authors suggest that overconfidence can explain both the heavy trading and the poor results. Every round trip pays a spread and often a commission, so an active decision has to earn those costs back before it earns anything.

Very short horizons make the arithmetic harder still. Chague, De-Losso and Giovannetti observed everyone who began day trading Brazilian equity futures between 2013 and 2015 and kept going for at least 300 days. Of those persistent traders, 97% lost money and only 0.4% earned more per day than a bank teller's starting pay; the authors found no evidence that traders improved with practice. Attention shapes short-term activity too. In a high-frequency study of Robinhood users, Ardia, Aymard and Cenesizoglu found that users favoured stocks with extreme negative moves and often bought within an hour, which looks more like a reaction to salient prices than a researched plan.

These samples come from particular markets, periods and account types, so they do not prove that every active decision is a mistake. They do explain why this course asks for a purpose, a horizon and evidence before a position. Before a practice trade, estimate its round-trip cost as a percentage of the amount invested and compare it with the move you expect. If a $200 position pays $2 in total costs, it must gain 1% just to break even, and a one-month result will rarely be long enough to tell skill from luck.""",
        [
            ("paper", "Barber & Odean", 2000, "Trading Is Hazardous to Your Wealth: The Common Stock Investment Performance of Individual Investors", "https://doi.org/10.1111/0022-1082.00226",
             "Household-level evidence that the most active traders earned far less than the market over 1991–1996."),
            ("paper", "Chague, De-Losso & Giovannetti", 2019, "Day Trading for a Living?", "https://ideas.repec.org/p/spa/wpaper/2019wpecon47.html",
             "Complete population of persistent Brazilian futures day traders; nearly all lost money and none showed learning."),
            ("arxiv", "Ardia, Aymard & Cenesizoglu", 2023, "Fast and Furious: A High-Frequency Analysis of Robinhood Users' Trading Behavior", "https://arxiv.org/abs/2307.11012",
             "Hourly data showing retail app users reacting within an hour to extreme price drops."),
        ],
    ),
    "0.2": (
        r"""The lesson's warning that a dividend is not free wealth has a formal version. Miller and Modigliani showed in 1961 that, in an idealized market without taxes, trading costs or information differences, dividend policy does not change what shares are worth. Cash paid out today lowers the value of the remaining claim by the same amount, and an investor who wanted cash could create a "homemade dividend" by selling a few shares. Real markets add taxes, costs and signals, which is why payout policy is still studied, but the benchmark explains why a share price normally falls when it starts trading without the right to a declared dividend.

Stock splits are a clean test of price versus value, because a split changes the share count and the per-share price without changing the business. Ikenberry, Rankine and Stice studied 1,275 two-for-one splits and reported a 3.38% return around the announcement followed by excess returns of 7.93% in the first year. Their interpretation is that managers choose to split when they expect good performance, so the decision carries information even though the arithmetic carries none. Byun and Rozeff later examined 12,747 splits from 1927 to 1996 with different benchmark methods. Splits of 25% or more showed no long-run performance significantly different from zero, and the authors concluded that the evidence against market efficiency is neither pervasive nor compelling.

Two habits follow. First, keep the arithmetic and the signal apart: a split does not create value, but the choice to split may reveal what managers believe. Second, treat a published pattern as provisional until you know how it was measured, because another team with a different sample or benchmark can reach the opposite conclusion. When you read that a stock "rose after its split", ask what it was compared with and over which period.""",
        [
            ("paper", "Miller & Modigliani", 1961, "Dividend Policy, Growth, and the Valuation of Shares", "https://doi.org/10.1086/294442",
             "The benchmark result that, without frictions, payout policy does not change shareholder value."),
            ("paper", "Ikenberry, Rankine & Stice", 1996, "What Do Stock Splits Really Signal?", "https://doi.org/10.2307/2331396",
             "Finds positive announcement and post-split excess returns and interprets splits as a management signal."),
            ("paper", "Byun & Rozeff", 2003, "Long-run Performance after Stock Splits: 1927 to 1996", "https://doi.org/10.1111/1540-6261.00558",
             "A 70-year sample in which long-run post-split abnormal performance largely disappears under careful benchmarks."),
        ],
    ),
    "0.3": (
        r"""Most modern stock trading happens in a limit order book: a continuously updated list of buy and sell orders at different prices. Incoming orders are usually matched by price first and then by arrival time. The survey by Gould and co-authors notes that limit order books match buyers and sellers in more than half of the world's financial markets, and it summarizes statistical regularities that appear across many of them. The same review stresses that many simple models of order books fail to reproduce what real books do, a reminder that "the market" is a mechanism with rules rather than an abstract price.

After a match comes settlement, when cash and securities actually change hands. The SEC shortened the standard U.S. settlement cycle for most broker-dealer transactions from two business days after the trade date (T+2) to one (T+1), with compliance from 28 May 2024. The trade date and the settlement date are therefore different events. Other markets set their own cycles and account rules, so check the rulebook of the exchange you study rather than assuming the U.S. convention applies.

Funds add one more layer. An ETF's market price is kept close to the value of its holdings because large dealers can create or redeem fund shares in exchange for the underlying securities and profit from any gap. Ben-David, Franzoni and Moussawi found that this arbitrage also works in reverse: stocks with more ETF ownership showed higher intraday and daily volatility, and a one-standard-deviation increase in ETF ownership was associated with about 16% higher daily volatility in their sample. A fund is a claim on a basket, but trading in the fund can also move the basket.

When you trace a trade, name four stages: the order, the match, clearing and settlement. For each stage, write down which institution is responsible and what could delay or reverse it.""",
        [
            ("arxiv", "Gould, Porter, Williams, McDonald, Fenn & Howison", 2010, "Limit Order Books", "https://arxiv.org/abs/1012.0349",
             "Survey of how limit order books work, what empirical studies find, and where popular models fall short."),
            ("official", "U.S. SEC · Investor.gov", 2024, "New T+1 Settlement Cycle: What Investors Need To Know", "https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/new-t1-settlement-cycle-what-investors-need-know-investor-bulletin",
             "Explains settlement and the U.S. move from T+2 to T+1 on 28 May 2024."),
            ("paper", "Ben-David, Franzoni & Moussawi", 2018, "Do ETFs Increase Volatility?", "https://doi.org/10.1111/jofi.12727",
             "Evidence that ETF arbitrage transmits trading into the underlying stocks and raises their volatility."),
        ],
    ),
    "0.4": (
        r"""Why is there a spread at all? Market-microstructure research gives three broad reasons: the cost of processing orders, the risk of holding inventory, and adverse selection. Glosten and Milgrom's model isolates the third. A market maker who cannot tell an informed trader from an uninformed one expects to lose to the informed side, so even a competitive market maker earning zero profit on average sets the ask above the bid to recover those losses from everyone else. The model predicts wider spreads when informed trading is more likely, such as just before important news.

The quoted spread only prices a small order. Larger orders consume depth, and a large body of empirical work finds that price impact grows much more slowly than order size. Tóth and co-authors explain the widely reported square-root law: the average impact of a large order executed in pieces scales roughly with the square root of its size relative to traded volume,

$$\Delta P \approx Y\,\sigma_{\mathrm{daily}}\sqrt{Q/V_{\mathrm{daily}}}$$

where Q is the order quantity, V is daily volume, σ is daily volatility and Y is a constant of order one. Quadrupling an order roughly doubles its expected impact per share. The relation is an average across many orders, not a quote you can rely on for a single trade.

Market orders that are large relative to the available depth can also produce abrupt moves. Braun and co-authors studied ultrafast extreme events, in which prices jump within milliseconds. Large market orders were the main cause in at least 60% of the events they observed, and fewer than 40% of the moves fully recovered over the following 100 trades. A stop order that turns into a market order during such an episode can fill far from its trigger.

Before submitting a practice order, compare its size with the displayed size and with typical daily volume. When the price condition matters more than immediacy, a limit instruction states that priority explicitly.""",
        [
            ("paper", "Glosten & Milgrom", 1985, "Bid, Ask and Transaction Prices in a Specialist Market with Heterogeneously Informed Traders", "https://doi.org/10.1016/0304-405X%2885%2990044-3",
             "The classic adverse-selection model in which a bid-ask spread exists even without order-processing costs."),
            ("arxiv", "Tóth, Lempérière, Deremble, de Lataillade, Kockelkoren & Bouchaud", 2011, "Anomalous price impact and the critical nature of liquidity in financial markets", "https://arxiv.org/abs/1105.1694",
             "A theory of thin liquidity near the price that accounts for square-root impact, with supporting data."),
            ("arxiv", "Braun, Fiegen, Wagner, Krause & Guhr", 2017, "Impact and Recovery Process of Mini Flash Crashes: An Empirical Study", "https://arxiv.org/abs/1707.05580",
             "Shows that most millisecond-scale price crashes follow large market orders and often do not fully reverse."),
        ],
    ),
    "0.5": (
        r"""The lesson's example of a 10% gain followed by a 10% loss is a small case of a general rule: volatility lowers compound growth. If a return series has an arithmetic mean μ and a volatility σ per period, its compound (geometric) growth rate is approximately

$$g \approx \mu - \tfrac{1}{2}\sigma^{2}$$

so two assets with the same average return can grow at very different rates. A position that gains 50% and then loses 50% has an arithmetic average of zero but ends 25% lower. Ole Peters describes this as the difference between an ensemble average, taken across many parallel investors, and a time average, experienced by one investor through time. For multiplicative wealth, the time average is the one you live through. It also sets a sensible limit on leverage: beyond some point, extra exposure raises the expected return while lowering the growth rate an individual actually experiences.

Compounding also skews long-horizon results. Bessembinder studied 25,967 U.S. common stocks from 1926 to 2016 and found that most had lifetime buy-and-hold returns below one-month Treasury bills. The best-performing 4% of companies accounted for the entire net wealth the market created over Treasury bills. One implication for a beginner is that a portfolio of a few stocks can easily miss the rare, very large winners that drive the market's average.

Costs compound in the same way. The SEC's investor bulletin illustrates a $100,000 portfolio growing 4% a year for 20 years: with a 0.25% annual fee it ends near $208,000, with 0.50% near $198,000, and with 1.00% near $179,000. A fee that looks small in one year removes a growing base of future returns.

When you study any return series, report both its arithmetic mean and its compound growth rate. Report fees both as an annual rate and as a total over your horizon.""",
        [
            ("arxiv", "Peters", 2009, "Optimal leverage from non-ergodicity", "https://arxiv.org/abs/0902.2965",
             "Distinguishes time-average from ensemble-average growth and derives an optimal leverage from the former."),
            ("paper", "Bessembinder", 2018, "Do stocks outperform Treasury bills?", "https://doi.org/10.1016/j.jfineco.2018.06.004",
             "Lifetime returns of nearly 26,000 U.S. stocks: most trailed Treasury bills while a few created the market's net gains."),
            ("official", "U.S. SEC · Investor.gov", None, "How Fees and Expenses Affect Your Investment Portfolio", "https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/updated",
             "Worked illustration of how annual fees of 0.25%, 0.50% and 1% compound over 20 years."),
        ],
    ),
    "0.6": (
        r"""The Cedar Tools example, with $2 million of profit but only $0.4 million of operating cash flow, touches one of the best-documented findings in accounting research. Earnings can be split into a cash component and an accrual component. Accruals are the part of profit recognized before, or without, the matching cash, such as a sale on credit. Sloan examined 40,679 firm-years from 1962 to 1991 and found that the accrual part of earnings persists less into future earnings than the cash part. Stock prices, however, behaved as if investors fixated on total earnings and did not fully distinguish the two components.

A simple accrual measure scales the gap by the size of the business:

$$\text{Accruals ratio}=\frac{\text{net income}-\text{operating cash flow}}{\text{average total assets}}$$

A high value is a question, not a verdict, because fast-growing firms build receivables and inventory for legitimate reasons. Dechow, Ge and Schrand reviewed the many measures researchers use for earnings quality, including persistence, accruals, smoothness, timeliness, restatements and enforcement actions. They reach no single definition, because quality depends on the decision the numbers are meant to inform.

Statements can also be combined into simple scores. Piotroski built a nine-signal score from profitability, cash flow, changes in leverage and liquidity, and operating efficiency, and applied it to cheap, high book-to-market stocks. In his 1976–1996 sample, choosing the financially strong firms raised the average return of such a portfolio by at least 7.5% a year. Whether a signal keeps working after it is published and after trading costs is a separate question, examined in the strategy courses.

For Cedar Tools, use the $15 million of total assets as a stand-in for the average: the accruals ratio is ($2 million − $0.4 million) / $15 million, about 10.7%. Then compare receivables growth with revenue growth, and name the later document, such as the next cash-flow statement, that would show whether collections recovered.""",
        [
            ("paper", "Sloan", 1996, "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows about Future Earnings?", "https://doi.org/10.2308/tar-9608042309",
             "The original accrual study: cash earnings persist more than accruals, and prices do not fully reflect the difference."),
            ("paper", "Dechow, Ge & Schrand", 2010, "Understanding earnings quality: A review of the proxies, their determinants and their consequences", "https://doi.org/10.1016/j.jacceco.2010.09.001",
             "A broad review explaining why no single number captures earnings quality for every decision."),
            ("paper", "Piotroski", 2000, "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers", "https://doi.org/10.2307/2672906",
             "A nine-signal financial-statement score that separated stronger from weaker cheap stocks in 1976–1996."),
        ],
    ),
    "0.7": (
        r"""How many stocks make a portfolio diversified? The answer has changed over time. Campbell, Lettau, Malkiel and Xu split U.S. stock volatility into market, industry and firm-level parts. From 1962 to 1997, firm-level volatility rose relative to market volatility while correlations between individual stocks fell, so the number of stocks needed to reach a given level of diversification increased. A rule of thumb from an older sample can therefore understate the company risk left in a small portfolio.

Diversification also weakens when it is most needed. Longin and Solnik used extreme-value methods to show that correlation between international equity markets is related to the market trend rather than to volatility alone: it rises in bear markets but not in bull markets. Sandoval and Franca reached a similar picture from the correlations of world market indices around the crashes of 1987, 2001 and 2008, finding that markets tend to behave as one during large downturns. Risk estimated with calm-period correlations will overstate the protection a portfolio has in a crisis.

Stop rules have limits of their own. Kaminski and Lo derived the conditions under which stop-loss rules add or subtract value. They showed that if prices follow a random walk, a simple rule that moves entirely to cash after a loss threshold always lowers the strategy's expected return. Whether a stop helps depends on how returns actually behave, for example whether declines tend to persist, and on the details of the rule. A stop is a risk-control choice with a cost, not free insurance.

Apply this to the lesson's example. Size the position from the planned loss, then repeat the calculation twice: once with the $45 gap exit, and once assuming every position in your paper portfolio falls on the same day.""",
        [
            ("paper", "Campbell, Lettau, Malkiel & Xu", 2001, "Have Individual Stocks Become More Volatile? An Empirical Exploration of Idiosyncratic Risk", "https://doi.org/10.1111/0022-1082.00318",
             "Documents rising firm-level volatility and the growing number of stocks needed for diversification."),
            ("paper", "Longin & Solnik", 2001, "Extreme Correlation of International Equity Markets", "https://doi.org/10.1111/0022-1082.00340",
             "Shows that international correlations rise in bear markets rather than simply with volatility."),
            ("arxiv", "Sandoval & Franca", 2011, "Correlation of financial markets in times of crisis", "https://arxiv.org/abs/1102.1339",
             "Correlation-matrix evidence that world markets move together during major crashes."),
            ("paper", "Kaminski & Lo", 2014, "When do stop-loss rules stop losses?", "https://doi.org/10.1016/j.finmar.2013.07.001",
             "A framework for when stop-loss rules help or hurt, including their cost under a random walk."),
        ],
    ),
    "0.8": (
        r"""A written plan protects you against two well-studied mistakes. The first is judging a decision by its outcome. Baron and Hershey gave people descriptions of decisions made under uncertainty and varied only the result. Participants rated the same decision as worse when it turned out badly, even though those who were asked said that outcomes should not affect the evaluation. Your review rules should therefore compare a trade with what the plan knew and intended at the time, not only with what happened next.

The second mistake is the disposition effect: selling winners too soon and holding losers too long. Odean analysed 10,000 accounts at a discount broker and found a strong preference for realizing gains rather than losses. The pattern was not explained by rebalancing or by the higher trading costs of low-priced stocks, it was not justified by the later performance of the stocks sold or kept, and in taxable accounts it lowered after-tax returns. Breitmayer, Hasso and Pelster later used brokerage records for 387,993 traders from 83 countries and found large differences in the strength of the effect between countries. Cultural traits such as long-term orientation, together with age and gender, helped explain those differences. Because the tendency varies from person to person, plan for it rather than assuming you are immune.

A plan turns both findings into procedure. Decide the exit conditions before entry, record the reason for closing each position, and review a sample of winning and losing trades against the reasons you wrote in advance. Ask whether you followed the plan, whether the information you used was available when you decided, and whether you would make the same decision again with the same information. Only the last question needs judgment; the first two can be checked from your records. Keeping the losing and abandoned plans in the same journal is what makes that check honest.""",
        [
            ("paper", "Baron & Hershey", 1988, "Outcome bias in decision evaluation", "https://doi.org/10.1037/0022-3514.54.4.569",
             "Experiments showing that people rate identical decisions worse when the outcome is bad."),
            ("paper", "Odean", 1998, "Are Investors Reluctant to Realize Their Losses?", "https://doi.org/10.1111/0022-1082.00072",
             "Account-level evidence of the disposition effect and its after-tax cost."),
            ("arxiv", "Breitmayer, Hasso & Pelster", 2019, "Culture and the disposition effect", "https://arxiv.org/abs/1908.11492",
             "Brokerage data from 83 countries showing how the disposition effect varies with culture, age and gender."),
        ],
    ),
}
