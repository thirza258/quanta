"""Research extensions for The intelligent & careful investor.

Each entry maps a lesson ID to (body, sources). A source is
(kind, authors, year, title, url, what it contributes); see research_depth.py.
Every figure was checked against a verbatim snippet from its source before merging.
"""

NOTES = {
    "11.1": (
        r"""The lesson's warning against grading a decision by its result has a name in psychology: outcome bias. Baron and Hershey gave undergraduates decisions made by others, in medical matters and monetary gambles; the students understood they held all the relevant information available to the decision maker. Favorable outcomes still earned better ratings of the thinking, more credit for competence or more willingness to yield the decision, though those asked said outcomes should not count. Shown only Rani's 15% fall and Dito's 20% gain, a reader may drift the same way; that is our inference, not a finding about investors.

Temperament shows up in real accounts. Odean studied trading records for 10,000 brokerage accounts and found a strong preference for realizing winners rather than losers, not justified by later performance and costly after tax in taxable accounts. Schatzmann and Haslhofer found a disposition effect in Bitcoin too, varying in intensity and not present throughout. Dichev found that investors' dollar-weighted returns fall systematically below buy-and-hold returns in nearly all major international stock markets, because of the timing and size of flows in and out. That is an aggregate result, so tying it to Rani or Dito is our inference.

Treat the lesson's +20% and −15% as consecutive years of one fund. Holding 100 throughout ends at 102, about 1.0% a year. Adding 100 after the good year ends at 187 on 200 contributed, roughly −4.4% a year: same fund, same two years (our arithmetic).

Exercise: date your deposits and withdrawals (fictional figures work), compute your money-weighted return (IRR) and compare it with the fund's published return. Then note what you did after each large move and whether your journal predicted it.""",
        [
            ('paper', 'Baron & Hershey', 1988, 'Outcome bias in decision evaluation', 'https://doi.org/10.1037/0022-3514.54.4.569',
             "Five studies in which judges who held all the decision maker's information still rated decisions better when outcomes were favorable, while saying outcomes should not matter."),
            ('paper', 'Odean', 1998, 'Are Investors Reluctant to Realize Their Losses?', 'https://doi.org/10.1111/0022-1082.00072',
             'Trading records of 10,000 brokerage accounts show a strong preference for selling winners over losers that later performance and, for taxable accounts, after-tax returns do not justify.'),
            ('paper', 'Dichev', 2007, "What Are Stock Investors' Actual Historical Returns? Evidence from Dollar-Weighted Returns", 'https://doi.org/10.1257/aer.97.1.386',
             'Shows that aggregate investor returns fall below buy-and-hold returns in nearly all major markets because of the timing and size of capital flows.'),
            ('arxiv', 'Schatzmann & Haslhofer', 2020, 'Exploring investor behavior in Bitcoin: a study of the disposition effect', 'https://arxiv.org/abs/2010.12415',
             'Finds a disposition effect of varying intensity in Bitcoin transactions, not present throughout the sample, so the habit is not confined to stocks.'),
        ],
    ),
    "11.2": (
        r"""Scheinkman and Xiong give the lesson's "bet on another buyer" a precise form. In their equilibrium model, overconfidence makes traders disagree about fundamentals and, with short sales restricted, a buyer also acquires an option to resell to someone more optimistic. Echoing earlier work, traders then pay prices above their own valuation of future dividends because they expect to find a buyer who will pay even more, and bubbles come with heavy trading volume and high price volatility. It is a model, not a measurement. Our inference is a test for any purchase: would you still pay this price if resale were impossible and only the business's distributions counted?

Evidence on who makes such bets concerns retail investors. Kumar found that individual investors prefer stocks with lottery features and, because those stocks underperform, the damage is larger for low-income investors who overweight them. Barber and co-authors found that intense buying by Robinhood users forecasts negative returns: average 20-day abnormal returns of −4.7% for the top stocks bought each day. Costola and co-authors found that meme stocks share common patterns in price, trading volume and social-media activity that differ from other heavily discussed stocks. These are averages and associations; none proves any single purchase wrong.

Exercise: for Cedar, write the distributions per share you would need to expect, now or later, to justify paying 12 if no buyer ever appeared. If you cannot, the rumor of a price target is carrying the argument.""",
        [
            ('paper', 'Scheinkman & Xiong', 2003, 'Overconfidence and Speculative Bubbles', 'https://doi.org/10.1086/378531',
             "Equilibrium model in which traders pay more than their own valuation of future dividends because they expect to resell to someone more optimistic; a precise form of the lesson's bet on another buyer."),
            ('paper', 'Kumar', 2009, 'Who Gambles in the Stock Market?', 'https://doi.org/10.1111/j.1540-6261.2009.01483.x',
             'Individual investors prefer lottery-type stocks, which underperform, and the loss is greater among low-income investors who overweight them.'),
            ('paper', 'Barber, Huang, Odean & Schwarz', 2022, 'Attention-Induced Trading and Returns: Evidence from Robinhood Users', 'https://doi.org/10.1111/jofi.13183',
             'Intense buying by Robinhood users forecasts negative returns; the top stocks bought each day show average 20-day abnormal returns of -4.7%.'),
            ('arxiv', 'Costola, Iacopini & Santagiustina', 2021, 'On the "mementum" of Meme Stocks', 'https://arxiv.org/abs/2106.03691',
             'Shows that meme stocks share common patterns in price, trading volume and social-media activity, and that their mementum regime differs from other stocks with heavy social-media activity.'),
        ],
    ),
    "11.3": (
        r"""Sharpe showed why the lesson's simple baseline is hard to beat, using only arithmetic. If active and passive management are defined sensibly, then before costs the average actively managed dollar earns the same return as the average passively managed dollar, and after costs it earns less, in any period. This describes the average dollar, not each investor: our reading is that an individual can still beat the market, but only at the expense of other active investors.

French priced the search. He compared the fees, expenses and trading costs of investing in the U.S. stock market with what everyone investing passively would pay; averaged over 1980–2006, investors spent 0.67% of the market's aggregate value each year searching for superior returns. Under reasonable assumptions, he estimated, the typical investor would have gained 67 basis points a year by switching to a passive market portfolio.

Heaton, Polson and Witte add a model-based reason beyond fees. Because the best performers in a broad index often do much better than the rest, randomly choosing a subset of stocks can dramatically raise the chance of trailing the index, a risk they argue likely matters more than the extra fees. Their subset is random, not researched, so this is a warning rather than a verdict; our inference is that a twelve-company portfolio is also a small subset.

Exercise: the lesson's plan needs 144 hours against 24 available, a 120-hour gap. Put a rupiah value on those hours, add the extra trading costs, and divide by the portfolio's value. The result is the annual outperformance the research must earn just to match the simple baseline.""",
        [
            ('paper', 'Sharpe', 1991, 'The Arithmetic of Active Management', 'https://doi.org/10.2469/faj.v47.n1.7',
             'Short proof that, before costs, the average active dollar matches the average passive dollar and, after costs, falls behind it, for any period; it concerns the average dollar, not each investor.'),
            ('paper', 'French', 2008, 'Presidential Address: The Cost of Active Investing', 'https://doi.org/10.1111/j.1540-6261.2008.01368.x',
             "Estimates that investors spent 0.67% of the U.S. market's value a year in 1980-2006 searching for superior returns, about 67 basis points a year for the typical investor."),
            ('arxiv', 'Heaton, Polson & Witte', 2015, 'Why Indexing Works', 'https://arxiv.org/abs/1510.03550',
             'Model, published in 2017, in which a random subset of an index often trails it because a few top performers drive index returns; underperformance risk may matter more than higher fees.'),
        ],
    ),
    "11.4": (
        r"""Shiller made the lesson's gap between quote and value testable. He formed an ex-post rational price from the dividends paid afterward and found it very stable and smooth next to the actual detrended real price. A market whose price is the optimal forecast of that series is inconsistent with the data if the long-run dividend trend is taken as given; reconciling the two requires market expectations of dividends to have strayed from trend much more than they historically did. That conditional is the caveat: the result tests one model under an assumed trend and says nothing about whether any single quote is wrong.

Joulin and co-authors matched high-frequency stock returns against news feeds and found that neither company-specific nor market-wide news explains the frequency and amplitude of price jumps; they conjecture that most jumps come from order-flow fluctuations near vanishing liquidity. Their data are intraday and the lesson's horizon is months, so our inference is that a fall alone is weak evidence of a changed thesis, and finding no news does not prove it unchanged.

In an experiment, Gneezy and Potters found that the more often returns are evaluated, the more risk averse investors are, in line with myopic loss aversion. Our inference: how often you look is a design choice for your review policy.

Exercise: add a third case in which the lawsuit cuts the value range to 40–55. At a price of 50 the discount against 55 is 9.09%, and against 40 the price sits 25% above the estimate. Then list what a move to 50 should make you re-examine (the lawsuit, the value range, your liquidity) and what evidence you would wait for before acting.""",
        [
            ('paper', 'Shiller', 1980, 'Do Stock Prices Move Too Much to be Justified by Subsequent Changes in Dividends?', 'https://doi.org/10.3386/w0456',
             'NBER working paper (1980); the American Economic Review version followed in 1981. A price built from later dividends is far smoother than actual prices, so an efficient-market price needs unusual dividend expectations, given the assumed trend.'),
            ('arxiv', 'Joulin, Lefevre, Grunberg & Bouchaud', 2008, 'Stock price jumps: news and volume play a minor role', 'https://arxiv.org/abs/0803.1769',
             'Intraday study finding that neither company-specific nor market-wide news explains the frequency and amplitude of price jumps; a price move alone is weak evidence of new information.'),
            ('paper', 'Gneezy & Potters', 1997, 'An Experiment on Risk Taking and Evaluation Periods', 'https://doi.org/10.1162/003355397555217',
             'Experiment showing that the more frequently returns are evaluated, the more risk averse investors are, in line with myopic loss aversion.'),
        ],
    ),
    "11.5": (
        r"""Willingness, the lesson's risk tolerance, is a shaky foundation for two reasons. It moves: Guiso, Sapienza and Zingales repeatedly surveyed an Italian bank's clients and found that qualitative and quantitative measures of risk aversion both rose substantially after the 2008 crisis, and in a lab experiment people who watched a horror movie had certainty equivalents 27% lower, pointing to fear. And a recorded tolerance may not predict behavior: in an investment dealer's data on over 23,000 clients, Thompson and co-authors found that the know-your-client information Canadian rules require, such as age or risk tolerance, did not explain what clients did; trading frequency and volume did.

Capacity lives on the balance sheet. Lusardi, Schneider and Tufano used a 2009 survey to ask whether Americans could come up with $2,000 in 30 days: about a quarter would certainly not, and another 19% would manage by relying at least partly on pawning, selling possessions or payday loans. Kaplan, Violante and Weidner found "wealthy hand-to-mouth" households across eight countries: little liquid wealth despite sizable housing or retirement assets. These are not Indonesian samples, so carrying the mechanism over is our inference.

Now stress the lesson's household. Its 66 million long-horizon pool is a residual, not a promise. Suppose a 48 million bill, twice the reserve, arrives right after the 30% fall: the reserve covers 24 million, and the other 24 million must come from a pool then worth 46.2 million, so about 52% of it is sold at the low (our arithmetic, assuming no borrowing and untouched near-term spending).

Exercise: using fictional or broad-category figures, not real balances, find the shock that would exhaust the reserve and note which holdings would be sold first.""",
        [
            ('paper', 'Guiso, Sapienza & Zingales', 2013, 'Time Varying Risk Aversion', 'https://doi.org/10.3386/w19284',
             "NBER working paper version of the 2018 article: an Italian bank's clients became markedly more risk averse after the 2008 crisis, and a horror-movie experiment points to fear."),
            ('arxiv', 'Thompson, Feng, Reesor & Grace', 2020, "Know Your Clients' behaviours: a cluster analysis of financial transactions", 'https://arxiv.org/abs/2005.03625',
             "In a dealer's data on over 23,000 clients, collected know-your-client information such as risk tolerance did not explain client behavior; trading frequency and volume did."),
            ('paper', 'Lusardi, Schneider & Tufano', 2011, 'Financially Fragile Households: Evidence and Implications', 'https://doi.org/10.3386/w17072',
             '2009 survey data on whether Americans could come up with $2,000 in 30 days, and the coping methods people use, from savings to pawning, selling possessions or payday loans.'),
            ('paper', 'Kaplan, Violante & Weidner', 2014, 'The Wealthy Hand-to-Mouth', 'https://doi.org/10.1353/eca.2014.0002',
             'Household portfolio surveys from eight countries show households with sizable illiquid assets but little liquid wealth, so net worth alone does not measure the ability to wait.'),
        ],
    ),
    "11.6": (
        r"""Bekaert and Wang put evidence behind the lesson's caution about equities. They estimated inflation betas, the sensitivity of returns to inflation, for standard bond and well-diversified equity indices in over 45 countries and concluded that such securities are poor inflation hedges. Adding Treasury bills, foreign bonds, real estate and gold helped, but inflation risk stayed hard to hedge.

Horizon changes the answer. Boudoukh and Richardson note that earlier work, using horizons of a year or less, found stocks a poor hedge; with two centuries of U.S. and U.K. data they found a positive relation between stock returns and inflation at long horizons. Albulescu and co-authors, testing U.S. sector indexes over 2002–2015 by cointegration, found inflation and its uncertainty negatively related to stock prices in the long run, contrary to the Fisher effect, though for several sectors the relation vanished after the crisis. The studies differ in method and sample (price levels in a recent period against returns over two centuries), so they do not refute each other; "long run" is not one number.

In the lesson's example, 6% against 4% inflation leaves a real return of about 1.923%, but that is one year's outcome, and these studies suggest it says little about how the same holding would fare if inflation changed (our inference). Exercise: for each holding, write the channel through which it should keep pace with your goal's own prices (indexation, resetting rates, pricing power) and the horizon at which the evidence above supports it. Mark any channel you cannot name as a hope, not a hedge.""",
        [
            ('paper', 'Bekaert & Wang', 2010, 'Inflation risk and the inflation risk premium', 'https://doi.org/10.1111/j.1468-0327.2010.00253.x',
             'Estimates inflation betas for bond and equity indices in over 45 countries and finds standard securities poor inflation hedges; broader asset menus help but inflation risk stays hard to hedge.'),
            ('paper', 'Boudoukh & Richardson', None, 'Stocks are a Good Hedge for Inflation (In the Long Run)', 'https://ideas.repec.org/p/fth/pennfi/14-92.html',
             "Working-paper version of the authors' 1993 American Economic Review article: stocks hedge inflation poorly at short horizons, but two centuries of data show a positive relation at long horizons."),
            ('arxiv', 'Albulescu, Aubin & Goyeau', 2016, 'Stock prices, inflation and inflation uncertainty in the U.S.: Testing the long-run relationship considering Dow Jones sector indexes', 'https://arxiv.org/abs/1603.01231',
             'Cointegration study of U.S. sector indexes over 2002-2015: in the long run inflation and its uncertainty were negatively related to stock prices, with the effect vanishing for several sectors after the crisis.'),
        ],
    ),
    "11.7": (
        r"""The lesson's 26% company shows what overlapping funds can hide. Three studies point to other places where one risk can sit behind many labels.

Country. French and Poterba estimated that Japanese investors held more than 98% of their equity portfolios at home, against 94% for U.S. and 82% for British investors. Their model implied that investors expected domestic returns to beat foreign ones by several hundred basis points, and they read the pattern as investor choice rather than institutional constraint. A portfolio of funds that are each labelled diversified can still be mostly one country, so the look-through table needs a country column (our inference).

Employer. Meulbroek priced the lost diversification of company stock held in pension plans. In her estimates, an employee who puts one-quarter of assets into the employer's shares gives up 42 percent of their market value relative to a well-diversified equity portfolio. Counting wages, which depend on the same firm, total exposure is larger than the portfolio weight alone suggests.

Shared drivers. Plerou and co-authors applied random-matrix methods to correlations among up to 1,000 U.S. stocks. Most of the structure looked like noise; what stood out was one influence common to all stocks and groups of stocks matching business sectors. Our inference: hundreds of tickers can reduce to one market factor plus sector bets.

Exercise: add country, sector and employer columns to the lesson's look-through table. Then halve the 26% company's price: the portfolio loses 13% (26% × 50%) before any effect on your wages. If that loss would break your plan, the exposure is larger than the plan can bear.""",
        [
            ('paper', 'French & Poterba', 1991, 'Investor Diversification and International Equity Markets', 'https://doi.org/10.3386/w3609',
             'Estimates the home share of Japanese, U.S. and British equity portfolios (98%, 94%, 82%) and argues the gap reflects investor choice, so a country column belongs in a look-through audit.'),
            ('paper', 'Meulbroek', 2005, 'Company Stock in Pension Plans: How Costly Is It?', 'https://doi.org/10.1086/430807',
             "Values the lost diversification of employer stock held in pension plans; one-quarter of assets in it sacrifices 42 percent of the stock's market value, relative to a diversified equity portfolio."),
            ('arxiv', 'Plerou et al.', 2001, 'A Random Matrix Approach to Cross-Correlations in Financial Data', 'https://arxiv.org/abs/cond-mat/0108023',
             'Random-matrix study of U.S. stock correlations: one influence common to all stocks, groups that match business sectors, and a bulk that is close to random.'),
        ],
    ),
    "11.8": (
        r"""Why shade the base case down to a conservative value? Smith and Winkler describe a selection effect: rank options by estimated value, pick the top one, and its true value is expected to fall short of the estimate even when every estimate is unbiased, sometimes by a lot. Screening for the widest discount works this way, so the lesson's 40% base-case discount is the figure most exposed to flattering errors (our inference). A cushion against the cautious value pre-pays for them.

Does a cushion pay? Oppenheimer tested Graham's rule of buying below net current assets over 1970–83. Portfolios earned higher mean returns than market benchmarks, and the most undervalued tended to beat them by the widest margins. Individual 30-month holding periods were widely variable, though the portfolios outperformed on the whole. A wide spread means a cushion is no guarantee, and one short, old sample illustrates rather than proves.

Bad stretches are where a decline can become permanent. Goldberg and Mahmoud, writing about fund risk, define a drawdown as the maximum decline in portfolio value over a fixed horizon and call it a trigger for forced selling: an investor unable to secure funding after an abrupt fall may have to sell valuable positions under unfavorable conditions. They add that volatility cannot tell intermittent losses from consecutive ones. We infer that anyone who must raise cash faces a version of this risk.

Exercise: at a price of 60 the lesson's conservative value of 70 leaves a 14.29% margin, and an extra 10 per share of debt would erase it. Write down when you might need this money. If that date could fall inside a drawdown, the margin does not protect it.""",
        [
            ('paper', 'Smith & Winkler', 2006, 'The Optimizer’s Curse: Skepticism and Postdecision Surprise in Decision Analysis', 'https://doi.org/10.1287/mnsc.1050.0451',
             'Shows that choosing the option with the best estimated value makes its true value fall short of the estimate on average, even with unbiased estimates; the logic behind shading a value estimate before comparing it with price.'),
            ('paper', 'Oppenheimer', 1986, 'Ben Graham’s Net Current Asset Values: A Performance Update', 'https://doi.org/10.2469/faj.v42.n6.40',
             "Tests Graham's buy-below-net-current-assets rule on 1970–83 data: higher mean returns than benchmarks, widest margins for the most undervalued, but widely variable 30-month results."),
            ('arxiv', 'Goldberg & Mahmoud', 2014, 'Drawdown: From Practice to Theory and Back Again', 'https://arxiv.org/abs/1404.7493',
             'Defines drawdown and explains how a large one can force liquidation under unfavorable conditions; shows why path matters more than volatility, which cannot separate intermittent from consecutive losses.'),
        ],
    ),
    "11.9": (
        r"""The lesson's scenario has bonds falling alongside stocks. Whether bonds cushion equity losses or add to them depends on how the two move together, and that has changed. Campbell, Sunderam and Viceira report that the covariance between U.S. Treasury bond and stock returns was slightly positive on average from 1953 to 2014, unusually high in the early 1980s, and negative in the early 21st century, particularly in the downturns of 2001 and 2007 to 2009. A policy tested in one era inherits that era's relationship (our inference).

How rare is the lesson's bad case? In Damodaran's annual series for 1928 to 2025, stocks with dividends and 10-year Treasury bonds both lost value in five of 98 years: 1931, 1941, 1969, 2018 and 2022. The severe one was 2022, at −18.04% and −17.83%; by our arithmetic a 60/40 mix rebalanced each year would have lost 17.96%. For such a mix, only 1931 was worse than the lesson's −22%.

One period also hides the path. Devanathan, Tzikas and Boyd, in a 2026 preprint, simulate an annually rebalanced 60/40 portfolio of two broad U.S. stock and bond funds over 2006–2026, net of trading costs, and report a maximum drawdown, the largest fall from a running peak, of 33.7%. That is one historical path, not a forecast.

Exercise: add two columns to your scenario table, a one-year shock and a peak-to-trough drawdown, and include a case where stocks and bonds fall together. Compare the worst figure with the loss you said you could bear in the earlier lesson on capacity.""",
        [
            ('paper', 'Campbell, Sunderam & Viceira', 2017, 'Inflation Bets or Deflation Hedges? The Changing Risks of Nominal Bonds', 'https://doi.org/10.1561/104.00000043',
             'Documents that the covariance between Treasury bond and stock returns changed sign across eras, so the cushion a bond sleeve gives in a stress scenario is not a constant.'),
            ('data', 'Damodaran', None, 'Historical Returns on Stocks, Bonds and Bills', 'https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html',
             'Annual U.S. stock, bill and Treasury bond returns since 1928; used to count the years when stocks and bonds both fell and to size a 60/40 mix in 2022.'),
            ('arxiv', 'Devanathan, Tzikas & Boyd', 2026, 'Simple Dynamic Stock/Bond/Gold Portfolios', 'https://arxiv.org/abs/2609.07946',
             "Simulates annually rebalanced 60/40 and other mixes over 2006–2026, net of trading costs; the 60/40's 33.7% maximum drawdown shows what a one-period scenario can understate (a September 2026 preprint)."),
        ],
    ),
    "11.10": (
        r"""The lesson's choice between a calendar rule and a deviation band has theory behind it. Muhle-Karbe, Reppen and Soner sketch the trade-off under proportional trading costs: the loss from drifting off target grows with the square of a no-trade band's width, while the trading needed to stay inside falls in inverse proportion to the width. Balancing the two puts the best width at the order of the cube root of the cost rate, and the best trade outside the band is the minimal one that brings the portfolio back inside. By our arithmetic, a cost eight times higher doubles the band.

Ekren, Liu and Muhle-Karbe compare calendar rules with band rules. With constant investment opportunities, the best calendar rule virtually coincides with the best band rule, and at a 1% transaction cost the best rule trades less often than every two years. With mean-reverting expected returns the best frequency rises to about once every half year, and for one risky asset bands offer a marked improvement. The authors call the message mixed.

Dichtl, Drobetz and Wambach compared rebalancing with buy-and-hold on a 30-year dataset from the United States, United Kingdom and Germany. Frequent rebalancing significantly improved risk-adjusted performance in every country and on every measure. The abstract does not say how costs were treated, so test the result against your own.

In the lesson's example the equity weight drifts to 64.286%. A ±5-point band around 60% trades nothing; a ±3-point band sells only back to 63%, a sale of 1.44 (0.63 × 112 = 70.56) rather than 4.8. The widths are illustrative.

Exercise: write your band and cost assumption, then double the cost; the scaling above widens the band by about a quarter. Check whether your rule changes.""",
        [
            ('arxiv', 'Ekren, Liu & Muhle-Karbe', 2015, 'Optimal Rebalancing Frequencies for Multidimensional Portfolios', 'https://arxiv.org/abs/1510.05097',
             'Compares calendar (time-based) and band (move-based) rebalancing under small proportional costs: near-identical with constant opportunities, with bands clearly better when expected returns mean-revert.'),
            ('arxiv', 'Muhle-Karbe, Reppen & Soner', 2016, 'A Primer on Portfolio Choice with Small Transaction Costs', 'https://arxiv.org/abs/1612.01302',
             'Survey explaining why optimal trading under proportional costs is a no-trade band whose width scales with the cube root of the cost rate, with minimal trading back to the band.'),
            ('paper', 'Dichtl, Drobetz & Wambach', 2015, 'Testing rebalancing strategies for stock-bond portfolios across different asset allocations', 'https://doi.org/10.1080/00036846.2015.1088139',
             'Compares rebalancing with buy-and-hold over a 30-year dataset from the United States, United Kingdom and Germany; frequent rebalancing improved risk-adjusted performance in every country.'),
        ],
    ),
    "11.12": (
        r"""The lesson's formula makes average cost an amount-weighted harmonic mean of the prices paid. With equal purchases it sits below the simple average price whenever prices differ: 6.667 against 7.5 in the lesson. That is arithmetic, not a return advantage: it compares your cost with a statistic, not with a lump sum or no purchase.

The question the lesson sets aside is a sum already in hand, invested at once or in instalments. Rozeff showed that with a positive expected risk premium a lump sum is mean-variance superior to dollar-averaging once the risks of the two policies are equal. Over 12 months it returned 1 to 4 percent more, depending on stock size, and beat dollar-averaging on the S&P 500 in 40 of 65 years, so staging won the other 25. He added that investing a smaller fraction of funds in the risky asset, all at once, cuts risk more effectively. Knight and Mandell, using historical returns and Monte Carlo simulation, found that staging gave no protection against a fall right after buying; optimal rebalancing and buy-and-hold did better in all three analyses.

Staging keeps less capital invested on average. Sato's arXiv note measures that as effective investment exposure, time-integrated invested capital, and says adopting such schedules under budgetary or timing constraints need not be irrational. Monthly salary is such a case (our reading). For the lesson's two purchases, one period apart, average exposure is 75% of a lump sum's (our arithmetic).

Exercise: replay the lesson's table with prices 10 then 20. Staged buying ends with 15 units worth 300; a lump sum of 200 holds 20 units worth 400. Then write the non-price rule that triggers a thesis review.""",
        [
            ('paper', 'Rozeff', 1994, 'Lump-Sum Investing versus Dollar-Averaging', 'https://doi.org/10.3905/jpm.1994.409474',
             'Shows a lump sum is mean-variance superior to dollar-averaging once risk is held equal, ahead in 40 of 65 years on the S&P 500, and that a smaller risky share invested at once cuts risk more effectively.'),
            ('paper', 'Knight & Mandell', 1992, 'Nobody Gains from Dollar Cost Averaging Analytical, Numerical and Empirical Results', 'https://doi.org/10.1016/1057-0810%2892%2990015-5',
             'Graphical, historical and Monte Carlo analysis finding no protection from staging a lump sum, with optimal rebalancing and buy-and-hold ahead in all three analyses.'),
            ('arxiv', 'Sato', 2025, 'A Clarifying Note on Long-Horizon Investment and Dollar-Cost Averaging: An Effective Investment Exposure Perspective', 'https://arxiv.org/abs/2601.06074',
             'Defines effective investment exposure as time-integrated invested capital and explains why timing schedules adopted under budget or timing constraints need not be irrational.'),
        ],
    ),
    "11.13": (
        r"""The lesson strips out a gain, but company-defined measures more often strip out costs. Bradshaw and Sloan found that over the preceding 20 years GAAP and "Street" earnings had come apart more often and by more, with a very strong bias toward a Street number above the GAAP one. The market response to the Street figure had displaced GAAP earnings as a primary determinant of stock prices, and management took a proactive role in defining and emphasizing it. An adjustment can run either way, so its direction and its reason are the clue.

In SEC filings, Regulation S-K Item 10(e) requires the most directly comparable GAAP measure with equal or greater prominence and a quantitative reconciliation. It also bars adjusting a performance measure to eliminate items identified as non-recurring, infrequent or unusual when the charge or gain is reasonably likely to recur within two years or a similar one occurred in the prior two years. That polices the label, not every exclusion, but it suggests a test for your own adjustments (our inference): before calling the lesson's 40 one-time, look back two years.

Cash is the second check. In 40,679 firm-years from 1962 to 1991, Sloan found that earnings carried by accruals were less persistent than earnings backed by cash flow, yet prices acted as if investors fixated on the headline. Firms with high accruals had negative future abnormal returns and low-accrual firms positive ones, concentrated around later earnings announcements.

Exercise: in one annual report, copy every reconciling item with its sign, search the two prior years for a similar item, and set net income beside cash from operations. Then redo the lesson's EPS and P/E (reported 6 and 10, recurring 4 and 15).""",
        [
            ('paper', 'Bradshaw & Sloan', 2002, 'GAAP versus The Street: An Empirical Assessment of Two Alternative Definitions of Earnings', 'https://doi.org/10.1111/1475-679X.00038',
             "Documents the growing, upward-biased gap between GAAP and Street earnings, the market's shift toward the Street number, and management's role in defining it."),
            ('paper', 'Sloan', 1996, 'Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?', 'https://doi.org/10.2308/tar-9608042309',
             'In 40,679 firm-years, accrual-based earnings were less persistent than cash-based earnings, yet prices behaved as if investors fixated on the earnings headline.'),
            ('official', 'U.S. SEC', None, 'Regulation S-K Item 10(e): Use of non-GAAP financial measures in Commission filings (17 CFR 229.10)', 'https://www.law.cornell.edu/cfr/text/17/229.10',
             'Rule text requiring a prominent GAAP comparison and a quantitative reconciliation, and barring items labelled non-recurring that are likely to recur within two years.'),
        ],
    ),
}
