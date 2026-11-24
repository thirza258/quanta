"""Original standalone credential course: Conduct & Compliance Essentials.

Promoted from internal module to a standalone catalog course with its own
landing page, tailored orientation for MSME owners and junior finance staff,
comprehensive 26-question final assessment (80% pass), and verifiable certificate
with score bands (Pass / Merit / Distinction) and public QR verification.

Note: Educational and informational material only; does not constitute legal, tax,
or regulatory advice. Regulatory requirements vary across jurisdictions.
"""

from foundations import question
from conduct_compliance_part4 import get_part4_modules, get_part4_exam_questions


def build_conduct_compliance():
    # Primary regulatory citations
    CFA_CODE = "CFA Institute · Code of Ethics and Standards of Professional Conduct (https://www.cfainstitute.org/standards/professionals/code-ethics-standards)"
    REG_BI = "U.S. SEC · Regulation Best Interest (https://www.sec.gov/regulation-best-interest)"
    BEST_EX = "FINRA · Rule 5310, best execution and interpositioning (https://www.finra.org/rules-guidance/rulebooks/finra-rules/5310)"
    HONOR = "FINRA · Rule 2010, standards of commercial honor and principles of trade (https://www.finra.org/rules-guidance/rulebooks/finra-rules/2010)"
    DECEPTIVE = "FINRA · Rule 2020, use of manipulative, deceptive or other fraudulent devices (https://www.finra.org/rules-guidance/rulebooks/finra-rules/2020)"
    GIPS = "CFA Institute · GIPS standards for firms (https://www.gipsstandards.org/standards/gips-standards-for-firms/)"
    MARKET_ACCESS = "U.S. SEC · Rule 15c3-5 Market Access Rule (https://www.sec.gov/rules/final/2010/34-63241.pdf)"
    FRAUD = "U.S. SEC · Investor.gov: what you can do to avoid investment fraud (https://www.investor.gov/protect-your-investments/fraud/how-avoid-fraud/what-you-can-do-avoid-investment-fraud)"

    modules = [
        {
            "id": "26.1",
            "part": "1",
            "title": "Why conduct rules apply outside the trading floor",
            "subtitle": "How fiduciary duties, prudent client segregation, and transparency protect businesses.",
            "minutes": 25,
            "objective": "Understand how core conduct rules (fiduciary duty of loyalty, conflict disclosure, client asset ring-fencing) apply directly to MSME owners, accountants, and corporate finance staff.",
            "kind": "fundamentals",
            "formula": r"\text{Fiduciary Duty} = \text{Duty of Loyalty (Client First)} + \text{Duty of Care (Prudence \& Record)}",
            "code": (
                "# Demonstrating the mathematical cost of undisclosed conflict of interest\n"
                "client_capital = 100_000_000\n"
                "standard_fund_return = 0.08       # 8% annual return\n"
                "conflicted_fund_return = 0.06     # 6% net return (2% fee drag from distributor kickback)\n"
                "\n"
                "terminal_clean = client_capital * (1 + standard_fund_return)**5\n"
                "terminal_conflicted = client_capital * (1 + conflicted_fund_return)**5\n"
                "client_loss = terminal_clean - terminal_conflicted\n"
                "print(f'Client Outcome with Unbiased Fund: Rp {terminal_clean:,.0f}')\n"
                "print(f'Client Outcome with Conflicted Fund: Rp {terminal_conflicted:,.0f}')\n"
                "print(f'Hidden Cost of Undisclosed Conflict: Rp {client_loss:,.0f}')\n"
            ),
            "content": (
                "## The idea\n\n"
                "Many practitioners assume that 'conduct and compliance' is a niche topic reserved exclusively for Wall Street floor traders and investment bank attorneys. That assumption is dangerously false.\n\n"
                "Whether you are an MSME owner managing customer prepayments, an in-house corporate bookkeeper handling supplier invoices, or a junior analyst building valuation models, the same fundamental principles of financial conduct apply:\n\n"
                "1. **Duty of Loyalty**: Putting the principal's financial interest strictly ahead of personal profit. Never using corporate funds as a personal zero-interest piggy bank.\n"
                "2. **Prudent Ring-Fencing of Client Assets**: Client funds must never be commingled with operating capital. When a client pays a deposit for goods or services to be delivered next month, that money is subject to prudent stewardship; spending it on speculative expenses risks operational insolvency.\n"
                "3. **Material Disclosure**: Revealing rebates, commissions, and familial ties before recommending a service or transaction.\n"
                "4. **Audit Provenance**: Every financial claim or performance metric must be verifiable from independent primary sources.\n\n"
                "$$\n"
                r"\text{Compliance Boundary: Prudent Segregation} \land \text{Prominent Conflict Disclosure} \land \text{Traceable Records}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A junior finance manager at an enterprise is tasked with placing Rp500 million in short-term corporate liquidity. A bank representative offers a 2% personal referral gift card if the manager chooses a specific deposit product yielding 3.5%, while another tier-one bank offers 5.5% with zero referral incentive.\n\n"
                "Accepting the gift card violates the fundamental Duty of Loyalty. Over one year, the 2% yield difference costs the company Rp10 million in lost cash flow. In institutional finance, this constitutes an illegal undisclosed kickback; in enterprise management, it constitutes immediate grounds for termination.\n\n"
                "## Work through it yourself\n\n"
                "1. Identify every party to whom you owe a duty of financial care (clients, shareholders, employees).\n"
                "2. Audit your business for commingled accounts or undisclosed vendor referral incentives.\n"
                "3. Codify an explicit written policy: personal conflicts must be registered in writing before contracts are executed.\n\n"
                "### In the sandbox\n\n"
                "Run the script to calculate how even a small 2% undisclosed fee difference compounds over a 5-year period."
            ),
            "exercise": question(
                "Why should client prepayments and custodial funds be prudently segregated from general operational accounts?",
                [
                    "Because commercial bank maintenance fees are always lower on multiple accounts",
                    "To prevent commingling where client funds are accidentally consumed by operating expenses",
                    "Because enterprise bank accounts are legally required to be opened in identical pairs",
                ],
                1,
                "Custodial and client funds must be segregated so they cannot be accidentally consumed by general operating cash burn.",
            ),
            "exercises": [
                question(
                    "Why should client prepayments be segregated from general operational accounts?",
                    [
                        "Commercial bank account maintenance fees are substantially lower when maintaining multiple separate corporate accounts",
                        "To prevent commingling where client money is spent on general operating expenses",
                        "Business bank accounts are legally required to be opened in identical pairs across all jurisdictions",
                    ],
                    1,
                    "Segregation prevents custodial funds from being commingled or spent on general operations.",
                ),
                question(
                    "What does the fiduciary Duty of Loyalty require of an individual managing other people's money?",
                    [
                        "Prioritizing the personal financial interests or institutional bonuses of the portfolio manager over the client",
                        "Subordinating personal financial interests to the exclusive benefit of the client",
                        "Guaranteeing that all investment portfolios achieve at least a 10% annual return regardless of market downturns",
                    ],
                    1,
                    "The duty of loyalty demands placing the client's financial interests above personal profit at all times.",
                ),
            ],
            "terms": [
                {"term": "Duty of Loyalty", "definition": "The legal and ethical obligation to act solely in the best interest of the client or principal, subordinating personal interests."},
                {"term": "Commingling", "definition": "The improper mixing of client or custodial funds with the personal or operational funds of a business or fiduciary."},
            ],
            "references": [
                {"title": "CFA Institute · Code of Ethics and Standards of Professional Conduct", "url": "https://www.cfainstitute.org/standards/professionals/code-ethics-standards"},
                {"title": "U.S. SEC · Regulation Best Interest (Reg BI)", "url": "https://www.sec.gov/regulation-best-interest"},
            ],
        },
        {
            "id": "26.2",
            "part": "1",
            "title": "Agency, duty of loyalty, and client priority",
            "subtitle": "Order priority under FINRA Rules 5270 and 5320, and CFA Standard VI(B).",
            "minutes": 25,
            "objective": "Identify fiduciary agency relationships, enforce client trade priority under FINRA Rules 5270/5320, and eliminate front-running.",
            "kind": "applied-study",
            "formula": r"\text{Execution Priority: } t_{\text{client fill}} \le t_{\text{proprietary fill}} \quad \forall \text{ overlapping orders}",
            "code": (
                "# Verifying trade priority: client order must precede personal order\n"
                "orders = [\n"
                "    {'account': 'client', 'time': '10:00:01', 'qty': 1000, 'symbol': 'BBCA', 'price': 10000.0},\n"
                "    {'account': 'personal', 'time': '10:00:02', 'qty': 500, 'symbol': 'BBCA', 'price': 10005.0},\n"
                "]\n"
                "if orders[0]['account'] == 'client':\n"
                "    print('Order book audit: Client priority strictly respected.')\n"
                "    print(f'Client fill @ {orders[0][\"price\"]} preceded personal fill @ {orders[1][\"price\"]}.')\n"
                "else:\n"
                "    print('VIOLATION: Front-running detected! Personal order preceded client order.')\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "In financial markets, an agency relationship exists whenever one person (the agent) exercises discretion or provides advice regarding another person's capital (the principal). The bedrock legal requirement of agency is the **Duty of Loyalty**.\n\n"
                "Under CFA Standard VI(B), **FINRA Rule 5270** (Front Running of Block Transactions), and **FINRA Rule 5320** (Trading Ahead of Customer Market and Limit Orders), client transactions must always take precedence over personal or firm proprietary transactions. Executing a personal trade before a known client order to benefit from subsequent price impact is an illegal practice known as **front-running**.\n\n"
                "$$\n"
                r"\tau_{\text{client}} < \tau_{\text{personal}} \implies P_{\text{client}} \text{ is protected from personal front-running impact}"
                "\n$$\n\n"
                "Note that SEC Regulation Best Interest (Reg BI) governs recommendations to retail customers, while trade priority and front-running are governed by FINRA Rules 5270 and 5320 and exchange trading rules.\n\n"
                "## A worked example\n\n"
                "An advisor receives a client order to buy 50,000 shares of a mid-cap stock. Knowing this large block order will move the price up, the advisor buys 500 shares in their personal account two minutes before routing the client order.\n\n"
                "This violates FINRA Rule 5270 and CFA Standard VI(B). The advisor captured an illicit $250 personal gain while forcing the client to pay higher fill prices. The required ethical conduct is strict: personal accounts cannot trade the same security until the client order is completely filled.\n\n"
                "## Work through it yourself\n\n"
                "1. Document all accounts where you or your firm have beneficial ownership.\n"
                "2. Maintain an auditable pre-clearance log for personal trades.\n"
                "3. Ensure client orders always execute first.\n\n"
                "### In the sandbox\n\n"
                "Run the script to audit chronological order book timestamps for client priority."
            ),
            "exercise": question(
                "What is front-running in security trading under FINRA Rule 5270 and CFA Standard VI(B)?",
                [
                    "Submitting electronic orders faster than competitors to the primary exchange matching engine",
                    "Entering personal orders ahead of known, pending client orders to profit from subsequent price impact",
                    "Trading exclusively during the opening thirty minutes of the regular market session",
                ],
                1,
                "Front-running is the illegal practice of placing orders on one's own account based on advance knowledge of pending client orders.",
            ),
            "exercises": [
                question(
                    "What constitutes front-running under FINRA Rule 5270?",
                    [
                        "Executing algorithmic limit orders faster than other market participants on a national electronic exchange",
                        "Trading ahead of known, pending customer block orders to profit from price impact",
                        "Trading exclusively during the opening thirty minutes of the regular exchange trading session",
                    ],
                    1,
                    "Front-running places personal trades ahead of pending client orders to capture price movement.",
                ),
                question(
                    "Under FINRA Rule 5320 (Manning Rule), what must a broker do when holding an unexecuted customer limit order?",
                    [
                        "Trade ahead for its own account at an equal or better price without filling the customer's pending limit order",
                        "Refrain from trading for its own account at a price that would satisfy the customer order unless filling it",
                        "Cancel the customer limit order after thirty minutes of market inactivity without notifying the client",
                    ],
                    1,
                    "Rule 5320 prohibits trading ahead of customer limit orders for the firm's own account without executing the customer.",
                ),
            ],
            "terms": [
                {"term": "Front-Running (FINRA 5270)", "definition": "Entering an order for personal or firm profit based on non-public knowledge of an impending customer block transaction."},
                {"term": "Trading Ahead (FINRA 5320)", "definition": "Prohibition against a broker-dealer trading for its own account at prices that would satisfy an unexecuted customer order."},
            ],
            "references": [
                {"title": "FINRA · Rule 5270 Front Running of Block Transactions", "url": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/5270"},
                {"title": "FINRA · Rule 5320 Prohibition Against Trading Ahead of Customer Orders", "url": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/5320"},
                {"title": "CFA Institute · Standard VI(B) Priority of Transactions", "url": "https://www.cfainstitute.org/ethics-standards/codes/code-of-ethics-standards-of-professional-conduct"},
            ],
        },
        {
            "id": "26.3",
            "part": "1",
            "title": "Hidden fees and total cost of ownership",
            "subtitle": "Exposing trailer fees, kickbacks, and compounding fee drag over long horizons.",
            "minutes": 25,
            "objective": "Calculate Total Expense Ratio (TER) and uncover hidden trailer fees that dilute long-term client returns.",
            "kind": "applied-study",
            "formula": r"\text{Terminal Drag} = (1 + r - \text{TER})^T - (1 + r)^T",
            "code": (
                "# Computing compounding fee drag over 30 years\n"
                "capital = 100_000\n"
                "gross_return = 0.08\n"
                "ter_low = 0.002   # 0.2% index fund\n"
                "ter_high = 0.022  # 2.2% loaded mutual fund with trailer fee\n"
                "\n"
                "wealth_clean = capital * (1 + gross_return - ter_low)**30\n"
                "wealth_loaded = capital * (1 + gross_return - ter_high)**30\n"
                "fee_drag_lost = wealth_clean - wealth_loaded\n"
                "print(f'Terminal Wealth (0.2% fee): ${wealth_clean:,.0f}')\n"
                "print(f'Terminal Wealth (2.2% fee): ${wealth_loaded:,.0f}')\n"
                "print(f'Wealth Lost to Compounding Fees: ${fee_drag_lost:,.0f}')\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "A small 2% annual fee sounds trivial when presented verbally. Over a 30-year investing horizon, however, a 2% fee drag consumes **about 43% of your total lifetime accumulated wealth** due to the loss of compounding returns.\n\n"
                "Fiduciary duty requires full disclosure of all direct and indirect compensation:\n"
                "- Management fees and performance fees.\n"
                "- 12b-1 distribution fees and platform revenue-sharing kickbacks.\n"
                "- Custodial custody markups and execution spreads.\n\n"
                "$$\n"
                r"\mathrm{Wealth}(T) = W_0 (1 + r - \mathrm{TER})^T"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A client invests $100,000 earning 8% gross annual returns over 30 years. In an index fund charging 0.20% (net return 7.8%), terminal wealth reaches **$951,838**.\n\n"
                "In a loaded active fund charging 2.20% (net return 5.8%), terminal wealth reaches only **$542,713**. The $409,125 difference represents a 43.0% loss of potential accumulated wealth. Transparent advisors explain total cost of ownership before clients commit capital.\n\n"
                "## Work through it yourself\n\n"
                "1. Audit all fee disclosures for explicit Total Expense Ratios.\n"
                "2. Check whether product recommendations carry third-party kickbacks.\n"
                "3. Disclose all compensation in plain writing before accepting client capital.\n\n"
                "### In the sandbox\n\n"
                "Run the script to observe how a 2% fee compounds into a 43% wealth loss over 30 years."
            ),
            "exercise": question(
                "Over a 30-year investment period, what proportion of total potential wealth is consumed by a 2% annual fee drag compared to a 0.2% low-cost baseline (assuming 8% gross returns)?",
                [
                    "Approximately 2% of total accumulated terminal wealth",
                    "Approximately 10% of total accumulated terminal wealth",
                    "Over 40% of total accumulated terminal wealth",
                ],
                2,
                "Because fees reduce capital that would otherwise compound exponentially, a 2% fee drag destroys approximately 43% of 30-year terminal wealth.",
            ),
            "exercises": [
                question(
                    "Over 30 years, what proportion of wealth is consumed by a 2% fee drag vs 0.2% baseline (at 8% gross)?",
                    [
                        "Approximately 2% of total wealth",
                        "Approximately 10% of total wealth",
                        "Over 40% of total terminal wealth",
                    ],
                    2,
                    "Fees destroy capital that would otherwise compound exponentially over multi-decade horizons.",
                ),
                question(
                    "What is a 12b-1 or trailer fee in fund distribution?",
                    [
                        "A standard clearance and custody fee paid to clearinghouses for overnight settlement of trades",
                        "An ongoing distribution fee paid to the salesperson or advisor who sold the fund",
                        "A penalty fee charged by central banks for holding excessive overnight cash reserves",
                    ],
                    1,
                    "Trailer fees are ongoing distribution kickbacks paid to advisors, creating conflicts of interest.",
                ),
            ],
            "terms": [
                {"term": "Total Expense Ratio (TER)", "definition": "The total percentage of fund assets dedicated to covering management fees, administrative costs, and operating expenses."},
                {"term": "Trailer Fee", "definition": "An ongoing fee paid by an investment fund manager to the salesperson or advisor who sold the fund to a client."},
            ],
            "references": [
                {"title": "SEC · Understanding Mutual Fund Fees and Expenses", "url": "https://www.sec.gov/investor/tools/mfcc/get-started.htm"},
            ],
        },
        {
            "id": "26.4",
            "part": "2",
            "title": "Material non-public information and mosaic theory",
            "subtitle": "Draw the boundary between illegal insider trading and legitimate mosaic research.",
            "minutes": 25,
            "objective": "Distinguish between Material Non-Public Information (MNPI) possession and legitimate multi-source Mosaic Theory research.",
            "kind": "applied-study",
            "formula": r"\text{MNPI: } \text{Material (price sensitive)} \land \text{Non-Public (not broadly disseminated)}",
            "code": (
                "# Evaluating information classification: Materiality and Public Availability\n"
                "def evaluate_information(is_material, is_public):\n"
                "    if is_material and not is_public:\n"
                "        return 'PROHIBITED: Material Non-Public Information (MNPI). Trading barred.'\n"
                "    if not is_material and not is_public:\n"
                "        return 'PERMISSIBLE MOSAIC PIECE: Non-material non-public clue. May synthesize.'\n"
                "    return 'PERMISSIBLE: Public information. Free to trade.'\n"
                "\n"
                "print(evaluate_information(True, False))\n"
                "print(evaluate_information(False, False))\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "Trading while in possession of **Material Non-Public Information (MNPI)** destroys market fairness and carries severe civil and criminal penalties under securities laws worldwide (including U.S. Exchange Act Section 10(b), Indonesian UU No. 8/1995 s.t.d.d. UU No. 4/2023 Pasal 95–98, and EU MAR Article 8).\n\n"
                "The core definition of MNPI has two prongs:\n"
                "1. **Materiality**: Information that a reasonable investor would view as significantly altering the total mix of available information, or that is likely to have a substantial effect on the market price of the security.\n"
                "2. **Non-Public**: Information that has not been disseminated broadly to the public through official filings, press releases, or recognized news channels.\n\n"
                "Under CFA Standard II(A) and EU MAR, trading while in possession of MNPI is prohibited regardless of breach. In U.S. federal courts, breach of a duty of trust or confidence (*Chiarella*, *Dirks*) is an element of Section 10(b) fraud liability for tippees.\n\n"
                "Conversely, **Mosaic Theory** protects analysts who combine publicly available information with **non-material** non-public observations (such as checking supplier trade patterns, satellite parking lot counts, or distributor interviews) to synthesize an investment thesis.\n\n"
                "$$\n"
                r"\text{MNPI} = \text{Material} \cap \text{Non-Public}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "Case A: A director at a pharmaceutical company tells a relative that a drug received unexpected FDA approval 30 minutes before the public press release. This is textbook MNPI; trading on it or tipping others violates insider trading laws.\n\n"
                "Case B: An analyst studies public customs declarations, monitors public parking lot satellite imagery, and interviews supply chain vendors to deduce that a smartphone manufacturer had strong shipments. This is protected under Mosaic Theory.\n\n"
                "## Work through it yourself\n\n"
                "1. If you receive confidential non-public data, halt trading immediately.\n"
                "2. Report the receipt of confidential data to your compliance officer.\n"
                "3. Never disclose non-public corporate metrics to colleagues or acquaintances.\n\n"
                "### In the sandbox\n\n"
                "Run the script to test information classification under the mosaic framework."
            ),
            "exercise": question(
                "Under Mosaic Theory, is an analyst allowed to trade based on non-material non-public clues combined with public data?",
                [
                    "No, all forms of non-public observation are strictly illegal under securities law",
                    "Yes, analysts may synthesize public information with non-material clues to reach conclusions",
                    "Only if the trade size is under one thousand dollars and approved by exchange officials",
                ],
                1,
                "Mosaic theory explicitly protects analysts who synthesize public filings with non-material observations to reach a research conclusion.",
            ),
            "exercises": [
                question(
                    "Is an analyst permitted to trade based on non-material clues synthesized with public filings?",
                    [
                        "No, synthesizing any non-public observation or proprietary fieldwork violates federal securities laws",
                        "Yes, combining public information with non-material clues is protected under Mosaic Theory",
                        "Only if the investment research and resulting trades are conducted by a certified university professor",
                    ],
                    1,
                    "Mosaic Theory explicitly protects synthesizing public facts with non-material clues.",
                ),
                question(
                    "What are the two core elements that define Material Non-Public Information (MNPI)?",
                    [
                        "It is material (price-sensitive) and non-public (not generally available to the market)",
                        "It is formally drafted in English and certified by an independent licensed public notary with official seal",
                        "It concerns an overseas cross-border corporate acquisition transaction with valuation exceeding one billion dollars",
                    ],
                    0,
                    "MNPI is defined by its materiality (impact on a reasonable investor) and its non-public status.",
                ),
            ],
            "terms": [
                {"term": "Material Non-Public Information (MNPI)", "definition": "Information that is not generally known to the public and that a reasonable investor would view as significantly altering the total mix of available information."},
                {"term": "Mosaic Theory", "definition": "The analysis method where an analyst gathers disparate pieces of non-material non-public information and public data to formulate a comprehensive investment thesis."},
            ],
            "references": [
                {"title": "U.S. SEC · Insider Trading: Investor Publication", "url": "https://www.sec.gov/about/reports-publications/investorpubsinsidertradingguidehtm"},
                {"title": "CFA Institute · Standard II(A) Material Nonpublic Information", "url": "https://www.cfainstitute.org/ethics-standards/codes/code-of-ethics-standards-of-professional-conduct"},
            ],
        },
        {
            "id": "26.5",
            "part": "2",
            "title": "Market manipulation: spoofing, layering, wash trading",
            "subtitle": "Recognize deceptive quotation tactics, volume fabrication, and statutory enforcement.",
            "minutes": 25,
            "objective": "Identify market manipulation tactics: spoofing, layering, wash trading, and understand FINRA, CFTC, and SEC regulatory enforcement.",
            "kind": "applied-study",
            "formula": r"\text{Wash Trade: } \text{Beneficial Owner}(A) = \text{Beneficial Owner}(B) \implies \text{Economic Change} = 0",
            "code": (
                "# Detecting wash trading: self-crossing trades with zero beneficial ownership change\n"
                "trades = [\n"
                "    {'buyer_owner_id': 'USR-101', 'seller_owner_id': 'USR-101', 'shares': 5000, 'price': 100.0},\n"
                "]\n"
                "for t in trades:\n"
                "    if t['buyer_owner_id'] == t['seller_owner_id']:\n"
                "        print('ALERT: Wash trading detected! Fake volume generated with no ownership transfer.')\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "A transparent market price reflects genuine supply and demand. Market manipulation involves entering orders or quotes with the deliberate intent to mislead participants regarding liquidity, price, or trading interest:\n\n"
                "1. **Spoofing & Layering**: Submitting non-bona fide limit orders that the trader never intends to execute, creating a false impression of buying or selling pressure, and canceling them before execution.\n"
                "2. **Wash Trading**: Simultaneously buying and selling the same instrument across accounts controlled by the same beneficial owner to fabricate fake volume.\n"
                "3. **Pump & Dump**: Artificially inflating a low-liquidity stock's price through coordinated promotional campaigns, then dumping personal holdings onto retail followers as exit liquidity.\n\n"
                "$$\n"
                r"\text{Manipulation: Intent to Deceive} \implies \text{Statutory Violation}"
                "\n$$\n\n"
                "Under FINRA Rule 2020, members face disciplinary action, fines, and industry bars. Criminal prosecution is pursued by the DOJ/CFTC under the Commodity Exchange Act (7 U.S.C. §6c(a)(5)(C), amended by Dodd-Frank §747) for commodities/derivatives, and by the SEC/DOJ under Exchange Act Section 9(a)(2) and Section 10(b) for equities.\n\n"
                "## A worked example\n\n"
                "A trader wants to sell 10,000 shares at $50.00. To push the market price up toward their offer, the trader places multiple buy orders of 1,000 shares each at $49.50, $49.60, and $49.70. Algorithmic participants see apparent bid support and step their quotes up.\n\n"
                "The manipulator sells their 10,000 shares into the rising bids at $50.00, then instantly cancels all the non-bona fide buy orders below. Because the buy orders were entered with pre-meditated intent to cancel rather than seek execution, this constitutes illegal spoofing.\n\n"
                "## Work through it yourself\n\n"
                "1. Inspect trade patterns for identical buyer/seller entities.\n"
                "2. Review order-to-cancellation ratios on automated execution desks.\n"
                "3. Ensure all posted quotes represent bona fide intent to execute.\n\n"
                "### In the sandbox\n\n"
                "Run the script to inspect automated wash trade identification logic."
            ),
            "exercise": question(
                "What distinguishes illegal spoofing from legitimate limit order cancellation?",
                [
                    "Spoofing uses faster computers and fiber-optic microwave network cables",
                    "Spoofing involves entering quotes with the pre-meditated intent to cancel before execution",
                    "There is no legal difference; cancelling any posted order is strictly illegal",
                ],
                1,
                "The defining legal standard of spoofing is the pre-meditated intent to cancel orders before execution rather than genuinely seeking liquidity.",
            ),
            "exercises": [
                question(
                    "What distinguishes illegal spoofing from legitimate order cancellation?",
                    [
                        "Spoofing relies on deploying lower-latency fiber optic networking hardware than competing market participants",
                        "Entering non-bona fide orders with the pre-meditated intent to cancel them before execution",
                        "Cancelling unexecuted resting limit orders is strictly prohibited by securities exchanges in all trading contexts",
                    ],
                    1,
                    "Spoofing is characterized by the intent to cancel orders rather than execute them.",
                ),
                question(
                    "What defines an illegal wash trade in securities or futures markets?",
                    [
                        "Selling a depreciated equity holding to harvest capital loss deductions before the fiscal year concludes",
                        "Executing trades where buyer and seller share beneficial ownership with zero economic change",
                        "Purchasing equity shares in two competing corporate firms within the same industrial sector on the same morning",
                    ],
                    1,
                    "Wash trades generate artificial trading volume without any transfer of beneficial ownership.",
                ),
            ],
            "terms": [
                {"term": "Spoofing", "definition": "The illegal practice of placing bids or offers with the intent to cancel before execution to create false appearances of market depth."},
                {"term": "Wash Trading", "definition": "A form of market manipulation where transactions are entered with no change in beneficial ownership to artificially inflate trading volume."},
            ],
            "references": [
                {"title": "CFTC · Anti-Spoofing Enforcement Overview", "url": "https://www.cftc.gov/PressRoom/PressReleases/8447-21"},
                {"title": "FINRA · Rule 2020 Use of Manipulative, Deceptive Devices", "url": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/2020"},
            ],
        },
        {
            "id": "26.6",
            "part": "3",
            "title": "Algorithmic accountability and pre-trade controls",
            "subtitle": "SEC Rule 15c3-5, market access risk collars, and human supervisory responsibility.",
            "minutes": 25,
            "objective": "Design pre-trade risk controls under SEC Rule 15c3-5, including price collars, capital limits, and automated emergency kill switches.",
            "kind": "applied-study",
            "formula": r"\text{Pre-Trade Checks: } P_{\text{order}} \in [P_{\text{ref}} \pm \delta] \quad \land \quad \text{OrderValue} \le \text{MaxCap} \quad \land \quad \text{KillSwitch} = \text{Active}",
            "code": (
                "# Pre-trade risk control firewall (SEC Rule 15c3-5 compliant)\n"
                "def pre_trade_risk_check(order_price, ref_price, order_value, max_value, kill_switch_engaged):\n"
                "    if kill_switch_engaged:\n"
                "        raise ValueError('HALT: Emergency Kill Switch is ACTIVE!')\n"
                "    if order_value > max_value:\n"
                "        raise ValueError(f'REJECT: Order value ${order_value} exceeds limit ${max_value}')\n"
                "    if abs(order_price - ref_price) / ref_price > 0.05:\n"
                "        raise ValueError('REJECT: Order price collar exceeded (5% move)')\n"
                "    return 'ACCEPTED'\n"
                "\n"
                "print(pre_trade_risk_check(101.0, 100.0, 50_000, 100_000, False))\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "A quantitative trader or algorithm engineer cannot blame the code when an automated system malfunctions. Under **SEC Rule 15c3-5 (Market Access Rule)**, broker-dealers that provide market access are legally obligated to maintain risk management controls and supervisory procedures reasonably designed to prevent erroneous orders and ensure regulatory compliance.\n\n"
                "Under Rule 15c3-5, broker-dealers must enforce pre-trade controls that operate before orders enter the exchange:\n\n"
                "1. **Price Collars**: Rejecting orders priced more than $X\\%$ away from the consolidated market quote.\n"
                "2. **Credit & Capital Caps**: Hard stop on maximum single-order notional and cumulative daily capital commitments.\n"
                "3. **Regulatory Checks**: Blocking short sales without locates and preventing wash trades.\n"
                "4. **Emergency Kill Switch**: While Rule 15c3-5 mandates credit and erroneous-order controls, an automated kill switch is industry best practice to halt order routing and cancel open orders immediately upon anomaly detection.\n\n"
                "$$\n"
                r"\text{KillSwitch}(\text{Desk}) \implies \text{CancelAllPending}() \land \text{BlockNewOrders}()"
                "\n$$\n\n"
                "## A worked example\n\n"
                "On August 1, 2012, Knight Capital deployed defective algorithmic code to production without adequate pre-trade safety controls. The algorithm entered an infinite loop, buying at the offer and selling at the bid 4 million times in 45 minutes, losing over **$460 million** (SEC Release 34-70694 / 2013-222). The catastrophic loss forced Knight into a distress rescue with about $400 million in dilutive capital before merging into KCG Holdings.\n\n"
                "A hard pre-trade capital ceiling or automated error-rate kill switch would have terminated order flow within 60 seconds, preventing firm destruction.\n\n"
                "## Work through it yourself\n\n"
                "1. Configure hard pre-trade caps inside your automated execution pipeline.\n"
                "2. Test your emergency kill switch monthly in a simulated testbed.\n"
                "3. Document operational escalation procedures.\n\n"
                "### In the sandbox\n\n"
                "Run the script to verify pre-trade firewall rules."
            ),
            "exercise": question(
                "Under SEC Rule 15c3-5, who bears regulatory responsibility for pre-trade controls on orders routed to an exchange?",
                [
                    "The programming language compiler software vendor",
                    "The broker-dealer with market access and its supervisory principals",
                    "The exchange matching engine operators",
                ],
                1,
                "Broker-dealers with market access bear strict legal accountability under Rule 15c3-5 for pre-trade risk controls.",
            ),
            "exercises": [
                question(
                    "Under SEC Rule 15c3-5, who bears legal accountability for market access risk controls?",
                    [
                        "Software compilers and open-source programming library developers",
                        "Broker-dealers providing market access and their supervisory principals",
                        "Third-party market data quote vendors and financial news aggregator websites",
                    ],
                    1,
                    "Rule 15c3-5 binds broker-dealers with market access to enforce financial and regulatory risk controls.",
                ),
                question(
                    "What pre-trade risk controls are mandated under SEC Rule 15c3-5?",
                    [
                        "Pre-trade price collars, capital limits, and regulatory compliance filters",
                        "Post-trade manual compliance inspections conducted forty-eight hours after order executions occur",
                        "Daily physical trading log printouts archived in offsite commercial document storage facilities",
                    ],
                    0,
                    "Rule 15c3-5 mandates pre-trade programmatic price, credit, capital, and regulatory controls.",
                ),
            ],
            "terms": [
                {"term": "Kill Switch", "definition": "An emergency mechanism used to shut down an automated trading system and cancel all open orders immediately."},
                {"term": "Market Access Rule (SEC 15c3-5)", "definition": "Federal regulation requiring broker-dealers to implement pre-trade risk controls on all electronic market access."},
            ],
            "references": [
                {"title": "U.S. SEC · Rule 15c3-5 Risk Management Controls for Market Access", "url": "https://www.sec.gov/rules/final/2010/34-63241.pdf"},
                {"title": "U.S. SEC · In the Matter of Knight Capital Americas LLC (Release 34-70694)", "url": "https://www.sec.gov/litigation/admin/2013/34-70694.pdf"},
            ],
        },
        {
            "id": "26.7",
            "part": "3",
            "title": "GIPS standards and honest performance presentation",
            "subtitle": "Performance presentation net of fees, composite rules, and survivorship-free presentation.",
            "minutes": 25,
            "objective": "Present historical performance in compliance with CFA Institute GIPS standards and SEC Marketing Rule net return requirements.",
            "kind": "applied-study",
            "formula": r"\text{Net Return} = R_{\text{gross}} - \text{Management Fees} - \text{Direct Trading Costs}",
            "code": (
                "# Presenting net performance under GIPS standards\n"
                "gross_returns = [0.12, 0.08, -0.04, 0.15, 0.10]\n"
                "mgmt_fee = 0.015  # 1.5% management fee deducted for net return\n"
                "net_y1 = gross_returns[0] - mgmt_fee\n"
                "net_y2 = gross_returns[1] - mgmt_fee\n"
                "print(f'Year 1: Gross Return = {gross_returns[0]*100:.1f}%, Net Return = {net_y1*100:.1f}%')\n"
                "print(f'Year 2: Gross Return = {gross_returns[1]*100:.1f}%, Net Return = {net_y2*100:.1f}%')\n"
                "print('SEC Marketing Rule requires net returns alongside gross in marketing presentations.')\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "Investment managers frequently cherry-pick their best-performing accounts or present hypothetical gross returns while burying hefty fees in fine print. To establish global comparability and honesty, the CFA Institute established the **Global Investment Performance Standards (GIPS)**.\n\n"
                "Core GIPS requirements:\n"
                "1. **Composites Defined by Mandate**: A composite must include all actual, fee-paying, discretionary portfolios managed according to the same investment strategy or mandate—no picking only the winners.\n"
                "2. **Net-of-Fees Presentation**: GIPS net-of-fees performance reflects the deduction of investment management fees. Under the **SEC Marketing Rule (17 CFR 275.206(4)-1(d)(1))**, whenever gross performance is displayed to prospective clients, net performance must be presented with equal prominence.\n"
                "3. **Survivorship Freedom**: Closed or terminated client accounts must remain in historical composite calculations for the periods they were active, eliminating survivorship bias.\n\n"
                "$$\n"
                r"R_{\text{composite}} = \sum_{i=1}^M \frac{V_{i, t-1}}{\sum V_{t-1}} R_{i, \text{net}}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "An asset manager launches five portfolios in a small-cap value composite mandate in 2020. By 2025, three portfolios performed poorly and were liquidated, while two accounts gained 14% annually. In an advertisement, the manager displays: 'Our track record shows 14% annual returns!'.\n\n"
                "This violates GIPS and SEC disclosure rules. By excluding the three liquidated accounts, the manager commits gross survivorship bias. GIPS requires reporting the composite return of all portfolios managed to that mandate, which yields a true historical return of 3.8%.\n\n"
                "## Work through it yourself\n\n"
                "1. Calculate returns net of investment management fees.\n"
                "2. Include terminated accounts in your historical composite records.\n"
                "3. Present net returns with equal prominence whenever gross returns are displayed.\n\n"
                "### In the sandbox\n\n"
                "Run the script to calculate net performance alongside gross returns."
            ),
            "exercise": question(
                "Under CFA Institute GIPS standards, how must closed or terminated client accounts be treated in historical composite returns?",
                [
                    "They must be deleted immediately to prevent cluttering the database",
                    "They must remain included in historical composite calculations for the periods they were active",
                    "Their historical returns must be replaced with the risk-free treasury rate",
                ],
                1,
                "GIPS requires terminated accounts to remain in historical composites to prevent survivorship bias from inflating past returns.",
            ),
            "exercises": [
                question(
                    "Under GIPS, how must terminated portfolios be handled in historical composites?",
                    [
                        "Permanently expunged from historical records upon closure to prevent database clutter",
                        "Must remain included in historical composite calculations for the periods they were open and active",
                        "Retroactively replaced with composite benchmark indices or risk-free sovereign treasury bill yields",
                    ],
                    1,
                    "Terminated accounts must remain in historical composite periods to eliminate survivorship bias.",
                ),
                question(
                    "Under the SEC Marketing Rule (17 CFR 275.206(4)-1), what is required when displaying gross returns?",
                    [
                        "Net-of-fee returns must be presented with at least equal prominence",
                        "Gross-of-fee returns may be presented exclusively without disclosing management fees to institutional clients",
                        "Marketing presentations must be submitted for prior authorization to international governmental bodies",
                    ],
                    0,
                    "The SEC Marketing Rule requires net-of-fee returns to be presented alongside gross returns with equal prominence.",
                ),
            ],
            "terms": [
                {"term": "GIPS Standards", "definition": "Global Investment Performance Standards created by the CFA Institute to ensure fair representation and full disclosure of performance records."},
                {"term": "Composite", "definition": "An aggregation of one or more portfolios managed according to a similar investment mandate, objective, or strategy."},
                {"term": "SEC Marketing Rule", "definition": "17 CFR 275.206(4)-1 governing investment adviser advertisements, requiring net-of-fee presentation alongside gross performance."},
            ],
            "references": [
                {"title": "CFA Institute · GIPS Standards for Firms", "url": "https://www.gipsstandards.org/standards/gips-standards-for-firms/"},
                {"title": "U.S. SEC · Marketing Rule for Investment Advisers (17 CFR 275.206(4)-1)", "url": "https://www.sec.gov/rules/final/2020/ia-5653.pdf"},
            ],
        },
        {
            "id": "26.8",
            "part": "4",
            "title": "Codifying your personal trading and compliance charter",
            "subtitle": "Pre-clearance, holding periods, restricted lists, and auditable conduct guardrails.",
            "minutes": 25,
            "objective": "Synthesize conduct principles into an auditable, written personal trading charter evaluated under the compliance rubric.",
            "kind": "applied-study",
            "formula": r"\text{Personal Charter} = \{\text{Pre-clearance}, \text{Restricted lists}, \text{Holding periods}, \text{Blackout windows}\}",
            "code": (
                "# Verifying adherence to personal trading charter rules\n"
                "max_position_size_pct = 0.10\n"
                "min_holding_period_days = 30\n"
                "def check_order(symbol, size_pct, holding_days):\n"
                "    if symbol == 'BBCA' or symbol == 'TLKM':\n"
                "        return f'REJECT: {symbol} is on the firm Restricted List!'\n"
                "    if size_pct > max_position_size_pct:\n"
                "        return 'REJECT: Position size exceeds 10% charter cap.'\n"
                "    if holding_days < min_holding_period_days:\n"
                "        return 'REJECT: Minimum 30-day holding period violated.'\n"
                "    return 'APPROVED: Order adheres to personal charter guardrails.'\n"
                "\n"
                "print(check_order('ASII', 0.08, 45))\n"
                "print(check_order('BBCA', 0.05, 60))\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "Knowledge without codified rules evaporates under market stress. When markets plunge or greed surges, rational intentions give way to emotional impulses.\n\n"
                "The capstone deliverable of this course is the codification of your own **Personal Trading & Compliance Charter**. In institutional firms, no portfolio manager or employee trades without a written Compliance Policy. Your personal charter establishes clear, auditable boundaries before you execute a trade:\n\n"
                "1. **Pre-Clearance Protocol**: Pre-clearing personal transactions with compliance before routing orders to prevent front-running or conflicts.\n"
                "2. **Restricted & Watch Lists**: Prohibiting personal trading in securities where your business or employer has confidential advisory relationships or possesses non-public knowledge.\n"
                "3. **Minimum Holding Periods**: Mandating that personal investments be held for at least 30 or 60 days to prevent short-term market speculation.\n"
                "4. **Blackout Windows**: Banning personal trading before and after corporate earnings releases or significant client rebalancing.\n\n"
                "$$\n"
                r"\mathrm{CharterCompliance} = \prod_{k=1}^K \mathbb{I}(\text{Rule}_k \text{ obeyed})"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A quantitative analyst drafts a charter requiring a 30-day minimum holding period and pre-clearance against the firm's Restricted List. When tempted by a volatile meme stock rumored to be an advisory client, the automated pre-trade checklist immediately rejects the order, preventing a career-ending regulatory breach.\n\n"
                "## Work through it yourself\n\n"
                "1. Draft your personal charter specifying pre-clearance and minimum holding periods.\n"
                "2. Review each rule against CFA, SEC, and FINRA standards.\n"
                "3. Submit the final assessment to earn your verifiable certificate.\n\n"
                "### In the sandbox\n\n"
                "Run the script to test daily compliance verification against charter constraints."
            ),
            "exercise": question(
                "What is the primary function of establishing a written personal trading charter with pre-clearance and restricted lists?",
                [
                    "To print on fancy paper for office decoration",
                    "To pre-commit to objective risk boundaries and ethical standards before volatility and temptation cloud judgment",
                    "To avoid paying statutory capital gains taxes on personal trades",
                ],
                1,
                "A personal charter pre-commits the investor to objective risk limits and ethical boundaries before emotional pressure arises in volatile markets.",
            ),
            "exercises": [
                question(
                    "What is the function of a written trading charter before trading?",
                    [
                        "Serving as ceremonial corporate documentation designed primarily for executive office display",
                        "Pre-commit to objective risk limits and ethical standards before volatility clouds decisions",
                        "Eliminating statutory capital gains and corporate dividend tax obligations on securities portfolios",
                    ],
                    1,
                    "A charter pre-commits an investor to objective boundaries before stress occurs.",
                ),
                question(
                    "What is the role of a Restricted List in an institutional compliance charter?",
                    [
                        "A list of publicly traded companies that have reported disappointing quarterly operating earnings",
                        "A list of securities in which personal and firm trading is barred due to confidential advisory roles or MNPI",
                        "A roster of corporate finance employees who are temporarily barred from taking statutory annual leave",
                    ],
                    1,
                    "Restricted lists prohibit trading in securities where the firm possesses confidential advisory relationships or non-public data.",
                ),
            ],
            "terms": [
                {"term": "Personal Trading Charter", "definition": "A formal written document outlining an investor's mandatory risk controls, ethical guardrails, and daily operational routines."},
                {"term": "Restricted List", "definition": "A confidential list of securities in which all trading by employees and the firm is barred due to material non-public information or advisory engagements."},
            ],
            "references": [
                {"title": "CFA Institute · Professional Standards: Personal Trading Policies", "url": "https://www.cfainstitute.org/standards/professionals/code-ethics-standards"},
            ],
        },
    ]

    # Add Part 4 real lessons (26.9 - 26.17)
    modules.extend(get_part4_modules())

    parts = [
        {
            "id": "1",
            "title": "Fiduciary Duty, Loyalty & Client Priority",
            "subtitle": "Why conduct applies outside the trading floor, managing agency conflicts, eliminating front-running, and exposing hidden fee drag.",
            "description": "Establish agency relationships, enforce client execution priority, and calculate total cost of ownership.",
        },
        {
            "id": "2",
            "title": "Market Integrity & Information Hygiene",
            "subtitle": "Navigating Material Non-Public Information (MNPI), mosaic research boundaries, and detecting manipulative market quoting.",
            "description": "Master the two-prong MNPI test, differentiate mosaic research, and detect spoofing, layering, and wash trading.",
        },
        {
            "id": "3",
            "title": "Algorithmic Accountability & Institutional Standards",
            "subtitle": "SEC Rule 15c3-5 risk firewalls, GIPS performance presentation standards, and quantitative research integrity.",
            "description": "Configure pre-trade capital collars and kill switches, eliminate backtest p-hacking, and present net returns under GIPS.",
        },
        {
            "id": "4",
            "title": "Supervision, Execution Quality & Personal Charter",
            "subtitle": "Best execution benchmarks, fraud detection, cybersecurity stewardship, and codifying your auditable trading charter.",
            "description": "Measure implementation shortfall, detect Ponzi schemes, enforce cybersecurity controls, and draft your written personal charter.",
        },
    ]

    STRATEGY_FOOTER = (
        "\n\n# The price sandbox stays in cash; its equity curve is not evidence for the strategy's performance.\n"
        "def strategy(data):\n"
        '    return data["close"] < 0\n'
    )
    for m in modules:
        if "def strategy(data)" not in m.get("code", ""):
            m["code"] = (m.get("code", "") + STRATEGY_FOOTER).strip()

    # 26 Question Final Examination (PRD requirement: min 25 questions, >=80% pass threshold)
    primary_exam_questions = [
        {
            "id": "conduct-final-q1",
            "lessonId": "26.1",
            "question": "Under fiduciary law, what is the core mandate of the Duty of Loyalty when managing investor or client assets?",
            "options": [
                "Always placing the client's financial interests strictly ahead of the manager's or firm's own interests",
                "Maximizing gross trading commission volumes and third-party distribution rebates for the sponsoring brokerage firm",
                "Guaranteeing that retail client investment portfolios achieve a minimum twenty percent annual compound capital return",
            ],
            "answer": 0,
            "explanation": "The Duty of Loyalty requires fiduciaries to subordinate their personal and corporate interests to the sole benefit of the client at all times.",
        },
        {
            "id": "conduct-final-q2",
            "lessonId": "26.2",
            "question": "Why is front-running considered an egregious violation of fair trading standards?",
            "options": [
                "The broker profits by trading personally ahead of a pending client order that will move market prices",
                "The broker executes routine customer block transactions on competing national exchanges across time zones",
                "The broker refuses to execute institutional client orders that encompass more than ten thousand individual shares",
            ],
            "answer": 0,
            "explanation": "Front-running exploits advance non-public knowledge of pending client orders to take personal positions, driving up costs for the client.",
        },
        {
            "id": "conduct-final-q3",
            "lessonId": "26.3",
            "question": "In wealth management, how do hidden distribution or 12b-1 trailer fees create severe agency conflicts?",
            "options": [
                "They incentivize advisors to recommend higher-cost loaded products that pay rebates over superior funds",
                "They eliminate all custodial account maintenance charges and transaction settlement fees for retail clients",
                "They mandate that registered investment advisers publish their complete personal trading records on public portals",
            ],
            "answer": 0,
            "explanation": "Trailer fees align the advisor's income with product issuers rather than the client, creating a hidden conflict of interest that biases investment recommendations.",
        },
        {
            "id": "conduct-final-q4",
            "lessonId": "26.4",
            "question": "Under the Mosaic Theory recognized by securities regulators, an analyst is legally permitted to trade when their thesis is built from:",
            "options": [
                "A synthesis of public corporate filings and non-material observations gathered through diligent analysis",
                "A confidential quarterly earnings report leaked in advance by an executive in breach of fiduciary duties",
                "An unreleased regulatory approval document obtained from an auditor without corporate authorization",
            ],
            "answer": 0,
            "explanation": "Mosaic Theory explicitly protects analysts who combine publicly available information with non-material clues to reach a novel investment conclusion.",
        },
        {
            "id": "conduct-final-q5",
            "lessonId": "26.5",
            "question": "What constitutes illegal layering in electronic order books?",
            "options": [
                "Entering multiple non-bona fide orders at staggered price levels to fabricate fake depth, canceling before fills",
                "Purchasing shares in three competing companies within the same industrial sector on the same trading morning",
                "Splitting an institutional parent order into smaller market slices executed across the regular trading session",
            ],
            "answer": 0,
            "explanation": "Layering creates artificial quotes with no genuine intent to trade, tricking other market participants into reacting to phantom liquidity.",
        },
        {
            "id": "conduct-final-q6",
            "lessonId": "26.6",
            "question": "Under SEC Rule 15c3-5, what is the regulatory requirement regarding pre-order risk checks for direct market access?",
            "options": [
                "Broker-dealers must enforce pre-trade price and capital limits, though certain controls may be allocated under (d)(1)",
                "Brokers are permitted to conduct manual risk evaluations forty-eight hours after algorithmic executions take place",
                "Pre-trade risk controls apply strictly to retail accounts while institutional proprietary desks are fully exempt",
            ],
            "answer": 0,
            "explanation": "Rule 15c3-5 mandates automated pre-trade financial and regulatory risk controls that prevent erroneous orders, with limited allocation permitted under paragraph (d)(1).",
        },
        {
            "id": "conduct-final-q7",
            "lessonId": "26.7",
            "question": "Under GIPS standards, why must composites include all actual, fee-paying, discretionary portfolios managed to a specific mandate?",
            "options": [
                "To eliminate cherry-picking bias by including all fee-paying discretionary accounts managed to that mandate",
                "To ensure that marketing materials include non-discretionary retail advisory accounts with custom restrictions",
                "To allow investment firms to report hypothetical backtested performance as if it were authentic client capital",
            ],
            "answer": 0,
            "explanation": "GIPS composites mandate complete inclusion of all qualifying portfolios to eliminate selection bias and provide a fair, unmanipulated track record.",
        },
        {
            "id": "conduct-final-q8",
            "lessonId": "26.8",
            "question": "What is the primary benefit of maintaining a documented personal trading policy and compliance charter?",
            "options": [
                "It codifies holding periods, pre-clearance rules, and restricted lists to prevent personal trading conflicts",
                "It guarantees that personal equity portfolios will never experience paper drawdowns during market corrections",
                "It exempts finance professionals from paying capital gains taxes on personal short-term securities holdings",
            ],
            "answer": 0,
            "explanation": "A personal compliance charter codifies holding periods, blackout windows, and pre-clearance protocols, protecting both the individual and firm from regulatory breach.",
        },
    ]

    # Add questions q9 to q17 from Part 4
    primary_exam_questions.extend(get_part4_exam_questions())

    exam_questions = list(primary_exam_questions)

    # 9 substantive scenario questions (reaching 26 questions total)
    extra_exam_q = [
        {
            "id": "conduct-final-scenario-1",
            "lessonId": "26.4",
            "question": "An investment advisor learns from a relative who works at a pharmaceutical company that the FDA approved a key drug 30 minutes before public disclosure. Can the advisor trade on this information for client accounts?",
            "options": [
                "Yes, because the advisor owes an overriding fiduciary duty to maximize client account investment returns",
                "No, this information constitutes MNPI; trading on it is illegal insider trading regardless of whose account is used",
                "Yes, provided the order is routed in small tranches of less than one thousand shares across competing execution venues",
            ],
            "answer": 1,
            "explanation": "MNPI cannot be used for any account (client or personal). The duty of loyalty to clients never overrides statutory prohibitions against insider trading.",
        },
        {
            "id": "conduct-final-scenario-2",
            "lessonId": "26.6",
            "question": "Under SEC Rule 15c3-5 and institutional risk practices, which mechanism must be configured to immediately halt all outbound orders across a broker's algorithmic desk during an anomaly?",
            "options": [
                "A 24-hour toll-free customer support telephone hotline for exchange operators",
                "An automated emergency kill switch capable of halting routing and canceling outstanding orders",
                "An annual end-of-year financial audit report submitted to securities clearinghouses",
            ],
            "answer": 1,
            "explanation": "A pre-trade kill switch is an essential electronic mechanism that immediately terminates order routing and cancels open orders when market or software anomalies occur.",
        },
        {
            "id": "conduct-final-scenario-3",
            "lessonId": "26.7",
            "question": "When an adviser shows gross-of-fee performance to prospective clients under the SEC Marketing Rule, why must net-of-fee returns be shown alongside it with equal prominence?",
            "options": [
                "Because gross returns give clients an inflated expectation of what capital actually compounds into their accounts",
                "Because calculating gross historical performance requires complex proprietary software that retail investors cannot audit",
                "Because custodian banks prohibit reporting gross returns unless all underlying client investment assets are held entirely in cash",
            ],
            "answer": 0,
            "explanation": "Net-of-fee returns represent the true economic return realized by the client after subtracting all fee drag that depletes compounding.",
        },
        {
            "id": "conduct-final-scenario-4",
            "lessonId": "26.5",
            "question": "What constitutes an illegal wash trade under securities and commodities regulations?",
            "options": [
                "Selling an equity holding at a loss in December to achieve tax-loss harvesting benefits",
                "Executing simultaneous buy and sell orders in the same instrument where there is no change in beneficial ownership",
                "Purchasing shares in a laundry detergent manufacturing company during high market volatility",
            ],
            "answer": 1,
            "explanation": "Wash trading involves trading with oneself or coordinated accounts to manipulate reported trading volume with zero economic risk or change in beneficial ownership.",
        },
        {
            "id": "conduct-final-scenario-5",
            "lessonId": "26.1",
            "question": "In corporate treasury and enterprise finance, what does the client asset segregation rule prevent?",
            "options": [
                "Accidental commingling and spending of client prepayments on general operating expenses",
                "Timely payment of enterprise commercial property leases and monthly utility obligations",
                "Opening enterprise commercial checking accounts with authorized domestic commercial banks",
            ],
            "answer": 0,
            "explanation": "Segregating client funds prevents fiduciary commingling where client money is spent on general enterprise expenses.",
        },
        {
            "id": "conduct-final-scenario-6",
            "lessonId": "26.4",
            "question": "What is the key ethical difference between legitimate Mosaic Theory research and illegal insider trading?",
            "options": [
                "Mosaic theory combines public data and non-material observations; insider trading exploits material non-public information",
                "Mosaic theory is restricted to academic professors, whereas commercial traders cannot use external clues",
                "Insider trading is legally permissible whenever total personal trade profits are under ten thousand dollars",
            ],
            "answer": 0,
            "explanation": "Mosaic theory relies on public information and non-material clues, whereas insider trading relies on material non-public information.",
        },
        {
            "id": "conduct-final-scenario-7",
            "lessonId": "26.9",
            "question": "A broker routes customer orders to an affiliated venue that pays higher order flow rebates, despite competing venues quoting narrower spreads. Does this violate FINRA Rule 5310?",
            "options": [
                "Yes, routing to maximize payment for order flow while ignoring superior prices breaches the duty of Best Execution",
                "No, broker-dealers are legally required to route all customer orders to whichever exchange offers the highest rebate",
                "No, Best Execution applies strictly to limit orders placed by institutional hedge funds with prime brokers",
            ],
            "answer": 0,
            "explanation": "Under FINRA Rule 5310, brokers cannot sacrifice execution quality or better prices to capture order flow rebates from favored venues.",
        },
        {
            "id": "conduct-final-scenario-8",
            "lessonId": "26.14",
            "question": "Under the Supreme Court ruling in Digital Realty Trust v. Somers (2018), what must an employee do to secure Dodd-Frank Section 21F anti-retaliation protections?",
            "options": [
                "Report the suspected securities violation directly to the Securities and Exchange Commission (SEC)",
                "Report the concern solely to internal human resources management and post on personal social media",
                "Resign immediately from the company and wait twelve months before contacting any regulatory authority",
            ],
            "answer": 0,
            "explanation": "In Digital Realty, the Supreme Court held that Section 21F anti-retaliation protections apply only to whistleblowers who report directly to the SEC.",
        },
        {
            "id": "conduct-final-scenario-9",
            "lessonId": "26.17",
            "question": "Under the SEC Names Rule (Rule 35d-1), an investment fund named the 'Clean Energy Growth Fund' must maintain what minimum asset allocation?",
            "options": [
                "At least 80% of the value of its assets invested in holdings aligned with the clean energy investment focus",
                "Exactly 50% of fund equity allocated to clean energy companies, with the remainder in conventional energy",
                "Any allocation chosen by the manager, provided shareholder reports are printed on recycled paper",
            ],
            "answer": 0,
            "explanation": "The SEC Names Rule mandates that funds with thematic names must invest at least 80% of assets in qualifying investments.",
        },
    ]

    exam_questions.extend(extra_exam_q)

    exams = [
        {
            "id": "conduct-compliance-essentials-final",
            "title": "Conduct & Compliance Essentials Comprehensive Examination",
            "kind": "final",
            "passingScore": 80,  # PRD requirement: >=80% pass threshold
            "minutes": 45,
            "version": 3,
            "description": "Comprehensive credential assessment covering fiduciary duties, conflict disclosure, market manipulation, algorithmic risk controls, GIPS, best execution, whistleblowing, and compliance charters. Passing threshold: 80%.",
            "moduleIds": [m["id"] for m in modules],
            "questions": exam_questions,
        }
    ]

    return {
        "id": "conduct-compliance-essentials",
        "number": 26,
        "title": "Conduct & Compliance Essentials",
        "description": (
            "Standalone verifiable compliance credential for MSME owners, corporate finance staff, "
            "and quantitative practitioners. Master fiduciary duty of loyalty, client asset segregation, "
            "conflict disclosure, material non-public information boundaries (MNPI vs Mosaic), market "
            "manipulation safeguards (spoofing, wash trading), SEC Rule 15c3-5 algorithmic risk firewalls, "
            "GIPS performance standards, best execution under FINRA 5310, and auditable compliance charters. Earn a verifiable certificate "
            "with score bands (Pass / Merit / Distinction) and public QR verification."
        ),
        "source": "Primary regulatory standards · SEC, FINRA, CFA Institute, and OJK frameworks",
        "level": "Intermediate",
        "icon": "book",
        "studyType": "applied",
        "modules": modules,
        "parts": parts,
        "prerequisites": "None. Suitable for MSME business owners, corporate finance teams, and quantitative developers.",
        "outcomes": [
            "Apply fiduciary agency duties and client asset segregation across business and trading operations",
            "Identify and eliminate hidden trailer fees, conflicts of interest, and front-running violations",
            "Distinguish between illegal MNPI breaches and protected Mosaic Theory research",
            "Detect and prevent market manipulation: spoofing, layering, wash trading, and exit liquidity traps",
            "Configure pre-trade risk controls and emergency kill switches under SEC Rule 15c3-5",
            "Present performance records net of all fees in full compliance with CFA Institute GIPS standards",
            "Measure execution quality using implementation shortfall under FINRA Rule 5310",
            "Draft and enforce an auditable written Personal Trading & Compliance Charter",
        ],
        "readingGuide": (
            "This standalone course prepares learners for professional financial responsibility. "
            "Work through each lesson, examine the real-world case studies, and complete the comprehensive "
            "26-question final assessment. Scoring 80% or higher earns an official verifiable digital certificate. "
            "Note: Educational and informational material only; does not constitute legal, tax, or regulatory advice."
        ),
        "resources": [
            {
                "title": "Auditable Compliance & Transaction Log Template (CSV)",
                "url": "/templates/transaction_log_template.csv",
            },
        ],
        "references": [
            {"title": "CFA Institute · Code of Ethics and Standards of Professional Conduct", "url": "https://www.cfainstitute.org/standards/professionals/code-ethics-standards"},
            {"title": "U.S. SEC · Regulation Best Interest (Reg BI)", "url": "https://www.sec.gov/regulation-best-interest"},
            {"title": "FINRA · Rule 2010 Standards of Commercial Honor", "url": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/2010"},
            {"title": "FINRA · Rule 5310 Best Execution and Interpositioning", "url": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/5310"},
            {"title": "CFA Institute · GIPS Standards for Firms", "url": "https://www.gipsstandards.org/standards/gips-standards-for-firms/"},
            {"title": "OJK · Regulasi Pasar Modal dan Perlindungan Konsumen (UU P2SK / POJK)", "url": "https://ojk.go.id"},
        ],
        "exams": exams,
        # CS-1 course metadata
        "slug": "conduct-compliance-essentials",
        "subtitle": "Professional Conduct, Regulatory Standards & Verifiable Credential",
        "audience_tags": ["compliance", "intermediate", "investor", "msme", "credential"],
        "estimated_minutes": sum(m["minutes"] for m in modules),
        "lesson_count": len(modules),
        "assessment_count": len(exams),
        "completion_criteria": {"lessons_pct": 100, "assessment_pass_pct": 80},
        "certificate": {
            "enabled": True,
            "template_id": "conduct-compliance-credential",
            "verification_required": True,
        },
        "funnel_cta": {
            "label": "Deepen Valuation in Security Analysis",
            "target_course_id": "security-analysis",
            "secondary_label": "Share Your Verifiable Certificate on LinkedIn",
            "secondary_target_course_id": "certifications",
        },
        "language": ["en", "id"],
    }
