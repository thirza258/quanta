"""Cyclicals, commodities, and industrial analysis course (20.x)."""

from advanced_security_common import finish, make_add, q

READING = (
    "Advanced security analysis · cyclicals and commodities. Read the company's capacity, hedging, "
    "cost-curve, and through-cycle margin disclosures beside this lesson. The worked figures are "
    "teaching numbers; the cited sources supply the real-world context."
)


def build_cyclical_industrials():
    modules = []
    add = make_add(modules, READING)

    add(
        "20.1",
        "I",
        "Mid-cycle normalization for cyclicals",
        "Normalize revenue and margins across a full cycle and avoid capitalizing either a peak or a trough.",
        r"""
## The analytical question

Cyclical businesses earn different profits at different points in the cycle. A valuation that uses the current year's earnings can be badly wrong if the current year is a peak or a trough. The analyst should build a **mid-cycle** estimate from a full cycle of margins and a normalized revenue base.

$$\overline{m}=\frac{1}{n}\sum_{t=1}^{n}m_t$$

$$\text{Normalized EBIT}=\overline{m}\times\text{Normalized revenue}$$

The cycle should include at least one downturn and one recovery. For a capital-intensive industrial, a seven- to ten-year window may be appropriate; for a commodity producer, the cycle can be longer. The normalized revenue base should reflect sustainable volume and market share, not the best year.

## A worked example

A steel producer reports EBIT margins of 4%, 8%, 12%, 6%, and −2% over five years. The average margin is (4 + 8 + 12 + 6 − 2)/5 = 5.6%. Normalized revenue is $800M, so normalized EBIT is $44.8M.

The current year is a peak: revenue is $900M and the margin is 12%, producing $108M of EBIT. At a 7× EV/EBIT multiple, the peak valuation is $756M; at 7× normalized EBIT, it is $313.6M. The difference is the cyclical illusion. A buyer at the peak multiple is paying for earnings that may not persist.

The analyst should also normalize the balance sheet. A cyclical company may have invested heavily at the top of the cycle, leaving debt and idle capacity in the downturn. The valuation should include the cost of carrying that capacity and the risk of a prolonged trough.

## Research discipline

1. **State the cycle window and why it is representative.**
2. **Normalize revenue and margin separately**, and reconcile them to historical data.
3. **Include a trough case** with negative or low EBIT and the associated liquidity needs.
4. **Compare the normalized multiple with the company's own history**, not only with today's peers.
""",
        r"\overline{m}=\frac{1}{n}\sum_t m_t;\quad \text{Normalized EBIT}=\overline{m}\times\text{Normalized revenue}",
        'margins = [0.04, 0.08, 0.12, 0.06, -0.02]\nnormalized_revenue = 800\navg = sum(margins) / len(margins)\nprint("Average margin (%):", round(avg * 100, 1))\nprint("Normalized EBIT:", round(avg * normalized_revenue, 1))\nprint("Peak EBIT:", 0.12 * 900)\nprint("Peak value at 7x:", 7 * 0.12 * 900)\nprint("Normalized value at 7x:", 7 * avg * normalized_revenue)',
        "A chemical producer reports margins of 5%, 9%, 11%, 7%, and 1% over five years. Normalized revenue is $600M and the current peak EBIT is $66M. Calculate the average margin, normalized EBIT, and the value at 6× normalized EBIT. Explain why the peak EBIT overstates sustainable earning power.",
        "The average margin is (5 + 9 + 11 + 7 + 1)/5 = 6.6%. Normalized EBIT is 6.6% × $600M = $39.6M. At 6× normalized EBIT, value is $237.6M. The peak EBIT of $66M is 67% higher than normalized EBIT and reflects the best point in the cycle; capitalizing it assumes the peak persists, which overstates value and understates the downside.",
        [
            q(
                "Margins of 2%, 4%, 6%, 8%, and 10% have an average of:",
                ["5%", "6%", "8%"],
                1,
                "The sum is 30%; divided by five years, the average is 6%.",
            ),
            q(
                "A peak-year EBIT multiple is dangerous because:",
                ["Peak earnings may not persist", "Multiples are always wrong", "EBIT is not a real measure"],
                0,
                "The denominator is temporarily high, making the multiple look deceptively low.",
            ),
            q(
                "Average margin is 6% and normalized revenue is 500. Normalized EBIT is:",
                ["30", "60", "300"],
                0,
                "0.06 × 500 = 30, so normalized EBIT is 30.",
            ),
        ],
    )

    add(
        "20.2",
        "I",
        "Commodity exposure and hedging",
        "Measure a producer's sensitivity to commodity prices and the effect of hedges on revenue, margins, and risk.",
        r"""
## The analytical question

A commodity producer's profit is driven by the difference between the price it receives and the cost of production. The analyst should separate **volume**, **price**, and **unit cost**, then model the effect of a price change. Hedges can reduce near-term volatility, but they do not create value; they shift cash flows between periods and can limit upside.

$$\text{Revenue}=\text{Volume}\times\text{Realized price}$$

$$\text{Realized price}=h\times\text{Hedge price}+(1-h)\times\text{Spot price}$$

where $h$ is the hedged share of volume. A producer with a high hedge ratio has more predictable near-term cash flow but less exposure to a price recovery.

## A worked example

A producer sells 100,000 tonnes at a spot price of $50 per tonne. Unit cash cost is $35, so unhedged EBIT is 100,000 × ($50 − $35) = $1.5M.

Suppose the producer has hedged 60% of volume at $48 per tonne. At a spot price of $50, the realized price is 0.60($48) + 0.40($50) = $48.80, and EBIT is 100,000 × ($48.80 − $35) = $1.38M. The hedge costs $0.12M relative to the unhedged case because the hedge price is below spot.

If spot falls to $40, the unhedged EBIT is 100,000 × ($40 − $35) = $0.5M. The hedged realized price is 0.60($48) + 0.40($40) = $44.80, and EBIT is 100,000 × ($44.80 − $35) = $0.98M. The hedge protects the downside. The analyst should value the producer with and without the hedge, and note the hedge's maturity and counterparty risk.

## Research discipline

1. **Read the hedging note**: volumes, prices, maturities, and counterparties.
2. **Model spot-price scenarios** with and without hedges.
3. **Separate realized price from spot price** and reconcile the difference.
4. **Check the cost curve**: a high-cost producer can lose money even at a healthy spot price.
""",
        r"\text{Realized}=hP_{\text{hedge}}+(1-h)P_{\text{spot}};\quad \text{EBIT}=V(P_{\text{realized}}-C_{\text{unit}})",
        'volume = 100000\nspot = 50\ncost = 35\nhedge_ratio = 0.60\nhedge_price = 48\nrealized = hedge_ratio*hedge_price + (1 - hedge_ratio)*spot\nprint("Realized price:", realized)\nprint("Hedged EBIT:", round(volume*(realized - cost), 2))\nprint("Unhedged EBIT:", round(volume*(spot - cost), 2))\nspot2 = 40\nrealized2 = hedge_ratio*hedge_price + (1 - hedge_ratio)*spot2\nprint("Stressed hedged EBIT:", round(volume*(realized2 - cost), 2))\nprint("Stressed unhedged EBIT:", round(volume*(spot2 - cost), 2))',
        "A producer sells 80,000 tonnes. Unit cost is $30, spot is $45, and 50% of volume is hedged at $44. Calculate realized price and EBIT. Then calculate EBIT if spot falls to $32, with and without the hedge.",
        "At spot $45, realized price is 0.50(44) + 0.50(45) = $44.50; EBIT is 80,000 × (44.50 − 30) = $1.16M. At spot $32, the hedged realized price is 0.50(44) + 0.50(32) = $38, and EBIT is 80,000 × (38 − 30) = $0.64M. Unhedged EBIT at $32 is 80,000 × (32 − 30) = $0.16M. The hedge protects $0.48M of EBIT in the stress.",
        [
            q(
                "A producer hedges 60% at $10 and spot is $12. Realized price is:",
                ["$10.80", "$11.20", "$12.00"],
                0,
                "0.60(10) + 0.40(12) = 6 + 4.8 = $10.80.",
            ),
            q(
                "A hedge primarily:",
                ["Creates value from price movements", "Shifts price exposure across periods", "Eliminates all business risk"],
                1,
                "Hedges transfer or smooth price exposure; they do not create economic value by themselves.",
            ),
            q(
                "Volume is 10,000, realized price $20, unit cost $15. EBIT is:",
                ["$5,000", "$50,000", "$200,000"],
                1,
                "10,000 × (20 − 15) = $50,000.",
            ),
        ],
    )

    add(
        "20.3",
        "I",
        "Operating leverage and capacity utilization",
        "Quantify how fixed costs amplify profit changes as volume moves through the cycle.",
        r"""
## The analytical question

Operating leverage describes how a change in revenue affects operating profit when costs are partly fixed. A company with high fixed costs and low variable costs has high operating leverage: profits rise quickly when volume grows and fall quickly when it declines. The **degree of operating leverage** is:

$$\text{DOL}=\frac{\text{Contribution margin}}{\text{EBIT}}$$

$$\text{Contribution margin}=\text{Revenue}-\text{Variable costs}$$

A high DOL is not inherently good or bad. It magnifies both upside and downside. The analyst should combine it with a view of capacity utilization: when a plant is near full capacity, additional volume may require new capital; when utilization is low, incremental volume can be very profitable.

## A worked example

A manufacturer has fixed costs of $40M and variable costs of 60% of revenue. At revenue of $150M, contribution margin is $60M and EBIT is $20M. DOL is 60/20 = 3.0×.

If revenue rises 10% to $165M, contribution margin rises to $66M and EBIT rises to $26M, a 30% increase. The 10% revenue increase produces a 30% profit increase because the fixed cost base is spread over more units. If revenue falls 10% to $135M, contribution margin is $54M and EBIT is $14M, a 30% decline.

The analyst should also consider capacity. If the plant is already at 95% utilization, a 10% volume increase may require overtime, new equipment, or a second shift, raising variable or fixed costs. The historical DOL may understate the cost of growth at the margin.

## Research discipline

1. **Separate fixed and variable costs** from the cost-of-sales and operating-expense notes.
2. **Estimate capacity utilization** and the cost of incremental volume.
3. **Model both a volume increase and a decrease**; operating leverage cuts both ways.
4. **Compare DOL across peers** with similar cost structures, not across unrelated industries.
""",
        r"\text{DOL}=\frac{\text{Contribution}}{\text{EBIT}};\quad \text{Contribution}=\text{Revenue}-\text{Variable costs}",
        'revenue = 150\nfixed = 40\nvariable_ratio = 0.60\ncontribution = revenue*(1 - variable_ratio)\nebit = contribution - fixed\nprint("Contribution:", contribution)\nprint("EBIT:", ebit)\nprint("DOL:", contribution/ebit)\nrevenue2 = revenue*1.10\ncontribution2 = revenue2*(1 - variable_ratio)\nprint("EBIT at +10% revenue:", contribution2 - fixed)',
        "A company has revenue of $200M, fixed costs of $50M, and variable costs of 55% of revenue. Calculate contribution margin, EBIT, and DOL. Then calculate EBIT if revenue falls 10%.",
        "Contribution margin is 200 × 0.45 = $90M. EBIT is 90 − 50 = $40M. DOL is 90/40 = 2.25×. A 10% revenue decline reduces contribution to $81M and EBIT to $31M, a 22.5% decline, which matches the DOL. The analyst should check whether fixed costs are truly fixed in a downturn; management may cut them, reducing the decline.",
        [
            q(
                "Contribution is 80 and EBIT is 20. DOL is:",
                ["2×", "4×", "8×"],
                1,
                "DOL is 80 / 20 = 4×.",
            ),
            q(
                "High operating leverage:",
                ["Amplifies both profit increases and decreases", "Only increases profit", "Eliminates fixed costs"],
                0,
                "The same fixed cost base magnifies the effect of revenue changes in both directions.",
            ),
            q(
                "Revenue is 100, variable costs are 60, fixed costs are 20. EBIT is:",
                ["20", "40", "60"],
                0,
                "EBIT is 100 − 60 − 20 = 20.",
            ),
        ],
    )

    add(
        "20.4",
        "II",
        "Working-capital cycles in industrial businesses",
        "Link receivables, inventory, and payables to cash generation and identify when growth consumes cash.",
        r"""
## The analytical question

Industrial businesses often consume cash as they grow. Receivables and inventory rise before customers pay, while payables may partially offset the outflow. The **cash conversion cycle** measures the net days of cash tied up:

$$\text{CCC}=\text{DSO}+\text{DIO}-\text{DPO}$$

A growing company with a long cycle can report strong profit and still need external financing. A cyclical downturn can reverse the cycle: inventory rises as orders slow, receivables age, and payables are stretched. The analyst should model working capital as a function of revenue, not as a fixed balance.

## A worked example

A machinery maker has revenue of $500M, COGS of $300M, receivables of $80M, inventory of $70M, and payables of $50M. DSO is 58.4 days, DIO is 85.2 days, and DPO is 60.8 days, for a CCC of 82.8 days.

The company plans to grow revenue 20% to $600M. If the cycle stays constant, receivables rise to about $96M, inventory to $84M, and payables to $60M. The net working-capital increase is ($96 + $84 − $60) − ($80 + $70 − $50) = $120M − $100M = $20M. That $20M consumes cash before the new revenue produces profit.

If the cycle lengthens during the growth phase, the cash need is larger. The analyst should model a stress case with slower collections and higher inventory, then compare the cash need with the company's liquidity and revolver capacity.

## Research discipline

1. **Model working capital as a percentage of revenue or COGS**, not as a constant balance.
2. **Test a downturn** in which inventory and receivables rise while payables are stretched.
3. **Compare the cash need with liquidity** and covenant headroom.
4. **Check the quality of receivables and inventory** before assuming they will convert at book value.
""",
        r"\text{CCC}=\text{DSO}+\text{DIO}-\text{DPO};\quad \Delta\text{NWC}=\text{NWC}_{t+1}-\text{NWC}_t",
        'revenue = 500\ncogs = 300\nar = 80\ninv = 70\nap = 50\nnwc = ar + inv - ap\nccc = ar/revenue*365 + inv/cogs*365 - ap/cogs*365\nprint("CCC:", round(ccc, 1))\nrevenue2 = 600\ncogs2 = 360\nar2 = revenue2*ar/revenue\ninv2 = cogs2*inv/cogs\nap2 = cogs2*ap/cogs\nprint("New NWC:", round(ar2 + inv2 - ap2, 1))\nprint("NWC increase:", round(ar2 + inv2 - ap2 - nwc, 1))',
        "A company has revenue of $400M, COGS of $240M, receivables of $60M, inventory of $48M, and payables of $36M. It plans 25% revenue growth with constant ratios. Calculate the current cash conversion cycle and the incremental working capital required.",
        "Current DSO is 60/400×365 = 54.75; DIO is 48/240×365 = 73.0; DPO is 36/240×365 = 54.75; CCC is 73.0 days. Current net working capital is 60 + 48 − 36 = $72M. At 25% higher revenue and COGS, receivables are $75M, inventory $60M, and payables $45M, for $90M of net working capital. The incremental need is $18M.",
        [
            q(
                "Net working capital in this lesson is:",
                ["Receivables plus inventory minus payables", "Cash plus debt", "Revenue minus COGS"],
                0,
                "The operating working-capital definition nets the three operating accounts.",
            ),
            q(
                "A company growing revenue with a constant cash conversion cycle generally:",
                ["Releases cash", "Requires incremental working capital", "Has no cash effect"],
                1,
                "Receivables and inventory grow with revenue, tying up cash.",
            ),
            q(
                "Current NWC is 100 and new NWC is 130. The incremental cash need is:",
                ["30", "100", "130"],
                0,
                "The incremental cash need is 130 − 100 = 30.",
            ),
        ],
    )

    add(
        "20.5",
        "II",
        "Capital intensity and maintenance capex",
        "Separate maintenance spending from growth investment and measure the cash a business must reinvest to stand still.",
        r"""
## The analytical question

Capital-intensive businesses must spend to maintain their assets before they can grow. Reported depreciation is an accounting estimate; actual maintenance capital spending may be higher or lower. The analyst should separate **maintenance capex** from **growth capex**:

$$\text{FCF}_{\text{maintenance}}=\text{CFO}-\text{Maintenance capex}$$

$$\text{Growth capex}=\text{Total capex}-\text{Maintenance capex}$$

A company that underinvests in maintenance can report strong near-term cash flow while deferring necessary spending. A company that overspends on growth can destroy value if the incremental returns are below the cost of capital.

## A worked example

A manufacturer reports operating cash flow of $120M, total capex of $100M, depreciation of $50M, and estimates that $60M of the capex is maintenance. Maintenance free cash flow is $120 − $60 = $60M. Growth capex is $40M.

If the company's growth capex earns a 12% return and its WACC is 10%, the growth spending creates value. If the return is 6%, it destroys value. The analyst should compare the growth capex with the incremental profit or cash flow it produces, not with the total capital budget.

Depreciation is not a reliable proxy for maintenance capex. A company can depreciate assets over long lives while spending more to keep them running, or it can defer spending and let the asset base deteriorate. The analyst should read the capital-expenditure note, the depreciation policy, and management's discussion of maintenance spending.

## Research discipline

1. **Estimate maintenance capex** from management disclosure, asset age, and industry norms.
2. **Compare maintenance capex with depreciation** over several years.
3. **Test the return on growth capex** and compare it with WACC.
4. **Stress a deferred-maintenance scenario**: lower near-term capex followed by a catch-up year.
""",
        r"\text{FCF}_{\text{maintenance}}=\text{CFO}-\text{Maintenance capex};\quad \text{Growth capex}=\text{Total capex}-\text{Maintenance capex}",
        'cfo = 120\ntotal_capex = 100\nmaintenance_capex = 60\ndepreciation = 50\nprint("Maintenance FCF:", cfo - maintenance_capex)\nprint("Growth capex:", total_capex - maintenance_capex)\nprint("Capex / depreciation:", total_capex/depreciation)',
        "A company reports CFO of $180M, total capex of $140M, depreciation of $70M, and maintenance capex of $85M. Calculate maintenance free cash flow and growth capex. Then explain why using depreciation as a proxy for maintenance capex would overstate cash available to owners.",
        "Maintenance FCF is 180 − 85 = $95M. Growth capex is 140 − 85 = $55M. Depreciation is $70M, below maintenance capex of $85M. Using depreciation as a proxy would treat $180 − $70 = $110M as available, overstating cash by $15M. The difference is the extra spending required to keep the asset base in place.",
        [
            q(
                "Maintenance capex is the spending required to:",
                ["Grow the business", "Keep existing assets operating", "Pay dividends"],
                1,
                "Maintenance capex sustains current capacity; growth capex adds capacity.",
            ),
            q(
                "CFO is 100 and maintenance capex is 40. Maintenance FCF is:",
                ["40", "60", "140"],
                1,
                "Maintenance FCF is 100 − 40 = 60.",
            ),
            q(
                "If depreciation is 30 and maintenance capex is 45, using depreciation as a proxy:",
                ["Overstates free cash flow by 15", "Understates free cash flow by 15", "Has no effect"],
                0,
                "The proxy ignores 15 of required maintenance spending, overstating cash.",
            ),
        ],
    )

    add(
        "20.6",
        "II",
        "Balance-sheet resilience in a downturn",
        "Stress-test EBITDA, liquidity, covenants, and capital spending to see whether a cyclical company can survive a trough.",
        r"""
## The analytical question

A cyclical company's survival depends on its balance sheet as well as its cost position. The analyst should build a downside case in which EBITDA falls, working capital consumes cash, and capital spending cannot be cut quickly. The key outputs are liquidity, covenant headroom, and the actions management can take.

$$\text{Stressed leverage}=\frac{\text{Debt}}{\text{Stressed EBITDA}}$$

$$\text{Liquidity runway}=\frac{\text{Cash}+\text{Available facilities}}{\text{Monthly cash burn}}$$

A company with high fixed costs and high leverage may need to cut capital spending, suspend the dividend, or raise equity in a downturn. The analyst should identify which levers are available and how quickly they can be pulled.

## A worked example

A mining company has debt of $400M, EBITDA of $200M, interest of $30M, maintenance capex of $50M, and liquidity of $80M. Its leverage is 2.0×. In a trough, EBITDA falls to $120M. Stressed leverage is 400/120 = 3.33×. If the covenant is 3.5×, the company is close to a breach.

Cash flow in the trough is EBITDA $120M − interest $30M − maintenance capex $50M = $40M before working capital and tax. If working capital consumes $60M as inventory builds and receivables slow, cash flow is −$20M. Liquidity of $80M gives a runway of four months at a $20M monthly burn.

Management can cut growth capex, suspend the dividend, or draw on facilities. The analyst should model those actions and the resulting covenant trajectory. A company that can cut spending quickly is more resilient than one with inflexible contracts.

## Research discipline

1. **Stress EBITDA, working capital, and capex together**, not separately.
2. **Check covenant definitions and step-downs** through the cycle.
3. **Identify the available levers** and the time needed to use them.
4. **Model a second year of downturn**, not only a single bad quarter.
""",
        r"\text{Stressed leverage}=\frac{\text{Debt}}{\text{EBITDA}_{\text{stress}}};\quad \text{Runway}=\frac{\text{Liquidity}}{\text{Monthly burn}}",
        'debt = 400\nebitda = 200\ninterest = 30\nmaintenance_capex = 50\nliquidity = 80\nprint("Base leverage:", debt/ebitda)\nstress = 120\nprint("Stressed leverage:", round(debt/stress, 2))\nprint("Trough cash flow:", stress - interest - maintenance_capex)\nprint("Runway with 20 monthly burn:", round(liquidity/20, 1))',
        "A company has debt of $300M, EBITDA of $150M, interest of $24M, maintenance capex of $40M, and liquidity of $60M. In a trough, EBITDA falls to $90M and working capital consumes $45M. Calculate base and stressed leverage, trough cash flow, and the liquidity runway if the resulting monthly burn is $15M.",
        "Base leverage is 300/150 = 2.0×; stressed leverage is 300/90 = 3.33×. Trough cash flow before working capital is 90 − 24 − 40 = $26M; after $45M of working-capital consumption, it is −$19M. At the stated $15M monthly burn, liquidity of $60M gives a four-month runway. The company needs to cut capex or raise funding before the trough deepens.",
        [
            q(
                "Debt is 240 and stressed EBITDA is 80. Stressed leverage is:",
                ["2×", "3×", "4×"],
                1,
                "Stressed leverage is 240 / 80 = 3×.",
            ),
            q(
                "A cyclical company's resilience is improved by:",
                ["High fixed costs and no liquidity", "Flexible capex and available liquidity", "A large maturity wall"],
                1,
                "The ability to cut spending and access cash helps the company survive a trough.",
            ),
            q(
                "Liquidity is 90 and monthly burn is 30. Runway is:",
                ["2 months", "3 months", "30 months"],
                1,
                "The runway is 90 / 30 = 3 months.",
            ),
        ],
    )

    checkpoints = [
        (
            "Checkpoint · cyclical earnings and cash",
            [
                (
                    "20.1",
                    q(
                        "Margins of 3%, 5%, 7%, 9%, and 11% have an average of:",
                        ["6%", "7%", "9%"],
                        1,
                        "The sum is 35%; divided by five, the average is 7%.",
                    ),
                ),
                (
                    "20.2",
                    q(
                        "A producer hedges 40% at $20 and spot is $25. Realized price is:",
                        ["$20", "$23", "$25"],
                        1,
                        "0.40(20) + 0.60(25) = 8 + 15 = $23.",
                    ),
                ),
                (
                    "20.3",
                    q(
                        "Contribution is 50 and EBIT is 10. DOL is:",
                        ["2×", "5×", "10×"],
                        1,
                        "DOL is 50 / 10 = 5×, so profit is highly sensitive to volume.",
                    ),
                ),
                (
                    "20.4",
                    q(
                        "Current NWC is 80 and new NWC is 104. The incremental cash need is:",
                        ["24", "80", "104"],
                        0,
                        "The incremental working capital is 104 − 80 = 24.",
                    ),
                ),
            ],
        ),
    ]

    return finish(
        {
            "id": "cyclical-industrials",
            "number": 20,
            "title": "Cyclicals, commodities & industrials",
            "description": "Normalize through-cycle earnings, model commodity and operating leverage, and stress the balance sheet before a downturn.",
            "source": "Advanced security analysis · original cyclical cases with official data anchors",
            "level": "Advanced",
            "icon": "book",
            "modules": modules,
            "prerequisites": "Security Analysis or equivalent knowledge of margins, fixed costs, and working capital.",
            "outcomes": [
                "Normalize cyclical revenue and margins across a full cycle.",
                "Model commodity price exposure and hedge effects.",
                "Quantify operating leverage and capacity constraints.",
                "Stress liquidity, covenants, and capex in a downturn.",
            ],
            "readingGuide": "Read the company's capacity, cost, hedging, and working-capital disclosures beside each lesson. The worked figures are teaching numbers.",
            "references": [
                {"title": "BPS · Indonesia's GDP growth release", "url": "https://www.bps.go.id/id/pressrelease/2025/02/05/2408/economic-growth.html"},
                {"title": "CME Group · Negative price testing advisory", "url": "https://www.cmegroup.com/notices/clearing/2020/04/Chadv20-160.html"},
            ],
            "parts": [
                {"id": "I", "title": "Cycles, commodities, and leverage", "description": "Mid-cycle earnings, hedging, and operating leverage"},
                {"id": "II", "title": "Cash and resilience", "description": "Working capital, maintenance capex, and downturn stress"},
            ],
            "studyType": "applied",
        },
        checkpoints,
    )
