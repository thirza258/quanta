"""Valuation under uncertainty and scenario modeling course (19.x)."""

from advanced_security_common import finish, make_add, q

READING = (
    "Advanced security analysis · valuation under uncertainty. Read the company's cash-flow history, "
    "guidance, and risk disclosures beside this lesson. The worked figures are teaching numbers; "
    "the cited sources supply the real-world context."
)


def build_valuation_uncertainty():
    modules = []
    add = make_add(modules, READING)

    add(
        "19.1",
        "I",
        "Scenario DCF and probability-weighted value",
        "Build bear, base, and bull DCF cases from explicit operating assumptions, then combine them into a probability-weighted value.",
        r"""
## The analytical question

A single discounted-cash-flow estimate hides the uncertainty in its inputs. A scenario model makes the uncertainty visible by building separate cases for the drivers that matter: revenue growth, margins, reinvestment, the discount rate, and the terminal growth rate. The analyst then assigns probabilities and computes an expected value, while keeping the individual cases available for inspection.

$$\text{EV}_j=\frac{\text{FCF}_{j,1}}{\text{WACC}_j-g_j}$$

$$V_{\text{expected}}=\sum_j p_j\text{EV}_j,\qquad \sum_j p_j=1$$

The probabilities are judgments, not measurements. The value of the exercise is that it forces the analyst to state which world each probability describes and to avoid pretending that a point estimate is certain.

## A worked example

A company has current base-case free cash flow of $100M, growing 2% to $102M next year. With a WACC of 9% and terminal growth of 2%, base EV is $102/(0.09 − 0.02) = $1,457.1M.

The bear case assumes current FCF of $70M, growing 1% to $70.7M next year, with an 11% WACC: $70.7/(0.11 − 0.01) = $707M. The bull case assumes current FCF of $130M, growing 2.5% to $133.25M, with an 8% WACC: $133.25/(0.08 − 0.025) = $2,422.7M.

With probabilities of 25%, 50%, and 25%, expected EV is 0.25(707) + 0.50(1,457.1) + 0.25(2,422.7) = $1,511.0M. Net debt of $200M leaves $1,311.0M of equity value; across 100M shares, that is $13.11 per share. The expected value is above the base case because the bull case is larger than the bear case, even though both have 25% probability. The analyst should explain why that asymmetry is justified.

## Research discipline

1. **Define each scenario by operating drivers**, not by a different valuation formula.
2. **Keep the discount rate and growth assumptions consistent** with the business risk in each case.
3. **Explain the probability weights** and the evidence behind them.
4. **Report the full range**, not only the expected value. A wide range is information.
""",
        r"\text{EV}_j=\frac{\text{FCF}_{j,1}}{\text{WACC}_j-g_j};\quad V_{\text{expected}}=\sum_j p_j\text{EV}_j",
        'bear_fcf = 70\nbear_wacc = 0.11\nbear_growth = 0.01\nbase_fcf = 100\nbase_wacc = 0.09\nbase_growth = 0.02\nbull_fcf = 130\nbull_wacc = 0.08\nbull_growth = 0.025\nbear_ev = bear_fcf*(1 + bear_growth)/(bear_wacc - bear_growth)\nbase_ev = base_fcf*(1 + base_growth)/(base_wacc - base_growth)\nbull_ev = bull_fcf*(1 + bull_growth)/(bull_wacc - bull_growth)\nexpected = 0.25*bear_ev + 0.50*base_ev + 0.25*bull_ev\nprint("Expected EV:", round(expected, 1))\nprint("Equity per share:", round((expected - 200)/100, 2))\nprint("Bear EV:", round(bear_ev, 1))\nprint("Base EV:", round(base_ev, 1))\nprint("Bull EV:", round(bull_ev, 1))',
        "A company has scenario free cash flows of $80M, $110M, and $140M, with WACCs of 10%, 9%, and 8% and terminal growth of 1%, 2%, and 3% for bear, base, and bull. Probabilities are 30%, 50%, and 20%. Calculate each EV, the expected EV, and equity value per share with $150M of net debt and 80M shares.",
        "Bear EV is 80 × 1.01/(0.10 − 0.01) = $897.8M. Base is 110 × 1.02/(0.09 − 0.02) = $1,602.9M. Bull is 140 × 1.03/(0.08 − 0.03) = $2,884M. Expected EV is 0.30(897.8) + 0.50(1,602.9) + 0.20(2,884) = $1,647.1M. Equity is $1,497.1M, or $18.71 per share across 80M shares.",
        [
            q(
                "A scenario model is most useful when each case:",
                [
                    "Uses a different formula to reach the desired answer",
                    "Changes operating assumptions and keeps the bridge consistent",
                    "Assumes the same cash flow and changes only the name",
                ],
                1,
                "The discipline is to change drivers and keep the valuation bridge internally consistent.",
            ),
            q(
                "Expected EV is the probability-weighted sum of:",
                ["Share prices", "Scenario enterprise values", "Accounting earnings"],
                1,
                "Each scenario's EV is weighted by its probability.",
            ),
            q(
                "A 25% probability on a $700M bear case contributes how much to expected EV?",
                ["175", "350", "700"],
                0,
                "The bear contribution is 0.25 × 700 = 175.",
            ),
        ],
    )

    add(
        "19.2",
        "I",
        "Sensitivity, tornado charts, and break-even analysis",
        "Rank valuation inputs by their effect on value and identify the assumptions that would change the decision.",
        r"""
## The analytical question

A valuation has many inputs, but not all of them matter equally. A **tornado chart** changes one input at a time across a plausible range and ranks the resulting value changes. The inputs at the top of the chart deserve the most research. The inputs at the bottom can be approximated without changing the conclusion.

The same analysis can identify a **break-even assumption**: the growth rate, margin, or price at which the investment decision flips. Break-even analysis is often more useful than a precise point estimate because it tells the analyst what must be true for the thesis to work.

$$\text{Value sensitivity}=\frac{V(\text{high})-V(\text{low})}{V(\text{base})}$$

## A worked example

A base-case DCF with next-year FCF of $102M, a 9% WACC, and 2% growth is worth $1,457.1M. The analyst tests three inputs:

| Input | Low | High | Value at low | Value at high | Swing |
| :--- | ---: | ---: | ---: | ---: | ---: |
| WACC | 8% | 10% | $1,700.0M | $1,275.0M | $425.0M |
| Terminal growth | 1.5% | 2.5% | $1,360.0M | $1,569.2M | $209.2M |
| Next-year FCF | $90M | $110M | $1,285.7M | $1,571.4M | $285.7M |

The WACC has the largest swing, followed by next-year FCF and terminal growth. The analyst should spend the most time on the discount rate and the cash-flow drivers. If the current price is below the low end of the WACC range, the decision may be robust; if it sits inside the range, the decision depends on an assumption that needs more evidence.

Break-even can be expressed as a price or as an operating variable. If the current price is $1,300M, it sits inside the WACC range of $1,275.0M to $1,700.0M, so a small change in the required return could eliminate the margin of safety. The analyst should state the break-even explicitly.

## Research discipline

1. **Choose plausible ranges from evidence**, not arbitrary round numbers.
2. **Change one input at a time** for the tornado, then test correlated changes separately.
3. **Report the swing in value and in the decision**, not only the percentage.
4. **Identify the break-even assumption** and monitor it after the investment.
""",
        r"\text{Swing}=\frac{V_{\text{high}}-V_{\text{low}}}{V_{\text{base}}};\quad \text{Break-even}=\text{value where NPV}=0",
        'fcf = 102\nwacc = 0.09\ngrowth = 0.02\nbase = fcf/(wacc - growth)\nprint("Base value:", round(base, 1))\nprint("WACC swing:", round(fcf/(wacc - 0.01) - fcf/(wacc + 0.01), 1))\nprint("Growth swing:", round(fcf/(wacc - 0.025) - fcf/(wacc - 0.015), 1))\nprint("FCF swing:", round(110/(wacc - growth) - 90/(wacc - growth), 1))',
        "A base-case DCF uses $120M of FCF, a 10% WACC, and 2% growth. Calculate the base value. Then calculate value at an 8% WACC and at a 12% WACC, and state which input you would research most before relying on the valuation.",
        "Base value is 120/(0.10 − 0.02) = $1,500M. At an 8% WACC, value is 120/(0.08 − 0.02) = $2,000M. At 12%, value is 120/(0.12 − 0.02) = $1,200M. The WACC swing is $800M, or 53% of the base value. The discount rate deserves the most research, because a small change in the required return has a large effect on a long-duration cash flow.",
        [
            q(
                "A tornado chart ranks inputs by:",
                ["Their accounting label", "Their effect on value across a plausible range", "The order they appear in the filing"],
                1,
                "The chart shows which assumptions matter most to the valuation.",
            ),
            q(
                "Break-even analysis asks:",
                ["What input value would make the decision flip?", "What the share price did last year?", "How many pages the report has?"],
                0,
                "Break-even identifies the threshold at which the investment case changes.",
            ),
            q(
                "If a valuation is $1,000M at a 9% WACC and $1,250M at 8%, the value change is:",
                ["$250M", "$500M", "$1,250M"],
                0,
                "1,250 − 1,000 = $250M.",
            ),
        ],
    )

    add(
        "19.3",
        "I",
        "Real options and decision trees",
        "Value the option to defer, expand, or abandon a project, and distinguish option value from a static NPV.",
        r"""
## The analytical question

A static NPV assumes the project is either undertaken now or rejected forever. Many real projects give managers the right, but not the obligation, to defer, expand, contract, or abandon. That flexibility has value, especially when uncertainty is high and the investment is staged.

A simple decision tree values the option:

$$\text{Option value}=\sum_s p_s\max\left(0,\text{Payoff}_s-\text{Investment}\right)$$

discounted at an appropriate rate. The max function captures the manager's ability to avoid the investment in bad states. The option value is generally higher than the static expected NPV when the downside can be avoided.

## A worked example

A project requires a $100M investment today. In one year, it will be worth $200M with 60% probability or $40M with 40% probability. The risk-adjusted discount rate is 10%.

The static expected payoff is 0.60(200) + 0.40(40) = $136M. Discounted one year, that is $123.6M; subtracting the $100M investment gives a static NPV of $23.6M.

Now suppose the company can wait one year and invest only if the project is worth $200M. The option payoff is 0.60 × max(0, 200 − 100) = $60M in the good state and zero in the bad state. Discounted at 10%, the option value is $54.5M. Waiting has value because it avoids the $60M loss in the bad state.

The option value depends on the discount rate, the probability, and the ability to wait. A project with a negative static NPV can still be valuable as an option if the upside is large and the downside can be avoided. The analyst should not double-count: if the option is valuable, the investment decision should reflect the option value, not the static NPV alone.

## Research discipline

1. **Identify the real option explicitly**: defer, expand, contract, switch, or abandon.
2. **Use a decision tree with probabilities and payoffs** rather than a single base case.
3. **Discount at a rate consistent with the risk of the cash flows**, and disclose the assumption.
4. **Check whether the option is actually available.** Contractual, competitive, or regulatory constraints can eliminate it.
""",
        r"\text{Static NPV}=\frac{\sum_s p_s\text{Payoff}_s}{1+r}-I;\quad \text{Option value}=\frac{\sum_s p_s\max(0,\text{Payoff}_s-I)}{1+r}",
        'prob_good = 0.60\ngood = 200\nbad = 40\ninvestment = 100\nrate = 0.10\nstatic_payoff = prob_good*good + (1 - prob_good)*bad\nstatic_npv = static_payoff/(1 + rate) - investment\noption_value = prob_good*max(0, good - investment)/(1 + rate)\nprint("Static NPV:", round(static_npv, 1))\nprint("Option value:", round(option_value, 1))',
        "A project requires $80M today. In one year it is worth $160M with 50% probability or $30M with 50% probability. The discount rate is 12%. Calculate the static expected NPV. Then calculate the value of the option to wait one year and invest only in the good state.",
        "The static expected payoff is 0.50(160) + 0.50(30) = $95M. Discounted at 12%, it is $84.8M; minus $80M, static NPV is $4.8M. The option payoff is 0.50 × max(0, 160 − 80) = $40M, discounted to $35.7M. Waiting is valuable because it avoids the $50M loss in the bad state, even though the static NPV is barely positive.",
        [
            q(
                "A real option is valuable because it:",
                ["Requires the company to invest in every state", "Allows the company to avoid the downside in bad states", "Eliminates all uncertainty"],
                1,
                "The right, but not the obligation, to invest lets the company capture upside while limiting downside.",
            ),
            q(
                "The max(0, payoff − investment) term represents:",
                ["The obligation to invest", "The option to abandon or not invest", "The accounting profit"],
                1,
                "The max function captures the ability to avoid a negative payoff.",
            ),
            q(
                "A 50% chance of a $100 payoff and a 50% chance of $20, with a $60 investment, gives an option payoff of:",
                ["20", "40", "50"],
                0,
                "0.50 × max(0, 100 − 60) + 0.50 × max(0, 20 − 60) = 20.",
            ),
        ],
    )

    add(
        "19.4",
        "II",
        "Reverse DCF and market-implied expectations",
        "Solve for the growth or margin the market price implies, then judge whether those expectations are plausible.",
        r"""
## The analytical question

A conventional DCF asks what the company is worth under the analyst's assumptions. A **reverse DCF** asks what assumptions the current price implies. The two questions are complementary: the first produces a value, the second produces a test of the market's expectations.

For a simple growing perpetuity:

$$P_0=\frac{\text{FCF}_1}{\text{WACC}-g}\quad\Rightarrow\quad g=\text{WACC}-\frac{\text{FCF}_1}{P_0}$$

More complex models can solve for revenue growth, margin, or the duration of excess returns. The reverse DCF is useful because it turns an argument about value into an argument about whether a specific expectation is reasonable.

## A worked example

A company has an enterprise value of $5,500M, next-year FCF of $300M, and a WACC of 9%. Solving for the implied perpetual growth rate:

$$g=0.09-\frac{300}{5{,}500}=0.09-0.0545=0.0355,\text{ or }3.55\%$$

The market price implies 3.55% perpetual growth. The analyst should compare that with the company's history, the industry's growth, and the reinvestment required to achieve it. If the company has grown FCF at 6% and has a large runway, 3.55% may be conservative. If the company is mature and facing competition, 3.55% may be optimistic.

The reverse DCF can also solve for the WACC or the margin. If the implied growth is implausibly high, the market may be pricing a lower discount rate or a longer period of high growth than the simple formula assumes. The analyst should state which assumption is being solved and which are held fixed.

## Research discipline

1. **State the model and the fixed assumptions** before solving for the implied variable.
2. **Compare the implied expectation with history and peers**, not with your own hope.
3. **Test the sensitivity of the implied variable** to the fixed assumptions.
4. **Use the reverse DCF to frame the debate**, not to declare the market wrong.
""",
        r"g=\text{WACC}-\frac{\text{FCF}_1}{P_0};\quad \text{Implied WACC}=\frac{\text{FCF}_1}{P_0}+g",
        'ev = 5500\nfcf = 300\nwacc = 0.09\nimplied_g = wacc - fcf/ev\nprint("Implied growth (%):", round(implied_g*100, 2))\nprint("Implied WACC at 3.55% growth (%):", round((fcf/ev + implied_g)*100, 2))',
        "A company has an enterprise value of $8,000M, next-year FCF of $400M, and a WACC of 8.5%. Calculate the perpetual growth rate implied by the price. Then explain what evidence would make that expectation look too optimistic.",
        "Implied growth is 0.085 − 400/8,000 = 0.085 − 0.05 = 3.5%. It would look too optimistic if the company's end markets are shrinking, its reinvestment needs are rising without corresponding growth, or competitors are eroding its returns. The analyst should compare 3.5% with the company's historical FCF growth and the industry's long-run growth.",
        [
            q(
                "A reverse DCF solves for:",
                ["The assumptions implied by the current price", "The company's tax rate", "The number of shares outstanding"],
                0,
                "It inverts the valuation to show what the market price requires.",
            ),
            q(
                "If EV is 2,000, FCF is 100, and WACC is 10%, implied perpetual growth is:",
                ["3%", "5%", "10%"],
                1,
                "0.10 − 100/2,000 = 0.10 − 0.05 = 5%.",
            ),
            q(
                "An implied growth rate above the company's historical growth should prompt:",
                ["Immediate rejection of the stock", "An investigation of what could justify the higher expectation", "Ignoring the result"],
                1,
                "The implied expectation may be justified by a new runway; the analyst should investigate rather than assume.",
            ),
        ],
    )

    add(
        "19.5",
        "II",
        "Distress-adjusted valuation",
        "Incorporate the probability and cost of financial distress into enterprise and equity value.",
        r"""
## The analytical question

A conventional DCF assumes the company continues to operate. A leveraged or cyclical company may face a meaningful probability of distress, in which value is reduced by lost customers, employee attrition, legal costs, and asset sales at discounts. The analyst should adjust the expected value for those states.

A simple approach is:

$$\text{Expected EV}=p_{\text{continue}}\text{EV}_{\text{continue}}+p_{\text{distress}}\text{EV}_{\text{distress}}$$

$$\text{Expected equity}=\text{Expected EV}-\text{Net debt}-\text{Expected distress costs}$$

The distress probability and the distress value are estimates. The purpose is not precision but honesty: a valuation that assumes the company always continues may overstate equity value for a leveraged business.

## A worked example

A leveraged company has a going-concern EV of $500M and a distress EV of $200M. The analyst estimates a 20% probability of distress over the investment horizon. Expected EV is 0.80(500) + 0.20(200) = $440M.

Net debt is $300M. A naive valuation gives equity of $500M − $300M = $200M. The distress-adjusted valuation gives $440M − $300M = $140M before additional distress costs. If legal and restructuring costs are expected to be $30M in the distress state, the expected cost is 0.20 × $30M = $6M, reducing equity to $134M.

The difference between $200M and $134M is material. The analyst should also consider the shape of the distribution: if the distress state is a total loss for equity, the equity value may be lower still. The debt's value, by contrast, depends on recovery in the distress state. The same scenario analysis can value each layer of the capital structure.

## Research discipline

1. **Estimate distress probability from leverage, liquidity, and business risk**, not from a single rating.
2. **Value the distress state explicitly**: liquidation, restructuring, or a forced sale.
3. **Include direct and indirect distress costs**, and disclose the assumptions.
4. **Value debt and equity separately** in the distress state; they do not share the same recovery.
""",
        r"\text{Expected EV}=p_c\text{EV}_c+p_d\text{EV}_d;\quad \text{Expected equity}=\text{Expected EV}-\text{Debt}-\text{Expected costs}",
        'ev_continue = 500\nev_distress = 200\np_distress = 0.20\ndebt = 300\ndistress_cost = 30\nexpected_ev = (1 - p_distress)*ev_continue + p_distress*ev_distress\nexpected_equity = expected_ev - debt - p_distress*distress_cost\nprint("Expected EV:", round(expected_ev, 1))\nprint("Expected equity:", round(expected_equity, 1))\nprint("Naive equity:", ev_continue - debt)',
        "A company has a going-concern EV of $800M, a distress EV of $300M, a 25% distress probability, net debt of $450M, and expected distress costs of $40M in the distress state. Calculate expected EV and expected equity value, and compare with a naive going-concern equity value.",
        "Expected EV is 0.75(800) + 0.25(300) = $675M. Expected equity is 675 − 450 − 0.25(40) = $215M. The naive going-concern equity is 800 − 450 = $350M. The difference, $135M, reflects the probability-weighted loss in the distress state and the expected distress costs. The analyst should state whether equity is assumed to receive any residual in the distress case.",
        [
            q(
                "Expected EV with a 70% continue probability at 600 and a 30% distress value at 200 is:",
                ["420", "480", "600"],
                1,
                "0.70 × 600 + 0.30 × 200 = 420 + 60 = 480.",
            ),
            q(
                "Distress costs should be included because:",
                ["They are always zero", "They reduce the value available to claimholders", "They increase the share count"],
                1,
                "Legal, restructuring, and operating costs consume value in the distress state.",
            ),
            q(
                "A naive going-concern equity value ignores:",
                ["The probability and cost of distress", "The share price", "The dividend history"],
                0,
                "A going-concern-only valuation assumes the distress state never occurs.",
            ),
        ],
    )

    add(
        "19.6",
        "II",
        "Valuation discipline and price ceilings",
        "Translate a valuation range into a maximum purchase price and a position rule that survives uncertainty.",
        r"""
## The analytical question

A valuation is not a buy signal. The analyst must compare the price with a conservative value and require a margin of safety. The maximum price is:

$$P_{\max}=V_{\text{conservative}}\times(1-M_{\text{required}})$$

The conservative value should be the low end of a defensible range, not the base case. The required margin depends on the uncertainty, the quality of the business, and the investor's tolerance for error. A wide valuation range calls for a larger margin.

A position rule can also be tied to the price ceiling:

$$\text{Target weight}=f\left(\frac{V_{\text{conservative}}-P}{V_{\text{conservative}}}\right)$$

The exact function is a policy choice. The important discipline is that the position size responds to the margin of safety, not to the strength of the story.

## A worked example

An analyst estimates a conservative value of $40 per share, a base value of $55, and an optimistic value of $70. The mandate requires a 30% margin of safety against the conservative value. The maximum purchase price is $40 × 0.70 = $28.00.

At a market price of $35, the stock trades 12.5% below the conservative value but 25% above the maximum price. The decision is to reject the purchase. At $26, the stock is 7.1% below the maximum price and offers a 35% margin to the conservative value; the purchase may be authorized, subject to position limits.

The analyst should not raise the conservative value to justify a purchase at $35. The whole point of the ceiling is to prevent the valuation from following the price. If new evidence genuinely raises the conservative value, the analyst can update it and document the reason; the update should be date-stamped and independently reviewable.

## Research discipline

1. **Set the conservative value before looking at the current price.**
2. **Use the low end of the range** for the margin-of-safety calculation.
3. **Pre-commit the required margin** and the position rule.
4. **Update valuations only on new evidence**, with a dated record of what changed and why.
""",
        r"P_{\max}=V_{\text{conservative}}(1-M_{\text{required}});\quad \text{Margin}=1-\frac{P}{V_{\text{conservative}}}",
        'conservative = 40\nrequired = 0.30\nprice = 35\npmax = conservative * (1 - required)\nprint("Maximum price:", round(pmax, 2))\nprint("Margin at current price (%):", round((1 - price / conservative) * 100, 1))\nprint("Buy at 26:", 26 <= pmax)',
        "A conservative value is $60 per share, the required margin of safety is 25%, and the current price is $48. Calculate the maximum purchase price and the actual margin of safety. Then determine whether the stock can be bought and what would happen if the analyst raised the conservative value to $70 without new evidence.",
        "The maximum price is 60 × 0.75 = $45.00. At $48, the actual margin is 1 − 48/60 = 20%, below the required 25%, so the purchase is rejected. Raising the conservative value to $70 without new evidence would make the maximum price $52.50 and appear to justify the purchase, but that is exactly the discipline the ceiling is designed to prevent. A valuation update requires documented new evidence.",
        [
            q(
                "Conservative value is 50 and the required margin is 20%. The maximum price is:",
                ["30", "40", "45"],
                1,
                "The maximum price is 50 × 0.80 = 40.",
            ),
            q(
                "A stock at 36 with a conservative value of 45 has a margin of safety of:",
                ["20%", "25%", "36%"],
                0,
                "The margin of safety is 1 − 36/45 = 20%.",
            ),
            q(
                "Raising the valuation estimate to justify a purchase is:",
                ["Good practice if the story is strong", "A violation of price discipline", "Required by accounting rules"],
                1,
                "The ceiling exists to stop the valuation from following the market price.",
            ),
        ],
    )

    checkpoints = [
        (
            "Checkpoint · scenarios, sensitivity, and price",
            [
                (
                    "19.1",
                    q(
                        "A bear case has 20% probability and an EV of 400; the base case has 80% and an EV of 900. Expected EV is:",
                        ["650", "800", "900"],
                        1,
                        "0.20 × 400 + 0.80 × 900 = 80 + 720 = 800.",
                    ),
                ),
                (
                    "19.2",
                    q(
                        "A valuation is 800 at a 10% WACC and 1,000 at 9%. The value change is:",
                        ["100", "200", "900"],
                        1,
                        "The value change is 1,000 − 800 = 200.",
                    ),
                ),
                (
                    "19.3",
                    q(
                        "An option to invest only in the good state is valuable because it:",
                        ["Avoids the bad-state investment", "Guarantees a profit", "Eliminates the discount rate"],
                        0,
                        "The option captures upside while avoiding the negative payoff in the bad state.",
                    ),
                ),
                (
                    "19.4",
                    q(
                        "EV is 4,000, FCF is 200, and WACC is 9%. Implied perpetual growth is:",
                        ["4%", "5%", "9%"],
                        0,
                        "0.09 − 200/4,000 = 0.09 − 0.05 = 4%.",
                    ),
                ),
            ],
        ),
    ]

    return finish(
        {
            "id": "valuation-uncertainty",
            "number": 19,
            "title": "Valuation under uncertainty",
            "description": "Build scenario DCFs, rank the assumptions that matter, value real options, reverse-engineer market expectations, and enforce a price ceiling.",
            "source": "Advanced security analysis · original valuation cases with real-world anchors",
            "level": "Advanced",
            "icon": "book",
            "modules": modules,
            "prerequisites": "Security Analysis and the time-value material in Statistical Foundations, or equivalent.",
            "outcomes": [
                "Build and probability-weight bear, base, and bull DCFs.",
                "Rank valuation sensitivities and find break-even assumptions.",
                "Value deferral and abandonment options with decision trees.",
                "Translate a valuation range into a maximum purchase price.",
            ],
            "readingGuide": "Work each calculation with a spreadsheet or the lesson worksheet. The figures are teaching numbers; the cited sources supply the real-world context.",
            "references": [
                {"title": "U.S. SEC · Investor.gov: asset allocation and risk", "url": "https://www.investor.gov/introduction-investing/getting-started/asset-allocation"},
                {"title": "U.S. SEC · EDGAR company filings", "url": "https://www.sec.gov/edgar/searchedgar/companysearch"},
            ],
            "parts": [
                {"id": "I", "title": "Scenarios, sensitivity, and options", "description": "Scenario DCFs, tornado analysis, and real options"},
                {"id": "II", "title": "Market expectations and discipline", "description": "Reverse DCF, distress adjustment, and price ceilings"},
            ],
            "studyType": "applied",
        },
        checkpoints,
    )
