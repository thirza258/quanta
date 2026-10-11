"""Research extensions for Algorithm evaluation & results reporting.

Each entry maps a lesson ID to (body, sources). A source is
(kind, authors, year, title, url, what it contributes); see research_depth.py.
Every figure was checked against a verbatim snippet from its source before merging.
"""

NOTES = {
    "10.1": (
        r"""Other fields have a name for the lesson's rule that the limit must exist before the result does: preregistration. Nosek and co-authors describe it as fixing the research question and analysis plan before outcomes are observed. Their reason is that an idea generated from data (a postdiction) cannot also be tested on those data, yet hindsight bias makes the two feel identical. A backtest sits in exactly this position, because the researcher already knows the history. In the lesson's example, the 12% return and the 10% drawdown breach are both observations; a new limit chosen afterwards is a postdiction that needs fresh data.

Medicine supplies a measured case. Kaplan and Irvin studied 55 large cardiovascular drug and supplement trials funded by a single U.S. health institute between 1970 and 2012. Of 30 trials published before 2000, 17 (57%) reported a significant benefit on the primary outcome, against only 2 of 25 (8%) published after 2000. Registration on clinicaltrials.gov was strongly associated with that shift, and the authors say declaring outcomes in advance may have contributed. It is one field and an association, so treat it as an analogy, not proof about trading.

Harvey brought the same discipline to finance in his 2017 presidential address to the American Finance Association. Before looking at the data, he recommends fixing the economic foundation, hypotheses, sample period and exclusions, tests, statistical methods, reporting plan and robustness checks, then reporting all results. These items map onto the contract's universe, timing, execution rule, cost model, comparator and thresholds. Because preexisting data make strict preregistration harder, a later period or paper trading is, by inference rather than finding, the cleaner test of a revised rule.

Exercise: write the contract as a plain-text file with those fields and the worked example's thresholds, then store a cryptographic hash of it (or commit it) before opening any result file. After the run, list every change under a heading marked post hoc and name the new data that would test it.""",
        [
            ('paper', 'Nosek, Ebersole, DeHaven & Mellor', 2018, 'The preregistration revolution', 'https://doi.org/10.1073/pnas.1708274114',
             'Defines preregistration as fixing the question and analysis plan before outcomes are seen, and separates prediction from postdiction.'),
            ('paper', 'Kaplan & Irvin', 2015, 'Likelihood of Null Effects of Large NHLBI Clinical Trials Has Increased over Time', 'https://doi.org/10.1371/journal.pone.0132382',
             'In 55 large trials, significant benefits on the primary outcome fell from 57% before 2000 to 8% after; registration was strongly associated.'),
            ('paper', 'Harvey', 2017, 'Presidential Address: The Scientific Outlook in Financial Economics', 'https://doi.org/10.1111/jofi.12530',
             'Recommends fixing hypotheses, data choices, tests and a reporting plan before looking at the data, and reporting all results.'),
        ],
    ),
    "10.2": (
        r"""Sandve and co-authors give ten rules for reproducible computation, and three describe this lesson's export contract. Store the raw data behind every plot: a sweep that prints only a final equity per window is a figure without its data, because volatility and drawdown cannot be recomputed from it. Archive the exact program versions, here the source version, compiler and build flags. Note where randomness enters. The authors add that equal results are a strong sign of exact reproduction, while merely approximate agreement rarely lets you conclude much.

This matters when a C run is checked against Python. Floating-point addition is not associative: Goldberg's classic survey shows that with a huge x, y = −x and z = 1, (x + y) + z gives 1 while x + (y + z) gives 0. Shanmugavelu and co-authors note that summing in an unspecified parallel order is equivalent to shuffling the inputs first, and that the resulting run-to-run variability can significantly affect reproducibility. An inference, not a finding: running whole windows in parallel leaves each window's arithmetic order unchanged, but splitting one sum across threads does not. Compare fill counts for exact equality, compare equity within a tolerance declared in advance, and do not expect bitwise agreement across thread counts.

Text export can lose information too. Since version 3.1, Python's repr (on most systems) picks the shortest decimal string that converts back to the same float, but a C writer must request enough digits itself. The C++ reference gives 17 digits for a double (the C macro is DBL_DECIMAL_DIG), and Goldberg's Theorem 15 shows the same effect in single precision, where eight digits can fail and nine suffice. Too few digits alter the last places of the thirteen valuations, and so of the twelve returns.

Exercise: write the thirteen valuations from both languages (17 significant digits in C), reload them, and report the largest absolute difference between the twelve returns. Then sum the returns forward and in reverse and record that gap too. Put the tolerance you accept and the number formats in the manifest beside the SHA-256 values.""",
        [
            ('paper', 'Sandve, Nekrutenko, Taylor & Hovig', 2013, 'Ten Simple Rules for Reproducible Computational Research', 'https://doi.org/10.1371/journal.pcbi.1003285',
             'Rules on storing the data behind plots, archiving program versions and recording randomness; separates exact from approximate reproduction.'),
            ('paper', 'Goldberg', 1991, 'What every computer scientist should know about floating-point arithmetic', 'https://doi.org/10.1145/103162.103163',
             'Classic account of rounding: why addition is not associative and how many decimal digits a binary float needs to survive a text round trip.'),
            ('arxiv', 'Shanmugavelu et al.', 2024, 'Impacts of floating-point non-associativity on reproducibility for HPC and deep learning applications', 'https://arxiv.org/abs/2408.05148',
             'Shows that parallel sums in an unspecified order behave like permuted serial sums and cause run-to-run variability.'),
            ('docs', 'Python Software Foundation', None, 'Floating-Point Arithmetic: Issues and Limitations', 'https://docs.python.org/3/tutorial/floatingpoint.html',
             'Documents that repr returns the shortest string that round-trips a float, and that math.fsum limits summation error to one rounding.'),
        ],
    ),
    "10.3": (
        r"""The lesson asks you to fix the benchmark before the result, and studies of mutual funds show why. Lehmann and Modest ranked funds against several benchmarks, from CAPM to APT-style models, and found little similarity between the rankings that different benchmarks produced. Sensoy found that almost one-third of actively managed, diversified U.S. equity funds named a size and value/growth benchmark in their prospectus that did not match their actual style. Performance against the named benchmark still drove later cash inflows, and he judged the pattern consistent with strategic benchmark choice meant to attract flows. A report that picks its comparator after seeing the answer is in the same position.

A tradable index is also not a neutral yardstick once a factor model is added. Cremers, Petajisto and Zitzewitz regressed S&P 500 excess returns on the Carhart four-factor model over 1980 to 2005 and obtained an annual alpha of 0.82% (t = 2.78); the Russell 2000's was −2.41% (t = −3.21). They traced such alphas mainly to the heavy weight the Fama-French factors give small value stocks and to the CRSP value-weighted market index being a downward-biased benchmark. A comparator and a risk-factor model can therefore disagree about the same passive portfolio, which is why the lesson keeps them apart.

In the lesson's example, 11,000 against 10,800 is a two-point gap in total return, or about 1.85% in relative wealth (computed as 11,000 ÷ 10,800 − 1). Neither number is alpha, and a different justified comparator could shrink or reverse the gap; that last point is an illustration, not a finding.

Exercise: compute the gap against at least three defensible comparators, for example the same asset bought and held, a cash reference and a broad index. Name the primary comparator, and the date you chose it, in the contract, then report all three results, including the one that flatters the strategy least.""",
        [
            ('paper', 'Lehmann & Modest', 1987, 'Mutual Fund Performance Evaluation: A Comparison of Benchmarks and Benchmark Comparisons', 'https://doi.org/10.1111/j.1540-6261.1987.tb02566.x',
             'Shows that fund rankings differ greatly across CAPM and APT benchmarks, so the choice of yardstick can change the verdict.'),
            ('paper', 'Sensoy', 2009, 'Performance evaluation and self-designated benchmark indexes in the mutual fund industry', 'https://doi.org/10.1016/j.jfineco.2008.02.011',
             'Finds that about one-third of funds name a mismatched benchmark that still influences investor flows.'),
            ('paper', 'Cremers, Petajisto & Zitzewitz', 2013, 'Should Benchmark Indices Have Alpha? Revisiting Performance Evaluation', 'https://doi.org/10.1561/104.00000007',
             'Shows that passive indices earn nonzero alphas against standard factor models, separating a comparator from a risk-factor model.'),
        ],
    ),
    "10.4": (
        r"""A cost label can decide a verdict. Fama and French studied active U.S. equity mutual funds from January 1984 to September 2006. Before expenses, the value-weighted portfolio of those funds had an alpha close to zero, so the alpha earned by investors after expenses was negative by about the amount of the expenses. The same funds look neutral or poor depending on which line of the ledger is reported. In the lesson's example, costs of 300 take a quarter of the 1,200 gross gain, and subtracting them twice would leave 600 instead of 900.

Cash flows need the same care. The 2020 GIPS standards require portfolios in a composite to be valued at least monthly and on the date of all large cash flows, with sub-period returns linked geometrically. Suppose 10,000 grows 10% to 11,000, a 10,000 deposit arrives, and the account then falls 10% to 18,900. The time-weighted return is −1.0%, because it ignores the deposit's size and timing. The account holder, though, is down 1,100 on 20,000 contributed, and the money-weighted (internal) return is about −3.7% per period (computed). The two figures answer different questions: how the strategy performed, and what the investor experienced.

Do not read such a gap as bad timing by default. Dichev, as summarised by Hayley, found dollar-weighted investor returns 1.3% a year below buy-and-hold on NYSE and AMEX stocks (1926 to 2002) and 5.3% below on Nasdaq stocks (1973 to 2002). Hayley then showed that the gap mixes flows that anticipate later returns with flows that merely follow earlier ones. For mainstream U.S. equities he found that most of the difference was this hindsight effect, and very little was bad timing.

Exercise: recompute the deposit example with a smaller deposit and check that the time-weighted return is unchanged while the money-weighted return moves. Then state which of the two your report uses for a run with external flows, and why.""",
        [
            ('paper', 'Fama & French', 2010, 'Luck versus Skill in the Cross-Section of Mutual Fund Returns', 'https://doi.org/10.1111/j.1540-6261.2010.01598.x',
             'Shows that gross-of-cost and net-of-cost alphas of the same fund portfolio differ by about the expenses, so the net label changes the verdict.'),
            ('official', 'CFA Institute · GIPS Standards', 2020, '2020 GIPS Standards for Firms', 'https://www.gipsstandards.org/wp-content/uploads/2021/03/2020_gips_standards_firms.pdf',
             'Provisions 2.A.23 and 2.A.24 on valuing portfolios at large external cash flows and geometrically linking sub-period returns.'),
            ('paper', 'Dichev', 2007, "What Are Stock Investors' Actual Historical Returns? Evidence from Dollar-Weighted Returns", 'https://doi.org/10.1257/aer.97.1.386',
             'Compares dollar-weighted investor returns with buy-and-hold returns and finds investors systematically earn less.'),
            ('paper', 'Hayley', 2014, 'Hindsight Effects in Dollar-Weighted Returns', 'https://doi.org/10.1017/S0022109014000155',
             'Argues that the dollar-weighted shortfall mostly reflects flows following past returns rather than poor timing.'),
        ],
    ),
    "10.5": (
        r"""Compounding turns the choice between averages into a question of horizon. Jacquier, Kane and Marcus show that an unbiased forecast of terminal wealth compounds at the arithmetic mean return, yet compounding at the arithmetic average of a historical sample gives an upwardly biased forecast, while compounding at the geometric average is generally biased downward. For horizons of 40 years the two forecasts can differ by more than a factor of 2, and for typical horizons the proper rate lies between them. Peters and Gell-Mann argue from another direction: for wealth that grows multiplicatively, the quantity that matches one investor's path is the time-averaged growth of log wealth, not the expected change in wealth.

The lesson's +10% then −10% path shows the mechanism. The arithmetic mean is zero, but the geometric mean is about −0.501% per period. A second-order approximation puts the geometric mean near the arithmetic mean minus half the variance. Here the variance is 0.01, half of it is 0.005, and so the approximation gives −0.5%, within about a thousandth of a percentage point of the exact value (computed). The more volatile the path, the larger this drag.

Annualizing a ratio needs a dependence assumption on top of a period count. Lo derived the distribution of the Sharpe ratio under several return-generating processes and showed that monthly Sharpe ratios cannot be annualized by multiplying by √12 except under very special circumstances. In his illustrative sample, a hedge fund's annual Sharpe ratio could be overstated by as much as 65% because of serial correlation in monthly returns. That is one sample from one study, but the lesson's warning about minute bars rests on the same logic: the multiplier encodes a claim about how returns depend on each other.

Exercise: for your own return series, compute annualized volatility two ways, as the per-period standard deviation times √P and as the standard deviation of non-overlapping monthly returns times √12. If the two differ materially, report both and say which one each ratio uses.""",
        [
            ('paper', 'Jacquier, Kane & Marcus', 2003, 'Geometric or Arithmetic Mean: A Reconsideration', 'https://doi.org/10.2469/faj.v59.n6.2574',
             'Shows that compounding the arithmetic average overstates and compounding the geometric average understates long-horizon wealth.'),
            ('arxiv', 'Peters & Gell-Mann', 2014, 'Evaluating gambles using dynamics', 'https://arxiv.org/abs/1405.0585',
             'Argues that for multiplicative wealth dynamics the relevant average is the time-averaged growth of log wealth.'),
            ('paper', 'Lo', 2002, 'The Statistics of Sharpe Ratios', 'https://doi.org/10.2469/faj.v58.n4.2453',
             "Shows that the square-root-of-time rule for annualizing Sharpe ratios needs special conditions and can overstate a hedge fund's ratio."),
        ],
    ),
    "10.6": (
        r"""The lesson's 0.794 is an estimate. Sharpe observed that a historic ratio is tied to the usual significance test for the mean differential return: the t-statistic is the per-period ratio multiplied by √T, with T the number of returns. Here the daily ratio is 0.05, so one year (T = 252) gives t ≈ 0.794, the same number as the annualized ratio. Reaching t = 2 takes (2 ÷ 0.05)² = 1,600 days, about 6.3 years, if returns are independent and normal (our arithmetic).

Those assumptions are the weak point. Bailey and López de Prado derive the probability that an estimated Sharpe ratio exceeds a threshold when returns are not normal, and the record length needed to reject the hypothesis that the true ratio lies below it. Records must be longer when returns are more negatively skewed or fatter-tailed, and even a high ratio leaves the risk of severe losses open. Ho proved that with long-memory volatility the estimation error converges more slowly than √n, so the 6.3-year figure is probably too short there (our inference).

Comparing two ratios has the same trap. Ledoit and Wolf note that the popular Jobson and Korkie test, as corrected by Memmel, is not valid for tails heavier than normal or for time-series dependence. They propose a studentized time-series bootstrap interval for the difference, calling the ratios different only if zero lies outside it.

Exercise: bootstrap the strategy's and the benchmark's Sharpe ratios on the same resampled blocks, report the interval for the difference beside the years of data behind each ratio, and leave any ratio with a zero denominator missing, not infinite.""",
        [
            ('paper', 'Sharpe', 1994, 'The Sharpe Ratio', 'https://doi.org/10.3905/jpm.1994.409501',
             'Notes that the historic Sharpe ratio is closely related to the t-statistic of the mean differential return, which equals the ratio times the square root of the number of returns.'),
            ('paper', 'Bailey & López de Prado', 2012, 'The Sharpe ratio efficient frontier', 'https://doi.org/10.21314/JOR.2012.255',
             'Gives the probability that an estimated Sharpe ratio exceeds a threshold under nonnormal returns, and the track-record length needed to reject a given threshold.'),
            ('paper', 'Ledoit & Wolf', 2008, 'Robust performance hypothesis testing with the Sharpe ratio', 'https://doi.org/10.1016/j.jempfin.2008.03.002',
             'Shows why the standard test for equal Sharpe ratios fails under heavy tails or time-series dependence and proposes a studentized time-series bootstrap interval for the difference.'),
            ('arxiv', 'Ho', 2007, 'Estimation errors of the Sharpe ratio for long-memory stochastic volatility models', 'https://arxiv.org/abs/math/0702812',
             "Proves that with a long-memory latent volatility component the Sharpe ratio's estimation error converges more slowly than the square root of the sample size."),
        ],
    ),
    "10.7": (
        r"""Maximum drawdown depends on how long you look. Magdon-Ismail and co-authors studied the expected maximum drawdown of a Brownian motion with drift. As the horizon T grows, they found, it increases logarithmically with positive drift, like a square root with zero drift and linearly with negative drift. Our own simulation uses independent normal daily returns with the previous lesson's 0.05% mean and 1% standard deviation, compounded (a geometric version, not their arithmetic model). Over 252, 1,008 and 2,520 days the average maximum drawdown is about 14%, 22% and 28% (20,000 paths). The 20% fall in the lesson's four-point path is therefore weak evidence about a long run, and maximum drawdowns from histories of different lengths are not comparable (our inference).

A single trough is also one episode. For one sample path, Chekhlov and co-authors define conditional drawdown as the mean of the worst (1 − α) × 100% drawdowns; the maximal and the average drawdown are its limiting cases. Setting α = 0.95 averages the worst 5%, which shows whether one event drives the maximum.

Time under water carries information as well. Challet showed that the total duration of drawdowns can estimate the Sharpe ratio without computing moments, and reported the estimator as unbiased, efficient and robust for Gaussian and heavy-tailed returns. Depth, duration and the previous lesson's ratio are therefore connected readings of one path (our reading).

Exercise: cut the equity curve into equal windows of 252 observations. For each, report the maximum drawdown, the average drawdown, the worst-5% average and the longest spell under water, flagging an unrecovered final spell as censored.""",
        [
            ('paper', 'Magdon-Ismail, Atiya, Pratap & Abu-Mostafa', 2004, 'On the maximum drawdown of a Brownian motion', 'https://doi.org/10.1239/jap/1077134674',
             'Shows that the expected maximum drawdown of a Brownian motion grows logarithmically, as a square root or linearly with the horizon, depending on the sign of the drift.'),
            ('paper', 'Chekhlov, Uryasev & Zabarankin', 2005, 'Drawdown measure in portfolio optimization', 'https://doi.org/10.1142/S0219024905002767',
             'Defines conditional drawdown as the mean of the worst drawdowns on the underwater curve, with maximal and average drawdown as limiting cases.'),
            ('arxiv', 'Challet', 2015, 'Sharper asset ranking from total drawdown durations', 'https://arxiv.org/abs/1505.01333',
             'Shows that the total duration of drawdowns is a moment-free estimator of the Sharpe ratio for Gaussian and heavy-tailed returns, linking time under water to risk-adjusted return.'),
        ],
    ),
    "10.8": (
        r"""The lesson's 60% fill ratio hides a selection problem. Handa and Schwartz identify two risks of limit orders: executing after bad news arrives, and failing to execute after good news. For such orders, fills over-represent bad news and misses over-represent good news, so slippage averaged over filled shares alone flatters the result (our inference). With an invented later price: 60 shares filled at 100.20 cost 12 against the decision price of 100, but if the price then rose to 101, the 40 unfilled shares forgo 40, over three times as much.

Costs also depend on size. Bucci and co-authors, using 8 million institutional trades in U.S. equities, found a crossover between a linear and a square-root market-impact regime depending on order volume, so 20 basis points measured on 100 shares cannot simply be scaled up (our inference). Turnover multiplies any per-trade cost: 20 basis points on a strategy that trades five times its equity a year costs 1.0% a year (computed).

The assumed cost model can decide a verdict. Novy-Marx and Velikov found that most anomalies with under 50% monthly turnover earn significant net spreads when designed to mitigate costs, while few with higher turnover do. Frazzini and co-authors, using $1.7 trillion of one manager's live trades in 21 developed markets, found actual costs an order of magnitude below earlier estimates, so a high-turnover result may hinge on which estimate you adopt (our inference).

Exercise: rerun the same signals with doubled costs and a one-bar delay, reporting fill ratio, slippage on filled shares and the missed gain on unfilled shares, and label each figure a rerun or a hand calculation.""",
        [
            ('paper', 'Handa & Schwartz', 1996, 'Limit Order Trading', 'https://doi.org/10.1111/j.1540-6261.1996.tb05228.x',
             'Frames limit-order trading as two risks, an undesirable execution after adverse news and a missed desirable execution after favorable news; relevant to why fills alone give a biased picture.'),
            ('arxiv', 'Bucci, Benzaquen, Lillo & Bouchaud', 2018, 'Crossover from linear to square-Root market impact', 'https://arxiv.org/abs/1811.05230',
             'Uses 8 million institutional U.S. equity trades to show a crossover between linear and square-root market impact as order volume changes; relevant to why a fixed cost per trade cannot establish capacity.'),
            ('paper', 'Novy-Marx & Velikov', 2016, 'A Taxonomy of Anomalies and Their Trading Costs', 'https://doi.org/10.1093/rfs/hhv063',
             'Finds that most anomalies with under 50% monthly turnover keep significant net spreads when designed to mitigate costs, while few with higher turnover do.'),
            ('paper', 'Frazzini, Israel & Moskowitz', 2018, 'Trading Costs', 'https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs',
             'Measures real-world costs from $1.7 trillion of live trades and finds them an order of magnitude below earlier estimates; relevant to how far an assumed cost model can swing a verdict.'),
        ],
    ),
    "10.9": (
        r"""Shuffling is not always wrong, which is why the lesson's time boundary needs a reason. Bergmeir and co-authors showed that when a purely autoregressive model is fitted, ordinary K-fold cross-validation stays usable provided the candidate models leave uncorrelated errors, and they advise checking residuals for serial correlation first. A five-day forward label breaks that condition by construction. With independent daily returns, labels k days apart share (5 − k)/5 of their days, so error correlations at lags 1 to 4 are 0.8, 0.6, 0.4 and 0.2 (our arithmetic), and the argument for shuffling no longer applies (our inference).

Even where the condition holds, time order can win. Cerqueira and co-authors compared cross-validation and out-of-sample variants on 62 real-world series. Cross-validation was usable for stationary series, but when several kinds of non-stationary change were present, order-preserving out-of-sample evaluation gave the most accurate estimates. Markets plausibly belong to the second group (our inference).

The repair has a classical form. Burman and co-authors' h-block cross-validation drops from the training set the h observations on each side of the test point. In the lesson's example, the last five training observations before July 1 have labels that reach into validation, so those five are the ones to remove.

Exercise: score one model on a chronological split with and without those five rows removed, and report residual autocorrelation at lags 1 to 4. The gap between the two scores isolates label-overlap leakage. A shuffled K-fold score adds look-ahead and regime effects, so interpret its gap separately.""",
        [
            ('paper', 'Bergmeir, Hyndman & Koo', 2018, 'A note on the validity of cross-validation for evaluating autoregressive time series prediction', 'https://doi.org/10.1016/j.csda.2017.11.003',
             'Shows that standard K-fold cross-validation is valid for purely autoregressive models when errors are uncorrelated, and advises testing residuals for serial correlation first.'),
            ('arxiv', 'Cerqueira, Torgo & Mozetič', 2019, 'Evaluating time series forecasting models: An empirical study on performance estimation methods', 'https://arxiv.org/abs/1905.11744',
             'Compares cross-validation and out-of-sample methods on 62 real-world series; with non-stationary variation, order-preserving out-of-sample methods gave the most accurate estimates.'),
            ('paper', 'Burman, Chow & Nolan', 1994, 'A cross-validatory method for dependent data', 'https://doi.org/10.1093/biomet/81.2.351',
             'Introduces h-block cross-validation, which removes the h observations before and after each test observation from the training set; purging and embargo apply the same idea to overlapping labels (our reading).'),
        ],
    ),
    "10.10": (
        r"""The lesson's 64.2% treats 20 variants as independent tests. Real variants are correlated, but the core problem is the same: the winner was picked after looking. White defined data snooping as reusing the same data for inference or for choosing among models, and built a Reality Check that tests whether the best model found in a specification search beats a benchmark. Hansen's SPA test improves on it. The reality check is affected by weak or irrelevant alternatives, so padding a search with poor variants can blunt it (our paraphrase), while studentization and a sample-dependent null distribution make the test more powerful. In the arch library, the SPA class takes a T by k array of every alternative's losses, so the full search log is an input to the test, not a courtesy (our reading).

Paulsen and Söhl show the same optimism for Sharpe ratios. A ratio maximized over k fitted parameters tends to overstate what to expect on new data, and their unbiased adjustment subtracts k ÷ (T × the in-sample ratio), with T in years. Their example: k = 5, an in-sample ratio of 1 and T = 10 give 1 − 5/10 = 0.5. The formula counts fitted parameters, not discrete trials like the lesson's 20, so treat it as a rough check on tuned parameters (our inference).

Exercise: save every variant you tried, including abandoned ones, as a column of losses (negative returns), and keep the benchmark's losses beside them. Run a reality check or SPA on the whole matrix, and report that result, the block-bootstrap interval for the winner and the parameter-count adjustment as three separate lines.""",
        [
            ('paper', 'White', 2000, 'A Reality Check for Data Snooping', 'https://doi.org/10.1111/1468-0262.00152',
             'Defines data snooping as reusing one data set for inference or model selection and gives a test of whether the best model found in a search beats a benchmark.'),
            ('paper', 'Hansen', 2005, 'A Test for Superior Predictive Ability', 'https://doi.org/10.1198/073500105000000063',
             'Improves the reality check with a studentized statistic and a sample-dependent null, making it more powerful and less sensitive to poor and irrelevant alternatives.'),
            ('docs', 'arch contributors', None, 'Test of Superior Predictive Ability (SPA), Reality Check', 'https://arch.readthedocs.io/en/latest/multiple-comparison/generated/arch.bootstrap.SPA.html',
             "Shows that the SPA and Reality Check take the benchmark's loss series and a T by k array of every alternative model's losses, so the whole search must be supplied."),
            ('arxiv', 'Paulsen & Söhl', 2016, 'Noise Fit, Estimation Error and a Sharpe Information Criterion', 'https://arxiv.org/abs/1602.06186',
             'Derives an unbiased out-of-sample Sharpe estimate from the in-sample ratio, the number of fitted parameters and the years of data, with a worked example.'),
        ],
    ),
    "10.11": (
        r"""The lesson's central difference cannot see the spike. At window 20 it gives (1% − 2%) ÷ 2 = −0.5 points per step, nearly flat, though both neighbors are far lower. The second difference, 2% − 2 × 18% + 1% = −33 points, does show it (our arithmetic). A central slope misses any peak whose neighbors are alike, so judge a peak by its drop to them.

Bailey and co-authors define the probability of backtest overfitting as the chance that the best in-sample strategy underperforms the out-of-sample median. In their example, 1,000 daily random-walk prices were searched over 8,800 parameter combinations; the best reached an annualized Sharpe ratio of 1.27, yet the probability was as high as 55%. A plateau shows smoothness, not persistence (our inference). Lezmi and co-authors generate artificial multi-asset histories that keep return distribution, asset dependence and serial correlation, and read backtest statistics off the resulting distribution. That probes sampling luck, not unseen regimes (our inference).

Stress cases may exceed your sample and need a full rerun. The Bank of England reported that in September 2022 the 30-year gilt yield rose 130 basis points in three days, three times larger than any earlier move over a similar span, as forced selling by levered funds fed fire-sale dynamics; the bid-ask spread widened from about 0.5 basis points on 22 September to 2.5 by 11 October. Positions, margin and costs changed along the path, so a linear subtraction from final profit misses them (our analogy).

Exercise: state the break condition first, such as net return below cash, then find the smallest cost multiple, delay or removed sub-period that triggers it, and keep that row even if it ends the hypothesis.""",
        [
            ('paper', 'Bailey, Borwein, López de Prado & Zhu', 2017, 'The probability of backtest overfitting', 'https://doi.org/10.21314/JCF.2016.322',
             'Defines the probability that the in-sample best strategy ranks below the out-of-sample median, with a random-walk example where a 1.27 Sharpe ratio came with a 55% probability.'),
            ('arxiv', 'Lezmi, Roche, Roncalli & Xu', 2020, 'Improving the Robustness of Trading Strategy Backtesting with Boltzmann Machines and Generative Adversarial Networks', 'https://arxiv.org/abs/2007.04838',
             'Proposes synthetic multi-asset histories that preserve return distributions, cross-asset dependence and autocorrelation, to estimate the distribution of backtest statistics.'),
            ('official', 'Bank of England', 2023, 'Financial stability buy/sell tools: a gilt market case study', 'https://www.bankofengland.co.uk/quarterly-bulletin/2023/2023/financial-stability-buy-sell-tools-a-gilt-market-case-study',
             'Records the September 2022 gilt shock: a 130 basis point three-day yield rise, margin calls, forced selling and wider spreads that changed positions and costs along the path.'),
        ],
    ),
    "10.12": (
        r"""Hoefler and Belli reviewed how HPC papers report performance. Among papers from three top HPC conferences, 39 reported speedups and 15 (38%) of those omitted the absolute performance of the base case. Their rules: state whether the base is a single parallel process or the best serial execution, never report ratios without absolute values, and avoid summarizing ratios; summarize the underlying costs instead, using a geometric mean of ratios only when costs are unavailable.

On the lesson's five pairs, the median of the ratios and the ratio of median times are both 3.00. The ratio of mean times is 152 ÷ 52 ≈ 2.92 and the geometric mean of the ratios is ≈ 2.94 (computed): a small spread here, though not necessarily on skewed timings. Chen and Revels designed a timing strategy for the highly nonideal statistics of timing measurements and implemented it in Julia's BenchmarkTools. The package manual argues that machine noise is, in some sense, inherently positive, so timings are right-skewed: the minimum is a robust location estimate, the median tolerates outliers, and the mean is pulled upward. Our reading: the minimum asks what the code can do, while medians and tail percentiles describe what a run experiences.

Tails need separate evidence. In Dean and Barroso's hypothetical service, each server has a 99th-percentile latency of one second, so a request waiting on 100 of them in parallel exceeds a second 63% of the time. In a Google service they measured, the 99th-percentile latency was 10 ms for a single request but 140 ms for all requests to finish. Five timings cannot see a 1% tail: the chance that none falls in the slowest 1% is 0.99⁵ ≈ 95% (computed).

Exercise: compute all four summaries for your own paired timings, print the serial base time beside them, and state whether serial means the best serial code or the parallel code on one worker. For gateway latency, define the event population, log every event, and report the median, 99th percentile and maximum with the count.""",
        [
            ('paper', 'Hoefler & Belli', 2015, 'Scientific benchmarking of parallel computing systems', 'https://doi.org/10.1145/2807591.2807644',
             'Reviews speedup reporting in HPC papers and gives rules on the base case, absolute values and summarizing ratios.'),
            ('arxiv', 'Chen & Revels', 2016, 'Robust benchmarking in noisy environments', 'https://arxiv.org/abs/1608.04295',
             'Designs a timing strategy that tolerates timer error, OS jitter and the highly nonideal statistics of timing measurements; implemented in BenchmarkTools.'),
            ('docs', 'JuliaCI · BenchmarkTools.jl', None, 'BenchmarkTools.jl manual: which estimator should I use?', 'https://juliaci.github.io/BenchmarkTools.jl/stable/manual/',
             'Explains why timing noise is positive and right-skewed, and what the minimum, median and mean each estimate.'),
            ('paper', 'Dean & Barroso', 2013, 'The tail at scale', 'https://doi.org/10.1145/2408776.2408794',
             'Shows how rare slow components dominate a request that waits on many of them, with a hypothetical case and a measured Google service.'),
        ],
    ),
    "10.13": (
        r"""Weissgerber and co-authors reviewed 703 articles in top physiology journals and found continuous data mostly shown as bar and line graphs, which is problematic because many different data distributions can lead to the same bar or line graph and the full data may suggest different conclusions from the summary statistics. The lesson's portfolios are a case in point: bars at 110 and 108 look alike, yet the path behind one of them includes a deep drawdown. By our inference, any single summary (final wealth, annualized return, a Sharpe ratio) shares this blind spot, so a path panel belongs beside it.

Axes then decide how large an edge looks. Correll and co-authors report that bar charts whose y-axes do not begin at zero can visually exaggerate effect sizes, while for other chart types truncation can be beneficial or harmful depending on intent. In their crowd-sourced experiments the impact of truncation persisted across designs, even with explicit visual cues that truncation had occurred. A wealth index plotted from about 100 rather than 0 is already truncated, so choose its range by the size of the effect you mean to show and print the end values on the chart.

Scale type matters too. Romano and co-authors showed COVID-19 deaths on logarithmic or linear axes: log-scale viewers understood the pandemic's course less accurately, predicted its evolution less accurately and held different policy preferences, and the authors recommend a linear default for the general public. A log axis gives equal heights to equal percentage changes, which suits compounding, so label it in the caption and keep a table beside it.

Exercise: plot your strategy and comparator wealth index three ways (range from zero, tight range, log scale) and ask a colleague who has not seen the table to estimate how much larger the strategy's final wealth is than the comparator's in each. Keep the version whose answers come closest to the table, state the scale in the caption, and show the drawdown panel beneath it.""",
        [
            ('paper', 'Weissgerber, Milic, Winham & Garovic', 2015, 'Beyond Bar and Line Graphs: Time for a New Data Presentation Paradigm', 'https://doi.org/10.1371/journal.pbio.1002128',
             'Systematic review showing that bar and line graphs of summary values can hide very different underlying distributions.'),
            ('arxiv', 'Correll, Bertini & Franconeri', 2019, 'Truncating the Y-Axis: Threat or Menace?', 'https://arxiv.org/abs/1907.02035',
             'Crowd-sourced experiments on how y-axis truncation changes perceived effect size across chart types, including designs that flag the truncation.'),
            ('paper', 'Romano, Sotis, Dominioni & Guidi', 2020, 'The scale of COVID-19 graphs affects understanding, attitudes, and policy preferences', 'https://doi.org/10.1002/hec.4143',
             'Shows that log versus linear axes change how accurately people read a growth series and what they conclude from it.'),
        ],
    ),
    "10.14": (
        r"""Brinson and co-authors split returns into investment policy, market timing and security selection by comparing a passive policy portfolio with actual returns. For 91 large U.S. pension plans over 1974–83, policy explained on average 93.6% of the variation in total plan return. Yet the average plan earned 9.01% against 10.11% for the policy benchmark, so active management cost 1.10% a year. A high explained share and a negative active contribution coexisted, because the 93.6% describes variation, not the level of return.

Ibbotson and Kaplan traced the controversy to different questions. Policy explained about 90% of a typical fund's variability over time, about 40% of the variation among funds, and on average about 100% of the return level. A share means little until its denominator is named. The lesson's 700 ÷ 900 ≈ 77.8% is a share of the PnL level. A sleeve's share of PnL variance is a separate answer and can differ sharply, because a sleeve with little PnL can still move the total a great deal (our inference).

Risk can be attributed in the same additive way. Tasche describes the Euler principle, which many financial institutions use to allocate capital to business units and sub-portfolios, and how Euler risk contributions are estimated for some important risk measures. For variance, a sleeve's contribution is its covariance with total PnL divided by the variance of total PnL, and these shares sum to 100% by construction. Setting each sleeve's PnL share beside its risk share shows whether concentration sits in the result, in the risk, or both (our reading).

Exercise: from daily PnL per sleeve, tabulate both shares for the lesson's three lines. Then rerun with the signal removed, or the parameters moved to a neighborhood median, and report how much of the net gain survives. Label each sentence of the interpretation as measured or conjectured.""",
        [
            ('paper', 'Brinson, Hood & Beebower', 1986, 'Determinants of Portfolio Performance', 'https://doi.org/10.2469/faj.v42.n4.39',
             'Attributes plan returns to policy, timing and selection; policy explains 93.6% of return variation, yet active management cost the average plan 1.10% a year.'),
            ('paper', 'Ibbotson & Kaplan', 2000, 'Does Asset Allocation Policy Explain 40, 90, or 100 Percent of Performance?', 'https://doi.org/10.2469/faj.v56.n1.2327',
             'Resolves the disagreement over attribution shares by showing that variability over time, variation among funds and return level are three different questions.'),
            ('arxiv', 'Tasche', 2007, 'Capital Allocation to Business Units and Sub-Portfolios: the Euler Principle', 'https://arxiv.org/abs/0708.2542',
             "Describes Euler allocation, widely used to split a portfolio's capital into contributions of its sub-portfolios, and how Euler risk contributions are estimated."),
        ],
    ),
    "10.15": (
        r"""Boutron and co-authors examined what happens to conclusions when the primary result disappoints. From 616 reports of randomized trials published in December 2006, they appraised the 72 with a clearly identified, statistically nonsignificant primary outcome. Spin, meaning reporting that highlights benefit anyway or distracts the reader from the nonsignificant result, appeared in 18.0% of titles and 37.5% of abstract results sections, but in 58.3% of abstract conclusions and 50.0% of main-text conclusions. Our inference: the conclusion is where the pull is strongest, so it is where an executive page needs the guard. The setting is clinical, so this is an analogy. In the lesson's example, whatever criterion the contract predeclared, such as net return against the comparator, should lead the conclusion even if a favorable subperiod or gross metric looks better.

Lipton and Steinhardt, writing about machine learning, list among four patterns they see trending the failure to distinguish explanation from speculation and the misuse of language, such as terms of art with colloquial connotations. In a strategy report, words like significant, robust or alpha should each carry the meaning actually computed (our examples), and every sentence can be marked measured or conjectured.

Stating limits need not cost credibility. In five experiments (total n = 5,780), van der Bles and co-authors found that people perceived greater uncertainty when it was communicated, yet trust in the numbers and the source fell only slightly, and mostly for verbal expressions. By our inference, a numeric range is a safer way to state uncertainty than hedging adjectives, and facts such as twelve months of data and sixty-four tried configurations belong beside it.

Exercise: write the first sentence of your conclusion so that it reports the contract's primary criterion as pass or fail, with sample size, period and cost basis. Then add one numeric statement of uncertainty, one measured limitation, and one test that could disprove the mechanism.""",
        [
            ('paper', 'Boutron, Dutton, Ravaud & Altman', 2010, 'Reporting and Interpretation of Randomized Controlled Trials With Statistically Nonsignificant Results for Primary Outcomes', 'https://doi.org/10.1001/jama.2010.651',
             'In 72 trials with nonsignificant primary outcomes, spin appeared in 18.0% of titles and 37.5% of abstract results but 58.3% of abstract conclusions; a clinical analogy for conclusions.'),
            ('arxiv', 'Lipton & Steinhardt', 2018, 'Troubling Trends in Machine Learning Scholarship', 'https://arxiv.org/abs/1807.03341',
             'Names failing to separate explanation from speculation, and misusing language, as recurring faults in how empirical results are reported.'),
            ('paper', 'van der Bles, van der Linden, Freeman & Spiegelhalter', 2020, 'The effects of communicating uncertainty on public trust in facts and numbers', 'https://doi.org/10.1073/pnas.1913678117',
             'Five experiments found only a small drop in trust when uncertainty was communicated, mostly for verbal rather than numeric expressions.'),
        ],
    ),
    "10.16": (
        r"""Reproducibility is easy to promise and hard to deliver. Stodden and co-authors drew a random sample of 204 computational articles from Science, published after the journal began requiring authors to supply data and code on request. They obtained artifacts for 44% and were able to reproduce the findings for 26%. They called on-request sharing an improvement over no policy but insufficient, and recommended that the journal verify deposit of the artifacts as a condition of publication. By inference, your bundle should be rerun from a clean copy before it ships, not after someone asks.

Wilson and co-authors give the matching practice: provide a simple example or test data set that anyone, yourself included, can run to learn whether the program works and returns a known correct output for a simple known input. Such a smoke test helps when supposedly innocent changes are made or the code moves between machines, and dependencies should be explicit. The lesson's fixture is that test, with known answers: a 10% net return, an 8% benchmark, a 6.6667% drawdown and a 3× median speedup.

A passing fixture has limited reach. GIPS 2020 distinguishes verification, a voluntary firm-wide test of a firm's policies and procedures, from a performance examination, a further optional test of one particular composite. By analogy (our inference), the fixture is assurance about the pipeline, and only reconciling your own run's table to its JSON and its input valuations is assurance about your numbers.

Exercise: copy the bundle to an empty directory, run only the commands in its README, and compare the regenerated metrics.json and input hashes with the shipped ones. Log every failure as a missing item, such as an undeclared dependency, an absolute path or an unrecorded seed.""",
        [
            ('paper', 'Stodden, Seiler & Ma', 2018, 'An empirical analysis of journal policy effectiveness for computational reproducibility', 'https://doi.org/10.1073/pnas.1708290115',
             'Random sample of 204 Science articles: artifacts obtained for 44%, findings reproduced for 26%; on-request sharing judged insufficient.'),
            ('arxiv', 'Wilson et al.', 2016, 'Good Enough Practices in Scientific Computing', 'https://arxiv.org/abs/1609.00037',
             'Practical rules for research projects, including a simple example or test data set with known output and explicit dependencies.'),
            ('official', 'CFA Institute · GIPS Standards', 2020, '2020 GIPS Standards for Firms', 'https://www.gipsstandards.org/wp-content/uploads/2021/03/2020_gips_standards_firms.pdf',
             'Describes verification (firm-wide testing of policies and procedures) and the optional performance examination of a particular composite.'),
        ],
    ),
}
