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
        "State whose interest a decision serves and rank the interests when they conflict.",
        "Every trading decision is made on behalf of someone: yourself, a client, an employer, or a fund's investors. Ethics in trading begins by naming that person, because the same transaction can be proper for one principal and improper for another. A duty of loyalty means placing the principal's interest ahead of your own, and placing the client's interest ahead of the firm's where the two diverge. CFA Institute's Code of Ethics expresses this as acting for the benefit of clients and placing their interests before your own; Regulation Best Interest expresses a related obligation for broker-dealers making recommendations to retail customers.\n\nThe difficulty is rarely identifying a blatant theft. It is noticing the ordinary decision where your interest quietly enters: the fund you are paid more to sell, the trade that helps your quarter, the position you already hold. Loyalty is not a feeling; it is an ordering you can write down and check afterwards.",
        "A fictional adviser can place a client in Fund A, which charges 0.20% a year and pays the adviser nothing, or Fund B, which charges 1.20% a year and pays the adviser 0.40%. On Rp500,000,000 invested, the annual cost difference is Rp5,000,000, and the adviser receives Rp2,000,000 only in the second case. Nothing about that arithmetic decides which fund suits the client, but it does identify exactly where the adviser's interest and the client's diverge, and it is the number the client is entitled to understand.",
        "Name the principal before you name the trade. Write the decision as a sentence with a subject: *I am buying this for X, whose objective is Y.* When two principals conflict, record which one you ranked first and why.\n\n### Do and do not\n\n- **Do** state the principal and the objective in writing before you act.\n- **Do** rank interests explicitly when they conflict, and keep the reasoning.\n- **Do not** rely on a recommendation being defensible; check whether it is the one you would make if you were paid identically either way.\n- **Do not** treat an undisclosed benefit to yourself as harmless because the client also did well.",
        r"\Delta\text{cost} = (f_B - f_A)\times V,\qquad \text{adviser benefit} = r\times V",
        'value = 500_000_000\nprint("Annual cost difference:", (0.012 - 0.002) * value)\nprint("Adviser benefit from the costlier fund:", 0.004 * value)',
        "For the two fictional funds above, calculate the annual cost difference to the client and the adviser's benefit. Then write the one sentence the adviser owes the client before the recommendation is made.",
        "The cost difference is Rp5,000,000 a year and the adviser's benefit is Rp2,000,000. The owed sentence names the payment, its size, and that a cheaper alternative exists, so the client can weigh the recommendation knowing what the adviser gains. The arithmetic does not by itself prove Fund B unsuitable; it proves the conflict must be disclosed.",
        [
            (
                "A duty of loyalty in this course means:",
                "Placing the principal's interest ahead of your own, in a written order",
                "Never charging a fee for advice",
                "Avoiding every transaction that could lose money",
                "Loyalty is an ordering of interests that can be recorded and reviewed, not a promise of profit.",
            ),
            (
                "On 500,000,000 invested, fees of 1.20% versus 0.20% differ annually by:",
                "5,000,000",
                "500,000",
                "10,000,000",
                "The difference is one percentage point: 0.01 x 500,000,000 = 5,000,000.",
            ),
            (
                "A recommendation pays the adviser more and also suits the client. The conflict:",
                "Still requires disclosure, because the client cannot weigh what they cannot see",
                "Disappears, because the outcome was good for the client",
                "Is resolved by the adviser's confidence in the product",
                "Suitability and disclosure are separate obligations; a good outcome does not retire the second.",
            ),
            (
                "The most useful first step when two principals' interests conflict is:",
                "Write down which interest you ranked first and the reason",
                "Choose whichever trade is larger",
                "Postpone the decision until prices move",
                "An explicit, recorded ranking is what allows the decision to be reviewed later.",
            ),
        ],
        [CFA_CODE, REG_BI, FEES],
    )

    add(
        "Conflicts you must disclose before you act",
        "Disclosure, materiality and timing",
        "Decide what to disclose, to whom, and before which action.",
        "Disclosure converts a hidden conflict into an informed decision by someone else. Three questions decide it: what is the conflict, is it material, and when must the other party know. Materiality is not a fixed percentage. A useful working test is whether a reasonable person would want the fact in hand before deciding, and the standards ask you to disclose all matters that could reasonably be expected to impair independence or objectivity.\n\nTiming is where disclosure usually fails. A conflict revealed after the trade cannot inform the decision it affected, and a disclosure buried in a document nobody reads is closer to concealment than to candour. Prominence, plainness and timing are part of the obligation, not presentation preferences. Company reporting works the same way: a filing's notes often carry the scope of an issue that a headline figure hides, which is why an analyst reads the notes.",
        "A fictional research analyst holds shares in Pelita Manufaktur and is about to publish a positive note. The holding is Rp60,000,000 against personal investable assets of Rp400,000,000, so it is 15% of their portfolio. Whether that is material to the reader does not depend on it being large to the firm; it depends on whether a reader weighing the note would want to know the author owns the share. Disclosing it in the note's first screen informs the reader; disclosing it in an appendix published a week later does not.",
        "Disclose before the action the disclosure is meant to inform, in the same document, in plain language.\n\n### Do and do not\n\n- **Do** apply the reasonable-person test to materiality rather than a private threshold.\n- **Do** put the disclosure where the decision is made, not in a separate document.\n- **Do not** use volume as camouflage; a page of boilerplate that hides one relevant fact fails the purpose.\n- **Do not** disclose after the fact and call it transparency.",
        r"w = \frac{\text{holding}}{\text{personal portfolio}},\qquad \text{disclose if a reasonable reader would want }w",
        'holding = 60_000_000\nportfolio = 400_000_000\nprint("Share of personal portfolio:", round(holding / portfolio, 4))',
        "Calculate the analyst's portfolio weight, then write the disclosure sentence and state exactly where and when it must appear.",
        "The weight is 0.15, or 15%. The disclosure names the holding and the interest, appears in the published note itself at first read rather than an appendix, and is dated before or with publication. A later appendix cannot inform a reader who already acted.",
        [
            (
                "Materiality for disclosure is best tested by:",
                "Whether a reasonable person would want the fact before deciding",
                "Whether the amount exceeds one million rupiah",
                "Whether the firm's lawyers have previously objected",
                "The reasonable-person test is the workable standard; a fixed private threshold is not.",
            ),
            (
                "A holding of 60,000,000 in a personal portfolio of 400,000,000 is:",
                "15%",
                "6.7%",
                "1.5%",
                "60,000,000 / 400,000,000 = 0.15.",
            ),
            (
                "A conflict disclosed a week after the research note was published:",
                "Failed its purpose, because it could not inform the decision it affected",
                "Satisfies the obligation, since it was eventually disclosed",
                "Is adequate if the note later proved accurate",
                "Disclosure must precede or accompany the action it is meant to inform.",
            ),
            (
                "Burying a relevant conflict inside lengthy boilerplate is best described as:",
                "A failure of prominence that works against the purpose of disclosing",
                "Acceptable, because the fact was technically published",
                "Required, since legal text belongs in an appendix",
                "Prominence and plain language are part of the obligation, not formatting taste.",
            ),
        ],
        [CFA_CODE, STATEMENTS, ADVERTISING],
    )

    add(
        "Costs, inducements and the incentive behind advice",
        "Compensation arrangements and total cost",
        "Trace how a payment arrangement reaches a recommendation, and quantify its cost to the investor.",
        "An inducement is any benefit that could influence a recommendation: commission, a revenue share, a platform payment, research paid for by order flow, a sales target, hospitality. The ethical problem is not that money exists; it is that the person acting on the recommendation cannot see the arrangement and therefore cannot discount it. Fee disclosure exists because small recurring percentages compound into large amounts that investors routinely underestimate.\n\nThe practical discipline is to compute total cost of ownership rather than compare headline rates. Add the ongoing charge, the transaction costs you cause by trading, and any spread or platform fee, then express the total in money over a realistic holding period. A small business owner understands this instinctively: sales are not cash, and an obligation you have not written down still has to be paid.",
        "A fictional portfolio of Rp250,000,000 is charged 0.9% a year, turns over twice a year at a round-trip cost of 0.3%, and pays a Rp600,000 annual platform fee. The ongoing charge is Rp2,250,000, the trading cost is 2 x 0.003 x 250,000,000 = Rp1,500,000, and the platform fee is Rp600,000: Rp4,350,000 in total, or 1.74% of the portfolio. A recommendation that raises turnover to four times a year adds another Rp1,500,000 without changing the headline fee at all.",
        "Quote costs in money over a holding period, not in basis points in isolation. Separate the costs the investor chose from the costs your activity creates.\n\n### Do and do not\n\n- **Do** total the ongoing charge, the trading cost and the platform fee before comparing products.\n- **Do** state who receives each payment.\n- **Do not** describe a recommendation as free because the fee is deducted rather than invoiced.\n- **Do not** increase turnover without being able to show the expected benefit exceeds the cost you just added.",
        r"C = f\cdot V + n\cdot c\cdot V + F",
        'value = 250_000_000\nfee = 0.009\nturns = 2\nround_trip = 0.003\nplatform = 600_000\ntotal = fee * value + turns * round_trip * value + platform\nprint("Total annual cost:", total)\nprint("As a share of the portfolio:", round(total / value, 4))',
        "Compute the total annual cost above in money and as a percentage, then recompute it with turnover of four times a year and state what the adviser must be able to show.",
        "The total is Rp4,350,000, or 1.74%. At four turns it becomes Rp5,850,000, or 2.34%. The adviser must be able to show an expected benefit larger than the Rp1,500,000 of added cost, evaluated before the trades rather than justified afterwards by whichever outcome occurred.",
        [
            (
                "Total cost of ownership in this lesson includes:",
                "Ongoing charge, trading costs caused by turnover, and platform fees",
                "Only the headline annual management fee",
                "Only the costs the investor pays by separate invoice",
                "Costs deducted from assets and costs created by trading both reduce the investor's outcome.",
            ),
            (
                "On 250,000,000, a 0.9% charge plus two round trips at 0.3% plus 600,000 totals:",
                "4,350,000",
                "2,850,000",
                "3,750,000",
                "2,250,000 + 1,500,000 + 600,000 = 4,350,000.",
            ),
            (
                "Doubling turnover while leaving the management fee unchanged:",
                "Raises the investor's total cost even though the headline rate did not move",
                "Has no cost effect, since the fee is what the investor agreed to",
                "Reduces cost by spreading it over more transactions",
                "Trading costs scale with turnover and are borne by the investor regardless of the headline fee.",
            ),
            (
                "Calling advice 'free' because the fee is deducted from assets is:",
                "Misleading, since the cost is borne by the investor either way",
                "Accurate, because no invoice is issued",
                "Acceptable if the product outperformed",
                "A deducted cost is still a cost; the description misstates what the investor pays.",
            ),
        ],
        [FEES, REG_BI, CFA_CODE],
    )

    add(
        "Personal trading and client priority",
        "Front-running, allocation and blackout windows",
        "Apply a priority rule that keeps personal and firm trading behind client trading.",
        "Priority of transactions means client orders come first, employer orders next, and personal orders last. The rule exists because the person who knows an order is coming can profit from the price effect of that order, and that profit is taken from the principal whose order caused it. Trading ahead of a client is the clearest case, but allocating the better fills to a personal account, or a favoured account, is the same wrong with better manners.\n\nControls that work are procedural rather than attitudinal: pre-clearance of personal trades, blackout windows around client activity and research publication, average-price allocation across accounts, and a reviewable record of who received which fill. Pre-committed trading arrangements are the same idea applied to insiders: a schedule fixed in advance, with a waiting period before the first trade, limits the discretion that knowledge could otherwise exploit.",
        "A fictional desk will buy 400,000 shares of Cendana Logistik over two days. An analyst buys 5,000 shares for a personal account the previous afternoon. Whether the personal trade 'moved the price' is not the test, and neither is its small size. The analyst acquired a position using knowledge of a client order that the client's own execution will then help to revalue, and the firm cannot show the client received unaffected execution. Under a blackout window of two business days either side of client activity, the trade would simply not have been permitted.",
        "Write the priority ordering, then give it a mechanism: pre-clearance, a blackout window, and allocation by average price.\n\n### Do and do not\n\n- **Do** pre-clear personal trades in any security your desk or research covers.\n- **Do** allocate partial fills by a rule fixed before the order, and keep the record.\n- **Do not** trade personally inside a blackout window, however small the size.\n- **Do not** treat a favourable personal outcome as evidence the timing was coincidental.",
        r"\text{blackout} = [t_{\text{order}} - d,\; t_{\text{complete}} + d],\qquad \text{personal trades prohibited in the window}",
        'client_days = 2\nbuffer = 2\nprint("Blackout length in business days:", client_days + 2 * buffer)\nprint("Personal orders inside the window:", "not permitted")',
        "State the priority ordering, compute the blackout length for the two-day client order with a two-day buffer, and explain why the personal trade's small size does not settle the question.",
        "Clients first, employer second, personal last. The window spans six business days: two days of client activity plus two on each side. Size is not the test, because the objection is to acquiring a position using knowledge of a pending client order and to the firm's inability to show unaffected client execution.",
        [
            (
                "The priority of transactions ordering is:",
                "Clients, then employer, then personal accounts",
                "Personal accounts, then clients, then employer",
                "Whichever order was entered into the system first",
                "Client interests rank first; personal transactions rank last.",
            ),
            (
                "A two-day client order with a two-day buffer on each side implies a blackout of:",
                "6 business days",
                "4 business days",
                "2 business days",
                "2 + 2 + 2 = 6 business days.",
            ),
            (
                "A small personal trade placed just before a large client order is objectionable because:",
                "It uses knowledge of a pending client order, regardless of its size",
                "Small trades are always prohibited",
                "It reduces the firm's commission income",
                "The wrong is the use of the order information, not the size of the resulting position.",
            ),
            (
                "Allocating the better fills to one account after seeing the prices is:",
                "A breach of fair dealing, even if every account received something",
                "Acceptable where all accounts had the same strategy",
                "Required, so the largest account is not disadvantaged",
                "Allocation must follow a rule fixed before the outcome is known.",
            ),
        ],
        [CFA_CODE, PLANS, HONOR],
    )

    # ---------------------------------------------------------------- Unit 2
    add(
        "Material non-public information",
        "Inside information and the duty not to trade",
        "Classify information by materiality and availability, and choose the action each combination requires.",
        "Two independent tests decide whether information restricts you. Is it material, meaning a reasonable investor would likely consider it important in deciding to buy or sell? Is it non-public, meaning it has not been broadly disseminated so the market has had a chance to absorb it? Information that is both material and non-public must not be traded on and must not be passed to someone who will trade, whatever the route by which you learned it.\n\nThe common failures are quiet ones: an overheard remark, a file left open, a supplier who mentions a cancelled order, a friend at the company. Selective disclosure is the mirror image, where an issuer tells some investors before others. Analysts work legitimately by assembling many non-material public and non-public pieces into a material conclusion. That mosaic is your own work; a single material non-public fact is not.",
        "A fictional analyst learns from a supplier's driver that Pelita Manufaktur has halted a production line, four days before the company says anything. Prior guidance implied quarterly revenue of Rp900,000,000,000 and the halt plausibly removes Rp72,000,000,000, about 8%. A reasonable investor would consider an 8% revenue shortfall important, and nothing has been disseminated. The information is material and non-public; the analyst may not trade, may not tell the portfolio manager to trade, and should report the receipt so the firm can restrict the security.",
        "Decide materiality and availability separately, then act on the combination. Only public information, or your own mosaic of non-material pieces, supports a trade.\n\n### Do and do not\n\n- **Do** report inadvertent receipt immediately so the security can be restricted.\n- **Do** keep a record of how you learned each significant fact.\n- **Do not** trade, tip, or recommend while holding material non-public information.\n- **Do not** assume a fact is public because it circulated among a few people.",
        r"\text{restricted} \iff \text{material} \wedge \neg\text{public},\qquad m=\frac{\Delta R}{R}",
        'revenue = 900_000_000_000\nlost = 72_000_000_000\nprint("Revenue effect:", round(lost / revenue, 4))\nprint("Status:", "material and non-public, restricted")',
        "Compute the revenue effect, classify the information on both tests, and list the three actions the analyst must take.",
        "The effect is 0.08, or 8%, which a reasonable investor would likely consider important, and it has not been disseminated, so the information is material and non-public. The analyst does not trade, does not pass it on, and reports the receipt so compliance can restrict the security and record the event.",
        [
            (
                "Information is restricted when it is:",
                "Both material and not yet broadly disseminated",
                "Material, whether or not it is public",
                "Non-public, whether or not it is material",
                "Both tests must be satisfied; each alone is insufficient.",
            ),
            (
                "A halt removing 72bn of 900bn of expected quarterly revenue is a shortfall of:",
                "8%",
                "12.5%",
                "0.8%",
                "72 / 900 = 0.08.",
            ),
            (
                "Assembling many non-material public and non-public pieces into a material conclusion is:",
                "Legitimate analysis, because the conclusion is the analyst's own work",
                "Prohibited, because the conclusion is material",
                "Permitted only after the issuer approves the conclusion",
                "The mosaic is the analyst's product; the prohibition attaches to a single material non-public fact.",
            ),
            (
                "On inadvertently receiving inside information, the correct first step is:",
                "Report it so the firm can restrict the security and record the event",
                "Trade quickly before the information spreads",
                "Wait to see whether the price moves on its own",
                "Prompt reporting lets the firm restrict trading and preserves a record of the receipt.",
            ),
        ],
        [INSIDER, MARKET_ABUSE, CFA_CODE],
    )

    add(
        "Quotations that are not bona fide",
        "Spoofing, layering, wash trades and painting the tape",
        "Identify manipulative order patterns and the evidence that distinguishes them from ordinary trading.",
        "A price is information only if the orders behind it are genuine. Manipulation is conduct that makes the order book say something false: entering orders you intend to cancel in order to move the displayed price, trading with yourself to create the appearance of volume, or transacting at the close to mark a valuation. The rule that quotations must be bona fide is the compact statement of the principle, and the prohibition on manipulative and deceptive devices sits behind it.\n\nIntent distinguishes manipulation from ordinary trading, and intent is inferred from patterns you can measure. An order-to-trade ratio far above a desk's norm, cancellations clustered immediately after an opposite-side execution, repeated activity concentrated in the closing auction, or trades between accounts under common control are the signatures supervision looks for. None is conclusive alone, which is why the record of intent, instruction and system behaviour matters so much.",
        "A fictional account enters 950 orders on one side of Cendana Logistik in an hour and executes 15, giving an order-to-trade ratio of about 63 against a desk norm near 6. Ninety per cent of the cancellations occur within two seconds of an execution on the opposite side. Neither number proves intent by itself; a genuine market maker can also cancel heavily. Together with the one-sided placement and the timing, they form the pattern a supervisor must investigate and the trader must be able to explain.",
        "Measure the pattern before arguing about intent, and keep the evidence that explains your own activity.\n\n### Do and do not\n\n- **Do** monitor order-to-trade ratios and cancellation timing against your own baseline.\n- **Do** record the purpose of an automated quoting strategy before deploying it.\n- **Do not** enter orders you do not intend to execute in order to influence a displayed price.\n- **Do not** transact with yourself, or arrange matched trades, to create an impression of volume.",
        r"\text{OTR}=\frac{\text{orders entered}}{\text{orders executed}}",
        'orders = 950\nexecuted = 15\nnorm = 6\nratio = orders / executed\nprint("Order-to-trade ratio:", round(ratio, 1))\nprint("Multiple of the desk norm:", round(ratio / norm, 1))',
        "Compute the order-to-trade ratio and its multiple of the desk norm, then state what the numbers do and do not establish.",
        "The ratio is about 63, roughly ten times the desk norm of 6. The numbers establish an outlier worth investigating and a pattern consistent with layering, but not intent by themselves; the trader's recorded purpose, the strategy's specification and the cancellation timing carry that question.",
        [
            (
                "Manipulation is best described as conduct that:",
                "Makes the order book or tape convey something false",
                "Results in a loss for the other side of a trade",
                "Uses an automated system rather than manual orders",
                "The wrong is the false impression created, not automation or the counterparty's outcome.",
            ),
            (
                "950 orders entered and 15 executed gives an order-to-trade ratio of about:",
                "63",
                "6.3",
                "16",
                "950 / 15 is approximately 63.",
            ),
            (
                "A high order-to-trade ratio on its own:",
                "Identifies an outlier to investigate, not proof of intent",
                "Establishes manipulation without further evidence",
                "Is irrelevant to any manipulation question",
                "Genuine strategies can cancel heavily; the ratio is a signal that requires explanation.",
            ),
            (
                "Two accounts under common control trading with each other to show volume is:",
                "A wash trade, because no genuine change of beneficial ownership occurs",
                "Acceptable, because both sides were willing",
                "Permitted if the price used is the prevailing market price",
                "Transactions without a real change in beneficial ownership create a false impression of activity.",
            ),
        ],
        [QUOTES, DECEPTIVE, MARKET_ABUSE],
    )

    add(
        "Promotion, rumour and the pump-and-dump",
        "Communications, verification and the promoted security",
        "Evaluate a promotional claim and identify who benefits from the resulting demand.",
        "A promotional campaign creates demand that someone then sells into. The pattern is old and its arithmetic is unkind: a thinly traded security is promoted, buyers arrive, the promoter's existing stock is sold into that demand, and the price returns to where the business justifies. The people who bought last carry the loss. Rules on communications with the public exist because a statement to investors is an inducement to act, and it must be fair, balanced and not omit what would make it misleading.\n\nApply the same standard to your own communications. Sharing a position publicly is not wrong, but doing so while intending to sell into the response is. The practical questions are who benefits from the demand this message creates, what the message omits, and whether the claimed return is plausible against the business's economics rather than against the sender's confidence.",
        "A fictional group promotes Nusantara Digital at Rp200, claiming a Rp1,200 target. Average daily volume is Rp400,000,000 and the promoters hold Rp15,000,000,000 of stock, which is 37.5 days of average volume. Selling that holding without moving the price is arithmetically implausible; the promotion exists to create the demand that makes an exit possible. The target figure is the least informative part of the message, and the holding and the volume are the most.",
        "Ask who is selling into the demand a message creates, then test the claim against the business rather than the promoter's confidence.\n\n### Do and do not\n\n- **Do** find out the promoter's holding and the security's normal traded volume before acting.\n- **Do** state your own position and your intent when you discuss a security publicly.\n- **Do not** repeat a claim you have not verified, even as a question or a rumour.\n- **Do not** publish a view while planning to trade against the response it creates.",
        r"\text{days of volume} = \frac{\text{promoter holding}}{\text{average daily volume}}",
        'holding = 15_000_000_000\nadv = 400_000_000\nprint("Days of average volume to exit:", round(holding / adv, 1))',
        "Compute how many days of average volume the promoters' holding represents, and explain what that implies about the purpose of the campaign.",
        "The holding is 37.5 days of average volume. Exiting a position that size without creating demand would move the price heavily against the seller, so the campaign's function is to manufacture the buyers needed for that exit. The price target is unverifiable; the holding and volume are checkable facts.",
        [
            (
                "In a pump-and-dump, the loss is generally borne by:",
                "The investors who bought into the promoted demand last",
                "The promoter, who must hold through the decline",
                "The exchange that listed the security",
                "The promoter sells into demand created by the campaign; late buyers hold the position as it falls.",
            ),
            (
                "A 15,000,000,000 holding against 400,000,000 average daily volume equals:",
                "37.5 days of volume",
                "3.75 days of volume",
                "375 days of volume",
                "15,000,000,000 / 400,000,000 = 37.5.",
            ),
            (
                "Repeating an unverified claim framed as a question is:",
                "Still a communication that induces action and must meet the same standard",
                "Acceptable, because a question asserts nothing",
                "Only a problem if the sender holds the security",
                "Framing does not change the effect on a reader or the obligation not to mislead.",
            ),
            (
                "The most checkable element of a promotional message is usually:",
                "The promoter's holding and the security's traded volume",
                "The price target",
                "The confidence of the person sending it",
                "Holdings and volume are verifiable facts; a target is an unverifiable forecast.",
            ),
        ],
        [ADVERTISING, FRAUD, DECEPTIVE],
    )

    add(
        "Best execution and order handling",
        "Reasonable diligence, routing and the customer's result",
        "Evaluate an execution against the alternatives available at the time, using cost rather than price alone.",
        "Best execution is an obligation of diligence, not a guarantee of the best possible price. The requirement is to use reasonable diligence to establish the best market for a security and to trade there so that the resulting price is as favourable as possible under prevailing conditions, judged on factors including the character of the market, the size of the order and the accessibility of quotations. Because outcomes are noisy, the obligation is discharged through a reviewable process and periodic comparison of execution quality, not by a good fill on one order.\n\nThe measure that makes this concrete is implementation shortfall: compare the average price achieved against the price at the moment the decision was made, and include commissions and fees. Routing arrangements that pay the firm are precisely where diligence must be documented, because the incentive runs against the customer's result.",
        "A fictional order to buy 20,000 shares is decided when the price is Rp1,000. It fills at an average of Rp1,004 and pays Rp150,000 in commission. The price slippage is Rp80,000 and total shortfall is Rp230,000, which is 1.15% of the Rp20,000,000 decision value. Whether that is good depends on the alternatives at the time: the displayed size, the spread, and how a more patient schedule would have traded against the risk of the price moving away.",
        "Measure the result against the decision price including costs, then review routing regularly rather than order by order.\n\n### Do and do not\n\n- **Do** record the decision price and time so execution can be measured afterwards.\n- **Do** review execution quality across venues on a schedule, and keep the comparison.\n- **Do not** treat a payment for order flow as neutral; document why the routing still served the customer.\n- **Do not** judge diligence by a single favourable fill.",
        r"\text{IS} = q\,(\bar{P}_{\text{exec}} - P_{\text{decision}}) + \text{fees}",
        'quantity = 20_000\ndecision = 1_000\nexecuted = 1_004\nfees = 150_000\nslippage = quantity * (executed - decision)\nprint("Price slippage:", slippage)\nprint("Total shortfall:", slippage + fees)\nprint("As a share of decision value:", round((slippage + fees) / (quantity * decision), 4))',
        "Compute the slippage, the total implementation shortfall and its percentage of decision value, then state what evidence would show the obligation was met.",
        "Slippage is Rp80,000, total shortfall Rp230,000, and 1.15% of the Rp20,000,000 decision value. Meeting the obligation is shown by the recorded decision price, the venues considered and why the chosen route was reasonable given displayed size and spread, plus a periodic review across many orders rather than this one.",
        [
            (
                "Best execution requires:",
                "Reasonable diligence to obtain the most favourable terms under prevailing conditions",
                "Achieving the lowest price printed that day",
                "Routing every order to the venue paying the firm the most",
                "The obligation is one of diligence and process, judged against conditions at the time.",
            ),
            (
                "Buying 20,000 shares at an average of 1,004 after a decision price of 1,000 slips by:",
                "80,000",
                "20,000",
                "150,000",
                "20,000 x 4 = 80,000 before commissions.",
            ),
            (
                "Implementation shortfall is measured against:",
                "The price when the decision was made, including costs",
                "The day's closing price only",
                "The best price printed at any point in the session",
                "The decision price is the benchmark, and costs form part of the shortfall.",
            ),
            (
                "A routing arrangement that pays the firm:",
                "Requires documented evidence that the customer's result was still served",
                "Is prohibited in all circumstances",
                "Needs no review if customers do not complain",
                "The incentive runs against the customer, so the diligence behind the routing must be evidenced.",
            ),
        ],
        [BEST_EX, REG_BI, SUPERVISION],
    )

    # ---------------------------------------------------------------- Unit 3
    add(
        "Accountability for a system that trades",
        "Pre-trade controls, kill switches and named owners",
        "Specify the controls and the named accountability a trading system requires before deployment.",
        "An automated system does not dilute responsibility; it concentrates it in the people who specified, deployed and supervised it. The market-access rule states the expectation plainly: a firm with access must maintain risk-management controls reasonably designed to manage the financial, regulatory and other risks of that access, and those controls must be under the firm's own direct and exclusive control.\n\nIn practice this means limits that reject rather than warn, applied before the order leaves: maximum order size, maximum order value, price collars against the last trade, a daily loss limit and a cumulative exposure cap. It means a kill switch a named person can operate without a deployment, and a rollback that has been rehearsed. A deployment that changes trading behaviour is a trading decision and needs the same review as one. When a system misbehaves, the question asked afterwards is who was accountable and what the control would have stopped.",
        "A fictional desk sets a maximum order value of Rp500,000,000, a price collar of 3% against the last trade, and a daily loss limit of Rp2,000,000,000. A defective release sends repeated orders of Rp90,000,000 each. The per-order controls pass every time, and only the cumulative loss limit stops the sequence, after 23 orders totalling Rp2,070,000,000. The gap is that no control counted orders per second or cumulative notional per symbol, so the limits were individually reasonable and collectively insufficient.",
        "Write each control as a rejection with a threshold and an owner, then test the case where every individual order is acceptable.\n\n### Do and do not\n\n- **Do** enforce limits pre-trade, as rejections rather than alerts.\n- **Do** name the person who can halt the system, and rehearse the halt.\n- **Do not** deploy a change that alters trading behaviour without the review a trading decision receives.\n- **Do not** rely on per-order limits alone; add rate and cumulative-exposure limits.",
        r"n^{*} = \left\lceil \frac{L}{v} \right\rceil,\qquad \text{loss limit } L,\ \text{order value } v",
        'limit = 2_000_000_000\norder = 90_000_000\ncrossing = limit // order + 1\nprint("Orders before the cumulative limit binds:", crossing)\nprint("Notional at that point:", crossing * order)',
        "Compute how many orders pass before the cumulative loss limit binds and the notional reached, then name the two controls that would have stopped the sequence sooner.",
        "Twenty-three orders pass, reaching Rp2,070,000,000. A maximum-orders-per-second rate limit and a cumulative notional-per-symbol cap would each have stopped the sequence far earlier; the per-order value limit could not, because every individual order was within it.",
        [
            (
                "Automating a strategy changes responsibility by:",
                "Concentrating it in whoever specified, deployed and supervised the system",
                "Transferring it to the software vendor",
                "Removing it, since no person entered the orders",
                "Accountability attaches to the people who built, released and supervised the system.",
            ),
            (
                "With a 2,000,000,000 loss limit and 90,000,000 orders, the limit binds after:",
                "23 orders",
                "20 orders",
                "223 orders",
                "2,000,000,000 / 90,000,000 is about 22.2, so the twenty-third order crosses the limit.",
            ),
            (
                "Per-order value limits failed here because:",
                "Every individual order was compliant while the cumulative total was not",
                "The limit was set too low",
                "The orders were entered manually",
                "Individually acceptable orders can breach a cumulative exposure that nothing was measuring.",
            ),
            (
                "A pre-trade control should:",
                "Reject the order before it reaches the market",
                "Log a warning for later review",
                "Notify the trader after the fill is received",
                "A control that only warns does not prevent the exposure it was designed to stop.",
            ),
        ],
        [MARKET_ACCESS, SUPERVISION, CFA_CODE],
    )

    add(
        "Honest backtests: search, selection and reporting",
        "Multiple testing, selective reporting and what a result supports",
        "Adjust a reported result for the size of the search that produced it.",
        "A backtest reports the best of everything you tried, but the reader usually sees only the winner. That gap is where quantitative research becomes dishonest without anyone stating a falsehood. Testing many configurations and presenting the survivor as though it were a single hypothesis overstates the evidence, and the overstatement grows with the number of trials.\n\nThe remedy is procedural and cheap. Record the number of configurations tried before you look at results, keep the rejected runs, and adjust the threshold you require for the search you actually performed. A Bonferroni-style adjustment divides the significance level by the number of trials, which is conservative but honest; the deeper point is that a result must be reported together with the search that produced it. Reserve a segment of data that no configuration has touched, and say plainly if you later looked at it.",
        "A fictional researcher tests 40 configurations and reports the best at a p-value of 0.01, describing it as significant at the 5% level. Adjusted for 40 trials, the required threshold is 0.05 / 40 = 0.00125, which the result does not meet. Under independence, the chance of at least one result below 0.05 across 40 null tests is 1 - 0.95^40, about 87%. The honest sentence is that the search produced a best result consistent with chance, not that a strategy was discovered.",
        "Report the search, not only the survivor. Fix the threshold before looking, and keep the rejected configurations.\n\n### Do and do not\n\n- **Do** record the number of configurations planned and tried, before seeing results.\n- **Do** adjust the required threshold for the number of trials, and say which adjustment you used.\n- **Do not** present the best of many trials as though it were a single pre-registered test.\n- **Do not** quietly re-use a holdout segment after a disappointing result.",
        r"\alpha^{*}=\frac{\alpha}{m},\qquad P(\text{any } p<\alpha)=1-(1-\alpha)^{m}",
        'alpha = 0.05\ntrials = 40\nreported = 0.01\nprint("Adjusted threshold:", alpha / trials)\nprint("Reported result passes:", reported < alpha / trials)\nhalf = (1 - alpha) ** 20\nprint("Chance of at least one false positive:", round(1 - half * half, 3))',
        "Compute the adjusted threshold, decide whether the reported result passes it, and calculate the probability of at least one false positive across the search. Then write the honest one-sentence conclusion.",
        "The adjusted threshold is 0.00125 and the reported 0.01 does not pass. The chance of at least one result below 0.05 across 40 independent null tests is about 0.871. The honest conclusion is that the best of forty configurations produced a result consistent with chance, so the evidence does not support deploying it.",
        [
            (
                "Reporting only the best of many tested configurations:",
                "Overstates the evidence, because the search itself is part of the result",
                "Is appropriate, since the others were rejected on merit",
                "Is acceptable whenever the winner has an economic story",
                "A result must be reported together with the search that produced it.",
            ),
            (
                "A Bonferroni-adjusted threshold at 5% across 40 trials is:",
                "0.00125",
                "0.05",
                "0.002",
                "0.05 / 40 = 0.00125.",
            ),
            (
                "Across 40 independent null tests, the chance of at least one p-value below 0.05 is about:",
                "87%",
                "5%",
                "40%",
                "1 - 0.95^40 is approximately 0.871.",
            ),
            (
                "Re-using a holdout segment after a disappointing result:",
                "Destroys its value as an untouched test and must be disclosed",
                "Is fine as long as the model is not changed afterwards",
                "Improves the estimate by adding data",
                "Once a segment informs a choice it is no longer an independent test, and the reader must be told.",
            ),
        ],
        [GIPS, CFA_CODE, HONOR],
    )

    add(
        "The data you are allowed to use",
        "Provenance, licensing and point-in-time evidence",
        "Establish whether a dataset may be used and whether it reflects what was knowable at the time.",
        "Two separate questions govern a dataset. May you use it, which is a matter of licence, terms of service and whether the information was obtained properly? And does it represent what was knowable at the time, which is a matter of vintage and revision? A dataset can be perfectly licensed and still produce a dishonest backtest because it contains values that were revised after the date they are attached to.\n\nVintage archives exist precisely to separate the latest revised value from the value published at an earlier decision date. Alternative data raises the first question sharply: information gathered by scraping a site against its terms, or containing personal data, or supplied by someone breaching their own duty of confidentiality, is not made usable by being commercially available. Record the source, the licence, the collection date and the as-of date with every field you keep.",
        "A fictional macro series shows 5.03% growth for a year, but that figure is the current revised value. The number published on the original release date was 4.86%, and a strategy that traded the day after the release could only have seen 4.86%. Using the revised figure adds 17 basis points of information that did not exist, and the error is silent: nothing in the file is wrong, it is simply attached to a date on which it was not knowable.",
        "Keep provenance with the data, and prefer the value as published at the decision date over the latest revision.\n\n### Do and do not\n\n- **Do** store the source, licence, collection time and as-of date for every series.\n- **Do** use vintage or point-in-time values when the model would have traded on the release.\n- **Do not** assume commercial availability implies a right to use, or that terms of service do not apply to you.\n- **Do not** mix a revised series into a backtest without stating that revisions are included.",
        r"\text{usable} \iff \text{licensed} \wedge \text{as\text{-}of} \le t_{\text{decision}}",
        'revised = 5.03\nas_published = 4.86\nprint("Basis points of hindsight:", round((revised - as_published) * 100, 1))\nprint("Usable at the decision date:", as_published)',
        "Compute the hindsight introduced by the revision in basis points, and list the four provenance fields you would store with the series.",
        "The revision adds 17 basis points of information unavailable on the decision date. The fields to store are the source, the licence or terms under which it may be used, the collection timestamp, and the as-of or vintage date the value belongs to.",
        [
            (
                "Whether a dataset may be used and whether it is point-in-time are:",
                "Two separate questions, and both must be answered",
                "The same question expressed differently",
                "Only relevant for paid data",
                "Licensing governs permission; vintage governs what was knowable. Either can fail alone.",
            ),
            (
                "A revised 5.03% against an originally published 4.86% differs by:",
                "17 basis points",
                "1.7 basis points",
                "0.17 basis points",
                "5.03 - 4.86 = 0.17 percentage points, which is 17 basis points.",
            ),
            (
                "Data being commercially available means:",
                "Nothing by itself about whether you are permitted to use it",
                "That any licensing question has been settled by the vendor",
                "That the data must be point-in-time",
                "Availability is not permission; terms, collection method and confidentiality duties still apply.",
            ),
            (
                "Using the latest revised value at an earlier decision date:",
                "Introduces information that did not exist then, even though no value is incorrect",
                "Is acceptable because revisions improve accuracy",
                "Only matters for high-frequency strategies",
                "The file is accurate but the value is attached to a date on which it was not knowable.",
            ),
        ],
        [STATEMENTS, CFA_CODE, GIPS],
    )

    add(
        "The claims you may make about performance",
        "Fair representation, net returns and full disclosure",
        "State a performance record so that a reader who did not build it can evaluate it.",
        "Performance presentation is where quantitative work meets the person relying on it. The principles behind the GIPS standards are fair representation and full disclosure: show the whole relevant record rather than a flattering window, state the benchmark, and present returns net of the costs an investor would actually bear. A gross-of-fee figure is not wrong, but it answers a question no investor faces.\n\nThe common failures are selection and omission. Starting the record at a convenient date, quietly dropping a discontinued account, showing simulated results beside live results without labelling which is which, or annualising a short period so it reads like a sustained rate. A record must also carry its own limitations: the sample length, the costs assumed, whether results are live or hypothetical, and the conditions under which the approach would be expected to do badly.",
        "A fictional strategy reports a 10% return over twelve months against an 8% benchmark, net of a stipulated 0.10 percentage point monthly cost. Gross of that cost the figure would be about 11.2%, and the twelve-month sample is a single observation of an annual outcome, not evidence of a sustained rate. A fair presentation gives 10% net, names the benchmark, states the 1.2 percentage points of annual cost deducted, says the record is twelve months long, and labels whether the result is live or simulated.",
        "Present the record net of costs, with its benchmark, its length, and the conditions under which it would fail.\n\n### Do and do not\n\n- **Do** report net of the costs an investor would bear, and state what was deducted.\n- **Do** label simulated results as simulated, in the same place the number appears.\n- **Do not** choose a start date that flatters the record, or drop accounts that closed.\n- **Do not** annualise a short sample into a rate that implies it can be sustained.",
        r"r_{\text{net}} = r_{\text{gross}} - \sum_{t} c_t,\qquad \text{state } n \text{ and the benchmark}",
        'monthly_cost = 0.001\nmonths = 12\nnet = 0.10\nprint("Annual cost deducted:", round(monthly_cost * months, 4))\nprint("Approximate gross return:", round(net + monthly_cost * months, 4))\nprint("Observations of an annual outcome:", 1)',
        "Compute the annual cost deducted and the approximate gross return, then write the four facts that must accompany the 10% figure.",
        "The annual cost is 1.2 percentage points and the approximate gross return is 11.2%. The 10% must be accompanied by the benchmark and its 8% result, the costs deducted, the twelve-month length of the record, and whether the result is live or simulated.",
        [
            (
                "Fair representation of performance requires:",
                "The whole relevant record, net of costs, with its benchmark and limitations",
                "The highest return the strategy achieved in any window",
                "Gross returns, so costs do not obscure the manager's skill",
                "A reader must be able to evaluate the record, which means completeness, net figures and context.",
            ),
            (
                "A 10% net return after 0.10 percentage points of monthly cost implies a gross of about:",
                "11.2%",
                "10.1%",
                "8.8%",
                "Twelve months at 0.10 points is 1.2 points, so gross is approximately 11.2%.",
            ),
            (
                "Twelve months of results represent:",
                "One observation of an annual outcome, not a sustained rate",
                "Twelve independent pieces of evidence about annual performance",
                "A sufficient sample once the return exceeds the benchmark",
                "A single year is one draw; monthly observations do not multiply the annual evidence.",
            ),
            (
                "Showing simulated results beside live results without labelling them is:",
                "An omission that makes the presentation misleading",
                "Acceptable if the simulation used the same rules",
                "Required, so the reader sees the full history",
                "The reader cannot evaluate the record without knowing which figures were actually earned.",
            ),
        ],
        [GIPS, ADVERTISING, FEES],
    )

    # ---------------------------------------------------------------- Unit 4
    add(
        "Advising another person",
        "Suitability, risk capacity and the money that cannot be lost",
        "Separate a client's willingness to take risk from their capacity to absorb a loss.",
        "Suitability has two independent inputs that are often collapsed into one. Risk tolerance is a preference: how much volatility a person is willing to experience. Risk capacity is a fact: how large a loss their circumstances can absorb without forcing a sale or failing an obligation. A client may be willing to accept a 40% decline and entirely unable to afford one, and the recommendation must respect the smaller of the two.\n\nCapacity is computed from the timing of obligations, not from a questionnaire. Money needed within the horizon of a plausible decline is not available for that risk, whatever the client's stated appetite. The liquidity dimension matters as much as the size: an institution can hold assets that are adequate on a balance sheet and still fail because it cannot convert them to cash quickly enough under stress.",
        "A fictional client holds Rp300,000,000 and needs Rp120,000,000 in eighteen months for a committed obligation. Risk capacity applies to the remaining Rp180,000,000. If the recommendation must survive a 30% decline in the risky portion without touching the committed money, the maximum risky allocation is Rp180,000,000, and a 30% fall costs Rp54,000,000, which is 18% of total assets. Willingness to accept a 40% decline does not extend capacity to the committed Rp120,000,000.",
        "Compute capacity from dated obligations first, then apply tolerance to what remains.\n\n### Do and do not\n\n- **Do** date every obligation and subtract it before sizing risk.\n- **Do** record both tolerance and capacity, and act on the smaller.\n- **Do not** let a stated appetite for risk override money that is already committed.\n- **Do not** recommend an illiquid holding for money that may be needed quickly.",
        r"K = A - L_{\text{committed}},\qquad \text{loss} = d\cdot K",
        'assets = 300_000_000\ncommitted = 120_000_000\ndecline = 0.30\ncapacity = assets - committed\nprint("Amount available for risk:", capacity)\nprint("Loss in the modelled decline:", capacity * decline)\nprint("Share of total assets:", round(capacity * decline / assets, 4))',
        "Compute the amount available for risk, the loss in the modelled decline and its share of total assets, then state why a stated 40% tolerance does not change the answer.",
        "Rp180,000,000 is available, a 30% decline costs Rp54,000,000, and that is 18% of total assets. A stated tolerance cannot extend capacity over the Rp120,000,000 committed within eighteen months, because that money must be there regardless of how the client feels about volatility.",
        [
            (
                "Risk capacity differs from risk tolerance because capacity is:",
                "A fact about circumstances, while tolerance is a preference",
                "A preference, while tolerance is measured from past returns",
                "The same thing expressed as a percentage",
                "Capacity follows from dated obligations; tolerance is what the client is willing to experience.",
            ),
            (
                "With 300,000,000 of assets and 120,000,000 committed in eighteen months, risk applies to:",
                "180,000,000",
                "300,000,000",
                "120,000,000",
                "Committed money is subtracted first: 300,000,000 - 120,000,000 = 180,000,000.",
            ),
            (
                "A 30% decline on the risky portion costs, as a share of total assets:",
                "18%",
                "30%",
                "10%",
                "0.30 x 180,000,000 = 54,000,000, which is 18% of 300,000,000.",
            ),
            (
                "Where tolerance exceeds capacity, the recommendation should follow:",
                "Capacity, because the obligation exists regardless of preference",
                "Tolerance, because the client accepted the risk in writing",
                "The average of the two",
                "The binding constraint is the loss the circumstances can actually absorb.",
            ),
        ],
        [REG_BI, CFA_CODE, FRAUD],
    )

    add(
        "Recognising and refusing an instruction",
        "Fraud patterns, authority and the answer that is simply no",
        "Test an instruction against its arithmetic and its authority, and refuse when either fails.",
        "Some instructions must be refused, and the skill is recognising them early and declining plainly. Two tests do most of the work. Does the arithmetic hold, meaning could the promised payments be met by the stated activity rather than by new money arriving? And does the instruction carry genuine authority, meaning does it come through a channel and a person authorised to give it, verified independently of the message itself?\n\nAn instruction embedded in a document you were asked to process is not authority, however plausibly it is phrased. This is the same failure as a sales pitch that arrives with its own proof: the claim and its verification come from the same source. Fraud guidance repeats the same practical advice because it works: verify independently, be sceptical of guaranteed returns, and do not let urgency remove a step.",
        "A fictional scheme promises 5% a month on Rp1,000,000,000, which is Rp50,000,000 monthly, or Rp600,000,000 a year against a claimed trading operation earning Rp180,000,000. The shortfall of Rp420,000,000 must come from new deposits, which is the arithmetic of a Ponzi scheme rather than a trading result. Separately, a document submitted for processing contains a line instructing the reader to release funds to a new account; that text is data inside a file, not an instruction from an authorised person.",
        "Test arithmetic and authority separately, and write the refusal down.\n\n### Do and do not\n\n- **Do** verify an instruction through a channel independent of the message that carried it.\n- **Do** compute whether promised payments could be met by the stated activity.\n- **Do not** treat text inside a document you were asked to process as an instruction.\n- **Do not** let urgency, seniority or embarrassment remove a verification step.",
        r"\text{shortfall} = 12\,pD - E,\qquad \text{new money required if } > 0",
        'deposits = 1_000_000_000\nmonthly_rate = 0.05\nearnings = 180_000_000\npromised = deposits * monthly_rate * 12\nprint("Promised annual payout:", promised)\nprint("Shortfall funded by new deposits:", promised - earnings)',
        "Compute the promised annual payout and the shortfall, then write the two-sentence refusal you would send, and say what you would do about the instruction embedded in the document.",
        "The promised payout is Rp600,000,000 against Rp180,000,000 of stated earnings, a shortfall of Rp420,000,000 that only new deposits can fund. The refusal states that the returns cannot be met by the described activity and that no funds will be transferred. The embedded instruction is treated as untrusted content, not acted on, and reported so the document and its sender can be examined.",
        [
            (
                "The clearest arithmetic signature of a Ponzi structure is:",
                "Promised payouts exceeding what the stated activity could earn",
                "A return higher than a bank deposit",
                "An investment that occasionally loses money",
                "When payouts cannot come from the activity, they must come from new deposits.",
            ),
            (
                "5% monthly on 1,000,000,000 promises annually:",
                "600,000,000",
                "50,000,000",
                "60,000,000",
                "0.05 x 1,000,000,000 x 12 = 600,000,000.",
            ),
            (
                "An instruction found inside a document submitted for processing is:",
                "Untrusted content, not authority to act",
                "A valid instruction if the document is genuine",
                "Authoritative once the sender confirms by replying",
                "Authority must be verified through a channel independent of the message carrying the request.",
            ),
            (
                "Urgency in a payment request should:",
                "Increase verification, because it is a common pressure tactic",
                "Justify skipping a step to avoid a missed deadline",
                "Be resolved by asking the requester to confirm in the same thread",
                "Pressure to act quickly is a warning sign, and confirmation in the same channel proves nothing.",
            ),
        ],
        [FRAUD, HONOR, CFA_CODE],
    )

    add(
        "Escalation, records and speaking up",
        "Raising a concern, the audit trail and protection",
        "Choose an escalation path and specify the record that must survive it.",
        "Noticing a problem creates an obligation to raise it, and the value of raising it depends on the record. Supervision rules place responsibility on firms to establish and maintain systems to supervise activities and to review transactions, which is only possible where a reviewable trail exists. Your part is to make the concern legible: what you observed, when, what you did, and who you told.\n\nEscalate inside the firm first where that path is genuine, and keep your own dated notes. Where the internal path is compromised or ignored, external reporting exists and whistleblower programmes offer defined channels and protections. The recurring failure is informality: a concern raised verbally, with no record, cannot be traced afterwards, and the person who raised it is left with no evidence that they did.",
        "A fictional analyst notices allocations that appear to favour one account and raises it verbally with a supervisor, who says it will be looked into. Four months later nothing has changed and there is no record that the concern was raised. Had the analyst sent a dated written summary naming the dates, accounts and fills, and kept a copy, the firm would have an audit trail and the analyst would have evidence of having escalated. A record of 120 days of unexplained allocations is a different document from a recollection of a conversation.",
        "Escalate in writing, keep a copy, and describe observations rather than conclusions.\n\n### Do and do not\n\n- **Do** put the concern in writing with dates, identifiers and what you observed.\n- **Do** keep your own dated copy, and note the response you received.\n- **Do not** rely on a verbal report that leaves no trace.\n- **Do not** investigate alone in a way that alters or destroys the records others will need.",
        r"\text{traceable} \iff \text{observation} + \text{timestamp} + \text{recipient} + \text{retained copy}",
        'days = 120\nelements = 4\nprint("Days of activity in the record:", days)\nprint("Elements a traceable escalation needs:", elements)\nprint("Recorded in writing:", "no")',
        "List the four elements that make an escalation traceable, and explain what the analyst lost by raising the concern verbally.",
        "A traceable escalation records the observation, its timestamp, the recipient, and a retained copy. Raising it verbally left no evidence that the concern existed, gave the firm no trail to supervise against, and left the analyst unable to show they had acted when the pattern continued for 120 days.",
        [
            (
                "An escalation is traceable when it records:",
                "The observation, its timestamp, the recipient and a retained copy",
                "The analyst's conclusion about who was responsible",
                "A verbal summary given to the nearest supervisor",
                "Those four elements let the concern be followed afterwards by someone else.",
            ),
            (
                "Raising a concern verbally with no record primarily costs:",
                "The evidence that the concern was ever raised",
                "The analyst's right to raise it again",
                "The firm's obligation to supervise",
                "Without a record neither the firm nor the analyst can show what happened.",
            ),
            (
                "An escalation is most useful when it describes:",
                "Observations with dates and identifiers, rather than conclusions",
                "The motive you believe explains the behaviour",
                "Only the total amount involved",
                "Observations can be checked; an attributed motive cannot, and it invites dismissal.",
            ),
            (
                "Investigating alone by altering the underlying records:",
                "Damages the evidence others will need",
                "Is the fastest way to confirm a concern",
                "Is required before escalating",
                "Preserving the record matters more than personally confirming the suspicion.",
            ),
        ],
        [SUPERVISION, WHISTLE, HONOR],
    )

    add(
        "Your written trading charter",
        "A personal code of conduct with checkable rules",
        "Assemble the course into a personal charter of rules that can be checked after the fact.",
        "A charter is the course made operational: a short written document stating what you will do, what you will not do, and how each rule can be checked. Its value comes from being written before the situation arises, because the moment of temptation is the worst moment to decide. Professional codes work the same way; they exist so that the answer is already settled when pressure is applied.\n\nA usable rule has three parts: the behaviour, the threshold, and the observable that shows whether it was followed. *I will not exceed 5% of equity in any one position* is checkable. *I will manage risk carefully* is not. Write a review cadence, decide in advance what a breach obliges you to do, and accept that a profitable breach is still a breach. Keep the charter short enough that you actually remember it.",
        "A fictional trader with Rp400,000,000 of equity sets a maximum position of 5%, a maximum daily loss of 1.5%, and a rule of no trading in a security their employer is transacting. The limits are Rp20,000,000 per position and Rp6,000,000 per day. In one week the position limit is breached once, to Rp26,000,000, and the trade was profitable. The charter's own rule applies: the breach is recorded, the position is reduced to the limit, and the profit does not amend the rule, because a rule that bends after a good outcome is not a rule.",
        "Write between six and ten rules, each with a threshold and an observable, and review them on a schedule.\n\n### Do and do not\n\n- **Do** express every rule as a behaviour, a threshold and something you can check.\n- **Do** decide in advance what a breach obliges you to do.\n- **Do not** amend a rule immediately after it costs you money, or after a breach pays.\n- **Do not** write more rules than you will actually review.",
        r"\text{limit}_i = w_i\cdot E,\qquad \text{breach} \iff \text{position} > \text{limit}_i",
        'equity = 400_000_000\nposition_cap = 0.05\ndaily_cap = 0.015\ntaken = 26_000_000\nlimit = equity * position_cap\nprint("Position limit:", limit)\nprint("Daily loss limit:", equity * daily_cap)\nprint("Breach:", taken > limit, "by", taken - limit)',
        "Compute the position and daily loss limits, quantify the breach, and write three charter rules of your own in the behaviour-threshold-observable form.",
        "The position limit is Rp20,000,000 and the daily loss limit is Rp6,000,000; the breach is Rp6,000,000 over the position limit. Good rules name the behaviour, the threshold and the check, for example: no position above 5% of equity, verified from the end-of-day position file; no personal trade in a covered security, verified against the pre-clearance log; every thesis written before entry, verified by a dated journal entry.",
        [
            (
                "A charter rule is checkable when it specifies:",
                "A behaviour, a threshold and an observable that shows compliance",
                "A general intention to act prudently",
                "A target return and a time horizon",
                "Without a threshold and an observable, the rule cannot be reviewed afterwards.",
            ),
            (
                "On 400,000,000 of equity, a 5% position limit is:",
                "20,000,000",
                "5,000,000",
                "40,000,000",
                "0.05 x 400,000,000 = 20,000,000.",
            ),
            (
                "A breach of the position limit that turned out profitable should be:",
                "Recorded and corrected, because the outcome does not amend the rule",
                "Left alone, since no harm resulted",
                "Used to raise the limit to the size that worked",
                "A rule that bends after a good outcome provides no constraint when it matters.",
            ),
            (
                "The best time to write a charter is:",
                "Before the situation arises, when no position is at stake",
                "During a drawdown, when the risks are vivid",
                "After a profitable run, when confidence is high",
                "Deciding in advance is the entire mechanism; pressure is what the charter is meant to survive.",
            ),
        ],
        [CFA_CODE, HONOR, REG_BI],
    )

    track = finish(
        {
            "id": "trading-ethics",
            "number": 12,
            "title": "Trading ethics & market conduct",
            "description": "Decide whose interest a trade serves, recognise the conduct that damages a market, and write a personal charter of trading do's and don'ts.",
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
