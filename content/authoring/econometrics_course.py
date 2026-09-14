"""Original, complete applied financial econometrics course; fictional worked data."""

from applied_courses import checkpoints_for, study
from book_courses import finish

REG = (
    "statsmodels contributors · Linear regression",
    "https://www.statsmodels.org/stable/regression.html",
)
DIAG = (
    "statsmodels contributors · Regression diagnostics",
    "https://www.statsmodels.org/stable/diagnostic.html",
)
TIME = (
    "statsmodels contributors · Time-series methods",
    "https://www.statsmodels.org/stable/tsa.html",
)
COINT = (
    "statsmodels contributors · Engle–Granger cointegration test",
    "https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.coint.html",
)
VOL = (
    "arch contributors · Conditional volatility models",
    "https://arch.readthedocs.io/en/latest/univariate/univariate_volatility_modeling.html",
)
FACTORS = (
    "Kenneth R. French · Factor construction and Data Library",
    "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html",
)
PANEL = (
    "linearmodels contributors · Panel model examples",
    "https://bashtage.github.io/linearmodels/panel/examples/examples.html",
)
IV = (
    "linearmodels contributors · Instrumental variables",
    "https://bashtage.github.io/linearmodels/iv/introduction.html",
)
MULTI = (
    "statsmodels contributors · Multiple-testing procedures",
    "https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html",
)


def build_econometrics():
    modules = []

    def add(*args):
        modules.append(study(*args))

    add(
        "3.6",
        1,
        "An econometric question and its estimand",
        "Separate description, prediction, and causal explanation before choosing a regression.",
        "An estimand is the quantity the analysis aims to learn. Average association between a factor and a return, a forecast of next month's return, and the effect of changing a policy are different targets. They may use similar regression syntax while requiring different evidence. Begin with the population, observation unit, horizon, outcome, conditioning information, and decision the result will inform.\n\nA coefficient belongs to a specified model and sample. Its meaning changes when controls, weights, transformations, or eligible observations change. Write the equation and identify which terms are observed, estimated, and assumed. The fictional Cedar research team will use this discipline throughout the course.",
        "Cedar compares monthly excess returns with a market factor. A fitted slope of 1.2 means that a one-percentage-point increase in the factor is associated with 1.2 percentage points more return, conditional on the model's other terms. It does not say an investor can cause that gain by choosing the factor's value. A 0.1-percentage-point intercept is a model residual mean component, not a guaranteed premium.\n\nFor a factor value of 2 percentage points, the fitted conditional mean is 0.1+1.2×2=2.5 percentage points. A realized outcome can differ because of the residual and parameter uncertainty.",
        "Write a research charter before viewing the final outcome sample: question, target population, units, as-of dates, estimator, identifying assumptions, and falsification checks. Record both the result and the strongest alternative explanation. Distinguish uncertainty about a coefficient from uncertainty about a future observation. Use a predictive metric for a forecast and an identification argument for a causal claim; neither can substitute for the other.",
        r"y_t=\alpha+\beta x_t+u_t",
        'print("Fitted return (percentage points):", 0.1 + 1.2 * 2)',
        "Define an estimand for whether a quality factor predicts next-month excess returns. State a separate causal question that the same predictive regression cannot automatically answer.",
        "Specify the eligible universe, monthly horizon, dated quality measure, and out-of-sample forecast loss. Whether changing a firm's quality causes its return requires an identification design addressing selection and confounding.",
        [
            (
                "A fitted association automatically establishes causality:",
                ["Yes", "No", "Only with a high R-squared"],
                1,
                "Causal interpretation requires additional identifying assumptions.",
            ),
            (
                "A forecast should be evaluated using:",
                [
                    "Only its coefficient's sign",
                    "Only its training fit",
                    "A declared future prediction task and loss",
                ],
                2,
                "The target and held-out loss determine forecast usefulness.",
            ),
            (
                "Intercept .2 and slope .8 with factor value 3 imply fitted outcome:",
                ["2.6", "3.8", ".24"],
                0,
                ".2+.8×3 = 2.6 in the declared units.",
            ),
            (
                "Changing the eligible universe can change a coefficient because:",
                [
                    "Coefficients are universal constants",
                    "The estimand and sample relationship may change",
                    "Units no longer matter",
                ],
                1,
                "A model estimate describes a specified population and conditioning set.",
            ),
        ],
        [REG],
    )

    add(
        "3.7",
        1,
        "Build a dated return and factor dataset",
        "Align returns, risk-free rates, publication dates, corporate actions, and missing observations without using future information.",
        "A financial dataset needs economic meaning as well as a rectangular shape. Identify simple versus log returns, percentage points versus decimals, raw versus adjusted prices, total-return treatment, currency, and observation frequency. Match a monthly asset return to the same month's factor and risk-free return. Annual rates cannot be subtracted directly from monthly returns.\n\nFundamental values need publication dates and revision identities. A December balance sheet released in March cannot enter a February information set. Distinguish missing observations, exchange closures, suspended trading, and genuine zero returns. Forward-filling a factor is a modeling decision, not neutral cleaning.",
        "A stock's monthly total return is 2.4% and the corresponding monthly risk-free return is 0.3%. Excess return is 2.1%, or 0.021 in decimal units. If factor data report 1.5 in percentage points, normalize it to 0.015 before combining it with decimal-return columns. A thousandfold or hundredfold scale mistake can leave an apparently plausible table of coefficients.\n\nOf 120 candidate dates, ten lack an eligible factor value and five different dates lack the asset return. A declared complete-case join retains 105 rows. Explain which observations disappear and whether their missingness is related to distress or liquidity.",
        "Keep a schema with column definitions, source versions, adjustment conventions, and availability rules. Audit duplicate timestamps and many-to-many joins before estimation. Compare the retained sample with the intended population, including delisted names. Use a small alignment fixture with a delayed filing and a missing factor; its expected result should be known before running the import. The course uses synthetic or explicitly supplied observations, never silently substituted historical data.",
        r"r^{excess}_t=r^{asset}_t-r^{free}_t",
        'print("Decimal excess return:", 0.024 - 0.003)\nprint("Normalized factor:", 1.5 / 100)\nprint("Complete rows:", 120 - 10 - 5)',
        "Create a data dictionary and alignment audit for monthly excess returns. Normalize an asset return of 1.8% and risk-free return of 0.2%, and explain how to treat a later amended filing.",
        "Excess return is 0.016. Preserve amendment availability separately and use only the version available at each decision date. Log missing rows instead of inventing zero returns.",
        [
            (
                "A monthly asset return 3% minus monthly risk-free .5% yields excess return:",
                ["2.5%", "3.5%", "6%"],
                0,
                "Subtract rates on the same horizon and unit basis.",
            ),
            (
                "A missing return always equals a zero return:",
                ["Yes", "No", "Only for daily data"],
                1,
                "Missingness and a realized zero are different observations.",
            ),
            (
                "A factor observation of 2 in percentage points is, in decimals:",
                ["2", ".2", ".02"],
                2,
                "Divide percentage points by 100.",
            ),
            (
                "A revision published in June may replace the data used by an April historical decision:",
                [
                    "Not unless it was already available in April",
                    "Always",
                    "Whenever the revised value looks better",
                ],
                0,
                "Historical reconstruction preserves the information available then.",
            ),
        ],
        [FACTORS, REG],
    )

    add(
        "3.8",
        1,
        "Derive and fit ordinary least squares",
        "Compute a slope, intercept, fitted values, and residuals and identify the assumptions behind their interpretation.",
        "Ordinary least squares chooses coefficients that minimize the sum of squared residuals. With an intercept and one nonconstant regressor, the slope is the centered cross-product divided by the centered squared-regressor sum; the intercept makes the fitted line pass through the sample means. These are algebraic properties, not proof of a causal model.\n\nFor multiple regressors, solve the least-squares problem using a numerically stable decomposition rather than explicitly inverting a poorly conditioned matrix. Full column rank is needed for unique unrestricted coefficients. Exogeneity connects the fitted association with a structural interpretation; random sampling or an appropriate dependence framework supports inference.",
        "Take x=[1,2,3] and y=[2,3,5]. Their means are 2 and 10/3. The centered cross-product is 3 and squared-x sum is 2, so slope is 1.5 and intercept is 1/3. Predictions are 1.8333, 3.3333, and 4.8333, with residuals 1/6, −1/3, and 1/6. Squared residuals sum to 1/6.\n\nThe residuals sum to zero because the fitted model contains an intercept. This property would not generally hold after arbitrary clipping or with a no-intercept model. Three observations make the arithmetic inspectable but are far too few for a persuasive financial study.",
        "Reproduce each fitted value and verify residual orthogonality to the intercept and x within numerical tolerance. Investigate a constant regressor, duplicate column, extreme observation, and different scaling. Preserve the specification alongside coefficients. A training fit should be reported as an in-sample description; future performance requires a separate dated evaluation. The downloadable research lab fits actual OLS models and compares classical and robust covariance estimates.",
        r"\hat\beta=\frac{\sum_i(x_i-\bar x)(y_i-\bar y)}{\sum_i(x_i-\bar x)^2}",
        'slope = 3 / 2\nintercept = 10 / 3 - slope * 2\nprint("OLS slope:", slope)\nprint("OLS intercept:", intercept)\nprint("Residual sum of squares:", (1 / 6) ** 2 + (-1 / 3) ** 2 + (1 / 6) ** 2)',
        "Fit x=[1,2,3], y=[3,5,7]. Then explain why an exact training fit does not establish a profitable forecasting strategy.",
        "Slope is 2 and intercept 1, with zero residuals. This tiny constructed sample establishes arithmetic, not stable future returns, realistic costs, or a causal relation.",
        [
            (
                "Centered cross-product 12 and squared-x sum 4 imply slope:",
                [".333", "3", "48"],
                1,
                "The OLS slope is 12/4 = 3.",
            ),
            (
                "Residuals sum to zero in ordinary OLS with:",
                [
                    "An intercept, up to numerical tolerance",
                    "Any arbitrary fitted curve",
                    "No data assumptions or fitted coefficients",
                ],
                0,
                "The normal equation for the intercept imposes this sample property.",
            ),
            (
                "Slope 2, mean x 3, and mean y 8 imply intercept:",
                ["6", "11", "2"],
                2,
                "The fitted intercept is 8−2×3 = 2.",
            ),
            (
                "Perfectly duplicated regressors create:",
                [
                    "More unique information",
                    "A rank-deficient design",
                    "Guaranteed predictive improvement",
                ],
                1,
                "Unrestricted coefficients cannot be separately identified from identical columns.",
            ),
        ],
        [REG],
    )

    add(
        "3.1",
        1,
        "Multiple regression and diagnostics",
        "Interpret partial slopes, multicollinearity, residual fit, and leverage without treating diagnostic cutoffs as automatic verdicts.",
        "A multiple-regression coefficient describes the association with one regressor conditional on the included others. Residualizing both the outcome and the chosen regressor against the controls gives the same partial slope under the standard OLS setup. Adding a control changes this conditioning set and can change the estimand.\n\nMulticollinearity means that regressors contain overlapping information. It can make individual coefficients imprecise or unstable even when combined predictions remain useful. Perfect collinearity prevents unique coefficients. The variance inflation factor summarizes how strongly a regressor is explained by the other included regressors; it is a diagnostic, not a universal deletion rule.",
        "If regressing one factor on the others gives R-squared .8, its VIF is 1/(1−.8)=5. Under comparable homoskedastic conditions, this corresponds to variance inflation relative to an orthogonal design; standard-error inflation is the square root, about 2.236. It does not mean the coefficient is biased by exactly five times.\n\nA model explains 80 of 100 units of centered outcome variation, giving R-squared .8. Adding another regressor cannot increase the ordinary in-sample residual sum of squares, but can worsen adjusted R-squared or future prediction loss.",
        "Inspect residual-versus-fitted plots, leverage, influential observations, condition numbers, and stability across sensible samples. Preserve economically necessary controls when their omission would alter the question; address redundant encoding or regularization deliberately. Report coefficient uncertainty and out-of-sample evidence alongside fit. Compare a model before and after removing one extreme observation, documenting why it is excluded rather than deleting points solely to improve significance.",
        r"VIF_j=(1-R_j^2)^{-1}",
        'import math\nvif = 1 / (1 - 0.8)\nprint("Variance inflation factor:", round(vif, 6))\nprint("Standard-error multiplier:", math.sqrt(vif))',
        "A regressor has auxiliary R-squared .75. Compute VIF and its square-root multiplier. Explain when removing this regressor could change the research question.",
        "VIF is 4 and its square root is 2. Removing an economically required control changes the conditioning set and may introduce omitted-variable bias, so use the diagnostic alongside the estimand.",
        [
            (
                "If R-squared for a regressor on other regressors is .8, VIF is:",
                ["1.25", "4", "5"],
                2,
                "1/(1−.8) = 5; the legacy first practice key is retained.",
            ),
            (
                "Adding a regressor always improves future forecasting:",
                ["Yes", "No", "Only if training R-squared rises"],
                1,
                "In-sample fit and future generalization are distinct.",
            ),
            (
                "Auxiliary R-squared .5 implies VIF:",
                ["2", "5", ".5"],
                0,
                "The variance inflation factor is 1/(1−.5) = 2.",
            ),
            (
                "An influential observation should be removed automatically:",
                [
                    "Yes",
                    "If it reduces the p-value",
                    "No; investigate its validity and report sensitivity",
                ],
                2,
                "Influence is a reason for diagnosis, not outcome-driven deletion.",
            ),
        ],
        [REG, DIAG],
    )

    add(
        "3.9",
        2,
        "Sampling uncertainty and joint hypotheses",
        "Distinguish confidence intervals, prediction intervals, t tests, and joint restrictions with explicit reference distributions.",
        "A standard error quantifies uncertainty in an estimator under a sampling model. A confidence interval concerns an unknown parameter; a prediction interval also includes variability of a future outcome. A narrow coefficient interval therefore does not imply a narrow range of future returns. State whether inference is finite-sample normal-theory, asymptotic, bootstrap-based, or otherwise justified.\n\nA t statistic divides an estimated departure from the null by its standard error. A p-value describes extremeness under the null and reference assumptions, not the probability that the null is true. Testing several coefficients jointly requires a joint procedure; reading each individual p-value is not equivalent.",
        "A coefficient estimate is .6 with standard error .2. Testing zero gives t=3. Using an illustrative large-sample 1.96 multiplier gives an interval [.208,.992]. For a small classical regression, the t critical value depends on residual degrees of freedom and is typically wider than 1.96.\n\nSuppose the standard error of a fitted mean is .1 while the disturbance standard deviation is .5. Ignoring their estimation uncertainty for illustration, a new observation's forecast standard deviation is sqrt(.1²+.5²), about .510. The disturbance dominates the parameter component.",
        "Record the null, direction, covariance estimator, degrees of freedom, and confidence level before interpreting a test. Distinguish statistical evidence from economic magnitude after fees. For joint restrictions, retain the restriction matrix or a plain-language equivalent and the chosen test distribution. The worked calculations use stipulated standard errors; the downloadable lab estimates them from data and reports the convention used.",
        r"t=(\hat\beta-\beta_0)/SE(\hat\beta)",
        'import math\nprint("t statistic:", 0.6 / 0.2)\nprint("Approximate interval:", 0.6 - 1.96 * 0.2, 0.6 + 1.96 * 0.2)\nprint("Forecast standard deviation:", math.sqrt(0.1 ** 2 + 0.5 ** 2))',
        "Estimate .4 with standard error .25: compute a zero-null statistic and large-sample 95% interval, then state what it does not establish.",
        "t=1.6 and interval [−.09,.89]. It includes zero under this approximation and does not prove absence of an effect, causal identification, or economic profitability.",
        [
            (
                "A p-value is the probability the null hypothesis is true:",
                ["False", "True", "True after enough observations"],
                0,
                "It is calculated conditional on the null and test assumptions.",
            ),
            (
                "Prediction intervals generally include uncertainty about:",
                [
                    "Only the intercept",
                    "Only the slope",
                    "The estimated mean and future disturbance",
                ],
                2,
                "A future observation varies around its conditional mean.",
            ),
            (
                "Estimate .9 and standard error .3 give a zero-null t statistic:",
                [".3", "3", "2.7"],
                1,
                ".9/.3 = 3 under the declared covariance estimate.",
            ),
            (
                "A small-sample classical regression should automatically use 1.96 for every 95% interval:",
                [
                    "Yes",
                    "Only for monthly returns",
                    "No; check degrees of freedom and the reference distribution",
                ],
                2,
                "Normal critical values need an appropriate approximation or model.",
            ),
        ],
        [REG],
    )

    add(
        "3.10",
        2,
        "Heteroskedasticity, robust covariance, and WLS",
        "Separate coefficient estimation from covariance estimation and explain when weighting changes the fitted model.",
        "Heteroskedasticity means that disturbance variance differs across observations conditional on the design. Under appropriate exogeneity, OLS coefficients can remain consistent while conventional homoskedastic standard errors become unreliable. Heteroskedasticity-robust covariance changes uncertainty estimates without changing the OLS coefficients. It does not repair endogeneity, selection bias, or arbitrary dependence.\n\nWeighted least squares changes the objective itself. If conditional variance is known up to scale, inverse-variance weights can improve efficiency under the model. Estimated or arbitrary weights need their own justification and may change the population emphasis of the analysis. Do not confuse robust standard errors with downweighting observations.",
        "Two observations have conditional variances 1 and 4. Their idealized inverse-variance weights are 1 and .25, respectively. If their outcomes are 2 and 6 in an intercept-only model, the weighted mean is (1×2+.25×6)/1.25=2.8, versus unweighted mean 4. The difference shows that WLS changes the fitted coefficients.\n\nIn a separate OLS fit, the slope remains .8 whether reported with conventional standard error .1 or robust standard error .2. The corresponding zero-null statistics change from 8 to 4 because the uncertainty estimate changed.",
        "Plot residual scale against fitted values and relevant covariates; combine diagnostic tests with the economic mechanism. Choose an HC variant deliberately, especially with leverage or a limited sample, and report it. Compare coefficient and covariance changes separately. If observations are serially dependent or grouped, heteroskedasticity-only robustness may be insufficient; the next lessons address HAC and panel dependence.",
        r"w_i\propto1/\sigma_i^2",
        'print("Second observation weight:", 1 / 4)\nprint("Weighted mean:", (2 + 0.25 * 6) / 1.25)\nprint("Robust t statistic:", 0.8 / 0.2)',
        "For variances 1 and 9 and outcomes 3 and 12, compute the inverse-variance weighted mean. Explain why HC covariance would leave an existing OLS point estimate unchanged.",
        "Weights 1 and 1/9 produce mean 3.9. HC covariance estimates uncertainty around the same OLS coefficients; WLS refits a differently weighted objective.",
        [
            (
                "HC robust covariance changes OLS coefficients automatically:",
                ["Yes", "No", "Only if the p-value falls"],
                1,
                "It changes the covariance estimate, not the fitted OLS objective.",
            ),
            (
                "Conditional variance 4 corresponds to inverse-variance weight:",
                ["4", "2", ".25"],
                2,
                "The weight is 1/4, not the inverse standard deviation.",
            ),
            (
                "Robust standard errors fix omitted-variable bias:",
                ["No", "Yes", "Only with many controls"],
                0,
                "Changing covariance does not establish exogeneity.",
            ),
            (
                "WLS weights are proportional to inverse variance. A variance of 16 gives weight:",
                [".25", ".0625", "16"],
                1,
                "1/16 = .0625 under the stated weighting convention.",
            ),
        ],
        [REG, DIAG],
    )

    add(
        "3.11",
        2,
        "Serial dependence and Newey–West inference",
        "Estimate uncertainty for dependent financial observations and explain what HAC does and does not correct.",
        "Autocorrelation links disturbances across time. Overlapping returns, stale marks, and gradual adjustment can produce dependence even when observations are stored on distinct dates. Treating dependent rows as independent can exaggerate precision. A heteroskedasticity-and-autocorrelation-consistent covariance estimator includes weighted lagged score cross-products in the covariance calculation.\n\nHAC modifies uncertainty around a coefficient estimator; it does not remove leakage, make an endogenous regressor exogenous, or guarantee good forecasts. Its lag length and kernel encode choices about dependence. Consistency requires suitable regularity and sample-size conditions, so small-sample results deserve sensitivity analysis.",
        "For a sample mean, suppose lag-zero autocovariance is 4 and lag-one autocovariance is 1. With a Bartlett lag-one weight .5, the illustrative long-run variance is 4+2×.5×1=5. Over 100 observations, standard error is sqrt(5/100)=.2236 instead of the independence value .2.\n\nNegative autocovariances could reduce the long-run variance, so robust standard errors are not guaranteed to be larger. In a regression, replace scalar residual autocovariances with the relevant regressor-times-residual score terms; the simple mean example teaches the weighting rather than a complete matrix estimator.",
        "Record row ordering, data frequency, overlapping horizon, maximum lag, kernel, finite-sample correction, and reference distribution. Compare plausible lag choices without selecting solely for significance. Preserve the coefficient and covariance separately in the research artifact. The downloadable factor project fits OLS and actual HAC covariance and checks that changing the covariance convention leaves point estimates unchanged.",
        r"\Omega=\gamma_0+2\sum_{j=1}^{L}w_j\gamma_j",
        'import math\nlong_run = 4 + 2 * 0.5 * 1\nprint("Long-run variance:", long_run)\nprint("HAC mean standard error:", math.sqrt(long_run / 100))',
        "Use lag-zero covariance 9, lag-one 2, Bartlett weight .5, and n=100. Compute the mean's long-run variance and standard error; state one defect HAC cannot fix.",
        "Long-run variance is 11 and standard error sqrt(.11), about .3317. HAC cannot repair look-ahead, endogeneity, or an incorrect information cutoff.",
        [
            (
                "HAC primarily changes:",
                [
                    "The data publication dates",
                    "Estimated coefficient covariance",
                    "The economic definition of a factor",
                ],
                1,
                "It estimates uncertainty allowing specified temporal dependence.",
            ),
            (
                "HAC standard errors must always exceed ordinary ones:",
                ["Yes", "Only for stocks", "No"],
                2,
                "Dependence signs and the full covariance structure determine the change.",
            ),
            (
                "Lag-zero covariance 3 and lag-one 1 with weight .5 imply long-run variance:",
                ["4", "3.5", "5"],
                0,
                "3+2×.5×1 = 4 in the sample-mean example.",
            ),
            (
                "A five-day overlapping outcome is treated as five independent daily outcomes. The main inference concern is:",
                [
                    "The font used in the chart",
                    "Dependence between adjacent labels",
                    "That means cannot be computed",
                ],
                1,
                "Overlapping windows share underlying returns.",
            ),
        ],
        [DIAG, REG],
    )

    add(
        "3.12",
        2,
        "Specification, omitted variables, and endogeneity",
        "Diagnose why a regression slope can differ from the structural quantity the researcher intended to estimate.",
        "Endogeneity occurs when a regressor is correlated with the structural disturbance. Omitted common causes, simultaneous determination, selection, and measurement error can create it. Adding more observations or using robust standard errors does not generally remove the resulting bias. A better fit is not an identification argument.\n\nIn a simple omitted-variable setting, the short regression's slope combines the direct slope with the omitted variable's effect multiplied by its projection on the included regressor. The direction depends on both relationships. Controls must be chosen according to the causal or predictive task; conditioning on a mediator or collider can create different problems.",
        "Suppose the structural direct effect of x is 1, an omitted z has effect 2, and z's population linear projection on x has slope .5. Under the simple model assumptions, the short-regression slope is 1+2×.5=2. A reported coefficient of 2 would overstate the direct effect of 1. If the projection slope were −.5, the short slope would be zero.\n\nClassical independent measurement error in a single regressor can attenuate its slope under a simple model. This direction is not universal in multiple-regressor or nonclassical-error settings.",
        "Draw a causal diagram or write a structured explanation of timing and common causes. Compare specifications as sensitivity evidence, not as automatic proof. Document proxy quality and plausible omitted factors. Consider a credible instrument, panel design, or quasi-experiment when the question is causal, and state why its assumptions are plausible. If no identification design is available, report an association or a prediction rather than silently upgrading the claim.",
        r"\beta_{short}=\beta+\gamma\delta",
        'print("Short-regression slope:", 1 + 2 * 0.5)\nprint("Opposite omitted relation:", 1 + 2 * -0.5)',
        "Let direct slope .8, omitted effect 1.5, and projection slope .4. Compute the short slope and explain why robust standard errors do not recover the direct effect.",
        "The short slope is 1.4. A covariance correction quantifies uncertainty around the fitted estimator; it does not remove the omitted association term .6.",
        [
            (
                "A larger sample automatically eliminates omitted-variable bias:",
                ["No", "Yes", "Only above 1,000 rows"],
                0,
                "An inconsistent estimator can become precisely wrong.",
            ),
            (
                "The sign of simple omitted-variable bias depends on:",
                [
                    "Only the sample size",
                    "Only the intercept",
                    "The omitted effect and its association with the included regressor",
                ],
                2,
                "The bias term is the product of those relationships.",
            ),
            (
                "Direct slope 2 plus omitted effect 3 times projection slope .2 gives short slope:",
                ["2.2", "2.6", "5.2"],
                1,
                "2+3×.2 = 2.6 under the stipulated model.",
            ),
            (
                "A model has excellent training fit but no identification design. A causal conclusion is:",
                ["Guaranteed", "Automatic with HC errors", "Not established by fit alone"],
                2,
                "Identification and goodness of fit answer different questions.",
            ),
        ],
        [REG, IV],
    )

    add(
        "3.13",
        3,
        "Stationarity, unit roots, and deterministic trends",
        "Distinguish stable dependence from stochastic trends and interpret complementary stationarity tests.",
        "Weak stationarity concerns a constant mean, finite constant variance, and autocovariances depending on lag rather than calendar time. A deterministic trend plus stationary noise differs from a unit-root process: detrending and differencing address different structures. A stationary series can still be highly persistent, heteroskedastic in a conditional model, or difficult to forecast.\n\nThe augmented Dickey–Fuller test uses a unit-root null under a chosen deterministic specification and lag structure. KPSS reverses the broad perspective by using a stationarity null under its own assumptions. Failure to reject either null is not proof; low power, breaks, and inappropriate deterministic terms can make conclusions uncertain.",
        "For a stationary AR(1) specification y_t=.2+.8y_(t−1)+u_t, the unconditional mean is .2/(1−.8)=1. The effect of an isolated shock after three steps is .8³=.512 of its initial size. At coefficient 1, the usual finite stationary mean formula no longer applies.\n\nA price random walk can produce apparently impressive regression fit against another trending series. Differencing may remove a unit root, but it can also discard an economically meaningful long-run relationship when variables are cointegrated.",
        "Plot levels and differences, inspect the observation frequency and breaks, and specify intercept/trend terms before interpreting test output. Report statistic, null, lag selection, sample span, and critical-value convention. Test sensitivity to plausible specifications rather than searching for whichever setting produces rejection. Keep stationarity diagnostics separate from a trading claim: a stationary spread may still be costly or unstable to trade.",
        r"\mu=c/(1-\phi),\quad |\phi|<1",
        'print("AR stationary mean:", 0.2 / (1 - 0.8))\nprint("Shock remaining after three steps:", 0.8 ** 3)',
        "For c=.1 and phi=.5, calculate the stationary mean and four-step shock multiplier. State the ADF null and a reason its test could be inconclusive.",
        "Mean is .2 and shock multiplier .0625. ADF tests a unit-root null under its specification; a short sample, structural break, or inappropriate deterministic terms can weaken interpretation.",
        [
            (
                "The usual ADF null is:",
                ["A unit root", "Guaranteed stationarity", "Zero trading cost"],
                0,
                "Specify deterministic terms and lag assumptions when using this null.",
            ),
            (
                "Failure to reject a unit-root null proves a unit root:",
                ["Yes", "No", "Only at monthly frequency"],
                1,
                "A test can lack power or be misspecified.",
            ),
            (
                "AR intercept .3 and coefficient .5 imply stationary mean:",
                [".15", ".3", ".6"],
                2,
                "The stationary mean is .3/(1−.5) = .6.",
            ),
            (
                "A deterministic trend and a unit root require identical treatment in every model:",
                ["No", "Yes", "Only if prices rise"],
                0,
                "Detrending and differencing target different structures.",
            ),
        ],
        [TIME],
    )

    add(
        "3.14",
        3,
        "AR, MA, and ARIMA forecasting",
        "Construct recursive forecasts and compare dynamic mean specifications with an explicit horizon and information set.",
        "An autoregressive model relates the current value to earlier values; a moving-average model relates it to current and earlier innovations. The moving average in ARMA terminology is not a rolling average of prices. ARIMA adds differencing when an integrated component is part of the specification. Seasonal terms require a justified calendar period and enough cycles to estimate.\n\nForecasting propagates the estimated model from information available at the origin. Future innovations have conditional mean zero under the model but remain a source of forecast uncertainty. A point forecast should therefore be accompanied by a horizon-specific uncertainty statement and a comparison with a simple baseline.",
        "Use y_t=.2+.8y_(t−1)+u_t with latest observation 2. The one-step prediction is 1.8; the two-step prediction is .2+.8×1.8=1.64. Both move toward the stationary mean 1. If innovation variance is .04 and parameters are treated as known, two-step forecast error variance is .04×(1+.8²)=.0656.\n\nThe random-walk baseline instead predicts the latest level 2 at both horizons. Whether the AR forecast improves matters empirically; mean reversion in a fitted equation is not proof of reliable future reversion.",
        "Choose candidate orders using development data and inspect residual dependence, convergence, stationarity, and invertibility conditions where relevant. Preserve the transformation needed to convert forecasts back to levels. Log the origin and horizon of every forecast; one-step rolling evaluation differs from a fixed-origin multi-step exercise. Never refresh a multi-step forecast with future observed values while labeling it as the original forecast.",
        r"\hat y_{t+h|t}=\mu+\phi^h(y_t-\mu)",
        'one = 0.2 + 0.8 * 2\ntwo = 0.2 + 0.8 * one\nprint("One-step forecast:", one)\nprint("Two-step forecast:", two)\nprint("Two-step error variance:", 0.04 * (1 + 0.8 ** 2))',
        "Forecast two steps from y=3 under c=.5 and phi=.5. Explain which future information must remain unavailable to a fixed-origin forecast.",
        "Predictions are 2 and 1.5. Future realized observations and shocks cannot enter the original fixed-origin computation; later updated forecasts must receive new origin labels.",
        [
            (
                "MA in ARMA means a model of:",
                [
                    "Only rolling price means",
                    "Current and lagged innovations",
                    "A guaranteed moving-average crossover profit",
                ],
                1,
                "The time-series term differs from a technical rolling-average indicator.",
            ),
            (
                "A fixed-origin forecast may silently use later actual outcomes:",
                ["Always", "Only for the second step", "No"],
                2,
                "That changes the information set and invalidates the original evaluation.",
            ),
            (
                "With c=1, phi=.5, and current y=4, the next prediction is:",
                ["3", "2", "5"],
                0,
                "The conditional next-step mean is 1+.5×4 = 3.",
            ),
            (
                "A multi-step forecast interval should account for:",
                [
                    "Only the first fitted value",
                    "Accumulating future innovation uncertainty",
                    "Only the chart's scale",
                ],
                1,
                "Unobserved future shocks contribute to horizon-specific error.",
            ),
        ],
        [TIME],
    )

    add(
        "3.15",
        3,
        "Forecast selection and rolling evaluation",
        "Separate information criteria, development selection, and untouched evaluation, including overlapping forecast errors.",
        "Information criteria trade in-sample likelihood fit against parameter complexity under a defined statistical model. They are not realized trading-performance scores. Comparing AIC or BIC requires compatible likelihoods and observations; a change in differencing or effective sample can complicate a naive comparison.\n\nA rolling-origin evaluation repeatedly trains using only observations available at each origin and scores later outcomes. Expanding windows retain earlier history; rolling windows limit it. This choice changes the bias–variance and regime-adaptation trade-off. Hyperparameters must be selected inside the development process rather than repeatedly optimized on the final test period.",
        "Model A has log likelihood −100 and three estimated parameters, so AIC is 206. Model B has log likelihood −98 and six parameters, so AIC is 208. Under the same-data comparison, A is preferred by AIC even though B fits better.\n\nSuppose forecast errors on a held-out segment are [1,−1,2]. MSE is 2 and MAE is 4/3. Squared loss places more weight on the large miss. For overlapping multi-step forecasts, adjacent errors share outcomes, so a comparison test must address dependence rather than count every row as independent.",
        "Save origin, training cutoff, label availability, chosen parameters, prediction, actual outcome, and baseline for every fold. Aggregate performance by horizon and regime as well as overall. Distinguish parameter-selection uncertainty from observation uncertainty. A difference in average loss should be paired with uncertainty suited to the forecast design; avoid declaring a universal winner from a handful of correlated errors.",
        r"AIC=2k-2\log\hat L",
        'print("AIC model A:", 2 * 3 - 2 * -100)\nprint("AIC model B:", 2 * 6 - 2 * -98)\nprint("Forecast MSE:", (1 + 1 + 4) / 3)',
        "Compare AIC for log likelihoods −50 with two parameters and −48 with five parameters. Specify a rolling-origin baseline and the data cutoff for fitting it.",
        "AIC values are 104 and 106, favoring the first under a compatible comparison. A training-mean or last-observation baseline must use only information available at each origin.",
        [
            (
                "Lower AIC automatically means higher net trading profit:",
                ["No", "Yes", "Only for daily prices"],
                0,
                "AIC concerns a likelihood/complexity criterion, not execution economics.",
            ),
            (
                "Tuning repeatedly on the final test set makes it:",
                ["More untouched", "Part of model development", "A larger population"],
                1,
                "Selection consumes the independence of the evaluation set.",
            ),
            (
                "Log likelihood −40 and four parameters give AIC:",
                ["72", "80", "88"],
                2,
                "Using the stated AIC convention gives 2×4−2×(−40) = 88.",
            ),
            (
                "Adjacent five-step forecast errors share realized outcomes. Treating them as independent can:",
                [
                    "Misstate comparison uncertainty",
                    "Make them unobservable",
                    "Remove the need for a baseline",
                ],
                0,
                "Overlapping horizons create dependence.",
            ),
        ],
        [TIME, DIAG],
    )

    add(
        "3.16",
        3,
        "VAR systems and predictive causality",
        "Model interdependent series while distinguishing Granger predictability from structural causal effects.",
        "A vector autoregression models each variable using lags of all included variables. It can capture feedback in predictive dynamics, but the parameter count grows with variables and lags. Stable estimation requires sufficient observations, appropriate transformations, and a coherent system specification.\n\nA Granger-style restriction asks whether one variable's lagged values improve prediction of another conditional on the included information. It does not by itself establish an intervention effect. Omitted variables, timing differences, and contemporaneous shocks can create predictive relationships without the proposed economic causality.",
        "Let the next two-variable mean equal A times the current vector, where A has rows [.6,.2] and [.1,.5], and the current vector is [2,1]. Predictions are [1.4,.7]. An isolated shock of one unit to the first variable has next-step propagation [.6,.1] under this reduced-form dynamic map.\n\nA structural impulse response additionally needs assumptions that identify economically meaningful shocks from correlated innovations. Cholesky ordering is one identification choice, not a fact discovered automatically from the covariance matrix.",
        "Inspect lag selection, residual autocorrelation, stability, deterministic terms, and available sample size. If levels are integrated and cointegrated, consider a system that preserves the long-run relation rather than blindly applying a stationary VAR to levels or discarding all information by differencing. Report the ordering or restrictions used in impulse responses and show sensitivity to plausible alternatives. Keep the language predictive unless a structural identification argument has been supplied.",
        r"y_t=c+A_1y_{t-1}+u_t",
        'print("First VAR forecast:", 0.6 * 2 + 0.2 * 1)\nprint("Second VAR forecast:", 0.1 * 2 + 0.5 * 1)',
        "Forecast the vector [1,2] using the stated matrix. Explain why predictive improvement from a lagged variable does not automatically identify its policy effect.",
        "Forecasts are [1,.1+1]=[1,1.1]. Shared omitted causes and contemporaneous shocks can produce predictability without identifying intervention effects.",
        [
            (
                "Granger predictability is automatically a structural causal effect:",
                ["Yes", "No", "Only in a two-variable system"],
                1,
                "It is conditional predictive information under the included model.",
            ),
            (
                "Adding many variables and lags to a VAR:",
                [
                    "Never costs degrees of freedom",
                    "Guarantees stability",
                    "Can sharply increase parameter count",
                ],
                2,
                "Each equation includes lags of all system variables.",
            ),
            (
                "A forecast equation .4x+.3z with x=2 and z=3 gives:",
                ["1.7", "1.2", "2.1"],
                0,
                "Apply the first equation to the lagged vector: .4×2+.3×3 = 1.7.",
            ),
            (
                "An orthogonalized impulse response depends on:",
                [
                    "Only the chart title",
                    "Its shock-identification assumptions",
                    "No assumptions beyond correlation",
                ],
                1,
                "Ordering and restrictions determine the interpretation of shocks.",
            ),
        ],
        [TIME],
    )

    add(
        "3.2",
        4,
        "Time series and cointegration",
        "Test whether integrated series share a stable long-run combination and distinguish that evidence from a tradable spread.",
        "Cointegration describes integrated variables whose particular linear combination is stationary under the chosen definition and deterministic terms. High correlation alone is insufficient: two unrelated trending series can look strongly associated. Establish plausible integration orders and an economic relation before testing a residual combination.\n\nIn a two-step Engle–Granger procedure, first estimate a levels relation and then assess its residual stationarity using the appropriate cointegration test distribution. Ordinary standalone ADF critical values are not automatically valid for estimated residuals. The null of the usual cointegration test is no cointegration under its assumptions.",
        "Suppose the estimated relation is y=2+1.5x+s. At x=10 and y=18, the estimated spread residual is 1. A change of units from x dollars to x cents changes the numerical hedge coefficient; the economic exposure must be converted consistently. If the two levels are both I(1) and the residual process is stationary, the relation may be cointegrating.\n\nEven with that statistical evidence, fees, borrow constraints, adjustment delays, parameter uncertainty, and structural breaks can make a spread strategy unattractive. The in-app long/cash simulator cannot represent a simultaneous long/short pair.",
        "Fit the relation on a training interval and assess stability on later data. Keep the intercept/trend convention, lag selection, test null, and estimated hedge units in the report. Inspect a known break and compare rolling estimates. Never select hundreds of pairs and interpret the smallest unadjusted p-value as a prespecified discovery. Preserve the distinction between evidence for a long-run relation and evidence for an executable after-cost strategy.",
        r"s_t=y_t-\alpha-\beta x_t",
        'print("Cointegrating residual:", 18 - 2 - 1.5 * 10)',
        "For y=25, x=12, intercept 1, and hedge coefficient 2, compute the residual. List the statistical and execution evidence still needed before proposing a pair trade.",
        "The residual is zero. Need plausible integration orders, a valid cointegration test and stability analysis, plus both-leg costs, borrow, margin, and fill-risk modeling. A zero residual at one date establishes none of these.",
        [
            (
                "Correlation alone establishes cointegration:",
                ["Always", "Only with daily data", "No"],
                2,
                "Cointegration concerns a stationary combination of integrated series.",
            ),
            (
                "Estimated-residual cointegration testing always uses ordinary ADF critical values:",
                ["No", "Yes", "Only when the intercept is nonzero"],
                0,
                "The estimated first-stage relation changes the relevant test distribution.",
            ),
            (
                "With y=15, x=6, intercept 1, and hedge slope 2, residual is:",
                ["1", "2", "3"],
                1,
                "Subtract the fitted levels relation: 15−1−2×6 = 2.",
            ),
            (
                "A statistically cointegrated pair is necessarily profitable after costs:",
                ["Yes", "Only if correlation is high", "No"],
                2,
                "Statistical equilibrium evidence does not establish executable economic edge.",
            ),
        ],
        [COINT, TIME],
    )

    add(
        "3.17",
        4,
        "Error correction and adjustment speed",
        "Interpret an error-correction coefficient and calculate a model-dependent spread half-life.",
        "An error-correction model links short-run changes to lagged deviation from a long-run relation, often with additional lagged differences. A negative adjustment coefficient can describe correction when the spread is above its equilibrium, but sign conventions and the variable being modeled matter. In a multivariate system, more than one variable may adjust.\n\nFor a simple AR(1) spread s_t=phi*s_(t−1)+u_t with 0<phi<1, the half-life is log(.5)/log(phi). This is a property of a fitted linear conditional-mean model. It is not a guaranteed exit time, and the expression needs modification or a different interpretation for oscillatory, unit-root, or explosive dynamics.",
        "A spread coefficient phi=.8 implies a half-life of about 3.106 observation periods. In the corresponding difference equation, delta s_t=−.2*s_(t−1)+u_t. If the previous spread is 5, the expected next change is −1 and the expected next level is 4.\n\nDaily and weekly observations give different calendar interpretations of the same numeric half-life. Parameter uncertainty is also nonlinear near phi=1: a small estimation change can greatly increase the inferred horizon.",
        "Estimate adjustment dynamics only after a defensible long-run specification. Report the sampling frequency, coefficient interval, residual diagnostics, and sensitivity across regimes. Define exits using both model evidence and operational risk; do not wait indefinitely because a fitted half-life once looked short. The worked worksheet uses fixed parameters; the downloadable lab estimates an autoregression from a synthetic spread and exposes its limitations.",
        r"h_{1/2}=\log(0.5)/\log(\phi)",
        'import math\nprint("Spread half-life:", math.log(0.5) / math.log(0.8))\nprint("Expected spread change:", -0.2 * 5)',
        "Compute the half-life for phi=.5 and expected next spread from current value 8. Explain why the result does not promise a filled exit after that duration.",
        "Half-life is one observation period and the next conditional mean is 4. Realized shocks, changing parameters, and execution constraints can prevent the expected path and any intended exit.",
        [
            (
                "A half-life computed from phi=.5 is:",
                ["One observation period", "Half a calendar year", "Five periods"],
                0,
                "log(.5)/log(.5)=1; calendar duration depends on data frequency.",
            ),
            (
                "Near phi=1, the estimated half-life tends to become:",
                ["Guaranteed and precise", "Highly sensitive to the coefficient", "Always zero"],
                1,
                "The denominator approaches zero, amplifying parameter uncertainty.",
            ),
            (
                "In delta s=−.25*s_previous, previous spread 8 implies expected change:",
                ["2", "6", "−2"],
                2,
                "−.25×8 = −2 under this sign convention.",
            ),
            (
                "A negative correction coefficient must be interpreted with:",
                [
                    "The spread definition and equation being modeled",
                    "Only the current stock price",
                    "No units or timing",
                ],
                0,
                "Changing the normalization can change signs and economic interpretation.",
            ),
        ],
        [COINT, TIME],
    )

    add(
        "3.18",
        4,
        "ARCH, GARCH, and volatility persistence",
        "Model conditional variance separately from the return mean and evaluate the restrictions behind a long-run variance.",
        "Volatility clustering means large absolute returns tend to occur near other large absolute returns. A conditional-variance model allows forecast uncertainty to evolve even when expected returns remain near a constant. ARCH uses lagged squared innovations; GARCH also includes lagged conditional variance to represent persistence parsimoniously.\n\nIn the standard GARCH(1,1) recursion, nonnegative omega, alpha, and beta with omega positive provide common positivity conditions. Under the usual innovation and finite-second-moment setup, alpha+beta<1 gives a finite unconditional variance omega/(1−alpha−beta). These conditions do not establish a correct tail distribution or guarantee useful forecasts.",
        "Let omega=.01, alpha=.1, beta=.8, previous squared innovation .09, and previous variance .04. The next variance is .01+.1×.09+.8×.04=.051, with standard deviation about .2258 in the chosen return units. Persistence is .9 and the model's unconditional variance is .1.\n\nIf returns are changed from decimals to percentage points, squared-return quantities and omega scale by 10,000. Mixing an omega estimated on percentages with decimal inputs produces a seriously incorrect variance path.",
        "Separate parameter estimation from recursion with stipulated parameters. Inspect optimizer convergence, parameter restrictions, standardized residuals, remaining squared-residual dependence, and sensitivity to innovation distribution. Compare forecasts on later data against a simple rolling-variance or EWMA baseline. The course project computes transparent fixed-parameter recursions; optional estimation with the arch package requires a separately specified environment and convergence review.",
        r"h_t=\omega+\alpha u_{t-1}^2+\beta h_{t-1}",
        'import math\nh = 0.01 + 0.1 * 0.09 + 0.8 * 0.04\nprint("GARCH next variance:", h)\nprint("GARCH next volatility:", math.sqrt(h))\nprint("Long-run variance:", 0.01 / (1 - 0.1 - 0.8))',
        "Use omega=.02, alpha=.15, beta=.75, previous squared shock .04, and previous variance .08. Compute next and long-run variances under the stated conditions.",
        "Next variance is .086. Alpha+beta=.9, so the usual unconditional variance is .02/.1=.2. Both are in squared return units, not return units.",
        [
            (
                "GARCH directly models:",
                ["Guaranteed next returns", "Conditional variance", "A broker order queue"],
                1,
                "Its recursion forecasts a second-moment component under a specified mean model.",
            ),
            (
                "Changing return units by a factor of 100 changes variance units by:",
                ["100", "10", "10,000"],
                2,
                "Variance scales with the square of the return scale.",
            ),
            (
                "Omega .02 and alpha+beta=.8 imply usual long-run variance:",
                [".1", ".02", ".8"],
                0,
                ".02/(1−.8)=.1 under the finite-variance assumptions.",
            ),
            (
                "Computing a GARCH recursion with chosen parameters is the same as estimating them from data:",
                ["Yes", "No", "Only with 100 observations"],
                1,
                "Recursion and statistical parameter fitting are separate operations.",
            ),
        ],
        [VOL],
    )

    add(
        "3.19",
        4,
        "Asymmetry, fat tails, and variance forecast loss",
        "Evaluate asymmetric volatility responses and compare positive variance forecasts without confusing fit with tail calibration.",
        "A symmetric squared-shock model responds equally to positive and negative innovations of the same magnitude. GJR-style terms allow an additional response to negative shocks under a specified indicator convention. EGARCH models log variance with a different functional form. These are alternative models, not automatic upgrades for every asset or sampling frequency.\n\nA heavy-tailed innovation distribution changes likelihood and tail probabilities; it does not mean all relevant moments exist. Distinguish a conditional scale from an unconditional tail measure. Validate residual and forecast behavior rather than choosing a distribution only because it improves training likelihood.",
        "Consider a GJR addition gamma*u² for a negative innovation, with gamma=.2 and magnitude .3. Relative to an equally sized positive shock, the negative shock adds .2×.09=.018 variance units. Positivity and stationarity restrictions depend on the full specification and innovation distribution.\n\nFor positive variance forecast h=.04 and realized variance proxy v=.09, a common QLIKE form is log(h)+v/h, approximately −.9689. Its absolute value may be negative; comparisons on the same observations matter. A squared-return proxy is noisy, and loss interpretation depends on the proxy's properties.",
        "Evaluate variance forecasts at a consistent horizon and scale, with a baseline and a frozen test interval. Use multiple diagnostics: likelihood, variance loss, standardized residuals, and tail-exceedance behavior. A good average variance forecast can still misrepresent extreme losses. Explain whether parameters were estimated or stipulated and how zero or nonpositive variance forecasts are rejected before taking logarithms or dividing.",
        r"QLIKE(h,v)=\log(h)+v/h,\quad h>0",
        'import math\nprint("Negative-shock extra variance:", 0.2 * 0.3 ** 2)\nprint("QLIKE forecast loss:", math.log(0.04) + 0.09 / 0.04)',
        "For gamma=.1 and shock magnitude .2, compute the asymmetric variance addition. State why a zero variance forecast is invalid for the stated QLIKE expression.",
        "The addition is .004. A zero forecast makes both log(h) and v/h invalid; validate positivity and report the model failure rather than silently clipping without disclosure.",
        [
            (
                "A GJR indicator term distinguishes:",
                [
                    "Positive and negative shocks under its sign convention",
                    "Only stock names",
                    "Only training-set length",
                ],
                0,
                "The additional term is activated by the specified shock sign.",
            ),
            (
                "A variance loss comparison should use:",
                [
                    "Different units for each model",
                    "The same horizon and observations",
                    "Only the best-looking dates",
                ],
                1,
                "Comparable evaluation requires common outcomes and units.",
            ),
            (
                "Gamma .3 and negative shock magnitude .1 add variance:",
                [".03", ".3", ".003"],
                2,
                "The extra asymmetric variance term is .3×(.1)²=.003.",
            ),
            (
                "A lower average variance loss proves all tail probabilities are calibrated:",
                ["No", "Yes", "Only for Gaussian models"],
                0,
                "Tail calibration is a separate diagnostic.",
            ),
        ],
        [VOL],
    )

    add(
        "3.20",
        5,
        "CAPM and multi-factor return models",
        "Specify factor exposures with consistent excess-return units and distinguish explanatory loadings from expected risk premiums.",
        "A time-series factor regression relates an asset's excess return to common return factors. In CAPM form, the market excess return is the regressor. Multi-factor extensions include portfolios constructed to represent additional characteristics or risks. Factor definitions, universe, rebalancing, and data revisions are part of the model, not interchangeable labels.\n\nA time-series loading measures exposure to a factor's realized return variation. An expected factor premium is a different quantity, estimated with substantial uncertainty. A factor that explains covariance does not automatically earn a stable positive premium. Check whether the factor series are already excess returns or long–short spreads before subtracting a risk-free rate again.",
        "Cedar uses alpha=.001, market loading 1.1, size loading .3, and value loading −.2, all with returns in decimals. For factor returns .02, .01, and −.005, the fitted excess return is .001+.022+.003+.001=.027, or 2.7%. A realized asset excess return of .03 leaves residual .003.\n\nNegative value exposure describes this conditional regression loading. It is not proof that the portfolio follows a particular manager intention, and it can change with holdings or factor definitions.",
        "Document factor construction from the primary data provider and align the same dates and currency conventions. Report alpha, loadings, robust uncertainty, sample fit, and stability. In Quanta's factor studio, seeded synthetic factors have planted relationships and are labeled accordingly; they are not historical Fama–French observations. Uploaded observations must match the chosen model columns exactly. Replicate coefficient calculations before interpreting investment skill.",
        r"r_{i,t}-r_{f,t}=\alpha_i+\beta_i^\top f_t+\epsilon_{i,t}",
        'fitted = 0.001 + 1.1 * 0.02 + 0.3 * 0.01 - 0.2 * -0.005\nprint("Fitted excess return:", fitted)\nprint("Residual excess return:", 0.03 - fitted)',
        "Compute fitted excess return with alpha .002, market loading .9, size loading .2, market return .01, and size return −.005. Name the factor metadata needed for replication.",
        "The fitted return is .010. Preserve factor construction, frequency, units, currency, dates, and revision/version identifiers so another analyst can reproduce the design matrix.",
        [
            (
                "A factor loading and an expected factor premium are:",
                ["The same estimate", "Different quantities", "Always both positive"],
                1,
                "Exposure and expected compensation answer different questions.",
            ),
            (
                "Synthetic planted factors in a lab are:",
                [
                    "Official historical factor returns",
                    "Evidence of manager skill",
                    "A labeled simulation fixture",
                ],
                2,
                "Their provenance limits the interpretation of fitted results.",
            ),
            (
                "Alpha .001, market loading 1.2, and market excess return .01 imply fitted excess return:",
                [".013", ".012", ".0012"],
                0,
                "The conditional fitted excess return is .001+1.2×.01=.013.",
            ),
            (
                "Subtracting the risk-free rate again from an already excess-return factor can:",
                ["Always improve accuracy", "Misdefine the regressor", "Remove all bias"],
                1,
                "Normalize according to the source's actual construction.",
            ),
        ],
        [FACTORS, REG],
    )

    add(
        "3.21",
        5,
        "Alpha inference, attribution, and changing exposure",
        "Separate realized factor contributions, residual returns, statistical alpha, and evidence of repeatable performance.",
        "A realized factor contribution is a loading multiplied by a factor return under a specified attribution model. Summing contributions and residuals reconciles a modeled period's return; it does not prove that the same exposures or premiums will persist. Holdings-based and return-based attribution use different information and can disagree.\n\nRegression alpha is conditional on the included factors, frequency, sample, and accounting conventions. An omitted factor, nonlinear exposure, stale pricing, or selection can create apparent alpha. Statistical uncertainty, multiple testing, economic costs, and stability matter before interpreting it as skill.",
        "A period's market contribution is 1.5%, size contribution −.2%, value contribution .3%, and residual .4%. Total explained-plus-residual return is 2%. The residual is not automatically a persistent 0.4% monthly alpha.\n\nA daily intercept estimate .0002 with HAC standard error .00015 has statistic about 1.333. Multiplying both by 252 changes reporting scale but leaves this ratio unchanged; it does not create more independent evidence or provide a correctly compounded annual return forecast.",
        "Compare rolling or expanding exposure estimates and retain their windows. An unstable coefficient may reflect changing holdings, weak identification, or noisy estimates. Use economic explanations and uncertainty to interpret changes rather than reacting to every wiggle. Evaluate any selected alpha on untouched later observations, with benchmark costs and all tried variants logged. Avoid mixing additive arithmetic attribution with compounded multi-period returns without an explicit linking convention.",
        r"r_t=\sum_j\beta_j f_{j,t}+\epsilon_t",
        'print("Attributed period return:", 0.015 - 0.002 + 0.003 + 0.004)\nprint("Alpha t statistic:", 0.0002 / 0.00015)',
        "Contributions are .8%, .1%, −.2%, and residual .3%. Reconcile the period return and write two alternative explanations for the residual before calling it skill.",
        "Total is 1%. Missing exposures, nonlinear payoffs, timing mismatch, noise, or cost differences can explain a residual. Persistence needs a separate evaluation.",
        [
            (
                "A realized regression residual is automatically persistent alpha:",
                ["No", "Yes", "Only when positive"],
                0,
                "Residuals include noise and model misspecification.",
            ),
            (
                "Multiplying a coefficient and its standard error by the same positive number changes its zero-null t ratio:",
                ["Always", "No", "Only by 252"],
                1,
                "The common scale cancels in the ratio.",
            ),
            (
                "Contributions 2%, −.5%, .2%, plus residual .1% sum to:",
                ["2.8%", "1.2%", "1.8%"],
                2,
                "Add the stipulated one-period contributions.",
            ),
            (
                "A changing rolling beta can reflect:",
                [
                    "Changing exposure, estimation noise, or both",
                    "Only manager skill",
                    "A guaranteed regime break",
                ],
                0,
                "A rolling estimate is itself uncertain.",
            ),
        ],
        [FACTORS, REG],
    )

    add(
        "3.3",
        5,
        "Portfolio theory and factor pricing",
        "Compute covariance-driven portfolio risk and distinguish an optimizer's in-sample solution from a robust allocation.",
        "Portfolio variance depends on weights, individual variances, and cross-asset covariances. Diversification can reduce risk when returns are imperfectly correlated, but does not guarantee positive returns or protection in every crisis. Correlations and volatilities are estimates that can change together under stress.\n\nMean–variance optimization chooses weights under an estimated objective and constraints. Small changes in expected returns or covariance can produce large weight changes, particularly near singularity or with unconstrained leverage. Constraints encode a mandate; they also change the solution and should be reported explicitly.",
        "Two assets have annualized volatilities 20% and 10%, correlation .3, and equal weights. Variance is .25×.04+.25×.01+2×.5×.5×.3×.2×.1=.0155, so volatility is about 12.45%. If correlation rises to 1 with the other inputs unchanged, volatility becomes 15%.\n\nA portfolio can therefore lose diversification benefit without any change in nominal weights. A lower-correlation estimate is useful only to the extent it represents the relevant future conditions and comparable measurement conventions.",
        "Audit covariance symmetry, positive semidefiniteness, data units, and sample overlap before optimization. Compare equal weighting, a simple constrained minimum-variance portfolio, and stress scenarios. Separate expected return assumptions from realized evaluation. Quanta's optimizer uses long-only constraints and disclosed shrinkage; its output is an in-sample estimated allocation, not a recommendation proven best for future markets.",
        r"\sigma_p^2=w^\top\Sigma w",
        'import math\nvariance = 0.25 * 0.2 ** 2 + 0.25 * 0.1 ** 2 + 2 * 0.5 * 0.5 * 0.3 * 0.2 * 0.1\nprint("Portfolio variance:", variance)\nprint("Portfolio volatility:", math.sqrt(variance))',
        "Calculate variance and volatility for equal weights, volatilities .2 and .1, and zero correlation. Compare with the lesson's .3 correlation case.",
        "Variance is .0125 and volatility about .111803. Lower correlation reduces the covariance term here, holding weights and individual volatilities fixed; it does not guarantee returns.",
        [
            (
                "Lower correlation, all else equal, typically:",
                [
                    "Improves diversification",
                    "Guarantees positive returns",
                    "Raises each asset’s expected return",
                ],
                0,
                "Covariance contributes to total portfolio risk.",
            ),
            (
                "A minimum-variance estimate is automatically the best future allocation:",
                ["Yes", "Only with many assets", "No"],
                2,
                "It depends on estimated inputs, constraints, and the future environment.",
            ),
            (
                "Two equal-weight assets with variances .04 and .04 and zero covariance have portfolio variance:",
                [".04", ".02", ".08"],
                1,
                "With zero covariance, portfolio variance is .25×.04+.25×.04=.02.",
            ),
            (
                "A reported covariance matrix should be checked for:",
                [
                    "Only attractive formatting",
                    "Only positive average returns",
                    "Compatible units and positive semidefinite structure",
                ],
                2,
                "Invalid inputs can make portfolio risk calculations nonsensical.",
            ),
        ],
        [FACTORS, REG],
    )

    add(
        "3.22",
        5,
        "Shrinkage, PCA, and estimation risk",
        "Regularize noisy covariance estimates and distinguish statistical components from economically named factors.",
        "Sample covariance becomes unstable when the number of assets is large relative to observations, or when assets are highly redundant. Shrinkage blends it with a structured target. The target and intensity express a trade-off between sample detail and stability; they are not universal constants. Estimate or choose them within development data and report sensitivity.\n\nPrincipal components find orthogonal directions of sample variation. A leading component may resemble a market factor, but its sign is arbitrary and its economic meaning is not supplied by the algorithm. Explained variance measures reconstruction of variation, not expected profit or causal importance.",
        "A sample covariance has diagonal entries .04 and .01 and off-diagonal .018. Shrinking 50% toward its diagonal target leaves variances unchanged and reduces covariance to .009. Equal-weight variance changes from .0215 to .017. The lower estimated number is a consequence of the chosen model, not proof that actual future risk fell.\n\nIf covariance eigenvalues are .06, .03, and .01, the first principal component explains 60% of total sample variance. Retaining it discards 40%, which may include economically important risks.",
        "Fit normalization and components on training data, then transform later observations using the frozen artifact. Inspect component stability and factor interpretation across windows. Report the shrinkage target, intensity, asset order, and units. Compare realized risk of constrained allocations against simple baselines rather than choosing the estimator solely because it gives the lowest in-sample volatility.",
        r"\hat\Sigma_{shrink}=(1-\lambda)S+\lambda T",
        'covariance = 0.5 * 0.018\nprint("Shrunk covariance:", covariance)\nprint("Equal-weight shrunk variance:", 0.25 * 0.04 + 0.25 * 0.01 + 0.5 * covariance)\nprint("First component variance share:", 0.06 / (0.06 + 0.03 + 0.01))',
        "Shrink covariance .02 halfway toward zero while retaining variances .09 and .04. Compute equal-weight variance and explain why it is an estimate rather than a physical risk reduction.",
        "Shrunk covariance is .01, and equal-weight variance is .0375. The assets did not change; the estimated covariance model did. Validate its forecasts on later data.",
        [
            (
                "A PCA component's sign is:",
                [
                    "A fixed economic law",
                    "Arbitrary up to an equivalent sign flip",
                    "Always positive",
                ],
                1,
                "Flipping both component direction and scores leaves reconstruction unchanged.",
            ),
            (
                "Shrinkage intensity should be selected using final test outcomes and still called untouched:",
                ["Yes", "Only for covariance", "No"],
                2,
                "Selection must remain inside the development process.",
            ),
            (
                "Eigenvalues 5, 3, and 2 imply first-component explained variance:",
                ["50%", "60%", "80%"],
                0,
                "The first component explains 5/(5+3+2)=.5 of total variance.",
            ),
            (
                "A smaller modeled portfolio variance after shrinkage establishes:",
                [
                    "Guaranteed lower realized risk",
                    "A different estimate under a stated target",
                    "Higher expected return",
                ],
                1,
                "Model changes require external validation.",
            ),
        ],
        [REG, FACTORS],
    )

    add(
        "3.23",
        6,
        "Panel data, fixed effects, and clustered inference",
        "Separate within-entity from between-entity variation and match covariance estimation to panel dependence.",
        "Panel data observe entities repeatedly over time. Entity fixed effects absorb time-invariant entity-specific components, so coefficients are identified from within-entity variation after the chosen transformation and other controls. Time effects absorb common date-specific components. A time-invariant regressor cannot be separately estimated alongside unrestricted entity effects.\n\nFixed effects do not automatically remove time-varying confounding, reverse causality, measurement error, or dynamic-panel bias. Random effects add assumptions about the relationship between entity components and regressors. Choose the model according to the estimand and defensible assumptions rather than whichever produces a smaller p-value.",
        "Firm A has x=[1,2] and y=[3,5]; firm B has x=[3,4] and y=[10,12]. Demeaning within each firm gives x deviations [−.5,.5] and y deviations [−1,1] for both. The within slope is 2. The level differences between firms are absorbed by their intercepts.\n\nRepeated observations within a firm may share disturbances. An entity-clustered covariance allows certain within-cluster dependence under its assumptions, but a tiny number of clusters provides weak asymptotic support. Two firms here demonstrate arithmetic, not reliable clustered inference.",
        "Check panel keys, duplicate entity-date rows, missing histories, and the source of identifying variation. Report entity/time effects, covariance clusters, and the number of independent clusters. Consider common shocks and two-way clustering when justified, with appropriate finite-sample care. Explain whether the question concerns within-firm changes or cross-firm differences; fixed effects can answer a different question from a pooled regression.",
        r"y_{it}-\bar y_i=\beta(x_{it}-\bar x_i)+(u_{it}-\bar u_i)",
        'cross = 4 * 0.5\nsquares = 4 * 0.25\nprint("Within-entity slope:", cross / squares)',
        "Two entities each have x deviations [−1,1] and y deviations [−3,3]. Compute the within slope and explain why entity fixed effects cannot identify a time-invariant entity attribute separately.",
        "Slope is 3. An entity-constant attribute is perfectly absorbed by the entity intercepts, leaving no within variation for a separate coefficient.",
        [
            (
                "Entity fixed effects primarily absorb:",
                ["Every future shock", "Time-invariant entity components", "All measurement error"],
                1,
                "Time-varying confounding can remain.",
            ),
            (
                "Two clusters are enough to assume standard cluster-asymptotic inference is reliable:",
                ["Always", "Only with many rows per cluster", "No"],
                2,
                "Independent cluster count matters for the reference approximation.",
            ),
            (
                "Within cross-product 12 and within squared-regressor sum 4 imply slope:",
                ["3", "4", "8"],
                0,
                "The within regression slope is 12/4=3.",
            ),
            (
                "A regressor constant within every entity is separately identified with entity fixed effects:",
                ["Always", "No, absent additional structure", "Only if measured precisely"],
                1,
                "Demeaning removes its variation.",
            ),
        ],
        [PANEL],
    )

    add(
        "3.24",
        6,
        "Instrumental variables and two-stage least squares",
        "Explain relevance, exclusion, and instrument exogeneity and interpret a simple IV estimate with weak-instrument caution.",
        "An instrument offers variation in an endogenous regressor that can support identification under explicit assumptions. Relevance links the instrument to the regressor after controls. Exclusion and exogeneity require that the instrument not affect the structural outcome through an omitted direct route or correlated disturbance, under the proposed model. These assumptions require substantive evidence; a strong first stage alone does not prove validity.\n\nTwo-stage least squares projects endogenous regressors onto instruments and exogenous controls, then estimates the structural relationship using the projected variation. Correct IV covariance accounts for this procedure. Naively treating fitted regressors as ordinary observed variables can give incorrect uncertainty.",
        "In a centered single-instrument setup, covariance between z and y is .6 and between z and x is .3, so the simple IV slope is 2. If the denominator were .03, the ratio would be 20, illustrating sensitivity to weak first-stage variation. This arithmetic does not identify a universal weak-instrument threshold.\n\nAn overidentification test, when available, assesses certain joint restrictions under assumptions. Passing it does not prove every instrument is valid, and exactly identified models lack that overidentifying comparison.",
        "Write an instrument argument covering timing, mechanism, exclusion threats, and the population affected. Report first-stage diagnostics, the instrument set, controls, covariance convention, and weak-instrument-robust inference when appropriate. Do not select instruments only because they produce the desired structural coefficient. Compare ordinary and IV estimates as evidence to interpret, not as an automatic instruction to trust whichever is larger.",
        r"\hat\beta_{IV}=\widehat{Cov}(z,y)/\widehat{Cov}(z,x)",
        'print("Simple IV estimate:", 0.6 / 0.3)\nprint("Weak-denominator sensitivity:", 0.6 / 0.03)',
        "Compute an IV ratio with covariances .4 and .2. Describe one plausible exclusion violation and why first-stage strength would not remove it.",
        "The ratio is 2. An instrument with a direct effect on the outcome or a shared omitted cause can violate validity even if it strongly predicts the regressor.",
        [
            (
                "A strong first stage proves instrument exclusion:",
                ["No", "Yes", "Only with robust errors"],
                0,
                "Relevance and validity are distinct requirements.",
            ),
            (
                "Weak instrument variation can make a ratio estimate:",
                [
                    "Automatically unbiased in finite samples",
                    "Stable by construction",
                    "Highly sensitive and poorly approximated by usual inference",
                ],
                2,
                "A small identifying denominator is a substantive warning.",
            ),
            (
                "Covariance z,y=.9 and covariance z,x=.3 imply simple IV slope:",
                [".3", "3", "2.7"],
                1,
                ".9/.3=3 in the stipulated single-instrument setup.",
            ),
            (
                "Passing an overidentification test proves all instruments valid:",
                ["Always", "Only if p>.05", "No"],
                2,
                "The test has assumptions and limited power against particular violations.",
            ),
        ],
        [IV],
    )

    add(
        "3.25",
        6,
        "Difference-in-differences and event studies",
        "Calculate a two-group treatment contrast and identify the counterfactual assumptions needed for a causal interpretation.",
        "Difference-in-differences compares outcome changes across treated and comparison groups. In the basic design, the untreated potential outcome trend for the treated group must be credibly represented by the comparison group's trend, conditional on the specified assumptions. Stable composition, no anticipatory response, and limited spillovers may also matter.\n\nA pre-trend graph is useful but cannot prove the counterfactual parallel-trends assumption. Few pre-periods or noisy estimates can conceal relevant differences. Event-study coefficients require a reference period and a clear treatment-timing convention. With staggered adoption and heterogeneous effects, a naive two-way fixed-effects coefficient can combine comparisons in misleading ways.",
        "The treated group's mean outcome rises from 10 to 14; the comparison group rises from 8 to 10. The difference-in-differences contrast is (14−10)−(10−8)=2. The raw treated change of 4 includes the shared change represented by the control group.\n\nIf a separate industry shock affects only treated entities at the treatment date, the contrast can include that shock as well as treatment. More precise standard errors do not repair the missing counterfactual.",
        "Specify treatment timing, eligible comparison entities, outcome measurement, and pre-period diagnostics before estimating. Match inference to the level of treatment assignment and dependence. Investigate anticipation, spillovers, and concurrent policies; show transparent group-time patterns. For staggered designs, use an estimator whose comparisons match the intended effect and heterogeneity assumptions. Report the descriptive contrast separately when causal assumptions are not credible.",
        r"DiD=(\bar y_{T,post}-\bar y_{T,pre})-(\bar y_{C,post}-\bar y_{C,pre})",
        'print("Difference-in-differences:", (14 - 10) - (10 - 8))',
        "Treated outcomes move 20→25 while comparison outcomes move 15→18. Compute the contrast and describe an event that would threaten its causal interpretation.",
        "The contrast is 2. A contemporaneous shock affecting only treated entities, anticipatory behavior, or spillovers can invalidate the intended counterfactual comparison.",
        [
            (
                "Parallel pre-trends prove future counterfactual parallel trends:",
                ["Yes", "No", "Only with a significant treatment coefficient"],
                1,
                "Observed pre-period evidence cannot prove the unobserved post-treatment counterfactual.",
            ),
            (
                "Treated change 5 and comparison change 2 imply DiD:",
                ["7", "2", "3"],
                2,
                "Subtract the comparison change from the treated change.",
            ),
            (
                "Staggered adoption with heterogeneous effects requires:",
                [
                    "Care about which group-time comparisons the estimator uses",
                    "No timing records",
                    "Only a larger pooled R-squared",
                ],
                0,
                "Some pooled specifications mix comparisons that do not match the intended estimand.",
            ),
            (
                "A treatment-specific concurrent shock is primarily a threat to:",
                [
                    "The table formatting",
                    "The counterfactual identification assumption",
                    "The ability to subtract means",
                ],
                1,
                "The contrast may capture the concurrent shock as well as treatment.",
            ),
        ],
        [
            PANEL,
            (
                "Callaway & Sant'Anna · Difference-in-Differences with Multiple Time Periods",
                "https://arxiv.org/abs/1803.09015",
            ),
        ],
    )

    add(
        "3.26",
        6,
        "Binary outcomes, likelihood, and probability forecasts",
        "Interpret logistic models and marginal effects while separating event probability from economic payoff.",
        "A binary outcome model specifies a probability rather than an unrestricted linear mean. Logistic regression maps a linear index through the logistic function, keeping fitted probabilities between zero and one. Coefficients are changes in log odds conditional on the included terms; they are not constant changes in probability.\n\nMaximum likelihood estimates parameters by evaluating how plausible the observed outcomes are under the model. Separation, rare events, dependence, and misspecification can impair estimates and uncertainty. Class weighting or oversampling changes the fitting objective and can require careful probability recalibration before deployment.",
        "A linear index of zero gives probability .5. Increasing it to log(3) gives probability .75 because the odds are three to one. With slope .8 at probability .5, the local derivative with respect to x is .8×.5×.5=.2 per unit of x under this simple specification. The derivative changes at other baseline probabilities.\n\nA .75 probability of a gain does not establish positive expected profit if losses are much larger than gains or costs consume the advantage. Predicting event frequency and deciding an allocation are separate problems.",
        "State the event definition, horizon, label availability, class prevalence, and decision threshold. Evaluate calibration, discrimination, proper scoring losses, and economic decision costs on later data. Inspect separation and convergence warnings rather than accepting enormous coefficients at face value. If repeated entity observations are used, choose an inference or predictive evaluation design that acknowledges their dependence.",
        r"p(x)=1/(1+e^{-x^\top\beta})",
        'import math\nprint("Probability at zero index:", 1 / (1 + math.exp(0)))\nprint("Probability at log-three index:", 1 / (1 + math.exp(-math.log(3))))\nprint("Local probability derivative:", 0.8 * 0.5 * 0.5)',
        "An event probability is .8. Compute its odds and explain why the same logit coefficient has different probability effects near .5 and .95.",
        "Odds are .8/.2=4. The derivative contains p(1−p), which is .25 at .5 but .0475 at .95, so a fixed slope has different local effects.",
        [
            (
                "A logit coefficient is a constant percentage-point effect on probability:",
                ["No", "Yes", "Only with one regressor"],
                0,
                "The nonlinear probability derivative depends on the starting probability.",
            ),
            ("Probability .75 corresponds to odds:", [".75", "3", "4"], 1, ".75/(1−.75)=3."),
            (
                "At p=.5 with slope 2, the local probability derivative is:",
                ["2", "1", ".5"],
                2,
                "2×.5×.5=.5 under the stated simple model.",
            ),
            (
                "A high gain probability alone establishes positive expected net profit:",
                ["No; payoff sizes and costs also matter", "Yes", "Only for a liquid stock"],
                0,
                "Event probability does not specify the payoff distribution.",
            ),
        ],
        [
            (
                "statsmodels contributors · Discrete dependent-variable models",
                "https://www.statsmodels.org/stable/discretemod.html",
            )
        ],
    )

    add(
        "3.4",
        7,
        "Risk and downside metrics",
        "Define empirical quantiles, expected shortfall, drawdown, and exceedance checks with explicit signs and horizons.",
        "Risk measures summarize different features of a return or loss distribution. Value at Risk is a quantile under a specified horizon and probability convention; it is not the largest possible loss. Expected shortfall summarizes losses in an explicitly defined tail. Maximum drawdown is a path-dependent peak-to-trough decline, so rearranging the same returns can change it.\n\nFinite samples make quantile conventions important. Interpolation, tied observations, and whether a threshold observation belongs to the tail can change the reported estimate. Use a documented convention and avoid representing a few historical observations as precise tail probabilities. Conditional and unconditional risk forecasts also answer different questions.",
        "A portfolio peaks at 200 and falls to 150, giving drawdown 150/200−1=−25%. Recovering from 150 to 200 requires a 33.33% gain because the return denominator changed.\n\nTake ordered losses [1,2,3,4,5,6,7,8,9,20]. Under the nearest-rank 90% quantile convention, VaR is the ninth observation, 9. Under a deliberately defined strictly-above-threshold tail, the mean is 20. Including the threshold would give 14.5; neither convention should be hidden behind an unexplained ES label.",
        "State loss signs, horizon, confidence level, sample size, quantile method, and tail inclusion rule. For a forecast, inspect exceedance frequency and clustering; a correct average count can hide failures concentrated during crises. Compare model risk with scenario analysis and liquidity constraints. A drawdown stop is an operating rule, not proof that realized losses cannot exceed the selected threshold.",
        r"DD_t=E_t/\max_{s\leq t}E_s-1",
        'print("Drawdown percent:", (150 / 200 - 1) * 100)\nprint("Required recovery percent:", (200 / 150 - 1) * 100)\nprint("Strict-tail mean loss:", 20)',
        "Compute drawdown and recovery gain after a peak of 100 falls to 80. Write a precise empirical VaR/ES convention before applying it to a sample.",
        "Drawdown is −20%; recovery requires 25%. Specify a quantile rule and whether boundary/tied observations enter the tail, plus horizon and loss sign.",
        [
            (
                "A fall from a peak of 200 to 150 has a drawdown of:",
                ["−25%", "−33.3%", "−50%"],
                0,
                "(150/200)−1=−25%; the original first answer remains compatible.",
            ),
            (
                "VaR is the maximum possible loss:",
                ["Always", "No", "Only at 95%"],
                1,
                "Losses can exceed the selected quantile.",
            ),
            (
                "Recovering from 80 to 100 requires a gain of:",
                ["20%", "80%", "25%"],
                2,
                "Recovering the original peak requires 100/80−1=.25.",
            ),
            (
                "Correct average exceedance frequency guarantees correct temporal risk behavior:",
                ["No; exceptions may cluster", "Yes", "Only over a year"],
                0,
                "Conditional calibration and dependence need additional checks.",
            ),
        ],
        [VOL, TIME],
    )

    add(
        "3.27",
        7,
        "Bootstrap uncertainty under dependence",
        "Choose a resampling unit that preserves relevant dependence and interpret bootstrap intervals within their assumptions.",
        "A bootstrap approximates an estimator's sampling behavior by resampling according to a declared mechanism. Independent row resampling is appropriate only when its independence approximation is defensible. Financial observations can be serially dependent, cross-sectionally linked, or grouped by entity, making the resampling unit central to the analysis.\n\nA moving-block bootstrap samples contiguous blocks to retain some local serial structure. Block length trades preservation of dependence against the effective number of independently drawn blocks. Very short blocks may erase dependence; very long blocks produce few distinct resamples. Structural changes and heavy tails can also limit a naive bootstrap interpretation.",
        "A 12-observation series is grouped into blocks of length three. Drawing four blocks yields a 12-observation resample under the chosen concatenation rule. Sampling individual rows would discard their within-block order. If overlapping blocks are allowed, possible starting positions and end handling must be specified.\n\nFor illustrative bootstrap estimates [.1,.2,.3,.4,.5], a nearest-rank 20% and 80% interval uses .1 and .4. This tiny set demonstrates quantile indexing only; a practical interval needs many draws and a justified resampling model.",
        "Set and record the random seed, block rule, number of draws, statistic, and interval method. Refit the full estimation procedure in each draw when that matches the target uncertainty; resampling only already fitted residual summaries can omit estimation steps. Compare block lengths and assess sensitivity. Never describe a bootstrap interval as distribution-free proof of future trading performance.",
        r"\hat\theta^{*(b)}=T(Data^{*(b)})",
        'print("Blocks in one resample:", 12 / 3)\nestimates = [0.1, 0.2, 0.3, 0.4, 0.5]\nprint("Illustrative nearest-rank interval:", estimates[0], estimates[3])',
        "Design a block-resampling plan for 120 monthly observations with candidate block lengths 3, 6, and 12. Explain which dependence and regime assumptions remain.",
        "Each draw assembles enough contiguous blocks to recover the desired sample length, with a declared boundary rule. Compare interval sensitivity across lengths; a block bootstrap still assumes the retained local structure is informative and does not automatically model regime shifts.",
        [
            (
                "Independent row resampling always preserves serial dependence:",
                ["Yes", "No", "Only with a fixed seed"],
                1,
                "Randomly permuting individual observations removes their local ordering.",
            ),
            (
                "Longer blocks necessarily make every bootstrap estimate more accurate:",
                [
                    "Always",
                    "Only for returns",
                    "No; they reduce the number of effectively distinct blocks",
                ],
                2,
                "Block length involves a dependence-versus-variation trade-off.",
            ),
            (
                "A 60-row resample assembled from length-five blocks requires:",
                ["12 blocks", "5 blocks", "300 blocks"],
                0,
                "60/5=12 before any boundary or truncation adjustments.",
            ),
            (
                "For parameter uncertainty, each bootstrap replicate may need to:",
                [
                    "Reuse every original fitted coefficient unchanged",
                    "Refit the relevant estimation procedure",
                    "Remove its random seed",
                ],
                1,
                "The resampling procedure must reproduce the estimator whose uncertainty is sought.",
            ),
        ],
        [
            (
                "arch contributors · Bootstrap methods",
                "https://arch.readthedocs.io/en/latest/bootstrap/bootstrap.html",
            )
        ],
    )

    add(
        "3.28",
        7,
        "Multiple testing and selection bias",
        "Account for a family of research attempts and distinguish family-wise error control from false-discovery control.",
        "Testing many variants creates opportunities for chance significance. The research family includes abandoned features, alternative universes, thresholds, samples, and model choices when they influenced selection. Reporting only the winner conceals the selection process. An untouched evaluation period helps, but repeatedly looking at it turns it into development data.\n\nBonferroni controls a family-wise error bound by dividing the family error level by the number of valid tests; it can be conservative, especially with dependent tests. False-discovery procedures target a different quantity and have their own dependence assumptions. Neither procedure repairs invalid individual p-values, data leakage, or an incorrectly defined research family.",
        "With 20 tests and family level .05, a Bonferroni threshold is .0025. A smallest raw p-value .01 is not significant under that rule, even though it is below .05. Under independence, the chance of at least one false rejection from twenty true nulls tested at .05 is 1−.95²⁰, about 64.15%.\n\nThis independence calculation is illustrative. Correlated strategy variants require more care; the observed number of trials is not automatically the number of independent trials, and hiding correlated trials is not a valid correction.",
        "Keep a research ledger with hypotheses, dates, tried variants, outcomes, and selection decisions. Predefine a small confirmatory family when possible, separate exploration from confirmation, and report effect sizes and uncertainty after selection. A deflated Sharpe or reality-check approach has additional distributional and dependence inputs; do not substitute a made-up trial discount for the specified method. Evaluate the chosen executable rule with costs after statistical selection.",
        r"\alpha_{individual}=\alpha_{family}/m",
        'print("Bonferroni threshold:", 0.05 / 20)\nprint("Independent family false-positive probability:", 1 - 0.95 ** 20)',
        "For ten tests at a family level .05, evaluate a smallest p-value .008 using Bonferroni. State why the number of unpublished variants matters.",
        "The threshold is .005, so .008 fails that rule. Unpublished attempts influenced the opportunity to select a chance winner and belong in the declared research history.",
        [
            (
                "Twenty tests with family level .05 give Bonferroni threshold:",
                [".0025", ".025", "1"],
                0,
                ".05/20=.0025.",
            ),
            (
                "False-discovery rate and family-wise error are:",
                [
                    "Identical targets",
                    "Different error criteria",
                    "Both measures of average return",
                ],
                1,
                "Choose the procedure according to the intended error guarantee and assumptions.",
            ),
            (
                "Multiple-testing correction repairs look-ahead bias:",
                ["Always", "Only for a small family", "No"],
                2,
                "Invalid information timing undermines the underlying tests themselves.",
            ),
            (
                "Abandoned variants can matter because:",
                [
                    "They contributed to the selection opportunity",
                    "They never affect a reported result",
                    "Only published code counts",
                ],
                0,
                "A research family's scope follows the actual selection process.",
            ),
        ],
        [MULTI],
    )

    add(
        "3.5",
        7,
        "Backtest traps and research hygiene",
        "Connect econometric evidence to an executable research design with point-in-time data, costs, and reproducible records.",
        "An econometric finding becomes a strategy hypothesis only after specifying how information turns into decisions and fills. A signal calculated from a completed close cannot execute at an earlier open. A historical universe assembled from today's survivors can exclude failed firms. Revised financial data can leak information that was unavailable at the original decision date.\n\nSeparate an effect estimate, a forecast, a portfolio rule, and an execution model. Each adds assumptions. A regression's positive coefficient does not specify a holding period, turnover budget, position size, or liquidity constraint. Keep these transformations explicit and evaluate the complete frozen rule on later observations.",
        "A gross strategy result is 8% over a stipulated period. Six one-way portfolio turnovers at 20 bps each consume 1.2%, leaving an approximate 6.8% before other omitted costs. If turnover rises to 20 equivalents, the same cost convention consumes 4%, leaving 4%. This additive approximation is a teaching decomposition; an actual ledger compounds dated cash flows and fees.\n\nA close signal with price 100 may first fill at a next open of 103. Using 100 because it makes the historical curve smoother can materially overstate performance.",
        "Write a preregistration-style record: data provenance, availability, transformation code, split manifests, model choice, target mapping, costs, fills, benchmark, and rejected variants. Preserve seeds and package versions for reproducibility. Stress an alternative fee model, delayed execution, missing data, and a market regime change. State the weakest assumption and a test that could falsify it. The capstone combines statistical inference with this operational evidence rather than accepting a chart alone.",
        r"r_{net}\approx r_{gross}-Turnover\times Cost_{one\ way}",
        'print("Approximate net return:", 0.08 - 6 * 0.002)\nprint("High-turnover net return:", 0.08 - 20 * 0.002)',
        "A rule earns 5% gross with eight one-way turnovers at 15 bps each. Compute the approximation and list three checks needed before interpreting it as a viable bot.",
        "Approximate net is 3.8%. Check signal/fill chronology, point-in-time universe/data, and realistic costs/liquidity, along with independent evaluation and deterministic risk limits.",
        [
            (
                "A close-derived signal should first execute at:",
                ["The same day’s open", "The next available tradable price", "The prior close"],
                1,
                "Execution follows information availability; the original first-answer key is retained.",
            ),
            (
                "Today's surviving securities automatically form an unbiased historical universe:",
                ["Yes", "Only for an index", "No"],
                2,
                "Survivorship can exclude historical failures and delistings.",
            ),
            (
                "Gross 6% minus ten turnovers at 10 bps each gives approximate net:",
                ["5%", "6%", "4%"],
                0,
                "Ten times .1% is 1% cost under the stated approximation.",
            ),
            (
                "A regression finding by itself fully specifies an executable strategy:",
                ["Yes", "No; decision and execution assumptions remain", "Only if significant"],
                1,
                "A coefficient does not define targets, timing, costs, or order behavior.",
            ),
        ],
        [FACTORS, MULTI],
    )

    add(
        "3.29",
        8,
        "Project: replicate a factor regression with HAC",
        "Run an actual regression pipeline and reconcile point estimates, covariance conventions, and held-out prediction errors.",
        "Download the [research lab](/course-assets/research/quant_research_lab.py), [environment file](/course-assets/research/requirements.txt), and [guide](/course-assets/research/README.md). The local project uses NumPy, SciPy, and statsmodels to fit a seeded synthetic factor model. The in-app worksheet below checks a small independent arithmetic case; it does not import those packages or fit the larger project.\n\nThe project preserves a chronological training/test split, fits OLS on training rows, and reports conventional and HAC uncertainty around the same coefficients. It predicts later asset outcomes from held-out factor observations, so that task is conditional return explanation rather than an ex-ante forecast of unknown future factors.",
        "For an independent check, x=[−1,0,1] and y=[−1,1,3] yield intercept 1 and slope 2. A future factor observation 2 gives fitted conditional outcome 5. If the realized outcome is 6, squared prediction error is 1. A training-mean baseline of 1 has squared error 25 on that case.\n\nThe larger noisy project produces imperfect estimates and different covariance estimates. Do not replace them with planted coefficients. Compare the reported estimates with the generating parameters as a simulation diagnostic, keeping finite-sample noise visible.",
        "Run the project twice with the same seed and environment and compare output. Alter only held-out outcomes: training coefficients must remain unchanged while evaluation losses change. Compare HAC lags without selecting the lag only for significance. Inspect rank deficiency, units, sample counts, and invalid values. Submit the fitted coefficients, covariance convention, split manifest, reproducibility command, and a paragraph explaining why synthetic planted exposure is not evidence of investment skill.",
        r"MSE_{test}=n_{test}^{-1}\sum_t(y_t-\hat y_t)^2",
        'prediction = 1 + 2 * 2\nprint("Project check prediction:", prediction)\nprint("Model squared error:", (6 - prediction) ** 2)\nprint("Baseline squared error:", (6 - 1) ** 2)',
        "Run the local factor project, preserve output, and change only the test outcomes in an independent experiment. Demonstrate unchanged training coefficients and changed loss.",
        "The fitting call must receive only the training slice. Predictions conditional on unchanged test factors remain identical; altered outcomes change scoring. Record that this is conditional explanation, not a forecast of unknown future factors.",
        [
            (
                "Using realized future factors to explain an asset's future return is automatically an ex-ante forecast:",
                ["No", "Yes", "Only if the factor coefficient is stable"],
                0,
                "The future factor values would also need to be available or forecast at decision time.",
            ),
            (
                "Changing only held-out outcomes should alter:",
                [
                    "Already fitted training coefficients",
                    "Evaluation errors",
                    "Training sample means",
                ],
                1,
                "Held-out outcomes enter scoring, not the training fit.",
            ),
            (
                "Prediction 4 and outcome 7 produce squared error:",
                ["3", "11", "9"],
                2,
                "Squared prediction error is (7−4)²=9.",
            ),
            (
                "Conventional and HAC results from the same OLS fit should share:",
                ["The point estimates", "Every standard error", "Every p-value"],
                0,
                "The covariance convention changes inference around the same coefficient fit.",
            ),
        ],
        [REG, DIAG],
    )

    add(
        "3.30",
        8,
        "Project: diagnose a synthetic long-run relation",
        "Fit and test a generated cointegrating relation while preserving integration assumptions and distinguishing known construction from estimated evidence.",
        "The downloadable research lab generates an integrated x path and a y path equal to 1.5x plus a stationary autoregressive disturbance. It estimates the levels relation, reports an Engle–Granger test, and fits simple spread dynamics. The generating design supplies a controlled case; the finite-sample estimates and test output still need interpretation.\n\nThis project is a statistical diagnostic, not a pair-trading backtest. It does not model short availability, both-leg fills, fees, or trading permissions. The bot course's advanced pairs lesson uses this distinction to explain what a statistical relationship leaves unresolved.",
        "Suppose an estimated relation is y=.5+1.4x+s. At x=20 and y=29.5, the residual is 1. If the estimated residual AR coefficient is .6, the model-implied half-life is log(.5)/log(.6), about 1.357 observation periods. These values are a separate hand-check fixture, not promised outputs of the seeded estimation.\n\nAn alternative dataset that inserts a permanent shift in the hedge relationship can invalidate a formerly stable model. A full-sample fit may average over this change and disguise the period in which the trading premise failed.",
        "Save the generating seed, sample span, deterministic test terms, lag choices, estimated hedge units, and diagnostics. Compare early and late subsamples and inspect a deliberately broken relation. Explain the distinction between rejecting no cointegration in a simulation and establishing an economic trade. A convincing project includes a negative control or failure case, not just the configuration designed to pass.",
        r"s_t=y_t-\hat\alpha-\hat\beta x_t",
        'import math\nprint("Project spread residual:", 29.5 - 0.5 - 1.4 * 20)\nprint("Project spread half-life:", math.log(0.5) / math.log(0.6))',
        "Run the time-series project and then alter the second half's hedge coefficient in a separate fixture. Compare estimates and explain why a single full-sample result can be misleading.",
        "A regime change can alter the long-run relation and residual behavior. Retain both subperiod diagnostics and the altered-data definition; do not declare a stable trading equilibrium from a pooled average alone.",
        [
            (
                "A planted cointegrating simulation is evidence that real pairs are profitable:",
                ["Yes", "No", "Only when the p-value is small"],
                1,
                "The fixture tests statistical behavior under a known design, not real execution economics.",
            ),
            (
                "A negative-control dataset is useful because it:",
                [
                    "Guarantees every test passes",
                    "Replaces source metadata",
                    "Challenges whether the method distinguishes a failed premise",
                ],
                2,
                "A diagnostic should also be examined where its intended relation is absent or broken.",
            ),
            (
                "With y=22, x=10, intercept 1, and hedge slope 2, the residual is:",
                ["1", "2", "3"],
                0,
                "The fitted levels residual is 22−1−2×10=1.",
            ),
            (
                "A structural shift can be hidden by:",
                [
                    "A clearly labeled subperiod comparison",
                    "A pooled estimate averaging incompatible regimes",
                    "Retaining the raw data",
                ],
                1,
                "Full-sample averages can obscure when the model stopped describing the data.",
            ),
        ],
        [COINT, TIME],
    )

    add(
        "3.31",
        8,
        "Project: risk model and allocation review",
        "Compare portfolio risk estimates and volatility recursions with clear model boundaries and adverse-case checks.",
        "The local research project includes an explicit GARCH recursion with stipulated parameters and a covariance-shrinkage comparison. These components calculate model implications; they do not estimate GARCH parameters or prove that an optimized portfolio will outperform. Keep estimation, forecasting, allocation, and execution as separate artifacts.\n\nA useful risk review examines the same holdings under several plausible input models. Compare sample covariance, a disclosed structured target, and a correlation stress. Report how concentration and expected turnover change when the allocation responds to those estimates. A lower model variance may simply reflect a more optimistic assumption.",
        "Two equal-weight assets have variances .04 and .09 and covariance .018. Portfolio variance is .0415. Shrinking covariance halfway toward zero gives .009 and estimated variance .037. If covariance rises to .06 under perfect positive correlation at these volatilities, variance becomes .0625 and volatility .25.\n\nFor an independent volatility check, omega=.01, alpha=.1, beta=.8, squared shock .04, and prior variance .09 give next variance .086. The number is a conditional estimate in squared units, not a maximum possible return loss.",
        "Include a covariance validity check, a unit-scale check, and a stress that undermines the preferred allocation. Document parameters chosen in advance and any data used to estimate them. Verify positive variance forecasts before computing loss metrics. Submit a review memo that distinguishes a changed estimate from a changed actual portfolio and states what evidence would justify altering a trading risk budget.",
        r"\hat\sigma_p=\sqrt{w^\top\hat\Sigma w}",
        'import math\nprint("Sample portfolio variance:", 0.25 * 0.04 + 0.25 * 0.09 + 0.5 * 0.018)\nprint("Shrunk portfolio variance:", 0.25 * 0.04 + 0.25 * 0.09 + 0.5 * 0.009)\nprint("Correlation-stress volatility:", math.sqrt(0.25 * 0.04 + 0.25 * 0.09 + 0.5 * 0.06))',
        "Reproduce all three risk estimates and identify an input change that could reverse your preferred allocation. Explain whether any result represents a guaranteed loss bound.",
        "Variances are .0415, .037, and .0625; stressed volatility is .25. Changing correlations, volatility, or concentration constraints can alter the allocation. None is a guaranteed maximum loss.",
        [
            (
                "Covariance shrinkage physically reduces the portfolio's market risk at the instant it is calculated:",
                ["No; it changes the estimate", "Yes", "Only with equal weights"],
                0,
                "Actual holdings and future market behavior remain separate from the estimator.",
            ),
            (
                "A variance forecast must be interpreted in:",
                [
                    "Share counts",
                    "Squared return units at its specified horizon",
                    "Unspecified annual dollars",
                ],
                1,
                "Units and horizon determine the numerical meaning.",
            ),
            (
                "Portfolio variance .0625 implies volatility:",
                [".0625", ".5", ".25"],
                2,
                "Take the square root of variance.",
            ),
            (
                "A credible allocation review should include:",
                [
                    "An adverse assumption that challenges the chosen model",
                    "Only the minimum in-sample variance",
                    "Only the most favorable chart",
                ],
                0,
                "Sensitivity exposes dependence on uncertain inputs.",
            ),
        ],
        [VOL, FACTORS],
    )

    add(
        "3.32",
        8,
        "Capstone: the Cedar econometric research dossier",
        "Deliver a reproducible study that connects an estimand, identification assumptions, statistical inference, and an investment decision boundary.",
        "Choose one primary question: a conditional factor explanation, a dated forecast, a long-run relation, or a credible causal contrast. State the estimand and avoid combining these into an undefined claim of alpha. Assemble the data dictionary, as-of rules, model specification, diagnostics, covariance convention, selection history, and independent evaluation.\n\nRun the downloadable project as a reproducibility baseline and add one self-designed sensitivity or negative-control experiment. All default data are synthetic. A later study using real observations needs a lawful data source, point-in-time metadata, and its own evaluation; changing the dataset is not a cosmetic substitution.",
        "Cedar reports a coefficient .4 with HAC standard error .25, a large-sample interval [−.09,.89], and model MSE .8 against baseline MSE 1. The conditional prediction improvement is 20% under that loss comparison, while the parameter interval includes zero. Neither fact alone establishes a causal effect or a profitable strategy.\n\nThe study must explain how these different evidence types relate to its original question. If the model used realized future factor returns, its conditional explanatory task cannot silently become an ex-ante trading forecast.",
        "Self-assess 100 points: question and estimand 15, data/provenance 20, estimation and diagnostics 20, uncertainty and selection 20, independent evaluation 15, and reproducibility/decision memo 10. Require at least 80 and no unresolved information leak, unit inconsistency, invalid inference convention, or misrepresented data source. The automatic final assesses conceptual transfer; it does not grade the written dossier or certify a real-world investment result. Conclude with the strongest supported claim, the largest unresolved limitation, and the next falsifying experiment.",
        r"R^2_{OOS}=1-MSE_{model}/MSE_{baseline}",
        'print("Capstone t statistic:", 0.4 / 0.25)\nprint("Capstone approximate interval:", 0.4 - 1.96 * 0.25, 0.4 + 1.96 * 0.25)\nprint("Capstone OOS improvement:", 1 - 0.8 / 1)\nprint("Rubric total:", 15 + 20 + 20 + 20 + 15 + 10)',
        "Submit the estimand, source/data dictionary, model and split manifests, diagnostics, uncertainty/selection report, project output, adverse experiment, and one-page decision. Complete the rubric and identify any mandatory failure.",
        "A valid packet distinguishes description, prediction, and causality; reproduces code and data timing; reports assumptions and uncertainty; and evaluates the declared task. An 80+ score cannot override a critical leak or false data claim. The automatic exam is separate from this self-assessed dossier.",
        [
            (
                "A capstone with a high score but unresolved test leakage should be:",
                [
                    "Accepted if its chart rises",
                    "Rejected until the critical failure is resolved",
                    "Accepted if the model is complex",
                ],
                1,
                "Mandatory evidence conditions apply in addition to rubric points.",
            ),
            (
                "The concept exam automatically verifies the submitted local project:",
                ["Yes", "Only its code syntax", "No; the dossier requires separate review"],
                2,
                "Multiple-choice grading does not inspect the research artifact.",
            ),
            (
                "Model MSE .6 and baseline MSE .8 imply OOS improvement:",
                ["25%", "20%", "75%"],
                0,
                "Relative loss improvement is 1−.6/.8=.25.",
            ),
            (
                "The strongest research conclusion should match:",
                [
                    "The most exciting possible interpretation",
                    "The estimand and evidence actually evaluated",
                    "The largest coefficient",
                ],
                1,
                "Claims must remain within the study's identification and evaluation scope.",
            ),
        ],
        [REG, TIME, MULTI],
    )

    parts = [
        (
            "Questions, data, and least squares",
            "Define the estimand, align financial observations, derive OLS, and diagnose multiple regression.",
        ),
        (
            "Inference and specification",
            "Confidence statements, heteroskedasticity, HAC dependence, and endogeneity.",
        ),
        (
            "Dynamic time-series models",
            "Stationarity, ARIMA forecasts, model selection, and VAR systems.",
        ),
        (
            "Long-run relations and volatility",
            "Cointegration, error correction, GARCH, asymmetric risk, and forecast loss.",
        ),
        (
            "Factors and portfolio estimation",
            "Factor definitions, alpha interpretation, diversification, shrinkage, and PCA.",
        ),
        (
            "Panel and causal analysis",
            "Fixed effects, instruments, difference-in-differences, and binary outcomes.",
        ),
        (
            "Risk and research credibility",
            "Tail conventions, dependent bootstrap, multiple testing, and executable evaluation.",
        ),
        (
            "Replication projects and capstone",
            "Fit regressions, diagnose time series, review risk models, and defend a research dossier.",
        ),
    ]
    checkpoints = checkpoints_for(modules, parts, 7)
    return finish(
        {
            "id": "econometrics",
            "number": 3,
            "title": "Financial econometrics & factor models",
            "description": "A complete applied course in regression, time series, volatility, factor investing, panel data, and causal research, with reproducible projects and a research capstone.",
            "source": "Original Quanta course · primary statistical documentation and factor research",
            "level": "Intermediate → advanced",
            "icon": "factors",
            "studyType": "applied",
            "modules": modules,
            "prerequisites": "Basic probability, algebra, and Python. Study Quantitative Investment Analysis first or use it alongside this course. Guided worksheets run in the app; the downloadable project uses Python with NumPy, SciPy, and statsmodels.",
            "outcomes": [
                "Define an estimand and build point-in-time financial datasets.",
                "Fit and diagnose regression with explicit robust-inference conventions.",
                "Evaluate stationarity, cointegration, forecasts, and conditional volatility.",
                "Interpret factor exposures and estimated portfolio risk.",
                "Assess panel, instrumental-variable, and quasi-experimental assumptions.",
                "Produce a reproducible, selection-aware research dossier.",
            ],
            "readingGuide": "Eight units and 32 original lessons, each with two practice items, a worked calculation, references, and a notebook assignment. Seven checkpoints lead to a 32-question final. The downloadable project fits actual OLS/HAC and time-series models on synthetic data, while the written capstone is self-assessed separately.",
            "parts": [
                {"id": str(i), "title": title, "description": description}
                for i, (title, description) in enumerate(parts, 1)
            ],
            "references": [
                {"title": title, "url": url}
                for title, url in [REG, DIAG, TIME, COINT, VOL, FACTORS, PANEL, IV]
            ],
            "resources": [
                {
                    "title": "Download the quantitative research lab",
                    "url": "/course-assets/research/quant_research_lab.py",
                },
                {
                    "title": "Download the research project guide",
                    "url": "/course-assets/research/README.md",
                },
                {
                    "title": "Download the project environment",
                    "url": "/course-assets/research/requirements.txt",
                },
            ],
        },
        checkpoints,
    )
