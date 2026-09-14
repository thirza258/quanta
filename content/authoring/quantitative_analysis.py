"""Original course spanning the fourth edition's fourteen quantitative topics."""

from book_courses import finish, lesson, q

BOOK = "https://www.wiley-vch.de/en/areas-interest/finance-economics-law/finance-investments-13fi/investments-securities-13fi3/quantitative-investment-analysis-978-1-119-74362-0"


def build_quantitative_analysis():
    modules = []

    def add(id, chapter, title, objective, content, formula, code, task, solution, questions):
        modules.append(
            lesson(
                id,
                str(chapter),
                title,
                objective,
                f"CFA Institute, Quantitative Investment Analysis, fourth edition · Chapter {chapter}. Pair the book reading with this original application; course lesson numbers are independent of book chapter numbers.",
                content,
                formula,
                code,
                task,
                solution,
                questions,
            )
        )

    add(
        "2.1",
        1,
        "Time value of money",
        "Put cash flows on a timeline and use a discount rate consistent with their timing and units.",
        r"""
## First draw the timeline

Discounting translates cash flows at different dates into a common date. Specify the currency, payment dates, compounding convention, and whether amounts are nominal or inflation-adjusted. A nominal rate belongs with nominal cash flows; mixing it with real cash flows can count inflation inconsistently.

For one payment, moving forward multiplies by the accumulation factor and moving backward divides by it. Multiple payments must each be discounted from their own date. The discount rate represents an assumed opportunity cost appropriate to the modeled cash flow, not a universal constant.

An ordinary annuity pays at period ends. An annuity due pays at period beginnings, so each payment is one period earlier. A growing perpetuity assumes infinitely many payments growing at a constant rate; its familiar formula requires a discount rate above growth.

$$PV=\sum_{t=1}^{T}\frac{CF_t}{(1+r)^t}$$

## A worked example

A fictional fund owes $110 in one year and $121 in two years. At a 10% annual rate, each payment has present value of $100, so total present value is $200. Simply dividing their sum by 1.10 discounts the second payment from the wrong date.

A perpetuity paying $5 next year with 2% growth and a 7% required return has value 5 / (0.07 − 0.02) = $100. The next-year payment belongs in the numerator. If rate and growth are equal, this finite-value formula is undefined.

## Translate a result into a decision

Check whether the selected rate and the timing assumptions match the actual question. A promised payment and an uncertain business cash flow need different risk analysis even if the arithmetic is identical. For a terminal value, show the share of total value that depends on distant assumptions.

Reproduce the timeline before using a spreadsheet function. A correct function with misdated cash flows gives the wrong economic answer.
""",
        r"PV=\sum CF_t/(1+r)^t",
        'cash_flows = [110, 121]\npv = 0\nfor i in range(len(cash_flows)):\n    pv = pv + cash_flows[i] / 1.10 ** (i + 1)\nprint("Present value:", round(pv, 2))\nprint("Growing perpetuity:", 5 / (.07 - .02))',
        "Discount payments of 105 and 110.25 at the ends of years one and two using 5%. Then move both payments one year earlier and explain the change.",
        "The ordinary timeline is worth 200. Moving every payment one year earlier multiplies value by 1.05, giving 210. State that the first shifted payment occurs today.",
        [
            q(
                "When is a growing perpetuity with positive next-year cash flow finite and positive?",
                ["When r > g", "When r = g", "When r < g"],
                0,
                "The denominator r − g must be positive in this constant-growth model.",
            ),
            q(
                "Two equal payments occur at years one and two. Which procedure is correct?",
                [
                    "Discount both for one year",
                    "Discount each from its own payment date",
                    "Add them without considering time",
                ],
                1,
                "Each cash flow has a different time to receipt and therefore a different discount factor.",
            ),
            q(
                "A single payment of 133.10 arrives in three years. At 10% annually its present value is:",
                ["100", "110", "121"],
                0,
                "133.10 / 1.10³ = 100, using three annual discount periods.",
            ),
        ],
    )

    add(
        "2.6",
        1,
        "Compounding, annuities, NPV, and IRR",
        "Compare effective rates and evaluate a project without confusing its return estimate with value added.",
        r"""
## Compounding conventions change the comparison

A quoted nominal annual rate compounded several times per year is not its effective annual rate. If the nominal rate is j and there are m equal compounding periods, each period earns j/m and the effective annual rate is (1 + j/m)^m − 1. Match the payment frequency to the rate used in an annuity calculation.

Net present value subtracts the initial cost from discounted future receipts. Internal rate of return is a rate making that NPV zero. IRR is useful for conventional cash-flow patterns, but multiple sign changes can produce multiple roots or no economically useful root. Projects of different size or timing can also rank differently by IRR and NPV.

A positive NPV is conditional on the projected cash flows and required return. It is not a promise of profit. Preserve the forecast assumptions and examine how much they can deteriorate before value is lost.

## A worked example

A nominal 12% annual rate compounded monthly has effective rate (1.01)^12 − 1 = 12.6825%. Treating it as exactly 12% understates annual compounding.

A project costs 100 now and pays 60 at each of the next two year ends. At 10%, NPV is −100 + 60/1.10 + 60/1.10² = 4.13. Its IRR is about 13.07%. The NPV answers how much value is added at the stipulated 10% requirement; IRR supplies the break-even rate.

## Diagnose before solving

Write the sign of every cash flow and identify whether the pattern is conventional. Compare mutually exclusive projects on a common basis appropriate to the decision. Reinvestment assumptions, project life, and capital constraints can matter.

When communicating the result, give both the monetary NPV and the assumptions that produce it. A percentage alone can conceal a small economic benefit or a fragile forecast.
""",
        r"EAR=(1+j/m)^m-1",
        'from math import sqrt\nprint("Effective annual rate (%):", ((1 + .12 / 12) ** 12 - 1) * 100)\nprint("Project NPV:", round(-100 + 60 / 1.1 + 60 / 1.1 ** 2, 2))\nprint("Project IRR (%):", ((60 + sqrt(60 ** 2 + 4 * 100 * 60)) / 200 - 1) * 100)',
        "Compute the effective rate for nominal 8% compounded quarterly. Calculate NPV of a cost of 100 followed by 55 at each of two year ends at 5%.",
        "Effective rate is 1.02⁴ − 1 = 8.2432%. NPV is −100 + 55/1.05 + 55/1.05² ≈ 2.27. The project passes the stipulated NPV rule if its forecasts and rate are appropriate.",
        [
            q(
                "Nominal 10% compounded semiannually has effective annual rate of:",
                ["10%", "10.25%", "20%"],
                1,
                "(1 + 0.10/2)² − 1 = 10.25%.",
            ),
            q(
                "Why inspect cash-flow signs before relying on IRR?",
                [
                    "Multiple sign changes can create multiple IRRs",
                    "IRR never depends on cash flows",
                    "Negative cash flows are always impossible",
                ],
                0,
                "Nonconventional cash-flow sequences can have multiple roots, so a single reported IRR can be misleading.",
            ),
            q(
                "A project costs 100 and returns 115 in one year. At a 10% required return, NPV is approximately:",
                ["15", "5", "4.55"],
                2,
                "115 / 1.10 − 100 = 4.55; discount the future receipt before comparing it with cost.",
            ),
        ],
    )

    add(
        "2.7",
        2,
        "Return measurement and data organization",
        "Build a clean return table and distinguish arithmetic, geometric, and log-return summaries.",
        r"""
## Define one observation

A dataset needs an observational unit: one asset-day, one company-year, or one transaction. Record identifiers, timestamps, currency, total-return treatment, and missing-value rules. A price return excludes distributions unless they are explicitly included. Split-adjusted prices and raw prices should not be mixed in one series.

Simple return is ending wealth divided by starting wealth minus one. Arithmetic mean summarizes the average one-period observation. Geometric mean is the constant compounded rate matching a sequence's terminal wealth. Log returns add across time for the same asset, but simple returns are generally needed for contemporaneous weighted portfolio returns.

Specify whether returns are decimals or percentage points. A decimal value of 0.02 means 2%. Applying a percentage conversion twice can produce errors much larger than any statistical refinement later in the process.

## A worked example

A hypothetical investment gains 20% and then loses 20%. Starting wealth of 100 becomes 120 and then 96. The arithmetic mean return is zero, but the two-period compounded return is −4%. The geometric mean is the square root of 0.96 minus one, about −2.02% per period.

The two log returns sum to log(0.96), about −0.04082. Exponentiating that sum and subtracting one returns the −4% total simple return. The transformations agree when their definitions are used consistently.

## Inspect before estimating

Sort observations by date, check duplicate asset-date keys, and distinguish absent observations from genuine zero returns. A market closure is not automatically a zero economic return observation at the frequency required by the model.

Keep an untouched source table and a documented transformation table. Later regression or machine learning cannot recover the intended meaning of data that were incorrectly joined, adjusted, or labeled at ingestion.
""",
        r"g=\left(\prod_{t=1}^{T}(1+r_t)\right)^{1/T}-1",
        'from math import sqrt, log\nprint("Terminal wealth:", 100 * 1.2 * .8)\nprint("Geometric mean (%):", (sqrt(1.2 * .8) - 1) * 100)\nprint("Sum of log returns:", log(1.2) + log(.8))',
        "A series returns +10% and −10%. Calculate terminal wealth from 200, arithmetic mean, and geometric mean. State a rule for missing observations.",
        "Wealth is 198, arithmetic mean 0%, geometric mean √0.99 − 1 ≈ −0.5013%. Missing observations need an explicit, economically justified treatment; do not automatically replace them with zero.",
        [
            q(
                "A +50% return followed by −50% changes wealth of 100 to:",
                ["100", "75", "50"],
                1,
                "100 × 1.5 × 0.5 = 75; equal percentage gains and losses do not cancel.",
            ),
            q(
                "Which return summary matches a sequence's compounded terminal wealth?",
                ["Geometric mean", "Arithmetic mean in every case", "Maximum one-period return"],
                0,
                "The geometric mean is the constant per-period rate producing the same wealth over the sequence.",
            ),
            q(
                "Returns are +25% then −20%. What is the total compounded return?",
                ["5%", "2.5%", "0%"],
                2,
                "1.25 × 0.80 = 1, so terminal wealth equals starting wealth despite a positive arithmetic mean.",
            ),
        ],
    )

    add(
        "2.8",
        2,
        "Describe distributions before fitting models",
        "Calculate dispersion and use distribution shape and visual checks to interrogate an average.",
        r"""
## A mean is only one description

Measures of center summarize location. Dispersion describes how widely observations vary. Skewness concerns asymmetry, while tail behavior concerns extreme outcomes. Two return samples can share a mean and standard deviation yet have very different downside experiences.

Sample variance uses n − 1 when estimating population variance from independent observations with an estimated mean. The sample standard deviation is its square root. A population description of a complete stipulated set uses a different denominator. State which question you are answering.

Use a histogram, time plot, and a simple table of quantiles before imposing a model. A histogram can conceal the order of events; a time plot can reveal changing volatility. An outlier may be a genuine event, a corporate action, or a data error. Investigate its origin before removing it.

## A worked example

A small sample of percentage-point returns is −2, 0, 2, and 4. The mean is 1. Deviations are −3, −1, 1, and 3; squared deviations sum to 20. Sample variance is 20/3 = 6.6667 squared percentage points, and sample standard deviation is about 2.582 percentage points.

If these four outcomes instead form an equally weighted, fully specified population, variance is 20/4 = 5 and standard deviation is about 2.236. The observations did not change; the estimation question did.

## Avoid cosmetic cleaning

Report how many observations were excluded and why. Winsorization replaces extreme values with boundaries; it changes the distribution and must be disclosed. It may improve stability for a purpose but can also conceal the very downside behavior a risk analysis needs to study.

A useful descriptive report includes count, units, frequency, center, dispersion, missingness, and extreme observations with their dates. That evidence helps determine which later model assumptions are plausible.
""",
        r"s^2=\sum(x_i-\bar{x})^2/(n-1)",
        'from math import sqrt\nx = [-2, 0, 2, 4]\nmean = sum(x) / len(x)\nsquared = 0\nfor v in x:\n    squared = squared + (v - mean) ** 2\nvariance = squared / (len(x) - 1)\nprint("Mean:", mean)\nprint("Sample standard deviation:", sqrt(variance))',
        "For observations 1, 3, and 5, calculate the mean and sample standard deviation. Explain why an isolated observation of 50 should be investigated before deletion.",
        "Mean is 3; squared deviations sum to 8; sample variance is 4 and standard deviation is 2. The observation 50 could be a genuine tail event or an error, and deleting it changes the risk description.",
        [
            q(
                "For sample observations 2, 4, and 6, sample variance is:",
                ["4", "8/3", "2"],
                0,
                "The mean is 4 and squared deviations sum to 8; divide by n − 1 = 2 to obtain 4.",
            ),
            q(
                "Which plot most directly preserves the sequence of volatility changes?",
                ["A histogram alone", "A time plot of returns", "A pie chart of ticker names"],
                1,
                "A time plot preserves chronological ordering, which a histogram discards.",
            ),
            q(
                "Two return series have identical means and standard deviations. What can still differ materially?",
                [
                    "Their sample units must differ",
                    "Nothing relevant to risk",
                    "Skewness, tails, and temporal dependence",
                ],
                2,
                "The first two moments do not determine every feature of a general return distribution.",
            ),
        ],
    )

    add(
        "2.9",
        3,
        "Conditional probability and Bayes updates",
        "Use a probability tree to update a prior belief without confusing conditional directions.",
        r"""
## Name the event and the information

An unconditional probability describes an event before the specified evidence. A conditional probability restricts attention to outcomes consistent with that evidence. The probability of a signal given distress is generally different from the probability of distress given a signal.

Use joint probabilities to keep the directions straight. Multiplying a prior probability by a conditional signal probability gives the joint probability of both events. Summing across mutually exclusive states gives the total probability of the signal. Dividing the relevant joint probability by that total produces the posterior.

A base rate matters. Even a fairly accurate warning can generate many false alarms when the event is rare. Posterior accuracy depends on the quality and relevance of both prior frequencies and the signal model.

## A worked example

In a fictional population, 10% of firms enter distress. A warning appears for 80% of distressed firms and 20% of nondistressed firms. Joint distress-and-warning probability is 0.10 × 0.80 = 0.08. Joint no-distress-and-warning probability is 0.90 × 0.20 = 0.18.

Total warning probability is 0.26. Conditional distress probability after a warning is 0.08/0.26 = 30.77%. It is neither the 80% signal sensitivity nor the 10% prior. The warning increases risk substantially while still producing more nondistressed than distressed firms among flagged observations.

## Check transferability

Ask whether the reference population resembles the current universe. A model calibrated on one industry or economic regime may have a different false-positive rate elsewhere. Treat supplied probabilities as assumptions in a case, not as universal characteristics of a financial ratio.

Draw the four cells of the joint table and check that their probabilities sum to one. This simple reconciliation prevents many interpretation errors before more elaborate modeling begins.
""",
        r"P(D\mid W)=P(W\mid D)P(D)/P(W)",
        'joint = .10 * .80\nwarning = joint + .90 * .20\nprint("Warning probability:", warning)\nprint("Distress given warning:", joint / warning)',
        "Prior distress is 20%. A warning occurs for 75% of distressed and 25% of nondistressed firms. Calculate the posterior and explain why it is not 75%.",
        "Joint distress-warning is 0.15; nondistress-warning is 0.20. Posterior is 0.15/0.35 = 42.86%. The 75% quantity conditions on distress, while the desired posterior conditions on seeing the warning.",
        [
            q(
                "If P(A)=0.2 and P(B|A)=0.5, P(A and B) is:",
                ["0.1", "0.4", "0.7"],
                0,
                "The joint probability is the prior multiplied by the conditional probability: 0.2 × 0.5.",
            ),
            q(
                "Why can a useful warning have many false alarms?",
                [
                    "Conditional probabilities must be equal",
                    "The event's base rate may be low",
                    "Bayes' rule ignores priors",
                ],
                1,
                "A large nondistressed population can generate many warnings even with a moderate false-positive rate.",
            ),
            q(
                "Prior distress is 25%; warning rates are 60% in distress and 20% otherwise. Posterior distress given warning is:",
                ["25%", "60%", "50%"],
                2,
                "Joint probabilities are 0.15 and 0.15, so posterior is 0.15 / 0.30 = 50%.",
            ),
        ],
    )

    add(
        "2.10",
        3,
        "Expected return, covariance, and diversification",
        "Combine state-dependent returns and explain how covariance changes portfolio uncertainty.",
        r"""
## Keep states aligned

Expected return is a probability-weighted average across stipulated outcomes. Variance measures squared deviations from that expectation. Covariance measures whether two variables tend to deviate in the same direction in the same states. Pairing observations from different dates can destroy the meaning of that relationship.

Portfolio expected return is the weighted average of component expectations. Portfolio variance also includes cross terms. A weighted average of individual variances alone misses the interaction between assets. Correlation is covariance divided by the product of standard deviations and has no units when both standard deviations are positive.

Diversification depends on imperfect co-movement, not simply the number of tickers. Several securities can share the same business or financing exposure. Estimated correlations can also change in adverse conditions.

## A worked example

Two assets have annual standard deviations of 20% and 10%, correlation of 0.25, and equal weights. Variance is 0.5² × 0.20² + 0.5² × 0.10² + 2 × 0.5 × 0.5 × 0.25 × 0.20 × 0.10 = 0.015. Volatility is √0.015 = 12.25%.

If expected returns are 8% and 4%, the expected portfolio return is 6%. With perfect positive correlation, volatility would be 15%, the weighted average of the two volatilities. The lower 12.25% result depends on the stated correlation assumption.

## Stress the dependence

Repeat the calculation for higher correlation and explain the economic scenario causing it. Covariance estimates from short samples can be unstable. A risk estimate should show its data window, frequency, and whether observations include stressed conditions.

Expected return and volatility are separate summaries. Neither establishes a guaranteed outcome or a complete description of downside risk, especially for asymmetric payoffs.
""",
        r"\sigma_p^2=w_1^2\sigma_1^2+w_2^2\sigma_2^2+2w_1w_2\rho\sigma_1\sigma_2",
        'from math import sqrt\nvariance = .5 ** 2 * .2 ** 2 + .5 ** 2 * .1 ** 2 + 2 * .5 * .5 * .25 * .2 * .1\nprint("Expected return:", .5 * .08 + .5 * .04)\nprint("Portfolio volatility:", sqrt(variance))',
        "Use equal weights in two assets each with 10% volatility. Calculate portfolio volatility at correlations of zero and one. Explain what independence would add beyond zero correlation.",
        "At zero correlation, variance is 0.005 and volatility 7.071%. At correlation one, volatility is 10%. Zero correlation means no linear covariance; it does not generally imply full probabilistic independence.",
        [
            q(
                "Equal weights in assets with expected returns 10% and 2% give expected portfolio return of:",
                ["4%", "6%", "12%"],
                1,
                "0.5 × 10% + 0.5 × 2% = 6%; covariance affects risk, not this weighted expectation.",
            ),
            q(
                "Zero correlation generally implies:",
                [
                    "Full independence in every distribution",
                    "No linear covariance, but possible nonlinear dependence",
                    "No investment risk",
                ],
                1,
                "Uncorrelated variables can still have nonlinear dependence unless stronger distributional assumptions apply.",
            ),
            q(
                "Two equally weighted assets each have 20% volatility and zero correlation. Portfolio volatility is approximately:",
                ["10%", "20%", "14.14%"],
                2,
                "Variance is 0.25×0.04 + 0.25×0.04 = 0.02; its square root is 14.14%.",
            ),
        ],
    )

    add(
        "2.2",
        4,
        "Probability distributions in finance",
        "Choose a distribution consistent with the variable and recognize when a normal model understates tail behavior.",
        r"""
## Match the model to the variable

A discrete distribution assigns probabilities to countable outcomes. A continuous distribution describes probability over intervals; its density at a point is not a point probability. Before selecting either, define the variable and its possible range.

A normal model is symmetric and unbounded. It can approximate some return behavior, but it permits values below −100% when used directly for simple returns. A lognormal price is positive because its logarithm is normal. Positive prices do not imply normally distributed simple returns.

The model is an assumption to test against the intended use. Real returns can have heavier tails, asymmetry, and changing volatility. A model that approximates the middle of a distribution may perform poorly for rare-loss decisions.

## A worked example

Suppose a stipulated one-day normal return has mean zero and standard deviation 1%. The 99% lower-tail loss threshold is approximately 2.326 standard deviations, or 2.326% of value. On a $100,000 position, that is about $2,326 under the model.

This threshold is not a maximum loss. The model itself assigns 1% probability to a worse daily outcome. If the actual distribution has heavier downside tails, the observed frequency and severity beyond the threshold can exceed the model's predictions.

For a separate positive-price model, let a log return equal −0.10. The simple return is exp(−0.10) − 1, approximately −9.52%, rather than exactly −10%.

## Inspect the consequences

Compare empirical tail quantiles with modeled ones and inspect the time pattern of large moves. A normal fit to pooled observations can disguise periods of very different risk. Stress the model using jumps or a mixture of volatility regimes and describe the resulting change in loss estimates.
""",
        r"R=e^{r_{log}}-1",
        'from math import exp\nprint("Normal 99% one-day loss threshold:", 100000 * 2.326 * .01)\nprint("Simple return from log return:", exp(-.10) - 1)',
        "At zero mean and 2% daily volatility, calculate the normal 95% loss threshold using z=1.645 on 50,000. Explain why the number is not a worst-case loss.",
        "The threshold is 50,000 × 1.645 × 0.02 = 1,645. Even the assumed normal distribution assigns 5% probability to a larger loss; model misspecification can further worsen outcomes.",
        [
            q(
                "Which observation most directly challenges a normal-return model?",
                [
                    "Positive asset prices",
                    "More extreme returns than the model predicts",
                    "Daily observations",
                ],
                1,
                "Excess tail events indicate that the normal model may understate extreme-outcome probability.",
            ),
            q(
                "A lognormal price model implies:",
                [
                    "The modeled price is positive",
                    "Its simple returns must be symmetric",
                    "Losses are impossible",
                ],
                0,
                "Exponentiating a real-valued normal variable gives a positive price, while negative returns remain possible.",
            ),
            q(
                "At zero mean, a normal loss threshold uses z=2 and volatility 1.5%. On 20,000, the threshold is:",
                ["300", "600", "3,000"],
                1,
                "20,000 × 2 × 0.015 = 600; this is a model quantile, not a maximum loss.",
            ),
        ],
    )

    add(
        "2.11",
        4,
        "Counts, joint models, and simulation logic",
        "Use a binomial model for repeated trials and identify the assumptions that financial dependence can violate.",
        r"""
## A count model has structural assumptions

A binomial count describes successes in a fixed number of independent trials with the same success probability. Its expected count is np and its variance is np(1 − p). These are consequences of the model, not properties of every observed count.

Financial events can cluster. Defaults can respond to a shared recession; trade outcomes can share a volatility regime. Independence can therefore be a particularly fragile assumption when counting adverse events. A correct binomial calculation can still give a poor risk estimate if its premise is wrong.

Simulation draws from an assumed model to approximate outcomes. It does not discover the correct distribution automatically. A reproducible simulation records its seed, parameters, number of draws, and summary error. More draws reduce Monte Carlo noise but do not remove model error.

## A worked example

Ten fictional independent loans each have a stipulated 2% default probability over one year. Expected defaults are 10 × 0.02 = 0.2. Probability of at least one default is 1 − 0.98^10 ≈ 18.29%. An expected count below one is compatible with a substantial chance of one or more events.

The binomial variance is 10 × 0.02 × 0.98 = 0.196. If defaults become positively dependent, the marginal expected count can remain 0.2 while the distribution of total losses changes materially. Joint assumptions matter beyond individual probabilities.

## Design a useful experiment

State the quantity being estimated before generating draws: a mean, a quantile, or a conditional loss. Compare a small independent case with an exact calculation to validate the simulator. Then introduce a shared adverse state and observe clustering.

Report both numerical uncertainty and structural uncertainty. A narrow Monte Carlo error bar should not be presented as confidence that the chosen economic model is correct.
""",
        r"P(X\geq1)=1-(1-p)^n",
        'n = 10\np = .02\nprint("Expected defaults:", n * p)\nprint("At least one default:", 1 - (1 - p) ** n)\nprint("Binomial variance:", n * p * (1 - p))',
        "For five independent trials with success probability 10%, calculate expected successes and probability of at least one. Name a condition that makes the binomial model unsuitable.",
        "Expected count is 0.5 and probability is 1 − 0.9⁵ = 40.951%. Dependence between trials or differing success probabilities violates the standard identical-independent binomial setup.",
        [
            q(
                "For 20 independent trials with p=0.05, expected successes are:",
                ["0.05", "1", "20"],
                1,
                "Expected binomial count is np = 20 × 0.05 = 1.",
            ),
            q(
                "Increasing simulation draws primarily reduces:",
                [
                    "Monte Carlo sampling noise",
                    "All economic model error",
                    "The true probability of loss",
                ],
                0,
                "More draws improve the approximation to the chosen model, but cannot establish that the model describes reality.",
            ),
            q(
                "Two independent events each have probability 20%. Probability of at least one is:",
                ["40%", "4%", "36%"],
                2,
                "1 − 0.8² = 36%; adding probabilities without subtracting overlap would double count joint occurrence.",
            ),
        ],
    )

    add(
        "2.3",
        5,
        "Sampling & confidence intervals",
        "Estimate sampling uncertainty and interpret a confidence interval without treating it as a posterior probability.",
        r"""
## The estimate changes across samples

A sample mean estimates a population mean. Under independent observations with finite variance, its standard error decreases approximately with the square root of sample size. More rows do not necessarily mean proportionally more information when observations are serially dependent or repeatedly describe the same exposure.

When population variance is unknown, a t interval uses the sample standard deviation and an appropriate t critical value. Small-sample exact coverage requires stronger distributional assumptions than a large-sample approximation. Specify sample size, frequency, and the population the sample is intended to represent.

A frequentist 95% confidence procedure covers the fixed parameter in 95% of repeated samples under its assumptions. After observing one interval, the usual frequentist statement is not that the fixed mean now has a 95% probability of lying inside it.

## A worked example

For 25 independent observations with mean return 1% and sample standard deviation 5%, standard error is 5%/√25 = 1%. Using a supplied 95% t critical value of 2.064, the interval is 1% ± 2.064%, or −1.064% to 3.064%.

The interval includes zero, so this two-sided procedure does not establish a positive population mean at that confidence level. It also permits economically meaningful positive and negative values. Failure to isolate a positive mean is not proof the true mean equals zero.

## Describe the sample's limits

Ask whether selection excluded failed funds, delisted securities, or unsuccessful strategies. A precise interval for a biased sample can be precisely wrong for the intended universe. Document the sampling frame before calculating a standard error.

For dependent returns, use a method that reflects dependence, such as an appropriate block-resampling procedure, and state its additional assumptions. Do not silently use the independent-observation formula because it is convenient.
""",
        r"\bar{x}\pm t^*s/\sqrt{n}",
        'from math import sqrt\nmean = .01\nse = .05 / sqrt(25)\nprint("Standard error:", se)\nprint("95% interval:", mean - 2.064 * se, mean + 2.064 * se)',
        "A mean is 2%, sample standard deviation 6%, and n=36. Using a supplied critical value of 2.03, compute an interval and explain the effect of quadrupling independent sample size.",
        "Standard error is 1%; the interval is −0.03% to 4.03%. Quadrupling independent sample size halves standard error, with other inputs held fixed; it does not automatically repair selection bias.",
        [
            q(
                "Quadrupling independent sample size, all else equal, changes standard error by:",
                ["Doubling it", "Halving it", "Leaving it unchanged"],
                1,
                "Standard error is proportional to 1/√n, so multiplying n by four divides it by two.",
            ),
            q(
                "An interval containing zero establishes:",
                [
                    "The true mean is exactly zero",
                    "The data and procedure do not exclude zero at that confidence level",
                    "Positive returns are impossible",
                ],
                1,
                "Not excluding zero is different from proving the parameter equals zero.",
            ),
            q(
                "Sample standard deviation is 8% and n=64 independent observations. Standard error of the mean is:",
                ["1%", "8%", "0.125%"],
                0,
                "8% / √64 = 1%; use the square root of sample size.",
            ),
        ],
    )

    add(
        "2.12",
        5,
        "Bootstrap, selection bias, and dependent samples",
        "Choose a resampling unit that respects the data and distinguish uncertainty estimation from bias correction.",
        r"""
## Resample the right object

The ordinary bootstrap repeatedly samples observations with replacement from the observed sample and recalculates an estimator. The variation across estimates approximates sampling uncertainty under suitable conditions. It relies on the observed sample representing the intended data-generating process.

For serially dependent observations, resampling individual days breaks time relationships. A block bootstrap resamples contiguous groups to preserve some local dependence. Block length creates a tradeoff: very short blocks lose dependence; very long blocks provide fewer distinct units of variation.

A bootstrap does not restore missing failed funds or historical firms removed by a survivor-only screen. It reproduces the sample supplied. Selection bias needs a better sampling frame or an explicit identification argument, not merely more resamples.

## A worked example

A return series is 1%, 1%, −1%, −1%, repeated twice. Its overall mean is zero, but adjacent observations tend to occur in same-sign pairs. Four nonoverlapping two-day blocks have means 1%, −1%, 1%, and −1%.

A case resample choosing the first positive block twice and the two negative blocks gives mean zero; choosing three positive blocks and one negative gives mean 0.5%. The point is the resampling unit: entire pairs remain intact. This tiny example illustrates mechanics and does not establish an optimal block length.

## Design the uncertainty report

Record the estimator, eligible observations, block construction, random seed, and resample count. Compare uncertainty under plausible block lengths and explain why the choice matches the dependence horizon. Keep overlapping labels and related entities in mind when defining groups.

A useful report separates sample uncertainty from coverage of the investment universe. Wide intervals indicate imprecision; a systematically selected universe can create bias even when intervals are narrow.
""",
        r"\hat\theta_b^*=f(\text{resampled blocks})",
        'blocks = [[.01, .01], [-.01, -.01], [.01, .01], [-.01, -.01]]\nselection = [0, 0, 2, 3]\ntotal = 0\ncount = 0\nfor i in selection:\n    for value in blocks[i]:\n        total = total + value\n        count = count + 1\nprint("Illustrative block-resample mean:", total / count)',
        "Explain how you would estimate uncertainty for monthly returns from funds that share a manager and include only surviving funds. Identify one dependence issue and one selection issue.",
        "Shared management may require grouping related funds or otherwise modeling cross-sectional dependence. Survivor-only inclusion omits failed funds and requires reconstruction of the historical universe; resampling survivors cannot fix that omission.",
        [
            q(
                "Resampling individual days from a serially dependent series can:",
                [
                    "Destroy the dependence structure",
                    "Always preserve all clusters",
                    "Recover missing failed firms",
                ],
                0,
                "Independent day draws break neighboring relationships that may determine estimator uncertainty.",
            ),
            q(
                "Which problem is not repaired by simply increasing bootstrap draws?",
                [
                    "Monte Carlo noise alone",
                    "Omission of failed funds from the sample",
                    "The number of computed resample means",
                ],
                1,
                "More resamples cannot add excluded observations or correct the sampling frame by themselves.",
            ),
            q(
                "A researcher resamples complete five-day blocks instead of individual days. The primary purpose is to:",
                [
                    "Guarantee positive returns",
                    "Preserve some local serial dependence",
                    "Remove every source of bias",
                ],
                1,
                "Keeping contiguous groups maintains some time relationships that an independent daily bootstrap would discard.",
            ),
        ],
    )

    add(
        "2.4",
        6,
        "Hypothesis testing in markets",
        "Specify a null, interpret a test statistic and p-value, and separate statistical from economic significance.",
        r"""
## State the claim before seeing the result

A hypothesis test compares observed evidence with a specified null model. Define the parameter, null and alternative, direction of the test, significance threshold, and sampling assumptions before inspecting the outcome. Choosing a one-sided test after observing the sign changes the actual error rate.

A p-value is the probability, under the null and model assumptions, of a test statistic at least as extreme as observed according to the chosen test. It is not the probability that the null is true or that a trading strategy will fail.

A Type I error rejects a true null. A Type II error fails to reject a false null. Power is the probability of rejecting at a specified alternative. Smaller economically relevant effects generally require more information to detect reliably.

## A worked example

A strategy's mean monthly excess return is 0.4%, sample standard deviation 2%, and sample size 100 independent months. Standard error is 0.2%. Testing a zero mean gives t = 0.4/0.2 = 2. With a supplied two-sided critical value of 1.984, the statistic exceeds the threshold.

Now suppose expected implementation costs are 0.5% per month. The observed gross mean minus costs is −0.1%. A statistically significant gross mean does not imply a useful net investment opportunity. If returns are dependent, even the original standard error may be inappropriate.

## Communicate the evidence honestly

Report the estimate, interval, assumptions, sample, and all material trials. Describe a failure to reject as insufficient evidence against the null under the procedure. Avoid interpreting it as proof of no effect.

A research decision should combine statistical evidence, economic magnitude, costs, and the plausibility of the proposed mechanism. No single threshold replaces that reasoning.
""",
        r"t=(\bar{x}-\mu_0)/(s/\sqrt{n})",
        'from math import sqrt\nmean = .004\nse = .02 / sqrt(100)\nprint("t statistic:", mean / se)\nprint("Mean after assumed costs:", mean - .005)',
        "A mean is 0.3%, standard deviation 3%, and n=100 independent periods. Calculate the statistic against zero and compare with a supplied two-sided threshold of 1.984.",
        "Standard error is 0.3% and t=1. The statistic does not exceed 1.984, so fail to reject under the stated procedure. This is not proof that the true mean is zero.",
        [
            q(
                "A Type I error is:",
                ["Failing to reject a false null", "Rejecting a true null", "Using a small sample"],
                1,
                "Type I error is a false rejection; its control depends on the test and its assumptions.",
            ),
            q(
                "A p-value of 0.03 means:",
                [
                    "The null is 3% likely",
                    "Under the null model, the specified tail event has probability 3%",
                    "A 97% chance the strategy will profit",
                ],
                1,
                "The p-value conditions on the null and measures extremeness of data, not the posterior probability of the null.",
            ),
            q(
                "A mean of 0.6% has standard error of 0.2%. Its statistic against a zero mean is:",
                ["0.3", "2", "3"],
                2,
                "0.6% / 0.2% = 3, using consistent units for estimate and standard error.",
            ),
        ],
    )

    add(
        "2.13",
        6,
        "Multiple testing and robust comparisons",
        "Control a family of research trials and choose a comparison that matches paired or independent observations.",
        r"""
## A research program is larger than its winning test

Trying many strategies increases the chance of a false discovery. Under twenty independent true nulls each tested at 5%, probability of at least one false rejection is 1 − 0.95^20, about 64.15%. Correlated tests change this exact calculation but do not remove the need to account for the research family.

A Bonferroni procedure tests each of m hypotheses at alpha/m to control family-wise error under valid individual tests. It does not require independent tests, but can be conservative. False-discovery-rate procedures target a different error criterion and should not be described as guaranteeing no false positives.

Choose the comparison unit carefully. Comparing two strategies over the same months often calls for analyzing monthly return differences. Treating the two aligned samples as unrelated discards their covariance. Rank-based methods can be useful for some distributional questions, but they also have assumptions and are not universal substitutes for mean tests.

## A worked example

A team predefines ten strategy variants and wants a 5% family-wise threshold using Bonferroni. Each individual threshold is 0.005. The best unadjusted p-value is 0.012, which does not pass. Reporting only that it is below 0.05 hides the number of opportunities to find a favorable result.

For two paired strategies, monthly differences are 1, −1, 2, and 0 percentage points. Their mean difference is 0.5 points. The inferential object is the distribution of those paired differences, not the two standalone mean estimates considered without their covariance.

## Preserve the research history

Log abandoned variants, data filters, and parameter searches. Reserve final evaluation data and avoid using its results to select another model. An untouched holdout loses that status once it drives a revision.

State the effect size worth detecting and how the error-control choice affects power. A disciplined process can conclude that the current evidence is insufficient despite an attractive backtest.
""",
        r"\alpha_{individual}=\alpha_{family}/m",
        'print("At least one false positive:", 1 - .95 ** 20)\nprint("Bonferroni threshold:", .05 / 10)\ndifferences = [1, -1, 2, 0]\nprint("Mean paired difference:", sum(differences) / len(differences))',
        "You predefine 25 tests and use Bonferroni at a 5% family-wise level. Does a p-value of 0.004 pass? Explain why repeatedly checking a holdout after revisions is a problem.",
        "The individual threshold is 0.002, so 0.004 fails. Repeated holdout-guided revision turns evaluation data into development information and invalidates the claim that it remains untouched.",
        [
            q(
                "Bonferroni at family alpha 0.05 across five tests uses threshold:",
                ["0.25", "0.05", "0.01"],
                2,
                "Divide the family threshold by the number of tests: 0.05 / 5 = 0.01.",
            ),
            q(
                "Two strategies are observed over the same months. A natural comparison starts with:",
                [
                    "Their paired monthly return differences",
                    "Unrelated random dates",
                    "Only the larger standalone Sharpe",
                ],
                0,
                "Paired differences preserve same-period covariance and target their relative performance.",
            ),
            q(
                "Twenty predefined tests use Bonferroni with a 5% family threshold. Which p-value passes?",
                ["0.003", "0.002", "0.02"],
                1,
                "The individual threshold is 0.0025, so only 0.002 among these choices passes.",
            ),
        ],
    )

    add(
        "2.5",
        7,
        "Linear regression & correlation",
        "Fit a single-factor relationship and interpret slope, intercept, and unexplained variation.",
        r"""
## Define the conditional relationship

A simple linear regression models y as an intercept plus a slope times x plus an error. Ordinary least squares chooses coefficients that minimize squared residuals. The slope measures fitted change in y for one unit of x; correlation standardizes association and is not generally the same number.

For an asset-pricing application, align asset and market returns over the same dates and subtract the same-period risk-free return from each. The intercept then describes an estimated return unexplained by this particular factor model. It is not automatically manager skill or a causal effect.

R-squared describes the share of in-sample variation around the dependent variable's mean explained by the fitted model when an intercept is included. A high value does not establish causation or future predictive performance.

## A worked example

Market excess returns in percentage points are −2, 0, and 2. Asset excess returns are −1, 1, and 3. The fitted line is asset return = 1 + 1 × market return: slope 1, intercept 1 percentage point, and zero residuals in this deliberately exact three-point example.

In a more realistic report, estimated daily alpha might be 0.02% with standard error 0.03%. Its t statistic is about 0.67. A positive coefficient with this uncertainty is weak evidence against a zero intercept. Sample size, model omissions, and costs remain relevant.

## Separate fit from explanation

Draw the scatterplot, inspect residuals, and identify observations with unusually large influence. Financial series can share trends or common omitted factors. A fitted relationship may change when the investment regime changes.

Write the slope's units in words. If beta is 1.2, a one-percentage-point change in market excess return is associated with about 1.2 percentage points in the fitted asset excess return, holding the simple model fixed.
""",
        r"\hat\beta=\sum(x_i-\bar x)(y_i-\bar y)/\sum(x_i-\bar x)^2",
        'x = [-2, 0, 2]\ny = [-1, 1, 3]\nxm = sum(x) / len(x)\nym = sum(y) / len(y)\ncross = 0\nsquares = 0\nfor i in range(len(x)):\n    cross = cross + (x[i] - xm) * (y[i] - ym)\n    squares = squares + (x[i] - xm) ** 2\nbeta = cross / squares\nprint("Beta:", beta)\nprint("Intercept:", ym - beta * xm)',
        "For x = −1, 0, 1 and y = −1, 1, 3, calculate slope and intercept. Explain why an exact fit to three observations is insufficient evidence of a durable opportunity.",
        "The line is y = 1 + 2x. The deliberately small sample provides little evidence of stability, causality, or performance after costs on future observations.",
        [
            q(
                "A beta of 1.2 primarily describes:",
                [
                    "Fitted market sensitivity",
                    "A guaranteed 20% excess return",
                    "The fraction of winning trades",
                ],
                0,
                "Beta is the slope on benchmark excess returns, not a guaranteed payoff.",
            ),
            q(
                "A high in-sample R-squared establishes:",
                [
                    "Causation",
                    "A high proportion of explained sample variation under the model",
                    "Guaranteed forecasting accuracy",
                ],
                1,
                "R-squared measures sample fit and cannot by itself establish cause or future performance.",
            ),
            q(
                "A fitted model is y = 0.5 + 1.5x, with both returns in percentage points. At x=2 the prediction is:",
                ["3", "2.5", "3.5"],
                2,
                "0.5 + 1.5 × 2 = 3.5 percentage points; retain the intercept.",
            ),
        ],
    )

    add(
        "2.14",
        7,
        "Regression uncertainty and prediction intervals",
        "Distinguish uncertainty in a fitted mean from uncertainty in a new individual outcome.",
        r"""
## A line is an estimate

Estimated regression coefficients vary across samples. Their standard errors describe sampling uncertainty under a stated error model. A coefficient's t statistic divides its estimated difference from the null value by its standard error. Coefficient size alone cannot establish precision.

A confidence interval for the conditional mean describes uncertainty in the fitted average outcome at a specified x. A prediction interval for a new observation includes both uncertainty in that mean and the new observation's residual variation. Under the same model and confidence level, the prediction interval is wider.

Both intervals become more fragile when extrapolating beyond the observed range. More sample observations near the center do not establish that a linear relationship continues far outside the data.

## A worked example

A fitted response at a selected market return is 2 percentage points. The standard error of its estimated conditional mean is 0.4 points. With a supplied critical value of 2, a mean-response interval is 1.2 to 2.8 points.

Suppose the residual standard deviation relevant to a new observation is 1.5 points. The simplified prediction standard error is √(0.4² + 1.5²) ≈ 1.552. The prediction interval is approximately −1.10 to 5.10 points. The fitted average is relatively precise while an individual result remains highly uncertain.

## Report what is being predicted

Specify whether the recipient wants an average response or a possible range for one future outcome. Label the interval accordingly. Also state whether the model assumes constant residual variance and independent errors.

A narrow confidence interval around an estimated alpha does not bound next month's return. The difference matters directly when translating a statistical model into a risk or position-sizing decision.
""",
        r"SE_{prediction}=\sqrt{SE_{mean}^2+s_{residual}^2}",
        'from math import sqrt\nmean = 2\nse_mean = .4\nse_prediction = sqrt(se_mean ** 2 + 1.5 ** 2)\nprint("Mean-response interval:", mean - 2 * se_mean, mean + 2 * se_mean)\nprint("Prediction interval:", mean - 2 * se_prediction, mean + 2 * se_prediction)',
        "A predicted mean is 1, mean-response standard error 0.3, residual standard deviation 0.4, and critical value 2. Compute both intervals and explain the extra uncertainty.",
        "Mean-response interval is 0.4–1.6. Prediction standard error is √(0.09 + 0.16) = 0.5, giving 0–2. The new observation adds residual uncertainty beyond uncertainty in the fitted average.",
        [
            q(
                "Which interval includes a new observation's residual variation?",
                [
                    "Prediction interval",
                    "Only the coefficient estimate",
                    "A mean-response interval alone",
                ],
                0,
                "A prediction interval includes the new outcome's noise as well as uncertainty in its fitted mean.",
            ),
            q(
                "Extrapolating far beyond observed x values primarily adds concern about:",
                [
                    "Whether the fitted relationship continues outside the data",
                    "The color of residuals",
                    "The number of decimal places",
                ],
                0,
                "The model's functional relationship may not remain valid in a region unsupported by observations.",
            ),
            q(
                "Mean-response standard error is 0.6 and residual standard deviation is 0.8. Simplified prediction standard error is:",
                ["0.2", "1", "1.4"],
                1,
                "√(0.6² + 0.8²) = 1; variances add under the stated decomposition.",
            ),
        ],
    )

    add(
        "2.15",
        8,
        "Multiple regression and categorical effects",
        "Interpret a coefficient conditional on other regressors and construct an identifiable model specification.",
        r"""
## A coefficient depends on the model around it

Multiple regression includes several explanatory variables. Each slope describes the fitted association with one regressor holding the others fixed. Adding or removing a correlated explanatory variable can change the estimated coefficients substantially.

A categorical variable can be represented with indicator variables. With an intercept, include a reference category rather than all mutually exclusive category indicators; otherwise the design contains exact linear dependence. An interaction term allows a slope to differ across a specified condition.

Interpretation still requires assumptions. Omitted variables correlated with included regressors and the outcome can bias a causal interpretation. A statistically useful prediction model does not automatically identify an intervention's effect.

## A worked example

A fictional monthly return model in percentage points is y = 0.2 + 1.1 × market + 0.4 × value + 0.3 × sector_indicator. For market = 2, value = −1, and sector_indicator = 1, fitted return is 0.2 + 2.2 − 0.4 + 0.3 = 2.3 points.

The sector coefficient means a fitted 0.3-point difference from the omitted reference category at the same market and value inputs. It does not prove that changing a firm's sector label would cause its return to rise.

## Specify before comparing

Record the dependent variable, units, intercept treatment, reference category, and economic reason for each regressor. Keep train and evaluation periods consistent across candidate specifications.

An apparently impressive fit can result from too many parameters relative to observations. Adjusted R-squared penalizes parameter count in sample, but a separate chronological evaluation remains necessary for a forecasting claim. A parsimonious model with stable performance can be more useful than a complex model whose coefficients change with small data revisions.
""",
        r"y=\beta_0+\beta_1x_1+\cdots+\beta_kx_k+\epsilon",
        'market = 2\nvalue = -1\nsector = 1\nprint("Fitted return (percentage points):", .2 + 1.1 * market + .4 * value + .3 * sector)',
        "For y = 1 + 2x − 0.5z + 0.4D, predict at x=3, z=2, D=1. Explain how three mutually exclusive sector categories should be encoded when an intercept is present.",
        "Prediction is 6.4. Use two indicators and one reference category with the intercept; including all three indicators creates exact linear dependence.",
        [
            q(
                "A multiple-regression slope is interpreted:",
                [
                    "Holding included other regressors fixed",
                    "Ignoring the other variables entirely",
                    "As guaranteed causation",
                ],
                0,
                "The fitted partial association is conditional on the other variables in the specified model.",
            ),
            q(
                "With an intercept and four mutually exclusive categories, a standard reference encoding uses:",
                [
                    "Four indicators plus the intercept",
                    "Three indicators",
                    "No possible indicators",
                ],
                1,
                "One category is omitted as reference to avoid exact dependence with the intercept.",
            ),
            q(
                "For y=1+0.5x+2z, x=4 and z=−1 give a prediction of:",
                ["5", "3", "1"],
                2,
                "1 + 0.5×4 + 2×(−1) = 1 in the stated response units.",
            ),
        ],
    )

    add(
        "2.16",
        8,
        "Diagnostics: unstable coefficients and invalid standard errors",
        "Identify multicollinearity, heteroskedasticity, serial correlation, and influential observations.",
        r"""
## Different defects require different responses

Multicollinearity means explanatory variables overlap strongly in their linear information. It can make individual coefficient estimates unstable and imprecise even when overall fit is high. Exact dependence prevents a unique ordinary least-squares solution without changing the specification.

Heteroskedasticity means residual variance changes with regressors or conditions. Serial correlation means errors are related across time. Either can invalidate conventional standard errors under the usual textbook assumptions. Appropriate robust covariance estimates address aspects of uncertainty; they do not fix omitted-variable bias or a wrong functional form.

An influential observation can move the fitted model materially. Influence depends on both unusual regressor values and residual behavior. Investigate the observation's origin before removing it. A genuine crisis observation may be particularly important for the intended investment use.

## A worked example

A fitted slope is 0.30. Its conventional standard error is 0.10, giving a statistic of 3.0 against zero. A dependence-aware estimate of standard error is 0.20, giving a statistic of 1.5. The point estimate is unchanged, but the evidence of precision is weaker under the revised error treatment.

Suppose two explanatory variables are almost copies of one another. Their separate slopes can swing between samples while their combined prediction remains similar. Interpreting either unstable slope as a reliable isolated economic effect would be misleading.

## Build a diagnostic sequence

Inspect residuals against fitted values and time, check regressor relationships, and review sensitivity to influential observations. Decide whether the goal is explanation, prediction, or risk estimation before choosing remedies.

Report what a correction changes. Replacing standard errors is not the same as refitting the conditional mean, and adding regressors is not the same as obtaining new information. The final interpretation must match the actual procedure used.
""",
        r"t=\hat\beta/SE(\hat\beta)",
        'coefficient = .30\nprint("Conventional statistic:", coefficient / .10)\nprint("Dependence-aware statistic:", coefficient / .20)',
        "A coefficient is 0.24 with conventional standard error 0.08 and robust standard error 0.16. Compare statistics and explain one problem robust standard errors do not solve.",
        "The statistics are 3 and 1.5. Robust uncertainty estimates do not by themselves repair omitted-variable bias, look-ahead data, or a misspecified conditional mean.",
        [
            q(
                "Strongly overlapping regressors can produce:",
                [
                    "Unstable individual coefficients",
                    "Guaranteed causal identification",
                    "Zero sampling uncertainty",
                ],
                0,
                "Multicollinearity makes it difficult to distinguish separate partial effects from similar information.",
            ),
            q(
                "Robust standard errors automatically fix:",
                [
                    "Omitted-variable bias",
                    "Every model defect",
                    "Neither omitted-variable bias nor data leakage",
                ],
                2,
                "They address specified covariance assumptions, not the validity of the data or identification of the mean relationship.",
            ),
            q(
                "A coefficient is 0.5 with revised standard error 0.25. Its statistic against zero is:",
                ["0.125", "2", "4"],
                1,
                "0.5 / 0.25 = 2; the revised uncertainty must be used in the statistic.",
            ),
        ],
    )

    add(
        "2.17",
        9,
        "Time-series dependence and stationarity",
        "Distinguish a stable autoregressive process from a unit-root process and avoid spurious level regressions.",
        r"""
## Time order contains information

A time series has a sequence, and neighboring observations may be related. Weak stationarity requires a constant mean, constant finite variance, and covariances depending on lag rather than calendar time. Many simple forecasting and uncertainty procedures rely on some form of stability.

An AR(1) model writes the current value as an intercept plus phi times the previous value plus an innovation. With suitable innovations and absolute phi below one, the stationary mean is intercept divided by one minus phi. A unit-root case with phi equal to one does not have this stable finite long-run mean under the same construction.

Regressing unrelated trending levels can produce a high apparent fit. Differencing can remove a unit-root trend in some cases, but it changes the modeled object. Cointegration concerns particular stationary combinations of nonstationary series and requires its own evidence; a high correlation in levels does not establish it.

## A worked example

Let x_t = 0.2 + 0.8x_(t−1) + error, with mean-zero innovations. The implied stationary mean is 0.2/(1 − 0.8) = 1. Starting from x=2, the one-step conditional forecast is 1.8. The next is 0.2 + 0.8×1.8 = 1.64, moving toward the model mean.

If phi were one, the denominator in the stationary-mean expression would be zero. Applying the same formula anyway would conceal a different process rather than solve it.

## Check stability before interpretation

Plot levels and changes, inspect autocorrelations, and consider structural breaks. A process can be stable over one window and unstable across a policy or business change. Statistical tests have finite-sample limitations and should be interpreted alongside the data-generating story.

Document whether the forecast targets a level, change, return, or spread. These distinctions determine how a prediction becomes a cash-flow or trading decision.
""",
        r"E[x]=c/(1-\phi),\quad |\phi|<1",
        'intercept = .2\nphi = .8\nvalue = 2\nprint("Stationary mean:", intercept / (1 - phi))\nfor step in range(3):\n    value = intercept + phi * value\n    print("Forecast:", value)',
        "For x_t = 0.3 + 0.5x_(t−1) + error, calculate the stationary mean and one-step forecast from x=1.2. Explain why phi=1 changes the analysis.",
        "Mean is 0.6 and forecast 0.9. At phi=1 the stationary-mean formula is undefined; the process lacks the same mean-reverting structure and requires a different treatment.",
        [
            q(
                "For a conventional stationary AR(1), the coefficient must satisfy:",
                ["|phi| < 1", "phi = 1", "phi > 1"],
                0,
                "Under the usual innovation assumptions, an absolute autoregressive coefficient below one permits a stationary solution.",
            ),
            q(
                "A high R-squared between unrelated trending levels may indicate:",
                ["Certain causation", "A spurious regression", "A verified trading edge"],
                1,
                "Common trending behavior can produce misleading sample fit without an economically valid stable relationship.",
            ),
            q(
                "In x_t=0.4+0.6x_(t−1)+error, the stationary mean is:",
                ["0.4", "0.6", "1"],
                2,
                "0.4 / (1 − 0.6) = 1 under the stated stationary model.",
            ),
        ],
    )

    add(
        "2.18",
        9,
        "Forecast evaluation and changing volatility",
        "Evaluate forecasts chronologically and distinguish conditional volatility from an unconditional average.",
        r"""
## A forecast must precede its outcome

For each forecast, record the estimation cutoff and the future period being predicted. Rolling estimation uses a moving historical window; expanding estimation retains the growing past. Neither permits future observations to enter model fitting, scaling, or feature construction.

Evaluate errors on observations excluded from estimation. Mean absolute error weights deviations linearly; mean squared error penalizes large errors more strongly. Compare against a simple forecast appropriate to the variable, such as a historical mean or a no-change level forecast.

Financial volatility often changes over time. A simple exponentially weighted variance update gives more weight to recent squared innovations. This is a conditional risk estimate, not a claim that the series has a constant unconditional variance or normal tails.

## A worked example

Forecast errors in percentage points are 1, −2, and 1. Mean absolute error is 4/3 = 1.333 points; root mean squared error is √(6/3) = 1.414 points. A model with a lower training error can still have a higher value of either metric on future observations.

For an illustrative variance update, previous daily variance is 0.0001, the most recent zero-mean return is 0.02, and decay is 0.94. New variance is 0.94×0.0001 + 0.06×0.02² = 0.000118, giving volatility about 1.086%. The recent larger move raises the estimate.

## Audit the chronology

A rolling study should fit each model using only information available at that forecast origin. If hyperparameters are selected, reserve an earlier validation process within the available history. Report the final evaluation once and retain unfavorable periods.

Explain what a lower statistical error means economically. A small improvement may not survive transaction costs or correspond to a useful decision boundary.
""",
        r"\sigma_t^2=\lambda\sigma_{t-1}^2+(1-\lambda)\epsilon_{t-1}^2",
        'from math import sqrt\nerrors = [1, -2, 1]\nabsolute = 0\nsquared = 0\nfor error in errors:\n    absolute = absolute + abs(error)\n    squared = squared + error ** 2\nprint("MAE:", absolute / len(errors))\nprint("RMSE:", sqrt(squared / len(errors)))\nprint("Updated volatility:", sqrt(.94 * .0001 + .06 * .02 ** 2))',
        "Forecast errors are 0, 0, and 3. Calculate MAE and RMSE. Explain why a random row split may be unsuitable for a forecasting study.",
        "MAE is 1 and RMSE is √3 ≈ 1.732. Random splits can put future information into training and mix dependent observations across evaluation boundaries.",
        [
            q(
                "Which model-evaluation split best reflects a forward forecast?",
                [
                    "Train on later dates and test earlier",
                    "Train on earlier dates and evaluate later dates",
                    "Select only dates with positive outcomes",
                ],
                1,
                "Forecast evaluation must respect the information set available before the predicted outcomes.",
            ),
            q(
                "RMSE compared with MAE places relatively more emphasis on:",
                ["Large errors", "Ticker symbols", "Only the sign of the mean"],
                0,
                "Squaring errors increases the relative penalty for large deviations before the square root restores units.",
            ),
            q(
                "Errors are −2 and 2. Their RMSE is:",
                ["0", "4", "2"],
                2,
                "Mean squared error is (4 + 4)/2 = 4, so RMSE is 2 despite zero mean error.",
            ),
        ],
    )

    add(
        "2.19",
        10,
        "Machine learning: objectives, validation, and regularization",
        "Define a learning task and control model complexity without allowing the test set to guide development.",
        r"""
## Begin with the decision and the label

Supervised learning uses observed outcomes to learn a predictive relationship. Regression predicts a numerical target; classification predicts a class or its probability. Unsupervised methods seek structure without a supplied outcome label. Select the task according to the investment decision rather than the popularity of an algorithm.

A label must specify horizon and availability. Predicting next month's return requires features known before that month. A company's eventual annual result cannot be a feature merely because it appears in a table indexed by the earlier fiscal year.

Split development into training and validation, then reserve a final test. Regularization penalizes complexity to trade some training fit for potential stability. Ridge uses a squared-coefficient penalty; lasso uses an absolute-coefficient penalty and can set some coefficients to zero. Scaling matters because penalties depend on coefficient units.

## A worked example

Two candidate models are compared using an illustrative objective equal to training mean squared error plus 0.1 times the sum of squared coefficients. Model A has training error 0.8 and squared-coefficient sum 1, giving objective 0.9. Model B has error 0.6 and coefficient sum 9, giving objective 1.5.

The penalty favors A despite its worse raw training fit. This arithmetic does not establish that A predicts better: validate that on earlier held-out chronological data. Select the penalty using the development process, then evaluate the frozen choice on the final period.

## Match complexity to evidence

Trees can capture nonlinear interactions; ensembles combine learners; more flexible models can also memorize noise. Compare each candidate with a simple baseline and document the search space. Fit scalers, imputers, and feature selectors on training observations only.

A model is an investment tool only after its predictions are connected to feasible decisions, costs, and risk. Good statistical fit alone is an incomplete objective.
""",
        r"L_{ridge}=MSE+\lambda\sum_j\beta_j^2",
        'penalty = .1\nprint("Model A penalized objective:", .8 + penalty * 1)\nprint("Model B penalized objective:", .6 + penalty * 9)',
        "Compare model C with MSE 0.5 and squared-coefficient sum 4 against D with MSE 0.7 and sum 1, using lambda 0.1. Describe which dataset may select lambda.",
        "C has objective 0.9; D has 0.8. Select lambda using training/validation procedures within the development period, never by repeatedly optimizing against the final test results.",
        [
            q(
                "Which transformation should be fitted using training data only?",
                ["A feature scaler", "The final test outcome itself", "The future realized return"],
                0,
                "Scaling parameters estimated on future evaluation rows can leak information into model development.",
            ),
            q(
                "A ridge penalty directly discourages:",
                [
                    "Large squared coefficient magnitudes",
                    "Every prediction error equally without fitting",
                    "Only negative coefficients",
                ],
                0,
                "The squared-coefficient term penalizes large magnitudes regardless of sign.",
            ),
            q(
                "A model has MSE 0.4, squared-coefficient sum 5, and lambda 0.2. Its stipulated penalized objective is:",
                ["0.6", "1.4", "5.4"],
                1,
                "0.4 + 0.2×5 = 1.4 under the stated objective convention.",
            ),
        ],
    )

    add(
        "2.20",
        10,
        "Classification, clustering, and economic evaluation",
        "Read a confusion matrix and explain why accuracy alone can be misleading for rare financial events.",
        r"""
## The class balance changes the meaning of success

Accuracy is the fraction of all classifications that are correct. For a rare event, predicting the common class every time can produce high accuracy while finding none of the events of interest. Precision asks how many predicted positives are truly positive. Recall asks how many actual positives were found.

The threshold converting a predicted probability into a decision controls the tradeoff between false positives and false negatives. Choose it with attention to their economic consequences. Probability calibration is a separate question: do events occur at approximately the probabilities assigned to them?

Unsupervised clustering groups similar observations according to a chosen distance and representation. The groups are not automatically economic regimes or causal categories. Principal components provide a lower-dimensional linear representation of variance; high explained variance is not the same as high predictive value.

## A worked example

A warning system examines 100 firms, of which 10 later enter distress. It flags 12 firms: 6 truly distressed and 6 not distressed. Four distressed firms are missed, while 84 nondistressed firms are correctly unflagged.

Accuracy is (6 + 84)/100 = 90%. Precision is 6/12 = 50%; recall is 6/10 = 60%. A model that never warns also has 90% accuracy here, but recall of zero. Which system is useful depends on the cost of missed distress and the cost of reviewing false alarms.

## Compare useful decisions

Evaluate thresholds on development data, then report the frozen threshold's results on a later sample. Track class prevalence because it can change precision even when conditional detection rates are stable.

For a clustering exercise, inspect which variables define the groups and whether the representation remains stable across periods. Give clusters descriptive interpretations only after examining their contents. Naming a cluster a crisis regime does not validate a forecast.
""",
        r"Precision=TP/(TP+FP);\quad Recall=TP/(TP+FN)",
        'tp = 6\nfp = 6\nfn = 4\ntn = 84\nprint("Accuracy:", (tp + tn) / (tp + fp + fn + tn))\nprint("Precision:", tp / (tp + fp))\nprint("Recall:", tp / (tp + fn))',
        "A model has TP=8, FP=2, FN=12, TN=78. Calculate accuracy, precision, and recall. Explain whether a higher classification threshold is likely to improve recall.",
        "Accuracy is 86%, precision 80%, recall 40%. A higher threshold generally flags fewer observations and tends to reduce recall; the actual tradeoff must be measured on appropriate data.",
        [
            q(
                "Ten true positives and ten false positives imply precision of:",
                ["100%", "50%", "10%"],
                1,
                "Precision is 10/(10+10) = 50%; it conditions on predicted positives.",
            ),
            q(
                "For a rare adverse event, high accuracy alone can conceal:",
                [
                    "Failure to identify almost every adverse event",
                    "Perfect probability calibration",
                    "Guaranteed economic usefulness",
                ],
                0,
                "A classifier can be accurate by always choosing the prevalent class while missing the rare event.",
            ),
            q(
                "A classifier finds 9 of 15 actual positives. Recall is:",
                ["40%", "60%", "90%"],
                1,
                "Recall is true positives divided by all actual positives: 9/15 = 60%.",
            ),
        ],
    )

    add(
        "2.21",
        11,
        "Point-in-time data engineering",
        "Build an auditable dataset with explicit keys, availability timestamps, and safe joins.",
        r"""
## A data pipeline is part of the model

Define the economic entity and observational key before joining tables. Ticker symbols can change or be reused. A stable entity identifier, security identifier, and timestamp often answer different questions. Corporate actions and multiple share classes require a clear mapping.

A dataset needs both an observation period and an availability time. Accounting values describe a period but are released later. Revised macroeconomic data may differ from the original release. A historical model should use the version actually available at the decision time.

Joining a price table with multiple matching records can multiply rows and distort returns or weights. Check uniqueness before and after each join. Missing data should carry a reason where possible: not yet reported, unavailable, not applicable, or removed by a defined filter.

## A worked example

A fictional December 31 financial statement is published on March 15. A February 1 signal cannot use it. If the previous available filing was published November 10, the February decision must use that older eligible information under a last-available-filing rule.

Suppose a price table has 100 unique security-date rows and a naive join produces 120 rows. The extra rows are not new market observations. Investigate duplicate keys or one-to-many mappings before calculating any portfolio statistic.

## Build a provenance checklist that can be rerun

Record source, retrieval date, observation period, availability timestamp, revision identifier, units, and transformations. Reconcile row counts, unique keys, missingness, and a few independently checked values at every stage.

A model trained on a clean-looking but historically impossible dataset can produce impressive false evidence. Data validation should therefore include chronology and meaning, not just file formats. Preserve a frozen version of the exact dataset used for a reported experiment so another analyst can reproduce it.
""",
        r"\text{Eligible datum}:t_{available}\leq t_{decision}",
        'decision = "2025-02-01"\nfilings = [("2024-11-10", 8), ("2025-03-15", 12)]\navailable_date = ""\navailable_value = 0\nfor filing in filings:\n    if filing[0] <= decision and filing[0] > available_date:\n        available_date = filing[0]\n        available_value = filing[1]\nprint("Available filing:", available_date, available_value)',
        "A forecast is issued April 1. A quarter ends March 31 but results are released May 10. State which timestamp controls eligibility and list two checks after joining fundamentals to prices.",
        "The May 10 availability date controls eligibility, so the new results are unavailable on April 1. Check unique security-date keys, row counts, currency/units, and that all joined availability times precede decisions.",
        [
            q(
                "Which field prevents use of unpublished financial results?",
                ["Availability timestamp", "Only the fiscal year label", "The current share price"],
                0,
                "Eligibility must reflect when the information became available, not merely the period it describes.",
            ),
            q(
                "A join unexpectedly doubles rows. What should happen next?",
                [
                    "Accept the larger sample",
                    "Inspect key uniqueness and join cardinality",
                    "Calculate a more precise t statistic",
                ],
                1,
                "Duplicated observations can bias every later statistic; the join must be reconciled first.",
            ),
            q(
                "A value describes June 30 and is published August 12. May it enter a July 15 historical signal?",
                [
                    "Yes, because June is earlier",
                    "Yes, if downloaded today",
                    "No, it was not yet available",
                ],
                2,
                "The August publication occurs after the July decision; using it would introduce look-ahead information.",
            ),
        ],
    )

    add(
        "2.22",
        11,
        "Alternative data, text features, and reproducibility",
        "Turn unstructured observations into documented features while separating coverage, timing, and predictive value.",
        r"""
## More data creates more choices

Alternative datasets can contain transactions, text, web activity, or other observations outside a conventional price table. Their coverage may change when a vendor adds contributors or modifies collection. An apparent business trend can therefore be a measurement change.

Text features require a defined document set, publication time, preprocessing method, and vocabulary. A dictionary score counts selected words; a learned representation estimates structure from a corpus. In either case, do not fit vocabulary, scaling, or selection using future documents when claiming historical predictability.

Document lawful access, permitted uses, retention limits, and the treatment of personal or confidential information. Use appropriately authorized data. Statistical utility does not establish that collection or reuse is permitted.

## A worked example

An original toy dictionary has positive words growth and strong, and negative words loss and weak. A document contains growth twice, strong once, loss once, and weak zero times. A stipulated score (positive − negative)/(positive + negative) is (3 − 1)/4 = 0.5.

The score misses context. The phrase no growth contains a positive dictionary word but communicates a different meaning. Boilerplate, negation, document length, and industry vocabulary can all change interpretation. A transparent simple score can still be a useful baseline if its limitations are measured.

## Design the validation packet

Record the source population, collection changes, timestamps, exclusions, and exact feature recipe. Compare the feature against a baseline controlling for obvious existing information. Check whether coverage itself predicts the target and whether that reflects selection rather than economics.

Save the dataset version, code, seed, configuration, and result together. Reproducibility means another researcher can obtain the same reported computation; it does not guarantee that the result transfers to future markets.
""",
        r"Score=(N_{positive}-N_{negative})/(N_{positive}+N_{negative})",
        'positive = 3\nnegative = 1\nscore = (positive - negative) / (positive + negative)\nprint("Toy text score:", score)',
        "A document has two positive and six negative dictionary matches. Compute the score and explain how you would handle a document with no matches. Name one coverage-change risk.",
        "Score is (2−6)/8 = −0.5. With no matches the denominator is zero; use a documented missing or neutral convention with an indicator rather than divide by zero. Vendor expansion can alter measured activity without an economic change.",
        [
            q(
                "A simple dictionary score can mishandle which text feature?",
                [
                    "Negation and context",
                    "Only numerical timestamps",
                    "Nothing if there are many words",
                ],
                0,
                "Word counts alone may not distinguish growth from no growth or identify context-dependent meaning.",
            ),
            q(
                "What can a sudden expansion in vendor coverage create?",
                [
                    "An artificial activity increase",
                    "Guaranteed investment alpha",
                    "A stable sampling frame by definition",
                ],
                0,
                "More observed contributors can raise measured activity even if behavior per contributor is unchanged.",
            ),
            q(
                "Positive matches are 5 and negative matches 3. The stipulated normalized score is:",
                ["0.625", "0.25", "2"],
                1,
                "(5−3)/(5+3) = 2/8 = 0.25, using the defined normalization.",
            ),
        ],
    )

    add(
        "2.23",
        12,
        "Multifactor return models and attribution",
        "Separate factor exposure from residual return and distinguish explanatory from predictive factor specifications.",
        r"""
## Factors describe shared variation

A multifactor model represents returns using several common influences plus a residual. Macroeconomic models use economic shocks; fundamental models use company characteristics or related factor portfolios; statistical models extract patterns from return covariance. These constructions are not interchangeable.

Factor exposures measure sensitivity to the specified factors. An intercept or residual depends on the model's coverage. Omitting a relevant systematic exposure can make ordinary compensation for risk appear to be unexplained performance.

Attribution decomposes realized return according to a chosen model. Forecasting requires expectations about future factors or relationships. Explaining a past return with realized factor movements is easier than predicting that return before the movements occur.

## A worked example

A stipulated monthly excess-return model has alpha 0.1 percentage points, market exposure 1.2, and value exposure 0.5. Realized market and value factor returns are 2 and −1 percentage points. The fitted return is 0.1 + 1.2×2 + 0.5×(−1) = 2.0 points.

If actual excess return is 2.4 points, the residual is 0.4. Market contributed 2.4, value −0.5, and intercept 0.1. These components reconcile to the fitted total, with residual bringing the sum to actual return. One positive residual does not establish persistent skill.

## Keep definitions and dates consistent

Record whether returns are raw or excess, how each factor is constructed, and whether exposures were estimated before the attribution period. A factor built with future membership or revised characteristics can contaminate a historical study.

Compare the portfolio's intended exposures with estimated ones and investigate changes. A strategy marketed as security selection may primarily load on a broad factor. That can still be a deliberate investment choice, but it should be described accurately.
""",
        r"r-r_f=\alpha+\sum_k\beta_k f_k+\epsilon",
        'fitted = .1 + 1.2 * 2 + .5 * -1\nactual = 2.4\nprint("Fitted excess return (points):", fitted)\nprint("Residual (points):", actual - fitted)',
        "Use alpha 0.2, market exposure 0.8, size exposure −0.3, market return 3, and size return 2, all returns in percentage points. Attribute an actual excess return of 2.5.",
        "Market contributes 2.4, size −0.6, intercept 0.2, for fitted return 2.0. Residual is 0.5. These are model-dependent components, not independent proof of manager skill.",
        [
            q(
                "An omitted systematic factor can make its return contribution appear as:",
                [
                    "Unexplained alpha or residual",
                    "A known transaction fee",
                    "A guaranteed risk-free return",
                ],
                0,
                "Model omissions can leave systematic compensation in the unexplained component.",
            ),
            q(
                "Attribution using realized factor returns is primarily:",
                [
                    "A forecast made before those returns",
                    "An explanation conditional on realized inputs and the model",
                    "Proof of causal skill",
                ],
                1,
                "Historical attribution uses observed factor outcomes; forecasting needs information available beforehand.",
            ),
            q(
                "Alpha is 0, exposure is 1.5, factor return is 2, and actual return is 4 percentage points. Residual is:",
                ["1", "2", "3"],
                0,
                "The factor contribution is 3, leaving actual 4 minus fitted 3 = 1 point.",
            ),
        ],
    )

    add(
        "2.24",
        12,
        "Factor risk and active portfolio exposures",
        "Combine factor and residual variance and distinguish total risk from risk relative to a benchmark.",
        r"""
## A portfolio inherits common exposures

Portfolio factor exposure is the weighted sum of its holdings' exposures under the model. Holding many securities does not remove a shared factor loading. Idiosyncratic risk may diversify when residuals are sufficiently independent, but correlated residuals can remain.

For a single factor uncorrelated with the residual, total variance equals beta squared times factor variance plus residual variance. With multiple factors, their covariance matrix matters. Adding individual factor variances without cross terms can misstate total risk.

Active return is portfolio return minus benchmark return. Tracking error is the standard deviation of active return. It differs from total volatility. A portfolio closely tracking a volatile benchmark can have low tracking error and high total risk.

## A worked example

A portfolio has beta 1.2 to a factor with volatility 15%, and residual volatility 8%. Assuming the factor and residual are uncorrelated, total variance is 1.2²×0.15² + 0.08² = 0.0388. Total volatility is about 19.70%.

A 60/40 portfolio holds assets with betas 1.5 and 0.5. Its beta is 0.6×1.5 + 0.4×0.5 = 1.1. If the benchmark beta is 1, active beta is 0.1. The active portfolio still needs residual and other-factor analysis; active beta alone is not tracking error.

## Translate a risk report

Separate intended exposures, unintended exposures, and estimation uncertainty. A risk-budget decision should account for covariance and concentration rather than simply ranking standalone volatilities.

State whether the performance ratio uses total volatility or tracking error. A Sharpe ratio uses excess return relative to a risk-free reference with total volatility; an information ratio uses active return with active-return volatility. Their denominators answer different questions.
""",
        r"\sigma_p^2=\beta^2\sigma_f^2+\sigma_\epsilon^2",
        'from math import sqrt\nprint("Total volatility:", sqrt(1.2 ** 2 * .15 ** 2 + .08 ** 2))\nprint("Portfolio beta:", .6 * 1.5 + .4 * .5)',
        "A portfolio has beta 0.8, factor volatility 20%, and uncorrelated residual volatility 12%. Compute total volatility and explain why low tracking error does not imply low total volatility.",
        "Variance is 0.8²×0.20² + 0.12² = 0.04, giving 20% volatility. Tracking error measures deviations from the benchmark; tracking a volatile benchmark closely can still leave substantial total risk.",
        [
            q(
                "Weights 25% and 75% in assets with betas 2 and 1 give portfolio beta of:",
                ["1.25", "1.5", "3"],
                0,
                "0.25×2 + 0.75×1 = 1.25 under the common factor model.",
            ),
            q(
                "Tracking error is the standard deviation of:",
                [
                    "The benchmark alone",
                    "Portfolio minus benchmark returns",
                    "Only positive returns",
                ],
                1,
                "It measures variability of active return, not total portfolio volatility.",
            ),
            q(
                "Beta is 1, factor volatility 12%, and uncorrelated residual volatility 9%. Total volatility is:",
                ["21%", "3%", "15%"],
                2,
                "√(0.12² + 0.09²) = 15%; add variances, not standard deviations.",
            ),
        ],
    )

    add(
        "2.25",
        13,
        "Value at risk and expected shortfall",
        "Calculate historical loss quantiles and tail averages with an explicit convention and horizon.",
        r"""
## Define loss before quoting a risk number

Value at risk is a loss quantile for a specified horizon and confidence level under a model or empirical distribution. It is not a maximum loss. Expected shortfall summarizes the average loss in the specified worst tail and therefore adds information about severity beyond a threshold.

State whether losses are positive, whether returns are simple or log, and how quantiles are computed. Small samples produce different results under nearest-rank, interpolation, or other conventions. A risk report should be reproducible from its stated convention.

Historical simulation uses observed outcomes or revalued historical shocks. Parametric approaches impose a distribution and exposure model. Monte Carlo approaches simulate from a chosen joint model. All depend on assumptions about future relevance, positions, and dependence.

## A worked example

Ten equally likely one-day losses in thousands are −3, −2, −1, 0, 1, 2, 3, 4, 7, and 12. Negative losses represent gains. Using the nearest-rank empirical 80% quantile, VaR is the eighth ordered loss, 4.

The worst 20% consists of the largest two losses, 7 and 12, so expected shortfall under this exact finite-scenario convention is 9.5. Averaging only observations strictly greater than a quantile can be ambiguous when there are ties or fractional tail masses; define how probability mass is allocated.

## Explain what the estimate omits

A ten-observation sample is deliberately tiny for arithmetic, not a credible tail-risk calibration. Future events can exceed every historical observation. Position changes, options, market gaps, and liquidity costs can also invalidate simple return scaling.

Pair quantile estimates with stress scenarios and an explanation of model uncertainty. A precise-looking confidence level does not certify the quality of the tail model or the sufficiency of capital.
""",
        r"VaR_\alpha=Q_\alpha(L);\quad ES_\alpha=\text{mean loss in worst }1-\alpha",
        'losses = [-3, -2, -1, 0, 1, 2, 3, 4, 7, 12]\n# These case observations are already sorted in ascending order.\nordered = losses\nprint("Nearest-rank 80% VaR:", ordered[7])\nprint("Worst-20% expected shortfall:", sum(ordered[-2:]) / 2)',
        "Ten equally likely sorted losses are −2, −1, 0, 1, 2, 3, 4, 5, 8, 10. Use nearest-rank 80% VaR and the worst two observations for expected shortfall. Explain the sign of a negative loss.",
        "VaR is the eighth observation, 5. Expected shortfall is (8+10)/2 = 9. A negative loss denotes a gain under this convention. Neither value is a maximum possible future loss.",
        [
            q(
                "A 95% one-day VaR is best described as:",
                [
                    "The largest possible loss",
                    "A one-day loss quantile under a specified model",
                    "An expected annual return",
                ],
                1,
                "VaR is a horizon-specific quantile; losses can exceed it.",
            ),
            q(
                "What additional aspect does expected shortfall describe?",
                [
                    "Average severity in the specified worst tail",
                    "Only the most favorable return",
                    "A guarantee that a threshold is never crossed",
                ],
                0,
                "Expected shortfall averages tail losses and therefore reflects their severity beyond the quantile.",
            ),
            q(
                "For ten equally likely losses, the largest two are 6 and 14. The worst-20% expected shortfall is:",
                ["6", "14", "10"],
                2,
                "With exactly two equal-mass observations in the 20% tail, expected shortfall is (6+14)/2 = 10.",
            ),
        ],
    )

    add(
        "2.26",
        13,
        "Stress testing, liquidity, and nonlinear exposures",
        "Complement statistical risk estimates with coherent scenarios and recognize the limits of square-root scaling.",
        r"""
## A scenario asks a different question

A statistical quantile estimates an outcome frequency under a model. A stress test asks what happens under a specified adverse set of conditions, even when its probability is unknown. Historical stresses reuse an observed episode; hypothetical stresses construct a coherent combination of shocks.

Simple square-root-of-time volatility scaling assumes suitable independence and stable variance. Autocorrelation, volatility changes, jumps, and nonlinear exposures can violate that approximation. A ten-day loss quantile is not always a one-day quantile multiplied by the square root of ten.

Liquidity can amplify losses. Bid-ask spreads, market impact, margin calls, and the inability to exit can change the portfolio between the initial shock and eventual realization. A static price shock should therefore be accompanied by a funding and liquidation path when those channels matter.

## A worked example

A portfolio holds 60% equities and 40% bonds. A stipulated stress applies −25% to equities and −8% to bonds simultaneously. The immediate portfolio return is 0.6×(−25%) + 0.4×(−8%) = −18.2%, assuming fixed initial weights and no intervening trades.

If liquidation costs add 1.5% of starting portfolio value, total modeled loss becomes 19.7%. On one million of starting value, that is 197,000. These costs are a case assumption, not a universal market-impact rate.

## Challenge the path

State whether the portfolio rebalances, faces collateral calls, or must sell assets during the shock. Derivatives may require full repricing rather than a linear exposure approximation. Concentrated positions may be difficult to sell at the quoted price.

Use reverse stress testing to ask what combination would breach a specified loss or liquidity limit. Report the mechanism and plausible dependencies, without attaching an invented probability merely to make the scenario resemble a statistical confidence statement.
""",
        r"R_{stress}=\sum_i w_iR_{i,stress}-\text{costs}",
        'gross = .6 * -.25 + .4 * -.08\nnet = gross - .015\nprint("Gross stress return:", gross)\nprint("Loss including liquidation:", -net * 1000000)',
        "A 70/30 portfolio experiences −20% and −5% shocks, plus liquidation costs of 2% of initial value. Calculate loss on 200,000 and name an assumption violated by forced rebalancing.",
        "Gross loss is 15.5%; including costs it is 17.5%, or 35,000. Forced rebalancing changes exposures during the path, so a static initial-weight calculation may no longer describe the realized outcome.",
        [
            q(
                "A stress scenario with no assigned probability should be presented as:",
                [
                    "A guaranteed 99% quantile",
                    "A conditional outcome under stipulated shocks",
                    "A forecast that must occur",
                ],
                1,
                "Stress analysis can be useful without a calibrated occurrence probability; its conditional assumptions must be explicit.",
            ),
            q(
                "Which feature can undermine square-root-of-time scaling?",
                [
                    "Serial dependence and changing volatility",
                    "Consistent units alone",
                    "An explicit horizon",
                ],
                0,
                "The scaling approximation relies on stability and dependence assumptions that financial series may violate.",
            ),
            q(
                "An equal-weight portfolio faces returns of −30% and +10%, before costs. Its static stress return is:",
                ["−20%", "−10%", "+10%"],
                1,
                "0.5×(−30%) + 0.5×10% = −10% with unchanged initial weights.",
            ),
        ],
    )

    add(
        "2.27",
        14,
        "Backtesting and simulation without hindsight",
        "Construct a chronological experiment that accounts for execution timing, costs, and the full research search.",
        r"""
## A backtest is a reconstruction

Specify the information set, signal timestamp, execution convention, position rule, and costs before evaluating outcomes. A close-derived signal cannot normally claim an earlier fill in the same bar. The app's price sandbox executes close-derived signals at the next open; use that convention when interpreting its results.

Include the historical universe, failed securities, distributions, and corporate actions appropriate to the research question. Separate development, validation, and final evaluation chronologically. When prediction labels span several periods, observations near a boundary can share future outcomes; purge or separate overlapping information as needed.

Simulation can explore hypothetical scenarios or resampled paths. It reveals behavior under its assumptions, not evidence that a real-market signal exists. Synthetic-price profits should not be presented as empirical validation of an economic strategy.

## A worked example

A toy strategy has period returns of 2%, −1%, 3%, and 0% before costs. Charge 0.2 percentage points each period as a stipulated implementation cost. Net returns are 1.8%, −1.2%, 2.8%, and −0.2%. Wealth from 100 becomes 100×1.018×0.988×1.028×0.998 ≈ 103.19.

The gross arithmetic mean is 1%; the net arithmetic mean is 0.8%. Neither arithmetic mean is the compounded total return. Cost assumptions should be linked to turnover, spreads, impact, and fees in a real study rather than held constant for convenience.

## Freeze the final experiment

Save the universe definition, data version, code, parameter search, dates, seed, and execution settings. Run the final evaluation only after selecting the model. Report unfavorable folds, turnover, drawdowns, and sensitivity to higher costs.

A robust research conclusion can be that evidence is insufficient. The purpose of a backtest is to challenge a specified idea with an honest reconstruction, not to produce the most attractive curve obtainable from the available history.
""",
        r"W_T=W_0\prod_t(1+r_t-c_t)",
        'gross = [.02, -.01, .03, 0]\nwealth = 100\nfor value in gross:\n    wealth = wealth * (1 + value - .002)\nprint("Net terminal wealth:", round(wealth, 2))\nprint("Net arithmetic mean:", sum(gross) / len(gross) - .002)',
        "A close signal occurs on Monday and the specified execution is the next open. Identify the earliest eligible fill. Then compound two gross returns of +3% and −2% with 0.5 percentage points of cost per period from 100.",
        "The next available trading-session open is the earliest eligible fill under this convention. Net returns are +2.5% and −2.5%; wealth is 100×1.025×0.975 = 99.9375. A zero net arithmetic mean does not imply unchanged wealth.",
        [
            q(
                "A close-derived signal under next-open execution may first fill:",
                [
                    "At the previous day's close",
                    "At the next eligible session open",
                    "At the current day's low known afterward",
                ],
                1,
                "The fill must follow the information used to produce the signal and respect the specified execution rule.",
            ),
            q(
                "A profitable synthetic-price experiment establishes:",
                [
                    "A real-market predictive edge",
                    "Behavior under the simulated assumptions",
                    "Guaranteed live execution quality",
                ],
                1,
                "Synthetic outcomes test mechanics and model behavior; they do not validate empirical profitability in actual markets.",
            ),
            q(
                "Gross return is 1% and implementation cost is 0.4 percentage points in a period. Net return is:",
                ["0.6%", "1.4%", "0.04%"],
                0,
                "Subtract consistent return units: 1.0% − 0.4% = 0.6%.",
            ),
        ],
    )

    add(
        "2.28",
        14,
        "Capstone: a reproducible investment research report",
        "Combine data provenance, inference, model comparison, risk, and costs in a decision-ready research packet.",
        r"""
## Your research brief

A fictional committee asks whether a monthly signal merits further paper testing. Development and validation are complete; the frozen model is evaluated over twelve later months. Net active returns, after a stipulated 0.10 percentage-point monthly cost, are: 1.2, −0.8, 0.5, 1.0, −1.1, 0.7, 0.3, −0.4, 1.4, −0.9, 0.6, and 0.2 percentage points.

The benchmark's active return is zero by definition. Twenty variants were explored during development. The evaluation period is small and the supplied independent-month assumption is questionable. Use the case to practice calculations and limitations, not to claim a validated strategy.

## A worked example

The net active mean is 0.225 percentage points per month. Sample standard deviation is about 0.8444 points and the independent-month standard error is about 0.2437. The t statistic against zero is approximately 0.923.

Using a supplied 95% critical value of 2.201, the mean interval is approximately −0.311 to 0.761 points. It includes zero. The positive sample mean does not establish a positive population mean under this procedure, and dependence or selection concerns can further weaken inference.

Increase the assumed monthly cost by 0.20 percentage points. The mean falls to 0.025 points. This sensitivity demonstrates that economic usefulness is fragile even before asking whether the model will generalize. Active-return observations alone do not reconstruct total portfolio drawdown; obtain total returns and the benchmark path before making that claim.

## Deliver a research packet

Write 700–1,000 words covering the economic hypothesis, label and feature dates, universe and missingness, development and final splits, all trials, baseline comparison, net inference, tail scenarios, execution assumptions, and monitoring criteria. Include the runnable worksheet and a provenance table for any additional data. Propose the next experiment without rebranding the used final period as untouched.

Self-assess five criteria from 0 to 4: chronology and provenance, reproducible calculations, valid inference, economic risk and cost analysis, and a decision with limitations. Aim for 15/20 with no zero. A score of 3 means correct and explicit; 4 also challenges a plausible alternative. Store the written report in your notebook. The app grades the separate numerical exam; the written rubric is for self-review.
""",
        r"t=\bar r_{active}/(s_{active}/\sqrt n)",
        'from math import sqrt\nx = [1.2, -.8, .5, 1, -1.1, .7, .3, -.4, 1.4, -.9, .6, .2]\nmean = sum(x) / len(x)\nsquared = 0\nfor v in x:\n    squared = squared + (v - mean) ** 2\ns = sqrt(squared / (len(x) - 1))\nse = s / sqrt(len(x))\nprint("Mean active return (points):", mean)\nprint("Sample standard deviation:", s)\nprint("t statistic:", mean / se)\nprint("95% interval:", mean - 2.201 * se, mean + 2.201 * se)\nprint("Mean with higher costs:", mean - .20)',
        "Write the committee report in your notebook. Explain the conclusion from the supplied interval, propose a dependence-aware uncertainty check, and specify a new evaluation period for the next frozen experiment.",
        "The interval includes zero and the cost sensitivity nearly eliminates the mean. A defensible decision is further research or paper observation, not a claim of established alpha. Compare suitable block lengths or dependence-aware errors, retain all twenty development trials in the log, and reserve genuinely later data after freezing the next model. Do not calculate total portfolio drawdown from active returns alone.",
        [
            q(
                "The capstone's confidence interval includes zero. What follows?",
                [
                    "Persistent positive alpha is proved",
                    "The stated procedure does not exclude a zero mean",
                    "The true mean is proved to be zero",
                ],
                1,
                "The interval indicates uncertainty rather than proof of either positive alpha or an exactly zero parameter.",
            ),
            q(
                "Can the supplied active returns alone establish total portfolio drawdown?",
                [
                    "Yes, with no benchmark data",
                    "No; total portfolio returns and the relevant wealth path are needed",
                    "Only if the mean is positive",
                ],
                1,
                "Active returns describe differences from a benchmark and do not by themselves reconstruct total portfolio wealth.",
            ),
            q(
                "A follow-up study has a net mean of 0.30 percentage points and an additional cost sensitivity of 0.35 points. The revised mean is:",
                ["0.65 points", "0.05 points", "−0.05 points"],
                2,
                "0.30 − 0.35 = −0.05 percentage points; implementation sensitivity can reverse an apparent advantage.",
            ),
        ],
    )

    checkpoints = [
        (
            "Checkpoint · cash flows and measurement",
            [
                (
                    "2.1",
                    q(
                        "A payment of 121 in two years discounted at 10% is worth:",
                        ["100", "110", "121"],
                        0,
                        "121 / 1.10² = 100 using two annual periods.",
                    ),
                ),
                (
                    "2.6",
                    q(
                        "Nominal 6% compounded semiannually gives an effective annual rate of:",
                        ["6%", "6.09%", "12%"],
                        1,
                        "1.03² − 1 = 6.09%; compounding adds 0.09 percentage points.",
                    ),
                ),
                (
                    "2.7",
                    q(
                        "A +10% return followed by +10% gives total compounded return of:",
                        ["10%", "20%", "21%"],
                        2,
                        "1.10² − 1 = 21%, including the return earned on the first period's gain.",
                    ),
                ),
                (
                    "2.8",
                    q(
                        "The sample 0, 2, 4 has sample standard deviation of:",
                        ["2", "4", "1"],
                        0,
                        "Mean is 2, squared deviations sum to 8, sample variance is 4, and standard deviation is 2.",
                    ),
                ),
            ],
        ),
        (
            "Checkpoint · probability and estimation",
            [
                (
                    "2.9",
                    q(
                        "Prior event probability is 50%; a signal occurs in 80% of events and 20% of nonevents. Event probability given signal is:",
                        ["50%", "80%", "20%"],
                        1,
                        "Joint probabilities are 0.4 and 0.1; 0.4 / 0.5 = 80%.",
                    ),
                ),
                (
                    "2.10",
                    q(
                        "Weights 40% and 60% with expected returns 5% and 10% give expected return of:",
                        ["6%", "7.5%", "8%"],
                        2,
                        "0.4×5% + 0.6×10% = 8%.",
                    ),
                ),
                (
                    "2.3",
                    q(
                        "Standard deviation is 12% and n=36 independent observations. Mean standard error is:",
                        ["2%", "6%", "0.33%"],
                        0,
                        "12% / √36 = 2%, under the independent-observation formula.",
                    ),
                ),
                (
                    "2.12",
                    q(
                        "A bootstrap samples only surviving funds. What remains unresolved?",
                        [
                            "The ability to compute a mean",
                            "Survivorship selection bias",
                            "The existence of any observations",
                        ],
                        1,
                        "Resampling does not reconstruct excluded failed funds; the sampling frame still needs correction.",
                    ),
                ),
            ],
        ),
        (
            "Checkpoint · inference and forecasting",
            [
                (
                    "2.13",
                    q(
                        "Ten predefined tests use Bonferroni at 1% family alpha. Individual threshold is:",
                        ["0.01", "0.1", "0.001"],
                        2,
                        "0.01 / 10 = 0.001 for each test under the stipulated family-wise procedure.",
                    ),
                ),
                (
                    "2.15",
                    q(
                        "For y=2+x−z, x=3 and z=1 give prediction:",
                        ["4", "5", "6"],
                        0,
                        "2 + 3 − 1 = 4 under the specified model.",
                    ),
                ),
                (
                    "2.17",
                    q(
                        "AR(1) intercept is 0.1 and phi is 0.5. Its stationary mean is:",
                        ["0.1", "0.2", "0.5"],
                        1,
                        "0.1 / (1 − 0.5) = 0.2 under the stationary setup.",
                    ),
                ),
                (
                    "2.18",
                    q(
                        "Errors 1 and 3 have MAE of:",
                        ["1", "3", "2"],
                        2,
                        "Mean absolute error is (1+3)/2 = 2 in the outcome's units.",
                    ),
                ),
            ],
        ),
        (
            "Checkpoint · models, data, and risk",
            [
                (
                    "2.20",
                    q(
                        "TP=12 and FP=3. Precision is:",
                        ["80%", "25%", "60%"],
                        0,
                        "12/(12+3) = 80%; precision conditions on all predicted positives.",
                    ),
                ),
                (
                    "2.21",
                    q(
                        "Which record may enter a June 1 decision?",
                        [
                            "A June 10 release describing May",
                            "A May 20 release available before the decision",
                            "A July restatement",
                        ],
                        1,
                        "The May 20 release is available by June 1; later releases are not.",
                    ),
                ),
                (
                    "2.24",
                    q(
                        "Factor volatility is 8%, beta 1, and independent residual volatility 6%. Total volatility is:",
                        ["14%", "2%", "10%"],
                        2,
                        "√(0.08² + 0.06²) = 10% under the uncorrelated variance decomposition.",
                    ),
                ),
                (
                    "2.26",
                    q(
                        "A 50/50 portfolio faces −10% and −20% shocks plus 1% of initial value in costs. Total loss is:",
                        ["16%", "15%", "31%"],
                        0,
                        "Weighted loss is 15%; adding the stipulated 1% cost gives 16%.",
                    ),
                ),
            ],
        ),
    ]
    part_titles = [
        (
            "Cash flows and investment decisions",
            "Discounting, compounding, annuities, and project value",
        ),
        (
            "Measure and describe the evidence",
            "Returns, data organization, dispersion, and visual diagnosis",
        ),
        ("Reason with probability", "Conditional events, covariance, and portfolio uncertainty"),
        (
            "Choose and challenge distributions",
            "Continuous models, discrete counts, and simulation assumptions",
        ),
        (
            "Estimate from samples",
            "Confidence intervals, dependence, resampling, and selection bias",
        ),
        ("Test research claims", "Error rates, power, paired comparisons, and multiple testing"),
        (
            "Fit a single relationship",
            "Linear regression, coefficient interpretation, and prediction uncertainty",
        ),
        (
            "Explain several influences",
            "Multiple regression, categorical variables, and diagnostics",
        ),
        (
            "Respect time and changing risk",
            "Stationarity, autoregression, forecasting, and conditional volatility",
        ),
        (
            "Learn patterns responsibly",
            "Regularization, classification, clustering, and model validation",
        ),
        (
            "Build a research data pipeline",
            "Availability dates, joins, text features, and reproducibility",
        ),
        (
            "Understand common return drivers",
            "Factor attribution, residuals, portfolio exposures, and active risk",
        ),
        (
            "Measure and challenge market risk",
            "Loss quantiles, expected shortfall, stresses, and liquidity",
        ),
        (
            "Evaluate an investment process",
            "Chronological backtesting, simulation, costs, and research capstone",
        ),
    ]
    return finish(
        {
            "id": "statistical-foundations",
            "number": 2,
            "title": "Quantitative Investment Analysis",
            "description": "A complete quantitative learning path from discounting and probability to machine learning, factor risk, and reproducible strategy evaluation.",
            "source": "CFA Institute · Quantitative Investment Analysis · Fourth edition",
            "level": "Foundational → advanced",
            "icon": "distribution",
            "modules": modules,
            "prerequisites": "Comfort with percentages, algebra, and basic investment vocabulary. The early units build the statistics needed later. Python worksheets are optional and use small, inspectable examples.",
            "outcomes": [
                "Translate cash flows and return data into consistent, reproducible calculations.",
                "Use probability, estimation, and tests while accounting for bias and dependence.",
                "Interpret regression, time-series, machine-learning, and factor models.",
                "Evaluate risk and a strategy after costs with a documented historical information set.",
            ],
            "readingGuide": "The fourteen units map to the fourteen chapters in the fourth-edition publisher contents. Read the corresponding chapter in your own copy, then use these original cases, worksheets, and transfer questions. Earlier editions organize some topics differently and do not provide the same later-chapter coverage. This independent course does not reproduce the publisher's questions and is not an official CFA exam preparation or credential. Allow additional time for book reading and written assignments.",
            "references": [
                {"title": "Fourth edition · publisher contents and reading reference", "url": BOOK}
            ],
            "parts": [
                {"id": str(i), "title": title, "description": f"Book chapter {i} · {desc}"}
                for i, (title, desc) in enumerate(part_titles, 1)
            ],
        },
        checkpoints,
    )
