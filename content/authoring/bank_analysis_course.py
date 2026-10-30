"""Bank and financial-institution analysis course (18.x)."""

from advanced_security_common import finish, make_add, q

READING = (
    "Advanced security analysis · banks and financial institutions. Read the regulatory capital, "
    "liquidity, asset-quality, and deposit disclosures beside this lesson. The worked figures are "
    "teaching numbers; the cited central-bank source supplies the real-world context."
)


def build_bank_analysis():
    modules = []
    add = make_add(modules, READING)

    add(
        "18.1",
        "I",
        "Bank balance sheets and net interest income",
        "Read a bank's earning assets, funding mix, net interest margin, and fee income as an operating business.",
        r"""
## The analytical question

A bank is a leveraged spread business. It funds assets with deposits and wholesale borrowings, lends or invests at a higher rate, and earns the difference. The analyst should separate the **net interest margin** from fee income and operating costs, because each has different risk and durability.

$$\text{NIM}=\frac{\text{Net interest income}}{\text{Average earning assets}}$$

$$\text{Pre-tax income}=\text{Net interest income}+\text{Non-interest income}-\text{Operating expenses}-\text{Provisions}$$

Bank statements look different from industrial statements. Loans are the main asset, deposits are the main funding source, and the allowance for credit losses is a critical estimate. Capital and liquidity are regulated, so the analyst must read the regulatory disclosures alongside the accounting statements.

## A worked example

A bank has average earning assets of $1,000M and net interest income of $30M, giving a NIM of 3.0%. Non-interest income is $8M, operating expenses are $20M, and provisions are $5M. Pre-tax income is $30 + $8 − $20 − $5 = $13M.

The NIM looks healthy, but the analyst must ask how it is produced. A bank can earn a wide margin by lending to riskier borrowers or by funding long-dated assets with short-dated deposits. The first choice raises credit risk; the second raises liquidity and interest-rate risk. A narrow margin can be safer if the loan book is high quality and the funding is stable.

The analyst should decompose the margin into asset yield and funding cost:

$$\text{NIM}\approx\text{Asset yield}-\text{Cost of funds}\times\frac{\text{Interest-bearing liabilities}}{\text{Earning assets}}$$

A rising funding cost with a stable asset yield compresses the margin. A rising asset yield with stable funding may reflect riskier lending. The composition matters as much as the level.

## Research discipline

1. **Use average balances** for earning assets and funding, and disclose the period.
2. **Separate interest and fee income.** Fees can be recurring or transactional; their durability differs.
3. **Read the funding mix**: deposits, wholesale borrowings, and maturities.
4. **Connect the margin to risk**: asset quality, duration, and liquidity.
""",
        r"\text{NIM}=\frac{\text{Net interest income}}{\text{Avg earning assets}};\quad \text{Pre-tax}=\text{NII}+\text{Fees}-\text{Opex}-\text{Provisions}",
        'earning_assets = 1000\nnii = 30\nfees = 8\nopex = 20\nprovisions = 5\nprint("NIM (%):", round(nii/earning_assets*100, 1))\nprint("Pre-tax income:", nii + fees - opex - provisions)',
        "A bank has average earning assets of $1,200M, net interest income of $42M, fee income of $10M, operating expenses of $26M, and provisions of $8M. Calculate NIM and pre-tax income. Then explain why a high NIM is not automatically a sign of quality.",
        "NIM is 42/1,200 = 3.5%. Pre-tax income is 42 + 10 − 26 − 8 = $18M. A high NIM can reflect riskier lending, a mismatched duration profile, or weak competition; it may also come with higher credit losses or liquidity risk. The analyst must connect the margin to the risk taken to earn it.",
        [
            q(
                "Net interest income is 40 and average earning assets are 1,000. NIM is:",
                ["2%", "4%", "40%"],
                1,
                "NIM is 40 / 1,000 = 4%.",
            ),
            q(
                "A bank's pre-tax income is reduced by:",
                ["Provisions and operating expenses", "Deposits", "Loan growth"],
                0,
                "Provisions for credit losses and operating costs are deductions from revenue.",
            ),
            q(
                "NII is 36, fees 6, opex 20, and provisions 4. Pre-tax income is:",
                ["18", "24", "26"],
                0,
                "36 + 6 − 20 − 4 = 18.",
            ),
        ],
    )

    add(
        "18.2",
        "I",
        "Asset quality and provisioning",
        "Measure non-performing loans, coverage, and credit cost, and test whether provisions are adequate for the loan book.",
        r"""
## The analytical question

A bank's largest risk is that borrowers do not repay. The analyst should measure the **non-performing loan ratio**, the **coverage ratio**, and the **credit cost**:

$$\text{NPL ratio}=\frac{\text{Non-performing loans}}{\text{Gross loans}}$$

$$\text{Coverage ratio}=\frac{\text{Allowance for credit losses}}{\text{Non-performing loans}}$$

$$\text{Credit cost}=\frac{\text{Provision expense}}{\text{Average gross loans}}$$

A high NPL ratio with low coverage suggests that losses may be under-reserved. A low NPL ratio with high coverage may be conservative, or it may reflect a loan book that has not yet deteriorated. The analyst should read the loan mix, collateral, and the definition of "non-performing" because banks can differ.

## A worked example

A bank has gross loans of $800M, non-performing loans of $40M, an allowance of $24M, and provision expense of $8M. The NPL ratio is 5.0%, coverage is 60.0%, and credit cost is 1.0%.

Suppose the analyst expects NPLs to rise to $80M and believes a 70% coverage ratio is appropriate. Required allowance is $56M. With a current allowance of $24M, the bank needs $32M of additional provisions. If pre-tax pre-provision profit is only $40M, the additional provision would consume 80% of it. The capital and dividend implications are material.

The analyst should also examine the loan book by segment. Commercial real estate, unsecured consumer loans, and small-business loans have different loss dynamics. A concentration in one segment can make the aggregate NPL ratio misleading. Collateral values matter: a well-secured loan may recover more even if it is non-performing.

## Research discipline

1. **Read the loan table by segment, collateral, and geography.**
2. **Compare the NPL definition and coverage with peers.** Definitions can differ.
3. **Test provisions against charge-offs and NPL formation.** A persistent gap between provisions and actual losses is a warning.
4. **Stress the loan book** with higher NPLs and lower collateral values, and show the capital impact.
""",
        r"\text{NPL ratio}=\frac{\text{NPL}}{\text{Gross loans}};\quad \text{Coverage}=\frac{\text{Allowance}}{\text{NPL}};\quad \text{Credit cost}=\frac{\text{Provisions}}{\text{Avg loans}}",
        'gross_loans = 800\nnpl = 40\nallowance = 24\nprovisions = 8\nprint("NPL ratio (%):", round(npl/gross_loans*100, 1))\nprint("Coverage (%):", round(allowance/npl*100, 1))\nprint("Credit cost (%):", round(provisions/gross_loans*100, 1))\nrequired = 80*0.70\nprint("Additional provisions:", required - allowance)',
        "A bank has gross loans of $1,000M, NPLs of $50M, an allowance of $30M, and provision expense of $12M. Calculate the NPL ratio, coverage, and credit cost. Then calculate the additional allowance needed if NPLs rise to $100M and the target coverage is 65%.",
        "The NPL ratio is 50/1,000 = 5.0%; coverage is 30/50 = 60.0%; credit cost is 12/1,000 = 1.2%. If NPLs rise to $100M and target coverage is 65%, required allowance is $65M. Additional provisions are 65 − 30 = $35M, before any charge-offs. The analyst should compare that amount with pre-tax pre-provision profit and capital.",
        [
            q(
                "NPLs are 30 and gross loans are 600. The NPL ratio is:",
                ["5%", "10%", "20%"],
                0,
                "The NPL ratio is 30 / 600 = 5%.",
            ),
            q(
                "Coverage ratio measures:",
                ["Allowance relative to NPLs", "Equity relative to deposits", "Loans relative to assets"],
                0,
                "Coverage shows how much of the non-performing book has already been provided for.",
            ),
            q(
                "Allowance is 20 and NPLs are 50. Coverage is:",
                ["20%", "40%", "60%"],
                1,
                "Coverage is 20 / 50 = 40% of non-performing loans.",
            ),
        ],
    )

    add(
        "18.3",
        "I",
        "Capital adequacy and regulatory ratios",
        "Interpret CET1, risk-weighted assets, leverage ratios, and capital buffers as constraints on growth and distributions.",
        r"""
## The analytical question

Bank capital absorbs losses and constrains risk-taking. The central ratio is **common equity tier 1 (CET1) divided by risk-weighted assets (RWA)**:

$$\text{CET1 ratio}=\frac{\text{CET1 capital}}{\text{Risk-weighted assets}}$$

Regulators also impose a **leverage ratio**, which uses total exposure rather than risk-weighted assets:

$$\text{Leverage ratio}=\frac{\text{Tier 1 capital}}{\text{Total leverage exposure}}$$

A bank can look well capitalized on a risk-weighted basis and thinly capitalized on a leverage basis if its assets are low-risk by regulatory weights. The analyst should read both, plus the buffer requirements and any restrictions on dividends or buybacks when a buffer is breached.

## A worked example

A bank has CET1 capital of $80M and RWA of $1,000M, giving a CET1 ratio of 8.0%. Assume the minimum is 4.5% plus a 2.5% conservation buffer, or 7.0%. The bank has 1.0 percentage point of headroom, equivalent to $10M of CET1 capital at the current RWA.

The leverage ratio is Tier 1 capital of $90M divided by total exposure of $1,200M, or 7.5%, against a 3% minimum. The bank looks comfortable on leverage but less so on risk-weighted capital. If RWA rise because the loan book becomes riskier, the CET1 ratio falls even if the balance sheet does not grow. That is the regulatory equivalent of a margin call: the bank may need to raise capital, shrink assets, or cut distributions.

The analyst should stress RWA growth and losses together. A credit shock can reduce capital and increase risk weights at the same time. The combination is more severe than either effect alone.

## Research discipline

1. **Use the regulatory filings**, not only the accounting equity, and reconcile the two.
2. **Read the RWA composition** and any model changes that affect risk weights.
3. **Track buffer requirements and distribution restrictions.**
4. **Stress capital and RWA together** under a credit shock.
""",
        r"\text{CET1}=\frac{\text{CET1 capital}}{\text{RWA}};\quad \text{Leverage}=\frac{\text{Tier 1}}{\text{Exposure}}",
        'cet1 = 80\nrwa = 1000\ntier1 = 90\nexposure = 1200\nprint("CET1 ratio (%):", round(cet1/rwa*100, 1))\nprint("Leverage ratio (%):", round(tier1/exposure*100, 1))\nprint("CET1 headroom over 7% (capital):", cet1 - 0.07*rwa)',
        "A bank has CET1 capital of $120M, RWA of $1,500M, Tier 1 capital of $135M, and total exposure of $2,000M. Calculate the CET1 and leverage ratios. If the minimum CET1 requirement including the buffer is 8%, how much capital headroom does the bank have?",
        "CET1 is 120/1,500 = 8.0%; leverage is 135/2,000 = 6.75%. At an 8% requirement, required CET1 is $120M, so headroom is zero. Any loss or RWA increase would breach the requirement unless the bank raises capital or reduces risk-weighted assets. The leverage ratio is above 3%, but the risk-weighted constraint is binding.",
        [
            q(
                "CET1 capital is 60 and RWA is 1,000. The CET1 ratio is:",
                ["3%", "6%", "60%"],
                1,
                "The CET1 ratio is 60 / 1,000 = 6%.",
            ),
            q(
                "The leverage ratio differs from the CET1 ratio because it:",
                ["Uses total exposure rather than risk-weighted assets", "Ignores capital", "Only applies to investment banks"],
                0,
                "The leverage ratio is a non-risk-weighted backstop.",
            ),
            q(
                "CET1 is 90, RWA is 1,200, and the requirement is 7%. Capital headroom is:",
                ["6", "10", "90"],
                0,
                "Required capital is 84; 90 − 84 = 6.",
            ),
        ],
    )

    add(
        "18.4",
        "II",
        "Liquidity, funding, and run risk",
        "Measure liquidity coverage, deposit concentration, and uninsured funding to assess how quickly a bank could be forced to sell assets.",
        r"""
## The analytical question

A bank can be solvent on a balance sheet and still fail because depositors and lenders withdraw funding faster than assets can be sold. The **liquidity coverage ratio** compares high-quality liquid assets with projected net cash outflows over a stress period:

$$\text{LCR}=\frac{\text{High-quality liquid assets}}{\text{Net cash outflows over 30 days}}$$

A ratio above 100% means the bank expects to have enough liquid assets to cover its modeled stress outflows. The model's assumptions matter: deposit stability, drawdowns on credit lines, and the marketability of securities.

The analyst should also examine **deposit concentration** and **uninsured deposits**:

$$\text{Top-10 deposit share}=\frac{\text{Top-10 deposits}}{\text{Total deposits}}$$

Concentrated, uninsured deposits are more likely to run. Long-duration assets funded by short-duration deposits create a maturity mismatch that can force sales at depressed prices.

## A worked example

A bank has $180M of high-quality liquid assets and projected net cash outflows of $150M over 30 days. Its LCR is 120%. Deposits are $1,000M, of which the top ten depositors hold $300M (30%), and 40% of deposits are uninsured.

The LCR looks adequate, but the concentration is high. If the top ten depositors withdraw half their balances, outflows increase by $150M, and the LCR falls to 180/300 = 60%, well below 100%. The bank would need to sell assets, borrow, or use central-bank facilities. If its assets are long-duration bonds trading below par, sales would crystallize losses.

The analyst should connect liquidity to capital. A forced sale at a loss reduces capital. A bank with thin capital and concentrated funding is more fragile than either ratio alone suggests. The 2023 regional-bank failures illustrated how quickly unrealized securities losses and uninsured deposit flight can interact.

## Research discipline

1. **Read the LCR and NSFR disclosures** and the assumptions behind the outflow model.
2. **Measure deposit concentration and uninsured deposits** from the funding note.
3. **Compare asset duration with funding duration.** A large mismatch is a liquidity risk even if the LCR looks adequate.
4. **Stress a run**: withdraw a share of uninsured deposits and mark securities to market.
""",
        r"\text{LCR}=\frac{\text{HQLA}}{\text{Net outflows}};\quad \text{Top-10 share}=\frac{\text{Top-10 deposits}}{\text{Deposits}}",
        'hqla = 180\noutflows = 150\ndeposits = 1000\ntop10 = 300\nuninsured_share = 0.40\nprint("LCR (%):", round(hqla/outflows*100, 1))\nprint("Top-10 deposit share (%):", round(top10/deposits*100, 1))\nprint("Uninsured deposits:", uninsured_share*deposits)\nstressed_outflows = outflows + top10*0.5\nprint("Stressed LCR (%):", round(hqla/stressed_outflows*100, 1))',
        "A bank has $240M of HQLA and $200M of projected net outflows. Deposits are $1,200M, the top ten depositors hold $360M, and 35% of deposits are uninsured. Calculate the LCR, top-10 share, and the LCR if half of the top-ten deposits leave.",
        "LCR is 240/200 = 120%. The top-10 share is 360/1,200 = 30%, and uninsured deposits are $420M. If half of the top-ten deposits leave, outflows rise by $180M to $380M, and the LCR falls to 240/380 = 63.2%. The bank would need additional liquid assets, borrowings, or asset sales to restore coverage.",
        [
            q(
                "HQLA is 150 and net outflows are 125. LCR is:",
                ["80%", "120%", "150%"],
                1,
                "LCR is 150 / 125 = 120%.",
            ),
            q(
                "Which funding profile is most fragile in a stress?",
                [
                    "Diversified insured retail deposits",
                    "Concentrated uninsured corporate deposits",
                    "Long-dated wholesale funding",
                ],
                1,
                "Concentrated uninsured deposits are more likely to withdraw quickly.",
            ),
            q(
                "An LCR below 100% means:",
                ["HQLA is less than projected net outflows", "The bank is insolvent", "Deposits are fully insured"],
                0,
                "The liquid asset buffer is below the modeled 30-day outflow.",
            ),
        ],
    )

    add(
        "18.5",
        "II",
        "Insurance and non-bank financials",
        "Read combined ratios, reserve development, and investment income for insurers and other non-bank financial institutions.",
        r"""
## The analytical question

Insurers and non-bank lenders have different accounting from banks, but the analytical questions are similar: What risks are being underwritten? Are reserves adequate? Is capital sufficient? For a property-and-casualty insurer, the **combined ratio** summarizes underwriting performance:

$$\text{Combined ratio}=\frac{\text{Losses}+\text{Expenses}}{\text{Premiums}}$$

A ratio below 100% indicates an underwriting profit before investment income. A ratio above 100% means the insurer relies on investment returns to earn a profit. Reserve development is critical: if prior-year reserves are increased, the current-year result absorbs the correction.

For a life insurer or a non-bank lender, the analyst should examine the duration of liabilities, the credit quality of assets, and the adequacy of reserves or loan-loss allowances.

## A worked example

An insurer writes $100M of premiums. Losses are $60M and expenses are $30M, so the combined ratio is 90% and underwriting profit is $10M. Investment assets are $700M and earn 4%, producing $28M of investment income. Pre-tax profit is $38M before other items.

The insurer then discloses $20M of adverse prior-year reserve development. The combined ratio becomes (60 + 20 + 30)/100 = 110%, and underwriting becomes a $10M loss. Pre-tax profit falls to $18M if investment income is unchanged. The adverse development is a signal that prior reserves were inadequate; the analyst should ask whether more development is likely.

The insurer's solvency depends on the duration and credit quality of its investment portfolio as well as its reserves. A portfolio concentrated in long-duration bonds can lose value when rates rise; a portfolio reaching for yield can take credit risk. The analyst should stress both sides of the balance sheet.

## Research discipline

1. **Separate underwriting from investment results.** A low combined ratio can be offset by investment losses.
2. **Read reserve development tables** and distinguish favorable from adverse development.
3. **Stress asset values and reserves together**, especially for long-tail liabilities.
4. **Check regulatory solvency ratios** and the quality of capital.
""",
        r"\text{Combined ratio}=\frac{\text{Losses}+\text{Expenses}}{\text{Premiums}};\quad \text{Pre-tax}=\text{Underwriting}+\text{Investment income}",
        'premiums = 100\nlosses = 60\nexpenses = 30\ninvestments = 700\nyield_rate = 0.04\ncombined = (losses + expenses)/premiums\nunderwriting = premiums - losses - expenses\nprint("Combined ratio (%):", round(combined*100, 1))\nprint("Underwriting profit:", underwriting)\nprint("Pre-tax income:", underwriting + investments*yield_rate)\nadverse = 20\nprint("Combined with adverse development (%):", round((losses + adverse + expenses)/premiums*100, 1))',
        "An insurer writes $200M of premiums, incurs $130M of losses and $50M of expenses, and earns 4% on $900M of investments. Calculate the combined ratio, underwriting profit, and pre-tax income. Then calculate the combined ratio if $30M of adverse reserve development is recognized.",
        "The combined ratio is (130 + 50)/200 = 90.0%; underwriting profit is $20M; investment income is $36M; pre-tax income is $56M. With $30M of adverse development, the combined ratio becomes (130 + 30 + 50)/200 = 105.0%, and underwriting becomes a $10M loss. Pre-tax income falls to $26M before any tax or other items.",
        [
            q(
                "Losses are 70 and expenses 25 on premiums of 100. The combined ratio is:",
                ["95%", "105%", "125%"],
                0,
                "The combined ratio is (70 + 25)/100 = 95%.",
            ),
            q(
                "Adverse reserve development means:",
                ["Prior reserves were too high", "Prior reserves were too low and are increased", "Investment income fell"],
                1,
                "Adverse development increases reserves for prior-year claims, reducing current profit.",
            ),
            q(
                "Combined ratio is 105% and investment income is 20. Underwriting result is:",
                ["A profit of 5", "A loss of 5", "A loss of 20"],
                1,
                "A 105% combined ratio implies a 5% underwriting loss before investment income.",
            ),
        ],
    )

    add(
        "18.6",
        "II",
        "Valuing a bank: P/B, residual income, and cost of equity",
        "Value a financial institution from sustainable return on equity, growth, and the cost of equity rather than from industrial free cash flow.",
        r"""
## The analytical question

A bank's equity value is driven by its **return on equity**, its **cost of equity**, and its **sustainable growth**. A simple residual-income model expresses the price-to-book multiple as:

$$\frac{P}{B}=\frac{\text{ROE}-g}{\text{COE}-g}$$

where ROE is the sustainable return on equity, COE is the cost of equity, and $g$ is the growth rate of book equity. The formula requires COE > g and assumes the bank can sustain both its ROE and its growth. A bank earning exactly its cost of equity is worth book value; a bank earning more is worth a premium; a bank earning less is worth a discount.

A bank's growth is constrained by capital. If it retains earnings and grows risk-weighted assets faster than capital, its capital ratio falls. The analyst should connect growth to capital and to the returns on new lending.

## A worked example

A bank has book equity of $100M, a sustainable ROE of 12%, a cost of equity of 10%, and sustainable growth of 3%. The justified P/B is:

$$\frac{0.12-0.03}{0.10-0.03}=\frac{0.09}{0.07}=1.286$$

The indicated equity value is $100M × 1.286 = $128.6M. If the bank trades at 0.9× book, the market is implying a lower ROE, a higher cost of equity, or slower growth. The analyst should ask which assumption the market is challenging.

If the bank's ROE falls to 8% while COE stays at 10%, the justified P/B becomes (0.08 − 0.03)/(0.10 − 0.03) = 0.714. The bank is worth a discount to book because it destroys value on new equity. A bank with a low ROE and a high payout may still be worth book if it shrinks rather than reinvests at a loss.

## Research discipline

1. **Use sustainable ROE**, not the latest year, and adjust for one-off items.
2. **Estimate COE from a defensible risk-free rate, beta, and equity risk premium.**
3. **Tie growth to capital and returns.** Growth without capital is not sustainable.
4. **Compare the implied P/B with the bank's history and peers**, and explain the difference.
""",
        r"\frac{P}{B}=\frac{\text{ROE}-g}{\text{COE}-g};\quad V=B\times\frac{P}{B}",
        'book = 100\nroe = 0.12\ncoe = 0.10\ngrowth = 0.03\npb = (roe - growth)/(coe - growth)\nprint("Justified P/B:", round(pb, 3))\nprint("Equity value:", round(book*pb, 1))\nprint("P/B at 8% ROE:", round((0.08 - growth)/(coe - growth), 3))',
        "A bank has book equity of $250M, a sustainable ROE of 11%, a cost of equity of 9%, and growth of 3.5%. Calculate the justified P/B and equity value. Then calculate the P/B if the ROE falls to 7%.",
        "The justified P/B is (0.11 − 0.035)/(0.09 − 0.035) = 0.075/0.055 = 1.364; equity value is $250M × 1.364 = $340.9M. At a 7% ROE, the P/B is (0.07 − 0.035)/0.055 = 0.636, a discount to book because the bank earns less than its cost of equity. The market price may already reflect this, so the analyst must compare the implied assumptions with the current quote.",
        [
            q(
                "ROE is 12%, COE is 10%, and growth is 2%. Justified P/B is:",
                ["1.0", "1.25", "2.0"],
                1,
                "(0.12 − 0.02)/(0.10 − 0.02) = 0.10/0.08 = 1.25.",
            ),
            q(
                "A bank earning exactly its cost of equity should trade at:",
                ["A premium to book", "Book value under the simple model", "Zero"],
                1,
                "When ROE = COE, the P/B formula gives 1.0.",
            ),
            q(
                "ROE is 8%, COE is 10%, and growth is 2%. Justified P/B is:",
                ["0.75", "1.00", "1.25"],
                0,
                "(0.08 − 0.02)/(0.10 − 0.02) = 0.06/0.08 = 0.75.",
            ),
        ],
    )

    checkpoints = [
        (
            "Checkpoint · bank margins, credit, and capital",
            [
                (
                    "18.1",
                    q(
                        "NII is 45 and earning assets are 1,500. NIM is:",
                        ["2%", "3%", "4%"],
                        1,
                        "NIM is 45 / 1,500 = 3%.",
                    ),
                ),
                (
                    "18.2",
                    q(
                        "NPLs are 40 and gross loans are 800. The NPL ratio is:",
                        ["5%", "10%", "20%"],
                        0,
                        "The NPL ratio is 40 / 800 = 5%.",
                    ),
                ),
                (
                    "18.3",
                    q(
                        "CET1 is 90 and RWA is 1,200. The CET1 ratio is:",
                        ["7.5%", "9.0%", "12.0%"],
                        0,
                        "The CET1 ratio is 90 / 1,200 = 7.5%.",
                    ),
                ),
                (
                    "18.4",
                    q(
                        "HQLA is 210 and net outflows are 175. LCR is:",
                        ["80%", "120%", "175%"],
                        1,
                        "LCR is 210 / 175 = 120%.",
                    ),
                ),
            ],
        ),
    ]

    return finish(
        {
            "id": "bank-analysis",
            "number": 18,
            "title": "Analyzing banks & financial institutions",
            "description": "Read bank margins, loan quality, capital, liquidity, and insurance economics, then value a financial institution from sustainable ROE.",
            "source": "Advanced security analysis · original bank cases with central-bank and regulatory anchors",
            "level": "Advanced",
            "icon": "book",
            "modules": modules,
            "prerequisites": "Security Analysis or equivalent knowledge of financial statements. Familiarity with leverage and interest rates helps.",
            "outcomes": [
                "Decompose bank net interest margin and pre-tax income.",
                "Measure NPLs, coverage, and credit cost under stress.",
                "Interpret CET1, leverage ratios, LCR, and deposit concentration.",
                "Value a bank from ROE, cost of equity, and sustainable growth.",
            ],
            "readingGuide": "Read the regulatory capital and liquidity disclosures beside each lesson. The worked figures are teaching numbers; the cited sources supply the real-world context.",
            "references": [
                {"title": "Federal Reserve · SVB review: key takeaways", "url": "https://www.federalreserve.gov/publications/2023-April-SVB-Key-Takeaways.htm"},
                {"title": "Bank for International Settlements · Basel Committee publications", "url": "https://www.bis.org/bcbs/publications.htm"},
            ],
            "parts": [
                {"id": "I", "title": "Margins, credit, and capital", "description": "NIM, asset quality, and regulatory capital"},
                {"id": "II", "title": "Liquidity, insurance, and valuation", "description": "Run risk, non-bank financials, and residual-income valuation"},
            ],
            "studyType": "applied",
        },
        checkpoints,
    )
