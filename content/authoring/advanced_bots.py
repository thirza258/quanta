"""Advanced algorithmic-trading units added without changing legacy lesson identities."""

from applied_courses import study

ORDER = (
    "Alpaca · Order instructions and lifecycle",
    "https://docs.alpaca.markets/us/docs/working-with-orders",
)
PAPER = (
    "Alpaca · Paper execution assumptions",
    "https://docs.alpaca.markets/us/docs/paper-trading",
)
SPLIT = (
    "scikit-learn contributors · TimeSeriesSplit",
    "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html",
)
LEAK = (
    "scikit-learn contributors · Model evaluation pitfalls",
    "https://scikit-learn.org/stable/common_pitfalls.html",
)
COINT = (
    "statsmodels contributors · Cointegration testing",
    "https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.coint.html",
)
MULTI = (
    "statsmodels contributors · Multiple-testing corrections",
    "https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html",
)
AGENT = (
    "Anthropic · Building effective agents",
    "https://www.anthropic.com/engineering/building-effective-agents",
)
LAB = "/course-assets/research/quant_research_lab.py"


def expand_stock_bots(track):
    additions = []

    def add(*args):
        additions.append(study(*args))

    add(
        "5.33",
        8,
        "Corporate actions, sessions, and universe membership",
        "Make splits, dividends, delistings, and trading calendars explicit in signal and account histories.",
        "A production-shaped dataset needs separate concepts for investment returns, executable prices, and account events. Split-adjusted prices help compare historical levels, but orders execute in the actual share and price units at that time. A dividend can enter a total-return calculation without being an immediate cash receipt under a particular settlement convention.\n\nUniverse membership must be dated. Selecting today's liquid survivors for an earlier test can exclude bankrupt or delisted companies. Eligibility also depends on session, halts, available history, supported order types, and the intended jurisdiction or venue. The course project uses supplied session flags and synthetic fixtures; it does not implement exchange calendars or corporate-action feeds.",
        "A two-for-one split changes a holding of 10 shares priced at 100 into 20 shares priced at 50, preserving value 1,000 before other market movement. A pending limit of 98 needs a broker-specific adjustment or cancellation policy; assuming it stays numerically unchanged can create unintended exposure.\n\nIf a dividend is 1 per share and price changes from 100 to 99, the simple total-return calculation is (99+1)/100−1=0 before taxes and reinvestment assumptions. A raw price-only return reports −1% and answers a different question.",
        "Define fixtures for a split, a cash dividend, a delisting, a newly eligible instrument, a holiday, and a halt. Reconcile holdings, order units, and data adjustments at the effective time. Retain raw and adjusted fields with source versions. Do not infer a causal trading opportunity from an adjustment artifact. A strategy release should fail its data contract if corporate-action handling or historical membership is unknown.",
        r"q_{after}=s q_{before},\quad P_{after}=P_{before}/s",
        'print("Split shares:", 10 * 2)\nprint("Split position value:", 10 * 2 * (100 / 2))\nprint("Dividend-inclusive return:", (99 + 1) / 100 - 1)',
        "Write a split fixture for 12 shares at 90 under a three-for-one split. Specify what happens to a pending order and which data fields change.",
        "Holdings become 36 shares and mechanically adjusted price 30, preserving 1,080 value. Pending orders require the documented adapter policy; reconcile effective timestamps, quantities, and limits rather than guessing.",
        [
            (
                "A two-for-one split mechanically doubles position value:",
                ["No", "Yes", "Only for limit orders"],
                0,
                "Share count and per-share price change inversely before other movement.",
            ),
            (
                "Today's surviving names automatically define an unbiased historical universe:",
                ["Yes", "No", "Only for large stocks"],
                1,
                "Historical eligibility includes failures and membership changes.",
            ),
            (
                "A three-for-one split of 7 shares at 60 produces:",
                ["7 shares at 20", "21 shares at 60", "21 shares at 20"],
                2,
                "Both share and price units must adjust consistently.",
            ),
            (
                "Mixing split-adjusted signals with unadjusted share quantities can:",
                [
                    "Create incorrect orders or exposure",
                    "Guarantee a neutral result",
                    "Replace a corporate-action policy",
                ],
                0,
                "Executable units must be reconciled with analytical adjustments.",
            ),
        ],
        [ORDER, PAPER],
    )

    add(
        "5.34",
        8,
        "Price-time priority and order-book replay",
        "Implement a small limit-book matcher and identify the information OHLC bars cannot supply.",
        "A limit order book stores resting quantities at prices, with a venue-specific priority rule. Under a simplified price-time rule, a marketable buy consumes the cheapest ask first and earlier orders first at a tied price. Actual venues may have hidden liquidity, special order types, pro-rata rules, and other allocation details. State the modeled rule explicitly.\n\nTop-of-book quotes and OHLC bars do not reveal an individual resting order's queue position. A bar touching a limit price does not prove that an order would have filled. A book replay needs time-ordered updates, sequence handling, and a defined response to missing messages; otherwise a detailed-looking simulation can still invent liquidity.",
        "The asks are an early three-share order at 100, a later four-share order at 100, and nine shares at 101. A five-share buy capped at 100 fills all three early shares and two later shares; its average price is 100. The higher-priced order is ineligible. If the taker requests ten shares with the same cap, three remain unfilled.\n\nThe downloadable research lab's match_asks function executes this price-time fixture. It is ask-side and synchronous, with no hidden orders or real exchange queue; the earlier paper-bot project handles durable account and fill identities separately.",
        "Test tied prices, an unmarketable limit, partial consumption, duplicate resting identities, and zero or invalid quantities. Preserve both price and arrival order. Report unfilled quantity rather than silently forcing completion at the last bar's price. If extending to a live feed, design sequence-gap recovery and snapshot reconciliation before using the reconstructed book for decisions.",
        r"P_{avg}=\sum_iq_iP_i/\sum_iq_i",
        'print("Filled quantity:", 3 + 2)\nprint("Average execution price:", (3 * 100 + 2 * 100) / 5)\nprint("Unfilled ten-share order:", 10 - 3 - 4)',
        "Run match_asks, then raise the taker limit to 101 for a ten-share order. Calculate its fills and weighted average price.",
        "The fills are 3 at 100, 4 at 100, and 3 at 101; average price is 100.3. The original cap of 100 instead leaves three unfilled.",
        [
            (
                "A bar touching your limit proves your resting order filled:",
                ["Always", "No", "Only on a daily chart"],
                1,
                "Bar extrema do not establish queue position or available allocation.",
            ),
            (
                "Under the stated rule, equal-price asks are consumed by:",
                ["Randomly changing share counts", "Alphabetical ticker alone", "Arrival priority"],
                2,
                "The fixture uses price first, then arrival order.",
            ),
            (
                "Four shares at 50 and six at 51 produce average price:",
                ["50.6", "50.5", "51"],
                0,
                "Quantity-weighted average fill price is (4×50+6×51)/10=50.6.",
            ),
            (
                "A ten-share taker with only seven eligible resting shares has:",
                ["A guaranteed ten-share fill", "Three unfilled shares", "No fill information"],
                1,
                "Do not manufacture liquidity to complete the order.",
            ),
        ],
        [ORDER, PAPER],
    )

    add(
        "5.35",
        8,
        "Multi-asset target reconciliation and cash budgets",
        "Translate a portfolio target into funded orders without spending the same cash twice or assuming unavailable netting.",
        "A portfolio rebalance begins with a dated account snapshot, executable marks, and a target vector. Compute target holdings and deltas per asset, then apply cash, share, exposure, and order constraints. Two individually affordable buys can be jointly unaffordable, so the account-level reservation must be atomic or otherwise coordinated.\n\nA sale may provide buying power only after its actual execution and under the account's settlement rules. Planned sale proceeds are not always spendable cash. The downloadable lagged replay uses immediate settlement, synchronous fills, fractional shares, and reductions before entries; those assumptions are explicitly narrower than a real brokerage workflow.",
        "With equity 10,000 and two desired weights .4 and .3, target notionals are 4,000 and 3,000 before fees, leaving 3,000 nominal cash. At prices 100 and 50, corresponding holdings are 40 and 60 shares. If holdings already include 20 shares of the first asset, its residual target is 20 shares, not 40.\n\nTo fund worst-case turnover in the toy replay, a fee reserve reduces the total target budget. The project declares this scaling rather than silently allowing a negative cash balance when requested weights sum to one.",
        "Test target sums above one, stale prices, conflicting outstanding orders, sell failures, and a price gap between decision and execution. Save target weights, fee reserve, actual fills, and remaining cash separately. A real multi-asset adapter needs settlement and margin rules, asynchronous reconciliation, and partial-fill planning. Portfolio weights describe a desired end state; they are not permission to bypass account constraints.",
        r"q_i^*=w_iE/P_i,\quad \Delta q_i=q_i^*-q_i^{held}-q_i^{committed}",
        'print("First target shares:", 0.4 * 10000 / 100)\nprint("Second target shares:", 0.3 * 10000 / 50)\nprint("First residual shares:", 0.4 * 10000 / 100 - 20)',
        "Allocate 20,000 equity at weights .25 and .5 with prices 50 and 100. Describe how failed sales and fees can change permitted buy instructions.",
        "Nominal targets are 100 shares in each asset and 5,000 cash before fees. Actual buys require available resources; failed sales cannot be treated as realized proceeds, and fee buffers reduce affordable size.",
        [
            (
                "A target weight is:",
                [
                    "A desired exposure before execution constraints",
                    "An instruction to buy the full target every tick",
                    "A settlement guarantee",
                ],
                0,
                "Convert targets to residual orders using actual state and commitments.",
            ),
            (
                "Planned sale proceeds are always immediately spendable:",
                [
                    "Yes",
                    "No; execution and account rules matter",
                    "Only when expected profit is positive",
                ],
                1,
                "Unexecuted or unsettled proceeds may not be available buying power.",
            ),
            (
                "Equity 8,000, target weight .25, and price 40 imply nominal shares:",
                ["20", "200", "50"],
                2,
                "Convert target weight to shares: .25×8,000/40=50.",
            ),
            (
                "Two workers using the same unreserved cash snapshot require:",
                [
                    "Coordinated account-level reservation",
                    "Larger random IDs only",
                    "No additional control",
                ],
                0,
                "Independent checks can otherwise approve jointly unaffordable orders.",
            ),
        ],
        [ORDER, PAPER],
    )

    add(
        "5.36",
        8,
        "Transaction-cost analysis and unfilled opportunity cost",
        "Reconcile realized execution cost with decision benchmarks and include the quantity that never traded.",
        "Transaction-cost analysis needs a declared benchmark, trade direction, authorized quantity, actual fills, explicit fees, and unfilled remainder. A midpoint or arrival price measures a different question from the signal-time price or a later market VWAP. Choosing the most favorable benchmark after the trade distorts interpretation.\n\nAverage cost of completed fills omits the opportunity cost of quantities that did not trade. This can flatter passive strategies that fill mainly under adverse selection while missing favorable moves. A complete parent-order analysis records cancellation, expiry, changed intent, and the price convention used to value the unfilled decision.",
        "A decision authorizes buying 100 shares at benchmark 50. Sixty fill at 50.10 with 3 of fees; forty remain unfilled while the evaluation price reaches 51. Realized price shortfall is 60×.10=6. Under this stipulated opportunity-cost convention, unfilled cost is 40×1=40. Total implementation shortfall is 6+3+40=49, or 98 bps of the 5,000 decision notional.\n\nThe unfilled component is model-dependent: if the investment decision was legitimately withdrawn, its interpretation may differ. Preserve the reason and time of withdrawal rather than rewriting the benchmark retrospectively.",
        "Report completion rate, average fill price, explicit fees, benchmark timestamps, and the opportunity-cost convention. Separate spread, delay, and impact only to the extent the data support their decomposition. Compare execution policies on the same parent decisions and market paths. A toy price-time matcher validates arithmetic and allocation rules; it does not estimate the causal market impact of the orders themselves.",
        r"IS=q_f(P_f-P_d)+q_u(P_{eval}-P_d)+Fees",
        'shortfall = 60 * (50.10 - 50) + 40 * (51 - 50) + 3\nprint("Parent shortfall:", round(shortfall, 6))\nprint("Shortfall bps:", shortfall / (100 * 50) * 10000)',
        "For a 50-share buy decision at 20, 30 fill at 20.05, 20 remain unfilled at evaluation price 20.50, and fees are 1. Compute shortfall under this convention.",
        "Filled price cost is 1.5, opportunity cost 10, and fees 1, totaling 12.5 or 125 bps of the 1,000 decision notional. Explain the evaluation-time choice.",
        [
            (
                "Comparing only completed fills can omit:",
                [
                    "Every fee in all systems",
                    "Unfilled opportunity cost",
                    "The existence of prices",
                ],
                1,
                "A parent decision includes quantities that may never execute.",
            ),
            (
                "An execution benchmark should be chosen:",
                [
                    "Afterward to minimize reported cost",
                    "From whichever chart looks best",
                    "According to a declared decision convention",
                ],
                2,
                "Benchmark choice determines the question being measured.",
            ),
            (
                "A 20-share unfilled buy rises from decision 10 to evaluation 11. Stipulated opportunity cost is:",
                ["20", "1", "220"],
                0,
                "20×(11−10)=20 before other components.",
            ),
            (
                "A toy matcher establishes the causal permanent market impact of its own orders:",
                ["Always", "No", "Only when volume is bounded"],
                1,
                "A fixed-price replay does not model the counterfactual price response.",
            ),
        ],
        [ORDER, PAPER],
    )

    add(
        "5.37",
        9,
        "Cross-sectional momentum and ranked portfolios",
        "Rank eligible securities using past information and map scores to bounded targets with deterministic ties and a cash policy.",
        "Cross-sectional momentum compares assets with one another, while a time-series trend rule compares an asset with its own past. Define the return window, any skipped recent interval, corporate-action convention, minimum history, liquidity filters, and rebalance schedule. A universe filter can influence performance as much as the ranking formula.\n\nA rank gives ordering, not expected return magnitude. Specify the number of selected names, equal or score-based weights, name and sector caps, and what happens when too few assets qualify. Deterministic tie-breaking and fixed missing-data rules support reproducibility. Do not impute an ineligible asset into the top group merely because its score is high.",
        "Scores are A=.1, B=.2, and C=.9, but C is unavailable under the dated universe rule. Selecting two eligible names gives B then A. With a .4 per-name weight cap, each gets .4 and .2 remains in cash. The downloadable rank_targets function reproduces this case.\n\nIf only A is eligible, a .4 cap leaves .6 in cash. Redistributing everything to A would violate the declared mandate even though the ranking step itself succeeded.",
        "Evaluate the full historical selection process, including delisted securities and contemporaneous liquidity. Compare equal weighting and a passive benchmark, report turnover and concentration, and test costs and delayed execution. Tie-breakers and filters must be frozen before final evaluation. A successful ranking function is evidence of implementation correctness; predictive performance requires independent market data and an executable portfolio study.",
        r"w_i\leq w_{cap},\quad w_{cash}=1-\sum_iw_i",
        'print("Selected name weight:", min(1 / 2, 0.4))\nprint("Residual cash weight:", 1 - 2 * min(1 / 2, 0.4))',
        "Run rank_targets with one eligible asset and a .3 cap. Specify tie-breaking and missing-history rules for a historical extension.",
        "The eligible asset receives .3 and cash .7. Use a stable symbol tie-breaker or another declared rule and reject insufficient history rather than borrowing future observations.",
        [
            (
                "A high score from an ineligible asset should:",
                [
                    "Override universe rules",
                    "Receive maximum leverage",
                    "Remain excluded under the declared contract",
                ],
                2,
                "Eligibility is applied before ranking and allocation.",
            ),
            ("Two names at .35 each leave cash weight:", [".3", ".65", "0"], 0, "1−.35−.35=.3."),
            (
                "A rank directly specifies expected return in basis points:",
                ["Always", "No", "Only for momentum"],
                1,
                "Ordering and calibrated return magnitude are different outputs.",
            ),
            (
                "Too few eligible names under a hard name cap may require:",
                ["Ignoring the cap", "Inventing eligible observations", "Holding additional cash"],
                2,
                "The allocation must still satisfy its constraints.",
            ),
        ],
        [LEAK, PAPER],
    )

    add(
        "5.38",
        9,
        "Pairs systems, hedge estimation, and regime failure",
        "Connect a statistical spread model to a two-leg execution contract without assuming correlation supplies a hedge.",
        "A pairs strategy needs a defensible relationship, an estimated hedge convention, a signal normalization, and two executable legs. Return correlation alone does not establish cointegration of levels, and a fitted stationary spread does not guarantee profitable reversion after costs. Study the econometrics course's cointegration and error-correction units before interpreting test output.\n\nEstimate hedge parameters on development data and preserve their units. Price-based, dollar-neutral, and beta-neutral hedges are different constructions. Borrow availability, financing, margin, and legging risk are operational requirements for a short leg, not implementation details that can be ignored because net notional is small.",
        "A fitted relation is A=2+1.5B+s. With A=80 and B=50, the residual is 3. Selling one unit of the spread under this normalization means shorting one A and buying 1.5 B units. The dollar notionals are 80 short and 75 long, so the pair is not exactly dollar neutral.\n\nIf the long leg fills and the short leg is rejected for unavailable borrow, the account has directional exposure. A planned target hedge is not a completed economic hedge.",
        "Write an order-state policy for both-leg acceptance, partial fills, cancel races, and a failed leg. Define exit and model-invalidation criteria, including structural shifts and stale estimates. Evaluate a deliberately broken relation as well as a planted cointegrating fixture. The course's local statistical lab diagnoses a synthetic relation; the current long/cash backtester does not execute short pairs and must not be used to claim their realized profitability.",
        r"s_t=A_t-\alpha-\beta B_t",
        'print("Pair residual:", 80 - 2 - 1.5 * 50)\nprint("Long dollar leg:", 1.5 * 50)\nprint("Net dollar exposure:", 1.5 * 50 - 80)',
        "For A=65, B=30, intercept 1, and hedge ratio 2, calculate spread and long/short notionals for selling one spread. State the failed-leg response.",
        "Spread is 4; selling one spread shorts 65 of A and buys 60 of B, leaving net −5. Reconcile a failed leg, bound remaining exposure, and use the declared cancellation or reduction procedure.",
        [
            (
                "A cointegrating hedge is always exactly dollar neutral:",
                ["No", "Yes", "Only when prices are positive"],
                0,
                "The fitted coefficient and current prices determine the dollar notionals.",
            ),
            (
                "An unavailable short borrow is:",
                [
                    "A cosmetic warning",
                    "An execution constraint that can invalidate the intended pair",
                    "Evidence the spread will revert",
                ],
                1,
                "The desired hedge cannot be assumed executable.",
            ),
            (
                "A=50, B=20, intercept 2, beta=2 imply residual:",
                ["2", "10", "8"],
                2,
                "Subtract the intercept and hedged leg: 50−2−2×20=8.",
            ),
            (
                "A long leg fills while its short hedge fails. The account is:",
                [
                    "Exposed to the actual long fill",
                    "Automatically flat",
                    "Unchanged until both fill",
                ],
                0,
                "Inventory follows actual fills, not planned paired intent.",
            ),
        ],
        [COINT, ORDER],
    )

    add(
        "5.39",
        9,
        "Volatility targeting and risk contributions",
        "Scale exposure using a dated risk estimate while controlling leverage, estimator instability, and rebalance turnover.",
        "Volatility targeting scales a baseline exposure according to the ratio of target volatility to an estimated volatility. It requires a compatible horizon and return convention. A small or missing denominator can create extreme leverage, so use an explicit estimate floor, position cap, warm-up rule, and uncertainty policy.\n\nA lagged volatility estimator can react slowly after a jump and can increase exposure following a calm period. Scaling does not make realized risk constant. Risk parity is a different portfolio construction problem involving marginal and total contributions; inverse-volatility weights coincide with some simpler cases but are not a universal risk-parity solution when correlations differ.",
        "With target volatility 10% and an estimate of 20%, the unconstrained scale is .5. If the estimate falls to 5%, the raw scale is 2, but a leverage cap of 1.2 permits only 1.2. If the estimate is unavailable, the correct action follows the declared abstention or conservative fallback, not division by an invented tiny value.\n\nTwo independent assets with volatilities 20% and 10% have inverse-volatility weights one-third and two-thirds. Different correlations or constraints can change the interpretation of their risk contributions.",
        "Fit and update risk estimates using available data only. Compare realized risk, turnover, concentration, and cost with an unscaled baseline across calm and stress periods. Log raw scale, constrained scale, estimator version, and fallback reason. A release should include a sudden-volatility-jump fixture and a near-zero estimate. Keep portfolio risk contributions distinct from signal confidence and enforce both exposure and cash constraints.",
        r"s_t=\min(s_{max},\sigma_{target}/\max(\hat\sigma_t,\sigma_{floor}))",
        'print("Scale at high volatility:", 0.10 / 0.20)\nprint("Capped scale at low volatility:", min(1.2, 0.10 / 0.05))\nprint("First inverse-volatility weight:", (1 / 0.2) / (1 / 0.2 + 1 / 0.1))',
        "Use target .12, estimate .08, and cap 1.1. Calculate raw and permitted scales, then define behavior for an unavailable estimate and a volatility jump.",
        "Raw scale is 1.5 and permitted scale 1.1. Missing estimates require a declared fallback or abstention; a sudden jump can outpace the lagged estimator, so stress the resulting exposure rather than promising constant risk.",
        [
            (
                "Volatility targeting guarantees constant realized risk:",
                ["Always", "No", "Only with daily updates"],
                1,
                "Estimation delay, jumps, and execution can produce deviations.",
            ),
            (
                "A near-zero volatility denominator requires:",
                ["Unlimited leverage", "No record", "An explicit floor, cap, or abstention policy"],
                2,
                "The raw ratio can otherwise create extreme exposure.",
            ),
            (
                "Target .09 divided by estimate .18 gives raw scale:",
                [".5", "2", ".09"],
                0,
                ".09/.18=.5 before other limits.",
            ),
            (
                "Inverse-volatility weighting equals risk parity in every correlated portfolio:",
                ["Yes", "No", "Only when weights sum to one"],
                1,
                "Marginal risk contributions depend on the full covariance structure.",
            ),
        ],
        [PAPER, LEAK],
    )

    add(
        "5.40",
        9,
        "Market making, inventory, and adverse selection",
        "Explain quote placement as a joint spread, inventory, and information-risk decision rather than a guaranteed spread capture.",
        "A market maker offers liquidity and may earn spread revenue, but inventory can move against it and informed counterparties may trade selectively. A backtest that fills both sides symmetrically whenever a bar crosses them can overstate performance by ignoring queue position and adverse selection. Maker rebates and taker fees also vary by venue and account; use explicit assumptions.\n\nInventory-aware quotes can shift their center or size to discourage further accumulation and encourage reduction. The sign convention matters: a positive long inventory may call for less aggressive buying and more aggressive selling. Quoting logic remains subordinate to hard inventory, loss, freshness, and order-count limits.",
        "A reference midprice is 100, half-spread .10, and a stipulated inventory skew shifts the quote center down .05 for a long position. Quotes become bid 99.85 and ask 100.05. Selling at the lower ask may reduce inventory more readily, while the lower bid discourages adding more. No fill is guaranteed.\n\nIf a buy fills at 99.85 and the market then drops to 99, the marked loss .85 exceeds the displayed .20 spread. One-sided fills and price moves dominate a simplistic spread-capture calculation.",
        "Build fixtures for a one-sided market, stale reference price, sudden jump, repeated cancellation, and inventory at its cap. Measure inventory distribution, adverse price movement after fills, quote lifetime, completion, fees, and drawdown. A toy quote formula illustrates control direction; it does not implement a complete market-making venue adapter or justify real orders. Use book-level evidence if queue-dependent claims are central to the strategy.",
        r"P_{bid}=m-skew-h,\quad P_{ask}=m-skew+h",
        'center = 100 - 0.05\nprint("Inventory-adjusted bid:", center - 0.10)\nprint("Inventory-adjusted ask:", center + 0.10)\nprint("Adverse mark after buy:", 99 - (center - 0.10))',
        "At mid 50, half-spread .05, and downward skew .02, calculate quotes and describe a one-sided fill scenario that loses money despite a positive quoted spread.",
        "Bid is 49.93 and ask 50.03. A buy followed by a drop to 49 produces a .93 marked loss before fees; the positive quote spread did not guarantee a round trip.",
        [
            (
                "A positive quoted spread guarantees profit:",
                ["No", "Yes", "Only with two-sided quotes"],
                0,
                "Inventory movement, adverse selection, fees, and asymmetric fills can dominate spread revenue.",
            ),
            (
                "A long-inventory downward quote skew generally aims to:",
                [
                    "Buy more aggressively at higher prices",
                    "Discourage additional buying and encourage selling",
                    "Remove all risk constraints",
                ],
                1,
                "The declared price shift changes both sides' aggressiveness.",
            ),
            (
                "Mid 20, half-spread .1, downward skew .05 imply bid:",
                ["20.15", "19.95", "19.85"],
                2,
                "The bid subtracts skew and half-spread: 20−.05−.1=19.85.",
            ),
            (
                "A credible market-making replay needs to challenge:",
                [
                    "Queue and one-sided-fill assumptions",
                    "Only the color of bid labels",
                    "Only the count of indicators",
                ],
                0,
                "Those assumptions directly affect executable spread capture.",
            ),
        ],
        [ORDER, PAPER],
    )

    add(
        "5.41",
        10,
        "Nested walk-forward evaluation and interval purging",
        "Select configurations inside chronological training windows and exclude training labels whose outcomes overlap the outer test interval.",
        "A label often describes a future interval, not a single timestamp. A training row observed before the test begins can still contain a target computed from prices inside the test period. Purging removes those overlapping labels. A fixed row gap is sufficient only if it actually covers the label horizon and data availability rules.\n\nNested evaluation places model and parameter selection inside each outer training window. The outer test then measures a procedure chosen without its outcomes. Repeatedly inspecting outer results and changing the procedure converts those results into development evidence; preserve a separate final evaluation or accurately describe the reuse.",
        "For observation indices 0 through 11, suppose each label ends two periods after its observation. At outer test origin 6, training labels must end strictly before 6: eligible observations are 0, 1, 2, and 3. Observation 4 ends at 6 and is excluded. At origin 9, eligible observations are 0 through 6.\n\nThe downloadable purged_forward_splits function applies this explicit interval rule. Variable label horizons require checking the actual end of each interval; merely subtracting a constant number of rows can retain leakage.",
        "Save each fold's observation IDs, label endpoints, available features, fitted transformations, selection score, and chosen configuration. Fit preprocessing within each inner training split. Evaluate only after the outer configuration is frozen. Test the split builder with an unusually long label, an empty eligible history, and an endpoint exactly at test start. Distinguish purging before a forward test from an embargo after a test in other split designs; they answer different overlap questions.",
        r"\mathcal T_k=\{i:i<t_k,\;end(i)<t_k\}",
        'eligible = 0\nfor i in range(6):\n    if i + 2 < 6:\n        eligible += 1\nprint("Eligible training rows:", eligible)',
        "With test origin 8 and label ends [2,3,4,5,9,7,8,10], identify eligible training indices and explain why a fixed two-row gap fails for index 4.",
        "Indices 0,1,2,3,5 qualify. Index 4 ends at 9 despite its early observation; indices 6 and 7 also overlap. A two-row gap would incorrectly retain index 4.",
        [
            (
                "An early observation with a label ending inside the test window is:",
                [
                    "Always safe",
                    "Potential leakage requiring exclusion",
                    "Automatically an unlabeled feature",
                ],
                1,
                "The target uses outcomes unavailable at the training cutoff.",
            ),
            (
                "Configuration selection belongs in:",
                [
                    "The final test score",
                    "A hindsight ranking",
                    "The inner training/evaluation procedure",
                ],
                2,
                "The outer test should assess the already selected procedure.",
            ),
            (
                "Origin 5 and label end i+2 allow training indices:",
                ["0,1,2", "0,1,2,3", "0 through 4"],
                0,
                "The strict rule i+2<5 retains only indices 0,1,2.",
            ),
            (
                "A variable-horizon label split must inspect:",
                [
                    "Only the total row count",
                    "Each label's actual information endpoint",
                    "Only ticker names",
                ],
                1,
                "A fixed gap need not cover irregular label intervals.",
            ),
        ],
        [SPLIT, LEAK],
    )

    add(
        "5.42",
        10,
        "Dependent uncertainty and the research trial ledger",
        "Separate sampling uncertainty from selection bias and account for the family of strategies actually explored.",
        "A strategy report is selected from a research process. The visible winner may represent hundreds of discarded signals, feature sets, or execution conventions. A confidence interval calculated as though this winner were specified in advance understates the evidence problem. Keep a trial ledger with hypotheses, datasets, costs, stopping rules, and result access.\n\nDependence introduces another issue. Resampling individual daily observations can destroy serial structure and make uncertainty look smaller. Block bootstrap designs preserve a chosen scale of dependence, but the block length and stationarity assumptions still need justification. A dependence correction does not erase strategy-selection bias; these are separate controls.",
        "A family of 20 planned tests using a Bonferroni familywise level .05 has per-test threshold .0025. A p-value .01 passes an unadjusted .05 test but does not pass this family rule. Under independent true nulls, 20 separate .05 tests have probability 1−.95^20, approximately .642, of at least one false rejection.\n\nFor 12 observations, a simple fixed-length block resample with block length three uses four blocks. That arithmetic describes the construction, not proof that three is a suitable block length for the observed process.",
        "Report both the unit being resampled and the selection process being evaluated. If the chosen strategy is reselected inside each resample, explain that procedure precisely; if it is held fixed, describe the conditional question. Compare several defensible dependence scales without selecting only the narrowest interval. Carry forward failed and inconclusive trials so a reviewer can distinguish genuinely new evidence from a repeated search through the same history. Connect this review to econometrics lessons 3.27 and 3.28.",
        r"\alpha_{test}=\alpha_{family}/M",
        'print("Family threshold:", 0.05 / 20)\nprint("Independent false-rejection probability:", 1 - 0.95 ** 20)\nprint("Length-three blocks for twelve rows:", 12 / 3)',
        "For 50 hypotheses, calculate a Bonferroni .05 threshold. Describe what a fixed-strategy block bootstrap does and does not account for after selecting the best strategy.",
        "The threshold is .001. A block bootstrap may reflect dependence for the specified resampling design, but fixing a selected winner does not automatically account for the earlier search over alternatives.",
        [
            (
                "Block resampling automatically corrects every form of strategy selection:",
                ["No", "Yes", "Only with many bootstrap draws"],
                0,
                "Dependence and selection require separate, explicit treatment.",
            ),
            (
                "A trial ledger should retain:",
                [
                    "Only profitable runs",
                    "Failed and inconclusive hypotheses as well as winners",
                    "Only deployment dates",
                ],
                1,
                "The family of attempted analyses affects evidence interpretation.",
            ),
            (
                "Family level .04 across 40 tests gives Bonferroni threshold:",
                [".01", ".04", ".001"],
                2,
                "Divide the family level across tests: .04/40=.001.",
            ),
            (
                "Selecting the block length solely for the narrowest interval creates:",
                [
                    "Another selection decision requiring disclosure",
                    "Guaranteed precision",
                    "An independent replication",
                ],
                0,
                "The uncertainty specification itself has been tuned to a preferred result.",
            ),
        ],
        [MULTI, LEAK],
    )

    add(
        "5.43",
        10,
        "Capacity, borrow, and stressed execution costs",
        "Evaluate whether a strategy remains feasible as order size, liquidity, and shorting constraints change.",
        "Capacity asks how performance and feasibility change with capital. Multiplying a small-account equity curve by ten assumes execution scales linearly, but spreads, book depth, participation limits, borrow, and market impact can change with order size. A strategy can exhaust its opportunity or violate operational limits before its theoretical signal disappears.\n\nSeparate observed costs from a stipulated stress model. A square-root impact formula is a scenario assumption unless calibrated and validated for the instrument, horizon, and trading process. Borrow availability and recalls can block a short position even when a quoted borrow fee looks acceptable. A paired signal remains exposed if only one executable leg survives.",
        "An order for 8,000 shares faces a stated participation cap of 5% of an independently specified 100,000-share interval volume. The simulator permits at most 5,000 shares, leaving 3,000 unresolved. If actual available volume is only 40,000, the same cap permits 2,000. A full fill at the requested size would violate this model.\n\nA short notional 100,000 with a stipulated annual borrow rate 12%, held ten days on a declared 365-day convention, incurs approximately 328.77 before other costs. This is an illustration; rates and conventions are inputs that must be sourced for a real study.",
        "Build a capacity curve across capital, participation, spread, delayed completion, and borrow scenarios. Recompute the inventory path and missed opportunity under partial fills instead of simply subtracting a larger flat fee from unchanged trades. Include a borrow rejection and a recall while the paired long remains open. Define a capital boundary based on both performance uncertainty and hard execution constraints. Do not use future realized interval volume as though it were known when the order was sized; label its use as an execution limit or supply an available forecast.",
        r"q_{fill}\le p_{max}V,\quad C_{borrow}=N r d/365",
        'print("Base permitted shares:", 0.05 * 100000)\nprint("Stressed permitted shares:", 0.05 * 40000)\nprint("Illustrative borrow cost:", 100000 * 0.12 * 10 / 365)',
        "Request 6,000 shares against volume 60,000 and a 4% cap. Calculate the maximum fill and residual, then specify what happens if a required short borrow disappears.",
        "Maximum fill is 2,400 and residual 3,600. Reject or reduce the intended short under the declared policy and reconcile any other filled legs; do not retain fictional hedged inventory.",
        [
            (
                "Scaling capital by ten necessarily scales net profit by ten:",
                ["Yes", "No", "Only in a backtest"],
                1,
                "Execution, liquidity, and financing can change with size.",
            ),
            (
                "Borrow availability should be treated as:",
                ["A chart label", "A fixed universal constant", "A dated feasibility constraint"],
                2,
                "An otherwise attractive short may not be executable.",
            ),
            (
                "A 3% participation limit on 50,000 shares permits at most:",
                ["1,500 shares", "15,000 shares", "3,000 shares"],
                0,
                "The permitted participation quantity is .03×50,000=1,500.",
            ),
            (
                "Partial-fill stress should change:",
                [
                    "Only an ending return label",
                    "The actual holdings and subsequent exposure path",
                    "Nothing if the intended target is unchanged",
                ],
                1,
                "Unfilled intent does not create inventory.",
            ),
        ],
        [ORDER, PAPER],
    )

    add(
        "5.44",
        10,
        "Differential tests for vectorized and event-driven research",
        "Use independent accounting identities and shared timing assumptions to diagnose disagreements between research implementations.",
        "Vectorized and event-driven systems can agree when they implement the same information, position, fill, and accounting conventions. Their architecture alone does not determine correctness. A discrepancy is a useful diagnostic: compare a short trace before comparing a full-period Sharpe ratio. Write down when the signal is known, which price executes it, how fees are funded, and whether weights refer to pre- or post-cost equity.\n\nThe downloadable lagged_backtest uses close decisions at the next supplied open, fractional long-only shares, sell-before-buy rebalancing, a conservative fee budget, and unlimited liquidity. These assumptions make its scope reproducible; they do not represent a full broker simulator.",
        "Open prices are 100, 110, and 120. Starting cash is 1,100. A full-investment decision after period 0 executes at the period-1 open, buying ten shares at 110. A cash decision after period 1 sells them at 120. With zero fees, final equity is 1,200. Buying at 100 would use a different execution convention and produce a different result.\n\nAt every event, equity equals cash plus shares times the current mark. In a constant-price round trip, any decline should reconcile to specified costs. A negative cash balance in a cash-only fixture is a failure even if the ending return looks plausible.",
        "Create golden cases for no trades, one purchase, a delayed exit, constant-price fees, a two-asset rotation, and a missing or invalid price. Compare shares, cash, fees, and execution index at each event. Treat a signal shift as an information rule, not a cosmetic array alignment. Explain any difference in fractional shares, cost reserve, or settlement before claiming one engine is more realistic. A differential test is strongest when its expected arithmetic is calculated independently rather than by copying the implementation under test.",
        r"E_t=C_t+\sum_i q_{i,t}P_{i,t}",
        'shares = 1100 / 110\nprint("Shares bought at next open:", shares)\nprint("Exit equity:", shares * 120)\nprint("Profit:", shares * 120 - 1100)',
        "With cash 900 and opens [80,90,99], calculate a next-open full-investment trade followed by exit. Specify a constant-price fee fixture and its accounting invariant.",
        "Buy ten shares at 90 and exit at 99 for equity 990 before fees. A constant-price round trip should lose exactly its recorded fees, with cash nonnegative and equity equal to cash plus marked holdings.",
        [
            (
                "Architecture alone makes every event-driven backtest unbiased:",
                ["No", "Yes", "Only if it uses classes"],
                0,
                "Timing, fills, and accounting still need validation.",
            ),
            (
                "A close-based decision filled at the next open should use:",
                [
                    "The already observed previous open",
                    "The next supplied opening price",
                    "Whichever price improves returns",
                ],
                1,
                "The fill must follow the declared information timing.",
            ),
            (
                "Cash 1,000 buys at 50 and exits at 55, without fees. Equity is:",
                ["1,050", "1,000", "1,100"],
                2,
                "Twenty shares multiplied by 55 give 1,100.",
            ),
            (
                "The best first comparison between disagreeing engines is:",
                [
                    "A short holdings, cash, and fill trace",
                    "Only the ending Sharpe ratio",
                    "The number of source lines",
                ],
                0,
                "Event-level accounting reveals where the conventions diverge.",
            ),
        ],
        [LEAK, PAPER],
    )

    add(
        "5.45",
        11,
        "Trade labels, meta-labels, and cost-aware classification",
        "Define the supervised learning target and evaluate probability decisions against class imbalance and economic payoffs.",
        "A label is a precise research object: observation time, event start and end, outcome rule, and available cost assumptions. A direction label asks a different question from a meta-label that accepts or rejects a trade proposed by a primary rule. Neither should be constructed using test-selected thresholds or features unavailable at the decision time.\n\nClass imbalance makes accuracy an incomplete metric. A model that always rejects trades may score highly when successful opportunities are rare, while providing no useful selection. Evaluate calibration, precision, recall, coverage, and the realized payoff of the declared decision rule. A classifier's probability is meaningful only relative to its label and evaluation population.",
        "Among 100 opportunities, only ten satisfy the positive label. Predicting negative for all gives 90% accuracy and zero recall for positive opportunities. Suppose a accepted trade gains 3 when successful, loses 2 otherwise, and incurs .2 cost regardless of outcome. Its stipulated expected payoff is 3p−2(1−p)−.2, positive only when p>.44.\n\nThis threshold assumes stable conditional payoffs and costs. If false positives tend to occur in expensive or illiquid periods, an aggregate probability threshold can hide the relevant dependency.",
        "Create labels only after fixing their horizon and outcome definition. Fit probability calibration using training or validation data, then freeze the threshold before the independent test. Record abstentions and rejected opportunities; their denominator is necessary for coverage and missed-opportunity analysis. Compare the full pipeline with the primary rule alone and a simple constant decision baseline. Link each feature to its availability timestamp and use interval purging when labels span time. The existing offline ridge project is a fitting demonstration; it does not automatically implement this richer labeling protocol.",
        r"E[\pi\mid p]=pG-(1-p)L-c",
        'print("Always-negative accuracy:", 90 / 100)\nprint("Break-even probability:", (2 + 0.2) / (3 + 2))\nprint("Expected payoff at p=.5:", 0.5 * 3 - 0.5 * 2 - 0.2)',
        "For gain 4, loss 1, and cost .25, derive the break-even probability. Explain why a 95%-accurate model may still fail on a dataset with 5% positive labels.",
        "The threshold is (1+.25)/(4+1)=.25 under the stipulated payoff model. Always predicting negative achieves 95% accuracy but retrieves no positives; inspect recall, coverage, calibration, and net payoff.",
        [
            (
                "A meta-label can represent:",
                [
                    "Guaranteed profit",
                    "Whether to accept a trade proposed by a primary rule",
                    "A replacement for timestamps",
                ],
                1,
                "Its target is conditional on the underlying opportunity definition.",
            ),
            (
                "An always-negative classifier on a rare-positive dataset can have:",
                [
                    "Perfect positive recall",
                    "No need for a baseline",
                    "High accuracy and zero positive recall",
                ],
                2,
                "The majority class can dominate the accuracy denominator.",
            ),
            (
                "Gain 2, loss 1, cost .2 imply break-even p:",
                [".4", ".2", ".6"],
                0,
                "Under the stated payoffs, break-even probability is (1+.2)/(2+1)=.4.",
            ),
            (
                "A probability threshold selected after seeing final test payoffs is:",
                [
                    "An untouched independent evaluation",
                    "A test-informed development choice",
                    "Automatically causal",
                ],
                1,
                "The evaluation sample has influenced the procedure.",
            ),
        ],
        [LEAK, SPLIT],
    )

    add(
        "5.46",
        11,
        "Evaluate retrieval, citations, and AI abstention",
        "Measure evidence retrieval and claim support separately from fluent output or schema compliance.",
        "An AI research assistant can return valid JSON and still make unsupported claims. Evaluation therefore separates retrieval, claim grounding, numerical extraction, temporal relevance, and abstention. A citation must support the particular proposition attached to it; merely mentioning a real source is insufficient. Build a small labeled set of source passages and expected claims before changing prompts or retrieval settings.\n\nThe downloadable evidence_scores function compares explicit expected and accepted evidence identifiers. It is a transparent set-based scoring example, not an automated verifier of semantic truth. Human labels or a separately validated evaluator still determine whether a passage supports a claim. Duplicated identifiers do not create extra evidence.",
        "Four evidence items are required. The system returns three distinct items, of which two are relevant. Precision is 2/3 and recall 2/4=.5. A system returning nothing has no accepted-item denominator, so precision is undefined in this implementation; recall is zero when relevant items exist. Report the convention rather than silently converting an undefined metric into perfect performance.\n\nAn assistant that abstains on every difficult case might have high precision among its few answers but poor coverage. Evaluate answer quality jointly with the fraction and difficulty of cases answered.",
        "Create cases containing an outdated filing, conflicting statements, unsupported arithmetic, missing source text, and an instruction embedded inside a retrieved document. Keep those documents as data and enforce tool permissions outside the model response. Score each category and preserve the exact evidence IDs, prompt/configuration version, answer, and review decision. A release gate should specify required support, acceptable abstention, and zero tolerance for invented source identifiers. These offline fixtures require no model API or live trading authority.",
        r"precision=TP/(TP+FP),\quad recall=TP/(TP+FN)",
        'print("Evidence precision:", 2 / 3)\nprint("Evidence recall:", 2 / 4)\nprint("Answer coverage:", 7 / 10)',
        "Five evidence items are required. An answer cites four distinct items, three relevant. Compute precision and recall, then define treatment of an empty answer and a fabricated source ID.",
        "Precision is .75 and recall .6. Empty-answer precision needs a declared undefined-value convention and must be considered alongside recall and coverage. A fabricated ID fails source validation even if the prose sounds plausible.",
        [
            (
                "Syntactically valid AI output proves its claims are supported:",
                ["No", "Yes", "Only when it contains URLs"],
                0,
                "Structure and evidential correctness are different properties.",
            ),
            (
                "High answer precision should also be evaluated with:",
                [
                    "Only font size",
                    "Coverage and the difficulty of abstained cases",
                    "Only token count",
                ],
                1,
                "Selective abstention can conceal broad failure to answer.",
            ),
            (
                "Two relevant citations among four returned give precision:",
                [".25", ".75", ".5"],
                2,
                "Precision uses relevant returned items divided by all returned items.",
            ),
            (
                "A retrieved instruction asking for trading authority should be:",
                [
                    "Treated as untrusted document content under external permission rules",
                    "Automatically executed",
                    "Allowed if it includes a citation",
                ],
                0,
                "Document text does not grant tool authority.",
            ),
        ],
        [AGENT, LEAK],
    )

    add(
        "5.47",
        11,
        "Monitor drift, delayed labels, and model decay",
        "Separate operational health from statistical change and evaluate outcomes only when their labels have matured.",
        "A running model needs several clocks: observation arrival, feature availability, prediction time, label maturity, and evaluation time. An apparent performance drop can come from a broken feed, changed population, execution costs, or a deteriorating predictive relationship. Monitoring should retain these distinctions so an incident response targets the actual failure.\n\nInput drift does not by itself prove economic failure, and stable input distributions do not guarantee stable conditional outcomes. Compare missingness, freshness, score distribution, coverage, calibration, costs, and realized risk against declared baselines. Define windows and minimum sample sizes before interpreting a noisy alert as evidence of a regime change.",
        "A feature was missing in 2 of 200 baseline observations, a rate of 1%. In a new window it is missing in 12 of 100, a rate of 12%, an increase of 11 percentage points. This warrants a data investigation under a predeclared 5-point alert rule; it does not establish which trades would have been profitable.\n\nIf 100 predictions were issued but only 70 outcome horizons have finished, scoring all 100 by treating unresolved labels as losses biases the result. Score the 70 eligible outcomes and disclose the pending 30 and any selection effects.",
        "Implement alerts with a named owner, observed statistic, threshold, sample count, and response. Separate a hard freshness halt from a softer statistical review. Freeze the deployed model while investigating unless a preapproved fallback applies; retraining on every alert can create unstable selection and hide a recurring data fault. Compare a challenger in shadow mode using the same matured opportunities, then review changes to calibration, net payoff, and worst-case behavior. Preserve the previous model and its economic state so rollback changes software without inventing holdings.",
        r"\Delta missing=m_{new}/n_{new}-m_{base}/n_{base}",
        'print("Missingness increase in percentage points:", 100 * (12 / 100 - 2 / 200))\nprint("Matured-label coverage:", 70 / 100)\nprint("Pending outcomes:", 100 - 70)',
        "Baseline missingness is 3/300 and current missingness is 8/80. Calculate the change. Define separate responses for a stale market feed and a weak but uncertain mature-label performance estimate.",
        "Missingness increases from 1% to 10%, a 9-point change. A stale feed follows the hard freshness policy; uncertain performance warrants a documented statistical review with adequate samples, not automatic outcome fabrication or uncontrolled retraining.",
        [
            (
                "An unresolved future label should automatically be scored as a loss:",
                ["Yes", "No", "Only on weekends"],
                1,
                "Its outcome is not yet available; report pending labels separately.",
            ),
            (
                "Feature drift alone proves a profitable relationship disappeared:",
                ["Always", "Only with a large sample", "No"],
                2,
                "Input distribution changes and conditional economic performance are different claims.",
            ),
            (
                "Missingness rising from 2% to 9% is an increase of:",
                ["7 percentage points", "7% relative", "11 percentage points"],
                0,
                "Subtract the rates to obtain a seven-point absolute increase.",
            ),
            (
                "A useful monitor alert contains:",
                [
                    "Only a red badge",
                    "Statistic, window, threshold, sample size, and response owner",
                    "Only the latest model name",
                ],
                1,
                "An actionable alert connects evidence to a defined operational response.",
            ),
        ],
        [LEAK, PAPER],
    )

    add(
        "5.48",
        11,
        "Advanced lab: challenge the complete trading and AI workflow",
        "Combine market replay, chronological research, cost accounting, and evidence evaluation into reproducible acceptance experiments.",
        "The advanced download joins several independent educational components: price-time ask matching, universe-constrained ranked targets, label-interval purging, a lagged multi-asset accounting engine, factor regression, a synthetic cointegration diagnostic, and set-based evidence evaluation. Run the default JSON report first, then construct an adverse fixture for each component. The components intentionally expose their assumptions rather than pretending to form a live brokerage service.\n\nA useful integrated review follows data into a decision, decision into intended exposure, intended exposure into actual fills, and actual fills into cash and holdings. AI evidence belongs beside this controlled workflow; a fluent generated recommendation must not bypass deterministic position and permission checks.",
        "The baseline replay buys ten shares at 110 and exits at 120, ending with 1,200 from 1,100 before fees. The queue case fills three shares from the earlier 100-price ask and two from the later ask. The first purged fold retains four observations. The evidence fixture gives precision 2/3 and recall .5. These independent hand checks make unexpected output visible.\n\nNow lower queue liquidity, introduce a long overlapping label, raise fees, and insert an unsupported evidence ID in separate runs. Record which assertion, metric, or acceptance rule changes. Do not modify every input at once and then infer an unexplained cause.",
        "Submit a fixture manifest, baseline output, four adverse runs, event-level cash reconciliation, timing diagram, and evidence review. Extend the final paper-bot dossier with these artifacts. Require no negative cash under its cash-only assumptions, no overlapping training labels, no invented fills, and no fabricated evidence identifiers. A failed premise is a useful result when it is correctly detected and documented. The unit checkpoint and final exam assess reasoning; local project execution and the written dossier require their own evidence and review.",
        r"accept=timing\_valid\land accounting\_valid\land evidence\_valid",
        'print("Baseline execution equity:", 1100 / 110 * 120)\nprint("Earlier and later queue fills:", 3, 2)\nprint("Evidence precision and recall:", 2 / 3, 2 / 4)',
        "Download the research lab and guide. Reproduce the baseline, add one adverse case for timing, liquidity, accounting, and evidence, and attach the results to the paper-bot capstone.",
        "The packet should reproduce the independent baseline arithmetic and show the appropriate rejection or changed outcome for each adverse fixture. An unsupported claim or impossible fill is a mandatory failure, regardless of the aggregate return.",
        [
            (
                "Changing every fixture input simultaneously is best for identifying a single failure cause:",
                ["No", "Yes", "Only when returns improve"],
                0,
                "Controlled changes make the cause of an output difference interpretable.",
            ),
            (
                "The advanced lab is a complete live brokerage adapter:",
                [
                    "Yes",
                    "No; its components use explicit offline assumptions",
                    "Only if its JSON is valid",
                ],
                1,
                "The local educational components do not implement live venue operations.",
            ),
            (
                "A project with invented fills and high return should:",
                [
                    "Pass automatically",
                    "Skip accounting review",
                    "Fail the execution acceptance condition",
                ],
                2,
                "A profitable number cannot override an invalid economic history.",
            ),
            (
                "A useful adverse fixture should demonstrate:",
                [
                    "The expected rejection or changed result under a challenged assumption",
                    "Only a different chart color",
                    "Only a longer runtime",
                ],
                0,
                "Failure tests connect a specified premise to observable behavior.",
            ),
        ],
        [ORDER, SPLIT, AGENT],
    )

    # Preserve original lesson, practice, and checkpoint identities for saved progress.
    originals = track["modules"]
    for item in originals:
        if item["part"] == "8":
            item["part"] = "12"
            item["reading"] = item["reading"].replace("Unit 8", "Unit 12")
    final = track["exams"].pop()
    final_questions = {row["lessonId"]: row for row in final["questions"]}
    for item in additions:
        final_questions[item["id"]] = {
            "id": f"stock-bots-final-{item['id']}",
            "lessonId": item["id"],
            **item.pop("_final"),
        }
    new_parts = [
        (
            "Advanced market and execution systems",
            "Corporate actions, price-time queues, multi-asset reconciliation, and implementation shortfall.",
        ),
        (
            "Strategy families and risk allocation",
            "Ranked momentum, pairs, volatility targeting, and inventory-aware market making.",
        ),
        (
            "Research validation and capacity",
            "Nested purged evaluation, selection uncertainty, liquidity stress, and independent accounting tests.",
        ),
        (
            "Advanced ML and AI evaluation",
            "Cost-aware labels, evidence scoring, delayed-label monitoring, and integrated adverse experiments.",
        ),
    ]
    project_part = track["parts"].pop()
    for index, (title, description) in enumerate(new_parts, 8):
        track["parts"].append({"id": str(index), "title": title, "description": description})
        group = additions[(index - 8) * 4 : (index - 7) * 4]
        exam_id = f"stock-bots-checkpoint-{index}"
        track["exams"].append(
            {
                "id": exam_id,
                "title": f"Unit {index}: {title}",
                "kind": "checkpoint",
                "version": 1,
                "description": "Four original transfer questions covering this advanced unit. Pass at 75%; review explanations after submission.",
                "minutes": 16,
                "passingScore": 75,
                "moduleIds": [m["id"] for m in group],
                "questions": [
                    {"id": f"{exam_id}-q{i}", "lessonId": m["id"], **m.pop("_checkpoint")}
                    for i, m in enumerate(group, 1)
                ],
            }
        )
    project_part["id"] = "12"
    track["parts"].append(project_part)
    track["modules"] = originals[:28] + additions + originals[28:]
    final.update(
        version=3,
        minutes=144,
        moduleIds=[m["id"] for m in track["modules"]],
        questions=[final_questions[m["id"]] for m in track["modules"]],
    )
    track["exams"].append(final)
    track["readingGuide"] = (
        "Twelve units, 48 original lessons, 96 practice questions, eleven checkpoints, and a 48-question final. Build the original offline paper bot, then extend the research with queue replay, multi-asset accounting, interval-purged evaluation, factor diagnostics, and AI evidence scoring. Guided worksheets run in the app; downloads run locally. The written capstone is self-assessed separately from the automatic exam."
    )
    track["description"] = (
        "Build and challenge algorithmic trading and AI research systems: signals, durable execution, portfolio strategies, rigorous validation, ML, evidence evaluation, and reproducible local projects."
    )
    track["resources"] += [
        {"title": "Download the advanced quantitative research lab", "url": LAB},
        {
            "title": "Download the advanced research guide",
            "url": "/course-assets/research/README.md",
        },
        {
            "title": "Download the research Python dependencies",
            "url": "/course-assets/research/requirements.txt",
        },
    ]
    track["modules"][-1]["assignment"]["prompt"] += (
        " Include the four advanced adverse experiments from lesson 5.48 and explain the resulting timing, liquidity, cash, and evidence decisions."
    )
    return track
