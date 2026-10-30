"""Original applied companion to Graham & Dodd; no reproduced book problems."""

from book_courses import finish, lesson, q

BOOK = (
    "https://www.mheducation.com/highered/mhp/product/security-analysis-classic-1940-edition.html"
)
STRUCTURE = "https://www.mheducation.com/highered/mhp/product/security-analysis-sixth-edition-foreword-warren-buffett.html?viewOption=student"


def build_security_analysis():
    modules = []

    def add(id, part, title, objective, content, formula, code, task, solution, questions):
        reading = f"Graham & Dodd, Security Analysis, 1940 edition · Part {part}. Read the relevant discussion in your own copy, then apply it to this original case."
        if part in ("VIII", "IX"):
            reading = "Course extension · modern valuation and synthesis. These tools and the growth heuristic are not presented as methods from the 1940 text."
        modules.append(
            lesson(
                id,
                part,
                title,
                objective,
                reading,
                content,
                formula,
                code,
                task,
                solution,
                questions,
            )
        )

    # -------------------------------------------------------------------------
    # PART I: THE ANALYST'S METHOD
    # -------------------------------------------------------------------------

    add(
        "1.1",
        "I",
        "Foundations of Graham & Dodd",
        "Distinguish a defensible investment operation from a price prediction and calculate a conservative margin of safety.",
        r"""
## The analytical question

In modern financial discourse, the word "investment" is frequently misapplied to any speculative transaction where an individual expects prices to rise. In their foundational 1940 treatise *Security Analysis*, Benjamin Graham and David Dodd established a rigorous boundary that remains the cornerstone of professional credit and equity valuation:

> *"An investment operation is one which, upon thorough analysis, promises safety of principal and an adequate return. Operations not meeting these requirements are speculative."*

Notice the three strict conditions embedded in this definition:
1. **Thorough analysis**: The decision must rest on verifiable primary facts—audited balance sheets, multi-year operating earnings records, contractual claim covenants, and liquidation asset recovery schedules—rather than market rumors, chart momentum, or unverified management forecasts.
2. **Safety of principal**: The investor's primary capital must be protected against permanent loss across adverse business cycles and liquidation scenarios, not merely during cyclical booms.
3. **Adequate return**: The expected cash yield or economic earnings yield must compensate for the time value of money and verifiable operational risks, without relying on future speculative multiple expansion from greater fools.

The central pillar of Graham and Dodd's framework is the **Margin of Safety** ($M$). A margin of safety expresses the percentage discount by which the current market quotation ($P$) sits below a sober, conservative estimate of intrinsic business value ($V$):

$$M = 1 - \frac{P}{V} = \frac{V - P}{V}$$

$$\text{Maximum Permitted Purchase Price: } P_{\max} = V_{\text{conservative}} \times (1 - M_{\text{required}})$$

Crucially, the margin of safety is not a statistical prediction that the share price will immediately rebound. Instead, it serves an engineering purpose: just as a structural engineer designs a bridge capable of carrying 30,000 pounds even if ordinary traffic weighs only 10,000 pounds, an investor insists on a substantial discount to absorb human error, unforeseen economic recessions, industry disruption, and accounting revisions.

$$V = \text{Conservative Going-Concern Value or Net Asset Value}$$
$$M_{\text{required}} \ge 30\% \quad (\text{or higher in cyclical and leveraged issuers})$$

If an analyst inflates the intrinsic value denominator ($V$) through heroic long-term growth assumptions, an apparent 50% discount can be manufactured out of thin air. A genuine margin of safety demands that $V$ be anchored to tangible assets or normalized earning power tested under adverse conditions.

## A worked example

Consider fictional industrial equipment manufacturer Alder Manufacturing. Alder's common shares currently trade on the secondary exchange at $P = \$60.00$. As an independent security analyst, you conduct an exhaustive forensic audit of the company's financial filings across an entire eight-year industrial cycle. Rather than producing a single speculative point estimate, you establish three disciplined valuation cases:

| Valuation Scenario | Underlying Operating Premise | Estimated Value ($V$) | Quoted Price ($P$) | Apparent Margin ($1 - P/V$) |
| :--- | :--- | :--- | :--- | :--- |
| **Weak / Depressed Case** | Trough cycle margins, loss of secondary customer, 12% discount rate | $\$75.00$ | $\$60.00$ | $20.0\%$ |
| **Base / Normalized Case** | Normalized 5-year average EBIT, mid-cycle reinvestment, 10% discount rate | $\$100.00$ | $\$60.00$ | $40.0\%$ |
| **Favorable / Peak Case** | High industry capacity utilization, favorable pricing power, 9% discount rate | $\$125.00$ | $\$60.00$ | $52.0\%$ |

Your investment committee enforces a strict policy rule: every prospective equity commitment must provide at least a **$30.0\%$ margin of safety** against the **weak-case conservative estimate** ($V_{\text{weak}} = \$75.00$).

Let us test the decision boundary:
1. Under the Base Case ($V = \$100.00$), the apparent discount is:
   $$M_{\text{base}} = 1 - \frac{\$60.00}{\$100.00} = 40.0\% \ge 30.0\% \quad \text{(Appears attractive)}$$
2. However, under the required Weak Case ($V = \$75.00$), the margin is:
   $$M_{\text{weak}} = 1 - \frac{\$60.00}{\$75.00} = 20.0\% < 30.0\% \quad \text{(Fails safety requirement)}$$
3. To achieve a $30.0\%$ margin against the conservative weak case, the maximum price the committee can pay is:
   $$P_{\max} = \$75.00 \times (1 - 0.30) = \$75.00 \times 0.70 = \$52.50$$

At the current market quote of $\$60.00$, the purchase is firmly rejected. The market price offers only a $20.0\%$ cushion against trough earnings. If an unrecorded environmental liability or customer bankruptcy destroys $\$25.00$ per share of value, an investor purchasing at $\$60.00$ faces permanent impairment, whereas an investor disciplined at $\$52.50$ preserves capital.

## Research discipline

To maintain Graham and Dodd's analytical integrity in professional practice, execute the following four-step protocol before submitting any recommendation:

1. **State the Exact Legal Claim**: Explicitly define whether you are evaluating senior secured debt, subordinated debentures, cumulative preferred shares, or the residual common equity interest. Each tier in the capital structure requires a different standard of protection.
2. **Separate Market Quotation from Intrinsic Value**: Maintain the market quote ($P$) in a separate, isolated column. Never adjust your valuation estimate ($V$) simply because market prices have dropped or rallied.
3. **Isolate Falsification Conditions**: Document exactly what disconfirming evidence would invalidate your thesis (e.g., loss of patent protection, recurring operating cash flow deficits, or covenant renegotiations).
4. **Enforce the Price Ceiling**: Calculate $P_{\max} = V_{\text{weak}} \times (1 - M_{\text{required}})$ and refuse to authorize capital allocation if market quotes exceed this ceiling, regardless of institutional consensus or fear of missing out.
""",
        r"M=1-P/V;\quad P_{\max}=V_{\text{conservative}}(1-M_{\text{required}})",
        'price = 60\nvalue_weak = 75\nvalue_base = 100\nprint("Weak margin of safety:", round((1 - price / value_weak) * 100, 1), "%")\nprint("Base margin of safety:", round((1 - price / value_base) * 100, 1), "%")\nprint("Conservative maximum price:", round(value_weak * 0.70, 2))',
        "A common stock trades at $54.00. Your forensic audit determines a weak-case intrinsic value of $72.00, a base-case value of $90.00, and your mandate requires a 30% margin of safety against the weak case. Calculate the maximum acceptable purchase price and determine whether the stock can be bought at $54.00.",
        "Under the weak case ($72.00), the maximum acceptable purchase price is $72.00 × (1 − 0.30) = $50.40. At $54.00, the actual margin of safety is ($72.00 − $54.00) / $72.00 = 25.0%, which fails the mandatory 30% threshold. The purchase must be rejected at $54.00. The stock becomes investable only if the quotation drops to $50.40 or lower.",
        [
            q(
                "A common stock priced at $60.00 has an estimated conservative intrinsic value of $100.00. What is its margin of safety?",
                ["20%", "40%", "60%"],
                1,
                "The margin of safety is ($100 − $60) / $100 = 40%. Intrinsic value, not the market price, serves as the denominator.",
            ),
            q(
                "Which analytical practice most severely undermines the integrity of a margin of safety?",
                [
                    "Auditing five years of audited balance sheets",
                    "Relying on an aggressive, optimistic cash-flow projection to manufacture a large discount",
                    "Stress-testing operating earnings against a recessionary downturn",
                ],
                1,
                "An inflated intrinsic value denominator manufactures an artificial discount, providing an illusion of safety without downside protection.",
            ),
            q(
                "An analyst requires a 25% margin of safety against a weak-case value of $80.00. The market quotation is $64.00. What is the investment decision?",
                [
                    "Purchase because the quote is below $80.00",
                    "Reject because the maximum allowable purchase price is $60.00",
                    "Purchase because the base-case value is likely $100.00",
                ],
                1,
                "The maximum permitted price is $80.00 × (1 − 0.25) = $60.00. At $64.00, the margin is only 20%, which fails the 25% requirement.",
            ),
        ],
    )

    add(
        "1.6",
        "I",
        "Build an evidence file",
        "Separate reported facts, analytical adjustments, and assumptions in a dated research record.",
        r"""
## The analytical question

A professional security analysis is not an essay of personal opinions; it is an evidentiary legal and financial brief that another analyst can independently audit and replicate. Every claim regarding revenues, margins, debt obligations, and asset recoveries must tie directly to primary sources—regulatory disclosure filings (such as SEC Form 10-K, 10-Q, or 8-K), indentures, credit agreements, and court dockets.

To prevent confirmation bias and intellectual drift, Graham and Dodd insisted on maintaining a rigid tripartite structure in every research working paper:

$$\begin{array}{|c|c|c|}
\hline
\textbf{Column 1: Reported Facts} & \textbf{Column 2: Analytical Adjustments} & \textbf{Column 3: Working Assumptions} \\
\hline
\text{Verifiable primary disclosures} & \text{Auditable mathematical reconciliations} & \text{Explicit judgments with sensitivity bounds} \\
\text{(Dates, exact units, accession numbers)} & \text{(Nonrecurring items, lease capitalizations)} & \text{(Discount rates, terminal growth, recovery \%)} \\
\hline
\end{array}$$

1. **Reported Facts**: The exact numbers as stated by the issuer, accompanied by document date, filing date, currency, scale (thousands vs millions), and scope of consolidation. Never overwrite a reported number.
2. **Analytical Adjustments**: Transparent reconciliations that bridge reported numbers to economic reality. If management reports an extraordinary asset sale gain, this column subtracts it with an explicit note.
3. **Working Assumptions**: The analyst's judgments regarding the future. Each assumption must state its rationale and an adverse sensitivity boundary.

A critical dimension of evidence discipline is **point-in-time timestamping**. When reconstructing historical corporate performance, you must distinguish between the **period-end date** (e.g., December 31) and the **public availability date** (e.g., March 15 when the 10-K was filed on EDGAR). Using financial numbers before their public release introduces hindsight bias (look-ahead contamination), rendering historical backtests and valuation conclusions invalid.

One classic diagnostic for evaluating corporate reporting quality is **receivables intensity** relative to sales:

$$\text{Receivables Intensity} = \frac{\text{Accounts Receivable}}{\text{Annual Net Sales}}$$

$$\Delta \text{Intensity} = \frac{\text{AR}_t}{\text{Sales}_t} - \frac{\text{AR}_{t-1}}{\text{Sales}_{t-1}}$$

When accounts receivable surge at a rate disproportionate to top-line revenue, it signals potential channel stuffing, aggressive revenue recognition, or customer payment distress requiring immediate investigation.

## A worked example

Let us construct an evidence audit for Alder Manufacturing's working capital accounts across two consecutive fiscal years:

| Metric | Prior Year ($t-1$) Reported | Current Year ($t$) Reported | Percentage Change |
| :--- | :--- | :--- | :--- |
| **Annual Net Sales** | $\$200.0\text{ million}$ | $\$240.0\text{ million}$ | $+20.0\%$ |
| **Accounts Receivable** | $\$30.0\text{ million}$ | $\$48.0\text{ million}$ | $+60.0\%$ |
| **Receivables Intensity** | $15.0\%$ | $20.0\%$ | $+5.0\text{ percentage points}$ |

Notice the clear divergence: sales grew by $20.0\%$, but receivables surged by $60.0\%$. Receivables intensity expanded from $15.0\%$ of sales to $20.0\%$.

As a security analyst building your evidence file, you do not immediately conclude fraud, but you document the anomaly across the three columns:
- **Reported**: Sales $\$240.0\text{M}$, AR $\$48.0\text{M}$ (SEC Form 10-K filed March 15, FY ended December 31).
- **Adjusted**: Incremental receivables beyond proportional sales growth equal $\$48.0\text{M} - (\$240.0\text{M} \times 0.15) = \$12.0\text{ million}$. Working capital consumed $\$12.0\text{M}$ of operating cash.
- **Assumed**: Base assumption assumes normal collection cycle with extended payment terms granted to large distributors. Stressed downside assumption applies a $25.0\%$ collection haircut to the incremental $\$12.0\text{M}$, reducing prospective liquid net assets by $\$3.0\text{ million}$.

Furthermore, verify the point-in-time timeline:
- Fiscal year ended: December 31, 2025.
- Annual report filed on EDGAR: March 15, 2026.
- A research committee decision dated January 31, 2026, **cannot** cite the $\$48.0\text{M}$ receivables figure because it was not publicly known on that date. Only third-quarter 10-Q numbers were knowable.

## Research discipline

To construct an institutional-grade evidence file, follow these mandatory practices:
1. **Preserve Filing Accession Numbers**: Every audited table must reference the specific SEC EDGAR accession number or company registry publication date.
2. **Never Average Incompatible Baselines**: If an issuer shifts accounting principles (e.g., from US GAAP to IFRS, or modifies segment reporting), construct a bridge year before comparing ratios.
3. **Track Restatements Separately**: When an issuer files an amended 10-K/A, keep the original 10-K in your historical timeline and record the amendment date as a separate information event.
4. **Demand Corroborating Disclosures**: Do not rely on press release summaries. Verify reported numbers against the audited footnotes, particularly Note 1 (Summary of Accounting Policies) and Note 4 (Segment and Customer Concentration).
""",
        r"\text{Receivables Intensity}=\frac{\text{AR}}{\text{Sales}};\quad \text{Days Sales Outstanding}=\frac{\text{AR}}{\text{Sales}}\times 365",
        'sales_prior = 200\nsales_curr = 240\nar_prior = 30\nar_curr = 48\nprint("Revenue growth (%):", round((sales_curr / sales_prior - 1) * 100, 1))\nprint("Receivables growth (%):", round((ar_curr / ar_prior - 1) * 100, 1))\nprint("Prior receivables intensity:", round(ar_prior / sales_prior, 3))\nprint("Current receivables intensity:", round(ar_curr / sales_curr, 3))\nprint("Disproportionate AR buildup ($M):", round(ar_curr - (sales_curr * (ar_prior / sales_prior)), 1))',
        "An issuer reports revenue of $300M and receivables of $90M in the current year, compared to revenue of $250M and receivables of $50M in the prior year. Management states in a press release that customer credit quality is pristine. Prepare the three-column evidence log entry and calculate the disproportionate receivables buildup.",
        "Prior intensity is $50M / $250M = 20.0%. Current intensity is $90M / $300M = 30.0% (a 10 percentage point increase). Disproportionate receivables buildup is $90M − ($300M × 0.20) = $30M. The evidence log records: Reported: $300M sales, $90M AR (with filing date). Adjusted: $30M excess working capital tie-up. Assumed: Management's qualitative assertion is noted but cannot be accepted without an audited receivables aging schedule and subsequent cash collection verification.",
        [
            q(
                "An issuer reports annual net sales of $250 million and year-end accounts receivable of $50 million. What is its receivables intensity?",
                ["5%", "20%", "50%"],
                1,
                "Receivables intensity is $50M / $250M = 20.0%.",
            ),
            q(
                "Which date legally and analytically governs the inclusion of a financial filing in a historical investment decision?",
                [
                    "The public filing availability date",
                    "The fiscal period closing date",
                    "The analyst's birthday",
                ],
                0,
                "To prevent look-ahead bias and hindsight contamination, an analysis must only use information publicly available on or before the decision date.",
            ),
            q(
                "A company files an amended 10-K/A in June restating its previously reported March earnings downward. How must an analyst document this?",
                [
                    "Overwriting March records with the June figures without a timestamp",
                    "Preserving the March information set as historical record and logging the June revision as a distinct subsequent event",
                    "Deleting the company from the coverage universe entirely",
                ],
                1,
                "Point-in-time research requires preserving the historical record of what was known in March, while logging the June restatement on its true announcement date.",
            ),
        ],
    )

    add(
        "1.7",
        "I",
        "Value ranges and the limits of precision",
        "Reconcile asset and earnings evidence without double counting or disguising uncertainty.",
        r"""
## The analytical question

One of the most dangerous tendencies in modern financial modeling is **false precision**. An analyst projects twenty line items out fifteen years into the future, discounts the cash flows at $9.347\%$, and concludes that a stock is worth exactly $\$54.82$. This creates a seductive illusion of scientific accuracy while obscuring the reality that a tiny $0.5\%$ shift in discount rate or operating margin alters the outcome by $30\%$.

Graham and Dodd repeatedly cautioned against mistaking mathematical elaboration for analytical certainty:

$$\text{Intrinsic value is not an exact point; it is a reasoned range.}$$

To establish a defensible valuation range, the analyst must first select a clear **valuation premise**:
1. **Going-Concern Operating Premise**: Assumes the business will continue its commercial operations indefinitely. Intrinsic value is derived from the capitalized earning power or discounted free cash flows generated by its operating assets.
2. **Orderly Liquidation Premise**: Assumes the business ceases operations and liquidates its assets over a reasonable timeframe (e.g., 6 to 18 months). Value is derived from realizable cash proceeds after paying all administrative costs, severance, and satisfying all senior liabilities.
3. **Forced Wind-Down / Distress Premise**: Assumes immediate distress sale under bankruptcy court supervision with steep fire-sale haircuts.

The cardinal error in security analysis is **double counting across incompatible premises**. An analyst cannot value an operating factory as a going concern generating $\$15\text{M}$ in annual operating profit, and simultaneously add the factory's vacant land liquidation resale value to the equity estimate! The factory cannot be both operated and demolished at the same time.

The rigorous claims bridge for a going concern is:

$$V_{\text{equity}} = V_{\text{operations}} + \text{Excess Nonoperating Cash} - \text{All Senior Claims}$$

$$\text{Equity Value per Share} = \frac{V_{\text{equity}}}{N_{\text{diluted shares}}}$$

Here, "Excess Cash" is strictly cash that is not required to fund everyday working capital cycles. If the business requires $\$10\text{M}$ in minimum cash balances to operate its store branches or pay supplier payroll, that $\$10\text{M}$ is an operating asset already embedded inside $V_{\text{operations}}$ and cannot be added a second time.

## A worked example

Let us evaluate Alder Manufacturing under alternative premises and construct an honest valuation range. The company has $10.0\text{ million}$ fully diluted shares outstanding and $\$60.0\text{ million}$ in interest-bearing debt. Balance sheet cash is $\$30.0\text{ million}$, of which $\$10.0\text{ million}$ is essential operating cash, leaving $\$20.0\text{ million}$ as true excess cash.

### Premise A: Going-Concern Operating Range
Through detailed earning power capitalization, you estimate the enterprise value of operations ($V_{\text{operations}}$) across three operating states:
- **Pessimistic Case**: $V_{\text{operations}} = \$180.0\text{ million}$
- **Base Case**: $V_{\text{operations}} = \$200.0\text{ million}$
- **Optimistic Case**: $V_{\text{operations}} = \$220.0\text{ million}$

Applying the claims bridge:

$$V_{\text{equity}} = V_{\text{operations}} + \$20.0\text{M (Excess Cash)} - \$60.0\text{M (Debt)}$$

$$V_{\text{equity}} = V_{\text{operations}} - \$40.0\text{ million}$$

Dividing across $10.0\text{ million}$ diluted shares:
- **Pessimistic**: $(\$180.0\text{M} - \$40.0\text{M}) / 10.0\text{M} = \$14.00\text{ per share}$
- **Base**: $(\$200.0\text{M} - \$40.0\text{M}) / 10.0\text{M} = \$16.00\text{ per share}$
- **Optimistic**: $(\$220.0\text{M} - \$40.0\text{M}) / 10.0\text{M} = \$18.00\text{ per share}$

### Premise B: Orderly Liquidation Value
Separately, you perform an asset-by-asset recovery audit. Selling off inventories at a $50\%$ discount, collecting receivables at $80\%$, auctioning machinery, paying off all $\$100.0\text{M}$ in total liabilities, and funding $\$8.0\text{M}$ in employee severance leaves $\$15.0\text{ million}$ in net cash, or **$\$1.50\text{ per share}$**.

Notice how an undisciplined analyst might err:
- **Error 1**: Adding the $\$1.50$ liquidation value to the $\$16.00$ going-concern value to produce $\$17.50$. This is gross double counting.
- **Error 2**: Adding the full $\$30.0\text{M}$ cash balance instead of only the $\$20.0\text{M}$ excess cash. That would overstate equity value by $\$1.00$ per share.

At a current market quote of $P = \$13.00$, compare the discount across endpoints:
- Discount to Conservative Endpoint ($\$14.00$): $1 - \frac{\$13.00}{\$14.00} = 7.1\%$
- Discount to Optimistic Endpoint ($\$18.00$): $1 - \frac{\$13.00}{\$18.00} = 27.8\%$

The disciplined analyst does not declare a "bargain" based on the optimistic $27.8\%$ discount. At $\$13.00$, the margin of safety against the conservative endpoint is an inadequate $7.1\%$.

## Research discipline

To avoid the trap of spurious precision, enforce these guidelines in every valuation report:
1. **Present Values as Ranges**: Always provide a conservative lower bound, a central base case, and an upper bound, accompanied by the specific economic driver for each band.
2. **Strictly Quarantine Operating vs Nonoperating Assets**: Verify that any asset added to enterprise value does not produce cash flow already capitalized in operating earnings.
3. **Explicitly State the Governing Premise**: Never blend liquidation proceeds with operating cash flows into a single blended average unless an actual partial restructuring has been formally enacted.
4. **Identify the Asymmetry of Error**: Ask: "If my operating estimate is too high by $20\%$, what protects the investor?" If the answer is "nothing," the position lacks an adequate margin of safety.
""",
        r"V_{\text{equity}}=V_{\text{operations}}+\text{Excess Cash}-\text{Senior Claims};\quad \text{Per Share}=\frac{V_{\text{equity}}}{N}",
        'excess_cash = 20\ndebt = 60\nshares = 10\nfor enterprise in [180, 200, 220]:\n    equity = enterprise + excess_cash - debt\n    print("Enterprise:", enterprise, "-> Equity per share:", equity / shares)',
        "An industrial firm has operating value estimated between $150M and $190M. It holds $25M in balance-sheet cash, of which $10M is required for operations. Total debt is $45M, and there are 8 million shares outstanding. An analyst suggests also adding $12M from liquidating the primary manufacturing warehouse. Calculate the correct equity value range per share and critique the analyst's suggestion.",
        "Excess cash is $25M − $10M = $15M. Net claim adjustment is $15M (excess cash) − $45M (debt) = −$30M. Equity value range is ($150M − $30M) to ($190M − $30M) = $120M to $160M. Dividing by 8M shares yields $15.00 to $20.00 per share. The analyst's suggestion to add $12M from liquidating the warehouse is an invalid double count: the warehouse is an essential operating asset required to generate the $150M–$190M operating value.",
        [
            q(
                "An enterprise has operating value of $100M, total cash of $15M (of which $5M is operating cash), debt of $30M, and 5 million shares. What is the equity value per share?",
                ["$14.00", "$16.00", "$20.00"],
                1,
                "Excess cash is $15M − $5M = $10M. Equity value is $100M + $10M − $30M = $80M. Dividing by 5M shares gives $16.00 per share.",
            ),
            q(
                "Under what condition can an asset be legitimately added to an operating enterprise valuation?",
                [
                    "Whenever the asset has a positive historical carrying book value",
                    "Only when the asset is strictly nonoperating, surplus, and its earnings are not included in operating cash flow",
                    "Whenever management mentions it in an earnings call",
                ],
                1,
                "To avoid double counting, an asset can only be added if it is surplus to ongoing operations and does not contribute to the capitalized operating earnings.",
            ),
            q(
                "An analyst combines the capitalized operating earnings of a hotel chain with the proceeds from selling all hotel real estate to third parties. What fundamental error occurred?",
                [
                    "Using too low a discount rate",
                    "Double counting across mutually exclusive going-concern and liquidation premises",
                    "Failing to compute EBITDA",
                ],
                1,
                "The hotel cannot generate operating earnings if its physical real estate is sold off. Adding the two numbers combines mutually exclusive premises.",
            ),
        ],
    )

    # -------------------------------------------------------------------------
    # PART II: PROTECTING A FIXED CLAIM
    # -------------------------------------------------------------------------

    add(
        "1.2",
        "II",
        "Bond safety and earnings coverage",
        "Evaluate a fixed claim using weak-period coverage, liquidity, and the issuer's business resilience.",
        r"""
## The analytical question

The economic posture of a bondholder or fixed-income investor is fundamentally asymmetric:
- **The Upside is Strictly Capped**: At best, the creditor receives only the contractual coupon payments and the return of principal at par.
- **The Downside is Complete Ruin**: If the issuer defaults, the creditor risks suffering a severe permanent loss of capital through restructuring haircuts, prolonged bankruptcy litigation, or total liquidation.

Because the bondholder does not participate in corporate super-profits, fixed-income analysis must never be conducted on the basis of optimistic growth forecasts. It is exclusively an exercise in **downside protection, structural seniority, and stress testing**.

The primary tool for assessing fixed claim safety is **Earnings Coverage of Fixed Charges**. This measures the margin by which operating earnings can contract before the company fails to cover its mandatory debt service:

$$\text{Interest Coverage Ratio} = \frac{\text{EBIT}}{\text{Annual Interest Charges}}$$

$$\text{Fixed Charge Coverage} = \frac{\text{EBIT} + \text{Operating Lease Rentals}}{\text{Interest} + \text{Operating Lease Rentals} + \frac{\text{Preferred Dividends}}{1 - t}}$$

Notice two vital nuances:
1. **The Numerator Must Be EBIT (Not EBITDA)**: Modern leveraged buyout promoters frequently market debt safety using EBITDA coverage. Graham and Dodd vehemently rejected this shortcut. Depreciation represents the physical wear-and-tear of plant and equipment. If a manufacturing or utility company does not replace its machinery, it will soon cease to operate. Using EBITDA assumes equipment never wears out or that maintenance capital expenditures can be permanently postponed without destroying earning capacity.
2. **Stress Testing Under Trough Conditions**: An average interest coverage of $5.0\times$ across an economic boom is meaningless if coverage collapses to $0.8\times$ during a routine recession. A defensible bond must demonstrate adequate coverage in the **poorest year** of a representative business cycle.

$$\text{Weak-Period Coverage} = \frac{\text{Trough EBIT}}{\text{Total Contractual Fixed Charges}} \ge 2.0\times \text{ to } 3.0\times \quad (\text{depending on industry cyclicity})$$

Furthermore, interest coverage measures only an annual flow of earnings; it does not settle principal maturities. A company can have pristine $6.0\times$ interest coverage and still file for bankruptcy if a $\$200\text{M}$ bond matures next month, cash reserves are depleted, and debt capital markets are frozen. A complete credit evaluation demands a synchronized **Maturity Liquidity Analysis**:

$$\text{Maturity Funding Gap} = \text{Maturing Principal} - \text{Accessible Cash} - \text{Free Operating Cash Flow}$$

## A worked example

Let us evaluate the senior unsecured bonds of Alder Manufacturing. Alder has $\$60.0\text{ million}$ of $8.33\%$ senior notes outstanding, generating an annual interest obligation of $\$5.0\text{ million}$. In addition, it has $\$25.0\text{ million}$ of bank loans carrying $\$2.5\text{ million}$ in annual interest. Total contractual annual interest is $\$7.5\text{ million}$.

You examine Alder's operating earnings across an eight-year cycle:
- **Peak Boom Year EBIT**: $\$45.0\text{ million} \implies \text{Coverage} = \frac{\$45.0\text{M}}{\$7.5\text{M}} = 6.0\times$
- **Normalized Average EBIT**: $\$30.0\text{ million} \implies \text{Coverage} = \frac{\$30.0\text{M}}{\$7.5\text{M}} = 4.0\times$
- **Severe Trough Year EBIT**: $\$15.0\text{ million} \implies \text{Coverage} = \frac{\$15.0\text{M}}{\$7.5\text{M}} = 2.0\times$

In the trough year, EBIT contracts by $66.7\%$ from the peak, but earnings still cover total interest obligations by $2.0\times$. The cushion before operating losses reach interest payments is:

$$\text{Earnings Cushion} = 1 - \frac{1}{\text{Coverage}} = 1 - \frac{1}{2.0} = 50.0\%$$

Operating earnings in the trough could drop by another $50\%$ before interest is missed.

Now examine the debt maturity schedule. Next year, the $\$25.0\text{ million}$ bank term loan matures in full. Alder's balance sheet displays:
- Total Cash: $\$18.0\text{ million}$, but $\$10.0\text{ million}$ is minimum operational cash locked in foreign subsidiaries, leaving accessible cash of $\$8.0\text{ million}$.
- Projected trough free operating cash flow after interest and maintenance CapEx: $\$4.0\text{ million}$.

Calculate the maturity funding gap:

$$\text{Total Available Internal Funds} = \$8.0\text{M (Accessible Cash)} + \$4.0\text{M (Internal FCF)} = \$12.0\text{ million}$$

$$\text{Maturity Funding Gap} = \$25.0\text{M} - \$12.0\text{M} = \$13.0\text{ million}$$

Even though annual interest is covered $2.0\times$, Alder faces a **$\$13.0\text{ million}$ liquidity deficit** to pay off maturing principal! The bond cannot be approved as a high-grade investment unless the analyst verifies that Alder has an undrawn, legally binding revolving credit facility from solvent banks to bridge the gap.

## Research discipline

To conduct professional fixed-income security analysis, adhere to this protocol:
1. **Never Accept EBITDA as a Proxy for Debt Safety**: Always deduct necessary replacement depreciation and maintenance CapEx. If management defines "Adjusted EBITDA" with add-backs for stock compensation or recurring restructuring, remove those add-backs immediately.
2. **Compute Coverage on Total Debt (Not Net Debt)**: Net interest coverage artificially deducts cash balances. In distress, cash can vanish rapidly. Use gross contractual fixed charges.
3. **Audit Structural Subordination**: Verify whether the debt was issued by the operating subsidiary (holding the revenue-generating factories) or by a parent holding company. Debt at the parent is structurally junior to all liabilities of the subsidiary.
4. **Construct an Unbroken 10-Year Maturity Schedule**: Map every maturity year by year against internal free cash generation. Flag any "debt wall" that requires capital market refinancing.
""",
        r"\text{Interest Coverage}=\frac{\text{EBIT}}{\text{Interest}};\quad \text{Maturity Gap}=\text{Principal Due}-(\text{Cash}_{\text{accessible}}+\text{FCF})",
        'ebit_peak = 45\nebit_norm = 30\nebit_trough = 15\ninterest = 7.5\nprint("Peak coverage:", round(ebit_peak / interest, 2))\nprint("Normalized coverage:", round(ebit_norm / interest, 2))\nprint("Trough coverage:", round(ebit_trough / interest, 2))\nmaturing_debt = 25\naccessible_cash = 8\ninternal_fcf = 4\ngap = maturing_debt - (accessible_cash + internal_fcf)\nprint("Maturity funding gap ($M):", round(gap, 2))',
        "An issuer owes $12M in annual interest and faces a $50M bond maturity next year. Current EBIT is $60M, but in a past recession EBIT dropped to $24M. The company holds $30M in cash (of which $15M is required for operations) and expects $10M in trough operating cash flow. Evaluate interest coverage in the recession and calculate the maturity funding gap.",
        "Recession interest coverage is $24M / $12M = 2.0x (down from 5.0x currently). Accessible cash is $30M − $15M = $15M. Total available funds are $15M (cash) + $10M (FCF) = $25M. The maturity funding gap is $50M − $25M = $25M. While recession interest coverage of 2.0x meets minimum standards, the company faces a $25M refinancing gap that creates substantial credit risk.",
        [
            q(
                "An issuer reports EBIT of $90 million and annual contractual interest charges of $30 million. What is its interest coverage ratio?",
                ["0.33 times", "3.0 times", "30 times"],
                1,
                "Interest coverage is $90M / $30M = 3.0 times.",
            ),
            q(
                "Why did Graham and Dodd insist on using EBIT rather than EBITDA when evaluating fixed claim safety?",
                [
                    "Depreciation represents a real economic cost of capital asset consumption that must be reinvested to maintain earning power",
                    "EBITDA is too difficult to calculate from an income statement",
                    "Taxes are paid before interest",
                ],
                0,
                "Depreciation reflects the exhaustion of productive equipment; ignoring it assumes machinery lasts forever without capital reinvestment.",
            ),
            q(
                "An issuer has annual interest of $15 million. In a severe industry downturn, EBIT falls from $90 million to $30 million. What is the stressed interest coverage?",
                ["6.0 times", "3.0 times", "2.0 times"],
                2,
                "Stressed coverage uses the trough earnings: $30M / $15M = 2.0 times.",
            ),
        ],
    )

    add(
        "1.8",
        "II",
        "Priority, collateral, and seniority",
        "Build a simplified claim waterfall and distinguish collateral value from the issuer's total asset value.",
        r"""
## The analytical question

When an enterprise enters severe distress or insolvency, earning power ceases to protect creditors. At that moment, the investor's recovery is dictated entirely by two legal realities:
1. **Contractual Seniority and the Priority Waterfall**: Which creditor class has the prior legal right to be satisfied before junior capital receives a single dollar?
2. **Collateral Security and Encumbrance**: Does the creditor hold a perfected, first-priority mortgage or security lien on specific ring-fenced assets, or are they an unpledged general claimant?

In insolvency law and classical security analysis, asset distributions obey the **Absolute Priority Rule**: senior classes must be made $100\%$ whole (principal plus accrued interest) before any subordinate class receives any distribution:

$$\text{Senior Recovery: } R_{\text{senior}} = \min(D_{\text{senior}}, A_{\text{net}})$$

$$\text{Junior Recovery: } R_{\text{junior}} = \min\left(D_{\text{junior}}, \max(0, A_{\text{net}} - D_{\text{senior}})\right)$$

$$\text{Equity Recovery: } R_{\text{equity}} = \max\left(0, A_{\text{net}} - D_{\text{senior}} - D_{\text{junior}}\right)$$

Here, $A_{\text{net}}$ represents the **net realizable liquidation proceeds** of the asset pool after deducting administrative bankruptcy expenses, trustee fees, and asset preservation costs.

A frequent error among beginner analysts is equating **balance sheet book value** with **collateral recovery value**. A manufacturing facility carried on the balance sheet at $\$80.0\text{ million}$ (historical cost less accumulated depreciation) may realize only $\$20.0\text{ million}$ at an industrial auction if the plant is specialized, located in a declining manufacturing belt, or contaminated with environmental liabilities.

Furthermore, analysts must distinguish between **legal entity tiers**:
- **Operating Company (OpCo) Debt**: Sits directly against the operating assets and revenues.
- **Holding Company (HoldCo) Debt**: Has no direct claim on OpCo assets. It holds only the common equity shares of OpCo. Under corporate law, OpCo creditors must be satisfied $100\%$ before OpCo can upstream a dividend to HoldCo. HoldCo debt is therefore **structurally subordinated** to all OpCo liabilities, including OpCo trade payables and leases!

## A worked example

Consider a ring-fenced collateral pool belonging to an industrial borrower undergoing restructuring. The asset pool consists of specialized assembly machinery and commercial warehouses. The audited book value of these assets is $\$120.0\text{ million}$, but an independent liquidation appraisal estimates net realizable auction proceeds at $A_{\text{net}} = \$70.0\text{ million}$ under an orderly 9-month sale.

The borrower has two debt tranches secured against this specific collateral pool:
- **First-Lien Senior Secured Notes**: $D_{\text{senior}} = \$50.0\text{ million}$ principal
- **Second-Lien Junior Notes**: $D_{\text{junior}} = \$30.0\text{ million}$ principal
- Total debt claim = $\$80.0\text{ million}$

Let us calculate the recovery waterfall across two disposal scenarios:

### Scenario 1: Base Liquidation Proceeds ($A_{\text{net}} = \$70.0\text{ million}$)
1. First-Lien Senior Notes claim is $\$50.0\text{M}$. Since proceeds ($\$70.0\text{M}$) exceed the claim, Senior Notes recover in full:
   $$\text{Senior Distribution} = \$50.0\text{M} \implies \text{Recovery} = \frac{\$50.0\text{M}}{\$50.0\text{M}} = 100.0\%$$
2. Remaining proceeds available for junior claims:
   $$\text{Residual Proceeds} = \$70.0\text{M} - \$50.0\text{M} = \$20.0\text{ million}$$
3. Second-Lien Junior Notes claim is $\$30.0\text{M}$. They receive the entire remaining $\$20.0\text{M}$:
   $$\text{Junior Distribution} = \$20.0\text{M} \implies \text{Recovery} = \frac{\$20.0\text{M}}{\$30.0\text{M}} = 66.7\%$$
4. Equity receives $\$0.00$.

### Scenario 2: Stressed Fire-Sale Proceeds ($A_{\text{net}} = \$40.0\text{ million}$)
Suppose industrial demand weakens, and net proceeds drop to $\$40.0\text{ million}$:
1. First-Lien Senior Notes receive all $\$40.0\text{M}$:
   $$\text{Senior Distribution} = \$40.0\text{M} \implies \text{Recovery} = \frac{\$40.0\text{M}}{\$50.0\text{M}} = 80.0\%$$
2. Second-Lien Junior Notes receive $\$0.00$ ($\text{Recovery} = 0.0\%$).
3. Equity receives $\$0.00$.

Notice the extreme non-linearity! A $42.9\%$ drop in net proceeds (from $\$70\text{M}$ to $\$40\text{M}$) reduces the senior recovery by only $20.0$ percentage points, but completely wipes out the junior claim from $66.7\%$ to zero.

## Research discipline

When evaluating the priority and collateral protection of a corporate debt issue:
1. **Demand the Security Agreement and Perfection Documents**: Verify whether the creditor's lien is legally perfected (e.g., UCC-1 financing statements, registered real property mortgages). An unperfected lien is treated as a general unsecured claim in bankruptcy.
2. **Deduct Bankruptcy Administration Costs First**: In chapter 11 or insolvency proceedings, administrative professional fees, debtor-in-possession (DIP) financing, and preservation costs take priority over pre-petition secured debt. Always deduct $5\%$ to $10\%$ of gross collateral proceeds for administrative friction.
3. **Map Structural Subordination Across the Corporate Tree**: Draw a box for every legal subsidiary. Place debt obligations inside the exact entity that signed the note. Never consolidate subsidiaries into a parent group without checking for upstream guarantees.
4. **Discount for Time to Liquidation**: A recovery of $80\%$ paid three years after default has a present value of only $60\%$ at a $10\%$ discount rate. Factor the legal delay clock into your recovery evaluation.
""",
        r"R_{\text{senior}}=\min(D_s,A_{\text{net}});\quad R_{\text{junior}}=\frac{\min(D_j,\max(0,A_{\text{net}}-D_s))}{D_j}",
        'for assets in [70, 40]:\n    senior_claim = 50\n    junior_claim = 30\n    senior_rec = min(senior_claim, assets)\n    junior_rec = min(junior_claim, max(0, assets - senior_claim))\n    print(f"Net Assets: ${assets}M -> Senior: {round(senior_rec/senior_claim*100, 1)}%, Junior: {round(junior_rec/junior_claim*100, 1)}%")',
        "A collateral pool realizes $95M net of sale costs. Senior secured debt is $60M, junior subordinated debt is $50M, and common equity has 5 million shares. Calculate the dollar distribution and percentage recovery for senior debt, junior debt, and equity. Repeat the calculation if net proceeds fall to $55M.",
        "Under $95M proceeds: Senior debt receives $60M (100% recovery). Junior debt receives the remaining $35M out of its $50M claim (70.0% recovery). Equity receives $0. Under $55M proceeds: Senior debt receives all $55M ($55M / $60M = 91.7% recovery). Junior debt receives $0 (0% recovery). Equity receives $0.",
        [
            q(
                "Net liquidation proceeds are $75 million. Senior debt is $60 million and junior debt is $30 million. What is the recovery percentage for junior debt?",
                ["25%", "50%", "100%"],
                1,
                "Senior debt takes $60M, leaving $15M for the junior claim. Junior recovery is $15M / $30M = 50.0%.",
            ),
            q(
                "Why is debt issued by a parent holding company structurally subordinated to debt issued by an operating subsidiary?",
                [
                    "Operating subsidiaries never have debt",
                    "The parent company owns only the equity of the subsidiary; under absolute priority, subsidiary creditors must be paid in full before cash can be upstreamed to equity",
                    "Holding companies are exempt from bankruptcy laws",
                ],
                1,
                "Subsidiary creditors have a direct claim on operating assets; parent creditors only own the residual equity of the subsidiary, placing them behind all subsidiary obligations.",
            ),
            q(
                "A subsidiary realizes $100 million in liquidation. Its own local trade creditors and bank debt total $90 million. What amount is available to the parent company?",
                ["$100 million", "$90 million", "$10 million"],
                2,
                "Only the residual equity after satisfying subsidiary claims reaches the parent: $100M − $90M = $10M.",
            ),
        ],
    )

    add(
        "1.9",
        "II",
        "Indentures, covenants, and the capital structure",
        "Read a covenant as a defined test and model how additional borrowing changes creditor protection.",
        r"""
## The analytical question

When an investor purchases a 10-year corporate bond, the initial balance sheet may look impeccably safe: debt is low, cash reserves are abundant, and interest coverage is $6.0\times$. However, during the subsequent five years, an aggressive management team or private equity sponsor could:
- Issue $\$200\text{ million}$ of new senior debt to fund a speculative acquisition.
- Pay a massive debt-funded cash dividend to common shareholders.
- Pledge the company's crown jewel patents to a third-party lender.

If these actions are unrestricted, the initial bondholder's credit safety is systematically expropriated for the benefit of equity owners. This is why Graham and Dodd emphasized the study of the **Trust Indenture** and its **Protective Covenants**.

A covenant is a legally binding contractual restriction imposed on the borrower to preserve creditor protection throughout the life of the loan. Covenants generally fall into two categories:
1. **Incurrence Covenants**: The borrower is prohibited from taking a specific action (such as issuing new debt, paying dividends, or selling assets) *unless* it meets a specified financial test at the moment the action is taken.
2. **Maintenance Covenants**: The borrower must continuously maintain a specified financial ratio (e.g., Debt/EBITDA below $4.0\times$, Interest Coverage above $3.0\times$) tested at the end of every fiscal quarter.

Consider a common **Debt Incurrence Covenant** based on interest coverage:

$$\text{Post-Incurrence Coverage} = \frac{\text{EBIT}}{I_0 + I_{\text{new}}} \ge c_{\text{threshold}}$$

Where:
- $\text{EBIT}$ is defined operating earnings (often subject to contractual add-backs).
- $I_0$ is existing contractual interest expense.
- $I_{\text{new}}$ is annual interest on the proposed new debt issue.
- $c_{\text{threshold}}$ is the mandatory minimum coverage ratio (e.g., $3.0\times$).

Solving for the **Maximum Incremental Interest Capacity** ($\Delta I_{\max}$):

$$\Delta I_{\max} = \frac{\text{EBIT}}{c_{\text{threshold}}} - I_0$$

If management proposes an issue that adds more annual interest than $\Delta I_{\max}$, the issuance is legally barred by the indenture.

However, an analyst must read the **covenant definitions** with forensic skepticism:
- **Contractual Headroom $\ne$ Economic Safety**: Passing an incurrence test at mid-cycle does not guarantee survival during a recession.
- **EBITDA Add-Back Games**: Modern credit agreements frequently redefine EBITDA ("Consolidated EBITDA") to add back speculative "projected synergies," litigation reserves, and stock compensation. An issuer may appear to pass a $3.0\times$ covenant on contractual definitions while its true economic coverage is dangerously close to $1.2\times$.

## A worked example

Alder Manufacturing has $\$20.0\text{ million}$ in existing annual interest charges ($I_0$). Its audited current EBIT is $\$90.0\text{ million}$. Alder's senior bond indenture contains an incurrence covenant stipulating that Alder may not issue any additional debt unless its pro-forma interest coverage ratio is at least:

$$c_{\text{threshold}} = 3.0\times$$

Management proposes issuing $\$100.0\text{ million}$ of new debentures bearing an $8.0\%$ coupon, adding $I_{\text{new}} = \$8.0\text{ million}$ in annual interest expense.

Let us evaluate the proposal:
1. Determine total maximum permitted interest:
   $$I_{\max} = \frac{\text{EBIT}}{c_{\text{threshold}}} = \frac{\$90.0\text{M}}{3.0} = \$30.0\text{ million}$$
2. Calculate incremental interest capacity:
   $$\Delta I_{\max} = I_{\max} - I_0 = \$30.0\text{M} - \$20.0\text{M} = \$10.0\text{ million}$$
3. Since the proposed debt adds $\$8.0\text{ million}$ in interest, which is below the $\$10.0\text{ million}$ ceiling, the covenant is legally satisfied:
   $$\text{Pro-Forma Coverage} = \frac{\$90.0\text{M}}{\$20.0\text{M} + \$8.0\text{M}} = \frac{\$90.0\text{M}}{\$28.0\text{M}} = 3.21\times \ge 3.0\times \quad (\text{Passed})$$

Now conduct the **Economic Stress Test**:
Suppose an industrial recession causes Alder's EBIT to drop by $37.8\%$ to $\$56.0\text{ million}$:
- Prior to the new debt, coverage in the recession would have been:
  $$\text{Coverage}_{\text{prior}} = \frac{\$56.0\text{M}}{\$20.0\text{M}} = 2.80\times$$
- With the new debt added, pro-forma coverage in the recession drops to:
  $$\text{Coverage}_{\text{pro-forma}} = \frac{\$56.0\text{M}}{\$28.0\text{M}} = 2.00\times$$

While the transaction legally satisfied the covenant during good times, it reduced the recessionary cushion by nearly $30\%$, dramatically escalating default risk for the original bondholders.

## Research discipline

When evaluating indenture protections:
1. **Scrutinize the "Restricted Payments" Basket**: Examine the covenant governing dividends and share repurchases. Ensure that distributions to equity are strictly capped by cumulative net income minus previous distributions (a "builder basket").
2. **Audit Negative Pledge Clauses**: Verify that the issuer cannot pledge existing unencumbered assets to a new lender without granting equal and ratable security to existing bondholders.
3. **Inspect the Definition of Consolidated EBITDA**: Note every permitted add-back. Strip out non-cash "synergies" and management consulting fees to calculate true cash coverage.
4. **Track Change-of-Control Covenants**: Ensure the indenture contains a "put option" requiring the issuer to repurchase the bonds at $101\%$ of par if the company is acquired in a leveraged buyout.
""",
        r"\text{Incremental Interest Capacity}=\frac{\text{EBIT}}{c_{\text{threshold}}}-I_0;\quad \text{Coverage}_{\text{pro-forma}}=\frac{\text{EBIT}}{I_0+I_{\text{new}}}",
        'ebit = 90\nexisting_interest = 20\nthreshold = 3.0\nmax_interest = ebit / threshold\ncapacity = max_interest - existing_interest\nnew_interest = 8\npro_forma_coverage = ebit / (existing_interest + new_interest)\nprint("Contractual interest capacity ($M):", round(capacity, 2))\nprint("Pro-forma coverage:", round(pro_forma_coverage, 2))\nebit_stressed = 56\nprint("Stressed coverage:", round(ebit_stressed / (existing_interest + new_interest), 2))',
        "An issuer's bond indenture forbids debt issuance if interest coverage drops below 4.0x. Existing EBIT is $120M and existing interest is $24M. Management wants to issue bonds adding $8M in annual interest. Calculate the maximum incremental interest allowed, test whether the proposed issue passes, and calculate pro-forma coverage.",
        "Maximum permitted total interest is $120M / 4.0 = $30M. Existing interest is $24M, so incremental interest capacity is $30M − $24M = $6M. The proposed issuance adds $8M in interest, resulting in total interest of $32M and coverage of $120M / $32M = 3.75x. Because 3.75x is below the 4.0x threshold (and $8M exceeds the $6M capacity), the proposed debt issue is legally barred by the covenant.",
        [
            q(
                "An issuer reports EBIT of $80 million and its debt covenant requires minimum interest coverage of 4.0 times. What is the maximum total annual interest permitted?",
                ["$20 million", "$40 million", "$320 million"],
                0,
                "Maximum interest is $80M / 4.0 = $20 million.",
            ),
            q(
                "Why must an analyst examine the precise definition of EBITDA in a loan agreement?",
                [
                    "Contractual definitions often permit aggressive add-backs that make headroom appear larger than true economic cash flow",
                    "EBITDA definitions are legally standardized and identical in all contracts",
                    "Covenants only apply to equity holders",
                ],
                0,
                "Loan agreements often allow borrowers to add back restructuring charges and anticipated synergies, masking underlying operational deterioration.",
            ),
            q(
                "A debt covenant requires 3.0x coverage. EBIT is $75 million and existing interest is $18 million. What is the maximum additional interest expense the company can incur?",
                ["$7 million", "$25 million", "$57 million"],
                0,
                "Maximum total interest is $75M / 3.0 = $25M. Additional capacity is $25M − $18M = $7 million.",
            ),
        ],
    )

    add(
        "1.10",
        "II",
        "Yield, maturity, and callable claims",
        "Separate coupon income from contractual return and identify how call rights limit upside.",
        r"""
## The analytical question

Investors frequently commit serious errors by conflating different definitions of "return" on a bond. A debt instrument's contractual economics depend on its purchase price, face value, coupon structure, maturity date, and embedded issuer options.

We must separate three fundamentally different yield measures:
1. **Coupon Rate**: The annual dollar coupon payment divided by par value ($F = \$100$):
   $$\text{Coupon Rate} = \frac{C}{F}$$
2. **Current Yield**: The annual dollar coupon divided by the current market purchase price ($P$):
   $$\text{Current Yield} = \frac{C}{P}$$
3. **Yield to Maturity (YTM)**: The internal rate of return ($y$) that equates the purchase price with the present value of all future scheduled coupon payments and the principal repayment:
   $$P = \sum_{t=1}^T \frac{C}{(1+y)^t} + \frac{F}{(1+y)^T}$$

For a simplified one-year bond with coupon $C$, face value $F$, and purchase price $P$, the promised one-year contractual return is:

$$R_{\text{1-year}} = \frac{C + F - P}{P} = \frac{C + (F - P)}{P}$$

Notice the critical distinction:
- When purchasing a bond at a **discount** ($P < F$), the capital accretion $(F - P)$ elevates the total return well above the current yield.
- When purchasing at a **premium** ($P > F$), the capital write-down $(F - P < 0)$ severely drags down the total return below the current yield.

The most dangerous pitfall in bond investing is ignoring the **Issuer Call Option**. Most corporate bonds are callable at the option of the issuer after a specified protection period at a fixed redemption price ($P_{\text{call}}$, typically par or par plus a declining premium).

$$\text{Asymmetric Call Risk: When interest rates fall or credit improves, the issuer calls the bond.}$$

If you pay $\$108.00$ for a $7.0\%$ bond because you desire high income, and the company refinances next year by calling the bond at $\$100.00$, you receive $\$7.00$ in coupon income but suffer an $\$8.00$ capital loss, resulting in a net **negative return**! Therefore, any bond trading at a premium must be evaluated on a **Yield to Worst (YTW)** basis:

$$\text{Yield to Worst} = \min(\text{Yield to Maturity}, \text{Yield to Earliest Call})$$

## A worked example

Let us analyze two distinct bond investment opportunities available from Alder Manufacturing:

### Instrument A: The Discount Bond
- Purchase Price: $P = \$98.00$ per $\$100$ face value.
- Scheduled Maturity: Exactly 1 year.
- Annual Coupon: $C = \$6.00$.
- Non-callable.

Calculate the returns:
1. Current Yield:
   $$\text{Current Yield} = \frac{\$6.00}{\$98.00} = 6.12\%$$
2. Total Promised 1-Year Return:
   $$R_{\text{1-year}} = \frac{\$6.00 + (\$100.00 - \$98.00)}{\$98.00} = \frac{\$8.00}{\$98.00} = 8.16\%$$

The $\$2.00$ principal gain adds $2.04$ percentage points of annualized return above the current yield.

### Instrument B: The High-Coupon Premium Bond with Call Option
- Purchase Price: $P = \$105.00$ per $\$100$ face value.
- Scheduled Maturity: 5 years.
- Annual Coupon: $C = \$6.00$.
- Call Option: Issuer has the right to redeem the bond at $P_{\text{call}} = \$100.00$ in 1 year.

Suppose market interest rates decline, prompting Alder to exercise its call option at the end of Year 1:
1. Quoted Current Yield:
   $$\text{Current Yield} = \frac{\$6.00}{\$105.00} = 5.71\% \quad (\text{Seductive apparent yield})$$
2. Total Cash Proceeds at Year 1:
   $$\text{Proceeds} = C + P_{\text{call}} = \$6.00 + \$100.00 = \$106.00$$
3. Realized One-Year Return:
   $$R_{\text{call}} = \frac{\$106.00 - \$105.00}{\$105.00} = \frac{\$1.00}{\$105.00} = 0.95\%$$

Notice the trap: an unsophisticated investor seeing the $5.71\%$ current yield expects strong income, but realizes a pitiful $0.95\%$ return due to the $\$5.00$ capital loss upon redemption. Furthermore, the investor is handed cash right when interest rates have plunged, forcing them to reinvest at lower yields (**reinvestment risk**).

## Research discipline

When auditing debt securities and yields:
1. **Always Demand Yield to Worst**: Never purchase a premium bond based on yield to maturity or current yield. Always solve the yield to the earliest call date.
2. **Map the Full Schedule of Call Dates and Prices**: Document when call protection expires and whether the call price includes a "make-whole" premium (which protects the lender) or a fixed dollar call (which benefits the borrower).
3. **Assess Reinvestment Risk**: If a high-coupon bond is likely to be called, recognize that your effective investment duration is the call date, not the maturity date.
4. **Remember That Quoted Yield $\ne$ Expected Return**: Quoted YTM assumes zero defaults and prompt reinvestment of all coupons at the same interest rate. In low-grade bonds, expected return is always lower than quoted YTM due to default friction.
""",
        r"R_{\text{1-year}}=\frac{C+F-P}{P};\quad R_{\text{call}}=\frac{C+P_{\text{call}}-P}{P}",
        'price_disc = 98\ncoupon = 6\nface = 100\nret_disc = (coupon + face - price_disc) / price_disc\nprint("Discount 1-year return (%):", round(ret_disc * 100, 2))\nprice_prem = 105\ncall_price = 100\nret_call = (coupon + call_price - price_prem) / price_prem\nprint("Premium call 1-year return (%):", round(ret_call * 100, 2))',
        "An investor pays $103.00 for a bond with a $4.00 annual coupon that matures in 3 years. However, the issuer can call the bond in 1 year at par ($100.00). Calculate the current yield and the 1-year return if called. Explain the economic risk.",
        "Current yield is $4.00 / $103.00 = 3.88%. If called at year 1, total cash received is $4.00 (coupon) + $100.00 (call price) = $104.00. The realized 1-year return is ($104.00 − $103.00) / $103.00 = 0.97%. The economic risk is call/reinvestment risk: the investor suffers a $3.00 capital loss that wipes out 75% of the coupon income, and must reinvest proceeds in a lower-yield environment.",
        [
            q(
                "A one-year zero-coupon bond is purchased for $95.00 and redeems at $105.00 face value. What is its promised return?",
                ["5.0%", "10.53%", "11.05%"],
                1,
                "The return is ($105 − $95) / $95 = $10 / $95 = 10.53%.",
            ),
            q(
                "Who primarily benefits when an issuer exercises a call option on a high-coupon bond after market interest rates decline?",
                [
                    "The bondholder who receives cash earlier",
                    "The issuer who refinances at lower interest rates, leaving the investor to reinvest at lower yields",
                    "The regulatory clearinghouse",
                ],
                1,
                "The call option is an asymmetric advantage for the issuer, allowing it to extinguish expensive debt and refinance cheaply.",
            ),
            q(
                "An investor pays $102.00 for a bond with an annual coupon of $5.00. Exactly one year later, the issuer calls the bond at $100.00. What is the realized return?",
                ["4.90%", "2.94%", "5.00%"],
                1,
                "Total proceeds are $5.00 (coupon) + $100.00 (call) = $105.00. Return is ($105 − $102) / $102 = $3 / $102 = 2.94%.",
            ),
        ],
    )

# -------------------------------------------------------------------------
    # PART III: PREFERRED AND CONVERTIBLE CLAIMS
    # -------------------------------------------------------------------------

    add(
        "1.11",
        "III",
        "Preferred shares and cumulative claims",
        "Analyze dividend priority, arrears, and the difference between preferred equity and debt.",
        r"""
## The analytical question

Preferred stock occupies an intermediate position in the corporate capital structure, positioned directly between senior debt and common equity:
- **Resembles Debt in Upside**: It carries a fixed dividend rate (e.g., $6.0\%$ of par preference) with no automatic participation in corporate growth or super-profits.
- **Resembles Equity in Legal Enforceability**: Unlike bond interest, the failure to pay a preferred dividend does *not* constitute an immediate event of default and cannot trigger involuntary bankruptcy.

Because preferred shares lack the contractual enforceability of debt while lacking the unlimited appreciation of common equity, Graham and Dodd warned that preferred stock often combines the **defects of both classes with the advantages of neither**.

To evaluate preferred shares safely, the analyst must examine four critical legal features in the corporate charter:
1. **Cumulative Dividend Rights**: If an issuer suspends dividends during a downturn, do unpaid dividends accumulate as **arrears** that must be paid in full before common shareholders can receive any cash distribution?
   $$\text{Total Preferred Dividend Obligation} = \text{Current Annual Preference} + \text{Cumulative Arrears}$$
   $$\text{Arrears} = \sum_{t=1}^k \text{Omitted Annual Preferred Dividends}$$
2. **Liquidation Preference**: In a voluntary or involuntary liquidation, does the preferred stock have a senior claim (e.g., $\$100$ par plus all accumulated arrears) before any asset proceeds reach common owners?
3. **Voting Control Rights**: Does the charter stipulate that after a specified number of missed dividends (e.g., six consecutive quarters), preferred holders gain the legal right to elect a majority or special contingent of the board of directors?
4. **Subordinated / Junior Creditor Posture**: Preferred dividends are paid out of **after-tax, after-interest earnings**. Therefore, interest on debt must be satisfied first:
   $$\text{Preferred Dividend Coverage} = \frac{\text{Net Income}}{\text{Annual Preferred Dividend Obligation}} = \frac{(\text{EBIT} - \text{Interest}) \times (1 - t)}{\text{Preferred Dividends}}$$

An analyst must never accept the accounting presence of cumulative arrears as proof of imminent cash payment. A company in chronic distress may leave preferred dividends in arrears for a decade, eventually coercing preferred holders into accepting a dilutive recapitalization or deeply discounted common stock exchange.

## A worked example

Alder Manufacturing has issued $200,000$ shares of $6.0\%$ Cumulative Preferred Stock with a par liquidation preference of $\$100.00$ per share, representing a total liquidation preference of:

$$\text{Liquidation Preference} = 200,000 \times \$100.00 = \$20.0\text{ million}$$

The annual preferred dividend requirement is:

$$\text{Annual Preferred Requirement} = \$20.0\text{M} \times 0.06 = \$1.20\text{ million}$$

During a severe two-year industrial downturn, Alder's board exercised its discretion to suspend all dividend payments. Consequently, the company has accumulated two full years of dividend arrears:

$$\text{Accumulated Arrears} = 2 \times \$1.20\text{M} = \$2.40\text{ million}$$

Under Alder's corporate charter, no dividend or share repurchase can be distributed to common shareholders until all accumulated preferred arrears and the current year's preferred dividend are satisfied in cash.

In the current recovery year, Alder generates $\$5.0\text{ million}$ in legally and operationally available distributable cash:
1. First, satisfy the $\$2.40\text{ million}$ of accumulated preferred arrears.
2. Second, satisfy the current year's $\$1.20\text{ million}$ preferred dividend.
   $$\text{Total Preferred Priority Claim} = \$2.40\text{M (Arrears)} + \$1.20\text{M (Current)} = \$3.60\text{ million}$$
3. The remaining cash available for common shareholder distribution is:
   $$\text{Residual for Common} = \$5.0\text{M} - \$3.60\text{M} = \$1.40\text{ million}$$

Now consider an alternative scenario:
Suppose distributable cash in the recovery year is only $\$2.0\text{ million}$.
- The $\$2.0\text{ million}$ is insufficient to cover even the $\$2.40\text{ million}$ of arrears.
- The preferred holders receive the entire $\$2.0\text{ million}$ as partial payment of arrears, leaving $\$0.40\text{M}$ of unpaid arrears plus the $\$1.20\text{M}$ current dividend to roll forward.
- Common shareholders receive $\$0.00$.

## Research discipline

When auditing preferred stock securities:
1. **Never Analyze Preferred Coverage in Isolation**: Always calculate **Combined Fixed Charge and Preferred Coverage**:
   $$\text{Overall Coverage} = \frac{\text{EBIT}}{\text{Interest} + \frac{\text{Preferred Dividends}}{1 - t}}$$
   Because preferred dividends are paid from post-tax income, each dollar of preferred dividend requires $\$1 / (1 - t)$ of pre-tax earnings to service.
2. **Inspect the "Coercive Exchange" Risk**: Investigate whether management has the legal power to merge with a shell subsidiary to extinguish dividend arrears without requiring a two-thirds supermajority preferred vote.
3. **Verify Common Equity Buffer**: Ensure that the market value of common equity beneath the preferred shares provides a substantial cushion (at least $2.0\times$ the preferred liquidation preference) to absorb business losses.
4. **Separate Liquidation Rights from Going-Concern Rights**: A preferred stock with a $\$100$ liquidation preference may trade at $\$40$ in the secondary market because its dividend is non-cumulative or indefinitely suspended. Do not treat the liquidation par as an immediate price floor.
""",
        r"D_{\text{pref}}=\text{Preference}\times r;\quad \text{Total Priority}=\text{Arrears}+D_{\text{pref}};\quad \text{Coverage}=\frac{\text{EBIT}}{\text{Interest}+\frac{D_{\text{pref}}}{1-t}}",
        'preference = 20\nrate = 0.06\nannual_pref = preference * rate\narrears = annual_pref * 2\ntotal_pref_due = arrears + annual_pref\navailable_dist = 5.0\nresidual_common = available_dist - total_pref_due\nprint("Annual preferred dividend ($M):", round(annual_pref, 2))\nprint("Cumulative arrears ($M):", round(arrears, 2))\nprint("Total preferred claim before common ($M):", round(total_pref_due, 2))\nprint("Residual available for common ($M):", round(residual_common, 2))',
        "An issuer has $30M of 8% cumulative preferred stock with 3 years of unpaid dividend arrears. In the charter, all arrears and current preferred dividends must be paid before common distributions. The company has $12M of available distributable cash. Calculate the annual preferred dividend, the accumulated arrears, the total preferred priority requirement, and the residual cash for common.",
        "Annual preferred dividend is $30M × 8% = $2.4M. Three years of arrears equal $2.4M × 3 = $7.2M. Total priority preferred claim is $7.2M (arrears) + $2.4M (current) = $9.6M. Residual cash available for common distributions is $12.0M − $9.6M = $2.4M.",
        [
            q(
                "A company has $50 million of preferred stock with a 4% annual dividend rate. What is its annual preferred dividend requirement?",
                ["$2.0 million", "$4.0 million", "$12.5 million"],
                0,
                "Annual preferred dividend is $50M × 4% = $2.0 million.",
            ),
            q(
                "What is the precise legal effect of cumulative dividend arrears on preferred stock?",
                [
                    "It guarantees an immediate cash deposit in the investor's brokerage account",
                    "It creates a contractual priority barrier that legally bars common distributions until all arrears and current dividends are satisfied",
                    "It forces the issuer into immediate involuntary liquidation",
                ],
                1,
                "Cumulative arrears restrict common equity distributions until preferred claims are caught up, but do not guarantee immediate cash payment.",
            ),
            q(
                "Annual preferred dividends are $3 million, with two years in arrears. If the charter requires paying arrears and current preferred dividends before common, how much of an available $11 million distribution remains for common owners?",
                ["$5 million", "$8 million", "$2 million"],
                2,
                "Arrears equal $3M × 2 = $6M. Current dividend is $3M. Total preferred requirement is $6M + $3M = $9M. Residual for common is $11M − $9M = $2 million.",
            ),
        ],
    )

    add(
        "1.12",
        "III",
        "Convertible securities and dilution",
        "Calculate conversion value and premium while testing the quality of the underlying fixed claim.",
        r"""
## The analytical question

A convertible bond or convertible preferred stock represents a hybrid instrument:
- A senior fixed claim (promising interest and principal repayment at maturity).
- An embedded call option permitting the holder to exchange the bond into a specified number of common shares.

Wall Street marketing frequently depicts convertible securities as an ideal, "can't-lose" asset: *"Enjoy the safety and income of a bond with the unlimited upside participation of a growth stock!"*

Graham and Dodd demolished this superficial view. In reality, a convertible security offers two distinct sources of value, but also **two distinct sources of loss**:
1. If the underlying business deteriorates, the common stock collapses, dragging down the conversion value.
2. Simultaneously, if the company's credit quality deteriorates, the value of the "straight bond floor" plummets as default risk surges.

To analyze a convertible rigorously, you must compute four interrelated metrics:
1. **Conversion Ratio ($n$)**: The contractual number of common shares received upon converting one bond:
   $$n = \frac{\text{Face Value}}{\text{Conversion Price}} = \frac{F}{P_{\text{conversion}}}$$
2. **Conversion Value (Parity Value, $V_{\text{conversion}}$)**: The immediate market liquidation value of the underlying shares:
   $$V_{\text{conversion}} = n \times P_{\text{stock}}$$
3. **Conversion Premium ($\text{Premium}$)**: The percentage by which the market quote of the convertible bond ($P_{\text{convertible}}$) exceeds its immediate conversion value:
   $$\text{Conversion Premium} = \frac{P_{\text{convertible}}}{V_{\text{conversion}}} - 1 = \frac{P_{\text{convertible}} - V_{\text{conversion}}}{V_{\text{conversion}}}$$
4. **Straight Bond Investment Value (Bond Floor, $V_{\text{straight}}$)**: The theoretical price at which the bond would trade purely on its credit merit and coupon stream without any conversion privilege:
   $$V_{\text{straight}} = \sum_{t=1}^T \frac{C}{(1 + y_{\text{comparable}})^t} + \frac{F}{(1 + y_{\text{comparable}})^T}$$

The fatal error in convertible analysis is **adding the bond floor to the conversion value**. An investor cannot convert the bond into stock and also keep the principal! The conversion option is an *exclusive choice*: you receive either the debt cash flows or the equity shares, not both.

Furthermore, never view the straight bond floor as an invariant concrete support. If the issuer's core business collapses, the straight bond floor falls alongside the common stock.

## A worked example

Alder Manufacturing issues an invented $\$1,000$ face value ($F$) convertible debenture due in 5 years with a $4.0\%$ annual coupon ($C = \$40.00$). The bond is convertible into $25$ shares of common stock:

$$\text{Conversion Ratio: } n = 25\text{ shares}$$

$$\text{Conversion Price: } P_{\text{conversion}} = \frac{\$1,000}{25} = \$40.00\text{ per share}$$

Alder's common stock currently trades on the exchange at $P_{\text{stock}} = \$36.00$.

Let us compute the conversion analytics:
1. Conversion Value:
   $$V_{\text{conversion}} = 25 \times \$36.00 = \$900.00$$
2. Market Quote of Convertible: Suppose the convertible bond trades at $P_{\text{convertible}} = \$1,080.00$.
3. Conversion Premium:
   $$\text{Premium} = \frac{\$1,080.00}{\$900.00} - 1 = \frac{\$180.00}{\$900.00} = 20.0\%$$
   The investor is paying a $20.0\%$ premium over immediate equity parity to own the hybrid package.
4. Straight Bond Value ($V_{\text{straight}}$):
   A comparable non-convertible 5-year debenture of Alder with an identical $B+$ credit rating yields $8.0\%$ to maturity. Discounting the $4.0\%$ coupon stream and $\$1,000$ principal at $8.0\%$:
   $$V_{\text{straight}} = \sum_{t=1}^5 \frac{\$40}{(1.08)^t} + \frac{\$1,000}{(1.08)^5} \approx \$840.28 \approx \$850.00$$

Notice the two-sided exposure:
- **Premium over Bond Floor**: Paying $\$1,080.00$ represents a premium of $\$1,080 - \$850 = \$230.00$ ($27.1\%$) above the straight bond value.
- **Downside Risk**: If Alder's stock price falls to $\$20.00$, the conversion value plummets to $25 \times \$20 = \$500.00$. If Alder's operating earnings also drop so its credit rating is downgraded to CCC (yielding $14\%$), the straight bond floor drops to $\$656.00$. The convertible bond will fall from $\$1,080.00$ toward $\$656.00$—a painful $39.3\%$ loss!

## Research discipline

When evaluating convertible securities:
1. **Never Justify an Unsound Credit with an Equity Option**: If the issuer does not meet your minimum standards for bond safety (interest coverage and debt maturity liquidity), reject the convertible immediately. A speculative call option cannot rehabilitate an insolvent borrower.
2. **Audit Forced Conversion and Issuer Call Terms**: Check if the indenture permits the issuer to call the bond at par if the stock trades at $130\%$ of the conversion price for 20 consecutive trading days. When called, the holder is forced to convert or accept par, truncating the option duration.
3. **Model Fully Diluted Share Count**: In equity analysis, always calculate the EPS impact under the "if-converted" method: assume all in-the-money convertibles are converted into shares, eliminate the after-tax interest expense, and determine the dilution to existing owners.
4. **Compare Net Dividend Yield Drag**: Calculate how long it will take for the higher coupon on the convertible bond to amortize the conversion premium compared to holding the common shares directly.
""",
        r"V_{\text{conversion}}=n P_s;\quad \text{Premium}=\frac{P_c}{V_{\text{conversion}}}-1;\quad P_{\text{conversion}}=\frac{F}{n}",
        'face = 1000\nratio = 25\nstock_price = 36\nconv_price = face / ratio\nconv_val = ratio * stock_price\nmarket_conv_price = 1080\npremium = (market_conv_price / conv_val - 1) * 100\nprint("Conversion price ($):", conv_price)\nprint("Conversion value ($):", conv_val)\nprint("Conversion premium (%):", round(premium, 2))',
        "A $1,000 par convertible bond can be exchanged for 20 shares of common stock. The common stock currently trades at $45.00, and the convertible bond is quoted at $990.00. Calculate the conversion price, conversion value, and conversion premium. Explain why an analyst cannot add the $1,000 principal to the conversion value.",
        "Conversion price is $1,000 / 20 = $50.00 per share. Conversion value is 20 shares × $45.00 = $900.00. Conversion premium is ($990.00 − $900.00) / $900.00 = $90.00 / $900.00 = 10.0%. An analyst cannot add principal to conversion value because conversion is an mutually exclusive contractual choice: the investor either redeems the bond for principal or surrenders it for shares, never both.",
        [
            q(
                "A $1,000 face value convertible bond converts into 40 shares of common stock. What is its conversion price?",
                ["$40.00", "$25.00", "$4.00"],
                1,
                "Conversion price is $1,000 / 40 shares = $25.00 per share.",
            ),
            q(
                "Why can an estimated straight-bond floor fail to protect a convertible investor during severe business distress?",
                [
                    "Convertible bondholders are personally liable for company debt",
                    "A deteriorating business impairs creditworthiness and escalates default spreads, causing the straight-debt floor to collapse alongside the common stock",
                    "Bond floors are legally tied to the consumer price index",
                ],
                1,
                "When a company's operational viability is threatened, credit risk spikes and the bond floor drops, removing downside protection.",
            ),
            q(
                "A convertible bond trades at $1,100.00 and converts into 50 shares of stock currently trading at $20.00 per share. What is its conversion premium?",
                ["5.0%", "10.0%", "50.0%"],
                1,
                "Conversion value is 50 × $20 = $1,000. Premium is ($1,100 − $1,000) / $1,000 = 10.0%.",
            ),
        ],
    )

    # -------------------------------------------------------------------------
    # PART IV: THE COMMON OWNER'S INTEREST
    # -------------------------------------------------------------------------

    add(
        "1.13",
        "IV",
        "Common ownership and dividend policy",
        "Evaluate distributions and retention through the economic interests of common shareholders.",
        r"""
## The analytical question

Common shareholders occupy the **residual interest** in the corporation. They possess no contractual claim to a fixed dollar coupon, no guaranteed repayment of principal, and no legal right to compel dividend payments. Their economic outcome depends entirely on two factors:
1. **The Magnitude of Sustainable Free Cash Flow**: The actual surplus cash generated by operations after servicing debt, paying taxes, and funding all necessary maintenance capital expenditures.
2. **Management Stewardship in Capital Allocation**: What corporate management decides to do with the earnings retained inside the business rather than paid out as cash dividends.

Graham and Dodd established a critical principle regarding corporate retained earnings:

$$\text{Retained earnings belong to the business before they become cash to owners.}$$

An analyst must never treat an accounting dollar of reported net income as equivalent to a dollar of cash dividend received. When a company retains $\$1.00$ of earnings, it deprives shareholders of the opportunity to invest that cash elsewhere at their own discretion. Therefore, the retention of earnings is economically justified *only* if management reinvests that capital at an **incremental return on capital ($ROE_{\text{incremental}}$)** that exceeds the shareholder's required hurdle rate:

$$\text{Dividend Payout Ratio} = \frac{D}{E} = \frac{\text{Total Cash Dividends}}{\text{Net Income}}$$

$$\text{Retention Ratio} = b = 1 - \frac{D}{E} = \frac{\text{Retained Earnings}}{\text{Net Income}}$$

$$\text{Incremental Return on Retained Capital} = \frac{\Delta E}{\text{Retained Capital}} = \frac{E_{t+1} - E_t}{\text{Net Income}_t \times b}$$

If a mature business operates in a low-return or declining industry where incremental reinvestment earns only $5.0\%$, retaining $80\%$ of earnings destroys shareholder value! In such cases, the prudent policy is to distribute surplus cash to shareholders via dividends or disciplined share repurchases so owners can allocate capital to higher-return opportunities.

Conversely, in an exceptional franchise business that earns a sustained $20.0\%$ return on incremental capital without taking excessive leverage, high retention compounds shareholder wealth far more effectively than cash payouts subject to personal dividend taxes.

## A worked example

Let us evaluate the capital allocation policy of Alder Manufacturing. In the current fiscal year, Alder generates:
- Net income for common shareholders: $E = \$30.0\text{ million}$
- Cash dividends paid: $D = \$12.0\text{ million}$
- Retained earnings: $\text{Retention} = \$30.0\text{M} - \$12.0\text{M} = \$18.0\text{ million}$

Calculate the dividend metrics:
1. Dividend Payout Ratio:
   $$\text{Payout} = \frac{\$12.0\text{M}}{\$30.0\text{M}} = 40.0\%$$
2. Retention Ratio:
   $$\text{Retention Rate} = 1 - 0.40 = 60.0\%$$

Management announces that the full $\$18.0\text{ million}$ in retained earnings will be deployed to construct a secondary assembly plant.

Let us evaluate the economic merit across two prospective operating cases:

### Case A: Disciplined High-Return Project
Management's engineering and sales study demonstrates that the new plant will generate $\$1.80\text{ million}$ in sustainable annual post-tax operating profit after accounting for full equipment depreciation:
$$\text{Incremental Project ROE} = \frac{\Delta E}{\text{Retained Earnings}} = \frac{\$1.80\text{M}}{\$18.0\text{M}} = 10.0\%$$
If the shareholder's cost of equity capital is $9.0\%$, this retention creates economic value ($\text{ROE} > k_e$).

### Case B: Empire Building in a Saturated Market
Suppose industry competition intensifies, and the plant yields only $\$0.90\text{ million}$ in sustainable incremental profit:
$$\text{Incremental Project ROE} = \frac{\$0.90\text{M}}{\$18.0\text{M}} = 5.0\%$$
The accounting act of retaining the $\$18.0\text{ million}$ was identical, but economically, management has locked up $\$18.0\text{M}$ of owner capital in an asset earning a substandard $5.0\%$ return. Shareholders would have been substantially better off receiving the $\$18.0\text{M}$ as a special dividend to invest in $6.0\%$ high-grade notes!

## Research discipline

To evaluate common dividend and retention policy as a security analyst:
1. **Audit the 5-Year Cumulative Retention vs Profit Growth**: Compare the total dollars retained over the past five years with the net change in operating earnings:
   $$\text{Cumulative Retention Efficiency} = \frac{\sum_{t=1}^5 \Delta E_t}{\sum_{t=1}^5 \text{Retained Earnings}_t}$$
   If a company has retained $\$100\text{M}$ over five years but earnings are flat or declining, management is destroying capital.
2. **Verify That Dividends Are Funded by Free Cash Flow (Not Debt)**: Ensure that:
   $$\text{Free Cash Flow} = CFO - \text{Maintenance CapEx} \ge \text{Total Cash Dividends}$$
   If an issuer pays dividends while running negative free cash flow, it is borrowing money to pay shareholders—a dangerous Ponzi-like practice that endangers credit ratings.
3. **Check for "Empire Building" Incentives**: Review executive compensation schemes. If executive bonuses are tied to total revenue or total asset size rather than return on invested capital (ROIC) or per-share intrinsic value growth, management has a built-in conflict of interest to over-retain earnings.
4. **Deduct Mandatory Maintenance Reinvestment**: Do not confuse gross retained earnings with discretionary capital. If an asset-heavy business must spend $70\%$ of its earnings on escalating replacement equipment costs due to inflation, that cash was never truly available for distribution.
""",
        r"\text{Payout}=\frac{D}{E};\quad \text{Retention}=1-\frac{D}{E};\quad ROE_{\text{incremental}}=\frac{\Delta E}{\text{Retained Capital}}",
        'earnings = 30\ndividends = 12\nretained = earnings - dividends\npayout = dividends / earnings\nprint("Dividend payout ratio (%):", round(payout * 100, 1))\nprint("Retention ratio (%):", round((1 - payout) * 100, 1))\nfor delta_e in [1.8, 0.9]:\n    inc_roe = delta_e / retained\n    print(f"Incremental Profit: ${delta_e}M -> Incremental ROE: {round(inc_roe * 100, 1)}%")',
        "An enterprise earns $40M in net income, distributes $10M in dividends, and retains $30M. Management invests the entire $30M retained sum into an expansion project that generates $2.4M in recurring annual profit. Calculate the payout ratio, retention ratio, and incremental return on retained capital. State what the analyst must investigate before endorsing the retention.",
        "Payout ratio is $10M / $40M = 25.0%. Retention ratio is 1 − 0.25 = 75.0%. Incremental return on retained capital is $2.4M / $30M = 8.0%. Before endorsing this retention, the analyst must verify: (1) whether the 8.0% return exceeds the company's cost of equity capital, (2) whether the $2.4M profit is truly net of necessary maintenance CapEx, and (3) whether cash collections will match recognized accounting profit.",
        [
            q(
                "An issuer reports net income of $25 million and distributes $10 million in cash dividends. What is its dividend payout ratio?",
                ["25%", "40%", "60%"],
                1,
                "Dividend payout ratio is $10M / $25M = 40.0%.",
            ),
            q(
                "Under what economic condition is the retention of earnings justified from the perspective of common shareholders?",
                [
                    "Whenever management desires to build a larger corporate enterprise",
                    "Only when incremental retained capital generates a sustainable return on equity that exceeds the shareholder's required hurdle rate",
                    "Whenever the company pays no taxes",
                ],
                1,
                "Retention is only economically justified if the capital reinvested inside the firm earns a higher return than owners could earn independently.",
            ),
            q(
                "A corporation retains $20 million of earnings to fund a new facility that generates $1.0 million in annual incremental profit. A comparable external hurdle rate is 9%. What is the primary concern?",
                [
                    "The 5% incremental return is significantly below the 9% hurdle rate, indicating value-destroying capital allocation",
                    "The dividend payout ratio must be greater than 100%",
                    "The company has violated debt covenants",
                ],
                0,
                "Incremental ROE is $1.0M / $20M = 5.0%, which is below the 9% cost of capital, destroying shareholder value.",
            ),
        ],
    )

    add(
        "1.14",
        "IV",
        "Share count, repurchases, and owner outcomes",
        "Distinguish mechanical EPS changes from an improvement in the value owned by continuing shareholders.",
        r"""
## The analytical question

When an investor buys shares in a publicly traded company, they acquire a fraction of the enterprise. That fractional ownership is defined by the **per-share denominator**:

$$\text{Fractional Ownership} = \frac{\text{Shares Owned}}{N_{\text{total diluted shares}}}$$

Changes in the share count denominator ($N$) directly dictate the per-share value of continuing owners. These changes occur through three common corporate actions:
1. **Stock Splits and Stock Dividends**: Merely slice the corporate pizza into smaller slices. In a 2-for-1 split, the number of shares doubles, but the underlying business value and earnings are unchanged. Value per share drops by exactly $50\%$, leaving the economic wealth of each owner identical.
2. **New Share Issuance / Option Dilution**: Increases the share count. If new shares are issued below intrinsic business value (e.g., through massive stock option grants to executives or discounted equity placements), the intrinsic value belonging to existing shareholders is diluted and transferred away.
3. **Share Repurchases (Buybacks)**: The company uses corporate cash to buy its own shares on the open market and retire them.

Modern corporate executives frequently promote share repurchases as an unmitigated good because they mechanically increase reported Earnings Per Share (EPS):

$$\text{Mechanical EPS Boost: } \text{EPS}_{\text{after}} = \frac{\text{Net Income} - \text{Lost Cash Interest}}{N_{\text{initial}} - \Delta N} > \text{EPS}_{\text{initial}}$$

Graham and Dodd insisted that an analyst must look past mechanical EPS increases. A share repurchase creates or destroys value based entirely on the **price paid relative to intrinsic value**:

$$\text{Per-Share Value After Repurchase: } V_{\text{after/share}} = \frac{V_{\text{before}} - C_{\text{cash spent}}}{N_{\text{before}} - \frac{C_{\text{cash spent}}}{P_{\text{buyback}}}}$$

- **Accretive Repurchase ($P_{\text{buyback}} < V_{\text{intrinsic}}$)**: When management repurchases shares at a discount to intrinsic value, they acquire claims for less than they are worth. The remaining continuing shareholders experience an immediate increase in intrinsic value per share!
- **Value-Destroying Repurchase ($P_{\text{buyback}} > V_{\text{intrinsic}}$)**: When management repurchases shares at an inflated market price during a market boom, they transfer company cash to departing shareholders for more than the shares are worth. Continuing shareholders suffer a permanent destruction of per-share intrinsic value, even if reported EPS rises!

## A worked example

Let us trace the per-share mathematics of share repurchases for Alder Manufacturing. Alder's enterprise consists of:
- Pre-repurchase Equity Value: $V_{\text{before}} = \$100.0\text{ million}$ (which includes $\$20.0\text{ million}$ of nonoperating excess cash).
- Fully diluted share count: $N = 10.0\text{ million shares}$.
- True Intrinsic Value per Share:
  $$V_{\text{intrinsic}} = \frac{\$100.0\text{M}}{10.0\text{M}} = \$10.00\text{ per share}$$

The board authorizes deploying the entire $C = \$20.0\text{ million}$ in excess cash to execute a share repurchase program. Remaining equity value after spending the cash is:

$$V_{\text{remaining}} = \$100.0\text{M} - \$20.0\text{M} = \$80.0\text{ million}$$

Let us analyze the owner outcome across two distinct market price scenarios:

### Scenario 1: Disciplined Buyback at a Discount ($P_{\text{buyback}} = \$8.00$)
1. Shares retired:
   $$\Delta N = \frac{\$20.0\text{M}}{\$8.00} = 2.50\text{ million shares}$$
2. Remaining shares outstanding:
   $$N_{\text{after}} = 10.0\text{M} - 2.50\text{M} = 7.50\text{ million shares}$$
3. Intrinsic value per remaining share:
   $$V_{\text{after/share}} = \frac{\$80.0\text{M}}{7.50\text{M}} = \$10.67\text{ per share}$$
By repurchasing undervalued shares at $\$8.00$ ($20\%$ below intrinsic value), management created **$\$0.67$ per share** in real economic value for continuing shareholders.

### Scenario 2: Profligate Buyback at a Premium ($P_{\text{buyback}} = \$12.00$)
Suppose the stock surges during a market bubble, and management deploys the same $\$20.0\text{M}$ at $\$12.00$:
1. Shares retired:
   $$\Delta N = \frac{\$20.0\text{M}}{\$12.00} = 1.667\text{ million shares}$$
2. Remaining shares outstanding:
   $$N_{\text{after}} = 10.0\text{M} - 1.667\text{M} = 8.333\text{ million shares}$$
3. Intrinsic value per remaining share:
   $$V_{\text{after/share}} = \frac{\$80.0\text{M}}{8.333\text{M}} = \$9.60\text{ per share}$$
Continuing shareholders suffered a **$\$0.40$ per share loss** in intrinsic value! Overpaying for shares destroyed capital, even if reported EPS increased mechanically due to the smaller share denominator.

## Research discipline

When evaluating corporate share count changes and buybacks:
1. **Never Judge Buybacks by EPS Growth**: Calculate the intrinsic value per share before and after the repurchase. If the repurchase was executed above conservative intrinsic value, treat it as an impairment of capital.
2. **Audit Debt-Financed Buybacks**: Beware of management borrowing money to buy back stock to hit executive stock option bonus targets. This weakens the company's balance sheet and strips away creditor protection.
3. **Use the Fully Diluted Treasury Stock Method**: Ensure that all stock options, restricted stock units (RSUs), and convertible warrants are included in the diluted share denominator:
   $$N_{\text{diluted}} = N_{\text{basic}} + \text{Options} - \frac{\text{Option Proceeds}}{P_{\text{market}}}$$
4. **Distinguish Share Retirement from Share Creep**: Compare gross repurchases with net share reduction. If a company spends $\$500\text{M}$ buying back stock, but total share count increases due to lavish executive equity grants, the buyback was merely a disguised operating expense to offset executive dilution.
""",
        r"V_{\text{after/share}}=\frac{V_{\text{before}}-C}{N-\frac{C}{P_{\text{buyback}}}};\quad \Delta N=\frac{C}{P_{\text{buyback}}}",
        'v_before = 100\ncash_spent = 20\nshares_before = 10\nfor price in [8, 12]:\n    shares_retired = cash_spent / price\n    shares_after = shares_before - shares_retired\n    v_after_share = (v_before - cash_spent) / shares_after\n    print(f"Buyback Price: ${price} -> Shares Retired: {round(shares_retired, 3)}M -> Value per Share: ${round(v_after_share, 2)}")',
        "An enterprise has equity value of $240M across 20 million shares ($12.00/share). It spends $24M of excess cash repurchasing shares at $8.00 per share. Calculate the remaining share count and intrinsic value per share for continuing owners. Contrast this with the effect of a 2-for-1 stock split.",
        "At $8.00, the company retires $24M / $8.00 = 3 million shares. Remaining shares are 20M − 3M = 17 million. Remaining equity value is $240M − $24M = $216M. Value per remaining share is $216M / 17M = $12.71 per share (an accretion of $0.71/share). In contrast, a 2-for-1 split doubles the share count to 40M shares and halves the value to $6.00/share, leaving each owner's total economic wealth unchanged.",
        [
            q(
                "A company executes a 2-for-1 stock split with no change in business operations or cash. What happens to each existing shareholder's percentage ownership of the firm?",
                ["It doubles", "It is halved", "It remains completely unchanged"],
                2,
                "Both the number of shares held and the total shares outstanding double, so the fractional ownership percentage remains identical.",
            ),
            q(
                "Why is a mechanical increase in EPS following a share repurchase insufficient proof of value creation?",
                [
                    "EPS can rise while the company permanently overpays for shares above intrinsic value or impairs its financial liquidity",
                    "Share repurchases are illegal under federal law",
                    "Earnings can never be divided by share count",
                ],
                0,
                "Repurchasing stock above intrinsic value destroys per-share wealth for continuing owners, even if EPS rises due to a smaller share denominator.",
            ),
            q(
                "An enterprise has equity value of $60 million across 6 million shares ($10.00/share). It spends $12 million repurchasing shares at $12.00 per share. What is the remaining intrinsic value per share under unchanged operating value?",
                ["$12.00", "$9.60", "$10.00"],
                1,
                "At $12, the firm retires $12M / $12 = 1.0M shares, leaving 5.0M shares. Remaining equity is $60M − $12M = $48M. Value per share is $48M / 5.0M = $9.60.",
            ),
        ],
    )

    # -------------------------------------------------------------------------
    # PART V: INTERROGATE REPORTED EARNINGS
    # -------------------------------------------------------------------------

    add(
        "1.3",
        "V",
        "Normalize earning power",
        "Reconcile reported earnings to a defensible range of recurring profit across a business cycle.",
        r"""
## The analytical question

The income statement is not a record of immutable physical facts; it is an accounting estimate constructed under subjective management accruals, historical cost conventions, and cyclical economic conditions. A single year's reported net income can be distorted by:
- Peak cyclical demand or windfall commodity spikes.
- Nonrecurring gains from selling surplus real estate or patent royalties.
- Arbitrary restructuring charges, inventory write-downs, or legal settlements.

In *Security Analysis*, Graham and Dodd introduced the concept of **Normalized Earning Power**:

$$\text{Earning power represents the sustainable operating profit a company can generate across a full business cycle.}$$

To calculate normalized earning power, the analyst must build an explicit, auditable **reconciliation bridge** from reported net income to recurring economic earnings:

$$E_{\text{normalized}} = E_{\text{reported}} - \text{Nonrecurring Gains (After Tax)} + \text{Justified Recurring Deductions}$$

$$\text{Cycle Average EPS} = \frac{1}{K} \sum_{k=1}^K E_{\text{normalized}, k}$$

Here, $K$ represents the length of a representative business cycle (typically 5 to 10 years).

When constructing this bridge, the analyst must enforce strict methodological neutrality:
1. **Beware the "One-Way Add-Back" Bias**: Corporate management routinely adds back extraordinary losses, restructuring charges, and legal expenses, but almost never deducts extraordinary gains, property sale profits, or cyclical tax windfalls! A disciplined analyst must strip out nonrecurring gains with the exact same rigor applied to one-time charges.
2. **Interrogate Recurring "Nonrecurring" Charges**: If an issuer reports a "one-time restructuring charge" in four out of the last five years, that charge is not an isolated event; it is an ongoing economic cost of doing business. It must be included in normalized operating expenses.
3. **Adjust for Structural Evolution**: If the company acquired a major subsidiary three years ago or permanently divested a division, historical averages must be pro-forma adjusted to reflect the current corporate perimeter.

## A worked example

Let us evaluate the reported historical earnings record of Alder Manufacturing across an eight-year industrial cycle (figures in EPS):

| Year | Cycle Stage | Reported EPS | Material Footnote Items |
| :--- | :--- | :--- | :--- |
| **Year 1** | Trough | $\$2.00$ | Clean operating earnings |
| **Year 2** | Recovery | $\$3.00$ | Clean operating earnings |
| **Year 3** | Mid-Cycle | $\$4.00$ | Clean operating earnings |
| **Year 4** | Peak Boom | $\$3.00$ | Includes $\$0.50$ after-tax litigation settlement expense |
| **Year 5** | Current Year | $\$5.00$ | Includes $\$2.00$ after-tax gain from selling surplus land, and $\$0.40$ plant closure charge |

Let us normalize Year 5's earnings:
1. The $\$2.00$ after-tax real estate gain is a one-time liquidation of land. Alder cannot sell this land again next year. It must be deducted:
   $$\text{Subtotal} = \$5.00 - \$2.00 = \$3.00$$
2. Now evaluate the $\$0.40$ plant closure charge:
   - **Hypothesis A (Truly Isolated)**: If this represents the final exit from a discontinued product line with no further expenses, an analyst estimating prospective forward earnings might exclude it:
     $$\text{Normalized EPS}_{\text{forward}} = \$3.00 + \$0.40 = \$3.40$$
   - **Hypothesis B (Recurring Industrial Rationalization)**: If Alder routinely closes obsolete lines every two years, this is a recurring cost of manufacturing. Keeping the charge yields:
     $$\text{Normalized EPS}_{\text{conservative}} = \$3.00$$

Now examine the historical baseline:
The five-year clean recurring earnings series is approximately $\$2.00, \$3.00, \$4.00, \$3.50, \$3.00$.
- Five-Year Arithmetic Mean:
  $$\text{Mean Recurring EPS} = \frac{\$2.00 + \$3.00 + \$4.00 + \$3.50 + \$3.00}{5} = \$3.10$$

If an undisciplined analyst had applied a $15\times$ multiple to the unadjusted $\$5.00$ reported EPS, they would have estimated value at $\$75.00$. In reality, normalized earning power is between $\$3.00$ and $\$3.10$, supporting an intrinsic value of only $\$45.00$ to $\$46.50$! Capitalizing unadjusted peak earnings produces an expensive value trap.

## Research discipline

To normalize earning power with institutional rigor:
1. **Demand 7 to 10 Years of Primary Income Statements**: Spanning at least one full recessionary cycle. If 10 years are unavailable, synthesize a stress-tested trough year based on industry peer drawdowns.
2. **Reconcile Footnote 2 (Other Income and Expenses)**: Inspect non-operating lines for investment gains, foreign exchange translations, and pension actuarial adjustments.
3. **Maintain Tax Consistency**: Every adjustment must be adjusted for income taxes using the issuer's marginal corporate tax rate ($t$):
   $$\text{After-Tax Adjustment} = \text{Pre-Tax Item} \times (1 - t)$$
4. **Document the "Recurrence Audit"**: Maintain a register of all restructuring charges over the past decade. If total restructuring exceeds $10\%$ of cumulative net income, treat restructuring as an ongoing annual operating charge.
""",
        r"E_{\text{normalized}}=E_{\text{reported}}-\text{Gains}_{\text{nonrecurring}}+\text{Adjustments};\quad \bar{E}=\frac{1}{K}\sum_{k=1}^K E_k",
        'eps_history = [2.0, 3.0, 4.0, 3.5, 3.0]\nmean_eps = sum(eps_history) / len(eps_history)\nreported_curr = 5.0\ngain_land = 2.0\ncharge_closure = 0.4\nnorm_conservative = reported_curr - gain_land\nnorm_forward = norm_conservative + charge_closure\nprint("Cycle mean recurring EPS:", round(mean_eps, 2))\nprint("Normalized conservative EPS ($):", round(norm_conservative, 2))\nprint("Normalized forward EPS ($):", round(norm_forward, 2))',
        "An issuer reports EPS of $6.00 in the current fiscal year. The income statement includes an after-tax gain of $2.00 from selling a regional distribution center and an after-tax restructuring charge of $0.50. Calculate normalized EPS under: (1) a conservative case treating restructuring as recurring, and (2) an optimistic case treating the restructuring as completely nonrecurring. State which estimate should govern.",
        "Under the conservative case: deduct the $2.00 asset sale gain and keep the $0.50 charge as recurring operational expense: $6.00 − $2.00 = $4.00 normalized EPS. Under the optimistic case: deduct the $2.00 gain and add back the $0.50 charge: $6.00 − $2.00 + $0.50 = $4.50 normalized EPS. In accordance with Graham and Dodd's margin-of-safety principles, the conservative estimate of $4.00 must govern valuation and maximum purchase price limits until independent evidence proves restructuring costs have permanently ceased.",
        [
            q(
                "Which item is the clearest candidate for deduction from reported net income when estimating recurring earning power?",
                [
                    "Routine employee wages and salaries",
                    "A one-time after-tax gain from selling a surplus corporate headquarters building",
                    "Routine property rent expense",
                ],
                1,
                "Selling corporate real estate is a non-operating, non-repeatable transaction that cannot be capitalized as ongoing earning power.",
            ),
            q(
                "A manufacturing company reports 'exceptional restructuring charges' in six of the past seven fiscal years. How should a security analyst treat these charges?",
                [
                    "Add them back automatically to create higher adjusted EBITDA",
                    "Treat them as an ongoing recurring economic cost of doing business and incorporate them into normalized earnings",
                    "Ignore the income statement entirely and rely only on share price momentum",
                ],
                1,
                "Repeated 'one-time' charges reflect ongoing operational friction and capital rationalization, making them true recurring economic costs.",
            ),
            q(
                "An issuer reports EPS of $8.00, which includes a $3.00 after-tax nonrecurring disposal gain. No other adjustments are justified. What is the normalized EPS?",
                ["$11.00", "$8.00", "$5.00"],
                2,
                "Normalized EPS is $8.00 − $3.00 = $5.00.",
            ),
        ],
    )

    add(
        "1.15",
        "V",
        "Depreciation, depletion, and economic wear",
        "Explain how asset lives affect reported profit and distinguish noncash expense from avoidable economic cost.",
        r"""
## The analytical question

Depreciation is an accounting allocation that amortizes the historical monetary cost of a tangible fixed asset across its estimated useful life:

$$\text{Straight-Line Depreciation} = \frac{\text{Historical Asset Cost} - \text{Estimated Residual Value}}{\text{Estimated Useful Life in Years}}$$

Because depreciation is recorded as an expense without requiring an immediate outflow of cash in the current fiscal period, modern financial culture frequently dismisses it as a "mere non-cash accounting convention." Wall Street promoters routinely invite investors to add back depreciation to net income to arrive at **EBITDA** or "cash earnings."

Graham and Dodd viewed the casual addition of depreciation back to earnings as one of the most perilous fallacies in security analysis:

$$\text{Depreciation is a non-cash expense today because the cash was already spent yesterday.}$$

More importantly, machines physically wear out, vehicles degrade, and technology becomes obsolete. If a business fails to replace its worn-out machinery, its productive capacity will degrade, its operating costs will escalate, and it will eventually become uncompetitive.

Therefore, an analyst must separate:
1. **Accounting Depreciation**: A mechanical formula based on historical purchase prices and arbitrary accounting life estimates.
2. **Economic Capital Consumption**: The true annual cash reinvestment required to maintain the company's competitive position and physical volume (**Maintenance Capital Expenditures**):

$$\text{True Distributable Cash Proxy} \approx \text{EBITDA} - \text{Maintenance CapEx} - \text{Cash Taxes} - \text{Contractual Interest}$$

Furthermore, management possesses vast discretion over useful life assumptions:
- If a railroad extends the accounting life of its locomotives from $20\text{ years}$ to $30\text{ years}$, its annual depreciation expense immediately drops by $33\%$, creating an instant surge in reported net income!
- Yet, not a single additional freight car was loaded, no customer paid higher tariffs, and locomotives wear out at the exact same physical rate.

## A worked example

Let us examine the depreciation mechanics of Alder Manufacturing's primary fabrication plant. The equipment was purchased for $\$60.0\text{ million}$ with an assumed salvage value of zero.

### Case 1: Initial 10-Year Straight-Line Life
$$\text{Annual Depreciation Expense} = \frac{\$60.0\text{M}}{10} = \$6.00\text{ million per year}$$

### Case 2: Management Extends Useful Life to 15 Years
In Year 4, management revises its accounting estimate, extending the total useful life to 15 years:
$$\text{Revised Annual Depreciation} = \frac{\$60.0\text{M}}{15} = \$4.00\text{ million per year}$$
- Pre-tax reported profit immediately rises by $\$2.00\text{ million}$ per year.
- At a $25\%$ corporate tax rate, reported net income increases by $\$1.50\text{ million}$.
- Yet, cash flow from operations did not increase by a single dime.

Now evaluate Alder's cash generation from the perspective of an equity owner:
- Reported EBITDA: $\$30.0\text{ million}$
- Cash interest charges: $\$5.0\text{ million}$
- Representative corporate cash taxes: $\$5.0\text{ million}$
- Management-reported total CapEx: $\$12.0\text{ million}$

Through forensic inspection of Alder's engineering notes, you determine that of the $\$12.0\text{ million}$ in CapEx, $\$7.0\text{ million}$ is strictly **Maintenance CapEx** (replacing worn-out cutting dies, repaving warehouse loading docks, and software maintenance), while $\$5.0\text{ million}$ is **Discretionary Growth CapEx** (building a new testing lab).

Calculate the true distributable owner cash flow:

$$\text{Distributable Cash} = \text{EBITDA} - \text{Maintenance CapEx} - \text{Cash Taxes} - \text{Interest}$$

$$\text{Distributable Cash} = \$30.0\text{M} - \$7.0\text{M} - \$5.0\text{M} - \$5.0\text{M} = \$13.0\text{ million}$$

Notice the contrast:
- If an investor looked at EBITDA: $\$30.0\text{ million}$.
- If an investor looked at EBITDA minus all CapEx: $\$30.0\text{M} - \$12.0\text{M} - \$5.0\text{M} - \$5.0\text{M} = \$8.0\text{ million}$.
- True sustainable distributable cash flow is **$\$13.0\text{ million}$**.

EBITDA overstated owner cash by $\$17.0\text{ million}$ ($130\%$)! Relying on EBITDA would have grossly exaggerated the cash available to service debt or pay dividends.

## Research discipline

When auditing depreciation and capital expenditure:
1. **Track Changes in Useful Life Estimates**: Scrutinize Footnote 1 (Summary of Significant Accounting Policies). If average depreciable lives have lengthened over the past five years without new technology justification, restate earnings using consistent historical lives.
2. **Audit Gross vs Net Property, Plant, and Equipment (PP&E)**:
   $$\text{Asset Depleted Ratio} = \frac{\text{Accumulated Depreciation}}{\text{Gross PP&E}}$$
   If this ratio exceeds $70\%$, the company's physical plant is nearing exhaustion, signaling an impending tsunami of mandatory replacement CapEx.
3. **Compare Cumulative CapEx to Cumulative Depreciation**: Over a 7-to-10 year cycle, if cumulative CapEx is significantly lower than cumulative depreciation, the company is under-investing and liquidating its physical asset base through the income statement.
4. **Factor in Inflation Replacement Drag**: Remember that historical cost depreciation reflects yesterday's price levels. If a machine bought for $\$10\text{M}$ ten years ago costs $\$18\text{M}$ to replace today due to inflation, accounting depreciation will dramatically understate economic capital consumption.
""",
        r"D=\frac{\text{Cost}-\text{Residual}}{\text{Life}};\quad \text{Owner Cash}\approx EBITDA-\text{Maint CapEx}-\text{Taxes}-\text{Interest}",
        'cost = 60\ndeprec_10 = cost / 10\ndeprec_15 = cost / 15\nprint("10-Year annual depreciation ($M):", deprec_10)\nprint("15-Year annual depreciation ($M):", deprec_15)\nprint("Accounting profit boost ($M):", deprec_10 - deprec_15)\nebitda = 30\nmaint_capex = 7\ntaxes = 5\ninterest = 5\nowner_cash = ebitda - maint_capex - taxes - interest\nprint("True distributable owner cash ($M):", owner_cash)',
        "An industrial asset costing $80M with zero salvage value is depreciated over 8 years. Management considers extending the depreciable life to 10 years. Calculate the annual depreciation under both assumptions and the resulting pre-tax profit increase. Explain why an analyst evaluating cash flow should not treat this profit increase as an economic gain.",
        "Annual depreciation over 8 years is $80M / 8 = $10.0M. Over 10 years, it is $80M / 10 = $8.0M. Pre-tax accounting profit increases by $10.0M − $8.0M = $2.0M per year. An analyst must not treat this as an economic gain because extending the accounting useful life does not produce a single dollar of additional cash revenue or change the physical wear-and-tear of the machinery; it merely spreads a past sunk cash outlay across a longer accounting timeline.",
        [
            q(
                "An asset costing $45 million with zero residual value has an estimated useful life of 9 years. What is its annual straight-line depreciation?",
                ["$4.0 million", "$5.0 million", "$9.0 million"],
                1,
                "Annual straight-line depreciation is $45M / 9 = $5.0 million.",
            ),
            q(
                "Why can relying on EBITDA severely overstate the cash resources available to corporate security owners?",
                [
                    "EBITDA does not deduct the mandatory capital expenditures required to replace worn-out machinery, nor does it deduct taxes or interest",
                    "EBITDA is calculated after deducting dividends",
                    "EBITDA cannot be computed for industrial companies",
                ],
                0,
                "EBITDA ignores the economic reality of capital consumption; machinery must be maintained and replaced to sustain business operations.",
            ),
            q(
                "A company extends the depreciable life of its plant from 10 years to 20 years, with historical cost of $100 million and zero residual value. What happens to annual pre-tax accounting profit, all else equal?",
                [
                    "It rises by $5.0 million with no change in cash flow",
                    "It rises by $10.0 million in cash",
                    "It falls by $5.0 million",
                ],
                0,
                "Depreciation falls from $100M/10 = $10M to $100M/20 = $5M. Pre-tax profit rises by $5.0 million purely through an accounting estimate change.",
            ),
        ],
    )

    add(
        "1.16",
        "V",
        "Inventory, reserves, and profit comparability",
        "Trace how inventory and reserve estimates can shift profit between periods without equivalent economic improvement.",
        r"""
## The analytical question

Inventory valuation and loss allowances represent two of the most potent levers by which corporate management can distort reported earnings between accounting periods.

Consider the economic reality of inventory in an inflationary environment:
- **First-In, First-Out (FIFO)**: Assumes the oldest (cheapest) inventory units acquired are sold first. During inflation, cost of goods sold (COGS) reflects older, lower costs, producing higher reported gross profit. However, to keep store shelves stocked, the company must immediately replenish inventory at today's higher replacement costs! The reported profit contains an ephemeral **phantom inventory holding gain**.
- **Last-In, First-Out (LIFO)** / **Replacement Cost Accounting**: Matches current sales against the cost of acquiring goods today, producing a truer picture of distributable economic profit:

$$\text{Reported Gross Profit} = Q \times (P_{\text{selling}} - C_{\text{historical}})$$

$$\text{Economic Replacement Gross Profit} = Q \times (P_{\text{selling}} - C_{\text{replacement}})$$

$$\text{Phantom Inventory Profit} = Q \times (C_{\text{replacement}} - C_{\text{historical}})$$

The second major area of managerial manipulation is **Reserve and Allowance Accounting** (e.g., allowances for doubtful accounts, warranty reserves, loan loss reserves, and inventory obsolescence allowances).

Under accrual accounting, management establishes a balance sheet reserve by taking a non-cash expense against current earnings:
- In prosperous boom years, an aggressive management team can intentionally over-provision reserves—creating a hidden **"cookie-jar reserve"**.
- When earnings stumble in a subsequent recession, management simply reverses ("releases") the reserve into earnings, manufacturing artificial accounting profit without receiving a single dollar of customer cash!

To detect reserve manipulation, the analyst must demand an auditable **Reserve Roll-Forward Schedule**:

$$\text{Ending Reserve} = \text{Beginning Reserve} + \text{New Provisions Charged to P&L} - \text{Actual Cash Charge-Offs} \pm \text{Revisions}$$

## A worked example

Let us examine Alder Manufacturing's inventory and allowance disclosures for the current fiscal year.

### Inventory Analysis
Alder sells $100,000$ specialty valve units at a price of $P_{\text{selling}} = \$15.00$ each.
- The recorded FIFO historical cost of these units is $C_{\text{historical}} = \$8.00$ per unit.
- Due to recent metal price inflation, replenishing these valves currently costs $C_{\text{replacement}} = \$11.00$ per unit.

Compare the reporting results:
1. Reported FIFO Gross Profit:
   $$\text{Reported GP} = 100,000 \times (\$15.00 - \$8.00) = \$700,000$$
2. Economic Replacement Gross Profit:
   $$\text{Replacement GP} = 100,000 \times (\$15.00 - \$11.00) = \$400,000$$
3. Phantom Inventory Holding Profit:
   $$\text{Phantom Profit} = \$700,000 - \$400,000 = \$300,000$$

If Alder distributes the full $\$700,000$ to shareholders, it will not have enough cash left to replace its $100,000$ valves! Distributing phantom inventory gains liquidates working capital.

### Reserve Roll-Forward Audit
Now examine Alder's Allowance for Doubtful Accounts across the year:
- Beginning Allowance: $\$8.0\text{ million}$
- Actual customer defaults written off during the year: $\$3.0\text{ million}$
- Expected year-end allowance needed based on historical default rates: $\$7.0\text{ million}$

However, management changes its "subjective model assumptions" and establishes the ending reserve at only $\$3.0\text{ million}$.
Tracing the roll-forward:
$$\text{Ending} = \text{Beginning} + \text{P&L Provision} - \text{Charge-Offs}$$
$$\$3.0\text{M} = \$8.0\text{M} + \text{P&L Provision} - \$3.0\text{M}$$
$$\text{P&L Provision} = \$3.0\text{M} - \$5.0\text{M} = -\$2.0\text{ million}$$

Management recorded a **$\$2.0\text{ million}$ negative expense (reserve release)**, boosting pre-tax earnings by $\$2.0\text{ million}$!
Not a single delinquent customer paid back a debt. The $\$2.0\text{M}$ earnings boost was manufactured solely by relaxing the allowance criteria. A forensic analyst normalizes earnings by stripping out this $\$2.0\text{M}$ paper gain.

## Research discipline

When evaluating inventory and reserve quality:
1. **Demand the LIFO Reserve Footnote**: In US GAAP filings, check Note 2 (Inventories). If a company uses FIFO, calculate the inventory holding gain by checking the change in replacement costs.
2. **Audit Days Inventory Outstanding (DIO)**:
   $$\text{DIO} = \frac{\text{Ending Inventory}}{\text{COGS}} \times 365$$
   If DIO surges by $25\%$ while sales growth is flat, the company is accumulating unsold goods, raising the risk of future emergency inventory write-downs.
3. **Compare Reserve Balances to Underlying Assets**: Calculate:
   $$\text{Coverage Ratio} = \frac{\text{Allowance for Doubtful Accounts}}{\text{Gross Accounts Receivable}}$$
   If gross receivables rose by $40\%$ but the allowance fell from $5.0\%$ to $2.5\%$, management is suppressing credit provisions to inflate earnings.
4. **Never Count the Same Impairment Twice**: If you take a conservative balance-sheet haircut on inventory during asset valuation, do not deduct the same inventory write-down a second time when normalizing earnings.
""",
        r"GP_{\text{replacement}}=Q(P-C_{\text{replacement}});\quad \text{Reserve}_{\text{end}}=\text{Reserve}_{\text{beg}}+\text{Provision}-\text{Write-Offs}",
        'units = 100000\nprice = 15\ncost_hist = 8\ncost_repl = 11\ngp_reported = units * (price - cost_hist)\ngp_repl = units * (price - cost_repl)\nprint("Reported gross profit ($):", gp_reported)\nprint("Replacement gross profit ($):", gp_repl)\nprint("Phantom inventory gain ($):", gp_reported - gp_repl)',
        "An enterprise sells 200,000 components at $12.00 each. Recorded inventory cost is $7.00 per unit, while the cost to replenish the stock is $9.00 per unit. Calculate reported gross profit, replacement-cost gross profit, and phantom inventory profit. Explain what happens if management treats the entire reported gross profit as distributable cash.",
        "Reported gross profit is 200,000 × ($12.00 − $7.00) = $1,000,000. Replacement-cost gross profit is 200,000 × ($12.00 − $9.00) = $600,000. Phantom inventory profit is $1,000,000 − $600,000 = $400,000. If management distributes the entire $1,000,000 reported profit as dividends, the company will have only $1,400,000 left from sales ($2.4M revenue − $1.0M dividend), which is insufficient to replace the 200,000 units at $9.00 ($1,800,000 required). Distributing phantom inventory profits forcibly shrinks the physical operating scale of the business.",
        [
            q(
                "A company sells 50,000 units at $20.00 each with a current replacement cost of $14.00 each. What is its economic replacement-cost gross profit?",
                ["$300,000", "$700,000", "$1,000,000"],
                0,
                "Replacement-cost gross profit is 50,000 × ($20 − $14) = $300,000.",
            ),
            q(
                "A company's pre-tax profit surges because management released $5 million from its warranty reserve into earnings. What should an analyst request to verify the quality of this profit?",
                ["Only the company's stock price chart", "A complete multi-year warranty reserve roll-forward schedule and empirical product failure rate data", "An increase in the price-to-earnings multiple"],
                1,
                "A reserve release is an accounting estimate change; verifying it requires empirical data showing that actual product failure claims have permanently declined.",
            ),
            q(
                "Recorded inventory unit cost is $5.00, replacement cost is $8.00, and 100 units are sold. By how much does reported gross profit exceed replacement-cost gross profit?",
                ["$100.00", "$300.00", "$800.00"],
                1,
                "Cost difference is $8 − $5 = $3 per unit. For 100 units, the phantom inventory holding profit is $300.00.",
            ),
        ],
    )

    add(
        "1.17",
        "V",
        "Profit, cash conversion, and financing strain",
        "Reconcile a simplified earnings-to-cash bridge and identify when growth consumes liquidity.",
        r"""
## The analytical question

One of the most frequent causes of corporate distress is the fatal divergence between **accrual accounting profit** and **cash conversion reality**:

$$\text{A company can report booming record net income and go completely bankrupt at the same time.}$$

How does this happen? Under accrual accounting rules:
- Revenue is recognized when a commercial contract is fulfilled, regardless of whether the customer pays cash today, next year, or never.
- Expenses are capitalized into inventory or deferred assets rather than expensed immediately.

If a company aggressively expands sales by offering loose credit terms to financially fragile customers, its accounts receivable surge. If it overproduces goods to artificially lower unit fixed costs, its warehouse inventory explodes. On the income statement, net income looks spectacular. On the balance sheet, cash vanishes into working capital!

To bridge the gap between accounting net income and actual cash in the bank, the analyst constructs the **Cash Flow from Operations (CFO)** bridge:

$$\text{CFO} \approx \text{Net Income} + \text{Depreciation} - \Delta \text{Accounts Receivable} - \Delta \text{Inventory} + \Delta \text{Accounts Payable} \pm \Delta \text{Other}$$

$$\text{Free Operating Cash Flow to Firm} = \text{CFO} - \text{Maintenance CapEx}$$

Notice the signs of working capital changes:
- An **increase in Accounts Receivable** ($+\Delta \text{AR}$) is a **cash outflow** (cash is locked up in unpaid customer invoices).
- An **increase in Inventory** ($+\Delta \text{Inv}$) is a **cash outflow** (cash was spent purchasing raw materials sitting idle on warehouse shelves).
- An **increase in Accounts Payable** ($+\Delta \text{AP}$) is a **cash inflow** (the company delayed paying its suppliers, preserving cash).

When $\Delta \text{AR} + \Delta \text{Inv}$ consistently outpaces $\Delta \text{AP}$, growth is consuming liquidity. If the company cannot secure external bank loans or sell equity, it will suffer a fatal liquidity crisis despite pristine reported accounting profits.

## A worked example

Let us evaluate the cash conversion performance of Alder Manufacturing across two contrasting operating scenarios:

### Scenario 1: Healthy Normalized Cash Conversion
Alder reports:
- Net Income: $\$20.0\text{ million}$
- Depreciation Expense: $\$6.0\text{ million}$
- Working capital changes:
  - Accounts receivable increase: $+\$8.0\text{ million}$
  - Inventory increase: $+\$5.0\text{ million}$
  - Operating accounts payable increase: $+\$3.0\text{ million}$
- Total Capital Expenditures: $\$7.0\text{ million}$

Let us calculate operating cash flow and free cash flow:
1. Cash Flow from Operations:
   $$\text{CFO} = \$20.0\text{M} + \$6.0\text{M} - \$8.0\text{M} - \$5.0\text{M} + \$3.0\text{M} = \$16.0\text{ million}$$
2. Cash Remaining After CapEx:
   $$\text{FCF} = \text{CFO} - \text{CapEx} = \$16.0\text{M} - \$7.0\text{M} = \$9.0\text{ million}$$
Alder generated $\$9.0\text{ million}$ in discretionary surplus cash to repay debt or distribute to owners.

### Scenario 2: Aggressive Channel Stuffing and Working Capital Bleed
Suppose that in order to meet an aggressive earnings target, management shipped unrequested machinery to dealers at year-end on extended 180-day credit terms:
- Reported Net Income remains unchanged: $\$20.0\text{ million}$
- Depreciation remains unchanged: $\$6.0\text{ million}$
- Accounts receivable surge by: $+\$18.0\text{ million}$ (an additional $\$10.0\text{M}$ drag!)
- Inventory increases by: $+\$5.0\text{ million}$
- Accounts payable increase: $+\$3.0\text{ million}$
- CapEx remains: $\$7.0\text{ million}$

Recalculate the cash bridge:
1. Cash Flow from Operations:
   $$\text{CFO} = \$20.0\text{M} + \$6.0\text{M} - \$18.0\text{M} - \$5.0\text{M} + \$3.0\text{M} = \$6.0\text{ million}$$
2. Cash Remaining After CapEx:
   $$\text{FCF} = \text{CFO} - \text{CapEx} = \$6.0\text{M} - \$7.0\text{M} = -\$1.0\text{ million}$$

Look at the revelation! While reported net income was an impressive $\$20.0\text{ million}$, the business actually suffered a **$\$1.0\text{ million}$ cash deficit**!
Alder had to draw down its bank line of credit to survive the year. If this working capital bleed continues for another two quarters, Alder will breach its debt covenants.

## Research discipline

To audit the accrual gap and cash conversion quality:
1. **Calculate the Accrual Ratio**:
   $$\text{Balance Sheet Accrual Ratio} = \frac{\Delta \text{Net Operating Assets}}{\text{Average Net Operating Assets}}$$
   A consistently high or rising accrual ratio indicates poor earnings quality and a high probability of future earnings restatements or write-offs.
2. **Track the Cash Conversion Cycle (CCC)**:
   $$\text{CCC} = \text{Days Sales Outstanding} + \text{Days Inventory Outstanding} - \text{Days Payables Outstanding}$$
   An expanding CCC reveals an operational bottleneck where cash is trapped inside working capital.
3. **Compare 5-Year Cumulative Net Income to 5-Year Cumulative CFO**:
   $$\text{Cumulative Cash Realization} = \frac{\sum_{t=1}^5 \text{CFO}_t}{\sum_{t=1}^5 \text{Net Income}_t}$$
   Over a 5-year period, this ratio should average near $1.0\times$ or higher for a healthy company. If cumulative CFO is less than $70\%$ of reported net income, the company is capitalizing expenses or recognizing uncollectible revenues.
4. **Audit Footnote Changes in Factoring and Supply Chain Finance**: Ensure that the company is not masking an accounts receivable blow-up by selling receivables to banks off-balance-sheet with recourse ("factoring").
""",
        r"CFO \approx NI + D - \Delta AR - \Delta Inv + \Delta AP;\quad FCF = CFO - \text{CapEx}",
        'ni = 20\ndeprec = 6\nar_growth_healthy = 8\nar_growth_distress = 18\ninv_growth = 5\nap_growth = 3\ncapex = 7\ncfo_healthy = ni + deprec - ar_growth_healthy - inv_growth + ap_growth\nprint("Healthy operating cash flow ($M):", cfo_healthy)\nprint("Healthy cash after CapEx ($M):", cfo_healthy - capex)\ncfo_distress = ni + deprec - ar_growth_distress - inv_growth + ap_growth\nprint("Distressed operating cash flow ($M):", cfo_distress)\nprint("Distressed cash after CapEx ($M):", cfo_distress - capex)',
        "An enterprise reports net income of $15M and depreciation of $4M. During the year, accounts receivable increased by $6M, inventory increased by $2M, and accounts payable increased by $1M. Capital expenditures were $5M. Reconcile operating cash flow (CFO) and free cash flow after CapEx. State the primary risk if accounts receivable fail to convert to cash next year.",
        "Operating cash flow is CFO = $15M (NI) + $4M (D) − $6M (ΔAR) − $2M (ΔInv) + $1M (ΔAP) = $12M. Free cash flow after CapEx is $12M − $5M = $7M. The primary risk is that if the $6M receivables buildup represents uncollectible customer balances or aggressive sales terms, the company will be forced to record a future bad-debt write-down, permanently impairing both reported equity book value and future liquidity.",
        [
            q(
                "An issuer experiences an increase in operating accounts receivable during the year. All else equal, what is the effect of this increase in the operating cash flow bridge?",
                [
                    "It increases operating cash flow relative to net income",
                    "It uses cash and is deducted from net income in the cash bridge because recognized revenue has not yet been collected in cash",
                    "It has zero impact on cash or accounting records",
                ],
                1,
                "An increase in receivables means revenue was recognized on credit without receiving cash, requiring a deduction in the CFO bridge.",
            ),
            q(
                "Why must a security analyst compare cumulative net income to cumulative operating cash flow over a 5-to-10 year period?",
                [
                    "To distinguish temporary working capital timing differences from chronic, structural earnings quality deterioration",
                    "To eliminate all future market volatility",
                    "To avoid reading the financial footnotes",
                ],
                0,
                "Over multiple years, temporary working capital swings should average out; a chronic divergence reveals aggressive accounting or uncollectible revenues.",
            ),
            q(
                "A company reports net income of $12 million, depreciation of $3 million, and its net operating working capital (AR + Inv − AP) increases by $7 million. What is its operating cash flow?",
                ["$22 million", "$16 million", "$8 million"],
                2,
                "Operating cash flow is $12M + $3M − $7M = $8 million.",
            ),
        ],
    )

# -------------------------------------------------------------------------
    # PART VI: ASSETS AND THEIR REALIZABILITY
    # -------------------------------------------------------------------------

    add(
        "1.4",
        "VI",
        "Net current assets and liquidation haircuts",
        "Calculate NCAV and a separate stressed realization estimate after every senior claim.",
        r"""
## The analytical question

Among Benjamin Graham's most celebrated quantitative screening techniques is the **Net Current Asset Value (NCAV)** method—often popularized as the "cigar-butt" or net-net investment strategy.

Graham defined Net Current Asset Value with complete legal and accounting precision:

$$\text{NCAV per Share} = \frac{\text{Current Assets} - \text{Total Liabilities} - \text{Preferred Claims}}{N_{\text{diluted shares}}}$$

Notice the fundamental distinction between **NCAV** and **Working Capital**:
- **Working Capital** deducts only *current liabilities* from current assets ($\text{CA} - \text{CL}$). It ignores long-term bonds, bank term loans, and pension obligations.
- **Net Current Asset Value** deducts **TOTAL LIABILITIES**—including every dollar of long-term debt, bank loans, trade payables, deferred taxes, and preferred stock preferences.

In essence, the NCAV screen assigns **zero economic value** to the company's property, plant, equipment (PP&E), customer lists, patents, and goodwill! If a stock can be purchased at a price below its NCAV, the investor is effectively buying the company's cash, receivables, and inventory at a discount, while acquiring the entire operating factory, machinery, and commercial enterprise for free.

Graham's classic operational rule was to purchase diversified baskets of securities trading at a **one-third discount to NCAV** (or paying no more than two-thirds of NCAV):

$$P_{\max} \le \frac{2}{3} \times \text{NCAV} = 0.667 \times \text{NCAV}$$

However, in professional security analysis, an analyst cannot simply take recorded balance sheet current assets at face value. In an actual orderly liquidation or distressed wind-down, assets suffer substantial **realization haircuts**:
- **Cash and Cash Equivalents**: Realize $100\%$ (unless held in restricted foreign accounts subject to capital controls).
- **Accounts Receivable**: Realize $75\%$ to $85\%$ (customers dispute invoices, demand warranty offsets, or default when a supplier shuts down).
- **Inventories**: Realize $40\%$ to $60\%$ (raw materials sell at scrap discounts; work-in-process is virtually worthless; finished goods require fire-sale discounts).
- **Fixed Assets (PP&E)**: Realize $10\%$ to $25\%$ of net book value at industrial auctions.
- **Total Liabilities**: Must be paid **$100\%$ in full** (creditors do not accept haircuts unless forced through bankruptcy).
- **Administrative Closure Costs**: Deduct $5\%$ to $10\%$ of assets for employee severance, lease break penalties, and legal fees.

$$\text{Adjusted Liquidation Value} = \frac{1.0 \times \text{Cash} + 0.80 \times \text{AR} + 0.50 \times \text{Inv} + 0.20 \times \text{PP\&E} - \text{TL} - \text{Closure Costs}}{N}$$

## A worked example

Let us audit the balance sheet of Alder Manufacturing under both classical NCAV and stressed liquidation realization. Alder has $10.0\text{ million}$ common shares outstanding ($N$) and trades at a market quote of $P = \$6.20$.

Alder's balance sheet reports (in millions):
- Cash and marketable securities: $\$40.0\text{ million}$
- Accounts receivable: $\$60.0\text{ million}$
- Inventory: $\$80.0\text{ million}$
- Property, Plant, & Equipment (PP&E, net book value): $\$90.0\text{ million}$
- **Total Current Assets**: $\$40.0\text{M} + \$60.0\text{M} + \$80.0\text{M} = \$180.0\text{ million}$
- **Total Liabilities** (current + long-term debt): $\$100.0\text{ million}$
- Preferred stock claims: $\$0.00$

### Step 1: Classical Benjamin Graham NCAV
Calculate total company NCAV:
$$\text{Total NCAV} = \text{Current Assets} - \text{Total Liabilities} = \$180.0\text{M} - \$100.0\text{M} = \$80.0\text{ million}$$

Divide by $10.0\text{ million}$ shares:
$$\text{NCAV per Share} = \frac{\$80.0\text{M}}{10.0\text{M}} = \$8.00\text{ per share}$$

Graham's two-thirds maximum purchase price ceiling is:
$$P_{\max} = \frac{2}{3} \times \$8.00 = \$5.33\text{ per share}$$
At the current market quote of $\$6.20$, the stock is below NCAV ($\$8.00$), but fails Graham's strict two-thirds margin-of-safety screen ($\$5.33$).

### Step 2: Realistic Liquidation Realization Haircuts
Now apply realistic wind-down realization factors:
- Cash: $100\% \implies \$40.0\text{ million}$
- Accounts Receivable: $80\% \implies \$60.0\text{M} \times 0.80 = \$48.0\text{ million}$
- Inventory: $50\% \implies \$80.0\text{M} \times 0.50 = \$40.0\text{ million}$
- PP&E: $20\% \implies \$90.0\text{M} \times 0.20 = \$18.0\text{ million}$
- **Total Realizable Gross Assets**: $\$40.0\text{M} + \$48.0\text{M} + \$40.0\text{M} + \$18.0\text{M} = \$146.0\text{ million}$

Now satisfy claims and wind-down costs:
- Deduct Total Liabilities: $-\$100.0\text{ million}$ (paid $100\%$ in full)
- Deduct Estimated Closure & Severance Costs: $-\$8.0\text{ million}$
- **Net Realizable Liquidation Residual**:
  $$\text{Net Proceeds} = \$146.0\text{M} - \$100.0\text{M} - \$8.0\text{M} = \$38.0\text{ million}$$

Divide by $10.0\text{ million}$ shares:
$$\text{Adjusted Realization Value per Share} = \frac{\$38.0\text{M}}{10.0\text{M}} = \$3.80\text{ per share}$$

Notice the profound revelation! While raw unadjusted NCAV was $\$8.00$ per share, realistic asset realization yields only **$\$3.80$ per share**. An investor who bought at $\$6.20$ believing they had an unassailable $\$8.00$ asset floor would lose nearly $40\%$ of their capital in a real-world liquidation!

## Research discipline

When conducting asset realization and net-net research:
1. **Never Confuse NCAV with Working Capital**: If a data service displays "Working Capital per Share," verify whether long-term debt was subtracted. Always manually deduct total liabilities.
2. **Audit Off-Balance-Sheet Severance Obligations**: In Europe and Asia, statutory employee severance pay and union termination liabilities can easily consume $20\%$ to $40\%$ of a manufacturing firm's current assets in a shutdown.
3. **Verify Cash Accessibility**: Inspect whether the reported cash is held in restricted escrow, pledged to secure letters of credit, or trapped in foreign jurisdictions with currency repatriation restrictions.
4. **Demand an Operational Realization Clock**: If a company is burning $\$15\text{M}$ of cash per year in operating losses, a $\$30\text{M}$ net asset surplus will be completely evaporated within 24 months. Never buy a net-net without analyzing the cash burn rate.
""",
        r"\text{NCAV/share}=\frac{\text{CA}-\text{TL}-\text{Pref}}{N};\quad P_{\max}\le \frac{2}{3}\text{NCAV};\quad \text{Adjusted}=\frac{\sum (w_i A_i)-\text{TL}-\text{Costs}}{N}",
        'ca = 40 + 60 + 80\ntl = 100\nshares = 10\nncav_per_share = (ca - tl) / shares\ngraham_max_price = ncav_per_share * (2 / 3)\nprint("Unadjusted NCAV per share ($):", ncav_per_share)\nprint("Graham 2/3 maximum purchase price ($):", round(graham_max_price, 2))\nadj_assets = 40 * 1.0 + 60 * 0.80 + 80 * 0.50 + 90 * 0.20\nclosure_costs = 8\nadj_realization_share = (adj_assets - tl - closure_costs) / shares\nprint("Adjusted liquidation realization per share ($):", round(adj_realization_share, 2))',
        "An enterprise reports balance sheet cash of $20M, receivables of $40M, inventory of $50M, PP&E of $60M, and total liabilities of $45M, with $5M in preferred stock claims and 5 million common shares. Calculate unadjusted NCAV per share. Then calculate adjusted liquidation realization per share assuming 80% receivables recovery, 50% inventory recovery, 20% PP&E recovery, and $4M in closure costs.",
        "Total current assets = $20M (cash) + $40M (AR) + $50M (Inv) = $110M. Unadjusted NCAV = ($110M − $45M liabilities − $5M preferred) / 5M shares = $60M / 5M = $12.00 per share. Adjusted gross assets = $20M (cash) + $32M (AR at 80%) + $25M (Inv at 50%) + $12M (PP&E at 20%) = $89M. Net realization = $89M − $45M liabilities − $5M preferred − $4M closure costs = $35M. Adjusted realization per share is $35M / 5M shares = $7.00 per share.",
        [
            q(
                "A company has current assets of $120 million, total liabilities of $70 million, preferred stock claims of $10 million, and 4 million common shares. What is its NCAV per share?",
                ["$10.00", "$12.50", "$30.00"],
                0,
                "NCAV is ($120M − $70M − $10M) / 4M shares = $40M / 4M = $10.00 per share.",
            ),
            q(
                "What is the crucial difference between Net Current Asset Value (NCAV) and ordinary Working Capital?",
                [
                    "NCAV deducts total liabilities and preferred claims, whereas working capital deducts only current liabilities",
                    "NCAV includes goodwill and patents",
                    "Working capital is used only in Europe",
                ],
                0,
                "Working capital ignores long-term debt; NCAV deducts all liabilities and preferred claims to measure the residual for common equity.",
            ),
            q(
                "An asset liquidation pool has cash of $10 million, receivables of $20 million realized at 75%, inventory of $30 million realized at 50%, and total liabilities of $25 million. What net cash residual remains?",
                ["$35 million", "$20 million", "$15 million"],
                2,
                "Realized assets are $10M + $15M + $15M = $40M. Net residual after $25M liabilities is $40M − $25M = $15 million.",
            ),
        ],
    )

    add(
        "1.18",
        "VI",
        "Contingent liabilities and cash burn",
        "Stress an asset surplus for cash burn, closure costs, and claims omitted from a first-pass screen.",
        r"""
## The analytical question

An apparent balance sheet bargain is not a static museum exhibit; it is an active economic engine attached to a running clock.

When an analyst identifies a company trading at $\$15.00$ with an estimated net asset value of $\$25.00$, the fundamental question is:

$$\text{How long will it take for shareholders to realize that } \$25.00\text{, and how much cash will evaporate while waiting?}$$

Two destructive economic forces routinely destroy apparent asset discounts:
1. **Operating Cash Burn Rate**: If the business is operating at a loss, every month that passes drains cash out of the balance sheet. If a firm with a $\$20\text{M}$ asset surplus burns $\$1.0\text{M}$ per month in operating losses, the entire surplus will be completely extinguished in twenty months!
2. **Hidden and Contingent Off-Balance-Sheet Liabilities**: Balance sheets constructed under standard accounting conventions frequently omit or under-record massive contractual obligations:
   - **Operating Lease Commitments**: Undiscounted future lease commitments on vacant store locations.
   - **Defined Benefit Pension Deficits**: Actuarial underfunding of retired worker pensions.
   - **Environmental Remediation Liabilities**: Mandatory cleanup costs for contaminated industrial sites.
   - **Litigation and Warranty Claims**: Pending product liability lawsuits.

To account for both cash burn and the time value of money, the analyst must model the **Discounted Realization Equation**:

$$V_0 = \frac{A_{\text{net}} - \sum_{t=1}^T \text{Burn}_t - \text{Incremental Closure Costs}}{(1 + r)^T}$$

Where:
- $A_{\text{net}}$ is the initial net realizable asset surplus.
- $\text{Burn}_t$ is the operating cash deficit consumed in year $t$.
- $T$ is the expected time horizon (in years) required to achieve liquidation, sale, or restructuring.
- $r$ is the required hurdle discount rate reflecting realization risk (typically $10\%$ to $15\%$).

If management is hostile to shareholder interests, entrenched behind a staggered board, and determined to spend the asset surplus on speculative corporate acquisitions, the "catalyst probability" drops to near zero, and the asset surplus should be discounted to zero.

## A worked example

Let us evaluate a deep-value liquidation thesis for Alder Manufacturing:
- Initial Net Current Asset Surplus: $A_{\text{net}} = \$40.0\text{ million}$
- Fully diluted share count: $N = 10.0\text{ million shares}$
- Initial apparent surplus per share: $\$4.00\text{ per share}$
- Current Market Share Price: $P = \$2.20\text{ per share}$
- The stock appears to offer a tempting $45.0\%$ discount to net assets!

However, your forensic committee investigates the operational realization timeline:
1. **Realization Time Horizon**: Liquidating the specialized machinery and selling corporate warehouses under court supervision will take at least $T = 2.0\text{ years}$.
2. **Annual Cash Burn**: The loss-making core manufacturing division runs an ongoing cash operating deficit of $\$6.0\text{ million}$ per year:
   $$\text{Total 2-Year Cash Burn} = 2 \times \$6.0\text{M} = \$12.0\text{ million}$$
3. **Mandatory Severance and Plant Closure Costs**: Mandated statutory employee termination pay and plant decommissioning expenses total:
   $$\text{Incremental Closure Costs} = \$5.0\text{ million}$$
4. **Unrecorded Environmental Remediation**: Soil testing at Alder's fabrication site reveals chemical contamination requiring mandatory state cleanup:
   $$\text{Contingent Liability} = \$3.0\text{ million}$$

Let us compute the net residual value at the end of Year 2:

$$\text{Residual at Year 2} = \$40.0\text{M} - \$12.0\text{M (Burn)} - \$5.0\text{M (Closure)} - \$3.0\text{M (Environmental)} = \$20.0\text{ million}$$

Now discount that $\$20.0\text{ million}$ back to today at a $10.0\%$ annual discount rate to reflect two years of legal and commercial delay:

$$\text{Present Value of Net Residual: } V_0 = \frac{\$20.0\text{M}}{(1.10)^2} = \frac{\$20.0\text{M}}{1.21} \approx \$16.53\text{ million}$$

Divide across $10.0\text{ million}$ shares:
$$V_{\text{per share}} = \frac{\$16.53\text{M}}{10.0\text{M}} = \$1.65\text{ per share}$$

Look at the true economic outcome!
- Initial apparent asset value: $\$4.00$ per share.
- True present economic value: **$\$1.65$ per share**.
- Market quote: $\$2.20$ per share.

The stock was not a bargain at $\$2.20$! The apparent $45\%$ discount was an illusion created by ignoring cash burn, environmental liabilities, and the realization clock. At $\$2.20$, an investor is actually **overpaying** relative to the $\$1.65$ discounted realization value.

## Research discipline

When auditing liquidation and net asset theses:
1. **Establish the "Cash Runway Clock"**:
   $$\text{Cash Runway in Months} = \frac{\text{Accessible Cash Reserves}}{\text{Monthly Cash Burn}}$$
   If the runway is under 12 months and management has no credible financing bridge, the equity will likely be wiped out in an emergency restructuring.
2. **Scrutinize Footnote 8 (Commitments and Contingencies)**: Review all pending litigation, patent infringement claims, and long-term uncancelable purchase obligations.
3. **Audit Management Ownership and Governance Incentives**: Check the proxy statement (Schedule 14A). Do executives own significant personal stock, or do they receive lucrative salaries that incentivize them to keep burning cash indefinitely?
4. **Identify the Enforceable Legal Catalyst**: A discount alone never closes itself. Demand a specific catalyst: an activist proxy contest, a binding tender offer, a debt covenant maturity forcing a sale, or an announced voluntary liquidation plan.
""",
        r"V_0=\frac{A_{\text{net}}-\text{Burn}\times T-\text{Costs}}{(1+r)^T};\quad \text{Runway}=\frac{\text{Cash}}{\text{Monthly Burn}}",
        'surplus = 40\nburn_annual = 6\nyears = 2\nclosure = 5\nenvironmental = 3\nresidual_t2 = surplus - burn_annual * years - closure - environmental\nrate = 0.10\npv_residual = residual_t2 / (1 + rate) ** years\nshares = 10\nprint("Net residual at Year 2 ($M):", residual_t2)\nprint("Present value of residual ($M):", round(pv_residual, 2))\nprint("True per-share value ($):", round(pv_residual / shares, 2))',
        "An asset surplus of $30M is identified in a distressed company with 5 million shares. Management estimates it will take 3 years to sell the assets. During this time, the company will burn $4M of cash annually in operating losses, and will incur $6M in total environmental and severance closure costs. Calculate the residual proceeds at Year 3 and its present value at an 8% discount rate. Compute the resulting per-share value.",
        "Total 3-year cash burn is $4M × 3 = $12M. Residual proceeds at Year 3 = $30M − $12M (burn) − $6M (closure costs) = $12.0M. Present value at 8% discount rate is $12.0M / (1.08)³ = $12.0M / 1.2597 = $9.53M. Dividing by 5 million shares yields $9.53M / 5M = $1.91 per share.",
        [
            q(
                "A company with a balance sheet surplus of $25 million burns $3 million in cash annually for two years and incurs $4 million in plant closure costs. What net residual remains before discounting?",
                ["$15 million", "$18 million", "$21 million"],
                0,
                "Net residual is $25M − (2 × $3M) − $4M = $25M − $6M − $4M = $15 million.",
            ),
            q(
                "Before adding an estimate of unrecorded operating lease liabilities to a company's debt schedule, what must the analyst verify?",
                [
                    "Verify whether current lease accounting rules already capitalized the lease as a right-of-use liability, avoiding double counting",
                    "Assume leases never have legal enforceability",
                    "Deduct the lease payment three times for maximum conservatism",
                ],
                0,
                "Under modern accounting standards (IFRS 16 / ASC 842), many leases are already capitalized on the balance sheet; deducting them again creates an erroneous double count.",
            ),
            q(
                "A company has net realizable liquidation proceeds of $22 million expected to be distributed exactly two years from today. At a 10% annual discount rate, what is the present value of this distribution?",
                ["$18.18 million", "$20.00 million", "$26.62 million"],
                0,
                "Present value is $22M / (1.10)² = $22M / 1.21 = $18.18 million.",
            ),
        ],
    )

    add(
        "1.19",
        "VI",
        "Tangible book value and the goodwill illusion",
        "Explain why book value is neither a universal floor nor a complete account of business worth.",
        r"""
## The analytical question

Book value—the accounting net worth of common equity reported on the balance sheet—is one of the most widely cited metrics in financial media. Yet, Graham and Dodd warned that book value is subject to profound analytical hazards:

$$\text{Book value is neither an automatic floor in distress nor a reliable ceiling on prosperity.}$$

To understand book value, you must dissect how it is constructed:
- **Total Accounting Assets**: The sum of cash, receivables, inventories, land, factories, and intangible assets.
- **Intangible Assets and Goodwill**: When Company A acquires Company B for $\$500\text{ million}$, but B's identifiable physical assets are worth only $\$200\text{ million}$, Company A records the arbitrary $\$300\text{ million}$ premium as **Goodwill** on its own balance sheet!

Goodwill is not a physical asset that can be auctioned to pay debts. It is simply an accounting monument to a past acquisition premium. If the acquired subsidiary underperforms, the goodwill is economically worthless and will eventually be written off to zero.

Therefore, Graham and Dodd insisted that any asset-based evaluation must begin with **Tangible Book Value (TBV)**:

$$\text{Tangible Book Value} = \text{Total Assets} - \text{Total Liabilities} - \text{Goodwill} - \text{Identifiable Intangible Assets}$$

$$\text{TBV per Share} = \frac{\text{Tangible Equity}}{N_{\text{shares}}}$$

However, the analyst must navigate two opposite errors:
1. **The Fallacy of the Tangible Book Floor**: An industrial company with $\$20.00$ in tangible book value trading at $\$10.00$ is not automatically a safe investment! If its machinery is specialized to an obsolete product and the business runs persistent operating losses, those tangible assets will generate zero cash and the book value will be wiped out by recurring deficits.
2. **The Fallacy of the Asset-Light Blind Spot**: Exceptional modern franchise businesses (such as software platforms, brand consumer staples, or credit rating agencies) frequently require almost no physical tangible assets to generate massive profits. Their value is derived from customer network effects, brand loyalty, and proprietary code—intangible economic moats that rarely appear on a GAAP balance sheet.

## A worked example

Let us evaluate the balance sheet of Alder Manufacturing to isolate tangible equity from accounting goodwill.

Alder's balance sheet reports (in millions):
- Total Assets: $\$200.0\text{ million}$
  - Cash, Receivables, Inventory: $\$110.0\text{ million}$
  - Net Property, Plant & Equipment (PP&E): $\$40.0\text{ million}$
  - Goodwill (from acquiring a specialty metal stamper 3 years ago): $\$50.0\text{ million}$
- Total Liabilities: $\$120.0\text{ million}$
- Common shares outstanding: $10.0\text{ million shares}$

Let us calculate the metrics:
1. Reported Accounting Book Equity:
   $$\text{Book Equity} = \text{Total Assets} - \text{Total Liabilities} = \$200.0\text{M} - \$120.0\text{M} = \$80.0\text{ million}$$
   $$\text{Book Value per Share} = \frac{\$80.0\text{M}}{10.0\text{M}} = \$8.00\text{ per share}$$
2. Tangible Book Equity:
   Strip out the $\$50.0\text{ million}$ of accounting goodwill:
   $$\text{Tangible Equity} = \$80.0\text{M} - \$50.0\text{M (Goodwill)} = \$30.0\text{ million}$$
   $$\text{Tangible Book Value per Share} = \frac{\$30.0\text{M}}{10.0\text{M}} = \$3.00\text{ per share}$$

Now evaluate the economic reality:
Suppose Alder's shares trade at $P = \$5.00$:
- An unsophisticated investor exclaims: *"Alder trades at only $0.625\times$ book value ($\$5.00 / \$8.00$), offering a $37.5\%$ discount to assets!"*
- The forensic analyst responds: *"Alder actually trades at $1.67\times$ tangible book value ($\$5.00 / \$3.00$). The apparent discount was manufactured by $\$50.0\text{M}$ of goodwill from an acquisition whose operating earnings have dropped by $60\%$."*

If the auditor performs the mandatory annual impairment test and writes off the $\$50.0\text{M}$ goodwill, reported book value will immediately collapse from $\$8.00$ to $\$3.00$ overnight!

## Research discipline

When evaluating book value and intangible assets:
1. **Deduct All Goodwill and Unidentifiable Intangibles**: Always calculate tangible book value as your primary baseline.
2. **Audit Return on Tangible Assets (ROTA)**:
   $$\text{ROTA} = \frac{\text{Normalized Operating EBIT}}{\text{Tangible Operating Assets}}$$
   If ROTA is below the company's cost of capital ($< 8\%$), the tangible assets are unproductive and do not support their carrying values.
3. **Check for Unrecorded Economic Intangibles**: If a company earns a sustained $30\%$ return on tangible equity without leverage, recognize that the enterprise possesses powerful unrecorded economic franchise value (moats) that make book value irrelevant as a ceiling.
4. **Inspect the Goodwill Impairment Disclosures**: Review Footnote 7 (Intangibles). Check the reporting unit discount rates and terminal growth assumptions used by management to justify not writing down goodwill. If those assumptions are unrealistic, model an immediate impairment.
""",
        r"\text{TBV}=\text{Assets}-\text{Liabilities}-\text{Goodwill};\quad \text{TBV/share}=\frac{\text{TBV}}{N};\quad \text{ROTA}=\frac{\text{EBIT}}{\text{Tangible Assets}}",
        'assets = 200\ngoodwill = 50\nliabilities = 120\nshares = 10\nbook_equity = assets - liabilities\ntangible_equity = book_equity - goodwill\nprint("Reported book equity ($M):", book_equity)\nprint("Tangible book equity ($M):", tangible_equity)\nprint("Reported book value per share ($):", book_equity / shares)\nprint("Tangible book value per share ($):", tangible_equity / shares)',
        "An enterprise reports total assets of $150M, which includes $35M in goodwill and $10M in capitalized software intangibles. Total liabilities are $90M, and there are 5 million shares outstanding. Calculate reported book equity per share and tangible book equity per share. State why neither number necessarily equals intrinsic business value.",
        "Reported book equity is $150M − $90M = $60M, or $12.00 per share ($60M / 5M). Tangible book equity strips out goodwill and software intangibles: $60M − $35M − $10M = $15M, or $3.00 per share ($15M / 5M). Neither figure equals intrinsic value because: (1) tangible book value ignores the company's future earning power, competitive moats, and customer franchise; while (2) in distress, tangible assets may realize far less than book value due to liquidation haircuts and asset obsolescence.",
        [
            q(
                "A corporation reports total assets of $100 million, total liabilities of $60 million, and goodwill of $15 million. What is its tangible common equity?",
                ["$25 million", "$40 million", "$55 million"],
                0,
                "Book equity is $100M − $60M = $40M. Tangible equity is $40M − $15M = $25 million.",
            ),
            q(
                "Which statement regarding corporate book value is methodologically sound?",
                [
                    "Book value guarantees the minimum cash proceeds an investor will receive in a corporate sale",
                    "Book value is an accounting record of historical capital supplied and allocations made; its economic relevance depends on asset productivity, earning power, and realization conditions",
                    "Book value captures all customer brand loyalty and internal software developments with exact precision",
                ],
                1,
                "Carrying values reflect historical accounting conventions and must be interpreted through economic earning power and asset realizability.",
            ),
            q(
                "A manufacturing firm trades at a 50% discount to its reported tangible book value, but its factories produce persistent operating losses and its machinery is technologically obsolete. What is the correct analytical conclusion?",
                [
                    "The 50% discount guarantees an unassailable margin of safety",
                    "Ongoing operating losses and asset obsolescence can completely destroy the apparent tangible asset floor",
                    "Earnings can be ignored because tangible assets always recover at par",
                ],
                1,
                "If assets cannot generate operating profits, their liquidation value is often negligible and ongoing losses will consume balance sheet equity.",
            ),
        ],
    )

    # -------------------------------------------------------------------------
    # PART VII: COMPARISON AND THE INVESTMENT DECISION
    # -------------------------------------------------------------------------

    add(
        "1.20",
        "VII",
        "Cross-company comparison and multiples",
        "Construct a peer comparison with matching claims, normalized earnings, and accounting assumptions.",
        r"""
## The analytical question

Valuation multiples—such as Price-to-Earnings ($P/E$) or Enterprise Value to EBITDA ($EV/\text{EBITDA}$)—are widely used shortcuts in equity research. However, Graham and Dodd warned that a multiple is not an independent valuation proof:

$$\text{A valuation multiple is simply a compressed shorthand for a complex set of underlying economic assumptions.}$$

The most frequent error in comparative analysis is the **mismatch of claims and cash flows**:
- **Price-to-Earnings ($P/E$)**: Divides the market value of *common equity* by net income belonging to *common shareholders*.
- **Enterprise Value to Operating Earnings ($EV/\text{EBIT}$)**: Divides the market value of *all capital providers* (equity + debt) by operating earnings generated *before debt payments*.

Mixing enterprise claims with equity earnings (e.g., Enterprise Value divided by Net Income, or Market Cap divided by Operating EBIT) produces complete financial nonsense.

To compare companies on consistent terms, the analyst must compute **Enterprise Value (EV)**:

$$EV = \text{Market Cap of Equity} + \text{Total Interest-Bearing Debt} + \text{Preferred Equity} - \text{Excess Nonoperating Cash}$$

$$\text{Enterprise Multiple} = \frac{EV}{\text{Normalized EBIT}}$$

Why is $EV/\text{EBIT}$ superior to $P/E$ when comparing industry competitors?
Because $P/E$ is violently distorted by **capital structure leverage**:
- Company A and Company B may own identical factories generating identical $\$20\text{M}$ operating profit.
- If Company A is funded $100\%$ with equity, its net income is high.
- If Company B is funded with $80\%$ debt, its net income is small because of massive interest deductions.
- An analyst looking only at $P/E$ will conclude Company B is far more expensive or erratic, when in reality both businesses possess identical underlying commercial earning power!

Furthermore, never compare raw reported multiples without **normalizing earnings**:
- A low $P/E$ multiple of $6.0\times$ at the cyclical peak of a commodity boom is often dangerously expensive, because peak earnings are about to collapse.
- A high $P/E$ multiple of $20.0\times$ at the trough of a recession can be extraordinarily cheap, because depressed earnings are about to rebound.

## A worked example

Let us evaluate and compare two industrial valve competitors: Alder Manufacturing and Peer Corp. Both operate in the same market sector and generate identical normalized operating earnings:

$$\text{Normalized EBIT} = \$20.0\text{ million for both firms}$$

Let us audit their capital structures and enterprise values (in millions):

| Metric | Alder Manufacturing | Peer Corp |
| :--- | :--- | :--- |
| **Market Value of Common Equity** | $\$120.0\text{ million}$ | $\$150.0\text{ million}$ |
| **Total Debt** | $\$60.0\text{ million}$ | $\$10.0\text{ million}$ |
| **Balance Sheet Cash** | $\$30.0\text{ million}$ | $\$10.0\text{ million}$ |
| **Operating Cash Required** | $\$10.0\text{ million}$ | $\$10.0\text{ million}$ |
| **Excess Nonoperating Cash** | $\$20.0\text{ million}$ | $\$0.00$ |

Let us calculate Enterprise Value:
1. Alder Manufacturing:
   $$EV_{\text{Alder}} = \$120.0\text{M (Equity)} + \$60.0\text{M (Debt)} - \$20.0\text{M (Excess Cash)} = \$160.0\text{ million}$$
   $$\text{EV / Normalized EBIT} = \frac{\$160.0\text{M}}{\$20.0\text{M}} = 8.0\times$$
2. Peer Corp:
   $$EV_{\text{Peer}} = \$150.0\text{M (Equity)} + \$10.0\text{M (Debt)} - \$0.0\text{M (Excess Cash)} = \$160.0\text{ million}$$
   $$\text{EV / Normalized EBIT} = \frac{\$160.0\text{M}}{\$20.0\text{M}} = 8.0\times$$

Notice the critical insight:
Both companies trade at the **exact same enterprise multiple of $8.0\times$ EBIT**!
However, consider the **financial risk profile**:
- Alder carries $\$60.0\text{M}$ in debt against $\$120.0\text{M}$ of equity ($\text{Debt/Equity} = 50\%$).
- Peer carries only $\$10.0\text{M}$ in debt against $\$150.0\text{M}$ of equity ($\text{Debt/Equity} = 6.7\%$).

If industry operating margins contract and operating enterprise value drops by $\$40.0\text{ million}$ for both companies:
- Peer's equity drops from $\$150\text{M}$ to $\$110\text{M}$ (a $26.7\%$ decline).
- Alder's equity drops from $\$120\text{M}$ to $\$80\text{M}$ (a $33.3\%$ decline).

Alder's higher debt leverage magnifies downside volatility for its common shareholders. Even though their enterprise multiples are identical, Alder requires a higher required return to compensate for financial leverage.

## Research discipline

When conducting peer comparisons:
1. **Never Mix Enterprise and Equity Metrics**: Always pair equity price with net income or book value per share, and enterprise value with EBIT, EBITDA, or unlevered cash flows.
2. **Audit Accounting Differences Across Peers**:
   - Inventory method (FIFO vs LIFO).
   - Depreciation life schedules (e.g., 10-year life vs 20-year life).
   - Lease capitalization and capitalized R&D vs expensed R&D.
3. **Beware the "Industry Average" Multiple Trap**: If every company in an overhyped bubble sector trades at $40\times$ earnings, buying a peer at $30\times$ is not a value investment; it is merely buying an overvalued asset at a slightly lower overvaluation.
4. **Compare Multiples to Normalized (Mid-Cycle) Denominators**: Always divide current price by 5-to-10 year normalized earnings, never unadjusted trailing 12-month peak earnings.
""",
        r"EV=\text{Equity MktCap}+\text{Debt}-\text{Excess Cash};\quad \text{Multiple}=\frac{EV}{\text{EBIT}_{\text{norm}}}",
        'equity_alder = 120\ndebt_alder = 60\nexcess_cash_alder = 20\nev_alder = equity_alder + debt_alder - excess_cash_alder\nebit_norm = 20\nprint("Alder Enterprise Value ($M):", ev_alder)\nprint("Alder EV / EBIT:", ev_alder / ebit_norm)\nequity_peer = 150\ndebt_peer = 10\nexcess_cash_peer = 0\nev_peer = equity_peer + debt_peer - excess_cash_peer\nprint("Peer Enterprise Value ($M):", ev_peer)\nprint("Peer EV / EBIT:", ev_peer / ebit_norm)',
        "Company A has common equity market value of $90M, debt of $40M, excess cash of $10M, and normalized EBIT of $15M. Company B has equity market value of $100M, debt of $20M, zero excess cash, and normalized EBIT of $12M. Calculate EV/EBIT for both firms. State two reasons why Company A's lower multiple might not make it the superior investment.",
        "For Company A: EV = $90M + $40M − $10M = $120M. EV/EBIT = $120M / $15M = 8.0x. For Company B: EV = $100M + $20M − $0M = $120M. EV/EBIT = $120M / $12M = 10.0x. Company A's lower multiple (8.0x vs 10.0x) does not automatically make it superior because: (1) Company A carries twice the debt of Company B ($40M vs $20M), exposing common equity to greater financial distress risk; and (2) Company A may suffer from higher customer concentration, obsolete plant equipment, or lower return on capital.",
        [
            q(
                "A corporation has common equity market value of $80 million, debt of $30 million, and excess nonoperating cash of $10 million. What is its Enterprise Value (EV)?",
                ["$60 million", "$100 million", "$120 million"],
                1,
                "EV = $80M (equity) + $30M (debt) − $10M (excess cash) = $100 million.",
            ),
            q(
                "Which valuation pairing is methodologically consistent across claims and cash flows?",
                [
                    "Enterprise Value divided by Common Net Income",
                    "Common Share Price divided by Earnings Per Share (P/E)",
                    "Common Share Price divided by Total Corporate Revenue",
                ],
                1,
                "Share price and EPS both refer strictly to the residual common equity claim, maintaining methodological consistency.",
            ),
            q(
                "A company has Enterprise Value of $180 million. In a peak boom year, EBIT reaches $30 million, but normalized mid-cycle EBIT is only $18 million. What is its normalized EV/EBIT multiple?",
                ["6.0 times", "10.0 times", "12.0 times"],
                1,
                "Normalized EV/EBIT is $180M / $18M = 10.0 times. Using peak earnings ($30M) creates an artificial 6.0x multiple that misrepresents mid-cycle valuation.",
            ),
        ],
    )

    add(
        "1.21",
        "VII",
        "Special situations and contingent outcomes",
        "Analyze a price discrepancy using completion, failure, timing, and funding scenarios.",
        r"""
## The analytical question

Beyond standard going-concern equities and corporate bonds, Graham and Dodd devoted extensive study to **Special Situations** (or "workouts"):
- Merger and acquisition arbitrage (cash tender offers).
- Corporate spin-offs and split-offs.
- Liquidations and court-supervised reorganizations.
- Contingent litigation settlements and asset tenders.

In a special situation, the investment thesis does not depend on the broad economic cycle or general stock market fluctuations. Instead, it depends on a **specific, verifiable corporate event** that will convert the security into cash or a higher-value claim at a specified future date.

Consider a classic cash merger arbitrage transaction:
- An acquirer announces a binding contract to purchase Target Company for $V_{\text{success}} = \$50.00$ per share in cash.
- The target stock currently trades in the market at $P = \$45.00$ per share.
- The $\$5.00$ difference ($11.1\%$ spread) exists because the market perceives a risk that the deal may fail to close (due to regulatory antitrust challenges, shareholder votes, or financing failure).
- If the merger collapses, the stock will fall back to its standalone unaffected value: $V_{\text{failure}} = \$32.00$.

Notice the asymmetric risk profile:
- On success: Gain $\$50.00 - \$45.00 = +\$5.00$ per share.
- On failure: Lose $\$45.00 - \$32.00 = -\$13.00$ per share!

Because the downside loss on failure is typically several times larger than the upside gain, an analyst must never evaluate an arbitrage spread as "free money." You must solve for the **Break-Even Completion Probability ($p^*$)**:

$$E[\text{Payoff}] = p \times V_{\text{success}} + (1 - p) \times V_{\text{failure}} = P$$

Solving for $p^*$:

$$p^* = \frac{P - V_{\text{failure}}}{V_{\text{success}} - V_{\text{failure}}}$$

If the actual objective probability of completion ($p$) exceeds $p^*$, the expected mathematical value of the transaction is positive:

$$E[\text{Gain}] = p \times (V_{\text{success}} - P) - (1 - p) \times (P - V_{\text{failure}})$$

Furthermore, an analyst must factor in the **time horizon and financing carry costs**:
If a $\$5.00$ gain takes eighteen months of antitrust litigation to close, the annualized rate of return drops significantly, and capital is locked up during an extended period of uncertainty.

## A worked example

Let us evaluate an invented special situation involving Alder Manufacturing's subsidiary, Alder Precision Instruments. An industrial conglomerate announces a definitive cash tender offer to acquire Alder Precision:
- Offer Price: $V_{\text{success}} = \$50.00\text{ per share in cash}$
- Current Market Quote: $P = \$45.00\text{ per share}$
- Unaffected Standalone Value (if deal fails): $V_{\text{failure}} = \$32.00\text{ per share}$
- Expected closing timeline: Exactly $6\text{ months}$ ($0.5\text{ years}$).

Let us calculate the analytical metrics:
1. Payoff on Success:
   $$\text{Gain}_{\text{success}} = \$50.00 - \$45.00 = +\$5.00\text{ per share } (+11.1\%)$$
2. Loss on Failure:
   $$\text{Loss}_{\text{failure}} = \$45.00 - \$32.00 = -\$13.00\text{ per share } (-28.9\%)$$
3. Calculate the Break-Even Completion Probability:
   $$p^* = \frac{P - V_{\text{failure}}}{V_{\text{success}} - V_{\text{failure}}} = \frac{\$45.00 - \$32.00}{\$50.00 - \$32.00} = \frac{\$13.00}{\$18.00} \approx 72.22\%$$
   To justify investing capital, the analyst must have documented, verifiable evidence that the probability of regulatory clearance and shareholder approval exceeds $72.22\%$.

Suppose your legal and regulatory antitrust audit concludes that the objective probability of deal closure is **$80.0\%$** ($p = 0.80$):
1. Expected Terminal Proceeds:
   $$E[\text{Proceeds}] = 0.80 \times \$50.00 + 0.20 \times \$32.00 = \$40.00 + \$6.40 = \$46.40$$
2. Expected Net Profit per Share:
   $$E[\text{Profit}] = \$46.40 - \$45.00 = +\$1.40\text{ per share}$$
3. Expected Percentage Return over 6 Months:
   $$\text{Return}_{\text{6-month}} = \frac{\$1.40}{\$45.00} = 3.11\%$$
   Annualized Return $\approx 3.11\% \times 2 = 6.22\%$.

Notice the disciplined decision:
Although the expected profit is positive ($+\$1.40$), the annualized return is only $6.22\%$. If 6-month risk-free Treasury bills yield $5.50\%$, an investor is accepting the risk of losing $\$13.00$ per share on deal failure for an incremental premium of only $0.72\%$ above cash! A disciplined investment committee rejects this trade despite the positive expected value.

## Research discipline

When evaluating special situations:
1. **Audit the Merger Agreement (SEC Form 8-K)**: Scrutinize the "Material Adverse Effect" (MAE) clause, regulatory clearance covenants, financing conditions, and termination break fees.
2. **Stress-Test Standalone Downside ($V_{\text{failure}}$)**: Never assume the stock will only fall back to its pre-announcement price. If the broader market has fallen during the interim, or if the failed deal reveals accounting problems inside the target, $V_{\text{failure}}$ can be far lower than pre-deal levels.
3. **Set Up a Milestone Tracking Matrix**: Track specific legal milestones (e.g., Hart-Scott-Rodino waiting period expiration, European Commission Phase II antitrust review, shareholder proxy vote).
4. **Enforce Strict Portfolio Sizing Limits**: Never allocate more than $3\%$ to $5\%$ of portfolio capital to any single merger arbitrage trade. When deals break, the stock collapses in minutes.
""",
        r"p^*=\frac{P-V_{\text{failure}}}{V_{\text{success}}-V_{\text{failure}}};\quad E[\text{Proceeds}]=p V_{\text{success}}+(1-p)V_{\text{failure}}",
        'p_target = 45\nv_success = 50\nv_failure = 32\np_breakeven = (p_target - v_failure) / (v_success - v_failure)\nprint("Break-even probability (%):", round(p_breakeven * 100, 2))\np_assumed = 0.80\nexpected_proceeds = p_assumed * v_success + (1 - p_assumed) * v_failure\nprint("Expected proceeds ($):", round(expected_proceeds, 2))\nprint("Expected profit per share ($):", round(expected_proceeds - p_target, 2))',
        "A corporate transaction offers a cash payout of $35.00 upon successful completion. If the transaction collapses, the stock is estimated to fall to $15.00. The current market price is $28.00. Calculate the break-even probability of completion. Then calculate expected proceeds and net profit if an analyst assumes a 70% probability of success.",
        "Break-even probability is ($28.00 − $15.00) / ($35.00 − $15.00) = $13.00 / $20.00 = 65.0%. At an assumed 70% probability of success: Expected proceeds = (0.70 × $35.00) + (0.30 × $15.00) = $24.50 + $4.50 = $29.00. Expected net profit per share is $29.00 − $28.00 = $1.00 per share. Notice that failure loses $13.00, while success gains only $7.00.",
        [
            q(
                "A special situation pays $40.00 on success and falls to $20.00 on failure. The current market quotation is $30.00. What is the break-even completion probability before costs?",
                ["25%", "50%", "75%"],
                1,
                "Break-even probability is ($30 − $20) / ($40 − $20) = $10 / $20 = 50.0%.",
            ),
            q(
                "What does a positive mathematical expected value ($E[V] > P$) establish in a contingent arbitrage event?",
                [
                    "It guarantees that the investor cannot lose money on the trade",
                    "It establishes an assumption-dependent statistical average, while the severe adverse downside outcome remains fully possible",
                    "It requires the fund manager to invest 100% of portfolio capital into the deal",
                ],
                1,
                "A positive expected value does not eliminate downside risk; a broken deal can still impose catastrophic losses on the specific holding.",
            ),
            q(
                "A contingent claim costs $24.00, pays $30.00 upon successful closing, and realizes $10.00 upon failure. At an assumed 60% probability of success, what are the expected proceeds?",
                ["$22.00", "$24.00", "$26.00"],
                0,
                "Expected proceeds are (0.60 × $30) + (0.40 × $10) = $18 + $4 = $22.00, which is below the $24.00 purchase price.",
            ),
        ],
    )

    add(
        "1.22",
        "VII",
        "Portfolio concentration and review discipline",
        "Write an investment memo with an opposing case, price discipline, and explicit review triggers.",
        r"""
## The analytical question

The culmination of security analysis is not an academic research paper; it is a **binding, revisable investment committee decision**.

A complete investment decision synthesizes four interconnected elements:
1. **The Core Thesis and Claim Rank**: The precise security purchased, its priority in liquidation, its conservative valuation range, and the required margin of safety.
2. **The Strongest Opposing Bear Case**: An authentic, steel-manned presentation of why the investment could fail. If the analyst cannot state the bear argument better than the bears themselves, the research is incomplete.
3. **Position Sizing and Scenario Risk Budgeting**: Ensuring that an adverse outcome on this individual position cannot permanently impair the overall fund:
   $$\text{Scenario Portfolio Loss} = w_i \times L_i$$
   Where $w_i$ is the portfolio weight of the position (e.g., $5.0\%$), and $L_i$ is the percentage loss in a severe stress scenario (e.g., $40.0\%$).
   $$\text{Portfolio Drawdown} = 0.05 \times 0.40 = 0.02 = 2.0\%$$
4. **Pre-Registered Review Triggers**: Clear, falsifiable conditions defined *before* purchase that mandate an immediate committee review or forced exit.

A critical habit of professional investors is separating **Business Review Triggers** from **Price Review Triggers**:
- **Business Review Triggers**: Relate to the *operating economics* of the firm (e.g., loss of a customer representing $> 25\%$ of revenues, breach of debt covenants, departure of key operational management, or two consecutive quarters of negative operating cash flow). These triggers require updating intrinsic value ($V$).
- **Price Review Triggers**: Relate strictly to the *market quotation* ($P$) relative to intrinsic value (e.g., price reaches full intrinsic value, prompting a harvest of capital, or price drops below a stop-loss threshold requiring an audit of thesis invalidation).

Never adjust your valuation estimate higher simply because the market price has risen, and never average down into a falling stock without verifying that the business value remains unimpaired!

## A worked example

Let us review the investment memo prepared by an analyst recommending a commitment to Alder Manufacturing:
- Estimated Weak-Case Intrinsic Value: $V_{\text{weak}} = \$40.00\text{ per share}$
- Required Margin of Safety: $M_{\text{required}} = 30.0\%$
- Maximum Allowable Purchase Price:
  $$P_{\max} = \$40.00 \times (1 - 0.30) = \$28.00\text{ per share}$$
- Current Market Quotation: $P = \$26.00\text{ per share}$

The numerical decision rule is satisfied ($P = \$26.00 \le \$28.00$).

Now review the risk budget and opposing thesis:
1. **The Opposing Bear Case**:
   - Primary customer (Northern Rail) accounts for $35\%$ of Alder's equipment revenue. Northern Rail's contract expires in eighteen months.
   - Alder faces a $\$25.0\text{ million}$ bank loan maturity in Year 2 requiring refinancing.
2. **Portfolio Sizing**:
   - The analyst proposes allocating $w = 5.0\%$ of total fund capital.
   - In a stress scenario where Northern Rail terminates its contract and Alder refinances at punitive interest rates, the stock is estimated to fall by $L = 40.0\%$ to $\$15.60$.
   - The impact on total fund capital is:
     $$\text{Fund Scenario Loss} = 0.05 \times 0.40 = 2.0\%$$
   The portfolio manager confirms that a $2.0\%$ drawdown is within the fund's risk tolerance.
3. **Pre-Registered Falsification Triggers**:
   - **Trigger 1 (Business Exit)**: If Northern Rail issues an RFP without naming Alder as preferred bidder, liquidate the position immediately regardless of share price.
   - **Trigger 2 (Valuation Exit)**: If the market quotation reaches $\$40.00$ (full conservative intrinsic value), sell the position to realize capital.

## Research discipline

To construct an institutional-grade investment memo:
1. **Write the Decision on One Page**: An investment thesis that requires thirty pages of convoluted justifications is often masking unacknowledged uncertainty. Summarize claim, value, margin of safety, and risks concisely.
2. **Pre-Commit to Exit Rules Before Capital Allocation**: Human emotions (fear, greed, anchoring bias) compromise judgment when prices plunge. Write down exit rules when calm and objective.
3. **Preserve the Unaltered Original Memo in the Audit File**: When conducting a post-mortem review three years later, compare actual developments against the original written memo, not against reconstructed memories.
4. **Remember That 'Pass' is a Valid Conclusion**: You do not have to own every stock or make an investment in every researched company. The power of a value investor lies in the ability to wait patiently for rare pitches where price, value, and safety align perfectly.
""",
        r"P_{\max}=V_{\text{weak}}(1-M_{\text{required}});\quad \text{Portfolio Loss}=w_i \times L_i",
        'value_weak = 40\nm_required = 0.30\np_max = value_weak * (1 - m_required)\nquote = 26\nprint("Maximum permitted price ($):", p_max)\nprint("Quote meets rule:", quote <= p_max)\npos_weight = 0.05\nstress_loss = 0.40\nportfolio_drawdown = pos_weight * stress_loss\nprint("Scenario portfolio drawdown (%):", round(portfolio_drawdown * 100, 2))',
        "Prepare an investment decision for a common equity with weak-case value of $50.00, a current market price of $32.00, and a required 35% margin of safety. If approved, the position will be sized at 6% of the portfolio, exposed to an estimated 50% stress-loss scenario. Calculate the maximum purchase price, test whether the quote qualifies, calculate portfolio drawdown, and formulate one business review trigger.",
        "Maximum purchase price is $50.00 × (1 − 0.35) = $32.50. At a market quote of $32.00, the stock meets the numerical rule ($32.00 ≤ $32.50). Scenario portfolio drawdown is 0.06 × 0.50 = 0.03 (3.0% of fund capital). A valid business review trigger: 'If quarterly operating cash flow falls below zero for two consecutive quarters, or if the company's interest coverage drops below 2.5x, halt all purchases and execute an emergency committee thesis re-evaluation.'",
        [
            q(
                "A 4% portfolio position suffers a 50% loss in an adverse scenario, while all other holdings remain unchanged. What is the impact on total portfolio value?",
                ["2.0% loss", "4.0% loss", "50.0% loss"],
                0,
                "Portfolio drawdown is 0.04 × 0.50 = 0.02 = 2.0% of total fund capital.",
            ),
            q(
                "Which event represents a genuine business-value review trigger rather than a mere market price fluctuation?",
                [
                    "A financial TV commentator downgrades the stock",
                    "The loss of the primary customer who accounts for 40% of the firm's normalized operating profits",
                    "The stock price crosses an arbitrary round number",
                ],
                1,
                "Losing the primary customer directly impairs the operating earning power that supports intrinsic value.",
            ),
            q(
                "A researcher estimates weak-case value at $60.00 and requires a 40% margin of safety. The market quote is $38.00. What is the investment decision?",
                [
                    "Purchase because the market price is below $60.00",
                    "Reject because the maximum permitted purchase price is $36.00, which $38.00 exceeds",
                    "Purchase because the stock is likely to double",
                ],
                1,
                "Maximum price is $60.00 × (1 − 0.40) = $36.00. The market quote of $38.00 violates the required margin of safety.",
            ),
        ],
    )

# -------------------------------------------------------------------------
    # PART VIII: MODERN BRIDGES AND CAPSTONE
    # -------------------------------------------------------------------------

    add(
        "1.5",
        "VIII",
        "The Graham growth heuristic: a separate extension",
        "Audit the units and sensitivity of a later growth heuristic without treating it as the 1940 book's valuation method.",
        r"""
## The analytical question

In his later 1962 and 1974 writings, Benjamin Graham introduced a popular mathematical shorthand intended to approximate the intrinsic value of growing common stocks without constructing complex twenty-year financial models. This expression is widely known as the **Graham Growth Formula**:

$$V = \text{EPS} \times (8.5 + 2g) \times \frac{4.4}{Y}$$

Where:
- $\text{EPS}$ is normalized trailing or current earnings per share.
- $8.5$ represents the baseline Price-to-Earnings ($P/E$) multiplier for a mature, zero-growth company ($g = 0$).
- $g$ is the expected annual earnings growth rate over the next 7 to 10 years, **expressed as a percentage point** (e.g., enter $5$ for $5.0\%$, not $0.05$).
- $4.4$ represents the historical yield on high-grade AAA corporate bonds in 1962 when the baseline formula was established.
- $Y$ is the current market yield on AAA corporate bonds, **expressed as a percentage point** (e.g., enter $6.0$ for $6.0\%$, not $0.06$).

The course creators and modern analysts emphasize a critical historical and methodological distinction:

$$\text{This heuristic is not presented as a method from the 1940 text.}$$

In the 1940 edition of *Security Analysis*, Graham and Dodd were deeply suspicious of capitalizing speculative long-term growth forecasts. They emphasized balance sheet assets, tangible liquidation recovery, and historical cycle earnings coverage. This 1974 heuristic is a much later rule of thumb with severe economic limitations:
1. **Extreme Sensitivity to Small Inputs**: Because growth ($g$) is multiplied by $2$ and then scaled by corporate bond yields ($4.4 / Y$), a tiny modification in an assumed growth rate or a 100-basis-point shift in interest rates swings the valuation by $40\%$ to $60\%$.
2. **Absence of Capital Reinvestment Modeling**: The formula assumes growth occurs magically without requiring cash reinvestment! In real businesses, achieving $10\%$ annual growth often requires massive capital expenditures, increasing debt, or working capital absorption that starves owners of cash.
3. **No Terminal Value or Competitive Fade**: The formula does not model competitive entry or the erosion of economic moats.

## A worked example

Let us audit the mathematical sensitivity of the Graham growth heuristic for Alder Manufacturing:
- Current Normalized EPS: $\text{EPS} = \$4.00$
- Expected Growth Rate: $g = 5.0\%\text{ per year}$ (entered as $g = 5$)
- Baseline Corporate Bond Yield: $Y = 4.4\%$ (entered as $Y = 4.4$)

Let us compute baseline value:
$$V_{\text{baseline}} = \$4.00 \times (8.5 + 2 \times 5) \times \frac{4.4}{4.4} = \$4.00 \times (8.5 + 10) \times 1.0 = \$4.00 \times 18.5 = \$74.00\text{ per share}$$

Now observe the violent sensitivity when economic conditions change:

### Sensitivity 1: Interest Rate Spike ($Y$ rises from $4.4\%$ to $6.0\%$)
Suppose inflationary pressures drive high-grade corporate bond yields up to $Y = 6.0\%$:
$$V_{\text{rates}} = \$4.00 \times 18.5 \times \frac{4.4}{6.0} = \$74.00 \times 0.7333 = \$54.27\text{ per share}$$
Without any change in the company's internal operations or sales volume, intrinsic value dropped by **$\$19.73$ per share ($-26.7\%$)** purely due to the external interest rate denominator!

### Sensitivity 2: Optimistic Growth Revision ($g$ raised from $5\%$ to $10\%$)
Now hold yield constant at $Y = 4.4$, but assume an enthusiastic equity analyst raises expected growth to $g = 10$:
$$V_{\text{growth}} = \$4.00 \times (8.5 + 2 \times 10) \times 1.0 = \$4.00 \times 28.5 = \$114.00\text{ per share}$$
Value surges by **$\$40.00$ per share ($+54.1\%$)** based entirely on a speculative multi-year growth assumption!

### Sensitivity 3: Earnings Normalization Error ($\text{EPS}$ is $\$3.00$ instead of $\$4.00$)
If normalized sustainable earnings are actually $\$3.00$ rather than $\$4.00$, baseline value drops from $\$74.00$ to $\$55.50$ (an instant $25\%$ decline across all scenarios).

## Research discipline

When evaluating growth formulas and heuristics:
1. **Audit Input Units with Extreme Care**: Confirm whether the model expects percentage points ($5$ and $4.4$) or decimals ($0.05$ and $0.044$). Entering $0.05$ for $g$ collapses the multiplier from $18.5$ to $8.6$, invalidating the calculation.
2. **Never Use Growth Heuristics as a Primary Purchase Justification**: Use this formula exclusively as a reverse-engineering sensitivity tool:
   $$g_{\text{implied}} = \frac{\frac{P \times Y}{\text{EPS} \times 4.4} - 8.5}{2}$$
   Ask: *"What growth rate is the current market quotation already pricing in?"* If the market prices in $12\%$ growth for a cyclical steel manufacturer, the stock is dangerously overvalued.
3. **Compare Against Asset Realization and Normalized Earning Power**: If the growth heuristic produces $\$74.00$, but tangible book value is $\$15.00$ and liquidation recovery is $\$8.00$, recognize that $\$59.00$ ($80\%$) of the heuristic value consists of capitalized hopes for future growth.
4. **Demand Proof of Capital Discipline**: If management claims it will grow earnings by $10\%$ annually, inspect whether historical Return on Invested Capital (ROIC) exceeds the cost of capital. Growth in a low-return business destroys value.
""",
        r"V=\text{EPS}\times(8.5+2g)\times\frac{4.4}{Y};\quad g_{\text{implied}}=\frac{\frac{P\times Y}{\text{EPS}\times 4.4}-8.5}{2}",
        'eps = 4.0\ngrowth = 5.0\nfor y in [4.4, 6.0]:\n    val = eps * (8.5 + 2 * growth) * (4.4 / y)\n    print(f"Yield Y = {y}% -> Heuristic Value: ${round(val, 2)}")\ngrowth_high = 10.0\nval_high = eps * (8.5 + 2 * growth_high) * (4.4 / 4.4)\nprint(f"Growth g = 10% -> Heuristic Value: ${round(val_high, 2)}")',
        "An issuer reports normalized EPS of $2.00. The analyst estimates a 3.0% growth rate (g = 3) and corporate bond yield of 4.4% (Y = 4.4). Calculate the indicated heuristic value. Then recalculate if bond yields rise to 5.5% (Y = 5.5). Identify two major economic factors completely omitted from this heuristic formula.",
        "At Y = 4.4%: V = $2.00 × (8.5 + 2 × 3) × (4.4 / 4.4) = $2.00 × 14.5 × 1.0 = $29.00 per share. At Y = 5.5%: V = $2.00 × 14.5 × (4.4 / 5.5) = $29.00 × 0.80 = $23.20 per share. Two major economic factors omitted: (1) Mandatory capital expenditures and working capital reinvestment required to generate the 3% growth; and (2) The duration of competitive advantage and risk of obsolescence or competitive entry.",
        [
            q(
                "In the Graham growth formula V = EPS × (8.5 + 2g) × (4.4 / Y), how are the growth rate g and the bond yield Y entered?",
                [
                    "As decimals (e.g., 0.05 for 5%)",
                    "As percentage points (e.g., 5 for 5% and 4.4 for 4.4%)",
                    "In basis points (e.g., 500 for 5%)",
                ],
                1,
                "The formula's convention requires percentage points as integers/floats (e.g., 5 for 5% and 4.4 for 4.4%).",
            ),
            q(
                "Why must an analyst treat the Graham growth heuristic as an assumption sensitivity rather than a complete valuation model?",
                [
                    "The formula does not model required capital reinvestment, competitive advantage fade, balance sheet liabilities, or failure risk",
                    "The formula was banned by the SEC",
                    "The formula can only be calculated on mainframe computers",
                ],
                0,
                "The formula is a compact rule of thumb that compresses complex operational, reinvestment, and competitive dynamics into fixed multipliers.",
            ),
            q(
                "Using the Graham growth heuristic, an issuer has EPS of $3.00, an expected growth rate input of 2%, and a reference bond yield Y of 4.4%. What is the indicated heuristic value?",
                ["$25.50", "$37.50", "$51.00"],
                1,
                "V = $3.00 × (8.5 + 2 × 2) × (4.4 / 4.4) = $3.00 × 12.5 × 1.0 = $37.50 per share.",
            ),
        ],
    )

    add(
        "1.23",
        "VIII",
        "Bridges to modern enterprise valuation",
        "Convert operating value into common equity and test discount-rate assumptions in a transparent modern model.",
        r"""
## The analytical question

Modern institutional finance largely organizes valuation around **Discounted Free Cash Flow (DCF)** and **Enterprise Valuation (EV)** models. While modern notation differs from Graham and Dodd's 1940 vocabulary, the underlying economic principles are identical:
- Both frameworks insist that business value is derived from the cash generation of operating assets.
- Both demand that debt and senior claims be deducted before arriving at the residual equity value.
- Both recognize that an asset cannot be counted twice.

To bridge classical security analysis to modern enterprise valuation, we examine the **Unlevered Free Cash Flow (FCFF)** framework.

Consider a stable, mature industrial operating business:
1. **Unlevered Free Cash Flow ($FCF$)**: The cash generated by operations after all operating expenses, taxes, and necessary maintenance capital expenditures, but *before* deducting interest payments to debt holders:
   $$FCF = \text{EBIT} \times (1 - t) + \text{Depreciation} - \text{CapEx} - \Delta \text{NWC}$$
2. **Capitalized Operating Enterprise Value ($V_{\text{operations}}$)**:
   - Under a conservative **Zero-Growth Perpetuity** premise:
     $$V_{\text{operations}} = \frac{FCF}{r}$$
   - Under a **Gordon Growth Perpetuity** premise (assuming sustainable perpetual growth $g < r$):
     $$V_{\text{operations}} = \frac{FCF_1}{r - g}$$
   Where $r$ is the required cost of capital, and $g$ is the perpetual growth rate.
3. **The Modern Claims Bridge to Common Equity ($V_{\text{equity}}$)**:
   $$V_{\text{equity}} = V_{\text{operations}} + \text{Excess Nonoperating Cash} - \text{Total Debt} - \text{Preferred Claims}$$
   $$\text{Common Value per Share} = \frac{V_{\text{equity}}}{N_{\text{diluted shares}}}$$

Notice the methodological rigor:
- **Never Deduct Operating Liabilities in the Bridge**: Operating trade payables and accrued payroll are already subtracted when calculating Net Operating Profit After Tax and working capital ($\Delta \text{NWC}$). Subtracting trade payables again in the equity bridge is a fatal double count!
- **Only Add Genuinely Excess Cash**: Operating cash needed to run everyday store branches cannot be added.
- **Respect the Mathematical Constraint ($r > g$)**: In a growing perpetuity, the discount rate $r$ must strictly exceed the growth rate $g$. If an analyst assumes $g \ge r$, the formula breaks down into infinity or nonsense.

## A worked example

Let us evaluate Alder Manufacturing using the modern enterprise valuation framework:
- Audited Sustainable Unlevered Free Cash Flow: $FCF = \$15.0\text{ million per year}$
- Total Balance Sheet Cash: $\$30.0\text{ million}$ (of which $\$20.0\text{ million}$ is true excess nonoperating cash)
- Total Interest-Bearing Debt: $\$40.0\text{ million}$
- Preferred stock claims: $\$0.00$
- Fully diluted share count: $N = 10.0\text{ million shares}$

Let us trace the valuation across three modern discount rate and growth scenarios:

### Scenario 1: Conservative No-Growth at 10% Hurdle Rate ($r = 10\%$, $g = 0$)
1. Capitalized Operating Enterprise Value:
   $$V_{\text{operations}} = \frac{\$15.0\text{M}}{0.10} = \$150.0\text{ million}$$
2. Apply the claims bridge to equity:
   $$V_{\text{equity}} = \$150.0\text{M} + \$20.0\text{M (Excess Cash)} - \$40.0\text{M (Debt)} = \$130.0\text{ million}$$
3. Value per Common Share:
   $$V_{\text{per share}} = \frac{\$130.0\text{M}}{10.0\text{M}} = \$13.00\text{ per share}$$

### Scenario 2: Stressed Hurdle Rate at 12% ($r = 12\%$, $g = 0$)
Suppose macroeconomic volatility raises the required rate of return to $12.0\%$:
1. Operating Enterprise Value:
   $$V_{\text{operations}} = \frac{\$15.0\text{M}}{0.12} = \$125.0\text{ million}$$
2. Equity Value:
   $$V_{\text{equity}} = \$125.0\text{M} + \$20.0\text{M} - \$40.0\text{M} = \$105.0\text{ million}$$
3. Value per Common Share:
   $$V_{\text{per share}} = \frac{\$105.0\text{M}}{10.0\text{M}} = \$10.50\text{ per share}$$

### Scenario 3: Modest Sustainable Growth ($r = 10\%$, $g = 2.0\%$)
Now suppose Alder's equipment patents allow it to achieve a modest $2.0\%$ perpetual growth rate without requiring incremental external capital:
1. Operating Enterprise Value:
   $$V_{\text{operations}} = \frac{\$15.0\text{M} \times 1.02}{0.10 - 0.02} = \frac{\$15.30\text{M}}{0.08} = \$191.25\text{ million}$$
2. Equity Value:
   $$V_{\text{equity}} = \$191.25\text{M} + \$20.0\text{M} - \$40.0\text{M} = \$171.25\text{ million}$$
3. Value per Common Share:
   $$V_{\text{per share}} = \frac{\$171.25\text{M}}{10.0\text{M}} = \$17.13\text{ per share}$$

Look at the sensitivity:
Across these three disciplined cases, value ranges from **$\$10.50$ to $\$17.13$ per share**.
Under Graham and Dodd's margin of safety discipline, the conservative lower bound ($\$10.50$) governs the purchase decision. A required $30\%$ margin demands a purchase price no higher than $\$10.50 \times 0.70 = \$7.35$.

## Research discipline

When constructing modern enterprise DCF models:
1. **Always Verify That Cash Flow is Truly Unlevered**: If you discount at WACC (Weighted Average Cost of Capital) or an asset hurdle rate, do not subtract interest expense from the cash flow! Subtracting interest and discounting by an enterprise hurdle rate subtracts financing costs twice.
2. **Stress-Test Terminal Growth Assumptions**: Never set perpetual growth ($g$) higher than long-term GDP growth ($2\%$ to $3\%$). Assuming a company grows faster than the global economy forever is mathematically impossible.
3. **Audit Excess Cash Rigorously**: Verify whether cash is trapped abroad or pledged to bank letters of credit before adding it to enterprise value.
4. **Reconcile with Balance Sheet Asset Realization**: Compare the indicated DCF equity value with the company's tangible book value and NCAV. If DCF is $\$15.00$ but tangible book value is $\$4.00$, recognize that $\$11.00$ ($73\%$) of your estimated value depends entirely on cash flows yet to be earned.
""",
        r"EV=\frac{FCF_1}{r-g};\quad V_{\text{equity}}=EV+\text{Excess Cash}-\text{Debt};\quad V_{\text{share}}=\frac{V_{\text{equity}}}{N}",
        'fcf = 15.0\nexcess_cash = 20.0\ndebt = 40.0\nshares = 10.0\nfor r in [0.10, 0.12]:\n    ev_nogrowth = fcf / r\n    eq_nogrowth = ev_nogrowth + excess_cash - debt\n    print(f"Rate r = {int(r*100)}% (g=0) -> EV: ${round(ev_nogrowth, 1)}M -> Equity/Share: ${round(eq_nogrowth / shares, 2)}")\nr = 0.10\ng = 0.02\nev_growth = (fcf * (1 + g)) / (r - g)\neq_growth = ev_growth + excess_cash - debt\nprint(f"Growth g = 2% (r=10%) -> EV: ${round(ev_growth, 2)}M -> Equity/Share: ${round(eq_growth / shares, 2)}")',
        "An enterprise generates sustainable unlevered free cash flow of $12M per year. It holds $8M in excess cash, $28M in interest-bearing debt, and has 8 million shares outstanding. Calculate the no-growth equity value per share at: (1) an 8% required hurdle rate, and (2) a 10% required hurdle rate.",
        "Under 8% hurdle rate: Enterprise value is $12M / 0.08 = $150M. Equity value is $150M + $8M (excess cash) − $28M (debt) = $130M. Value per share is $130M / 8M = $16.25 per share. Under 10% hurdle rate: Enterprise value is $12M / 0.10 = $120M. Equity value is $120M + $8M − $28M = $100M. Value per share is $100M / 8M = $12.50 per share. Consistent claims treatment requires adding only excess cash and deducting all interest-bearing debt.",
        [
            q(
                "Under the Gordon growth perpetuity model EV = FCF1 / (r − g), what mathematical condition is required for enterprise value to be positive and finite?",
                ["r = g", "r > g", "r < g"],
                1,
                "The discount rate r must strictly exceed the perpetual growth rate g (r − g > 0) to yield a finite positive value.",
            ),
            q(
                "When transitioning from unlevered enterprise operating value (EV) to the equity value belonging to common shareholders, how is debt treated?",
                [
                    "Debt is added to enterprise value",
                    "Debt is deducted from enterprise value because debtholders possess a prior contractual claim on operating assets",
                    "Debt is ignored entirely",
                ],
                1,
                "Enterprise value represents total firm value; debt claims must be deducted to isolate the residual equity value.",
            ),
            q(
                "A company generates sustainable unlevered free cash flow of $10 million discounted at a 10% required return with zero growth. It holds $5 million in excess cash, $25 million in debt, and has 10 million shares. What is the indicated common equity value per share?",
                ["$8.00", "$10.00", "$13.00"],
                0,
                "EV = $10M / 0.10 = $100M. Equity value = $100M + $5M (cash) − $25M (debt) = $80M. Per share = $80M / 10M = $8.00 per share.",
            ),
        ],
    )

    add(
        "1.24",
        "VIII",
        "Capstone: the Alder investment committee",
        "Deliver a reconciled valuation memo that combines credit protection, earning power, assets, and price discipline.",
        r"""
## The analytical question

Welcome to the **Capstone Case Study** of *Security Analysis*. As a senior security analyst presenting before the Investment Committee, you are tasked with evaluating a definitive investment recommendation for **Alder Manufacturing Corporation**.

Your mandate is to reconcile all three classical Graham and Dodd valuation methodologies into an auditable investment brief:
1. **Creditor Protection and Fixed Claim Coverage**: Stress-testing interest coverage across peak, normalized, and recessionary trough cycles.
2. **Asset Realizability and Liquidation Recovery**: Calculating classical Net Current Asset Value (NCAV) and applying stressed realization haircuts to physical assets.
3. **Normalized Earning Power and Going-Concern Valuation**: Bridging reported earnings to sustainable cash flows, capitalizing unlevered operations, and constructing an honest claims bridge to common equity.
4. **Margin of Safety and Final Decision Rule**: Establishing the maximum conservative purchase price ceiling ($P_{\max}$) and issuing a formal recommendation (Buy, Hold, or Reject).

### The Capstone Case File (All dollar amounts in millions, except per-share data)
- **Current Common Share Market Quote**: $P = \$6.20\text{ per share}$
- **Diluted Common Shares Outstanding**: $N = 10.0\text{ million shares}$
- **Balance Sheet Disclosures**:
  - Cash and cash equivalents: $\$30.0\text{ million}$ (Audited minimum operational cash required is $\$10.0\text{ million}$, leaving **$\$20.0\text{ million}$ in true excess cash**)
  - Accounts receivable: $\$50.0\text{ million}$
  - Inventories: $\$70.0\text{ million}$
  - Net Property, Plant, & Equipment (fixed assets): $\$90.0\text{ million}$
  - **Total Liabilities**: $\$100.0\text{ million}$ (including **$\$60.0\text{ million}$ in interest-bearing debt** and $\$40.0\text{ million}$ in operating liabilities)
  - Preferred stock claims: $\$0.00$
- **Operating Earnings Disclosures**:
  - Reported current EBIT: $\$24.0\text{ million}$ (includes an isolated nonrecurring pretax gain of $\$4.0\text{ million}$ from selling surplus land)
  - Annual contractual debt interest charges: $\$5.0\text{ million}$
  - Severe trough recessionary EBIT: $\$12.0\text{ million}$
  - Sustainable unlevered operating free cash flow range: $\$9.0\text{ million to } \$12.0\text{ million}$
  - Required hurdle rate of return: $10.0\%$ ($r = 0.10$, zero growth)
- **Stressed Asset Realization Haircut Assumptions**:
  - Cash: $100\%$ recovery
  - Accounts receivable: $80\%$ recovery
  - Inventories: $50\%$ recovery
  - Fixed assets: $20\%$ recovery
  - Total liabilities: paid $100\%$ in full ($\$100.0\text{ million}$)
  - Mandatory plant decommissioning & severance closure costs: $\$8.0\text{ million}$

## A worked example

Let us execute the exact forensic reconciliations required for the committee brief:

### 1. Interest Coverage Reconciliations
1. Normalized EBIT:
   $$\text{EBIT}_{\text{norm}} = \text{Reported EBIT} - \text{Nonrecurring Gain} = \$24.0\text{M} - \$4.0\text{M} = \$20.0\text{ million}$$
2. Normalized Interest Coverage:
   $$\text{Coverage}_{\text{norm}} = \frac{\$20.0\text{M}}{\$5.0\text{M}} = 4.0\times$$
3. Stressed Recessionary Trough Coverage:
   $$\text{Coverage}_{\text{weak}} = \frac{\$12.0\text{M}}{\$5.0\text{M}} = 2.4\times$$
Both coverage ratios meet high-grade creditor standards ($4.0\times$ normal, $2.4\times$ trough $\ge 2.0\times$).

### 2. Balance Sheet Asset Realizations
1. Classical Net Current Asset Value (NCAV):
   $$\text{Current Assets} = \$30.0\text{M (Cash)} + \$50.0\text{M (AR)} + \$70.0\text{M (Inv)} = \$150.0\text{ million}$$
   $$\text{Total NCAV} = \$150.0\text{M} - \$100.0\text{M (Total Liabilities)} = \$50.0\text{ million}$$
   $$\text{NCAV per Share} = \frac{\$50.0\text{M}}{10.0\text{M}} = \$5.00\text{ per share}$$
2. Stressed Liquidation Realization:
   $$\text{Realized Assets} = (\$30.0\text{M} \times 1.0) + (\$50.0\text{M} \times 0.80) + (\$70.0\text{M} \times 0.50) + (\$90.0\text{M} \times 0.20)$$
   $$\text{Realized Assets} = \$30.0\text{M} + \$40.0\text{M} + \$35.0\text{M} + \$18.0\text{M} = \$123.0\text{ million}$$
   Subtract total liabilities ($\$100.0\text{M}$) and closure costs ($\$8.0\text{M}$):
   $$\text{Net Realization Residual} = \$123.0\text{M} - \$100.0\text{M} - \$8.0\text{M} = \$15.0\text{ million}$$
   $$\text{Adjusted Realization per Share} = \frac{\$15.0\text{M}}{10.0\text{M}} = \$1.50\text{ per share}$$

### 3. Going-Concern Operating Equity Valuation
Capitalize sustainable unlevered cash flows ($\$9.0\text{M}$ to $\$12.0\text{M}$) at $10.0\%$:
- **Conservative Operating Case ($FCF = \$9.0\text{M}$)**:
  $$V_{\text{operations}} = \frac{\$9.0\text{M}}{0.10} = \$90.0\text{ million}$$
  $$V_{\text{equity}} = \$90.0\text{M} + \$20.0\text{M (Excess Cash)} - \$60.0\text{M (Debt)} = \$50.0\text{ million}$$
  $$\text{Per Share} = \frac{\$50.0\text{M}}{10.0\text{M}} = \$5.00\text{ per share}$$
- **Base Operating Case ($FCF = \$12.0\text{M}$)**:
  $$V_{\text{operations}} = \frac{\$12.0\text{M}}{0.10} = \$120.0\text{ million}$$
  $$V_{\text{equity}} = \$120.0\text{M} + \$20.0\text{M (Excess Cash)} - \$60.0\text{M (Debt)} = \$80.0\text{ million}$$
  $$\text{Per Share} = \frac{\$80.0\text{M}}{10.0\text{M}} = \$8.00\text{ per share}$$

### 4. Margin of Safety Decision Rule
Your investment policy requires a **mandatory $30.0\%$ margin of safety** against the **conservative operating equity estimate** ($\$5.00$):

$$P_{\max} = \$5.00 \times (1 - 0.30) = \$5.00 \times 0.70 = \$3.50\text{ per share}$$

Now evaluate the current market quotation ($P = \$6.20$):
- At $\$6.20$, the stock trades at a $22.5\%$ discount to the optimistic base case ($\$8.00$).
- However, $\$6.20$ is **$24.0\%$ ABOVE** the conservative operating estimate of $\$5.00$!
- Most importantly, $\$6.20$ is **$77.1\%$ above** the maximum allowable price ceiling of $\$3.50$.

**Committee Decision**: **REJECT PURCHASE AT \$6.20**. The security lacks an adequate margin of safety. Capital allocation is prohibited until market quotations decline to $\$3.50$ or lower.

## Research discipline

To deliver your Capstone Investment Committee brief:
1. **Never Add Incompatible Premise Values**: Do not add the $\$1.50$ liquidation value to the $\$5.00$ operating value. State why they represent mutually exclusive outcomes.
2. **Maintain the Python Golden Arithmetic Verification**: Run the standardized committee worksheet. Verify that all six primary metrics print exactly in the terminal.
3. **Pre-Register Falsification Triggers**:
   - If market quotation reaches $\$3.50$ while normalized EBIT remains $\ge \$20.0\text{M}$, authorize execution of a $5\%$ portfolio position.
   - If trough EBIT drops below $\$10.0\text{M}$ (violating $2.0\times$ interest coverage), reduce conservative equity value to $\$3.00$ and lower $P_{\max}$ to $\$2.10$.
4. **Archive the Complete Evidentiary Audit Trail**: Store all filings, indenture excerpts, and calculations in your permanent investment journal.
""",
        r"P_{\max}=V_{\text{conservative}}(1-M_{\text{required}});\quad \text{Coverage}=\frac{\text{EBIT}_{\text{norm}}}{I}",
        'print("Normalized coverage:", (24 - 4) / 5)\nprint("Weak coverage:", 12 / 5)\nprint("NCAV per share:", (30 + 50 + 70 - 100) / 10)\nprint("Adjusted realization:", (30 + 50 * .8 + 70 * .5 + 90 * .2 - 100 - 8) / 10)\nfor cash_flow in [9, 12]:\n    print("Operating equity estimate:", (cash_flow / .10 + 20 - 60) / 10)\nprint("Maximum conservative price:", 5 * .70)',
        "Write the committee memo in your notebook. Then stress the case with two years of cash burn totaling $12M before asset realization, and raise the operating discount rate to 12%. Does either sensitivity support the $6.20 quote under the stipulated 30% rule?",
        "Ignoring additional timing discount, realization falls from $15M to $3M in total, or $0.30 per share. At 12%, operating equity is ($75M + $20M − $60M) / 10M to ($100M + $20M − $60M) / 10M = $3.50 to $6.00 per share. A 30% discount to $3.50 permits a maximum price of $2.45. Neither sensitivity supports the current $6.20 quote under the chosen rule. A strong memo also questions the timing, recoveries, and durability of cash flow.",
        [
            q(
                "In the Alder Manufacturing capstone, why can only $20 million of the reported $30 million cash balance be added as excess cash in the enterprise valuation bridge?",
                [
                    "All $30 million in cash can be distributed immediately",
                    "The $10 million required for everyday operations is already embedded in the operating cash flows; adding all $30 million would count that operating cash twice",
                    "Cash is legally prohibited from having value in security analysis",
                ],
                1,
                "The $10M required for operations supports the modeled cash flows; adding all cash counts that portion twice.",
            ),
            q(
                "In the capstone case, applying a mandatory 30% margin of safety to the conservative operating equity estimate of $5.00 per share yields what maximum allowable purchase price?",
                ["$3.50", "$5.00", "$6.20"],
                0,
                "Maximum price is $5.00 × (1 − 0.30) = $3.50 per share.",
            ),
            q(
                "An investment committee reviews a revised capstone case where conservative intrinsic equity value is estimated at $7.00 per share and the mandate requires a 30% margin of safety. The current market price is $5.20. What is the committee's decision?",
                [
                    "Approve purchase because $5.20 is below $7.00",
                    "Reject purchase because the maximum allowable price is $4.90 ($7.00 × 0.70), which $5.20 exceeds",
                    "Increase the valuation estimate until the stock passes",
                ],
                1,
                "The rule demands $7.00 × 0.70 = $4.90. A quote of $5.20 violates the margin of safety; modifying valuation to fit market price violates core investment discipline.",
            ),
        ],
    )

    # -------------------------------------------------------------------------
    # PART IX: ADVANCED FORENSIC AND VALUATION SYNTHESIS
    # -------------------------------------------------------------------------

    add(
        "1.25",
        "IX",
        "Accrual forensics and cash conversion",
        "Quantify the gap between reported profit and operating cash, and separate sustainable earnings from accrual-driven accounting results.",
        r"""
## The analytical question

Accrual accounting records revenue when it is earned and expenses when they are incurred, not when cash changes hands. That convention can describe a business well, but it also gives management discretion over timing. When profit rises while operating cash flow lags, the analyst must ask whether the business is genuinely more profitable or merely booking more estimates.

The basic diagnostic is **accruals**, the portion of reported profit not represented by operating cash flow:

$$\text{Accruals} = \text{Net income} - \text{Operating cash flow}$$

Scale accruals by average total assets so that companies of different sizes can be compared:

$$\text{Accrual ratio} = \frac{\text{Net income} - \text{Operating cash flow}}{\text{Average total assets}}$$

A second view is **cash conversion**, the share of each profit dollar that arrived as operating cash:

$$\text{Cash conversion} = \frac{\text{Operating cash flow}}{\text{Net income}}$$

A high accrual ratio and a cash conversion ratio materially below one are not proof of manipulation. They are reasons to inspect receivables, inventory, contract assets, payables, and nonrecurring items. The same tests should be repeated across several years; a single year can be distorted by seasonality or a large contract.

## A worked example

A distributor reports net income of $120 million, operating cash flow of $70 million, and average total assets of $1,000 million. Its accrual ratio is:

$$\frac{120-70}{1{,}000}=5.0\%$$

Cash conversion is $70 / 120 = 58.3\%$, meaning only about 58 cents of operating cash arrived for each dollar of reported profit. The remaining $50 million sits in accruals.

The analyst then decomposes the balance-sheet change. Suppose receivables rose $30 million faster than revenue, inventory rose $15 million, and payables contributed $5 million. Those items explain the direction of the gap but not yet whether it is benign. A distributor extending terms to win a large new customer might show the same pattern temporarily. A distributor stuffing inventory into a weakening channel, or recognizing revenue on shipments its customers may return, would show it persistently.

The evidence file should therefore record three things separately: the reported accrual ratio, the specific balance-sheet accounts that moved, and the assumption about whether those balances will convert into cash. If the company's five-year accrual ratio is consistently above its industry and cash conversion keeps falling, the analyst lowers the sustainable earnings estimate rather than capitalizing the reported profit.

## Research discipline

1. **Reconcile the cash-flow statement to the income statement** before computing a ratio. Reclassifications and discontinued operations can otherwise create a false gap.
2. **Use average assets, not year-end assets**, when the balance sheet changed materially during the year.
3. **Inspect the composition of accruals.** Receivable growth, inventory build, and capitalized costs carry different risks. A single ratio cannot distinguish them.
4. **Test persistence.** One year is an observation; a multi-year pattern is evidence. Compare the company with its own history and with a relevant peer group.
""",
        r"\text{Accrual ratio}=\frac{\text{NI}-\text{CFO}}{\text{Avg assets}};\quad \text{Cash conversion}=\frac{\text{CFO}}{\text{NI}}",
        'net_income = 120\ncfo = 70\nassets = 1000\naccruals = net_income - cfo\nprint("Accruals:", accruals)\nprint("Accrual ratio (%):", round(accruals / assets * 100, 1))\nprint("Cash conversion (%):", round(cfo / net_income * 100, 1))',
        "A company reports net income of $90 million, operating cash flow of $45 million, and average total assets of $900 million. Calculate accruals, the accrual ratio, and cash conversion. State one account you would inspect first and why.",
        "Accruals are $90M − $45M = $45M. The accrual ratio is 45 / 900 = 5.0%. Cash conversion is 45 / 90 = 50.0%. Inspect receivables or contract assets first if revenue grew, because they show whether profit was recognized before cash collection. Inventory is the next candidate when sales are slowing.",
        [
            q(
                "Net income is 80 and operating cash flow is 60. Accruals are:",
                ["20", "60", "140"],
                0,
                "Accruals equal net income minus operating cash flow: 80 − 60 = 20.",
            ),
            q(
                "Which pattern most clearly calls for deeper forensic work?",
                [
                    "Rising profit with falling cash conversion across several years",
                    "Stable profit and stable cash conversion",
                    "A one-year cash outflow from a known inventory build",
                ],
                0,
                "A persistent divergence between profit and cash is stronger evidence than a single explained outflow.",
            ),
            q(
                "A company has net income of 150, operating cash flow of 90, and average assets of 1,200. Its accrual ratio is:",
                ["2.5%", "5.0%", "60.0%"],
                1,
                "Accruals are 150 − 90 = 60; 60 / 1,200 = 5.0%. Cash conversion is a separate 60% measure.",
            ),
        ],
    )

    add(
        "1.26",
        "IX",
        "Manipulation screens and model risk",
        "Use the Beneish M-score as a screening aid, understand its inputs, and state the limits of a statistical manipulation model.",
        r"""
## The analytical question

A manipulation screen combines several accounting signals into one score. Messod Beneish's eight-variable model is one of the best-known examples. It compares a company's current accounting ratios with its own prior-year ratios and produces an M-score; lower values are generally less suggestive of earnings manipulation.

$$M=-4.84+0.92\,\text{DSRI}+0.528\,\text{GMI}+0.404\,\text{AQI}+0.892\,\text{SGI}+0.115\,\text{DEPI}-0.172\,\text{SGAI}+4.679\,\text{TATA}-0.327\,\text{LGVI}$$

The inputs capture different pressures:

| Variable | What it compares | Why it matters |
| :--- | :--- | :--- |
| DSRI | Days sales in receivables, current vs prior | Revenue recognized faster than cash collection |
| GMI | Gross margin, prior vs current | Margin deterioration can create pressure to manage earnings |
| AQI | Asset quality, current vs prior | More soft or non-current assets can signal capitalization |
| SGI | Sales growth, current vs prior | High growth raises both opportunity and pressure |
| DEPI | Depreciation rate, prior vs current | Slower depreciation raises reported profit |
| SGAI | SG&A intensity, current vs prior | Falling overhead may reflect cuts that impair future growth |
| TATA | Total accruals to total assets | The accrual diagnostic from the previous lesson |
| LVGI | Leverage, current vs prior | Rising debt can create covenant pressure |

A common screening threshold is an M-score above **−1.78**. The threshold is a prompt for investigation, not a verdict.

## A worked example

Suppose a company has DSRI = 1.10, GMI = 1.05, AQI = 1.02, SGI = 1.15, DEPI = 1.00, SGAI = 1.00, TATA = 0.04, and LVGI = 1.00. Substituting:

$$M=-4.84+0.92(1.10)+0.528(1.05)+0.404(1.02)+0.892(1.15)+0.115(1.00)-0.172(1.00)+4.679(0.04)-0.327(1.00)$$

The sum is approximately **−2.03**, below the threshold, so the screen does not flag the company. If TATA rises to 0.10 while the other inputs stay unchanged, the score rises to approximately **−1.75**, above the threshold. The entire change came from accruals, which is exactly the kind of lead an analyst should investigate.

The model's weaknesses matter. It was estimated on a particular historical sample and industry mix. It produces false positives for fast-growing firms with legitimate working-capital needs, and false negatives for manipulators whose ratios remain inside the model's range. It uses reported data, so a fraud that also falsifies the underlying accounts can pass.

## Research discipline

1. **Compute the inputs yourself** from filings rather than relying on a data vendor's score. Record the period and units.
2. **Treat the score as a triage tool.** A flag means read the footnotes, reconcile receivables, and inspect accruals; it does not establish fraud.
3. **Compare within an industry and a size band.** A retailer's working-capital pattern should not be judged against a software company's.
4. **Document the threshold and the model version** in the research file so another analyst can reproduce the screen.
""",
        r"M=-4.84+0.92D+0.528G+0.404A+0.892S+0.115P-0.172E+4.679T-0.327L",
        'dsri = 1.10\ngmi = 1.05\naqi = 1.02\nsgi = 1.15\ndepi = 1.00\nsgai = 1.00\ntata = 0.10\nlvgi = 1.00\nm = -4.84 + 0.92*dsri + 0.528*gmi + 0.404*aqi + 0.892*sgi + 0.115*depi - 0.172*sgai + 4.679*tata - 0.327*lvgi\nprint("M-score:", round(m, 2))\nprint("Above threshold:", m > -1.78)',
        "Using DSRI 1.20, GMI 1.00, AQI 1.10, SGI 1.30, DEPI 1.00, SGAI 1.00, TATA 0.06, and LVGI 1.10, calculate the M-score and state the screening conclusion. Then name one reason the result could be a false positive.",
        "The score is approximately −1.74, just above the −1.78 threshold, so the screen flags the company. A fast-growing firm can legitimately show high sales growth, receivables growth, and accruals while expanding into new customers; that is a common false-positive path. The next step is to reconcile receivables and inspect revenue recognition, not to conclude fraud.",
        [
            q(
                "In the Beneish model, which input directly measures accruals relative to assets?",
                ["DSRI", "TATA", "LVGI"],
                1,
                "TATA is total accruals to total assets; DSRI concerns receivables and LVGI concerns leverage.",
            ),
            q(
                "An M-score above the threshold should be interpreted as:",
                [
                    "Proof that management committed fraud",
                    "A reason to investigate specific accounting accounts",
                    "A guarantee that future earnings will fall",
                ],
                1,
                "The model is a screening aid with false positives and false negatives; it prompts evidence gathering.",
            ),
            q(
                "A company's M-score is −2.30. Under the −1.78 convention, the screen suggests:",
                ["A flag requiring investigation", "No flag, though other evidence may still matter", "Guaranteed manipulation"],
                1,
                "A score below the threshold does not flag the company under this convention, but the model is not a clean bill of health.",
            ),
        ],
    )

    add(
        "1.27",
        "IX",
        "Hidden liabilities and off-balance-sheet claims",
        "Adjust reported debt for leases, guarantees, pension deficits, and contingent claims before judging solvency.",
        r"""
## The analytical question

A balance sheet reports liabilities that accounting rules recognize, but an analyst cares about obligations the business must actually fund. Operating leases, purchase commitments, guarantees, underfunded pensions, litigation, and special-purpose entities can all consume cash without appearing as conventional debt. Comparing an issuer's reported leverage with a peer's can therefore be misleading.

Build an **adjusted debt** figure:

$$\text{Adjusted debt} = \text{Reported debt} + \text{Lease liabilities} + \text{Guarantees} + \text{Pension deficit} + \text{Other probable claims}$$

Then compare it with a measure of recurring cash earnings:

$$\text{Adjusted leverage} = \frac{\text{Adjusted debt}}{\text{Recurring EBITDA}}$$

The adjustment should be explicit and consistent. A lease is not identical to a bond: it can be renegotiated, and its timing may differ. A guarantee may never be called. The purpose is not to pretend every contingent claim is certain, but to stop the analyst from treating a legally real obligation as if it did not exist.

## A worked example

A manufacturer reports debt of $60 million. Its notes disclose lease liabilities with a present value of $20 million, a guarantee of a supplier's borrowings of $10 million, and a pension deficit of $5 million. Adjusted debt is:

$$60+20+10+5=\$95\text{ million}$$

Recurring EBITDA is $40 million. Reported leverage is $60 / 40 = 1.5×$, while adjusted leverage is $95 / 40 = 2.375×$. The gap is large enough to change the conclusion of a credit screen that treats 2× as a ceiling.

The analyst should then classify the claims. The lease is a contractual payment stream and belongs in the base case. The guarantee is contingent; it belongs in a stress case unless the supplier is already distressed. The pension deficit depends on discount rates and asset returns. A disciplined file shows reported leverage, adjusted base-case leverage, and stressed leverage separately, with each item's source and maturity.

## Research discipline

1. **Read the lease, guarantee, pension, and contingency notes**, not only the face of the balance sheet.
2. **Trace special-purpose entities** and other structured vehicles. Ask who bears the loss if the vehicle's assets fall short.
3. **Match the adjustment to the maturity profile.** A pension deficit payable over decades is not the same liquidity burden as a bond maturing next year.
4. **Apply the same definition across peers** and disclose every adjustment so the comparison is reproducible.
""",
        r"\text{Adj. debt}=\text{Debt}+\text{Leases}+\text{Guarantees}+\text{Pension deficit}+\text{Other claims}",
        'debt = 60\nleases = 20\nguarantees = 10\npension = 5\nebitda = 40\nadjusted = debt + leases + guarantees + pension\nprint("Reported leverage:", debt / ebitda)\nprint("Adjusted debt:", adjusted)\nprint("Adjusted leverage:", adjusted / ebitda)',
        "A company reports debt of $80 million, leases of $30 million, guarantees of $15 million, an underfunded pension of $5 million, and recurring EBITDA of $50 million. Calculate reported and adjusted leverage. Which claim would you stress separately, and why?",
        "Adjusted debt is 80 + 30 + 15 + 5 = $130M. Reported leverage is 80 / 50 = 1.6×; adjusted leverage is 130 / 50 = 2.6×. Stress the guarantee separately because it is contingent: it may never be called, but it could become a real claim if the guaranteed party fails. The lease is a contractual stream and normally belongs in the base case.",
        [
            q(
                "Which item is an off-balance-sheet claim that an analyst should consider adding to adjusted debt?",
                ["A trade payable due next month", "A guarantee of another company's borrowings", "A prepaid insurance premium"],
                1,
                "A guarantee is a contingent obligation that may become a claim; trade payables are already recognized and prepaid insurance is an asset.",
            ),
            q(
                "Reported debt is 60, adjusted debt is 90, and EBITDA is 30. Adjusted leverage is:",
                ["2.0×", "3.0×", "5.0×"],
                1,
                "90 / 30 = 3.0×; the unadjusted ratio would be 2.0×.",
            ),
            q(
                "Why should an analyst show reported, adjusted, and stressed leverage separately?",
                [
                    "To make every company look equally risky",
                    "To distinguish contractual, contingent, and downside claims instead of hiding the judgment in one number",
                    "Because accounting rules require three ratios",
                ],
                1,
                "Separating the cases shows which obligations are certain, which are contingent, and how the conclusion changes under stress.",
            ),
        ],
    )

    add(
        "1.28",
        "IX",
        "Segment, customer, and concentration analysis",
        "Measure concentration and test whether reported group margins hide a fragile mix of segments, customers, or geographies.",
        r"""
## The analytical question

Consolidated revenue and margin can conceal very different businesses. A group may report a healthy average margin while one segment earns most of the profit and another is loss-making. A single customer may account for a third of sales. A currency or a regulator may dominate the cash flows. The analyst's task is to separate the sources of value and the sources of risk.

A simple concentration measure is the **Herfindahl-Hirschman Index** applied to revenue shares:

$$\text{HHI}=\sum_{i=1}^{n}s_i^2$$

where $s_i$ is the share of total revenue from segment or customer $i$. A firm with four equal segments has HHI $=4(0.25^2)=0.25$. A firm with one segment at 70% has HHI at least $0.49$. Higher values mean more concentration, but the measure says nothing about the quality of the concentrated relationship.

The analyst should also compute **segment contribution margin** and **customer concentration** separately. A segment with high revenue but low or negative margin can dilute group profitability; a customer with high revenue but weak bargaining power can compress margins when the contract renews.

## A worked example

A group reports revenue of $100 million across three segments: A $50M, B $30M, and C $20M. The HHI is:

$$0.50^2+0.30^2+0.20^2=0.25+0.09+0.04=0.38$$

The group also discloses that its largest customer represents 35% of revenue. Group operating margin is 12%, but segment A earns 20%, segment B earns 8%, and segment C loses 5%.

The analyst reconstructs segment profit: A contributes $10M, B contributes $2.4M, and C subtracts $1.0M, for $11.4M before unallocated costs. The headline margin is not wrong, but it is not a stable description of the whole group. If customer A, which buys mostly from segment A, renegotiates a 5% price cut, revenue falls $2.5M and, at the segment's incremental margin, profit can fall by much more than the group average suggests.

The file should record the concentration measure, the segment margins, the customer disclosure, and a stressed case in which the largest customer or segment deteriorates. A diversified group is not automatically safer if its diversification is only in low-margin activities.

## Research discipline

1. **Use the segment note**, not a management presentation's adjusted view. Reconcile segment profit to consolidated profit.
2. **Distinguish revenue concentration from profit concentration.** The segment that matters for value may be smaller by sales.
3. **Read customer-concentration disclosures** and contract terms. A large customer can be an asset or a source of pricing pressure.
4. **Stress the concentrated unit.** Ask what happens to group value if the largest segment's margin normalizes or its customer leaves.
""",
        r"\text{HHI}=\sum_i s_i^2;\quad \text{Segment margin}=\frac{\text{Segment profit}}{\text{Segment revenue}}",
        'segment_a = 50\nsegment_b = 30\nsegment_c = 20\ntotal = segment_a + segment_b + segment_c\nhhi = (segment_a/total)**2 + (segment_b/total)**2 + (segment_c/total)**2\nprint("Total revenue:", total)\nprint("HHI:", round(hhi, 2))\nprint("Largest segment share (%):", round(segment_a/total*100, 1))',
        "A company reports segments of $40M, $30M, $20M, and $10M. Calculate the HHI and the largest-segment share. Then explain why a 10% group operating margin could still hide a segment with a negative margin.",
        "The shares are 0.40, 0.30, 0.20, and 0.10. The HHI is 0.16 + 0.09 + 0.04 + 0.01 = 0.30. The largest segment is 40% of revenue. A 10% group margin is an average: one segment can lose money while another earns well above 10%. The analyst must reconstruct segment profit to see which part of the group supports the valuation and which part consumes capital.",
        [
            q(
                "Four equal segments produce an HHI of:",
                ["0.25", "0.40", "1.00"],
                0,
                "Each share is 0.25; four squared shares sum to 4 × 0.0625 = 0.25.",
            ),
            q(
                "A group's largest customer is 40% of revenue. The most relevant next question is:",
                [
                    "Whether the customer's logo is well known",
                    "How much profit the customer contributes and what happens at renewal",
                    "Whether the group has more than one product",
                ],
                1,
                "Concentration matters through profit and bargaining power, not through brand recognition.",
            ),
            q(
                "Segment shares are 0.5, 0.3, and 0.2. The HHI is:",
                ["0.38", "0.50", "0.62"],
                0,
                "0.25 + 0.09 + 0.04 = 0.38.",
            ),
        ],
    )

    add(
        "1.29",
        "IX",
        "Cyclical normalization and mid-cycle earnings",
        "Normalize earnings across a full cycle so that a peak-year multiple does not masquerade as a cheap valuation.",
        r"""
## The analytical question

Cyclical companies earn very different profits at different points in the cycle. Capitalizing peak earnings at a low multiple can make an expensive stock look cheap; capitalizing trough earnings can make a sound company look distressed. The analyst needs a **mid-cycle** estimate that reflects the business's through-cycle economics.

One practical approach is to average margins over a full cycle, then apply the average to a normalized revenue base:

$$\text{Normalized EBIT} = \overline{m}_{\text{cycle}} \times \text{Normalized revenue}$$

$$\overline{m}_{\text{cycle}} = \frac{1}{n}\sum_{t=1}^{n} m_t$$

The cycle should include at least one downturn and one recovery. A five-year window is common for industrials; commodity producers may need a longer period. The normalized revenue base should reflect capacity and market share, not the single best year.

The same logic applies to returns on capital. A company that earns 25% ROIC at the top of the cycle may earn 6% at the bottom. Valuation should use a return that the business can sustain, not the peak print.

## A worked example

An industrial company reports EBIT margins of −2%, 4%, 8%, 10%, and 6% over five years. The average margin is:

$$\frac{-2+4+8+10+6}{5}=5.2\%$$

Normalized revenue, based on recent capacity and a mid-cycle volume assumption, is $500 million. Normalized EBIT is $500M × 5.2% = $26 million.

The current year is a peak year: revenue is $550M and the margin is 10%, producing $55M of EBIT. Valuing the company at 8× current EBIT gives an enterprise value of $440M. Valuing it at 8× normalized EBIT gives $208M. The difference is the cyclical illusion: the market may be capitalizing peak earnings, or the analyst may be using a trough multiple. Either way, the comparison must use a consistent basis.

The analyst should present peak, mid-cycle, and trough values. A margin of safety based only on the peak case is not a margin of safety; it is a bet that the cycle stays at its top.

## Research discipline

1. **Choose the cycle explicitly.** State the years, the demand driver, and why the window includes a downturn.
2. **Normalize revenue and margin separately.** Mixing peak revenue with trough margin produces a number that never occurred.
3. **Check capacity and inflation.** A nominal revenue base from ten years ago may need adjustment before it is compared with today's costs.
4. **Value the same business on peak, mid-cycle, and trough earnings** and explain which case anchors the purchase price.
""",
        r"\overline{m}_{\text{cycle}}=\frac{1}{n}\sum_t m_t;\quad \text{Normalized EBIT}=\overline{m}_{\text{cycle}}\times\text{Normalized revenue}",
        'margins = [-0.02, 0.04, 0.08, 0.10, 0.06]\nnormalized_revenue = 500\navg_margin = sum(margins) / len(margins)\nprint("Average cycle margin (%):", round(avg_margin * 100, 1))\nprint("Normalized EBIT:", round(avg_margin * normalized_revenue, 1))\nprint("Peak EBIT at 10% on 550:", 0.10 * 550)',
        "A cyclical company reports margins of 2%, 5%, 7%, 9%, and 12% over five years. Normalized revenue is $400 million. Calculate the average cycle margin and normalized EBIT, then explain why valuing the company on the 12% peak year would overstate its sustainable earning power.",
        "The average margin is (2 + 5 + 7 + 9 + 12) / 5 = 7.0%. Normalized EBIT is 7% × $400M = $28M. The 12% year produces $48M of EBIT, almost 71% more. Capitalizing the peak year assumes the best point of the cycle is permanent, which overstates value and understates the risk of a downturn.",
        [
            q(
                "Five annual EBIT margins are 2%, 4%, 6%, 8%, and 10%. The average is:",
                ["6%", "8%", "10%"],
                0,
                "The sum is 30%, divided by five years, giving 6%.",
            ),
            q(
                "Why is a peak-year EBIT multiple potentially misleading?",
                [
                    "Peak earnings may not be sustainable through the cycle",
                    "Peak earnings are always fraudulent",
                    "Multiples cannot be applied to industrials",
                ],
                0,
                "The multiple may look low because the denominator is temporarily high; normalized earnings are a better anchor.",
            ),
            q(
                "Average cycle margin is 5% and normalized revenue is 600. Normalized EBIT is:",
                ["30", "60", "120"],
                0,
                "0.05 × 600 = 30, so normalized EBIT is $30M.",
            ),
        ],
    )

    add(
        "1.30",
        "IX",
        "Real options, dilution, and contingent claims",
        "Value the claims that sit between debt and common equity, and calculate diluted per-share value under the treasury-stock and if-converted methods.",
        r"""
## The analytical question

A common-equity valuation is a residual claim, but the number of shares entitled to that residual is not always the basic share count. Options, warrants, convertibles, and contingent issuance can transfer value from existing owners. The analyst must model the **fully diluted** claim and the conditions under which additional shares appear.

Under the **treasury-stock method**, options are assumed exercised and the proceeds are used to repurchase shares at the current price:

$$\text{Net new shares}=\text{Options}-\frac{\text{Options}\times\text{Strike}}{\text{Share price}}$$

For a convertible bond, the **if-converted** method adds the shares issuable on conversion and removes the after-tax interest expense from earnings:

$$\text{Diluted EPS}=\frac{\text{Net income}+\text{After-tax interest on convertibles}}{\text{Basic shares}+\text{Shares from conversion}}$$

These are accounting conventions, not necessarily the economic value of the claims. A convertible is a hybrid: it participates in upside while retaining a bond's downside claim. A real-options view treats the conversion feature as a call option on the business, but the analyst still needs a per-share bridge that shows who owns what.

## A worked example

A company has 100 million basic shares. It has 10 million options with a $20 strike, and the share price is $40. The treasury-stock method gives:

$$\text{Net new shares}=10-\frac{10\times20}{40}=10-5=5\text{ million}$$

Diluted shares are 105 million. If the company also has a $50 million convertible bond paying 4% interest, convertible into 2 million shares, and the tax rate is 25%, the if-converted calculation adds $1.5 million of after-tax interest and 2 million shares. Assuming net income of $120 million:

$$\text{Diluted EPS}=\frac{120+1.5}{105+2}=\frac{121.5}{107}\approx\$1.136$$

The basic EPS is $1.20. The difference is not merely arithmetic; it is value transferred to option and convertible holders. A valuation that ignores dilution can overpay for the common shares.

## Research discipline

1. **Read the equity-compensation and convertible notes.** Record strikes, vesting, conversion ratios, and anti-dilution terms.
2. **Use the treasury-stock method for options** and the if-converted method for convertibles, then disclose both basic and diluted figures.
3. **Test the in-the-money condition.** Options and convertibles can move in and out of the money as the share price changes; dilution is state-dependent.
4. **Include contingent issuance** such as earn-outs or performance shares in a scenario, not as a certainty.
""",
        r"\text{Net new shares}=N_o-\frac{N_o K}{P};\quad \text{Diluted EPS}=\frac{\text{NI}+\text{AT interest}}{N_b+N_c}",
        'basic = 100\noptions = 10\nstrike = 20\nprice = 40\nnet_new = options - options * strike / price\nprint("Diluted shares:", basic + net_new)\nnet_income = 120\nconvert_interest = 50 * 0.04 * (1 - 0.25)\nprint("Diluted EPS:", round((net_income + convert_interest) / (basic + net_new + 2), 3))',
        "A company has 200 million basic shares, 20 million options with a $25 strike, and a $50 share price. Calculate diluted shares under the treasury-stock method. Then explain why a convertible bond's dilution depends on the share price.",
        "Proceeds are 20M × $25 = $500M; at $50 per share, the company can repurchase 10M shares. Net new shares are 20M − 10M = 10M, so diluted shares are 210M. A convertible's dilution depends on the share price because conversion is optional: holders convert when the conversion value exceeds the bond's value, so the shares appear only in the states where the equity is valuable.",
        [
            q(
                "Basic shares are 100, options are 10 at a 20 strike, and the price is 40. Treasury-stock diluted shares are:",
                ["105", "110", "115"],
                0,
                "Net new shares are 10 − (10 × 20 / 40) = 5; diluted shares are 105.",
            ),
            q(
                "The if-converted method for a convertible bond generally:",
                [
                    "Adds the conversion shares and adds back after-tax interest",
                    "Ignores the bond entirely",
                    "Subtracts the conversion shares",
                ],
                0,
                "It treats the bond as if converted, adding shares and removing the interest expense.",
            ),
            q(
                "Basic shares are 50, options are 5 at a 10 strike, and the price is 20. Net new shares are:",
                ["2.5", "5", "7.5"],
                0,
                "5 − (5 × 10 / 20) = 5 − 2.5 = 2.5 million net new shares.",
            ),
        ],
    )

    add(
        "1.31",
        "IX",
        "Capstone: advanced red-team investment committee",
        "Reconcile scenario values, dilution, hidden claims, and accounting quality into a red-team memo with an explicit decision rule.",
        r"""
## The analytical question

The classical capstone asked whether one conservative valuation supported a purchase. The advanced capstone adds the questions a red team should ask before capital is committed:

1. **Is the earnings base clean?** Have accruals, nonrecurring items, and hidden claims been reconciled?
2. **Is the valuation internally consistent?** Are the cash flows, discount rate, and share count describing the same claim?
3. **What would have to be true for the thesis to fail?** Which observable event would falsify it?
4. **Does the price compensate for the range of outcomes**, not merely the base case?

A useful synthesis is a probability-weighted value beside a strict downside price ceiling:

$$V_{\text{expected}}=\sum_j p_j V_j,\qquad \sum_j p_j=1$$

$$P_{\max}=V_{\text{bear}}\times(1-M_{\text{required}})$$

The expected value answers "what is a fair bet?" The downside ceiling answers "what price protects me if the bear case is the one that happens?" A disciplined committee uses both and explains when they disagree.

## A worked example

An advanced manufacturing company has 10 million diluted shares and net debt of $30 million. The team builds three operating cases:

| Case | Free cash flow | EV multiple | Enterprise value | Equity value | Per share |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Bear | $8M | 10× | $80M | $50M | $5.00 |
| Base | $12M | 12× | $144M | $114M | $11.40 |
| Bull | $16M | 14× | $224M | $194M | $19.40 |

Assign probabilities of 30%, 50%, and 20%. Expected equity value per share is:

$$0.30(5.00)+0.50(11.40)+0.20(19.40)=1.50+5.70+3.88=\$11.08$$

The market price is $9.00. The stock trades at an 18.8% discount to expected value, which may look attractive. But the bear-case value is $5.00, and a 30% margin of safety against that case gives a maximum price of $3.50. At $9.00, the investor is paying a large premium to the downside value and relying on the base and bull cases.

The committee's decision rule matters. A mandate that prioritizes capital preservation rejects the purchase at $9.00 and places the company on a watchlist with a review trigger: either the price falls toward $3.50 or the bear-case cash flow improves with evidence. A mandate that explicitly accepts probability-weighted risk might buy a small position, but it must disclose that the downside case is not protected by the price.

## Research discipline

1. **Use the same share count and net-debt bridge in every scenario.** A valuation that changes the balance sheet between cases is not comparable.
2. **Separate operating uncertainty from financing claims.** Hidden liabilities, dilution, and pension deficits belong in every case.
3. **Pre-register the falsification triggers.** Identify the specific filing, margin, or cash-flow observation that would move the bear case.
4. **Write the memo for a dissenting reader.** State the strongest counterargument and why the decision still holds, or change the decision.
""",
        r"V_{\text{expected}}=\sum_j p_jV_j;\quad P_{\max}=V_{\text{bear}}(1-M_{\text{required}})",
        'bear = 5.00\nbase = 11.40\nbull = 19.40\nexpected = 0.30*bear + 0.50*base + 0.20*bull\nprice = 9.00\nprint("Expected value per share:", round(expected, 2))\nprint("Discount to expected (%):", round((1 - price/expected)*100, 1))\nprint("Bear-case price ceiling:", round(bear*0.70, 2))',
        "A company has 8 million diluted shares and $20 million of net debt. Bear, base, and bull free cash flows are $6M, $10M, and $14M; the EV multiples are 10×, 12×, and 14×; the probabilities are 25%, 50%, and 25%. Calculate each per-share value, the expected value, and the bear-case price ceiling at a 30% margin of safety.",
        "Bear: EV $60M − $20M = $40M, or $5.00 per share. Base: $120M − $20M = $100M, or $12.50. Bull: $196M − $20M = $176M, or $22.00. Expected value is 0.25(5.00) + 0.50(12.50) + 0.25(22.00) = $13.00. The bear-case ceiling is $5.00 × 0.70 = $3.50. The gap between expected value and the downside ceiling is the central committee debate.",
        [
            q(
                "Why does the advanced capstone report both expected value and a bear-case price ceiling?",
                [
                    "They answer different questions: a fair probability-weighted value and a capital-preservation limit",
                    "They must always be equal",
                    "The ceiling replaces the need for scenarios",
                ],
                0,
                "Expected value describes a bet; the downside ceiling describes protection if the bear case occurs.",
            ),
            q(
                "Bear value is $6.00 and the required margin of safety is 25%. The maximum price is:",
                ["$4.50", "$6.00", "$7.50"],
                0,
                "6.00 × (1 − 0.25) = $4.50.",
            ),
            q(
                "A memo's bull case depends on a customer contract that has not been signed. The most appropriate treatment is:",
                [
                    "Include it in the base case as certain",
                    "Put it in a scenario with an explicit probability and a falsification trigger",
                    "Ignore every scenario and use the current price",
                ],
                1,
                "An unsigned contract is a contingent outcome; scenario weight and a review trigger make the assumption auditable.",
            ),
        ],
    )

    # -------------------------------------------------------------------------
    # CHECKPOINTS
    # -------------------------------------------------------------------------

    checkpoints = [
        (
            "Checkpoint · evidence and bond protection",
            [
                (
                    "1.1",
                    q(
                        "A conservative estimate is 50 and required discount 20%. Maximum price is:",
                        ["30", "40", "45"],
                        1,
                        "50 × 0.80 = 40 under the stated margin-of-safety rule.",
                    ),
                ),
                (
                    "1.2",
                    q(
                        "Weak EBIT is 35 and interest 7. Coverage is:",
                        ["3", "4", "5"],
                        2,
                        "35 / 7 = 5 times; use the weak-case numerator supplied.",
                    ),
                ),
                (
                    "1.8",
                    q(
                        "A pool realizes 90 net of costs, ahead of senior debt 70 and junior debt 40. Junior recovery is:",
                        ["50%", "100%", "25%"],
                        0,
                        "20 remains after the senior claim, giving 20 / 40 = 50%.",
                    ),
                ),
                (
                    "1.10",
                    q(
                        "Pay 100 today and receive 104 in one year including coupon and principal. Promised return is:",
                        ["2%", "4%", "104%"],
                        1,
                        "The gain is 4 on a cost of 100, before default effects and costs.",
                    ),
                ),
            ],
        ),
        (
            "Checkpoint · senior and common ownership",
            [
                (
                    "1.11",
                    q(
                        "Annual cumulative preference is 2, with one year in arrears. Current preference also comes first. How much of a distribution of 7 remains?",
                        ["3", "5", "7"],
                        0,
                        "Arrears and current preference total 4, leaving 3 for common under these terms.",
                    ),
                ),
                (
                    "1.12",
                    q(
                        "A bond converts into 30 shares at a stock price of 25. Conversion value is:",
                        ["300", "750", "1,000"],
                        1,
                        "30 shares × 25 per share = 750 of immediate conversion value.",
                    ),
                ),
                (
                    "1.13",
                    q(
                        "A firm retains 16 and adds 2 of recurring annual profit. Implied incremental return is:",
                        ["8%", "10%", "12.5%"],
                        2,
                        "2 / 16 = 12.5%, subject to the profit and investment assumptions.",
                    ),
                ),
                (
                    "1.14",
                    q(
                        "Value is 120 across 12 shares; 20 of excess cash repurchases shares at 5. Remaining value per share is:",
                        ["10", "12.50", "15"],
                        1,
                        "Four shares retire; remaining value 100 divided by 8 shares is 12.50.",
                    ),
                ),
            ],
        ),
        (
            "Checkpoint · earnings and asset evidence",
            [
                (
                    "1.3",
                    q(
                        "Reported EPS of 9 includes a 4 after-tax isolated gain. Recurring EPS with no other adjustments is:",
                        ["5", "9", "13"],
                        0,
                        "Subtract the isolated gain: 9 − 4 = 5.",
                    ),
                ),
                (
                    "1.17",
                    q(
                        "Profit is 18, depreciation 2, and net operating working capital rises 5. Simplified operating cash is:",
                        ["11", "15", "25"],
                        1,
                        "18 + 2 − 5 = 15 before any other adjustments.",
                    ),
                ),
                (
                    "1.4",
                    q(
                        "Current assets 90, all liabilities 55, preferred claims 5, and 6 shares imply NCAV per share of:",
                        ["15", "10", "5"],
                        2,
                        "(90 − 55 − 5) / 6 = 5 per common share.",
                    ),
                ),
                (
                    "1.19",
                    q(
                        "Assets 180 include goodwill 40; liabilities are 110. Tangible equity is:",
                        ["30", "70", "110"],
                        0,
                        "180 − 110 − 40 = 30; economic recovery still needs investigation.",
                    ),
                ),
            ],
        ),
        (
            "Checkpoint · price discrepancies and decisions",
            [
                (
                    "1.18",
                    q(
                        "An asset surplus of 18 faces total burn of 5 and incremental costs of 4. Residual before discounting is:",
                        ["9", "13", "14"],
                        0,
                        "18 − 5 − 4 = 9; a timing adjustment may reduce present value further.",
                    ),
                ),
                (
                    "1.20",
                    q(
                        "Enterprise value 144 and normalized EBIT 18 imply which multiple?",
                        ["6", "8", "12"],
                        1,
                        "144 / 18 = 8 times normalized EBIT.",
                    ),
                ),
                (
                    "1.21",
                    q(
                        "A claim costs 18, pays 24 on success and 9 on failure. Break-even probability is:",
                        ["40%", "50%", "60%"],
                        2,
                        "(18 − 9) / (24 − 9) = 9 / 15 = 60%, before time and costs.",
                    ),
                ),
                (
                    "1.22",
                    q(
                        "A 3% position suffers a 60% loss, other holdings unchanged. Portfolio loss is:",
                        ["1.8%", "3%", "60%"],
                        0,
                        "0.03 × 0.60 = 0.018, or 1.8% of starting portfolio value.",
                    ),
                ),
            ],
        ),
    ]

    return finish(
        {
            "id": "security-analysis",
            "number": 1,
            "title": "Security Analysis",
            "description": "Study Graham & Dodd through creditor protection, earning power, asset values, and a complete investment committee case.",
            "source": "Benjamin Graham & David Dodd · Security Analysis · 1940 edition",
            "level": "Intermediate",
            "icon": "book",
            "modules": modules,
            "prerequisites": "Start with Trading & market fundamentals or equivalent knowledge. Comfort with ratios and basic financial statements helps; Python is optional.",
            "outcomes": [
                "Build a dated evidence file and a conservative valuation range.",
                "Assess bonds, preferred shares, convertibles, and common-owner claims.",
                "Normalize earnings and reconcile asset, cash-flow, and per-share values.",
                "Write and challenge an investment memo with explicit price and review rules.",
            ],
            "readingGuide": "Use your own copy of the 1940 edition alongside the seven book-aligned units. The publisher's sixth-edition contents also preserves the seven-part organization around the historical text. Unit VIII is a clearly separated course extension. These are original teaching cases and exercises, not reproduced chapters or publisher exam questions. Allow additional time for the book readings and written assignments beyond the displayed lesson estimates.",
            "references": [
                {"title": "1940 edition · publisher reference", "url": BOOK},
                {"title": "Seven-part organization · publisher contents", "url": STRUCTURE},
            ],
            "parts": [
                {"id": id, "title": title, "description": desc}
                for id, title, desc in [
                    (
                        "I",
                        "The analyst's method",
                        "Evidence, investment judgment, and uncertainty · book Part I",
                    ),
                    (
                        "II",
                        "Protecting a fixed claim",
                        "Coverage, priority, covenants, and promised return · book Part II",
                    ),
                    (
                        "III",
                        "Preferred and convertible claims",
                        "Participation, arrears, conversion, and dilution · book Part III",
                    ),
                    (
                        "IV",
                        "The common owner's interest",
                        "Distributions, retention, and share-count changes · book Part IV",
                    ),
                    (
                        "V",
                        "Interrogate reported earnings",
                        "Normalization, capital consumption, inventory, and cash conversion · book Part V",
                    ),
                    (
                        "VI",
                        "Assets and their realizability",
                        "NCAV, hidden claims, cash burn, and book-value limits · book Part VI",
                    ),
                    (
                        "VII",
                        "Comparison and the investment decision",
                        "Peer analysis, contingent events, and monitored decisions · book Part VII",
                    ),
                    (
                        "VIII",
                        "Modern bridges and capstone",
                        "Separate extensions, model critique, and an original committee case",
                    ),
                    (
                        "IX",
                        "Advanced forensic and valuation synthesis",
                        "Accrual forensics, manipulation screens, hidden claims, concentration, cyclical normalization, dilution, and a red-team capstone",
                    ),
                ]
            ],
        },
        checkpoints,
        version=3,
    )
