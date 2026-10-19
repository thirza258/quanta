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
    # -------------------------------------------------------------------------
    # UNIT 1: QUESTIONS, DATA, AND LEAST SQUARES
    # -------------------------------------------------------------------------

    add(
        "3.6",
        1,
        "An econometric question and its estimand",
        "Separate description, prediction, and causal explanation before choosing a regression.",
        r"""In financial econometrics, rigorous empirical research begins not with software code or a table of regressors, but by defining an exact **estimand**: the specific mathematical and economic quantity the study aims to uncover. Analysts routinely run identical linear regression commands ($y = X\beta + u$) to answer three fundamentally different classes of questions:

1. **Descriptive Summarization**: What is the historical empirical association between an asset's excess return and a risk factor within an observed sample? Descriptive estimands quantify sample moments, correlations, and partial linear projections without claiming that the pattern will persist into future periods or survive corporate policy changes.
2. **Predictive Forecasting**: Given market observations available strictly at time $t$ ($X_t$), what is the conditional expectation of future returns at horizon $t+h$ ($E[y_{t+h}|X_t]$)? Predictive estimands are judged exclusively by their out-of-sample forecast accuracy, loss functions (such as Mean Squared Error), and post-cost trading viability.
3. **Causal Explanation (Structural Analysis)**: If a corporate executive, policymaker, or central bank actively intervenes to change variable $X$ by $\Delta X$, what will be the resulting change in outcome $y$? Causal estimands require formal identification strategies (such as instrumental variables, difference-in-differences, or exogenous shocks) to rule out confounding and selection bias.

Conflating these three objectives is among the most pervasive errors in empirical quantitative finance. A regression slope ($\hat{\beta}$) estimated with high precision describes an in-sample partial association; it does **not** prove that allocating capital to the factor will generate forward-looking alpha, nor does it imply that corporate management can engineer a higher valuation by manipulating that accounting variable.

Every research specification must establish a formal research charter declaring:
- The target population (e.g., all liquid equities listed on the exchange, excluding OTC pink sheets).
- The observational unit and frequency (e.g., firm-month pairs).
- The information timing cutoff ($t_{available} \le t_{decision}$).
- The exact conditioning set and mathematical loss metric.""",
        r"""The quantitative research desk at Cedar Capital evaluates a monthly factor model relating a single stock's excess return ($y_t$) to a broad market equity factor ($x_t$):

$$y_t = \alpha + \beta x_t + u_t$$

The estimated parameters obtained from sixty historical months are an intercept $\hat{\alpha} = 0.10$ percentage points and a slope coefficient $\hat{\beta} = 1.20$.

1. **Interpret the estimated slope ($\hat{\beta} = 1.20$)**:
   - For every $1.00$ percentage point increase in the market factor return, the asset's expected excess return increases by $1.20$ percentage points, *holding the model specification and sample fixed*.
   - This estimate represents a conditional linear association. It does not prove that an investor can force a higher return by "choosing" higher market exposure, nor does it guarantee that the sensitivity will remain $1.20$ during market stress.
2. **Calculate the fitted conditional expectation**:
   Suppose the market factor generates an excess return of $x_t = 2.00$ percentage points in an evaluation month:
   $$\hat{y}_t = \hat{\alpha} + \hat{\beta} x_t = 0.10 + (1.20 \times 2.00) = 0.10 + 2.40 = 2.50 \text{ percentage points}$$
3. **Contrast fitted expectation against realized reality**:
   The fitted conditional mean is $+2.50$ percentage points. If the stock actually realizes an excess return of $+3.10$ percentage points, the unobserved idiosyncratic disturbance is:
   $$\hat{u}_t = y_t - \hat{y}_t = 3.10 - 2.50 = +0.60 \text{ percentage points}$$
   The intercept $\hat{\alpha} = 0.10$ is merely the fitted mean of the residuals when $x_t = 0$; it is not a guaranteed risk-free profit or proof of investment skill.""",
        r"""Before viewing the held-out test data or calculating performance metrics:
- **Write a preregistered research charter**: Define the research question, eligible universe filters, handling of delistings, currency denomination, and econometric estimator before opening the test partition.
- **Separate parameter uncertainty from future outcome variance**: A statistically narrow confidence interval for $\beta$ (e.g., $1.20 \pm 0.05$) does not mean future returns will fall within a narrow band. Realized outcomes are subject to the full variance of the idiosyncratic disturbance $Var(u_t) = \sigma^2$.
- **Avoid semantic upgrades**: Never rebrand a descriptive regression as a "predictive signal" without out-of-sample walk-forward testing, and never label a predictive relationship as "causal" without a verified identification design.""",
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
        r"""In financial econometrics, empirical models fail far more frequently from flawed data alignment than from sophisticated mathematical errors. A financial dataset is not merely a generic matrix of floating-point numbers; it represents an immutable chronological sequence where every observation must respect economic causality and physical information availability.

When constructing a research-grade financial dataset, the quantitative researcher must address four foundational data engineering requirements:

1. **Exact Return Definitions and Compounding Conventions**:
   - **Simple Discrete Returns**: $R_t = \frac{P_t + D_t - P_{t-1}}{P_{t-1}}$, essential for cross-sectional portfolio weighting because portfolio return is the linear combination of asset returns: $R_p = \sum w_i R_i$.
   - **Continuously Compounded Log Returns**: $r_t = \ln(1 + R_t) = \ln(P_t / P_{t-1})$, mathematically convenient for multi-period temporal aggregation: $r_{0 \to T} = \sum_{t=1}^T r_t$. However, log returns do not aggregate linearly across assets ($\ln(\sum w_i e^{r_i}) \neq \sum w_i r_i$).
2. **Synchronized Frequency and Units**:
   - An analyst cannot subtract an annualized 3-month Treasury bill yield ($4.8\%$ per annum) directly from a monthly equity return ($+2.4\%$). The risk-free rate must be converted to an effective monthly rate:
     $$r_{f, monthly} = (1 + r_{f, annual})^{1/12} - 1 \quad \text{or approximately } \frac{r_{f, annual}}{12}$$
   - Consistent decimal vs. percentage point units: If asset returns are stored in decimals ($0.024$ for $2.4\%$) while a commercial factor feed reports values in percentage points ($1.5$ for $1.5\%$), combining them without normalization distorts factor exposures by a factor of 100!
3. **Point-in-Time Availability and Corporate Filing Lags**:
   - A corporate balance sheet for the fiscal year ending December 31 is not physically available on December 31. Public filing via SEC 10-K occurs weeks or months later (e.g., March 15). Backtesting an investment rebalance on February 1 using December 31 numbers introduces severe **look-ahead bias**.
4. **Missing Data and Selection Conventions**:
   - A missing return from a trading suspension or holiday is **not** a zero return. Forward-filling prices fabricates artificial zero returns and depresses volatility estimates, biasing beta toward zero.""",
        r"""Cedar Capital's risk analyst constructs a monthly excess return series for an equity asset over an evaluation period:
- Asset raw gross monthly return: $+2.4\%$ ($R_{asset} = 0.024$).
- Monthly risk-free rate (cash return): $+0.3\%$ ($R_{free} = 0.003$).
- Value factor spread reported by a data vendor: $1.5$ percentage points.

1. **Calculate normalized excess return**:
   $$R^{excess}_t = R^{asset}_t - R^{free}_t = 0.024 - 0.003 = 0.021 \text{ (or } 2.1\%)$$
2. **Normalize the factor regressor**:
   The vendor data reports $1.5$ in percentage points. To match the decimal convention of the dependent variable, scale by 100:
   $$F_{normalized} = \frac{1.5}{100} = 0.015$$
   Failing to normalize would cause the regression slope on the factor to be shrunk by 100-fold, creating invalid inferences.
3. **Audit merge cardinality and sample attrition**:
   Out of $120$ calendar months in the study window:
   - $10$ months lack published factor data (e.g., vendor history begins later).
   - $5$ separate months lack valid asset pricing due to trading suspensions.
   Under a declared complete-case analysis, the retained sample size is:
   $$n_{complete} = 120 - 10 - 5 = 105 \text{ valid months}$$
   The analyst must document whether the 5 suspended months were driven by financial distress, because dropping them can induce survivorship selection bias.""",
        r"""To ensure reproducibility and eliminate look-ahead contamination:
- **Build an explicit data dictionary**: Store field names, sources, publication date timestamps ($t_{filing}$), revision IDs, currency symbols, and adjustment factors (splits and dividends).
- **Audit merge integrity**: Assert uniqueness on `(security_id, date)` primary keys prior to joining fundamental tables to pricing series. Unintended one-to-many joins duplicate rows and corrupt regression weighting.
- **Maintain a frozen historical ingestion pipeline**: Store raw vendor data files with cryptographic SHA-256 hashes. Never allow automated dynamic web scraping to overwrite historical records without version control.""",
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
        r"""Ordinary Least Squares (OLS) is the mathematical bedrock of linear econometric modeling. Given $n$ paired observations of an outcome variable $y_i$ and an explanatory regressor $x_i$, OLS selects the intercept $\hat{\alpha}$ and slope $\hat{\beta}$ that minimize the empirical **Sum of Squared Residuals (SSR)**:

$$S(\hat{\alpha}, \hat{\beta}) = \sum_{i=1}^n \hat{u}_i^2 = \sum_{i=1}^n \left(y_i - \hat{\alpha} - \hat{\beta} x_i\right)^2$$

Taking first-order partial derivatives with respect to $\hat{\alpha}$ and $\hat{\beta}$ and setting them to zero produces the fundamental **normal equations**:

$$\frac{\partial S}{\partial \hat{\alpha}} = -2 \sum_{i=1}^n \left(y_i - \hat{\alpha} - \hat{\beta} x_i\right) = 0 \implies \sum_{i=1}^n \hat{u}_i = 0$$

$$\frac{\partial S}{\partial \hat{\beta}} = -2 \sum_{i=1}^n x_i \left(y_i - \hat{\alpha} - \hat{\beta} x_i\right) = 0 \implies \sum_{i=1}^n x_i \hat{u}_i = 0$$

Solving these equations algebraically yields the classical OLS estimators:

$$\hat{\beta} = \frac{\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^n (x_i - \bar{x})^2} = \frac{\widehat{Cov}(x, y)}{\widehat{Var}(x)}$$

$$\hat{\alpha} = \bar{y} - \hat{\beta} \bar{x}$$

These first-order conditions guarantee two purely algebraic properties for any OLS regression containing an intercept:
1. The residuals sum to exactly zero ($\sum \hat{u}_i = 0$), so the average residual is identically zero ($\bar{\hat{u}} = 0$).
2. The sample covariance between the regressor $x$ and the residuals $\hat{u}$ is identically zero ($\sum x_i \hat{u}_i = 0$).
3. The regression line passes through the point of sample means $(\bar{x}, \bar{y})$.

**The Gauss-Markov Theorem**: Under the classical assumptions of linearity, strict exogeneity ($E[u_i|X] = 0$), no perfect multicollinearity, homoskedasticity ($Var(u_i|X) = \sigma^2$), and no autocorrelation ($Cov(u_i, u_j|X) = 0$), OLS is the **Best Linear Unbiased Estimator (BLUE)**—possessing minimum variance among all linear unbiased estimators.

However, in matrix notation for multiple regressors ($\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \mathbf{u}$), solving the normal equations:
$$\hat{\boldsymbol{\beta}} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$$
requires the design matrix $\mathbf{X}$ to have full column rank ($rank(\mathbf{X}) = k + 1$). If regressors are perfectly collinear, $(\mathbf{X}^T\mathbf{X})$ is singular, and unique coefficients cannot be computed.""",
        r"""To illustrate the exact mechanics, examine a small inspection sample with three paired observations:
$$\mathbf{x} = [1, 2, 3], \quad \mathbf{y} = [2, 3, 5]$$

1. **Compute sample means**:
   $$\bar{x} = \frac{1 + 2 + 3}{3} = 2.0, \quad \bar{y} = \frac{2 + 3 + 5}{3} = \frac{10}{3} \approx 3.3333$$
2. **Compute centered deviations and sums**:
   - Centered $x$: $(1 - 2) = -1$, $(2 - 2) = 0$, $(3 - 2) = +1$.
   - Centered $y$: $(2 - 10/3) = -4/3$, $(3 - 10/3) = -1/3$, $(5 - 10/3) = +5/3$.
   - Cross-product sum:
     $$\sum (x_i - \bar{x})(y_i - \bar{y}) = (-1 \times -4/3) + (0 \times -1/3) + (1 \times 5/3) = \frac{4}{3} + 0 + \frac{5}{3} = \frac{9}{3} = 3.0$$
   - Squared regressor sum:
     $$\sum (x_i - \bar{x})^2 = (-1)^2 + 0^2 + 1^2 = 1 + 0 + 1 = 2.0$$
3. **Calculate OLS slope and intercept**:
   $$\hat{\beta} = \frac{3.0}{2.0} = 1.50$$
   $$\hat{\alpha} = \bar{y} - \hat{\beta}\bar{x} = \frac{10}{3} - (1.50 \times 2) = \frac{10}{3} - 3 = \frac{1}{3} \approx 0.3333$$
4. **Calculate fitted values and residuals**:
   - $\hat{y}_1 = 1/3 + 1.5(1) = 11/6 \approx 1.8333 \implies \hat{u}_1 = 2 - 11/6 = +1/6$
   - $\hat{y}_2 = 1/3 + 1.5(2) = 20/6 \approx 3.3333 \implies \hat{u}_2 = 3 - 20/6 = -2/6 = -1/3$
   - $\hat{y}_3 = 1/3 + 1.5(3) = 29/6 \approx 4.8333 \implies \hat{u}_3 = 5 - 29/6 = +1/6$
   - Sum of residuals: $+1/6 - 2/6 + 1/6 = 0.0$ (verified!).
   - Sum of squared residuals: $(1/6)^2 + (-2/6)^2 + (1/6)^2 = \frac{1 + 4 + 1}{36} = \frac{6}{36} = \frac{1}{6} \approx 0.1667$.""",
        r"""In production quantitative implementations:
- **Numerical stability over explicit inversion**: Never compute $(\mathbf{X}^T\mathbf{X})^{-1}$ directly in software; explicit matrix inversion is numerically unstable for ill-conditioned financial data. Use QR decomposition or Singular Value Decomposition (SVD), as implemented in `numpy.linalg.lstsq` and `statsmodels`.
- **Verify residual orthogonality**: Always check that $\mathbf{X}^T\hat{\mathbf{u}} \approx 0$ within floating-point machine precision.
- **Do not confuse in-sample fit with trading edge**: Achieving $R^2 = 1.0$ on three data points proves only algebraic fitting, not future return predictability or actionable alpha.""",
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
        r"""Multiple linear regression extends bivariate OLS by modeling an outcome variable $y$ conditional on a vector of $k$ explanatory variables:

$$y_i = \beta_0 + \beta_1 x_{1i} + \beta_2 x_{2i} + \cdots + \beta_k x_{ki} + u_i$$

The economic interpretation of an individual coefficient $\beta_j$ is the **partial derivative** $\frac{\partial E[y|X]}{\partial x_j}$: the expected change in $y$ associated with a one-unit increase in $x_j$, holding all other regressors constant ($ceteris\ paribus$).

By the **Frisch-Waugh-Lovell (FWL) Theorem**, this partial slope can be obtained identically through a two-step residualized regression:
1. Regress $y$ on all regressors except $x_j$, collecting residuals $\tilde{y}$.
2. Regress $x_j$ on all other regressors, collecting residuals $\tilde{x}_j$.
3. Regressing $\tilde{y}$ on $\tilde{x}_j$ yields the exact multiple regression slope $\hat{\beta}_j = \frac{\sum \tilde{x}_{ji} \tilde{y}_i}{\sum \tilde{x}_{ji}^2}$.

This highlights that $\hat{\beta}_j$ uses only the *unique, orthogonal information* in $x_j$ that cannot be explained by the other included variables.

**Multicollinearity and Variance Inflation**:
When explanatory variables are linearly correlated with one another, their unique information shrinks. The variance of the estimated slope explodes according to the **Variance Inflation Factor (VIF)**:

$$Var(\hat{\beta}_j) = \frac{\sigma^2}{\sum_{i=1}^n (x_{ji} - \bar{x}_j)^2} \times \text{VIF}_j, \quad \text{where } \text{VIF}_j = \frac{1}{1 - R_j^2}$$

Here, $R_j^2$ is the auxiliary coefficient of determination obtained from regressing regressor $x_j$ on all other $k-1$ explanatory variables.
- When $R_j^2 = 0$ (orthogonal regressors), $\text{VIF}_j = 1$ (no variance inflation).
- When $R_j^2 = 0.80$, $\text{VIF}_j = \frac{1}{1 - 0.80} = 5.0$, meaning sampling variance is inflated by 500%, and the standard error is inflated by $\sqrt{5} \approx 2.236$.
- Multicollinearity does not bias OLS point estimates, but it inflates standard errors, causing $t$-statistics to collapse and rendering individual coefficients statistically insignificant even when the overall regression $R^2$ and $F$-statistic are large.

**Goodness-of-Fit and Diagnostics**:
Adding any regressor monotonically increases unadjusted $R^2$. Analysts rely on **adjusted $R^2$** ($\bar{R}^2$), which penalizes model complexity:
$$\bar{R}^2 = 1 - \left[\frac{SSR / (n - k - 1)}{SST / (n - 1)}\right]$$

Additionally, high-leverage points ($h_{ii}$ from hat matrix $\mathbf{H} = \mathbf{X}(\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T$) and Cook's Distance ($D_i$) identify influential observations that exert disproportionate pull on the regression plane.""",
        r"""Cedar Capital investigates a multi-factor risk model where an auxiliary regression of the momentum factor on the market, size, and value factors yields an auxiliary $R_j^2 = 0.80$.

1. **Calculate the Variance Inflation Factor (VIF)**:
   $$\text{VIF}_j = \frac{1}{1 - R_j^2} = \frac{1}{1 - 0.80} = \frac{1}{0.20} = 5.0$$
2. **Calculate the standard-error inflation multiplier**:
   $$\text{SE Multiplier} = \sqrt{\text{VIF}_j} = \sqrt{5.0} \approx 2.236068$$
   Due to collinearity with the other three factors, the standard error of the momentum slope is more than double ($2.236\times$) what it would be in an orthogonal experimental design.
3. **Decompose total variance and adjusted fit**:
   Suppose total sum of squares is $SST = 100$ and the fitted model explains $SSR = 80$ with $n = 105$ observations and $k = 4$ factors:
   $$R^2 = \frac{SSR}{SST} = \frac{80}{100} = 0.800$$
   $$\bar{R}^2 = 1 - \left[\frac{(100 - 80) / (105 - 4 - 1)}{100 / (105 - 1)}\right] = 1 - \left[\frac{20 / 100}{100 / 104}\right] = 1 - \frac{0.20}{0.9615} \approx 0.792$$
   If an analyst adds an irrelevant noise variable that reduces residual sum of squares by only $0.01$, unadjusted $R^2$ rises, but adjusted $\bar{R}^2$ decreases due to degrees-of-freedom penalty.""",
        r"""When conducting multiple regression diagnostics:
- **Do not treat VIF cutoffs (e.g., VIF > 10) as automatic deletion rules**: If a variable is theoretically essential to prevent omitted-variable bias (such as market beta in an asset pricing regression), removing it simply because of collinearity with a sector factor introduces fatal bias into the remaining coefficients.
- **Inspect residuals against fitted values**: Look for non-random funnel patterns (heteroskedasticity) or curvature (non-linear misspecification).
- **Audit influential crisis observations**: Never delete extreme observations (such as October 1987 or March 2020) merely to improve statistical significance. Investigate whether the crisis contains genuine risk factor dynamics.""",
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

    # -------------------------------------------------------------------------
    # UNIT 2: INFERENCE AND SPECIFICATION
    # -------------------------------------------------------------------------

    add(
        "3.9",
        2,
        "Sampling uncertainty and joint hypotheses",
        "Distinguish confidence intervals, prediction intervals, t tests, and joint restrictions with explicit reference distributions.",
        r"""In financial econometrics, parameter point estimates ($\hat{\boldsymbol{\beta}}$) are random variables whose realization depends on the specific sample drawn from the underlying data-generating process. To make rigorous statistical statements about unobserved population parameters ($\boldsymbol{\beta}$), analysts must quantify sampling uncertainty.

Under classical normal-theory assumptions ($u_i|X \sim \mathcal{N}(0, \sigma^2)$), the sampling distribution of the OLS estimator is:

$$\hat{\boldsymbol{\beta}} \sim \mathcal{N}\left(\boldsymbol{\beta}, \; \sigma^2 (\mathbf{X}^T\mathbf{X})^{-1}\right)$$

In practice, the true disturbance variance $\sigma^2$ is unknown and must be estimated by the unbiased sample residual variance:
$$s^2 = \frac{SSR}{n - k - 1} = \frac{\sum_{i=1}^n \hat{u}_i^2}{n - k - 1}$$

The **Standard Error** of an individual slope coefficient is $SE(\hat{\beta}_j) = \sqrt{s^2 [(\mathbf{X}^T\mathbf{X})^{-1}]_{jj}}$.

Testing a single hypothesis $H_0: \beta_j = \beta_{j0}$ against $H_a: \beta_j \neq \beta_{j0}$ uses the Student's $t$-statistic:

$$t = \frac{\hat{\beta}_j - \beta_{j0}}{SE(\hat{\beta}_j)} \sim t_{n - k - 1}$$

A $p$-value represents the probability of observing a test statistic at least as extreme as the realized value, *conditional on the null hypothesis and model assumptions being true*. It is **not** the probability that the null hypothesis is true!

**Confidence Intervals vs. Prediction Intervals**:
- A **Confidence Interval** bounds uncertainty around the unobservable population parameter or conditional mean:
  $$\text{CI}_{1-\alpha}[E[y|x_0]] = \hat{y}_0 \pm t_{crit} \times \sqrt{s^2 \mathbf{x}_0^T (\mathbf{X}^T\mathbf{X})^{-1} \mathbf{x}_0}$$
- A **Prediction Interval** bounds an individual future realization ($y_0 = \mathbf{x}_0^T\boldsymbol{\beta} + u_0$), which incorporates both parameter estimation error AND the random disturbance shock $u_0$:
  $$\text{PI}_{1-\alpha}[y_0] = \hat{y}_0 \pm t_{crit} \times \sqrt{s^2 \left(1 + \mathbf{x}_0^T (\mathbf{X}^T\mathbf{X})^{-1} \mathbf{x}_0\right)}$$
Because individual financial returns contain substantial unpredictable market noise ($s^2$), prediction intervals are always much wider than confidence intervals.

**Joint Linear Hypotheses ($F$-Tests)**:
Testing multiple restrictions simultaneously (e.g., $H_0: \beta_1 = 0 \text{ and } \beta_2 = 0$) cannot be performed by checking individual $t$-tests because regressors are correlated. Instead, we use the Wald $F$-statistic:
$$F = \frac{(SSR_R - SSR_U) / q}{SSR_U / (n - k - 1)} \sim F_{q, \; n - k - 1}$$
where $SSR_R$ is the residual sum of squares from the restricted model and $q$ is the number of joint restrictions.""",
        r"""A factor fund manager estimates an alpha intercept for a trading strategy over 100 historical months ($n = 100$, $k = 1$ factor). The estimated coefficient is $\hat{\beta} = 0.60$ with an estimated standard error $SE(\hat{\beta}) = 0.20$.

1. **Calculate the $t$-statistic against zero ($H_0: \beta = 0$)**:
   $$t = \frac{\hat{\beta} - 0}{SE(\hat{\beta})} = \frac{0.60}{0.20} = 3.00$$
2. **Construct the 95% Confidence Interval for the parameter**:
   Using the asymptotic normal critical value $z_{0.025} = 1.96$ (or $t_{0.025, 98} \approx 1.984$):
   $$\text{CI}_{95\%} = 0.60 \pm (1.96 \times 0.20) = [0.60 - 0.392, \; 0.60 + 0.392] = [0.208, \; 0.992]$$
   Because zero lies outside the interval, the null hypothesis of zero parameter is rejected at the 5% significance level.
3. **Contrast parameter uncertainty with individual outcome uncertainty**:
   Suppose the standard error of the estimated conditional mean is $SE(\hat{y}_0) = 0.10$, while the standard deviation of individual monthly return disturbance shocks is $s = 0.50$.
   The forecast standard deviation for an individual realization is:
   $$\sigma_{forecast} = \sqrt{SE(\hat{y}_0)^2 + s^2} = \sqrt{0.10^2 + 0.50^2} = \sqrt{0.01 + 0.25} = \sqrt{0.26} \approx 0.5099$$
   Notice that the disturbance shock ($0.50$) dominates total forecast uncertainty ($0.5099$). Even with a highly precise slope estimate, future monthly returns fluctuate widely!""",
        r"""When conducting statistical inference:
- **Do not rely on large-sample 1.96 critical values in small samples**: When degrees of freedom are small ($n - k - 1 < 30$), Student's $t$ critical values are significantly larger than 1.96 (e.g., $t_{0.025, 10} = 2.228$).
- **Report exact $p$-values and effect sizes**: Statistical significance ($p < 0.05$) does not imply economic importance. A tiny alpha of 1 basis point per month can be statistically significant in a 50-year sample yet completely unviable after 10 bps of transaction fees.
- **Use matrix $F$-tests for joint factor tests**: Never claim that two factors are jointly insignificant simply because their individual $t$-ratios are insignificant.""",
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
        r"""The classical Gauss-Markov assumption of **homoskedasticity** asserts that the variance of the error term conditional on the regressors is constant across all observations: $Var(u_i|X) = \sigma^2$. In financial asset returns, cross-sectional firm data, and macroeconomic time series, this assumption is almost universally violated: small-cap stocks have vastly higher return variance than mega-cap stocks, and market volatility spikes during economic downturns. This phenomenon is **heteroskedasticity** ($Var(u_i|X) = \sigma_i^2 \neq \sigma^2$).

When heteroskedasticity is present:
1. **OLS point estimates ($\hat{\boldsymbol{\beta}}$) remain unbiased and consistent**, provided strict exogeneity ($E[u_i|X] = 0$) holds.
2. **Conventional OLS standard errors are biased and inconsistent**, usually understating true uncertainty, leading to artificially inflated $t$-statistics and false discoveries (Type I errors).
3. **OLS is no longer BLUE** (Best Linear Unbiased Estimator).

To resolve this defect, modern econometrics separates **covariance estimation** from **coefficient estimation**:

**1. Heteroskedasticity-Consistent (HC) Robust Standard Errors**:
Keep the OLS point estimates $\hat{\boldsymbol{\beta}}$ completely unchanged, but compute White's sandwich covariance estimator:

$$\widehat{Var}_{HC}(\hat{\boldsymbol{\beta}}) = (\mathbf{X}^T\mathbf{X})^{-1} \left(\sum_{i=1}^n \hat{u}_i^2 \mathbf{x}_i \mathbf{x}_i^T\right) (\mathbf{X}^T\mathbf{X})^{-1}$$

Modern variants (HC1, HC2, HC3) apply finite-sample leverage adjustments ($h_{ii}$) to prevent underestimation in small samples:
$$\text{HC3}: \quad \hat{u}_{i, HC3}^2 = \frac{\hat{u}_i^2}{(1 - h_{ii})^2}$$
Robust standard errors fix hypothesis tests; they do **not** alter the OLS slope, nor do they repair omitted-variable bias.

**2. Weighted Least Squares (WLS) / Generalized Least Squares (GLS)**:
If the conditional variance structure $\sigma_i^2$ is known or can be modeled as a function of firm size ($z_i$), the researcher can transform the objective function by weighting each observation by its inverse variance:
$$w_i = \frac{1}{\sigma_i^2}$$
$$\min_{\boldsymbol{\beta}} \sum_{i=1}^n w_i \left(y_i - \mathbf{x}_i^T\boldsymbol{\beta}\right)^2$$
WLS restores BLUE efficiency, but **it alters the fitted point estimates $\hat{\boldsymbol{\beta}}$**! Weighted least squares estimates a parameter for a variance-weighted population, which may answer a different economic question than equal-weighted OLS.""",
        r"""Cedar Capital evaluates an intercept-only regression ($y_i = \mu + u_i$) across two cross-sectional market observations:
- Observation 1: Outcome $y_1 = 2.0$, conditional variance $\sigma_1^2 = 1.0$.
- Observation 2: Outcome $y_2 = 6.0$, conditional variance $\sigma_2^2 = 4.0$.

1. **Calculate the unweighted OLS estimate**:
   $$\hat{\mu}_{OLS} = \frac{y_1 + y_2}{2} = \frac{2.0 + 6.0}{2} = 4.0$$
2. **Calculate the Weighted Least Squares (WLS) estimate**:
   - Inverse-variance weights:
     $$w_1 = \frac{1}{\sigma_1^2} = \frac{1}{1.0} = 1.0, \quad w_2 = \frac{1}{\sigma_2^2} = \frac{1}{4.0} = 0.25$$
   - Total weight: $W = w_1 + w_2 = 1.0 + 0.25 = 1.25$.
   - Weighted mean estimate:
     $$\hat{\mu}_{WLS} = \frac{w_1 y_1 + w_2 y_2}{w_1 + w_2} = \frac{(1.0 \times 2.0) + (0.25 \times 6.0)}{1.25} = \frac{2.0 + 1.5}{1.25} = \frac{3.5}{1.25} = 2.80$$
   Notice that $\hat{\mu}_{WLS} = 2.80 \neq \hat{\mu}_{OLS} = 4.00$. Weighting altered the point estimate by downweighting the noisier second observation.
3. **Contrast with Robust Standard Errors**:
   In a separate linear model, the OLS slope is $\hat{\beta} = 0.80$.
   - Conventional homoskedastic standard error: $SE_{OLS} = 0.10 \implies t = \frac{0.80}{0.10} = 8.00$.
   - White-Huber robust standard error: $SE_{HC} = 0.20 \implies t = \frac{0.80}{0.20} = 4.00$.
   The point estimate remains exactly $0.80$; only the test statistic and confidence interval are updated to reflect heteroskedasticity.""",
        r"""In production econometric research:
- **Default to HC3 robust standard errors in cross-sections**: Avoid raw homoskedastic standard errors in financial cross-sections. In small to moderate samples, HC3 outperforms HC0 by correcting for high-leverage points.
- **Justify WLS weights economically**: When using market-cap weighting in asset pricing, recognize that WLS estimates the value-weighted market portfolio, which reflects macroeconomic capital rather than average firm behavior.
- **Robust standard errors do not fix endogeneity**: If an explanatory variable correlates with the error term ($Cov(X, u) \neq 0$), robust standard errors yield consistent uncertainty around an inconsistent and biased parameter!""",
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
        r"""In time-series econometrics, consecutive observations frequently exhibit temporal correlation. When error disturbances correlate across time ($Cov(u_t, u_{t-j}) \neq 0$), the regression errors violate the Gauss-Markov assumption of independence. In financial data, serial correlation arises naturally from:
- **Overlapping return horizons**: Regressing quarterly returns measured at monthly intervals causes neighboring observations to share two months of identical underlying price shocks.
- **Stale pricing and microstructure frictions**: Illiquid assets exhibit bid-ask bounce or delayed price discovery.
- **Gradual macro policy adjustments**: Monetary policy rate cycles and inflation persistence.

When disturbances exhibit positive serial correlation (typical in finance), OLS residuals cluster in runs of similar sign. Conventional OLS standard errors severely underestimate true sampling variability because they divide by $\sqrt{n}$ under the false assumption that each observation brings $100\%$ independent new information. The resulting $t$-statistics are spuriously inflated.

To obtain valid statistical inference without changing the consistent OLS slope coefficients, econometrics relies on **Heteroskedasticity and Autocorrelation Consistent (HAC)** covariance estimators, pioneered by Newey and West (1987).

The **long-run variance** of the score vector $\mathbf{s}_t = \mathbf{x}_t u_t$ incorporates both contemporaneous variance and weighted lagged autocovariances:

$$\boldsymbol{\Omega}_{HAC} = \boldsymbol{\Gamma}_0 + \sum_{j=1}^L w_j \left(\boldsymbol{\Gamma}_j + \boldsymbol{\Gamma}_j^T\right)$$

where:
- $\boldsymbol{\Gamma}_j = \frac{1}{T}\sum_{t=j+1}^T \mathbf{s}_t \mathbf{s}_{t-j}^T$ is the sample autocovariance of scores at lag $j$.
- $w_j = 1 - \frac{j}{L + 1}$ is the **Bartlett triangular kernel weight**, which downweights higher lags toward zero and guarantees that the resulting covariance matrix $\boldsymbol{\Omega}_{HAC}$ is positive semi-definite.
- $L$ is the truncation lag parameter, typically chosen proportional to $T^{1/4}$ or matched to the overlap horizon.

The Newey-West sandwich covariance matrix for OLS coefficients is:

$$\widehat{Var}_{HAC}(\hat{\boldsymbol{\beta}}) = (\mathbf{X}^T\mathbf{X})^{-1} \left(T \boldsymbol{\Omega}_{HAC}\right) (\mathbf{X}^T\mathbf{X})^{-1}$$

Crucially, HAC adjusts uncertainty *around* the estimated parameters; it does **not** cure look-ahead leakage, make an endogenous regressor exogenous, or repair structural parameter instability.""",
        r"""Cedar Capital evaluates a time-series mean return ($\mu$) across $n = 100$ monthly observations exhibiting positive first-order autocorrelation:
- Contemporaneous sample variance (lag-zero autocovariance): $\gamma_0 = 4.0$.
- Lag-one sample autocovariance: $\gamma_1 = 1.0$.
- Truncation lag $L = 1$, with Bartlett weight $w_1 = 1 - \frac{1}{1 + 1} = 0.50$.

1. **Calculate the long-run variance ($\Omega$)**:
   $$\Omega = \gamma_0 + 2 w_1 \gamma_1 = 4.0 + (2 \times 0.50 \times 1.0) = 4.0 + 1.0 = 5.0$$
2. **Compare standard error under independence vs. HAC**:
   - Under naive independence ($\gamma_1 = 0$):
     $$SE_{naive} = \sqrt{\frac{\gamma_0}{n}} = \sqrt{\frac{4.0}{100}} = \sqrt{0.04} = 0.200$$
   - Under Newey-West HAC accounting for serial correlation:
     $$SE_{HAC} = \sqrt{\frac{\Omega}{n}} = \sqrt{\frac{5.0}{100}} = \sqrt{0.05} \approx 0.2236$$
3. **Examine the impact on statistical inference**:
   The HAC standard error ($0.2236$) is approximately $11.8\%$ larger than the naive standard error ($0.200$). If the sample mean estimate were $\hat{\mu} = 0.42$:
   - Naive $t$-statistic: $t = \frac{0.42}{0.200} = 2.10$ ($p < 0.05$, declaring statistical significance).
   - HAC $t$-statistic: $t = \frac{0.42}{0.2236} \approx 1.878$ ($p > 0.05$, failing to reject the null hypothesis of zero alpha).
   Ignoring autocorrelation would have published a false discovery!""",
        r"""When implementing HAC standard errors in quantitative workflows:
- **Match truncation lag to overlapping horizons**: If modeling 12-month forward returns sampled monthly, set $L \ge 11$ to span the mechanical 11-month overlap.
- **Do not assume HAC standard errors are always larger**: If a series exhibits negative autocorrelation (e.g., bid-ask bounce or mean-reverting daily spreads), $\gamma_1 < 0$, which can make HAC standard errors smaller than conventional OLS errors.
- **HAC requires sufficient sample size**: In samples of fewer than 50 observations, HAC estimators exhibit substantial finite-sample downward bias. Consider block bootstrap alternatives or pre-whitening filters.""",
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
        r"""The paramount challenge in empirical econometrics is **endogeneity**: the statistical condition where an explanatory regressor $x$ correlates with the unobserved structural disturbance term $u$ ($Cov(x, u) \neq 0$). When endogeneity is present, OLS estimates are **biased and inconsistent**—increasing the sample size from 100 to 1,000,000 observations merely converges to the wrong number with extreme precision!

Endogeneity originates from four fundamental mechanisms:
1. **Omitted Variable Bias (Confounding)**: A third unobserved variable $z$ simultaneously affects both the regressor $x$ and the outcome $y$.
2. **Reverse Causality (Simultaneity)**: The outcome $y$ dynamically feeds back into the determination of $x$.
3. **Measurement Error (Errors-in-Variables)**: Observing an imperfect proxy $x = x^* + \nu$ attenuates the estimated slope toward zero (**attenuation bias**).
4. **Sample Selection Bias**: Conditioning the sample on an outcome or survivorship threshold (e.g., analyzing only surviving hedge funds).

**The Omitted Variable Bias Formula**:
Suppose the true structural model is:
$$y = \beta x + \gamma z + \epsilon, \quad \text{where } Cov(x, \epsilon) = Cov(z, \epsilon) = 0$$
If the researcher fails to observe or include $z$ and fits the "short regression" $y = \beta_{short} x + v$, the expected OLS estimator is:

$$\beta_{short} = \frac{Cov(x, y)}{Var(x)} = \beta + \gamma \frac{Cov(x, z)}{Var(x)} = \beta + \gamma \delta$$

where:
- $\beta$ is the true direct structural effect of $x$ on $y$.
- $\gamma$ is the effect of the omitted variable $z$ on $y$.
- $\delta = \frac{Cov(x, z)}{Var(x)}$ is the auxiliary regression slope from projecting the omitted variable $z$ on the included regressor $x$.

The bias term $\gamma \delta$ demonstrates that:
- If $\gamma > 0$ and $\delta > 0$ (or both negative), the short regression is **upwardly biased** ($\beta_{short} > \beta$).
- If $\gamma$ and $\delta$ have opposite signs, the short regression is **downwardly biased** ($\beta_{short} < \beta$).
- Only if $\gamma = 0$ (the omitted variable has zero effect on $y$) OR $\delta = 0$ (the omitted variable is completely uncorrelated with $x$) does OLS remain unbiased.

Crucially, calculating White or Newey-West robust standard errors does **not** cure endogeneity. Robust standard errors adjust covariance matrices; they do not remove the omitted confounding term $\gamma \delta$.""",
        r"""A quantitative equity research group studies whether corporate governance quality ($x$) drives equity returns ($y$).
- The true structural direct effect of governance on returns is $\beta = 1.00$.
- An unobserved confounding variable—unrecorded managerial competence ($z$)—also boosts returns with true effect $\gamma = 2.00$.
- Firms with high managerial competence naturally adopt superior corporate governance, resulting in an auxiliary projection slope $\delta = \frac{Cov(x, z)}{Var(x)} = 0.50$.

1. **Calculate the estimated short-regression slope ($\beta_{short}$)**:
   $$\beta_{short} = \beta + \gamma \delta = 1.00 + (2.00 \times 0.50) = 1.00 + 1.00 = 2.00$$
   The researcher runs a regression of returns on governance, discovers $\hat{\beta} = 2.00$ with $p < 0.001$, and claims that improving governance doubles returns. In reality, half of the estimated effect ($1.00$) is pure omitted-variable bias from unmeasured management skill!
2. **Examine opposite correlation**:
   Suppose instead that distressed firms are forced by activist investors to adopt strict governance, creating a negative relationship between competence and governance ($\delta = -0.50$):
   $$\beta_{short} = 1.00 + (2.00 \times -0.50) = 1.00 - 1.00 = 0.00$$
   The short regression estimates $\hat{\beta} = 0.00$, completely masking the true positive structural effect!""",
        r"""To protect empirical research against endogeneity traps:
- **Draw Directed Acyclic Graphs (DAGs)**: Map out causal relationships, confounders, colliders, and mediators before selecting control variables.
- **Beware the "Bad Control" trap**: Do not control for variables that are themselves outcomes of the treatment (mediators or colliders). Conditioning on a collider creates spurious selection bias where none previously existed.
- **Transparently qualify claims**: If you lack an identification strategy (such as natural experiments or instrumental variables), report the result as a descriptive partial association, never as a structural causal impact.""",
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
    # -------------------------------------------------------------------------
    # UNIT 3: DYNAMIC TIME-SERIES MODELS
    # -------------------------------------------------------------------------

    add(
        "3.13",
        3,
        "Stationarity, unit roots, and deterministic trends",
        "Distinguish stable dependence from stochastic trends and interpret complementary stationarity tests.",
        r"""In financial time-series modeling, valid statistical inference and stable forecasting depend upon the underlying stochastic process being **covariance stationary** (weakly stationary). A discrete-time stochastic process $\{y_t\}$ is covariance stationary if its unconditional mean $E[y_t] = \mu$ and variance $Var(y_t) = \gamma_0$ are constant and finite across all time periods, and the autocovariance $Cov(y_t, y_{t-k}) = \gamma_k$ depends solely on the time lag displacement $k$, rather than calendar date $t$.

An analyst must distinguish between two fundamentally distinct forms of non-stationarity:

1. **Deterministic Trend-Stationary Process**:
   $$y_t = \alpha + \delta t + u_t, \quad u_t \sim I(0)$$
   Here, deviations from the deterministic linear time trend $\delta t$ are mean-reverting and stationary. Shocks have transitory effects, and the series is rendered stationary by **linear detrending** (regressing $y_t$ on $t$ and collecting residuals).
2. **Stochastic Trend (Unit Root / Difference-Stationary Process)**:
   $$y_t = y_{t-1} + u_t = y_0 + \sum_{i=1}^t u_i, \quad u_t \sim I(0)$$
   Here, the process possesses a **unit root** ($y_t \sim I(1)$). Historical innovations $u_i$ accumulate indefinitely with permanent memory: variance explodes linearly with time ($Var(y_t) = t \sigma^2 \to \infty$). The process does **not** revert to a deterministic mean. Applying linear detrending to a unit-root process generates spurious cycles; it must be rendered stationary by **first-differencing**:
   $$\Delta y_t = y_t - y_{t-1} = u_t \sim I(0)$$

**Testing for Unit Roots and Stationarity**:
- **Augmented Dickey-Fuller (ADF) Test**:
  $$\Delta y_t = \alpha + \beta t + \gamma y_{t-1} + \sum_{j=1}^p \psi_j \Delta y_{t-j} + e_t$$
  Tests the null hypothesis of a unit root ($H_0: \gamma = 0$) against the alternative of stationarity ($H_a: \gamma < 0$). Under the null, the $t$-statistic does not follow a Student's $t$ distribution; it follows the non-standard Dickey-Fuller distribution, requiring MacKinnon critical values.
- **KPSS Test**: Reverses the burden of proof by testing the null hypothesis of stationarity ($H_0: y_t \sim I(0)$) against the alternative of a unit root ($H_a: y_t \sim I(1)$).
Using ADF and KPSS complementarily prevents misclassifying persistent near-unit-root series as stationary.""",
        r"""Cedar Capital evaluates an interest rate spread $y_t$ modeled as an autoregressive AR(1) process:

$$y_t = 0.20 + 0.80 y_{t-1} + u_t, \quad |\phi| = 0.80 < 1.0$$

1. **Calculate the long-run stationary equilibrium mean ($\mu$)**:
   $$\mu = \frac{c}{1 - \phi} = \frac{0.20}{1 - 0.80} = \frac{0.20}{0.20} = 1.00 \text{ percentage point}$$
2. **Calculate shock persistence over time**:
   Suppose a sudden liquidity shock of $+1.00$ unit occurs at time $t$. Because the autoregressive coefficient is $\phi = 0.80$:
   - After 1 period: $(0.80)^1 = 0.800$ of the shock remains.
   - After 2 periods: $(0.80)^2 = 0.640$ of the shock remains.
   - After 3 periods: $(0.80)^3 = 0.512$ of the shock remains.
   - After 4 periods: $(0.80)^4 = 0.4096$ of the shock remains.
   Because $|\phi| < 1$, the shock decays exponentially toward zero, confirming mean reversion.
3. **Contrast with a unit root ($\phi = 1.00$)**:
   If $\phi = 1.00$, the denominator $1 - \phi = 0$; the stationary mean is undefined. After 3 steps, $(1.00)^3 = 1.00$ of the shock remains permanently, and the series drifts without an anchor. Attempting to fit stationary spread-arbitrage models on a unit-root process results in uncontained capital drawdowns.""",
        r"""In systematic quantitative research:
- **Never regress non-stationary price levels against each other**: Regressing two independent random walks produces a **spurious regression** with high $R^2$ ($R^2 > 0.80$) and significant $t$-statistics, accompanied by a Durbin-Watson statistic near zero ($DW \to 0$).
- **Select ADF deterministic terms based on economic theory**: If asset prices trend upward over decades, include a drift and trend term ($\alpha + \beta t$); for interest rate spreads or basis trades, include only an intercept ($\alpha$).
- **Beware structural breaks**: A stationary process that experiences a permanent regime break (e.g., central bank policy change) can cause standard ADF tests to falsely fail to reject the unit root null (Perron 1989).""",
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
        r"""Time-series forecasting models parameterize the dynamic conditional expectation of future outcomes based on historical values and innovations. The general class of linear dynamic models is the **Autoregressive Moving-Average, ARMA($p, q$)** process:

$$y_t = c + \sum_{i=1}^p \phi_i y_{t-i} + u_t + \sum_{j=1}^q \theta_j u_{t-j}, \quad u_t \sim WN(0, \sigma^2)$$

where:
- **Autoregressive (AR) components** capture persistence by regressing $y_t$ onto its own past realized values $y_{t-i}$.
- **Moving-Average (MA) components** model shocks by regressing $y_t$ onto current and unobserved past white-noise innovations $u_{t-j}$. **Crucial distinction**: In time-series econometrics, an "MA" process does *not* mean a simple technical rolling moving average of prices; it models persistence through past structural error disturbances!
- **ARIMA($p, d, q$)** incorporates order-$d$ fractional or integer differencing ($\Delta^d y_t$) to achieve stationarity before fitting ARMA dynamics.

**Recursive Multi-Step Forecasting**:
For an AR(1) process $y_t = c + \phi y_{t-1} + u_t$ with stationary mean $\mu = \frac{c}{1 - \phi}$:
1. **One-step ahead forecast ($t+1$)**:
   $$\hat{y}_{t+1|t} = E[y_{t+1}|I_t] = c + \phi y_t = \mu + \phi (y_t - \mu)$$
2. **Two-step ahead forecast ($t+2$)**:
   $$\hat{y}_{t+2|t} = E[c + \phi y_{t+1} + u_{t+2}|I_t] = c + \phi \hat{y}_{t+1|t} = \mu + \phi^2 (y_t - \mu)$$
3. **General $h$-step ahead forecast ($t+h$)**:
   $$\hat{y}_{t+h|t} = \mu + \phi^h (y_t - \mu)$$
As the forecast horizon $h \to \infty$, the conditional forecast converges geometrically to the unconditional long-run mean $\mu$.

**Accumulating Forecast Uncertainty**:
While point forecasts revert toward $\mu$, the forecast error variance **expands monotonically** with horizon $h$ as unobserved future shocks accumulate:
$$Var(e_{t+1|t}) = \sigma^2$$
$$Var(e_{t+2|t}) = \sigma^2 (1 + \phi^2)$$
$$Var(e_{t+h|t}) = \sigma^2 \sum_{j=0}^{h-1} \phi^{2j} \xrightarrow{h \to \infty} \frac{\sigma^2}{1 - \phi^2} = Var(y_t)$$
Consequently, multi-step prediction intervals widen rapidly as the forecast horizon extends.""",
        r"""Cedar Capital's quantitative futures desk models a mean-reverting basis spread using an estimated AR(1) model:
$$y_t = 0.20 + 0.80 y_{t-1} + u_t, \quad \sigma^2 = 0.04$$
The latest observed spread at forecast origin $t$ is $y_t = 2.00$ (with long-run mean $\mu = \frac{0.20}{1 - 0.80} = 1.00$).

1. **Calculate the one-step ahead forecast ($t+1$)**:
   $$\hat{y}_{t+1|t} = 0.20 + (0.80 \times 2.00) = 0.20 + 1.60 = 1.80$$
   - One-step forecast error variance:
     $$Var(e_{t+1|t}) = \sigma^2 = 0.0400 \implies SE = \sqrt{0.04} = 0.20$$
2. **Calculate the two-step ahead forecast ($t+2$)**:
   $$\hat{y}_{t+2|t} = 0.20 + (0.80 \times \hat{y}_{t+1|t}) = 0.20 + (0.80 \times 1.80) = 0.20 + 1.44 = 1.64$$
   - Two-step forecast error variance:
     $$Var(e_{t+2|t}) = \sigma^2 (1 + \phi^2) = 0.04 \times (1 + 0.80^2) = 0.04 \times (1 + 0.64) = 0.04 \times 1.64 = 0.0656$$
     $$SE(e_{t+2|t}) = \sqrt{0.0656} \approx 0.2561$$
3. **Contrast with naive random-walk benchmark**:
   A naive random-walk baseline asserts $\hat{y}_{t+1} = \hat{y}_{t+2} = y_t = 2.00$. The AR(1) forecast explicitly anticipates mean reversion from $2.00$ down toward $1.64$, but its 2-step uncertainty interval expands by $28\%$ ($0.2561$ vs $0.200$).""",
        r"""In systematic time-series pipelines:
- **Strictly freeze forecast origin dates**: When reporting an $h$-step forecast issued at time $t$, never update the origin with intermediate realized observations $y_{t+1}$ without changing the timestamp label.
- **Invert differencing cleanly**: If an ARIMA model differences prices to returns ($\Delta p_t$), convert the return forecasts back into price levels recursively: $\hat{P}_{t+h|t} = P_t \times \exp(\sum_{i=1}^h \hat{r}_{t+i|t})$.
- **Verify invertibility and stationarity roots**: For ARMA models, verify that all roots of the autoregressive polynomial lie strictly outside the unit circle ($|z| > 1$).""",
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
        r"""Model selection in time-series econometrics involves balancing explanatory power against model complexity. Adding additional autoregressive or moving-average lags always improves in-sample likelihood fit, but risks severe overfitting that degrades out-of-sample prediction.

To select optimal lag orders ($p, q$), researchers use likelihood-based **Information Criteria**:
1. **Akaike Information Criterion (AIC)**:
   $$\text{AIC} = 2k - 2\ln(\hat{L})$$
   where $k$ is the number of estimated parameters and $\hat{L}$ is the maximized likelihood value. AIC penalizes parameters linearly ($2k$), aiming for asymptotic predictive efficiency.
2. **Bayesian Information Criterion (BIC / Schwarz Criterion)**:
   $$\text{BIC} = k\ln(T) - 2\ln(\hat{L})$$
   BIC imposes a heavier penalty ($k \ln T$) for moderate-to-large samples ($T \ge 8$). BIC is statistically consistent, meaning it identifies the true model with probability approaching 1 as $T \to \infty$.

**Critical Rule for Information Criteria**: Comparing AIC or BIC across models requires identical sample spans and identical dependent variable transformations. Comparing an AR(1) in price levels against an AR(1) in first differences using AIC is mathematically invalid because their underlying likelihoods are defined over completely different data supports.

**Rolling Walk-Forward Evaluation**:
Information criteria guide model selection during development, but true predictive validity must be tested on an **untouched held-out sample** using chronological walk-forward splits:
- **Expanding Window**: Fits the model on $t=1 \dots T_0$, forecasts $T_0+1$, then expands training to $t=1 \dots T_0+1$ to forecast $T_0+2$.
- **Rolling Window**: Maintains a fixed window size $M$, dropping the oldest observation as each new date is added ($t = T - M + 1 \dots T$).

Forecast errors are evaluated using **Mean Squared Error (MSE)** and **Mean Absolute Error (MAE)**:
$$\text{MSE} = \frac{1}{H}\sum_{t=1}^H e_t^2, \quad \text{MAE} = \frac{1}{H}\sum_{t=1}^H |e_t|$$

**Overlapping Forecast Error Dependence**:
When evaluating multi-step forecasts ($h > 1$), adjacent forecast errors share $h - 1$ periods of identical market shocks. Consequently, forecast errors are serially correlated up to lag $h - 1$. Comparing models using paired $t$-tests without Newey-West or Diebold-Mariano adjustments severely underestimates test variance and reports spuriously low $p$-values.""",
        r"""Cedar Capital compares two candidate forecasting specifications for monthly asset return dynamics:
- **Model A (Parsimonious AR(2))**: $k = 3$ parameters (intercept + 2 AR lags), maximized log likelihood $\ln(\hat{L}) = -100.0$.
- **Model B (Over-parameterized ARMA(3,2))**: $k = 6$ parameters, maximized log likelihood $\ln(\hat{L}) = -98.0$ (better in-sample fit).

1. **Calculate Akaike Information Criterion (AIC)**:
   $$\text{AIC}_A = (2 \times 3) - 2(-100.0) = 6 - (-200.0) = 206.0$$
   $$\text{AIC}_B = (2 \times 6) - 2(-98.0) = 12 - (-196.0) = 208.0$$
   Even though Model B achieves a higher log likelihood ($-98.0 > -100.0$), Model A is preferred by AIC ($206.0 < 208.0$) because Model B's modest fit improvement does not justify three additional parameters.
2. **Evaluate out-of-sample forecast errors**:
   On three held-out test months, Model A records forecast errors of $e = [1.0, -1.0, 2.0]$ percentage points.
   $$\text{MSE} = \frac{1^2 + (-1)^2 + 2^2}{3} = \frac{1.0 + 1.0 + 4.0}{3} = \frac{6.0}{3} = 2.00 \text{ points}^2$$
   $$\text{MAE} = \frac{|1.0| + |-1.0| + |2.0|}{3} = \frac{1.0 + 1.0 + 2.0}{3} = \frac{4.0}{3} \approx 1.333 \text{ points}$$
   MSE penalizes the $2.0$-point forecast miss quadratically, while MAE treats it linearly.""",
        r"""When conducting model selection and rolling validation:
- **Do not tune hyperparameters on the final test partition**: Repeatedly running AIC searches or grid searches on the test set turns the test set into an informal training set, invalidating out-of-sample claims.
- **Compare against a naive benchmark**: A model must beat a simple historical mean or random-walk baseline ($\hat{y}_{t+1} = y_t$) out-of-sample.
- **Apply the Diebold-Mariano test for forecast comparison**: When comparing two competing forecasting models over overlapping horizons, use the Diebold-Mariano (1995) test with Newey-West HAC weighting to account for serial correlation in forecast loss differentials.""",
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
        r"""Financial market variables rarely evolve in isolation. Stock returns, interest rate spreads, currency exchange rates, and credit default swaps interact dynamically through feedback loops and spillover mechanisms. A **Vector Autoregression (VAR)** models an $m$-dimensional vector of endogenous stationary variables $\mathbf{y}_t = [y_{1t}, y_{2t}, \dots, y_{mt}]^T$ as a linear function of its own $p$ lagged vectors:

$$\mathbf{y}_t = \mathbf{c} + \mathbf{A}_1 \mathbf{y}_{t-1} + \mathbf{A}_2 \mathbf{y}_{t-2} + \cdots + \mathbf{A}_p \mathbf{y}_{t-p} + \mathbf{u}_t$$

where:
- $\mathbf{c}$ is an $m \times 1$ vector of constant intercepts.
- $\mathbf{A}_i$ are $m \times m$ coefficient matrices capturing both direct auto-lags and cross-variable dynamic cross-lags.
- $\mathbf{u}_t$ is an $m \times 1$ vector of white-noise disturbances with contemporaneous covariance matrix $\boldsymbol{\Sigma}_u = E[\mathbf{u}_t \mathbf{u}_t^T]$.

**The Curse of Dimensionality**:
A VAR($p$) with $m$ variables estimates $m + p \times m^2$ parameters. For a 5-variable system with 4 lags, the model estimates $5 + 4(25) = 105$ parameters! Without substantial sample size, unconstrained VARs suffer from massive estimation variance and parameter instability.

**Granger "Causality" vs. Structural Causality**:
A variable $x$ **Granger-causes** $y$ if historical lags of $x$ contain predictive information that helps forecast future values of $y$, above and beyond the information contained in historical lags of $y$ alone:
$$H_0: A_{12, 1} = A_{12, 2} = \cdots = A_{12, p} = 0 \quad \text{via Wald } F\text{-test}$$
**Crucial Econometric Warning**: Granger causality is a statement of **temporal linear predictability**, *not structural economic causality*! If financial market participants anticipate a future regulatory fine and sell off shares before the fine is announced, stock prices will Granger-cause the regulatory announcement. The stock drop did not *cause* the regulator to act!

**Structural Impulse Response Functions (IRFs)**:
Because contemporaneous errors $\mathbf{u}_t$ are mutually correlated ($\boldsymbol{\Sigma}_u$ is non-diagonal), an isolated shock to equation 1 cannot occur without moving equation 2. To trace how an isolated structural shock propagates through the system, researchers must identify orthogonal shocks ($\mathbf{e}_t = \mathbf{B}^{-1}\mathbf{u}_t$, where $E[\mathbf{e}_t \mathbf{e}_t^T] = \mathbf{I}$).
The standard identification tool is the **Cholesky decomposition** ($\boldsymbol{\Sigma}_u = \mathbf{P}\mathbf{P}^T$, where $\mathbf{P}$ is lower triangular). Cholesky imposes a strict recursive causal ordering: the first variable responds only with a lag to shocks in subsequent variables, while the last variable responds instantaneously to all shocks. Reversing the Cholesky ordering can radically alter the resulting impulse response curves!""",
        r"""Cedar Capital estimates a bivariate VAR(1) system connecting changes in a sovereign bond yield ($y_{1t}$) and equity index returns ($y_{2t}$):
$$\begin{pmatrix} y_{1t} \\ y_{2t} \end{pmatrix} = \begin{pmatrix} 0.60 & 0.20 \\ 0.10 & 0.50 \end{pmatrix} \begin{pmatrix} y_{1, t-1} \\ y_{2, t-1} \end{pmatrix} + \begin{pmatrix} u_{1t} \\ u_{2t} \end{pmatrix}$$
At time $t$, the current state vector is $\mathbf{y}_t = [y_{1t}, y_{2t}]^T = [2.00, 1.00]^T$.

1. **Compute one-step ahead conditional vector forecast ($\hat{\mathbf{y}}_{t+1|t}$)**:
   - First variable (yield change forecast):
     $$\hat{y}_{1, t+1|t} = (0.60 \times 2.00) + (0.20 \times 1.00) = 1.20 + 0.20 = 1.40 \text{ points}$$
   - Second variable (equity return forecast):
     $$\hat{y}_{2, t+1|t} = (0.10 \times 2.00) + (0.50 \times 1.00) = 0.20 + 0.50 = 0.70 \text{ points}$$
   The forecast vector is $\hat{\mathbf{y}}_{t+1|t} = [1.40, 0.70]^T$.
2. **Trace shock propagation**:
   Suppose a pure one-unit shock strikes the first variable at time $t$ ($\mathbf{u}_{t+1} = [1.0, 0.0]^T$).
   The immediate next-step response across the system is given by the first column of $\mathbf{A}_1$:
   $$\Delta \hat{\mathbf{y}}_{t+2} = \mathbf{A}_1 \begin{pmatrix} 1.0 \\ 0.0 \end{pmatrix} = \begin{pmatrix} 0.60 \\ 0.10 \end{pmatrix}$$
   Yield changes absorb $+0.60$ of the shock, while equity returns experience a $+0.10$ spillover.""",
        r"""In production VAR modeling:
- **Test stability roots**: Check that all eigenvalues of the companion matrix lie strictly inside the unit circle ($|\lambda_i| < 1$). An unstable VAR explodes toward infinity.
- **Always report Cholesky ordering sensitivity**: Show impulse responses under alternative recursive orderings. If reversing variable order flips the sign of an impulse response, the causal story is fragile.
- **Do not fit VARs to non-stationary levels without cointegration**: If series are $I(1)$ and cointegrated, estimate a Vector Error Correction Model (VECM). Fitting a standard VAR in levels invalidates standard asymptotic $F$-test distributions.""",
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

    # -------------------------------------------------------------------------
    # UNIT 4: LONG-RUN RELATIONS AND VOLATILITY
    # -------------------------------------------------------------------------

    add(
        "3.2",
        4,
        "Time series and cointegration",
        "Test whether integrated series share a stable long-run combination and distinguish that evidence from a tradable spread.",
        r"""In financial economics, individual asset price series typically exhibit random-walk unit-root non-stationarity ($y_t \sim I(1)$ and $x_t \sim I(1)$). While regressing two unrelated $I(1)$ series produces invalid spurious regressions, certain economic assets are bound together by fundamental equilibrium forces—such as dual-listed shares, cross-currency exchange rates, commodity crack spreads, or ETF holding baskets.

When two non-stationary $I(1)$ series share a common stochastic drift such that a specific linear combination is stationary ($I(0)$), the series are said to be **cointegrated** (Engle and Granger 1987):

$$s_t = y_t - \alpha - \beta x_t \sim I(0)$$

where:
- $\beta$ is the **cointegrating parameter (hedge ratio)**.
- $\alpha$ is the equilibrium constant offset.
- $s_t$ is the stationary **cointegrating residual (equilibrium spread)**, which possesses a constant long-run mean ($E[s_t] = 0$) and finite variance.

**The Engle-Granger Two-Step Procedure**:
1. **Step 1 (Estimate Long-Run Equation)**: Estimate the levels regression via OLS: $y_t = \alpha + \beta x_t + s_t$. Under cointegration, OLS is **super-consistent**—converging to the true parameter at rate $T$ rather than the usual $\sqrt{T}$.
2. **Step 2 (Test Residual Stationarity)**: Run an Augmented Dickey-Fuller test on the estimated residuals $\hat{s}_t$:
   $$\Delta \hat{s}_t = \gamma \hat{s}_{t-1} + \sum_{j=1}^p \psi_j \Delta \hat{s}_{t-j} + e_t$$
   testing $H_0: \gamma = 0$ (no cointegration) versus $H_a: \gamma < 0$ (cointegration exists).
   **Crucial Critical Value Warning**: Because $\hat{s}_t$ are estimated residuals from a first-stage regression that minimized residual variance, they appear "more stationary" than raw data. Standard standalone ADF critical values (e.g., $-2.86$) **cannot be used**! Analysts must use **Engle-Granger / Phillips-Ouliaris critical values** (which are more negative, e.g., $-3.37$ for $m=2$ with intercept) to prevent false discoveries of cointegration.

**Statistical Cointegration vs. Tradable Strategy**:
Finding statistical evidence of cointegration does **not** guarantee a profitable statistical arbitrage pairs-trading strategy:
- Real-world execution requires paying bid-ask spread crossing fees on *both* legs.
- Shorting stock $x$ incurs borrow fees and margin financing costs.
- The spread may experience structural breaks or protracted multi-month excursions that exceed investor risk limits.""",
        r"""Cedar Capital investigates a synthetic pairs-trading candidate between two dual-listed share classes with observed levels $y_t$ and $x_t$. The estimated long-run equilibrium relationship is:
$$y_t = 2.00 + 1.50 x_t + s_t$$

1. **Calculate the equilibrium spread residual**:
   On a specific trading day, price observations are $x_t = 10.00$ and $y_t = 18.00$.
   $$\hat{s}_t = y_t - \hat{\alpha} - \hat{\beta} x_t = 18.00 - 2.00 - (1.50 \times 10.00) = 16.00 - 15.00 = +1.00$$
   The spread is $+1.00$ unit above its historical equilibrium mean of zero. A statistical arbitrage model signals that $y$ is relatively rich and $x$ is relatively cheap.
2. **Accounting for transaction costs and units**:
   Suppose the model requires a long position of $\$15.00$ in $x$ and a short position of $\$18.00$ in $y$.
   - Round-trip transaction costs across both legs (spread crossing + exchange fees) consume $0.80$ units.
   - Net expected reversion profit from the $+1.00$ mispricing is:
     $$\text{Net Edge} = 1.00 - 0.80 = +0.20 \text{ units}$$
   If transaction costs were $1.20$ units, the strategy would lose money despite perfect statistical cointegration!""",
        r"""In statistical arbitrage research:
- **Never claim cointegration based on correlation**: Two random walks can have a sample correlation of $0.95$ and yet drift apart indefinitely with zero mean reversion.
- **Verify unit consistency**: If prices are quoted in different currencies or lot sizes, harmonize units before estimating the hedge ratio $\beta$.
- **Test stability on rolling out-of-sample data**: Cointegrating parameters often undergo structural breaks due to corporate mergers, share buybacks, or regulatory shifts. Always audit subperiod stability.""",
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
        r"""By the **Granger Representation Theorem**, if two non-stationary $I(1)$ series are cointegrated, there must exist an equivalent dynamic **Vector Error Correction Model (VECM)** that governs their short-run adjustments toward long-run equilibrium:

$$\Delta y_t = \mu_y + \alpha_y \left(y_{t-1} - \beta x_{t-1}\right) + \sum_{i=1}^p \psi_{y, i} \Delta y_{t-i} + \sum_{j=1}^p \gamma_{y, j} \Delta x_{t-j} + \epsilon_{yt}$$

$$\Delta x_t = \mu_x + \alpha_x \left(y_{t-1} - \beta x_{t-1}\right) + \sum_{i=1}^p \psi_{x, i} \Delta y_{t-i} + \sum_{j=1}^p \gamma_{x, j} \Delta x_{t-j} + \epsilon_{xt}$$

where:
- $(y_{t-1} - \beta x_{t-1}) = s_{t-1}$ is the **error correction term (lagged cointegrating residual)**.
- $\alpha_y$ and $\alpha_x$ are the **speed of adjustment coefficients**.
- For stable mean reversion toward equilibrium, when $y_{t-1}$ is higher than equilibrium ($s_{t-1} > 0$), $y$ must decline ($\alpha_y < 0$) and/or $x$ must rise ($\alpha_x > 0$).
- If $\alpha_x = 0$, $x$ does not adjust to the spread; $x$ is **weakly exogenous**, meaning $y$ bears 100% of the burden of restoring equilibrium.

**The Half-Life of Mean Reversion**:
In pairs trading, an essential operational metric is the **half-life** ($h_{1/2}$): the expected time required for a spread divergence to decay by 50% back toward equilibrium.
Modeling the spread $s_t$ as a continuous-time Ornstein-Uhlenbeck process or discrete AR(1) process:
$$s_t = \phi s_{t-1} + u_t \iff \Delta s_t = (\phi - 1) s_{t-1} + u_t = \lambda s_{t-1} + u_t$$
where $\lambda = \phi - 1 \in (-1, 0)$ is the rate of reversion.
The half-life of mean reversion is:

$$h_{1/2} = \frac{\ln(0.5)}{\ln(\phi)} \approx \frac{-\ln(2)}{\ln(\phi)} \approx \frac{-0.693}{\lambda}$$

**Calendar Scaling and Estimation Sensitivity**:
- The half-life is measured in units of the sampling frequency (e.g., days vs. months). An estimated half-life of $h_{1/2} = 3$ on daily data means 3 trading days; on monthly data, it means 3 months!
- Near the unit root boundary ($\phi \to 1.0$), the denominator $\ln(\phi) \to 0$. Consequently, tiny estimation errors in $\hat{\phi}$ cause the estimated half-life to explode by hundreds of days.""",
        r"""Cedar Capital monitors an equity pairs arbitrage spread modeled as:
$$\Delta s_t = -0.20 s_{t-1} + u_t \iff s_t = 0.80 s_{t-1} + u_t$$
where $\phi = 0.80$ and $\lambda = -0.20$ on daily market observations.

1. **Calculate the spread half-life ($h_{1/2}$)**:
   $$h_{1/2} = \frac{\ln(0.5)}{\ln(0.80)} \approx \frac{-0.693147}{-0.223144} \approx 3.106 \text{ trading days}$$
   On average, the spread is expected to decay by half in approximately 3.1 trading days.
2. **Compute expected next-day adjustment from an observed deviation**:
   Suppose the spread widens to $s_{t-1} = 5.00$ units above equilibrium:
   - Expected change in spread:
     $$E[\Delta s_t | s_{t-1} = 5] = -0.20 \times 5.00 = -1.00 \text{ unit}$$
   - Expected next-day spread level:
     $$E[s_t | s_{t-1} = 5] = s_{t-1} + E[\Delta s_t] = 5.00 - 1.00 = 4.00 \text{ units}$$
3. **Contrast with $\phi = 0.50$**:
   If the speed of adjustment is faster ($\phi = 0.50$, $\lambda = -0.50$):
   $$h_{1/2} = \frac{\ln(0.5)}{\ln(0.5)} = 1.00 \text{ trading day}$$
   Half-life collapses to a single day, dramatically reducing holding-period inventory risk.""",
        r"""When implementing error-correction trading systems:
- **Set deterministic time-stop limits**: Never hold a divergence indefinitely based on an estimated half-life. If a spread fails to revert within $3 \times h_{1/2}$ (e.g., 10 days), assume a structural regime break or corporate insolvency event and cut the position.
- **Audit borrow fees over the expected holding duration**: If the half-life is 20 days and short borrow fees on the hard-to-borrow leg are 15% annualized, holding the trade will consume the expected spread convergence profit.
- **Verify adjustment symmetry**: Test whether the speed of adjustment differs when the spread is positive vs. negative (threshold cointegration).""",
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
        r"""In financial asset returns, expected conditional returns are close to zero and difficult to predict, but return **volatility is highly predictable**. Financial returns exhibit **volatility clustering** (Mandelbrot 1963): large price shocks (of either sign) tend to be followed by large price shocks, and quiet periods cluster together.

While classical homoskedastic models assume constant unconditional variance $Var(u_t) = \sigma^2$, risk management requires modeling the dynamic **conditional variance** $h_t = Var(u_t | I_{t-1})$.

**The ARCH and GARCH Formulations**:
- **ARCH($q$) (Engle 1982)** models conditional variance as a linear function of lagged squared innovations:
  $$h_t = \omega + \sum_{i=1}^q \alpha_i u_{t-i}^2$$
- **GARCH(1, 1) (Bollerslev 1986)** adds lagged conditional variance, providing an extremely parsimonious representation of long-memory volatility persistence:
  $$h_t = \omega + \alpha u_{t-1}^2 + \beta h_{t-1}$$
  where:
  - $\omega > 0$ is the baseline variance constant.
  - $\alpha \ge 0$ (the ARCH parameter) measures sensitivity to the most recent market return shock $u_{t-1}^2$.
  - $\beta \ge 0$ (the GARCH parameter) measures the persistence of conditional variance from yesterday's forecast $h_{t-1}$.

**Stationarity and Unconditional Long-Run Variance**:
For a GARCH(1,1) process to be covariance stationary, the persistence sum must be strictly less than one:
$$\text{Persistence} = \alpha + \beta < 1.0$$
Taking unconditional expectations on both sides ($E[h_t] = E[h_{t-1}] = V_L$):
$$V_L = \omega + \alpha V_L + \beta V_L \implies V_L = \frac{\omega}{1 - \alpha - \beta}$$
where $V_L$ is the **unconditional long-run variance**.

**Unit Scaling Warnings**:
Variance is measured in **squared return units**.
- If returns are in decimals ($0.02$ for $2\%$), squared returns and variance are on the order of $0.0004$.
- If returns are in percentage points ($2.0$), squared returns and variance are on the order of $4.0$.
Multiplying return units by $100$ multiplies variance $h_t$ and constant $\omega$ by $100^2 = 10{,}000$! Mixing percentage-point inputs with decimal parameters causes catastrophic variance calculation errors.""",
        r"""Cedar Capital's risk management desk deploys a daily GARCH(1,1) model calibrated with parameters:
$$\omega = 0.010, \quad \alpha = 0.10, \quad \beta = 0.80$$
Yesterday's conditional variance was $h_{t-1} = 0.040$, and yesterday's market innovation was $u_{t-1} = 0.30$ (with squared shock $u_{t-1}^2 = 0.090$).

1. **Calculate the updated conditional variance for today ($h_t$)**:
   $$h_t = \omega + \alpha u_{t-1}^2 + \beta h_{t-1}$$
   $$h_t = 0.010 + (0.10 \times 0.090) + (0.80 \times 0.040)$$
   $$h_t = 0.010 + 0.009 + 0.032 = 0.0510 \text{ squared units}$$
2. **Calculate conditional volatility ($\sigma_t$)**:
   $$\sigma_t = \sqrt{h_t} = \sqrt{0.0510} \approx 0.225832 \text{ units}$$
3. **Calculate volatility persistence and long-run equilibrium variance ($V_L$)**:
   - Persistence:
     $$\alpha + \beta = 0.10 + 0.80 = 0.90 < 1.00 \quad \text{(Stationary)}$$
   - Unconditional long-run variance:
     $$V_L = \frac{\omega}{1 - \alpha - \beta} = \frac{0.010}{1 - 0.90} = \frac{0.010}{0.10} = 0.100$$
   - Long-run equilibrium volatility:
     $$\sigma_L = \sqrt{V_L} = \sqrt{0.100} \approx 0.3162$$
   Because current variance ($0.051$) is below long-run variance ($0.100$), the GARCH forecast expects volatility to rise over multi-day horizons toward $0.3162$.""",
        r"""When deploying GARCH models in production:
- **Audit parameter positivity constraints**: Optimization routines must enforce $\omega > 0, \alpha \ge 0, \beta \ge 0$ to guarantee that conditional variance can never become negative.
- **Check standardized residuals**: Standardized residuals $z_t = \frac{u_t}{\sqrt{h_t}}$ should be independent white noise with zero mean, unit variance, and no remaining autocorrelation in squared residuals ($z_t^2$).
- **Recognize normal tail limitations**: Even with GARCH dynamics, financial standardized residuals frequently exhibit excess kurtosis. Model innovations with Student's $t$ or skewed generalized error distributions to prevent underestimating tail risks.""",
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
        r"""Standard symmetric GARCH(1,1) treats positive and negative price shocks identically: $u_{t-1}^2 = (-u_{t-1})^2$. In equity markets, however, asset volatility reacts asymmetrically to news: bad news (market crashes) triggers a much larger spike in volatility than good news (rallies) of identical magnitude. This asymmetry is driven by the **leverage effect** (debt-to-equity increases as stock prices drop) and the **volatility feedback mechanism**.

To capture this asymmetry, quantitative econometrics uses **Asymmetric GARCH models**:

1. **GJR-GARCH(1, 1) (Glosten, Jagannathan, and Runkle 1993)**:
   $$h_t = \omega + \left(\alpha + \gamma \mathbf{1}_{\{u_{t-1} < 0\}}\right) u_{t-1}^2 + \beta h_{t-1}$$
   where $\mathbf{1}_{\{u_{t-1} < 0\}}$ is an indicator function equal to $1$ if yesterday's shock was negative, and $0$ if positive.
   - For a positive shock ($u_{t-1} > 0$): sensitivity is $\alpha$.
   - For a negative shock ($u_{t-1} < 0$): sensitivity surges to $\alpha + \gamma$.
   - If $\gamma > 0$, negative return shocks generate substantially higher volatility.
   - Covariance stationarity requires $\alpha + \beta + \frac{\gamma}{2} < 1$ under symmetric distributions.
2. **EGARCH (Nelson 1991)**: Models $\ln(h_t)$, naturally guaranteeing positive variance without parameter constraints.

**Evaluating Volatility Forecasts**:
Because true conditional variance $h_t$ is latent and never directly observed in markets, forecast accuracy must be evaluated against a realized proxy $v_t$ (such as intraday realized variance from high-frequency tick data, or squared daily returns $r_t^2$).

Standard Mean Squared Error on variance ($(\hat{h}_t - v_t)^2$) is problematic because variance errors are heavily skewed and heteroskedastic. Econometricians evaluate volatility forecasts using **Quasi-Likelihood (QLIKE)** loss (Patton 2011), which is robust to noise in the realized proxy:

$$\text{QLIKE}(h_t, v_t) = \ln(h_t) + \frac{v_t}{h_t}, \quad h_t > 0$$

QLIKE heavily penalizes models that underestimate volatility ($h_t < v_t$) relative to those that overestimate it, making it ideal for financial risk management and margin buffers.""",
        r"""Cedar Capital evaluates an equity index using an asymmetric GJR-GARCH(1,1) specification with asymmetry coefficient $\gamma = 0.20$.

1. **Calculate asymmetric response to negative shock**:
   Consider a negative return shock of magnitude $|u_{t-1}| = 0.30$ ($u_{t-1} = -0.30$, with $u_{t-1}^2 = 0.090$).
   - The extra variance contributed specifically by the negative sign is:
     $$\Delta h_{asymmetric} = \gamma u_{t-1}^2 = 0.20 \times 0.30^2 = 0.20 \times 0.090 = +0.018 \text{ variance units}$$
   A negative shock generates $0.018$ more variance units than an identical positive $+0.30$ rally.
2. **Compute QLIKE forecast evaluation loss**:
   On a test day, the GJR-GARCH model forecasts conditional variance $h_t = 0.040$, while the realized variance proxy is $v_t = 0.090$.
   $$\text{QLIKE}(h_t, v_t) = \ln(h_t) + \frac{v_t}{h_t} = \ln(0.040) + \frac{0.090}{0.040}$$
   $$\text{QLIKE} = -3.218876 + 2.250000 \approx -0.968876$$
   Notice that QLIKE loss can take negative values because $\ln(h_t) < 0$ for decimal variances. When comparing models, lower QLIKE represents superior forecast accuracy.""",
        r"""In production volatility forecasting:
- **Always enforce strictly positive variance before taking logs**: If a model generates $h_t \le 0$, evaluating $\ln(h_t)$ triggers an immediate `ValueError`. Validate $h_t > 0$ with automated assertions.
- **Do not rely on squared returns as a sole proxy**: Daily squared returns $r_t^2$ are a very noisy proxy for true integrated variance. When available, compute realized variance from 5-minute intraday returns.
- **A lower variance loss does not guarantee correct Value at Risk**: A model with optimal QLIKE loss can still underestimate tail crashes if the standardized innovation distribution fails to capture extreme tail fatness.""",
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
    # -------------------------------------------------------------------------
    # UNIT 5: FACTORS AND PORTFOLIO ESTIMATION
    # -------------------------------------------------------------------------

    add(
        "3.20",
        5,
        "CAPM and multi-factor return models",
        "Specify factor exposures with consistent excess-return units and distinguish explanatory loadings from expected risk premiums.",
        r"""Modern empirical asset pricing explains cross-sectional and time-series variation in asset returns using **multifactor risk models**. Extending the classical Capital Asset Pricing Model (CAPM, Sharpe 1964; Lintner 1965), multi-factor models decompose an asset's excess return ($R_{it} - R_{ft}$) into systematic exposures to common factor risks and an idiosyncratic residual component:

$$r_{it} - r_{ft} = \alpha_i + \boldsymbol{\beta}_i^\top \mathbf{f}_t + \epsilon_{it} = \alpha_i + \sum_{k=1}^K \beta_{ik} f_{kt} + \epsilon_{it}$$

where:
- $r_{it} - r_{ft}$ is the asset's excess return over the risk-free rate at time $t$.
- $f_{kt}$ is the realized excess return of factor $k$ (e.g., Market $MKT$, Size $SMB$, Value $HML$, Momentum $WML$, Profitability $RMW$, and Investment $CMA$).
- $\beta_{ik}$ is the **factor loading (exposure sensitivity)**: $\beta_{ik} = \frac{Cov(R_i, F_k)}{Var(F_k)}$.
- $\alpha_i$ is the pricing error (Jensen's alpha). Under theoretical equilibrium where the $K$ factors span the mean-variance efficient stochastic discount factor, $E[\alpha_i] = 0$.
- $\epsilon_{it}$ is the idiosyncratic residual disturbance ($E[\epsilon_{it}] = 0$, $Cov(\epsilon_{it}, \mathbf{f}_t) = 0$).

**Factor Exposures vs. Factor Risk Premiums**:
A fundamental conceptual error in quantitative research is confusing a **time-series factor loading** ($\beta_i$) with an **expected factor risk premium** ($\lambda_k$):
- $\beta_{ik}$ measures *sensitivity*: how much asset $i$'s return co-moves with contemporaneous realizations of factor $k$.
- $\lambda_k = E[f_k]$ represents *expected compensation*: the average excess return earned per unit of factor exposure in equilibrium:
  $$E[R_i - R_f] = \sum_{k=1}^K \beta_{ik} \lambda_k$$
A factor can explain substantial covariance in asset returns (high $R^2$ and large $\beta$) while offering an expected premium indistinguishable from zero ($\lambda \approx 0$).

**Factor Regressor Construction Warnings**:
- Factor series published by academic libraries (such as the Kenneth French Data Library) are **already excess returns** (long-short hedge spreads or market minus risk-free rate). **Never subtract the risk-free rate a second time from a factor regressor!** Doing so distorts regression slopes and corrupts alpha estimation.""",
        r"""Cedar Capital evaluates an equity quantitative market-neutral fund using a three-factor specification (Market, Size, and Value):
- Estimated manager alpha: $\alpha = 0.0010$ (10 basis points per month in decimal return units).
- Market factor loading: $\beta_{MKT} = 1.10$.
- Size factor loading ($SMB$): $\beta_{SMB} = 0.30$.
- Value factor loading ($HML$): $\beta_{HML} = -0.20$ (growth tilt).

During an evaluation month, realized factor returns are:
$$f_{MKT} = +0.020 \text{ (+2.0\%)}, \quad f_{SMB} = +0.010 \text{ (+1.0\%)}, \quad f_{HML} = -0.005 \text{ (-0.5\%)}$$

1. **Calculate the fitted systematic excess return**:
   $$\hat{r}_t - r_{ft} = \alpha + \beta_{MKT} f_{MKT} + \beta_{SMB} f_{SMB} + \beta_{HML} f_{HML}$$
   $$\hat{r}_t - r_{ft} = 0.0010 + (1.10 \times 0.020) + (0.30 \times 0.010) + (-0.20 \times -0.005)$$
   $$\hat{r}_t - r_{ft} = 0.0010 + 0.0220 + 0.0030 + 0.0010 = 0.0270 \text{ (or } 2.7\%)$$
2. **Calculate the idiosyncratic residual**:
   Suppose the fund realizes an actual excess return of $r_{actual} - r_{ft} = +0.030$ ($+3.0\%$):
   $$\hat{\epsilon}_t = (r_{actual} - r_{ft}) - (\hat{r}_t - r_{ft}) = 0.0300 - 0.0270 = +0.0030 \text{ (+30 bps)}$$
   The systematic factors explain $+2.60\%$ of performance, alpha contributes $+0.10\%$, and the unexplained stock-picking residual contributes $+0.30\%$. A single positive residual does not prove repeatable skill.""",
        r"""When conducting factor research:
- **Preserve exact factor provenance and versions**: Factor data providers periodically restate factor returns due to CRSP/Compustat database revisions or universe reconstitution. Always record the date and version of the factor download.
- **Audit synthetic and planted lab factors**: In simulation environments, planted synthetic factors are pedagogical fixtures. Never confuse a model calibrated on synthetic factors with empirical historical alpha.
- **Ensure date synchronization**: Match monthly asset returns to identical calendar-month factor series. Offsetting factors by a single month destroys explanatory power ($R^2 \to 0$).""",
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
        r"""In institutional asset management, **Performance Attribution** decomposes realized portfolio returns into systematic factor compensation and manager-specific added value. Realized active return is decomposed additively:

$$r_{pt} = \alpha_p + \sum_{k=1}^K \beta_{pk} f_{kt} + \epsilon_{pt}$$

$$\text{Contribution of Factor } k = \beta_{pk} f_{kt}$$

Attribution reconciles historical accounting performance; it is an **ex-post descriptive decomposition**, *not a predictive forecast*. A portfolio that generated $80\%$ of its performance from a strong value factor rally during a single year cannot claim that performance as structural, unrepeatable alpha.

**Alpha Inference and Annualization Conventions**:
Estimated regression alpha ($\hat{\alpha}$) is a point estimate subject to estimation uncertainty. Testing whether an alpha is statistically different from zero uses the $t$-ratio:
$$t_\alpha = \frac{\hat{\alpha}}{SE_{HAC}(\hat{\alpha})}$$

**The Annualization Scaling Rule**:
When converting a daily or monthly alpha and its standard error to an annualized figure:
$$\hat{\alpha}_{annual} = 252 \times \hat{\alpha}_{daily}, \quad SE(\hat{\alpha}_{annual}) = \sqrt{252} \times SE(\hat{\alpha}_{daily}) \quad \text{for independent observations}$$
However, when computing the $t$-statistic on the annualized numbers:
$$t = \frac{\hat{\alpha}_{annual}}{SE(\hat{\alpha}_{annual})} = \frac{252 \hat{\alpha}}{\sqrt{252} SE(\hat{\alpha})} = \sqrt{252} \times \frac{\hat{\alpha}}{SE(\hat{\alpha})}$$
If an analyst simply multiplies *both* the coefficient and standard error by 252, the ratio is completely unchanged: $\frac{252 \alpha}{252 SE} = \frac{\alpha}{SE}$. Scaling both by 252 does not create more independent data or enhance statistical power!

**Time-Varying Factor Exposures (Beta Drift)**:
Portfolio managers actively trade, causing factor loadings $\beta_{pk}$ to fluctuate over time. Estimating a static full-sample OLS beta across a 10-year period averages across different investment regimes, obscuring tactical bets and generating false alpha.""",
        r"""Cedar Capital evaluates an institutional equity portfolio over a single monthly accounting cycle:
- Market factor contribution ($\beta_1 f_1$): $+1.50\%$ ($+0.015$).
- Size factor drag ($\beta_2 f_2$): $-0.20\%$ ($-0.002$).
- Value factor contribution ($\beta_3 f_3$): $+0.30\%$ ($+0.003$).
- Idiosyncratic residual ($\hat{\epsilon}$): $+0.40\%$ ($+0.004$).

1. **Reconcile total realized portfolio return**:
   $$r_p = 0.015 - 0.002 + 0.003 + 0.004 = 0.0200 \implies +2.00\%$$
   The portfolio gained $2.00\%$, of which $1.60\%$ was driven by common systematic factor exposures, and $0.40\%$ represents the idiosyncratic residual.
2. **Evaluate alpha statistical significance**:
   In a separate daily regression, the estimated daily alpha intercept is $\hat{\alpha}_{daily} = 0.0002$ ($+2$ bps per day), with a Newey-West HAC standard error $SE_{HAC} = 0.00015$.
   $$t_\alpha = \frac{\hat{\alpha}_{daily}}{SE_{HAC}(\hat{\alpha}_{daily})} = \frac{0.00020}{0.00015} \approx 1.333$$
   Because $t = 1.333 < 1.96$, the $p$-value is approximately $0.18$. Despite a positive estimated alpha, the performance is **statistically insignificant** and indistinguishable from random chance! Multiplying both numbers by 252 gives $\hat{\alpha} = 0.0504$ and $SE = 0.0378$, with ratio $1.333$; it does not make the alpha statistically significant.""",
        r"""In quantitative attribution workflows:
- **Track rolling and expanding factor betas**: Compute 36-month rolling regressions to detect style drift and changing market exposure.
- **Do not confuse residuals with structural skill**: A positive residual can arise from omitted risk factors (e.g., illiquidity or carry risk), benchmark mismatch, or temporary luck.
- **Link arithmetic attribution to geometric wealth**: For multi-period attribution, use Carino or Menchero linking coefficients to convert single-period arithmetic factor contributions into multi-period compounded portfolio returns.""",
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
        r"""Modern portfolio theory (Markowitz 1952) formalizes investment diversification: the total risk of a portfolio depends not only on the standalone variances of its constituent assets, but critically on their **cross-asset covariances**.

For a portfolio of $N$ assets with capital weight vector $\mathbf{w} = [w_1, w_2, \dots, w_N]^T$ satisfying $\sum w_i = 1$, the portfolio variance is:

$$\sigma_p^2 = \mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w} = \sum_{i=1}^N w_i^2 \sigma_i^2 + 2 \sum_{i=1}^N \sum_{j < i} w_i w_j Cov(R_i, R_j)$$

where $\boldsymbol{\Sigma}$ is the $N \times N$ return covariance matrix and $Cov(R_i, R_j) = \rho_{ij} \sigma_i \sigma_j$.

As portfolio size $N$ expands, the number of variance terms is $N$, while the number of covariance terms is $N(N - 1)$. In a portfolio of 100 securities, there are 100 variance terms and **9,900 covariance terms**! Cross-asset covariance accounts for over $98\%$ of portfolio variance.

**The Pitfalls of Unconstrained Mean-Variance Optimization**:
Classical mean-variance optimization solves:
$$\min_{\mathbf{w}} \frac{1}{2}\mathbf{w}^T \boldsymbol{\Sigma} \mathbf{w} - \lambda \mathbf{w}^T \boldsymbol{\mu} \quad \text{subject to } \mathbf{w}^T \mathbf{1} = 1$$
In practice, unconstrained optimizers are notorious **"error maximizers"** (Michaud 1989):
- Asset expected returns ($\boldsymbol{\mu}$) are estimated with immense statistical error.
- Optimizers aggressively overweight assets with spuriously high historical returns and underweight assets with temporary drawdowns.
- Near-singular sample covariance matrices ($\boldsymbol{\Sigma}$) produce wildly leveraged, unstable long/short weights that collapse out-of-sample.

**Mathematical Requirements for Covariance Matrices**:
A valid covariance matrix must be **symmetric** ($\boldsymbol{\Sigma} = \boldsymbol{\Sigma}^T$) and **positive semi-definite (PSD)**:
$$\mathbf{w}^T \boldsymbol{\Sigma} \mathbf{w} \ge 0 \quad \forall \mathbf{w} \neq \mathbf{0} \iff \text{all eigenvalues } \lambda_i \ge 0$$
If non-synchronous trading, missing data, or pairwise deletion produces negative eigenvalues, the calculated portfolio variance can become mathematically negative, rendering the optimization nonsensical.""",
        r"""Cedar Capital evaluates an equal-weight portfolio ($w_1 = 0.50, w_2 = 0.50$) across two assets:
- Asset 1: Annualized volatility $\sigma_1 = 20.0\%$ ($0.20$, with variance $\sigma_1^2 = 0.040$).
- Asset 2: Annualized volatility $\sigma_2 = 10.0\%$ ($0.10$, with variance $\sigma_2^2 = 0.010$).
- Baseline correlation: $\rho_{12} = 0.30$.

1. **Calculate portfolio variance and volatility under $\rho = 0.30$**:
   $$\sigma_p^2 = w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 + 2 w_1 w_2 \rho_{12} \sigma_1 \sigma_2$$
   $$\sigma_p^2 = (0.50^2 \times 0.040) + (0.50^2 \times 0.010) + (2 \times 0.50 \times 0.50 \times 0.30 \times 0.20 \times 0.10)$$
   $$\sigma_p^2 = (0.25 \times 0.040) + (0.25 \times 0.010) + (0.50 \times 0.006) = 0.0100 + 0.0025 + 0.0030 = 0.0155$$
   $$\sigma_p = \sqrt{0.0155} \approx 0.124499 \implies 12.45\% \text{ annualized volatility}$$
   Notice the diversification benefit: portfolio volatility ($12.45\%$) is significantly below the simple weighted average volatility ($0.50 \times 20\% + 0.50 \times 10\% = 15.0\%$).
2. **Stress test correlation surge during market crisis**:
   Suppose that during a liquidity panic, correlation spikes to perfect comovement ($\rho_{12} = 1.00$):
   $$\sigma_{p, stress}^2 = 0.0100 + 0.0025 + (0.50 \times 1.00 \times 0.02) = 0.0125 + 0.0100 = 0.0225$$
   $$\sigma_{p, stress} = \sqrt{0.0225} = 0.1500 \implies 15.00\%$$
   The diversification benefit evaporates, and portfolio risk surges from $12.45\%$ to $15.00\%$ without changing a single share!""",
        r"""In systematic portfolio construction:
- **Audit positive semi-definiteness**: Check `np.all(np.linalg.eigvals(cov) >= 0)`. If negative eigenvalues exist due to missing data, apply Higham's (2002) nearest correlation matrix projection algorithm.
- **Impose realistic constraints**: Enforce long-only weight constraints ($w_i \ge 0$) and maximum position caps ($w_i \le 0.05$). Constraints act as implicit Bayesian shrinkage, preventing extreme leveraged bets.
- **Compare against naive 1/N equal weighting**: DeMiguel, Garlappi, and Uppal (2009) demonstrated that out-of-sample, naive equal weighting often outperforms mean-variance optimizers due to zero estimation error.""",
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
        r"""When estimating covariance matrices for large investment universes ($N$ assets) over a finite time series ($T$ periods), sample covariance matrices $\mathbf{S} = \frac{1}{T-1}\mathbf{X}^T\mathbf{X}$ suffer from acute **estimation risk**.

By the Marčenko-Pastur law from Random Matrix Theory, when the dimensionality ratio $\frac{N}{T} \to c > 0$, the sample eigenvalues disperse dramatically: the largest sample eigenvalue is substantially upwardly biased, while the smallest eigenvalue is downwardly biased toward zero. If $N \ge T$, the sample covariance matrix is singular ($rank(\mathbf{S}) \le T < N$), with zero eigenvalues that make unconstrained portfolio optimization impossible!

To solve this defect, quantitative finance employs **Covariance Shrinkage** (Ledoit and Wolf 2004):

$$\hat{\boldsymbol{\Sigma}}_{shrink} = (1 - \lambda) \mathbf{S} + \lambda \mathbf{T}$$

where:
- $\mathbf{S}$ is the unstructured, noisy sample covariance matrix (unbiased but high variance).
- $\mathbf{T}$ is a structured, highly constrained **shrinkage target** (biased but zero or low variance), such as:
  - Diagonal target (preserving sample variances, zeroing all covariances).
  - Constant correlation target (Sharpe single-index target: all pairwise correlations set to the cross-sectional mean correlation $\bar{\rho}$).
  - Identity matrix target ($\sigma^2 \mathbf{I}$).
- $\lambda \in [0, 1]$ is the **shrinkage intensity**, optimally selected to minimize expected Frobenius loss: $E[\|\hat{\boldsymbol{\Sigma}} - \boldsymbol{\Sigma}\|^2]$.

**Principal Component Analysis (PCA) and Statistical Risk Models**:
PCA spectral decomposition factors the covariance matrix into orthogonal eigenvectors:
$$\boldsymbol{\Sigma} = \mathbf{V} \boldsymbol{\Lambda} \mathbf{V}^T = \sum_{k=1}^N \lambda_k \mathbf{v}_k \mathbf{v}_k^T$$
where eigenvalues $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_N \ge 0$ quantify the variance explained by each orthogonal component.
The proportion of total market variance explained by the first $K$ principal components is:
$$\text{Explained Variance Ratio} = \frac{\sum_{k=1}^K \lambda_k}{\sum_{i=1}^N \lambda_i}$$

**Critical PCA Interpretive Boundaries**:
1. PCA eigenvectors are purely statistical constructions. The leading eigenvector often looks like a market factor, but the algorithm provides **no economic labeling**.
2. **Eigenvector signs are mathematically arbitrary**: Flipping the sign of an eigenvector ($\mathbf{v}_k \to -\mathbf{v}_k$) and its scores leaves variance and covariance reconstruction identically unchanged!
3. High explained variance does not imply future strategy alpha; it simply measures variance reconstruction within the historical training sample.""",
        r"""Cedar Capital regularizes an unstable $2 \times 2$ covariance matrix where sample variances are $S_{11} = 0.040, S_{22} = 0.010$, and sample covariance is $S_{12} = 0.018$ (correlation $\rho = \frac{0.018}{\sqrt{0.04 \times 0.01}} = \frac{0.018}{0.020} = 0.90$).

1. **Apply 50% shrinkage ($\lambda = 0.50$) toward a diagonal target ($\mathbf{T}$)**:
   The diagonal target retains sample variances ($T_{11} = 0.040, T_{22} = 0.010$) and sets off-diagonal covariance to zero ($T_{12} = 0$).
   - Shrunk covariance:
     $$\hat{\Sigma}_{12} = (1 - 0.50) S_{12} + 0.50 T_{12} = (0.50 \times 0.018) + (0.50 \times 0.0) = 0.0090$$
   - Shrunk variances remain $0.040$ and $0.010$.
2. **Compare equal-weight portfolio variance before and after shrinkage**:
   - Sample equal-weight variance:
     $$\sigma_{p, sample}^2 = (0.25 \times 0.040) + (0.25 \times 0.010) + (0.50 \times 0.018) = 0.0125 + 0.0090 = 0.0215$$
   - Shrunk equal-weight variance:
     $$\sigma_{p, shrunk}^2 = (0.25 \times 0.040) + (0.25 \times 0.010) + (0.50 \times 0.009) = 0.0125 + 0.0045 = 0.0170$$
   Shrinking the noisy covariance toward zero reduces modeled portfolio variance from $0.0215$ to $0.0170$. This is an estimator change, not physical risk elimination!
3. **Calculate PCA explained variance ratio**:
   Suppose a 3-factor market covariance matrix has eigenvalues $\lambda_1 = 0.060, \lambda_2 = 0.030, \lambda_3 = 0.010$ (total variance $= 0.100$).
   $$\text{Component 1 Share} = \frac{\lambda_1}{\lambda_1 + \lambda_2 + \lambda_3} = \frac{0.060}{0.060 + 0.030 + 0.010} = \frac{0.060}{0.100} = 60.0\%$$
   The first principal component explains $60\%$ of total variance, while the remaining two components account for $40\%$, which may contain important idiosyncratic tail risks.""",
        r"""In systematic factor modeling and portfolio optimization:
- **Never tune shrinkage intensity $\lambda$ on the test set**: Select $\lambda$ using analytical Ledoit-Wolf formulas or cross-validation strictly within the development period.
- **Fit PCA eigenvectors strictly on training windows**: Transform out-of-sample data using frozen training eigenvectors ($\mathbf{z}_{test} = \mathbf{V}_{train}^T \mathbf{x}_{test}$). Re-estimating PCA across the full dataset introduces look-ahead data leakage.
- **Beware discarding lower eigenvalues**: Discarding smaller principal components removes idiosyncratic variance, causing optimizers to take unconstrained leveraged bets on unmodeled risks.""",
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

    # -------------------------------------------------------------------------
    # UNIT 6: PANEL AND CAUSAL ANALYSIS
    # -------------------------------------------------------------------------

    add(
        "3.23",
        6,
        "Panel data, fixed effects, and clustered inference",
        "Separate within-entity from between-entity variation and match covariance estimation to panel dependence.",
        r"""In corporate finance, banking, and empirical asset pricing, research datasets frequently span both time and entities: observing $N$ firms repeatedly over $T$ time periods (a **panel dataset**).

The two-way error components model is expressed as:

$$y_{it} = \alpha_i + \gamma_t + \mathbf{x}_{it}^\top \boldsymbol{\beta} + u_{it}, \quad i=1 \dots N, \; t=1 \dots T$$

where:
- $\alpha_i$ is an unobserved **entity fixed effect**, capturing all time-invariant firm-specific heterogeneity (such as corporate culture, founding charter, or historical industry classification).
- $\gamma_t$ is an unobserved **time fixed effect**, capturing all common macroeconomic shocks affecting all firms simultaneously in period $t$ (such as interest rate changes, GDP growth, or pandemic shutdowns).
- $u_{it}$ is the idiosyncratic idiosyncratic disturbance term.

**The Within-Transformation (Fixed Effects Estimator)**:
To eliminate unobserved entity confounders $\alpha_i$ without estimating $N$ separate dummy variables, the **Within-Transformation** subtracts the entity-specific time averages ($\bar{y}_i = \frac{1}{T}\sum_t y_{it}, \bar{\mathbf{x}}_i = \frac{1}{T}\sum_t \mathbf{x}_{it}$):

$$\left(y_{it} - \bar{y}_i\right) = \left(\mathbf{x}_{it} - \bar{x}_i\right)^\top \boldsymbol{\beta} + \left(u_{it} - \bar{u}_i\right)$$

Because $\alpha_i - \bar{\alpha}_i = 0$, all unobserved time-invariant confounders are completely purged!
**Crucial Identification Consequence**: Any explanatory variable that is constant over time for a firm (such as state of incorporation or founder gender) has $\mathbf{x}_{it} - \bar{\mathbf{x}}_i = \mathbf{0}$. **Time-invariant regressors cannot be identified in an entity fixed effects regression!**

**Clustered Standard Errors (Petersen 2009)**:
Panel residuals violate classical OLS independence:
- **Firm Clustering**: Observations for the same firm across different time periods share persistent disturbances ($Cov(u_{it}, u_{is}) \neq 0$).
- **Time Clustering**: Observations across different firms within the same year share macro shocks ($Cov(u_{it}, u_{jt}) \neq 0$).
Treating $N \times T$ observations as independent severely inflates $t$-statistics. Analysts must compute **clustered robust standard errors**:

$$\widehat{Var}_{cluster}(\hat{\boldsymbol{\beta}}) = (\mathbf{X}^T\mathbf{X})^{-1} \left(\sum_{g=1}^G \mathbf{X}_g^T \hat{\mathbf{u}}_g \hat{\mathbf{u}}_g^T \mathbf{X}_g\right) (\mathbf{X}^T\mathbf{X})^{-1}$$

**Cluster Asymptotics Warning**: Clustered covariance estimation relies on asymptotic approximations based on the number of clusters $G \to \infty$. Having 2 or 5 clusters is grossly inadequate; reliable cluster inference requires at least 30 to 50 independent clusters.""",
        r"""Cedar Capital evaluates an executive compensation panel across two firms over two periods ($N=2, T=2$):
- Firm A: $x_A = [1.0, 2.0], \quad y_A = [3.0, 5.0]$
  - Means: $\bar{x}_A = 1.5, \; \bar{y}_A = 4.0$
  - Demeaned deviations: $\tilde{x}_A = [-0.5, +0.5], \; \tilde{y}_A = [-1.0, +1.0]$
- Firm B: $x_B = [3.0, 4.0], \quad y_B = [10.0, 12.0]$
  - Means: $\bar{x}_B = 3.5, \; \bar{y}_B = 11.0$
  - Demeaned deviations: $\tilde{x}_B = [-0.5, +0.5], \; \tilde{y}_B = [-1.0, +1.0]$

1. **Calculate the within-entity regression slope**:
   - Cross-product sum across all 4 demeaned observations:
     $$\sum \tilde{x}_{it} \tilde{y}_{it} = (-0.5 \times -1.0) + (0.5 \times 1.0) + (-0.5 \times -1.0) + (0.5 \times 1.0) = 0.5 + 0.5 + 0.5 + 0.5 = 2.0$$
   - Squared regressor sum:
     $$\sum \tilde{x}_{it}^2 = (-0.5)^2 + 0.5^2 + (-0.5)^2 + 0.5^2 = 0.25 + 0.25 + 0.25 + 0.25 = 1.0$$
   - Within slope:
     $$\hat{\beta}_{within} = \frac{2.0}{1.0} = 2.00$$
   The within-firm slope is $2.00$. Notice that Firm B's level outcome is vastly higher than Firm A's ($11.0$ vs $4.0$), but that permanent between-firm difference is absorbed entirely by the entity fixed effects $\alpha_i$.
2. **Examine cluster count validity**:
   With only two firms ($G = 2$), applying clustered standard errors is mathematically invalid because asymptotic cluster theory requires $G \ge 30-50$.""",
        r"""In empirical panel workflows:
- **Choose between Fixed Effects (FE) and Random Effects (RE) via the Hausman Test**: Random effects assumes $Cov(\alpha_i, \mathbf{x}_{it}) = 0$. If the Hausman test rejects this null ($p < 0.05$), RE is inconsistent, and FE must be used.
- **Implement Two-Way Clustering when appropriate**: In asset pricing panels with both time-series persistence within firms and cross-sectional correlation across firms, use two-way clustering on both `firm_id` and `date` (Thompson 2011; Cameron, Gelbach, and Miller 2011).
- **Fixed effects do not cure time-varying endogeneity**: If a shock simultaneously moves both $x_{it}$ and $y_{it}$ in a given year, entity fixed effects cannot eliminate the resulting omitted-variable bias.""",
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
        r"""When an explanatory regressor $x$ is endogenous ($Cov(x, u) \neq 0$), OLS estimates are biased and inconsistent. **Instrumental Variables (IV)** estimation provides a mathematical method for identifying the true causal parameter $\beta$ by isolating an exogenous component of variation in $x$.

A valid instrumental variable $z$ must satisfy two fundamental conditions:
1. **Instrument Relevance (First-Stage Association)**:
   The instrument must be correlated with the endogenous regressor conditional on controls:
   $$Cov(z, x) \neq 0$$
   Relevance is verifiable in empirical data by inspecting the first-stage regression $F$-statistic. Under the rule of thumb of Stock and Yogo (2005), a first-stage $F$-statistic must exceed **$F > 10$** (or modern thresholds $F > 104$) to rule out severe weak-instrument bias.
2. **Instrument Exogeneity (Exclusion Restriction)**:
   The instrument must be uncorrelated with the unobserved structural disturbance term:
   $$Cov(z, u) = 0$$
   This implies that $z$ affects the outcome $y$ **only through its indirect effect on $x$**, with zero direct path to $y$. **Crucial Epistemological Point**: The exclusion restriction is fundamentally **untestable** in an exactly identified model; it must be defended using economic theory, institutional institutional facts, and timing arguments.

**The Two-Stage Least Squares (2SLS) Estimator**:
For a single endogenous regressor $x$ and single instrument $z$, the IV estimator is the ratio of sample covariances:

$$\hat{\beta}_{IV} = \frac{\widehat{Cov}(z, y)}{\widehat{Cov}(z, x)} = \frac{\sum (z_i - \bar{z})(y_i - \bar{y})}{\sum (z_i - \bar{z})(x_i - \bar{x})}$$

In multiple regression with vector of instruments $\mathbf{Z}$:
- **Stage 1**: Regress endogenous $\mathbf{X}$ on exogenous instruments $\mathbf{Z}$, obtaining fitted values $\hat{\mathbf{X}} = \mathbf{Z}(\mathbf{Z}^T\mathbf{Z})^{-1}\mathbf{Z}^T\mathbf{X}$.
- **Stage 2**: Regress outcome $\mathbf{y}$ on fitted values $\hat{\mathbf{X}}$ via OLS.
- **Covariance Warning**: Standard errors must be computed using original residuals $\mathbf{u} = \mathbf{y} - \mathbf{X}\hat{\boldsymbol{\beta}}_{2SLS}$, *not* the second-stage residuals $\hat{\mathbf{u}} = \mathbf{y} - \hat{\mathbf{X}}\hat{\boldsymbol{\beta}}$.

**The Peril of Weak Instruments**:
When an instrument has a weak first-stage correlation with $x$ ($Cov(z, x) \approx 0$), the denominator in $\hat{\beta}_{IV}$ approaches zero!
In finite samples, weak instruments cause:
- Severe bias in $\hat{\beta}_{IV}$ toward the biased OLS estimator.
- Wildly inflated standard errors and distorted non-normal $t$-distributions, producing false rejection rates far exceeding nominal $5\%$ thresholds.""",
        r"""Cedar Capital evaluates an investment model where a trading parameter is suspected of endogeneity. An analyst proposes an instrument $z$ to estimate structural slope $\beta$.
- Sample covariance between instrument $z$ and outcome $y$: $\widehat{Cov}(z, y) = 0.60$.
- Case A (Strong Instrument): Sample covariance between $z$ and $x$ is $\widehat{Cov}(z, x) = 0.30$.
- Case B (Weak Instrument): Sample covariance between $z$ and $x$ collapses to $\widehat{Cov}(z, x) = 0.03$.

1. **Calculate Case A (Strong Instrument)**:
   $$\hat{\beta}_{IV} = \frac{\widehat{Cov}(z, y)}{\widehat{Cov}(z, x)} = \frac{0.60}{0.30} = 2.00$$
   The estimated structural effect is $2.00$.
2. **Calculate Case B (Weak Instrument Sensitivity)**:
   $$\hat{\beta}_{IV, weak} = \frac{\widehat{Cov}(z, y)}{\widehat{Cov}(z, x)} = \frac{0.60}{0.03} = 20.00$$
   Because the first-stage denominator is near zero ($0.03$), a tiny variation in sampling covariance causes the estimated parameter to explode from $2.00$ to $20.00$!
3. **Examine an exclusion restriction violation**:
   If the instrument $z$ has even a tiny direct correlation with the error term $u$ ($Cov(z, u) = 0.02$):
   $$\text{Asymptotic Bias} = \frac{Cov(z, u)}{Cov(z, x)} = \frac{0.02}{0.03} \approx 0.667$$
   When instruments are weak, even a microscopic exclusion violation produces massive asymptotic bias that is far worse than ordinary OLS!""",
        r"""In empirical IV research:
- **Always report the First-Stage $F$-statistic**: If $F < 10$, discard standard Wald tests and compute weak-instrument-robust confidence intervals, such as the Anderson-Rubin (1949) test.
- **Overidentification Tests (Sargan-Hansen $J$-test)**: When you have more instruments than endogenous variables ($L > K$), test whether the extra instruments are orthogonal to the estimated residuals. Note: Passing the $J$-test does not prove all instruments are valid; it only tests whether all instruments estimate the same parameter.
- **Never pick instruments because they yield significant $t$-statistics**: Data-mining for instruments that produce attractive coefficients generates severe false discoveries.""",
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
        r"""In corporate finance, banking policy evaluation, and market microstructure, researchers frequently study the causal effect of an exogenous policy intervention (e.g., tick size pilot program, short-selling ban, or banking regulation reform). The standard quasi-experimental tool is **Difference-in-Differences (DiD)**.

In the classical $2 \times 2$ setup, researchers observe two groups across two time periods:
- **Treated Group ($T$)**: Subject to the policy intervention in the post-treatment period ($Post = 1$).
- **Comparison / Control Group ($C$)**: Never receives treatment ($Post = 1$ and $Post = 0$).

The classical DiD estimator calculates the difference in outcome changes across the two groups:

$$\text{DiD} = \left(\bar{y}_{T, post} - \bar{y}_{T, pre}\right) - \left(\bar{y}_{C, post} - \bar{y}_{C, pre}\right) = \Delta \bar{y}_T - \Delta \bar{y}_C$$

In regression form, this is estimated via OLS:
$$y_{it} = \beta_0 + \beta_1 Treat_i + \beta_2 Post_t + \delta (Treat_i \times Post_t) + u_{it}$$
where:
- $\beta_1$ absorbs baseline time-invariant differences between groups prior to treatment.
- $\beta_2$ absorbs common macroeconomic time trends affecting both groups.
- $\delta$ is the **causal treatment effect** (the interaction coefficient).

**The Parallel Trends Assumption**:
The foundational identification assumption of DiD is **Parallel Trends**:
$$\textbf{In the absence of treatment, the average outcome of the treated group would have followed}$$
$$\textbf{the exact same trajectory as the comparison group.}$$
Because the counterfactual trajectory of the treated group is unobservable, the parallel trends assumption **cannot be directly tested**. Researchers test for parallel pre-trends by estimating an **Event-Study specification**:
$$y_{it} = \alpha_i + \gamma_t + \sum_{\tau \neq -1} \delta_\tau \left(Treat_i \times \mathbf{1}_{\{t = \tau\}}\right) + u_{it}$$
If the pre-treatment leads ($\delta_\tau$ for $\tau < -1$) are statistically indistinguishable from zero, it lends credibility to the counterfactual design.

**Modern Staggered Adoption Warnings**:
When units receive treatment at different calendar dates with heterogeneous treatment effects over time, classical Two-Way Fixed Effects (TWFE) OLS estimators can produce **negative weights** on already-treated units, reversing the sign of the true causal effect (Goodman-Bacon 2021; Callaway and Sant'Anna 2021). Researchers must use robust staggered estimators (such as Callaway-Sant'Anna or Sun-Abraham).""",
        r"""Cedar Capital studies the impact of a market microstructure rule change on trading volume across two groups of equities:
- **Treated Stocks**: Pre-treatment average volume is $\bar{y}_{T, pre} = 10.0$ million shares; post-treatment volume rises to $\bar{y}_{T, post} = 14.0$ million shares.
- **Comparison Stocks**: Pre-treatment volume is $\bar{y}_{C, pre} = 8.0$ million shares; post-treatment volume rises to $\bar{y}_{C, post} = 10.0$ million shares.

1. **Calculate the simple treated change**:
   $$\Delta \bar{y}_T = \bar{y}_{T, post} - \bar{y}_{T, pre} = 14.0 - 10.0 = +4.0 \text{ million shares}$$
   A naive analyst observing this $+4.0$ jump might attribute the entire increase to the new policy rule.
2. **Calculate the comparison group change (macro secular trend)**:
   $$\Delta \bar{y}_C = \bar{y}_{C, post} - \bar{y}_{C, pre} = 10.0 - 8.0 = +2.0 \text{ million shares}$$
   The comparison group also experienced a $+2.0$ million increase due to general market-wide liquidity growth.
3. **Calculate the Difference-in-Differences causal contrast**:
   $$\text{DiD} = \Delta \bar{y}_T - \Delta \bar{y}_C = 4.0 - 2.0 = +2.0 \text{ million shares}$$
   Subtracting the control group's trend isolates the true net policy impact: $+2.0$ million shares.
4. **Threat to identification**:
   If an algorithmic market maker launched new automated trading programs exclusively on the treated stocks during the post-period, that contemporaneous shock would contaminate the $+2.0$ estimate, violating parallel counterfactual trends.""",
        r"""In quasi-experimental research:
- **Inspect pre-treatment leads**: Plot event-study coefficients with 95% confidence bands. If pre-treatment coefficients exhibit a pre-existing trend, parallel trends fails, and DiD is invalid.
- **Audit spillovers and stable unit treatment value (SUTVA)**: Verify that treating group $T$ did not divert order flow or liquidity away from control group $C$.
- **Avoid naive TWFE with staggered timing**: In panels where firms enter treatment in waves, use cohort-specific Callaway-Sant'Anna estimators rather than a single pooled interaction dummy.""",
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
        r"""In quantitative credit risk and market timing, the dependent variable is frequently binary ($y_i \in \{0, 1\}$): Will a corporate bond issuer default? Will the central bank hike interest rates? Will an earnings announcement trigger a gap breakout?

Attempting to model binary outcomes with OLS (the **Linear Probability Model, LPM**: $P(y_i=1|x) = \mathbf{x}_i^T\boldsymbol{\beta}$) is fundamentally flawed:
- Fitted probabilities can lie outside the logical $[0, 1]$ interval (e.g., predicting $-0.15$ or $+1.30$).
- Disturbances are mechanically heteroskedastic ($Var(u_i|x) = p_i(1 - p_i)$) and non-normal.

**Logistic Regression (Logit)**:
The logit model maps a continuous linear index $z_i = \mathbf{x}_i^T\boldsymbol{\beta}$ onto the strictly bounded interval $(0, 1)$ via the **standard logistic cumulative distribution function**:

$$p(x_i) = P(y_i = 1 | \mathbf{x}_i) = \Lambda(\mathbf{x}_i^\top \boldsymbol{\beta}) = \frac{1}{1 + e^{-\mathbf{x}_i^\top \boldsymbol{\beta}}} = \frac{e^{\mathbf{x}_i^\top \boldsymbol{\beta}}}{1 + e^{\mathbf{x}_i^\top \boldsymbol{\beta}}}$$

Inverting this function yields the **log-odds (logit)**:
$$\ln\left(\frac{p_i}{1 - p_i}\right) = \mathbf{x}_i^\top \boldsymbol{\beta}$$
where $\frac{p_i}{1 - p_i}$ is the **odds ratio**.
**Crucial Coefficient Interpretation**: The slope $\beta_j$ represents the change in the *log-odds* of the event occurring per unit change in $x_j$, holding other regressors constant. It is **not** a constant change in probability!

**Non-Linear Marginal Effects**:
The marginal effect of regressor $x_j$ on the probability $p_i$ is non-linear and depends directly on the baseline probability level:

$$\frac{\partial P(y=1|\mathbf{x})}{\partial x_j} = \beta_j \times p_i(1 - p_i)$$

- When $p_i = 0.50$, $p(1 - p) = 0.25$ (maximum responsiveness to changes in $x$).
- When $p_i = 0.95$, $p(1 - p) = 0.0475$ (compressed responsiveness near the probability boundary).

**Maximum Likelihood Estimation (MLE)**:
Parameters are estimated by maximizing the log-likelihood function across $n$ independent Bernoulli trials:
$$\ln L(\boldsymbol{\beta}) = \sum_{i=1}^n \left[y_i \ln(p_i) + (1 - y_i) \ln(1 - p_i)\right]$$
**Event Probability vs. Expected Economic Payoff**:
A trading system that predicts a $75\%$ probability of price increase does **not** guarantee a profitable trading strategy if the average loss on a false alarm is $-10\%$ while the average gain is only $+2\%$. Expected economic payoff integrates probability with payoff magnitude and execution costs.""",
        r"""Cedar Capital calibrates a logistic regression model for corporate bond default screening:
$$\ln\left(\frac{p_i}{1 - p_i}\right) = \beta_0 + \beta_1 x_i$$
with estimated slope coefficient $\hat{\beta}_1 = 0.80$.

1. **Calculate probability when linear index is zero ($z_i = 0$)**:
   $$p(0) = \frac{1}{1 + e^{-0}} = \frac{1}{1 + 1} = 0.50 \text{ (50.0\% default probability)}$$
   - Odds of default: $\frac{0.50}{1 - 0.50} = 1.00$ (even odds: 1 to 1).
   - Local marginal derivative with respect to $x$:
     $$\frac{\partial p}{\partial x} = \hat{\beta}_1 \times p(1 - p) = 0.80 \times 0.50 \times (1 - 0.50) = 0.80 \times 0.25 = +0.20 \text{ (or } +20 \text{ bps per unit)}$$
2. **Calculate probability when linear index is $z_i = \ln(3) \approx 1.0986$**:
   $$p(\ln 3) = \frac{1}{1 + e^{-\ln 3}} = \frac{1}{1 + \frac{1}{3}} = \frac{1}{4/3} = \frac{3}{4} = 0.75 \text{ (75.0\% default probability)}$$
   - Odds of default: $\frac{0.75}{1 - 0.75} = \frac{0.75}{0.25} = 3.00$ (3 to 1 odds).
   - Notice that odds tripled from $1$ to $3$ because the index increased by $\ln(3)$.
3. **Contrast local responsiveness near probability boundaries**:
   If an issuer has an existing default probability $p_i = 0.95$:
   $$\frac{\partial p}{\partial x} = 0.80 \times 0.95 \times (1 - 0.95) = 0.80 \times 0.0475 = +0.038 \text{ (only } +3.8 \text{ bps per unit)}$$
   Due to the sigmoid logistic curve, the same slope $\beta_1 = 0.80$ produces over $5\times$ smaller probability sensitivity at $p = 0.95$ than at $p = 0.50$.""",
        r"""When developing binary classification pipelines:
- **Report Average Marginal Effects (AME)**: Because marginal effects vary across observations, report the sample average $\frac{1}{n}\sum \hat{\beta}_j p_i(1 - p_i)$ alongside log-odds coefficients.
- **Audit Quasi-Complete Separation**: If a regressor perfectly separates the classes (e.g., all defaulting firms have negative cash flow), standard MLE fails, and parameter estimates explode toward $\pm \infty$. Apply Firth's penalized likelihood.
- **Calibrate probability predictions using Brier Score**: High classification accuracy does not mean probabilities are calibrated. Evaluate the Brier Score ($\frac{1}{n}\sum (\hat{p}_i - y_i)^2$) and reliability diagrams before using probabilities in position sizing.""",
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
    # -------------------------------------------------------------------------
    # UNIT 7: RISK AND RESEARCH CREDIBILITY
    # -------------------------------------------------------------------------

    add(
        "3.4",
        7,
        "Risk and downside metrics",
        "Define empirical quantiles, expected shortfall, drawdown, and exceedance checks with explicit signs and horizons.",
        r"""Financial risk measurement quantifies downside exposure over a specified holding period under extreme market conditions. Relying exclusively on standard deviation ($\sigma$) fails because financial asset returns exhibit negative skewness, fat tails (leptokurtosis), and asymmetric downside correlation surges.

Institutional risk frameworks deploy three complementary downside metrics:

1. **Value at Risk (VaR)**:
   For horizon $T$ and confidence level $1 - \alpha$ (e.g., $95\%$ or $99\%$), $\text{VaR}_{1-\alpha}$ represents the threshold dollar loss or percentage return loss $L$ such that the probability of exceeding $L$ is at most $\alpha$:
   $$P(L \ge \text{VaR}_{1-\alpha}) \le \alpha \iff \text{VaR}_{1-\alpha} = Q_{1-\alpha}(L)$$
   **Critical Boundary**: VaR is a quantile boundary, **not the maximum possible loss**! It provides zero information regarding loss severity once the threshold is breached.
2. **Expected Shortfall (ES / Conditional VaR)**:
   The conditional average loss in the worst $(1 - \alpha)$ tail:
   $$\text{ES}_{1-\alpha} = E\left[L \;\big|\; L \ge \text{VaR}_{1-\alpha}\right]$$
   Expected Shortfall is mathematically **coherent** (Artzner et al. 1999)—satisfying subadditivity ($\rho(A + B) \le \rho(A) + \rho(B)$)—and captures extreme tail crash severity.
3. **Maximum Drawdown (MDD)**:
   Drawdown measures path-dependent wealth erosion from a historical peak $E_{\tau}$ to a subsequent trough $E_t$:
   $$\text{DD}_t = \frac{E_t}{\max_{s \le t} E_s} - 1 \in [-1, 0]$$
   $$\text{MDD} = \min_{t \in [0, T]} \text{DD}_t$$
   Due to compounding asymmetry, a $-50\%$ drawdown requires a $+100\%$ return to recover capital, while a $-90\%$ drawdown requires a $+900\%$ surge.

**Quantile Conventions in Finite Samples**:
Calculating empirical quantiles on small samples depends heavily on discrete sorting conventions: nearest-rank vs. linear interpolation, and whether boundary threshold observations strictly belong to the tail average. A risk report must explicitly state its quantile algorithm.""",
        r"""Cedar Capital evaluates the historical drawdown and tail losses of a systematic strategy across a 10-observation sample:
Ordered loss observations (in thousands of dollars, where positive values denote cash losses):
$$\mathbf{L} = [1, 2, 3, 4, 5, 6, 7, 8, 9, 20]$$

1. **Calculate Nearest-Rank 90% VaR**:
   With $n = 10$ observations, the $90\%$ quantile rank index is $k = \lceil 0.90 \times 10 \rceil = 9$.
   The 9th ordered observation is $L_{(9)} = \$9{,}000$.
   Therefore, $90\%$ VaR is **$\$9{,}000$**. Exactly $90\%$ of days experienced losses of $\$9{,}000$ or less.
2. **Calculate Expected Shortfall (ES)**:
   - Under a strictly-above-threshold tail definition ($L > \text{VaR}_{90\%}$):
     The tail contains only the single extreme loss $L_{(10)} = \$20{,}000$.
     $$\text{ES}_{strict} = \$20{,}000$$
   - Under a weak tail definition including the boundary quantile ($L \ge \text{VaR}_{90\%}$):
     $$\text{ES}_{inclusive} = \frac{9 + 20}{2} = \$14{,}500$$
   Notice that while $90\%$ VaR is $\$9{,}000$, the realized tail crash loss is $\$20{,}000$—more than double the VaR threshold!
3. **Calculate Drawdown and Asymmetric Recovery**:
   Suppose the fund's peak equity was $\$200{,}000$ and subsequently plunged to $\$150{,}000$:
   $$\text{Drawdown} = \frac{150{,}000}{200{,}000} - 1 = 0.75 - 1 = -0.25 \implies \mathbf{-25.0\%}$$
   To recover from $\$150{,}000$ back to the original $\$200{,}000$ peak:
   $$\text{Required Gain} = \frac{200{,}000}{150{,}000} - 1 = 1.3333 - 1 = \mathbf{+33.33\%}$$
   Because the capital denominator shrank from $200$ to $150$, recovery requires a $33.33\%$ gain to offset a $25\%$ decline.""",
        r"""In systematic risk protocols:
- **Perform Kupiec POF Backtests on VaR**: Count historical exceedances where loss $L_t > \text{VaR}_t$. If a $95\%$ VaR model produces 15 exceedances over 100 days (15% failure rate vs. 5% expected), reject the risk model.
- **Check for Exceedance Clustering (Christoffersen Test)**: A risk model may achieve the correct average exceedance rate over 5 years yet have all its failures cluster within three consecutive panic days.
- **Pair quantitative statistics with scenario stress testing**: Statistical quantiles reflect past sample regimes; stress tests evaluate survival under unprecedented forward structural ruptures.""",
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
        r"""Classical analytical standard errors and $t$-tests rely on asymptotic distribution theory (such as the Central Limit Theorem) and strong parametric assumptions (e.g., normal or Student's $t$ innovations). When sample sizes are modest or return distributions exhibit extreme fat tails and skewness, analytical approximations can be severely biased.

The **Bootstrap** (Efron 1979) approximates the finite-sample distribution of an estimator $\hat{\theta} = T(\mathbf{X})$ by repeatedly resampling with replacement from the observed empirical dataset:
$$\mathbf{X}^{*(b)} \xrightarrow{sample} \hat{\theta}^{*(b)} = T(\mathbf{X}^{*(b)}), \quad b = 1 \dots B$$

**The Catastrophic Failure of I.I.D. Resampling**:
In standard textbook bootstrap, individual rows are drawn independently with replacement. In financial time series, **independent row resampling fails catastrophically**:
- Permuting individual rows completely destroys the chronological time order.
- It wipes out all autocorrelation, volatility clustering, and lead-lag dynamics.
- An analyst bootstrapping an autoregressive model using independent row draws severely underestimates confidence intervals.

**Block Bootstrap Methods for Dependent Time Series**:
To preserve temporal dependence, researchers use **Block Bootstrapping** (Künsch 1989):
1. **Moving-Block Bootstrap (MBB)**: Groups the $T$ time-series observations into overlapping contiguous blocks of length $L$: $\mathbf{B}_t = [y_t, y_{t+1}, \dots, y_{t+L-1}]$. Drawing $k = \lceil T / L \rceil$ blocks with replacement and concatenating them preserves within-block serial autocorrelation and conditional heteroskedasticity.
2. **Stationary Bootstrap (Politis and Romano 1994)**: Resamples blocks of random length drawn from a geometric distribution with mean block length $L = 1/p$, ensuring that the resampled pseudo-series is strictly stationary.

**The Block Length Trade-Off**:
Selecting the optimal block length $L$ balances a fundamental trade-off:
- **Too short ($L \to 1$)**: Fails to capture multi-lag serial dependence, biasing standard errors downward toward the naive i.i.d. assumption.
- **Too long ($L \to T$)**: Preserves dependence perfectly, but dramatically reduces the number of effectively distinct pseudo-samples ($T/L \to 1$), exploding the variance of the bootstrap estimator.""",
        r"""Cedar Capital evaluates an autoregressive trading spread across a 12-month sample ($T = 12$):
- Chosen block length: $L = 3$ consecutive months.
- Number of blocks required to assemble one full synthetic history:
  $$k = \frac{T}{L} = \frac{12}{3} = 4 \text{ contiguous blocks}$$

1. **Construct a pseudo-replicate history**:
   Draw four block indices with replacement from the available contiguous blocks:
   $$\text{Draws} = \{\mathbf{B}_2, \mathbf{B}_7, \mathbf{B}_2, \mathbf{B}_5\}$$
   Each block preserves the internal 3-month dependence structure: $\mathbf{B}_2 = [y_2, y_3, y_4]$. Concatenating the four blocks yields a 12-observation pseudo-series $\mathbf{y}^{*(1)}$.
2. **Calculate bootstrap quantile confidence intervals**:
   Across $B = 5$ illustrative bootstrap replications, estimated alpha coefficients are:
   $$\hat{\boldsymbol{\alpha}}^* = [0.10, 0.20, 0.30, 0.40, 0.50]$$
   - Under nearest-rank empirical quantile indexing:
     - 20th percentile ($k = \lceil 0.20 \times 5 \rceil = 1$): $0.10$.
     - 80th percentile ($k = \lceil 0.80 \times 5 \rceil = 4$): $0.40$.
   - The illustrative $[20\%, 80\%]$ bootstrap interval is $[0.10, 0.40]$.
   In production research, analysts generate $B = 1{,}000$ to $10{,}000$ bootstrap replicates to construct smooth 95% percentile or BCa (bias-corrected and accelerated) intervals.""",
        r"""In systematic empirical research:
- **Always refit the entire estimation algorithm in each bootstrap loop**: If the strategy includes hyperparameter selection, feature standardization, or PCA decomposition, run the *entire pipeline* on each resampled dataset $\mathbf{X}^{*(b)}$. Bootstrapping only the final regression residual ignores estimation uncertainty in preceding stages.
- **Audit sensitivity to block length**: Compute bootstrap intervals across candidate block lengths $L \in \{3, 6, 12\}$. If standard errors jump by $50\%$ when moving from $L=3$ to $L=6$, long-memory autocorrelation is present.
- **Bootstrapping does not create new empirical regimes**: Resampling cannot invent unprecedented market crashes that never occurred in the historical sample.""",
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
        r"""In systematic algorithmic trading and empirical factor discovery, researchers rarely test a single isolated hypothesis. An analyst routinely tests dozens or hundreds of indicator variants, lookback windows, universe filters, and entry/exit thresholds. This process generates acute **Multiple Testing Bias** (data-snooping / $p$-hacking).

When testing $m$ independent true null hypotheses at a nominal significance level $\alpha = 0.05$:
- The probability of a false positive on a single test is $\alpha = 0.05$.
- The probability of at least one false discovery across $m$ tests—the **Family-Wise Error Rate (FWER)**—explodes exponentially:
  $$\text{FWER} = 1 - (1 - \alpha)^m$$
For $m = 20$ independent tests:
$$\text{FWER} = 1 - (1 - 0.05)^{20} = 1 - (0.95)^{20} = 1 - 0.3585 \approx 0.6415 \implies \mathbf{64.15\%}$$
There is a $64\%$ probability of discovering a "statistically significant" trading rule ($p < 0.05$) purely by random chance when zero real signal exists! If the analyst explores 100 variants, the false discovery probability exceeds $99.4\%$.

**Multiple Testing Corrections**:
1. **Bonferroni Single-Step Correction**:
   To guarantee that the family-wise error rate is bounded by $\alpha_{family}$, each individual hypothesis is tested at the adjusted threshold:
   $$\alpha_{individual} = \frac{\alpha_{family}}{m}$$
   Bonferroni provides strict FWER control, but is conservative when tests are positively correlated.
2. **Holm-Bonferroni Step-Down Procedure**:
   Sorts $p$-values in ascending order ($p_{(1)} \le p_{(2)} \le \dots \le p_{(m)}$) and compares $p_{(i)} \le \frac{\alpha_{family}}{m - i + 1}$, providing strictly greater statistical power than Bonferroni while preserving FWER.
3. **False Discovery Rate (FDR - Benjamini and Hochberg 1995)**:
   Instead of preventing *any* false positives, FDR controls the expected proportion of false discoveries among all rejected hypotheses ($E\left[\frac{FP}{FP + TP}\right] \le q$). In large factor discovery screening ($m = 10{,}000$), FDR is far more powerful than Bonferroni.

**The Research Ledger and Publication Bias**:
The "research family" $m$ includes **every failed, abandoned, or unpublished trial variant** tested during strategy development. Discarding 99 failed strategies and submitting only the single "winning" strategy with its unadjusted $p$-value is academic and scientific fraud.""",
        r"""Cedar Capital evaluates $m = 20$ trading factor strategies generated during a quantitative exploratory sprint. The committee requires family-wise error control at the $\alpha_{family} = 0.05$ significance level.
Across the 20 trials, the single best strategy achieves an unadjusted raw $p$-value of $p_{(1)} = 0.010$.

1. **Calculate the Bonferroni significance threshold**:
   $$\alpha_{individual} = \frac{\alpha_{family}}{m} = \frac{0.05}{20} = 0.0025$$
2. **Evaluate the hypothesis test**:
   - The raw $p$-value ($0.010$) is less than $0.05$, which would lead a naive researcher to claim a discovery.
   - However, comparing against the Bonferroni threshold:
     $$p_{(1)} = 0.010 > 0.0025 = \alpha_{individual}$$
   The strategy **fails to achieve statistical significance** under multiple-testing correction! The apparent edge is fully consistent with a false positive generated by testing 20 random paths.
3. **Calculate independent family false-positive probability**:
   If all 20 strategies were pure random noise:
   $$P(\ge 1 \text{ false discovery}) = 1 - (1 - 0.05)^{20} = 1 - 0.358486 \approx 0.6415 \implies 64.15\%$$
   There was a nearly two-thirds probability of finding at least one rule with $p < 0.05$ by chance alone.""",
        r"""In systematic factor discovery pipelines:
- **Maintain an automated, immutable research ledger**: Log every backtest iteration, parameter permutation, data transformation, and outcome in an automated database.
- **Compute the Deflated Sharpe Ratio (DSR)**: Use López de Prado's DSR formulation, which adjusts a strategy's observed Sharpe ratio for the number of trials $m$, variance of trials, skewness, and kurtosis.
- **Pre-register confirmatory validation sets**: Separate exploratory research from confirmatory validation. A strategy selected from $m$ trials must be tested once on an untouched, pre-registered future dataset.""",
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
        r"""A statistically significant regression coefficient or predictive factor signal is an incomplete investment hypothesis. A statistical finding only becomes an investable algorithmic strategy after specifying exact execution rules, order timing, capacity constraints, and transaction cost modeling.

The majority of quantitative trading strategies that look spectacular in backtests fail immediately upon live deployment due to five structural backtest traps:

1. **Execution Chronology and Look-Ahead Fills**:
   - If a trading signal is generated from closing market prices at date $t$ ($C_t$), **the trade cannot execute at $C_t$**. The official closing price is finalized only after trading halts.
   - The earliest physically executable fill occurs at the opening price of the next trading session ($O_{t+1}$), or via pre-market orders. Assuming execution at $C_t$ or intra-bar lows ($L_t$) fabricates impossible profits.
2. **Transaction Costs and Portfolio Turnover Drag**:
   Net realized returns must subtract all trading frictions:
   $$r_{net} \approx r_{gross} - \text{Turnover} \times \text{Cost}_{one\text{-}way}$$
   where $\text{Cost}_{one\text{-}way}$ accounts for broker commissions, exchange fees, bid-ask spread crossing ($\frac{Spread}{2}$), and non-linear market impact ($\Delta P \propto \sigma \sqrt{\frac{V}{ADV}}$). A high-turnover strategy can easily consume $400$ basis points of gross alpha in transaction friction!
3. **Survivorship Bias in Universe Construction**:
   Constructing a historical universe using today's index constituents (e.g., today's S&P 500) systematically drops all companies that went bankrupt, were acquired, or delisted over the past 20 years, inflating historical strategy returns by $100 \text{ to } 300$ basis points annually.
4. **Data Restatement Leakage**:
   Using revised accounting numbers published in 2026 to backtest trades in 2020 introduces look-ahead information that was physically unknown to historical market participants.
5. **Overlapping Label Autocorrelation**:
   Multi-period holding horizons (e.g., holding a position for 20 days) cause neighboring backtest rows to share future price outcomes, requiring purged and embargoed evaluation.""",
        r"""Cedar Capital audits a proposed algorithmic strategy evaluated over a 1-year backtest window:
- Gross backtest return: $+8.0\%$ ($0.080$).
- Baseline one-way transaction cost (spread crossing + commission): $20$ basis points ($0.0020$).
- Low-Turnover Case: Strategy executes $6$ one-way portfolio turns per year.
- High-Turnover Case: Strategy executes $20$ one-way portfolio turns per year.

1. **Calculate net return under low turnover ($6$ turns)**:
   - Annual turnover friction drag:
     $$\text{Cost} = 6 \times 0.0020 = 0.0120 \implies 1.20\%$$
   - Net realized return:
     $$r_{net} = 0.080 - 0.0120 = 0.0680 \implies \mathbf{+6.80\%}$$
   The strategy preserves $+6.80\%$ net alpha.
2. **Calculate net return under high turnover ($20$ turns)**:
   - Annual turnover friction drag:
     $$\text{Cost} = 20 \times 0.0020 = 0.0400 \implies 4.00\%$$
   - Net realized return:
     $$r_{net} = 0.080 - 0.0400 = 0.0400 \implies \mathbf{+4.00\%}$$
   Half of the entire gross profit ($4.0\%$) is completely consumed by execution fees!
3. **Examine timing distortion**:
   Suppose a signal generated from Monday's close ($P = 100$) assumes an immediate fill at $100$. In live trading, the order executes at Tuesday's open ($P = 103$). That single $+3\%$ slippage gap can turn an apparent $+8\%$ strategy into an annual loss.""",
        r"""In systematic quantitative development:
- **Enforce Next-Open Execution**: Configure backtesting engines to calculate signals at close $t$ and generate fills at open $t+1$.
- **Build Survivorship-Free Universes**: Maintain historical constituent membership tables with accurate delisting returns ($R_{delist} \in [-100\%, -30\%]$).
- **Stress Test Cost Multipliers**: Double and triple assumed slippage parameters ($2\times$ and $3\times$ spread costs). If a strategy collapses when slippage rises from 10 bps to 20 bps, it is an unviable execution trap.""",
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

    # -------------------------------------------------------------------------
    # UNIT 8: REPLICATION PROJECTS AND CAPSTONE
    # -------------------------------------------------------------------------

    add(
        "3.29",
        8,
        "Project: replicate a factor regression with HAC",
        "Run an actual regression pipeline and reconcile point estimates, covariance conventions, and held-out prediction errors.",
        r"""In institutional quantitative research, mathematical theory must be implemented through verified, reproducible computational pipelines. The first replication project tasks the researcher with downloading and executing the quantitative research lab suite ([`quant_research_lab.py`](/course-assets/research/quant_research_lab.py)), verifying OLS parameter estimation, contrasting conventional vs. Newey-West HAC covariance matrices, and measuring out-of-sample prediction loss.

The replication pipeline enforces three foundational empirical disciplines:

1. **Strict Chronological Data Partitioning**:
   The historical dataset is partitioned into an in-sample **training split** ($t = 1 \dots T_{train}$) and an out-of-sample **held-out test split** ($t = T_{train}+1 \dots T$).
   - The OLS parameter vector $\hat{\boldsymbol{\beta}}$ is fitted exclusively on training rows:
     $$\hat{\boldsymbol{\beta}} = (\mathbf{X}_{train}^T \mathbf{X}_{train})^{-1} \mathbf{X}_{train}^T \mathbf{y}_{train}$$
   - Any data normalization (mean centering or scaling) must be fitted on training rows and applied forward without refitting.
2. **Reconciliation of Covariance Conventions**:
   Under OLS, point estimates $\hat{\boldsymbol{\beta}}$ are identical whether reported with conventional homoskedastic standard errors or Newey-West HAC standard errors. The covariance matrix convention alters hypothesis tests ($t$-statistics and $p$-values); it does **not** alter the fitted regression line.
3. **Out-of-Sample Prediction Scoring**:
   Predicted outcomes on the test partition are generated using held-out factor realizations: $\hat{y}_t = \mathbf{x}_{t, test}^T \hat{\boldsymbol{\beta}}$.
   Model generalization is quantified using test Mean Squared Error:
   $$\text{MSE}_{test} = \frac{1}{n_{test}} \sum_{t \in test} \left(y_t - \hat{y}_t\right)^2$$
   **Important Pedagogical Note**: Evaluating test returns conditional on realized future factor values is a **conditional return explanation**, *not* an ex-ante forecast of unknown future factor returns.""",
        r"""Cedar Capital runs a hand-calculation verification fixture to audit the local Python script's mathematical engine:
Three historical paired observations:
$$\mathbf{x} = [-1.0, 0.0, 1.0], \quad \mathbf{y} = [-1.0, 1.0, 3.0]$$

1. **Fit the training regression**:
   - Means: $\bar{x} = 0.0, \; \bar{y} = 1.0$.
   - Slope: $\hat{\beta} = \frac{\sum (x_i - 0)(y_i - 1)}{\sum (x_i - 0)^2} = \frac{(-1 \times -2) + (0 \times 0) + (1 \times 2)}{(-1)^2 + 0^2 + 1^2} = \frac{2 + 2}{1 + 1} = \frac{4}{2} = 2.00$.
   - Intercept: $\hat{\alpha} = \bar{y} - \hat{\beta}\bar{x} = 1.0 - (2.0 \times 0.0) = 1.00$.
   The fitted model is $\hat{y} = 1.00 + 2.00 x$.
2. **Evaluate out-of-sample prediction error**:
   A held-out test observation arrives with factor value $x_{test} = 2.00$ and realized outcome $y_{test} = 6.00$:
   - Model prediction: $\hat{y}_{test} = 1.00 + (2.00 \times 2.00) = 5.00$.
   - Model squared error: $(y_{test} - \hat{y}_{test})^2 = (6.00 - 5.00)^2 = 1.00^2 = 1.00$.
3. **Compare against naive training-mean baseline**:
   The baseline predicts the historical sample mean $\bar{y}_{train} = 1.00$:
   - Baseline squared error: $(y_{test} - \bar{y}_{train})^2 = (6.00 - 1.00)^2 = 5.00^2 = 25.00$.
   The model achieves a $96\%$ error reduction ($1.00$ vs $25.00$) on this case.""",
        r"""When conducting local code replication:
- **Verify virtual environment reproducibility**: Run `pip install -r requirements.txt` and confirm NumPy, SciPy, and statsmodels package versions match the environment manifest.
- **Audit training/test isolation**: Verify that altering test set outcomes alters test MSE while leaving training point estimates $\hat{\alpha}, \hat{\beta}$ identically unchanged.
- **Synthetic data disclosure**: Disclose that the research lab uses seeded synthetic data with known generating parameters. Synthetic simulation proves code execution integrity; it does not constitute historical alpha.""",
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
        r"""The second replication project tasks the researcher with diagnosing long-run equilibrium relationships in multivariate time series using the Engle-Granger cointegration engine. The local research lab generates a non-stationary random-walk driver $x_t \sim I(1)$ and a cointegrated series $y_t = 1.5 x_t + s_t$, where $s_t$ follows a stationary autoregressive mean-reverting process.

The research protocol requires executing four systematic diagnostic stages:

1. **Unit Root Verification on Individual Series**:
   Verify that both raw series are integrated of order one ($I(1)$) using the Augmented Dickey-Fuller (ADF) test on levels and first differences.
2. **First-Stage Long-Run Levels Estimation**:
   Fit the static cointegrating regression via OLS:
   $$y_t = \alpha + \beta x_t + s_t$$
   and extract the estimated equilibrium spread residuals $\hat{s}_t = y_t - \hat{\alpha} - \hat{\beta} x_t$.
3. **Engle-Granger Residual Cointegration Test**:
   Execute the residual unit-root test using Phillips-Ouliaris / Engle-Granger non-standard critical values. Rejecting the null hypothesis ($p < 0.05$) establishes statistical cointegration.
4. **Error-Correction Dynamics and Half-Life Estimation**:
   Model spread adjustment speed:
   $$s_t = \phi s_{t-1} + u_t \implies h_{1/2} = \frac{\ln(0.5)}{\ln(\phi)}$$

**The Negative Control Requirement**:
A rigorous scientific experiment must include a **negative control**: a deliberately broken specification where $x$ and $y$ are independent un-cointegrated random walks. If the econometric test falsely claims cointegration on the negative control, the diagnostic pipeline is misspecified.""",
        r"""Cedar Capital runs a hand-calculation verification fixture for the cointegration diagnostic engine:
The estimated long-run regression is:
$$y_t = 0.50 + 1.40 x_t + s_t$$

1. **Calculate the equilibrium spread residual**:
   At a test observation date with $x_t = 20.00$ and $y_t = 29.50$:
   $$\hat{s}_t = 29.50 - 0.50 - (1.40 \times 20.00) = 29.00 - 28.00 = +1.00$$
   The spread is $+1.00$ unit above long-run equilibrium.
2. **Estimate the spread mean-reversion half-life**:
   The estimated autoregressive persistence coefficient for the residual spread is $\hat{\phi} = 0.60$.
   $$h_{1/2} = \frac{\ln(0.5)}{\ln(\hat{\phi})} = \frac{\ln(0.5)}{\ln(0.60)} \approx \frac{-0.693147}{-0.510826} \approx 1.357 \text{ observation periods}$$
   Deviations from equilibrium are expected to decay by half in approximately $1.36$ periods.
3. **Diagnose a structural break in the hedge ratio**:
   Suppose in the second half of the sample, an economic policy shock shifts the true hedge slope from $1.40$ to $2.00$.
   A naive full-sample pooled regression estimates an intermediate slope ($\hat{\beta} \approx 1.70$), which fits neither period, causing the residuals to appear non-stationary and destroying statistical cointegration! Subsample stability audits are essential.""",
        r"""In systematic time-series project audits:
- **Save full simulation seeds**: Record random number generator seeds (`seed=42`) and sample lengths ($T = 500$) to enable bit-for-bit replication.
- **Distinguish statistical cointegration from tradable pairs**: A cointegration test evaluates mathematical stationarity; it does not account for exchange fees, borrow availability, margin haircuts, or slippage.
- **Never omit the negative control experiment**: Document that the cointegration test correctly fails to reject the null hypothesis on independent random walks.""",
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
        r"""The third replication project evaluates portfolio risk modeling and dynamic capital allocation. An institutional investment committee must review an allocation strategy under multiple competing risk estimation models: sample covariance, Ledoit-Wolf shrinkage, dynamic GARCH volatility recursions, and correlation stress tests.

A rigorous risk model audit evaluates three core dimensions:

1. **Covariance Estimator Sensitivity**:
   Portfolio variance $\sigma_p^2 = \mathbf{w}^T \boldsymbol{\Sigma} \mathbf{w}$ is highly sensitive to the covariance estimator:
   - **Sample Covariance ($\mathbf{S}$)**: Unbiased but noisy, with extreme eigenvalue dispersion that causes optimizers to over-allocate to spuriously low-volatility assets.
   - **Shrunk Covariance ($\hat{\boldsymbol{\Sigma}}_{shrink}$)**: Blends sample covariance with a structured diagonal or constant-correlation target, pulling extreme weights toward equal weighting.
2. **Dynamic Conditional Volatility Recursion**:
   Tracking time-varying asset volatility using GARCH(1,1):
   $$h_t = \omega + \alpha u_{t-1}^2 + \beta h_{t-1}$$
   Updating volatility forecasts dynamically allows risk managers to proactively size positions down before volatility surges breach fund limits.
3. **Adverse Correlation Stress Scenarios**:
   During market liquidity panics, cross-asset correlations surge toward $+1.00$. A risk review must re-evaluate portfolio risk under stressed correlation assumptions ($\rho \to 1.0$) to verify that capital reserves and margin limits survive extreme market contagion.""",
        r"""Cedar Capital audits a two-asset portfolio ($w_1 = 0.50, w_2 = 0.50$) across three distinct risk models:
- Asset 1 variance: $S_{11} = 0.040$ ($\sigma_1 = 20\%$).
- Asset 2 variance: $S_{22} = 0.090$ ($\sigma_2 = 30\%$).
- Sample covariance: $S_{12} = 0.018$ (sample correlation $\rho = \frac{0.018}{0.20 \times 0.30} = 0.30$).

1. **Model 1: Sample Covariance Allocation**:
   $$\sigma_{p, sample}^2 = (0.25 \times 0.040) + (0.25 \times 0.090) + (0.50 \times 0.018) = 0.0100 + 0.0225 + 0.0090 = 0.0415$$
   $$\sigma_{p, sample} = \sqrt{0.0415} \approx 0.2037 \implies 20.37\% \text{ volatility}$$
2. **Model 2: Covariance Shrinkage (50% toward diagonal target)**:
   Shrunk covariance: $\hat{\Sigma}_{12} = 0.50 \times 0.018 = 0.0090$.
   $$\sigma_{p, shrunk}^2 = 0.0100 + 0.0225 + (0.50 \times 0.0090) = 0.0325 + 0.0045 = 0.0370$$
   $$\sigma_{p, shrunk} = \sqrt{0.0370} \approx 0.1924 \implies 19.24\% \text{ volatility}$$
   Shrinkage lowers modeled portfolio risk by reducing estimated covariance.
3. **Model 3: Crisis Correlation Stress ($\rho \to 1.00$)**:
   Under perfect correlation, covariance surges to $\Sigma_{12} = 1.00 \times 0.20 \times 0.30 = 0.0600$.
   $$\sigma_{p, stress}^2 = 0.0100 + 0.0225 + (0.50 \times 0.0600) = 0.0325 + 0.0300 = 0.0625$$
   $$\sigma_{p, stress} = \sqrt{0.0625} = 0.2500 \implies \mathbf{25.00\% \text{ volatility}}$$
   In a panic, portfolio volatility jumps from $19.24\%$ to $25.00\%$, increasing margin requirements by over $30\%$.
4. **Dynamic GARCH check**:
   With $\omega = 0.010, \alpha = 0.10, \beta = 0.80$, squared shock $u_{t-1}^2 = 0.040$, and prior variance $h_{t-1} = 0.090$:
   $$h_t = 0.010 + (0.10 \times 0.040) + (0.80 \times 0.090) = 0.010 + 0.004 + 0.072 = 0.086 \text{ squared units}$$""",
        r"""In institutional risk committee reporting:
- **Never present a single risk number**: Always present a tripartite risk matrix: baseline sample estimate, regularized shrunk estimate, and stressed tail scenario.
- **Enforce variance positivity checks**: Assert $h_t > 0$ and verify that all covariance matrices are positive semi-definite before submitting portfolio weights to the execution broker.
- **Distinguish model changes from portfolio changes**: A reduction in reported portfolio risk from shrinkage is an estimator adjustment, not a physical reduction in market risk.""",
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
        r"""The capstone of applied financial econometrics is synthesizing data engineering, econometric modeling, robust statistical inference, risk analysis, and execution economics into a comprehensive, decision-ready **Research Dossier**.

Investment committees and capital allocators evaluate quantitative proposals through a rigorous scientific audit. The analyst's objective is not to present a cosmetically optimized backtest curve, but to transparently document the research sieve, stress-test empirical assumptions, and establish credible decision boundaries.

A complete Cedar Research Dossier is evaluated across a **100-point rubric**:
1. **Research Question & Estimand (15 points)**: Explicitly defines whether the study addresses descriptive association, out-of-sample prediction, or structural causal effect.
2. **Data Lineage & Provenance (20 points)**: Documented data dictionary, verification of point-in-time availability timestamps ($t_{available} \le t_{decision}$), and absence of look-ahead leakage.
3. **Econometric Specification & Diagnostics (20 points)**: Functional specification, residual diagnostics, tests for multicollinearity ($VIF$), heteroskedasticity, and unit-root stationarity.
4. **Statistical Uncertainty & Selection History (20 points)**: Proper standard error conventions (White HC, Newey-West HAC, or clustered SEs) and complete disclosure of all exploratory model trials to account for multiple-testing bias.
5. **Independent Out-of-Sample Evaluation (15 points)**: Strict walk-forward evaluation on frozen, untouched test data comparing performance against a naive benchmark.
6. **Reproducibility & Decision Boundary Memo (10 points)**: Deterministic code scripts, explicit random seeds, and an actionable investment committee recommendation with operational risk controls.

**Mandatory Disqualification Conditions**:
Regardless of total rubric points, a research proposal faces **mandatory rejection** if it exhibits:
- Look-ahead data leakage (e.g., using future financial filings or test set feedback).
- Inconsistent units (e.g., mixing decimals and percentage points).
- Invalid inference conventions (e.g., using homoskedastic standard errors for overlapping time series).
- Concealment of failed exploratory variants.""",
        r"""Cedar Capital's quantitative committee reviews a final research dossier for an active equity strategy evaluated over a held-out test partition:
- Estimated factor coefficient: $\hat{\beta} = 0.40$.
- Newey-West HAC standard error: $SE_{HAC} = 0.25$.
- Model out-of-sample Mean Squared Error: $\text{MSE}_{model} = 0.80$.
- Naive benchmark Mean Squared Error: $\text{MSE}_{baseline} = 1.00$.

1. **Calculate the test statistic and confidence interval**:
   - $t$-statistic against zero ($H_0: \beta = 0$):
     $$t = \frac{\hat{\beta}}{SE_{HAC}} = \frac{0.40}{0.25} = 1.60$$
   - Asymptotic 95% Confidence Interval ($z_{0.025} = 1.96$):
     $$\text{CI}_{95\%} = 0.40 \pm (1.96 \times 0.25) = [0.40 - 0.49, \; 0.40 + 0.49] = [-0.09, \; +0.89]$$
   Notice that the interval spans zero! The parameter is statistically insignificant at the 5% level ($p \approx 0.11$).
2. **Evaluate Out-of-Sample Predictive Improvement**:
   $$\text{OOS } R^2 = 1 - \frac{\text{MSE}_{model}}{\text{MSE}_{baseline}} = 1 - \frac{0.80}{1.00} = 1 - 0.80 = \mathbf{0.20 \text{ (or } 20.0\%)}$$
   The model achieves a $20\%$ error reduction relative to the baseline.
3. **Reconcile Evidence for the Committee**:
   - The model delivers positive out-of-sample predictive improvement ($20\%$).
   - However, parameter uncertainty spans zero ($[-0.09, 0.89]$), and the factor was estimated conditional on realized contemporarous factor returns.
   - The defensible committee recommendation is: **Approve for paper-trading observation, but withhold live capital deployment until parameter stability is demonstrated over an additional out-of-sample regime.**
4. **Rubric Total**:
   $$15 + 20 + 20 + 20 + 15 + 10 = \mathbf{100 \text{ points}}$$""",
        r"""In submitting the final research capstone:
- **Submit the runnable project script**: Verify that executing `python quant_research_lab.py` runs cleanly from command line without environment errors.
- **State the strongest falsification experiment**: Explicitly propose the exact future market event or test that would disprove your hypothesis.
- **The automated exam evaluates conceptual mastery**: The multiple-choice final exam grades theoretical transfer; it does not grade the written dossier or certify a live trading hedge fund.""",
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
            "description": "A comprehensive, mathematically rigorous, and practitioner-focused curriculum in empirical financial econometrics. Master OLS and Gauss-Markov mechanics, HAC robust inference, multivariate dynamic systems, cointegration and ECMs, GARCH conditional volatility, factor modeling and shrinkage, panel data with fixed effects, instrumental variables, difference-in-differences, extreme value theory, dependent block bootstraps, and false discovery rate control. Designed with research integrity and out-of-sample discipline at every step.",
            "source": "Original Quanta course · primary statistical documentation and factor research",
            "level": "Intermediate → advanced",
            "icon": "factors",
            "studyType": "applied",
            "modules": modules,
            "prerequisites": "Single- and multivariable calculus, linear algebra (matrices, eigenvalues, projections), introductory probability and statistics (distributions, hypothesis testing), and intermediate Python with NumPy. Study Quantitative Investment Analysis first or use it alongside this course.",
            "outcomes": [
                "Define an estimand, construct point-in-time financial panels, and derive OLS algebraic and statistical properties.",
                "Diagnose heteroskedasticity and autocorrelation, applying White, Newey–West HAC, and clustered robust standard errors.",
                "Specify, diagnose, and forecast stationary time series using ARIMA and multivariate Vector Autoregressions (VAR).",
                "Test for cointegration using Engle–Granger methodology, estimate Error Correction Models (ECM), and trade mean-reverting basis relationships.",
                "Model conditional volatility with ARCH, GARCH(1,1), and GJR-GARCH asymmetric leverage specifications under fat-tailed distributions.",
                "Estimate CAPM and Fama–French multi-factor models, isolate genuine alpha, and implement covariance shrinkage and PCA decomposition.",
                "Control for unobserved entity heterogeneity with panel fixed effects and identify causal effects using instrumental variables and difference-in-differences.",
                "Apply extreme value theory, stationary block bootstraps, and false discovery rate control to assemble and defend an audited institutional research dossier.",
            ],
            "readingGuide": "Eight units and 32 original lessons, each with two practice items, a worked calculation, references, and a notebook assignment. Seven checkpoints lead to a 32-question final. The downloadable project fits actual OLS/HAC and time-series models on synthetic data, while the written capstone is self-assessed separately.",
            "parts": [
                {"id": str(i), "title": title, "description": description}
                for i, (title, description) in enumerate(parts, 1)
            ],
            "references": [
                {"title": title, "url": url}
                for title, url in [REG, DIAG, TIME, COINT, VOL, FACTORS, PANEL, IV, MULTI]
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
