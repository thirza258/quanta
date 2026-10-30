"""Forensic accounting and earnings-quality course (15.x)."""

from advanced_security_common import finish, make_add, q

READING = (
    "Advanced security analysis · forensic accounting. Read the company's revenue-recognition, "
    "receivable, inventory, and related-party notes beside this lesson. The worked numbers are "
    "teaching figures; the cited enforcement action supplies the real-world context."
)


def build_forensic_accounting():
    modules = []
    add = make_add(modules, READING)

    add(
        "15.1",
        "I",
        "The accrual-to-cash bridge",
        "Reconcile profit to operating cash through receivables, inventory, and payables, and measure how the cash-conversion cycle is changing.",
        r"""
## The analytical question

A company can report growing profit while its operating cash flow falls. The bridge from net income to cash explains why: revenue may be booked before collection, inventory may be built ahead of demand, or payables may be stretched to fund the gap. The analyst's job is to locate the movement in a specific account rather than accept a vague assurance that "timing" explains it.

Three working-capital ratios organize the bridge:

$$\text{DSO}=\frac{\text{Accounts receivable}}{\text{Revenue}}\times365$$

$$\text{DIO}=\frac{\text{Inventory}}{\text{COGS}}\times365$$

$$\text{DPO}=\frac{\text{Accounts payable}}{\text{COGS}}\times365$$

$$\text{Cash conversion cycle}=\text{DSO}+\text{DIO}-\text{DPO}$$

A rising cycle consumes cash. A rising DSO can reflect generous credit to win customers, weak collection, or revenue recognized before the customer is billed. A rising DIO can reflect planned stocking, a demand slowdown, or obsolete goods carried at cost. A rising DPO improves the cycle but may signal supplier stress or an inability to pay.

## A worked example

A distributor reports current revenue of $500M and COGS of $300M. Receivables are $80M (prior $60M on revenue of $450M), inventory is $70M (prior $55M on COGS of $270M), and payables are $50M (prior $45M).

Current DSO is $80/500×365 = 58.4 days, versus $60/450×365 = 48.7 days. DIO is $70/300×365 = 85.2 days, versus $55/270×365 = 74.4 days. DPO is $50/300×365 = 60.8 days, essentially unchanged. The cash conversion cycle therefore lengthens from about 62.3 days to 82.7 days, a 20.4-day deterioration.

That is a concrete cash cost. Each extra day of the cycle ties up roughly $500M/365 = $1.37M of revenue-related working capital, before considering the inventory base. The analyst should trace whether the receivables are concentrated in one customer, whether inventory is finished goods or raw material, and whether payables are overdue. The bridge is not complete until the cash-flow statement reconciles to the income statement.

## Research discipline

1. **Use average balances** when the accounts moved sharply during the year, and disclose which revenue or COGS base you used.
2. **Read the receivables note**: aging, customer concentration, non-accrual accounts, and the allowance for credit losses.
3. **Separate growth-driven working capital from deterioration.** A growing firm may legitimately consume cash; the question is whether the incremental return justifies it.
4. **Reconcile the indirect cash-flow statement** line by line. A ratio is a summary; the statement is the evidence.
""",
        r"\text{DSO}=\frac{\text{AR}}{\text{Revenue}}365;\quad \text{DIO}=\frac{\text{Inventory}}{\text{COGS}}365;\quad \text{CCC}=\text{DSO}+\text{DIO}-\text{DPO}",
        'ar = 80\nrevenue = 500\nprior_ar = 60\nprior_revenue = 450\ninv = 70\ncogs = 300\nprior_inv = 55\nprior_cogs = 270\nap = 50\nprint("DSO current:", round(ar/revenue*365, 1))\nprint("DSO prior:", round(prior_ar/prior_revenue*365, 1))\nprint("DIO current:", round(inv/cogs*365, 1))\nprint("DIO prior:", round(prior_inv/prior_cogs*365, 1))\nprint("DPO current:", round(ap/cogs*365, 1))\nccc = ar/revenue*365 + inv/cogs*365 - ap/cogs*365\nprint("Cash conversion cycle:", round(ccc, 1))',
        "A company reports revenue of $600M, COGS of $360M, receivables of $90M, inventory of $72M, and payables of $54M. Calculate DSO, DIO, DPO, and the cash conversion cycle. Then state which account you would inspect first if the cycle lengthened sharply.",
        "DSO = 90/600×365 = 54.75 days. DIO = 72/360×365 = 73.0 days. DPO = 54/360×365 = 54.75 days. The cycle is 54.75 + 73.0 − 54.75 = 73.0 days. Inspect receivables first if revenue grew, because they connect reported sales to cash collection; inspect inventory first if sales slowed or the product mix changed.",
        [
            q(
                "Revenue is 400 and receivables are 80. DSO is approximately:",
                ["20 days", "73 days", "146 days"],
                1,
                "80 / 400 × 365 = 73 days.",
            ),
            q(
                "A rising cash conversion cycle generally:",
                ["Releases cash", "Consumes cash", "Has no cash effect"],
                1,
                "More days between paying suppliers and collecting customers ties up working capital.",
            ),
            q(
                "If revenue is 500, inventory 100, and COGS 250, DIO is:",
                ["73 days", "146 days", "36.5 days"],
                1,
                "100 / 250 × 365 = 146 days.",
            ),
        ],
    )

    add(
        "15.2",
        "I",
        "Revenue-recognition red flags",
        "Test reported revenue against cash collection, contract assets, and the timing of customer acceptance.",
        r"""
## The analytical question

Revenue is the largest single input to most valuations and the most common target of accounting manipulation. The analyst should test whether revenue is supported by an enforceable customer obligation, whether collection is probable, and whether the seller has completed its performance. Common warning signs include receivables growing faster than sales, unbilled contract assets rising, revenue recognized on bill-and-hold arrangements, and round-tripping through related parties.

A practical first test is the **receivables-to-revenue gap**:

$$\Delta\text{DSO}=\text{DSO}_t-\text{DSO}_{t-1}$$

A second is the growth of **contract assets** relative to revenue. Under percentage-of-completion accounting, a company may recognize revenue before it can bill the customer. That can be legitimate, but a persistent gap between revenue and billing deserves a read of the contract terms.

## A worked example

A software company reports revenue of $200M, up from $160M. Receivables are $50M, up from $30M, and unbilled contract assets are $20M, up from $5M.

DSO rises from $30/160×365 = 68.4 days to $50/200×365 = 91.2 days. Contract assets grow from 3.1% of revenue to 10.0%, a much faster rate than the 25% revenue increase. The analyst asks three questions. First, are the new contracts with creditworthy customers, or has the company extended terms to win growth? Second, has the company recognized revenue on milestones that the customer has not accepted? Third, are the contract assets concentrated in one project whose recoverability depends on future funding?

A legitimate explanation might be a large multi-year contract with milestone billing. A red flag would be a pattern of rising unbilled balances, slowing cash collection, and a customer base that is increasingly concentrated. The analyst should not conclude fraud from one ratio; the ratio identifies the note to read.

## Research discipline

1. **Read the revenue-recognition policy** and the contract-asset note. Compare the policy with the economics of the contracts.
2. **Test cutoff.** Look for large fourth-quarter revenue, returns after year-end, or side agreements that allow cancellation.
3. **Trace cash.** A sale that never collects is not evidence of value, even if it satisfies an accounting rule.
4. **Document alternative explanations** and the evidence that would distinguish them before forming a conclusion.
""",
        r"\Delta\text{DSO}=\text{DSO}_t-\text{DSO}_{t-1};\quad \text{Contract-asset intensity}=\frac{\text{Contract assets}}{\text{Revenue}}",
        'revenue = 200\nprior_revenue = 160\nar = 50\nprior_ar = 30\ncontract_assets = 20\nprior_contract_assets = 5\ndso_now = ar/revenue*365\ndso_prior = prior_ar/prior_revenue*365\nprint("DSO current:", round(dso_now, 1))\nprint("DSO prior:", round(dso_prior, 1))\nprint("Contract-asset intensity current (%):", round(contract_assets/revenue*100, 1))\nprint("Contract-asset intensity prior (%):", round(prior_contract_assets/prior_revenue*100, 1))',
        "A company's revenue rises from $300M to $390M, receivables rise from $45M to $78M, and contract assets rise from $9M to $39M. Calculate the change in DSO and contract-asset intensity. What additional disclosure would you request before accepting the revenue as high quality?",
        "DSO rises from 45/300×365 = 54.75 days to 78/390×365 = 73.0 days. Contract-asset intensity rises from 3.0% to 10.0%. Request the contract-asset aging, the identity and credit quality of the largest customers, the billing milestones, and evidence of customer acceptance. Also check whether cash collected from customers grew at a similar rate to revenue.",
        [
            q(
                "Revenue is 100 and receivables rise from 10 to 25 while revenue is unchanged. This most directly suggests:",
                ["Faster collection", "Slower collection or earlier revenue recognition", "Lower inventory"],
                1,
                "Receivables growing without revenue growth lengthens DSO and may indicate collection or recognition problems.",
            ),
            q(
                "Unbilled contract assets are best understood by reading:",
                ["The share-price chart", "The contract terms and customer acceptance conditions", "The dividend history"],
                1,
                "Revenue recognized before billing depends on the enforceable contract and completion conditions.",
            ),
            q(
                "A company reports revenue of 500 and contract assets of 50. Contract-asset intensity is:",
                ["5%", "10%", "50%"],
                1,
                "Contract assets of 50 divided by revenue of 500 give 10% intensity.",
            ),
        ],
    )

    add(
        "15.3",
        "I",
        "Expense capitalization and cost deferral",
        "Identify costs moved from the income statement to the balance sheet and measure the effect on profit, returns, and future amortization.",
        r"""
## The analytical question

Capitalizing a cost spreads it over future periods; expensing it reduces current profit immediately. Accounting rules permit capitalization when a cost creates a future economic benefit, but the boundary is judgmental. Software development, customer acquisition, maintenance, and restructuring costs are common areas where a company can improve current profit by capitalizing more aggressively.

The analyst should reconstruct an **expensed-basis** profit:

$$\text{Adjusted EBIT}=\text{Reported EBIT}-\text{Capitalized costs}+\text{Amortization of those costs}$$

The adjustment matters for three reasons. It lowers current profit, it changes invested capital, and it creates a future amortization obligation. A company that capitalizes aggressively can report rising profit and rising returns while consuming cash and accumulating assets that may later be written off.

## A worked example

A software company reports EBIT of $50M and capitalizes $20M of development spending that it would previously have expensed. The new spending is amortized over four years, so current amortization on the new layer is $5M.

On an expensed basis, EBIT is roughly $50M − $20M + $5M = $35M, not $50M. Operating cash flow is largely unchanged because the cash was spent either way; the difference is presentation and timing. If the company reports invested capital of $400M, its reported return on capital is 12.5%. On an adjusted capital base that removes the unamortized software layer and uses adjusted profit, the return is lower and the trend may look very different.

The analyst should also ask whether the capitalized spending is maintaining existing products or creating new ones. Maintenance-like spending that is capitalized flatters profit without creating a durable asset. A capitalization policy that lengthens useful lives or lowers the threshold for capitalization is a change worth tracking.

## Research discipline

1. **Read the accounting-policy note** for capitalization thresholds, useful lives, and any change in estimate.
2. **Compare capitalized spending with amortization** over several years. A growing gap means the balance sheet is accumulating costs.
3. **Test impairment risk.** If the products or customers supported by the capitalized asset deteriorate, a write-down may follow.
4. **Keep cash flow separate from accounting profit.** Capitalization does not create cash; it changes when the cost appears in profit.
""",
        r"\text{Adj. EBIT}=\text{Reported EBIT}-\text{Capitalized costs}+\text{Amortization of new layer}",
        'reported_ebit = 50\ncapitalized = 20\nnew_amortization = 5\nadjusted_ebit = reported_ebit - capitalized + new_amortization\nprint("Reported EBIT:", reported_ebit)\nprint("Adjusted EBIT:", adjusted_ebit)\nprint("Reported return on capital (%):", round(reported_ebit / 400 * 100, 1))\nprint("Adjusted return on capital (%):", round(adjusted_ebit / 380 * 100, 1))',
        "A company reports EBIT of $80M, capitalizes $30M of costs, and records $6M of amortization on the new layer. It reports invested capital of $500M. Calculate adjusted EBIT and the reported versus adjusted return on capital, using $470M as the adjusted capital base. Then explain why cash flow is not improved by the capitalization.",
        "Adjusted EBIT is 80 − 30 + 6 = $56M. Reported return is 80/500 = 16.0%; adjusted return is 56/470 = 11.9%. Cash flow is not improved because the $30M was spent in cash either way; capitalization only defers the expense in the income statement. The analyst should check whether the spending creates a durable asset or merely maintains current products.",
        [
            q(
                "Capitalizing a cost instead of expensing it generally:",
                ["Raises current profit and creates future amortization", "Reduces current profit permanently", "Has no effect on the balance sheet"],
                0,
                "The cost moves to the balance sheet and is amortized later, raising current profit.",
            ),
            q(
                "Which question best tests whether capitalized software is a real asset?",
                [
                    "Whether it creates future economic benefits that can be sold or used",
                    "Whether the company's logo changed",
                    "Whether the CFO is an engineer",
                ],
                0,
                "Capitalization is justified by future economic benefit, not by job titles or branding.",
            ),
            q(
                "Reported EBIT is 60, capitalized costs are 10, and new amortization is 2. Adjusted EBIT is:",
                ["52", "60", "72"],
                0,
                "Adjusted EBIT is 60 − 10 + 2 = 52 after reversing the capitalization.",
            ),
        ],
    )

    add(
        "15.4",
        "II",
        "Inventory, reserves, and cookie-jar accounting",
        "Use inventory turnover, reserve movements, and write-down history to detect earnings management through the balance sheet.",
        r"""
## The analytical question

Inventory and accounting reserves are two of the most flexible areas in financial reporting. Inventory can be valued under different cost-flow assumptions, written down, or held at cost while its market value falls. Reserves for credit losses, warranties, restructuring, or litigation can be increased in good years and released in weak years, smoothing reported profit.

The analyst should track **inventory days** and the relationship between reserve movements and profit:

$$\text{Inventory days}=\frac{\text{Inventory}}{\text{COGS}}\times365$$

$$\text{Reserve release impact}=\frac{\Delta\text{Reserve}}{\text{Pre-tax profit}}$$

A reserve release is not necessarily improper. The question is whether the original reserve was reasonable and whether the release reflects a genuine change in the underlying obligation or a desire to meet a profit target.

## A worked example

A retailer reports revenue of $300M, COGS of $180M, and inventory of $90M, up from $60M. Inventory days rise from $60/160×365 = 136.9 to $90/180×365 = 182.5, a 45.6-day increase. At the same time, the company releases $6M from a warranty reserve, raising pre-tax profit from $20M to $26M.

The analyst reconstructs the release: the reserve balance fell from $15M to $9M. The release explains 23% of reported pre-tax profit. If claims experience has genuinely improved, the release may be justified. If claims are stable and the release coincides with a weak sales quarter, the analyst should treat the profit as lower quality.

Inventory is the second issue. The company may be carrying slow-moving goods at cost. A write-down would reduce profit and inventory. The analyst should compare inventory days with sales growth, inspect the inventory note for write-downs, and ask whether the gross margin is being supported by holding older, lower-cost inventory that will eventually be replaced at higher cost.

## Research discipline

1. **Read the inventory and reserve notes**, including any change in accounting estimate.
2. **Compare reserve movements with the underlying claims or losses.** A release without an improvement in experience is a yellow flag.
3. **Test gross margin against inventory age.** Older inventory can flatter margin until it is replaced or written down.
4. **Use cash flow as a cross-check.** A profit increase driven by a non-cash release does not improve operating cash.
""",
        r"\text{Inventory days}=\frac{\text{Inventory}}{\text{COGS}}365;\quad \text{Release impact}=\frac{\Delta\text{Reserve}}{\text{Pre-tax profit}}",
        'inventory = 90\ncogs = 180\nprior_inventory = 60\nprior_cogs = 160\nprint("Inventory days current:", round(inventory/cogs*365, 1))\nprint("Inventory days prior:", round(prior_inventory/prior_cogs*365, 1))\nrelease = 6\npretax = 26\nprint("Release share of pre-tax profit (%):", round(release/pretax*100, 1))',
        "A company reports inventory of $120M and COGS of $240M, versus inventory of $80M and COGS of $200M a year earlier. It also releases $10M from a restructuring reserve, raising pre-tax profit to $40M. Calculate inventory days and the release's share of profit, then state what evidence would make the release acceptable.",
        "Current inventory days are 120/240×365 = 182.5; prior days are 80/200×365 = 146.0. The release is 10/40 = 25% of pre-tax profit. It is acceptable if the underlying restructuring obligation genuinely fell, the original reserve was reasonable, and the release is disclosed as a change in estimate rather than a one-off gain engineered to meet a target. The analyst should read the reserve roll-forward and compare it with actual cash payments.",
        [
            q(
                "Inventory is 60, COGS is 120. Inventory days are:",
                ["91.25", "182.5", "365"],
                1,
                "60 / 120 × 365 = 182.5 days.",
            ),
            q(
                "A reserve release in a weak operating quarter is most suspicious when:",
                [
                    "The underlying claims experience has improved",
                    "The release is needed to meet a profit threshold and claims are unchanged",
                    "The release is disclosed in the notes",
                ],
                1,
                "A release that lacks an economic basis and coincides with a profit target is a classic smoothing warning sign.",
            ),
            q(
                "A reserve release affects operating cash flow by:",
                ["Increasing it by the release amount", "Usually not at all, because it is non-cash", "Reducing inventory"],
                1,
                "The release is an accounting adjustment; cash flow changes only if cash payments differ from the original estimate.",
            ),
        ],
    )

    add(
        "15.5",
        "II",
        "Related parties, SPEs, and circular transactions",
        "Trace transactions with affiliated entities and decide when off-balance-sheet structures transfer risk back to the parent.",
        r"""
## The analytical question

A related-party transaction is not automatically improper. Companies buy from affiliates, lease from family-owned properties, and fund joint ventures. The analytical question is whether the transaction is at arm's length, whether the counterparty can bear the risk it appears to assume, and whether the parent retains an obligation that the reported accounts do not show.

Special-purpose entities (SPEs) are a particular concern. A parent may sell assets to an SPE at a gain, guarantee the SPE's debt, or provide liquidity support. If the SPE's assets fall short, the risk can return to the parent. The analyst should reconstruct the economic substance:

$$\text{Adjusted parent risk}=\text{Reported debt}+\text{Guarantees}+\text{Liquidity commitments}+\text{SPE debt not consolidated}$$

and remove gains that depended on the SPE's willingness to pay above fair value.

## A worked example

A parent reports equity of $100M, including a $30M gain on the sale of a project to an SPE. The parent guarantees $25M of the SPE's $40M debt and has agreed to buy back the project if the SPE cannot refinance.

On an economic view, the $30M gain is not a completed sale: the parent retains downside risk through the guarantee and the buy-back. Adjusted equity removes the gain, leaving $70M. Adjusted debt adds the $25M guarantee, and a stress case adds the remaining $15M of SPE debt if the project deteriorates. The parent's reported leverage may look modest; the adjusted leverage may not.

The analyst must read the SPE's own financial statements if available, the guarantee terms, and the buy-back trigger. The key disclosure is often not the gain itself but the conditions under which the parent must return cash or absorb losses. A structure that is legally off-balance-sheet can still be economically on-balance-sheet.

## Research discipline

1. **Map every material related party** and the nature of the transaction: sales, purchases, loans, guarantees, or leases.
2. **Eliminate gains that are not supported by an independent buyer.** A sale to a controlled entity at a premium is not evidence of market value.
3. **Read guarantees and liquidity commitments** and stress the conditions that trigger them.
4. **Check the auditor's related-party procedures** and any disclosed weaknesses in controls.
""",
        r"\text{Adjusted parent risk}=\text{Debt}+\text{Guarantees}+\text{Liquidity commitments}+\text{Unconsolidated SPE debt}",
        'reported_equity = 100\nspe_gain = 30\nguarantee = 25\nspe_debt = 40\nprint("Adjusted equity after removing gain:", reported_equity - spe_gain)\nprint("Adjusted risk added (guarantee):", guarantee)\nprint("Stress-case SPE exposure:", spe_debt - guarantee)',
        "A parent reports equity of $150M, including a $40M gain from selling an asset to an affiliated fund. It guarantees $30M of the fund's $50M debt and has a liquidity backstop for the remainder. Reconstruct adjusted equity and the stress-case exposure. Explain why the legal sale may not settle the economic risk.",
        "Adjusted equity is $150M − $40M = $110M. The guarantee adds $30M of risk, and the stress case adds the remaining $20M of fund debt, for $50M of total exposure. The legal sale may not settle the economic risk because the parent retains a guarantee and a liquidity backstop; if the fund cannot pay, the parent's cash is still at risk. The gain should not be treated as a completed, arm's-length profit.",
        [
            q(
                "A sale of an asset to a controlled SPE at a gain should be tested for:",
                [
                    "Whether an independent buyer would pay the same price and whether the parent retains risk",
                    "Whether the SPE has a different name",
                    "Whether the gain is large enough to matter",
                ],
                0,
                "Economic substance depends on arm's-length pricing and retained risk, not on legal form.",
            ),
            q(
                "A guarantee of an SPE's debt is best treated as:",
                ["Irrelevant because it is off-balance-sheet", "A contingent claim to stress", "A guaranteed profit"],
                1,
                "A guarantee can become a real obligation if the SPE fails; it belongs in the risk analysis.",
            ),
            q(
                "Reported equity is 200, including a 50 gain from an affiliate sale. Adjusted equity is:",
                ["150", "200", "250"],
                0,
                "Remove the unsupported gain: 200 − 50 = 150.",
            ),
        ],
    )

    add(
        "15.6",
        "II",
        "The forensic scorecard and red-team memo",
        "Combine accrual, revenue, capitalization, related-party, and governance evidence into a weighted risk score and an auditable memo.",
        r"""
## The analytical question

Individual red flags can be explained away. A forensic conclusion is stronger when several independent signals point in the same direction. A scorecard makes the weights and the evidence explicit, so a reviewer can challenge the judgment rather than argue about a vague impression.

One practical design uses five categories, each scored from 0 (no concern) to 5 (severe concern):

$$\text{Forensic score}=\sum_i w_i s_i,\qquad \sum_i w_i=1$$

Suggested weights are 30% accruals and cash conversion, 25% revenue recognition, 15% capitalization and cost deferral, 20% related parties and hidden claims, and 10% governance and disclosure. The weights are a policy choice; the important discipline is to fix them before seeing the answer.

## A worked example

An analyst scores a company as follows: accruals 4, revenue 3, capitalization 2, related parties 5, governance 3. With the weights above:

$$0.30(4)+0.25(3)+0.15(2)+0.20(5)+0.10(3)=1.20+0.75+0.30+1.00+0.30=3.55$$

A score of 3.55 out of 5 is high. The largest contributor is related parties, followed by accruals. The memo should explain the evidence behind each score, not merely report the total. For related parties, the evidence might be a sale to an affiliated fund at a premium, a guarantee, and a buy-back obligation. For accruals, it might be a multi-year gap between profit and cash.

The score is not a probability of fraud. It is a structured way to decide how much additional work is required. A high score might lead to a refusal to invest, a demand for more disclosure, or a smaller position with a wider margin of safety. The memo should state which of those responses follows and why.

## Research discipline

1. **Fix the categories and weights before scoring.** Changing them after seeing the total destroys the discipline.
2. **Cite evidence for each score.** A number without a filing reference is an opinion.
3. **Look for correlated signals.** Accruals, revenue, and related-party concerns that reinforce each other are more serious than isolated flags.
4. **State the decision and the falsification trigger.** Explain what new evidence would lower the score or change the recommendation.
""",
        r"\text{Forensic score}=\sum_i w_i s_i;\quad 0\le s_i\le5;\quad \sum_i w_i=1",
        'accruals = 4\nrevenue = 3\ncapitalization = 2\nrelated = 5\ngovernance = 3\nscore = 0.30*accruals + 0.25*revenue + 0.15*capitalization + 0.20*related + 0.10*governance\nprint("Forensic score:", round(score, 2))\nprint("Accrual contribution:", 0.30*accruals)\nprint("Related-party contribution:", 0.20*related)',
        "A company scores 3 on accruals, 4 on revenue, 1 on capitalization, 2 on related parties, and 4 on governance, using the lesson's weights. Calculate the forensic score and identify the two largest contributors. Then state one decision the committee could take besides simply rejecting the investment.",
        "The score is 0.30(3) + 0.25(4) + 0.15(1) + 0.20(2) + 0.10(4) = 0.90 + 1.00 + 0.15 + 0.40 + 0.40 = 2.85. Revenue and governance are tied as the largest contributors at 1.00 each. Besides rejection, the committee could demand specific disclosures, commission an independent review of revenue contracts, or approve a smaller position with a wider margin of safety and a pre-registered review trigger.",
        [
            q(
                "A forensic scorecard is most useful when:",
                [
                    "The weights and evidence are fixed before the conclusion",
                    "The score is chosen to match the desired recommendation",
                    "Only one category is scored",
                ],
                0,
                "Pre-committing the weights and documenting evidence prevents the score from becoming a rationalization.",
            ),
            q(
                "A high forensic score should be interpreted as:",
                ["A finding of fraud", "A signal that more work or a stricter decision is required", "A guarantee of future losses"],
                1,
                "The score organizes risk; it is not a legal finding or a forecast.",
            ),
            q(
                "If accruals score 5 with a 40% weight and revenue scores 2 with a 20% weight, their weighted contribution totals:",
                ["2.0", "2.4", "3.0"],
                1,
                "0.40(5) + 0.20(2) = 2.0 + 0.4 = 2.4.",
            ),
        ],
    )

    checkpoints = [
        (
            "Checkpoint · accruals and revenue evidence",
            [
                (
                    "15.1",
                    q(
                        "Revenue is 500, receivables 100, and DSO is computed on 365 days. DSO is:",
                        ["36.5 days", "73 days", "100 days"],
                        1,
                        "100 / 500 × 365 = 73 days.",
                    ),
                ),
                (
                    "15.2",
                    q(
                        "Revenue rises 20% while receivables rise 80%. The most likely immediate concern is:",
                        [
                            "Faster cash collection",
                            "Slower collection or revenue recognized ahead of cash",
                            "A reduction in inventory",
                        ],
                        1,
                        "Receivables growing much faster than revenue lengthens DSO and raises recognition questions.",
                    ),
                ),
                (
                    "15.3",
                    q(
                        "Reported EBIT is 70, capitalized costs are 15, and new amortization is 3. Adjusted EBIT is:",
                        ["52", "58", "70"],
                        1,
                        "Adjusted EBIT is 70 − 15 + 3 = 58 after removing the capitalized cost and adding back amortization.",
                    ),
                ),
                (
                    "15.4",
                    q(
                        "Inventory is 80 and COGS is 160. Inventory days on 365 days are:",
                        ["91.25", "182.5", "365"],
                        1,
                        "80 / 160 × 365 = 182.5 days.",
                    ),
                ),
            ],
        ),
    ]

    return finish(
        {
            "id": "forensic-accounting",
            "number": 15,
            "title": "Forensic accounting & earnings quality",
            "description": "Read reported profit like an investigator: reconcile accruals, test revenue and capitalization, trace related parties, and score earnings quality.",
            "source": "Advanced security analysis · original cases with SEC enforcement anchors",
            "level": "Advanced",
            "icon": "book",
            "modules": modules,
            "prerequisites": "Security Analysis or equivalent comfort with the three financial statements. The course is quantitative but does not require programming.",
            "outcomes": [
                "Reconcile net income to operating cash and locate the working-capital cause of a gap.",
                "Test revenue recognition, capitalization, inventory, and related-party disclosures.",
                "Quantify hidden claims and adjust profit, capital, and leverage.",
                "Write a weighted forensic memo with evidence and a decision rule.",
            ],
            "readingGuide": "Each lesson pairs a compact method with a filing-reading protocol. Use a real annual report or 10-K as your laboratory; the worked figures are teaching numbers, not live recommendations.",
            "references": [
                {"title": "U.S. SEC · Enforcement actions and litigation releases", "url": "https://www.sec.gov/enforcement-litigation"},
                {"title": "U.S. SEC · EDGAR full-text search", "url": "https://efts.sec.gov/LATEST/search-index?q=%22revenue%20recognition%22"},
            ],
            "parts": [
                {"id": "I", "title": "Accruals, revenue, and costs", "description": "Cash conversion, revenue recognition, and capitalization"},
                {"id": "II", "title": "Reserves, related parties, and synthesis", "description": "Inventory and reserves, affiliated structures, and a forensic scorecard"},
            ],
            "studyType": "applied",
        },
        checkpoints,
    )
