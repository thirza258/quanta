"""Research extensions for Financial news to company & stock analysis.

Each entry maps a lesson ID to (body, sources). A source is
(kind, authors, year, title, url, what it contributes); see research_depth.py.
Every figure was checked against a verbatim snippet from its source before merging.
"""

NOTES = {
    "8.1": (
        r"""The lesson's $90 million is a ceiling, and contract design shows why a ceiling and committed revenue can differ. Take a U.S. federal indefinite-quantity contract as a model. The Federal Acquisition Regulation says such a contract must require the government to order at least a stated minimum, and the contractor must furnish any further quantities that are ordered only up to a stated maximum. The minimum must be more than nominal but should not exceed what the government is fairly certain to order, so the guaranteed amount can sit far below the headline maximum. Other contract types work differently, which is why the filing's own terms matter more than a press-release summary.

Order backlog is a related disclosure. Rajgopal, Shevlin and Venkatachalam studied backlog as a leading indicator and found that the stock market overweights its contribution to predicting future earnings. A strategy that exploited the overweighting earned significant abnormal returns, and the authors say the mispricing was not due to analysts being unable to use backlog in their forecasts. Backlog is an input with an uncertain conversion into profit, not sales already earned.

The headline itself is a presentation choice. Huang, Nekrasov and Teoh counted the quantitative items in earnings press-release headlines. More items were associated with stronger announcement reactions and later reversals, and managers were more likely to choose them before selling shares after the announcement. That evidence concerns earnings releases, not contract announcements, so read it as a reason to test a big number, not as a rule (an inference, not a finding).

Verification is also hard to automate. Zhao and co-authors built FinDVer, 2,400 expert-annotated examples for checking claims against long financial documents, and reported that even the best system they tested, GPT-4o, lagged human experts.

Check: find the minimum, maximum and term in a real contract announcement. For Cedar, suppose the minimum were $9 million (hypothetical). The annual floor would be $3 million, or 0.5% of $600 million, against the 5% ceiling. Report the range, not one number.""",
        [
            ('official', 'Federal Acquisition Regulation · eCFR', None, 'Indefinite-quantity contracts (48 CFR 16.504)', 'https://www.ecfr.gov/current/title-48/chapter-1/subchapter-C/part-16/subpart-16.5/section-16.504',
             'The U.S. federal rule defining a stated minimum and maximum in indefinite-quantity contracts; it separates the guaranteed amount from the ceiling.'),
            ('paper', 'Rajgopal, Shevlin & Venkatachalam', 2003, 'Does the Stock Market Fully Appreciate the Implications of Leading Indicators for Future Earnings? Evidence from Order Backlog', 'https://doi.org/10.1023/A:1027364031775',
             'Tests whether order backlog predicts earnings and whether prices reflect it correctly; the market overweights backlog.'),
            ('paper', 'Huang, Nekrasov & Teoh', 2018, 'Headline Salience, Managerial Opportunism, and Over- and Underreactions to Earnings', 'https://doi.org/10.2308/accr-52010',
             "Shows how the number of quantitative items in an earnings headline relates to market reactions and to managers' share sales."),
            ('arxiv', 'Zhao et al.', 2024, 'FinDVer: Explainable Claim Verification over Long and Hybrid-Content Financial Documents', 'https://arxiv.org/abs/2411.05764',
             'A claim-verification benchmark on long financial documents in which the best model tested still trails human experts.'),
        ],
    ),
    "8.2": (
        r"""The lesson counts four blog posts as one claim. Research shows why that discipline matters, because repeated or old information can still move prices. Huberman and Regev studied EntreMed after a Sunday New York Times article on potential cancer-curing drugs. The stock closed at 12.063 on Friday, opened at 85 on Monday, closed near 52, and stayed above 30 for the following three weeks. The same breakthrough had been reported in Nature and in popular newspapers more than five months earlier, and the authors conclude that no genuinely new information had been presented.

Tetlock made staleness measurable: a story's textual similarity to the previous ten stories about the same firm. Returns responded less to stale news, but the return on a stale-news day negatively predicted the following week's return, and individual investors traded more aggressively when news was stale. So log repetition rather than assume the market ignores it.

Corrections have a long tail too. In September 2008 a six-year-old article about United Airlines' 2002 bankruptcy resurfaced and was mistaken for a new filing. Carvalho, Klagge and Moench report that the stock fell by as much as 76% within minutes before NASDAQ halted trading, and still ended the day 11.2% below the previous close even after the news was identified as false. After three trading sessions it remained below their model's two-standard-deviation band, and it was back at the predicted level on the seventh day. Our inference: an 'available by' flag says what was knowable at a time, not that prices or other readers had already absorbed it.

The same rule applies to AI helpers. Glasserman and Lin warn that a language model trained on many years of text biases a backtest when the training and backtesting periods overlap. Inside the training window, anonymized headlines outperformed the originals, which they read as a distraction effect, and out of sample look-ahead bias was not a concern.

Check: in Cedar's timeline, mark each item eligible or not at 10:00 and at 12:30. Write 'one claim' beside the 09:00 rumor and the four 09:15 reposts unless a repost adds a fact the original lacked.""",
        [
            ('paper', 'Huberman & Regev', 2001, 'Contagious Speculation and a Cure for Cancer: A Nonevent That Made Stock Prices Soar', 'https://doi.org/10.1111/0022-1082.00330',
             'A case in which re-reported, already public news produced a lasting price jump in EntreMed.'),
            ('paper', 'Tetlock', 2011, "All the News That's Fit to Reprint: Do Investors React to Stale Information?", 'https://doi.org/10.1093/rfs/hhq141',
             'Defines news staleness by textual similarity to earlier stories and tests how prices and investor types respond.'),
            ('paper', 'Carvalho, Klagge & Moench', 2011, 'The persistent effects of a false news shock', 'https://doi.org/10.1016/j.jempfin.2011.03.003',
             'Event study of the 2008 United Airlines false-bankruptcy episode and the days it took the price to recover.'),
            ('arxiv', 'Glasserman & Lin', 2023, 'Assessing Look-Ahead Bias in Stock Return Predictions Generated By GPT Sentiment Analysis', 'https://arxiv.org/abs/2309.17322',
             'Shows how overlapping model-training and backtest periods can contaminate headline-sentiment strategies.'),
        ],
    ),
    "8.3": (
        r"""The lesson calls its size screen a triage tool, and official guidance agrees. In Staff Accounting Bulletin No. 99 the SEC staff accepted a percentage threshold such as 5% as a basis for a preliminary assumption that a smaller deviation is unlikely to be material. It added that expressing a misstatement as a percentage is only the start of the analysis and cannot replace weighing every relevant consideration. Its qualitative factors include whether an item masks a change in earnings or other trends, hides a miss against analysts' consensus, turns a loss into income, or affects loan covenants or regulatory compliance. The bulletin is aimed at preparers and auditors, so using those factors as an analyst's checklist for looking past a ratio is our inference.

Size can also understate consequences. Karpoff, Lee and Martin examined 585 firms targeted by SEC enforcement for financial misrepresentation from 1978 to 2002. Legal penalties averaged $23.5 million per firm, but their estimated reputational penalty was over 7.5 times all legal and regulatory penalties combined. For each dollar of inflated market value, firms lost that dollar plus $3.08, of which $0.36 was expected legal penalty and $2.71 lost reputation. These are misconduct cases, so they illustrate the principle rather than set a rate.

Units are a practical hazard. The builders of the TAT-QA dataset note that magnitudes such as thousand, million and billion are often omitted or shown only in headers or nearby paragraphs, and they call this a number's scale. Their proposed model reached 58.0% F1 against 90.8% for human experts, so an automated extraction still needs your units box.

Check: Nusa's Rp15 billion is 0.75% of sales and 15% of EBIT. Pick one factor from the bulletin's list that would make it matter more. For example, if a covenant required EBIT of at least Rp90 billion (hypothetical), headroom would fall from Rp10 billion to negative Rp5 billion.""",
        [
            ('official', 'U.S. SEC · Federal Register', 1999, 'Staff Accounting Bulletin No. 99', 'https://www.govinfo.gov/content/pkg/FR-1999-08-19/html/99-21484.htm',
             "The SEC staff's guidance that a percentage rule of thumb is only a starting point for materiality, with a list of qualitative factors."),
            ('paper', 'Karpoff, Lee & Martin', 2008, 'The Cost to Firms of Cooking the Books', 'https://doi.org/10.1017/S0022109000004221',
             'Compares legal penalties with the much larger reputational loss for 585 firms that faced SEC misrepresentation actions.'),
            ('arxiv', 'Zhu et al.', 2021, 'TAT-QA: A Question Answering Benchmark on a Hybrid of Tabular and Textual Content in Finance', 'https://arxiv.org/abs/2105.07624',
             "A financial-report question-answering dataset that treats a number's unit scale as something a model must infer from headers."),
        ],
    ),
    "8.4": (
        r"""The lesson's Cedar example, a 20% EPS gain that still misses the estimate, fits a pattern that Skinner and Sloan documented. Growth stocks, they found, are at least as likely to report negative earnings surprises as positive ones, but they react with an asymmetrically large price drop to the negative ones. After controlling for that asymmetric response, they found no remaining return gap between growth and value stocks, and they read the gap as optimistic expectations corrected by later disappointments. Whether Cedar fits depends on what its pre-release price assumed, which the 6% fall alone cannot tell you.

The word 'expected' also hides a choice. Livnat and Mendenhall measured surprises two ways: from analysts' forecasts and from a time-series model built on Compustat earnings. The post-announcement drift was significantly larger with the analyst-based surprise, and they suggest the two measures may capture somewhat different forms of mispricing. A dated consensus and a naive 'last year plus trend' benchmark are therefore different tests, not interchangeable ones.

Is the news fully priced at the announcement? Studies disagree by period and firm size. Martineau argues that stock prices now fully reflect earnings surprises on the announcement date: drift has been non-existent for large stocks since 2006 and has disappeared only recently for microcaps. Christensen, Timmermann and Veliyev, in a recent preprint, find that earnings announcements almost always trigger price jumps and that a post-announcement trading strategy is consistent with efficient price formation after 2016. Our inference: for a large listed company, a continued slide after a miss is more likely new information or noise than a slow reaction, while a microcap or an older sample deserves a different prior.

Check: scale Cedar's 10-cent miss two ways. Against $1.30 expected EPS it is 7.69%; against a hypothetical $26 share price it is 0.38%. Write down which scaling you chose, because it changes how large the surprise looks.""",
        [
            ('paper', 'Skinner & Sloan', 2002, "Earnings Surprises, Growth Expectations, and Stock Returns or Don't Let an Earnings Torpedo Sink Your Portfolio", 'https://doi.org/10.1023/A:1020294523516',
             'Shows that growth stocks react asymmetrically to negative surprises, which explains why a miss can hurt when expectations are high.'),
            ('paper', 'Livnat & Mendenhall', 2006, 'Comparing the Post-Earnings Announcement Drift for Surprises Calculated from Analyst and Time Series Forecasts', 'https://doi.org/10.1111/j.1475-679X.2006.00196.x',
             'Compares surprises built from analyst forecasts with those from time-series models and finds different drift.'),
            ('paper', 'Martineau', 2022, 'Rest in Peace Post-Earnings Announcement Drift', 'https://doi.org/10.1561/104.00000122',
             'Argues that prices now reflect earnings surprises on the announcement date, so drift has vanished for large stocks.'),
            ('arxiv', 'Christensen, Timmermann & Veliyev', 2026, 'Warp speed price moves: Jumps after earnings announcements', 'https://arxiv.org/abs/2601.08962',
             'High-frequency evidence that announcements trigger price jumps and that later returns look consistent with efficient pricing.'),
        ],
    ),
    "8.5": (
        r"""Where you stop on the income statement matters. Novy-Marx argued that gross profit is the cleanest accounting measure of true economic profitability, because measures grow more polluted the farther down the income statement you go. He found that gross profits-to-assets has roughly the same power as book-to-market in predicting the cross-section of average returns. Cedar's gross profit fell from 80 to 77 while revenue rose 10%, so the headline growth hides the line he emphasizes. His result concerns portfolios of many firms, not one quarter, so it tells you where to look rather than what Cedar's stock will do.

The next question is which earnings number the release leads with. Bradshaw and Sloan found that over the past 20 years the frequency and magnitude of gaps between GAAP and 'Street' earnings rose dramatically, with a very strong bias toward a Street figure above the GAAP figure. They also found that the market response to the Street number had displaced GAAP earnings as a primary determinant of prices, and that management actively defines and emphasizes the Street number in earnings releases.

Exclusions are not necessarily harmless. Doyle, Lundholm and Soliman found that higher levels of expenses excluded from pro forma earnings led to predictably lower future cash flows, that investors did not fully appreciate this at the announcement, and that a strategy based on the exclusions earned large positive abnormal returns in later years. For measures in SEC filings, Item 10(e) of Regulation S-K requires the GAAP measure with equal or greater prominence plus a quantitative reconciliation. It also bars adjusting a performance measure to eliminate an item labelled non-recurring, infrequent or unusual when a similar charge is reasonably likely to recur within two years or occurred within the prior two years.

Check: for Cedar, write the gross-margin change in percentage points, the gross-profit change and the EBIT change. Then, for each item the release excludes, search the previous two years of releases for a similar charge or gain. A repeat is a reason to treat it as part of ongoing operations in your own bridge.""",
        [
            ('paper', 'Novy-Marx', 2013, 'The other side of value: The gross profitability premium', 'https://doi.org/10.1016/j.jfineco.2013.01.003',
             'Argues that gross profit is the cleanest profitability measure and that it predicts returns about as strongly as book-to-market.'),
            ('paper', 'Bradshaw & Sloan', 2002, 'GAAP versus The Street: An Empirical Assessment of Two Alternative Definitions of Earnings', 'https://doi.org/10.1111/1475-679X.00038',
             "Documents the widening gap between GAAP and Street earnings and the market's greater reliance on the Street figure."),
            ('paper', 'Doyle, Lundholm & Soliman', 2003, 'The Predictive Value of Expenses Excluded from Pro Forma Earnings', 'https://doi.org/10.1023/A:1024472210359',
             'Shows that expenses excluded from pro forma earnings predict lower future cash flows that investors underweight.'),
            ('official', 'Regulation S-K · eCFR', None, 'Item 10 (17 CFR 229.10): Use of non-GAAP financial measures in Commission filings', 'https://www.ecfr.gov/current/title-17/chapter-II/part-229/subpart-229.1/section-229.10',
             'The SEC rule requiring a GAAP comparison and reconciliation, and barring certain non-recurring labels on items likely to recur.'),
        ],
    ),
}
