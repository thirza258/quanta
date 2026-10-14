"""Original trading-ethics course: duties, market conduct, and a written charter.

Every scenario, firm, person and amount below is invented. The references are
primary sources for the rule or standard being described; they are not claims
that any named case in this course occurred.
"""

from applied_courses import checkpoints_for, study
from book_courses import finish

CFA_CODE = (
    "CFA Institute · Code of Ethics and Standards of Professional Conduct",
    "https://www.cfainstitute.org/standards/professionals/code-ethics-standards",
)
REG_BI = (
    "U.S. SEC · Regulation Best Interest",
    "https://www.sec.gov/regulation-best-interest",
)
INSIDER = (
    "U.S. SEC · Insider trading: investor publication",
    "https://www.sec.gov/about/reports-publications/investorpubsinsidertradingguidehtm",
)
BEST_EX = (
    "FINRA · Rule 5310, best execution and interpositioning",
    "https://www.finra.org/rules-guidance/rulebooks/finra-rules/5310",
)
QUOTES = (
    "FINRA · Rule 5210, publication of transactions and quotations",
    "https://www.finra.org/rules-guidance/rulebooks/finra-rules/5210",
)
HONOR = (
    "FINRA · Rule 2010, standards of commercial honor and principles of trade",
    "https://www.finra.org/rules-guidance/rulebooks/finra-rules/2010",
)
DECEPTIVE = (
    "FINRA · Rule 2020, use of manipulative, deceptive or other fraudulent devices",
    "https://www.finra.org/rules-guidance/rulebooks/finra-rules/2020",
)
SUPERVISION = (
    "FINRA · Rule 3110, supervision",
    "https://www.finra.org/rules-guidance/rulebooks/finra-rules/3110",
)
ADVERTISING = (
    "FINRA · Advertising regulation and communications with the public",
    "https://www.finra.org/rules-guidance/key-topics/advertising-regulation",
)
WHISTLE = (
    "U.S. SEC · Office of the Whistleblower",
    "https://www.sec.gov/enforcement-litigation/whistleblower-program",
)
GIPS = (
    "CFA Institute · GIPS standards for firms",
    "https://www.gipsstandards.org/standards/gips-standards-for-firms/",
)
MARKET_ABUSE = (
    "ESMA · Market integrity and the Market Abuse Regulation",
    "https://www.esma.europa.eu/esmas-activities/markets-and-infrastructure/market-integrity",
)
PLANS = (
    "U.S. SEC · Insider trading arrangements and related disclosures, December 2022",
    "https://www.sec.gov/newsroom/press-releases/2022-222",
)
MARKET_ACCESS = (
    "U.S. SEC · Risk management controls for brokers or dealers with market access",
    "https://www.sec.gov/files/rules/final/2010/34-63241.pdf",
)
FRAUD = (
    "U.S. SEC · Investor.gov: what you can do to avoid investment fraud",
    "https://www.investor.gov/protect-your-investments/fraud/how-avoid-fraud/what-you-can-do-avoid-investment-fraud",
)
FEES = (
    "U.S. SEC · Investor.gov: understanding investment fees",
    "https://www.investor.gov/introduction-investing/getting-started/understanding-fees",
)
STATEMENTS = (
    "U.S. SEC · Beginners' guide to financial statements",
    "https://www.sec.gov/about/reports-publications/investorpubsbegfinstmtguide",
)

PARTS = [
    (
        "Duty, conflict and disclosure",
        "Whose interest a decision serves, what must be disclosed, and how incentives reach a recommendation.",
    ),
    (
        "Market integrity",
        "Information, quotations, promotion and order handling: the conduct that keeps a price meaningful.",
    ),
    (
        "Conduct in automated and quantitative work",
        "Accountability for a system that trades, honest search and reporting, and the data you are allowed to use.",
    ),
    (
        "Care, refusal and record",
        "Advising another person, refusing an instruction, escalating a concern and writing your own charter.",
    ),
]


def build_trading_ethics():
    modules = []

    def add(
        title,
        theme,
        objective,
        principle,
        case,
        rules,
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
            f"12.{index}",
            (index - 1) // 4 + 1,
            title,
            objective,
            principle,
            case,
            rules
            + "\n\n### Add it to your charter\n\nWrite the rule you will actually follow, the observation that would tell you the rule was broken, and the person you would tell. A rule you cannot check is a preference, not a control. Record the decision and its reasons before the outcome is known; a profitable breach is still a breach, and a loss suffered while following your rules is not evidence that the rules were wrong.",
            formula,
            code,
            task,
            solution,
            rows,
            refs,
        )
        item["minutes"] = 30
        item["reading"] = (
            f"Conduct theme: {theme}. 30-minute session: 10 minutes reading the principle and the named rule, "
            "8 minutes on the calculation, and 12 minutes adding a checkable rule to your trading charter. Every "
            "firm, person, price and amount in the scenarios is invented. The linked rules and standards are real "
            "primary sources, but this course is education, not legal, compliance or investment advice, and the "
            "obligations that bind you depend on your own jurisdiction, licence and role."
        )
        modules.append(item)

    # ---------------------------------------------------------------- Unit 1
    add(
        "Whose interest the decision serves",
        "Duty of loyalty and the order of interests",
        "Identify whose interest a financial decision serves, prioritize client interests above all others, and resolve conflicts of interest systematically.",
        "Every trading decision is executed on behalf of a specific party: yourself, an individual client, an institutional employer, or a fund's pooled investors. Ethics in financial markets starts with identifying who that principal is. In law and professional conduct, an agency relationship exists whenever one person (the agent) agrees to act on behalf of another (the principal). A trade that is completely proper when placed for your own account can become a serious regulatory breach when placed with a client's capital.\n\nA duty of loyalty is the bedrock of the financial profession. It requires placing the principal's financial interest ahead of your personal wealth, and placing the client's interests ahead of your employer's corporate profits whenever they diverge. CFA Institute's Code of Ethics and Standards of Professional Conduct (Standard III.A) requires members to act for the benefit of their clients and place their clients' interests before their employer's or their own personal interests. Similarly, the U.S. Securities and Exchange Commission's Regulation Best Interest (Reg BI) mandates that broker-dealers cannot place their own financial interests ahead of retail customers when making recommendations.\n\nIn daily market practice, ethical failures rarely begin with blatant embezzlement or overt theft. Instead, they arise in quiet, routine operational choices: choosing a mutual fund that pays your brokerage a higher distribution kickback, routing a trade to win a firm commission contest, or adjusting an order to benefit a personal position. Loyalty is not a vague emotional aspiration; it is an explicit hierarchy of interests that you must write down, justify, and audit before executing an order.",
        "Consider a fictional wealth manager deciding between two investment funds for a client with Rp500,000,000 to invest:\n\n• Fund A charges an annual management fee of 0.20% (20 basis points) and pays no commission or referral kickback to the adviser.\n• Fund B charges an annual management fee of 1.20% (120 basis points) and pays the adviser a recurring annual trailer fee of 0.40% (40 basis points) out of the fund's management fee.\n\nStep-by-step arithmetic:\n1. Annual cost of Fund A: 0.002 x Rp500,000,000 = Rp1,000,000.\n2. Annual cost of Fund B: 0.012 x Rp500,000,000 = Rp6,000,000.\n3. Annual cost difference borne by the client: Rp6,000,000 - Rp1,000,000 = Rp5,000,000.\n4. Annual financial benefit paid directly to the adviser from Fund B: 0.004 x Rp500,000,000 = Rp2,000,000.\n\nOver a 10-year holding period without compounding, Fund B costs the client Rp50,000,000 in extra management fees, while generating Rp20,000,000 in personal revenue for the adviser. This arithmetic does not automatically mean Fund B is fraudulent—it might offer unique exposure or active risk management that the client genuinely requires. However, the calculation clearly reveals where the adviser's personal financial interest conflicts with the client's wealth. The client has an absolute right to understand this cost drag and the adviser's incentive before agreeing to the recommendation.",
        "Name the principal before choosing the trade. Write the decision as a complete sentence with an explicit subject: 'I am recommending [Security] for [Principal], whose financial objective is [Objective].' When the interests of two parties collide, document which interest was ranked first and explain the fiduciary rationale.\n\n### Do and do not\n\n- **Do** state the principal and their investment objective in writing before executing or recommending any transaction.\n- **Do** rank competing interests explicitly whenever a conflict arises, and maintain the documentation in your client file.\n- **Do not** assume a recommendation is ethical simply because you can build a clever argument for it; ask whether you would make the exact same recommendation if your compensation were identical either way.\n- **Do not** treat an undisclosed commission or personal benefit as harmless just because the investment performed well or made money for the client.",
        r"\Delta\text{cost} = (f_B - f_A)\times V,\qquad \text{adviser benefit} = r\times V",
        'value = 500_000_000\nprint("Annual cost difference:", (0.012 - 0.002) * value)\nprint("Adviser benefit from the costlier fund:", 0.004 * value)',
        "For the two fictional funds above, calculate the annual cost difference to the client and the adviser's benefit. Then write the one sentence the adviser owes the client before the recommendation is made.",
        "The annual cost difference is Rp5,000,000 and the adviser's annual benefit is Rp2,000,000. Before the recommendation is finalized, the adviser owes the client a clear, plain-language disclosure: 'Fund B charges an annual fee of 1.20% (Rp6,000,000/year on Rp500,000,000), of which my firm receives 0.40% (Rp2,000,000/year) as a trailer fee, whereas a low-cost alternative (Fund A) charges 0.20% (Rp1,000,000/year) with zero compensation to me.' This disclosure allows the client to weigh the recommendation knowing exactly what the adviser stands to gain. Suitability and disclosure are complementary obligations; the arithmetic proves that a material conflict exists and must be disclosed in writing.",
        [
            (
                "A duty of loyalty in this course means:",
                "Placing the principal's interest ahead of your own, in a written order",
                "Never charging a fee for advice",
                "Avoiding every transaction that could lose money",
                "Loyalty is an objective, auditable ranking of interests that places the client first, not a promise that investments will never lose money.",
            ),
            (
                "On 500,000,000 invested, fees of 1.20% versus 0.20% differ annually by:",
                "5,000,000",
                "500,000",
                "10,000,000",
                "The fee difference is 1.00 percentage point (0.012 - 0.002 = 0.010). On Rp500,000,000, that equals 0.01 x 500,000,000 = Rp5,000,000 each year.",
            ),
            (
                "A recommendation pays the adviser more and also suits the client. The conflict:",
                "Still requires disclosure, because the client cannot weigh what they cannot see",
                "Disappears, because the outcome was good for the client",
                "Is resolved by the adviser's confidence in the product",
                "Suitability and conflict disclosure are separate obligations. Even if the product is suitable, the client has a right to know the adviser's financial incentive.",
            ),
            (
                "The most useful first step when two principals' interests conflict is:",
                "Write down which interest you ranked first and the reason",
                "Choose whichever trade is larger",
                "Postpone the decision until prices move",
                "Documenting an explicit, recorded hierarchy of interests creates an auditable record that demonstrates fiduciary compliance before outcomes are known.",
            ),
        ],
        [CFA_CODE, REG_BI, FEES],
    )

    add(
        "Conflicts you must disclose before you act",
        "Disclosure, materiality and timing",
        "Determine what constitutes a material conflict of interest, when it must be disclosed, and how to communicate it clearly to investors.",
        "Disclosure transforms a hidden conflict of interest into an informed decision by the client or counterparty. When an analyst, adviser, or trader has an outside financial stake, three core questions determine compliance: what is the nature of the conflict, is it material, and when must the other party be informed?\n\nMateriality is not an arbitrary mathematical threshold. In securities law and professional standards, the benchmark is the 'Reasonable Person Standard': a fact is material if there is a substantial likelihood that a reasonable investor would attach importance to it when deciding whether to buy, sell, or hold a security. Under CFA Standard VI(A) (Disclosure of Conflicts), professionals must make full and fair disclosure of all matters that could reasonably be expected to impair their independence and objectivity or interfere with respective duties to clients and prospective clients.\n\nTiming and prominence are where disclosures most often break down. A conflict disclosed after an order is executed cannot help the client make an informed choice; the decision has already passed. Similarly, burying a disclosure in microscopic print at the bottom of a 40-page regulatory filing is concealment disguised as compliance. For disclosure to be valid, it must be prominent, delivered in plain language, and presented before or concurrently with the actionable recommendation.",
        "Imagine an equity research analyst who personally owns Rp60,000,000 worth of shares in Pelita Manufaktur. The analyst's total personal investable portfolio across all assets is Rp400,000,000. The analyst is preparing to publish an influential research note upgrading Pelita Manufaktur from 'Neutral' to 'Strong Buy' with a 25% price target increase.\n\nStep-by-step arithmetic:\n1. Analyst's portfolio allocation to this single stock: Rp60,000,000 / Rp400,000,000 = 0.15 = 15.0%.\n2. Potential personal gain: If the stock rises by 25% following the report, the analyst's personal holding gains 0.25 x Rp60,000,000 = Rp15,000,000.\n\nDoes this meet the reasonable-person standard of materiality? Yes. A 15% personal portfolio concentration gives the analyst significant personal financial exposure to the market's reaction. An institutional or retail investor reading the note would want to know that the analyst stands to gain Rp15,000,000 from an upward price move. Disclosing this fact prominently on the front page of the research note ensures readers can discount potential bias; placing it in a delayed quarterly report a week later completely fails the purpose of disclosure.",
        "Disclose material conflicts before the action occurs, within the same document or conversation, and in clear, plain language that an ordinary investor can understand.\n\n### Do and do not\n\n- **Do** apply the reasonable-person test to materiality rather than relying on private, self-serving internal thresholds.\n- **Do** place conflict disclosures prominently right where the investment decision is made, such as the front page of a research note or on the order ticket.\n- **Do not** use voluminous boilerplate text to camouflage a specific personal holding or compensation arrangement.\n- **Do not** disclose a conflict after a trade has been executed and claim that transparency was maintained.",
        r"w = \frac{\text{holding}}{\text{personal portfolio}},\qquad \text{disclose if a reasonable reader would want }w",
        'holding = 60_000_000\nportfolio = 400_000_000\nprint("Share of personal portfolio:", round(holding / portfolio, 4))',
        "Calculate the analyst's portfolio weight, then write the disclosure sentence and state exactly where and when it must appear.",
        "The analyst's portfolio weight is 0.15, or 15.0%. The disclosure sentence must state: 'The authoring research analyst holds 15.0% of their personal investment portfolio (Rp60,000,000) in common shares of Pelita Manufaktur as of the publication date.' This disclosure must appear prominently on the first page of the research report, in bold or boxed text adjacent to the recommendation, before or at the exact moment the report is distributed to clients. A disclosure buried in a subsequent filing or released after trading opens cannot inform a reader who acts on the note.",
        [
            (
                "Materiality for disclosure is best tested by:",
                "Whether a reasonable person would want the fact before deciding",
                "Whether the amount exceeds one million rupiah",
                "Whether the firm's lawyers have previously objected",
                "The reasonable-person standard is the accepted legal and professional benchmark for determining whether an omitted fact is material.",
            ),
            (
                "A holding of 60,000,000 in a personal portfolio of 400,000,000 is:",
                "15%",
                "6.7%",
                "1.5%",
                "Dividing Rp60,000,000 by Rp400,000,000 gives exactly 0.15, which corresponds to 15.0% of the portfolio.",
            ),
            (
                "A conflict disclosed a week after the research note was published:",
                "Failed its purpose, because it could not inform the decision it affected",
                "Satisfies the obligation, since it was eventually disclosed",
                "Is adequate if the note later proved accurate",
                "Disclosures must be delivered before or concurrently with the recommendation so the investor can evaluate potential bias before committing capital.",
            ),
            (
                "Burying a relevant conflict inside lengthy boilerplate is best described as:",
                "A failure of prominence that works against the purpose of disclosing",
                "Acceptable, because the fact was technically published",
                "Required, since legal text belongs in an appendix",
                "Prominence and plain language are essential elements of effective disclosure; burying facts in boilerplate undermines transparency.",
            ),
        ],
        [CFA_CODE, STATEMENTS, ADVERTISING],
    )

    add(
        "Costs, inducements and the incentive behind advice",
        "Compensation arrangements and total cost",
        "Unpack hidden fee structures and inducements, calculate Total Cost of Ownership (TCO), and identify predatory churning.",
        "An inducement is any financial or non-financial benefit that could influence an investment recommendation: upfront sales commissions, trailing revenue shares, platform custody kickbacks, research paid for via directed order flow (soft dollars), sales performance bonuses, or luxury hospitality. There is nothing wrong with being fairly paid for professional advisory work. The ethical and regulatory violation occurs when the investor cannot see the payment arrangement and is therefore unable to assess how that compensation shapes the advice they receive.\n\nFee disclosure is vital because small annual percentage fees compound aggressively over time. An investor who compares only headline management fees misses the true cost of owning an investment. The professional discipline required here is calculating the Total Cost of Ownership (TCO). To find TCO, sum the recurring management charge, the transaction costs created by trading turnover (including brokerage commissions, exchange fees, and bid-ask spread slippage), and any fixed annual platform or custody fees.\n\nConsider the destructive practice of 'churning' (excessive trading). When an adviser or broker is compensated per transaction, they face a perverse incentive to recommend frequent buying and selling. Each transaction generates fresh commission revenue for the broker while steadily eroding the client's principal through execution costs and taxes. Over a 10- or 20-year horizon, an extra 1.0% to 1.5% in unnecessary annual turnover friction can eliminate up to a third of a portfolio's potential compounded wealth.",
        "Consider a fictional client portfolio worth Rp250,000,000. The wealth manager charges an annual management fee of 0.90%, turns the portfolio over 2 times per year with an estimated round-trip trading cost of 0.30% per turn, and passes along an annual platform administration fee of Rp600,000.\n\nStep-by-step arithmetic for Baseline (Turnover = 2):\n1. Annual management fee: 0.009 x Rp250,000,000 = Rp2,250,000.\n2. Annual trading friction (2 turns x 0.30% round trip): 2 x 0.003 x Rp250,000,000 = Rp1,500,000.\n3. Platform custody fee: Rp600,000.\n4. Total annual cost: Rp2,250,000 + Rp1,500,000 + Rp600,000 = Rp4,350,000.\n5. Total cost as a percentage of assets: Rp4,350,000 / Rp250,000,000 = 1.74%.\n\nNow suppose the adviser increases portfolio turnover to 4 times per year under the claim of 'tactical active rebalancing':\n1. Annual management fee remains unchanged at Rp2,250,000.\n2. New trading friction (4 turns x 0.30%): 4 x 0.003 x Rp250,000,000 = Rp3,000,000.\n3. Platform custody fee remains Rp600,000.\n4. New total annual cost: Rp2,250,000 + Rp3,000,000 + Rp600,000 = Rp5,850,000.\n5. New total cost ratio: Rp5,850,000 / Rp250,000,000 = 2.34%.\n\nThe headline management fee did not move by a single basis point, yet the client suffers an additional Rp1,500,000 in annual friction. Unless the adviser can demonstrate with documented evidence that this increased turnover delivers expected alpha exceeding Rp1,500,000, the extra trading is unjustified and breaches fiduciary care.",
        "Quote investment costs in currency terms over defined multi-year holding periods rather than isolated percentages. Separate the structural costs chosen by the investor from the transaction costs generated by your trading recommendations.\n\n### Do and do not\n\n- **Do** calculate and present the Total Cost of Ownership (ongoing management fee, turnover transaction costs, and custody fees) in actual currency.\n- **Do** state explicitly who receives each component of the client's fees, distinguishing independent third-party costs from advisory revenue.\n- **Do not** describe advisory or brokerage services as 'free' or 'zero-commission' when costs are deducted from fund assets or extracted via spread markups.\n- **Do not** increase portfolio turnover without pre-trade documentation proving that expected risk-adjusted net gains exceed the added transaction costs.",
        r"C = f\cdot V + n\cdot c\cdot V + F",
        'value = 250_000_000\nfee = 0.009\nturns = 2\nround_trip = 0.003\nplatform = 600_000\ntotal = fee * value + turns * round_trip * value + platform\nprint("Total annual cost:", total)\nprint("As a share of the portfolio:", round(total / value, 4))',
        "Compute the total annual cost above in money and as a percentage, then recompute it with turnover of four times a year and state what the adviser must be able to show.",
        "At 2 turns per year, total annual cost is Rp4,350,000, which equals 1.74% of the portfolio. When turnover doubles to 4 turns, total annual cost rises to Rp5,850,000, or 2.34% of portfolio value. The adviser must be able to provide clear, documented, pre-trade evidence showing that the expected return from the additional trading exceeds the extra Rp1,500,000 in transaction costs. Justifying turnover after the fact by cherry-picking winning trades is unacceptable; fiduciary care requires ex-ante justification.",
        [
            (
                "Total cost of ownership in this lesson includes:",
                "Ongoing charge, trading costs caused by turnover, and platform fees",
                "Only the headline annual management fee",
                "Only the costs the investor pays by separate invoice",
                "Total Cost of Ownership accounts for all structural fees deducted from assets, platform charges, and trading frictions created by turnover.",
            ),
            (
                "On 250,000,000, a 0.9% charge plus two round trips at 0.3% plus 600,000 totals:",
                "4,350,000",
                "2,850,000",
                "3,750,000",
                "Management fee = Rp2,250,000; trading cost = 2 x 0.003 x 250,000,000 = Rp1,500,000; platform fee = Rp600,000. Sum = Rp4,350,000.",
            ),
            (
                "Doubling turnover while leaving the management fee unchanged:",
                "Raises the investor's total cost even though the headline rate did not move",
                "Has no cost effect, since the fee is what the investor agreed to",
                "Reduces cost by spreading it over more transactions",
                "Every trade incurs commissions, taxes, and spread slippage. Doubling turnover doubles transaction costs regardless of the headline management fee.",
            ),
            (
                "Calling advice 'free' because the fee is deducted from assets is:",
                "Misleading, since the cost is borne by the investor either way",
                "Accurate, because no invoice is issued",
                "Acceptable if the product outperformed",
                "Deducting fees directly from portfolio NAV or client cash is still a direct economic cost paid by the investor and cannot be marketed as free.",
            ),
        ],
        [FEES, REG_BI, CFA_CODE],
    )

    add(
        "Personal trading and client priority",
        "Front-running, allocation and blackout windows",
        "Establish strict trading priority rules that place client orders ahead of firm and personal accounts, eliminating front-running and cherry-picking.",
        "Priority of transactions establishes a clear rule of market conduct: client transactions must always come first, employer transactions second, and personal transactions last. This rule exists because individuals with advance knowledge of pending client orders have the power to exploit that information for personal gain at the direct expense of the client.\n\nFront-running is the classic violation: buying or selling a security in a personal account immediately ahead of a large client order, knowing that the client's order will push the market price in a predictable direction. When the client's order executes, the market price moves, allowing the front-runner to profit by selling into that price move. The client suffers worse execution prices (slippage) because the front-runner captured liquidity ahead of them. A related violation is 'cherry-picking' or post-trade allocation: pooling orders across accounts during the day, observing which fills executed at the best prices, and assigning the profitable fills to personal or favored accounts while allocating the worse fills to retail clients.\n\nEffective organizational controls are structural and verifiable, not based on trust or personal promises. They include mandatory pre-clearance for all employee personal trades, restricted lists prohibiting trading in securities under active research or advisory mandates, blackout windows before and after client orders, and automated pro-rata or volume-weighted average price (VWAP) trade allocation systems.",
        "Consider a fictional institutional trading desk preparing to purchase 400,000 shares of Cendana Logistik for a client portfolio over two consecutive trading days. An equity analyst on the desk enters an order to buy 5,000 shares of Cendana Logistik for their personal brokerage account the afternoon before the client's order begins executing.\n\nStep-by-step analysis:\n1. Client order duration: 2 full business days.\n2. Compliance blackout buffer rule: 2 business days before execution begins, through 2 business days after execution completes.\n3. Total blackout window duration: 2 (pre-order buffer) + 2 (execution days) + 2 (post-order buffer) = 6 business days.\n4. Personal trade restriction: Under this standard policy, personal trading in Cendana Logistik is completely prohibited throughout all 6 business days.\n\nThe analyst might argue: 'My 5,000 shares is tiny compared to the client's 400,000 shares; it didn't move the market.' This argument fails on principle. Front-running is defined by the misuse of confidential, non-public client order information, not by position size. By trading ahead of the client, the analyst stepped in front of client liquidity, created an irreconcilable conflict, and made it impossible for the firm to prove that the client received unaffected best execution.",
        "Enforce the priority sequence (clients first, employer second, personal last) through mandatory operational controls: pre-clearance, blackout windows, and automated average-price allocation.\n\n### Do and do not\n\n- **Do** pre-clear all personal trades with compliance for any security covered by your research desk or firm mandates.\n- **Do** allocate block trades across accounts using predetermined, automated rules (such as pro-rata average pricing) fixed before orders are submitted.\n- **Do not** trade in your personal account during a blackout window, regardless of how small or inconsequential your order may seem.\n- **Do not** allocate favorable execution prices to favored accounts after seeing where market orders filled during the session.",
        r"\text{blackout} = [t_{\text{order}} - d,\; t_{\text{complete}} + d],\qquad \text{personal trades prohibited in the window}",
        'client_days = 2\nbuffer = 2\nprint("Blackout length in business days:", client_days + 2 * buffer)\nprint("Personal orders inside the window:", "not permitted")',
        "State the priority ordering, compute the blackout length for the two-day client order with a two-day buffer, and explain why the personal trade's small size does not settle the question.",
        "The mandatory priority ordering is: clients first, employer second, personal transactions last. With a 2-day execution period and a 2-day buffer on either side, the blackout window spans exactly 6 business days: 2 days prior + 2 execution days + 2 days after completion. The trade size is irrelevant because the breach consists of misusing confidential advance knowledge of pending client orders. Front-running deprives the client of priority liquidity and destroys the firm's ability to prove fair and unaffected execution.",
        [
            (
                "The priority of transactions ordering is:",
                "Clients, then employer, then personal accounts",
                "Personal accounts, then clients, then employer",
                "Whichever order was entered into the system first",
                "Client interests always take precedence, followed by the employing firm, with personal employee trading ranking strictly last.",
            ),
            (
                "A two-day client order with a two-day buffer on each side implies a blackout of:",
                "6 business days",
                "4 business days",
                "2 business days",
                "The window combines 2 days prior buffer + 2 days of order execution + 2 days post buffer = 6 full business days.",
            ),
            (
                "A small personal trade placed just before a large client order is objectionable because:",
                "It uses knowledge of a pending client order, regardless of its size",
                "Small trades are always prohibited",
                "It reduces the firm's commission income",
                "The violation lies in trading on confidential knowledge of client order flow, not the size of the resulting position.",
            ),
            (
                "Allocating the better fills to one account after seeing the prices is:",
                "A breach of fair dealing, even if every account received something",
                "Acceptable where all accounts had the same strategy",
                "Required, so the largest account is not disadvantaged",
                "Post-trade cherry-picking breaches the duty of fair dealing; allocation rules must be determined before fills are known.",
            ),
        ],
        [CFA_CODE, PLANS, HONOR],
    )

    # ---------------------------------------------------------------- Unit 2
    add(
        "Material non-public information",
        "Inside information and the duty not to trade",
        "Classify information by materiality and availability, and choose the action each combination requires.",
        "Two independent legal criteria determine whether information restricts you from trading: materiality and public availability. Under securities regulations worldwide and CFA Standard II(A), anyone who possesses material non-public information (MNPI) must not trade, direct trades, or tip others until the information has been broadly disseminated to the public.\n\n1. Materiality: Information is material if there is a substantial likelihood that a reasonable investor would consider it important when deciding to buy, sell, or hold a security, or if its disclosure would significantly alter the market price of the asset. Classic examples include impending merger announcements, earnings surprises, major product recalls, regulatory sanctions, or abrupt executive departures.\n2. Non-Public Status: Information remains non-public until it has been broadly disseminated through recognized public channels—such as official regulatory filing systems (e.g. SEC EDGAR, IDX disclosures), major financial news services, or widely distributed press releases—and the market has had sufficient time to absorb and price the news. Information shared in a private chat group, overheard in an elevator, or leaked by a supplier is strictly non-public.\n\nA vital distinction exists between illegal insider tipping and the legitimate 'Mosaic Theory'. Professional financial analysts routinely gather dozens of non-material public facts, industry data points, and non-material non-public observations (such as foot traffic counts or vendor interviews). Piecing these non-material clues together to formulate an insightful, material investment conclusion is good research, not insider trading. The resulting conclusion is the analyst's intellectual property; the legal prohibition applies to receiving and trading on a specific, non-public material fact.",
        "Consider a fictional equity research analyst who visits an industrial park and speaks with an independent transport contractor. The contractor mentions that Pelita Manufaktur experienced a catastrophic boiler failure and halted its primary assembly line four days ago. The company has made no public announcement or regulatory disclosure.\n\nStep-by-step arithmetic:\n1. Management's official published guidance: Expected quarterly revenue of Rp900,000,000,000.\n2. Estimated production loss from the shutdown: Rp72,000,000,000.\n3. Revenue impact: Rp72,000,000,000 / Rp900,000,000,000 = 0.08 = 8.0%.\n\nEvaluating the information:\n• Materiality test: An unexpected 8.0% shortfall in quarterly revenue is undeniably material; any reasonable investor would adjust their cash flow models and lower their valuation.\n• Non-public test: The information has not been published through regulatory disclosures or broad financial news media.\n\nBecause the information satisfies both tests (material AND non-public), the analyst faces immediate restrictions:\n1. Do not trade Pelita Manufaktur shares, bonds, or derivatives in personal or firm accounts.\n2. Do not tip colleagues, portfolio managers, or outside clients.\n3. Immediately report the receipt of this information to compliance so Pelita Manufaktur can be placed on the firm's Restricted List.",
        "Evaluate materiality and public availability separately. Only public information or your own mosaic of non-material facts may support an investment decision or trade.\n\n### Do and do not\n\n- **Do** report the accidental or inadvertent receipt of material non-public information immediately to compliance so the security can be restricted.\n- **Do** maintain a detailed research trail showing the public sources, filings, and non-material observations that formed your investment mosaic.\n- **Do not** buy, sell, or recommend any security while in possession of material non-public information.\n- **Do not** share non-public corporate insights with colleagues, friends, or family members, even in casual conversation.",
        r"\text{restricted} \iff \text{material} \wedge \neg\text{public},\qquad m=\frac{\Delta R}{R}",
        'revenue = 900_000_000_000\nlost = 72_000_000_000\nprint("Revenue effect:", round(lost / revenue, 4))\nprint("Status:", "material and non-public, restricted")',
        "Compute the revenue effect, classify the information on both tests, and list the three actions the analyst must take.",
        "The estimated revenue loss is Rp72,000,000,000 out of Rp900,000,000,000, which equals 8.0%. An 8% revenue drop is clearly material to a reasonable investor, and because the company has not publicly announced the shutdown, the information is non-public. The analyst must take three immediate actions: (1) refrain from trading any securities of Pelita Manufaktur, (2) refrain from tipping or sharing the information with colleagues or clients, and (3) report the receipt to the firm's compliance officer so the company can be placed on the firm's restricted list.",
        [
            (
                "Information is restricted when it is:",
                "Both material and not yet broadly disseminated",
                "Material, whether or not it is public",
                "Non-public, whether or not it is material",
                "Trading restrictions require both conditions to be met: the information must be material (price-sensitive) and non-public (not yet disseminated).",
            ),
            (
                "A halt removing 72bn of 900bn of expected quarterly revenue is a shortfall of:",
                "8%",
                "12.5%",
                "0.8%",
                "72,000,000,000 divided by 900,000,000,000 equals exactly 0.08, or 8.0%.",
            ),
            (
                "Assembling many non-material public and non-public pieces into a material conclusion is:",
                "Legitimate analysis, because the conclusion is the analyst's own work",
                "Prohibited, because the conclusion is material",
                "Permitted only after the issuer approves the conclusion",
                "The Mosaic Theory protects analysts who combine non-material facts into a material thesis; the prohibition applies to trading on specific non-public material items.",
            ),
            (
                "On inadvertently receiving inside information, the correct first step is:",
                "Report it so the firm can restrict the security and record the event",
                "Trade quickly before the information spreads",
                "Wait to see whether the price moves on its own",
                "Immediate compliance reporting allows the firm to restrict trading, establish an information barrier, and create a verifiable record of proper conduct.",
            ),
        ],
        [INSIDER, MARKET_ABUSE, CFA_CODE],
    )

    add(
        "Quotations that are not bona fide",
        "Spoofing, layering, wash trades and painting the tape",
        "Identify manipulative order patterns and the evidence that distinguishes them from ordinary trading.",
        "Market prices only reflect economic supply and demand when the orders behind them represent genuine trading intent. Market manipulation refers to any conduct that creates a false or misleading appearance of trading volume, liquidity, or price movement. The fundamental regulatory requirement under FINRA Rule 5210 and ESMA's Market Abuse Regulation (MAR) is that all quotations and transactions must be bona fide—submitted with the genuine intention of being executed under prevailing market rules.\n\nCommon forms of market manipulation include:\n1. Spoofing and Layering: Entering large non-bona-fide orders on one side of the order book (for instance, massive buy orders) to create the false impression of heavy buying interest. As other market participants adjust their prices upward, the manipulator enters a sell order on the opposite side to execute against that induced price, and instantly cancels the large buy orders before they can be filled.\n2. Wash Trading: Executing transactions where the buyer and seller are under common control or ownership, resulting in no actual change in beneficial ownership. This creates fictitious volume and misleading liquidity on the public tape.\n3. Painting the Tape and Marking the Close: Entering aggressive buy or sell trades at the end of the trading session to manipulate the official closing settlement price, artificially inflating the reported valuation of a fund or avoiding margin calls.\n\nSurveillance algorithms identify manipulation by measuring behavioral patterns: an Order-to-Trade Ratio (OTR) that is an extreme outlier compared to market norms, rapid cancellations clustered immediately after opposite-side fills, or repetitive quote flickering during illiquid periods. While high cancellation rates can occur in legitimate market making, a systematic pattern of deceptive intent distinguishes unlawful manipulation.",
        "Consider a fictional automated trading account active in shares of Cendana Logistik. Over a single trading hour, the algorithm submits 950 limit buy orders and executes only 15 trades. The historical desk baseline for market-making strategies in this security is an Order-to-Trade Ratio (OTR) of 6. Furthermore, audit logs show that 90% of the cancellations occurred within two seconds of the algorithm executing an opposite-side sell order.\n\nStep-by-step arithmetic:\n1. Observed Order-to-Trade Ratio: 950 orders entered / 15 executed trades = 63.3.\n2. Multiple of desk norm: 63.3 / 6.0 = 10.55 times the normal baseline.\n3. Cancellation pattern: 90% of cancels occur within 2 seconds of opposite-side fills.\n\nStatistical interpretation:\nAn OTR of 63.3 (more than ten times the normal desk average) flags the activity as an extreme statistical outlier. When combined with the one-sided order placement and the immediate cancellation after opposite-side executions, this creates clear evidence of spoofing and layering. The algorithm created false visible buy depth to execute sell orders at favorable prices, then vanished. A supervisory investigation must be opened, and the strategy's operational logic and code must be reviewed.",
        "Measure order patterns against statistical baselines before evaluating intent, and maintain technical documentation demonstrating the legitimate economic purpose of automated quoting algorithms.\n\n### Do and do not\n\n- **Do** track order-to-trade ratios, cancellation latencies, and fill rates against documented historical baselines for your strategy.\n- **Do** document the economic and market-making logic of any automated quoting algorithm before deploying it to live markets.\n- **Do not** enter orders that you intend to cancel before execution in order to deceive other participants or induce price movements.\n- **Do not** execute wash trades or matched orders between affiliated accounts to fabricate artificial volume or paint the tape.",
        r"\text{OTR}=\frac{\text{orders entered}}{\text{orders executed}}",
        'orders = 950\nexecuted = 15\nnorm = 6\nratio = orders / executed\nprint("Order-to-trade ratio:", round(ratio, 1))\nprint("Multiple of the desk norm:", round(ratio / norm, 1))',
        "Compute the order-to-trade ratio and its multiple of the desk norm, then state what the numbers do and do not establish.",
        "The order-to-trade ratio is approximately 63.3, which is 10.6 times the normal desk baseline of 6.0. These numbers establish a severe statistical outlier consistent with layering and spoofing, which requires an immediate supervisory review. However, the ratio alone does not constitute final legal proof of manipulative intent; legitimate market makers can experience elevated cancel rates during extreme volatility. The proof of intent comes from combining the ratio with the timing of cancellations—specifically that 90% of orders were canceled immediately after opposite-side fills.",
        [
            (
                "Manipulation is best described as conduct that:",
                "Makes the order book or tape convey something false",
                "Results in a loss for the other side of a trade",
                "Uses an automated system rather than manual orders",
                "Manipulation is defined by conduct that distorts market reality by injecting false impressions of price, volume, or depth into the market.",
            ),
            (
                "950 orders entered and 15 executed gives an order-to-trade ratio of about:",
                "63",
                "6.3",
                "16",
                "950 divided by 15 equals approximately 63.3, which rounds to 63.",
            ),
            (
                "A high order-to-trade ratio on its own:",
                "Identifies an outlier to investigate, not proof of intent",
                "Establishes manipulation without further evidence",
                "Is irrelevant to any manipulation question",
                "High cancellation rates occur in legitimate electronic market making; the ratio flags an anomaly that requires contextual investigation of intent and timing.",
            ),
            (
                "Two accounts under common control trading with each other to show volume is:",
                "A wash trade, because no genuine change of beneficial ownership occurs",
                "Acceptable, because both sides were willing",
                "Permitted if the price used is the prevailing market price",
                "A wash trade involves buying and selling between accounts with the same beneficial owner, creating an illusion of active trading volume without real risk transfer.",
            ),
        ],
        [QUOTES, DECEPTIVE, MARKET_ABUSE],
    )

    add(
        "Promotion, rumour and the pump-and-dump",
        "Communications, verification and the promoted security",
        "Evaluate promotional claims, expose predatory pump-and-dump schemes, and quantify exit liquidity requirements.",
        "A promotional stock campaign creates artificial buying demand that insiders and promoters sell into. The predatory pattern of a 'pump-and-dump' follows a predictable sequence:\n1. Accumulation: Promoters quietly accumulate a large position in a thinly traded, illiquid micro-cap stock.\n2. The Pump: The promoters coordinate an aggressive marketing blitz—across social media groups, anonymous forums, chat rooms, and promotional newsletters—claiming extravagant price targets, imminent corporate acquisitions, or revolutionary technology.\n3. The Dump: As retail investors rush in driven by Fear of Missing Out (FOMO), the price temporarily surges. The promoters quietly dump their massive accumulated holdings directly into this incoming retail demand.\n4. The Collapse: Once the promoters have liquidated their holdings, the promotional messages cease, liquidity vanishes, and the share price collapses back to intrinsic value (or zero). The retail investors who bought last are left holding catastrophic losses.\n\nFINRA Rule 2210 and CFA Standard V(B) govern communications with the public. Every public statement must be fair, balanced, and complete. Repeating unverified market rumors—even when framed as a question like 'Could stock XYZ surge 500%?'—serves as an inducement to trade. The ethical discipline requires examining who benefits from the buying demand generated by a message, what critical risks are omitted, and whether the claimed price target is supported by audited business financials.",
        "Consider a fictional promotional campaign circulating across messaging apps touting Nusantara Digital. The stock trades at Rp200, and promoters claim an imminent target price of Rp1,200 (a 500% increase). The stock is illiquid, with an Average Daily Volume (ADV) of only Rp400,000,000. Corporate registry and disclosure filings reveal that the promoter syndicate currently holds Rp15,000,000,000 worth of shares.\n\nStep-by-step arithmetic:\n1. Total promoter holding: Rp15,000,000,000.\n2. Average daily volume in the market: Rp400,000,000 per day.\n3. Days of trading volume required to exit: Rp15,000,000,000 / Rp400,000,000 = 37.5 trading days.\n\nEconomic reality:\nIn a normal market, trying to sell 37.5 days worth of volume would crash the stock price by 70% to 90% due to market impact. It is mathematically impossible for the promoters to exit their Rp15 billion stake at market prices without manufacturing a massive flood of incoming retail buyers. The campaign does not exist to help investors discover an undervalued company; it exists solely to manufacture the exit liquidity the promoters need to cash out. The Rp1,200 price target is unverifiable fiction, while the Rp15 billion holding and Rp400 million ADV are verifiable facts.",
        "Identify who sells into the buying demand created by a promotional communication, and verify financial claims against audited company statements rather than promotional enthusiasm.\n\n### Do and do not\n\n- **Do** check insider holdings, float size, and average daily volume before acting on unsolicited investment tips or promotional messages.\n- **Do** disclose your personal holdings and your intention to trade whenever you discuss a security in a public forum or media channel.\n- **Do not** repeat or forward unverified market claims, even when framed casually as a rumor or an open question.\n- **Do not** publish bullish commentary or price targets while preparing to sell your own holdings into the resulting retail demand.",
        r"\text{days of volume} = \frac{\text{promoter holding}}{\text{average daily volume}}",
        'holding = 15_000_000_000\nadv = 400_000_000\nprint("Days of average volume to exit:", round(holding / adv, 1))',
        "Compute how many days of average volume the promoters' holding represents, and explain what that implies about the purpose of the campaign.",
        "The promoter syndicate's holding represents 37.5 days of average daily traded volume. Selling a position of this magnitude into an illiquid market without creating artificial demand would cause catastrophic price slippage. Therefore, the promotional campaign exists solely to manufacture artificial retail buying demand (exit liquidity) so the promoters can unload their shares at inflated prices before the hype fades. The advertised price target is an unverified assertion, whereas the promoter holding and daily volume are verifiable facts that expose the scheme.",
        [
            (
                "In a pump-and-dump, the loss is generally borne by:",
                "The investors who bought into the promoted demand last",
                "The promoter, who must hold through the decline",
                "The exchange that listed the security",
                "Promoters sell their accumulated shares into the wave of incoming retail buying; the late buyers suffer the loss when prices collapse.",
            ),
            (
                "A 15,000,000,000 holding against 400,000,000 average daily volume equals:",
                "37.5 days of volume",
                "3.75 days of volume",
                "375 days of volume",
                "Dividing 15,000,000,000 by 400,000,000 yields exactly 37.5 days of average daily volume.",
            ),
            (
                "Repeating an unverified claim framed as a question is:",
                "Still a communication that induces action and must meet the same standard",
                "Acceptable, because a question asserts nothing",
                "Only a problem if the sender holds the security",
                "Framing an unverified rumor as a question does not change its promotional impact on readers or remove the regulatory requirement to avoid misleading statements.",
            ),
            (
                "The most checkable element of a promotional message is usually:",
                "The promoter's holding and the security's traded volume",
                "The price target",
                "The confidence of the person sending it",
                "Shareholder registries, float size, and daily traded volume are verifiable market facts, whereas price targets are speculative assertions.",
            ),
        ],
        [ADVERTISING, FRAUD, DECEPTIVE],
    )

    add(
        "Best execution and order handling",
        "Reasonable diligence, routing and the customer's result",
        "Evaluate execution quality using implementation shortfall, audit order routing incentives, and uphold best execution duties.",
        "Best execution is a legal and fiduciary duty of reasonable diligence, not an impossible guarantee of obtaining the absolute best price recorded during the trading session. Under FINRA Rule 5310 and European MiFID II standards, a broker or asset manager must use reasonable diligence to ascertain the best market for a security and buy or sell so that the resultant price to the customer is as favorable as possible under prevailing market conditions.\n\nBecause financial markets are dynamic and prices fluctuate constantly, regulators evaluate best execution based on the quality and rigor of the firm's execution process rather than an isolated fill on a single order. Diligence is evaluated across multiple factors: the prevailing market price, the bid-ask spread, the size and nature of the order, transaction speed, execution certainty, and available trading venues.\n\nA recognized quantitative measure of execution quality is 'Implementation Shortfall' (IS). Implementation shortfall measures the total economic friction between the paper decision and actual market execution by comparing the average executed price against the benchmark price at the exact moment the investment decision was made ($P_{\text{decision}}$), adding explicit commissions and exchange fees:\n$$\\text{IS} = q\\,(\\bar{P}_{\\text{exec}} - P_{\\text{decision}}) + \\text{fees}$$\nOrder routing arrangements where brokers receive 'Payment for Order Flow' (PFOF) or venue rebates create an inherent conflict of interest. A firm must document that its routing decisions genuinely serve the customer's execution quality rather than maximizing the firm's rebate revenue.",
        "Consider a fictional institutional buy order for 20,000 shares. The portfolio manager decides to execute the order when the market price is Rp1,000 per share (a Rp20,000,000 decision value). The order is routed to the market, filling across multiple trades at a volume-weighted average price of Rp1,004 per share, with total broker commissions and exchange fees of Rp150,000.\n\nStep-by-step arithmetic:\n1. Decision value: 20,000 shares x Rp1,000 = Rp20,000,000.\n2. Price slippage: 20,000 shares x (Rp1,004 - Rp1,000) = Rp80,000.\n3. Explicit commissions and fees: Rp150,000.\n4. Total implementation shortfall: Rp80,000 (slippage) + Rp150,000 (fees) = Rp230,000.\n5. Shortfall as a percentage of decision value: Rp230,000 / Rp20,000,000 = 1.15%.\n\nEvaluating the result:\nWhether an implementation shortfall of 1.15% represents good execution depends on prevailing market conditions: the bid-ask spread at the time, available liquidity on the order book, and whether the order had to be filled urgently or worked patiently. If the stock had an active Rp10 spread (Rp995 bid / Rp1,005 offer), filling 20,000 shares at an average of Rp1,004 shows effective price improvement inside the offer. The firm proves compliance by preserving the decision timestamp, recording venue quotes at arrival, and conducting periodic committee reviews across all executions.",
        "Measure execution performance against the decision price inclusive of all costs, and review venue routing performance periodically across entire order populations.\n\n### Do and do not\n\n- **Do** record the exact decision price and timestamp so that execution slippage can be measured accurately after the trade.\n- **Do** conduct regular, documented reviews of execution quality across all competing venues, market makers, and dark pools.\n- **Do not** treat payment for order flow as neutral revenue; document why routing to that specific venue delivered superior execution for the customer.\n- **Do not** judge execution diligence based on a single favorable fill while ignoring systematic slippage across the broader order book.",
        r"\text{IS} = q\,(\bar{P}_{\text{exec}} - P_{\text{decision}}) + \text{fees}",
        'quantity = 20_000\ndecision = 1_000\nexecuted = 1_004\nfees = 150_000\nslippage = quantity * (executed - decision)\nprint("Price slippage:", slippage)\nprint("Total shortfall:", slippage + fees)\nprint("As a share of decision value:", round((slippage + fees) / (quantity * decision), 4))',
        "Compute the slippage, the total implementation shortfall and its percentage of decision value, then state what evidence would show the obligation was met.",
        "The price slippage is Rp80,000, the total implementation shortfall is Rp230,000, and this represents 1.15% of the Rp20,000,000 decision value. Proving that the best execution obligation was met requires documented evidence: the recorded decision timestamp, the prevailing bid-ask quotes across alternative venues at arrival, the rationale for the chosen routing strategy, and regular committee reviews demonstrating competitive execution quality across all client orders over time.",
        [
            (
                "Best execution requires:",
                "Reasonable diligence to obtain the most favourable terms under prevailing conditions",
                "Achieving the lowest price printed that day",
                "Routing every order to the venue paying the firm the most",
                "Best execution is a process of reasonable diligence across price, cost, speed, and likelihood of execution under prevailing market conditions.",
            ),
            (
                "Buying 20,000 shares at an average of 1,004 after a decision price of 1,000 slips by:",
                "80,000",
                "20,000",
                "150,000",
                "Price slippage equals quantity times price difference: 20,000 x (1,004 - 1,000) = 20,000 x 4 = Rp80,000 before commissions.",
            ),
            (
                "Implementation shortfall is measured against:",
                "The price when the decision was made, including costs",
                "The day's closing price only",
                "The best price printed at any point in the session",
                "Implementation shortfall benchmarks the final executed price and explicit fees against the market price at the moment the trading decision was reached.",
            ),
            (
                "A routing arrangement that pays the firm:",
                "Requires documented evidence that the customer's result was still served",
                "Is prohibited in all circumstances",
                "Needs no review if customers do not complain",
                "Payment for order flow creates an inherent conflict of interest; firms must document that execution quality was preserved and not compromised for rebates.",
            ),
        ],
        [BEST_EX, REG_BI, SUPERVISION],
    )

    # ---------------------------------------------------------------- Unit 3
    add(
        "Accountability for a system that trades",
        "Pre-trade controls, kill switches and named owners",
        "Specify the controls and the named accountability a trading system requires before deployment.",
        "Automating a trading strategy does not reduce human accountability; it concentrates responsibility in the individuals who designed, programmed, deployed, and supervised the algorithm. Algorithms have no independent moral agency or legal liability. Under SEC Rule 15c3-5 (the Market Access Rule) and FINRA Rule 3110 (Supervision), any firm with direct market access must maintain risk management controls and supervisory procedures reasonably designed to systematically manage the financial, regulatory, and market risks of that access.\n\nCrucially, these controls must be pre-trade, hard rejections—not soft advisory warnings—enforced at the gateway before an order reaches an exchange. Core pre-trade controls include:\n1. Maximum single-order share quantity and notional value limits.\n2. Price collars that reject orders priced too far away from the National Best Bid and Offer (NBBO) or last sale price.\n3. Message rate throttles that limit the number of orders and cancellations sent per second.\n4. Cumulative intraday exposure and notional position limits per symbol and for the entire firm.\n5. Cumulative intraday loss limits that halt trading if realized plus unrealized losses cross a defined threshold.\n\nEvery automated system must have an emergency kill switch that can immediately halt all trading activity and cancel open orders. The kill switch must be operable by named supervisors without requiring a code deployment. Furthermore, deployment procedures must include rehearsed rollback plans; deploying code that alters live trading behavior is a market decision that requires the same rigorous sign-off as committing capital.",
        "Consider a fictional quantitative trading desk with the following risk controls: a maximum single-order value of Rp500,000,000, a price collar of 3% against the last trade, and a daily cumulative loss limit of Rp2,000,000,000. Due to a software defect in an unverified release, a trading algorithm enters an infinite loop, submitting repetitive buy orders of Rp90,000,000 each in rapid succession.\n\nStep-by-step arithmetic:\n1. Single order value: Rp90,000,000 (well within the Rp500,000,000 limit, so single-order checks pass).\n2. Price collar: Orders execute within 3% of the prevailing market price, so price collars pass.\n3. Cumulative loss limit: Rp2,000,000,000.\n4. Number of orders passed before the cumulative loss limit halts trading:\n   2,000,000,000 / 90,000,000 = 22.22, which rounds up to the 23rd order.\n5. Total cumulative notional exposure committed: 23 x Rp90,000,000 = Rp2,070,000,000.\n\nControl gap analysis:\nAlthough the cumulative loss limit eventually stopped the loop, the firm incurred over Rp2 billion in unintended exposure. Why? Because the firm relied on per-order limits and an aggregate loss limit, but omitted two critical controls: an order-rate throttle (maximum orders per second) and a cumulative notional exposure cap per symbol. Had an order rate limit of 5 orders per second or a symbol notional cap of Rp500,000,000 been active, the sequence would have been halted after only a few orders, saving hundreds of millions in potential losses.",
        "Establish risk controls as pre-trade hard rejections with defined thresholds and named owners, and test emergency kill switches and rollback procedures in staging before deployment.\n\n### Do and do not\n\n- **Do** enforce risk limits pre-trade at the trading gateway, configured as hard order rejections rather than post-trade warnings.\n- **Do** designate named supervisory owners authorized to trigger the kill switch, and rehearse emergency shutdowns regularly.\n- **Do not** deploy code modifications that alter live trading behavior without the formal review and sign-off required for a trading decision.\n- **Do not** rely solely on single-order value limits; enforce message rate throttles and cumulative intraday notional caps.",
        r"n^{*} = \left\lceil \frac{L}{v} \right\rceil,\qquad \text{loss limit } L,\ \text{order value } v",
        'limit = 2_000_000_000\norder = 90_000_000\ncrossing = limit // order + 1\nprint("Orders before the cumulative limit binds:", crossing)\nprint("Notional at that point:", crossing * order)',
        "Compute how many orders pass before the cumulative loss limit binds and the notional reached, then name the two controls that would have stopped the sequence sooner.",
        "Twenty-three orders pass before the cumulative loss limit binds, reaching a total notional exposure of Rp2,070,000,000. Two pre-trade controls would have halted the runaway sequence much sooner: (1) an order-rate limit (throttling maximum orders per second) and (2) a cumulative notional exposure cap per symbol. The single-order limit of Rp500,000,000 failed to stop the loop because each individual Rp90,000,000 order was below that threshold.",
        [
            (
                "Automating a strategy changes responsibility by:",
                "Concentrating it in whoever specified, deployed and supervised the system",
                "Transferring it to the software vendor",
                "Removing it, since no person entered the orders",
                "Automation concentrates accountability in the developers, risk managers, and supervisors who build, release, and oversee the software.",
            ),
            (
                "With a 2,000,000,000 loss limit and 90,000,000 orders, the limit binds after:",
                "23 orders",
                "20 orders",
                "223 orders",
                "2,000,000,000 / 90,000,000 is approximately 22.22, meaning the limit is breached when the 23rd order is processed.",
            ),
            (
                "Per-order value limits failed here because:",
                "Every individual order was compliant while the cumulative total was not",
                "The limit was set too low",
                "The orders were entered manually",
                "Each order of Rp90,000,000 was well within the Rp500,000,000 per-order limit; without rate and cumulative caps, repeated orders slipped through.",
            ),
            (
                "A pre-trade control should:",
                "Reject the order before it reaches the market",
                "Log a warning for later review",
                "Notify the trader after the fill is received",
                "Pre-trade controls must actively block and reject non-compliant orders before they enter market gateways to prevent erroneous exposure.",
            ),
        ],
        [MARKET_ACCESS, SUPERVISION, CFA_CODE],
    )

    add(
        "Honest backtests: search, selection and reporting",
        "Multiple testing, selective reporting and what a result supports",
        "Adjust a reported result for the size of the search that produced it.",
        "A historical backtest represents the outcome of an experimentation process, but outside readers typically see only the single winning configuration. This gap between the search process and the reported result is where quantitative research often becomes misleading without anyone stating an outright falsehood. Testing dozens of indicator combinations, moving average windows, or stop-loss thresholds and presenting only the survivor as if it were a single pre-specified hypothesis severely exaggerates the statistical evidence. This bias is known as data snooping, p-hacking, or selection bias.\n\nWhen testing multiple hypotheses, the probability of finding a false positive increases dramatically with every trial. If you test 40 independent, completely random strategies at a conventional 5% significance level (alpha = 0.05), the probability of finding at least one false positive purely by chance is:\n$$P(\\text{at least one false positive}) = 1 - (1 - \\alpha)^m = 1 - (0.95)^{40} \\approx 87.1\\%$$\nPresenting that lucky winner as a genuine market discovery is deceptive.\n\nThe ethical and scientific remedy is procedural and straightforward: record the total number of configurations tested in an auditable research registry before analyzing results, archive rejected runs, and adjust your significance threshold for the search conducted. A standard Bonferroni adjustment divides the target significance level by the number of trials ($m$):\n$$\\alpha^* = \\frac{\\alpha}{m}$$\nFurthermore, researchers must hold out a sequestered out-of-sample dataset that is never touched during strategy design, and report transparently if that holdout was ever inspected.",
        "Consider a fictional quantitative researcher who tests 40 different parameter variations of a momentum strategy on historical stock data. The researcher selects the single best-performing variation, which achieves a p-value of 0.01, and writes an investment memo describing the strategy as 'statistically significant at the 5% level (p < 0.05)'.\n\nStep-by-step arithmetic:\n1. Target significance level: alpha = 0.05.\n2. Number of configurations tested: m = 40.\n3. Bonferroni-adjusted significance threshold: 0.05 / 40 = 0.00125.\n4. Comparison: The reported p-value of 0.01 is greater than the adjusted threshold of 0.00125 (0.01 > 0.00125), so the result fails the multiple-testing test.\n5. Probability of at least one false positive under the null hypothesis:\n   1 - (1 - 0.05)^40 = 1 - (0.95)^40 = 1 - 0.1285 = 0.8715 = 87.1%.\n\nScientific interpretation:\nAcross 40 independent random tests, there is an 87.1% probability of finding at least one result with p < 0.05 by pure chance. Therefore, finding a best p-value of 0.01 is entirely consistent with random noise. The honest conclusion for the research memo is: 'Across 40 tested configurations, the best parameter set achieved a p-value of 0.01, which fails the multiple-testing threshold of 0.00125 and is consistent with random chance; the evidence does not support live capital allocation.'",
        "Report the entire search process, not just the surviving configuration. Determine significance thresholds before examining results, and archive all rejected parameter runs.\n\n### Do and do not\n\n- **Do** log the number of configurations planned and tested in a research registry before running backtest trials.\n- **Do** adjust the required significance threshold for the number of trials conducted, and specify the adjustment method used.\n- **Do not** present the best result of dozens of backtests as if it were a single pre-registered hypothesis.\n- **Do not** re-use a sequestered holdout data segment to tune parameters after receiving disappointing initial results.",
        r"\alpha^{*}=\frac{\alpha}{m},\qquad P(\text{any } p<\alpha)=1-(1-\alpha)^{m}",
        'alpha = 0.05\ntrials = 40\nreported = 0.01\nprint("Adjusted threshold:", alpha / trials)\nprint("Reported result passes:", reported < alpha / trials)\nhalf = (1 - alpha) ** 20\nprint("Chance of at least one false positive:", round(1 - half * half, 3))',
        "Compute the adjusted threshold, decide whether the reported result passes it, and calculate the probability of at least one false positive across the search. Then write the honest one-sentence conclusion.",
        "The adjusted significance threshold is 0.00125, and the reported p-value of 0.01 fails this test. The probability of observing at least one false positive below 0.05 across 40 independent tests under the null hypothesis is approximately 0.871 (87.1%). The honest conclusion is: 'The best result across forty tested configurations yielded a p-value of 0.01, which is fully consistent with random noise under multiple testing and does not provide statistical evidence to support deploying capital.'",
        [
            (
                "Reporting only the best of many tested configurations:",
                "Overstates the evidence, because the search itself is part of the result",
                "Is appropriate, since the others were rejected on merit",
                "Is acceptable whenever the winner has an economic story",
                "The breadth of the search determines how easily random noise can produce an attractive result; omitting trials misrepresents the evidence.",
            ),
            (
                "A Bonferroni-adjusted threshold at 5% across 40 trials is:",
                "0.00125",
                "0.05",
                "0.002",
                "Dividing 0.05 by 40 trials gives an adjusted threshold of exactly 0.00125.",
            ),
            (
                "Across 40 independent null tests, the chance of at least one p-value below 0.05 is about:",
                "87%",
                "5%",
                "40%",
                "The probability is 1 - (1 - 0.05)^40 = 1 - 0.95^40 = 1 - 0.1285 = approximately 0.8715, or 87%.",
            ),
            (
                "Re-using a holdout segment after a disappointing result:",
                "Destroys its value as an untouched test and must be disclosed",
                "Is fine as long as the model is not changed afterwards",
                "Improves the estimate by adding data",
                "Once holdout data influences a modeling decision or parameter choice, it is no longer an independent out-of-sample test.",
            ),
        ],
        [GIPS, CFA_CODE, HONOR],
    )

    add(
        "The data you are allowed to use",
        "Provenance, licensing and point-in-time evidence",
        "Establish whether a dataset may be used and whether it reflects what was knowable at the time.",
        "Two independent questions govern whether a dataset can be used in quantitative trading: legal provenance and temporal integrity.\n\n1. Legal Provenance: Do you have the lawful right to collect, store, and use this data for trading? Commercial availability does not automatically grant a right of use. Data scraped from a website in violation of its Terms of Service (ToS), datasets containing Personally Identifiable Information (PII) harvested without consent, or proprietary data leaked by someone breaching a duty of confidentiality are legally tainted. Using such data exposes your firm to breach-of-contract claims, copyright infringement, and regulatory sanctions.\n2. Temporal Integrity (Point-in-Time Reality): Does the dataset reflect what market participants actually knew at the exact timestamp of the simulated trading decision? Many macroeconomic indicators (such as GDP, employment numbers, and inflation) and corporate financial statements undergo subsequent revisions months or years after their initial release.\n\nIf a historical database updates its records with final revised figures without preserving the original as-published values, a backtest querying that database will suffer from 'look-ahead bias' or 'revision hindsight'. The model will simulate trades based on information that was not knowable on the decision date. Professional research environments utilize point-in-time (vintage) databases that preserve the exact values published at each historical release date.",
        "Consider a fictional macroeconomic quantitative strategy that trades government bonds based on annual GDP growth releases. The research backtest uses a historical database showing that GDP growth for a given year was 5.03%. However, archival records show that on the official morning release date, the statistics agency published an initial estimate of 4.86%. The figure was only revised upward to 5.03% fourteen months later following comprehensive annual tax audits.\n\nStep-by-step arithmetic:\n1. Final revised GDP figure in database: 5.03%.\n2. As-published GDP figure on release date: 4.86%.\n3. Hindsight bias introduced: 5.03% - 4.86% = 0.17 percentage points = 17 basis points.\n\nImplications of the error:\nA trading algorithm executing on the morning after the release could only have observed 4.86%. If the strategy rule was to buy bonds whenever GDP growth came in below 5.00%, in live trading on that day it would have bought bonds (since 4.86% < 5.00%). In the backtest, however, the model observed the revised 5.03% and did not buy bonds. The backtest file contains no false numbers—5.03% is indeed the true revised GDP—but attaching that value to the earlier decision date injects 17 basis points of future hindsight, producing a backtest result that cannot be replicated in live markets.",
        "Record complete provenance metadata with every dataset, and use point-in-time vintage archives that preserve as-published values for historical backtests.\n\n### Do and do not\n\n- **Do** store the data source, license terms, collection timestamp, and as-of vintage date for every series in your database.\n- **Do** use point-in-time datasets that record the exact numbers published on the decision date whenever modeling release-driven trades.\n- **Do not** assume that because data is accessible on the web or sold by a vendor, you automatically have the legal right to trade on it.\n- **Do not** use revised historical time series in a backtest without documenting that the simulation relies on post-release revisions.",
        r"\text{usable} \iff \text{licensed} \wedge \text{as\text{-}of} \le t_{\text{decision}}",
        'revised = 5.03\nas_published = 4.86\nprint("Basis points of hindsight:", round((revised - as_published) * 100, 1))\nprint("Usable at the decision date:", as_published)',
        "Compute the hindsight introduced by the revision in basis points, and list the four provenance fields you would store with the series.",
        "The revision introduces 17 basis points of hindsight bias (5.03% - 4.86% = 0.17%). The four essential provenance fields that must be stored with every historical data series are: (1) the originating source or publisher, (2) the license terms and permitted use rights, (3) the exact collection timestamp, and (4) the as-of vintage date indicating when the data became knowable to the market.",
        [
            (
                "Whether a dataset may be used and whether it is point-in-time are:",
                "Two separate questions, and both must be answered",
                "The same question expressed differently",
                "Only relevant for paid data",
                "Licensing determines legal permission to use the data; point-in-time status determines whether it reflects what was historically knowable.",
            ),
            (
                "A revised 5.03% against an originally published 4.86% differs by:",
                "17 basis points",
                "1.7 basis points",
                "0.17 basis points",
                "5.03% minus 4.86% equals 0.17 percentage points. Since 1 percentage point equals 100 basis points, 0.17 points equals 17 basis points.",
            ),
            (
                "Data being commercially available means:",
                "Nothing by itself about whether you are permitted to use it",
                "That any licensing question has been settled by the vendor",
                "That the data must be point-in-time",
                "Commercial availability does not guarantee legal compliance; buyers must still verify that the collection method respects privacy, terms of service, and confidentiality.",
            ),
            (
                "Using the latest revised value at an earlier decision date:",
                "Introduces information that did not exist then, even though no value is incorrect",
                "Is acceptable because revisions improve accuracy",
                "Only matters for high-frequency strategies",
                "While the revised value is factually accurate today, using it at an earlier historical date introduces look-ahead bias that distorts backtests.",
            ),
        ],
        [STATEMENTS, CFA_CODE, GIPS],
    )

    add(
        "The claims you may make about performance",
        "Fair representation, net returns and full disclosure",
        "State a performance record so that a reader who did not build it can evaluate it.",
        "Performance reporting is where quantitative research directly meets investors and prospective clients. The Global Investment Performance Standards (GIPS) established by CFA Institute rest on two foundational principles: Fair Representation and Full Disclosure. The goal is to provide a complete, unbiased historical record so that an investor who did not build the model can independently evaluate its risk and return characteristics.\n\nA presentation must show the entire relevant record rather than a cherry-picked flattering window. Common deceptive marketing practices include:\n1. Selective Period Selection: Choosing an inception date that starts immediately after a major drawdown to show inflated annualized gains.\n2. Survivorship Bias: Quietly excluding closed or poorly performing accounts and displaying only surviving funds.\n3. Gross-of-Fees Distortion: Advertising gross returns that ignore management fees, performance allocations, and execution costs that real investors must bear.\n4. Unlabeled Simulations: Presenting hypothetical or simulated paper-trading returns alongside live track records without prominent, clear labels.\n\nA single year of returns represents exactly one draw from an underlying distribution, not evidence of a sustained rate. Annualizing a short sample (such as multiplying a 3-month gain by four) to imply an ongoing return is misleading. A fair presentation discloses sample length, benchmark performance, deducted costs, live versus simulated status, and the market conditions under which the strategy would be expected to perform poorly.",
        "Consider a fictional trading strategy presenting a marketing summary that highlights a 10.0% return over its first twelve months of live trading, compared to an 8.0% return for its benchmark index. The fund deducted an ongoing operating charge of 0.10 percentage points per month (10 basis points monthly).\n\nStep-by-step arithmetic:\n1. Monthly deducted cost: 0.10% = 0.001.\n2. Annual operating cost deducted: 12 months x 0.10% = 1.20% (120 basis points).\n3. Reported net return: 10.0%.\n4. Approximate gross return: Net return + deducted costs = 10.0% + 1.2% = 11.2%.\n5. Sample size: 12 monthly periods represent 1 single observation of an annual outcome.\n\nEvaluating fair presentation:\nUnder GIPS standards, presenting the 10.0% net figure is appropriate, but it cannot stand alone. The presentation must prominently state:\n• The benchmark name and its 8.0% return over the exact same period.\n• The 1.20% annual fee drag that was deducted to reach the net figure.\n• That the track record spans only 12 months, representing a single annual sample.\n• Whether the results reflect actual live capital or hypothetical backtested paper performance.",
        "Present investment performance net of all client-borne fees, alongside an appropriate benchmark, stating sample length and live versus simulated status.\n\n### Do and do not\n\n- **Do** report performance net of all management fees, performance fees, and trading expenses that an investor would bear.\n- **Do** label simulated, backtested, or paper-trading results clearly and prominently wherever performance numbers appear.\n- **Do not** choose an arbitrary start date that flatters the track record, or quietly drop accounts that suffered losses.\n- **Do not** annualize returns from a short time window to create the impression of a sustained long-term rate of return.",
        r"r_{\text{net}} = r_{\text{gross}} - \sum_{t} c_t,\qquad \text{state } n \text{ and the benchmark}",
        'monthly_cost = 0.001\nmonths = 12\nnet = 0.10\nprint("Annual cost deducted:", round(monthly_cost * months, 4))\nprint("Approximate gross return:", round(net + monthly_cost * months, 4))\nprint("Observations of an annual outcome:", 1)',
        "Compute the annual cost deducted and the approximate gross return, then write the four facts that must accompany the 10% figure.",
        "The annual cost deducted is 1.20 percentage points (120 basis points), and the approximate gross return is 11.20%. To satisfy fair representation, the 10.0% net return must be accompanied by four essential facts: (1) the designated benchmark and its 8.0% return over the same period, (2) the specific management and operating costs deducted, (3) the 12-month duration of the record (indicating a single annual observation), and (4) an explicit label confirming whether the performance is live or simulated.",
        [
            (
                "Fair representation of performance requires:",
                "The whole relevant record, net of costs, with its benchmark and limitations",
                "The highest return the strategy achieved in any window",
                "Gross returns, so costs do not obscure the manager's skill",
                "Fair presentation requires completeness: presenting the entire record net of fees, alongside relevant benchmarks, and disclosing sample limitations.",
            ),
            (
                "A 10% net return after 0.10 percentage points of monthly cost implies a gross of about:",
                "11.2%",
                "10.1%",
                "8.8%",
                "Twelve months at 0.10 percentage points per month equals 1.2 percentage points of annual cost. Adding that to 10.0% net gives approximately 11.2% gross.",
            ),
            (
                "Twelve months of results represent:",
                "One observation of an annual outcome, not a sustained rate",
                "Twelve independent pieces of evidence about annual performance",
                "A sufficient sample once the return exceeds the benchmark",
                "A one-year track record is a single annual observation; monthly returns within that year share the same macro environment and do not provide multi-year evidence.",
            ),
            (
                "Showing simulated results beside live results without labelling them is:",
                "An omission that makes the presentation misleading",
                "Acceptable if the simulation used the same rules",
                "Required, so the reader sees the full history",
                "Prospective investors cannot evaluate risk without knowing whether results represent real capital traded under live market frictions or hypothetical simulations.",
            ),
        ],
        [GIPS, ADVERTISING, FEES],
    )

    # ---------------------------------------------------------------- Unit 4
    add(
        "Advising another person",
        "Suitability, risk capacity and the money that cannot be lost",
        "Separate a client's willingness to take risk from their capacity to absorb a loss.",
        "Suitability is a core regulatory obligation under Regulation Best Interest (Reg BI) and CFA Standard III(C). Advisers and traders often make the dangerous mistake of collapsing two completely different concepts into a single questionnaire score:\n\n1. Risk Tolerance: A psychological preference—how much price volatility, uncertainty, or temporary drawdown an investor is emotionally willing to experience.\n2. Risk Capacity: An objective financial fact—how large a financial loss an investor's balance sheet and life circumstances can actually absorb without forcing asset liquidations, causing debt default, or preventing essential life commitments from being met.\n\nA client may have an aggressive psychological risk tolerance (answering 'I am comfortable with a 40% decline for higher growth'), yet have zero capacity to take risk with money that is legally committed to a tuition payment, home mortgage down payment, or medical expense in the near term. The investment recommendation must always be constrained by the smaller of the two factors: Risk Capacity overrides Risk Tolerance.\n\nRisk capacity is determined by mapping out the timeline of committed liabilities, not by administering an attitude questionnaire. Any funds needed within the time horizon of a plausible market downturn cannot be exposed to equity or credit risk, regardless of how enthusiastically the client claims to embrace volatility. Liquidity is equally essential: an institution or individual can own assets that look valuable on paper, yet face catastrophic insolvency if those assets cannot be converted into cash to meet mandatory obligations during a crisis.",
        "Consider a fictional client who holds total investable assets of Rp300,000,000. In eighteen months, the client has a binding legal commitment to pay Rp120,000,000 for a property down payment. The client completes a risk questionnaire and states an enthusiastic willingness to endure a 40% market decline for maximum capital growth.\n\nStep-by-step arithmetic:\n1. Total assets: Rp300,000,000.\n2. Committed liabilities due within 18 months: Rp120,000,000.\n3. True Risk Capacity (capital available for risk): Rp300,000,000 - Rp120,000,000 = Rp180,000,000.\n4. Modeled 30% decline on the risky allocation: 0.30 x Rp180,000,000 = Rp54,000,000.\n5. Dollar loss as a percentage of total wealth: Rp54,000,000 / Rp300,000,000 = 18.0%.\n\nSuitability evaluation:\nThe committed Rp120,000,000 must be placed in liquid, capital-preserving instruments (such as short-term government treasury bills or insured bank deposits) so it is guaranteed to be available in 18 months. The client's stated 40% risk tolerance can only be applied to the remaining Rp180,000,000 of risk capacity. Even if the client insists that they want to invest all Rp300,000,000 in volatile equities, doing so would violate fiduciary suitability. If a 30% market drop occurred, total assets would fall to Rp210,000,000, and paying the Rp120,000,000 liability would leave only Rp90,000,000—permanently locking in the loss.",
        "Compute objective risk capacity by identifying and subtracting dated financial commitments first, then apply psychological risk tolerance only to the capital that remains.\n\n### Do and do not\n\n- **Do** map out the exact date and amount of every committed obligation before determining risk asset allocations.\n- **Do** record both psychological risk tolerance and objective risk capacity, and ensure recommendations respect the lower limit.\n- **Do not** allow a client's enthusiastic risk tolerance questionnaire to risk money that is committed to short-term obligations.\n- **Do not** recommend illiquid or volatile investment products for funds that may need to be accessed on short notice.",
        r"K = A - L_{\text{committed}},\qquad \text{loss} = d\cdot K",
        'assets = 300_000_000\ncommitted = 120_000_000\ndecline = 0.30\ncapacity = assets - committed\nprint("Amount available for risk:", capacity)\nprint("Loss in the modelled decline:", capacity * decline)\nprint("Share of total assets:", round(capacity * decline / assets, 4))',
        "Compute the amount available for risk, the loss in the modelled decline and its share of total assets, then state why a stated 40% tolerance does not change the answer.",
        "The capital available for risk is Rp180,000,000, a 30% decline on that portion results in a loss of Rp54,000,000, which represents 18.0% of total assets. The client's stated 40% risk tolerance cannot alter this allocation because the Rp120,000,000 is legally committed within 18 months. Risk capacity is an objective balance sheet constraint; risking committed funds exposes the client to forced liquidation at a market bottom.",
        [
            (
                "Risk capacity differs from risk tolerance because capacity is:",
                "A fact about circumstances, while tolerance is a preference",
                "A preference, while tolerance is measured from past returns",
                "The same thing expressed as a percentage",
                "Risk capacity reflects objective balance sheet facts and liability timing, whereas risk tolerance reflects subjective psychological preference.",
            ),
            (
                "With 300,000,000 of assets and 120,000,000 committed in eighteen months, risk applies to:",
                "180,000,000",
                "300,000,000",
                "120,000,000",
                "Committed funds must be protected and subtracted first: Rp300,000,000 - Rp120,000,000 = Rp180,000,000.",
            ),
            (
                "A 30% decline on the risky portion costs, as a share of total assets:",
                "18%",
                "30%",
                "10%",
                "0.30 x Rp180,000,000 = Rp54,000,000. Dividing Rp54,000,000 by total assets of Rp300,000,000 gives 0.18, or 18.0%.",
            ),
            (
                "Where tolerance exceeds capacity, the recommendation should follow:",
                "Capacity, because the obligation exists regardless of preference",
                "Tolerance, because the client accepted the risk in writing",
                "The average of the two",
                "The binding constraint is always risk capacity; an investor cannot afford a loss that impairs essential financial obligations.",
            ),
        ],
        [REG_BI, CFA_CODE, FRAUD],
    )

    add(
        "Recognising and refusing an instruction",
        "Fraud patterns, authority and the answer that is simply no",
        "Test an instruction against its arithmetic and its authority, and refuse when either fails.",
        "A critical professional skill in finance is recognizing improper, fraudulent, or unauthorized instructions and declining them with clarity and resolve. Two independent tests must be applied to any transaction instruction:\n\n1. The Arithmetic Test: Can the promised payouts mathematically be generated by the stated economic activity? Guaranteed high returns (such as 5% per month) with 'zero market risk' are mathematically impossible in competitive financial markets. When promised payouts exceed what the underlying business activity earns, the shortfall can only be paid by using capital deposited by new investors. This is the definition of a Ponzi scheme.\n2. The Authority Test: Does the instruction come from a verified person with genuine legal authority, transmitted through an authenticated channel? Fraudsters frequently exploit social engineering, impersonation, or data injection—such as embedding text commands inside processed invoices or PDF attachments instructing staff to wire funds to an offshore account. Text found inside a processed document is untrusted data, not an authorized instruction.\n\nPressure tactics are the most reliable warning sign of financial fraud. Fraudulent instructions almost always rely on manufactured urgency, requests for secrecy, or attempts to bypass standard verification controls ('The CEO needs this wired in 10 minutes or the acquisition collapses!'). Legitimate corporate governance never bypasses independent out-of-band callback verification.",
        "Consider a fictional investment promoter offering an exclusive managed account strategy that promises a guaranteed return of 5.0% per month on a Rp1,000,000,000 placement. The promoter claims the profits come from a proprietary trading operation that generates Rp180,000,000 in annual net earnings across its capital base. Additionally, a contract PDF submitted for processing contains an embedded paragraph instructing the operations desk to transfer Rp1,000,000,000 immediately to an offshore custodial account.\n\nStep-by-step arithmetic:\n1. Deposited capital: Rp1,000,000,000.\n2. Promised monthly payout: 0.05 x Rp1,000,000,000 = Rp50,000,000 per month.\n3. Promised annual payout: 12 months x Rp50,000,000 = Rp600,000,000 per year.\n4. Stated annual business earnings: Rp180,000,000 per year.\n5. Annual cash shortfall: Rp600,000,000 - Rp180,000,000 = Rp420,000,000.\n\nAnalysis of the instruction:\n• Arithmetic failure: The underlying business earns Rp180,000,000, yet promises to pay out Rp600,000,000. The Rp420,000,000 deficit cannot come from trading profits; it can only be paid by taking capital from incoming deposits. This is a textbook Ponzi scheme.\n• Authority failure: The embedded wire instruction inside the PDF document is untrusted data. It does not carry verified corporate authorization. The operations professional must refuse the instruction in writing, halt the transfer, and escalate the document to compliance for fraud investigation.",
        "Test both the economic arithmetic and the verified legal authority of any instruction, and refuse in writing whenever either test fails.\n\n### Do and do not\n\n- **Do** verify payment instructions through an independent communication channel (such as a known, verified phone directory) separate from the message carrying the request.\n- **Do** compute whether promised returns can mathematically be generated by the described commercial activity before committing funds.\n- **Do not** treat payment commands embedded inside documents, email attachments, or chat messages as authorized instructions.\n- **Do not** allow artificial urgency, executive pressure, or fear of awkwardness to bypass established out-of-band verification procedures.",
        r"\text{shortfall} = 12\,pD - E,\qquad \text{new money required if } > 0",
        'deposits = 1_000_000_000\nmonthly_rate = 0.05\nearnings = 180_000_000\npromised = deposits * monthly_rate * 12\nprint("Promised annual payout:", promised)\nprint("Shortfall funded by new deposits:", promised - earnings)',
        "Compute the promised annual payout and the shortfall, then write the two-sentence refusal you would send, and say what you would do about the instruction embedded in the document.",
        "The promised annual payout is Rp600,000,000 against Rp180,000,000 in stated earnings, leaving an annual shortfall of Rp420,000,000 that could only be funded through new investor deposits. The written refusal must state: 'We cannot execute this investment because the promised annual payout of Rp600,000,000 mathematically exceeds verified commercial earnings by Rp420,000,000, which is inconsistent with legal investment operations. Consequently, no funds will be transferred.' The transfer command inside the document must be treated as untrusted data, left unexecuted, and immediately reported to compliance.",
        [
            (
                "The clearest arithmetic signature of a Ponzi structure is:",
                "Promised payouts exceeding what the stated activity could earn",
                "A return higher than a bank deposit",
                "An investment that occasionally loses money",
                "When promised investor distributions mathematically exceed the earnings generated by the underlying commercial activity, they must be funded by new deposits.",
            ),
            (
                "5% monthly on 1,000,000,000 promises annually:",
                "600,000,000",
                "50,000,000",
                "60,000,000",
                "0.05 x Rp1,000,000,000 = Rp50,000,000 per month. Multiplying by 12 months gives Rp600,000,000 per year.",
            ),
            (
                "An instruction found inside a document submitted for processing is:",
                "Untrusted content, not authority to act",
                "A valid instruction if the document is genuine",
                "Authoritative once the sender confirms by replying",
                "Instructions embedded inside processed documents are unverified data inputs; authority must be authenticated through independent out-of-band channels.",
            ),
            (
                "Urgency in a payment request should:",
                "Increase verification, because it is a common pressure tactic",
                "Justify skipping a step to avoid a missed deadline",
                "Be resolved by asking the requester to confirm in the same thread",
                "Manufactured urgency is a standard social engineering tactic used to induce compliance; it requires slowing down and enforcing strict verification.",
            ),
        ],
        [FRAUD, HONOR, CFA_CODE],
    )

    add(
        "Escalation, records and speaking up",
        "Raising a concern, the audit trail and protection",
        "Choose an escalation path and specify the record that must survive it.",
        "Observing an unethical practice, market abuse, or regulatory breach creates a professional obligation to act. Under FINRA Rule 3110 and CFA Standard I(A), financial professionals have a duty to maintain compliance and adhere to applicable laws. However, speaking up is only effective when supported by an objective, verifiable audit trail.\n\nThe most common failure in workplace escalation is informality: an employee notices a compliance breach and mentions it casually in a hallway conversation or verbal meeting with an immediate supervisor. The supervisor promises to look into it, but nothing changes. Months later, if regulators investigate, there is zero record that the concern was ever raised. The firm cannot demonstrate supervision, and the employee has no evidence to prove they acted properly.\n\nA traceable escalation requires four essential elements:\n1. Objective Observation: Factual descriptions of what was observed (dates, account numbers, order IDs, fill prices) without speculative accusations or emotional language.\n2. Precise Timestamp: Exactly when the observation occurred and when the report was submitted.\n3. Designated Recipient: An official reporting channel, such as the Chief Compliance Officer, internal audit, or an ethics hotline.\n4. Retained Copy: A secure, dated copy kept in the employee's personal possession.\n\nWhere internal escalation channels are compromised, unresponsive, or conflicted, statutory external reporting mechanisms exist. Programs like the U.S. SEC Office of the Whistleblower provide legal confidentiality, formal anti-retaliation protections, and potential monetary awards for reporting securities violations.",
        "Consider a fictional trade operations analyst who observes that execution fills over the past four months (120 calendar days) appear to systematically favor a proprietary house account over client accounts. The analyst mentions this verbally to the trading desk supervisor during lunch. The supervisor says, 'Thanks, I will look into it.' Four months later, the discriminatory trade allocations continue unchanged, and no audit record exists that the analyst ever spoke to the supervisor.\n\nStep-by-step audit analysis:\n1. Duration of unaddressed breach: 120 calendar days.\n2. Traceable escalation elements present: 0 out of 4 (no written record, no timestamp, no official compliance receipt, no retained copy).\n\nConsequences of informal reporting:\nBy relying on an unrecorded verbal remark, the analyst lost 120 days of enforcement time, the clients suffered continued financial harm, and the analyst has no documentation proving they fulfilled their duty. If regulators examine the desk, the analyst could be questioned as a complicit bystander.\n\nHad the analyst drafted a formal, dated written memorandum to the compliance department—specifying the exact trade IDs, timestamps, account numbers, and fill price disparities, and keeping a copy—the firm would have had an actionable audit trail, and the analyst would have possessed irrefutable proof of timely escalation.",
        "Escalate compliance concerns in writing, keep a secure personal copy with timestamps, and report verifiable observations rather than personal conclusions.\n\n### Do and do not\n\n- **Do** submit compliance concerns in writing with specific dates, trade identifiers, account numbers, and factual observations.\n- **Do** retain your own dated copy of the escalation and document any official response or remediation received.\n- **Do not** rely on casual verbal conversations that leave no auditable paper trail.\n- **Do not** conduct rogue personal investigations that alter, delete, or compromise the integrity of underlying electronic records.",
        r"\text{traceable} \iff \text{observation} + \text{timestamp} + \text{recipient} + \text{retained copy}",
        'days = 120\nelements = 4\nprint("Days of activity in the record:", days)\nprint("Elements a traceable escalation needs:", elements)\nprint("Recorded in writing:", "no")',
        "List the four elements that make an escalation traceable, and explain what the analyst lost by raising the concern verbally.",
        "A traceable escalation requires four components: (1) an objective factual observation, (2) an exact timestamp, (3) a designated formal recipient (such as compliance), and (4) a securely retained copy. By raising the concern verbally, the analyst lost all proof of having reported the breach, deprived the firm of a documented audit trail to initiate supervisory action, and allowed the unfair allocation pattern to continue uncorrected for 120 days without accountability.",
        [
            (
                "An escalation is traceable when it records:",
                "The observation, its timestamp, the recipient and a retained copy",
                "The analyst's conclusion about who was responsible",
                "A verbal summary given to the nearest supervisor",
                "A verifiable audit trail requires a factual observation, a timestamp, a documented formal recipient, and a retained copy.",
            ),
            (
                "Raising a concern verbally with no record primarily costs:",
                "The evidence that the concern was ever raised",
                "The analyst's right to raise it again",
                "The firm's obligation to supervise",
                "Without a written record, there is no proof that the concern was brought to management's attention, making supervisory follow-up unverifiable.",
            ),
            (
                "An escalation is most useful when it describes:",
                "Observations with dates and identifiers, rather than conclusions",
                "The motive you believe explains the behaviour",
                "Only the total amount involved",
                "Documenting verifiable facts (timestamps, account numbers, prices) allows independent reviewers to audit the data without being sidetracked by subjective motives.",
            ),
            (
                "Investigating alone by altering the underlying records:",
                "Damages the evidence others will need",
                "Is the fastest way to confirm a concern",
                "Is required before escalating",
                "Tampering with or modifying database records spoils electronic evidence required by compliance officers and regulatory investigators.",
            ),
        ],
        [SUPERVISION, WHISTLE, HONOR],
    )

    add(
        "Your written trading charter",
        "A personal code of conduct with checkable rules",
        "Assemble the course into a personal charter of rules that can be checked after the fact.",
        "A personal trading charter transforms ethical principles into operational reality: a concise, written document specifying what you will do, what you will never do, and how every rule will be independently audited. Its protective value comes from being drafted in calm reflection before market pressure begins. In the heat of live trading—surrounded by price volatility, fear, greed, and time pressure—human willpower is unreliable and prone to self-serving rationalizations. Professional codes exist so that ethical decisions are already settled before temptation arises.\n\nA usable charter rule consists of three essential components:\n1. The Specific Behavior: Exactly what action is permitted or restricted (e.g. entering a trade, setting a position size, routing an order).\n2. The Quantitative Threshold: A numerical boundary that leaves no room for debate (e.g. maximum 5% of portfolio equity, 2-day blackout buffer, 1.5% maximum daily loss).\n3. The Verifiable Observable: An auditable data source that proves whether the rule was followed (e.g. end-of-day broker ledger, timestamped trading journal, pre-clearance ticket).\n\nContrast two statements: 'I will manage portfolio risk carefully' versus 'I will never allocate more than 5% of portfolio equity to any single position, verified against the daily broker account statement.' The first statement is an unmeasurable aspiration; the second is an auditable control.\n\nFinally, adopt the foundational rule of trading discipline: A profitable breach is still a breach. If you violate your charter by taking an oversized position and happen to make a profit, you have not succeeded; you have made an operational error that happened to get lucky. Justifying rule violations because of positive outcomes destroys discipline and inevitably leads to catastrophic ruin.",
        "Consider a fictional proprietary trader managing Rp400,000,000 in equity. The trader establishes a personal trading charter with three clear rules:\n1. Maximum single position limit of 5.0% of portfolio equity, verified against the broker position report.\n2. Maximum daily loss limit of 1.5% of equity, verified against the daily profit-and-loss file.\n3. No personal trading in any security under active execution by the firm's trading desk.\n\nStep-by-step arithmetic:\n1. Maximum allowable position size: 0.05 x Rp400,000,000 = Rp20,000,000.\n2. Maximum daily loss limit: 0.015 x Rp400,000,000 = Rp6,000,000.\n\nEvaluating a breach scenario:\nDuring a fast-moving trading session, the trader spots an attractive breakout and takes a position worth Rp26,000,000—exceeding the position limit by Rp6,000,000 (a 30% breach). By the end of the day, the position rallies, generating a net profit of Rp3,000,000.\n\nThe charter protocol:\nUnder the charter's predetermined rules, the trader must:\n1. Formally record the breach in the trading log: Rp26,000,000 taken versus Rp20,000,000 permitted.\n2. Immediately reduce the position back to the Rp20,000,000 threshold.\n3. Refuse to adjust or relax the 5% limit simply because the trade was profitable. Celebrating a profitable rule breach reinforces dangerous habits that lead to severe losses on the next breach.",
        "Draft between six and ten charter rules, each formatted with a behavior, a numerical threshold, and a verifiable check, and review compliance on a recurring schedule.\n\n### Do and do not\n\n- **Do** format every charter rule with a specific behavior, a numerical threshold, and an auditable check.\n- **Do** decide in advance exactly what corrective actions a rule breach requires before entering live positions.\n- **Do not** modify or relax a charter rule immediately after it causes a loss or after an undisciplined breach results in a profit.\n- **Do not** write vague, subjective aspirations that cannot be independently audited by another person.",
        r"\text{limit}_i = w_i\cdot E,\qquad \text{breach} \iff \text{position} > \text{limit}_i",
        'equity = 400_000_000\nposition_cap = 0.05\ndaily_cap = 0.015\ntaken = 26_000_000\nlimit = equity * position_cap\nprint("Position limit:", limit)\nprint("Daily loss limit:", equity * daily_cap)\nprint("Breach:", taken > limit, "by", taken - limit)',
        "Compute the position and daily loss limits, quantify the breach, and write three charter rules of your own in the behaviour-threshold-observable form.",
        "The position limit is Rp20,000,000 and the daily loss limit is Rp6,000,000; the actual trade breached the position limit by Rp6,000,000 (Rp26,000,000 taken vs Rp20,000,000 allowed). Three examples of robust charter rules in behavior-threshold-observable form are: (1) Position Sizing: 'I will not allocate more than 5.0% of portfolio equity to any single position, verified daily against the broker statement.' (2) Loss Control: 'I will halt all trading for the day if cumulative losses reach 1.5% of equity, verified in the real-time P&L monitor.' (3) Research Rigor: 'I will document an investment thesis and risk-reward calculation before submitting any entry order, verified by a timestamped entry in my trading journal.'",
        [
            (
                "A charter rule is checkable when it specifies:",
                "A behaviour, a threshold and an observable that shows compliance",
                "A general intention to act prudently",
                "A target return and a time horizon",
                "A checkable rule defines the specific action, a quantitative threshold, and an auditable data source to verify compliance.",
            ),
            (
                "On 400,000,000 of equity, a 5% position limit is:",
                "20,000,000",
                "5,000,000",
                "40,000,000",
                "0.05 multiplied by Rp400,000,000 equals exactly Rp20,000,000.",
            ),
            (
                "A breach of the position limit that turned out profitable should be:",
                "Recorded and corrected, because the outcome does not amend the rule",
                "Left alone, since no harm resulted",
                "Used to raise the limit to the size that worked",
                "Outcome bias must be rejected; a profitable breach is still an operational violation and must be documented and corrected.",
            ),
            (
                "The best time to write a charter is:",
                "Before the situation arises, when no position is at stake",
                "During a drawdown, when the risks are vivid",
                "After a profitable run, when confidence is high",
                "Pre-commitment before entering market positions ensures that rules are formulated with objectivity rather than fear or greed.",
            ),
        ],
        [CFA_CODE, HONOR, REG_BI],
    )

    track = finish(
        {
            "id": "trading-ethics",
            "number": 12,
            "title": "Trading ethics & market conduct",
            "description": "Master duties of loyalty, resolve conflicts of interest, protect market integrity against manipulation, and build your own auditable personal trading charter.",
            "source": "Original Quanta course · CFA Institute, SEC, FINRA, ESMA & GIPS primary references",
            "level": "Foundational",
            "icon": "book",
            "studyType": "applied",
            "modules": modules,
            "prerequisites": "Complete Trading & market fundamentals, or understand shares, orders, fees and returns. No coding experience is required; the worksheets are short arithmetic. This course is education, not legal or compliance advice, and the obligations that apply to you depend on your jurisdiction, licence and role.",
            "outcomes": [
                "Name whose interest a decision serves and rank interests explicitly when they conflict.",
                "Decide what is material, disclose it before the action it informs, and quantify the cost of an incentive.",
                "Classify information by materiality and availability, and identify manipulative order patterns from measurable evidence.",
                "Specify the pre-trade controls, named accountability and review an automated strategy requires.",
                "Report a research result together with the search that produced it, and present performance net of costs with its limitations.",
                "Separate a client's risk capacity from their tolerance, refuse an instruction that fails arithmetic or authority, and escalate in writing.",
                "Produce a personal trading charter whose rules each carry a threshold and a check.",
            ],
            "readingGuide": "16 lessons x 30 minutes = 8 hours of planned study across four units; exam time is additional. Includes 32 practice questions, four four-question checkpoints and a 16-question final. Every firm, person, price and amount in the scenarios is invented, including the Indonesian rupiah figures. The linked rules and standards are real primary sources, cited for the principle being described rather than as claims about any case in this course. Obligations differ by jurisdiction, licence and role; treat this as education and check your own regulator's rules before acting.",
            "parts": [
                {"id": str(i), "title": t, "description": d} for i, (t, d) in enumerate(PARTS, 1)
            ],
            "references": [
                {"title": t, "url": u}
                for t, u in [CFA_CODE, REG_BI, INSIDER, BEST_EX, QUOTES, MARKET_ABUSE, GIPS, WHISTLE]
            ],
        },
        checkpoints_for(modules, PARTS, 4),
    )
    track["exams"][-1]["version"] = 1
    return track
