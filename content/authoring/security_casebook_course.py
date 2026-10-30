"""Real-world security-analysis casebook course (22.x)."""

from advanced_security_common import finish, make_add, q

READING = (
    "Advanced security analysis · real-world casebook. Read the cited primary source beside each "
    "lesson before relying on the lesson's summary. The figures in the worked examples are teaching "
    "figures unless the text explicitly cites a source figure. Enforcement allegations are attributed "
    "to the source; a settlement is not an admission unless the source says so."
)


def build_security_casebook():
    modules = []
    add = make_add(modules, READING)

    add(
        "22.1",
        "I",
        "Enron: special entities, mark-to-market, and disclosure",
        "Reconstruct how affiliated structures and fair-value estimates can remove risk from a reported balance sheet.",
        r"""
## The analytical question

The Enron case is a study in the gap between legal structure and economic substance. The company used special-purpose entities and fair-value accounting to report gains and move obligations off its balance sheet. The SEC's later enforcement materials and the bankruptcy record describe a pattern in which reported results depended on assumptions and structures that outside investors could not easily verify.

The analyst's method is not to assume every SPE is abusive. It is to ask three questions:

1. Who controls the entity, and who bears its losses?
2. Is the reported gain supported by an independent buyer at a fair price?
3. Does the parent retain a guarantee, liquidity support, or buy-back obligation?

$$\text{Adjusted parent equity}=\text{Reported equity}-\text{Unsupported gains}-\text{Guarantees and retained risk}$$

## A worked example

A parent reports equity of $100M, including a $40M gain on a sale of assets to an affiliated entity. The parent guarantees $30M of the entity's debt and has agreed to repurchase the assets if the entity cannot refinance.

On an economic view, the $40M gain is not a completed, arm's-length profit. Removing it leaves $60M. The $30M guarantee is a retained risk; if the entity fails, the parent's cash is at stake. An adjusted equity measure that deducts the guarantee is $30M, before any further write-down of the assets.

The analyst should read the entity's own financial statements, the guarantee terms, and the repurchase trigger. The key question is not whether the structure is legally off-balance-sheet, but whether the parent has retained the economics. A structure that transfers legal ownership while retaining downside risk is economically on-balance-sheet.

## Research discipline

1. **Map the entities and the control relationships**, including management and related-party interests.
2. **Test the gain against an independent valuation**, and remove gains that depend on the parent's support.
3. **Read every guarantee and liquidity commitment**, including oral side agreements disclosed in litigation.
4. **Stress the parent's cash** if the entities cannot refinance.
""",
        r"\text{Adjusted equity}=\text{Reported equity}-\text{Unsupported gains}-\text{Guarantees and retained risk}",
        'reported_equity = 100\nspe_gain = 40\nguarantee = 30\nprint("Equity after removing gain:", reported_equity - spe_gain)\nprint("Adjusted equity after guarantee:", reported_equity - spe_gain - guarantee)\nprint("Guarantee as % of reported equity:", round(guarantee/reported_equity*100, 1))',
        "A parent reports equity of $250M, including a $60M gain from an asset sale to an affiliated entity. It guarantees $45M of the entity's debt and has a $20M liquidity backstop. Reconstruct adjusted equity and explain why the reported gain should not be treated as a completed profit.",
        "Equity after removing the gain is $190M. Adjusted equity after the guarantee and backstop is $125M. The gain should not be treated as completed because the parent retains downside risk through the guarantee and backstop; if the entity cannot pay, the parent's cash is still exposed. The analyst should also check whether the sale price was supported by an independent buyer.",
        [
            q(
                "A sale to a controlled entity at a gain should be tested for:",
                [
                    "Arm's-length pricing and retained risk",
                    "The entity's name",
                    "The size of the gain only",
                ],
                0,
                "Economic substance depends on independent pricing and who bears the downside.",
            ),
            q(
                "A guarantee is best treated as:",
                ["A completed profit", "A contingent claim to stress", "An asset"],
                1,
                "A guarantee can become a real obligation if the guaranteed party fails.",
            ),
            q(
                "Reported equity is 180, including a 30 gain from an affiliate sale, and a 20 guarantee. Adjusted equity is:",
                ["130", "150", "180"],
                0,
                "Adjusted equity is 180 − 30 − 20 = 130.",
            ),
        ],
    )

    add(
        "22.2",
        "I",
        "CSC and WorldCom: capitalization and the cost of deception",
        "Measure how capitalizing operating costs raises current profit, accumulates assets, and eventually forces a restatement.",
        r"""
## The analytical question

Capitalizing a cost that should be expensed shifts it from the income statement to the balance sheet. Current profit rises, assets rise, and the eventual amortization or write-down is deferred. If the capitalized cost does not create a durable asset, the balance sheet becomes a reservoir of future losses.

The SEC's 2015 action against Computer Sciences Corporation (CSC) concerned accounting fraud and a $190M penalty; the SEC's release describes improper accounting that affected reported results. WorldCom's earlier collapse involved the capitalization of line costs, among other issues. These cases illustrate the same analytical question: did the capitalized spending create an asset, or did it merely defer an operating cost?

$$\text{Adjusted EBIT}=\text{Reported EBIT}-\text{Capitalized operating costs}+\text{Amortization of the capitalized layer}$$

## A worked example

A company reports EBIT of $150M and capitalizes $100M of operating costs that should have been expensed. It amortizes the new layer over five years, so current amortization is $20M. Adjusted EBIT is $150 − $100 + $20 = $70M.

If the capitalized layer accumulates for three years, the unamortized balance is $300M minus the amortization already taken. The reported equity and assets are overstated by the unamortized amount. When the company eventually corrects the accounting, the write-down reduces equity and may trigger covenant or liquidity problems.

The analyst should compare capital spending with depreciation and with the asset base it is supposed to support. A company that capitalizes costs while its asset base is not growing, or while its cash flow is weak, deserves scrutiny. The cash-flow statement is the cross-check: capitalization does not create cash, so operating cash flow will not improve by the amount of the capitalized cost.

## Research discipline

1. **Read the capitalization policy and the asset roll-forward**, including additions and amortization.
2. **Compare capex with depreciation and with revenue growth** over several years.
3. **Trace the cash**: a capitalized cost is still a cash outflow.
4. **Test the restatement scenario** and its effect on equity, covenants, and liquidity.
""",
        r"\text{Adj. EBIT}=\text{EBIT}-\text{Capitalized operating costs}+\text{Amortization};\quad \text{Overstated assets}=\text{Unamortized layer}",
        'reported_ebit = 150\ncapitalized = 100\namortization = 20\nprint("Adjusted EBIT:", reported_ebit - capitalized + amortization)\nprint("Profit boost from capitalization:", capitalized - amortization)\nprint("Unamortized layer after one year:", capitalized - amortization)',
        "A company reports EBIT of $240M and capitalizes $120M of operating costs, amortizing them over six years. Calculate adjusted EBIT and the current profit boost. Then explain what happens to reported equity if the accounting is later corrected.",
        "Adjusted EBIT is 240 − 120 + 20 = $140M. The current profit boost is 120 − 20 = $100M. If the accounting is corrected, the unamortized balance is written off against equity; reported equity falls by the remaining capitalized amount, and prior-period profits may be restated. The correction can also breach covenants or reduce liquidity if the company must repay debt or raise capital.",
        [
            q(
                "Capitalizing an operating cost generally:",
                ["Raises current profit and assets", "Reduces current profit and assets", "Has no effect on the balance sheet"],
                0,
                "The cost moves to the balance sheet and is amortized later.",
            ),
            q(
                "The cash-flow statement shows that capitalization:",
                ["Creates cash", "Does not create cash; the spending is still an outflow", "Eliminates the cost"],
                1,
                "Capitalization changes presentation and timing, not the cash spent.",
            ),
            q(
                "Reported EBIT is 180, capitalized costs are 60, and new amortization is 12. Adjusted EBIT is:",
                ["108", "132", "180"],
                1,
                "Adjusted EBIT is 180 − 60 + 12 = 132.",
            ),
        ],
    )

    add(
        "22.3",
        "I",
        "Luckin Coffee: revenue, related parties, and cash",
        "Test reported revenue against cash collection, related-party sales, and third-party evidence.",
        r"""
## The analytical question

The SEC's 2020 action against Luckin Coffee concerned fabricated transactions and materially inflated reported revenue and costs. Luckin agreed to pay a $180M penalty to settle the charges, without admitting or denying the allegations, according to the SEC's release. The case is a reminder that revenue growth is not evidence of a business until it is tied to cash and to independent customers.

The analyst's method is to reconcile revenue to cash and to separate related-party sales from third-party sales:

$$\text{Cash conversion}=\frac{\text{Cash collected from customers}}{\text{Revenue}}$$

$$\text{Third-party revenue}=\text{Reported revenue}-\text{Related-party revenue}$$

A company can report rapid growth by selling to affiliated entities, by recognizing revenue on transactions that lack economic substance, or by recording sales that never occurred. The analyst should read the related-party note, the customer-concentration disclosure, and the cash-flow statement.

## A worked example

A company reports revenue of $500M, of which $150M is to related parties. Cash collected from customers is $300M. Third-party revenue is $350M. Cash conversion against total revenue is 60%; against third-party revenue it is 85.7%.

The analyst should ask why related-party revenue is so large, whether the related parties have the ability to pay, and whether the sales are at arm's length. If the related-party revenue is not supported by cash or independent evidence, it should be excluded from the sustainable revenue base. A valuation that capitalizes the reported revenue would overstate the business.

The case also shows the value of independent evidence: short-seller reports, employee interviews, and third-party data can reveal transactions that the financial statements present as ordinary. The analyst should treat such evidence as investigative leads, not conclusions, and verify each claim against primary documents.

## Research discipline

1. **Reconcile revenue to cash collected** and investigate any persistent gap.
2. **Separate related-party revenue** and read the terms and payment history.
3. **Check customer concentration and new-customer growth** for unusual patterns.
4. **Use independent evidence carefully**, and verify allegations against filings and court records.
""",
        r"\text{Cash conversion}=\frac{\text{Cash collected}}{\text{Revenue}};\quad \text{Third-party revenue}=\text{Revenue}-\text{Related-party revenue}",
        'revenue = 500\nrelated_party = 150\ncash_collected = 300\nthird_party = revenue - related_party\nprint("Third-party revenue:", third_party)\nprint("Cash conversion on total (%):", round(cash_collected/revenue*100, 1))\nprint("Cash conversion on third-party (%):", round(cash_collected/third_party*100, 1))',
        "A company reports revenue of $800M, including $240M from related parties. Cash collected from customers is $520M. Calculate third-party revenue and cash conversion on both bases. Then explain why the related-party revenue should be examined separately.",
        "Third-party revenue is 800 − 240 = $560M. Cash conversion is 520/800 = 65.0% on total revenue and 520/560 = 92.9% on third-party revenue. The related-party revenue should be examined separately because it may not be at arm's length, may not be collectible, and may not represent independent demand. If it is excluded, the sustainable revenue base is lower and the valuation should reflect that.",
        [
            q(
                "Revenue is 400 and cash collected is 260. Cash conversion is:",
                ["55%", "65%", "75%"],
                1,
                "Cash conversion is 260 / 400 = 65%.",
            ),
            q(
                "Related-party revenue should be examined because:",
                ["It is always fraudulent", "It may not be at arm's length or collectible", "It is always cash-based"],
                1,
                "Related-party sales can lack independent economic substance; the terms and cash collection matter.",
            ),
            q(
                "Revenue is 600 and related-party revenue is 150. Third-party revenue is:",
                ["150", "450", "600"],
                1,
                "Third-party revenue is 600 − 150 = 450.",
            ),
        ],
    )

    add(
        "22.4",
        "I",
        "Theranos: private valuations and the evidence gap",
        "Value a private company from verifiable evidence rather than from its last financing round or promotional claims.",
        r"""
## The analytical question

The SEC's 2018 action against Theranos, Elizabeth Holmes, and Ramesh Balwani concerned misleading claims about the company's technology and financial prospects. Theranos and Holmes settled with the SEC, without admitting or denying the allegations, according to the release. The case is a study in how a private valuation can outrun the evidence.

A private company's last financing round is not an independent valuation. It reflects the price one investor paid at one time, often with preferences and protections that ordinary shares do not have. The analyst should build a value from evidence:

$$\text{Evidence-based value}=\text{Verifiable revenue or asset base}\times\text{Defensible multiple}$$

and compare it with the headline valuation. If the gap is large, the analyst should ask what evidence would justify the difference.

## A worked example

A private company was last valued at $9B. Its disclosed revenue is $40M, but the revenue is not audited and a large share comes from a related party. The analyst builds three cases:

| Case | Sustainable revenue | Multiple | Value |
| :--- | ---: | ---: | ---: |
| Bear | $10M | 5× | $50M |
| Base | $30M | 8× | $240M |
| Bull | $60M | 10× | $600M |

Even the bull case is far below the headline valuation. The gap is a claim about future technology and market position that the current evidence does not support. The analyst should request audited financials, customer contracts, independent validation of the technology, and the terms of the last financing round.

The lesson is not that every high private valuation is wrong. It is that the valuation must be connected to evidence, and the burden of proof rises with the size of the gap. A private company can be worth a high multiple if it has verifiable revenue, retention, and a defensible technology; without those, the headline price is a narrative.

## Research discipline

1. **Use audited financials and independent technical validation** where available.
2. **Read the financing terms**: preferences, liquidation stacks, and investor rights.
3. **Build a range from evidence**, and state what would justify the headline valuation.
4. **Treat promotional claims as hypotheses**, not as inputs to the valuation.
""",
        r"\text{Evidence value}=\text{Sustainable revenue}\times\text{Defensible multiple};\quad \text{Gap}=\text{Headline value}-\text{Evidence value}",
        'headline = 9000\nbear_revenue = 10\nbear_multiple = 5\nbase_revenue = 30\nbase_multiple = 8\nbull_revenue = 60\nbull_multiple = 10\nprint("Bear value:", bear_revenue*bear_multiple)\nprint("Base value:", base_revenue*base_multiple)\nprint("Bull value:", bull_revenue*bull_multiple)\nprint("Gap to bull case:", headline - bull_revenue*bull_multiple)',
        "A private company is valued at $2B. Sustainable revenue is estimated at $50M in the bear case, $100M in the base case, and $160M in the bull case, with multiples of 4×, 6×, and 8×. Calculate the three values and the gap to the headline valuation. What evidence would you request?",
        "Bear value is 50 × 4 = $200M; base is 100 × 6 = $600M; bull is 160 × 8 = $1,280M. The gap to the headline $2B is $720M even in the bull case. Request audited financials, customer contracts, retention data, independent technical validation, and the terms of the last financing round. The analyst should also check whether the headline valuation includes preferences that ordinary shares do not receive.",
        [
            q(
                "A private company's last financing round is:",
                ["An independent market valuation of all shares", "A price paid by one investor with specific terms", "Audited financial evidence"],
                1,
                "Financing terms, preferences, and timing mean the round price is not a general valuation.",
            ),
            q(
                "An evidence-based valuation should be built from:",
                ["Promotional claims", "Verifiable revenue and defensible multiples", "The founder's forecast"],
                1,
                "The valuation should rest on evidence that an independent analyst can inspect.",
            ),
            q(
                "Sustainable revenue is 80 and the multiple is 5×. Evidence value is:",
                ["40", "400", "800"],
                1,
                "Evidence value is 80 × 5 = 400.",
            ),
        ],
    )

    add(
        "22.5",
        "II",
        "Nikola: partnerships, backlog, and disclosure",
        "Test whether partnerships and order backlog are supported by binding contracts and independent confirmation.",
        r"""
## The analytical question

The SEC's 2021 action against Nikola and its founder concerned misleading statements about the company's technology, partnerships, and business prospects. Nikola later agreed to pay $125M to settle the SEC's charges, without admitting or denying the findings, according to the release. The case illustrates how a company's narrative can outpace its contracts.

The analyst should separate three categories of evidence:

1. **Binding contracts** with enforceable volumes and prices.
2. **Non-binding memoranda or partnerships** that may not create revenue.
3. **Promotional claims** that cannot be tested.

$$\text{Evidence-backed backlog}=\sum \text{Binding contract value}\times\text{Probability of realization}$$

A headline backlog that includes non-binding agreements can overstate future revenue. The analyst should read the contract terms, the counterparty's disclosures, and the company's own risk factors.

## A worked example

A company reports a $10B backlog. The analyst finds that $6B is non-binding memoranda, $3B is a binding contract with a customer that has not yet obtained financing, and $1B is a firm order. Applying probabilities of 0% to the memoranda, 50% to the financed-contingent contract, and 90% to the firm order gives an evidence-backed backlog of 0 + $1.5B + $0.9B = $2.4B.

The gap between $10B and $2.4B is the narrative premium. The analyst should ask what the company's valuation implies about the backlog and whether the contracts support it. A high multiple on a large backlog can be justified if the contracts are binding and the customers can pay; it is not justified by announcements alone.

The case also shows the importance of independent confirmation. If a partnership is material, the counterparty may disclose it in its own filings. If the counterparty does not confirm it, the analyst should treat the claim with caution.

## Research discipline

1. **Read the contract terms**, not only the press release: volume, price, duration, and conditions.
2. **Check the counterparty's disclosures** for confirmation.
3. **Apply realization probabilities** to each category of backlog.
4. **Compare the evidence-backed backlog with the valuation** and the company's revenue history.
""",
        r"\text{Evidence backlog}=\sum \text{Binding value}_i\times p_i;\quad \text{Narrative premium}=\text{Reported backlog}-\text{Evidence backlog}",
        'memoranda = 6000\nmemoranda_probability = 0.0\nconditional = 3000\nconditional_probability = 0.5\nfirm = 1000\nfirm_probability = 0.9\nevidence = memoranda*memoranda_probability + conditional*conditional_probability + firm*firm_probability\nprint("Evidence-backed backlog:", evidence)\nprint("Narrative premium:", 10000 - evidence)',
        "A company reports a $6B backlog: $3B of non-binding memoranda, $2B of a contract contingent on customer financing, and $1B of firm orders. Apply probabilities of 0%, 40%, and 90%. Calculate the evidence-backed backlog and the narrative premium.",
        "Evidence-backed backlog is 0 + 0.40(2,000) + 0.90(1,000) = $1.7B. The narrative premium is $6B − $1.7B = $4.3B. The analyst should read the contract terms, check whether the customer has financing, and compare the evidence-backed backlog with the company's revenue and valuation.",
        [
            q(
                "A non-binding memorandum of understanding is best treated as:",
                ["Certain revenue", "A low-probability or zero-probability backlog item", "A cash equivalent"],
                1,
                "Without enforceable obligations, the memorandum may never produce revenue.",
            ),
            q(
                "Evidence-backed backlog applies:",
                ["A realization probability to each contract category", "The same probability to every item", "No probability at all"],
                0,
                "Different contract types have different probabilities of producing revenue.",
            ),
            q(
                "A $4B backlog item has a 25% probability. Its expected value is:",
                ["100", "1000", "4000"],
                1,
                "0.25 × 4,000 = 1,000.",
            ),
        ],
    )

    add(
        "22.6",
        "II",
        "FTX: related-party balance sheets and customer funds",
        "Trace customer assets, related-party receivables, and governance failures in a complex financial platform.",
        r"""
## The analytical question

The SEC's 2022 action against Samuel Bankman-Fried concerned the alleged diversion of customer funds and misleading statements about FTX's financial condition. The case is a study in related-party exposure and the difference between a platform's stated safeguards and its actual control of customer assets.

The analyst should reconstruct the balance sheet from the customer's perspective:

$$\text{Customer asset coverage}=\frac{\text{Liquid assets available to customers}}{\text{Customer claims}}$$

If the numerator includes receivables from related parties or illiquid tokens, the coverage ratio is not a cash coverage ratio. The analyst should separate:

1. **Segregated customer assets** held in custody.
2. **Related-party receivables** that may not be collectible.
3. **Illiquid or affiliated tokens** whose value depends on the platform itself.

## A worked example

A platform reports $100B of customer deposits, $20B of liquid assets, $40B of receivables from affiliated entities, and $40B of affiliated tokens. Headline coverage appears to be $100B of assets against $100B of liabilities. But liquid coverage is only 20/100 = 20%.

If the affiliated receivables are not collectible and the affiliated tokens are worth zero in a stress, the shortfall is $80B. The analyst should value the assets at their realizable value, not their stated value, and check whether customer assets are legally segregated.

The governance question is equally important. Who controls the entities on both sides of the related-party transactions? Are the receivables disclosed? Is there an independent board or auditor? A platform that controls the customer's assets and the affiliated entities that owe it money has a conflict that requires strong controls.

## Research discipline

1. **Separate liquid, related-party, and affiliated-token assets** and value each at realizable value.
2. **Read the custody and segregation disclosures**, and compare them with the actual legal structure.
3. **Map related-party ownership and control**; identify who benefits from the receivables.
4. **Stress the affiliated assets to zero** and show the customer shortfall.
""",
        r"\text{Coverage}=\frac{\text{Liquid assets}}{\text{Customer claims}};\quad \text{Shortfall}=\text{Claims}-\text{Realizable assets}",
        'claims = 100\nliquid = 20\nrelated_receivable = 40\naffiliated_tokens = 40\nprint("Headline coverage:", (liquid + related_receivable + affiliated_tokens)/claims)\nprint("Liquid coverage:", liquid/claims)\nprint("Stress shortfall:", claims - liquid)',
        "A platform reports $80B of customer claims, $15B of liquid assets, $30B of related-party receivables, and $35B of affiliated tokens. Calculate headline coverage, liquid coverage, and the shortfall if the related-party assets are worth zero in a stress.",
        "Headline coverage is (15 + 30 + 35)/80 = 100%. Liquid coverage is 15/80 = 18.75%. If the related-party receivables and affiliated tokens are worth zero, the shortfall is 80 − 15 = $65B. The analyst should check segregation, custody, and related-party control before treating the headline coverage as meaningful.",
        [
            q(
                "Customer asset coverage should use:",
                ["All stated assets, including related-party receivables", "Liquid, realizable assets", "The platform's own token at its peak price"],
                1,
                "Only assets that can actually be realized for customers count in a stress.",
            ),
            q(
                "A related-party receivable is risky because:",
                ["The counterparty may be controlled by the same people and may not pay", "It is always cash", "It is always disclosed"],
                0,
                "Control and collectibility are central; related-party receivables can disappear in a stress.",
            ),
            q(
                "Liquid assets are 24 and customer claims are 120. Liquid coverage is:",
                ["10%", "20%", "24%"],
                1,
                "Liquid coverage is 24 / 120 = 20%.",
            ),
        ],
    )

    add(
        "22.7",
        "II",
        "SVB and Lehman: solvency, liquidity, and the clock",
        "Compare a solvency problem with a liquidity problem and identify which ratios reveal each.",
        r"""
## The analytical question

Silicon Valley Bank failed in March 2023 after a run by concentrated, largely uninsured depositors. The Federal Reserve's review identified concentrated funding, interest-rate exposure, and weak liquidity-risk management. Lehman Brothers' 2008 bankruptcy is a different case, but both illustrate how a balance sheet can look solvent on one measure and fail on another.

The analyst should distinguish:

- **Solvency**: assets are worth less than liabilities on a realistic valuation.
- **Liquidity**: the institution cannot meet cash outflows as they come due, even if assets are adequate over time.

$$\text{Tangible equity ratio}=\frac{\text{Tangible equity}}{\text{Tangible assets}}$$

$$\text{Liquidity coverage}=\frac{\text{Liquid assets}}{\text{Short-term outflows}}$$

A bank with a high reported capital ratio can still fail if its assets are long-duration and its depositors are concentrated. A bank with liquid assets can survive a run even if its capital is thin, provided the run is short. The interaction of the two is what matters.

## A worked example

A bank has $100B of securities classified as held-to-maturity, a duration of 5 years, and a yield of 2%. Market yields rise to 5%. Using a duration approximation, the price change is approximately −5 × 3% = −15%, or a $15B unrealized loss. If tangible equity is $10B, the loss exceeds equity on a mark-to-market basis.

The bank also has 90% uninsured deposits. If 30% of those depositors withdraw, the outflow is 0.30 × 0.90 × deposits. The bank may be forced to sell securities at a loss to meet withdrawals, converting an unrealized loss into a realized one. The capital ratio and the liquidity ratio interact: the run forces the sale, and the sale destroys capital.

The analyst should stress both the asset side and the funding side together. A static capital ratio is not enough; the path of outflows and asset sales determines whether the bank survives.

## Research discipline

1. **Mark available-for-sale and held-to-maturity securities to market** in a stress.
2. **Measure uninsured and concentrated deposits**, and model a run.
3. **Stress asset sales and capital together**, not separately.
4. **Read the supervisory findings** for the specific weaknesses in each case.
""",
        r"\Delta P/P\approx-D\times\Delta y;\quad \text{Liquidity coverage}=\frac{\text{Liquid assets}}{\text{Short-term outflows}}",
        'duration = 5\nyield_change = 0.03\nsecurities = 100\nequity = 10\nloss = duration*yield_change*securities\nprint("Approximate loss:", loss)\nprint("Loss vs equity:", loss/equity)\nuninsured = 0.90\nwithdrawal = 0.30\nprint("Withdrawal share of deposits:", uninsured*withdrawal)',
        "A bank has $150B of long-duration securities, a duration of 4 years, and a 2.5% rise in market yields. Tangible equity is $12B. Estimate the mark-to-market loss using the duration approximation and compare it with equity. Then explain why a run by uninsured depositors can make the loss real.",
        "The approximate loss is 4 × 2.5% × $150B = $15B, which exceeds $12B of tangible equity. A run by uninsured depositors forces the bank to sell securities to meet withdrawals; selling at a loss converts an unrealized loss into a realized one, reducing capital. The bank may then face a capital shortfall and further withdrawals, creating a spiral.",
        [
            q(
                "A duration of 5 and a 2% yield rise imply an approximate price change of:",
                ["−10%", "+10%", "−2%"],
                0,
                "The approximate price change is −5 × 2% = −10%.",
            ),
            q(
                "Liquidity risk is most acute when:",
                ["Deposits are diversified and insured", "Funding is concentrated and uninsured", "Assets are short-duration cash"],
                1,
                "Concentrated, uninsured funding can withdraw quickly.",
            ),
            q(
                "A bank sells securities at a loss to meet withdrawals. This:",
                ["Increases capital", "Converts an unrealized loss into a realized loss", "Has no effect on capital"],
                1,
                "The sale realizes the loss and reduces equity.",
            ),
        ],
    )

    add(
        "22.8",
        "II",
        "GE: disclosure, insurance reserves, and segment complexity",
        "Use segment and reserve analysis to test whether a complex company's reported results reflect recurring economics.",
        r"""
## The analytical question

General Electric's 2020 SEC settlement concerned disclosures about its Power business and run-off insurance operations. GE's filing describes a $200M settlement and changes to disclosure and internal-control processes. The case is a study in complexity: when a company has many segments, legacy liabilities, and long-tail insurance reserves, the consolidated result can hide the economics of individual units.

The analyst should rebuild the group from its segments:

$$\text{Group value}=\sum_i \text{Segment value}_i-\text{Net debt}-\text{Legacy liabilities}$$

and test each segment's margin, capital intensity, and growth separately. A segment that looks small by revenue can be large by capital or risk. Insurance reserves are especially important because they are estimates of future claims; adverse development can reduce profit and equity years later.

## A worked example

A conglomerate reports group EBIT of $50M. Segment analysis shows industrial profit of $80M, power profit of $10M, and an insurance reserve increase of $40M. The insurance charge reduces group profit by 80%. If the analyst assumes the insurance charge is nonrecurring, the forward valuation may be too high; if the charge is the first of several, the group's equity is overstated.

The analyst should read the reserve roll-forward, the assumptions behind the reserves, and the segment disclosure. A reserve increase is not automatically a one-time event; it may signal that prior estimates were too low. The same logic applies to warranties, environmental liabilities, and long-term contracts.

The case also illustrates the value of disclosure quality. When a company changes its disclosure or internal controls, the analyst should ask what the change reveals about the reliability of prior numbers. A settlement is not proof that every prior number was wrong, but it is a reason to increase the evidence standard.

## Research discipline

1. **Rebuild the group from segments** and reconcile to consolidated profit.
2. **Read the reserve roll-forward** and distinguish favorable from adverse development.
3. **Test whether a charge is recurring** by comparing it with prior years.
4. **Treat disclosure changes and control weaknesses as evidence about reliability.**
""",
        r"\text{Group value}=\sum_i \text{Segment value}_i-\text{Net debt}-\text{Legacy liabilities}",
        'industrial = 80\npower = 10\ninsurance_charge = 40\ngroup_ebit = 50\nprint("Group EBIT:", group_ebit)\nprint("Insurance share of EBIT (%):", round(insurance_charge/group_ebit*100, 1))\nprint("EBIT excluding insurance charge:", industrial + power)',
        "A conglomerate reports group EBIT of $120M. Segment analysis shows industrial profit of $90M, power profit of $70M, and an insurance reserve increase of $40M. Reconcile the group result and calculate the insurance charge's share of group EBIT. Then explain why treating the charge as nonrecurring could overstate forward value.",
        "The segments sum to 90 + 70 = $160M before the insurance charge; subtracting $40M gives $120M. The charge is 40/120 = 33.3% of group EBIT. Treating it as nonrecurring assumes it will not recur; if the reserve increase reflects a systematic underestimation of claims, further charges may follow. The analyst should read the reserve roll-forward and compare the charge with prior-year development.",
        [
            q(
                "A conglomerate's group profit is best understood by:",
                ["Ignoring segments", "Reconciling segment profits to the group result", "Using only the share price"],
                1,
                "Segment analysis shows which units create or consume profit and capital.",
            ),
            q(
                "Adverse insurance reserve development means:",
                ["Prior reserves were too high", "Prior reserves were too low and are increased", "The insurer has no claims"],
                1,
                "Adverse development increases reserves for prior claims, reducing current profit.",
            ),
            q(
                "Segments earn 100 and 40, and a reserve charge is 30. Group EBIT is:",
                ["110", "140", "170"],
                0,
                "Group EBIT is 100 + 40 − 30 = 110.",
            ),
        ],
    )

    checkpoints = [
        (
            "Checkpoint · accounting failures and evidence",
            [
                (
                    "22.1",
                    q(
                        "A parent removes an unsupported $50M gain and adds a $20M guarantee. Reported equity is $200M. Adjusted equity is:",
                        ["130", "150", "200"],
                        0,
                        "Adjusted equity is 200 − 50 − 20 = 130.",
                    ),
                ),
                (
                    "22.2",
                    q(
                        "Capitalizing an operating cost instead of expensing it:",
                        ["Raises current profit", "Lowers current profit", "Reduces cash flow"],
                        0,
                        "The cost moves to the balance sheet, raising current profit.",
                    ),
                ),
                (
                    "22.3",
                    q(
                        "Revenue is 500 and cash collected is 300. Cash conversion is:",
                        ["40%", "60%", "80%"],
                        1,
                        "Cash conversion is 300 / 500 = 60%.",
                    ),
                ),
                (
                    "22.4",
                    q(
                        "How should an analyst treat a private company's last financing round?",
                        ["As an independent valuation of all shares", "As one investor's price with specific terms", "As audited evidence"],
                        1,
                        "The round price reflects one investor's terms and timing, not a general market value.",
                    ),
                ),
            ],
        ),
        (
            "Checkpoint · solvency, liquidity, and complexity",
            [
                (
                    "22.5",
                    q(
                        "A non-binding memorandum in a backlog should be:",
                        ["Counted at full value", "Assigned a low or zero realization probability", "Treated as cash"],
                        1,
                        "Without an enforceable obligation, the memorandum may never produce revenue.",
                    ),
                ),
                (
                    "22.6",
                    q(
                        "Liquid assets are 30 and customer claims are 150. Liquid coverage is:",
                        ["10%", "20%", "30%"],
                        1,
                        "Liquid coverage is 30 / 150 = 20%.",
                    ),
                ),
                (
                    "22.7",
                    q(
                        "A duration of 4 and a 3% yield rise imply an approximate price change of:",
                        ["−12%", "+12%", "−4%"],
                        0,
                        "The approximate price change is −4 × 3% = −12%.",
                    ),
                ),
                (
                    "22.8",
                    q(
                        "Adverse reserve development:",
                        ["Increases current profit", "Reduces current profit", "Has no effect on equity"],
                        1,
                        "The reserve increase is charged against current profit and reduces equity.",
                    ),
                ),
            ],
        ),
    ]

    return finish(
        {
            "id": "real-world-casebook",
            "number": 22,
            "title": "Real-world security analysis casebook",
            "description": "Work through documented accounting failures, private-company evidence gaps, platform governance, and solvency events using primary sources.",
            "source": "Advanced security analysis · documented cases from SEC, Federal Reserve, and other primary sources",
            "level": "Advanced",
            "icon": "book",
            "modules": modules,
            "prerequisites": "Security Analysis and at least one of forensic accounting, credit analysis, or bank analysis. The casebook assumes comfort with financial statements and valuation.",
            "outcomes": [
                "Reconstruct reported results for affiliated structures and capitalized costs.",
                "Test revenue, backlog, and private valuations against independent evidence.",
                "Separate solvency from liquidity in a financial institution.",
                "Write a case memo that distinguishes allegations, findings, and inferences.",
            ],
            "readingGuide": "Read the cited release or filing before the lesson. The case summaries are original teaching notes; they do not reproduce the sources, and they distinguish allegations from findings. Worked figures are illustrative unless a source figure is named.",
            "references": [
                {"title": "U.S. SEC · Enforcement actions and litigation releases", "url": "https://www.sec.gov/enforcement-litigation"},
                {"title": "Federal Reserve · SVB review: key takeaways", "url": "https://www.federalreserve.gov/publications/2023-April-SVB-Key-Takeaways.htm"},
            ],
            "parts": [
                {"id": "I", "title": "Accounting and evidence failures", "description": "Enron, CSC/WorldCom, Luckin, and Theranos"},
                {"id": "II", "title": "Contracts, platforms, and solvency", "description": "Nikola, FTX, SVB/Lehman, and GE"},
            ],
            "studyType": "applied",
        },
        checkpoints,
    )
