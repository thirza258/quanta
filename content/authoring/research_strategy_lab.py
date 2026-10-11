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
        r"""The lesson's twelve configurations are a trial count, and trial counts have measurable consequences. Bailey, Borwein, López de Prado and Zhu showed that it takes a relatively small number of trials to find a strategy with spuriously high backtested performance. With five years of data they say no more than 45 independent configurations should be tried. On a two-year backtest, seven are enough for the expected best in-sample Sharpe ratio to be 1 while the expected out-of-sample ratio is 0. Their calculation assumes independent trials, and for overlapping variants they suggest a dimension-reduction method such as principal component analysis. My reading is that the two fee settings of one rule will behave almost alike, so the independent count is below twelve, but the full count still belongs in the report.

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
}
