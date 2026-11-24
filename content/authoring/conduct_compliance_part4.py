"""Part 4 of Conduct & Compliance Essentials: Lessons 26.9 - 26.17.

Comprehensive, verified lessons covering:
26.9 Best execution & implementation shortfall (FINRA 5310)
26.10 P-hacking, multiple hypothesis testing & backtest overfitting
26.11 Point-in-time data hygiene & restatements
26.12 Objective risk capacity vs emotional risk tolerance (FINRA 2111, Reg BI, POJK)
26.13 Detecting investment scams, Ponzi mechanics & illegal offerings (OJK Satgas PASTI)
26.14 Audit trails, record-keeping & whistleblower protection (Exchange Act §21F, Digital Realty)
26.15 Cybersecurity, credential stewardship & privacy (Reg S-P, UU 27/2022 PDP)
26.16 Supervisory systems & written procedures (FINRA 3110)
26.17 Non-financial disclosures, ESG integrity & anti-greenwashing (SEC Names Rule, SFDR, TKBI)
"""

from foundations import question


def get_part4_modules():
    return [
        {
            "id": "26.9",
            "part": "4",
            "title": "Best execution and implementation shortfall",
            "subtitle": "FINRA Rule 5310: measuring execution quality and transaction costs against arrival benchmarks.",
            "minutes": 25,
            "objective": "Measure execution quality under FINRA Rule 5310 using implementation shortfall in basis points against arrival prices.",
            "kind": "applied-study",
            "formula": r"\text{Implementation Shortfall (bps)} = \frac{P_{\text{executed}} - P_{\text{arrival}}}{P_{\text{arrival}}} \times 10{,}000",
            "code": (
                "# Calculate VWAP and implementation shortfall in basis points against arrival price\n"
                "arrival_price = 10000.0\n"
                "qty1 = 6000\n"
                "price1 = 10005.0\n"
                "qty2 = 4000\n"
                "price2 = 10010.0\n"
                "total_shares = qty1 + qty2\n"
                "total_notional = (qty1 * price1) + (qty2 * price2)\n"
                "avg_price = total_notional / total_shares\n"
                "shortfall_bps = ((avg_price - arrival_price) / arrival_price) * 10000\n"
                "print(f'Arrival Price: Rp {arrival_price:,.2f}')\n"
                "print(f'Average Fill Price: Rp {avg_price:,.2f}')\n"
                "print(f'Implementation Shortfall: {shortfall_bps:.2f} bps')\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "In financial trading, a broker or asset manager owes clients an affirmative duty of **Best Execution**. Under FINRA Rule 5310, firms must use reasonable diligence to ascertain the best market for the subject security and buy or sell in that market so that the resultant price to the customer is as favorable as possible under prevailing market conditions.\n\n"
                "FINRA Rule 5310(a)(1) mandates explicit evaluation of multiple core factors:\n"
                "1. **Price and Volatility**: The character of the market for the security, including liquidity and quotes.\n"
                "2. **Size and Type of Transaction**: Order scale relative to market depth and time sensitivity.\n"
                "3. **Number of Markets Checked**: Accessing multiple competing venues and market makers.\n"
                "4. **Accessibility of Quotations**: System reliability, fill likelihood, and speed.\n"
                "5. **Terms and Conditions of the Order**: Limit instructions and customer directives.\n\n"
                "Firms routing non-directed orders cannot simply send orders to an affiliate or venue paying the highest order flow rebate if that venue yields inferior fills. Institutional desks quantify execution quality using **Implementation Shortfall**—the basis-point spread between the arrival quote when the order was submitted and the final volume-weighted average price (VWAP) filled.\n\n"
                "$$\n"
                r"\text{Shortfall} = \frac{\bar{P}_{\text{fill}} - P_{\text{arrival}}}{P_{\text{arrival}}} \times 10{,}000 \quad [\text{bps}]"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A client issues an order to buy 10,000 shares of BBCA when the consolidated market quote is Rp10,000. The broker routes 6,000 shares at Rp10,005 and 4,000 shares at Rp10,010. The average execution price is:\n\n"
                "$$\n"
                r"\bar{P} = \frac{6{,}000 \times 10{,}005 + 4{,}000 \times 10{,}010}{10{,}000} = \text{Rp } 10{,}007"
                "\n$$\n\n"
                "The implementation shortfall is $(10{,}007 - 10{,}000) / 10{,}000 = 7\\text{ bps}$. Under Rule 5310.09, firms conduct regular and rigorous internal reviews of execution quality across venues to verify that execution slippage is minimized.\n\n"
                "## Work through it yourself\n\n"
                "1. Record arrival timestamps and arrival mid-quotes whenever routing client orders.\n"
                "2. Calculate post-trade execution slippage in basis points.\n"
                "3. Benchmark fills against volume-weighted average price (VWAP) across market venues.\n\n"
                "### In the sandbox\n\n"
                "Run the script to compute average fill prices and implementation shortfall in basis points."
            ),
            "exercise": question(
                "Under FINRA Rule 5310(a)(1), which factors must a broker evaluate to determine Best Execution?",
                [
                    "Exclusively the execution price quoted on the primary exchange matching engine terminal display",
                    "Character of the market, size and type of order, number of markets checked, and quote accessibility",
                    "The personal relationship between executive committee members and primary clearing firm directors",
                ],
                1,
                "FINRA Rule 5310(a)(1) requires evaluating market character, order size/type, quotation accessibility, and terms of the order.",
            ),
            "exercises": [
                question(
                    "Under FINRA Rule 5310(a)(1), which factors determine Best Execution?",
                    [
                        "Solely the lowest posted clearing commission fee offered by an affiliated wholesale dealer",
                        "Market character, order size/type, number of markets checked, and quote accessibility",
                        "Personal relationships between investment executives and registered exchange clearing members",
                    ],
                    1,
                    "Best execution requires examining market depth, quote access, order size, and multiple venue options.",
                ),
                question(
                    "What does an implementation shortfall benchmark measure in trade execution?",
                    [
                        "The distance in basis points between the arrival benchmark quote and final execution price",
                        "The total annual headline consumer inflation rate reported by the central monetary authority",
                        "The maximum permitted transmission packet size of an automated order routing network protocol",
                    ],
                    0,
                    "Implementation shortfall measures execution slippage against the market price prevailing when the decision to trade was made.",
                ),
            ],
            "terms": [
                {"term": "Best Execution", "definition": "The legal duty requiring brokers to use reasonable diligence to execute customer orders on the most favorable terms available."},
                {"term": "Implementation Shortfall", "definition": "The difference between the market price when an investment decision is initiated and the final executed price, usually expressed in basis points."},
                {"term": "FINRA Rule 5310", "definition": "Financial Industry Regulatory Authority rule governing Best Execution and Interpositioning in securities transactions."},
            ],
            "references": [
                {"title": "FINRA · Rule 5310 Best Execution and Interpositioning", "url": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/5310"},
                {"title": "U.S. SEC · Rule 606 Disclosure of Order Routing Practices", "url": "https://www.sec.gov/tm/faq-rule-606-regulation-nms"},
            ],
        },
        {
            "id": "26.10",
            "part": "4",
            "title": "P-hacking and backtest overfitting",
            "subtitle": "Multiple testing bias, false discovery rates, and quantitative research integrity.",
            "minutes": 25,
            "objective": "Quantify multiple testing bias using Family-Wise Error Rate (FWER) and deflated Sharpe ratio concepts to prevent backtest overfitting.",
            "kind": "applied-study",
            "formula": r"\text{Family-Wise Error Rate (FWER)} = 1 - (1 - \alpha)^N",
            "code": (
                "# Calculate Family-Wise Error Rate (FWER) across N backtest trials\n"
                "alpha = 0.05\n"
                "trials = [1, 5, 10, 20, 30]\n"
                "print('Trials | Family-Wise Error Rate (Probability of False Discovery)')\n"
                "print('-------------------------------------------------------------')\n"
                "for n in trials:\n"
                "    fwer = 1.0 - (1.0 - alpha)**n\n"
                "    print(f'{n:6d} | {fwer * 100:.2f}%')\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "In quantitative finance and algorithmic strategy design, **p-hacking** (also known as data snooping or backtest overfitting) is an integrity failure that masquerades as scientific discovery. When a researcher tests dozens or hundreds of parameter variations until one happens to look profitable on historical data, that apparent 'alpha' is almost always a random statistical artifact.\n\n"
                "Under classical hypothesis testing at significance level $\\alpha = 0.05$, a single test has a 5% chance of falsely rejecting the null hypothesis (a false positive). When $N$ independent strategies or indicator variations are tested, the **Family-Wise Error Rate (FWER)** grows rapidly:\n\n"
                "$$\n"
                r"\mathrm{FWER} = 1 - (1 - \alpha)^N"
                "\n$$\n\n"
                "For $N = 30$ trials, $\\mathrm{FWER} = 1 - (0.95)^{30} \\approx 78.5\\%$. Even if every strategy is pure random noise, there is nearly an 80% chance that at least one strategy appears statistically significant at the $p < 0.05$ level!\n\n"
                "In institutional research, practitioners apply the **Deflated Sharpe Ratio** (Bailey & López de Prado, 2014) or Benjamini-Hochberg False Discovery Rate (FDR) adjustments. In Quanta, all quantitative experiments are tracked in the research registry at `/research` to preserve the full denominator of attempted runs rather than publishing only the cherry-picked winner.\n\n"
                "## A worked example\n\n"
                "An analyst tests 50 moving-average parameter combinations on historical price data. 48 versions produce negative or flat returns, but parameter pair (17, 43) yields an annualized Sharpe ratio of 1.85. The analyst packages this single configuration into an investor pitch deck, concealing the 49 failed trials.\n\n"
                "This violates CFA Standard V(A) (Diligence and Reasonable Basis). Live deployment will inevitably revert to noise, destroying investor capital. Honest research requires reporting the total number of tested variations and adjusting significance thresholds for multiple testing.\n\n"
                "## Work through it yourself\n\n"
                "1. Maintain a complete research log documenting every trial, rejected hypothesis, and failed parameter run.\n"
                "2. Apply multi-hypothesis adjustments (such as Bonferroni or False Discovery Rate) before declaring statistical significance.\n"
                "3. Perform out-of-sample testing on strictly separated, unseen price vintages in `/research`.\n\n"
                "### In the sandbox\n\n"
                "Run the script to observe how testing multiple configurations inflates the false discovery rate toward certainty."
            ),
            "exercise": question(
                "Why does testing 30 strategy configurations without adjustment create an acute risk of false discovery?",
                [
                    "Because executing 30 parallel simulations consumes excessive CPU server computational resources",
                    "Because cumulative probability of uncovering a false positive by pure chance exceeds seventy-five percent",
                    "Because financial market compilers disallow testing more than five strategy indicator parameters concurrently",
                ],
                1,
                "With alpha=0.05, 30 trials yield a family-wise error rate of 1 - (0.95)^30 = 78.5%, making false positive discovery highly probable.",
            ),
            "exercises": [
                question(
                    "Why does unadjusted multiple testing produce false positive trading strategies?",
                    [
                        "Computer operating systems leak virtual memory allocations during long backtesting processes",
                        "Cumulative false positive probability increases exponentially with each unadjusted historical trial",
                        "Securities regulatory agencies prohibit testing more than five quantitative indicators per portfolio",
                    ],
                    1,
                    "Each additional trial increases the likelihood that random historical noise satisfies the significance threshold.",
                ),
                question(
                    "What is the core function of the Deflated Sharpe Ratio in quantitative strategy research?",
                    [
                        "To discount apparent performance based on trial count and non-normal return distributions",
                        "To subtract the national headline inflation rate from gross proprietary trading commissions",
                        "To decrease the physical font formatting dimensions of institutional equity research reports",
                    ],
                    0,
                    "The Deflated Sharpe Ratio discounts apparent performance by accounting for trial count and skewness/kurtosis.",
                ),
            ],
            "terms": [
                {"term": "P-Hacking", "definition": "The misuse of data analysis to search for patterns in data until something appears statistically significant, reporting only the winning trial."},
                {"term": "Family-Wise Error Rate (FWER)", "definition": "The probability of making one or more false discoveries (Type I errors) among all the hypotheses tested."},
                {"term": "Deflated Sharpe Ratio", "definition": "A statistical framework developed by Bailey and López de Prado that discounts Sharpe ratios based on the number of trials attempted."},
            ],
            "references": [
                {"title": "Bailey & López de Prado · The Deflated Sharpe Ratio (2014)", "url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551"},
                {"title": "Harvey, Liu & Zhu · ... and the Cross-Section of Expected Returns (2016)", "url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2249314"},
            ],
        },
        {
            "id": "26.11",
            "part": "4",
            "title": "Point-in-time data hygiene and corporate actions",
            "subtitle": "Preventing retroactive restatement leakage and survivorship distortions in historical testing.",
            "minutes": 25,
            "objective": "Identify retroactive restatements in financial databases and enforce point-in-time filing availability dates.",
            "kind": "applied-study",
            "formula": r"\text{Point-in-Time Availability: } t_{\text{decision}} \ge t_{\text{SEC/IDX public release}} \quad (\text{not fiscal period end})",
            "code": (
                "# Point-in-time filing date validation check\n"
                "decision_date = '2026-03-15'\n"
                "filing_date_original = '2026-02-28'\n"
                "eps_as_reported = 2.00\n"
                "filing_date_restated = '2026-11-15'\n"
                "eps_restated = 1.20\n"
                "\n"
                "print(f'Decision Date: {decision_date}')\n"
                "if decision_date >= filing_date_original:\n"
                "    print(f'Known EPS on Decision Date: ${eps_as_reported:.2f}')\n"
                "if decision_date < filing_date_restated:\n"
                "    print(f'Restated EPS of ${eps_restated:.2f} was UNKNOWN to the market on decision date.')\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "A backtest that relies on historical financial data must reflect what market participants actually knew on the decision date—not what was disclosed months or years later. Two major flaws corrupt historical datasets:\n\n"
                "1. **Restatement Look-Ahead Leakage**: Companies routinely restate previous financial results due to accounting errors, auditor adjustments, or changes in revenue recognition standards. If your database retroactively replaces the original as-reported numbers with restated figures, your backtest is trading on future information that did not exist in the market at that time.\n"
                "2. **Availability Lag**: The end of a fiscal quarter (e.g. December 31) is not when the market learns the quarterly earnings. Public companies typically file annual reports (10-K or Laporan Keuangan Tahunan) 45 to 90 days after period end. Assuming financial data is available on the period-end date is a severe look-ahead leak.\n\n"
                "$$\n"
                r"\text{Information Set}(t) = \{F_{i, \tau} \mid \tau_{\text{public publication}} \le t\}"
                "\n$$\n\n"
                "True institutional quantitative databases are **point-in-time (PIT)**: they preserve every revision vintage with its exact public release timestamp, ensuring zero look-ahead bias.\n\n"
                "## A worked example\n\n"
                "A firm finishes its fiscal year on December 31, 2025. On February 28, 2026, it files its audited annual report reporting EPS of $2.00. In November 2026, an accounting inquiry forces the company to restate 2025 EPS down to $1.20.\n\n"
                "If a backtest algorithm simulated a rebalance on March 15, 2026 using the restated database, it would use $1.20—an information set that was physically impossible for any market participant to know on March 15. A point-in-time database correctly supplies $2.00 on March 15 and introduces the $1.20 revision only after November 15.\n\n"
                "## Work through it yourself\n\n"
                "1. Always query databases using the publication timestamp (`file_date` or `release_date`) rather than `fiscal_period_end`.\n"
                "2. Verify whether corporate actions (splits, dividends) are applied prospectively without retroactively warping raw historical OHLC volume.\n"
                "3. Document data provenance in your compliance log.\n\n"
                "### In the sandbox\n\n"
                "Run the script to see how point-in-time filtering prevents retroactive information leakage."
            ),
            "exercise": question(
                "Why must quantitative fundamental backtests strictly use point-in-time datasets rather than restated financial series?",
                [
                    "Because point-in-time databases require smaller file storage space on local computer hard drives",
                    "Because restatements introduce retroactive revisions that were unknown to market participants on historical dates",
                    "Because accounting standard setters mandate that corporate annual reports must be deleted after five years",
                ],
                1,
                "Point-in-time datasets preserve the exact information available on each historical date, eliminating retroactive look-ahead leakage.",
            ),
            "exercises": [
                question(
                    "Why are point-in-time datasets required for accurate fundamental backtesting?",
                    [
                        "They compress binary data files to optimize network download bandwidth across large distributed cloud clusters",
                        "They prevent look-ahead bias by tracking the exact publication dates when disclosures were released",
                        "They permanently remove stock price quotations from corporate balance sheet filings across all global markets",
                    ],
                    1,
                    "Point-in-time data ensures historical simulations use only the information available to the public at each historical decision point.",
                ),
                question(
                    "If a company's fiscal quarter ends on March 31, when should an algorithm assume earnings data is available?",
                    [
                        "Immediately at the market close on March 31 without waiting for external auditor reviews to be completed",
                        "On the exact date and timestamp when the official regulatory filing is publicly disseminated",
                        "On the first business day of the subsequent calendar year following board dividend declarations",
                    ],
                    1,
                    "Financial data cannot be used in a simulation prior to its official public dissemination date and timestamp.",
                ),
            ],
            "terms": [
                {"term": "Point-in-Time (PIT) Data", "definition": "A historical database structure that stores information according to when it was publicly released and known, rather than the period it covers."},
                {"term": "Financial Restatement", "definition": "The formal revision of previously issued financial statements to correct material errors or reflect accounting adjustments."},
                {"term": "Look-Ahead Bias", "definition": "A backtesting error where information from the future is inadvertently used to make historical simulated trading decisions."},
            ],
            "references": [
                {"title": "U.S. SEC · EDGAR Public Dissemination Service Information", "url": "https://www.sec.gov/edgar/searchedgar/accessing-edgar-data.htm"},
                {"title": "CFA Institute · Quantitative Methods in Practice: Financial Statement Lags", "url": "https://www.cfainstitute.org/research/foundation/publications"},
            ],
        },
        {
            "id": "26.12",
            "part": "4",
            "title": "Objective risk capacity versus emotional risk tolerance",
            "subtitle": "FINRA Rule 2111, Reg BI care obligations, and balance sheet survival runway.",
            "minutes": 25,
            "objective": "Distinguish between objective balance sheet risk capacity and subjective emotional risk tolerance under suitability and Reg BI standards.",
            "kind": "applied-study",
            "formula": r"\text{Survival Runway (months)} = \frac{\text{Liquid Unencumbered Reserves}}{\text{Monthly Non-Discretionary Debt \& Cash Burn}}",
            "code": (
                "# Calculate objective survival runway and debt service coverage\n"
                "liquid_reserves = 60_000_000\n"
                "monthly_fixed_costs = 12_000_000\n"
                "monthly_debt_service = 6_000_000\n"
                "monthly_burn = monthly_fixed_costs + monthly_debt_service\n"
                "runway_months = liquid_reserves / monthly_burn\n"
                "print(f'Total Monthly Fixed Obligations: Rp {monthly_burn:,.0f}')\n"
                "print(f'Objective Survival Runway: {runway_months:.1f} months')\n"
                "if runway_months < 6.0:\n"
                "    print('VULNERABILITY: Risk capacity is constrained regardless of emotional risk tolerance.')\n"
                "else:\n"
                "    print('ADEQUATE: Sufficient balance sheet cushion to sustain market volatility.')\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "In wealth management, corporate finance, and personal investing, a dangerous conflation often occurs between **risk tolerance** and **risk capacity**:\n\n"
                "1. **Risk Tolerance (Subjective/Emotional)**: How an individual feels about volatility. A high risk tolerance means the investor does not panic when their portfolio drops 25% on paper.\n"
                "2. **Risk Capacity (Objective/Financial)**: What the investor's balance sheet can actually endure without catastrophic insolvency. Risk capacity is determined by contractual debt payments, liquidity needs, emergency reserves, and near-term cash liabilities.\n\n"
                "Under FINRA Rule 2111 (Suitability), the SEC Regulation Best Interest (Reg BI) Care Obligation (17 CFR 240.15l-1), and Indonesian consumer protection regulations (POJK No. 6/POJK.07/2022), financial professionals have an affirmative legal duty to evaluate objective risk capacity. Recommending volatile, illiquid, or high-risk assets to a client who needs cash within six months violates conduct standards, even if the client enthusiastically signs an aggressive risk tolerance questionnaire.\n\n"
                "$$\n"
                r"\text{Prudent Allocation Limit} \le \min(\text{Emotional Tolerance}, \text{Objective Capacity})"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A small business owner has Rp60 million in liquid reserves and monthly non-discretionary commitments of Rp18 million (Rp12m shop lease/salaries + Rp6m bank loan installment). The owner's objective survival runway is:\n\n"
                "$$\n"
                r"\text{Runway} = \frac{\text{Rp } 60{,}000{,}000}{\text{Rp } 18{,}000{,}000/\text{month}} = 3.33 \text{ months}"
                "\n$$\n\n"
                "Even if the owner claims an 'aggressive' risk tolerance and wants to invest Rp50 million in high-beta equities, their financial risk capacity is minimal. A 25% market drawdown combined with a minor sales dip would force liquidation of equity holdings at the market trough to meet payroll and debt service, converting a temporary paper loss into permanent ruin.\n\n"
                "## Work through it yourself\n\n"
                "1. Calculate your non-discretionary monthly cash burn (fixed expenses + loan amortization).\n"
                "2. Ensure at least 6 months of cash runway is ring-fenced in liquid, low-risk instruments before allocating to volatile assets.\n"
                "3. Document that asset allocations respect objective financial capacity before subjective appetite.\n\n"
                "### In the sandbox\n\n"
                "Run the script to compute liquid survival runway under monthly cash obligations."
            ),
            "exercise": question(
                "Under suitability standards (FINRA Rule 2111 / Reg BI), why does objective risk capacity take precedence over emotional risk tolerance?",
                [
                    "Because statutory regulations strictly mandate that all individual retail investors must hold only government bonds",
                    "Because regardless of emotional courage, an investor with low cash runway can be forced into liquidation during a drawdown",
                    "Because emotional risk profiling questionnaires have been ruled unconstitutional under federal appellate law",
                ],
                1,
                "Objective cash obligations govern risk capacity; an aggressive emotional appetite cannot prevent forced liquidation if cash runs out.",
            ),
            "exercises": [
                question(
                    "What is the key distinction between risk capacity and risk tolerance?",
                    [
                        "Risk tolerance measures balance sheet runway; risk capacity measures psychological feelings",
                        "Risk capacity is objective loss endurance; risk tolerance is subjective comfort with volatility",
                        "There is no legal difference; both terms refer to the identical mathematical portfolio deviation",
                    ],
                    1,
                    "Risk capacity measures objective balance sheet resilience; risk tolerance measures subjective psychological response to volatility.",
                ),
                question(
                    "Under POJK No. 6/POJK.07/2022 and Reg BI, what is the legal duty of a financial adviser?",
                    [
                        "To recommend investment products that maximize up-front sales commissions and trailing kickbacks for the distributor",
                        "To ensure recommendations align with client financial capacity, time horizon, and liquidity needs",
                        "To guarantee to retail clients that recommended equity portfolios will never experience a negative quarterly return",
                    ],
                    1,
                    "Advisors must ensure recommendations match the client's financial capacity, liquidity constraints, and investment horizon.",
                ),
            ],
            "terms": [
                {"term": "Risk Capacity", "definition": "The objective financial ability of an individual or business to absorb monetary loss without altering living standards or facing insolvency."},
                {"term": "Risk Tolerance", "definition": "The subjective, psychological willingness of an investor to accept price volatility and paper losses."},
                {"term": "FINRA Rule 2111 (Suitability)", "definition": "Regulatory rule requiring brokers to have a reasonable basis to believe a recommended transaction is suitable based on the client's investment profile."},
            ],
            "references": [
                {"title": "FINRA · Rule 2111 Suitability FAQ and Guidance", "url": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/2111"},
                {"title": "U.S. SEC · Regulation Best Interest (Reg BI) 17 CFR 240.15l-1", "url": "https://www.sec.gov/regulation-best-interest"},
                {"title": "OJK · POJK No. 6/POJK.07/2022 Perlindungan Konsumen Sektor Jasa Keuangan", "url": "https://ojk.go.id/id/regulasi/Pages/POJK-Nomor-6-POJK.07-2022.aspx"},
            ],
        },
        {
            "id": "26.13",
            "part": "4",
            "title": "Detecting Ponzi schemes and unauthorized instructions",
            "subtitle": "Guaranteed yields, opaque custody, Satgas PASTI red flags, and fraud defense.",
            "minutes": 25,
            "objective": "Identify warning signs of investment fraud, Ponzi schemes, and illegal investment offerings using regulatory fraud typologies.",
            "kind": "applied-study",
            "formula": r"\text{Ponzi Sustainability: } \text{Payouts}(t) > \text{Inflows}(t) \implies \text{Insolvency Deficit}",
            "code": (
                "# Modeling Ponzi cash exhaustion as new depositor inflows decline\n"
                "monthly_guaranteed_return = 0.05\n"
                "investor_principal = 100_000_000\n"
                "cash_reserve = 50_000_000\n"
                "inflows = [20_000_000, 15_000_000, 8_000_000, 2_000_000, 0]\n"
                "print('Month | Inflow | Payout Due | Reserve Status')\n"
                "print('--------------------------------------------')\n"
                "month = 1\n"
                "for inflow in inflows:\n"
                "    payout = (investor_principal + (month * 10_000_000)) * monthly_guaranteed_return\n"
                "    cash_reserve = cash_reserve + inflow - payout\n"
                "    status = 'SOLVENT' if cash_reserve > 0 else 'COLLAPSED'\n"
                "    print(f'{month:5d} | {inflow:10,d} | {int(payout):10,d} | {status}')\n"
                "    if cash_reserve <= 0:\n"
                "        break\n"
                "    month = month + 1\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "Every year, billions of dollars of individual and enterprise capital are destroyed by fraudulent investment schemes. While the branding evolves—from high-yield forex syndicates to algorithmic crypto bots and fake commodity cooperatives—the underlying mathematical architecture of a **Ponzi scheme** remains unchanged:\n\n"
                "**Money from new investors is used to pay artificial 'returns' to earlier investors.** No legitimate underlying economic value or market yield is generated.\n\n"
                "Regulators worldwide, including the SEC, CFTC, and Indonesia's **Satgas PASTI** (Satuan Tugas Pemberantasan Aktivitas Keuangan Ilegal, formerly Satgas Waspada Investasi), publish clear red flag indicators of illegal investment schemes:\n\n"
                "1. **Guaranteed Abnormally High Returns**: Promising 2% to 5% monthly return with 'zero market risk'. In real financial markets, higher returns are inextricably linked to higher risk; guaranteed double-digit risk-free returns do not exist.\n"
                "2. **Consistent Performance Through Down Markets**: Claiming steady gains every single month, even during historic market drawdowns.\n"
                "3. **Unregistered Entities and Unlicensed Promoters**: Failing to hold valid licenses from OJK, Bappebti, the SEC, or FINRA.\n"
                "4. **Opaque 'Proprietary' Strategies**: Explaining high profits with vague jargon ('secret AI trading formula', 'arbitrage algorithms') while refusing independent third-party custodial verification.\n"
                "5. **Difficulty Cashing Out**: Delaying withdrawals, offering bonus incentives to reinvest, or imposing exorbitant exit penalties.\n\n"
                "$$\n"
                r"\text{Promise: High Return} \land \text{Zero Volatility} \land \text{No Regulated Custodian} \implies \text{Fraud Red Flag}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A local trading syndicate invites an MSME business owner to deposit Rp100 million, promising a guaranteed 5% monthly payout (79.6% APY compounded). The promoter shows screenshots of successful withdrawals from other members. However, the syndicate is not registered with OJK or Bappebti, and funds are deposited into a personal bank account rather than a segregated custodian.\n\n"
                "This possesses all five classic fraud red flags. As modeled in the code, the moment new depositor growth slows, the scheme runs out of cash to fund monthly payouts and collapses, leaving late depositors with total capital loss.\n\n"
                "## Work through it yourself\n\n"
                "1. Always check the regulator's registry (e.g. OJK Sipendikar, Satgas PASTI, SEC EDGAR, or FINRA BrokerCheck) before sending funds.\n"
                "2. Confirm that funds are received by a licensed, segregated custodian bank in your own name.\n"
                "3. Never execute financial transactions based on unverified social media tips or unsolicited messaging groups.\n\n"
                "### In the sandbox\n\n"
                "Run the script to see how a Ponzi scheme mathematically collapses as new depositor inflows decline."
            ),
            "exercise": question(
                "Which combination of characteristics represents a definitive warning sign of an illegal Ponzi investment scheme?",
                [
                    "A mutual fund reporting negative returns during a general economic recession while using regulated bank custody",
                    "Guaranteed high monthly returns, zero reported down months, and lack of an independently licensed custodian",
                    "Comprehensive quarterly financial reports detailing market volatility, trading costs, and asset depreciation",
                ],
                1,
                "Guaranteed high returns with zero volatility and opaque or personal custody are universal hallmarks of fraudulent Ponzi structures.",
            ),
            "exercises": [
                question(
                    "What is a primary indicator of fraudulent investment schemes according to OJK Satgas PASTI and the SEC?",
                    [
                        "Clear disclosure of downside volatility and potential capital impairment in the formal prospectus",
                        "Promised high returns with guaranteed principal protection and zero market risk",
                        "Holding client capital in segregated accounts at regulated commercial banks",
                    ],
                    1,
                    "Guaranteed returns and zero-risk claims violate basic financial principles and indicate fraudulent structures.",
                ),
                question(
                    "What happens mathematically in a Ponzi scheme when new depositor growth declines?",
                    [
                        "The investment syndicate switches to holding risk-free sovereign treasury bills with central banks",
                        "Cash reserves are exhausted by guaranteed payout obligations, triggering rapid liquidity collapse",
                        "The fund management team lowers advisory fees to attract institutional institutional capital",
                    ],
                    1,
                    "Without legitimate investment earnings, a Ponzi scheme becomes illiquid and collapses once new capital inflows drop.",
                ),
            ],
            "terms": [
                {"term": "Ponzi Scheme", "definition": "A fraudulent investing scam where returns are paid to existing investors from funds contributed by new investors rather than legitimate profits."},
                {"term": "Satgas PASTI", "definition": "Indonesia's inter-agency Task Force for the Eradication of Illegal Financial Activities (formerly Satgas Waspada Investasi), coordinated by OJK."},
                {"term": "Custodial Verification", "definition": "Independent confirmation from a regulated bank or clearinghouse that client assets actually exist in segregated accounts."},
            ],
            "references": [
                {"title": "U.S. SEC · Investor.gov: How to Avoid Investment Fraud", "url": "https://www.investor.gov/protect-your-investments/fraud/how-avoid-fraud"},
                {"title": "OJK · Siaran Pers Satgas PASTI Hentikan Aktivitas Entitas Ilegal", "url": "https://ojk.go.id/id/berita-dan-kegiatan/siaran-pers/Pages/default.aspx"},
            ],
        },
        {
            "id": "26.14",
            "part": "4",
            "title": "Audit trails and regulatory whistleblowing",
            "subtitle": "Immutable records, Exchange Act §21F, and anti-retaliation protections under Digital Realty.",
            "minutes": 25,
            "objective": "Understand statutory record-keeping rules and whistleblower protections under Exchange Act Section 21F and judicial precedents.",
            "kind": "applied-study",
            "formula": r"\text{Hash-Chained Audit Log: } H_t = \mathrm{SHA256}(H_{t-1} \parallel \text{Event}_t \parallel \text{Timestamp}_t)",
            "code": (
                "# Simulating an append-only, tamper-evident audit log checksum\n"
                "events = [\n"
                "    '10:00:00:SUBMIT_ORDER:1000 BBCA @ 10000',\n"
                "    '10:00:02:PRE_TRADE_APPROVE:Collars checked',\n"
                "    '10:00:03:FILL_CONFIRMED:1000 BBCA filled',\n"
                "]\n"
                "checksum = 1000003\n"
                "count = 0\n"
                "for event in events:\n"
                "    count = count + 1\n"
                "    checksum = (checksum * 31 + len(event)) % 1000000007\n"
                "    print(f'Event {count}: {event} | Checksum: {checksum}')\n"
                "print('Tamper check: Any historical modification invalidates downstream checksums.')\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "In financial operations, an undocumented action is legally considered an unperformed action. Regulatory bodies enforce strict record-keeping rules (e.g. SEC Rule 17a-4 and CFTC Rule 1.31) requiring firms to maintain tamper-evident, append-only records of all trade instructions, communications, and compliance approvals for at least six years.\n\n"
                "When illicit activity occurs within an organization, statutory frameworks protect individuals who report violations. Under **Section 21F of the Securities Exchange Act of 1934** (enacted under the Dodd-Frank Act):\n\n"
                "1. **Bounties**: Qualified whistleblowers who voluntarily provide original information leading to successful enforcement actions resulting in monetary sanctions exceeding $1 million are entitled to receive **10% to 30%** of the collected funds.\n"
                "2. **Confidentiality**: Whistleblowers can submit information anonymously through an attorney.\n"
                "3. **Anti-Retaliation Protections**: Employers are strictly prohibited from discharging, demoting, suspending, harassing, or discriminating against employees who report securities violations.\n\n"
                "**Crucial Legal Precedent: *Digital Realty Trust, Inc. v. Somers* (2018)**\n"
                "In a landmark unanimous ruling, the U.S. Supreme Court held that the anti-retaliation protections of Dodd-Frank Section 21F apply **only** to individuals who have provided information directly to the SEC. An employee who reports misconduct solely to internal management or internal compliance hotlines does not qualify as a statutory whistleblower under Section 21F and cannot sue under its anti-retaliation provisions. Understanding this jurisdictional distinction is vital for practitioners.\n\n"
                "## A worked example\n\n"
                "A quantitative risk analyst discovers that a trading desk is concealing mark-to-market losses by manually editing valuation spreadsheets. The analyst creates an immutable contemporaneous record of the spreadsheets and timestamps.\n\n"
                "Under *Digital Realty*, if the analyst reports only to the firm's CEO and is fired the following week, they cannot claim Section 21F anti-retaliation remedies in federal court. However, if the analyst submits a Form TCR directly to the SEC's Office of the Whistleblower, statutory anti-retaliation protections attach immediately.\n\n"
                "## Work through it yourself\n\n"
                "1. Maintain contemporaneous written logs with exact dates, times, and documentary attachments.\n"
                "2. Review internal escalation pathways alongside statutory whistleblower reporting requirements.\n"
                "3. Implement append-only logging for critical algorithmic state transitions.\n\n"
                "### In the sandbox\n\n"
                "Run the script to inspect how checksum chaining prevents retroactive tampering in compliance audit logs."
            ),
            "exercise": question(
                "Under the U.S. Supreme Court ruling in Digital Realty Trust v. Somers (2018), when do Dodd-Frank Section 21F anti-retaliation protections attach?",
                [
                    "Whenever an employee reports ethical concerns informally to an internal human resources representative",
                    "Only after the whistleblower has provided information directly to the Securities and Exchange Commission (SEC)",
                    "Automatically upon signing a standard employment contract with a registered broker-dealer firm",
                ],
                1,
                "In Digital Realty, the Supreme Court ruled that Section 21F statutory protections apply only to whistleblowers who report to the SEC.",
            ),
            "exercises": [
                question(
                    "Under Digital Realty Trust v. Somers (2018), what is required to receive Section 21F whistleblower protection?",
                    [
                        "Publishing confidential corporate spreadsheets on an external anonymous internet message forum",
                        "Submitting original information regarding securities violations directly to the SEC",
                        "Reporting concerns exclusively to the internal corporate compliance department and waiting one year",
                    ],
                    1,
                    "The Supreme Court held that Dodd-Frank Section 21F anti-retaliation protections require reporting directly to the SEC.",
                ),
                question(
                    "Why must institutional trading systems maintain append-only, tamper-evident audit logs?",
                    [
                        "To consume unused hard drive storage capacity before the end of the corporate fiscal year across data centers",
                        "To ensure complete reconstructability of algorithmic decisions and prevent retroactive alteration of records",
                        "To eliminate the need for supervisory risk officers to monitor electronic trading systems across market venues",
                    ],
                    1,
                    "Tamper-evident logs guarantee that investigators and auditors can reconstruct the exact historical sequence of events.",
                ),
            ],
            "terms": [
                {"term": "Section 21F (Exchange Act)", "definition": "Statutory whistleblower provision created by Dodd-Frank providing financial awards and anti-retaliation protections for reporting securities violations to the SEC."},
                {"term": "Digital Realty v. Somers", "definition": "2018 U.S. Supreme Court decision holding that Dodd-Frank anti-retaliation protections apply only to individuals who report violations directly to the SEC."},
                {"term": "Audit Trail", "definition": "A step-by-step, chronological, tamper-evident record of all transactions, approvals, and data transformations."},
            ],
            "references": [
                {"title": "U.S. SEC · Office of the Whistleblower Overview & Form TCR", "url": "https://www.sec.gov/whistleblower"},
                {"title": "Legal Information Institute · 15 U.S. Code § 78u-6 Securities Whistleblower Incentives", "url": "https://www.law.cornell.edu/uscode/text/15/78u-6"},
                {"title": "Supreme Court of the United States · Digital Realty Trust v. Somers (2018)", "url": "https://www.supremecourt.gov/opinions/17pdf/16-1276_bap6.pdf"},
            ],
        },
        {
            "id": "26.15",
            "part": "4",
            "title": "Cybersecurity and credential stewardship",
            "subtitle": "Safeguarding API secret keys, least privilege, Reg S-P amendments, and Indonesian PDP compliance.",
            "minutes": 25,
            "objective": "Apply cybersecurity hygiene: secret key protection, least privilege scoping, SEC Regulation S-P breach notification, and UU 27/2022 compliance.",
            "kind": "applied-study",
            "formula": r"\text{API Key Hygiene} = \text{Read/Trade Scopes Only} \land \text{Withdrawals Disabled} \land \text{IP Whitelisted}",
            "code": (
                "# Verifying API key security configuration and least-privilege scoping\n"
                "api_key_config = {\n"
                "    'key_id': 'KEY-849201',\n"
                "    'allow_withdrawals': False,\n"
                "    'ip_whitelist_enforced': True,\n"
                "    'created_days_ago': 45,\n"
                "}\n"
                "def audit_api_key(config):\n"
                "    if config['allow_withdrawals']:\n"
                "        return 'FATAL VIOLATION: API keys must NEVER have withdrawal permissions!'\n"
                "    if not config['ip_whitelist_enforced']:\n"
                "        return 'WARNING: Unrestricted IP access. Restrict key to designated server IP.'\n"
                "    if config['created_days_ago'] > 90:\n"
                "        return 'WARNING: Key age exceeds 90 days. Key rotation required.'\n"
                "    return 'COMPLIANT: API key adheres to least privilege and security hygiene.'\n"
                "\n"
                "print(audit_api_key(api_key_config))\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "In programmatic trading and digital asset management, an API key is the mathematical equivalent of cash. If an algorithmic trader stores API secret keys in plain text in a public repository or shares them via unencrypted chat, malicious actors can drain accounts or manipulate order books in seconds.\n\n"
                "Robust cybersecurity stewardship requires strict adherence to three core principles:\n\n"
                "1. **Principle of Least Privilege**: An API key used by an algorithm to query market data should have read-only permissions. A key used to execute orders should have trade execution permissions only. **Trading API keys must NEVER have withdrawal or transfer permissions**.\n"
                "2. **IP Whitelisting & Environment Isolation**: All programmatic endpoints should restrict order routing to designated, static server IP addresses. API secrets must be loaded from secure environment variables or secret vaults, never hard-coded into source files.\n"
                "3. **Regulatory Safeguards**: Under the **SEC Regulation S-P 2024 Amendments**, registered broker-dealers and investment advisers must implement written incident response programs capable of detecting, responding to, and notifying affected customers within **30 days** of a significant data breach. In Indonesia, **Undang-Undang No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP)** imposes civil and criminal liability on data controllers who fail to protect personal financial and identification data.\n\n"
                "$$\n"
                r"\text{Secure Credential} \implies \text{Vault Storage} \land \text{No Withdrawal Scope} \land \text{90-Day Rotation}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A junior developer accidentally commits a script containing live exchange API credentials to a public GitHub repository. Within 90 seconds, automated scrapers discover the secret key.\n\n"
                "Scenario A (Unsecured): The key had full permissions including withdrawals without IP restrictions. Attackers initiate transfers and drain $50,000 before the developer notices.\n\n"
                "Scenario B (Secured under Least Privilege): The key was strictly scoped to order-placement only, withdrawals were disabled, and execution was locked to the production server IP. The attacker's unauthorized IP is rejected at the gateway with zero loss.\n\n"
                "## Work through it yourself\n\n"
                "1. Audit every API key connected to your trading and business accounts; revoke any key with withdrawal permissions.\n"
                "2. Implement Multi-Factor Authentication (MFA) using hardware keys or authenticator apps (avoid SMS verification).\n"
                "3. Rotate API credentials every 90 days and enforce IP restrictions.\n\n"
                "### In the sandbox\n\n"
                "Run the script to audit API key privilege configurations against institutional security standards."
            ),
            "exercise": question(
                "When configuring an API key for an automated trading algorithm, which security setting is critical to prevent total fund exfiltration?",
                [
                    "Enabling unrestricted withdrawal permissions so the algorithm can autonomously rebalance capital reserves",
                    "Disabling all withdrawal permissions and restricting execution to designated whitelisted IP addresses",
                    "Labeling the API key with a misleading test filename in order to confuse potential network eavesdroppers",
                ],
                1,
                "Trading API keys should strictly forbid withdrawal capabilities and be locked to specific server IPs to prevent theft.",
            ),
            "exercises": [
                question(
                    "What is the Principle of Least Privilege in algorithmic cybersecurity?",
                    [
                        "Granting all employees administrator-level server permissions across all internal systems",
                        "Restricting system permissions and API scopes to the minimum necessary for the specific function",
                        "Sharing trading execution passwords across company communication channels for operational redundancy",
                    ],
                    1,
                    "Least privilege dictates that credentials and keys possess only the minimum permissions necessary for their specific tasks.",
                ),
                question(
                    "Under the SEC Regulation S-P 2024 amendments, what is the notification requirement for financial institutions following a significant breach?",
                    [
                        "Notifying affected individuals within thirty days of becoming aware of the security breach incident",
                        "Reporting the security incident only in the subsequent calendar year's standard annual tax disclosures",
                        "Notifying law enforcement only if aggregate client financial losses exceed ten million dollars",
                    ],
                    0,
                    "Regulation S-P mandates formal customer notification within 30 days when sensitive customer information has been accessed without authorization.",
                ),
            ],
            "terms": [
                {"term": "Principle of Least Privilege", "definition": "A computer security concept in which a user or program is given only the minimum privileges and permissions necessary to perform its job."},
                {"term": "Regulation S-P (SEC)", "definition": "Federal regulation governing the privacy and safeguarding of customer financial records, updated in 2024 with mandatory 30-day breach notification."},
                {"term": "UU No. 27/2022 (UU PDP)", "definition": "Indonesian Personal Data Protection Law establishing comprehensive legal standards and penalties for protecting personal data."},
            ],
            "references": [
                {"title": "U.S. SEC · Adoption of Final Rule: Regulation S-P Amendments (2024)", "url": "https://www.sec.gov/news/press-release/2024-58"},
                {"title": "JDIH BPK RI · Undang-Undang No. 27 Tahun 2022 tentang Pelindungan Data Pribadi", "url": "https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022"},
            ],
        },
        {
            "id": "26.16",
            "part": "4",
            "title": "Supervisory systems and written procedures",
            "subtitle": "FINRA Rule 3110: supervisory hierarchies, maker-checker controls, and operational governance.",
            "minutes": 25,
            "objective": "Understand the architecture of supervisory systems under FINRA Rule 3110 and implement maker-checker controls for algorithmic deployments.",
            "kind": "applied-study",
            "formula": r"\text{Deployment Gate: } \text{Maker}(\text{Dev}) \ne \text{Checker}(\text{Risk Principal}) \implies \text{Approval Valid}",
            "code": (
                "# Maker-Checker dual authorization verification gate\n"
                "maker = 'dev_alex'\n"
                "checker = 'risk_sarah'\n"
                "backtest_reviewed = True\n"
                "def verify_deployment(dev, reviewer, reviewed):\n"
                "    if dev == reviewer:\n"
                "        return 'REJECT: Maker and Checker must be independent individuals.'\n"
                "    if not reviewed:\n"
                "        return 'REJECT: Backtest multi-testing review missing.'\n"
                "    return f'APPROVED: Strategy deployment cleared for live execution by {reviewer}.'\n"
                "\n"
                "print(verify_deployment(maker, checker, backtest_reviewed))\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "A firm cannot prevent misconduct or catastrophic software glitches through good intentions alone. Under **FINRA Rule 3110**, every registered broker-dealer must establish and maintain a system to supervise the activities of each associated person that is reasonably designed to achieve compliance with applicable securities laws and regulations.\n\n"
                "Core requirements of FINRA Rule 3110 include:\n"
                "1. **Written Supervisory Procedures (WSPs)**: Documenting who is responsible for each operational area, what supervisory reviews are conducted, and how often they take place.\n"
                "2. **Designated Principals**: Assigning qualified supervisory principals with clear authority to inspect trades, approve communications, and halt non-compliant operations.\n"
                "3. **Annual Supervisory Review**: Conducting comprehensive annual internal audits of the supervisory system.\n\n"
                "While FINRA Rule 3110 formally binds registered member broker-dealers, its principles are universal across quantitative hedge funds, proprietary trading desks, and corporate finance teams. In particular, institutional operations enforce **Maker-Checker controls**: no algorithm or financial model can be deployed to live production by the developer alone; an independent risk principal or supervisor must review and approve the parameters before live capital is committed.\n\n"
                "$$\n"
                r"\text{Maker} \neq \text{Checker} \implies \text{Mitigation of Unilateral Operational Rogue Risk}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A quantitative developer designs an automated arbitrage model and pushes it straight to the live exchange server without code review. A misplaced decimal point in the order sizing function multiplies trade quantities by 100×, causing millions in unauthorized exposure within minutes.\n\n"
                "Under a compliant supervisory structure, the deployment pipeline enforces a maker-checker gate: the developer (maker) submits the pull request, but only a designated risk officer (checker) can unlock production execution after verifying pre-trade risk caps and unit tests.\n\n"
                "## Work through it yourself\n\n"
                "1. Identify the supervisory chain in your team or business.\n"
                "2. Enforce four-eyes review (maker-checker) on all live code deployments and financial disbursements.\n"
                "3. Document operational procedures in written, version-controlled compliance guidelines.\n\n"
                "### In the sandbox\n\n"
                "Run the script to verify maker-checker dual authorization logic."
            ),
            "exercise": question(
                "Under FINRA Rule 3110 and institutional governance standards, what is the core purpose of a Maker-Checker control?",
                [
                    "To guarantee that two software developers receive equal credit on marketing brochures",
                    "To prevent unilateral errors or rogue actions by requiring independent review and authorization",
                    "To double the mathematical execution speed of automated high-frequency order routers",
                ],
                1,
                "Maker-checker controls eliminate single-point operational risk by requiring an independent reviewer to authorize actions.",
            ),
            "exercises": [
                question(
                    "Under FINRA Rule 3110, what must a member firm establish and maintain?",
                    [
                        "A physical member-only trading floor facility located in a recognized metropolitan financial district",
                        "A written supervisory system reasonably designed to achieve compliance with applicable securities laws",
                        "An exclusive automated algorithmic market-making software program operating on proprietary exchange networks",
                    ],
                    1,
                    "Rule 3110 mandates establishing, maintaining, and enforcing written supervisory procedures across all business operations.",
                ),
                question(
                    "Why should software developers be prohibited from unilaterally deploying trading algorithms to live production?",
                    [
                        "Software developers do not hold registered academic credentials in professional computer programming disciplines",
                        "To prevent unchecked software bugs or rogue risk limit bypasses through independent four-eyes oversight",
                        "Because securities exchanges require all computer algorithms to be handwritten by corporate compliance attorneys",
                    ],
                    1,
                    "Four-eyes review ensures that risk collars and code logic are verified independently before capital is committed.",
                ),
            ],
            "terms": [
                {"term": "FINRA Rule 3110", "definition": "Regulatory rule mandating that broker-dealer firms maintain a written supervisory system to oversee all associated persons and business operations."},
                {"term": "Maker-Checker", "definition": "An operational control principle requiring that any high-risk action or deployment initiated by one person (the maker) must be approved by an independent second person (the checker)."},
                {"term": "Written Supervisory Procedures (WSPs)", "definition": "A formal, auditable manual outlining a firm's supervisory policies, designated principals, and compliance workflows."},
            ],
            "references": [
                {"title": "FINRA · Rule 3110 Supervision Standards and Guidelines", "url": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/3110"},
                {"title": "FINRA · Algorithmic Trading Supervisory Responsibilities (Notice 15-09)", "url": "https://www.finra.org/rules-guidance/notices/15-09"},
            ],
        },
        {
            "id": "26.17",
            "part": "4",
            "title": "ESG and non-financial disclosure integrity",
            "subtitle": "SEC Names Rule, EU SFDR, Indonesian TKBI, and eliminating greenwashing.",
            "minutes": 25,
            "objective": "Identify greenwashing in investment products and apply the SEC 80% Names Rule, EU SFDR, and Indonesian TKBI standards.",
            "kind": "applied-study",
            "formula": r"\text{Names Rule Compliance: } \frac{\text{Eligible Mandate Assets}}{\text{Total Portfolio Value}} \ge 80\%",
            "code": (
                "# SEC 80% Names Rule compliance validation\n"
                "portfolio = [\n"
                "    {'asset': 'Solar Manufacturer', 'value': 35_000_000, 'esg_qualified': True},\n"
                "    {'asset': 'Wind Turbine Systems', 'value': 25_000_000, 'esg_qualified': True},\n"
                "    {'asset': 'Clean Water Utility', 'value': 15_000_000, 'esg_qualified': True},\n"
                "    {'asset': 'Fossil Fuel Conglomerate', 'value': 25_000_000, 'esg_qualified': False},\n"
                "]\n"
                "total_portfolio = 0\n"
                "esg_total = 0\n"
                "for a in portfolio:\n"
                "    total_portfolio = total_portfolio + a['value']\n"
                "    if a['esg_qualified']:\n"
                "        esg_total = esg_total + a['value']\n"
                "esg_pct = (esg_total / total_portfolio) * 100\n"
                "print(f'Total Portfolio AUM: ${total_portfolio:,.0f}')\n"
                "print(f'ESG Qualified Assets: ${esg_total:,.0f} ({esg_pct:.1f}%)')\n"
                "if esg_pct >= 80.0:\n"
                "    print('COMPLIANT: Meets SEC 80% Names Rule for ESG-branded funds.')\n"
                "else:\n"
                "    print('VIOLATION: Fails 80% threshold! Marketing as an ESG fund constitutes greenwashing.')\n"
            ),
            "content": (
                "## Understand the idea\n\n"
                "As investor interest in environmental, social, and governance (ESG) factors has surged, so too has the deceptive marketing practice known as **greenwashing**: exaggerating, falsifying, or misleadingly marketing an investment product as sustainable when its actual holdings do not reflect those claims.\n\n"
                "Securities regulators have enacted rigorous disclosure and truth-in-advertising frameworks to combat greenwashing:\n\n"
                "1. **SEC Names Rule 2023 Amendments (Rule 35d-1)**: Requires that if a registered fund's name suggests a focus in a particular type of investment—including terms like 'ESG', 'Sustainable', 'Green', or 'Socially Responsible'—the fund must invest at least **80% of the value of its assets** in the investments suggested by its name.\n"
                "2. **EU Sustainable Finance Disclosure Regulation (SFDR)**: Establishes strict classification categories (Article 6 mainstream funds, Article 8 light green funds promoting environmental characteristics, and Article 9 dark green funds with explicit sustainable objectives), requiring verified, audited metric disclosures.\n"
                "3. **Taksonomi Keuangan Berkelanjutan Indonesia (TKBI)**: Indonesia's Financial Services Authority (OJK) sustainable taxonomy classifying economic activities into green, transitional, and non-aligned categories to ensure transparency in corporate disclosures and sustainable debt issuance.\n\n"
                "$$\n"
                r"\text{Sustainable Brand Name} \implies \text{Audited Metric Disclosures} \land \ge 80\% \text{ Qualifying Assets}"
                "\n$$\n\n"
                "## A worked example\n\n"
                "A mutual fund markets itself as the 'Sustainable Indonesian Equity Fund' with $100 million in AUM. An audit reveals that the manager allocated $35 million to solar, $25 million to wind, $15 million to water, but also $25 million to conventional oil and gas extraction.\n\n"
                "Qualified sustainable holdings total $75 million (75%). Because this falls below the mandatory 80% threshold under the SEC Names Rule, the fund cannot market itself under a sustainable brand name without violating anti-fraud and disclosure provisions. The fund must either divest the non-qualifying holdings or rename the fund.\n\n"
                "## Work through it yourself\n\n"
                "1. Audit any fund marketing claims against actual underlying portfolio holdings.\n"
                "2. Verify that non-financial disclosures cite audited primary sources rather than marketing puffery.\n"
                "3. Comply with the 80% allocation threshold when naming and promoting thematic strategies.\n\n"
                "### In the sandbox\n\n"
                "Run the script to verify portfolio asset allocations against the SEC 80% Names Rule threshold."
            ),
            "exercise": question(
                "Under the amended SEC Names Rule (Rule 35d-1), what minimum proportion of a fund's assets must be invested in accordance with its investment focus if its name includes 'ESG' or 'Sustainable'?",
                [
                    "At least 50% of the total market capitalization value across all equity asset classes",
                    "At least 80% of the value of its assets under normal investment market conditions",
                    "Exactly 100% of total portfolio value with zero allocation permitted to liquid cash reserves",
                ],
                1,
                "The SEC Names Rule mandates that at least 80% of fund assets must align with the investment characteristics suggested by its name.",
            ),
            "exercises": [
                question(
                    "Under the SEC Names Rule (Rule 35d-1), what is the minimum asset percentage required for ESG-named funds?",
                    [
                        "At least 50% of total portfolio value across all asset holdings",
                        "80% of the value of its assets under normal market circumstances",
                        "Exactly 100% of net equity holdings excluding cash and equivalents",
                    ],
                    1,
                    "Rule 35d-1 requires that at least 80% of assets match the thematic investment focus stated in the fund's name.",
                ),
                question(
                    "What constitutes 'greenwashing' under modern securities regulatory enforcement?",
                    [
                        "Planting indoor decorative foliage inside executive boardrooms and corporate headquarters office facilities",
                        "Misleadingly marketing an investment product as sustainable when holdings do not meet stated criteria",
                        "Allocating capital exclusively to municipal regulated water utility infrastructure development bonds",
                    ],
                    1,
                    "Greenwashing involves deceptive marketing where claims of environmental or social alignment are unsubstantiated by actual holdings.",
                ),
            ],
            "terms": [
                {"term": "Greenwashing", "definition": "The deceptive practice of making unsubstantiated or misleading claims regarding the environmental or social benefits of an investment product."},
                {"term": "SEC Names Rule (Rule 35d-1)", "definition": "Federal rule requiring funds with names suggesting a specific investment focus (including ESG) to invest at least 80% of their assets in that focus."},
                {"term": "Taksonomi Keuangan Berkelanjutan Indonesia (TKBI)", "definition": "Indonesia's official sustainable finance taxonomy published by OJK to classify green, transitional, and non-aligned economic activities."},
            ],
            "references": [
                {"title": "U.S. SEC · Final Rule: Amendments to the Investment Company Names Rule (2023)", "url": "https://www.sec.gov/news/press-release/2023-188"},
                {"title": "OJK · Taksonomi Keuangan Berkelanjutan Indonesia (TKBI)", "url": "https://ojk.go.id/keuanganberkelanjutan/id/publikasi/taksonomi-keuangan-berkelanjutan-indonesia"},
                {"title": "EUR-Lex · Sustainable Finance Disclosure Regulation (SFDR) Regulation (EU) 2019/2088", "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32019R2088"},
            ],
        },
    ]


def get_part4_exam_questions():
    """Return exam questions q9 to q17 with distractors rewritten to remove length bias."""
    return [
        {
            "id": "conduct-final-q9",
            "lessonId": "26.9",
            "question": "When an institutional broker assesses Best Execution under FINRA Rule 5310(a)(1), which factors must be evaluated?",
            "options": [
                "Market character, order size and type, quote accessibility, and number of markets checked",
                "Personal connections and social relationships between trading floor executives and exchange directors",
                "The visual design and user interface layout of the broker's proprietary execution order terminal",
            ],
            "answer": 0,
            "explanation": "FINRA Rule 5310(a)(1) requires examining market character, quote accessibility, order size and type, and multiple competing venues.",
        },
        {
            "id": "conduct-final-q10",
            "lessonId": "26.10",
            "question": "In quantitative factor research, why does unadjusted multiple testing (p-hacking) constitute an integrity failure?",
            "options": [
                "It causes computer memory limits to be exceeded during automated portfolio optimization runs across clusters",
                "It presents random statistical artifacts as true signals by concealing dozens of failed tests",
                "It requires researchers to purchase expensive proprietary software licenses for backtesting algorithms",
            ],
            "answer": 1,
            "explanation": "P-hacking exploits multiple hypothesis testing to report false positive noise as genuine predictive discoveries while hiding failed trials.",
        },
        {
            "id": "conduct-final-q11",
            "lessonId": "26.11",
            "question": "Why must historical backtests strictly use point-in-time fundamental data rather than restated financial statements?",
            "options": [
                "Point-in-time data files are smaller and significantly faster to download from distributed remote web servers",
                "Restated filings introduce information that was unknown to market participants on historical dates",
                "Securities regulators mandate that historical corporate filings must be deleted after five calendar years",
            ],
            "answer": 1,
            "explanation": "Restated numbers create hindsight look-ahead bias; point-in-time archives preserve what was known on each exact historical date.",
        },
        {
            "id": "conduct-final-q12",
            "lessonId": "26.12",
            "question": "Under suitability standards (FINRA Rule 2111 / Reg BI), why does objective risk capacity govern client allocations?",
            "options": [
                "Advisors are required by federal statutory law to assume all retail investors possess zero risk tolerance",
                "Contractual cash liabilities can force asset liquidation during drawdowns regardless of emotional courage",
                "Emotional questionnaires are legally invalid unless notarized by a licensed certified public accountant",
            ],
            "answer": 1,
            "explanation": "Objective balance sheet runway determines whether an investor can withstand drawdowns without forced liquidation, regardless of subjective feelings.",
        },
        {
            "id": "conduct-final-q13",
            "lessonId": "26.13",
            "question": "What is a primary warning sign indicating a fraudulent Ponzi scheme or unauthorized investment syndicate?",
            "options": [
                "Guaranteed high returns with zero reported down months, combined with opaque custody and no license",
                "Transparent disclosure of negative monthly returns and market volatility during economic contractions across sectors",
                "Using an independent, licensed commercial custodian bank to safeguard all investor capital and transaction records",
            ],
            "answer": 0,
            "explanation": "Guaranteed yields, zero volatility, and lack of independent licensed custody are universal hallmarks of fraudulent Ponzi structures.",
        },
        {
            "id": "conduct-final-q14",
            "lessonId": "26.14",
            "question": "Under Digital Realty Trust v. Somers (2018), when do Dodd-Frank Section 21F anti-retaliation protections apply?",
            "options": [
                "Only when the whistleblower provides original information regarding violations directly to the SEC",
                "Whenever an employee expresses informal verbal concerns to their immediate human resources department manager",
                "Automatically upon the employee signing an initial confidentiality agreement with the broker-dealer company",
            ],
            "answer": 0,
            "explanation": "The Supreme Court ruled that Section 21F anti-retaliation protections strictly require reporting directly to the Securities and Exchange Commission.",
        },
        {
            "id": "conduct-final-q15",
            "lessonId": "26.15",
            "question": "Under algorithmic cybersecurity hygiene and least privilege principles, what permission should a trading API key have?",
            "options": [
                "Full unrestricted permissions including external withdrawals so the algorithm can autonomously manage capital reserves",
                "Order placement and market data access only, with withdrawal permissions strictly disabled and IP whitelisted",
                "Root administrative server credentials shared across the entire engineering and quantitative software development staff",
            ],
            "answer": 1,
            "explanation": "Trading API keys must follow least privilege: order entry only, with withdrawals permanently disabled and execution restricted to whitelisted IPs.",
        },
        {
            "id": "conduct-final-q16",
            "lessonId": "26.16",
            "question": "In institutional algorithmic trading systems, what is the core function of a Maker-Checker deployment control?",
            "options": [
                "Ensuring that two distinct developers receive financial bonuses for writing the execution algorithm in production",
                "Preventing unilateral rogue actions by requiring an independent risk principal to verify and authorize code",
                "Doubling the order processing throughput speed of the automated execution gateway during volatile trading hours",
            ],
            "answer": 1,
            "explanation": "Maker-checker controls enforce independent four-eyes oversight, ensuring no individual can unilaterally deploy unverified code to live markets.",
        },
        {
            "id": "conduct-final-q17",
            "lessonId": "26.17",
            "question": "Under the amended SEC Names Rule (Rule 35d-1), what requirement applies to a fund with 'ESG' or 'Sustainable' in its name?",
            "options": [
                "It must invest at least 80% of its asset value in holdings aligned with the stated investment focus",
                "It must donate at least fifteen percent of annual management fee revenue to international environmental charities",
                "It is prohibited from holding cash or short-term treasury bills under any economic or volatile market circumstances",
            ],
            "answer": 0,
            "explanation": "The SEC Names Rule mandates that funds with thematic names like ESG must invest at least 80% of assets in qualifying investments.",
        },
    ]
