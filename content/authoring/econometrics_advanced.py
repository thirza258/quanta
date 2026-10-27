"""Advanced econometrics units 8 and 9 (lessons 3.33-3.40): likelihood, moments and
asset-pricing tests; time-varying parameters and tail risk. Original lessons with
fictional data; each worksheet runs in the guided runtime and is recomputed
independently in backend/tests/test_advanced_quant_lessons.py."""

# Each entry is the argument list for applied_courses.study().
ADVANCED_LESSONS = [
    (
        '3.33',
        8,
        'Maximum likelihood and the Wald, likelihood-ratio and score tests',
        'Derive the score, information and asymptotic covariance of a maximum likelihood estimator, run the Wald, likelihood-ratio and score tests, and switch to a sandwich covariance when the density is wrong.',
        r"""Lesson 3.18 ran the GARCH variance recursion at parameters you were given, and Lesson 3.26 wrote down the Bernoulli log-likelihood of a logit. This lesson supplies the machinery behind both: how a likelihood is turned into an estimate, how far to trust it, and the three classical tests of a restriction.

**Setup.** Observations $y_1,\dots,y_n$ have conditional density $f(y_t\mid x_t;\theta)$ with $\theta\in\mathbb R^k$. The log-likelihood is $\ell_n(\theta)=\sum_t\ln f(y_t\mid x_t;\theta)$ and the maximum likelihood estimator (MLE) is $\hat\theta=\arg\max_\theta\ell_n(\theta)$. Three objects do the work:
- the **score** $s_n(\theta)=\partial\ell_n/\partial\theta$, which is zero at $\hat\theta$;
- the **Hessian** $H_n(\theta)=\partial^2\ell_n/\partial\theta\,\partial\theta^\top$, whose negative on the sample is the **observed information**;
- the **expected (Fisher) information** $\mathcal I_n(\theta)=\mathrm E[s_ns_n^\top]$. Observed and expected information agree asymptotically but are different numbers in any finite sample.

**Conditions.** The model is correctly specified with true value $\theta_0$ in the interior of the parameter space; $\theta_0$ is identified; the support of $y$ does not depend on $\theta$; the density is twice differentiable; and, for time series, the data are stationary and ergodic with a martingale-difference score.

**Consistency, normality, invariance.** Because $\int f\,dy=1$ for every $\theta$, differentiating once gives $\mathrm E[s_t(\theta_0)]=0$, and differentiating again gives the information-matrix equality $\mathrm E[s_ts_t^\top]=-\mathrm E[\partial^2\ln f_t/\partial\theta\,\partial\theta^\top]$. The expected log-density is largest at $\theta_0$ because Kullback–Leibler divergence is non-negative, which is the heart of consistency. Expanding the first-order condition around the truth,
$$0=s_n(\hat\theta)\approx s_n(\theta_0)+H_n(\theta_0)(\hat\theta-\theta_0)\;\Rightarrow\;\sqrt n(\hat\theta-\theta_0)\approx\big[-H_n/n\big]^{-1}\,\frac{s_n(\theta_0)}{\sqrt n}\;\xrightarrow{d}\;N\big(0,\ \mathcal I_1(\theta_0)^{-1}\big),$$
because a law of large numbers governs the Hessian and a central limit theorem the score. The MLE is also **invariant**: the MLE of $g(\theta)$ is $g(\hat\theta)$, with variance $G\,\mathcal I_n^{-1}G^\top$ and $G=\partial g/\partial\theta^\top$ (the delta method). Optimizers use this by searching over an unconstrained scale, such as log-variance or log-odds, and mapping back.

**Three tests of $H_0:r(\theta)=0$.** Let $q$ be the number of restrictions, $R=\partial r/\partial\theta^\top$, $\hat\theta$ the unrestricted MLE and $\tilde\theta$ the MLE with the restriction imposed.
- **Wald:** $W=r(\hat\theta)^\top\big[R\,\mathcal I_n(\hat\theta)^{-1}R^\top\big]^{-1}r(\hat\theta)$ needs only the unrestricted fit.
- **Likelihood ratio:** $LR=2\,[\ell_n(\hat\theta)-\ell_n(\tilde\theta)]$ needs both fits.
- **Score (Lagrange multiplier, Rao):** $LM=s_n(\tilde\theta)^\top\mathcal I_n(\tilde\theta)^{-1}s_n(\tilde\theta)$ needs only the restricted fit.

Each converges to $\chi^2(q)$ under $H_0$.

**Why they agree, and why they do not.** Expand $\ell_n$ around $\hat\theta$: $\ell_n(\theta_0)\approx\ell_n(\hat\theta)-\tfrac12(\hat\theta-\theta_0)^\top\mathcal I_n(\hat\theta-\theta_0)$ and $s_n(\theta_0)\approx\mathcal I_n(\hat\theta-\theta_0)$. Hence $LR\approx W\approx LM$, with differences of smaller order. The three statistics approximate one log-likelihood from different places: Wald from the estimate, LM from the null, LR with no curvature approximation. If $\ell_n$ is exactly quadratic, as for a normal mean with known variance, they coincide. Otherwise they differ in finite samples in three ways:
- **Parametrization.** $W$ depends on how the restriction is written, for instance $p=0.04$ versus $\ln\frac p{1-p}=\ln\frac{0.04}{0.96}$. $LR$ and $LM$ depend only on the restricted model.
- **Which information.** Expected or observed, evaluated at $\hat\theta$ or $\tilde\theta$: each choice gives a different number (Efron and Hinkley 1978 compared observed with expected information).
- **Ordering.** In the Gaussian linear model, with $x=(\mathrm{RSS}_r-\mathrm{RSS}_u)/\mathrm{RSS}_u$, one has $W=nx\ \ge\ LR=n\ln(1+x)\ \ge\ LM=nx/(1+x)$ (Berndt and Savin 1977). No such law holds in general, and the example below reverses it.

They also differ in cost. LM needs only the null fit, so it suits checks where the alternative is expensive; the leftover-ARCH check on squared standardized residuals in Lesson 3.18's workflow is usually run as Engle's ARCH-LM test, a score test of constant variance.

**Misspecification and the sandwich.** Suppose the data come from a density $g$ that is not in the family. The maximizer of $\ell_n$ then converges to the **pseudo-true** value $\theta^*$ that minimizes the Kullback–Leibler divergence from $g$ to the model (White 1982), and
$$\sqrt n(\hat\theta-\theta^*)\xrightarrow{d}N\big(0,\ A^{-1}BA^{-1}\big),\qquad A=-\mathrm E\Big[\frac{\partial^2\ln f_t}{\partial\theta\,\partial\theta^\top}\Big],\quad B=\lim\mathrm{Var}\Big(\frac1{\sqrt n}\sum_ts_t(\theta^*)\Big).$$
Under correct specification $A=B$ and the sandwich collapses to $A^{-1}$. When scores are serially correlated, $B$ is a long-run variance and the Newey–West estimator of Lesson 3.11 replaces the outer product of scores. Under misspecification the inverse-information standard errors and the plain LM statistic are wrong, and the LR statistic converges to a weighted sum of $\chi^2(1)$ variables rather than to $\chi^2(q)$; Wald and LM statistics built on the sandwich remain valid. This is the logic of fitting a Gaussian GARCH likelihood to fat-tailed returns (Lessons 3.18 and 3.19): the mean and variance parameters are consistent when both equations are right (Bollerslev and Wooldridge 1992), but their standard errors need the sandwich. It also covers the logit of Lesson 3.26 when its index is wrong: the robust covariance then describes the pseudo-true slope, which need not equal the structural one.

**Boundary nulls.** When $H_0$ sits on the edge of the parameter space, as for $\alpha=0$ in an ARCH(1) model or a variance component equal to zero, the $\chi^2(q)$ limit fails. For one parameter on the boundary the LR limit is the mixture $\tfrac12\chi^2(0)+\tfrac12\chi^2(1)$ (Self and Liang 1987), whose 5% critical value is 2.706, not 3.841.""",
        r"""Cedar Capital's credit desk holds a bucket of $n=200$ unrated bonds and counts $x=14$ defaults over the year. The reserve model assumes a default probability of $p_0=0.04$. Test $H_0:p=p_0$ at the 5% level; the $\chi^2(1)$ critical value is 3.841.

**Step 1: likelihood, score, information.** For independent bonds, $\ell(p)=x\ln p+(n-x)\ln(1-p)$, with score $s(p)=\frac{x-np}{p(1-p)}$ and expected information $\mathcal I(p)=\frac{n}{p(1-p)}$. Setting the score to zero gives $\hat p=x/n=0.07$. The log-likelihood is $-50.728$ at $\hat p$ and $-52.657$ at $p_0$. At the null the score is $s(p_0)=156.25$ and the information is $5208.3$; at the estimate the information is $3072.2$. This is the logit of Lesson 3.26 with a constant as its only regressor and $\ln\frac p{1-p}$ as the parameter.

**Step 2: the three statistics.**
$$W=(\hat p-p_0)^2\,\mathcal I(\hat p)=2.765,\qquad LR=2\,[\ell(\hat p)-\ell(p_0)]=3.8587,\qquad LM=\frac{s(p_0)^2}{\mathcal I(p_0)}=\frac{(x-np_0)^2}{np_0(1-p_0)}=4.6875.$$
The $\chi^2(1)$ p-values are 0.0963, 0.0495 and 0.0304. Wald does not reject, LR rejects by a whisker (3.8587 against 3.8415) and the score test rejects: one hypothesis, one data set, two verdicts. Wald and LM share the numerator $(\hat p-p_0)^2$ and differ only in the variance they plug in, $\hat p(1-\hat p)=0.0651$ against $p_0(1-p_0)=0.0384$, so $W<LM$; LR lands between them. The order $W<LR<LM$ is the reverse of the Gaussian-regression order. The halved statistics show where each approximation goes wrong. The actual log-likelihood drop from $\hat p$ to $p_0$ is 1.929. The quadratic approximation built at $\hat p$ (Wald) claims 1.382 and the one built at $p_0$ (LM) claims 2.344.

**Step 3: which information.** The LM value above uses the expected information at the null. The observed information there, $x/p_0^2+(n-x)/(1-p_0)^2$, is 8951.8, and the score statistic built on it is 2.7273, which does not reject. Both are legitimate score tests; the expected-information form is the one whose inversion gives the Wilson (1927) interval.

**Step 4: invariance.** Write the same null on the log-odds scale. The estimate is $\ln\frac{0.07}{0.93}=-2.5867$, the null value is $\ln\frac{0.04}{0.96}=-3.1781$, and the variance of the estimate is $1/(n\hat p(1-\hat p))$. The Wald statistic becomes 4.5532, with p-value 0.0329, and now rejects. $LR$ and $LM$ are unchanged because they depend only on the restricted model. The MLE itself is invariant (the MLE of the log-odds is the log-odds of $\hat p$), but the Wald test of a restriction is not.

**Step 5: an exact benchmark.** Only $np_0=8$ defaults are expected under $H_0$, which is small for a normal approximation. The exact binomial upper tail is $P(X\ge14)=0.0312$. The two-sided exact p-value depends on a convention: summing every outcome no more likely than 14 gives 0.0437, while doubling the tail gives 0.0624. Inverting the tests gives confidence sets: the Wald interval is (0.0346, 0.1054) and contains 0.04, while the score interval is (0.0422, 0.1141) and excludes it.

**Step 6: what to trust.** Wald plugs in the variance at $\hat p$, which is 1.695 times the null variance that governs the sampling distribution when $H_0$ is true, and its verdict flips with the parametrization. The score and likelihood-ratio statistics and the two exact two-sided p-values place the evidence between 0.03 and 0.06. The honest report is a default rate of 0.07 with the score interval (0.0422, 0.1141) and moderate, not conclusive, evidence against 0.04. No claim should rest on the Wald interval at this event count; Brown, Cai and DasGupta (2001) documented the Wald interval's erratic coverage for proportions and recommended alternatives such as the Wilson interval.

**Step 7: a misspecified density.** The market-risk desk fits a normal likelihood to $m=500$ daily returns in percent, mean taken as zero, and obtains the variance estimate $\hat v=4.0$; the sample kurtosis is $\hat\kappa=6$. Per observation the score is $s_t=(r_t^2-v)/(2v^2)$ and the second derivative of the log-density is $\frac1{2v^2}-\frac{r_t^2}{v^3}$. At $v=\mathrm E[r^2]$ this gives $A=\frac1{2v^2}=0.03125$ and $B=\mathrm{Var}(r^2)/(4v^4)=\frac{\kappa-1}{4v^2}=0.078125$. Under normality $\kappa=3$ and $B=A$; here $B/A=2.5$. The sandwich variance is $A^{-1}BA^{-1}=(\kappa-1)v^2=80.0$ per observation, against $A^{-1}=2v^2=32$ from the model. The standard error of $\hat v$ is therefore 0.4 rather than 0.253, an inflation factor of $\sqrt{(\kappa-1)/2}=1.581$. The point estimate is unaffected, since it is the sample mean of $r^2$. A test of the risk budget $v=3.4$ gives $z=2.372$ with the model-based standard error and $z=1.5$ with the sandwich: the model-based standard error would have rejected the budget at 5%, and the honest one does not.""",
        r"""- **Fit on an unconstrained scale.** In statsmodels, `GenericLikelihoodModel` needs only a `loglike` or `loglikeobs` method and supplies numerical derivatives and the scipy optimizers. Coded directly in $p$, an unconstrained BFGS search can step outside $(0,1)$, where the logarithm is undefined, and return NaNs. Code the log-odds instead: the fit gives $-2.5867$ with standard error 0.2771, and the delta method $\hat p(1-\hat p)\times0.2771=0.018$ gives the standard error of $\hat p$. Before reading any output, check that the gradient is near zero and the Hessian is negative definite.
- **One call per test.**
  - Wald: `res.wald_test("x1 = 0")` or `res.t_test`. The default covariance is the inverse of the negative Hessian at the estimate, the observed information. An intercept-only `Logit` fitted to the 200 outcomes returns the constant $-2.5867$, and its Wald test against $-3.1781$ is the log-odds statistic 4.5532.
  - Likelihood ratio: `2 * (res_u.llf - res_r.llf)` against `scipy.stats.chi2.sf(stat, q)`. Discrete-model results also carry `llr` and `llr_pvalue` against the constant-only model.
  - Score: `statsmodels.stats.proportion.proportions_ztest(14, 200, value=0.04, prop_var=0.04)` returns the expected-information score $z=2.165$, whose square is 4.6875; without `prop_var` it returns the Wald $z=1.663$. `scipy.stats.binomtest(14, 200, 0.04)` is the exact test and `proportion_confint(..., method="wilson")` the score interval.
- **A robust covariance needs something to be robust to.** `fit(cov_type="HC0")` gives the sandwich of per-observation scores, `"HAC"` the Newey–West version for dependent scores and `"cluster"` the cluster-robust version. In an intercept-only Bernoulli model the HC0 and classical standard errors are the same number, because $A$ and $B$ coincide algebraically, so a robust covariance repairs nothing in the bond example. Its real misspecification would be correlated defaults within a sector or vintage, which push the variance of the count above $np(1-p)$ and call for clustered inference or an overdispersed model such as the beta-binomial. In `arch`, `fit(cov_type="robust")`, the default, is the Bollerslev–Wooldridge sandwich and `"classic"` assumes the information-matrix equality holds; a large gap between the two is a sign that it does not, as with the excess kurtosis of Step 7.
- **Calibrate small samples.** When $np_0(1-p_0)$ is below a common rule of thumb of about 10, check an asymptotic p-value against an exact test or a parametric bootstrap: simulate from the restricted fit, recompute the statistic each time, and compare the observed value with that distribution.
- **Report the choices.** Name the statistic, the information matrix and the covariance estimator, show a likelihood-based interval, and fix the test before seeing which one rejects, because choosing the statistic after the fact is the forking-paths problem of Lesson 3.28.""",
        'W=(\\hat\\theta-\\theta_0)^\\top I(\\hat\\theta)(\\hat\\theta-\\theta_0),\\quad LR=2[\\ell(\\hat\\theta)-\\ell(\\theta_0)],\\quad LM=s(\\theta_0)^\\top I(\\theta_0)^{-1}s(\\theta_0)',
        r"""import math
from math import sqrt, log, exp

# The guided runtime has no erf, so the normal CDF uses the Abramowitz and
# Stegun 26.2.17 approximation (published error bound 7.5e-8). With one degree
# of freedom, P(chi-square > s) = 2 * (1 - Phi(sqrt(s))).
def phi(x):
    sign = 1.0
    z = x
    if z < 0:
        sign = -1.0
        z = -z
    t = 1.0 / (1.0 + 0.2316419 * z)
    poly = t * (0.319381530 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429))))
    tail = 0.3989422804014327 * exp(-0.5 * z * z) * poly
    return 0.5 + sign * (0.5 - tail)

def pvalue(stat):
    return 2.0 * (1.0 - phi(sqrt(stat)))

# Credit desk: 14 defaults among 200 bonds, null default probability 4 percent.
n = 200
x = 14
p0 = 0.04
phat = x / n
print("Default rate estimate:", round(phat, 4))

def loglik(p):
    return x * log(p) + (n - x) * log(1 - p)

ll_hat = loglik(phat)
ll_null = loglik(p0)
print("Log-likelihood at the MLE:", round(ll_hat, 3))
print("Log-likelihood at the null:", round(ll_null, 3))

score0 = (x - n * p0) / (p0 * (1 - p0))
info0 = n / (p0 * (1 - p0))
info_hat = n / (phat * (1 - phat))
print("Score at the null:", round(score0, 2))
print("Expected information at the null:", round(info0, 1))
print("Expected information at the MLE:", round(info_hat, 1))
print("Bernoulli variance at the MLE:", round(phat * (1 - phat), 4))
print("Bernoulli variance at the null:", round(p0 * (1 - p0), 4))
print("Variance ratio, MLE over null:", round(phat * (1 - phat) / (p0 * (1 - p0)), 3))
print("Expected defaults under the null:", round(n * p0, 2))

wald = (phat - p0) ** 2 * info_hat
lr = 2 * (ll_hat - ll_null)
lm = score0 ** 2 / info0
print("Wald statistic:", round(wald, 4))
print("LR statistic:", round(lr, 4))
print("LM statistic:", round(lm, 4))
print("Wald p-value:", round(pvalue(wald), 4))
print("LR p-value:", round(pvalue(lr), 4))
print("LM p-value:", round(pvalue(lm), 4))
print("Wald log-likelihood drop:", round(wald / 2, 3))
print("Actual log-likelihood drop:", round(lr / 2, 3))
print("LM log-likelihood drop:", round(lm / 2, 3))

# The same score with the observed (Hessian-based) information at the null.
obs_info0 = x / p0 ** 2 + (n - x) / (1 - p0) ** 2
print("Observed information at the null:", round(obs_info0, 1))
print("LM statistic with observed information:", round(score0 ** 2 / obs_info0, 4))

# The same null written on the log-odds scale.
logit_hat = log(phat / (1 - phat))
logit_null = log(p0 / (1 - p0))
wald_logit = (logit_hat - logit_null) ** 2 * n * phat * (1 - phat)
print("Log-odds estimate:", round(logit_hat, 4))
print("Log-odds null value:", round(logit_null, 4))
print("Wald statistic on log-odds scale:", round(wald_logit, 4))
print("Wald p-value on log-odds scale:", round(pvalue(wald_logit), 4))

# Exact binomial benchmark; P(X = k) by recursion from P(X = 0).
ratio = p0 / (1 - p0)
prob = exp(n * log(1 - p0))
observed = 0
upper = 0
for k in range(0, n + 1):
    if k == x:
        observed = prob
    if k >= x:
        upper += prob
    prob = prob * (n - k) / (k + 1) * ratio
prob = exp(n * log(1 - p0))
two_sided = 0
for k in range(0, n + 1):
    if prob <= observed * 1.0000001:
        two_sided += prob
    prob = prob * (n - k) / (k + 1) * ratio
print("Exact upper tail P(X >= 14):", round(upper, 4))
print("Exact two-sided p, probability ordering:", round(two_sided, 4))
print("Exact two-sided p, doubled tail:", round(2 * upper, 4))

# Confidence sets from inverting the Wald and the score tests.
z = 1.959964
se_hat = sqrt(phat * (1 - phat) / n)
print("Wald interval lower:", round(phat - z * se_hat, 4))
print("Wald interval upper:", round(phat + z * se_hat, 4))
zz = z * z
centre = (phat + zz / (2 * n)) / (1 + zz / n)
half = z * sqrt(phat * (1 - phat) / n + zz / (4 * n * n)) / (1 + zz / n)
print("Score interval lower:", round(centre - half, 4))
print("Score interval upper:", round(centre + half, 4))

# Quasi-maximum likelihood: normal likelihood for a daily variance (percent
# squared units, mean taken as zero), 500 days, sample kurtosis 6.
m = 500
v = 4.0
kurt = 6.0
hess_a = 1 / (2 * v ** 2)
score_b = (kurt - 1) / (4 * v ** 2)
sandwich = score_b / hess_a ** 2
print("Hessian term A:", round(hess_a, 5))
print("Score variance B:", round(score_b, 6))
print("B divided by A:", round(score_b / hess_a, 2))
print("Model-based variance per observation:", round(1 / hess_a, 2))
print("Sandwich variance per observation:", round(sandwich, 2))
se_model = sqrt(1 / hess_a / m)
se_robust = sqrt(sandwich / m)
print("Model-based SE of the variance:", round(se_model, 4))
print("Sandwich SE of the variance:", round(se_robust, 4))
print("SE inflation factor:", round(se_robust / se_model, 3))
budget = 3.4
print("z-statistic, model-based SE:", round((v - budget) / se_model, 3))
print("z-statistic, sandwich SE:", round((v - budget) / se_robust, 3))""",
        'A second bucket holds 150 bonds with 3 defaults, against a reserve rate of p0 = 0.06. Compute the estimate, the Wald, likelihood-ratio and score statistics (expected information at the null), and the Wald statistic on the log-odds scale. State which exceed 3.841, rank the three, explain why the ranking differs from the 14-of-200 case, and say which p-value you would quote, given an exact binomial lower tail P(X <= 3) = 0.0186.',
        'The estimate is 0.02, so the variance at the estimate is 0.02 × 0.98 = 0.0196 against 0.06 × 0.94 = 0.0564 at the null. Wald = 0.04² × 150 / 0.0196 = 12.245. Score = (3 − 9)² / (150 × 0.06 × 0.94) = 36 / 8.46 = 4.255. LR = 2[3 ln(0.02/0.06) + 147 ln(0.98/0.94)] = 5.660. All three exceed 3.841, with p-values 0.0005, 0.0391 and 0.0174. On the log-odds scale the Wald statistic is 3.823 and does not reject, so the Wald verdict again depends on how the null is written. The ranking is W > LR > LM, the reverse of the 14-of-200 case, because the estimate is now below the null and the variance at the estimate (0.0196) is smaller than the null variance (0.0564), which inflates Wald. Its p-value of 0.0005 greatly overstates the evidence. Quote the likelihood-ratio or score p-value (0.0174 or 0.0391) beside the exact lower tail 0.0186 (0.0372 two-sided by probability ordering) and call the evidence moderate: 3 defaults were seen where 9 were expected, and at that count the score, likelihood-ratio and exact figures deserve more trust than Wald.',
        [
            (
                'A desk can cheaply fit only the model that imposes the null. Which classical statistic needs nothing more than that fit?',
                ['Lagrange multiplier (score) statistic', 'Wald statistic', 'Likelihood-ratio statistic'],
                0,
                'The score test evaluates the score and the information at the restricted estimate. The Wald statistic needs the unrestricted fit and the likelihood ratio needs both fits.',
            ),
            (
                'A bucket shows 30 defaults among 200 bonds and the null is p0 = 0.10. The score statistic with expected information at the null is:',
                ['3.92', '5.00', '5.56'],
                2,
                'LM = (x − n p0)² / (n p0 (1 − p0)) = (30 − 20)² / 18 = 5.56. The value 3.92 is the Wald statistic, which uses the variance at the estimate 0.15, and 5.00 drops the factor (1 − p0).',
            ),
            (
                'A normal likelihood estimates a daily variance from returns whose kurtosis is 9. Compared with the model-based standard error, the sandwich standard error of the variance estimate is:',
                ['The same', 'Twice as large', 'Half as large'],
                1,
                'A = 1/(2v²) and B = (kurtosis − 1)/(4v²), so the sandwich variance is (kurtosis − 1)v² against 2v² from the model. The ratio of standard errors is √((9 − 1)/2) = 2.',
            ),
            (
                'The same null is written first on the probability scale and then on the log-odds scale. Which statistic can change its verdict?',
                ['Likelihood ratio', 'Score with expected information', 'Wald'],
                2,
                'The Wald statistic depends on how the restriction is written, as 2.765 against 4.553 in the bond example. The likelihood ratio and the score statistic depend only on the restricted model.',
            ),
        ],
        [('statsmodels contributors · Maximum likelihood estimation with GenericLikelihoodModel', 'https://www.statsmodels.org/stable/examples/notebooks/generated/generic_mle.html'), ('arch contributors · ARCHModel.fit and its robust and classic covariance estimators', 'https://arch.readthedocs.io/en/latest/univariate/generated/generated/arch.univariate.base.ARCHModel.fit.html'), ('Halbert White · Maximum likelihood estimation of misspecified models (Econometrica, 1982)', 'https://doi.org/10.2307/1912526'), ('Brown, Cai and DasGupta · Interval estimation for a binomial proportion (Statistical Science, 2001)', 'https://doi.org/10.1214/ss/1009213286')],
    ),
    (
        '3.34',
        8,
        "Generalized method of moments and Hansen's J test",
        "Estimate parameters from moment conditions with an efficient weighting matrix, test the overidentifying restrictions with Hansen's J statistic, and read the result as pricing errors.",
        r"""Lesson 3.33 estimated parameters from a full density. The generalized method of moments (GMM; Hansen 1982) asks for less: only that some function of the data and the parameters has mean zero at the truth. Economic theory often supplies exactly that, in Euler equations and pricing equations, with no distributional model.

**Moment conditions.** Let $w_t$ be the data, $\theta\in\mathbb R^k$ the parameters and $g(w_t,\theta)\in\mathbb R^q$ moment functions with
$$\mathrm E\,[\,g(w_t,\theta_0)\,]=0 .$$
Write $\bar g_n(\theta)=\frac1n\sum_t g(w_t,\theta)$, $G=\mathrm E[\partial g/\partial\theta^\top]$ (a $q\times k$ matrix of full column rank when $\theta_0$ is identified) and $S=\lim\mathrm{Var}\big(\sqrt n\,\bar g_n(\theta_0)\big)$, the long-run variance of $g_t$.
- **Just-identified** ($q=k$): solve $\bar g_n(\hat\theta)=0$. Nothing is left over to test.
- **Over-identified** ($q>k$): $\bar g_n$ cannot be zeroed, so make it short in the metric of a positive definite weighting matrix $W$,
$$\hat\theta(W)=\arg\min_\theta\ Q_n(\theta),\qquad Q_n(\theta)=\bar g_n(\theta)^\top W\,\bar g_n(\theta).$$
The $q-k$ leftover directions are testable restrictions.

**Familiar estimators are special cases.**
- OLS: $g_t=x_t(y_t-x_t^\top\theta)$ has $q=k$, so every $W$ gives OLS, and the covariance below is the White or Newey–West covariance of Lessons 3.10 and 3.11.
- IV and 2SLS (Lesson 3.24): $g_t=z_t(y_t-x_t^\top\theta)$ with $l$ instruments. If $l=k$ this is the IV estimator. If $l>k$, 2SLS is GMM with $W=(Z^\top Z/n)^{-1}$, efficient only when errors are conditionally homoskedastic and serially uncorrelated; the Sargan statistic is the $J$ statistic of that case.
- Maximum likelihood (Lesson 3.33): the score is the moment function and $q=k$.

**Sampling theory.** Assume stationary ergodic data, $g$ continuously differentiable in $\theta$, $G$ of full column rank, $S$ nonsingular and a central limit theorem for $\sqrt n\,\bar g_n(\theta_0)$. The first-order condition is $\hat G^\top W\bar g_n(\hat\theta)=0$, and linearizing, $\bar g_n(\hat\theta)\approx\bar g_n(\theta_0)+G(\hat\theta-\theta_0)$, gives $\sqrt n\,(\hat\theta-\theta_0)\approx-(G^\top WG)^{-1}G^\top W\sqrt n\,\bar g_n(\theta_0)$. Hence $\hat\theta(W)$ is consistent for every positive definite $W$ and
$$\sqrt n\,(\hat\theta-\theta_0)\xrightarrow{d}N\Big(0,\ (G^\top WG)^{-1}G^\top WSWG\,(G^\top WG)^{-1}\Big).$$
The weighting matrix affects efficiency, not consistency. By a generalized Gauss–Markov argument the covariance is smallest at $W=S^{-1}$, where it collapses to $(G^\top S^{-1}G)^{-1}$. With $S$ known, the efficient estimator is also invariant to invertible linear recombinations of the moments, because $S^{-1}$ undoes them; the identity-weighted estimator is not, which is why its units matter. When the moments are linear in $\theta$, $\bar g_n(\theta)=\bar a-\bar C\theta$, the minimizer is explicit, $\hat\theta=(\bar C^\top W\bar C)^{-1}\bar C^\top W\bar a$, and with $\bar C=Z^\top X/n$, $\bar a=Z^\top y/n$ and $W=(Z^\top Z/n)^{-1}$ it is the 2SLS formula.

This gives **two-step efficient GMM**: (1) minimize with a convenient $W_1$, such as the identity or $(Z^\top Z/n)^{-1}$, to get a consistent $\hat\theta_1$; (2) estimate $\hat S$ from $g_t(\hat\theta_1)$ and minimize again with $W=\hat S^{-1}$. Iterating the two steps, or re-estimating $S$ inside the objective (the continuously updated estimator), are variants (Hansen, Heaton and Yaron 1996).

**Estimating $S$.** When $g_t$ is serially correlated, $S$ is a long-run variance, estimated as in Lesson 3.11 but for a vector:
$$\hat S=\hat\Gamma_0+\sum_{j=1}^{L}w_j\big(\hat\Gamma_j+\hat\Gamma_j^\top\big),\qquad\hat\Gamma_j=\frac1n\sum_{t=j+1}^{n}g_tg_{t-j}^\top,\qquad w_j=1-\frac{j}{L+1}.$$
With $q>1$, $\hat\Gamma_j$ is not symmetric because it holds cross-autocovariances, so the transpose matters. The Bartlett weights keep $\hat S$ positive semidefinite.

**Hansen's $J$ test.** At the efficient estimate, $\sqrt n\,\bar g_n(\hat\theta)\approx\big[I-G(G^\top S^{-1}G)^{-1}G^\top S^{-1}\big]\sqrt n\,\bar g_n(\theta_0)$. After premultiplying by $S^{-1/2}$, the bracket becomes a symmetric idempotent matrix of rank $q-k$ acting on a standard normal vector. Hence
$$J=n\,\bar g_n(\hat\theta)^\top\hat S^{-1}\bar g_n(\hat\theta)\ \xrightarrow{d}\ \chi^2(q-k)\qquad\text{under }H_0:\ \mathrm E[g(w_t,\theta_0)]=0 .$$
$J$ is the squared length of the part of the moment vector that no choice of $\theta$ can remove. It must use $\hat S^{-1}$ at the efficient estimate; the same quadratic form at a first-step estimate is larger and is not $\chi^2$. It is identically zero when $q=k$.

**The stochastic-discount-factor view.** A linear SDF $m_t(b)=1-bf_t$ prices excess returns $R^e_{i,t}$ when $\mathrm E[m_tR^e_{i,t}]=0$ for every asset $i$. The moment functions are SDF-discounted excess returns, $g_{i,t}(b)=R^e_{i,t}(1-bf_t)$, so $\bar g(b)=\bar a-b\,\bar c$ with $\bar a_i$ the mean excess return, $\bar c_i$ the mean of $f_tR^e_{i,t}$ and $G=-\bar c$. The conditional pricing equation $\mathrm E_t[m_{t+1}R^e_{i,t+1}]=0$ survives multiplication by any variable $z_t$ known at time $t$, so every instrument adds moments; this is how Euler-equation estimation (Hansen and Singleton 1982) creates over-identification, and why $q$ can outgrow the sample. The sample moment is the vector of **pricing errors** $\hat\alpha_i=\bar g_i(\hat b)$, and $J=n\,\hat\alpha^\top\hat S^{-1}\hat\alpha$ is their weighted squared length.
- With $W=I$ the estimator is the cross-sectional regression of mean returns on $\bar c$ through the origin. It depends on the units of the assets.
- With $W=\hat S^{-1}$ it is the GLS version. It weights by precision and may take offsetting positions in correlated assets, so its raw pricing errors need not be smaller than the first step's. Hansen and Jagannathan (1997) therefore compare misspecified models with a weight, the inverse second-moment matrix of payoffs, that does not depend on the model.
- Standard errors of individual pricing errors come from $\tfrac1n\big[S-G(G^\top S^{-1}G)^{-1}G^\top\big]$, not from $S/n$, because estimating $b$ absorbs part of the noise.

Lesson 3.35 turns to the GRS and Fama–MacBeth treatments of the same pricing question.""",
        r"""Cedar's factor desk asks whether a one-factor stochastic discount factor $m_t=1-bf_t$, with $f_t$ the market excess return in percentage points, prices two test portfolios. From $n=120$ months the desk has mean excess returns $\bar a=(0.60,\ 0.80)$ in percent per month and mean products $\bar c=(20,\ 10)$ of the factor with each portfolio's excess return. The moment vector is $\bar g(b)=\bar a-b\,\bar c$: one parameter, two moments, one over-identifying restriction.

**Step 1: the weighting matrix from Newey–West.** The moment series has autocovariances
$$\hat\Gamma_0=\begin{pmatrix}12&1.5\\1.5&3\end{pmatrix},\qquad\hat\Gamma_1=\begin{pmatrix}4&0.6\\0.4&1\end{pmatrix}.$$
With $L=1$ and Bartlett weight $w_1=0.5$,
$$\hat S=\hat\Gamma_0+0.5\,(\hat\Gamma_1+\hat\Gamma_1^\top)=\begin{pmatrix}16&2\\2&4\end{pmatrix},\qquad\det\hat S=60 .$$
The off-diagonal entries of $\hat\Gamma_1$ differ because they are cross-autocovariances; only their sum enters $\hat S$.

**Step 2: first step with $W=I$.** $\hat b_1=\bar c^\top\bar a/\bar c^\top\bar c=(12+8)/500=0.04$, and the pricing errors $\bar a-\hat b_1\bar c$ are $(-0.2,\ 0.4)$. The standard error must be the sandwich, because $W=I$ is not $\hat S^{-1}$:
$$\mathrm{SE}_1=\sqrt{\frac{\bar c^\top\hat S\,\bar c}{n\,(\bar c^\top\bar c)^2}}=0.0159,\qquad t=2.513 .$$

**Step 3: efficient step with $W=\hat S^{-1}$.** Here $\bar c^\top\hat S^{-1}=(1,\ 2)$, so the less noisy second moment gets twice the weight, $\bar c^\top\hat S^{-1}\bar c=40$ and $\bar c^\top\hat S^{-1}\bar a=2.2$. Then
$$\hat b_2=\frac{2.2}{40}=0.055,\qquad\mathrm{SE}_2=\frac1{\sqrt{n\,\bar c^\top\hat S^{-1}\bar c}}=\frac1{\sqrt{120\times40}}=0.0144,\qquad t=3.811 .$$
The efficient standard error is 0.907 times the first-step one. The efficient estimate moved by 0.015, and its raw pricing errors $(-0.50,\ 0.25)$ are larger in unweighted terms than the first step's, because the efficient estimator minimizes the weighted length, which favors the precisely measured combination.

**Step 4: Hansen's $J$.** With $\hat\alpha=(-0.50,\ 0.25)$,
$$J=n\,\hat\alpha^\top\hat S^{-1}\hat\alpha=120\times\tfrac1{60}\big[4(0.25)-4(-0.5)(0.25)+16(0.0625)\big]=5.0 .$$
Against the 5% critical value 3.841 of $\chi^2(q-k)=\chi^2(1)$, with p-value 0.0253, $J$ rejects. With one parameter and two moments the test reduces to a contrast that does not involve $b$: $\bar c_1\bar a_2-\bar c_2\bar a_1=10$, whose t-ratio of 2.2361 squares to $J$. In finance terms, portfolio 1 implies the SDF loading $\bar a_1/\bar c_1=0.03$ and portfolio 2 implies $0.08$. For one parameter and two moments only, $J$ also equals $(\hat b_1-\hat b_2)^2/(\mathrm{SE}_1^2-\mathrm{SE}_2^2)=5.0$: the two weightings disagree about $b$ by exactly what $J$ reports.

**Step 5: individual pricing errors.** The covariance of the fitted pricing errors is $\frac1n\big[\hat S-\bar c(\bar c^\top\hat S^{-1}\bar c)^{-1}\bar c^\top\big]$, with standard errors 0.2236 and 0.1118. The t-ratios are $-2.2361$ and $2.2361$, each equal to $\pm\sqrt J$. Dividing instead by $\sqrt{S_{ii}/n}$ gives $-1.3693$ and $1.3693$ and misses the problem, because it ignores the noise that estimating $b$ has absorbed.

**Step 6: what moves the verdict.** Using the lag-zero covariance alone, $\hat S=\hat\Gamma_0$, gives $J=6.6667$: positive autocorrelation enlarges $S$, so ignoring it overstates the evidence against the model. The same quadratic form evaluated at the first-step estimate is 6.08, which is not a test statistic because $\hat b_1$ does not minimize it. A significant loading ($t=3.811$) therefore coexists with a rejected model: the factor matters for pricing, yet no single $b$ prices both portfolios.""",
        r"""- **Linear IV models: `linearmodels`.** `IVGMM(dependent, exog, endog, instruments, weight_type="kernel", bandwidth=L)` fits two-step efficient GMM by default; `fit(iter_limit=1)` stops after the first step and larger values iterate. The first-step weighting matrix comes from the instruments' outer product unless `initial_weight` is supplied. `weight_type` chooses the estimator of $S$: `"unadjusted"`, `"robust"`, `"kernel"` (HAC) or `"clustered"`. Results carry `j_stat` (statistic and p-value) and `c_stat(...)`, a difference-of-$J$ test for treating chosen variables as exogenous. `IV2SLS` is the 2SLS baseline of Lesson 3.24 and `IVGMMCUE` the continuously updated estimator.
- **Nonlinear or asset-pricing moments: `statsmodels`.** Subclass `statsmodels.sandbox.regression.gmm.GMM`, write `momcond(self, params)` to return an $n\times q$ array of moments, and call `fit(start_params, maxiter=2, weights_method="hac", wargs={"maxlag": L})`. Then `res.jtest()` returns $(J,\ p,\ q-k)$. The class lives in a sandbox module; if its default BFGS optimizer raises an error, add `optim_method="nm"` (Nelder–Mead). `statsmodels.stats.sandwich_covariance.S_hac_simple(g, nlags=L)` returns the Newey–West sum without dividing by $n$. Packages differ in whether $S$ uses centered moments (`wargs={"centered": False}` here, `center` in linearmodels), in the divisor and in the scaling of $J$, and each moves $J$ in finite samples, so reproduce a small case such as Steps 1–5 by hand first.
- **Report.** $J$ with its degrees of freedom and p-value; both steps' estimates, because a large gap is itself evidence of misspecification; pricing errors with the Step 5 covariance; the lag $L$ and results at $L$ and $2L$; and how well conditioned $\hat S$ is. Put moments in comparable units before using any first-step $W=I$.
- **Failure modes.**
  - *Weak identification.* If $G$ is nearly rank deficient, as with the weak instruments of Lesson 3.24, $G^\top S^{-1}G$ is small, estimates wander and Wald intervals mislead; Stock and Wright (2000) developed identification-robust tests.
  - *Many moments for the sample.* $\hat S$ has $q(q+1)/2$ distinct entries and its inverse amplifies their noise, so two-step estimates can be biased and the $\chi^2$ approximation to $J$ poor. This is why Hansen, Heaton and Yaron (1996) compared iterated and continuously updated estimators.
  - *Limited power.* $J$ tests only the over-identifying directions. In the SDF example, mispricing proportional to $\bar c$ is absorbed by $b$, so a non-rejection certifies neither the instruments nor the model.
  - *Which moment fails.* $J$ does not say. Use pricing-error t-ratios and difference-of-$J$ tests on subsets of moments.""",
        '\\hat\\theta=\\arg\\min_\\theta\\,\\bar g_n(\\theta)^\\top W\\bar g_n(\\theta),\\quad \\widehat{\\mathrm{Var}}(\\hat\\theta)=\\tfrac1n(G^\\top S^{-1}G)^{-1},\\quad J=n\\,\\bar g_n(\\hat\\theta)^\\top\\hat S^{-1}\\bar g_n(\\hat\\theta)\\sim\\chi^2(q-k)',
        r"""import math
from math import sqrt, exp

# The guided runtime has no erf, so the normal CDF uses the Abramowitz and
# Stegun 26.2.17 approximation (published error bound 7.5e-8). With one degree
# of freedom, P(chi-square > s) = 2 * (1 - Phi(sqrt(s))).
def phi(x):
    sign = 1.0
    z = x
    if z < 0:
        sign = -1.0
        z = -z
    t = 1.0 / (1.0 + 0.2316419 * z)
    poly = t * (0.319381530 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429))))
    tail = 0.3989422804014327 * exp(-0.5 * z * z) * poly
    return 0.5 + sign * (0.5 - tail)

def pvalue(stat):
    return 2.0 * (1.0 - phi(sqrt(stat)))

# One SDF loading b, two test portfolios, n = 120 months.
n = 120
a1 = 0.60    # mean excess return, portfolio 1 (percent per month)
a2 = 0.80
c1 = 20.0    # mean of factor times excess return, portfolio 1
c2 = 10.0

# Step 1: long-run covariance S from Newey-West with L = 1 (Bartlett weight 0.5).
g0_11 = 12.0
g0_12 = 1.5
g0_22 = 3.0
g1_11 = 4.0
g1_12 = 0.6    # covariance of moment 1 with lagged moment 2
g1_21 = 0.4    # covariance of moment 2 with lagged moment 1
g1_22 = 1.0
w1 = 1 - 1 / (1 + 1)
s11 = g0_11 + w1 * (g1_11 + g1_11)
s12 = g0_12 + w1 * (g1_12 + g1_21)
s22 = g0_22 + w1 * (g1_22 + g1_22)
print("S11:", s11)
print("S12:", s12)
print("S22:", s22)

# Step 2: first step with identity weighting, sandwich standard error.
b1 = (c1 * a1 + c2 * a2) / (c1 * c1 + c2 * c2)
r11 = a1 - b1 * c1
r12 = a2 - b1 * c2
se1 = sqrt((c1 * c1 * s11 + 2 * c1 * c2 * s12 + c2 * c2 * s22) / (n * (c1 * c1 + c2 * c2) ** 2))
print("First-step estimate:", round(b1, 4))
print("First-step pricing error, portfolio 1:", round(r11, 4))
print("First-step pricing error, portfolio 2:", round(r12, 4))
print("First-step standard error:", round(se1, 4))
print("First-step t-ratio:", round(b1 / se1, 3))

# Step 3: efficient step, W = S^-1 (2 x 2 inverse by hand).
def efficient(s11, s12, s22):
    det = s11 * s22 - s12 * s12
    i11 = s22 / det
    i12 = -s12 / det
    i22 = s11 / det
    w_1 = c1 * i11 + c2 * i12
    w_2 = c1 * i12 + c2 * i22
    denom = w_1 * c1 + w_2 * c2
    b = (w_1 * a1 + w_2 * a2) / denom
    r1 = a1 - b * c1
    r2 = a2 - b * c2
    j = n * (i11 * r1 * r1 + 2 * i12 * r1 * r2 + i22 * r2 * r2)
    return [b, 1 / sqrt(n * denom), j, r1, r2, w_1, w_2, denom, det]

res = efficient(s11, s12, s22)
print("Determinant of S:", round(res[8], 4))
print("Efficient denominator:", round(res[7], 4))
print("Efficient numerator:", round(res[5] * a1 + res[6] * a2, 4))
print("Efficient weight on moment 1:", round(res[5], 4))
print("Efficient weight on moment 2:", round(res[6], 4))
print("Efficient estimate:", round(res[0], 4))
print("Efficient standard error:", round(res[1], 4))
print("Efficient t-ratio:", round(res[0] / res[1], 3))
print("Estimate shift, efficient minus first step:", round(res[0] - b1, 4))
print("SE ratio, efficient over first step:", round(res[1] / se1, 3))
print("Efficient pricing error, portfolio 1:", round(res[3], 4))
print("Efficient pricing error, portfolio 2:", round(res[4], 4))

# Step 4: Hansen J, its p-value, and two equivalent checks for one overidentifying restriction.
print("Hansen J statistic:", round(res[2], 4))
print("J p-value:", round(pvalue(res[2]), 4))
print("Implied SDF loading, portfolio 1:", round(a1 / c1, 4))
print("Implied SDF loading, portfolio 2:", round(a2 / c2, 4))
contrast = c1 * a2 - c2 * a1
var_contrast = (c2 * c2 * s11 - 2 * c1 * c2 * s12 + c1 * c1 * s22) / n
print("Contrast of the two moments:", round(contrast, 4))
print("Contrast t-ratio:", round(contrast / sqrt(var_contrast), 4))
gap = (b1 - res[0]) ** 2 / (se1 * se1 - res[1] * res[1])
print("Squared gap over variance difference:", round(gap, 4))

# Step 5: pricing-error standard errors from S - c (c' S^-1 c)^-1 c', not from S.
cov11 = (s11 - c1 * c1 / res[7]) / n
cov22 = (s22 - c2 * c2 / res[7]) / n
print("Pricing-error standard error, portfolio 1:", round(sqrt(cov11), 4))
print("Pricing-error standard error, portfolio 2:", round(sqrt(cov22), 4))
print("Pricing-error t-ratio, portfolio 1:", round(res[3] / sqrt(cov11), 4))
print("Pricing-error t-ratio, portfolio 2:", round(res[4] / sqrt(cov22), 4))
print("Naive t-ratio using S/n, portfolio 1:", round(res[3] / sqrt(s11 / n), 4))
print("Naive t-ratio using S/n, portfolio 2:", round(res[4] / sqrt(s22 / n), 4))

# Step 6: what moves the verdict.
res0 = efficient(g0_11, g0_12, g0_22)
print("J using the lag-zero covariance only:", round(res0[2], 4))
det = s11 * s22 - s12 * s12
q1 = n * ((s22 / det) * r11 * r11 + 2 * (-s12 / det) * r11 * r12 + (s11 / det) * r12 * r12)
print("Quadratic form at the first-step estimate:", round(q1, 4))""",
        "Cedar's second pair of test portfolios has n = 100 months, mean excess returns (0.45, 0.40) in percent per month, mean factor products (12, 6) and long-run covariance S = [[8, 2], [2, 2]]. Compute the identity-weighted estimate, the efficient estimate with its standard error, the efficient pricing errors, and J against 3.841. Then explain what a non-rejection does and does not establish here.",
        "First step: b1 = (12 × 0.45 + 6 × 0.40) / (144 + 36) = 7.8 / 180 = 0.0433. Since S⁻¹ = (1/12)[[2, −2], [−2, 8]], c'S⁻¹ = (1, 2), c'S⁻¹c = 24 and c'S⁻¹a = 0.45 + 0.80 = 1.25. Efficient: b2 = 1.25 / 24 = 0.0521 with standard error 1 / √(100 × 24) = 0.0204. Pricing errors at b2 are (0.45 − 0.625, 0.40 − 0.3125) = (−0.175, 0.0875), and J = 100 × (1/12) × [2(0.175²) − 4(−0.175)(0.0875) + 8(0.0875²)] = 1.531, below 3.841 (p = 0.216), so the overidentifying restriction is not rejected. Check with the contrast: 12 × 0.40 − 6 × 0.45 = 2.1 has variance (36 × 8 − 2 × 72 × 2 + 144 × 2) / 100 = 2.88, so t = 1.237 and t² = 1.531. The non-rejection means the two portfolios' implied SDF loadings, 0.45 / 12 = 0.0375 and 0.40 / 6 = 0.0667, differ by no more than sampling noise allows. It does not show that the SDF is correct: with one overidentifying restriction and 100 months the test has limited power, and mispricing proportional to the factor products would be absorbed by b.",
        [
            (
                "A model has 3 moment conditions and 1 parameter, estimated by efficient GMM. Under correct specification, Hansen's J statistic is asymptotically:",
                ['Chi-square with 1 degree of freedom', 'Chi-square with 2 degrees of freedom', 'Chi-square with 3 degrees of freedom'],
                1,
                'J has q − k = 3 − 1 = 2 degrees of freedom: one parameter absorbs one direction of the moment vector and two directions remain testable.',
            ),
            (
                "Efficient GMM has covariance (G'S⁻¹G)⁻¹ per observation. With one parameter, G'S⁻¹G = 24 and n = 100, the standard error of the estimate is:",
                ['0.0204', '0.0417', '0.2041'],
                0,
                'The variance is 1 / (n × 24) = 1/2400, so the standard error is 1/√2400 = 0.0204. The values 0.0417 (1/24) and 0.2041 (1/√24) both forget the factor n.',
            ),
            (
                'An efficient two-step GMM test gives J = 1.8 with one degree of freedom (5% critical value 3.841). The best conclusion is:',
                ['The moment conditions are proven valid', 'The weighting matrix was misspecified', 'The restriction is not rejected, but the test may have little power'],
                2,
                'Since 1.8 < 3.841 the overidentifying restriction is not rejected. That is an absence of evidence against the model, not proof, because J has limited power and cannot see mispricing that a parameter absorbs.',
            ),
            (
                'In a just-identified GMM problem (as many moments as parameters), changing the weighting matrix W changes:',
                ['The estimate but not its covariance', 'Neither the estimate nor its asymptotic covariance', 'Both the estimate and its covariance'],
                1,
                'With q = k the estimator solves the sample moment equation exactly, so W drops out of the estimate, and the sandwich reduces to G⁻¹ S G⁻ᵀ, which does not contain W either.',
            ),
        ],
        [('linearmodels contributors · IVGMM: generalized method of moments for IV models', 'https://bashtage.github.io/linearmodels/iv/iv/linearmodels.iv.model.IVGMM.html'), ('statsmodels contributors · Generalized method of moments (gmm)', 'https://www.statsmodels.org/stable/gmm.html'), ('Lars Peter Hansen · Large sample properties of generalized method of moments estimators (Econometrica, 1982)', 'https://doi.org/10.2307/1912775'), ('linearmodels contributors · Instrumental variable estimation: GMM options, J and C statistics', 'https://bashtage.github.io/linearmodels/iv/introduction.html')],
    ),
    (
        '3.35',
        8,
        'Testing factor models: GRS, Fama–MacBeth and the Shanken correction',
        "Test a factor model with the Gibbons–Ross–Shanken alpha test and Fama–MacBeth risk prices, and explain what Shanken's errors-in-variables correction does and does not fix.",
        r"""Lesson 3.20 kept factor loadings and risk premiums apart. This lesson tests whether a set of factors prices a set of test assets. There are two routes, and they have different null hypotheses.

**Time-series route: are the alphas zero?** Let $r_t$ be the $N\times1$ vector of test-asset excess returns and $f_t$ the $L\times1$ vector of factors, observed for $t=1,\dots,T$. If every factor is itself a traded excess return, the model implies $E[r_t]=B\,E[f_t]$, so the intercepts of

$$r_t=\alpha+Bf_t+\varepsilon_t$$

must all be zero. Gibbons, Ross and Shanken (1989) derived an exact test of $H_0:\alpha=0$. Let $\hat\mu_f$ and $\hat\Omega$ be the sample mean and covariance of the factors and $\hat\Sigma$ the covariance of the regression residuals, all computed with divisor $T$ (the maximum-likelihood convention). If the residuals are i.i.d. normal given the factors,

$$F=\frac{T-N-L}{N}\,\frac{\hat\alpha^\top\hat\Sigma^{-1}\hat\alpha}{1+\hat\theta_f^2}\sim F_{N,\,T-N-L},\qquad \hat\theta_f^2=\hat\mu_f^\top\hat\Omega^{-1}\hat\mu_f$$

Three readings of this statistic matter.
- It is a Wald test. With $W=T\hat\alpha^\top\hat\Sigma^{-1}\hat\alpha/(1+\hat\theta_f^2)$, the Wald statistic of Lesson 3.33, we have $F=\frac{T-N-L}{NT}W$. GRS is the exact finite-sample form of a test that is otherwise only asymptotically $\chi^2_N$, and the $\chi^2$ version rejects too readily in short samples.
- It measures economic size. $\hat\theta_f^2$ is the squared Sharpe ratio of the factors' ex post tangency portfolio, and $\hat\alpha^\top\hat\Sigma^{-1}\hat\alpha$ equals the gain in squared Sharpe ratio when the test assets join the factors. The p-value says whether that gain is noise; the gain says how big it is.
- It needs $T>N+L$ and in practice $T\gg N$, because $\hat\Sigma$ has $N(N+1)/2$ free elements. The exact $F$ law also needs normal, homoskedastic, serially independent residuals. When those fail, use the robust Wald test from GMM (Lesson 3.34), which is only asymptotic.

If a factor is not a return, $E[f_t]$ is not its risk price and $\alpha=0$ is the wrong restriction. The cross-sectional route handles that case.

**Cross-sectional route: do betas price average returns?** The model also says $E[r_{it}]=\beta_i^\top\lambda$ for every asset $i$. The two-pass method of Fama and MacBeth (1973) proceeds in two steps.
1. Pass one: a time-series regression for each asset gives $\hat\beta_i$.
2. Pass two: in each month $t$, regress $r_{it}$ on $\hat\beta_i$ across the assets, giving slopes $\hat\lambda_t$ and residuals $\hat e_{it}$.

The estimate is $\hat\lambda=\frac1T\sum_t\hat\lambda_t$, and its standard error comes from the spread of the monthly slopes:

$$\widehat{SE}(\hat\lambda)=\frac{s_\lambda}{\sqrt T},\qquad s_\lambda^2=\frac1{T-1}\sum_{t=1}^T(\hat\lambda_t-\hat\lambda)^2$$

Time-series spread absorbs the correlation among residuals within a month without modelling it. It assumes the slopes are uncorrelated over time (otherwise apply Newey–West to the slope series, Lesson 3.11) and it treats $\hat\beta_i$ as known. The average residuals $\hat\alpha_i=\frac1T\sum_t\hat e_{it}$ are the pricing errors. With excess returns the pass-two intercept should be zero, and for a traded factor $\lambda$ should equal the factor's mean return; GRS uses neither restriction.

**Errors in variables and Shanken's correction.** The pass-two regressors are estimates, $\hat\beta_i=\beta_i+\eta_i$, which causes two separate problems.
- Bias. As in Lesson 3.12, classical measurement error attenuates the slope by the reliability ratio $\sigma_\beta^2/(\sigma_\beta^2+\sigma_\eta^2)$, where $\sigma_\beta^2$ is the cross-sectional variance of the true betas and $\sigma_\eta^2$ the average sampling variance of $\hat\beta_i$. The intercept is pushed up. Sorting assets into portfolios on beta cuts $\sigma_\eta^2$ while keeping the spread of betas.
- Standard errors. The error in $\hat\beta_i$ adds noise to $\hat\lambda$ that the monthly slopes do not reveal. Shanken (1992) showed that the conventional standard error is too small and derived the asymptotically valid adjustment. For one factor,

$$\widehat{Var}_S(\hat\lambda)=\frac1T\Big[(1+\hat\kappa)\big(s_\lambda^2-\hat\sigma_f^2\big)+\hat\sigma_f^2\Big],\qquad \hat\kappa=\hat\lambda^\top\hat\Sigma_f^{-1}\hat\lambda$$

Here $\hat\sigma_f^2$ is the factor's sample variance; with several factors, $s_\lambda^2$ and $\hat\sigma_f^2$ become the covariance matrices of the slope vectors and of the factors. Read it as a split. The slope variance $s_\lambda^2$ is factor variation, $\hat\sigma_f^2$, plus cross-sectional noise, $s_\lambda^2-\hat\sigma_f^2$, and only the noise is inflated, by $1+\hat\kappa$. Multiplying the whole Fama–MacBeth variance by $1+\hat\kappa$ is a cruder, conservative shortcut. For a traded factor $\hat\kappa$ is the squared Sharpe ratio per period, so the multiplier is modest at monthly frequency. Use per-period quantities: an annualised Sharpe ratio would inflate the multiplier by the number of periods per year. The correction repairs the standard error only. It does not undo the attenuation, which is why long samples and portfolios still matter.

**Why a significant risk price can coexist with large pricing errors.** The two tests have different nulls and different noise.
1. $H_0:\lambda=0$ asks whether average returns have any slope against beta. $H_0:\alpha=0$ asks whether the line passes through every asset. A line can be steep and well measured yet miss several assets by more than their sampling error.
2. For a traded factor the premium's t ratio is about $\sqrt T\,\hat\theta_f$, which depends on the factor's Sharpe ratio, while $F$ depends on the alphas relative to residual noise. Both grow with $T$, and neither implies the other.
3. Lewellen, Nagel and Shanken (2010) criticise judging a model by its fit to size and book-to-market portfolios alone: a high cross-sectional $R^2$ and small pricing errors there can be weak evidence for it. Report the pricing errors and their joint test beside the risk prices, and never read either alone as validation.""",
        r"""Cedar Capital's research desk tests a one-factor market model on two fictional portfolios, small-cap value (1) and large-cap growth (2). Returns are in percent per month.

**Part 1: GRS with $T=60$, $N=2$, $L=1$.** The time-series regressions return alphas $\hat\alpha=(0.50,\,-0.30)$, residual variances 4.00 and 6.25 with covariance 2.50 (volatilities 2.00 and 2.50, correlation 0.50, divisor $T$), and a market mean $\hat\mu_f=0.60$ with variance $\hat\Omega=16.00$.

1. The determinant is $4.00\times6.25-2.50^2=18.75$, so the inverse is
$$\hat\Sigma^{-1}=\frac1{18.75}\begin{pmatrix}6.25&-2.50\\-2.50&4.00\end{pmatrix}$$
2. The quadratic form is
$$\hat\alpha^\top\hat\Sigma^{-1}\hat\alpha=\frac{6.25(0.50)^2-2(2.50)(0.50)(-0.30)+4.00(-0.30)^2}{18.75}=\frac{1.5625+0.75+0.36}{18.75}=\frac{2.6725}{18.75}=0.14253$$
3. The market's squared Sharpe ratio is $\hat\theta_f^2=0.60^2/16.00=0.0225$. Adding the two portfolios lifts the squared Sharpe ratio from 0.0225 to 0.16503.
4. $F=\frac{57}{2}\times\frac{0.14253}{1.0225}=3.973$ on $(2,57)$ degrees of freedom. When $N=2$ the $F_{2,m}$ survival function has the closed form $(1+2F/m)^{-m/2}$, which gives $p=0.0243$ and a 5% critical value of 3.159. The alphas are jointly significant at 5%.
5. Each alpha's OLS standard error is $\sqrt{(1+\hat\theta_f^2)\,\hat\sigma_{ii}/(T-L-1)}$, where $\hat\sigma_{ii}$ is the divisor-$T$ residual variance, so $t=1.883$ and $t=-0.904$. Neither alpha is significant alone.
6. The asymptotic Wald statistic is $W=60\times0.14253/1.0225=8.364$, with $p=e^{-W/2}=0.0153$. It rejects a little more readily than the exact test.

The joint test rejects because the alphas have opposite signs while the residuals are positively correlated. A long-short pair of the two portfolios has a precisely measured alpha, and the quadratic form sees that where two separate t tests cannot.

**Part 2: the same estimates over 600 months.** For a traded factor the premium is its mean, with t ratio about $\hat\mu_f\sqrt T/\hat\sigma_f$. That is $0.60\sqrt{60}/4.00=1.162$ in Part 1, an insignificant risk price beside significant pricing errors. Over 600 months it would be $0.60\sqrt{600}/4.00=3.674$. If the same alphas and covariances held for 600 months, $F=\frac{597}{2}\times\frac{0.14253}{1.0225}=41.61$ against a 5% critical value of 3.011. A significant risk price and jointly significant pricing errors would then coexist.

**Part 3: how much attenuation?** Take a true price of risk of 0.60 and a mean beta of 1. For beta-sorted portfolios with $\sigma_\beta=0.30$ and sampling standard error $\sigma_\eta=0.10$, the reliability ratio is $0.09/(0.09+0.01)=0.900$ and the pass-two intercept is pushed up by $(1-0.900)\times0.60=0.060$. For single stocks with $\sigma_\beta=0.40$ and $\sigma_\eta=0.30$ the ratio is $0.16/(0.16+0.09)=0.640$ and the intercept bias is $0.216$ percent per month. Shanken's multiplier, introduced next, changes neither number.

**Part 4: Fama–MacBeth with a non-traded factor.** A sentiment index is not a return, so $\alpha=0$ is not the restriction and GRS does not apply; the desk prices it from the cross-section. Eight monthly cross-sectional slopes, in percent per unit of the index, are $2.1,\,-0.8,\,1.4,\,0.3,\,2.6,\,-1.5,\,0.9,\,-0.2$, and the index was scaled to sample variance $\hat\sigma_f^2=1.00$.

1. The mean slope is $\hat\lambda=4.8/8=0.60$. The squared deviations sum to 14.08, so $s_\lambda^2=14.08/7=2.0114$ and $s_\lambda=1.418$.
2. $\widehat{SE}=1.418/\sqrt8=0.5014$ and $t=1.197$, to be compared with $t_{0.975,7}=2.365$ (the $t_{T-1}$ convention).
3. For Shanken, $\hat\kappa=0.60^2/1.00=0.36$, so the multiplier is 1.36. The cross-sectional noise is $s_\lambda^2-\hat\sigma_f^2=1.0114$, and
$$\widehat{Var}_S=\frac{1.36\times1.0114+1.00}{8}=0.2969,\qquad SE_S=\sqrt{0.2969}=0.5449,\qquad t_S=\frac{0.60}{0.5449}=1.101$$
4. The crude shortcut gives $0.5014\sqrt{1.36}=0.5848$ and $t=1.026$.

The correction raises the standard error by 8.7% and lowers $t$ from 1.197 to 1.101. Neither reaches 2.365: eight months cannot price any factor, and the exercise is about the arithmetic.""",
        r"""**Running it with real libraries.**
- GRS: fit one `statsmodels` OLS per test portfolio on the same factor matrix (`sm.add_constant`), stack the intercepts into $\hat\alpha$, form $\hat\Sigma$ as `resid.T @ resid / T`, compute $F$ and take `scipy.stats.f.sf(F, N, T-N-L)`. Use divisor $T$ throughout: plugging in an unbiased $\hat\Sigma$ (divisor $T-L-1$) understates the quadratic form by the factor $(T-L-1)/T$.
- `linearmodels.asset_pricing.TradedFactorModel(portfolios, factors).fit(cov_type="robust")`, or `"kernel"` for HAC, returns `alphas` and a `j_statistic`. That statistic is a robust Wald test against $\chi^2_N$, not the exact $F$, so compute GRS by hand when you want the finite-sample test.
- By hand: loop over months with `sm.OLS(r_t, sm.add_constant(betas)).fit()`, collect the slope series, and report `slopes.mean()` and `slopes.std(ddof=1) / np.sqrt(T)`, then the Shanken-adjusted version from the formula above.
- `linearmodels.panel.FamaMacBeth(y, X).fit(cov_type="kernel")` runs the monthly regressions, averages them and uses $t_{T-1}$ for inference. It treats the regressors as given, so betas estimated in pass one need the Shanken adjustment applied by hand to its slope covariance.
- `linearmodels.asset_pricing.LinearFactorModel(portfolios, factors).fit(cov_type="kernel")` estimates risk premia from average returns for traded or non-traded factors. Its covariance comes from the stacked multi-step GMM moments (Lesson 3.34), which include the first-pass beta uncertainty, so it plays the role of Shanken's formula. Its `j_statistic` is a Wald test of the pricing errors against a $\chi^2$ law with $N-K$ degrees of freedom when no risk-free rate is estimated.

**Failure modes.**
- Too many assets. When $N$ approaches $T$, $\hat\Sigma$ is nearly singular, the statistic is noisy and the test loses power, so a non-rejection may only reflect that.
- Broken assumptions. Fat tails, volatility clustering and autocorrelation invalidate the exact $F$ law. Use the robust or HAC Wald test, and a dependent bootstrap (Lesson 3.27) when $T$ is small.
- Weak test assets. If the portfolios share one low-dimensional factor structure, almost any factor can show a high cross-sectional $R^2$. Add portfolios sorted on other characteristics, report $R^2$ with confidence intervals, and for a traded factor check that $\hat\lambda$ is close to the factor's sample mean.
- Units and frequency. Keep $\hat\lambda$, $\hat\sigma_f^2$ and the data in the same period. Mixing percent with decimals, or monthly slopes with an annual Sharpe ratio, corrupts the multiplier.
- Bias that no standard error repairs. Shanken's correction fixes the standard error, not the point estimate. With ten assets, betas spread from 0.5 to 1.5, 60 months and residual volatility four times the factor's, the reliability ratio is about 0.28 and a simulation of that design averaged a pass-two slope of 0.30 against a true price of risk of 1.0. No standard error repairs that.
- Statistical versus economic size. With long samples, trivial alphas reject. Report $\sqrt{\hat\alpha^\top\hat\alpha/N}$ and the Sharpe-ratio gain beside the p-value.

**Reporting.** State the sample, frequency, test-portfolio construction and factor source. Give $F$ with both degrees of freedom and its p-value, the average pricing error, and the risk prices with Fama–MacBeth and Shanken-adjusted t ratios. A model that is rejected can still be the best available description, and a model that is not rejected may simply have been tested with little power.""",
        'F=\\frac{T-N-L}{N}\\,\\frac{\\hat\\alpha^\\top\\hat\\Sigma^{-1}\\hat\\alpha}{1+\\hat\\mu_f^\\top\\hat\\Omega^{-1}\\hat\\mu_f}\\sim F_{N,\\,T-N-L}',
        r"""from math import sqrt, exp, log

# Part 1: GRS test with N = 2 portfolios, L = 1 factor and T = 60 months.
# Every covariance uses divisor T (maximum-likelihood convention).
T = 60
N = 2
L = 1
a1 = 0.50
a2 = -0.30
s11 = 4.00
s12 = 2.50
s22 = 6.25
mu_f = 0.60
var_f = 16.00

det = s11 * s22 - s12 * s12
print("Determinant:", round(det, 2))
# Inverse of [[s11, s12], [s12, s22]] is (1 / det) * [[s22, -s12], [-s12, s11]].
numerator = s22 * a1 * a1 - 2 * s12 * a1 * a2 + s11 * a2 * a2
print("Quadratic form numerator:", round(numerator, 4))
q = numerator / det
theta = mu_f * mu_f / var_f
print("Squared Sharpe ratio gain:", round(q, 5))
print("Factor squared Sharpe ratio:", round(theta, 4))
print("Squared Sharpe ratio with test assets:", round(theta + q, 5))
m = T - N - L
F = m / N * q / (1 + theta)
print("GRS F statistic:", round(F, 3))
# These closed forms hold only because N = 2: the survival function of F(2, m) is
# (1 + 2F/m) ** (-m/2) and that of chi-square(2) is exp(-x/2).
p = exp(-m / 2 * log(1 + 2 * F / m))
print("GRS p-value:", round(p, 4))
crit = m / 2 * (exp(-2 / m * log(0.05)) - 1)
print("GRS critical value:", round(crit, 3))
W = T * q / (1 + theta)
print("Wald statistic:", round(W, 3))
print("Wald p-value:", round(exp(-W / 2), 4))
t1 = a1 / sqrt((1 + theta) * s11 / (T - L - 1))
t2 = a2 / sqrt((1 + theta) * s22 / (T - L - 1))
print("Alpha t statistic, portfolio 1:", round(t1, 3))
print("Alpha t statistic, portfolio 2:", round(t2, 3))

# Part 2: the same estimates over 600 months.
T_long = 600
m_long = T_long - N - L
print("Premium ratio, 60 months:", round(mu_f * sqrt(T) / sqrt(var_f), 3))
print("Premium ratio, 600 months:", round(mu_f * sqrt(T_long) / sqrt(var_f), 3))
F_long = m_long / N * q / (1 + theta)
print("GRS F statistic, 600 months:", round(F_long, 2))
crit_long = m_long / 2 * (exp(-2 / m_long * log(0.05)) - 1)
print("GRS critical value, 600 months:", round(crit_long, 3))

# Part 3: attenuation of the pass-two slope by errors in the first-pass betas.
true_lambda = 0.60
rel_port = 0.30 ** 2 / (0.30 ** 2 + 0.10 ** 2)
rel_stock = 0.40 ** 2 / (0.40 ** 2 + 0.30 ** 2)
print("Reliability ratio, portfolios:", round(rel_port, 3))
print("Intercept bias, portfolios:", round((1 - rel_port) * true_lambda, 3))
print("Reliability ratio, stocks:", round(rel_stock, 3))
print("Intercept bias, stocks:", round((1 - rel_stock) * true_lambda, 3))

# Part 4: Fama-MacBeth slopes of a non-traded factor, then Shanken's correction.
slopes = [2.1, -0.8, 1.4, 0.3, 2.6, -1.5, 0.9, -0.2]
var_index = 1.00
n = len(slopes)
lam = sum(slopes) / n
ss = 0.0
for x in slopes:
    ss += (x - lam) ** 2
var_s = ss / (n - 1)
sd_s = sqrt(var_s)
print("Mean slope:", round(lam, 4))
print("Sum of squared deviations:", round(ss, 2))
print("Slope variance:", round(var_s, 4))
print("Slope standard deviation:", round(sd_s, 3))
se_fm = sd_s / sqrt(n)
print("Fama-MacBeth standard error:", round(se_fm, 4))
print("Fama-MacBeth t statistic:", round(lam / se_fm, 3))
# The two-sided 5 percent critical value of t with 7 degrees of freedom is 2.365 (table value).
kappa = lam * lam / var_index
noise = var_s - var_index
var_shanken = ((1 + kappa) * noise + var_index) / n
se_shanken = sqrt(var_shanken)
print("Shanken multiplier:", round(1 + kappa, 3))
print("Cross-sectional noise variance:", round(noise, 4))
print("Shanken variance:", round(var_shanken, 4))
print("Shanken standard error:", round(se_shanken, 4))
print("Shanken t statistic:", round(lam / se_shanken, 3))
se_short = se_fm * sqrt(1 + kappa)
print("Shortcut standard error:", round(se_short, 4))
print("Shortcut t statistic:", round(lam / se_short, 3))
print("Standard error increase percent:", round((se_shanken / se_fm - 1) * 100, 1))""",
        "Repeat Part 1 with T = 120 months, N = 2, L = 1, alphas 0.30 and −0.20, residual variances 3.00 and 5.00 with covariance 1.80 (divisor T), and a market mean of 0.80 with variance 20.25. Compute the determinant, the quadratic form, the GRS F statistic with its p-value and 5% critical value (use the N = 2 closed forms), the Wald statistic, and the two alpha t statistics. Then take six monthly Fama–MacBeth slopes 1.4, −0.2, 1.1, 0.5, 2.0, −0.6 for a non-traded factor with sample variance 0.64: compute the mean slope, its Fama–MacBeth t statistic, Shanken's multiplier and the Shanken-corrected t statistic, and compare with the t(5) critical value 2.571. Finally say whether the market premium's ratio √T·μ̂/σ̂ and the GRS test tell the same story, and why.",
        "Part 1. The determinant is 3.00 × 5.00 − 1.80² = 11.76. The quadratic form is [5.00(0.30)² − 2(1.80)(0.30)(−0.20) + 3.00(0.20)²] / 11.76 = (0.45 + 0.216 + 0.12) / 11.76 = 0.06684. The market's squared Sharpe ratio is 0.80² / 20.25 = 0.03160, so F = (117 / 2) × 0.06684 / 1.03160 = 3.790 on (2, 117) degrees of freedom. The closed-form p-value is (1 + 2 × 3.790 / 117)^(−58.5) = 0.0254 and the 5% critical value is 58.5 × (0.05^(−2/117) − 1) = 3.074, so the alphas are jointly significant at 5%. The Wald statistic is 120 × 0.06684 / 1.03160 = 7.775 with p = exp(−3.887) = 0.0205. The alpha standard errors are sqrt(1.03160 × 3.00 / 118) = 0.1619 and sqrt(1.03160 × 5.00 / 118) = 0.2091, so t = 1.852 and t = −0.957: neither is significant alone, because the alphas have opposite signs and the residuals are positively correlated. Part 2. The mean slope is 4.2 / 6 = 0.70, the squared deviations sum to 4.88, so the sample variance is 0.976 and the standard deviation is 0.988. The Fama–MacBeth standard error is 0.988 / sqrt(6) = 0.4033 and t = 1.736, below 2.571. Shanken's κ = 0.70² / 0.64 = 0.7656, so the multiplier is 1.7656. The cross-sectional noise is 0.976 − 0.64 = 0.336, the corrected variance is (1.7656 × 0.336 + 0.64) / 6 = 0.2055, the standard error is 0.4534 (12.4% larger) and t = 0.70 / 0.4534 = 1.544. The multiplier matters more here than in the lesson because κ is large and the noise is a big share of the slope variance. Interpretation. The market premium's ratio is 0.80 × sqrt(120) / 4.50 = 1.947, just under 1.96, so the risk price is not significant while the pricing errors are: the two tests answer different questions, and with a longer sample both could be significant together. Caveat: six slopes are far too few for Shanken's asymptotic result, so the numbers are practice for the arithmetic, not evidence about any factor.",
        [
            (
                "A single factor has a monthly mean premium estimate of 0.50 percent and a monthly standard deviation of 2.50 percent. Shanken's multiplier 1 + λ̂²/σ̂_f², computed in monthly units, is:",
                ['1.20', '1.48', '1.04'],
                2,
                'λ̂²/σ̂_f² = (0.50 / 2.50)² = 0.04, so the multiplier is 1.04. Forgetting to square gives 1.20. Using an annualised ratio (0.04 × 12 = 0.48) gives 1.48, which overstates the correction because the slopes are monthly.',
            ),
            (
                "A factor's Fama–MacBeth risk price is significant after Shanken's correction (t = 3.2), yet the GRS test of the same model rejects with p = 0.001. The most defensible reading is:",
                ['One of the two tests must be wrong, because a priced factor cannot leave pricing errors', 'The factor earns a premium, but the model still leaves pricing errors that its betas do not explain', 'The GRS test is invalid whenever a risk price is significant'],
                1,
                'The risk-price test asks whether average returns have any slope against beta. The GRS test asks whether the line passes through every asset. Both can hold at once, so report the pricing errors beside the risk prices.',
            ),
            (
                "In a GRS test with T = 63 months, N = 2 portfolios and L = 1 factor, α̂′Σ̂⁻¹α̂ = 0.10 and the factor's squared Sharpe ratio is 0.05 (divisor T throughout). The F statistic is closest to:",
                ['2.86', '3.00', '3.15'],
                0,
                '(T − N − L) / N = 60 / 2 = 30 and 0.10 / (1 + 0.05) = 0.09524, so F = 30 × 0.09524 = 2.857, compared with F(2, 60). Omitting the 1 + θ² denominator gives 3.00; multiplying by it gives 3.15.',
            ),
            (
                'The Wald test of H0: α = 0 (Lesson 3.33) and the GRS statistic are related as follows:',
                ['They test unrelated null hypotheses', 'GRS is the exact finite-sample F version of the same Wald test under i.i.d. normal errors, F = (T − N − L) / (N T) × W', 'GRS is the asymptotic chi-square version of the Wald test'],
                1,
                'W = T α̂′Σ̂⁻¹α̂ / (1 + θ̂²) is asymptotically chi-square with N degrees of freedom. Rescaling it by (T − N − L) / (N T) gives a statistic with an exact F(N, T − N − L) law under normality. In the Cedar example F = 57 / 120 × 8.364 = 3.973.',
            ),
        ],
        [('Gibbons, Ross & Shanken (1989) · A Test of the Efficiency of a Given Portfolio', 'https://doi.org/10.2307/1913625'), ('Shanken (1992) · On the Estimation of Beta-Pricing Models', 'https://doi.org/10.1093/rfs/5.1.1'), ('Lewellen, Nagel & Shanken (2010) · A skeptical appraisal of asset pricing tests', 'https://doi.org/10.1016/j.jfineco.2009.09.001'), ('linearmodels contributors · Formulas and mathematical detail for linear factor models', 'https://bashtage.github.io/linearmodels/asset-pricing/mathematical-formula.html')],
    ),
    (
        '3.36',
        8,
        'Predictive regressions with persistent predictors',
        'Quantify Stambaugh bias, overlap-inflated t statistics and out-of-sample R² for a persistent return predictor, and say why in-sample fit and out-of-sample usefulness diverge.',
        r"""Return prediction regresses future returns on a persistent, price-based variable such as a dividend yield. The standard system is

$$r_{t+1}=\alpha+\beta x_t+u_{t+1},\qquad x_{t+1}=\theta+\rho x_t+v_{t+1}$$

where $(u_t,v_t)$ are i.i.d. normal with variances $\sigma_u^2$, $\sigma_v^2$ and covariance $\sigma_{uv}$, and $|\rho|<1$ but often close to one. The predictor is predetermined, $E[u_{t+1}\mid x_t]=0$, so OLS is consistent. It is not strictly exogenous, which is what unbiasedness needs: $x_{t+1}$ contains $v_{t+1}$, which is correlated with $u_{t+1}$, and $x_{t+1}$ is a regressor in the next observation. This is weaker than the contemporaneous endogeneity of Lesson 3.12, which makes OLS inconsistent. Here OLS stays consistent but is biased in finite samples.

**Stambaugh's bias.** Write $u_{t+1}=\gamma v_{t+1}+e_{t+1}$ with $\gamma=\sigma_{uv}/\sigma_v^2$. Under normality $e$ is independent of every $v$, hence of the whole path of $x$. Let $\tilde x_t$ be the demeaned lagged predictor. The predictive slope error is $\sum\tilde x_tu_{t+1}/\sum\tilde x_t^2$ and the autoregressive error is $\hat\rho-\rho=\sum\tilde x_tv_{t+1}/\sum\tilde x_t^2$, with the same denominator, so

$$\hat\beta-\beta=\gamma(\hat\rho-\rho)+\frac{\sum\tilde x_te_{t+1}}{\sum\tilde x_t^2}$$

The last term has mean zero. Therefore $E[\hat\beta-\beta]=\gamma\,E[\hat\rho-\rho]$ exactly (Stambaugh 1999). The autoregressive coefficient is biased downward in small samples, $E[\hat\rho-\rho]\approx-(1+3\rho)/T$ (Kendall 1954), so

$$E[\hat\beta-\beta]\approx-\gamma\,\frac{1+3\rho}{T}$$

The bias grows with persistence and with $|\gamma|$ and shrinks with $T$. The approximation is first-order and slightly understates the bias near a unit root.

**Why valuation ratios bias the slope upward.** A return shock that comes from a price rise lowers the dividend yield, so unless cash-flow news dominates, $\sigma_{uv}<0$ and $\gamma<0$. Then $\gamma\,E[\hat\rho-\rho]>0$: OLS overstates a positive slope and, when the true $\beta=0$, centres the t statistic above zero, so the usual critical values reject "no predictability" too often. Campbell and Yogo (2006) propose a pretest that flags when the conventional t test is unreliable for a persistent predictor, and a replacement test designed to stay valid there. Amihud and Hurvich (2004) reduce the bias by adding the predictor's autoregressive residual as an extra regressor.

**Overlapping long-horizon regressions.** Regress the $h$-month return $r_{t+1:t+h}=\sum_{j=1}^{h}r_{t+j}$ on $x_t$, sampled monthly. Neighbouring errors share $h-1$ months, so they follow an MA($h-1$) pattern (Lesson 3.11). Under the null of no predictability, with i.i.d. monthly shocks (ignoring their correlation with $v$) and a predictor whose autocorrelations are $\rho^j$, the true variance of the slope is the OLS formula multiplied by

$$VIF_h=1+2\sum_{j=1}^{h-1}\Big(1-\frac jh\Big)\rho^{j}$$

This is 1 when $\rho=0$ and approaches $h$ as $\rho\to1$, so persistent predictors are exactly where OLS t statistics mislead. Newey–West with $L=h-1$ shrinks the autocovariances by the Bartlett weights $1-j/h$, so its expected variance factor is only $1+2\sum_{j=1}^{h-1}(1-j/h)^2\rho^j$, below $VIF_h$, and a t statistic that survives it can still be too large. In Monte Carlo experiments Hodrick (1992) found the Hansen and Hodrick (1980) estimator biased at long horizons, and found that alternatives, among them an estimator derived under the null and a vector autoregression, performed better.

**Out-of-sample R².** Fit the regression on data available before date $t$, using an expanding or rolling window, and forecast $\hat r_t$. Let $\bar r_t$ be the historical mean over the same data. Campbell and Thompson (2008) define

$$R^2_{OS}=1-\frac{\sum_t(r_t-\hat r_t)^2}{\sum_t(r_t-\bar r_t)^2}$$

It is positive when the regression beats the historical mean. In-sample $R^2$ cannot be negative, because OLS minimises the sum of squares over that sample, but $R^2_{OS}$ can be. Three things separate the two.
1. Estimation noise. With $n$ training observations and Gaussian i.i.d. data, an OLS forecast with one predictor has expected squared error near $\sigma^2(1+2/n)$, while the historical mean has $\sigma_r^2(1+1/n)$ with $\sigma_r^2=\sigma^2/(1-R^2)$. The regression has the smaller expected squared error only if the population $R^2$ exceeds about $1/(n+2)$, which is 0.82% for $n=120$. This is a rule of thumb from those approximations, not an empirical finding, and it is optimistic for a persistent predictor. The extra forecast variance from estimating the slope scales with $d^2/S_{xx}$, where $d$ is the distance of the current predictor from the window mean and $S_{xx}$ is the window's sum of squared deviations. For an AR(1) predictor with variance $\sigma_x^2=\sigma_v^2/(1-\rho^2)$ we have $E[S_{xx}]=\sigma_x^2\,n_{\text{eff}}$, where $n_{\text{eff}}=n-\frac1n\sum_{s,t}\rho^{|s-t|}$ falls far below $n$ when $\rho$ is near one. The break-even then rises to about $1/(n_{\text{eff}}+1)$, which is 1.13% for $\rho=0.95$ and $n=120$. A simulation of that design puts it nearer 1.2%, so even this is slightly optimistic.
2. Bias and instability. The Stambaugh bias inflates the in-sample slope, and a slope that drifts makes the full-sample fit stale.
3. Selection. A predictor chosen after looking at the whole sample has already used the information the out-of-sample test was meant to withhold (Lesson 3.28).

Nested comparisons add a wrinkle. A regression's estimated slope adds noise to its forecasts even when the true slope is zero, so $R^2_{OS}$ is expected to be negative under the null and also under small true predictability, and a slightly negative value does not by itself rule predictability out. Clark and West (2007) adjust the squared-error difference for that noise before testing it. Campbell and Thompson found that imposing sign restrictions on the slope and on the forecast lets many predictive regressions beat the historical average, with out-of-sample gains that are small but not negligible in their mean-variance investor calculation.""",
        r"""Cedar Capital's research desk asks whether the dividend yield predicts next month's excess return on a fictional equity index. Returns are in percent per month, the yield $x_t$ is in percentage points, and the sample has $T=240$ months.

1. **Persistence.** The AR(1) fit of the yield gives $\hat\rho=0.95$, which we use as $\rho$ in the bias formula. Then $E[\hat\rho-\rho]\approx-(1+3\times0.95)/240=-0.01604$.
2. **Slope bias.** The residual covariance estimates give $\sigma_{uv}/\sigma_v^2=-12.75$ (percent of return per point of yield). The slope bias is $(-12.75)\times(-0.01604)=+0.2045$ percent per point.
3. **Corrected slope.** The OLS slope is $\hat\beta=0.70$ with standard error 0.34, so $t=2.059$ and the in-sample $R^2=t^2/(t^2+T-2)=1.75\%$. The bias is 0.602 standard errors. The corrected slope is $0.70-0.2045=0.4955$, which gives $t=1.457$ if the OLS standard error is kept; that simple subtraction ignores the sampling error of the correction. Because $R^2=\hat\beta^2S_{xx}/S_{yy}$, the corrected slope implies an $R^2$ of $1.75\%\times(0.4955/0.70)^2=0.88\%$.
4. **Overlap.** Regressing 12-month returns on the same yield gives an OLS t of 4.80. With $\rho=0.95$ and $h=12$ the variance factor is $VIF_{12}=9.889$, a standard-error factor of $\sqrt{9.889}=3.145$, so the corrected $t=4.80/3.145=1.526$. The Newey–West factor with 11 lags is $1+2\sum(1-j/12)^2(0.95)^j=6.943$, a standard-error factor of 2.635, so its $t=1.822$ would still be too large.
5. **Out-of-sample.** A rolling-window recursion fits on the previous 120 months and forecasts the next month, 120 times, so $n=120$ throughout. The squared forecast errors sum to 1,862.0 for the regression and 1,856.0 for the historical mean, so $R^2_{OS}=1-1862/1856=-0.32\%$. The i.i.d. break-even population $R^2$ is $1/(120+2)=0.82\%$, a little below the 0.88% the corrected slope implies, and the i.i.d. rule of thumb expects $R^2_{OS}\approx1-(1+2/120)(1-0.0088)/(1+1/120)=+0.06\%$. But the yield is persistent. Its effective window size is $n_{\text{eff}}=87.3$ rather than 120, so the break-even rises to $1/(87.3+1)=1.13\%$, above the 0.88% the corrected slope implies. Repeating the expected-error calculation with that adjustment gives $R^2_{OS}\approx-0.25\%$, and the observed $-0.32\%$ is a loss of that kind.

In-sample fit looks respectable ($t=2.06$, $R^2=1.75\%$). Removing the bias roughly halves the $R^2$ to 0.88%, which is below the persistence-adjusted break-even of 1.13% for 120 training months, so the regression is not expected to beat the historical mean out of sample. The 12-month regression's t statistic of 4.80 mostly counted overlapping months more than once.""",
        r"""**Running it with real libraries.**
- Predictive regression: `sm.OLS(r[1:], sm.add_constant(x[:-1])).fit()` regresses $r_{t+1}$ on $x_t$. Align timestamps so $x_t$ is known when the forecast is made. The predictor's AR(1) is `sm.OLS(x[1:], sm.add_constant(x[:-1])).fit()`. Its residuals $\hat v$ and the predictive residuals $\hat u$ give $\hat\gamma$ as `np.cov(u_hat, v_hat)[0, 1] / np.var(v_hat, ddof=1)`.
- Bias adjustment: subtract the estimated bias, $-\hat\gamma(1+3\hat\rho)/T$, as in the example, or run the Amihud and Hurvich (2004) augmented regression, which adds $\hat v_{t+1}$ as a regressor. Resample the pairs $(\hat u,\hat v)$ jointly (Lesson 3.27) to get a standard error for the adjusted slope, or simulate the fitted system with $\beta=0$ to see how the t statistic behaves under the null.
- Overlap: `.fit(cov_type="HAC", cov_kwds={"maxlags": L})` with $L\ge h-1$, preferably longer. Treat the result as optimistic when the predictor is persistent, and cross-check with non-overlapping observations or a short-horizon vector autoregression.
- Out-of-sample: loop over origins, refit `sm.OLS` on data through date $t$ only (or use `RollingOLS(r, X, window=len(r), min_nobs=120, expanding=True)` and shift its output one period), forecast $r_{t+1}$, keep the historical-mean forecast beside it and compute $R^2_{OS}$. Do any scaling of $x$ inside the loop. For a nested comparison use the Clark–West adjusted loss differential, regressed on a constant with HAC errors when forecasts overlap, rather than a plain squared-error comparison.

**Failure modes.**
- Near-unit-root predictors. $\hat\rho$ is imprecise, and unit-root tests (Lesson 3.13) cannot tell 0.95 from 1. The t statistic's distribution depends on $\rho$, which is why Campbell and Yogo built methods that account for it.
- Look-ahead. Standardising $x$ on the full sample, choosing the window after seeing results, or benchmarking against the full-sample mean all inflate $R^2_{OS}$.
- Dependent losses. Multi-month forecasts overlap, so loss differentials are serially correlated (Lesson 3.15).
- Selection. Searching across predictors, windows and horizons multiplies the chances of a spurious win (Lesson 3.28).
- Bias that cuts the other way. If $\gamma>0$, the correction adds to the slope instead of subtracting, so check the sign of $\hat\gamma$ before interpreting.
- Statistical versus economic value. A small positive $R^2_{OS}$ can matter or not depending on how a decision uses it; Campbell and Thompson evaluate it for a mean-variance investor. This lesson studies forecasting evidence, not a trading recommendation.

**Reporting.** Give the in-sample slope with its HAC t statistic, the bias-adjusted slope, the overlap-robust t statistic, $R^2_{OS}$ with its benchmark, window and evaluation dates, the nested-model test, and the sample length. A slope that survives all of these is a stronger claim than any one of them.""",
        'E[\\hat\\beta-\\beta]=\\frac{\\sigma_{uv}}{\\sigma_v^{2}}\\,E[\\hat\\rho-\\rho]\\approx-\\frac{\\sigma_{uv}}{\\sigma_v^{2}}\\,\\frac{1+3\\rho}{T}',
        r"""from math import sqrt

# Monthly data, T = 240. Returns in percent, dividend yield in percentage points.
T = 240
rho = 0.95
gamma = -12.75
beta_hat = 0.70
se_beta = 0.34

rho_bias = -(1 + 3 * rho) / T
print("Bias in rho-hat:", round(rho_bias, 5))
slope_bias = gamma * rho_bias
print("Slope bias:", round(slope_bias, 4))
t_ols = beta_hat / se_beta
print("OLS t statistic:", round(t_ols, 3))
print("Bias in standard errors:", round(slope_bias / se_beta, 3))
beta_corr = beta_hat - slope_bias
print("Corrected slope:", round(beta_corr, 4))
print("Corrected t statistic:", round(beta_corr / se_beta, 3))
r2_in = t_ols ** 2 / (t_ols ** 2 + T - 2)
print("In-sample R-squared percent:", round(r2_in * 100, 2))
r2_corr = r2_in * (beta_corr / beta_hat) ** 2
print("Implied R-squared percent:", round(r2_corr * 100, 2))

# Overlapping 12-month regression: variance factors for the OLS formula and for Newey-West with 11 lags.
h = 12
vif = 1.0
nw = 1.0
for j in range(1, h):
    vif += 2 * (1 - j / h) * rho ** j
    nw += 2 * (1 - j / h) ** 2 * rho ** j
t_overlap = 4.80
print("Overlap variance factor:", round(vif, 3))
print("Overlap standard error factor:", round(sqrt(vif), 3))
print("Overlap-corrected t statistic:", round(t_overlap / sqrt(vif), 3))
print("Newey-West variance factor:", round(nw, 3))
print("Newey-West standard error factor:", round(sqrt(nw), 3))
print("Newey-West corrected t statistic:", round(t_overlap / sqrt(nw), 3))

# Out-of-sample: rolling 120-month window, 120 forecasts.
sse_regression = 1862.0
sse_mean = 1856.0
n_train = 120
r2_os = 1 - sse_regression / sse_mean
print("Out-of-sample R-squared percent:", round(r2_os * 100, 2))
print("Break-even R-squared percent:", round(100 / (n_train + 2), 2))
expected = 1 - (1 + 2 / n_train) * (1 - r2_corr) / (1 + 1 / n_train)
print("Expected out-of-sample R-squared percent:", round(expected * 100, 2))

# Persistence adjustment. a_sum is the sum over window pairs (s, t) of rho^|s-t|, built as
# n + 2 * sum (n - k) rho^k; s_sum is the sum of rho^k for k = 1..n; power avoids a large exponent.
power = 1.0
a_sum = n_train * 1.0
s_sum = 0.0
for k in range(1, n_train + 1):
    power *= rho
    s_sum += power
    a_sum += 2 * (n_train - k) * power
n_eff = n_train - a_sum / n_train
# d_var is the expected squared distance of the next predictor from the window mean, in units of the
# predictor's variance.
d_var = 1 - 2 * s_sum / n_train + a_sum / n_train ** 2
print("Effective window size:", round(n_eff, 1))
print("Persistence-adjusted break-even R-squared percent:", round(100 / (n_eff + 1), 2))
q = r2_corr / (1 - r2_corr)
e_regression = 1 + 1 / n_train + d_var / n_eff
e_mean = 1 + 1 / n_train + q * d_var
print("Persistence-adjusted expected out-of-sample R-squared percent:", round((1 - e_regression / e_mean) * 100, 2))""",
        'Cedar re-runs the study on another predictor with T = 360 months, ρ̂ = 0.98, σ_uv/σ_v² = −16 and an OLS slope of 0.55 with standard error 0.25. Compute the bias in ρ̂, the slope bias, the corrected slope and its t statistic with the OLS standard error held fixed, the in-sample R² (from t² / (t² + T − 2)) and the R² the corrected slope implies. A six-month overlapping regression on the same predictor reports an OLS t of 3.40: compute the variance factor for h = 6, the corrected t, the Newey–West factor with L = 5 and its t. Finally a rolling 180-month recursion has squared forecast errors of 2,310 for the regression and 2,325 for the historical mean over 180 forecasts. Compute R²_OS, the i.i.d. break-even R², and the persistence-adjusted break-even 1 / (n_eff + 1) with n_eff = n − (1/n) Σ_s Σ_t ρ^|s−t| (run the worksheet with the new inputs), and say whether the result justifies using the predictor.',
        "The bias in ρ̂ is −(1 + 3 × 0.98) / 360 = −0.01094. The slope bias is (−16) × (−0.01094) = +0.1751, which is 0.700 standard errors, so the corrected slope is 0.55 − 0.1751 = 0.3749 and t = 0.3749 / 0.25 = 1.500 with the OLS standard error held fixed. The OLS t is 2.20, so the in-sample R² is 4.84 / (4.84 + 358) = 1.33%, and the corrected slope implies 1.33% × (0.3749 / 0.55)² = 0.62%. For h = 6 and ρ = 0.98 the variance factor is 1 + 2 Σ_{j=1..5} (1 − j/6) 0.98^j = 5.771, a standard-error factor of 2.402, so the corrected t is 3.40 / 2.402 = 1.415. The Newey–West factor with L = 5 is 1 + 2 Σ (1 − j/6)² 0.98^j = 3.941, a standard-error factor of 1.985, so its t = 1.713 is still too large. The out-of-sample R² is 1 − 2310 / 2325 = +0.65%. The i.i.d. break-even is 1 / (180 + 2) = 0.55%, and the i.i.d. rule of thumb expects 1 − (1 + 2/180)(1 − 0.0062) / (1 + 1/180) = +0.07% from the implied R². With ρ = 0.98 the effective window is n_eff = 107.5, so the persistence-adjusted break-even is 1 / 108.5 = 0.92% and the adjusted expectation is −0.26%. The observed +0.65% is therefore about 0.9 points above what the persistent-predictor calculation expects. Interpretation: in this window the regression beats the historical mean, by 0.65% of the mean's squared error, but the corrected slope implies an R² of 0.62%, below the 0.92% persistence-adjusted break-even. The corrected slope is only 1.5 standard errors and the overlap-corrected t is about 1.4 to 1.7, so a positive R²_OS from one split is more likely a favourable draw than an edge. Before using the predictor one would add a Clark–West test of the squared-error difference, check other windows and sub-periods, and ask whether the gain survives an economic evaluation.",
        [
            (
                'A predictor has ρ = 0.90, the sample has T = 120 months and σ_uv/σ_v² = −10. The approximate bias of the OLS predictive slope is closest to:',
                ['−0.31', '+0.31', '+0.031'],
                1,
                'E[ρ̂ − ρ] ≈ −(1 + 3 × 0.90) / 120 = −0.03083, so the slope bias is (−10) × (−0.03083) = +0.308. The sign is positive because the covariance is negative. −0.31 flips the sign and 0.031 is only the size of the bias in ρ̂ itself.',
            ),
            (
                'In an h-month overlapping regression with i.i.d. monthly shocks and an AR(1) predictor, the true slope variance equals the OLS formula times 1 + 2 Σ_{j=1}^{h−1} (1 − j/h) ρ^j. For ρ = 0 and for ρ → 1 this factor equals, respectively:',
                ['1 and h', 'h and 1', '1 and 1'],
                0,
                'With ρ = 0 every term after the 1 vanishes, so there is no inflation. As ρ → 1 the sum becomes 2 Σ (1 − j/h) = h − 1, so the factor is h. Persistent predictors are therefore where overlapping OLS t statistics mislead most.',
            ),
            (
                'Over 100 months a recursive predictive regression has a sum of squared forecast errors of 980 and the historical mean has 960. The out-of-sample R² is closest to:',
                ['+2.1%', '−4.2%', '−2.1%'],
                2,
                'R²_OS = 1 − 980 / 960 = −0.0208, or −2.1%. The negative sign means the regression lost to the historical mean, even if its in-sample R² was positive. Doubling the figure to −4.2% has no basis.',
            ),
            (
                "Stambaugh's finite-sample bias in a predictive regression arises because the predictor is:",
                ['Non-stationary, so OLS is inconsistent', 'Predetermined but not strictly exogenous: its innovation is correlated with the return shock', 'Measured with error, so the slope is attenuated'],
                1,
                'OLS stays consistent because E[u(t+1) | x(t)] = 0, but x(t+1) contains an innovation correlated with the next return shock, which breaks strict exogeneity. The result is E[β̂ − β] = (σ_uv/σ_v²) E[ρ̂ − ρ], not non-stationarity or measurement error.',
            ),
        ],
        [('Stambaugh (1999) · Predictive regressions', 'https://doi.org/10.1016/S0304-405X%2899%2900041-0'), ('Campbell & Thompson (2008) · Predicting Excess Stock Returns Out of Sample: Can Anything Beat the Historical Average?', 'https://doi.org/10.1093/rfs/hhm055'), ('Amihud & Hurvich (2004) · Predictive Regressions: A Reduced-Bias Estimation Method', 'https://doi.org/10.1017/S0022109000003227'), ('statsmodels contributors · OLS.fit with HAC covariance options', 'https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLS.fit.html')],
    ),
    (
        '3.37',
        9,
        'Structural breaks and regime switching',
        'Test for a parameter break with a Chow test, explain why searching over break dates changes the critical values, and run the Hamilton filter for a two-state Markov-switching model.',
        r"""Lesson 3.9 tested restrictions on coefficients that were taken to be the same across the whole sample. Return relations rarely stay put: a fund changes its mandate, a rule changes, volatility moves from calm to stress. Two families of tools address this. **Break tests** ask whether a regression's coefficients changed. **Regime-switching models** let a hidden state choose the parameters each month and estimate how probable each state is now.

**The Chow test (date known in advance).** Take $y_t=x_t'\beta+u_t$ with $k$ coefficients (intercept included), $n$ observations and a break after month $\tau$, with $D_t=1\{t>\tau\}$, so the coefficients are $\beta$ before the break and $\beta+\delta$ after it:

$$y_t=x_t'\beta+D_t\,x_t'\delta+u_t,\qquad H_0:\ \delta=0 .$$

The unrestricted fit is two separate regressions, so $SSR_U=SSR_1+SSR_2$. The restricted fit pools everything and gives $SSR_R$. This is the joint F test of Lesson 3.9 with $q=k$ restrictions (Chow 1960):

$$F=\frac{(SSR_R-SSR_U)/k}{SSR_U/(n-2k)}\ \sim\ F_{k,\;n-2k}\quad\text{under }H_0 .$$

The exact F law needs three conditions: the date was fixed without looking at the returns, errors are normal with the same variance on both sides, and each segment has more than $k$ observations. When the post-break segment has no more than $k$ observations, Chow's predictive-failure form $F=\frac{(SSR_R-SSR_1)/n_2}{SSR_1/(n_1-k)}\sim F_{n_2,\,n_1-k}$ applies instead. Compare the segment variances $SSR_i/(n_i-k)$. If they differ, or errors are autocorrelated, fit the interacted regression with a HAC covariance and test $\delta=0$ with a Wald statistic against $\chi^2_k$ (Lesson 3.11).

**Unknown date: the maximum of many tests.** If the date is chosen because the fit looks best, the F table no longer applies. Each $F_\tau$ alone has an $F_{k,n-2k}$ law under $H_0$, but the largest of about $0.7n$ strongly overlapping statistics exceeds that critical value far more often than 5% of the time. Quandt (1960) proposed the maximum and Andrews (1993) derived its asymptotic null law. With candidate dates trimmed to $[\rho n,(1-\rho)n]$,

$$\sup_\tau F_\tau\ \Rightarrow\ \sup_{\rho\le s\le1-\rho}\frac{\lVert B_k(s)\rVert^2}{k\,s(1-s)},$$

where $B_k$ is a $k$-dimensional Brownian bridge. Trimming is part of the method: as $s\to0$ or $1$ the denominator vanishes and the supremum has no tight limit. The convention is $\rho=0.15$. The price is that breaks in the first and last 15% of the sample cannot be tested, often the part a practitioner cares about most. The critical values are non-standard. For $k=2$ and 15% trimming, our simulation of the limit puts the 5% point at about 5.8 to 5.9 on the F scale (the Wald statistic divided by $k$; Andrews' Wald-form tables list $k$ times this), against 3.0 for $F_{2,\infty}$. In the same simulation, applying 3.0 to the best-looking date rejects a true null in about 43% of samples. This is the selection problem of Lesson 3.28. Andrews and Ploberger (1994) add average and exponential versions, Hansen (1997) gives approximate p-values, and Bai and Perron (1998) handle several breaks.

**CUSUM checks (no date needed).** Recursive residuals predict each month from earlier months only: $w_t=(y_t-x_t'\hat\beta_{t-1})/\sqrt{1+x_t'(X_{t-1}'X_{t-1})^{-1}x_t}$ for $t=k+1,\dots,n$, with $\hat\beta_{t-1}$ fitted to months $1,\dots,t-1$. Under constant coefficients they are iid $N(0,\sigma^2)$. Brown, Durbin and Evans (1975) cumulate them, $W_r=\hat\sigma^{-1}\sum_{t=k+1}^{r}w_t$, and flag instability when $|W_r|$ leaves the funnel $\pm a\,[\sqrt{n-k}+2(r-k)/\sqrt{n-k}]$, with $a=0.948$ at the 5% level. A shift in the average prediction error pushes the path out. A slope change on a regressor whose mean is near zero, such as a factor return, moves errors up and down around zero and they cancel in the sum, so CUSUM has little power there. The CUSUM of squares reacts to variance changes, and a sup-F scan has better power against one slope break. The OLS-residual CUSUM of Ploberger and Krämer (1992) is a related but different statistic.

**A two-state Markov-switching model (Hamilton 1989).** Let $S_t\in\{1,2\}$ be an unobserved regime and

$$y_t=\mu_{S_t}+\sigma_{S_t}\varepsilon_t,\quad\varepsilon_t\sim N(0,1)\ \text{iid},\qquad\Pr(S_t=j\mid S_{t-1}=i,\text{ past})=p_{ij}.$$

In a regression, $\mu_{S_t}$ becomes $x_t'\beta_{S_t}$. The transition matrix $P=(p_{ij})$ has rows that sum to one, and its ergodic (stationary) probabilities solve $\pi'P=\pi'$:

$$\pi_1=\frac{1-p_{22}}{2-p_{11}-p_{22}},\qquad\pi_2=\frac{1-p_{11}}{2-p_{11}-p_{22}} .$$

A regime lasts $1/(1-p_{ii})$ periods on average. The second eigenvalue, $\lambda=p_{11}+p_{22}-1$, measures how persistent regime beliefs are. With different variances the unconditional law is a two-normal mixture, which typically has excess kurtosis, and persistent regimes produce volatility clustering. That rivals the GARCH explanation of Lesson 3.18, and Lamoureux and Lastrapes (1990) showed that ignoring shifts in the variance level inflates estimated GARCH persistence.

**The Hamilton filter.** Let $\xi_{t|s}(j)=\Pr(S_t=j\mid y_1,\dots,y_s)$ and let $f_j$ be regime $j$'s normal density. Start at $\xi_{1|0}=\pi$. Each month has two steps:

$$\text{predict:}\ \ \xi_{t|t-1}(j)=\sum_i p_{ij}\,\xi_{t-1|t-1}(i),$$

$$\text{update:}\ \ \xi_{t|t}(j)=\frac{f_j(y_t)\,\xi_{t|t-1}(j)}{\sum_i f_i(y_t)\,\xi_{t|t-1}(i)} .$$

The update is Bayes' rule with the prediction as the prior. Its denominator is the density of $y_t$ given the past, so the log-likelihood $\sum_t\ln\sum_i f_i(y_t)\,\xi_{t|t-1}(i)$ is a by-product of the filter. It is maximized numerically, which is the likelihood of Lesson 3.33 built by the filter. Beliefs relax toward the ergodic law: $\xi_{t+h|t}(2)=\pi_2+\lambda^h\,(\xi_{t|t}(2)-\pi_2)$.

**Predicted, filtered, smoothed.** The smoother of Kim (1994) runs backward from the last month $T$:

$$\xi_{t|T}(i)=\xi_{t|t}(i)\sum_j p_{ij}\,\frac{\xi_{t+1|T}(j)}{\xi_{t+1|t}(j)} .$$

Look-ahead has three layers. Smoothed probabilities use returns after $t$. Filtered probabilities $\xi_{t|t}$ already contain month $t$'s own return, so an exposure decision for month $t$ may use only the prediction $\xi_{t|t-1}$. And any of these built from full-sample parameter estimates leaks the future through the parameters, so a backtest must re-estimate on expanding windows. Two cautions on estimation. Regime labels are arbitrary, so impose an order such as $\sigma_1<\sigma_2$. And the likelihood-ratio test of one regime against two has no $\chi^2$ law, because $p_{ij}$ and the second regime's parameters are unidentified under the null (Hansen 1992; Garcia 1998).""",
        r"""**Part A: a Chow test.** The Cedar Capital research desk regresses the monthly excess return of a fictional dividend fund on the market's excess return for $n=120$ months ($k=2$: intercept and beta). The investment committee changed the fund's mandate after month 60, a date recorded in its minutes before anyone examined returns, so each segment has 60 observations. The fits give, in percent squared, $SSR_R=583.0$ pooled, $SSR_1=262.0$ for months 1 to 60 and $SSR_2=278.0$ for months 61 to 120.

1. Unrestricted fit: $SSR_U=262.0+278.0=540.0$.
2. Numerator $(583.0-540.0)/2=21.5$ and denominator $540.0/116=4.6552$, so $F=4.619$.
3. The 5% point of $F_{2,116}$ is 3.074, and the exact tail for two numerator degrees of freedom, $(1+2F/116)^{-58}$, gives $p=0.0118$. The date was fixed in advance, so the ordinary table applies and constant coefficients are rejected.
4. The segment residual variances differ by a ratio of 1.061, so nothing contradicts the equal-variance condition.

**Part B: the same statistic with an unknown date.** Suppose the desk had not known the date. It computes $F_\tau$ for every month from 18 to 102 (15% trimming) and the largest value is again 4.619, at month 60. The right 5% comparison is now the sup-F value of about 5.9, and the test does not reject. Identical regressions and an identical statistic give opposite conclusions, because whether the date was fixed before or after seeing the returns is part of the evidence.

**Part C: the CUSUM funnel.** With 118 recursive residuals the 5% funnel ends at $\pm0.948\sqrt{118}\times3=30.89$ at the last month, in units of the residual standard deviation.

**Part D: the Hamilton filter by hand.** The desk models monthly returns in percent. Regime 1 (calm) is $N(1.0,\,2.0^2)$ and regime 2 (stress) is $N(-2.0,\,5.0^2)$, with

$$P=\begin{pmatrix}0.95&0.05\\0.20&0.80\end{pmatrix}.$$

The ergodic stress probability is $(1-0.95)/(2-0.95-0.80)=0.2$, so calm has 0.8. Mean durations are $1/0.05=20.0$ and $1/0.20=5.0$ months, and $\lambda=0.75$. The three fictional returns are $+1.0$, $-3.0$ and $-5.0$. Intermediate values are carried at full precision, so the last digit can differ from a hand calculation with the rounded figures.

- **Month 1**, prior $\xi_{1|0}=(0.8,0.2)$. Densities at $+1.0$: $f_1=0.199471$ and $f_2=0.066645$. Joint terms: $0.8\times0.199471=0.159577$ and $0.2\times0.066645=0.013329$, summing to 0.172906. Filtered stress is $0.013329/0.172906=0.0771$.
- **Month 2.** Predicted stress is $0.9229\times0.05+0.0771\times0.80=0.1078$. Densities at $-3.0$: 0.026995 and 0.078209. Joint terms: $0.8922\times0.026995=0.024085$ and $0.1078\times0.078209=0.008432$, summing to 0.032517. Filtered stress is 0.2593.
- **Month 3.** Predicted stress is $0.7407\times0.05+0.2593\times0.80=0.2445$. Densities at $-5.0$: 0.002216 and 0.066645. Joint terms: $0.7555\times0.002216=0.001674$ and $0.2445\times0.066645=0.016294$, summing to 0.017968. Filtered stress is 0.9068.

The log-likelihood is $\ln0.172906+\ln0.032517+\ln0.017968=-9.2002$.

**Smoothing.** Month 3's filtered law $(0.0932,\,0.9068)$ and predicted law $(0.7555,\,0.2445)$ give ratios $0.1233$ and $3.7091$. For month 2 the calm weight is $0.95\times0.1233+0.05\times3.7091=0.3026$ and the stress weight is $0.20\times0.1233+0.80\times3.7091=2.992$. Smoothed stress is $0.2593\times2.992=0.7759$. The same step for month 1 gives 0.4477.

**Reading the numbers.** Filtered stress climbs 0.0771, 0.2593, 0.9068, while smoothed stress is 0.4477, 0.7759, 0.9068. For month 1, hindsight puts stress at nearly six times the figure the desk could compute at the time. For month 3 the pre-return prediction was 0.2445 and the filtered value, which has seen the $-5.0$ return, is 0.9068: a risk limit applied to month 3's return can use only 0.2445. Three months ahead of month 3 the stress probability has relaxed to $0.2+0.75^3\,(0.9068-0.2)=0.4982$, still well above the ergodic 0.2.""",
        r"""**Break tests in practice.** statsmodels has no Chow or Quandt–Andrews command. Build the interaction columns yourself, fit `sm.OLS`, and call `f_test` on the $k$ interaction coefficients (or compare nested fits with `compare_f_test`). Fit with `cov_type='HAC'` (plus a `maxlags` choice in `cov_kwds`) when errors are heteroskedastic or autocorrelated, so that the test uses a robust covariance. A scan loops over the trimmed dates and keeps the maximum, which is then judged against Andrews's tables, Hansen's (1997) approximate p-values or a simulation, never the F table. The Brown–Durbin–Evans CUSUM is `RecursiveLS(y, X).fit()` with `.cusum`, `.cusum_squares` and `.plot_cusum()`, and `recursive_olsresiduals` returns the recursive residuals and the funnel. `breaks_cusumolsresid` is the OLS-residual variant, a different statistic. Report where the date came from (an external event or a search), the trimming, and the size of the shift with an interval, not only a p-value. After a confirmed break a pooled estimate averages two regimes (Lesson 3.21), so estimate after the break or model the break.

**Regime models in practice.** `MarkovRegression(y, k_regimes=2, trend='c', switching_variance=True).fit(search_reps=20)` estimates the means, variances and transition probabilities. The `search_reps` argument draws random starting values around the defaults and keeps the best, which matters because the likelihood has local maxima. The results object holds `predicted_marginal_probabilities`, `filtered_marginal_probabilities` and `smoothed_marginal_probabilities`, and `expected_durations` gives $1/(1-p_{ii})$. `regime_transition` is column-stochastic: entry $[i,j]$ is $\Pr(S_t=i\mid S_{t-1}=j)$, the transpose of this lesson's $P$. Calling `.filter(params)` or `.smooth(params)` on the model runs the recursions at fixed parameters and reproduces Part D (its default initial regime probabilities are the ergodic ones used here).

Checklist for a regime signal:
- Decide on predicted probabilities, refit on expanding windows, and expect regime labels to flip between refits.
- Check the ordering of $\sigma_j$, the durations and the occupancy. A regime lasting one or two months, or holding a handful of observations, is probably fitting outliers.
- Compare with a one-regime model and a GARCH benchmark out of sample (Lesson 3.15), and report how much the estimated $P$ moves.
- Treat regime probabilities as model output, not observed states. They depend on the assumed normal densities and on estimated parameters.""",
        'F=\\frac{(SSR_R-SSR_U)/k}{SSR_U/(n-2k)},\\qquad \\xi_{t|t}(j)=\\frac{f_j(y_t)\\,\\xi_{t|t-1}(j)}{\\sum_i f_i(y_t)\\,\\xi_{t|t-1}(i)}',
        r"""from math import exp, log, sqrt, pi

# Parts A to C: Chow test from the stated sums of squared residuals (percent squared),
# the scan range for a sup-F test, and the CUSUM funnel.
n = 120
k = 2
ssr_pooled = 583.0
ssr_first = 262.0
ssr_second = 278.0
ssr_split = ssr_first + ssr_second
m = n - 2 * k
chow = ((ssr_pooled - ssr_split) / k) / (ssr_split / m)
print("Split SSR:", ssr_split)
print("Chow numerator:", round((ssr_pooled - ssr_split) / k, 1))
print("Chow denominator:", round(ssr_split / m, 4))
print("Chow F:", round(chow, 3))
# With two numerator degrees of freedom the F tail has the closed form (1 + 2F/m) ** (-m/2).
print("Known-date p-value:", round(exp(-0.5 * m * log(1 + 2 * chow / m)), 4))
# Critical values are hard-coded. F(2,116) at 5% is a standard table value. The sup-F value
# (15% trimming, two tested coefficients, F scale = Wald statistic / 2) is approximate:
# a simulation of the Andrews (1993) limit law puts it at 5.8 to 5.9.
print("F(2,116) 5% critical value:", 3.074)
print("Sup-F 5% critical value:", 5.9)
print("First scanned month:", int(0.15 * n))
print("Last scanned month:", n - int(0.15 * n))
print("Variance ratio:", round((ssr_second / (n / 2 - k)) / (ssr_first / (n / 2 - k)), 3))
print("CUSUM bound at the last month:", round(0.948 * sqrt(n - k) * 3, 2))

# Part D: the Hamilton filter. Regime 1 is calm, regime 2 is stress.
mu1 = 1.0
sd1 = 2.0
mu2 = -2.0
sd2 = 5.0
p11 = 0.95
p22 = 0.80
returns = [1.0, -3.0, -5.0]

def dens(y, mu, sd):
    z = (y - mu) / sd
    return exp(-0.5 * z * z) / (sd * sqrt(2 * pi))

pi_calm = (1 - p22) / (2 - p11 - p22)
pi_stress = 1 - pi_calm
lam = p11 + p22 - 1
print("Ergodic stress probability:", round(pi_stress, 4))
print("Expected calm duration:", round(1 / (1 - p11), 1))
print("Expected stress duration:", round(1 / (1 - p22), 1))
print("Persistence eigenvalue:", round(lam, 2))

def hamilton(upto, show):
    # Runs the filter through month `upto`; returns
    # [filtered stress, log-likelihood, predicted stress for the next month].
    calm = pi_calm
    stress = pi_stress
    ll = 0.0
    post = 0.0
    for t in range(upto):
        y = returns[t]
        f1 = dens(y, mu1, sd1)
        f2 = dens(y, mu2, sd2)
        j1 = calm * f1
        j2 = stress * f2
        lik = j1 + j2
        post = j2 / lik
        ll += log(lik)
        if show == 1:
            print(f"Month {t + 1} predicted stress:", round(stress, 4))
            print(f"Month {t + 1} calm density:", round(f1, 6))
            print(f"Month {t + 1} stress density:", round(f2, 6))
            print(f"Month {t + 1} calm joint:", round(j1, 6))
            print(f"Month {t + 1} stress joint:", round(j2, 6))
            print(f"Month {t + 1} likelihood:", round(lik, 6))
            print(f"Month {t + 1} filtered stress:", round(post, 4))
        stress = (1 - post) * (1 - p11) + post * p22
        calm = 1 - stress
    return [post, ll, stress]

full = hamilton(3, 1)
print("Log-likelihood:", round(full[1], 4))

# Smoothing: backward from month 3, where smoothed and filtered probabilities coincide.
smooth = full[0]
for i in range(2):
    t = 2 - i
    here = hamilton(t, 0)
    stress_f = here[0]
    stress_pred = here[2]
    ratio_calm = (1 - smooth) / (1 - stress_pred)
    ratio_stress = smooth / stress_pred
    w_calm = p11 * ratio_calm + (1 - p11) * ratio_stress
    w_stress = (1 - p22) * ratio_calm + p22 * ratio_stress
    smooth = stress_f * w_stress
    if t == 2:
        print("Month 2 smoothing ratio calm:", round(ratio_calm, 4))
        print("Month 2 smoothing ratio stress:", round(ratio_stress, 4))
        print("Month 2 smoothing weight calm:", round(w_calm, 4))
        print("Month 2 smoothing weight stress:", round(w_stress, 4))
    print(f"Month {t} smoothed stress:", round(smooth, 4))

ahead = pi_stress + lam ** 3 * (full[0] - pi_stress)
print("Stress probability three months ahead:", round(ahead, 4))""",
        'Variant desk. (a) A Chow test on n = 80 months (k = 2) has pooled SSR 410.0 and segment SSRs 150.0 and 190.0, with 40 months in each segment. Compute F, its p-value from the closed form (1 + 2F/m)^(−m/2) with m = n − 2k, and the ratio of the segment residual variances. Then say whether the rejection survives if the date was the best of a trimmed scan with a 5% sup-F value of about 5.9. (b) A two-state filter has calm N(1.0, 2.0²), stress N(−2.0, 5.0²), p11 = 0.90 and p22 = 0.70. It starts from its ergodic probabilities and sees returns −1.0 and −5.0. Compute the filtered stress probability after each month, the prediction for month 2 made before its return, and the smoothed stress probability for month 1. (c) At the start of month 2, which of these numbers may a risk limit for that month use, and why?',
        "(a) SSR_U = 150.0 + 190.0 = 340.0, so F = ((410.0 − 340.0)/2)/(340.0/76) = 35.0/4.4737 = 7.82 and p = (1 + 2 × 7.82/76)^(−38) = 0.0008. The segment variances are 150.0/38 and 190.0/38, a ratio of 1.27, so the equal-variance condition is not contradicted. Because 7.82 exceeds 5.9, the rejection survives a date scan, although its p-value would then come from the sup-F law rather than the F table. (b) The ergodic stress probability is (1 − 0.90)/(2 − 0.90 − 0.70) = 0.25. Month 1: the densities at −1.0 are 0.120985 and 0.078209, the joint terms 0.75 × 0.120985 = 0.090739 and 0.25 × 0.078209 = 0.019552 sum to 0.110291, and filtered stress is 0.019552/0.110291 = 0.1773. The month-2 prediction is 0.8227 × 0.10 + 0.1773 × 0.70 = 0.2064. Month 2: the densities at −5.0 are 0.002216 and 0.066645, the joint terms are 0.001759 and 0.013753 (sum 0.015512), and filtered stress is 0.8866. Smoothing month 1: the ratios of the filtered to the predicted month-2 probabilities are 0.1429 and 4.2964, the weights are 0.90 × 0.1429 + 0.10 × 4.2964 = 0.5582 and 0.30 × 0.1429 + 0.70 × 4.2964 = 3.0503, and smoothed stress for month 1 is 0.1773 × 3.0503 = 0.5408 against a filtered 0.1773. (c) Only the prediction 0.2064 exists before month 2's return. The filtered 0.8866 contains the −5.0 return itself, and the smoothed 0.5408 uses it too, so a rule built on either would be using the future.",
        [
            (
                'A desk computes the Chow F statistic for every candidate break date between 15% and 85% of the sample, takes the largest, and compares it with the ordinary F(k, n − 2k) 5% critical value. Under no break, the rejection rate of this procedure is:',
                ['Exactly 5%', 'Well above 5%', 'Below 5%, because trimming removes extreme dates'],
                1,
                "Each F at a single date has the F(k, n − 2k) law, but the maximum of about 0.7n strongly overlapping statistics is stochastically larger. For k = 2 a simulation of the limit rejects about 43% of the time at the single-date value of 3.0, so Andrews's sup-F critical value (about 5.9 here) is needed.",
            ),
            (
                'With n = 100 months and k = 2, the pooled regression has SSR 300 and the regressions on the two halves have SSR 100 and 150. The Chow F statistic is closest to:',
                ['0.20', '19.2', '9.60'],
                2,
                'SSR_U = 100 + 150 = 250, so F = ((300 − 250)/2)/(250/(100 − 4)) = 25/2.604 = 9.60. Forgetting the degrees of freedom gives 50/250 = 0.20, and skipping the division by k gives 19.2.',
            ),
            (
                "In a two-state model with p11 = 0.90 and p22 = 0.60, the filtered probability of regime 2 at the end of month t is 0.30. Before month t + 1's return is seen, the predicted probability of regime 2 is:",
                ['0.25', '0.30', '0.60'],
                0,
                "Predict: 0.70 × (1 − 0.90) + 0.30 × 0.60 = 0.07 + 0.18 = 0.25. Reusing the filtered 0.30 ignores the transition matrix, and 0.60 is only the regime's own persistence.",
            ),
            (
                'A backtest moves to cash whenever the smoothed probability of the stress regime exceeds 0.5, using parameters estimated on the full sample. Its results cannot be reproduced in real time because:',
                ['Markov-switching models cannot assign monthly regime probabilities at all', 'Smoothed probabilities are always below the filtered probabilities in stress', 'Smoothed probabilities at date t use later returns, and full-sample parameters leak too'],
                2,
                "The backward smoother conditions on returns after t, so the signal was not available at t. Parameters estimated on the whole sample leak later data too, and even a filtered probability contains the month's own return, so an unbiased test needs predicted probabilities and expanding-window re-estimation.",
            ),
        ],
        [('statsmodels contributors · MarkovRegression', 'https://www.statsmodels.org/stable/generated/statsmodels.tsa.regime_switching.markov_regression.MarkovRegression.html'), ('Chow (1960) · Tests of Equality Between Sets of Coefficients in Two Linear Regressions', 'https://doi.org/10.2307/1910133'), ('Andrews (1993) · Tests for Parameter Instability and Structural Change With Unknown Change Point', 'https://doi.org/10.2307/2951764'), ('Hamilton (1989) · A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle', 'https://doi.org/10.2307/1912559')],
    ),
    (
        '3.38',
        9,
        'State-space models and the Kalman filter: a time-varying beta',
        'Write a time-varying beta as a state-space model, run the Kalman filter by hand, and explain how the signal-to-noise ratio sets the adaptation speed.',
        r"""Lesson 3.21 tracked changing exposure by re-running OLS on a rolling window. That treats beta as constant inside the window and irrelevant outside it, and the window length is a free choice. A **state-space model** gives beta an explicit law of motion, and the **Kalman filter** turns that law into a recursive estimate of today's beta together with its uncertainty.

**The model.** For a fund return $r_t$ and an observed factor return $f_t$, the measurement and transition equations are

$$r_t=\beta_tf_t+\varepsilon_t,\quad\varepsilon_t\sim N(0,\sigma_\varepsilon^2);\qquad\beta_t=\beta_{t-1}+\eta_t,\quad\eta_t\sim N(0,\sigma_\eta^2).$$

The state $\beta_t$ is unobserved, and $\varepsilon_t$ and $\eta_t$ are independent over time and of each other. In the general form $y_t=Z_t\alpha_t+\varepsilon_t$, $\alpha_t=\Phi\alpha_{t-1}+\eta_t$, the factor is a known, date-varying design coefficient $Z_t=f_t$ and $\Phi=1$. With an intercept the state is $(\alpha_t,\beta_t)'$ and $Z_t=(1,f_t)$. The prior for the first state is $\beta_1\sim N(b_{1|0},P_{1|0})$. Setting $\sigma_\eta^2=0$ gives a constant beta (recursive least squares), while a large $\sigma_\eta^2$ lets beta chase each month's data.

**The recursions.** Write $b_{t|s}$ and $P_{t|s}$ for the mean and variance of $\beta_t$ given returns through month $s$. Month $t$ updates and then predicts:

$$v_t=r_t-f_tb_{t|t-1},\qquad F_t=f_t^2P_{t|t-1}+\sigma_\varepsilon^2,\qquad K_t=\frac{P_{t|t-1}f_t}{F_t},$$

$$b_{t|t}=b_{t|t-1}+K_tv_t,\qquad P_{t|t}=(1-K_tf_t)P_{t|t-1},\qquad b_{t+1|t}=b_{t|t},\qquad P_{t+1|t}=P_{t|t}+\sigma_\eta^2.$$

The innovation $v_t$ is the one-step-ahead forecast error and $F_t$ is its variance. With an $m$-dimensional random-walk state ($\Phi=I$) the steps keep their shape in matrix form:

$$F_t=Z_tP_{t|t-1}Z_t'+\sigma_\varepsilon^2,\qquad K_t=P_{t|t-1}Z_t'F_t^{-1},\qquad b_{t|t}=b_{t|t-1}+K_tv_t,$$

$$P_{t|t}=P_{t|t-1}-K_tF_tK_t',\qquad P_{t+1|t}=P_{t|t}+Q.$$

To derive the update, note that given the past, $(\beta_t,r_t)$ is jointly normal with $\operatorname{Cov}(\beta_t,r_t)=P_{t|t-1}f_t$ and $\operatorname{Var}(r_t)=F_t$. The normal conditional-mean formula gives $b_{t|t}=b_{t|t-1}+(\operatorname{Cov}/\operatorname{Var})\,v_t$, and the variance falls by $\operatorname{Cov}^2/\operatorname{Var}$. Without normality the same recursion gives the best linear estimator (Kalman 1960). Because $v_t=f_t\,(r_t/f_t-b_{t|t-1})$, the update is a precision-weighted average of the old estimate and the month's implied beta $r_t/f_t$, with weights $1/P_{t|t-1}$ and $f_t^2/\sigma_\varepsilon^2$. A month with $f_t\approx0$ carries almost no information, so only the variance grows. The gain is negative when $f_t<0$, but $K_tv_t$ still moves beta toward $r_t/f_t$.

**Signal-to-noise and adaptation speed.** Adaptation depends on how far beta can drift relative to the noise in a month's return: $\lambda=\sigma_\eta^2\,\overline{f^2}/\sigma_\varepsilon^2$, where $\overline{f^2}$ is the mean squared factor return. This ratio is unit-free, unlike $\sigma_\eta^2/\sigma_\varepsilon^2$ alone, so rescaling returns from decimals to percent leaves it unchanged (compare the unit warning in Lesson 3.18). For a factor of constant size, let $p=f^2P_{t|t-1}/\sigma_\varepsilon^2$. The predicted variance settles where $p=p/(1+p)+\lambda$, so

$$p^2-\lambda p-\lambda=0,\qquad w=K_tf_t=\frac{p}{1+p},$$

and $w$ is the share of each month's surprise that beta absorbs. The filter then weights data $j$ months old by $w(1-w)^j$. A rolling window of $M$ months matches this weighting in mean age and in variance when $w=2/(M+1)$, which is $\lambda=4/(M^2-1)$. A larger $\lambda$ gives a faster but noisier beta, and a smaller one gives a smooth beta that lags real changes. As $\lambda\to0$ with a diffuse prior the filter becomes expanding-window OLS, and as $\lambda$ grows it simply reports $r_t/f_t$. The match to a window is a steady-state approximation that assumes the factor's size is constant.

**Estimating the variances.** Given the past, the innovations are independent with $v_t\sim N(0,F_t)$, so the joint density of the returns factorizes into $\prod_tN(r_t;\,f_tb_{t|t-1},F_t)$. This prediction-error decomposition gives

$$\ln L(\theta)=-\frac12\sum_{t=1}^{T}\Big[\ln(2\pi F_t)+\frac{v_t^2}{F_t}\Big],\qquad\theta=(\sigma_\varepsilon^2,\sigma_\eta^2).$$

Each trial $\theta$ needs one pass of the filter, and a numerical optimizer does the rest. It is the likelihood of Lesson 3.33 with the filter supplying the factorization.

**Filtering versus smoothing.** $b_{t|t}$ uses returns through month $t$. The fixed-interval smoother (Rauch, Tung and Striebel 1965) runs backward from $T$ with $J_t=P_{t|t}/P_{t+1|t}$:

$$b_{t|T}=b_{t|t}+J_t\,(b_{t+1|T}-b_{t+1|t}),\qquad P_{t|T}=P_{t|t}+J_t^2\,(P_{t+1|T}-P_{t+1|t}).$$

Smoothed betas are the best description of history, but they use future returns, so they must never drive a backtest decision. As in Lesson 3.37, look-ahead has three layers. Smoothed betas use later returns. $b_{t|t}$ already contains month $t$'s own return, so a hedge applied to month $t$ may use only $b_{t|t-1}$. And variances estimated on the full sample leak the future, so a backtest must re-estimate on expanding windows.

**Against rolling OLS (Lesson 3.21).** A rolling regression weights the last $M$ months equally and older months at zero, so an extreme month leaving the window moves the estimate abruptly. It has no model of drift, and $M$ is chosen by hand. The filter's weights decay smoothly, every estimate carries a variance $P_{t|t}$, the drift variance can be estimated by likelihood, and several factors fit in the same framework. Its costs are that a random-walk beta can wander without bound, that $\sigma_\eta^2$ is hard to estimate in short samples, and that Gaussian errors let one outlier move beta.""",
        r"""The Cedar Capital desk filters the market beta of a fictional fund over five months, in percent units. The prior for month 1 is $\beta_1\sim N(0.80,\,0.0625)$, a mandate beta near 0.8 with standard deviation 0.25. The noise variances are $\sigma_\varepsilon^2=1.0$ and $\sigma_\eta^2=0.01$. Factor returns are $f=(2.0,-3.0,4.0,1.5,-2.5)$ and fund returns are $r=(2.2,-3.5,5.3,2.1,-3.7)$. Figures are carried at full precision and shown to four decimals, so a hand calculation with rounded values can differ in the last digit.

- **Month 1.** $P_{1|0}=0.0625$, so $F_1=4(0.0625)+1=1.25$ and $K_1=0.0625\times2/1.25=0.1$. The predicted return is $0.80\times2.0=1.6$, so $v_1=2.2-1.6=0.6$. Then $b_{1|1}=0.80+0.1\times0.6=0.86$ and $P_{1|1}=0.0625/1.25=0.05$.
- **Month 2.** $P_{2|1}=0.05+0.01=0.06$, $F_2=9(0.06)+1=1.54$, $K_2=0.06\times(-3)/1.54=-0.1169$ and $v_2=-3.5-(-3)(0.86)=-0.92$. Then $b_{2|2}=0.86+(-0.1169)(-0.92)=0.9675$ and $P_{2|2}=0.06/1.54=0.039$.
- **Month 3.** $P_{3|2}=0.049$, $F_3=1.7834$, $K_3=0.1098$, $v_3=5.3-4(0.9675)=1.4299$, $b_{3|3}=1.1246$ and $P_{3|3}=0.0275$.
- **Month 4.** $P_{4|3}=0.0375$, $F_4=1.0843$, $K_4=0.0518$, $v_4=0.4132$, $b_{4|4}=1.146$ and $P_{4|4}=0.0345$.
- **Month 5.** $P_{5|4}=0.0445$, $F_5=1.2784$, $K_5=-0.0871$, $v_5=-0.8351$, $b_{5|5}=1.2187$ and $P_{5|5}=0.0348$.

The filtered beta climbs from the 0.8 prior through 0.86, 0.9675, 1.1246 and 1.146 to 1.2187, with a standard deviation of 0.1867 at month 5. Months 2 and 5 have negative factor returns, so their gains are negative, yet the product $K_tv_t$ still moves beta toward $r_t/f_t$. The innovation is also the result of a hedge: hedging month 5 with the beta known at its start, $b_{5|4}=1.146$, leaves $r_5-b_{5|4}f_5=-0.8351$.

**Against rolling OLS.** A three-month rolling regression at month 5 uses months 3 to 5 only: $\sum fr=33.6$, $\sum f^2=24.5$, so the beta is $1.3714$. The full-sample OLS beta is $48.5/37.5=1.2933$. The filter's 1.2187 blends the prior and all five months with fading weights and comes with an error bar, whereas the rolling estimate rests on three points.

**Smoothing.** One backward step uses $J_4=P_{4|4}/P_{5|4}=0.7755$ (computed from unrounded variances), giving $b_{4|5}=1.146+0.7755\times(1.2187-1.146)=1.2024$. Running back gives smoothed betas 1.0916, 1.1379, 1.1816 and 1.2024 for months 1 to 4, and month 5 keeps 1.2187. Month 1's smoothed beta exceeds its filtered 0.86 by 0.2316 because it has seen the four later months.

**Likelihood.** Month 1 contributes $-\tfrac12[\ln(2\pi\times1.25)+0.6^2/1.25]=-1.1745$, and the five terms sum to $-6.7182$. On a grid, $\sigma_\eta^2=0,\,0.01,\,0.02,\,0.05,\,0.1$ gives log-likelihoods $-6.8396$, $-6.7182$, $-6.672$, $-6.7076$ and $-6.9177$. The grid maximum is at 0.02, but the whole range spans less than 0.25 log-points: five months cannot identify the drift variance. In our own statsmodels run, unconstrained maximum likelihood over both variances drove $\sigma_\varepsilon^2$ to essentially zero, a degenerate fit that takes every month's $r_t/f_t$ as the exact beta. That is why a desk needs years of data or a fixed $\sigma_\varepsilon^2$.

**Adaptation speed.** The mean squared factor return is 7.5, so $\lambda=0.01\times7.5/1.0=0.075$. The steady-state weight is $w=0.2389$, about a quarter of each month's surprise, and the equivalent rolling window is $2/w-1=7.37$ months. Lesson 3.21's 36-month window corresponds to $\lambda=4/(36^2-1)=0.0031$, far smaller. The example is deliberately fast so that five months show visible movement.""",
        r"""**In statsmodels.** For a time-varying slope on an observed factor, subclass `statsmodels.tsa.statespace.mlemodel.MLEModel` with `k_states=1`. Set `self.ssm['design']` to the factor with shape `(1, 1, nobs)` and `transition` and `selection` to 1. Inside `update`, write the two variances into `obs_cov` and `state_cov`, and let `transform_params` square a free parameter so the variances stay positive. The prior of this lesson is `initialization='known'` with `initial_state=[0.8]` and `initial_state_cov=[[0.0625]]`: statsmodels takes it as the law of the first state before month 1, so the CASE starts from $P_{1|0}$. Calling `.smooth(params)` with the CASE variances reproduces the CASE, and `.fit()` maximizes the prediction-error likelihood. The results hold `filtered_state` ($b_{t|t}$), `filtered_state_cov`, `smoothed_state`, `forecasts_error` ($v_t$) and `standardized_forecasts_error`. `UnobservedComponents(y, 'local level')` covers only the special case $f_t=1$, a time-varying mean; its regression coefficients on `exog` are constants. `RollingOLS` from `statsmodels.regression.rolling` and `RecursiveLS` give the comparisons with Lesson 3.21.

**Diagnostics and failure modes.**
- Standardized innovations $v_t/\sqrt{F_t}$ should look iid $N(0,1)$. Test their autocorrelation with Ljung–Box, and do the same for their squares. Volatility clustering makes $F_t$ too small, and a GARCH or stochastic-volatility error term (Lesson 3.18) addresses it.
- The maximum likelihood estimate of $\sigma_\eta^2$ often piles up at zero in short samples (Shephard and Harvey 1990), which returns a constant beta even when beta drifts. Because $\sigma_\eta^2=0$ is a boundary and the state is nonstationary, likelihood-ratio statistics are not $\chi^2$. Use the stability test of Nyblom (1989), the median-unbiased estimator of Stock and Watson (1998) or a simulation, and profile the likelihood over a grid as in the CASE.
- Initialize from data before the evaluation period. A prior taken from full-sample OLS leaks the future. A diffuse prior ($P_{1|0}\to\infty$) makes the first update set $b_{1|1}=r_1/f_1$ with variance $\sigma_\varepsilon^2/f_1^2$, which is very noisy when $f_1$ is small, so drop the burn-in months from the likelihood and from any evaluation.
- With several factors, collinearity lets the states trade off against each other. Restrict the state covariance to be diagonal and check that the filtered betas stay economically sensible.
- For a bounded beta use a mean-reverting transition, $\beta_t=\mu+\phi(\beta_{t-1}-\mu)+\eta_t$.
- Report filtered betas with a $\pm2\sqrt{P_{t|t}}$ band, remembering that it treats the estimated variances as known and so understates uncertainty, and label smoothed betas as history, not as signals.""",
        'K_t=\\frac{P_{t|t-1}f_t}{f_t^2P_{t|t-1}+\\sigma_\\varepsilon^2},\\qquad b_{t|t}=b_{t|t-1}+K_t\\,(r_t-f_tb_{t|t-1})',
        r"""from math import sqrt, log, pi

f = [2.0, -3.0, 4.0, 1.5, -2.5]     # factor returns, percent
r = [2.2, -3.5, 5.3, 2.1, -3.7]     # fund returns, percent
b0 = 0.80       # prior mean of beta in month 1
p0 = 0.0625     # prior variance of beta in month 1
se2 = 1.0       # measurement noise variance
sn2 = 0.01      # state (drift) noise variance

def kalman(sn, upto, show):
    # Update-then-predict for months 1..upto. Returns
    # [log-likelihood, filtered beta, filtered variance] after month `upto`.
    b = b0
    p = p0
    ll = 0.0
    post_b = b0
    post_p = p0
    for t in range(upto):
        ft = f[t]
        fv = ft * ft * p + se2
        gain = p * ft / fv
        v = r[t] - ft * b
        post_b = b + gain * v
        post_p = p * se2 / fv
        term = -0.5 * (log(2 * pi * fv) + v * v / fv)
        ll += term
        if show == 1:
            print(f"Month {t + 1} predicted variance:", round(p, 4))
            print(f"Month {t + 1} forecast variance:", round(fv, 4))
            print(f"Month {t + 1} gain:", round(gain, 4))
            print(f"Month {t + 1} innovation:", round(v, 4))
            print(f"Month {t + 1} filtered beta:", round(post_b, 4))
            print(f"Month {t + 1} filtered variance:", round(post_p, 4))
            if t == 0:
                print("Month 1 predicted return:", round(ft * b, 4))
                print("Month 1 log-likelihood term:", round(term, 4))
        b = post_b
        p = post_p + sn
    return [ll, post_b, post_p]

full = kalman(sn2, 5, 1)
print("Log-likelihood:", round(full[0], 4))
print("Filtered standard deviation, month 5:", round(sqrt(full[2]), 4))

# Rolling (last three months) and full-sample OLS on the same five months.
num3 = 0.0
den3 = 0.0
num5 = 0.0
den5 = 0.0
for t in range(5):
    num5 += f[t] * r[t]
    den5 += f[t] * f[t]
    if t >= 2:
        num3 += f[t] * r[t]
        den3 += f[t] * f[t]
print("Rolling cross-product:", round(num3, 2))
print("Rolling sum of squares:", round(den3, 2))
print("Rolling OLS beta:", round(num3 / den3, 4))
print("Full-sample cross-product:", round(num5, 2))
print("Full-sample sum of squares:", round(den5, 2))
print("Full-sample OLS beta:", round(num5 / den5, 4))

# Smoothing backward from month 5 (random-walk transition, so b(t+1|t) = b(t|t)).
smooth_b = full[1]
for i in range(4):
    t = 4 - i
    flt = kalman(sn2, t, 0)
    j = flt[2] / (flt[2] + sn2)
    smooth_b = flt[1] + j * (smooth_b - flt[1])
    if t == 4:
        print("Smoothing gain, month 4:", round(j, 4))
    print(f"Smoothed beta, month {t}:", round(smooth_b, 4))
first = kalman(sn2, 1, 0)
print("Month 1 smoothed minus filtered:", round(smooth_b - first[1], 4))

# Prediction-error likelihood on a grid of state variances.
for q in [0.0, 0.01, 0.02, 0.05, 0.1]:
    res = kalman(q, 5, 0)
    print(f"Log-likelihood at state variance {q}:", round(res[0], 4))

# Signal-to-noise ratio and the steady-state weight for a factor of constant size.
sum_f2 = 0.0
for t in range(5):
    sum_f2 += f[t] * f[t]
lam = sn2 * (sum_f2 / 5) / se2
pp = (lam + sqrt(lam * lam + 4 * lam)) / 2
w = pp / (1 + pp)
print("Mean squared factor return:", round(sum_f2 / 5, 2))
print("Signal-to-noise ratio:", round(lam, 3))
print("Steady-state weight:", round(w, 4))
print("Equivalent window in months:", round(2 / w - 1, 2))
print("Signal-to-noise ratio of a 36-month window:", round(4 / (36 * 36 - 1), 4))""",
        'Variant desk. The prior for month 1 is beta ~ N(1.00, 0.09), the noise variances are 1.0 (measurement) and 0.04 (drift), the factor returns are 3.0 and −2.0, and the fund returns are 2.4 and −2.6, all in percent. (a) Filter both months by hand: for each month give the forecast variance, gain, innovation, filtered beta and filtered variance. (b) Compute the smoothed month-1 beta from the backward step with J = P(1|1)/P(2|1). (c) Which of three values (the prior mean, the filtered month-1 beta, the smoothed month-1 beta) may set the hedge for month 1, and which for month 2? Explain.',
        "Figures are carried at full precision. (a) Month 1: P(1|0) = 0.09, F = 9 × 0.09 + 1 = 1.81, K = 0.09 × 3/1.81 = 0.1492, innovation = 2.4 − 3.0 × 1.00 = −0.6, so beta = 1.00 + 0.1492 × (−0.6) = 0.9105 and P(1|1) = 0.09/1.81 = 0.0497. Month 2: P(2|1) = 0.0497 + 0.04 = 0.0897, F = 4 × 0.0897 + 1 = 1.3589, K = 0.0897 × (−2)/1.3589 = −0.1321, innovation = −2.6 − (−2.0)(0.9105) = −0.7790, so beta = 0.9105 + (−0.1321)(−0.7790) = 1.0134 and P(2|2) = 0.0897/1.3589 = 0.0660. (b) J = 0.0497/0.0897 = 0.5542 and the smoothed month-1 beta is 0.9105 + 0.5542 × (1.0134 − 0.9105) = 0.9675, which is 0.0570 above the filtered value. (c) A hedge applied to month 1 can use only the prior mean 1.00, because even the filtered 0.9105 contains month 1's own return. The hedge for month 2 can use the filtered 0.9105, which equals the prediction for month 2. The smoothed 0.9675 uses month 2's return, so a hedge built on it would be using the future.",
        [
            (
                'In a time-varying beta model a month has factor return f = 3, prior variance P = 0.04 for the beta, and measurement variance 1.0. The Kalman gain K = P f / (f² P + 1.0) is closest to:',
                ['0.120', '0.088', '0.333'],
                1,
                'The forecast variance is F = 9 × 0.04 + 1.0 = 1.36, so K = 0.04 × 3/1.36 = 0.0882. The value 0.120 is the numerator alone, and 0.333 = 1/f would hold only if measurement noise were zero.',
            ),
            (
                'Holding the measurement variance fixed, raising the drift variance of a random-walk beta makes the filtered beta:',
                ['Slower to adapt, with a narrower error band', 'Identical to the full-sample OLS beta', 'Faster to adapt, since the gain is larger'],
                2,
                'A larger drift variance raises the predicted variance P(t|t−1) each month, which raises the gain K and the weight on the newest return. The estimate follows recent data more closely and is noisier. Only a drift variance of zero with a diffuse prior reproduces expanding-window OLS.',
            ),
            (
                "One month's term in the prediction-error log-likelihood is −½[ln(2πF) + v²/F]. With forecast variance F = 2 and innovation v = 1, the term is closest to:",
                ['−1.52', '−3.03', '−0.25'],
                0,
                'ln(2π × 2) = ln(12.566) = 2.531 and v²/F = 0.5, so the term is −½ × (2.531 + 0.5) = −1.5155. Forgetting the factor ½ gives −3.03, and keeping only the squared-error part gives −0.25.',
            ),
            (
                'A desk hedges month t using a Kalman-filtered beta. Which estimate is available when the hedge for month t must be set, without look-ahead?',
                ['The predicted beta b(t|t−1), built from returns before month t', 'The filtered beta b(t|t), because it is a real-time estimate', 'The smoothed beta b(t|T), because it has the smallest variance'],
                0,
                "Month t's own return enters b(t|t), and b(t|T) also uses every later return. Only b(t|t−1), which equals b(t−1|t−1) for a random walk, is known at the start of month t. The smoothed beta has the smallest variance because it uses the future.",
            ),
        ],
        [('statsmodels contributors · Time series analysis by state space methods', 'https://www.statsmodels.org/stable/statespace.html'), ('statsmodels contributors · UnobservedComponents', 'https://www.statsmodels.org/stable/generated/statsmodels.tsa.statespace.structural.UnobservedComponents.html'), ('Kalman (1960) · A New Approach to Linear Filtering and Prediction Problems', 'https://doi.org/10.1115/1.3662552'), ('Durbin & Koopman (2012) · Time Series Analysis by State Space Methods', 'https://doi.org/10.1093/acprof:oso/9780199641178.001.0001')],
    ),
    (
        '3.39',
        9,
        'Quantile regression and conditional value at risk',
        'Estimate a conditional return quantile by minimizing the check loss, read its slopes as tail effects, and score the resulting VaR forecast on later data.',
        r"""Lesson 3.4 treated value at risk as an unconditional quantile of the loss, and Lesson 3.18 made risk time-varying through a variance recursion. Quantile regression models what a risk limit actually needs: the quantile of tomorrow's return given what is known today, with no model for the rest of the distribution. "Conditional" here means conditional on information at $t-1$. It does not mean the expected-shortfall average that some texts, and the shorthand in Lesson 3.4, also call conditional VaR.

**Model and sign convention.** Let $x_{t-1}$ be known at $t-1$, for example $(1,\hat\sigma_{t-1})'$ with $\hat\sigma_{t-1}$ a volatility forecast. The model is
$$Q_\tau(r_t\mid\mathcal F_{t-1})=x_{t-1}'\beta(\tau),\qquad P\big(r_t\le x_{t-1}'\beta(\tau)\mid\mathcal F_{t-1}\big)=\tau.$$
Losses are positive, so the VaR at confidence $1-\tau$ is $\mathrm{VaR}_t=-x_{t-1}'\beta(\tau)$. Each $\tau$ is a separate regression and no distribution is assumed.

**The check loss.** Define $\rho_\tau(u)=u\,(\tau-\mathbf 1\{u<0\})$: weight $\tau$ per unit of positive residual and $1-\tau$ per unit of negative residual. For a random variable $Y$ with distribution function $F$,
$$\frac{d}{dq}\,\mathrm E\,\rho_\tau(Y-q)=F(q)-\tau.$$
Raising $q$ saves $\tau$ on every outcome above it and costs $1-\tau$ on every outcome below it. The derivative is negative below the $\tau$-quantile and positive above, so the minimizer solves $F(q)=\tau$. In a sample, minimizing $\sum_t\rho_\tau(r_t-q)$ returns the $\lceil n\tau\rceil$-th smallest observation when $n\tau$ is not an integer. Koenker and Bassett (1978) extended this to
$$\hat\beta(\tau)=\arg\min_{b}\sum_t\rho_\tau\big(r_t-x_{t-1}'b\big).$$

**The linear program.** Write each residual as $u_t^+-u_t^-$ with both parts nonnegative. Minimizing $\tau\,\mathbf 1'u^++(1-\tau)\,\mathbf 1'u^-$ subject to $r=Xb+u^+-u^-$ is a linear program, so an optimum sits at a vertex where $p$ residuals are exactly zero: a fitted line passes through two observations. Two facts follow. First, with an intercept, the numbers of observations strictly below the fit ($N_-$) and exactly on it ($N_0$) satisfy $N_-\le n\tau\le N_-+N_0$, so the in-sample hit rate is close to $\tau$ by construction and says nothing about calibration. Second, when $n\tau$ is small, a handful of days pin the line.

**Reading slopes.** $\beta_j(\tau)=\partial Q_\tau(r_t\mid x)/\partial x_j$ is the shift in the conditional $\tau$-quantile per unit of $x_j$. It is not the effect on one particular day's return. If $r_t=\mu+(\delta+\lambda x_{t-1})\varepsilon_t$ with $\varepsilon_t$ independent of $x$ and $\delta+\lambda x_{t-1}>0$, then $Q_\tau=\mu+\delta q_\tau+\lambda q_\tau x_{t-1}$ with $q_\tau=F_\varepsilon^{-1}(\tau)$: slopes differ across $\tau$ when the regressor changes the scale and not only the location. The rule "VaR is 1.2816 times forecast volatility" is the special case $q_{0.10}=-1.2816$ with no intercept; quantile regression lets the data choose both numbers. Quantiles also commute with increasing transformations, so a quantile fitted to log returns and exponentiated is a quantile of the gross return.

**Quantile crossing.** Each $\tau$ is fitted separately, so nothing forces $x'\hat\beta(\tau_1)\le x'\hat\beta(\tau_2)$ for $\tau_1<\tau_2$. Lines with different slopes cross somewhere, and a forecast beyond the crossing describes an impossible distribution. Keep forecasts inside the range of $x$ used for fitting, change the specification, or sort the fitted quantiles at each $x$ (monotone rearrangement; Chernozhukov, Fernández-Val and Galichon 2010).

**Inference.** If the quantile is correctly specified given $\mathcal F_{t-1}$, the score $x_{t-1}(\tau-\mathbf 1\{r_t<x_{t-1}'\beta\})$ is a martingale difference and
$$\sqrt T\big(\hat\beta-\beta\big)\ \xrightarrow{d}\ N\!\big(0,\ \tau(1-\tau)\,H^{-1}JH^{-1}\big),$$
where $J=\mathrm E[xx']$, $H=\mathrm E[f_t(q_t)\,xx']$ and $f_t(q_t)$ is the conditional density of $r_t$ at its own quantile. That density is hardest to estimate in the tail. For one unconditional quantile the variance reduces to $\tau(1-\tau)/(n f(q)^2)$. A pairs bootstrap resamples $(r_t,x_{t-1})$ rows together, and with serially dependent data it should resample blocks (Lesson 3.27). Either way the effective sample is the $n\tau$ observations in the tail.

**CAViaR.** Engle and Manganelli (published 2004) model the quantile's own dynamics instead of tying it to an outside regressor. On the positive VaR scale the symmetric absolute value form is
$$\mathrm{VaR}_t=\beta_0+\beta_1\mathrm{VaR}_{t-1}+\beta_2|r_{t-1}|,$$
with $0<\beta_1<1$ giving persistence. (On the return-quantile scale the intercept and the $|r|$ coefficient change sign.) Because $\mathrm{VaR}_{t-1}$ depends on the parameters, the pinball objective is non-smooth and not convex, so it is minimized numerically from several starting values.

**Evaluation.** Call a forecast breached when $r_t<\hat q_t$, strictly. A calibrated forecast has Bernoulli$(\tau)$ hits given the past, so a count over $T$ days has mean $T\tau$ and variance $T\tau(1-\tau)$. A hit rate checks calibration but not sharpness, since a forecast that always sits far out in the tail is rarely breached. The average pinball loss $T^{-1}\sum_t\rho_\tau(r_t-\hat q_t)$ scores both. Gneiting (2011) showed that it is a consistent score for quantiles, whereas expected shortfall has no consistent score of its own (Lesson 3.19). Compute both on days not used for fitting. The Kupiec and Christoffersen tests of coverage and independence are the subject of Lesson 2.40 in the Quantitative Investment Analysis course.""",
        r"""Cedar Capital's desk keeps eleven days of prior-evening volatility forecast $x$ and next-day return $r$, both in percent, sorted by $x$:

- $x$: 0.8, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.4, 2.7, 3.1
- $r$: −0.9, −0.5, 0.0, −0.3, 0.7, −2.6, 0.1, 1.0, −0.8, −4.1, −0.1

The desk wants a 90% VaR, so $\tau=0.10$ and $n\tau=1.1$. At $\tau=0.05$ the product would be 0.55, which forces the fitted line to lie on or below every observation and teaches nothing.

**1. Check loss.** At $\tau=0.10$ a return 2 points below its quantile ($u=-2$) costs $-2\times(0.10-1)=1.8$, and one 2 points above ($u=+2$) costs $2\times0.10=0.2$. A breach costs nine times more per point, because a breach is meant to be nine times rarer than a non-breach.

**2. Constant line.** Over constants the minimizer is the $\lceil 1.1\rceil=2$nd smallest return, $-2.6$. Its mean pinball loss is 0.3282, and one day (the $-4.1$) falls below it.

**3. Normal rule.** The line $q=-1.2816\,x$ has mean pinball loss 0.2555 and two days below it.

**4. Fitted line.** The optimum of the linear program lies on a line through two days, so try all $\binom{11}{2}=55$ such lines and keep the lowest loss. The winner passes through the days at $x=0.8$ and $x=2.7$:
$$\hat q_{0.10}(x)=0.4474-1.6842\,x,\qquad \text{mean pinball loss }0.2024.$$
One day (the $-2.6$ at $x=1.7$) lies below it, consistent with $N_-\le n\tau\le N_-+N_0$, that is $1\le1.1\le3$. Each extra point of forecast volatility moves the 10% quantile of next-day return down by 1.68 points. This line beats the other two in sample because it minimizes the loss over all lines, including them, so the eleven days cannot show that conditioning helps.

**5. Weak identification.** The runner-up line through $x=1.7$ and $x=2.7$ has slope $-1.5$ and intercept $-0.05$. Its mean pinball loss is 0.2027 against 0.2024. A different slope fits the data almost as well, because about one observation determines the tail.

**6. Other quantiles and crossing.** The same search gives slope 0.1111 at the median and 0.5 at the 90th percentile. Volatility pushes the lower tail down by 1.68 points per unit but the upper tail up by only 0.5. The median line is $-0.4444+0.1111x$, so the 10% and 50% lines meet at $x^*=(0.4474+0.4444)/(0.1111+1.6842)=0.4967$. They are ordered correctly on the sample range 0.8 to 3.1, but a forecast below 0.50 would put the 10% quantile above the median.

**7. Forecast.** For tomorrow's volatility forecast of 2.0, the fitted 90% VaR is $-(0.4474-1.6842\times2.0)=2.9211$ points, and the normal rule gives $1.2816\times2.0=2.5632$.

**8. Hold-out.** Six later days have forecasts 1.0, 1.4, 1.8, 2.2, 2.8, 3.3 and returns 0.6, 1.4, −1.4, −1.1, −1.2, −4.4. Mean pinball loss is 0.2045 for the fitted line, 0.1938 for the normal rule and 0.4583 for the constant line. Days below the line are 0, 1 and 1 respectively. Both volatility-based lines beat the constant clearly. The normal rule edges the fitted line on pinball although it was breached once, because the fitted line sits further out at high volatility and pays for that on most of the other days. The last day has forecast 3.3, just beyond the fitted range of 0.8 to 3.1, so the fitted line is extrapolating exactly where it sits furthest out. Six days cannot settle this: a perfectly calibrated 10% quantile has a $0.9^6=0.5314$ chance of no breach at all.

**9. CAViaR step.** With $\mathrm{VaR}_{t-1}=2.0$ and $(\beta_0,\beta_1,\beta_2)=(0.05,0.90,0.30)$, a $-3.0$ return gives $0.05+1.8+0.9=2.75$, and a $+0.5$ return gives $0.05+1.8+0.15=2.0$. A large move of either sign raises tomorrow's VaR, and calm days let it decay.

**10. Tail precision.** For 250 standard normal returns, $\sqrt{\tau(1-\tau)/n}/f(q_\tau)$ gives a standard error of 0.1336 for the empirical 5% quantile (about 8% of 1.645) and 0.2361 for the 1% quantile (about 10% of 2.326).""",
        r"""- **Fit.** `statsmodels.formula.api.quantreg("r ~ vol_lag", data).fit(q=0.10)` or `QuantReg(y, X).fit(q=0.10)` returns `params`, `bse` and `conf_int()`. It solves by iteratively reweighted least squares, so coefficients match the exact vertex only to `p_tol` (default 1e-6). When the exact vertex matters, as in this lesson's worksheet, solve the linear program with `scipy.optimize.linprog(method="highs")`.
- **Timing.** The regressor must be known at $t-1$. A realized-volatility measure that includes day $t$ leaks the answer. A volatility forecast fitted on the same sample needs its own out-of-sample discipline (Lesson 3.15).
- **Quantile grid.** Fit several $\tau$ on the same data, report each slope with an interval, and check the ordering of fitted quantiles over the range of $x$. Sort them if they cross.
- **Inference.** `fit(q, vcov="robust", kernel="epa", bandwidth="hsheather")` is the default kernel sandwich, and `vcov="iid"` assumes one density at every $x$. Both rely on a density estimate that is poor when $n\tau$ is small. Prefer a pairs or block bootstrap: `arch.bootstrap.StationaryBootstrap` with a function that refits `QuantReg` on each replicate. The delete-one jackknife is a poor variance estimator for quantiles. Report $n\tau$ beside every interval.
- **CAViaR.** statsmodels has no implementation. Code the recursion, start $\mathrm{VaR}_0$ at the sample quantile of a burn-in window, and minimize the pinball objective with `scipy.optimize.minimize` from several starting values, keeping the best.
- **Evaluation.** Fit on a window, forecast one day ahead, roll forward, and store each candidate's hit and pinball loss on identical days: the quantile regression, an unconditional rolling quantile and a volatility rule. `scipy.stats.binomtest(hits, T, tau)` gives a first look at the count; Lesson 2.40 covers the formal tests. To check conditional calibration, regress hits on lagged hits and on $x$. A calibrated forecast leaves them unpredictable.
- **Report.** State the sign convention, $\tau$, regressor timing, window, tail count $n\tau$, hit rate and pinball loss against benchmarks, and the crossing check. A VaR forecast says nothing about how large losses are beyond it; Lesson 3.40 models that tail.""",
        "\\rho_\\tau(u)=u\\,\\bigl(\\tau-\\mathbf{1}\\{u<0\\}\\bigr),\\qquad \\hat\\beta(\\tau)=\\arg\\min_b\\sum_t\\rho_\\tau\\bigl(r_t-x_{t-1}'b\\bigr)",
        r"""from math import sqrt, exp, pi

# Cedar Capital desk log: prior-evening volatility forecast x and next-day return r, both in percent.
xs = [0.8, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.4, 2.7, 3.1]
rs = [-0.9, -0.5, 0.0, -0.3, 0.7, -2.6, 0.1, 1.0, -0.8, -4.1, -0.1]
# Six later days kept aside for evaluation.
xh = [1.0, 1.4, 1.8, 2.2, 2.8, 3.3]
rh = [0.6, 1.4, -1.4, -1.1, -1.2, -4.4]
tau = 0.10

def check(u, t):
    if u < 0:
        return u * (t - 1)
    return u * t

def mean_pinball(a, b, t, xl, rl):
    s = 0
    for i in range(len(xl)):
        s += check(rl[i] - a - b * xl[i], t)
    return s / len(xl)

# A day is below the line only if it is strictly below, with a tiny tolerance for rounding.
def below(a, b, xl, rl):
    k = 0
    for i in range(len(xl)):
        if rl[i] < a + b * xl[i] - 0.000001:
            k += 1
    return k

# The optimum of the linear program sits at a vertex: a line through two observations.
# With 11 days there are only 55 such lines, so try them all and keep the lowest loss.
def fit(t, xl, rl):
    best = 1000
    ba = 0
    bb = 0
    for i in range(len(xl)):
        for j in range(len(xl)):
            if j > i:
                if xl[j] != xl[i]:
                    b = (rl[j] - rl[i]) / (xl[j] - xl[i])
                    a = rl[i] - b * xl[i]
                    m = mean_pinball(a, b, t, xl, rl)
                    if m < best:
                        best = m
                        ba = a
                        bb = b
    return [ba, bb, best]

print("Check loss at u=-2:", round(check(-2, tau), 4))
print("Check loss at u=+2:", round(check(2, tau), 4))

# Candidate 1: one constant for every day. The minimizer is the ceil(n*tau)-th smallest return.
low1 = min(rs)
low2 = 1000
for r in rs:
    if r > low1:
        if r < low2:
            low2 = r
print("Constant 10% quantile:", low2)
print("Mean pinball, constant line:", round(mean_pinball(low2, 0, tau, xs, rs), 4))
print("Days below the constant line:", below(low2, 0, xs, rs))

# Candidate 2: zero-mean normal rule q = -1.2816 * x, where 1.2816 is the 90% normal quantile.
print("Mean pinball, normal rule:", round(mean_pinball(0, -1.2816, tau, xs, rs), 4))
print("Days below the normal rule:", below(0, -1.2816, xs, rs))

# Candidate 3: the fitted quantile line.
f = fit(tau, xs, rs)
print("Fitted intercept:", round(f[0], 4))
print("Fitted slope:", round(f[1], 4))
print("Mean pinball, fitted line:", round(f[2], 4))
print("Days below the fitted line:", below(f[0], f[1], xs, rs))

# Runner-up: the line through the days at x=1.7 and x=2.7.
s2 = (rs[9] - rs[5]) / (xs[9] - xs[5])
a2 = rs[5] - s2 * xs[5]
print("Mean pinball, runner-up line:", round(mean_pinball(a2, s2, tau, xs, rs), 4))

# Other quantiles, and where the 10% and 50% lines cross.
med = fit(0.50, xs, rs)
up = fit(0.90, xs, rs)
print("Median intercept:", round(med[0], 4))
print("Median slope:", round(med[1], 4))
print("90th percentile slope:", round(up[1], 4))
print("Lines cross at volatility:", round((f[0] - med[0]) / (med[1] - f[1]), 4))

# Forecast for tomorrow with volatility forecast 2.0. VaR is the negative of the quantile.
print("Fitted 90% VaR at volatility 2.0:", round(-(f[0] + f[1] * 2.0), 4))
print("Normal-rule 90% VaR at volatility 2.0:", round(1.2816 * 2.0, 4))

# Hold-out: the same three lines scored on days that were not used for fitting.
print("Hold-out mean pinball, fitted line:", round(mean_pinball(f[0], f[1], tau, xh, rh), 4))
print("Hold-out mean pinball, normal rule:", round(mean_pinball(0, -1.2816, tau, xh, rh), 4))
print("Hold-out mean pinball, constant line:", round(mean_pinball(low2, 0, tau, xh, rh), 4))
print("Hold-out days below the fitted line:", below(f[0], f[1], xh, rh))
print("Hold-out days below the normal rule:", below(0, -1.2816, xh, rh))
print("Hold-out days below the constant line:", below(low2, 0, xh, rh))
print("Chance of no breach in 6 days:", round(0.9 ** 6, 4))

# One CAViaR step on the positive VaR scale: VaR_t = b0 + b1 * VaR_{t-1} + b2 * |r_{t-1}|.
var_prev = 2.0
print("CAViaR VaR after a -3.0 return:", round(0.05 + 0.90 * var_prev + 0.30 * abs(-3.0), 4))
print("CAViaR VaR after a +0.5 return:", round(0.05 + 0.90 * var_prev + 0.30 * abs(0.5), 4))

# Precision of an empirical quantile of 250 standard normal returns: sqrt(tau(1-tau)/n) / f(q).
def normal_pdf(z):
    return exp(-0.5 * z * z) / sqrt(2 * pi)

print("SE of a 5% quantile, 250 days:", round(sqrt(0.05 * 0.95 / 250) / normal_pdf(1.6448536), 4))
print("SE of a 1% quantile, 250 days:", round(sqrt(0.01 * 0.99 / 250) / normal_pdf(2.3263479), 4))""",
        "Cedar's second hold-out has four days with volatility forecasts 1.2, 1.9, 2.5, 3.0 and returns −0.8, −2.9, 0.3, −4.2. At τ = 0.10, use the case's fitted line (intercept 0.4474, slope −1.6842) and the normal rule (−1.2816 times the forecast). For each rule count the days with a return strictly below its quantile and compute the mean pinball loss. Then find the probability that a perfectly calibrated 10% quantile is breached at least twice in four days, and say in two sentences what these four days can and cannot show.",
        "Fitted-line quantiles are −1.574, −2.753, −3.763 and −4.605. Only the −2.9 day lies below its quantile, so there is 1 breach. The pinball terms are 0.077, 0.133, 0.406 and 0.041, giving a mean of 0.164. Normal-rule quantiles are −1.538, −2.435, −3.204 and −3.845. The −2.9 and −4.2 days both lie below, so there are 2 breaches. Its terms are 0.074, 0.418, 0.350 and 0.320, a mean of 0.291. The fitted line wins here, whereas the normal rule edged it on the case's six days, so the ranking flips between small windows. For a calibrated 10% quantile the chance of at least two breaches in four days is 1 − 0.9^4 − 4(0.1)(0.9^3) = 1 − 0.6561 − 0.2916 = 0.0523. Two breaches for the normal rule are therefore mildly surprising but not damning, particularly after comparing several rules on the same four days. Four days can show that a rule is not wildly wrong, but they cannot establish calibration or rank two rules whose losses differ by this little. That needs hundreds of days scored out of sample.",
        [
            (
                "A 5% quantile forecast is breached by a return 3 points below it. Another day's return lands 3 points above it. The check loss of the breach is how many times that of the other day?",
                ['5 times', '1 time (they are equal)', '19 times'],
                2,
                'At tau = 0.05 the breach has u = −3, so the loss is −3 × (0.05 − 1) = 2.85. The other day has u = +3, so its loss is 3 × 0.05 = 0.15. The ratio is 2.85 / 0.15 = 19 = (1 − tau) / tau.',
            ),
            (
                'A quantile regression of returns on one volatility forecast, with an intercept, is a linear program. At the exact solution the fitted line passes through:',
                ['No observations', 'Exactly two observations', 'Every observation below it'],
                1,
                'A vertex of the feasible polyhedron has p residuals exactly zero, where p is the number of coefficients. With an intercept and one slope p = 2, so the line interpolates two days.',
            ),
            (
                "A desk fits the 5% quantile line q = 0.20 − 1.70x in percent. Tomorrow's volatility forecast is x = 2.5. The 95% VaR as a positive loss is:",
                ['4.05', '4.25', '4.45'],
                0,
                'q = 0.20 − 1.70 × 2.5 = 0.20 − 4.25 = −4.05, and VaR is the negative of the quantile, so 4.05. The value 4.25 drops the intercept, and 4.45 adds the intercept to the VaR with the wrong sign.',
            ),
            (
                'A fitted 5% quantile line, with an intercept, breaches 5.0% of the days it was fitted on, but 9% of the days after the fit. Which reading is correct?',
                ['The in-sample 5% proves the model is correctly specified, and the 9% is noise', 'The in-sample 5% is close to mechanical, so only the 9% out-of-sample rate is evidence about calibration', 'The pinball loss must be miscomputed'],
                1,
                'With an intercept, the fit satisfies N_- ≤ n·tau ≤ N_- + N_0, so the in-sample hit rate is near tau by construction. A 9% rate on later days, if it persists, points to miscalibration or a change in the relationship between volatility and the tail.',
            ),
        ],
        [('statsmodels contributors · QuantReg', 'https://www.statsmodels.org/stable/generated/statsmodels.regression.quantile_regression.QuantReg.html'), ('Koenker & Bassett (1978) · Regression Quantiles', 'https://doi.org/10.2307/1913643'), ('Engle & Manganelli · CAViaR: Conditional Value at Risk by Quantile Regression (NBER Working Paper 7341; published 2004 in J. Business & Economic Statistics)', 'https://www.nber.org/papers/w7341'), ('Gneiting (2011) · Making and Evaluating Point Forecasts', 'https://arxiv.org/abs/0912.0902')],
    ),
    (
        '3.40',
        9,
        'Extreme value theory: peaks over threshold and tail quantiles',
        'Fit a generalized Pareto tail to threshold excesses and extrapolate a high loss quantile and expected shortfall beyond the sample, with honest uncertainty.',
        r"""Lesson 3.4 estimated a 99% VaR as a sample quantile, and Lesson 3.39 modelled a conditional quantile. Both need observations in the region they describe. With $n=1{,}000$ days, a 99.9% loss quantile has $n(1-p)=1$ expected exceedance, so the sample says almost nothing about it. Extreme value theory (EVT) treats the tail as its own object and extrapolates from the few observations that reach it.

**Why central-limit reasoning fails in the tail.** The central limit theorem describes averages near their center, on the scale of standard errors. It does not give the probability of a single loss six standard deviations out: the theorem controls absolute error, and far in the tail, where probabilities are tiny, the relative error of a normal approximation can be orders of magnitude. For heavy-tailed variables a sum's tail is dominated by its largest term, $P(S_n>x)\approx nP(X_1>x)$ for large $x$, which no normal approximation reproduces. A one-in-a-thousand-day loss is a statement about a maximum, and maxima have their own limit theory.

**Fisher–Tippett–Gnedenko.** Let $M_n=\max(X_1,\dots,X_n)$ for iid $X_i$. If constants $a_n>0$ and $b_n$ exist such that $(M_n-b_n)/a_n$ converges in distribution to a nondegenerate $G$, then $G$ is, up to location and scale, a generalized extreme value law,
$$G_\xi(x)=\exp\{-(1+\xi x)^{-1/\xi}\},\qquad 1+\xi x>0,$$
with the Gumbel law $\exp(-e^{-x})$ at $\xi=0$. The shape $\xi$ classifies tails. For $\xi>0$ the tail decays like a power, $x^{-1/\xi}$; a Student $t$ with $\nu$ degrees of freedom has $\xi=1/\nu$. At $\xi=0$ the decay is exponential-type, as for the normal. For $\xi<0$ the support has a finite upper end point.

**Pickands–Balkema–de Haan.** Block maxima discard most of the data, so work with excesses over a high threshold $u$. If $F$ lies in the domain of attraction of $G_\xi$, then as $u$ rises toward the upper end point
$$P(X-u\le y\mid X>u)\ \to\ G_{\xi,\beta}(y)=1-\Big(1+\frac{\xi y}{\beta}\Big)^{-1/\xi},\qquad y\ge0,$$
the generalized Pareto distribution (GPD) with shape $\xi$ and scale $\beta=\beta(u)>0$ (exponential at $\xi=0$). For $\xi<1$ its mean excess over any $v\ge u$ is linear in $v$: $e(v)=\mathrm E[X-v\mid X>v]=\big(\beta+\xi(v-u)\big)/(1-\xi)$. Above a higher threshold the GPD keeps the same $\xi$ and has scale $\beta+\xi(v-u)$.

**Tail quantiles.** Let $N_u$ of $n$ observations exceed $u$. The frequency $N_u/n$ estimates $P(X>u)$ and the GPD models the excess, so for $x>u$
$$\hat F(x)=1-\frac{N_u}{n}\Big(1+\hat\xi\,\frac{x-u}{\hat\beta}\Big)^{-1/\hat\xi}.$$
Inverting at level $p$, with $\tfrac{n}{N_u}(1-p)<1$ so that the quantile exceeds $u$,
$$\mathrm{VaR}_p=u+\frac{\beta}{\xi}\Big[\Big(\frac{n}{N_u}(1-p)\Big)^{-\xi}-1\Big].$$
For $\xi<1$, expected shortfall adds the mean excess at the VaR, $\mathrm{ES}_p=\mathrm{VaR}_p+e(\mathrm{VaR}_p)$, which simplifies to
$$\mathrm{ES}_p=\frac{\mathrm{VaR}_p+\beta-\xi u}{1-\xi}.$$
For $\xi>0$ the ratio $\mathrm{ES}_p/\mathrm{VaR}_p$ tends to $1/(1-\xi)$ as $p\to1$. Maximum likelihood on the $N_u$ excesses is regular for $\xi>-\tfrac12$, with $\mathrm{se}(\hat\xi)\approx(1+\xi)/\sqrt{N_u}$ for independent excesses.

**Hill and Weissman.** If $\xi>0$ and $1-F(x)=x^{-1/\xi}L(x)$ with $L$ slowly varying, take the order statistics $X_{(1)}\ge X_{(2)}\ge\cdots$ and use $X_{(k+1)}$ as the threshold. Hill (1975) proposed
$$\hat\xi_k=\frac1k\sum_{i=1}^{k}\big[\ln X_{(i)}-\ln X_{(k+1)}\big],\qquad \mathrm{se}\approx\hat\xi_k/\sqrt k.$$
It needs positive losses. Multiplying every loss by a constant leaves it unchanged, whereas adding a constant does not. Since $P(X>x)\approx\frac kn\big(x/X_{(k+1)}\big)^{-1/\xi}$, Weissman's extrapolation is
$$\hat x_p=X_{(k+1)}\Big(\frac{k}{n(1-p)}\Big)^{\hat\xi_k}.$$
It is the VaR formula with $u=X_{(k+1)}$, $N_u=k$ and $\beta=\xi u$. To leading order its relative standard error is $\hat\xi_k\ln\!\big(k/(n(1-p))\big)/\sqrt k$, which grows with the extrapolation distance; the sampling error of the threshold itself adds to it at short distances.

**Threshold choice.** Raising $u$ makes the GPD more accurate but leaves fewer exceedances, so variance grows like $1/N_u$. Lowering $u$ adds bias because the GPD is a limit result. Inspect (i) the mean-excess plot, roughly linear above a valid threshold with slope $\xi/(1-\xi)$; (ii) $\hat\xi$ and the modified scale $\hat\beta-\hat\xi u$ against $u$, both flat above it; and (iii) the Hill plot of $\hat\xi_k$ against $k$, looking for a plateau. Report results at several thresholds.

**Dependence and declustering.** The iid likelihood assumes independent excesses, but returns show volatility clustering (Lesson 3.18), so exceedances arrive in runs of stress days. For a stationary sequence the extremal index $\theta\in(0,1]$ is the reciprocal of the mean cluster size, with $\theta=1$ under independence. Runs declustering ends a cluster once $r$ consecutive days fall at or below $u$, keeps each cluster's maximum, and estimates $\hat\theta=N_c/N_u$ from the number of clusters $N_c$. Fitting all excesses still targets the marginal tail, but iid standard errors are too small, because the information is nearer $N_c$ independent peaks than $N_u$ excesses (a heuristic, not a theorem). McNeil and Frey (2000) avoid the problem by fitting a GARCH filter (Lesson 3.18), applying the GPD to the roughly independent standardized residuals, and rebuilding $\mathrm{VaR}_{t+1}=\mu_{t+1}+\sigma_{t+1}z_p$.""",
        r"""Cedar Capital's book has $n=1{,}000$ daily losses, in percent of net asset value, with sample standard deviation 1.00. The 21 largest are 6.1, 4.5, 3.6, 3.1, 3.0, 2.9, 2.8, 2.7, 2.6, 2.5, 2.5, 2.4, 2.4, 2.3, 2.2, 2.2, 2.1, 2.1, 2.1, 2.1, 2.1.

**1. Normal benchmark.** A normal model puts the 99.9% loss quantile at $3.0902\times1.00=3.0902$. The second-largest loss, which is the nearest-rank 99.9% sample quantile, is 4.5, and the worst day was a 6.1 standard deviation loss.

**2. Hill estimates.** With $k=10$ the threshold is $X_{(11)}=2.5$ and $\hat\xi_{10}=\frac1{10}\sum_{i=1}^{10}\ln(X_{(i)}/2.5)=0.262$. With $k=20$ the threshold is $X_{(21)}=2.1$ and $\hat\xi_{20}=0.2494$. The standard errors $\hat\xi_k/\sqrt k$ are 0.0828 and 0.0558. The two estimates agree within one standard error, which is consistent with a plateau. They share their ten largest terms, so a real Hill plot scans every $k$ to look for stability.

**3. Mean-excess check.** The 14 losses above 2.2 average 3.1, a mean excess of 0.9. The 8 losses above 2.6 average 3.5875, a mean excess of 0.9875. The slope between the two thresholds is $s=(0.9875-0.9)/0.4=0.21875$, which implies $\xi=s/(1+s)=0.1795$. That is below the Hill values, but it rests on only 8 to 14 points, so it cannot tell $\xi$ near 0.18 from $\xi$ near 0.26. Far-tail mean-excess plots are noisy.

**4. Weissman extrapolation.** At $p=0.999$ and $k=20$, $k/(n(1-p))=20$, so
$$\hat x_{0.999}=2.1\times20^{0.2494}=4.4335.$$
With $k=10$ the result is $2.5\times10^{0.262}=4.57$. Fractional powers are computed as exp(power × log(base)). The leading-order relative standard error for $k=20$ is $0.2494\ln 20/\sqrt{20}=0.1671$, about 17%. The sample maximum is no better: the true 99.9% quantile is exceeded at least once in 1,000 days with probability $1-0.999^{1000}=0.6323$, so the maximum overshoots it more often than not.

**5. Generalized Pareto tail.** The desk's maximum-likelihood fit to its $N_u=50$ excesses over $u=1.5$ gave $\hat\xi=0.24$ and $\hat\beta=0.50$, so $n/N_u=20$. Then
$$\mathrm{VaR}_{0.99}=1.5+\frac{0.50}{0.24}\Big[(20\times0.01)^{-0.24}-1\Big]=2.4822$$
$$\mathrm{VaR}_{0.999}=1.5+\frac{0.50}{0.24}\Big[(20\times0.001)^{-0.24}-1\Big]=4.744$$
$$\mathrm{ES}_{0.99}=\frac{2.4822+0.50-0.24\times1.5}{1-0.24}=3.4503$$
$$\mathrm{ES}_{0.999}=\frac{4.744+0.50-0.36}{0.76}=6.4263$$
At 99% the GPD agrees with the sample quantile, the 11th largest loss, 2.5, so EVT adds little inside the data. At 99.9% it gives 4.744, close to the Weissman values 4.4335 and 4.57 and to the observed second-largest loss of 4.5. The 99.9% expected shortfall of 6.4263 exceeds the worst loss in the sample, 6.1. The sample holds one loss beyond the 99.9% VaR, whereas the model averages over the whole tail beyond it.

**6. Declustering.** Among seven exceedance days, 12, 13, 14, 20, 40, 41 and 90, a gap of more than 5 days starts a new cluster. The clusters are {12, 13, 14}, {20}, {40, 41} and {90}, so $N_c=4$ and $\hat\theta=4/7=0.5714$. With 50 independent excesses the shape standard error is $(1+0.24)/\sqrt{50}=0.1754$, and 1.96 standard errors give a half-width of 0.3437, wide enough to reach below zero. If the desk's 50 exceedances clustered like these seven, they would carry about $50\times0.5714=28.5714$ independent peaks, and the heuristic standard error would rise to $1.24/\sqrt{28.5714}=0.232$.""",
        r"""- **Choose the threshold.** Sort the losses, compute the mean excess $e(u)$ and the fitted $\hat\xi$ and $\hat\beta-\hat\xi u$ over a grid of $u$ with numpy, and plot them. Take the lowest threshold above which they look flat while $(1+\hat\xi)/\sqrt{N_u}$ is still tolerable. Then repeat the final quantile at neighbouring thresholds and report the range.
- **Fit.** `scipy.stats.genpareto.fit(excesses, floc=0)` returns `(c, loc, scale)`, where `c` is $\xi$ and `scale` is $\beta$. Fix `floc=0` because excesses start at zero. Beware that `scipy.stats.genextreme` uses the opposite sign, with `c` equal to $-\xi$. The quantile is `u + genpareto.ppf(1 - n / N_u * (1 - p), c, scale=scale)`, and expected shortfall is the integral of that quantile function over $[p,1]$ divided by $1-p$, computed with `scipy.integrate.quad`.
- **Uncertainty.** Use a profile-likelihood or bootstrap interval for $\hat\xi$ and for the extrapolated quantile instead of a symmetric normal interval alone. The quantile depends on $\xi$ through the power $\big(\tfrac{n}{N_u}(1-p)\big)^{-\xi}$, so its interval is skewed and widens quickly with extrapolation distance. For dependent returns, bootstrap blocks (Lesson 3.27) and redo the threshold step in every replicate.
- **Dependence.** Decluster with several run lengths $r$, report $N_c$ and $\hat\theta$, and fit the cluster maxima. Or follow McNeil and Frey: fit a GARCH model with the `arch` package (Lesson 3.18), run the GPD on the tail of the standardized residuals, and rebuild the forecast as $\mu_{t+1}+\sigma_{t+1}z_p$.
- **Check.** Levels beyond $1-1/n$ cannot be verified on the same sample. Validate the method at levels you can observe, such as 95% to 99%, on later data with the hit counts and pinball loss of Lesson 3.39, and compare Hill and GPD answers when $\xi>0$ is plausible.
- **Report.** State the loss sign, $n$, $u$, $N_u$ and clusters, $\hat\xi$ and $\hat\beta$ with intervals, VaR and ES levels, and the sensitivity to $u$. An extrapolated 99.9% figure is a statement about a fitted model, not an observed frequency, and it is only as good as the GPD assumption above the threshold.""",
        '\\mathrm{VaR}_p=u+\\frac{\\beta}{\\xi}\\left[\\left(\\frac{n}{N_u}(1-p)\\right)^{-\\xi}-1\\right],\\qquad \\mathrm{ES}_p=\\frac{\\mathrm{VaR}_p+\\beta-\\xi u}{1-\\xi}',
        r"""from math import sqrt, log, exp

n = 1000
# The 21 largest of 1,000 daily losses, in percent of NAV, largest first.
top = [6.1, 4.5, 3.6, 3.1, 3.0, 2.9, 2.8, 2.7, 2.6, 2.5, 2.5, 2.4, 2.4, 2.3, 2.2, 2.2, 2.1, 2.1, 2.1, 2.1, 2.1]

# Hill estimator from the top k losses, with the (k+1)-th largest as the threshold.
def hill(xs, k):
    s = 0
    for i in range(k):
        s += log(xs[i]) - log(xs[k])
    return s / k

# Mean excess over a threshold v, using only the stored losses (valid for v above the 22nd largest).
def mean_excess(xs, v):
    s = 0
    c = 0
    for x in xs:
        if x > v:
            s += x - v
            c += 1
    return s / c

# Weissman extrapolation. Fractional powers are written as exp(power * log(base)).
def weissman(xs, k, size, p, xi):
    return xs[k] * exp(xi * log(k / (size * (1 - p))))

# 99.9% normal quantile 3.0902 times the desk's sample standard deviation of 1.00 percent.
print("Normal 99.9% loss quantile:", round(3.0902 * 1.00, 4))
print("Second largest loss:", top[1])

h10 = hill(top, 10)
h20 = hill(top, 20)
print("Hill estimate, k=10:", round(h10, 4))
print("Hill estimate, k=20:", round(h20, 4))
print("Hill standard error, k=10:", round(h10 / sqrt(10), 4))
print("Hill standard error, k=20:", round(h20 / sqrt(20), 4))
me1 = mean_excess(top, 2.2)
me2 = mean_excess(top, 2.6)
slope = (me2 - me1) / (2.6 - 2.2)
print("Mean excess over 2.2:", round(me1, 4))
print("Mean excess over 2.6:", round(me2, 4))
print("Mean-excess slope:", round(slope, 5))
print("Shape implied by the mean-excess slope:", round(slope / (1 + slope), 4))
print("Weissman 99.9% quantile, k=10:", round(weissman(top, 10, n, 0.999, h10), 4))
print("Weissman 99.9% quantile, k=20:", round(weissman(top, 20, n, 0.999, h20), 4))
print("Relative standard error, k=20:", round(h20 * log(20 / (n * (1 - 0.999))) / sqrt(20), 4))
print("Chance of a 99.9% breach within 1,000 days:", round(1 - exp(1000 * log(0.999)), 4))

# Generalized Pareto tail from the desk's maximum-likelihood fit to its 50 excesses over 1.5.
xi = 0.24
beta = 0.50
u = 1.5
nu = 50

def gpd_var(p):
    return u + beta / xi * (exp(-xi * log(n / nu * (1 - p))) - 1)

def gpd_es(p):
    return (gpd_var(p) + beta - xi * u) / (1 - xi)

print("Sample 99% quantile, 11th largest:", top[10])
print("GPD 99% VaR:", round(gpd_var(0.99), 4))
print("GPD 99.9% VaR:", round(gpd_var(0.999), 4))
print("GPD 99% expected shortfall:", round(gpd_es(0.99), 4))
print("GPD 99.9% expected shortfall:", round(gpd_es(0.999), 4))
print("Shape standard error, independent excesses:", round((1 + xi) / sqrt(nu), 4))
print("Shape half-width of a 95% interval:", round(1.96 * (1 + xi) / sqrt(nu), 4))

# Runs declustering of seven exceedance days: a new cluster starts after a gap of more than 5 days.
days = [12, 13, 14, 20, 40, 41, 90]
clusters = 1
for j in range(1, len(days)):
    if days[j] - days[j - 1] > 5:
        clusters += 1
theta = clusters / len(days)
print("Clusters among seven exceedance days:", clusters)
print("Extremal index estimate:", round(theta, 4))
print("Effective exceedances out of 50:", round(nu * theta, 4))
print("Shape standard error, clustered:", round((1 + xi) / sqrt(nu * theta), 4))""",
        "Using the case's 21 losses, take k = 15, so the threshold is the 16th largest loss, 2.2. Compute the Hill estimate and its standard error, the Weissman 99.95% loss quantile (so n(1 − p) = 0.5), and its relative standard error. Compare them with the k = 20 values at the same level, and say in two sentences what moving from 99.9% to 99.95% does to the uncertainty.",
        'For k = 15 the threshold is the 16th largest loss, 2.2. The 15th largest is also 2.2, so its term ln(2.2/2.2) is 0, and the Hill estimate is the average of ln(loss / 2.2) over the 15 largest losses, which is 0.2830. Its standard error is 0.2830/sqrt(15) = 0.0731. At p = 0.9995, k/(n(1 − p)) = 15/0.5 = 30, so the Weissman quantile is 2.2 × 30^0.2830 = 5.7596, with relative standard error 0.2830 × ln(30)/sqrt(15) = 0.2485. With k = 20 the ratio is 20/0.5 = 40, giving 2.1 × 40^0.2494 = 5.2703 with relative standard error 0.2494 × ln(40)/sqrt(20) = 0.2058. At 99.9% the k = 20 relative standard error was 0.1671, so the extra extrapolation raises it by about 23%, because the factor ln(k/(n(1 − p))) grows from 3.00 to 3.69 while the estimate of the shape stays the same. The two choices of k differ by 0.49, about 9%, which is well inside one standard error of 0.2485 × 5.76 = 1.43. The data cannot say which k is right, so report both and the range, and treat the 99.95% figure as a model statement beyond the sample: at n(1 − p) = 0.5 it lies past what a thousand days can directly show.',
        [
            (
                'A GPD has shape 0.5 and scale 0.6 over the threshold u = 2.0. With n / N_u = 20, the 99.8% VaR is:',
                ['1.04', '4.80', '6.80'],
                2,
                'n/N_u × (1 − p) = 20 × 0.002 = 0.04, and 0.04^(−0.5) = 5. Then VaR = 2.0 + (0.6 / 0.5)(5 − 1) = 2.0 + 4.8 = 6.8. The value 4.80 forgets to add the threshold, and 1.04 flips the sign of the exponent.',
            ),
            (
                'A Hill estimate computed on losses in percent is 0.25. Recomputing it on the same losses divided by 100, in decimals, gives:',
                ['0.0025', '0.25', '2.5'],
                1,
                'Each term is ln X(i) − ln X(k+1). Dividing every loss by 100 subtracts ln 100 from both logarithms, so each difference and the average are unchanged. Adding a constant to the losses, unlike rescaling, would change the estimate.',
            ),
            (
                'A GPD tail has shape 0.25, scale 1.0 and threshold 2.0, and its VaR at the chosen level is 5.0. The expected shortfall at that level is:',
                ['7.33', '6.67', '8.00'],
                0,
                'ES = (VaR + beta − xi × u) / (1 − xi) = (5.0 + 1.0 − 0.25 × 2.0) / 0.75 = 5.5 / 0.75 = 7.33. The value 6.67 is the pure Pareto shortcut VaR / (1 − xi), and 8.00 omits the xi × u term.',
            ),
            (
                'Daily returns show volatility clustering. For a GPD fitted to all N_u threshold excesses, the main consequence is:',
                ['The GPD cannot be fitted to dependent data at all', 'The excesses arrive in clusters, so standard errors that assume N_u independent excesses are too small', 'Clustering forces the shape xi to be negative'],
                1,
                'Fitting all excesses still targets the marginal tail, but stress days come in runs, so the information is nearer the number of clusters than N_u. Declustering, or a GARCH filter followed by a GPD on standardized residuals, restores approximate independence.',
            ),
        ],
        [('SciPy contributors · scipy.stats.genpareto', 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.genpareto.html'), ('Pickands (1975) · Statistical Inference Using Extreme Order Statistics', 'https://doi.org/10.1214/aos/1176343003'), ('Hill (1975) · A Simple General Approach to Inference About the Tail of a Distribution', 'https://doi.org/10.1214/aos/1176343247'), ('McNeil & Frey (2000) · Estimation of tail-related risk measures for heteroscedastic financial time series: an extreme value approach', 'https://doi.org/10.1016/S0927-5398(00)00012-8')],
    ),
]

APPLICATIONS = [
    ('3.33', 'calibration', "A payment processor's stated loss rate is a likelihood claim, and the choice of test statistic can decide whether a batch of data appears to contradict it.", "A fictional processor's model says 2% of invoices in a merchant batch go unpaid. A batch of 150 invoices has 7 unpaid. Compute the Wald and score statistics against 3.841, the exact upper binomial tail, and say what you would report.", 'The estimate is 4.67%. The Wald statistic is 2.398 and does not reject, the score statistic is 5.442 and does, and the exact tail P(X >= 7) = 0.0320 supports the score verdict. With only 3 unpaid invoices expected the normal approximation is stretched, so report the exact tail and a Wilson interval. Caveat: if the invoices come from one merchant, outcomes may be correlated, and an independent binomial likelihood then understates the variance.'),
    ('3.34', 'factors', 'A one-factor model must price every test portfolio with the same factor loading, so disagreement between portfolios is a testable restriction rather than a matter of taste.', 'A fictional test uses 60 months, mean excess returns of 0.10% and 0.90% for two portfolios, equal factor products of 10 and a long-run covariance equal to 4 times the identity. Estimate the SDF loading, its standard error, the pricing errors and J against 3.841.', 'With equal weights the first step is already efficient: b = (10 × 0.10 + 10 × 0.90) / 200 = 0.05, standard error 1 / √(60 × 50) = 0.0183, pricing errors (−0.4, +0.4) and J = 60 × (0.16 + 0.16) / 4 = 4.8, which exceeds 3.841 (p = 0.028). The portfolios imply different SDF loadings, 0.01 and 0.09, and no single loading reconciles them. J does not say which portfolio is mispriced, and with 60 months and an estimated long-run covariance it can over-reject, so check a longer lag and an iterated estimator before discarding the model.'),
    ('3.35', 'factors', "A joint test of every portfolio's alpha answers a different question from scanning separate alpha t statistics, and its power depends on how many portfolios the sample can support.", 'A fictional desk fits a market model to 25 portfolios over 84 months and obtains a GRS F of 2.10. State the two degrees of freedom, count the distinct residual covariance elements the test must estimate, and name what you would report beside the p-value.', 'The degrees of freedom are 25 and 84 − 25 − 1 = 58. The residual covariance matrix has 325 distinct elements estimated from 84 months, so the statistic is noisy and its power is limited. Report the average absolute alpha and the Sharpe-ratio gain beside the p-value; a tiny, precisely measured alpha can reject, and low power can hide a large one.'),
    ('3.36', 'forecasting', 'A persistent predictor whose innovations correlate with return shocks makes a regression slope look stronger in-sample than it is, so a forecasting rule must be judged on data it has not seen.', "A fictional desk finds that a valuation ratio predicts next quarter's excess return with an in-sample R² of 5.4% and a t of 2.6 over 120 quarters. Specify the bias check, the overlap check and the out-of-sample benchmark you would run before trusting the slope.", "Estimate the predictor's autoregression and the covariance of its innovation with the return shock, then adjust the slope for Stambaugh bias. Use a covariance that allows for overlap if returns span several quarters, and compare recursive forecasts with the historical mean through R²_OS. A positive out-of-sample R² in one window is not stable evidence, and its economic value depends on costs the statistical result ignores."),
    ('3.37', 'bi_rate', 'A dated policy announcement supplies a break date from the calendar rather than from the return data, which is the condition a Chow test needs.', 'A fictional desk regresses 310 daily rupiah returns on a dollar-index factor (k = 2) around a 24 April 2024 policy date, with 250 days before and 60 after. The pooled SSR is 120.0 and the segment SSRs are 70.0 and 44.0. Compute the Chow F, compare it with a 5% critical value of 3.03, and check the equal-variance condition.', 'F = ((120.0 − 114.0)/2)/(114.0/306) = 8.05, well above 3.03, so constant coefficients are rejected if the date is exogenous. The segment variances are 70.0/248 = 0.282 and 44.0/58 = 0.759, a ratio near 2.7, which breaks the equal-variance condition, so use a heteroskedasticity-robust Wald test before trusting the p-value. A caveat: one announcement date can coincide with other news, so a rejection shows that coefficients shifted, not that the decision caused the shift.'),
    ('3.38', 'factors', "A fund's exposure to a published factor can drift between reporting dates, so an audit needs an estimate of today's beta that uses only what was known on that date.", 'A fictional fund has a prior market beta of 0.9 with variance 0.04 before month 1. Residual variance is 1.0 and drift variance is 0.01, in percent units. Month 1 brings a factor return of 2.0 and a fund return of 2.4. Compute the Kalman gain, the innovation and the updated beta, and say which beta can set the hedge for month 1 and which can set the hedge for month 2.', "The forecast variance is 4 × 0.04 + 1.0 = 1.16, so the gain is 0.04 × 2/1.16 = 0.0690. The innovation is 2.4 − 2.0 × 0.9 = 0.6, and the updated beta is 0.9 + 0.0690 × 0.6 = 0.9414 with variance 0.0345. The hedge for month 1 had to use the prior 0.9, because 0.9414 already contains month 1's own return. The updated 0.9414 can set the hedge for month 2, and a smoothed beta can set neither because it borrows later months. A caveat: one month barely moves a tight prior, and every figure depends on the assumed noise variances, which a handful of months cannot estimate reliably."),
    ('3.39', 'calibration', 'A quantile forecast is a probability statement: a 5% limit that is breached far more or less often than 5% of the time is miscalibrated.', "A fictional Cedar desk's 5% loss limit, scaled to forecast volatility, was breached on 9 of 120 days. Compute the expected breaches, their standard deviation and the z-score, then name two scores to compare the limit with a constant limit on later days.", 'Expected breaches are 120 × 0.05 = 6 with standard deviation sqrt(120 × 0.05 × 0.95) = 2.39, so 9 breaches give z = 1.26, within ordinary noise. Compare average pinball loss and breach counts on days not used to set the limit. With only 9 breach days driving the evidence, a sample this short cannot separate miscalibration from luck.'),
    ('3.40', 'flash_crash', 'A tail model must say how bad a rare day could be, and sudden liquidity loss is the kind of event that tests whether a fitted tail is believable.', 'A fictional Cedar fund has 2,500 daily losses, of which 125 exceed 1.8% of NAV. A generalized Pareto fit gives shape 0.30 and scale 0.60. Compute the 99.9% VaR and expected shortfall, and name two checks to run before a limit is set at that VaR.', 'Here n/N_u = 20, so VaR = 1.8 + (0.60/0.30)[(20 × 0.001)^(−0.30) − 1] = 6.27 and ES = (6.27 + 0.60 − 0.30 × 1.8)/0.70 = 9.04, in percent of NAV. Repeat the fit at neighbouring thresholds and bootstrap an interval for the quantile. The fitted tail describes ordinary stress days, so a day when liquidity disappears can fall outside it.'),
]
