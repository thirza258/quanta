"""Final synthesis course: original evaluation cases and reproducible reports."""

from applied_courses import checkpoints_for, study
from book_courses import finish

CFA = (
    "CFA Institute · Portfolio performance evaluation",
    "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/portfolio-performance-evaluation",
)
PRESENTATION = (
    "CFA Institute · Fair performance presentation",
    "https://www.cfainstitute.org/standards/professionals/code-ethics-standards/standards-of-practice-iii-d",
)
PBO = (
    "Bailey, Borwein, López de Prado & Zhu · The probability of backtest overfitting",
    "https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf",
)
LEAKAGE = (
    "scikit-learn contributors · Common pitfalls and data leakage",
    "https://scikit-learn.org/stable/common_pitfalls.html",
)
SPLITS = (
    "scikit-learn contributors · TimeSeriesSplit",
    "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html",
)
PLOTS = (
    "Matplotlib contributors · Saving reproducible figures",
    "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html",
)
CLOCK = (
    "Linux man-pages project · Monotonic timing with clock_gettime",
    "https://man7.org/linux/man-pages/man3/clock_gettime.3.html",
)
BOOTSTRAP = (
    "arch contributors · Circular block bootstrap",
    "https://arch.readthedocs.io/en/latest/bootstrap/generated/arch.bootstrap.CircularBlockBootstrap.html",
)


def build_algorithm_evaluation():
    modules = []

    def add(
        title, objective, principle, case, workflow, formula, code, task, solution, questions, refs
    ):
        index = len(modules) + 1
        rows = []
        for offset, (prompt, correct, wrong1, wrong2, explanation) in enumerate(questions):
            options = [correct, wrong1, wrong2]
            shift = (index + offset) % 3
            options = options[shift:] + options[:shift]
            rows.append((prompt, options, options.index(correct), explanation))
        item = study(
            f"10.{index}",
            (index - 1) // 4 + 1,
            title,
            objective,
            principle,
            case,
            workflow
            + "\n\n### Build your evaluation dossier\n\nReproduce the small worksheet before applying the idea to a full run. Save the input, calculation, interpretation and limitation in your notebook. Add the corresponding evidence to the downloadable report notebook. The in-browser Python worksheet remains in cash and is an arithmetic aid; it does not execute the evaluated trading algorithm. Run the downloadable reporting project locally for actual metrics, files and figures. A clear negative result is a valid finding: never remove a losing period or failed experiment to improve the story.",
            formula,
            code,
            task,
            solution,
            rows,
            refs,
        )
        item["minutes"] = 30
        item["reading"] = (
            "30-minute session: 10 minutes reading primary references, 8 minutes reproducing calculations, and 12 minutes assembling or challenging report evidence. All supplied company, return and timing examples are fictional. Evaluate algorithms written in Python, C or other languages through a documented result-export contract."
        )
        modules.append(item)

    add(
        "An evaluation contract before the final result",
        "Define the research question, comparator, evidence, and rejection criteria before judging performance.",
        "The last stage of an algorithm project is a defensible decision, supported by a report another researcher can reproduce. Begin with the hypothesis: which economic or statistical mechanism should produce what behavior, under which market conditions? Specify the eligible universe, information timing, execution rule, cost model and comparator before reviewing a final test result.\n\nSeparate three questions. Is the implementation correct? Is the strategy supported by independent evidence? Is its operational behavior acceptable for the proposed paper workflow? A fast, bug-free algorithm can still have no investment value. A high-return backtest can still contain look-ahead. The report needs an evidence ledger that connects each claim to a dataset, table, figure, test or source.",
        "A researcher promises to evaluate net return, drawdown, benchmark difference and data freshness. The test returns 12% but breaches a predeclared 10% drawdown limit. The report must retain the breach; changing the limit afterward creates a revised hypothesis that needs new evidence.",
        "Start report-notebook.md. Write the intended reader and a reject/revise/paper-study decision framework. Link the implementation contract to the Python bot or C/HPC project you completed, keeping strategy quality separate from computing speed.",
        r"\mathrm{decision}=f(\mathrm{predeclared\ criteria},\mathrm{evidence},\mathrm{uncertainty})",
        'return_net = 0.12\ndrawdown = 0.14\nlimit = 0.10\nprint("Return:", return_net)\nprint("Drawdown criterion met:", drawdown <= limit)',
        "Write a one-paragraph evaluation contract with a hypothesis, benchmark, cost basis, holdout rule, three rejection criteria and a named evidence artifact for each criterion.",
        "A complete contract separates model correctness, independent performance and operations. Define thresholds before final evaluation; preserve any breach in the report. A revised threshold is a new research choice, not proof that the original criterion was met.",
        [
            (
                "When should final evaluation criteria be specified?",
                "Before examining the final test result",
                "After selecting the best return",
                "Only after publishing a chart",
                "Predeclared criteria reduce the freedom to rewrite success around observed outcomes.",
            ),
            (
                "Which claim can a fast C implementation establish by itself?",
                "Only measured computing behavior under its test conditions",
                "Positive expected investment returns",
                "Absence of look-ahead in every dataset",
                "Systems performance is a separate claim from strategy validity and data correctness.",
            ),
            (
                "A report breaches a predeclared risk threshold but has a high return. The breach should:",
                "Remain visible and affect the decision",
                "Be hidden behind the return chart",
                "Be removed by changing the original threshold silently",
                "A balanced report retains contradictory evidence and does not rewrite its original criteria.",
            ),
            (
                "What links an executive claim to inspectable support?",
                "An evidence ledger referencing data, figures and tests",
                "A confident adjective",
                "A longer algorithm name",
                "Traceable artifacts allow another reader to assess the stated claim.",
            ),
        ],
        [CFA, PRESENTATION],
    )
    add(
        "Exporting reproducible results from Python and C",
        "Build a language-independent contract for valuations, provenance, and runtime measurements.",
        "Evaluation should consume explicit outputs rather than scrape an attractive screenshot. Export an initial valuation followed by dated strategy and benchmark valuations on a shared calendar. Declare currency, net/gross basis, external cash flows, sampling frequency, source version and data identity. The algorithm can be written in C, Python or another language; the reporting boundary is the same.\n\nA terminal value is insufficient for path-dependent metrics. The C/HPC sweep prints a final equity and fill count for each window; those rows cannot supply volatility or drawdown without the underlying path. Runtime observations also need separate paired records, with equal workloads and documented build settings. Hashes identify exact files but do not prove that their contents are economically valid or free of leakage.",
        "Thirteen monthly valuations contain twelve return intervals because the first value is the starting capital. Treating all thirteen rows as returns overstates the sample. A repeated date, nonfinite number or unannounced deposit makes a naive ratio-return interpretation invalid.",
        "Read the supplied equity CSV and manifest. Run the project with --no-charts first, inspect SHA-256 values, and compare its input contract with your algorithm's export. For C timings, transcribe repeat, serial_ms and parallel_ms while retaining equal-result evidence separately.",
        r"n_{\mathrm{returns}}=n_{\mathrm{valuations}}-1",
        'valuations = 13\nprint("Return observations:", valuations - 1)\nprint("Return from first interval:", 10200 / 10000 - 1)',
        "Create an export schema and manifest for one saved run. Identify which fields support returns, drawdowns, execution diagnostics, reproducibility and HPC timing; mark unavailable evidence explicitly.",
        "Dated positive aligned valuations support ratio returns and drawdowns under the no-external-flow convention. Trade/event records are needed for execution diagnostics. Source/data hashes, costs, split and parameter history support reproduction. Paired runtime samples and hardware/build metadata support timing claims; final equity alone cannot replace the path.",
        [
            (
                "Thirteen valuations including initial capital provide how many returns?",
                "Twelve",
                "Thirteen",
                "Fourteen",
                "Each return connects two adjacent valuations, so there is one fewer return than rows.",
            ),
            (
                "Can a C sweep's final-equity table alone determine drawdown?",
                "No; drawdown requires the valuation path",
                "Yes, using only the best and worst parameter",
                "Yes, if values are integer cents",
                "Different paths can finish at the same terminal equity with very different drawdowns.",
            ),
            (
                "What does an input SHA-256 establish?",
                "The identity of a particular file's bytes",
                "That the dataset contains no future information",
                "That a strategy will be profitable",
                "A hash supports file identity, not the validity of the data or research design.",
            ),
            (
                "A portfolio rises only because of a deposit. A plain equity ratio measures:",
                "A mixture of flow and investment change unless adjusted",
                "Pure strategy return automatically",
                "Only realized trading profit",
                "External flows violate the simple no-flow ratio-return contract and need adjustment.",
            ),
        ],
        [CFA, PRESENTATION],
    )
    add(
        "Choose and align a meaningful benchmark",
        "Compare against an investable alternative with matching dates, units, and return definitions.",
        "A benchmark should reflect the opportunity set and constraints relevant to the algorithm. A long/cash strategy might use buy-and-hold of the same asset plus a cash reference; a market-neutral strategy needs a different interpretation. Select the benchmark before the result, document its return construction, and distinguish a comparator from a risk-factor model.\n\nAlign strategy and benchmark by valuation timestamp, currency and reinvestment convention. Do not forward-fill unavailable future data or silently shrink the comparison to favorable dates. Missing benchmark observations require an explicit decision about the evaluation sample. Both curves can start at a common index of 100 for presentation, but normalization does not repair a mismatched investment universe or different gross/net assumptions.",
        "The strategy finishes at 11,000 from 10,000 while a benchmark finishes at 10,800 from 10,000. Total returns are 10% and 8%, a two-percentage-point difference. This is not automatically Jensen alpha, and the ratio of final wealth gives a different relative-wealth calculation.",
        "Write a benchmark selection note in the dossier. Check each input row's date and units before plotting. If comparing multiple alternatives, show all justified alternatives and explain why the primary one was chosen rather than selecting the weakest after the fact.",
        r"\Delta R=R_{\mathrm{strategy}}-R_{\mathrm{benchmark}}",
        'strategy = 11000 / 10000 - 1\nbenchmark = 10800 / 10000 - 1\nprint("Cumulative return difference:", strategy - benchmark)\nprint("Relative wealth change:", 11000 / 10800 - 1)',
        "Defend a primary benchmark for your algorithm and document dates, currency, cash treatment, dividends and costs. Calculate both percentage-point return difference and relative wealth change for the worked case.",
        "The worked returns differ by 2 percentage points; relative wealth changes by about 1.852%. Neither is a factor-adjusted alpha estimate. A valid comparator needs a justified opportunity set and aligned accounting/calendar conventions before either number is interpreted.",
        [
            (
                "What is 10% minus 8% in a performance report?",
                "A two-percentage-point cumulative return difference",
                "A proven two-percent Jensen alpha",
                "A twenty-percent wealth gain",
                "Subtraction gives a percentage-point difference, not a factor-adjusted attribution result.",
            ),
            (
                "Normalizing both curves to 100 fixes what?",
                "Their starting display scale",
                "A mismatched opportunity set",
                "Missing future data",
                "Indexing helps visual comparison but does not repair an inappropriate benchmark.",
            ),
            (
                "A 7% strategy and 9% benchmark have a cumulative difference of:",
                "−2 percentage points",
                "+2 percentage points",
                "−22 percentage points",
                "The strategy minus benchmark difference is seven minus nine percentage points.",
            ),
            (
                "When should the primary benchmark be chosen?",
                "Before judging the final result",
                "After finding the easiest comparator to beat",
                "Only after the best chart is selected",
                "Selecting the comparator in advance avoids tailoring the comparison to favorable outcomes.",
            ),
        ],
        [CFA, PRESENTATION],
    )
    add(
        "Reconcile costs, cash flows, and net performance",
        "Make the bridge from gross opportunity to net account change auditable.",
        "A report must state which costs are modeled: commissions, spread, slippage, market impact, borrowing, funding, taxes and infrastructure. Some belong in the economic ledger; others belong in an operating budget. Avoid subtracting the same costs once in the engine and again in the report. A label such as net is incomplete without the included and omitted items.\n\nDistinguish investment gains from external contributions and withdrawals. The downloadable project accepts valuations already net of modelled costs and no external flows. More general accounts need a declared time-weighted or money-weighted methodology with appropriate flow timing. Trade-level realized PnL also need not equal equity change when open positions, dividends, interest, fees or valuation changes remain.",
        "A hypothetical gross gain is 1,200, fees 100 and modeled slippage 200. Net gain is 900 before omitted impact and taxes. If the supplied equity already incorporates that 900, subtracting 300 again understates the same modeled result.",
        "Create a reconciliation table with starting wealth, external flows, realized changes, unrealized changes, income, modeled costs and ending wealth. Identify missing components before computing risk ratios. Use a higher-cost scenario as a separate rerun or labeled sensitivity, not an unexplained edit to history.",
        r"\Pi_{\mathrm{net}}=\Pi_{\mathrm{gross}}-\mathrm{fees}-\mathrm{slippage}-\mathrm{other\ modelled\ costs}",
        'gross = 1200\nfees = 100\nslippage = 200\nnet = gross - fees - slippage\nprint("Net gain:", net)\nprint("Incorrect double-deducted gain:", net - fees - slippage)',
        "Reconcile a sample account's starting and ending wealth, identify which costs are already included, and list omitted costs. Explain what changes if external deposits occur during the evaluation.",
        "A complete bridge reconciles all ledger components and subtracts each modeled cost once. Deposits are not investment gains: use an appropriate flow-adjusted return convention and timestamps. Omitted impact, tax or borrow costs remain visible limitations rather than being hidden inside a net label.",
        [
            (
                "What happens if already-net equity has its fees subtracted again?",
                "Costs are counted twice",
                "The estimate becomes automatically conservative and correct",
                "The benchmark is aligned",
                "Duplicate deduction changes the accounting result rather than improving model realism.",
            ),
            (
                "What must accompany a net-return label?",
                "The modeled and omitted cost definitions",
                "Only the algorithm name",
                "A higher gross-return chart",
                "Readers need to know exactly which economic costs the supplied equity includes.",
            ),
            (
                "Gross gain 800 minus fees 50 and slippage 150 leaves:",
                "600",
                "750",
                "1,000",
                "Each cost is deducted once from gross gain: 800 − 50 − 150.",
            ),
            (
                "Do realized trade profits always equal total equity change?",
                "No; open marks, flows, income and other charges can differ",
                "Yes, regardless of open positions",
                "Only when written in C",
                "The account bridge must include all components, not only closed-trade PnL.",
            ),
        ],
        [CFA, PRESENTATION],
    )
    add(
        "Compounded returns and annualization conventions",
        "Report the observed wealth change before extrapolating an annualized rate.",
        "Returns compound multiplicatively. Arithmetic averages describe a typical periodic observation under a stated sample, while geometric growth describes compounded wealth. The two answer different questions. Report total return and sample length before annualized figures, especially for short or irregular histories.\n\nAnnualization requires a period convention. The project uses declared periods per year and suppresses geometric annualization below one declared year of observations. Square-root volatility scaling has additional dependence assumptions and does not follow merely from date formatting. An intraday dataset cannot inherit 252 periods per year if each row is a minute. Also distinguish return on allocated portfolio capital from return on only the capital deployed in trades; changing denominators can make unrelated results appear comparable.",
        "A 10% gain followed by a 10% loss turns 100 into 99, a −1% total return, although the arithmetic average is zero. The two-period geometric mean is the square root of 0.99 minus one, about −0.501% per period.",
        "Calculate the worksheet by both wealth multiplication and period returns. Inspect observations and annualized_geometric_return in metrics.json. Write the sampling convention next to every annualized metric and leave unsupported extrapolations undefined.",
        r"R_{\mathrm{total}}=\prod_{t=1}^{n}(1+r_t)-1,\qquad g=(1+R_{\mathrm{total}})^{P/n}-1",
        'wealth = 100 * 1.10 * 0.90\nprint("Ending wealth:", wealth)\nprint("Total return:", wealth / 100 - 1)\nprint("Geometric mean:", (1.10 * 0.90) ** 0.5 - 1)',
        "Show why +10% then −10% is not a flat wealth result. Define the correct periods-per-year convention for your export and explain why a short sample should not be presented as a stable annual track record.",
        "The compounded wealth is 99 from 100 despite a zero arithmetic mean. Use the declared valuation frequency and verify regularity/calendar completeness. Short-sample annualization magnifies noise; total return, observation count and uncertainty remain the primary observed facts.",
        [
            (
                "What does +10% followed by −10% do to wealth?",
                "Reduce it by 1%",
                "Leave it exactly unchanged",
                "Increase it by 1%",
                "Multiplication gives 1.1 × 0.9 = 0.99, so wealth falls one percent.",
            ),
            (
                "Which metric directly describes compounded wealth growth?",
                "Geometric return",
                "Arithmetic mean alone",
                "The number of worker threads",
                "Geometric growth reflects multiplication of gross periodic returns.",
            ),
            (
                "Twelve monthly returns with a 6% total change have a declared one-year geometric return of:",
                "6%",
                "72%",
                "0.5% necessarily",
                "With twelve periods and twelve periods per year, the annualization exponent is one.",
            ),
            (
                "Can minute observations use 252 as periods per year without adjustment?",
                "No; the observation frequency must match the convention",
                "Yes, every stock dataset uses it",
                "Only if the algorithm is fast",
                "The scaling factor must correspond to the frequency of the supplied returns.",
            ),
        ],
        [CFA, PRESENTATION],
    )
    add(
        "Risk-adjusted metrics and undefined denominators",
        "Interpret volatility, Sharpe, Sortino, tracking error, and information ratio together.",
        "A ratio compresses several assumptions into one number. Sharpe compares mean periodic excess return to periodic return standard deviation; the risk-free conversion and annualization convention must be stated. Sortino requires a target and a downside-deviation definition. The project uses root mean squared negative excess returns over all periods, which differs from averaging only negative observations.\n\nTracking error measures variability of strategy-minus-benchmark periodic returns; information ratio divides mean active return by that variability under a scaling convention. These are descriptive sample statistics. Serial dependence, fat tails, selection and a small sample can make comparisons unstable. Zero variance or no downside does not establish infinite skill. Preserve undefined denominators as missing with an explanation rather than displaying a favorable infinity or a fabricated zero.",
        "A strategy has mean daily excess return 0.05% and daily standard deviation 1%. Under a 252-period square-root convention its Sharpe is 0.0005/0.01 × sqrt(252), about 0.794. This numerical calculation does not establish that daily returns are independent.",
        "Read evaluate.py's sd, downside and tracking calculations. Compare a constant-cash input with a variable-return input. Verify that undefined ratios are exported as JSON null and described explicitly in the report.",
        r"\widehat{S}=\frac{\bar r-r_f}{s_r}\sqrt{P}",
        'mean_excess = 0.0005\nsd = 0.01\nprint("Sharpe under stated scaling:", mean_excess / sd * 252 ** 0.5)\nnegative_excess = [-0.02, 0, 0, 0]\nprint("RMS downside:", (0.02 ** 2 / 4) ** 0.5)',
        "Reproduce a Sharpe and a downside-deviation calculation, documenting risk-free rate, target, sample denominator and frequency. Explain the report output for a zero-volatility cash series.",
        "The worked Sharpe is about 0.794 and the four-period RMS downside is 1%. A zero denominator leaves its ratio undefined; it is not automatically zero or infinity. Document dependence and small-sample limits alongside the descriptive statistic.",
        [
            (
                "How should a zero-volatility Sharpe denominator be reported?",
                "Undefined with an explanation",
                "As guaranteed infinite skill",
                "As an arbitrary perfect score",
                "A division by zero does not supply a meaningful risk-adjusted performance estimate.",
            ),
            (
                "What must accompany a Sortino value?",
                "Its target and downside-deviation convention",
                "Only total return",
                "A claim that all definitions agree",
                "Different targets and denominator conventions can produce different Sortino values.",
            ),
            (
                "Mean excess 0.001, standard deviation 0.02 and 100 periods/year give a scaled Sharpe of:",
                "0.5",
                "5",
                "0.05",
                "The periodic ratio is 0.05 and multiplying by sqrt(100) gives 0.5.",
            ),
            (
                "What does tracking error describe?",
                "Variability of periodic active returns against the benchmark",
                "Compiler measurement error",
                "The maximum possible future loss",
                "Tracking error concerns the strategy-minus-benchmark return series, not operational latency.",
            ),
        ],
        [CFA, PBO],
    )
    add(
        "Drawdown depth, duration, and recovery",
        "Read the path of losses and time underwater rather than only terminal wealth.",
        "Drawdown compares current wealth with the highest wealth previously observed, including initial capital. The maximum depth is only one aspect of the path. Record when the decline started, when it reached the trough, whether the previous peak was recovered, and how long capital remained underwater. An unrecovered ending drawdown has a censored duration; do not invent a recovery date.\n\nSampling matters. Monthly valuations can hide intramonth losses, while intraday paths need consistent marks and trading-calendar treatment. Report the valuation frequency beside the chart. Percentage loss and required recovery are asymmetric: losing one fifth of capital requires a one-quarter gain on what remains. A drawdown chart supports a risk discussion but does not bound future losses or establish a safe leverage level.",
        "Wealth goes 100 → 80 → 90 → 110. The initial fall is a 20% drawdown and the next observation remains 10% below the peak. Recovery occurs only at 110. From 80, reaching the old 100 peak requires a 25% gain.",
        "Trace the project drawdowns function and verify initial capital is included. Read both the wealth and drawdown panels. Add drawdown dates and duration to your written analysis; the generator supplies the path and maximum depth but does not infer every recovery narrative for you.",
        r"D_t=\frac{E_t}{\max_{s\le t}E_s}-1,\qquad R_{\mathrm{recovery}}=\frac{1}{1-L}-1",
        'peak = 100\ntrough = 80\nprint("Drawdown:", trough / peak - 1)\nprint("Required recovery:", peak / trough - 1)\nprint("Still underwater at 90:", 90 < peak)',
        "Annotate a wealth path with peak, trough, recovery or unrecovered ending, and sampling frequency. Explain how omitting initial capital can hide an immediate loss.",
        "The starting valuation is a valid high-water mark. In the example, 80 is 20% below 100 and needs a 25% gain to recover; 90 remains underwater. If the last observation never regains the prior peak, report the duration as still ongoing at the sample end.",
        [
            (
                "Should initial capital participate in the drawdown peak?",
                "Yes",
                "No, only profitable observations count",
                "Only after the first winning trade",
                "Ignoring initial capital can conceal a loss immediately after the test begins.",
            ),
            (
                "A 20% loss requires what gain to recover?",
                "25%",
                "20%",
                "16%",
                "Eighty must rise by twenty to reach one hundred, a gain of twenty divided by eighty.",
            ),
            (
                "Wealth falls from a peak of 200 to 150. Drawdown magnitude is:",
                "25%",
                "33.33%",
                "50%",
                "The loss of fifty is measured relative to the previous peak of two hundred.",
            ),
            (
                "A drawdown remains unrecovered at the last valuation. Its recovery date is:",
                "Unknown beyond the observed sample",
                "The sample's final date automatically",
                "The date of the trough",
                "No observed recovery exists, so the report must preserve that incomplete duration.",
            ),
        ],
        [CFA, PRESENTATION],
    )
    add(
        "Execution quality, turnover, and cost sensitivity",
        "Explain how implementation choices change realized results and required trading capacity.",
        "Strategy-level equity is necessary but insufficient to diagnose execution. Collect order intents, acknowledgments, fills, cancellations, timestamps and decision prices under a stable identity scheme. Separate signal quality from fill quality, and treat a missing or duplicated fill as an accounting problem before interpreting performance.\n\nUseful diagnostics include fill ratio, rejected order reasons, decision-to-fill delay, slippage relative to a stated reference, turnover, participation and concentration. Each metric needs a denominator and population. A fast-filled subset can hide slow or unfilled orders if the report conditions only on successes. Costs often increase with size and market conditions; a fixed-fee backtest cannot establish capacity. The reporting project accepts valuations and timings, so trade diagnostics require separately supplied event evidence in the dossier.",
        "An order requests 100 shares and fills 60. Fill ratio is 60%, not 100% because the accepted portion completed. A buy decision price of 100 and fill price of 100.20 implies 20 basis points of adverse price slippage before fees under that reference convention.",
        "Build an execution appendix with all submitted intents, including rejected and unfilled ones. Rerun a small set of higher-cost and delayed-fill scenarios under unchanged signals. Distinguish an implemented rerun from a hand-calculated sensitivity assumption.",
        r"\mathrm{fill\ ratio}=q_{\mathrm{filled}}/q_{\mathrm{requested}},\qquad \mathrm{buy\ slippage}_{bps}=10^4(P_{\mathrm{fill}}/P_{\mathrm{decision}}-1)",
        'print("Fill ratio:", 60 / 100)\nprint("Buy slippage bps:", (100.20 / 100 - 1) * 10000)\nprint("Extra cost on 500000 notional at 10 bps:", 500000 * 10 / 10000)',
        "Create an execution table including unfilled/rejected orders, denominator definitions, slippage reference, turnover and a higher-cost scenario. Explain what evidence is missing from an equity-only report.",
        "Equity alone does not reveal which intents were delayed, rejected or duplicated. Retain the full intent population and event timestamps, calculate fill ratio against requested quantity, and disclose the slippage reference. A cost rerun needs changed ledger/execution assumptions; a simple sensitivity is labeled as such.",
        [
            (
                "Sixty shares filled out of one hundred requested gives:",
                "60% fill ratio",
                "100% fill ratio",
                "40% fill ratio",
                "The denominator is the originally requested quantity under the stated definition.",
            ),
            (
                "Why retain unfilled orders in execution evaluation?",
                "To avoid conditioning the report only on successful fills",
                "To increase reported profit automatically",
                "To replace the equity path",
                "Excluding failures hides part of the algorithm's actual execution behavior.",
            ),
            (
                "An extra 5 bps on 200,000 notional costs:",
                "100",
                "1,000",
                "10",
                "Five basis points is 0.0005; multiplying by 200,000 gives one hundred.",
            ),
            (
                "Can a fixed five-cent fee model establish market capacity?",
                "No; impact, liquidity and scale behavior need additional evidence",
                "Yes, for every stock",
                "Only if compiled with optimization",
                "Capacity depends on how execution costs and fill behavior change with trading size.",
            ),
        ],
        [CFA, PRESENTATION],
    )

    add(
        "Chronological holdouts and walk-forward evaluation",
        "Separate model fitting, selection, and final evaluation without leaking information across time.",
        "A final evaluation must reflect the information available when decisions would have been made. Fit preprocessing and parameters on training data, use validation for model selection, and reserve a test period for a limited predeclared final assessment. Once a test result influences choices, it becomes part of development and cannot be described as untouched.\n\nFinancial labels may span multiple dates. A simple date boundary can still leak if a training label uses outcomes inside the next fold. Purge overlapping label intervals and use an embargo where the research design requires it. Walk-forward evaluation simulates repeated refits through time, but folds are not necessarily independent. Preserve the selection and refit rule, report each fold and compare against baselines at the same information boundary.",
        "Training ends on June 30 but its final label measures the following five trading days. A July 1 validation start overlaps that training outcome. Removing overlapping training labels respects the boundary; shuffling rows does not solve it.",
        "Draw the train, validation and test timeline with feature availability and label end dates. Link to your stock-ML or econometrics project for actual purged evaluation. Enter the number of tried configurations and test-set reuse honestly in the reporting manifest.",
        r"\mathrm{training\ label\ end}<\mathrm{next\ evaluation\ start}",
        'training_label_ends = [28, 29, 30, 32, 35]\nvalidation_start = 31\nprint("Eligible labels:", [28 < validation_start, 29 < validation_start, 30 < validation_start, 32 < validation_start, 35 < validation_start])\nprint("Purged labels:", 2)',
        "Draw a chronological evaluation with overlapping five-day labels. Specify the purge rule, fit/selection/refit sequence, baselines, and what happens if you change the algorithm after seeing test results.",
        "Training labels ending inside the next evaluation window must be excluded under the chosen boundary. Fit transforms only on eligible training data and select on validation. Any change driven by final test results consumes that holdout and must be disclosed with a revised evaluation plan.",
        [
            (
                "What is the final test period for under a predeclared protocol?",
                "A limited independent final assessment",
                "Unlimited hyperparameter selection",
                "Fitting the scaler on every row",
                "The holdout is reserved from model development to reduce selection contamination.",
            ),
            (
                "Why can a chronological split still leak?",
                "Training labels can extend into future evaluation dates",
                "Time ordering always randomizes outcomes",
                "All time series are independent",
                "Outcome intervals can overlap across a nominal row-date boundary.",
            ),
            (
                "A training label ends at day 35 and validation starts at day 31. Under a strict nonoverlap rule it is:",
                "Ineligible for that training fold",
                "Safe because its feature date is earlier",
                "Automatically moved to the test metric",
                "The label uses outcomes from inside the validation period and violates the boundary.",
            ),
            (
                "A researcher modifies the strategy after reviewing test losses. The same test set is now:",
                "Part of the development process",
                "Still untouched out-of-sample evidence",
                "Guaranteed more conservative",
                "Feedback from the test influences selection and must be disclosed as such.",
            ),
        ],
        [LEAKAGE, SPLITS],
    )
    add(
        "Selection bias and uncertainty around a chosen algorithm",
        "Disclose the search process and distinguish sampling uncertainty from backtest overfitting.",
        "Trying more variants increases the chance that an apparently strong winner reflects noise. Record all material choices: parameters, features, universes, holding periods, filters, costs and revisions after inspecting results. The number of configurations in a final grid can understate the larger research history. A high selected Sharpe should trigger a selection audit, not just a more polished chart.\n\nResampling estimates uncertainty under assumptions about the observed data-generating process. The project uses a circular block bootstrap of mean periodic active return, preserving short within-block sequences. Block length, stationarity and sample size matter. It does not correct a strategy chosen on the same observations, establish a precise overfitting probability, or model unseen regimes. Keep sampling uncertainty, selection bias and economic model uncertainty distinct.",
        "With 20 independent null tests each having a 5% false-positive probability, the chance of at least one false positive is 1 − 0.95^20, about 64.2%. Real strategy tests are often correlated, so this illustration is not a direct estimate for an arbitrary parameter search.",
        "Inspect block_interval and its fixed seed/block/repetition settings. Compare an identical strategy/benchmark path with a variable active-return path. Report the interval beside the search history and sample size, with a clear statement of what the resampling does not address.",
        r"P(\text{at least one false positive})=1-(1-\alpha)^m\quad\text{under independence}",
        'print("Illustrative family false-positive probability:", 1 - 0.95 ** 20)\nprint("Block bootstrap settings:", [3, 1000, 42])',
        "Disclose the complete selection history and interpret a bootstrap interval without calling it an overfitting correction. Recalculate the independent-test illustration for ten tests and explain its dependence assumption.",
        "Ten independent 5% tests give 1 − 0.95^10 ≈ 40.1%. Strategy variants are often dependent, so the example is illustrative. A block interval describes resampling uncertainty under its assumptions; it does not undo using the evaluation period to select the winner.",
        [
            (
                "What should a search-history disclosure include?",
                "Material variants and revisions, including failed ones",
                "Only the final winning parameter",
                "Only experiments with positive return",
                "The extent of research selection affects how surprising a selected result should appear.",
            ),
            (
                "Does the project's block bootstrap correct a winner selected on the same sample?",
                "No",
                "Yes, automatically",
                "Only because the seed is fixed",
                "Resampling the selected series does not remove the selection procedure's bias.",
            ),
            (
                "For two independent 5% false-positive tests, at least one false positive has probability:",
                "9.75%",
                "5%",
                "0.25%",
                "One minus 0.95 squared equals 0.0975 under the stated independence assumption.",
            ),
            (
                "Why report block length and sample size?",
                "They affect the resampling dependence model and uncertainty",
                "They prove future stationarity",
                "They replace the benchmark",
                "Bootstrap conclusions depend on the resampling construction and available observations.",
            ),
        ],
        [PBO, BOOTSTRAP],
    )
    add(
        "Robustness: parameter neighborhoods, regimes, and stress",
        "Challenge the mechanism with predeclared perturbations and preserve unsuccessful results.",
        "Robustness asks whether a conclusion survives reasonable changes to assumptions and conditions. Examine neighboring parameters, different chronological regimes, delayed execution, higher costs, data gaps and relevant market shocks. Choose perturbations because they challenge the proposed mechanism, not because they produce attractive plots. A broad stable region can be more credible than one isolated best setting, but it is not proof of future profitability.\n\nKeep separate base, sensitivity and stress cases. A sensitivity changes one assumption to explain direction; a scenario combines related changes into a coherent environment; a stress probes an adverse condition. Some scenarios require a rerun of the algorithm because positions and compounding change. Linear subtraction from final profit may be only a rough labeled approximation. The reporting tool summarizes supplied paths; it does not automatically execute every robustness experiment.",
        "Neighboring windows 19, 20 and 21 show net returns 2%, 18% and 1%. That sharp peak deserves investigation of data selection, event timing and parameter sensitivity. It does not justify reporting only window 20 as representative performance.",
        "Prepare a robustness matrix with scenario, mechanism, changed input, expected direction, actual result and interpretation. Link every executed case to its output hash. Preserve scenarios that invalidate the initial hypothesis and define a review trigger for new data.",
        r"\mathrm{sensitivity}\approx\frac{f(\theta+\Delta)-f(\theta-\Delta)}{2\Delta}",
        'results = [0.02, 0.18, 0.01]\nprint("Neighbor spread:", max(results) - min(results))\nprint("Lowest neighbor return:", min(results))\nprint("Net gain under extra 500 cost:", 900 - 500)',
        "Create a six-case robustness matrix including parameter neighbors, cost increase, delayed execution, a data fault and an adverse regime. Mark which cases need a full rerun and which are only approximate sensitivities.",
        "Execution delay, missing observations and parameter changes can alter positions and require reruns. A fixed added cost may be a labeled first-order sensitivity but does not model nonlinear impact or changed fills. Report the entire matrix, including failures and untested proposals.",
        [
            (
                "An isolated high-return parameter surrounded by weak neighbors suggests:",
                "A sensitivity that needs investigation",
                "Guaranteed optimal economic design",
                "Permission to omit the neighbors",
                "A narrow peak can reflect instability or selection and should be challenged with evidence.",
            ),
            (
                "What distinguishes a reported executed stress from a proposed stress?",
                "A reproducible run and its actual output artifacts",
                "A confident scenario title",
                "The number of colors in its chart",
                "Claims about tested behavior require recorded execution evidence.",
            ),
            (
                "A base net gain of 900 with an additional assumed 500 cost gives a first-order sensitivity of:",
                "400",
                "1,400",
                "900",
                "Subtract the additional assumed cost once, while labeling the approximation's limits.",
            ),
            (
                "Why can delayed execution require a full rerun?",
                "It can change fills, positions and later account state",
                "It changes only the report title",
                "The final cash always shifts linearly",
                "Execution timing affects the path-dependent trading process, not only a terminal adjustment.",
            ),
        ],
        [PBO, LEAKAGE],
    )
    add(
        "Evaluate computing performance alongside trading results",
        "Report C/HPC speed, correctness parity, and operational latency as separate evidence.",
        "A complete algorithm report distinguishes financial behavior from computing behavior. Document workload size, input identity, parameter count, worker count, compiler/version, flags, hardware, operating system, timing boundaries and output equality. A faster candidate with changed fills is not an equivalent implementation speedup until the discrepancy is explained.\n\nUse repeated paired runs and show both elapsed times and speedup. The median of paired speedup ratios can differ from the ratio of elapsed-time medians; label the statistic you actually calculate. Tiny workloads may be dominated by thread setup. A batch research benchmark does not measure gateway tail latency. For operations, define the event population and include queueing, stale data, risk checks, network uncertainty and failure recovery.",
        "Five paired serial/parallel timings are (30,10), (31,11), (29,9), (32,12), (30,10) milliseconds. Median serial time is 30, median parallel is 10, and the median paired speedup is 3×. These are illustrative fixture values, not a measurement of your own machine.",
        "Transfer the C/HPC lab's actual paired timing rows into the reporting timing CSV and retain all equal=yes evidence. Run the evaluator with --timings, inspect the summary and write a separate interpretation of workload scaling and observed variability.",
        r"S_i=T_{\mathrm{serial},i}/T_{\mathrm{parallel},i},\qquad \widetilde{S}=\mathrm{median}(S_i)",
        'print("Paired speedups:", [30 / 10, 31 / 11, 29 / 9, 32 / 12, 30 / 10])\nprint("Fixture median paired speedup:", 3.0)\nprint("Unchanged result required:", 999950 == 999950)',
        "Attach an actual paired C/HPC timing table with equal-result evidence, workload, CPU/OS/compiler/flags and full repetitions. Explain why it cannot certify real order-response p99 latency.",
        "The report can describe the measured batch's elapsed time and paired-speedup statistic. Gateway p99 needs a different event population and sufficient measurements including queues/network. Preserve correctness parity, timing boundaries and all repetitions; distinguish illustrative sample timings from your actual measurements.",
        [
            (
                "Which evidence must accompany an equivalent-implementation speedup?",
                "Matching outputs under the same contract and workload",
                "Only the fastest elapsed time",
                "A more profitable changed strategy",
                "Behavioral equality is required to interpret a timing difference as implementation speed.",
            ),
            (
                "The median of paired ratios is:",
                "A statistic that need not equal the ratio of medians",
                "Always identical to the ratio of medians",
                "A trading Sharpe ratio",
                "Nonlinear aggregation means these summaries can differ and should be labeled precisely.",
            ),
            (
                "A paired run takes 24 ms serial and 8 ms parallel. Its speedup is:",
                "3×",
                "16×",
                "0.333×",
                "The paired speedup divides baseline elapsed time by candidate elapsed time.",
            ),
            (
                "Can five research-batch timings certify exchange p99 latency?",
                "No; both the measured path and sample are inadequate",
                "Yes, if the median is low",
                "Yes, with integer cash accounting",
                "Tail latency requires an appropriate operational event population and enough observations.",
            ),
        ],
        [CLOCK, CFA],
    )
    add(
        "Build clear result tables and honest charts",
        "Turn calculations into readable, traceable visuals without concealing unfavorable periods.",
        "A figure should answer a specific question. Use a common date axis and normalized starting wealth for strategy/benchmark comparison, a separate drawdown panel for losses, and tables with units, sample length, cost basis and undefined-value explanations. Keep the complete evaluation period visible; a selectively cropped winning segment is a different sample and must be identified as such.\n\nAvoid visual choices that imply more precision than the evidence supports. A dense legend, misleading axis, unmarked log scale or unexplained annualization makes scrutiny harder. Include a caption describing the data and interpretation. For export, use standard plotting software and save standalone files with readable fonts. The project creates PNG and SVG figures plus printable HTML and Markdown that reference those artifacts.",
        "Two portfolios both start at index 100. One reaches 110 after a deep drawdown, while the other reaches 108 smoothly. A final-value bar chart misses the path distinction; aligned wealth and drawdown panels show both terminal return and the route taken.",
        "Install the project requirements and generate the sample report with charts. Open report.html, compare its table with metrics.json, and inspect the exported PNG/SVG. Retain the report folder so relative image links work when shared.",
        r"W_t^{\mathrm{index}}=100\frac{E_t}{E_0}",
        'initial = 10000\nprint("Indexed wealth:", [100 * 10000 / initial, 100 * 9800 / initial, 100 * 11000 / initial])\nprint("Benchmark ending index:", 100 * 10800 / 10000)',
        "Create a wealth/drawdown figure and a metric table with units, dates, frequency and cost basis. Verify every displayed number against the machine-readable output and keep all loss periods in the main view.",
        "Both wealth curves begin at 100 on shared dates; the drawdown panel includes initial capital and full loss periods. Tables identify percent versus percentage-point difference and undefined ratios. Captions state sampling/cost conventions, and PNG/SVG files travel with the HTML/Markdown report.",
        [
            (
                "What does a shared wealth index of 100 help compare?",
                "Relative growth paths from a common display origin",
                "Different currencies without conversion",
                "Unrelated valuation dates",
                "Normalization aids display but still requires aligned and meaningful input conventions.",
            ),
            (
                "Why include a drawdown panel beside wealth?",
                "It exposes the depth and path of losses",
                "It proves maximum future loss",
                "It replaces the benchmark",
                "A separate loss view reveals path risk that terminal wealth can conceal.",
            ),
            (
                "Starting equity 5,000 and current equity 5,500 give a wealth index of:",
                "110",
                "10",
                "550",
                "Normalize as 100 × 5,500 / 5,000 to get an index level of 110.",
            ),
            (
                "A figure cropped to omit a bad year should be:",
                "Clearly labeled as a subset, with the full period also reported",
                "Presented as the full track record",
                "Used to replace every full-period metric",
                "Sample selection changes the claim and cannot be concealed by presentation.",
            ),
        ],
        [PLOTS, PRESENTATION],
    )
    add(
        "Attribution and diagnosing where results came from",
        "Explain performance by exposures, periods, decisions and costs without overstating causality.",
        "After measuring the outcome, ask what generated it. Break results down by time period, instrument, sector, direction, signal family, market exposure and execution cost when the underlying data supports that partition. An attribution table should reconcile to a declared total under its accounting method. Simply adding compounded period returns does not generally reconcile to the multi-period wealth change.\n\nDistinguish explanation from causal proof. A positive correlation with a factor can describe exposure; a regression intercept is conditional on the chosen model and sample. Strategy-minus-benchmark return is not automatically alpha. Concentration in a single instrument or regime can weaken the claim that a broad mechanism is working. The report generator does not fit factor models; bring those estimates and diagnostics from the quantitative/econometric projects and cite the exact specification.",
        "A total net gain of 900 is decomposed into 700 from one asset, 300 from another and −100 from a hedge under a consistent PnL ledger. The sum reconciles, but 700/900 ≈ 77.8% comes from one asset, which is important context for robustness.",
        "Create a reconciled PnL contribution table using consistent units and an explicit treatment of costs. Add relevant exposure or regression evidence only if available. Identify the concentration, alternative explanations and missing diagnostics in the written interpretation.",
        r"\Pi_{\mathrm{total}}=\sum_j\Pi_j\quad\text{under consistent PnL accounting}",
        'contributions = [700, 300, -100]\nprint("Reconciled net gain:", sum(contributions))\nprint("Largest contribution share:", 700 / sum(contributions))\nprint("Two-period compounded return:", 1.05 * 1.04 - 1)',
        "Produce a reconciled contribution table and one exposure diagnostic. Explain why summed period returns or an unqualified benchmark difference should not be presented as a complete causal attribution.",
        "Consistent PnL contributions reconcile to 900, with 77.8% from one asset in the example. Compounded returns need an appropriate linking method, not naive addition. Exposure models depend on specification, and benchmark difference alone is not factor-adjusted alpha or causal proof.",
        [
            (
                "What should an attribution table reconcile to?",
                "Its declared total under a consistent accounting method",
                "Only the best-performing asset",
                "The largest raw return",
                "Attribution is interpretable when components connect to a stated total without missing costs.",
            ),
            (
                "Does a positive factor correlation establish a causal mechanism?",
                "No; it describes association under the analysis",
                "Yes, always",
                "Only when shown in green",
                "Association and conditional model fit do not alone prove causality.",
            ),
            (
                "Contributions 500, 200 and −100 sum to:",
                "600",
                "800",
                "400",
                "The net total retains the negative contribution: 500 + 200 − 100.",
            ),
            (
                "Why disclose that one asset supplies most of the gain?",
                "It reveals concentration and a robustness question",
                "It invalidates every strategy automatically",
                "It permits removal of losing assets",
                "Concentration helps readers assess whether the claimed broad mechanism is supported.",
            ),
        ],
        [CFA, PBO],
    )
    add(
        "Write a balanced executive conclusion",
        "Turn evidence into a clear decision, limitations, and the next falsification test.",
        "The executive page should make the reader's decision easier. State the question and evaluated version, summarize the strongest supporting and contrary evidence, explain uncertainty and scope, and choose reject, revise or a bounded next paper study. Link each factual assertion to its supporting artifact. A report can be complete even when the algorithm is rejected.\n\nUse precise language: the observed sample showed a result under specified costs and timing; it does not guarantee future returns. Distinguish measured behavior from an untested explanation or proposed next step. Explain benchmark weaknesses, selection history, small samples and omitted execution costs near the conclusion rather than burying them in an appendix. The generator deliberately leaves a REVIEW REQUIRED section so a descriptive metric table is not mistaken for an automatic investment decision.",
        "A report finds 10% sample return versus 8% benchmark, a 6.67% drawdown, only twelve synthetic monthly observations and sixty-four tried configurations. A defensible conclusion treats this as a successful reporting fixture, not independent evidence that the algorithm should trade real capital.",
        "Complete the one-page conclusion in report-notebook.md. Make a claim/evidence/limitation table, then ask another reader to locate each cited artifact. Define a concrete next test that could disprove the mechanism instead of promising to find better parameters.",
        r"\mathrm{claim}\longleftrightarrow\mathrm{evidence}\longleftrightarrow\mathrm{limitation}",
        'print("Observed strategy return:", 0.10)\nprint("Observed benchmark return:", 0.08)\nprint("Sample months:", 12)\nprint("Configurations disclosed:", 64)\nprint("Decision:", "Reporting fixture only; independent evaluation required")',
        "Write a one-page executive conclusion with the evaluated version, strongest supporting result, strongest contrary result, uncertainty, decision and one falsifiable next test. Cite the exact tables and figures.",
        "A strong conclusion is traceable and balanced. The supplied synthetic sample cannot justify a real-capital decision; it demonstrates the reporting workflow. For actual research, state the holdout and search history, omitted costs and operational limits, then define a bounded independent follow-up.",
        [
            (
                "Can a complete report conclude that an algorithm should be rejected?",
                "Yes; a supported negative decision is a valid result",
                "No; every report must recommend deployment",
                "Only if there are no charts",
                "Reporting quality depends on evidence and reasoning, not on reaching a favorable decision.",
            ),
            (
                "Where should a material limitation appear?",
                "Near the conclusion and relevant result",
                "Only in an obscure appendix",
                "Nowhere if return is positive",
                "Readers need material limits when assessing the central decision, not after it is implied.",
            ),
            (
                "A twelve-month synthetic fixture with many tried configurations supports:",
                "A demonstration of reporting mechanics under stated assumptions",
                "An independent real-market deployment claim",
                "A guarantee of persistent alpha",
                "Synthetic and selected examples do not establish independent investment performance.",
            ),
            (
                "What makes a useful next research step?",
                "A specific test capable of falsifying the mechanism",
                "Only trying more parameters until returns improve",
                "Deleting contrary observations",
                "A falsifiable follow-up tests the hypothesis rather than optimizing the narrative.",
            ),
        ],
        [PRESENTATION, PBO],
    )
    add(
        "Capstone: deliver the complete algorithm evaluation report",
        "Assemble reproducible inputs, calculations, figures, diagnostics and a defensible written judgment.",
        "The final course deliverable is a report bundle that another researcher can inspect and rerun. Include the evaluated algorithm/source identity, input data and manifest, calculation code, JSON metrics, full-period wealth/drawdown charts, readable report, notebook interpretation and references. Add execution diagnostics, robustness outputs and computing measurements when those claims are part of your conclusion.\n\nFirst validate the supplied fixture, then replace it with your documented algorithm outputs. Do not silently invent a path from a C sweep's terminal values or relabel illustrative timing rows as measurements. The reporting project accepts aligned no-flow net valuations; other account conventions need an explicit adapter. Audit all claims against available evidence and leave unimplemented analyses labeled as proposals. The concept final and the report rubric assess different work.",
        "The supplied twelve-month fixture must produce 10% net strategy return, 8% benchmark return, a two-percentage-point difference, and a maximum drawdown of 1 − 9,800/10,500 = 6.6667%. Its timing fixture has a median paired speedup of 3×. All values are fictional and serve as independent report checks.",
        "Run the project tests, then generate HTML, Markdown, JSON, PNG and SVG output. Review the report in a browser and reconcile its table to the JSON. Complete the 100-point rubric and executive conclusion, retain the archive's source hashes, then submit the final concept exam.",
        r"\mathrm{report}=\mathrm{reproducible\ inputs}+\mathrm{validated\ results}+\mathrm{balanced\ interpretation}",
        'print("Strategy total return:", 11000 / 10000 - 1)\nprint("Benchmark total return:", 10800 / 10000 - 1)\nprint("Maximum drawdown:", 1 - 9800 / 10500)\nprint("Report rubric total:", 20 + 25 + 25 + 20 + 10)',
        "Deliver the full report bundle with input/source identity, validated metrics, wealth/drawdown figures, selection/holdout disclosure, robustness and execution evidence, HPC timing where relevant, a balanced executive conclusion and primary references.",
        "Reproduce the fixture's 10%/8% returns, two-percentage-point difference, 6.6667% drawdown and 3× illustrative timing median. Then distinguish your measured data from fixtures and proposals. Target 80/100 on the separate rubric; unresolved look-ahead, hidden flows, missing losses, mismatched benchmarks or fabricated results require revision regardless of score.",
        [
            (
                "What belongs in the final reproducible report bundle?",
                "Inputs, manifest, code, metrics, figures, interpretation and references",
                "Only a screenshot of the final return",
                "Only the selected algorithm name",
                "An inspectable bundle links the result to its data, calculations and reasoning.",
            ),
            (
                "The sample falls from 10,500 to 9,800. Maximum drawdown magnitude is:",
                "About 6.6667%",
                "7% exactly",
                "About 7.1429%",
                "The 700 loss is divided by its 10,500 high-water mark.",
            ),
            (
                "A concept exam passes but the report omits a losing year. The report is:",
                "Incomplete and requires revision",
                "Accepted because the score replaces evidence",
                "Automatically conservative",
                "Conceptual knowledge cannot excuse a misleading evaluation sample or missing evidence.",
            ),
            (
                "Can the lab's illustrative 3× timing median be labeled as a measurement of your C algorithm?",
                "No; supply actual paired measurements and build metadata",
                "Yes, if the source language matches",
                "Yes, without running anything",
                "Fixture values teach the reporting calculation and are not measurements of another workload.",
            ),
        ],
        [CFA, PRESENTATION, PBO, PLOTS],
    )

    parts = [
        (
            "Define and audit the evaluation",
            "Contracts, reproducible exports, benchmark alignment and cost reconciliation.",
        ),
        (
            "Measure return, risk and execution",
            "Compounding, risk ratios, drawdowns, fill quality and cost sensitivity.",
        ),
        (
            "Challenge the result",
            "Holdouts, selection bias, block uncertainty, stress cases and C/HPC measurement.",
        ),
        (
            "Create and defend the report",
            "Tables/figures, attribution, executive interpretation and the final dossier.",
        ),
    ]
    track = finish(
        {
            "id": "algorithm-evaluation",
            "number": 10,
            "title": "Algorithm evaluation & results reporting",
            "description": "The final synthesis course: evaluate a trading algorithm, challenge its results, and create a reproducible report with benchmarks, costs, risk, uncertainty, execution diagnostics, charts, and a clear written decision.",
            "source": "Original Quanta course · CFA Institute, Bailey et al., scikit-learn, arch, Matplotlib & systems references",
            "level": "Advanced",
            "icon": "report",
            "studyType": "applied",
            "modules": modules,
            "prerequisites": "Complete a trading algorithm project in the Python bot, C/HPC, or stock-ML course. Use quantitative analysis and econometrics for statistical context. Basic Python is helpful for the reporting script; algorithms evaluated through its export contract can be written in any language.",
            "outcomes": [
                "Define a reproducible evaluation contract and audit data, costs, timing and benchmark alignment.",
                "Calculate and interpret compounded return, risk ratios, drawdowns and execution diagnostics.",
                "Disclose selection, preserve chronological holdouts and challenge performance with uncertainty and stress evidence.",
                "Evaluate C/HPC speed and correctness separately from investment and operational claims.",
                "Produce JSON, Markdown, printable HTML and PNG/SVG figures from supplied valuations.",
                "Defend a balanced report conclusion with explicit limitations, references and a falsifiable next test.",
            ],
            "readingGuide": "The final learning track has 16 lessons × 30 minutes = 8 hours of planned study across four units: 10 minutes reading, 8 minutes calculations and 12 minutes report work per lesson; exam time is additional. Includes 32 practice questions, four four-question checkpoints, a 16-question final, a real downloadable reporting project and a separately self-assessed capstone dossier. Generated metrics and figures require analyst interpretation; sample prices and timings are fictional. The reporting program does not automatically certify strategies, execute all robustness proposals, or claim regulatory/GIPS compliance.",
            "parts": [
                {"id": str(i), "title": t, "description": d} for i, (t, d) in enumerate(parts, 1)
            ],
            "references": [
                {"title": t, "url": u}
                for t, u in [CFA, PRESENTATION, PBO, LEAKAGE, BOOTSTRAP, PLOTS]
            ],
            "resources": [
                {
                    "title": "Download the complete algorithm reporting lab",
                    "url": "/course-assets/algorithm-evaluation/algorithm-report-lab.zip",
                },
                {
                    "title": "Download the report notebook and capstone rubric",
                    "url": "/course-assets/algorithm-evaluation/report-notebook.md",
                },
                {
                    "title": "Download the report project guide",
                    "url": "/course-assets/algorithm-evaluation/README.md",
                },
            ],
        },
        checkpoints_for(modules, parts, 4),
    )
    track["exams"][-1]["version"] = 1
    return track
