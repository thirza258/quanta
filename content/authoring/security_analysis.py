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
        if part == "VIII":
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

    add(
        "1.1",
        "I",
        "Foundations of Graham & Dodd",
        "Distinguish a defensible investment operation from a price prediction and calculate a conservative margin of safety.",
        r"""
## The analytical question

Start with the security's claim, the evidence supporting payment, and the price paid. A profitable trade can have been poorly reasoned; an adverse outcome can follow a reasonable analysis. Judge the process using information available when the decision was made. Calling an asset a bond or holding a stock for years does not by itself establish investment merit.

The course treats intrinsic value as a reasoned range supported by assets, earning power, and contractual rights. Each method answers a different question. A liquidation estimate asks what might remain after disposing of assets and settling claims. A going-concern estimate assumes the business continues. Keep those assumptions visible instead of averaging incompatible numbers.

A margin of safety expresses the discount to an estimate. Its usefulness depends on the quality of that estimate. An inflated denominator can manufacture an impressive discount. A falling quotation does not automatically increase protection if the business deteriorates faster.

$$M=1-P/V$$

## A worked example

Fictional Alder Manufacturing trades at $60. Your estimated values are $75 under a weak operating case, $100 in the base case, and $125 in a favorable case. The margins are 20%, 40%, and 52%, respectively. With a required 30% discount to the weak-case estimate, the maximum price is $75 × 0.70 = $52.50. The base case passes; the conservative case fails.

This rule does not assign a probability to loss. If an unrecorded obligation destroys $30 of per-share value, even the weak-case estimate was inadequate. Your memo must identify what could make the analysis wrong and what evidence would cause a revision.

## Research discipline

Write a dated decision with four lines: claim purchased, conservative value range, evidence that could impair it, and maximum acceptable price. Keep the market quotation in a separate column from the valuation inputs. Revisit business facts on new information; avoid changing the estimate merely to justify a position already held.

Use the optional worksheet to vary price and value independently. Its accompanying cash-only price simulation is a technical container; it does not test whether your estimate is correct.
""",
        r"M=1-P/V",
        'price = 60\nvalue = 100\nprint("Margin of safety:", round((1 - price / value) * 100, 1), "%")\nprint("Conservative maximum price:", 75 * 0.70)',
        "At a price of $54 and weak-case value of $72, apply a 30% required discount. Write a decision and name one fact that could reduce value.",
        "The discount is 25%; the maximum price is $50.40. The stated rule does not permit purchase at $54. A customer loss, debt maturity, or impaired asset could lower the denominator; the numerical discount alone is insufficient.",
        [
            q(
                "A stock priced at $60 has estimated value of $100. Its margin of safety is:",
                ["20%", "40%", "60%"],
                1,
                "The discount is (100 − 60) / 100 = 40%; value, not price, is the denominator.",
            ),
            q(
                "Which change weakens a margin-of-safety conclusion?",
                [
                    "A better documented asset register",
                    "Using an optimistic value without testing downside",
                    "Separating price from value",
                ],
                1,
                "A large apparent discount can be created by an unsupported optimistic value estimate.",
            ),
            q(
                "A researcher requires a 25% discount to a weak-case value of $80. The quote is $64. What follows?",
                [
                    "Buy because the base case is higher",
                    "The price meets the rule",
                    "The maximum permitted price is $60",
                ],
                2,
                "$80 × 0.75 = $60; the $64 quote provides only a 20% discount to the chosen conservative estimate.",
            ),
        ],
    )

    add(
        "1.6",
        "I",
        "Build an evidence file",
        "Separate reported facts, analytical adjustments, and assumptions in a dated research record.",
        r"""
## From information to evidence

A security analysis is an argument supported by traceable information. Build a file that another analyst can reconstruct: document date, period covered, currency, units, scope of consolidation, and the exact item used. Published accounts, governing security documents, and management explanations answer different questions. Agreement among several data vendors may simply reflect one shared source.

Use three columns: **reported**, **adjusted**, and **assumed**. The first preserves the original observation. The second documents an explicit reconciliation. The third records a judgment with a reason and sensitivity range. Never silently replace a reported loss with a favorable estimate.

Contemporary filings are a course application of evidence discipline, not a claim about 1940 reporting rules. The [SEC financial-statement guide](https://www.sec.gov/investor/pubs/begfinstmtguide.htm) provides a starting reference for the different statements and their notes. Use the issuer's actual reporting policy when doing a real analysis.

## A worked example

Alder's year-end accounts report revenue of $240 million and receivables of $48 million. The previous year shows $200 million and $30 million. Revenue rose 20%; receivables rose 60%. Year-end receivables divided by annual sales rose from 15% to 20%. That is an investigation signal, not proof of fabrication: acquisitions, seasonality, customer terms, or collection trouble could explain it.

The filing was released on March 15. A January 31 historical decision cannot use its contents merely because the accounting period ended in December. Record both period-end and availability dates. Restated figures need their own publication date.

## A reproducible research packet

Preserve the original units and reconcile any restatement before comparing years. Record unanswered questions rather than filling gaps with plausible-looking numbers. A strong packet includes a statement bridge, a claims schedule, a list of key estimates, and an opposing interpretation of the same evidence. A weak packet contains ratios without definitions.

A discrepancy is a reason to investigate. Decide what additional document would discriminate between a benign explanation and an impaired business before changing your value estimate.
""",
        r"\text{Receivables intensity}=AR/\text{sales}",
        'print("Revenue growth (%):", (240 / 200 - 1) * 100)\nprint("Receivables growth (%):", (48 / 30 - 1) * 100)\nprint("Receivables / sales:", 48 / 240)',
        "Prepare a three-column evidence log for sales of 300, receivables of 90, and a management assertion that collections are normal. The prior receivables/sales ratio was 20%.",
        "Reported: 300 sales and 90 receivables, with dates and units. Calculated: 30% intensity, up 10 percentage points. Assumed: no collection impairment, if used at all. Request aging and subsequent receipts; management's assertion does not independently establish recoverability.",
        [
            q(
                "Receivables of 50 on annual sales of 250 imply what intensity?",
                ["5%", "20%", "50%"],
                1,
                "50 / 250 = 20%; this simplified ratio uses year-end receivables, not an average balance.",
            ),
            q(
                "Which date governs use of a filing in a historical investment decision?",
                [
                    "Its availability date",
                    "Only the period-end date",
                    "The date you downloaded it today",
                ],
                0,
                "The information must have been available by the decision date to avoid hindsight contamination.",
            ),
            q(
                "A dataset substitutes a June restatement into a March decision. What must the analyst do?",
                [
                    "Keep it because it is more accurate",
                    "Use the March information set and label the later revision",
                    "Delete all losses",
                ],
                1,
                "A reconstruction must preserve what was knowable in March; the June revision belongs to a later information set.",
            ),
        ],
    )

    add(
        "1.7",
        "I",
        "Value ranges and the limits of precision",
        "Reconcile asset and earnings evidence without double counting or disguising uncertainty.",
        r"""
## Choose a valuation premise

An estimate has meaning only under a stated premise. An operating factory may be worth more as part of a profitable business than as equipment sold separately. A loss-making business may consume its cash before owners realize an asset surplus. A single spreadsheet total can hide these mutually exclusive paths.

Distinguish a screening value, a full analytical estimate, and a transaction price. A screen narrows the research universe. A full estimate examines business economics and claims. A transaction price also reflects bargaining, control, financing, and timing. None is automatically interchangeable with the others.

Precision should follow evidence. Use a range wide enough to reflect uncertain margins, required returns, recoveries, and timing. Do not assign probabilities merely to make a weighted average look scientific. If you do use probabilities, explain where they came from and test alternative weights.

## A worked example

Alder's continuing operations are estimated at $180–220 million. Excess cash is $20 million; debt is $60 million; diluted shares are 10 million. Equity value is $140–180 million, or $14–18 per share. Separately, a liquidation worksheet produces $9 per share after all claims and closure costs.

Do not add the $9 liquidation value to the $14–18 operating range. The factory and receivables supporting operations are already inside the enterprise estimate. Only genuinely nonoperating assets excluded from that estimate can be added separately. Nor does $9 establish an assured floor if liquidation is neither feasible nor timely.

## Make uncertainty decision-relevant

At a $13 quote, the discount to $14 is only about 7.1%; the discount to $18 is about 27.8%. Selecting the upper endpoint changes the answer without changing the business. State which endpoint governs your decision and why.

The useful output is a decision boundary: what must be true for the proposed price to be justified? Then seek evidence about those assumptions. An unresolved liability or uncertain ownership right may justify withholding a conclusion even when the arithmetic is easy.
""",
        r"V_{equity}=V_{operations}+\text{excess cash}-\text{senior claims}",
        'for enterprise in [180, 200, 220]:\n    print("Equity per share:", (enterprise + 20 - 60) / 10)',
        "Value operations at 150–190, add 15 of excess cash, deduct 45 of debt, and use 8 million shares. Explain whether you may also add the operating inventory's liquidation proceeds.",
        "Equity is 120–160, or $15–20 per share. Operating inventory is already part of the going concern; adding its liquidation proceeds would double count the same economic resources.",
        [
            q(
                "Operations worth 100, excess cash 10, debt 30, and 5 shares give what equity value per share?",
                ["$16", "$20", "$28"],
                0,
                "(100 + 10 − 30) / 5 = $16 per share, using consistent company-wide units.",
            ),
            q(
                "When can a separate asset be added to an operating valuation?",
                [
                    "Whenever it has book value",
                    "When it is excluded from the operating estimate and available to owners after claims",
                    "Only when the quote falls",
                ],
                1,
                "The asset must represent an additional claim on value rather than an input already supporting operating earnings.",
            ),
            q(
                "An analyst adds a factory's resale value to the capitalized earnings generated by that factory. What is the main defect?",
                [
                    "The result uses too few decimal places",
                    "The factory is counted twice",
                    "All asset values must be zero",
                ],
                1,
                "The operating valuation already includes the productive asset; its separate sale proceeds describe another premise.",
            ),
        ],
    )

    add(
        "1.2",
        "II",
        "Bond safety and earnings coverage",
        "Evaluate a fixed claim using weak-period coverage, liquidity, and the issuer's business resilience.",
        r"""
## Begin with the obligation

A bond promises specified payments, but the issuer must generate or obtain the resources to make them. The contract limits the holder's upside while a serious impairment can impose a large loss. Investigate the reasons a payment could fail before comparing attractive yields.

Coverage measures a flow of earnings against a flow of charges. State whether your numerator is before interest, taxes, depreciation, or rent. A ratio that removes economically necessary costs may overstate protection. Use several years and a deliberately weak operating case. Historical survival is evidence, not a guarantee that tomorrow's industry structure will resemble yesterday's.

A high coverage ratio cannot settle a near-term maturity if cash is inaccessible and refinancing is unavailable. Add a maturity schedule and a source-of-payment analysis. Cash at a subsidiary may not be freely distributable to the entity that issued the bond.

## A worked example

Alder earns $120 million before interest and tax and owes $30 million of annual interest. Coverage is 4.0 times. In a weak year EBIT falls to $45 million, leaving 1.5 times coverage. If necessary recurring costs were excluded from EBIT, restore them before relying on either ratio.

Suppose $100 million of principal also matures next year, while accessible cash is $20 million and expected cash remaining after operations and interest is $25 million. The $55 million funding gap remains even though annual interest is covered. Refinancing is a possible source, not cash already on hand.

## An exclusion worksheet

Record business cyclicality, weak-period coverage, cash accessibility, maturity concentration, collateral quality, and restrictions on new claims. An unusually high yield should prompt a search for the corresponding risk. Do not let the quoted return repair a weak payment case.

No single coverage threshold works across all issuers. Define a policy for the case and explain its economic basis. A cyclical producer and a regulated utility can have different sources of uncertainty even with identical current ratios.
""",
        r"\text{Interest coverage}=EBIT/\text{interest}",
        'for ebit in [120, 45]:\n    print("Interest coverage:", ebit / 30)\nprint("Maturity funding gap:", 100 - 20 - 25)',
        "Stress EBIT from 90 to 36 with annual interest of 18. Separately assess a maturity of 80 against cash of 15 and internally generated cash of 20.",
        "Coverage falls from 5.0 to 2.0 times. The maturity gap is 45. Adequate interest coverage alone does not provide the principal payment; document a credible source or classify refinancing as unresolved.",
        [
            q(
                "EBIT of 90 and interest of 30 imply coverage of:",
                ["0.33 times", "3 times", "30 times"],
                1,
                "Divide earnings before interest and tax by the annual interest charge: 90 / 30 = 3.",
            ),
            q(
                "Which evidence most directly addresses a bond maturing in six months?",
                [
                    "A distant growth forecast",
                    "An accessible cash and committed funding schedule",
                    "The color of its price chart",
                ],
                1,
                "Principal repayment requires accessible funds by the due date, not merely accounting earnings.",
            ),
            q(
                "EBIT falls from 84 to 28 while annual interest remains 14. What is weak-case coverage?",
                ["6 times", "4 times", "2 times"],
                2,
                "The weak case uses 28 / 14 = 2; the historical 6-times ratio is not the stressed result.",
            ),
        ],
    )

    add(
        "1.8",
        "II",
        "Seniority, collateral, and recovery",
        "Build a simplified claim waterfall and distinguish collateral value from the issuer's total asset value.",
        r"""
## Identify who owes whom

Read the exact issuer and the claim's rank. A mortgage on one asset does not create a claim on every asset in a corporate group. A parent-company creditor can depend on residual distributions from subsidiaries whose own creditors must first be satisfied. Guarantees can change that picture; their scope matters.

Collateral protection depends on realizable proceeds after costs and competing claims. Book value is a historical accounting measure, while recovery depends on sale conditions, asset specificity, and enforceable rights. A pledge over obsolete equipment can offer little practical protection despite a large recorded balance.

The following waterfall is an arithmetic teaching model with stipulated priority and no dispute. Real legal priority, insolvency expenses, guarantees, and intercreditor terms require the actual documents; this lesson does not supply a jurisdictional rule.

## A worked example

A ring-fenced collateral pool realizes $70 million net of stipulated sale costs. The first-ranking secured claim is $50 million; a junior claim is $30 million. The senior holder recovers $50 million in full. Only $20 million remains, so the junior recovery is 20 / 30 = 66.7%. Equity receives nothing from this pool.

If proceeds fall to $40 million, the senior recovery becomes 80%, and junior recovery is zero. Label these outcomes as scenario recoveries. They are not default probabilities or present values. Waiting two years for a recovery also changes its economic value.

## Draw the claims map

List assets by owner, security interests by claimant, and residual transfers between entities. State whether each liability is recourse to the pool, another entity, or both. Avoid assigning the same collateral proceeds in full to two different creditors.

A recovery estimate should include a timing range and a sensitivity to realizable proceeds. Investigate whether maintaining the asset until sale consumes cash. Coverage and collateral complement one another: one studies payment from ongoing activity, the other protection if that activity fails.
""",
        r"R_{junior}=\min(D_j,\max(0,A-D_s))/D_j",
        'for assets in [70, 40]:\n    senior = min(50, assets)\n    junior = min(30, max(0, assets - senior))\n    print("Senior and junior recovery:", senior / 50, junior / 30)',
        "Allocate net proceeds of 95 to a first claim of 60, a second claim of 50, and equity. Repeat with proceeds of 55.",
        "At 95, senior receives 60, junior 35 (70%), equity zero. At 55, senior receives 55 (91.67%), junior and equity zero. These results depend on the stipulated priority and net proceeds.",
        [
            q(
                "Net proceeds are 75, senior debt 60, and junior debt 30. Junior recovery is:",
                ["100%", "50%", "25%"],
                1,
                "After 60 is paid, 15 remains for the junior claim of 30, giving 50%.",
            ),
            q(
                "Which fact is essential before assigning collateral value to a bond?",
                [
                    "The issuer's share-price momentum",
                    "The specific pledge, priority, and net realizable proceeds",
                    "The highest historical book value",
                ],
                1,
                "Recovery depends on the rights to particular assets and what remains after prior claims and costs.",
            ),
            q(
                "A parent owns a subsidiary whose assets realize 100 and whose own creditors are owed 90. Ignoring all other costs, what reaches the parent?",
                ["100", "90", "10"],
                2,
                "Only the subsidiary's residual 100 − 90 = 10 is available to the parent in this simplified ownership structure.",
            ),
        ],
    )

    add(
        "1.9",
        "II",
        "Covenants and the deterioration of protection",
        "Read a covenant as a defined test and model how additional borrowing changes creditor protection.",
        r"""
## Protection can change after purchase

An issuer can weaken an initially sound bond by adding debt, transferring assets, or distributing cash. Contractual restrictions can limit those actions, but the precise definitions and exceptions matter. An earnings test based on an adjusted metric can behave differently from the ordinary income statement.

For any stipulated covenant, record numerator, denominator, measurement date, threshold, permitted adjustments, and what happens if the test is failed. Do not infer the remedy from the word covenant alone. This exercise uses invented contract terms, not a claim about standard legal protections.

A limit on new borrowing is different from a test that must be satisfied continuously or periodically. Passing an incurrence test today does not ensure adequate payment resources in a later downturn. Likewise, covenant headroom is not identical to economic safety.

## A worked example

An invented bond permits additional debt only if EBIT divided by total annual interest remains at least 3.0 times immediately after the new issue. Current EBIT is $90 million and interest is $20 million. The maximum permitted annual interest is $30 million, so contractual incremental interest capacity is $10 million under these definitions.

Management proposes debt adding $8 million of interest. Pro-forma coverage is 90 / 28 = 3.21 times, so this test passes. At stressed EBIT of $56 million, coverage would be only 2.0 times. The contract's initial permission has not removed operating risk.

## Analyze the incentives

Ask who benefits from a dividend, acquisition, or refinancing and which security bears the added downside. Compare cash transferred to owners with the remaining coverage cushion. Read definitions before importing a ratio from a data service.

Your report should show the contract calculation beside an economic calculation using recurring costs. Differences can be informative without implying that either definition is mathematically wrong. The decision is whether the remaining protection is adequate at the proposed price.
""",
        r"\text{Incremental interest capacity}=EBIT/c-I_0",
        'ebit = 90\nthreshold = 3\ninterest = 20\nprint("Additional interest capacity:", ebit / threshold - interest)\nprint("Pro-forma coverage:", ebit / (interest + 8))',
        "A stipulated test requires 4-times coverage. EBIT is 120 and existing interest is 24. Can an issue adding 8 of interest pass? Explain economic versus contractual protection.",
        "Maximum interest is 30, leaving capacity of 6. Proposed total interest of 32 gives 3.75 times, so the issue fails this test. Even a passing issue would require a separate stress and liquidity analysis.",
        [
            q(
                "EBIT of 80 and a required coverage of 4 allow total interest of:",
                ["20", "40", "320"],
                0,
                "80 / 4 = 20 is total permitted interest under the stipulated definition.",
            ),
            q(
                "Why read the covenant's earnings definition?",
                [
                    "It always equals cash flow",
                    "Adjustments can materially change the measured headroom",
                    "Definitions cannot affect ratios",
                ],
                1,
                "Permitted add-backs and deductions can change coverage even when the operating business is unchanged.",
            ),
            q(
                "A borrowing test requires 3-times coverage; EBIT is 75 and existing interest is 18. What incremental interest fits?",
                ["7", "25", "57"],
                0,
                "Maximum total interest is 75 / 3 = 25, so additional capacity is 25 − 18 = 7.",
            ),
        ],
    )

    add(
        "1.10",
        "II",
        "Price, yield, calls, and reinvestment",
        "Separate coupon income from contractual return and identify how call rights limit upside.",
        r"""
## A quoted yield needs a cash-flow schedule

Coupon rate divides the annual coupon by face value. Current yield divides it by market price. Yield to maturity is the discount rate equating price with promised coupons and principal, assuming those payments occur. These quantities answer different questions. A discount to par contributes to promised maturity return; a premium can be lost as the bond approaches repayment.

Before solving a yield, write every payment date and amount. For a callable security, also model the issuer's right to redeem early. When rates fall, an attractive coupon may be removed just when reinvestment opportunities become less attractive. The holder does not control the most favorable repayment scenario.

A promised yield does not adjust itself for default risk or transaction costs. Comparing two securities solely by yield can conceal differences in payment reliability, maturity, embedded options, and liquidity.

## A worked example

An invented one-year bond has $100 face value and a $6 final coupon. At a price of $98, its promised one-year return is (106 − 98) / 98 = 8.16%. Current yield is 6 / 98 = 6.12%. The difference comes from receiving $100 principal after paying $98.

Now consider a different bond purchased at $105 that the issuer may call in one year at $100, with one $6 coupon before redemption. Under that stipulated call scenario, proceeds are $106 and the return is only 0.95%. Looking only at its 5.71% current yield misses the $5 capital loss.

## Compare complete alternatives

Build a table of price, payment dates, maturity proceeds, possible call proceeds, and key protection. Use consistent compounding and include accrued interest where the actual transaction requires it. A higher coupon can be worth less if call terms sharply constrain favorable outcomes.

A useful analyst explains both how the quoted return is calculated and what events prevent it from being earned. Credit analysis and valuation belong in the same decision.
""",
        r"R_{1y}=(C+F-P)/P",
        'print("One-year maturity return (%):", round((106 - 98) / 98 * 100, 2))\nprint("One-year call return (%):", round((106 - 105) / 105 * 100, 2))',
        "Pay 103 for a bond with one coupon of 4 before a stipulated one-year call at 100. Compare call return with current yield.",
        "Call return is (104 − 103) / 103 = 0.97%. Current yield is 4 / 103 = 3.88%. The premium loss explains the difference; neither calculation guarantees the issuer's payment.",
        [
            q(
                "A one-year bond costs 95 and pays 105 including principal. Promised return is approximately:",
                ["5%", "10.53%", "11.05%"],
                1,
                "The gain is 10 on an investment of 95, or 10.53%.",
            ),
            q(
                "Who generally benefits from an issuer's option to redeem a high-coupon bond when rates fall?",
                [
                    "The issuer exercising the option",
                    "The holder automatically receives extra principal",
                    "Neither party can be affected",
                ],
                0,
                "The issuer may replace expensive funding while the holder must reinvest on less favorable terms.",
            ),
            q(
                "A security costs 102 and pays a coupon of 5 plus call proceeds of 100 exactly one year later. Its return is:",
                ["4.90%", "2.94%", "5%"],
                1,
                "Total receipts of 105 less cost of 102 give 3 / 102 = 2.94%, before costs and default effects.",
            ),
        ],
    )

    add(
        "1.11",
        "III",
        "Preferred shares and cumulative claims",
        "Analyze dividend priority, arrears, and the difference between preferred equity and debt.",
        r"""
## Read the preference

Preferred shares combine a stated priority with issuer-specific terms. A fixed dividend rate can resemble a coupon economically, but preferred stock is equity and its payment rights are defined by its terms. Do not assume that a missed dividend creates the same remedies as missed bond interest.

Check whether dividends are cumulative, whether arrears restrict common distributions, whether the issue participates beyond its stated dividend, and whether the issuer can redeem it. Voting rights or other protections may change after specified events. Analyze the actual instrument; the label preferred is insufficient.

For a cumulative issue, unpaid dividends can accumulate as a priority before common dividends under the stipulated terms. Accumulation does not place cash in the holder's account. A profitable recovery may still leave a long wait before common shareholders receive distributions.

## A worked example

An invented cumulative preferred issue has $20 million of liquidation preference and a 6% annual dividend. Its annual requirement is $1.2 million. Two omitted annual dividends create $2.4 million of arrears. Under the case terms, common dividends cannot resume until arrears and the current preferred dividend are satisfied.

If $5 million is lawfully available for distributions this year, paying $2.4 million of arrears plus $1.2 million current preference leaves $1.4 million for common holders. If only $2 million is available, it cannot satisfy all preferred requirements. The accumulated claim should not be confused with evidence of payment capacity.

## Evaluate the junior creditor-like position

Study earnings after interest and tax because preferred dividends are paid from resources remaining after senior obligations. Compare the preference with common equity support and inspect whether assets can be transferred away. A low market price can indicate an impaired claim rather than an exceptional income opportunity.

Write a distribution waterfall separate from a liquidation waterfall. The rights and amounts applicable to one need not be identical to those in the other. Treat the simplified arithmetic as the beginning of document analysis.
""",
        r"D_{pref}=\text{preference}\times\text{dividend rate}",
        'annual = 20 * 0.06\narrears = annual * 2\nprint("Annual preference:", annual)\nprint("Residual distribution:", 5 - arrears - annual)',
        "A cumulative issue has preference of 30, an 8% dividend, and three years of arrears. Under terms requiring arrears plus the current dividend first, allocate an available distribution of 12.",
        "Annual dividend is 2.4; arrears are 7.2. Total priority is 9.6, leaving 2.4 for common holders if the distribution is permitted. This says nothing about the separate liquidation recovery.",
        [
            q(
                "A preference of 50 with a 4% dividend requires annually:",
                ["2", "4", "12.5"],
                0,
                "50 × 4% = 2 in the same monetary units as the preference.",
            ),
            q(
                "Cumulative arrears establish:",
                [
                    "Cash has already been paid",
                    "A claim priority under the issue's terms, not assured payment",
                    "A guaranteed common dividend",
                ],
                1,
                "Arrears describe a contractual preference; the issuer still needs resources and the applicable conditions to pay.",
            ),
            q(
                "Annual preferred dividends are 3 with two unpaid years. If current dividends must also be paid first, how much of an available 11 remains for common?",
                ["5", "8", "2"],
                2,
                "Arrears of 6 plus the current 3 absorb 9, leaving 2 under the stipulated distribution terms.",
            ),
        ],
    )

    add(
        "1.12",
        "III",
        "Convertible securities and participation",
        "Calculate conversion value and premium while testing the quality of the underlying fixed claim.",
        r"""
## Two sources of value, two sources of error

A convertible security offers a fixed or preferred claim together with a right to exchange it for common shares on stated terms. The conversion feature can provide participation in favorable business outcomes. That attraction does not repair an unsound issuer: the bond's protection and the stock's value may deteriorate together.

Identify face value, conversion ratio, adjustment provisions, maturity, and redemption terms. The conversion price is face value divided by shares delivered. Conversion value is the current share price multiplied by that ratio. A quoted convertible can trade above immediate conversion value because its remaining rights have value, but the size of the premium matters.

A so-called bond floor is an estimate of the comparable nonconvertible claim, not an assured market minimum. Its assumptions include credit quality, rates, and liquidity. A falling share price caused by business distress can coincide with a falling fixed-claim value.

## A worked example

An invented $1,000 bond converts into 25 common shares. Its conversion price is $40. At a common share price of $36, conversion value is $900. If the convertible costs $1,080, its premium over conversion value is $180, or 20% of $900.

Suppose a comparable straight claim is estimated at $850. Paying $1,080 includes $230 above that estimate for the package's additional features and differences. Do not add $850 and $900: the holder normally chooses between claims rather than receiving both principal and the full conversion shares.

## Investigate dilution and forced decisions

Model the share count if every relevant security converts. Compare conversion benefits with coupons or dividends surrendered. An issuer call may force a decision sooner than an investor expected. Read the timing and adjustment provisions before describing the instrument as a bond with free upside.

Your memo should show both a weak credit case and a favorable conversion case. The most attractive feature can dominate attention while the protection needed in adversity remains unexamined.
""",
        r"V_{conversion}=nP_s;\quad \text{premium}=P_c/V_{conversion}-1",
        'ratio = 25\nconversion = ratio * 36\nprint("Conversion price:", 1000 / ratio)\nprint("Conversion value:", conversion)\nprint("Premium (%):", round((1080 / conversion - 1) * 100, 2))',
        "A 1,000-face convertible exchanges for 20 shares. The stock is 45 and the convertible is 990. Calculate conversion price, conversion value, and premium; explain why principal and conversion value cannot simply be added.",
        "Conversion price is 50, conversion value 900, and premium 10%. Conversion exchanges the fixed claim for shares under the stipulated terms; adding both assumes receipt of mutually exclusive payoffs.",
        [
            q(
                "A 1,000-face bond converts into 40 shares. Its conversion price is:",
                ["$40", "$25", "$4"],
                1,
                "Divide face value by conversion shares: 1,000 / 40 = $25.",
            ),
            q(
                "Why can an estimated straight-bond floor fall with the stock?",
                [
                    "Credit quality may deteriorate at the same time",
                    "It is legally fixed at par",
                    "Conversion creates cash automatically",
                ],
                0,
                "Business distress can reduce both debt recovery prospects and equity value; the floor is an estimate.",
            ),
            q(
                "A convertible priced at 1,100 delivers 50 shares worth 20 each. What is the premium over conversion value?",
                ["5%", "10%", "50%"],
                1,
                "Conversion value is 1,000; the 100 premium divided by 1,000 is 10%.",
            ),
        ],
    )

    add(
        "1.13",
        "IV",
        "Common ownership and dividend policy",
        "Evaluate distributions and retention through the economic interests of common shareholders.",
        r"""
## Earnings belong to a business before they become cash to owners

Common shareholders hold the residual interest. They benefit when retained resources earn worthwhile returns or when surplus resources are distributed sensibly. Reported profit is neither automatically distributable cash nor proof that retention benefits owners.

Study the reason for retention: working capital, maintenance, expansion, debt reduction, or an acquisition. Distinguish necessary reinvestment from discretionary growth. A business that must reinvest heavily just to maintain earnings may have less distributable capacity than an equally profitable business with modest maintenance needs.

Dividend yield describes one component of return. A high payout can be financed by borrowing or asset sales and may be unsustainable. A low payout can reflect attractive opportunities or poor capital discipline. Evaluate the use of retained funds rather than assuming either policy is superior.

## A worked example

Alder earns $30 million for common shareholders, pays $12 million of dividends, and retains $18 million. Its payout ratio is 40%; retention is 60%. Suppose management proposes a project costing the retained $18 million that is expected to add $1.8 million of sustainable annual profit. The implied incremental return is 10% under the case assumptions.

If the project instead adds only $0.9 million, the incremental return is 5%. The accounting act of retaining money is identical, but the economic opportunity differs. Compare the uncertain return with an appropriately chosen requirement and examine whether the estimate includes all additional costs.

## Observe results over time

Track incremental capital committed and subsequent operating performance. Acquisitions, share issuance, and changes in business mix complicate attribution. Do not compare a single year's total profit with a single year's retention and call that the return on new capital.

Write an owner-focused question: what can the company do with the next dollar that I could not accomplish as well outside it? Answer with evidence about business opportunities, management decisions, and claims on the cash.
""",
        r"\text{Payout}=D/E;\quad \text{retention}=1-D/E",
        'earnings = 30\ndividends = 12\nprint("Payout:", dividends / earnings)\nprint("Incremental project return:", 1.8 / (earnings - dividends))',
        "Earnings are 40, dividends 10, and a project uses all retained earnings to add 2.4 of recurring annual profit. Calculate payout, retention, and incremental return. Identify an assumption to investigate.",
        "Payout is 25%, retention 75%, and project return 2.4 / 30 = 8%. Investigate whether the additional profit is sustainable and net of maintenance, working-capital, and financing effects relevant to the chosen comparison.",
        [
            q(
                "Earnings of 25 and dividends of 10 give a payout ratio of:",
                ["25%", "40%", "60%"],
                1,
                "10 / 25 = 40%; the remaining 60% is retained in this simplified case.",
            ),
            q(
                "What best supports a retention policy?",
                [
                    "Management's preference for a larger company",
                    "Evidence that incremental investment creates sufficient value for its risk",
                    "The absence of any dividend",
                ],
                1,
                "Retention should be judged by the prospective and realized economics of the resources kept in the business.",
            ),
            q(
                "A company retains 20 to earn 1 of incremental annual profit. A comparable requirement is 9%. What is the key concern?",
                [
                    "Its 5% incremental return is below the requirement",
                    "Retention always creates value",
                    "The payout ratio must be negative",
                ],
                0,
                "1 / 20 = 5%, below 9% under the stipulated comparison; assumptions and risk need further review.",
            ),
        ],
    )

    add(
        "1.14",
        "IV",
        "Share count, repurchases, and owner outcomes",
        "Distinguish mechanical EPS changes from an improvement in the value owned by continuing shareholders.",
        r"""
## Keep the denominator honest

A per-share measure combines company-wide resources with a claim count. Changes in either can alter the result. Stock splits change units; issuance changes the ownership fraction; repurchases use company resources to retire claims. Dilution analysis must include the relevant contingent securities under clearly stated assumptions.

An increase in earnings per share after a repurchase does not establish value creation. The company has spent cash or taken on debt. What matters is the value surrendered compared with the value of claims retired, including financing effects and remaining resilience.

Use a consistent date and share basis. A period's reported EPS may use a weighted-average denominator, while an estimate of value today uses the claims outstanding or expected to participate today. Explain the difference instead of mixing the two measures.

## A worked example

Alder has equity value of $100 million, including $20 million of genuinely excess cash, and 10 million shares. Estimated value is $10 per share. It spends $20 million repurchasing 2.5 million shares at $8. Remaining equity value is $80 million and remaining shares are 7.5 million, giving $10.67 per share under the unchanged operating-value assumption.

If it instead spends the same $20 million at $12, it retires about 1.667 million shares. Remaining value per share is $80 / 8.333 = $9.60. The repurchase label is the same; the purchase price changes the owner outcome.

## Check the financing and opportunity cost

The example assumes the cash was not required to operate, no taxes or transaction costs, and no change in business value. Borrowing for a repurchase can alter risk and required returns. Buying shares before a severe operating deterioration can weaken liquidity.

Compare the repurchase with debt reduction, distributions, and productive investment. A careful memo reconciles cash used, shares retired, new obligations, and the value of each continuing claim.
""",
        r"V_{after/share}=(V_{before}-C)/(N-C/P_{buyback})",
        'for price in [8, 12]:\n    print("Value after repurchase:", round((100 - 20) / (10 - 20 / price), 2))',
        "Equity value is 240 with 20 shares. Spend 24 of excess cash buying shares at 8. Compute remaining per-share value and contrast a two-for-one split.",
        "Three shares are retired, leaving value of 216 and 17 shares: $12.71 versus $12 initially. A two-for-one split alone halves value per share and doubles shares, leaving each owner's economic interest unchanged.",
        [
            q(
                "A two-for-one split, with no other change, does what to ownership percentage?",
                ["Doubles it", "Halves it", "Leaves it unchanged"],
                2,
                "Both the owner's shares and total shares double, so the fraction owned is unchanged.",
            ),
            q(
                "Why is higher EPS after a repurchase insufficient evidence of value creation?",
                [
                    "The cash spent and price paid also affect continuing owners",
                    "Shares never have value",
                    "Repurchases cannot change share count",
                ],
                0,
                "EPS can rise mechanically while the company overpays for shares or weakens its financing position.",
            ),
            q(
                "Equity is worth 60 across 6 shares. Spend 12 repurchasing at 12 per share. What value per remaining share results under unchanged operations?",
                ["$12", "$9.60", "$10"],
                1,
                "Value falls to 48 and shares to 5; 48 / 5 = $9.60, below the initial $10.",
            ),
        ],
    )

    add(
        "1.3",
        "V",
        "Normalize earning power",
        "Reconcile reported earnings to a defensible range of recurring profit across a business cycle.",
        r"""
## Decide what can recur

Earning power is an estimate of what a business can sustain under stated conditions. Start from reported results and construct an explicit bridge. Remove a disposal gain if it does not represent ongoing operations. Restore an omitted recurring cost. Treat a charge called exceptional skeptically if similar charges appear repeatedly.

Use a history long enough to observe relevant business conditions, but recognize structural changes. A simple average of a business that has doubled capacity or lost its main product can be misleading. Adjust for changes in scale and economics before treating the past as representative.

Normalize both favorable and unfavorable items. Adding back every loss while keeping every gain biases the result. Maintain consistent tax treatment and share counts. Present a range if judgments about recurrence cannot be resolved confidently.

## A worked example

Alder's recurring EPS over five comparable years is $2, $3, $4, $3, and $3. The arithmetic average is $3. A separate after-tax property disposal adds $2 to the final year's reported EPS, taking it to $5. Using $5 as sustainable profit would capitalize a gain that cannot repeat without another asset sale.

Suppose the final year also includes a $0.40 after-tax plant closure charge. If this truly concludes a unique exit, an analyst might exclude it when estimating future earnings. If closures occur as part of an ongoing restructuring program, some recurring allowance may be necessary. The label alone cannot decide the adjustment.

## Build the bridge before the multiple

Record reported EPS, each after-tax adjustment, the supporting evidence, and adjusted EPS. Then compare margins, utilization, customer concentration, and required reinvestment across years. A multiple applied to a weakly supported earnings number cannot rescue the analysis.

A conservative conclusion might use $2.50–3.00 until demand and cost stability are better established. Report why the lower endpoint differs from the historical mean. The exercise is economic judgment disciplined by reconciliation, not a search for the largest allowable add-back.
""",
        r"E_{normalized}=E_{reported}-\text{nonrecurring gains}+\text{justified adjustments}",
        'eps = [2, 3, 4, 3, 3]\nprint("Average recurring EPS:", sum(eps) / len(eps))\nprint("Reported EPS including disposal:", eps[-1] + 2)',
        "Reported EPS is 6, including a 2 after-tax disposal gain and a 0.5 after-tax charge. Prepare normalized EPS assuming the charge is either recurring or genuinely isolated.",
        "Keeping the recurring charge gives 6 − 2 = 4. Excluding a genuinely isolated charge gives 4.5. Document evidence for the choice; do not use the higher result just because it supports the desired price.",
        [
            q(
                "Which item is the strongest candidate for exclusion from recurring earnings?",
                [
                    "Routine salaries",
                    "A one-time gain from selling a surplus building",
                    "Normal rent",
                ],
                1,
                "A surplus-building disposal is not an ongoing operating source of profit in the stipulated case.",
            ),
            q(
                "A company reports restructuring charges every year. The best starting treatment is:",
                [
                    "Add all of them back automatically",
                    "Investigate whether a recurring economic cost remains",
                    "Ignore the entire income statement",
                ],
                1,
                "Repeated charges may reflect continuing costs; recurrence must be assessed before excluding them.",
            ),
            q(
                "Reported EPS is 8, including a 3 after-tax disposal gain. No other adjustment is justified. What normalized EPS follows?",
                ["11", "8", "5"],
                2,
                "Subtract the nonrecurring gain from reported earnings: 8 − 3 = 5.",
            ),
        ],
    )

    add(
        "1.15",
        "V",
        "Depreciation and the cost of staying in business",
        "Explain how asset lives affect reported profit and distinguish noncash expense from avoidable economic cost.",
        r"""
## An accounting allocation represents a real resource

Depreciation spreads an asset's recorded cost across accounting periods. The charge is noncash in the current period, but the equipment was paid for and may eventually need replacement. Adding depreciation back to earnings without allowing for necessary reinvestment can exaggerate resources available to owners.

Compare useful-life assumptions with wear, technology, utilization, and replacement plans. An extension of estimated life reduces annual expense immediately even if no additional cash is generated. Conversely, accounting depreciation may exceed or fall short of current maintenance spending for legitimate reasons.

Separate maintenance from growth expenditure where evidence permits. The distinction is an analytical estimate, not a license to classify every costly project as optional expansion. A capacity project can include replacement of worn-out equipment; sustaining a competitive position can require investment beyond physical repair.

## A worked example

A machine costs $60 million with no assumed residual value. Straight-line depreciation over ten years is $6 million annually. Extending the assumed life to fifteen years reduces annual expense to $4 million, raising pretax profit by $2 million without changing current receipts or payments.

Alder reports EBITDA of $30 million. Estimated recurring maintenance investment is $7 million and a representative tax charge is $5 million. A simplified pre-financing, pre-working-capital cash proxy is $18 million. EBITDA alone would exceed that proxy by $12 million. This is not a complete cash-flow valuation: working capital, financing, and other claims remain to be considered.

## Reconcile accounting and economics

Inspect asset age, gross and net carrying amounts, accumulated depreciation, capital spending, and capacity changes. Explain differences over several periods. One year's unusually low capital spending may reflect deferred maintenance that raises future requirements.

Write a sensitivity for the maintenance estimate and show its effect on distributable resources. A business whose value depends on permanently negligible replacement spending needs particularly strong evidence.
""",
        r"D=(\text{cost}-\text{residual})/\text{life}",
        'print("Ten-year depreciation:", 60 / 10)\nprint("Fifteen-year depreciation:", 60 / 15)\nprint("Simplified cash proxy:", 30 - 7 - 5)',
        "An asset costing 80 with no residual is depreciated over 8 rather than 10 years. Calculate the annual difference and explain why adding it back is not automatically justified.",
        "Annual depreciation is 10 versus 8, a difference of 2. Choosing a longer economic life requires evidence. Depreciation is noncash this year but represents capital consumption that may require future replacement.",
        [
            q(
                "An asset costing 45 with zero residual and a 9-year life has annual straight-line depreciation of:",
                ["4", "5", "9"],
                1,
                "45 / 9 = 5 under the stipulated straight-line method.",
            ),
            q(
                "Why can EBITDA overstate funds available to owners?",
                [
                    "It already deducts every cash cost",
                    "Maintenance investment, taxes, and other uses can remain",
                    "It is always negative",
                ],
                1,
                "EBITDA does not by itself deduct required capital spending, taxes, working capital, or financing uses.",
            ),
            q(
                "A cost of 100 is spread over 20 years instead of 10, with zero residual. What happens to annual pretax profit, all else equal?",
                [
                    "It rises by 5 with no immediate cash improvement",
                    "It rises by 10 in cash",
                    "It falls by 5",
                ],
                0,
                "Depreciation falls from 10 to 5, increasing accounting profit by 5 without an immediate cash-flow change.",
            ),
        ],
    )

    add(
        "1.16",
        "V",
        "Inventory, reserves, and profit comparability",
        "Trace how inventory and reserve estimates can shift profit between periods without equivalent economic improvement.",
        r"""
## Accounting choices affect the comparison

Inventory costs become expenses when goods are sold, subject to the reporting framework and the firm's policies. In a changing cost environment, the expense assigned to current sales can differ from the cost of replacing the goods. A favorable reported margin may therefore reflect the release of older, cheaper stock rather than stronger pricing power.

Reserve estimates introduce another source of timing differences. A reduction in an allowance can raise earnings today while future collections or obligations remain uncertain. Study the reserve roll-forward: opening balance, additions, actual uses, acquisitions, and closing balance. A reserve release deserves an explanation tied to new evidence.

This lesson uses simplified economic comparisons. It does not prescribe a particular modern accounting treatment. Real policies differ across reporting frameworks and asset classes; first establish the method the issuer actually uses.

## A worked example

Alder sells 100 units for $15 each. Their recorded cost is $8 per unit, while replacing them would cost $11. Reported gross profit on this simplified batch is $700. A replacement-cost comparison gives $400. The $300 difference matters if the firm must replenish inventory to sustain sales.

Separately, an allowance falls by $2 million solely because management changes an estimate. Pretax profit rises by $2 million in the case. That increase does not represent $2 million of additional customer cash received. Whether the release is justified depends on the underlying evidence.

## Ask what repeats

Compare inventory quantities, unit costs, sales prices, write-downs, and turnover. Falling inventory can temporarily support cash flow while leaving the next period understocked. Rising inventory can reflect growth, seasonality, or unsold goods.

For each adjustment, preserve reported profit and show a separate economic comparison. Do not deduct the same inventory impairment twice through both a carrying-value haircut and an additional earnings charge in a valuation that already incorporates the loss.
""",
        r"GP_{replacement}=Q(P-C_{replacement})",
        'units = 100\nprint("Recorded gross profit:", units * (15 - 8))\nprint("Replacement-cost comparison:", units * (15 - 11))',
        "Sell 200 units at 12. Recorded cost is 7 and replacement cost is 9. Calculate both gross profits and explain the difference to an owner who must replenish inventory.",
        "Recorded gross profit is 1,000; replacement-cost comparison is 600. The 400 difference cannot be assumed distributable while maintaining the same inventory quantity at the new cost.",
        [
            q(
                "Selling 50 units at 20 with replacement cost of 14 gives replacement-cost gross profit of:",
                ["300", "700", "1,000"],
                0,
                "50 × (20 − 14) = 300 before overhead and other expenses.",
            ),
            q(
                "An allowance release raises profit. What should the analyst request?",
                [
                    "Only the new share price",
                    "A roll-forward and evidence supporting the revised estimate",
                    "A higher multiple automatically",
                ],
                1,
                "The release is an estimate change that needs reconciliation to actual underlying developments.",
            ),
            q(
                "Recorded unit cost is 5, replacement cost 8, and 100 units are sold. How much does recorded gross profit exceed the replacement-cost comparison?",
                ["100", "300", "800"],
                1,
                "The cost difference is 3 per unit across 100 units, giving a 300 profit difference.",
            ),
        ],
    )

    add(
        "1.17",
        "V",
        "Profit, cash conversion, and financing strain",
        "Reconcile a simplified earnings-to-cash bridge and identify when growth consumes liquidity.",
        r"""
## Profit can arrive before cash

An income statement recognizes economic activity under accounting rules; a cash-flow analysis asks when resources actually enter or leave. The difference can be normal and temporary. It can also reveal a business that continually reports profit while requiring external finance.

Separate noncash expenses from working-capital investment. A rise in receivables typically absorbs cash relative to recognized revenue. Additional inventory also ties up resources. Growth in operating payables can temporarily finance these uses, but suppliers may not extend terms indefinitely.

The bridge below is an original simplified contemporary worksheet. Its purpose is to continue the book's analytical habit of interrogating reported earnings. It omits many real adjustments and is not a substitute for a complete statement of cash flows.

## A worked example

Alder reports net income of $20 million and depreciation of $6 million. Receivables rise by $8 million, inventory by $5 million, and operating payables by $3 million. With no other adjustments, operating cash flow is 20 + 6 − 8 − 5 + 3 = $16 million. After $7 million of capital spending, cash remaining before financing distributions is $9 million.

If receivables instead rise by $18 million, operating cash flow falls to $6 million and the amount after capital spending becomes −$1 million. Reported net income remains $20 million in this isolated sensitivity. The company must fund the difference through existing cash or financing.

## Follow the cash through the cycle

Determine whether receivable growth reflects timing or poor collection, whether inventory supports future demand, and whether payables are overdue. One period's weak conversion is not proof of low-quality earnings. Persistent unexplained divergence is more informative.

Compare cumulative earnings, cumulative cash generation, investment, and changes in financing over several years. Explain the source of distributions. A dividend paid using borrowed money does not validate the sustainability of earnings.
""",
        r"CFO\approx NI+D-\Delta AR-\Delta Inv+\Delta AP",
        'cfo = 20 + 6 - 8 - 5 + 3\nprint("Operating cash flow:", cfo)\nprint("Cash after capital spending:", cfo - 7)',
        "Net income is 15, depreciation 4, receivables increase 6, inventory increases 2, and payables increase 1. Calculate operating cash and cash after capital spending of 5.",
        "Operating cash is 15 + 4 − 6 − 2 + 1 = 12. Cash after spending is 7. This simplified result excludes financing and any other cash-flow adjustments; investigate whether working-capital uses will reverse.",
        [
            q(
                "An increase in operating receivables, holding other bridge items fixed, generally:",
                [
                    "Adds to cash relative to profit",
                    "Uses cash relative to profit",
                    "Cannot affect cash conversion",
                ],
                1,
                "Recognized revenue has not yet been collected, so the receivables increase is deducted in the simplified bridge.",
            ),
            q(
                "Why compare cumulative cash conversion over several years?",
                [
                    "To distinguish timing differences from persistent financing needs",
                    "To eliminate all uncertainty",
                    "To avoid reading any notes",
                ],
                0,
                "Several periods can reveal whether temporary differences reverse or recurring cash shortfalls accumulate.",
            ),
            q(
                "Net income is 12, depreciation 3, and net operating working capital increases 7. With no other adjustments, operating cash is:",
                ["22", "16", "8"],
                2,
                "12 + 3 − 7 = 8 in the stipulated simplified bridge.",
            ),
        ],
    )

    add(
        "1.4",
        "VI",
        "Net current assets and liquidation haircuts",
        "Calculate NCAV and a separate stressed realization estimate after every senior claim.",
        r"""
## The balance sheet is a starting inventory of claims

Net-current-asset value deducts all liabilities and applicable preferred claims from current assets. It is not ordinary working capital, which deducts only current liabilities. Long-term debt still stands ahead of common owners even when the analyst focuses only on cash, receivables, and inventory.

Recorded current assets need not realize their carrying amounts. Collection quality, obsolescence, restricted cash, and sale conditions affect recovery. Haircuts should be tied to evidence about specific assets. Fixed percentage assumptions are useful for sensitivity exercises, not universal recovery laws.

A discount to NCAV is a research screen. Check whether losses will consume the surplus, whether owners can access it, and whether unrecognized obligations or closure costs remain. A low quoted price does not force liquidation or guarantee realization.

## A worked example

Alder has cash of $40 million, receivables of $60 million, inventory of $80 million, total liabilities of $70 million, no preferred claim, and 10 million common shares. NCAV is $110 million, or $11 per share. A two-thirds screening price would be approximately $7.33, using this stipulated rule.

Apply a 15% haircut to receivables and 40% to inventory. Adjusted resources become 40 + 51 + 48 = $139 million. After liabilities, $69 million remains, or $6.90 per share. Additional closure costs would reduce it further. The original $11 is not a conservative liquidation promise.

## Separate scenarios and deductions

Prepare a reported NCAV column, an orderly-realization case, and a more adverse case. Show every liability and preferred claim exactly once. Include a timeline and expected cash consumption if the thesis requires waiting.

A business can be cheap on a current-asset screen and still destroy owner value. The next analytical step is understanding whether the surplus can survive and eventually reach common shareholders.
""",
        r"NCAV/share=(CA-TL-Pref)/N",
        'ncav = (40 + 60 + 80 - 70) / 10\nadjusted = (40 + 60 * 0.85 + 80 * 0.60 - 70) / 10\nprint("NCAV per share:", ncav)\nprint("Adjusted realization:", adjusted)',
        "Use cash 20, receivables 40, inventory 50, total liabilities 45, preferred claims 5, and 5 shares. Calculate NCAV and an adjusted value using 80% receivable and 50% inventory recovery.",
        "NCAV is (110 − 45 − 5) / 5 = 12. Adjusted value is (20 + 32 + 25 − 45 − 5) / 5 = 5.4. Closure costs and waiting-period losses would require further deductions.",
        [
            q(
                "Current assets 120, total liabilities 70, preferred claims 10, and 4 shares give NCAV per share of:",
                ["10", "12.5", "30"],
                0,
                "(120 − 70 − 10) / 4 = 10; all liabilities and the preferred claim are deducted.",
            ),
            q(
                "What distinguishes NCAV from ordinary working capital?",
                [
                    "NCAV ignores long-term debt",
                    "NCAV deducts total liabilities and applicable preferred claims",
                    "They are always identical",
                ],
                1,
                "Working capital uses current liabilities; the common-owner NCAV screen must also recognize other senior claims.",
            ),
            q(
                "Cash is 10, receivables 20 at 75% recovery, inventory 30 at 50%, and total senior claims 25. What adjusted residual remains?",
                ["35", "20", "15"],
                2,
                "10 + 15 + 15 − 25 = 15, before any additional realization costs.",
            ),
        ],
    )

    add(
        "1.18",
        "VI",
        "Hidden obligations and the realization clock",
        "Stress an asset surplus for cash burn, closure costs, and claims omitted from a first-pass screen.",
        r"""
## Time can consume the apparent bargain

An asset-based thesis requires more than a balance-sheet surplus. The business may continue losing cash while owners wait for a sale, restructuring, or change in policy. Management may invest the surplus in an unattractive project. A static calculation should therefore be accompanied by a timeline.

List restrictions on cash, commitments, guarantees, customer deposits, disputed obligations, and likely realization expenses. In contemporary accounts, some lease obligations and other items may already be recognized. Reconcile the claims schedule to recorded liabilities before adding any incremental estimate, so that you do not deduct the same obligation twice.

Distinguish a known liability, an estimated additional cost, and a downside contingency. Show the probability or scenario premise if relevant rather than presenting all possibilities as certain cash payments. The objective is a transparent range.

## A worked example

An initial asset screen leaves $40 million for common shareholders. The proposed realization takes two years. Expected net operating cash burn is $6 million each year, incremental closure costs are $5 million, and an additional obligation not included in the original claims schedule is estimated at $3 million. The residual before discounting is 40 − 12 − 5 − 3 = $20 million.

At a stipulated 10% annual discount rate, a single $20 million receipt at the end of year two has present value of about $16.53 million. This timing simplification differs from a detailed schedule in which individual costs occur earlier; state which model you use.

## Demand a path to realization

Identify who can initiate a sale or distribution, what approvals and financing are required, and what prevents delay. A catalyst is an event with a plausible mechanism, not just the hope that investors notice a low multiple.

Track the thesis through time. Compare actual cash burn with the estimate and update value when evidence changes. A lower share price cannot offset a vanishing asset surplus indefinitely.
""",
        r"V_0=(A-\text{burn}-\text{incremental costs})/(1+r)^T",
        'residual = 40 - 6 * 2 - 5 - 3\nprint("Residual at realization:", residual)\nprint("Simplified present value:", round(residual / 1.10 ** 2, 2))',
        "A surplus of 30 faces three years of annual cash burn of 4 and incremental closure costs of 6. Calculate the residual and its value if all net proceeds arrive in year three at an 8% discount rate.",
        "Residual is 30 − 12 − 6 = 12. Discounted value is 12 / 1.08³ ≈ 9.53. A more detailed model would date each cash flow separately; delay and further burn can undermine the bargain.",
        [
            q(
                "A balance-sheet surplus of 25 loses 3 annually for two years and incurs 4 in closure costs. Residual is:",
                ["15", "18", "21"],
                0,
                "25 − 2 × 3 − 4 = 15 before any discounting or other claims.",
            ),
            q(
                "Before adding a lease estimate to liabilities, the analyst should:",
                [
                    "Assume leases are never recorded",
                    "Reconcile it with obligations already included",
                    "Deduct it twice for conservatism",
                ],
                1,
                "Double counting a recorded obligation creates an incorrect claims bridge rather than a sound conservative estimate.",
            ),
            q(
                "A net realization of 22 arrives exactly two years from now. At a stipulated 10% discount rate its present value is approximately:",
                ["18.18", "20", "26.62"],
                0,
                "22 / 1.10² = 18.18; timing reduces present value even if the nominal recovery is achieved.",
            ),
        ],
    )

    add(
        "1.19",
        "VI",
        "Book value, intangibles, and asset productivity",
        "Explain why book value is neither a universal floor nor a complete account of business worth.",
        r"""
## Interpret what the carrying amount measures

Book equity is the residual of recognized assets and liabilities under accounting conventions. It can reflect historical costs, estimates, acquisitions, and past losses. It is useful evidence about capital supplied and resources recorded, but it does not automatically measure sale proceeds or sustainable earning power.

Tangible assets may be specialized, obsolete, or costly to remove. Intangible assets can be economically valuable even when little appears on the balance sheet. Conversely, an acquisition premium recorded as goodwill does not itself establish value that a new buyer would pay.

Separate an asset's independent realization value from its contribution to an operating system. Customer relationships, trained staff, and distribution arrangements can support earnings without being readily saleable in isolation. The analytical premise determines how to treat them.

## A worked example

Alder reports assets of $200 million, including $50 million of goodwill, and liabilities of $120 million. Book equity is $80 million. A simple tangible-equity calculation removes goodwill, leaving $30 million. With 10 million shares, the two figures are $8 and $3 per share.

Neither figure settles value. If tangible assets can realize only $130 million in total after removing goodwill and considering recoveries, the residual before further costs is $10 million. Alternatively, a durable profitable business could have going-concern value exceeding book equity. Those are separate hypotheses requiring different evidence.

## Connect assets to earning power

Compare the resources required to generate normalized profit with the profit actually earned. A large asset base earning very little may signal poor economics, excess capacity, or understated future improvement. A small recorded asset base earning a great deal requires an explanation of durability and competition.

Avoid declaring every intangible worthless or every high return permanent. Write what a buyer would need to recreate, what could be sold independently, and what might disappear if the organization stopped operating.
""",
        r"\text{Tangible equity}=\text{assets}-\text{liabilities}-\text{goodwill}",
        'book = 200 - 120\ntangible = book - 50\nprint("Book and tangible equity per share:", book / 10, tangible / 10)',
        "Assets are 150 including 35 goodwill; liabilities are 90 and there are 5 shares. Calculate book and tangible equity per share, then state why neither must equal intrinsic value.",
        "Book equity is 60, or 12 per share. Tangible equity is 25, or 5 per share. Recoverability, unrecorded business strengths, obligations, and earning power can produce a different economic estimate.",
        [
            q(
                "Assets 100, liabilities 60, and goodwill 15 imply tangible equity of:",
                ["25", "40", "55"],
                0,
                "100 − 60 − 15 = 25 under this simplified tangible-equity definition.",
            ),
            q(
                "Which statement about book value is defensible?",
                [
                    "It guarantees a sale price",
                    "It is accounting evidence that needs economic interpretation",
                    "It captures all internally developed strengths perfectly",
                ],
                1,
                "Carrying amounts and recognition conventions do not directly establish realizable proceeds or complete earning capacity.",
            ),
            q(
                "A company trades below tangible book but earns persistent losses and owns obsolete machinery. What follows?",
                [
                    "The discount guarantees recovery",
                    "The losses and asset recoverability can invalidate the apparent floor",
                    "Earnings no longer matter",
                ],
                1,
                "Recorded tangible assets may not realize book amounts, and operating losses can consume the remaining resources.",
            ),
        ],
    )

    add(
        "1.20",
        "VII",
        "Compare businesses on consistent terms",
        "Construct a peer comparison with matching claims, normalized earnings, and accounting assumptions.",
        r"""
## A multiple compresses assumptions

A price-to-earnings ratio combines the market value of common equity with earnings attributable to common owners. An enterprise multiple pairs the value of operating claims with an operating measure. Mixing enterprise value with common EPS produces an incoherent comparison.

Cheapness is relative to an economic denominator. Two identical reported multiples can conceal different leverage, cyclicality, accounting policies, reinvestment needs, and customer concentration. Begin with a small comparable set and explain the reasons for inclusion. A large automated ranking does not establish comparability.

Normalize earnings before comparing multiples. Record how taxes, unusual items, minority interests, and diluted shares are treated. A low multiple at peak profit can be more expensive than a higher multiple on depressed but recoverable earnings.

## A worked example

Alder has equity market value of $120 million, debt of $60 million, and excess cash of $20 million. Enterprise value is $160 million. Normalized EBIT is $20 million, giving EV/EBIT of 8 times. A peer has equity value of $150 million, debt of $10 million, no excess cash, and normalized EBIT of $20 million: also 8 times.

The companies have the same enterprise multiple but different financing risk. Alder's common holders stand behind more net debt. If operating values fall by the same amount, the percentage impact on their smaller residual equity can be larger.

## Explain the residual difference

Build a bridge from reported to comparable figures for each company. Then identify the facts a multiple does not capture: asset quality, business durability, governance, and required reinvestment. A peer's market price is another market observation, not independent proof of intrinsic value.

Use comparables to challenge an estimate. If your conclusion requires a much higher multiple than similarly exposed businesses, explain the difference in economics. Do not import the peer average solely because it creates an attractive upside.
""",
        r"EV=\text{equity market value}+\text{debt}-\text{excess cash}",
        'ev = 120 + 60 - 20\nprint("Enterprise value:", ev)\nprint("EV / normalized EBIT:", ev / 20)',
        "Company A has equity 90, debt 40, excess cash 10, and normalized EBIT 15. Company B has equity 100, debt 20, no excess cash, and EBIT 12. Compare EV/EBIT and name two reasons the lower ratio may not be the better investment.",
        "A is 120 / 15 = 8 times; B is 120 / 12 = 10 times. A may have greater cyclicality, weaker asset quality, more financing risk, or greater reinvestment needs. The ratio alone cannot settle value.",
        [
            q(
                "Equity market value 80, debt 30, and excess cash 10 imply enterprise value of:",
                ["60", "100", "120"],
                1,
                "80 + 30 − 10 = 100, under the simplified claims bridge.",
            ),
            q(
                "Which pairing is internally consistent?",
                [
                    "Enterprise value / common EPS",
                    "Equity price per share / common EPS",
                    "Share price / total revenue",
                ],
                1,
                "Price per common share and common earnings per share refer to matching claims and units.",
            ),
            q(
                "A firm has EV of 180 and peak EBIT of 30, but normalized EBIT is 18. Its normalized EV/EBIT is:",
                ["6 times", "10 times", "12 times"],
                1,
                "180 / 18 = 10 times; the 6-times multiple uses peak earnings and understates the normalized ratio.",
            ),
        ],
    )

    add(
        "1.21",
        "VII",
        "Special situations and contingent outcomes",
        "Analyze a price discrepancy using completion, failure, timing, and funding scenarios.",
        r"""
## A spread describes a contingent claim

A announced cash transaction, liquidation, or exchange can create a difference between today's price and a possible future receipt. The spread is not free profit. Completion can fail, timing can stretch, and interim financing or liquidity can become expensive.

Start with the actual mechanism that turns the security into cash or another claim. List conditions, required approvals, financing dependencies, and what the holder owns if the event fails. Treat probability estimates as assumptions to be tested, not objective frequencies merely because a spreadsheet accepts them.

A positive expected payoff can coexist with a large loss in an adverse outcome. Position size, correlation among events, and the ability to hold through delays matter separately from the expected value calculation.

## A worked example

A fictional target costs $45. A stipulated cash deal pays $50 if completed; estimated standalone value after failure is $32. If the analyst assumes an 80% completion probability, expected terminal proceeds are 0.8 × 50 + 0.2 × 32 = $46.40, before discounting and costs. Expected gain is $1.40, while failure loses $13.

Ignoring timing and costs, the break-even completion probability solves 45 = p × 50 + (1 − p) × 32. It is 13 / 18 = 72.22%. A lower assumed probability produces a negative expected payoff. Longer waiting periods can reduce attractiveness even if the event ultimately completes.

## Write both stories

Describe why completion should occur and what evidence would support failure. Avoid treating management's target date as a certainty. Test the failure value independently; it may have changed since the announcement.

Keep the arithmetic, probability judgment, and risk budget separate. An attractive spread may compensate for a risk the portfolio cannot tolerate. The decision should survive a plausible adverse scenario rather than relying entirely on the most likely outcome.
""",
        r"p_{break-even}=(P-V_{failure})/(V_{success}-V_{failure})",
        'print("Expected proceeds:", 0.8 * 50 + 0.2 * 32)\nprint("Break-even probability:", (45 - 32) / (50 - 32))',
        "An event costs 28, pays 35 on success, and leaves value of 15 on failure. Calculate break-even probability and expected proceeds at a 70% assumed success probability, before timing and costs.",
        "Break-even probability is (28 − 15) / (35 − 15) = 65%. Expected proceeds are 29, a gain of 1; failure loses 13. Costs, delay, and an overstated failure value could erase the apparent advantage.",
        [
            q(
                "Success pays 40, failure 20, and price is 30. Break-even probability before costs is:",
                ["25%", "50%", "75%"],
                1,
                "(30 − 20) / (40 − 20) = 50%.",
            ),
            q(
                "A positive expected event payoff establishes:",
                [
                    "No possible loss",
                    "An assumption-dependent average, not guaranteed completion",
                    "An unlimited appropriate position size",
                ],
                1,
                "The adverse outcome remains possible and can be much larger than the expected gain.",
            ),
            q(
                "A claim costs 24, pays 30 on success and 10 on failure. At an assumed 60% success probability, expected proceeds are:",
                ["22", "24", "26"],
                0,
                "0.6 × 30 + 0.4 × 10 = 22, below the price even before costs and discounting.",
            ),
        ],
    )

    add(
        "1.22",
        "VII",
        "From an estimate to a monitored decision",
        "Write an investment memo with an opposing case, price discipline, and explicit review triggers.",
        r"""
## Analysis must lead to a revisable decision

A useful memo connects evidence to action. State the security, claim priority, value premise, conservative range, required discount, and source of realization. Then present the strongest opposing case. If the adverse argument is trivial, the research may not yet have confronted the real uncertainty.

Separate business review triggers from price review triggers. A lost customer, covenant change, or unexpected cash drain can alter value. A quotation reaching a target can alter the prospective return without changing the business. Both matter, but they should not be confused.

Position sizing introduces portfolio considerations beyond the security estimate. Several apparently unrelated bargains may depend on the same refinancing market or economic cycle. A discount to value does not eliminate the consequences of concentrated exposure.

## A worked example

A researcher estimates weak-case value at $40 per share and requires a 30% discount, producing a maximum purchase price of $28. The stock trades at $26. The memo identifies a customer representing 35% of revenue and a debt maturity in eighteen months as its two major risks.

A stress loss of 40% on the position would cost 2% of portfolio value if the initial position were 5%, assuming other holdings were unchanged. This is a scenario budget, not a bound on possible loss. A larger impairment or correlated losses could be worse.

## Use a repeatable review

Record the dated evidence supporting each assumption, the next expected information release, and the condition requiring reassessment. Compare actual results with the thesis rather than only with the share price. Preserve the original memo so later success does not erase the uncertainties present at purchase.

A sound conclusion can be buy, watch, avoid, or insufficient evidence. No numerical valuation obliges a trade. What matters is whether the claim, price, and evidence together satisfy the stated process.
""",
        r"\text{Scenario portfolio loss}=\text{position weight}\times\text{position loss}",
        'print("Maximum price:", 40 * 0.70)\nprint("Scenario portfolio loss (%):", 0.05 * 0.40 * 100)',
        "Write a six-line memo for value 50, price 32, and a required 35% discount. Include a 6% position exposed to a 50% stress loss, one evidence gap, and a review trigger.",
        "Maximum price is 32.50, so 32 satisfies the numerical rule. Scenario portfolio loss is 3%. A complete memo still needs evidence supporting value, an opposing case, the unresolved fact, and a trigger tied to business or financing developments.",
        [
            q(
                "A 4% position loses 50% while other holdings are unchanged. Portfolio impact is:",
                ["2% loss", "4% loss", "50% loss"],
                0,
                "0.04 × 0.50 = 0.02, or 2% of the starting portfolio.",
            ),
            q(
                "Which is a business-value review trigger?",
                [
                    "A change in the chart's color",
                    "Loss of the principal customer supporting normalized earnings",
                    "A round-number share price alone",
                ],
                1,
                "A major customer loss can directly invalidate the earnings assumptions used to estimate value.",
            ),
            q(
                "Weak-case value is 60 and the required discount is 40%. The quote is 38. What follows?",
                [
                    "The quote passes automatically",
                    "The maximum price is 36, so the stated rule fails",
                    "The required price is 24",
                ],
                1,
                "60 × 0.60 = 36; a quote of 38 is above the decision boundary.",
            ),
        ],
    )

    add(
        "1.5",
        "VIII",
        "The Graham growth heuristic: a separate extension",
        "Audit the units and sensitivity of a later growth heuristic without treating it as the 1940 book's valuation method.",
        r"""
## Keep historical layers separate

This optional bridge retains the earlier course's growth worksheet. The expression below is a later heuristic commonly associated with Graham; it is not the organizing valuation method of the 1940 Security Analysis course. The course does not use it to replace analysis of earning power, assets, and creditor protection.

The worksheet combines EPS, an assumed growth input, and a reference-yield scaling factor. Its constants are fixed assumptions rather than a complete economic model. It has no explicit cash-flow forecast, reinvestment schedule, fade of competitive advantage, or probability of failure.

In this expression, growth and yield are entered in percentage points: 5 for 5%, and 4.4 for 4.4%. Mixing decimals with percentage points can create an apparently precise but meaningless answer. The mathematical requirement of a positive yield denominator does not establish that the resulting value is appropriate.

$$V=EPS(8.5+2g)\frac{4.4}{Y}$$

## A worked example

With EPS of $4, growth input of 5, and yield input of 4.4, the worksheet gives $74. Raising the yield input to 6 reduces the result to about $54.27. Keeping the original yield but raising growth to 10 produces $114.

These large changes come from a few assumptions, without any explicit modeling of the investment needed to achieve growth. If normalized EPS is actually $3 rather than $4, every result falls by 25%. Sensitivity can overwhelm the supposed discount to the market price.

## Use the worksheet as a critique

Reproduce the calculation, label every input, and explain what the formula leaves out. Compare its conclusion with a separate asset and earning-power analysis. A disagreement is a reason to investigate assumptions, not to average three outputs until the desired answer emerges.

For book study, keep this exercise in the extension unit. Its role is to demonstrate the danger of compressing a complex business into a popular rule of thumb.
""",
        r"V=EPS(8.5+2g)4.4/Y",
        'eps = 4\ngrowth = 5\nfor yield_points in [4.4, 6]:\n    print("Heuristic value:", round(eps * (8.5 + 2 * growth) * 4.4 / yield_points, 2))',
        "Use EPS 2, growth input 3, and yield input 4.4, then change yield to 5.5. Explain two economic elements absent from the worksheet.",
        "Values are 29 and 23.20. The formula does not explicitly model required reinvestment, duration of growth, future dilution, or failure risk. Treat its output as an assumption sensitivity, not an independent valuation conclusion.",
        [
            q(
                "In this growth worksheet, a 5% growth input is entered as:",
                ["0.05", "5", "500"],
                1,
                "The worksheet uses percentage-point inputs for both growth and yield, preserving its stated convention.",
            ),
            q(
                "How should this worksheet be classified within the course?",
                [
                    "The core method of the 1940 text",
                    "A separate later heuristic with substantial limitations",
                    "A guaranteed purchase rule",
                ],
                1,
                "The course distinguishes this later expression from the original book's broader analytical methods.",
            ),
            q(
                "EPS is 3, growth input 2, and yield input 4.4. What does the stipulated heuristic produce?",
                ["25.5", "37.5", "51"],
                1,
                "3 × (8.5 + 4) × 4.4 / 4.4 = 37.5, before considering the heuristic's economic limitations.",
            ),
        ],
    )

    add(
        "1.23",
        "VIII",
        "Modern bridge: earning-power and cash-flow valuation",
        "Convert operating value into common equity and test discount-rate assumptions in a transparent modern model.",
        r"""
## A modern model should preserve analytical discipline

This extension uses contemporary cash-flow notation to apply the course's emphasis on normalized operations and conservative assumptions. It is not attributed to the 1940 text. Begin by defining the cash flow: to the business before debt financing, or to common owners after financing. Use a discount rate consistent with that claim.

A no-growth operating model can capitalize sustainable cash available before financing at an assumed required return. A growing perpetuity additionally assumes stable growth, a consistent reinvestment policy embedded in cash flow, and a discount rate above growth. Those are strong assumptions.

After estimating operating value, add only excess nonoperating assets and deduct debt and other senior claims not already reflected. Do not deduct debt twice if the modeled cash flow and discount rate already value common equity directly.

## A worked example

Alder's sustainable annual cash flow to operating capital is estimated at $15 million. A no-growth perpetuity discounted at 10% gives operating value of $150 million. Add $10 million of excess cash and deduct $40 million of debt: common value is $120 million, or $12 with 10 million shares.

At a 12% required return, operating value falls to $125 million and common value to $9.50 per share. If next year's cash flow is still $15 million but a perpetual 2% growth assumption is introduced at a 10% rate, operating value becomes $187.5 million. The increase is an assumption effect, not a newly discovered asset.

## Test the model's dependencies

Show a grid of sustainable cash flow and required return. If growth is included, explain how investment requirements are funded and why the growth-rate assumption is sustainable. Compare with asset evidence without adding mutually exclusive values.

A model is useful when it makes the decision's dependencies inspectable. Its formula does not reduce uncertainty unless the underlying evidence improves.
""",
        r"EV=FCF_1/(r-g);\quad V_{common}=(EV+Cash-Debt)/N",
        'for rate in [0.10, 0.12]:\n    enterprise = 15 / rate\n    print("No-growth equity per share:", (enterprise + 10 - 40) / 10)',
        "Sustainable unlevered cash flow is 12, excess cash 8, debt 28, and shares 8. Calculate no-growth equity value per share at 8% and 10% required returns.",
        "At 8%, operations are 150 and equity is 130, or 16.25 per share. At 10%, operations are 120 and equity is 100, or 12.50 per share. These values require sustainable cash flow and consistent treatment of financing claims.",
        [
            q(
                "A growing perpetuity with positive next-year cash flow requires which condition for a finite positive value?",
                ["r = g", "r > g", "r < g"],
                1,
                "The denominator r − g must be positive under this perpetuity model.",
            ),
            q(
                "When valuing unlevered operating cash flows, how is debt generally handled in the final claims bridge?",
                [
                    "Add debt to common value",
                    "Deduct debt to move from operating to common equity value",
                    "Ignore all claims",
                ],
                1,
                "Operating value belongs to providers of capital; debt must be deducted when isolating the common residual.",
            ),
            q(
                "No-growth operating cash flow is 10 at a 10% rate, with excess cash 5, debt 25, and 10 shares. Common value per share is:",
                ["8", "10", "13"],
                0,
                "Operating value is 100; common value is 100 + 5 − 25 = 80, or 8 per share.",
            ),
        ],
    )

    add(
        "1.24",
        "VIII",
        "Capstone: the Alder investment committee",
        "Deliver a reconciled valuation memo that combines credit protection, earning power, assets, and price discipline.",
        r"""
## Your case file

All amounts below are fictional millions except per-share figures. The date is the case decision date; assume all listed information was available then. Alder has 10 million common shares at $6.20. Cash is 30, of which 10 is required for operations. Receivables are 50, inventory 70, and recorded fixed assets 90. Total liabilities are 100, including interest-bearing debt of 60. There is no preferred claim.

Reported EBIT is 24, including a nonrecurring pretax asset-sale gain of 4. Annual interest is 5. Weak-case recurring EBIT is 12. For a separate modern no-growth model, use a stipulated sustainable unlevered cash-flow range of 9–12 and a required return of 10%. These cash flows already reflect operating investment needs and taxes.

For an asset realization scenario, recover cash in full, 80% of receivables, 50% of inventory, and 20% of fixed assets. Deduct all recorded liabilities and incremental closure costs of 8. Assume no additional burn in this immediate-realization scenario; then challenge that assumption.

## A worked example

Normalized EBIT is 20 and normal interest coverage is 4 times; weak coverage is 2.4 times. NCAV is (30 + 50 + 70 − 100) / 10 = $5 per share. Adjusted realization is (30 + 40 + 35 + 18 − 100 − 8) / 10 = $1.50.

No-growth operating value is 90–120. Add only 20 of excess cash, deduct debt of 60, and divide by 10: common value is $5–8 per share. The other operating liabilities are reflected in this case's stipulated operating cash flows; the asset realization separately deducts all liabilities. Explain that difference in your claims bridge.

At $6.20 the discount to the upper endpoint is 22.5%, but the quote exceeds the lower endpoint. A required 30% discount to the $5 conservative operating estimate implies a maximum price of $3.50. The current quote fails that rule.

## Committee deliverable

Write 600–900 words with a claims map, normalized earnings bridge, three valuation premises, downside case, price decision, and monitoring plan. Cite case facts and clearly label your assumptions. Explain why the three values should not be added or mechanically averaged.

Self-assess five criteria, each from 0 to 4: traceable evidence, correct reconciliations, consistent valuation premises, serious downside analysis, and a revisable decision. A score of 3 means correct with explicit limitations; 4 also explains a plausible alternative. Aim for 15/20 with no zero. The notebook stores your memo; the app grades the numerical final exam separately and does not certify the written work.
""",
        r"P_{max}=V_{conservative}(1-M_{required})",
        'print("Normalized coverage:", (24 - 4) / 5)\nprint("Weak coverage:", 12 / 5)\nprint("NCAV per share:", (30 + 50 + 70 - 100) / 10)\nprint("Adjusted realization:", (30 + 50 * .8 + 70 * .5 + 90 * .2 - 100 - 8) / 10)\nfor cash_flow in [9, 12]:\n    print("Operating equity estimate:", (cash_flow / .10 + 20 - 60) / 10)\nprint("Maximum conservative price:", 5 * .70)',
        "Write the committee memo in your notebook. Then stress the case with two years of cash burn totaling 12 before asset realization, and raise the operating discount rate to 12%. Does either sensitivity support the $6.20 quote under the stipulated 30% rule?",
        "Ignoring additional timing discount, realization falls from 15 to 3 in total, or $0.30 per share. At 12%, operating equity is (75 + 20 − 60) / 10 to (100 + 20 − 60) / 10 = $3.50–6.00. A 30% discount to $3.50 permits $2.45. Neither sensitivity supports the current quote under the chosen rule. A strong memo also questions the timing, recoveries, and durability of cash flow.",
        [
            q(
                "In the capstone, what cash may be added separately to the operating valuation?",
                [
                    "All 30",
                    "Only the 20 excess over operating needs",
                    "None of the cash can ever have value",
                ],
                1,
                "The 10 required for operations supports the modeled business; adding all cash would count that portion twice.",
            ),
            q(
                "Which capstone conclusion follows from the stipulated 30% discount to conservative value of 5?",
                [
                    "Maximum price is 3.50",
                    "Any price below 8 passes",
                    "Add NCAV to operating value",
                ],
                0,
                "5 × 0.70 = 3.50; neither choosing only the optimistic endpoint nor adding overlapping values follows the rule.",
            ),
            q(
                "A revised capstone estimates conservative common value at 7 and requires a 30% discount. The quote is 5.20. Which decision follows the stated rule?",
                [
                    "Accept because 5.20 is below 7",
                    "Reject at this quote; maximum price is 4.90",
                    "Raise value until it passes",
                ],
                1,
                "7 × 0.70 = 4.90, below 5.20. The analysis must retain its decision discipline rather than adjust assumptions to fit price.",
            ),
        ],
    )

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
                ]
            ],
        },
        checkpoints,
    )
