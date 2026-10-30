"""Credit analysis and distressed securities course (16.x)."""

from advanced_security_common import finish, make_add, q

READING = (
    "Advanced security analysis · credit and distress. Read the credit agreement, maturity schedule, "
    "and liquidation waterfall beside this lesson. The worked figures are teaching numbers; the cited "
    "primary source supplies the real-world context."
)


def build_credit_distress():
    modules = []
    add = make_add(modules, READING)

    add(
        "16.1",
        "I",
        "Cash-flow coverage through the cycle",
        "Measure interest and free-cash-flow coverage at peak, mid-cycle, and trough, and distinguish accounting EBITDA from cash available to creditors.",
        r"""
## The analytical question

A credit investor is paid from cash, not from EBITDA. Coverage ratios are useful only when the numerator is a defensible measure of cash available to service debt and the denominator includes every fixed claim. The analyst should compute coverage at several points in the cycle, because a ratio that looks comfortable at the top can disappear in a downturn.

Two core measures are:

$$\text{Interest coverage}=\frac{\text{EBITDA}}{\text{Interest expense}}$$

$$\text{FCF to debt}=\frac{\text{EBITDA}-\text{Interest}-\text{Taxes}-\text{Maintenance capex}}{\text{Total debt}}$$

EBITDA is not cash flow. It ignores working-capital investment, maintenance capital spending, and cash taxes. A company with high EBITDA and heavy maintenance needs can have weak free cash flow. The analyst should reconcile EBITDA to operating cash flow and then subtract the capital spending required to keep the business running.

## A worked example

A manufacturer reports EBITDA of $100M, interest of $25M, cash taxes of $10M, maintenance capex of $30M, and total debt of $300M. Interest coverage is 4.0×. Free cash flow to debt is:

$$\frac{100-25-10-30}{300}=\frac{35}{300}=11.7\%$$

In a trough, EBITDA falls to $60M while interest and maintenance spending remain. Coverage falls to 2.4×, and free cash flow becomes $60 − 25 − 10 − 30 = −$5M. The company can still pay interest from cash balances for a while, but it is no longer generating cash to reduce debt.

The analyst should present peak, mid-cycle, and trough coverage side by side, with the assumptions that produced each case. A covenant that permits 4.0× may look safe at peak and bind quickly in a downturn. The relevant question is not only "can the company pay today?" but "how much EBITDA can fall before liquidity or a covenant becomes the constraint?"

## Research discipline

1. **Use cash taxes and maintenance capex**, not reported depreciation alone, in free-cash-flow coverage.
2. **Include leases and other fixed charges** in the denominator where the credit agreement treats them as debt-like.
3. **Model a trough**, not only a base case. A credit analysis that assumes the cycle never turns is not a credit analysis.
4. **Reconcile EBITDA to operating cash flow** and disclose every adjustment.
""",
        r"\text{Interest coverage}=\frac{\text{EBITDA}}{\text{Interest}};\quad \text{FCF/debt}=\frac{\text{EBITDA}-\text{Interest}-\text{Tax}-\text{Maint. capex}}{\text{Debt}}",
        'ebitda = 100\ninterest = 25\ntaxes = 10\ncapex = 30\ndebt = 300\nfcf = ebitda - interest - taxes - capex\nprint("Interest coverage:", ebitda/interest)\nprint("FCF to debt (%):", round(fcf/debt*100, 1))\ntrough = 60\ntrough_fcf = trough - interest - taxes - capex\nprint("Trough interest coverage:", trough/interest)\nprint("Trough FCF:", trough_fcf)',
        "A company reports EBITDA of $120M, interest of $30M, cash taxes of $12M, maintenance capex of $36M, and debt of $360M. Calculate interest coverage and FCF to debt. Then calculate both measures if EBITDA falls to $72M.",
        "Base interest coverage is 120/30 = 4.0×; FCF to debt is (120 − 30 − 12 − 36)/360 = 42/360 = 11.7%. At trough EBITDA of $72M, coverage is 2.4× and FCF is 72 − 30 − 12 − 36 = −$6M. The company can service interest but is cash-flow negative after maintenance spending, so liquidity and covenant headroom become central.",
        [
            q(
                "EBITDA is 90 and interest is 30. Interest coverage is:",
                ["2×", "3×", "4×"],
                1,
                "Interest coverage is 90 / 30 = 3×.",
            ),
            q(
                "Free cash flow to debt is most useful when it includes:",
                ["Only EBITDA", "Interest, taxes, and maintenance capex", "Dividends paid"],
                1,
                "Creditors are paid after taxes and the capex needed to keep the business running.",
            ),
            q(
                "EBITDA is 80, interest 20, taxes 10, maintenance capex 20, and debt 200. FCF to debt is:",
                ["10%", "15%", "20%"],
                1,
                "(80 − 20 − 10 − 20) / 200 = 30 / 200 = 15%.",
            ),
        ],
    )

    add(
        "16.2",
        "I",
        "Capital structure and the recovery waterfall",
        "Rank claims by priority and calculate recovery for each tranche under a stressed asset value.",
        r"""
## The analytical question

When a company cannot pay its debts, value is distributed in a legal order. Secured creditors are paid from their collateral; administrative claims and taxes often rank ahead of unsecured creditors; subordinated debt and preferred shares sit behind them; common equity receives the residual. The analyst's task is to build a **waterfall** that shows how much each tranche recovers under a given asset value.

$$\text{Recovery}_i=\frac{\max\left(0,\min\left(\text{Claim}_i,\text{Pool}_i\right)\right)}{\text{Claim}_i}$$

where the pool available to tranche $i$ is what remains after all higher claims and administrative costs. The **fulcrum security** is the tranche that is partly paid and therefore captures the marginal value of the enterprise. It is often the most interesting claim for a distressed investor.

## A worked example

A distressed company has a liquidation pool of $180M before administrative costs of $20M. Its claims are $120M of secured debt, $60M of senior unsecured notes, and $50M of subordinated notes.

The pool after administration is $160M. The secured claim is paid in full, leaving $40M. The senior unsecured notes recover $40M / $60M = 66.7%. The subordinated notes recover nothing. The fulcrum security is the senior unsecured note: it is the tranche whose recovery changes most directly with the enterprise value.

If the pool improves to $220M, the subordinated notes begin to recover. The analyst should show a table of enterprise values and recoveries rather than a single point estimate, because the fulcrum can move between tranches as value changes. Legal priority, intercreditor agreements, and collateral coverage can complicate the simple waterfall; the analyst must read the documents rather than assume the labels.

## Research discipline

1. **Map the capital structure** from the credit agreement and indentures, including guarantees and collateral.
2. **Include administrative, tax, and priority claims** before distributing value to prepetition creditors.
3. **Identify the fulcrum security** and test how it changes across a range of asset values.
4. **Separate legal priority from economic bargaining power.** A weak lien or a contested claim can change the outcome.
""",
        r"\text{Recovery}_i=\frac{\max(0,\min(\text{Claim}_i,\text{Pool after senior claims}))}{\text{Claim}_i}",
        'pool = 180\nadmin = 20\nsecured = 120\nunsecured = 60\nsubordinated = 50\navailable = pool - admin\nsecured_recovery = min(secured, available)\nremaining = available - secured_recovery\nprint("Available after admin:", available)\nprint("Secured recovery (%):", round(secured_recovery / secured * 100, 1))\nprint("Unsecured recovery (%):", round(min(unsecured, remaining) / unsecured * 100, 1))\nprint("Subordinated recovery (%):", round(max(0, remaining - unsecured) / subordinated * 100, 1))',
        "A company has a $140M pool, $15M of administrative claims, $100M of secured debt, $50M of senior unsecured notes, and $40M of subordinated notes. Calculate recovery for each tranche and identify the fulcrum security.",
        "Available after administration is $125M. The secured debt recovers 100%, leaving $25M. Senior unsecured recovers 25/50 = 50%. Subordinated recovers nothing. The fulcrum security is the senior unsecured note because it is partly paid and absorbs the next increment of value.",
        [
            q(
                "In a liquidation waterfall, secured debt generally ranks:",
                ["Behind common equity", "Ahead of unsecured debt to the extent of collateral", "After subordinated debt"],
                1,
                "Secured creditors have a claim on their collateral ahead of unsecured creditors.",
            ),
            q(
                "A $60M pool remains after senior claims, and a $90M unsecured tranche is next. Its recovery is:",
                ["33.3%", "66.7%", "100%"],
                1,
                "The unsecured recovery is 60 / 90 = 66.7%.",
            ),
            q(
                "The fulcrum security is best described as the tranche that:",
                ["Is always paid in full", "Is partly paid and captures marginal enterprise value", "Has the largest face amount"],
                1,
                "The fulcrum is the tranche whose recovery changes most directly with enterprise value.",
            ),
        ],
    )

    add(
        "16.3",
        "I",
        "Covenants, liquidity, and maturity walls",
        "Translate covenant thresholds, cash burn, and debt maturities into a concrete liquidity runway and breach scenario.",
        r"""
## The analytical question

A credit can look adequately covered on an income statement and still fail because cash arrives at the wrong time. The analyst needs to combine three clocks: the **covenant clock**, the **liquidity clock**, and the **maturity clock**. A company may have years before a bond matures but only months of covenant headroom.

Covenant headroom is often expressed in EBITDA terms:

$$\text{Maximum debt}=\text{Covenant multiple}\times\text{EBITDA}$$

$$\text{EBITDA headroom}=\text{Current EBITDA}-\frac{\text{Current debt}}{\text{Covenant multiple}}$$

Liquidity runway is:

$$\text{Runway}=\frac{\text{Unrestricted cash}+\text{Available revolver}}{\text{Monthly cash burn}}$$

The maturity wall is the schedule of principal repayments by year. A large maturity in a weak market can force refinancing at a higher cost or a distressed exchange.

## A worked example

A company has $300M of debt, EBITDA of $80M, and a leverage covenant of 4.0×. Current leverage is 3.75×. Maximum debt at the covenant is $320M, so the company has $20M of debt headroom, equivalent to $5M of EBITDA headroom because the covenant is 4×. If EBITDA falls to $70M, leverage rises to 4.29× and the covenant is breached unless the lender grants a waiver.

Liquidity is $40M of cash plus $30M of revolver availability, or $70M. Monthly cash burn in a stress case is $15M, giving a runway of about 4.7 months. The maturity schedule shows $50M due in 2026, $100M in 2027, and $150M in 2028. The 2027 maturity is the critical refinancing event.

The analyst should present the three clocks together. A covenant breach can accelerate maturities even if the company could otherwise pay them. A short runway can force asset sales at distressed prices. A maturity wall concentrates refinancing risk in a single year. The credit decision depends on which clock runs out first.

## Research discipline

1. **Read the covenant definitions**, not just the threshold. EBITDA add-backs and debt exclusions can change the calculation.
2. **Use unrestricted cash and actual revolver availability**, not the full commitment if the borrowing base is constrained.
3. **Model a stress case** with lower EBITDA, slower collections, and no new financing.
4. **Map every maturity and amortization payment** and identify the first refinancing date.
""",
        r"\text{Max debt}=\text{Covenant}\times\text{EBITDA};\quad \text{Runway}=\frac{\text{Cash}+\text{Revolver}}{\text{Monthly burn}}",
        'debt = 300\nebitda = 80\ncovenant = 4.0\nprint("Current leverage:", debt/ebitda)\nprint("Maximum debt:", covenant*ebitda)\nprint("Debt headroom:", covenant*ebitda - debt)\nprint("EBITDA headroom:", ebitda - debt/covenant)\nstress_ebitda = 70\nprint("Stress leverage:", round(debt/stress_ebitda, 2))\nprint("Liquidity runway (months):", round((40 + 30)/15, 1))',
        "A company has $240M of debt, EBITDA of $80M, and a 3.5× leverage covenant. It holds $25M of cash, has $20M of revolver availability, and burns $12M a month in a stress case. Its next maturity is $60M in 18 months. Calculate current and maximum leverage, debt and EBITDA headroom, and liquidity runway. Which clock is most pressing?",
        "Current leverage is 240/80 = 3.0×. Maximum debt is 3.5 × 80 = $280M, so headroom is $40M of debt, or about $11.4M of EBITDA before the covenant binds. Liquidity is $45M / $12M = 3.75 months. The liquidity clock is the most pressing: the company runs out of cash long before the 18-month maturity, unless it cuts burn or raises new funding.",
        [
            q(
                "Debt is 180, EBITDA is 60, and the covenant is 3.0×. The company is:",
                ["At the covenant exactly", "Above the covenant", "Below the covenant"],
                0,
                "180 / 60 = 3.0×, exactly at the threshold; any EBITDA decline would breach it.",
            ),
            q(
                "Liquidity runway is cash plus available revolver divided by:",
                ["Annual revenue", "Monthly cash burn", "Total debt"],
                1,
                "Runway measures how long available liquidity lasts at a given burn rate.",
            ),
            q(
                "Cash is 30, revolver availability is 15, and monthly burn is 15. Runway is:",
                ["2 months", "3 months", "45 months"],
                1,
                "(30 + 15) / 15 = 3 months.",
            ),
        ],
    )

    add(
        "16.4",
        "II",
        "Distressed valuation: going concern versus liquidation",
        "Value a distressed business on both a going-concern and a liquidation basis, and explain which one governs the investment decision.",
        r"""
## The analytical question

A distressed company has two very different values: the value of continuing to operate, and the value of selling its assets and paying claims. The going-concern value depends on cash flows, restructuring costs, and the time needed to stabilize the business. The liquidation value depends on asset recoveries, selling costs, and legal priority. The analyst should calculate both and explain which is more credible.

$$\text{Going-concern equity}=\text{Enterprise value}-\text{Net debt}-\text{Restructuring costs}$$

$$\text{Liquidation residual}=\sum_i \text{Asset}_i\times\text{Recovery}_i-\text{Liabilities}-\text{Administrative costs}$$

The going-concern value is usually higher, but it is also conditional: it requires liquidity, customer retention, and a viable operating plan. A liquidation analysis sets a floor, though that floor can be lower than the reported book value suggests.

## A worked example

A retailer has a going-concern enterprise value of $180M and $100M of debt, implying $80M of equity value before restructuring costs. The analyst assumes $20M of restructuring costs, reducing going-concern equity to $60M.

On a liquidation basis, the company has $20M of cash, $40M of receivables recovering 80%, $60M of inventory recovering 50%, and $120M of property recovering 30%. Realized assets are $20 + $32 + $30 + $36 = $118M. After $15M of administrative costs and $100M of debt, the residual is $3M.

The equity is worth far more as a going concern than in liquidation, but the going-concern case depends on executing a turnaround. The analyst should ask how much liquidity is needed, how much time the plan requires, and what happens if customers leave. A distressed investor may buy the debt rather than the equity, because the debt's recovery is protected by the liquidation value while the equity's upside depends on a successful restructuring.

## Research discipline

1. **Use realistic recovery rates** by asset class and explain the assumptions. A liquidation analysis with optimistic receivables and inventory is not a floor.
2. **Include restructuring and administrative costs**, which can consume a large share of a small residual.
3. **Test the going-concern plan's liquidity and timing.** A plan that runs out of cash before it works is not a going concern.
4. **Identify which security you are valuing.** The equity, the fulcrum debt, and the secured debt have different sensitivities to the same enterprise value.
""",
        r"\text{Going-concern equity}=\text{EV}-\text{Debt}-\text{Restructuring};\quad \text{Liquidation residual}=\sum \text{Asset}_i r_i-\text{Liabilities}-\text{Admin}",
        'ev = 180\ndebt = 100\nrestructuring = 20\nprint("Going-concern equity:", ev - debt - restructuring)\nrealized = 20 + 40*0.8 + 60*0.5 + 120*0.3\nprint("Realized assets:", realized)\nprint("Liquidation residual:", realized - 15 - debt)',
        "A company has a going-concern EV of $250M, debt of $160M, and restructuring costs of $30M. Its liquidation realizations are cash $25M, receivables $50M at 70%, inventory $80M at 40%, and fixed assets $180M at 25%. Administrative costs are $20M. Calculate going-concern equity and the liquidation residual. Which value would you use to anchor a secured-debt investment?",
        "Going-concern equity is 250 − 160 − 30 = $60M. Liquidation realizations are 25 + 35 + 32 + 45 = $137M; after $20M of administrative costs and $160M of debt, the residual is −$43M. The liquidation value suggests the debt is not fully covered, so a secured-debt investor should anchor on the collateral recovery, not the going-concern equity. The going-concern case may still support a restructuring, but it requires new liquidity and execution.",
        [
            q(
                "A liquidation analysis is most useful as:",
                ["A guarantee of recovery", "A stressed floor for claims", "A forecast of going-concern cash flow"],
                1,
                "It estimates recoveries under a sale of assets, setting a floor that may still be uncertain.",
            ),
            q(
                "Going-concern EV is 200, debt is 120, and restructuring costs are 25. Going-concern equity is:",
                ["55", "80", "105"],
                0,
                "Going-concern equity is 200 − 120 − 25 = 55.",
            ),
            q(
                "Which cost is often omitted when analysts overstate a liquidation residual?",
                ["Administrative and restructuring costs", "Cash balances", "Secured debt"],
                0,
                "Administrative costs and professional fees can consume a large part of a small residual.",
            ),
        ],
    )

    add(
        "16.5",
        "II",
        "Credit spreads, yields, and expected loss",
        "Relate bond price, yield, spread, probability of default, and loss given default into a coherent credit return.",
        r"""
## The analytical question

A credit investor earns a spread for bearing default and recovery risk. The yield to maturity summarizes the promised return if the issuer pays in full. The spread over a risk-free bond is compensation for expected loss plus a risk premium and liquidity premium. A wide spread can be attractive or can signal that the market expects a default the analyst has not modeled.

The promised yield solves:

$$P=\sum_{t=1}^{T}\frac{C}{(1+y)^t}+\frac{F}{(1+y)^T}$$

Expected loss is approximately:

$$\text{Expected loss}=\text{Probability of default}\times\text{Loss given default}$$

A simple spread compensation is expected loss plus a risk premium. The analyst should not treat the promised yield as an expected return; if default occurs, the realized return is the recovery value, not the coupon.

## A worked example

A two-year bond with a $100 face value and a 6% annual coupon trades at $90. The promised yield is approximately 11.9%, because the cash flows of $6 and $106 discounted at that rate produce about $90. If a comparable risk-free bond yields 5%, the credit spread is about 6.9 percentage points.

Suppose the analyst estimates an 8% probability of default over the period and a 60% loss given default. Expected loss is 0.08 × 0.60 = 4.8%. The spread of 6.9% covers expected loss and leaves about 2.1 percentage points for risk, liquidity, and estimation error. That may be adequate or not, depending on the uncertainty in the default estimate and the recovery assumptions.

The analysis should include a stress case in which default probability doubles or recovery falls. A bond that looks adequately compensated in the base case can be unattractive when the loss distribution is wide. The investor should also consider the covenant package, the maturity, and the liquidity of the bond.

## Research discipline

1. **Distinguish promised yield from expected return.** The coupon is not received in the default state.
2. **Estimate default probability and recovery from evidence**, not from the spread alone. The market may be wrong or may be pricing a different scenario.
3. **Include liquidity and risk premiums** in the spread decomposition.
4. **Stress default and recovery together.** They are not independent in many crises.
""",
        r"P=\sum_t\frac{C}{(1+y)^t}+\frac{F}{(1+y)^T};\quad \text{Expected loss}=PD\times LGD",
        'face = 100\ncoupon = 6\nprice = 90\nyears = 2\nlow = 0.0\nhigh = 1.0\nfor i in range(80):\n    mid = (low + high)/2\n    value = 0.0\n    for t in range(1, years + 1):\n        value = value + coupon/(1 + mid)**t\n    value = value + face/(1 + mid)**years\n    if value > price:\n        low = mid\n    else:\n        high = mid\nprint("Promised yield (%):", round(mid*100, 2))\nprint("Expected loss (%):", 0.08*0.60*100)',
        "A two-year bond with a $100 face value and a 5% coupon trades at $92. The risk-free rate is 4%. Estimate the promised yield approximately, calculate the spread, and compute expected loss if the default probability is 6% and loss given default is 55%. Does the spread cover expected loss?",
        "At about 9.5%, the cash flows of $5 and $105 discount to roughly $92; the spread over 4% is about 5.5 percentage points. Expected loss is 0.06 × 0.55 = 3.3%. The spread covers expected loss and leaves about 2.2 percentage points for risk, liquidity, and error. The analyst should stress a higher default probability and a lower recovery before concluding the bond is attractive.",
        [
            q(
                "A bond's promised yield is 10% and the risk-free rate is 4%. The approximate spread is:",
                ["4%", "6%", "14%"],
                1,
                "10% − 4% = 6 percentage points.",
            ),
            q(
                "Expected credit loss is calculated as:",
                ["Coupon times maturity", "Probability of default times loss given default", "Price minus face value"],
                1,
                "Expected loss combines the chance of default with the share lost in that state.",
            ),
            q(
                "Default probability is 5% and loss given default is 40%. Expected loss is:",
                ["2%", "5%", "20%"],
                0,
                "0.05 × 0.40 = 0.02, or 2%.",
            ),
        ],
    )

    add(
        "16.6",
        "II",
        "The distressed playbook and catalyst analysis",
        "Map claims, liquidity, catalysts, and the fulcrum security into a distressed investment process with explicit legal and timing risk.",
        r"""
## The analytical question

Distressed investing is a process, not a single valuation. The analyst must answer five questions: Who is owed what? What liquidity does the company have? What event will force a restructuring or a sale? Which security is the fulcrum? What legal jurisdiction and process will govern the outcome?

A compact catalyst map links the event to the waterfall:

$$\text{Recovery}_i=\frac{\max(0,\min(\text{Claim}_i,\text{Proceeds after senior claims}))}{\text{Claim}_i}$$

The catalyst might be a maturity the company cannot refinance, a covenant breach, an asset sale, a litigation outcome, or a strategic buyer. The analyst should assign a date and a probability to each catalyst, then value the fulcrum security under the resulting scenarios.

## A worked example

A company has $20M of cash, $60M of secured debt, and $40M of unsecured notes. A strategic buyer has offered $50M for the business, and administrative costs are $10M. Total proceeds are $70M; after administration, $60M is available. The secured debt recovers 100%, and the unsecured notes recover nothing.

If the buyer raises the offer to $90M, proceeds after administration are $80M; the secured debt is paid in full and the unsecured notes recover $20M / $40M = 50%. The unsecured note is the fulcrum security in the improved scenario. The analyst should compare the current market price of the unsecured notes with the probability-weighted recovery, then subtract the legal and timing costs.

The process risk matters. A sale may take a year, during which professional fees and employee attrition reduce value. A creditor committee may challenge the waterfall. A court may subordinate a claim. The analyst should model the recovery net of these costs and state the legal assumptions explicitly.

## Research discipline

1. **Build the claim map from the credit agreements and court filings**, not from memory or press summaries.
2. **Identify the catalyst and its date.** A cheap security with no catalyst can stay cheap for years.
3. **Value the fulcrum security**, not the equity, when the capital structure is distressed.
4. **Model legal and timing costs**, and disclose the jurisdiction and process assumptions.
""",
        r"\text{Recovery}_i=\frac{\max(0,\min(\text{Claim}_i,\text{Proceeds after senior claims}))}{\text{Claim}_i}",
        'cash = 20\nsale = 50\nadmin = 10\nsecured = 60\nunsecured = 40\nproceeds = cash + sale\navailable = proceeds - admin\nsecured_paid = min(secured, available)\nremaining = available - secured_paid\nprint("Proceeds:", proceeds)\nprint("Available after admin:", available)\nprint("Secured recovery (%):", round(secured_paid/secured*100, 1))\nprint("Unsecured recovery (%):", round(min(unsecured, remaining)/unsecured*100, 1))',
        "A company has $15M of cash, a $70M asset-sale offer, $8M of administrative costs, $55M of secured debt, and $45M of unsecured notes. Calculate recovery for each tranche. Then explain how a one-year delay with $6M of additional professional fees changes the unsecured recovery.",
        "Proceeds are $85M; after $8M of administration, $77M is available. Secured debt recovers 100%, leaving $22M; unsecured notes recover 22/45 = 48.9%. A one-year delay with $6M of additional fees reduces the available pool to $71M, leaving $16M for unsecured notes, or 35.6%. The delay and fees can consume a meaningful share of the fulcrum recovery.",
        [
            q(
                "A distressed investment without a catalyst is most likely to:",
                ["Repay quickly", "Remain cheap for an uncertain period", "Guarantee a recovery"],
                1,
                "A catalyst is what forces value to be realized or claims to be renegotiated.",
            ),
            q(
                "Proceeds after administration are 50 and a 40 claim is next in line. Recovery is:",
                ["80%", "100%", "125%"],
                1,
                "min(40, 50) / 40 = 100%; the claim is paid in full, with 10 left for junior claims.",
            ),
            q(
                "The fulcrum security in a distressed capital structure is the tranche that:",
                ["Is first in priority", "Is partly paid and sensitive to enterprise value", "Always recovers nothing"],
                1,
                "The fulcrum is partly paid and captures the marginal value of the enterprise.",
            ),
        ],
    )

    checkpoints = [
        (
            "Checkpoint · coverage, priority, and liquidity",
            [
                (
                    "16.1",
                    q(
                        "EBITDA is 120, interest is 40, taxes 10, maintenance capex 20, and debt 300. FCF to debt is:",
                        ["10%", "16.7%", "20%"],
                        1,
                        "(120 − 40 − 10 − 20) / 300 = 50 / 300 = 16.7%.",
                    ),
                ),
                (
                    "16.2",
                    q(
                        "After senior claims, 30 remains for a 60 unsecured claim. Recovery is:",
                        ["30%", "50%", "100%"],
                        1,
                        "Recovery is 30 / 60 = 50% of the unsecured claim.",
                    ),
                ),
                (
                    "16.3",
                    q(
                        "Cash is 20, revolver availability is 10, and monthly burn is 10. Runway is:",
                        ["2 months", "3 months", "30 months"],
                        1,
                        "(20 + 10) / 10 = 3 months.",
                    ),
                ),
                (
                    "16.4",
                    q(
                        "Going-concern EV is 180, debt is 100, and restructuring costs are 20. Equity value is:",
                        ["60", "80", "100"],
                        0,
                        "Going-concern equity is 180 − 100 − 20 = 60.",
                    ),
                ),
            ],
        ),
    ]

    return finish(
        {
            "id": "credit-distress",
            "number": 16,
            "title": "Credit analysis & distressed securities",
            "description": "Follow a credit from coverage and covenants to recovery waterfalls, expected loss, and a distressed catalyst process.",
            "source": "Advanced security analysis · original credit cases with regulatory and central-bank anchors",
            "level": "Advanced",
            "icon": "book",
            "modules": modules,
            "prerequisites": "Security Analysis or equivalent knowledge of debt, interest, and financial statements. The course is quantitative and document-heavy.",
            "outcomes": [
                "Measure coverage and free cash flow through the cycle.",
                "Build a recovery waterfall and identify the fulcrum security.",
                "Translate covenants, burn, and maturities into a liquidity runway.",
                "Value a distressed business on going-concern and liquidation bases.",
            ],
            "readingGuide": "Read the credit agreement, indenture, and maturity schedule beside each lesson. The worked cases are teaching figures; the cited sources supply the real-world context.",
            "references": [
                {"title": "U.S. SEC · EDGAR full-text search for credit agreements", "url": "https://efts.sec.gov/LATEST/search-index?q=%22credit%20agreement%22"},
                {"title": "Federal Reserve · Financial stability resources", "url": "https://www.federalreserve.gov/financial-stability.htm"},
            ],
            "parts": [
                {"id": "I", "title": "Coverage, priority, and liquidity", "description": "Cash-flow coverage, recovery waterfalls, and the three clocks"},
                {"id": "II", "title": "Distress valuation and process", "description": "Going concern versus liquidation, spreads and expected loss, and catalysts"},
            ],
            "studyType": "applied",
        },
        checkpoints,
    )
