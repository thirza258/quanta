"""Original strategy research course; legacy 4.1–4.4 URLs retain their subjects."""

from applied_courses import checkpoints_for, study
from book_courses import finish

SEC = (
    "U.S. SEC · EDGAR disclosure APIs and filing histories",
    "https://www.sec.gov/search-filings/edgar-application-programming-interfaces",
)
FACTORS = (
    "Kenneth R. French · Five-factor portfolio construction",
    "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_5_factors_2x3.html",
)
MOMENTUM = (
    "Kenneth R. French · Momentum factor construction",
    "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_mom_factor.html",
)
COINT = (
    "statsmodels contributors · Engle–Granger cointegration test",
    "https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.coint.html",
)
LEAKAGE = (
    "scikit-learn contributors · Common pitfalls and data leakage",
    "https://scikit-learn.org/stable/common_pitfalls.html",
)
PBO = (
    "Bailey, Borwein, López de Prado & Zhu · The probability of backtest overfitting",
    "https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf",
)
BOOK = (
    "Graham & Dodd · Security Analysis, classic 1940 edition",
    "https://www.mheducation.com/highered/mhp/product/security-analysis-classic-1940-edition.html",
)


def build_strategy_lab():
    modules = []

    def add(
        id,
        title,
        objective,
        principle,
        case,
        workflow,
        formula,
        code,
        task,
        solution,
        questions,
        refs,
    ):
        rows = []
        for offset, (prompt, correct, wrong1, wrong2, explanation) in enumerate(questions):
            options = [correct, wrong1, wrong2]
            shift = (len(modules) + offset) % 3
            options = options[shift:] + options[:shift]
            rows.append((prompt, options, options.index(correct), explanation))
        item = study(
            id,
            len(modules) // 4 + 1,
            title,
            objective,
            principle,
            case,
            workflow
            + "\n\n### Research notebook evidence\n\nReproduce the worksheet, change the stated assumption, and save your calculation and interpretation with the assignment. Record what information was available, what was estimated, and what would invalidate the conclusion. The browser worksheet stays in cash: its price chart does not backtest this lesson's strategy. Use the downloadable Strategy Lab project for multi-asset simulations, trade ledgers and report exports. All supplied companies, prices and results are fictional teaching cases.",
            formula,
            code,
            task,
            solution,
            rows,
            refs,
        )
        item["minutes"] = 30
        item["reading"] = (
            "30-minute session: 10 minutes of original explanation and primary-source reading, 8 minutes of calculations, and 12 minutes of research notebook or project work. Longer independent experiments and exam time are additional."
        )
        modules.append(item)

    add(
        "4.5",
        "From an investment idea to a falsifiable strategy",
        "Translate an economic mechanism into a rule, comparator and rejection criterion.",
        "A strategy specification connects a proposed mechanism to an observable decision. State who might supply the return, why competition might not remove it, and what risks could explain it. A chart rising after a signal cannot distinguish compensation for risk, an information advantage, luck or a coding error. Begin with an argument that could be wrong.\n\nWrite the eligible assets, information set, signal, portfolio rule, execution time, cost assumptions and comparator before measuring performance. Define an invalidating observation such as failure after realistic costs or dependence on one illiquid security. A rejection threshold guides this research exercise; it is not a universal investment rule. Keep exploratory revisions in an experiment ledger so a later test evaluates a frozen specification.",
        "Cedar's proposal ranks three fictional companies using already released accounts and holds the two strongest names. It predicts an advantage over an equal-weight comparison after 20 basis points per traded notional. A 6% gross advantage with 7% measured cost drag fails the stated net-performance claim even though its raw ranking looked useful.",
        "Open research-notebook.md and complete the hypothesis card. Separate a mechanism claim from an implementation invariant: 'new filings change future ranks' is testable in the supplied fixture, whereas 'this factor earns a premium in real markets' needs independent market evidence.",
        r"\mathrm{net\ advantage}=\mathrm{gross\ advantage}-\mathrm{incremental\ cost\ drag}",
        'print("Net advantage:", 0.06 - 0.07)',
        "Write a research contract with an economic mechanism, eligible universe, signal timing, benchmark, cost basis and two observations that would reject the idea.",
        "An acceptable contract makes the decisions reproducible and preserves a negative result. Distinguish evidence that code follows the contract from independent evidence that the proposed mechanism survives realistic implementation.",
        [
            (
                "What should a strategy hypothesis make possible?",
                "A test that could reject it",
                "Only a more attractive chart",
                "A guarantee of profit",
                "A falsifiable claim specifies observations inconsistent with the mechanism.",
            ),
            (
                "A 6% gross advantage faces 7% incremental cost drag. The net advantage is:",
                "−1 percentage point",
                "13 percentage points",
                "6 percentage points",
                "Subtract incremental costs on the same valuation basis: 6 minus 7 equals −1.",
            ),
            (
                "A researcher changes the rule after inspecting the final result. The changed rule is:",
                "A new exploratory specification requiring new evidence",
                "The unchanged original test",
                "Proof that the original hypothesis passed",
                "Outcome-driven revisions must be logged and evaluated as new research choices.",
            ),
            (
                "Which artifact most clearly fixes the proposed signal before evaluation?",
                "A dated specification with data timing and rejection rules",
                "The final wealth screenshot",
                "The best parameter alone",
                "A specification makes the intended decisions inspectable independently of their outcome.",
            ),
        ],
        [PBO, LEAKAGE],
    )

    add(
        "4.6",
        "Benchmarks, null models and controlled comparisons",
        "Choose comparisons that isolate what the strategy contributes.",
        "A benchmark represents an alternative allocation or a specific null hypothesis. Cash asks whether taking the modeled risk was worthwhile in the sample. An equal-weight eligible portfolio asks whether selection helped relative to broad exposure. A factor-matched comparison asks whether familiar exposures explain the apparent advantage. These questions are related but not interchangeable.\n\nAlign dates, starting wealth, cash-flow conventions, currency and return basis. A costless index is an opportunity comparator, not a perfectly implementable substitute. To attribute a difference to selection, repeat the comparison with matched execution and fees. Do not select a weaker benchmark after seeing which one your strategy beats; document the primary comparison and retain secondary diagnostics.",
        "Strategy wealth grows from 10,000 to 10,800 while an aligned benchmark reaches 10,600. The cumulative return difference is two percentage points. The wealth ratio advantage is 10,800/10,600 − 1 = 1.887%; it answers a different question. Both calculations must use the same start and end dates.",
        "List a cash control, an equal-weight comparator and the thesis-specific benchmark. The download runs equal-weight with the same next-open execution convention and also exports a frictionless close-to-close equal-weight index. Label their differences before comparing the tables.",
        r"\Delta R=R_s-R_b,\qquad R_{\mathrm{relative\ wealth}}=\frac{1+R_s}{1+R_b}-1",
        'print("Return difference:", 10800 / 10000 - 10600 / 10000)\nprint("Relative wealth advantage:", 10800 / 10600 - 1)',
        "Specify three benchmark questions and reconcile a cumulative return difference with a relative wealth ratio. Explain which benchmark is implementable and which is diagnostic.",
        "The two-percentage-point difference compares total returns; the 1.887% ratio compares ending wealth. Match costs and execution when isolating selection, and disclose any costless index convention.",
        [
            (
                "What does an equal-weight eligible portfolio mainly help test?",
                "Whether selection adds to broad universe exposure",
                "Whether every trade can fill instantly",
                "Whether source data are licensed",
                "A broad comparable allocation provides a baseline for the selection rule.",
            ),
            (
                "10800 versus 10600 from equal 10000 starts gives a return difference of:",
                "2 percentage points",
                "20 percentage points",
                "1.887 percentage points",
                "Returns of 8% and 6% differ by two percentage points; the wealth ratio differs.",
            ),
            (
                "A net strategy is compared with a costless index. What belongs in the report?",
                "The benchmark cost convention and a matched-cost sensitivity",
                "A claim that the cost basis is identical",
                "Only the more favorable months",
                "A costless index can be useful, but it does not isolate selection under identical costs.",
            ),
            (
                "Selecting the weakest benchmark after evaluation introduces:",
                "An outcome-driven research choice",
                "A fixed independent comparison",
                "A correction for all factor exposures",
                "Benchmark selection is another degree of freedom that must be disclosed.",
            ),
        ],
        [FACTORS, PBO],
    )

    add(
        "4.7",
        "Signals, orders, fills and the event clock",
        "Separate the decision price from the price at which a trade can execute.",
        "A signal is an instruction inferred from available information, an order is a request, and a fill changes holdings and cash. A backtest that combines them can accidentally trade at a price used to compute its own decision. Define the event clock explicitly: observe the close, calculate target shares, queue an order, execute at the next observed open, and value holdings at the next close.\n\nThe next-open convention removes one obvious timing error but does not model queues, auctions or guaranteed liquidity. Overnight gaps change affordability and realized entry prices. Set whether orders expire, partially fill or remain pending; the teaching project expires unfilled quantities after one open. Record both decision and fill dates so reviewers can reconstruct causality.",
        "A signal at a 100 close requests two shares. The next open is 105 and the per-side cost is 0.1% of notional. The purchase consumes 210.21, not 200.20. A signal on the last close has no next bar and must not receive a fabricated fill.",
        "Draw a five-event timeline and locate the exact cash mutation. In trades.csv, verify every fill date follows its signal date. In the project tests, change tomorrow's close and ensure today's queued target remains identical.",
        r"\mathrm{cash\ after\ buy}=C-qP_{t+1,\mathrm{open}}(1+c)",
        'print("Purchase cash:", 2 * 105 * (1 + 0.001))\nprint("Cash remaining:", 300 - 2 * 105 * (1 + 0.001))',
        "Reconcile a two-share purchase across decision close, next open, fees, closing mark and unfilled last-bar signal. State an order-expiration policy.",
        "The purchase uses 210.21 of the initial 300, leaving 89.79. Subsequent equity includes the two shares at their current mark. A last-bar signal remains unexecuted because no future open exists.",
        [
            (
                "When can a signal using the completed close trade under this lab's convention?",
                "At the next observed open",
                "At that same close automatically",
                "At yesterday's open",
                "The event sequence separates observing the close from a later executable event.",
            ),
            (
                "Two shares at 105 with 0.1% buy cost consume:",
                "210.21",
                "210.00",
                "200.20",
                "Notional is 210 and the fee is 0.21.",
            ),
            (
                "What happens to a new signal on the dataset's final close?",
                "It has no modeled fill without a later bar",
                "It fills at an invented next open",
                "It is moved backward one day",
                "Missing future execution data cannot be replaced by a favorable assumption.",
            ),
            (
                "An overnight gap makes the target unaffordable. The engine should:",
                "Apply a declared cash constraint and record the partial fill",
                "Create undeclared leverage",
                "Use the previous close as its fill",
                "Execution must respect available cash under the documented allocation policy.",
            ),
        ],
        [LEAKAGE, PBO],
    )

    add(
        "4.8",
        "Experiment manifests and reproducible research",
        "Record enough information for another person to reproduce and challenge a run.",
        "An experiment consists of more than a parameter and a terminal return. Record the source revision, input identity, universe definition, calendar, feature availability, signal and execution conventions, fees, sample boundaries and all attempted alternatives. Keep outputs together with the manifest that produced them. A file hash identifies bytes; it does not establish that the provider supplied correct or point-in-time observations.\n\nSeparate development, validation and final evaluation. Use development data to debug invariants, validation data to compare the predeclared candidate set, and a final segment for the locked choice. Once inspected, a final segment has been used; calling another run 'out of sample' does not restore independence. Synthetic fixtures are valuable for engineering checks but cannot establish an investment effect.",
        "Three signal families are tested at two lookbacks and two fee assumptions: twelve configurations, even if only one appears in the presentation. An archive with one winner and no rejected runs understates the search. A source hash and input hash let a reviewer rerun that exact archive.",
        "Run the supplied project into a fresh output directory. Inspect its manifest, experiment ledger and source/input SHA-256 values. Enter any additional local trials in the notebook; the program records its own declared candidates but cannot discover unlogged experiments elsewhere.",
        r"N_{\mathrm{trials}}=N_{\mathrm{families}}N_{\mathrm{lookbacks}}N_{\mathrm{cost\ settings}}",
        'print("Attempted configurations:", 3 * 2 * 2)',
        "Create an experiment manifest, list twelve planned configurations and assign each data segment a role. Explain what a hash verifies and what it cannot verify.",
        "Record all twelve attempts, including poor outcomes. Hashes verify exact bytes; data meaning, availability and selection independence need separate evidence. Do not reclassify a viewed final segment as untouched.",
        [
            (
                "What does an input hash identify?",
                "A particular sequence of file bytes",
                "A profitable mechanism",
                "A guarantee against survivorship bias",
                "Hash identity supports reproduction but does not certify the dataset's semantics.",
            ),
            (
                "Three families, two lookbacks and two costs create how many configurations?",
                "Twelve",
                "Seven",
                "One",
                "The product of independently varied choices is 3 × 2 × 2 = 12.",
            ),
            (
                "A viewed test segment is reused to choose a parameter. It is now:",
                "Part of the research selection process",
                "Untouched independent evidence",
                "Equivalent to a new future sample",
                "Once outcomes influence decisions, the segment has participated in selection.",
            ),
            (
                "Which missing artifact most prevents reproduction of a winning backtest?",
                "The exact input and configuration manifest",
                "A decorative logo",
                "The researcher's favorite chart color",
                "Exact inputs and decisions are necessary to reproduce the computation.",
            ),
        ],
        [PBO, LEAKAGE],
    )

    add(
        "4.9",
        "Point-in-time fundamentals and filing revisions",
        "Join accounts by information availability while preserving original revisions.",
        "An accounting period end is not the date a researcher learned the result. A usable fundamental row needs the company identity, reporting period, publication or acceptance timestamp, units, share basis and revision identity. An amended filing may describe an old quarter but was unavailable to the original investor. A table containing only today's latest figures can silently rewrite the past.\n\nChoose an as-of policy explicitly. The teaching project takes the latest available reporting period, then its latest available revision, and excludes records first available after the decision. Its date-only fixture conservatively permits a filing from the following session. A real feed needs timezone-aware publication and ingestion timestamps, reconciliation of duplicate facts, and a justified processing delay.",
        "A December-period NCAV of 12 is published on February 10 and amended to 9 on March 15. A February 20 screen can use 12; an April screen uses 9. A January trade can use neither. A newer amendment to an older period should not displace a more recent reporting period without an explicit policy.",
        "Inspect fundamentals.csv and append a future revision. Run the causality test: earlier orders must remain unchanged. Build a separate audit table showing period end, available date, selected revision and stale-age threshold for each decision.",
        r"\mathrm{eligible\ filing}:\quad t_{\mathrm{available}}<t_{\mathrm{decision}}",
        'print("February screen NCAV:", 12)\nprint("April screen NCAV:", 9)\nprint("Revision change:", 9 - 12)',
        "Construct an as-of join for the original filing and amendment. State when each becomes usable and how an amendment to an older reporting period is handled.",
        "The January decision has no eligible filing, February 20 sees 12, and April sees 9. Select by latest eligible reporting period before revision date; retain all versions and disclose the conservative date-only delay.",
        [
            (
                "Which date determines whether a filing could inform a simulated trade?",
                "Its information-availability date",
                "Only its fiscal period end",
                "The date the backtest is run",
                "Availability, with a declared processing delay, controls the investor's information set.",
            ),
            (
                "A March amendment changes a December value. May February decisions use it?",
                "No, it was not yet available",
                "Yes, because December is earlier",
                "Yes, if the revision helps accuracy",
                "A revision can describe the past without being known in the past.",
            ),
            (
                "A date-only feed lacks publication time. A defensible lab convention is:",
                "Delay use until a later session and document it",
                "Assume every release preceded the open",
                "Ignore publication dates entirely",
                "A conservative explicit delay avoids claiming intraday knowledge the data cannot establish.",
            ),
            (
                "What should happen when a late amendment concerns an older reporting period?",
                "Apply the documented period-and-revision selection policy",
                "Always overwrite every newer quarter",
                "Delete the amendment from provenance",
                "Preserving period identity prevents late old-period revisions from silently replacing newer accounts.",
            ),
        ],
        [SEC, LEAKAGE],
    )

    add(
        "4.10",
        "Historical universes, missing prices and corporate actions",
        "Distinguish an unavailable observation from a zero return or a surviving company.",
        "A present-day ticker list is not a historical investment universe. Companies enter, merge, delist or change identifiers. Build membership as of each decision and retain exits, including unfavorable ones. A missing quote may mean a suspension, a vendor outage or a delisting; forward-filling indefinitely manufactures an executable price and hides uncertainty. Decide when marking is allowed and when trading must halt.\n\nCorporate actions require consistent units. A split changes share quantity and per-share price while leaving immediate economic value unchanged. Dividends belong in cash or in a consistent total-return series; applying both double-counts them. Raw prices are useful for execution, while adjusted histories support certain signals, but their relationship must be documented. The supplied fixture deliberately has no corporate actions and rejects incomplete panels rather than inventing fills.",
        "Ten shares at 100 become twenty at 50 after a two-for-one split: value remains 1,000. A price-only calculation reports −50% if quantity is left unchanged. Separately, excluding a delisted company with a −80% return from a two-stock portfolio whose other return is +20% changes the equal-weight result from −30% to +20%.",
        "Create separate status fields for membership, tradability and mark quality. In a real-data adapter, require an explicit terminal-value policy for delistings and test split/dividend accounting before accepting any performance output.",
        r"q_{\mathrm{after}}=kq_{\mathrm{before}},\quad P_{\mathrm{after}}=P_{\mathrm{before}}/k",
        'print("Split value:", 10 * 2 * (100 / 2))\nprint("Survivorship-aware return:", (0.20 - 0.80) / 2)',
        "Reconcile the split and two-stock delisting case. Draft policies for a missing quote, a suspension, a cash dividend and a terminal delisting payment.",
        "The split preserves 1,000 of value and the full two-stock sample returns −30%. A missing quote is not a zero return or permission to fill; document mark age, order rejection and terminal settlement separately.",
        [
            (
                "Ten shares at 100 undergo a two-for-one split. Immediate value becomes:",
                "1000",
                "500",
                "2000",
                "Share quantity doubles as per-share price halves, preserving value.",
            ),
            (
                "A missing quote should automatically be interpreted as:",
                "Neither a zero return nor an executable fill",
                "A guaranteed unchanged tradable price",
                "A profitable delisting",
                "The cause of missingness and the mark/trading policy must be established.",
            ),
            (
                "Dropping a −80% delisted stock from a +20%/−80% equal-weight pair changes the record through:",
                "Survivorship bias",
                "A valid split adjustment",
                "Lower arithmetic precision",
                "Removing failed securities conditions the universe on future survival.",
            ),
            (
                "Cash dividends added to an already dividend-adjusted total-return path cause:",
                "Double counting",
                "Automatic benchmark alignment",
                "Removal of all corporate-action risk",
                "The same distribution must enter the wealth calculation only once.",
            ),
        ],
        [SEC, FACTORS],
    )

    add(
        "4.11",
        "Feature cleaning, robust ranks and missingness",
        "Clean observations without allowing future data to set today's transformation.",
        "Cleaning decisions encode economic assumptions. Check currency, scale, sign and denominator before clipping an extreme ratio. A negative earnings denominator is not simply a very cheap positive P/E. A stale balance sheet and a genuine zero have different meanings. Record exclusions and missingness by date and sector so data coverage cannot silently become a predictive signal about survival.\n\nFor a cross-sectional rule, ranks can be calculated from the contemporaneously eligible universe because those inputs exist at that decision time. For a fitted ML transformation, estimate clipping, imputation and scaling parameters within each training fold and reuse them on later observations. Handle ties deterministically, and define what happens when every value is equal or a standard deviation is zero. These policies change holdings and belong in the strategy specification.",
        "Three comparable positive earnings yields are 4%, 6% and 8%; a fourth field reads 600 because a vendor expressed basis points as a raw fraction. Clipping 600 without fixing units hides the error. Once corrected to 6%, the tied middle observations require an explicit equal-rank or stable tie policy.",
        "Write a small data dictionary and a cleaning log. Compare winsorized z-scores with percentile ranks, record membership changes, and test that future outliers cannot alter a prior fitted scaler. The downloadable ranker uses symbol order only to make exact ties reproducible.",
        r"z_i=(x_i-\mu_{\mathrm{fit}})/\sigma_{\mathrm{fit}}",
        'print("600 basis points as a fraction:", 600 / 10000)\nprint("Standardized yield:", (0.08 - 0.06) / 0.02)',
        "Repair the unit error, specify a missing-value and tie policy, and explain when contemporaneous ranks are valid versus when a learned scaler must be frozen.",
        "600 basis points is 0.06, not 600. Today's eligible cross-section can define today's ranks; parameters learned across observations belong to training folds. Missing data, zero variance and ties require explicit deterministic handling.",
        [
            (
                "600 basis points expressed as a return fraction is:",
                "0.06",
                "6",
                "600",
                "One basis point is 0.0001, so 600 basis points equals 0.06.",
            ),
            (
                "Before clipping a suspicious financial ratio, first check:",
                "Units, definitions and denominator validity",
                "Which clipping level maximizes test return",
                "Only the chart's color",
                "Data-definition errors need correction before statistical treatment of outliers.",
            ),
            (
                "A contemporaneous cross-sectional rank uses:",
                "Only the universe and values available at that decision",
                "Future entrants to improve coverage",
                "The final sample's best performers",
                "Ranking is causal only when its membership and inputs are available at the decision time.",
            ),
            (
                "Two equal scores compete for one portfolio slot. A reproducible rule needs:",
                "A declared deterministic tie policy",
                "The stock with the best future return",
                "An unrecorded random choice",
                "A stable tie rule prevents hidden dependence on row ordering or future outcomes.",
            ),
        ],
        [LEAKAGE, SEC],
    )

    add(
        "4.12",
        "Return labels, overlap and chronological splits",
        "Define a tradable target and remove training labels that reach into evaluation time.",
        "The prediction target must match the proposed holding period and execution convention. A close-to-close label can measure an information relation, but it is not the return of a next-open trade. Save the feature decision time, entry time, exit time and label end for each observation. A chronological row split alone does not prevent leakage when a training label uses prices from the evaluation period.\n\nPurge training observations whose label intervals overlap the evaluation boundary. If the design has additional information overlap or observations on both sides of a test block, choose and document an appropriate embargo; a fixed gap is not a universal repair. Cross-sectional samples also share dates and market shocks. Keep entire dates together rather than randomly distributing stocks from one date between training and test.",
        "A ten-session label made on session 95 ends on 105, while validation begins on 101. That training row overlaps validation and must be removed. A label ending on 100 does not cross that boundary. If the next-open entry is 102 and the exit is 105, the gross trade return is 2.941%, not the 5% implied by a decision close of 100.",
        "Draw interval endpoints for six rows around the boundary and mark which rows are eligible. Use the ML course for full fitted-model pipelines; this lab focuses on whether the resulting signal can be evaluated as a tradable allocation.",
        r"y_t=P_{\mathrm{exit}}/P_{\mathrm{entry}}-1,\qquad t_{\mathrm{label\ end}}<t_{\mathrm{validation\ start}}",
        'print("Next-open gross target:", 105 / 102 - 1)\nprint("Overlapping training row:", 105 >= 101)',
        "Build a table of decision, entry, exit and label-end times for six observations. Purge overlapping labels and explain why a random stock-row split is inadequate.",
        "The row ending at 105 is excluded from training when validation begins at 101. A trade entering at 102 and exiting at 105 earns about 2.941% before costs. Group rows by date and fit all transformations on the retained training segment.",
        [
            (
                "A label ending on 105 with validation starting on 101 should be:",
                "Purged from training",
                "Kept because its feature date is earlier",
                "Assigned a zero return",
                "The label uses validation-period prices despite an earlier feature timestamp.",
            ),
            (
                "Entry at 102 and exit at 105 gives a gross return closest to:",
                "2.941%",
                "5%",
                "3.922%",
                "The realized entry basis is 102, so the return is 105/102 minus one.",
            ),
            (
                "Why keep stocks from the same date together in a chronological split?",
                "They share time information and market shocks",
                "To guarantee equal sector weights",
                "To remove transaction costs",
                "Random stock-row splitting can expose evaluation-period structure to training.",
            ),
            (
                "What determines an appropriate purge or embargo policy?",
                "Label intervals and the design's information overlap",
                "A universally correct one-day gap",
                "The final Sharpe ratio",
                "The required separation follows actual information horizons, not a favorable test outcome.",
            ),
        ],
        [LEAKAGE, PBO],
    )

    add(
        "4.1",
        "The systematic net-net screen",
        "Turn net-current-asset value into an auditable screen with quality and liquidity exclusions.",
        "A net-net screen compares market price with a conservative balance-sheet claim. Compute current assets less total liabilities and other senior claims, then divide by the contemporaneous diluted share count appropriate to the analysis. Current liabilities alone are insufficient: long-term creditors also stand ahead of equity. The accounting number is a starting estimate, not a promise of realizable liquidation proceeds.\n\nDiscount doubtful receivables and inventory, inspect restricted cash, off-balance-sheet obligations, dilution and operating cash burn. A mechanical two-thirds threshold can locate candidates while admitting deteriorating businesses that consume their apparent cushion. Separate the candidate screen, financial quality review and portfolio implementation. This modern systematic exercise extends the analytical discipline of Security Analysis; it does not reproduce the book's text or claim that a synthetic test validates a historical premium.",
        "Cash 40, receivables 60 and inventory 80 less total liabilities 70 leave 110. With ten shares, NCAV is 11 and the two-thirds ceiling is 7.333. Haircut receivables by 20% and inventory by 40%: adjusted NCAV falls to 6.6 and the ceiling to 4.4. A price of 6 passes the raw screen but fails the adjusted one.",
        "Build both raw and adjusted columns in the notebook. Use only eligible filings, record the share-count basis, and count exclusions before examining returns. Run the downloadable value-quality rule to inspect a simplified raw NCAV filter; add and test haircuts as a separately logged extension.",
        r"\mathrm{NCAV/share}=\frac{C+AR+I-L_{\mathrm{total}}-S_{\mathrm{senior}}}{N},\qquad P<\frac23\mathrm{NCAV/share}",
        'raw = (40 + 60 + 80 - 70) / 10\nadjusted = (40 + 60 * 0.8 + 80 * 0.6 - 70) / 10\nprint("Raw NCAV:", raw)\nprint("Adjusted screen ceiling:", adjusted * 2 / 3)',
        "Reconcile raw and adjusted NCAV, classify the price-6 candidate, and list five reasons realizable equity value could be below the accounting screen.",
        "Raw NCAV is 11 with a 7.333 ceiling; adjusted NCAV is 6.6 with a 4.4 ceiling. The candidate changes from pass to fail. Doubtful assets, senior claims, restricted cash, dilution and continuing losses can reduce the cushion.",
        [
            (
                "Which liabilities belong in a basic NCAV calculation?",
                "Total liabilities and relevant senior claims",
                "Only current liabilities",
                "No liabilities when the price is low",
                "All claims senior to common equity matter to the residual asset estimate.",
            ),
            (
                "After the stated haircuts, the two-thirds price ceiling is:",
                "4.4",
                "7.333",
                "6.6",
                "Adjusted assets less liabilities are 66; per-share NCAV is 6.6 and two-thirds is 4.4.",
            ),
            (
                "A stock passes raw NCAV but fails after conservative inventory haircuts. The analyst should:",
                "Retain the sensitivity and investigate realizable asset values",
                "Delete the haircut to preserve the purchase",
                "Claim the raw screen guarantees liquidation proceeds",
                "The discrepancy exposes dependence on asset-recovery assumptions.",
            ),
            (
                "Using current liabilities alone in a net-net screen generally:",
                "Overstates equity's residual claim when other liabilities exist",
                "Automatically incorporates long-term debt",
                "Eliminates the need for share counts",
                "Long-term creditors and other senior claims also reduce the residual available to common equity.",
            ),
        ],
        [BOOK, SEC],
    )

    add(
        "4.2",
        "Quality at a reasonable price",
        "Combine comparable value and quality inputs without hiding leverage or sector effects.",
        "Quality at a reasonable price combines a valuation preference with evidence about business economics. Define earnings yield, invested-capital return and coverage carefully: recurring earnings, net operating assets and financing costs must refer to compatible periods. Financial companies may require different definitions from industrial companies, and sector composition can dominate a pooled ranking.\n\nA composite is a declared preference rather than an objective truth. Standardize or rank comparable inputs before combining them, specify weights, and inspect each component separately. Apply essential solvency exclusions before ranking instead of allowing exceptional cheapness to compensate for an unacceptable liability profile. Contemporaneous cross-sectional scaling is valid when all inputs and membership are known; temporal transformations learned from data must stay within training folds.",
        "Standardized earnings yield 1.2, ROIC 0.6 and coverage −0.3 give an equal-weight score of 0.5. Increasing the value weight to 50% and using 25% each for the others gives 0.675. This is a different preference, not new evidence. A company failing a predeclared coverage floor remains excluded under either score.",
        "Reproduce both composites and compare within-sector versus pooled ranks. The download ranks eligible fictional firms on earnings yield and ROIC after positive-earnings, coverage and NCAV gates. Its simplified definitions are explicit; add a third component only with a new manifest and validation comparison.",
        r"S_i=\sum_{k=1}^{K}a_kz_{ik},\qquad \sum_k a_k=1",
        'print("Equal-weight quality score:", (1.2 + 0.6 - 0.3) / 3)\nprint("Value-heavy score:", 0.5 * 1.2 + 0.25 * 0.6 - 0.25 * 0.3)',
        "Calculate both composite scores, state a solvency exclusion and compare the holdings produced by pooled and within-sector ranks. Log the weight change as a separate trial.",
        "Scores are 0.5 and 0.675. A fixed coverage exclusion applies before either rank. Sector-aware comparisons reveal whether the score mostly selected an industry, and changing weights increases the research search count.",
        [
            (
                "A composite score primarily expresses:",
                "An explicit set of feature weights and preferences",
                "A universally optimal valuation",
                "A guarantee that every input is reliable",
                "The score reflects its definitions, scaling, universe and chosen weights.",
            ),
            (
                "The value-heavy 50%/25%/25% score for 1.2, 0.6 and −0.3 is:",
                "0.675",
                "0.5",
                "1.5",
                "Compute 0.6 + 0.15 − 0.075 = 0.675.",
            ),
            (
                "A candidate fails a mandatory coverage floor but has exceptional earnings yield. It should:",
                "Remain excluded under the predeclared rule",
                "Automatically pass because the composite is high",
                "Have its debt removed from the data",
                "Hard eligibility constraints are applied before compensating composite scores.",
            ),
            (
                "Pooled quality ranks select nearly one sector. A useful diagnostic is:",
                "Compare sector exposures and within-sector ranks",
                "Assume the sector is inherently superior",
                "Hide the benchmark's sector weights",
                "Sector analysis separates intended company selection from broad industry exposure.",
            ),
        ],
        [BOOK, FACTORS],
    )

    add(
        "4.13",
        "Catalysts, value traps and thesis invalidation",
        "Distinguish a valuation gap from a timed mechanism for closing it.",
        "A cheap security may stay cheap because value is uncertain, inaccessible or declining. A catalyst is a proposed event that could change cash flows, capital allocation or investor information; it is not a substitute for valuation. State the expected event window, the evidence needed to recognize it and the observation that would invalidate the thesis. Avoid labeling every price increase as confirmation after the fact.\n\nTranslate new information into the accounts before changing the portfolio. Inventory write-downs reduce recoverable assets, cash burn shortens the runway, and dilution changes the per-share claim. An event-driven screen needs timestamped event data and realistic reaction delays. A scheduled earnings date alone does not reveal its outcome. Use the news-to-markets course to build an evidence chain from a release to the company and its valuation.",
        "A company has adjusted NCAV of 8 per share and trades at 5.5. Four quarters of 0.5 per-share cash burn reduce the simple asset cushion to 6 before other changes, leaving only 0.5 above price. An expected asset sale is relevant only after considering proceeds, taxes, debt repayment and the probability that it occurs.",
        "Write a thesis-monitoring table with one confirming event, one disconfirming event and one noninformative price move. Connect your entry to [news analysis](/curriculum/news-to-markets) and label any event-based extension as unimplemented until its timestamps and cash effects are tested.",
        r"\mathrm{remaining\ asset\ cushion}=\mathrm{NCAV}_0-BT-P",
        'print("NCAV after cash burn:", 8 - 0.5 * 4)\nprint("Cushion over price:", 8 - 0.5 * 4 - 5.5)',
        "Create a catalyst and invalidation memo, calculate the cash-burn sensitivity, and define how a late or cancelled event changes the research rule.",
        "Four quarters of burn reduce the simplified NCAV to 6 and the cushion to 0.5. Require evidence about realizable proceeds and timing; a price increase alone does not validate the asset-sale hypothesis.",
        [
            (
                "Why can a low valuation multiple persist?",
                "Value may be uncertain, inaccessible or deteriorating",
                "Every low multiple must close within a month",
                "Discounts eliminate all business risk",
                "Cheapness can reflect a changing business or uncertainty about access to its assets.",
            ),
            (
                "NCAV 8 less four quarters of 0.5 cash burn leaves:",
                "6 per share",
                "7.5 per share",
                "10 per share",
                "The simplified burn reduction is 4 × 0.5 = 2 per share.",
            ),
            (
                "A known earnings date provides advance knowledge of:",
                "The scheduled event, not the eventual earnings surprise",
                "The exact release outcome",
                "A guaranteed favorable return",
                "Event timing and event content are different information sets.",
            ),
            (
                "What is the strongest reason to invalidate an asset-value thesis?",
                "Evidence that expected recoverable assets have materially deteriorated",
                "An unrelated daily price movement",
                "A change in chart scale",
                "Disconfirmation should challenge the mechanism or valuation assumptions directly.",
            ),
        ],
        [BOOK, SEC],
    )

    add(
        "4.14",
        "Fundamental strategy research from screen to holdings",
        "Evaluate a complete fundamental allocation and audit its exclusions and concentration.",
        "A screen does not define a portfolio until entry, exit, weighting, rebalance and missing-data policies are specified. A monthly value screen may hold companies between publications, while a daily rerank may create turnover with little new accounting information. Distinguish an eligibility exit from a small rank change and measure how each contributes to trading.\n\nWrite a waterfall from the historical universe to usable filings, valid denominators, financial gates, ranked candidates and final constrained holdings. A strategy holding only one name after filters should not silently invest all capital if its mandate caps single-name exposure. Retain cash when too few candidates qualify. Compare the full rule against equal-weight eligible stocks and against simpler value-only and quality-only variants with matching timing and costs.",
        "Six stocks enter the universe; one lacks available accounts, one fails coverage, and one fails the NCAV gate. Three candidates remain. A two-name portfolio with a 40% single-name cap invests at most 80%, leaving 20% in cash. If only one qualifies, the same cap leaves 60% cash rather than creating a new concentration rule.",
        "Run value-quality in the local project and trace a signal through signals.csv to trades.csv and equity.csv. Reconcile rejected candidates and unused cash. Design a slower rebalance extension and compare the number of changed positions before interpreting its return.",
        r"w_i=\min(1/N_{\mathrm{selected}},w_{\max}),\qquad w_{\mathrm{cash}}=1-\sum_iw_i",
        'print("Two-name invested weight:", 2 * min(1 / 2, 0.4))\nprint("One-name cash weight:", 1 - min(1, 0.4))',
        "Produce an eligibility waterfall, holdings table and cash reconciliation for a fundamental rule. Compare at least two ablations and state whether any observed difference comes from selection or exposure.",
        "Three names survive the example gates. Two holdings capped at 40% leave 20% cash; one leaves 60%. Keep execution and fees fixed when isolating the value and quality components.",
        [
            (
                "A fundamental screen becomes an executable portfolio only after specifying:",
                "Sizing, rebalance, exits and execution rules",
                "A more confident name",
                "Only the lowest observed P/E",
                "Selection alone does not determine positions, cash or trading events.",
            ),
            (
                "Two selected names each capped at 40% leave cash of:",
                "20%",
                "0%",
                "40%",
                "The two position weights sum to 80%, leaving the remainder in cash.",
            ),
            (
                "Only one name qualifies under a fixed 40% cap. The allocation should:",
                "Retain 60% cash",
                "Silently raise the cap to 100%",
                "Invent another qualifying company",
                "A shortage of candidates does not justify changing the predeclared concentration rule.",
            ),
            (
                "What reveals where a fundamental rule loses most of its universe?",
                "An eligibility waterfall with exclusion reasons",
                "Only its terminal wealth",
                "The selected ticker font size",
                "Counts after each filter expose coverage and selection effects.",
            ),
        ],
        [FACTORS, BOOK],
    )

    add(
        "4.15",
        "Time-series trend following",
        "Build a causal directional trend rule and identify its regime-dependent losses.",
        "A time-series trend rule compares an asset with its own history. Examples include price above a moving average or positive trailing return. These are hypotheses about persistence, not valuation estimates. Specify whether the latest completed close is included, how the warm-up period works, how often the rule updates and whether the allocation is long/cash or allows short exposure.\n\nThe rule can lose repeatedly in a sideways market when small reversals trigger entries and exits. A lagged indicator may also exit well after a sudden gap. Parameter choice changes the trade-off between responsiveness and turnover; there is no universally best lookback. Evaluate performance across windows and regimes under the same execution convention, and compare with an always-invested baseline so cash exposure is visible.",
        "Completed closes of 98, 100, 101 and 105 have a four-close mean of 101. The 105 close is above that mean and queues a long instruction for the next open. If the next open gaps to 110, the strategy does not obtain the earlier 105 close. A close equal to the average remains cash under a strictly-greater rule.",
        "Reproduce the moving average and list signals for a rising path and an alternating path. Compare entry counts under two windows before comparing profits. The project implements cross-sectional momentum; a time-series filter is a separate extension with its own tests.",
        r"s_t=\mathbf{1}\{P_t>L^{-1}\sum_{j=0}^{L-1}P_{t-j}\}",
        'average = (98 + 100 + 101 + 105) / 4\nprint("Trailing mean:", average)\nprint("Next-open long instruction:", 105 > average)',
        "Specify and hand-run a four-close long/cash rule on rising and alternating paths, including warm-up, equality and overnight-gap cases.",
        "The example average is 101 and the last close triggers a next-open instruction. Warm-up holds cash until all required observations exist; equality follows the declared strict comparison. Whipsaw losses and delayed gap exits remain possible.",
        [
            (
                "A time-series trend signal compares an asset primarily with:",
                "Its own past observations",
                "Only next month's winners",
                "A liquidation balance sheet",
                "Time-series rules use the asset's historical path to form a directional instruction.",
            ),
            (
                "The mean of 98, 100, 101 and 105 is:",
                "101",
                "100",
                "105",
                "The four completed closes sum to 404, giving a mean of 101.",
            ),
            (
                "A close-based trend rule signals at 105 before an open of 110. Its modeled entry uses:",
                "110 plus declared costs",
                "105 automatically",
                "The better of 105 and 110",
                "The next-open convention cannot choose an earlier or retrospectively favorable price.",
            ),
            (
                "Repeated small reversals around a trend threshold primarily create:",
                "Whipsaw and transaction-cost risk",
                "Guaranteed arbitrage",
                "Perfect valuation information",
                "Frequent entries and exits can lose money even without a large directional move.",
            ),
        ],
        [MOMENTUM, PBO],
    )

    add(
        "4.16",
        "Cross-sectional momentum and skip periods",
        "Rank assets by past performance with an explicit formation and holding calendar.",
        "Cross-sectional momentum compares assets with each other, while time-series momentum asks whether an asset's own trailing return is positive. Ranking can select relative winners even when every asset has fallen. Decide whether the mandate holds those winners or adds a positive-return gate; those are different strategies with different market exposures.\n\nDefine formation, skip and holding periods in actual timestamps. The French momentum factor uses prior months 2–12; it is a specific long-short research construction, not the same as a small long-only top-two portfolio. A skip period avoids using the most recent segment in the ranking but does not eliminate all reversal, crash or liquidity risk. The supplied daily fixture uses a short declared lookback and one-observation skip to make indexing inspectable, not to replicate a published factor.",
        "At decision index 6 with lookback 3 and skip 1, the score uses close[5]/close[2] − 1. Values 110 and 100 give 10%. The current close[6] is not part of that score. Candidate B with 8% ranks below A; a separate positive-score gate determines what happens if both scores are negative.",
        "Make an index table and manually check the first non-cash formation date in signals.csv. Mutate the current skipped close and verify its rank effect is absent while the decision's position-sizing price can still change. Keep ranking logic separate from sizing logic.",
        r"M_{i,t}=\frac{P_{i,t-s}}{P_{i,t-s-L}}-1",
        'print("Momentum score:", 110 / 100 - 1)\nprint("Formation end index:", 6 - 1)\nprint("Formation start index:", 6 - 1 - 3)',
        "Document formation endpoints, skip and holding periods, reproduce two candidate scores, and explain the difference between relative winners and a positive-trend requirement.",
        "The score spans indices 2 to 5 and equals 10%. Relative ranking can select a negative-return winner; a positive-score gate is an additional rule. The short synthetic implementation is not the French monthly factor.",
        [
            (
                "Can the highest cross-sectional momentum score still be negative?",
                "Yes, if all candidates declined",
                "No, ranking forces a positive return",
                "Only if returns are annualized",
                "Relative ranking orders candidates without changing the sign of their returns.",
            ),
            (
                "At t=6, skip=1 and lookback=3, the score endpoints are:",
                "Indices 2 and 5",
                "Indices 3 and 6",
                "Indices 1 and 6",
                "The end is t−skip=5 and the start is 5−lookback=2.",
            ),
            (
                "A top-two long-only daily rule and the French momentum factor are:",
                "Different constructions whose calendars and exposures must be disclosed",
                "Identical because both use past returns",
                "Guaranteed to have equal turnover",
                "A common broad idea does not make the universe, horizon or long-short construction identical.",
            ),
            (
                "Adding a positive-score gate to a relative ranking changes:",
                "The allocation and potentially its cash exposure",
                "Only the strategy's label",
                "Nothing when every asset is falling",
                "The gate can exclude relative winners and leave cash when their absolute returns are negative.",
            ),
        ],
        [MOMENTUM, FACTORS],
    )

    add(
        "4.17",
        "Short-horizon reversal and microstructure effects",
        "Distinguish a tradable reversal hypothesis from bid–ask bounce and execution artifacts.",
        "A reversal rule expects a recent deviation to move back toward a reference level. It requires a reason: temporary liquidity pressure is different from a permanent earnings shock. A negative return by itself does not establish mispricing. Define the horizon, entry threshold, exit threshold and maximum holding time, and state which information would invalidate the reference level.\n\nAt short horizons, a last-trade price can alternate between bid and ask even while the midpoint is unchanged. Apparent negative autocorrelation then comes from measurement and spread crossing rather than an exploitable price pattern. Use quote-aware data when the claim depends on microstructure, include both entry and exit costs, and test slower execution. Daily bars cannot establish queue position or intraday fill probability.",
        "A stable quote has bid 99.9 and ask 100.1. Alternating prints suggest reversals, but buying at the ask and immediately selling at the bid loses 0.2 per share before fees. A supposed 0.15 gross edge cannot cover that 0.2 round-trip spread cost under this simple model.",
        "Compare a midpoint series and alternating last trades, then subtract a round-trip spread estimate from the proposed edge. Identify what additional data would be required before adapting the strategy to a short-horizon execution engine.",
        r"\mathrm{round\ trip\ edge/share}=\mathrm{gross\ edge}-(\mathrm{ask}-\mathrm{bid})-\mathrm{fees/share}",
        'print("Round-trip spread:", 100.1 - 99.9)\nprint("Edge after spread:", 0.15 - (100.1 - 99.9))',
        "Calculate the quote-bounce case, specify reversal invalidation and holding-time rules, and list evidence unavailable from daily OHLC bars.",
        "The spread is 0.2 and the 0.15 proposed edge becomes −0.05 before fees. Daily bars cannot establish quote-side entry, queue priority or two-sided intraday liquidity; permanent information changes can invalidate mean reversion.",
        [
            (
                "Alternating bid and ask prints with a stable midpoint can create:",
                "Apparent reversal without an executable edge",
                "Guaranteed positive after-cost returns",
                "A change in fundamental value every trade",
                "Bid–ask bounce can create a statistical pattern that disappears under executable prices.",
            ),
            (
                "A 0.15 gross per-share edge less a 0.20 spread leaves:",
                "−0.05 before fees",
                "0.35 before fees",
                "0.15 after all costs",
                "The round-trip spread exceeds the proposed gross edge by 0.05.",
            ),
            (
                "A permanent earnings impairment should prompt a reversal researcher to:",
                "Reassess whether the previous reference level remains valid",
                "Assume an inevitable rebound",
                "Remove the bad announcement from the sample",
                "A permanent information change differs from temporary price pressure.",
            ),
            (
                "What cannot daily bars establish for an intraday reversal order?",
                "Its queue position and executable quote sequence",
                "That a daily close was recorded",
                "The number of supplied daily rows",
                "OHLC aggregation omits the order-book and event sequence needed for precise fill claims.",
            ),
        ],
        [COINT, PBO],
    )

    add(
        "4.18",
        "Rebalance buffers and parameter stability",
        "Reduce unnecessary turnover and compare neighboring rules without selecting on the final sample.",
        "A ranking rule can oscillate around a cutoff, replacing nearly identical candidates every rebalance. A buffer or hysteresis rule enters at a stronger threshold and exits only after a weaker threshold is crossed. This can reduce trading but also delays response. It changes the strategy and must be specified before final evaluation. Record whether retained positions can exceed a cap because of price drift and when they are resized.\n\nInspect a parameter surface rather than only its maximum. A broad region of similar validation results is more encouraging than one isolated spike, but it is still selected evidence. Evaluate costs, turnover, concentration and drawdown across nearby settings. Do not repeatedly inspect the holdout while searching for an attractive plateau. The final choice should follow a declared tie-break, such as lower turnover among candidates meeting the validation requirement.",
        "A top-ten rule with an exit buffer at rank fifteen retains an existing holding at rank twelve but does not admit a new candidate at rank twelve. If modeled traded notional falls from 2.0 to 1.2 times equity, a 20-basis-point per-side proportional cost falls from 0.004 to 0.0024 of equity under a fixed notional approximation.",
        "Hand-run entry and exit decisions for ranks 9, 12 and 16. Record neighboring lookbacks and their net result, turnover and worst period in the notebook. Label a buffer extension separately from the downloadable engine's unbuffered daily target rule.",
        r"\mathrm{approximate\ cost\ drag}=c\sum_t\mathrm{traded\ notional}_t/E_t",
        'print("Unbuffered cost approximation:", 0.002 * 2.0)\nprint("Buffered cost approximation:", 0.002 * 1.2)',
        "Write an entry/retention state table for a top-ten, exit-fifteen rule and compare a small validation-only parameter grid with a declared tie-break.",
        "An existing rank-twelve holding stays, a new rank-twelve candidate does not enter, and rank sixteen exits. The illustrative cost drag falls from 0.4% to 0.24%, while delayed exits and changed exposure still require evaluation.",
        [
            (
                "What distinguishes a hysteresis rule?",
                "Different entry and exit thresholds",
                "An entry price chosen after observing the exit",
                "No dependence on current holdings",
                "Hysteresis adds state by allowing retention under a weaker threshold than entry.",
            ),
            (
                "Under top-ten entry and exit beyond fifteen, an existing rank-twelve holding:",
                "Remains eligible for retention",
                "Must always exit",
                "Becomes an automatic new entry",
                "The retention band includes rank twelve even though the new-entry cutoff does not.",
            ),
            (
                "A single excellent parameter surrounded by poor validation results suggests:",
                "Sensitivity requiring investigation",
                "Guaranteed generalization",
                "No need to count attempted settings",
                "An isolated optimum may depend on noise or fragile implementation assumptions.",
            ),
            (
                "Which tie-break can be fixed before the final test?",
                "Lower turnover among validation-qualified candidates",
                "Whichever later wins the holdout",
                "The most favorable future drawdown",
                "A predeclared selection rule avoids using the final result to choose the candidate.",
            ),
        ],
        [PBO, MOMENTUM],
    )

    add(
        "4.3",
        "Statistical arbitrage pairs",
        "Construct a spread with an explicit hedge definition and interpretable entry signal.",
        "A pairs hypothesis proposes that a relationship between two assets is sufficiently stable to support a spread trade. Start with an economic connection, then define whether the spread uses price levels, log prices or returns. The units of the hedge coefficient depend on that choice. A coefficient estimated in log prices is not automatically the number of shares to short.\n\nEstimate the hedge ratio and reference distribution from information available before the trade. Define the formation window, re-estimation schedule, entry, exit, stop and maximum holding period. Standardizing a spread makes its deviation interpretable but does not make convergence certain. Hedging notional, market beta and statistical spread exposure are different objectives; identify which one the proposed trade targets.",
        "A price-level spread is A − 2B. With A at 108 and B at 50, the spread is 8. A prior mean of 2 and standard deviation of 3 give z = 2. A short-spread trade sells one A and buys two B before sizing; its notionals are 108 short and 100 long, so it is not exactly dollar-neutral.",
        "Write both share legs and their signs beside every z-score. Compare the same pair under a dollar-neutral hedge and explain why the statistical spread changes. This lesson's worksheet calculates the case; a real two-leg engine is an extension beyond the supplied long-only project.",
        r"s_t=A_t-\beta B_t,\qquad z_t=(s_t-\mu_{\mathrm{past}})/\sigma_{\mathrm{past}}",
        'spread = 108 - 2 * 50\nprint("Spread:", spread)\nprint("Spread z-score:", (spread - 2) / 3)\nprint("Short minus long notional:", 108 - 2 * 50)',
        "Calculate the spread and z-score, state the short-spread legs in shares and currency, and distinguish statistical, dollar and beta neutrality.",
        "The spread is 8 and z is 2. Selling one A and buying two B gives 108 short versus 100 long. The price-level coefficient defines the spread but does not guarantee dollar or beta neutrality or convergence.",
        [
            (
                "A price-level coefficient of two in A−2B indicates:",
                "Two B shares per A share in the defined spread",
                "Exactly equal dollar notionals at every price",
                "Certain mean reversion",
                "The coefficient defines spread units; its dollar exposure changes with prices.",
            ),
            (
                "Shorting A−2B means:",
                "Sell one A and buy two B before sizing",
                "Buy one A and sell two B",
                "Buy both legs equally",
                "Shorting the spread reverses its positive A and negative B positions.",
            ),
            (
                "A log-price hedge coefficient can be used directly as a fixed share ratio:",
                "Only after a justified conversion; not automatically",
                "Always without considering prices",
                "Only when the test return is positive",
                "Log-price exposure and share quantities have different units and need an explicit sizing conversion.",
            ),
            (
                "A z-score threshold by itself establishes:",
                "A standardized deviation under the fitted reference distribution",
                "A guaranteed convergence date",
                "That borrow is available",
                "Standardization describes the observed deviation but does not prove an executable profitable trade.",
            ),
        ],
        [COINT, LEAKAGE],
    )

    add(
        "4.19",
        "Cointegration, stationarity and half-life diagnostics",
        "Use statistical diagnostics as conditional evidence rather than a guarantee of spread stability.",
        "High return correlation does not establish that a price-level spread is stationary. Two integrated price series can share short-run movements while their difference wanders. An Engle–Granger cointegration test assesses a particular residual relationship under stated assumptions; its null is no cointegration. Check the integration assumptions, deterministic terms, lag selection and sample size before interpreting the result.\n\nTesting many candidate pairs creates selection bias even when each individual p-value is correctly computed. Reserve later windows to examine persistence and record every pair considered. A discrete AR(1) approximation can summarize local mean-reversion speed when its coefficient lies strictly between zero and one. Coefficients near one imply long, uncertain half-lives; structural changes can invalidate both the estimate and the trading horizon.",
        "For a spread deviation following x[t+1] = 0.8x[t] with no new shock, an initial deviation of 10 becomes 5.12 after three steps and 4.096 after four. Its model half-life lies between three and four observations. This conditional decay calculation says nothing about new shocks, changing coefficients or actual execution costs.",
        "Read the cointegration test's assumptions and write the null in words. Use the [econometrics course](/curriculum/econometrics) for estimation and diagnostics, then design a formation/validation split and a pair-search ledger before ranking p-values.",
        r"h=-\log(2)/\log(\phi),\qquad 0<\phi<1",
        'print("Deviation after three steps:", 10 * 0.8 ** 3)\nprint("Deviation after four steps:", 10 * 0.8 ** 4)',
        "Explain the cointegration null, list the model assumptions, bracket the example half-life, and design a later-window stability test that includes all searched pairs.",
        "The null is no cointegration under the test specification. The noiseless AR(1) half-life lies between three and four steps. Neither a small selected p-value nor a short estimated half-life guarantees future stationarity or profitable convergence.",
        [
            (
                "The Engle–Granger test's null hypothesis is:",
                "No cointegration under the specified model",
                "Guaranteed profitable convergence",
                "Equal bid and ask prices",
                "The test evaluates evidence against no cointegration, conditional on its assumptions.",
            ),
            (
                "A noiseless 0.8 AR coefficient takes a deviation of 10 after three steps to:",
                "5.12",
                "8",
                "2",
                "Repeated multiplication gives 10 × 0.8 cubed = 5.12.",
            ),
            (
                "Choosing the smallest p-value among hundreds of pairs requires disclosure of:",
                "The full search and independent stability evidence",
                "Only the selected pair's name",
                "Only the final chart dimensions",
                "Multiple searched hypotheses change the interpretation of the selected result.",
            ),
            (
                "High return correlation alone proves a stationary price spread:",
                "No; these are different properties",
                "Yes for every pair",
                "Yes if both prices are positive",
                "Correlated returns do not ensure a stable linear relationship between price levels.",
            ),
        ],
        [COINT, PBO],
    )

    add(
        "4.20",
        "Borrow, two-leg execution and asynchronous risk",
        "Price the full pair trade and handle the case where only one leg fills.",
        "A statistical spread is not an atomic exchange order unless a specific execution mechanism makes it so. One leg may fill while the other is rejected or delayed, leaving directional exposure. Record order identifiers, partial fills, residual hedge, timeout, cancel and unwind policies. An attractive close-to-close spread change cannot reveal whether the two legs were available at those prices.\n\nShort exposure needs borrow availability, a fee convention, collateral and recall handling. Borrow rates and shares available can change during the holding period. Charge commissions and spread on both legs and use gross capital or a clearly stated margin convention when reporting returns. Dividing a long-short profit by near-zero net notional creates a meaningless return denominator.",
        "A pair has 10,000 long and 10,000 short. A 0.1% fee on each of four entry/exit legs costs about 40 if notionals stay constant. Borrow at 6% annually on 10,000 for 30/360 of a year adds 50 under the declared simple convention. A 120 gross gain leaves only 30 before spread, impact and financing.",
        "Write a state table for both filled, long-only filled, short-only filled, rejected borrow and recall. Define a maximum unhedged interval and a cash-reserved unwind action. These are design exercises; the supplied long-only engine does not pretend to simulate short borrow or atomic pair fills.",
        r"\Pi_{\mathrm{net}}=\Pi_{\mathrm{gross}}-\sum_{\mathrm{legs}}\mathrm{fees}-N_{\mathrm{short}}r_b d/D",
        'fees = 4 * 10000 * 0.001\nborrow = 10000 * 0.06 * 30 / 360\nprint("Pair fees:", fees)\nprint("Borrow cost:", borrow)\nprint("Remaining profit:", 120 - fees - borrow)',
        "Reconcile the pair's costs and specify a one-leg-fill timeout, unwind policy, borrow rejection and recall response. Choose and justify a return denominator.",
        "Fees total 40 and borrow 50, leaving 30 before other costs. A one-leg fill creates directional exposure and needs an explicit response. Use committed capital or another documented economic denominator, never near-zero net notional.",
        [
            (
                "One filled leg of a pair creates:",
                "Potential unhedged directional exposure",
                "Automatic atomic execution of the other leg",
                "Zero risk because the spread was stationary",
                "Actual holdings follow fills, so a delayed second leg leaves unmatched exposure.",
            ),
            (
                "Borrowing 10000 at 6% for 30/360 year costs:",
                "50",
                "600",
                "5",
                "Under the stated simple convention, 10000 × 0.06 × 30/360 equals 50.",
            ),
            (
                "A long-short profit divided by nearly zero net notional is:",
                "An unsuitable return measure without an economic capital basis",
                "Always the correct portfolio return",
                "Equivalent to return on gross exposure",
                "Offsetting notionals do not eliminate the capital, collateral or risk supporting the trade.",
            ),
            (
                "What must a short strategy do when borrow is unavailable?",
                "Follow the declared rejection or alternative-position policy",
                "Assume free unlimited borrowing",
                "Erase the attempted order",
                "Borrow is an implementation constraint and failed availability belongs in the event record.",
            ),
        ],
        [COINT, PBO],
    )

    add(
        "4.21",
        "Relationship breaks and pairs research capstone",
        "Decide when new information invalidates a spread and design an auditable pair experiment.",
        "A spread relationship can break after a merger, a capital-structure change, a business divestiture or a persistent shift in input economics. A widening z-score may therefore reflect a new equilibrium rather than a larger bargain. Monitor both statistical behavior and the economic link. Define observation windows and stop rules before looking at the most dramatic historical episode.\n\nSeparate a trading stop from model re-estimation. A stop bounds a particular position under imperfect execution; it does not prove the model is wrong or cap loss through every gap. Re-estimation changes the model and needs later validation. Averaging down increases exposure to the same unverified relationship. Record a maximum holding time and borrow/hedge limits even if the original statistical fit was strong.",
        "A spread enters at z = 2, has a planned exit at 0.5 and a risk exit at 3.5. A structural announcement moves it from 3.2 to 4.2 overnight. The strategy cannot assume execution at 3.5 through the gap; the actual next executable prices determine the loss on both legs.",
        "Complete a pair research protocol with formation sample, hedge units, diagnostics, entry/exit policy, two-leg costs and a break scenario. Compare it with the single-asset engine contract and list the additional events needed before a pairs extension could be considered implemented.",
        r"\mathrm{exit\ reason}\in\{\mathrm{convergence},\mathrm{risk},\mathrm{time},\mathrm{borrow},\mathrm{thesis\ break}\}",
        'print("Convergence exit:", 4.2 <= 0.5)\nprint("Risk threshold breached:", 4.2 >= 3.5)\nprint("Gap beyond threshold:", 4.2 - 3.5)',
        "Deliver a pair protocol and an adverse-event replay. Distinguish a stop breach, executable unwind, model invalidation and a proposed re-estimation experiment.",
        "The observed z of 4.2 breaches the 3.5 threshold but does not grant a fill at that threshold. Report actual leg prices, the structural event, residual exposure and whether the economic relationship still warrants a new experiment.",
        [
            (
                "A merger permanently changes one company's economics. A widening spread may indicate:",
                "A new relationship rather than a larger convergence opportunity",
                "A guaranteed larger arbitrage",
                "That costs can be ignored",
                "Structural events can invalidate the economic basis of a historical spread.",
            ),
            (
                "A z-score gap from 3.2 to 4.2 crosses a 3.5 stop. The stop guarantees:",
                "Neither an exact threshold fill nor a fixed maximum loss",
                "A fill precisely at 3.5",
                "Immediate free execution of both legs",
                "Thresholds trigger actions; executable prices and gaps determine realized losses.",
            ),
            (
                "Re-estimating the hedge after a break should be treated as:",
                "A revised model needing later validation",
                "Proof the old model never failed",
                "A reason to remove the loss",
                "New parameters change the hypothesis and cannot retroactively repair its historical trade.",
            ),
            (
                "A complete pairs protocol needs which exit reasons beyond convergence?",
                "Risk, time, borrow and thesis invalidation",
                "Only a desired profit target",
                "Only the latest model fit",
                "Operational and economic failures can require exit even without mean reversion.",
            ),
        ],
        [COINT, PBO],
    )

    add(
        "4.4",
        "Cross-sectional machine learning",
        "Turn time-valid predictions into a researchable allocation with a simple baseline.",
        "A stock-prediction model is one component in a strategy. Define the observable features, tradable target, training dates, refit schedule, prediction output and rule converting predictions to positions. A lower prediction error does not by itself establish better portfolio returns: ranking, turnover, costs and constraints mediate the economic outcome. Begin with a simple factor rank and a regularized linear model before adding flexible alternatives.\n\nFit imputation, scaling, feature selection and model parameters within training data. Keep all stocks from a date together and purge overlapping forward labels. A cross-sectional ranking at a decision time can use the available cross-section, but a learned preprocessing pipeline cannot learn from the future test distribution. Record model and feature versions alongside every prediction so an execution audit can identify what was actually used.",
        "A single-feature ridge fit without an intercept has sum(xy) = 6 and sum(x²) = 4. With penalty 2, the coefficient is 1 rather than the unpenalized 1.5. This arithmetic illustrates shrinkage; choosing the penalty after seeing the holdout would still contaminate evaluation, and the example is not a complete trained stock model.",
        "Write the prediction-to-position contract and compare a frozen rank baseline. Continue to the [full stock-ML lifecycle](/curriculum/stock-machine-learning) for fitted pipelines, training and evaluation; return here to audit timing, sizing and after-cost portfolio evidence.",
        r"\widehat\beta=\arg\min_\beta\{\|y-X\beta\|_2^2+\lambda\|\beta\|_2^2\}",
        'print("Unpenalized coefficient:", 6 / 4)\nprint("Ridge coefficient:", 6 / (4 + 2))',
        "Specify feature, label, fit and prediction timestamps, compute the ridge example, and define how a prediction becomes a constrained position compared with a factor-rank baseline.",
        "The coefficients are 1.5 without penalty and 1 with penalty 2. Fit every learned transformation on retained training rows; keep model quality, rank quality and net portfolio performance as separate claims.",
        [
            (
                "A lower stock-return prediction error necessarily produces higher net portfolio returns:",
                "No; allocation, turnover and costs also matter",
                "Yes for any trading rule",
                "Yes if the model is nonlinear",
                "Prediction loss and implemented portfolio economics measure different outcomes.",
            ),
            (
                "For sum(xy)=6, sum(x²)=4 and ridge penalty 2, the coefficient is:",
                "1",
                "1.5",
                "3",
                "In this no-intercept single-feature case, ridge gives 6/(4+2)=1.",
            ),
            (
                "Which record allows a fill to be linked to the model that requested it?",
                "Versioned predictions with decision and model timestamps",
                "Only the model's marketing name",
                "The final chart screenshot",
                "Prediction provenance connects trained artifacts to the resulting orders.",
            ),
            (
                "What is a useful first comparator for a complex cross-sectional model?",
                "A time-valid simple factor rank under the same portfolio rule",
                "Only the weakest random test result",
                "An unrelated asset with a different calendar",
                "A matched simple baseline tests whether model complexity contributes useful evidence.",
            ),
        ],
        [LEAKAGE, PBO],
    )

    add(
        "4.22",
        "Walk-forward model selection and nested validation",
        "Separate hyperparameter selection from evaluation of the selected training procedure.",
        "A walk-forward experiment repeatedly fits on past information and evaluates on a later block. If hyperparameters are selected within that process, use inner training/validation splits restricted to the outer training history. The outer block then evaluates the whole selection procedure rather than a model chosen with knowledge of that block. Purge label overlaps at every relevant boundary, not just the final split.\n\nSpecify expanding versus rolling history, training-window length, retraining frequency and what happens when too little valid data remain. A model can use earlier evaluation observations once they become past data in a later live-like refit, but the original evaluation prediction must remain frozen. Chronology determines admissible information; it does not guarantee stationarity or sufficient effective sample size.",
        "An outer fit uses sessions 1–120 and evaluates 121–140. Hyperparameter selection may compare inner fits ending before 120, with their own purges. It cannot choose penalty strength from 121–140. The next outer refit can extend to 140, but it must not overwrite the predictions previously made for that block.",
        "Draw two outer folds and their inner splits, including label-end dates. Record one prediction file per outer evaluation block and merge those frozen files for portfolio evaluation. Use the stock-ML project for executable fitting; the Strategy Lab project demonstrates a simpler fixed candidate selection protocol.",
        r"\theta_k=\operatorname{select}(D_{\mathrm{outer\ train},k}),\qquad \widehat y_{\mathrm{outer\ test},k}=f_{\theta_k}(X_{\mathrm{outer\ test},k})",
        'print("Outer training sessions:", 120)\nprint("Outer evaluation sessions:", 140 - 120)\nprint("Training endpoint precedes evaluation:", 120 < 121)',
        "Draw a nested chronological split and refit schedule for two outer folds. Identify every purge boundary and explain which stored predictions may never be recomputed retrospectively.",
        "Inner selection stays within sessions 1–120 for the first outer fold. Predictions for 121–140 are frozen as originally produced. Later refits may use that now-past data but cannot rewrite earlier evaluation decisions.",
        [
            (
                "Inner hyperparameter selection for an outer fold may use:",
                "Only its permitted outer training history",
                "The outer test outcomes",
                "Future folds' best models",
                "The outer test must evaluate selection without having supplied its choices.",
            ),
            (
                "Sessions 121 through 140 contain how many evaluation sessions?",
                "20",
                "19",
                "140",
                "Inclusive session counting gives 140−121+1=20.",
            ),
            (
                "A later refit learns from an earlier completed evaluation block. What must stay unchanged?",
                "The predictions originally issued for that earlier block",
                "Every future model parameter forever",
                "The total available training history",
                "Live-like refitting can use newly historical data while preserving past prediction provenance.",
            ),
            (
                "Purging overlapping labels belongs at:",
                "Every split boundary where labels cross information sets",
                "Only the very last date",
                "No boundary when data are chronological",
                "Chronological ordering alone does not remove forward-label overlap at inner or outer boundaries.",
            ),
        ],
        [LEAKAGE, PBO],
    )

    add(
        "4.23",
        "Ranking diagnostics and economic usefulness",
        "Relate information coefficients and portfolio spreads to costs and concentration.",
        "A cross-sectional information coefficient measures association between predicted scores and later outcomes at a date. Rank correlation emphasizes ordering rather than return calibration. Compute diagnostics by date and inspect their distribution rather than pooling every stock-date into one impressive number. Observations share market shocks and overlapping labels, so a naive count of rows can overstate independent evidence.\n\nRank buckets and top-minus-bottom returns help explain the shape of a signal, but a long-short diagnostic is not the same as an implementable long-only portfolio. Compare the actual selected names, turnover, sector exposures and capacity. A weak global rank correlation can coexist with useful tail separation, while a positive correlation can disappear after implementation costs. Keep both the statistical and economic views visible.",
        "Across three assets, predicted ranks [1,2,3] and realized ranks [2,1,3] have squared rank differences totaling 2. With no ties, Spearman correlation is 1 − 6×2/(3×(3²−1)) = 0.5. This tiny fictional cross-section provides a calculation check, not evidence of a persistent signal.",
        "Reproduce the rank coefficient, then write a dated diagnostic table with bucket returns, selected-name concentration and traded notional. State how ties are ranked. Link every claimed net return to the engine's holdings and ledger, rather than applying an IC directly to capital.",
        r"\rho_s=1-\frac{6\sum_i d_i^2}{n(n^2-1)}\quad\mathrm{(no\ ties)}",
        'print("Rank IC:", 1 - 6 * 2 / (3 * (3 ** 2 - 1)))\nprint("Net edge after turnover cost:", 0.003 - 0.002 * 2)',
        "Compute the rank IC, explain why three stocks are insufficient evidence, and design a date-by-date table connecting rank separation with after-cost holdings.",
        "The no-tie rank coefficient is 0.5. Dependence, sample size and selection limit its interpretation; a 0.3% gross edge with turnover 2 and cost 0.2% per traded notional becomes −0.1% under the approximation.",
        [
            (
                "A rank information coefficient primarily evaluates:",
                "Ordering association between scores and subsequent outcomes",
                "Exact trade-fill probability",
                "Whether borrowing is free",
                "Rank correlation measures ordering, not execution or the full portfolio return.",
            ),
            (
                "For n=3 with squared rank differences totaling 2, no-tie Spearman correlation is:",
                "0.5",
                "1",
                "−0.5",
                "Substitute into 1−6×2/(3×8) to obtain 0.5.",
            ),
            (
                "A long-short bucket spread can be labeled as a long-only strategy return:",
                "Only after constructing and evaluating the actual long-only allocation",
                "Automatically without sizing",
                "Whenever its IC is positive",
                "Diagnostic portfolios and implemented holdings have different exposures and costs.",
            ),
            (
                "Why report IC by date rather than only pooling all stock rows?",
                "To inspect time variation and shared-date dependence",
                "To guarantee statistical significance",
                "To eliminate every missing value",
                "Date-level diagnostics expose instability obscured by a single pooled correlation.",
            ),
        ],
        [FACTORS, LEAKAGE],
    )

    add(
        "4.24",
        "Ablations, negative controls and model failure analysis",
        "Test whether added complexity contributes evidence and detect suspiciously good results.",
        "An ablation removes or simplifies a component while preserving the surrounding experiment. Compare value-only with value-plus-quality, a fixed rank with a trained model, and the same signal under slower execution. Match sample, costs and constraints so a difference has an interpretable cause. An ablation is another trial; do not report only the one that favors the preferred model.\n\nNegative controls probe the research machinery. Random labels or deliberately uninformative features should not reliably produce exceptional independent predictions. If they do, investigate leakage, selection and evaluation code before celebrating the original signal. Shuffling must respect the question and dependence structure; indiscriminate row shuffling can remove time dependence and create an unrealistically easy null. Controls diagnose problems, but passing them does not prove a real economic advantage.",
        "A baseline has validation net return 4%, an added feature raises it to 4.1%, and doubling modeled costs reduces the new rule to 1%. If the feature also triples turnover, the incremental prediction result may have little implementation value. A random-label run that appears excellent warrants an audit of label timing and the full search count.",
        "Create an ablation matrix with one changed element per row and retain losses. Use a fixed seed for controls and record their construction. For a failed experiment, write whether the mechanism, data, model, portfolio or execution assumption was challenged.",
        r"\Delta_{\mathrm{ablation}}=M(\mathrm{full\ rule})-M(\mathrm{matched\ simpler\ rule})",
        'print("Incremental validation return:", 0.041 - 0.04)\nprint("Return lost in cost stress:", 0.041 - 0.01)',
        "Design three matched ablations and one negative control. Interpret the 0.1-percentage-point feature gain alongside turnover and cost stress, and write a failure diagnosis.",
        "The added feature gains only 0.1 percentage point in validation while cost stress removes 3.1 points. Matched ablations isolate a change; unexpectedly strong random-label results require a leakage and selection audit rather than a profitability claim.",
        [
            (
                "A matched ablation changes:",
                "One component while keeping the comparison conditions fixed",
                "Every parameter and the benchmark together",
                "Only the chart title",
                "Controlled changes make an observed difference interpretable.",
            ),
            (
                "Validation return rising from 4% to 4.1% is an improvement of:",
                "0.1 percentage point",
                "4.1 percentage points",
                "10 percentage points",
                "Subtracting percentage returns gives 4.1−4=0.1 percentage point.",
            ),
            (
                "Excellent independent-looking performance on random labels should first trigger:",
                "An audit of leakage, selection and evaluation code",
                "Immediate confidence in market predictability",
                "Deletion of the control result",
                "An uninformative target performing exceptionally can reveal a broken research process.",
            ),
            (
                "Passing a negative-control check establishes:",
                "Only that this diagnostic did not reveal the tested failure",
                "Guaranteed economic alpha",
                "Freedom from every possible implementation error",
                "A diagnostic has a defined scope and cannot certify all assumptions.",
            ),
        ],
        [LEAKAGE, PBO],
    )

    add(
        "4.25",
        "Position sizing, exposure caps and volatility targets",
        "Translate a score into bounded exposure while treating risk estimates as uncertain.",
        "A signal says which exposure is preferred; sizing determines how much risk reaches the portfolio. Start with equal weights, a single-name cap, a gross exposure limit and a cash rule. Integer shares, lot sizes and next-open gaps mean realized weights differ from target weights. Record requested and filled quantities so a cash constraint cannot silently appear as a better signal.\n\nVolatility targeting scales exposure using a past estimate of risk. Specify the return horizon, estimator, floor, rebalance frequency and leverage cap. A low recent estimate can otherwise produce excessive leverage just before a shock. Volatility is not a complete loss model: gaps, correlation changes and illiquidity remain possible. Use stress scenarios and capital constraints alongside the estimate rather than interpreting a target as a guaranteed realized volatility.",
        "A 10% target divided by a 20% annualized estimate suggests 0.5 times exposure. If the estimate falls to 4%, the raw multiplier is 2.5; a declared 1.2 cap limits it to 1.2. The resulting future volatility can still exceed 10% if conditions change.",
        "Calculate target and capped exposure, then convert a 40% weight on 10,000 equity at a 103 close into 38 whole shares. Explain how a next-open gap and fees can reduce the actual purchase. The lab uses long-only caps without volatility leverage; targeting is a tested extension assignment.",
        r"g_t=\min(g_{\max},\sigma_{\mathrm{target}}/\max(\widehat\sigma_t,\sigma_{\min}))",
        'print("Normal risk multiplier:", 0.10 / 0.20)\nprint("Capped low-volatility multiplier:", min(1.2, 0.10 / 0.04))\nprint("Whole-share target:", int(10000 * 0.4 / 103))',
        "Specify a sizing policy with volatility floor, leverage and single-name caps. Reconcile target weight to integer shares and explain which risks a volatility estimate does not capture.",
        "The multipliers are 0.5 and capped 1.2. A 4,000 target at 103 yields 38 whole shares before next-open affordability. Volatility targets are conditional estimates; they cannot guarantee drawdown, liquidity or future realized risk.",
        [
            (
                "A 10% target divided by a 20% volatility estimate suggests exposure of:",
                "0.5 times",
                "2 times",
                "10 times",
                "The target-to-estimate ratio is 0.10/0.20=0.5.",
            ),
            (
                "Why cap a volatility-targeting multiplier?",
                "Low estimated risk can otherwise imply excessive exposure",
                "To guarantee no future loss",
                "To eliminate all correlation changes",
                "A noisy or unusually low estimate can produce an imprudently large raw multiplier.",
            ),
            (
                "A 40% target on 10000 equity at price 103 requests how many whole shares?",
                "38",
                "40",
                "39",
                "Flooring 4000/103 gives 38 shares before next-open execution constraints.",
            ),
            (
                "Realized portfolio volatility above its target is:",
                "Possible because the estimate and future conditions differ",
                "Impossible with a formula",
                "Proof that transaction costs are zero",
                "A target uses past estimates and cannot control all future shocks.",
            ),
        ],
        [FACTORS, PBO],
    )

    add(
        "4.26",
        "Covariance, diversification and portfolio constraints",
        "Evaluate joint exposures rather than treating several strategies as independent bets.",
        "Combining strategies changes the portfolio through weights and covariance, not through the number of names alone. Two individually attractive signals may own the same stocks or respond to the same macro factor. Inspect holdings overlap, sector and factor exposures, and correlations of aligned net returns. Correlations estimated in quiet periods may rise during stress, exactly when diversification is most valuable.\n\nA minimum-variance or risk-budget allocation depends on uncertain covariance estimates. Small samples and nearly duplicate strategies can make unconstrained solutions unstable. Compare a simple equal-weight allocation with constrained alternatives, regularize estimates when justified, and report sensitivity. Exposure limits and cash reserves express the mandate; an optimizer should not silently violate them to produce an attractive historical objective.",
        "Two sleeves each have 20% volatility and receive 50% weights. At correlation zero, portfolio variance is 0.02 and volatility about 14.14%. At correlation one, volatility becomes 20%. Merely labeling the sleeves 'value' and 'AI' does not establish the zero-correlation assumption.",
        "Reproduce both covariance cases and build a holdings-overlap table. Add a correlation-one stress to the research notebook, and compare equal weights with a capped candidate allocation using the same net-return calendar.",
        r"\sigma_p^2=w_A^2\sigma_A^2+w_B^2\sigma_B^2+2w_Aw_B\rho\sigma_A\sigma_B",
        'base = 0.5 ** 2 * 0.2 ** 2 * 2\nprint("Uncorrelated portfolio volatility:", base ** 0.5)\nprint("Perfect-correlation volatility:", (base + 2 * 0.5 * 0.5 * 0.2 * 0.2) ** 0.5)',
        "Calculate the two-sleeve risk under zero and perfect correlation, audit holdings overlap and propose constraints for a portfolio whose covariance estimates may be unstable.",
        "Volatility is approximately 14.14% at zero correlation and 20% at correlation one. Diversification depends on joint exposures, while caps, regularization and stress checks reduce reliance on one noisy covariance estimate.",
        [
            (
                "Two equally weighted 20%-volatility sleeves with zero correlation have volatility near:",
                "14.14%",
                "20%",
                "40%",
                "The combined variance is 0.02 and its square root is approximately 0.1414.",
            ),
            (
                "Different strategy names establish independent risk exposures:",
                "No; examine holdings and aligned return covariance",
                "Yes automatically",
                "Only when one name contains AI",
                "Economic and statistical overlap must be measured rather than inferred from labels.",
            ),
            (
                "A covariance optimizer assigns extreme weights after a tiny data change. This suggests:",
                "Estimation sensitivity requiring constraints and diagnostics",
                "A guaranteed superior portfolio",
                "That historical correlation is exact",
                "Unstable weights can amplify noisy covariance estimates.",
            ),
            (
                "Why stress correlations upward?",
                "Diversification can weaken during common shocks",
                "To prove every strategy always loses together",
                "To remove the need for a benchmark",
                "A stressed joint-risk case challenges reliance on quiet-period diversification.",
            ),
        ],
        [FACTORS, PBO],
    )

    add(
        "4.27",
        "Turnover, transaction costs and strategy capacity",
        "State turnover conventions and test whether proposed orders fit plausible liquidity.",
        "Turnover measures trading activity, but conventions differ. The sum of absolute weight changes counts both purchases and sales; half that sum is often called one-way turnover for a fully invested rebalance. Fees assessed per traded notional apply to the full traded amount. Mixing these conventions can understate cost by a factor of two. Keep cash changes and drift assumptions explicit.\n\nCapacity asks whether more capital changes the execution economics. Measure order size relative to an observable liquidity estimate, then consider spread, impact, urgency and participation limits. A fixed fee does not capture market impact, and current-session total volume is unknown at the open. The teaching engine uses a fraction of prior-session volume as a quantity cap; this is a transparent approximation, not a claim about actual opening liquidity.",
        "Weights move from [0.6,0.4] to [0.4,0.6]. Absolute changes total 0.4; one-way turnover is 0.2. At 20 basis points per traded notional, approximate fee drag is 0.0008 of equity. A desired 300-share order with a 5% cap on prior volume of 2,000 can fill at most 100 shares under the lab policy.",
        "Reconcile both turnover conventions, double costs and reduce the participation cap. Compare unfilled quantities and cash across runs. Record that a prior-volume proxy cannot determine the actual order book or spread available at the opening event.",
        r"T_{\mathrm{traded}}=\sum_i|w_i^*-w_i|,\qquad C/E\approx cT_{\mathrm{traded}}",
        'traded = abs(0.4 - 0.6) + abs(0.6 - 0.4)\nprint("Two-sided traded weight:", traded)\nprint("Approximate fee drag:", traded * 0.002)\nprint("Quantity cap:", int(0.05 * 2000))',
        "Compute both turnover measures, reconcile fee drag and fill caps, and design a capital/participation sensitivity with all unfilled orders retained.",
        "Traded weight is 0.4, one-way turnover 0.2 and approximate fee drag 0.08%. The 300-share request is capped at 100 using prior volume; the remainder expires under the project's policy and is visible in the order ledger.",
        [
            (
                "Weights changing from 60/40 to 40/60 produce absolute traded weight of:",
                "0.4",
                "0.2",
                "0",
                "Both the 0.2 sale and 0.2 purchase count toward traded notional.",
            ),
            (
                "At 20 basis points on traded weight 0.4, approximate fee drag is:",
                "0.08%",
                "0.8%",
                "8%",
                "Multiply 0.002 by 0.4 to obtain 0.0008, or 0.08%.",
            ),
            (
                "Using today's total volume to size an opening fill introduces:",
                "Information unavailable at that opening event",
                "A guaranteed realistic queue model",
                "Only a harmless unit conversion",
                "The session's eventual total volume is future information at its open.",
            ),
            (
                "A fixed commission rate alone models strategy capacity adequately:",
                "No; liquidity and market impact also matter",
                "Yes for arbitrarily large orders",
                "Only if gross returns are high",
                "Trading more capital can change fill prices and available size beyond fixed fees.",
            ),
        ],
        [LEAKAGE, PBO],
    )

    add(
        "4.28",
        "Portfolio accounting and independent engine checks",
        "Reconcile cash, holdings, fees and wealth with a hand-calculated event ledger.",
        "Before interpreting performance, prove that the engine accounts for its own events. Each fill changes shares and cash once, fees are charged once, and wealth equals cash plus marked holdings. Process sells before buys if that is the declared rebalance convention, maintain deterministic allocation when cash is scarce, and record partial fills. A correct signal with incorrect accounting produces an invalid research result.\n\nUse tiny independent fixtures with obvious expected answers: constant prices, an overnight gap, one profitable round trip, one losing round trip, insufficient cash and a final unexecuted signal. Compare event-ledger arithmetic with the wealth path. Tests that simply repeat the implementation's formula are weaker than a separately worked cash ledger. Mark remaining holdings at the end and disclose whether liquidation costs are included.",
        "Start with 1,000. Buy two shares at the next open of 100 with a 1% fee: cash becomes 798. Sell both at a later open of 110 with a 1% fee: proceeds are 217.8 and final cash is 1,015.8. Gross gain is 20, fees total 4.2 and net gain is 15.8.",
        "Run the archive's unit tests and reconcile the fixed trade fixture without reading the implementation first. Inspect positions.csv and verify cash plus closing market value equals equity on every row. Confirm the first signal cannot earn a return before its next-open fill.",
        r"E_t=C_t+\sum_i q_{i,t}P_{i,t},\qquad \Pi_{\mathrm{net}}=\Pi_{\mathrm{gross}}-\mathrm{fees}",
        'cash_after_buy = 1000 - 2 * 100 * 1.01\nfinal_cash = cash_after_buy + 2 * 110 * 0.99\nprint("Cash after buy:", cash_after_buy)\nprint("Round-trip final equity:", final_cash)\nprint("Total fees:", 2 * 100 * 0.01 + 2 * 110 * 0.01)',
        "Produce the full cash/holding ledger for the round trip and specify independent assertions for causality, fee charging, partial fills and final valuation.",
        "Cash is 798 after buying and 1,015.8 after selling; fees are 4.2. Every row must reconcile equity to cash plus holdings. Ending open positions are marked, not silently liquidated for free.",
        [
            (
                "Two shares at 100 with a 1% purchase fee from 1000 leave cash of:",
                "798",
                "800",
                "802",
                "The purchase costs 200 plus a fee of 2.",
            ),
            (
                "Selling those two shares at 110 with a 1% sale fee leaves final equity of:",
                "1015.8",
                "1020",
                "1018",
                "Sale proceeds are 220−2.2=217.8, added to the remaining 798 cash.",
            ),
            (
                "Which invariant should hold on every valuation row?",
                "Equity equals cash plus marked holdings",
                "Equity equals only invested notional",
                "Fees are added back to cash",
                "Portfolio wealth reconciles the cash account and current value of all holdings.",
            ),
            (
                "Open positions at the final mark should be described as:",
                "Marked holdings with liquidation costs omitted unless explicitly modeled",
                "Automatically liquidated at no cost",
                "Realized cash profits regardless of sales",
                "A closing mark and an executed liquidation are different economic events.",
            ),
        ],
        [LEAKAGE, PBO],
    )

    add(
        "4.29",
        "Chronological validation and untouched evaluation",
        "Select a candidate on validation data and evaluate its frozen rule on a later segment.",
        "A research comparison needs a selection protocol, not only a train/test label. Fix the candidate list, development period, validation objective, tie-break and final evaluation window. Use development fixtures to find implementation errors, then select the candidate using validation outcomes only. Freeze the specification before revealing the final segment and record that the segment has now been consumed.\n\nA reset evaluation and a continuous walk-forward simulation answer different questions. The supplied project starts each validation and test account in cash at the preceding decision close, with historical observations available only for indicator warm-up. No earlier holdings are imported. A continuous strategy would carry holdings and accounting state across the boundary; implement and disclose that separately. Short synthetic segments exercise this procedure but cannot provide convincing market evidence.",
        "Validation net returns for equal-weight, value-quality and momentum are 2%, 3% and 1%. The predeclared highest-return rule selects value-quality. If the later test returns −4%, the result remains −4%; selecting equal-weight after seeing test outcomes would turn that segment into another selection sample.",
        "Run strategy_lab.py and inspect experiments.json. Confirm the winner depends only on validation rows. Open the selected strategy's test export after writing your prediction in the notebook. The program evaluates only the selected candidate on the final segment; repeated manual trials still need disclosure.",
        r"j^*=\arg\max_j R_{j,\mathrm{validation}},\qquad R_{\mathrm{reported}}=R_{j^*,\mathrm{test}}",
        'print("Selected validation return:", max(0.02, 0.03, 0.01))\nprint("Retained test outcome:", -0.04)',
        "Write the fixed candidate list, split endpoints and tie-break, identify the selected candidate, and explain why the negative test outcome must remain in the record.",
        "Value-quality wins validation at 3%. Its later −4% remains the evaluation outcome. A new choice based on that result requires new independent evidence. State whether each boundary resets cash or carries positions.",
        [
            (
                "With validation returns 2%, 3% and 1%, a highest-return selection chooses:",
                "The second candidate",
                "The candidate with the best unseen test outcome",
                "All candidates retroactively",
                "Selection uses the declared validation objective before final outcomes are inspected.",
            ),
            (
                "The selected candidate later returns −4%. The evaluation record should:",
                "Retain −4% with its limitations",
                "Replace it with the best test candidate",
                "Delete the final segment",
                "Negative independent outcomes are evidence and cannot be removed to preserve the thesis.",
            ),
            (
                "A reset test account differs from a continuous simulation because:",
                "It starts in cash instead of carrying prior holdings",
                "It can use future prices freely",
                "It guarantees lower risk",
                "Boundary state affects trades and returns and must be part of the evaluation contract.",
            ),
            (
                "Indicator warm-up before a test boundary may use:",
                "Historical observations available before each decision",
                "All future test closes",
                "The winning test ranking",
                "Past data can initialize indicators without allowing future evaluation information into decisions.",
            ),
        ],
        [PBO, LEAKAGE],
    )

    add(
        "4.30",
        "Multiple testing, uncertainty and honest inference",
        "Interpret a selected backtest in light of search effort and dependent observations.",
        "The best result among many noisy trials tends to look better than its underlying process. Count families, features, windows, costs, benchmarks and informal revisions, not just the final grid. A nominal p-value or Sharpe estimate for the selected winner does not automatically account for that search. The probability-of-backtest-overfitting literature formalizes aspects of selection; citing it is not the same as implementing its procedure.\n\nReturns also exhibit dependence and changing regimes. A row-wise bootstrap may break serial structure, while a block bootstrap preserves some local dependence under its own stationarity and block-length assumptions. Uncertainty intervals from one selected series remain conditional on selection unless the procedure explicitly models the search. Use descriptive intervals, independent periods and economic reasoning together, and distinguish a failed rejection from proof that no effect exists.",
        "If twenty independent null tests each have a 5% false-positive probability, the chance of at least one false positive is 1 − 0.95²⁰, about 64.15%. Real strategy trials are usually dependent, so this is an illustrative independence calculation rather than the exact probability for a research grid.",
        "Record the complete trial count and identify dependencies among settings. Use the final reporting course's block-uncertainty tool for a descriptive interval, explicitly retaining its selection caveat. Do not label a simple count or bootstrap as a computed PBO estimate.",
        r"\Pr(\mathrm{at\ least\ one\ false\ positive})=1-(1-\alpha)^m\quad\mathrm{(independent\ nulls)}",
        'print("Illustrative family false-positive probability:", 1 - 0.95 ** 20)',
        "Calculate the independent-null example, inventory all research choices and propose an uncertainty analysis whose dependence and selection assumptions are explicit.",
        "The illustrative probability is about 64.15%. Correlated trials need a different joint model, and a bootstrap of the selected return series alone does not correct the full selection process. Disclose what was actually computed.",
        [
            (
                "Reporting only the best of many tried strategies tends to introduce:",
                "Selection optimism",
                "Automatic out-of-sample validity",
                "A complete multiple-testing correction",
                "Selecting the maximum of noisy outcomes favors positive estimation errors.",
            ),
            (
                "Twenty independent 5% null tests have at least one false-positive probability near:",
                "64.15%",
                "5%",
                "100% exactly",
                "Under independence, the complement of no false positives is 1−0.95 to the twentieth power.",
            ),
            (
                "A block interval computed on a selected winner automatically corrects all strategy search:",
                "No; selection must be addressed explicitly",
                "Yes regardless of the search",
                "Only if the chart has confidence bands",
                "Resampling one selected path does not reproduce the process that selected it.",
            ),
            (
                "Citing a PBO paper allows a report to claim it computed PBO:",
                "Only if the stated procedure was actually implemented and validated",
                "Without running any calculation",
                "Whenever there are at least two trials",
                "Method attribution does not substitute for performing and checking the claimed analysis.",
            ),
        ],
        [PBO, LEAKAGE],
    )

    add(
        "4.31",
        "Stress experiments and implementation readiness",
        "Challenge a frozen strategy with adverse costs, delays, liquidity and concentration.",
        "Stress tests ask how the proposed rule behaves when an assumption becomes less favorable. Keep the candidate fixed while increasing costs, tightening a prior-volume participation cap, delaying execution, removing a feature or imposing a concentration shock. Preserve the base input identity when testing one changed assumption so the comparison remains interpretable. A stress is a scenario, not a prediction of its probability.\n\nSeparate implementation readiness from expected profitability. Correct accounting, deterministic replay and clean inputs support engineering confidence. Later independent performance, an economic mechanism and robust implementation assumptions support a research argument. Paper execution adds evidence about data freshness, order handling and reconciliation without proving that live fills will match. Set concrete pause conditions such as stale inputs, irreconcilable holdings or an unexplained model-version change.",
        "A fixed strategy returns 5% at base costs, 1% at doubled costs and −2% under a tighter liquidity cap. The appropriate conclusion identifies execution sensitivity rather than averaging the three into a guaranteed return. If a replay changes earlier fills after only future data are edited, that is a causality defect requiring repair before any performance claim.",
        "Run the download's cost and liquidity stress modes on the selected rule, retain every output and label them as post-selection diagnostics. Propose a one-event execution delay as an extension. Use the Python bot or C/HPC track for subsequent operational implementation.",
        r"\mathrm{stress\ impact}=M(\mathrm{fixed\ rule},\mathrm{adverse\ assumption})-M(\mathrm{fixed\ rule},\mathrm{base})",
        'print("Cost stress change:", 0.01 - 0.05)\nprint("Liquidity stress change:", -0.02 - 0.05)',
        "Produce a stress matrix with fixed source/data identity, isolate changed assumptions, and define three paper-workflow pause conditions and one falsifiable next experiment.",
        "Cost stress changes return by −4 percentage points and liquidity stress by −7. Preserve the sensitivity and distinguish engineering checks from investment evidence. Stale data, mismatched holdings and unexplained model changes are concrete pause conditions.",
        [
            (
                "What should remain fixed when isolating a cost stress?",
                "The strategy, input sample and other execution assumptions",
                "Only the report title",
                "Nothing; choose a new winner each time",
                "A controlled stress changes the named assumption while preserving the comparison basis.",
            ),
            (
                "A base return of 5% falling to −2% under liquidity stress changes by:",
                "−7 percentage points",
                "−3 percentage points",
                "7% guaranteed future loss",
                "Subtract 5% from −2% to get a seven-percentage-point deterioration.",
            ),
            (
                "Editing only future prices changes earlier fills. This indicates:",
                "A causality or data-processing defect",
                "Useful forward prediction",
                "A successful stress test",
                "Decisions and fills in the past must not depend on later observations.",
            ),
            (
                "Successful deterministic replay establishes:",
                "Reproducibility under the tested inputs and implementation",
                "Profitable live execution",
                "An unlimited strategy capacity",
                "Replay checks engineering consistency rather than the economic value of the strategy.",
            ),
        ],
        [PBO, LEAKAGE],
    )

    add(
        "4.32",
        "Capstone: defend a reproducible strategy dossier",
        "Deliver a tested research project, balanced conclusion and evaluation-ready result bundle.",
        "The capstone combines the strategy contract, data audit, experiment ledger, selected rule, order and position records, net wealth path, benchmark and limitations. Reproduce the supplied engine's independent fixtures before studying its fictional results. Then complete one predeclared research extension and show what changed, what remained fixed and what evidence challenged the original idea. A careful negative result is a successful research deliverable.\n\nThe downloadable engine runs equal-weight, value-quality and momentum portfolios with available filings, next-open fills, fees, whole shares, cash and prior-volume caps. It selects on a validation segment, evaluates the frozen choice on a later synthetic segment, and exports two post-selection stresses. Pairs execution, fitted ML, corporate actions and real market adapters are explicit extension work. Do not describe them as implemented merely because their design appears in the course.",
        "Your engine fixture must finish the two-share round trip at 1,015.8 with 4.2 of fees. The 100-point dossier rubric allocates 20 to hypothesis/data, 25 to timing/accounting, 20 to comparison/selection, 20 to stress/limitations and 15 to reproducibility/communication. Unresolved look-ahead or unreconciled cash requires revision regardless of score.",
        "Run the archive tests and project, complete research-notebook.md and inspect the exported CSV/JSON files. Send the base test equity.csv and manifest.json to [algorithm evaluation and reporting](/curriculum/algorithm-evaluation) for the final report, charts and written decision. Continue operational implementation in [Python bots](/curriculum/stock-bots) or [C/HPC](/curriculum/c-hpc-trading) with the same research contract.",
        r"\mathrm{dossier}=\mathrm{specification}+\mathrm{audited\ data}+\mathrm{tested\ execution}+\mathrm{independent\ evaluation}+\mathrm{limitations}",
        'print("Round-trip final equity:", 1000 - 2 * 100 * 1.01 + 2 * 110 * 0.99)\nprint("Strategy rubric total:", 20 + 25 + 20 + 20 + 15)\nprint("Planned study hours:", 32 * 30 / 60)',
        "Deliver the complete dossier and one predeclared extension: source/input identity, data audit, independent engine checks, all validation trials, frozen evaluation, costs/liquidity stresses, trade/position reconciliation, reporting exports, primary references and a reject/revise/paper-study conclusion.",
        "Reproduce 1,015.8 final fixture equity and 4.2 fees. Target at least 80/100 on the separately self-assessed dossier, with no unresolved look-ahead or cash mismatch. Preserve negative outcomes, identify synthetic versus independent data, and distinguish implemented strategies from proposed extensions before handing results to the reporting course.",
        [
            (
                "Which result can the synthetic capstone directly establish?",
                "That the tested implementation follows its documented fixture rules",
                "A real-market return premium",
                "Guaranteed production fills",
                "Synthetic fixtures check behavior and arithmetic, not independent market profitability.",
            ),
            (
                "The dossier rubric 20+25+20+20+15 totals:",
                "100 points",
                "90 points",
                "110 points",
                "The five separately assessed evidence categories sum to 100.",
            ),
            (
                "A high concept-exam score with unreconciled cash means the project:",
                "Still requires revision before its results are credible",
                "Is automatically accepted",
                "Can omit its trade ledger",
                "Concept knowledge does not repair a broken accounting result.",
            ),
            (
                "What should be handed to the final reporting course?",
                "Aligned net valuations, benchmark, manifest and supporting research evidence",
                "Only the maximum backtest return",
                "Invented holdings for an unimplemented pairs engine",
                "The report needs traceable data and assumptions rather than an isolated or fabricated performance claim.",
            ),
        ],
        [PBO, SEC, LEAKAGE],
    )

    return _finish_course(modules)


def _finish_course(modules):
    parts = [
        (
            "Specify the research",
            "Hypotheses, benchmarks, event timing and reproducible experiments.",
        ),
        (
            "Build trustworthy data",
            "As-of filings, historical universes, cleaning and chronological labels.",
        ),
        (
            "Value and quality strategies",
            "Net-net screening, quality ranks, catalysts and fundamental portfolio research.",
        ),
        (
            "Trend, momentum and reversal",
            "Time-series trends, cross-sectional momentum, short-horizon reversal and rule stability.",
        ),
        (
            "Pairs and relative value",
            "Spread construction, stationarity, two-leg execution and relationship breaks.",
        ),
        (
            "Machine learning as a signal",
            "Cross-sectional predictions, nested validation, ranking diagnostics and ablations.",
        ),
        (
            "Portfolio and implementation",
            "Position sizing, covariance, turnover, capacity and accounting.",
        ),
        (
            "Validate and defend a strategy",
            "Walk-forward tests, selection uncertainty, stress experiments and a reproducible capstone.",
        ),
    ]
    return finish(
        {
            "id": "strategy-lab",
            "number": 4,
            "title": "The strategy lab",
            "description": "Design, implement and challenge investment strategies: value and quality, trend and momentum, pairs, machine-learning signals, portfolio construction and realistic backtesting.",
            "source": "Original Quanta course · Graham & Dodd, Kenneth French, SEC, statsmodels, scikit-learn & backtest research",
            "level": "Applied",
            "icon": "lab",
            "studyType": "applied",
            "modules": modules,
            "prerequisites": "Complete quantitative investment analysis and the core econometrics units; Security Analysis supports the fundamental strategies. Basic Python and return arithmetic are useful. The bot, C/HPC and stock-ML tracks provide subsequent implementation depth.",
            "outcomes": [
                "Write falsifiable strategy specifications and reconstruct a point-in-time information set.",
                "Design value, quality, momentum, reversal, pairs and predictive-ranking research experiments.",
                "Convert signals into constrained portfolios with explicit timing, costs and cash accounting.",
                "Run a multi-asset Python lab, inspect orders and compare strategies under matched conventions.",
                "Preserve holdouts, disclose all trials, and challenge results with ablations and adverse assumptions.",
                "Deliver a reproducible research dossier and export results to the final evaluation/reporting course.",
            ],
            "readingGuide": "32 lessons × 30 minutes = 16 hours of planned study across eight units; exam time is additional. Includes 64 practice questions, eight four-question checkpoints, a 32-question final, a downloadable Python research project and a separately self-assessed capstone. Original fictional cases teach research methods; they do not establish real-market profitability. The local engine implements equal-weight, value-quality and momentum portfolios. Pairs and ML receive guided design/calculation labs; their full engines are extension assignments linked to the econometrics and stock-ML courses.",
            "parts": [
                {"id": str(i), "title": t, "description": d} for i, (t, d) in enumerate(parts, 1)
            ],
            "references": [
                {"title": t, "url": u}
                for t, u in [BOOK, SEC, FACTORS, MOMENTUM, COINT, LEAKAGE, PBO]
            ],
            "resources": [
                {
                    "title": "Download the complete Strategy Lab project",
                    "url": "/course-assets/strategy-lab/strategy-research-lab.zip",
                },
                {
                    "title": "Download the research notebook and capstone rubric",
                    "url": "/course-assets/strategy-lab/research-notebook.md",
                },
                {
                    "title": "Download the Strategy Lab project guide",
                    "url": "/course-assets/strategy-lab/README.md",
                },
            ],
        },
        checkpoints_for(modules, parts, 8),
    )
