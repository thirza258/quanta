"""Original careful-investor companion; no reproduced book text or exercises."""

from applied_courses import checkpoints_for, study
from book_courses import finish

BOOK = (
    "Benjamin Graham & Jason Zweig · The Intelligent Investor, book information",
    "https://jasonzweig.com/books/the-intelligent-investor/",
)
ALLOCATION = (
    "U.S. SEC · Investor.gov: asset allocation and diversification",
    "https://www.investor.gov/introduction-investing/getting-started/asset-allocation",
)
FEES = (
    "U.S. SEC · Investor.gov: understanding investment fees",
    "https://www.investor.gov/introduction-investing/getting-started/understanding-fees",
)
FRAUD = (
    "U.S. SEC · Investor.gov: avoiding investment fraud",
    "https://www.investor.gov/protect-your-investments/fraud/how-avoid-fraud/what-you-can-do-avoid-investment-fraud",
)
FILINGS = (
    "U.S. SEC · EDGAR company disclosure APIs",
    "https://www.sec.gov/search-filings/edgar-application-programming-interfaces",
)


def build_intelligent_investor():
    modules = []

    def add(
        title,
        theme,
        objective,
        principle,
        case,
        workflow,
        formula,
        code,
        task,
        solution,
        questions,
        refs,
    ):
        index = len(modules) + 1
        rows = []
        for offset, (prompt, correct, wrong1, wrong2, explanation) in enumerate(questions):
            options = [correct, wrong1, wrong2]
            shift = (index + offset) % 3
            options = options[shift:] + options[:shift]
            rows.append((prompt, options, options.index(correct), explanation))
        item = study(
            f"11.{index}",
            (index - 1) // 4 + 1,
            title,
            objective,
            principle,
            case,
            workflow
            + "\n\n### Build your careful-investor plan\n\nWrite the calculation, decision rule and one reason the conclusion might be wrong in your notebook. Add the evidence to investor-plan.md. Read the named theme in your own copy of The Intelligent Investor; these explanations and fictional cases are original Quanta material, not reproduced chapters or publisher exercises. The worksheet calculates the case and keeps the price sandbox in cash. Its chart is not an investment recommendation or a test of Graham's approach.",
            formula,
            code,
            task,
            solution,
            rows,
            refs,
        )
        item["minutes"] = 30
        item["reading"] = (
            f"Book companion theme: {theme}. 30-minute session: 10 minutes of reading, 8 minutes of calculations, and 12 minutes of investor-plan work. Modern product, fraud and planning examples are course extensions, not claims about Graham's historical recommendations."
        )
        modules.append(item)

    add(
        "Intelligent investing starts with temperament",
        "Investor temperament and a disciplined process",
        "Define careful investing as a repeatable decision process rather than an IQ contest.",
        "In this course, an intelligent investor is someone who can work within limits, examine evidence and maintain a deliberate process when prices provoke emotion. Fast calculation and a confident forecast cannot replace those habits. The Indonesian phrase investor yang hati-hati captures the intended attitude: think through consequences, acknowledge uncertainty and avoid commitments whose downside you cannot carry.\n\nA good decision can have a disappointing outcome, while an impulsive decision can be lucky. Evaluate what was knowable at the time: the investment's claim, price, costs, alternatives and possible failure. Write your reasons before buying and revisit them on a schedule. This creates evidence about the quality of the process instead of rewriting a story to fit each price movement.",
        "Rani buys a diversified allocation after documenting a ten-year goal and a loss scenario; the market falls 15%. Dito buys a promoted stock without reading disclosures and gains 20%. Those two outcomes alone cannot establish which process deserves repetition. Starting wealth of 100 falls to 85 in Rani's case, but whether she can continue depends on her plan and circumstances.",
        "Start the investor plan with goals, limits and a decision journal. Write one behavior you will follow after a large gain and one after a large loss. Keep the quality of the original decision separate from its realized result.",
        r"\mathrm{decision\ review}=f(\mathrm{available\ evidence},\mathrm{alternatives},\mathrm{downside},\mathrm{process})",
        'print("Wealth after a 15% fall:", 100 * (1 - 0.15))',
        "Compare Rani's and Dito's decision processes without using their outcomes as the only evidence. Draft three observable habits of a careful investor.",
        "Rani ends at 85 in the example, but a process review examines her evidence, horizon and capacity. Dito's gain does not validate an unexamined promotion. Useful habits include documenting assumptions, checking disclosures and applying a scheduled review rule.",
        [
            (
                "In this course, intelligent investing primarily emphasizes:",
                "Disciplined judgment within one's limits",
                "Winning every short-term forecast",
                "The fastest reaction to every price tick",
                "The course emphasizes a repeatable process, evidence and temperament under uncertainty.",
            ),
            (
                "Wealth of 100 after a 15% decline becomes:",
                "85",
                "115",
                "95",
                "A 15% loss leaves 100 × 0.85 = 85.",
            ),
            (
                "A speculative purchase rises sharply. That outcome alone proves:",
                "Neither the quality nor repeatability of the original process",
                "That checking evidence was unnecessary",
                "That the next purchase must also rise",
                "A favorable outcome can occur through luck and does not validate the decision method.",
            ),
            (
                "What makes a decision journal useful?",
                "Recording reasons before outcomes can rewrite memory",
                "Adding only winning trades later",
                "Replacing all evidence with confidence scores",
                "Contemporaneous reasons allow a fairer review of what the investor knew and assumed.",
            ),
        ],
        [BOOK, ALLOCATION],
    )

    add(
        "Investment, speculation and a business owner's claim",
        "Investment versus speculation",
        "Distinguish analysis of a security's claim from a bet on another buyer's enthusiasm.",
        "A share represents an economic claim on a business, while its quoted price is the amount another participant currently offers to transact. An investment argument examines the business, financing, expected distributions and price paid. A speculative argument may rely mainly on a near-term price move or someone else's willingness to pay more. The label depends on the reasoning and risk assumed, not merely on holding period or the word 'stock'.\n\nNeither a popular company nor a low nominal share price makes an investment suitable. A strong business can be overpriced; a weak business can still rise temporarily. If a learner chooses to study speculation, keep its assumptions and potential full loss explicit rather than allowing it to masquerade as required long-term capital. This course does not prescribe a personal speculative allocation.",
        "Cedar has 1,000 shares and a quoted price of 12, giving equity market value of 12,000. Buying ten shares creates a 1% equity ownership interest, not ownership of 1% of gross assets free of creditors. An argument based only on a rumor of tomorrow's price target has not analyzed that residual claim.",
        "Write two purchase rationales for the same fictional share: one based on business evidence and valuation uncertainty, one based on anticipated price action. Identify the missing evidence in each without assuming either return in advance.",
        r"\mathrm{ownership\ fraction}=n/N,\qquad \mathrm{equity\ market\ value}=PN",
        'print("Ownership fraction:", 10 / 1000)\nprint("Equity market value:", 12 * 1000)',
        "Calculate ownership and market value, distinguish the two rationales and explain why a long holding period does not automatically turn speculation into investment.",
        "Ten of 1,000 shares represent 1%; equity market value is 12,000. Creditors retain their senior claims. The argument must address evidence and price; elapsed holding time cannot supply missing analysis.",
        [
            (
                "Ten shares out of 1000 outstanding represent ownership of:",
                "1%",
                "10%",
                "0.1%",
                "Ownership fraction is 10/1000 = 0.01, or one percent.",
            ),
            (
                "A low nominal share price by itself establishes:",
                "Neither cheap valuation nor suitable risk",
                "A bargain independent of shares outstanding",
                "Guaranteed principal protection",
                "Price must be evaluated relative to the economic claim, share count and business evidence.",
            ),
            (
                "Holding an unexamined promotion for several years automatically changes it into:",
                "Neither a sound analysis nor a justified investment",
                "A fully analyzed investment",
                "A senior creditor claim",
                "A longer holding period does not repair the missing reasoning at purchase.",
            ),
            (
                "Equity ownership gives a claim on:",
                "Residual business value after senior claims",
                "Gross assets without any liabilities",
                "A guaranteed daily price increase",
                "Common equity is a residual claim rather than an unencumbered share of gross assets.",
            ),
        ],
        [BOOK, FILINGS],
    )

    add(
        "Defensive and enterprising approaches",
        "Defensive and enterprising investors",
        "Choose a research commitment that matches time, skill and willingness to maintain it.",
        "The defensive approach seeks a sound process with limited ongoing security-selection demands. An enterprising approach accepts substantial additional work to investigate opportunities and monitor them. The distinction concerns commitment and method; it is not a promise that taking more action or buying riskier securities earns a higher return. Research effort has an opportunity cost and still may fail to add value.\n\nInventory the time you can sustain, the statements you can interpret and the decisions you can explain. A complex portfolio that is neglected after purchase is not improved by having an elaborate starting spreadsheet. A simpler diversified policy can provide a meaningful baseline for judging active research. Historical selection criteria in the book need context; do not apply old numerical thresholds as timeless commands without examining today's business and market structure.",
        "A learner can reliably spend two hours a month maintaining an investment plan, while a proposed individual-company process needs three hours per company each quarter for twelve companies. That proposal requires 144 hours yearly before event-driven updates; the stated capacity is only 24. The mismatch is operational even before any return comparison.",
        "Create a workload budget and define what will trigger simplification. Compare a broad allocation plan with an individual-company research plan under the same goal, costs and review horizon. State what added evidence would justify the extra work.",
        r"\mathrm{annual\ research\ hours}=N_{\mathrm{companies}}\times h_{\mathrm{quarter}}\times4",
        'print("Proposed annual research hours:", 12 * 3 * 4)\nprint("Available annual hours:", 2 * 12)',
        "Build the annual workload comparison and choose a defensible process for the fictional learner. Explain why enterprising does not simply mean more speculative.",
        "The proposal needs 144 hours versus 24 available. Reduce scope or use a maintainable baseline. Enterprising work means sustained analysis and monitoring, not merely more trades or greater exposure.",
        [
            (
                "The defensive/enterprising distinction primarily concerns:",
                "The research and maintenance effort the investor undertakes",
                "A guaranteed return ranking",
                "Whether the investor can predict every market turn",
                "The distinction is about approach and commitment rather than a promise of higher risk-adjusted return.",
            ),
            (
                "Twelve companies at three hours each per quarter require annually:",
                "144 hours",
                "36 hours",
                "24 hours",
                "Twelve times three times four quarters equals 144 hours.",
            ),
            (
                "A complex process far exceeds available maintenance time. A reasonable response is:",
                "Reduce scope and define a maintainable policy",
                "Assume initial research removes all future work",
                "Increase the number of unattended holdings",
                "A strategy needs an ongoing process the learner can actually carry out.",
            ),
            (
                "Old numerical screening criteria should be treated as:",
                "Historically situated rules requiring context and analysis",
                "Universal guarantees across every industry and era",
                "A substitute for reading financial statements",
                "Business definitions and market conditions affect whether a historical threshold remains informative.",
            ),
        ],
        [BOOK, ALLOCATION],
    )

    add(
        "Market quotations, behavior and the margin for error",
        "Market fluctuations and investor behavior",
        "Use market prices as information and opportunities without letting them dictate every judgment.",
        "Graham's discussion of market fluctuations invites the investor to distinguish the quoted price from a considered estimate of value. A price is real and actionable, but it need not be an authoritative judgment of long-term worth. Repeatedly checking a quote can amplify fear, imitation and overconfidence without adding business evidence. A prewritten review policy helps distinguish a changed price from a changed thesis.\n\nIgnoring every price change is also careless: a falling price can accompany new information or make a previously tolerable position too risky for its owner. Revisit business facts, valuation assumptions and personal liquidity before deciding whether to hold, add or reduce. Never infer that a price must return to its previous high simply because that number is psychologically salient.",
        "A fictional company is quoted at 70 and later at 50 while the analyst's conservative value range remains 60–80. The fall increases the apparent discount, but an unreviewed lawsuit could invalidate that range. Against the lower estimate of 60, the discount at 50 is 16.67%; against 80 it is 37.5%. Different assumptions produce different cushions.",
        "Write a price-change response sheet: what evidence to inspect, what assumptions to update, and what actions require a cooling-off period. Record an opposing interpretation before acting on either excitement or fear.",
        r"\mathrm{discount\ to\ estimate}=1-P/V",
        'print("Discount to conservative value:", 1 - 50 / 60)\nprint("Discount to upper estimate:", 1 - 50 / 80)',
        "Calculate the two discounts and write a response to the fall from 70 to 50 that examines both behavioral pressure and potentially new business evidence.",
        "Discounts are about 16.67% and 37.5%. A lower quote changes price but does not prove the valuation assumptions survive. Review the lawsuit and liquidity needs; the previous high is not a guaranteed destination.",
        [
            (
                "A lower quoted price with no completed business review proves:",
                "Neither a bargain nor a permanent impairment by itself",
                "A guaranteed return to the former high",
                "That every valuation estimate is unchanged",
                "The price move needs interpretation alongside new evidence and the investor's constraints.",
            ),
            (
                "Price 50 against conservative value 60 gives a discount near:",
                "16.67%",
                "20%",
                "37.5%",
                "The discount uses the value denominator: 1−50/60 is approximately 0.1667.",
            ),
            (
                "Anchoring to a previous market high risks assuming:",
                "A historical quote is a promised future value",
                "Every liability has disappeared",
                "All future returns are independent",
                "An old price can become a psychological anchor without supporting business evidence.",
            ),
            (
                "A useful response to a dramatic quotation change begins with:",
                "A review of evidence, assumptions and liquidity constraints",
                "Automatically doubling the position",
                "Erasing the original decision journal",
                "A structured review separates changed facts from emotional reactions to the quote.",
            ),
        ],
        [BOOK, ALLOCATION],
    )

    add(
        "Goals, liquidity and the capacity to bear losses",
        "Defensive planning; modern course extension",
        "Separate willingness to accept risk from the financial ability to absorb it.",
        "Risk tolerance describes willingness to experience uncertainty and losses; risk capacity concerns what those losses would do to required spending and commitments. A person may feel comfortable with volatility while having a near-term obligation that cannot tolerate a large drawdown. Build the plan around dates and cash needs before choosing an attractive security.\n\nSeparate emergency liquidity, known near-term commitments and genuinely long-horizon capital. The size and instruments of those pools depend on circumstances and local protections; this fictional worksheet does not prescribe a universal reserve. Borrowing to invest adds obligations whose timing may not match the investment's recovery. The ability to wait is a balance-sheet condition as well as a personality trait.",
        "A fictional household has 120 million rupiah of available financial assets, 30 million of identified near-term spending and a chosen 24 million reserve. The residual long-horizon pool is 66 million. A 30% decline in that pool would lose 19.8 million. Whether the household can tolerate it requires a full view of income and obligations, not only confidence about stocks.",
        "Complete the goals and liquidity page using fictional numbers or broad categories; do not put account credentials or sensitive balances into a shared notebook. Stress the long-horizon pool and record which obligation would force a sale.",
        r"C_{\mathrm{long\ horizon}}=A-C_{\mathrm{near\ term}}-C_{\mathrm{reserve}}",
        'capital = 120 - 30 - 24\nprint("Long-horizon capital, million rupiah:", capital)\nprint("Illustrative 30% loss:", capital * 0.30)',
        "Calculate the fictional household's separate capital pools and stress loss. Explain the difference between emotional willingness and ability to fund required spending.",
        "Long-horizon capital is 66 million and the illustrative loss is 19.8 million. Neither the reserve amount nor a stock allocation is universal; identify obligations, income uncertainty and the consequences of a forced sale.",
        [
            (
                "Risk capacity concerns:",
                "The financial consequences of losses for obligations and goals",
                "Only enthusiasm for volatile investments",
                "The number of chart indicators used",
                "Capacity addresses whether losses impair the investor's ability to meet commitments.",
            ),
            (
                "120 minus 30 of spending and 24 of reserves leaves:",
                "66",
                "96",
                "90",
                "The residual long-horizon pool is 120−30−24=66.",
            ),
            (
                "A person likes risk but needs the money soon. The plan must consider:",
                "The near-term liability even if emotional tolerance is high",
                "Only the person's confidence",
                "Only the highest historical return",
                "Willingness to take risk does not remove a required near-term cash need.",
            ),
            (
                "The course's 24-million reserve is:",
                "A fictional assumption to analyze, not a universal prescription",
                "A required amount for every household",
                "A guarantee against every financial emergency",
                "Reserve needs depend on circumstances, commitments and available liquidity.",
            ),
        ],
        [ALLOCATION, BOOK],
    )

    add(
        "Inflation and purchasing-power risk",
        "Inflation and the investor",
        "Distinguish a nominal account gain from an increase in purchasing power.",
        "An account can grow in currency units while losing purchasing power. Compare the net nominal return with the change in the prices relevant to the goal. The exact real-return relationship compounds the two factors; simple subtraction is an approximation. A household's actual spending basket can differ from a published inflation index, and future inflation is uncertain.\n\nCash, bonds and equities each carry different risks to purchasing power and nominal capital. Equities are claims on businesses whose pricing power, costs and valuations vary; they are not an automatic inflation hedge over every horizon. A fixed nominal payment can become less useful when prices rise, while inflation-linked products have their own terms, availability and market-price risks. Study the mechanism rather than replacing uncertainty with a single protective label.",
        "Savings rise by 6% over a year while the illustrative cost of the goal rises 4%. The exact real return is 1.06/1.04 − 1, about 1.923%, rather than exactly 2%. If nominal return were 3% under the same inflation assumption, purchasing power would decline about 0.962%.",
        "Add a nominal and real column to the plan, state whether fees are already included, and compare two inflation scenarios. Keep local inflation, tax and product rules as items for current source verification before making a personal decision.",
        r"1+r_{\mathrm{real}}=\frac{1+r_{\mathrm{nominal,net}}}{1+\pi}",
        'print("Real return at 6% nominal:", 1.06 / 1.04 - 1)\nprint("Real return at 3% nominal:", 1.03 / 1.04 - 1)',
        "Calculate both real returns and describe purchasing-power risks in cash, fixed payments and business ownership without assuming a universal inflation hedge.",
        "Real returns are about 1.923% and −0.962%. The instrument's cash flows, horizon, valuation and costs determine its exposure; a broad label cannot guarantee protection in every inflation episode.",
        [
            (
                "A nominal gain necessarily increases purchasing power:",
                "No, inflation can exceed the net nominal return",
                "Yes whenever the account balance rises",
                "Only if the statement is printed",
                "Purchasing power depends on the change in relevant prices as well as nominal wealth.",
            ),
            (
                "6% net nominal return with 4% inflation gives exact real return near:",
                "1.923%",
                "2.000% exactly",
                "10%",
                "The exact compounded relationship is 1.06/1.04−1.",
            ),
            (
                "Equity ownership is an automatic inflation hedge over every horizon:",
                "No; business economics and valuation also matter",
                "Yes for every company",
                "Yes when a stock is popular",
                "Pricing power, costs and purchase valuation affect how a business responds to inflation.",
            ),
            (
                "A published inflation index and a household's goal costs can:",
                "Differ because spending baskets differ",
                "Never differ",
                "Be replaced by a stock's recent return",
                "The relevant purchasing-power comparison depends on the goods and timing of the goal.",
            ),
        ],
        [BOOK, ALLOCATION],
    )

    add(
        "Diversification and hidden concentration",
        "Portfolio policy and diversification",
        "Look through labels to identify the actual sources of portfolio risk.",
        "Diversification spreads exposure across different claims and economic drivers. Counting tickers or fund names is insufficient when their holdings overlap or they depend on the same industry, employer, country or currency. A portfolio can contain many lines while remaining one concentrated bet. Examine look-through holdings and relate them to the investor's income and obligations.\n\nDiversification can reduce company-specific risk but does not eliminate broad market losses. Correlations can change, and assets that appeared different may fall together under stress. Choose a maintainable allocation whose exposures you can explain rather than continually adding products for the appearance of sophistication. The course's weights are calculation examples, not recommended allocations for every learner.",
        "Fund A is 60% of a portfolio and holds 30% in one company; Fund B is 40% and holds 20% in the same company. Combined look-through exposure is 0.6×0.3 + 0.4×0.2 = 26%. Owning two funds has not capped that company at either fund's portfolio weight.",
        "Draw a holdings overlap table and stress a common exposure. Include employer stock alongside labor income conceptually, since both can deteriorate together. State the information needed to maintain the look-through audit over time.",
        r"w_{\mathrm{company}}=\sum_jw_{\mathrm{fund},j}w_{\mathrm{company\ within\ fund},j}",
        'print("Look-through company weight:", 0.6 * 0.3 + 0.4 * 0.2)',
        "Calculate the overlapping company exposure and describe three other ways a portfolio can remain concentrated despite holding several products.",
        "Look-through exposure is 26%. Shared sectors, currencies, country risks and employer-linked income can create concentration. Diversification reduces some risks while leaving common market risk and changing correlations.",
        [
            (
                "Two fund names necessarily mean two independent sets of holdings:",
                "No; inspect their underlying overlap",
                "Yes by definition",
                "Only when their fees differ",
                "Different wrappers may contain the same securities or share the same economic exposures.",
            ),
            (
                "60%×30% plus 40%×20% gives company exposure of:",
                "26%",
                "50%",
                "12%",
                "The weighted contributions are 18% and 8%, totaling 26%.",
            ),
            (
                "Diversification guarantees no broad market loss:",
                "No; common risks can affect many assets together",
                "Yes if there are ten tickers",
                "Yes if all products have different names",
                "Diversification does not eliminate systematic shocks or changing correlations.",
            ),
            (
                "Employer stock deserves extra concentration review because:",
                "Investment wealth and labor income may share the same business risk",
                "It is always risk-free",
                "Salary guarantees the share price",
                "A business setback can affect both employment income and the concentrated shareholding.",
            ),
        ],
        [ALLOCATION, BOOK],
    )

    add(
        "Margin of safety and permanent impairment",
        "Margin of safety",
        "Use a conservative valuation cushion while acknowledging uncertainty and business deterioration.",
        "A margin of safety is room between the price paid and a cautiously supported estimate of value. It is intended to absorb errors in assumptions and adverse developments; it is not a guarantee of principal. An apparently large discount can vanish if the valuation excludes debt, overstates sustainable earnings or assumes asset recoveries that never occur.\n\nDistinguish quotation volatility from permanent impairment of the economic claim. A temporary price decline can be uncomfortable without destroying value, while a stable quote can conceal deteriorating finances. Both matter if the investor must sell at an unfavorable time. Work with a range, inspect the lower case and identify facts that would force a revision. Diversification and position limits address the possibility that even a careful estimate is wrong.",
        "A share costs 60 with conservative, base and optimistic estimates of 70, 100 and 120. Discounts are 14.29%, 40% and 50%. Under a hypothetical rule requiring a 25% cushion against conservative value, the maximum price is 52.5. The price-60 purchase fails that particular rule even though the base-case discount looks large.",
        "Write the assumptions behind each valuation case and name one permanent-impairment mechanism. Use this conceptual exercise as preparation for the statement analysis and valuation work in Security Analysis.",
        r"\mathrm{margin}=1-P/V,\qquad P_{\max}=(1-m)V_{\mathrm{conservative}}",
        'print("Conservative margin:", 1 - 60 / 70)\nprint("Maximum price under the fictional rule:", 70 * (1 - 0.25))',
        "Calculate the three margins and the maximum price under the fictional rule. Explain how an error in value can consume the cushion and distinguish price movement from impairment.",
        "Margins are about 14.29%, 40% and 50%; the stated conservative rule permits at most 52.5. The 25% threshold is a case assumption, not a universal recommendation. Wrong earnings, senior claims or asset recoveries can erase the estimate.",
        [
            (
                "A margin of safety should be interpreted as:",
                "A cushion against errors and adverse outcomes, not a guarantee",
                "A promise that the quoted price cannot fall",
                "A replacement for examining liabilities",
                "The cushion depends on the validity of the valuation and can be consumed by error or deterioration.",
            ),
            (
                "Conservative value 70 with a required 25% cushion permits price up to:",
                "52.5",
                "87.5",
                "56",
                "The fictional maximum-price rule is 70×0.75=52.5.",
            ),
            (
                "A large base-case discount with a weak conservative case calls for:",
                "Examining downside assumptions before relying on the headline discount",
                "Ignoring the lower estimate",
                "Assuming value is known exactly",
                "The apparent cushion is sensitive to valuation uncertainty and downside evidence.",
            ),
            (
                "Permanent impairment refers most directly to:",
                "A lasting deterioration in the economic claim",
                "Every daily price decline",
                "Only a change in chart scale",
                "Business and claim deterioration differ from temporary market quotation changes.",
            ),
        ],
        [BOOK, FILINGS],
    )

    add(
        "Allocation policy before product selection",
        "General portfolio policy; modern planning extension",
        "Connect a broad allocation to a goal and stress its consequences before choosing products.",
        "Allocation policy determines the broad claims held and their intended roles. Start with the goal, horizon, liquidity needs and ability to bear loss. A policy expressed as ranges and review triggers is easier to maintain than an allocation repeatedly changed by the latest forecast. The instrument chosen must actually provide the exposure its label suggests, with understood costs and access conditions.\n\nThere is no single mix appropriate for every learner. A historical stock/bond rule is a framework to study, not a personal instruction independent of liabilities or local product terms. Evaluate adverse combinations: stocks can fall while bonds also lose market value, and cash can lose purchasing power. A scenario calculation is useful because it makes those assumptions inspectable without pretending to forecast their probability.",
        "A fictional policy holds 60% equities and 40% bonds. In a scenario with equities down 30% and bonds down 10%, the one-period portfolio return is −22% before fees and rebalancing. A 100-unit starting portfolio becomes 78. Whether that loss is acceptable depends on the goal and capacity described earlier.",
        "Give each allocation sleeve a purpose, write a permitted range and specify what would justify a policy change. Stress the same policy under several assumptions; do not choose the most reassuring scenario as the only evidence.",
        r"R_p=\sum_i w_iR_i,\qquad \sum_iw_i=1",
        'loss = 0.6 * (-0.30) + 0.4 * (-0.10)\nprint("Scenario portfolio return:", loss)\nprint("Scenario ending wealth:", 100 * (1 + loss))',
        "Calculate the 60/40 stress, identify the role of each sleeve and write an allocation range and review trigger for the fictional plan.",
        "The one-period loss is 22%, leaving 78. The example is not a universal allocation recommendation. Review goals, liquidity and capacity alongside multiple adverse scenarios before deciding whether a policy is maintainable.",
        [
            (
                "Broad allocation should begin with:",
                "Goals, horizon, liquidity and capacity",
                "Only the best recent fund return",
                "Only a product's promotional name",
                "The policy should serve the investor's requirements rather than begin with a favored product.",
            ),
            (
                "60% at −30% plus 40% at −10% produces:",
                "−22%",
                "−20%",
                "−40%",
                "The weighted contributions are −18% and −4%, totaling −22%.",
            ),
            (
                "Stocks and bonds must always move in opposite directions:",
                "No; both can decline in the same scenario",
                "Yes under every inflation outcome",
                "Only when allocation weights sum to one",
                "Diversification does not impose a fixed negative correlation across all conditions.",
            ),
            (
                "A policy change should be justified by:",
                "Documented changes in goals, constraints or supported assumptions",
                "Only a day's market excitement",
                "The desire to match every headline",
                "A recorded rationale separates deliberate policy review from reactive allocation changes.",
            ),
        ],
        [ALLOCATION, BOOK],
    )

    add(
        "Rebalancing, drift and transaction discipline",
        "Portfolio policy through market fluctuations",
        "Restore a chosen exposure deliberately while accounting for costs and changing circumstances.",
        "As assets earn different returns, portfolio weights drift even when no trade occurs. Rebalancing returns the portfolio toward its stated policy; it is not a forecast that the recent winner must immediately lose. Define a calendar rule or a deviation band, the prices used to measure weights, and how contributions can reduce the required trading.\n\nRebalancing can incur spreads, fees and taxes, and personal circumstances may justify reviewing the target itself. A policy should distinguish a scheduled rebalance from a fundamental change in goals. Avoid continuously trading tiny deviations that add cost without meaningfully changing risk. The lesson's arithmetic ignores taxes and fees to make the mechanics visible; an actual decision must account for applicable costs rather than assuming free transactions.",
        "A 100-unit 60/40 allocation experiences a 20% equity gain and flat bonds. Equity becomes 72, bonds 40, total 112 and equity weight 64.286%. Restoring 60/40 requires equity value 67.2, so 4.8 is transferred from equities to bonds before costs. Selling 12 would mistakenly reverse the entire gain rather than restore the target weight.",
        "Build a before/after holdings table, compare a calendar and band rule, and calculate how a new bond contribution could reduce selling. Record the action in the plan so a future review can distinguish policy execution from a market prediction.",
        r"w_{i,\mathrm{drift}}=V_i/\sum_jV_j,\qquad \Delta V_i=w_i^*V_{\mathrm{total}}-V_i",
        'print("Drifted equity weight:", 72 / 112)\nprint("Equity sale before costs:", 72 - 0.6 * 112)',
        "Calculate drift and the required transfer, specify a rebalance trigger and list costs or goal changes that must be reviewed before acting.",
        "Equity weight becomes about 64.286%; a 4.8 transfer restores 60/40 before costs. The trade implements a policy, not a certain prediction of reversal. Review costs and changed obligations before execution.",
        [
            (
                "72 of equities in a 112 portfolio is an equity weight near:",
                "64.286%",
                "72%",
                "60%",
                "The denominator is total current wealth, so the weight is 72/112.",
            ),
            (
                "Restoring 60% equity in that portfolio requires selling:",
                "4.8",
                "12",
                "7.2",
                "Target equity is 0.6×112=67.2; current equity 72 exceeds it by 4.8.",
            ),
            (
                "Rebalancing to a fixed policy necessarily predicts imminent price reversal:",
                "No; it restores the planned exposure",
                "Yes for every recent winner",
                "Only if the investor uses a calendar",
                "A policy trade can manage exposure without forecasting the next return.",
            ),
            (
                "Frequent tiny rebalances require scrutiny because:",
                "Costs may exceed their practical risk-management benefit",
                "Fees always become negative",
                "They guarantee a more diversified universe",
                "Small exposure adjustments can create unnecessary trading costs.",
            ),
        ],
        [ALLOCATION, FEES],
    )

    add(
        "Funds, fees and the price of convenience",
        "Investment funds; modern product comparison extension",
        "Compare a fund's actual exposure, costs and trading terms rather than its recent ranking.",
        "A pooled fund can make diversification and administration easier, but its mandate, holdings and costs still need inspection. A broad diversified fund differs from a concentrated sector fund even if both hold many securities. Compare the investment objective, benchmark, holdings overlap, expense structure, turnover and access conditions. A recent performance rank alone does not establish which exposure suits a goal.\n\nCosts can include ongoing expenses, advisory charges, trading spreads and other account or transaction fees. Distinguish the costs already reflected in reported returns from additional charges so they are not subtracted twice or omitted. Passive and active are implementation descriptions, not complete judgments about suitability. A higher-cost product needs an understood role and credible evidence rather than an assumption that price guarantees expertise.",
        "Two fictional products start at 10,000 and have a stipulated 6% annual gross return for twenty years. Under the simplified convention of subtracting annual fees from that return, a 0.2% fee yields 10,000×1.058²⁰ and a 1.5% fee yields 10,000×1.045²⁰. The difference illustrates compounding under fixed assumptions, not a forecast of either fund.",
        "Create a product-comparison sheet with objective, holdings, total stated costs, benchmark and redemption/trading terms. Show the fee convention explicitly and test lower gross returns. Use the source's general guidance without assuming U.S. account rules apply in another jurisdiction.",
        r"W_T=W_0(1+r_{\mathrm{gross}}-f)^T\quad\mathrm{(simplified\ fee\ convention)}",
        'low = 10000 * (1.06 - 0.002) ** 20\nhigh = 10000 * (1.06 - 0.015) ** 20\nprint("Lower-fee wealth:", low)\nprint("Higher-fee wealth:", high)\nprint("Illustrative fee gap:", low - high)',
        "Compare the two fee scenarios, state the simplified convention and complete a fund comparison covering holdings, cost basis and trading terms.",
        "The lower-fee scenario compounds at 5.8% and the higher-fee scenario at 4.5%; reproduce their ending values in the worksheet. Neither fixed gross return is a forecast. Verify whether reported performance is already net of each fee.",
        [
            (
                "A sector fund necessarily provides broad diversification:",
                "No; its holdings may share concentrated sector risk",
                "Yes because it is called a fund",
                "Only if it has a high expense ratio",
                "A fund wrapper does not determine how diversified its underlying exposures are.",
            ),
            (
                "Under the stated subtraction convention, 6% gross less 1.5% annual fee compounds at:",
                "4.5%",
                "7.5%",
                "5.8%",
                "The simplified net rate is 0.06−0.015=0.045.",
            ),
            (
                "A performance figure already net of an expense ratio should have that same fee:",
                "Identified without subtracting it a second time",
                "Subtracted again automatically",
                "Added back and called net",
                "Cost reconciliation requires recognizing which charges are already reflected.",
            ),
            (
                "A useful fund comparison examines:",
                "Mandate, holdings, costs, benchmark and access terms",
                "Only the latest winner ranking",
                "Only the brand's popularity",
                "The product must be evaluated in relation to the role it will serve in the plan.",
            ),
        ],
        [FEES, ALLOCATION],
    )

    add(
        "Regular contributions and the limits of averaging",
        "Disciplined purchasing; modern planning extension",
        "Understand what a regular contribution rule does and does not protect against.",
        "A regular purchase plan invests a stated amount on scheduled dates. It buys more units when the price is lower and fewer when it is higher, which can make a contribution process easier to maintain. It does not guarantee profit, remove business risk or establish that delaying an already available lump sum will outperform immediate investment. New income arriving over time is different from deliberately keeping investable cash aside.\n\nCompute average cost using total money invested divided by total units purchased, not the simple average of quoted prices when quantities differ. Include fees and distinguish contributed capital from investment return. Averaging into a deteriorating individual company can enlarge a permanent loss. The instrument still needs to meet the plan's quality, diversification and liquidity requirements.",
        "A learner invests 100 at price 10, buying ten units, then 100 at price 5, buying twenty. Total cost is 200 for thirty units, so average cost is 6.667 rather than 7.5. If the price remains 5, holdings are worth 150 and the loss is 50 despite the lower average cost.",
        "Create a dated cash-flow and units table for the two purchases. Add a declining-business case and state when the plan calls for a thesis review. Keep contribution discipline separate from automatic averaging down into any falling asset.",
        r"\mathrm{average\ cost/unit}=\frac{\sum_t C_t}{\sum_t C_t/P_t}",
        'units = 100 / 10 + 100 / 5\nprint("Total units:", units)\nprint("Average cost:", 200 / units)\nprint("Value at price 5:", units * 5)',
        "Reconcile contributions, units, average cost and ending value, and explain why regular investing neither guarantees a profit nor repairs a failing business thesis.",
        "The learner owns thirty units at average cost 6.667; value at 5 is 150 against 200 contributed. A purchasing schedule governs behavior, while instrument quality and goal suitability still require review.",
        [
            (
                "100 invested at 10 and 100 at 5 buy a total of:",
                "30 units",
                "20 units",
                "15 units",
                "The two purchases buy ten and twenty units, respectively.",
            ),
            (
                "The average cost of those purchases is closest to:",
                "6.667 per unit",
                "7.5 per unit",
                "5 per unit",
                "Average cost is total 200 divided by thirty units, not the simple average quote.",
            ),
            (
                "A lower average purchase cost guarantees a profit:",
                "No; the asset can remain below cost or deteriorate further",
                "Yes after any second purchase",
                "Only when purchases are scheduled",
                "The eventual asset value can still be below the total capital invested.",
            ),
            (
                "Scheduled purchases funded from new monthly income differ from:",
                "Deliberately delaying investment of an already available lump sum",
                "Any purchase involving shares",
                "A transaction with a recorded date",
                "Cash availability changes the decision being compared and its opportunity cost.",
            ),
        ],
        [BOOK, ALLOCATION],
    )

    add(
        "Read the business before trusting the headline number",
        "Security analysis for the lay investor",
        "Identify the accounting questions to answer before beginning detailed security analysis.",
        "An initial business review asks what the company sells, how it earns cash, how much financing it needs and which claims rank ahead of common shareholders. Compare earnings with cash generation and inspect the balance sheet rather than treating one attractive ratio as a complete analysis. A one-time gain can make reported earnings look inexpensive even while recurring operations weaken.\n\nPer-share figures require attention to dilution and share-count definitions. Debt, leases, pension or other commitments can change the residual claim, while management's adjusted measures may exclude costs that recur. Read the reconciliation and notes, record uncertainty and refuse to substitute a promotional summary for primary disclosures. This unit prepares the questions; the following Security Analysis course develops the statement and valuation work in depth.",
        "A company reports profit of 120 including a one-time asset-sale gain of 40. With twenty shares, reported EPS is 6 while the simplified recurring EPS is 4. At a share price of 60, reported P/E is 10 and recurring P/E is 15. The adjustment changes the valuation impression before any conclusion about value is warranted.",
        "Write a one-page company map and reconcile the earnings example. List the source documents and notes needed to challenge management's headline figure. Carry those unanswered questions into Security Analysis rather than forcing an estimate from missing information.",
        r"\mathrm{recurring\ EPS}=\frac{\mathrm{reported\ profit}-\mathrm{identified\ nonrecurring\ gain}}{N}",
        'eps = (120 - 40) / 20\nprint("Recurring EPS:", eps)\nprint("Recurring P/E:", 60 / eps)',
        "Reconcile reported and recurring EPS/P/E and draft five disclosure questions covering cash, liabilities, dilution, accounting adjustments and business economics.",
        "Reported EPS is 6 and recurring EPS 4; P/E changes from 10 to 15. The simplified adjustment is a starting question, not a complete valuation. Verify whether excluded costs or gains are actually nonrecurring.",
        [
            (
                "Profit 120 less a one-time gain 40 across twenty shares gives recurring EPS of:",
                "4",
                "6",
                "8",
                "Recurring profit is 80, divided by twenty shares.",
            ),
            (
                "Price 60 divided by recurring EPS 4 produces P/E of:",
                "15",
                "10",
                "20",
                "The relevant denominator in this case is recurring EPS, so 60/4=15.",
            ),
            (
                "An adjusted earnings measure from management should be:",
                "Reconciled to disclosures and examined for recurring exclusions",
                "Accepted without reading its definition",
                "Assumed to equal cash flow exactly",
                "Adjusted measures can omit economically recurring costs and require examination.",
            ),
            (
                "Before detailed valuation, a careful investor should understand:",
                "The business model, cash needs and senior claims",
                "Only the ticker's popularity",
                "Only the most recent price target",
                "Those fundamentals define the economic claim being valued.",
            ),
        ],
        [BOOK, FILINGS],
    )

    add(
        "Advisers, incentives and investment fraud",
        "Adviser judgment; modern fraud-prevention extension",
        "Check the source, incentives and verifiability of an investment claim.",
        "Advice can be helpful, but an investor still needs to understand what is being proposed and how the provider is compensated. Ask about fees, conflicts, custody, withdrawal terms and the evidence supporting a performance claim. Verify identities and relevant registrations through independent official channels for the applicable jurisdiction; a logo, testimonial or copied certificate is not that verification.\n\nPromises of high returns with little risk, pressure to act immediately, secrecy and difficulty obtaining clear documents deserve scrutiny. Refuse to treat a familiar community or influential personality as a substitute for checking the actual entity and product. A genuine investment can lose money, so the presence of risk disclosure does not validate a product either. This is a modern source-checking extension to the book's emphasis on independent judgment.",
        "A promoter promises a fixed 3% every month with no losses. If reinvested, that claim implies 1.03¹² − 1, about 42.58% a year. The arithmetic does not prove fraud by itself, but the riskless promise and pressure to transfer to a personal account demand independent verification before any commitment.",
        "Build a claim-checking sheet with provider identity, source of returns, risks, complete fee schedule and custody. Write down which statements can be verified and where. Use fictional cases for practice; do not send credentials or money to test a promoter.",
        r"r_{\mathrm{annual,claim}}=(1+r_{\mathrm{monthly,claim}})^{12}-1",
        'print("Annualized promised return:", 1.03 ** 12 - 1)',
        "Translate the monthly promise into its annual implication and write a verification checklist focused on evidence, incentives, custody and withdrawal terms.",
        "The compounded promise is about 42.58% annually. Arithmetic alone cannot establish legitimacy. Independently verify the entity, product terms and custody, and treat pressure and riskless high-return promises as reasons to stop and investigate.",
        [
            (
                "A fixed 3% monthly compounded promise implies annual return near:",
                "42.58%",
                "3%",
                "36% exactly",
                "Monthly compounding gives 1.03 to the twelfth power minus one.",
            ),
            (
                "A provider's copied registration certificate is sufficient independent verification:",
                "No; check official records through an independently obtained channel",
                "Yes if it contains a logo",
                "Yes if an influencer reposted it",
                "A copied document can be false or refer to another entity; independent identity checks matter.",
            ),
            (
                "Understanding adviser compensation helps identify:",
                "Incentives and potential conflicts in the recommendation",
                "A guarantee that the product will lose",
                "The exact future market return",
                "Compensation can influence recommendations and should be considered alongside the advice.",
            ),
            (
                "A risk disclosure alone establishes a product is legitimate:",
                "No; the entity and claims still require verification",
                "Yes in every jurisdiction",
                "Only when returns are high",
                "Including risk language does not independently validate the provider, custody or performance claim.",
            ),
        ],
        [FRAUD, FEES],
    )

    add(
        "Decision journals, disconfirmation and review rules",
        "Independent judgment and market behavior",
        "Review investments without confusing luck, hindsight and a change in the original thesis.",
        "A decision journal records the question, available evidence, assumptions, alternatives and what would change the conclusion. Include an opposing explanation and a review date. Distinguish facts from estimates and forecasts; a forecast that happens to be right does not turn its original probability into certainty. This practice limits hindsight rewriting and makes patterns of error easier to identify.\n\nReview both process and result. A missed disclosure calls for a better research step, while a well-understood adverse scenario may call for no change beyond the planned response. Selling because a thesis failed differs from selling because cash is needed or a position exceeds its policy limit. Record the actual reason instead of retrospectively choosing whichever explanation looks best. A checklist improves consistency but cannot remove uncertainty.",
        "A fictional thesis assigns 60% probability to a value of 100 and 40% to 50, giving an expected value of 80 under those assumptions. Buying at 70 does not mean the investor will receive 80 or avoid a loss; the downside outcome is still 50. If evidence shifts the probabilities to 30% and 70%, the estimate falls to 65.",
        "Write the initial journal before viewing the second scenario, then update only the assumptions changed by evidence. Explain the difference between a valuation update, an allocation rebalance and an emotional reaction to a quote.",
        r"E[V]=\sum_k p_kV_k,\qquad \sum_kp_k=1",
        'print("Initial scenario-weighted value:", 0.6 * 100 + 0.4 * 50)\nprint("Updated scenario-weighted value:", 0.3 * 100 + 0.7 * 50)',
        "Draft a dated decision journal, compute both scenario-weighted values and define an evidence-based review or exit rule that preserves the original reasoning.",
        "The estimates are 80 and 65, conditional on supplied probabilities and values. Neither is a guaranteed outcome. Document which evidence changes probabilities and separate thesis invalidation from liquidity or allocation-driven actions.",
        [
            (
                "60% probability of value 100 and 40% of 50 give expected value:",
                "80",
                "75",
                "100",
                "The scenario-weighted value is 0.6×100+0.4×50=80.",
            ),
            (
                "An expected value of 80 guarantees a realized value of 80:",
                "No; individual outcomes and assumptions remain uncertain",
                "Yes for every investor",
                "Only when price is below 80",
                "An expectation summarizes a distribution and is not a promised realized outcome.",
            ),
            (
                "A useful disconfirming observation should:",
                "Challenge a material assumption of the investment thesis",
                "Only repeat supporting publicity",
                "Depend solely on a preferred price target",
                "Disconfirmation is evidence capable of weakening the original argument.",
            ),
            (
                "Selling for a near-term cash need versus a failed business thesis should be:",
                "Recorded as distinct reasons",
                "Retrospectively described as the same prediction",
                "Hidden from the decision journal",
                "Different causes imply different lessons for the investor's process and allocation plan.",
            ),
        ],
        [BOOK, FILINGS],
    )

    add(
        "Capstone: write your careful-investor policy",
        "Synthesis and preparation for Security Analysis",
        "Assemble a maintainable plan with clear limits, evidence and a review process.",
        "The course deliverable is a written policy you can explain and maintain. Use a fictional household if you prefer to keep personal finances private. Include goals and dates, liquidity pools, risk capacity, the defensive or enterprising workload, broad allocation roles, contribution and rebalance rules, product-cost checks and limits on unsupported speculation. Record what changes would require a policy review.\n\nAdd a sample decision journal and a due-diligence checklist for one fictional company or fund. Show the calculations that support the plan, identify uncertainty and name the primary sources used. The written rubric assesses reasoning and completeness separately from the concept exam. This educational exercise cannot certify that an allocation suits a particular person or that the selected securities are safe.",
        "Use the case household's 120 million assets, 30 million near-term need and 24 million reserve to isolate 66 million of long-horizon capital. Reproduce the 52.5 maximum price under the fictional conservative-value rule. The plan rubric awards 25 points for goals/capacity, 25 for portfolio/costs, 20 for valuation/judgment, 20 for behavior/review and 10 for sources and clarity.",
        "Complete investor-plan.md, review the worked cases and self-assess the 100-point rubric. Then continue to [Security Analysis](/curriculum/security-analysis) with a list of questions about earnings quality, asset recoverability, senior claims and purchase price. The final evaluation/reporting track remains the end of the wider curriculum.",
        r"\mathrm{policy}=\mathrm{goals}+\mathrm{constraints}+\mathrm{allocation}+\mathrm{decision\ rules}+\mathrm{review}",
        'print("Long-horizon capital:", 120 - 30 - 24)\nprint("Case maximum price:", 70 * 0.75)\nprint("Investor plan rubric total:", 25 + 25 + 20 + 20 + 10)',
        "Deliver a complete careful-investor policy, workload budget, allocation stress, fee comparison, valuation range, decision journal, fraud-checking procedure, review calendar and sources. End with three questions to investigate in Security Analysis.",
        "Reproduce 66 million long-horizon capital and a 52.5 case price ceiling. Aim for 80/100 on the self-assessed plan while addressing every essential section. Keep all numerical allocations conditional on the fictional case, preserve uncertainty and prepare specific disclosure questions for the next course.",
        [
            (
                "A complete investor policy should connect:",
                "Goals, constraints, allocation, decision rules and review",
                "Only a list of recent winners",
                "Only a target return with no downside",
                "The policy must explain how actions serve goals under real constraints and uncertainty.",
            ),
            (
                "The plan rubric 25+25+20+20+10 totals:",
                "100 points",
                "90 points",
                "110 points",
                "The five categories sum to a separate 100-point written assessment.",
            ),
            (
                "Passing the concept exam establishes that a personal allocation is suitable:",
                "No; suitability depends on circumstances beyond the educational exam",
                "Yes for every learner",
                "Only if the worksheet used rupiah",
                "The exam assesses concepts rather than certifying individual financial decisions.",
            ),
            (
                "Which next course deepens the analysis of earnings, assets and senior claims?",
                "Security Analysis",
                "Only changing a chart theme",
                "A course completion screenshot",
                "Security Analysis develops the company and security assessment that this policy course prepares for.",
            ),
        ],
        [BOOK, ALLOCATION, FRAUD],
    )

    return _finish_course(modules)


def _finish_course(modules):
    parts = [
        (
            "Think like a careful investor",
            "Temperament, investment versus speculation, research commitment and market behavior.",
        ),
        (
            "Protect the plan from avoidable mistakes",
            "Liquidity, purchasing power, diversification and valuation uncertainty.",
        ),
        (
            "Build a maintainable portfolio",
            "Allocation, rebalancing, funds, fees and repeatable purchasing rules.",
        ),
        (
            "Exercise independent judgment",
            "Disclosure reading, incentives, fraud checks, decision review and a written investor plan.",
        ),
    ]
    track = finish(
        {
            "id": "intelligent-investor",
            "number": 11,
            "title": "The intelligent & careful investor",
            "description": "Investor yang hati-hati: build judgment, patience and a disciplined investment plan before analyzing individual securities. An original companion inspired by Benjamin Graham's The Intelligent Investor.",
            "source": "Benjamin Graham · The Intelligent Investor · Original Quanta companion with modern Investor.gov references",
            "level": "Foundational",
            "icon": "book",
            "studyType": "applied",
            "modules": modules,
            "prerequisites": "Complete Trading Fundamentals or understand basic shares, bonds, returns and orders. No coding experience is required; worksheets explain their inputs. Read your own legally obtained copy of the book for the original discussion.",
            "outcomes": [
                "Separate investing from speculation and evaluate the quality of a decision independently of luck.",
                "Choose a maintainable defensive or enterprising process and identify behavioral traps.",
                "Connect goals, liquidity, risk capacity, inflation and diversification to a written plan.",
                "Calculate valuation cushions, allocation drift, fee drag and purchase averages.",
                "Read disclosures, investigate incentives and recognize promises that need independent verification.",
                "Produce an investor-policy workbook and prepare for the deeper Security Analysis course.",
            ],
            "readingGuide": "16 lessons × 30 minutes = 8 hours of planned study across four units; exam time is additional. Includes 32 practice questions, four four-question checkpoints, a 16-question final and a downloadable investor-plan workbook with a self-assessed capstone. This is an original thematic companion, not the full book or a substitute for it. Edition pagination varies; use the named themes in your own copy. Modern planning, fund and fraud examples are explicitly course extensions. Case allocations and thresholds are fictional assumptions, not personalized recommendations.",
            "parts": [
                {"id": str(i), "title": t, "description": d} for i, (t, d) in enumerate(parts, 1)
            ],
            "references": [
                {"title": t, "url": u} for t, u in [BOOK, ALLOCATION, FEES, FRAUD, FILINGS]
            ],
            "resources": [
                {
                    "title": "Download the careful-investor workbook",
                    "url": "/course-assets/intelligent-investor/careful-investor-workbook.zip",
                },
                {
                    "title": "Download the investor plan and capstone rubric",
                    "url": "/course-assets/intelligent-investor/investor-plan.md",
                },
                {
                    "title": "Download the book companion reading guide",
                    "url": "/course-assets/intelligent-investor/README.md",
                },
            ],
        },
        checkpoints_for(modules, parts, 4),
    )
    track["exams"][-1]["version"] = 1
    return track
