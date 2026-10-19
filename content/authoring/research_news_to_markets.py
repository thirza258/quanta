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
    "8.6": (
        r"""The lesson's bridge subtracts a change in working capital, so how that change is measured matters. Hribar and Collins contrasted accruals derived from differences between successive balance sheets with accruals read straight from the cash-flow statement. Their main finding was that the balance-sheet route can be contaminated by measurement error, and that tests turn biased when the variable meant to flag earnings management happens to be correlated with mergers and acquisitions or discontinued operations. For Nusa, a rise of 25 computed from two balance sheets could include receivables or inventory acquired in a deal that consumed no operating cash (our inference), so the cash-flow statement's own working-capital lines are the cleaner starting point.

The composition matters as well. Thomas and Zhang traced Sloan's accrual result, in which high accruals precede weaker abnormal returns, mainly to inventory changes. They speculate that demand shifts lie behind it, and their evidence fits earnings management hiding what those shifts imply. Our reading is that an inventory build needs a demand explanation, not only a timing one.

None of this makes one weak quarter proof of manipulation. Beneish's statement-based model identified roughly half of the earnings manipulators before public discovery, yet he cautioned that each flag still has to be sorted into manipulation or another structural root. Zavitsanos and co-authors design their evaluation around the rarity of misstatements, time-ordered data splits and the long delay before misstatements are detected, and show that the way a detector is evaluated materially changes its measured performance. Our inference: a cash-conversion flag is a question for management, not a verdict.

Check: split Nusa's 25 into receivables, inventory and payables from the notes, and compare each line with the cash-flow statement; look for acquisitions or disposals in the period. Then compute conversion as operating cash flow over net income, 25 ÷ 40 = 62.5%, and ask for last year's figure on the same definition.""",
        [
            ('paper', 'Hribar & Collins', 2002, 'Errors in Estimating Accruals: Implications for Empirical Research', 'https://doi.org/10.1111/1475-679X.00041',
             "Shows that accruals computed from balance-sheet changes can be contaminated by mergers, acquisitions and discontinued operations, so the lesson's working-capital change should be checked against the cash-flow statement."),
            ('paper', 'Thomas & Zhang', 2002, 'Inventory Changes and Future Returns', 'https://doi.org/10.1023/A:1020221918065',
             "Finds that inventory changes drive the accrual-return relation, which is why the inventory share of Nusa's working-capital build deserves its own question."),
            ('paper', 'Beneish', 1999, 'The Detection of Earnings Manipulation', 'https://doi.org/10.2469/faj.v55.n5.2296',
             'A statement-based screen that finds about half of manipulators, with the caution that a flag needs a check for a structural explanation.'),
            ('arxiv', 'Zavitsanos et al.', 2023, 'Financial misstatement detection: a realistic evaluation', 'https://arxiv.org/abs/2305.17457',
             'Treats misstatement detection as a rare-event problem whose measured accuracy depends on the evaluation design, a caution for single-quarter flags.'),
        ],
    ),
    "8.7": (
        r"""Cedar's "greater confidence" is the kind of qualitative statement Hutton, Miller and Skinner call soft talk. They separated qualitative soft talk from verifiable forward-looking statements that accompany management earnings forecasts. Managers offered soft talk about equally often with good and bad news forecasts, but were more likely to back good news with verifiable statements. Bad news forecasts were always informative; good news forecasts were informative only when verifiable statements came with them, which the authors read as bolstering credibility. In Cedar's release, the narrowed range is the verifiable part and the adjective is not.

On the call, Matsumoto, Pronk and Roelofsen studied more than 10,000 transcripts. Both the prepared remarks and the discussion added information beyond the press release, but the discussion was the more informative part, and in weak quarters relatively more of the news emerged there. That suggests the Q&A is where to test Cedar's backlog. Liang and Carrasco Kind, in a 2025 preprint, used language models to measure managers' non-responses on S&P 500 calls. Calls with more non-responses showed bigger analyst forecast errors, more disagreement and more uncertainty, and were followed by stronger post-earnings drift, higher volatility and volume, and wider bid-ask spreads. It is a preprint, so treat it as preliminary support for logging every unanswered question.

For the new backlog definition, the SEC's 2020 guidance on key performance indicators expects a metric to come with a clear definition and an explanation of how it is calculated. If the method changes, a company should consider disclosing how it differs from prior periods, why it changed and what it does to previously reported amounts, and whether prior metrics should be recast.

Check: add three columns to Cedar's guidance table, labelled verifiable commitment, soft talk and unanswered question. Then ask whether the filing bridges the old backlog definition to the new one, including the amount of cancellable orders; if it does not, record that as an open item rather than assuming a favourable answer.""",
        [
            ('paper', 'Hutton, Miller & Skinner', 2003, 'The Role of Supplementary Statements with Management Earnings Forecasts', 'https://doi.org/10.1046/j.1475-679x.2003.00126.x',
             "Separates soft talk from verifiable forward-looking statements and shows that only the latter make good news forecasts informative, which tests Cedar's 'greater confidence'."),
            ('paper', 'Matsumoto, Pronk & Roelofsen', 2011, "What Makes Conference Calls Useful? The Information Content of Managers' Presentations and Analysts' Discussion Sessions", 'https://doi.org/10.2308/accr-10034',
             "Finds that the discussion segment of a call is relatively more informative than the presentation, especially when performance is poor, so Cedar's backlog answers matter."),
            ('official', 'U.S. SEC', 2020, "Commission Guidance on Management's Discussion and Analysis of Financial Condition and Results of Operations", 'https://www.sec.gov/files/rules/interp/2020/33-10751.pdf',
             "The SEC's guidance on key performance indicators: what to disclose with a metric and when a changed calculation should be explained or prior figures recast."),
            ('arxiv', 'Liang & Carrasco Kind', 2025, "How do managers' non-responses during earnings calls affect analyst forecasts", 'https://arxiv.org/abs/2505.18419',
             "A 2025 preprint that measures managers' non-responses with language models and links them to analyst forecast errors; it supports logging unanswered questions as open items."),
        ],
    ),
    "8.8": (
        r"""The lesson's formula also covers a buyback, with the cash paid out and the shares retired, and the same price-versus-value logic appears. If Nusa, valued at 500 over 50 shares, repurchased 10 shares, each remaining share would be worth 9.50 if the price paid were 12, 10.00 at 10 and 10.50 at 8 (our arithmetic, assuming the 500 estimate is right). In the issue example the old holders lose 16.67 in total and the new holders gain the same amount, so the price relative to value decides who benefits.

The announcement is not the transaction. Stephens and Weisbach pointed out that an open-market program commits a firm to no particular purchase quantity. Across 450 programs in their 1981 to 1990 sample, the average firm bought 74 to 82 percent of its announced target within three years. Purchases tracked prior stock performance negatively, which suggests firms buy more when they perceive undervaluation, and tracked cash flow positively. In Indonesia, the 2023 OJK rule (POJK 29/2023) requires general-meeting approval first, completion within 12 months of that meeting, a public announcement with reasons if a buyback stops early, and reports on results every six months to the regulator.

Accretion is a weak test. Middleton, Dodd and Baird, in an arXiv preprint, frame the trade-off: fewer shares may raise EPS, but the cash spent lowers net earnings, so the EPS gain depends on the price paid. Almeida, Fos and Kronlund found that EPS-raising buybacks become far more likely for firms that would otherwise have narrowly missed the EPS forecast than for firms that narrowly beat it. Repurchases made for that reason were associated with lower employment and investment and with a fall in cash holdings.

Check: for an announced buyback, compare the shares and rupiah actually bought with the approved ceiling, read the reason if it stopped early, and set the average price paid against your own value per share.""",
        [
            ('paper', 'Stephens & Weisbach', 1998, 'Actual Share Reacquisitions in Open-Market Repurchase Programs', 'https://doi.org/10.1111/0022-1082.115194',
             'Measures how much of an announced open-market buyback is actually carried out, which is the gap between authorization and completed cash distribution.'),
            ('official', 'Otoritas Jasa Keuangan (OJK)', 2023, 'Peraturan OJK Nomor 29 Tahun 2023 tentang Pembelian Kembali Saham yang Dikeluarkan oleh Perusahaan Terbuka', 'https://ojk.go.id/id/regulasi/Documents/Pages/Pembelian-Kembali-Saham-yang-Dikeluarkan-oleh-Perusahaan-Terbuka-/POJK%2029%20Tahun%202023%20Pembelian%20Kembali%20Saham%20Yang%20Dikeluarkan%20Oleh%20Perusahaan%20Terbuka.pdf',
             "Indonesia's buyback rule: approval, a 12-month completion window, disclosure when a buyback stops, and six-monthly reports on results."),
            ('paper', 'Almeida, Fos & Kronlund', 2016, 'The real effects of share repurchases', 'https://doi.org/10.1016/j.jfineco.2015.08.008',
             'Shows that repurchases that lift EPS to meet analyst forecasts are associated with cuts in employment and investment, so accretion alone is not value creation.'),
            ('arxiv', 'Middleton, Dodd & Baird', 2019, 'Quantitative earnings enhancement from share buybacks', 'https://arxiv.org/abs/1911.04199',
             "A preprint on the mechanical EPS effect of a buyback as a function of the price paid, matching the lesson's point about price relative to value."),
        ],
    ),
    "8.9": (
        r"""The ECB treats a base effect as an unusual monthly change in the index a year earlier: when that month leaves the 12-month window, the annual rate shifts even if current prices behave normally. It adds that no single method exists to quantify the effect. In earlier ECB work it was estimated as the typical movement, an estimated seasonal effect plus an average trend, minus the actual monthly change, and cumulative effects are always stated against a reference month. In a 2017 box, measured against July 2017, base effects from energy and unprocessed food were expected to cut headline HICP inflation by half a percentage point by February 2018, then swing to about plus 0.2 points by July 2018.

Apply that to the lesson's index. With the annual rate at 4.87% and this month's gain at 0.5%, suppose the month about to drop out had risen 1.2% (a hypothetical) and next month again rises 0.5%. The annual rate would then fall to about 4.14%, roughly 0.7 points lower, with no price falling.

For Indonesia, Bank Indonesia says BPS-Statistics Indonesia calculates inflation and that CPI inflation is split into core, the persistent component; volatile food, shaped by harvests and disruptions; and administered prices, such as subsidised fuel, electricity and transport fares. Our inference: lumpy administered-price changes can create base effects exactly 12 months later.

One month is also a noisy trend signal. The Cleveland Fed's median CPI takes the one-month rate of the component sitting at the middle of the price-change distribution, and leaving out the extremes can give a cleaner read of underlying inflation than all-items or core CPI. Dowd and Cotter's results suggest that wavelet-based core estimates track trend inflation and predict later inflation better than traditional measures, sometimes by a wide margin.

Check: from two years of monthly index values, mark the changes in the earlier year that exceeded a typical month and note when each leaves the window. Then map each of a company's cost lines to the CPI component it tracks.""",
        [
            ('official', 'European Central Bank', 2017, 'The role of base effects in the projected path of HICP inflation', 'https://www.ecb.europa.eu/pub/pdf/other/ebbox201706_06.en.pdf',
             'Defines a base effect as an atypical month-on-month change 12 months earlier, explains why it has no single measure, and shows how cumulative effects depend on the reference month.'),
            ('official', 'Bank Indonesia', None, 'Introduction to Inflation', 'https://www.bi.go.id/en/fungsi-utama/moneter/inflasi/default.aspx',
             "Bank Indonesia's overview: BPS-Statistics Indonesia calculates inflation, and CPI inflation is split into core, volatile food and administered prices."),
            ('official', 'Federal Reserve Bank of Cleveland', None, 'Median CPI and 16 percent trimmed-mean CPI', 'https://www.clevelandfed.org/indicators-and-data/median-cpi',
             'Explains why measures that omit outlying price changes can give a better signal of the underlying trend than the all-items index.'),
            ('arxiv', 'Dowd & Cotter', 2011, 'U.S. Core Inflation: A Wavelet Analysis', 'https://arxiv.org/abs/1103.5659',
             'Compares wavelet-based core inflation with traditional measures for following trend inflation and predicting future inflation.'),
        ],
    ),
    "8.10": (
        r"""BEA's FAQ gives the official convention behind the lesson's formula: it restates one quarter's growth as the pace a full year would show if that rate persisted, by compounding it over four quarters. Its example turns a 1.0 percent quarterly rise in real GDP into an annualized 4.0 percent, the relationship the lesson inverts to get about 0.985% from 4%. BEA does not annualize everything: it reports corporate profits, a volatile quarterly series, at quarterly rates, and monthly series like personal income at monthly rates, since an annualized single month would overstate month-to-month swings.

Then treat the first print as an estimate. Aruoba examined revisions to major U.S. macroeconomic series and found that their average is not zero, which points to biased initial announcements; that they are large relative to the original variables; and that they can be predicted from information available when the first figure was released. Kuang, in a 2026 preprint using Survey of Professional Forecasters data, reports that revisions between the first release and about 180 days later make up 8.3 percent of the mean squared error against later outcomes for real-activity targets, compared with 3.6 percent for inflation targets, and stresses that an uncertainty interval for a first release is not the same statement as one for a later value. In the lesson's fictional jobs release, the downward revisions of 40 and 30 thousand are this kind of gap (our inference): log them with their sign, and record which vintage you compare against.

The sign of the stock reaction is not fixed either. Boyd, Hu and Jagannathan found that on average a report of higher unemployment lifts stocks during expansions and hurts them during contractions, because such news carries three kinds of information at once: where interest rates are heading, how much risk investors will demand, and what firms will earn and pay out. Rate information dominates in expansions and dividend information in contractions.

Check: take twelve months of payrolls or GDP from a vintage archive such as ALFRED, subtract each first print from its latest value, and look at the mean and the largest gap before treating a headline as settled.""",
        [
            ('official', 'U.S. Bureau of Economic Analysis', None, 'Why does BEA publish percent changes in quarterly series at annual rates?', 'https://www.bea.gov/help/faq/122',
             "BEA's own statement of how annual-rate growth is compounded from a quarterly rate, and why some series are published at quarterly or monthly rates instead."),
            ('paper', 'Aruoba', 2008, 'Data Revisions Are Not Well Behaved', 'https://doi.org/10.1111/j.1538-4616.2008.00115.x',
             'Documents that revisions to major U.S. macroeconomic series are biased, large and predictable, which is why the lesson separates the new observation from revisions.'),
            ('paper', 'Boyd, Hu & Jagannathan', 2005, "The Stock Market's Reaction to Unemployment News: Why Bad News Is Usually Good for Stocks", 'https://doi.org/10.1111/j.1540-6261.2005.00742.x',
             'Shows that the stock reaction to a labour-market headline changes sign with the state of the economy, a warning against reading a jobs number as simply good or bad.'),
            ('arxiv', 'Kuang', 2026, 'Revision Risk in Real-Time Macroeconomic Forecasting', 'https://arxiv.org/abs/2607.05882',
             'A 2026 preprint that splits later-outcome forecast error into preliminary-forecast and revision risk using Survey of Professional Forecasters data.'),
        ],
    ),
    "8.11": (
        r"""The lesson's present-value example changes only r, but stock prices respond to several components at once. Bernanke and Kuttner studied U.S. policy events from June 1989 to December 2002. On average, a hypothetical surprise cut of 25 basis points in the federal funds target went with roughly a 1% rise in broad stock indexes. Their decomposition assigns the largest share of that response to expected excess returns, which we read as the risk-premium part of the discount rate, a channel that a single r hides.

The decision is also only part of the news. Gürkaynak, Sack and Swanson found that surprises in the funds-rate target alone cannot describe the reaction. They needed a second factor for the expected future path of policy, closely tied to FOMC statements, and it moved longer-term Treasury yields far more than the rate action did. Our inference: a statement can move the long yield that discounts the lesson's 110 even when the policy rate is unchanged.

Banks follow their own logic. English, Van den Heuvel and Zakrajšek started from the conventional view that a steeper curve should help banks, yet found that bank shares dropped sharply after unexpected rises in the level of rates or the curve's slope. A large maturity gap softened the reaction to a slope surprise, and banks funded heavily by core deposits fell more, which the authors attribute mainly to deposit disintermediation.

Text can be scored too, with limits. Shah, Paturi and Chava built an annotated dataset of FOMC speeches, minutes and press conferences and a hawkish-dovish stance measure from it. The measure's full-sample correlation with the next year-over-year CPI figure is 0.54 (1996 to 2022), so the score tracks the inflation backdrop and does not isolate a policy surprise (our inference); compare any score with prior expectations before calling it news.

Check: at the next policy announcement you follow, record the surprise against expectations, the move in a one-year and a ten-year yield, and the move in a bank share. Then note which column of your rate map each number informs.""",
        [
            ('paper', 'Bernanke & Kuttner', 2005, "What Explains the Stock Market's Reaction to Federal Reserve Policy?", 'https://doi.org/10.1111/j.1540-6261.2005.00760.x',
             "Sizes the stock reaction to an unanticipated rate move and attributes most of it to expected excess returns, which complicates the lesson's single-r present-value example."),
            ('paper', 'Gürkaynak, Sack & Swanson', 2004, 'Do Actions Speak Louder Than Words? The Response of Asset Prices to Monetary Policy Actions and Statements', 'https://doi.org/10.17016/feds.2004.66',
             'Federal Reserve working-paper version. Separates the rate decision from the guidance in statements, which moves longer-term yields more.'),
            ('paper', 'English, Van den Heuvel & Zakrajšek', 2012, 'Interest Rate Risk and Bank Equity Valuations', 'https://doi.org/10.17016/feds.2012.26',
             'Federal Reserve working-paper version. Shows how bank stock reactions depend on maturity mismatch and deposit funding, the asset and funding repricing the lesson asks for.'),
            ('arxiv', 'Shah, Paturi & Chava', 2023, 'Trillion Dollar Words: A New Financial Dataset, Task & Market Analysis', 'https://arxiv.org/abs/2305.07972',
             'Builds a hawkish-dovish stance measure from FOMC text and tests it against market and inflation data, illustrating both the use and the limits of scoring central-bank language.'),
        ],
    ),
    "8.12": (
        r"""The lesson's no-hedge, no-pass-through case is an upper bound on Nusa's extra cost, and research shows which levers move it. Start with the choice of exchange rate. Gopinath and co-authors propose a dominant currency paradigm, in which one currency dominates how trade is priced and production relies on imported inputs. In data covering 91 percent of world trade, the dollar rate outweighed the bilateral rate in regressions explaining price pass-through and trade elasticities, more strongly where more imports were invoiced in dollars. A 1 percent dollar appreciation against all other currencies also predicted a 0.6 percent decline in trade among countries outside the United States within a year. Our inference: USD/IDR can matter for Nusa even when its supplier is not American, so the invoice currency in each contract is a fact to look up, not assume.

Measured currency exposure is smaller than theory predicts, and Bartram, Brown and Minton trace why. For a typical firm, each of pass-through and operational hedging trims exposure by 10–15%, while foreign-currency debt and, to a lesser extent, derivatives cut it by about 40%. The sign depends on the business: dollar debt offsets an exporter's dollar receipts but adds to an importer's dollar bills (our inference). Changing suppliers is not free either. Camara, using Argentine data on firms' foreign suppliers, found significant adjustment costs in those links and strong complementarity between imported inputs and exports.

Bank Indonesia describes one local rule. Its article on deepening the foreign exchange market says regulation 16/21/PBI/2014, dated 29 December 2014, obliges non-bank corporations to cover at least 25% of net foreign exchange exposure with hedges, as a prudential step in managing external debt. Ask which of Nusa's flows that definition would count.

Check: if Nusa hedged only 25% of its $10 million at 15,000, 75% of the Rp10 billion rise would remain, or Rp7.5 billion. Then confirm on Bank Indonesia's site that the rule is still current.""",
        [
            ('paper', 'Gopinath et al.', 2020, 'Dominant Currency Paradigm', 'https://doi.org/10.1257/aer.20171201',
             'Shows that the dollar exchange rate dominates bilateral rates in price pass-through, so USD/IDR is the rate to test for dollar-invoiced imports.'),
            ('paper', 'Bartram, Brown & Minton', 2010, 'Resolving the exposure puzzle: The many facets of exchange rate exposure', 'https://doi.org/10.1016/j.jfineco.2009.09.002',
             "Quantifies how pass-through, operational hedges, foreign debt and derivatives shrink a firm's measured currency exposure."),
            ('official', 'Bank Indonesia', None, "Bank Indonesia's role in deepening the foreign exchange market as a part of promoting financial stability", 'https://www.bi.go.id/en/iru/economic-policies/Documents/article%20Foreign%20Exchange%20Market%20Deepening-with%20contact.pdf',
             'Central-bank description of the 25% minimum hedge for non-bank corporations with external debt and of FX rules for hedging.'),
            ('arxiv', 'Camara', 2022, "Does an increase in the cost of imported inputs hurt exports? Evidence from firms' network of foreign suppliers", 'https://arxiv.org/abs/2202.12811',
             'Firm-level evidence that imported-input cost shocks hurt exporters because supplier links are costly to adjust.'),
        ],
    ),
    "8.13": (
        r"""Before any margin arithmetic, ask why the benchmark moved. Kilian and Park showed that an oil price shock has no single stock-market effect: the response of U.S. real stock returns varies greatly with whether demand or supply shocks in the oil market lie behind it, and together those shocks account for 22% of the long-run variation in the returns. Bastianin and Manera modelled three structural oil-market shocks, from oil supply, aggregate demand and oil-specific demand, and found that stock market volatility reacts significantly to the two demand shocks, while supply-side shocks have a negligible effect. These are U.S. results about oil, so coal and other inputs need their own check. Our inference for the lesson's producer: the $90 case with unchanged cost resembles a supply-side windfall, while a demand boom may lift costs too, as in the $56 case.

Kilian and Park also found that industry responses are consistent with accounts that stress a reduction in domestic final demand. Our inference: a user such as the lesson's manufacturer may face lower volumes as well as dearer inputs, which is why the lesson asks for a volume stress.

Hedges change how benchmark news reaches earnings. Jin and Jorion studied hedging at 119 U.S. oil and gas producers between 1998 and 2001. Hedging lowered how strongly a producer's stock price responded to oil and gas prices, yet the authors found that it did not seem to affect market value. Suppose half of the lesson's million units are sold at a fixed $80: EBIT at a $90 benchmark is $15 million, not $20 million.

Check: in a filing, find the hedged volume, fixed price and expiry, then recompute EBIT for the hedged and unhedged portions separately.""",
        [
            ('paper', 'Kilian & Park', 2009, 'The Impact of Oil Price Shocks on the U.S. Stock Market', 'https://doi.org/10.1111/j.1468-2354.2009.00568.x',
             'Shows that U.S. stock returns respond differently to oil price shocks driven by demand than by supply, so the cause of a price move matters.'),
            ('paper', 'Jin & Jorion', 2006, 'Firm Value and Hedging: Evidence from U.S. Oil and Gas Producers', 'https://doi.org/10.1111/j.1540-6261.2006.00858.x',
             "Finds that producers' hedges lower the stock price sensitivity to oil and gas prices without a measurable effect on market value."),
            ('arxiv', 'Bastianin & Manera', 2018, 'How does stock market volatility react to oil shocks?', 'https://arxiv.org/abs/1811.03820',
             'Structural model in which volatility responds to aggregate and oil-specific demand shocks but hardly to supply-side shocks.'),
        ],
    ),
    "8.14": (
        r"""A tariff reaches a company in stages, and studies of recent U.S. tariffs measure different stages. Cavallo and co-authors found that tariff pass-through at the border far exceeded exchange-rate pass-through, and that Chinese exporters trimmed their dollar prices only slightly. Prices in stores rose by less, which suggests that retail margins were squeezed and that the burden had so far landed largely on U.S. firms. Alviarez and co-authors, using U.S. customs data on continuing buyer-supplier relationships, estimated that suppliers take on roughly 30 percent of the 2018 tariffs, and their model implies that prices fall as a buyer accounts for more of its supplier's output. Our inference: the same charge may be shared differently by a large buyer and a small one.

Nusa's worksheet starts after the border: the supplier price stays at 60, the tariff adds 6 to unit cost, and a price rise of 3 passes on 3/6 = 50% of it. Treat the 30 percent supplier absorption as a scenario input, not a forecast: unit cost then rises 4.2 instead of 6, and contribution at a price of 103 and volume of 95 is 1,786 rather than 1,615.

Supplier switches have limits. Flaaen, Hortaçsu and Tintelnot found that earlier antidumping duties on South Korean and Chinese washers brought falling or small price changes and moved production to other export platforms. The 2018 tariffs hit nearly all source countries, and washer prices rose nearly 12 percent while dryer prices, which were not tariffed, climbed by an equivalent amount. Our inference: relocation helps mainly when the charge is country-specific, and rivals' price moves belong in the volume assumption.

Check: before choosing any scenario, write the charge's scope in one line, covering the products, the origins and the date it first reaches the income statement.""",
        [
            ('paper', 'Cavallo, Gopinath, Neiman & Tang', 2021, 'Tariff Pass-Through at the Border and at the Store: Evidence from US Trade Policy', 'https://doi.org/10.1257/aeri.20190536',
             'Compares tariff pass-through in import prices at the border with prices in stores and concludes retail margins absorbed part of the charge.'),
            ('paper', 'Flaaen, Hortaçsu & Tintelnot', 2020, 'The Production Relocation and Price Effects of US Trade Policy: The Case of Washing Machines', 'https://doi.org/10.1257/aer.20190611',
             'Washing-machine evidence on relocation after country-specific duties and on price rises, including for untariffed dryers, after broad tariffs.'),
            ('arxiv', 'Alviarez, Fioretti, Kikkawa & Morlacco', 2025, 'Two-Sided Market Power in Firm-to-Firm Trade', 'https://arxiv.org/abs/2507.12848',
             'Estimates that suppliers absorb about 30 percent of the 2018 tariffs within continuing relationships, with bargaining power depending on buyer share.'),
        ],
    ),
    "8.15": (
        r"""Two ideas sharpen the lesson's scenario tree. The first is what the accounts already recognise. IAS 37 draws the line: an entity recognises a provision if an outflow is probable, and otherwise the item is a contingent liability. The IFRS summary gives litigation as an example of the latter when it is uncertain whether the entity committed wrongdoing and settlement is not probable. A provision is also discounted to present value. Our inference: a balance sheet without a provision does not mean zero risk, and a provision already booked should be reconciled with the scenario cost so the same amount is not deducted twice, as in the lesson's remediation warning.

The second is how large the swings can be. Cutler and Summers studied the Texaco-Pennzoil dispute over the Getty Oil takeover and found that it cost the two companies' claimants, taken together, more than $3 billion of wealth. Over the case, the gain to Pennzoil's shareholders was only one-sixth of the loss to Texaco's, and at settlement about two-thirds of the lost wealth came back. The swings exceeded most estimates of direct litigation costs and may reflect disruption of Texaco's operations. That is a single case; our inference is that the operating-restriction branch deserves its own cost line.

Probabilities deserve humility. Katz, Bommarito and Blackman built a model to predict U.S. Supreme Court outcomes using only data available before each decision. Over nearly two centuries it reached 70.2% accuracy at the case level and beat null models, and across the past century it edged out a null model optimized in-sample, by nearly 5%. Our inference: even a documented out-of-sample model with two centuries of data errs in nearly three cases in ten, so the lesson's 50/35/15 weights should be shown as ranges.

Check: move 10 points of weight from the no-restriction branch to closure. Expected cost rises from 12 to 16.8, which you can set against the liquidity available to survive the adverse branch.""",
        [
            ('official', 'IFRS Foundation', None, 'IAS 37 Provisions, Contingent Liabilities and Contingent Assets', 'https://www.ifrs.org/issued-standards/list-of-standards/ias-37-provisions-contingent-liabilities-and-contingent-assets/',
             'Official summary of when a legal exposure becomes a recognised provision, a disclosed contingent liability, and how provisions are measured.'),
            ('paper', 'Cutler & Summers', 1988, 'The Costs of Conflict Resolution and Financial Distress: Evidence from the Texaco-Pennzoil Litigation', 'https://doi.org/10.2307/2555697',
             'Uses market values around a landmark corporate lawsuit to show that the wealth swings exceeded most estimates of direct litigation costs.'),
            ('arxiv', 'Katz, Bommarito & Blackman', 2016, 'A General Approach for Predicting the Behavior of the Supreme Court of the United States', 'https://arxiv.org/abs/1612.03473',
             'Out-of-sample legal-outcome model reaching 70.2% case-level accuracy, a benchmark for how reliable any outcome probability can be.'),
        ],
    ),
    "8.16": (
        r"""A transmission map separates two kinds of link. A business link is a customer, supplier or funding relationship that carries news into cash flows. Cohen and Frazzini identified related firms from each firm's principal customers and showed that stock prices are slow to reflect news about them, so a strategy built on the effect yielded monthly alphas of over 150 basis points. Pinchuk's later replication confirmed customer momentum but found that in the post-discovery sample it was smaller and lost statistical significance, consistent with exploitation by investors. Our inference: a map can show where news should travel, but a once-visible lag may no longer pay, so use the map to explain exposure rather than to manufacture signals.

A market link is different. Anton and Polk linked stocks that share the same active mutual fund owners and found that shared ownership forecasts return correlation after controls for factor exposure, style and sector similarity. They argue from the 2003 mutual fund trading scandal that shared ownership causes the excess comovement. Two stocks can move together with no operating connection, so a correlation alone should not become an arrow on the map.

The lesson's bank adds a measurable link inside one firm. Drechsler, Savov and Schnabl argue that the deposit franchise lets banks keep deposit rates low and slow to follow market rates, and show that banks closely match the rate sensitivities of interest income and expense, which insulates their equity from rate shocks. In the lesson's rate cut, income falls by 10 and expense by 4.5, so net interest income drops from 44 to 38.5. Our inference: that is an unmatched bank, and the question for a real one is where it sits.

Check: label every arrow on your map as business or market, and for each business arrow name the filing line that measures it.""",
        [
            ('paper', 'Cohen & Frazzini', 2008, 'Economic Links and Predictable Returns', 'https://doi.org/10.1111/j.1540-6261.2008.01379.x',
             "Shows that customer-supplier links carry news with a delay, so related firms' returns are predictable; a business link, not a sector label."),
            ('paper', 'Anton & Polk', 2014, 'Connected Stocks', 'https://doi.org/10.1111/jofi.12149',
             'Shows that shared mutual fund owners create return comovement independent of sector and style, a market link without a business link.'),
            ('arxiv', 'Pinchuk', 2023, 'Customer Momentum', 'https://arxiv.org/abs/2301.11394',
             'Replicates the customer-momentum effect and finds it weaker and insignificant after its discovery, a caution on using links as signals.'),
            ('paper', 'Drechsler, Savov & Schnabl', 2021, 'Banking on Deposits: Maturity Transformation without Interest Rate Risk', 'https://doi.org/10.1111/jofi.13013',
             "Shows that banks match the rate sensitivities of interest income and expense through the deposit franchise, the measurable link behind the lesson's bank."),
        ],
    ),
    "8.17": (
        r"""Reverse valuation has a research record, and it comes with warnings. Easton and Monahan examined seven accounting-based proxies for expected returns, each imputed from prices and analysts' earnings forecasts, which solves the lesson's pricing equation for the discount rate instead of for cash flow. For the entire cross-section they found the proxies unreliable: none had a positive association with realized returns, although some looked reliable when consensus long-term growth forecasts were low or analysts' forecast accuracy was high. An implied number inherits the forecasts put into it.

Li and Wang, in a preprint, apply the same arithmetic to the whole market. Dividing total market value by next-year dividends gives a valuation duration. When the tech bubble peaked, just 0.57% of market value came from the following year's dividends, a duration of 175 years; with the global financial crisis at its height, more than 2.2% did, a duration of 46 years. They report that investors know little about cash flow more than a year out, so a higher duration reflects a falling discount rate, not better news on long-run growth. At the lesson's prices, the toy firm's CF1/P moves from 6/70 = 8.57%, about 11.7 years, to 6.3/85 = 7.41%, about 13.5 years.

Which input moved? Vuolteenaho split firm-level returns into cash-flow news and expected-return news and found cash flows dominant, with a variance more than double that of expected-return news for a typical stock. Expected-return news, however, was highly correlated across firms. Our inference: if the stock's rise from 70 to 85 came with its peers, give the discount rate more weight than the cash-flow estimate.

Check: at 85 with CF1 of 6.3, r − g must be 7.41%. Holding g at 2%, r is 9.41%; holding r at 10%, g is 2.59%. State which change you can defend.""",
        [
            ('paper', 'Easton & Monahan', 2005, 'An Evaluation of Accounting-Based Measures of Expected Returns', 'https://doi.org/10.2308/accr.2005.80.2.501',
             'Tests implied-return proxies built from prices and analyst forecasts and finds them unreliable except where growth forecasts are low or analysts accurate.'),
            ('paper', 'Vuolteenaho', 2002, 'What Drives Firm-Level Stock Returns?', 'https://doi.org/10.1111/1540-6261.00421',
             'Splits firm-level returns into cash-flow news and discount-rate news, the two things a price reversal cannot tell apart.'),
            ('arxiv', 'Li & Wang', 2023, 'Valuation Duration of the Stock Market', 'https://arxiv.org/abs/2310.07110',
             "Preprint measuring market value divided by next-year dividends, the lesson's 1/(r - g) multiple, and linking its swings to discount rates."),
        ],
    ),
    "8.18": (
        r"""Cedar's zero CAR hides a benchmark choice. A market-adjusted return assumes a beta of 1, while a market-model residual is Cedar's return minus α minus β times the market return. Cedar's three returns sum to zero and so do the market's, so the three-day sum equals −3α whatever β is. Only the daily path shows the choice. With β = 1.5 the abnormal returns are 0.25%, −1.5% and 1.25%; with β = 0.5 they are 0.75%, −2.5% and 1.75%. The middle day stays negative, but how much of its −3% belongs to Cedar depends on a beta that must come from pre-event data.

Goldsmith-Pinkham and Lyu, in a 2025 preprint, show why such choices matter. Standard event studies assume a linear factor model whose factors are known; if that model is wrong, which the authors treat as nearly certain, the estimated effects are inconsistent. The distortion grows in turbulent markets, in long-horizon windows, and when the date of the news is tied to market conditions. For short windows with randomly timed events they say the conventional approach holds up, and as an alternative they propose synthetic controls assembled from comparison securities. Firms often pick their own release times, so a short window helps without settling the question (our inference).

Dependence is a second trap. Kolari and Pynnönen show that when events share a date, even modest correlation among firms' abnormal returns leads standard tests to reject a zero average effect too often. If one tariff headline moves five suppliers on the same day, treat it as one cluster, not five independent observations.

Check: re-run Cedar with β = 0.5, 1 and 1.5, and state which conclusion survives all three.""",
        [
            ('paper', 'Kolari & Pynnönen', 2010, 'Event Study Testing with Cross-sectional Correlation of Abnormal Returns', 'https://doi.org/10.1093/rfs/hhq072',
             'Shows that event-date clustering with even low cross-correlation makes standard tests over-reject, so same-day sector headlines are not independent observations.'),
            ('arxiv', 'Goldsmith-Pinkham & Lyu', 2025, 'Causal Inference in Financial Event Studies', 'https://arxiv.org/abs/2511.15123',
             'Explains how a misspecified factor model biases abnormal returns, most in volatile periods and long horizons, and why short windows are safer.'),
        ],
    ),
    "8.19": (
        r"""The lesson's quote moves from 100.00/100.10 to 98.00/102.00 while the midpoint stays put, so the quote carries a liquidity message, not a valuation one. Lee and co-authors studied NYSE firms and found that wide spreads go with thin depth, and that ahead of earnings releases spreads widen and depth shrinks, more so when the eventual price change is large. They read this as liquidity providers managing information-asymmetry risk with both spreads and depths. A quote of 98.00/102.00 may therefore be dealers protecting themselves, and the quoted size matters as much as the quoted price.

Forced trading is a second mechanism. Coval and Stafford examined fund trades driven by capital flows between 1980 and 2003. Funds hit by large outflows tended to shrink their holdings, which put price pressure on the stocks these funds held in common, and investors who traded against such constrained funds earned highly significant returns for supplying liquidity. Our inference: a drop that reverses without new facts fits price pressure better than a lasting change in value, though one case cannot prove which.

News may also explain less than expected. Joulin and co-authors cross-correlated high-frequency stock returns with several news feeds. Neither company-specific nor market-wide news accounted for how often prices jump or how large the jumps are, and the authors suspect that most jumps come from swings in order flow when liquidity nearly vanishes.

Check: the post-news half-spread of 2.00 is 2% of the 100 midpoint, against 0.05% before it. For the next jump you study, record the quoted size at the bid and the offer, then see whether the price level held a week later.""",
        [
            ('paper', 'Lee, Mucklow & Ready', 1993, 'Spreads, Depths, and the Impact of Earnings Information: An Intraday Analysis', 'https://doi.org/10.1093/rfs/6.2.345',
             "Shows that spreads widen and depths fall around earnings news, so a wide quote signals dealers' information risk as well as a trading cost."),
            ('paper', 'Coval & Stafford', 2007, 'Asset fire sales (and purchases) in equity markets', 'https://doi.org/10.1016/j.jfineco.2006.09.007',
             'Documents price pressure from fund outflows and the returns earned by liquidity providers, a flow mechanism separate from a business change.'),
            ('arxiv', 'Joulin et al.', 2008, 'Stock price jumps: news and volume play a minor role', 'https://arxiv.org/abs/0803.1769',
             'Cross-correlates high-frequency returns with news feeds and finds that news does not explain the frequency or size of price jumps.'),
        ],
    ),
    "8.20": (
        r"""The lesson's 42.86% posterior counts the verified operational report once. Enke and Zimmermann show why that discipline matters. In their experiments many people neglected the correlation between signals and treated correlated information as independent, so beliefs reacted too strongly to widely connected sources, a pattern the authors call overshooting. In an experimental asset market, the confidence swings this caused produced predictable bubbles and crashes. Apply the same slip to the lesson. Prior odds are 0.25 and the likelihood ratio is 3 (60% over 20%). Counting the report and one newspaper reprint as two signals gives odds of 0.25 × 3 × 3 = 2.25, a posterior of about 69.2%; two reprints would give about 87.1%, and no new fact has arrived.

A vivid report can mislead even when it is counted once. Griffin and Tversky separate the strength of evidence, meaning how extreme it looks, from its weight, meaning the credibility of the source or how large the sample is. People, they argue, attend mostly to strength, which breeds overconfidence when evidence is striking but thin. Augenblick and co-authors add that the error depends on signal size: in experiments, sports betting and financial markets alike, people drew too much from weak signals and too little from strong ones. Our inference: expect your gut to overshoot the Bayes arithmetic on a minor datum and to undershoot on a decisive one.

Check: give each report two ratings, how extreme it is and how much weight its source can bear, then recompute the posterior with every shared-origin report counted once.""",
        [
            ('paper', 'Enke & Zimmermann', 2017, 'Correlation Neglect in Belief Formation', 'https://doi.org/10.1093/restud/rdx081',
             'Experiments showing that people treat correlated signals as independent, which inflates beliefs and, in an asset market, produces bubbles and crashes.'),
            ('paper', 'Griffin & Tversky', 1992, 'The weighing of evidence and the determinants of confidence', 'https://doi.org/10.1016/0010-0285%2892%2990013-R',
             'Separates the strength of evidence from its weight and explains when confidence runs ahead of what the source can support.'),
            ('arxiv', 'Augenblick, Lazarus & Thaler', 2021, 'Overinference from Weak Signals and Underinference from Strong Signals', 'https://arxiv.org/abs/2109.09871',
             'Finds in experiments, betting markets and financial markets that people overreact to weak signals and underreact to strong ones.'),
        ],
    ),
    "8.21": (
        r"""The lesson's evidence coverage of 4/6 is a recall-type measure. Liu and co-authors, auditing four generative search engines, paired two such measures: citation recall, meaning statements fully backed by their citations, and citation precision, meaning citations that genuinely support the statement they are attached to. On average only 51.5% of generated sentences were fully supported and only 74.5% of citations supported their sentence. Our inference: a memo needs both ratios, because a link beside a claim does not prove the page backs it.

The CIA-hosted Tradecraft Primer of 2009 supplies a ledger and a method. Its quality-of-information check suggests a database that sorts information by source type and date, with notes on each source's strengths and weaknesses, and it cautions that several sources do not replace information that has been properly vetted. That describes the packet's derivative commentary article: another link, not another fact. For the alternative-explanations section, the primer describes analysis of competing hypotheses: list hypotheses as columns and evidence as rows, mark each item consistent, inconsistent or not applicable, and treat evidence that fits every hypothesis as unimportant for choosing among them.

Do not oversell the method. Dhami and co-authors randomly assigned fifty intelligence analysts to use it or not. The trained analysts skipped some of its steps, the evidence that it curbs confirmation bias was mixed, and it may even raise inconsistency and error in judgement. Our inference: use the matrix as a transparency device, not as proof.

Check: mark each of the six claims as having a verified source location or not, mark each citation as supporting its claim or not, and report both ratios.""",
        [
            ('arxiv', 'Liu, Zhang & Liang', 2023, 'Evaluating Verifiability in Generative Search Engines', 'https://arxiv.org/abs/2304.09848',
             'Defines citation recall and precision and measures how often AI-generated answers are actually supported by their cited sources.'),
            ('official', 'U.S. Government · CIA Center for the Study of Intelligence', 2009, 'A Tradecraft Primer: Structured Analytic Techniques for Improving Intelligence Analysis', 'https://www.cia.gov/resources/csi/static/Tradecraft-Primer-apr09.pdf',
             "Describes a source-quality check and the analysis of competing hypotheses matrix, which map onto the memo's source ledger and alternative explanations."),
            ('paper', 'Dhami, Belton & Mandel', 2019, 'The “analysis of competing hypotheses” in intelligence analysis', 'https://doi.org/10.1002/acp.3550',
             'A randomized test with intelligence analysts that found mixed evidence for the technique, a caution against treating a matrix as proof.'),
        ],
    ),
    "8.22": (
        r"""The lesson's 60% precision and 66.67% recall measure agreement with a declared label, so the labeling rule deserves scrutiny too. Loughran and McDonald found that, across a large set of 10-Ks from 1994 to 2008, nearly three quarters of the words that the Harvard Dictionary tags as negative do not usually carry a negative meaning in financial writing. They built finance-specific word lists and linked them to returns around filings, trading volume, volatility, fraud, material weaknesses and earnings surprises. Record which lexicon or model version produced each label.

Extraction needs its own audit. Islam and co-authors tested 16 model configurations on a sample of 150 cases and manually reviewed 2,400 answers. GPT-4-Turbo paired with a retrieval system gave a wrong answer or declined to answer for 81% of questions, and every model showed weaknesses such as hallucinations. Those were 2023-era systems, so treat 81% as a snapshot, not a current error rate (our inference); the lesson is the verification gate.

Dates need care with language models. Lopez-Lira and co-authors argue that a model's forecasts about periods inside its training data deserve no trust: once it has seen the outcome, good output could be skill or memory, and the two cannot be separated. Telling the model to respect historical boundaries did not prevent accurate recall, and masking did not help because models rebuild entities and dates from small clues. For events after the cutoff they found no recall. Our inference: a held-out date interval must start after the model's training cutoff, not merely after your own training sample.

Check: run the classifier only on events dated after the tool's stated cutoff, and count wrong, refused and unsupported extractions separately.""",
        [
            ('paper', 'Loughran & McDonald', 2011, 'When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks', 'https://doi.org/10.1111/j.1540-6261.2010.01625.x',
             'Shows that a general-purpose negative-word list misclassifies financial text, so a sentiment label depends on the dictionary behind it.'),
            ('arxiv', 'Islam et al.', 2023, 'FinanceBench: A New Benchmark for Financial Question Answering', 'https://arxiv.org/abs/2311.11944',
             'Manually reviews thousands of model answers about public companies and reports high rates of wrong or refused answers and hallucinations.'),
            ('arxiv', 'Lopez-Lira, Tang & Zhu', 2025, "The Memorization Problem: Can We Trust LLMs' Economic Forecasts?", 'https://arxiv.org/abs/2504.14765',
             'Shows that language models recall data from their training period, which undermines tests run on dates the model has already seen.'),
        ],
    ),
    "8.23": (
        r"""Hindsight bias is why the lesson fixes the log before the outcome. Biais and Weber model agents who, once they have seen information, forget how little they knew beforehand. In an experiment with 66 students, hindsight bias reduced volatility estimates, and in another with 85 investment bankers working in London and Frankfurt, the more biased agents had lower performance. Roese and Vohs add that prompting people to weigh other causal stories for an outcome can weaken the bias. Our inference: the lesson's log categories (evidence wrong, mechanism incomplete, timing differed, within the downside) work partly because they force alternatives.

Scoring has its own hindsight trap. Murphy partitioned the Brier score into the uncertainty built into the events, the reliability of the forecasts and their resolution, and defined the uncertainty term as the score of the sample's relative frequencies. For the lesson's outcomes 1, 0 and 1 that frequency is 2/3, and a constant forecast of 2/3 scores 0.2222, better than the analyst's 0.2967 and better than the 0.25 of a constant 0.5. That baseline uses the outcomes, so nobody could have declared it in advance; write the baseline, such as a base rate from earlier events, into the memo.

Three cases cannot show calibration either. Dimitriadis and co-authors note that the usual way of binning forecasts for reliability diagrams gives unstable pictures because it hangs on arbitrary implementation choices, and their CORP method lets you attach uncertainty estimates. Pool resolved events before reading any calibration plot.

Check: at memo creation write the baseline, review date and resolution rule, then score every resolved event, including no-action cases, against that baseline.""",
        [
            ('paper', 'Biais & Weber', 2009, 'Hindsight Bias, Risk Perception, and Investment Performance', 'https://doi.org/10.1287/mnsc.1090.1000',
             'Experiments with students and investment bankers linking hindsight bias to lower volatility estimates and lower performance.'),
            ('paper', 'Roese & Vohs', 2012, 'Hindsight Bias', 'https://doi.org/10.1177/1745691612454303',
             'Review of what hindsight bias is, where it comes from and why considering alternative causal explanations can reduce it.'),
            ('paper', 'Murphy', 1973, 'A New Vector Partition of the Probability Score', 'https://doi.org/10.1175/1520-0450%281973%29012%3C0595%3AANVPOT%3E2.0.CO%3B2',
             "Splits the Brier score into uncertainty, reliability and resolution, with uncertainty defined by the sample's own relative frequencies."),
            ('arxiv', 'Dimitriadis, Gneiting & Jordan', 2020, 'Evaluating probabilistic classifiers: Reliability diagrams and score decompositions revisited', 'https://arxiv.org/abs/2008.03033',
             'Shows why binned reliability diagrams are unstable and offers a method that attaches uncertainty to calibration checks.'),
        ],
    ),
    "8.24": (
        r"""Banyu's one forecast year capitalized forever is a crude model, so ask how well even careful discounted cash flow does. Kaplan and Ruback compared the discounted value of cash flow forecasts with the market values of 51 highly leveraged transactions from 1983 to 1989. The valuations landed within 10 percent on average and did no worse than approaches built on comparable companies and deals. Our inference: the sample is narrow, and an average can hide larger single-case misses.

Horizon matters too. Penman and Sougiannis note that standard formulas need payoffs forecast to infinity, while practical analysis uses a finite horizon and needs troublesome terminal-value calculations. They valued firms from average realized payoffs across several horizons, with or without a terminal value, and compared the results with market prices. Errors were lower for accrual-earnings techniques than for cash-flow and dividend discounting. Banyu's whole value capitalizes one year, including its capex and working-capital investment.

Inputs swing the answer. With FCFF₁ held at 112.5, an 11% discount rate gives 9.50 per share and 3% growth gives about 13.07, against 11.0625 in the base case and a price of 12 (the growth case is crude, since faster growth usually needs more reinvestment). Either change exceeds the 0.9375 gap between value and price, and net debt magnifies it. Yee notes that DCF, comparables and fundamental analysis usually produce conflicting estimates that also tend to differ from the market price, and his Bayesian framework supports averaging them. Our inference: report the base case, the downside case and the market price as a range.

Check: re-run the base case at 9%, 10% and 11% and write the three per-share values beside the price of 12.""",
        [
            ('paper', 'Kaplan & Ruback', 1995, 'The Valuation of Cash Flow Forecasts: An Empirical Analysis', 'https://doi.org/10.1111/j.1540-6261.1995.tb04050.x',
             'Tests discounted cash flow against transaction values in 51 deals and finds it within 10 percent on average, a benchmark for how far a model can be trusted.'),
            ('paper', 'Penman & Sougiannis', 1998, 'A Comparison of Dividend, Cash Flow, and Earnings Approaches to Equity Valuation', 'https://doi.org/10.1111/j.1911-3846.1998.tb00564.x',
             'Compares valuation techniques over finite horizons and finds lower errors for accrual earnings than for cash-flow discounting.'),
            ('arxiv', 'Yee', 2007, 'A Bayesian Framework for Combining Valuation Estimates', 'https://arxiv.org/abs/0707.3482',
             'Argues that discounted cash flow, comparables and market price disagree and justifies combining them instead of trusting one.'),
        ],
    ),
}
