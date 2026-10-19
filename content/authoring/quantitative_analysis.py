"""Part 1 of Quantitative Analysis authoring expansion: Header, Chapters 1-4 (Modules 2.1, 2.6, 2.7, 2.8, 2.9, 2.10, 2.2, 2.11)."""

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

    # =========================================================================
    # PART I: CLASSICAL STATISTICAL FOUNDATIONS (CHAPTERS 1 - 7)
    # =========================================================================

    # -------------------------------------------------------------------------
    # CHAPTER 1: TIME VALUE OF MONEY
    # -------------------------------------------------------------------------

    add(
        "2.1",
        1,
        "Time value of money",
        "Put cash flows on a timeline and use a discount rate consistent with their timing and units.",
        r"""
## The analytical question

The foundational premise of financial mathematics is that a unit of currency received today is worth more than the same unit of currency received in the future. This divergence arises from three economic forces:
1. **The Opportunity Cost of Capital**: Capital available today can be invested to earn a productive return.
2. **Purchasing Power Depletion (Inflation)**: Future prices are generally higher, reducing the real goods and services a fixed nominal payment can purchase.
3. **Credit and Uncertainty Risk**: A promised future payment carries the risk that the payer may default or experience financial distress.

To evaluate any investment security, all projected future cash receipts and disbursements must be translated onto a single, synchronized date. This operation is governed by the **Present Value (PV)** equation:

$$PV = \sum_{t=1}^{T} \frac{CF_t}{(1 + r)^t}$$

Where:
- $CF_t$ represents the expected net cash flow occurring at the end of period $t$.
- $r$ is the periodic discount rate (the required hurdle rate of return) reflecting opportunity cost and risk.
- $t$ is the exact time index (measured in consistent periods: years, semi-annual periods, or months).

A pervasive analytical error is mixing **cash flow units and discount rate conventions**:
- **Nominal vs Real**: A nominal cash flow forecast (which includes expected inflation) must be discounted at a **nominal discount rate**. Discounting nominal cash flows at a real interest rate produces an artificially inflated present value!
- **Matching Compounding Frequency**: If cash flows arrive quarterly, the discount rate must be expressed as an effective quarterly rate ($r_{\text{quarterly}} = (1 + r_{\text{annual}})^{1/4} - 1$), not an annual rate divided haphazardly.

When valuing perpetual cash flows, we encounter two classical asymptotic forms:
1. **Constant Flat Perpetuity**:
   $$PV = \frac{C}{r} \quad (\text{for constant periodic payment } C)$$
2. **Growing Perpetuity (Gordon Model)**:
   $$PV = \frac{CF_1}{r - g} \quad (\text{requires } r > g)$$

Notice the strict mathematical boundary: if the perpetual growth rate $g$ equals or exceeds the discount rate $r$, the denominator becomes zero or negative, rendering the finite-value formula completely undefined.

## A worked example

Consider a specialized mezzanine debt claim that promises two contractual cash payments:
- $CF_1 = \$110.00$ to be received exactly 1 year from today.
- $CF_2 = \$121.00$ to be received exactly 2 years from today.
- The investor's required opportunity cost of capital for this risk class is $r = 10.0\%\text{ per year}$ ($0.10$).

Let us compute the present value step-by-step:
1. Discount Year 1 Cash Flow:
   $$PV_1 = \frac{\$110.00}{(1.10)^1} = \frac{\$110.00}{1.10} = \$100.00$$
2. Discount Year 2 Cash Flow:
   $$PV_2 = \frac{\$121.00}{(1.10)^2} = \frac{\$121.00}{1.21} = \$100.00$$
3. Total Contractual Present Value:
   $$PV = PV_1 + PV_2 = \$100.00 + \$100.00 = \$200.00$$

Observe the common arithmetic blunder:
An unsophisticated analyst sums the nominal cash flows ($\$110 + \$121 = \$231$) and simply divides by $1.10$, arriving at $\$210.00$. This error under-discounts the second payment by treating a two-year obligation as if it matured in one year!

Now examine a perpetual equity royalty stream:
The royalty promises $CF_1 = \$5.00$ next year, with cash flows projected to grow perpetually at $g = 2.0\%$ per year. The required rate of return is $r = 7.0\%$:
$$PV = \frac{\$5.00}{0.07 - 0.02} = \frac{\$5.00}{0.05} = \$100.00$$

If an analyst aggressively raises the growth assumption from $2.0\%$ to $5.0\%$, the denominator shrinks from $0.05$ to $0.02$, causing the estimated value to explode from $\$100.00$ to $\$250.00$ ($+150\%$). Sensitivity to long-term growth dominates the valuation.

## Research discipline

To ensure institutional rigor in time-value-of-money models:
1. **Draw the Explicit Cash Flow Timeline**: Before writing code or entering numbers, plot every payment on a numbered time grid ($t=0, 1, 2, \dots, T$). Verify whether payments occur at period-end (ordinary annuity) or period-beginning (annuity due).
2. **Audit Nominal vs Real Consistency**: In corporate filings, check whether management's capital project projections are in constant purchasing-power dollars or nominal inflation-adjusted dollars.
3. **Conduct Terminal Value Decomposition**:
   $$\text{Terminal Value Percentage} = \frac{PV(\text{Terminal Value})}{PV(\text{Total Asset})}$$
   If more than $75\%$ of an asset's present value resides in cash flows occurring beyond Year 10, recognize that the thesis is primarily a speculation on terminal growth.
4. **Never Rely on Blind Spreadsheet Formulas**: Always verify that the built-in function conventions (e.g., Excel `NPV` assumes period 1 discounting, whereas Python array indexing starts at 0) match your intended timeline.
""",
        r"PV=\sum_{t=1}^T \frac{CF_t}{(1+r)^t};\quad PV_{\text{perpetuity}}=\frac{CF_1}{r-g}",
        'cash_flows = [110, 121]\npv = 0\nfor i in range(len(cash_flows)):\n    pv = pv + cash_flows[i] / 1.10 ** (i + 1)\nprint("Present value:", round(pv, 2))\nprint("Growing perpetuity:", round(5 / (.07 - .02), 2))',
        "Discount cash flows of $105.00 at Year 1 and $110.25 at Year 2 at a 5.0% annual discount rate. Then calculate the present value if both payments are shifted one year earlier (Year 0 and Year 1). Explain the economic difference.",
        "For payments at Year 1 and 2: PV = $105 / (1.05)^1 + $110.25 / (1.05)^2 = $100.00 + $100.00 = $200.00. If shifted one year earlier (Year 0 and 1): PV = $105 / (1.05)^0 + $110.25 / (1.05)^1 = $105.00 + $105.00 = $210.00. Shifting cash flows one year earlier eliminates one period of discounting, multiplying total present value by exactly (1 + r) = 1.05 ($200 × 1.05 = $210). Receiving money sooner increases economic value by avoiding delay.",
        [
            q(
                "A contractual payment of $121.00 is due in exactly two years. At an annual discount rate of 10%, what is its present value?",
                ["$100.00", "$110.00", "$121.00"],
                0,
                "PV = $121 / (1.10)^2 = $121 / 1.21 = $100.00.",
            ),
            q(
                "Under what condition is the constant-growth perpetuity formula PV = CF1 / (r − g) mathematically valid and economically meaningful?",
                [
                    "Whenever growth g exceeds discount rate r",
                    "Only when discount rate r is strictly greater than perpetual growth rate g (r > g)",
                    "Whenever inflation is zero",
                ],
                1,
                "If r ≤ g, the denominator is zero or negative, making the finite present value formula invalid.",
            ),
            q(
                "An analyst discounts nominal corporate cash flows using a real risk-free rate. What error occurs?",
                [
                    "Present value is correctly stated",
                    "Present value is artificially inflated because inflation is counted in cash flows but omitted from the discount rate",
                    "Present value becomes negative",
                ],
                1,
                "Using a real discount rate on nominal cash flows creates an inconsistent mismatch that overstates asset value.",
            ),
        ],
    )

    add(
        "2.6",
        1,
        "Compounding, annuities, NPV, and IRR",
        "Distinguish nominal from effective rates, value annuities, and evaluate capital projects using NPV and IRR.",
        r"""
## The analytical question

When evaluating investments across different financing agreements, interest rates are quoted under varying compounding frequencies (annual, semi-annual, monthly, continuous). A stated nominal annual rate does not reflect the true economic return earned over a full year due to intra-year interest reinvestment.

To compare rates on a uniform footing, the analyst must compute the **Effective Annual Rate (EAR)**:

$$\text{EAR} = \left(1 + \frac{r_{\text{stated}}}{m}\right)^m - 1$$

Where $r_{\text{stated}}$ is the stated annual percentage rate, and $m$ is the number of compounding periods per year. Under the mathematical limit of **continuous compounding** ($m \to \infty$):

$$\text{EAR}_{\text{continuous}} = e^{r_{\text{stated}}} - 1$$

In project finance and capital budgeting, two primary criteria govern resource allocation:
1. **Net Present Value (NPV)**: The present value of all expected future cash inflows minus the initial cash outlay:
   $$NPV = \sum_{t=1}^T \frac{CF_t}{(1 + k)^t} - C_0$$
   Where $k$ is the project's cost of capital. A project creates economic value if and only if $NPV > 0$.
2. **Internal Rate of Return (IRR)**: The discount rate that equates the present value of future cash inflows with the initial investment, forcing $NPV = 0$:
   $$\sum_{t=1}^T \frac{CF_t}{(1 + \text{IRR})^t} - C_0 = 0$$

Graham, Dodd, and modern CFA quantitative standards establish strict warnings regarding **IRR pitfalls**:
- **The Reinvestment Rate Fallacy**: IRR implicitly assumes all intermediate cash flows can be reinvested at the IRR itself (which may be an unrealistically high $40\%$), whereas NPV correctly assumes reinvestment at the actual cost of capital ($k$).
- **Multiple IRRs and Non-Normal Cash Flows**: If a project involves cash outflows in later years (e.g., environmental decommissioning), Descartes' Rule of Signs dictates that there may be multiple positive IRRs, making the IRR metric completely unreliable.
- **Scale and Mutually Exclusive Projects**: A small project earning a $50\%$ IRR on a $\$1,000$ investment generates less economic wealth than a large project earning a $20\%$ IRR on a $\$1,000,000$ investment. In all mutually exclusive project decisions, **NPV strictly dominates IRR**.

## A worked example

Let us evaluate the effective compounding rate and capital budgeting decisions for Alder Manufacturing:

### 1. Compounding Frequency Audit
A commercial lender offers Alder two financing structures:
- **Loan A**: Stated rate $6.0\%$ compounded semi-annually ($m = 2$).
  $$\text{EAR}_A = \left(1 + \frac{0.06}{2}\right)^2 - 1 = (1.03)^2 - 1 = 6.09\%$$
- **Loan B**: Stated rate $5.95\%$ compounded monthly ($m = 12$).
  $$\text{EAR}_B = \left(1 + \frac{0.0595}{12}\right)^{12} - 1 = (1.004958)^{12} - 1 = 6.115\%$$
Although Loan B advertised a lower stated nominal rate ($5.95\%$ vs $6.0\%$), Loan A is actually cheaper on an effective annual economic basis ($6.09\%$ vs $6.12\%$).

### 2. Capital Project NPV vs IRR Evaluation
Alder's engineering division proposes purchasing an automated robotic welding cell:
- Initial capital expenditure: $C_0 = \$20.0\text{ million}$
- Projected cash savings: $CF_1 = \$12.0\text{ million}$, $CF_2 = \$12.0\text{ million}$
- Cost of capital: $k = 10.0\%$

Let us compute NPV:
$$NPV = \frac{\$12.0\text{M}}{1.10} + \frac{\$12.0\text{M}}{(1.10)^2} - \$20.0\text{M} = \$10.909\text{M} + \$9.917\text{M} - \$20.0\text{M} = +\$0.826\text{ million}$$

Now solve for the project's IRR:
$$\frac{\$12.0\text{M}}{1 + \text{IRR}} + \frac{\$12.0\text{M}}{(1 + \text{IRR})^2} = \$20.0\text{M}$$
Setting $x = \frac{1}{1 + \text{IRR}}$, we have the quadratic equation:
$$12x + 12x^2 = 20 \implies 3x^2 + 3x - 5 = 0$$
Using the quadratic formula:
$$x = \frac{-3 + \sqrt{9 - 4(3)(-5)}}{6} = \frac{-3 + \sqrt{69}}{6} \approx \frac{-3 + 8.3066}{6} \approx 0.8844$$
$$1 + \text{IRR} = \frac{1}{0.8844} \approx 1.1307 \implies \text{IRR} \approx 13.07\%$$

Since $\text{IRR} = 13.07\% > k = 10.0\%$ and $NPV = +\$0.826\text{M} > 0$, the project is approved.

## Research discipline

When evaluating interest rates and capital projects:
1. **Always Convert Quoted Rates to EAR**: In credit agreements, inspect whether interest compounds daily, monthly, or quarterly. Never compare stated nominal APRs directly.
2. **Never Rely on IRR Alone for Mutually Exclusive Decisions**: Always rank mutually exclusive investment proposals by NPV in currency units.
3. **Verify the Reinvestment Assumption**: If a strategy claims an annualized internal rate of return of $60\%$, verify whether realized cash gains can actually be redeployed at that same $60\%$ rate in real markets.
4. **Audit Terminal Decommissioning Outlays**: If a project requires cash outflows at the end of its life (e.g., mine reclamation, lease restoration), plot the NPV profile across multiple discount rates to detect multiple IRR cross-over points.
""",
        r"\text{EAR}=\left(1+\frac{r}{m}\right)^m-1;\quad NPV=\sum_{t=1}^T \frac{CF_t}{(1+k)^t}-C_0",
        'r_nominal = 0.06\near_semi = (1 + r_nominal / 2) ** 2 - 1\nprint("Effective annual rate (semi-annual):", round(ear_semi * 100, 3), "%")\nc0 = 20.0\ncf1 = 12.0\ncf2 = 12.0\nk = 0.10\nnpv = cf1 / (1 + k) + cf2 / (1 + k) ** 2 - c0\nprint("Project NPV ($M):", round(npv, 3))',
        "A bank offers 8.0% nominal interest compounded quarterly. Calculate its effective annual rate (EAR). Then evaluate a capital project requiring an initial outlay of $50M that generates $30M at Year 1 and $30M at Year 2 at a 12% cost of capital. Determine whether the project should be accepted.",
        "EAR = (1 + 0.08 / 4)⁴ − 1 = (1.02)⁴ − 1 = 1.08243 − 1 = 8.243%. For the project: NPV = $30M / (1.12)¹ + $30M / (1.12)² − $50M = $26.786M + $23.916M − $50M = $50.702M − $50M = +$0.702M ($702,000). Because NPV > 0 (and IRR ≈ 13.07% exceeds the 12% hurdle rate), the project is economically viable and should be accepted.",
        [
            q(
                "A stated nominal rate of 6% is compounded semi-annually. What is the Effective Annual Rate (EAR)?",
                ["6.00%", "6.09%", "12.00%"],
                1,
                "EAR = (1 + 0.06/2)^2 − 1 = (1.03)^2 − 1 = 6.09%.",
            ),
            q(
                "Why is Net Present Value (NPV) considered methodologically superior to Internal Rate of Return (IRR) for evaluating mutually exclusive capital projects?",
                [
                    "NPV assumes cash flows are reinvested at the realistic opportunity cost of capital and correctly measures total wealth creation",
                    "IRR is illegal under modern accounting standards",
                    "NPV requires no discount rate",
                ],
                0,
                "NPV assumes reinvestment at the cost of capital, whereas IRR assumes reinvestment at the IRR, which distorts project rankings.",
            ),
            q(
                "An investment requiring an outlay of $100 yields $60 in Year 1 and $60 in Year 2. At a 10% discount rate, what is its NPV?",
                ["+$4.13", "+$20.00", "−$5.00"],
                0,
                "NPV = $60/1.10 + $60/1.21 − $100 = $54.55 + $49.59 − $100 = +$4.13.",
            ),
        ],
    )

    # -------------------------------------------------------------------------
    # CHAPTER 2: ORGANIZING, VISUALIZING, AND DESCRIBING DATA
    # -------------------------------------------------------------------------

    add(
        "2.7",
        2,
        "Return measurement and data organization",
        "Distinguish arithmetic from geometric compounding and normalize prices for corporate actions.",
        r"""
## The analytical question

In empirical finance and investment research, raw market prices cannot be analyzed directly without rigorous normalization. Corporate actions (such as stock splits, reverse splits, cash dividends, and rights offerings) alter the number of shares and nominal price levels without altering the underlying economic wealth of the investor:
- In a 5-for-1 stock split, the share price drops by $80\%$ overnight, but each shareholder receives five times as many shares. Treating this as an $80\%$ loss is a catastrophic data-engineering failure.

When summarizing historical investment returns over time, the analyst must distinguish between two fundamentally different averages:
1. **Arithmetic Mean Return ($\bar{R}_A$)**:
   $$\bar{R}_A = \frac{1}{T} \sum_{t=1}^T R_t$$
   The arithmetic mean is the best unbiased estimate of the expected single-period return for the next period.
2. **Geometric Mean Return ($\bar{R}_G$, Compound Annual Growth Rate / CAGR)**:
   $$\bar{R}_G = \left[ \prod_{t=1}^T (1 + R_t) \right]^{1/T} - 1$$
   The geometric mean measures the true compounded rate of wealth accumulation over multiple sequential periods.

The mathematical relationship between the arithmetic and geometric mean is governed by volatility:

$$\bar{R}_G \approx \bar{R}_A - \frac{1}{2} \sigma^2$$

$$\text{The Arithmetic Mean is strictly greater than the Geometric Mean whenever returns fluctuate } (\sigma > 0).$$

Consider the classic volatility drag example:
- Period 1: $+50.0\%$ return.
- Period 2: $-50.0\%$ return.
- Arithmetic Mean: $\frac{+50\% - 50\%}{2} = 0.0\%$.
- An investor who starts with $\$100$ reaches $\$150$ in Period 1, and drops to $\$75$ in Period 2—a severe **$-25.0\%$ net loss**!
- True Geometric Return: $\bar{R}_G = \sqrt{1.50 \times 0.50} - 1 = \sqrt{0.75} - 1 = 0.866 - 1 = -13.4\%\text{ per period}$.

The arithmetic mean paints an entirely false picture of capital preservation, while the geometric mean reflects real wealth in the bank.

## A worked example

Let us examine the corporate action adjustment and return measurement for an investor holding shares in Bank Central Asia (BBCA):
- Initial position: $100\text{ shares}$ purchased at $P_0 = \text{Rp } 50.00\text{ per share}$ (Total portfolio value = $\text{Rp } 5,000$).
- The company executes a **5-for-1 stock split**.
- The investor's share count expands to $100 \times 5 = 500\text{ shares}$.
- In the subsequent trading session, the stock closes at $P_1 = \text{Rp } 10.20\text{ per share}$.

Let us calculate the true investment return:
1. True Total Portfolio Value after split:
   $$V_1 = 500\text{ shares} \times \text{Rp } 10.20 = \text{Rp } 5,100$$
2. True Holding Period Return:
   $$R = \frac{V_1 - V_0}{V_0} = \frac{\text{Rp } 5,100 - \text{Rp } 5,000}{\text{Rp } 5,000} = \frac{\text{Rp } 100}{\text{Rp } 5,000} = +2.0\%$$

Look at the error of an unadjusted raw price calculation:
If an automated script simply looked at the raw price change:
$$R_{\text{naive}} = \frac{\text{Rp } 10.20 - \text{Rp } 50.00}{\text{Rp } 50.00} = -79.6\%$$
The script would report a phantom $-79.6\%$ crash and trigger false stop-loss liquidations!

Now evaluate multi-period compounding:
An asset produces returns of $+10.0\%$ in Year 1 followed by $+10.0\%$ in Year 2:
$$\text{Wealth Factor} = (1 + 0.10) \times (1 + 0.10) = 1.10 \times 1.10 = 1.21$$
$$\text{Compounded Cumulative Return} = 1.21 - 1 = +21.0\%$$
The extra $1.0\%$ represents the return earned on the first year's reinvested gain (**compound interest**).

## Research discipline

When managing financial return data:
1. **Maintain Separate Split and Dividend Adjustment Factors**: Store raw closing prices alongside the corporate action multiplier. Never overwrite historical raw price records permanently.
2. **Use Geometric Means for Multi-Year Performance Reporting**: When reporting historical performance to investors or regulators (GIPS standards), always display the geometric CAGR. Never use the arithmetic mean to report multi-year historical wealth growth.
3. **Use Arithmetic Means for Single-Period Forward Projections**: In portfolio optimization (Markowitz mean-variance models), the expected return vector must use the arithmetic mean of single-period returns.
4. **Audit Survivorship Bias in Index Constituents**: When calculating the average return of an industry over ten years, ensure that companies that went bankrupt or were delisted are included in the sample.
""",
        r"\bar{R}_G=\left[\prod_{t=1}^T(1+R_t)\right]^{1/T}-1;\quad \bar{R}_G \approx \bar{R}_A - \frac{1}{2}\sigma^2",
        'r1 = 0.10\nr2 = 0.10\ntotal_wealth = (1 + r1) * (1 + r2)\nprint("Compounded cumulative return (%):", round((total_wealth - 1) * 100, 2))\nr_pos = 0.50\nr_neg = -0.50\nfrom math import sqrt\ngeom = sqrt((1 + r_pos) * (1 + r_neg)) - 1\nprint("Geometric mean of +50% and -50% (%):", round(geom * 100, 2))',
        "An investor experiences returns of +20.0% in Year 1, −10.0% in Year 2, and +15.0% in Year 3. Calculate the arithmetic mean return and the geometric compound annual growth rate (CAGR). Explain why the geometric mean is lower.",
        "Arithmetic mean is (0.20 − 0.10 + 0.15) / 3 = 0.25 / 3 = +8.33% per year. Wealth factor is (1.20) × (0.90) × (1.15) = 1.242. Total cumulative return is +24.2%. Geometric mean is (1.242)^(1/3) − 1 = 1.0749 − 1 = +7.49% per year. The geometric mean (7.49%) is lower than the arithmetic mean (8.33%) because of return volatility; experiencing a −10% drawdown in Year 2 permanently impaired the compounding base.",
        [
            q(
                "A stock gains +10% in Year 1 and +10% in Year 2. What is the total cumulative compounded return?",
                ["10%", "20%", "21%"],
                2,
                "Compounded return is (1.10)^2 − 1 = 1.21 − 1 = 21%, including the return on reinvested gains.",
            ),
            q(
                "Why must an analyst use the geometric mean rather than the arithmetic mean when summarizing multi-year historical investment performance?",
                [
                    "The geometric mean measures the actual compound rate of capital growth realized by an investor, whereas the arithmetic mean ignores volatility drag",
                    "The geometric mean is always higher than the arithmetic mean",
                    "The arithmetic mean cannot be calculated for percentages",
                ],
                0,
                "The geometric mean accurately reflects the multi-period terminal wealth, accounting for the destructive effect of drawdowns.",
            ),
            q(
                "A stock undergoes a 5-for-1 stock split. An investor held 100 shares at $50.00 ($5,000 total). Afterward, the stock trades at $10.20 per share. What is the true holding period return?",
                ["−79.6%", "+2.0%", "+10.2%"],
                1,
                "The investor now owns 500 shares at $10.20 = $5,100 total value, representing a +2.0% return on the initial $5,000.",
            ),
        ],
    )

    add(
        "2.8",
        2,
        "Describe distributions before fitting models",
        "Calculate dispersion, skewness, and kurtosis to assess non-normality before applying statistical models.",
        r"""
## The analytical question

Before fitting any econometric model or calculating a risk metric, a quantitative analyst must inspect the empirical distribution of the underlying data. Blindly assuming that financial returns obey a bell-shaped Gaussian normal distribution is one of the most common causes of quantitative failure in market crises.

To describe a distribution rigorously, we compute the **Four Statistical Moments**:
1. **First Moment (Central Tendency - Mean $\mu$ or $\bar{x}$)**: The arithmetic center of the observations:
   $$\bar{x} = \frac{1}{n} \sum_{i=1}^n x_i$$
2. **Second Moment (Dispersion - Sample Variance $s^2$ and Standard Deviation $s$)**: Measures the spread of observations around the mean:
   $$s^2 = \frac{1}{n - 1} \sum_{i=1}^n (x_i - \bar{x})^2, \quad s = \sqrt{s^2}$$
   Notice the denominator: we divide by $n - 1$ (Bessel's correction) to ensure the sample variance is an unbiased estimator of the true population variance.
3. **Third Moment (Asymmetry - Skewness $S$)**: Measures the degree of directional asymmetry:
   $$S = \frac{n}{(n - 1)(n - 2)} \sum_{i=1}^n \left(\frac{x_i - \bar{x}}{s}\right)^3$$
   - **Negative Skewness ($S < 0$)**: The left tail is elongated. In finance, strategies that produce small steady gains punctuated by sudden catastrophic wipeouts (such as uncovered options writing or carry trades) exhibit severe negative skewness.
   - **Positive Skewness ($S > 0$)**: The right tail is elongated (e.g., venture capital or long out-of-the-money call options).
4. **Fourth Moment (Peakedness & Tails - Kurtosis $K$)**: Measures the probability mass concentrated in the extreme tails:
   $$\text{Excess Kurtosis} = \text{Sample Kurtosis} - 3$$
   A normal distribution has a kurtosis of exactly $3.0$ ($\text{Excess Kurtosis} = 0$). Financial return series almost universally display **leptokurtosis (fat tails)** ($\text{Excess Kurtosis} > 0$), meaning extreme market crashes occur with vastly higher frequency than a normal distribution predicts.

Under **Chebyshev's Inequality**, for any distribution regardless of shape, the proportion of observations lying within $k$ standard deviations of the mean is at least:

$$P(|X - \mu| < k\sigma) \ge 1 - \frac{1}{k^2} \quad (\text{for all } k > 1)$$

## A worked example

Let us calculate the dispersion metrics for a tiny sample of three return observations:
$$X = \{0, 2, 4\}$$

Let us trace the calculations step-by-step:
1. Sample Mean ($\bar{x}$):
   $$\bar{x} = \frac{0 + 2 + 4}{3} = \frac{6}{3} = 2.0$$
2. Sum of Squared Deviations:
   $$(0 - 2)^2 = (-2)^2 = 4$$
   $$(2 - 2)^2 = (0)^2 = 0$$
   $$(4 - 2)^2 = (2)^2 = 4$$
   $$\sum_{i=1}^3 (x_i - \bar{x})^2 = 4 + 0 + 4 = 8.0$$
3. Sample Variance ($s^2$, dividing by $n - 1 = 2$):
   $$s^2 = \frac{8.0}{3 - 1} = \frac{8.0}{2} = 4.0$$
4. Sample Standard Deviation ($s$):
   $$s = \sqrt{4.0} = 2.0$$

Now evaluate the impact of an extreme outlier:
Consider five daily sales figures from an Indonesian retail shop: $\{10, 11, 9, 10, 60\}$.
- Median: $10.0$
- Mean: $\frac{10 + 11 + 9 + 10 + 60}{5} = \frac{100}{5} = 20.0$
The single outlier of $60$ doubles the mean from $10$ to $20$!
A disciplined analyst does not delete $60$ automatically; they investigate whether it represents a major holiday festival order, a data recording error, or a genuine tail demand spike required for inventory sizing.

## Research discipline

When describing financial datasets:
1. **Always Plot Histograms and Box Plots First**: Never proceed to regression or risk modeling without visually inspecting the distribution for bimodal clusters, truncation, and outliers.
2. **Report Both Mean and Median**: If the mean diverges substantially from the median, the distribution is skewed or contaminated by extreme outliers.
3. **Audit Excess Kurtosis in Daily Returns**: If daily stock or currency returns display excess kurtosis of $4.0$ or higher, reject standard deviation as a sufficient risk metric; standard deviation will severely underestimate tail crash probability.
4. **Document Outlier Treatment Explicitly**: If an outlier is winsorized or trimmed, record the exact threshold and justify why the excluded event will not repeat in live trading.
""",
        r"s^2=\frac{1}{n-1}\sum_{i=1}^n(x_i-\bar{x})^2;\quad \text{Excess Kurtosis}=K-3",
        'x = [0, 2, 4]\nmean = sum(x) / len(x)\nsum_sq = 0.0\nfor val in x:\n    sum_sq = sum_sq + (val - mean) ** 2\nsample_var = sum_sq / (len(x) - 1)\nfrom math import sqrt\nsample_std = sqrt(sample_var)\nprint("Sample mean:", mean)\nprint("Sample variance:", sample_var)\nprint("Sample standard deviation:", sample_std)',
        "A sample consists of five return observations: [−4, −2, 0, 2, 4]. Calculate the sample mean, sample variance, and sample standard deviation. State whether this symmetric sample exhibits positive, negative, or zero skewness.",
        "Sample mean is (−4 − 2 + 0 + 2 + 4) / 5 = 0 / 5 = 0.0. Squared deviations from mean: (−4)² = 16, (−2)² = 4, (0)² = 0, (2)² = 4, (4)² = 16. Sum of squared deviations = 16 + 4 + 0 + 4 + 16 = 40. Sample variance is 40 / (5 − 1) = 40 / 4 = 10.0. Sample standard deviation is √10 ≈ 3.162. Because the distribution is perfectly symmetrical around zero, its skewness is exactly zero.",
        [
            q(
                "A sample consists of the observations 0, 2, and 4. What is its sample standard deviation?",
                ["2.0", "4.0", "1.0"],
                0,
                "Mean is 2; squared deviations sum to 8; sample variance is 8 / (3 − 1) = 4; standard deviation is √4 = 2.0.",
            ),
            q(
                "An investment strategy generates steady small positive returns for eleven months but suffers an enormous catastrophic loss in month twelve. What shape best characterizes its return distribution?",
                [
                    "Positive skewness",
                    "Negative skewness with fat tails (leptokurtosis)",
                    "Symmetric normal distribution",
                ],
                1,
                "Strategies with rare large downside drawdowns exhibit pronounced negative skewness and high kurtosis.",
            ),
            q(
                "According to Chebyshev's inequality, what minimum proportion of observations must lie within 2 standard deviations of the mean for any distribution?",
                ["50%", "75%", "95%"],
                1,
                "Chebyshev's inequality states P(|X − μ| < kσ) ≥ 1 − 1/k^2. For k = 2, 1 − 1/4 = 75%.",
            ),
        ],
    )

    # -------------------------------------------------------------------------
    # CHAPTER 3: PROBABILITY CONCEPTS
    # -------------------------------------------------------------------------

    add(
        "2.9",
        3,
        "Conditional probability and Bayes updates",
        "Update prior probabilities using Bayes' formula and avoid base-rate neglect in market signals.",
        r"""
## The analytical question

Investment decision-making under uncertainty requires constantly updating beliefs in response to incoming evidence (earnings surprises, debt covenant amendments, macro releases). The mathematical foundation for updating beliefs is **Bayes' Rule**:

$$P(A \mid B) = \frac{P(B \mid A) P(A)}{P(B)}$$

Where:
- $P(A)$ is the **Prior Probability**: The baseline probability of event $A$ before observing new evidence.
- $P(B \mid A)$ is the **Likelihood**: The probability of observing signal $B$ given that event $A$ is true.
- $P(B)$ is the **Total Probability of the Signal**: The unconditional probability of observing signal $B$ across all possible states:
  $$P(B) = P(B \mid A) P(A) + P(B \mid A^c) P(A^c)$$
- $P(A \mid B)$ is the **Posterior Probability**: The revised probability of event $A$ after observing signal $B$.

The most pervasive cognitive error among both novice traders and machine-learning engineers is **Base-Rate Neglect**. When a signal sounds highly accurate (e.g., $90\%$ sensitivity), people intuitively assume that seeing the signal means the event is almost certain.

However, if the underlying event is rare (a low base rate $P(A)$), even an accurate signal will generate a massive number of **false positives** that swamp the true positives!

$$\text{If the base rate is low, most positive alerts are false alarms.}$$

To avoid confusion, an analyst must always construct a complete **Joint Probability Matrix** ($2 \times 2$ contingency table) and verify that all cells sum to $1.00$.

## A worked example

Let us evaluate a quantitative credit distress warning algorithm designed to detect corporate bond defaults:
- **Prior Base Rate of Distress**: In the corporate bond universe, only $10.0\%$ of issuers enter distress in a given year:
  $$P(D) = 0.10 \implies P(D^c) = 0.90$$
- **Signal Sensitivity (True Positive Rate)**: If a company is truly in distress, the algorithm triggers an alarm ($W$) $80.0\%$ of the time:
  $$P(W \mid D) = 0.80$$
- **False Alarm Rate (False Positive Rate)**: For healthy, non-distressed companies, the algorithm incorrectly triggers an alarm $20.0\%$ of the time:
  $$P(W \mid D^c) = 0.20$$

Now calculate the probabilities step-by-step:
1. Joint Probability of Distress and Alarm:
   $$P(D \cap W) = P(D) \times P(W \mid D) = 0.10 \times 0.80 = 0.08$$
2. Joint Probability of Healthy Company and False Alarm:
   $$P(D^c \cap W) = P(D^c) \times P(W \mid D^c) = 0.90 \times 0.20 = 0.18$$
3. Total Unconditional Probability of an Alarm ($P(W)$):
   $$P(W) = P(D \cap W) + P(D^c \cap W) = 0.08 + 0.18 = 0.26 \quad (26.0\%)$$
4. Posterior Probability of Distress Given an Alarm ($P(D \mid W)$):
   $$P(D \mid W) = \frac{P(D \cap W)}{P(W)} = \frac{0.08}{0.26} = \frac{8}{26} \approx 30.769\% \approx 30.77\%$$

Look at the staggering insight!
Even though the detector has an impressive $80\%$ sensitivity, when an alarm sounds, there is only a **$30.77\%$ chance** that the company is actually in distress!
Out of every 26 flagged companies, 18 are healthy companies generating false alarms ($69.2\%$), while only 8 are truly distressed. The low $10\%$ base rate dominates the outcome.

## Research discipline

To execute Bayesian analysis without cognitive distortion:
1. **Always Establish the Empirical Base Rate First**: Before evaluating the accuracy of any predictive signal or machine-learning classifier, record the historical frequency of the target event.
2. **Build the Four-Cell Contingency Table**:
   - Cell 1: True Positives ($P(A \cap B)$)
   - Cell 2: False Positives ($P(A^c \cap B)$)
   - Cell 3: False Negatives ($P(A \cap B^c)$)
   - Cell 4: True Negatives ($P(A^c \cap B^c)$)
   Verify that all four cells sum exactly to $1.000$.
3. **Evaluate the Asymmetry of Error Costs**: In credit analysis, missing a true default (False Negative) is far more expensive than investigating a false alarm (False Positive). Factor the economic cost matrix into your threshold selection.
4. **Re-Test When Regimes Shift**: During a severe macro recession, the base rate of distress may jump from $10\%$ to $30\%$, dramatically increasing the posterior precision of the exact same warning signal.
""",
        r"P(A \mid B)=\frac{P(B \mid A)P(A)}{P(B)};\quad P(B)=P(B \mid A)P(A)+P(B \mid A^c)P(A^c)",
        'joint = .10 * .80\nwarning = joint + .90 * .20\nprint("Warning probability:", warning)\nprint("Distress given warning:", joint / warning)',
        "Prior distress probability is 20%. A warning system triggers for 75% of distressed firms and 25% of nondistressed firms. Calculate the total probability of a warning and the posterior probability of distress given an alert. Explain why the posterior is not 75%.",
        "Joint distress and warning is 0.20 × 0.75 = 0.15. Joint nondistress and false warning is 0.80 × 0.25 = 0.20. Total probability of warning is 0.15 + 0.20 = 0.35 (35%). Posterior probability is 0.15 / 0.35 = 42.86%. The posterior is 42.86% rather than 75% because the 75% metric conditions on the company already being distressed, whereas the posterior conditions on observing the alert and must account for false alarms from the 80% nondistressed majority.",
        [
            q(
                "If P(A) = 0.20 and the conditional probability P(B | A) = 0.50, what is the joint probability P(A and B)?",
                ["0.10", "0.40", "0.70"],
                0,
                "Joint probability is P(A and B) = P(A) × P(B | A) = 0.20 × 0.50 = 0.10.",
            ),
            q(
                "Why can an automated trading alert with 85% accuracy generate mostly false alarms in live market conditions?",
                [
                    "Because if the underlying market opportunity or fault is rare (low base rate), the absolute number of false alarms from the vast non-event population exceeds the true alerts",
                    "Because Bayes' rule is mathematically flawed",
                    "Because probability cannot exceed 50%",
                ],
                0,
                "Base-rate neglect: when an event is rare, false positives from the large majority overwhelm true positives.",
            ),
            q(
                "Prior distress is 25%. A signal occurs in 60% of distressed firms and 20% of nondistressed firms. What is the posterior probability of distress given the signal?",
                ["25%", "60%", "50%"],
                2,
                "Joint distress is 0.25 × 0.60 = 0.15. Joint non-distress is 0.75 × 0.20 = 0.15. Total signal is 0.30. Posterior is 0.15 / 0.30 = 50.0%.",
            ),
        ],
    )

    add(
        "2.10",
        3,
        "Expected return, covariance, and diversification",
        "Combine state-dependent returns and explain how covariance changes portfolio uncertainty.",
        r"""
## The analytical question

Modern portfolio theory begins with Harry Markowitz's fundamental mathematical insight:

$$\text{The risk of a portfolio is not the weighted average of the risks of its individual assets.}$$

While portfolio **expected return** is a simple linear combination of component expected returns:

$$E[R_p] = \sum_{i=1}^n w_i E[R_i]$$

Portfolio **variance** is governed by the pairwise **covariance** between all constituent assets:

$$\sigma_p^2 = \sum_{i=1}^n \sum_{j=1}^n w_i w_j \text{Cov}(R_i, R_j) = \sum_{i=1}^n w_i^2 \sigma_i^2 + 2 \sum_{i=1}^{n-1}\sum_{j=i+1}^n w_i w_j \text{Cov}(R_i, R_j)$$

For a two-asset portfolio ($w_1 + w_2 = 1$):

$$\sigma_p^2 = w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 + 2 w_1 w_2 \rho_{1,2} \sigma_1 \sigma_2$$

Where:
- $\sigma_1, \sigma_2$ are the standard deviations of Asset 1 and Asset 2.
- $\rho_{1,2} = \frac{\text{Cov}(R_1, R_2)}{\sigma_1 \sigma_2}$ is the correlation coefficient, strictly bounded between $-1.0 \le \rho \le +1.0$.

Observe the power of the correlation coefficient:
- **Perfect Positive Correlation ($\rho = +1.0$)**: Portfolio volatility is a linear weighted average: $\sigma_p = w_1 \sigma_1 + w_2 \sigma_2$. **Zero diversification benefit**.
- **Zero Correlation ($\rho = 0.0$)**: The cross-term vanishes. For two equal-weight assets with identical volatility $\sigma$:
  $$\sigma_p = \sqrt{(0.5)^2 \sigma^2 + (0.5)^2 \sigma^2} = \sqrt{0.5 \sigma^2} = \frac{\sigma}{\sqrt{2}} \approx 0.707 \sigma$$
  Portfolio volatility drops by **$29.3\%$** without sacrificing a single basis point of expected return!
- **Perfect Negative Correlation ($\rho = -1.0$)**: Complete elimination of portfolio variance is mathematically possible.

However, an analyst must recognize the fatal trap of **Correlation Breakdown in Crises**:
In normal market regimes, assets may display correlations near zero. But during a liquidity panic or global market contagion, asset correlations rapidly converge toward $+1.0$, causing diversification benefits to evaporate precisely when investors need them most.

## A worked example

Let us evaluate an equal-weight portfolio ($w_1 = 0.50, w_2 = 0.50$) constructed from two assets:
- **Asset 1 (Equities)**: Expected return $E[R_1] = 8.0\%$, annual volatility $\sigma_1 = 20.0\%$.
- **Asset 2 (Bonds)**: Expected return $E[R_2] = 4.0\%$, annual volatility $\sigma_2 = 10.0\%$.
- Correlation: $\rho_{1,2} = 0.25$.

Let us compute portfolio return and risk step-by-step:
1. Portfolio Expected Return:
   $$E[R_p] = (0.50 \times 8.0\%) + (0.50 \times 4.0\%) = 4.0\% + 2.0\% = 6.0\%$$
2. Component Variance Terms:
   $$w_1^2 \sigma_1^2 = (0.50)^2 \times (0.20)^2 = 0.25 \times 0.04 = 0.0100$$
   $$w_2^2 \sigma_2^2 = (0.50)^2 \times (0.10)^2 = 0.25 \times 0.01 = 0.0025$$
3. Covariance Interaction Term:
   $$2 w_1 w_2 \text{Cov}(R_1, R_2) = 2 \times 0.50 \times 0.50 \times (0.25 \times 0.20 \times 0.10) = 0.50 \times 0.0050 = 0.0025$$
4. Total Portfolio Variance ($\sigma_p^2$):
   $$\sigma_p^2 = 0.0100 + 0.0025 + 0.0025 = 0.0150$$
5. Portfolio Volatility ($\sigma_p$):
   $$\sigma_p = \sqrt{0.0150} \approx 0.12247 \approx 12.25\%$$

Now compare this with an undiversified portfolio ($\rho = +1.0$):
$$\sigma_{\text{undiversified}} = (0.50 \times 20.0\%) + (0.50 \times 10.0\%) = 10.0\% + 5.0\% = 15.00\%$$
The modest $0.25$ correlation reduced annual volatility from $15.00\%$ down to $12.25\%$—a risk reduction of $2.75$ percentage points ($18.3\%$) with zero sacrifice of the $6.0\%$ expected return!

## Research discipline

When modeling portfolio risk and covariance:
1. **Never Calculate Correlation on Mismatched Timestamps**: Ensure that both return series use identical closing timestamps and currency conventions. Mismatched time zones (e.g., Tokyo vs New York) artificially depress measured correlation.
2. **Stress-Test Correlation Spikes**: In stress-testing models, recalculate portfolio volatility assuming all credit and equity correlations jump to $+0.80$ or $+0.90$.
3. **Remember That Zero Correlation $\ne$ Independence**: Correlation measures only *linear* co-movement. Two assets can have zero linear correlation while possessing massive non-linear tail dependence (e.g., asset returns and volatility options).
4. **Audit Covariance Matrix Dimensionality**: If you estimate a covariance matrix for $N = 100$ assets from $T = 60$ monthly observations, the sample covariance matrix is singular (rank deficient) and cannot be inverted for portfolio optimization without shrinkage techniques.
""",
        r"\sigma_p^2=w_1^2\sigma_1^2+w_2^2\sigma_2^2+2w_1w_2\rho\sigma_1\sigma_2;\quad E[R_p]=w_1E[R_1]+w_2E[R_2]",
        'from math import sqrt\nw1 = 0.50\nw2 = 0.50\ns1 = 0.20\ns2 = 0.10\nrho = 0.25\nvariance = w1**2 * s1**2 + w2**2 * s2**2 + 2 * w1 * w2 * rho * s1 * s2\nprint("Expected return (%):", round((w1 * 0.08 + w2 * 0.04) * 100, 2))\nprint("Portfolio volatility (%):", round(sqrt(variance) * 100, 2))',
        "Two assets each have an annual standard deviation of 10.0% and an expected return of 6.0%. Calculate the portfolio volatility of an equal-weight portfolio if: (1) correlation is 0.0, and (2) correlation is 1.0. Explain what probabilistic independence implies beyond zero correlation.",
        "Under correlation rho = 0.0: Variance = (0.5)²(0.10)² + (0.5)²(0.10)² + 0 = 0.0025 + 0.0025 = 0.0050. Volatility is √0.0050 ≈ 7.071%. Under correlation rho = 1.0: Volatility is (0.5 × 10%) + (0.5 × 10%) = 10.0%. Zero correlation establishes that there is no linear relationship between the assets. Full probabilistic independence is much stronger: it requires that the entire conditional probability distribution P(A|B) = P(A), precluding non-linear tail co-dependence or volatility clustering.",
        [
            q(
                "An equal-weight portfolio consists of two assets with expected returns of 10% and 2%. What is the portfolio's expected return?",
                ["4%", "6%", "12%"],
                1,
                "Expected return is (0.50 × 10%) + (0.50 × 2%) = 5% + 1% = 6.0%.",
            ),
            q(
                "Under what condition does combining two risky assets with equal volatility produce ZERO reduction in portfolio standard deviation?",
                [
                    "When the correlation between the assets is exactly +1.0",
                    "When the correlation is 0.0",
                    "When both assets have positive expected returns",
                ],
                0,
                "When correlation is +1.0, portfolio volatility is a pure linear weighted average, providing no diversification benefit.",
            ),
            q(
                "Two assets each have 20% volatility. With a correlation of zero, what is the volatility of a 50/50 portfolio?",
                ["20.00%", "14.14%", "10.00%"],
                1,
                "Portfolio variance is (0.5)^2(0.20)^2 + (0.5)^2(0.20)^2 = 0.01 + 0.01 = 0.02. Volatility is √0.02 ≈ 14.14%.",
            ),
        ],
    )

    # -------------------------------------------------------------------------
    # CHAPTER 4: COMMON PROBABILITY DISTRIBUTIONS
    # -------------------------------------------------------------------------

    add(
        "2.2",
        4,
        "Probability distributions in finance",
        "Select and challenge continuous distributions, and assess the danger of thin-tail assumptions.",
        r"""
## The analytical question

In quantitative finance, probability distributions serve as mathematical abstractions used to model asset returns, interest rates, and operational losses.

We must separate two foundational families of continuous distributions:
1. **The Normal (Gaussian) Distribution**: Defined completely by its mean ($\mu$) and variance ($\sigma^2$):
   $$f(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{(x - \mu)^2}{2\sigma^2}}$$
   - **Key Property**: A linear combination of independent normal random variables is itself normally distributed.
   - **Severe Flaw for Asset Prices**: A normal distribution assigns positive probability to negative asset prices. A stock cannot trade at $-\$15.00$ because equity owners possess limited liability.
2. **The Lognormal Distribution**: If a variable's natural logarithm is normally distributed ($\ln(S_t / S_0) \sim \mathcal{N}(\mu, \sigma^2)$), the variable itself is lognormally distributed:
   - **Key Property**: $S_t > 0$ strictly. Asset prices can never drop below zero.
   - **Key Property**: Bounded below by zero and skewed to the right, matching real-world stock prices.

However, Graham, Dodd, and modern risk managers issue an unyielding warning regarding the **Gaussian Thin-Tail Illusion**:
Under a standard normal distribution:
- A $3\sigma$ move occurs once every $370\text{ trading days}$ (roughly every 1.5 years).
- A $5\sigma$ move occurs once every $14,000\text{ years}$!
- A $7\sigma$ move occurs once in the history of the universe!

Yet, in actual financial markets, $5\sigma$ and $7\sigma$ daily drawdowns occur **multiple times per decade**!
This extreme divergence occurs because financial returns are not normal; they are **leptokurtic (fat-tailed)**. To model returns realistically, analysts use:
- **Student's t-Distribution**: Controlled by its **degrees of freedom ($\nu$)**. As $\nu \to \infty$, the t-distribution converges to the normal distribution. For low degrees of freedom ($\nu = 4 \text{ or } 5$), it generates heavy, realistic crash tails.

## A worked example

Let us evaluate an automated market-making strategy that models daily stock returns as normally distributed with:
$$\mu = 0.0\%, \quad \sigma = 1.0\%\text{ per day}$$

The risk committee tests the model against an empirical market stress event:
On a turbulent day, the stock suffers a **$-10.0\%$ flash crash**:
1. Calculate the z-score of this event:
   $$z = \frac{-10.0\% - 0.0\%}{1.0\%} = -10.0\sigma$$
2. What does the Gaussian normal model say about a $-10\sigma$ event?
   Under a normal distribution, the probability of observing a move beyond $10$ standard deviations is approximately:
   $$P(Z \le -10) \approx 7.6 \times 10^{-24}$$
   This implies that such an event should happen once every **$5 \times 10^{20}$ years**—an impossibility on Earth.

Yet, $-10\%$ market crashes occurred in October 1987, October 2008, and March 2020!
An algorithmic fund that configured its capital reserves based on the normal distribution would have been wiped out instantly because it assigned a probability of zero to an event that occurs in real financial history.

Now contrast this with a Student's t-distribution with $\nu = 4$ degrees of freedom:
Under a t-distribution with fat tails, the probability of extreme tail exceedances is thousands of times higher, forcing the quantitative desk to hold adequate cash buffers.

## Research discipline

When selecting probability distributions for financial systems:
1. **Never Assume Daily Asset Returns Are Normal**: Use the normal distribution only for analytical convenience in small toy examples or long-horizon annualized aggregates where the Central Limit Theorem begins to apply.
2. **Conduct QQ-Plots (Quantile-Quantile Plots)**: Plot empirical return quantiles against theoretical normal quantiles. If the points flare upward on the right and downward on the left (an S-curve), fat tails are conclusively proven.
3. **Use Lognormal for Asset Prices, Continuous Rates for Returns**:
   $$r_{\text{log}} = \ln\left(\frac{P_t}{P_{t-1}}\right)$$
   Continuously compounded returns are additive over time and can be modeled with symmetric fat-tailed distributions without violating limited liability.
4. **Stress-Test Downside Parameters**: Calibrate risk models using the **worst three months of historical crisis data** rather than five years of tranquil bull-market data.
""",
        r"z=\frac{x-\mu}{\sigma};\quad \ln(P_t/P_0) \sim \mathcal{N}(\mu, \sigma^2)",
        'import math\ndef normal_pdf(x, mu, sigma):\n    return (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - mu) / sigma) ** 2)\nprint("Normal density at mean (0.0):", round(normal_pdf(0, 0, 1), 4))\nprint("Normal density at 3 sigma:", round(normal_pdf(3, 0, 1), 6))\nprint("Normal density at 5 sigma:", round(normal_pdf(5, 0, 1), 10))',
        "A risk model assumes normal daily returns with mean 0.0% and standard deviation 1.5%. A market index drops 6.0% in one day. Calculate the z-score of this event. State how an analyst should respond if management insists this event was an 'impossible outlier' that does not require model revision.",
        "The z-score is (−6.0% − 0.0%) / 1.5% = −4.0σ. Under a normal distribution, a 4-sigma event has a one-tailed probability of approximately 0.0000317 (1 in 31,560 days, or once every 125 years). An analyst must reject management's claim that it was an 'impossible outlier': empirical financial returns exhibit fat tails (leptokurtosis) and volatility clustering. The occurrence of a 4-sigma move proves the thin-tailed normal model is misspecified, requiring the adoption of a Student's t-distribution or historical simulation.",
        [
            q(
                "Why is the lognormal distribution preferred over the normal distribution for modeling asset prices?",
                [
                    "Because lognormal asset prices cannot drop below zero, respecting the limited liability of equity holders",
                    "Because the lognormal distribution has zero variance",
                    "Because lognormal distributions are always symmetric",
                ],
                0,
                "A normal distribution allows negative prices, whereas a lognormal variable is strictly positive (P > 0).",
            ),
            q(
                "A daily return of −10σ occurs in a market portfolio. What does this empirical event establish regarding the assumption of normality?",
                [
                    "It proves that the financial markets are strictly Gaussian",
                    "It proves that the normal distribution model is dangerously misspecified because real market returns possess fat tails (leptokurtosis)",
                    "It proves that standard deviation was zero",
                ],
                1,
                "A 10-sigma event is statistically impossible under a normal distribution; its occurrence proves returns have heavy fat tails.",
            ),
            q(
                "As the degrees of freedom parameter (ν) in a Student's t-distribution approaches infinity, what does the distribution become?",
                [
                    "A uniform distribution",
                    "A standard normal distribution",
                    "A Poisson distribution",
                ],
                1,
                "As degrees of freedom increase, the t-distribution converges asymptotically to the standard normal distribution.",
            ),
        ],
    )

    add(
        "2.11",
        4,
        "Counts, joint models, and simulation logic",
        "Model discrete arrival events, evaluate burstiness, and design Monte Carlo simulations.",
        r"""
## The analytical question

Not all financial variables are continuous prices. Many critical market phenomena are discrete integer counts:
- How many corporate defaults will occur in a high-yield loan portfolio this quarter?
- How many orders will hit an exchange trading gateway in a 10-millisecond window?
- How many operational server outages will occur in a fiscal year?

To model discrete count phenomena, we use two fundamental probability distributions:
1. **The Binomial Distribution**: Models the number of successes ($k$) in $n$ independent trials, each with success probability $p$:
   $$P(X = k) = \binom{n}{k} p^k (1 - p)^{n - k} = \frac{n!}{k!(n - k)!} p^k (1 - p)^{n - k}$$
   $$\text{Mean} = n p, \quad \text{Variance} = n p (1 - p)$$
2. **The Poisson Distribution**: Models the number of discrete events occurring in a fixed interval of time when events occur independently at a constant average rate $\lambda$:
   $$P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}$$
   $$\text{Mean} = \lambda, \quad \text{Variance} = \lambda$$

However, in electronic markets and systemic credit events, the foundational assumption of **independence breaks down**. Events arrive in **bursts (clustering)**:
- High-frequency order arrivals cluster during market breakouts.
- Corporate defaults cluster during systemic credit contractions.
If an engineering team designs an exchange order queue assuming smooth Poisson arrivals averaging $100\text{ msgs/sec}$, the system will crash when a volatility burst sends $1,000\text{ messages}$ in a single burst!

When mathematical equations become intractable due to path-dependency, embedded options, or complex correlations, quantitative analysts turn to **Monte Carlo Simulation**:

$$\text{Simulated Expected Payoff: } E[V] \approx \frac{1}{M} \sum_{m=1}^M V(\omega_m)$$

Where $\omega_m$ represents simulated random scenarios drawn from a specified joint probability distribution across $M$ trials (typically $10,000$ to $1,000,000$ iterations).

## A worked example

Let us evaluate the message handling capacity of Alder Trading's electronic order routing gateway:
- Average message arrival rate: $\lambda = 100\text{ messages per second}$.
- Queue buffer capacity before dropping packets: $250\text{ messages}$.

Let us compare two simulation models:

### Model A: Standard Independent Poisson Arrivals
Under smooth independent arrivals with $\lambda = 100$, the standard deviation is:
$$\sigma = \sqrt{\lambda} = \sqrt{100} = 10\text{ messages}$$
A surge beyond $250$ messages represents a $15\sigma$ deviation:
$$z = \frac{250 - 100}{10} = 15.0\sigma$$
The Poisson simulation reports that the buffer will **never overflow in a thousand years**. Management concludes the system has massive excess capacity.

### Model B: Burst-Clustered Hawkes Arrival Process
In live trading, market makers cancel and replace orders simultaneously in response to news. During volatility spikes, arrivals cluster:
- For $90\%$ of seconds, arrivals average $50\text{ msgs/sec}$.
- For $10\%$ of seconds (burst mode), arrivals spike to $1,000\text{ msgs/sec}$.
- The long-run average remains identical: $(0.90 \times 50) + (0.10 \times 1000) = 45 + 100 = 145\text{ msgs/sec}$.

Under Model B:
During the $10\%$ burst seconds, $1,000$ messages slam into a $250$-message buffer. The queue overflows immediately, dropping orders, creating execution latency, and causing massive trading losses!

Notice the vital lesson:
Both models share similar average arrival rates, but the **clustered arrival model exposes the fatal queue bottleneck** that the independent Poisson model completely concealed.

## Research discipline

When designing simulation engines and discrete count models:
1. **Never Confuse Average Arrival Rate with Peak Burst Capacity**: Size queues and margin liquidity buffers for peak 99.9th percentile bursts, not average throughput.
2. **Set and Log Pseudo-Random Number Seeds**:
   ```python
   import random
   random.seed(42)  # Enforce reproducibility
   ```
   Every simulation experiment must be reproducible by another researcher down to the exact bit.
3. **Verify Convergence and Standard Error of the Mean**:
   $$\text{Simulation Error} = \frac{s_{\text{sim}}}{\sqrt{M}}$$
   To double the precision of a Monte Carlo estimate, you must quadruple the number of iterations ($M$).
4. **Audit Correlated Binomial Defaults**: In credit portfolios, never model defaults as independent coin flips. Incorporate a common macro factor that drives joint defaults across all borrowers simultaneously.
""",
        r"P(X=k)=\frac{\lambda^k e^{-\lambda}}{k!};\quad E[V]\approx\frac{1}{M}\sum_{m=1}^M V(\omega_m)",
        'import math\ndef poisson_pmf(k, lam):\n    factorial = 1\n    for i in range(k):\n        factorial = factorial * (i + 1)\n    return (lam ** k * math.exp(-lam)) / factorial\nprint("Poisson probability k=0 (lambda=2):", round(poisson_pmf(0, 2), 4))\nprint("Poisson probability k=2 (lambda=2):", round(poisson_pmf(2, 2), 4))\nprint("Poisson probability k=5 (lambda=2):", round(poisson_pmf(5, 2), 4))',
        "A portfolio holds 10 corporate bonds. The historical default probability for each bond is 5.0% over one year. Assuming defaults are independent, calculate the probability of observing exactly zero defaults using the binomial formula. Explain why assuming independence in a credit portfolio is dangerous.",
        "Using the binomial formula for n = 10, k = 0, p = 0.05: P(X = 0) = (10! / (0! 10!)) × (0.05)⁰ × (0.95)¹⁰ = 1 × 1 × (0.95)¹⁰ ≈ 0.5987 (59.87%). Assuming independence is dangerous because corporate borrowers share common macroeconomic exposures (recession, interest rates, credit crunches). If a severe recession strikes, defaults cluster together; assuming independence severely underestimates the probability of multiple joint defaults.",
        [
            q(
                "A discrete event follows a Poisson distribution with average arrival rate λ = 4. What is the variance of this distribution?",
                ["2", "4", "16"],
                1,
                "A key mathematical property of the Poisson distribution is that its variance equals its mean (Variance = λ = 4).",
            ),
            q(
                "Why can an order-routing engine sized for average Poisson message traffic crash during real market trading?",
                [
                    "Because real market orders arrive in correlated bursts during volatility events, swamping buffers designed only for average independent throughput",
                    "Because Poisson distributions cannot be simulated in code",
                    "Because computers cannot process more than 10 messages per second",
                ],
                0,
                "Financial arrivals cluster in intense bursts during news releases, easily overwhelming systems sized only for mean independent rates.",
            ),
            q(
                "In a Monte Carlo simulation, if you increase the number of simulated iterations M from 10,000 to 40,000, what happens to the standard error of the simulation estimate?",
                [
                    "It is cut in half (1/√4 = 1/2)",
                    "It is divided by 4",
                    "It remains completely unchanged",
                ],
                0,
                "Simulation standard error scales as 1/√M. Quadrupling M halves the estimation standard error.",
            ),
        ],
    )

    # =========================================================================
    # CHAPTERS 5 - 7
    # =========================================================================

# -------------------------------------------------------------------------
    # CHAPTER 5: SAMPLING AND ESTIMATION
    # -------------------------------------------------------------------------

    add(
        "2.3",
        5,
        "Sampling & confidence intervals",
        "Construct point estimates and confidence intervals for population means while accounting for sample size.",
        r"""
## The analytical question

In investment research, analysts almost never observe the entire population of historical returns. We observe only a limited sample of $n$ observations (e.g., $60$ monthly returns). From this sample, we construct a sample mean ($\bar{X}$) to estimate the unobservable true population mean ($\mu$).

The theoretical foundation of statistical estimation is the **Central Limit Theorem (CLT)**:

$$\text{As sample size } n \text{ increases, the distribution of the sample mean } \bar{X} \text{ approaches a normal distribution,}$$
$$\text{regardless of the shape of the underlying population distribution (provided variance is finite).}$$

The dispersion of the sample mean around the true population mean is measured by the **Standard Error of the Mean (SE)**:

$$\sigma_{\bar{X}} = \frac{\sigma}{\sqrt{n}} \quad (\text{if population } \sigma \text{ is known})$$

$$s_{\bar{X}} = \frac{s}{\sqrt{n}} \quad (\text{if population } \sigma \text{ is unknown and estimated by sample } s)$$

Notice the inverse square-root relationship ($1/\sqrt{n}$):
- To cut the standard error in half, an analyst must **quadruple** the sample size ($4n$).
- Increasing sample size diminishes estimation error, but at an increasingly sluggish rate.

A **Confidence Interval** provides a range of plausible values for the true population mean at a specified $(1 - \alpha)$ degree of confidence:

$$\text{Confidence Interval: } \bar{X} \pm t_{\alpha/2, n-1} \left(\frac{s}{\sqrt{n}}\right)$$

Where $t_{\alpha/2, n-1}$ is the critical two-tailed value from the Student's t-distribution with $df = n - 1$ degrees of freedom.

Two vital nuances must guide the analyst:
1. **The Meaning of a 95% Confidence Interval**: It does *not* mean there is a $95\%$ probability that the true parameter lies inside this specific calculated interval! In classical frequentist statistics, the true parameter $\mu$ is a fixed, non-random constant. A $95\%$ confidence level means that if we repeated the sampling procedure 1,000 times, $95\%$ of the resulting intervals would successfully bracket the true parameter.
2. **The Impact of Sample Size on Tails**: For small samples ($n < 30$), the Student's t-distribution has fatter tails than the normal distribution, producing a wider, more conservative confidence interval to account for uncertainty in estimating the standard deviation.

## A worked example

Let us evaluate an Indonesian micro-retail business consulting initiative. Across a sample of $n = 100$ independent shops, the recorded average annual sales increase is:
- Sample Mean Improvement: $\bar{X} = \text{Rp } 4.0\text{ million}$
- Sample Standard Deviation: $s = \text{Rp } 10.0\text{ million}$
- Sample Size: $n = 100$

Let us construct an approximate $95\%$ confidence interval for the true population mean improvement:
1. Calculate the Standard Error of the Mean:
   $$s_{\bar{X}} = \frac{s}{\sqrt{n}} = \frac{\text{Rp } 10.0\text{M}}{\sqrt{100}} = \frac{\text{Rp } 10.0\text{M}}{10} = \text{Rp } 1.0\text{ million}$$
2. For $n = 100$ ($df = 99$), the two-tailed $95\%$ critical value is approximately $z \approx 1.96$ (or $t_{0.025, 99} \approx 1.984$). Using $1.96$:
   $$\text{Margin of Error} = 1.96 \times s_{\bar{X}} = 1.96 \times \text{Rp } 1.0\text{M} = \text{Rp } 1.96\text{ million}$$
3. Construct the Confidence Interval:
   $$\text{Lower Bound} = \text{Rp } 4.0\text{M} - \text{Rp } 1.96\text{M} = \text{Rp } 2.04\text{ million}$$
   $$\text{Upper Bound} = \text{Rp } 4.0\text{M} + \text{Rp } 1.96\text{M} = \text{Rp } 5.96\text{ million}$$
   $$\text{95% Interval: } [\text{Rp } 2.04\text{M}, \text{Rp } 5.96\text{M}]$$

Because the entire confidence interval lies comfortably above zero, the evidence indicates that the true average improvement is positive under these sampling assumptions.
However, note what the interval *does not* prove: it does not prove that the consulting caused the increase (it could be regional economic growth), and it assumes all 100 shops were independent.

## Research discipline

When constructing and interpreting confidence intervals:
1. **Always Use the Student's t-Distribution When Population Variance is Unknown**: In financial markets, population $\sigma$ is never known. Always use the t-distribution with $n - 1$ degrees of freedom.
2. **Audit Independent Sampling Assumptions**: If return observations are serially correlated (e.g., overlapping monthly hedge fund returns or daily bond illiquidity), observations are not independent. Serial correlation causes the standard error $s / \sqrt{n}$ to severely understate true estimation uncertainty.
3. **Beware of Selection and Survivorship Bias**: If your sample includes only surviving mutual funds, the sample mean is upwardly biased, producing a confidence interval centered on an artificial survivorship premium.
4. **Distinguish Confidence Interval from Prediction Interval**: A confidence interval estimates where the *average* of the population lies ($\mu$). It does not tell you where the *next single observation* ($X_{n+1}$) will fall.
""",
        r"s_{\bar{X}}=\frac{s}{\sqrt{n}};\quad \text{CI}=\bar{X} \pm t_{\alpha/2, n-1} \left(\frac{s}{\sqrt{n}}\right)",
        'from math import sqrt\ns = 10.0\nn = 100\nse = s / sqrt(n)\nmean = 4.0\nz_crit = 1.96\nprint("Standard error of mean:", se)\nprint("95% lower bound:", round(mean - z_crit * se, 2))\nprint("95% upper bound:", round(mean + z_crit * se, 2))',
        "A quantitative strategy generates a sample mean monthly active return of 0.80% across n = 36 months, with a sample standard deviation of 2.40%. Calculate the standard error of the mean. Using a critical t-value of 2.030 (df = 35), construct the 95% confidence interval for the true mean active return. Determine whether the interval includes zero.",
        "Standard error of the mean is se = s / √n = 2.40% / √36 = 2.40% / 6 = 0.40%. Margin of error = 2.030 × 0.40% = 0.812%. Lower bound = 0.80% − 0.812% = −0.012% (−0.01%). Upper bound = 0.80% + 0.812% = +1.612% (+1.61%). The 95% confidence interval is [−0.01%, +1.61%]. Because the interval crosses zero, the analyst cannot conclude with 95% confidence that the strategy generates a positive population active return.",
        [
            q(
                "A sample of n = 64 independent observations has a sample standard deviation of 16%. What is the standard error of the sample mean?",
                ["0.25%", "2.00%", "4.00%"],
                1,
                "Standard error is s / √n = 16% / √64 = 16% / 8 = 2.00%.",
            ),
            q(
                "Why does the Student's t-distribution produce wider confidence intervals than the standard normal distribution for small sample sizes?",
                [
                    "Because estimating the unknown population standard deviation with a small sample introduces additional sampling uncertainty, creating fatter tails",
                    "Because the t-distribution is skewed to the right",
                    "Because t-values are always negative",
                ],
                0,
                "The t-distribution accounts for the added uncertainty of estimating population variance from small samples.",
            ),
            q(
                "A 95% confidence interval for a trading strategy's monthly mean excess return is [−0.20%, +0.80%]. What is the correct statistical interpretation?",
                [
                    "The strategy has definitively proved it generates positive alpha",
                    "The interval includes zero, so the data does not provide sufficient evidence to reject a true mean return of zero at the 5% significance level",
                    "The true mean return is guaranteed to be +0.30%",
                ],
                1,
                "Because zero falls inside the 95% interval, the hypothesis that the strategy has zero mean excess return cannot be rejected.",
            ),
        ],
    )

    add(
        "2.12",
        5,
        "Bootstrap, selection bias, and dependent samples",
        "Design bootstrap resampling schemes that preserve time dependence and audit databases for survivorship bias.",
        r"""
## The analytical question

Classical statistical formulas (such as $s / \sqrt{n}$) rely on two demanding mathematical assumptions:
1. Observations are **Independent and Identically Distributed (I.I.D.)**.
2. The sampling distribution follows a known parametric family (such as the normal or Student's t).

In modern financial datasets, both assumptions are routinely violated:
- Financial returns exhibit **volatility clustering and serial dependence** (today's panic carries over to tomorrow).
- Return distributions have **skewness and excess kurtosis** that distort analytical confidence intervals.

When parametric formulas fail, quantitative analysts deploy the **Bootstrap**:

$$\text{The Bootstrap: Resampling with replacement from the empirical dataset to approximate the sampling distribution.}$$

In a standard I.I.D. bootstrap:
1. Draw $n$ observations at random **with replacement** from the original dataset of size $n$.
2. Calculate the statistic of interest (e.g., mean, median, Sharpe ratio) on this resample.
3. Repeat $B = 10,000\text{ times}$ to build the empirical distribution of the estimator.

However, an analyst must confront two critical failure modes in real-world resampling:
1. **The Row-by-Row Fallacy on Time-Series Data**: If you apply standard I.I.D. resampling to consecutive daily stock returns, you randomly scramble the time sequence! A week of clustered bank runs is chopped into isolated days, destroying the serial correlation and volatility clustering.
   - **The Solution**: **Block Bootstrap**. Instead of resampling individual days, resample contiguous blocks of consecutive observations (e.g., 10-day or 20-day blocks), preserving the internal temporal dependence.
2. **Selection and Survivorship Bias in Databases**:
   If a commercial mutual fund database purges funds that went bankrupt or were liquidated over the past decade, resampling that database 100,000 times will simply resample surviving winners!
   $$\text{Resampling cannot create data that was omitted from the sampling frame.}$$

## A worked example

Let us evaluate the demand forecasting dataset of an Indonesian logistics distributor:
- Two years of daily package volumes ($n = 730\text{ days}$).
- The data contains pronounced **week-long holiday festival clusters** (e.g., Lebaran / Eid al-Fitr), during which package volumes remain elevated for 7 to 10 consecutive days.

Compare two resampling schemes:

### Scheme A: Standard Independent Row Bootstrap
- The algorithm picks individual random days from the 730-day history with replacement.
- In any single bootstrap sample, a high-volume festival Tuesday might be selected without its Monday or Wednesday.
- The consecutive holiday cluster is completely obliterated.
- Result: The bootstrap severely **underestimates the variance** of weekly demand and fails to simulate the multi-day warehouse gridlock that occurs in reality!

### Scheme B: Moving Block Bootstrap
- The analyst sets a block length of $L = 10\text{ consecutive trading days}$.
- The algorithm draws random 10-day contiguous slices of time with replacement.
- Whenever a festival week is drawn, the entire multi-day surge is preserved intact.
- Result: The block bootstrap accurately captures the risk of prolonged warehouse backlog and correctly sizes emergency liquidity buffers.

Now audit the database for **Survivorship Bias**:
A hedge fund analyst tests a momentum strategy on historical Indonesian equities from 2015 to 2025 using today's constituent list of the IDX LQ45 index:
- The screen omits textile and retail companies that filed for bankruptcy in 2018.
- The backtest reports a stellar $18.5\%$ CAGR.
- When re-run on a point-in-time database including the 24 delisted, bankrupt firms, the CAGR collapses to $6.2\%$! The $12.3\%$ difference was pure survivorship hallucination.

## Research discipline

To execute non-parametric estimation without methodological bias:
1. **Use Block Bootstrap for Dependent Time Series**:
   $$\text{Block Length } L \approx \mathcal{O}(n^{1/3}) \quad (\text{calibrated to empirical autocorrelation decay})$$
   Report a sensitivity analysis across multiple block lengths ($L = 5, 10, 20$).
2. **Audit Point-in-Time Database Provenance**: Confirm whether the database contains delisted, merged, and liquidated entities. If delisted entities are absent, do not report the backtest without an explicit survivorship disclaimer.
3. **Beware of Backfill (Instant History) Bias**: When hedge funds join commercial databases, vendors frequently backfill 3 to 5 years of historical returns prior to the onboarding date. Exclude all backfilled historical data.
4. **Never Bootstrap Across Structural Breaks**: If a company executed a massive transformative merger or regulatory reform occurred in Year 3, do not pool pre-break and post-break data into the same bootstrap bag.
""",
        r"\text{Block Bootstrap: } \{B_1, B_2, \dots, B_k\}, \quad B_i = (X_{t}, X_{t+1}, \dots, X_{t+L-1})",
        'data = [10, 12, 11, 45, 50, 48, 12, 10, 11]\nblock = 3\navailable = len(data) - block + 1\n# A stated generator stands in for random.choice, so the draw is reproducible.\nseed = 42\nresample = ""\nfor draw in range(3):\n    seed = (seed * 1103515245 + 12345) % 2147483648\n    start = seed % available\n    print("Draw", draw + 1, "takes the block starting at index", start)\n    for offset in range(block):\n        resample = f"{resample}{data[start + offset]} "\nprint("Original series:", data)\nprint("Blocks of length", block, "available:", available)\nprint("Block resample (9 values):", resample)',
        "An analyst evaluates a historical fund database to compute average hedge fund returns over a 10-year period. The database drops funds once they liquidate or cease reporting. Explain how this database defect introduces survivorship bias and describe why applying a 10,000-iteration bootstrap cannot fix the error.",
        "Dropping liquidated funds removes the worst-performing funds that suffered catastrophic drawdowns, leaving only successful survivors in the database. This artificially inflates the measured historical average return. Applying a bootstrap (even with 10,000 iterations) cannot fix the error because bootstrapping merely resamples with replacement from the existing data; it cannot reconstruct the missing failed funds that were never recorded in the sample frame. The bias resides in the data collection itself.",
        [
            q(
                "When bootstrapping time-series financial returns that display volatility clustering, why must an analyst use a block bootstrap rather than an independent row bootstrap?",
                [
                    "An independent row bootstrap scrambles the chronological sequence, destroying the serial correlation and volatility clustering",
                    "Block bootstrapping is required by federal securities law",
                    "Block bootstrapping always increases the sample mean",
                ],
                0,
                "Resampling individual rows breaks the serial dependence structure; block bootstrapping draws contiguous time slices to preserve temporal clustering.",
            ),
            q(
                "A quantitative backtest is conducted on a database containing only companies currently listed on the stock exchange today. What fatal statistical bias is present?",
                [
                    "Look-ahead bias only",
                    "Survivorship bias, because failed and delisted companies are excluded from the historical test",
                    "No bias is present",
                ],
                1,
                "Testing only current survivors ignores firms that failed, producing an artificially rosy historical performance record.",
            ),
            q(
                "What happens to the estimated standard error of the mean if you increase bootstrap resamples B from 1,000 to 10,000 on a sample of n = 50 observations?",
                [
                    "It eliminates all sampling uncertainty entirely",
                    "It stabilizes the Monte Carlo approximation of the bootstrap distribution, but does not increase the underlying empirical sample size n = 50",
                    "It increases the true population mean",
                ],
                1,
                "Increasing B refines the numerical precision of the bootstrap approximation, but cannot add new empirical information beyond the original n = 50 observations.",
            ),
        ],
    )

    # -------------------------------------------------------------------------
    # CHAPTER 6: HYPOTHESIS TESTING
    # -------------------------------------------------------------------------

    add(
        "2.4",
        6,
        "Hypothesis testing in markets",
        "Formulate null hypotheses, evaluate Type I and Type II errors, and test research claims against sampling noise.",
        r"""
## The analytical question

Quantitative investment research is fundamentally a discipline of **falsification**. A researcher claims to have discovered an algorithmic signal that generates positive risk-adjusted excess return (alpha). Before allocating capital, an institutional investment committee demands a formal statistical hypothesis test:

$$\text{Does this observed outperformance represent true repeatable skill, or is it merely sampling noise?}$$

A classical hypothesis test establishes two mutually exclusive propositions:
1. **The Null Hypothesis ($H_0$)**: The baseline hypothesis of "no effect," "no skill," or "zero alpha." We assume $H_0$ is true until the data provides overwhelming evidence to the contrary:
   $$H_0: \alpha \le 0$$
2. **The Alternative Hypothesis ($H_a$)**: The research proposition we hope to substantiate:
   $$H_a: \alpha > 0$$

When evaluating a sample test statistic, the researcher faces two unavoidable errors:

$$\begin{array}{|c|c|c|}
\hline
\textbf{Decision} & H_0 \textbf{ is Actually True (No Skill)} & H_0 \textbf{ is Actually False (Real Alpha)} \\
\hline
\textbf{Reject } H_0 & \textbf{Type I Error } (\alpha) & \textbf{Correct Decision: Power } (1 - \beta) \\
& \text{False Positive: False claim of skill} & \text{True Positive: Capital allocated to real edge} \\
\hline
\textbf{Fail to Reject } H_0 & \textbf{Correct Decision } (1 - \alpha) & \textbf{Type II Error } (\beta) \\
& \text{Avoided allocating capital to noise} & \text{False Negative: Missed true edge} \\
\hline
\end{array}$$

For testing a sample mean against a hypothesized benchmark ($\mu_0 = 0$) when population variance is unknown:

$$t = \frac{\bar{X} - \mu_0}{s / \sqrt{n}} = \frac{\bar{X}}{s_{\bar{X}}}$$

Where $t$ follows a Student's t-distribution with $df = n - 1$.

An analyst must understand the exact definition of a **p-value**:
- The p-value is the probability of observing a test statistic at least as extreme as the one calculated from the sample, *assuming the null hypothesis is true*.
- If $p \le \alpha$ (e.g., $p \le 0.05$), we reject $H_0$.
- **Failure to reject $H_0$ is NOT proof that $H_0$ is true!** It simply means the sample data is insufficient to distinguish the observed result from random noise.

## A worked example

Let us evaluate an algorithmic statistical arbitrage fund that claims to produce positive monthly alpha:
- Hypothesized benchmark: $H_0: \alpha \le 0.0\%$ vs $H_a: \alpha > 0.0\%$ (one-tailed test).
- Sample observation period: $n = 36\text{ months}$ ($3\text{ years}$).
- Sample Mean Monthly Alpha: $\hat{\alpha} = +0.30\%$ ($30\text{ basis points}$).
- Sample Standard Deviation of Alpha: $s = 1.20\%$.
- Pre-set significance level: $\alpha = 0.05$ ($5\%$).

Let us calculate the test statistic step-by-step:
1. Calculate the Standard Error of the Alpha Estimate:
   $$s_{\bar{\alpha}} = \frac{s}{\sqrt{n}} = \frac{1.20\%}{\sqrt{36}} = \frac{1.20\%}{6} = 0.20\%$$
2. Compute the t-statistic:
   $$t = \frac{\hat{\alpha} - 0}{s_{\bar{\alpha}}} = \frac{0.30\%}{0.20\%} = 1.50$$
3. Determine the Critical Value:
   For a one-tailed test with $df = 36 - 1 = 35$ at $\alpha = 0.05$:
   $$t_{\text{critical}} \approx 1.690$$
   For a two-tailed test at $\alpha = 0.05$:
   $$t_{\text{critical}} \approx 2.030$$

Evaluate the decision:
Since calculated $t = 1.50 < t_{\text{critical}} = 1.690$ (one-tailed p-value $\approx 0.071 > 0.05$):
- **Decision**: **Fail to reject the null hypothesis $H_0$**.
- **Interpretation**: Although the sample generated a positive average alpha of $30\text{ bps}$, this result is not statistically distinguishable from random sampling noise over 36 months. The fund manager has not demonstrated statistically significant skill at the $5\%$ level.

## Research discipline

When conducting hypothesis tests in financial research:
1. **Pre-Specify Hypotheses and Significance Levels Before Looking at Data**: Setting the significance level $\alpha$ after observing the sample result is unethical data snooping.
2. **Never Confuse Statistical Significance with Economic Significance**: A high-frequency signal on 10 million trades might have a massive t-statistic of $t = 8.0$ with a mean return of $0.001\%$. If transaction fees and bid-ask spreads are $0.02\%$, the signal is statistically significant but economically bankrupt!
3. **Audit Serial Correlation in Test Residuals**: If monthly alpha is serially correlated, the standard error $s / \sqrt{n}$ is artificially suppressed, artificially inflating the t-statistic. Use Newey-West adjusted standard errors.
4. **Demand High Power ($1 - \beta$) for Rejecting Alpha**: If a sample has only 12 months, the test has low statistical power, meaning it has a high probability of committing a Type II error (failing to recognize a real edge due to a small sample).
""",
        r"t=\frac{\bar{X}-\mu_0}{s/\sqrt{n}};\quad \text{p-value}=P(|T| \ge |t| \mid H_0)",
        'from math import sqrt\nalpha_mean = 0.003\ns = 0.012\nn = 36\nse = s / sqrt(n)\nt_stat = alpha_mean / se\nprint("Standard error of alpha (%):", round(se * 100, 3))\nprint("Calculated t-statistic:", round(t_stat, 3))\nprint("Significant at 5% 1-tailed (t > 1.690):", t_stat > 1.690)',
        "A quantitative strategy generates a sample mean monthly excess return of 0.40% across n = 64 months with sample standard deviation of 1.60%. Test the null hypothesis H0: μ ≤ 0 against Ha: μ > 0 at the 5% significance level (critical t = 1.669). Calculate the t-statistic and state your investment conclusion.",
        "Standard error is se = s / √n = 1.60% / √64 = 1.60% / 8 = 0.20%. The t-statistic is t = (0.40% − 0%) / 0.20% = 2.00. Because calculated t = 2.00 exceeds the critical value of 1.669 (p-value ≈ 0.025 < 0.05), we reject the null hypothesis at the 5% significance level. The strategy demonstrates statistically significant positive excess return over this 64-month sample.",
        [
            q(
                "A monthly alpha estimate is +0.30% with a standard error of 0.20%. What is its calculated t-statistic against zero?",
                ["0.67", "1.50", "3.00"],
                1,
                "The t-statistic is 0.30% / 0.20% = 1.50.",
            ),
            q(
                "In hypothesis testing, what is a Type I error?",
                [
                    "Rejecting the null hypothesis when it is actually true (a false positive claim of outperformance)",
                    "Failing to reject the null hypothesis when it is false",
                    "Calculating standard deviation incorrectly",
                ],
                0,
                "A Type I error occurs when random noise is mistaken for genuine statistical outperformance.",
            ),
            q(
                "If an analyst fails to reject the null hypothesis H0: α = 0 at the 5% significance level, what does this mathematically prove?",
                [
                    "It proves that alpha is exactly equal to zero with 100% certainty",
                    "It proves the strategy will lose money in the future",
                    "It establishes that the observed sample data does not provide sufficient evidence to distinguish the return from random sampling noise",
                ],
                2,
                "Failing to reject the null indicates insufficient evidence against H0; it is never mathematical proof that the null is true.",
            ),
        ],
    )

    add(
        "2.13",
        6,
        "Multiple testing and robust comparisons",
        "Control false discovery rates when testing multiple signals and eliminate p-hacking.",
        r"""
## The analytical question

In the era of automated algorithmic research, computing power allows researchers to backtest thousands of potential trading rules, technical indicators, and machine-learning feature combinations in minutes. This creates the most severe crisis in quantitative finance: **The Multiple Testing Problem (p-hacking / data dredging)**.

Under standard hypothesis testing at a significance level of $\alpha = 0.05$:
- The probability of falsely rejecting a true null hypothesis on a single test is $5.0\%$.
- If an algorithm tests $m = 100$ independent variables, each of which is complete random noise ($H_0$ is true for all 100 variables), the **Expected Number of False Discoveries** is:
  $$E[\text{False Positives}] = m \times \alpha = 100 \times 0.05 = 5\text{ false discoveries!}$$

The probability of finding **at least one** falsely "statistically significant" signal ($p < 0.05$) among 100 random noise factors is:

$$P(\text{At least one false positive}) = 1 - (1 - \alpha)^m = 1 - (0.95)^{100} = 1 - 0.0059 = 99.41\%!$$

If a quantitative team tests 100 noise factors and reports only the single factor that achieved $p = 0.01$, they are presenting pure luck as algorithmic genius. When deployed in live trading with real capital, the strategy collapses immediately.

To prevent multiple testing failure, quantitative researchers enforce two rigorous corrections:
1. **The Bonferroni Correction**: Controls the **Family-Wise Error Rate (FWER)**—the probability of making even a single Type I error across all $m$ tests:
   $$\alpha^* = \frac{\alpha_{\text{family}}}{m}$$
   If you test $m = 50$ signals with a desired family-wise error of $\alpha = 0.05$, an individual test must achieve:
   $$p \le \frac{0.05}{50} = 0.001$$
2. **The Benjamini-Hochberg (FDR) Procedure**: In large-scale feature screening ($m = 1,000$), Bonferroni is often excessively conservative, discarding real discoveries. The **False Discovery Rate (FDR)** controls the expected proportion of false positives among all rejected tests:
   - Rank all $m$ p-values in ascending order: $p_{(1)} \le p_{(2)} \le \dots \le p_{(m)}$.
   - Find the largest index $k$ such that:
     $$p_{(k)} \le \frac{k}{m} \times Q^*$$
   - Reject all null hypotheses for $i = 1, 2, \dots, k$.

## A worked example

Let us evaluate a quantitative research team that tests $m = 20$ distinct moving average crossover signals on foreign exchange pairs:
- All 20 signals are applied to historical market data.
- The team enforces a strict Family-Wise Error Rate of $\alpha_{\text{family}} = 0.05$.

Calculate the required threshold:
1. Individual Bonferroni Significance Threshold:
   $$\alpha^* = \frac{0.05}{20} = 0.0025$$
2. The team sorts the resulting p-values for the top three signals:
   - Signal A: $p = 0.0012$
   - Signal B: $p = 0.0084$
   - Signal C: $p = 0.0320$

Evaluate the findings:
- An undisciplined researcher exclaims: *"All three signals passed! Their p-values are all below 0.05!"*
- The disciplined quantitative committee responds:
  - Signal C ($p = 0.0320 > 0.0025$): **Rejected**. Pure selection noise.
  - Signal B ($p = 0.0084 > 0.0025$): **Rejected**. Failed Bonferroni threshold.
  - Signal A ($p = 0.0012 \le 0.0025$): **Accepted for out-of-sample forward paper testing**.

Out of three apparent discoveries, only Signal A survives multiple testing correction.

## Research discipline

To eliminate multiple testing bias and p-hacking in quantitative operations:
1. **Maintain an Immutable Research Trial Ledger**: Log every single trial, backtest, indicator, and parameter combination ever tested—including all failed trials.
   $$\text{Disclose } m = \text{Total Trials Attempted}$$
2. **Lock Down the Out-of-Sample Holdout Dataset**: Never allow researchers access to the final test dataset while tuning parameters. The final evaluation period must be opened exactly once after the model is frozen.
3. **Apply the Harvey-Liu-Zhu t-Statistic Hurdle**: For stock market anomaly research where hundreds of factors have been published in academic literature, raise the required t-statistic hurdle from $t = 2.0$ to $t \ge 3.0$ ($p \le 0.0027$).
4. **Enforce Economic Plausibility**: Never accept a signal purely because it passed a mathematical test. Demand a clear, falsifiable economic mechanism (e.g., liquidity supply friction, regulatory constraint, or institutional mandate).
""",
        r"\alpha^*=\frac{\alpha_{\text{family}}}{m};\quad E[\text{False Positives}]=m \times \alpha;\quad p_{(k)} \le \frac{k}{m}Q^*",
        'm_trials = 100\nalpha_single = 0.05\nexpected_false = m_trials * alpha_single\nprob_none = 1.0\nfor trial in range(m_trials):\n    prob_none = prob_none * (1 - alpha_single)\nprob_at_least_one = 1 - prob_none\nprint("Expected false discoveries from 100 noise tests:", int(expected_false))\nprint("Probability of at least one false positive (%):", round(prob_at_least_one * 100, 2))\nbonferroni_thresh = alpha_single / m_trials\nprint("Bonferroni required threshold:", bonferroni_thresh)',
        "A quantitative researcher tests 50 uncorrelated potential momentum indicators against a null hypothesis of zero alpha at the 5% significance level. Calculate: (1) the expected number of false discoveries if all 50 indicators are pure noise, (2) the probability of finding at least one falsely significant indicator, and (3) the Bonferroni-corrected threshold required to maintain a 5% family-wise error rate.",
        "Expected false discoveries = m × α = 50 × 0.05 = 2.5 false positive signals. Probability of at least one false discovery = 1 − (1 − 0.05)⁵⁰ = 1 − (0.95)⁵⁰ = 1 − 0.0769 = 92.31%. Bonferroni-corrected threshold = α / m = 0.05 / 50 = 0.0010 (0.10%). Any signal must achieve p ≤ 0.001 to be considered statistically significant across the family of 50 trials.",
        [
            q(
                "If a researcher tests 100 pure random noise signals at a 5% individual significance level, what is the expected number of false positive discoveries?",
                ["0", "5", "50"],
                1,
                "Expected false discoveries = m × α = 100 × 0.05 = 5.",
            ),
            q(
                "Ten predefined statistical tests are conducted under a Bonferroni correction to maintain an overall family-wise error rate of 1.0% (0.01). What is the required individual test threshold?",
                ["0.01", "0.10", "0.001"],
                2,
                "Bonferroni threshold is α / m = 0.01 / 10 = 0.001.",
            ),
            q(
                "Why is reporting only the best-performing strategy out of 50 explored variations without disclosing the other 49 considered a serious research defect?",
                [
                    "It conceals multiple testing bias and presents what is likely random selection noise as genuine predictive skill",
                    "It violates copyright law",
                    "It increases computer memory usage",
                ],
                0,
                "Testing many variations inflates the chance of finding a lucky result; concealing unsuccessful trials invalidates reported p-values.",
            ),
        ],
    )

    # -------------------------------------------------------------------------
    # CHAPTER 7: SIMPLE LINEAR REGRESSION
    # -------------------------------------------------------------------------

    add(
        "2.5",
        7,
        "Linear regression & correlation",
        "Fit an ordinary least squares regression, interpret slope and intercept, and evaluate correlation.",
        r"""
## The analytical question

Simple linear regression models the linear relationship between a dependent response variable ($Y$) and a single independent explanatory variable ($X$):

$$Y_i = \beta_0 + \beta_1 X_i + \epsilon_i$$

Where:
- $\beta_0$ is the true population intercept.
- $\beta_1$ is the true population slope coefficient.
- $\epsilon_i$ is the unobservable random disturbance term.

In financial asset pricing, the most famous application is the **Capital Asset Pricing Model (CAPM) / Single-Index Model**:

$$R_{i,t} - R_{f,t} = \alpha_i + \beta_i (R_{m,t} - R_{f,t}) + \epsilon_{i,t}$$

Where $\beta_i$ measures systematic market exposure, and $\alpha_i$ represents excess risk-adjusted return.

Under **Ordinary Least Squares (OLS)**, the regression line is estimated by minimizing the **Sum of Squared Residuals ($SSE$)**:

$$\min_{\hat{\beta}_0, \hat{\beta}_1} \sum_{i=1}^n e_i^2 = \sum_{i=1}^n (Y_i - \hat{Y}_i)^2$$

Solving the OLS first-order conditions yields the exact closed-form estimators:

$$\hat{\beta}_1 = \frac{\sum_{i=1}^n (X_i - \bar{X})(Y_i - \bar{Y})}{\sum_{i=1}^n (X_i - \bar{X})^2} = \frac{\text{Cov}(X, Y)}{\text{Var}(X)} = r_{X,Y} \frac{s_Y}{s_X}$$

$$\hat{\beta}_0 = \bar{Y} - \hat{\beta}_1 \bar{X}$$

Two foundational properties govern OLS residuals:
1. **The residuals sum to exactly zero**: $\sum_{i=1}^n e_i = 0$.
2. **The regression line passes through the center of gravity**: $(\bar{X}, \bar{Y})$ lies on the fitted line.

To measure the proportion of total variation in $Y$ explained by the linear relationship with $X$, we compute the **Coefficient of Determination ($R^2$)**:

$$R^2 = \frac{\text{Explained Sum of Squares (SSR)}}{\text{Total Sum of Squares (SST)}} = 1 - \frac{\text{SSE}}{\text{SST}} = r_{X,Y}^2$$

In simple linear regression with an intercept, $R^2$ is exactly equal to the square of the Pearson correlation coefficient ($r_{X,Y}^2$).

## A worked example

Let us evaluate the systematic risk exposure of Alder Capital Fund relative to the market index across three monthly observations:
- Market Excess Returns ($X$): $\{1.0\%, 2.0\%, 3.0\%\}$
- Fund Excess Returns ($Y$): $\{2.0\%, 3.0\%, 5.0\%\}$

Let us calculate the OLS coefficients by hand step-by-step:
1. Calculate Sample Means:
   $$\bar{X} = \frac{1 + 2 + 3}{3} = 2.0\%$$
   $$\bar{Y} = \frac{2 + 3 + 5}{3} = \frac{10}{3} \approx 3.333\%$$
2. Compute Deviations and Covariance Numerator:
   - For $i=1$: $(1 - 2)(2 - 3.333) = (-1)(-1.333) = +1.333$
   - For $i=2$: $(2 - 2)(3 - 3.333) = (0)(-0.333) = 0.000$
   - For $i=3$: $(3 - 2)(5 - 3.333) = (1)(+1.667) = +1.667$
   $$\sum (X_i - \bar{X})(Y_i - \bar{Y}) = 1.333 + 0 + 1.667 = 3.00$$
3. Compute Variance Denominator of $X$:
   $$\sum (X_i - \bar{X})^2 = (1 - 2)^2 + (2 - 2)^2 + (3 - 2)^2 = (-1)^2 + 0^2 + 1^2 = 1 + 0 + 1 = 2.00$$
4. Calculate OLS Slope ($\hat{\beta}_1$):
   $$\hat{\beta}_1 = \frac{3.00}{2.00} = 1.50$$
5. Calculate OLS Intercept ($\hat{\beta}_0$):
   $$\hat{\beta}_0 = \bar{Y} - \hat{\beta}_1 \bar{X} = 3.333 - (1.50 \times 2.0) = 3.333 - 3.00 = +0.333\% \quad (1/3\%)$$
   The fitted regression equation is:
   $$\hat{Y} = 0.333 + 1.50 X$$

Now verify the residual property:
- For $X_1 = 1$: $\hat{Y}_1 = 0.333 + 1.5 = 1.833 \implies e_1 = 2.0 - 1.833 = +0.167$
- For $X_2 = 2$: $\hat{Y}_2 = 0.333 + 3.0 = 3.333 \implies e_2 = 3.0 - 3.333 = -0.333$
- For $X_3 = 3$: $\hat{Y}_3 = 0.333 + 4.5 = 4.833 \implies e_3 = 5.0 - 4.833 = +0.167$
$$\sum e_i = +0.167 - 0.333 + 0.167 = 0.000 \quad (\text{Exact verification!})$$

Now consider a predictive scenario:
If the market excess return next month is $X = 2.0\%$, the predicted fund excess return is $\hat{Y} = 0.333 + 1.5(2.0) = 3.333\%$.
If the fund's actual observed return is $Y = 3.0\%$, the residual is $e = 3.0\% - 3.333\% = -0.333\%$.

## Research discipline

When using linear regression in investment analysis:
1. **Never Confuse Correlation with Causation**: A high $R^2$ between ice cream sales and drowning rates does not mean eating ice cream causes drowning; both are driven by a third confounding variable (summer heat).
2. **Always Verify Linear Assumptions**: Plot residuals against fitted values ($\hat{Y}$). If the residual plot exhibits a curved U-shape, the underlying relationship is non-linear, rendering linear regression invalid.
3. **Audit Outlier Leverage**: In small financial samples, a single extreme market crash day can single-handedly rotate the OLS regression slope by $40\%$. Calculate Cook's Distance to detect influential data points.
4. **Distinguish Sample Fit from Out-of-Sample Performance**: An in-sample $R^2$ of $60\%$ often collapses to $R^2 \le 0$ when evaluated on out-of-sample forward market data.
""",
        r"\hat{\beta}_1=\frac{\text{Cov}(X,Y)}{\text{Var}(X)};\quad \hat{\beta}_0=\bar{Y}-\hat{\beta}_1\bar{X};\quad R^2=r_{X,Y}^2",
        'x = [1.0, 2.0, 3.0]\ny = [2.0, 3.0, 5.0]\nmean_x = sum(x) / len(x)\nmean_y = sum(y) / len(y)\ncov_xy = 0.0\nvar_x = 0.0\nfor i in range(len(x)):\n    cov_xy = cov_xy + (x[i] - mean_x) * (y[i] - mean_y)\n    var_x = var_x + (x[i] - mean_x) ** 2\nbeta_1 = cov_xy / var_x\nbeta_0 = mean_y - beta_1 * mean_x\nprint("OLS slope (beta_1):", beta_1)\nprint("OLS intercept (beta_0):", round(beta_0, 4))',
        "In a fitted single-index model, a fund's excess return is estimated as: Y = 0.10% + 1.20 X, where X is the market excess return. For a month in which the market excess return is 2.0% and the fund's actual observed excess return is 3.0%, calculate the model's predicted return and the residual. Explain the economic meaning of the residual.",
        "Predicted return is Ŷ = 0.10% + 1.20 × (2.0%) = 0.10% + 2.40% = 2.50%. The residual is e = Y − Ŷ = 3.00% − 2.50% = +0.50 percentage points (+50 bps). The +0.50% residual represents the portion of the fund's excess return for that specific month that cannot be explained by systematic market exposure; it represents idiosyncratic performance (a combination of manager selection and random noise).",
        [
            q(
                "In a simple linear regression of Y on X, the Pearson correlation coefficient between X and Y is r = 0.60. What is the coefficient of determination (R^2)?",
                ["0.36", "0.60", "0.77"],
                0,
                "In simple linear regression, R^2 = r^2 = (0.60)^2 = 0.36 (36% of the variation in Y is explained by X).",
            ),
            q(
                "A fund regression yields a fitted equation: Return = 0.2% + 1.1 × Market. If the market returns 3.0% and the fund actually returns 4.0%, what is the residual?",
                ["+0.5%", "+3.5%", "−0.5%"],
                0,
                "Predicted return is 0.2% + 1.1(3.0%) = 3.5%. Residual is actual − predicted = 4.0% − 3.5% = +0.5%.",
            ),
            q(
                "What is a mathematical property guaranteed to hold for ordinary least squares (OLS) residuals when an intercept is included?",
                [
                    "The sum of the residuals is always strictly positive",
                    "The sum of the residuals is exactly zero",
                    "All residuals are equal to each other",
                ],
                1,
                "The OLS first-order condition forces the sum of the residuals to equal exactly zero when an intercept is included.",
            ),
        ],
    )

    add(
        "2.14",
        7,
        "Regression uncertainty and prediction intervals",
        "Calculate the standard error of estimate, evaluate ANOVA tables, and build prediction intervals.",
        r"""
## The analytical question

Fitting an OLS regression line is only the first step. Because the slope ($\hat{\beta}_1$) and intercept ($\hat{\beta}_0$) are estimated from a finite sample of data, they carry statistical sampling uncertainty.

To measure the dispersion of the observed data points around the fitted regression line, we compute the **Standard Error of the Estimate ($s_e$)**:

$$s_e = \sqrt{\frac{\sum_{i=1}^n (Y_i - \hat{Y}_i)^2}{n - 2}} = \sqrt{\frac{SSE}{n - 2}}$$

Notice the degrees of freedom: we divide by $n - 2$ because two parameters ($\beta_0$ and $\beta_1$) were estimated from the data.

The standard error of the slope coefficient estimator ($\hat{\beta}_1$) is:

$$s_{\hat{\beta}_1} = \frac{s_e}{\sqrt{\sum_{i=1}^n (X_i - \bar{X})^2}}$$

To test whether the independent variable has a statistically significant linear relationship with $Y$, we formulate:
$$H_0: \beta_1 = 0 \quad \text{vs} \quad H_a: \beta_1 \ne 0$$
$$t = \frac{\hat{\beta}_1 - 0}{s_{\hat{\beta}_1}} \quad (df = n - 2)$$

Now consider the vital distinction between two types of intervals for a given explanatory value $X_0$:
1. **Confidence Interval for the Expected Mean Response ($E[Y \mid X_0]$)**: Estimates where the *average* value of $Y$ will fall across many repetitions:
   $$s_{\text{mean}}^2 = s_e^2 \left[ \frac{1}{n} + \frac{(X_0 - \bar{X})^2}{\sum (X_i - \bar{X})^2} \right]$$
2. **Prediction Interval for an Individual New Observation ($Y_0$)**: Predicts where a *single future observation* will fall. This must incorporate both uncertainty in the regression line AND the inherent variance of the new disturbance term ($\sigma^2$):
   $$s_f^2 = s_e^2 \left[ 1 + \frac{1}{n} + \frac{(X_0 - \bar{X})^2}{\sum (X_i - \bar{X})^2} \right]$$

$$\text{A prediction interval is ALWAYS substantially wider than a confidence interval of the mean.}$$

In corporate inventory and risk management, mistaking a confidence interval of the mean for a prediction interval of individual demand causes catastrophic stockouts and bankruptcy!

## A worked example

Let us evaluate the weekly sales forecasting model of Alder Manufacturing's distribution depot:
- Regression model: $Y = \text{Weekly Unit Demand}$, $X = \text{Regional Activity Index}$.
- For next week, the model predicts an average demand of $\hat{Y}_0 = 100\text{ units}$.
- Standard error of estimate: $s_e = 10\text{ units}$.
- Sample size: $n = 30\text{ weeks}$.
- Activity index is at its sample mean ($X_0 = \bar{X}$).

Let us compare the two intervals at a 95% level ($t_{\text{crit}} \approx 2.048$):

### Interval 1: Confidence Interval for Average Weekly Demand
$$s_{\text{mean}} = s_e \sqrt{\frac{1}{n}} = 10 \times \sqrt{\frac{1}{30}} = 10 \times 0.1826 = 1.826\text{ units}$$
$$\text{Margin of Error} = 2.048 \times 1.826 = 3.74\text{ units}$$
$$\text{95% Mean Interval: } [100 - 3.74, 100 + 3.74] = [96.26, 103.74\text{ units}]$$
Management says: *"Look! Average demand will not exceed 104 units. If we stock 105 units, we are 95% safe from running out!"*

### Interval 2: Prediction Interval for NEXT WEEK'S Actual Demand
The warehouse does not deliver an average over 30 weeks; it must satisfy the *specific individual customer orders* arriving next week!
$$s_f = s_e \sqrt{1 + \frac{1}{n}} = 10 \times \sqrt{1 + \frac{1}{30}} = 10 \times \sqrt{1.0333} = 10 \times 1.0165 = 10.165\text{ units}$$
$$\text{Margin of Error} = 2.048 \times 10.165 = 20.82\text{ units}$$
$$\text{95% Prediction Interval: } [100 - 20.82, 100 + 20.82] = [79.18, 120.82\text{ units}]$$

Look at the revelation!
Actual demand next week can easily reach **$121\text{ units}$**!
If the depot stocked only $105$ units based on the confidence interval of the mean, it faces a massive **$16$-unit stockout**! Management confused average demand with individual observation variance.

## Research discipline

When evaluating regression inference and predictions:
1. **Always Use Prediction Intervals for Risk and Inventory Sizing**: Any decision regarding VaR, capital adequacy, or physical stock must be sized to the prediction interval ($s_f$), never the confidence interval of the mean ($s_{\text{mean}}$).
2. **Inspect the ANOVA (Analysis of Variance) Table**:
   - $SST = SSR + SSE$
   - Check the F-statistic: $F = \frac{MSR}{MSE} = \frac{SSR / 1}{SSE / (n - 2)}$. In simple linear regression, $F = t^2$ exactly.
3. **Beware of Extrapolation Far from the Sample Mean**:
   Notice the term $\frac{(X_0 - \bar{X})^2}{\sum (X_i - \bar{X})^2}$ in both interval formulas. The further $X_0$ is from historical sample average $\bar{X}$, the wider the interval balloons. Making predictions for extreme market conditions far outside historical ranges yields massive uncertainty.
4. **Audit Homoskedasticity Assumptions**: Both interval formulas assume that residual variance $\sigma^2$ is constant across all values of $X$. If the data displays heteroskedasticity (e.g., higher volatility during market drops), the standard formulas are invalid.
""",
        r"s_e=\sqrt{\frac{SSE}{n-2}};\quad s_f=s_e\sqrt{1+\frac{1}{n}+\frac{(X_0-\bar{X})^2}{\sum(X_i-\bar{X})^2}}",
        'from math import sqrt\nse = 10.0\nn = 30\nt_crit = 2.048\nse_mean = se * sqrt(1 / n)\nse_pred = se * sqrt(1 + 1 / n)\nprint("SE of mean response:", round(se_mean, 3))\nprint("95% CI of mean margin (+/-):", round(t_crit * se_mean, 2))\nprint("SE of prediction:", round(se_pred, 3))\nprint("95% Prediction interval margin (+/-):", round(t_crit * se_pred, 2))',
        "A sales regression yields a standard error of estimate se = 8 units from n = 25 observations. At X0 = X̄, the predicted demand is 80 units. Using critical t = 2.069 (df = 23), calculate: (1) the 95% confidence interval for the mean demand, and (2) the 95% prediction interval for an individual week's demand. Explain why the prediction interval is wider.",
        "For mean demand: se_mean = 8 × √(1/25) = 8 × 0.20 = 1.60. Margin of error = 2.069 × 1.60 = 3.31. 95% CI of mean = [80 − 3.31, 80 + 3.31] = [76.69, 83.31]. For individual prediction: se_pred = 8 × √(1 + 1/25) = 8 × √1.04 = 8 × 1.0198 = 8.158. Margin of error = 2.069 × 8.158 = 16.88. 95% Prediction interval = [80 − 16.88, 80 + 16.88] = [63.12, 96.88]. The prediction interval is much wider because it must account for both uncertainty in the estimated regression parameters AND the unpredictable random error (ε) of the individual week itself.",
        [
            q(
                "Why is a prediction interval for an individual future observation Y0 always wider than a confidence interval for the expected mean response E[Y | X0]?",
                [
                    "Because predicting an individual outcome involves both parameter estimation uncertainty and the random variance of the individual disturbance term",
                    "Because prediction intervals use fewer degrees of freedom",
                    "Because confidence intervals assume zero variance",
                ],
                0,
                "An individual observation contains random disturbance noise (s_e^2) that averages out when estimating the population mean.",
            ),
            q(
                "In a simple linear regression with n = 20 observations, how many degrees of freedom are associated with the standard error of estimate (SSE)?",
                ["20", "19", "18"],
                2,
                "Degrees of freedom for SSE in simple linear regression is n − 2 = 20 − 2 = 18 (two parameters are estimated: slope and intercept).",
            ),
            q(
                "What happens to the width of both confidence intervals of the mean and prediction intervals as the explanatory variable X0 moves further away from its historical sample mean X̄?",
                [
                    "The intervals become narrower",
                    "The intervals expand and become wider due to greater leverage uncertainty",
                    "The intervals remain exactly the same width everywhere",
                ],
                1,
                "The term (X0 − X̄)^2 increases as X0 diverges from the sample mean, expanding estimation uncertainty.",
            ),
        ],
    )

    # =========================================================================
    # PART II: ADVANCED QUANTITATIVE APPLICATIONS (CHAPTERS 8 - 14)
    # =========================================================================

# -------------------------------------------------------------------------
    # CHAPTER 8: MULTIPLE REGRESSION AND DIAGNOSTICS
    # -------------------------------------------------------------------------

    add(
        "2.15",
        8,
        "Multiple regression and categorical effects",
        "Interpret a coefficient conditional on other regressors and construct an identifiable model specification.",
        r"""
## The analytical question

Asset returns and corporate performance metrics almost never depend on a single isolated variable. In cross-sectional and time-series finance, an analyst must model how an outcome variable ($y$, such as excess equity return) varies across multiple simultaneous influences ($x_1, x_2, \dots, x_k$, such as market exposure, size, value, momentum, and sector indicators).

The classical multiple linear regression specification is:

$$y_i = \beta_0 + \beta_1 x_{1i} + \beta_2 x_{2i} + \cdots + \beta_k x_{ki} + \epsilon_i,\quad i=1, 2, \dots, n$$

where:
- $\beta_0$ is the intercept term (expected value of $y$ when all explanatory regressors equal zero).
- $\beta_j = \frac{\partial E[y|X]}{\partial x_j}$ is the **partial slope coefficient**, quantifying the expected change in $y$ associated with a one-unit increase in $x_j$, **holding all other regressors in the specification constant** ($ceteris\ paribus$).
- $\epsilon_i$ is the unobserved disturbance term, assumed under classical Gauss-Markov conditions to satisfy $E[\epsilon_i|X] = 0$, $Var(\epsilon_i|X) = \sigma^2$ (homoskedasticity), and $Cov(\epsilon_i, \epsilon_j|X) = 0$ for $i \neq j$ (no autocorrelation).

When explanatory variables correlate with one another, the meaning of each slope is strictly conditional on the other regressors included in the model. If a critical regressor $x_2$ is omitted from the specification, the estimated slope $\hat{\beta}_1$ on $x_1$ suffers from **omitted variable bias**:

$$\hat{\beta}_1 \xrightarrow{p} \beta_1 + \beta_2 \frac{Cov(x_1, x_2)}{Var(x_1)}$$

If $Cov(x_1, x_2) \neq 0$ and $\beta_2 \neq 0$, the single-variable regression will misattribute the effect of $x_2$ to $x_1$, producing biased, inconsistent estimates and invalidating causal or factor-risk interpretations.

Categorical attributes (such as industry sector, exchange listing, credit rating tier, or monetary policy regime) are incorporated into multiple regressions using qualitative **dummy indicator variables** ($D_i \in \{0, 1\}$). To avoid exact linear dependence—the notorious **dummy variable trap**—a model with an intercept $\beta_0$ spanning $M$ mutually exclusive categories must include exactly $M - 1$ dummy indicators:

$$y_i = \beta_0 + \sum_{m=1}^{M-1} \gamma_m D_{mi} + \sum_{j=1}^k \beta_j x_{ji} + \epsilon_i$$

Here, the omitted category serves as the baseline **reference benchmark**. The coefficient $\gamma_m$ represents the differential intercept shift for category $m$ relative to that omitted reference category, holding all continuous covariates fixed. If all $M$ indicators were included alongside an intercept, $\sum_{m=1}^M D_{mi} = 1 = x_{0i}$, causing the design matrix $(\mathbf{X}^T\mathbf{X})$ to be singular and non-invertible.

Furthermore, interaction terms ($x_{1i} \times D_i$) allow the slope sensitivity of continuous variables to differ across categories or regimes, enabling tests of structural slope shifts.

Overall model fit is measured by the **coefficient of determination** ($R^2$):

$$R^2 = \frac{SSR}{SST} = 1 - \frac{SSE}{SST}$$

Because adding any regressor—even pure random noise—weakly increases $R^2$, analysts rely on **adjusted $R^2$** ($\bar{R}^2$), which penalizes model complexity by scaling sums of squares by their respective degrees of freedom:

$$\bar{R}^2 = 1 - \left[\frac{SSE / (n - k - 1)}{SST / (n - 1)}\right] = 1 - \frac{s_e^2}{s_y^2}$$

To test whether the full set of $k$ explanatory variables jointly explains a statistically significant proportion of variance in $y$, we conduct an **overall $F$-test**:

$$H_0: \beta_1 = \beta_2 = \cdots = \beta_k = 0 \quad \text{versus} \quad H_a: \text{at least one } \beta_j \neq 0$$

$$F = \frac{MSR}{MSE} = \frac{(SST - SSE) / k}{SSE / (n - k - 1)} = \frac{R^2 / k}{(1 - R^2) / (n - k - 1)} \sim F_{k,\, n - k - 1}$$

## A worked example

A quantitative analyst models monthly equity excess returns ($y_i$, in percentage points) using three regressors: broad market excess return ($x_{1i}$), value factor spread ($x_{2i}$), and a binary indicator for the Technology sector ($D_i$, where $D_i = 1$ if Technology, $0$ for the omitted reference sector, Industrials):

$$\hat{y}_i = 0.20 + 1.10 \times \text{market}_i + 0.40 \times \text{value}_i + 0.30 \times \text{sector}_i$$

Consider an investment scenario where the market excess return is $+2.0$ percentage points, the value factor is $-1.0$ percentage point, and the security belongs to the Technology sector ($D_i = 1$):

1. **Calculate the fitted return**:
   $$\hat{y} = 0.20 + (1.10 \times 2.0) + (0.40 \times -1.0) + (0.30 \times 1.0)$$
   $$\hat{y} = 0.20 + 2.20 - 0.40 + 0.30 = 2.30 \text{ percentage points}$$

2. **Economic interpretation of coefficients**:
   - The slope on market ($1.10$) indicates that for every $1.0$ percentage point increase in market excess return, the asset's expected excess return increases by $1.10$ percentage points, *holding value exposure and sector classification fixed*.
   - The coefficient on the Technology sector dummy ($+0.30$) indicates that a Technology firm earns an estimated $0.30$ percentage points higher return per month than an otherwise identical Industrials firm with identical market and value exposures.
   - The intercept ($0.20$) represents the baseline expected return for an Industrials firm ($D_i = 0$) when market and value factor excess returns are both zero.

## Research discipline

Before estimating or comparing multiple regression models:
1. **Specify economic rationale**: Motivate every regressor with prior economic theory. Data-mining algorithms that indiscriminately throw dozens of financial ratios into a regression produce in-sample overfit that collapses out-of-sample.
2. **Prevent the dummy variable trap**: Always verify that the number of category indicators equals $M - 1$ when an intercept is included. Explicitly identify and document the reference category.
3. **Do not confuse prediction with causal intervention**: A statistically significant partial correlation does not imply that manipulating a firm's characteristics will engineer a higher stock return.
""",
        r"y=\beta_0+\beta_1x_1+\cdots+\beta_kx_k+\epsilon",
        'market = 2\nvalue = -1\nsector = 1\nprint("Fitted return (percentage points):", .2 + 1.1 * market + .4 * value + .3 * sector)',
        "For y = 1 + 2x − 0.5z + 0.4D, predict at x=3, z=2, D=1. Explain how three mutually exclusive sector categories should be encoded when an intercept is present.",
        "Prediction is 6.4 (1 + 2*3 - 0.5*2 + 0.4*1 = 1 + 6 - 1 + 0.4 = 6.4). Use two indicators and one reference category with the intercept; including all three indicators creates exact linear dependence.",
        [
            q(
                "In multiple linear regression, how is an individual slope coefficient β_j interpreted?",
                [
                    "As the expected change in the dependent variable per unit change in x_j, holding all other regressors in the specification fixed",
                    "As the unconditional correlation between x_j and y, completely ignoring other variables",
                    "As absolute mathematical proof that changing x_j causes an identical change in y",
                ],
                0,
                "Partial slope coefficients quantify conditional marginal effects, holding all other included regressors constant (ceteris paribus).",
            ),
            q(
                "When modeling four mutually exclusive credit rating categories in a regression containing an intercept term, how many dummy indicator variables must be included?",
                [
                    "Four indicators plus the intercept",
                    "Three indicators, reserving one category as the baseline reference benchmark",
                    "Zero indicators, because categorical variables cannot be modeled in linear regression",
                ],
                1,
                "To avoid exact multicollinearity (the dummy variable trap), an intercept specification requires M − 1 = 4 − 1 = 3 indicators.",
            ),
            q(
                "A quantitative model estimates y = 1 + 0.5x + 2z. If an observation has x = 4 and z = −1, what is the fitted value ŷ?",
                ["5", "3", "1"],
                2,
                "ŷ = 1 + (0.5 × 4) + (2 × −1) = 1 + 2 − 2 = 1 in the stated response units.",
            ),
        ],
    )

    add(
        "2.16",
        8,
        "Diagnostics: unstable coefficients and invalid standard errors",
        "Identify multicollinearity, heteroskedasticity, serial correlation, and influential observations.",
        r"""
## The analytical question

Ordinary Least Squares (OLS) regression relies on key structural assumptions to produce Best Linear Unbiased Estimates (BLUE). When these assumptions are violated in real-world market datasets, regression models can generate deceptive in-sample fits, severely unstable coefficients, and invalid hypothesis tests.

Institutional quantitative researchers must systematically diagnose four major econometric defects:

1. **Multicollinearity**: Occurs when two or more explanatory regressors are highly linearly correlated.
   - *Consequences*: OLS coefficient estimates remain unbiased and consistent, but their sampling variances and standard errors explode:
     $$Var(\hat{\beta}_j) = \frac{\sigma^2}{(1 - R_j^2) \sum_{i=1}^n (x_{ji} - \bar{x}_j)^2} = \frac{\sigma^2}{\sum (x_{ji} - \bar{x}_j)^2} \times VIF_j$$
     where $VIF_j = \frac{1}{1 - R_j^2}$ is the **Variance Inflation Factor** obtained from regressing $x_j$ on all other regressors.
   - *Diagnostic Symptoms*: A classic symptom is a high overall regression $R^2$ and a statistically significant global $F$-statistic, yet virtually none of the individual $t$-statistics are statistically significant!
   - *Remedies*: Check pairwise correlation matrices ($|r| > 0.70$) and $VIF > 5 \text{ to } 10$. Drop redundant collinear regressors, transform variables into ratios/differences, or apply regularized ridge regression.

2. **Heteroskedasticity**: Occurs when the variance of the error terms is not constant across observations ($Var(\epsilon_i|X) = \sigma_i^2 \neq \sigma^2$).
   - *Unconditional heteroskedasticity* (variance fluctuates unrelated to regressors) does not bias OLS standard errors.
   - *Conditional heteroskedasticity* (error variance depends on the levels of explanatory variables) severely biases conventional OLS standard errors (typically understating them), leading to artificially inflated $t$-statistics and false discoveries (Type I errors).
   - *Detection*: Breusch-Pagan test ($n R^2_{aux} \sim \chi^2_k$) or White's test.
   - *Remedy*: Calculate **White-Huber heteroskedasticity-consistent (HC) robust standard errors**. Note that robust standard errors correct hypothesis tests; they do not alter the OLS point estimates $\hat{\beta}$.

3. **Serial Correlation (Autocorrelation)**: Occurs in time-series regressions when error terms correlate across time periods ($Cov(\epsilon_t, \epsilon_{t-s}) \neq 0$).
   - *Consequences*: Positive serial correlation (common in financial time series) causes OLS residuals to cluster, dramatically understating standard errors and overstating $t$-statistics and $F$-statistics.
   - *Detection*: Durbin-Watson statistic ($DW \approx 2(1 - r)$, where $DW \approx 2$ indicates no first-order serial correlation, $DW < 2$ indicates positive autocorrelation) or Breusch-Godfrey LM test.
   - *Remedy*: Use **Newey-West Heteroskedasticity and Autocorrelation Consistent (HAC) standard errors**, or model the dynamic error structure directly with autoregressive time-series terms.

4. **Influential Observations and Outliers**: High leverage points ($h_{ii}$) and extreme residuals that exert disproportionate pull on the regression plane. Measured via **Cook's Distance** ($D_i$):

$$D_i = \frac{e_i^2}{(k + 1) s_e^2} \left[\frac{h_{ii}}{(1 - h_{ii})^2}\right]$$

Observations with $D_i > \frac{4}{n}$ warrant immediate structural investigation.

## A worked example

A financial econometrician fits a predictive regression for monthly hedge fund alpha. The estimated slope coefficient is $\hat{\beta} = 0.30$.

1. **Under conventional textbook OLS assumptions**:
   - The reported conventional standard error is $SE_{OLS}(\hat{\beta}) = 0.10$.
   - The test statistic against $H_0: \beta = 0$ is:
     $$t_{conventional} = \frac{\hat{\beta}}{SE_{OLS}(\hat{\beta})} = \frac{0.30}{0.10} = 3.00$$
   - At a 5% significance level (critical value $\approx 1.96$), the $p$-value is $< 0.01$, leading the analyst to claim statistically significant positive alpha.

2. **Under diagnostic testing**:
   - The Durbin-Watson statistic is $1.20$, indicating strong positive serial correlation in the monthly residuals.
   - Re-estimating uncertainty using Newey-West HAC robust standard errors yields $SE_{HAC}(\hat{\beta}) = 0.20$.
   - The corrected test statistic is:
     $$t_{robust} = \frac{\hat{\beta}}{SE_{HAC}(\hat{\beta})} = \frac{0.30}{0.20} = 1.50$$
   - Because $1.50 < 1.96$, the null hypothesis of zero alpha **cannot be rejected** ($p \approx 0.13$). The apparent statistical significance was an artifact of ignoring time-series dependence!

## Research discipline

Institutional quants must adhere to strict diagnostic protocols:
- **Never claim alpha based solely on OLS standard errors**: Always compute and report Newey-West HAC or clustered standard errors alongside OLS estimates.
- **Robust standard errors do not repair omitted variable bias**: If the conditional mean function is misspecified, or if critical risk factors are omitted, robust standard errors merely yield consistent standard errors for a biased coefficient!
- **Do not blindly delete market crisis outliers**: A market crash observation (e.g., October 1987, March 2020) carries genuine tail-risk information. Removing it merely to boost regression $R^2$ creates catastrophic vulnerability in live deployment.
""",
        r"t=\hat\beta/SE(\hat\beta)",
        'coefficient = .30\nprint("Conventional statistic:", coefficient / .10)\nprint("Dependence-aware statistic:", coefficient / .20)',
        "A coefficient is 0.24 with conventional standard error 0.08 and robust standard error 0.16. Compare statistics and explain one problem robust standard errors do not solve.",
        "The statistics are 3.0 and 1.5. Robust uncertainty estimates adjust the covariance matrix for heteroskedasticity and autocorrelation, but they cannot repair omitted-variable bias, look-ahead data leakage, or a misspecified conditional mean.",
        [
            q(
                "What is a classic diagnostic symptom of severe multicollinearity in multiple regression?",
                [
                    "A high overall regression R-squared and significant F-statistic, yet individual regressors have large standard errors and insignificant t-statistics",
                    "A Durbin-Watson statistic equal to exactly 2.0",
                    "A negative sum of squared errors",
                ],
                0,
                "Multicollinearity inflates coefficient variances and standard errors, making individual partial slopes appear statistically insignificant despite strong joint predictive power.",
            ),
            q(
                "Which modeling defect is NOT resolved by calculating White or Newey-West robust standard errors?",
                [
                    "Omitted variable bias and structural model misspecification",
                    "Conditional heteroskedasticity in the residuals",
                    "Serial correlation in time-series error terms",
                ],
                0,
                "Robust standard errors correct inference under non-ideal disturbance structures; they cannot rectify a biased conditional mean caused by omitted variables or incorrect functional form.",
            ),
            q(
                "A quantitative factor slope is 0.50 with a revised dependence-aware standard error of 0.25. What is the test statistic against zero?",
                ["0.125", "2.0", "4.0"],
                1,
                "t = 0.50 / 0.25 = 2.0, which compares the point estimate to its corrected standard error.",
            ),
        ],
    )

    # -------------------------------------------------------------------------
    # CHAPTER 9: TIME-SERIES ANALYSIS AND FORECASTING
    # -------------------------------------------------------------------------

    add(
        "2.17",
        9,
        "Time-series dependence and stationarity",
        "Distinguish a stable autoregressive process from a unit-root process and avoid spurious level regressions.",
        r"""
## The analytical question

Financial market observations arrive in chronological order. Unlike cross-sectional data, where observations are assumed to be independent draws, time series exhibit temporal dependence: yesterday's volatility, liquidity, or macro conditions directly influence today's state.

Statistical inference and forecasting in time series require the underlying data-generating process to be **covariance stationary** (or weakly stationary). A discrete-time stochastic process $\{x_t\}$ is covariance stationary if it satisfies three strict conditions:
1. **Constant mean**: The expected value is constant and finite across all time:
   $$E[x_t] = \mu < \infty \quad \forall t$$
2. **Constant variance**: The unconditional variance is constant and finite across all time:
   $$Var(x_t) = \gamma_0 < \infty \quad \forall t$$
3. **Stationary autocovariance**: The covariance between two values depends only on the lag displacement $k$, not on the calendar date $t$:
   $$Cov(x_t, x_{t-k}) = E[(x_t - \mu)(x_{t-k} - \mu)] = \gamma_k \quad \forall t, k$$

The foundational baseline model for persistent financial time series is the **first-order autoregressive model, AR(1)**:

$$x_t = b_0 + b_1 x_{t-1} + \epsilon_t,\quad \epsilon_t \sim WN(0, \sigma^2)$$

where $\epsilon_t$ is independent white-noise disturbance with mean zero and constant variance $\sigma^2$.

If $|b_1| < 1$, the AR(1) process is covariance stationary. Taking expectations on both sides yields its **unconditional mean reversion level** ($\mu$):

$$E[x_t] = b_0 + b_1 E[x_{t-1}] \implies \mu = b_0 + b_1 \mu \implies \mu = \frac{b_0}{1 - b_1}$$

The term $(1 - b_1)$ represents the speed of mean reversion. The **half-life** of a shock is given by $t_{1/2} = \frac{\ln(0.5)}{\ln(b_1)}$. For an AR(1) process starting at $x_t$, the multi-step ahead conditional forecast converges geometrically toward the long-run mean:

$$\hat{x}_{t+h} = \mu + b_1^h (x_t - \mu)$$

When $b_1 = 1$, the process possesses a **unit root** and becomes a **random walk** (with drift if $b_0 \neq 0$):

$$x_t = b_0 + x_{t-1} + \epsilon_t \implies x_t = x_0 + b_0 t + \sum_{i=1}^t \epsilon_i$$

A unit root violates covariance stationarity: its variance grows linearly with time ($Var(x_t) = t \sigma^2 \to \infty$ as $t \to \infty$), and historical shocks persist forever with no mean reversion.

Attempting to fit OLS regressions on non-stationary price levels produces **spurious regression**: independent trending series exhibit artificially high $R^2$ values and statistically significant $t$-statistics simply because both series trend with time ($DW \to 0$, $R^2 > DW$). 

Stationarity is verified using the **Dickey-Fuller (DF)** or **Augmented Dickey-Fuller (ADF)** unit root test:

$$\Delta x_t = b_0 + g x_{t-1} + \sum_{j=1}^p \psi_j \Delta x_{t-j} + \epsilon_t$$

testing $H_0: g = 0$ (unit root, non-stationary) versus $H_a: g < 0$ (stationary, mean-reverting) against non-standard Dickey-Fuller critical values. If a unit root is present, first-differencing ($\Delta x_t = x_t - x_{t-1}$) transforms the series into a stationary $I(0)$ process.

If two non-stationary $I(1)$ series share a common stochastic drift such that a linear combination $y_t - \beta x_t = \epsilon_t \sim I(0)$ is stationary, the series are **cointegrated**, forming the mathematical basis for statistical arbitrage pairs trading.

## A worked example

An automated statistical arbitrage model tracks an interest-rate spread described by an estimated stationary AR(1) process:

$$x_t = 0.20 + 0.80 x_{t-1} + \epsilon_t$$

1. **Calculate the long-run stationary mean**:
   $$\mu = \frac{b_0}{1 - b_1} = \frac{0.20}{1 - 0.80} = \frac{0.20}{0.20} = 1.00 \text{ percentage point}$$

2. **Forecast future values from an initial spread $x_t = 2.00$**:
   - One-step ahead forecast ($t+1$):
     $$\hat{x}_{t+1} = 0.20 + (0.80 \times 2.00) = 0.20 + 1.60 = 1.80 \text{ points}$$
   - Two-step ahead forecast ($t+2$):
     $$\hat{x}_{t+2} = 0.20 + (0.80 \times 1.80) = 0.20 + 1.44 = 1.64 \text{ points}$$
   - Three-step ahead forecast ($t+3$):
     $$\hat{x}_{t+3} = 0.20 + (0.80 \times 1.64) = 0.20 + 1.312 = 1.512 \text{ points}$$

Notice how the conditional forecast steadily decays toward the unconditional long-run equilibrium of $1.00$. If $b_1$ were equal to $1.0$, the denominator $(1 - b_1)$ would be zero; the process would exhibit no finite mean reversion, rendering stationary spread trading models completely invalid.

## Research discipline

Before conducting time-series research or deploying pairs trading algorithms:
1. **Never regress non-stationary price levels**: Always test for unit roots using the Augmented Dickey-Fuller (ADF) test. If unit roots are detected, either difference the series to returns or prove cointegration via the Engle-Granger two-step test.
2. **Examine residual autocorrelations**: After fitting an AR model, inspect the autocorrelation function (ACF) of the residuals. If residuals exhibit autocorrelation, add higher-order autoregressive lags ($p$) until errors are pure white noise.
3. **Beware structural regime shifts**: A series may appear stationary over a 5-year sample yet experience a permanent parameter break during a central bank regime change.
""",
        r"E[x]=c/(1-\phi),\quad |\phi|<1",
        'intercept = .2\nphi = .8\nvalue = 2\nprint("Stationary mean:", intercept / (1 - phi))\nfor step in range(3):\n    value = intercept + phi * value\n    print("Forecast:", value)',
        "For x_t = 0.3 + 0.5x_(t−1) + error, calculate the stationary mean and one-step forecast from x=1.2. Explain why phi=1 changes the analysis.",
        "Stationary mean is 0.3 / (1 - 0.5) = 0.6. One-step forecast is 0.3 + 0.5*1.2 = 0.9. At phi=1, the denominator (1 - phi) becomes zero; the process possesses a unit root (random walk), lacks a finite mean-reversion level, and shocks persist permanently.",
        [
            q(
                "What mathematical condition must the autoregressive parameter b_1 satisfy for an AR(1) process to be covariance stationary?",
                [
                    "|b_1| < 1.0",
                    "b_1 = 1.0 exactly",
                    "b_1 > 1.0",
                ],
                0,
                "Covariance stationarity requires that the absolute value of the autoregressive slope be strictly less than 1 (|b_1| < 1).",
            ),
            q(
                "What econometric failure occurs when two completely independent non-stationary random walks are regressed against each other?",
                [
                    "A spurious regression exhibiting falsely high R-squared and misleadingly significant t-statistics",
                    "A guaranteed profitable cointegrated pairs-trading strategy",
                    "An exact zero correlation in every sample",
                ],
                0,
                "Spurious regressions occur when non-stationary trending series generate deceptive statistical significance despite having zero structural relationship.",
            ),
            q(
                "An AR(1) process is parameterized as x_t = 0.40 + 0.60 x_{t-1} + ε_t. What is its long-run stationary mean reversion level?",
                ["0.40", "0.60", "1.00"],
                2,
                "μ = b_0 / (1 − b_1) = 0.40 / (1 − 0.60) = 0.40 / 0.40 = 1.00.",
            ),
        ],
    )

    add(
        "2.18",
        9,
        "Forecast evaluation and changing volatility",
        "Evaluate forecasts chronologically and distinguish conditional volatility from an unconditional average.",
        r"""
## The analytical question

A forecasting model's in-sample fit is virtually useless for evaluating real-world investment efficacy. In quantitative trading, models must be evaluated strictly **out-of-sample** using historical walk-forward cross-validation schemes that preserve the chronological arrow of time:
- **Expanding window**: The model is initially trained on an anchor period (e.g., years 1–5), predicts year 6, then re-estimates parameters on years 1–6 to predict year 7.
- **Rolling window**: The model maintains a fixed historical window (e.g., most recent 60 months), dropping the oldest month as each new month is added, allowing parameters to adapt to structural evolution.

Forecast errors are defined as $e_{t+h} = y_{t+h} - \hat{y}_{t+h|t}$, where $\hat{y}_{t+h|t}$ is formed strictly using information available at or before time $t$. We summarize performance across $T$ out-of-sample evaluation periods using two loss functions:
1. **Mean Absolute Error (MAE)**: Measures average absolute magnitude under linear loss:
   $$\text{MAE} = \frac{1}{T}\sum_{t=1}^T |e_t|$$
2. **Root Mean Squared Error (RMSE)**: Penalizes large outlier errors under quadratic loss:
   $$\text{RMSE} = \sqrt{\frac{1}{T}\sum_{t=1}^T e_t^2}$$

Because RMSE squares each error before taking the square root, $\text{RMSE} \ge \text{MAE}$, with equality holding only when all error magnitudes are identical. For strategies with asymmetric payoff profiles or liquidity penalties, large forecast errors are disproportionately disastrous, making RMSE a critical risk metric.

Crucially, return volatility in financial markets is not constant; it exhibits **volatility clustering** (large price shocks cluster together). While an unconditional variance ($\sigma^2$) assumes risk is identical every day, risk managers require **conditional volatility** ($\sigma_t^2$), which updates dynamically as new market shocks arrive.

The **Exponentially Weighted Moving Average (EWMA / RiskMetrics)** volatility model updates conditional variance recursively:

$$\sigma_t^2 = \lambda \sigma_{t-1}^2 + (1 - \lambda) \epsilon_{t-1}^2$$

where:
- $\lambda \in (0, 1)$ is the exponential persistence decay factor (standardly $\lambda = 0.94$ for daily market data).
- $\epsilon_{t-1}^2$ is the most recent squared shock (return innovation).
- $(1 - \lambda)$ is the sensitivity weight placed on the latest market event.

In more general econometric settings, the **GARCH(1,1)** process models conditional variance with an explicit long-run mean reversion anchor:

$$\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$$

where covariance stationarity requires $\alpha + \beta < 1$, yielding an unconditional long-run variance of $V_L = \frac{\omega}{1 - \alpha - \beta}$.

## A worked example

A quantitative momentum strategy records three consecutive out-of-sample monthly forecast errors (in percentage points): $+1.0$, $-2.0$, and $+1.0$.

1. **Calculate out-of-sample evaluation metrics**:
   - Absolute errors: $|1| = 1.0$, $|-2| = 2.0$, $|1| = 1.0$. Sum $= 4.0$.
     $$\text{MAE} = \frac{4.0}{3} = 1.333 \text{ percentage points}$$
   - Squared errors: $1^2 = 1.0$, $(-2)^2 = 4.0$, $1^2 = 1.0$. Sum $= 6.0$.
     $$\text{MSE} = \frac{6.0}{3} = 2.000 \implies \text{RMSE} = \sqrt{2.000} \approx 1.414 \text{ percentage points}$$
   - Notice that RMSE ($1.414$) is larger than MAE ($1.333$) because it penalizes the $-2.0$ point forecast miss more aggressively.

2. **Recursive conditional volatility update**:
   - Assume yesterday's conditional variance was $\sigma_{t-1}^2 = 0.000100$ (equivalent to $1.00\%$ daily volatility).
   - A sudden geopolitical event produces a daily return shock of $\epsilon_{t-1} = 0.020$ ($2.00\%$, with squared shock $\epsilon_{t-1}^2 = 0.000400$).
   - Using decay parameter $\lambda = 0.94$:
     $$\sigma_t^2 = (0.94 \times 0.000100) + (0.06 \times 0.000400)$$
     $$\sigma_t^2 = 0.000094 + 0.000024 = 0.000118$$
   - The updated conditional volatility is:
     $$\sigma_t = \sqrt{0.000118} \approx 0.010863 \implies 1.086\% \text{ per day}$$
   The single $2\%$ market move immediately raises the portfolio's estimated daily risk from $1.00\%$ to $1.086\%$.

## Research discipline

When evaluating predictive models and estimating market risk:
1. **Never use standard random $k$-fold cross-validation**: Shuffling time-series observations leaks future information into past training sets, producing spuriously inflated accuracy metrics.
2. **Compare against naive benchmarks**: A complex machine learning forecast must be compared against a random-walk baseline ($\hat{y}_{t+1} = y_t$) or historical moving average. If the complex model cannot beat naive benchmarks out-of-sample, it should not be deployed.
3. **Audit conditional risk before sizing positions**: Sizing positions using a static unconditional variance during a high-volatility regime will result in severe leverage blowups.
""",
        r"\sigma_t^2=\lambda\sigma_{t-1}^2+(1-\lambda)\epsilon_{t-1}^2",
        'from math import sqrt\nerrors = [1, -2, 1]\nabsolute = 0\nsquared = 0\nfor error in errors:\n    absolute = absolute + abs(error)\n    squared = squared + error ** 2\nprint("MAE:", absolute / len(errors))\nprint("RMSE:", sqrt(squared / len(errors)))\nprint("Updated volatility:", sqrt(.94 * .0001 + .06 * .02 ** 2))',
        "Forecast errors are 0, 0, and 3. Calculate MAE and RMSE. Explain why a random row split may be unsuitable for a forecasting study.",
        "MAE is (0+0+3)/3 = 1.0. MSE is (0+0+9)/3 = 3.0, so RMSE is √3 ≈ 1.732. Random row splits violate time chronology, leaking future observations into training folds and contaminating evaluation across dependent serial boundaries.",
        [
            q(
                "Why must quantitative time-series models be evaluated using chronological walk-forward splits rather than random k-fold cross-validation?",
                [
                    "Because random shuffling leaks future information into training splits and destroys serial correlation structures",
                    "Because Python code cannot execute random splits on arrays",
                    "Because chronological splits guarantee 100% forecasting accuracy",
                ],
                0,
                "In financial time series, future data cannot be used to predict the past. Chronological splits preserve information causality.",
            ),
            q(
                "Compared to Mean Absolute Error (MAE), Root Mean Squared Error (RMSE) places disproportionate penalty on:",
                ["Large outlier forecast errors", "Ticker symbol changes", "Zero-error predictions"],
                0,
                "Squaring deviations before taking the average penalizes large errors quadratically, reflecting severe costs of large market misses.",
            ),
            q(
                "Two forecast errors are −2.0 and +2.0. What is their Root Mean Squared Error (RMSE)?",
                ["0.0", "4.0", "2.0"],
                2,
                "MSE = [(-2)^2 + (2)^2] / 2 = (4 + 4) / 2 = 4.0. RMSE = √4.0 = 2.0.",
            ),
        ],
    )

    # -------------------------------------------------------------------------
    # CHAPTER 10: MACHINE LEARNING IN FINANCE
    # -------------------------------------------------------------------------

    add(
        "2.19",
        10,
        "Machine learning: objectives, validation, and regularization",
        "Define a learning task and control model complexity without allowing the test set to guide development.",
        r"""
## The analytical question

Machine learning (ML) algorithms excel at uncovering complex, nonlinear patterns and interactions across vast feature spaces. However, in financial markets characterized by low signal-to-noise ratios, non-stationarity, and competitive arbitrage, flexible ML models face an acute danger: **overfitting**.

The generalization performance of any statistical learner is governed by the **Bias-Variance Tradeoff**:

$$E\left[\left(y - \hat{f}(x)\right)^2\right] = \text{Bias}\left[\hat{f}(x)\right]^2 + Var\left[\hat{f}(x)\right] + \sigma_\epsilon^2$$

where:
- $\text{Bias}\left[\hat{f}(x)\right] = E\left[\hat{f}(x)\right] - f(x)$ measures approximation error from overly restrictive model assumptions (underfitting).
- $Var\left[\hat{f}(x)\right] = E\left[\left(\hat{f}(x) - E[\hat{f}(x)]\right)^2\right]$ measures model sensitivity to the specific training sample (overfitting to sample noise).
- $\sigma_\epsilon^2$ is irreducible intrinsic market noise.

To prevent flexible models from memorizing historical noise, institutional quants apply **penalized regularization**, augmenting the empirical loss function with a complexity penalty:

$$\min_{\boldsymbol{\beta}} \left\{ \frac{1}{n} \sum_{i=1}^n \left(y_i - \mathbf{x}_i^T\boldsymbol{\beta}\right)^2 + \mathcal{P}(\boldsymbol{\beta}; \lambda) \right\}$$

Two primary regularization regimes dominate quantitative finance:

1. **Ridge Regression ($L_2$ Penalty)**:
   $$\mathcal{P}_{ridge}(\boldsymbol{\beta}) = \lambda \sum_{j=1}^k \beta_j^2 = \lambda \|\boldsymbol{\beta}\|_2^2$$
   Ridge regression shrinks coefficients continuously toward zero without forcing them to exactly zero. Analytically, it stabilizes the matrix inversion in OLS by adding a positive constant $\lambda$ along the diagonal: $\hat{\boldsymbol{\beta}}_{ridge} = (\mathbf{X}^T\mathbf{X} + \lambda \mathbf{I})^{-1}\mathbf{X}^T\mathbf{y}$. This eliminates collinearity blowups.

2. **Lasso Regression ($L_1$ Penalty - Least Absolute Shrinkage and Selection Operator)**:
   $$\mathcal{P}_{lasso}(\boldsymbol{\beta}) = \lambda \sum_{j=1}^k |\beta_j| = \lambda \|\boldsymbol{\beta}\|_1$$
   Because the $L_1$ ball possesses sharp geometric corners at the coordinate axes, Lasso drives uninformative or redundant coefficients to **identically zero**, performing automated feature selection and producing sparse, interpretable models.

3. **Elastic Net**: Combines both $L_1$ and $L_2$ penalties ($\lambda_1 \|\boldsymbol{\beta}\|_1 + \lambda_2 \|\boldsymbol{\beta}\|_2^2$), effectively grouping correlated regressors while performing feature selection.

**Critical Data Preprocessing Rule**: Because regularization penalties depend directly on the absolute numerical scale of coefficients, **all features must be standardized** ($z = \frac{x - \mu}{\sigma}$) prior to fitting. The standardization parameters ($\mu_{train}, \sigma_{train}$) must be computed **strictly on training folds**, then applied forward without refitting on validation and test folds. Computing scalers across the full dataset introduces catastrophic look-ahead leakage.

## A worked example

A quantitative research team compares two regularized factor-selection models on training data using an objective function with ridge penalty $\lambda = 0.10$:

$$\mathcal{L}_{obj} = \text{MSE}_{train} + \lambda \sum_{j=1}^k \beta_j^2$$

- **Model A (Parsimonious Factor Model)**:
  - Training mean squared error: $\text{MSE}_{train} = 0.80$
  - Sum of squared coefficients: $\sum \beta_j^2 = 1.0$
  - Penalized loss: $\mathcal{L}_A = 0.80 + (0.10 \times 1.0) = 0.90$

- **Model B (Over-parameterized 50-Feature Model)**:
  - Training mean squared error: $\text{MSE}_{train} = 0.60$ (superior raw in-sample fit)
  - Sum of squared coefficients: $\sum \beta_j^2 = 9.0$ (large, leveraged coefficients)
  - Penalized loss: $\mathcal{L}_B = 0.60 + (0.10 \times 9.0) = 0.60 + 0.90 = 1.50$

Although Model B achieves a 25% lower in-sample training error ($0.60$ vs $0.80$), its aggressive coefficient magnitudes incur a heavy regularization penalty ($0.90$), making Model A the superior choice under the penalized objective ($0.90 < 1.50$).

## Research discipline

To maintain scientific integrity in machine learning pipelines:
1. **Never touch the test set during hyperparameter tuning**: The test set must remain completely frozen in a digital vault until model architecture, feature sets, and $\lambda$ penalties are finalized on validation folds. Iterating on the test set turns it into an informal training set.
2. **Implement Purged and Embargoed Walk-Forward Cross-Validation**: Standard random k-fold cross-validation leaks information when labels overlap across time (e.g., 20-day forward returns). Training sets must purge overlapping event windows and embargo immediate post-event data.
3. **Interpretability is a risk control**: If an ML model cannot provide economic feature attributions (via SHAP values or partial dependence plots), unexpected market regime changes will trigger unmanageable drawdown risks.
""",
        r"L_{ridge}=MSE+\lambda\sum_j\beta_j^2",
        'penalty = .1\nprint("Model A penalized objective:", .8 + penalty * 1)\nprint("Model B penalized objective:", .6 + penalty * 9)',
        "Compare model C with MSE 0.5 and squared-coefficient sum 4 against D with MSE 0.7 and sum 1, using lambda 0.1. Describe which dataset may select lambda.",
        "Model C objective: 0.5 + 0.1*4 = 0.9. Model D objective: 0.7 + 0.1*1 = 0.8. Model D is preferred. Lambda must be selected using validation folds within the training history, never by evaluating against the frozen final test set.",
        [
            q(
                "Why must feature scalers (mean and standard deviation) be fitted strictly on the training partition and only applied forward to validation and test data?",
                [
                    "Fitting scalers on the full dataset leaks information from future test periods into model training",
                    "Because test sets never contain numerical data",
                    "To ensure that regression coefficients sum to exactly one",
                ],
                0,
                "Estimating normalization parameters across the entire dataset introduces look-ahead data leakage, invalidating out-of-sample claims.",
            ),
            q(
                "What unique mathematical property distinguishes Lasso (L1) regularization from Ridge (L2) regularization?",
                [
                    "Lasso can shrink coefficients to identically zero, performing automated feature selection",
                    "Lasso always increases the sum of squared errors",
                    "Lasso works only on single-variable regressions",
                ],
                0,
                "The L1 penalty constraint geometry drives non-critical coefficients to zero, creating sparse feature representations.",
            ),
            q(
                "A model has MSE = 0.40, a sum of squared coefficients equal to 5.0, and a ridge penalty parameter λ = 0.20. What is its penalized objective score?",
                ["0.60", "1.40", "5.40"],
                1,
                "Score = MSE + λ × (sum of β^2) = 0.40 + (0.20 × 5.0) = 0.40 + 1.00 = 1.40.",
            ),
        ],
    )

    add(
        "2.20",
        10,
        "Classification, clustering, and economic evaluation",
        "Read a confusion matrix and explain why accuracy alone can be misleading for rare financial events.",
        r"""
## The analytical question

Many critical financial decisions are categorical rather than continuous: Will a corporate borrower default on its debt ($y \in \{0, 1\}$)? Will the central bank hike interest rates? Will an earnings announcement trigger a gap breakout?

In binary classification, model performance on $N$ evaluation instances is recorded in a **confusion matrix**:

$$\begin{array}{c|cc}
& \textbf{Actual Positive } (y=1) & \textbf{Actual Negative } (y=0) \\
\hline
\textbf{Predicted Positive } (\hat{y}=1) & \text{True Positive } (TP) & \text{False Positive } (FP) \\
\textbf{Predicted Negative } (\hat{y}=0) & \text{False Negative } (FN) & \text{True Negative } (TN)
\end{array}$$

Standard diagnostic metrics derived from these counts include:
- **Accuracy**: $\frac{TP + TN}{TP + FP + FN + TN}$ (overall fraction of correct classifications).
- **Precision (Positive Predictive Value)**: $\frac{TP}{TP + FP}$ (of all instances flagged by the model as positive, what fraction are truly positive?).
- **Recall (Sensitivity / True Positive Rate)**: $\frac{TP}{TP + FN}$ (of all actual positive events that occurred in the world, what fraction did the model successfully detect?).
- **Specificity (True Negative Rate)**: $\frac{TN}{TN + FP}$.
- **$F_1$-Score**: Harmonic mean of Precision and Recall:
  $$F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} = \frac{2TP}{2TP + FP + FN}$$

**The Accuracy Paradox**: In financial datasets, catastrophic events (bankruptcy, flash crashes, sovereign defaults) are extremely rare (e.g., $1\%$ base rate). A naive classifier that blindly predicts "no default" for $100\%$ of cases achieves a dazzling **$99\%$ accuracy**, yet its recall is **$0\%$**—it detects zero defaults, rendering it useless to a credit risk manager!

Furthermore, in institutional finance, prediction errors carry asymmetric economic costs:
$$Cost(FN) \gg Cost(FP)$$
Failing to flag an impending corporate bankruptcy ($FN$) can destroy $100\%$ of invested bond principal, whereas investigating a false alarm ($FP$) costs only a few hours of analyst review time. Therefore, the classification decision threshold $p^*$ must be tuned to minimize expected economic loss:

$$p^* = \frac{Cost(FP)}{Cost(FP) + Cost(FN)}$$

In unsupervised learning, where outcomes lack labels, algorithms group data by structural similarity:
- **$K$-Means Clustering**: Partitions $n$ observations into $K$ clusters by minimizing within-cluster sum of squares (inertia):
  $$\min \sum_{k=1}^K \sum_{i \in S_k} \|\mathbf{x}_i - \boldsymbol{\mu}_k\|^2$$
- **Principal Component Analysis (PCA)**: Finds orthogonal linear combinations of features that maximize explained variance. However, high explained variance in PCA does not guarantee predictive power for future asset returns.

## A worked example

A credit risk division deploys a machine-learning warning model to screen 100 distressed corporate bond issuers. In reality, 10 firms subsequently default ($y=1$), and 90 firms remain solvent ($y=0$). The model flags 12 issuers as high-risk, yielding:
- True Positives ($TP$): $6$ (six defaulting firms successfully flagged).
- False Positives ($FP$): $6$ (six solvent firms mistakenly flagged).
- False Negatives ($FN$): $4$ (four defaulting firms missed).
- True Negatives ($TN$): $84$ (eighty-four solvent firms correctly cleared).

1. **Calculate standard metrics**:
   $$\text{Accuracy} = \frac{TP + TN}{N} = \frac{6 + 84}{100} = \frac{90}{100} = 90.0\%$$
   $$\text{Precision} = \frac{TP}{TP + FP} = \frac{6}{6 + 6} = \frac{6}{12} = 50.0\%$$
   $$\text{Recall} = \frac{TP}{TP + FN} = \frac{6}{6 + 4} = \frac{6}{10} = 60.0\%$$

2. **Evaluate the business utility**:
   - A naive baseline predicting zero defaults achieves $90.0\%$ accuracy with $0.0\%$ recall.
   - The ML model catches $60\%$ of actual defaults. Half of its warnings turn out to be true defaults ($\text{Precision} = 50\%$).
   - If avoiding a default saves $\$10{,}000{,}000$ and reviewing a false alarm costs $\$50{,}000$, the model delivers immense net economic value despite its seemingly modest $50\%$ precision.

## Research discipline

When designing classification systems for trading and risk:
1. **Never rely on raw accuracy**: Always evaluate Precision, Recall, and the Area Under the Receiver Operating Characteristic curve (ROC-AUC) or Precision-Recall curve (PR-AUC).
2. **Select probability thresholds based on the cost matrix**: Never default to an arbitrary $p = 0.50$ cutoff. Calibrate the threshold to balance financial losses between missed events and false alarms.
3. **Do not reify unsupervised clusters**: Identifying three clusters in asset returns does not mean you have discovered permanent "macro regimes." Cluster boundaries often shift radically across market crises.
""",
        r"Precision=TP/(TP+FP);\quad Recall=TP/(TP+FN)",
        'tp = 6\nfp = 6\nfn = 4\ntn = 84\nprint("Accuracy:", (tp + tn) / (tp + fp + fn + tn))\nprint("Precision:", tp / (tp + fp))\nprint("Recall:", tp / (tp + fn))',
        "A model has TP=8, FP=2, FN=12, TN=78. Calculate accuracy, precision, and recall. Explain whether a higher classification threshold is likely to improve recall.",
        "Accuracy is (8+78)/100 = 86%. Precision is 8/(8+2) = 80%. Recall is 8/(8+12) = 40%. Raising the classification threshold requires higher predicted probability to flag an event; this reduces total positive predictions, which generally lowers recall while potentially improving precision.",
        [
            q(
                "A fraud-detection algorithm generates 10 True Positives and 10 False Positives. What is its precision?",
                ["100%", "50%", "10%"],
                1,
                "Precision = TP / (TP + FP) = 10 / (10 + 10) = 50%. It measures the accuracy of positive flags.",
            ),
            q(
                "Why can an impressive 98% accuracy score be dangerously deceptive for predicting rare financial events like hedge fund blowups?",
                [
                    "Because a naive model can achieve 98% accuracy by always predicting 'no blowup', while completely failing to detect a single actual collapse",
                    "Because accuracy can only be calculated on small datasets",
                    "Because false positives are impossible in financial data",
                ],
                0,
                "In severely imbalanced classes, high accuracy is trivially obtained by predicting the majority class, obscuring zero detection ability (zero recall).",
            ),
            q(
                "A distress classifier identifies 9 of the 15 firms that actually went bankrupt. What is the recall of the model?",
                ["40%", "60%", "90%"],
                1,
                "Recall = TP / (TP + FN) = 9 / 15 = 60%.",
            ),
        ],
    )

    # -------------------------------------------------------------------------
    # CHAPTER 11: BIG DATA, TEXT FEATURES, AND PIPELINE ENGINEERING
    # -------------------------------------------------------------------------

    add(
        "2.21",
        11,
        "Point-in-time data engineering",
        "Build an auditable dataset with explicit keys, availability timestamps, and safe joins.",
        r"""
## The analytical question

Quantitative strategies fail in live production far more often from corrupted data engineering pipelines than from flawed mathematical algorithms. The primary culprit is **look-ahead bias** caused by improper handling of temporal availability.

In financial accounting and macroeconomic research, every data point involves three distinct timestamps:
1. **Period End Date ($t_{period}$)**: The fiscal calendar date being measured (e.g., Q4 ended December 31, 2024).
2. **Public Filing / Release Date ($t_{filing}$)**: The exact date when the data became publicly known to the market via SEC filing or government press release (e.g., 10-K filed March 15, 2025).
3. **Database Ingestion Timestamp ($t_{ingest}$)**: The precise second when the commercial vendor parsed, verified, and broadcast the record across feeds.

The iron rule of **Point-in-Time (PIT)** data architecture is:

$$t_{available} = \max(t_{filing}, t_{ingest}) \le t_{decision}$$

An investment algorithm executing a rebalance on February 1, 2025, **cannot** observe December 31, 2024 financial statements if they were not filed until March 15, 2025! Backtesting against period-end dates creates massive look-ahead bias, generating fictional backtest returns that vanish in live trading.

Furthermore, corporate fundamentals undergo repeated **accounting restatements** and macroeconomic data undergo revisions (e.g., GDP, non-farm payrolls). A true point-in-time database preserves historical **data vintages**, ensuring that a backtest run on historical dates observes only the preliminary vintage available on that day, not the restated figure finalized two years later.

Equally perilous is **entity resolution**:
- Ticker symbols are mutable and frequently recycled (e.g., a bankrupt firm's ticker assigned to an unrelated startup years later).
- Robust data pipelines link records using immutable permanent identifiers (such as CUSIP, SEDOL, FIGI, or CRSP PERMNO).
- Data joins must be audited for cardinality: joining a pricing table to an un-deduplicated corporate action or dividend table can trigger accidental Cartesian products ($1 \times M$ joins), multiplying rows, distorting weighting vectors, and fabricating phantom return shocks.

Finally, the historical research universe must be **survivorship-bias free**: delisted, acquired, and bankrupt firms must be preserved in historical investment universes. Excluding failed firms inflates historical strategy returns by $100 \text{ to } 300$ basis points annually.

## A worked example

A systematic equity factor fund runs an automated screening process on February 1, 2025 ($t_{decision} = \text{"2025-02-01"}$). The pipeline queries quarterly earnings per share (EPS) filings for a target company:
- Filing A: For fiscal quarter ending September 30, 2024; filed publicly on November 10, 2024 ($\text{EPS} = \$0.80$).
- Filing B: For fiscal quarter ending December 31, 2024; filed publicly on March 15, 2025 ($\text{EPS} = \$1.20$).

1. **Point-in-time eligibility filter**:
   - Filing A: $t_{available} = \text{"2024-11-10"} \le \text{"2025-02-01"} \implies \textbf{Eligible}$.
   - Filing B: $t_{available} = \text{"2025-03-15"} > \text{"2025-02-01"} \implies \textbf{Ineligible (Look-Ahead Violation)}$.

2. **Decision state**:
   The February 1 trading decision must strictly use Filing A ($\text{EPS} = \$0.80$). Even though the December quarter has physically ended, its financial figures are unknown to the market.

3. **Join cardinality check**:
   Suppose a daily price table has 100 unique `(security_id, date)` records. After performing a left join against a corporate fundamentals table, the output table expands to 120 rows.
   - The extra 20 rows indicate that 20 dates matched multiple records in the fundamental table (e.g., multiple share classes or duplicate restatements).
   - If not reconciled immediately, these duplicated rows will corrupt portfolio position weights, double-count exposures, and produce invalid trading signals.

## Research discipline

Institutional data engineering standards require:
1. **As-of timestamp indexing**: Structure all database joins using temporal constraints (`WHERE data.available_at <= decision.timestamp`).
2. **Validate join uniqueness before and after merge**: Assert `assert len(merged) == len(prices)` after joining pricing and feature tables.
3. **Capture delisting returns**: When a company defaults or delists, record its terminal delisting return (often $-30\%$ to $-100\%$). Replacing delisting missing values with zero generates severe survivorship bias.
""",
        r"\text{Eligible datum}:t_{available}\leq t_{decision}",
        'decision = "2025-02-01"\nfilings = [("2024-11-10", 8), ("2025-03-15", 12)]\navailable_date = ""\navailable_value = 0\nfor filing in filings:\n    if filing[0] <= decision and filing[0] > available_date:\n        available_date = filing[0]\n        available_value = filing[1]\nprint("Available filing:", available_date, available_value)',
        "A forecast is issued April 1. A quarter ends March 31 but results are released May 10. State which timestamp controls eligibility and list two checks after joining fundamentals to prices.",
        "The public release date (May 10) controls eligibility; the March 31 quarter data cannot enter an April 1 decision. After joins, verify: (1) row counts match exactly without duplicate fan-outs, and (2) all joined feature availability timestamps precede the decision date.",
        [
            q(
                "Which timestamp must be used to determine whether a corporate earnings figure is eligible for a historical backtest decision?",
                [
                    "The public filing / availability timestamp when the data was broadcast to the market",
                    "The fiscal period end date (e.g., quarter end)",
                    "Today's date when downloading the file from the internet",
                ],
                0,
                "Point-in-time eligibility requires using the public availability date; period-end dates precede public dissemination and introduce look-ahead bias.",
            ),
            q(
                "When joining a fundamental metrics table to a daily price series, the row count unexpectedly jumps from 5,000 to 5,800. What is the immediate required action?",
                [
                    "Accept the larger sample size because more data improves statistical power",
                    "Audit join keys and deduplicate one-to-many cardinality matches before running any analysis",
                    "Drop the price series entirely",
                ],
                1,
                "Duplicate join keys create phantom rows that distort portfolio weights and invalidate subsequent statistics.",
            ),
            q(
                "A corporate filing covering the period ending June 30 is released publicly on August 12. May an algorithmic trading model include this filing's data in a July 15 rebalancing signal?",
                [
                    "Yes, because June 30 occurred prior to July 15",
                    "Yes, provided the data vendor verified the numbers",
                    "No, because the data was not publicly available on July 15",
                ],
                2,
                "Using information released on August 12 for a July 15 trade constitutes look-ahead bias.",
            ),
        ],
    )

    add(
        "2.22",
        11,
        "Alternative data, text features, and reproducibility",
        "Turn unstructured observations into documented features while separating coverage, timing, and predictive value.",
        r"""
## The analytical question

Quantitative investment research increasingly leverages non-traditional, unstructured data: satellite imagery, supply-chain bills of lading, consumer credit card transaction panels, patent filings, and corporate natural language text (earnings call transcripts, 10-K/10-Q filings, and central bank communications).

Transforming unstructured financial text into predictive numerical features requires rigorous Natural Language Processing (NLP) pipelines:
1. **Corpus preprocessing**: Tokenization, lowercasing, stop-word removal, and lemmatization.
2. **Domain-Specific Sentiment Scoring**: General-purpose sentiment dictionaries (e.g., Harvard Psychosociological Dictionary) fail catastrophically in finance because standard business terms like *liability*, *depreciation*, *cost*, or *tax* are classified as negative words. Financial researchers rely on specialized lexicons, such as the **Loughran-McDonald (LM) Financial Sentiment Dictionary**.
3. **Normalized Sentiment Polarity**: A transparent, widely used baseline sentiment metric scales the difference between positive and negative word occurrences:

$$\text{Sentiment Score} = \frac{N_{positive} - N_{negative}}{N_{positive} + N_{negative}}$$

where $N_{positive}$ and $N_{negative}$ represent the counts of matched sentiment tokens within the document.
- If $N_{positive} + N_{negative} = 0$, the document contains zero sentiment tokens; the pipeline must assign a neutral score ($0.0$) and activate an explicit `has_sentiment` indicator flag rather than dividing by zero.

Beyond basic dictionary bag-of-words scoring, modern pipelines construct numerical feature vectors using **Term Frequency-Inverse Document Frequency (TF-IDF)**:

$$w_{t,d} = \text{TF}(t, d) \times \log\left(\frac{N}{\text{DF}(t)}\right)$$

or pre-trained financial transformer embeddings (e.g., FinBERT).

However, alternative datasets carry profound institutional risks:
- **Coverage expansion distortion**: When an alternative data vendor onboards new retail merchants or data partners, raw transaction counts surge. An analyst might misinterpret this technical vendor growth as booming underlying corporate sales.
- **Selection and survivorship bias**: Vendors often sell datasets covering only large, successful firms or surviving merchants, omitting failed entities.
- **Legal and compliance integrity**: Institutional firms must verify lawful acquisition, explicit terms of service, absence of Material Non-Public Information (MNPI), and adherence to privacy frameworks (GDPR, CCPA).
- **Auditability and reproducible lineage**: Every research output must track the source dataset version, parser Git commit SHA, random seed, and exact preprocessing parameters.

## A worked example

A quantitative research team extracts forward-looking statements from an earnings call transcript using an illustrative financial sentiment dictionary:
- Matched positive tokens (*accelerating*, *expanding*, *record*): $N_{positive} = 3$
- Matched negative tokens (*headwinds*): $N_{negative} = 1$

1. **Calculate normalized sentiment polarity**:
   $$\text{Score} = \frac{N_{positive} - N_{negative}}{N_{positive} + N_{negative}} = \frac{3 - 1}{3 + 1} = \frac{2}{4} = +0.50$$

2. **Address context and edge cases**:
   - While the score is strongly positive ($+0.50$), simple dictionary word counts are blind to **negation**. A sentence such as *"We see no accelerating growth"* contains the positive token *accelerating*, yet expresses an adverse outlook.
   - If a subsequent brief announcement contains zero sentiment tokens ($N_{pos} = 0, N_{neg} = 0$), calculating $(0 - 0)/(0 + 0)$ causes a zero-division error. The pipeline must catch this condition, output $0.0$, and record `missing_sentiment = True`.

## Research discipline

To ensure robust deployment of alternative data features:
1. **Never fit NLP vocabularies or TF-IDF weights on future text**: Estimating Inverse Document Frequencies across the entire multi-year corpus leaks future language evolution and crisis vocabulary into early historical periods.
2. **Normalize by total vendor volume**: To neutralize phantom vendor coverage expansions, normalize merchant transactions by the total panel volume recorded on that date.
3. **Archive raw unstructured source files**: Never store only the derived numerical score. Maintain compressed archives of raw text and vendor snapshots with cryptographic SHA-256 hashes to enable full compliance audits.
""",
        r"Score=(N_{positive}-N_{negative})/(N_{positive}+N_{negative})",
        'positive = 3\nnegative = 1\nscore = (positive - negative) / (positive + negative)\nprint("Toy text score:", score)',
        "A document has two positive and six negative dictionary matches. Compute the score and explain how you would handle a document with no matches. Name one coverage-change risk.",
        "Score is (2 - 6) / (2 + 6) = -4 / 8 = -0.50. With zero matches, the denominator is zero; assign a documented neutral value (0.0) with a missing-data indicator flag. A coverage-change risk is vendor panel expansion, where adding contributors creates an artificial surge in measured volume without any true economic change.",
        [
            q(
                "Why can general-purpose English dictionaries produce severely misleading sentiment scores when applied to financial corporate filings?",
                [
                    "Because common financial terms like 'cost', 'liability', and 'depreciation' are mistakenly categorized as negative distress words",
                    "Because financial filings are written in code rather than words",
                    "Because financial dictionaries require supercomputers to count words",
                ],
                0,
                "General lexicons misclassify everyday corporate accounting terminology as negative sentiment, requiring domain-specific financial dictionaries like Loughran-McDonald.",
            ),
            q(
                "What risk arises when an alternative data vendor expands its contributor network during a multi-year historical sample?",
                [
                    "Measured activity can artificially spike simply from greater vendor coverage rather than real economic customer growth",
                    "The stock price immediately becomes predictable with 100% certainty",
                    "All historical timestamps are automatically corrupted",
                ],
                0,
                "Panel expansions create artificial upward trends in raw counts that mimic organic revenue growth unless properly normalized.",
            ),
            q(
                "A financial document contains 5 positive dictionary words and 3 negative words. What is its normalized sentiment score?",
                ["0.625", "0.250", "2.000"],
                1,
                "Score = (5 − 3) / (5 + 3) = 2 / 8 = 0.250.",
            ),
        ],
    )

    # =========================================================================
    # CHAPTERS 12 - 14 & CHECKPOINTS
    # =========================================================================

# -------------------------------------------------------------------------
    # CHAPTER 12: MULTIFACTOR RETURN MODELS AND ATTRIBUTION
    # -------------------------------------------------------------------------

    add(
        "2.23",
        12,
        "Multifactor return models and attribution",
        "Separate factor exposure from residual return and distinguish explanatory from predictive factor specifications.",
        r"""
## The analytical question

Modern portfolio theory recognizes that an asset's risk and return profile cannot be encapsulated by broad market beta alone. Institutional asset managers employ **multifactor return models** to decompose asset returns into systematic risk factor exposures and security-specific idiosyncratic components.

The general linear multifactor specification for asset excess returns ($R_i - R_f$) is:

$$R_{it} - R_{ft} = \alpha_i + \sum_{k=1}^K \beta_{ik} F_{kt} + \epsilon_{it}$$

where:
- $\alpha_i$ is the intercept, representing the expected return unexplained by the $K$ risk factors. In an asset pricing model, if factors represent all priced systematic risks, equilibrium requires $E[\alpha_i] = 0$.
- $F_{kt}$ is the realized return or shock of factor $k$ during period $t$.
- $\beta_{ik} = \frac{Cov(R_i, F_k)}{Var(F_k)}$ is the asset's factor sensitivity (or factor loading) to factor $k$.
- $\epsilon_{it}$ is the idiosyncratic residual disturbance, assumed to have mean zero ($E[\epsilon_{it}] = 0$) and to be uncorrelated across assets ($Cov(\epsilon_{it}, \epsilon_{jt}) = 0$) and uncorrelated with factor movements ($Cov(F_{kt}, \epsilon_{it}) = 0$).

Institutional factor models fall into three major structural taxonomies:
1. **Macroeconomic Factor Models**: Regress returns on observable surprises in macroeconomic variables (such as unanticipated changes in inflation, industrial production growth, default credit spreads, and yield curve slope). Exposures ($\beta_{ik}$) are estimated via time-series regression.
2. **Fundamental Factor Models**: Pre-specify standardized firm attributes (such as earnings yield, book-to-market ratio, market capitalization, debt-to-equity, and price momentum) as known factor exposures ($\beta_{ik}$), and then estimate factor returns ($F_{kt}$) at each time period via cross-sectional regression across all assets (e.g., Fama-French, Carhart, and MSCI Barra models).
3. **Statistical Factor Models**: Apply unsupervised Principal Component Analysis (PCA) or Maximum Likelihood Factor Analysis to historical return covariance matrices, extracting mathematical eigenvectors that explain maximum variance without requiring prior economic labeling.

**Performance Attribution**: Ex-post factor attribution decomposes a portfolio's realized active return into distinct factor contributions:

$$R_{pt} - R_{ft} = \alpha_p + \sum_{k=1}^K \beta_{pk} F_{kt} + \epsilon_{pt}$$

$$\text{Contribution of Factor } k = \beta_{pk} F_{kt}$$

Crucially, attribution using realized factor returns is an **explanatory, conditional accounting decomposition**, not a predictive forecast! Moreover, if a quantitative model omits a critical systematic factor (e.g., liquidity risk or credit carry), the returns earned as compensation for taking that systematic risk will be falsely attributed to manager skill ($\alpha_p$).

## A worked example

A quantitative equity market-neutral strategy is evaluated over a monthly period using a two-factor model consisting of broad market excess return ($F_1$) and a value factor spread ($F_2$):
- Estimated manager alpha: $\alpha = +0.10$ percentage points
- Market factor sensitivity: $\beta_1 = 1.20$
- Value factor sensitivity: $\beta_2 = 0.50$

During the evaluation month, the realized market excess return is $F_1 = +2.0$ percentage points, and the value factor return is $F_2 = -1.0$ percentage point. The actual realized excess return of the fund is $R_{actual} = +2.40$ percentage points.

1. **Calculate the fitted systematic return**:
   $$\hat{R} = \alpha + \beta_1 F_1 + \beta_2 F_2$$
   $$\hat{R} = 0.10 + (1.20 \times 2.0) + (0.50 \times -1.0)$$
   $$\hat{R} = 0.10 + 2.40 - 0.50 = 2.00 \text{ percentage points}$$

2. **Calculate the idiosyncratic residual**:
   $$\epsilon = R_{actual} - \hat{R} = 2.40 - 2.00 = +0.40 \text{ percentage points}$$

3. **Reconcile the performance attribution**:
   - Alpha intercept contribution: $+0.10$ points
   - Market factor contribution: $+2.40$ points
   - Value factor drag: $-0.50$ points
   - Idiosyncratic stock-selection residual: $+0.40$ points
   - Total realized excess return: $0.10 + 2.40 - 0.50 + 0.40 = +2.40$ points.

While the manager delivered a positive residual ($+0.40$ points), a single monthly positive residual does not prove persistent investment skill; it may reflect unmodeled industry noise or random luck.

## Research discipline

When building factor models and evaluating investment performance:
1. **Verify point-in-time factor construction**: When constructing fundamental factors (e.g., Book-to-Market), ensure that accounting book value was publicly available prior to the return period. Using restated or forward-looking balance sheets fabricates synthetic alpha.
2. **Audit factor correlation matrices**: If two factors (e.g., Size and Quality) exhibit high correlation, collinearity will make factor return estimation erratic and unstable.
3. **Beware benchmark mismatch**: Attributing a small-cap value portfolio against a large-cap growth benchmark produces massive artificial active factor bets that swamp security selection analysis.
""",
        r"r-r_f=\alpha+\sum_k\beta_k f_k+\epsilon",
        'fitted = .1 + 1.2 * 2 + .5 * -1\nactual = 2.4\nprint("Fitted excess return (points):", fitted)\nprint("Residual (points):", actual - fitted)',
        "Use alpha 0.2, market exposure 0.8, size exposure −0.3, market return 3, and size return 2, all returns in percentage points. Attribute an actual excess return of 2.5.",
        "Market contributes 0.8*3 = 2.4 points. Size contributes -0.3*2 = -0.6 points. Alpha contributes 0.2 points. Fitted return is 0.2 + 2.4 - 0.6 = 2.0 points. The idiosyncratic residual is 2.5 - 2.0 = 0.5 points. These are model-dependent components, not conclusive proof of manager skill.",
        [
            q(
                "When a relevant systematic risk factor (such as liquidity risk) is omitted from a performance attribution model, how does it affect the results?",
                [
                    "Compensation earned for taking the omitted systematic risk will falsely appear as manager alpha or unexplained residual",
                    "The model's R-squared automatically reaches 1.0",
                    "The portfolio's risk-free rate is doubled",
                ],
                0,
                "Model omissions leave systematic risk compensation uncaptured, inflating estimated alpha or residual noise.",
            ),
            q(
                "Why is performance attribution using realized factor returns fundamentally different from a predictive forecasting model?",
                [
                    "Because historical attribution evaluates past performance conditional on already observed factor outcomes, whereas forecasting requires estimating unknown future factor returns",
                    "Because attribution only works on bond portfolios",
                    "Because attribution does not use mathematical formulas",
                ],
                0,
                "Attribution is an ex-post accounting decomposition of historical events; forecasting is an ex-ante decision tool under genuine uncertainty.",
            ),
            q(
                "A factor model has alpha = 0.0, factor exposure β = 1.5, realized factor return = 2.0 percentage points, and actual portfolio excess return = 4.0 percentage points. What is the idiosyncratic residual return?",
                ["1.0 percentage point", "2.0 percentage points", "3.0 percentage points"],
                0,
                "Fitted return = 0.0 + (1.5 × 2.0) = 3.0 points. Residual = Actual − Fitted = 4.0 − 3.0 = 1.0 percentage point.",
            ),
        ],
    )

    add(
        "2.24",
        12,
        "Factor risk and active portfolio exposures",
        "Combine factor and residual variance and distinguish total risk from risk relative to a benchmark.",
        r"""
## The analytical question

A quantitative portfolio manager must manage two distinct dimensions of risk:
1. **Total Risk ($\sigma_p$)**: The standard deviation of the portfolio's absolute return ($R_p$), governing drawdown risk, solvency, and leverage constraints.
2. **Active Risk / Tracking Error ($\sigma_A$)**: The standard deviation of active returns relative to a specified benchmark ($R_p - R_B$), governing benchmark-relative performance and investor mandate compliance.

Under a linear multifactor model, a portfolio's factor exposure is simply the capital-weighted average of its constituent asset exposures:

$$\boldsymbol{\beta}_p = \sum_{i=1}^N w_i \boldsymbol{\beta}_i$$

Holding hundreds of stocks does **not** eliminate shared systematic factor exposures! Even in a portfolio of 500 equities, if the average stock has a market beta of $1.20$, the portfolio has an unavoidable market beta of $1.20$.

The **total variance** of a portfolio decomposes into systematic factor variance and idiosyncratic residual variance:

$$\sigma_p^2 = \boldsymbol{\beta}_p^T \boldsymbol{\Sigma}_F \boldsymbol{\beta}_p + \sigma^2(\epsilon_p)$$

where:
- $\boldsymbol{\Sigma}_F$ is the $K \times K$ covariance matrix of the common factor returns.
- $\sigma^2(\epsilon_p) = \mathbf{w}^T \mathbf{D} \mathbf{w} = \sum_{i=1}^N w_i^2 \sigma^2(\epsilon_i)$ is the portfolio's specific (idiosyncratic) variance, assuming asset residuals are mutually uncorrelated (where $\mathbf{D}$ is diagonal).

In the single-factor case where the factor is uncorrelated with the residual disturbance, this simplifies to:

$$\sigma_p^2 = \beta_p^2 \sigma_F^2 + \sigma_\epsilon^2 \implies \sigma_p = \sqrt{\beta_p^2 \sigma_F^2 + \sigma_\epsilon^2}$$

**Crucial Mathematical Warning**: Variances add; standard deviations do **not** add linearly! That is, $\sigma_p \neq \beta_p \sigma_F + \sigma_\epsilon$.

**Active Risk and Tracking Error**:
Active return is $R_{At} = R_{pt} - R_{Bt}$. Active risk, or **Tracking Error (TE)**, is the sample standard deviation of active return:

$$\text{TE} = s(R_p - R_B) = \sqrt{\frac{1}{T-1}\sum_{t=1}^T \left(R_{At} - \bar{R}_A\right)^2}$$

Active factor exposure represents the difference between portfolio and benchmark factor loadings: $\Delta \beta = \beta_p - \beta_B$.

The **Information Ratio (IR)** measures active excess return per unit of active risk:

$$\text{IR} = \frac{\bar{R}_p - \bar{R}_B}{\text{TE}} = \frac{\bar{R}_A}{\sigma_A}$$

Contrast this with the **Sharpe Ratio (SR)**:

$$\text{SR} = \frac{E[R_p - R_f]}{\sigma_p}$$

A portfolio hugging an equity index with $30\%$ annual volatility can achieve a tiny $1\%$ tracking error ($\text{TE} = 1\%$) while carrying massive absolute volatility ($\sigma_p \approx 30\%$).

## A worked example

An institutional asset manager constructs a quantitative long-only equity portfolio with:
- Factor loading to the market factor: $\beta = 1.20$
- Annualized market factor volatility: $\sigma_F = 15.0\%$ ($0.15$)
- Uncorrelated residual idiosyncratic volatility: $\sigma_\epsilon = 8.0\%$ ($0.08$)

1. **Calculate total portfolio volatility**:
   - Factor systematic variance: $\beta^2 \sigma_F^2 = 1.20^2 \times 0.15^2 = 1.44 \times 0.0225 = 0.0324$
   - Specific residual variance: $\sigma_\epsilon^2 = 0.08^2 = 0.0064$
   - Total portfolio variance:
     $$\sigma_p^2 = 0.0324 + 0.0064 = 0.0388$$
   - Total portfolio volatility:
     $$\sigma_p = \sqrt{0.0388} \approx 0.196977 \implies 19.70\% \text{ annualized}$$
   Notice that simply adding standard deviations ($1.20 \times 15\% + 8\% = 18\% + 8\% = 26\%$) severely overstates risk because factor movements and idiosyncratic noise are orthogonal.

2. **Portfolio beta combination**:
   Consider a portfolio allocating $60\%$ to Asset 1 ($\beta_1 = 1.50$) and $40\%$ to Asset 2 ($\beta_2 = 0.50$):
   $$\beta_p = (0.60 \times 1.50) + (0.40 \times 0.50) = 0.90 + 0.20 = 1.10$$
   If the benchmark index has $\beta_B = 1.00$, the portfolio carries an active beta of $\Delta \beta = 1.10 - 1.00 = +0.10$.

## Research discipline

When constructing risk budgets:
1. **Never sum standalone standard deviations**: Always compute portfolio risk through the full covariance matrix: $\sigma_p = \sqrt{\mathbf{w}^T \boldsymbol{\Sigma} \mathbf{w}}$.
2. **Distinguish Sharpe Ratio from Information Ratio**: The Sharpe Ratio evaluates total risk efficiency relative to cash; the Information Ratio evaluates active efficiency relative to a benchmark. Never use them interchangeably.
3. **Monitor residual concentration**: Even in a portfolio of 100 securities, if $40\%$ of capital is concentrated in three names, idiosyncratic risk will dominate factor risk, driving tracking error blowups.
""",
        r"\sigma_p^2=\beta^2\sigma_f^2+\sigma_\epsilon^2",
        'from math import sqrt\nprint("Total volatility:", sqrt(1.2 ** 2 * .15 ** 2 + .08 ** 2))\nprint("Portfolio beta:", .6 * 1.5 + .4 * .5)',
        "A portfolio has beta 0.8, factor volatility 20%, and uncorrelated residual volatility 12%. Compute total volatility and explain why low tracking error does not imply low total volatility.",
        "Total variance is 0.8^2 * 0.20^2 + 0.12^2 = 0.64 * 0.04 + 0.0144 = 0.0256 + 0.0144 = 0.0400. Total volatility is √0.0400 = 0.20 (20.0%). Tracking error measures deviations from a benchmark; a portfolio tracking a volatile benchmark closely can have a tiny tracking error while experiencing severe total volatility.",
        [
            q(
                "A portfolio holds 25% in Asset A (beta = 2.0) and 75% in Asset B (beta = 1.0). What is the portfolio's factor beta?",
                ["1.25", "1.50", "3.00"],
                0,
                "Portfolio beta = (0.25 × 2.0) + (0.75 × 1.0) = 0.50 + 0.75 = 1.25.",
            ),
            q(
                "Tracking error is mathematically defined as:",
                [
                    "The standard deviation of portfolio active return (portfolio return minus benchmark return)",
                    "The standard deviation of the benchmark index alone",
                    "The sum of all positive trading returns",
                ],
                0,
                "Tracking error measures the volatility of active return differences between a portfolio and its benchmark.",
            ),
            q(
                "A portfolio has beta = 1.0 to a factor with 12% volatility, and an uncorrelated idiosyncratic residual volatility of 9%. What is its total volatility?",
                ["21%", "3%", "15%"],
                2,
                "Total variance = (1.0^2 × 0.12^2) + 0.09^2 = 0.0144 + 0.0081 = 0.0225. Total volatility = √0.0225 = 0.15 (15%). Add variances, not standard deviations.",
            ),
        ],
    )

    # -------------------------------------------------------------------------
    # CHAPTER 13: VALUE AT RISK, EXPECTED SHORTFALL, AND STRESS TESTING
    # -------------------------------------------------------------------------

    add(
        "2.25",
        13,
        "Value at risk and expected shortfall",
        "Calculate historical loss quantiles and tail averages with an explicit convention and horizon.",
        r"""
## The analytical question

Quantitative risk management requires measuring potential downside portfolio losses over a specified holding period. The foundational industry standard is **Value at Risk (VaR)**.

For a specified time horizon $T$ and confidence level $1 - \alpha$ (e.g., $95\%$ or $99\%$), Value at Risk represents the threshold dollar loss or percentage return loss $L$ such that the probability of experiencing a loss greater than or equal to $L$ is at most $\alpha$:

$$P(L \ge \text{VaR}_{1-\alpha}) \le \alpha \iff \text{VaR}_{1-\alpha} = Q_{1-\alpha}(L)$$

where $Q_{1-\alpha}(L)$ is the $(1-\alpha)$-quantile of the loss distribution.

**Crucial Distinction**: VaR is **not** the maximum possible loss! It merely establishes a loss threshold that is expected to be exceeded with probability $\alpha$ (e.g., on $1$ out of every $20$ trading days for a $95\%$ VaR, or $1$ out of every $100$ days for a $99\%$ VaR). It provides zero information regarding how severe the loss will be once the threshold is breached.

Three primary methodologies are used to estimate VaR:
1. **Parametric (Variance-Covariance) VaR**: Assumes asset returns follow a multivariate normal distribution:
   $$\text{VaR}_{1-\alpha} = -(\mu_p - z_\alpha \sigma_p) \times V_0$$
   where $z_\alpha$ is the standard normal critical value ($1.645$ for $95\%$, $2.326$ for $99\%$). While computationally instantaneous, parametric VaR severely understates risk because real financial returns exhibit fat tails (leptokurtosis) and negative skewness.
2. **Historical Simulation VaR**: Re-prices the current portfolio against the actual historical sequence of market price shocks over a lookback window (e.g., past 500 or 1,000 days), ordering the resulting scenario losses from worst to best. It naturally accommodates empirical non-normality and non-linear options, but assumes the historical sample represents all possible future risks.
3. **Monte Carlo Simulation VaR**: Calibrates a stochastic statistical model (incorporating copulas, GARCH volatility, and jump diffusions) to generate thousands of hypothetical market paths.

**The Failure of Subadditivity and Expected Shortfall**:
Artzner et al. (1999) established that a **coherent risk measure** must satisfy four mathematical axioms: Monotonicity, Translation Invariance, Positive Homogeneity, and **Subadditivity**:

$$\rho(A + B) \le \rho(A) + \rho(B)$$

Subadditivity states that combining portfolios must never create more risk than the sum of their individual risks (the diversification principle). **VaR is notoriously NOT subadditive** for non-normal or non-linear distributions: merging two independent portfolios can produce a joint VaR that exceeds their combined VaRs!

To resolve this defect, the Basel Committee and institutional quants rely on **Expected Shortfall (ES)** (also called Conditional VaR / CVaR):

$$\text{ES}_{1-\alpha} = E\left[L \;\big|\; L \ge \text{VaR}_{1-\alpha}\right] = \frac{1}{\alpha}\int_{1-\alpha}^1 Q_u(L)\,du$$

Expected Shortfall measures the **conditional average loss in the worst $(1 - \alpha)$ tail**. ES is mathematically coherent, satisfies subadditivity, and directly reflects tail thickness and catastrophic severity.

## A worked example

A risk committee evaluates a portfolio over a historical sample of $n = 10$ equally likely daily loss scenarios (expressed in thousands of dollars):
$$\text{Losses} = \{-3, -2, -1, 0, 1, 2, 3, 4, 7, 12\}$$
(Under loss sign convention, negative values denote gains, while positive values denote losses).

1. **Calculate Nearest-Rank 80% VaR**:
   - Order the $n=10$ observations in ascending order:
     $$L_{(1)}=-3,\; L_{(2)}=-2,\; L_{(3)}=-1,\; L_{(4)}=0,\; L_{(5)}=1,\; L_{(6)}=2,\; L_{(7)}=3,\; L_{(8)}=4,\; L_{(9)}=7,\; L_{(10)}=12$$
   - Under the standard nearest-rank discrete quantile convention, the $80\%$ rank index is $k = \lceil 0.80 \times 10 \rceil = 8$.
   - The 8th ordered observation is $L_{(8)} = 4$.
   - Therefore, the nearest-rank $80\%$ VaR is **$\$4{,}000$**. Exactly $80\%$ of historical days experienced losses of $\$4{,}000$ or less (or gains).

2. **Calculate Worst-20% Expected Shortfall**:
   - The worst $20\%$ tail comprises the largest $10 \times (1 - 0.80) = 2$ loss observations:
     $$L_{(9)} = 7 \quad \text{and} \quad L_{(10)} = 12$$
   - The Expected Shortfall is the arithmetic average of these tail losses:
     $$\text{ES}_{80\%} = \frac{7 + 12}{2} = \frac{19}{2} = 9.5 \implies \mathbf{\$9{,}500}$$
   Notice that while $80\%$ VaR is $\$4{,}000$, Expected Shortfall is $\$9{,}500$—more than double the VaR threshold! Relying solely on VaR would conceal the severity of the tail crash.

## Research discipline

When reporting risk metrics to risk committees or regulators:
1. **Always specify the three defining parameters**: Never quote a VaR number without explicitly stating: (1) holding period / horizon (e.g., 1-day vs 10-day), (2) confidence level (e.g., 95% vs 99%), and (3) methodology (parametric, historical, or Monte Carlo).
2. **Complement VaR with Expected Shortfall**: Because VaR ignores loss severity beyond the threshold, always report Expected Shortfall alongside VaR.
3. **Perform statistical backtesting (Kupiec Test)**: Count how many times actual trading losses exceed estimated VaR. If a 95% VaR model produces 20 breaches over 100 days (20% violation rate instead of 5%), the model is misspecified and must be recalibrated immediately.
""",
        r"VaR_\alpha=Q_\alpha(L);\quad ES_\alpha=\text{mean loss in worst }1-\alpha",
        'losses = [-3, -2, -1, 0, 1, 2, 3, 4, 7, 12]\n# These case observations are already sorted in ascending order.\nordered = losses\nprint("Nearest-rank 80% VaR:", ordered[7])\nprint("Worst-20% expected shortfall:", sum(ordered[-2:]) / 2)',
        "Ten equally likely sorted losses are −2, −1, 0, 1, 2, 3, 4, 5, 8, 10. Use nearest-rank 80% VaR and the worst two observations for expected shortfall. Explain the sign of a negative loss.",
        "Nearest-rank 80% VaR is the 8th observation: 5. Expected shortfall is the average of the worst two observations: (8 + 10) / 2 = 9. Under standard loss accounting, a negative loss represents a cash gain. Neither metric defines a maximum possible future loss.",
        [
            q(
                "How is a 95% one-day Value at Risk (VaR) correctly interpreted?",
                [
                    "As the absolute maximum dollar loss that the portfolio could ever suffer under any market conditions",
                    "As a threshold loss quantile that is expected to be exceeded on approximately 5% of trading days under the modeled conditions",
                    "As the expected average daily investment profit",
                ],
                1,
                "VaR is a quantile threshold, not a maximum ceiling; actual realized losses can and do exceed VaR during tail events.",
            ),
            q(
                "Why do institutional risk managers and regulators favor Expected Shortfall (CVaR) over Value at Risk (VaR)?",
                [
                    "Expected Shortfall satisfies the mathematical axiom of subadditivity and quantifies average loss severity in the tail beyond the VaR cutoff",
                    "Expected Shortfall guarantees that losses will never occur",
                    "Expected Shortfall eliminates the need for historical market data",
                ],
                0,
                "Expected Shortfall is a coherent risk measure that reflects tail risk magnitude and respects the diversification principle.",
            ),
            q(
                "For ten equally likely loss scenarios, the two largest losses are 6 and 14. What is the worst-20% Expected Shortfall?",
                ["6", "14", "10"],
                2,
                "The worst-20% tail contains exactly 2 observations (2 / 10 = 20%). ES = (6 + 14) / 2 = 10.",
            ),
        ],
    )

    add(
        "2.26",
        13,
        "Stress testing, liquidity, and nonlinear exposures",
        "Complement statistical risk estimates with coherent scenarios and recognize the limits of square-root scaling.",
        r"""
## The analytical question

Statistical risk measures like VaR and Expected Shortfall are backward-looking calibrations derived from historical distributions. In unprecedented market crises—such as systemic liquidity freezes, sovereign debt defaults, or geopolitical ruptures—historical distributions fail because the underlying data-generating regime breaks down.

To ensure survival under extreme market turbulence, risk managers conduct **Stress Testing** and **Scenario Analysis**.

Stress testing addresses questions that statistical models cannot answer:
1. **Historical Scenario Replay**: Re-evaluates the existing portfolio under the exact market factor shocks observed during famous historical crises (e.g., the 1987 Black Monday $-22.6\%$ crash, the 1998 LTCM default, the 2008 Lehman collapse, or the March 2020 COVID dash-for-cash).
2. **Hypothetical Scenario Analysis**: Simulates coherent forward-looking shocks (e.g., a simultaneous $+300$ bps interest rate surge, a $-35\%$ collapse in equity valuations, and an oil supply shock of $+70\%$).
3. **Reverse Stress Testing**: Instead of asking *"What loss occurs if the market drops 20%?"*, reverse stress testing asks:
   $$\textbf{What specific combination of market shocks and counterparty defaults would wipe out our capital or cause insolvency?}$$
   By working backward from catastrophic failure, reverse stress testing identifies hidden non-linear vulnerabilities, concentrated exposures, and fatal correlation shifts.

**The Fallacy of Square-Root-of-Time Scaling**:
In textbook finance, a 1-day volatility or VaR is frequently scaled to a 10-day or 1-year horizon by multiplying by the square root of time:
$$\sigma_{T\text{-day}} \approx \sigma_{1\text{-day}} \times \sqrt{T}$$
This square-root rule strictly requires return increments to be **independent, identically distributed (i.i.d.) normal random variables**. In real financial markets, this assumption fails catastrophically:
- Return volatility exhibits strong autocorrelation and clustering ($\sigma_t$ rises after shocks).
- Liquidity evaporates during crashes, preventing orderly multi-day execution.
- Portfolios containing options, credit default swaps, or dynamic stop-loss triggers possess severe non-linear gamma profiles that cannot be scaled linearly.

**Liquidity-Adjusted Risk and Fire-Sale Spirals**:
In a real liquidation, selling large positions incurs market impact and bid-ask spread expansion. The modeled net stress return must subtract liquidation frictions:

$$R_{stress} = \sum_{i=1}^n w_i R_{i,stress} - \text{liquidation friction costs}$$

When a leveraged fund faces margin calls, forced selling depresses asset prices further, widening spreads and triggering feedback loops of forced liquidations (**fire-sale spirals**).

## A worked example

A quantitative balanced fund manages $\$1{,}000{,}000$ of capital, allocated $60\%$ to equities ($w_1 = 0.60$) and $40\%$ to corporate bonds ($w_2 = 0.40$).

A severe stagflationary stress scenario applies simultaneous market shocks of $-25.0\%$ to equities ($R_{1,stress} = -0.25$) and $-8.0\%$ to corporate bonds ($R_{2,stress} = -0.08$).

1. **Calculate gross stress return**:
   $$R_{gross} = (0.60 \times -0.25) + (0.40 \times -0.08)$$
   $$R_{gross} = -0.150 - 0.032 = -0.182 \implies -18.20\%$$

2. **Incorporate market impact and liquidation costs**:
   Due to market illiquidity during the panic, unwinding positions to meet margin requirements incurs liquidation costs equal to $1.50\%$ ($0.015$) of starting fund capital.
   $$R_{net} = R_{gross} - \text{costs} = -0.182 - 0.015 = -0.197 \implies -19.70\%$$

3. **Calculate total dollar capital loss**:
   $$\text{Dollar Loss} = -(-0.197) \times \$1{,}000{,}000 = \$197{,}000$$
   A static pricing model ignoring liquidity would have projected an $\$182{,}000$ loss; factoring in execution slippage reveals an additional $\$15{,}000$ loss, potentially triggering a covenant breach.

## Research discipline

When architecting stress testing frameworks:
1. **Never rely solely on square-root-of-time scaling**: For multi-day risk horizons, simulate dynamic daily paths with rebalancing, liquidity constraints, and margin calls rather than multiplying daily VaR by $\sqrt{10}$.
2. **Re-price non-linear derivatives explicitly**: Do not use linear delta approximations for options during a $25\%$ market crash. Full repricing via Black-Scholes or local volatility surfaces is mandatory.
3. **Execute regular reverse stress tests**: Present reverse stress scenarios to executive committees annually to ensure that capital buffers can survive extreme tail dependencies.
""",
        r"R_{stress}=\sum_i w_iR_{i,stress}-\text{costs}",
        'gross = .6 * -.25 + .4 * -.08\nnet = gross - .015\nprint("Gross stress return:", gross)\nprint("Loss including liquidation:", -net * 1000000)',
        "A 70/30 portfolio experiences −20% and −5% shocks, plus liquidation costs of 2% of initial value. Calculate loss on 200,000 and name an assumption violated by forced rebalancing.",
        "Gross return is 0.70*(-0.20) + 0.30*(-0.05) = -0.14 - 0.015 = -0.155 (-15.5%). Including costs: -0.155 - 0.02 = -0.175 (-17.5%). Dollar loss on 200,000 is 0.175 * 200,000 = 35,000. Forced rebalancing dynamically alters asset weights during market declines, violating the assumption of static initial portfolio weights.",
        [
            q(
                "Why should hypothetical stress test scenarios be evaluated even when their occurrence probability cannot be statistically calculated?",
                [
                    "Because unprecedented crisis events lie outside historical probability distributions, yet capital planning must ensure institutional solvency if they occur",
                    "Because stress testing makes financial regulators happy without requiring calculations",
                    "Because historical returns are always identical to future returns",
                ],
                0,
                "Stress testing evaluates conditional survival under severe structural shocks regardless of whether a precise historical probability can be assigned.",
            ),
            q(
                "Which real-world market characteristic invalidates the square-root-of-time rule (scaling 1-day VaR by √10 to obtain 10-day VaR)?",
                [
                    "Volatility clustering, serial autocorrelation, and liquidity evaporation during market stress",
                    "Consistent portfolio accounting units",
                    "Maintaining a cash reserve",
                ],
                0,
                "Square-root scaling requires i.i.d. normal returns; time-series dependence and market impact render the approximation dangerously inadequate.",
            ),
            q(
                "A balanced 50/50 portfolio experiences asset returns of −30% and +10% before costs. What is its gross portfolio return?",
                ["−20%", "−10%", "+10%"],
                1,
                "Gross return = (0.50 × −30%) + (0.50 × +10%) = −15% + 5% = −10%.",
            ),
        ],
    )

    # -------------------------------------------------------------------------
    # CHAPTER 14: BACKTESTING, SIMULATION, AND RESEARCH CAPSTONE
    # -------------------------------------------------------------------------

    add(
        "2.27",
        14,
        "Backtesting and simulation without hindsight",
        "Construct a chronological experiment that accounts for execution timing, costs, and the full research search.",
        r"""
## The analytical question

A backtest is a historical simulation designed to evaluate whether a quantitative investment strategy would have generated positive risk-adjusted returns after all transaction costs and real-world execution frictions.

However, the vast majority of published backtests fail in live production. The primary driver is **backtest overfitting** and **hindsight bias**.

To construct a scientifically credible backtest, an institutional researcher must rigorously enforce four structural principles:

1. **Chronological Decision and Execution Architecture**:
   - If a trading signal is generated from market closing prices at date $t$ ($C_t$), the trade **cannot be executed at $C_t$**! The closing price is only known after trading has ceased.
   - The earliest feasible execution fill occurs at the opening price of the next trading session ($O_{t+1}$), or using Market-On-Close (MOC) orders placed before the cutoff. Assuming execution at $C_t$ or intra-bar extremes ($L_t$) fabricates impossible profits.

2. **Comprehensive Friction and Cost Modeling**:
   Gross simulated returns are meaningless. Portfolio terminal wealth evolves under net returns:
   $$W_T = W_0 \prod_{t=1}^T (1 + r_t - c_t)$$
   where $c_t$ accounts for:
   - Direct broker commissions and exchange clearing fees.
   - Half bid-ask spread crossing costs: $\frac{\text{Spread}}{2}$.
   - Market impact and slippage: Kyle's lambda or square-root volume participation models ($I \propto \sigma \sqrt{\frac{V}{ADV}}$).
   - Short borrowing costs and margin financing rates.

3. **Compounding Realities vs Arithmetic Means**:
   An arithmetic mean of net returns ($\frac{1}{T}\sum r_{net,t}$) does not reflect compounded terminal wealth. Due to **volatility drag**, the geometric compound growth rate is approximately:
   $$g \approx \mu_{arithmetic} - \frac{1}{2}\sigma^2$$
   A strategy alternating between $+10\%$ and $-10\%$ returns has an arithmetic average return of $0.0\%$, yet it systematically destroys capital: $1.10 \times 0.90 = 0.99 \implies -1.0\%$ net loss per round trip!

4. **Accounting for the Multiple Testing Research Sieve**:
   When an analyst explores 100 variations of an indicator, the single variation that achieved a backtest Sharpe ratio of $2.0$ is often pure data-mined noise. Researchers must report the total number of trial variations and apply the **Deflated Sharpe Ratio (DSR)** to adjust for selection bias.

## A worked example

A quantitative trading strategy records four consecutive quarterly gross returns: $+2.0\%$, $-1.0\%$, $+3.0\%$, and $0.0\%$ (as decimals: $0.02, -0.01, 0.03, 0.00$).

The institutional mandate applies a realistic implementation friction cost of $0.20$ percentage points ($0.002$) per quarter for bid-ask spread crossing and slippage.

1. **Calculate net returns per quarter**:
   - Quarter 1: $0.020 - 0.002 = +0.018$ ($+1.8\%$)
   - Quarter 2: $-0.010 - 0.002 = -0.012$ ($-1.2\%$)
   - Quarter 3: $0.030 - 0.002 = +0.028$ ($+2.8\%$)
   - Quarter 4: $0.000 - 0.002 = -0.002$ ($-0.2\%$)

2. **Compound net terminal wealth from an initial base $W_0 = 100.00$**:
   $$W_1 = 100.00 \times (1 + 0.018) = 101.800$$
   $$W_2 = 101.800 \times (1 - 0.012) = 100.5784$$
   $$W_3 = 100.5784 \times (1 + 0.028) = 103.3946$$
   $$W_4 = 103.3946 \times (1 - 0.002) \approx \mathbf{103.19}$$

3. **Calculate arithmetic metrics**:
   - Gross arithmetic mean: $\frac{0.02 - 0.01 + 0.03 + 0.00}{4} = \frac{0.04}{4} = 0.010$ ($1.0\%$).
   - Net arithmetic mean: $0.010 - 0.002 = \mathbf{0.008}$ ($0.8\%$).
   Notice that compounding over four periods yields terminal wealth of $103.19$ (a compounded gain of $3.19\%$), which differs from four times the net arithmetic mean ($4 \times 0.8\% = 3.2\%$).

## Research discipline

Before presenting backtest results to an investment committee:
1. **Never use close-to-close execution for close-derived signals**: Execute close signals at next-day open prices.
2. **Incorporate survivorship-free universes**: Include delisted and bankrupt tickers with realistic delisting returns.
3. **Subject the strategy to cost sensitivity stress testing**: Double and triple the assumed trading fees and slippage. If doubling slippage turns strategy alpha negative, the strategy is an implementation trap that cannot survive live trading.
""",
        r"W_T=W_0\prod_t(1+r_t-c_t)",
        'gross = [.02, -.01, .03, 0]\nwealth = 100\nfor value in gross:\n    wealth = wealth * (1 + value - .002)\nprint("Net terminal wealth:", round(wealth, 2))\nprint("Net arithmetic mean:", sum(gross) / len(gross) - .002)',
        "A close signal occurs on Monday and the specified execution is the next open. Identify the earliest eligible fill. Then compound two gross returns of +3% and −2% with 0.5 percentage points of cost per period from 100.",
        "The Tuesday market open is the earliest eligible execution fill. Net returns are 3.0% - 0.5% = +2.5% (1.025) and -2.0% - 0.5% = -2.5% (0.975). Net terminal wealth is 100 * 1.025 * 0.975 = 99.9375. Even though the net arithmetic mean is zero ((+2.5% + -2.5%)/2 = 0.0%), volatility drag causes compounded wealth to decline below 100.",
        [
            q(
                "When a trading signal is generated using daily closing prices at date t, what is the earliest realistic execution timestamp without hindsight bias?",
                [
                    "The opening price of the next trading session (t + 1)",
                    "The previous day's closing price (t − 1)",
                    "The lowest price of the current day known at the end of the year",
                ],
                0,
                "A signal calculated from the close cannot be executed at the close without lookahead assumptions; next-open execution preserves physical chronology.",
            ),
            q(
                "What does a profitable backtest conducted exclusively on synthetic simulated prices demonstrate?",
                [
                    "Internal model mechanics under the specific simulated assumptions, but NOT empirical proof of a profitable real-world market edge",
                    "Definitive proof that the strategy will make money in actual live markets",
                    "A guarantee of zero transaction costs",
                ],
                0,
                "Synthetic simulations test computational behavior; they do not validate predictive empirical performance in live trading environments.",
            ),
            q(
                "In a given trading period, a strategy earns a gross return of 1.0% and incurs implementation transaction costs of 0.4 percentage points. What is its net return?",
                ["0.6%", "1.4%", "0.04%"],
                0,
                "Net return = Gross − Costs = 1.0% − 0.4% = 0.6%.",
            ),
        ],
    )

    add(
        "2.28",
        14,
        "Capstone: a reproducible investment research report",
        "Combine data provenance, inference, model comparison, risk, and costs in a decision-ready research packet.",
        r"""
## The analytical question

The capstone of quantitative investment analysis is synthesizing data engineering, statistical inference, econometric modeling, risk management, and execution economics into a rigorous, reproducible investment research report.

Investment committees at institutional hedge funds and asset managers evaluate research proposals through a skeptical scientific lens. An analyst's duty is not to showcase a cherry-picked backtest curve, but to stress-test the empirical evidence, challenge underlying assumptions, and transparently quantify statistical uncertainty.

Consider an institutional research proposal: A quantitative equity market-neutral strategy is evaluated over a held-out, frozen chronological test period of $n = 12$ consecutive months. After deducting a standard baseline execution cost of $0.10$ percentage points per month, the realized monthly net active returns (in percentage points) are:
$$\mathbf{r}_{active} = \{+1.2, -0.8, +0.5, +1.0, -1.1, +0.7, +0.3, -0.4, +1.4, -0.9, +0.6, +0.2\}$$

The benchmark's active return is zero by definition. To evaluate whether this strategy delivers statistically significant active alpha, we formulate hypothesis tests and confidence intervals:
- Null Hypothesis: $H_0: \mu_{active} \le 0$ (strategy delivers zero or negative active alpha).
- Alternative Hypothesis: $H_a: \mu_{active} > 0$ (strategy delivers genuine positive alpha).

Under independent monthly assumptions with $n - 1 = 11$ degrees of freedom, the test statistic is:

$$t = \frac{\bar{r}_{active} - 0}{s / \sqrt{n}} = \frac{\bar{r}_{active}}{SE(\bar{r})}$$

The two-sided $95\%$ confidence interval for the true population mean active return is:

$$\text{CI}_{95\%} = \bar{r}_{active} \pm t_{crit, 0.025,\, 11} \times SE(\bar{r})$$

## A worked example

1. **Calculate sample summary statistics**:
   - Sum of net active returns: $1.2 - 0.8 + 0.5 + 1.0 - 1.1 + 0.7 + 0.3 - 0.4 + 1.4 - 0.9 + 0.6 + 0.2 = 2.70$
   - Sample mean active return:
     $$\bar{r}_{active} = \frac{2.70}{12} = \mathbf{0.225} \text{ percentage points per month}$$
   - Sum of squared deviations from the mean:
     $$\sum_{i=1}^{12} (r_i - 0.225)^2 \approx 7.8425$$
   - Sample variance: $s^2 = \frac{7.8425}{11} \approx 0.712955$
   - Sample standard deviation:
     $$s = \sqrt{0.712955} \approx \mathbf{0.8443663574} \text{ points}$$
   - Standard error of the mean:
     $$SE(\bar{r}) = \frac{s}{\sqrt{12}} = \frac{0.8443663574}{3.4641016} \approx 0.24374758 \text{ points}$$

2. **Compute test statistic and confidence interval**:
   - The $t$-statistic against zero is:
     $$t = \frac{0.225}{0.24374758} \approx \mathbf{0.9230861185}$$
   - Using the Student's $t$ critical value with $11$ degrees of freedom ($t_{0.025, 11} \approx 2.201$):
     $$\text{Margin of Error} = 2.201 \times 0.24374758 \approx 0.5364884$$
     $$\text{Confidence Interval} = [0.225 - 0.5365,\; 0.225 + 0.5365] = [-0.3114884057,\; 0.7614884057]$$
     Rounding to three decimal places yields a 95% interval of **−0.311 to 0.761** points.

3. **Interpret the statistical conclusion**:
   Because the $95\%$ confidence interval includes zero (spanning from **−0.311 to 0.761**), and the $t$-statistic ($0.923$) is far below the critical value ($2.201$), we **fail to reject the null hypothesis of zero alpha**. The positive point estimate of $+0.225\%$ per month is entirely consistent with sampling variability and chance!

4. **Stress test cost sensitivity**:
   Suppose live execution costs increase by an additional $0.20$ percentage points per month (due to wider spreads in market stress):
   $$\bar{r}_{stressed} = 0.225 - 0.200 = \mathbf{0.025} \text{ percentage points per month}$$
   The apparent active edge collapses to virtually zero ($+0.025\%$).

## Research discipline

An institutional-grade quantitative research packet must include:
1. **Full Research Sieve Disclosure**: If 20 parameter variants were backtested during development, report all 20 iterations. Omitting 19 failed variants and presenting only the best one is academic fraud.
2. **Never deduce total portfolio drawdown from active returns alone**: Active returns measure performance relative to a benchmark. If the benchmark drops $-40\%$ and the active return is $+1\%$, the portfolio suffered a catastrophic $-39\%$ absolute capital loss!
3. **Defensible Committee Recommendation**: Based on the wide confidence interval including zero and extreme sensitivity to execution costs, the defensible recommendation is paper trading and further research, NOT live capital deployment.
""",
        r"t=\bar r_{active}/(s_{active}/\sqrt n)",
        'from math import sqrt\nx = [1.2, -.8, .5, 1, -1.1, .7, .3, -.4, 1.4, -.9, .6, .2]\nmean = sum(x) / len(x)\nsquared = 0\nfor v in x:\n    squared = squared + (v - mean) ** 2\ns = sqrt(squared / (len(x) - 1))\nse = s / sqrt(len(x))\nprint("Mean active return (points):", mean)\nprint("Sample standard deviation:", s)\nprint("t statistic:", mean / se)\nprint("95% interval:", mean - 2.201 * se, mean + 2.201 * se)\nprint("Mean with higher costs:", mean - .20)',
        "Write the committee report in your notebook. Explain the conclusion from the supplied interval, propose a dependence-aware uncertainty check, and specify a new evaluation period for the next frozen experiment.",
        "The 95% confidence interval spans -0.311 to 0.761, containing zero, and cost sensitivity reduces the mean to 0.025. A defensible committee recommendation is further paper testing, not live deployment. Re-evaluate using Newey-West HAC standard errors to check for serial autocorrelation across months, document all 20 development variants in the audit log, and freeze a new future evaluation window before re-testing.",
        [
            q(
                "The capstone study's 95% confidence interval for mean active return spans from −0.311 to +0.761 percentage points. What is the valid statistical conclusion?",
                [
                    "Persistent positive alpha has been conclusively proven",
                    "We fail to reject the null hypothesis; the data does not provide sufficient evidence to rule out a zero or negative mean active return",
                    "The true population mean is mathematically proven to be exactly zero",
                ],
                1,
                "Because the confidence interval contains zero, the positive sample mean is statistically indistinguishable from random noise at the 5% level.",
            ),
            q(
                "Can an investment committee determine a portfolio's maximum historical drawdown from active return series alone?",
                [
                    "Yes, because active return and portfolio return are identical",
                    "No; active returns describe differences against a benchmark, so total portfolio return series and wealth paths are required",
                    "Only if the portfolio has an Information Ratio greater than 1.0",
                ],
                1,
                "Active returns isolate relative outperformance; total return series are essential to calculate actual portfolio wealth loss and drawdown.",
            ),
            q(
                "A strategy has a net mean active return of 0.30 percentage points per month. If adverse market conditions increase execution friction by 0.35 percentage points, what is the revised mean active return?",
                ["0.65 points", "0.05 points", "−0.05 points"],
                2,
                "Revised mean = 0.30 − 0.35 = −0.05 percentage points per month, reversing the apparent edge into an ongoing loss.",
            ),
        ],
    )

    # -------------------------------------------------------------------------
    # CHECKPOINTS AND FINISH
    # -------------------------------------------------------------------------

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
            "description": "A comprehensive institutional quantitative curriculum covering both foundational statistical inference (Part I: Chapters 1–7) and advanced econometrics, machine learning, factor risk modeling, and backtesting (Part II: Chapters 8–14).",
            "source": "CFA Institute · Quantitative Investment Analysis · Fourth edition",
            "level": "Foundational → advanced",
            "icon": "distribution",
            "modules": modules,
            "prerequisites": "Comfort with algebra, basic calculus intuition, and foundational investment concepts. The course is structured into two coherent halves: Part I develops classical probability, sampling distributions, hypothesis testing, and OLS regression; Part II advances into multiple regression diagnostics, time-series stationarity, machine-learning regularization, factor risk models, Value at Risk, and execution-aware backtesting.",
            "outcomes": [
                "Structure cash flows and return series with rigorous compounding, timing, and inflation conventions.",
                "Apply probability theory, Bayes' rule, sampling distributions, and robust hypothesis testing accounting for selection bias and multiple testing.",
                "Estimate, diagnose, and regularize linear and multiple regressions, addressing multicollinearity, heteroskedasticity, and autocorrelation with robust covariance estimators.",
                "Model time series using stationary autoregressive processes, evaluate out-of-sample forecasts, and update conditional volatility dynamically.",
                "Build point-in-time research pipelines free from look-ahead leakage, process text sentiment features, and prevent backtest overfitting.",
                "Decompose portfolio returns with multifactor models, calculate active risk and Information Ratios, estimate VaR and Expected Shortfall, and formulate stress tests.",
            ],
            "readingGuide": "The textbook Quantitative Investment Analysis (CFA Institute Investment Series, 4th Edition) is structurally organized into two major halves: Part I (Chapters 1–7) covers classical foundational statistics (time value of money, probability distributions, sampling, hypothesis tests, simple regression), while Part II (Chapters 8–14) covers advanced quantitative applications (multiple regression, time series, machine learning, big data engineering, multifactor models, risk measures, and backtesting). The platform unifies both parts into a single 28-module learning path across 14 parts to deliver a continuous, unbroken progression from basic principles to institutional-grade quantitative research. Each unit maps directly to the corresponding textbook chapter.",
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

