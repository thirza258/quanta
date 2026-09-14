"""Original news-to-business analysis course. All company cases are fictional."""

from applied_courses import checkpoints_for, study
from book_courses import finish

FILINGS = (
    "U.S. SEC · Reading company annual reports",
    "https://www.investor.gov/introduction-investing/getting-started/researching-investments/how-read-10-k",
)
EVENTS = (
    "U.S. SEC · Reading current reports and material events",
    "https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/how-read-8",
)
EDGAR = (
    "U.S. SEC · Researching investments with EDGAR",
    "https://www.investor.gov/introduction-investing/getting-started/researching-investments/using-edgar-research-investments",
)
CASH = (
    "U.S. SEC · Beginners’ guide to financial statements",
    "https://www.sec.gov/about/reports-publications/beginners-guide-financial-statements",
)
FED = (
    "Federal Reserve · How monetary policy affects financial conditions",
    "https://www.federalreserve.gov/monetarypolicy/monetary-policy-what-are-its-goals-how-does-it-work.htm",
)
CPI = (
    "U.S. Bureau of Labor Statistics · Consumer Price Index questions",
    "https://www.bls.gov/cpi/questions-and-answers.htm",
)
SEASONAL = (
    "U.S. Bureau of Labor Statistics · Seasonal adjustment",
    "https://www.bls.gov/cpi/seasonal-adjustment/questions-and-answers.htm",
)
GDP = (
    "U.S. Bureau of Economic Analysis · GDP revisions",
    "https://www.bea.gov/gdp-revision-information",
)
BI = (
    "Bank Indonesia · Monetary policy framework and transmission",
    "https://www.bi.go.id/en/fungsi-utama/moneter/Default.aspx",
)
EIA = (
    "U.S. Energy Information Administration · Oil prices and outlook",
    "https://www.eia.gov/energyexplained/oil-and-petroleum-products/prices-and-outlook.php",
)
RUMORS = (
    "U.S. SEC · Social media and stock-tip scams",
    "https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/social-media-stock-scams",
)
SENTIMENT = (
    "U.S. SEC · Limits of social-sentiment investing tools",
    "https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-18",
)
VALIDATION = (
    "scikit-learn contributors · Leakage and common evaluation pitfalls",
    "https://scikit-learn.org/stable/common_pitfalls.html",
)
VALUATION = (
    "Aswath Damodaran, NYU Stern · Valuation teaching materials",
    "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/valuation/val.htm",
)


def build_news_to_markets():
    modules = []

    def add(
        title,
        objective,
        principle,
        case,
        workflow,
        formula,
        code,
        task,
        solution,
        questions,
        references,
    ):
        index = len(modules) + 1
        item = study(
            f"8.{index}",
            (index - 1) // 4 + 1,
            title,
            objective,
            principle,
            case,
            workflow,
            formula,
            code,
            task,
            solution,
            questions,
            references,
        )
        item["minutes"] = 30
        item["reading"] = (
            "30-minute session: 8 minutes reading the lesson and linked primary material, 8 minutes reproducing the worksheet, and 14 minutes writing and challenging your interpretation. Every company, release, forecast, and price in this course is a fictional teaching case."
        )
        modules.append(item)

    add(
        "From a headline to an investment question",
        "Separate a reported fact, a management claim, an inference, and a stock-price prediction.",
        "Security Analysis gives you a framework for business value. News analysis asks which assumptions need updating when new information arrives. A headline is an entry point: read the underlying announcement, identify its date and scope, and translate it into a question about revenue, costs, assets, financing, or uncertainty.\n\nKeep four columns. A fact is directly supported by a dated source; a claim is attributed to its speaker; an inference explains a mechanism under stated assumptions; a price forecast adds assumptions about expectations and valuation. Even a verified contract does not reveal its margin, collection timing, or whether investors already expected it. Your first output can be a research question rather than a trading decision.",
        "Fictional Cedar Components announces a three-year contract with a maximum value of $90 million. Its existing annual revenue is $600 million. The headline calls this a 'transformational win'. Dividing the ceiling evenly implies at most $30 million a year, or 5% of current revenue, before delivery conditions, cancellations, and displacement of other work. The filing verifies the announcement; it does not verify the word transformational or a future share-price increase.",
        "Record the original source and exact period. Ask whether $90 million is committed revenue, an optional ceiling, or backlog. Then ask about capacity, incremental costs, capital spending, customer concentration, and cash collection. Build a chain: contract terms → recognized sales → operating cash flow → value per share. Stop at each missing link and write what evidence would resolve it. Do not convert a maximum into a probability-weighted forecast without an explicit assumption.",
        r"\text{Annual exposure ceiling}=\frac{\text{Contract ceiling}/\text{Years}}{\text{Existing annual sales}}",
        'annual = 90 / 3\nprint("Annual ceiling:", annual)\nprint("Revenue exposure:", annual / 600)',
        "Write the four-column interpretation of the Cedar announcement. List three questions that could make the contract less valuable than the headline suggests.",
        "Fact: Cedar announced a conditional three-year ceiling of 90. Claim: management describes it as transformational. Inference: even annual delivery would add no more than 5% of current sales before offsets. Price prediction: unresolved without margins, expectations, and valuation. Check minimum purchase commitments, incremental capex, and payment terms.",
        [
            (
                "Cedar's maximum annual contract exposure is:",
                ["15% of sales", "5% of sales", "A guaranteed 5% profit increase"],
                1,
                "90 divided by three years and by 600 gives 5%; it is a sales ceiling.",
            ),
            (
                "Which sentence is an inference rather than a sourced fact?",
                [
                    "The announcement is dated Tuesday",
                    "Management called the contract important",
                    "The deal may improve margins if spare capacity is used",
                ],
                2,
                "Margin improvement depends on the analyst's capacity and cost assumptions.",
            ),
            (
                "A four-year contract ceiling of 80 meets annual sales of 400. Even delivery implies:",
                [
                    "5% annual sales exposure before conditions",
                    "20% guaranteed annual profit growth",
                    "A 5% share-price rise",
                ],
                0,
                "80 / 4 / 400 is 5%; valuation and realized delivery remain separate questions.",
            ),
            (
                "A confirmed order omits its margin and capital requirements. Your research memo should:",
                [
                    "Treat its full face value as equity value",
                    "State the missing inputs before estimating value",
                    "Assume the stock must rise",
                ],
                1,
                "Order value alone cannot establish incremental cash flow or value per share.",
            ),
        ],
        [FILINGS, EVENTS],
    )
    add(
        "Source quality, timestamps, and corrections",
        "Build a traceable source chain and distinguish fresh information from repeated reporting.",
        "Ten posts repeating one anonymous message provide one underlying claim, not ten independent confirmations. Follow links backward to the original disclosure, dataset, transcript, or named observer. Record publication time, event time, access time, time zone, and later corrections separately. An article updated after the close cannot be treated as fully available at the open.\n\nPrimary material is closer to the event but still requires interpretation. A company release reflects management's incentives; an auditor's report has a defined scope; a social post can impersonate an official source. Confirm the issuing entity and distinguish independent corroboration from syndication. Keep rejected evidence in the research log with its rejection reason.",
        "A rumor appears at 09:00. Four blogs repeat it at 09:15. Cedar publishes a clarification at 11:00: a proposed deal is still under negotiation. An aggregator updates the article at 12:00 without preserving its old headline. For a decision at 10:00, the clarification was unavailable. For a decision at 12:30, continuing to classify the rumor as confirmed ignores a known correction.",
        "Create a timeline with an 'available by decision time' flag. Prefer links and your own short factual notes over copying articles. Preserve permitted versions or document hashes where lawful and useful, with source-use terms. Do not invent an earlier consensus or a historical headline from today's revised page. An unresolved original source should lower confidence and can justify waiting.",
        r"\text{Eligible evidence}_i=\mathbf{1}(t_{\mathrm{available},i}\leq t_{\mathrm{decision}})",
        'times = [9.0, 9.25, 11.0, 12.0]\nprint("Available at 10:", [times[0] <= 10, times[1] <= 10, times[2] <= 10, times[3] <= 10])\nprint("Available at 12.5:", [times[0] <= 12.5, times[1] <= 12.5, times[2] <= 12.5, times[3] <= 12.5])',
        "Create two evidence logs for the rumor case, one at 10:00 and one at 12:30. Explain why a retrospective chart annotation must keep both.",
        "At 10:00 only the unconfirmed rumor and derivative reports are available. At 12:30 include the issuer's negotiation clarification and label the changed aggregator page. A later correction may improve the current decision but cannot be inserted into the earlier information set.",
        [
            (
                "Five blogs all cite the same anonymous post. Independent origins:",
                ["Five", "Six", "One"],
                2,
                "Repetition does not create independent evidence or raise the quality of the origin.",
            ),
            (
                "Which timestamp determines eligibility for a simulated decision?",
                [
                    "When the information was available to the decision maker",
                    "Only the fiscal period end",
                    "The latest access time regardless of history",
                ],
                0,
                "The information must have been available before the decision; period end is insufficient.",
            ),
            (
                "An article revised at 15:00 supports a fact absent at 10:00. A 10:30 backtest must:",
                [
                    "Use all revised text",
                    "Use the version actually available or exclude the uncertain item",
                    "Move the trade to 10:00",
                ],
                1,
                "Point-in-time evaluation needs the contemporaneous version or an explicit exclusion.",
            ),
            (
                "A widely shared screenshot has no verifiable issuer link. The strongest next step is:",
                [
                    "Count its likes",
                    "Increase conviction",
                    "Locate and verify the original disclosure",
                ],
                2,
                "Source authentication addresses the factual uncertainty; popularity does not.",
            ),
        ],
        [EDGAR, RUMORS],
    )
    add(
        "Materiality, denominators, and units",
        "Translate big-looking numbers into exposure relative to the specific company.",
        "Economic importance depends on scale, persistence, and the affected claim. A $10 million cost can be negligible to one firm and absorb a small firm's annual profit. Compare a flow with a flow for the same period; compare a debt balance with liquidity, asset value, and maturities. Use consistent currencies, units, and consolidated versus segment scope.\n\nPercent changes, percentage points, and basis points answer different questions. Moving a margin from 10% to 11% is one percentage point, 100 basis points, and a 10% relative improvement in the margin. None automatically describes the change in net profit or equity value. Qualitative events such as a lost license can also matter before a precise cost is known; a simple size screen is an analyst's triage tool, not a legal definition of materiality.",
        "Fictional Nusa Retail sells Rp2,000 billion a year with EBIT of Rp100 billion. A recurring Rp15 billion logistics cost equals 0.75% of sales but 15% of EBIT if nothing else changes. A quoted margin improvement of '50 points' is ambiguous: 50 basis points would be Rp10 billion on unchanged sales, while 50 percentage points would be Rp1,000 billion. Request the exact unit before modeling.",
        "Build a units box: currency, millions or billions, annual or quarterly, stock or flow, gross or net, total or per share. Then compute exposure against both revenue and profit. Check persistence and management responses instead of treating the static calculation as a forecast. In your memo use 'Rp15 billion annually, 15% of base EBIT before offsets' rather than simply 'small cost'.",
        r"\text{EBIT impact ratio}=\frac{\Delta\text{Recurring cost}}{\text{Base EBIT}}",
        'sales = 2000\nebit = 100\ncost = 15\nprint("Sales exposure:", cost / sales)\nprint("EBIT exposure:", cost / ebit)\nprint("50 bps on sales:", sales * 50 / 10000)',
        "Explain the logistics headline in two sentences, normalize all units, and give one reason the static EBIT impact might overstate or understate the eventual effect.",
        "The recurring cost is 0.75% of sales and 15% of EBIT before tax and offsets. Passing costs to customers could reduce the loss, while lower volumes or implementation costs could increase it. The 50-basis-point claim would imply 10 of EBIT at unchanged sales; ambiguous wording must be resolved first.",
        [
            (
                "A Rp15 billion cost compared with Rp100 billion EBIT is:",
                ["15% of base EBIT", "0.15% of EBIT", "15 percentage points of revenue margin"],
                0,
                "15 / 100 is 15%; this is an EBIT exposure ratio, not a revenue-margin change.",
            ),
            (
                "A margin increases from 8% to 9%. The increase is:",
                ["One basis point", "100 basis points", "Nine percentage points"],
                1,
                "One percentage point is 100 basis points; the relative margin increase is 12.5%.",
            ),
            (
                "Annual sales are 1,000 and EBIT is 40. A recurring annual cost of 8 equals:",
                ["8% of sales only", "2% of EBIT", "0.8% of sales and 20% of EBIT"],
                2,
                "8 / 1,000 is 0.8%; 8 / 40 is 20%, making the profit denominator consequential.",
            ),
            (
                "A news article compares quarterly costs with annual profit. First:",
                [
                    "Align periods and units",
                    "Assume the ratio is comparable",
                    "Use the share price as denominator",
                ],
                0,
                "Comparable period and unit definitions are necessary before interpreting the ratio.",
            ),
        ],
        [CASH, FILINGS],
    )
    add(
        "Expectations, surprises, and 'priced in'",
        "Explain why favorable business news can coexist with a falling stock.",
        "A change in business conditions and a surprise relative to expectations are different measurements. Markets price a distribution of future outcomes, not just last year's reported result. Compare actuals with a dated, definition-matched expectation and with what the price appears to assume. A consensus estimate is an imperfect proxy for expectations; record its provider, sample, timestamp, currency, and accounting basis.\n\nA statement that news was 'priced in' should specify what was expected before release and how that inference was obtained. A subsequent price move alone cannot prove it. Guidance, margins, risk premia, positioning, and other announcements can dominate the headline number. A miss can also be less bad than investors feared.",
        "Cedar reports EPS of $1.20 versus $1.00 a year earlier, but the dated estimate was $1.30. EPS grew 20% year over year and missed the estimate by about 7.69%. Management also reduces next-year volume guidance. The stock falls 6%. The growth headline is true; it does not establish that the release improved the outlook relative to the pre-release price.",
        "Write three separate comparisons: actual versus prior period, actual versus dated consensus, and your revised valuation versus the current price. Match GAAP or adjusted definitions and share counts. If expectations are unavailable, write 'surprise cannot be measured reliably' instead of using the prior year as a substitute. Keep price response as an observation to explain, not as evidence that every assumption in your story is correct.",
        r"\text{Surprise}=\frac{\text{Actual}-\text{Expected}}{|\text{Expected}|},\quad \text{Expected}\ne0",
        'actual = 1.20\nprint("Year-over-year growth:", actual / 1.00 - 1)\nprint("Estimate surprise:", (actual - 1.30) / 1.30)',
        "Write a short explanation of Cedar's apparently contradictory release and price response. Include an alternative explanation and the evidence needed to distinguish it.",
        "EPS grew 20% but was 7.69% below the recorded estimate, while guidance weakened. Those changes could lower value relative to expectations. A simultaneous market selloff is an alternative: compare sector and market returns and inspect release timing. Neither narrative is proven by the stock's decline alone.",
        [
            (
                "EPS of 1.20 versus 1.00 last year and 1.30 expected represents:",
                [
                    "A beat and a decline",
                    "20% growth and a roughly 7.69% miss",
                    "A guaranteed price increase",
                ],
                1,
                "Growth and surprise use different denominators and can have opposite signs.",
            ),
            (
                "If the expected figure is zero, percentage surprise should:",
                [
                    "Always be zero",
                    "Be called infinite alpha",
                    "Be replaced with a clearly defined absolute or scaled difference",
                ],
                2,
                "The ratio divides by zero; use a defensible alternative and disclose its scale.",
            ),
            (
                "Profit rises from 80 to 100 while the pre-release estimate was 110. Which is correct?",
                [
                    "25% annual growth and a 9.09% miss",
                    "A 25% consensus beat",
                    "No new information",
                ],
                0,
                "100 / 80 - 1 is 25%, while (100 - 110) / 110 is about -9.09%.",
            ),
            (
                "A claim that a policy decision was fully priced in needs:",
                [
                    "Only the after-event price chart",
                    "Evidence of prior expectations and a stated comparison",
                    "The strongest adjective in the headline",
                ],
                1,
                "A priced-in claim concerns pre-event expectations; the later chart is not enough.",
            ),
        ],
        [FILINGS, FED],
    )
    add(
        "Read an earnings release through the income statement",
        "Bridge sales growth into operating profit and identify mix, price, and volume effects.",
        "Read an earnings release in layers: headline measures, segment results, accounting statements, reconciliations, and outlook. Build a consistent bridge from revenue to gross profit to operating profit before interpreting EPS. Revenue may rise through price increases, unit sales, acquisitions, or currency translation, each with different persistence and costs.\n\nDo not compare an adjusted metric with an unadjusted expectation. Note exclusions, repeated restructuring, stock compensation, and changes in reporting definitions. Management's preferred metric can be informative when reconciled and consistently used, but it does not replace cash flow or the claims senior to shareholders. Keep recurring operating developments separate from disposal gains and financing effects.",
        "Cedar's quarterly revenue increases from 200 to 220, but gross margin falls from 40% to 35%. Gross profit falls from 80 to 77. Operating expense rises from 50 to 52, taking EBIT from 30 to 25, a 16.67% decline despite 10% sales growth. A $12 property gain could lift reported net profit without improving this operating bridge.",
        "Create old and new columns using one accounting basis and the same period. Reconcile price, volume, mix, acquisitions, and FX where the release permits it; mark unavailable components instead of forcing them to sum through invented estimates. Compare each segment with its prior trajectory. Ask whether weaker margin reflects a temporary launch, permanent competition, or a mix shift, then attach a measurable follow-up indicator.",
        r"\text{EBIT}=\text{Revenue}\times\text{Gross margin}-\text{Operating expense}",
        'old = 200 * 0.40 - 50\nnew = 220 * 0.35 - 52\nprint("Old EBIT:", old)\nprint("New EBIT:", new)\nprint("EBIT growth:", new / old - 1)',
        "Write an earnings bridge and a headline of your own that fairly describes both Cedar's revenue and operating result. Identify two missing data points.",
        "Revenue grew 10%, but gross profit fell by 3 and operating costs rose by 2, lowering EBIT from 30 to 25. A fair headline acknowledges both growth and margin pressure. Missing information includes segment mix and whether lower gross margin is recurring; the property gain should be shown separately.",
        [
            (
                "Cedar's new operating profit is:",
                ["25", "77", "220"],
                0,
                "220 times 35% is 77 gross profit; subtract operating expense of 52.",
            ),
            (
                "A property disposal gain should first be:",
                [
                    "Capitalized as permanent growth",
                    "Separated from recurring operations",
                    "Ignored in all accounting statements",
                ],
                1,
                "It belongs in reported results but needs separate treatment in recurring earning-power analysis.",
            ),
            (
                "Sales of 300 at a 30% gross margin with operating expense of 70 imply EBIT of:",
                ["90", "230", "20"],
                2,
                "Gross profit is 90; deducting operating expense of 70 leaves EBIT of 20.",
            ),
            (
                "Adjusted EPS beats while accounting EPS misses. A defensible comparison requires:",
                [
                    "The reconciliation and a definition-matched estimate",
                    "Selecting whichever number is larger",
                    "Assuming both measures are identical",
                ],
                0,
                "Different exclusions can change the result; compare consistent definitions and inspect adjustments.",
            ),
        ],
        [FILINGS, CASH],
    )
    add(
        "Cash conversion and hidden working-capital demands",
        "Link earnings headlines to receivables, inventory, cash collection, and reinvestment.",
        "Revenue recognition and cash collection can occur in different periods. Growing receivables or inventory may absorb cash even when reported profit rises. Start with earnings and reconcile noncash charges, working-capital changes, and capital spending. Specify the sign convention: an increase in operating working capital uses cash; depreciation is a noncash expense added back in a simplified reconciliation.\n\nA single weak quarter does not prove aggressive accounting. Seasonality, product launches, contract terms, or strategic inventory can explain timing. Conversely, repeated collection delays may contradict management's growth narrative. Compare the change with sales, prior seasonal patterns, receivable aging, and customer concentration. Free cash flow definitions vary; state yours explicitly.",
        "Nusa reports net income of 40 and depreciation of 10. Operating working capital rises by 25 and capex is 20. Under the simplified assumptions, operating cash flow is 25 and cash after capex is 5. Last year the comparable amount was 20. Profit alone misses the financing required to support the new inventory and receivables. These numbers omit other possible cash-flow adjustments and are not a complete statement reconstruction.",
        "Read the cash-flow statement alongside balance-sheet notes. Break working capital into receivables, inventory, and payables; distinguish cash held by the group from cash available to the parent. Ask what reverses next quarter and what is structural. Model a collection-delay sensitivity instead of automatically adding all working-capital investment back to value. Keep dividends, buybacks, and debt repayments separate from operating cash generation.",
        r"\text{Illustrative cash after capex}=NI+D\&A-\Delta NWC-\text{Capex}",
        'income = 40\ndepreciation = 10\nworking_capital = 25\ncapex = 20\nprint("Operating cash flow:", income + depreciation - working_capital)\nprint("Cash after capex:", income + depreciation - working_capital - capex)',
        "Explain how profitable growth could create a need for financing. Recalculate cash after capex if working-capital investment doubles and list the evidence needed to judge reversibility.",
        "The base case leaves 5 after capex. Working-capital investment of 50 would produce -20, potentially requiring cash reserves or external financing. Review aging, inventory turnover, supplier terms, and seasonal history before assuming the cash use will reverse.",
        [
            (
                "The simplified Nusa case leaves cash after capex of:",
                ["50", "25", "5"],
                2,
                "40 + 10 - 25 - 20 leaves 5; operating cash flow before capex is 25.",
            ),
            (
                "An increase in operating receivables, all else equal, generally:",
                ["Uses cash", "Creates a financing cash inflow", "Automatically proves fraud"],
                0,
                "Revenue not yet collected ties up cash, but its cause still needs investigation.",
            ),
            (
                "Income 30, depreciation 8, working-capital increase 18, and capex 25 produce:",
                ["45 cash after capex", "-5 cash after capex", "No cash-flow information"],
                1,
                "The simplified reconciliation is 30 + 8 - 18 - 25 = -5.",
            ),
            (
                "A seasonal inventory build weakens cash flow. The next useful comparison is:",
                [
                    "Only today's share price",
                    "A different industry's margin",
                    "Prior seasonal patterns and subsequent sell-through",
                ],
                2,
                "Comparable seasonality and inventory realization help distinguish timing from deterioration.",
            ),
        ],
        [CASH, FILINGS],
    )
    add(
        "Guidance, conference calls, and changing KPIs",
        "Read management's future claims with ranges, definitions, and observable follow-up tests.",
        "Guidance is conditional management communication, not a contractual promise. Record the metric, period, range, assumptions, and exclusions. Compare with prior guidance and dated market estimates on the same basis. A range midpoint is a convenient summary, not necessarily management's expected value or a probability distribution.\n\nConference-call answers can clarify mix, pricing, or capacity, but tone is weaker evidence than an attributable numeric commitment. Changes in KPI definitions can break comparability: active users, backlog, recurring revenue, and same-store sales depend on inclusion rules. Look for reconciliation, discontinued measures, changing cohorts, and a widening range. Treat a missing answer as unresolved rather than filling the gap with optimism.",
        "Cedar previously guided annual revenue to 900–1,000 and now guides 920–960. Both midpoints are 950 and 940 respectively, a 1.05% decline in the midpoint. The lower bound improves while the upper bound falls. Management calls this 'greater confidence', which may describe a narrower range but does not erase the lower central estimate. A new backlog definition includes cancellable orders absent from the old definition.",
        "Build a guidance-change table and write a question for each major movement. Separate changes in demand from changes in the reporting metric. Tie management's narrative to a future release: conversion of backlog to recognized sales, churn by cohort, or capacity utilization. Preserve the old definition in your history and do not splice incompatible series into one growth chart.",
        r"\text{Midpoint revision}=\frac{(L_1+U_1)/2}{(L_0+U_0)/2}-1",
        'old_mid = (900 + 1000) / 2\nnew_mid = (920 + 960) / 2\nprint("Old midpoint:", old_mid)\nprint("New midpoint:", new_mid)\nprint("Midpoint revision:", new_mid / old_mid - 1)',
        "Write three questions for management: one about demand, one about the narrower range, and one about the changed backlog definition. Specify how you will review the next quarter.",
        "Ask which demand assumptions reduced the upper bound, whether the narrower range reflects visibility or conservatism, and how backlog reconciles under the old definition. Review order conversion and cancellations next quarter. The midpoint falls from 950 to 940; the narrower range is not by itself a stronger earnings forecast.",
        [
            (
                "Cedar's revised guidance midpoint is:",
                ["940", "950", "960"],
                0,
                "The new bounds of 920 and 960 average to 940, below the prior 950 midpoint.",
            ),
            (
                "A KPI definition changes without a bridge. The historical growth series is:",
                [
                    "Automatically comparable",
                    "Subject to a comparability break",
                    "Evidence of guaranteed fraud",
                ],
                1,
                "The inclusion rules changed; request a reconciliation and avoid an unsupported continuous series.",
            ),
            (
                "Guidance changes from 100–140 to 110–120. Its midpoint:",
                ["Rises by 10", "Stays at 120", "Falls from 120 to 115"],
                2,
                "The new range is narrower and the midpoint is five lower; those are distinct observations.",
            ),
            (
                "A confident call answer contains no metric, date, or condition. Your memo should:",
                [
                    "Label it qualitative and request a testable follow-up",
                    "Convert it to a precise growth rate",
                    "Treat tone as audited evidence",
                ],
                0,
                "Qualitative communication can inform questions but does not supply missing numeric assumptions.",
            ),
        ],
        [EVENTS, FILINGS],
    )
    add(
        "Corporate actions and value per share",
        "Connect financing, buybacks, acquisitions, and dilution to the shareholder's actual claim.",
        "A financing headline changes both resources and claims on those resources. Issuing shares brings cash into the firm and expands the share count. A buyback reduces cash and shares; whether it creates value per remaining share depends on the price paid, financing, alternative uses, and future economics. EPS accretion alone is not proof of value creation.\n\nFor acquisitions, separate stand-alone value, payment, financing costs, integration spending, and uncertain synergies. For dividends and buybacks, distinguish authorization from completed cash distributions. A split changes units of ownership rather than the underlying business value. Read the actual terms before comparing per-share metrics, including convertible instruments and employee dilution.",
        "Nusa has equity value of 500 and 50 shares, or 10 per share. It raises 80 by issuing 10 shares at 8. With no fees or new project value, total equity becomes 580 across 60 shares, or about 9.67 per share. Cash increased while estimated value per old share fell. A new investment could offset that transfer only if its net value is supported, not simply because gross spending is large.",
        "Use a before-and-after table for cash, debt, equity value, and diluted shares. Model the transaction separately from operating assumptions so the same cash or synergy is not counted twice. For a rights offering, examine the rights terms and participation assumptions rather than transplanting this simple placement example. Evaluate deals under downside integration and financing cases before relying on management's headline accretion figure.",
        r"V_{\mathrm{share,new}}=\frac{V_{\mathrm{equity,old}}+\mathrm{Net\ proceeds}+\mathrm{Project\ NPV}}{\mathrm{Shares}_{old}+\mathrm{Shares}_{new}}",
        'old_value = 500\nproceeds = 10 * 8\nprint("Before value per share:", old_value / 50)\nprint("After value per share:", (old_value + proceeds) / 60)',
        "Recalculate Nusa's value per share if the new investment has NPV of 40. Explain the difference between proceeds, investment spending, and NPV.",
        "Adding project NPV of 40 gives (500 + 80 + 40) / 60 = 10.33 per share. Proceeds are financing cash; investment spending uses that cash; NPV is value above the investment's cost. Adding gross project value without deducting its required investment would double count resources.",
        [
            (
                "The placement without project NPV produces estimated value per share of:",
                ["11.60", "About 9.67", "Exactly 10.00"],
                1,
                "Equity rises to 580 but shares rise to 60, giving about 9.67 per share.",
            ),
            (
                "An announced buyback authorization is:",
                [
                    "The same as completed repurchases",
                    "A guarantee of undervaluation",
                    "Permission or intent whose execution must be checked",
                ],
                2,
                "Authorization does not establish the amount, timing, or price of completed repurchases.",
            ),
            (
                "Equity value 240 with 30 shares raises 60 by issuing 10 shares. With no other effects:",
                [
                    "New value per share is 7.50",
                    "New value per share is 10",
                    "Share count is unchanged",
                ],
                0,
                "(240 + 60) / (30 + 10) = 7.50, versus 8 before issuance.",
            ),
            (
                "An acquisition raises EPS solely through cheaper debt financing. This alone proves:",
                [
                    "Positive acquisition NPV",
                    "Neither value creation nor adequate risk compensation",
                    "That integration costs are zero",
                ],
                1,
                "EPS accretion does not price leverage risk, payment relative to value, or integration costs.",
            ),
        ],
        [EVENTS, CASH],
    )
    add(
        "Inflation releases: levels, rates, and base effects",
        "Read inflation data without confusing slower price growth with falling prices.",
        "A price index measures a level; an inflation rate measures how that level changes over a specified interval. Slower inflation can coexist with rising prices. Read the release's population, basket, period, units, adjustment method, and revision policy before interpreting the headline. Monthly seasonally adjusted changes and annual unadjusted changes should not be treated as interchangeable observations.\n\nFor companies, map the release to actual exposures. Wages, energy, rents, and selling prices affect different businesses on different schedules. A broad index does not equal a particular firm's input-cost inflation. A favorable inflation surprise can lower financing pressure while also signaling weaker demand, so the earnings and discount-rate channels may oppose each other.",
        "A fictional index rises from 120.0 last month to 120.6 today and was 115.0 a year ago. Monthly inflation is 0.5%, while the twelve-month change is about 4.87%. If last year's comparison base had been 118.0 instead, the same current index would produce only 2.20% annual inflation. Nothing about that denominator change means today's price level fell.",
        "Calculate both rates from consistent index series, label any seasonal adjustment, and compare the surprise with a dated forecast on the same basis. Then identify the company's cost basket, pricing power, and contract-reset lags. Build a two-channel note: input margin effect and demand/financing effect. Do not extrapolate a single month's change into a reliable annual forecast; annualization is a conditional arithmetic exercise.",
        r"\pi_{m}=\frac{I_t}{I_{t-1}}-1,\qquad \pi_{y}=\frac{I_t}{I_{t-12}}-1",
        'current = 120.6\nprint("Monthly inflation:", current / 120 - 1)\nprint("Annual inflation:", current / 115 - 1)\nprint("Annual rate with higher base:", current / 118 - 1)',
        "Explain the fictional inflation release to an investor studying Nusa Retail. List one favorable and one unfavorable business channel and a missing company-specific fact.",
        "Prices rose 0.5% in the month and 4.87% over twelve months. Lower input-cost pressure could support gross margin, while a demand slowdown could reduce volumes. Nusa's purchasing basket, supplier contracts, and customer price sensitivity are needed; the aggregate index does not provide them.",
        [
            (
                "Inflation slows from 6% to 3% while remaining positive. Prices are:",
                ["Necessarily falling", "Rising more slowly on the stated comparison", "Unchanged"],
                1,
                "Positive inflation means the index increased relative to the comparison period.",
            ),
            (
                "A higher year-ago index with the same current index makes annual inflation:",
                ["Lower", "Higher", "Undefined in every case"],
                0,
                "A larger positive denominator lowers the measured annual change, all else equal.",
            ),
            (
                "An index moves from 200 to 202 in a month and was 190 a year earlier. Monthly and annual changes are:",
                ["2% and 12%", "1% and 1%", "1% and about 6.32%"],
                2,
                "202 / 200 - 1 is 1%; 202 / 190 - 1 is approximately 6.32%.",
            ),
            (
                "A headline CPI decline is used as an exact forecast of a software firm's wage bill. The missing step is:",
                [
                    "Annualizing the headline without checking its basket",
                    "Mapping the index to its actual cost exposure and timing",
                    "Treating consumer prices as company input costs",
                ],
                1,
                "A broad consumer basket does not identify the company's wage contracts or labor-market exposure.",
            ),
        ],
        [CPI, SEASONAL],
    )
    add(
        "Growth, jobs, surveys, and data revisions",
        "Connect macro releases to business demand while preserving the information available at the time.",
        "Macroeconomic releases summarize an economy through measurement systems with sampling error, revisions, and different publication lags. GDP growth, payroll changes, unemployment, and business surveys are different objects. A diffusion index is not a direct revenue growth rate. A seasonally adjusted annualized quarterly growth rate is not the quarter's raw percentage change.\n\nSeparate the new observation from revisions to earlier periods. A strong headline can coexist with weaker earlier estimates. For company analysis, narrow the aggregate to relevant customers, geographies, and products; a domestic construction supplier may respond differently from a global subscription business. A causal mechanism needs an exposure link and time horizon, not just two lines on the same chart.",
        "A fictional jobs release adds 180 thousand jobs for the latest month, while the prior two months are revised down by 40 and 30 thousand. The sum of those reported changes relative to the previous vintage is 110 thousand, but that arithmetic is not itself an official measure of current monthly growth. A fictional annualized quarterly GDP growth figure of 4% corresponds to about 0.985% growth during the quarter: 1.04 to the one-quarter power minus one.",
        "Record vintage, units, revision size, and consensus timestamp. Keep first-release data for historical decisions and revised data for a clearly labeled retrospective analysis. Map demand to company orders and revenue recognition lags. Ask whether the release changes the distribution of future demand or merely confirms a trend already reflected in orders. Avoid declaring a recession or recovery from a single noisy indicator.",
        r"g_{\mathrm{quarter}}=(1+g_{\mathrm{annualized}})^{1/4}-1",
        'print("Reported vintage change (thousands):", 180 - 40 - 30)\nprint("Quarterly growth:", 1.04 ** 0.25 - 1)',
        "Create an as-published macro note and a separate revised-history note. Explain why a housing supplier and an export software company could interpret the same release differently.",
        "The as-published note retains each release and its revisions at their actual availability times. Revised history can improve measurement but cannot be inserted into old decisions. Housing orders may depend on domestic credit and construction, while export software depends on foreign demand, contract renewals, and currency exposure.",
        [
            (
                "A 4% annualized quarterly growth rate equals:",
                [
                    "4% actual growth during the quarter",
                    "About 0.985% growth during the quarter",
                    "Exactly 16% annual growth",
                ],
                1,
                "Reverse the four-quarter compounding convention: 1.04^(1/4) - 1.",
            ),
            (
                "Historical evaluation of decisions should normally use:",
                [
                    "Only the latest revised macro history",
                    "Future revisions shifted backward",
                    "The release vintage available at each decision",
                ],
                2,
                "Later revisions were unavailable and can create hindsight bias in a backtest.",
            ),
            (
                "New jobs are 150 thousand and prior months are revised by -20 and -35 thousand. Their arithmetic vintage change is:",
                ["95 thousand", "205 thousand", "150 thousand with no revisions"],
                0,
                "150 - 20 - 35 is 95; label this arithmetic rather than inventing an official growth metric.",
            ),
            (
                "A broad survey improves. Linking it to a specific stock requires:",
                [
                    "Assuming its revenue grows by the index reading",
                    "Matching customers, exposure, and recognition lags",
                    "Ignoring the survey's definition",
                ],
                1,
                "Aggregate indicators need a company-specific demand mechanism and a relevant horizon.",
            ),
        ],
        [GDP, FILINGS],
    )
    add(
        "Interest rates, bond yields, and competing stock channels",
        "Trace policy news through discount rates, refinancing, demand, and bank margins.",
        "A policy announcement can affect short rates, longer yields, credit spreads, currencies, and expected activity. Separate the decision from prior expectations and the accompanying guidance. Long-term yields need not move by the same amount as the policy rate. A firm's borrowing cost also reflects maturity, credit risk, contract terms, and whether existing debt is fixed or floating.\n\nFor equities, distinguish cash-flow news from discount-rate news. Lower rates can increase the present value of unchanged future cash flows, yet lower expected sales or a wider risk premium can offset that benefit. Banks require both asset and funding repricing analysis: lower rates may reduce borrower stress while also compressing margins. Avoid a universal 'rate cuts mean stocks rise' rule.",
        "An unchanged cash flow of 110 due in one year has value 100 at a 10% discount rate and about 101.85 at 8%. If the same news reduces the expected cash flow to 100, its value at 8% is only 92.59. For a separate company with 200 of floating-rate debt, a full-year 100-basis-point borrowing-cost increase adds 2 of interest before tax, assuming immediate repricing and unchanged principal.",
        "Build a four-column rate map: debt maturity and repricing, customer demand, discount rate, and credit conditions. For banks, add deposit pricing and credit losses. Show sensitivities rather than multiplying all debt by the policy change indiscriminately. Record whether your cash flows and rates are nominal or real and use the same currency. Verify the actual statement and rate definition before analyzing any live policy event.",
        r"PV=\frac{CF_1}{1+r},\qquad \Delta\mathrm{Interest}\approx\mathrm{Repricing\ debt}\times\Delta r",
        'print("Old present value:", 110 / 1.10)\nprint("Rate-only value:", 110 / 1.08)\nprint("Weaker-cash-flow value:", 100 / 1.08)\nprint("Extra annual interest:", 200 * 0.01)',
        "Write opposite but internally consistent stock scenarios following a rate cut. Specify which observations would distinguish a relief scenario from a demand-deterioration scenario.",
        "Relief: financing costs decline while orders and cash flows remain stable, raising estimated value. Deterioration: weaker demand lowers cash flows enough to dominate the rate benefit. Compare orders, credit spreads, refinancing terms, and company guidance. The worksheet's values are 101.85 and 92.59, not forecasts of market prices.",
        [
            (
                "Discounting unchanged 110 at 8% gives a present value of about:",
                ["101.85", "118.80", "92.59"],
                0,
                "110 / 1.08 is about 101.85; 92.59 corresponds to a reduced cash flow of 100.",
            ),
            (
                "Fixed-rate debt with no near-term refinancing necessarily reprices immediately after a policy change:",
                ["Yes", "No", "Only if the stock falls"],
                1,
                "The contractual rate may remain fixed; refinancing dates and debt terms determine exposure.",
            ),
            (
                "Floating debt of 300 reprices upward by 150 basis points for a full year. Extra pretax interest is:",
                ["45", "0.45", "4.5"],
                2,
                "300 × 0.015 = 4.5, assuming unchanged principal and immediate repricing.",
            ),
            (
                "A rate cut accompanies weaker expected demand. The valuation conclusion is:",
                [
                    "Conditional on both cash flows and discount rates",
                    "Necessarily positive",
                    "Determined only by yesterday's closing price",
                ],
                0,
                "The cash-flow and discount-rate channels can offset each other and must be modeled separately.",
            ),
        ],
        [FED, VALUATION],
    )
    add(
        "Rupiah, currency exposure, and Bank Indonesia news",
        "Connect exchange-rate headlines to importers, exporters, debt, and hedges in Indonesia.",
        "When USD/IDR rises, more rupiah are required to buy one dollar. The business effect depends on the net cash exposure, not merely the company's listing location. Identify the currencies of sales, inputs, debt service, and cash balances, then separate transaction cash flows from accounting translation. Natural offsets and financial hedges may reduce exposure, but their amounts, maturities, and costs matter.\n\nRead Bank Indonesia communication in its own policy context rather than copying a Federal Reserve narrative. Distinguish the policy announcement, rupiah movement, domestic credit conditions, and global dollar effects. An exporter can face dollar-denominated costs or weak external demand; an importer can have pricing power or hedges. 'Rupiah weakens' is not a complete company thesis.",
        "Fictional Nusa imports $10 million of goods and earns rupiah revenue. USD/IDR moves from 15,000 to 16,000. With unchanged volume, no pass-through, and no hedge, rupiah cost rises from Rp150 billion to Rp160 billion. Hedging half at 15,000 leaves a simplified blended cost of Rp155 billion, before hedge fees. A fictional exporter with $12 million receipts and $8 million dollar operating payments has a $4 million operating surplus; debt service may reduce that surplus further.",
        "Create a currency ladder by settlement month. Match hedge notional and maturity to the actual underlying cash flows, and distinguish operating flows from debt principal. Test pass-through and volume responses in rupiah. In the notebook write the connection explicitly: berita kurs → biaya atau pendapatan → arus kas → nilai perusahaan. Use the issuer's disclosures for exposure and the central bank's own release for policy facts.",
        r"\Delta\mathrm{IDR\ cost}=\mathrm{Unhedged\ USD\ payments}\times\Delta(\mathrm{USD/IDR})",
        'usd = 10_000_000\nprint("Unhedged cost increase (IDR billion):", usd * (16000 - 15000) / 1_000_000_000)\nprint("Half-hedged total cost (IDR billion):", usd * (0.5 * 15000 + 0.5 * 16000) / 1_000_000_000)\nprint("Exporter operating USD surplus (million):", 12 - 8)',
        "Build importer and exporter exposure tables. Add $3 million of exporter dollar debt service and explain why gross dollar revenue overstates its natural hedge.",
        "The unhedged importer pays 10 billion more; the simplified half hedge limits the increase to 5 billion before fees. Exporter operating surplus is 4 million dollars, falling to 1 million after the assumed debt service. Gross receipts of 12 million are not the net currency exposure, and mismatched settlement dates still matter.",
        [
            (
                "USD/IDR rises from 15,000 to 16,000. An unhedged $10 million import bill rises by:",
                ["Rp1 billion", "Rp10 billion", "Rp160 million"],
                1,
                "Ten million dollars times an extra 1,000 rupiah per dollar is Rp10 billion.",
            ),
            (
                "Which is the best starting point for currency sensitivity?",
                [
                    "The currency of its stock quotation alone",
                    "Gross export revenue alone",
                    "Currency, amount, timing, and offsets of cash exposures",
                ],
                2,
                "Net and dated exposures determine sensitivity; gross revenue omits costs, debt, and hedges.",
            ),
            (
                "A $6 million payable is half hedged; USD/IDR rises by 500. Ignoring fees, added rupiah cost is:",
                ["Rp1.5 billion", "Rp3 billion", "Rp30 billion"],
                0,
                "Only $3 million is unhedged, so 3 million × 500 = Rp1.5 billion.",
            ),
            (
                "An exporter earns dollars but owes more dollars over the same horizon. Rupiah weakness is:",
                [
                    "Guaranteed to benefit it",
                    "Potentially adverse after netting exposures",
                    "Irrelevant to its debt service",
                ],
                1,
                "A net dollar payment obligation can become more expensive in rupiah despite export receipts.",
            ),
        ],
        [BI, FILINGS],
    )
    add(
        "Commodity shocks: producers, users, and realized margins",
        "Map oil, coal, and input-price news through contracts, costs, and operating leverage.",
        "A commodity price is not a company's realized selling price or profit margin. Benchmark movements pass through contracts, product grades, transportation, taxes, hedges, and production costs. A supply disruption and a demand boom can both raise prices but have different consequences for volumes and customers. Identify which mechanism the evidence supports.\n\nCompare producers with users. A coal producer may benefit from higher realized prices while a power-intensive manufacturer faces higher costs. An airline can face fuel pressure at the same time as strong travel demand raises fares. Contract resets, inventory accounting, and hedges create lags. Keep a static sensitivity separate from a complete forecast, and distinguish a temporary shock from a durable change in earning power.",
        "A fictional commodity producer sells one million units at $80 with a variable cost of $50 and fixed cost of $20 million. EBIT is $10 million. At $90 with the same volume and costs, EBIT doubles to $20 million. If variable cost also rises to $56, EBIT is only $14 million. Separately, a manufacturer buying two million units pays $20 million more after the same $10 input increase before pass-through or hedges.",
        "Build a value-chain map from input extraction through processing, distribution, and the final buyer. For each firm, document realized-price formulas, unit costs, spare capacity, and balance-sheet resilience. Stress lower volumes as well as higher prices. Avoid applying a windfall multiple to a peak margin without testing a normalized commodity case and required reinvestment.",
        r"\mathrm{EBIT}=Q(P-C_v)-C_f",
        'quantity = 1\nprint("Base EBIT (million):", quantity * (80 - 50) - 20)\nprint("Price-only EBIT (million):", quantity * (90 - 50) - 20)\nprint("Cost-pressure EBIT (million):", quantity * (90 - 56) - 20)',
        "Write a paired producer/user analysis for a fictional coal-price increase. Show three assumptions that could reverse the apparent winner and loser labels.",
        "The producer benefits only if realized prices rise faster than costs and volumes hold up. The user can be protected by hedges, regulated or contractual pass-through, or offsetting output-price gains. Falling producer volumes, higher royalties, or expensive expansion can reduce its benefit. The static producer EBIT cases are 10, 20, and 14 million.",
        [
            (
                "The producer's EBIT at price 90 and variable cost 56 is:",
                ["14 million", "20 million", "34 million"],
                0,
                "One million units × (90 - 56) minus 20 million fixed cost gives 14 million.",
            ),
            (
                "A benchmark oil-price rise proves an airline's net profit must fall:",
                [
                    "Always",
                    "No; fares, demand, hedges, and other costs also matter",
                    "Whenever the fuel price and fare currency differ",
                ],
                1,
                "Fuel is one channel; the total profit impact depends on offsetting business exposures.",
            ),
            (
                "Two million units sell at 70 with variable cost 45 and fixed cost 30 million. EBIT is:",
                ["50 million", "25 million", "20 million"],
                2,
                "2 × (70 - 45) - 30 = 20 million using millions of units.",
            ),
            (
                "A temporary supply shock raises peak margins. A long-term valuation should:",
                [
                    "Test normalized prices and reinvestment needs",
                    "Assume peak margins last forever",
                    "Ignore production costs",
                ],
                0,
                "Temporary windfalls and durable cash-generating capacity should be modeled separately.",
            ),
        ],
        [EIA, FILINGS],
    )
    add(
        "Supply chains, tariffs, and pass-through",
        "Trace a policy or logistics shock through unit economics and customer behavior.",
        "A supply-chain shock changes more than a purchase price. Lead times, alternative suppliers, certification, inventory, working capital, and customer delivery commitments can all matter. Identify the exact product, jurisdiction, timing, and scope in the original announcement. A proposal, enacted measure, exemption, and implemented charge are distinct states; do not model them as interchangeable.\n\nPass-through is a behavioral and contractual assumption. A firm may raise prices but lose volume, absorb costs but preserve share, or redesign its supply chain at an upfront cost. A supplier's country of headquarters does not by itself determine the treatment of every shipment. For a live case, verify applicable terms through official material; the worksheet below is a fictional cost shock, not a statement of tariff law.",
        "Nusa sells 100 units at 100 each. Its per-unit imported cost is 60 and other variable cost is 20, leaving contribution of 2,000. A fictional 10% charge on the imported-cost base raises unit cost by 6. With no response, contribution falls to 1,400. Raising price by 3 while volume falls to 95 gives contribution of (103 - 66 - 20) × 95 = 1,615. Partial pass-through does not restore the original economics.",
        "Build a cost bridge with the explicitly assumed charge base. Model at least no pass-through, partial pass-through with lost volume, and a supplier-switch scenario with upfront costs. Add inventory and financing needs where lead times increase. Separate the policy's announced effective date from the date the firm's income statement first reflects it. Keep uncertain scope as an open question, not a silently chosen input.",
        r"\mathrm{Contribution}=Q\left(P-C_{\mathrm{import}}(1+\tau)-C_{\mathrm{other}}\right)",
        'print("Base contribution:", 100 * (100 - 60 - 20))\nprint("No-response contribution:", 100 * (100 - 66 - 20))\nprint("Partial-pass-through contribution:", 95 * (103 - 66 - 20))',
        "Recalculate contribution if Nusa passes through the full 6 but volume falls to 90. Explain why full price pass-through does not mean unchanged profit.",
        "At price 106 and volume 90, unit contribution returns to 20 but total contribution is 1,800, below 2,000. Volume response matters. Also examine supplier-switch costs, longer inventory cycles, and the actual policy scope before using the toy charge in a real valuation.",
        [
            (
                "Partial pass-through at price 103 and volume 95 produces contribution of:",
                ["2,000", "1,615", "1,400"],
                1,
                "The new unit contribution is 17, multiplied by 95 units.",
            ),
            (
                "A proposed policy and an implemented policy should be:",
                [
                    "Treated as identical costs today",
                    "Ignored equally",
                    "Separated by status, probability assumptions, and timing",
                ],
                2,
                "Proposal risk differs from an actual charge, and effective dates affect cash-flow timing.",
            ),
            (
                "Price 50, total variable cost 35, and volume 80 produce contribution of:",
                ["1,200", "2,800", "4,000"],
                0,
                "Contribution is (50 - 35) × 80 = 1,200, before fixed costs.",
            ),
            (
                "Full unit-cost pass-through with lower volume guarantees unchanged total profit:",
                [
                    "Yes",
                    "No; fewer units and fixed costs still matter",
                    "Yes, as long as the selling price rises",
                ],
                1,
                "Restoring margin per unit does not restore lost volume or eliminate fixed-cost pressure.",
            ),
        ],
        [EVENTS, FILINGS],
    )
    add(
        "Regulation, litigation, and event-stage uncertainty",
        "Separate allegations, proposals, decisions, appeals, and economic consequences.",
        "Read the status of an event before assigning a cash-flow impact. An allegation is not a judgment; an investigation is not a quantified liability; an announced rule may have implementation conditions. Identify the issuing authority, affected entity, procedural stage, stated effective date, and the source's actual claims. Do not turn legal vocabulary into a probability without a documented basis.\n\nThe economic impact can exceed an explicit fine through remediation, restricted operations, lost customers, or capital requirements. It can also be smaller if a remedy is limited or reversible. Keep a decision tree with mutually exclusive outcomes and show ranges when probabilities are uncertain. This is an analysis framework; live legal interpretation requires the current primary documents and appropriate expertise.",
        "A fictional licensing dispute has analyst-assigned teaching scenarios: 50% no operating restriction with cost 2, 35% remediation with cost 10, and 15% closure with cost 50, all in millions and discounted to the same date. Expected cost is 12. A separate 8 of remediation spending already included in a chosen scenario must not be deducted again. The 12 is a scenario-weighted input, not a prediction that a court will order that amount.",
        "Create a status timeline and a matrix of direct payments, operational restrictions, and timing. Label which facts are documented and which estimates belong to the analyst. Stress the probability of the adverse branch and the liquidity available to survive it. A small expected cost can hide an unacceptable tail outcome. Update the scenario tree when the event's stage changes, keeping the previous version for review.",
        r"E[C]=\sum_s p_s C_s,\qquad \sum_s p_s=1",
        'probabilities = [0.50, 0.35, 0.15]\ncosts = [2, 10, 50]\nprint("Probability total:", sum(probabilities))\nprint("Expected cost:", probabilities[0] * costs[0] + probabilities[1] * costs[1] + probabilities[2] * costs[2])',
        "Write a litigation-event note that clearly labels facts, scenario assumptions, expected cost, and the worst-case liquidity question. Do not assign guilt or certainty from an allegation.",
        "The provided probabilities are invented analysis assumptions. They sum to one and imply expected cost 12, while the adverse branch costs 50. Compare that branch with accessible liquidity and continuing cash burn. Record the actual event stage and identify the next source update needed; do not call the expected cost a legal outcome.",
        [
            (
                "The fictional probability-weighted cost is:",
                ["12", "62", "50"],
                0,
                "0.50 × 2 + 0.35 × 10 + 0.15 × 50 = 12.",
            ),
            (
                "An investigation announcement establishes:",
                [
                    "A final guilty verdict",
                    "That the announced investigation exists, subject to source verification",
                    "A precise future fine",
                ],
                1,
                "The procedural fact does not establish the final outcome or its economic amount.",
            ),
            (
                "A 70% scenario costs 5 and a 30% scenario costs 25. Expected cost is:",
                ["30", "15", "11"],
                2,
                "0.7 × 5 + 0.3 × 25 = 11, with a separate 25-cost downside branch.",
            ),
            (
                "Expected legal cost is small but the closure branch exceeds liquidity. The memo should:",
                [
                    "Show the survival constraint separately",
                    "Discard the branch",
                    "Treat expected cost as the maximum loss",
                ],
                0,
                "An average does not capture whether the firm can survive an adverse outcome.",
            ),
        ],
        [EVENTS, FILINGS],
    )
    add(
        "Build a sector and company transmission map",
        "Translate the same news into different business-model sensitivities instead of trading sector labels.",
        "Sector membership is a starting point, not an exposure measurement. Two banks can have different deposit mixes and loan repricing schedules; two retailers can sell necessities or discretionary goods; two software companies can differ in renewals, usage pricing, and customer concentration. Read segment economics and funding structure before generalizing from an industry headline.\n\nBuild a causal map with measurable links: news → relevant demand or cost driver → company KPI → revenue or margin → cash flow → valuation. Identify the time lag at every step and a counteracting channel. Correlated share-price moves can result from shared ownership or index flows even when near-term operating exposures differ. Distinguish that market linkage from a business linkage.",
        "A fictional bank has 1,000 of earning assets yielding 8% and 900 of funding costing 4%, for net interest income of 44 before credit losses and operating costs. In a rate-cut scenario, asset yield falls 100 basis points while funding cost falls only 50 basis points; income becomes 70 - 31.5 = 38.5. Lower borrower defaults could offset part of that decline. A retailer could instead benefit through consumer financing, while a software vendor may respond mainly through enterprise budgets and valuation rates.",
        "For three firms, create an exposure table with one primary metric, one lag, one offset, and one disconfirming observation. Score evidence completeness rather than inventing a universal stock signal. Separate effects on this quarter's earnings from effects on long-run competitive position. Rank research priorities by exposure and uncertainty, then open the relevant filings to refine them.",
        r"\mathrm{Net\ interest\ income}=A y_A-F c_F",
        'print("Base net interest income:", 1000 * 0.08 - 900 * 0.04)\nprint("Repriced net interest income:", 1000 * 0.07 - 900 * 0.035)\nprint("Change:", (1000 * 0.07 - 900 * 0.035) - (1000 * 0.08 - 900 * 0.04))',
        "Map a fictional rate cut to a bank, retailer, and software firm. For each, identify a business KPI and an observation that could contradict your initial interpretation.",
        "Bank: net interest income and credit losses; deposit costs falling faster than modeled would challenge the margin-pressure case. Retailer: financed purchases and comparable volumes; falling employment could overwhelm cheaper credit. Software: renewals and customer budgets; stable renewals could challenge a demand-decline assumption. The bank worksheet shows a 5.5 decline before offsets.",
        [
            (
                "The bank's repriced net interest income is:",
                ["44", "38.5", "70"],
                1,
                "Asset income is 70 and funding cost is 31.5, leaving 38.5 before other expenses.",
            ),
            (
                "The best company-specific transmission map ends with:",
                [
                    "A ticker chosen from a sector list",
                    "A guarantee of the next return",
                    "A measurable cash-flow mechanism and a test that could contradict it",
                ],
                2,
                "A useful interpretation is explicit and testable rather than an unsupported sector association.",
            ),
            (
                "Assets of 500 yield 6% and funding of 400 costs 3%. Net interest income is:",
                ["18", "30", "12"],
                0,
                "500 × 6% - 400 × 3% = 18 before credit losses and operating expenses.",
            ),
            (
                "Two firms in the same sector react differently to a cost shock. First inspect:",
                [
                    "The average past return of their sector",
                    "Input mix, contracts, pricing power, and hedges",
                    "Their current market capitalization alone",
                ],
                1,
                "Operating exposures and offsets can differ substantially within the same sector.",
            ),
        ],
        [FILINGS, FED],
    )
    add(
        "Update valuation and reverse the market's assumptions",
        "Distinguish better business prospects from an attractive price after the announcement.",
        "A sound news interpretation changes specific valuation assumptions rather than adding a vague premium for a positive story. Update cash-flow level, growth duration, reinvestment, financing claims, or the required return. Keep cash flows and discount rates matched by currency, inflation basis, and claim: equity cash flows use an equity rate, while operating cash flows require the corresponding firm-wide treatment.\n\nReverse valuation asks what the current price requires before deciding whether your new estimate differs meaningfully. A price increase can exceed the estimated business improvement; a good company development may leave less margin of safety. A simple perpetuity is useful for sensitivity training but requires stable distributable cash flows and a discount rate greater than growth. It cannot represent every growth stage or financing change.",
        "A fictional mature firm is expected to distribute next-year equity cash flow of 6 per share, growing 2% with a 10% required return. The toy value is 75. News raises the cash flow estimate to 6.3, giving 78.75 at unchanged rates. If the stock moves from 70 to 85, the new price requires cash flow of 6.8 under those same assumptions. The business estimate improved 5%, yet the market price now exceeds the analyst's updated value.",
        "Show the old model, each changed input, and the new value range. Reverse one uncertain assumption at a time rather than claiming a unique implied growth rate when several inputs can vary. Stress the required return and terminal growth together with reinvestment needs. Relate the conclusion back to Security Analysis: a narrative does not replace a conservative value range and the evidence that could invalidate it.",
        r"V=\frac{CF_1}{r-g},\qquad CF_{1,\mathrm{implied}}=P(r-g),\quad r>g",
        'print("Old value:", 6 / (0.10 - 0.02))\nprint("Updated value:", 6.3 / (0.10 - 0.02))\nprint("Cash flow implied by 85:", 85 * (0.10 - 0.02))',
        "Write a valuation update for the case and calculate the updated value at an 11% required return. State which assumption is most important to challenge before drawing a conclusion.",
        "At 10% the new estimate is 78.75; at 11% it is 70. The price of 85 requires 6.8 cash flow at the original rates, above the new 6.3 forecast. Challenge cash-flow durability, reinvestment, and the required return. The comparison supports further research or waiting under these assumptions, not a guaranteed future price decline.",
        [
            (
                "The new toy value at a 10% rate and 2% growth is:",
                ["78.75", "85", "63"],
                0,
                "6.3 / (0.10 - 0.02) = 78.75 under the stated stable-growth assumptions.",
            ),
            (
                "The stable-growth formula requires:",
                [
                    "Growth greater than the discount rate",
                    "Discount rate greater than growth",
                    "No cash-flow estimate",
                ],
                1,
                "A finite positive perpetuity value requires r > g and sustainable cash-flow assumptions.",
            ),
            (
                "Price 120, required return 9%, and growth 3% imply next-year cash flow of:",
                ["10.8", "3.6", "7.2"],
                2,
                "120 × (0.09 - 0.03) = 7.2 under the specified model.",
            ),
            (
                "A business improvement raises estimated value 5% while price rises 20%. It follows that:",
                [
                    "The valuation gap must be reassessed at the new price",
                    "The stock is automatically cheaper",
                    "The news cannot be favorable",
                ],
                0,
                "Business quality and price attractiveness are separate judgments; recompute the comparison.",
            ),
        ],
        [VALUATION, FILINGS],
    )
    add(
        "Read the price reaction with an event-study baseline",
        "Measure abnormal returns while separating description from causal attribution.",
        "An event return mixes company information with market and industry movements. Start with a defined event timestamp, a predeclared return window, consistent price adjustments, and a benchmark. A market-adjusted return subtracts the benchmark; a market-model residual subtracts a return predicted using parameters estimated before the event. Neither automatically isolates the causal effect of one headline.\n\nConfounding announcements, after-hours trading, thin liquidity, anticipatory moves, and benchmark choice complicate interpretation. Summing daily abnormal returns is a short-window CAR convention, distinct from compounding wealth. A single company's short-window residual is descriptive evidence; statistical claims need an appropriate design, uncertainty estimates, and attention to dependence across events.",
        "Across three fictional event-window days, Cedar returns 1%, -3%, and 2%, while the chosen market returns 0.5%, -1%, and 0.5%. Simple market-adjusted abnormal returns are 0.5%, -2%, and 1.5%, summing to zero. A sensational -3% middle-day headline misses both the market decline and the rebound. Zero CAR does not prove the event was irrelevant; other news or an unsuitable benchmark may mask its effect.",
        "Write the event window before inspecting the reaction and record competing announcements. Compare more than one defensible benchmark without choosing the one that supports your thesis. If fitting beta, use only pre-event observations and check stability. Report raw and abnormal returns, adjustment method, and limitations together. Do not assume the release price was an executable fill for someone who only read the news afterward.",
        r"AR_t=R_{i,t}-R_{m,t},\qquad CAR=\sum_{t\in W}AR_t",
        'stock = [0.01, -0.03, 0.02]\nmarket = [0.005, -0.01, 0.005]\nabnormal = [stock[0] - market[0], stock[1] - market[1], stock[2] - market[2]]\nprint("Abnormal returns:", abnormal)\nprint("Cumulative abnormal return:", sum(abnormal))',
        "Reconstruct the three-day case and write two competing explanations for zero CAR. Then design a pre-event beta estimate and identify which data must be excluded from its fitting window.",
        "The daily abnormal returns are 0.005, -0.02, and 0.015, totaling zero. One explanation is offsetting company news; another is market exposure that the simple benchmark does not model. Fit beta on an earlier declared window, excluding event and future data. A causal conclusion requires evidence beyond this arithmetic.",
        [
            (
                "The three-day simple CAR in the case is:",
                ["-3%", "0%", "3%"],
                1,
                "0.5% - 2% + 1.5% sums to zero across the declared window.",
            ),
            (
                "A positive abnormal return establishes that one selected headline caused it:",
                [
                    "Always",
                    "If the headline was popular",
                    "No; confounders and design still matter",
                ],
                2,
                "A benchmark adjustment is descriptive and does not eliminate all alternative explanations.",
            ),
            (
                "A stock returns -4% while its benchmark returns -1.5%. Simple abnormal return is:",
                ["-2.5%", "+2.5%", "-5.5%"],
                0,
                "Subtract the benchmark: -4% - (-1.5%) = -2.5%.",
            ),
            (
                "Estimating event-study beta using observations after the event creates:",
                [
                    "A better pre-event information set by definition",
                    "A risk of contamination and hindsight",
                    "A guarantee of causal identification",
                ],
                1,
                "Post-event data can reflect the event and were not available for a pre-event model.",
            ),
        ],
        [VALIDATION, FILINGS],
    )
    add(
        "Liquidity, positioning, and second-order effects",
        "Interpret rapid market reactions without mistaking a price mechanism for a business change.",
        "News can move prices through order flow before an analyst can update a business model. Wide spreads, limited depth, forced selling, short covering, and index-related trades can amplify a move. These are possible mechanisms to investigate, not explanations to assert from a candle alone. A one-day rally need not mean estimated intrinsic value rose by the same amount.\n\nSecond-order effects follow responses: a competitor may gain customers after a rival's disruption, but capacity limits or shared suppliers can reduce that benefit. Ask who must act, over what horizon, and with which constraints. Positioning data, where available, often has lags and incomplete coverage. Keep sourced positioning facts separate from speculation about what 'everyone' owns.",
        "A fictional stock was quoted 100.00/100.10 before news and 98.00/102.00 after it. The midpoint remains 100, while the quoted spread widens from 0.10 to 4.00. A market buy of 100 shares at the offered price would cost 200 more than the midpoint reference, assuming enough shares at that offer and excluding fees. The midpoint alone conceals a large execution cost; a limit price controls a bound but may leave the order unfilled.",
        "Record bid, ask, timestamp, market status, and available depth when studying execution. Separate a mark-to-market observation from a realizable return. In a second-order company map, identify capacity, contract, and input constraints before assigning a rival's lost sales to a beneficiary. A clear decision can be to wait for reliable prices and source confirmation while preserving the research thesis.",
        r"\mathrm{Quoted\ spread}=Ask-Bid,\qquad \mathrm{Midpoint}=\frac{Ask+Bid}{2}",
        'bid = 98\nask = 102\nmid = (bid + ask) / 2\nprint("Midpoint:", mid)\nprint("Quoted spread:", ask - bid)\nprint("Buy cost above midpoint:", 100 * (ask - mid))',
        "Explain why the unchanged midpoint does not imply unchanged trading conditions. Add a second-order beneficiary thesis and one operational constraint that could invalidate it.",
        "The midpoint is 100 but the spread widens to 4, making an offer-priced purchase 2 per share above the midpoint before fees. Actual fills also depend on depth and movement. A rival might gain orders from a disrupted supplier, but limited capacity or the same component shortage could block the gain.",
        [
            (
                "At 98/102, the quoted spread is:",
                ["4", "2", "100"],
                0,
                "Ask minus bid is 102 - 98 = 4; 100 is the midpoint.",
            ),
            (
                "A limit order guarantees:",
                [
                    "Immediate execution at the limit",
                    "A price bound if executed, with no guarantee of a fill",
                    "A profitable trade",
                ],
                1,
                "A limit constrains the execution price but may not execute when liquidity is unavailable.",
            ),
            (
                "A 49/51 quote and 200-share market buy at 51 imply cost above the midpoint of:",
                ["100", "400", "200"],
                2,
                "The midpoint is 50; one extra unit per share across 200 shares costs 200 before fees.",
            ),
            (
                "A competitor's factory closes. A rival's potential benefit depends first on:",
                [
                    "Capacity, substitutability, contracts, and shared bottlenecks",
                    "The rival automatically receiving every lost order",
                    "The stock's yesterday-only return",
                ],
                0,
                "Orders transfer only when buyers can switch and the rival can actually supply them.",
            ),
        ],
        [
            (
                "FINRA · Stock order types and execution trade-offs",
                "https://www.finra.org/investors/investing/investment-products/stocks/order-types",
            ),
            FILINGS,
        ],
    )
    add(
        "Scenarios, Bayesian updates, and correlated evidence",
        "Update conviction proportionally while avoiding false precision and duplicate evidence.",
        "A news item should update a prior assessment rather than automatically replacing it. For a binary teaching case, Bayes' rule combines a prior probability with the likelihood of seeing the evidence under each state. The likelihood ratio measures discrimination; it is not the probability that the source is correct. Real investment states and observation processes are usually more complex than this binary model.\n\nDo not multiply evidence weights as though dependent reports were independent. Several articles derived from the same company release can repeat one signal. Subjective probabilities need ranges and sensitivity checks, particularly when the evidence's reliability is uncertain. Confidence should describe what the evidence supports, while position or research decisions also consider costs, downside, liquidity, and model error.",
        "Suppose an analyst assigns a fictional 20% prior probability to a lasting margin recovery. A specific independently verified operational signal has probability 60% if recovery is real and 20% otherwise. The posterior is 0.12 / (0.12 + 0.16), or about 42.86%. The evidence raises the probability but does not establish certainty. Reprinting that same operational report in two newspapers is not a second independent signal.",
        "Write the prior, event definition, likelihood assumptions, and source independence assessment before calculating. Test weaker signal reliability and alternative base rates. Use scenario-weighted values only when outcomes and their units are compatible, and show downside separately. In a memo, state 'conviction increases under these likelihood assumptions' rather than presenting a subjective posterior as a measured natural constant.",
        r"P(H\mid E)=\frac{P(E\mid H)P(H)}{P(E\mid H)P(H)+P(E\mid\neg H)(1-P(H))}",
        'prior = 0.20\ntrue_signal = 0.60\nfalse_signal = 0.20\nposterior = prior * true_signal / (prior * true_signal + (1 - prior) * false_signal)\nprint("Posterior recovery probability:", posterior)',
        "Recalculate the posterior if the false-signal probability rises to 40%. Explain what this changes in the memo and why repeated articles should not restore the original confidence.",
        "The posterior becomes 0.12 / (0.12 + 0.32) = 27.27%. A less discriminating signal produces a smaller update. Repeated articles with a common source do not add independent likelihood information, so they cannot justify multiplying the update again.",
        [
            (
                "The original recovery posterior is approximately:",
                ["80%", "42.86%", "60%"],
                1,
                "The numerator is 0.12 and total signal probability is 0.28, giving 42.86%.",
            ),
            (
                "Two articles repeat the same disclosed observation. For evidence updating they are:",
                [
                    "Necessarily independent",
                    "Two separate confirmed recoveries",
                    "Dependent reports of one underlying signal",
                ],
                2,
                "Shared provenance means the observations should not automatically receive separate likelihood multipliers.",
            ),
            (
                "Prior 50%, signal likelihood 80% under success and 20% otherwise gives posterior:",
                ["80%", "50%", "20%"],
                0,
                "0.5 × 0.8 divided by (0.5 × 0.8 + 0.5 × 0.2) equals 80%.",
            ),
            (
                "Unknown signal reliability should be handled by:",
                [
                    "Reporting a precise probability without assumptions",
                    "Sensitivity ranges and explicit uncertainty",
                    "Counting social-media reposts as independent trials",
                ],
                1,
                "Varying the likelihood inputs exposes dependence on uncertain assumptions rather than hiding it.",
            ),
        ],
        [RUMORS, VALIDATION],
    )
    add(
        "Build an evidence-led news research memo",
        "Turn reading into a dated, reviewable company interpretation with citations and counterarguments.",
        "A useful news memo lets another person retrace the reasoning without trusting your tone. Start with the question, decision time, and source ledger. Keep the sourced facts separate from the company's interpretation and your own forecast. Connect each modeled change to a specific driver, assumption, and follow-up test. A list of links without a causal explanation is not yet analysis.\n\nUse an original short summary with publisher, title, link, date, and relevant location. Credit the source of figures and distinguish licensed data from your calculations. A reference does not itself grant permission to republish an article, chart, photograph, or dataset. The course's fictional packet is supplied for practice; for live research use material you may access and reuse appropriately, without fabricating quotations or sources.",
        "Your fictional packet contains an issuer release, an older annual report, a central-bank summary, and a derivative commentary article. Six claims appear in the draft memo, but only four have verified source locations. Evidence coverage is 4/6, or 66.67%; that is a workflow measure, not a probability that the investment thesis is right. Two unsupported claims about customer losses must be marked as hypotheses or removed.",
        "Use the downloadable memo template: question; source timeline; facts; expectation baseline; business bridge; valuation range; alternative explanations; decision; next review. Link the note to the lesson in Quanta's notebook. For every conclusion write what would change your mind. Preserve previous memo versions so you can distinguish information improvements from hindsight rewriting.",
        r"\mathrm{Evidence\ coverage}=\frac{\mathrm{Claims\ with\ verified\ support}}{\mathrm{Claims\ requiring\ support}}",
        'supported = 4\nclaims = 6\nprint("Evidence coverage:", supported / claims)\nprint("Unresolved claims:", claims - supported)',
        "Create a one-page memo from the fictional packet using the supplied template. Include at least two alternative explanations and mark every unsupported statement explicitly.",
        "A complete memo identifies source times and locations, distinguishes four supported claims from two unresolved ones, states how demand/cost/financing assumptions affect value, and sets a review trigger. Coverage of 66.67% is a documentation statistic only. A research conclusion can be 'insufficient evidence; monitor the next disclosure'.",
        [
            (
                "Four supported claims out of six yield evidence coverage of:",
                ["About 66.67%", "A 66.67% chance of a profitable trade", "Exactly 50%"],
                0,
                "4 / 6 is 66.67%; this counts documentation, not investment success probability.",
            ),
            (
                "Adding a reference automatically permits republishing a full article:",
                [
                    "Yes",
                    "No; attribution and reuse permission are different",
                    "Yes, whenever the content is available without a paywall",
                ],
                1,
                "A citation credits a source; permission or an applicable allowance governs copying its material.",
            ),
            (
                "Eight memo claims need support; five are verified. A sound memo should:",
                [
                    "Hide the other three",
                    "Treat every claim as equally established",
                    "Mark the three unresolved claims and their required evidence",
                ],
                2,
                "Traceability requires separating verified statements from assumptions and unknowns.",
            ),
            (
                "A reviewable news conclusion includes:",
                [
                    "Evidence, assumptions, counterarguments, and a revision trigger",
                    "Only a price target",
                    "Only a copied headline",
                ],
                0,
                "Another reader needs the reasoning chain and a way to test when it should change.",
            ),
        ],
        [EDGAR, FILINGS],
    )
    add(
        "Use AI and sentiment tools as supervised research aids",
        "Evaluate extraction and summaries without outsourcing source verification or investment judgment.",
        "An AI summary can omit qualifiers, confuse an issuer with a subsidiary, mix reporting periods, or invent a citation. Use a fixed extraction schema: entity, event, event time, publication time, numeric claim, unit, source location, confidence, and unresolved ambiguity. Require the tool to distinguish an unsupported field from an empty value. Verify consequential claims against the original material.\n\nSentiment labels describe language under a labeling rule, not cash flow or expected returns. Positive wording can accompany an earnings miss. Evaluate on a labeled sample with duplicates grouped and time-based separation; a random split can leak repeated press releases across training and evaluation. Document false positives, false negatives, class balance, and the human review burden. Do not paste restricted articles into a service without checking permitted use.",
        "A fictional material-event classifier flags 20 items: 12 are true material events and 8 are false alarms. It misses another 6 true events. Precision is 12/20 = 60%; recall is 12/18 = 66.67%. Those metrics assess the declared labels, not trading profitability. If repeated versions of one release appear in both evaluation and training, even those scores may be overstated.",
        "Compare tool output with a manually checked source ledger. Create a small failure log containing negation mistakes, wrong units, stale guidance, duplicate stories, and mismatched entities. Use a held-out date interval and deduplicated event groups. Set a human verification gate for source links and business-impact calculations. Connect further model work to the Machine learning for stocks course rather than treating this classifier worksheet as a complete trained model.",
        r"\mathrm{Precision}=\frac{TP}{TP+FP},\qquad\mathrm{Recall}=\frac{TP}{TP+FN}",
        'true_positive = 12\nfalse_positive = 8\nfalse_negative = 6\nprint("Precision:", true_positive / (true_positive + false_positive))\nprint("Recall:", true_positive / (true_positive + false_negative))',
        "Audit two invented AI summaries against the packet: one omits the word 'proposed'; the other treats quarterly millions as annual billions. Define a test and a review rule for each failure.",
        "The first changes event status and needs a source-span check for qualifiers. The second changes period and scale and needs schema validation plus arithmetic checks. Reject unsupported summaries before valuation use. The example classifier's 60% precision and 66.67% recall do not validate either summary or a trading strategy.",
        [
            (
                "The classifier's precision is:",
                ["66.67%", "60%", "40%"],
                1,
                "Twelve true positives divided by twenty positive flags is 60%.",
            ),
            (
                "Positive textual sentiment should be interpreted as:",
                [
                    "Guaranteed positive stock return",
                    "Proof of increased free cash flow",
                    "A language classification requiring separate business analysis",
                ],
                2,
                "A sentiment label does not establish financial impact, expectations, or market returns.",
            ),
            (
                "A system finds 18 true events, flags 6 false events, and misses 12 true events. Precision and recall are:",
                ["75% and 60%", "60% and 75%", "100% and 50%"],
                0,
                "Precision is 18/24 = 75%; recall is 18/30 = 60%.",
            ),
            (
                "Rewritten copies of one release appear in training and test sets. The main concern is:",
                [
                    "Too many different companies",
                    "Information leakage through duplicate event content",
                    "A guarantee of improved calibration",
                ],
                1,
                "Near-duplicate releases can let evaluation reflect memorization rather than unseen-event performance.",
            ),
        ],
        [SENTIMENT, VALIDATION],
    )
    add(
        "Review decisions, avoid hindsight, and know when to wait",
        "Evaluate the quality of the reasoning separately from the next price move.",
        "A good decision can lose money, and a weak process can get lucky. Preserve the prediction, probability, horizon, source set, and invalidation condition before observing the outcome. Review both the accuracy of factual extraction and the appropriateness of the business mechanism. Do not rewrite the original thesis after prices move.\n\nUse a decision log to distinguish 'evidence was wrong', 'mechanism was incomplete', 'timing differed', and 'outcome was within the stated downside distribution'. Probability scores can evaluate calibration over a suitable set of resolved events, but tiny, selected, or dependent samples do not support broad claims. A decision to wait is substantive when it specifies what information or price condition would justify reopening the case.",
        "Three fictional binary forecasts assign probabilities 0.8, 0.6, and 0.3 to precisely defined events. Outcomes are 1, 0, and 1. Their mean squared probability error is (0.04 + 0.36 + 0.49)/3 = 0.2967. A constant 0.5 forecast scores 0.25 on these same three cases, which is better for this loss on this sample. The result is not enough to conclude the analyst has no skill across all news events.",
        "Schedule a review date and outcome-resolution rule at memo creation. Record changes as new versions with new evidence. Compare with a declared baseline, keep unsuccessful and no-action cases, and avoid choosing the scoring window after the fact. Note unresolved events separately. For paper execution, include delay, spreads, fees, and the possibility of no fill; a research signal does not grant access to a past price.",
        r"\mathrm{Brier\ score}=\frac{1}{N}\sum_i(p_i-y_i)^2",
        'probabilities = [0.8, 0.6, 0.3]\noutcomes = [1, 0, 1]\nscore = ((probabilities[0] - outcomes[0]) ** 2 + (probabilities[1] - outcomes[1]) ** 2 + (probabilities[2] - outcomes[2]) ** 2) / 3\nprint("Forecast score:", score)\nprint("Constant-0.5 baseline score:", 0.25)',
        "Write a no-action decision with an evidence trigger and a price trigger. Score the fictional forecasts and explain what conclusions the three-case sample cannot support.",
        "Example: wait until the issuer reconciles cash conversion and revisit only if the price offers the required conservative margin. Record the next release date and downside indicators. The forecasts score about 0.2967 versus 0.25 for the baseline, but three selected events cannot establish stable skill, calibration, or profitable implementation.",
        [
            (
                "Lower Brier score means:",
                [
                    "Lower mean squared probability error on the evaluated sample",
                    "Guaranteed higher trading profits",
                    "A smaller worst-case portfolio loss",
                ],
                0,
                "The score measures probability error under the specified outcomes, not portfolio performance.",
            ),
            (
                "A profitable trade proves the original news interpretation was sound:",
                [
                    "Always",
                    "No; outcome luck and alternative mechanisms can intervene",
                    "Yes, if the broader market also rose",
                ],
                1,
                "Process quality and realized outcome must be reviewed separately.",
            ),
            (
                "Probabilities 0.9 and 0.4 have outcomes 1 and 0. Their Brier score is:",
                ["0.17", "0.25", "0.085"],
                2,
                "The mean of (0.9 - 1)^2 and (0.4 - 0)^2 is (0.01 + 0.16)/2 = 0.085.",
            ),
            (
                "A useful decision to wait includes:",
                [
                    "A review trigger and the evidence needed to reconsider",
                    "No documented rationale",
                    "A promise to buy after any positive headline",
                ],
                0,
                "Explicit triggers make no-action research testable and help avoid hindsight rationalization.",
            ),
        ],
        [VALIDATION, VALUATION],
    )
    add(
        "Capstone: connect the news packet to a company valuation",
        "Defend a complete evidence-to-cash-flow-to-price interpretation, including an alternative case.",
        "Combine the course into one dated investment-research memo. Your deliverable is a reasoning chain with traceable inputs, a range of outcomes, and a revision rule. Separate what changed in the business from what changed in market expectations. A final exam checks concepts; it cannot certify the quality of a written memo or turn a fictional exercise into a live recommendation.\n\nUse the supplied fictional Banyu Industrials packet and the reusable memo template. Each release has an availability time so you can reconstruct two information sets. Show revenue, costs, operating profit, cash conversion, financing claims, and diluted shares before assigning a value. The valuation cases deliberately simplify taxes and stable growth; discuss what a real multi-period model would require.",
        "Before the news, Banyu has sales of 1,000, variable cost of 600, and fixed operating cost of 200, so EBIT is 200. A confirmed input shock raises variable cost by 30, a conditional contract adds 20 of sales at 40% contribution, and efficiency saves 12. Base-case EBIT becomes 190. At 25% tax, depreciation 30, capex 40, and working-capital investment 20, illustrative next-year FCFF is 112.5. A 10% firm-wide discount rate and 2% perpetual growth imply operating value 1,406.25; subtract net debt of 300 and divide by 100 shares to get 11.0625 per share. At price 12, this base case offers no discount.",
        "Build a downside case that removes the conditional contract, uses working-capital investment of 35, and raises the discount rate to 11%. EBIT is 182, FCFF is 91.5, and value per share is about 7.1667. Apply a hypothetical 25% required margin to that downside estimate to obtain a research price threshold of 5.375. Do not call this a recommended order: the threshold is conditional on a crude fictional model. Explain debt maturity, reinvestment, growth, and event-probability omissions, then write what evidence would justify a model update.",
        r"FCFF=EBIT(1-T)+D\&A-Capex-\Delta NWC,\qquad V_{share}=\frac{FCFF_1/(WACC-g)-NetDebt}{Shares}",
        'base_ebit = 1000 - 600 - 200 - 30 + 20 * 0.40 + 12\nbase_fcff = base_ebit * 0.75 + 30 - 40 - 20\nbase_value = (base_fcff / (0.10 - 0.02) - 300) / 100\ndown_ebit = base_ebit - 20 * 0.40\ndown_fcff = down_ebit * 0.75 + 30 - 40 - 35\ndown_value = (down_fcff / (0.11 - 0.02) - 300) / 100\nprint("Base EBIT:", base_ebit)\nprint("Base FCFF:", base_fcff)\nprint("Base value per share:", base_value)\nprint("Downside EBIT:", down_ebit)\nprint("Downside FCFF:", down_fcff)\nprint("Downside value per share:", down_value)\nprint("Conditional 25% margin threshold:", down_value * 0.75)',
        "Submit a two-page notebook memo with a source timeline, expectation baseline, business bridge, base/downside valuation, competing price explanations, decision, and next-review conditions. Use the downloadable rubric for self-assessment and label every fictional input.",
        "The bridge yields base EBIT 190, FCFF 112.5, and value 11.0625; downside EBIT 182, FCFF 91.5, and value about 7.1667. A 25% downside margin gives 5.375 under the toy assumptions. At the supplied price of 12, a documented wait-and-research decision is consistent with this model. The memo must address contract probability, reinvestment needed for growth, financing risk, source timing, and alternative price explanations; automatic exam success does not grade those judgments.",
        [
            (
                "Banyu's base-case EBIT after the three modeled changes is:",
                ["200", "190", "220"],
                1,
                "200 - 30 + 20 × 40% + 12 = 190, before tax and financing.",
            ),
            (
                "Why is the contract treated differently in the downside case?",
                [
                    "All contracts are worthless",
                    "Because the stock price fell",
                    "Its conditional contribution is not assured",
                ],
                2,
                "The downside removes an uncertain 8 of EBIT rather than treating optional sales as guaranteed.",
            ),
            (
                "A new case has FCFF 80, WACC 10%, growth 2%, net debt 200, and 100 shares. Value per share is:",
                ["8", "10", "6"],
                0,
                "Operating value is 80/0.08 = 1,000; subtract 200 and divide by 100 to get 8.",
            ),
            (
                "A capstone earns full conceptual exam marks but omits sources and downside liquidity. Its research memo is:",
                [
                    "Automatically investment-ready",
                    "Incomplete and still needs separate review",
                    "Validated by the score alone",
                ],
                1,
                "The exam cannot replace source traceability, model scrutiny, and a written downside assessment.",
            ),
        ],
        [VALUATION, CASH, EVENTS, BI],
    )

    parts = [
        ("Read and verify the news", "Facts, provenance, materiality, units, and expectations."),
        (
            "Connect company news to the accounts",
            "Earnings, cash conversion, guidance, and per-share corporate actions.",
        ),
        (
            "Interpret macroeconomic releases",
            "Inflation, growth revisions, interest rates, rupiah exposure, and Bank Indonesia.",
        ),
        (
            "Map industries and second-order business effects",
            "Commodities, supply chains, event-stage uncertainty, and sector economics.",
        ),
        (
            "Link fundamentals to stock-market reactions",
            "Reverse valuation, event returns, liquidity, scenarios, and evidence updates.",
        ),
        (
            "Build and defend a repeatable research process",
            "Cited memos, supervised AI tools, decision review, and a complete capstone.",
        ),
    ]
    track = finish(
        {
            "id": "news-to-markets",
            "number": 8,
            "title": "Financial news to company & stock analysis",
            "description": "Learn to read financial news critically, understand what changed, and connect it to a company's earnings, cash flow, valuation, and stock-market reaction. Includes Indonesian macro and rupiah cases.",
            "source": "Original Quanta course · SEC, BLS, BEA, Federal Reserve, Bank Indonesia, EIA, FINRA & NYU Stern references",
            "level": "Intermediate",
            "icon": "news",
            "studyType": "applied",
            "modules": modules,
            "prerequisites": "Study Trading & market fundamentals and Security Analysis first. Basic percentages and financial-statement concepts are sufficient. Python worksheets are optional aids; every worked case can also be reproduced by hand or in a spreadsheet.",
            "outcomes": [
                "Verify sources, timestamps, units, and the difference between facts and claims.",
                "Translate earnings, guidance, financing, and operating news into cash-flow changes.",
                "Connect inflation, growth, policy rates, rupiah, and commodity shocks to specific firms.",
                "Distinguish business improvements, expectation surprises, valuation, and observed returns.",
                "Evaluate scenarios, alternative explanations, sentiment tools, and uncertainty.",
                "Produce a cited company memo with a downside case, decision, and review triggers.",
            ],
            "readingGuide": "24 lessons × 30 minutes = 12 hours of guided study across six units. Each session includes 8 minutes of lesson and primary-source reading, 8 minutes reproducing the worksheet, and 14 minutes writing and challenging your interpretation. This estimate includes assignments; exam time is additional. There are 48 practice questions, six four-question checkpoints, and a 24-question final. The capstone memo is self-assessed separately. All company names, releases, estimates, probabilities, and prices in the cases are fictional; the course contains no live news feed or stock recommendations.",
            "parts": [
                {"id": str(i), "title": title, "description": description}
                for i, (title, description) in enumerate(parts, 1)
            ],
            "references": [
                {"title": title, "url": url}
                for title, url in [FILINGS, EVENTS, CPI, GDP, FED, BI, EIA, VALUATION]
            ],
            "resources": [
                {
                    "title": "Download the news analysis study pack",
                    "url": "/course-assets/news-to-markets/news-analysis-pack.zip",
                },
                {
                    "title": "Download the research memo template and rubric",
                    "url": "/course-assets/news-to-markets/research-memo.md",
                },
                {
                    "title": "Download the fictional Banyu news packet",
                    "url": "/course-assets/news-to-markets/case-packet.md",
                },
                {
                    "title": "Download the English–Indonesian news glossary",
                    "url": "/course-assets/news-to-markets/glossary.md",
                },
            ],
        },
        checkpoints_for(modules, parts, 6),
    )
    track["exams"][-1]["version"] = 1
    return track
