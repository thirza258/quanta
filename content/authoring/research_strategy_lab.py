"""Research extensions for The strategy lab.

Each entry maps a lesson ID to (body, sources). A source is
(kind, authors, year, title, url, what it contributes); see research_depth.py.
Every figure was checked against a verbatim snippet from its source before merging.
"""

NOTES = {
    "4.5": (
        r"""How many ideas you tried changes what one good result is worth, and finance researchers have tried to measure that. Harvey, Liu and Zhu built a multiple-testing framework using factor tests going back to 1967 and concluded that a new factor should clear a t-statistic above 3.0. Harvey's presidential address adds a caution: if the effect being studied is rare, even t > 3 produces many false positives, so a stated economic mechanism is a reason to believe a result before you run the test, not decoration afterwards. That last step is our reading of his point, not his wording.

Chen disagrees about how far to push the hurdle. He argues that calls to raise statistical hurdles may be hard to justify empirically, because results that fail existing hurdles often go unobserved, so any new hurdle has to be extrapolated from a biased sample. Your experiment ledger is the small-scale answer to that problem: it keeps the failures that the published record lacks.

Where an edge lives matters as much as how big it looks. Hou, Xue and Zhang replicated 452 anomalies and found that once microcaps were mitigated through NYSE breakpoints and value-weighted returns, 65% could not clear the single-test hurdle of an absolute t-value of 1.96. A rule that works only in tiny, illiquid stocks is the dependence on one illiquid security that Cedar's rejection criterion should name.

Now test the lesson's own numbers. At 20 basis points per traded notional, a 7% cost drag implies about 35 times the portfolio's value was traded (7 ÷ 0.20). That is our arithmetic, and it assumes this proportional cost is the whole drag. For a two-name portfolio it is a lot of trading, so the gap suggests checking whether the drag also includes other costs. Before running anything, write down the net-advantage floor, the cost per traded notional, and a liquidity-restricted version of the rule that must also pass. Then log every variant you try.""",
        [
            ('paper', 'Harvey, Liu & Zhu', 2016, '… and the Cross-Section of Expected Returns', 'https://doi.org/10.1093/rfs/hhv059',
             'Multiple-testing framework for factor research; argues new factors need a t-statistic above 3.0 and that most claimed findings are likely false.'),
            ('paper', 'Harvey', 2017, 'Presidential Address: The Scientific Outlook in Financial Economics', 'https://doi.org/10.1111/jofi.12530',
             'Explains why p-values and fixed thresholds mislead when effects are rare, and sets out guidelines for a transparent research culture.'),
            ('arxiv', 'Chen', 2022, 'Do t-Statistic Hurdles Need to be Raised?', 'https://arxiv.org/abs/2204.10275',
             'A counterpoint: because failed results go unobserved, higher hurdles are weakly identified, so published-sample methods are preferred.'),
            ('paper', 'Hou, Xue & Zhang', 2020, 'Replicating Anomalies', 'https://doi.org/10.1093/rfs/hhy131',
             'Replication of 452 anomalies showing most fail standard hurdles once microcaps are down-weighted.'),
        ],
    ),
    "4.6": (
        r"""Each comparator in this lesson answers a different question, and published studies show how much the choice matters. DeMiguel, Garlappi and Uppal compared 14 portfolio-construction models with the naive equal-weight rule across seven datasets. None was consistently better on Sharpe ratio, certainty-equivalent return or turnover. That result concerns weighting schemes rather than stock picking, but it is a reason to treat equal weight over the same eligible names as a demanding first comparison.

A matched benchmark removes exposures you could have bought cheaply. Daniel, Grinblatt, Titman and Wermers built 125 passive portfolios from market capitalization, book-to-market and prior-year return, then compared each stock a fund held with the passive portfolio sharing its characteristics. Across more than 2,500 equity funds from 1975 to 1994 they found some selectivity, especially among aggressive-growth funds, but no characteristic timing. The parallel for a value rule is asking whether it beats stocks of similar size and valuation, not only the market.

The benchmark can also leak the future. Daniel, Sornette and Wöhrmann showed that testing against the assets that make up an index at the end of the period, rather than at the start, produces a bias that can reach 8% a year when the S&P 500 is the benchmark. Their CRSP sample ran from 1926 to 2006, and they propose random strategies with similar constraints as a general test. So record benchmark membership as of the first date.

Try it on the lesson's numbers. The 2-point gap and the 1.887% wealth ratio both come from 10,800 against 10,600, yet neither says whether chance could do as well. If a universe has three eligible names and the rule holds two, only three two-name portfolios exist; list them all. Even if your pair ranks first, the best attainable p-value is 1/3 (our arithmetic), so a single period cannot separate skill from luck at conventional significance levels.""",
        [
            ('paper', 'DeMiguel, Garlappi & Uppal', 2009, 'Optimal Versus Naive Diversification: How Inefficient Is the 1/N Portfolio Strategy?', 'https://doi.org/10.1093/rfs/hhm075',
             'Out-of-sample test of 14 optimizing models against equal weighting; none consistently wins, so 1/N is a hard null to beat.'),
            ('paper', 'Daniel, Grinblatt, Titman & Wermers', 1997, 'Measuring Mutual Fund Performance with Characteristic-Based Benchmarks', 'https://doi.org/10.1111/j.1540-6261.1997.tb02724.x',
             'Builds 125 characteristic-matched passive portfolios so selection is judged against stocks with the same size, value and momentum traits.'),
            ('arxiv', 'Daniel, Sornette & Wöhrmann', 2008, 'Look-Ahead Benchmark Bias in Portfolio Performance Evaluation', 'https://arxiv.org/abs/0810.1922',
             'Shows that using end-of-period benchmark constituents biases performance tests, and proposes random strategies with similar constraints as a test.'),
        ],
    ),
    "4.7": (
        r"""Filling at the next open removes one timing error, but research shows that the decision price and the fill price can sit in very different parts of a return. Glasserman and co-authors report that over the past 30 years nearly all the gains in the U.S. stock market were earned overnight, while average intraday returns were negative or flat. Lou, Polk and Skouras examined 14 trading strategies and found that profits were earned either entirely overnight, for reversal and a variety of momentum strategies, or entirely intraday, typically with opposite signs. A label that runs from one close to the next includes the overnight leg, whereas an order queued after the close fills at the open and never earns it. That implication is our reading of their decomposition.

The open can also be an expensive place to buy. Berkman and co-authors found positive overnight returns followed by reversals during the trading day, driven by opening prices that are high relative to intraday prices. The pattern was concentrated in stocks that had recently attracted retail attention, and for retail traders buying such stocks near the open the extra implicit cost frequently exceeded the effective half spread. A flat 0.1% per side, as in the lesson, would not capture that.

Apply it to the worked example. A signal at a 100 close that fills at 105 has already gapped 5%, because 105 / 100 − 1 = 0.05. A close-to-close label would credit the strategy with that gap, while the purchase actually pays it. As an exercise, split each return in your price file into an overnight part (previous close to open) and an intraday part (open to close). Then rerun the rule once with close-to-close returns and once with next-open-to-close returns. If the edge shrinks sharply, it lived in a period that your fill convention cannot trade.""",
        [
            ('arxiv', 'Glasserman, Krstovski, Laliberte & Mamaysky', 2025, 'Does Overnight News Explain Overnight Returns?', 'https://arxiv.org/abs/2507.04481',
             'Documents that, over three decades, almost all U.S. stock-market gains arrived overnight, and tests news-based explanations.'),
            ('paper', 'Lou, Polk & Skouras', 2019, 'A tug of war: Overnight versus intraday expected returns', 'https://doi.org/10.1016/j.jfineco.2019.03.011',
             'Splits the profits of 14 trading strategies into overnight and intraday components, which often have opposite signs.'),
            ('paper', 'Berkman, Koch, Tuttle & Zhang', 2012, 'Paying Attention: Overnight Returns and the Hidden Cost of Buying at the Open', 'https://doi.org/10.1017/S0022109012000270',
             'Shows that opening prices of high-attention stocks are inflated, so buying near the open carries a hidden implicit cost.'),
        ],
    ),
    "4.8": (
        r"""The lesson's twelve configurations are a trial count, and trial counts have measurable consequences. Bailey, Borwein, López de Prado and Zhu showed that it takes a relatively small number of trials to find a strategy with spuriously high backtested performance. With five years of data they say no more than 45 independent configurations should be tried. On a two-year backtest, seven are enough for the expected best in-sample Sharpe ratio to be 1 while the expected out-of-sample ratio is 0. Their calculation assumes independent trials, and for overlapping variants they suggest a dimension-reduction method such as principal component analysis. Our reading is that the two fee settings of one rule will behave almost alike, so the independent count is below twelve, but the full count still belongs in the report.

A manifest answers a different question: can someone else rerun this? Sandve and co-authors' ten rules include keeping track of how every result was produced, archiving the exact versions of external programs, version-controlling custom scripts, and noting the random seeds of any analysis that includes randomness. Henderson and co-authors, working on reinforcement learning, found that reproducing results is seldom straightforward, because non-determinism combined with variance intrinsic to the methods makes reported results hard to interpret. Store package versions and seeds beside the lesson's source and input hashes.

Reproducibility does not guarantee agreement. Menkveld and co-authors let 164 teams test the same hypotheses on the same data. The spread across teams, which they call nonstandard errors, was sizable, though smaller for more reproducible or higher rated research. A manifest cannot make two analysts choose alike; it makes their differences traceable.

Exercise: for your own run, write N = families × lookbacks × cost settings, add every other choice you varied, and print the total beside the headline result. Then rerun in a clean directory and confirm the output hashes match.""",
        [
            ('paper', 'Bailey, Borwein, López de Prado & Zhu', 2014, 'Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance', 'https://doi.org/10.1090/noti1105',
             'Shows how few independent trials produce a spuriously high Sharpe ratio and relates the number of trials to the backtest length needed.'),
            ('paper', 'Sandve, Nekrutenko, Taylor & Hovig', 2013, 'Ten Simple Rules for Reproducible Computational Research', 'https://doi.org/10.1371/journal.pcbi.1003285',
             'Practical rules for recording provenance, software versions, scripts and random seeds, which map onto an experiment manifest.'),
            ('paper', 'Menkveld et al.', 2024, 'Nonstandard Errors', 'https://doi.org/10.1111/jofi.13337',
             '164 research teams tested the same hypotheses on the same data and reached sizably different estimates, smaller for more reproducible work.'),
            ('arxiv', 'Henderson et al.', 2017, 'Deep Reinforcement Learning that Matters', 'https://arxiv.org/abs/1709.06560',
             'Shows how non-determinism and intrinsic variance make reported results hard to reproduce, and urges standardized reporting.'),
        ],
    ),
    "4.9": (
        r"""Historical databases get rewritten, and the rewrites are not small. Ljungqvist, Malloy and Marston downloaded the I/B/E/S analyst-recommendation history seven times between 2000 and 2007. Between 6,580 (1.6%) and 97,582 (21.7%) of matched observations differed from one download to the next, the changes were nonrandom, and they altered trading-signal classifications. Those are analyst ratings rather than accounts, but a fundamentals table faces the same mechanism.

For accounting data, Lyle, Siano and Yohn compared Compustat Snapshot, which preserves data as it existed at each point in time, with later versions of the same observations. In their working paper, Compustat's adjustments flipped the sign of reported earnings about 14% of the time and the sign of annual accruals about 8% of the time, and the variation stayed high even after restatement-related adjustments were removed. Even when no company restated, the numbers behind a screen can still move.

Without filing timestamps, researchers fall back on lags. Chen and Zimmermann, rebuilding 319 published predictors in open code, mostly use a six-month lag for annual accounting data and a one-quarter lag for quarterly data, and use the earnings report date in a couple of cases. A lag is a conservative stand-in for a timestamp, and our inference is that it gives up information.

Test that on the lesson's NCAV of 12, published on February 10 and amended to 9 on March 15. February 10 is 41 days after the December 31 period end, while a six-month lag would hold the figure back until June 30, about 140 days later. With an illustrative price of 7, the two-thirds ceiling is 8 on the original figure, so the stock passes a February 20 screen, but 6 after the amendment, so it would fail. For each decision date in your fixture, record which of three policies (timestamp, lag, latest restated) changes the buy list.""",
        [
            ('paper', 'Ljungqvist, Malloy & Marston', 2009, 'Rewriting History', 'https://doi.org/10.1111/j.1540-6261.2009.01484.x',
             'Seven downloads of the I/B/E/S recommendation history show widespread, nonrandom changes that affect back-tests of trading signals.'),
            ('paper', 'Lyle, Siano & Yohn', 2024, 'Re-Standardized Financial Statement Data', 'https://som.yale.edu/sites/default/files/2024-07/Re-Standardized%20Financial%20Statement%20Data.pdf',
             'Working paper using Compustat Snapshot to show how standardized fundamentals change over time, including sign flips in earnings and accruals.'),
            ('paper', 'Chen & Zimmermann', 2022, 'Open Source Cross-Sectional Asset Pricing', 'https://doi.org/10.1561/104.00000112',
             'Open code for 319 predictors that states its accounting-data availability lags (six months annual, one quarter quarterly).'),
        ],
    ),
    "4.10": (
        r"""The lesson's −80% delisting is realistic, and standard databases have stumbled exactly there. Shumway showed that CRSP, a widely used U.S. stock-return database, had no correct delisting return for most stocks dropped for negative reasons after 1962, and that the missing returns were large. For Nasdaq, Shumway and Warther found that the missing returns averaged large losses and that delisted stocks also became far less liquid. Substituting a corrected return of −55% wherever a performance-related delisting return was missing removed the bias, and with that fix they found no evidence that a Nasdaq size effect had ever existed.

The omission reaches fundamental screens too. Beaver and co-authors found that anomaly returns can change once delisting firm-years are added: strategies built on earnings, cash flows and book-to-market can gain, an accruals strategy can lose, and the reason is that delisting firm-years crowd into the bottom decile of those variables. Survivor-only universes can still bias recent backtests. A single-author 2026 preprint, so an order of magnitude rather than settled evidence, rebuilt NIFTY Smallcap 250 membership over nine years and found that equal-weight portfolios of current members overstated annual returns by 4.94 percentage points (23.3%) relative to all historical members. Its own reconstruction of past membership is estimated to be only 85–90% accurate.

Apply this to the two-stock case (our arithmetic). Dropping the delisted name gives +20%. Carrying its last quote forward as a 0% return gives +10%. A −55% terminal return gives −17.5%, and the lesson's −80% gives −30%. The missing-price policy alone moves the result by 50 percentage points. Exercise: rerun your fixture under each policy and report the spread before judging any rule.""",
        [
            ('paper', 'Shumway', 1997, 'The Delisting Bias in CRSP Data', 'https://doi.org/10.1111/j.1540-6261.1997.tb03818.x',
             "Documents that CRSP lacked correct delisting returns for most negative-reason delistings since 1962 and that the omitted returns were large, the origin of this lesson's terminal-value policy."),
            ('paper', 'Shumway & Warther', 1999, "The Delisting Bias in CRSP's Nasdaq Data and Its Implications for the Size Effect", 'https://doi.org/10.1111/0022-1082.00192',
             'Estimates a corrected return of −55 percent for missing performance-related Nasdaq delistings and shows that the apparent size effect disappears once the bias is corrected.'),
            ('paper', 'Beaver, McNichols & Price', 2007, 'Delisting returns and their effect on accounting-based market anomalies', 'https://doi.org/10.1016/j.jacceco.2006.12.002',
             'Shows that earnings, cash-flow, book-to-market and accruals strategy returns change when delisting firm-years are included, linking delisting bias to fundamental screens.'),
            ('arxiv', 'Ranse', 2026, "Survivorship Bias in Emerging Market Small-Cap Indices: Evidence from India's NIFTY Smallcap 250", 'https://arxiv.org/abs/2603.19380',
             'A single-author 2026 preprint that measures how much testing only current index members overstates returns; read it as an illustration of scale, not settled evidence.'),
        ],
    ),
    "4.11": (
        r"""Rank transforms are a common robustness device: in their NBER working paper on machine learning, Gu and co-authors rank each characteristic across stocks period by period, map the ranks into [−1, 1], and fill missing values with the cross-sectional median. Applied to the lesson's yields (our arithmetic, assuming a linear map), the corrected values 4, 6, 6 and 8 rank 1, 2.5, 2.5 and 4, which map to −1, 0, 0 and +1, so the tied names sit at the median. Leave the 600 in place and the ranks become 1, 2, 3 and 4. The error no longer stretches the scale, but it becomes the cheapest stock, which suggests unit checks must precede any robust transform.

Missing values raise a harder question, and the evidence is not uniform. Chen and McCoy studied 159 return predictors and found missingness in large blocks organized by time and data source, with small cross-sectional correlations. Simple cross-sectional-mean imputation therefore performed well against expectation-maximization methods, while sophisticated imputation added estimation noise. Bryzgalova and co-authors reported that over 70% of firms, together about half of market capitalization, have missing fundamentals, with systematic patterns that undermine conventional imputation, and they propose filling gaps from both time-series and cross-sectional dependence. Chen and McCoy judge imputation by machine-learning portfolio performance, while Bryzgalova and co-authors also assess risk premiums and anomalies, so part of the gap may reflect purpose (our inference).

Exercise: for each date, count the eligible names missing each field and test whether missingness predicts delisting before filling anything. Then score the two 6% names under average ranks (0 and 0) and under the lesson's symbol-order tie-break (−1/3 and +1/3), and see whether a holding changes.""",
        [
            ('paper', 'Gu, Kelly & Xiu', 2018, 'Empirical Asset Pricing via Machine Learning', 'https://doi.org/10.3386/w25398',
             'The NBER working-paper text documents a common practice: characteristics ranked across stocks period by period and mapped into [−1, 1], with missing values filled by the cross-sectional median.'),
            ('arxiv', 'Chen & McCoy', 2022, 'Missing Values Handling for Machine Learning Portfolios', 'https://arxiv.org/abs/2207.13071',
             'Studies 159 predictors and finds that missingness is organized in blocks by time and data source, so simple cross-sectional-mean imputation holds up against expectation-maximization.'),
            ('paper', 'Bryzgalova, Lerner, Lettau & Pelger', 2024, 'Missing Financial Data', 'https://doi.org/10.1093/rfs/hhae036',
             'Documents that missing fundamentals are widespread and systematic, argues that traditional imputation fails, and proposes a method using time-series and cross-sectional dependence.'),
        ],
    ),
    "4.12": (
        r"""Purging and embargoing have precise meanings. In the documentation of the skfolio library, purging removes every training observation whose label overlaps in time with a label in the test set, while embargoing removes training observations that immediately follow a test observation, because financial features can be serially correlated. López de Prado's book, which that documentation cites, devotes a chapter to cross-validation in finance, with sections on why ordinary K-fold fails and on purged K-fold with an embargo. Our reading: where training always precedes validation, as in this lesson, no training row follows the test block, so only the purge applies.

Not everyone treats shuffled K-fold as invalid. Bergmeir and co-authors showed that for a purely autoregressive model standard K-fold is possible if the models have uncorrelated errors. Overlapping labels violate that condition, because successive ten-session labels share nine sessions of return and so their errors are correlated (our inference). Cerqueira and co-authors compared cross-validation with out-of-sample methods on 62 real-world and three synthetic series. Cross-validation could be applied to stationary series, but in real-world conditions with non-stationary variation, out-of-sample methods that keep the time order gave the most accurate estimates. So keep the chronological split as the main test and use purging to repair its boundary.

Exercise: with validation starting at session 101, a ten-session label made on session t ends on t + 10, so rows 91 through 100 overlap and ten rows are purged. Repeat with five-session labels, then compare validation scores with and without the purge.""",
        [
            ('book', 'López de Prado', 2018, 'Advances in Financial Machine Learning', 'https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086',
             'Source of purged K-fold cross-validation with an embargo; its contents list a chapter on why K-fold fails in finance and one on purging the training set.'),
            ('docs', 'skfolio documentation', None, 'skfolio.model_selection.CombinatorialPurgedCV', 'https://skfolio.org/generated/skfolio.model_selection.CombinatorialPurgedCV.html',
             'Gives operational definitions of purging (labels overlapping the test set) and embargoing (observations that follow a test observation) and cites López de Prado as its source.'),
            ('paper', 'Bergmeir, Hyndman & Koo', 2018, 'A note on the validity of cross-validation for evaluating autoregressive time series prediction', 'https://doi.org/10.1016/j.csda.2017.11.003',
             "Shows when standard K-fold is valid for time series (purely autoregressive models with uncorrelated errors), which marks where this lesson's stricter rules are needed."),
            ('arxiv', 'Cerqueira, Torgo & Mozetič', 2019, 'Evaluating time series forecasting models: An empirical study on performance estimation methods', 'https://arxiv.org/abs/1905.11744',
             'Compares cross-validation and out-of-sample estimators on 62 real and three synthetic series; order-preserving methods were most accurate when non-stationary variation was present.'),
        ],
    ),
    "4.1": (
        r"""Published tests of this screen span four decades, and they show where the payoff concentrates. Oppenheimer's portfolios of stocks priced below net current asset value beat market benchmarks over 1970–83, including on a 13-year risk-adjusted basis. The edge was uneven: returns over individual 30-month holding periods varied a great deal, though the portfolios still finished ahead of the market. Two splits matter for a systematic screen. Firms with positive earnings that paid no dividends did better than earnings-positive dividend payers, and the deepest discounts, measured as price relative to net asset value, tended to deliver the largest margins over benchmarks.

Mohanty and Oxman tested a two-thirds criterion on U.S. data from 1969 to 2019, using 648 unique firms. A value-weighted portfolio averaged 1.94% a month, and after controlling for the Fama-French five factors, a liquidity factor and a January control, alpha was 1.09% a month (13.9% annually). Industry- and size-matched control portfolios showed no abnormal returns, so size alone did not explain the premium, but the strategy's profitability declined over 2004–2019. Our inference: a full-sample average can hide a rule that has weakened, so report subperiods.

Apply this to the lesson's stock. A price of 6 is 6 / 11 = 54.5% of raw NCAV but 6 / 6.6 = 90.9% of adjusted NCAV, above the 66.7% ceiling, so on Oppenheimer's measure of undervaluation the discount is shallow. Exercise: rank passing names by price as a percentage of adjusted NCAV, compare the cheapest bucket with the rest, and count passes per year before looking at returns.""",
        [
            ('paper', 'Oppenheimer', 1986, 'Ben Graham’s Net Current Asset Values: A Performance Update', 'https://doi.org/10.2469/faj.v42.n6.40',
             'Performance update on below-NCAV portfolios for 1970–83, showing variable 30-month results and the roles of positive earnings, dividends and depth of discount.'),
            ('paper', 'Mohanty & Oxman', 2026, "Does Ben Graham's net current asset value investing continue to generate excess returns?", 'https://doi.org/10.1002/rfe.70034',
             'A recent U.S. test of the two-thirds NCAV rule over 1969–2019, with factor-adjusted alpha, size- and industry-matched controls and a weaker 2004–2019 subperiod.'),
        ],
    ),
    "4.2": (
        r"""The lesson's composite has a research lineage, and its key finding is that value and quality pull in opposite directions. Novy-Marx reported that profitability, measured as gross profits over assets, forecasts average returns about as well as book-to-market does, and that profitable firms outperform even though they trade at richer valuations. Adding a profitability control lifts value strategies sharply, most of all among the largest, most liquid stocks. In an October 2013 draft, Asness and co-authors found their quality-minus-junk factor negatively correlated with the value factor HML and called the combination quality at a reasonable price. Our inference: because the two signals disagree on many names, the weights decide which side of that disagreement wins the ranking.

Their construction mirrors the lesson's formula. Each month every profitability measure is converted into ranks and standardized into a z-score, and the profitability score averages the individual z-scores. To add country-industry fixed effects in their price-of-quality regressions, they change the pool within which variables are ranked and standardized, so each country-industry pair is handled on its own. Pooled versus within-sector ranking is therefore a named design choice, not a detail. In their U.S. sample, quality accounts for only 12% of the differences in prices across stocks, so price alone says little about quality (our inference).

Use the lesson's numbers. Equal weights give 0.5, and a 50% value weight gives 0.675, a gap of 0.175 that comes from preference alone. Exercise: recompute both composites within sectors, then count how many names change rank.""",
        [
            ('paper', 'Novy-Marx', 2013, 'The other side of value: The gross profitability premium', 'https://doi.org/10.1016/j.jfineco.2013.01.003',
             'Shows that profitable firms earn higher returns despite higher valuation ratios and that controlling for profitability sharply improves value strategies, the logic for combining the two.'),
            ('paper', 'Asness, Frazzini & Pedersen', 2013, 'Quality Minus Junk', 'https://doi.org/10.2139/ssrn.2312432',
             'The October 2013 SSRN draft names quality at a reasonable price, ranks then standardizes each measure into z-scores, and varies the standardization universe to control for country and industry.'),
        ],
    ),
    "4.13": (
        r"""A catalyst deserves explicit modelling because anomaly returns cluster around news. Across 97 anomalies, Engelberg and co-authors found returns six times higher on earnings announcement days and 50% higher on days with corporate news; their tests favored biased expectations, at least in part corrected once news appears, over dynamic risk and data mining. Our reading: the same event can also disconfirm the thesis, so an earnings date is a test rather than a confirmation.

Cheapness and failure risk are entangled, and the evidence has a real tension. Campbell and co-authors estimated each firm's failure probability from accounting and market data and found that since 1981 the stocks with high estimates earned unusually low returns while showing much greater volatility, market betas and exposure to value and small-cap factors. Griffin and Lemmon, proxying distress with Ohlson's O-score, found that in the most distressed group the return spread between high and low book-to-market stocks was over twice that of other firms, and that these firms also had the sharpest reversals at earnings announcements. Both can hold: within a distressed group cheap stocks may beat expensive ones even though the group lags. A cash-burning net-net sits in exactly that corner, where payoff and failure risk coexist (both points are our inference).

Turn the lesson's cushion into a clock. With adjusted NCAV 8, price 5.5 and burn of 0.5 a quarter, the cushion is 8 − 5.5 − 0.5n, which reaches zero after (8 − 5.5) / 0.5 = 5 quarters. Exercise: for each candidate, compute the quarters of burn until the cushion is gone, and write the exit rule as a number before the next earnings date.""",
        [
            ('paper', 'Engelberg, McLean & Pontiff', 2018, 'Anomalies and News', 'https://doi.org/10.1111/jofi.12718',
             'Across 97 anomalies, returns concentrate on corporate news and earnings announcement days, evidence that mispricing is corrected when information arrives, which is what a catalyst must supply.'),
            ('paper', 'Campbell, Hilscher & Szilagyi', 2008, 'In Search of Distress Risk', 'https://doi.org/10.1111/j.1540-6261.2008.01416.x',
             'Builds a failure probability and shows that distressed stocks since 1981 delivered low, not high, returns, so cheapness caused by distress is not automatically rewarded.'),
            ('paper', 'Griffin & Lemmon', 2002, 'Book-to-Market Equity, Distress Risk, and Stock Returns', 'https://doi.org/10.1111/1540-6261.00497',
             'Finds the book-to-market return spread is largest among the most distressed firms, with the biggest reversals at earnings announcements, locating value payoffs and traps in the same group.'),
        ],
    ),
    "4.14": (
        r"""Piotroski's work shows how much a screen's average return can hide. He documented that less than 44% of high book-to-market firms earn positive market-adjusted returns in the two years after formation, so a value-only rule leans on a minority of winners. A financial-strength screen then produced a long-short return of 23% a year between 1976 and 1996, with the benefit concentrated in small and medium-sized firms, firms with low share turnover and firms with no analyst following.

Novy-Marx found that adding a profitability control sharply improves value strategies, most of all among the largest, most liquid stocks. The signals differ, so this is a contrast, not a contradiction, but a coverage or liquidity gate can remove the stocks where Piotroski's gains sat while keeping those where Novy-Marx's did. Our inference: log names and return contribution removed at every gate, and run value-only, quality-only and combined variants inside size buckets.

French's size and book-to-market portfolios show what full specification looks like: constructed at the end of each June, with NYSE breakpoints (30th and 70th percentiles for book-to-market), admitting a stock only with December and June market equity and positive prior-year book equity. State your own timing and missing-data rules as plainly.

Cattaneo and co-authors treat sorting as a nonparametric estimator and find that the optimal number of portfolios may be much larger than the usual 5 or 10. Our inference: how many names a screen keeps is the same kind of tuning choice, so report neighboring values of N and the cash each implies. Check the cap rule w = min(1/N, 0.4): N = 3 gives 33.3% each and no cash, N = 2 invests 80%, N = 1 invests 40%, and the cap binds only below N = 2.5. Count rebalance dates in each state before reading any return.""",
        [
            ('paper', 'Piotroski', 2000, 'Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers', 'https://doi.org/10.2307/2672906',
             "Shows that a value portfolio's average return hides wide dispersion, and that the gains from a financial-strength screen sit in small, thinly covered, low-turnover firms."),
            ('paper', 'Novy-Marx', 2013, 'The other side of value: The gross profitability premium', 'https://doi.org/10.1016/j.jfineco.2013.01.003',
             'Combines value with gross profitability and finds the improvement largest among big, liquid stocks, a useful contrast when comparing value-only, quality-only and combined variants.'),
            ('data', 'Kenneth R. French', None, 'Detail for 6 Portfolios Formed on Size and Book-to-Market', 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/six_portfolios.html',
             "Official documentation of a published sort: June formation, NYSE breakpoints and the data a stock needs to enter. A model for stating a screen's timing and missing-data rules."),
            ('arxiv', 'Cattaneo, Crump, Farrell & Schaumburg', 2018, 'Characteristic-Sorted Portfolios: Estimation and Inference', 'https://arxiv.org/abs/1809.03584',
             'Treats portfolio sorting as a nonparametric estimator whose number of portfolios is a tuning choice, a useful lens for how many names a screen keeps.'),
        ],
    ),
    "4.15": (
        r"""The published evidence for trend following is wide, but it comes from a different setting than the lesson's rule. Moskowitz and co-authors studied 58 liquid instruments and found persistence in returns for one to 12 months that partially reverses at longer horizons, with the best performance in extreme markets. Hurst and co-authors pushed the record back to 1880: positive average returns in each decade and good results in 8 of the 10 largest crisis periods for a 60/40 portfolio, which by implication leaves two where it did not do well. Both use diversified portfolios across many markets, so our inference is that they say little about a single-asset long/cash average rule, and that the lesson's four-close window, far shorter than one to 12 months, is a timing exercise rather than evidence of a premium.

Lempérière and co-authors add three points for your design. They report a t-statistic of about 5 since 1960 and about 10 since 1800 for excess returns after accounting for the upward drift of these markets. In our view a long/cash rule needs the same correction, because part of its return is simply being invested. They also find a saturation effect for large signals, which in our reading favors a bounded indicator like the lesson's over a position that grows with distance from the average. Finally, they find no statistical degradation of long trends, while shorter trends have significantly withered.

Check this on a longer fixture: run the four-close rule beside much longer windows. For each, report entries, the share of days invested and the excess return over the always-invested baseline under the same next-open execution, then split the sample in halves to see whether the short window's edge survives in both.""",
        [
            ('paper', 'Moskowitz, Ooi & Pedersen', 2012, 'Time series momentum', 'https://doi.org/10.1016/j.jfineco.2011.11.003',
             'Canonical study of own-history momentum across 58 liquid instruments: persistence over one to 12 months, partial reversal beyond, and strongest results in extreme markets.'),
            ('paper', 'Hurst, Ooi & Pedersen', 2017, 'A Century of Evidence on Trend-Following Investing', 'https://doi.org/10.3905/jpm.2017.44.1.015',
             'Extends the trend-following record to 1880 and reports results by decade, crisis episode and macro regime, a template for regime-by-regime reporting.'),
            ('arxiv', 'Lempérière et al.', 2014, 'Two centuries of trend following', 'https://arxiv.org/abs/1404.3274',
             'Drift-adjusted t-statistics for trend following since 1960 and 1800, a saturation effect for large signals, and evidence that short trends weakened while long trends held up.'),
        ],
    ),
    "4.16": (
        r"""Jegadeesh and Titman tested a skip in the original design. Using NYSE and AMEX stocks from 1965 to 1989, they ranked on returns over the past one to four quarters and held for one to four quarters, which gives 16 strategies. They then repeated all 16 with a one-week gap, to avoid some of the bid-ask spread, price-pressure and lagged-reaction effects. Their most successful long-short strategy, ranked on 12 months and held for 3, earned 1.31% a month with no gap and 1.49% with a one-week gap. In that sample the skip changed the return itself, so declare it before you test.

Which part of the lookback does the work? Novy-Marx found that momentum is driven mainly by performance 12 to seven months before formation, and that strategies built on the recent past are less profitable than those built on the intermediate past, especially among the largest, most liquid stocks. Split your formation window into an older and a newer segment and report each.

Falck and co-authors study factor momentum rather than stock ranking, but their spanning test, which controls for stock momentum, leaves significant Sharpe ratios only for implementations that include the last month of returns. Their stylized model has stock-level mean reversion at short lags and momentum at longer lags. Our inference is that the treatment of the most recent segment can decide whether a result exists.

A skip does not remove crash risk. Daniel and Moskowitz found infrequent, persistent strings of losses that occur in panic states, after market declines and when volatility is high, and coincide with market rebounds. Before trusting a top-two portfolio, line up its worst months against that pattern.""",
        [
            ('paper', 'Jegadeesh & Titman', 1993, 'Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency', 'https://doi.org/10.1111/j.1540-6261.1993.tb04702.x',
             "Original formation-by-holding grid for relative-strength strategies, run with and without a one-week gap, with the gap's stated purpose and its effect on the best strategy's return."),
            ('paper', 'Novy-Marx', 2012, 'Is momentum really momentum?', 'https://doi.org/10.1016/j.jfineco.2011.05.003',
             'Shows that the older part of the formation window carries more of the momentum signal than the recent past, which matters when choosing lookback and skip.'),
            ('paper', 'Daniel & Moskowitz', 2016, 'Momentum crashes', 'https://doi.org/10.1016/j.jfineco.2015.12.002',
             'Documents momentum crashes in panic states after market declines and shows a dynamic strategy that roughly doubles alpha and Sharpe ratio, so a skip month is no crash protection.'),
            ('arxiv', 'Falck, Rej & Thesmar', 2020, 'Is Factor Momentum More than Stock Momentum?', 'https://arxiv.org/abs/2009.04824',
             'A spanning test of factor momentum against stock momentum in which only implementations that include the last month of returns stand out, plus a model with short-lag mean reversion.'),
        ],
    ),
    "4.17": (
        r"""Start with the bounce itself. Roll showed that when fundamental value fluctuates randomly, trading costs still induce negative serial dependence in successive observed price changes, and that the effective spread can be inferred from the first-order serial covariance of price changes. In our reading, a negative covariance in trade prices is therefore a reason to suspect the spread before suspecting a signal. For the lesson's prints, alternating between 99.9 and 100.1 gives changes of +0.2, −0.2, +0.2 and so on, so consecutive changes multiply to −0.04, while the midpoint stays at 100.0 and never changes.

Tradable reversal is a separate claim, tied to a horizon. Lehmann studied weeks and found that one week's winners and losers reverse sizeably the next week, with apparent arbitrage profits that persisted after corrections for bid-ask spreads and plausible transaction costs. He read this as probably reflecting inefficiency in the market for liquidity around large price changes. Within the day, Heston and co-authors report that short-term reversal is driven by temporary liquidity imbalances lasting less than an hour as well as bounce. Our inference: a daily-close rule can capture multi-day effects like Lehmann's, not the sub-hour one.

The cost side is not constant either. Zawadowski and co-authors examined liquid stocks after large intraday price changes and found significant reversals after both falls and rises. On the NYSE, though, a large widening of the bid-ask spread eliminated most of the contrarian profits, while on NASDAQ the spread stayed almost constant and profits survived. Use the quote at the signal time, subtract both legs of the round trip, and rerun with a delayed entry.""",
        [
            ('paper', 'Roll', 1984, 'A Simple Implicit Measure of the Effective Bid-Ask Spread in an Efficient Market', 'https://doi.org/10.1111/j.1540-6261.1984.tb03897.x',
             'Classic result that trading costs create negative serial dependence in observed price changes even when value is a random walk, so apparent reversal in trade prices measures spread.'),
            ('paper', 'Lehmann', 1990, 'Fads, Martingales, and Market Efficiency', 'https://doi.org/10.2307/2937816',
             'Weekly winner-loser reversals whose apparent profits survive corrections for bid-ask spreads and plausible transaction costs, interpreted as a liquidity effect around large price changes.'),
            ('arxiv', 'Heston, Korajczyk & Sadka', 2010, 'Intraday Patterns in the Cross-section of Stock Returns', 'https://arxiv.org/abs/1005.3535',
             'Attributes short-term reversal to temporary liquidity imbalances lasting under an hour plus bid-ask bounce, which limits what daily bars can reveal.'),
            ('arxiv', 'Zawadowski, Andor & Kertész', 2004, 'Short-term market reaction after extreme price changes of liquid stocks', 'https://arxiv.org/abs/cond-mat/0406696',
             'After large intraday moves in liquid stocks, reversals are significant, but a widening NYSE spread removed most contrarian profit while a steady NASDAQ spread did not.'),
        ],
    ),
    "4.18": (
        r"""Your buffer has a name in the literature: a buy/hold spread. Novy-Marx and Velikov found it the most effective cost-mitigation technique they tested. Most anomalies with turnover below 50% a month kept significant net spreads when designed to cut costs, while few with higher turnover did. Their working paper gives the rule's shape: a 10%/20% rule buys only stocks entering the top 10% and sells only those leaving the top 20%, the same structure as admitting a top-ten name and holding it until rank fifteen. The same paper puts average round-trip costs for typical value-weighted strategies above 50 bps, though they have fallen over the last decade.

Why does a band make sense? Rej and co-authors show that with linear costs the optimal trading speed is zero inside a band, and that adding small quadratic costs narrows the band and lets speed grow with the distance outside it. Gârleanu and Pedersen derive a related partial-adjustment policy: the new portfolio blends the existing one with an aim portfolio, and slower-decaying signals get more weight in the aim. Our inference is that a buffer's width should depend on cost size and signal decay, so it is a design choice you can reason about before touching the holdout.

Rerun the lesson's cost arithmetic at a harsher level. Splitting 50 bps evenly gives 25 bps per side, so 1.2 times equity of traded notional costs 0.003 instead of 0.0024. Then compare exit ranks of 10 (no buffer), 12, 16 and 20 on turnover, net result and worst period, and choose with the tie-break you declared in advance.""",
        [
            ('paper', 'Novy-Marx & Velikov', 2016, 'A Taxonomy of Anomalies and Their Trading Costs', 'https://doi.org/10.1093/rfs/hhv063',
             'Finds that a buy/hold spread, stricter to enter than to keep, is the most effective trading-cost mitigation, and that net spreads survive mainly for low-turnover strategies.'),
            ('paper', 'Gârleanu & Pedersen', 2013, 'Dynamic Trading with Predictable Returns and Transaction Costs', 'https://doi.org/10.1111/jofi.12080',
             'Closed-form optimal policy that trades partially toward an aim portfolio, weighting slower-decaying signals more, a counterpart to hard buffers.'),
            ('arxiv', 'Rej et al.', 2015, 'Optimal Trading with Linear and (small) Non-Linear Costs', 'https://arxiv.org/abs/1511.07359',
             'Derives a no-trade band under linear costs and shows how small quadratic costs narrow it and make trading speed grow outside it.'),
        ],
    ),
    "4.3": (
        r"""Published pair strategies hedge in different ways, which is the lesson's notional-versus-beta-versus-spread distinction in practice. Gatev and co-authors matched stocks by minimum distance between normalized historical prices, with no fitted coefficient in our reading. A simple rule on daily data over 1962–2002 earned average annualized excess returns of up to 11% for self-financing portfolios of pairs, typically above conservative cost estimates, and they link the profit to a common factor in returns that differs from conventional risk measures.

Avellaneda and Lee regress each stock on PCA factors or sector ETFs and treat the residual as mean-reverting, so the hedge targets factor exposure rather than one partner. They standardize the residual's distance from equilibrium (their s-score), open at 1.25 standard deviations, close within 0.5 and estimate on a 60-day window, which corresponds roughly to one earnings cycle. They chose the cutoffs empirically from simulations over 2000 to 2004, inside a backtest running from 1997 to 2007, so part of the reported period also shaped the thresholds (our reading). After an assumed 5 basis points per trade, PCA strategies averaged a Sharpe ratio of 1.44 over 1997 to 2007 but only 0.9 in 2003–2007, and ETF strategies degraded similarly since 2002.

Guijarro-Ordonez and co-authors generalize the idea by building arbitrage portfolios as residuals from conditional latent factors; a pair is then the single-partner special case (our inference).

For the lesson's trade, 108 short against 100 long leaves 8 net short, 3.8% of 208 gross. Re-estimate the z-score on a 60-observation window, compare entry at 1.25 and 2 standard deviations, and report each half of the sample separately.""",
        [
            ('paper', 'Gatev, Goetzmann & Rouwenhorst', 2006, 'Pairs Trading: Performance of a Relative-Value Arbitrage Rule', 'https://doi.org/10.1093/rfs/hhj020',
             'Original distance-method study of pairs trading in daily US data 1962 to 2002, with excess returns, cost robustness and a link to a common factor.'),
            ('paper', 'Avellaneda & Lee', 2010, 'Statistical arbitrage in the US equities market', 'https://doi.org/10.1080/14697680903124632',
             'Factor-residual statistical arbitrage with a 60-day window, entry and exit cutoffs, an assumed 5 bps cost per trade and Sharpe ratios that fell after 2002 (window, cutoffs and cost from the author-hosted version).'),
            ('arxiv', 'Guijarro-Ordonez, Pelger & Zanotti', 2021, 'Deep Learning Statistical Arbitrage', 'https://arxiv.org/abs/2106.04028',
             'Frames statistical arbitrage as residual portfolios from conditional latent factors, a generalization of single-partner pairs.'),
        ],
    ),
    "4.19": (
        r"""Cointegration describes the gap this lesson points to. Engle and Granger call series co-integrated when each needs differencing to become stationary but some linear combination does not, so deviations from equilibrium have finite variance although the series themselves do not. Economic closeness does not guarantee the property: in their examples consumption and income were co-integrated, but wages and prices were not.

Graziano's single-pair study of PepsiCo and Coca-Cola shows the lesson's steps in order. Over 2013–2018 the two daily return series had a sample correlation of 0.66, yet augmented Dickey–Fuller tests could not reject a unit root in either log-price. An Engle–Granger test with critical values adjusted for the estimated hedge ratio then rejected the null of no cointegration (p = 0.033), and an AR(1) coefficient of 0.9785 on the spread implied a half-life of about 31.9 trading days, matching the lesson's formula. On the later out-of-sample window, re-estimating the hedge ratio gave −0.2376 against 1.6618, and the test no longer rejected (p = 0.12). One pair is an illustration, not a base rate.

Half-lives near φ = 1 are fragile. Yu notes that standard estimators of the mean-reversion parameter are biased in finite samples, and that a simple bias formula works poorly when reversion is slow, a case he calls empirically realistic for financial series. By our arithmetic, φ = 0.99 instead of 0.9785 more than doubles the half-life, to about 69 days, while the lesson's toy φ = 0.8 gives only 3.1.

Exercise: estimate φ on the formation window and again on the validation window. If the half-life more than doubles, or exceeds your maximum holding time, treat the pair as unproven.""",
        [
            ('paper', 'Engle & Granger', 1987, 'Co-Integration and Error Correction: Representation, Estimation, and Testing', 'https://doi.org/10.2307/1913236',
             'Defines co-integration and develops the residual-based tests; its examples show that economically related series can fail the test.'),
            ('paper', 'Yu', 2012, 'Bias in the estimation of the mean reversion parameter in continuous time models', 'https://doi.org/10.1016/j.jeconom.2012.01.004',
             'Shows that standard estimators of the mean-reversion speed are biased, and that slow reversion (the near-unit-root case) is the hard one.'),
            ('arxiv', 'Graziano', 2026, 'From Cointegration to Out-of-Sample Failure: A Pairs-Trading Case Study on PEP-KO', 'https://arxiv.org/abs/2609.35359',
             'A recent single-author, single-pair case study that walks through ADF, Engle–Granger and AR(1) half-life steps and then tests them out of sample.'),
        ],
    ),
    "4.20": (
        r"""The short leg is where a pair stops being symmetric. Under SEC Regulation SHO a broker-dealer needs reasonable grounds to believe a stock can be borrowed before it effects a short sale, and a stock that falls at least 10 percent in one day triggers a price test on short-sale prices for the rest of that day and the following day. Our inference: a long leg can fill while the short leg is refused or delayed.

Borrowing can also change after entry. Engelberg and co-authors describe two risks peculiar to short sellers, that stock loans become expensive and that they are recalled, and find that stocks with greater exposure to this risk earn lower returns, are priced less efficiently and are shorted less. Glover and Hulley model recall risk alongside margin risk, where a short seller who cannot fund a margin call is forced out, and find that realistic constraints cost a substantial amount of value. In our reading, that supports a cash-reserved unwind rule.

Do and Faff charged commissions, market impact and short selling fees on U.S. pairs trading from 1963 to 2009. Well-matched pairs stayed profitable at about 30 basis points a month, risk-adjusted, but pairs trading was largely unprofitable after 2002.

Check the lesson's example. Net profit is 120 − 40 − 50 = 30. With the 120 gross gain and 40 of fees held fixed, the pair breaks even at a borrow rate of 9.6% a year, because 80 of borrow cost on 10,000 for 30/360 of a year is 9.6% annualised (our arithmetic). Then trace a recall on day 10: which leg is left open, and which cash reserve pays to close it?""",
        [
            ('official', 'U.S. SEC', None, 'Key Points About Regulation SHO', 'https://www.sec.gov/investor/pubs/regsho.htm',
             "Regulator's summary of the locate requirement, close-out rule and the price test that applies after a 10 percent one-day fall."),
            ('paper', 'Engelberg, Reed & Ringgenberg', 2018, 'Short-Selling Risk', 'https://doi.org/10.1111/jofi.12601',
             'Shows that the risk of loans becoming expensive or being recalled is priced across stocks, which is the borrow risk the lesson asks you to record.'),
            ('arxiv', 'Glover & Hulley', 2019, 'Short Selling with Margin Risk and Recall Risk', 'https://arxiv.org/abs/1903.11804',
             'Optimal-stopping model of a short seller who can be forced out by margin calls or stock recalls, with the value lost to each friction.'),
            ('paper', 'Do & Faff', 2012, 'Are Pairs Trading Profits Robust to Trading Costs?', 'https://doi.org/10.1111/j.1475-6803.2012.01317.x',
             'U.S. evidence, 1963 to 2009, that pairs trading survives commissions, market impact and short selling fees only at modest levels.'),
        ],
    ),
    "4.21": (
        r"""A widening spread is ambiguous, and tests alone cannot settle it. Gregory and Hansen built residual-based cointegration tests that allow one break of unknown timing in the intercept or slope. In their limited experiments the tests detected cointegration across such a break, while the conventional ADF test, which allows no regime shift, lost power sharply. Our inference: after a merger or divestiture, a failed standard re-test fits both a broken link and a shifted but intact one, so the economic evidence must decide, and a re-estimated model still needs later data.

A stop is a separate design choice. Leung and Li model the spread as an Ornstein–Uhlenbeck process and show that, with a stop-loss, the entry region is a bounded interval strictly above the stop level, and that raising the stop level always lowers the optimal take-profit level. Their stop sits below a long position, so for the lesson's short spread our mirror-image reading is that a nearer stop pairs with a nearer profit target, making the 0.5 exit and 3.5 stop one design. We infer that Ornstein–Uhlenbeck paths do not jump, so that model can fill at the stop while the lesson's overnight gap cannot.

Do and Faff found that pairs-trading profits kept trending down, yet the strategy did well in long stretches of market turmoil, the global financial crisis among them. Our inference: outcomes differ by regime, so recheck stops and holding limits on another stretch.

Exercise: with entry at 2, exit at 0.5 and stop at 3.5, planned gain and planned loss are both 1.5 z-units. A fill at 4.2 after the gap loses 2.2, about 47% more than planned. Repeat for gaps ending at 5 and 6.""",
        [
            ('paper', 'Gregory & Hansen', 1996, 'Residual-based tests for cointegration in models with regime shifts', 'https://doi.org/10.1016/0304-4076%2869%2941685-7',
             'Cointegration tests that allow one break of unknown timing, and a simulation showing the conventional ADF test loses power when the relationship shifts.'),
            ('arxiv', 'Leung & Li', 2014, 'Optimal Mean Reversion Trading with Transaction Costs and Stop-Loss Exit', 'https://arxiv.org/abs/1411.5062',
             'Optimal entry and exit for an Ornstein–Uhlenbeck spread, and how a stop-loss level changes the entry region and the take-profit level.'),
            ('paper', 'Do & Faff', 2010, 'Does Simple Pairs Trading Still Work?', 'https://doi.org/10.2469/faj.v66.n4.1',
             'U.S. evidence of a long decline in pairs-trading profitability alongside strong results in prolonged turbulence, so regimes matter.'),
        ],
    ),
    "4.4": (
        r"""Gu and co-authors give a large-scale template for this lesson's contract. They fit models on 1957–1974, tuned hyperparameters on 1975–1986 and tested on 1987–2016, refitting once a year with the training sample growing by one year. Their baselines matter. Ordinary least squares on all 920 features scored a monthly out-of-sample R² of −3.46%, worse than forecasting zero, while least squares on size, value and momentum alone scored 0.16% and an elastic net 0.11%. In our reading, that is the lesson's ridge shrinkage (a penalty of 2 cutting 1.5 to 1) at scale. Trees and neural networks did best, with gains traced to nonlinear interactions, and a value-weighted long-short decile strategy built on neural-network forecasts earned an annualized out-of-sample Sharpe ratio of 1.35.

The economic layer can change the verdict. Avramov and co-authors report that deep-learning profits come from difficult-to-arbitrage stocks and high limits-to-arbitrage states. Removing microcaps, distressed stocks or turbulent periods shrinks the profits a lot, and realistic trading costs cut them further because the strategies turn over heavily and hold extreme positions.

Chen and co-authors fit a deep network to individual stock returns using the no-arbitrage condition as the training criterion, and report that it beats every benchmark they tried out of sample on Sharpe ratio, explained variation and pricing errors. Our contrast: the training objective, not only the model class, is a design choice.

Exercise: on your held-out dates, report the top-minus-bottom spread three ways: all stocks, without the smallest and least liquid, and after your cost per traded notional. If the edge vanishes in the last two, the allocation rule is the weak link, not the model.""",
        [
            ('paper', 'Gu, Kelly & Xiu', 2020, 'Empirical Asset Pricing via Machine Learning', 'https://doi.org/10.1093/rfs/hhaa009',
             'Time-ordered training, validation and test design for stock-level return forecasts, with linear baselines, flexible models and long-short portfolio results.'),
            ('paper', 'Avramov, Cheng & Metzker', 2023, 'Machine Learning vs. Economic Restrictions: Evidence from Stock Return Predictability', 'https://doi.org/10.1287/mnsc.2022.4449',
             'Shows that deep-learning profits shrink once microcaps, distressed stocks, volatile episodes and trading costs are handled.'),
            ('arxiv', 'Chen, Pelger & Zhu', 2019, 'Deep Learning in Asset Pricing', 'https://arxiv.org/abs/1904.00745',
             'Neural-network asset pricing model for individual stocks that uses the no-arbitrage condition as its training criterion.'),
        ],
    ),
    "4.22": (
        r"""Varma and Simon show why the outer block must stay out of selection. They generated classification datasets in which the two classes did not differ, tuned each classifier by minimizing cross-validated error, and read that same error as its performance. The estimate was below 30% on 18.5% of datasets for shrunken centroids and on 38% for support vector machines, yet on independent data both were no better than chance. A nested procedure, tuning in an inner loop and scoring in an outer one, cut the bias substantially. Cawley and Talbot add that over-fitting the selection criterion is often comparable in size to the performance gaps between learning algorithms. Our inference: a flexible model with more knobs can win by selection alone.

The outer score has limits too. Bates and co-authors prove, for least squares, that cross-validation measures how a procedure performs on average across fresh training sets, not how the one fitted model will do, and that standard intervals can cover the true error far less often than claimed because fold accuracies are correlated. Bergmeir and co-authors show that ordinary K-fold cross-validation is valid for purely autoregressive models whose errors are uncorrelated. Overlapping forward labels, as in the lesson, produce correlated errors, so our inference is that purging stays necessary.

Exercise: replace your features with random noise, keep the real labels and the lesson's 1–120 and 121–140 split, and run the whole inner selection. The winning inner score is the optimistic number; the frozen 121–140 score should show no skill.""",
        [
            ('paper', 'Varma & Simon', 2006, 'Bias in error estimation when using cross-validation for model selection', 'https://doi.org/10.1186/1471-2105-7-91',
             "Null-data simulations showing that a tuned classifier's own cross-validated error is badly optimistic, while nested cross-validation comes close to independent test error."),
            ('paper', 'Cawley & Talbot', 2010, 'On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation', 'https://jmlr.org/papers/v11/cawley10a.html',
             'Shows that over-fitting the model-selection criterion can be as large as the differences between algorithms, making some evaluation practices unreliable.'),
            ('arxiv', 'Bates, Hastie & Tibshirani', 2021, 'Cross-validation: what does it estimate and how well does it do it?', 'https://arxiv.org/abs/2104.00673',
             'Proves what cross-validation actually estimates and why its usual confidence intervals are too narrow, and proposes a nested scheme for the variance.'),
            ('paper', 'Bergmeir, Hyndman & Koo', 2018, 'A note on the validity of cross-validation for evaluating autoregressive time series prediction', 'https://doi.org/10.1016/j.csda.2017.11.003',
             'Gives the conditions under which ordinary K-fold cross-validation is valid for autoregressive forecasting, a counterpoint to always using forward chaining.'),
        ],
    ),
    "4.23": (
        r"""The bridge from rank correlation to money is the fundamental law of active management: the information ratio (IR, excess return divided by its volatility) depends on IC and on breadth, roughly the number of independent bets. Zhang and co-authors extend that classic relationship with IC volatility and turnover cost. Through derivations and simulations, for mean-variance and quintile portfolios alike, they find a turnover-adjusted IR always lower than one that ignores cost, and that limiting turnover may raise IR, contrary to the law's implication. Our reading: an IC table needs a turnover column, since a higher-IC model that trades far more can still lose.

Constraints separate score from holdings. Clarke and co-authors note that short and turnover limits are common and materially restrictive, and derive an ex post split of performance into the success of return prediction and the noise that constraints add, illustrated with equity portfolios benchmarked to the S&P 500. A long-only top bucket need not capture everything a long-short spread shows.

Statistical fit and profit can diverge. Leitch and Tanner asked why firms buy professional forecasts when a naive model looks about as good on root-mean-squared or mean absolute error. They argued such statistics may not be closely related to profits, and found only very weak relationships. Rank IC is another summary statistic, so the same caution applies (our inference).

Check the lesson's numbers: of the six possible orderings of three assets, three score 0.5 or better, so a random ranking does at least as well as the worked example half the time. For your own run, tabulate IC by date (mean, standard deviation, share positive) beside traded notional and the net return of the holdings actually held.""",
        [
            ('arxiv', 'Zhang, Wang & Cao', 2021, 'Turnover-Adjusted Information Ratio', 'https://arxiv.org/abs/2105.10306',
             "Extends the fundamental law's IC-and-breadth relationship with IC volatility and turnover cost; a turnover-adjusted IR is always lower, and limiting turnover can raise IR."),
            ('paper', 'Clarke, de Silva & Thorley', 2002, 'Portfolio Constraints and the Fundamental Law of Active Management', 'https://doi.org/10.2469/faj.v58.n5.2468',
             'Derives ex ante and ex post relationships for constrained portfolios, separating the success of return prediction from the noise that short and turnover limits add.'),
            ('paper', 'Leitch & Tanner', 1991, 'Economic Forecast Evaluation: Profits versus the Conventional Error Measures', 'https://ideas.repec.org/a/aea/aecrev/v81y1991i3p580-90.html',
             'Finds only very weak links between RMSE-type error statistics and forecast profits, a precedent for judging rank IC by economic value as well.'),
        ],
    ),
    "4.24": (
        r"""An ablation is only as fair as the effort behind its simpler arm. Melis and co-authors re-evaluated popular neural language-model architectures under large-scale automatic hyperparameter tuning and found that standard LSTM architectures, when properly regularised, outperform more recent models. Earlier comparisons had used differing code bases and limited computing, uncontrolled sources of variation. If the full rule gets a tuning search and the matched simpler rule does not, the gap in the lesson's formula may measure search effort, not information. A 0.1-point gain (4.1% against 4%) could be exactly that (our inference).

Negative controls are a laboratory staple that Lipsitch and co-authors argue epidemiology should use more often. They distinguish exposure controls from outcome controls, which can detect suspected and unsuspected sources of spurious causal inference, yet they conclude that more work is needed to specify when controls sensitively detect other errors. A control reassures only about the failure it was built to expose. A forecasting analogue (our inference): shuffle scores within each date, so market-wide moves survive and stock-level information does not; its rank-IC distribution should centre on zero.

Data leakage is widespread enough to be the first suspect when a control looks too good. Kapoor and Narayanan found 17 research fields with reported errors, affecting 329 papers, and proposed a taxonomy of 8 leakage types. In civil-war prediction, every paper claiming that complex machine-learning models beat logistic regression failed to reproduce because of leakage, and the complex models did not perform substantively better.

Exercise: give the baseline the same tuning budget, run a shuffled-score control under several fixed seeds, and repeat every row at doubled costs. Report each paired difference, including losses, and the number of rows tried.""",
        [
            ('arxiv', 'Melis, Dyer & Blunsom', 2017, 'On the State of the Art of Evaluation in Neural Language Models', 'https://arxiv.org/abs/1707.05589',
             'Re-tuning older architectures under the same large-scale search made standard LSTMs beat newer models, a warning that ablations need matched tuning effort.'),
            ('paper', 'Lipsitch, Tchetgen Tchetgen & Cohen', 2010, 'Negative Controls', 'https://doi.org/10.1097/EDE.0b013e3181d61eeb',
             'Explains exposure and outcome negative controls and how they detect spurious inference, while noting that their sensitivity to other errors still needs study.'),
            ('arxiv', 'Kapoor & Narayanan', 2022, 'Leakage and the Reproducibility Crisis in ML-based Science', 'https://arxiv.org/abs/2207.07048',
             'Surveys leakage across 17 fields, gives a taxonomy of 8 types, and shows complex models losing their edge over logistic regression once leakage is fixed.'),
        ],
    ),
    "4.25": (
        r"""Volatility targeting rests on volatility clustering: high volatility in the recent past tends to be followed by high volatility soon after. Published tests disagree on whether scaling by inverse volatility still pays when traded in real time. Moreira and Muir found that portfolios taking less risk when volatility is high earned large alphas and higher Sharpe ratios across equity factors and the currency carry trade, because volatility swings are not offset by proportional swings in expected returns. Cederburg and co-authors, using 103 equity strategies, found that volatility-managed portfolios do not systematically beat their unmanaged counterparts in direct comparisons. The strategies implied by spanning-regression alphas cannot be traded in real time, and reasonable out-of-sample versions generally earned lower certainty-equivalent returns and Sharpe ratios, mainly because of structural instability in those regressions.

Harvey and co-authors, covering more than 60 assets, with US equity data from 1926, found higher Sharpe ratios for equities and credit but negligible effects for bonds, currencies and commodities, and fewer extreme returns across assets. Our inference: the stronger case for a target is tail control, not extra return.

Leverage and turnover matter too. Bianco and Bernardi report that smoothing volatility forecasts reduces excess leverage and turnover and improves risk-adjusted returns after transaction costs, and that superior forecasting accuracy does not guarantee superior portfolio performance.

Apply it to the lesson's numbers. With no floor, a 1.2 cap binds whenever the estimate is below 10% / 1.2 ≈ 8.3%, and a floor at or above that level would make the cap redundant (our arithmetic). Replay your prices with two estimator windows and report how often the cap binds, the multiplier's turnover and the worst day, not just a Sharpe ratio.""",
        [
            ('paper', 'Moreira & Muir', 2017, 'Volatility-Managed Portfolios', 'https://doi.org/10.1111/jofi.12513',
             'Reports that cutting exposure when volatility is high raised alphas and Sharpe ratios for the market, equity factors and the currency carry trade.'),
            ('paper', "Cederburg, O'Doherty, Wang & Yan", 2020, 'On the performance of volatility-managed portfolios', 'https://doi.org/10.1016/j.jfineco.2020.04.015',
             'Tests 103 equity strategies as a real-time investor would; the strategies implied by spanning-regression alphas are not implementable and out-of-sample volatility management often earns less.'),
            ('paper', 'Harvey et al.', 2018, 'The Impact of Volatility Targeting', 'https://doi.org/10.3905/jpm.2018.45.1.014',
             'More than 60 assets, with US equities back to 1926: scaling lifts Sharpe ratios for equities and credit, not for bonds, currencies or commodities, and reduces extreme returns.'),
            ('arxiv', 'Bianco & Bernardi', 2022, 'Flexible variational approximations for stochastic volatility-managed portfolios', 'https://arxiv.org/abs/2212.07288',
             'Shows that smoothing volatility forecasts cuts excess leverage and turnover and improves after-cost results, and that forecast accuracy alone does not ensure better portfolios.'),
        ],
    ),
    "4.26": (
        r"""The lesson's algebra generalises to N sleeves, and the result is a floor on diversification. With N equally weighted sleeves of volatility σ and the same pairwise correlation ρ, portfolio variance is

$$
\sigma_p^2=\sigma^2\left[\rho+\frac{1-\rho}{N}\right],
$$

so volatility cannot fall below σ√ρ however many sleeves you add (our algebra). At σ = 20% and ρ = 0.5 that floor is 14.14%, the figure the lesson reaches with two uncorrelated sleeves. Polakow and Gebbie make a related point about breadth, the number of independent bets. Applying a singular value decomposition to the return correlation matrix, they estimated South African breadth as considerably lower than anticipated, and suggest concentration and commodity-cycle and currency exposure as possible causes.

Estimating the inputs is the next hazard. Ledoit and Wolf averaged the sample covariance matrix with a single-index matrix using optimal weights; for NYSE and AMEX stocks from 1972 to 1995 this selected portfolios with significantly lower out-of-sample variance than existing estimators, including multifactor models. Bun and co-authors review random-matrix tools for estimating large covariance matrices and report that, in a financial application, their rotationally invariant estimator was superior to all previously proposed methods. Jagannathan and Ma add a twist: requiring non-negative weights can reduce risk in estimated optimal portfolios even when the constraint is wrong, and with it the sample covariance matrix did as well as factor-model, shrinkage and daily-data estimates. Our inference: a long-only run already imposes that constraint, so test whether a fancier estimator changes your allocation at all.

Exercise: estimate your sleeves' correlation over the full sample and over your weakest months, then compare equal weights with the capped allocation under both matrices and under correlation one.""",
        [
            ('arxiv', 'Polakow & Gebbie', 2006, 'How many independent bets are there?', 'https://arxiv.org/abs/physics/0601166',
             'Separates the number of bets from independent breadth using the correlation matrix, finding South African breadth well below the naive count.'),
            ('paper', 'Ledoit & Wolf', 2003, 'Improved estimation of the covariance matrix of stock returns with an application to portfolio selection', 'https://doi.org/10.1016/S0927-5398%2803%2900007-0',
             'Shrinks the sample covariance matrix toward a single-index matrix and reports lower out-of-sample portfolio variance for NYSE and AMEX stocks, 1972 to 1995.'),
            ('paper', 'Jagannathan & Ma', 2003, 'Risk Reduction in Large Portfolios: Why Imposing the Wrong Constraints Helps', 'https://doi.org/10.1111/1540-6261.00580',
             'Explains why non-negative-weight constraints can cut the risk of estimated optimal portfolios even when wrong, leaving the sample covariance matrix competitive.'),
            ('arxiv', 'Bun, Bouchaud & Potters', 2016, 'Cleaning large correlation matrices: tools from random matrix theory', 'https://arxiv.org/abs/1610.08104',
             'Reviews random-matrix methods for estimating large covariance matrices and reports that a rotationally invariant estimator beat earlier methods in a financial application.'),
        ],
    ),
    "4.27": (
        r"""A flat fee per traded dollar is a placeholder, and measurement shows why. Frazzini and co-authors analysed 1.7 trillion dollars of live executions by one large institutional manager across 21 developed equity markets over 19 years. Actual trading costs were an order of magnitude smaller than earlier studies suggested, and they varied with trade type, stock characteristics, trade size, time and exchange. The lesson's 20 basis points is therefore an assumption about who trades and how, not a measurement (our inference).

Size matters, but the shape of its effect is contested. Almgren and co-authors, using Citigroup US equity trading data, rejected the common square-root model of temporary impact against trade rate in favour of a 3/5 power law across the order sizes considered. Zarinelli and co-authors studied large orders executed in U.S. equities between 2007 and 2009 and found that the square-root formula fits well across only about two orders of magnitude in size, while a logarithmic form fits across almost five. Capacity estimates are most fragile where they extrapolate beyond observed sizes (our inference).

Apply it to the lesson. A 300-share order against a 100-share cap (5% of 2,000) fills one-third; at double the capital, 600 desired shares fill one-sixth, so unfilled quantity is already a capacity signal before any impact is charged. As an illustration only, a 3/5 law raises per-share impact about 1.5 times when the trade rate doubles (our arithmetic; it was fitted to other data, not to a prior-volume cap). Exercise: run one, two and four times the capital, log fill ratio, unfilled shares and net result, and declare beforehand the fill ratio or net advantage at which the strategy counts as full.""",
        [
            ('paper', 'Frazzini, Israel & Moskowitz', 2018, 'Trading Costs', 'https://doi.org/10.2139/ssrn.3229719',
             'Live execution data from 21 developed equity markets over 19 years: real trading costs far below earlier estimates, varying with trade size, stock traits, time and exchange.'),
            ('paper', 'Almgren, Thum, Hauptmann & Li', 2005, 'Direct Estimation of Equity Market Impact', 'https://www.cis.upenn.edu/~mkearns/finread/costestim.pdf',
             'Analyses Citigroup US equity executions and rejects the square-root model of temporary impact against trade rate in favour of a 3/5 power law.'),
            ('arxiv', 'Zarinelli, Treccani, Farmer & Lillo', 2014, 'Beyond the square root: Evidence for logarithmic dependence of market impact on size and participation rate', 'https://arxiv.org/abs/1412.2152',
             'Large U.S. equity orders, 2007 to 2009: the square-root law fits only about two orders of magnitude of size, while a logarithmic form fits almost five.'),
        ],
    ),
    "4.28": (
        r"""Weyuker called a program non-testable when no oracle, a reliable way to judge its output, exists or checking takes extraordinary effort, and concluded that assuming an oracle is often unrealistic. A multi-asset backtest is plausibly non-testable in that sense (our inference); the two-share round trip is not, so it can serve as your oracle.

A second engine is the usual substitute. In a 2026 preprint, Yin and co-authors ran 15 benchmark strategies through five independent open-source engines on 180 S&P 500 stocks. With costs set to zero, all five agreed exactly, so cost handling was the only possible source of disagreement. With costs switched on they diverged: by under 0.75 percentage points for most strategies but 3.71% for high-turnover rotations, and reading the source code exposed seven defects nobody had documented. One engine processed its order queue in sequence and rejected purchases that depended on cash from sales queued after them, the case a declared sells-before-buys convention is meant to settle.

Two cautions follow (our inference). Give every fixture a nonzero fee and one purchase that only a sale can fund. And a second implementation is less independent than it sounds: Knight and Leveson had 27 versions written from one specification at two universities and ran one million tests, and the individually extremely reliable versions failed together substantially more often than expected. A ledger and an engine built from the same reading of the rules can share a misreading, so Yin and co-authors recommend validators chosen for implementation diversity.

Try it on the round trip. If the sell fee is computed from the entry price of 100 instead of the exit price of 110, final cash is 1,016.0 rather than 1,015.8. Set your test tolerance below that 0.2 gap, then predict each variant's result before running it.""",
        [
            ('paper', 'Weyuker', 1982, 'On Testing Non-Testable Programs', 'https://doi.org/10.1093/comjnl/25.4.465',
             'Defines non-testable programs, where no oracle exists or checking output is impractical, and questions the routine assumption that a tester can recognise the correct answer.'),
            ('paper', 'Knight & Leveson', 1986, 'An experimental evaluation of the assumption of independence in multiversion programming', 'https://doi.org/10.1109/TSE.1986.6312924',
             'Twenty-seven versions written independently from one specification failed together more often than independence predicts, a limit on any second-implementation check.'),
            ('arxiv', 'Yin, Miki, Lesnichenko & Gural', 2026, 'Implementation Risk in Portfolio Backtesting: A Previously Unquantified Source of Error', 'https://arxiv.org/abs/2603.20319',
             'Runs the same strategies through five open-source backtest engines: exact agreement at zero cost, cost-driven divergence otherwise, and seven undocumented defects found by source inspection.'),
        ],
    ),
    "4.29": (
        r"""Each look at a held-back segment spends some of its independence. Dwork and co-authors point out that classical inference presumes the analysis plan was settled before anyone looked at the data, whereas real analysis is adaptive: each step is shaped by exploration and by what earlier steps showed on the same data. Opening the test export, reacting and rerunning therefore makes the segment part of selection, even if no code trains on it (our reading). Their reusable holdout lets analysts query one holdout many times, drawing on privacy-preserving data analysis. The lab relies on disclosure instead, so your count of looks is the control.

Finance shows the cost too. Wiecki and co-authors studied 888 Quantopian strategies that had at least six months of out-of-sample performance. Backtest Sharpe ratios were poor predictors of that performance (R² < 0.025), and strategies that had been backtested more showed a bigger gap between backtest and out-of-sample results.

Not every drop is selection, though. Recht and co-authors built fresh CIFAR-10 and ImageNet test sets after almost a decade of heavy reuse and found accuracy drops of 3% to 15% and 11% to 14%. Their results suggest the drops did not come from adaptivity but from slightly harder images, and gains on the old test sets still carried over. A later market segment is likewise a new draw, perhaps under different conditions, so a gap like the lesson's 3% validation return and −4% test return, seven points, cannot alone separate overfitting from a changed market (our inference; their evidence comes from image classification).

Before opening the test export, write down the sign and rough size of that gap you expect, and log every look. A second look after any tweak consumes the segment: report that result as exploratory.""",
        [
            ('paper', 'Dwork et al.', 2015, 'The reusable holdout: Preserving validity in adaptive data analysis', 'https://doi.org/10.1126/science.aaa9375',
             'Explains why adaptive analysis on the same data undermines fixed-procedure inference, and shows how a holdout can be reused safely through methods from privacy-preserving analysis.'),
            ('paper', 'Wiecki, Campbell, Lent & Stauth', 2016, 'All That Glitters Is Not Gold: Comparing Backtest and Out-of-Sample Performance on a Large Cohort of Trading Algorithms', 'https://doi.org/10.3905/joi.2016.25.3.069',
             'Compares backtests with later out-of-sample results for 888 trading algorithms: backtest Sharpe ratios predict little, and more backtesting widens the gap.'),
            ('arxiv', 'Recht, Roelofs, Schmidt & Shankar', 2019, 'Do ImageNet Classifiers Generalize to ImageNet?', 'https://arxiv.org/abs/1902.10811',
             'Fresh test sets after years of reuse showed sizeable accuracy drops that the authors attribute to harder images rather than adaptivity, a caution against reading every gap as overfitting.'),
        ],
    ),
    "4.30": (
        r"""Bailey and López de Prado argue that the number of trials attempted is the key missing fact in nearly every published backtest. Their deflated Sharpe ratio uses it to correct for selection under multiple testing and for non-normal returns. Trials are rarely independent, so they shrink M dependent trials to an implied number of independent ones using the average correlation between trials. That makes the lesson's request to identify dependencies concrete: it needs each trial's return series, not only the winner's (our inference).

How large is the selection effect? For twenty independent strategies with no true edge, the expected best z-score is about 1.87 (our calculation, in standard-error units rather than Sharpe units), already above the one-sided 5% cutoff of 1.645. The lesson's 64.15% is the same selection effect stated as a probability.

Dependence also matters for intervals. Ledoit and Wolf point out that the classic test for a Sharpe-ratio difference is not valid for heavy-tailed or time-series returns, and propose a studentized time-series bootstrap interval for the difference, declaring two ratios different only if zero lies outside it. That suits comparing the selected rule with its benchmark, but it still ignores how the rule was chosen (our inference). Neither a count nor a bootstrap is a deflated Sharpe ratio.

Nor is a failed rejection proof of no effect. Chen and Dim mined 136,000 long-short strategies built from accounting ratios, past returns and ticker symbols, and found that the multiple-testing procedures common in finance miss most of the strategies that went on to perform out of sample. Report the trial count, an effective count and a benchmark-difference interval, and word a null result as "not distinguished from luck".""",
        [
            ('paper', 'Bailey & López de Prado', 2014, 'The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality', 'https://doi.org/10.3905/jpm.2014.40.5.094',
             'Argues the number of trials is the missing number in most backtests, deflates the Sharpe ratio for selection and non-normality, and converts dependent trials into an implied number of independent ones.'),
            ('paper', 'Ledoit & Wolf', 2008, 'Robust performance hypothesis testing with the Sharpe ratio', 'https://doi.org/10.1016/j.jempfin.2008.03.002',
             'Shows the standard Sharpe-difference test fails for heavy tails and time-series returns, and proposes a studentized time-series bootstrap confidence interval instead.'),
            ('arxiv', 'Chen & Dim', 2023, 'High-Throughput Asset Pricing', 'https://arxiv.org/abs/2311.10685',
             'Mines 136,000 long-short strategies and finds that popular multiple-testing methods miss most out-of-sample performers, a reminder that a failed rejection is not proof of no effect.'),
        ],
    ),
    "4.31": (
        r"""Chen and Velikov stripped three adverse effects from the returns of 204 published stock anomalies at once: effective spreads, post-publication effects and the modern era of trading technology. The average anomaly's expected return fell to 4 bps per month, and even the strongest netted at most 10 bps once data mining was controlled for, with price impact still left out.

Stacking suggests that one-at-a-time stresses can understate the damage (our inference). Saltelli and co-authors found that many analyses vary one factor at a time, along what they call one-dimensional corridors, and that 42% of the highly cited papers they analysed failed to explore the input space properly. A 2026 preprint by Deo warns that hand-chosen scenarios can miss the truly dangerous combinations or dwell on shocks too unlikely to matter.

With the lesson's numbers, doubled costs lose 4 points (5% to 1%) and the tighter cap 7 points (5% to −2%). If the effects simply added, both together would give −6%; run the combination and compare. If the return fell linearly with costs, it would hit zero at 2.25 times base costs (our inference); test that break-even directly.

On readiness, the SEC found that Knight Capital's router sent more than 4 million orders in the first 45 minutes to fill 212 customer orders, and the firm lost more than $460 million. It lacked adequate controls, including a check of outgoing orders against the customer orders entered, and 97 automated emails flagging a router error before the open went unheeded. That is more than 18,800 orders per customer order. Put a trigger like that, and an owner for it, into your pause rules.

Check the fixture too: doubling the 1% fee in the 1,015.8 round trip must cut final cash by exactly the 4.2 of base fees, to 1,011.6.""",
        [
            ('paper', 'Chen & Velikov', 2022, 'Zeroing In on the Expected Returns of Anomalies', 'https://doi.org/10.1017/S0022109022000874',
             'Nets spreads, post-publication effects and the modern trading era out of 204 anomalies at once; expected returns shrink to a few basis points a month, with price impact still omitted.'),
            ('paper', 'Saltelli et al.', 2019, 'Why so many published sensitivity analyses are false: A systematic review of sensitivity analysis practices', 'https://doi.org/10.1016/j.envsoft.2019.01.012',
             'Systematic review finding that many highly cited analyses vary one input at a time and leave most of the input space unexplored.'),
            ('arxiv', 'Deo', 2026, 'Generating Plausible Stress Scenarios via Large Deviations', 'https://arxiv.org/abs/2606.31122',
             'Warns that handpicked stress scenarios can miss dangerous configurations or dwell on implausible shocks, and proposes generating scenarios systematically from the loss itself.'),
            ('official', 'U.S. SEC', 2013, 'SEC Charges Knight Capital With Violations of Market Access Rule', 'https://www.sec.gov/newsroom/press-releases/2013-222',
             "The SEC's account of Knight Capital's 2012 incident: millions of erroneous orders, missing pre-submission controls and unheeded automated warnings."),
        ],
    ),
    "4.32": (
        r"""A dossier needs two defences that do not substitute for each other. In a 2026 preprint, Gençay built a strategy-discovery system whose tools make look-ahead impossible and which logs every strategy it tries, so reported results can be discounted by the number of trials. A deliberately leaky "oracle" strategy with a Sharpe ratio of 35 passed the deflated Sharpe ratio and probability-of-backtest-overfitting tests untouched, while honest evaluation rejected every strategy the language models discovered, which the paper lists among its main findings: a negative result as the deliverable. Our reading: statistical corrections cannot stand in for the lesson's mechanical checks, which is why unresolved look-ahead or unreconciled cash forces revision regardless of score.

Sums also hide holes. The rubric gives 25 of 100 points to timing and accounting, so a dossier that earned every other point would still total 75. Breck and co-authors' ML Test Score takes the minimum of its four section scores, choosing it because all four sections are important. Because your sections carry different maximums, report each as a share of its own maximum and flag the lowest share, not only the total.

Expect the headline to shrink. McLean and Pontiff examined 97 published return predictors and found their portfolio returns 26% lower out of sample and 58% lower once the papers appeared, reading the first drop as an upper bound on data-mining effects. State the shrinkage your dossier assumes, and remember that the fictional segments here exercise the protocol, not the market idea.

Last, rerun everything. The same ML paper lists reproducible training as a test: training twice on the same data should ideally produce identical models. Rerun the engine from a clean copy and confirm that the two-share fixture still ends at 1,015.8 and that equity.csv and the manifest figures match before you hand over the bundle.""",
        [
            ('arxiv', 'Gençay', 2026, 'What survives honest evaluation? Leakage-safe, search-aware assessment of LLM-driven trading strategy discovery', 'https://arxiv.org/abs/2608.27734',
             'Pairs structural look-ahead guardrails with trial-count deflation, shows that a planted leaky strategy passes the statistical tests, and reports that honest evaluation rejects every discovered strategy.'),
            ('paper', 'Breck et al.', 2017, 'The ML test score: A rubric for ML production readiness and technical debt reduction', 'https://doi.org/10.1109/BigData.2017.8258038',
             'A 28-test readiness rubric whose overall score is the minimum across four sections, so strength in one area cannot hide a weak one; also lists reproducible training as a test.'),
            ('paper', 'McLean & Pontiff', 2016, 'Does Academic Research Destroy Stock Return Predictability?', 'https://doi.org/10.1111/jofi.12365',
             'Documents how returns on 97 published predictors fall out of sample and after publication, the shrinkage a dossier should expect for a published idea.'),
        ],
    ),
}
