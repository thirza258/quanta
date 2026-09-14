"""Original applied course: strategy research, execution, ML, and AI bot operations."""

from book_courses import finish, lesson, q

ORDERS = "https://docs.alpaca.markets/us/docs/working-with-orders"
PAPER = "https://docs.alpaca.markets/us/docs/paper-trading"
LEAKAGE = "https://scikit-learn.org/stable/common_pitfalls.html"
SPLITS = (
    "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html"
)
BOOSTING = "https://xgboost.readthedocs.io/en/stable/tutorials/monotonic.html"
CALIBRATION = "https://scikit-learn.org/1.8/modules/calibration.html"
AGENTS = "https://www.anthropic.com/engineering/building-effective-agents"
CONTAINMENT = "https://www.anthropic.com/engineering/how-we-contain-claude"
QUEUES = "https://docs.python.org/3/library/asyncio-queue.html"
PROJECT = "/course-assets/stock-bots/paper_bot_lab.py"


def build_stock_bots():
    modules = []

    def add(id, part, title, objective, content, formula, code, task, solution, questions, reading):
        item = lesson(
            id,
            str(part),
            title,
            objective,
            reading,
            content,
            formula,
            code,
            task,
            solution,
            questions,
        )
        item["kind"] = "applied-study"
        modules.append(item)

    add(
        "5.6",
        1,
        "Specify a bot before writing a loop",
        "Turn an investment idea into a testable decision contract with explicit data, execution, and failure assumptions.",
        r"""
## Define the operation

A bot is a process that turns observations into state changes. Start with a decision contract: eligible instruments, information cutoff, signal rule, target holdings, rebalance frequency, execution convention, risk budget, and conditions for doing nothing. A slogan such as buy strong companies leaves almost every engineering choice unresolved.

Distinguish an alpha model from an execution algorithm. The first proposes which exposure might be useful. The second tries to obtain an already chosen exposure under trading constraints. A good execution algorithm does not establish predictive edge; a useful signal does not guarantee affordable fills.

The course follows a fictional Harbor research team building a long-only paper system. Dollar amounts, thresholds, and model outputs are stipulated teaching inputs. Each lesson produces one artifact for the final design dossier. Small calculations run in the in-app sandbox; the downloadable Python project runs an offline event and ledger simulation.

## A worked example

Harbor proposes a daily strategy in a $100,000 paper portfolio. It may allocate at most 10% to one eligible stock, observes completed daily bars, and places a target order at the next eligible open. An estimate of 12 basis points of gross benefit faces 4 basis points of spread cost, 2 of fees, and 3 of slippage. The rough expected net benefit is only 3 basis points.

A second analyst assumes 6 basis points of slippage. That consumes the entire gross estimate. Before building a faster bot, the team must decide whether the underlying idea survives a plausible cost range. An estimate is not a realized return, and these cost components must not overlap.

## Acceptance evidence

Write observable requirements: duplicate delivery does not duplicate exposure; missing features produce no new order; a fill changes cash exactly once; a restart recovers a halted state. Pair each requirement with a normal and adverse example. Define success in terms of reconciliation and sound evaluation before looking at a profit chart.

Keep research permission, paper execution, and any later live release as separate stages. Completing this course produces a tested educational prototype and a review packet. It does not silently connect credentials or authorize a brokerage trade.
""",
        r"\text{Net edge}_{bps}=\text{gross edge}-\text{spread}-\text{fees}-\text{slippage}",
        'gross = 12\nprint("Estimated net edge (bps):", gross - 4 - 2 - 3)\nprint("Stress net edge (bps):", gross - 4 - 2 - 6)',
        "Write a one-page bot contract. Use a gross estimate of 18 bps, spread cost 5, fees 3, and slippage 4. State a cost stress that makes the proposed advantage disappear.",
        "The initial net estimate is 6 bps. Slippage of 10 bps, holding other inputs fixed, brings it to zero. The contract also needs information and execution timestamps, eligible assets, position and cash caps, and an explicit abstention policy.",
        [
            q(
                "A gross estimate of 15 bps faces distinct costs of 4, 2, and 5 bps. Net estimate is:",
                ["4 bps", "11 bps", "26 bps"],
                0,
                "Subtract each nonoverlapping cost: 15 − 4 − 2 − 5 = 4 bps.",
            ),
            q(
                "Which statement is testable as a bot requirement?",
                [
                    "It should trade intelligently",
                    "Delivering the same event twice creates at most one intended order",
                    "Its chart should rise",
                ],
                1,
                "A concrete event and observable order count define an acceptance test independent of profit.",
            ),
            q(
                "A team improves order slicing but never tests its selection signal. What remains unestablished?",
                [
                    "The number of slices",
                    "The signal's predictive or economic value",
                    "That software can submit messages",
                ],
                1,
                "Execution quality concerns obtaining exposure; it does not prove that choosing that exposure has an edge.",
            ),
        ],
        "Start here. Deliverable: a bot decision contract. Read the project guide, then complete the data and event units before designing a trading rule.",
    )

    add(
        "5.1",
        1,
        "Event-driven bot architecture",
        "Separate market events, targets, orders, and fills so repeated or delayed messages cannot silently change the strategy.",
        r"""
## Design a pipeline with explicit boundaries

Market ingestion records an observation. Feature computation produces a dated input set. Strategy logic proposes a target. Risk logic permits, resizes, or rejects that target. An order manager tracks instructions, and a fill handler updates the ledger. These steps can live in one process initially while retaining separate interfaces.

A vectorized research calculation is useful for rapid experiments; an event-driven replay is useful for modeling chronology and operational state. Neither architecture automatically prevents look-ahead. Both require correct timestamps and information boundaries.

Give each event a stable identity, source, event time, receipt time, and schema version. Event time describes the underlying observation; receipt time describes when the bot learned about it. A late event should follow a documented policy rather than revise a decision as if the data had arrived earlier.

## A worked example

The feed delivers event E101 twice, followed by E102. The strategy intends one rebalance per completed event, so the expected count is two distinct intents. If each delivery creates a fresh random order ID, the bot can accidentally produce three orders. A deterministic intent key such as strategy-version plus symbol plus decision timestamp ties retries to the same decision.

Now crash after a broker accepts E101's order but before acknowledgement is stored. Local absence of confirmation means unknown external state, not rejection. Reconcile using the stable client identifier and broker records before deciding whether another submission is permissible. Identifier support and retry semantics are adapter-specific; verify the actual broker contract.

## Make replay a first-class tool

Keep an immutable input log and enough state to reconstruct what each component believed. Test duplicate events, a missing sequence number, late data, an out-of-order acknowledgement, and a fill arriving during cancellation. Record the transition and the reason for every rejected action.

A single owner of account mutations makes reasoning easier. If multiple workers are introduced, use a durable transactional boundary and uniqueness constraints. An in-memory set alone does not survive a crash or coordinate two processes.
""",
        r"\text{Observation}\rightarrow\text{Features}\rightarrow\text{Target}\rightarrow\text{Risk}\rightarrow\text{Order}\rightarrow\text{Fill}",
        'events = [101, 101, 102]\nintents = 0\nfor i in range(len(events)):\n    duplicate = False\n    for j in range(i):\n        if events[i] == events[j]:\n            duplicate = True\n    if not duplicate:\n        intents = intents + 1\nprint("Distinct intents:", intents)',
        "Draw six component boundaries for Harbor. Describe recovery after an accepted order's acknowledgement is lost, and explain why the in-memory deduplication example is insufficient for deployment.",
        "Preserve the intent and stable client ID, query the external order and fill records, then reconcile before retrying. Durable uniqueness must survive restart and coordinate writers; the small loop demonstrates only the counting rule.",
        [
            q(
                "What prevents duplicate orders after a retry?",
                [
                    "Faster polling",
                    "Stable identifiers plus durable reconciliation",
                    "Random position sizing",
                ],
                1,
                "A stable identity links retries to the original intent; durable reconciliation establishes what already happened.",
            ),
            q(
                "An acknowledgement is missing after submission. The correct initial classification is:",
                ["Definitely rejected", "Definitely filled", "Unknown external order state"],
                2,
                "The broker may have accepted the instruction even if its response was lost.",
            ),
            q(
                "Events A, A, B, B, and C each require one distinct decision. How many decision intents should survive deduplication?",
                ["3", "4", "5"],
                0,
                "Only A, B, and C are distinct; repeated delivery does not imply a new decision.",
            ),
        ],
        "Deliverable: event schema and architecture diagram. Broker reference: stable client identifiers and order lookup; implementation semantics must be verified per adapter.",
    )

    add(
        "5.7",
        1,
        "Market data contracts and trading clocks",
        "Reject stale or historically unavailable inputs and make sessions, adjustments, and missing data explicit.",
        r"""
## A timestamp is part of the value

A price needs an instrument, venue or source, currency, event timestamp, receipt timestamp, and adjustment convention. A financial statement also needs its publication timestamp and revision identity. Calendar dates alone are insufficient when a decision depends on intraday availability.

Store a consistent clock representation and convert to the exchange's session schedule at the boundary. Daylight-saving changes, holidays, half-days, and trading halts should come from a maintained calendar or broker session interface. Never equate a weekday with an open market. The offline project uses a supplied session-open flag rather than pretending to implement an exchange calendar.

Distinguish a missing bar from a genuine zero return. Mixing adjusted historical closes with raw order prices can fabricate a signal around splits. Keep corporate actions and total-return assumptions separate from executable quotes.

## A worked example

A quote event is timestamped 10:00:00.000 and arrives at 10:00:00.400. At a decision time of 10:00:00.900, its age from the event clock is 900 ms. Under a stipulated 750 ms freshness limit, the bot rejects a new entry even though network transport took only 400 ms.

A second quote carries a timestamp after the decision time because of clock skew. It must not pass merely because the computed age is negative. Validate both clock ordering and a maximum age. These thresholds are policy examples, not universal trading standards.

## Reconstruct the information set

For each decision, retain the exact quote or bar ID and the latest eligible filing version. A March release describing December cannot enter a February historical decision. Reject unsupported instruments and nonfinite or nonpositive prices before computing exposure.

The assignment should include fixtures for stale data, future timestamps, duplicate bars, missing volume, a split, and a closed session. Explain whether each causes an abstention, a delayed decision, or a research-only adjustment. Avoid filling a data gap with generated prices while labeling the result historical.
""",
        r"\text{Age}=t_{decision}-t_{event};\quad 0\leq\text{Age}\leq\text{limit}",
        'event_ms = 0\nreceived_ms = 400\ndecision_ms = 900\nage = decision_ms - event_ms\nprint("Quote age (ms):", age)\nprint("Entry permitted:", age >= 0 and age <= 750)',
        "A quote is 650 ms old under a 500 ms policy; another is dated 100 ms in the future. Explain both decisions and list the clocks that belong in the audit record.",
        "Both should fail the stated freshness validation: the first is too old and the second has an invalid future age. Keep event, receipt, decision, and order timestamps plus the clock and session conventions.",
        [
            q(
                "A quote 900 ms old under a 750 ms maximum is:",
                [
                    "Eligible because it arrived today",
                    "Stale under this policy",
                    "Always a valid fill price",
                ],
                1,
                "The age exceeds the stipulated maximum; current-day membership does not make it fresh.",
            ),
            q(
                "Why retain a filing's publication timestamp?",
                [
                    "To determine when it could enter a historical decision",
                    "To replace its actual reporting period",
                    "To guarantee its claims are correct",
                ],
                0,
                "Availability, rather than the period described, determines whether a decision could have used the information.",
            ),
            q(
                "A quote timestamp is later than the bot's decision time. What should the freshness gate do?",
                [
                    "Accept because age is below the maximum",
                    "Increase order size",
                    "Reject or investigate clock inconsistency",
                ],
                2,
                "A negative age is not evidence of freshness; clock ordering must be valid before using the quote.",
            ),
        ],
        "Deliverable: point-in-time data contract and six bad-data fixtures. Reuse the data-provenance methods from Quantitative Investment Analysis.",
    )

    add(
        "5.8",
        1,
        "Feature engineering and reproducible signals",
        "Build past-only features with explicit warm-up, scale, and version rules shared by research and execution.",
        r"""
## Treat features as versioned computations

Define each feature with its input field, window, lag, adjustment basis, missing-data rule, and units. A twenty-bar return and a twenty-calendar-day return need not be identical. A trailing average that includes the current completed bar is available only after that bar completes.

Warm-up is a state, not a zero. If a feature needs twenty valid observations and only twelve exist, the model should see an unavailable input or abstain under a documented rule. Filling the missing feature with zero can change a model's meaning and create unexpected orders.

Use the same transformations in training and inference. Fitted preprocessing belongs to the training artifact, while rolling calculations require a defined historical window. A price-level feature can drift with splits or nominal scale; return, ratio, or normalized features can be more interpretable but do not automatically become stationary.

## A worked example

Completed closes are 100, 102, 101, and 104. A three-period simple return at the final close is 104/100 − 1 = 4%. The three most recent completed closes average (102 + 101 + 104)/3 = 102.333. The final close is about 1.63% above that average.

This is a feature calculation, not proof of trend profitability. If the decision instead occurs before the final close, 104 is unavailable and both inputs must be recomputed from earlier data. Feature timing determines the earliest possible execution.

## A reproducibility check

Save a tiny input fixture and expected feature values. Compare research and running-bot outputs on identical data, including a missing observation and the first eligible warm-up point. Record model and feature versions together so an old model cannot silently consume a reordered feature vector.

When a new feature is proposed, document the economic hypothesis before tuning its window. Log rejected variants and retain a baseline. A precise calculation can still be an overfit research choice.
""",
        r"Momentum_t=P_t/P_{t-L}-1",
        'closes = [100, 102, 101, 104]\nmean = (closes[1] + closes[2] + closes[3]) / 3\nprint("Three-period momentum:", closes[3] / closes[0] - 1)\nprint("Distance from trailing mean:", closes[3] / mean - 1)',
        "Using closes 50, 51, 49, and 52, compute the three-period return and final three-close average. Specify the output when only two closes are available.",
        "Return is 4%; the trailing mean is 50.6667. With only two closes the requested features lack sufficient history; return an explicit unavailable state and suppress decisions requiring them.",
        [
            q(
                "Price rises from 80 to 84 over the defined lookback. Simple momentum is:",
                ["4%", "5%", "8%"],
                1,
                "84/80 − 1 = 5%; the lookback definition determines the observation pair.",
            ),
            q(
                "A rolling feature has insufficient history. A sound default is:",
                [
                    "An explicit warm-up or unavailable state",
                    "Pretend the feature equals zero",
                    "Use future observations",
                ],
                0,
                "Unavailable inputs must not be silently converted into an ordinary valid feature value.",
            ),
            q(
                "A model expects features in the order momentum, volatility, valuation. Inference reverses the first two without changing the model. What is required?",
                [
                    "Nothing if both are numbers",
                    "More leverage",
                    "Reject the schema mismatch or restore the trained order",
                ],
                2,
                "Feature meaning and order are part of the model contract; numeric validity alone is insufficient.",
            ),
        ],
        "Deliverable: a feature dictionary and exact input/output fixtures. Read the preprocessing consistency reference linked from the course plan.",
    )

    def teach(
        id,
        part,
        title,
        objective,
        principle,
        case,
        operation,
        formula,
        code,
        task,
        solution,
        questions,
    ):
        add(
            id,
            part,
            title,
            objective,
            f"## Design and reasoning\n\n{principle}\n\n## A worked example\n\n{case}\n\n## Implementation and review\n\n{operation}",
            formula,
            code,
            task,
            solution,
            [q(*row) for row in questions],
            f"Unit {part} engineering study. Produce the assignment artifact, reproduce the worksheet, and consult the primary references below. All Harbor cases are fictional.",
        )

    teach(
        "5.2",
        2,
        "Rule-based strategy bots",
        "Convert a signal into a target position and reconcile that target with holdings and outstanding orders.",
        "Separate the desired end state from the instruction sent now. A binary signal can mean a target weight of 0% or 10%; it does not mean buy another 10% on every iteration. Convert weight to shares using a dated equity estimate and an executable price convention. Specify rounding, minimum lot size, cash reserves, and when a target expires.\n\nOutstanding orders are commitments. A pending buy contributes positive shares and a pending sell contributes negative shares to the projected holding. Ignoring them causes repeated rebalancing to overshoot. A cancellation request does not remove that commitment until its result is known.",
        "Harbor targets 200 shares and holds 120. With no open orders the buy requirement is 80 shares. With a previously accepted buy of 50 shares still outstanding, the residual is only 30. If 20 of that order fill, holdings become 140 and remaining commitments become 30; the residual stays 30. This invariance is a useful test of the accounting.\n\nIf the signal disappears, first reconcile or cancel the existing buy. Do not immediately submit a 120-share sell while assuming the buy vanished. Treat conflicting instructions as an order-management problem.",
        "Implement target calculation as a pure function of a versioned snapshot. The order manager, not the signal function, owns retries. Introduce a no-trade band so negligible target changes do not create excessive turnover. Record the raw target, rounded target, existing holdings, commitments, and final permitted instruction. Compare the same rule against cash and a declared passive benchmark using identical costs and dates.",
        r"q_{new}=q_{target}-q_{held}-q_{pending,buy}+q_{pending,sell}",
        'target = 200\nheld = 120\npending = 50\nprint("Residual buy shares:", target - held - pending)\nprint("After partial fill:", target - (held + 20) - (pending - 20))',
        "Target 150 shares with 100 held and 20 pending buys. Then model a 10-share partial fill. Explain both new-order requirements.",
        "The residual is 30 in both states: 150−100−20 and 150−110−10. Holdings and outstanding commitments move together on a fill. The target should not be re-added on each tick.",
        [
            (
                "A target of 200 shares with 120 held requires how many new shares, without pending orders?",
                ["320", "200", "80"],
                2,
                "The difference is 200−120 = 80. The generator retains the legacy first question exactly.",
            ),
            (
                "Target 200, held 120, and 50 accepted buy shares still pending. The residual is:",
                ["30", "80", "170"],
                0,
                "Subtract the accepted commitment as well as the holding.",
            ),
            (
                "Target 90, held 50, pending buy 25. Ten pending shares fill. The remaining residual decision is:",
                ["5 shares", "15 shares", "25 shares"],
                1,
                "After the fill: 90−60−15 = 15, the same residual as before.",
            ),
        ],
    )

    teach(
        "5.9",
        2,
        "Trend rules, breakouts, and turnover",
        "Specify an executable trend rule with entry, exit, warm-up, and turnover controls.",
        "A rule must define the information window precisely. For a breakout observed at today's completed close, compare that close with an earlier high window that excludes today. Including today's high changes the question and can make a strict close-above-high test impossible. A moving-average rule instead compares levels computed from a declared window.\n\nUse separate entry and exit thresholds when a small fluctuation would otherwise churn the portfolio. This hysteresis is a design choice with a trade-off: less turnover can delay an exit. Do not select the band after inspecting the final evaluation period.",
        "Earlier highs are 100, 102, and 101. A completed close of 103 exceeds the prior maximum of 102. Under an illustrative rule requiring a 0.5% breakout, the entry threshold is 102.51, so the signal qualifies. A 1.5% band would require 103.53 and would not qualify. Execution occurs on a later eligible event, whose price need not equal 103.\n\nA backtest earns 1.2% gross while turning the portfolio over six one-way notional equivalents. At 15 bps per equivalent, estimated trading costs are 0.9%, leaving 0.3% before other omitted costs.",
        "Build a fixture for a flat market, a gap, a missing close, and a split-adjustment mismatch. Evaluate a small preregistered parameter grid on training and validation windows, then freeze it. Report return, drawdown, time in market, turnover, and sensitivity to costs. A trend indicator is a descriptive transformation; the ability to compute it does not establish an economic edge.",
        r"\text{Entry threshold}=\max(H_{t-L},\ldots,H_{t-1})(1+b)",
        'prior_high = max([100, 102, 101])\nprint("Breakout threshold:", prior_high * 1.005)\nprint("Entry signal:", 103 > prior_high * 1.005)\nprint("Net percent:", 1.2 - 6 * 0.15)',
        "Create a prior-window breakout test with earlier maximum 80, band 1%, and close 80.5. Explain which next-event execution assumption you will test.",
        "The threshold is 80.8, so no entry qualifies. A later marketable fill can gap away from the signal close; specify costs and a fresh price before sizing.",
        [
            (
                "The prior high is 100 and the entry band is 1%. Threshold is:",
                ["99", "100", "101"],
                2,
                "Multiply 100 by 1.01.",
            ),
            (
                "Why use separate entry and exit bands?",
                [
                    "To make losses impossible",
                    "To reduce frequent reversals near a boundary",
                    "To eliminate the need for costs",
                ],
                1,
                "Hysteresis can reduce churn while introducing delayed responses.",
            ),
            (
                "Gross return is 2%, turnover is eight one-way equivalents, and cost is 20 bps each. Approximate net return is:",
                ["0.4%", "1.8%", "3.6%"],
                0,
                "Costs are 8×0.2% = 1.6%; subtract from 2%.",
            ),
        ],
    )

    teach(
        "5.10",
        2,
        "Mean reversion and pairs hypotheses",
        "Distinguish a normalized deviation from evidence of reversion and account for both legs of a spread.",
        "A z-score describes deviation relative to an estimated mean and scale. It is not a guarantee that price will return to a historical level. Structural changes can move both the mean and variance. Specify the estimation window, fit the relationship using past data, and explain why a temporary displacement might close.\n\nFor pairs, define a spread such as A minus beta times B. Correlation of returns does not prove that this price spread is stationary. A fitted hedge ratio, a stationarity diagnostic, and an economic relationship answer different questions. Check sensitivity to sample choice and corporate changes before treating a spread as tradable.",
        "A spread of 14 has a training mean of 10 and standard deviation 2, giving a z-score of 2. Harbor's paper research rule considers selling the spread above 1.5. That requires short A and long beta units of B under the stated sign convention; the current in-app long/cash sandbox cannot express both legs.\n\nIf the planned legs are $10,000 long and $10,000 short, net dollar exposure is zero but gross exposure is $20,000. Fees, stock borrow, asymmetric fills, beta mismatch, and abrupt divergence can still produce a loss.",
        "Keep pairs work as a research worksheet unless the execution engine explicitly supports borrow availability, short margin, and two-leg state. Test a one-leg fill, a borrow recall, and a spread that never reverts. Define an exit based on elapsed time or invalidated evidence as well as the signal. Zero estimated net exposure must never bypass gross and concentration limits.",
        r"z_t=(s_t-\mu_{train})/\sigma_{train}",
        'spread = 14\nprint("Spread z-score:", (spread - 10) / 2)\nprint("Gross exposure:", abs(10000) + abs(-10000))\nprint("Net exposure:", 10000 - 10000)',
        "For a spread of 7, training mean 10, and scale 1.5, calculate z. Explain why a zero-net pair still needs a risk budget.",
        "z is −2. A proposed long-spread trade can continue falling and either leg may fill alone. Gross exposure, borrow, margin, and hedge error remain material.",
        [
            ("Spread 14, mean 10, scale 2 gives z of:", ["2", "4", "7"], 0, "(14−10)/2 = 2."),
            (
                "A $5,000 long and $5,000 short pair has gross exposure of:",
                ["$0", "$5,000", "$10,000"],
                2,
                "Gross adds absolute notionals, even when net is zero.",
            ),
            (
                "Only the long leg of a planned pair fills. The immediate account state is:",
                [
                    "Automatically hedged",
                    "Exposed to the filled leg until reconciled",
                    "Unchanged until both legs fill",
                ],
                1,
                "Each actual fill changes exposure; a planned hedge is not an executed hedge.",
            ),
        ],
    )

    teach(
        "5.11",
        2,
        "Backtests that respect costs and chronology",
        "Evaluate a frozen trading rule using a declared information cutoff, execution delay, benchmark, and cost model.",
        "Separate signal time, order time, and fill time. A strategy computed from a completed closing bar cannot assume it entered earlier at that bar's open. An OHLC bar also does not reveal whether its high preceded its low. Any intrabar stop or limit convention is an assumption that needs documentation.\n\nKeep research selection distinct from final evaluation. Changing a window after seeing the holdout makes that period part of development. Record every tried variant, fit preprocessing on training data, and keep an untouched later segment for the final frozen rule. Corporate actions, delistings, and availability timestamps belong in the data audit.",
        "Harbor signals at a close of 100 and buys 10 shares at the next open of 102. Later it sells at 104. At 5 bps commission on each notional, entry commission is $0.51 and exit commission $0.52. Net P&L is $18.97. Pretending entry occurred at the signal close would overstate the gross profit by $20.\n\nIf slippage is modeled in the fill price, do not subtract the same slippage again as a separate ledger fee. Compare with a passive position using the same timestamps, capital, and cost convention.",
        "Review an order-by-order trace in addition to aggregate statistics. Report drawdown, turnover, exposure, number of independent decisions, and a cost stress. A smooth curve from few trades does not support a precise Sharpe claim. Use the sandbox to demonstrate timing and costs; use the offline project for event and ledger failure tests. Neither establishes a live execution advantage.",
        r"\Pi=q(P_{exit}-P_{entry})-f q(P_{entry}+P_{exit})",
        'quantity = 10\nfee_rate = 0.0005\nprofit = quantity * (104 - 102) - fee_rate * quantity * (102 + 104)\nprint("Net trade P&L:", round(profit, 2))',
        "Compute a 20-share trade from 50 to 51 with 10 bps commission each way. Write the earliest fill time for a close-based signal.",
        "Gross profit is $20; fees are $1+$1.02, leaving $17.98. A decision based on a completed close requires a subsequent executable event under the chosen convention.",
        [
            (
                "A signal uses today's completed close. Buying at today's open is:",
                [
                    "A conservative delay",
                    "Using information unavailable at that fill time",
                    "Always valid for a daily bar",
                ],
                1,
                "The close was not known at the earlier open.",
            ),
            (
                "Slippage is already embedded in fill prices. The ledger should:",
                [
                    "Subtract the same slippage again",
                    "Ignore fees too",
                    "Avoid counting that slippage twice",
                ],
                2,
                "Separate explicit fees from costs already captured by execution prices.",
            ),
            (
                "Ten shares are bought at 20 and sold at 21; commissions total $0.41. Net P&L is:",
                ["$9.59", "$10.41", "$0.59"],
                0,
                "Gross profit is $10; subtract $0.41.",
            ),
        ],
    )

    teach(
        "5.12",
        3,
        "Quotes, spread, and implementation shortfall",
        "Measure an execution against a declared decision benchmark while distinguishing spread, impact, and delay.",
        "A quote is an indication at a particular time, size, and venue. The midpoint is useful as a benchmark but is not necessarily executable. A marketable buy typically consumes offered liquidity; a resting limit may fail to fill or fill when the market moves against it. Better price and greater fill certainty are competing objectives.\n\nImplementation shortfall compares execution with a decision benchmark, adjusted for trade direction. Explicit fees can be added separately. Spread, market impact, and delay are explanatory components whose estimates may overlap; avoid presenting a precise causal decomposition without the necessary data.",
        "The bid is 99.90 and the ask 100.10, so the midpoint is 100 and the quoted spread is 20 bps. A buy filling at 100.12 costs 12 bps relative to that midpoint before commission. Half the quoted spread accounts for 10 bps in a simple interpretation; the extra 2 bps cannot be confidently called permanent impact from this single observation.\n\nA sell at 99.88 also has 12 bps adverse shortfall under a direction-adjusted convention. Use consistent signs so a worse sell is not accidentally reported as a benefit.",
        "Store the benchmark's source, timestamp, and size with each decision. Report fill rate and unfilled opportunity cost alongside the average cost of completed trades; measuring only successful fills can flatter passive strategies. Paper fills do not reproduce queue priority, hidden liquidity, or adverse selection. The course uses explicit toy assumptions that should be challenged before interpreting results.",
        r"IS_{bps}=10^4 d(P_{fill}/P_{decision}-1),\quad d\in\{+1,-1\}",
        'mid = (99.90 + 100.10) / 2\nprint("Quoted spread (bps):", round((100.10 - 99.90) / mid * 10000, 2))\nprint("Buy shortfall (bps):", round((100.12 / mid - 1) * 10000, 2))',
        "A sell benchmark is 50 and fill is 49.95. Compute adverse shortfall before fees and list two limitations of a midpoint benchmark.",
        "Shortfall is 10 bps. The midpoint may not be executable for the desired size and may be stale relative to arrival; retain quote provenance and timing.",
        [
            (
                "Bid 49.95 and ask 50.05 have midpoint:",
                ["49.95", "50", "50.05"],
                1,
                "Average bid and ask.",
            ),
            (
                "A passive limit order guarantees:",
                [
                    "A completed trade",
                    "No adverse selection",
                    "A price constraint if executed, under its contract",
                ],
                2,
                "The limit constrains price; it does not guarantee a fill.",
            ),
            (
                "A buy benchmark is 200 and fill 200.20. Shortfall before fees is:",
                ["10 bps adverse", "10 bps favorable", "100 bps adverse"],
                0,
                "200.20/200−1 = 0.001, or 10 bps.",
            ),
        ],
    )

    teach(
        "5.13",
        3,
        "Order state machines and cancellation races",
        "Handle acknowledgements, partial fills, cancellations, rejections, and ambiguous submissions without losing commitments.",
        "Model submission, acknowledgement, partial fill, complete fill, cancellation, and rejection as explicit states with legal transitions. A timeout is an observation about communication, not necessarily an order state. Broker messages can arrive twice or out of order, so deduplicate by durable identity and reconcile cumulative quantities.\n\nSeparate an intent ID from an external order ID and a fill ID. One intent may have a documented cancel-and-replace sequence, while one order may have many fills. Track original quantity, cumulative filled quantity, remaining quantity, and cancellation status. Do not assume a cancellation acknowledgement erases earlier fills.",
        "An order buys 100 shares. Forty fill, leaving 60. The bot requests cancellation, but 15 more fill before the cancellation completes. The ledger must contain 55 bought shares; the successful cancellation removes only the remaining 45. If the 15-share fill message is replayed, holdings remain 55.\n\nIf the broker reports cumulative filled quantity of 55, do not treat it as 55 additional shares after already booking 40. Distinguish incremental fill messages from cumulative order updates in the adapter contract.",
        "Build a transition table and test every terminal state. Preserve unknown orders as risk commitments until reconciliation resolves them. Record rejected transitions for investigation instead of forcing state to match the latest message blindly. The offline lab demonstrates partial fills and idempotent fill records; a real asynchronous adapter additionally needs broker-specific cancel races and sequencing behavior.",
        r"q_{remaining}=q_{original}-\sum_i q_{fill,i}",
        'original = 100\nfilled = 40 + 15\nprint("Actual holding:", filled)\nprint("Canceled remainder:", original - filled)',
        "Trace a 75-share order: fills 20, cancel request, fills 10, cancellation confirmed, replay of the 10-share fill. State holdings and canceled shares.",
        "Holdings are 30; the remaining 45 are canceled. Replaying the same fill ID makes no further ledger change. A cancel request alone is insufficient to release commitments.",
        [
            (
                "After 40 and 15 shares fill on a 100-share order, the remaining quantity is:",
                ["45", "55", "60"],
                0,
                "100−40−15 = 45.",
            ),
            (
                "A cumulative fill update rises from 40 to 55. New filled shares are:",
                ["55", "95", "15"],
                2,
                "Only the difference, or independently identified new fills, should be booked.",
            ),
            (
                "Cancellation confirms after 25 of 60 shares filled. What remains in holdings?",
                ["Zero", "25 shares", "60 shares"],
                1,
                "Cancellation ends the remainder; it does not reverse actual fills.",
            ),
        ],
    )

    teach(
        "5.14",
        3,
        "Execution schedules: TWAP, VWAP, and participation",
        "Choose and evaluate a slicing policy with explicit urgency, liquidity, and completion constraints.",
        "TWAP distributes quantity over time; VWAP schedules against an estimated volume profile; a participation policy sizes child orders relative to observed or estimated market volume. Each needs a remaining-quantity cap, eligibility rules, and an end-of-window policy. Naming the algorithm does not define its actual fill mechanics.\n\nFast execution reduces waiting exposure but can consume expensive liquidity. Slow execution may reduce immediate pressure while risking price movement or an unfinished parent order. Models that optimize this trade-off rely on assumptions about volatility, impact, and constraints; there is no universally optimal schedule.",
        "A 1,000-share parent has four equal time buckets. TWAP requests 250 per bucket. A forecast volume profile of 10%, 20%, 40%, and 30% suggests VWAP child targets of 100, 200, 400, and 300. Under a 5% participation cap, a bucket with 4,000 shares of eligible volume permits at most 200 shares, even when the schedule asks for 400.\n\nThe remaining 200 cannot simply disappear from the report. The parent needs a documented carry-forward, cancellation, or urgency change, with risk approval. Do not use a bucket's eventual full volume for an order placed before that volume was known.",
        "Simulate sparse volume, a missed bucket, a session ending early, and a late cancellation. Report both shortfall and completion percentage. A schedule should preserve parent quantity after partial fills and retries. Cap each child by remaining authorized quantity as well as participation; otherwise a catch-up rule can overfill the original decision.",
        r"q_{child}\leq\min(q_{remaining},\rho V_{eligible})",
        'parent = 1000\nprint("TWAP slice:", parent / 4)\nprofile = [0.1, 0.2, 0.4, 0.3]\nfor weight in profile:\n    print("VWAP target:", parent * weight)\nprint("Participation cap:", 4000 * 0.05)',
        "A 600-share remainder faces 3,000 shares of eligible volume and a 4% cap. State the largest child quantity and the unresolved completion decision.",
        "The child is capped at 120 shares. The other 480 remain unexecuted; carry forward, cancel, or change urgency only under the declared parent policy.",
        [
            (
                "A 900-share parent split over three equal time buckets requests:",
                ["30", "300", "900"],
                1,
                "TWAP's planned equal slices are 900/3.",
            ),
            (
                "A participation rule based on the entire future day's volume creates:",
                ["A guaranteed fair benchmark", "No timing issue", "A potential information leak"],
                2,
                "Future realized volume was unavailable to an earlier decision.",
            ),
            (
                "Remaining quantity is 80 and the volume cap permits 120. Maximum child quantity is:",
                ["80", "120", "200"],
                0,
                "The parent remainder is also a binding limit.",
            ),
        ],
    )

    teach(
        "5.5",
        3,
        "Mock broker and paper accounting",
        "Reconcile cash, inventory, fees, reservations, and marked equity from a durable fill ledger.",
        "An order does not itself change owned inventory. Accepted orders reserve resources; fills change cash and holdings; cancellations release only unfilled commitments. Keep available cash distinct from settled or total ledger cash. The educational lab uses immediate settlement, long-only integer shares, and one symbol, so its simplicity remains visible.\n\nUse a stable fill ID and an atomic transaction to book cash, shares, and fill history together. Money should have an explicit precision policy. The downloadable project uses integer cents for prices and a deterministic commission rounding rule; a production adapter must match the broker's actual currency and settlement semantics.",
        "Harbor starts with $10,000. Buying 40 shares at $100 with a $2 fee leaves $5,998 cash and 40 shares. Marking at $101 produces equity of $10,038: $5,998 plus $4,040. The $38 gain combines $40 unrealized appreciation with the $2 entry fee.\n\nA pending order for 60 additional shares is not a holding. It reserves buying power using its price cap and a fee buffer. Canceling that remainder releases the reserve without undoing the 40-share fill.",
        "Test cash and share conservation after every transition, not just at the final report. Reconcile independent order and fill records after restart. Compare paper outcomes with the documented simulation model; vendor paper environments can differ from live conditions, and the offline lab does not model queue position, market impact, borrow, or settlement delays. Treat correct arithmetic as evidence of ledger correctness, not a forecast of execution quality.",
        r"E_t=C_t+q_tP_{mark,t}",
        'cash = 10000 - 40 * 100 - 2\nprint("Cash after buy:", cash)\nprint("Marked equity:", cash + 40 * 101)\nprint("Net marked P&L:", cash + 40 * 101 - 10000)',
        "Start with $5,000, buy 20 at $50, pay $1, and mark at $49. Reconcile cash, inventory value, equity, and P&L.",
        "Cash $3,999; inventory $980; equity $4,979; P&L −$21. A canceled unfilled order does not affect this owned inventory.",
        [
            (
                "A partial fill should:",
                [
                    "Be treated as completely filled",
                    "Retain its remaining quantity",
                    "Erase its fill history",
                ],
                1,
                "The filled portion changes inventory; the remainder stays tracked until resolved.",
            ),
            (
                "An accepted but unfilled buy order changes:",
                ["Owned shares immediately", "Historical profit", "Reserved buying power"],
                2,
                "Resources are committed before inventory is actually acquired.",
            ),
            (
                "Cash is $7,499 after buying 25 shares with fees. Mark is $102. Total equity is:",
                ["$10,049", "$7,601", "$10,050"],
                0,
                "7,499 + 25×102 = 10,049.",
            ),
        ],
    )

    teach(
        "5.4",
        4,
        "Position sizing and circuit breakers",
        "Translate uncertain return assumptions into constrained position sizes and explicit loss-control states.",
        "Kelly sizing maximizes expected log growth in a specified repeated-bet model; it does not supply reliable probabilities or eliminate drawdowns. The binary-bet expression assumes a known win probability, a fixed payoff ratio, and losses bounded by the staked fraction. Stock gaps, changing payoffs, correlated bets, and estimation error break a literal mapping.\n\nFractional Kelly reduces the output of that model, but remains sensitive to its inputs. Practical sizing also needs capital, exposure, liquidity, and loss limits. A stop distance is a planned trigger distance, not a guaranteed maximum loss: a gap or unavailable market can execute beyond it.",
        "For a hypothetical even-money bet with win probability 0.55, full Kelly is 0.55−0.45 = 10%; half Kelly is 5%. If the true probability is 0.51, full Kelly is only 2%. The original estimate therefore matters more than the apparent precision of the arithmetic.\n\nUnder a separate stop-risk rule, a $200 loss budget and $2 distance suggest 100 shares before other caps. If an entry gaps from a $50 assumption to $55 while the stop remains $48, the $7 distance suggests at most 28 integer shares. Recompute at the executable price.",
        "Keep the position-size function deterministic and place it after the model proposal. Validate positive distances and finite inputs before division. Combine the resulting cap with cash, single-name, and portfolio constraints. Define which events halt new risk and who can resume. A halt blocks new exposure; cancellation and risk reduction require their own reconciled procedures.",
        r"f^*=p-(1-p)/b;\quad q_{risk}=\lfloor B/|P_{entry}-P_{stop}|\rfloor",
        'p = 0.55\nprint("Half Kelly fraction:", round((p - (1 - p)) / 2, 4))\nprint("Shares under stop budget:", int(200 / 2))\nprint("Shares after gap:", int(200 / 7))',
        "Calculate half Kelly for p=0.52 and b=1. Then size a $150 stop-risk budget with a $3 distance and a separate 40-share exposure cap.",
        "Half Kelly is 2%. Stop sizing permits 50 shares but the independent exposure cap reduces the allowed quantity to 40. Neither calculation guarantees a realized loss bound.",
        [
            (
                "For p=.55 and even payoffs, half Kelly is:",
                ["5%", "10%", "55%"],
                0,
                "Full Kelly is 10%; half is 5%.",
            ),
            (
                "A stop order guarantees the planned maximum loss:",
                [
                    "For every liquid stock",
                    "Only if the model is accurate",
                    "No; gaps and execution can exceed the planned distance",
                ],
                2,
                "A trigger is not a guaranteed execution price.",
            ),
            (
                "A $240 risk budget and $4 distance permit 60 shares; a separate name cap permits 45. Which cap binds?",
                ["60 shares", "45 shares", "105 shares"],
                1,
                "All independent limits must hold, so use the smaller quantity.",
            ),
        ],
    )

    teach(
        "5.15",
        4,
        "Portfolio exposure and outstanding commitments",
        "Aggregate correlated positions and open-order commitments before approving a new trade.",
        "A collection of individually acceptable orders can violate the account's overall limits. Calculate projected cash and holdings after outstanding commitments, then test gross exposure, net exposure, single-name concentration, sector concentration, and any factor budgets supported by reliable estimates. Different measures detect different failure modes.\n\nFor a long-only account, net and gross dollar exposure coincide, but sector and name concentration still differ. A future long/short extension cannot assume that netting removes liquidity or margin risk. An exposure estimate also needs a declared mark and stale-price policy.",
        "Harbor's $100,000 account holds $12,000 in one name and has an accepted $5,000 buy outstanding. A proposed additional $4,000 would produce $21,000 projected exposure. It breaches a stipulated 20% name limit even though the current holding is only 12%. The maximum extra notional under this cap is $3,000 before fee and price buffers.\n\nTwo $10,000 positions in different companies may still create $20,000 exposure to the same industry. Splitting orders across names does not necessarily diversify the underlying economic risk.",
        "Recompute reservations atomically with acceptance, so two simultaneous proposals cannot both consume the same remaining budget. Revalue after material price changes; a limit that held at submission can be exceeded by the market without any new order. Such a breach should trigger the declared review or reduction policy, not rewrite historical acceptance records. Test concurrent buys, opposite-side commitments, and a stale mark.",
        r"w_{projected}=(N_{held}+N_{pending}+N_{new})/E",
        'equity = 100000\nprint("Projected name weight:", (12000 + 5000 + 4000) / equity)\nprint("Remaining name budget:", equity * 0.20 - 12000 - 5000)',
        "An account worth $80,000 has $8,000 held and $3,000 pending in a name capped at 15%. Compute additional allowed notional before other constraints.",
        "The cap is $12,000; $11,000 is already held or committed, leaving $1,000. Fees, execution price buffers, and other portfolio limits can reduce it further.",
        [
            (
                "Exposure limits should evaluate:",
                [
                    "Only filled holdings",
                    "Holdings plus outstanding commitments and the proposed order",
                    "Only today's profit",
                ],
                1,
                "Accepted unfilled orders can still create future exposure.",
            ),
            (
                "Two different stocks in one industry necessarily remove sector concentration:",
                ["True", "Only on a large exchange", "False"],
                2,
                "Different issuers may share the same economic driver.",
            ),
            (
                "A $50,000 account has a 10% name cap, $3,000 held, and $1,500 pending. Remaining cap is:",
                ["$500", "$2,000", "$5,000"],
                0,
                "5,000−3,000−1,500 = 500.",
            ),
        ],
    )

    teach(
        "5.16",
        4,
        "Pre-trade gates and invariants",
        "Make invalid prices, stale data, unavailable cash, and policy breaches fail before order acceptance.",
        "A risk gate evaluates a typed proposal against a consistent account and market snapshot. Validate the schema first: known instrument, supported side, positive integer quantity, finite positive price, and an allowed order type. Then validate freshness and session eligibility, followed by cash, shares, exposure, and halt policy. A malformed number must never participate in arithmetic as if it were valid.\n\nCollect explicit rejection reasons rather than replacing invalid input with zero. The exact evaluation order is an implementation choice, but every mandatory condition must hold. Keep model confidence outside this permission boundary: confidence can influence a proposed target, while the gate owns hard limits.",
        "Available cash is $1,000, a buy price cap is $100, and commission is 10 bps. Ten shares require $1,001, so the order fails cash validation. Nine require $900.90 and fit that constraint. They still need to pass all other gates.\n\nA quote can have an acceptable price and insufficient freshness. An order can fit the name limit and exceed the sector limit. Passing one gate is not a general approval.",
        "Write assertions over all accepted orders: projected cash never becomes negative under the fill-price cap; cumulative fills never exceed authorized quantity; sell reservations never exceed owned shares. Mutate one input at a time to test each rejection. The lab's market-event flag and price cap are explicit simplifications, with no exchange calendar or broker connection. Keep an invariant failure visible and halt further mutations until the state is reconciled.",
        r"qP_{cap}+Fee(q,P_{cap})\leq C_{available}",
        'cash = 1000\nprint("Ten-share cash need:", 10 * 100 * 1.001)\nprint("Nine-share cash need:", 9 * 100 * 1.001)\nprint("Ten permitted by cash:", 10 * 100 * 1.001 <= cash)',
        "Design five rejection fixtures: future quote, zero quantity, insufficient fee-inclusive cash, excess name exposure, and an active halt. State the expected reason for each.",
        "Each fixture should fail its named gate while other inputs remain valid. An accepted control fixture proves the system is not merely rejecting every proposal.",
        [
            (
                "Ten shares cost $1,000 before a $1 fee with $1,000 available. Cash validation should:",
                [
                    "Accept because principal fits",
                    "Reject or resize under policy",
                    "Discard the fee",
                ],
                1,
                "The fee-inclusive commitment exceeds available cash.",
            ),
            (
                "A model gives confidence 0.99 on a stale quote. The hard freshness rule:",
                ["Still applies", "Is waived", "Becomes a price prediction"],
                0,
                "Model confidence does not authorize bypassing execution policy.",
            ),
            (
                "A proposed quantity is negative but its absolute notional fits the budget. The gate should:",
                [
                    "Turn it into a buy silently",
                    "Accept as a hedge",
                    "Reject the malformed proposal",
                ],
                2,
                "Side and positive quantity are separate validated fields.",
            ),
        ],
    )

    teach(
        "5.17",
        4,
        "Halts, loss limits, and controlled resumption",
        "Design a persistent operating-state machine that separates stopping new risk from managing existing exposure.",
        "Define states such as running, new-risk halted, reconciling, and disabled. A loss threshold, stale feed, ledger mismatch, or unknown external order may require different actions, but each transition needs a recorded reason. A halt must survive restart; otherwise reboot becomes an accidental permission reset.\n\nStopping new risk does not guarantee that all orders disappeared or that positions are flat. Cancel outstanding entries through the order manager and reconcile their actual results. A reduction order still needs valid quantity, price, session, and execution controls; an emergency label is not a license to corrupt the ledger.",
        "A session begins with equity $100,000 and later marks at $97,400. The session loss is 2.6%, crossing Harbor's illustrative 2.5% halt threshold. Peak-to-trough drawdown would use a different denominator if equity had first risen above $100,000. Decide which measure the policy means.\n\nIf equity rebounds to $98,000, a latched halt remains active until an explicit review and resume event. Automatic oscillation around the boundary can produce repeated stop-and-start trading.",
        "Write a resumption checklist tied to evidence: current balances reconcile, unknown orders are resolved, input freshness is restored, the triggering defect is understood, and a permitted reviewer records the release. Test restart while halted, a fill arriving during the halt, and an attempted unreviewed resume. The educational project offers an explicit resume method for experiments; it is not a multi-user approval system.",
        r"L_{session}=1-E_t/E_{start}",
        'loss = 1 - 97400 / 100000\nprint("Session loss percent:", round(loss * 100, 2))\nprint("Halt threshold crossed:", loss >= 0.025)',
        "Compare a session-loss measure from $100,000 with a drawdown from a $105,000 peak when current equity is $99,000. Specify a persistent halt policy.",
        "Session loss is 1%; peak drawdown is about 5.714%. Name the actual measure and denominator. Latch the halt, reconcile fills, and require an explicit evidence-backed resume event.",
        [
            (
                "A latched halt should survive:",
                ["Only one quote", "Only the current chart tab", "A process restart"],
                2,
                "A restart must not erase the risk state.",
            ),
            (
                "A halt means every pending order is instantly canceled:",
                ["False", "True", "True for any paper adapter"],
                0,
                "Cancellation is a separate action whose outcome must be reconciled.",
            ),
            (
                "Equity starts at $40,000 and falls to $38,800. Session loss is:",
                ["1.2%", "3%", "12%"],
                1,
                "1−38,800/40,000 = 3%.",
            ),
        ],
    )

    teach(
        "5.18",
        5,
        "Labels, overlapping horizons, and time splits",
        "Construct prediction targets without allowing future labels or fitted preprocessing to leak into evaluation.",
        "A label has an observation time and an end time: a five-day forward return becomes fully known five days later. Features at a decision time must use only information available then. Training rows whose labels extend into the evaluation interval can carry future information across an apparently chronological boundary.\n\nUse forward validation with a training cutoff that respects label availability. Purge overlapping label intervals when necessary. A fixed gap in a time-series splitter is convenient for fixed horizons, but it does not automatically identify variable event horizons or solve every dependence problem. An embargo is a separate exclusion interval; naming a split purged does not make it so.",
        "Validation begins at time index 10. Candidate training labels begin at 4, 6, and 8 and end three steps later at 7, 9, and 11. Under a strict end-before-validation rule, the first two are eligible; the row ending at 11 is excluded. Training data that starts before 10 can still contain a label unavailable at 10.\n\nA scaler is fitted on the eligible training features and then applied unchanged to validation. Fitting it on all dates leaks information even if the labels were properly separated.",
        "Save train, validation, and test index manifests with label intervals and data versions. Unit-test boundary cases where a label ends exactly at the cutoff and explicitly declare whether that endpoint is allowed. Tune only on development folds and retain a later frozen evaluation. Report the number of independent time periods, not just the number of overlapping rows.",
        r"\text{Eligible training row }i:\quad t^{label}_{end,i}<t^{validation}_{start}",
        'ends = [7, 9, 11]\neligible = 0\nfor end in ends:\n    if end < 10:\n        eligible = eligible + 1\nprint("Eligible training labels:", eligible)',
        "Validation starts at 20. Label ends are 17, 19, 20, and 23. Apply the strict rule and explain why a generic random split is unsuitable here.",
        "Only 17 and 19 qualify. The strict rule excludes the endpoint at 20. A random split can train on future outcomes and overlapping intervals relative to an earlier evaluation decision.",
        [
            (
                "A training feature is dated 8 but its forward label ends at 11; validation starts at 10. Under the strict rule it is:",
                ["Excluded", "Always valid", "A validation-free label"],
                0,
                "The outcome was not complete before validation began.",
            ),
            (
                "A fixed gap automatically purges every variable-horizon label:",
                ["Always", "Only for stocks", "No; inspect actual label intervals"],
                2,
                "A fixed number of rows need not cover variable endpoint overlap.",
            ),
            (
                "Validation starts at 30 and label ends are 27, 29, 31. How many meet end < 30?",
                ["One", "Two", "Three"],
                1,
                "Ends 27 and 29 qualify; 31 does not.",
            ),
        ],
    )

    teach(
        "5.19",
        5,
        "Baselines and prediction-to-position mapping",
        "Compare simple predictive baselines and convert model output into a bounded decision under trading costs.",
        "Start with an explicit no-skill baseline: a training mean for regression or a training base rate for classification. A complex model must improve a relevant out-of-sample objective, not merely fit the training data. Compare squared error, calibration where relevant, ranking quality, and eventual cost-aware decisions without conflating them.\n\nA prediction in return units can be compared with estimated trading costs. A rank cannot directly be treated as a return magnitude, and a probability of a positive return does not state the size of wins or losses. Define the mapping from model output to target before evaluating the holdout.",
        "Observed validation returns are 1% and −1%. The zero-return baseline has mean squared error 0.0001. Predictions of 0.8% and −0.6% have MSE 0.00001, improving this tiny illustrative sample. Two rows are insufficient evidence of durable performance.\n\nIf a proposed trade has expected benefit 8 bps and estimated nonoverlapping cost 6 bps, only 2 bps remain before model uncertainty. Harbor may require an additional margin or abstain. Position size is capped by deterministic risk logic even if the prediction is large.",
        "Log the baseline, prediction units, evaluation dates, costs, turnover, and target mapping. Inspect whether apparent gains come from one outlier or one regime. A ranking model may be assessed with cross-sectional rank correlation, but time-series dependence and universe construction still affect inference. Keep predictive evaluation and portfolio simulation as separate evidence artifacts.",
        r"MSE=n^{-1}\sum_i(y_i-\hat y_i)^2",
        'actual = [0.01, -0.01]\npredicted = [0.008, -0.006]\nerror = 0\nfor i in range(2):\n    error = error + (actual[i] - predicted[i]) ** 2\nprint("Model MSE:", error / 2)\nprint("Zero baseline MSE:", 0.0001)',
        "Compare forecasts 0.02 and 0 against actual returns 0.01 and −0.01 using MSE. Explain why a lower MSE need not produce higher net profit.",
        "MSE is 0.0001, equal to the zero baseline for these observations. Trading depends on thresholds, position sizes, payoff asymmetry, turnover, and costs as well as prediction error.",
        [
            (
                "A probability of a positive return directly tells you:",
                [
                    "The full payoff distribution",
                    "The predicted sign probability under the model",
                    "The permitted leverage",
                ],
                1,
                "It does not specify gain and loss magnitudes or risk limits.",
            ),
            (
                "A return forecast of 8 bps faces 6 bps estimated cost. Pre-uncertainty net estimate is:",
                ["2 bps", "6 bps", "14 bps"],
                0,
                "Subtract the distinct costs.",
            ),
            (
                "A model improves MSE but trades much more often. What is still required?",
                [
                    "Assume profit increased",
                    "Discard the benchmark",
                    "Evaluate its fixed decision rule with costs",
                ],
                2,
                "Predictive accuracy and realized economic performance are different objectives.",
            ),
        ],
    )

    teach(
        "5.20",
        5,
        "Boosted trees and defensible constraints",
        "Develop a nonlinear model with controlled complexity, time-aware selection, and documented feature assumptions.",
        "Boosting adds learners that correct the current model under a specified loss. Depth, learning rate, number of rounds, minimum leaf support, and regularization influence complexity. More rounds can improve training loss while degrading later performance. Use a chronologically valid validation set for early stopping and preserve the chosen iteration with the model artifact.\n\nA monotonic constraint imposes a direction on a model's response to a selected feature while other inputs are held fixed. It expresses a modeling assumption. It does not prove that a financial relationship is universally monotonic, causal, or stable across regimes. Forcing an unjustified relationship can reduce accuracy.",
        "Validation losses over five training checkpoints are 0.90, 0.75, 0.71, 0.73, and 0.78. Under this illustrative selection rule, checkpoint three is preferred. Choosing checkpoint five merely because it trained longest ignores the validation evidence. The final test set must not become another tuning input.\n\nHarbor considers a positive constraint on a quality score. Before adopting it, the team documents the score's definition, tests an unconstrained baseline, and checks whether the same feature meaning survives revisions. A renamed or rescaled feature is not automatically compatible with an old constraint vector.",
        "The in-app worksheet illustrates model selection arithmetic; it does not train XGBoost. For an optional external extension, pin a supported library version, save feature order and constraints, inspect that version's early-stopping prediction behavior, and reproduce the result from a clean environment. Report the validation manifest and rejected variants. The later standard-library project trains a small ridge model to make the fit/evaluate boundary runnable without extra dependencies.",
        r"m^*=\arg\min_m L_{validation}(m)",
        'losses = [0.90, 0.75, 0.71, 0.73, 0.78]\nbest = 0\nfor i in range(1, 5):\n    if losses[i] < losses[best]:\n        best = i\nprint("Selected checkpoint:", best + 1)\nprint("Selected loss:", losses[best])',
        "Select among validation losses 0.8, 0.7, 0.72, and 0.76. Write one financial monotonicity assumption and a test that could cause you to reject it.",
        "Checkpoint two has the lowest loss. A proposed constraint needs a documented feature meaning and comparison with an unconstrained model on development folds; economic intuition alone is not evidence that the constraint helps.",
        [
            (
                "Early stopping should select using:",
                [
                    "The final test labels repeatedly",
                    "A valid development validation set",
                    "The longest training run",
                ],
                1,
                "Keep final evaluation separate from model selection.",
            ),
            (
                "A monotonic constraint establishes financial causality:",
                ["No", "Yes", "Only with many trees"],
                0,
                "It constrains a fitted function, not the data-generating process.",
            ),
            (
                "Validation losses are 0.6, 0.5, 0.52. Which checkpoint has minimum loss?",
                ["First", "Third", "Second"],
                2,
                "The second checkpoint has loss 0.5.",
            ),
        ],
    )

    teach(
        "5.21",
        5,
        "Calibration, thresholds, and drift",
        "Evaluate probability quality and monitor changes in data, predictions, and delayed outcomes.",
        "Calibration asks whether predicted probabilities agree with observed frequencies in comparable cases. Discrimination asks whether the model separates outcomes. A proper score such as Brier loss reflects more than calibration alone, so a lower score is not a pure proof of better calibration. Inspect reliability bins with counts and uncertainty as well as aggregate scores.\n\nFit a calibration transform using development data separate from the base model's fitting observations, under a valid time design. Never calibrate on the final holdout and then report that same holdout as untouched. A calibrated probability still needs a payoff and cost model before becoming a trading decision.",
        "Predictions 0.8 and 0.3 face outcomes 1 and 0. The Brier score is ((0.8−1)² + (0.3−0)²)/2 = 0.065. A constant 0.5 forecast scores 0.25 on these two observations. This is an arithmetic comparison, not enough data to establish calibration.\n\nIf a winning trade gains 1 unit and a losing trade loses 1, expected gross payoff is 2p−1. With a cost of 0.1 units per trade, break-even requires p above 0.55 under those stipulated payoffs. Different loss sizes change the threshold.",
        "Monitor feature missingness, schema changes, prediction distribution, abstention frequency, and eventually realized label quality. Covariate drift does not necessarily imply performance failure; stable inputs do not prove stable outcomes either. Outcomes arrive late, so distinguish immediate operational alerts from delayed predictive monitoring. A drift alert should trigger a declared review or fallback; it should not silently retrain and promote a model.",
        r"BS=n^{-1}\sum_i(p_i-y_i)^2",
        'print("Brier score:", ((0.8 - 1) ** 2 + (0.3 - 0) ** 2) / 2)\nprint("Symmetric payoff threshold:", (1 + 0.1) / 2)',
        "Compute Brier loss for probabilities 0.6 and 0.4 against outcomes 1 and 0. Name an immediate input alert and a delayed outcome measure.",
        "The score is 0.16. Missing-feature rate is available immediately; realized Brier loss requires the prediction horizon to finish. Neither two examples nor one aggregate score establishes robust calibration.",
        [
            (
                "Brier score measures only calibration and nothing else:",
                ["True", "False", "True for probabilities below 0.5"],
                1,
                "It also reflects discrimination and outcome uncertainty.",
            ),
            (
                "A drift alert should automatically authorize a new live model:",
                [
                    "No; promotion needs the declared evaluation process",
                    "Yes",
                    "Only if its training score rises",
                ],
                0,
                "Detection and model release are separate decisions.",
            ),
            (
                "For p=0.7 and outcome 1, the individual Brier loss is:",
                ["0.3", "0.49", "0.09"],
                2,
                "Square the forecast error: (0.7−1)² = 0.09.",
            ),
        ],
    )

    teach(
        "5.3",
        6,
        "AI decision layers and authority boundaries",
        "Assign useful research tasks to AI while keeping order permissions and risk limits outside model-generated text.",
        "An AI component can summarize evidence, extract candidate facts, classify documents, or draft a research rationale. A deterministic controller validates these outputs and decides whether they are usable. Separate a research recommendation from an authorized target, and keep both separate from broker submission.\n\nA multi-agent committee can provide different analytical perspectives, but agreement is not independence when agents share the same model, prompt, or source error. More discussion does not convert missing evidence into a fact. Start with a small bounded workflow and add autonomous steps only when their benefit can be evaluated.",
        "An AI analyst proposes a 30% position with a confidence score of 0.9. Harbor's fixed single-name cap is 10%. The proposal is rejected or resized under the declared deterministic policy. The model's explanation cannot override the cap, and confidence is not an authenticated permission.\n\nA second proposal includes a plausible conclusion but no source identifier for its revenue figure. The research controller marks the required evidence missing and abstains. Passing numeric risk checks does not repair an unsupported premise.",
        "Define a narrow input/output contract: task, document identifiers, allowed fields, uncertainty or missing status, and an explanation linked to evidence. Keep API secrets and trading tools out of document-analysis context. Evaluate correctness, unsupported claims, abstentions, latency, and cost against a deterministic or human-reviewed baseline. The downloadable AI lab uses fixed fictional responses to test validation; it does not call an AI provider or imply measured model accuracy.",
        r"q_{accepted}=RiskGate(Proposal,Account,Market,Policy)",
        'proposal_weight = 0.30\ncap = 0.10\nprint("Proposal exceeds cap:", proposal_weight > cap)\nprint("Maximum policy weight:", min(proposal_weight, cap))',
        "Design an AI analyst contract that can recommend further research but cannot submit orders. Explain how to handle a strong recommendation missing its source.",
        "Return structured candidate facts, source IDs, units, and uncertainty. The controller checks evidence and policy; a missing required source produces abstention. No model output grants a new tool permission.",
        [
            (
                "Which layer should enforce a hard exposure limit?",
                ["The LLM’s prose response", "A deterministic risk layer", "The chart renderer"],
                1,
                "Limits must be enforced by code outside the model's generated text.",
            ),
            (
                "Three agents repeat one unsupported claim from the same source. This is:",
                [
                    "Three independent confirmations",
                    "A broker instruction",
                    "Potentially one shared error",
                ],
                2,
                "Shared sources and models can create correlated mistakes.",
            ),
            (
                "A model recommends 18% exposure under a hard 7% cap. The controller must:",
                [
                    "Enforce the 7% cap or reject under policy",
                    "Accept because the prose is persuasive",
                    "Ask the model to disable the cap",
                ],
                0,
                "Authority remains in the deterministic permission and risk layer.",
            ),
        ],
    )

    teach(
        "5.22",
        6,
        "Filing retrieval and evidence records",
        "Build a point-in-time research packet that preserves document identity, reporting units, and claim provenance.",
        "Retrieval selects candidate evidence; generation interprets it. Store each document's issuer, filing type, reporting period, publication timestamp, revision identity, and retrieval provenance. A semantic match does not establish that a passage answers the question or was available at a historical decision time.\n\nChunk boundaries should retain headings and table context. A revenue number without currency, scale, period, or scope can be materially misleading. Keep the original document pointer and local source identifier so a reviewer can trace the candidate fact. Access and redistribution rights for stored documents remain separate from their usefulness as evidence.",
        "A fictional Harbor filing published on March 15 reports prior-year revenue of 120 million currency units. It is eligible for an April 1 research decision but not a March 1 historical decision. An amended filing published April 20 cannot silently replace it in the April 1 record.\n\nThe analyst extracts 120 and tags the unit as millions. A controller normalizes it to 120,000,000 for a ratio calculation. If the accompanying text said thousands, the same digits would mean a thousandfold smaller amount. Preserve both the reported and normalized value.",
        "Test missing pages, conflicting revisions, ambiguous table headers, and a relevant-looking passage about the wrong issuer. Require an explicit not-found outcome. An evidence packet should include the question, allowed as-of time, candidate documents, supported fields, unresolved disagreements, and reviewer disposition. A citation points to a source; it does not prove that the generated claim follows from it.",
        r"Value_{base}=Value_{reported}\times UnitMultiplier",
        'reported = 120\nprint("Revenue in base units:", reported * 1000000)\nprint("Available on March 1:", 15 <= 1)',
        "Draft evidence metadata for a May 10 release used in a May 1 backtest decision. Explain the exclusion and how a later amendment is represented.",
        "Exclude it from May 1 because it was unavailable. Keep each revision with its own publication timestamp and ID; a later decision may use the amendment without rewriting earlier evidence.",
        [
            (
                "A March 15 release can enter a March 1 historical decision:",
                [
                    "Yes, because it reports last year",
                    "No, it was not yet available",
                    "Yes, if retrieved today",
                ],
                1,
                "Publication availability determines the historical information set.",
            ),
            (
                "Reported 120 in millions normalizes to:",
                ["120,000,000", "120,000", "120"],
                0,
                "Multiply by one million.",
            ),
            (
                "A later amended filing disagrees with the version used in an earlier decision. The audit record should:",
                [
                    "Erase the old version",
                    "Pretend both were available earlier",
                    "Preserve both versions with their availability times",
                ],
                2,
                "Point-in-time reconstruction requires the original evidence set.",
            ),
        ],
    )

    teach(
        "5.23",
        6,
        "Structured extraction and numeric validation",
        "Validate AI-extracted facts beyond JSON syntax by checking provenance, units, scope, and arithmetic.",
        "A schema can require fields and restrict types; it cannot guarantee that a value is true. Validate source membership, instrument identity, reporting period, allowed units, numeric finiteness, and consistency with the supplied evidence. Reject unknown fields when they could be interpreted as instructions or unauthorized actions.\n\nKeep reported facts separate from derived ratios and judgment. Let deterministic code compute ratios from validated inputs, with explicit zero-denominator and missing-value behavior. Avoid using a generated ratio when the underlying numerator and denominator are available for verification.",
        "A fictional evidence record states current revenue 120 million and prior revenue 100 million. The computed growth is 20%. A generated response of 200% has valid numeric syntax but fails arithmetic reconciliation. A response saying 120 thousand fails its unit contract even though its raw number matches.\n\nIf prior revenue is zero, percentage growth under this formula is undefined. The controller should return a missing or not-applicable result with a reason instead of producing an infinite score that might dominate position sizing.",
        "Build accepted and rejected fixtures before connecting a provider. Include a fabricated source ID, mixed currencies, a future filing, an omitted field, a zero denominator, and unsupported instructions embedded in a note. Measure false acceptance as well as extraction completeness. The offline fixture project demonstrates strict comparison against supplied records; general document interpretation still requires a separately evaluated extraction system.",
        r"g=Revenue_{current}/Revenue_{prior}-1",
        'current = 120\nprior = 100\nprint("Verified growth percent:", (current / prior - 1) * 100)\nclaimed = 2.0\nprint("Claim reconciles:", abs(claimed - (current / prior - 1)) < 0.000001)',
        "Revenue rises from 80 to 92 in the same units and scope. Compute growth and write rejection reasons for a different currency or an unknown source ID.",
        "Growth is 15%. Currency mismatch prevents direct comparison; an unknown source ID prevents provenance verification. Valid JSON alone resolves neither issue.",
        [
            (
                "A valid JSON number proves factual accuracy:",
                ["Yes", "No", "Only when rounded"],
                1,
                "Syntactic validation does not establish evidence support.",
            ),
            (
                "A prior revenue denominator of zero should produce:",
                [
                    "An explicit undefined or not-applicable result",
                    "Infinite trading conviction",
                    "A silently substituted value of one",
                ],
                0,
                "The ratio is undefined under this formula.",
            ),
            (
                "Revenue rises from 200 to 230 with consistent units. Verified growth is:",
                ["30%", "1.5%", "15%"],
                2,
                "Divide by the prior revenue base: 230/200−1 = 15%.",
            ),
        ],
    )

    teach(
        "5.24",
        6,
        "Agent tools, prompt injection, and evaluation",
        "Keep untrusted retrieved text from changing tool permissions and test bounded AI workflows against adversarial fixtures.",
        "A retrieved filing, webpage, tool response, or agent message is data, even when it contains imperative language. A passage that says ignore the risk policy does not acquire authority because it appears in a source document. Enforce allowed operations in application code, with narrow tool arguments and task-scoped permissions.\n\nUse a bounded workflow: retrieve approved documents, extract candidate facts, validate evidence, draft a memo, and submit for review. Set maximum calls, elapsed time, and output size. A recursive agent loop without a budget can fail operationally even if every individual response is harmless. Secrets and broker capabilities do not belong in a read-only research worker.",
        "Harbor budgets four analysis calls at an illustrative $0.03 each, for $0.12 maximum modeled call cost. A fifth requested call is stopped by the controller. An embedded source instruction requesting a cash transfer is recorded as untrusted content and has no corresponding allowed tool.\n\nThe evaluation suite includes supported extraction, missing evidence, fabricated citations, conflicting filings, prompt injection, malformed output, and provider timeout. Score whether the workflow produces the expected decision and evidence, not whether its prose sounds confident.",
        "Test defenses outside the prompt: reject disallowed tool names, constrain schemas, preserve a permission boundary, and verify that rejected requests create no state changes. Prompt instructions can help the model behave but are not an access-control mechanism. A timeout should lead to a declared fallback or abstention, never a stale recommendation promoted as fresh. Track false acceptance, unsupported claims, correct abstention, latency, and cost separately.",
        r"Cost_{budget}=N_{calls,max}\times Cost_{call,assumed}",
        'print("Illustrative call budget:", 4 * 0.03)\nrequested_calls = 5\nprint("Within call limit:", requested_calls <= 4)',
        "Write an adversarial filing fixture containing an instruction to override exposure limits. State the expected tool behavior and the evidence you would inspect.",
        "Treat the instruction as source content. The research worker has no execution capability, the controller rejects any disallowed operation, and account/order state remains unchanged. Inspect tool logs and state, not merely a refusal sentence.",
        [
            (
                "A retrieved document instructs the system to override its tool policy. It is:",
                [
                    "A higher-priority instruction",
                    "A trusted broker command",
                    "Untrusted source content",
                ],
                2,
                "Retrieved material does not grant application permissions.",
            ),
            (
                "The strongest evidence that a forbidden tool did not run is:",
                [
                    "A polite model response",
                    "Controller logs and unchanged relevant state",
                    "The model's confidence score",
                ],
                1,
                "Verify the enforced boundary and actual effects.",
            ),
            (
                "A workflow has a three-call budget and requests a fourth. The controller should:",
                [
                    "Enforce the limit and use its declared fallback",
                    "Let the model redefine the limit",
                    "Remove the audit record",
                ],
                0,
                "Resource budgets are application policy, not model suggestions.",
            ),
        ],
    )

    teach(
        "5.25",
        7,
        "Async queues, backpressure, and retry budgets",
        "Prevent slow consumers and ambiguous writes from turning transient failures into duplicated work or stale decisions.",
        "An asynchronous pipeline needs bounded queues and an overload policy. Waiting for queue capacity creates backpressure; dropping or coalescing observations is a separate policy that may be appropriate for some quote updates but not for authoritative fills. A queue is not a durable ledger, and process-local async coordination does not automatically coordinate threads or machines.\n\nClassify operations before retrying. Repeating a read is different from resubmitting an order whose outcome is unknown. Bound attempts, use a total deadline, and apply jitter where appropriate to avoid synchronized retries. Reconcile an ambiguous write before deciding whether it can be repeated.",
        "A consumer handles 80 events per second while a producer supplies 100. Backlog grows by 20 per second. A queue with 200 free slots fills in roughly 10 seconds under those constant rates. An unlimited queue hides the overload in rising latency and memory use.\n\nA sequence of retry delays 1, 2, and 4 seconds consumes seven seconds before considering request duration. If the decision expires after five seconds, the planned retry schedule is already inconsistent with its freshness budget.",
        "Measure queue depth and age of the oldest event, not just CPU use. Define priority and preservation rules for fills, cancellations, and observations. Use structured shutdown: stop new proposals, drain or persist authoritative events, reconcile orders, and close resources. The synchronous offline lab isolates accounting first; an async extension must preserve the same invariants across task cancellation and process failure.",
        r"t_{full}=Capacity_{free}/(Rate_{in}-Rate_{out})",
        'print("Seconds until queue full:", 200 / (100 - 80))\nprint("Retry waiting seconds:", 1 + 2 + 4)',
        "With 300 free slots and arrival/service rates 150/120 per second, compute time to saturation. Explain which events you would never silently drop.",
        "The queue fills in 10 seconds. Fills and authoritative order-state events require durable preservation or reconciliation; quote coalescing needs an explicit decision policy.",
        [
            (
                "An unbounded queue under sustained overload tends to:",
                [
                    "Grow latency and memory use",
                    "Increase consumer capacity automatically",
                    "Guarantee fresh decisions",
                ],
                0,
                "It stores the mismatch instead of resolving it.",
            ),
            (
                "An order-submission timeout is safe to retry blindly:",
                ["Always", "No; reconcile its potentially accepted state", "Only after one second"],
                1,
                "The response can be lost after acceptance.",
            ),
            (
                "Free capacity 120, arrivals 90/s, service 60/s. Time to full is:",
                ["2 seconds", "30 seconds", "4 seconds"],
                2,
                "Backlog grows by 30 per second; 120/(90−60) = 4 seconds.",
            ),
        ],
    )

    teach(
        "5.26",
        7,
        "Durable state and crash recovery",
        "Use transactions and stable identities to reconstruct orders, fills, and risk state after interruption.",
        "Persist the decision identity, immutable order payload, fills, and risk-state transitions. A uniqueness constraint prevents the same identity from creating multiple local records; a payload comparison detects a conflicting reuse of that identity. Merely returning the old result for a changed payload hides a caller defect.\n\nAn atomic transaction should encompass all local ledger changes caused by a fill. If the process stops midway, recovery sees either the committed fill and its effects or neither. This does not create an atomic transaction with an external broker: network submission still needs an intent record, stable external identifiers, and reconciliation.",
        "Fill F1 buys 10 shares for $1,000 plus a $1 fee. Applying it twice under the same unchanged fill identity must leave one ledger entry, a $1,001 cash reduction, and 10 shares. Reusing F1 for 12 shares is a conflict, not another fill.\n\nAfter a restart, the bot reads its persisted halt state before accepting a proposal. Reconstructing current holdings from durable fills provides an independent check against the cached account row. A disagreement blocks further trading until investigated.",
        "Test a restart after order acceptance, after a partial fill, and while halted. Include transaction rollback and duplicate delivery fixtures. Keep schema migrations and model versions explicit. The downloadable SQLite lab uses local transactions and uniqueness, and demonstrates reopening the same database; it does not claim exactly-once execution across an external service boundary.",
        r"State_{recovered}=Fold(State_0,UniqueCommittedFills)",
        'initial_cash = 10000\nunique_fill_count = 1\nprint("Cash after unique fill:", initial_cash - unique_fill_count * 1001)\nprint("Recovered shares:", unique_fill_count * 10)',
        "Describe a conflict test where the same fill ID arrives with a different quantity, and a restart test that proves a halt survives.",
        "The conflict must reject with no account mutation. Close and reopen the same database after halting, then verify a new-risk proposal is rejected and the stored halt reason remains visible.",
        [
            (
                "A reused fill ID with changed quantity should:",
                ["Overwrite history", "Book the difference silently", "Raise a conflict"],
                2,
                "Stable identity refers to an immutable economic event.",
            ),
            (
                "A local database transaction also atomically commits an external broker order:",
                ["False", "True", "True when IDs are strings"],
                0,
                "The external service is a separate failure boundary.",
            ),
            (
                "One unique fill buys 5 shares for $250 plus $0.25 fee from $1,000. Replaying it unchanged leaves cash:",
                ["$499.50", "$749.75", "$750.00"],
                1,
                "The fill is booked once: 1,000−250−0.25.",
            ),
        ],
    )

    teach(
        "5.27",
        7,
        "Observability and incident response",
        "Instrument decision traces and operational invariants so incidents can be detected and reconstructed.",
        "Link market event, feature version, model version, intent, order, fill, and account update through stable correlation identifiers. Record decision reasons and timings while keeping secrets out of logs. A profit dashboard cannot explain whether a missing trade arose from absent data, an abstention, a risk rejection, or an order failure.\n\nSeparate operational measures from investment outcomes. Track data age, queue delay, rejected proposals, unknown orders, reconciliation mismatches, duplicate messages, fill latency, fees, and exposure. Performance measures require their own benchmark and horizon. A low error count can hide a component that stopped producing useful work.",
        "During a window with 200 proposals, 30 are rejected for stale data, 10 for risk caps, and 160 are accepted. The acceptance rate is 80%. That number alone does not tell whether the rejection policy is correct; review samples and expected fixture outcomes.\n\nIf accepted order count continues rising but no acknowledgements arrive, investigate the external-state gap rather than simply increasing retries. Unknown-order age is a more useful alert than another aggregate request-success percentage.",
        "Write a runbook with detection signal, immediate containment, evidence to preserve, reconciliation steps, and resumption criteria. Test it using a deliberate feed outage and a duplicate fill. Version configuration and deployment artifacts so the incident can be replayed. Access to logs, backups, and secrets should follow the actual operational roles; never paste a live token into a research notebook or a course exercise.",
        r"AcceptanceRate=N_{accepted}/N_{proposed}",
        'print("Acceptance rate:", 160 / 200)\nprint("Stale rejection rate:", 30 / 200)',
        "Draft a runbook for rising unknown-order age. Name an immediate action, three evidence records, and a condition for resuming proposals.",
        "Halt new risk under policy; retain intent IDs, broker lookup results, and recent fills/account snapshots. Resume only after ambiguous orders and balances reconcile and the communication cause is understood.",
        [
            (
                "A useful execution trace connects:",
                [
                    "Only final profit",
                    "Decision, order, fill, and account identities",
                    "Only the model's prose",
                ],
                1,
                "Correlated records support reconstruction of actual state transitions.",
            ),
            (
                "Zero logged errors guarantees a functioning strategy:",
                ["No", "Yes", "Only in paper mode"],
                0,
                "A stalled pipeline may produce neither useful work nor errors.",
            ),
            (
                "Of 250 proposals, 50 are rejected. Acceptance rate is:",
                ["20%", "50%", "80%"],
                2,
                "There are 200 accepted proposals; 200/250 = 80%.",
            ),
        ],
    )

    teach(
        "5.28",
        7,
        "Paper release gates and rollback",
        "Build an evidence-based promotion packet and practice rollback without confusing paper results with live readiness.",
        "A release gate is a declared acceptance condition with supporting evidence. Examples include passing ledger invariants, reproducing a frozen replay, reconciling partial fills after restart, and rejecting malformed or stale proposals. A paper profit threshold alone does not test operational correctness.\n\nFreeze the code, configuration, feature schema, model artifact, data version, and validation manifest together. Shadow evaluation can compare proposed decisions without executing them, while a paper canary tests a limited scope in a simulated environment. Neither automatically authorizes live deployment or demonstrates realistic liquidity.",
        "Harbor defines five mandatory gates: deterministic replay, correct fees and inventory, duplicate handling, persistent halt, and evidence-validation failures. A release passes four but fails persistent halt after restart. Its status is blocked under the declared policy even if the simulated return is positive.\n\nRollback restores a known software and model version, but it does not reverse fills that actually occurred. The restored process must reconcile current account state before resuming. Database schema compatibility is part of the rollback plan.",
        "Prepare a release record with artifact hashes, test results, known limitations, an owner, and rollback instructions. Run an incident rehearsal before promotion. Keep the paper evaluation scope and capital limits visible. Any later real broker integration requires its own adapter tests, access configuration, market-data permissions, and review; this course ends at an offline educational acceptance packet.",
        r"ReleaseEligible=\bigwedge_{j=1}^{k}Gate_j",
        'gates = [True, True, True, False, True]\npassed = 0\nfor gate in gates:\n    if gate:\n        passed = passed + 1\nprint("Gates passed:", passed)\nprint("Release eligible:", passed == len(gates))',
        "Write a five-gate release checklist and simulate rollback after a partial fill. Explain which state must be preserved across the rollback.",
        "All mandatory gates must pass. Preserve actual cash, inventory, fills, outstanding orders, and halt status; rollback changes software, not economic history.",
        [
            (
                "Four of five mandatory gates pass. Release status is:",
                [
                    "Eligible by majority",
                    "Eligible if profitable",
                    "Blocked by the failed mandatory gate",
                ],
                2,
                "Mandatory gates are conjunctive.",
            ),
            (
                "Rollback of a model version reverses executed fills:",
                ["No", "Yes", "Only before midnight"],
                0,
                "Executed economic events remain in the account ledger.",
            ),
            (
                "A paper canary passes. The supported conclusion is:",
                [
                    "Live execution is guaranteed equivalent",
                    "The tested paper conditions passed",
                    "Data licensing is no longer relevant",
                ],
                1,
                "Evidence is limited to the tested model and environment.",
            ),
        ],
    )

    teach(
        "5.29",
        8,
        "Project: a durable rule-based paper bot",
        "Run the downloadable event replay and prove that duplicate delivery, partial fills, and restart preserve the ledger.",
        f"Download the [offline Python lab]({PROJECT}) and its [project guide](/course-assets/stock-bots/README.md). Run it locally with Python 3.10 or later; it uses only the standard library and makes no network calls. The in-app worksheet below checks arithmetic, while the downloaded program runs the event and SQLite state machine.\n\nThe fixed rule observes completed closes 98, 99, and 100 and proposes ten shares because the last close exceeds their mean. A $100 buy limit constrains later fills. This is a deliberately tiny execution fixture, not a researched trading strategy. Policy values, synthetic events, immediate settlement, and fee rounding are declared in the project guide.",
        "Start with $10,000. Event E1 fills four shares at $100 with a $0.20 fee; its duplicate creates no additional fill. After closing and reopening the database, E2 fills the remaining six at $99 with a $0.30 fee. Cash is now $9,005.50 and holdings are ten shares. Replaying the first fill identity leaves both unchanged.\n\nThe lab halts new risk, reopens again, and verifies that an entry is rejected. A permitted reduction sells two shares at $102 with a $0.11 fee. Final cash is $9,209.39, shares are eight, and equity marked at $102 is $10,025.39.",
        "Read the order, event, fill, and transition tables. Change one fixture at a time: duplicate an event, use a conflicting payload under its ID, offer a nonmarketable price, reduce volume, or cancel a remainder. Record the expected and actual state before reading the report. The toy matcher fills at the supplied event price up to eligible volume; it does not model exchange queue priority or realistic liquidity. Keep the halt active until an explicit, documented resume experiment.",
        r"E_{final}=9209.39+8(102)=10025.39",
        'cash = 10000 - 4 * 100 - 0.20 - 6 * 99 - 0.30 + 2 * 102 - 0.11\nprint("Project cash:", round(cash, 2))\nprint("Project equity:", round(cash + 8 * 102, 2))\nprint("Project fees:", 0.20 + 0.30 + 0.11)',
        "Run the downloaded project and preserve its output. Reconcile all three fills, then create a fresh fixture that cancels a partially filled buy. Show that the canceled remainder does not change owned shares.",
        "The default replay produces cash 920939 cents, 8 shares, equity 1002539 cents, fees 61 cents, three fills, zero open orders, and an active incident-rehearsal halt. For a cancellation fixture, book only actual fills and release the remaining reservation.",
        [
            (
                "The project finishes with cash $9,209.39 and eight shares marked $102. Equity is:",
                ["$10,025.39", "$9,311.39", "$10,000.00"],
                0,
                "Add the $816 marked inventory to cash.",
            ),
            (
                "The in-app arithmetic worksheet performs the SQLite replay:",
                [
                    "Yes",
                    "No; run the downloadable local project for that replay",
                    "Only after changing the chart",
                ],
                1,
                "The guided sandbox computes the worksheet; the separate standard-library program owns the event ledger.",
            ),
            (
                "An unchanged E1 event is replayed after its four-share fill. Expected additional shares are:",
                ["Four", "Ten", "Zero"],
                2,
                "Stable event and fill identities prevent duplicate booking.",
            ),
        ],
    )

    teach(
        "5.30",
        8,
        "Project: expanding-window machine learning",
        "Fit a small ridge model in two chronological folds and compare genuinely held-out predictions with a training-only baseline.",
        "The downloaded lab's ridge_walkforward function trains a one-feature ridge regression with an unpenalized intercept. For each cutoff it computes training means, centers the observations, estimates the slope with a fixed penalty of one, and predicts only the next unseen row. No external ML dependency is required.\n\nThe artificial observations obey y=1+2x for x values −2, −1, 0, 1, 2, and 3. Units are abstract; they are not market returns. This deliberately simple fixture makes chronology and coefficient shrinkage visible. It establishes that a training and evaluation pipeline runs correctly, not that a stock model has skill.",
        "The first fold trains on four rows. Centered cross-product is 10 and centered squared-feature sum is 5, so slope is 10/(5+1)=1.6667. Its intercept is 0.8333, and prediction at x=2 is 4.1667 versus actual 5. The training-mean baseline predicts zero.\n\nThe second fold trains on five rows, with slope 20/11=1.8182 and intercept 1. Its prediction at x=3 is 6.4545 versus actual 7; the training-mean baseline predicts one. Across these two held-out predictions the ridge MSE is about 0.495983, versus 30.5 for the baseline.",
        "Inspect the saved fold rows and verify that changing the final y value cannot alter either prediction. It can change the final evaluation error, because that is the correct role of a held-out outcome. For a financial extension, replace artificial inputs only after defining point-in-time features, label intervals, costs, and a frozen target mapping. Do not tune the penalty on these two final outcomes and continue calling them untouched.",
        r"\hat\beta=\frac{\sum(x_i-\bar x)(y_i-\bar y)}{\sum(x_i-\bar x)^2+\lambda}",
        'slope1 = 10 / 6\npred1 = slope1 * 2.5\nslope2 = 20 / 11\npred2 = 1 + slope2 * 3\nprint("First prediction:", pred1)\nprint("Second prediction:", pred2)\nprint("Walk-forward MSE:", ((pred1 - 5) ** 2 + (pred2 - 7) ** 2) / 2)\nprint("Baseline MSE:", (5 ** 2 + 6 ** 2) / 2)',
        "Reproduce both fold predictions. Then change only the last outcome from 7 to 8 and explain which fitted quantities must remain unchanged.",
        "Both fitted slopes and predictions stay unchanged because the last outcome is not used for training either fold. The second prediction's error and aggregate MSE change. Earlier observed outcomes may legitimately enter later expanding training windows.",
        [
            (
                "The first ridge slope with cross-product 10, squared-feature sum 5, and penalty 1 is:",
                ["2", "1.6667", "10"],
                1,
                "10/(5+1) = 1.6667.",
            ),
            (
                "Changing only the final held-out outcome should change:",
                [
                    "The already fitted slope",
                    "The earlier feature means",
                    "Evaluation error, not the existing prediction",
                ],
                2,
                "Held-out labels belong to scoring, not training.",
            ),
            (
                "A baseline predicts 0 and 1 against outcomes 5 and 7. Its MSE is:",
                ["30.5", "5.5", "61"],
                0,
                "((5−0)²+(7−1)²)/2 = 30.5.",
            ),
        ],
    )

    teach(
        "5.31",
        8,
        "Project: a verifiable AI research packet",
        "Test a deterministic evidence validator with accepted, fabricated, unavailable, and malformed model-response fixtures.",
        "The downloaded validate_fact function evaluates a fixed candidate response against a supplied fictional evidence record. It requires an exact field set, known source, matching issuer and period, allowed unit, finite numeric value, and an as-of date after availability. It then computes growth from the verified source values.\n\nThis is the validation half of an AI research workflow. The project does not call a language model or retrieve real filings. Fixed response fixtures make false acceptance testable without provider credentials. A later model integration would need its own extraction-quality evaluation and document access policy.",
        "Source HBR-2025-v1 is available at fixture time 15 and records revenue 120 and prior revenue 100 in USD millions. The candidate passes at time 20 and produces 20% growth. It fails at time 10 because the evidence is not yet available. Changing the source ID, value, unit, issuer, or period causes rejection.\n\nAdding an unexpected execute_order field also fails the strict schema. The research validator has no broker tool. This illustrates an enforced boundary whose outcome can be inspected in code and state, rather than relying on a generated promise to obey instructions.",
        "Create a labeled evaluation table before connecting a provider: supported fact, unknown source, wrong scale, future record, nonfinite number, extra instruction, and missing required field. Count correct acceptances and correct abstentions separately. Avoid making the validator permissive just to improve apparent completion rate. Keep the verified record and the source pointer together when writing the final research memo.",
        r"VerifiedGrowth=120/100-1=0.20",
        'print("Verified revenue:", 120)\nprint("Verified growth:", 120 / 100 - 1)\nprint("Source eligible at time 10:", 15 <= 10)\nprint("Source eligible at time 20:", 15 <= 20)',
        "Run one accepted response and six rejected variants against validate_fact. Preserve the expected reason and prove no order was created by the research validation calls.",
        "The unchanged candidate passes at time 20. Reject unknown source, future availability, wrong units, nonfinite value, extra field, and missing field. The validator returns a research record or raises an error and has no account mutation or broker capability.",
        [
            (
                "The offline AI fixture project measures a real provider's extraction accuracy:",
                [
                    "No; it tests validation against fixed candidate responses",
                    "Yes",
                    "Only when the result is bullish",
                ],
                0,
                "No provider is called, so no model-quality claim is supported.",
            ),
            (
                "A candidate adds an unauthorized execution field. The strict validator:",
                [
                    "Runs it after validating revenue",
                    "Rejects the unexpected field",
                    "Converts it to a larger target",
                ],
                1,
                "Schema and tool boundaries do not grant execution authority.",
            ),
            (
                "A source becomes available at time 40 and the decision is at 35. The validator should:",
                [
                    "Accept because it can be retrieved now",
                    "Infer an earlier publication",
                    "Reject it as unavailable at the decision time",
                ],
                2,
                "A valid identifier is insufficient without valid availability.",
            ),
        ],
    )

    teach(
        "5.32",
        8,
        "Capstone: bot acceptance and incident dossier",
        "Integrate the strategy contract, replay ledger, ML evaluation, AI evidence tests, and operational review into one defensible release packet.",
        "The final deliverable is a reproducible educational system and a written decision about its tested scope. Assemble the decision contract from Unit 1, rule and cost specification from Unit 2, order transition table from Unit 3, risk gates from Unit 4, split manifest from Unit 5, evidence-validation matrix from Unit 6, and incident runbook from Unit 7.\n\nRun the downloadable project from a clean environment and retain the code revision, fixture inputs, output, and assumptions. The paper rule, artificial ridge experiment, and fixed AI response tests are distinct experiments in one packet. Do not imply that the ridge or AI fixture has been validated as a live trading signal.",
        "The default paper replay reconciles to $10,025.39 equity, three fills, $0.61 fees, and an active halt. The artificial ridge comparison yields MSE about 0.495983 versus 30.5 for its baseline. The evidence validator accepts the supported 120-million revenue record and derives 20% growth. Each result answers a different acceptance question.\n\nSuppose an altered implementation reports the same final equity but creates two fills for E1 and later offsets them. The final number matches while event idempotency fails. Review both state invariants and the full transition trace; a favorable final balance cannot excuse invalid intermediate actions.",
        "Use a 100-point self-assessment: decision and data contract 15, execution and ledger evidence 25, risk and restart behavior 20, ML evaluation 15, AI evidence and permissions 15, and incident/release documentation 10. Require at least 80 points and no unresolved failure of cash/share conservation, duplicate handling, persistent halts, or source validation. The automatic final exam assesses conceptual transfer; it does not grade the code or written dossier. Conclude what the tests support, what remains simulated, and what experiment would challenge the weakest assumption next.",
        r"Score=15+25+20+15+15+10=100",
        'print("Project P&L:", 10025.39 - 10000)\nprint("Rubric total:", 15 + 25 + 20 + 15 + 15 + 10)\nscore = 88\ncritical_failure = True\nprint("Dossier accepted:", score >= 80 and not critical_failure)',
        "Submit the seven unit artifacts, reproducible project output, an adverse-event trace, a completed rubric, and a one-page release decision. Include at least one rejected design assumption and an unresolved simulation limitation.",
        "A sound packet reproduces the stated arithmetic and shows unchanged state after duplicates, rejection of invalid evidence and orders, correct partial-fill accounting, and a halt that survives restart. An 80+ score is insufficient while any critical invariant fails. Passing the concept exam alone does not establish project acceptance or live readiness.",
        [
            (
                "A dossier scores 88 but fails duplicate-fill handling. Under the rubric it is:",
                [
                    "Accepted because score exceeds 80",
                    "Accepted if profitable",
                    "Not accepted until the critical failure is resolved",
                ],
                2,
                "Critical invariants are mandatory in addition to the numeric score.",
            ),
            (
                "The automatic final exam grades the submitted local Python project:",
                [
                    "No; the written and code dossier is self-assessed separately",
                    "Yes",
                    "Only its final equity",
                ],
                0,
                "The exam measures conceptual transfer; project acceptance needs its own evidence.",
            ),
            (
                "A replay's final equity matches the expected value but intermediate cash becomes negative. The correct conclusion is:",
                [
                    "The ending number proves correctness",
                    "The invariant failure invalidates acceptance",
                    "Only the chart needs changing",
                ],
                1,
                "A valid final balance does not repair an invalid state transition.",
            ),
        ],
    )

    parts = [
        (
            "Specification, events, and data",
            "Decision contracts, event identities, market clocks, and reproducible features.",
        ),
        (
            "Rules and research evaluation",
            "Target reconciliation, trend and reversion hypotheses, chronology, and costs.",
        ),
        (
            "Execution and paper accounting",
            "Quotes, order lifecycles, slicing policies, cash, inventory, and fees.",
        ),
        (
            "Risk and operating controls",
            "Sizing, portfolio commitments, pre-trade gates, and persistent halts.",
        ),
        (
            "Machine learning for decisions",
            "Labels, time splits, baselines, nonlinear models, calibration, and drift.",
        ),
        (
            "LLM research and bounded agents",
            "Evidence retrieval, validated extraction, permissions, and adversarial evaluation.",
        ),
        (
            "Operations and release discipline",
            "Backpressure, durable recovery, observability, and paper release gates.",
        ),
        (
            "Projects and capstone",
            "Run the offline paper bot, fit a small ML model, validate AI fixtures, and assemble an acceptance dossier.",
        ),
    ]
    unit_sources = {
        "1": [
            ("Alpaca · Order identifiers and lifecycle", ORDERS),
            ("scikit-learn contributors · Consistent preprocessing", LEAKAGE),
        ],
        "2": [
            ("scikit-learn contributors · Leakage and evaluation pitfalls", LEAKAGE),
            ("Alpaca · Paper simulation assumptions", PAPER),
        ],
        "3": [
            ("Alpaca · Working with orders", ORDERS),
            ("Alpaca · Paper trading limitations", PAPER),
        ],
        "4": [
            ("Alpaca · Order lifecycle and execution constraints", ORDERS),
            ("Alpaca · Paper trading model", PAPER),
        ],
        "5": [
            ("scikit-learn contributors · TimeSeriesSplit and gaps", SPLITS),
            ("scikit-learn contributors · Common pitfalls", LEAKAGE),
        ],
        "6": [
            ("Anthropic · Building effective agents", AGENTS),
            ("Anthropic · Containing untrusted content", CONTAINMENT),
        ],
        "7": [
            ("Python Software Foundation · asyncio queues", QUEUES),
            ("Alpaca · Order lookup and reconciliation inputs", ORDERS),
        ],
        "8": [
            (
                "Python Software Foundation · sqlite3 transactions",
                "https://docs.python.org/3/library/sqlite3.html",
            ),
            ("scikit-learn contributors · Time-aware evaluation", SPLITS),
        ],
    }
    extra_sources = {
        "5.20": [("XGBoost contributors · Monotonic constraints", BOOSTING)],
        "5.21": [("scikit-learn contributors · Probability calibration", CALIBRATION)],
        "5.22": [("U.S. SEC · EDGAR company filings", "https://www.sec.gov/edgar/search/")],
        "5.4": [
            (
                "J. L. Kelly Jr. · A New Interpretation of Information Rate (1956)",
                "https://www.princeton.edu/~wbialek/rome/refs/kelly_56.pdf",
            )
        ],
    }
    for item in modules:
        item["references"] = [
            {"title": title, "url": url}
            for title, url in unit_sources[item["part"]] + extra_sources.get(item["id"], [])
        ]
        item["code"] = item["code"].replace(
            "valuation or statistical claim", "bot or model's performance"
        )

    # Each checkpoint uses a new transfer question per lesson, separate from practice and final.
    checkpoint_items = [
        (
            "A decision contract omits its information cutoff. What is unresolved?",
            [
                "Which inputs were available at decision time",
                "The app's font",
                "The number of chart colors",
            ],
            0,
            "The cutoff defines the permissible information set.",
        ),
        (
            "A broker accepted an order but the client crashed before storing the response. First recover:",
            [
                "A new random order",
                "The stable intent and external order state",
                "A different strategy name",
            ],
            1,
            "Reconcile the accepted or unknown order before another submission.",
        ),
        (
            "A quote is 800 ms old under a 500 ms policy. New entry should be:",
            ["Doubled", "Delayed without any record", "Rejected under the freshness rule"],
            2,
            "Its age exceeds the declared limit.",
        ),
        (
            "Feature schema v2 changes column order. An old model requires:",
            [
                "Explicit compatibility validation",
                "A larger sample after execution",
                "No changes because columns are numeric",
            ],
            0,
            "Feature order is part of the trained input contract.",
        ),
        (
            "Target 60, held 30, pending buy 20. Residual shares are:",
            ["30", "10", "50"],
            1,
            "Subtract both held and committed shares: 60−30−20 = 10.",
        ),
        (
            "Prior breakout high 50 and band 2% imply threshold:",
            ["49", "50", "51"],
            2,
            "The prior high plus the 2% band is 50×1.02 = 51.",
        ),
        (
            "Spread 18, training mean 12, scale 3 yields z:",
            ["2", "3", "6"],
            0,
            "(18−12)/3 = 2; this alone does not prove reversion.",
        ),
        (
            "Five shares bought at 40 and sold at 42 incur $0.41 fees. Net profit:",
            ["$10.41", "$9.59", "$2"],
            1,
            "Gross is $10; subtract the fee.",
        ),
        (
            "A sell executes below its decision midpoint. Direction-adjusted shortfall is:",
            ["Always favorable", "Zero", "Adverse before any offsetting effects"],
            2,
            "Receiving less than the sell benchmark is adverse under this convention.",
        ),
        (
            "An 80-share order fills 30 before cancellation completes. Canceled remainder is:",
            ["50", "30", "80"],
            0,
            "Only 80−30 = 50 remain to cancel.",
        ),
        (
            "A 3% participation cap on 2,000 eligible shares allows at most:",
            ["600", "60", "6"],
            1,
            "2,000×0.03 = 60, subject also to parent remainder.",
        ),
        (
            "$2,000 cash minus a $500 purchase and $0.50 fee leaves:",
            ["$1,500", "$2,500.50", "$1,499.50"],
            2,
            "Subtract both principal and fee.",
        ),
        (
            "A $90 stop-risk budget and $3 distance permit, before other caps:",
            ["30 shares", "90 shares", "270 shares"],
            0,
            "90/3 = 30; the stop is not a guaranteed loss bound.",
        ),
        (
            "A $6,000 name cap has $4,000 held and $1,000 pending. Additional budget:",
            ["$2,000", "$1,000", "$6,000"],
            1,
            "6,000−4,000−1,000 = 1,000.",
        ),
        (
            "An order fits cash but violates the instrument allowlist. It should:",
            ["Pass by majority", "Ignore the instrument", "Fail the mandatory gate"],
            2,
            "Every mandatory constraint must hold.",
        ),
        (
            "After a latched halt, a price rebound automatically resumes new risk:",
            ["No; use the explicit resume procedure", "Yes", "Only if the chart is green"],
            0,
            "The halt remains until its review and resume conditions are met.",
        ),
        (
            "Validation starts at 12; label ends 10, 11, 13 satisfy the strict cutoff for:",
            ["One row", "Two rows", "Three rows"],
            1,
            "Ends 10 and 11 are before 12.",
        ),
        (
            "A ranking score is treated as an expected return in dollars. This is:",
            ["Always appropriate", "A useful risk exemption", "A unit and interpretation error"],
            2,
            "Ranks have no direct return magnitude without a separately justified mapping.",
        ),
        (
            "A feature monotonicity prior hurts development validation consistently. Consider:",
            [
                "Revising or rejecting the constraint",
                "Claiming it proves causality",
                "Tuning on the final test until it helps",
            ],
            0,
            "Evaluate the prior rather than treating intuition as an unconditional law.",
        ),
        (
            "Predicted probability .9 and outcome 1 produce Brier loss:",
            [".1", ".01", ".81"],
            1,
            "Square the probability error: (.9−1)² = .01.",
        ),
        (
            "An AI research worker needs to summarize filings. Appropriate authority is:",
            [
                "Full broker access",
                "Permission to alter risk caps",
                "Only the bounded research tools it needs",
            ],
            2,
            "Research capability does not require execution permission.",
        ),
        (
            "A document reports 5 in thousands. Base-unit value is:",
            ["5,000", "5", "5,000,000"],
            0,
            "Preserve scale and normalize explicitly.",
        ),
        (
            "A ratio's inputs disagree on issuer. Validation should:",
            [
                "Average the issuers",
                "Reject the mismatch",
                "Ignore metadata if values are positive",
            ],
            1,
            "The values must refer to the intended entity and scope.",
        ),
        (
            "A source text asks the agent to expose a secret. The tool layer should:",
            [
                "Obey cited material",
                "Ask the document for permission",
                "Deny capabilities outside its allowed task",
            ],
            2,
            "Retrieved text does not authorize secret access.",
        ),
        (
            "Arrivals 60/s, service 40/s, free capacity 100. Saturation time:",
            ["5 seconds", "20 seconds", "100 seconds"],
            0,
            "Backlog grows by 20 per second; 100/(60−40) = 5 seconds.",
        ),
        (
            "The same intent ID is reused for a different price limit. Required behavior:",
            ["Overwrite the earlier order", "Reject the identity conflict", "Submit both"],
            1,
            "An identity is tied to an immutable intended payload.",
        ),
        (
            "A stalled feed yields no errors and no new events. Which measure helps detect it?",
            ["Only cumulative profit", "Only log file size", "Age of the latest valid observation"],
            2,
            "A freshness metric detects silence that error counters miss.",
        ),
        (
            "A rollback restores an older executable. Before resuming it must:",
            [
                "Reconcile current fills, orders, and account state",
                "Reset cash to initial capital",
                "Erase new fill IDs",
            ],
            0,
            "Software rollback must preserve actual economic history.",
        ),
    ]
    checkpoints = []
    for unit in range(7):
        rows = [(modules[i]["id"], q(*checkpoint_items[i])) for i in range(unit * 4, unit * 4 + 4)]
        checkpoints.append((f"Unit {unit + 1}: {parts[unit][0]}", rows))
    return finish(
        {
            "id": "stock-bots",
            "number": 5,
            "title": "Algorithmic & AI stock bots",
            "description": "Build a disciplined paper bot from first signal to durable execution, then evaluate machine learning and evidence-based AI research workflows.",
            "source": "Original Quanta engineering course · primary broker, Python, ML, and AI documentation",
            "level": "Advanced",
            "icon": "bot",
            "studyType": "applied",
            "modules": modules,
            "prerequisites": "Comfort with Python functions, lists, and basic probability. Complete Trading & market fundamentals and the strategy-evaluation units in Quantitative Investment Analysis first. The offline project requires Python 3.10+; no credentials or paid services are needed.",
            "outcomes": [
                "Specify point-in-time signals and reproducible evaluation contracts.",
                "Reconcile targets, pending orders, partial fills, cash, and inventory.",
                "Enforce deterministic sizing, exposure, freshness, and halt policies.",
                "Fit and evaluate a small chronological ML model without test leakage.",
                "Validate AI evidence and constrain tools outside generated text.",
                "Produce a replayable paper-bot project and an incident acceptance dossier.",
            ],
            "readingGuide": "Eight units, 32 original lessons, 64 practice questions, seven checkpoints, and a 32-question final. Complete the worksheet and written artifact in each lesson. The final unit includes a downloadable standard-library paper bot, an actual small ridge fit, and fixed AI response validation tests. These are offline educational projects, with explicit simulation assumptions; the written capstone is self-assessed separately from the automatic exam.",
            "parts": [
                {"id": str(i), "title": title, "description": description}
                for i, (title, description) in enumerate(parts, 1)
            ],
            "references": [
                {"title": title, "url": url}
                for title, url in [
                    ("Alpaca · Orders and client identifiers", ORDERS),
                    ("Alpaca · Paper trading assumptions", PAPER),
                    ("scikit-learn contributors · Model evaluation pitfalls", LEAKAGE),
                    ("Python Software Foundation · asyncio queues", QUEUES),
                    ("Anthropic · Building effective agents", AGENTS),
                ]
            ],
            "resources": [
                {"title": "Download the Python paper-bot lab", "url": PROJECT},
                {
                    "title": "Download the project guide",
                    "url": "/course-assets/stock-bots/README.md",
                },
            ],
        },
        checkpoints,
    )
