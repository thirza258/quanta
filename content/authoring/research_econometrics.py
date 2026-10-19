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
    "3.9": (
        r"""Three results extend the lesson's t = 3 example.

Gelman and Stern showed that a change in significance status is often not itself significant, and that even a large change in significance level can match a small, nonsignificant change in the underlying quantity. Suppose a second coefficient, estimated independently, is .2 with the same standard error: t = 1 beside the lesson's t = 3. Their difference of .4 has standard error √(.2² + .2²) ≈ .283, so t ≈ 1.41 (our arithmetic). The data give no sign that the two differ.

The lesson's intervals also answer different questions. With a fitted-mean standard error of .1 and a disturbance standard deviation of .5, the large-sample 95% interval for the mean (±.196) would contain a new observation about 30% of the time; the prediction interval is about five times wider (our arithmetic, normal errors).

Joint tests depend on how estimates co-vary. Two coefficients with t = 1.5 each have individual p-values near .13. If the estimates are correlated at −.8, as two strongly positively correlated regressors would give, the Wald statistic (t₁² − 2ρt₁t₂ + t₂²)/(1 − ρ²) is 22.5 on two degrees of freedom; at ρ = 0 it is 4.5 (our arithmetic). Gibbons and co-authors derived a finite-sample test of a portfolio's efficiency, in regression terms a joint test that every alpha is zero (our gloss), and their examples suggest multivariate inference can reach better conclusions than a set of dependent univariate statistics.

McShane and co-authors, writing for the biomedical and social sciences, would demote the p-value from a threshold to one continuous piece of evidence beside prior evidence, mechanism, design quality and costs and benefits.

Exercise: fit a two-factor regression and report each t-statistic, the correlation between the two coefficient estimates, and the joint Wald test with its reference distribution.""",
        [
            ('paper', 'Gelman & Stern', 2006, 'The Difference Between “Significant” and “Not Significant” is not Itself Statistically Significant', 'https://doi.org/10.1198/000313006X152649',
             "Shows that changes in statistical significance are often not themselves significant; the basis for comparing the lesson's significant and nonsignificant coefficients through their difference."),
            ('paper', 'Gibbons, Ross & Shanken', 1989, 'A Test of the Efficiency of a Given Portfolio', 'https://doi.org/10.2307/1913625',
             'Derives a joint test with a tractable small-sample distribution and argues that multivariate inference can beat a set of dependent univariate statistics; the standard joint test in factor-model work.'),
            ('arxiv', 'McShane et al.', 2017, 'Abandon Statistical Significance', 'https://arxiv.org/abs/1709.07588',
             'Argues for dropping p-value thresholds and treating p-values continuously alongside prior evidence, mechanism, design and costs and benefits.'),
        ],
    ),
    "3.10": (
        r"""Both robust errors and weights have documented failure modes.

Long and Ervin ran Monte Carlo simulations of heteroskedasticity-consistent estimators. HC0, the version most applications then appeared to use, often gave incorrect inferences when N ≤ 250, while HC3 worked well even at N = 25. They recommend HC3 when N ≤ 250, and advise against letting a screening test for heteroskedasticity decide whether to use a robust estimator. The advice has a boundary. Cattaneo and co-authors show that when the number of covariates grows as fast as the sample size, all the usual Eicker–White versions are inconsistent, though a variant of HC3 errs upward, so its inference stays valid but conservative. Our inference: HC3 is the safer default in both regimes, at some cost in power in the second.

King and Roberts argue that when classical and robust standard errors diverge, assuming the misspecification does not also bias everything else takes considerable optimism. The lesson's robust error of .2 against a classical .1 is a twofold divergence; read it as a clue about the model, not only as a correction.

Weighting is a different intervention. In the lesson's two-observation example, inverse-variance weights cut the variance of the mean from 1.25 to .8, a 36% reduction (our arithmetic, independent observations). Solon and co-authors distinguish three motives for weighting in causal work: precision under heteroskedasticity, consistency under endogenous sampling, and identification of average partial effects under unmodeled heterogeneity. They find that the motive sometimes does not apply where practitioners assume it does.

Exercise: fit your regression with HC0 and HC3 errors, then again with your proposed weights. Report coefficient changes and standard-error changes separately, and name the motive that justifies each weight.""",
        [
            ('paper', 'Long & Ervin', 2000, 'Using Heteroscedasticity Consistent Standard Errors in the Linear Regression Model', 'https://doi.org/10.1080/00031305.2000.10474549',
             'Monte Carlo evidence that HC0 misleads in samples up to 250 observations while HC3 works well even at 25; the source for choosing an HC variant deliberately.'),
            ('arxiv', 'Cattaneo, Jansson & Newey', 2015, 'Inference in Linear Regression Models with Many Covariates and Heteroskedasticity', 'https://arxiv.org/abs/1507.02493',
             'Shows that the usual Eicker–White estimators are inconsistent when covariates grow with the sample size, and that a variant of HC3 is upward biased and therefore conservative.'),
            ('paper', 'King & Roberts', 2015, 'How Robust Standard Errors Expose Methodological Problems They Do Not Fix, and What to Do About It', 'https://doi.org/10.1093/pan/mpu015',
             'Argues that a gap between classical and robust standard errors signals misspecification that robust errors do not repair.'),
            ('paper', 'Solon, Haider & Wooldridge', 2015, 'What Are We Weighting For?', 'https://doi.org/10.3368/jhr.50.2.301',
             'Separates three motives for weighting in causal work and finds that practitioners often assume a motive applies when it does not.'),
        ],
    ),
    "3.11": (
        r"""The lesson's weight of .5 at lag one is a Bartlett weight, and it matters. Newey and West built their estimator to be positive semi-definite by construction, which a plain sum of autocovariances is not: with lag-zero autocovariance 1 and lag-one autocovariance −.6, the unweighted one-lag sum is 1 + 2(−.6) = −.2, an impossible variance, while the weight .5 gives .4 (our arithmetic).

Lag length is the harder choice. Lazarus and co-authors report that a larger-than-usual truncation parameter plus Kiefer–Vogelsang fixed-b critical values can substantially reduce size distortions at a modest cost in power, and that practice has not kept up. For Newey–West tests they recommend S = 1.3√T with nonstandard fixed-b critical values: S = 13 for the lesson's 100 observations, against one lag in the worked example (our arithmetic; check how your software maps S to its lag option).

Baillie and co-authors add that popular HAC estimators are ill-suited to the autoregressive autocorrelation typical of economic series, giving large size distortions and reduced power in all but the largest samples, and that OLS estimates can themselves be inconsistent, so that HAC inference fails even asymptotically.

A check of ours: two independent AR(1) series with φ = .8, 100 observations, 5,000 replications. A nominal 5% test of the true zero slope rejected in 34% of samples with classical errors, 28% with Newey–West at one lag, 20% at four lags and 19% at 12 or 13 lags, using standard-normal critical values. Longer lags helped but still left nearly four times the nominal rate.

Exercise: rerun the simulation at φ = .5 and φ = .95 and note where additional lags stop helping.""",
        [
            ('paper', 'Newey & West', 1987, 'A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix', 'https://doi.org/10.2307/1913610',
             "The original Bartlett-weighted HAC estimator, positive semi-definite by construction; explains why the lesson's lag-one weight is .5 rather than 1."),
            ('paper', 'Lazarus, Lewis, Stock & Watson', 2018, 'HAR Inference: Recommendations for Practice', 'https://doi.org/10.1080/07350015.2018.1506926',
             'Reviews the size distortions of Newey–West tests and recommends a longer truncation parameter, S = 1.3T^(1/2), with fixed-b critical values.'),
            ('arxiv', 'Baillie et al.', 2022, 'On Robust Inference in Time Series Regression', 'https://arxiv.org/abs/2203.04080',
             'Argues that HAC inference suffers size distortions and power loss with autoregressive dependence and can fail even asymptotically when OLS estimates are inconsistent; published in The Econometrics Journal in 2024.'),
        ],
    ),
    "3.12": (
        r"""The lesson's formula, β_short = β + γδ, hides one product, and sensitivity analysis asks how large it must be. In the lesson's numbers a reported slope of 2 is a direct effect of 1 plus a bias of 1. Removing the whole slope needs a bias of 2, for instance γ = 4 at the same δ = .5, while a direct effect of 3 with δ = −.5 gives the same reported 2 (our arithmetic).

Cinelli and Hazlett turn this into numbers for routine reporting, chiefly the robustness value: the minimum strength of association that unobserved confounding would need with both the treatment and the outcome to change the research conclusions. They also describe problems with a common benchmarking practice and give a procedure that bounds confounder strength formally by comparison with observed covariates.

Oster examines the habit of watching a coefficient move as controls are added. That is informative only if selection on observables is informative about selection on unobservables, and R-squared movements must be read alongside coefficient movements. The lesson's slope halves from 2 to 1 once z enters; Oster's point is that whether this reassures depends on R-squared as well. Diegert and co-authors add that such comparisons run into limits when omitted variables are correlated with the included controls, and propose a regression sensitivity analysis that avoids those limits while still calibrating against selection on observables.

In factor work the same algebra reaches the intercept (our derivation): omitting a factor z with loading γ shifts alpha by γ(μ_z − δμ_x), the omitted premium net of what the included factor absorbs.

Exercise: for a slope of your own, state the bias γδ that would reduce it to zero, then name an omitted variable that could plausibly be that strong.""",
        [
            ('paper', 'Oster', 2019, 'Unobservable Selection and Coefficient Stability: Theory and Evidence', 'https://doi.org/10.1080/07350015.2016.1227711',
             'Shows that coefficient stability across specifications is informative only under stated conditions and that R-squared movements must be considered; the formal bounding argument behind comparing specifications.'),
            ('paper', 'Cinelli & Hazlett', 2020, 'Making Sense of Sensitivity: Extending Omitted Variable Bias', 'https://doi.org/10.1111/rssb.12348',
             'Extends the omitted-variable-bias formula into sensitivity measures, including the robustness value, computed from standard regression output.'),
            ('arxiv', 'Diegert, Masten & Poirier', 2022, 'Assessing Omitted Variable Bias when the Controls are Endogenous', 'https://arxiv.org/abs/2206.02303',
             'Develops a regression sensitivity analysis that stays valid when omitted variables are correlated with the included controls, where earlier comparison methods run into limits.'),
        ],
    ),
    "3.13": (
        r"""Stationarity tests answer narrower questions than their names suggest. Kwiatkowski and co-authors argued that the common failure to reject a unit root may simply mean that economic series say little about it, or equivalently that unit-root tests have low power against relevant alternatives. A simulation of ours puts a scale on this. On the lesson's AR(1) with mean 1 (100 observations, 5,000 replications), a 5% Dickey–Fuller test with a constant rejects the unit root in 89% of samples at φ = .8, but in 34% at φ = .9 and 14% at φ = .95. The KPSS test, whose stationarity null is true at φ = .8, rejected it in 21% of samples against a nominal 5%, and both nulls were rejected together in 16.5%.

Perron added a second trap: standard unit-root tests cannot reject when the true process fluctuates around a trend that contains a one-time break. A failure to reject can therefore reflect low power, a break, or the wrong deterministic terms.

The lesson's warning about random walks has a measurable size. Ernst and co-authors mathematically confirmed Yule's classic finding of nonsense correlation by computing the second moment of the correlation between two independent Wiener processes, random walks in continuous time. Its standard deviation is nearly .5, its distribution is heavily dispersed and frequently large in absolute value, and the cause is that each process is self-correlated in time, an integral of pure noise. In our simulation, 77% of 5,000 regressions of one independent 100-step random walk on another gave |t| > 1.96, against 5% after differencing.

Exercise: repeat the pair simulation in levels and in differences, and report both rejection rates.""",
        [
            ('paper', 'Kwiatkowski, Phillips, Schmidt & Shin', 1992, 'Testing the null hypothesis of stationarity against the alternative of a unit root', 'https://doi.org/10.1016/0304-4076%2892%2990104-Y',
             'Introduces the KPSS stationarity test and argues that the usual failure to reject a unit root reflects the low power of unit-root tests; the basis for treating ADF and KPSS as complements.'),
            ('paper', 'Perron', 1989, 'The Great Crash, the Oil Price Shock, and the Unit Root Hypothesis', 'https://doi.org/10.2307/1913712',
             'Shows that standard unit-root tests cannot reject when a stationary series fluctuates around a trend with a one-time break.'),
            ('arxiv', 'Ernst, Shepp & Wyner', 2016, 'Yule\'s "Nonsense Correlation" Solved!', 'https://arxiv.org/abs/1608.04120',
             "Confirms Yule's nonsense-correlation finding mathematically by computing the spread of the correlation between independent Wiener processes, a standard deviation of nearly .5; published in the Annals of Statistics in 2017."),
        ],
    ),
    "3.14": (
        r"""The lesson's forecasts converge to the mean of 1, and their uncertainty settles at a constant. Hyndman and Athanasopoulos note that with a constant and no differencing, long-term forecasts go to the mean of the data and the forecast standard deviation goes to the historical standard deviation, so prediction intervals stop widening. For the lesson's model the standard deviation rises from .2 at one step to .256 at two and approaches √(.04/(1 − .64)) ≈ .333 (our arithmetic). Their one-step interval, the forecast ± 1.96 residual standard deviations, holds for every ARIMA model, but all the intervals assume uncorrelated, normal residuals.

How much the model adds over the random-walk baseline is a separate question. With known parameters the lesson's one-step error variance is .04 against .0444 for the random-walk forecast, a ratio of (1 + φ)/2 = .9 (our arithmetic). Estimation spends part of that gain. Petropoulos and co-authors split forecast mean squared error into noise, a variance term from estimating parameters, and squared bias, and report Ca' Zorzi and co-authors' analytical result: for persistent AR(1) processes with a half-life over two years, the random walk, or an AR(1) with φ fixed at a value implying a five-year half-life, tends to beat the estimated AR(1). In our simulation (100 observations, 20,000 replications) the estimated AR(1) had about 8% lower one-step mean squared error than the naive forecast at φ = .8, and about 3% higher at φ = .99.

Meese and Rogoff tested the baseline on monthly data from March 1973 to June 1981: a random walk performed as well as any estimated model at one to twelve month horizons for several dollar exchange rates, even though the structural models were given realized future values of their explanatory variables.

Exercise: simulate the lesson's AR(1), fit it on 100 observations, and compare its one-step squared error with the naive forecast at φ = .8 and φ = .99.""",
        [
            ('book', 'Hyndman & Athanasopoulos', None, 'Forecasting: Principles and Practice, 3rd edition', 'https://otexts.com/fpp3/arima.html',
             'Chapter 9 of the online textbook: how ARIMA forecasts and prediction intervals behave at long horizons, how the constant and differencing order matter, and the residual assumptions behind the intervals.'),
            ('arxiv', 'Petropoulos et al.', 2020, 'Forecasting: theory and practice', 'https://arxiv.org/abs/2012.03854',
             'Encyclopedic review whose bias-variance discussion reports why the random walk is a tough benchmark for persistent processes.'),
            ('paper', 'Meese & Rogoff', 1983, 'Empirical exchange rate models of the seventies', 'https://doi.org/10.1016/0022-1996%2883%2990017-X',
             'Classic out-of-sample test in which a random walk matched every estimated model at one to twelve month horizons.'),
        ],
    ),
    "3.15": (
        r"""Average losses become evidence only when the test respects the forecast design. Diebold and Mariano built theirs on the loss differential, the gap between two forecasts' losses at each date, allowing non-quadratic or asymmetric losses and errors that are non-Gaussian, nonzero mean, serially correlated and contemporaneously correlated. For k-step forecasts they use the result that optimal errors are at most (k − 1)-dependent, so only k − 1 sample autocovariances enter the variance; their three-step application showed loss-differential autocorrelation at lags 1 and 2 and nowhere else. Our inference: three held-out errors, as in the lesson's [1, −1, 2], give no asymptotic test anything to work with.

Diebold later noted that the statistic can be computed by regressing the loss differential on an intercept with HAC standard errors, and that conditioning variables move it from unconditional to conditional expected loss. Giacomini and White took that view farther: their tests ask whether we can predict which forecast will be more accurate at a future date, capture estimation uncertainty, and handle nested and nonnested models.

A dissent is worth keeping. Diebold argues the test was meant for comparing forecasts, not models; for models, simpler full-sample procedures exist, and pseudo-out-of-sample analysis is not necessarily a good guard against overfitting, though it remains useful for particular historical episodes. He notes that the Schwarz criterion, as used routinely, rests on the full-sample likelihood, and the lesson's AIC has the same basis, so the comparison of 206 with 208 and a rolling-origin comparison answer different questions. Hewamalage and co-authors add that rolling origin, if not used properly, is susceptible to data leakage.

Exercise: for models A and B, collect three-step errors across origins, form the loss differential, regress it on a constant with HAC errors using two lags, then add a regime dummy and check whether the sign changes.""",
        [
            ('paper', 'Diebold & Mariano', 1995, 'Comparing Predictive Accuracy', 'https://doi.org/10.1080/07350015.1995.10524599',
             'Introduces tests on the loss differential that allow non-quadratic losses and serially correlated errors, with a lag window set by the forecast horizon; its three-step application shows the dependence that overlapping errors create.'),
            ('paper', 'Giacomini & White', 2006, 'Tests of Conditional Predictive Ability', 'https://doi.org/10.1111/j.1468-0262.2006.00718.x',
             'Extends forecast comparison to conditional objectives, estimation uncertainty, nested and nonnested models and general estimation methods.'),
            ('paper', 'Diebold', 2015, 'Comparing Predictive Accuracy, Twenty Years Later: A Personal Perspective on the Use and Abuse of Diebold–Mariano Tests', 'https://doi.org/10.1080/07350015.2014.983236',
             "Author's retrospective: the test compares forecasts, not models; full-sample criteria such as AIC and SIC answer a different question from pseudo-out-of-sample evaluation, which remains useful for historical episodes."),
            ('arxiv', 'Hewamalage, Ackermann & Bergmeir', 2022, 'Forecast Evaluation for Data Scientists: Common Pitfalls and Best Practices', 'https://arxiv.org/abs/2203.10716',
             'Tutorial on fixed-origin versus rolling-origin evaluation and the data-leakage risk in rolling setups.'),
        ],
    ),
    "3.16": (
        r"""A Granger verdict belongs to a system, and it can change with the series placed in it. Stock and Watson fitted a three-variable VAR with inflation, unemployment and the federal funds rate, using four lags and quarterly U.S. data for 1960:I–2000:IV. Unemployment helped predict inflation (p = 0.02) but the funds rate did not (p = 0.27); inflation did not help predict unemployment, but the funds rate did. Shojaie and Fox note that testing just a pair of series can give confounded inferences when many series interact, and that the standard setup assumes a fixed sampling rate matching the time scale of the causal structure.

The lesson's warning about parameter growth is easy to quantify: three variables and four lags mean 36 lag coefficients, before intercepts and the error covariance, estimated from about 160 quarters (our arithmetic). The lesson's own A has eigenvalues 0.7 and 0.4, so it is stable, and a unit shock to the first variable still moves the system by [0.38, 0.11] two steps later.

Prediction and structure part ways. In pseudo out-of-sample forecasts over 1985:I–2000:IV, the VAR did no worse than a univariate autoregression, and both beat a random walk. Structural inference needs correlation separated from causation, which Stock and Watson say a purely statistical tool cannot do; economic theory or institutional knowledge must supply it. A recursive VAR also depends on the order of the variables, and n variables allow n! orderings, six in their system (our arithmetic).

Exercise: give the lesson's system unit innovation variances and correlation 0.5. Under one Cholesky ordering the second variable's impact response to a first-variable shock is 0.5, under the other it is 0 (our arithmetic). Then rerun the Granger tests at one, two and four lags and see whether the verdicts hold.""",
        [
            ('paper', 'Stock & Watson', 2001, 'Vector Autoregressions', 'https://doi.org/10.1257/jep.15.4.101',
             'Worked three-variable VAR (inflation, unemployment, federal funds rate): Granger tests, ordering dependence of recursive VARs, pseudo out-of-sample forecasts, and why structural inference needs more than statistics.'),
            ('arxiv', 'Shojaie & Fox', 2021, 'Granger Causality: A Review and Recent Advances', 'https://arxiv.org/abs/2105.02675',
             'Review of the debate over reading Granger tests as causal, with the limits of pairwise tests, linear VARs and mismatched sampling rates.'),
        ],
    ),
    "3.2": (
        r"""Why test a residual instead of reading the slope? Phillips showed that for regressions relating independent random walks the usual t ratios have no limiting distribution and diverge as the sample grows, while the Durbin–Watson statistic converges to zero. A large t between independent random walks is therefore the expected outcome, not evidence.

MacKinnon's tables show how the residual test differs from a plain unit-root test. With a constant and no trend, the 5% asymptotic critical values for N series, each integrated of order one, are about −2.86 for N = 1, −3.34 for N = 2 and −3.74 for N = 3. The lesson's pair has N = 2, so a residual ADF statistic of −3.0 would reject a unit root alone yet fail to reject no cointegration here (our reading of the tables). MacKinnon also notes that the regressand choice changes the statistic's value, not its distribution, so the lesson's 1.5 depends on it (our inference).

A rejection is not a strategy. Rad and co-authors, studying the entire U.S. equity market from 1962 to 2014, report a mean monthly excess return of 85 bps for cointegration pairs before costs and 33 bps after, so costs took about 61% (our arithmetic), and opportunities fell from 2009. Selection is the other leak. Graziano's 2026 single-pair preprint on PepsiCo and Coca-Cola found a significant cointegrating relationship over 2013–2018, then picked its best trading policy from 901 candidates. A Deflated Sharpe Ratio, comparing the observed Sharpe ratio with the level expected from that many zero-skill strategies, came to 0.423, limited evidence of genuine skill in Graziano's reading; the later out-of-sample test produced a single losing trade.

Exercise: run the lesson's regression with each series as regressand, compare both statistics with −3.34, then refit on a later window and compare the new hedge coefficient with 1.5.""",
        [
            ('paper', 'Phillips', 1986, 'Understanding spurious regressions in econometrics', 'https://doi.org/10.1016/0304-4076%2886%2990001-1',
             'Asymptotic theory for regressions between independent random walks: t ratios diverge and the Durbin–Watson statistic goes to zero, which explains why a strong levels fit proves nothing.'),
            ('paper', 'MacKinnon', 2010, 'Critical Values for Cointegration Tests', 'https://www.econ.queensu.ca/sites/econ.queensu.ca/files/qed_wp_1227.pdf',
             'Defines the Engle–Granger residual test and tabulates its asymptotic critical values by number of series, which differ from those of a single-series Dickey–Fuller test.'),
            ('paper', 'Rad, Low & Faff', 2016, 'The profitability of pairs trading strategies: distance, cointegration and copula methods', 'https://doi.org/10.1080/14697688.2016.1164337',
             'U.S. equity evidence on cointegration-based pairs trading before and after transaction costs, with fewer trading opportunities from 2009.'),
            ('arxiv', 'Graziano', 2026, 'From Cointegration to Out-of-Sample Failure: A Pairs-Trading Case Study on PEP-KO', 'https://arxiv.org/abs/2609.35359',
             'Recent single-pair case study: a significant cointegrating relation, a best policy chosen from 901 candidates, a Sharpe ratio deflated for that search, and a losing out-of-sample trade.'),
        ],
    ),
    "3.17": (
        r"""Behind the lesson's single −0.2 sit two adjustment coefficients. In the Granger representation theorem as the Royal Swedish Academy's 2003 prize background states it, both variables' equations carry the same lagged disequilibrium, with coefficient α₁ for x and α₂ for y and at least one of them nonzero. For a spread s = y − βx the spread's own correction is then α₂ − βα₁ (our algebra, ignoring lagged differences). With the cointegration lesson's β = 1.5, the lesson's −0.2 and its 3.106-period half-life could come from y alone (α₂ = −0.2), from x alone (α₁ ≈ 0.133) or from any mix, so the half-life does not say which leg moves.

Estimation adds uncertainty. Kilian and Zha built a Bayesian framework for the half-life of deviations from purchasing power parity, confirmed substantial uncertainty, and found that no hypothesis, including Rogoff's claim of 3 to 5 years, received strong support. The curve is steep near one: φ of 0.8, 0.9, 0.95 and 0.99 give half-lives of 3.1, 6.6, 13.5 and 69 periods. With 100 observations and a fitted φ of 0.8, the textbook standard error is 0.06, so a two-standard-error band of 0.68 to 0.92 spans 1.8 to 8.3 periods (our arithmetic).

Sampling frequency matters too. In Leung and Li's Ornstein–Uhlenbeck spread, with speed μ, the transition coefficient over a step Δt is exp(−μΔt), so a daily φ of 0.8 becomes 0.8⁵ ≈ 0.33 weekly, the same 3.106 days read as 0.62 weeks (our arithmetic, five-day weeks). The Academy's background adds that transaction and information costs can make correction nonlinear, with no adjustment until a deviation passes a threshold, so a single linear half-life may average over regimes.

Exercise: fit φ on a synthetic spread, bootstrap its interval, convert both ends to half-lives, and compare the upper end with your holding limit.""",
        [
            ('official', 'Royal Swedish Academy of Sciences · NobelPrize.org', 2003, 'Time-series Econometrics: Cointegration and Autoregressive Conditional Heteroskedasticity', 'https://www.nobelprize.org/uploads/2018/06/advanced-economicsciences2003.pdf',
             "Prize background that states the Granger representation theorem with an adjustment coefficient in each variable's equation, and explains threshold error correction when transaction costs block small adjustments."),
            ('paper', 'Kilian & Zha', 2002, 'Quantifying the uncertainty about the half-life of deviations from PPP', 'https://doi.org/10.1002/jae.621',
             'Bayesian treatment of half-life uncertainty for purchasing power parity deviations; the data fail to support any of several sharp half-life claims.'),
            ('arxiv', 'Leung & Li', 2014, 'Optimal Mean Reversion Trading with Transaction Costs and Stop-Loss Exit', 'https://arxiv.org/abs/1411.5062',
             "Specifies the Ornstein–Uhlenbeck spread model and its discrete-time transition density, which links the lesson's φ to a frequency-free speed μ."),
        ],
    ),
    "3.18": (
        r"""The lesson's α + β < 1 is the finite-variance condition, not the whole stationarity story. Nelson derived necessary and sufficient conditions for stationarity and ergodicity of GARCH(1,1), showed that IGARCH(1,1) with a positive drift is still strictly stationary and ergodic, and found that whether shocks to conditional variance persist depends crucially on how persistence is defined.

The lesson's numbers show the finite-variance case. With persistence 0.9 and long-run variance 0.1, the next variance of 0.051 sits 0.049 below the long-run level, the following forecast of 0.0559 sits 0.0441 below it, and the gap halves in log(0.5)/log(0.9) ≈ 6.58 steps, the half-life formula from the error-correction lesson (our arithmetic).

Persistence estimates also deserve humility. Gatheral and co-authors found that log-volatility behaves like a fractional Brownian motion with Hurst exponent of order 0.1, and that classical procedures for detecting volatility persistence tend to conclude long memory in data from their model, where volatility is not long memory. Our inference: a fitted α + β near one describes how a recursion fits, not which mechanism generated the data.

Baselines matter too. Hansen and Lunde compared 330 ARCH-type models out of sample on Deutsche mark–dollar exchange rates and IBM returns. They found no evidence that GARCH(1,1) was outperformed on exchange rates, yet it was clearly inferior to models that accommodate a leverage effect on IBM.

Exercise: iterate the lesson's recursion forward and check the halving; then set α = 0.15 and β = 0.85, so persistence is 1, and watch the variance forecast rise by ω each step instead of settling.""",
        [
            ('paper', 'Nelson', 1990, 'Stationarity and Persistence in the GARCH(1,1) Model', 'https://doi.org/10.1017/s0266466600005296',
             'Gives necessary and sufficient stationarity conditions for GARCH(1,1), shows IGARCH with a positive drift is strictly stationary, and shows that shock persistence depends on how it is defined.'),
            ('paper', 'Hansen & Lunde', 2005, 'A forecast comparison of volatility models: does anything beat a GARCH(1,1)?', 'https://doi.org/10.1002/jae.800',
             'Out-of-sample comparison of 330 ARCH-type models on exchange-rate and IBM data; GARCH(1,1) holds up on exchange rates but not where a leverage effect matters.'),
            ('arxiv', 'Gatheral, Jaisson & Rosenbaum', 2014, 'Volatility is rough', 'https://arxiv.org/abs/1410.3394',
             'Shows log-volatility behaving like rough fractional Brownian motion and that standard persistence procedures can suggest long memory that the model does not have.'),
        ],
    ),
    "3.19": (
        r"""Asymmetry is an empirical claim, and the evidence is specific. Glosten and co-authors let positive and negative innovations affect conditional volatility differently. They found that positive unanticipated returns lowered it while negative ones raised it, and suggested that monthly volatility may be less persistent than thought. Bouchaud and co-authors measured the leverage effect as the negative correlation between past returns and future volatility: moderate for individual stocks, decaying over about 50 days, but much stronger and faster-decaying for indices. Asymmetry also changes persistence: adding the lesson's γ = 0.2 to the earlier α = 0.1 and β = 0.8 gives α + β + γ/2 = 1 for symmetric innovations, so the variance forecast no longer settles at a finite long-run level (our arithmetic).

The loss needs equal care. Patton showed that MSE and QLIKE are the only robust losses that depend solely on the forecast error and on the standardised forecast error respectively, that robust losses can penalise under-prediction or over-prediction more, and that a homogeneous robust loss keeps rankings unchanged when returns are rescaled from decimals to percentages. At v = 0.09, forecasts of 0.04 and 0.14 have equal squared error, yet QLIKE's excess over its minimum is 0.439 against 0.085 (our arithmetic): under-forecasting costs more.

Gneiting adds that a score must be consistent for the functional requested. In his GARCH(1,1) simulation a constant forecast beat the true conditional variance forecast on absolute error, and conditional value-at-risk has no strictly consistent score, while quantiles do. Our inference: tails are checked through quantile exceedances, not through a variance loss.

Exercise: simulate Gneiting's recursion (0.05, 0.20, 0.75), score the true variance and a constant with MAE and QLIKE on squared returns, then count how often returns breach each forecast's quantile band.""",
        [
            ('paper', 'Glosten, Jagannathan & Runkle', 1993, 'On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks', 'https://doi.org/10.1111/j.1540-6261.1993.tb05128.x',
             'Origin of the GJR asymmetry: negative and positive monthly return surprises revise conditional volatility in opposite directions, and allowing for it lowers estimated persistence.'),
            ('arxiv', 'Bouchaud, Matacz & Potters', 2001, 'The leverage effect in financial markets: retarded volatility and market panic', 'https://arxiv.org/abs/cond-mat/0101120',
             'Measures the leverage effect and shows it is moderate and slow for individual stocks but much stronger and faster-decaying for indices.'),
            ('paper', 'Patton', 2011, 'Volatility forecast comparison using imperfect volatility proxies', 'https://doi.org/10.1016/j.jeconom.2010.03.034',
             'Derives which losses rank variance forecasts correctly under a noisy proxy such as squared returns; MSE and QLIKE belong to the robust family, which can be asymmetric and is unit-invariant when homogeneous.'),
            ('arxiv', 'Gneiting', 2009, 'Making and Evaluating Point Forecasts', 'https://arxiv.org/abs/0912.0902',
             'Shows that scoring functions must be consistent for the functional requested, with a GARCH(1,1) simulation in which common scores rank forecasters misleadingly.'),
        ],
    ),
    "3.20": (
        r"""Cedar's regression follows Fama and French's 1993 design, which keeps loadings and premiums apart. They regressed excess returns on 25 stock portfolios, July 1963 to December 1991 (342 months), on the market excess return and mimicking returns for size and book-to-market. The slopes are loadings with a clear reading as risk-factor sensitivities, and a well-specified model leaves intercepts indistinguishable from zero. Our reading: Cedar's .001 tests the factor set on that asset and is not evidence of skill by itself.

A traded factor's premium is its average return, and averages carry wide error bars. Fama and French report 0.43% a month for the market, only 1.76 standard errors from zero, 0.27% for size (t = 1.73) and 0.40% for value (t = 2.91). Their term and default factors averaged just 0.06% and 0.02% a month, yet their high volatility let them capture substantial common variation in bond and stock returns.

Estimating premiums across assets is harder. Lewellen and co-authors argue that high cross-sectional R² and small pricing errors on size and book-to-market portfolios can lend a model only weak support. Anatolyev and Mikusheva show that with weak factors and a growing number of assets, the conventional two-pass procedure, which estimates betas and then explains returns with them, gives inconsistent premia.

As an illustration, not a forecast, Cedar's loadings 1.1, .3 and −.2 times those three premiums give 0.474% a month (our arithmetic), against the 2.6% the factors contribute in the lesson's one-month scenario. The first uses estimated premiums, the second one realized factor draw.

Exercise: compute each factor's mean and t-statistic in your sample, then mark which of Cedar's loadings multiplies a premium you cannot tell from zero.""",
        [
            ('paper', 'Fama & French', 1993, 'Common risk factors in the returns on stocks and bonds', 'https://doi.org/10.1016/0304-405X%2893%2990023-5',
             'Time-series factor regressions on 25 size and book-to-market portfolios, with the average premiums and t-statistics of the market, size, value, term and default factors.'),
            ('paper', 'Lewellen, Nagel & Shanken', 2010, 'A skeptical appraisal of asset pricing tests', 'https://doi.org/10.1016/j.jfineco.2009.09.001',
             'Argues that a high cross-sectional R² and small pricing errors on size and book-to-market portfolios can give weak support for a factor model.'),
            ('arxiv', 'Anatolyev & Mikusheva', 2018, 'Factor models with many assets: strong factors, weak factors, and the two-pass procedure', 'https://arxiv.org/abs/1807.04094',
             'Shows that with weak factors and many assets the conventional two-pass estimator of risk premia is inconsistent, and proposes a sample-splitting remedy.'),
        ],
    ),
    "3.21": (
        r"""Four ways an intercept can mislead have documented cases.

Omitted factor. Carhart, with a sample free of survivor bias, found that common return factors and expenses almost completely explain persistence in mutual funds' mean and risk-adjusted returns. The "hot hands" result was mostly the one-year momentum effect, yet funds did not earn more by following momentum; the only significant unexplained persistence was strong underperformance by the worst funds. Our reading: in the lesson's attribution a momentum tilt would sit in the .4% residual, and a momentum factor would move it into a contribution.

Changing exposure. Ferson and Schadt conditioned expectations on public information variables, which proved statistically and economically significant, and found that conditioning makes their mutual funds' average performance look better. A fixed-loading alpha can therefore misstate performance when exposure moves with conditions (our reading).

Stale pricing. Getmansky and co-authors found hedge-fund returns often highly serially correlated, most likely because of illiquidity exposure. Reported returns are then smoother than true economic returns, which understates volatility and raises risk-adjusted measures such as the Sharpe ratio. Their 908 funds showed smoothing that varies by style. Our reading: the lesson's HAC error is the guard here, because a plain OLS error ignores that autocorrelation.

Selection. Harvey and Liu use a double bootstrap to set a t-statistic hurdle tied to a stated false discovery rate such as 5%, and report that current methods lack power to detect outperforming managers. Our reading: the hurdle rises with the number of funds screened.

Exercise: simulate batches of funds with zero true alpha and your own sample length, record the largest intercept t-statistic in each batch, and compare it with the lesson's 1.333.""",
        [
            ('paper', 'Carhart', 1997, 'On Persistence in Mutual Fund Performance', 'https://doi.org/10.1111/j.1540-6261.1997.tb03808.x',
             'Shows that common return factors and expenses almost completely explain fund-return persistence, with the hot-hands pattern mostly a momentum effect; the omitted-factor case for alpha.'),
            ('paper', 'Ferson & Schadt', 1996, 'Measuring Fund Strategy and Performance in Changing Economic Conditions', 'https://doi.org/10.1111/j.1540-6261.1996.tb02690.x',
             'Conditions fund performance measures on public information variables and finds that doing so changes the picture of average fund performance; the changing-exposure case.'),
            ('paper', 'Getmansky, Lo & Makarov', 2004, 'An econometric model of serial correlation and illiquidity in hedge fund returns', 'https://doi.org/10.1016/j.jfineco.2004.04.001',
             'Explains why illiquid holdings make reported hedge-fund returns smoother than true returns, understating volatility and flattering risk-adjusted measures; the stale-pricing case.'),
            ('arxiv', 'Harvey & Liu', 2020, 'False (and Missed) Discoveries in Financial Economics', 'https://arxiv.org/abs/2006.04269',
             'Calibrates false and missed discoveries in fund and factor selection with a double bootstrap and a false-discovery-rate t-statistic hurdle; the selection case.'),
        ],
    ),
    "3.3": (
        r"""Three studies measure what estimation error does to optimizers; the lesson's two assets show the mechanism. With volatilities of 20% and 10%, the unconstrained, fully invested minimum-variance weight on the riskier asset is about 10.5% at the lesson's correlation of .3. It reaches zero when correlation equals the volatility ratio, .5, then turns negative: −7.7% at .6, and −100% as correlation approaches 1, where the covariance matrix is singular (our arithmetic). A correlation estimate near .5 can therefore flip the answer from long to short.

DeMiguel and co-authors compared sample-based mean–variance optimization and its estimation-error remedies with equal weighting. Of 14 models across seven datasets, none was consistently better than 1/N in Sharpe ratio, certainty-equivalent return or turnover. Calibrated to US equities, their estimated window for those optimizers to beat 1/N was around 3000 months with 25 assets and about 6000 with 50.

Jagannathan and Ma explain why constraining weights to be nonnegative can reduce the risk of estimated optimal portfolios even when the constraints are wrong, and found that with the constraint in place the sample covariance matrix performed as well as factor-model, shrinkage and daily-data estimates. In the two-asset case the long-only constraint binds from .5 upward.

Pafka and Kondor give a counterweight. In their simulations, covariance noise displaced the solution of the classical problem, minimizing variance under linear constraints, by only about 5 to 15% measured in variance, yet under non-linear constraints such as margin accounts it caused serious instability. Our reading: the studies address different problems, so they need not conflict.

Exercise: recompute the two weights at correlations .45, .5 and .55, with and without the long-only constraint, and note where the constraint decides.""",
        [
            ('paper', 'DeMiguel, Garlappi & Uppal', 2009, 'Optimal Versus Naive Diversification: How Inefficient is the 1/N Portfolio Strategy?', 'https://doi.org/10.1093/rfs/hhm075',
             'Tests mean-variance optimizers and estimation-error remedies against equal weighting across seven datasets and gives the estimation windows needed for the optimizers to win.'),
            ('paper', 'Jagannathan & Ma', 2003, 'Risk Reduction in Large Portfolios: Why Imposing the Wrong Constraints Helps', 'https://doi.org/10.1111/1540-6261.00580',
             'Explains why no-short-sale constraints lower the risk of estimated optimal portfolios even when they are wrong; with them, the sample covariance matrix matches fancier estimators.'),
            ('arxiv', 'Pafka & Kondor', 2001, 'Noisy Covariance Matrices and Portfolio Optimization', 'https://arxiv.org/abs/cond-mat/0111503',
             'Simulations of how covariance noise displaces minimum-variance solutions: modest under linear constraints, serious instability under non-linear ones such as margin accounts.'),
        ],
    ),
    "3.22": (
        r"""Ledoit and Wolf explain why the sample covariance matrix misleads an optimizer. When stocks are numerous relative to the observations, its most extreme entries tend to be extreme because they contain extreme error, and the optimizer places its biggest bets on exactly those, a pattern Michaud named error maximization. Shrinkage pulls the extremes toward a structured target: a single-factor matrix in their earlier work, a constant-correlation matrix (sample variances, one average correlation) in their 2004 article. The best intensity is the one minimizing expected distance from the true matrix, and they derive a formula to estimate it. Re-estimating from the last 60 monthly returns for benchmarks of 30 to 500 stocks, over 239 out-of-sample months to December 2002, shrinkage beat the sample matrix on average information ratio in every scenario, and the sample matrix always had the highest turnover.

Our arithmetic on the lesson's matrix: its correlation is .018/(.2 × .1) = .9. With two assets a constant-correlation target equals the sample matrix, so that target matters only from three assets up; the lesson's 50% shrink toward a diagonal target cuts the correlation to .45.

On components, Plerou and co-authors used samples including 1000 US stocks (30-minute returns, 1994–95) and 422 stocks (daily returns, 1962–96). Most eigenvalues fell within the bounds for random correlation matrices. The largest reflected an influence common to all stocks, while the other deviating eigenvectors formed groups matching business sectors and were stable in time. Our reading: the labels come from inspecting loadings, not from the algorithm.

Exercise: on a 60-month window of your data, shrink toward both targets and compare each minimum-variance portfolio's realized variance over the next year with equal weighting.""",
        [
            ('paper', 'Ledoit & Wolf', 2004, 'Honey, I Shrunk the Sample Covariance Matrix', 'https://doi.org/10.3905/jpm.2004.110',
             'Explains why sample covariance errors mislead optimizers, describes the constant-correlation shrinkage target, and tests it out of sample against the sample matrix and rivals.'),
            ('arxiv', 'Plerou et al.', 2001, 'A Random Matrix Approach to Cross-Correlations in Financial Data', 'https://arxiv.org/abs/cond-mat/0108023',
             'Compares eigenvalues of stock correlation matrices with a random-matrix null; the largest eigenvector is a common influence and the others match sectors and stay stable.'),
        ],
    ),
    "3.23": (
        r"""Petersen explains why panels need care: residuals can be correlated across firms and across time, so OLS standard errors can be biased, and corporate finance relied on Rogers (clustered) errors while asset pricing used the Fama–MacBeth procedure. His posted test data, where the regressor and the residual both carry a firm effect but no year effect, show the stakes. The OLS slope is 1.0348 with a standard error of 0.0286 (t = 36.20). Clustering by firm gives 0.0506 (t = 20.45), so the OLS error is about 43% below it (our arithmetic). Clustering by year gives 0.0334, firm and year together 0.0536, and Fama–MacBeth 0.0333. Our reading is that Fama–MacBeth lands beside the year-clustered value because it handles dependence within a period, not a persistent firm effect.

Cameron and Miller add that default errors can greatly overstate precision when errors correlate within clusters, that with many clusters inference should use cluster-robust errors, and that fixed effects, few clusters and multiway clustering complicate matters. Abadie and co-authors say clustering can be needed when clusters are sampled from a population of clusters or when treatment assignment is correlated with cluster membership, and propose estimators for intermediate cases where conventional cluster errors are too conservative and robust errors too small.

In the lesson's panel the within regression fits all four points exactly, so every standard error is zero. Even with noisy data, two clusters would leave a t distribution with one degree of freedom, which needs |t| > 12.71 at 5% (our arithmetic).

Exercise: reproduce 0.0506 from Petersen's test data, then say whether your question concerns within-firm change or cross-firm difference.""",
        [
            ('paper', 'Petersen', 2009, 'Estimating Standard Errors in Finance Panel Data Sets: Comparing Approaches', 'https://doi.org/10.1093/rfs/hhn053',
             "Explains when OLS, clustered and Fama-MacBeth standard errors agree or diverge in finance panels; the author's posted test data give worked standard errors under each method."),
            ('paper', 'Cameron & Miller', 2015, "A Practitioner's Guide to Cluster-Robust Inference", 'https://doi.org/10.3368/jhr.50.2.317',
             'Practical guide to cluster-robust inference and its complications: cluster-specific fixed effects, few clusters and multiway clustering.'),
            ('arxiv', 'Abadie, Athey, Imbens & Wooldridge', 2017, 'When Should You Adjust Standard Errors for Clustering?', 'https://arxiv.org/abs/1710.02926',
             'Argues that clustering should follow how clusters were sampled and how treatment was assigned, and proposes estimators for the cases between conventional clustering and robust errors.'),
        ],
    ),
    "3.24": (
        r"""The lesson's slope of 2 is only as trustworthy as its denominator. Stock and co-authors explain that weak identification leaves GMM statistics with nonnormal distributions even in large samples, so conventional IV inference misleads. A common screen is a first-stage F above 10. Lee and co-authors show that, in the single-instrument model, passing that screen still leaves the usual t-test anti-conservative: a true 5 percent test needs F above 104.7, and keeping 10 as the cutoff means replacing the critical value 1.96 with 3.43. They re-examined 57 AER papers and found that corrected inference turned half of the initially significant results insignificant. Their tF procedure instead supplies critical values that depend on the observed F, so 104.7 is a cutoff for the unadjusted t-test, not a universal threshold.

Convert the lesson's covariances into F under assumptions of our own: unit-variance z and x, and 400 observations. A covariance of .3 gives F ≈ 39, above 10 but below 104.7. A covariance of .03 gives F ≈ 0.36, so the slope of 20 rests on a first stage that cannot be told from zero. At .3, F would reach 104.7 only with about 1,060 observations.

Andrews and co-authors note that much weak-instrument theory assumed independent, homoskedastic data, and they review results for heteroskedastic, serially correlated or clustered data, which return panels often are (our gloss). Their tabulations and simulations, based on AER papers that use IV between 2014 and 2018, suggest that weak instruments remain an important issue for practice.

Exercise: compute the first-stage F with the covariance estimator you will use for the IV standard errors, then name the F-dependent critical value or robust confidence set you will report.""",
        [
            ('arxiv', 'Lee, McCrary, Moreira & Porter', 2020, 'Valid t-ratio Inference for IV', 'https://arxiv.org/abs/2010.05058',
             'For the single-instrument model, shows that the first-stage F above 10 rule leaves the t-test anti-conservative, gives the F and critical-value numbers for a true 5 percent test, and proposes the tF procedure.'),
            ('paper', 'Andrews, Stock & Sun', 2019, 'Weak Instruments in Instrumental Variables Regression: Theory and Practice', 'https://doi.org/10.1146/annurev-economics-080218-025643',
             'Review of weak-instrument methods with an emphasis on heteroskedastic, serially correlated or clustered data, plus a survey of IV papers in the American Economic Review.'),
            ('paper', 'Stock, Wright & Yogo', 2002, 'A Survey of Weak Instruments and Weak Identification in Generalized Method of Moments', 'https://doi.org/10.1198/073500102288618658',
             'Explains why weak identification makes conventional IV and GMM inference misleading even in large samples, and that procedures exist to detect and handle it.'),
        ],
    ),
    "3.25": (
        r"""The lesson's contrast of 2 uses a single adoption date. With staggered adoption, de Chaisemartin and D'Haultfœuille showed that a regression with period and group fixed effects estimates a weighted sum of group-by-period average treatment effects, with weights that may be negative, so the coefficient can be negative while every effect is positive.

A tiny panel of our own shows how. An early adopter is treated from period 2 and a late adopter in period 3, with no never-treated unit. The early adopter's effect is 1, then 4; the late adopter's effect is 1. The average treated-cell effect is 2, yet the fixed-effects regression returns −0.5. The weights on the three treated cells are 1, −0.5 and 0.5. Our reading: in period 3 the late adopter is compared with an early adopter whose effect is still growing, and that growth is subtracted.

Baker and co-authors argue that such biases are likely to matter for a large portion of finance, accounting and law research that relies on staggered timing, and that they can produce Type I and Type II errors. When they re-examined published results with alternative estimators, the causal estimates or inferences in many cases differed substantially.

Pre-trend checks need caution as well. Roth shows that conventional pre-trend tests may have low power, and that conditioning the analysis on the result of a pretest can distort estimation and inference, potentially worsening bias and the under-coverage of confidence intervals.

Exercise: list every two-group comparison in your design, flag those whose comparison group was already treated, and compare the regression with an estimator that avoids them.""",
        [
            ('arxiv', "de Chaisemartin & D'Haultfœuille", 2018, 'Two-way fixed effects estimators with heterogeneous treatment effects', 'https://arxiv.org/abs/1803.08807',
             'Shows that period-and-group fixed-effects regressions weight group-by-period effects, possibly negatively, so the coefficient can be negative while all effects are positive; the basis for the tiny staggered panel.'),
            ('paper', 'Baker, Larcker & Wang', 2022, 'How much should we trust staggered difference-in-differences estimates?', 'https://doi.org/10.1016/j.jfineco.2022.01.004',
             'Explains when staggered DiD estimators are biased, argues the problem is widespread in finance, accounting and law, and re-examines published results with three alternative estimators.'),
            ('paper', 'Roth', 2022, 'Pretest with Caution: Event-Study Estimates after Testing for Parallel Trends', 'https://doi.org/10.1257/aeri.20210236',
             'Shows that pre-trend tests may have low power and that conditioning on their result can distort estimation and inference; adds practical recommendations.'),
        ],
    ),
    "3.26": (
        r"""Shumway argued that single-period models of bankruptcy are inconsistent while hazard models produce consistent estimates, and he described a simple way to fit a discrete-time hazard model. About half of the accounting ratios used in earlier models were not statistically significant, while market size, past stock returns and idiosyncratic return variability were strongly related to bankruptcy, and a model using both kinds of variables forecast out of sample more accurately than the alternatives. Our inference: when an entity can fail in any period, the at-risk window belongs in the model, not only in the label.

Gneiting and Raftery call a scoring rule proper if a forecaster maximizes the expected score by issuing the true distribution, and strictly proper if that maximum is unique; the logarithmic and quadratic scores are among their examples (for yes/no events the quadratic score is the Brier score, our gloss). If the true chance is .75, a forecast of .75 has expected Brier loss .1875, against .21 for .9 and .2451 for .99 (our arithmetic). Accuracy at a .5 cutoff cannot tell these forecasts apart.

Dimitriadis and co-authors call a probability forecast calibrated when predicted probabilities are matched by observed frequencies. They note that classical binned reliability diagrams are unstable under ad hoc implementation choices, and propose CORP diagrams built on isotonic regression, with uncertainty quantification by resampling or asymptotic theory. With 200 forecasts of .75, the observed frequency has a standard error near .031 (our arithmetic), so a realized .70 is only about 1.6 standard errors low.

Exercise: score a forecast set with log and Brier loss, draw an isotonic reliability curve, and attach an interval before calling the model calibrated.""",
        [
            ('paper', 'Shumway', 2001, 'Forecasting Bankruptcy More Accurately: A Simple Hazard Model', 'https://doi.org/10.1086/209665',
             'Argues that hazard models suit bankruptcy forecasting better than single-period models, and shows market variables beside accounting ratios improve out-of-sample forecasts; an example of an event defined over time at risk.'),
            ('paper', 'Gneiting & Raftery', 2007, 'Strictly Proper Scoring Rules, Prediction, and Estimation', 'https://doi.org/10.1198/016214506000001437',
             'Defines proper and strictly proper scoring rules and reviews the logarithmic and quadratic scores; the theory behind scoring probability forecasts honestly.'),
            ('arxiv', 'Dimitriadis, Gneiting & Jordan', 2020, 'Evaluating probabilistic classifiers: Reliability diagrams and score decompositions revisited', 'https://arxiv.org/abs/2008.03033',
             'Introduces CORP reliability diagrams based on isotonic regression, with uncertainty quantification and a Brier score decomposition; a stable way to check calibration.'),
        ],
    ),
    "3.4": (
        r"""Acerbi and Tasche note that most definitions of expected shortfall agree for continuous loss distributions but can differ when the distribution has discontinuities, as a finite sample's does (our gloss). They define it as the average loss over the worst 100α% of cases, with fractional weight on a boundary observation (our reading), and they report that the tail conditional expectation, though easy to apply, is not coherent. For the lesson's ten losses at the 90% level, expected shortfall is 20, while conditioning on losses at or beyond the VaR of 9 gives 14.5. At 85% the two are 16.33 and 14.5, and the strictly-above rule still gives 20. Expected shortfall is continuous in the level, so it moves smoothly while the simple rules jump (our arithmetic).

Christoffersen observed that most work on interval forecasts implicitly assumed homoskedastic errors and tested only unconditional coverage, and he built a framework for conditional evaluation, which matters when higher-order moment dynamics are present. Two VaR models can each record three exceedances in 250 days, one spread across the year and one on consecutive days. The counts match, but only the second shows exceedances followed by exceedances (our illustration).

Magdon-Ismail and co-authors show that the expected maximum drawdown of a Brownian motion with drift behaves, as the horizon grows, logarithmically for positive drift, like a square root for zero drift and linearly for negative drift. If log equity behaves like such a motion (our mapping), quadrupling a driftless history roughly doubles the drawdown in log points (our inference).

Exercise: compute expected shortfall at 90%, 85% and 80% for the ten losses under all three conventions, then compare maximum drawdown over one-year and full-sample windows.""",
        [
            ('arxiv', 'Acerbi & Tasche', 2001, 'On the coherence of Expected Shortfall', 'https://arxiv.org/abs/cond-mat/0104295',
             "Compares definitions of expected shortfall, shows they differ for distributions with discontinuities, and identifies the average of the worst cases as the coherent one; the basis for the lesson's 14.5 versus 20."),
            ('paper', 'Christoffersen', 1998, 'Evaluating Interval Forecasts', 'https://doi.org/10.2307/2527341',
             'Argues that interval forecasts, such as VaR, need conditional evaluation beyond unconditional coverage when higher-order moment dynamics are present; applied to exchange-rate risk-management forecasts.'),
            ('paper', 'Magdon-Ismail, Atiya, Pratap & Abu-Mostafa', 2004, 'On the maximum drawdown of a Brownian motion', 'https://doi.org/10.1239/jap/1077134674',
             'Derives the distribution and expected value of maximum drawdown for Brownian motion with drift, with logarithmic, square-root or linear growth in the horizon depending on the drift.'),
        ],
    ),
    "3.27": (
        r"""The lesson's blocks of three follow Künsch's block bootstrap, which selects blocks of length l at random with replacement and obtains consistency when, among other conditions, l grows with n while l/n shrinks to zero. Counting shows the trade-off. With 12 observations, overlapping blocks of 3 allow 10 starting points and 10,000 possible four-block resamples, blocks of 6 allow only 49, and a block of 12 allows exactly one (our arithmetic).

Politis and Romano resample blocks of random, geometrically distributed length, which makes the resampled series stationary given the data, as fixed-length blocks do not. A mean length of 3 means each draw begins a new block with probability 1/3 (our arithmetic).

Nordman and Lahiri compare block-length selectors for the moving-block bootstrap. Two general methods reach convergence rates of n^(−1/6) and n^(−2/7), and the best possible rate for variance estimation, n^(−1/3), belongs to a method of Politis and White. Our inference: estimated lengths stay noisy, so report results at several.

Ledoit and Wolf show that the Jobson–Korkie Sharpe-ratio test, as corrected by Memmel, is not valid when returns have heavier tails than the normal or are of time series nature. They propose a studentized time series bootstrap interval for the difference of Sharpe ratios, resampling the observed data rather than null-restricted data.

Exercise: bootstrap a Sharpe-ratio difference with mean block lengths 3, 6 and 12, and report how the interval moves.""",
        [
            ('paper', 'Künsch', 1989, 'The Jackknife and the Bootstrap for General Stationary Observations', 'https://doi.org/10.1214/aos/1176347265',
             "Extends the jackknife and bootstrap to stationary sequences by resampling blocks of length l, with consistency when l grows with n but l/n shrinks to zero; the origin of the lesson's block bootstrap."),
            ('paper', 'Politis & Romano', 1994, 'The Stationary Bootstrap', 'https://doi.org/10.1080/01621459.1994.10476870',
             'Introduces resampling of blocks with geometrically distributed random length so the resampled pseudo-series is stationary; the alternative to fixed blocks.'),
            ('arxiv', 'Nordman & Lahiri', 2014, 'Convergence rates of empirical block length selectors for block bootstrap', 'https://arxiv.org/abs/1403.3275',
             'Compares methods for choosing the block length of the moving-block bootstrap and gives their convergence rates, so block length is itself an estimate with error.'),
            ('paper', 'Ledoit & Wolf', 2008, 'Robust performance hypothesis testing with the Sharpe ratio', 'https://doi.org/10.1016/j.jempfin.2008.03.002',
             'Shows the standard Sharpe-ratio difference test fails for heavy tails or time series data, and proposes a studentized time series bootstrap interval instead.'),
        ],
    ),
    "3.28": (
        r"""Romano and Wolf formalize the lesson's family of attempts: several strategies are compared with one benchmark, and the task is deciding which hypotheses to reject. Their stepwise procedure asymptotically controls the familywise error rate, is more powerful than related single-step methods, and implicitly captures the joint dependence structure of the test statistics, which raises the ability to detect false hypotheses. Our inference: when strategy variants overlap heavily, the honest cutoff for the best of twenty lies between .05 and Bonferroni's .0025, and only resampling the whole family shows where.

Benjamini and Yekutieli studied the other error rate. The Benjamini–Hochberg procedure was shown to be much more powerful than comparable familywise procedures; they proved it controls the false discovery rate under positive regression dependency on the true nulls, with a conservative modification for any other dependence. It compares each ordered p-value with its rank times q/m. Our arithmetic with the lesson's numbers: the cutoffs are .0025 at rank 1, equal to Bonferroni's, then .005, .0075 and .01 at rank 4. A smallest p-value of .01 is rejected only if enough other p-values are small for some rank of 4 or higher to meet its own cutoff.

Chen supplies a dissent about hurdles themselves. Calls to raise t-statistic hurdles may be hard to justify empirically: published data are biased because results that miss existing hurdles are often unobserved, so a revised hurdle rests on extrapolation and is weakly identified, whereas the false discovery rate and empirical Bayes shrinkage target published findings and can be strongly identified. Our reading: every threshold depends on the count of attempts behind it, which is the ledger's job.

Exercise: simulate twenty zero-alpha strategies sharing one common factor, record the largest absolute t-statistic in each of many runs, and compare its 95th percentile with the Bonferroni cutoff of about 3.02.""",
        [
            ('paper', 'Romano & Wolf', 2005, 'Stepwise Multiple Testing as Formalized Data Snooping', 'https://doi.org/10.1111/j.1468-0262.2005.00615.x',
             'Stepwise procedure that controls the familywise error rate while capturing the dependence among test statistics, presented for comparing several strategies with a common benchmark.'),
            ('paper', 'Benjamini & Yekutieli', 2001, 'The control of the false discovery rate in multiple testing under dependency', 'https://doi.org/10.1214/aos/1013699998',
             'Shows that the Benjamini-Hochberg false-discovery-rate procedure remains valid under positive regression dependency and gives a conservative modification for any other dependence.'),
            ('arxiv', 'Chen', 2022, 'Do t-Statistic Hurdles Need to be Raised?', 'https://arxiv.org/abs/2204.10275',
             'Argues that revised t-statistic hurdles are weakly identified because unpublished results are unobserved, while false-discovery-rate and empirical-Bayes statistics on published findings are strongly identified.'),
        ],
    ),
    "3.5": (
        r"""Arnott and co-authors turn the lesson's record into a protocol. Keep track of what is tried: among twenty randomly selected strategies, one will likely exceed the two-sigma threshold (a t-statistic of 2.0) by chance, so 2.0 means little once several are tested, and correlation matters because twenty strategies with near 1.0 correlation amount to one. A data transformation such as volatility scaling counts as an extra variable; the best of ten tried is a red flag. Researchers know the history, so out-of-sample data are rarely clean, and a model repaired after failing out of sample is overfit. Costs and implementation shortfall belong in both samples, since even modest costs make the significance of many published anomalies essentially vanish.

Novy-Marx and Velikov measured the cost side. Most anomalies with less than 50% turnover per month still show significant net spreads when built to mitigate costs, for example with a buy/hold spread that asks more to open a position than to keep it; few with higher turnover do. Costs always reduce profitability, which heightens data-snooping concerns. Our arithmetic on the lesson: 8% gross at 20 bps per one-way turnover breaks even at 8 ÷ .2 = 40 turnovers, and the twenty-turnover case earns nothing net at 40 bps.

Kapoor and Narayanan show how leakage survives review. Across 17 fields they found leakage affecting 329 papers, built a taxonomy of 8 types, and proposed model info sheets; in a civil-war-prediction replication, every paper claiming that complex models beat logistic regression failed to reproduce because of leakage. Our reading: the lesson's close signal filled at the open is such a leak, and a record stating when each input became known catches it.

Exercise: for one backtest, list every variant tried and each input's availability timestamp, then recompute net return at the lesson's cost and at double it.""",
        [
            ('paper', 'Arnott, Harvey & Markowitz', 2019, 'A Backtesting Protocol in the Era of Machine Learning', 'https://doi.org/10.3905/jfds.2019.1.064',
             'Research protocol for quantitative finance: keep track of every strategy tried and their correlations, document data transformations, treat out-of-sample data with suspicion, and include trading costs in both samples.'),
            ('paper', 'Novy-Marx & Velikov', 2016, 'A Taxonomy of Anomalies and Their Trading Costs', 'https://doi.org/10.1093/rfs/hhv063',
             'After-cost performance of anomalies by turnover, with a buy/hold spread as the most effective cost-mitigation technique and the observation that costs sharpen data-snooping concerns.'),
            ('arxiv', 'Kapoor & Narayanan', 2022, 'Leakage and the Reproducibility Crisis in ML-based Science', 'https://arxiv.org/abs/2207.07048',
             'Survey of data leakage across fields, a taxonomy of leakage types, and model info sheets that let readers check a claim for leaks.'),
        ],
    ),
    "3.29": (
        r"""Morris and co-authors give the lesson's simulation diagnostic a structure. A simulation study is a computer experiment in which the truth is known, so properties such as bias can be judged, yet such studies are often poorly designed, analysed and reported; they propose stating the aims, data-generating mechanisms, estimands, methods and performance measures (ADEMP). Coverage is estimated from repetitions, so it carries Monte Carlo error: if the required standard error for a coverage of 95% is 0.5%, they compute 1,900 repetitions. They also advise recording the random-number generator's end state so more repetitions can be added later. One seeded run is a single repetition.

Newey and West proposed a nonparametric rule for the number of autocovariances in a HAC matrix, asymptotically equivalent to the choice that is optimal under mean-squared-error loss; their simulations suggested it performs tolerably well but still leaves size distortions. Our reading: a rule fixed in advance beats choosing the lag that delivers significance, yet it does not make intervals exact.

Hou and co-authors show how conventions decide a replication. With microcaps mitigated through NYSE breakpoints and value-weighted returns, 65% of 452 anomalies fail the single-test hurdle of 1.96, 82% fail the multiple-test hurdle of 2.78, and economic magnitudes are much smaller than originally reported.

Check on the project's data: its generator pairs serially independent factors with an autocorrelated disturbance, so for the two slopes classical and HAC errors should nearly agree while the intercept's should differ, and even HAC intervals for the intercept may undercover (our inference, echoing the size-distortion warning). Rerun the factor routine over 1,000 seeds, recording each coefficient's error against the planted value and the share of classical and of HAC 95% intervals that cover it. At 95% coverage the Monte Carlo error of each share is about √(.95 × .05/1,000) ≈ .007.""",
        [
            ('arxiv', 'Morris, White & Crowther', 2017, 'Using simulation studies to evaluate statistical methods', 'https://arxiv.org/abs/1712.03198',
             'Tutorial on designing and reporting simulation studies (ADEMP), with guidance on bias, coverage, Monte Carlo error, the number of repetitions and recording the random-number state.'),
            ('paper', 'Newey & West', 1994, 'Automatic Lag Selection in Covariance Matrix Estimation', 'https://doi.org/10.2307/2297912',
             'Nonparametric rule for choosing the number of autocovariances in a HAC covariance matrix, with simulations showing acceptable performance but remaining size distortions.'),
            ('paper', 'Hou, Xue & Zhang', 2020, 'Replicating Anomalies', 'https://doi.org/10.1093/rfs/hhy131',
             'Large replication of anomalies with microcaps mitigated; most fail the single-test and multiple-test t-statistic hurdles and the survivors have much smaller economic magnitudes.'),
        ],
    ),
    "3.30": (
        r"""Stock and Watson address inference on a long-run slope. Their efficient estimators of cointegrating vectors, computed by GLS or OLS, give Wald statistics with asymptotic chi-squared distributions; the lab reports its plain levels slope with no interval, and our inference is that a defensible interval needs an estimator of this kind. Applied to U.S. M1 demand, they found a relation stable over 1900–1989, with a 95 percent interval of (0.88, 1.06) for the income elasticity, while postwar data alone gave unstable estimates and substantial sampling uncertainty. Our reading: an early-late slope gap shows a break only if each half carries its own interval.

Gregory and Hansen tested the null of no cointegration against cointegration with a single break of unknown timing in the intercept and/or slope. In their limited experiments their tests detected cointegration despite a break, while the power of the conventional ADF test, with no allowance for regime shifts, fell sharply. The lesson's permanent shift is this design; our inference is that on broken data a failure to reject says little about whether a relation once existed.

Reichold adds a finite-sample warning: compared with popular residual-based tests, a variance-ratio test is less prone to size distortions, asymptotic power is not a useful indicator of finite-sample power, and ADF-type tests show power reversal problems.

Check on the project's data: using the lab's generator and test settings, run many seeds under three designs, namely independent random walks, the planted 1.5 relation, and a mid-sample slope change, and report the share of rejections at the 5% level for each. The first share estimates size and the others power. Our inference: the broken design rejects far less often than the planted one, and its full-sample slope lands between the two halves' slopes.""",
        [
            ('paper', 'Stock & Watson', 1993, 'A Simple Estimator of Cointegrating Vectors in Higher Order Integrated Systems', 'https://doi.org/10.2307/2951763',
             'Efficient cointegrating-vector estimators with chi-squared Wald tests, applied to long-run U.S. money demand: a stable relation over 1900-1989 but unstable, imprecise estimates from postwar data alone.'),
            ('paper', 'Gregory & Hansen', 1996, 'Residual-based tests for cointegration in models with regime shifts', 'https://doi.org/10.1016/0304-4076%2869%2941685-7',
             'Residual-based cointegration tests that allow one break of unknown timing; the conventional ADF test loses power sharply when the relation shifts.'),
            ('arxiv', 'Reichold', 2022, 'A Residuals-Based Nonparametric Variance Ratio Test for Cointegration', 'https://arxiv.org/abs/2211.06288',
             'Compares residual-based no-cointegration tests in finite samples, covering size distortions, size-corrected power and the power reversal of ADF-type tests.'),
        ],
    ),
    "3.31": (
        r"""Bun and co-authors show how estimation error enters an allocation. With N assets and T observations, let q = N/T. In their Markowitz application the ratio of out-of-sample risk to the true optimum is close to one when q is small, but for a wide class of processes it equals 1/(1−q) and diverges as q approaches 1. Their rotationally invariant estimators, which assume no prior structure, proved superior to all previously proposed methods in their financial application. Our arithmetic: their typical 500 stocks with 2,500 daily observations give q = .2, a factor of 1.25; 30 assets on 60 monthly returns would give q = .5, roughly a factor of 2.

Forbes and Rigobon explain why a correlation measured in a crisis window needs care: correlation coefficients are conditional on market volatility, so heteroskedasticity biases correlation-based contagion tests, and after adjusting they found virtually no rise in unconditional correlations in 1997, 1994 and 1987. Our reading: the lesson's correlation of 1 is a bound, not an estimate.

The 2026 interagency guidance on model risk (Federal Reserve SR 26-2, which replaced SR 11-7) calls models simplified representations whose assumptions create limitations, warns that even a sound model can carry high risk if misapplied, and asks validation to document modeling choices and data selection and to compare outputs with outcomes. It is written for banks and is not enforceable, so here it is a template for the memo.

Check on the project's numbers: the half-shrunk matrix has eigenvalues of about .092 and .038, but the stress matrix has .13 and 0, so it is a boundary rather than an input an optimizer can invert. For the stipulated recursion, the next variance .086 sits below the long-run level .01/(1 − .9) = .1, and its square root, about .29, is the figure in return units.""",
        [
            ('arxiv', 'Bun, Bouchaud & Potters', 2016, 'Cleaning large correlation matrices: tools from random matrix theory', 'https://arxiv.org/abs/1610.08104',
             'Review of random-matrix estimators of large covariance matrices, including how sample-matrix portfolios understate out-of-sample risk by a factor tied to N/T and an empirical comparison of cleaning methods.'),
            ('paper', 'Forbes & Rigobon', 2002, 'No Contagion, Only Interdependence: Measuring Stock Market Comovements', 'https://doi.org/10.1111/0022-1082.00494',
             'Shows that correlation coefficients depend on market volatility, biasing crisis-period contagion tests, and finds little rise in adjusted correlations in three crises.'),
            ('official', 'Federal Reserve, FDIC & OCC', 2026, 'Supervisory Guidance on Model Risk Management', 'https://www.federalreserve.gov/supervisionreg/srletters/SR2602.pdf',
             'Interagency guidance (SR 26-2, replacing SR 11-7) on model limitations, misuse, validation, alternative assumptions, outcomes analysis and documentation; written for banks, not a requirement here.'),
        ],
    ),
    "3.32": (
        r"""Campbell and Thompson's out-of-sample R² is the lesson's formula: one minus the ratio of squared forecast errors, where the model is a regression estimated through the previous period and the baseline is the historical average estimated through that same date. Goyal and Welch had argued that the historical average beats predictive regressions; Campbell and Thompson answered that many regressions win once weak restrictions are placed on coefficient signs and forecasts, with out-of-sample explanatory power small but economically meaningful for mean-variance investors. Our reading: if Cedar's 20% gain relies on realized factor returns, as the project's does, it is a conditional explanation on a different scale from a forecasting R², so the two should never share a table without labels.

Harvey warns that higher thresholds may be necessary but not sufficient: if an effect is rare, even t > 3 yields many false positives. He offers the minimum Bayes factor, a function of the p-value combined with prior odds, and notes that the threshold depends on economic plausibility. Cedar's t = .4/.25 = 1.6 (p ≈ .11) falls well short of 3, so the selection history decides how much weight it deserves.

Wilson and co-authors list practices that make a dossier rerunnable: save the raw data, record every processing step in scripts because otherwise no one can repeat the analysis, and provide a simple example that gives a known correct output for a simple known input. The earlier project's three-point regression, with intercept 1 and slope 2, is such an example.

Check: from a clean environment, recompute .4 ± 1.96 × .25 = (−.09, .89), t = 1.6 and 1 − .8/1 = .2, and confirm the three-point fit still returns intercept 1 and slope 2 before trusting any larger output.""",
        [
            ('paper', 'Campbell & Thompson', 2008, 'Predicting Excess Stock Returns Out of Sample: Can Anything Beat the Historical Average?', 'https://doi.org/10.1093/rfs/hhm055',
             'Defines the out-of-sample R² against the historical average, answers Goyal and Welch with sign restrictions, and argues that small out-of-sample explanatory power can still be economically meaningful.'),
            ('paper', 'Harvey', 2017, 'Presidential Address: The Scientific Outlook in Financial Economics', 'https://doi.org/10.1111/jofi.12530',
             'Explains p-hacking, why higher t-statistic thresholds may not suffice, the minimum Bayes factor, and guidelines for a robust, transparent research culture.'),
            ('arxiv', 'Wilson et al.', 2016, 'Good Enough Practices in Scientific Computing', 'https://arxiv.org/abs/1609.00037',
             'Practical rules for data management, scripted processing steps and small test cases that let someone else rerun an analysis.'),
        ],
    ),
}
