"""Verified case anchors with original, explicitly illustrative lesson applications.

Shared context is stored once per course; every lesson has a hand-authored application.
Rebuilds fail on missing/duplicate lessons rather than silently inventing a generic case.
"""

from copy import deepcopy


def case(case_id, title, kind, setting, period, context, source_title, url, scope):
    return {
        "id": case_id, "title": title, "kind": kind, "setting": setting,
        "period": period, "context": context,
        "references": [{"title": source_title, "url": url, "scope": scope}],
        "boundary": (
            "The historical context is sourced. Exercises and worked explanations are original; sample numbers and records are illustrative unless the task explicitly asks you to use the cited release."
            if kind == "documented" else
            "This is an original implementation exercise based on the cited documentation. The sample system, data, and results are illustrative; no claim is made that the named organization runs this exact system."
            if kind == "implementation" else
            "This is a fictional but realistic everyday scenario. All people, businesses, amounts, and outcomes in the exercise are illustrative. References explain the underlying method."
        ),
    }


CASES = {item["id"]: item for item in [
    case("household", "A household separates next month's bills from long-term savings", "illustrative", "Indonesia · everyday finances", "Original scenario",
         "Rani receives a monthly salary in rupiah, helps with family expenses, and saves for a goal several years away. A market decline is inconvenient for her long-term savings, but could be immediately harmful if rent money is invested in the same risky assets.",
         "Investor.gov · Asset allocation and diversification", "https://www.investor.gov/introduction-investing/getting-started/asset-allocation", "Time horizon, risk tolerance, and the purpose of asset allocation."),
    case("warung", "A neighborhood shop needs cash even when sales are growing", "illustrative", "Indonesia · small business", "Original scenario",
         "A fictional neighborhood grocery sells both for cash and on credit, buys inventory before holidays, and replaces refrigerators when they wear out. Looking only at sales would hide unpaid customer invoices, supplier obligations, and the cash needed to keep trading.",
         "U.S. SEC · Beginners' guide to financial statements", "https://www.sec.gov/about/reports-publications/investorpubsbegfinstmtguide", "The relationships between balance sheets, income statements, and operating/investing/financing cash flows."),
    case("bca_split", "BCA's 2021 five-for-one stock split", "documented", "Indonesia · listed shares", "October 2021",
         "BCA announced a 1:5 split and a schedule for trading its shares at the adjusted price in October 2021. A split changes the number of shares and the quoted price per share; it does not by itself multiply an investor's ownership value.",
         "BCA · Saham BBCA segera diperdagangkan dengan harga baru", "https://www.bca.co.id/id/tentang-bca/media-riset/pressroom/siaran-pers/2021/10/07/09/52/saham-bbca-segera-diperdagangkan-dengan-harga-baru", "The issuer's announced split ratio and implementation schedule; sample prices below are invented."),
    case("bi_rate", "Bank Indonesia's April 2024 rate decision", "documented", "Indonesia · rates, rupiah, and business costs", "23–24 April 2024",
         "Bank Indonesia raised BI-Rate by 25 basis points to 6.25% at its April 2024 meeting, linking the decision to rupiah stability and inflation risks. The release is a dated policy observation, not today's interest rate or proof that every Indonesian business benefits or suffers equally.",
         "Bank Indonesia · BI-Rate increased 25 bps to 6.25%, April 2024", "https://www.bi.go.id/en/publikasi/ruang-media/news-release/Pages/sp_268024.aspx", "The historical decision, its date, and the central bank's stated rationale."),
    case("bps_growth", "Reading Indonesia's 2024 GDP release without mixing growth measures", "documented", "Indonesia · economic news", "Release: 5 February 2025",
         "BPS reported 5.03% growth for Indonesia's economy in 2024, 5.02% year-on-year growth for the fourth quarter, and 0.53% quarter-on-quarter growth. These are different comparisons in the same release. The publication date also differs from the period being measured.",
         "BPS · Indonesia's 2024 economic growth release", "https://www.bps.go.id/id/pressrelease/2025/02/05/2408/economic-growth.html", "Published growth measures, comparison periods, and release date."),
    case("ojk_scam", "An investment pitch that left students with loan obligations", "documented", "Indonesia · student and family finances", "OJK release: 19 December 2022",
         "OJK described an investment-disguised fraud involving IPB students who took loans from legal financing platforms and used the proceeds for online-store transactions linked to the alleged scheme. A legitimate lender did not make the separate investment pitch legitimate or remove the borrowers' obligations.",
         "OJK · Education and consumer protection in the IPB investment-fraud case", "https://ojk.go.id/id/berita-dan-kegiatan/siaran-pers/Pages/OJK-Tingkatkan-Edukasi-dan-Perlindungan-Konsumen-dalam-Kasus-Penipuan-Berkedok-Investasi-di-IPB.aspx", "OJK's account of the scheme and its distinction between financing platforms and the investment pitch."),
    case("ge_disclosure", "GE's 2020 settlement and the importance of disclosure notes", "documented", "United States · company reporting", "9 December 2020",
         "GE disclosed a $200 million SEC settlement concerning disclosures about its Power business and run-off insurance operations. Its filing also describes changes to disclosure and internal-control processes. An analyst has to read the notes and the scope of the issue, rather than treating a headline earnings figure as a complete explanation.",
         "General Electric · Form 8-K, 9 December 2020", "https://www.sec.gov/Archives/edgar/data/40545/000004054520000062/ge-20201209.htm", "GE's own settlement announcement and description of the affected reporting areas."),
    case("svb", "Silicon Valley Bank: assets, funding, and a liquidity clock", "documented", "United States · banking risk", "March 2023; review published April 2023",
         "The Federal Reserve's review of SVB identified concentrated funding, interest-rate exposure, and weak liquidity-risk management. Depositor withdrawals accelerated before the bank closed on 10 March 2023. Assets that appear adequate on a balance sheet can still fail to provide cash quickly enough under stress.",
         "Federal Reserve · SVB review: key takeaways", "https://www.federalreserve.gov/publications/2023-April-SVB-Key-Takeaways.htm", "Supervisory findings on concentration, interest-rate risk, liquidity, and the March 2023 failure."),
    case("gme", "GameStop in January 2021: a price, a story, and market plumbing", "documented", "United States · retail market activity", "January 2021; SEC report October 2021",
         "The SEC's staff report describes unusually large price and volume moves in GameStop alongside short interest, social-media attention, and restrictions at some retail brokers. The episode offers several competing explanations to investigate; a striking price chart alone does not identify the cause of every trade.",
         "U.S. SEC · Equity and options market structure conditions in early 2021", "https://www.sec.gov/newsroom/press-releases/2021-212", "The reported market features and topics for further study; not a claim that one factor explains the entire episode."),
    case("flash_crash", "The May 2010 Flash Crash and disappearing execution capacity", "documented", "United States · market microstructure", "6 May 2010; joint report September 2010",
         "The CFTC and SEC examined the rapid market disruption on 6 May 2010, including trading across futures and equities, changing liquidity, and execution dynamics. This is a useful historical anchor for testing assumptions that an order will always find normal depth at the last observed price.",
         "CFTC and SEC · Findings regarding the market events of May 6, 2010", "https://www.cftc.gov/sites/default/files/idc/groups/public/%40otherif/documents/ifdocs/staff-findings050610.pdf", "Joint staff investigation of the event, especially the executive summary and liquidity discussion."),
    case("knight", "Knight Capital: a software release became an unwanted portfolio", "documented", "United States · trading operations", "1 August 2012; SEC order October 2013",
         "The SEC found that faulty deployment and inadequate controls allowed Knight Capital's router to send millions of erroneous orders on 1 August 2012. The firm accumulated unwanted positions and lost more than $460 million. Deployment verification, order-state checks, exposure limits, and incident response are part of a trading system's correctness.",
         "U.S. SEC · Knight Capital market-access rule settlement", "https://www.sec.gov/newsroom/press-releases/2013-222", "SEC findings on deployment, erroneous orders, risk controls, alerts, and losses."),
    case("ldi", "UK pension hedges and the 2022 gilt liquidity spiral", "documented", "United Kingdom · leveraged portfolio risk", "September–October 2022",
         "The Bank of England describes forced gilt selling by liability-driven investment funds and a temporary purchase facility during the 2022 market disruption. A portfolio designed around long-term liabilities can still require urgent cash when leveraged positions face collateral demands.",
         "Bank of England · Financial stability buy/sell tools: a gilt-market case study", "https://www.bankofengland.co.uk/quarterly-bulletin/2023/2023/financial-stability-buy-sell-tools-a-gilt-market-case-study", "The documented intervention, forced-sale dynamics, and liquidity objective."),
    case("negative_prices", "CME prepared test systems for negative energy prices", "documented", "Global · instrument-specific data contracts", "15 April 2020 advisory",
         "CME published test-environment guidance for zero or negative prices and strikes in certain NYMEX energy contracts. A validation rule that is correct for cash-equity prices is not automatically correct for every futures or spread instrument. Product definitions have to travel with the numbers.",
         "CME Group · Testing for negative prices and strikes in energy contracts", "https://www.cmegroup.com/notices/clearing/2020/04/Chadv20-160.html", "The dated testing advisory and supported message/file formats; this source is not used as a settlement-price dataset."),
    case("edgar", "Build a filing reader with an evidence trail", "implementation", "Global research using U.S. public filings", "Documented API workflow",
         "EDGAR exposes filing submissions and XBRL facts through SEC APIs. A useful research pipeline keeps the filing identifier, measurement period, units, and availability date with each extracted value. The implementation task is to preserve evidence when a later filing revises a number.",
         "U.S. SEC · EDGAR application programming interfaces", "https://www.sec.gov/search-filings/edgar-application-programming-interfaces", "Available submission/fact endpoints, filing metadata, and unit/period caveats."),
    case("alfred", "Recreate the economic data an analyst actually knew", "implementation", "Global · dated macroeconomic research", "Vintage-data workflow",
         "ALFRED stores historical vintages of economic observations. It lets a researcher distinguish the latest revised value from the value published at an earlier decision date. This is a practical model for keeping release history in an Indonesian or international macro research database.",
         "Federal Reserve Bank of St. Louis · ALFRED help", "https://alfred.stlouisfed.org/help", "Vintage observations, release dates, and the purpose of preserving earlier data versions."),
    case("factors", "Audit a fund's performance against published factor definitions", "implementation", "Global · portfolio research", "Research-data workflow",
         "Kenneth French's factor documentation explains the construction of market, size, and value factors. A research desk can use the definitions to ask whether a fund's returns reflect common exposures or something left unexplained by the model. These U.S. research factors are not a substitute for an Indonesian market model.",
         "Kenneth R. French · Description of Fama/French factors", "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html", "Factor definitions and construction universe; the exercises do not assert a fund's actual alpha."),
    case("forecasting", "Maintain a forecast as new monthly observations arrive", "implementation", "Indonesia-inspired · demand and market forecasting", "Local research workflow",
         "A fictional distributor forecasts demand to plan inventory, while a research analyst uses similar time-series tools for market variables. The statsmodels forecasting examples show rolling or expanding updates and out-of-sample evaluation. A good fit to yesterday's data is only one input to an operational forecast.",
         "statsmodels contributors · Forecasting with state-space models", "https://www.statsmodels.org/stable/examples/notebooks/generated/statespace_forecasting.html", "Forecast generation, updates, and pseudo-out-of-sample evaluation."),
    case("causal", "Did a training program change small-business sales?", "illustrative", "Indonesia-inspired · program evaluation", "Original scenario",
         "A fictional district offers bookkeeping training to selected shop owners. Participating shops later report higher sales. The evaluator must separate the effect of training from selection, seasonal demand, and differences that already existed between shops.",
         "World Bank · Impact Evaluation in Practice, second edition", "https://www.worldbank.org/en/programs/sief-trust-fund/publication/impact-evaluation-in-practice", "Counterfactual reasoning and experimental/quasi-experimental evaluation methods; the district and results are fictional."),
    case("ml_pipeline", "A stock-ranking model that must survive next month's data", "implementation", "Global methods · local stock research", "Reproducible ML workflow",
         "A fictional research team ranks stocks using dated features. The scikit-learn common-pitfalls guide explains why preprocessing and feature selection must be learned on training data. The team must reproduce every transformation on later observations without borrowing information from the future.",
         "scikit-learn contributors · Common pitfalls and recommended practices", "https://scikit-learn.org/stable/common_pitfalls.html", "Data leakage, consistent preprocessing, and pipeline-based training/validation."),
    case("calibration", "A probability forecast must justify its decision threshold", "implementation", "Global methods · paper-trading decisions", "Probability-evaluation workflow",
         "A model can rank opportunities well while reporting unreliable probabilities. Calibration compares predicted probabilities with observed outcomes. In a paper-trading workflow, a decision also depends on losses, payoffs, and costs; a probability above one-half is not automatically enough.",
         "scikit-learn contributors · Probability calibration", "https://scikit-learn.org/stable/modules/calibration.html", "Calibration curves, reliability, and probability scoring concepts."),
    case("model_release", "A saved model has to reproduce its training-time behavior", "implementation", "Global · research-to-production handoff", "Model persistence workflow",
         "A model file is only part of a release. Preprocessing, feature order, dependency versions, and input assumptions also matter. Scikit-learn's persistence documentation explains environment compatibility and the risks of loading untrusted artifacts.",
         "scikit-learn contributors · Model persistence", "https://scikit-learn.org/stable/model_persistence.html", "Persistence options, trusted artifacts, and environment/version compatibility."),
    case("llm_evidence", "A filing assistant reads an instruction hidden inside a document", "implementation", "Global · AI-assisted investment research", "Original adversarial document exercise",
         "A fictional filing packet contains normal financial text and a sentence instructing an AI system to ignore its rules. OWASP describes how untrusted documents can become prompt-injection inputs. The research workflow should keep retrieved text as evidence and independently validate any proposed numeric claim or action.",
         "OWASP · LLM prompt injection prevention cheat sheet", "https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html", "Indirect injection, separation of instructions and data, and constrained tool access."),
    case("idempotency", "A lost acknowledgement must not create a second order", "implementation", "Global · reliable order and payment systems", "Distributed-systems pattern",
         "AWS's Builders' Library explains using caller-provided identifiers to make retries safe. The same design question appears when a paper broker accepts an order but its acknowledgement is lost: the caller needs to retry the original intent without silently creating another commitment.",
         "AWS Builders' Library · Making retries safe with idempotent APIs", "https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/", "Request identity, retries, and duplicate side effects; paper-broker examples are original."),
    case("overload", "A burst of market messages exceeds processing capacity", "implementation", "Global · data and trading operations", "Overload-control pattern",
         "Google's SRE book describes how overload can create queues and cascading failures. In the course's fictional market-data service, bursts of updates can make a technically connected feed too stale to trade from. The useful question is which work to admit, delay, coalesce, or reject.",
         "Google SRE · Handling overload", "https://sre.google/sre-book/handling-overload/", "Admission control, queueing, and overload behavior; no claim is made about Google's trading systems."),
    case("atomic_ledger", "Recover a paper account after power is lost halfway through a fill", "implementation", "Global · accounting and crash recovery", "Atomic-commit pattern",
         "SQLite documents how transactions are committed atomically despite interruption. A paper-trading ledger needs the same all-or-nothing property for cash, positions, and execution records. A correct price calculation cannot rescue an account whose two sides were persisted separately.",
         "SQLite contributors · Atomic commit in SQLite", "https://www.sqlite.org/atomiccommit.html", "Atomicity, journaling, and crash-recovery concepts."),
    case("c_safety", "A faster C backtest must still respect memory boundaries", "implementation", "Global · compiled research tools", "Local C17 development",
         "Clang's AddressSanitizer instruments programs to detect classes of memory errors. A research engine that reads past a price array or uses freed data can produce plausible but invalid output. Sanitizer fixtures and explicit input contracts belong beside numerical checks.",
         "LLVM/Clang · AddressSanitizer", "https://clang.llvm.org/docs/AddressSanitizer.html", "Detected memory-error classes and compiler/linker instrumentation; sanitizer success is not proof of all correctness."),
    case("vectorization", "Prove that a faster price loop computes the same thing", "implementation", "Global · CPU performance engineering", "Compiler-guided optimization",
         "LLVM documents loop and SLP vectorization, including opportunities and limits. An analyst optimizing a scan over prices should inspect compiler evidence and compare outputs before claiming an improvement. Data layout and dependencies can matter as much as the number of arithmetic operations.",
         "LLVM · Vectorizers", "https://llvm.org/docs/Vectorizers.html", "Loop/SLP vectorization, loop dependencies, and optimization diagnostics."),
    case("parallel", "Distribute independent research trials without losing identity", "implementation", "Global · parallel research", "OpenMP 5.2 reference",
         "OpenMP specifies parallel work sharing, data environments, scheduling, and reductions. A fictional parameter sweep uses these concepts to distribute independent experiments. Each trial still needs a stable identity, a reproducible input, and a deterministic collection rule.",
         "OpenMP Architecture Review Board · OpenMP 5.2 specification", "https://www.openmp.org/spec-html/5.2/openmp.html", "Parallel constructs, work sharing, synchronization, and reductions."),
    case("gpu", "A GPU kernel is fast, but the end-to-end job is slower", "implementation", "Global · accelerated research", "GPU batching workflow",
         "NVIDIA's CUDA best-practices guide emphasizes measurement and the cost of moving data. A small research batch can spend more time in transfer and setup than it saves in a kernel. A useful benchmark measures the complete workload and verifies the result.",
         "NVIDIA · CUDA C++ best practices guide", "https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/", "Host/device transfer, batching, memory access, and measurement practices."),
    case("bitcoin", "Follow a signed payment into a small native-coin ledger", "implementation", "Global · cryptographic payment systems", "Bitcoin paper: 2008",
         "Bitcoin's original paper combines digital signatures, hash-linked blocks, proof of work, and a mechanism for selecting a chain. A local teaching ledger can demonstrate those ingredients, while remaining far smaller and less secure than an operational cryptocurrency network.",
         "Satoshi Nakamoto · Bitcoin: A Peer-to-Peer Electronic Cash System", "https://bitcoin.org/bitcoin.pdf", "The proposed payment, hashing, proof-of-work, and verification mechanisms; the course ledger is an original toy implementation."),
    case("erc20", "Issue classroom credits with explicit supply and spending authority", "implementation", "Global · local token development", "ERC-20 interface",
         "ERC-20 defines a token interface for balances, transfers, and allowances. A local classroom-credit project makes the distinction between holding tokens and granting someone permission to spend them concrete. Implementing this interface alone does not establish safe governance or economic value.",
         "Ethereum Improvement Proposals · ERC-20 token standard", "https://eips.ethereum.org/EIPS/eip-20", "The token interface and transfer/approval behavior; classroom credits are fictional."),
    case("replay", "A valid signature should not authorize a payment on another chain", "implementation", "Global · transaction authorization", "EIP-155 replay protection",
         "EIP-155 adds a chain identifier to the signing scheme for legacy Ethereum transactions. The design illustrates why a signature must be bound to the intended domain, not merely checked for mathematical validity. A local exercise uses dummy keys and distinct test-chain identifiers.",
         "Ethereum Improvement Proposals · EIP-155 replay protection", "https://eips.ethereum.org/EIPS/eip-155", "Chain-bound legacy transaction signatures; this is not a complete guide to all current transaction formats."),
    case("uniswap", "A token swap changes the inventory of a liquidity pool", "implementation", "Global · decentralized exchange mechanics", "Uniswap v2 model",
         "Uniswap v2's documentation describes pools that hold reserves of two assets. A local pool exercise connects a swap quote to reserve changes and the inventory left with liquidity providers. A displayed spot ratio is not the executable price for an arbitrarily large trade.",
         "Uniswap · v2 pools and reserves", "https://docs.uniswap.org/contracts/v2/concepts/core-concepts/pools", "Pool reserves and the constant-product model; use the version named here rather than assuming all AMMs work identically."),
    case("oracle", "A lending contract receives a price, but is it usable?", "implementation", "Global · smart-contract data boundaries", "Price-feed integration pattern",
         "Chainlink's feed-selection documentation describes different data-feed risk profiles and integration considerations. In a fictional collateral system, a numeric price is insufficient unless its timestamp, units, asset identity, and operational assumptions also pass checks.",
         "Chainlink · Selecting quality data feeds", "https://docs.chain.link/data-feeds/selecting-data-feeds", "Feed selection and risk considerations; the lending contract and thresholds are teaching assumptions."),
    case("reporting", "Hand a strategy report to someone who did not build the strategy", "implementation", "Global · investment reporting", "GIPS reporting principles as a reference",
         "The GIPS standards emphasize fair representation and full disclosure of investment performance. A course report can borrow that discipline by naming its benchmark, cash-flow treatment, costs, sample, and limitations. Completing this exercise does not establish GIPS compliance or verification.",
         "CFA Institute · GIPS standards for firms", "https://www.gipsstandards.org/standards/gips-standards-for-firms/", "Performance-presentation and disclosure principles, not certification of the learner's report."),
]}


def attach_real_world_cases(catalog):
    from case_applications_investing import APPLICATIONS as investing
    from case_applications_quant import APPLICATIONS as quant
    from case_applications_systems import APPLICATIONS as systems
    from case_applications_evaluation import APPLICATIONS as evaluation
    from case_applications_ethics import APPLICATIONS as ethics

    rows = investing + quant + systems + evaluation + ethics
    applications = {}
    for lesson_id, case_id, connection, task, walkthrough in rows:
        if lesson_id in applications:
            raise ValueError(f"Duplicate real-world application: {lesson_id}")
        if case_id not in CASES:
            raise ValueError(f"Unknown case: {case_id}")
        if not all(isinstance(text, str) and text.strip() for text in (connection, task, walkthrough)):
            raise ValueError(f"Incomplete real-world application: {lesson_id}")
        applications[lesson_id] = {
            "caseId": case_id, "connection": connection, "task": task,
            "walkthrough": walkthrough,
        }
    lesson_ids = {m["id"] for c in catalog for m in c["modules"]}
    if set(applications) != lesson_ids:
        raise ValueError(f"Real-world coverage mismatch: missing {lesson_ids - applications.keys()}, extra {applications.keys() - lesson_ids}")
    for course in catalog:
        case_ids = list(dict.fromkeys(applications[m["id"]]["caseId"] for m in course["modules"]))
        course["caseStudies"] = [deepcopy(CASES[key]) for key in case_ids]
        for module in course["modules"]:
            application = deepcopy(applications[module["id"]])
            module["realWorld"] = application
            for ref in CASES[application["caseId"]]["references"]:
                for item in (module, course):
                    if not any(old["url"] == ref["url"] for old in item["references"]):
                        item["references"].append({"title": ref["title"], "url": ref["url"]})
