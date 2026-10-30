"""Business quality, moats, and capital allocation course (17.x)."""

from advanced_security_common import finish, make_add, q

READING = (
    "Advanced security analysis · business quality. Read the company's returns-on-capital history, "
    "segment economics, incentive disclosures, and capital-allocation record beside this lesson. "
    "The worked figures are teaching numbers."
)


def build_quality_moats():
    modules = []
    add = make_add(modules, READING)

    add(
        "17.1",
        "I",
        "ROIC, WACC, and economic profit",
        "Calculate returns on invested capital, compare them with the cost of capital, and value the economic profit a business creates.",
        r"""
## The analytical question

A business creates value when its return on invested capital exceeds the cost of that capital. Accounting profit alone does not establish value creation: a company can grow earnings while earning less than its investors require. The analyst should compute **return on invested capital** and compare it with a **weighted average cost of capital**.

$$\text{ROIC}=\frac{\text{NOPAT}}{\text{Invested capital}}$$

$$\text{Economic profit}=(\text{ROIC}-\text{WACC})\times\text{Invested capital}$$

$$\text{Value}=\text{Invested capital}+\frac{\text{Economic profit}}{\text{WACC}-g}$$

The growth rate $g$ must be sustainable and below WACC for the formula to be finite. Economic profit is also called EVA. It makes the cost of capital explicit and prevents a high-return business from being valued as if its capital were free.

## A worked example

A company has invested capital of $500M and NOPAT of $75M, giving ROIC of 15%. Its WACC is 10%, so economic profit is (0.15 − 0.10) × $500M = $25M. If economic profit grows at 4% forever, the value is:

$$500+\frac{25}{0.10-0.04}=500+416.7=\$916.7\text{M}$$

Now suppose the company's ROIC falls to 11% while invested capital and WACC stay the same. Economic profit falls to $5M, and value falls to $500 + 5/0.06 = $583.3M. A 4-percentage-point decline in ROIC reduces value by about 36%. The sensitivity shows why the durability of returns matters as much as the current level.

The analyst should also test whether the invested capital base is measured consistently. Acquisitions, goodwill, capitalized research, and operating leases can all change the denominator. A company that looks high-return on a narrow capital base may look ordinary once acquiredintangibles are included.

## Research discipline

1. **Reconcile NOPAT** from operating profit, using a consistent tax rate and excluding nonrecurring items.
2. **Define invested capital consistently** across peers: debt plus equity, or operating assets minus non-interest-bearing liabilities.
3. **Use a WACC appropriate to the business and geography**, and disclose its inputs.
4. **Test the ROIC history** through a cycle. A single year's return may be a peak, not a durable advantage.
""",
        r"\text{ROIC}=\frac{\text{NOPAT}}{\text{IC}};\quad \text{EP}=(\text{ROIC}-\text{WACC})\text{IC};\quad V=\text{IC}+\frac{\text{EP}}{\text{WACC}-g}",
        'ic = 500\nnopat = 75\nwacc = 0.10\ngrowth = 0.04\nroic = nopat/ic\nep = (roic - wacc)*ic\nprint("ROIC (%):", round(roic*100, 1))\nprint("Economic profit:", round(ep, 1))\nprint("Value:", round(ic + ep/(wacc - growth), 1))\nroic2 = 0.11\nprint("Value at 11% ROIC:", round(ic + (roic2 - wacc)*ic/(wacc - growth), 1))',
        "A company has invested capital of $800M, NOPAT of $104M, WACC of 9%, and sustainable economic-profit growth of 3%. Calculate ROIC, economic profit, and value. Then calculate value if ROIC falls to 9% exactly.",
        "ROIC is 104/800 = 13.0%. Economic profit is (0.13 − 0.09) × 800 = $32M. Value is 800 + 32/(0.09 − 0.03) = 800 + 533.3 = $1,333.3M. At a 9% ROIC, economic profit is zero and value is simply invested capital, $800M, because the business earns exactly its cost of capital.",
        [
            q(
                "NOPAT is 60 and invested capital is 400. ROIC is:",
                ["10%", "15%", "25%"],
                1,
                "ROIC is 60 / 400 = 15%.",
            ),
            q(
                "A company earning exactly its WACC creates:",
                ["Positive economic profit", "Zero economic profit", "Infinite value"],
                1,
                "When ROIC equals WACC, the spread is zero and economic profit is zero.",
            ),
            q(
                "ROIC is 12%, WACC is 10%, and invested capital is 500. Economic profit is:",
                ["10", "20", "50"],
                0,
                "(0.12 − 0.10) × 500 = 10.",
            ),
        ],
    )

    add(
        "17.2",
        "I",
        "Moat sources and durability",
        "Identify the sources of a competitive advantage and test whether the evidence supports durability rather than a temporary lead.",
        r"""
## The analytical question

A moat is a structural reason a company can earn returns above its cost of capital for longer than competitors can erode them. Common sources are intangible assets (brands, patents, regulatory licences), switching costs, network effects, cost advantages, and efficient scale. A high current margin is not proof of a moat; it may be a cyclical peak or a temporary shortage.

The analyst should evaluate each source on two dimensions: **evidence** and **durability**. A useful scoring approach assigns 0–5 for evidence and 0–5 for durability to each source, then takes a weighted average. The weights should reflect how much of the company's profit the source actually protects.

$$\text{Moat score}=\sum_i w_i\frac{e_i+d_i}{2}$$

## A worked example

A payment network scores 5 on evidence and 5 on durability for network effects, 4 and 4 for switching costs, and 2 and 2 for brand. With weights of 50%, 30%, and 20%:

$$0.50(5)+0.30(4)+0.20(2)=2.50+1.20+0.40=4.10$$

A score of 4.10 out of 5 suggests a strong structural advantage, but the analyst should still ask what could erode it. Regulation, new technology, or a change in merchant behaviour could weaken network effects. A high score is a hypothesis to be tested, not a permanent property.

By contrast, a commodity producer might score high on cost advantage in one region but low on durability because new capacity can erode the cost position. The score should be tied to specific evidence: market share stability, customer retention, pricing history, and the returns of competitors. A moat that does not show up in returns is a story, not an advantage.

## Research discipline

1. **Tie every score to evidence**: retention rates, market share, pricing, cost curves, or regulatory barriers.
2. **Test durability through a shock.** Did the advantage survive a recession, a new entrant, or a technology change?
3. **Separate the moat from the industry.** A strong company in a weak industry may still earn poor returns.
4. **Look for erosion signals** such as falling ROIC, rising customer acquisition costs, or shortening contract lengths.
""",
        r"\text{Moat score}=\sum_i w_i\frac{e_i+d_i}{2};\quad 0\le e_i,d_i\le5",
        'network_evidence = 5\nnetwork_durability = 5\nswitching_evidence = 4\nswitching_durability = 4\nbrand_evidence = 2\nbrand_durability = 2\nnetwork_score = 0.50*(network_evidence + network_durability)/2\nswitching_score = 0.30*(switching_evidence + switching_durability)/2\nbrand_score = 0.20*(brand_evidence + brand_durability)/2\nprint("Moat score:", round(network_score + switching_score + brand_score, 2))\nprint("Network contribution:", round(network_score, 2))',
        "A company scores 4 and 5 for cost advantage, 3 and 3 for brand, and 2 and 4 for regulation, with weights of 40%, 35%, and 25%. Calculate the moat score. Then name one piece of evidence that would weaken the cost-advantage score.",
        "The score is 0.40(4.5) + 0.35(3.0) + 0.25(3.0) = 1.80 + 1.05 + 0.75 = 3.60. A new low-cost entrant, a rise in the company's unit costs relative to peers, or a technology that removes the scale advantage would weaken the cost-advantage score. The analyst should look for evidence in gross margins, unit costs, and competitor capacity announcements.",
        [
            q(
                "A high current margin is by itself:",
                ["Proof of a moat", "Only a signal that requires evidence of durability", "Irrelevant to quality"],
                1,
                "Margins can be cyclical or temporary; a moat requires a structural reason they persist.",
            ),
            q(
                "Which pair is a classic moat source?",
                ["Switching costs and network effects", "A rising share price and high trading volume", "A recent advertising campaign"],
                0,
                "Switching costs and network effects can protect returns structurally; price movement is not a moat.",
            ),
            q(
                "Evidence scores 4 and durability 4 with a 50% weight contribute:",
                ["2.0", "4.0", "8.0"],
                1,
                "0.50 × (4 + 4)/2 = 2.0; the other sources add to the total.",
            ),
        ],
    )

    add(
        "17.3",
        "I",
        "Reinvestment runway and incremental returns",
        "Separate growth that creates value from growth that merely consumes capital, using incremental returns on reinvestment.",
        r"""
## The analytical question

Growth is valuable only when the return on new investment exceeds the cost of capital. A company can grow revenue rapidly while destroying value if each new dollar of capital earns less than investors require. The analyst should estimate the **reinvestment rate** and the **incremental return on invested capital**:

$$g=\text{Reinvestment rate}\times\text{Incremental ROIC}$$

$$\text{Reinvestment rate}=\frac{\text{Net capex}+\text{Change in working capital}}{\text{NOPAT}}$$

A high growth rate can come from a high reinvestment rate, a high incremental return, or both. The quality of growth depends on which. A company reinvesting 80% of profit at a 25% return is creating more value than one reinvesting 20% at a 5% return, even if the latter reports faster near-term earnings growth from a low base.

## A worked example

A company has NOPAT of $100M, reinvests $40M, and earns 20% on incremental capital. Its implied growth is 40% × 20% = 8%. With a 10% WACC, the value is:

$$100\times\frac{1-0.08/0.20}{0.10-0.08}=100\times\frac{0.60}{0.02}=\$3{,}000\text{M}$$

Now suppose the incremental return falls to 10% while the reinvestment rate stays at 40%. Growth is 4%, and value is $100 × (1 − 0.04/0.10)/(0.10 − 0.04) = $100 × 0.60/0.06 = $1,000M. The company is still growing, but the growth no longer creates value because the new capital earns only the cost of capital.

The analyst should ask whether the company has a genuine runway. A high incremental return on a small capital base may not scale. A large runway with a modest return can still create value if the return exceeds WACC. The relevant question is the return on the next dollar, not the average return on the existing business.

## Research discipline

1. **Estimate incremental returns from segment data or project disclosures**, not from the consolidated average.
2. **Include working capital** in the reinvestment base; growth often consumes cash before it produces profit.
3. **Test whether the runway is real**: addressable market, competition, regulation, and capital intensity.
4. **Compare growth with the return on new capital** and state which one is driving the valuation.
""",
        r"g=\text{Reinvestment rate}\times\text{Incremental ROIC};\quad V=\text{NOPAT}\frac{1-g/\text{ROIC}}{WACC-g}",
        'nopat = 100\nreinvestment = 40\nincremental_roic = 0.20\nwacc = 0.10\nrate = reinvestment/nopat\ngrowth = rate*incremental_roic\nvalue = nopat*(1 - growth/incremental_roic)/(wacc - growth)\nprint("Reinvestment rate (%):", round(rate*100, 1))\nprint("Implied growth (%):", round(growth*100, 1))\nprint("Value:", round(value, 1))\nprint("Value at 10% incremental ROIC:", round(nopat*(1 - 0.04/0.10)/(wacc - 0.04), 1))',
        "A company has NOPAT of $150M, reinvests $60M, earns 18% on incremental capital, and has a 9% WACC. Calculate the reinvestment rate, implied growth, and value. Then calculate value if the incremental return falls to 9%.",
        "The reinvestment rate is 60/150 = 40%; implied growth is 0.40 × 0.18 = 7.2%. Value is 150 × (1 − 0.072/0.18)/(0.09 − 0.072) = 150 × 0.60/0.018 = $5,000M. At a 9% incremental return, growth is 3.6% and value is 150 × (1 − 0.036/0.09)/(0.09 − 0.036) = 150 × 0.60/0.054 = $1,666.7M. Growth at the cost of capital destroys most of the value.",
        [
            q(
                "Reinvestment rate is 50% and incremental ROIC is 20%. Implied growth is:",
                ["5%", "10%", "70%"],
                1,
                "0.50 × 0.20 = 0.10, or 10%.",
            ),
            q(
                "Growth creates value when:",
                ["Incremental ROIC exceeds WACC", "Revenue grows faster than costs", "The company issues more shares"],
                0,
                "New capital must earn more than the cost of capital to create value.",
            ),
            q(
                "NOPAT is 80 and reinvestment is 20. The reinvestment rate is:",
                ["20%", "25%", "80%"],
                1,
                "The reinvestment rate is 20 / 80 = 25% of NOPAT.",
            ),
        ],
    )

    add(
        "17.4",
        "II",
        "Capital allocation: dividends, buybacks, and acquisitions",
        "Compare the per-share consequences of dividends, repurchases, debt reduction, and acquisitions at explicit prices.",
        r"""
## The analytical question

Capital allocation is the decision about what to do with the cash the business generates. The options include reinvestment, dividends, share repurchases, debt reduction, and acquisitions. Each can create or destroy value depending on the price paid and the return available. The analyst should compare them on a per-share basis and ask whether the company is buying its own shares below intrinsic value or buying other businesses above it.

A repurchase at a price below intrinsic value increases value per remaining share. A repurchase above intrinsic value destroys value for continuing holders. The arithmetic is:

$$\text{Value per share after buyback}=\frac{\text{Pre-buyback equity value}-\text{Cash paid}}{\text{Shares outstanding}-\text{Shares repurchased}}$$

An acquisition should be tested at the price paid, not at the target's standalone value:

$$\text{Acquirer value created}=\text{Target value to acquirer}-\text{Purchase price}$$

## A worked example

A company has an equity value of $1,000M, 100M shares, and $160M of excess cash. The shares trade at $8.00, below the analyst's intrinsic value of $10.00. If the company buys back $160M of stock at $8.00, it retires 20M shares. The remaining equity value is $840M across 80M shares, or $10.50 per share. The buyback creates $0.50 per share for continuing holders because it purchases undervalued shares.

If the shares trade at $12.00 instead, the same $160M retires 13.33M shares. The remaining value is $840M across 86.67M shares, or $9.69 per share. The buyback destroys value for continuing holders because it purchases above intrinsic value. The same decision can be good or bad depending on price.

For an acquisition, suppose the acquirer pays $200M for a business worth $170M to the acquirer after synergies. The acquisition destroys $30M of value even if the target is a good standalone business. The analyst should separate the target's standalone value, the synergies, and the price paid.

## Research discipline

1. **Compare every allocation option at the same price and risk basis.** A dividend, a buyback, and an acquisition are not interchangeable.
2. **Test buybacks against intrinsic value**, not against last year's price or management's optimism.
3. **Separate synergies from the purchase price** in an acquisition. A good asset at a high price can still destroy value.
4. **Check the funding source.** Debt-funded buybacks transfer risk to creditors and can reduce financial flexibility.
""",
        r"V_{\text{after}}=\frac{V_0-\text{Cash paid}}{N_0-\text{Shares repurchased}};\quad \text{Value created}=\text{Target value}-\text{Price}",
        'value = 1000\nshares = 100\ncash = 160\nprice = 8.0\nretired = cash/price\nprint("Shares retired:", round(retired, 2))\nprint("Value per share after buyback:", round((value - cash)/(shares - retired), 2))\nprice2 = 12.0\nretired2 = cash/price2\nprint("Value per share at $12:", round((value - cash)/(shares - retired2), 2))',
        "A company has an equity value of $600M, 60M shares, and $120M of excess cash. It can repurchase shares at $8.00 or at $12.00. Calculate the value per share after each buyback and explain which price creates value for continuing shareholders.",
        "At $8.00, the company retires 15M shares; remaining value is $480M / 45M = $10.67 per share. At $12.00, it retires 10M shares; remaining value is $480M / 50M = $9.60 per share. The $8.00 buyback creates value if intrinsic value is above $8.00; the $12.00 buyback may destroy value if intrinsic value is below $12.00. The comparison requires an independent intrinsic-value estimate.",
        [
            q(
                "A buyback below intrinsic value generally:",
                ["Increases value per remaining share", "Decreases value per remaining share", "Has no effect on value"],
                0,
                "Retiring undervalued shares leaves the remaining holders with a larger claim on the same value.",
            ),
            q(
                "An acquisition creates value when:",
                ["The target is well known", "The value to the acquirer exceeds the price paid", "The acquirer issues shares"],
                1,
                "Value creation depends on the target's value to the acquirer relative to the purchase price.",
            ),
            q(
                "Equity value is 500, cash paid is 100, shares are 50, and 10 shares are retired. Value per share is:",
                ["8", "10", "12.5"],
                1,
                "(500 − 100) / (50 − 10) = 400 / 40 = 10.",
            ),
        ],
    )

    add(
        "17.5",
        "II",
        "Management incentives and governance",
        "Read compensation, ownership, board structure, and related-party dealings as evidence about whose interests management is likely to serve.",
        r"""
## The analytical question

Management quality is difficult to observe directly, but incentives and governance leave evidence. The analyst should ask: How is management paid? How much equity do managers own? Are there related-party transactions? Is the board independent? Are minority shareholders protected? Does the company have dual-class shares or a controlling family?

A simple governance score can be built from five categories: pay alignment, ownership, board independence, related-party dealings, and shareholder rights. Each is scored 0–5 and weighted. The score is not a moral judgment; it is a structured way to assess whether the people controlling the company are likely to allocate capital in the interests of all owners.

$$\text{Governance score}=\sum_i w_i s_i$$

## A worked example

A company has a CEO whose bonus is tied to revenue growth rather than returns on capital, owns 2% of the equity, and sits on a board with two independent directors out of seven. It has a history of leasing properties from a family-owned entity, and it has dual-class shares that give the founder 60% of voting power with 20% of the economic interest.

The analyst scores pay alignment 2, ownership 2, board independence 1, related-party dealings 1, and shareholder rights 1. With equal weights, the score is 1.4 out of 5. The combination is concerning: the CEO is rewarded for growth, owns little equity, faces a weak board, and controls the company through a dual-class structure. The related-party leases are a concrete path for value to leave the company.

The analyst should not assume misconduct. Many founder-controlled companies create substantial value. The point is that the governance structure increases the burden of proof on the analyst and may justify a larger margin of safety or a smaller position.

## Research discipline

1. **Read the proxy statement and compensation discussion** for the metrics that actually determine pay.
2. **Map ownership and voting control**, including dual-class shares and family vehicles.
3. **List related-party transactions** and compare their terms with market benchmarks.
4. **Test whether governance has affected capital allocation**: buybacks at high prices, acquisitions at large premiums, or loans to insiders.
""",
        r"\text{Governance score}=\sum_i w_i s_i;\quad 0\le s_i\le5",
        'pay = 2\nownership = 2\nboard = 1\nrelated = 1\nrights = 1\nscore = (pay + ownership + board + related + rights)/5\nprint("Average governance score:", round(score, 2))\nprint("Weakest category score:", min(pay, ownership, board, related, rights))',
        "A company scores 3 on pay alignment, 4 on ownership, 2 on board independence, 2 on related-party dealings, and 1 on shareholder rights. Calculate the equal-weighted score. Then explain why a founder-controlled company can still be a good investment despite a low governance score.",
        "The equal-weighted score is (3 + 4 + 2 + 2 + 1) / 5 = 2.4. A founder-controlled company can create value through long-term vision, concentrated ownership, and operational skill. The governance score is a risk indicator, not a verdict: the analyst should ask whether the controller's interests align with minority owners and whether the evidence shows fair treatment. A larger margin of safety may be appropriate.",
        [
            q(
                "A bonus tied to revenue growth without a return-on-capital condition most directly encourages:",
                ["Profitable growth", "Growth even when the return is below the cost of capital", "Lower leverage"],
                1,
                "A growth-only metric can reward size rather than value creation.",
            ),
            q(
                "Dual-class shares are most relevant to an analyst because they:",
                ["Separate economic ownership from voting control", "Guarantee superior returns", "Eliminate related-party risk"],
                0,
                "A founder can control the company with a minority economic stake, affecting governance and minority protection.",
            ),
            q(
                "A governance score of 1.5 out of 5 should lead an analyst to:",
                [
                    "Ignore governance because the score is subjective",
                    "Increase scrutiny and consider a larger margin of safety or smaller position",
                    "Assume fraud has occurred",
                ],
                1,
                "A low score raises the burden of proof; it is not proof of fraud.",
            ),
        ],
    )

    add(
        "17.6",
        "II",
        "The quality scorecard and disconfirming evidence",
        "Combine returns, moat, reinvestment, capital allocation, and governance into a quality score, then actively search for evidence that would change it.",
        r"""
## The analytical question

Quality analysis can become a collection of favorable impressions. A scorecard forces the analyst to state the dimensions, weights, and evidence. A **disconfirming-evidence** process then asks what observation would lower each score, and whether that observation has occurred.

A practical composite uses five dimensions:

| Dimension | Weight | What it measures |
| :--- | ---: | :--- |
| Returns on capital | 30% | ROIC versus WACC through a cycle |
| Moat durability | 25% | Evidence that the advantage survives competition |
| Reinvestment runway | 20% | Incremental returns and available opportunities |
| Capital allocation | 15% | Buybacks, dividends, and acquisitions at sensible prices |
| Governance | 10% | Incentives, control, and related-party risk |

$$\text{Quality score}=\sum_i w_i s_i$$

The weights reflect the analyst's view of what drives long-term value. They should be fixed before scoring and disclosed in the memo.

## A worked example

An analyst scores returns 4, moat 3, reinvestment 5, capital allocation 2, and governance 3. The composite is:

$$0.30(4)+0.25(3)+0.20(5)+0.15(2)+0.10(3)=1.20+0.75+1.00+0.30+0.30=3.55$$

The strongest contribution is reinvestment, and the weakest is capital allocation. The memo should explain why. Perhaps the company has a large addressable market and earns high incremental returns, but it has a history of buying back shares at high prices. The analyst should then ask what would change the capital-allocation score: a new policy tied to intrinsic value, a board change, or evidence that the prior buybacks were value-creating.

The disconfirming-evidence list might include: ROIC falling below WACC for two consecutive years, customer retention declining, incremental returns falling, a large acquisition at a premium, or a related-party transaction on unfavorable terms. If one of those occurs, the score and the valuation should change.

## Research discipline

1. **Fix weights and scoring rules before seeing the conclusion.**
2. **Write a disconfirming observation for each dimension** and monitor it.
3. **Separate quality from price.** A high-quality business can be a poor investment at the wrong price.
4. **Record the evidence date** for every score so the analysis can be updated without hindsight.
""",
        r"\text{Quality score}=\sum_i w_i s_i;\quad 0\le s_i\le5",
        'returns = 4\nmoat = 3\nreinvestment = 5\nallocation = 2\ngovernance = 3\nscore = 0.30*returns + 0.25*moat + 0.20*reinvestment + 0.15*allocation + 0.10*governance\nprint("Quality score:", round(score, 2))\nprint("Returns contribution:", round(0.30*returns, 2))\nprint("Reinvestment contribution:", round(0.20*reinvestment, 2))',
        "A company scores 5 on returns, 4 on moat, 3 on reinvestment, 3 on capital allocation, and 2 on governance, using the lesson's weights. Calculate the quality score and the largest contributor. Then state one disconfirming observation that would most reduce the returns score.",
        "The score is 0.30(5) + 0.25(4) + 0.20(3) + 0.15(3) + 0.10(2) = 1.50 + 1.00 + 0.60 + 0.45 + 0.20 = 3.75. Returns is the largest contributor at 1.50. A sustained fall in ROIC below WACC, or a multi-year decline in returns on new capital, would most directly reduce the returns score. The analyst should specify the measurement period and the evidence source.",
        [
            q(
                "A quality score is most useful when:",
                [
                    "It is calculated after the investment decision is made",
                    "The weights and evidence are stated before the conclusion",
                    "Only the highest-scoring dimension is used",
                ],
                1,
                "Pre-committing weights and evidence prevents the score from becoming a rationalization.",
            ),
            q(
                "Which pair best describes the purpose of a quality scorecard?",
                [
                    "To guarantee returns and eliminate risk",
                    "To organize evidence and make the judgment auditable",
                    "To replace the need for a valuation",
                ],
                1,
                "The scorecard structures qualitative evidence; it does not guarantee returns or replace valuation.",
            ),
            q(
                "Returns score 4 at 30% weight and moat score 2 at 25% weight contribute:",
                ["1.2", "1.7", "2.0"],
                1,
                "0.30(4) + 0.25(2) = 1.20 + 0.50 = 1.70.",
            ),
        ],
    )

    checkpoints = [
        (
            "Checkpoint · returns, moats, and allocation",
            [
                (
                    "17.1",
                    q(
                        "NOPAT is 90 and invested capital is 600. ROIC is:",
                        ["10%", "15%", "20%"],
                        1,
                        "ROIC is 90 / 600 = 15% of invested capital.",
                    ),
                ),
                (
                    "17.2",
                    q(
                        "A moat score is strongest when:",
                        [
                            "The advantage is large and has survived competitive shocks",
                            "The current margin is high for one quarter",
                            "The company spends the most on advertising",
                        ],
                        0,
                        "Durability and evidence matter more than a single period's margin or spending.",
                    ),
                ),
                (
                    "17.3",
                    q(
                        "Reinvestment rate is 40% and incremental ROIC is 15%. Implied growth is:",
                        ["4%", "6%", "15%"],
                        1,
                        "Implied growth is 0.40 × 0.15 = 6%.",
                    ),
                ),
                (
                    "17.4",
                    q(
                        "A company buys back shares above intrinsic value. For continuing shareholders this generally:",
                        ["Creates value", "Destroys value", "Has no effect"],
                        1,
                        "Paying more than the shares are worth transfers value to selling shareholders.",
                    ),
                ),
            ],
        ),
    ]

    return finish(
        {
            "id": "quality-moats",
            "number": 17,
            "title": "Business quality, moats & capital allocation",
            "description": "Decide whether a business earns more than its cost of capital, why, for how long, and whether management allocates the cash well.",
            "source": "Advanced security analysis · original quality cases with primary-source anchors",
            "level": "Advanced",
            "icon": "book",
            "modules": modules,
            "prerequisites": "Security Analysis or equivalent knowledge of returns, cost of capital, and financial statements.",
            "outcomes": [
                "Calculate ROIC, economic profit, and value from a capital base.",
                "Score moat sources against evidence and durability.",
                "Separate value-creating growth from growth that consumes capital.",
                "Evaluate buybacks, dividends, and acquisitions at explicit prices.",
            ],
            "readingGuide": "Use the company's annual report, proxy statement, and segment disclosures as the evidence base. The worked figures are teaching numbers, not recommendations.",
            "references": [
                {"title": "U.S. SEC · EDGAR company filings", "url": "https://www.sec.gov/edgar/searchedgar/companysearch"},
                {"title": "U.S. SEC · Investor.gov: evaluating stocks", "url": "https://www.investor.gov/introduction-investing/investing-basics/investment-products/stocks"},
            ],
            "parts": [
                {"id": "I", "title": "Returns, moats, and reinvestment", "description": "Economic profit, moat durability, and incremental returns"},
                {"id": "II", "title": "Capital allocation and governance", "description": "Buybacks, acquisitions, incentives, and a quality scorecard"},
            ],
            "studyType": "applied",
        },
        checkpoints,
    )
