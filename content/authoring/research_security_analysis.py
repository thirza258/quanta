"""Research extensions for Security Analysis.

Each entry maps a lesson ID to (body, sources). A source is
(kind, authors, year, title, url, what it contributes); see research_depth.py.
Every figure was checked against a verbatim snippet from its source before merging.
"""

NOTES = {
    "1.1": (
        r"""Researchers measure what the lesson calls the margin, but mechanically. Because M = 1 − P/V, the value-to-price ratio is V/P = 1/(1 − M): Alder's weak, base and favorable cases give 1.25, 1.67 and 2.08. In the studies below, V is a book-value or earnings figure, not a reasoned range.

Lakonishok, Shleifer and Vishny sorted NYSE and AMEX stocks from April 1963 to April 1990. Averaged over the post-formation years, size-adjusted returns of high book-to-market (value) stocks beat low book-to-market (glamour) stocks by 7.8 percent per year. They argued that value strategies exploit the extrapolation mistakes reflected in prices, not extra risk. Fama and French found that size and book-to-market equity capture the variation in average returns associated with leverage and earnings-price ratios, while the relation between market β and average return was flat once β could vary independently of size. Why cheap stocks earn more is the disputed part.

Two cautions. These are portfolio averages; they do not show that any single 40% discount pays. And Chen, Lopez-Lira and Zimmermann found that for published predictors and for data-mined accounting ratios alike, about half of the predictability remains after the original sample periods. Our inference: a historical value premium is a hypothesis about the future, not a margin of safety.

Check: at $60, a 30% discount needs V of at least 60 ÷ 0.70 = $85.71, which is 14.3% below the $100 base case and above the $75 weak case. Then, for a company you follow, compute M twice, once from your own V and once from book value per share; the gap between the two is the claim to defend.""",
        [
            ('paper', 'Lakonishok, Shleifer & Vishny', 1993, 'Contrarian Investment, Extrapolation, and Risk', 'https://doi.org/10.3386/w4360',
             'NBER working-paper version of the 1994 Journal of Finance article: NYSE and AMEX stocks, April 1963 to April 1990, value versus glamour portfolios, and the argument that the value premium reflects extrapolation errors rather than extra risk.'),
            ('paper', 'Fama & French', 1992, 'The Cross-Section of Expected Stock Returns', 'https://doi.org/10.1111/j.1540-6261.1992.tb04398.x',
             'Size and book-to-market equity capture the variation in average returns associated with market beta, leverage and earnings-price ratios, while the beta-return relation is flat once beta varies independently of size.'),
            ('arxiv', 'Chen, Lopez-Lira & Zimmermann', 2022, 'Does Peer-Reviewed Research Help Predict Stock Returns?', 'https://arxiv.org/abs/2212.10317',
             'Both peer-reviewed predictors and data-mined accounting ratios keep only about half of their predictability after the original sample periods, a caution for treating a historical discount pattern as a margin of safety.'),
        ],
    ),
    "1.6": (
        r"""Two outside facts tighten the file. First, deadlines: Form 10-K sets the annual-report deadline at 60 days after fiscal year-end for large accelerated filers, 75 days for accelerated filers and 90 days for all other registrants. For a December 31 year-end in an ordinary year, those fall on March 1, March 16 and March 31. If Alder's year ended December 31, its March 15 release is day 74: inside the 75- and 90-day windows but past the 60-day one, so the file needs its filer category (our arithmetic). A deadline is not the filing date, which must be recorded.

Second, the receivables signal. Dechow and co-authors examined 2,190 SEC enforcement releases (AAERs) from 1982 to 2005, covering 676 firms that misstated results. Almost half the misstating firms were alleged to have misstated sales, and change in receivables had the highest t-statistic of all accrual variables. Yet an F-score cut-off of 1.4 flagged over 50 percent of misstating firms and 20 percent of public firms; because misstatement is rare, most flagged firms are probably clean (our inference). Their variable scales the receivables change by average total assets, so Alder's rise from 15% to 20% of sales is related, not identical.

Jofre and Gerlach built 1,594 fraud-year observations from SEC releases for 1990 to 2012, stopping at 2012 because their study began in mid-2013, when that year's cases could still come to light. By analogy, Alder's newest year is "not yet flagged", not "clean" (our inference).

Check: add filer category, period-end date and filing date to the file, then set Alder's 60% receivables growth beside 20% revenue growth, with two benign explanations and the document that separates them from collection trouble.""",
        [
            ('official', 'U.S. SEC', None, 'Form 10-K: General Instructions', 'https://www.sec.gov/files/form10-k.pdf',
             "General Instruction A(2) sets annual-report deadlines of 60, 75 or 90 days after fiscal year-end by filer category, a reference point for when a period's accounts should have become public."),
            ('paper', 'Dechow, Ge, Larson & Sloan', 2011, 'Predicting Material Accounting Misstatements', 'https://doi.org/10.1111/j.1911-3846.2010.01041.x',
             'Builds a database from 2,190 SEC enforcement releases (1982 to 2005) and shows that receivables changes stand out among accrual variables, with an F-score cut-off that over half of misstating firms, but also 20 percent of public firms, exceed.'),
            ('arxiv', 'Jofre & Gerlach', 2018, 'Fighting Accounting Fraud Through Forensic Data Analytics', 'https://arxiv.org/abs/1805.02840',
             "Labels fraud from SEC releases for 1990 to 2012 and stops the sample at 2012 because the study began in mid-2013, when that year's cases could still be discovered, a reminder that the newest accounts have not yet been tested."),
        ],
    ),
    "1.7": (
        r"""Two studies show how loose an honest value range can be. Liu, Nissim and Thomas collected firms each April from 1982 to 1999 (26,613 observations before further screens). Forward-earnings multiples came within 15 percent of stock prices for about half the sample, which needed analyst forecasts and positive values, so many firm-years were excluded. Gilson, Hotchkiss and Ruback compared the market value of firms reorganizing in bankruptcy with estimates built from management's published cash flow projections: the estimates were generally unbiased, yet the ratio of estimated to market value ran from under 20% to over 250%, with errors related to claimholders' incentives to overstate or understate value.

Both benchmark against market value, and Liu and co-authors assume market efficiency. Closeness to price therefore measures agreement with the market, not whether a Graham-style estimate is right (our inference).

The cash term in the bridge carries error too. Pinkowitz, Stulz and Williamson found the relation between cash holdings and firm value much weaker in countries with poor investor protection, as agency theory predicts when controlling shareholders can extract private benefits. Alder's $20 million of excess cash is $2 a share; credit half of it and the $14–18 range becomes $13–17 (our arithmetic).

Check: at the $13 quote, a 15% band is $11.05 to $14.95. Alder's $14 low end sits inside it, so at multiple-like accuracy a 7.1% discount is indistinguishable from noise (our inference); $18, 38.5% above the price, needs a stated reason. Write what must be true for the upper endpoint.""",
        [
            ('paper', 'Liu, Nissim & Thomas', 2002, 'Equity Valuation Using Multiples', 'https://doi.org/10.1111/1475-679X.00042',
             'Tests how closely multiples track stock prices for firms collected each April from 1982 to 1999: forward earnings come within 15 percent for about half the sample, which excludes firms lacking analyst forecasts or positive values.'),
            ('paper', 'Gilson, Hotchkiss & Ruback', 2000, 'Valuation of Bankrupt Firms', 'https://doi.org/10.1093/rfs/13.1.43',
             "Compares market values of firms reorganizing in bankruptcy with estimates built from management's cash flow projections: unbiased on average, but the estimate-to-market ratio spans under 20% to over 250%."),
            ('paper', 'Pinkowitz, Stulz & Williamson', 2006, 'Does the Contribution of Corporate Cash Holdings and Dividends to Firm Value Depend on Governance? A Cross-country Analysis', 'https://doi.org/10.1111/j.1540-6261.2006.01003.x',
             'Valuation regressions across countries show the link between cash holdings and firm value is much weaker where investor protection is poor, so excess cash may not be worth its face amount to minority owners.'),
        ],
    ),
    "1.2": (
        r"""Federal Reserve staff define interest coverage as EBIT divided by interest expense and measured it for US nonfinancial firms in Compustat from 1970 to 2017. The average was about 3.7, and on average about one third of firms, weighted by debt, had ratios below 2. Alder's 4.0 times is near that average; its weak-year 1.5 falls below 2. Yet the same note found that one ratio maps to different default rates by industry: the industry-level ratio tied to a 1.5 percent default rate was about 3.3 for communications and 5.1 for retail. Its warning: a simple reading of a low ratio may mislead.

Coverage also says nothing about when principal falls due. Almeida and co-authors compared firms whose long-term debt largely matured right after the third quarter of 2007 with similar firms whose debt fell due after 2008. The first group cut investment-to-capital by 2.5 percentage points more per quarter, one-third of pre-crisis investment. Alder's $100 million of principal next year, against $45 million of cash and expected surplus, is that kind of exposure (our inference).

Korangi, Mues and Bravo, modelling US mid-cap defaults over 30 years, found accounting data still the largest contributor, with market data second. Our inference: coverage work is not wasted, but it is one input.

Check: write Alder's 4.0 and 1.5 beside its own industry's average ratio, then divide internal sources by principal due: ($20 million + $25 million) ÷ $100 million = 45%, leaving the $55 million gap that neither ratio shows.""",
        [
            ('official', 'Palomino, Paolillo, Perez-Orive & Sanz-Maldonado', 2019, 'The Information in Interest Coverage Ratios of the US Nonfinancial Corporate Sector', 'https://www.federalreserve.gov/econres/notes/feds-notes/information-in-interest-coverage-ratios-of-the-us-nonfinancial-corporate-sector-20190110.html',
             'Federal Reserve Board staff note: EBIT-over-interest ratios for Compustat nonfinancial firms, 1970 to 2017, and evidence that the same ratio corresponds to different default rates in different industries.'),
            ('paper', 'Almeida, Campello, Laranjeira & Weisbenner', 2012, 'Corporate Debt Maturity and the Real Effects of the 2007 Credit Crisis', 'https://doi.org/10.1561/104.00000001',
             'Natural experiment on long-term debt that happened to mature right after the third quarter of 2007: those firms cut investment by 2.5 percentage points more than similar firms, showing that the timing of principal matters.'),
            ('arxiv', 'Korangi, Mues & Bravo', 2021, 'A transformer-based model for default prediction in mid-cap corporate markets', 'https://arxiv.org/abs/2111.09902',
             'Thirty years of US mid-cap data: a deep-learning default model ranks accounting data as the largest contributor to default prediction and market data second, so financial-statement work remains central.'),
        ],
    ),
    "1.8": (
        r"""The lesson's waterfall stipulates priority and leaves equity with nothing. Eberhart, Moore and Roenfeldt examined thirty reorganization filings under the 1978 Bankruptcy Reform Act and found that the amount paid to shareholders beyond absolute priority averaged 7.6% of the total awarded to all claimants. Illustration: if 7.6% of Alder's $70 million pool, $5.32 million, reached equity first and the junior claim bore it, junior recovery would be 14.68 ÷ 30 = 48.9%, not 66.7% (our arithmetic; the 7.6% is an average over their own cases).

The pool is not a fixed number either. Acharya, Bharath and Srinivasan studied US defaulted firms from 1982 to 1999: in present-value terms, creditors recovered significantly less when the industry was in distress, particularly if its assets were specific, not easily redeployable by other industries, and the debt was collateralized by them. Altman and co-authors examined bond defaults from 1982 to 2002 and found that recovery rates depend on supply and demand for the securities, with default rates playing a pivotal role. Becker and co-authors, in an arXiv study of Moody's data for senior secured bonds, likewise report a strong negative correlation between default probability and recovery rate. Our inference: Alder's $40 million case is more likely to arise when other borrowers are failing too.

Check: rerun the pool at $70 million, at $40 million (senior 80%, junior zero) and with the 7.6% deviation, then discount each recovery for a two-year wait at a rate you state. Label every run illustrative.""",
        [
            ('paper', 'Eberhart, Moore & Roenfeldt', 1990, 'Security Pricing and Deviations from the Absolute Priority Rule in Bankruptcy Proceedings', 'https://doi.org/10.1111/j.1540-6261.1990.tb03723.x',
             'Thirty reorganization filings under the 1978 Bankruptcy Reform Act: shareholders received, on average, an amount equal to 7.6 percent of total awards in excess of absolute priority, so a stipulated waterfall is a simplification.'),
            ('paper', 'Acharya, Bharath & Srinivasan', 2007, 'Does industry-wide distress affect defaulted firms? Evidence from creditor recoveries', 'https://doi.org/10.1016/j.jfineco.2006.05.011',
             'US defaults from 1982 to 1999: creditors recover less, in present value, when the industry is distressed, especially where assets are specific and pledged as collateral, so collateral value depends on who else can buy it.'),
            ('paper', 'Altman, Brady, Resti & Sironi', 2005, 'The Link between Default and Recovery Rates: Theory, Empirical Evidence, and Implications', 'https://doi.org/10.1086/497044',
             'Corporate bond defaults from 1982 to 2002: recovery rates depend on supply and demand for the defaulted securities, with default rates playing a pivotal role, so scenario recoveries move with the default cycle.'),
            ('arxiv', 'Becker, Koivusalo & Schäfer', 2012, 'Empirical Evidence for the Structural Recovery Model', 'https://arxiv.org/abs/1203.3188',
             "Uses Moody's Default and Recovery Database to relate default probability and recovery rate for senior secured bonds and finds a strong negative correlation; a modest arXiv-only study, offered as corroboration."),
        ],
    ),
}
