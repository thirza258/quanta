"""Original application questions for the six specialist tracks."""

from foundations import question

ROWS = [
    (
        "1.1",
        "A stock costs $72 and conservative value is $90. Does it meet a 25% required margin of safety?",
        ["Yes: 25%", "No: the margin is 20%", "Yes: 80%"],
        1,
        "1 − 72/90 = 20%, below the assumed 25% requirement.",
    ),
    (
        "1.2",
        "EBIT falls from $100m to $40m while interest stays $20m. How does coverage change?",
        ["5× to 2×", "2× to 5×", "It stays at 5×"],
        0,
        "Divide EBIT by interest for each scenario. Fixed interest leaves less coverage when EBIT falls.",
    ),
    (
        "1.3",
        "Reported EPS is $7, including a nonrecurring $3 disposal gain. Ignoring other adjustments, recurring EPS is:",
        ["$10", "$7", "$4"],
        2,
        "Subtract the disposal gain: $7 − $3 = $4. Check whether other adjustments are needed.",
    ),
    (
        "1.4",
        "Current assets are $150m, total liabilities $90m, preferred claims $10m, and diluted shares 5m. NCAV per share is:",
        ["$12", "$10", "$30"],
        1,
        "($150m − $90m − $10m) / 5m = $10; fixed assets receive no credit in NCAV.",
    ),
    (
        "1.5",
        "In the Graham heuristic, EPS is $2, g is 3, and Y is 4.4. What value follows?",
        ["$29", "$17.12", "$58"],
        0,
        "2 × (8.5 + 2×3) × 4.4 / 4.4 = $29. Growth and yield inputs use percentage points.",
    ),
    (
        "2.1",
        "$121 arrives in two years. At a 10% annual discount rate, present value is:",
        ["$110", "$121", "$100"],
        2,
        "$121 / 1.1² = $100, using consistent annual timing.",
    ),
    (
        "2.2",
        "A normal-return model repeatedly underpredicts extreme losses. Which change merits investigation?",
        [
            "Set the loss probability to zero",
            "Evaluate heavier tails and changing volatility",
            "Assume prices cannot change",
        ],
        1,
        "Heavy tails and varying volatility can change tail probabilities. A model needs empirical checks.",
    ),
    (
        "2.3",
        "With independent observations and unchanged dispersion, increasing sample size from 36 to 144 makes standard error:",
        ["Half as large", "Four times as large", "Unchanged"],
        0,
        "Standard error scales with 1/√n; √36/√144 = 1/2.",
    ),
    (
        "2.4",
        "A strategy has p = 0.03. Which interpretation is valid under the null model?",
        [
            "There is a 97% chance the strategy will profit",
            "The null has 3% probability of being true",
            "Outcomes at least as extreme have 3% probability under the null assumptions",
        ],
        2,
        "A p-value is calculated under the null; it is not a posterior probability or a profit forecast.",
    ),
    (
        "2.5",
        "A fitted beta is 0.8. A +1 percentage point market excess return contributes what fitted component, holding other terms fixed?",
        ["+80 percentage points", "+0.8 percentage points", "A guaranteed +0.8% total return"],
        1,
        "The slope contribution is 0.8 × 1 percentage point. Alpha and residuals remain separate.",
    ),
    (
        "3.1",
        "Daily regression residuals show heteroskedasticity and autocorrelation. Which inference adjustment is relevant?",
        ["HAC standard errors", "Discard every negative return", "Interpret R² as causality"],
        0,
        "HAC addresses heteroskedasticity and autocorrelation in uncertainty estimates under its assumptions.",
    ),
    (
        "3.2",
        "Two trending price series have high correlation. What additional evidence supports a mean-reverting spread?",
        [
            "A shared chart color",
            "A high price level",
            "Evidence of a stationary combination under a cointegration analysis",
        ],
        2,
        "Correlation of levels is insufficient; cointegration examines a stationary linear combination of nonstationary series.",
    ),
    (
        "3.3",
        "A portfolio optimizer returns low estimated variance. What still needs examination?",
        [
            "Nothing: future variance is guaranteed",
            "Estimation error, constraints, and concentration",
            "Only the portfolio name",
        ],
        1,
        "Optimization depends on estimated inputs and constraints, which can be unstable out of sample.",
    ),
    (
        "3.4",
        "A daily 95% VaR estimate is 2%. Which claim is incorrect?",
        [
            "The model allows losses beyond the threshold",
            "Tail observations inform CVaR",
            "A daily loss cannot exceed 2%",
        ],
        2,
        "VaR is a quantile estimate, not a maximum-loss bound.",
    ),
    (
        "3.5",
        "A backtest chooses companies from today's surviving listings for a test twenty years ago. What problem arises?",
        ["Survivorship bias", "Guaranteed excess return", "More accurate historical availability"],
        0,
        "Companies that disappeared may be omitted; a current universe can distort the historical opportunity set.",
    ),
    (
        "4.1",
        "A net-net screen uses last year's statements released after its simulated purchase date. What must change?",
        [
            "Increase leverage",
            "Use statements available by the purchase date",
            "Ignore the publication date",
        ],
        1,
        "A point-in-time screen must respect public availability, not just the accounting period.",
    ),
    (
        "4.2",
        "An apparently cheap company has recurring cash burn and deteriorating returns on capital. What is a useful next test?",
        [
            "Assume the low multiple proves value",
            "Remove costs from the backtest",
            "Test business quality and whether cash burn erodes estimated value",
        ],
        2,
        "A low multiple can reflect deterioration; valuation and quality assumptions need joint examination.",
    ),
    (
        "4.3",
        "A pairs strategy's historical relationship breaks after a merger. What should the research process consider?",
        [
            "Regime change and invalidation of the old spread model",
            "A guaranteed return to the old mean",
            "Unlimited averaging down",
        ],
        0,
        "A structural event can invalidate historical relationships; mean reversion is a hypothesis.",
    ),
    (
        "4.4",
        "A scaler is fitted on all observations before a chronological train/test split. What is wrong?",
        [
            "Scaling is never allowed",
            "The test period influenced preprocessing",
            "There are too few chart types",
        ],
        1,
        "Fit preprocessing on training data only, then apply it to later observations without refitting on the test set.",
    ),
    (
        "5.1",
        "A broker acknowledgment is retried after a network interruption. What helps avoid placing the same economic order twice?",
        [
            "A new random order every retry",
            "Ignoring acknowledgments",
            "An idempotency key and reconciliation of order state",
        ],
        2,
        "Stable identifiers and reconciliation distinguish a retry from a genuinely new order.",
    ),
    (
        "5.2",
        "A rule uses the current day's closing price. In Quanta's backtest, when can its resulting order first fill?",
        ["At the next bar's open", "At the previous day's close", "Earlier in the same day"],
        0,
        "The close signal is not available earlier; the modeled fill occurs at the next open.",
    ),
    (
        "5.3",
        "An AI response suggests buying but omits the required risk fields. What should an execution layer do?",
        [
            "Infer a larger quantity",
            "Reject the invalid proposal before execution",
            "Treat confident wording as validation",
        ],
        1,
        "Validate a structured proposal and its limits before it can affect orders.",
    ),
    (
        "5.4",
        "Price data exceeds the configured freshness limit. Which behavior follows a stale-data guard?",
        [
            "Double position size",
            "Reuse the price without a check",
            "Reject or pause new orders until acceptable data is available",
        ],
        2,
        "A freshness guard stops decisions based on data outside its configured age constraint.",
    ),
    (
        "5.5",
        "A request for 120 shares fills 75. What should the position ledger reflect immediately?",
        [
            "75 executed shares and 45 remaining unfilled",
            "120 executed shares",
            "No position until all shares fill",
        ],
        0,
        "Execution events determine positions; requested and unfilled quantities are separate.",
    ),
    (
        "6.1",
        "Token issuance grows while demand stays weak. Which question is most relevant to holders?",
        [
            "Whether the ticker is short",
            "How dilution and actual token utility affect value capture",
            "Whether issuance guarantees a higher price",
        ],
        1,
        "Supply mechanics and demand for economic utility matter; issuance alone does not create holder value.",
    ),
    (
        "6.2",
        "Ignoring fees, a constant-product pool receives more of token X. What happens to its token Y reserve during the swap?",
        [
            "It must rise by the same amount",
            "It never changes",
            "It falls so the reserve product is maintained",
        ],
        2,
        "Under x·y = k, increasing x reduces y; the difference is paid out.",
    ),
    (
        "6.3",
        "A long spot / short perpetual position collects funding. Why is its return not guaranteed?",
        [
            "Funding can change and basis, financing, and liquidation risks remain",
            "A hedge removes every operational risk",
            "The spot price never moves",
        ],
        0,
        "Directionally offsetting legs do not remove funding, basis, collateral, counterparty, or execution risks.",
    ),
    (
        "6.4",
        "An on-chain transaction was broadcast but the receipt is missing. What should be checked before a replacement?",
        [
            "Only the price chart",
            "Nonce and transaction status under the chain's confirmation rules",
            "Assume the first transaction never existed",
        ],
        1,
        "Reconcile transaction and nonce state to avoid conflicting or duplicate economic actions.",
    ),
    (
        "6.5",
        "Collateral is $8,000, liquidation threshold 0.75, and debt $5,000. After collateral falls 25%, what is the simplified health factor?",
        ["1.2", "1.5", "0.9"],
        2,
        "Collateral becomes $6,000; $6,000 × 0.75 / $5,000 = 0.9, below one in this simplified model.",
    ),
]


def attach_exams(tracks):
    for track in tracks:
        exam_id = f"{track['id']}-final"
        rows = [row for row in ROWS if row[0] in {m["id"] for m in track["modules"]}]
        track["exams"] = [
            {
                "id": exam_id,
                "title": f"{track['title']} final exam",
                "kind": "final",
                "passingScore": 80,
                "minutes": len(rows) * 3,
                "version": 1,
                "description": "Apply each module to a new scenario. Untimed and open-book; review explanations after submission and retake whenever you are ready.",
                "moduleIds": [m["id"] for m in track["modules"]],
                "questions": [
                    {"id": f"{exam_id}-q{i}", "lessonId": row[0], **question(*row[1:])}
                    for i, row in enumerate(rows, 1)
                ],
            }
        ]
