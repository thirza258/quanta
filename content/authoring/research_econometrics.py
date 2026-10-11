"""Research extensions for Financial econometrics & factor models.

Each entry maps a lesson ID to (body, sources). A source is
(kind, authors, year, title, url, what it contributes); see research_depth.py.
Every figure was checked against a verbatim snippet from its source before merging.
"""

NOTES = {
    "3.6": (
        r"""One regression line can seem to serve three different jobs, and the methodological literature separates them. Hernán, Hsu and Healy sort data-science work into description, prediction, and counterfactual prediction, which includes causal inference, and argue that each class needs its own data, assumptions and analytics. For the causal class they add that good data and algorithms are not enough without domain expert knowledge. Shmueli makes a parallel point about statistical modelling: many fields use models almost only for causal explanation and assume that high explanatory power means high predictive power. She argues the goals must be kept apart, partly because with a finite quantity of real data an optimal model for prediction may differ from the one obtained by estimating the "true model".

Lundberg, Johnson and Stewart turn this into a procedure. State the theoretical estimand in precise terms that exist outside any statistical model, link it to an empirical estimand that is informative about it under stated identification assumptions, and only then learn from data. The estimator comes last, not first.

Apply the three steps to Cedar's fitted line, with intercept 0.1 and slope 1.2. As a description, the slope summarises how excess returns and the factor moved together in the sample. As a forecast, the factor has to be known before the return it is meant to predict, and a same-month factor generally is not; our inference, not a finding of these papers, is that a forecast therefore needs a lagged equation and an out-of-sample loss. As a cause, the fitted mean of 2.5 at a factor value of 2 says nothing until you can argue what could move the factor and what else moves with it.

Exercise: write Cedar's claim three times, once per task. For each version name the theoretical estimand, the empirical estimand, and the assumption that connects them. A version where you cannot state the connecting assumption remains an association.""",
        [
            ('arxiv', 'Hernán, Hsu & Healy', 2018, "Data science is science's second chance to get causal inference right: A classification of data science tasks", 'https://arxiv.org/abs/1804.10846',
             "Splits analysis into description, prediction and counterfactual prediction and says each needs different data, assumptions and analytics; used to separate three readings of Cedar's fitted line."),
            ('arxiv', 'Shmueli', 2011, 'To Explain or to Predict?', 'https://arxiv.org/abs/1101.0891',
             'Argues that explanatory and predictive modelling are different goals and that high explanatory power is wrongly assumed to imply high predictive power.'),
            ('paper', 'Lundberg, Johnson & Stewart', 2021, 'What Is Your Estimand? Defining the Target Quantity Connects Statistical Evidence to Theory', 'https://doi.org/10.1177/00031224211004187',
             'Defines the estimand as the target quantity and gives a three-step framework from theoretical estimand to empirical estimand to estimation.'),
        ],
    ),
    "3.7": (
        r"""Four sources show how often a tidy table hides a dating problem. Shumway and Warther studied CRSP's Nasdaq data and found that returns for delisted stocks were often missing, that the missing returns were large and negative on average, and that delisted stocks lost liquidity. They estimated that using a return of −55 percent for missing performance-related delistings corrects the bias, and after that correction they found no evidence that a Nasdaq size effect ever existed. Our inference is that a complete-case join that quietly drops distressed names can manufacture a result, not just shrink the sample.

Membership has the same problem. Daniel, Sornette and Wohrmann showed that testing a portfolio against the assets in a benchmark at the end of the period, rather than the start, creates a look-ahead benchmark bias of up to 8% a year for the S&P 500, using CRSP data from 1926 to 2006.

Vendors also revise history. Ljungqvist, Malloy and Marston compared seven downloads of the IBES recommendations database taken between 2000 and 2007, and between 6,580 (1.6%) and 97,582 (21.7%) of matched observations differed from one download to the next. Record the download date, not just the vendor.

Even a standard factor file states its conventions. French's description says the stocks in SMB and HML for July of year t to June of t+1 need market equity data for December of t−1 and June of t, plus positive book equity for t−1, and that the one-month bill rate comes from Ibbotson Associates through May 2024 and from an ICE BofA index afterwards.

Exercise: in the lesson's 120-date join, label each of the 15 lost rows (ten missing factor values, five missing asset returns) by cause: closure, suspension, delisting or vendor gap. Any row you cannot explain is an untested assumption behind the 105-row result.""",
        [
            ('paper', 'Shumway & Warther', 1999, "The Delisting Bias in CRSP's Nasdaq Data and Its Implications for the Size Effect", 'https://doi.org/10.1111/0022-1082.00192',
             'Shows that missing delisting returns were large and negative and that correcting them removes the apparent Nasdaq size effect; the model case for non-random missingness.'),
            ('arxiv', 'Daniel, Sornette & Wohrmann', 2008, 'Look-Ahead Benchmark Bias in Portfolio Performance Evaluation', 'https://arxiv.org/abs/0810.1922',
             'Quantifies the bias from defining a benchmark universe with end-of-period rather than start-of-period constituents, using CRSP 1926 to 2006.'),
            ('paper', 'Ljungqvist, Malloy & Marston', 2009, 'Rewriting History', 'https://doi.org/10.1111/j.1540-6261.2009.01484.x',
             'Documents ex post changes between vendor downloads of the I/B/E/S recommendations database; the case for recording source versions and download dates.'),
            ('data', 'French', None, 'Description of Fama/French Factors', 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html',
             'States how the standard factors are built: the timing of market and book equity, the sample screens, and the source of the risk-free rate.'),
        ],
    ),
    "3.8": (
        r"""The lesson's advice to solve rather than invert has a measurable record. Longley's 1967 appraisal of least-squares programs left behind a 16-observation dataset that NIST still distributes in its Statistical Reference Datasets. NIST rates it, like the 82-observation Filip polynomial problem, as higher difficulty, and calls the higher-difficulty datasets multicollinear. Its stated reason for the collection is that even with reliable code available, problems persist, often because the best algorithms are not used. NIST also reports meeting codes that produce negative R-squared and incorrect F statistics on its lines-through-the-origin datasets, which echoes the lesson's no-intercept warning.

Conditioning is the mechanism. Mirzaei's lecture notes state that forming XᵀX squares the condition number of X. In the statsmodels Longley example the raw design has condition number 4.86e+09, falling to about 56,000 once each regressor is scaled to unit length, still far above the page's cited rule of thumb of 20.

NIST's suggested remedy is centering, which the lesson's slope formula already does through x − x̄. For the lesson's three points, centering makes the two columns orthogonal and cuts the condition number from about 6.8 to 1.22 (our arithmetic). In our own double-precision run on the Filip file, subtracting the mean of x cut the condition number from about 1.8e15 to about 1.3e5. On the raw powers of x, a normal-equations solve returned no correct digits, Cholesky failed, and QR matched NIST's certified coefficients to about 7 digits. The default statsmodels pseudoinverse also returned none, because its 1e-15 rank cutoff discards the smallest singular value; method="qr" returned about 7. After centering, every solver we tried agreed on the fitted values.

Exercise: repeat this on Filip with your own software, judging each fit by comparing its fitted values with those from NIST's certified coefficients.""",
        [
            ('official', 'NIST · Statistical Reference Datasets', None, 'Linear Least Squares Regression: Background Information', 'https://www.itl.nist.gov/div898/strd/lls/lls_info.shtml',
             "NIST's account of why certified regression benchmarks exist, which datasets are multicollinear, and why centering the data is the suggested remedy."),
            ('paper', 'Longley', 1967, 'An Appraisal of Least Squares Programs for the Electronic Computer from the Point of View of the User', 'https://doi.org/10.1080/01621459.1967.10500896',
             'The 1967 appraisal of least-squares programs that supplied the Longley benchmark data still used to test regression software.'),
            ('docs', 'statsmodels contributors', None, 'Ordinary Least Squares', 'https://www.statsmodels.org/stable/examples/notebooks/generated/ols.html',
             'Worked Longley example showing the raw condition number, the value after unit-length scaling, and the rule of thumb of 20.'),
            ('arxiv', 'Mirzaei', 2024, 'Numerical Linear Algebra: Least Squares, QR and SVD', 'https://arxiv.org/abs/2412.19960',
             'Lecture notes stating why the normal equations square the condition number and why QR or SVD factorisations are preferred.'),
        ],
    ),
    "3.1": (
        r"""The Frisch–Waugh–Lovell result behind partial slopes has a less familiar second half. Ding showed that regressing the residualized outcome on the residualized regressor reproduces the full regression's coefficient and its Eicker–Huber–White robust standard error exactly, while the classical standard errors differ only by a degrees-of-freedom correction. Done by hand, the second step forgets the degrees of freedom spent on the K controls. Ding's theorem implies the variance comes out too small by the factor (n − K − L)/(n − L), where L counts the focal regressors; that is 95/99 for n = 100, K = 4 and L = 1 (our arithmetic).

The variance inflation factor rests on the same residualization: only the share 1 − R² of a regressor's variation is left, which is the 20% behind the lesson's VIF of 5. O'Brien argued that thresholds such as 10 must be read with sample size, the regressor's own variance and the model's unexplained variance, because all of them scale a coefficient's variance, and that VIFs of 10, 20, 40 or higher do not by themselves discount a regression. His formula implies that a VIF of 5 with 496 observations leaves the same coefficient variance as a VIF of 1 with 100, since 495/99 = 5 (our arithmetic). Small samples cut the other way. In the statsmodels Longley example, with 16 observations and a condition number of 4.86e+09, refitting on the first 14 moves two coefficients by −105.20% and 97.06%.

A finance case: Fama and French reported that once profitability and investment factors are added, the value factor becomes redundant for describing average returns in the sample they examine. A factor's coefficient depends on which other factors share the model.

Exercise: fit a model with controls, then rebuild one slope from the two residual series. Confirm that the coefficients match and that the classical standard errors differ by √((n − K − L)/(n − L)).""",
        [
            ('arxiv', 'Ding', 2020, 'The Frisch-Waugh-Lovell Theorem for Standard Errors', 'https://arxiv.org/abs/2009.06621',
             'Extends the Frisch–Waugh–Lovell theorem from coefficients to standard errors: robust errors are identical in the full and partial fits, and classical errors differ only by a degrees-of-freedom factor.'),
            ('paper', "O'Brien", 2007, 'A Caution Regarding Rules of Thumb for Variance Inflation Factors', 'https://doi.org/10.1007/s11135-006-9018-6',
             'Shows that VIF thresholds must be judged alongside sample size, regressor variance and fit, with worked variance ratios.'),
            ('docs', 'statsmodels contributors', None, 'Ordinary Least Squares', 'https://www.statsmodels.org/stable/examples/notebooks/generated/ols.html',
             'Longley example: a large condition number and coefficients that move sharply when two observations are dropped.'),
            ('paper', 'Fama & French', 2015, 'A five-factor asset pricing model', 'https://doi.org/10.1016/j.jfineco.2014.10.010',
             'Factor-model example in which the value factor becomes redundant once profitability and investment factors are included.'),
        ],
    ),
}
