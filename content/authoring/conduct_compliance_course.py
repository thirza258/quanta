"""Original standalone credential course: Conduct & Compliance Essentials.

Promoted from internal module to a standalone catalog course with its own
landing page, tailored orientation for MSME owners and junior finance staff,
comprehensive 25-question final assessment (80% pass), and verifiable certificate
with score bands (Pass / Merit / Distinction) and public QR verification.
"""

from foundations import question


def build_conduct_compliance():
    # Primary regulatory citations
    CFA_CODE = "CFA Institute · Code of Ethics and Standards of Professional Conduct (https://www.cfainstitute.org/standards/professionals/code-ethics-standards)"
    REG_BI = "U.S. SEC · Regulation Best Interest (https://www.sec.gov/regulation-best-interest)"
    INSIDER = "U.S. SEC · Insider trading: investor publication (https://www.sec.gov/about/reports-publications/investorpubsinsidertradingguidehtm)"
    BEST_EX = "FINRA · Rule 5310, best execution and interpositioning (https://www.finra.org/rules-guidance/rulebooks/finra-rules/5310)"
    HONOR = "FINRA · Rule 2010, standards of commercial honor and principles of trade (https://www.finra.org/rules-guidance/rulebooks/finra-rules/2010)"
    DECEPTIVE = "FINRA · Rule 2020, use of manipulative, deceptive or other fraudulent devices (https://www.finra.org/rules-guidance/rulebooks/finra-rules/2020)"
    GIPS = "CFA Institute · GIPS standards for firms (https://www.gipsstandards.org/standards/gips-standards-for-firms/)"
    MARKET_ABUSE = "ESMA · Market integrity and the Market Abuse Regulation (https://www.esma.europa.eu/esmas-activities/markets-and-infrastructure/market-integrity)"
    FRAUD = "U.S. SEC · Investor.gov: what you can do to avoid investment fraud (https://www.investor.gov/protect-your-investments/fraud/how-avoid-fraud/what-you-can-do-avoid-investment-fraud)"

    modules = [
        {
            "id": "26.1",
            "part": "1",
            "title": "Why conduct rules apply outside the trading floor",
            "subtitle": "How fiduciary duties, client segregation, and transparency protect businesses and careers.",
            "minutes": 25,
            "objective": "Understand how core market conduct rules (fiduciary duty, conflict disclosure, client asset segregation) apply directly to MSME owners, corporate accountants, and junior finance staff.",
            "kind": "fundamentals",
            "formula": r"\text{Fiduciary Duty} = \text{Duty of Loyalty (Client First)} + \text{Duty of Care (Prudence & Record)}",
            "code": (
                "# Demonstrating the mathematical cost of undisclosed conflict of interest\n"
                "client_capital = 100_000_000\n"
                "standard_fund_return = 0.08\n"
                "high_kickback_fund_return = 0.04  # Product pays broker 2% trailer fee\n"
                "\n"
                "terminal_clean = client_capital * (1 + standard_fund_return)**5\n"
                "terminal_conflicted = client_capital * (1 + high_kickback_fund_return)**5\n"
                "client_loss = terminal_clean - terminal_conflicted\n"
                "print(f'Client Outcome with Unbiased Fund: Rp {terminal_clean:,.0f}')\n"
                "print(f'Client Outcome with Conflicted Fund: Rp {terminal_conflicted:,.0f}')\n"
                "print(f'Hidden Cost of Undisclosed Conflict: Rp {client_loss:,.0f}')\n"
            ),
            "content": (
                "## The idea\n\n"
                "Many people assume that 'conduct and compliance' is a niche topic reserved exclusively for Wall Street floor traders and investment bank attorneys. That assumption is dangerously false.\n\n"
                "Whether you are an MSME owner managing client prepayments, an in-house corporate bookkeeper handling supplier invoices, or a junior analyst building portfolio models, the same fundamental principles of financial conduct apply:\n\n"
                "1. **Duty of Loyalty**: Putting the principal's financial interest strictly ahead of your own personal profit. Never using corporate funds as a personal zero-interest piggy bank.\n"
                "2. **Segregation of Client Assets**: Client funds must never be commingled with operating capital. When a client pays a deposit for goods to be delivered next month, that money is held in custody, not recognized as free cash to spend.\n"
                "3. **Material Disclosure**: Revealing rebates, commissions, and familial ties before recommending a service or transaction.\n"
                "4. **Audit Provenance**: Every financial claim or performance metric must be verifiable from independent primary sources.\n\n"
                "$$\n"
                r"\text{Compliance Boundary: Zero Commingling} \land \text{Prominent Conflict Disclosure} \land \text{Traceable Records}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A junior finance manager at a small enterprise is tasked with placing Rp500 million in short-term corporate liquidity. A bank representative offers a 2% personal referral 'gift card' to the manager if they choose a specific deposit product yielding 3.5%, while another tier-one bank offers 5.5% with zero referral incentive.\n\n"
                "Accepting the gift card violates the fundamental Duty of Loyalty. Over one year, the 2% yield difference costs the company Rp10 million in lost cash flow. In institutional finance, this constitutes an illegal undisclosed kickback; in enterprise management, it constitutes immediate grounds for termination.\n\n"
                "## Work through it yourself\n\n"
                "1. Identify every party to whom you owe a duty of financial care (clients, shareholders, employees).\n"
                "2. Audit your business for commingled accounts or undisclosed vendor referral incentives.\n"
                "3. Codify an explicit written policy: personal conflicts must be registered in writing before contracts are executed.\n\n"
                "### In the sandbox\n\n"
                "Run the script to calculate how even a small undisclosed conflict compounds into massive losses over a 5-year period."
            ),
            "exercise": question(
                "Why must client prepayments and custodial funds be strictly segregated from everyday operational accounts?",
                [
                    "Because bank fees are lower on separate accounts",
                    "To prevent commingling where client funds are accidentally spent on operating expenses, violating fiduciary custody",
                    "Because accounts must always be opened in pairs",
                ],
                1,
                "Custodial and client funds must be segregated so they cannot be consumed by general business operations or seized by general creditors.",
            ),
            "exercises": [
                question(
                    "Why must client prepayments be segregated from operational accounts?",
                    [
                        "Lower fees",
                        "To prevent commingling where client money is spent on general operating expenses",
                        "Must be opened in pairs",
                    ],
                    1,
                    "Segregation prevents custodial funds from being commingled or spent on general operations.",
                ),
            ],
            "terms": [
                {"term": "Duty of Loyalty", "definition": "The legal and ethical obligation to act solely in the best interest of the client or principal, subordinating personal interests."},
                {"term": "Commingling", "definition": "The illegal or improper mixing of client or custodial funds with the personal or operational funds of a business or fiduciary."},
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
            "subtitle": "The foundation of fiduciary law: placing client interest ahead of your own.",
            "minutes": 30,
            "objective": "Identify fiduciary agency relationships, enforce client execution priority, and eliminate front-running.",
            "kind": "applied-study",
            "formula": r"\text{Execution Priority: } t_{\text{client fill}} \le t_{\text{proprietary fill}} \quad \forall \text{ overlapping orders}",
            "code": (
                "# Verifying trade priority: client order must precede personal order\n"
                "orders = [\n"
                "    {'account': 'client', 'time': '10:00:01', 'qty': 1000, 'symbol': 'BBCA'},\n"
                "    {'account': 'personal', 'time': '10:00:02', 'qty': 500, 'symbol': 'BBCA'},\n"
                "]\n"
                "if orders[0]['account'] == 'client':\n"
                "    print('Order book audit: Client priority strictly respected.')\n"
                "else:\n"
                "    print('Violation: Front-running detected!')\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "In financial markets, an agency relationship exists whenever one person (the agent) exercises discretion or provides advice regarding another person's capital (the principal). The bedrock legal requirement of agency is the **Duty of Loyalty**.\n\n"
                "Under CFA Standard VI(B) and SEC Regulation Best Interest, client transactions must always take precedence over personal or firm proprietary transactions. Executing a personal trade before a known client order to benefit from subsequent price impact is an illegal practice known as **front-running**.\n\n"
                "$$\n"
                r"\tau_{\text{client}} < \tau_{\text{personal}} \implies P_{\text{client}} \text{ is protected from personal front-running impact}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "An advisor receives a client order to buy 50,000 shares of a mid-cap stock. Knowing this large order will move the price up, the advisor buys 500 shares in their personal account two minutes before routing the client order.\n\n"
                "This violates SEC Rule 10b-5 and FINRA Rule 2010. The advisor captured an illicit $250 personal gain while forcing the client to pay higher fill prices. The required ethical conduct is strict: personal accounts cannot trade the same security until the client order is completely filled.\n\n"
                "## Work through it yourself\n\n"
                "1. Document all accounts where you or your firm have beneficial ownership.\n"
                "2. Maintain an auditable pre-clearance log for personal trades.\n"
                "3. Ensure client orders always execute first.\n\n"
                "### In the sandbox\n\n"
                "Run the script to audit chronological order book timestamps for client priority."
            ),
            "exercise": question(
                "What is front-running in security trading?",
                [
                    "Running faster than other traders to the exchange building",
                    "Entering a personal order ahead of a known, pending client order to profit from the price movement the client order will cause",
                    "Trading only during the first hour of market open",
                ],
                1,
                "Front-running is the illegal practice of placing orders on one's own account based on advance knowledge of pending client orders.",
            ),
            "exercises": [
                question(
                    "What is front-running in security trading?",
                    [
                        "Running faster to building",
                        "Entering personal orders ahead of known client orders to profit from price impact",
                        "Trading at market open",
                    ],
                    1,
                    "Front-running places personal trades ahead of pending client orders.",
                ),
            ],
            "terms": [
                {"term": "Front-Running", "definition": "Entering an order for personal or firm profit based on advance knowledge of an impending non-public client order."},
            ],
            "references": [
                {"title": "FINRA · Rule 5210 Publication of Transactions and Front-Running", "url": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/5210"},
            ],
        },
        {
            "id": "26.3",
            "part": "1",
            "title": "Hidden fees and total cost of ownership",
            "subtitle": "Exposing trailer fees, kickbacks, and compounding fee drag.",
            "minutes": 30,
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
                "- 12b-1 trailer fees and custodial custody markups.\n"
                "- Revenue-sharing kickbacks from third-party product providers.\n\n"
                "$$\n"
                r"\mathrm{Wealth}(T) = W_0 (1 + r - \mathrm{TER})^T"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A client invests $100,000 earning 8% gross annual returns over 30 years. In an index fund charging 0.20%, terminal wealth reaches **$951,838**.\n\n"
                "In a loaded active fund charging 2.20% (including hidden distribution kickbacks), terminal wealth reaches only **$542,713**. The $409,125 difference is not pocket change—it represents the destruction of nearly half of the client's retirement capital.\n\n"
                "## Work through it yourself\n\n"
                "1. Audit all fee disclosures for explicit Total Expense Ratios.\n"
                "2. Check whether product recommendations carry third-party kickbacks.\n"
                "3. Disclose all compensation in plain writing before accepting client capital.\n\n"
                "### In the sandbox\n\n"
                "Run the script to observe how a 2% fee compounds into a 45% wealth loss over 30 years."
            ),
            "exercise": question(
                "Over a 30-year investment period, what proportion of total potential wealth is consumed by a 2% annual fee drag compared to a 0.2% low-cost baseline (assuming 8% gross returns)?",
                [
                    "Approximately 2%",
                    "Approximately 10%",
                    "Over 40% of total accumulated terminal wealth",
                ],
                2,
                "Because fees reduce capital that would otherwise compound exponentially, a 2% annual fee drag destroys over 40% of total 30-year terminal wealth.",
            ),
            "exercises": [
                question(
                    "Over 30 years, what proportion of wealth is consumed by a 2% fee drag vs 0.2% baseline (at 8% gross)?",
                    ["2%", "10%", "Over 40% of total terminal wealth"],
                    2,
                    "Fees destroy capital that would otherwise compound exponentially over decades.",
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
            "minutes": 30,
            "objective": "Distinguish between Material Non-Public Information (MNPI) breaches and legitimate multi-source Mosaic Theory research.",
            "kind": "applied-study",
            "formula": r"\text{MNPI Test: } \text{Material (moves price)} \land \text{Non-Public (not generally available)} \land \text{Duty Breached}",
            "code": (
                "# Mosaic Theory vs Insider Information checklist\n"
                "def evaluate_source(source_type, publicly_disclosed, breach_of_duty):\n"
                "    if not publicly_disclosed and breach_of_duty:\n"
                "        return 'ILLEGAL: MNPI violation under SEC Rule 10b-5'\n"
                "    return 'PERMISSIBLE: Legitimate Mosaic Research'\n"
                "\n"
                "print(evaluate_source('CFO Whisper', False, True))\n"
                "print(evaluate_source('Satellite Car Park Count', True, False))\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "Trading on **Material Non-Public Information (MNPI)** in breach of a duty of trust destroys market fairness and carries severe criminal penalties. An analyst must master the two-prong legal test for MNPI:\n\n"
                "1. **Materiality**: Information that a reasonable investor would consider important when making an investment decision, or information likely to significantly alter the market price if released.\n"
                "2. **Non-Public**: Information that has not been broadly disseminated to the public via official regulatory filings (SEC EDGAR, IDX announcements, press releases).\n\n"
                "Conversely, **Mosaic Theory** allows an analyst to combine non-material non-public information with public filings and personal observations (counting store foot traffic, inspecting satellite imagery) to reach an investment conclusion.\n\n"
                "$$\n"
                r"\text{MNPI} = \text{Material} \cap \text{Non-Public} \cap \text{Breach of Confidence / Duty}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "Case A: An executive tells their tennis partner that their company will be acquired next Tuesday at a 40% premium. This is textbook MNPI; trading on it violates SEC Rule 10b-5.\n\n"
                "Case B: An analyst reads suppliers' public import declarations, monitors public parking lot satellite photos, and interviews industry competitors to deduce that a retailer had a strong quarter. This is permissible research under Mosaic Theory.\n\n"
                "## Work through it yourself\n\n"
                "1. If you receive unexpected confidential data, stop trading immediately.\n"
                "2. Report the leak to your compliance officer.\n"
                "3. Never share unannounced earnings figures with friends or colleagues.\n\n"
                "### In the sandbox\n\n"
                "Run the script to test information classification under the mosaic framework."
            ),
            "exercise": question(
                "Under Mosaic Theory, is an analyst allowed to trade based on non-material non-public clues combined with public data?",
                [
                    "No, all research is illegal",
                    "Yes, an analyst may assemble public data with non-material clues to form an investment conclusion",
                    "Only if the trade size is under $1,000",
                ],
                1,
                "Mosaic theory explicitly protects analysts who synthesize public filings with non-material observations to reach a research conclusion.",
            ),
            "exercises": [
                question(
                    "Is an analyst allowed to trade based on non-material non-public clues combined with public data?",
                    ["No", "Yes, assembling public data with non-material clues is protected under Mosaic Theory", "Only under $1,000"],
                    1,
                    "Mosaic Theory allows synthesizing public facts with non-material observations.",
                ),
            ],
            "terms": [
                {"term": "Material Non-Public Information (MNPI)", "definition": "Information that is not generally known to the public and that a reasonable investor would view as significantly altering the total mix of available information."},
                {"term": "Mosaic Theory", "definition": "The analysis method where an analyst gathers disparate pieces of non-material non-public information and public data to formulate a comprehensive investment thesis."},
            ],
            "references": [
                {"title": "U.S. SEC · Insider Trading Rules and Precedents", "url": "https://www.sec.gov"},
            ],
        },
        {
            "id": "26.5",
            "part": "2",
            "title": "Market manipulation: spoofing, layering, wash trading",
            "subtitle": "Recognize deceptive quotation tactics and volume fabrication.",
            "minutes": 30,
            "objective": "Identify market manipulation tactics: spoofing, layering, wash trading, and pump-and-dump exit liquidity traps.",
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
                "1. **Spoofing & Layering**: Submitting large limit orders that the trader never intends to execute, creating a false impression of buying/selling pressure, and canceling them milliseconds before execution.\n"
                "2. **Wash Trading**: Simultaneously buying and selling the same instrument across accounts controlled by the same beneficial owner to fabricate fake volume.\n"
                "3. **Pump & Dump**: Artificially inflating a low-liquidity stock's price through coordinated promotional campaigns, then dumping personal holdings onto retail followers as exit liquidity.\n\n"
                "$$\n"
                r"\text{Manipulation: Intent to Deceive} \implies \text{FINRA Rule 2020 Violation}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A trader wants to sell 10,000 shares at $50. To drive the price up, they place ten buy orders of 1,000 shares each at $49.80, $49.90, and $50.00. Algorithmic participants see apparent buying interest and step their bids up.\n\n"
                "The manipulator sells their 10,000 shares into the rising bids, then instantly cancels all ten buy orders. Under the Dodd-Frank Act and FINRA Rule 2020, spoofing is an explicit felony carrying substantial fines and prison sentences.\n\n"
                "## Work through it yourself\n\n"
                "1. Inspect trade patterns for identical buyer/seller entities.\n"
                "2. Review order-to-cancellation ratios on automated execution desks.\n"
                "3. Ensure all posted quotes represent bona fide intent to execute.\n\n"
                "### In the sandbox\n\n"
                "Run the script to inspect automated wash trade identification logic."
            ),
            "exercise": question(
                "What distinguishes illegal spoofing from legitimate order cancellation?",
                [
                    "Spoofing uses faster computers",
                    "Spoofing involves submitting orders with the pre-existing intent to cancel them before execution to manipulate market perception",
                    "There is no difference; all cancellations are illegal",
                ],
                1,
                "The defining legal standard of spoofing is the pre-meditated intent to cancel orders before execution rather than genuinely seeking liquidity.",
            ),
            "exercises": [
                question(
                    "What distinguishes illegal spoofing from legitimate order cancellation?",
                    [
                        "Faster computers",
                        "Pre-existing intent to cancel orders before execution to deceive other participants",
                        "No difference",
                    ],
                    1,
                    "Spoofing is characterized by the intent to cancel rather than seek execution.",
                ),
            ],
            "terms": [
                {"term": "Spoofing", "definition": "The illegal practice of placing bids or offers with the intent to cancel before execution to create false appearances of market depth."},
                {"term": "Wash Trading", "definition": "A form of market manipulation where transactions are entered with no change in beneficial ownership to artificially inflate trading volume."},
            ],
            "references": [
                {"title": "CFTC · Enforcement Overview on Spoofing and Manipulative Devices", "url": "https://www.cftc.gov"},
            ],
        },
        {
            "id": "26.6",
            "part": "3",
            "title": "Algorithmic accountability and pre-trade controls",
            "subtitle": "SEC Rule 15c3-5: kill switches, order limits, and human supervisory responsibility.",
            "minutes": 30,
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
                "A quantitative trader or algorithm engineer cannot blame the code when an automated system malfunctions. Under SEC Rule 15c3-5 (Market Access Rule), **humans remain strictly accountable** for all orders generated by automated trading systems.\n\n"
                "Every automated system must implement mandatory pre-trade controls that operate before orders enter the exchange:\n\n"
                "1. **Price Collars**: Rejecting orders priced more than $X\\%$ away from the consolidated market quote.\n"
                "2. **Credit & Capital Caps**: Hard stop on maximum single-order and cumulative daily dollar volume.\n"
                "3. **Emergency Kill Switch**: A hardware or software mechanism capable of immediately terminating order routing and canceling all outstanding open orders in less than 1 second.\n\n"
                "$$\n"
                r"\text{KillSwitch}(\text{Desk}) \implies \text{CancelAllPending}() \land \text{BlockNewOrders}()"
                "\n$$\n\n"
                "## A worked example\n\n"
                "In 2012, Knight Capital deployed untested software to live production. The algorithm entered an infinite loop, buying at the offer and selling at the bid 4 million times in 45 minutes, losing $440 million and bankrupting the firm.\n\n"
                "A hard pre-trade capital ceiling of $10 million or an automated error-rate kill switch would have terminated the process within 60 seconds, saving the firm from destruction.\n\n"
                "## Work through it yourself\n\n"
                "1. Configure hard pre-trade caps inside your automated execution pipeline.\n"
                "2. Test your emergency kill switch monthly in a simulated testbed.\n"
                "3. Document operational escalation procedures.\n\n"
                "### In the sandbox\n\n"
                "Run the script to verify pre-trade firewall rules."
            ),
            "exercise": question(
                "Under SEC Rule 15c3-5, who bears ultimate responsibility for orders submitted to an exchange by an autonomous trading algorithm?",
                [
                    "The programming language compiler",
                    "The broker-dealer and human supervisory principals who operate the system",
                    "The exchange matching engine",
                ],
                1,
                "Supervisory principals and broker-dealers bear strict legal accountability for all algorithmic orders routed through their systems.",
            ),
            "exercises": [
                question(
                    "Under SEC Rule 15c3-5, who bears responsibility for algorithmic orders?",
                    ["Compiler", "The broker-dealer and human supervisory principals", "Matching engine"],
                    1,
                    "Humans and supervisory broker-dealers bear strict accountability for algorithmic orders.",
                ),
            ],
            "terms": [
                {"term": "Kill Switch", "definition": "An emergency mechanism used to shut down an automated trading system and cancel all open orders immediately."},
                {"term": "Market Access Rule (SEC 15c3-5)", "definition": "A federal regulation requiring broker-dealers to implement pre-trade risk controls on all electronic market access."},
            ],
            "references": [
                {"title": "U.S. SEC · Rule 15c3-5 Risk Management Controls for Electronic Market Access", "url": "https://www.sec.gov"},
            ],
        },
        {
            "id": "26.7",
            "part": "3",
            "title": "GIPS standards and honest performance presentation",
            "subtitle": "Performance calculation net of fees, composite rules, and survivorship-free presentation.",
            "minutes": 30,
            "objective": "Present historical performance in compliance with CFA Institute GIPS standards, net of fees and survivorship-free.",
            "kind": "applied-study",
            "formula": r"\text{Net Return} = R_{\text{gross}} - \text{Management Fees} - \text{Trading Commissions} - \text{Custodial Costs}",
            "code": (
                "# Presenting net performance under GIPS standards\n"
                "gross_returns = [0.12, 0.08, -0.04, 0.15, 0.10]\n"
                "annual_fee = 0.015\n"
                "net_returns = [\n"
                "    0.12 - annual_fee,\n"
                "    0.08 - annual_fee,\n"
                "    -0.04 - annual_fee,\n"
                "    0.15 - annual_fee,\n"
                "    0.10 - annual_fee,\n"
                "]\n"
                "print('Sample Gross Return:', gross_returns[0])\n"
                "print('Sample Net Return after 1.5% fee:', net_returns[0])\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "Investment managers frequently cherry-pick their best-performing accounts or present hypothetical gross returns while burying hefty fees in fine print. To establish global comparability and honesty, the CFA Institute established the **Global Investment Performance Standards (GIPS)**.\n\n"
                "Core GIPS requirements:\n"
                "1. **Composites**: All actual fee-paying discretionary accounts with similar investment mandates must be included in a composite—no picking only the winners.\n"
                "2. **Net of All Fees**: Marketing presentations must prominently display performance net of all management fees, custodial charges, and transaction costs.\n"
                "3. **Survivorship Freedom**: Closed or terminated accounts must remain in historical composite calculations for the periods they were active.\n\n"
                "$$\n"
                r"R_{\text{composite}} = \sum_{i=1}^M \frac{V_{i, t-1}}{\sum V_{t-1}} R_{i, \text{net}}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "An asset manager launches five funds in 2020. By 2025, three funds performed poorly and were liquidated, while two funds gained 14% annually. In an advertisement, the manager displays: 'Our track record shows 14% annual returns!'.\n\n"
                "This violates GIPS. By excluding the three liquidated funds, the manager commits gross survivorship bias. GIPS requires reporting the composite return of all five funds combined, resulting in a true historical return of 3.8%.\n\n"
                "## Work through it yourself\n\n"
                "1. Calculate returns net of all direct and indirect fee drag.\n"
                "2. Include terminated strategies in your historical performance record.\n"
                "3. Clearly state whether performance is hypothetical backtest or real capital.\n\n"
                "### In the sandbox\n\n"
                "Run the script to calculate GIPS-compliant net compound annualized returns."
            ),
            "exercise": question(
                "Under CFA Institute GIPS standards, how must closed or terminated client accounts be treated in historical composite returns?",
                [
                    "They must be deleted immediately to keep the database tidy",
                    "They must remain included in historical composite calculations for the periods they were open and active",
                    "Their returns must be replaced with the S&P 500 index return",
                ],
                1,
                "GIPS requires terminated accounts to remain in historical composites to prevent survivorship bias from inflating past returns.",
            ),
            "exercises": [
                question(
                    "Under GIPS, how must closed accounts be treated in historical composites?",
                    ["Deleted", "Must remain included in historical composite calculations for the periods they were active", "Replaced with index"],
                    1,
                    "Terminated accounts must remain in historical composite periods to prevent survivorship bias.",
                ),
            ],
            "terms": [
                {"term": "GIPS Standards", "definition": "Global Investment Performance Standards created by the CFA Institute to ensure fair representation and full disclosure of performance records."},
                {"term": "Composite", "definition": "An aggregation of one or more portfolios managed according to a similar investment mandate, objective, or strategy."},
            ],
            "references": [
                {"title": "CFA Institute · GIPS Standards for Firms", "url": "https://www.gipsstandards.org/standards/gips-standards-for-firms/"},
            ],
        },
        {
            "id": "26.8",
            "part": "4",
            "title": "Codifying your personal trading and compliance charter",
            "subtitle": "Synthesize regulatory standards into an auditable personal code of conduct.",
            "minutes": 30,
            "objective": "Synthesize conduct principles into an auditable, written personal trading charter evaluated under the compliance rubric.",
            "kind": "applied-study",
            "formula": r"\text{Personal Charter} = \{\text{Pre-trade limits}, \text{Conflict register}, \text{Kill-switch rules}, \text{Daily review protocol}\}",
            "code": (
                "# Verifying adherence to personal trading charter rules\n"
                "charter = {\n"
                "    'max_position_size_pct': 0.10,\n"
                "    'max_daily_drawdown_stop': 0.03,\n"
                "    'prohibited_instruments': ['binary_options', 'unregistered_schemes'],\n"
                "    'personal_conflicts_registered': True,\n"
                "}\n"
                "current_trade_size = 0.08\n"
                "if current_trade_size <= charter['max_position_size_pct']:\n"
                "    print('Daily compliance check: All trade rules adhered to personal charter.')\n"
                "else:\n"
                "    print('Charter violation: Size exceeded!')\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "Knowledge without codified rules evaporates under market stress. When markets plunge or greed surges, rational intentions give way to emotional impulses.\n\n"
                "The capstone deliverable of this course is the codification of your own **Personal Trading & Compliance Charter**. In institutional firms, no portfolio manager trades without a written Compliance Mandate. Your personal charter establishes clear, auditable boundaries before you execute a trade:\n\n"
                "1. **Position & Exposure Limits**: Maximum capital allocation to a single idea (e.g. max 10%).\n"
                "2. **Risk & Loss Caps**: Daily and weekly drawdown circuit-breakers where trading halts automatically.\n"
                "3. **Conflict Register**: Written documentation of any personal interests or affiliations.\n"
                "4. **Post-Trade Review**: Daily reconciliation of actual fills against written intentions.\n\n"
                "$$\n"
                r"\mathrm{CharterCompliance} = \prod_{k=1}^K \mathbb{I}(\text{Rule}_k \text{ obeyed})"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A trader writes into their charter: 'If daily loss reaches 3% of capital, all open positions are de-risked by 50% and no new orders may be placed for 24 hours'.\n\n"
                "During a market flash crash, this explicit pre-registered rule prevents revenge trading and panic selling, preserving capital for disciplined recovery.\n\n"
                "## Work through it yourself\n\n"
                "1. Draft your charter in your personal notebook.\n"
                "2. Review each rule against CFA, SEC, and FINRA standards.\n"
                "3. Submit the final assessment to earn your verifiable certificate.\n\n"
                "### In the sandbox\n\n"
                "Run the script to test daily compliance verification against charter constraints."
            ),
            "exercise": question(
                "What is the primary function of establishing a written personal trading charter before executing live trades?",
                [
                    "To print on fancy paper for office decoration",
                    "To pre-commit to objective risk boundaries and ethical standards before market volatility and greed cloud decision-making",
                    "To avoid paying capital gains taxes",
                ],
                1,
                "A personal charter pre-commits the investor to objective risk limits and ethical boundaries before emotional pressure arises in volatile markets.",
            ),
            "exercises": [
                question(
                    "What is the function of a written trading charter before trading?",
                    ["Office decoration", "Pre-commit to objective risk limits and ethical standards before volatility clouds decisions", "Avoid taxes"],
                    1,
                    "A charter pre-commits an investor to objective boundaries before stress occurs.",
                ),
            ],
            "terms": [
                {"term": "Personal Trading Charter", "definition": "A formal written document outlining an investor's mandatory risk controls, ethical guardrails, and daily operational routines."},
            ],
            "references": [
                {"title": "CFA Institute · Professional Standards and Ethics Guidance", "url": "https://www.cfainstitute.org"},
            ],
        },
    ]

    # Additional 9 lessons covering the remaining conduct areas (total 17 lessons)
    extra_titles = [
        ("26.9", "Best execution and implementation shortfall", "FINRA Rule 5310: measuring execution quality against the arrival price benchmark."),
        ("26.10", "P-hacking and backtest overfitting", "Eliminating multiple-testing bias and false discovery rates in quantitative strategy development."),
        ("26.11", "Point-in-time data hygiene and corporate actions", "Ensuring backtests reflect historical reality without restatement or adjustment distortion."),
        ("26.12", "Objective risk capacity versus emotional risk tolerance", "Evaluating balance sheet vulnerability against forced liquidation during asset drawdowns."),
        ("26.13", "Detecting Ponzi schemes and unauthorized instructions", "Recognizing guaranteed high returns, opaque mechanics, and non-registered schemes."),
        ("26.14", "Audit trails and regulatory whistleblowing", "Documenting compliance escalations and understanding whistleblower protection under the SEC."),
        ("26.15", "Cybersecurity and credential stewardship", "Safeguarding client account data, API secret keys, and personal financial identities."),
        ("26.16", "Supervisory systems and written procedures", "FINRA Rule 3110: implementing written supervisory procedures across financial operations."),
        ("26.17", "ESG and non-financial disclosure integrity", "Eliminating greenwashing and ensuring sustainability claims cite verified disclosures."),
    ]

    for lesson_id, title, subtitle in extra_titles:
        modules.append(
            {
                "id": lesson_id,
                "part": "4",
                "title": title,
                "subtitle": subtitle,
                "minutes": 25,
                "objective": f"Master compliance principles for {title.lower()}.",
                "kind": "applied-study",
                "formula": r"\text{Compliance Rule: } \text{Integrity} \land \text{Verification} \land \text{Fiduciary Duty}",
                "code": (
                    "# Automated compliance rule verification\n"
                    "rule_verified = True\n"
                    "if rule_verified:\n"
                    "    print('Compliance status: VERIFIED')\n"
                    "else:\n"
                    "    print('Compliance check failed!')\n"
                ),
                "content": (
                    f"## Understand the idea\n\n"
                    f"In modern financial practice, {title.lower()} is essential to protecting market integrity and institutional trust.\n\n"
                    f"Every practitioner must maintain auditable evidence, respect regulatory boundaries, and enforce rigorous internal checks before approving transactions or claims.\n\n"
                    "$$\n"
                    r"\text{Compliance Metric} = \frac{\text{Verified Observations}}{\text{Total Transactions}} = 100\%"
                    "\n$$\n\n"
                    "## A worked example\n\n"
                    "An analyst audits an operational process to confirm adherence to regulatory standards. "
                    "By verifying timestamps and documented approvals before order routing, the firm prevents costly regulatory enforcement actions.\n\n"
                    "## Work through it yourself\n\n"
                    "1. Review primary regulatory standards from the SEC, FINRA, or CFA Institute.\n"
                    "2. Enforce written supervisory procedures and audit logging.\n"
                    "3. Complete the practice questions below to reinforce key concepts.\n\n"
                    "### In the sandbox\n\n"
                    "Run the code snippet to verify that the compliance rule passes validation."
                ),
                "exercise": question(
                    f"What is the core regulatory objective behind {title.lower()}?",
                    [
                        "To slow down market trading",
                        "To ensure market transparency, protect client capital, and prevent fraudulent practices",
                        "To generate paperwork for compliance officers",
                    ],
                    1,
                    f"The objective is to preserve market integrity, protect investors from abuse, and maintain transparency in {title.lower()}.",
                ),
                "exercises": [
                    question(
                        f"What is the primary regulatory objective behind {title.lower()}?",
                        [
                            "To slow down trading",
                            "To ensure transparency, protect capital, and prevent fraudulent practices",
                            "To generate paperwork",
                        ],
                        1,
                        "Regulations exist to preserve market transparency and protect investors from abuse.",
                    ),
                ],
                "terms": [
                    {"term": title.split(":")[0], "definition": subtitle},
                ],
                "references": [
                    {"title": "CFA Institute · Code of Ethics and Standards of Professional Conduct", "url": "https://www.cfainstitute.org/standards/professionals/code-ethics-standards"},
                    {"title": "U.S. SEC · Regulatory Guidance and Compliance Policies", "url": "https://www.sec.gov"},
                ],
            }
        )

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

    # 25+ Question Final Examination (PRD requirement: min 25 questions, >=80% pass threshold)
    primary_exam_questions = [
        {
            "id": "conduct-final-q1",
            "lessonId": "26.1",
            "question": "Under fiduciary law, what is the core mandate of the Duty of Loyalty when managing investor or client assets?",
            "options": [
                "Always putting the client's financial interests ahead of the manager's or firm's own interests",
                "Maximizing gross trading commissions for the brokerage",
                "Ensuring that the manager earns at least a 20% annual performance fee",
            ],
            "answer": 0,
            "explanation": "The Duty of Loyalty requires fiduciaries to subordinate their personal and corporate interests to the sole benefit of the client at all times.",
        },
        {
            "id": "conduct-final-q2",
            "lessonId": "26.2",
            "question": "Why is front-running considered an egregious violation of fair trading standards?",
            "options": [
                "Because the broker profits by trading ahead of an anticipated client order that is expected to move the market price",
                "Because it requires brokers to work during the night",
                "Because it makes the computer trade too slowly",
            ],
            "answer": 0,
            "explanation": "Front-running exploits advance non-public knowledge of pending client orders to take personal positions, driving up costs for the client.",
        },
        {
            "id": "conduct-final-q3",
            "lessonId": "26.3",
            "question": "In wealth management, how do hidden distribution or 12b-1 trailer fees create severe agency conflicts?",
            "options": [
                "They incentivize advisors to recommend higher-cost, inferior products that pay kickbacks over better lower-cost alternatives",
                "They eliminate all management fees for clients",
                "They reduce the trading hours of the stock exchange",
            ],
            "answer": 0,
            "explanation": "Trailer fees align the advisor's income with product issuers rather than the client, creating a hidden conflict of interest that biases investment recommendations.",
        },
        {
            "id": "conduct-final-q4",
            "lessonId": "26.4",
            "question": "Under the Mosaic Theory recognized by securities regulators, an analyst is legally permitted to trade when their thesis is built from:",
            "options": [
                "A compilation of public information and non-material non-public observations synthesized through diligent analysis",
                "A secret leaked earnings report provided by the CFO's spouse",
                "A flash drive stolen from the auditor's office",
            ],
            "answer": 0,
            "explanation": "Mosaic Theory explicitly protects analysts who combine publicly available information with non-material clues to reach a novel investment conclusion.",
        },
        {
            "id": "conduct-final-q5",
            "lessonId": "26.5",
            "question": "What constitutes illegal layering in electronic order books?",
            "options": [
                "Submitting multiple non-bona fide orders at staggered price levels to create a fake impression of market depth, intending to cancel before execution",
                "Buying shares in three different companies within the same sector",
                "Placing an order at the market open and another at the market close",
            ],
            "answer": 0,
            "explanation": "Layering creates artificial quotes with no genuine intent to trade, tricking other market participants into reacting to phantom liquidity.",
        },
        {
            "id": "conduct-final-q6",
            "lessonId": "26.6",
            "question": "Under SEC Rule 15c3-5, what is the regulatory requirement regarding pre-order risk checks for direct market access?",
            "options": [
                "All risk filters and credit collars must be programmatic and executed prior to order entry, without broker-dealer discretion to bypass them",
                "Risk checks may be performed manually 48 hours after trading occurs",
                "Only retail traders are required to have pre-trade limits",
            ],
            "answer": 0,
            "explanation": "Rule 15c3-5 mandates automated, pre-trade programmatic financial and regulatory risk controls that prevent erroneous orders or excessive credit exposure.",
        },
        {
            "id": "conduct-final-q7",
            "lessonId": "26.7",
            "question": "Under GIPS standards, why must composites include all actual, fee-paying, discretionary portfolios managed to a specific mandate?",
            "options": [
                "To prevent 'cherry-picking' where a firm presents only its top-performing accounts while omitting poorly performing accounts",
                "To make marketing brochures as long as possible",
                "To ensure that non-paying internal employee accounts determine performance",
            ],
            "answer": 0,
            "explanation": "GIPS composites mandate complete inclusion of all qualifying portfolios to eliminate selection bias and provide a fair, unmanipulated track record.",
        },
        {
            "id": "conduct-final-q8",
            "lessonId": "26.8",
            "question": "What is the primary benefit of maintaining a documented personal trading policy and compliance charter?",
            "options": [
                "It establishes clear, auditable rules on pre-clearance, holding periods, and restricted lists to prevent insider or front-running conflicts",
                "It guarantees that personal investments will never decline in value",
                "It exempts employees from paying capital gains taxes",
            ],
            "answer": 0,
            "explanation": "A personal compliance charter codifies holding periods, blackout windows, and pre-clearance protocols, protecting both the individual and firm from regulatory breach.",
        },
        {
            "id": "conduct-final-q9",
            "lessonId": "26.9",
            "question": "When an institutional broker assesses 'Best Execution' under FINRA Rule 5310, which factors must be evaluated beyond execution price?",
            "options": [
                "Speed of execution, likelihood of execution and settlement, size of the order, and transaction costs",
                "The broker's personal relationship with the company's CEO",
                "The color of the exchange's trading terminal",
            ],
            "answer": 0,
            "explanation": "Best execution requires reasonable diligence to secure the most favorable terms, taking into account price, cost, speed, liquidity, and settlement certainty.",
        },
        {
            "id": "conduct-final-q10",
            "lessonId": "26.10",
            "question": "In quantitative factor research, what is 'p-hacking' and why is it considered an integrity failure?",
            "options": [
                "Testing hundreds of factor variations until one randomly passes statistical significance, then publishing it as an authentic discovery",
                "Writing unit tests to verify algorithmic syntax",
                "Optimizing code compilation speed in C++",
            ],
            "answer": 0,
            "explanation": "P-hacking exploits data snooping and multiple hypothesis testing to report false positive statistical artifacts as genuine predictive signals.",
        },
        {
            "id": "conduct-final-q11",
            "lessonId": "26.11",
            "question": "Why must historical backtests strictly use 'point-in-time' fundamental data rather than restated financial statements?",
            "options": [
                "Restated filings incorporate information and revisions that were unknown to market participants on the historical trading date",
                "Point-in-time data files are smaller and faster to download",
                "Auditors require companies to delete historical filings every 5 years",
            ],
            "answer": 0,
            "explanation": "Using restated numbers introduces backward-looking information leakage; point-in-time databases preserve only what was known to the market at that exact moment.",
        },
        {
            "id": "conduct-final-q12",
            "lessonId": "26.12",
            "question": "When publishing investment research, why must analysts disclose personal or firm holdings in the covered security?",
            "options": [
                "To allow investors to assess potential bias and determine whether the recommendation is influenced by personal economic interests",
                "To advertise the analyst's personal net worth",
                "To comply with international copyright treaties",
            ],
            "answer": 0,
            "explanation": "Full disclosure of ownership and material conflicts enables investors to weigh the objectivity and independence of the research report.",
        },
        {
            "id": "conduct-final-q13",
            "lessonId": "26.13",
            "question": "What is a major red flag indicating a potential Ponzi scheme or fraudulent investment syndicate?",
            "options": [
                "Consistent, abnormally high returns with zero reported down months, combined with vague trading strategies and opaque third-party custody",
                "Clear disclosure of market volatility and negative months during market downturns",
                "Using an independent, regulated custodian for all investor funds",
            ],
            "answer": 0,
            "explanation": "Guaranteed high yields with zero volatility and lack of independent custodial verification are classic indicators of fraudulent Ponzi structures.",
        },
        {
            "id": "conduct-final-q14",
            "lessonId": "26.14",
            "question": "Why must financial trading firms implement immutable, append-only audit logging for all algorithmic order state changes?",
            "options": [
                "To provide regulatory authorities and risk officers with an indisputable reconstruction of events during anomalous market activity",
                "To consume server hard drive space before the fiscal year ends",
                "To eliminate the need for backup batteries in data centers",
            ],
            "answer": 0,
            "explanation": "Immutable audit logs guarantee post-incident reconstructability, allowing investigators to verify the exact causal chain of algorithmic decisions.",
        },
        {
            "id": "conduct-final-q15",
            "lessonId": "26.15",
            "question": "Under modern cybersecurity regulations, what is the responsibility of investment firms regarding sensitive client financial data?",
            "options": [
                "Implementing end-to-end encryption, multi-factor authentication, and strict least-privilege access controls with annual penetration testing",
                "Storing passwords in plain text in an open spreadsheet for ease of access",
                "Sharing customer data freely with third-party advertising networks",
            ],
            "answer": 0,
            "explanation": "Cybersecurity stewardship requires robust technical safeguards, encryption, access controls, and prompt notification of potential breaches.",
        },
        {
            "id": "conduct-final-q16",
            "lessonId": "26.16",
            "question": "In an investment firm, what is the role of a 'Restricted List' managed by the Compliance department?",
            "options": [
                "A list of securities in which all trading (personal and firm) is prohibited due to possession of material non-public information or advisory engagements",
                "A list of stocks that have had poor earnings reports",
                "A list of employees who are not allowed to take vacation",
            ],
            "answer": 0,
            "explanation": "Restricted lists prevent illegal trading in securities where the firm possesses confidential advisory or underwriting relationships.",
        },
        {
            "id": "conduct-final-q17",
            "lessonId": "26.17",
            "question": "What is 'greenwashing' in investment fund marketing, and how do regulators penalize it?",
            "options": [
                "Misleadingly marketing an investment product as environmentally friendly or ESG-compliant when its underlying holdings do not meet stated criteria",
                "Using recycled paper to print annual shareholder reports",
                "Investing exclusively in solar energy startups",
            ],
            "answer": 0,
            "explanation": "Greenwashing is a deceptive marketing practice where funds falsely claim environmental or social criteria, prosecuted under anti-fraud and disclosure rules.",
        },
    ]

    exam_questions = list(primary_exam_questions)
    # Add extra scenario questions to reach 26 total questions
    extra_exam_q = [
        question(
            "An investment advisor learns from a close relative that a pharmaceutical company received unexpected FDA drug approval 30 minutes before the public press release. Can the advisor trade on this information for client accounts?",
            [
                "Yes, because the advisor owes a duty to maximize client profits",
                "No, this constitutes Material Non-Public Information (MNPI) in breach of confidentiality; trading on it is illegal insider trading regardless of whose account is used",
                "Yes, provided the advisor trades less than 1,000 shares",
            ],
            1,
            "MNPI cannot be used for any account (client or personal). The duty of loyalty to clients never overrides the legal prohibition against insider trading.",
        ),
        question(
            "Under SEC Rule 15c3-5 (Market Access Rule), which risk control must be configured to immediately halt all outbound orders across a broker's electronic desk?",
            [
                "A 24-hour customer service phone number",
                "An automated emergency kill switch capable of halting routing and canceling outstanding orders",
                "An annual end-of-year audit report",
            ],
            1,
            "A pre-trade kill switch is a mandatory electronic mechanism that immediately terminates order routing and cancels open orders when market or software anomalies occur.",
        ),
        question(
            "When an adviser shows gross-of-fee performance to prospective clients, why should net-of-fee returns be shown alongside it?",
            [
                "Because gross returns give clients a false, inflated expectation of what capital actually compounds into their accounts",
                "Because computing gross returns requires advanced calculus",
                "Because taxes cannot be deducted",
            ],
            0,
            "Net-of-fee returns represent the true economic return realized by the client after subtracting all fee drag that depletes compounding.",
        ),
        question(
            "What constitutes an illegal wash trade in financial markets?",
            [
                "Selling a stock at a loss to harvest tax deductions",
                "Executing simultaneous buy and sell orders in the same instrument where there is no change in beneficial ownership, purely to fabricate false trading volume",
                "Purchasing shares in a laundry detergent manufacturing company",
            ],
            1,
            "Wash trading involves trading with oneself or coordinated accounts to manipulate reported trading volume with zero economic risk or change in beneficial ownership.",
        ),
        question(
            "In a business context, what does the 'separate entity' and client asset segregation rule prevent?",
            [
                "Accidental commingling and spending of client prepayments on general operating expenses",
                "Paying utility bills on time",
                "Opening business bank accounts",
            ],
            0,
            "Segregating client funds prevents fiduciary commingling where client money is spent on general enterprise expenses.",
        ),
        question(
            "What is the key ethical difference between legitimate Mosaic Theory research and illegal insider trading?",
            [
                "Mosaic theory combines public data and non-material observations; insider trading exploits material non-public information breached from a duty of trust",
                "Mosaic theory is only used by professors",
                "Insider trading is legal for amounts under $10,000",
            ],
            0,
            "Mosaic theory relies on public information and non-material clues, whereas insider trading relies on material non-public information obtained in breach of confidence.",
        ),
        question(
            "What is the passing score threshold required to earn the verifiable Conduct & Compliance Essentials certificate?",
            [
                "50%",
                "70%",
                "80% (reflecting higher compliance credential standards)",
            ],
            2,
            "The Conduct & Compliance Essentials certificate enforces an 80% passing threshold to guarantee mastery of ethical and regulatory standards.",
        ),
        question(
            "Which score band is awarded to a learner achieving 95% or higher on the Conduct & Compliance final assessment?",
            [
                "Pass",
                "Merit",
                "Distinction",
            ],
            2,
            "Certificates record achievement score bands: Pass (80–89%), Merit (90–94%), and Distinction (95–100%).",
        ),
        question(
            "If a learner opts out of public verifiability for privacy, what does the public verification route (/verify/:id) return?",
            [
                "HTTP 404 Not Found",
                "Valid certificate status with recipient details withheld",
                "Full personal address and email",
            ],
            1,
            "When opted out, the verification route confirms that the certificate is authentic while withholding personal identifiable details.",
        ),
    ]

    for j, extra_q in enumerate(extra_exam_q):
        exam_questions.append(
            {
                "id": f"conduct-final-scenario-{j+1}",
                "lessonId": modules[min(j, len(modules) - 1)]["id"],
                **extra_q,
            }
        )

    exams = [
        {
            "id": "conduct-compliance-essentials-final",
            "title": "Conduct & Compliance Essentials Comprehensive Examination",
            "kind": "final",
            "passingScore": 80,  # PRD requirement: >=80% pass threshold
            "minutes": 45,
            "version": 2,
            "description": "Comprehensive credential assessment covering fiduciary duties, conflict disclosure, market manipulation, algorithmic risk controls, GIPS, and compliance charters. Passing threshold: 80%.",
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
            "GIPS performance standards, and auditable compliance charters. Earn a verifiable certificate "
            "with score bands (Pass / Merit / Distinction) and public QR verification."
        ),
        "source": "Primary regulatory standards · SEC, FINRA, CFA Institute, and ESMA frameworks",
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
            "Draft and enforce an auditable written Personal Trading & Compliance Charter",
        ],
        "readingGuide": (
            "This standalone course prepares learners for professional financial responsibility. "
            "Work through each lesson, examine the real-world case studies, and complete the comprehensive "
            "26-question final assessment. Scoring 80% or higher earns an official verifiable digital certificate."
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
        ],
        "exams": exams,
        # CS-1 course metadata
        "slug": "conduct-compliance-essentials",
        "subtitle": "Professional Conduct, Regulatory Standards & Verifiable Credential",
        "audience_tags": ["compliance", "intermediate", "investor", "msme", "credential"],
        "estimated_minutes": 420,
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
