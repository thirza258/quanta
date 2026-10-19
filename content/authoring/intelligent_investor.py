"""Unit 1 (11.1 - 11.4) of The Intelligent & Careful Investor course."""

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
            + "\n\n### Build your careful-investor plan\n\nWrite the calculation, decision rule and one reason the conclusion might be wrong in your notebook. Add the evidence to your My notebook page. Read the named theme in your own copy of The Intelligent Investor; these explanations and fictional cases are original Quanta material, not reproduced chapters or publisher exercises. The worksheet calculates the case and keeps the price sandbox in cash. Its chart is not an investment recommendation or a test of Graham's approach.",
            formula,
            code,
            task,
            solution,
            rows,
            refs,
        )
        item["minutes"] = 30
        item["reading"] = (
            f"Book companion theme: {theme}. 30-minute session: 10 minutes of reading, 8 minutes of calculations, and 12 minutes of notebook work. Modern product, fraud and planning examples are course extensions, not claims about Graham's historical recommendations."
        )
        modules.append(item)

    # ------------------------------------------------------------------ 11.1
    add(
        "Intelligent investing starts with temperament",
        "Investor temperament and a disciplined process",
        "Define careful investing as a repeatable decision process rather than an IQ contest.",
        "In financial markets, 'intelligence' does not mean intellectual brilliance, mathematical wizardry, or the ability to forecast tomorrow's price movements. As Benjamin Graham observed, outstanding investment results rarely require superior intellect; what they demand is emotional discipline, intellectual humility, and the temperament to prevent self-destructive instincts from sabotaging long-term plans. The Indonesian phrase investor yang hati-hati captures this philosophy: an investor who proceeds with deliberate care, thinks through downstream consequences, explicitly acknowledges uncertainty, and refuses commitments whose adverse downside they cannot financially or psychologically survive.\n\nA central cognitive trap that derails market participants is outcome bias: the psychological tendency to evaluate the quality of a past decision exclusively by its realized result rather than by the information and process available when the choice was made. In speculative environments, a careless, unhedged gamble can produce an impressive short-term gain through pure random luck, while a rigorous, well-diversified plan can experience an initial drawdown due to unpredictable macro shocks. If you praise the reckless gambler and reprimand the disciplined planner based solely on recent performance, you reinforce hazardous habits that inevitably compound into financial ruin.\n\nA sound decision process evaluates four non-negotiable dimensions at the time of commitment:\n• Available evidence: What audited filings, cash flow statements, debt covenants, and cost disclosures were verified before committing capital?\n• Evaluated alternatives: What competing opportunities or baseline risk-free cash equivalents were considered?\n• Downside survival capacity: What happens to your household or fund if the asset suffers a 30% to 50% drawdown? Will you be forced to liquidate at the market bottom?\n• Documented process: Are the specific purchase rationale, valuation cushion, and review schedule recorded in advance, before price fluctuations distort your memory?",
        "Consider two contrasting market participants navigating the same market environment:\n• Rani conducts a thorough assessment of her household financial capacity, reserves 12 months of non-negotiable living expenses in liquid deposits, and allocates 100 units of long-term surplus capital into an evidence-based, low-cost diversified portfolio aligned with a 10-year horizon. Shortly after her purchase, a severe macroeconomic downturn causes broad equity prices to decline by 15%, reducing her invested balance from 100 to 85.\n• Dito receives a promotional tip on an unvetted speculative stock in a social media chat group. Without reading financial disclosures, balance sheet liabilities, or customer concentration risks, he commits 100 units of capital. By coincidence, speculative momentum drives the stock up 20%, lifting his account to 120.\n\nEvaluating these two outcomes solely by their surface numbers (85 versus 120) produces the dangerous illusion that Dito made a superior decision. In reality, Dito took on unquantified risk of total capital loss; repeating his unexamined process over ten transactions carries a near-certain probability of eventual wipeout. Rani, by contrast, suffered an ordinary market drawdown that was anticipated in her pre-registered loss scenario; because her liquidity was safeguarded, she has no need to sell at depressed prices and her investment process remains structurally robust and repeatable.",
        "To insulate your decisions from emotional swings, establish an explicit Decision Journal and personal investment rules in your My notebook page:\n1. Separate decision quality from realized outcome: When reviewing any past investment, ask first: 'Was the thesis supported by verified evidence at the purchase date?' and only second: 'What was the realized return?'\n2. Establish cooling-off rules: Commit to a mandatory 72-hour pause before acting on unexpected windfalls (+20% or more) or sudden paper losses (-15% or more). This interrupts the panic-greed cycle.\n3. Pre-commit to review dates: Schedule quarterly or annual portfolio reviews rather than checking daily account ticks. Research shows that higher evaluation frequency amplifies myopic loss aversion and increases unnecessary trading friction.",
        r"\mathrm{decision\ review} = f(\mathrm{available\ evidence},\, \mathrm{alternatives},\, \mathrm{downside\ capacity},\, \mathrm{documented\ process})",
        'print("Wealth after a 15% fall:", 100 * (1 - 0.15))',
        "Compare Rani's and Dito's decision processes without using their outcomes as the primary evidence. Draft three observable operational habits of an investor yang hati-hati that differentiate disciplined process from outcome luck.",
        "Rani's ending portfolio of 85 reflects an ordinary cyclical drawdown that was pre-planned, stress-tested, and funded with true surplus capital. Her process is repeatable and preserves survival. Dito's 120 gain represents an unhedged speculative gamble where luck masked the total absence of due diligence; repeating his method leads to catastrophic ruin. Three observable habits of an investor yang hati-hati include: (1) documenting written purchase rationales and downside failure scenarios in a decision journal prior to order entry; (2) verifying primary financial disclosures rather than relying on promotional summaries; and (3) enforcing scheduled calendar reviews while ignoring daily market noise.",
        [
            (
                "In this course, intelligent investing primarily emphasizes:",
                "Disciplined judgment within one's limits",
                "Winning every short-term forecast",
                "The fastest reaction to every price tick",
                "Careful investing focuses on a repeatable decision process, verified evidence, risk capacity, and emotional discipline rather than forecasting luck or high-frequency reaction speed.",
            ),
            (
                "Wealth of 100 after a 15% decline becomes:",
                "85",
                "115",
                "95",
                "A 15% loss subtracts 15 units from 100, leaving exactly 100 × (1 - 0.15) = 85 units of capital.",
            ),
            (
                "A speculative purchase rises sharply. That outcome alone proves:",
                "Neither the quality nor repeatability of the original process",
                "That checking evidence was unnecessary",
                "That the next purchase must also rise",
                "Outcome bias frequently misleads investors: a favorable outcome can result from pure chance or temporary liquidity bubbles and does not validate an unexamined or reckless decision method.",
            ),
            (
                "What makes a decision journal useful?",
                "Recording reasons before outcomes can rewrite memory",
                "Adding only winning trades later",
                "Replacing all evidence with confidence scores",
                "A decision journal preserves your original facts, assumptions, and risk limits in real time, preventing hindsight bias from retrospectively altering your memory of why the trade was made.",
            ),
        ],
        [BOOK, ALLOCATION],
    )

    # ------------------------------------------------------------------ 11.2
    add(
        "Investment, speculation and a business owner's claim",
        "Investment versus speculation",
        "Distinguish analysis of a security's claim from a bet on another buyer's enthusiasm.",
        "In the opening chapter of The Intelligent Investor, Benjamin Graham drew an indelible boundary between investment and speculation: 'An investment operation is one which, upon thorough analysis, promises safety of principal and an adequate return. Operations not meeting these requirements are speculative.' Every component of this definition must be understood with rigorous precision:\n• Thorough analysis: A systematic study of financial statements, balance sheet asset quality, debt covenants, revenue durability, and operational cash flows against the price demanded by the market. Relying on chart patterns, promotional social media chatter, or market rumors does not constitute analysis.\n• Safety of principal: Protection against substantial, permanent capital loss under adverse, realistic economic conditions. It does not mean absence of paper quotation volatility, but rather assurance that the underlying economic claims remain solvent and recoverable.\n• Adequate return: A competitive yield or capital appreciation that the investor is willing to accept under realistic assumptions, without needing speculative bubbles or heroic growth forecasts.\n\nA common share is not an abstract lottery ticket or an electronic flickering icon; it is an undivided, fractional ownership interest in an operating enterprise. The quoted market price represents merely the price at which another market participant is currently willing to trade. An investment perspective evaluates the cash distributions and productive earning power of that enterprise; a speculative approach bets primarily that another buyer will arrive tomorrow willing to pay a higher price regardless of underlying business value (the 'greater fool' theory).\n\nFurthermore, never succumb to the nominal price fallacy: a share trading at $1.00 is not 'cheaper' than a share trading at $100.00. The enterprise value depends on total market capitalization (share price multiplied by total shares outstanding) and the claims of senior creditors, not the arbitrary visual size of a single unit.",
        "Examine the capital structure of Cedar Corporation:\n• Total common shares outstanding: N = 1,000 shares.\n• Quoted market price: P = $12.00 per share.\n• Equity market capitalization: P × N = $12.00 × 1,000 = $12,000.\n• Senior liabilities: Cedar carries $8,000 in senior bank debt and trade payables.\n• Enterprise earnings: Cedar generates $1,200 per year in distributable free cash flow.\n\nAn investor purchasing n = 10 shares commits $120.00. That purchase establishes an economic ownership fraction of exactly n / N = 10 / 1,000 = 1.0% of the common equity. This 1.0% is a residual claim: in liquidation or bankruptcy, senior creditors holding the $8,000 debt must be paid 100 cents on the dollar before common equity holders receive a single cent. However, while solvent, Cedar's $1,200 annual free cash flow provides an owner cash yield of $12.00 per year on the 10 shares (a 10% cash return on the $120 purchase price), with debt interest comfortably covered 3.5 times.\n\nNow contrast this with a speculative rationale: a promoter claims Cedar is 'cheap at $12' and will 'double to $24 next month' because of rumored acquisition interest. This speculative claim completely ignores the $8,000 senior debt, makes no reference to Cedar's audited cash generation, and depends entirely on finding an eager buyer at an inflated price.",
        "In your My notebook page, implement an explicit diagnostic test before every security commitment:\n1. The Five-Year Market Closure Test: Ask yourself: 'If the stock exchange were to close tomorrow for five consecutive years, would I remain satisfied owning this business solely based on its operating cash flows and balance sheet strength?' If the answer is no, your rationale is speculative.\n2. Senior Claim Audit: Calculate total market capitalization and inspect all senior liabilities (bank loans, bonds, lease commitments, pension deficits) ranking ahead of your equity.\n3. Segregate Speculation: If you choose to engage in speculative trading, isolate it into a strictly capped, non-essential account (e.g. under 5% of risk capital) and never allow speculative losses to contaminate your primary core investment portfolio.",
        r"\mathrm{ownership\ fraction} = \frac{n}{N},\qquad \mathrm{equity\ market\ value} = P \times N",
        'print("Ownership fraction:", 10 / 1000)\nprint("Equity market value:", 12 * 1000)',
        "Calculate the ownership fraction and equity market capitalization for Cedar Corporation. Contrast the business-owner investment thesis with the speculative trading thesis, explaining why a long holding period alone cannot transform an unexamined gamble into an investment.",
        "Ten of 1,000 shares represent exactly 1.0% of the common equity residual claim; total equity market capitalization is $12.00 × 1,000 = $12,000. An investment thesis values Cedar's $1,200 sustainable cash flow and verifies that operating earnings cover senior debt obligations. A speculative thesis bets blindly on finding another buyer at $24 based on rumors. Merely holding a speculative asset for many years does not convert it into an investment; elapsed time cannot supply the rigorous analysis, principal protection, and cash-flow justification that were missing at the initial purchase.",
        [
            (
                "Ten shares out of 1000 outstanding represent ownership of:",
                "1%",
                "10%",
                "0.1%",
                "The fractional equity ownership is calculated as shares held divided by total shares outstanding: 10 / 1000 = 0.01, which represents exactly 1.0%.",
            ),
            (
                "A low nominal share price by itself establishes:",
                "Neither cheap valuation nor suitable risk",
                "A bargain independent of shares outstanding",
                "Guaranteed principal protection",
                "A share price of $1.00 can represent an egregiously overvalued company if share count is massive or liabilities exceed assets; valuation requires comparing total market capitalization to fundamental enterprise claims.",
            ),
            (
                "Holding an unexamined promotion for several years automatically changes it into:",
                "Neither a sound analysis nor a justified investment",
                "A fully analyzed investment",
                "A senior creditor claim",
                "Passive passage of time cannot retroactively supply the thorough financial analysis, safety of principal, and adequate return required to classify an operation as an investment.",
            ),
            (
                "Equity ownership gives a claim on:",
                "Residual business value after senior claims",
                "Gross assets without any liabilities",
                "A guaranteed daily price increase",
                "Common equity represents a strictly residual ownership interest in the business's assets and earnings after all operating expenses, taxes, and senior debt obligations are fully satisfied.",
            ),
        ],
        [BOOK, FILINGS],
    )

    # ------------------------------------------------------------------ 11.3
    add(
        "Defensive and enterprising approaches",
        "Defensive and enterprising investors",
        "Choose a research commitment that matches time, skill and willingness to maintain it.",
        "Graham categorized investors into two distinct operational profiles: the Defensive (or Passive) Investor and the Enterprising (or Active/Aggressive) Investor. It is crucial to understand what this distinction means and, more importantly, what it does NOT mean:\n• Enterprising does NOT mean taking wilder financial risks, buying speculative penny stocks, trading on margin, or gambling with options. An enterprising investor takes calculated, intelligent actions backed by deep intellectual labor.\n• The defining distinction is the commitment of time, specialized analytical training, and emotional stamina that the investor is willing and able to devote to managing their portfolio.\n\nA defensive investor prioritizes simplicity, freedom from anxiety, and broad diversification. Their objective is to achieve satisfactory long-term results with minimal ongoing research demands, typically through low-cost broad index funds, balanced asset allocation, and automated regular rebalancing. By contrast, an enterprising investor treats investment research as a demanding second career or serious business endeavor, dedicating hundreds of hours annually to dissecting corporate balance sheets, evaluating management incentives, and identifying mispriced securities.\n\nNobel laureate William Sharpe's 'Arithmetic of Active Management' proves mathematically that before fees, the average actively managed dollar earns the exact return of the average passively managed dollar; after deducting research costs, trading commissions, and management fees, the average active dollar must underperform. Therefore, an enterprising strategy should only be undertaken if the investor has both the operational time budget and a demonstrated analytical edge to justify the substantial additional effort.",
        "Consider a working professional auditing their investment time budget:\n• Available capacity: The investor can realistically and reliably commit 2 hours per month of focused weekend study to portfolio management, providing an annual time budget of 2 × 12 = 24 hours.\n• Proposed enterprising strategy: An acquaintance recommends building an active stock-picking portfolio of 12 individual companies, estimating that conducting proper due diligence (reading 10-K annual reports, four 10-Q quarterly reports, earnings call transcripts, and updating valuation models) requires 3 hours per company each quarter.\n\nLet us compute the total annual workload demanded by this enterprising proposal:\n$$\\mathrm{Annual\\ Hours} = 12\\text{ companies} \\times 3\\text{ hours/quarter} \\times 4\\text{ quarters} = 144\\text{ hours per year}$$\n\nComparing 144 required hours against 24 available hours reveals a staggering 120-hour operational deficit! If the investor attempts this enterprising strategy without the necessary hours, they will inevitably cut corners: skimming filings, ignoring covenant modifications, and failing to monitor corporate developments. An unmonitored active portfolio is not sophisticated; it is reckless negligence.",
        "Establish an honest Workload Budget in your My notebook page:\n1. Audit your weekly hours: Quantify the sustainable hours you can commit without neglecting your primary career, family, and rest. If you have under 5 hours per week, adopt a defensive indexation framework.\n2. Adopt the Defensive Baseline Benchmark: Treat a broad, low-cost index fund allocation as your hurdle benchmark. Any enterprising strategy must justify not only its financial costs but the opportunity cost of your personal time.\n3. The Simplification Trigger: Formulate a binding policy rule: 'If I fall behind on reading quarterly filings for two consecutive quarters, I will automatically liquidate individual stock positions and transfer the capital into my defensive baseline fund.'",
        r"\mathrm{annual\ research\ hours} = N_{\mathrm{companies}} \times h_{\mathrm{quarter}} \times 4",
        'print("Proposed annual research hours:", 12 * 3 * 4)\nprint("Available annual hours:", 2 * 12)',
        "Calculate the annual research workload for 12 companies requiring 3 hours per quarter each, compare it to a 24-hour annual budget, and justify why choosing a defensive approach is a mark of intelligent self-awareness rather than inferiority.",
        "Twelve companies at 3 hours per quarter across 4 quarters require 12 × 3 × 4 = 144 annual research hours, creating a 120-hour deficit against the 24 hours available. Selecting a defensive index approach acknowledges this reality, preventing unmonitored active holdings. In investing, adopting a defensive approach is an intelligent, rational alignment of portfolio architecture with operational capacity, ensuring that scarce personal time is spent effectively while capturing broad economic growth.",
        [
            (
                "The defensive/enterprising distinction primarily concerns:",
                "The research and maintenance effort the investor undertakes",
                "A guaranteed return ranking",
                "Whether the investor can predict every market turn",
                "Graham's classification distinguishes investors by the commitment of time, analysis, and ongoing effort they are able and willing to dedicate, not by a promise of superior return or speculative risk-taking.",
            ),
            (
                "Twelve companies at three hours each per quarter require annually:",
                "144 hours",
                "36 hours",
                "24 hours",
                "The total annual requirement is calculated as 12 companies × 3 hours per quarter × 4 quarters = 144 hours.",
            ),
            (
                "A complex process far exceeds available maintenance time. A reasonable response is:",
                "Reduce scope and define a maintainable policy",
                "Assume initial research removes all future work",
                "Increase the number of unattended holdings",
                "When research demands exceed available hours, an investor must simplify their strategy to a maintainable baseline to prevent catastrophic neglect and unmonitored risk.",
            ),
            (
                "Old numerical screening criteria should be treated as:",
                "Historically situated rules requiring context and analysis",
                "Universal guarantees across every industry and era",
                "A substitute for reading financial statements",
                "Historical screening benchmarks (such as P/E or current ratio thresholds) reflect the specific corporate accounting and market structures of their era and must be adapted thoughtfully to modern realities.",
            ),
        ],
        [BOOK, ALLOCATION],
    )

    # ------------------------------------------------------------------ 11.4
    add(
        "Market quotations, behavior and the margin for error",
        "Market fluctuations and investor behavior",
        "Use market prices as information and opportunities without letting them dictate every judgment.",
        "In Chapter 8 of The Intelligent Investor, Graham introduced his most enduring pedagogical allegory: the parable of **Mr. Market**. Imagine you own an equal share in a private business alongside a partner named Mr. Market. Every single day, without fail, Mr. Market knocks on your door and quotes a price at which he is willing to either buy your share or sell you additional shares. Mr. Market is emotionally volatile: on days when optimism overwhelms him, he quotes an exorbitant price; on days when gloom and pessimism take over, he quotes a depressed, fire-sale price.\n\nThe profound lesson of Mr. Market is this: **Mr. Market is your servant, not your master or teacher.** His daily quotation is an option, an opportunity to transact if the price is extraordinarily favorable to you, but it carries zero authority regarding the true economic value of your business. If his quoted price does not suit you, you can simply ignore him; he will return tomorrow with a new offer.\n\nUnfortunately, many market participants allow Mr. Market to become their master. When prices plummet, they assume Mr. Market knows something they do not, succumbing to panic and selling at the bottom. When prices soar, they succumb to FOMO (fear of missing out) and buy at the peak. Two pervasive cognitive distortions fuel this behavior:\n1. Anchoring to historical highs: Believing that because a stock once traded at $100, it is 'guaranteed' to return to $100, ignoring that underlying earning power or debt structure may have collapsed.\n2. Myopic loss aversion: Constantly monitoring intraday price ticks increases emotional distress, leading to impulsive, value-destroying trading activity.",
        "Consider a stock quoted at $70. An analyst has performed rigorous fundamental analysis, establishing a conservative intrinsic value range of $60 to $80 per share. Over the next month, broader market turmoil causes the market price to drop sharply to $50. Let us calculate the apparent discounts to intrinsic value:\n• Discount to conservative value ($60):\n  $$1 - \\frac{P}{V_{\\mathrm{cons}}} = 1 - \\frac{50}{60} = 1 - 0.8333 = 16.67\\%$$\n• Discount to optimistic upper value ($80):\n  $$1 - \\frac{P}{V_{\\mathrm{opt}}} = 1 - \\frac{50}{80} = 1 - 0.6250 = 37.50\\%$$\n\nAn amateur investor reacts in one of two flawed ways: either panicking and selling because the price fell from $70 to $50, or blindly buying more under the assumption that the $70 high is guaranteed to return. An intelligent investor conducts a diagnostic review: Did the price fall because of macro market mood swings, or did a fundamental event occur? If the company suffered a major unrecorded toxic tort lawsuit that permanently impairs its assets by $25 per share, its true conservative value is not $60, but $35! At $50, the stock is now overvalued, not a bargain. Price action alone tells you nothing about which scenario occurred.",
        "In your My notebook page, formulate an explicit Price-Change Protocol:\n1. The 48-Hour Cooling-Off Rule: When an existing holding drops by more than 15% or surges by more than 20%, enforce a mandatory 48-hour pause before placing any trade. This decouples emotional adrenaline from execution.\n2. The Fundamental Diagnostic Checklist: Ask three mandatory questions:\n   a. Have audited cash flows, customer demand, or balance sheet solvency deteriorated?\n   b. Has senior debt maturity or interest coverage changed?\n   c. Is my personal liquidity adequate, ensuring I am not forced to sell to meet cash obligations?\n3. Eradicate Price Anchors: Delete all references to historical peak prices from your tracking tools; an asset is worth only its future discounted cash flows, never what someone paid for it in the past.",
        r"\mathrm{discount\ to\ estimate} = 1 - \frac{P}{V}",
        'print("Discount to conservative value:", 1 - 50 / 60)\nprint("Discount to upper estimate:", 1 - 50 / 80)',
        "Calculate the discount to conservative ($60) and upper ($80) valuation estimates when price falls to $50. Describe how an intelligent investor investigates whether the price drop represents a Mr. Market opportunity or a permanent impairment of business fundamentals.",
        "At price $50, the discount is 1 - 50/60 = 16.67% against the conservative $60 value, and 1 - 50/80 = 37.50% against the upper $80 value. An intelligent investor does not rely on price movement alone; they audit corporate disclosures to determine whether business earning power remains intact. If cash flows are unaffected, Mr. Market is offering an attractive liquidity discount. If new liabilities or customer losses have impaired business value below $50, the price drop is an accurate reflection of economic decay rather than a buying opportunity.",
        [
            (
                "A lower quoted price with no completed business review proves:",
                "Neither a bargain nor a permanent impairment by itself",
                "A guaranteed return to the former high",
                "That every valuation estimate is unchanged",
                "A price drop alone merely reflects transacting sentiment; establishing whether it represents an undervalued bargain or a justified reaction to fundamental decay requires auditing current business evidence.",
            ),
            (
                "Price 50 against conservative value 60 gives a discount near:",
                "16.67%",
                "20%",
                "37.5%",
                "The discount formula relative to intrinsic value is 1 - P / V = 1 - 50 / 60 = 1 - 0.8333 = 16.67%.",
            ),
            (
                "Anchoring to a previous market high risks assuming:",
                "A historical quote is a promised future value",
                "Every liability has disappeared",
                "All future returns are independent",
                "Anchoring bias causes market participants to view past peak quotations as rightful targets, overlooking that the historical price may have been an irrational bubble or that underlying business fundamentals have permanently deteriorated.",
            ),
            (
                "A useful response to a dramatic quotation change begins with:",
                "A review of evidence, assumptions and liquidity constraints",
                "Automatically doubling the position",
                "Erasing the original decision journal",
                "A structured review decouples judgment from emotional market panic, systematically investigating whether corporate facts changed and confirming personal liquidity buffers before taking any action.",
            ),
        ],
        [BOOK, ALLOCATION],
    )
    # ------------------------------------------------------------------ 11.5
    add(
        "Goals, liquidity and the capacity to bear losses",
        "Defensive planning; modern course extension",
        "Separate willingness to accept risk from the financial ability to absorb it.",
        "One of the most dangerous points of confusion in wealth management is the conflation of risk tolerance with risk capacity:\n• Risk tolerance is psychological and emotional: it describes your subjective attitude toward market volatility, your comfort with fluctuating account balances, and whether paper drawdowns keep you awake at night.\n• Risk capacity is mathematical, financial, and structural: it describes your objective balance-sheet ability to sustain monetary losses without being forced to default on debt, disrupt essential household spending, or liquidate depressed assets to pay near-term bills.\n\nA market participant may possess an aggressive psychological risk tolerance, feeling completely unbothered by a 40% stock market crash. However, if that same individual faces a mandatory tuition payment, mortgage maturity, or business cash call in six months and holds all their money in equities, their risk capacity for that capital is exactly zero. When the crash occurs, their emotional bravery becomes irrelevant: forced liquidation at the market trough converts paper losses into permanent, unrecoverable capital destruction.\n\nTo prevent forced selling, careful investors deploy the **Three-Pot Liquidity Architecture**:\n1. The Emergency Reserve Pot: 6 to 12 months of non-negotiable living costs held strictly in liquid, capital-guaranteed bank deposits or short-term Treasury bills. This pot is never invested in volatile risk assets.\n2. The Dated Commitments Pot: Fixed expenditures due within the next 1 to 3 years (e.g. tax liabilities, tuition, medical payments, down payments). This capital must be matched in high-quality, fixed-income instruments with duration aligned precisely to the expenditure date.\n3. The Long-Horizon Capital Pot: Surplus capital with an investment horizon of 5 to 10+ years. Only this residual capital may be allocated to equities and long-term productive investments.",
        "Consider a household performing an objective balance-sheet audit:\n• Total liquid financial assets: A = 120 million rupiah.\n• Identified near-term commitments (due within 18 months): C_near_term = 30 million rupiah.\n• Required essential living emergency reserve (9 months): C_reserve = 24 million rupiah.\n\nWe determine the true long-horizon risk capital using the residual capacity equation:\n$$C_{\\mathrm{long\\ horizon}} = A - C_{\\mathrm{near\\ term}} - C_{\\mathrm{reserve}} = 120 - 30 - 24 = 66\\text{ million rupiah}$$\n\nOnly this 66 million rupiah may be allocated toward long-term risk assets. Now, let us stress-test this capital under an adverse macroeconomic shock where equity markets plunge by 30%:\n$$\\mathrm{Illustrative\\ Loss} = 66 \\times 0.30 = 19.8\\text{ million rupiah}$$\n$$\\mathrm{Ending\\ Risk\\ Capital} = 66 - 19.8 = 46.2\\text{ million rupiah}$$\n\nNotice the profound defensive stability of this architecture: although the equity sleeve suffered a painful 19.8 million rupiah drawdown, the household still possesses 24 million rupiah in cash reserves and 30 million rupiah in dedicated short-term funds. They do not face any liquidity emergency. They are never forced to sell their depressed shares at 46.2 million rupiah to buy groceries or pay immediate bills; they can comfortably wait out the multi-year economic recovery.",
        "In your My notebook page, formalize your personal balance-sheet architecture:\n1. Map the Three Pots: Explicitly calculate your Emergency Reserve, your Dated Commitments (next 1–3 years), and isolate your Long-Horizon Capital pool. Never invest capital needed within 36 months into equities.\n2. Stress-Test Forced Liquidation: Simulate a 35% drawdown on your long-horizon pool. Write down: 'Which obligation would force me to sell equities at the bottom if this drawdown occurred?' If any obligation appears, your equity allocation is too large.\n3. Debt Elimination Priority: High-interest consumer or margin debt represents a guaranteed negative yield. Repaying debt yielding 15% provides an immediate, risk-free 15% return that no volatile stock market can reliably match.",
        r"C_{\mathrm{long\ horizon}} = A - C_{\mathrm{near\ term}} - C_{\mathrm{reserve}}",
        'capital = 120 - 30 - 24\nprint("Long-horizon capital, million rupiah:", capital)\nprint("Illustrative 30% loss:", capital * 0.30)',
        "Calculate the separate capital pools for the fictional household and compute the 30% stress loss. Explain why relying exclusively on emotional risk tolerance while ignoring balance-sheet risk capacity is a primary cause of forced liquidation during market crashes.",
        "Subtracting 30 million of dated spending and 24 million of emergency reserves from 120 million leaves exactly 66 million rupiah of long-horizon capital; a 30% market stress loss erodes 19.8 million rupiah. Relying solely on emotional risk tolerance overlooks contractual cash obligations. If near-term liabilities come due during a market downturn, an investor with high emotional tolerance but insufficient liquid reserves will be legally or practically forced to sell depressed assets, converting temporary market drawdowns into catastrophic permanent capital impairment.",
        [
            (
                "Risk capacity concerns:",
                "The financial consequences of losses for obligations and goals",
                "Only enthusiasm for volatile investments",
                "The number of chart indicators used",
                "Risk capacity measures the structural ability of your balance sheet to withstand losses without jeopardizing mandatory living expenses, debt payments, or dated financial commitments.",
            ),
            (
                "120 minus 30 of spending and 24 of reserves leaves:",
                "66",
                "96",
                "90",
                "Long-horizon capital is calculated as total liquid assets minus near-term commitments minus emergency reserves: 120 - 30 - 24 = 66.",
            ),
            (
                "A person likes risk but needs the money soon. The plan must consider:",
                "The near-term liability even if emotional tolerance is high",
                "Only the person's confidence",
                "Only the highest historical return",
                "Subjective psychological risk tolerance cannot alter contractual cash requirements; money needed in the near term must be protected in low-risk, liquid instruments regardless of personal risk appetite.",
            ),
            (
                "The course's 24-million reserve is:",
                "A fictional assumption to analyze, not a universal prescription",
                "A required amount for every household",
                "A guarantee against every financial emergency",
                "Emergency reserve sizing depends on household living expenses, job stability, insurance coverage, and family dependents; the 24-million figure is a pedagogical case assumption.",
            ),
        ],
        [ALLOCATION, BOOK],
    )

    # ------------------------------------------------------------------ 11.6
    add(
        "Inflation and purchasing-power risk",
        "Inflation and the investor",
        "Distinguish a nominal account gain from an increase in purchasing power.",
        "A common illusion among novice investors is evaluating wealth exclusively in nominal currency units. An account statement showing a growing balance creates a comforting visual impression of progress. However, money has no intrinsic utility; its true economic value lies entirely in its purchasing power—the quantity of actual goods, healthcare, housing, and services it can acquire.\n\nThe mathematical relationship between nominal returns, inflation, and real purchasing power is governed by the exact Fisher compounding relation:\n$$1 + r_{\\mathrm{real}} = \\frac{1 + r_{\\mathrm{nominal,net}}}{1 + \\pi} \\implies r_{\\mathrm{real}} = \\frac{1 + r_{\\mathrm{nominal,net}}}{1 + \\pi} - 1$$\nWhen inflation rates and nominal returns are small, people often use the crude linear subtraction approximation: $r_{\\mathrm{real}} \\approx r_{\\mathrm{nominal}} - \\pi$. However, over extended compounding horizons or in inflationary environments, this approximation systematically overstates real gains.\n\nEvery asset class carries distinct purchasing-power risk profiles:\n• Cash and short-term deposits: Offer nominal safety of principal but guarantee real purchasing-power erosion whenever inflation exceeds net after-tax interest rates.\n• Fixed-income bonds: Fixed coupon payments lose real purchasing power as price levels rise, and rising inflation expectations push bond yields up, causing capital losses on existing bonds.\n• Equities: Represent fractional ownership of real productive operating assets. In the long run, businesses with genuine pricing power can raise customer prices to offset rising input costs. However, equities are NOT an automatic short-term inflation hedge: during sudden inflationary spikes, input cost shocks compress operating profit margins, and rising interest rates compress price-to-earnings valuation multiples.",
        "Let us examine two comparative financial scenarios over a one-year horizon where the cost of the investor's specific living goal increases by an inflation rate of π = 4.0% (π = 0.04):\n• Scenario 1 (Conservative Wealth Fund): The fund earns a net nominal return of r_nominal = 6.0% (r_nominal = 0.06). Let us calculate the exact real purchasing-power return:\n  $$1 + r_{\\mathrm{real}} = \\frac{1 + 0.06}{1 + 0.04} = \\frac{1.06}{1.04} \\approx 1.019231 \\implies r_{\\mathrm{real}} = +1.923\\%$$\n  (Notice that the crude linear approximation 6.0% - 4.0% = 2.0% slightly overstates the true gain).\n• Scenario 2 (Standard Bank Deposit): The deposit yields a modest nominal interest rate of r_nominal = 3.0% (r_nominal = 0.03). Computing the exact real return:\n  $$1 + r_{\\mathrm{real}} = \\frac{1 + 0.03}{1 + 0.04} = \\frac{1.03}{1.04} \\approx 0.990385 \\implies r_{\\mathrm{real}} = -0.962\\%$$\n\nIn Scenario 2, despite the bank statement showing a 3% nominal cash increase, the investor suffered a real purchasing-power loss of nearly 1.0%! Over a decade, a continuous -1% real drag quietly destroys more than 9.5% of the real purchasing power of accumulated savings.",
        "In your My notebook page, implement an Inflation Audit:\n1. Audit Personal Inflation: Recognize that official headline Consumer Price Index (CPI) figures measure an aggregate national basket. Your personal cost basket—dominated by education, healthcare, and housing—may experience inflation substantially higher than official headline CPI.\n2. Calculate Net Real Return: Require all investment projections to state returns net of fees and net of assumed inflation: $r_{\\mathrm{real}} = (1 + r_{\\mathrm{nominal,net}}) / (1 + \\pi) - 1$.\n3. Balance Safety and Growth: While cash protects nominal capital for near-term needs, a long-horizon portfolio must allocate sufficient capital to productive business equities to outpace purchasing-power erosion over decades.",
        r"1 + r_{\mathrm{real}} = \frac{1 + r_{\mathrm{nominal,net}}}{1 + \pi}",
        'print("Real return at 6% nominal:", 1.06 / 1.04 - 1)\nprint("Real return at 3% nominal:", 1.03 / 1.04 - 1)',
        "Calculate the exact real returns for 6% and 3% nominal gains under 4% inflation. Explain why equities cannot be treated as an automatic, foolproof inflation hedge over short-term horizons.",
        "Under 4% inflation, a 6% net nominal return produces an exact real return of 1.06 / 1.04 - 1 = +1.923%, while a 3% nominal return produces an exact real return of 1.03 / 1.04 - 1 = -0.962%. Equities are not an automatic short-term inflation hedge because rapid inflation increases raw material and labor costs faster than many businesses can raise prices, compressing profit margins. Additionally, central banks raise interest rates to combat inflation, which increases discount rates and depresses equity valuation multiples.",
        [
            (
                "A nominal gain necessarily increases purchasing power:",
                "No, inflation can exceed the net nominal return",
                "Yes whenever the account balance rises",
                "Only if the statement is printed",
                "Purchasing power reflects the volume of goods and services capital can buy; if inflation exceeds net nominal returns, real purchasing power declines even as nominal balances grow.",
            ),
            (
                "6% net nominal return with 4% inflation gives exact real return near:",
                "1.923%",
                "2.000% exactly",
                "10%",
                "The exact compounded Fisher relation is (1 + 0.06) / (1 + 0.04) - 1 = 1.06 / 1.04 - 1 = 0.01923, or approximately 1.923%.",
            ),
            (
                "Equity ownership is an automatic inflation hedge over every horizon:",
                "No; business economics and valuation also matter",
                "Yes for every company",
                "Yes when a stock is popular",
                "A company's pricing power, input cost sensitivity, debt structure, and purchase valuation determine how it fares under inflation; sudden inflation often compresses margins and depresses valuation multiples in the short run.",
            ),
            (
                "A published inflation index and a household's goal costs can:",
                "Differ because spending baskets differ",
                "Never differ",
                "Be replaced by a stock's recent return",
                "Official Consumer Price Index numbers measure an aggregate statistical basket; an individual household's actual spending basket (e.g. tuition, healthcare, regional rent) can experience significantly different inflation rates.",
            ),
        ],
        [BOOK, ALLOCATION],
    )

    # ------------------------------------------------------------------ 11.7
    add(
        "Diversification and hidden concentration",
        "Portfolio policy and diversification",
        "Look through labels to identify the actual sources of portfolio risk.",
        "Diversification is often celebrated as the only 'free lunch' in finance. By combining assets whose returns are imperfectly correlated, an investor can reduce portfolio variance and eliminate unsystematic (company-specific) risk without reducing expected return. If one company suffers an industrial accident or executive fraud, a well-diversified portfolio absorbs the loss without catastrophic damage.\n\nHowever, true diversification requires looking beyond marketing labels. A widespread trap among individual investors is the **superficial diversification fallacy**: believing that holding five different mutual funds, three fintech apps, or twenty distinct stock tickers automatically ensures diversification. In modern financial markets, fund products frequently hold identical underlying mega-cap companies or share the exact same underlying economic vulnerabilities.\n\nTo measure true exposure, an investor must compute their **Look-Through Exposure** across all accounts:\n$$w_{\\mathrm{company}} = \\sum_j w_{\\mathrm{fund}, j} \\times w_{\\mathrm{company\\ within\\ fund}, j}$$\n\nFurthermore, consider **human capital concentration**: your primary source of financial cash flow is your employment salary. If you work for a technology company and also invest heavily in company stock and technology-sector mutual funds, you have created extreme hidden concentration. An industry downturn can simultaneously eliminate your employment income, wipe out your employer stock options, and depress your investment portfolio.",
        "Examine an investor who holds two separate mutual funds with completely different brand names:\n• Fund A: An equity growth fund representing 60% of the total portfolio (w_fund,A = 0.60). An audit of its portfolio disclosures reveals it holds 30% of its assets in Megacorp (w_company,A = 0.30).\n• Fund B: A dividend value fund representing the remaining 40% of the portfolio (w_fund,B = 0.40). Its disclosures reveal it holds 20% in Megacorp (w_company,B = 0.20).\n\nLet us calculate the investor's total look-through exposure to Megacorp:\n$$w_{\\mathrm{Megacorp}} = (0.60 \\times 0.30) + (0.40 \\times 0.20) = 0.18 + 0.08 = 0.26 \\implies 26\\%$$\n\nMore than a quarter (26%) of the investor's entire accumulated wealth is concentrated in a single corporate enterprise! Despite holding two distinct funds from different asset managers, the investor is dangerously exposed to Megacorp's balance sheet liabilities, accounting controversies, and competitive fortunes. If Megacorp experiences an unexpected collapse and drops 50%, the investor's overall portfolio suffers a direct 13% loss (0.26 × 0.50) from this single holding alone.",
        "In your My notebook page, institute an Annual Look-Through Audit:\n1. Consolidate Top Holdings: Aggregate the top 10 individual stock exposures across all mutual funds, ETFs, retirement accounts, and direct shareholdings. Cap single-company exposure at a strict threshold (e.g. no single company > 10% of total wealth).\n2. Sector and Currency Audit: Quantify total exposure to individual economic sectors (e.g. banking, technology, real estate) and foreign currencies. Ensure no single sector exceeds 25% of your equity sleeve.\n3. Human Capital Safeguard: Limit direct investment in your employer's stock to under 5% of total liquid assets. Your labor income already provides substantial exposure to your employer's ongoing solvency.",
        r"w_{\mathrm{company}} = \sum_j w_{\mathrm{fund},j} \cdot w_{\mathrm{company\ within\ fund},j}",
        'print("Look-through company weight:", 0.6 * 0.3 + 0.4 * 0.2)',
        "Calculate the total look-through company weight across Fund A (60% weight, 30% company) and Fund B (40% weight, 20% company). Explain three ways a portfolio can remain heavily concentrated despite holding multiple product wrappers.",
        "Total look-through exposure is 0.60 × 0.30 + 0.40 × 0.20 = 0.18 + 0.08 = 0.26, or 26.0%. A portfolio can remain concentrated despite holding multiple fund wrappers through: (1) overlapping mega-cap holdings where different fund managers buy the same market-cap-weighted stocks; (2) shared sector or macroeconomic drivers where different companies all depend on the same interest rate, commodity price, or regulatory regime; and (3) correlated human capital, where an investor concentrates personal wealth into their own employer or local domestic industry.",
        [
            (
                "Two fund names necessarily mean two independent sets of holdings:",
                "No; inspect their underlying overlap",
                "Yes by definition",
                "Only when their fees differ",
                "Different fund wrappers often hold identical underlying stocks; assessing diversification requires performing a look-through audit of the underlying portfolio holdings.",
            ),
            (
                "60%×30% plus 40%×20% gives company exposure of:",
                "26%",
                "50%",
                "12%",
                "Multiplying portfolio fund weights by internal stock allocations produces (0.60 × 0.30) + (0.40 × 0.20) = 0.18 + 0.08 = 0.26, or 26%.",
            ),
            (
                "Diversification guarantees no broad market loss:",
                "No; common risks can affect many assets together",
                "Yes if there are ten tickers",
                "Yes if all products have different names",
                "Diversification reduces company-specific (idiosyncratic) risk, but cannot eliminate systematic (market-wide) risk such as recessions, liquidity crises, or rising interest rates that impact all assets simultaneously.",
            ),
            (
                "Employer stock deserves extra concentration review because:",
                "Investment wealth and labor income may share the same business risk",
                "It is always risk-free",
                "Salary guarantees the share price",
                "Holding substantial equity in your employer concentrates both your monthly salary and your accumulated savings into the fortunes of a single corporate balance sheet.",
            ),
        ],
        [ALLOCATION, BOOK],
    )

    # ------------------------------------------------------------------ 11.8
    add(
        "Margin of safety and permanent impairment",
        "Margin of safety",
        "Use a conservative valuation cushion while acknowledging uncertainty and business deterioration.",
        "In Chapter 20 of The Intelligent Investor, Benjamin Graham identified the secret of sound investment in three words: **MARGIN OF SAFETY**. The margin of safety is the discount between the market price paid and the conservatively estimated intrinsic value of the business. Graham intended this cushion to perform a vital engineering function: to absorb the inevitable errors in human forecasting, unforeseen industry disruptions, and cyclical recessions without causing the investor permanent capital loss.\n\nCrucially, an intelligent investor must distinguish between two fundamentally different types of loss:\n• Temporary quotation volatility: The daily, weekly, or monthly price fluctuations generated by Mr. Market's mood swings. If a business remains solvent, maintains its competitive earning power, and services its debt, quotation declines are temporary paper marks that offer buying opportunities rather than destruction of capital.\n• Permanent impairment of capital: An unrecoverable loss of economic value caused by corporate insolvency, unpayable debt defaults, severe operational obsolescence, or catastrophic legal liabilities. A margin of safety is designed specifically to protect against permanent capital impairment.\n\nBeware the 'Optimizer's Curse': if you screen a stock universe solely for the widest apparent discount to consensus target price, you will systematically select companies with the most fragile accounting or hidden liabilities. True protection requires anchoring your margin of safety against a *conservative downside valuation*, rather than an optimistic forecast.",
        "Consider a manufacturing company currently trading at a market price of P = $60 per share. An analyst constructs three valuation scenarios based on detailed balance-sheet forensics:\n• Optimistic scenario: V_opt = $120 per share (assumes rapid expansion and record margins).\n• Base scenario: V_base = $100 per share (assumes historical average cash flows).\n• Conservative downside scenario: V_cons = $70 per share (assumes severe recession, customer defaults, and asset recovery haircuts).\n\nLet us calculate the apparent margin of safety under each scenario:\n• Optimistic margin: $1 - \\frac{60}{120} = 50.00\\%$\n• Base margin: $1 - \\frac{60}{100} = 40.00\\%$\n• Conservative margin:\n  $$\\mathrm{Conservative\\ margin} = 1 - \\frac{60}{70} = \\frac{10}{70} = \\frac{1}{7} \\approx 14.2857\\%$$\n\nNow suppose the investor enforces a disciplined policy rule: 'I require at least a 25% margin of safety (m = 0.25) against my conservative valuation estimate.' Let us calculate the maximum allowable purchase price under this fictional rule:\n$$P_{\\max} = (1 - m) \\times V_{\\mathrm{cons}} = (1 - 0.25) \\times 70 = 0.75 \\times 70 = \\$52.50$$\n\nAt the current market price of $60, the stock FAILS the conservative rule! Even though the base-case discount looks seductive at 40%, buying at $60 leaves only a slim 14.29% cushion against conservative reality. If the recession hits and unrecorded pension liabilities emerge, the cushion evaporates completely.",
        "In your My notebook page, formulate your Valuation and Margin of Safety Protocol:\n1. Construct the Conservative Downside Baseline: Always establish a stressed conservative valuation that haircuts receivables, tests inventory liquidation values, and incorporates debt service stress.\n2. Enforce the Price Ceiling: Calculate your maximum allowable purchase price: $P_{\\max} = (1 - m) \\times V_{\\mathrm{conservative}}$. Never exceed this ceiling, regardless of social media hype or FOMO.\n3. Verify Debt Seniority: Inspect the debt maturity wall. If debt matures during a cyclical trough and the business lacks refinancing capacity, even a 50% discount to asset book value cannot protect against bankruptcy.",
        r"\mathrm{margin} = 1 - \frac{P}{V},\qquad P_{\max} = (1 - m) V_{\mathrm{conservative}}",
        'print("Conservative margin:", 1 - 60 / 70)\nprint("Maximum price under the fictional rule:", 70 * (1 - 0.25))',
        "Calculate the conservative margin of safety for price $60 against value $70 and determine the maximum purchase price under a 25% conservative cushion rule. Explain how the Optimizer's Curse causes unadjusted discount screens to select value traps.",
        "The conservative margin of safety is 1 - 60 / 70 = 10 / 70 = 14.2857% (or 1/7); under a 25% cushion rule against conservative value $70, the maximum allowable price is 70 × (1 - 0.25) = $52.50. At price $60, the purchase fails the policy. The Optimizer's Curse describes how screening blindly for the highest apparent discount systematically selects companies whose financial estimates are most exaggerated by management or burdened by unrecorded liabilities (value traps), making disciplined conservative haircuts essential.",
        [
            (
                "A margin of safety should be interpreted as:",
                "A cushion against errors and adverse outcomes, not a guarantee",
                "A promise that the quoted price cannot fall",
                "A replacement for examining liabilities",
                "The margin of safety provides an analytical cushion designed to absorb unforeseen disruptions and valuation errors, but it cannot prevent market fluctuations or compensate for unexamined corporate debt.",
            ),
            (
                "Conservative value 70 with a required 25% cushion permits price up to:",
                "52.5",
                "87.5",
                "56",
                "Applying a 25% required cushion to conservative value 70 establishes a maximum purchase price of 70 × (1 - 0.25) = 70 × 0.75 = 52.5.",
            ),
            (
                "A large base-case discount with a weak conservative case calls for:",
                "Examining downside assumptions before relying on the headline discount",
                "Ignoring the lower estimate",
                "Assuming value is known exactly",
                "A wide headline discount against an optimistic or base forecast is often fragile; an investor must audit downside risks, debt burdens, and asset recovery haircuts before committing capital.",
            ),
            (
                "Permanent impairment refers most directly to:",
                "A lasting deterioration in the economic claim",
                "Every daily price decline",
                "Only a change in chart scale",
                "Permanent impairment describes lasting, unrecoverable destruction of underlying business earning power, solvency, or assets, in sharp contrast to temporary market quotation fluctuations.",
            ),
        ],
        [BOOK, FILINGS],
    )
    # ------------------------------------------------------------------ 11.9
    add(
        "Allocation policy before product selection",
        "General portfolio policy; modern planning extension",
        "Connect a broad allocation to a goal and stress its consequences before choosing products.",
        "A foundational insight of modern portfolio theory, first documented comprehensively by Brinson, Hood, and Beebower, is that broad **asset allocation policy** determines over 90% of the variation in portfolio returns over time. Market timing (attempting to jump in and out of the market) and security selection (picking individual winning stocks) account for only a tiny fraction of long-term variance and frequently generate net negative returns after accounting for transaction costs, spreads, and taxes.\n\nTherefore, an intelligent investor always establishes their overall allocation policy *before* evaluating any specific fund or stock. The allocation policy determines the broad proportions of wealth committed to equities (for long-term capital growth and purchasing-power protection) versus fixed income and cash equivalents (for capital preservation, current income, and deflationary stability). Graham famously advised that a defensive investor should never hold less than 25% or more than 75% in common stocks, using a 50/50 balance as the baseline neutral anchor.\n\nCrucially, never assume that stocks and bonds will always move in opposite directions. While high-grade government bonds frequently rally during economic recessions (as central banks slash interest rates), an inflationary supply shock (such as 1969, 1973, or 2022) causes interest rates to soar, triggering simultaneous sharp drawdowns in both equities and fixed-income bonds. Portfolio policy must be rigorously stress-tested against such joint-drawdown scenarios before capital is committed.",
        "Consider an investor establishing a classic 60/40 asset allocation policy on a 100-unit portfolio:\n• Equities sleeve: w_e = 60% (w_e = 0.60), assigned 60 units of capital.\n• Fixed-income bonds sleeve: w_b = 40% (w_b = 0.40), assigned 40 units of capital.\n\nNow suppose an acute stagflationary shock hits financial markets: central banks raise interest rates rapidly to combat persistent inflation while economic activity slows. As a consequence, equities plunge by R_e = -30.0% (-0.30), and bond prices simultaneously drop by R_b = -10.0% (-0.10) as yields rise.\n\nLet us compute the combined portfolio return:\n$$R_p = \\sum_i w_i R_i = (w_e \\times R_e) + (w_b \\times R_b) = (0.60 \\times -0.30) + (0.40 \\times -0.10)$$\n$$R_p = -0.18 - 0.04 = -0.22 \\implies -22.0\\%$$\n\nEnding portfolio wealth declines from 100 to 78 units:\n$$\\mathrm{Ending\\ Wealth} = 100 \\times (1 + R_p) = 100 \\times (1 - 0.22) = 78\\text{ units}$$\n\nNotice that the bonds did not prevent a substantial portfolio loss; however, because the 40% bond sleeve lost only 10% (compared to equities losing 30%), it cushioned the overall decline from -30% down to -22%. The investor must verify in advance whether their balance-sheet risk capacity can comfortably carry this 22-unit drawdown without triggering panic or forced liquidation.",
        "In your My notebook page, formulate your Asset Allocation Policy Statement:\n1. Define Policy Targets: Specify target weights for each sleeve (e.g. 60% Global Equity Index, 30% Intermediate Government Bonds, 10% Cash Reserves). Give each sleeve an explicit operational job.\n2. Mandate Joint-Drawdown Stress Tests: Model a -35% equity shock combined with a -10% bond shock. Check whether your remaining portfolio wealth satisfies your 10-year goal trajectory.\n3. Establish Change Triggers: Forbid ad-hoc allocation changes based on daily financial news or market euphoria. Permit changes to target weights *only* when personal financial milestones change (e.g. marriage, retirement, inheritance) or upon a scheduled annual policy review.",
        r"R_p = \sum_i w_i R_i,\qquad \sum_i w_i = 1",
        'loss = 0.6 * (-0.30) + 0.4 * (-0.10)\nprint("Scenario portfolio return:", loss)\nprint("Scenario ending wealth:", 100 * (1 + loss))',
        "Calculate the scenario portfolio return for a 60/40 equity/bond allocation when equities decline 30% and bonds decline 10%. Explain why asset allocation policy should precede individual product selection in an investment plan.",
        "The weighted portfolio return is (0.60 × -0.30) + (0.40 × -0.10) = -0.18 - 0.04 = -0.22, or -22.0%, leaving 78 units of wealth. Asset allocation policy must precede individual product selection because empirical research demonstrates that the broad mix of asset classes drives over 90% of long-term return variance and drawdown depth. Selecting individual funds or stocks before establishing policy targets leads to disjointed, emotionally driven portfolios that fail to match the investor's true risk capacity and horizon.",
        [
            (
                "Broad allocation should begin with:",
                "Goals, horizon, liquidity and capacity",
                "Only the best recent fund return",
                "Only a product's promotional name",
                "Asset allocation must be grounded in the investor's concrete financial goals, investment horizon, non-negotiable liquidity needs, and objective balance-sheet risk capacity.",
            ),
            (
                "60% at −30% plus 40% at −10% produces:",
                "−22%",
                "−20%",
                "−40%",
                "The weighted portfolio return is calculated as (0.60 × -0.30) + (0.40 × -0.10) = -0.18 - 0.04 = -0.22, or -22%.",
            ),
            (
                "Stocks and bonds must always move in opposite directions:",
                "No; both can decline in the same scenario",
                "Yes under every inflation outcome",
                "Only when allocation weights sum to one",
                "While stocks and bonds often exhibit low or negative correlation during ordinary recessions, both asset classes can decline simultaneously during inflationary periods or sharp interest-rate spikes.",
            ),
            (
                "A policy change should be justified by:",
                "Documented changes in goals, constraints or supported assumptions",
                "Only a day's market excitement",
                "The desire to match every headline",
                "Disciplined investors modify their target allocation policy only in response to documented changes in life circumstances, financial goals, or verifiable long-term constraints, never in reaction to daily market volatility.",
            ),
        ],
        [ALLOCATION, BOOK],
    )

    # ------------------------------------------------------------------ 11.10
    add(
        "Rebalancing, drift and transaction discipline",
        "Portfolio policy through market fluctuations",
        "Restore a chosen exposure deliberately while accounting for costs and changing circumstances.",
        "Over any investment horizon, asset classes produce divergent returns: equities may surge during economic expansions while fixed-income returns remain modest, or equities may plummet during market panics. As a mathematical consequence, an unmanaged portfolio naturally experiences **portfolio drift**: its internal asset weights drift away from the target allocation policy chosen by the investor.\n\nLeft unchecked, drift distorts your risk profile: after a prolonged bull market, a 60/40 portfolio can drift to 80/20, exposing the investor to far greater equity drawdown risk precisely when valuations are extended. Conversely, after a crash, the equity sleeve shrinks, depriving the portfolio of recovery potential.\n\n**Rebalancing** is the disciplined, unemotional process of restoring portfolio weights toward their target policy by trimming outperforming assets and buying underperforming assets. It enforces the classic mandate: *buy low, sell high*. There are three primary operational approaches to rebalancing:\n1. Calendar Rebalancing: Reviewing and rebalancing on a fixed schedule (e.g. annually or semi-annually).\n2. Tolerance Band Rebalancing: Rebalancing only when an asset's weight drifts outside an explicit corridor (e.g. ±5 percentage points from target, such as 55% to 65% for a 60% target).\n3. Cash-Flow Rebalancing: Directing new monthly savings, salary contributions, or dividend payouts into currently underweighted asset sleeves, restoring target weights without selling winners or triggering trading commissions and capital gains taxes.",
        "Examine the step-by-step arithmetic of portfolio drift and rebalancing on a 100-unit portfolio with a 60/40 target allocation:\n• Initial state: Equities = 60 units (w_e* = 60%), Bonds = 40 units (w_b* = 40%). Total wealth = 100 units.\n• Market movement: Over the next year, equities appreciate by 20% (60 × 1.20 = 72 units), while bonds earn a flat 0% return (remaining at 40 units).\n• Total drifted wealth: V_total = 72 + 40 = 112 units.\n\nLet us compute the drifted equity weight:\n$$w_{e,\\mathrm{drift}} = \\frac{V_e}{V_{\\mathrm{total}}} = \\frac{72}{112} = \\frac{9}{14} \\approx 64.2857\\%$$\n\nThe equity weight has drifted from 60.0% up to 64.286%. Now let us compute the exact dollar rebalance required to restore the 60.0% target policy (w_e* = 0.60):\n$$V_e^* = w_e^* \\times V_{\\mathrm{total}} = 0.60 \\times 112 = 67.20\\text{ units}$$\n$$\\Delta V_e = V_e - V_e^* = 72.00 - 67.20 = 4.80\\text{ units}$$\n\nNotice that restoring the 60/40 allocation requires transferring exactly 4.8 units from equities into bonds (selling 4.8 of equity to buy 4.8 of bonds). Beware the widespread amateur mistake of selling the entire 12-unit equity gain! Selling 12 units would reduce equities to 60 on a 112-unit portfolio, dropping the equity weight down to 53.57% and unintentionally under-allocating to equities.",
        "In your My notebook page, formalize your Rebalancing Protocol:\n1. Establish Rebalancing Corridors: Implement a ±5% tolerance band around target weights (e.g. for a 60% equity target, rebalance only if equity falls below 55% or rises above 65%). This avoids costly micro-trading.\n2. Prioritize Cash-Flow Rebalancing: When rebalancing is indicated, first check whether new monthly savings or quarterly dividend payouts can be routed into the underweight sleeve before executing taxable sales.\n3. Friction Audit: Before executing any portfolio sale, verify all brokerage fees, exchange commissions, bid-ask spreads, and capital gains tax liabilities to ensure the rebalancing benefit exceeds implementation costs.",
        r"w_{i,\mathrm{drift}} = \frac{V_i}{\sum_j V_j},\qquad \Delta V_i = w_i^* V_{\mathrm{total}} - V_i",
        'print("Drifted equity weight:", 72 / 112)\nprint("Equity sale before costs:", 72 - 0.6 * 112)',
        "Calculate the drifted equity weight and the required pre-cost equity sale to restore a 60/40 allocation after equity rises to 72 and bonds remain at 40. Explain why selling the entire 12-unit gain is a mathematical error.",
        "The drifted equity weight is 72 / 112 = 9 / 14 ≈ 64.2857%; target equity value is 0.60 × 112 = 67.20, requiring an equity sale of 72 - 67.20 = 4.80 units before costs. Selling the entire 12-unit gain is an error because it ignores that total portfolio wealth expanded to 112; selling 12 would reduce equity to 60 on 112 (53.57%), unnecessarily underweighting equities and failing to maintain the intended 60% risk exposure.",
        [
            (
                "72 of equities in a 112 portfolio is an equity weight near:",
                "64.286%",
                "72%",
                "60%",
                "The drifted equity weight is calculated as current equity value divided by total portfolio wealth: 72 / 112 = 9 / 14 ≈ 0.64286, or 64.286%.",
            ),
            (
                "Restoring 60% equity in that portfolio requires selling:",
                "4.8",
                "12",
                "7.2",
                "Target equity is 0.60 × 112 = 67.2; current equity of 72 exceeds the target by exactly 72 - 67.2 = 4.8 units.",
            ),
            (
                "Rebalancing to a fixed policy necessarily predicts imminent price reversal:",
                "No; it restores the planned exposure",
                "Yes for every recent winner",
                "Only if the investor uses a calendar",
                "Rebalancing is a risk-management rule designed to maintain the investor's intended exposure bands, not a speculative forecast that outperforming assets are about to decline.",
            ),
            (
                "Frequent tiny rebalances require scrutiny because:",
                "Costs may exceed their practical risk-management benefit",
                "Fees always become negative",
                "They guarantee a more diversified universe",
                "Executing frequent trades for negligible weight deviations generates excessive brokerage fees, bid-ask spreads, and potential tax liabilities without meaningfully reducing portfolio risk.",
            ),
        ],
        [ALLOCATION, FEES],
    )

    # ------------------------------------------------------------------ 11.11
    add(
        "Funds, fees and the price of convenience",
        "Investment funds; modern product comparison extension",
        "Compare a fund's actual exposure, costs and trading terms rather than its recent ranking.",
        "Pooled investment vehicles—such as mutual funds, unit investment trusts, and exchange-traded funds (ETFs)—offer retail and institutional investors remarkable convenience: instant diversification across hundreds of securities, professional administrative recordkeeping, and automated dividend reinvestment. However, an intelligent investor must recognize that a fund is merely a legal wrapper; its investment merit depends entirely on its underlying portfolio holdings, its governance mandate, and, above all, its **total cost of ownership**.\n\nManagement fees and operational expenses are deducted continuously from fund assets, quietly reducing the daily Net Asset Value (NAV). Because investment returns compound geometrically, an apparently small annual difference in fund expense ratios—such as 0.20% for a broad index ETF versus 1.50% for an active mutual fund—compounds into a massive wealth disparity over an investor's career. Under the standard simplified convention of subtracting annual fees from gross returns, wealth after T years is governed by:\n$$W_T = W_0 \\times (1 + r_{\\mathrm{gross}} - f)^T$$\n\nFurthermore, an investor must be vigilant regarding hidden friction beyond the stated expense ratio:\n• Portfolio turnover costs: High-turnover active funds trade securities constantly, incurring bid-ask spread friction and broker commissions that are deducted directly from performance rather than reported in the expense ratio.\n• Sales loads and 12b-1 fees: Front-end charges, redemption penalties, and ongoing distribution trailer fees paid to advisers to incentivize product sales.\n• Cash drag: Active managers holding significant cash to meet redemptions or time the market, depressing returns during bull markets.",
        "Consider an investor committing W_0 = $10,000 into an equity investment over a T = 20-year horizon. Suppose both funds invest in the identical equity universe, achieving an identical gross annualized market return of r_gross = 6.0% (0.06):\n• Low-Cost Index ETF: The fund charges a competitive annual total expense ratio of f_low = 0.20% (0.002). The net compounding rate is 6.0% - 0.2% = 5.8% (0.058):\n  $$W_{20,\\mathrm{low}} = 10{,}000 \\times (1 + 0.058)^{20} = 10{,}000 \\times (1.058)^{20} \\approx 10{,}000 \\times 3.0874 = \\$30{,}874$$\n• High-Cost Active Mutual Fund: The fund charges an active management expense ratio of f_high = 1.50% (0.015). The net compounding rate is 6.0% - 1.5% = 4.5% (0.045):\n  $$W_{20,\\mathrm{high}} = 10{,}000 \\times (1 + 0.045)^{20} = 10{,}000 \\times (1.045)^{20} \\approx 10{,}000 \\times 2.4117 = \\$24{,}117$$\n\nLet us compute the catastrophic cumulative fee gap:\n$$\\mathrm{Fee\\ Gap} = W_{20,\\mathrm{low}} - W_{20,\\mathrm{high}} = \\$30{,}874 - \\$24{,}117 = \\$6{,}757$$\n\nOver twenty years, the seemingly modest 1.30% fee difference silently confiscated $6,757—representing more than 67.5% of the investor's entire original starting principal! The investor took 100% of the market risk, yet the fund management company captured over two-thirds of the starting capital in fees.",
        "In your My notebook page, implement an explicit Fund Due Diligence Protocol:\n1. Audit the Stated Expense Ratio: Never invest in a core equity index fund charging over 0.25% annually, or a core bond fund charging over 0.20%. Low-cost index funds tracking identical benchmarks are widely available.\n2. Verify Net Reporting Conventions: When comparing historical fund performance, verify whether published returns already reflect the expense ratio. Never subtract an expense ratio a second time from net published returns.\n3. Inspect Portfolio Turnover: Avoid funds with annual turnover exceeding 30%, which indicates rapid speculative churn and unmeasured execution friction.",
        r"W_T = W_0 (1 + r_{\mathrm{gross}} - f)^T\quad\mathrm{(simplified\ fee\ convention)}",
        'low = 10000 * (1.06 - 0.002) ** 20\nhigh = 10000 * (1.06 - 0.015) ** 20\nprint("Lower-fee wealth:", low)\nprint("Higher-fee wealth:", high)\nprint("Illustrative fee gap:", low - high)',
        "Calculate the 20-year ending wealth under 0.2% and 1.5% fee structures with a 6% gross return on $10,000, and quantify the resulting fee drag. Explain why past performance rankings are an unreliable guide to future fund selection.",
        "At 5.8% net compounding (0.2% fee), $10,000 grows to approximately $30,874; at 4.5% net compounding (1.5% fee), it grows to $24,117, resulting in a $6,757 wealth gap. Past performance rankings are notoriously unreliable because academic studies (e.g. Carhart 1997, Fama & French 2010) show that short-term top performance is largely driven by random luck or temporary style factor tilts; once fees and transaction costs are deducted, fund performance exhibits mean reversion rather than persistent outperformance.",
        [
            (
                "A sector fund necessarily provides broad diversification:",
                "No; its holdings may share concentrated sector risk",
                "Yes because it is called a fund",
                "Only if it has a high expense ratio",
                "A sector fund concentrates capital within a single industry (such as energy or technology), exposing the investor to severe sector-specific downturns regardless of how many individual stocks it holds.",
            ),
            (
                "Under the stated subtraction convention, 6% gross less 1.5% annual fee compounds at:",
                "4.5%",
                "7.5%",
                "5.8%",
                "Under the simplified subtraction convention, the net annual compounding rate is calculated as 6.0% - 1.5% = 4.5%.",
            ),
            (
                "A performance figure already net of an expense ratio should have that same fee:",
                "Identified without subtracting it a second time",
                "Subtracted again automatically",
                "Added back and called net",
                "When reviewing published fund performance, check the reporting convention; if returns are already net of the annual expense ratio, subtracting the fee again would double-count costs.",
            ),
            (
                "A useful fund comparison examines:",
                "Mandate, holdings, costs, benchmark and access terms",
                "Only the latest winner ranking",
                "Only the brand's popularity",
                "Rigorous fund evaluation requires analyzing the investment objective, underlying holdings, total fee structure, tracking error against benchmark, and redemption liquidity terms.",
            ),
        ],
        [FEES, ALLOCATION],
    )

    # ------------------------------------------------------------------ 11.12
    add(
        "Regular contributions and the limits of averaging",
        "Disciplined purchasing; modern planning extension",
        "Understand what a regular contribution rule does and does not protect against.",
        "A central pillar of disciplined financial planning is regular scheduled investing, widely known as **Dollar-Cost Averaging (DCA)**. Under this strategy, an investor commits a fixed monetary sum (e.g. $100 or 1 million rupiah) into a designated asset at consistent calendar intervals (e.g. monthly), regardless of prevailing market headlines or price fluctuations.\n\nThe mathematical mechanics of dollar-cost averaging stem from the properties of the **harmonic mean**: because you invest a fixed currency amount at each interval, your money automatically purchases *more units when the price is low* and *fewer units when the price is high*. As a consequence, your average purchase cost per unit is strictly lower than the simple arithmetic average of the market prices:\n$$\\mathrm{average\\ cost\\ per\\ unit} = \\frac{\\sum_t C_t}{\\sum_t \\frac{C_t}{P_t}} = \\frac{\\mathrm{Total\\ Capital\\ Invested}}{\\mathrm{Total\\ Units\\ Acquired}}$$\n\nHowever, an intelligent investor must recognize the vital boundaries and limitations of dollar-cost averaging:\n1. DCA does NOT guarantee a profit or prevent capital loss: If an asset suffers continuous fundamental deterioration or bankruptcy, averaging down simply pours good money after bad, accelerating total capital destruction.\n2. DCA vs Lump-Sum Investing: When investing an already existing lump sum, historical empirical studies show that immediate lump-sum investing outperforms dollar-cost averaging approximately two-thirds of the time, because markets tend to rise over time (the equity risk premium). However, DCA provides immense behavioral value by mitigating regret risk and smoothing emotional entry.\n3. Natural Savings Flow: When capital originates from new monthly salary savings, dollar-cost averaging is the natural, optimal mechanism for continuous wealth accumulation.",
        "Consider an investor executing two scheduled monthly contributions of C_1 = $100 and C_2 = $100:\n• Month 1: Market quotation is P_1 = $10 per unit. The $100 purchase acquires:\n  $$n_1 = \\frac{100}{10} = 10\\text{ units}$$\n• Month 2: A sudden market panic causes prices to drop by 50% to P_2 = $5 per unit. The $100 purchase acquires:\n  $$n_2 = \\frac{100}{5} = 20\\text{ units}$$\n\nLet us compute the total position metrics:\n• Total capital invested: $100 + $100 = $200.\n• Total units acquired: 10 + 20 = 30 units.\n• Average purchase cost per unit:\n  $$\\mathrm{Average\\ Cost} = \\frac{200}{30} = \\$6.6667\\text{ per unit}$$\n\nNotice the power of the harmonic mean: while the simple arithmetic average of the two market prices is (10 + 5) / 2 = $7.50, the investor's actual cost per unit is only $6.67! Because they bought twice as many units at $5 than at $10, their cost basis was dragged down significantly.\n\nHowever, observe the crucial risk lesson: if the market price remains at $5, the investor's 30 units are worth 30 × $5 = $150. Despite achieving a low average cost of $6.67, the investor carries an unrealized loss of $50 on their $200 invested capital. A lower average cost provides a mathematical cushion, but it cannot manufacture profits if the asset fails to recover.",
        "In your My notebook page, formulate your Scheduled Contribution Rules:\n1. Automate Monthly Savings: Establish automated standing transfers from your monthly income into your core diversified index funds on pay day, removing emotional hesitation from the contribution loop.\n2. The Anti-Averaging-Down Safeguard: Strictly prohibit dollar-cost averaging into individual stocks that have suffered fundamental thesis failure (e.g. lost competitive advantage, debt covenant breach, accounting scandal). Average down *only* in broadly diversified index funds.\n3. The Lump-Sum Compromise: If deploying a large existing lump sum (e.g. business sale or inheritance), commit to a pre-scheduled 6- to 12-month DCA schedule to manage psychological regret, pre-committing dates in advance.",
        r"\mathrm{average\ cost/unit} = \frac{\sum_t C_t}{\sum_t C_t/P_t}",
        'units = 100 / 10 + 100 / 5\nprint("Total units:", units)\nprint("Average cost:", 200 / units)\nprint("Value at price 5:", units * 5)',
        "Reconcile total contributions, units acquired, average cost per unit, and ending portfolio value for the two $100 purchases at $10 and $5. Explain why dollar-cost averaging cannot rescue an unexamined or deteriorating individual stock thesis.",
        "The two $100 purchases acquire 10 units at $10 and 20 units at $5, yielding 30 total units on $200 invested capital for an average cost of 200 / 30 = $6.667 per unit. At price $5, ending value is 30 × 5 = $150, reflecting a $50 loss. Dollar-cost averaging cannot rescue a deteriorating individual company because buying additional shares as prices fall simply magnifies exposure to an enterprise whose underlying business earning power or solvency may be collapsing toward zero.",
        [
            (
                "100 invested at 10 and 100 at 5 buy a total of:",
                "30 units",
                "20 units",
                "15 units",
                "The first purchase acquires 100 / 10 = 10 units, and the second acquires 100 / 5 = 20 units, totaling 10 + 20 = 30 units.",
            ),
            (
                "The average cost of those purchases is closest to:",
                "6.667 per unit",
                "7.5 per unit",
                "5 per unit",
                "Average cost per unit is calculated as total capital invested divided by total units acquired: 200 / 30 ≈ 6.667, which is lower than the simple price average of 7.5.",
            ),
            (
                "A lower average purchase cost guarantees a profit:",
                "No; the asset can remain below cost or deteriorate further",
                "Yes after any second purchase",
                "Only when purchases are scheduled",
                "A lower average cost reduces the break-even threshold, but does not guarantee a profit; if the market price remains depressed or the business fails, the investor still incurs a loss.",
            ),
            (
                "Scheduled purchases funded from new monthly income differ from:",
                "Deliberately delaying investment of an already available lump sum",
                "Any purchase involving shares",
                "A transaction with a recorded date",
                "Investing new salary cash flows as they arrive is natural ongoing savings; by contrast, deliberately staging an already existing lump sum over time incurs the opportunity cost of holding idle cash during market advances.",
            ),
        ],
        [BOOK, ALLOCATION],
    )
    # ------------------------------------------------------------------ 11.13
    add(
        "Read the business before trusting the headline number",
        "Security analysis for the lay investor",
        "Identify the accounting questions to answer before beginning detailed security analysis.",
        "A critical milestone in the development of an intelligent investor is learning to read financial statements with healthy professional skepticism. Corporate executives face intense pressure to meet quarterly Wall Street consensus estimates, and financial media frequently amplify flattering press releases that highlight non-GAAP 'Adjusted EBITDA' or headline Net Income. These summary headline numbers often obscure operational deterioration, aggressive accounting choices, and unsustainable one-off windfalls.\n\nTo evaluate the true economic earning power of an enterprise, an investor must construct a rigorous analytical bridge from reported accounting net income to **normalized recurring owner earnings**:\n1. Strip out non-recurring gains: Extraordinary one-time asset sales (e.g. selling a corporate building or patent settlement) boost reported net income for a single quarter, but do not recur. Including them in earnings multiples creates an illusion of cheapness.\n2. Normalize recurring operational costs: Management frequently labels recurring expenses (such as ongoing restructuring, litigation charges, or asset write-downs) as 'extraordinary' and adds them back to Adjusted EBITDA. If an expense occurs every two years, it is an ordinary operational cost of doing business.\n3. Audit the Accrual Gap: Check the relationship between reported Net Income and Cash Flow from Operations (CFO). If reported net income is growing while operating cash flow is stagnating or negative, the company is accumulating unpaid receivables or unmarketable inventory (the classic accrual anomaly documented by Sloan 1996).\n4. Account for Dilution: Check the fully diluted share count. Heavy issuance of stock-based compensation (SBC) dilutes existing shareholders' ownership claim even if reported headline net income increases.",
        "Consider a corporation with N = 20 million common shares outstanding, currently trading at a market price of P = $60 per share:\n• Reported Results: The company issues an enthusiastic press release reporting Net Income of $120 million, producing a headline Earnings Per Share (EPS) of:\n  $$\\mathrm{Reported\\ EPS} = \\frac{\\$120\\text{ million}}{20\\text{ million shares}} = \\$6.00$$\n• Headline Valuation Multiple: At $60 per share, the stock appears extraordinarily cheap, trading at a headline P/E ratio of:\n  $$\\mathrm{Headline\\ P/E} = \\frac{\\$60}{\\$6.00} = 10.0\\times$$\n\nHowever, a forensic examination of the footnotes in the 10-Q filing reveals that reported profit includes a $40 million pre-tax non-recurring gain from the sale of an idle factory. Let us compute true recurring operational net income and recurring EPS:\n$$\\mathrm{Recurring\\ Net\\ Income} = \\$120\\text{ million} - \\$40\\text{ million} = \\$80\\text{ million}$$\n$$\\mathrm{Recurring\\ EPS} = \\frac{\\$80\\text{ million}}{20\\text{ million shares}} = \\$4.00$$\n\nNow, let us recalculate the true valuation multiple based on recurring earning power:\n$$\\mathrm{Recurring\\ P/E} = \\frac{\\$60}{\\$4.00} = 15.0\\times$$\n\nNotice the dramatic change: the true valuation multiple is not 10.0×, but 15.0×—a 50% premium! An investor who relied on the headline summary bought an average business at a normal multiple while believing they had discovered an undervalued bargain.",
        "In your My notebook page, formulate a Financial Disclosure Forensics Checklist:\n1. Reconcile Non-GAAP Adjustments: Examine management's bridge from GAAP Net Income to Adjusted EBITDA. For every add-back, ask: 'Did this company incur a similar expense within the past three years?' If so, treat it as a recurring operational cost.\n2. The Cash Flow Quality Check: Require Cash Flow from Operations (CFO) to equal or exceed GAAP Net Income over a rolling 3-year period: $\\sum \\mathrm{CFO} \\ge \\sum \\mathrm{Net\\ Income}$. Severe negative divergences warrant immediate disqualification.\n3. Prepare Security Analysis Bridge Questions: Compile five essential forensic questions regarding debt maturity schedules, off-balance-sheet leases, pension liabilities, customer concentration, and revenue recognition policies before entering Security Analysis.",
        r"\mathrm{recurring\ EPS} = \frac{\mathrm{reported\ profit} - \mathrm{identified\ nonrecurring\ gain}}{N}",
        'eps = (120 - 40) / 20\nprint("Recurring EPS:", eps)\nprint("Recurring P/E:", 60 / eps)',
        "Reconcile reported vs recurring EPS and P/E for the company with $120 profit, $40 one-time gain, 20 shares, and $60 price. Explain why Cash Flow from Operations must be audited alongside reported net income.",
        "Reported net income of $120 across 20 shares produces headline EPS of $6.00 and a 10.0× P/E. Stripping out the $40 non-recurring gain leaves $80 of recurring profit, yielding recurring EPS of $4.00 and a true recurring P/E of 15.0×. Cash Flow from Operations must be audited alongside net income because accounting rules allow revenue to be recognized before cash is collected; if reported earnings are inflated by uncollected receivables or inventory build-up, operating cash flow will lag, signaling that reported profits do not represent real, distributable cash.",
        [
            (
                "Profit 120 less a one-time gain 40 across twenty shares gives recurring EPS of:",
                "4",
                "6",
                "8",
                "Recurring profit is 120 - 40 = 80; dividing by 20 shares yields recurring EPS of 80 / 20 = 4.",
            ),
            (
                "Price 60 divided by recurring EPS 4 produces P/E of:",
                "15",
                "10",
                "20",
                "The recurring valuation multiple is calculated using normalized earnings: Price / Recurring EPS = 60 / 4 = 15.",
            ),
            (
                "An adjusted earnings measure from management should be:",
                "Reconciled to disclosures and examined for recurring exclusions",
                "Accepted without reading its definition",
                "Assumed to equal cash flow exactly",
                "Management-adjusted earnings measures frequently exclude economically recurring expenses; an investor must audit the reconciliation footnote to identify recurring costs that management labeled non-recurring.",
            ),
            (
                "Before detailed valuation, a careful investor should understand:",
                "The business model, cash needs and senior claims",
                "Only the ticker's popularity",
                "Only the most recent price target",
                "Valuation requires understanding how the enterprise produces revenue, its ongoing capital expenditure requirements, and the contractual claims of senior creditors ranking ahead of common equity.",
            ),
        ],
        [BOOK, FILINGS],
    )

    # ------------------------------------------------------------------ 11.14
    add(
        "Advisers, incentives and investment fraud",
        "Adviser judgment; modern fraud-prevention extension",
        "Check the source, incentives and verifiability of an investment claim.",
        "When seeking financial guidance, an investor must navigate a pervasive **agency conflict**: the person advising you may have financial incentives that diverge sharply from your long-term wealth accumulation. Financial advisers, brokers, and wealth managers are often compensated through front-end commissions, trailer fees (12b-1 fees), and revenue-sharing kickbacks that reward them for steering client capital into expensive, proprietary, or high-churn products.\n\nTo protect yourself, you must distinguish between two legal and regulatory standards of care:\n• Fiduciary Standard: The adviser is legally bound to act solely in your best interest, eliminate or prominently disclose all conflicts of interest, and charge transparent, fee-only compensation.\n• Suitability Standard: A broker is merely required to recommend products that are 'suitable' for your profile at the time of sale, allowing them to legally recommend an inferior, high-fee fund over an identical low-fee fund simply because the former pays them a higher commission.\n\nAt the predatory extreme of the financial spectrum lies outright **investment fraud and Ponzi schemes**. Fraudsters exploit cognitive biases—such as greed, social proof (affinity fraud within religious, professional, or social circles), and fear of missing out—to solicit capital for fictitious investments. Every investor must memorize the non-negotiable warning signs of financial fraud:\n1. Guaranteed high returns with 'zero risk': In economics, return is the compensation for bearing verifiable risk. Any promoter offering guaranteed returns far exceeding prevailing risk-free Treasury yields is running a scam.\n2. Secretive, proprietary 'black box' algorithms: Refusing to provide audited disclosures or clear explanations of how returns are generated.\n3. Pressure to act immediately: Manufacturing artificial urgency to prevent you from conducting independent due diligence.\n4. Custody irregularities: Requesting that investment funds be transferred to an individual's personal bank account, an unregulated offshore entity, or a private crypto wallet rather than an independent, qualified institutional custodian.",
        "Consider a real-world fraudulent pitch: an unlicensed promoter solicits capital for an 'exclusive automated quantitative trading syndicate' promising a guaranteed, fixed return of 3.0% per month with zero downside volatility.\n\nLet us compute the annual compounded return implied by this claim:\n$$r_{\\mathrm{annual,claim}} = (1 + r_{\\mathrm{monthly,claim}})^{12} - 1 = (1 + 0.03)^{12} - 1 = (1.03)^{12} - 1$$\n$$r_{\\mathrm{annual,claim}} \\approx 1.42576 - 1 = 0.42576 \\implies 42.58\\%\\text{ per year}$$\n\nOver a 5-year horizon, $10,000 compounded at 3% monthly would balloon to:\n$$W_5 = 10{,}000 \\times (1.03)^{60} \\approx \\$58{,}916$$\nOver 10 years, it would reach an astonishing $347,109!\n\nNow apply common-sense economic logic: If this promoter possessed an algorithm capable of generating a guaranteed, risk-free 42.58% annual return, why would they solicit money from retail individuals on the internet? Any commercial bank would eagerly lend them millions at 6% or 8% interest, allowing the promoter to capture the entire spread and become a multi-billionaire within a decade. The fact that they are soliciting retail capital proves that the claimed returns are fabricated and the operation is a classic Ponzi scheme, paying early investors with subsequent investors' deposits until the collapse occurs.",
        "In your My notebook page, establish a binding Independent Due Diligence Protocol:\n1. Verify Official Regulatory Registrations: Never invest through any financial adviser, broker, or platform without independently checking their official registration on official regulatory databases: OJK (Indonesia), SEC IAPD / FINRA BrokerCheck (US), or FCA (UK). Never rely on a screenshot or certificate provided by the promoter.\n2. The Independent Custody Mandate: Mandate that all investment funds must be deposited directly with a licensed, regulated third-party qualified custodian or depository institution in your own name. Never transfer funds to an individual, personal bank account, or unregulated platform.\n3. Fiduciary Written Confirmation: Before hiring any financial adviser, demand a signed written statement confirming that they operate as a fiduciary 100% of the time and receive no third-party commissions or kickbacks.",
        r"r_{\mathrm{annual,claim}} = (1 + r_{\mathrm{monthly,claim}})^{12} - 1",
        'print("Annualized promised return:", 1.03 ** 12 - 1)',
        "Calculate the annual compounded return of a promised 3% monthly yield and explain why guaranteed high-return promises are economically absurd. List four essential verification steps before committing capital to any third-party adviser or investment scheme.",
        "A 3% monthly yield compounded over 12 months produces an annual return of (1.03)^12 - 1 = 42.576%, or approximately 42.58%. This is economically absurd because no legitimate counterparty can guarantee risk-free returns exceeding economic growth rates; anyone possessing such a capability would borrow from banks at single-digit rates rather than soliciting retail funds. Four essential verification steps include: (1) verifying registrations directly via official regulatory registries (e.g. OJK, SEC BrokerCheck); (2) requiring independent qualified third-party asset custody; (3) auditing the adviser's commission and conflict compensation structure; and (4) verifying that historical performance claims are backed by audited financial statements.",
        [
            (
                "A fixed 3% monthly compounded promise implies annual return near:",
                "42.58%",
                "3%",
                "36% exactly",
                "Monthly compounding across 12 months is calculated as (1 + 0.03)^12 - 1 = 1.42576 - 1 ≈ 0.42576, or approximately 42.58%.",
            ),
            (
                "A provider's copied registration certificate is sufficient independent verification:",
                "No; check official records through an independently obtained channel",
                "Yes if it contains a logo",
                "Yes if an influencer reposted it",
                "Promoters frequently forge or misappropriate registration certificates; verification requires independently accessing the official registry website of the relevant financial regulator (e.g. SEC, FINRA, OJK).",
            ),
            (
                "Understanding adviser compensation helps identify:",
                "Incentives and potential conflicts in the recommendation",
                "A guarantee that the product will lose",
                "The exact future market return",
                "Knowing how an adviser is compensated (e.g. commissions, sales loads, kickbacks vs. transparent hourly fees) reveals inherent conflicts of interest that may bias their product recommendations.",
            ),
            (
                "A risk disclosure alone establishes a product is legitimate:",
                "No; the entity and claims still require verification",
                "Yes in every jurisdiction",
                "Only when returns are high",
                "Including boilerplate risk warnings does not certify that an investment entity is licensed, that custody is secure, or that the investment strategy is legitimate.",
            ),
        ],
        [FRAUD, FEES],
    )

    # ------------------------------------------------------------------ 11.15
    add(
        "Decision journals, disconfirmation and review rules",
        "Independent judgment and market behavior",
        "Review investments without confusing luck, hindsight and a change in the original thesis.",
        "Human cognition is burdened by systematic memory biases that make objective learning in financial markets difficult. The most prevalent of these is **hindsight bias**: once an outcome is known, people unconsciously rewrite their memories, believing they 'knew it all along' or misremembering their original expectations. When a lucky gamble pays off, hindsight bias convinces the trader they possessed analytical genius; when a well-reasoned trade encounters an unforeseen loss, they retroactively blame themselves for failing to predict the unpredictable.\n\nTo counteract hindsight bias and outcome bias, disciplined investors maintain a **Decision Journal**. A decision journal is a contemporaneous written record executed *at the exact moment of commitment*, capturing:\n1. The Core Thesis: What specific facts, balance-sheet strengths, or valuation discounts justify committing capital?\n2. Probabilistic Scenario Weighting: What are the explicit probabilities and expected outcomes across multiple economic scenarios?\n   $$E[V] = \\sum_k p_k V_k,\\qquad \\sum_k p_k = 1$$\n3. Falsifiable Disconfirming Evidence: What observable, verifiable event or metric would prove the investment thesis wrong?\n4. Pre-Committed Exit Rules: Under what specific conditions will the position be reduced or closed?\n\nCrucially, an investor must separate **thesis invalidation** from **liquidity adjustments**: selling a position because the company's competitive advantage deteriorated is an analytical thesis exit; selling because your household needs cash for medical bills is a balance-sheet liquidity event. Confusing the two prevents you from learning the true lessons of your investment history.",
        "Consider an investor evaluating an enterprise using probabilistic scenario analysis:\n• Initial Assessment (Prior Belief):\n  - Scenario 1 (Successful enterprise expansion): Assessed intrinsic value V_1 = $100 per share, with an estimated probability of p_1 = 60% (0.60).\n  - Scenario 2 (Expansion stumbles under competition): Assessed intrinsic value V_2 = $50 per share, with an estimated probability of p_2 = 40% (0.40).\n\nLet us compute the initial expected value of the business:\n$$E[V]_{\\mathrm{initial}} = (p_1 \\times V_1) + (p_2 \\times V_2) = (0.60 \\times 100) + (0.40 \\times 50) = 60 + 20 = \\$80.00$$\n\nAt a market quotation of P = $70, the investor purchases shares, observing a $10 cushion against expected value ($80). In their decision journal, the investor pre-registers explicit disconfirming criteria: 'If quarterly customer churn exceeds 15% and gross margins drop below 40%, Scenario 2 becomes the dominant reality.'\n\n• Twelve Months Later (New Evidence): Audited quarterly disclosures reveal that customer churn jumped to 18% and gross margins contracted to 38%. Instead of stubbornly defending their pride, the investor performs an objective Bayesian update in their decision journal, revising the scenario probabilities to p_1 = 30% and p_2 = 70%:\n$$E[V]_{\\mathrm{updated}} = (0.30 \\times 100) + (0.70 \\times 50) = 30 + 35 = \\$65.00$$\n\nAt the current price of $70, the expected value has collapsed to $65. The pre-registered exit rule triggers: the investor liquidates the position promptly, avoiding emotional attachment and preserving capital.",
        "In your My notebook page, implement your Personal Decision Journal Protocol:\n1. The Pre-Commitment Template: Before buying any security, complete a one-page journal entry containing: purchase date, market price, conservative/base/optimistic valuation estimates, probabilistic expected value, and the investment horizon.\n2. Pre-Register Disconfirming Evidence: Complete this sentence in advance: 'My thesis will be proven wrong, and I will reduce or exit this position, if [Metric X] drops below [Value Y] or if [Event Z] occurs.'\n3. Scheduled Review Cadence: Review your decision journal on fixed quarterly dates. Update scenario probabilities *only* when audited primary disclosures provide new facts, never in response to price volatility.",
        r"E[V] = \sum_k p_k V_k,\qquad \sum_k p_k = 1",
        'print("Initial scenario-weighted value:", 0.6 * 100 + 0.4 * 50)\nprint("Updated scenario-weighted value:", 0.3 * 100 + 0.7 * 50)',
        "Calculate the initial ($80) and updated ($65) expected values when scenario probabilities shift from (0.6, 0.4) to (0.3, 0.7) for values $100 and $50. Explain why pre-registering disconfirming criteria is essential for combating confirmation bias.",
        "Initial expected value is (0.60 × 100) + (0.40 × 50) = 60 + 20 = $80; when evidence shifts probabilities to 30% and 70%, updated expected value becomes (0.30 × 100) + (0.70 × 50) = 30 + 35 = $65. Pre-registering disconfirming criteria is essential because human psychology is prone to confirmation bias and escalation of commitment; without explicit written criteria established in advance, investors unconsciously ignore negative news, rationalize deteriorating fundamentals, and hold losing positions until total capital destruction occurs.",
        [
            (
                "60% probability of value 100 and 40% of 50 give expected value:",
                "80",
                "75",
                "100",
                "The scenario-weighted expected value is calculated as (0.60 × 100) + (0.40 × 50) = 60 + 20 = 80.",
            ),
            (
                "An expected value of 80 guarantees a realized value of 80:",
                "No; individual outcomes and assumptions remain uncertain",
                "Yes for every investor",
                "Only when price is below 80",
                "Expected value represents the probability-weighted average of possible outcomes; any single realized outcome can be higher or lower depending on which scenario unfolds.",
            ),
            (
                "A useful disconfirming observation should:",
                "Challenge a material assumption of the investment thesis",
                "Only repeat supporting publicity",
                "Depend solely on a preferred price target",
                "Disconfirming evidence is observable, verifiable information (such as lost market share or deteriorating margins) that directly refutes the fundamental premises of the original investment thesis.",
            ),
            (
                "Selling for a near-term cash need versus a failed business thesis should be:",
                "Recorded as distinct reasons",
                "Retrospectively described as the same prediction",
                "Hidden from the decision journal",
                "Distinguishing between balance-sheet liquidity needs and analytical thesis invalidation is critical for accurately auditing your investment decision process and refining future rules.",
            ),
        ],
        [BOOK, FILINGS],
    )

    # ------------------------------------------------------------------ 11.16
    add(
        "Capstone: write your careful-investor policy",
        "Synthesis and preparation for Security Analysis",
        "Assemble a maintainable plan with clear limits, evidence and a review process.",
        "The capstone deliverable of this course is the creation of your own comprehensive, auditable **Investment Policy Statement (IPS)**, codified in your My notebook page. In professional institutional asset management (such as sovereign wealth funds, university endowments, and pension plans), no capital is ever committed without a written Investment Policy Statement. An IPS bridges abstract financial theory and personal financial reality, establishing transparent rules of conduct before market volatility, greed, and panic cloud your judgment.\n\nA complete careful-investor policy synthesizes five operational components, evaluated under the course's **100-Point Capstone Rubric**:\n1. Goals, Horizons & Risk Capacity (25 points): Documenting specific financial goals, time horizons, the Three-Pot liquidity segregation (Emergency Reserve, Dated Commitments, Long-Horizon Capital), and balance-sheet stress tests against forced liquidation.\n2. Asset Allocation, Portfolio Corridors & Cost Audits (25 points): Defining explicit target asset allocation weights (e.g. 60/40), rebalancing tolerance bands (e.g. ±5%), look-through single-company concentration caps (e.g. max 10%), and annual fund fee drag ceilings.\n3. Valuation Discipline, Screening & Margin of Safety (20 points): Formulating conservative vs base vs optimistic valuation procedures, enforcing maximum purchase price ceilings ($P_{\\max} = (1 - m) \\times V_{\\mathrm{cons}}$), and checking senior debt priorities.\n4. Behavioral Guardrails, Decision Journal & Review Rules (20 points): Establishing mandatory cooling-off pauses after price shocks, pre-registering disconfirming exit criteria, maintaining a decision journal, and enforcing independent regulatory fraud checks.\n5. Primary Source Provenance & Document Clarity (10 points): Ensuring all financial figures and company analyses cite verifiable primary disclosures (audited 10-K/10-Q filings, regulatory databases, peer-reviewed studies) rather than secondary commentary.\n\nCompleting this plan marks your graduation as an *investor yang hati-hati*. You will transition seamlessly into the subsequent course, [Security Analysis](/curriculum/security-analysis), equipped with a disciplined personal policy and specific accounting forensic questions.",
        "Let us perform the complete mathematical synthesis for our case household:\n• Balance-Sheet Capital Partitioning:\n  - Total liquid assets: A = 120 million rupiah.\n  - Dated near-term commitments (next 18 months): C_near_term = 30 million rupiah.\n  - Essential emergency reserve: C_reserve = 24 million rupiah.\n  - Isolated long-horizon risk capital:\n    $$C_{\\mathrm{long\\ horizon}} = 120 - 30 - 24 = 66\\text{ million rupiah}$$\n• Conservative Valuation Ceiling:\n  - Conservative intrinsic value estimate: V_cons = $70 per share.\n  - Required policy margin of safety cushion: m = 25% (0.25).\n  - Maximum allowable purchase price:\n    $$P_{\\max} = 70 \\times (1 - 0.25) = 70 \\times 0.75 = \\$52.50$$\n• 100-Point Capstone Rubric Verification:\n  $$\\mathrm{Rubric\\ Total} = 25\\text{ (Goals/Capacity)} + 25\\text{ (Portfolio/Costs)} + 20\\text{ (Valuation)} + 20\\text{ (Behavior)} + 10\\text{ (Clarity)} = 100\\text{ points}$$\n\nNotice how these calculations reconcile the entire journey: from balance-sheet survival and allocation discipline to valuation cushions and behavioral governance. The plan is complete, mathematically verifiable, and ready for operational deployment.",
        "To finalize your capstone and prepare for Security Analysis:\n1. Complete your My notebook page: Populate every section of the careful-investor workbook with either your personal financial parameters or a realistic fictional case study.\n2. Self-Assess Against the Rubric: Grade your completed plan against the 100-point rubric, aiming for a score of at least 80/100 across all five categories.\n3. Formulate Security Analysis Questions: Conclude your workbook with three specific forensic questions regarding corporate accounting, asset recovery haircuts, and debt covenants to investigate in [Security Analysis](/curriculum/security-analysis).",
        r"\mathrm{policy} = \mathrm{goals} + \mathrm{constraints} + \mathrm{allocation} + \mathrm{decision\ rules} + \mathrm{review}",
        'print("Long-horizon capital:", 120 - 30 - 24)\nprint("Case maximum price:", 70 * 0.75)\nprint("Capstone rubric total:", 25 + 25 + 20 + 20 + 10)',
        "Deliver a comprehensive careful-investor policy integrating goals, risk capacity, asset allocation, rebalancing bands, fee limits, conservative margin of safety, decision journal protocol, and fraud checks. Score your plan against the 100-point rubric and outline three questions for Security Analysis.",
        "A complete careful-investor policy isolates 66 million rupiah of long-horizon capital from 120 million total assets (after reserving 30 million for near-term spending and 24 million for reserves), sets a $52.50 maximum purchase price ceiling on a $70 conservative value (25% margin of safety), enforces ±5% rebalancing corridors and fee ceilings, and mandates pre-registered disconfirming criteria in a decision journal. Scoring at least 80/100 on the 100-point rubric verifies readiness for Security Analysis, prompting three essential forensic questions: (1) How do operating cash flows compare to reported net income over five years? (2) What is the liquidation recovery value of inventories and receivables after senior debt? and (3) What debt covenants or maturity cliffs exist in footnotes?",
        [
            (
                "A complete investor policy should connect:",
                "Goals, constraints, allocation, decision rules and review",
                "Only a list of recent winners",
                "Only a target return with no downside",
                "An Investment Policy Statement must systematically integrate concrete goals, balance-sheet constraints, target asset allocations, disciplined execution rules, and scheduled review protocols into a coherent operational framework.",
            ),
            (
                "The plan rubric 25+25+20+20+10 totals:",
                "100 points",
                "90 points",
                "110 points",
                "The five evaluation categories (Goals/Capacity 25, Portfolio/Costs 25, Valuation/Judgment 20, Behavior/Review 20, Sources/Clarity 10) sum to exactly 100 assessment points.",
            ),
            (
                "Passing the concept exam establishes that a personal allocation is suitable:",
                "No; suitability depends on circumstances beyond the educational exam",
                "Yes for every learner",
                "Only if the worksheet used rupiah",
                "Academic exam completion tests conceptual understanding; determining whether a specific financial allocation is suitable requires analyzing individual personal liabilities, tax status, family commitments, and risk capacity.",
            ),
            (
                "Which next course deepens the analysis of earnings, assets and senior claims?",
                "Security Analysis",
                "Only changing a chart theme",
                "A course completion screenshot",
                "The Security Analysis course expands directly upon this policy foundation, providing rigorous forensic methods for evaluating corporate balance sheets, asset recoverability, earnings quality, and capital structure seniority.",
            ),
        ],
        [BOOK, ALLOCATION, FRAUD],
    )

    # ---------------------------------------------------------------- Unit 5
    add(
        "Bonds and cash: what the safe half is actually for",
        "The defensive investor and the bond component",
        "Say what the fixed-income half of a policy is bought for, and recognise when reaching for yield has quietly turned it into a second equity position.",
        "Lesson 11.9 fixed the proportions: Graham's defensive investor holds no less than 25% and no more than 75% in common stocks, with 50/50 as the neutral anchor. This lesson is about the other half, and the question most portfolios never answer explicitly: what is it for?\n\nIt is not there to earn a return. If return were the objective you would hold more equity. The fixed-income and cash half is bought so that an equity drawdown never forces a sale. That is its whole job, and it decides every other property you should want from it: it has to be worth roughly what you paid when you need it, and it has to be worth that at the exact moment equities are worst.\n\nTwo different risks sit inside a bond and they behave completely differently in that moment.\n• Interest-rate risk, measured by duration. Duration is the approximate percentage price change for a one-percentage-point move in yields. A seven-year duration means roughly a 7% price fall for a 1% rise in rates. This risk is symmetric and reverses: hold to maturity and you still receive par.\n• Credit risk, the chance the borrower does not pay. This is not symmetric and does not reverse. A default is permanent, and defaults cluster in exactly the recessions that are also pushing your equities down.\n\nThe trap is reaching for yield. A bond paying two percentage points more than a government issue is not a free two points; it is payment for taking the second risk. If recovery in default is 60 cents on the dollar, that extra 2 points compensates you for about a 5% annual default rate, and you are being paid to accept a loss that arrives on the worst possible day. A high-yield allocation held as the safe half is not a safe half. It is a second equity position wearing a bond's label, and it will fall with your shares rather than funding them.\n\nThis course stops at policy. The arithmetic of judging an individual issuer's ability to pay — coverage of fixed charges, trough-year stress, the maturity funding gap — is the opening work of Security Analysis; see lesson 1.2 rather than repeating it here.",
        "Compare two candidates for the safe half of a plan, both quoted at par.\n\nCandidate A: a government issue with a duration of 7 and a yield of 4.0%.\nCandidate B: a corporate issue with the same duration and a yield of 6.0%.\n\nFirst, what the shared duration costs. If yields rise by one percentage point, the first-order estimate is a price change of −duration × Δy = −7 × 0.01 = −7%. For a two-point rise the straight-line estimate is −14%. Convexity softens this: at a convexity of 55 the second-order estimate is −7 × 0.02 + 0.5 × 55 × 0.02² = −12.9%. Both candidates suffer this equally, and both recover it by holding to maturity.\n\nNow what the extra 2 points is paying for. Write the break-even: with recovery R = 60% of face, an annual default rate d costs you d × (1 − R) of principal each year. Setting that equal to the spread gives d = 2.0 / (1 − 0.60) = 5.0%. So Candidate B is fair only if you believe the issuer's annual default probability is below 5%. That is a credit judgement, not a yield pickup, and you have to make it.\n\nThe decisive question is not which yields more. It is which one you can sell at close to par in the quarter your equities are down 30%. Candidate A's loss in that quarter is an interest-rate loss you can wait out, or a gain if rates have fallen. Candidate B's loss is a credit loss arriving precisely when the issuer's own prospects have worsened, and it does not wait out.",
        "Write the purpose of your fixed-income allocation down before you choose any instrument for it:\n1. State the job in one sentence. For example: 'this half exists so that a 40% equity decline never forces me to sell shares in the following 36 months.' If you cannot write a sentence like that, you are holding bonds for a reason you have not examined.\n2. Size it against the job, not against a yield target. How many months of planned spending, or how much of a drawdown, must it cover? That number sets the amount; the yield does not.\n3. Separate the two risks in writing. For every holding, record its duration and whether it carries credit risk. Add the durations weighted by value; that is the portfolio's rate sensitivity.\n4. Price any yield pickup as a default rate. Divide the spread over the government issue by one minus your recovery assumption. If the implied default rate looks acceptable, say why in a sentence. If you cannot, the pickup is not yours to take.\n5. Re-read it after a joint drawdown. Lesson 11.9 warned that stocks and bonds can fall together in an inflation shock. A safe half that fell with your equities did not do its job, whatever its yield was.",
        r"\Delta P \approx -D\,\Delta y + \tfrac{1}{2} C\,(\Delta y)^2,\qquad d_{\text{break-even}} = \frac{s}{1 - R}",
        'duration = 7.0\nconvexity = 55.0\nshift = 0.02\nfirst = -duration * shift\nsecond = first + 0.5 * convexity * shift * shift\nprint("Straight-line price change percent:", round(first * 100, 1))\nprint("With convexity, percent:", round(second * 100, 2))\n\nspread = 2.0\nrecovery = 0.60\nprint("Break-even annual default rate percent:", round(spread / (1 - recovery), 2))\nprint("Loss given default, cents on the dollar:", round((1 - recovery) * 100, 0))',
        "For the two candidates above, compute the price change on a two-point rise in yields using both the straight-line and the convexity-adjusted estimates, and compute the annual default rate at which the 2-point spread is fair at 60% recovery. Then write, in one sentence, the job your own fixed-income allocation is meant to do, and say whether Candidate B could do it.",
        "The straight-line estimate is −7 × 0.02 = −14.0%; adding the convexity term gives −7 × 0.02 + 0.5 × 55 × 0.0004 = −12.9%, so the linear figure overstates the loss by about 1.1 points. Both candidates share this, and both recover it at maturity. The spread break-even is 2.0 / (1 − 0.60) = 5.0% a year: Candidate B pays you to accept default losses up to that rate. The job of the safe half is to let an equity drawdown pass without forcing a sale, and Candidate B is poorly suited to it, because its loss is a permanent credit loss that arrives in the same recession that is pushing equities down, rather than a recoverable rate loss you can hold through. Judging whether this particular issuer's default probability is under 5% is the work of Security Analysis lesson 1.2, not a yield comparison.",
        [
            (
                "A bond with a duration of 7 faces a two-percentage-point rise in yields. The straight-line price estimate is:",
                "About a 14% fall, before any convexity adjustment",
                "About a 7% fall, because duration is quoted per year",
                "No change, because the bond repays par at maturity",
                "Duration is the approximate percentage price change per one-point move, so a two-point move gives −7 × 2 = −14%. Convexity then softens it to about −12.9%. Repayment at par is why the loss is recoverable, not why it is absent.",
            ),
            (
                "A corporate bond yields two points more than a government bond of the same duration. At 60% recovery, that spread is fair if the annual default rate is below:",
                "5%",
                "2%",
                "40%",
                "Each default costs 1 − 0.60 = 40 cents of principal, so a default rate d costs 0.40d a year. Setting 0.40d = 2.0 gives d = 5.0%. The spread is payment for a judgement you still have to make.",
            ),
            (
                "Why is credit risk a worse fit for the safe half than interest-rate risk?",
                "A default is permanent and clusters in the recessions that are also hurting equities",
                "Credit risk is larger in every scenario",
                "Interest-rate risk does not affect bond prices",
                "Rate losses reverse: hold to maturity and par is still paid. Default losses do not, and they arrive exactly when the equity side needs the safe half to be whole.",
            ),
            (
                "What should decide the size of the fixed-income allocation?",
                "The drawdown or spending it has to cover without forcing an equity sale",
                "The yield available on the instruments being considered",
                "The proportion that produced the best returns last decade",
                "The allocation exists to stop a forced sale, so the size follows from what it must absorb. Sizing it by yield chooses the amount for a reason unrelated to the job.",
            ),
        ],
        [BOOK, ALLOCATION],
    )
    add(
        "A selection rule is a hypothesis, not a verdict",
        "Stock selection for the defensive investor",
        "Apply Graham's combined price filter honestly, and state what passing or failing it does and does not establish.",
        "Graham gave the defensive investor a short list of tests for a common stock, set out in chapter 14 of the 1973 fourth revised edition: adequate size, a strong financial condition, a record of earnings and of dividends over many years, some earnings growth, and a moderate price against both earnings and assets. The last two are the arithmetic ones, and he set them as a price-to-earnings ratio under about 15 and a price-to-book ratio under about 1.5.\n\nOne detail of the earnings test is usually dropped in summaries and matters here. Graham applied the 15 limit twice: once to the last twelve months of earnings and once to the average of the past three years, and wanted both below it. The second check exists precisely so that a single unusual year cannot carry a share through the filter, which is the same concern lesson 11.13 raised about non-recurring items.\n\nHe then made the pair tradeable against each other. The two limits multiply to 15 × 1.5 = 22.5, and he offered that product as a rule of thumb: a share at 9 times earnings and 2.5 times book has a product of 22.5 and passes, as does one at 18 times earnings and 1.25 times book. The product is the test, not either number alone.\n\nTwo cautions belong with it. First, the closed form sometimes sold as 'the Graham number', the square root of 22.5 × EPS × book value per share, is a later derivation from these limits rather than a formula Graham put forward; treat it as arithmetic someone else arranged, not as his recommendation. Second, and much more important, a screen is a hypothesis generator. Passing the filter says the price is modest relative to two accounting numbers. It says nothing about whether those numbers are durable, whether the book value is real, or whether the business is shrinking fast enough to make a low multiple generous rather than cheap.\n\nThis is the course's recurring point in a new place. A rule that returns a list has not done the analysis; it has told you where to start. The work of deciding whether reported earnings recur and whether assets are worth their carrying value is Security Analysis — see lessons 1.6 and 11.13 on reading the business behind the headline number — and no filter substitutes for it.",
        "Meridian Works trades at 42.00. Its trailing earnings are 3.20 a share, its three-year average earnings are also 3.20, and its book value is 24.00 a share. Both earnings figures must clear the 15 limit, and here they are the same number, so one calculation serves for both.\n\nWork the filter:\n• Price to earnings: 42.00 / 3.20 = 13.12, which is under 15 and passes on its own.\n• Price to book: 42.00 / 24.00 = 1.75, which is above 1.5 and fails on its own.\n• The product: 13.12 × 1.75 = 22.97.\n\nThe product is above 22.5, so Meridian fails the combined test — but only just, and the single-ratio readings would have given you two opposite answers. This is exactly why the product exists: a low enough multiple of earnings is allowed to buy back some excess over book.\n\nWhat price would pass? The product rule says P² / (EPS × BVPS) ≤ 22.5, so the ceiling is the square root of 22.5 × 3.20 × 24.00, which is 41.57. At 41.50 the product is 22.43 and it passes; at 42.00 it does not. The whole disagreement is 43 cents, about 1% of the price.\n\nThat margin should tell you what the filter is worth. A 1% price move flips the verdict, and so would a small revision to either accounting input — one impairment to book value, or one quarter of earnings that turns out not to recur. Lesson 11.13 asked you to separate recurring from reported earnings before using any multiple. If Meridian's 3.20 includes a one-time gain of 0.40 a share averaged across the three years — 1.20 in the single year it arose — the recurring figure is 2.80, the recurring P/E is 15.0, and the product becomes 26.25: a clear failure that the headline numbers hid. This is exactly what Graham's second earnings check is for, and why it is worth restoring when a summary has dropped it.",
        "Use the filter as the first step of a process that does not end there:\n1. Compute the product, not the ratios. Record P/E, P/B and their product. A pass or fail on one ratio alone is not the test.\n2. Record the margin. Write how far the product sits from 22.5 in percentage terms. A name that passes by 1% has not told you much; one that passes at 12 has told you more.\n3. Re-run it on recurring earnings. Strip the non-recurring items identified in lesson 11.13 and compute the product again. Record both results side by side; the gap between them is the quality of the screen's input.\n4. Treat the output as a reading list. Everything that survives is a candidate for analysis, not a purchase. Write the three questions you would need answered before buying, before you look at the price again.\n5. Keep the names that failed. A list of rejects with the reason recorded is how you later discover the filter was wrong, which a list of only your purchases can never show.",
        r"\frac{P}{E}\times\frac{P}{B}\le 22.5 \iff P \le \sqrt{22.5\,\times\,\mathrm{EPS}\times\mathrm{BVPS}}",
        'price = 42.00\neps = 3.20\nbvps = 24.00\npe = price / eps\npb = price / bvps\nprint("Price to earnings:", round(pe, 2))\nprint("Price to book:", round(pb, 2))\nprint("Product:", round(pe * pb, 2))\nprint("Passes the 22.5 rule:", pe * pb <= 22.5)\n\nceiling = (22.5 * eps * bvps) ** 0.5\nprint("Highest passing price:", round(ceiling, 2))\nprint("Distance from the quote:", round(price - ceiling, 2))\n\nrecurring = 2.80\nprint("Recurring price to earnings:", round(price / recurring, 2))\nprint("Recurring product:", round((price / recurring) * pb, 2))',
        "Compute Meridian's two ratios, their product, and the highest price that would pass the combined rule. Then recompute the product on recurring earnings of 2.80 and state, in two sentences, what the filter has and has not established about the company.",
        "At 42.00 the ratios are 13.12 and 1.75, whose product is 22.97, so Meridian fails the combined rule despite passing on earnings alone. The highest passing price is the square root of 22.5 × 3.20 × 24.00 = 41.57, so the verdict turns on 43 cents, about 1% of the quote. On recurring earnings of 2.80 the multiple rises to 15.00 and the product to 26.25, a clear failure that the reported figure concealed. The filter has established that the price is not modest against these two accounting numbers once the one-time gain is removed. It has established nothing about whether the remaining earnings are durable, whether the 24.00 of book value would survive an impairment review, or whether the business is contracting; those are questions for analysis, and a screen that returns a name has only told you where to begin.",
        [
            (
                "A share trades at 9 times earnings and 2.5 times book. Under Graham's combined rule it:",
                "Passes, because 9 × 2.5 = 22.5 is within the limit",
                "Fails, because the price-to-book ratio is above 1.5",
                "Fails, because both ratios must pass separately",
                "The two limits multiply to 22.5 and Graham offered the product as a rule of thumb that lets a low earnings multiple buy back some excess over book. Judging each ratio alone defeats the trade-off the product exists to permit.",
            ),
            (
                "Meridian passes on P/E and fails on P/B, with a product of 22.97 against a ceiling of 22.5. What does that margin suggest?",
                "That the verdict is fragile: about 1% on the price, or one revision to either input, reverses it",
                "That the company is a clear buy once the price falls one cent",
                "That the product rule should be abandoned for this name",
                "The passing price is 41.57 against a quote of 42.00, so 43 cents decides it. A result that thin is a reason to look at the quality of the inputs, not to act on the output.",
            ),
            (
                "Removing a one-time gain of 0.40 moves earnings from 3.20 to 2.80. The product then becomes:",
                "26.25, a clear failure the reported figure had hidden",
                "22.97, unchanged, because book value did not move",
                "19.69, a pass, because lower earnings reduce the ratio",
                "The multiple rises to 42.00 / 2.80 = 15.00 and the product to 15.00 × 1.75 = 26.25. A lower earnings figure raises a price-to-earnings ratio, which is why lesson 11.13 insists on stripping non-recurring items before any multiple is used.",
            ),
            (
                "What does passing the defensive price filter establish?",
                "Only that the price is modest against two accounting numbers, which still have to be checked",
                "That the shares offer a margin of safety",
                "That the business has durable earnings",
                "A screen is a hypothesis generator. Durability of earnings, the realism of book value and the direction of the business are questions the filter cannot reach, and they are the ones that decide whether a low multiple is cheap or deserved.",
            ),
        ],
        [BOOK, FILINGS],
    )
    add(
        "Where bargains come from, and the arithmetic of looking for them",
        "The enterprising investor and bargain issues",
        "Name the conditions that let a mispricing persist, and compute honestly what a search for one costs in hours per find.",
        "Lesson 11.3 drew the line between the defensive and enterprising investor as a commitment of time and effort rather than a tolerance for risk. This lesson asks the question that commitment implies: if a security really is mispriced, why has nobody else taken it?\n\nA mispricing that survives needs a reason to survive. Graham's bargain issues were not simply cheap; they were cheap for a structural reason that kept better-resourced buyers away. Three such reasons recur:\n• Neglect. The company is too small, too illiquid, or too obscure for an institution to buy a meaningful position without moving the price. The constraint is the buyer's size, not the analyst's insight.\n• Forced selling. An index deletion, a fund liquidation, a covenant breach or a spin-off distributes shares to holders who must sell for reasons unrelated to value. The seller's deadline, not their opinion, sets the price.\n• Complexity or ugliness. A holding company, a litigation overhang, a restatement, a business that is embarrassing to own. The work to understand it is real, and most people will not do it.\n\nNotice what is absent from that list: 'the market has not noticed'. A thesis whose only support is that a widely-followed, liquid share is obviously too cheap has no mechanism, and a mispricing without a mechanism is usually an error in your own analysis. Requiring yourself to name the reason is the cheapest filter you will ever apply.\n\nThe second half of this lesson is arithmetic, and it is unwelcome. Enterprising investing is a search with a base rate, and the base rate decides whether the search is worth running at all. Most people who choose the enterprising route never compute it.",
        "Suppose you screen 200 companies a year and judge, generously, that 6% of them are genuinely mispriced. That is 12 real opportunities inside the list — but you do not know which 12, and you cannot analyse 200 companies properly.\n\nSay a serious analysis takes 8 hours: reading several years of filings, checking the balance sheet, understanding the business, and writing the thesis down. At that rate you can study perhaps 20 names a year alongside other work.\n\nNow the expected finds. If the 20 you choose are no better than random draws from the list, the expected number of real opportunities among them is 20 × 0.06 = 1.2. The hours are 20 × 8 = 160. That is roughly 133 hours per genuine find, before you have decided whether the one you found is large enough to matter to your portfolio, and before considering that you may be wrong about which of the 20 was the real one.\n\nThis is not an argument against the enterprising route. It is the honest budget for it, and it clarifies two things. First, the only lever with real leverage is the quality of the screen: raising the hit rate from 6% to 12% halves the hours per find, where working faster does not. Second, if 160 hours a year is not available to you, the arithmetic has answered the question lesson 11.3 posed, and the defensive route is the correct choice rather than the lesser one. Sharpe's arithmetic of active management, cited in 11.3, says the average active dollar must underperform after costs; your own time is one of those costs, and this is how you price it.",
        "Before committing to the enterprising route, write the budget down:\n1. Name the mechanism for every candidate. In one sentence: why is this cheap, and what stops a larger buyer from taking it? If the sentence is 'the market has not noticed', discard the candidate.\n2. Record your screen's hit rate. Of the names you studied last year, how many turned out to be genuinely mispriced rather than cheap for cause? That ratio is the only input you can improve.\n3. Compute hours per find. Multiply names studied by hours each, then divide by names studied times the hit rate. Write the number in your notebook as a plain figure.\n4. Compare it against the defensive alternative. The comparison is not 'enterprising returns versus defensive returns'. It is the excess return you expect, after costs, against the hours it consumes and the risk you were wrong.\n5. Review the rejects annually. Of the names you passed over, how many would have worked? A hit rate computed only from the ones you bought is not a hit rate.",
        r"\text{hours per find} = \frac{n \times h}{n \times p} = \frac{h}{p}",
        'screened = 200\nhit_rate = 0.06\nstudied = 20\nhours_each = 8\n\nprint("Real opportunities in the screen:", int(screened * hit_rate))\nprint("Expected real finds among those studied:", round(studied * hit_rate, 1))\nprint("Hours spent:", studied * hours_each)\nprint("Hours per genuine find:", round(hours_each / hit_rate, 0))\n\nbetter = 0.12\nprint("At a 12 percent hit rate, hours per find:", round(hours_each / better, 0))\nprint("Hours saved by doubling the hit rate:", round(hours_each / hit_rate - hours_each / better, 0))',
        "Compute the expected number of genuine finds and the hours per find for a search of 20 names a year at 8 hours each and a 6% hit rate. Then recompute at a 12% hit rate, and write which of the two levers — a better screen or more hours — changes the answer, and why.",
        "Twenty names at a 6% hit rate give an expected 1.2 genuine finds for 160 hours, which is 8 / 0.06 = 133 hours per find. Doubling the hit rate to 12% halves it to 67 hours per find, saving 67 hours for each one. The arithmetic shows that the hours-per-find figure depends only on the hours each analysis takes divided by the hit rate, so the number of names studied cancels out entirely: studying more names finds more opportunities but does not make any one of them cheaper to find. The only lever with leverage is the screen's quality, because it is the denominator. This is also why the mechanism question matters so much — requiring a named reason why a mispricing persists is the cheapest available way to raise the hit rate, and it costs one sentence per candidate rather than eight hours.",
        [
            (
                "Which of these is a reason a mispricing can persist?",
                "The company is too small for an institution to buy without moving the price",
                "The market has not yet noticed a widely-followed, liquid share",
                "The share price has fallen a long way from its high",
                "A surviving mispricing needs a mechanism keeping better-resourced buyers away: size, forced selling, or genuine complexity. A liquid, widely-followed name that is simply unnoticed usually means the error is in your own analysis.",
            ),
            (
                "You study 20 names a year at 8 hours each with a 6% hit rate. The hours per genuine find are:",
                "About 133, because the figure is hours each divided by the hit rate",
                "160, the total hours spent",
                "8, the hours one analysis takes",
                "Expected finds are 20 × 0.06 = 1.2 and hours are 160, so 160 / 1.2 ≈ 133. Algebraically the name count cancels: the figure is 8 / 0.06, which is why studying more names does not lower it.",
            ),
            (
                "Doubling the screen's hit rate from 6% to 12% does what to the hours per find?",
                "Halves them, from about 133 to about 67",
                "Leaves them unchanged, since the hours per analysis are the same",
                "Doubles them, because more candidates must be studied",
                "The figure is hours each over the hit rate, so the hit rate is the denominator. Improving the screen is the only lever with leverage; working faster reduces the numerator but not the structure of the problem.",
            ),
            (
                "What does this arithmetic imply for an investor without 160 hours a year?",
                "That the defensive route is the correct choice, not the lesser one",
                "That they should study fewer names at the same hit rate",
                "That they should raise their hit rate by lowering their standards",
                "Lesson 11.3 framed the choice as a commitment of time. Pricing that commitment honestly is how the choice gets made, and a defensive process chosen for a reason is better than an enterprising one that is not actually resourced.",
            ),
        ],
        [BOOK, FEES],
    )
    add(
        "What a shareholder is owed: dividends, buybacks and management",
        "Shareholders and managements, and dividend policy",
        "Evaluate a distribution decision as an owner, and compute who gains and who loses when a company repurchases shares at a given price.",
        "Graham's complaint about shareholders was that they behaved like ticket-holders rather than owners: passive about management quality, indifferent to how retained earnings were used, and attentive only to the quoted price. A share is a claim on a business, and the most consequential decision that business makes on your behalf is what to do with the cash it earns.\n\nThere are four things a company can do with a dollar of earnings, and they are not equivalent:\n• Reinvest it in the business, which is right only if the business earns more on that dollar than you could elsewhere.\n• Pay down debt, which transfers value from equity holders to creditors unless the leverage was genuinely threatening.\n• Pay it out as a dividend, which hands you the dollar and lets you decide.\n• Repurchase shares, which is the subtle one, because whether it helps you depends entirely on the price paid.\n\nA buyback is a purchase of your own company made with your money. Like any purchase it creates value if the price is below what the asset is worth and destroys value if it is above. This is the part that announcements never say. A repurchase at a discount to intrinsic value transfers wealth from the selling shareholders to those who remain; a repurchase above intrinsic value transfers it the other way, from the holders who stay to the ones who leave. Management is on both sides of that trade and is usually buying when the price is high, because that is when cash is plentiful and confidence is greatest.\n\nThe per-share arithmetic is why this is so easy to hide. A buyback mechanically raises earnings per share by shrinking the denominator, whatever price was paid. An EPS that rose because shares were retired is not the same event as an EPS that rose because the business earned more, and a management rewarded on EPS has a reason not to distinguish them. Lesson 11.14 asked you to read incentives; this is where that reading pays.",
        "Harrow Industries has 1,000 shares outstanding. Your own appraisal, done before you looked at the quote, puts the business at 20.00 a share, so 20,000 in total. The shares trade at 26.00. Management announces a 5,200 repurchase and the press release calls it a vote of confidence.\n\nWork out what it does to you as a holder who is not selling.\n• Shares bought: 5,200 / 26.00 = 200 shares.\n• Shares remaining: 1,000 − 200 = 800.\n• Intrinsic value before: 1,000 × 20.00 = 20,000.\n• Intrinsic value after: 20,000 − 5,200 = 14,800, because 5,200 of cash left the business.\n• Value per remaining share: 14,800 / 800 = 18.50.\n\nYou began holding something worth 20.00 a share and now hold something worth 18.50. The company spent 5,200 to buy 200 shares worth 4,000, and the 1,200 difference came out of the holders who stayed and went to the holders who sold. Per remaining share that is a transfer of 1.50.\n\nMeanwhile the reported figures improve. If Harrow earns 2,000 a year, earnings per share rise from 2.00 to 2,000 / 800 = 2.50, a 25% increase, with no change whatever in the business. A dividend of 5,200, by contrast, would have handed each holder 5.20 a share and left the per-share value of what remains at 14,800 / 1,000 = 14.80 — the same total of 20.00 between cash in hand and shares held, with nothing transferred between holders.\n\nThe test, then, is not whether a buyback happened. It is the price it happened at, measured against an appraisal you made first.",
        "Judge distributions as an owner, with the appraisal written down before the announcement:\n1. Appraise first, then read the announcement. A value estimate formed after reading a press release is not independent of it. Lesson 11.15 on decision journals applies directly: write the number and the date.\n2. For a buyback, compute the transfer. Subtract the cash spent from your appraisal of the whole business, divide by the shares that remain, and compare with your appraisal per share before. Record the difference as a figure, positive or negative.\n3. Separate mechanical EPS from earned EPS. Ask what earnings per share would have been with the old share count. If the entire improvement came from the denominator, say so in your notes.\n4. Read the incentive. Check whether management's compensation references earnings per share, total shareholder return or a share-price target, and whether the repurchase was funded by debt. Both change how you should read the decision.\n5. Record what you would have preferred and why. Over several years this becomes evidence about the management's capital allocation, which is a more reliable signal than any single year's result.",
        r"V_{\text{after}} = \frac{V - C}{N - C/P},\qquad \text{transfer per share} = V_{\text{per share}} - V_{\text{after}}",
        'shares = 1000\nvalue_per_share = 20.00\nprice = 26.00\nspend = 5200.0\n\nbought = spend / price\nremaining = shares - bought\nbefore = shares * value_per_share\nafter = before - spend\nprint("Shares repurchased:", round(bought, 0))\nprint("Shares remaining:", round(remaining, 0))\nprint("Business value before:", round(before, 0))\nprint("Business value after:", round(after, 0))\nprint("Value per remaining share:", round(after / remaining, 2))\nprint("Transferred away per remaining share:", round(value_per_share - after / remaining, 2))\n\nearnings = 2000.0\nprint("Earnings per share before:", round(earnings / shares, 2))\nprint("Earnings per share after:", round(earnings / remaining, 2))\nprint("Percent rise from the share count alone:", round((shares / remaining - 1) * 100, 1))',
        "Compute the value per remaining share after Harrow's repurchase, the transfer per share, and the rise in earnings per share it produces. Then state the price at which the buyback would have been neutral for holders who stay, and explain why the announcement's framing as a vote of confidence is not evidence either way.",
        "The company buys 5,200 / 26.00 = 200 shares, leaving 800. Business value falls from 20,000 to 14,800 because the cash left, so value per remaining share is 14,800 / 800 = 18.50 against 20.00 before — a transfer of 1.50 a share away from the holders who stayed and to those who sold. Earnings per share rise from 2.00 to 2.50, a 25% increase produced entirely by the smaller denominator with no change in the business. The buyback is neutral only at a price equal to intrinsic value, 20.00 a share: below that it adds value for continuing holders, above it subtracts. The vote-of-confidence framing is not evidence because it is an assertion about management's opinion of the price, and management's opinion is precisely what the repurchase price is being used to test; a confident management buying at 26.00 against a 20.00 value has expressed confidence and destroyed 1,200 of value in the same act.",
        [
            (
                "A company worth 20.00 a share repurchases stock at 26.00. For a holder who does not sell, this:",
                "Transfers value away from them and towards the holders who sold",
                "Is neutral, because the share count and the cash both fall",
                "Adds value, because fewer shares now share the same earnings",
                "The company paid 26.00 for something worth 20.00. The 6.00 difference on each share bought comes out of the continuing holders; in the worked case that is 1.50 per remaining share.",
            ),
            (
                "After the repurchase, Harrow's earnings per share rise from 2.00 to 2.50. What has happened to the business?",
                "Nothing: the rise is entirely the smaller share count",
                "It has become 25% more profitable",
                "It has earned back the cash it spent",
                "Earnings are unchanged at 2,000; only the denominator moved, from 1,000 shares to 800. Separating a mechanical EPS rise from an earned one is the point, especially where management is paid on EPS.",
            ),
            (
                "At what price would the repurchase have been neutral for continuing holders?",
                "At intrinsic value, 20.00 a share",
                "At the market price, since that is what the shares are worth",
                "At book value, whatever it happens to be",
                "A buyback is a purchase. It creates value below intrinsic value and destroys it above, so the neutral point is intrinsic value itself — which means you need an appraisal made before the announcement to judge it at all.",
            ),
            (
                "A dividend of the same 5,200 would have left each holder with:",
                "5.20 in cash and shares worth 14.80, totalling the 20.00 they started with",
                "Shares worth 18.50, the same as the buyback",
                "More total value, because dividends are always preferable",
                "A dividend distributes the cash without changing the share count, so nothing is transferred between holders: 14,800 / 1,000 = 14.80 a share plus 5.20 received. Neither form is always better; the buyback's merit depends entirely on the price paid.",
            ),
        ],
        [BOOK, FILINGS],
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
        (
            "Choose the securities, and know what a rule cannot decide",
            "The purpose of the safe half, the defensive price filter, where bargains come from, and judging a distribution as an owner.",
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
                "Judge the purpose of a fixed-income allocation, apply a price filter as a hypothesis rather than a verdict, and evaluate a dividend or repurchase as an owner.",
                "Produce an investor-policy workbook and prepare for the deeper Security Analysis course.",
            ],
            "readingGuide": "20 lessons × 30 minutes = 10 hours of planned study across five units; exam time is additional. Includes 40 practice questions, five four-question checkpoints, a 20-question final and a downloadable workbook with a self-assessed capstone in your notebook. This is an original thematic companion, not the full book or a substitute for it. Edition pagination varies; use the named themes in your own copy. Modern planning, fund and fraud examples are explicitly course extensions. Case allocations and thresholds are fictional assumptions, not personalized recommendations.",
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
                    "title": "Download the careful-investor template (Markdown)",
                    "url": "/course-assets/intelligent-investor/investor-plan.md",
                },
                {
                    "title": "Download the book companion reading guide",
                    "url": "/course-assets/intelligent-investor/README.md",
                },
            ],
        },
        checkpoints_for(modules, parts, len(parts)),
    )
    # Bumped when unit 5 took the final from 16 questions to 20, so a draft
    # started against the old paper is told the exam changed.
    track["exams"][-1]["version"] = 2
    return track
