"""Technology, platforms, and intangible-heavy analysis course (21.x)."""

from advanced_security_common import finish, make_add, q

READING = (
    "Advanced security analysis · technology and intangibles. Read the company's R&D, software, "
    "customer-cohort, and related-party disclosures beside this lesson. The worked figures are "
    "teaching numbers; the cited sources supply the real-world context."
)


def build_tech_intangibles():
    modules = []
    add = make_add(modules, READING)

    add(
        "21.1",
        "I",
        "Capitalizing R&D and software",
        "Reconstruct an intangible-adjusted profit and capital base before comparing a technology company with peers.",
        r"""
## The analytical question

Accounting rules often expense research and development, while acquired intangibles are capitalized. Two companies with similar economics can therefore report very different profits and capital bases. The analyst should **capitalize R&D** analytically, amortize it over a reasonable life, and compare the adjusted profit and invested capital.

$$\text{Adjusted EBIT}=\text{Reported EBIT}-\text{R\&D expense}+\text{Amortization of capitalized R\&D}$$

$$\text{Adjusted capital}=\text{Reported capital}+\text{Unamortized R\&D pool}$$

The adjustment is not a claim that R&D always creates a durable asset. It is a way to compare companies that invest in intangibles through the income statement rather than through acquisitions.

## A worked example

A software company reports EBIT of $150M and R&D expense of $100M. The analyst capitalizes R&D over four years. The current-year amortization of the new layer is $25M. Adjusted EBIT is $150 − $100 + $25 = $75M.

If the company reports invested capital of $400M and the unamortized R&D pool is $150M, adjusted capital is $550M. Reported return on capital is 37.5%; adjusted return is 75/550 = 13.6%. The adjusted figure is a more comparable measure of the return on all the capital, including the intangible investment.

The analyst should check whether the R&D is maintenance or growth. Maintenance R&D keeps existing products competitive; growth R&D creates new products. A company that expenses both may look less profitable than an acquirer that capitalizes a similar asset. The adjustment should use a consistent amortization period and be disclosed.

## Research discipline

1. **Read the R&D and software notes** for amounts, capitalization policy, and useful lives.
2. **Use a consistent amortization period** and test sensitivity to the choice.
3. **Separate maintenance from growth spending** where disclosure allows.
4. **Compare adjusted returns across peers**, not just reported margins.
""",
        r"\text{Adj. EBIT}=\text{EBIT}-\text{R\&D}+\text{Amortization};\quad \text{Adj. capital}=\text{Capital}+\text{Unamortized R\&D}",
        'ebit = 150\nrd = 100\namortization = 25\ncapital = 400\nunamortized = 150\nadjusted_ebit = ebit - rd + amortization\nadjusted_capital = capital + unamortized\nprint("Adjusted EBIT:", adjusted_ebit)\nprint("Reported return (%):", round(ebit/capital*100, 1))\nprint("Adjusted return (%):", round(adjusted_ebit/adjusted_capital*100, 1))',
        "A company reports EBIT of $200M, R&D of $120M, and amortization of the new R&D layer of $30M. Reported capital is $500M and the unamortized R&D pool is $180M. Calculate adjusted EBIT, adjusted capital, and reported versus adjusted return on capital.",
        "Adjusted EBIT is 200 − 120 + 30 = $110M. Adjusted capital is 500 + 180 = $680M. Reported return is 200/500 = 40.0%; adjusted return is 110/680 = 16.2%. The adjusted return is lower because the full intangible investment is included in the capital base. The analyst should disclose the amortization period and test a shorter or longer life.",
        [
            q(
                "Reported EBIT is 100, R&D is 40, and new amortization is 10. Adjusted EBIT is:",
                ["70", "100", "140"],
                0,
                "Adjusted EBIT is 100 − 40 + 10 = 70.",
            ),
            q(
                "Analytically capitalizing R&D is useful because:",
                ["It makes every company profitable", "It improves comparability of intangible investment", "It eliminates the need for cash flow"],
                1,
                "The adjustment puts expensed and acquired intangibles on a more comparable footing.",
            ),
            q(
                "Reported capital is 300 and the unamortized R&D pool is 100. Adjusted capital is:",
                ["200", "300", "400"],
                2,
                "Adjusted capital is 300 + 100 = 400.",
            ),
        ],
    )

    add(
        "21.2",
        "I",
        "Platform unit economics",
        "Calculate customer acquisition cost, lifetime value, payback, and churn, and test whether growth creates or destroys value.",
        r"""
## The analytical question

A platform business can grow quickly while losing money on every customer. The analyst should model the **unit economics**: the cost to acquire a customer, the revenue and gross profit that customer generates, and the rate at which the customer leaves.

$$\text{LTV}=\frac{\text{ARPU}\times\text{Gross margin}}{\text{Churn rate}}$$

$$\text{CAC payback}=\frac{\text{CAC}}{\text{ARPU}\times\text{Gross margin}}$$

$$\text{LTV/CAC}=\frac{\text{LTV}}{\text{CAC}}$$

A high LTV/CAC ratio suggests that growth is economically attractive. A low ratio suggests that the company is buying revenue rather than building value. The ratios depend on churn and gross margin, which are estimates; the analyst should stress them.

## A worked example

A subscription platform has annual revenue per user (ARPU) of $60, a gross margin of 80%, annual churn of 20%, and a customer acquisition cost of $100. LTV is 60 × 0.80 / 0.20 = $240. CAC payback is 100 / (60 × 0.80) = 2.08 years. LTV/CAC is 2.4×.

The economics look acceptable but not exceptional. If churn rises to 30%, LTV falls to 60 × 0.80 / 0.30 = $160, and LTV/CAC falls to 1.6×. If gross margin falls to 60%, LTV falls to $180 and the ratio to 1.8×. The analyst should test both. A company with high churn and low gross margin can grow revenue while destroying value.

The analyst should also distinguish gross customer additions from net additions. A company can report strong gross adds while churn consumes most of them. Cohort analysis shows whether newer customers retain as well as older ones.

## Research discipline

1. **Use cohort data**, not just aggregate revenue, to estimate churn and retention.
2. **Include all acquisition costs**, including sales commissions and marketing.
3. **Stress churn and gross margin**, and show the effect on LTV/CAC.
4. **Compare payback with the company's funding cost** and cash position.
""",
        r"\text{LTV}=\frac{\text{ARPU}\times\text{GM}}{\text{Churn}};\quad \text{Payback}=\frac{\text{CAC}}{\text{ARPU}\times\text{GM}}",
        'arpu = 60\ngm = 0.80\nchurn = 0.20\ncac = 100\nltv = arpu*gm/churn\nprint("LTV:", round(ltv, 1))\nprint("CAC payback (years):", round(cac/(arpu*gm), 2))\nprint("LTV/CAC:", round(ltv/cac, 2))\nprint("LTV at 30% churn:", round(arpu*gm/0.30, 1))',
        "A platform has ARPU of $120, gross margin of 75%, annual churn of 15%, and CAC of $180. Calculate LTV, CAC payback, and LTV/CAC. Then recalculate LTV and the ratio if churn rises to 25%.",
        "LTV is 120 × 0.75 / 0.15 = $600. Payback is 180 / (120 × 0.75) = 2.0 years. LTV/CAC is 600/180 = 3.33×. At 25% churn, LTV is 120 × 0.75 / 0.25 = $360, and LTV/CAC is 2.0×. The growth is still value-creating under the assumptions, but the margin of safety is thinner.",
        [
            q(
                "ARPU is 50, gross margin 80%, churn 20%. LTV is:",
                ["100", "200", "250"],
                1,
                "50 × 0.80 / 0.20 = 200.",
            ),
            q(
                "CAC payback measures:",
                ["How long it takes gross profit to recover acquisition cost", "The total lifetime revenue", "The churn rate"],
                0,
                "Payback is CAC divided by periodic gross profit per customer.",
            ),
            q(
                "CAC is 120 and annual gross profit per customer is 60. Payback is:",
                ["0.5 years", "2 years", "60 years"],
                1,
                "CAC payback is 120 / 60 = 2 years.",
            ),
        ],
    )

    add(
        "21.3",
        "I",
        "Network effects, churn, and cohort analysis",
        "Test whether a platform's growth is reinforced by network effects or merely purchased through marketing.",
        r"""
## The analytical question

A network effect exists when each additional user makes the platform more valuable to other users. The evidence is not a large user count; it is improved retention, lower acquisition costs, or higher engagement as the network grows. The analyst should compare cohorts over time.

A cohort table shows the revenue or users from each acquisition cohort in subsequent periods. **Net revenue retention** measures how much revenue a cohort generates after a year, including expansion and churn:

$$\text{NRR}=\frac{\text{Revenue from cohort in year }t}{\text{Revenue from cohort in year }0}$$

A ratio above 100% means existing customers are spending more; below 100% means churn and downgrades exceed expansion. The analyst should separate gross retention from expansion.

## A worked example

A platform acquired 1,000 customers in year 0 at an average revenue of $100 each, for $100,000. In year 1, 800 customers remain, each paying $110, for $88,000. Gross retention is 80%, but net revenue retention is 88,000/100,000 = 88%.

In year 2, 650 of the original customers remain, each paying $120, for $78,000. The two-year NRR is 78%. The platform is losing customers faster than it expands the remaining ones. If the company reports strong total revenue growth, it may be adding new cohorts that mask the deterioration in older ones.

A genuine network effect would tend to improve retention or lower CAC over time. The analyst should compare CAC by cohort, engagement by cohort, and the retention curve. A flattening retention curve suggests a durable base; a curve that keeps falling suggests the product is not sticky.

## Research discipline

1. **Build cohort tables** from disclosed data, and separate gross retention from expansion.
2. **Compare CAC and retention across cohorts**, not just aggregate averages.
3. **Test the network-effect claim** with evidence: engagement, match rates, or liquidity.
4. **Stress churn** and show the effect on revenue and valuation.
""",
        r"\text{NRR}=\frac{\text{Cohort revenue}_t}{\text{Cohort revenue}_0};\quad \text{Gross retention}=\frac{\text{Customers}_t}{\text{Customers}_0}",
        'customers0 = 1000\narpu0 = 100\ncustomers1 = 800\narpu1 = 110\ncustomers2 = 650\narpu2 = 120\nrev0 = customers0*arpu0\nrev1 = customers1*arpu1\nrev2 = customers2*arpu2\nprint("Gross retention year 1 (%):", round(customers1/customers0*100, 1))\nprint("NRR year 1 (%):", round(rev1/rev0*100, 1))\nprint("NRR year 2 (%):", round(rev2/rev0*100, 1))',
        "A cohort starts with 500 customers paying $200 each. After one year, 400 remain and pay $220. After two years, 300 remain and pay $230. Calculate gross retention and net revenue retention for each year. What does the pattern suggest about the strength of the network effect?",
        "Initial revenue is $100,000. Year 1 revenue is 400 × 220 = $88,000, so gross retention is 80% and NRR is 88%. Year 2 revenue is 300 × 230 = $69,000, so NRR is 69%. The pattern suggests that expansion is not offsetting churn; the network effect may be weak or the customer base may be deteriorating. The analyst should compare CAC and engagement by cohort before concluding.",
        [
            q(
                "A cohort's revenue falls from 100 to 90 while customer count falls from 50 to 40. Gross retention is:",
                ["80%", "90%", "100%"],
                0,
                "Gross retention is 40 / 50 = 80%.",
            ),
            q(
                "Net revenue retention above 100% means:",
                ["Existing customers are spending more than churn removes", "The company has no churn", "Revenue is falling"],
                0,
                "Expansion and cross-sell exceed the revenue lost from churn and downgrades.",
            ),
            q(
                "A cohort starts at 200 customers and 120 remain. Gross retention is:",
                ["40%", "60%", "80%"],
                1,
                "Gross retention is 120 / 200 = 60%.",
            ),
        ],
    )

    add(
        "21.4",
        "II",
        "Intangible-heavy comparables and multiples",
        "Adjust multiples for R&D, stock compensation, and growth so that technology peers are compared on a consistent basis.",
        r"""
## The analytical question

A simple EV/EBITDA multiple can mislead for technology companies. EBITDA excludes R&D, which is a real operating cost for a software business, and it ignores stock-based compensation, which dilutes owners. A company that expenses R&D and pays employees in stock may look cheaper or more expensive than a peer with different accounting.

The analyst should compare **EV/revenue**, **EV/gross profit**, and **EV/adjusted EBIT**, and disclose the adjustments. A useful cross-check is:

$$\text{EV/Revenue}=\frac{\text{EV}}{\text{Revenue}}$$

$$\text{EV/Gross profit}=\frac{\text{EV}}{\text{Gross profit}}$$

$$\text{EV/Adjusted EBIT}=\frac{\text{EV}}{\text{EBIT after R\&D and SBC}}$$

The multiples are only comparable if the numerator and denominator describe the same capital structure and the same cost basis.

## A worked example

Company A trades at an EV of $1,000M with revenue of $200M, gross profit of $160M, EBITDA of $50M, R&D of $40M, and stock-based compensation of $20M. EV/revenue is 5.0×; EV/gross profit is 6.25×; EV/EBITDA is 20×. Adjusted EBIT after R&D and SBC is $50 − $40 − $20 = −$10M, so an EV/adjusted EBIT multiple is not meaningful.

Company B trades at an EV of $800M with revenue of $200M, gross profit of $140M, EBITDA of $60M, R&D of $20M, and SBC of $10M. EV/revenue is 4.0×; EV/gross profit is 5.71×; adjusted EBIT is $30M, so EV/adjusted EBIT is 26.7×.

Company B looks cheaper on revenue and gross profit but more expensive on adjusted EBIT because it has a lower R&D burden and positive profit. The analyst must decide which multiple matches the companies' economics and stage of growth.

## Research discipline

1. **Use the same adjustments for every peer**, including R&D and SBC.
2. **Treat negative adjusted EBIT as not meaningful**, not as a very high multiple.
3. **Compare growth, margins, and capital intensity** alongside the multiple.
4. **Disclose the multiple definitions** and the period used.
""",
        r"\text{EV/Revenue}=\frac{\text{EV}}{R};\quad \text{EV/GP}=\frac{\text{EV}}{GP};\quad \text{Adj. EBIT}=\text{EBITDA}-R\&D-SBC",
        'ev_a = 1000\nrev_a = 200\ngp_a = 160\nebitda_a = 50\nrd_a = 40\nsbc_a = 20\nprint("A EV/revenue:", ev_a/rev_a)\nprint("A EV/gross profit:", round(ev_a/gp_a, 2))\nprint("A adjusted EBIT:", ebitda_a - rd_a - sbc_a)\nev_b = 800\nrev_b = 200\ngp_b = 140\nebitda_b = 60\nrd_b = 20\nsbc_b = 10\nprint("B EV/revenue:", ev_b/rev_b)\nprint("B EV/gross profit:", round(ev_b/gp_b, 2))\nprint("B EV/adjusted EBIT:", round(ev_b/(ebitda_b - rd_b - sbc_b), 2))',
        "Company A has EV of $1,200M, revenue of $300M, gross profit of $240M, EBITDA of $90M, R&D of $50M, and SBC of $20M. Company B has EV of $900M, revenue of $300M, gross profit of $210M, EBITDA of $100M, R&D of $25M, and SBC of $15M. Calculate EV/revenue, EV/gross profit, and adjusted EBIT for each. Which comparison is most informative?",
        "Company A: EV/revenue 4.0×, EV/gross profit 5.0×, adjusted EBIT 90 − 50 − 20 = $20M. Company B: EV/revenue 3.0×, EV/gross profit 4.29×, adjusted EBIT 100 − 25 − 15 = $60M. Company B is cheaper on revenue and gross profit but has much higher adjusted EBIT, so the EV/adjusted EBIT comparison (45× for A vs 15× for B) is the most informative if the businesses are at similar maturity. The analyst should also compare growth and margins.",
        [
            q(
                "EV is 600 and revenue is 200. EV/revenue is:",
                ["2×", "3×", "6×"],
                1,
                "EV/revenue is 600 / 200 = 3×.",
            ),
            q(
                "Adjusted EBIT in this lesson subtracts:",
                ["R&D and stock-based compensation", "Only interest", "Dividends"],
                0,
                "The adjustment treats R&D and SBC as real operating costs.",
            ),
            q(
                "A company with negative adjusted EBIT should have its EV/adjusted EBIT multiple:",
                ["Reported as a very high number", "Treated as not meaningful", "Set to zero"],
                1,
                "A negative denominator makes the multiple uninterpretable.",
            ),
        ],
    )

    add(
        "21.5",
        "II",
        "Governance, disclosure, and hype risk",
        "Separate verifiable operating evidence from promotional claims in fast-growing technology companies.",
        r"""
## The analytical question

Technology companies often operate in new markets where traditional metrics are scarce and narratives are powerful. The analyst should distinguish **verifiable evidence** (audited revenue, customer contracts, retention data, unit economics) from **promotional claims** (addressable market, technology leadership, partnerships). A claim that cannot be tested is not evidence.

A simple evidence score can be built from five questions:

1. Is the revenue audited and reconciled to cash?
2. Are customer and cohort data disclosed?
3. Are partnerships and backlog supported by contracts?
4. Does the board provide independent oversight?
5. Are related-party transactions disclosed and at arm's length?

Each question can be scored 0–5, and the analyst can weight the categories according to the company's stage. The score is a structured way to raise the burden of proof before paying a high multiple.

## A worked example

A private technology company claims a $50 billion addressable market, a strategic partnership with a large manufacturer, and a proprietary technology that is "years ahead." It discloses revenue of $40M, but no audited financials, no customer concentration, and no contract for the partnership. Two of five directors are independent, and the founder controls 70% of the votes.

The analyst scores financial evidence 2, customer evidence 1, partnership evidence 1, board independence 2, and related-party disclosure 2. With equal weights, the score is 1.6 out of 5. The narrative may be true, but the evidence does not support paying a high multiple. The analyst should request the audit, the partnership agreement, customer references, and the related-party ledger.

A high score does not guarantee a good investment, and a low score does not prove fraud. The score changes the price the analyst is willing to pay and the size of the position.

## Research discipline

1. **Ask for primary documents**, not summaries: audited accounts, contracts, and customer data.
2. **Test the partnership claim** by checking whether the counterparty has disclosed it and whether it has economic substance.
3. **Read the board and ownership structure** and identify related-party paths.
4. **Separate the market-size story from the company's ability to capture it.**
""",
        r"\text{Evidence score}=\sum_i w_i s_i;\quad 0\le s_i\le5",
        'financial = 2\ncustomer = 1\npartnership = 1\nboard = 2\nrelated = 2\nscore = (financial + customer + partnership + board + related)/5\nprint("Evidence score:", round(score, 2))\nprint("Weakest area score:", min(financial, customer, partnership, board, related))',
        "A company scores 3 on financial evidence, 2 on customer data, 1 on partnership documentation, 3 on board independence, and 2 on related-party disclosure. Calculate the equal-weighted evidence score. Then state two documents you would request before relying on the growth story.",
        "The score is (3 + 2 + 1 + 3 + 2)/5 = 2.2. Request the audited financial statements and the partnership contract, plus customer references and the related-party transaction ledger. The analyst should also check whether the counterparty has publicly disclosed the partnership and whether it has minimum-volume or payment obligations.",
        [
            q(
                "A large addressable-market estimate is best treated as:",
                ["Audited evidence", "A promotional claim that requires a capture plan", "A guarantee of revenue"],
                1,
                "Market size does not establish that the company can capture it profitably.",
            ),
            q(
                "Which document most directly tests a partnership claim?",
                ["A press release", "The executed agreement with obligations", "A conference slide"],
                1,
                "An executed contract with obligations is stronger evidence than a press release.",
            ),
            q(
                "An evidence score of 1.8 out of 5 should lead to:",
                ["A larger position", "More diligence or a lower price", "Ignoring the company"],
                1,
                "A low score raises the burden of proof and should affect price and position size.",
            ),
        ],
    )

    add(
        "21.6",
        "II",
        "Valuing growth with discipline",
        "Use growth duration, reinvestment, and reverse DCF to test whether a high multiple is justified.",
        r"""
## The analytical question

A high-growth company can be worth many times current revenue, but only if it sustains growth for a long period at attractive returns. The analyst should model **growth duration**, the period during which returns on new investment exceed the cost of capital, and connect it to reinvestment.

$$\text{Value}=\text{Invested capital}+\sum_{t=1}^{T}\frac{(\text{ROIC}_t-\text{WACC})\times\text{Invested capital}_t}{(1+\text{WACC})^t}+\text{Terminal value}$$

A simpler test is a reverse DCF: solve for the growth or margin implied by the current price, then ask whether the company can deliver it. A high multiple is not automatically wrong; it is a claim about the future that must be tested.

## A worked example

A software company trades at an EV of $2,000M with revenue of $200M, an EV/revenue multiple of 10×. The analyst assumes a 10% WACC, a 25% steady-state EBIT margin, and a 25% tax rate, giving NOPAT of 18.75% of revenue at maturity. If the company reaches $1,000M of revenue in ten years and then grows at 3% forever, the terminal value alone is large; the current price implies that the company must sustain high growth and margins for a decade.

The analyst should build a explicit ten-year forecast with revenue growth, margin expansion, reinvestment, and share dilution. The reverse DCF can then show which assumption is doing the most work. If the price requires 30% annual growth for ten years, the analyst should compare that with the company's current growth, market size, and competitive position.

A high-growth company can be a good investment if the growth is durable and the price is reasonable. The danger is paying for a narrative that assumes perfection. A margin of safety can come from a lower price or from a business that is more durable than the market expects.

## Research discipline

1. **Model growth and margins explicitly** for each year, not as a single terminal assumption.
2. **Include reinvestment and dilution**; growth is not free.
3. **Use reverse DCF to identify the implied expectation** and compare it with evidence.
4. **Stress the growth duration** and show the value if growth ends earlier.
""",
        r"\text{Value}=\text{IC}+\sum_t\frac{(\text{ROIC}_t-\text{WACC})\text{IC}_t}{(1+\text{WACC})^t}+\text{TV}",
        'ev = 2000\nrevenue = 200\nwacc = 0.10\nprint("EV/revenue:", ev/revenue)\nmature_nopat_margin = 0.25*(1 - 0.25)\nprint("Mature NOPAT margin (%):", round(mature_nopat_margin*100, 1))\nprint("Implied mature NOPAT on 1000 revenue:", 1000*mature_nopat_margin)',
        "A company trades at an EV of $3,000M with revenue of $250M. It expects to reach $1,000M of revenue in eight years with a 20% EBIT margin and a 25% tax rate. Calculate the current EV/revenue and the mature NOPAT at $1,000M of revenue. Then explain why the current price depends on more than the mature NOPAT.",
        "EV/revenue is 3,000/250 = 12×. Mature NOPAT is $1,000M × 20% × (1 − 0.25) = $150M. The current price depends on the path to that NOPAT, the reinvestment required, the discount rate, and the terminal growth after year eight. A high mature NOPAT alone does not justify the price; the company must survive the growth phase and earn attractive returns on the capital it invests.",
        [
            q(
                "EV is 1,800 and revenue is 300. EV/revenue is:",
                ["3×", "6×", "18×"],
                1,
                "EV/revenue is 1,800 / 300 = 6×.",
            ),
            q(
                "A high growth multiple is justified only if:",
                ["Growth is durable and returns exceed the cost of capital", "Revenue grows in one year", "The company has a popular product"],
                0,
                "Value depends on the duration and profitability of growth, not on popularity alone.",
            ),
            q(
                "Mature revenue is 800, EBIT margin 20%, tax 25%. Mature NOPAT is:",
                ["120", "160", "200"],
                0,
                "800 × 0.20 × 0.75 = 120.",
            ),
        ],
    )

    checkpoints = [
        (
            "Checkpoint · intangibles, unit economics, and growth",
            [
                (
                    "21.1",
                    q(
                        "EBIT is 120, R&D is 50, and new amortization is 12. Adjusted EBIT is:",
                        ["82", "120", "182"],
                        0,
                        "Adjusted EBIT is 120 − 50 + 12 = 82.",
                    ),
                ),
                (
                    "21.2",
                    q(
                        "ARPU is 80, gross margin 75%, churn 20%. LTV is:",
                        ["300", "400", "600"],
                        0,
                        "80 × 0.75 / 0.20 = 300.",
                    ),
                ),
                (
                    "21.3",
                    q(
                        "A cohort starts at 100 customers and 75 remain. Gross retention is:",
                        ["25%", "75%", "100%"],
                        1,
                        "Gross retention is 75 / 100 = 75%.",
                    ),
                ),
                (
                    "21.4",
                    q(
                        "EV is 900 and gross profit is 180. EV/gross profit is:",
                        ["3×", "5×", "9×"],
                        1,
                        "EV/gross profit is 900 / 180 = 5×.",
                    ),
                ),
            ],
        ),
    ]

    return finish(
        {
            "id": "tech-intangibles",
            "number": 21,
            "title": "Technology, platforms & intangibles",
            "description": "Adjust R&D and software, test platform unit economics and cohorts, compare intangible-heavy peers, and value growth with discipline.",
            "source": "Advanced security analysis · original technology cases with SEC enforcement anchors",
            "level": "Advanced",
            "icon": "book",
            "modules": modules,
            "prerequisites": "Security Analysis or equivalent knowledge of margins, capital, and valuation. Familiarity with subscription businesses helps.",
            "outcomes": [
                "Reconstruct adjusted profit and capital for R&D-heavy companies.",
                "Measure CAC, LTV, payback, and cohort retention.",
                "Compare intangible-heavy peers on consistent multiples.",
                "Test a high-growth valuation with a reverse DCF and explicit path.",
            ],
            "readingGuide": "Read the R&D, software, cohort, and related-party disclosures beside each lesson. The worked figures are teaching numbers; the cited sources supply the real-world context.",
            "references": [
                {"title": "U.S. SEC · EDGAR company filings", "url": "https://www.sec.gov/edgar/searchedgar/companysearch"},
                {"title": "U.S. SEC · Enforcement actions", "url": "https://www.sec.gov/enforcement-litigation"},
            ],
            "parts": [
                {"id": "I", "title": "Intangibles and unit economics", "description": "R&D, software, LTV/CAC, and cohort retention"},
                {"id": "II", "title": "Comparables, governance, and growth", "description": "Adjusted multiples, evidence scores, and growth duration"},
            ],
            "studyType": "applied",
        },
        checkpoints,
    )
