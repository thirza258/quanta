"""Strategy lab workshop: a hands-on course for every tool on the /lab page."""

from applied_courses import checkpoints_for, study
from book_courses import finish

# Every URL below was fetched with .research-work/page.py: HTTP 200 and the keyword matched.
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


def prose(*paragraphs):
    """Join paragraphs; whitespace inside a paragraph is normalised so source lines can wrap."""
    return "\n\n".join(" ".join(p.split()) for p in paragraphs)


def practise(tool, task):
    """The shared closing section of every lesson."""
    return prose(
        "### Practise in the lab",
        f"""Open the [{LAB_TOOLS[tool]}](/lab?tool={tool}) and {task} The worksheet on this
        page is only an arithmetic aid: it stays in cash and does not run your experiment, so take
        every result that matters from the lab itself. The lab's default data is synthetic, so a good
        result there is a reason to test harder, never evidence of a real edge. Finish by writing
        what you changed, what you saw and what you would test next in [My notebook](/notebook).""",
    )


COURSE_GUIDE = (
    "Learn to use every tool on the Strategy lab page, from a synthetic-market backtest to a paper broker and a liquidity pool, and to keep an honest research trail.",
    "The Strategy lab is a bench for testing ideas, not a place to make money. This workshop takes each tool one control at a time: how the lab generates a market, how a one-line Python rule becomes trades, what the metrics and charts say, how a balance sheet becomes a value per share, what a factor regression can and cannot show, why a broker refuses some orders, and how a liquidity pool moves its price. The lab's default data is synthetic, so every result is a teaching device and a strong backtest is a reason to test harder, never evidence of a real edge. Each lesson takes thirty minutes: read, reproduce the arithmetic by hand, then repeat it in the lab and write down what you saw.",
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
        "Name the five tools on the Strategy lab page, run the default experiment, and use the four-step research loop to read one result honestly.",
        prose(
            """The Strategy lab is a research bench: a place to test an idea against assumptions you
            control, not a trading account. One page holds five tools. The Market sandbox runs a
            Python rule on a generated market. Valuation turns balance-sheet numbers into per-share
            values. The Factor studio fits a regression to returns whose true exposures are known.
            Paper trading sends one order at a time to a mock broker with safety guards. The AMM
            simulator follows a constant-product liquidity pool. Two companion pages keep your work:
            Saved experiments stores the code and settings of a run, and My notebook stores your
            reasoning.""",
            """The lab is built around a loop: state a hypothesis you could disprove, change one
            assumption, read the evidence, and keep a research trail. The default data is synthetic
            and generated from a seed, so the same settings always give the same bars and every
            change is a controlled comparison. That is also the lab's limit. A synthetic market has no
            real news, companies or crowds, so a good result shows that your mechanics work, never
            that an edge exists. The display below is the comparison we use throughout: a rule's
            total return against holding the same market.""",
        ),
        prose(
            """Take the hypothesis printed beside the sandbox: a trend rule reduces drawdown in a
            persistent bear regime. The default market is a three-year geometric Brownian motion
            path with 8% drift and 20% volatility, seed 42, $100,000 of starting capital, 5 bps
            commission and 3 bps slippage. That path happens to fall, from about 100 to about 81.70.
            With the default rule (hold when the close is above its 50-bar average), expect roughly
            these results: final equity near $76,598, so R = 76,598 ÷ 100,000 − 1 ≈ −23.4%, and a
            MAX DRAWDOWN near −27.1%.""",
            """Now compare with holding. The Buy & hold quick-strategy chip finishes near $81,536, so
            R ≈ 81,536 ÷ 100,000 − 1 ≈ −18.5%, with a maximum drawdown near −34.2%. The rule's return
            gap is ΔR ≈ −23.4% − (−18.5%) = −4.9 percentage points, but its worst fall was about
            34.2 − 27.1 = 7.1 points shallower. The evidence is mixed and comes from one path: the
            hypothesis holds on drawdown, fails on return, and says nothing yet about other seeds,
            costs or scenarios. That is exactly what the next steps of the loop are for.""",
        ),
        prose(
            """**Open the lab.** In the sidebar choose **Strategy lab**. The heading reads “Ideas
            become clearer when you test them.” and five tabs sit beneath it: **Market sandbox**,
            **Valuation**, **Factor studio**, **Paper trading** and **AMM simulator**. Click each one
            and watch the address change to `/lab?tool=` followed by market, valuation, factors,
            broker or amm. Switching tabs discards the tool you leave, including its results, inputs
            and paper account, so write down any number you need before you click away. Only strategy
            code is kept, as a draft.""",
            """**Start from the default rule.** Click **Market sandbox**, then **strategy.py**. The
            editor should show `return data["close"] > data["sma_50"]`. If it does not, an earlier
            visit left a draft: open **Parameters** and click the **Trend following** chip under
            QUICK STRATEGY, or click the **Restore lesson code** icon above the editor.""",
            """**Run the experiment.** Click **Run experiment**, or press Ctrl+Enter or Cmd+Enter
            with the cursor in the editor. Under EXPERIMENT OUTPUT read the four cards: CAGR, SHARPE,
            MAX DRAWDOWN and WIN RATE. With the default settings, expect roughly −8.5%, −0.92, −27.1%
            and 17.2%. Open **All metrics** and find “total return” near −0.2340 and “trades” at
            59.0000, then open **Console**: it ends with a line like “756 bars · 59 fills · final
            equity $76,598.46”.""",
            """**Compare with holding.** Click **Parameters**, then the **Buy & hold** chip, then
            **Run experiment**. MAX DRAWDOWN should read about −34.2% and “total return” in **All
            metrics** about −0.1846. The chip is a strategy that returns True on every bar, so it
            enters one bar later than the dashed Buy & hold line on the **Equity curve** and differs
            from it by a hair. Click the **Trend following** chip to restore the rule.""",
            """**Read the loop.** Beside the sandbox, the panel THE RESEARCH LOOP lists four steps:
            State a hypothesis, Change one assumption, Read the evidence and Keep a research trail.
            Write the hypothesis you just tested as one sentence that a result could prove wrong.""",
            """**Meet the lesson worksheet.** Every lesson also has a worksheet under Try the lesson
            template. Click **Run in sandbox**, then **Run experiment**: the Console prints the
            lesson's arithmetic, while the cards show CAGR 0.0%, SHARPE —, MAX DRAWDOWN 0.0% and WIN
            RATE — because the worksheet's strategy stays in cash. It is an arithmetic aid; real
            experiments belong in the lab.""",
            """**See where work is kept.** Click **Saved experiments** at the top right of the lab
            page, then **My notebook** in the sidebar. On a new workspace they show “An idea is worth
            revisiting.” and “Make space for a good question.”""",
            """**What you should see.** A losing default run is normal in this market. The chart
            legend shows SYNTHETIC DATA, and the panel beside the sandbox says “Default data is
            synthetic.” Our figures were computed with the same code as the lab, so a small
            difference usually means a changed setting: check the seed and the costs first.""",
        ),
        r"R=\frac{E_{\text{final}}}{E_{0}}-1,\qquad \Delta R=R_{\text{rule}}-R_{\text{hold}}",
        '''
capital = 100000
rule_final = 76598.46
hold_final = 81536.23
rule_return = rule_final / capital - 1
hold_return = hold_final / capital - 1
print("Rule total return:", round(rule_return, 4))
print("Buy and hold total return:", round(hold_return, 4))
gap = (rule_return - hold_return) * 100
print("Return gap in percentage points:", round(gap, 1))
rule_drawdown = -0.2707
hold_drawdown = -0.3418
shallower = (rule_drawdown - hold_drawdown) * 100
print("Drawdown advantage in percentage points:", round(shallower, 1))
print("Shallower drawdown on this path:", rule_drawdown > hold_drawdown)
fills = 59
sells = fills // 2
print("Buys:", fills - sells, "Sells:", sells)
''',
        "Write a short research note for the default run: one hypothesis about the trend rule that a result could disprove, the single assumption you will change first, the four card values, the Buy & hold maximum drawdown and total return, and one result that would make you drop the hypothesis.",
        "A good note names a testable claim, for example: the 50-bar trend rule has a shallower maximum drawdown than Buy & hold on synthetic GBM markets. It records the baseline (CAGR about −8.5%, Sharpe about −0.92, maximum drawdown about −27.1%, win rate about 17.2%, and for Buy & hold a drawdown near −34.2% and a total return near −18.5%), says the first change will be the seed, and states a falsifier such as: if the rule's drawdown is not shallower on most of five seeds, drop the claim. It also admits that the evidence so far is one path, that the return is worse than holding, and that synthetic data cannot establish a real edge.",
        [
            (
                "A learner changes the Market sandbox settings, opens the Valuation tab and then returns to the Market sandbox tab. What has happened to the sandbox?",
                "Its results and market settings are reset, and only the code draft is kept",
                "Everything is kept until the browser is closed",
                "Only the market settings are kept; the code is reset",
                "Each lab tool is rebuilt when you switch tabs. Code is autosaved as a draft, but results and settings are not, so record numbers before you leave a tab.",
            ),
            (
                "Why can the lab promise that the same settings and the same seed give identical bars?",
                "The default market is generated by a seeded random process rather than downloaded",
                "The lab caches a copy of real prices for every seed",
                "The server stores your earlier bars and replays them",
                "A seeded generator draws the same random numbers each time, so the bars are reproducible by construction. No real prices stand behind the default data.",
            ),
            (
                "Which sequence matches the lab's research loop?",
                "State a hypothesis, change one assumption, read the evidence, keep a research trail",
                "Run many variations, keep the best curve, save it, then write the hypothesis",
                "Pick a seed that shows a profit, change every setting at once, discard weaker runs",
                "The hypothesis comes first so the result can disprove it, one change at a time keeps comparisons clean, and keeping every run and note keeps the trail honest.",
            ),
            (
                "On the default run the trend rule returns about −23% with a drawdown near −27%, while the Buy & hold chip returns about −18% with a drawdown near −34%. What is the fairest reading?",
                "Mixed evidence from one synthetic path, so more tests are needed",
                "The rule is proven to work because its drawdown is smaller",
                "The rule is proven useless because its return is lower",
                "One seed is one path. The drawdown claim holds on this path and the return claim does not; neither is a verdict until seeds, costs and scenarios are varied.",
            ),
        ],
        [PBO, TURING],
        "market",
        "repeat the default run, write one disprovable hypothesis about the trend rule in your notebook, and record the four card values and the Buy & hold drawdown.",
        "30-minute session: 8 minutes reading the tour, 10 minutes working the default run by hand and 12 minutes in the Market sandbox, where the default data is synthetic and every result is a teaching device rather than evidence of a real edge.",
    )

    # ------------------------------------------------------------------ 14.2
    add(
        "Generate a market: processes, scenarios and seeds",
        "Choose a stochastic process, scenario, horizon and seed, predict what each will do to the generated bars, and explain why one seed is only one possible path.",
        prose(
            """The sandbox does not download prices; it generates them. Each bar comes from a
            stochastic process, which is a rule for drawing random daily returns. The series starts
            at a price of 100 on 2 January 2020 and uses a weekday calendar with 252 bars a year.
            Geometric Brownian motion (GBM) draws independent returns with a fixed drift and
            volatility. Merton jump-diffusion adds occasional jumps, Heston stochastic volatility lets
            the variance itself wander, and Markov regime switching hops between a calm, a flat and a
            crash regime. Real markets show fat tails and volatility clustering, which is why the lab
            offers more than one process.""",
            """A seed makes the randomness repeatable: the same settings and the same seed give
            identical bars, so you can change one setting and see only that setting's effect. It also
            means a run is one path out of many. A named scenario can override the process settings, so
            the sliders may keep showing your values while the scenario is in charge, and the scenario
            names are inspired by history but only illustrate stress mechanisms; they do not recreate
            historical events. The display below is the daily rule for GBM, where μ is the annual
            drift, σ the annual volatility and z a standard normal draw fixed by the seed.""",
        ),
        prose(
            """Run the defaults: GBM, 8% drift, 20% volatility, a three-year horizon and seed 42. The
            lab creates 3 × 252 = 756 bars from Thursday 2 January 2020 to Thursday 24 November 2022.
            With the probe in the steps below you should read a first open near 100.09 and a last
            close near 81.70, a price return of 81.70 ÷ 100 − 1 ≈ −18.3% in a market whose drift is
            +8% a year.""",
            """Is that a bug? Work it out. Expected log growth over three years is
            (0.08 − 0.20² ÷ 2) × 3 = 0.06 × 3 = 0.18, and one standard deviation of the three-year
            log return is 0.20 × √3 ≈ 0.346. The seed-42 path has a log return of ln(0.817) ≈ −0.202,
            which is (−0.202 − 0.18) ÷ 0.346 ≈ −1.1 standard deviations from expectation. Roughly one
            path in seven ends that low, so seed 42 is an unlucky draw, not an error. Drift describes
            the average over many paths; it is never a promise about one.""",
        ),
        prose(
            """**Add a probe.** Open the **Market sandbox** and click **strategy.py**. Above the
            `return` line, add three lines, each indented four spaces:
            `print("Bars:", len(data["close"]))`, `print("First open:", round(data["open"][0], 2))`
            and `print("Last close:", round(data["close"][-1], 2))`. They only read the data and do
            not change the signal.""",
            """**Run the baseline.** Click **Run experiment**. The Console opens by itself because the
            code prints. With the default settings, expect Bars: 756, First open: 100.09 and Last
            close: 81.7. The Console shows numbers the way Python prints them, so 81.70 appears as
            81.7.""",
            """**Change the process.** Click **Parameters**. The **Stochastic process** select offers
            Geometric Brownian motion, Merton jump-diffusion, Heston stochastic volatility and Markov
            regime switching. Choose Merton jump-diffusion: the **Jumps per year** slider appears at
            1, and the last close should come out near 104.93. Drag **Jumps per year** to 0 and run
            again: with no jumps Merton collapses to the GBM path and the last close returns to 81.7.
            Choose Heston stochastic volatility to reveal **Mean reversion κ**, **Long-run variance
            θ**, **Vol of variance ξ** and **Correlation ρ**; expect a last close near 92.78. Choose
            Markov regime switching and note that **Annual drift** and **Annual volatility** stop
            mattering; expect about 55.61.""",
            """**Change the horizon.** Put the process back to Geometric Brownian motion, then open
            the **Horizon** select, which offers 1 year, 3 years, 5 years, 10 years, 20 years and 30
            years. Choose 1 year: you get 252 bars and a last close near 91.07. With GBM the 1-year
            run is exactly the first 252 bars of the 3-year run, a fact lesson 14.4 uses to test for
            look-ahead.""",
            """**Try a scenario.** Above the editor, open the **SCENARIO** select: Custom market, Pure
            random walk, Deflationary crash · 1929-inspired, Stagflation · 1970s-inspired, Liquidity
            crisis · 2008-inspired and Crypto flash crash · −50%. Choose Crypto flash crash · −50% and
            run, then open the **Market** tab and look at the middle of the chart, around mid-June
            2021: the price roughly halves in a single day, and the last close should be near 40.85.
            The flash crash keeps your process and sliders and only adds the shock. The 1929-, 1970s-
            and 2008-inspired scenarios behave differently: they override the process, drift and
            volatility (the 2008-inspired one runs Heston with −18% drift and 55% volatility) while
            the sliders keep showing your values.""",
            """**Change the seed.** Click the gear icon in the sandbox header (**Execution
            settings**) and change **Seed** from 42 to 7. The seed is not on the **Parameters** tab.
            Run again: expect a last close near 45.54. Try 1 and 3 as well (about 68.85 and 195.65),
            then set the seed back to 42 and the original numbers return exactly.""",
            """**What you should see.** The same settings and seed always print the same three lines,
            and a different seed gives a different path from the same process. That is why a single
            run proves little. The API also has a synthetic-data endpoint that returns the bars
            directly; the lab has no screen for it.""",
        ),
        r"r_t=\frac{\mu-\tfrac{1}{2}\sigma^{2}}{252}+\frac{\sigma}{\sqrt{252}}\,z_t,\qquad P_t=P_{t-1}\,e^{r_t}",
        '''
from math import sqrt, log, exp

years = 3
mu = 0.08
sigma = 0.20
bars = years * 252
print("Bars generated:", bars)
log_drift = (mu - 0.5 * sigma * sigma) * years
spread = sigma * sqrt(years)
print("Expected 3-year log return:", round(log_drift, 3))
print("One standard deviation:", round(spread, 3))
first_price = 100
last_close = 81.70
actual = log(last_close / first_price)
print("Seed 42 log return:", round(actual, 3))
z_score = (actual - log_drift) / spread
print("Standard deviations from expectation:", round(z_score, 2))
print("Median price if the drift held:", round(first_price * exp(log_drift), 2))
print("Price return of the seed 42 path:", round(last_close / first_price - 1, 3))
''',
        "Record the last close for geometric Brownian motion, Merton jump-diffusion, Heston stochastic volatility and Markov regime switching on seed 42, then for GBM on seeds 1, 2 and 3. Say which differences come from the process and which from the seed, and why the +8% drift did not make seed 42 rise.",
        "On seed 42 expect last closes near 81.7 (GBM), 104.93 (Merton), 92.78 (Heston) and 55.61 (regime switching); on GBM expect about 68.85, 78.88 and 195.65 for seeds 1, 2 and 3. Differences between processes with the same seed come from the return rule, differences between seeds come from the random draws. Seed 42 ends about 1.1 standard deviations below the expected three-year log return of 0.18, which happens roughly one time in seven, so the drift is an average over many paths and not a forecast for one.",
        [
            (
                "Why does the seed-42 market end near 81.70 when the Annual drift slider says +8%?",
                "Drift is an average over many random paths, and seed 42 is one path that happens to end low",
                "The lab subtracts commission from prices while it generates them",
                "Seed 42 secretly switches the process to a bear regime",
                "A drift of 8% a year shifts the expected log return, but every path also carries volatility. A final price about 1.1 standard deviations below expectation is common, roughly one path in seven.",
            ),
            (
                "Which pair of settings guarantees that two runs produce identical bars?",
                "The same market settings and the same Seed",
                "The same strategy code and the same keyboard shortcut",
                "The same commission and slippage values",
                "Bars depend only on the process, scenario, drift, volatility, horizon and seed. Strategy code and costs act on the bars afterwards.",
            ),
            (
                "A learner selects Markov regime switching and then drags the Annual drift slider from 8% to 20%. What happens to the generated bars?",
                "Nothing changes: regime switching uses its own three regimes and ignores the drift and volatility sliders",
                "Every regime's drift rises by 12 percentage points",
                "The market switches back to geometric Brownian motion",
                "The regime process takes drift and volatility from three built-in regimes. The sliders only matter for GBM, Merton and Heston.",
            ),
            (
                "What does the Crypto flash crash · −50% scenario do to the generated market?",
                "It keeps the selected process and settings and adds a one-day −50% shock at the middle bar",
                "It replaces the bars with real crypto prices from a past crash",
                "It cuts every daily return in half",
                "The scenario adds a single shock to the path. It is a synthetic stress mechanism, not a reconstruction of a historical event.",
            ),
        ],
        [NUMPY_RANDOM, STYLIZED, FLASH],
        "market",
        "run the probe on seed 42 for each process, then on seeds 1, 2 and 3 for GBM, and write the six last closes next to the one change that produced each.",
        "30-minute session: 8 minutes reading how the lab generates bars, 10 minutes reproducing the seed-42 arithmetic and 12 minutes changing processes, scenarios and seeds in the Market sandbox, whose default data is synthetic.",
    )

    # ------------------------------------------------------------------ 14.3
    add(
        "Write a strategy in the guided Python runtime",
        "Write a long-or-cash rule as strategy(data), build signals from whole-series operations instead of loops, and recognize the runtime's limits and look-ahead traps.",
        prose(
            """A strategy in the lab is one function, `strategy(data)`. It receives the whole history
            at once as named series: open, high, low, close, volume, returns, sma_50 and sma_200. It
            must return a long-or-cash signal: one True or False (or 1 or 0) for every bar, or a
            single Boolean that applies to every bar. The guided runtime is a small interpreter for a
            subset of Python, not the full language. It supports assignments, def with positional
            parameters, if and else, for loops over lists or ranges, comparisons, arithmetic,
            f-strings, print, a few built-ins and selected math and numpy functions. Anything else
            fails closed with a plain message instead of doing something surprising. The moving
            averages use whatever bars exist at the start, so early signals rest on short averages.""",
            """Signals are series, so rules are written with whole-series operations: compare series
            with > and <, combine them with & and |, and wrap each comparison in brackets. Loops are
            for scalar summaries, because the runtime has no append, no list concatenation and no way
            to assign to one element of a list. Two limits matter: a two-second budget and 750,000
            operations. Finally, the runtime hands your function the entire history, including bars
            after the one being judged. The engine delays your signal by one bar, but it cannot see
            what your code looked at, so a threshold built from a whole-sample statistic such as the
            highest close quietly uses the future.""",
        ),
        prose(
            """On the default market (seed 42, 5 bps commission, 3 bps slippage), the rule
            `data["close"] > data["sma_50"]` produces 59 fills and a total return near −23.4%. Write it
            again with `np.where(close > average, 1, 0)` and the result must be identical, which is
            the check that two forms of a rule agree. Add a 2% buffer, `data["close"] > data["sma_50"]
            * 1.02`, and expect 56 fills and about −22.4%. Require the 50-bar average to sit above
            the 200-bar average and expect 24 fills and about −9.1%.""",
            """Why do the fills matter? Each fill pays about 8 bps (5 bps commission plus 3 bps
            slippage) on roughly $88,600 of value, which is 88,600 × 0.0008 ≈ $71 per fill. Fifty-nine
            fills cost about 59 × $71 ≈ $4,200, and 24 fills of the same size would cost about
            $1,700. The last rule loses less partly because it trades less, and partly because one seed
            is one path, not because it has shown skill.""",
        ),
        prose(
            """**Open the editor.** In the **Market sandbox**, click **strategy.py**. The default
            function has one working line, `return data["close"] > data["sma_50"]`. If the editor
            shows something else, open **Parameters** and click the **Trend following** chip.""",
            """**Count with sum.** Above the return line, add
            `print("Bars above the average:", sum(data["close"] > data["sma_50"]))`. Run: the Console
            should print about 309, roughly 41% of the 756 bars, because summing a series of True and
            False values counts the True ones. The rule is in the market only about two bars in five.""",
            """**Write the same rule with numpy.** Add `import numpy as np` as the first line and change
            the return line to `return np.where(data["close"] > data["sma_50"], 1, 0)`. Run. The
            cards and the Console summary should match the default run exactly: −8.5%, −0.92, −27.1%,
            17.2% and 59 fills. Identical outputs are your evidence that two ways of writing a rule
            agree.""",
            """**Add a condition.** Change the return line to
            `(data["close"] > data["sma_50"]) & (data["sma_50"] > data["sma_200"])`. Keep the
            brackets. Expect 24 fills and a total return near −9.1%. Now delete the brackets: `&`
            binds tighter than `>`, so the line becomes a chained comparison and the run fails with
            “SandboxError: Use separate comparisons joined with & for series.” Using the word `and`
            between two series fails too: “Use & and | for series comparisons.”""",
            """**Add a buffer.** Try `data["close"] > data["sma_50"] * 1.02`. Expect 56 fills and about
            −22.4%. Trading less trims costs, but costs are only part of the story.""",
            """**Meet the guard rails.** Try each of these and read the red alert under the run bar:
            `import pandas as pd` (“Imports are limited to math and the guided numpy subset.”), a
            `while` loop (“While is not supported. Use bounded for loops and documented functions.”)
            and a return value such as `data["close"] * 0 + 0.5` (“Only long/cash signals
            (True/False or 1/0) are supported.”). Messages begin with SandboxError. Then restore the
            default rule with the **Trend following** chip.""",
            """**Spot the look-ahead.** Do not run this one for results, only to see why it is wrong:
            `data["close"] > max(data["close"]) * 0.9`. The runtime accepts it, because the maximum of
            a series is allowed, but the threshold uses the highest close of the whole history, which
            nobody knows in real time. Lesson 14.4 gives you a test that catches it.""",
            """**What you should see.** Each valid variant runs in a fraction of a second and shows its
            fill count in the Console summary, so you can compare rules by their fills as well as
            their returns. The runtime stops anything slower than two seconds or heavier than 750,000
            operations, and limits code to 20,000 characters and printed output to 20 KB. Treat that
            as a design hint: write a rule as a few whole-series expressions. An optional Docker
            runtime, set up by whoever runs the lab, allows full Python; the default does not.""",
        ),
        r"s_t=\begin{cases}1 & C_t>\overline{C}_{t,n}\\ 0 & \text{otherwise}\end{cases},\qquad \overline{C}_{t,n}=\frac{1}{n}\sum_{j=0}^{n-1}C_{t-j}",
        '''
close = [100, 101, 99, 102, 104, 103, 105, 101]
window = 3
signal_count = 0
fills = 0
holding = 0
for i in range(len(close)):
    start = max(0, i - window + 1)
    total = 0
    for j in range(start, i + 1):
        total += close[j]
    average = total / (i + 1 - start)
    if close[i] > average:
        signal = 1
    else:
        signal = 0
    signal_count += signal
    if signal != holding:
        fills += 1
        holding = signal
print("Bars with a long signal:", signal_count)
print("Signal changes, one fill each:", fills)
bps = 5 + 3
notional = 88616
per_fill = notional * bps / 10000
print("Cost per fill at 8 bps:", round(per_fill, 2))
print("Cost of 59 fills:", round(59 * per_fill))
print("Cost of 24 fills of the same size:", round(24 * per_fill))
''',
        "Rewrite the default trend rule two more ways in the Market sandbox, once with np.where and once with an extra condition or buffer. Record the fill count and total return of each, say which pair of results should be identical, and explain why the lower-cost variant does not prove skill.",
        "The default rule gives 59 fills and about −23.4%, and the np.where form must give exactly the same numbers because it is the same rule. The extra-condition rule gives 24 fills and about −9.1%; the 2% buffer gives 56 fills and about −22.4%. A fill costs about 8 bps on roughly $88,600, or $71, so 59 fills cost about $4,200 and 24 fills of that size about $1,700. Fewer fills explain part of the improvement and the rest is the luck of one seed, so neither result shows skill; it only shows how a rule's trading frequency feeds into costs.",
        [
            (
                "Which return value does strategy(data) accept?",
                "A single True, or one True/False (or 1/0) value for each bar",
                "A target weight such as 0.5 for each bar",
                "A signed position of −1, 0 or 1 for each bar",
                "The lab backtests long or cash only. Fractional weights and shorts are rejected with “Only long/cash signals (True/False or 1/0) are supported.”",
            ),
            (
                "A learner writes data[\"close\"] > data[\"sma_50\"] & data[\"sma_50\"] > data[\"sma_200\"] and the run fails. What is the fix?",
                "Put each comparison in brackets and join them with &",
                "Replace & with the word and",
                "Wrap the whole expression in a for loop",
                "& binds tighter than >, so the unbracketed line becomes a chained comparison, which the runtime rejects. The words and/or do not work on whole series either.",
            ),
            (
                "Why can a signal list not be built bar by bar inside a loop in the guided runtime?",
                "There is no append, list concatenation or element assignment, so signals come from whole-series expressions",
                "Loops are disabled entirely",
                "Loops are allowed only after the first 200 bars",
                "For loops over lists and ranges work, but a list cannot be extended or edited. Series comparisons, &, |, ~ and np.where produce the signal instead.",
            ),
            (
                "A rule sets its threshold at 0.9 × max(data[\"close\"]). Why is that a look-ahead problem even though the engine delays signals by one bar?",
                "The maximum is computed over the whole history, including bars after the one being judged",
                "The engine fills at the previous close instead of the next open",
                "The runtime does not support max()",
                "A live trader cannot know the full-period maximum. The one-bar delay stops a bar from trading on its own close; it cannot detect whole-sample statistics inside your code.",
            ),
        ],
        [PY_FLOW, PY_MATH, NUMPY_WHERE],
        "market",
        "rewrite the default rule two more ways, one with np.where and one with an extra condition, and record the fill count and total return of each.",
        "30-minute session: 8 minutes reading the runtime rules, 10 minutes reproducing the toy loop and cost arithmetic and 12 minutes writing rules in the Market sandbox, whose default data is synthetic and whose wins are never proof of a real edge.",
    )

    # ------------------------------------------------------------------ 14.4
    add(
        "Backtest mechanics: signals, fills, costs and buy-and-hold",
        "Trace how a signal becomes a fill at the next open, compute the cost of a round trip, read the buy-and-hold comparison, and run a test that catches look-ahead.",
        prose(
            """The backtest turns your signal into trades with a fixed timing rule: a signal formed
            on one bar's close trades at the next bar's open. The account is long or in cash, all
            in, and it may hold fractional shares. A buy pays the open plus slippage and then a
            commission on top; a sale receives the open minus slippage and pays a commission on its
            proceeds. Every trade's profit or loss is net of both costs. A position still open at the
            end is marked to the last close and left out of the win rate and profit factor.""",
            """The comparison line, "Buy & hold", buys at the first bar's open, pays the entry costs
            once and never sells, so it has no exit cost. That is the honest benchmark for a
            long-or-cash rule on one market: if your rule cannot beat simply owning the asset after
            costs, its trading is not adding anything. The one-bar delay stops a bar from trading on
            its own close, but it cannot see inside your code, so the look-ahead from lesson 14.3
            needs its own test.""",
        ),
        prose(
            """Your rule turns long at a close of 100.00 and the next open is 101.00. With $100,000,
            3 bps of slippage and a 5 bps commission, the buy price is 101.00 × 1.0003 = 101.0303,
            and the shares are 100,000 ÷ (101.0303 × 1.0005) ≈ 989.31. Later the rule turns off and
            the next open is 104.00. The sale price is 104.00 × 0.9997 = 103.9688, the proceeds are
            about $102,857.10 and the 5 bps commission takes about $51.43, leaving roughly
            $102,805.67, a net gain of about 2.81% against a 2.97% move in the price.""",
            """Here is the look-ahead test promised in lesson 14.3. Run a rule on Horizon "1 year" and
            again on "3 years" with the same seed, then compare the trades inside the first year. The
            first 252 bars are identical, so a rule that only looks backwards must make identical
            first-year trades. On seed 42 the trend rule makes 28 trades both times. The rule that
            compares the close with 0.9 × the maximum close makes 22 first-year trades on the short
            run but only 10 on the long one, because its threshold moved when later bars were added.
            Different trades on identical data are proof that the rule peeked.""",
        ),
        prose(
            """**Run the default rule.** In the **Market sandbox**, click the **Trend following**
            chip and then **Run experiment** (or Ctrl/Cmd+Enter in the editor). The **Console**
            ends with a summary such as "756 bars · 59 fills · final equity …".""",
            """**Follow one trade.** Open the **Trades** tab. Its columns are Date, Side, Quantity,
            Price, Fee and P&L. Take the first BUY row's date, open the **Market** tab ("OHLC
            prices") and find that day's open. The Price column should equal the open × 1.0003.""",
            """**Compare with buy and hold.** Open **Equity curve**. The legend shows "Strategy" and
            "Buy & hold". Then click the **Buy & hold** chip and run it: its total return in **All
            metrics** should match the end of the Buy & hold line.""",
            """**Switch costs off and on.** Click the gear icon (aria "Execution settings"), set
            **Commission (bps)** and **Slippage (bps)** to 0, restore the **Trend following** chip
            and run. Note the final equity. Set both to 20 and run again. The fill count stays the
            same while the final equity falls, because costs never change the signals.""",
            """**Run the look-ahead test.** Open **Parameters**, set **Horizon** to "1 year" and run
            the rule `data["close"] > max(data["close"]) * 0.9`. Note the first-year trades. Set
            **Horizon** to "3 years", run again and count the trades dated inside the first year.
            Repeat with the default trend rule.""",
            """**What you should see.** Fills dated one bar after each signal, prices equal to the
            open adjusted by slippage, and identical first-year trades for the trend rule but not for
            the maximum-based rule.""",
        ),
        r"P^{\text{buy}}_t=O_t(1+s),\quad q=\frac{\text{cash}}{P^{\text{buy}}_t(1+c)},\qquad \text{proceeds}=q\,O_{t'}(1-s)(1-c)",
        '''
cash = 100000
slippage = 3 / 10000
commission = 5 / 10000
buy_price = 101.00 * (1 + slippage)
shares = cash / (buy_price * (1 + commission))
sell_price = 104.00 * (1 - slippage)
proceeds = shares * sell_price
net = proceeds * (1 - commission)
print("Buy price:", round(buy_price, 4), "shares:", round(shares, 2))
print("Sale price:", round(sell_price, 4), "net proceeds:", round(net, 2))
print("Net gain:", round((net / cash - 1) * 100, 2), "% against a price move of", round((104 / 101 - 1) * 100, 2), "%")
first_year_short = 22
first_year_long = 10
print("Look-ahead rule trades in year one, 1-year run vs 3-year run:", first_year_short, first_year_long)
''',
        "Run the default trend rule with costs at 0, at the defaults and at 20 bps each, and record final equity and fills for each. Then run the look-ahead test on both the trend rule and the maximum-based rule and report the first-year trade counts.",
        "Fills stay at 59 in all three cost settings because costs never change signals, while final equity falls as costs rise; on seed 42 the zero-cost run returns about −19.7% against −23.4% with default costs. In the look-ahead test the trend rule makes 28 first-year trades on both horizons, while the maximum-based rule makes 22 on the 1-year run and 10 on the 3-year run. A rule whose past trades change when future data is added is using the future, so its backtest cannot be trusted.",
        [
            (
                "A trend rule's signal turns long at Monday's close. When does the lab buy?",
                "At Tuesday's open, adjusted for slippage",
                "At Monday's close, when the signal appears",
                "At Tuesday's close, after the day is complete",
                "A signal formed on one bar's close trades at the next bar's open. This one-bar delay prevents trading on information from the same bar.",
            ),
            (
                "With 3 bps of slippage, what does a buy at an open of 101.00 pay per share before commission?",
                "About 101.03, which is 101.00 × 1.0003",
                "Exactly 101.00, because slippage applies only to sales",
                "About 104.03, the next day's price",
                "Buys pay the open plus slippage: 101.00 × (1 + 0.0003) = 101.0303. The commission is charged on top.",
            ),
            (
                "How does the lab treat a position that is still open when the backtest ends?",
                "It is marked to the last close and left out of win rate and profit factor",
                "It is sold at the last close and counted as a closed trade",
                "It is removed from the results entirely",
                "Open positions count in equity at the last close, but only closed round trips enter the win rate and profit factor.",
            ),
            (
                "Run on 1 year and on 3 years with the same seed, a rule makes different trades inside the first year. What does that show?",
                "The rule uses information from later bars, because the first year's data is identical in both runs",
                "The seed was ignored by the second run",
                "Longer horizons always change early trades",
                "The first 252 bars match exactly, so a rule that looks only backwards must trade identically on them. Different trades reveal look-ahead.",
            ),
        ],
        [FLASH, PBO, IG_ORDERS],
        "market",
        "rerun the default rule with costs at 0, at the defaults and at 20 bps each, then run the one-year versus three-year look-ahead test on two rules and record what changes.",
        "30-minute session: 7 minutes reading the execution rules, 9 minutes reproducing the round-trip arithmetic and 14 minutes tracing trades and running the look-ahead test in the Market sandbox; the lab's default data is synthetic, so no result is evidence of a real edge.",
    )
    # ------------------------------------------------------------------ 14.5
    add(
        "Read the results: metrics, charts, monthly returns and the trade log",
        "Read the four cards and all 14 metrics, connect each chart to the numbers behind it, and explain why no single metric can rank a rule.",
        prose(
            """After a run, the four cards show CAGR, SHARPE, MAX DRAWDOWN and WIN RATE, and **All
            metrics** lists fourteen values with four decimals. CAGR compounds the total return over
            252 bars a year. Sharpe and Sortino subtract a 3% annual risk-free rate from the daily
            returns and divide by their variability (all of it for Sharpe, only the downside for
            Sortino), scaled by √252. Maximum drawdown is the deepest fall from a running peak, and
            Calmar divides CAGR by its size. Beta and alpha compare the rule's daily returns with
            buy and hold, and VaR and CVaR at 95% describe the worst daily losses.""",
            """A metric that cannot be computed shows "—" on a card and "Undefined" in All metrics,
            never a flattering zero. An all-cash rule has no variability, so its Sharpe is undefined;
            a rule with no closed trades has no win rate. The tabs show the same run from different
            angles: Equity curve, Drawdown, Market, a Returns heat map by month, Trades, Console and
            All metrics. If you change a setting after running, the run time gains "· inputs changed"
            to warn you that the output no longer matches the controls.""",
        ),
        prose(
            """With the default settings the Trend following run returns −23.40% over 756 bars. CAGR
            is (1 − 0.2340)^(252 ÷ 756) − 1 = 0.766^(1/3) − 1 ≈ −8.5%, the card's value. The deepest
            drawdown is −27.07%, so Calmar is −0.085 ÷ 0.2707 ≈ −0.31. The run made 59 fills, 30 buys
            and 29 sales, so there are 29 closed round trips; a win rate of 17.2% means 5 of them
            made money, and a profit factor of 0.32 says the winners earned about a third of what the
            losers lost.""",
            """Now click the Mean reversion chip on the same seed. Its win rate is 76.7%, yet its
            total return is −2.37%. Many small wins and a few large losses produce exactly that
            pattern, which is why a win rate is meaningless without the size of wins and losses,
            the drawdown and the comparison with buy and hold.""",
        ),
        prose(
            """**Run and read the cards.** Run the **Trend following** chip with the defaults. Read
            CAGR, SHARPE, MAX DRAWDOWN and WIN RATE, then open **All metrics** and find total
            return, profit factor, trades, final equity, alpha, beta, VaR 95%, CVaR 95% and
            Calmar.""",
            """**Check two numbers by hand.** Recompute CAGR from total return and the bar count, and
            Calmar from CAGR and maximum drawdown, using the worksheet. They should match the panel to
            the second decimal.""",
            """**Read the charts.** Open **Drawdown** ("Drawdown from peak") and find the date of the
            deepest point. Open **Returns** and find the worst month in the heat map; empty months show
            "—". Open **Trades** and count the rows with a positive P&L.""",
            """**Compare a second rule.** Click **Mean reversion**, run it, and write both rules'
            fourteen metrics side by side in your notebook.""",
            """**Make the output stale on purpose.** Move the **Annual volatility** slider without
            running, and look for "· inputs changed" beside the run time.""",
            """**What you should see.** Hand-computed CAGR and Calmar that match the panel, a
            mean-reversion run with a high win rate and a negative total return, and a stale-output
            warning after any change you have not run.""",
        ),
        r"\text{Sharpe}=\frac{\bar r-r_f}{s_r}\sqrt{252},\qquad \text{Calmar}=\frac{\text{CAGR}}{\left|\text{MDD}\right|}",
        '''
total_return = -0.2340
bars = 756
cagr = (1 + total_return) ** (252 / bars) - 1
max_drawdown = -0.2707
calmar = cagr / abs(max_drawdown)
print("CAGR:", round(cagr * 100, 2), "%")
print("Calmar:", round(calmar, 3))
closed_trades = 59 // 2
winners = round(0.1724 * closed_trades)
print("Closed round trips:", closed_trades, "winners:", winners)
''',
        "Run the Trend following and Mean reversion chips on the default seed and record all fourteen metrics for each. Recompute CAGR and Calmar for one of them by hand, and explain in three sentences why the rule with the higher win rate is not necessarily the better rule.",
        "On the default seed the trend rule shows total return −23.40%, CAGR −8.5%, maximum drawdown −27.07%, win rate 17.2% and profit factor 0.32; mean reversion shows total return −2.37% with a win rate of 76.7%. CAGR is (1 + total return) raised to 252 ÷ 756, minus one, and Calmar is CAGR divided by the size of the drawdown. A high win rate can coexist with losses when losing trades are larger than winning ones, so a fair comparison uses return, drawdown, profit factor and the buy-and-hold benchmark together, all on more than one seed.",
        [
            (
                "The default run shows CAGR −8.5% and maximum drawdown −27.1%. What is its Calmar ratio?",
                "About −0.31, CAGR divided by the size of the drawdown",
                "About −3.19, the drawdown divided by CAGR",
                "−35.6%, the sum of the two",
                "Calmar = CAGR ÷ |max drawdown| = −0.085 ÷ 0.271 ≈ −0.31.",
            ),
            (
                "A rule wins 76.7% of its trades yet loses 2.37% overall. How is that possible?",
                "Its few losing trades are larger than its many winning ones",
                "The win rate includes the open position at the end",
                "The metrics are computed before costs",
                "Win rate counts trades, not their size. A handful of large losses can outweigh many small gains.",
            ),
            (
                "Why does an all-cash rule show '—' for Sharpe?",
                "Its daily returns have no variability, so the ratio's denominator is zero",
                "Sharpe is hidden whenever the data is synthetic",
                "Sharpe needs at least one losing trade to be computed",
                "Sharpe divides by the standard deviation of daily returns. With no variability the ratio is undefined, and the lab shows '—' rather than a misleading number.",
            ),
            (
                "What does '· inputs changed' beside the run time tell you?",
                "A setting changed after the last run, so the output no longer matches the controls",
                "The lab rewrote your strategy code",
                "The market data was refreshed from a live feed",
                "The output belongs to the previous settings. Run again before reading or saving the numbers.",
            ),
        ],
        [DSR, HLZ, PBO],
        "market",
        "run the Trend following and Mean reversion chips on the same seed and compare all fourteen metrics side by side.",
        "30-minute session: 8 minutes reading the metric definitions, 9 minutes recomputing CAGR and Calmar and 13 minutes reading the cards, charts and trade log in the Market sandbox; the lab's default data is synthetic, so no metric is evidence of a real edge.",
    )
    # ------------------------------------------------------------------ 14.6
    add(
        "The valuation tool: net current assets, haircuts and Graham value",
        "Use the Valuation tab to compute unadjusted and adjusted net current asset value, the two-thirds screen and the Graham heuristic, and test how sensitive each is to its assumptions.",
        prose(
            """Net current asset value (NCAV) asks what would be left for shareholders if a company
            collected its current assets and paid every liability. It counts cash, receivables and
            inventory, subtracts total liabilities and divides by diluted shares, giving fixed assets
            no value at all. The tool shows that unadjusted figure, a two-thirds screen price that
            Graham-style investors used as a demanding entry point, and an adjusted NCAV that applies
            recovery rates: in a forced sale, customers pay late or not at all and inventory sells at
            a discount.""",
            """The tool also computes the Graham heuristic, earnings per share × (8.5 + 2 × growth) ×
            4.4 ÷ bond yield, with growth and yield entered in percentage points. It is a sensitivity
            device, not a price: small changes to growth or yield swing it widely. All amounts are in
            millions except per-share values, the outputs update about a quarter of a second after
            each edit, and nothing here describes a real company.""",
        ),
        prose(
            """The defaults describe a company with $40m of cash, $60m of receivables, $80m of
            inventory, $70m of liabilities and 10m diluted shares at $6. Unadjusted NCAV is (40 + 60 +
            80 − 70) ÷ 10 = $11.00 per share, and the two-thirds screen price is $7.33, so the stock
            passes the screen. Recovering 85% of receivables and 60% of inventory gives (40 + 51 + 48 −
            70) ÷ 10 = $6.90, and the margin of safety against that adjusted value is 1 − 6 ÷ 6.90 ≈
            13.0%.""",
            """Cut inventory recovery to 40% and adjusted NCAV falls to (40 + 51 + 32 − 70) ÷ 10 =
            $5.30, so the price now exceeds the adjusted value by about 13%, while the unadjusted
            screen still passes. The Graham heuristic with EPS $4, growth 5 and yield 4.4 is 4 × 18.5
            × 4.4 ÷ 4.4 = $74.00; raising the yield to 6 lowers it to about $54.27.""",
        ),
        prose(
            """**Open the tool.** Click the **Valuation** tab. Under "BALANCE SHEET INPUTS" (amounts in
            millions, except per-share values) you will find **Cash & equivalents**, **Accounts
            receivable**, **Inventory**, **Total liabilities**, **Diluted shares** and **Market price
            / share**.""",
            """**Read the worksheet.** The panel "VALUATION WORKSHEET" shows "ADJUSTED NCAV / SHARE",
            a bar comparing "Market price" with "Adjusted asset value", "Unadjusted NCAV",
            "Two-thirds screen price", "Margin of safety · adjusted NCAV" and "Graham heuristic value",
            plus a verdict that begins "Passes the unadjusted two-thirds NCAV screen." or "Does not
            pass".""",
            """**Stress the recoveries.** Under **Liquidation assumptions**, drag **Inventory
            recovered** from 60% down to 40%. Watch "· UPDATING" appear briefly and the adjusted
            value fall to $5.30 while the screen verdict stays the same.""",
            """**Stress the heuristic.** Under **Graham formula inputs**, change **Bond yield (%)**
            from 4.4 to 6, then **Growth (%)** from 5 to 10, and note how far the value moves.""",
            """**What you should see.** An adjusted value that is always at or below the unadjusted
            one, a margin of safety that turns negative once recoveries fall far enough, and a
            heuristic that moves sharply with growth and yield.""",
        ),
        r"\text{NCAV}_{\text{adj}}=\frac{C+\rho_R R+\rho_I I-L}{N},\qquad \text{MoS}=1-\frac{P}{\text{NCAV}_{\text{adj}}}",
        '''
cash = 40
receivables = 60
inventory = 80
liabilities = 70
shares = 10
price = 6
ncav = (cash + receivables + inventory - liabilities) / shares
print("Unadjusted NCAV:", ncav, "two-thirds screen:", round(ncav * 2 / 3, 2))
for inventory_rate in [0.60, 0.40]:
    adjusted = (cash + 0.85 * receivables + inventory_rate * inventory - liabilities) / shares
    print("Inventory recovery", inventory_rate, "adjusted NCAV:", round(adjusted, 2), "margin of safety:", round((1 - price / adjusted) * 100, 1), "%")
for bond_yield in [4.4, 6.0]:
    print("Graham value at yield", bond_yield, ":", round(4 * (8.5 + 2 * 5) * 4.4 / bond_yield, 2))
''',
        "Find the inventory recovery rate at which the adjusted NCAV equals the $6 price, using the default inputs. Then record the Graham heuristic at growth 0, 5 and 10 with a 4.4 yield, and explain which output you would trust least and why.",
        "Adjusted NCAV is (40 + 0.85 × 60 + r × 80 − 70) ÷ 10; setting it to 6 gives 21 + 80r = 60, so r = 48.75%. Below that recovery rate the price exceeds the adjusted asset value. The Graham heuristic gives $34.00 at zero growth, $74.00 at 5 and $114.00 at 10, so a five-point change in assumed growth moves it by $40. It deserves the least trust because its result depends almost entirely on a growth guess, while the asset-based values rest on balance-sheet items you can check.",
        [
            (
                "With the default inputs, what does 'ADJUSTED NCAV / SHARE' show?",
                "$6.90, after recovering 85% of receivables and 60% of inventory",
                "$11.00, the unadjusted figure",
                "$7.33, the two-thirds screen price",
                "Adjusted NCAV = (40 + 0.85 × 60 + 0.60 × 80 − 70) ÷ 10 = $6.90 per share.",
            ),
            (
                "Inventory recovery falls from 60% to 40%. What happens to adjusted NCAV per share?",
                "It falls by $1.60, to $5.30",
                "It rises, because liabilities fall",
                "It stays at $6.90, because inventory is excluded",
                "Twenty points less recovery on $80m of inventory removes $16m, or $1.60 per share across 10m shares.",
            ),
            (
                "Why can a stock pass the two-thirds NCAV screen yet trade above its adjusted asset value?",
                "The screen uses unadjusted NCAV, while the adjusted value applies recovery haircuts",
                "The screen already includes the haircuts",
                "The Graham heuristic overrides the screen",
                "The screen is computed from book values. Realistic recoveries can push the adjusted value below the price even when the screen passes.",
            ),
            (
                "In the Graham heuristic, what does raising the bond yield from 4.4% to 6% do to a value of $74?",
                "Lowers it to about $54.27",
                "Raises it to about $100.91",
                "Leaves it unchanged, because the yield is not in the formula",
                "The yield divides the heuristic: 74 × 4.4 ÷ 6 ≈ $54.27.",
            ),
        ],
        [SEC_STATEMENTS, IG_STOCKS],
        "valuation",
        "move the two recovery sliders until the margin of safety reaches zero, and record the recovery rates at which the price equals the adjusted asset value.",
        "30-minute session: 8 minutes reading how the tool values a balance sheet, 10 minutes reproducing the NCAV and heuristic arithmetic and 12 minutes stressing the inputs in the Valuation tab; every company in the tool is fictional.",
    )
    # ------------------------------------------------------------------ 14.7
    add(
        "The factor studio: models, coefficients and robust errors",
        "Fit CAPM and Fama–French models to known synthetic data, read each coefficient with its HAC standard error, and judge an alpha estimate by its uncertainty rather than its size.",
        prose(
            """A factor model explains an asset's excess return with a few common exposures: the
            market, small versus large companies (SMB), value versus growth (HML), and, in larger
            models, momentum or profitability and investment factors. The studio fits these by
            ordinary least squares. Because the data are generated with known exposures, shown in the
            box "KNOWN DATA-GENERATING PROCESS", you can check every estimate against the truth,
            which no real dataset allows.""",
            """Each coefficient comes with a standard error labelled "SE · HAC": a Newey–West estimate
            that stays valid when errors change size over time or are correlated from day to day. The
            p-value asks how surprising the estimate would be if the true value were zero. "TEST R² ·
            RIDGE" fits a ridge regression on the earlier 75% of observations and scores the later
            25%, an out-of-sample check that ordinary R² cannot give. The data are generated
            observations, not historical factor returns.""",
        ),
        prose(
            """With the defaults ("Fama–French · three factors", 756 observations, seed 42 and 1.0%
            idiosyncratic volatility), the planted exposures are 1.10 to the market, 0.25 to SMB and
            0.40 to HML, with a daily alpha of 0.0001. The fit returns 1.0907 for the market with a
            standard error of 0.0393, about a quarter of a standard error from the truth. HML comes
            out at 0.3662 with a standard error of 0.0371, about 0.9 standard errors low. R² is 0.564
            and the ridge test R² is 0.496.""",
            """The alpha estimate is 0.000586 a day, which annualizes to roughly 0.000586 × 252 ≈
            14.8%, an impressive-looking number. Its t-statistic is only 1.54 and its p-value 0.124,
            so the data cannot separate it from zero, and indeed the planted value is much smaller.
            Precise exposures and an imprecise alpha are the usual outcome, with real data as well as
            generated data.""",
        ),
        prose(
            """**Open the studio.** Click the **Factor studio** tab. Leave **Factor specification** on
            "Fama–French · three factors", **Observations** on 756, **Random seed** on 42 and
            **Idiosyncratic daily volatility** on 1.0%, and click **Fit factor model**.""",
            """**Read the diagnostics.** Under "MODEL DIAGNOSTICS", note "R² · OLS", "ADJUSTED R²" and
            "TEST R² · RIDGE", then the table with Factor, β, SE · HAC and p-value for "Alpha
            (daily)", "Market", "SMB" and "HML". The footnote reads "756 observations · 6 HAC lags ·
            ridge training/test split 567/189." """,
            """**Compare with the truth.** For each factor, subtract the planted exposure from the
            estimate and divide by its standard error. Values within about two standard errors are
            ordinary sampling noise.""",
            """**Change the model.** Switch to "CAPM · market only" and fit again. The market beta
            moves because the omitted factors now load onto it. Switch to "Carhart · four factors"
            and "Fama–French · five factors" and note how R² changes.""",
            """**Add noise.** Raise **Idiosyncratic daily volatility** to 3% and fit. Standard errors
            widen and R² falls, while the planted exposures stay the same.""",
            """**What you should see.** Estimates within a couple of standard errors of the planted
            values, an alpha that is rarely significant, and a "OLS residuals" chart without obvious
            structure.""",
        ),
        r"r_t-r_{f,t}=\alpha+\sum_{k}\beta_k f_{k,t}+\varepsilon_t,\qquad t_{\beta}=\frac{\hat\beta-\beta_0}{\operatorname{SE}_{\text{HAC}}(\hat\beta)}",
        '''
estimates = [1.0907, 0.2256, 0.3662]
errors = [0.0393, 0.0385, 0.0371]
truth = [1.10, 0.25, 0.40]
names = ["Market", "SMB", "HML"]
for i in range(3):
    distance = (estimates[i] - truth[i]) / errors[i]
    print(names[i], "estimate", estimates[i], "truth", truth[i], "standard errors away:", round(distance, 2))
alpha = 0.000586
alpha_error = 0.000381
print("Alpha t-statistic:", round(alpha / alpha_error, 2))
print("Alpha annualized:", round(alpha * 252 * 100, 1), "%")
''',
        "Fit the three-factor model at seeds 42, 43 and 44 with the other defaults. For each seed record every estimate, its HAC standard error and its distance from the planted value in standard errors, and the alpha's p-value. Summarize what changes across seeds and what does not.",
        "Across seeds the estimates move by a few hundredths around the planted exposures of 1.10, 0.25 and 0.40, and nearly all distances stay within about two standard errors, which is what sampling noise looks like. The alpha estimate changes sign or size from seed to seed with p-values usually far above 0.05, because a tiny planted alpha is hard to detect in 756 noisy observations. The lesson for real data is to report exposures with their errors and treat an unstable, insignificant alpha as unproven rather than as skill.",
        [
            (
                "Which column shows how uncertain each coefficient is?",
                "SE · HAC, a standard error robust to changing and correlated errors",
                "β, because it already includes the error",
                "R² · OLS, the share of variance explained",
                "The HAC standard error measures sampling uncertainty and stays valid under heteroskedasticity and autocorrelation.",
            ),
            (
                "The planted market exposure is 1.10 and the estimate is 1.0907 with a standard error of 0.0393. What is the right reading?",
                "The estimate lies about a quarter of a standard error from the truth, ordinary sampling noise",
                "The model is badly biased",
                "The true exposure must be 1.0907",
                "(1.0907 − 1.10) ÷ 0.0393 ≈ −0.24, well within normal sampling variation.",
            ),
            (
                "The daily alpha estimate is 0.000586 with a p-value of 0.124. What can you conclude?",
                "The data cannot distinguish it from zero, even though it annualizes to about 15%",
                "The strategy earns about 15% a year of skill",
                "Alpha is exactly zero",
                "A p-value of 0.124 means an estimate this large is not unusual when the true alpha is zero. Annualizing does not make it more certain.",
            ),
            (
                "Why does the studio also report 'TEST R² · RIDGE'?",
                "It fits on the earlier 75% of observations and scores the later 25%, an out-of-sample check",
                "It is the same R² computed with a different formula",
                "It counts how many factors are in the model",
                "In-sample R² rewards fitting the sample. The ridge test R² measures how well a model fitted on earlier data explains later data.",
            ),
        ],
        [FRENCH, STATSMODELS_HAC, HLZ],
        "factors",
        "fit the three-factor model at seeds 42, 43 and 44 and record how far each estimated exposure lands from its planted value, measured in standard errors.",
        "30-minute session: 8 minutes reading what a factor model estimates, 10 minutes computing distances in standard errors and 12 minutes fitting models in the Factor studio; its observations are generated, not historical factor returns.",
    )
    # ------------------------------------------------------------------ 14.8
    add(
        "Robustness in the sandbox: costs, seeds and scenarios",
        "Test one rule across seeds, cost settings and named stress scenarios, summarize the spread of results honestly, and count every trial you ran.",
        prose(
            """One seed is one path through a random market. A rule that looks good on seed 42 may look
            poor on seed 43, and the only way to know is to run it on several seeds with every other
            setting fixed, then report the average, the spread and the comparison with buy and hold
            on each path. Costs are the second dimension: a rule whose edge disappears when costs are
            raised slightly has no edge worth trusting.""",
            """Named scenarios are the third. "Pure random walk" uses geometric Brownian motion with no
            drift; "Deflationary crash · 1929-inspired" uses jumps, a 15% annual decline and 38%
            volatility; "Stagflation · 1970s-inspired" a 1.5% drift with 32% volatility; "Liquidity
            crisis · 2008-inspired" stochastic volatility with an 18% decline and 55% volatility; and
            "Crypto flash crash · −50%" adds a one-day −50% shock at the middle bar. They illustrate
            stress mechanisms and do not recreate historical events. Every run you try is a trial,
            and the best of many trials looks better than it is.""",
        ),
        prose(
            """With default costs and a three-year horizon, the trend rule returns −23.4%, +4.9%,
            +19.6%, +2.3% and −5.8% on seeds 42 to 46, an average of about −0.5% with a standard
            deviation near 15.8 points. Buy and hold returns −18.5%, +5.1%, +88.4%, +30.7% and +0.4% on
            the same seeds, so the rule trails it every time, though its maximum drawdown is
            shallower on four of the five seeds. At zero cost seed 42 still loses 19.7%, so costs are
            not the whole story.""",
            """The scenarios tell a different part of the story. On seed 42 the rule loses 26.6%
            against 35.8% for buy and hold in the pure random walk, 75.4% against 92.0% in the 1929
            crash, 36.8% against 51.4% in stagflation, 37.3% against 64.1% in the liquidity crisis and
            57.5% against 59.2% in the flash crash. Stepping aside in falling markets limits damage,
            but the flash crash's one-day shock arrives before any signal can act.""",
        ),
        prose(
            """**Fix everything but one setting.** Click **Trend following**, keep the defaults and
            open the gear icon (aria "Execution settings"), where **Seed** lives.""",
            """**Sweep five seeds.** Run seeds 42, 43, 44, 45 and 46 in turn. For each, write the
            total return and maximum drawdown from **All metrics**, and the buy-and-hold return from
            the end of the Buy & hold line or a run of the **Buy & hold** chip.""",
            """**Sweep costs.** On seed 42, run with **Commission (bps)** and **Slippage (bps)** at 0,
            at the defaults (5 and 3) and at 20 each, and record final equity.""",
            """**Sweep scenarios.** On seed 42 with default costs, open **Parameters** and choose each
            **SCENARIO** in turn, from "Pure random walk" to "Crypto flash crash · −50%". Read the
            fine print "Named stress scenarios override selected process defaults." """,
            """**Count your trials.** Add up every run you made in this lesson and write the number at
            the top of your notes, before any conclusion.""",
            """**What you should see.** Results that vary widely across seeds, a final equity that
            falls as costs rise, and scenario results that differ in a pattern you can explain.""",
        ),
        r"\bar{R}=\frac{1}{S}\sum_{s=1}^{S}R_s,\qquad \hat\sigma_R=\sqrt{\frac{1}{S-1}\sum_{s=1}^{S}\left(R_s-\bar{R}\right)^{2}}",
        '''
from math import sqrt

rule = [-23.4, 4.9, 19.6, 2.3, -5.8]
hold = [-18.5, 5.1, 88.4, 30.7, 0.4]
mean = sum(rule) / len(rule)
total = 0
for value in rule:
    total += (value - mean) ** 2
spread = sqrt(total / (len(rule) - 1))
beats = 0
for i in range(len(rule)):
    if rule[i] > hold[i]:
        beats += 1
print("Rule mean:", round(mean, 2), "% standard deviation:", round(spread, 2), "points")
print("Seeds where the rule beat buy and hold:", beats, "of", len(rule))
print("Trials in this lesson so far:", 5 + 3 + 5)
''',
        "Run the default trend rule on five seeds, three cost settings and the five named scenarios. Report the average and standard deviation of total return across seeds, how often the rule beat buy and hold, the cost sensitivity, the scenario results and the total number of runs.",
        "With default settings the rule averages about −0.5% across seeds 42–46 with a standard deviation near 15.8 points and trails buy and hold on all five, though it has a shallower drawdown on four. On seed 42 it loses 19.7% at zero cost and 23.4% with default costs, so costs matter but do not explain everything. Across the named scenarios it loses less than buy and hold in every falling market, because stepping aside limits damage. A complete report lists all thirteen runs and states that synthetic paths cannot establish a real-market edge.",
        [
            (
                "Why rerun the same rule on several seeds?",
                "Each seed is one generated path, so a single result could be luck",
                "Seeds change the strategy code",
                "More seeds make each individual run more accurate",
                "Varying only the seed shows how much the result depends on the particular random path.",
            ),
            (
                "What does the 'Crypto flash crash · −50%' scenario add?",
                "A one-day −50% shock at the middle bar, on top of the chosen process",
                "A permanent −50% annual drift",
                "Real cryptocurrency prices",
                "The flash-crash scenario keeps your process and adds a single −50% shock halfway through the run.",
            ),
            (
                "You tried 40 variants and want to report the best Sharpe ratio. What must accompany it?",
                "The number of trials, because the best of many is inflated by chance",
                "Nothing, because the best result is the true one",
                "A higher commission setting",
                "Selecting the maximum of many noisy results biases it upward. Reporting the number of trials lets a reader judge that bias.",
            ),
            (
                "Setting commission and slippage to zero turns a losing rule into a winner. What does that show?",
                "Any edge the rule has is smaller than its trading costs",
                "Costs should always be set to zero",
                "The rule is robust",
                "If costs decide whether the rule wins, the rule cannot be expected to survive real trading frictions.",
            ),
        ],
        [PBO, DSR, STYLIZED],
        "market",
        "run the default rule on five seeds and on the five named scenarios with every other setting fixed, and tabulate total return against buy and hold for all ten runs.",
        "30-minute session: 6 minutes reading why one path is not evidence, 8 minutes summarizing results across seeds and 16 minutes running the sweeps in the Market sandbox; the lab's data is synthetic and its scenarios do not recreate historical events.",
    )
    # ------------------------------------------------------------------ 14.9
    add(
        "Paper trading: liquidity, stale-data, spread and drawdown guards",
        "Place paper orders through the mock broker, compute a fill with spread, slippage, commission and a participation cap, and trigger each pre-trade guard deliberately.",
        prose(
            """The **Paper trading** tab is a single-session mock broker that shows the checks a real
            trading system should run before an order reaches a market. A fill takes at most 10% of
            the available bar volume, so a large order fills partly and the remainder is not retried.
            The fill price moves away from the reference price by slippage plus half the spread, and
            a commission is charged on the filled value. The account is long-only and holds $100,000
            of paper cash.""",
            """Before filling, the broker runs guards in a fixed order: a halted account is refused;
            equity below 97.5% of the starting amount trips a drawdown circuit breaker and halts the
            account; a price older than 60 seconds is stale; a spread wider than 100 bps is refused;
            no volume means no liquidity; and the order must be affordable, or the shares must be
            owned. Each rejection is written to the audit log with its reason. The account has no
            live brokerage connection and its state lives in your browser.""",
        ),
        prose(
            """With the defaults (10 shares, a $100 reference price, 1,000 shares of bar volume, a
            5 bps spread, 3 bps slippage and a 5 bps commission) a buy fills all 10 shares at 100 ×
            (1 + (3 + 5 ÷ 2) ÷ 10,000) = $100.055, and the commission is 10 × 100.055 × 0.0005 ≈
            $0.50. An order for 150 shares against the same volume fills only 100, the 10% cap, and
            is marked partially filled.""",
            """To see the drawdown breaker, set the volume to 100,000 and buy 990 shares: that costs
            990 × 100.055 = $99,054.45 plus a $49.53 commission, leaving about $896.02 of cash. Now set
            the reference price to 97 and submit any order. Marked equity is 896.02 + 990 × 97 ≈
            $96,926, which is 96.9% of the starting amount, below the 97.5% limit, so the order is
            rejected and the account halts.""",
        ),
        prose(
            """**Open the broker.** Click the **Paper trading** tab. The header reads "QUANTA MOCK
            BROKER" and the stats show "CASH AVAILABLE", "SHARES HELD", "MARKED EQUITY" and "RISK
            STATE".""",
            """**Place a default order.** Keep **Buy**, **Order quantity** 10, **Reference price ($)**
            100, **Available bar volume** 1000, **Bid-ask spread (bps)** 5, **Slippage (bps)** 3,
            **Commission (bps)** 5 and **Price age (seconds)** 0, and click **Submit buy order**. The
            "ORDER AUDIT LOG" shows the fill at $100.06 a share and the commission.""",
            """**Hit the participation cap.** Set **Order quantity** to 150 and submit. Only 100 shares
            fill and the status reads partially filled.""",
            """**Trip each guard.** Set **Price age (seconds)** to 90 and submit ("Price data is
            stale."); restore it and set the spread to 150 ("Spread exceeds the 100 bps guard."); set
            the volume to 0 ("No available liquidity."); then follow the drawdown recipe above
            ("Drawdown circuit breaker triggered.").""",
            """**Reset.** Click the icon with aria "Reset paper account", read "Reset the paper
            account?" and choose **Reset simulation**.""",
            """**What you should see.** A rejection message for every guard you trip, a "Halted" risk
            state after the drawdown breaker, and the message "Circuit breaker is halted. Reset the
            paper account after reviewing the event." for any order placed before you reset.""",
        ),
        r"P_{\text{fill}}=P_{\text{ref}}\left(1\pm\frac{s+\sigma/2}{10^{4}}\right),\qquad q_{\text{fill}}=\min(q,\ 0.1\,V)",
        '''
reference = 100
spread = 5
slippage = 3
commission_bps = 5
price = reference * (1 + (slippage + spread / 2) / 10000)
print("Fill price:", price, "commission on 10 shares:", round(10 * price * commission_bps / 10000, 4))
print("Shares filled for 150 ordered against 1,000 volume:", min(150, 1000 * 0.10))
cost = 990 * price
fee = cost * commission_bps / 10000
cash = 100000 - cost - fee
equity = cash + 990 * 97
print("Cash after 990 shares:", round(cash, 2), "marked equity at 97:", round(equity, 2))
print("Equity as a share of the start:", round(equity / 100000 * 100, 2), "% against a 97.5% limit")
''',
        "Trigger every guard in the Paper trading tab, one at a time: participation cap, stale price, wide spread, no volume, insufficient cash and the drawdown breaker. Copy each message from the audit log and explain the risk each guard prevents.",
        "The participation cap fills at most 10% of the bar's volume, preventing the fantasy of trading any size at one price. The stale-price guard rejects prices older than 60 seconds, so decisions are not based on old information. The spread guard refuses spreads above 100 bps, where a quote is unreliable. Zero volume gives 'No available liquidity.', and an unaffordable order gives 'Insufficient cash for the simulated fill and fees.' The drawdown breaker halts the account once marked equity falls below 97.5% of the start, forcing a review before more trading, which is the control Knight Capital's systems lacked.",
        [
            (
                "With the default inputs, what is the buy fill price?",
                "$100.055, the reference price plus slippage and half the spread",
                "$100.00 exactly",
                "$100.08, adding the full spread and the slippage",
                "100 × (1 + (3 + 5 ÷ 2) ÷ 10,000) = 100.055. Only half the spread is paid on one side of the trade.",
            ),
            (
                "An order for 150 shares meets 1,000 shares of available volume. What happens?",
                "100 shares fill, the order is marked partially filled and the rest is not retried",
                "All 150 shares fill at once",
                "Nothing fills until more volume appears",
                "The broker fills at most 10% of the available volume and does not retry the remainder.",
            ),
            (
                "Price age is set to 90 seconds. What does the broker do?",
                "Rejects the order with 'Price data is stale.'",
                "Fills at the old reference price",
                "Waits 90 seconds and then fills",
                "Prices older than 60 seconds fail the stale-data guard, regardless of the other inputs.",
            ),
            (
                "After the drawdown breaker halts the account, how does trading resume?",
                "Only after resetting the paper account, once the event has been reviewed",
                "Automatically with the next order",
                "By lowering the commission",
                "A halted account rejects every order until it is reset, which forces a deliberate review.",
            ),
        ],
        [KNIGHT_SEC, FLASH, IG_ORDERS],
        "broker",
        "trigger every guard on purpose, one at a time (stale price, wide spread, no volume, insufficient cash and the drawdown breaker), and copy each rejection from the ORDER AUDIT LOG.",
        "30-minute session: 7 minutes reading how the mock broker fills and refuses orders, 9 minutes reproducing the fill and drawdown arithmetic and 14 minutes tripping each guard in the Paper trading tab; the broker never touches real money.",
    )
    # ------------------------------------------------------------------ 14.10
    add(
        "The AMM simulator: pool prices, fees and impermanent loss",
        "Quote swaps in a constant-product pool, separate spot price from execution price and impact, and compare full-range and concentrated liquidity against simply holding.",
        prose(
            """An automated market maker holds two assets and prices trades with a rule rather than an
            order book. In a constant-product pool the product of the reserves, x · y = k, stays the
            same after each trade, apart from fees. The spot price is the ratio of the reserves, but a
            trade moves along the curve, so the price you actually get is worse than spot, and the gap
            grows with the size of the trade. The fee is taken from the input and kept by the pool.""",
            """Liquidity providers face a different risk. When the external price moves, the pool's
            arbitrage-driven rebalancing leaves them with more of the asset that fell, and the value
            of their share trails simply holding the original tokens. That gap is called impermanent
            loss. Concentrating liquidity in a price range uses capital more efficiently inside the
            range but amplifies the loss, and a position outside its range stops earning. The
            simulator's comparisons exclude fees earned and gas costs.""",
        ),
        prose(
            """The default pool holds 10 ETH and 20,000 USDC, so spot is 2,000 USDC per ETH. Swapping 1
            ETH with a 0.3% fee returns 20,000 × 0.997 ÷ (10 + 0.997) ≈ 1,813.22 USDC, an execution
            price of $1,813.22 and a price impact of 1 − 1,813.22 ÷ 2,000 ≈ 9.34%. A 0.1 ETH swap returns
            about 197.43 USDC, an execution price near 1,974.32 and an impact of about 1.28%.""",
            """If the ETH price doubles, the full-range impermanent loss is 2√2 ÷ (1 + 2) − 1 ≈ −5.72%
            against holding. A position concentrated between 0.5× and 2× of the starting price loses
            about 19.53% against holding at the same move, more than three times as much, and it sits
            at the edge of its range. These are the simulator's default outputs.""",
        ),
        prose(
            """**Open the pool.** Click the **AMM simulator** tab: "CONSTANT-PRODUCT POOL", "Explore an
            ETH / USDC pool with x · y = k." Inputs are **ETH reserves** 10, **USDC reserves** 20000,
            **ETH to swap** 1 and **Swap fee (decimal)** 0.003.""",
            """**Read a quote.** Note "Estimated swap output", "Execution price", "Price impact
            including fee" and "Fee retained by pool". Change **ETH to swap** to 0.1 and then 5, and
            watch the impact grow faster than the size.""",
            """**Move the price.** Drag **Future price / initial price** from 2.00× down to 0.5× and up
            to 4×. Read "Full-range impermanent loss", "Concentrated position vs. holding" and
            "Position status".""",
            """**Change the range.** Under **Concentrated liquidity range**, set **Lower price ratio**
            and **Upper price ratio** wider and narrower. A range must contain the starting price, or
            the tool refuses it with "The starting price must lie within the liquidity range." """,
            """**Read the curve.** The chart under "LIQUIDITY PROVIDER ANALYSIS" draws full-range
            impermanent loss from 0.1× to about 4.9×. Find the price ratio where the loss is zero.""",
            """**What you should see.** Execution prices below spot for every sale of ETH, losses
            against holding for any price move away from 1×, and larger losses for narrower ranges.""",
        ),
        r"\Delta y=\frac{y\,\Delta x\,(1-\varphi)}{x+\Delta x\,(1-\varphi)},\qquad \text{IL}(r)=\frac{2\sqrt{r}}{1+r}-1",
        '''
from math import sqrt

eth = 10
usdc = 20000
fee = 0.003
spot = usdc / eth
for size in [0.1, 1, 5]:
    output = usdc * size * (1 - fee) / (eth + size * (1 - fee))
    execution = output / size
    print("Swap", size, "ETH: output", round(output, 2), "execution", round(execution, 2), "impact", round((1 - execution / spot) * 100, 2), "%")
for ratio in [0.5, 2, 4]:
    loss = 2 * sqrt(ratio) / (1 + ratio) - 1
    print("Price ratio", ratio, "full-range impermanent loss:", round(loss * 100, 2), "%")
''',
        "Quote swaps of 0.1, 1 and 5 ETH in the default pool and record output, execution price and impact for each. Then record full-range and concentrated losses at price ratios of 0.5, 2 and 4, and explain why the concentrated position loses more.",
        "The swaps return about 197.43, 1,813.22 and 6,653.32 USDC, with impacts near 1.3%, 9.3% and 33.5%, because each unit sold moves the pool's price further. Full-range impermanent loss is about −5.72% at both 0.5× and 2× and about −20% at 4×. A concentrated position provides the liquidity of a much larger full-range position inside its range, so the same price move rebalances it harder and its loss against holding is larger; outside the range it holds only one asset and stops earning fees, which this simulator excludes.",
        [
            (
                "Why does swapping 1 ETH into a 10 ETH / 20,000 USDC pool return only about 1,813 USDC?",
                "The trade moves the price along x · y = k, and the 0.3% fee is kept by the pool",
                "The pool charges a fixed 187 USDC fee on every swap",
                "The spot price is 1,813 USDC per ETH",
                "Spot is 2,000, but each unit sold lowers the price further along the curve, and the fee reduces the effective input.",
            ),
            (
                "What is the full-range impermanent loss if the ETH price doubles?",
                "About −5.72% against simply holding",
                "−50%, half the value",
                "Zero, because the price went up",
                "IL(2) = 2√2 ÷ 3 − 1 ≈ −5.72%. The loss appears for any move away from the starting price, up or down.",
            ),
            (
                "Why does the concentrated position lose about 19.53% while the full-range position loses 5.72% at the same move?",
                "Concentrated liquidity acts like a larger position inside its range, so the same move rebalances it harder",
                "Concentrated liquidity pays higher swap fees",
                "The concentrated calculation includes gas costs",
                "A narrow range provides more liquidity per unit of capital, which amplifies both fee income and impermanent loss.",
            ),
            (
                "What do the simulator's comparisons with holding leave out?",
                "Fees earned by the pool and gas costs",
                "The pool's reserves",
                "The price ratio",
                "The tool notes that fees and gas are excluded, so a real liquidity provider's result could be better or worse.",
            ),
        ],
        [UNISWAP, ANGERIS],
        "amm",
        "quote swaps of 0.1, 1 and 5 ETH, record each execution price and impact, then move the price slider from 0.5× to 4× and note where the concentrated position leaves its range.",
        "30-minute session: 8 minutes reading how a constant-product pool prices trades, 10 minutes reproducing the swap and impermanent-loss arithmetic and 12 minutes in the AMM simulator; the pool is a model and never touches real tokens.",
    )
    # ------------------------------------------------------------------ 14.11
    add(
        "Saved experiments, the notebook and historical imports",
        "Save and reopen experiments that reproduce their results, export your research, keep notes tied to lessons, and know what an imported dataset changes.",
        prose(
            """A saved experiment stores the code and the exact market settings behind the result on
            screen, plus its metrics when the output is fresh. It does not store bars, curves or
            trades: reopening it regenerates them from the seed, which is why the seed matters so
            much. Saving from the free lab or a lesson creates a new record each time; only a session
            opened from **Saved experiments** overwrites its own record. Your work is kept in your
            browser and synced to your account when you are signed in.""",
            """Two behaviours catch people out. Clicking another lab tab drops the experiment from the
            address, so returning to the Market sandbox shows the free lab rather than your
            experiment. And unsaved code is kept as a draft that wins over the saved code when the
            experiment reopens. The notebook holds your reasoning: notes you write, notes created from
            lesson assignments and case prompts, all exportable as Markdown. A historical dataset can
            replace the synthetic market, but none ships with Quanta, and an import's prices are used
            exactly as supplied.""",
        ),
        prose(
            """Suppose you import a file of 2,520 daily rows, ten years of prices, and leave **Horizon**
            at "3 years". The run reads the first 3 × 252 = 756 rows, which are the oldest three years
            of the file, not the latest. To test the most recent period you would have to import a
            file that starts where you want the test to begin.""",
            """A saved experiment is small because it stores settings rather than bars. Reopening it
            and running again must give the same metrics as the card in **Saved experiments**, so a
            mismatch is a signal that a draft or a changed setting is in play. These rules are what
            make an experiment reproducible by someone else, given the same code and settings.""",
        ),
        prose(
            """**Save an experiment.** Run any rule in the **Market sandbox**, then click **Save** in
            the footer. The dialog "Keep this experiment" asks for an **Experiment name** (up to 120
            characters, placeholder "My first market hypothesis"); click **Save experiment**. The icon
            "Export experiment" downloads quanta-experiment.json with the code, settings and
            result.""",
            """**Find and reopen it.** Open **Saved experiments** in the sidebar. Use **Search
            experiments** to filter by title, read the card's tags (data type, model, "Seed …" and
            date) and its CAGR and MAX DRAWDOWN, then click the title. The lab heading now shows the
            experiment's name. Run it and compare the metrics with the card.""",
            """**See the traps.** Click the **Valuation** tab and then **Market sandbox** again: the
            free lab appears. Reopen the experiment, edit the code without saving, and reload the page:
            your draft appears. Click the icon "Restore lesson code" to return to the saved code.""",
            """**Use the notebook.** Open **My notebook**, click **New note**, fill in **Title** and
            **Your note** and click **Save note**. On a lesson page, **Write in notebook** on the
            assignment creates a prefilled note. **Export notebook** saves quanta-notebook.md.""",
            """**Check the data source.** In **Parameters**, set **DATA SOURCE** to "Historical data".
            Without an import you will see a notice explaining that no historical dataset is
            installed; imports are added from the command line, as described in How Quanta works.""",
            """**What you should see.** Reopened experiments that reproduce their card metrics, a free
            lab after a tab click, and a notebook export that contains your notes in order.""",
        ),
        r"n_{\text{rows}}=252\,H,\qquad \text{rows used}=\{1,\dots,252H\}",
        '''
horizon_years = 3
rows_in_file = 2520
rows_used = 252 * horizon_years
print("Rows used:", rows_used, "of", rows_in_file)
print("Years skipped at the end of the file:", (rows_in_file - rows_used) / 252)
saved_items = ["code", "data type", "process", "scenario", "drift", "volatility", "horizon", "seed",
               "window", "capital", "commission", "slippage"]
print("Settings stored with an experiment (examples):", len(saved_items))
''',
        "Save two experiments that differ only by seed, export both, reopen each from Saved experiments and confirm that a fresh run reproduces its card's CAGR and maximum drawdown. Then write a notebook note explaining which settings an outsider would need to reproduce them.",
        "Each experiment stores its code and every market setting, including the seed, so a fresh run regenerates the same bars and the same metrics as its card. The two exports differ only in the seed field and in the results that follow from it. An outsider needs the code, the data source and process, scenario, drift, volatility, horizon, seed, moving-average window, capital and both cost settings; with those, the run is reproducible without the bars themselves, which is the point of saving settings rather than results.",
        [
            (
                "What does a saved experiment store?",
                "The code and the exact market settings, plus metrics if the output was fresh",
                "Every bar, curve and trade of the run",
                "Only the experiment's name",
                "Bars and trades are regenerated from the stored settings and seed when you run the experiment again.",
            ),
            (
                "You open an experiment, click the Valuation tab and return to the Market sandbox. What do you see?",
                "The free lab, because a tab click drops the experiment from the address",
                "The same experiment, unchanged",
                "An error page",
                "Tab clicks replace the address parameters, so reopen the experiment from Saved experiments.",
            ),
            (
                "An imported dataset has 2,520 daily rows and Horizon is 3 years. Which rows does a run use?",
                "The first 756 rows, the oldest three years in the file",
                "The last 756 rows, the most recent three years",
                "All 2,520 rows",
                "The run reads the first Horizon × 252 rows of an import, which are the earliest dates in the file.",
            ),
            (
                "How do you save a lesson's assignment answer to your notebook?",
                "Click Write in notebook on the assignment, complete the prefilled note and save it",
                "Copy it into Saved experiments",
                "It is saved automatically when you pass a practice question",
                "Write in notebook opens a note prefilled with the assignment, which you complete and save.",
            ),
        ],
        [TURING, PLOS, NUMPY_RANDOM],
        "market",
        "save two experiments that differ only by seed, export both JSON files, and confirm that reopening each from Saved experiments reproduces its own metrics.",
        "30-minute session: 7 minutes reading what experiments and notes keep, 8 minutes checking the horizon arithmetic and 15 minutes saving, reopening and exporting in the lab and notebook; the lab's default data is synthetic.",
    )
    # ------------------------------------------------------------------ 14.12
    add(
        "Capstone: a complete research loop from hypothesis to saved evidence",
        "Run the lab's research loop end to end: state a falsifiable hypothesis, fix the criteria, develop on some seeds, test on reserved seeds, and leave a trail another person can rerun.",
        prose(
            """The lab's sidebar names the research loop in four steps: state a hypothesis, change one
            assumption, read the evidence, keep a research trail. The capstone adds the two habits
            that make the loop honest. First, write the claim and the criteria that would reject it
            before you run anything. Second, split your seeds: develop and tune on one set, and keep
            another set untouched until the end, because results on the seeds that shaped your
            choices are optimistic by construction.""",
            """Every variant you try is a trial, and the trail records all of them, including the
            failures. A rule that holds up on reserved seeds under stated settings has passed a fair
            test on synthetic paths; it has not shown an edge in any real market. That modest claim
            is the correct output of the lab, and a reviewer can trust it precisely because it does
            not claim more.""",
        ),
        prose(
            """A worked plan: the hypothesis is that adding the condition "the 50-day average is above
            the 200-day average" to the trend rule gives a shallower maximum drawdown than buy and hold
            in the "Liquidity crisis · 2008-inspired" scenario. The rejection criterion is a shallower
            drawdown on fewer than four of five reserved seeds. You develop on seeds 42–46 with two
            variants of the window, which is 2 × 5 = 10 development runs, then run the chosen variant
            once on seeds 47–51, five more, for 15 trials in total.""",
            """The report states the hypothesis, criterion, seeds, settings, all 15 results and the
            decision, and it names what the lab does not model. The worksheet counts the twelve steps
            of the loop, from writing the hypothesis to exporting the notebook; a complete capstone
            ticks all twelve.""",
        ),
        prose(
            """**Write before you run.** In **My notebook**, create a note with your hypothesis, the
            metric, the comparison, the rejection criterion, the development seeds and the reserved
            seeds.""",
            """**Develop.** In the **Market sandbox**, choose the scenario and settings, write the
            rule, and run each variant on each development seed. Save each run with a name that
            includes the variant and seed, using **Save** and **Save experiment**.""",
            """**Test once.** Run the chosen variant on each reserved seed without changing anything
            else. Save these runs too.""",
            """**Decide.** Apply your written criterion to the reserved-seed results only, and record
            the decision whether or not it is the one you hoped for.""",
            """**Leave the trail.** In **Saved experiments**, check that every run is listed with its
            seed tag, export the ones your report cites, and click **Export notebook** to save your
            notes.""",
            """**What you should see.** A note written before the first run, one saved experiment per
            trial, a decision taken from the reserved seeds, and exports that let someone else rerun
            every number.""",
        ),
        r"N_{\text{trials}}=V\times S_{\text{dev}}+S_{\text{test}}",
        '''
variants = 2
development_seeds = 5
reserved_seeds = 5
trials = variants * development_seeds + reserved_seeds
print("Trials to report:", trials)
steps = ["hypothesis", "metric", "comparison", "rejection criterion", "seeds split",
         "settings fixed", "development runs", "experiments saved", "reserved test",
         "decision", "trail exported", "limits stated"]
print("Lab research loop steps:", len(steps), "of", 12)
''',
        "Complete one full research loop in the lab: write the hypothesis and rejection criterion first, develop on five seeds, test once on five reserved seeds, save every run, and export your notebook and the experiments your conclusion cites.",
        "A complete capstone shows the hypothesis and criterion dated before the first run, a list of every development and test run with its seed and settings, and a decision taken only from the reserved seeds, even if it rejects the idea. It reports all trials rather than the best one, exports the notebook and the experiments it cites so another person can rerun them, and states its limits: synthetic paths, fixed-slippage fills, long-or-cash trading and no evidence about real markets.",
        [
            (
                "Which statement is a testable hypothesis for the lab?",
                "A 200-day filter gives a shallower maximum drawdown than buy and hold on at least four of five reserved seeds in the 2008-inspired scenario",
                "Trend following is a good strategy",
                "This rule will make money",
                "A testable hypothesis names a rule, a metric, a comparison, a threshold and the conditions, so a result can reject it.",
            ),
            (
                "Why keep some seeds untouched until the end?",
                "They act as a fresh test that played no part in your choices",
                "Reserved seeds run faster",
                "The lab allows only five seeds a day",
                "Seeds used for tuning favour the chosen variant. Untouched seeds give a fairer estimate of how it behaves on new paths.",
            ),
            (
                "Your final rule beats buy and hold on the reserved seeds. What can you claim?",
                "It held up on fresh synthetic paths under the stated settings, which is not evidence of a real-market edge",
                "It will beat the real market",
                "It carries no risk",
                "The lab's evidence is about its generated markets. A fair test there is a reason for further work, not proof about real prices.",
            ),
            (
                "What belongs in the research trail besides the winning experiment?",
                "Every variant tried, with its seed, settings and result, including failures",
                "Only the best run",
                "Only screenshots of the charts",
                "Reporting every trial lets a reader judge selection bias and rerun any result.",
            ),
        ],
        [PBO, TURING, PLOS],
        "market",
        "run your capstone loop: write the hypothesis and criterion first, develop on five seeds, test on five reserved seeds, save every run and export your notebook.",
        "30-minute session: 5 minutes reading the loop, 5 minutes planning trials and 20 minutes running, saving and exporting the capstone in the lab; the lab's data is synthetic, so the capstone tests a process, not a market edge.",
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
