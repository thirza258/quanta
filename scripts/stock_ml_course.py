"""A twelve-hour original stock machine-learning lifecycle course."""

from applied_courses import checkpoints_for, study
from book_courses import finish

PIT = (
    "scikit-learn contributors · Common pitfalls and data leakage",
    "https://scikit-learn.org/stable/common_pitfalls.html",
)
PIPE = (
    "scikit-learn contributors · Pipelines and composite estimators",
    "https://scikit-learn.org/stable/modules/compose.html",
)
MISSING = (
    "pandas contributors · Missing-data semantics",
    "https://pandas.pydata.org/docs/user_guide/missing_data.html",
)
ASOF = (
    "pandas contributors · Dated as-of joins",
    "https://pandas.pydata.org/docs/reference/api/pandas.merge_asof.html",
)
SPLIT = (
    "scikit-learn contributors · Chronological cross-validation",
    "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html",
)
METRIC = (
    "scikit-learn contributors · Model evaluation metrics",
    "https://scikit-learn.org/stable/modules/model_evaluation.html",
)
CAL = (
    "scikit-learn contributors · Probability calibration",
    "https://scikit-learn.org/stable/modules/calibration.html",
)
TREE = (
    "scikit-learn contributors · Tree ensemble models",
    "https://scikit-learn.org/stable/modules/ensemble.html",
)
NN = (
    "scikit-learn contributors · Supervised neural networks",
    "https://scikit-learn.org/stable/modules/neural_networks_supervised.html",
)
TUNE = (
    "scikit-learn contributors · Hyperparameter search",
    "https://scikit-learn.org/stable/modules/grid_search.html",
)
IMPORTANCE = (
    "scikit-learn contributors · Permutation importance",
    "https://scikit-learn.org/stable/modules/permutation_importance.html",
)
SAVE = (
    "scikit-learn contributors · Model persistence and compatibility",
    "https://scikit-learn.org/stable/model_persistence.html",
)


def build_stock_ml():
    modules = []

    def add(*args):
        item = study(*args)
        item["minutes"] = 30
        item["reading"] = (
            "30-minute session: 8 minutes of lesson and primary-source study, 8 minutes reproducing the worksheet, and 14 minutes on the project assignment and review. Allow extra time if Python or statistics is new to you."
        )
        item["content"] += (
            "\n\n## Put this session into practice\n\nUse the first eight minutes to read the explanation and the linked primary material, then spend eight minutes reproducing and changing the worksheet calculation. Use the remaining fourteen minutes to complete the assignment in your lifecycle notebook or downloaded project. Record the expected result before running code, compare it with the output, and keep an unresolved question for the next review. The 12-hour estimate includes these activities; checkpoint and final-exam time is additional."
        )
        modules.append(item)

    add(
        "7.1",
        1,
        "Define the stock-ML task and lifecycle",
        "Translate a trading idea into a prediction contract with data, labels, baselines, evaluation, and release criteria.",
        "Machine learning estimates a relationship from examples; a trading system additionally needs a decision rule, execution assumptions, and operational controls. Start with the prediction question, horizon, eligible universe, available information, loss function, and baseline. Distinguish forecasting a return, classifying its sign, ranking stocks, and deciding whether an opportunity is worth its costs.\n\nThe lifecycle links problem definition to collection, cleaning, features, labels, splitting, training, selection, independent evaluation, error diagnosis, artifact release, inference, monitoring, and retirement. A failure in an early stage can invalidate a sophisticated model later.",
        "The downloadable project observes features after close t, predicts the return from open t+1 to open t+2, and separately classifies whether that return is positive. With entry 100 and exit 102, its regression target is .02 and its direction label is positive. A positive label alone does not establish profit after execution costs.",
        "Create a one-page contract before running the lab. Define what a prediction means and what evidence would reject the idea. Preserve a simple mean-return and class-prior baseline. The default project uses synthetic data and produces research artifacts, not orders. Its negative or inconclusive results are legitimate outcomes of the lifecycle, not reasons to change the test retrospectively.",
        r"y_t=O_{t+2}/O_{t+1}-1",
        'print("Next-open holding return:", 102 / 100 - 1)\nprint("Net after stated .3% cost:", 102 / 100 - 1 - 0.003)',
        "Write the project prediction contract, including information cutoff, target interval, two baselines, primary metrics, and a rejection condition.",
        "A complete contract separates the predicted next-open interval from feature observation, defines regression and sign tasks, includes mean/prior baselines, and states what would make the evidence insufficient for further paper research.",
        [
            (
                "A predictive model alone specifies a complete trading operation:",
                ["No", "Yes", "Only if it uses deep learning"],
                0,
                "Execution, costs, authority, and operational rules require additional specifications.",
            ),
            (
                "The target interval should be defined:",
                [
                    "After inspecting the best result",
                    "Before training and evaluation",
                    "Only after deployment",
                ],
                1,
                "The task must remain stable while its evidence is evaluated.",
            ),
            (
                "Entry 50 and exit 51 imply target return:",
                ["1%", "51%", "2%"],
                2,
                "51/50−1=.02 under the declared return convention.",
            ),
            (
                "An inconclusive independent result should be:",
                [
                    "Retained and interpreted within the research contract",
                    "Deleted",
                    "Converted into a guaranteed-profit claim",
                ],
                0,
                "A lifecycle records failed hypotheses as well as useful findings.",
            ),
        ],
        [PIT, METRIC],
    )

    add(
        "7.2",
        1,
        "Source provenance and point-in-time stock data",
        "Record when each observation became available and avoid using revised data or today's surviving universe as historical knowledge.",
        "Financial observations have multiple timestamps: the economic period, exchange event time, publication time, vendor receipt, and later revision time. A statement about last quarter was not necessarily available at quarter end. A historical study should use the version available at its decision cutoff or disclose that a point-in-time reconstruction is unavailable.\n\nUniverse membership also changes. Restricting historical training to today's surviving listings can omit delisted or failed firms. Symbols can change and need stable identity mapping. Data access and reuse conditions belong in the source manifest alongside coverage and adjustment conventions.",
        "A filing describes a quarter ending March 31 but is released May 10. A model deciding April 15 cannot use that release merely because its period label says March. Similarly, a record arriving at 21:05 is late for a stipulated 21:00 decision cutoff.",
        "The local CSV schema includes date, symbol, open, close, volume, and available_at. It rejects rows unavailable by its synthetic 21:00 UTC cutoff. This clock is a teaching convention, not a real exchange calendar. For actual research, replace it with the intended venue's sessions, publication rules, and dated membership before making historical claims. Record missing coverage explicitly instead of inferring availability from a populated table.",
        r"availableAt\le decisionAt",
        'print("A 21:05 observation meets a 21:00 cutoff:", 21 * 60 + 5 <= 21 * 60)\nprint("Minutes late:", 5)',
        "Build a data dictionary and source manifest with event time, availability time, revisions, universe membership, and adjustment policy. Identify one unavailable field you would exclude.",
        "Use publication/receipt timing for the decision rule, retain revision lineage, and document membership and missing coverage. A period-end label cannot substitute for the actual availability timestamp.",
        [
            (
                "A March financial period guarantees its report was available in March:",
                ["Yes", "No", "Only for large stocks"],
                1,
                "The reporting period and publication time are different timestamps.",
            ),
            (
                "Today's surviving listings necessarily form a historical unbiased universe:",
                ["Yes", "Only with many firms", "No"],
                2,
                "Survivorship can exclude securities that disappeared.",
            ),
            (
                "An observation arrives at 10:07 for a 10:00 cutoff. It is:",
                ["Seven minutes late", "Available seven minutes early", "Automatically usable"],
                0,
                "Availability occurs after the specified decision time.",
            ),
            (
                "A source manifest should include:",
                [
                    "Only a provider logo",
                    "Coverage, timing, revisions, identifiers, and reuse conditions",
                    "Only the download date",
                ],
                1,
                "These determine whether the data support the intended historical task.",
            ),
        ],
        [ASOF, PIT],
    )

    add(
        "7.3",
        1,
        "Validate schemas, duplicates, prices, and volume",
        "Create a cleaning audit that distinguishes invalid observations, exact duplicates, conflicting revisions, and optional missing features.",
        "Cleaning begins with a data contract, not a command that drops every row containing a null. Validate required columns, identifier/date uniqueness, numeric types, units, price positivity, volume conventions, and timestamp availability. Exact duplicate rows can be removed under an explicit policy; conflicting rows for the same date and symbol need a revision rule rather than an arbitrary keep-last choice.\n\nA missing optional volume feature differs from an invalid tradable price. The project preserves missing volume for training-only imputation, while it excludes nonpositive prices and late observations. Every exclusion is counted in the audit so learners can detect unexpected changes in coverage.",
        "Suppose 101 input rows contain one exact duplicate and two distinct invalid-price rows, with no overlap. Removing them leaves 98 rows. A separate missing-volume value can remain in those rows for later imputation; it need not reduce the count to 97.",
        "Run the project and inspect audit fields rather than only the cleaned file. Add a conflicting duplicate and verify that the cleaner asks for a defined policy by raising an error. Add a negative price, a nonnumeric volume, and an unknown availability time separately. Keep a copy of raw input and a reproducible transformation history. Never repair a negative price by taking its absolute value without evidence of the source error.",
        r"retained=raw-exactDuplicates-excludedUniqueRows",
        'print("Retained rows under disjoint exclusions:", 101 - 1 - 2)\nprint("Optional missing volume does not require another price exclusion:", 98)',
        "Run the seeded cleaning audit, then create one conflicting duplicate and one invalid-price fixture. Explain why these cases have different handling.",
        "Exact duplicates can be deduplicated, conflicting versions require an explicit revision decision, and invalid prices are excluded without inventing a tradable replacement. Optional volume remains missing until the training pipeline handles it.",
        [
            (
                "Taking the absolute value of every negative price is a justified universal repair:",
                ["No", "Yes", "Only in pandas"],
                0,
                "A repair needs source evidence and an explicit transformation rule.",
            ),
            (
                "Conflicting same-key rows require:",
                [
                    "An arbitrary order choice",
                    "A documented revision policy",
                    "Automatic averaging",
                ],
                1,
                "Different observations may represent different information versions.",
            ),
            (
                "200 rows minus two duplicates and three other excluded rows leaves:",
                ["198", "197", "195"],
                2,
                "The disjoint exclusions remove five rows in total.",
            ),
            (
                "A cleaning audit should preserve:",
                [
                    "Counts and reasons for exclusions and retained missingness",
                    "Only the final row count",
                    "Only the model score",
                ],
                0,
                "The transformation history explains what population reaches training.",
            ),
        ],
        [MISSING, PIT],
    )

    add(
        "7.4",
        1,
        "Repair missing data, outliers, and corporate-action discontinuities",
        "Choose defensible repair or exclusion policies without erasing real market events or introducing future information.",
        "An extreme observation can be a source error, a split, a stale quote, or a genuine market jump. These cases have different meanings. Compare raw and adjusted fields, volume, corporate-action records, and neighboring observations before choosing a repair. A model may be harmed by a real jump, but removing it solely because it hurts performance changes the research population.\n\nForward filling an optional slowly changing field can be defensible only with a known availability and staleness rule. Backfilling from a later release uses future information. Tradable prices and target returns should not be invented merely to keep every row in the training matrix.",
        "Ten shares priced at 100 become twenty at 50 in a two-for-one split, preserving value 1,000 before other changes. Treating the raw price change as a −50% economic return creates a false label. Conversely, a genuine fall from 100 to 50 without a split is not repaired by doubling the price.",
        "The synthetic project has no real corporate-action feed and makes no automatic split repair. It removes bad prices and preserves the global observed date grid so feature and target windows do not silently jump across an excluded observation. Add an audit note distinguishing a confirmed correction from a sensitivity-based exclusion. Fit clipping thresholds, if justified, on training data only and report the number and type of observations changed.",
        r"q_{after}P_{after}=q_{before}P_{before}\quad\text{for the idealized split}",
        'print("Before-split value:", 10 * 100)\nprint("After-split value:", 20 * 50)\nprint("Misleading raw price return:", 50 / 100 - 1)',
        "Write separate policies for an exact split, a confirmed bad tick, missing volume, and a real price crash. Include the evidence needed for each action.",
        "A split needs a consistent adjustment/holdings convention, a bad tick needs source-supported correction or exclusion, volume may remain missing for training imputation, and a real crash should remain unless the population rule explicitly excludes it.",
        [
            (
                "A real crash should be removed because it lowers model performance:",
                ["Yes", "No", "Only from test data"],
                1,
                "Outcome-driven deletion distorts the evaluation population.",
            ),
            (
                "Backfilling an earlier feature from a later publication risks:",
                ["Only extra storage", "Only slower training", "Future-information leakage"],
                2,
                "The value was not known at the historical decision cutoff.",
            ),
            (
                "Five shares at 80 become ten at 40. Value is:",
                ["400 before and after", "800 after", "200 after"],
                0,
                "The split changes quantity and price without changing this idealized value.",
            ),
            (
                "Clipping thresholds estimated from the full dataset use:",
                [
                    "Training information only",
                    "Potentially held-out distribution information",
                    "No data information",
                ],
                1,
                "The transformation has learned from observations outside the training slice.",
            ),
        ],
        [MISSING, PIPE],
    )

    add(
        "7.5",
        2,
        "Build dated lagged and rolling features",
        "Construct features within each stock's history and verify that every value is available at prediction time.",
        "A feature is a dated transformation with a unit, lookback, minimum history, and availability rule. Momentum, rolling volatility, volume transformations, and fundamental ratios can be useful candidates, but their definitions must remain identical in training and inference. Group by stable security identity before shifting or rolling so one stock's last row cannot become another stock's lag.\n\nA lag is only meaningful relative to a calendar. Removing a missing row and shifting the remaining rows can turn a one-session label into a longer interval. The project reindexes each stock to the observed global date grid and requires complete price windows for its five-period features.",
        "A five-period close ratio from 100 to 105 gives momentum .05. A feature based on the close at t is available for the project's after-close decision, but not necessarily for an order assumed to have filled at that same close. Execution timing remains part of the contract.",
        "Inspect momentum_5, volatility_5, and log_volume in dataset.csv. Select one row and reconstruct the exact source window. Alter only later prices in a copy and verify that earlier features do not change. For a fundamental extension, perform an as-of join on availability time within the stock and apply an explicit staleness tolerance. Do not join on accounting period alone.",
        r"momentum_{5,t}=C_t/C_{t-5}-1",
        'print("Five-period momentum:", 105 / 100 - 1)\nprint("Momentum after a decline:", 95 / 100 - 1)',
        "Trace one feature row to its six closing prices and volume. Write a future-perturbation test proving earlier features are unchanged.",
        "The row uses only its current and prior declared observations. Later price edits must not alter its features; grouped, dated transformations should preserve that invariant.",
        [
            (
                "Shifting the entire multi-stock table without grouping is always safe:",
                ["No", "Yes", "Only if sorted by price"],
                0,
                "A lag can cross security boundaries and use another asset's observation.",
            ),
            (
                "An as-of fundamental join should use:",
                [
                    "Only fiscal period end",
                    "The field's actual availability time",
                    "The eventual revised value",
                ],
                1,
                "The historical decision can use only information already available.",
            ),
            (
                "A lookback close of 80 and current close 84 give momentum:",
                ["4%", "84%", "5%"],
                2,
                "84/80−1=.05 under the ratio-return definition.",
            ),
            (
                "Changing future observations should leave past features:",
                [
                    "Unchanged under a causal feature pipeline",
                    "Always higher",
                    "Dependent on the final test score",
                ],
                0,
                "Historical features must not depend on later information.",
            ),
        ],
        [ASOF, PIPE],
    )

    add(
        "7.6",
        2,
        "Label returns, classes, and opportunity horizons",
        "Construct labels from the declared executable interval and retain their maturity endpoints for splitting and monitoring.",
        "A target describes the outcome the model should estimate. A next-close return, next-open holding return, market-relative return, and binary profitable-trade label are different tasks. Costs can be included in a target or in a later decision rule, but the convention must be consistent and clearly named.\n\nFuture labels are allowed in historical supervised training only after those outcomes become available. Retain label_end so a training cutoff can exclude labels that extend into validation or test. At inference time, the newest rows have no matured label; they still need features and predictions without inventing outcomes.",
        "At decision t, the next two opening prices are 200 and 198. The project's target is −1% and the positive-sign class is false. If the previous close was 190, using 198/190−1 would define a different interval and falsely include a price move that the stipulated next-open entry did not capture.",
        "Open dataset.csv and verify the entry/exit prices for one positive and one negative row. Keep the last unresolved label rows out of training while allowing them in the separate scoring feature path. If adding multi-day or barrier labels, store actual end times and reconsider overlap, class balance, costs, and purging. Do not select the horizon solely because it produces the best final test chart.",
        r"class_t=\mathbb{1}[O_{t+2}/O_{t+1}-1>0]",
        'target = 198 / 200 - 1\nprint("Executable interval target:", target)\nprint("Positive-sign label:", target > 0)\nprint("Different prior-close interval:", 198 / 190 - 1)',
        "Hand-check two label rows and identify the latest unlabeled observations. Explain how a five-day target would change the split boundary requirements.",
        "Labels use the two future opens specified by the contract. Unmatured rows cannot train the model; longer targets require retaining their actual end times and excluding any overlap with evaluation boundaries.",
        [
            (
                "The newest unlabeled row should be given a zero return for training:",
                ["Yes", "No", "Only for a linear model"],
                1,
                "An unknown outcome is not an observed zero return.",
            ),
            (
                "Changing the return horizon changes:",
                ["Only a heading", "Only file size", "The prediction task and label maturity"],
                2,
                "The outcome interval determines both target meaning and availability.",
            ),
            (
                "Entry 125 and exit 130 produce return:",
                ["4%", "5%", "0.4%"],
                0,
                "130/125−1=.04 for the specified holding interval.",
            ),
            (
                "A label ending after the training cutoff is:",
                [
                    "Always eligible if its feature is old",
                    "Not yet available for that training fit",
                    "Automatically an independent test",
                ],
                1,
                "Training availability depends on the outcome endpoint as well as feature time.",
            ),
        ],
        [SPLIT, PIT],
    )

    add(
        "7.7",
        2,
        "Split by date, group related rows, and purge overlap",
        "Create train, validation, and test partitions that respect financial chronology and label availability.",
        "Random row splitting can place the same market date or overlapping outcome interval in both training and evaluation. For the pooled stock task here, split by global date so all stocks on a date receive the same partition. Keep model selection in validation and reserve test for a frozen procedure.\n\nThe project uses approximately 60%, 20%, and 20% of eligible dates. It purges earlier rows whose label_end reaches the next partition's start. This is stricter than merely checking the feature date. A separate development set combines eligible pre-test observations for a final refit after validation selection.",
        "If validation starts at index 10 and each label ends two indices after its observation, training observations 8 and 9 are excluded: their labels end at 10 and 11. Observation 7 ends at 9 and can qualify. A long irregular label could require an even earlier exclusion.",
        "Inspect report.json split boundaries and assert last training label end is before the first validation decision, and last development label end is before the first test decision. Verify no date appears in two decision partitions. For multi-asset event data, also consider shared events and issuer relationships where they affect the intended generalization claim. Chronology alone does not solve every dependence or selection problem, so state what population the split is designed to represent.",
        r"train_i\ eligible\iff decision_i<cutoff\land labelEnd_i<cutoff",
        'print("Label from observation 7 ends before 10:", 7 + 2 < 10)\nprint("Label from observation 8 ends before 10:", 8 + 2 < 10)',
        "Export the split manifest and prove its endpoint inequalities. Construct one variable-horizon label that an ordinary two-row gap would fail to remove.",
        "Use actual label endpoints in the exclusion rule. An early observation with an unusually long target can overlap the next partition despite falling outside a fixed gap.",
        [
            (
                "Stocks on the same date should be randomly scattered across this task's time partitions:",
                ["No", "Yes", "Only for many tickers"],
                0,
                "The evaluation asks about later market dates, so partition dates consistently.",
            ),
            (
                "Hyperparameter selection should use:",
                [
                    "The final test outcomes",
                    "Validation observations within the development procedure",
                    "Future deployment labels",
                ],
                1,
                "Test data should assess a procedure already selected without them.",
            ),
            (
                "Cutoff 8 and label end i+2 make observation 6:",
                [
                    "Safely inside training",
                    "Unlabeled forever",
                    "Excluded because its label ends at the cutoff",
                ],
                2,
                "The required endpoint is strictly earlier than the next partition start.",
            ),
            (
                "A variable-horizon purge needs:",
                [
                    "The actual endpoint of each label",
                    "Only a fixed count of rows",
                    "Only the number of stocks",
                ],
                0,
                "Irregular outcome intervals cannot always be covered by a constant gap.",
            ),
        ],
        [SPLIT, PIT],
    )

    add(
        "7.8",
        2,
        "Fit imputation and scaling inside the pipeline",
        "Keep preprocessing statistics within the training fit and reuse exactly those transformations for validation, test, and inference.",
        "A transformation can learn from data even when it has no target variable. Medians, means, standard deviations, clipping quantiles, PCA components, and feature selections all carry sample information. Fitting them on the complete dataset exposes the training procedure to held-out observations. A pipeline keeps the transformation and estimator in one fit/predict contract.\n\nThe project uses median imputation, standardization, and an estimator. Optional missing volume is handled by the fitted imputer; invalid price and target windows have already been excluded. Validation and test call predict, not fit_transform, on this pipeline.",
        "Training values [1,2,9] have median 2. A missing validation value should receive that fitted median, even if later values would make the full-sample median much larger. For a feature with training mean 10 and scale 2, an observed value 14 becomes standardized value 2.",
        "Inspect the imputer statistics and scaler means in the fitted artifact. Change only held-out feature values and refit on the unchanged training slice; training statistics must remain identical. When a model is legitimately refitted on the larger pre-test development set, its preprocessing may change because its authorized training population changed. Document that distinction so a valid final refit is not confused with accidental test leakage.",
        r"z=(x-\mu_{train})/\sigma_{train}",
        'print("Training-only imputation value:", 2)\nprint("Standardized value:", (14 - 10) / 2)',
        "Inspect fitted medians and scaling parameters, then perturb only held-out data. Demonstrate that the training fit remains unchanged and explain the separate final development refit.",
        "Training preprocessing depends only on the training slice. A later authorized refit can use pre-test development rows, but never held-out test values to estimate its preprocessing.",
        [
            (
                "Unsupervised scaling on the full dataset cannot leak information:",
                ["True", "False", "True for small datasets"],
                1,
                "Distribution statistics can still reveal held-out information.",
            ),
            (
                "Validation normally uses the fitted pipeline's:",
                [
                    "fit_transform on validation",
                    "New target-aware median",
                    "predict or transform with training parameters",
                ],
                2,
                "Evaluation applies learned transformations without refitting them on the evaluation rows.",
            ),
            (
                "Value 18 with training mean 12 and scale 3 standardizes to:",
                ["2", "6", ".5"],
                0,
                "(18−12)/3=2 under the stated standardization.",
            ),
            (
                "An authorized final refit should exclude:",
                [
                    "All training observations",
                    "Held-out test information",
                    "All preprocessing steps",
                ],
                1,
                "The final fit may use development data while preserving the test boundary.",
            ),
        ],
        [PIPE, MISSING],
    )

    add(
        "7.9",
        3,
        "Baselines, regression loss, and regularization",
        "Train a simple return model and compare it with a baseline before increasing model complexity.",
        "A regression model estimates a numerical target under a chosen loss. Mean squared error emphasizes large residuals, while mean absolute error has a different sensitivity. A constant prediction based on the training mean is a useful baseline for squared error; using the test mean instead would give the baseline information unavailable at deployment.\n\nRidge regression adds a coefficient penalty to least squares. The penalty trades fit against coefficient magnitude and can stabilize correlated predictors. Its scale depends on the objective convention and feature scaling, so record the implementation and preprocessing. A smaller training error alone does not establish a better future model.",
        "Predictions [1,2,3] and outcomes [1,3,5] have errors [0,1,2], MSE 5/3, and MAE 1 in the stated units. If a training-mean baseline has MSE 2, the model improves this particular error comparison by 1−(5/3)/2≈16.7%.",
        "Run the project's three ridge candidates and retain every validation loss. Compare the selected model's held-out error with mean_baseline_mse. Inspect the fitted coefficient scale only after accounting for standardization. Do not interpret a coefficient as a causal effect or a return guarantee. Record a negative result when the baseline wins and identify whether the next justified experiment concerns data, target, features, or model assumptions.",
        r"MSE=n^{-1}\sum_i(y_i-\hat y_i)^2",
        'print("MSE:", (0 ** 2 + 1 ** 2 + 2 ** 2) / 3)\nprint("MAE:", (0 + 1 + 2) / 3)\nprint("Relative MSE improvement:", 1 - ((0 + 1 + 4) / 3) / 2)',
        "Compare every ridge validation result with the final baseline report. Explain what a stronger penalty changes and why test outcomes must not select it.",
        "The penalty changes the fitted coefficient tradeoff; validation selects among declared candidates. Test metrics assess the selected/refitted procedure, and a baseline loss lower than the model's is evidence against an improvement claim.",
        [
            (
                "The constant baseline should be estimated from:",
                [
                    "Eligible training/development outcomes",
                    "The final test outcomes",
                    "The best future month",
                ],
                0,
                "Its information set must match what the deployed procedure could know.",
            ),
            (
                "Ridge regularization changes:",
                [
                    "The dates on which outcomes occurred",
                    "The tradeoff between fit and coefficient magnitude",
                    "Whether test data are future data",
                ],
                1,
                "The penalty constrains the fitted coefficients under the specified objective.",
            ),
            (
                "Errors 1 and 3 have MSE:",
                ["2", "4", "5"],
                2,
                "(1²+3²)/2=5 for these two residuals.",
            ),
            (
                "A lower training MSE alone proves better generalization:",
                ["No", "Yes", "Only with many features"],
                0,
                "Independent evaluation is needed to assess performance beyond the fitted sample.",
            ),
        ],
        [METRIC, PIPE],
    )

    add(
        "7.10",
        3,
        "Train classifiers and understand class imbalance",
        "Fit a direction classifier and distinguish probability, classification threshold, and class prevalence.",
        "Logistic regression models a binary outcome through a probability link. The class definition comes first: the project labels a positive next-open holding return, not a profitable trade after every cost. A probability estimate and a hard decision threshold are separate outputs. Class imbalance can make raw accuracy misleading because predicting the majority class may already score well.\n\nThe project fits logistic candidates on training data, compares validation Brier loss, and refits the selected configuration on eligible development observations. A fixed .55 threshold is declared for the confusion matrix; it is not optimized on test results.",
        "If only 20 of 100 outcomes are positive, predicting negative for every row achieves 80% accuracy and zero positive recall. If a classifier accepts ten opportunities and six are positive, precision is .6; if twenty positives existed, recall is .3. Neither statistic alone describes the magnitude of gains and losses.",
        "Inspect class counts in each date partition before fitting. A training slice with only one class cannot support the intended logistic fit. Compare probabilities with the development class-prior baseline, and retain confusion counts rather than only a headline score. If using weighting or resampling, apply it within training and re-evaluate calibration and the population being represented. Do not balance the final test by deleting inconvenient real outcomes.",
        r"precision=TP/(TP+FP),\quad recall=TP/(TP+FN)",
        'print("Majority-class accuracy:", 80 / 100)\nprint("Accepted-trade precision:", 6 / 10)\nprint("Positive recall:", 6 / 20)',
        "Inspect the fitted classifier, class prevalence, and confusion counts. Compare its Brier score with the prior baseline and explain one reason accuracy can mislead.",
        "A majority-class prediction can achieve high accuracy without retrieving useful positive cases. Probability loss, prevalence, precision, recall, coverage, and economic outcomes answer different evaluation questions.",
        [
            (
                "A positive-return class automatically means profit after all costs:",
                ["Yes", "No", "Only at probability .9"],
                1,
                "The sign label omits costs unless they are explicitly part of its definition.",
            ),
            (
                "A one-class training slice is sufficient for the project's intended logistic fit:",
                ["Always", "Only if large", "No"],
                2,
                "The binary training procedure requires both outcome classes.",
            ),
            (
                "Three true positives among twelve accepted predictions give precision:",
                ["25%", "40%", "75%"],
                0,
                "Precision is 3/12=.25 in this fixture.",
            ),
            (
                "Class balancing or weighting should be fitted or chosen using:",
                ["Final test labels", "The training/development procedure", "Future live labels"],
                1,
                "The independent test must not shape the selected training protocol.",
            ),
        ],
        [CAL, METRIC],
    )

    add(
        "7.11",
        3,
        "Trees, random forests, and boosting comparisons",
        "Evaluate nonlinear models under the same data and split contract as the linear baseline.",
        "A decision tree partitions feature space into regions. Deep trees can fit highly specific patterns, while ensembles combine multiple trees using different construction rules. Random forests average randomized trees; boosting adds models sequentially to improve an objective. Their hyperparameters and uncertainty properties differ, so do not treat all tree ensembles as interchangeable.\n\nThe downloadable project trains a bounded random forest candidate with a fixed seed, depth, leaf size, and tree count. It compares that candidate with ridge using the same training and validation observations. Gradient boosting is a documented extension exercise, not a hidden implementation in the supplied run.",
        "Suppose ridge validation MSE is .00018 and a forest's is .00016, while their training errors are .00015 and .00003. The forest wins this stipulated validation comparison, but its very low training error alone would not justify selection. The final independent result may still favor the simpler baseline.",
        "Inspect the candidate definition and validation trial ledger. Change one complexity parameter in a new development experiment, record the added trial, and compare both training and validation behavior. Keep missing-data handling and feature definitions consistent. If adding boosting, disable or carefully control any internal validation scheme that violates the time contract. Record runtime and memory as engineering costs alongside statistical performance.",
        r"ensemble\ prediction=B^{-1}\sum_{b=1}^{B}f_b(x)\quad\text{for an averaging ensemble}",
        'print("Mean of three tree predictions:", (0.01 + 0.02 - 0.003) / 3)\nprint("Illustrative validation improvement:", 1 - 0.00016 / 0.00018)',
        "Compare the forest and ridge validation entries. Propose one bounded forest or boosting extension and specify how its internal validation will preserve chronology.",
        "Use identical authorized data and metrics, record the new trial, and constrain complexity. Any early-stopping validation must stay inside development chronology; the test cannot choose the extension.",
        [
            (
                "A much smaller training loss alone justifies choosing a deep tree:",
                ["No", "Yes", "Only for stocks"],
                0,
                "A flexible model can fit noise that does not generalize.",
            ),
            (
                "The supplied nonlinear regression candidate is:",
                ["An LSTM", "A bounded random forest", "A live reinforcement-learning trader"],
                1,
                "The project explicitly defines a random forest with fixed construction settings.",
            ),
            (
                "Tree predictions .01, .02, and .03 average to:",
                [".06", ".03", ".02"],
                2,
                "The arithmetic mean is (.01+.02+.03)/3=.02.",
            ),
            (
                "A boosting extension's early stopping must respect:",
                [
                    "The same chronological development boundaries",
                    "The final test's best date",
                    "Only a default random split",
                ],
                0,
                "Internal selection is still part of the training procedure.",
            ),
        ],
        [TREE, TUNE],
    )

    add(
        "7.12",
        3,
        "Neural networks and sequence-model readiness",
        "Understand what a neural model adds and design a fair bounded extension before investing in architecture search.",
        "A neural network composes learned transformations under an optimization objective. Hidden width, depth, regularization, learning rate, batch construction, and stopping criteria influence both capacity and training behavior. More parameters do not create information absent from the features or repair mislabeled outcomes. A small tabular baseline remains a useful reference even when sequence architectures are being considered.\n\nSequence windows introduce additional alignment and overlap requirements. The last input timestamp must precede the decision cutoff, while the target interval must remain separate. Randomly distributing overlapping windows across partitions can share substantial historical information and outcome structure.",
        "A dense layer with three inputs and four hidden units has 3×4 weights and four biases, totaling sixteen parameters. A single output connected to those four units adds five, for twenty-one in this small two-layer example. This count describes capacity, not the number of independent financial observations.",
        "Design a local MLPRegressor extension using the primary documentation and the existing pipeline interface. Keep the parameter budget small, seed recorded, scaling fitted within training, and validation chronological. The supplied default project does not train a neural model; your extension must produce its own trial and convergence evidence. Compare runtime, validation loss, and sensitivity with ridge and forest before claiming that a larger sequence model is warranted.",
        r"dense\ parameters=n_{in}n_{out}+n_{out}",
        'print("Input-to-hidden parameters:", 3 * 4 + 4)\nprint("Hidden-to-output parameters:", 4 * 1 + 1)\nprint("Total:", 3 * 4 + 4 + 4 + 1)',
        "Specify a small neural extension with parameter count, optimization settings, stopping rule, and a time-respecting comparison plan. Optionally implement it as an additional local candidate.",
        "The plan must preserve the existing target and split contract, document convergence and added trials, and compare independent validation behavior with simpler models. Architecture size alone is not evidence of improvement.",
        [
            (
                "A larger neural network automatically repairs target leakage:",
                ["Yes", "No", "Only with dropout"],
                1,
                "Information leakage is a data/evaluation design failure, not a capacity shortage.",
            ),
            (
                "Overlapping sequence windows require attention to:",
                [
                    "Only tensor color",
                    "Only GPU brand",
                    "Timing, grouping, and label overlap across partitions",
                ],
                2,
                "Window construction can share information across an intended evaluation boundary.",
            ),
            (
                "A dense layer with five inputs and two outputs has parameters:",
                ["12", "10", "7"],
                0,
                "Five times two weights plus two biases equals twelve.",
            ),
            (
                "The default project already trains a deep sequence model:",
                ["Yes", "No; neural training is an explicit extension", "Only during scoring"],
                1,
                "The shipped candidates are ridge, forest, and logistic models.",
            ),
        ],
        [NN, PIT],
    )

    add(
        "7.13",
        4,
        "Hyperparameter search and walk-forward evaluation",
        "Control the search procedure and distinguish one validation split from repeated chronological evaluation.",
        "Every tried feature set, hyperparameter, seed choice, and stopping rule is part of the research search. A small declared candidate set is easier to audit than an undocumented sequence of improvements. Record the primary validation metric and tie-breaking rule before fitting. The best validation result is selected evidence, not an untouched estimate of future performance.\n\nThe project implements a single chronological train/validation/test design. Walk-forward and nested designs are extensions: repeat the selection procedure within each outer training history, then evaluate its frozen choice on the next dated block. Do not describe the supplied single split as a full nested backtest.",
        "Three candidates have validation losses .020, .018, and .021. The second wins the declared minimum-loss rule. If the researcher then sees a poor final test and adds a fourth candidate tailored to it, that test has become development evidence. A new independent evaluation or an explicit limitation is needed.",
        "Save the full trial ledger and split manifest. Use the advanced research lab's interval-purged splits as a starting point for a three-origin extension, but fit preprocessing and model selection afresh within each permitted history. Aggregate losses with declared date/row weighting and report variation across origins. Record computational budget and failed fits rather than silently dropping them from the comparison.",
        r"\hat\lambda=\arg\min_{\lambda\in\Lambda}L_{validation}(\lambda)",
        'print("Best declared validation loss:", min(0.020, 0.018, 0.021))\nprint("Mean of three outer-fold losses:", (0.02 + 0.03 + 0.025) / 3)',
        "Draw a three-origin walk-forward plan with an inner selection interval at each origin. State which artifacts are refitted and how label overlap is removed.",
        "Each origin refits preprocessing and candidate models using only its eligible history, selects inside that history, and scores the next frozen block. Actual label endpoints govern purging.",
        [
            (
                "The project's default single validation split is a nested walk-forward evaluation:",
                ["No", "Yes", "Only with four candidates"],
                0,
                "Nested evaluation requires repeated outer tests and inner selection procedures.",
            ),
            (
                "Changing candidates after inspecting test results makes that test:",
                [
                    "Untouched independent evidence",
                    "Part of the development process",
                    "A training-free proof",
                ],
                1,
                "The procedure has used information from the evaluation outcome.",
            ),
            (
                "Losses .04, .03, and .05 have equal-weight mean:",
                [".03", ".12", ".04"],
                2,
                "Their sum .12 divided by three is .04.",
            ),
            (
                "A search ledger should include:",
                [
                    "Failed fits and unsuccessful candidates",
                    "Only the winner",
                    "Only the model family name",
                ],
                0,
                "The search history is needed to interpret selection and reproducibility.",
            ),
        ],
        [TUNE, SPLIT],
    )

    add(
        "7.14",
        4,
        "Read regression, ranking, and classification metrics",
        "Match evaluation metrics to the task and preserve denominators, baselines, and undefined cases.",
        "MSE and MAE evaluate numerical prediction errors in different ways. R-squared compares squared error with variation around the evaluated sample mean and can be negative. An out-of-sample improvement against an available training-mean baseline is a related but distinct comparison. Classification metrics such as ROC AUC and average precision assess ordering under different summaries; neither directly measures tradable profit.\n\nPrecision and recall require their denominators. When no positives are predicted, precision is undefined under the project's convention. A one-class evaluation slice also cannot supply ordinary two-class ROC AUC. Reporting null with a reason is more informative than fabricating a perfect score.",
        "A model MSE .8 against an available baseline MSE 1 gives a 20% relative improvement. A classifier with TP=8, FP=2, and FN=12 has precision .8 and recall .4. The high precision does not show that it found most positives or that its positive predictions had favorable payoff magnitudes.",
        "Read the project's full held-out metric report and compare every model metric with the appropriate baseline. Reconstruct confusion counts and verify they sum to the test sample size. Add a per-date or per-stock error table to detect domination by a large subgroup. Do not choose the final headline metric after discovering which makes the model look strongest; distinguish exploratory summaries from the metric declared in the contract.",
        r"relative\ MSE\ improvement=1-MSE_{model}/MSE_{baseline}",
        'print("Relative MSE improvement:", 1 - 0.8 / 1)\nprint("Precision:", 8 / (8 + 2))\nprint("Recall:", 8 / (8 + 12))',
        "Recompute three reported metrics from predictions.csv. Include one baseline comparison and explain how the project represents an undefined denominator.",
        "Use the declared prediction/outcome columns and counts. Compare like-for-like task metrics; undefined precision or ROC AUC should be reported with its sample condition rather than silently treated as success.",
        [
            (
                "ROC AUC directly measures net trading profit:",
                ["Yes", "No", "Only above .5"],
                1,
                "Ranking quality and economic payoffs are separate evaluation questions.",
            ),
            (
                "No predicted positives means precision should automatically be one:",
                ["Always", "Only in finance", "No; use a declared undefined-value convention"],
                2,
                "The precision denominator is zero in that case.",
            ),
            (
                "Model MSE .6 and baseline .75 imply improvement:",
                ["20%", "15%", "80%"],
                0,
                "1−.6/.75=.2 for this relative loss comparison.",
            ),
            (
                "A metric report should identify:",
                [
                    "Only its largest number",
                    "Task, population, baseline, and denominator",
                    "Only the library name",
                ],
                1,
                "These determine what the reported value actually measures.",
            ),
        ],
        [METRIC, CAL],
    )

    add(
        "7.15",
        4,
        "Calibration, probability loss, and cost thresholds",
        "Evaluate probability reliability and choose decision rules using development evidence and explicit payoff assumptions.",
        "Calibration asks whether predicted probabilities correspond to observed outcome frequencies in an appropriate evaluation population. It differs from ranking: a model can sort cases well while systematically overstating probabilities. Reliability bins, Brier score, and log loss provide complementary views, with finite-sample uncertainty and binning choices still relevant.\n\nThe project reports probability bins and Brier loss but does not fit an additional post-hoc calibrator. A calibration extension must reserve suitable development observations or use a carefully specified cross-fitting procedure. Fitting it on the final test would consume that evaluation boundary.",
        "For two binary outcomes [1,0] with probabilities [.8,.3], Brier loss is ((1−.8)^2+(0−.3)^2)/2=.065. Under a separate payoff model with gain 3, loss 2, and cost .2, expected payoff becomes positive only when probability exceeds .44. This threshold depends on those stipulated conditional payoffs.",
        "Inspect each reliability bin's count before interpreting a probability gap. Compare the classifier with the class-prior baseline. Write a threshold policy that accounts for costs and abstention, and freeze it before the independent test. The fixed .55 report threshold is a declared classification convention, not a universal optimal trading rule. Document a change in gain/loss asymmetry or cost that would invalidate an earlier threshold.",
        r"Brier=n^{-1}\sum_i(p_i-y_i)^2,\quad p^*=(L+c)/(G+L)",
        'print("Brier loss:", ((0.8 - 1) ** 2 + (0.3 - 0) ** 2) / 2)\nprint("Stipulated payoff threshold:", (2 + 0.2) / (3 + 2))',
        "Recompute a reliability bin and Brier score, then derive a threshold for gain 4, loss 1, and cost .25. Explain where a calibrator could be fitted without using test outcomes.",
        "The threshold is .25 under those payoffs. A calibrator belongs in reserved development data or an explicitly time-respecting cross-fitting procedure, with the test remaining independent.",
        [
            (
                "Good ranking guarantees calibrated probabilities:",
                ["No", "Yes", "Only for logistic models"],
                0,
                "Ordering and probability-frequency agreement are distinct properties.",
            ),
            (
                "The project automatically fits a separate post-hoc calibrator:",
                ["Yes", "No; it reports calibration diagnostics", "Only on the test set"],
                1,
                "An additional calibration model is an explicit development extension.",
            ),
            (
                "Probability .7 for an outcome of 1 has squared probability error:",
                [".3", ".49", ".09"],
                2,
                "(.7−1)²=.09 for that observation.",
            ),
            (
                "An economic threshold is conditional on:",
                [
                    "Payoffs, costs, probability meaning, and the evaluated population",
                    "Only model complexity",
                    "Only the stock ticker",
                ],
                0,
                "A universal threshold cannot represent all decision economics.",
            ),
        ],
        [CAL, METRIC],
    )

    add(
        "7.16",
        4,
        "Evaluate returns, costs, exposure, and practical limits",
        "Translate predictions into a declared opportunity rule while distinguishing a return proxy from a full execution simulation.",
        "Statistical improvement is only one input to an investment decision. A policy also specifies which predictions create exposure, how much, when entry and exit occur, and what costs and constraints apply. Report a gross-to-net bridge and compare with a baseline under the same opportunity set. Avoid annualizing a short favorable interval into a confident long-term claim.\n\nThe project uses an explicit opportunity proxy: predictions above the stipulated round-trip cost select next-open-to-following-open opportunities, equal weights are capped at .4 per selected stock, and each daily round trip pays the full stated cost. It does not simulate broker cash, queue position, settlement, or borrow.",
        "Two selected stocks each receive weight .4 and cash keeps .2. Their realized returns are .02 and −.01, so gross portfolio contribution is .004. At .001 round-trip cost on each invested weight, cost is .0008 and net contribution .0032. A single selected stock remains capped at .4 rather than becoming a fully invested position.",
        "Inspect opportunities.json and reconcile one date by hand. Re-evaluate the same frozen predictions under several predeclared cost scenarios, separating sensitivity analysis from threshold retuning. Compare selected count, exposure, compounded proxy return, and adverse dates. Before connecting the model to the paper-bot lab, reconcile its target weights with actual fills and cash under that simulator's different assumptions. A profitable proxy alone is insufficient evidence for live deployment.",
        r"r_{net,t}=\sum_i w_{i,t}r_{i,t}-c\sum_i w_{i,t}",
        'gross = 0.4 * 0.02 + 0.4 * (-0.01)\nprint("Gross contribution:", gross)\nprint("Round-trip cost:", 0.001 * 0.8)\nprint("Net contribution:", gross - 0.001 * 0.8)',
        "Reconcile one opportunity date and run a cost sensitivity. List the extra assumptions required to use the predictions in the paper-bot execution project.",
        "Reconcile weights, returns, and the full stipulated round-trip cost. Paper integration additionally needs timing parity, actual fills, cash/position constraints, freshness, and deterministic risk controls.",
        [
            (
                "The opportunity proxy implements a complete broker execution ledger:",
                ["Yes", "No", "Only with three stocks"],
                1,
                "Its stated scope omits queues, settlement, and full cash accounting.",
            ),
            (
                "One selected stock under the .4 cap receives weight:",
                ["1", "0", ".4"],
                2,
                "The concentration cap leaves the remaining allocation in cash.",
            ),
            (
                "Gross .006 minus costs .0015 gives net:",
                [".0045", ".0075", ".0015"],
                0,
                "Net contribution subtracts the specified cost from gross.",
            ),
            (
                "A cost sensitivity using frozen predictions should distinguish:",
                [
                    "Only model file size",
                    "Changed cost assumptions from a retuned selection rule",
                    "Only chart color",
                ],
                1,
                "Changing the decision threshold is another development choice, not merely rescoring costs.",
            ),
        ],
        [METRIC, PIT],
    )

    add(
        "7.17",
        5,
        "Diagnose errors by stock, date, and market condition",
        "Investigate where predictions fail without turning the final test into an undocumented tuning set.",
        "An average loss can hide large differences across stocks, dates, liquidity conditions, missing-data patterns, and outcome magnitudes. Error analysis connects a failure to an actionable hypothesis: stale features, a wrong label, an unrepresented population, an unstable relation, or a model that cannot express the relevant pattern. Begin with the largest residuals and a random sample of ordinary cases so the investigation does not focus only on spectacular exceptions.\n\nSlices chosen after seeing test outcomes are exploratory. They can guide a new development cycle, but repeated corrections informed by the same test do not create repeated independent confirmations.",
        "A model has MSE .5 on 80 rows and MSE 2 on 20 rows. Its pooled MSE is .8, which conceals the weaker subgroup. An equal-weight mean of the two subgroup scores is 1.25 and answers a different weighting question. State whether the unit of evaluation is a row, stock, date, or opportunity.",
        "Add a grouped error table from predictions.csv and trace three large residuals back to the raw and cleaned rows. Check the feature window, label interval, available_at, and cleaning audit before changing the model. Compare against the same baseline within each slice. Record whether the observed issue is a confirmed data fault, an uncertain statistical pattern, or a limitation of the task itself, then define the next experiment without retroactively rewriting the current report.",
        r"MSE_{pooled}=\frac{n_1MSE_1+n_2MSE_2}{n_1+n_2}",
        'print("Pooled MSE:", (80 * 0.5 + 20 * 2) / 100)\nprint("Equal-slice MSE:", (0.5 + 2) / 2)',
        "Produce per-stock and per-date error summaries, inspect three residuals, and classify each finding as data fault, model limitation, or unresolved evidence.",
        "Trace errors through the complete data/label path and preserve the weighting convention. Post-test findings guide a new research cycle and must be disclosed as exploratory.",
        [
            (
                "A pooled score proves every stock is predicted equally well:",
                ["No", "Yes", "Only with many dates"],
                0,
                "Subgroup performance can vary beneath an aggregate metric.",
            ),
            (
                "A test-driven slice discovered after evaluation is:",
                [
                    "A prespecified independent hypothesis",
                    "Exploratory evidence for further investigation",
                    "Automatically causal",
                ],
                1,
                "The slice was selected using the observed evaluation outcomes.",
            ),
            (
                "MSE 1 on 30 rows and 3 on 10 rows give pooled MSE:",
                ["2", "4", "1.5"],
                2,
                "(30×1+10×3)/40=1.5 under row weighting.",
            ),
            (
                "Before changing architecture after a large residual, inspect:",
                [
                    "The raw data, feature timing, label, and baseline case",
                    "Only the model's name",
                    "Only the best date",
                ],
                0,
                "An upstream data or task error can explain the apparent model failure.",
            ),
        ],
        [METRIC, PIT],
    )

    add(
        "7.18",
        5,
        "Feature importance, correlated predictors, and explanations",
        "Use model inspection to describe dependence on inputs without confusing predictive attribution with causality.",
        "Feature importance depends on the model, evaluation data, metric, and inspection procedure. Permutation importance measures how a fitted model's score changes when a feature is disrupted under a specified permutation design. A feature with low importance may still contain useful information that another correlated feature supplies. Conversely, a highly important feature can be a leaked target proxy.\n\nFor time-dependent financial data, unrestricted row permutation changes temporal structure. Choose and describe a diagnostic permutation scheme appropriate to the question, and avoid claiming that its importance score is a causal intervention effect.",
        "A model's held-out MSE is .010. After a specified feature permutation it becomes .014, an increase of .004. This suggests reliance on that feature under this diagnostic. If another near-duplicate feature remains intact, the increase may be small even when both represent useful information.",
        "Use the primary permutation-importance API in a separate development analysis on the fitted pipeline. Repeat the diagnostic with fixed seeds and retain its variation. Compare individual and grouped disruption of correlated features, and inspect feature provenance whenever importance is suspiciously large. The supplied report does not automatically calculate explanations; this assignment adds a documented inspection artifact without changing the frozen model or claiming causality.",
        r"importance_j=L_{permuted\ j}-L_{original}",
        'print("Permutation loss increase:", 0.014 - 0.010)\nprint("Relative loss increase:", 0.014 / 0.010 - 1)',
        "Create a development-only feature inspection report. Explain correlated-feature substitution and why a large importance value should trigger a leakage review.",
        "Importance measures dependence under the chosen disruption and metric. Correlated inputs can substitute, and a target-derived feature can look extremely useful while invalidating the experiment.",
        [
            (
                "Permutation importance establishes a causal stock-return effect:",
                ["Yes", "No", "Only if positive"],
                1,
                "Predictive reliance under a diagnostic is not causal identification.",
            ),
            (
                "A near-duplicate correlated feature can make individual permutation importance:",
                [
                    "Universally infinite",
                    "A proof of uselessness",
                    "Small because the model can use the substitute",
                ],
                2,
                "Information redundancy changes the effect of disrupting one column.",
            ),
            (
                "Loss rising from .03 to .05 after permutation gives increase:",
                [".02", ".08", ".6"],
                0,
                "Subtract original loss from the perturbed loss.",
            ),
            (
                "An unexpectedly dominant feature warrants:",
                [
                    "Only a celebratory chart",
                    "Inspection of its provenance and availability",
                    "Automatic live trading",
                ],
                1,
                "Strong apparent predictiveness can result from leakage or a labeling error.",
            ),
        ],
        [IMPORTANCE, PIT],
    )

    add(
        "7.19",
        5,
        "Stress regimes, uncertainty, and repeated research trials",
        "Assess model stability under dependent data and disclose the selection process behind reported success.",
        "A finite financial sample contains dependence and changing conditions. A model that works in one volatility or liquidity regime may fail in another. Compare prespecified windows and adverse scenarios, but do not select only the favorable period for the final claim. Row-level uncertainty formulas can overstate effective information when many stocks share the same market date or labels overlap.\n\nRepeated research introduces selection bias. The family includes feature and data choices as well as model hyperparameters. A bootstrap around a fixed selected winner does not automatically account for the search that produced it.",
        "Under an illustrative independence assumption, 20 true-null tests at .05 have probability 1−.95^20≈.642 of at least one rejection. Bonferroni testing at family level .05 uses .0025 per test without requiring that independence assumption for its familywise bound. Neither calculation converts a statistical rejection into executable profit.",
        "Write a trial register and a stability report across dated windows, missingness conditions, and cost scenarios. For a bootstrap extension, resample a declared dependence unit such as date blocks and explain the stationarity and block-length assumptions. Link the exercise to econometrics 3.27–3.28 and bot lesson 5.42. Preserve uncertainty about scarce stress observations rather than inventing a precise crisis-performance estimate.",
        r"\alpha_{per\ test}=\alpha_{family}/M",
        'print("Twenty-test Bonferroni threshold:", 0.05 / 20)\nprint("Independent chance of at least one rejection:", 1 - 0.95 ** 20)',
        "Prepare a dated stability table and trial ledger. Design a date-block uncertainty experiment and explain which selection effects it would still leave unresolved.",
        "The design should preserve an appropriate scale of shared/time dependence, disclose block choices, and distinguish uncertainty conditional on a fixed model from the broader process that selected it.",
        [
            (
                "Resampling individual stock rows always preserves market-date dependence:",
                ["No", "Yes", "Only with many bootstrap draws"],
                0,
                "Independent row resampling can break the common-date structure.",
            ),
            (
                "A research family includes:",
                [
                    "Only the final model",
                    "Tried features, labels, data rules, and models",
                    "Only published successes",
                ],
                1,
                "Each data-informed alternative can contribute to selection.",
            ),
            (
                "Family level .05 over 100 tests gives Bonferroni threshold:",
                [".05", ".005", ".0005"],
                2,
                ".05/100=.0005 for the stated family rule.",
            ),
            (
                "A scarce stress sample should lead to:",
                [
                    "Explicit uncertainty and limited claims",
                    "A guaranteed crisis return",
                    "Deleting adverse observations",
                ],
                0,
                "Limited evidence constrains how precisely stress performance can be stated.",
            ),
        ],
        [PIT, SPLIT],
    )

    add(
        "7.20",
        5,
        "Fix data faults and run a controlled retraining cycle",
        "Choose between data repair, feature redesign, model changes, and retirement using a documented diagnosis.",
        "Retraining is a controlled change to a model artifact, not a universal response to every bad result. A broken feed requires data repair; a changed target definition requires a new task version; unstable estimates may require a simpler model or more suitable data. Some hypotheses should be retired when repeated evidence fails to support them.\n\nA repair should preserve raw input, identify affected observations, state the source-supported correction, and regenerate downstream artifacts. Changing a historical feature or label can invalidate old comparisons even if the model code stays identical.",
        "A confirmed unit error multiplies one volume column by 1,000 on 20 dates. Correcting those values affects their transformed volume features and potentially the fitted imputer/scaler and model. The fix should be versioned as a data change. It should not silently overwrite the old report and make the improvement appear to come from a new architecture.",
        "Create a fault ticket with evidence, impact interval, repair rule, tests, and acceptance criteria. Run a new output directory and compare data hashes, audit counts, split boundaries, selected models, and metrics. If the repair was discovered through the final test, disclose that reuse and plan new independent evidence before a stronger claim. Retain the previous artifact for reproducibility and define when the research idea should stop receiving additional tuning.",
        r"correctedValue=reportedValue/unitMultiplier",
        'print("Corrected volume:", 2500000 / 1000)\nprint("Relative unit error factor:", 2500000 / 2500)',
        "Introduce a known volume-unit fault in a local copy, document its detection and repair, and run a new experiment directory with a change log.",
        "Preserve both raw versions and identify affected rows. Correct according to the known unit error, regenerate features and fits, and attribute resulting differences to the documented data change.",
        [
            (
                "Every performance alert should trigger immediate automatic retraining:",
                ["Yes", "No", "Only for trees"],
                1,
                "Diagnosis may call for data repair, a halt, review, or retirement instead.",
            ),
            (
                "A repaired dataset should silently replace all old evidence:",
                ["Always", "Only if better", "No"],
                2,
                "Versioned artifacts are necessary to reproduce and interpret the change.",
            ),
            (
                "A value 800,000 overstated by a factor of 100 corrects to:",
                ["8,000", "80,000", "800"],
                0,
                "Divide the reported value by the confirmed unit multiplier.",
            ),
            (
                "A repair discovered through test inspection means:",
                [
                    "The test remains completely untouched",
                    "The report should disclose test-informed development",
                    "The old prediction task never existed",
                ],
                1,
                "The evaluation evidence has influenced the revised procedure.",
            ),
        ],
        [MISSING, SAVE],
    )

    add(
        "7.21",
        6,
        "Persist pipelines, versions, and a model card",
        "Package the full fitted transformation and estimator with reproducibility evidence and a precise intended-use statement.",
        "A model artifact includes more than coefficients. It needs feature names and order, preprocessing, target definition, training data identity, split boundaries, selected parameters, dependency versions, and validation evidence. A model card connects those details to intended use, evaluated population, known limits, and release responsibility.\n\nThe project writes fitted regression and classification pipelines, report.json, predictions.csv, cleaning and dataset files, opportunity output, and MODEL_CARD.md. It hashes the input and model files and verifies a save/load prediction round trip for artifacts created by that run.",
        "If training uses feature order [momentum, volatility, log-volume] but inference swaps the first two columns, the same three numbers describe a different input vector. A file that loads successfully can still be semantically wrong. Schema and transformation identity therefore belong beside binary integrity checks.",
        "Run the project into a new directory and inspect every output. Joblib uses Python serialization capable of executing code during loading: use only your own trusted artifacts and a matching environment. A matching hash proves consistency with a manifest, not that an untrusted manifest is safe. Record which model and data version a report evaluates, and keep release approval separate from merely obtaining a saved file or a favorable metric.",
        r"reproducibility=(data,features,split,fit,environment,artifact)",
        'print("Required feature count:", 3)\nprint("Declared independent tasks:", 2)\nprint("A saved file alone authorizes trades:", False)',
        "Inspect the model card, hashes, versions, and saved pipelines. Demonstrate prediction parity after loading your own artifact and document the feature order.",
        "The full pipeline must reproduce predictions in the matching environment with the same schema. Load only trusted local serialization and preserve the report linking the artifact to its data and evaluation.",
        [
            (
                "A file hash alone makes an arbitrary downloaded Python model safe to load:",
                ["No", "Yes", "Only if SHA-256"],
                0,
                "Integrity relative to a manifest does not establish trust in its origin or contents.",
            ),
            (
                "The persisted artifact should include:",
                [
                    "Only the final coefficient",
                    "The fitted preprocessing and estimator contract",
                    "Only the model family name",
                ],
                1,
                "Inference must use the same transformations learned during fitting.",
            ),
            (
                "Swapping two feature columns while keeping three columns total:",
                [
                    "Always preserves meaning",
                    "Only changes display",
                    "Can change the model's input semantics",
                ],
                2,
                "Feature count alone does not validate feature identity and order.",
            ),
            (
                "A model card should identify:",
                [
                    "Intended use, data, evaluation, limits, and artifact version",
                    "Only the best metric",
                    "Only the author photo",
                ],
                0,
                "The card connects the model to its tested scope and operational context.",
            ),
        ],
        [SAVE, PIPE],
    )

    add(
        "7.22",
        6,
        "Batch inference, feature parity, and shadow release",
        "Score new dated feature rows without requiring their future outcomes and keep predictions separate from execution authority.",
        "Inference consumes available features and a frozen fitted pipeline. It must not require the future target to construct a prediction. The project's batch-scoring path retains eligible latest feature rows even when their next two opens are unknown, while the training path requires matured labels. This separation prevents a common mistake in which a research table is mistaken for a live feature service.\n\nBatch output is a prediction artifact, not an order. A shadow release compares predictions and operational behavior without granting trading authority. A later paper integration needs a deterministic adapter for timing, sizing, risk limits, stale-data handling, and account reconciliation.",
        "A dataset ends on Friday under its declared calendar. The latest valid feature row can receive a prediction even though the next two opening prices are absent. Its actual outcome remains pending. Filling the target with zero would fabricate evaluation evidence; dropping it from inference would prevent the intended current prediction.",
        "Use --score-run with the directory of your own generated artifact, --csv with the input file, --trust-local-model, and a fresh --output directory. The scorer checks versions, feature schema, and artifact hashes before loading the trusted local pipeline. Compare historical batch predictions with the run's stored predictions, then inspect the additional unmatured rows. Document missing-history or freshness failures as abstentions or exclusions, not invented feature values.",
        r"prediction_t=f_{frozen}(features_{available,t})",
        'print("Feature available:", True)\nprint("Future outcome required for inference:", False)\nprint("Trading authority granted by a prediction:", False)',
        "Run batch scoring on your own saved artifact. Verify parity for overlapping historical rows and confirm that latest eligible rows can be scored without future labels.",
        "Historical predictions should match the frozen pipeline, while extra latest rows retain unknown outcomes. The output is a local batch artifact and does not submit trades.",
        [
            (
                "A live prediction requires its future label to be known:",
                ["Yes", "No", "Only for regression"],
                1,
                "Inference uses features; the future outcome becomes available only later for evaluation.",
            ),
            (
                "A shadow prediction automatically grants order authority:",
                ["Always", "Only above .55", "No"],
                2,
                "Execution permission and deterministic controls are separate from model output.",
            ),
            (
                "Ten historical rows plus two eligible unmatured rows can produce how many batch predictions:",
                ["12", "10 only", "2 only"],
                0,
                "The inference path does not require labels for otherwise valid feature rows.",
            ),
            (
                "A feature-schema mismatch should trigger:",
                [
                    "Silent column rearrangement",
                    "An explicit rejection or reviewed migration",
                    "Automatic retraining on the test set",
                ],
                1,
                "The frozen model's input meaning must remain consistent.",
            ),
        ],
        [PIPE, SAVE],
    )

    add(
        "7.23",
        6,
        "Monitor data drift, mature labels, and release decisions",
        "Track operational input quality and delayed predictive outcomes with explicit review and rollback policies.",
        "Monitoring should distinguish input failures from model-performance changes. Missingness, timestamp freshness, feature distribution, prediction coverage, and processing failures describe operational behavior. Calibration, loss, and realized opportunity outcomes require labels that have matured. Treat pending outcomes separately rather than classifying them as failures or successes.\n\nThe report includes descriptive missingness and standardized feature-mean shifts between development and test data. These are diagnostics, not automatic statistical significance tests or retraining decisions. A shifted feature mean can reflect a real market change, a unit fault, or a different population.",
        "Missingness rises from 2 of 200 rows to 10 of 100, moving from 1% to 10%, a nine-percentage-point increase. If a feature's reference mean is 5 and standard deviation 2, a current mean of 8 has standardized shift 1.5. Neither calculation identifies the cause by itself.",
        "Write a monitoring table with metric, window, minimum sample, threshold, owner, and response. Separate hard data-validity or freshness failures from softer model-review triggers. Compare a challenger on the same matured opportunities before release and preserve the old model's artifact and prediction history. Rollback changes the software version; a trading integration must still preserve actual economic fills and positions. Define retirement conditions when data quality or supported usefulness cannot be restored.",
        r"meanShift=(\mu_{current}-\mu_{reference})/\sigma_{reference}",
        'print("Missingness increase in percentage points:", 100 * (10 / 100 - 2 / 200))\nprint("Standardized mean shift:", (8 - 5) / 2)',
        "Create a monitoring and response table using report.json. Add separate rules for stale features, a unit shift, delayed labels, and uncertain performance degradation.",
        "Each rule needs a sample/window and owner. Hard invalid inputs can halt scoring, while uncertain performance requires mature-label evidence and review; neither automatically authorizes uncontrolled retraining.",
        [
            (
                "A feature mean shift alone proves the model has lost economic value:",
                ["No", "Yes", "Only above one standard deviation"],
                0,
                "The diagnostic does not by itself identify cause or conditional performance.",
            ),
            (
                "Pending labels should be:",
                [
                    "Scored as zero-return outcomes",
                    "Reported separately until their outcomes mature",
                    "Counted as correct predictions",
                ],
                1,
                "Unknown outcomes cannot be treated as observed evaluation evidence.",
            ),
            (
                "Reference mean 10, scale 4, and current mean 12 give standardized shift:",
                ["2", "4", ".5"],
                2,
                "(12−10)/4=.5 under the stated diagnostic.",
            ),
            (
                "A release or rollback decision should preserve:",
                [
                    "Artifact history and actual economic state in any integration",
                    "Only the newest file",
                    "An invented reset of positions",
                ],
                0,
                "Software changes must not rewrite the history of predictions or executed trades.",
            ),
        ],
        [PIT, SAVE],
    )

    add(
        "7.24",
        6,
        "Capstone: the complete stock-ML lifecycle review",
        "Deliver a reproducible data-to-model project and defend its evaluation, repair process, inference behavior, and monitoring plan.",
        "Run the downloadable lifecycle project from a clean environment and assemble the prediction contract, raw/clean data manifest, quality audit, feature and label definitions, chronological split, trial ledger, fitted artifacts, held-out report, error analysis, batch predictions, and model card. Include the monitoring and response table developed in the previous lesson.\n\nComplete one controlled data-fault repair and one inference-parity test. The objective is to show that the lifecycle handles both ordinary operation and a challenged assumption. A negative model result can satisfy the capstone when it is reproduced and interpreted honestly; there is no required profitable curve.",
        "Suppose a model's test MSE is .012 and the available baseline's is .010. Relative improvement is −20%, so the numerical model did not improve that declared loss comparison. If batch parity and data controls pass, the engineering work can still be correct while the investment hypothesis remains unsupported. The decision memo should keep those conclusions separate.",
        "Self-assess 100 points: task/provenance 15, cleaning/features/labels 25, training/selection 20, independent evaluation/diagnosis 20, and artifacts/inference/monitoring 20. Require at least 80 plus no unresolved future-information leak, fabricated outcome, invalid source claim, or untrusted-model loading. The 24 thirty-minute sessions total 12 hours of planned study and project work; the final and checkpoints add assessment time. The automatic exam checks concepts and does not independently inspect your local dossier.",
        r"planned\ study=24\times30=720\ minutes",
        'print("Planned study hours:", 24 * 30 / 60)\nprint("Relative baseline improvement:", 1 - 0.012 / 0.010)\nprint("Rubric total:", 15 + 25 + 20 + 20 + 20)',
        "Submit the complete artifact packet, a controlled repair comparison, historical inference parity, latest-row predictions, monitoring rules, and a one-page release/research decision.",
        "The packet should reproduce the full lifecycle, preserve its independent evaluation boundary, and accurately state whether the model improves the chosen baseline. Critical data or evidence failures override a high rubric score; project review is separate from exam grading.",
        [
            (
                "The capstone requires finding a profitable test curve:",
                ["Yes", "No; a well-supported negative result is valid", "Only for ridge"],
                1,
                "The learning objective is rigorous lifecycle evidence, not selecting a favorable outcome.",
            ),
            (
                "A passing concept exam automatically verifies local project files:",
                ["Yes", "Only at 100%", "No"],
                2,
                "The written and executable artifacts require their own review.",
            ),
            (
                "24 lessons at 30 minutes each total:",
                ["12 hours", "8 hours", "24 hours"],
                0,
                "720 minutes divided by 60 equals twelve hours.",
            ),
            (
                "Model MSE worse than baseline should be described as:",
                [
                    "Guaranteed improvement",
                    "Failure to improve that declared loss comparison",
                    "Proof all ML is useless",
                ],
                1,
                "The conclusion is specific to the evaluated task, sample, and metric.",
            ),
        ],
        [PIT, SAVE, METRIC],
    )

    parts = [
        (
            "Problem and data quality · 2 hours",
            "Define the prediction contract, source timing, schema checks, and defensible repairs.",
        ),
        (
            "Features, labels, and splits · 2 hours",
            "Build causal features, executable targets, purged date partitions, and fitted preprocessing.",
        ),
        (
            "Model training · 2 hours",
            "Baselines, ridge, logistic models, tree ensembles, and a bounded neural extension.",
        ),
        (
            "Selection and evaluation · 2 hours",
            "Hyperparameter search, walk-forward design, metrics, calibration, and cost-aware decisions.",
        ),
        (
            "Diagnosis and improvement · 2 hours",
            "Slice errors, inspect features, stress assumptions, and repair data in a controlled new run.",
        ),
        (
            "Inference, monitoring, and capstone · 2 hours",
            "Persist artifacts, score unseen outcomes, define monitoring, and defend the complete lifecycle.",
        ),
    ]
    track = finish(
        {
            "id": "stock-machine-learning",
            "number": 7,
            "title": "Machine learning for stocks",
            "description": "A 12-hour applied course covering the complete stock-ML lifecycle: data repair, features, labels, training, evaluation, diagnosis, reproducible inference, and monitoring.",
            "source": "Original Quanta course · primary pandas and scikit-learn documentation",
            "level": "Intermediate → advanced",
            "icon": "machine-learning",
            "studyType": "applied",
            "modules": modules,
            "prerequisites": "Basic Python and probability; study Quantitative Investment Analysis and the regression units in Financial econometrics first. Guided worksheets run in the app. The full project runs locally with the pinned Python scientific stack, using synthetic stock data by default.",
            "outcomes": [
                "Audit and repair market datasets without future-information leakage.",
                "Build dated features, matured labels, and purged chronological evaluation.",
                "Train and compare regression, classification, and tree models with baselines.",
                "Interpret calibration, errors, costs, selection uncertainty, and model limitations.",
                "Save fitted pipelines, verify batch inference parity, and define drift/retraining policies.",
                "Deliver a complete reproducible lifecycle dossier and a justified research decision.",
            ],
            "readingGuide": "24 lessons × 30 minutes = 12 hours: six two-hour units. Each session budgets 8 minutes for the lesson and primary reading, 8 for a worked worksheet, and 14 for the local project assignment and review. This is a study-time estimate, not 12 hours of video. There are 48 practice questions, five checkpoints, and a 24-question final; exam time is additional. The capstone dossier is self-assessed separately from the automatic exam.",
            "parts": [
                {"id": str(i), "title": t, "description": d} for i, (t, d) in enumerate(parts, 1)
            ],
            "references": [
                {"title": t, "url": u} for t, u in [PIT, PIPE, MISSING, SPLIT, METRIC, SAVE]
            ],
            "resources": [
                {
                    "title": "Download the full stock-ML lifecycle project",
                    "url": "/course-assets/stock-ml/stock-ml-lab.zip",
                },
                {
                    "title": "Download the 12-hour study and project guide",
                    "url": "/course-assets/stock-ml/README.md",
                },
                {
                    "title": "Download the stock-ML Python source",
                    "url": "/course-assets/stock-ml/stock_ml_lab.py",
                },
                {
                    "title": "Download the pinned ML dependencies",
                    "url": "/course-assets/stock-ml/requirements.txt",
                },
            ],
        },
        checkpoints_for(modules, parts, 5),
    )
    track["exams"][-1]["version"] = 1
    return track
