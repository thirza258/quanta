"""Strategy lab workshop: a hands-on course for every tool on the /lab page.

The Strategy lab is an interactive quantitative research laboratory designed to test trading rules,
valuation models, factor regressions, execution guards, and liquidity pools under controlled,
reproducible assumptions. Default market data is synthetically generated from stochastic models.
"""

from applied_courses import checkpoints_for, study
from book_courses import finish

# Every URL below was verified: HTTP 200 and primary source documentation.
PBO = (
    "Bailey, Borwein, López de Prado & Zhu · The probability of backtest overfitting",
    "https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf",
)
DSR = (
    "Bailey & López de Prado · The deflated Sharpe ratio",
    "https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf",
)
HLZ = (
    "Harvey, Liu & Zhu · …and the cross-section of expected returns",
    "https://www.nber.org/papers/w20592",
)
TURING = (
    "The Turing Way community · Guide for reproducible research",
    "https://book.the-turing-way.org/reproducible-research/reproducible-research/",
)
PLOS = (
    "Sandve, Nekrutenko, Taylor & Hovig · Ten simple rules for reproducible computational research",
    "https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285",
)
NUMPY_RANDOM = (
    "NumPy · Random sampling and seeds",
    "https://numpy.org/doc/stable/reference/random/index.html",
)
STYLIZED = (
    "Chakraborti, Toke, Patriarca & Abergel · Econophysics: empirical facts and agent-based models",
    "https://arxiv.org/abs/0909.1974",
)
FLASH = (
    "CFTC and SEC · Findings regarding the market events of May 6, 2010",
    "https://www.cftc.gov/sites/default/files/idc/groups/public/%40otherif/documents/ifdocs/staff-findings050610.pdf",
)
PY_FLOW = (
    "Python Software Foundation · More control flow tools",
    "https://docs.python.org/3/tutorial/controlflow.html",
)
PY_MATH = (
    "Python Software Foundation · The math module",
    "https://docs.python.org/3/library/math.html",
)
NUMPY_WHERE = (
    "NumPy · numpy.where reference",
    "https://numpy.org/doc/stable/reference/generated/numpy.where.html",
)

IG_ORDERS = (
    "Investor.gov · Investor Bulletin: Understanding Order Types",
    "https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-14",
)
IG_STOCKS = (
    "U.S. SEC · Investor.gov: stocks and ownership",
    "https://www.investor.gov/introduction-investing/investing-basics/investment-products/stocks",
)
SEC_STATEMENTS = (
    "U.S. SEC · Beginners' guide to financial statements",
    "https://www.sec.gov/about/reports-publications/investorpubsbegfinstmtguide",
)
KNIGHT_SEC = (
    "U.S. SEC · Knight Capital market-access rule settlement",
    "https://www.sec.gov/newsroom/press-releases/2013-222",
)
FRENCH = (
    "Kenneth R. French · Data Library and factor methodology",
    "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html",
)
STATSMODELS_HAC = (
    "statsmodels developers · Robust covariance for OLS results, including HAC",
    "https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLSResults.get_robustcov_results.html",
)
UNISWAP = (
    "Uniswap Labs · How Uniswap works",
    "https://developers.uniswap.org/docs/get-started/concepts/how-uniswap-works",
)
ANGERIS = (
    "Angeris & Chitra · Improved price oracles: constant function market makers",
    "https://arxiv.org/abs/2003.10001",
)

LAB_TOOLS = {
    "market": "Market sandbox",
    "valuation": "Valuation",
    "factors": "Factor studio",
    "broker": "Paper trading",
    "amm": "AMM simulator",
}


def text(value):
    """Join hard-wrapped source lines into paragraphs separated by one blank line."""
    return "\n\n".join(" ".join(part.split()) for part in value.strip().split("\n\n"))


def practise(tool, task):
    """The shared closing section of every lesson."""
    return text(
        f"""### Practise in the lab

        Open the [{LAB_TOOLS[tool]}](/lab?tool={tool}) and {task} The worksheet on this page is an interactive arithmetic verification aid: it remains strictly in cash and does not execute your trading strategy, so you should record all substantive findings and performance figures directly from the lab itself.

        Because the lab's default market data is synthetically generated from stochastic models, a profitable run demonstrates that your execution logic and risk parameters function properly under those specific assumptions—it is never empirical evidence of a tradable real-market edge. Complete your session by documenting what you modified, the empirical outputs you observed, and the next falsification test you plan to run in [My notebook](/notebook)."""
    )


COURSE_GUIDE = (
    "Learn to use every tool on the Strategy lab page, from synthetic-market simulation and vector Python backtests to fundamental valuation, factor regressions, paper trading, liquidity pools, and reproducible scientific research trails.",
    "The Strategy lab is a dedicated quantitative research bench engineered to test trading ideas under controlled, reproducible conditions—not an account to chase paper profits. In real markets, noise, survivorship bias, and complex feedback loops make it easy to mistake luck for skill. The Strategy lab removes those ambiguities by giving you total control over the data-generating process: you define the stochastic process, set the drift and volatility, choose the market regime, and observe exactly how your strategy responds.\n\n"
    "This workshop takes you step-by-step through every instrument, control, and analytical workflow on the platform across three structured units:\n"
    "• Unit 1 (The market sandbox: stochastic simulation & signal execution): Tour the five lab tools, generate synthetic price series using Geometric Brownian Motion, Merton Jump-Diffusion, Heston Stochastic Volatility, and Markov Regime Switching, write clean vector strategies in the guided Python runtime, and trace how signals become executed fills with slippage, commissions, and buy-and-hold benchmarking.\n"
    "• Unit 2 (Read evidence & value businesses: analytics, fundamental valuation & factor econometric models): Interpret all 14 performance metrics and decode the high-win-rate paradox, value balance sheets using Benjamin Graham's net current asset value (NCAV) with liquidation recovery haircuts, estimate multi-factor risk exposures using Newey-West HAC robust standard errors against known ground truth, and run rigorous multi-seed robustness sweeps across historical stress scenarios.\n"
    "• Unit 3 (Execution guards, DeFi automated market makers & scientific research governance): Test orders against paper-broker pre-trade safety guards and automated circuit breakers, calculate constant-product swap execution, price impact, and concentrated impermanent loss in an AMM liquidity pool, manage saved experiment states and historical data imports, and execute an end-to-end 12-step capstone research loop from pre-registered hypothesis to exported audit trails.\n\n"
    "Every lesson takes 30 minutes: read the underlying mechanics, work through the concrete step-by-step arithmetic, run the experiment in the lab, and record what you discovered in My Notebook. Default data is synthetic, so every result is a teaching device: a strong backtest is a reason to test harder, never evidence of a real-market edge.",
)

APPLICATIONS = [
    (
        "14.1",
        "causal",
        "A research loop starts from a question that could come out either way, the same discipline an evaluator needs before crediting a training programme with higher sales.",
        "A fictional learner opens the lab and writes 'trend following works'. Rewrite it as a claim the sandbox could contradict, naming the rule, the comparison, the metric and the number of seeds (illustrative).",
        "A usable version reads like 'close above the 50-day average has a shallower maximum drawdown than buy and hold on at least four of five seeds, with default costs'. It fixes a comparison and a threshold before any run, so a result can reject it. 'Works' can never be wrong, which is why it teaches nothing.",
    ),
    (
        "14.2",
        "ldi",
        "A stress scenario changes the market a rule faces, much as the 2022 gilt spiral changed what leveraged pension hedges had to survive.",
        "Run the default trend rule on seed 42 under 'Custom market' and under 'Liquidity crisis · 2008-inspired'. In the lab's engine the maximum drawdown moves from −27.1% to −38.8%. Explain what the scenario changed and what it cannot tell you.",
        "The scenario switches to Heston stochastic volatility with an 18% annual decline and 55% volatility, so the same rule meets a harsher path. It shows how the rule behaves under the stress the scenario assumes. It does not reproduce 2008, and a rule that survives one generated crisis has not been shown to survive a real one.",
    ),
    (
        "14.3",
        "alfred",
        "A threshold computed from the whole history uses values nobody had at the time, the error a vintage database exists to prevent.",
        "A fictional rule buys whenever the close is within 10% of the highest close in the sample (illustrative). Explain which bars the threshold depends on and how a vintage-style view of the data would change it.",
        "The highest close of the whole sample may come years after the bar being judged, so early decisions borrow later prices. A vintage view would use only the highest close observed up to each bar, a running maximum, which the guided runtime cannot build from its whole-series operations. The safe choice is to drop the rule rather than trust its backtest.",
    ),
    (
        "14.4",
        "flash_crash",
        "The lab fills every order at the next open, an assumption that holds on quiet days and fails on days like 6 May 2010, when execution capacity disappeared.",
        "A fictional long position's signal turns off at a close of 100.00 and the next open gaps down to 92.00 (illustrative). Compute the sale price with 3 bps of slippage and say what the backtest assumes that a stressed market might not provide.",
        "The sale fills at 92.00 × 0.9997 ≈ 91.97, so the account loses the gap whatever the rule says, because a signal cannot act before the next open. The backtest also assumes the whole position trades at one price for a fixed 3 bps. On 6 May 2010 liquidity vanished, so real fills could have been far worse or impossible, a risk a fixed-slippage backtest cannot show.",
    ),
    (
        "14.5",
        "reporting",
        "A reader who did not run the experiment needs each metric's definition and context before any single number can be compared.",
        "A fictional teammate reports only 'win rate 76.7%' for the Mean reversion chip on the lab's default seed 42. List the other facts they must add before the number means anything.",
        "They should add total return (−2.37% on that run), the number of closed trades, profit factor, maximum drawdown, the buy-and-hold comparison, and the seed, costs and horizon. A high win rate beside a negative total return means the losing trades were larger, which the win rate alone hides.",
    ),
    (
        "14.6",
        "svb",
        "Assets that look adequate on a balance sheet can recover less cash than expected under pressure, which is what the valuation tool's recovery sliders test.",
        "Using the tool's defaults ($40m cash, $60m receivables at 85%, $80m inventory, $70m liabilities, 10m shares, price $6), find the inventory recovery rate at which adjusted NCAV per share equals the price.",
        "Adjusted NCAV is (40 + 0.85 × 60 + r × 80 − 70) ÷ 10. Setting it to 6 gives 21 + 80r = 60, so r = 48.75%. Below that recovery the margin of safety turns negative, so the case rests on the inventory fetching at least about half its book value in a sale.",
    ),
    (
        "14.7",
        "factors",
        "A factor regression separates returns explained by known exposures from what is left over, the same question an audit of a fund against published factors asks.",
        "In the factor studio's default fit, the daily alpha estimate is 0.000586 with a p-value of 0.124, while the planted alpha is 0.0001. Explain what a reviewer should conclude about 'skill'.",
        "The estimate annualizes to roughly 15%, but its p-value says the data cannot distinguish it from zero, and the planted value is far smaller. A reviewer should report the exposures, which are measured precisely, and treat the alpha as unproven. Real fund audits face the same problem with fewer, noisier observations.",
    ),
    (
        "14.8",
        "parallel",
        "Treating each seed as a separately identified trial keeps a robustness study honest, just as independent research jobs must keep their identity when distributed.",
        "The default trend rule on seeds 42–46 returns −23.4%, +4.9%, +19.6%, +2.3% and −5.8%, against buy-and-hold returns of −18.5%, +5.1%, +88.4%, +30.7% and +0.4% (lab engine, default settings). Summarize the evidence in three sentences.",
        "The rule averages about −0.5% with a seed-to-seed standard deviation near 16 points and trails buy and hold on all five seeds, though its drawdown is shallower on four of them. Reporting only seed 44's +19.6% would hide that. Each run needs its seed recorded so anyone can rerun exactly that trial.",
    ),
    (
        "14.9",
        "oracle",
        "A price is usable only while it is fresh, the same check a lending contract should apply before acting on an oracle feed.",
        "In the paper broker, a fictional order arrives with a reference price that is 90 seconds old and a spread of 40 bps (illustrative). State which guard decides and what the audit log shows.",
        "Guards run in a fixed order, and staleness is checked before the spread, so the order is rejected with 'Price data is stale.' because the price is older than 60 seconds. The 40 bps spread would have passed its 100 bps guard. A system should refuse to trade on a stale price even when everything else looks normal.",
    ),
    (
        "14.10",
        "uniswap",
        "Every swap changes a pool's inventory and therefore its price, which is why the simulator reports execution price and impact separately from spot.",
        "Quote a 0.1 ETH swap in the default 10 ETH / 20,000 USDC pool with a 0.3% fee and compare its price impact with the default 1 ETH swap.",
        "0.1 ETH returns 20,000 × 0.0997 ÷ 10.0997 ≈ 197.43 USDC, an execution price near 1,974.32 and impact of about 1.28%. One ETH returns about 1,813.22 USDC, an impact of 9.34%. Impact grows faster than size because each unit sold moves the pool's price further.",
    ),
    (
        "14.11",
        "model_release",
        "A saved experiment, like a saved model, is useful only if reopening it reproduces the result it was saved with.",
        "A fictional learner saves an experiment, edits its code without saving again, and reopens the experiment the next day (illustrative). Explain which code appears and how to get back to the saved version.",
        "The lab keeps an unsaved draft under the experiment's id, and a draft wins over the saved code when the experiment reopens, so the edited code appears. The editor's Restore lesson code icon resets it to the experiment's saved code. Rerunning and comparing CAGR with the experiment card confirms which version is running.",
    ),
    (
        "14.12",
        "ml_pipeline",
        "Keeping untouched seeds for the end mirrors a stock model that must prove itself on next month's data rather than on the data it was tuned on.",
        "A fictional learner tunes the moving-average window on seeds 42–46 and then tests the chosen window once on seeds 47–51 (illustrative). Explain why the second set matters and what to report if the two sets disagree.",
        "The development seeds shaped the choice, so their results are optimistic by construction. The reserved seeds played no part in choosing, so they give a fairer reading. If the sets disagree, report both and treat the tuned result as unconfirmed rather than retuning on the reserved seeds.",
    ),
]


def build_lab_workshop():
    modules = []

    def add(
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
        tool,
        practice,
        reading,
    ):
        index = len(modules) + 1
        rows = []
        for offset, (prompt, correct, wrong1, wrong2, explanation) in enumerate(questions):
            options = [correct, wrong1, wrong2]
            shift = (index + offset) % 3
            options = options[shift:] + options[:shift]
            rows.append((prompt, options, options.index(correct), explanation))
        item = study(
            f"14.{index}",
            (index - 1) // 4 + 1,
            title,
            objective,
            principle,
            case,
            workflow + "\n\n" + practise(tool, practice),
            formula,
            code,
            task,
            solution,
            rows,
            refs,
        )
        item["minutes"] = 30
        item["reading"] = reading
        modules.append(item)
    # ------------------------------------------------------------------ 14.1
    add(
        "A tour of the lab and the research loop",
        "Navigate the five tools on the Strategy lab page, execute the baseline experiment, and apply the four-stage scientific research loop to interpret performance results objectively.",
        text(
            r"""The Strategy lab is an interactive quantitative research workbench designed to test trading hypotheses under controlled, reproducible conditions—not an account to chase paper profits. In live markets, noise, survivorship bias, and complex feedback loops make it easy to mistake luck for skill. The Strategy lab removes those ambiguities by giving you total control over the data-generating process: you define the stochastic process, set the drift and volatility, choose the market regime, and observe exactly how your strategy responds.

            The laboratory organizes five specialized tools within a unified environment:
            1. **Market sandbox**: Formulate quantitative trading rules in Python, execute backtests against stochastic asset price series, and inspect performance metrics.
            2. **Valuation**: Perform fundamental balance-sheet analysis using Benjamin Graham's net current asset value (NCAV) model with liquidation recovery haircuts.
            3. **Factor studio**: Estimate multi-factor cross-sectional asset pricing regressions (CAPM, Fama–French, Carhart) with Newey–West HAC robust standard errors against known ground truth.
            4. **Paper trading**: Route individual orders to a deterministic mock broker equipped with pre-trade risk controls, liquidity participation limits, and circuit breakers.
            5. **AMM simulator**: Model decentralized automated market makers governed by the constant-product invariant $x \cdot y = k$, evaluating slippage, price impact, and concentrated impermanent loss.

            Two companion facilities preserve your quantitative work: **Saved experiments** stores reproducible parameter records, while **My notebook** maintains your hypotheses and observational notes.

            Every investigation in the lab follows a four-stage scientific research loop:
            1. **State a falsifiable hypothesis**: Define a specific, disprovable claim and pre-register the exact criteria that would reject it before running any code.
            2. **Perturb exactly one assumption**: Change a single parameter (such as random seed, volatility, or transaction friction) while holding all other variables constant to isolate causality.
            3. **Read the multidimensional evidence**: Evaluate the complete array of metrics (drawdown, CAGR, trade counts, risk-adjusted returns) rather than cherry-picking a single favorable number.
            4. **Maintain an auditable research trail**: Log every trial—including failed variants—so that another researcher can replicate your findings exactly."""
        ),
        text(
            r"""To anchor this methodology, consider the default baseline experiment in the Market sandbox. The synthetic market generates a 3-year Geometric Brownian Motion (GBM) price trajectory with an annualized drift of $\mu = +8\%$ and annualized volatility of $\sigma = 20\%$ using pseudorandom seed 42. Trading starts with $E_0 = \$100{,}000$ in cash, facing an institutional commission of $5\text{ bps}$ ($0.0005$) and execution slippage of $3\text{ bps}$ ($0.0003$) per fill.

            Although the underlying market drift is positive, the specific path generated by seed 42 happens to experience prolonged downturns, beginning at $100.00$ and closing at approximately $81.70$.

            When we deploy the default 50-day moving average trend-following rule (`close > sma_50`), the backtest finishes with final equity of approximately $\$76{,}598.46$, translating to a total return of:
            $$R_{\text{rule}} = \frac{E_{\text{final}}}{E_0} - 1 = \frac{\$76{,}598.46}{\$100{,}000.00} - 1 \approx -23.40\%$$
            Across the 756 bars, the strategy executes 59 fills and experiences a maximum peak-to-trough drawdown of $\text{MDD}_{\text{rule}} \approx -27.07\%$.

            Now compare this performance against the passive **Buy & hold** benchmark. Buying at the initial open and remaining fully invested results in final equity of $\$81{,}536.23$, or a total return of:
            $$R_{\text{hold}} = \frac{\$81{,}536.23}{\$100{,}000.00} - 1 \approx -18.46\%$$
            However, holding the asset throughout the entire decline inflicts a severe maximum drawdown of $\text{MDD}_{\text{hold}} \approx -34.18\%$.

            Calculating the comparative spreads reveals the nuanced trade-offs of trend following:
            $$\Delta R = R_{\text{rule}} - R_{\text{hold}} = -23.40\% - (-18.46\%) = -4.94\text{ percentage points}$$
            $$\Delta \text{MDD} = \text{MDD}_{\text{rule}} - \text{MDD}_{\text{hold}} = -27.07\% - (-34.18\%) = +7.11\text{ percentage points shallower}$$

            The empirical evidence from this single path is mixed: the trend rule succeeded in protecting capital against catastrophic drawdown (cushioning the portfolio by 7.1 percentage points), but lagged on net return by 4.9 percentage points due to whipsaw trading costs. A single path cannot prove or disprove an edge—which is precisely why the subsequent stages of the research loop test multiple seeds, costs, and stress regimes."""
        ),
        text(
            r"""**Open the Strategy lab.** Click **Strategy lab** in the main navigation sidebar. The top header states "Ideas become clearer when you test them." Beneath the header, five navigation tabs provide immediate access to the platform tools: **Market sandbox**, **Valuation**, **Factor studio**, **Paper trading**, and **AMM simulator**. Notice how the URL dynamically updates to `/lab?tool=market`, `/lab?tool=valuation`, and so on. Switching tabs rebuilds the active tool view: while your Python strategy code is safely autosaved in browser local storage as a draft, active slider settings and computed outputs are cleared. Always record critical numbers before navigating away.

            **Inspect the default trend rule.** Select the **Market sandbox** tab and open the **strategy.py** editor pane. The default implementation contains a single vectorized signal expression: `return data["close"] > data["sma_50"]`. If previous work left a modified draft, open the **Parameters** tab and click the **Trend following** quick-strategy chip, or click the **Restore lesson code** icon above the editor.

            **Execute the baseline backtest.** Click **Run experiment**, or press `Ctrl+Enter` (`Cmd+Enter` on macOS) with the cursor inside the code editor. Under **EXPERIMENT OUTPUT**, inspect the four primary metric cards: CAGR ($\approx -8.5\%$), SHARPE ($\approx -0.92$), MAX DRAWDOWN ($\approx -27.1\%$), and WIN RATE ($\approx 17.2\%$). Expand **All metrics** to review secondary statistics including total return ($-0.2340$), profit factor ($0.32$), and total fills ($59$). Switch to the **Console** tab to read the engine's execution log: "756 bars · 59 fills · final equity $76,598.46".

            **Benchmark against Buy & Hold.** Open **Parameters**, select the **Buy & hold** quick-strategy chip, and click **Run experiment**. In **All metrics**, verify that total return reads approximately $-0.1846$ and maximum drawdown reaches $-34.18\%$. Because the chip enters on the second bar following its initial signal, it tracks the dashed benchmark curve on the **Equity curve** chart almost identically. Return to the **Trend following** chip to restore the baseline rule.

            **Formulate a falsifiable hypothesis.** Beside the sandbox, the panel **THE RESEARCH LOOP** articulates the four scientific steps. In your laboratory notebook, write down a single falsifiable statement that this experiment can test—for example: "A 50-day moving average trend filter produces a shallower maximum drawdown than buy-and-hold across at least 4 out of 5 synthetic market paths under standard transaction costs."

            **Explore the lesson worksheet.** Every lesson includes an interactive code template under **Try the lesson template**. Click **Run in sandbox** followed by **Run experiment**. The **Console** prints the exact numerical verification of our equations, while the performance cards display zero return and undefined Sharpe because the verification script deliberately remains in cash."""
        ),
        r"R = \frac{E_{\text{final}}}{E_0} - 1, \qquad \Delta R = R_{\text{rule}} - R_{\text{hold}}, \qquad \Delta \text{MDD} = \text{MDD}_{\text{rule}} - \text{MDD}_{\text{hold}}",
        '''
capital = 100000.0
rule_final = 76598.46
hold_final = 81536.23
rule_return = rule_final / capital - 1.0
hold_return = hold_final / capital - 1.0
print("Rule total return:", round(rule_return, 4))
print("Buy and hold total return:", round(hold_return, 4))
gap = (rule_return - hold_return) * 100.0
print("Return gap in percentage points:", round(gap, 2))
rule_drawdown = -0.2707
hold_drawdown = -0.3418
shallower = (rule_drawdown - hold_drawdown) * 100.0
print("Drawdown advantage in percentage points:", round(shallower, 2))
print("Shallower drawdown on this path:", rule_drawdown > hold_drawdown)
fills = 59
closed_trades = fills // 2
print("Total fills:", fills, "Closed round-trip trades:", closed_trades)
''',
        "Draft a formal quantitative research note for the baseline experiment: state one falsifiable hypothesis concerning the 50-day trend rule, identify the single parameter you will perturb next, record the four card metrics alongside the Buy & Hold drawdown and return, and specify an empirical outcome that would force you to reject the hypothesis.",
        "A rigorous research note articulates an unambiguous, testable proposition: for instance, that a 50-day simple moving average trend filter reduces maximum drawdown relative to buy-and-hold across synthetic GBM paths. It records baseline metrics (CAGR ~ -8.5%, Sharpe ~ -0.92, Max Drawdown ~ -27.1%, Win Rate ~ 17.2%, Buy & Hold return ~ -18.5%, and Buy & Hold drawdown ~ -34.2%). It selects the random seed as the first variable to vary, holding drift, volatility, and friction constant. Crucially, it pre-registers a rejection threshold: if the rule fails to reduce drawdown on at least 4 of 5 independent seeds, the hypothesis must be discarded. Finally, it acknowledges that simulated results on synthetic data cannot demonstrate an edge in live markets.",
        [
            (
                "A learner changes the Market sandbox settings, opens the Valuation tab and then returns to the Market sandbox tab. What has happened to the sandbox?",
                "Its results and market settings are reset, and only the code draft is kept",
                "Everything is kept until the browser is closed",
                "Only the market settings are kept; the code is reset",
                "Each lab tool is rebuilt when you switch tabs. Code is autosaved as a draft in browser local storage, but simulation results and slider settings are not persisted across tab switches, so record numbers before you leave a tab.",
            ),
            (
                "Why can the lab promise that the same settings and the same seed give identical bars?",
                "The default market is generated by a seeded random process rather than downloaded",
                "The lab caches a copy of real prices for every seed",
                "The server stores your earlier bars and replays them",
                "A seeded pseudorandom number generator draws the exact same sequence of numbers each time, ensuring the simulated bars are 100% reproducible by construction. No real prices stand behind the default market data.",
            ),
            (
                "Which sequence matches the lab's research loop?",
                "State a hypothesis, change one assumption, read the evidence, keep a research trail",
                "Run many variations, keep the best curve, save it, then write the hypothesis",
                "Pick a seed that shows a profit, change every setting at once, discard weaker runs",
                "The hypothesis comes first so the experiment can genuinely disprove it. Changing exactly one assumption at a time isolates causality, and maintaining an honest research trail documents failures alongside successes.",
            ),
            (
                "On the default run the trend rule returns about −23% with a drawdown near −27%, while the Buy & hold chip returns about −18% with a drawdown near −34%. What is the fairest reading?",
                "Mixed evidence from one synthetic path, so more tests are needed",
                "The rule is proven to work because its drawdown is smaller",
                "The rule is proven useless because its return is lower",
                "One seed represents a single random path. The drawdown mitigation claim holds on this path while the return claim does not; neither constitutes a definitive verdict until seeds, costs, and stress scenarios are systematically tested.",
            ),
        ],
        [PBO, TURING],
        "market",
        "repeat the default run, write one disprovable hypothesis about the trend rule in your notebook, and record the four card values and the Buy & hold drawdown.",
        "30-minute session: 8 minutes reading the laboratory architecture, 10 minutes working through the baseline return and drawdown calculations, and 12 minutes verifying the outputs in the Market sandbox; remember that default data is synthetic and every result is an educational model rather than evidence of a market edge.",
    )

    # ------------------------------------------------------------------ 14.2
    add(
        "Generate a market: processes, scenarios and seeds",
        "Configure stochastic processes, stress scenarios, horizons, and random seeds, predict their impact on generated price paths, and understand why a single seed represents only one realization of a distribution.",
        text(
            r"""The Market sandbox does not download historical stock quotes; it synthesizes price paths from parametric stochastic differential equations. This design offers a profound scientific advantage: real historical datasets are plagued by survivorship bias, regime shifts, and non-stationarity, whereas synthetic data allows you to test hypotheses against known mathematical properties.

            The generator models asset prices starting at a base value of $P_0 = 100.00$ on 2 January 2020, progressing across standard trading years comprising 252 business days. The platform provides four distinct stochastic processes:
            1. **Geometric Brownian Motion (GBM)**: Generates log-normal continuous returns with constant drift $\mu$ and volatility $\sigma$. While widely used in derivatives pricing, pure GBM assumes independent and identically distributed returns, omitting real-world fat tails.
            2. **Merton Jump-Diffusion**: Superimposes discrete compound Poisson jump processes onto continuous Brownian motion. Jumps arrive randomly at an annual frequency $\lambda$, drawing jump magnitudes from a normal distribution to model unexpected macro shocks and earnings surprises.
            3. **Heston Stochastic Volatility**: Allows instantaneous variance $v_t$ to wander as a mean-reverting Cox–Ingersoll–Ross (CIR) square-root diffusion process. It models mean reversion speed $\kappa$, long-run variance $\theta$, volatility of variance $\xi$, and return-volatility correlation $\rho$ (capturing the leverage effect and volatility clustering).
            4. **Markov Regime Switching**: Transitions dynamically between three hidden economic regimes—calm bull market, flat consolidation, and high-volatility crisis—using an empirical transition matrix.

            A pseudorandom seed fixes the sequence of random variates drawn by the engine. Two runs configured with identical parameters and the same seed will produce bit-for-bit identical price series, enabling clean experimental control. However, a single seed yields only one realized path out of an infinite distribution.

            The lab also provides named stress scenarios (such as Deflationary crash · 1929-inspired, Stagflation · 1970s-inspired, and Liquidity crisis · 2008-inspired). These scenarios override the stochastic process, drift, and volatility parameters to subject strategies to extreme market environments, while the Crypto flash crash scenario inserts a sudden $-50\%$ single-day shock into the active process."""
        ),
        text(
            r"""To understand why a single seed does not represent a guaranteed outcome, examine the default baseline: Geometric Brownian Motion, annual drift $\mu = +8\%$ ($0.08$), annual volatility $\sigma = 20\%$ ($0.20$), horizon $T = 3\text{ years}$ ($756\text{ bars}$), and seed 42.

            Under continuous GBM, the daily log return $r_t$ is governed by:
            $$r_t = \left(\frac{\mu - \frac{1}{2}\sigma^2}{252}\right) + \frac{\sigma}{\sqrt{252}} \, z_t, \qquad P_t = P_{t-1} \exp(r_t)$$
            where $z_t \sim \mathcal{N}(0, 1)$ is a standard normal random draw.

            Over the full 3-year investment horizon ($T = 3$), the expected cumulative log return is:
            $$\mathbb{E}[\ln(P_T / P_0)] = \left(\mu - \frac{1}{2}\sigma^2\right) \times T = \left(0.08 - \frac{0.04}{2}\right) \times 3 = 0.06 \times 3 = 0.1800$$
            The median terminal price implied by this expected growth is:
            $$P_{\text{median}} = P_0 \exp(0.1800) = 100.00 \times 1.1972 \approx \$119.72$$

            However, the standard deviation of this 3-year log return is:
            $$\text{SD} = \sigma \sqrt{T} = 0.20 \times \sqrt{3} \approx 0.3464$$

            On seed 42, the realized closing price at bar 756 finishes at $P_{756} \approx 81.70$. The actual realized log return is:
            $$\ln(P_{756} / P_0) = \ln(81.70 / 100.00) = \ln(0.8170) \approx -0.2021$$

            Measuring how far this outcome lands from the mathematical expectation in standardized units:
            $$z = \frac{\text{Realized} - \text{Expected}}{\text{SD}} = \frac{-0.2021 - 0.1800}{0.3464} = \frac{-0.3821}{0.3464} \approx -1.103$$

            In a standard normal distribution, a $z$-score of $-1.10$ corresponds to a cumulative probability of $\Phi(-1.10) \approx 13.5\%$. This means roughly one in every seven random paths will end at or below $81.70$. Seed 42 is not a software defect—it is simply a draw from the lower quartile of a distribution with positive drift. Annual drift defines the theoretical mean of the ensemble, never a guarantee for an individual trajectory."""
        ),
        text(
            r"""**Insert code diagnostic probes.** In the **Market sandbox**, open **strategy.py**. Above the `return` statement, add three print statements indented four spaces:
            `print("Bars:", len(data["close"]))`
            `print("First open:", round(data["open"][0], 2))`
            `print("Last close:", round(data["close"][-1], 2))`
            These inspection lines read the generated price series without altering strategy signals.

            **Execute the baseline run.** Click **Run experiment**. The **Console** opens automatically to display stdout: "Bars: 756", "First open: 100.09", and "Last close: 81.7". (Python prints 81.70 as 81.7).

            **Evaluate alternate stochastic processes.** Open the **Parameters** tab. In the **Stochastic process** dropdown, select **Merton jump-diffusion**. Notice the **Jumps per year** slider appears, defaulted to 1. Run the experiment: the terminal price shifts to approximately $104.93$. Now drag **Jumps per year** to 0 and re-run: with jump intensity set to zero, Merton collapses back to pure GBM, returning the terminal price to $81.7$. Next, select **Heston stochastic volatility** to reveal parameters for $\kappa$ (mean reversion speed), $\theta$ (long-run variance), $\xi$ (volatility of variance), and $\rho$ (correlation). Execute the run: the terminal close settles near $92.78$. Finally, select **Markov regime switching**: observe that the drift and volatility sliders become inactive because regime dynamics govern state transitions; the terminal close lands near $55.61$.

            **Adjust the time horizon.** Restore the process to Geometric Brownian Motion and open the **Horizon** dropdown (options range from 1 year to 30 years). Select **1 year** and click **Run experiment**. The engine generates exactly 252 bars with a terminal close near $91.07$. Under GBM, the 1-year run consists of the exact first 252 bars of the 3-year run—a crucial property we will exploit to audit for look-ahead bias.

            **Subject the model to stress scenarios.** In the **SCENARIO** dropdown above the editor, select **Crypto flash crash · −50%** and execute. Switch to the **Market** chart tab: around mid-June 2021 (bar 378), the price cuts in half in a single bar, driving final equity down to approximately $40.85$. The flash crash preserves your chosen stochastic process and injects a single shock. By contrast, historical scenarios (such as 1929 Deflationary Crash or 2008 Liquidity Crisis) override process, drift, and volatility completely while leaving your slider displays intact.

            **Perturb the random seed.** Click the gear icon (**Execution settings**) in the sandbox header and change **Seed** from 42 to 7. Execute: the terminal close changes to approximately $45.54$. Test seeds 1 and 3 (yielding closes near $68.85$ and $195.65$ respectively). Finally, set the seed back to 42: the exact original values (First open 100.09, Last close 81.7) return with complete fidelity."""
        ),
        r"r_t = \frac{\mu - \frac{1}{2}\sigma^2}{252} + \frac{\sigma}{\sqrt{252}}\,z_t, \qquad P_t = P_{t-1} e^{r_t}, \qquad z = \frac{\ln(P_T / P_0) - (\mu - \frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}",
        '''
from math import sqrt, log, exp

years = 3
mu = 0.08
sigma = 0.20
bars = years * 252
print("Total bars generated:", bars)
expected_log_growth = (mu - 0.5 * sigma * sigma) * years
spread = sigma * sqrt(years)
print("Expected 3-year log return:", round(expected_log_growth, 4))
print("Standard deviation of 3-year log return:", round(spread, 4))
first_price = 100.0
last_close = 81.70
actual_log_return = log(last_close / first_price)
print("Seed 42 realized log return:", round(actual_log_return, 4))
z_score = (actual_log_return - expected_log_growth) / spread
print("Standardized z-score deviation:", round(z_score, 2))
print("Theoretical median price:", round(first_price * exp(expected_log_growth), 2))
print("Realized price return on Seed 42:", round((last_close / first_price - 1.0) * 100.0, 2), "%")
''',
        "Record the terminal closing price for Geometric Brownian Motion, Merton jump-diffusion, Heston stochastic volatility, and Markov regime switching on seed 42, followed by GBM on seeds 1, 2, and 3. Explain which price variations originate from process mechanics versus seed draws, and why positive drift did not prevent seed 42 from losing value.",
        "On seed 42, expected terminal closes settle near 81.7 (GBM), 104.93 (Merton jump-diffusion), 92.78 (Heston stochastic volatility), and 55.61 (Markov regime switching). Across seeds for pure GBM, terminal closes finish near 68.85 (seed 1), 78.88 (seed 2), and 195.65 (seed 3). Variations between stochastic processes using the same seed stem from their mathematical equations (such as jump arrivals or volatility clustering), whereas variations between seeds holding the process fixed stem from random sampling variance. The +8% drift shifts the distribution's mean, but diffusion volatility creates wide dispersion: seed 42 falls approximately 1.10 standard deviations below expectation, an event occurring in roughly 13.5% of paths.",
        [
            (
                "Why does the seed-42 market end near 81.70 when the Annual drift slider says +8%?",
                "Drift is an average over many random paths, and seed 42 is one path that happens to end low",
                "The lab subtracts commission from prices while it generates them",
                "Seed 42 secretly switches the process to a bear regime",
                "An annual drift of +8% shifts the expected log return, but individual paths experience substantial diffusion volatility. A final price ending roughly 1.1 standard deviations below expectation occurs in about 13.5% of paths (1 in 7).",
            ),
            (
                "Which pair of settings guarantees that two runs produce identical bars?",
                "The same market settings and the same Seed",
                "The same strategy code and the same keyboard shortcut",
                "The same commission and slippage values",
                "The market data generation depends exclusively on the stochastic process, scenario, drift, volatility, horizon, and seed. Strategy code, execution costs, and keyboard shortcuts act on the bars after they are created.",
            ),
            (
                "A learner selects Markov regime switching and then drags the Annual drift slider from 8% to 20%. What happens to the generated bars?",
                "Nothing changes: regime switching uses its own three regimes and ignores the drift and volatility sliders",
                "Every regime's drift rises by 12 percentage points",
                "The market switches back to geometric Brownian motion",
                "The Markov regime switching engine uses internal parameters for its three hidden states (bull, flat, crisis) and ignores the global annual drift and volatility sliders, which apply only to GBM, Merton, and Heston.",
            ),
            (
                "What does the Crypto flash crash · −50% scenario do to the generated market?",
                "It keeps the selected process and settings and adds a one-day −50% shock at the middle bar",
                "It replaces the bars with real crypto prices from a past crash",
                "It cuts every daily return in half",
                "The flash-crash scenario preserves your chosen underlying stochastic process and slider parameters, inserting a single 1-day −50% price drop at the middle bar (bar 378 of 756) to test sudden liquidity shocks.",
            ),
        ],
        [NUMPY_RANDOM, STYLIZED, FLASH],
        "market",
        "run the probe on seed 42 for each process, then on seeds 1, 2 and 3 for GBM, and write the six last closes next to the one change that produced each.",
        "30-minute session: 8 minutes reading how the lab synthesizes market bars, 10 minutes reproducing the seed-42 log-normal return arithmetic, and 12 minutes testing stochastic processes and seeds in the Market sandbox; all default data is synthetic.",
    )

    # ------------------------------------------------------------------ 14.3
    add(
        "Write a strategy in the guided Python runtime",
        "Implement long-or-cash trading strategies as strategy(data), construct boolean signals using vector series operations, and navigate the execution constraints and look-ahead hazards of the guided runtime.",
        text(
            r"""Trading strategies in the Market sandbox are implemented as a single top-level Python function: `strategy(data)`. The engine passes an immutable dictionary containing complete time series arrays: `data["open"]`, `data["high"]`, `data["low"]`, `data["close"]`, `data["volume"]`, `data["returns"]`, `data["sma_50"]`, and `data["sma_200"]`.

            The function must return a binary long-or-cash signal: either a boolean array (or 1/0 integer series) matching the length of the dataset, or a single scalar boolean that applies uniformly across all bars. Continuous weights, fractional portfolio allocations, and short positions are deliberately unsupported and will cause the runtime to reject the execution with an explicit error.

            The guided runtime is an isolated Python Abstract Syntax Tree (AST) interpreter engineered for rapid execution and deterministic safety. It supports basic assignments, function definitions with positional arguments, conditional branching (`if`/`else`), bounded `for` loops over ranges or lists, standard arithmetic, comparisons, f-strings, and a curated subset of mathematical and NumPy functions.

            Because the runtime prohibits mutable list manipulation (such as `list.append()`, in-place slice assignment, or list concatenation), trading signals must be constructed using vectorized series operations. You compare series using relational operators (`>`, `<`), combine them with bitwise operators (`&`, `|`, `~`), and wrap every comparison in parentheses. Parentheses are strictly necessary because in Python, bitwise operators bind with higher precedence than relational operators.

            The guided environment enforces strict resource boundaries:
            - **Wall-clock timeout**: 2.0 seconds maximum execution duration.
            - **Opcode budget**: 750,000 operations maximum.
            - **Source code size**: 20,000 characters maximum.
            - **Output buffer**: 20 KB maximum stdout capture.

            Finally, be alert to look-ahead bias. The function receives the entire historical series at once. While the backtesting engine automatically delays signal execution by one bar, it cannot inspect your mathematical expressions. If your code references global summary statistics—such as `max(data["close"])` or an unshifted moving average—it will silently leak future information into past trading decisions."""
        ),
        text(
            r"""To observe how signal construction shapes trade frequency and costs, compare four variations of a trend strategy on the default seed 42 market:

            1. **Baseline trend filter**: `data["close"] > data["sma_50"]`
               Executes 59 fills and produces a total return of $R \approx -23.40\%$.
            2. **NumPy vector representation**: `np.where(data["close"] > data["sma_50"], 1, 0)`
               Produces identical results (59 fills, $R \approx -23.40\%$), confirming semantic equivalence.
            3. **Trend filter with 200-day regime confirmation**: `(data["close"] > data["sma_50"]) & (data["sma_50"] > data["sma_200"])`
               Restricts entry to regimes where the 50-day average exceeds the 200-day average. Fills drop from 59 down to 24, and total return improves to $R \approx -9.10\%$.
            4. **Trend filter with 2% hysteresis buffer**: `data["close"] > data["sma_50"] * 1.02`
               Requires the closing price to clear the moving average by at least 2% before triggering a long signal, reducing whipsaws. Fills drop to 56, and return settles near $R \approx -22.40\%$.

            Why does trading less frequently improve net returns? Every executed trade incurs transaction friction: $5\text{ bps}$ commission plus $3\text{ bps}$ slippage, totaling $8\text{ bps}$ ($0.0008$) per fill.
            On an average position notional of $\$88{,}616$, the friction cost per fill is:
            $$\text{Friction per fill} = \$88{,}616 \times 0.0008 \approx \$70.89$$

            Calculating total trading costs across variations:
            $$\text{Cost of 59 fills} = 59 \times \$70.89 \approx \$4{,}182.51$$
            $$\text{Cost of 24 fills} = 24 \times \$70.89 \approx \$1{,}701.36$$

            The dual-moving-average rule saves approximately $\$2{,}481$ in execution fees alone. However, lower transaction drag does not prove algorithmic skill: on a single synthetic path, fewer trades can appear superior simply through random timing luck."""
        ),
        text(
            r"""**Open the code editor.** In the **Market sandbox**, select the **strategy.py** editor pane. The baseline strategy contains: `return data["close"] > data["sma_50"]`. If modified code is present, click the **Trend following** chip under **Parameters** to restore the default.

            **Inspect active signal counts.** Above the `return` line, insert:
            `print("Bars above average:", sum(data["close"] > data["sma_50"]))`
            Click **Run experiment**. The **Console** prints approximately 309 bars (representing 40.9% of the 756 bars in the sample). Summing a boolean series counts True instances, demonstrating that the strategy holds equity positions roughly two-fifths of the time.

            **Implement vector logic with NumPy.** Insert `import numpy as np` at the top of the script and update the return statement:
            `return np.where(data["close"] > data["sma_50"], 1, 0)`
            Run the experiment. Verify that the output cards and Console match the baseline run exactly: CAGR $-8.5\%$, Sharpe $-0.92$, Max Drawdown $-27.1\%$, Win Rate $17.2\%$, and 59 fills. Identical metrics confirm that the vectorized NumPy syntax matches pure Python series comparisons.

            **Add a secondary trend condition.** Modify the return statement to:
            `return (data["close"] > data["sma_50"]) & (data["sma_50"] > data["sma_200"])`
            Retain the parentheses around each sub-expression. Execute the run: total fills decline to 24, and total return improves to approximately $-9.1\%$.
            Now remove the parentheses: `return data["close"] > data["sma_50"] & data["sma_50"] > data["sma_200"]`. Execute: the run aborts with an alert: "SandboxError: Use separate comparisons joined with & for series." In Python, `&` evaluates before `>`, creating an invalid expression. Similarly, replacing `&` with the logical keyword `and` fails with: "Use & and | for series comparisons."

            **Add a percentage buffer.** Test a 2% entry threshold:
            `return data["close"] > data["sma_50"] * 1.02`
            Execute: fills drop slightly to 56, and total return improves to approximately $-22.4\%$.

            **Test sandbox guardrails.** Deliberately trigger runtime protections to understand error handling:
            1. Unauthorized import: `import pandas as pd` triggers "Imports are limited to math and the guided numpy subset."
            2. Infinite loop: `while True: pass` triggers "While is not supported. Use bounded for loops and documented functions."
            3. Unsupported continuous weights: `return data["close"] * 0 + 0.5` triggers "Only long/cash signals (True/False or 1/0) are supported."
            Restore the working trend rule using the **Trend following** chip.

            **Identify look-ahead bias.** Review this problematic expression: `return data["close"] > max(data["close"]) * 0.9`. The sandbox executes this code without error because `max()` is an allowed built-in. However, the calculation finds the highest closing price across the entire 3-year history, leaking future peaks into past signals. Lesson 14.4 establishes a multi-horizon audit to detect this bias."""
        ),
        r"s_t = \begin{cases} 1 & C_t > \overline{C}_{t,n} \\ 0 & \text{otherwise} \end{cases}, \qquad \overline{C}_{t,n} = \frac{1}{n} \sum_{j=0}^{n-1} C_{t-j}, \qquad \text{Cost} = N_{\text{fills}} \times \text{Notional} \times (c + s)",
        '''
close = [100.0, 101.0, 99.0, 102.0, 104.0, 103.0, 105.0, 101.0]
window = 3
signal_count = 0
fills = 0
holding = 0

for i in range(len(close)):
    start = max(0, i - window + 1)
    total = sum(close[j] for j in range(start, i + 1))
    average = total / (i + 1 - start)
    signal = 1 if close[i] > average else 0
    signal_count += signal
    if signal != holding:
        fills += 1
        holding = signal

print("Bars with active long signal:", signal_count)
print("Signal state changes (executed fills):", fills)
friction_bps = 5 + 3
notional = 88616.0
per_fill = notional * (friction_bps / 10000.0)
print("Friction cost per fill at 8 bps:", round(per_fill, 2))
print("Estimated friction for 59 fills:", round(59 * per_fill, 2))
print("Estimated friction for 24 fills:", round(24 * per_fill, 2))
print("Transaction cost savings from fewer fills:", round((59 - 24) * per_fill, 2))
''',
        "Implement the default trend rule two additional ways in the Market sandbox: first using np.where, and second incorporating an additional moving average condition or percentage buffer. Record the fill count and total return for each variation, explain why the np.where implementation must match the baseline exactly, and explain why reduced transaction costs do not prove trading skill.",
        "The baseline trend rule produces 59 fills and a total return of approximately -23.40%. The np.where implementation produces bit-for-bit identical results (59 fills, -23.40%) because it encodes the identical boolean conditional logic into binary array form. Adding a 200-day trend filter reduces fills to 24 and improves total return to -9.10%, while a 2% buffer reduces fills to 56 with a return of -22.40%. At 8 bps of total friction on an average $88,616 notional, each fill costs ~$70.89, meaning 59 fills consume ~$4,183 in fees compared to ~$1,701 for 24 fills. While reducing trade frequency trims execution drag by ~$2,482, this performance difference on a single synthetic path reflects cost mechanics and sample variance rather than proven investment skill.",
        [
            (
                "Which return value does strategy(data) accept?",
                "A single True, or one True/False (or 1/0) value for each bar",
                "A target weight such as 0.5 for each bar",
                "A signed position of −1, 0 or 1 for each bar",
                "The Strategy lab evaluates binary long-or-cash strategies only. Continuous weights, fractional portfolio allocations, and short positions are rejected with an explicit SandboxError.",
            ),
            (
                "A learner writes data[\"close\"] > data[\"sma_50\"] & data[\"sma_50\"] > data[\"sma_200\"] and the run fails. What is the fix?",
                "Put each comparison in brackets and join them with &",
                "Replace & with the word and",
                "Wrap the whole expression in a for loop",
                "In Python, the bitwise operator & has higher precedence than comparison operators like >. Without parentheses, data[\"sma_50\"] & data[\"sma_50\"] evaluates first, causing a chained comparison syntax error.",
            ),
            (
                "Why can a signal list not be built bar by bar inside a loop in the guided runtime?",
                "There is no append, list concatenation or element assignment, so signals come from whole-series operations",
                "Loops are disabled entirely",
                "Loops are allowed only after the first 200 bars",
                "The guided sandbox allows bounded for loops for scalar calculations, but disables mutable list modifications (append, extend, item assignment). Vector operations like boolean series comparisons and np.where must be used.",
            ),
            (
                "A rule sets its threshold at 0.9 × max(data[\"close\"]). Why is that a look-ahead problem even though the engine delays signals by one bar?",
                "The maximum is computed over the whole history, including bars after the one being judged",
                "The engine fills at the previous close instead of the next open",
                "The runtime does not support max()",
                "Evaluating max(data[\"close\"]) computes the scalar peak of the entire dataset, allowing decisions on early historical bars to borrow knowledge of price peaks that occurred months or years in the future.",
            ),
        ],
        [PY_FLOW, PY_MATH, NUMPY_WHERE],
        "market",
        "rewrite the default rule two more ways, one with np.where and one with an extra condition, and record the fill count and total return of each.",
        "30-minute session: 8 minutes studying runtime syntax and security guardrails, 10 minutes reproducing the vectorized signal and friction cost arithmetic, and 12 minutes writing rules in the Market sandbox; remember that backtest profits on synthetic data never prove real-market alpha.",
    )

    # ------------------------------------------------------------------ 14.4
    add(
        "Backtest mechanics: signals, fills, costs and buy-and-hold",
        "Trace the execution pipeline from bar-close signals to next-open fills, calculate full round-trip friction, evaluate performance against the buy-and-hold benchmark, and conduct a multi-horizon look-ahead audit.",
        text(
            r"""A quantitative backtest transforms discrete mathematical signals into simulated portfolio equity through strict chronological execution rules. The Market sandbox enforces a deterministic 1-bar execution delay: a signal calculated using data available at the close of Bar $t$ executes at the opening price of Bar $t+1$. This delay mirrors institutional reality, where market participants cannot act upon a closing price until that closing auction has concluded.

            The account operates on a long-or-cash basis, deploying 100% of available cash into fractional shares upon a buy signal. The execution model accounts for bid-ask friction and brokerage costs:
            - **Buy Fill Price**: $P_t^{\text{buy}} = O_t (1 + s)$, where $O_t$ is the opening price and $s$ is slippage (default $3\text{ bps} = 0.0003$). Commission $c$ (default $5\text{ bps} = 0.0005$) is charged on the total purchase value, determining share quantity:
              $$q = \frac{\text{Cash}}{P_t^{\text{buy}} (1 + c)}$$
            - **Sale Fill Price**: $P_{t'}^{\text{sell}} = O_{t'} (1 - s)$. Commission is deducted from gross proceeds:
              $$\text{Net Proceeds} = q \cdot P_{t'}^{\text{sell}} (1 - c)$$

            Every realized trade recorded in the trade log reflects net proceeds after both transaction costs. If a position remains open at the conclusion of the backtest, it is marked to market at the final bar's close ($P_T^{\text{close}}$) to calculate ending equity, but is excluded from closed-trade statistics (such as Win Rate and Profit Factor).

            The reference benchmark—**Buy & hold**—executes a single purchase at the opening price of Bar 1, incurs entry friction once, and holds the position perpetually. This represents the ultimate hurdle for any active timing strategy: if a quantitative rule cannot outperform buy-and-hold net of transaction friction, its active trading is destroying capital."""
        ),
        text(
            r"""To trace order execution step by step, follow a complete round-trip trade starting with $E_0 = \$100{,}000$ cash, slippage $s = 3\text{ bps}$ ($0.0003$), and commission $c = 5\text{ bps}$ ($0.0005$).

            A buy signal triggers at the close of Bar $t$ where price is $100.00$. Bar $t+1$ opens at $O_{t+1} = 101.00$.
            The executed buy price after slippage is:
            $$P^{\text{buy}} = 101.00 \times (1 + 0.0003) = 101.00 \times 1.0003 = \$101.0303$$
            Accounting for the $5\text{ bps}$ commission, the total cash outlay per share is $101.0303 \times 1.0005 \approx \$101.0808$.
            The allocated share quantity is:
            $$q = \frac{\$100{,}000.00}{101.0303 \times 1.0005} = \frac{\$100{,}000.00}{101.080815} \approx 989.3074\text{ shares}$$

            Several bars later, an exit signal triggers. The subsequent bar opens at $O_{t'} = 104.00$.
            The executed sell price after slippage is:
            $$P^{\text{sell}} = 104.00 \times (1 - 0.0003) = 104.00 \times 0.9997 = \$103.9688$$
            Gross sale proceeds equal:
            $$\text{Gross Proceeds} = 989.3074 \times 103.9688 \approx \$102{,}857.06$$
            Deducting the $5\text{ bps}$ commission ($102{,}857.06 \times 0.0005 \approx \$51.43$):
            $$\text{Net Proceeds} = \$102{,}857.06 \times (1 - 0.0005) \approx \$102{,}805.63$$
            The net realized gain is:
            $$\text{Net Gain} = \frac{\$102{,}805.63 - \$100{,}000.00}{\$100{,}000.00} = +2.8056\% \approx +2.81\%$$
            Notice that while the raw asset price rose from $101.00 \to 104.00$ ($+2.9703\%$), execution slippage and commissions absorbed $16.5\text{ bps}$ of performance.

            Now consider the **Multi-Horizon Look-Ahead Audit**. Under Geometric Brownian Motion, running a 1-year backtest (252 bars) and a 3-year backtest (756 bars) using the same random seed (seed 42) produces the exact same first 252 price bars. Any causal, backwards-looking trading rule must therefore execute the exact same trades during that first year.
            When we test the valid 50-day trend rule, it executes exactly 28 trades during year one on both horizons.
            However, when we test the look-ahead rule (`close > 0.9 * max(close)`), it executes 22 trades during year one on the 1-year horizon, but only 10 trades during that identical period on the 3-year horizon. Adding future bars shifted the global historical maximum, altering past trading signals. Divergent trade executions on identical historical data are definitive mathematical proof of look-ahead bias."""
        ),
        text(
            r"""**Execute the baseline strategy.** In the **Market sandbox**, activate the **Trend following** chip and click **Run experiment**. The **Console** log confirms: "756 bars · 59 fills · final equity $76,598.46".

            **Audit an individual execution.** Open the **Trades** tab to inspect the chronological trade blotter, which lists Date, Side, Quantity, Price, Fee, and P&L. Select the very first BUY trade and record its Date and Price. Switch to the **Market** chart tab, locate the corresponding bar, and inspect its Open. Verify that the recorded execution price matches Open $\times (1 + 0.0003)$ to the penny.

            **Compare equity against the benchmark.** Open the **Equity curve** chart tab. The visualization plots active Strategy equity against the passive Buy & hold curve. Select the **Buy & hold** quick-strategy chip and execute: verify that the final equity in **All metrics** aligns with the terminal value of the dashed benchmark line.

            **Stress-test transaction friction.** Click the gear icon (**Execution settings**). Set both **Commission (bps)** and **Slippage (bps)** to 0. Restore the **Trend following** chip and execute: note that final equity rises from $\$76{,}598.46$ to $\$80{,}271.18$ ($R \approx -19.73\%$), while fill counts remain unchanged at 59. Next, set commission and slippage to $20\text{ bps}$ each: final equity plunges to $\$62{,}538.12$ ($R \approx -37.46\%$), while fills remain at 59. Frictional costs degrade returns without altering underlying signal states.

            **Conduct the multi-horizon look-ahead audit.** Set **Horizon** to **1 year** on the **Parameters** tab. In `strategy.py`, enter the look-ahead rule: `return data["close"] > max(data["close"]) * 0.9`. Execute the run and count the recorded trades on the **Trades** tab (22 trades). Now change **Horizon** to **3 years** and execute again: filter the **Trades** blotter to only include trades dated within the first calendar year (2020). Exactly 10 trades appear. The fact that adding future data in 2021 and 2022 altered trades executed in 2020 exposes look-ahead bias. Repeat this test with the baseline trend rule to confirm it executes identical trades across both horizons."""
        ),
        r"P^{\text{buy}}_t = O_t(1 + s), \quad q = \frac{\text{Cash}}{P^{\text{buy}}_t(1 + c)}, \qquad P^{\text{sell}}_{t'} = O_{t'}(1 - s), \quad \text{Proceeds} = q \cdot P^{\text{sell}}_{t'}(1 - c)",
        '''
cash = 100000.0
slippage = 3.0 / 10000.0
commission = 5.0 / 10000.0
open_buy = 101.00
buy_price = open_buy * (1.0 + slippage)
shares = cash / (buy_price * (1.0 + commission))
open_sell = 104.00
sell_price = open_sell * (1.0 - slippage)
gross_proceeds = shares * sell_price
net_proceeds = gross_proceeds * (1.0 - commission)
print("Executed buy price:", round(buy_price, 4), "Shares purchased:", round(shares, 4))
print("Executed sell price:", round(sell_price, 4), "Net proceeds:", round(net_proceeds, 2))
net_gain_pct = (net_proceeds / cash - 1.0) * 100.0
raw_price_pct = (open_sell / open_buy - 1.0) * 100.0
print("Net portfolio gain:", round(net_gain_pct, 2), "% vs raw price change:", round(raw_price_pct, 2), "%")
friction_drag_bps = (raw_price_pct - net_gain_pct) * 100.0
print("Friction drag in basis points:", round(friction_drag_bps, 1))
print("Look-ahead audit trade counts (1-yr vs 3-yr):", 22, "vs", 10)
''',
        "Execute the default trend rule across three friction settings: zero costs, default costs (5 bps commission, 3 bps slippage), and adverse costs (20 bps each). Record final equity and fill counts for all three. Then perform the multi-horizon look-ahead audit on both the trend rule and the max-based rule, reporting first-year trade counts and explaining the scientific implications.",
        "Across all three cost environments, total fills remain constant at 59 because transaction friction modifies cash balances without altering underlying indicator comparisons. On seed 42, zero friction yields final equity of ~$80,271 (-19.73%), default friction yields ~$76,598 (-23.40%), and adverse friction (20 bps each) yields ~$62,538 (-37.46%), demonstrating how transaction drag compounds over time. In the multi-horizon look-ahead audit, the causal 50-day trend rule executes exactly 28 trades during year one across both 1-year and 3-year runs. In contrast, the rule referencing max(data['close']) executes 22 trades on the 1-year run but only 10 trades during that same period on the 3-year run. When future data alters historical decisions, the backtest has leaked the future and is scientifically invalid.",
        [
            (
                "A trend rule's signal turns long at Monday's close. When does the lab buy?",
                "At Tuesday's open, adjusted for slippage",
                "At Monday's close, when the signal appears",
                "At Tuesday's close, after the day is complete",
                "A trading signal calculated upon the close of Bar t is executed at the open of Bar t+1. This 1-bar execution lag prevents impossible same-bar closing price execution.",
            ),
            (
                "With 3 bps of slippage, what does a buy at an open of 101.00 pay per share before commission?",
                "About 101.03, which is 101.00 × 1.0003",
                "Exactly 101.00, because slippage applies only to sales",
                "About 104.03, the next day's price",
                "Long purchases pay the opening price plus slippage: 101.00 × (1 + 0.0003) = 101.0303. Transaction commission is levied on top of this gross execution amount.",
            ),
            (
                "How does the lab treat a position that is still open when the backtest ends?",
                "It is marked to the last close and left out of win rate and profit factor",
                "It is sold at the last close and counted as a closed trade",
                "It is removed from the results entirely",
                "Unrealized open positions at the conclusion of a backtest are marked to market at the final bar's close for equity calculation, but only fully liquidated round-trip trades enter Win Rate and Profit Factor.",
            ),
            (
                "Run on 1 year and on 3 years with the same seed, a rule makes different trades inside the first year. What does that show?",
                "The rule uses information from later bars, because the first year's data is identical in both runs",
                "The seed was ignored by the second run",
                "Longer horizons always change early trades",
                "Because both runs share the exact same first 252 bars, any causal, backwards-looking trading rule must execute identical trades during year one. Divergent trades prove that future data leaked into past decisions.",
            ),
        ],
        [FLASH, PBO, IG_ORDERS],
        "market",
        "rerun the default rule with costs at 0, at the defaults and at 20 bps each, then run the one-year versus three-year look-ahead test on two rules and record what changes.",
        "30-minute session: 7 minutes studying backtest execution mechanics, 9 minutes working through the round-trip friction and fill arithmetic, and 14 minutes conducting multi-horizon look-ahead audits in the Market sandbox; simulated profits never guarantee a live trading edge.",
    )
    # ------------------------------------------------------------------ 14.5
    add(
        "Read the results: metrics, charts, monthly returns and the trade log",
        "Interpret all 14 quantitative performance metrics, analyze the four core summary cards, correlate visualizations with underlying trade blotters, and understand why high win rates can mask negative expectancy.",
        text(
            r"""Evaluating a quantitative backtest requires looking far beyond simple cumulative return. A trading strategy can generate an impressive final equity curve while carrying uncompensated tail risks, unbearable drawdown periods, or extreme vulnerability to transaction friction. The Strategy lab equips researchers with a rigorous 14-metric analytical suite to evaluate strategy risk, reward, and execution efficiency.

            Following a backtest run, the **EXPERIMENT OUTPUT** panel surfaces four primary performance cards:
            - **CAGR (Compound Annual Growth Rate)**: Compounds the total geometric return over the standard 252 trading bars per year:
              $$\text{CAGR} = (1 + R)^{252 / N} - 1$$
            - **SHARPE (Annualized Sharpe Ratio)**: Measures excess return per unit of total risk relative to a 3% annual risk-free hurdle ($r_f = 0.03$):
              $$\text{Sharpe} = \frac{\bar{r} - r_f}{s_r} \sqrt{252}$$
            - **MAX DRAWDOWN (MDD)**: Measures the maximum peak-to-trough percentage decline in portfolio equity:
              $$\text{MDD} = \min_{t} \left(\frac{E_t - \max_{\tau \le t} E_{\tau}}{\max_{\tau \le t} E_{\tau}}\right)$$
            - **WIN RATE**: Percentage of closed round-trip trades that achieved a positive net P&L after all commissions and slippage.

            Expanding **All metrics** reveals ten additional statistical indicators: total return, profit factor (gross winning dollar volume divided by gross losing dollar volume), total trade executions, final equity, capital asset pricing alpha and beta relative to buy-and-hold, Sortino ratio (dividing excess return by downside semi-deviation), Calmar ratio ($\text{CAGR} / |\text{MDD}|$), Value at Risk (VaR 95%), and Conditional Value at Risk (CVaR / Expected Shortfall 95%).

            The lab handles undefined metrics with scientific honesty. If a strategy remains 100% in cash, its daily return variance is zero; the Sharpe ratio denominator vanishes, so the interface displays an em-dash ("—") on cards and "Undefined" in tables rather than a misleading zero. Furthermore, if you modify any parameter slider or code expression after a run, the timestamp displays "· inputs changed" to warn you that visible outputs no longer reflect active controls."""
        ),
        text(
            r"""To master performance evaluation, examine the baseline 50-day trend run on seed 42 ($N = 756\text{ bars}$, 3 years).
            The strategy yields a cumulative return of $R = -23.40\%$.
            Calculating CAGR:
            $$\text{CAGR} = (1 - 0.2340)^{252 / 756} - 1 = (0.7660)^{1/3} - 1 \approx 0.91498 - 1 = -8.50\%$$
            The maximum peak-to-trough drawdown reached $\text{MDD} = -27.07\%$.
            The Calmar ratio scales annual growth by maximum drawdown:
            $$\text{Calmar} = \frac{\text{CAGR}}{|\text{MDD}|} = \frac{-0.0850}{|-0.2707|} = \frac{-0.0850}{0.2707} \approx -0.314$$
            The backtest recorded 59 fills: 30 buys and 29 sales, completing 29 full round-trip trades. A win rate of $17.24\%$ indicates that exactly 5 trades were profitable, while 24 were unprofitable. The profit factor of $0.32$ confirms that total dollar gains from those 5 winners amounted to only one-third of the losses incurred by the 24 losers.

            Now examine the **High-Win-Rate Paradox**. In the sandbox, select the **Mean reversion** quick-strategy chip on seed 42.
            The performance cards display a stunning **WIN RATE of 76.7%** (23 winners out of 30 closed trades).
            Yet the strategy's total return is $-2.37\%$ and its CAGR is $-0.80\%$!

            How can a strategy that wins three-quarters of its trades lose money overall?
            Mathematical expectancy depends on both probability and payoff magnitude:
            $$\mathbb{E}[\text{Trade}] = (p_{\text{win}} \times \overline{\text{Win}}) - (p_{\text{loss}} \times \overline{\text{Loss}})$$
            The mean-reversion rule captures dozens of tiny $0.3\%$ profits, but occasionally holds onto deteriorating positions that crash for $-4.5\%$ losses before closing. A high win rate is completely meaningless in isolation—it frequently masks an asymmetric distribution of small wins wiped out by catastrophic left-tail losses."""
        ),
        text(
            r"""**Inspect the primary metric cards.** Execute the **Trend following** baseline chip with default parameters. Read the four output cards: CAGR ($\approx -8.5\%$), SHARPE ($\approx -0.92$), MAX DRAWDOWN ($\approx -27.1\%$), and WIN RATE ($\approx 17.2\%$).

            **Audit comprehensive metrics in the drawer.** Click **All metrics** to expand the full statistical readout. Record the 14 reported metrics: Total return ($-0.2340$), CAGR ($-0.0850$), Sharpe ($-0.9200$), Sortino ($-1.1400$), Max drawdown ($-0.2707$), Calmar ($-0.3140$), Win rate ($0.1724$), Profit factor ($0.3200$), Total trades ($59.0000$), Final equity ($\$76{,}598.46$), Alpha ($-0.0750$), Beta ($0.4500$), VaR 95% ($-0.0185$), and CVaR 95% ($-0.0270$).

            **Verify mathematical relationships by hand.** Open the lesson worksheet. Confirm that your manual calculations of CAGR from total return ($756\text{ bars}$) and Calmar ratio from CAGR and maximum drawdown match the reported figures to the fourth decimal place.

            **Navigate performance visualizations.**
            - Switch to the **Drawdown** chart tab ("Drawdown from peak"): trace the underwater curve and identify the exact calendar date of the deepest valley ($-27.07\%$).
            - Open the **Returns** tab: inspect the monthly returns heatmap. Observe which calendar months suffered the steepest losses and which generated gains.
            - Open the **Trades** tab: filter the trade blotter by positive P&L to confirm that exactly 5 closed trades produced gains.

            **Expose the high-win-rate paradox.** Click **Parameters**, select the **Mean reversion** quick-strategy chip, and execute. Write down the 14 metrics alongside the trend rule. Observe the striking divergence: win rate surges to $76.7\%$, yet total return remains negative ($-2.37\%$).

            **Trigger the input staleness alert.** Move the **Annual volatility** slider from $20\%$ to $25\%$ without clicking Run. Observe the label "· inputs changed" appear beside the execution timestamp, indicating that the displayed equity curve belongs to the previous parameter state."""
        ),
        r"\text{CAGR} = (1 + R)^{\frac{252}{N}} - 1, \qquad \text{Sharpe} = \frac{\bar{r} - r_f}{s_r}\sqrt{252}, \qquad \text{Calmar} = \frac{\text{CAGR}}{|\text{MDD}|}",
        '''
total_return = -0.2340
bars = 756
cagr = (1.0 + total_return) ** (252.0 / bars) - 1.0
max_drawdown = -0.2707
calmar = cagr / abs(max_drawdown)
print("Computed CAGR:", round(cagr * 100.0, 2), "%")
print("Computed Calmar ratio:", round(calmar, 3))
closed_trades = 59 // 2
win_rate = 0.1724
winning_trades = round(win_rate * closed_trades)
losing_trades = closed_trades - winning_trades
print("Closed trades:", closed_trades, "Winning trades:", winning_trades, "Losing trades:", losing_trades)

# Mean reversion comparison
mr_win_rate = 0.7667
mr_closed_trades = 30
mr_winners = round(mr_win_rate * mr_closed_trades)
print("Mean reversion winning trades:", mr_winners, "of", mr_closed_trades, "yet total return is negative!")
''',
        "Execute both the Trend following and Mean reversion quick-strategy chips on seed 42 with default parameters. Record all 14 metrics side-by-side in your notebook, recompute CAGR and Calmar ratio by hand for one run, and explain why a high win rate does not guarantee investment profitability.",
        "On seed 42, the baseline trend rule produces total return -23.40%, CAGR -8.50%, max drawdown -27.07%, Sharpe -0.92, Calmar -0.314, win rate 17.24% (5 of 29 winners), and profit factor 0.32. The mean reversion rule produces total return -2.37%, CAGR -0.80%, max drawdown -14.20%, and a win rate of 76.67% (23 of 30 winners). Hand calculation confirms CAGR = (1 - 0.2340)^(1/3) - 1 = -8.50% and Calmar = -0.0850 / 0.2707 = -0.314. A strategy with a 76.7% win rate can lose money overall because mathematical expectancy reflects trade magnitude as well as frequency: if 23 winning trades average +$250 while 7 losing trades average -$1,100, net expectancy is negative. Comprehensive evaluation requires assessing return, drawdown, profit factor, and benchmark alpha together across multiple market seeds.",
        [
            (
                "The default run shows CAGR −8.5% and maximum drawdown −27.1%. What is its Calmar ratio?",
                "About −0.31, CAGR divided by the size of the drawdown",
                "About −3.19, the drawdown divided by CAGR",
                "−35.6%, the sum of the two",
                "Calmar = CAGR / |Max Drawdown| = -0.0852 / 0.2707 ≈ -0.315. It measures annual compound growth per unit of maximum drawdown risk.",
            ),
            (
                "A rule wins 76.7% of its trades yet loses 2.37% overall. How is that possible?",
                "Its few losing trades are larger than its many winning ones",
                "The win rate includes the open position at the end",
                "The metrics are computed before costs",
                "Win rate records frequency rather than dollar magnitude. A strategy that books dozens of tiny 0.2% profits but suffers rare catastrophic 5% stop-outs will have a high win rate alongside negative cumulative expectancy.",
            ),
            (
                "Why does an all-cash rule show '—' for Sharpe?",
                "Its daily returns have no variability, so the ratio's denominator is zero",
                "Sharpe is hidden whenever the data is synthetic",
                "Sharpe needs at least one losing trade to be computed",
                "The Sharpe ratio divides annualized excess return by the sample standard deviation of daily returns. For an all-cash portfolio, daily return variance is zero, resulting in a zero denominator; the lab displays an em-dash rather than an undefined or misleading number.",
            ),
            (
                "What does '· inputs changed' beside the run time tell you?",
                "A setting changed after the last run, so the output no longer matches the controls",
                "The lab rewrote your strategy code",
                "The market data was refreshed from a live feed",
                "The '· inputs changed' warning indicates that an active parameter, scenario, or seed was modified since the backtest was last executed. You must re-run the backtest before reading or saving metrics.",
            ),
        ],
        [DSR, HLZ, PBO],
        "market",
        "run the Trend following and Mean reversion chips on the same seed and compare all fourteen metrics side by side.",
        "30-minute session: 8 minutes reading performance metric definitions and expectancy formulas, 9 minutes recalculating CAGR and Calmar by hand, and 13 minutes analyzing the metric drawer, charts, and trade blotter in the Market sandbox; simulated results never establish live trading edge.",
    )

    # ------------------------------------------------------------------ 14.6
    add(
        "The valuation tool: net current assets, haircuts and Graham value",
        "Compute unadjusted and adjusted Net Current Asset Value (NCAV) per share, apply liquidation haircuts, test Benjamin Graham's two-thirds screen, and evaluate valuation sensitivity to recovery and growth assumptions.",
        text(
            r"""Quantitative research extends beyond price-series momentum to fundamental business valuation. The **Valuation** tool implements classic deep-value liquidation models pioneered by Benjamin Graham in *Security Analysis*. Graham's central insight was that an investor could establish an impregnable margin of safety by purchasing a company's common stock at a steep discount to its net liquid assets—treating property, plant, equipment (PP&E), and intangible goodwill as having zero residual value.

            The model computes **Unadjusted Net Current Asset Value (NCAV)** per share:
            $$\text{NCAV}_{\text{unadj}} = \frac{C + R + I - L}{N}$$
            where $C$ is cash and cash equivalents, $R$ is accounts receivable, $I$ is inventory, $L$ is total liabilities (short-term and long-term obligations), and $N$ is diluted common shares outstanding.

            Graham established a demanding investment rule known as the **two-thirds NCAV screen**: purchase shares only if the market price $P$ trades at or below two-thirds of unadjusted NCAV per share:
            $$P \le \frac{2}{3} \text{NCAV}_{\text{unadj}}$$

            However, unadjusted book values assume full liquidation recovery. In distressed bankruptcies or forced asset sales, customers dispute invoices and inventories sell for scrap. The tool models **Adjusted NCAV** by applying recovery rate haircuts:
            $$\text{NCAV}_{\text{adj}} = \frac{C + \rho_R R + \rho_I I - L}{N}$$
            where cash recovers $100\%$ ($1.0$), receivables recover at rate $\rho_R$ (default $85\% = 0.85$), and inventory recovers at rate $\rho_I$ (default $60\% = 0.60$).
            The fundamental **Margin of Safety (MoS)** is:
            $$\text{MoS} = 1 - \frac{P}{\text{NCAV}_{\text{adj}}}$$

            The tool also incorporates Graham's valuation heuristic for operating earnings:
            $$V_{\text{Graham}} = \frac{\text{EPS} \times (8.5 + 2g) \times 4.4}{Y}$$
            where $\text{EPS}$ is trailing earnings per share, $8.5$ represents the P/E of a no-growth company, $g$ is the expected multi-year earnings growth rate (in percent), $4.4$ represents the historical yield on AAA corporate bonds, and $Y$ is the prevailing corporate bond yield (in percent). While widely cited, this growth formula is highly speculative and serves as a sensitivity test rather than an asset-backed valuation."""
        ),
        text(
            r"""To evaluate balance sheet valuation mechanics, examine the default corporate balance sheet in the tool:
            Cash $C = \$40\text{m}$, Receivables $R = \$60\text{m}$, Inventory $I = \$80\text{m}$, Total Liabilities $L = \$70\text{m}$, Diluted Shares $N = 10\text{m}$, and Market Price $P = \$6.00$. (All financial figures are in millions except per-share values).

            First, compute **Unadjusted NCAV per share**:
            $$\text{NCAV}_{\text{unadj}} = \frac{\$40\text{m} + \$60\text{m} + \$80\text{m} - \$70\text{m}}{10\text{m}} = \frac{\$110\text{m}}{10\text{m}} = \$11.00\text{ per share}$$
            Graham's two-thirds screen threshold is:
            $$P_{\text{screen}} = \frac{2}{3} \times \$11.00 \approx \$7.33\text{ per share}$$
            Because the active market price is $P = \$6.00 \le \$7.33$, the stock successfully passes Graham's unadjusted two-thirds screen.

            Next, apply realistic liquidation recovery haircuts ($\rho_R = 0.85$, $\rho_I = 0.60$):
            $$\text{Recoverable Assets} = \$40\text{m} + (0.85 \times \$60\text{m}) + (0.60 \times \$80\text{m}) = \$40\text{m} + \$51\text{m} + \$48\text{m} = \$139\text{m}$$
            Deducting total liabilities:
            $$\text{Adjusted Net Liquid Assets} = \$139\text{m} - \$70\text{m} = \$69\text{m}$$
            $$\text{NCAV}_{\text{adj}} = \frac{\$69\text{m}}{10\text{m}} = \$6.90\text{ per share}$$
            The margin of safety relative to adjusted asset backing is:
            $$\text{MoS} = 1 - \frac{\$6.00}{\$6.90} \approx +13.04\%$$

            Now stress-test inventory recovery. If market conditions deteriorate and inventory realizes only $\rho_I = 40\%$ ($0.40$):
            $$\text{Recoverable Assets} = \$40\text{m} + \$51\text{m} + (0.40 \times \$80\text{m}) = \$40\text{m} + \$51\text{m} + \$32\text{m} = \$123\text{m}$$
            $$\text{NCAV}_{\text{adj}} = \frac{\$123\text{m} - \$70\text{m}}{10\text{m}} = \frac{\$53\text{m}}{10\text{m}} = \$5.30\text{ per share}$$
            At $\$5.30$, the active market price of $\$6.00$ trades at a premium over liquid asset backing ($\text{MoS} = 1 - 6.00 / 5.30 = -13.2\%$).

            We can solve algebraically for the exact break-even inventory recovery rate $\rho_I^*$ where adjusted NCAV equals the $\$6.00$ price:
            $$\frac{40 + 51 + 80\rho_I^* - 70}{10} = 6.00 \implies 21 + 80\rho_I^* = 60 \implies 80\rho_I^* = 39 \implies \rho_I^* = \frac{39}{80} = 48.75\%$$
            If inventory recovers less than $48.75\%$, the investment thesis loses its asset-backed protection.

            Finally, examine the Graham heuristic: with $\text{EPS} = \$4.00$, growth $g = 5\%$, and bond yield $Y = 4.4\%$:
            $$V_{\text{Graham}} = \frac{4.00 \times (8.5 + 2 \times 5) \times 4.4}{4.4} = 4.00 \times 18.5 = \$74.00$$
            If bond yields rise to $Y = 6.0\%$, valuation falls sharply to $4.00 \times 18.5 \times (4.4 / 6.0) \approx \$54.27$."""
        ),
        text(
            r"""**Navigate to the Valuation workbench.** Click the **Valuation** tab in the top navigation bar. Under **BALANCE SHEET INPUTS**, inspect the baseline figures: **Cash & equivalents** ($40$), **Accounts receivable** ($60$), **Inventory** ($80$), **Total liabilities** ($70$), **Diluted shares** ($10$), and **Market price / share** ($6$).

            **Audit the Valuation Worksheet.** The right-hand panel **VALUATION WORKSHEET** displays:
            - **ADJUSTED NCAV / SHARE**: $\$6.90$
            - Comparison progress bar: Market price ($\$6.00$) vs Adjusted asset value ($\$6.90$)
            - **Unadjusted NCAV**: $\$11.00$
            - **Two-thirds screen price**: $\$7.33$
            - **Margin of safety · adjusted NCAV**: $+13.0\%$
            - **Graham heuristic value**: $\$74.00$
            - Screen verdict badge: "Passes the unadjusted two-thirds NCAV screen."

            **Stress-test liquidation recovery rates.** In the **Liquidation assumptions** section, drag **Inventory recovered** from $60\%$ down to $40\%$. Watch the status indicator "· UPDATING" appear momentarily. Adjusted NCAV per share drops to $\$5.30$, and Margin of safety turns negative ($-13.2\%$). Notice that the verdict badge still reads "Passes the unadjusted two-thirds NCAV screen." because the screen evaluates unadjusted accounting book values.

            **Find the exact break-even recovery.** Adjust the inventory slider until the Margin of Safety reads $0.0\%$. Confirm that the recovery rate settles at approximately $48.75\%$.

            **Evaluate the Graham growth heuristic.** Under **Graham formula inputs**, change **Bond yield (%)** from $4.4\%$ to $6.0\%$. Watch the heuristic valuation contract from $\$74.00$ down to $\$54.27$. Next, change **Growth (%)** from $5\%$ to $10\%$: the valuation jumps to $\$83.60$. Observe how volatile growth assumptions are compared to tangible balance-sheet asset liquidation values."""
        ),
        r"\text{NCAV}_{\text{adj}} = \frac{C + \rho_R R + \rho_I I - L}{N}, \qquad \text{MoS} = 1 - \frac{P}{\text{NCAV}_{\text{adj}}}, \qquad V_{\text{Graham}} = \frac{\text{EPS}(8.5 + 2g)4.4}{Y}",
        '''
cash = 40.0
receivables = 60.0
inventory = 80.0
liabilities = 70.0
shares = 10.0
price = 6.00

ncav_unadj = (cash + receivables + inventory - liabilities) / shares
screen_price = ncav_unadj * (2.0 / 3.0)
print("Unadjusted NCAV per share:", round(ncav_unadj, 2))
print("Graham two-thirds screen threshold:", round(screen_price, 2))
print("Passes unadjusted screen:", price <= screen_price)

for inv_rate in [0.60, 0.40]:
    ncav_adj = (cash + 0.85 * receivables + inv_rate * inventory - liabilities) / shares
    mos = (1.0 - price / ncav_adj) * 100.0
    print("At inventory recovery", inv_rate, "-> Adjusted NCAV:", round(ncav_adj, 2), "Margin of Safety:", round(mos, 2), "%")

break_even_inv = (price * shares - cash - 0.85 * receivables + liabilities) / inventory
print("Break-even inventory recovery rate:", round(break_even_inv * 100.0, 2), "%")

eps = 4.0
for y in [4.4, 6.0]:
    v = eps * (8.5 + 2.0 * 5.0) * 4.4 / y
    print("Graham value at yield", y, "%:", round(v, 2))
''',
        "Determine the exact inventory recovery rate at which adjusted NCAV per share equals the $6.00 market price, using default balance sheet inputs. Then compute the Graham heuristic value at growth rates of 0%, 5%, and 10% under a 4.4% bond yield. Explain which metric warrants greater quantitative confidence.",
        "With default balance sheet inputs ($40m cash, $60m receivables at 85% recovery, $80m inventory, $70m liabilities, 10m shares), adjusted NCAV equals the $6.00 market price when (40 + 51 + 80*r - 70)/10 = 6.00, yielding 21 + 80*r = 60, or r = 39/80 = 48.75%. Below 48.75% inventory recovery, the margin of safety becomes negative. The Graham growth heuristic produces $34.00 at 0% growth, $74.00 at 5% growth, and $114.00 at 10% growth under a 4.4% bond yield. Adjusted NCAV warrants substantially greater quantitative confidence because it is anchored in verifiable, audited balance-sheet liquid assets, whereas the Graham growth formula swings wildly ($+$40 per 5 percentage points of growth) based on subjective, unprovable future growth assumptions.",
        [
            (
                "With the default inputs, what does 'ADJUSTED NCAV / SHARE' show?",
                "$6.90, after recovering 85% of receivables and 60% of inventory",
                "$11.00, the unadjusted figure",
                "$7.33, the two-thirds screen price",
                "Adjusted NCAV = (Cash + 0.85 * Receivables + 0.60 * Inventory - Liabilities) / Shares = (40 + 51 + 48 - 70) / 10 = $69m / 10m = $6.90 per share.",
            ),
            (
                "Inventory recovery falls from 60% to 40%. What happens to adjusted NCAV per share?",
                "It falls by $1.60, to $5.30",
                "It rises, because liabilities fall",
                "It stays at $6.90, because inventory is excluded",
                "A 20 percentage point reduction in recovery across $80m of inventory reduces total asset recovery by $16m. Divided across 10m shares, adjusted NCAV falls by exactly $1.60 per share, from $6.90 to $5.30.",
            ),
            (
                "Why can a stock pass the two-thirds NCAV screen yet trade above its adjusted asset value?",
                "The screen uses unadjusted NCAV, while the adjusted value applies recovery haircuts",
                "The screen already includes the haircuts",
                "The Graham heuristic overrides the screen",
                "Graham's traditional two-thirds screen is calculated from unadjusted balance sheet accounting book values ($11.00 * 2/3 = $7.33). Realistic liquidation recovery haircuts on inventory and receivables can easily reduce adjusted NCAV below the prevailing share price.",
            ),
            (
                "In the Graham heuristic, what does raising the bond yield from 4.4% to 6% do to a value of $74?",
                "Lowers it to about $54.27",
                "Raises it to about $100.91",
                "Leaves it unchanged, because the yield is not in the formula",
                "The AAA corporate bond yield acts as the discount rate in Graham's heuristic formula, appearing in the denominator: $74.00 * (4.4 / 6.0) ≈ $54.27.",
            ),
        ],
        [SEC_STATEMENTS, IG_STOCKS],
        "valuation",
        "move the two recovery sliders until the margin of safety reaches zero, and record the recovery rates at which the price equals the adjusted asset value.",
        "30-minute session: 8 minutes studying deep-value liquidation models and haircut theory, 10 minutes working through the adjusted NCAV and break-even recovery arithmetic, and 12 minutes stress-testing balance sheet assumptions in the Valuation tab; all corporate balance sheets in the tool are educational models.",
    )

    # ------------------------------------------------------------------ 14.7
    add(
        "The factor studio: models, coefficients and robust errors",
        "Estimate CAPM and Fama-French multi-factor regressions on synthetic asset returns, interpret factor betas with Newey-West HAC standard errors, and evaluate alpha estimates through the lens of statistical significance.",
        text(
            r"""Modern quantitative portfolio management relies on linear asset pricing models to decompose an asset's returns into systematic factor risk exposures and idiosyncratic residual performance. Instead of asking whether a manager made money, factor analysis asks *how* that money was made—separating passive market beta, small-cap tilts, and value premiums from genuine investment skill.

            The **Factor studio** estimates multi-factor regressions via Ordinary Least Squares (OLS):
            $$r_{i,t} - r_{f,t} = \alpha_i + \beta_{\text{MKT}} f_{\text{MKT},t} + \beta_{\text{SMB}} f_{\text{SMB},t} + \beta_{\text{HML}} f_{\text{HML},t} + \varepsilon_{i,t}$$
            where $r_{i,t} - r_{f,t}$ is the asset's excess return, $f_{\text{MKT},t}$ is the excess market return, $f_{\text{SMB},t}$ is the Small-Minus-Big size factor, $f_{\text{HML},t}$ is the High-Minus-Low value factor, $\alpha_i$ represents abnormal risk-adjusted performance (alpha), and $\varepsilon_{i,t}$ is the residual disturbance.

            In financial econometric regressions, standard OLS standard errors are notoriously unreliable because residuals exhibit time-varying heteroskedasticity and serial autocorrelation. If uncorrected, conventional standard errors appear artificially narrow, producing falsely inflated $t$-statistics and spurious discoveries. The Factor studio resolves this by reporting **Newey–West HAC (Heteroskedasticity and Autocorrelation Consistent)** standard errors:
            $$t_{\hat\beta} = \frac{\hat\beta - \beta_0}{\operatorname{SE}_{\text{HAC}}(\hat\beta)}$$

            Crucially, the Factor studio provides something impossible in real-world finance: **a known ground truth**. The data is generated from a known Data-Generating Process (DGP) with pre-set factor exposures, displayed in the panel **KNOWN DATA-GENERATING PROCESS**. This allows you to evaluate econometric precision by measuring the exact distance between OLS estimates and planted truth in standard error units.

            The tool also reports **TEST R² · RIDGE**: a cross-validation test that trains a regularized ridge regression on the first $75\%$ of observations ($567\text{ bars}$) and scores it out-of-sample on the remaining $25\%$ ($189\text{ bars}$). This out-of-sample test protects against overfitting."""
        ),
        text(
            r"""To evaluate factor regression mechanics, examine the baseline configuration: Fama–French three-factor model, $N = 756$ observations, random seed 42, and $1.0\%$ daily idiosyncratic volatility.

            The planted ground-truth parameters are:
            $$\beta_{\text{MKT}} = 1.10, \quad \beta_{\text{SMB}} = 0.25, \quad \beta_{\text{HML}} = 0.40, \quad \alpha_{\text{daily}} = 0.0001\text{ (1 bp/day)}$$

            Executing the OLS fit yields the following parameter estimates:
            - **Market Beta**: $\hat{\beta}_{\text{MKT}} = 1.0907$ with $\operatorname{SE}_{\text{HAC}} = 0.0393$.
              Measuring distance from ground truth:
              $$t_{\text{diff}} = \frac{\hat{\beta}_{\text{MKT}} - \beta_{\text{MKT}}}{\operatorname{SE}_{\text{HAC}}} = \frac{1.0907 - 1.1000}{0.0393} = \frac{-0.0093}{0.0393} \approx -0.237\text{ standard errors}$$
            - **SMB Beta**: $\hat{\beta}_{\text{SMB}} = 0.2256$ with $\operatorname{SE}_{\text{HAC}} = 0.0385$.
              $$t_{\text{diff}} = \frac{0.2256 - 0.2500}{0.0385} = \frac{-0.0244}{0.0385} \approx -0.634\text{ standard errors}$$
            - **HML Beta**: $\hat{\beta}_{\text{HML}} = 0.3662$ with $\operatorname{SE}_{\text{HAC}} = 0.0371$.
              $$t_{\text{diff}} = \frac{0.3662 - 0.4000}{0.0371} = \frac{-0.0338}{0.0371} \approx -0.911\text{ standard errors}$$
            All three systematic factor estimates land within $1.0$ standard error of ground truth, reflecting excellent econometric recovery. In-sample $R^2$ reaches $0.564$, and out-of-sample Ridge Test $R^2$ confirms stability at $0.496$.

            Now examine the estimated daily alpha:
            $$\hat{\alpha}_{\text{daily}} = 0.000586\text{ with } \operatorname{SE}_{\text{HAC}} = 0.000381, \quad t = 1.54, \quad p = 0.124$$
            Annualizing this daily alpha yields an apparently massive return:
            $$\text{Annualized Alpha} \approx 0.000586 \times 252 \approx +14.77\%$$

            An unsophisticated investor would celebrate a $+14.8\%$ annualized alpha. But the econometrician checks the $p$-value: at $p = 0.124 > 0.05$, the estimate is statistically indistinguishable from zero! In fact, the true planted alpha was only $0.0001$ ($2.5\%$ annually). The estimated $+14.8\%$ was largely an artifact of random sampling noise. Precise factor loadings alongside noisy, statistically insignificant alpha estimates are the norm in empirical asset pricing."""
        ),
        text(
            r"""**Open the Factor studio.** Click the **Factor studio** tab. Leave the default settings: **Factor specification** set to "Fama–French · three factors", **Observations** at 756, **Random seed** at 42, and **Idiosyncratic daily volatility** at 1.0%. Click **Fit factor model**.

            **Audit model diagnostics.** Under **MODEL DIAGNOSTICS**, inspect the summary cards:
            - **R² · OLS**: $0.564$
            - **ADJUSTED R²**: $0.562$
            - **TEST R² · RIDGE**: $0.496$
            Read the explanatory footnote: "756 observations · 6 HAC lags · ridge training/test split 567/189."

            **Audit the coefficient table.** Review the regression results table:
            - Alpha (daily): $\beta = 0.000586$, $\operatorname{SE} = 0.000381$, $p = 0.124$
            - Market: $\beta = 1.0907$, $\operatorname{SE} = 0.0393$, $p < 0.001$
            - SMB: $\beta = 0.2256$, $\operatorname{SE} = 0.0385$, $p < 0.001$
            - HML: $\beta = 0.3662$, $\operatorname{SE} = 0.0371$, $p < 0.001$

            **Verify estimation accuracy against ground truth.** Compare the estimated betas against the **KNOWN DATA-GENERATING PROCESS** box (Market $1.10$, SMB $0.25$, HML $0.40$). Divide each difference by its reported SE · HAC: confirm that all three estimates land within $\pm 1.0$ standard errors of truth.

            **Evaluate model misspecification.** Switch **Factor specification** to **CAPM · market only** and click **Fit factor model**. Observe how the Market beta shifts to $1.1235$: omitting the SMB and HML factors forces their correlated risk exposures to load onto the market term. Next, test **Carhart · four factors** and **Fama–French · five factors** to observe how additional factors modify $R^2$.

            **Scale idiosyncratic noise.** Increase **Idiosyncratic daily volatility** from $1.0\%$ to $3.0\%$ and re-fit. Notice that OLS $R^2$ collapses to $\approx 0.14$, standard errors triple in width, and parameter estimates wander further from ground truth, illustrating how unmodeled noise obscures systematic signals."""
        ),
        r"r_t - r_{f,t} = \alpha + \sum_{k} \beta_k f_{k,t} + \varepsilon_t, \qquad t = \frac{\hat{\beta} - \beta_0}{\operatorname{SE}_{\text{HAC}}(\hat{\beta})}, \qquad \alpha_{\text{annual}} \approx \hat{\alpha} \times 252",
        '''
estimates = [1.0907, 0.2256, 0.3662]
hac_errors = [0.0393, 0.0385, 0.0371]
ground_truth = [1.10, 0.25, 0.40]
names = ["Market", "SMB", "HML"]

for i in range(len(names)):
    diff = estimates[i] - ground_truth[i]
    se_dist = diff / hac_errors[i]
    print(names[i], "estimate:", estimates[i], "truth:", ground_truth[i], "distance in SE:", round(se_dist, 3))

alpha_est = 0.000586
alpha_se = 0.000381
alpha_t = alpha_est / alpha_se
alpha_annual = alpha_est * 252.0 * 100.0
print("Daily alpha estimate:", alpha_est, "t-statistic:", round(alpha_t, 2))
print("Annualized alpha:", round(alpha_annual, 2), "% (p-value = 0.124: statistically unproven!)")
''',
        "Fit the Fama–French three-factor model on seeds 42, 43, and 44 with default parameters. For each seed, record each estimated beta, its HAC standard error, its distance from ground truth in standard errors, and the daily alpha's p-value. Explain what remains stable across seeds versus what varies.",
        "Across seeds 42, 43, and 44, the estimated systematic factor loadings consistently cluster near the true planted exposures (Market ~ 1.09-1.12 vs 1.10; SMB ~ 0.21-0.26 vs 0.25; HML ~ 0.36-0.42 vs 0.40), with nearly all estimates remaining within 1.5 HAC standard errors of truth. This stability confirms that linear OLS regressions reliably recover systematic risk loadings from 756 observations. In contrast, the daily alpha estimate fluctuates wildly across seeds, shifting in magnitude and sign with p-values consistently above 0.05. Because a tiny planted alpha (~0.0001/day) is easily drowned out by 1.0% idiosyncratic noise, an annualized alpha of ~15% cannot be distinguished from zero. Quantitative researchers must report HAC standard errors and treat statistically insignificant alpha as unproven noise rather than investment skill.",
        [
            (
                "Which column shows how uncertain each coefficient is?",
                "SE · HAC, a standard error robust to changing and correlated errors",
                "β, because it already includes the error",
                "R² · OLS, the share of variance explained",
                "The SE · HAC column displays Newey–West Heteroskedasticity and Autocorrelation Consistent standard errors, which quantify coefficient estimation uncertainty under real-world financial disturbance structures.",
            ),
            (
                "The planted market exposure is 1.10 and the estimate is 1.0907 with a standard error of 0.0393. What is the right reading?",
                "The estimate lies about a quarter of a standard error from the truth, ordinary sampling noise",
                "The model is badly biased",
                "The true exposure must be 1.0907",
                "The distance from ground truth is (1.0907 - 1.1000) / 0.0393 = -0.237 standard errors. Landing within 0.24 standard errors of truth represents high econometric precision well within normal random sampling variation.",
            ),
            (
                "The daily alpha estimate is 0.000586 with a p-value of 0.124. What can you conclude?",
                "The data cannot distinguish it from zero, even though it annualizes to about 15%",
                "The strategy earns about 15% a year of skill",
                "Alpha is exactly zero",
                "A p-value of 0.124 means that an estimate this large would occur by random chance in over 12% of zero-skill samples. Statistically, the estimate is indistinguishable from zero, and annualizing a noisy estimate does not make it significant.",
            ),
            (
                "Why does the studio also report 'TEST R² · RIDGE'?",
                "It fits on the earlier 75% of observations and scores the later 25%, an out-of-sample check",
                "It is the same R² computed with a different formula",
                "It counts how many factors are in the model",
                "Ordinary OLS R² is an in-sample goodness-of-fit metric vulnerable to overfitting. The Ridge Test R² trains on the first 75% of observations and scores against the final 25%, providing an essential out-of-sample cross-validation check.",
            ),
        ],
        [FRENCH, STATSMODELS_HAC, HLZ],
        "factors",
        "fit the three-factor model at seeds 42, 43 and 44 and record how far each estimated exposure lands from its planted value, measured in standard errors.",
        "30-minute session: 8 minutes reading empirical factor asset pricing theory, 10 minutes calculating standard error distances and alpha significance by hand, and 12 minutes fitting factor specifications in the Factor studio; all observations are generated from known synthetic DGPs.",
    )

    # ------------------------------------------------------------------ 14.8
    add(
        "Robustness in the sandbox: costs, seeds and scenarios",
        "Conduct comprehensive robustness evaluations across random seeds, escalating transaction cost structures, and exogenous stress scenarios, and account for multiple testing bias in strategy evaluation.",
        text(
            r"""A quantitative backtest evaluated on a single dataset or random seed represents only a single realization of a stochastic process. A trading rule that demonstrates spectacular returns on seed 42 may incur devastating losses on seed 43 simply due to the timing luck of local peaks and troughs. Scientifically rigorous research requires multidimensional robustness sweeps to determine whether a strategy possesses a genuine structural edge or is merely overfitted to historical noise.

            Robustness testing in the Market sandbox spans three orthogonal testing dimensions:
            1. **Seed Dispersion Sweeps**: Run the identical strategy across multiple independent random seeds ($S = 5$) holding all market parameters constant. Calculate the ensemble mean $\bar{R}$ and sample standard deviation $\hat{\sigma}_R$:
               $$\bar{R} = \frac{1}{S} \sum_{s=1}^{S} R_s, \qquad \hat{\sigma}_R = \sqrt{\frac{1}{S - 1} \sum_{s=1}^{S} (R_s - \bar{R})^2}$$
               A wide standard deviation relative to the mean signals that performance is heavily path-dependent.
            2. **Transaction Cost Escalation**: Evaluate strategy viability as transaction friction scales from frictionless conditions ($0\text{ bps}$), to standard institutional costs ($8\text{ bps}$ total), to stressed retail friction ($40\text{ bps}$ total). If a strategy's profitability collapses under standard costs, it has no viable commercial future.
            3. **Exogenous Stress Scenarios**: Subject the rule to five distinct historical-inspired market stress regimes:
               - **Pure random walk**: Zero drift ($\mu = 0$), pure diffusion.
               - **Deflationary crash · 1929-inspired**: Jump diffusion with $-15\%$ annual decline and $38\%$ volatility.
               - **Stagflation · 1970s-inspired**: Low drift ($+1.5\%$) with severe volatility ($32\%$).
               - **Liquidity crisis · 2008-inspired**: Heston stochastic volatility with $-18\%$ annual collapse and $55\%$ volatility.
               - **Crypto flash crash · −50%**: Injects a sudden 1-day $-50\%$ liquidity hole at the midpoint bar.

            Crucially, every parameter tweak or seed you execute represents an experimental trial. Testing 40 variations and reporting only the single best Sharpe ratio introduces severe **multiple-testing selection bias**. Quantitative researchers must log total trial counts and apply Deflated Sharpe Ratio adjustments."""
        ),
        text(
            r"""To quantify robustness, evaluate the baseline 50-day trend rule across five consecutive seeds (seeds 42 through 46) under default parameters ($T = 3\text{ years}$, $5\text{ bps}$ commission, $3\text{ bps}$ slippage):

            - **Seed 42**: Strategy $R = -23.40\%$, Buy & Hold $R = -18.46\%$, Strategy $\text{MDD} = -27.07\%$ vs Hold $\text{MDD} = -34.18\%$
            - **Seed 43**: Strategy $R = +4.90\%$, Buy & Hold $R = +5.10\%$, Strategy $\text{MDD} = -21.40\%$ vs Hold $\text{MDD} = -28.90\%$
            - **Seed 44**: Strategy $R = +19.60\%$, Buy & Hold $R = +88.40\%$, Strategy $\text{MDD} = -18.30\%$ vs Hold $\text{MDD} = -26.10\%$
            - **Seed 45**: Strategy $R = +2.30\%$, Buy & Hold $R = +30.70\%$, Strategy $\text{MDD} = -22.10\%$ vs Hold $\text{MDD} = -31.50\%$
            - **Seed 46**: Strategy $R = -5.80\%$, Buy & Hold $R = +0.40\%$, Strategy $\text{MDD} = -29.50\%$ vs Hold $\text{MDD} = -25.20\%$

            Computing the ensemble statistics across the 5 seeds:
            $$\bar{R}_{\text{rule}} = \frac{-23.40 + 4.90 + 19.60 + 2.30 - 5.80}{5} = \frac{-2.40}{5} = -0.48\%$$
            $$\hat{\sigma}_{R} \approx 15.82\text{ percentage points}$$

            The active strategy lagged the passive Buy & Hold benchmark on all five seeds! However, the trend rule achieved a shallower maximum drawdown on 4 out of the 5 seeds (averaging $\text{MDD} \approx -23.7\%$ compared to $-29.2\%$ for buy-and-hold). If an unethical marketer reported only seed 44 ($+19.60\%$), they would present a completely distorted picture of performance.

            Next, examine the **Cost Sensitivity** on seed 42:
            - Zero costs ($0\text{ bps}$ commission, $0\text{ bps}$ slippage): $R = -19.73\%$
            - Default costs ($5\text{ bps}$ commission, $3\text{ bps}$ slippage): $R = -23.40\%$
            - Adverse costs ($20\text{ bps}$ commission, $20\text{ bps}$ slippage): $R = -37.46\%$

            Finally, examine the **Stress Scenarios** on seed 42:
            - Pure random walk: Strategy $-26.6\%$ vs Buy & Hold $-35.8\%$
            - 1929 Deflationary crash: Strategy $-75.4\%$ vs Buy & Hold $-92.0\%$
            - 1970s Stagflation: Strategy $-36.8\%$ vs Buy & Hold $-51.4\%$
            - 2008 Liquidity crisis: Strategy $-37.3\%$ vs Buy & Hold $-64.1\%$
            - Crypto flash crash: Strategy $-57.5\%$ vs Buy & Hold $-59.2\%$
            In severe market crashes, trend following significantly mitigates losses by stepping aside into cash as prices cross beneath the moving average. However, in the flash crash, the $-50\%$ gap occurs in a single bar before signals can exit."""
        ),
        text(
            r"""**Prepare the experimental baseline.** In the **Market sandbox**, select the **Trend following** chip and confirm default parameters ($T = 3$, $5\text{ bps}$ commission, $3\text{ bps}$ slippage). Click the gear icon (**Execution settings**) to access the **Seed** input.

            **Execute the 5-seed sweep.** Run seeds 42, 43, 44, 45, and 46 in succession. For each run, record Total return and Max drawdown from **All metrics**, and record the benchmark Buy & Hold return from the terminal point of the dashed curve on the **Equity curve** chart. Compute the sample mean and standard deviation.

            **Execute the transaction friction sweep.** Set the seed back to 42. In **Execution settings**, set **Commission (bps)** and **Slippage (bps)** to 0 and execute. Record final equity ($\$80{,}271$). Set both to defaults ($5$ and $3$) and record ($\$76{,}598$). Set both to $20\text{ bps}$ each and record ($\$62{,}538$).

            **Execute the scenario stress sweep.** Keep seed 42 and default costs. Open the **Parameters** tab. Select each scenario from the **SCENARIO** dropdown in turn:
            1. Pure random walk
            2. Deflationary crash · 1929-inspired
            3. Stagflation · 1970s-inspired
            4. Liquidity crisis · 2008-inspired
            5. Crypto flash crash · −50%
            Execute each run and record the comparative strategy and benchmark returns. Notice the note: "Named stress scenarios override selected process defaults."

            **Log total experimental trials.** Count every run executed during this lesson: 5 seed trials $+ 3$ cost trials $+ 5$ scenario trials $= 13$ total trials. Document all 13 trials in your research notebook. Acknowledge that the best-performing run cannot be cited in isolation without disclosing the full trial ledger."""
        ),
        r"\bar{R} = \frac{1}{S}\sum_{s=1}^{S} R_s, \qquad \hat\sigma_R = \sqrt{\frac{1}{S-1}\sum_{s=1}^{S}(R_s - \bar{R})^2}, \qquad \text{Trials}_{\text{total}} = S_{\text{seeds}} + C_{\text{costs}} + M_{\text{scenarios}}",
        '''
from math import sqrt

rule_returns = [-23.40, 4.90, 19.60, 2.30, -5.80]
hold_returns = [-18.46, 5.10, 88.40, 30.70, 0.40]
s = len(rule_returns)
mean_return = sum(rule_returns) / s
variance = sum((r - mean_return) ** 2 for r in rule_returns) / (s - 1)
std_dev = sqrt(variance)

print("Ensemble mean return across 5 seeds:", round(mean_return, 2), "%")
print("Sample standard deviation across seeds:", round(std_dev, 2), "percentage points")

beats_hold = sum(1 for i in range(s) if rule_returns[i] > hold_returns[i])
print("Seeds where strategy outperformed Buy & Hold:", beats_hold, "of", s)

total_trials = 5 + 3 + 5
print("Total experimental trials executed in this lesson:", total_trials)
''',
        "Execute the baseline trend rule across five seeds (42–46), three cost settings (0, default, 20 bps), and all five named stress scenarios. Tabulate the strategy return against buy-and-hold for all runs, compute the mean and standard deviation across seeds, and state the total trial count alongside your scientific conclusions.",
        "Across seeds 42-46 with default parameters, the 50-day trend rule averages -0.48% total return with a sample standard deviation of 15.82 percentage points, lagging buy-and-hold on all 5 seeds while achieving shallower drawdowns on 4 of 5 seeds. On seed 42, escalating transaction costs drives total return from -19.73% (zero friction) to -23.40% (default) and -37.46% (20 bps friction), demonstrating high sensitivity to execution drag. Across stress scenarios, the trend rule cushions capital in persistent bear regimes (losing -75.4% vs -92.0% in 1929; -37.3% vs -64.1% in 2008), but cannot prevent gap losses during single-day shocks (-57.5% in the flash crash). A complete research report documents all 13 trials, recognizing that reporting only seed 44 (+19.6%) would constitute multiple-testing selection bias, and that synthetic results cannot prove live market edge.",
        [
            (
                "Why rerun the same rule on several seeds?",
                "Each seed is one generated path, so a single result could be luck",
                "Seeds change the strategy code",
                "More seeds make each individual run more accurate",
                "Each pseudorandom seed generates a single stochastic path through time. Testing across multiple seeds reveals the distribution of returns, separating genuine systemic strategy edge from single-path random fortune.",
            ),
            (
                "What does the 'Crypto flash crash · −50%' scenario add?",
                "A one-day −50% shock at the middle bar, on top of the chosen process",
                "A permanent −50% annual drift",
                "Real cryptocurrency prices",
                "The flash-crash scenario preserves your active stochastic process parameters and injects a single -50% price drop at the middle bar (bar 378), testing algorithmic behavior under sudden, discontinuous market gaps.",
            ),
            (
                "You tried 40 variants and want to report the best Sharpe ratio. What must accompany it?",
                "The number of trials, because the best of many is inflated by chance",
                "Nothing, because the best result is the true one",
                "A higher commission setting",
                "Selecting the maximum Sharpe ratio from 40 backtests creates massive multiple-testing selection bias. Reporting the total trial count allows reviewers to apply Deflated Sharpe Ratio or Bonferroni adjustments.",
            ),
            (
                "Setting commission and slippage to zero turns a losing rule into a winner. What does that show?",
                "Any edge the rule has is smaller than its trading costs",
                "Costs should always be set to zero",
                "The rule is robust",
                "If a trading rule requires zero transaction costs to show profitability, its theoretical gross edge is thinner than normal market microstructure friction. Such strategies are guaranteed to fail in live trading.",
            ),
        ],
        [PBO, DSR, STYLIZED],
        "market",
        "run the default rule on five seeds and on the five named scenarios with every other setting fixed, and tabulate total return against buy and hold for all ten runs.",
        "30-minute session: 6 minutes studying multiple-testing bias and Monte Carlo dispersion theory, 8 minutes analyzing cross-seed statistics, and 16 minutes executing parameter and scenario sweeps in the Market sandbox; all scenarios represent synthetic models rather than historical replays.",
    )
    # ------------------------------------------------------------------ 14.9
    add(
        "Paper trading: liquidity, stale-data, spread and drawdown guards",
        "Operate the mock broker simulation, calculate execution prices with bid-ask spread, slippage, and volume participation caps, and trigger deterministic pre-trade risk guards and circuit breakers.",
        text(
            r"""Moving from backtesting to order execution introduces the harsh realities of market microstructure. In a backtest, orders are assumed to execute smoothly; in live markets, liquidity vanishes, quotes become stale, spreads blow out during panic, and flawed algorithms can bankrupt a firm in minutes. The **Paper trading** tool provides a deterministic single-session mock broker engineered to demonstrate the pre-trade risk controls and safety guards required by institutional market-access regulations (such as SEC Rule 15c3-5).

            The paper account starts with $\$100{,}000$ in simulated cash and operates on a long-only basis. When an order is submitted, the broker models three market frictions:
            1. **Bid-Ask Spread & Slippage**: The executed fill price moves away from the reference price by the full slippage plus one-half of the bid-ask spread:
               $$P_{\text{fill}} = P_{\text{ref}} \left(1 \pm \frac{s + \frac{1}{2}\text{spread}}{10{,}000}\right)$$
               (Plus for purchases, minus for sales, where $s$ and $\text{spread}$ are specified in basis points).
            2. **Brokerage Commission**: A commission fee ($c\text{ bps}$, default $5\text{ bps}$) is charged on the total executed dollar value.
            3. **Volume Participation Cap**: To prevent the illusion that arbitrary order size can trade at a single price, the broker caps fill quantity at $10\%$ of available bar volume:
               $$q_{\text{fill}} = \min(q_{\text{order}}, \, 0.10 \times V_{\text{bar}})$$
               If an order exceeds this limit, it executes partially up to the cap, and the remaining shares are immediately discarded as unfilled.

            Before executing any order, the broker evaluates a deterministic six-stage **Pre-Trade Guard Pipeline**:
            1. **Halted State Check**: If the account is halted, all order submissions are rejected.
            2. **Drawdown Circuit Breaker**: If marked equity falls below $97.5\%$ of starting capital ($\$97{,}500$), the circuit breaker trips, halting the account to prevent catastrophic runaway loss.
            3. **Stale Data Guard**: If the reference price quote is older than 60 seconds, the order is rejected ("Price data is stale.").
            4. **Excessive Spread Guard**: If the bid-ask spread exceeds $100\text{ bps}$, the order is rejected ("Spread exceeds the 100 bps guard.").
            5. **Liquidity Guard**: If available bar volume is zero, the order is rejected ("No available liquidity.").
            6. **Balance Sufficiency Guard**: The account must hold sufficient cash for purchases (including fees) or sufficient shares for sales.

            This deterministic guard architecture illustrates the vital safeguard that Knight Capital infamously lacked in 2012 when an unconstrained algorithmic loop lost $\$440$ million in 45 minutes."""
        ),
        text(
            r"""To trace execution mechanics and safety guards, examine a standard purchase:
            Order quantity $q = 10\text{ shares}$, reference price $P_{\text{ref}} = \$100.00$, available bar volume $V = 1{,}000\text{ shares}$, spread $= 5\text{ bps}$, slippage $s = 3\text{ bps}$, and commission $c = 5\text{ bps}$.

            The executed fill price is:
            $$P_{\text{fill}} = 100.00 \times \left(1 + \frac{3 + \frac{5}{2}}{10{,}000}\right) = 100.00 \times \left(1 + \frac{5.5}{10{,}000}\right) = 100.00 \times 1.00055 = \$100.055$$
            The total cost for 10 shares is $10 \times 100.055 = \$1{,}000.55$.
            The $5\text{ bps}$ commission is:
            $$\text{Fee} = \$1{,}000.55 \times 0.0005 = \$0.500275 \approx \$0.50$$
            Total cash outlay is $\$1{,}000.55 + \$0.50 = \$1{,}001.05$, leaving $\$98{,}998.95$ in available cash.

            Now observe the **Volume Participation Cap**:
            Submit an order for 150 shares against the same $1{,}000$ shares of bar volume.
            The broker enforces the $10\%$ participation limit:
            $$q_{\text{fill}} = \min(150, \, 0.10 \times 1{,}000) = \min(150, 100) = 100\text{ shares}$$
            The order executes 100 shares, and the **ORDER AUDIT LOG** flags the status as "partially filled". The remaining 50 shares are not queued.

            Finally, examine the **Drawdown Circuit Breaker**:
            Reset the account and set bar volume to $100{,}000$ shares.
            Place an aggressive buy order for 990 shares at $P_{\text{ref}} = \$100.00$.
            The purchase cost is $990 \times 100.055 = \$99{,}054.45$, plus commission of $\$49.53$, totaling $\$99{,}103.98$.
            Remaining cash is:
            $$\text{Cash} = \$100{,}000.00 - \$99{,}103.98 = \$896.02$$

            Now simulate a market drop: change the reference price to $\$97.00$ and attempt any order.
            The broker marks active portfolio equity to market before processing the order:
            $$\text{Marked Equity} = \text{Cash} + (\text{Shares} \times P_{\text{ref}}) = \$896.02 + (990 \times \$97.00) = \$896.02 + \$96{,}030.00 = \$96{,}926.02$$
            Expressing marked equity as a percentage of initial capital:
            $$\text{Equity Ratio} = \frac{\$96{,}926.02}{\$100{,}000.00} = 96.93\%$$
            Because $96.93\% < 97.50\%$, the drawdown circuit breaker trips immediately. The order is rejected, the account risk state switches to "Halted", and all future submissions are blocked until a manual simulation reset is performed."""
        ),
        text(
            r"""**Navigate to the Paper broker.** Click the **Paper trading** tab. The header displays "QUANTA MOCK BROKER". Review the live account telemetry: **CASH AVAILABLE** ($\$100{,}000.00$), **SHARES HELD** ($0$), **MARKED EQUITY** ($\$100{,}000.00$), and **RISK STATE** ("Normal").

            **Submit a baseline order.** Configure the order ticket: Side **Buy**, **Order quantity** $10$, **Reference price ($)** $100$, **Available bar volume** $1000$, **Bid-ask spread (bps)** $5$, **Slippage (bps)** $3$, **Commission (bps)** $5$, and **Price age (seconds)** $0$. Click **Submit buy order**. In the **ORDER AUDIT LOG**, inspect the fill record: 10 shares filled at $\$100.06$ ($100.055$), commission $\$0.50$, cash debited $\$1{,}001.05$.

            **Test the participation volume cap.** Enter **Order quantity** $150$ with volume still at $1000$. Click **Submit buy order**. Inspect the audit log: exactly 100 shares fill (10% of volume) and the status badge reads "partially filled".

            **Deliberately trip pre-trade risk guards.** Test each protective barrier one at a time:
            1. **Stale quote guard**: Set **Price age (seconds)** to 90 and submit. The audit log rejects the order: "Price data is stale."
            2. **Wide spread guard**: Restore age to 0, set **Bid-ask spread (bps)** to 150, and submit. Rejection reads: "Spread exceeds the 100 bps guard."
            3. **Zero liquidity guard**: Restore spread to 5, set **Available bar volume** to 0, and submit. Rejection reads: "No available liquidity."
            4. **Insufficient funds guard**: Enter **Order quantity** $2000$. Rejection reads: "Insufficient cash for the simulated fill and fees."

            **Trigger the drawdown circuit breaker.** Follow the walk-through: set volume to $100{,}000$ and buy 990 shares. Then change the reference price to $\$97.00$ and attempt to submit an order. Marked equity drops to $\$96{,}926$, tripping the breaker. The **RISK STATE** badge switches to a red "Halted" indicator, and the audit log records: "Drawdown circuit breaker triggered." Any subsequent submission displays: "Circuit breaker is halted. Reset the paper account after reviewing the event."

            **Execute a formal account reset.** Click the reset icon in the header (aria "Reset paper account"), confirm the modal dialog by clicking **Reset simulation**, and verify that cash restores to $\$100{,}000$ with risk state returned to "Normal"."""
        ),
        r"P_{\text{fill}} = P_{\text{ref}}\left(1 \pm \frac{s + \frac{1}{2}\text{spread}}{10^4}\right), \qquad q_{\text{fill}} = \min(q_{\text{order}}, \, 0.10\,V), \qquad E_{\text{marked}} = \text{Cash} + q_{\text{held}} P_{\text{ref}}",
        '''
ref_price = 100.0
spread_bps = 5.0
slippage_bps = 3.0
commission_bps = 5.0

fill_price = ref_price * (1.0 + (slippage_bps + spread_bps / 2.0) / 10000.0)
print("Executed buy fill price:", fill_price)
shares_ordered = 10
fee = shares_ordered * fill_price * (commission_bps / 10000.0)
print("Commission on 10 shares:", round(fee, 4))

bar_volume = 1000
cap = bar_volume * 0.10
print("Filled shares for 150 ordered against 1,000 volume:", min(150, cap))

# Circuit breaker calculation
large_shares = 990
initial_cash = 100000.0
trade_cost = large_shares * fill_price
trade_fee = trade_cost * (commission_bps / 10000.0)
remaining_cash = initial_cash - trade_cost - trade_fee
stressed_price = 97.0
marked_equity = remaining_cash + (large_shares * stressed_price)
equity_ratio = (marked_equity / initial_cash) * 100.0

print("Remaining cash after 990 shares:", round(remaining_cash, 2))
print("Marked equity at $97 price:", round(marked_equity, 2))
print("Equity as percentage of starting capital:", round(equity_ratio, 2), "% vs 97.5% breaker threshold")
print("Breaker triggered:", equity_ratio < 97.5)
''',
        "Deliberately trigger each pre-trade guard in the Paper trading tab: participation cap, stale price guard, wide spread guard, zero liquidity guard, insufficient funds, and the drawdown circuit breaker. Transcribe each rejection message from the ORDER AUDIT LOG and explain the market risk each guard is designed to mitigate.",
        "The mock broker's pre-trade guards protect capital against specific execution failures: (1) The volume participation cap restricts fills to 10% of bar volume ('partially filled'), preventing unrealistic liquidity assumptions. (2) The stale-quote guard rejects prices older than 60 seconds with 'Price data is stale.', protecting algorithms against executing on obsolete quotes during network latency. (3) The spread guard blocks orders when spreads exceed 100 bps with 'Spread exceeds the 100 bps guard.', avoiding adverse fills during market illiquidity. (4) The liquidity guard rejects orders when volume is 0 with 'No available liquidity.' (5) The cash guard blocks unaffordable orders with 'Insufficient cash for the simulated fill and fees.' (6) The drawdown circuit breaker halts the account when marked equity drops to $96,926 (96.93% < 97.50% threshold) with 'Drawdown circuit breaker triggered.', emulating institutional kill-switches (such as SEC Rule 15c3-5) that prevent runaway algorithmic trading catastrophes like Knight Capital.",
        [
            (
                "With the default inputs, what is the buy fill price?",
                "$100.055, the reference price plus slippage and half the spread",
                "$100.00 exactly",
                "$100.08, adding the full spread and the slippage",
                "Fill price = Ref * (1 + (slippage + spread/2)/10000) = 100 * (1 + (3 + 2.5)/10000) = 100 * 1.00055 = $100.055. Only half the bid-ask spread is paid on a single side of the transaction.",
            ),
            (
                "An order for 150 shares meets 1,000 shares of available volume. What happens?",
                "100 shares fill, the order is marked partially filled and the rest is not retried",
                "All 150 shares fill at once",
                "Nothing fills until more volume appears",
                "The mock broker caps execution at 10% of available bar volume (0.10 * 1,000 = 100 shares). The unfilled 50 shares are discarded, and the order status is set to partially filled.",
            ),
            (
                "Price age is set to 90 seconds. What does the broker do?",
                "Rejects the order with 'Price data is stale.'",
                "Fills at the old reference price",
                "Waits 90 seconds and then fills",
                "The pre-trade risk engine enforces a strict 60-second quote freshness guard. If price age exceeds 60 seconds, the order is immediately rejected before touching the market.",
            ),
            (
                "After the drawdown breaker halts the account, how does trading resume?",
                "Only after resetting the paper account, once the event has been reviewed",
                "Automatically with the next order",
                "By lowering the commission",
                "When marked equity breaches the 97.5% threshold, the automated circuit breaker halts the account to prevent runaway algorithmic losses. It requires a manual post-mortem review and simulation reset to resume.",
            ),
        ],
        [KNIGHT_SEC, FLASH, IG_ORDERS],
        "broker",
        "trigger every guard on purpose, one at a time (stale price, wide spread, no volume, insufficient cash and the drawdown breaker), and copy each rejection from the ORDER AUDIT LOG.",
        "30-minute session: 7 minutes studying broker execution architecture and risk controls, 9 minutes calculating fill friction and circuit breaker equity thresholds, and 14 minutes triggering pre-trade guards in the Paper trading tab; the mock broker never connects to real exchanges.",
    )

    # ------------------------------------------------------------------ 14.10
    add(
        "The AMM simulator: pool prices, fees and impermanent loss",
        r"Model constant-product automated market makers ($x \cdot y = k$), calculate swap execution prices, fees, and price impact, and evaluate impermanent loss in full-range and concentrated liquidity positions.",
        text(
            r"""Decentralized finance (DeFi) protocols depart from traditional limit order books by deploying **Automated Market Makers (AMMs)**. Governed by deterministic smart contracts, Constant Function Market Makers (CFMMs) hold token reserves and price swaps dynamically along mathematical bonding curves rather than matching bids and offers.

            The **AMM simulator** models the foundational constant-product invariant popularized by Uniswap:
            $$x \cdot y = k$$
            where $x$ represents the reserve of Token A (e.g., ETH), $y$ represents the reserve of Token B (e.g., USDC), and $k$ is the invariant product.

            The instantaneous marginal **Spot Price** is simply the reserve ratio:
            $$P_{\text{spot}} = \frac{y}{x}$$

            However, an incoming trade alters the reserve balances, moving the price along the hyperbolic curve. When a trader deposits $\Delta x$ tokens to extract $\Delta y$ tokens subject to a liquidity provider fee $\varphi$ (default $0.3\% = 0.003$), the effective token input is $\Delta x (1 - \varphi)$. The invariant requires $(x + \Delta x(1 - \varphi))(y - \Delta y) = k = xy$.
            Solving for the swap output $\Delta y$:
            $$\Delta y = \frac{y \cdot \Delta x (1 - \varphi)}{x + \Delta x (1 - \varphi)}$$
            The **Effective Execution Price** obtained by the trader is $P_{\text{exec}} = \frac{\Delta y}{\Delta x}$, and the **Price Impact** (including the fee) is:
            $$\text{Price Impact} = 1 - \frac{P_{\text{exec}}}{P_{\text{spot}}}$$

            For liquidity providers (LPs), depositing assets exposes capital to **Impermanent Loss (IL)**. When the broader market price shifts, arbitrageurs trade against the pool until its internal spot price matches external market quotes. This arbitrage drains the appreciating asset from the pool, leaving LPs with a portfolio worth less than if they had simply held the original tokens in a private wallet.
            For a full-range liquidity position, impermanent loss is a pure function of the price ratio $r = P_{\text{new}} / P_{\text{initial}}$:
            $$\text{IL}(r) = \frac{2\sqrt{r}}{1 + r} - 1$$

            **Concentrated Liquidity** (Uniswap v3 style) allows LPs to bound their capital within an active price range $[p_a, p_b]$. While this concentration amplifies fee income per dollar of capital, it equally amplifies impermanent loss: the position rebalances more aggressively, and if price breaches either bound, the position converts entirely into the depreciating asset and stops earning fees. (Note: the simulator's comparative analysis excludes accumulated fee earnings and gas costs)."""
        ),
        text(
            r"""To quantify AMM mechanics, examine the default liquidity pool configuration:
            Reserves $x = 10\text{ ETH}$ and $y = 20{,}000\text{ USDC}$.
            The marginal spot price is:
            $$P_{\text{spot}} = \frac{20{,}000\text{ USDC}}{10\text{ ETH}} = 2{,}000\text{ USDC per ETH}$$
            The swap fee is $\varphi = 0.003$ ($0.3\%$).

            Evaluate a swap of $\Delta x = 1\text{ ETH}$ for USDC:
            The net token input after the $0.3\%$ fee is $\Delta x(1 - \varphi) = 1.0 \times 0.997 = 0.997\text{ ETH}$.
            Applying the constant-product swap formula:
            $$\Delta y = \frac{20{,}000 \times 0.997}{10 + 0.997} = \frac{19{,}940}{10.997} \approx 1{,}813.2218\text{ USDC}$$
            The trader deposits $1\text{ ETH}$ and receives approximately $1{,}813.22\text{ USDC}$.
            The effective execution price is:
            $$P_{\text{exec}} = \frac{1{,}813.2218}{1.0} \approx \$1{,}813.22\text{ per ETH}$$
            The total price impact incurred is:
            $$\text{Price Impact} = 1 - \frac{\$1{,}813.22}{\$2{,}000.00} = 1 - 0.90661 = 0.09339 \approx 9.34\%$$
            The fee retained by the pool is $0.003\text{ ETH} \times 2{,}000 = \$6.00$ in notional value.

            Now compare swap sizes to observe non-linear impact scaling:
            - **Swap 0.1 ETH**: $\Delta y \approx 197.43\text{ USDC} \implies P_{\text{exec}} \approx \$1{,}974.32 \implies \text{Impact} \approx 1.28\%$
            - **Swap 1.0 ETH**: $\Delta y \approx 1{,}813.22\text{ USDC} \implies P_{\text{exec}} \approx \$1{,}813.22 \implies \text{Impact} \approx 9.34\%$
            - **Swap 5.0 ETH**: $\Delta y \approx 6{,}653.32\text{ USDC} \implies P_{\text{exec}} \approx \$1{,}330.66 \implies \text{Impact} \approx 33.47\%$
            Because the bonding curve steepens as reserves diminish, price impact grows exponentially rather than linearly with order size.

            Next, analyze **Impermanent Loss**:
            Suppose external market prices double ($r = 2.0$, ETH reaches $\$4{,}000$).
            Full-range impermanent loss is:
            $$\text{IL}(2.0) = \frac{2\sqrt{2}}{1 + 2} - 1 = \frac{2 \times 1.41421}{3} - 1 = \frac{2.82843}{3} - 1 \approx -0.05719 \approx -5.72\%$$
            The LP's pool holdings are worth $5.72\%$ less than holding the original 10 ETH and 20,000 USDC.

            Now examine a **Concentrated Liquidity Position** bounded between $0.5\times$ and $2.0\times$ ($[1{,}000, 4{,}000]\text{ USDC}$):
            At $r = 2.0$, the concentrated position incurs an impermanent loss of approximately $-19.53\%$ relative to holding—more than three times the divergence loss of full-range liquidity! Furthermore, at $2.0\times$, the position reaches the upper bound and converts 100% into USDC, ceasing to generate swap fees."""
        ),
        text(
            r"""**Navigate to the AMM simulator.** Click the **AMM simulator** tab. The header reads "CONSTANT-PRODUCT POOL: Explore an ETH / USDC pool with x · y = k." Inspect the baseline inputs: **ETH reserves** ($10$), **USDC reserves** ($20000$), **ETH to swap** ($1$), and **Swap fee (decimal)** ($0.003$).

            **Audit swap output and execution price.** Review the calculated quote metrics:
            - **Estimated swap output**: $\approx 1,813.22\text{ USDC}$
            - **Execution price**: $\approx \$1,813.22\text{ per ETH}$
            - **Price impact including fee**: $\approx 9.34\%$
            - **Fee retained by pool**: $0.003\text{ ETH}$ ($\approx \$6.00$)

            **Analyze non-linear price impact.** Change **ETH to swap** to $0.1$. Observe output of $197.43\text{ USDC}$ and price impact of $1.28\%$. Now enter $5\text{ ETH}$: output reaches $6,653.32\text{ USDC}$ with a massive price impact of $33.47\%$. Notice how large trades suffer severe slippage relative to pool depth.

            **Evaluate impermanent loss across price moves.** Locate the **LIQUIDITY PROVIDER ANALYSIS** section. Drag **Future price / initial price** from $1.00\times$ up to $2.00\times$. Inspect the performance readouts:
            - **Full-range impermanent loss**: $-5.72\%$
            - **Concentrated position vs. holding**: $-19.53\%$
            - **Position status**: "At range upper bound"
            Now drag the price ratio to $0.50\times$: confirm that full-range loss is again $-5.72\%$, while the concentrated position hits the lower bound. Drag the price ratio to $4.00\times$: full-range loss reaches $-20.00\%$.

            **Manipulate concentrated liquidity boundaries.** Under **Concentrated liquidity range**, adjust **Lower price ratio** and **Upper price ratio**. Narrow the range: observe how divergence loss accelerates. Now attempt to set the lower ratio to $1.2\times$: the tool displays an alert: "The starting price must lie within the liquidity range."

            **Read the impermanent loss curve.** Inspect the interactive chart under **LIQUIDITY PROVIDER ANALYSIS**: trace the curve from $0.1\times$ to $5.0\times$, observing that impermanent loss is zero strictly when the price ratio equals $1.0\times$."""
        ),
        r"\Delta y = \frac{y \cdot \Delta x (1 - \varphi)}{x + \Delta x (1 - \varphi)}, \qquad P_{\text{exec}} = \frac{\Delta y}{\Delta x}, \qquad \text{IL}(r) = \frac{2\sqrt{r}}{1 + r} - 1",
        '''
from math import sqrt

eth_reserves = 10.0
usdc_reserves = 20000.0
fee = 0.003
spot_price = usdc_reserves / eth_reserves
print("Initial pool spot price:", round(spot_price, 2), "USDC/ETH")

for swap_eth in [0.1, 1.0, 5.0]:
    effective_input = swap_eth * (1.0 - fee)
    out_usdc = (usdc_reserves * effective_input) / (eth_reserves + effective_input)
    exec_price = out_usdc / swap_eth
    impact = (1.0 - exec_price / spot_price) * 100.0
    print("Swap", swap_eth, "ETH -> Output:", round(out_usdc, 2), "USDC | Exec Price:", round(exec_price, 2), "| Impact:", round(impact, 2), "%")

for r in [0.5, 2.0, 4.0]:
    il_full = (2.0 * sqrt(r) / (1.0 + r) - 1.0) * 100.0
    print("Price ratio", r, "x -> Full-range impermanent loss:", round(il_full, 2), "%")
''',
        "Quote swaps of 0.1, 1.0, and 5.0 ETH in the default 10 ETH / 20,000 USDC pool, recording output USDC, execution price, and price impact for each. Then record full-range and concentrated impermanent loss at price ratios of 0.5x, 2.0x, and 4.0x, and explain why concentrated liquidity amplifies divergence loss.",
        "In the default pool (10 ETH, 20,000 USDC, spot 2,000 USDC/ETH, fee 0.3%), a 0.1 ETH swap yields 197.43 USDC (exec price $1,974.32, impact 1.28%); a 1.0 ETH swap yields 1,813.22 USDC (exec price $1,813.22, impact 9.34%); and a 5.0 ETH swap yields 6,653.32 USDC (exec price $1,330.66, impact 33.47%), illustrating that price impact accelerates non-linearly with order size along x*y=k. Full-range impermanent loss reaches -5.72% at both 0.5x and 2.0x price ratios, and -20.00% at 4.0x. A concentrated liquidity position bounded in [0.5x, 2.0x] suffers -19.53% loss at 2.0x (more than 3.4x the full-range loss) because concentrating liquidity within a narrow band provides the depth of a much larger pool within that interval, causing arbitrageurs to drain the appreciating asset at an accelerated rate until the boundary is reached.",
        [
            (
                "Why does swapping 1 ETH into a 10 ETH / 20,000 USDC pool return only about 1,813 USDC?",
                "The trade moves the price along x · y = k, and the 0.3% fee is kept by the pool",
                "The pool charges a fixed 187 USDC fee on every swap",
                "The spot price is 1,813 USDC per ETH",
                "While the pre-trade spot price is 2,000 USDC/ETH, the trade shifts the reserve ratio along the constant-product curve x * y = k, and 0.3% of the input is retained as a liquidity fee: Output = 20,000 * 0.997 / (10 + 0.997) ≈ 1,813.22 USDC.",
            ),
            (
                "What is the full-range impermanent loss if the ETH price doubles?",
                "About −5.72% against simply holding",
                "−50%, half the value",
                "Zero, because the price went up",
                "Impermanent loss at price ratio r = 2.0 is IL(2) = 2*sqrt(2)/(1 + 2) - 1 ≈ 2.8284/3 - 1 ≈ -5.72% relative to holding the original token inventory outside the pool.",
            ),
            (
                "Why does the concentrated position lose about 19.53% while the full-range position loses 5.72% at the same move?",
                "Concentrated liquidity acts like a larger position inside its range, so the same move rebalances it harder",
                "Concentrated liquidity pays higher swap fees",
                "The concentrated calculation includes gas costs",
                "Concentrating liquidity within a narrow range [0.5x, 2.0x] provides the market depth of a substantially larger pool within that interval, accelerating the rate at which external arbitrageurs drain the appreciating token.",
            ),
            (
                "What do the simulator's comparisons with holding leave out?",
                "Fees earned by the pool and gas costs",
                "The pool's reserves",
                "The price ratio",
                "The simulator models raw divergence loss against a buy-and-hold benchmark, omitting accumulated trading fee yields and blockchain network transaction (gas) costs.",
            ),
        ],
        [UNISWAP, ANGERIS],
        "amm",
        "quote swaps of 0.1, 1 and 5 ETH, record each execution price and impact, then move the price slider from 0.5× to 4× and note where the concentrated position leaves its range.",
        "30-minute session: 8 minutes studying automated market maker bonding curves and constant-product mathematics, 10 minutes working through swap output and impermanent loss equations, and 12 minutes testing liquidity parameters in the AMM simulator; all pool interactions model decentralized protocols.",
    )

    # ------------------------------------------------------------------ 14.11
    add(
        "Saved experiments, the notebook and historical imports",
        "Archive and restore reproducible experiment artifacts, maintain contemporaneous quantitative logs in My Notebook, and understand point-in-time chronological sampling in historical dataset imports.",
        text(
            r"""Open, verifiable computational science requires that any reported finding can be perfectly reproduced by an independent researcher. In quantitative trading, claiming a Sharpe ratio without preserving the exact strategy source code, random seed, execution costs, and data-generating parameters is scientifically void. The Strategy lab implements an auditable research architecture built on **Saved experiments**, **My notebook**, and **Historical data imports**.

            A **Saved experiment** archives a lightweight, self-contained parameter manifest. Rather than storing millions of raw price ticks, equity curves, or trade logs, the lab saves the exact input configuration dictionary:
            - Full Python strategy code.
            - Data source and stochastic process specification.
            - Named stress scenario selection.
            - Annual drift and volatility settings.
            - Trading horizon and pseudorandom seed.
            - Indicator lookback parameters (e.g., SMA window).
            - Initial portfolio equity.
            - Commission (bps) and slippage (bps) friction.
            - Performance metrics at the time of archival (if fresh).

            Because the simulation engine is fully deterministic, reopening an experiment regenerates the exact tick series, equity curves, and trade blotters on demand from the random seed. Saving from the interactive sandbox creates a new versioned entry in browser local storage (synced to cloud storage when logged in). Only experiments reopened directly from **Saved experiments** allow in-place updating.

            Researchers must understand two crucial operational behaviors:
            1. **Tab Navigation Reset**: Clicking between lab tabs clears the active experiment ID from the URL. Returning to the Market sandbox returns you to the unlinked "free lab" sandbox. Always reopen experiments from the **Saved experiments** repository.
            2. **Draft Precedence**: If you edit strategy code without saving, the uncommitted code is preserved as an active draft in local storage. When reopening the experiment, this draft takes precedence. To discard modifications and restore the archived code, click the **Restore lesson code** icon.

            Finally, the engine supports **Historical data imports**. When a historical CSV dataset is loaded, the backtest slices the earliest $H \times 252$ trading rows from the file, maintaining point-in-time causality by advancing forward from past data rather than sampling backwards from the present."""
        ),
        text(
            r"""To analyze historical data slicing, consider an imported dataset comprising 10 years of daily equity data ($N_{\text{rows}} = 2{,}520\text{ bars}$).
            If the researcher configures a 3-year trading horizon ($H = 3$), the backtest requires:
            $$\text{Rows Processed} = 252 \times H = 252 \times 3 = 756\text{ bars}$$
            The engine reads rows $1$ through $756$—representing the oldest three chronological years in the historical dataset. The remaining $2{,}520 - 756 = 1{,}764\text{ rows}$ (7 years of recent price history) are left untouched. To backtest a more recent market period, the imported file must be formatted to start on the desired start date.

            Now examine the lightweight storage footprint of `quanta-experiment.json`.
            A complete experiment record consumes less than $4\text{ KB}$ of JSON metadata:
            - Complete Python source code string.
            - 11 configuration fields: data type, process, scenario, drift ($0.08$), volatility ($0.20$), horizon ($3$), seed ($42$), capital ($\$100{,}000$), commission ($5$), slippage ($3$), and SMA window ($50$).
            - Verified output metrics: CAGR ($-0.0850$), Sharpe ($-0.9200$), Max Drawdown ($-0.2707$), Win Rate ($0.1724$), and Total Trades ($59$).

            When another researcher downloads this JSON artifact, they do not need to download multi-gigabyte tick databases. By running the identical script against seed 42 with default costs, their machine deterministically recreates the exact $\$76{,}598.46$ equity curve and all 59 trade executions, validating computational reproducibility."""
        ),
        text(
            r"""**Save an experiment from the sandbox.** In the **Market sandbox**, execute the baseline trend rule on seed 42. In the footer toolbar, click **Save**. In the "Keep this experiment" modal dialog, enter an **Experiment name** (e.g., "Baseline Trend SMA-50 Seed 42") and click **Save experiment**. Then click the **Export experiment** icon to download `quanta-experiment.json`.

            **Reopen and verify the experiment.** In the main navigation sidebar, click **Saved experiments**. In the experiment repository, locate your newly saved experiment card. Inspect the metadata tags: "Synthetic data", "Geometric Brownian motion", "Seed 42", CAGR $-8.5\%$, and Max Drawdown $-27.1\%$. Click the experiment title: the Market sandbox opens with the experiment name prominently displayed in the header. Click **Run experiment** and confirm that all metrics match the card values perfectly.

            **Observe draft precedence.** While viewing the opened experiment, modify `strategy.py` by inserting a comment: `# Draft modification`. Refresh the browser: observe that your edited code remains in the editor. Now click the **Restore lesson code** icon above the editor: the editor immediately resets back to the saved, unedited experiment code.

            **Maintain research notes in My notebook.** Click **My notebook** in the sidebar. Click **New note**, enter a title ("Hypothesis 1: Seed 42 Baseline"), type your experimental observations, and click **Save note**. Next, return to this lesson and locate the assignment section: click the **Write in notebook** button. A prefilled note opens automatically, populated with the assignment prompt. Complete the note and save it. Finally, click **Export notebook** to download your full research journal as `quanta-notebook.md`.

            **Inspect historical data configuration.** In the sandbox **Parameters** tab, open the **DATA SOURCE** dropdown and select **Historical data**. Read the informational notice explaining how historical CSV files are imported and sliced chronologically."""
        ),
        r"n_{\text{rows}} = 252 \times H, \qquad \text{Rows Used} = \{1, 2, \dots, 252H\}, \qquad \text{Manifest} = \{\text{Code}, \text{Params}, \text{Seed}, \text{Metrics}\}",
        '''
horizon_years = 3
rows_in_file = 2520
rows_used = 252 * horizon_years
rows_remaining = rows_in_file - rows_used
years_skipped = rows_remaining / 252.0

print("Total rows in imported file:", rows_in_file)
print("Rows used by 3-year backtest:", rows_used)
print("Chronological rows preserved for out-of-sample testing:", rows_remaining)
print("Years of data preserved:", years_skipped)

saved_fields = [
    "strategy_code", "data_source", "stochastic_process", "scenario",
    "annual_drift", "annual_volatility", "horizon_years", "seed",
    "initial_capital", "commission_bps", "slippage_bps"
]
print("Essential configuration parameters in quanta-experiment.json:", len(saved_fields))
''',
        "Save two distinct experiments that differ only by random seed (seed 42 and seed 43). Export both JSON files, reopen each from Saved experiments, and verify that executing a fresh run reproduces the card's CAGR and maximum drawdown exactly. In your notebook, list the essential configuration parameters required for an outsider to replicate your findings.",
        "Each saved experiment stores its Python strategy code alongside its complete configuration dictionary (data source, process, scenario, drift, volatility, horizon, seed, initial capital, commission, and slippage). When reopened, the engine draws the identical pseudorandom sequence from the seed, deterministically regenerating the identical 756 bars and matching the card metrics (Seed 42: CAGR -8.5%, MDD -27.1%; Seed 43: CAGR +1.6%, MDD -21.4%). The exported JSON files differ only in the seed field and the resulting performance metrics. An external researcher requires only these 11 parameters and the code to replicate the backtest bit-for-bit on any machine, embodying the computational reproducibility standards established by the Turing Way and PLOS Computational Biology.",
        [
            (
                "What does a saved experiment store?",
                "The code and the exact market settings, plus metrics if the output was fresh",
                "Every bar, curve and trade of the run",
                "Only the experiment's name",
                "A saved experiment persists the strategy source code and configuration parameter dictionary. Because the market generator is deterministic, the full bar series, equity curve, and trade log are regenerated on demand from the random seed.",
            ),
            (
                "You open an experiment, click the Valuation tab and return to the Market sandbox. What do you see?",
                "The free lab, because a tab click drops the experiment from the address",
                "The same experiment, unchanged",
                "An error page",
                "Navigating between lab tool tabs resets URL query parameters, returning the Market sandbox to its unlinked 'free lab' state. You can reopen your saved work at any time from the Saved experiments repository.",
            ),
            (
                "An imported dataset has 2,520 daily rows and Horizon is 3 years. Which rows does a run use?",
                "The first 756 rows, the oldest three years in the file",
                "The last 756 rows, the most recent three years",
                "All 2,520 rows",
                "When evaluating an imported time series, the backtest processes the first Horizon * 252 rows (rows 1 to 756), representing the earliest chronological years in the dataset, leaving subsequent years for forward testing.",
            ),
            (
                "How do you save a lesson's assignment answer to your notebook?",
                "Click Write in notebook on the assignment, complete the prefilled note and save it",
                "Copy it into Saved experiments",
                "It is saved automatically when you pass a practice question",
                "Clicking the 'Write in notebook' button beneath any lesson assignment initializes a new note in My notebook prefilled with the prompt, ready for you to record your findings and save.",
            ),
        ],
        [TURING, PLOS, NUMPY_RANDOM],
        "market",
        "save two experiments that differ only by seed, export both JSON files, and confirm that reopening each from Saved experiments reproduces its own metrics.",
        "30-minute session: 7 minutes studying computational reproducibility and state persistence architecture, 8 minutes analyzing chronological data windowing, and 15 minutes saving, reopening, and exporting artifacts in the lab and notebook; all default data is synthetic.",
    )

    # ------------------------------------------------------------------ 14.12
    add(
        "Capstone: a complete research loop from hypothesis to saved evidence",
        "Execute the complete 12-stage Quanta Research Loop from pre-registered hypothesis to archived evidence, separating development seeds from reserved test seeds to produce an honest, peer-reviewable study.",
        text(
            r"""The culmination of the Strategy lab workshop is executing an end-to-end scientific research project. The difference between an amateur backtester and an institutional quantitative researcher lies not in the complexity of their code, but in the integrity of their experimental methodology. Amateurs test dozens of variations, discard losing runs, and report the best backtest curve as if it were foreseen. Quantitative scientists formulate falsifiable hypotheses, pre-register rejection thresholds, separate development data from out-of-sample test data, and account for every trial executed.

            The capstone synthesizes the **12-Step Quanta Research Loop**:
            1. **Pre-registered Hypothesis**: State an unambiguous, testable proposition prior to running simulations.
            2. **Target Metric**: Select primary performance indicators (e.g., Maximum Drawdown, CAGR, Sharpe ratio).
            3. **Hurdle Benchmark**: Establish an explicit opportunity cost benchmark (e.g., passive Buy & Hold).
            4. **Falsification Threshold**: Pre-register quantitative criteria that would force rejection of the hypothesis.
            5. **Seed Partitioning**: Partition random seeds into in-sample development seeds ($42\text{--}46$) and untouched out-of-sample reserved test seeds ($47\text{--}51$).
            6. **Parameter Discipline**: Fix market environment and transaction friction parameters ($5\text{ bps}$ commission, $3\text{ bps}$ slippage).
            7. **Iterative Development**: Test indicator variations strictly across development seeds.
            8. **Trial Ledger Archival**: Save all development runs in **Saved experiments**, documenting every iteration.
            9. **Single Confirmation Run**: Execute the selected strategy model exactly once across the reserved test seeds.
            10. **Objective Decision**: Evaluate the pre-registered rejection threshold strictly against reserved-seed results.
            11. **Artifact Export**: Export research artifacts (`quanta-notebook.md` and experiment JSON manifests).
            12. **Boundary Disclosures**: Transparently report model limitations (synthetic data, frictionless liquidity, long-only constraints).

            The out-of-sample discipline enforced by seed partitioning is paramount: parameters tuned on development seeds are optimistic by construction. The reserved seeds have played no role in parameter selection, providing an unbiased assessment of strategy generalization."""
        ),
        text(
            r"""To anchor this capstone, execute the following pre-registered research plan:

            **Hypothesis**: Under the "Liquidity crisis · 2008-inspired" scenario (Heston stochastic volatility, annual decline of $-18\%$, annual volatility of $55\%$), augmenting the baseline 50-day trend rule with a 200-day moving average regime filter (`(close > sma_50) & (sma_50 > sma_200)`) produces a shallower maximum drawdown than the Buy & Hold benchmark on at least 4 out of 5 reserved test seeds.

            **Experimental Ledger**:
            - You evaluate two strategy variants across 5 development seeds (seeds 42, 43, 44, 45, and 46):
              Variant A: 50-day trend filter alone ($5\text{ runs}$).
              Variant B: 50-day trend filter with 200-day regime confirmation ($5\text{ runs}$).
              Development trials: $2 \times 5 = 10\text{ runs}$.
            - You select Variant B based on superior drawdown mitigation in development.
            - You test Variant B exactly once across the 5 reserved test seeds (seeds 47, 48, 49, 50, and 51):
              Reserved trials: $5\text{ runs}$.
            - Total experimental trials reported:
              $$N_{\text{trials}} = V \times S_{\text{dev}} + S_{\text{test}} = (2 \times 5) + 5 = 15\text{ trials}$$

            The final report catalogs all 15 trials, applies the pre-registered decision rule strictly to the reserved seeds, and exports the complete audit trail. The accompanying Python worksheet verifies completion of the 12-point research protocol, printing:
            `"Lab research loop steps: 12 of 12"`
            and confirming that the verification code remains strictly in cash."""
        ),
        text(
            r"""**Step 1: Document pre-registered hypothesis in My notebook.** Open **My notebook** and create a new note titled "Capstone Research Charter". Record your formal hypothesis, target metric (Maximum Drawdown), benchmark (Buy & Hold), rejection threshold (shallower drawdown on fewer than 4 of 5 reserved seeds), development seeds (42–46), and reserved seeds (47–51).

            **Step 2: Configure development environment.** In the **Market sandbox**, open **Parameters** and select **Liquidity crisis · 2008-inspired** from the **SCENARIO** dropdown. Confirm default costs ($5\text{ bps}$ commission, $3\text{ bps}$ slippage).

            **Step 3: Execute development sweeps.**
            - Run Variant A (`data["close"] > data["sma_50"]`) across seeds 42, 43, 44, 45, and 46. Save each run in **Saved experiments** with title "Cap-Dev-A-Seed[X]".
            - Run Variant B (`(data["close"] > data["sma_50"]) & (data["sma_50"] > data["sma_200"])`) across the same five seeds. Save each run as "Cap-Dev-B-Seed[X]".
            - Compare development results: Variant B demonstrates superior drawdown mitigation during severe volatility spikes.

            **Step 4: Execute the single out-of-sample confirmation test.** Without altering code or scenario parameters, evaluate Variant B across reserved seeds 47, 48, 49, 50, and 51. Save each test run as "Cap-Test-B-Seed[X]".

            **Step 5: Apply the objective decision rule.** Tabulate maximum drawdown for Variant B versus Buy & Hold across seeds 47–51. If Variant B achieves a shallower drawdown on 4 or more seeds, the hypothesis is confirmed; otherwise, it is rejected. Document the final verdict in your notebook.

            **Step 6: Export audit trail.** In **Saved experiments**, confirm that all 15 trials are archived with appropriate seed tags. Export the JSON manifests for the five confirmation tests. In **My notebook**, click **Export notebook** to download `quanta-notebook.md`.

            **Step 7: Verify completion via worksheet.** Open the lesson worksheet under **Try the lesson template**. Click **Run in sandbox** followed by **Run experiment**. The **Console** prints the verification checklist:
            "Trials to report: 15"
            "Lab research loop steps: 12 of 12"."""
        ),
        r"N_{\text{trials}} = V \times S_{\text{dev}} + S_{\text{test}}, \qquad \text{Decision} = \sum_{s \in S_{\text{test}}} \mathbf{1}_{\{\text{MDD}_{\text{rule}, s} > \text{MDD}_{\text{hold}, s}\} } \ge 4",
        '''
variants = 2
development_seeds = 5
reserved_seeds = 5
trials = variants * development_seeds + reserved_seeds
print("Trials to report:", trials)

steps = [
    "hypothesis", "metric", "comparison", "rejection criterion", "seeds split",
    "settings fixed", "development runs", "experiments saved", "reserved test",
    "decision", "trail exported", "limits stated"
]
print("Lab research loop steps:", len(steps), "of", 12)
''',
        "Execute a complete scientific research loop in the Strategy lab: document your hypothesis and falsification threshold in My notebook prior to execution, develop across seeds 42–46, test once across reserved seeds 47–51, archive all 15 trials, and export your research trail. State your final decision and model limitations.",
        "A complete capstone presents an auditable research journal containing the pre-registered hypothesis and rejection threshold timestamped prior to simulation. The trial ledger documents all 10 development runs across seeds 42-46 alongside the 5 confirmation runs on reserved seeds 47-51. Under the 2008 liquidity crisis scenario, the dual-moving-average trend filter (Variant B) achieved a shallower maximum drawdown than buy-and-hold across 5 of the 5 reserved seeds (averaging ~ -38.2% vs -64.1%), successfully confirming the pre-registered hypothesis. The report exports the full notebook markdown and JSON manifests, transparently disclosing critical limitations: the strategy was evaluated on synthetic stochastic paths, assumes fixed slippage and infinite liquidity, trades long-or-cash only, and does not establish an exploitable edge in live financial markets.",
        [
            (
                "Which statement is a testable hypothesis for the lab?",
                "A 200-day filter gives a shallower maximum drawdown than buy and hold on at least four of five reserved seeds in the 2008-inspired scenario",
                "Trend following is a good strategy",
                "This rule will make money",
                "A scientifically valid hypothesis identifies the exact strategy rule, benchmark comparison, target metric, pre-registered rejection threshold, and specific stress scenario, enabling unambiguous empirical verification.",
            ),
            (
                "Why keep some seeds untouched until the end?",
                "They act as a fresh test that played no part in your choices",
                "Reserved seeds run faster",
                "The lab allows only five seeds a day",
                "Iterative parameter tuning inevitably optimizes for the specific random paths encountered during development. Reserving untouched seeds ensures an unbiased, out-of-sample evaluation on unobserved market paths.",
            ),
            (
                "Your final rule beats buy and hold on the reserved seeds. What can you claim?",
                "It held up on fresh synthetic paths under the stated settings, which is not evidence of a real-market edge",
                "It will beat the real market",
                "It carries no risk",
                "Successfully passing a confirmation test on synthetic stochastic data verifies internal algorithmic logic and drawdown mitigation mechanics under defined assumptions, but cannot guarantee an edge in live financial markets.",
            ),
            (
                "What belongs in the research trail besides the winning experiment?",
                "Every variant tried, with its seed, settings and result, including failures",
                "Only the best run",
                "Only screenshots of the charts",
                "An honest scientific research log records every trial executed—including discarded parameters and negative results—enabling peer reviewers to evaluate multiple-testing adjustments and verify reproducibility.",
            ),
        ],
        [PBO, TURING, PLOS],
        "market",
        "run your capstone loop: write the hypothesis and criterion first, develop on five seeds, test on five reserved seeds, save every run and export your notebook.",
        "30-minute session: 5 minutes reviewing research loop governance, 5 minutes pre-registering hypotheses and seed splits, and 20 minutes executing, archiving, and exporting the capstone project in the Market sandbox; the capstone evaluates quantitative methodology rather than market forecasting.",
    )

    parts = [
        (
            "The market sandbox",
            "Tour the lab, generate markets, write strategies and see how a backtest trades.",
        ),
        (
            "Read evidence and value businesses",
            "Metrics and trade logs, balance-sheet valuation, factor regressions and robustness checks.",
        ),
        (
            "Execution, DeFi and your research trail",
            "Paper-broker guards, constant-product pools, saved experiments, the notebook and a complete research loop.",
        ),
    ]
    track = finish(
        {
            "id": "lab-workshop",
            "number": 14,
            "title": "Strategy lab workshop",
            "description": "Learn every tool on the Strategy lab page, from generating a synthetic market and backtesting a Python rule to valuation, factor regressions, paper trading, liquidity pools and saved research.",
            "source": "Original Quanta course · Quanta Strategy lab documentation, Python, statsmodels, Uniswap, SEC & CFA Institute references",
            "level": "Beginner → intermediate",
            "icon": "lab",
            "studyType": "applied",
            "modules": modules,
            "prerequisites": "Complete Trading & market fundamentals first. Basic arithmetic is enough: Python, valuation and factor regression are introduced from scratch in this course.",
            "outcomes": [
                "Operate all five Strategy lab tools, Saved experiments and My notebook without hunting for controls.",
                "Generate reproducible synthetic markets and explain how process, scenario, horizon and seed shape a result.",
                "Write a long-or-cash rule in the guided Python runtime and avoid its limits and look-ahead traps.",
                "Read the four cards, the output tabs and all 14 metrics, and say what a backtest does and does not show.",
                "Value a balance sheet with haircuts, fit a factor model with robust errors, test orders against paper-broker guards and quote a liquidity-pool swap.",
                "Stress a result against costs, seeds and scenarios, then save the experiment and your reasoning as a reproducible trail.",
            ],
            "readingGuide": "The workshop has 12 lessons × 30 minutes = 6 hours of planned study across three units: about 8 minutes of reading, 10 minutes of arithmetic and 12 minutes in the lab per lesson; exam time is additional. It includes 24 practice questions, three four-question checkpoints and a 12-question final. The lab's default data is synthetic, so every price, company and result is a teaching device; a good simulated result is never evidence of a real edge, and the paper broker and AMM never touch real money.",
            "parts": [
                {"id": str(i), "title": t, "description": d} for i, (t, d) in enumerate(parts, 1)
            ],
            "references": [
                {"title": t, "url": u} for t, u in [PBO, DSR, TURING, NUMPY_RANDOM, PY_FLOW]
            ],
            "resources": [],
        },
        checkpoints_for(modules, parts, 3),
    )
    track["exams"][-1]["version"] = 1
    return track
