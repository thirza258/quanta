"""Build the shared, original lesson catalog. Re-run after editing lesson data."""

import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from c_hpc_course import build_c_hpc_trading
from course_references import attach_references
from econometrics_course import build_econometrics
from evaluation_course import build_algorithm_evaluation
from foundations import build_foundations
from intelligent_investor import build_intelligent_investor
from news_to_markets import build_news_to_markets
from quantitative_analysis import build_quantitative_analysis
from real_world_cases import attach_real_world_cases
from security_analysis import build_security_analysis
from stock_bots import build_stock_bots
from stock_ml_course import build_stock_ml
from strategy_course import build_strategy_lab
from track_exams import attach_exams
from web3_course import build_web3

tracks = [
    (
        "security-analysis",
        "Classical value investing",
        "The foundation of sound investment.",
        "Graham & Dodd · Security Analysis",
        "Foundational",
        "book",
        [
            (
                "Foundations of Graham & Dodd",
                "Investment, speculation, and the margin of safety",
                "An investment thesis begins with a claim about value and the evidence that could disprove it. Price is observable; intrinsic value is an estimate. Treat that estimate as a range built from conservative assumptions about assets, earnings, and the claims senior to common equity.",
                r"\text{Margin of safety} = 1 - \frac{P}{V}",
                "A company trades at $60. Your conservative, base, and optimistic estimates are $75, $100, and $125. Against the base estimate, the discount is 40%. Against the conservative estimate, it is only 20%. A 30% required margin would reject this purchase under the conservative case.",
                "Distinguish a quoted discount from a loss guarantee. Financial leverage, a deteriorating business, and a mistaken estimate can consume the entire cushion. Write down a disconfirming observation before considering a purchase.",
                "At a price of $60 and intrinsic value of $100, what is the margin of safety?",
                ["20%", "40%", "60%"],
                1,
                "Subtract price divided by value from one: 1 − 60/100 = 40%.",
                "valuation",
            ),
            (
                "Fixed-income & senior securities",
                "Coverage, priority, and the asset cushion",
                "A bond is a contractual claim, but the issuer must generate the cash to honor it. Examine payment priority, recurring earnings, and fixed charges across a full cycle. The common shareholder receives what remains after creditors and preferred holders are paid.",
                r"\text{Interest coverage} = \frac{\text{EBIT}}{\text{Interest expense}}",
                "An issuer reports EBIT of $120 million and annual interest expense of $30 million: coverage is 4×. In a recession, EBIT falls to $45 million and coverage becomes 1.5×. If leases add $15 million of fixed charges, an appropriately adjusted numerator and denominator are needed; interest coverage alone is incomplete.",
                "Reconcile accounting earnings to operating cash flow. Compare the weak-year coverage with covenants, refinancing dates, and liquid assets. Do not infer safety from a single strong year.",
                "EBIT is 90 and interest expense is 30. What is coverage?",
                ["2×", "3×", "4×"],
                1,
                "90 / 30 = 3 times.",
                "coverage",
            ),
            (
                "Normalized earning power",
                "Separate recurring performance from accounting noise",
                "Reported earnings combine durable operations, cyclical effects, and items unlikely to recur. Build an explicit bridge from reported profit to adjusted profit. Normalization should remove symmetrical gains and losses, rather than merely adding back inconvenient expenses.",
                r"\overline{\mathrm{EPS}} = \frac{1}{n}\sum_{t=1}^{n}\mathrm{EPS}^{\mathrm{adjusted}}_t",
                "Adjusted earnings per share over five years are $2, $3, $4, $3, and $3. Their arithmetic mean is $3. A one-time property gain of $2 per share in the most recent year would raise reported EPS to $5, but does not raise this normalized estimate.",
                "Check share-count changes, inflation, and changes in the business mix before averaging. Review inventory methods, provisions, stock compensation, and repeated restructuring costs. A frequently recurring “one-off” is an operating cost.",
                "Which item most clearly calls for a normalization adjustment?",
                [
                    "Ordinary employee salaries",
                    "Recurring rent",
                    "A gain from selling the headquarters",
                ],
                2,
                "A disposal gain generally does not describe recurring operating earning power.",
                "earnings",
            ),
            (
                "Balance sheet & asset-based valuation",
                "Net-current-asset value and the liquidation test",
                "Net-current-asset value gives no credit to fixed assets and deducts all liabilities and preferred claims. It is a deliberately demanding starting point. A separate liquidation analysis applies realistic recovery assumptions to receivables and inventory, recognizing collection costs and deteriorating stock.",
                r"\mathrm{NCAV/share} = \frac{\mathrm{Current\ assets}-\mathrm{Total\ liabilities}-\mathrm{Preferred}}{\mathrm{Diluted\ shares}}",
                "Cash of $40 million, receivables of $60 million, and inventory of $80 million sum to $180 million in current assets. With $70 million of liabilities and 10 million shares, NCAV is $11 per share. A two-thirds screen requires a price below $7.33. Haircuts of 15% to receivables and 40% to inventory lower adjusted value to $6.90 per share.",
                "Use actual filing availability dates. Deduct debt and other liabilities, including obligations that may not appear in current liabilities. Test whether cash burn can exhaust the cushion before value is realized.",
                "Why does NCAV subtract total liabilities?",
                [
                    "Common equity is junior to all liabilities",
                    "Only current liabilities are payable",
                    "Fixed assets are always worthless",
                ],
                0,
                "All creditors rank ahead of the residual common-equity claim.",
                "ncav",
            ),
            (
                "The Graham valuation formula",
                "A sensitivity tool, with explicit limitations",
                "The Graham heuristic links earnings and an assumed growth rate. It is useful for seeing how an estimate responds to assumptions; it is not a universal pricing law. Small changes to growth and bond yields can produce large swings in implied value, especially for cyclical firms.",
                r"V = \frac{\mathrm{EPS}\,(8.5+2g)\,4.4}{Y}",
                "With EPS of $4, growth g = 5 (five percentage points), and bond yield Y = 4.4 (also in percent), the formula gives $74. Raising Y to 6 reduces the estimate to about $54.27. Entering g = 0.05 would use the wrong units in this historical heuristic.",
                "Cap growth assumptions and compare with an independently derived DCF and asset valuation. Expensing versus capitalizing research and development changes earnings and reinvestment requirements; keep those adjustments consistent.",
                "In the historical Graham formula, 5% growth is entered as:",
                ["0.05", "5", "500"],
                1,
                "The formula uses percentage-point inputs for both growth and bond yield.",
                "graham",
            ),
        ],
    ),
    (
        "statistical-foundations",
        "Statistical foundations",
        "Turn uncertainty into measurable evidence.",
        "Quantitative Investment Analysis · Vol. I",
        "Foundational",
        "distribution",
        [
            (
                "Time value of money",
                "Discounting cash flows and terminal value",
                "Money available today can be invested. To compare future cash flows, discount each at a rate consistent with its timing, currency, and risk. Keep nominal cash flows with nominal rates and real cash flows with real rates.",
                r"PV = \sum_{t=1}^{T}\frac{CF_t}{(1+r)^t}+\frac{CF_{T+1}}{(r-g)(1+r)^T}",
                "A payment of $110 one year from now is worth $100 at a 10% discount rate. For a perpetuity paying $5 next year with growth of 2% and a required return of 7%, value is $100. The growing-perpetuity relation requires r > g.",
                "Model an explicit forecast period before applying terminal growth. Examine what fraction of value comes from the terminal term and report a discount-rate/growth sensitivity table.",
                "When is a growing-perpetuity valuation finite and positive?",
                ["When r > g", "When r = g", "When r < g"],
                0,
                "The denominator r − g must be positive.",
                "dcf",
            ),
            (
                "Probability distributions in finance",
                "Normal, lognormal, and heavy-tailed returns",
                "Prices cannot fall below zero in an unlevered cash asset, while returns can be negative. Lognormal price models arise from normal log returns. Real returns often exhibit heavier tails and time-varying volatility than a Gaussian model captures.",
                r"\log(S_T/S_0)\sim\mathcal{N}((\mu-\sigma^2/2)T,\sigma^2T)",
                "A one-day normal 99% loss threshold is about 2.33 standard deviations below the mean. If daily volatility doubles from 1% to 2%, the threshold roughly doubles. Heavy tails can still make realized losses beyond this threshold more frequent than the model predicts.",
                "Generate both GBM and jump-diffusion paths with the same seed. Compare downside quantiles, not just means. A model is an approximation whose assumptions need direct checks.",
                "Which feature most directly challenges a normal-return model?",
                [
                    "A positive asset price",
                    "More extreme returns than predicted",
                    "Daily observations",
                ],
                1,
                "Heavy tails imply more probability mass far from the mean.",
                "trend",
            ),
            (
                "Sampling & confidence intervals",
                "Estimate uncertainty, not just a point estimate",
                "A sample mean varies across samples. Its standard error reflects sample size and dispersion. Serial dependence reduces the effective information in a time series, so the independent-observation formula can be too optimistic.",
                r"\overline{x}\pm t_{\alpha/2,n-1}\frac{s}{\sqrt n}",
                "If 25 independent observations have a sample mean of 1% and a standard deviation of 5%, the standard error is 1%. A 95% interval uses about 2.064 standard errors, giving approximately −1.064% to 3.064%. The data do not establish a positive mean at this confidence level.",
                "For dependent returns, use a block bootstrap or a dependence-aware standard error. Record the resampling seed. A confidence interval describes repeated-sampling coverage, not a probability statement about a fixed parameter.",
                "All else equal, quadrupling independent sample size changes standard error by:",
                ["Doubling it", "Halving it", "Leaving it unchanged"],
                1,
                "Standard error scales as 1 / square root of n.",
                "trend",
            ),
            (
                "Hypothesis testing in markets",
                "Distinguish evidence from a lucky backtest",
                "State a null hypothesis before looking at the outcome. A p-value measures how incompatible an observation is with the null model; it is not the probability the null is true. Multiple strategy trials demand stronger evidence than a single pre-specified test.",
                r"t=\frac{\overline{x}-\mu_0}{s/\sqrt n}",
                "A test with a 5% significance threshold rejects true nulls about 5% of the time under its assumptions. If you independently test 20 null strategies, the probability of at least one false positive is 1 − 0.95²⁰, about 64%.",
                "Separate model development and final evaluation chronologically. Keep a research log of failed trials and apply family-wise or false-discovery controls appropriate to the research question.",
                "A Type I error is:",
                [
                    "Failing to reject a false null",
                    "Rejecting a true null",
                    "Using a small sample",
                ],
                1,
                "Type I error is a false positive.",
                "trend",
            ),
            (
                "Linear regression & correlation",
                "Estimate alpha, beta, and explained variation",
                "Regress asset excess returns on benchmark excess returns to estimate market exposure and an intercept. The slope describes association conditional on the model. Neither a significant coefficient nor a high R² establishes causation.",
                r"r_i-r_f=\alpha+\beta(r_m-r_f)+\epsilon_i",
                "An estimated daily alpha of 0.02% with a standard error of 0.03% has a t-statistic near 0.67. A positive estimate alone is weak evidence of persistent skill. A beta of 1.2 means a one-percentage-point benchmark move is associated with about a 1.2-point asset move in the fitted model.",
                "Align return timestamps and subtract the same-period risk-free return. Inspect residuals for heteroskedasticity and autocorrelation, and use appropriate uncertainty estimates.",
                "A beta of 1.2 primarily describes:",
                [
                    "Expected market sensitivity",
                    "A guaranteed 20% excess return",
                    "The fraction of winning trades",
                ],
                0,
                "Beta is the slope on benchmark excess returns.",
                "trend",
            ),
        ],
    ),
    (
        "econometrics",
        "Econometrics & factor models",
        "Understand the forces behind returns.",
        "Quantitative Investment Analysis · Applied econometrics extensions",
        "Intermediate",
        "factors",
        [
            (
                "Multiple regression & diagnostics",
                "Partial effects and fragile coefficients",
                "A multiple regression attributes returns to several explanatory variables at once. A coefficient is a partial association holding the included regressors constant. Correlated features can make estimates unstable even when predictions appear accurate.",
                r"\widehat{\beta}=(X^\top X)^{-1}X^\top y,\qquad \mathrm{VIF}_j=\frac{1}{1-R_j^2}",
                "If one factor is explained by the remaining factors with R² = 0.90, its VIF is 10. The inflated variance makes its separate contribution hard to identify. Use a numerically stable least-squares decomposition rather than explicitly inverting XᵀX.",
                "Inspect condition numbers and VIF, test residual variance and dependence, and document whether robust or HAC standard errors are used. Excluding a correlated feature changes the estimand.",
                "If R² for a regressor on other regressors is 0.8, VIF is:",
                ["1.25", "4", "5"],
                2,
                "1 / (1 − 0.8) = 5.",
                "trend",
            ),
            (
                "Time series & cointegration",
                "Stationarity, mean reversion, and volatility",
                "A stationary process has stable distributional properties over time. Two non-stationary price series may share a stationary linear combination; this is cointegration. Correlated returns alone are insufficient evidence for a mean-reverting price spread.",
                r"x_t=c+\phi x_{t-1}+\epsilon_t,\qquad |\phi|<1",
                "For an AR(1) with φ = 0.8, shocks decay geometrically. Its half-life is ln(0.5)/ln(0.8), approximately 3.1 periods. If φ = 1, the process is a random walk and the stationary mean-reversion interpretation fails.",
                "Estimate hedge ratios using training data only and apply the correct residual-based cointegration test. Stress-test structural breaks. GARCH models conditional variance, not a guarantee of directional predictability.",
                "Correlation alone establishes cointegration:",
                ["Always", "Only with daily data", "No"],
                2,
                "Cointegration concerns a stationary combination of integrated series.",
                "mean_reversion",
            ),
            (
                "Portfolio theory & factor pricing",
                "Diversification depends on covariance",
                "Portfolio variance depends on both individual risks and their co-movement. Estimated means are noisy, and unconstrained optimization can produce extreme weights. Shrinkage and position bounds trade theoretical fit for more stable allocations.",
                r"\sigma_p^2=w^\top\Sigma w,\qquad \sum_iw_i=1",
                "Two equally weighted assets each have 20% volatility. With zero correlation, portfolio volatility is about 14.14%. With correlation of one, it remains 20%. Diversification is lost precisely when assets begin moving together.",
                "Distinguish exposure to market, size, value, profitability, investment, and momentum from unexplained alpha. Align factor definitions and timing, and evaluate a constrained portfolio outside the estimation window.",
                "Lower correlation, all else equal, typically:",
                [
                    "Improves diversification",
                    "Guarantees positive returns",
                    "Raises each asset’s expected return",
                ],
                0,
                "Covariance contributes to total portfolio risk.",
                "trend",
            ),
            (
                "Risk & downside metrics",
                "Describe the loss distribution honestly",
                "Volatility treats gains and losses symmetrically. Drawdown, downside deviation, VaR, and expected shortfall answer different questions. Use them together and disclose the horizon, confidence level, and sign convention.",
                r"\mathrm{DD}_t=\frac{V_t}{\max_{s\le t}V_s}-1",
                "A portfolio rises from 100 to 120 and then falls to 90. The drawdown is −25%, despite being only 10% below its initial value. To recover from a 25% loss, it must gain 33.33%.",
                "Estimate historical VaR from daily loss quantiles, then compute expected shortfall from losses in the tail. Sparse samples make extreme quantiles unstable. In this workspace, VaR and CVaR are reported as positive loss magnitudes.",
                "A fall from a peak of 200 to 150 has a drawdown of:",
                ["−25%", "−33.3%", "−50%"],
                0,
                "(150 / 200) − 1 = −25%.",
                "trend",
            ),
            (
                "Backtest traps & research hygiene",
                "Control what the experiment is allowed to know",
                "A backtest should recreate the information set available at each decision. Revised financial statements, surviving-only universes, and same-bar execution all inflate apparent performance. The research process itself can overfit through repeated trials.",
                r"\mathrm{Position}_t=f(\mathcal{I}_{t-1})",
                "A filing describing the March quarter becomes public in May. A portfolio formed in April cannot use it. Similarly, a close-derived signal cannot earn the full return of the bar on which that close was observed.",
                "Archive point-in-time data and use next-open fills. Log strategy versions and split data chronologically. Reserve a final untouched test and disclose delisted-security coverage before interpreting a historical screen.",
                "A close-derived signal should first execute at:",
                [
                    "The same day’s open",
                    "The next available tradable price",
                    "The prior close",
                ],
                1,
                "Execution must occur after the signal becomes observable.",
                "trend",
            ),
        ],
    ),
    (
        "strategy-lab",
        "The strategy lab",
        "Put investment ideas to the test.",
        "Applied research · Four guided projects",
        "Applied",
        "lab",
        [
            (
                "The systematic net-net screen",
                "Translate balance-sheet discipline into a rule",
                "Build a universe at each rebalance date, select the latest statements actually published, and compute per-share net-current-asset value. A price below two-thirds of NCAV is a candidate screen, not a complete investment decision.",
                r"P_t<\frac{2}{3}\mathrm{NCAV}_t",
                "A stock at $6 with NCAV of $12 passes the valuation screen. If operating earnings are negative and quarterly cash burn is $2 per share, the apparent cushion can disappear quickly. Apply financial quality and liquidity filters before sizing.",
                "Use delisted securities and historical share counts. Compare gross and net performance, report turnover, and stress forced liquidation. The bundled synthetic data illustrates execution mechanics, not historical net-net profitability.",
                "A $9 stock with $12 NCAV passes the two-thirds screen:",
                ["Yes", "No", "Only when beta is low"],
                1,
                "The screen threshold is $8.",
                "ncav",
            ),
            (
                "Quality at a reasonable price",
                "Combine valuation and business quality",
                "Standardize earnings yield, invested-capital returns, and coverage within a contemporaneous universe. A composite score expresses an explicit preference rather than discovering an objective ranking. Avoid scale differences dominating the combination.",
                r"\mathrm{Score}_i=\tfrac13[z(E/P)_i+z(ROIC)_i+z(\mathrm{Coverage})_i]",
                "Suppose a company’s standardized scores are 1.2 for earnings yield, 0.6 for ROIC, and −0.3 for coverage. Its equal-weight composite is 0.5. A debt-heavy company may look cheap on P/E while failing the coverage test.",
                "Winsorize using training-universe thresholds and neutralize sector exposures only if the thesis requires it. Track accounting definitions and compare with a simple equal-weight baseline.",
                "Why standardize inputs before combining them?",
                [
                    "To guarantee alpha",
                    "To make feature scales comparable",
                    "To eliminate all outliers",
                ],
                1,
                "A common scale prevents arbitrary measurement units from dominating the score.",
                "trend",
            ),
            (
                "Statistical arbitrage pairs",
                "Trade a spread with explicit exit conditions",
                "A pairs strategy trades deviations in a statistically justified spread. Estimate a hedge ratio and a spread mean and scale from past observations. Entry and exit thresholds must be set before observing the test-period outcome.",
                r"z_t=\frac{s_t-\overline{s}_{t-L:t-1}}{\sigma_{s,t-L:t-1}}",
                "A spread of 8 with a trailing mean of 2 and standard deviation of 3 has z = 2. A mean-reversion rule might short the spread, while a risk rule exits if the relationship breaks. Hedging notional value alone does not ensure beta or dollar neutrality.",
                "Include short borrow, both legs’ commissions, and asynchronous fill risk. Re-estimate with a walk-forward schedule. Never assume that a historically stationary spread cannot undergo a permanent change.",
                "A z-score of 2 means the spread is:",
                [
                    "Two dollars above the mean",
                    "Two standard deviations above the mean",
                    "Certain to fall next period",
                ],
                1,
                "The z-score measures standardized deviation.",
                "mean_reversion",
            ),
            (
                "Cross-sectional machine learning",
                "Predict with a chronological research design",
                "Train regularized models on features known at prediction time. Cross-sectional ranking may be more stable than forecasting exact returns. The target horizon determines the embargo and overlap handling required between train and test sets.",
                r"\widehat{\beta}=\arg\min_\beta\left\{\|y-X\beta\|_2^2+\lambda\|\beta\|_2^2\right\}",
                "A 20-day forward return label for a training observation on January 31 contains February prices. A test fold beginning February 1 overlaps that information. Purge overlapping labels and apply an embargo appropriate to the design.",
                "Fit scaling and feature selection on training data only. Compare ridge and tree models with simple factor ranks. Report net turnover-adjusted outcomes and every material hyperparameter search.",
                "Where should a feature scaler be fitted?",
                [
                    "On the whole dataset",
                    "On the test set",
                    "On each training fold only",
                ],
                2,
                "Fitting preprocessing on test observations leaks information.",
                "trend",
            ),
        ],
    ),
    (
        "stock-bots",
        "Algorithmic & AI stock bots",
        "Engineer a disciplined execution system.",
        "Architecture · Risk · Paper trading",
        "Advanced",
        "bot",
        [
            (
                "Event-driven bot architecture",
                "Separate signals from execution and state",
                "A reliable bot separates market ingestion, signal generation, sizing, order routing, and the audit trail. Each event has an identity and a timestamp. Replaying an event must not create a second unintended order.",
                r"\mathrm{Event}\rightarrow\mathrm{Signal}\rightarrow\mathrm{Risk}\rightarrow\mathrm{Order}\rightarrow\mathrm{Fill}",
                "A process crashes after the broker accepts an order but before local confirmation. On restart, blindly retrying may double the position. Store an idempotent client order ID and reconcile broker state before retrying.",
                "Keep an append-only event log and a durable position snapshot. Treat missing acknowledgments as unknown state. This course uses a local mock broker, with no connection to a live brokerage account.",
                "What prevents duplicate orders after a retry?",
                [
                    "A faster polling loop",
                    "Idempotent order identifiers and reconciliation",
                    "Randomized position sizing",
                ],
                1,
                "Stable identities connect retries to the same intended order.",
                "trend",
            ),
            (
                "Rule-based strategy bots",
                "Build a rebalancer with observable rules",
                "A rule-based bot transforms an information event into a target portfolio. Rebalancing computes the difference between current and desired holdings. Signal generation and execution frequency need not be the same.",
                r"\Delta q_i=\frac{w_i^{*}V}{P_i}-q_i",
                "A $100,000 portfolio targets a 10% allocation to an asset priced at $50. Its target is 200 shares. If 120 shares are already held, the raw order is 80 shares before commissions, lot sizes, and cash constraints.",
                "Schedule filing-driven value screens, spread-driven pairs rules, or trend rules independently. Test stale data and reject oversized orders. Log the inputs that produced each target.",
                "With a target of 200 shares and 120 held, the rebalance quantity is:",
                ["320", "200", "80"],
                2,
                "Trade the difference between target and current holdings.",
                "trend",
            ),
            (
                "AI decision layers",
                "Keep model suggestions inside deterministic limits",
                "A predictive model ranks opportunities; a qualitative model can summarize source text and identify risks. Neither should bypass position limits, data provenance checks, or the order approval policy. Treat model output as untrusted structured input.",
                r"\mathrm{AllowedOrder}=\mathrm{Signal}\cap\mathrm{DataChecks}\cap\mathrm{RiskLimits}",
                "An LLM identifies an accounting concern in a filing. Save the cited passage, source date, schema version, and confidence rationale. A deterministic rule can veto the candidate, but a fluent summary is not verified financial evidence.",
                "Evaluate on held-out filings and include adversarial text in tests. Track drift and abstentions. Provider credentials and a separately validated model are required for live inference; the local simulator uses explicit deterministic rules.",
                "Which component should enforce hard exposure limits?",
                [
                    "The LLM’s prose response",
                    "A deterministic risk layer",
                    "The chart renderer",
                ],
                1,
                "Hard constraints must be enforced independently of probabilistic model output.",
                "trend",
            ),
            (
                "Position sizing & circuit breakers",
                "Design the failure path before the happy path",
                "Position sizing couples expected edge to uncertainty and loss tolerance. The Kelly fraction is highly sensitive to estimated probabilities and payoff ratios. Fractional sizing and strict caps reduce exposure to estimation error.",
                r"f^*=\frac{pb-(1-p)}{b}",
                "With win probability p = 0.55 and win/loss payoff b = 1, full Kelly is 10%. Half Kelly is 5%. If p is actually 0.48, the strategy has negative expected edge; leverage does not repair a mistaken estimate.",
                "Set independent drawdown, concentration, stale-data, and spread checks. Persist the halt state and require an explicit reset after investigation. A stop order cannot guarantee its trigger price in a gap.",
                "For p = 0.55 and b = 1, half Kelly is:",
                ["5%", "10%", "55%"],
                0,
                "Full Kelly is 0.10, so half Kelly is 0.05.",
                "kelly",
            ),
            (
                "Mock broker & paper deployment",
                "Observe fees, partial fills, and rejected orders",
                "Paper trading checks operational behavior using simulated fills. An order acknowledgment is not a fill. Track submitted, partially filled, filled, cancelled, and rejected states, and reconcile cash and holdings after every fill.",
                r"\mathrm{Cash}_{t+1}=\mathrm{Cash}_t-qP-\mathrm{Commission}",
                "Buying 10 shares at $100 with a $1 commission reduces cash by $1,001. With only $500 cash, the broker must reject or resize the request according to an explicit policy. A spread and participation cap make simulated execution less optimistic.",
                "Use the mock-broker panel in the Strategy Lab to place orders. Adjust slippage and available volume and inspect the resulting partial fills. Paper results omit many venue and market-impact effects.",
                "A partially filled order should:",
                [
                    "Be treated as completely filled",
                    "Retain its remaining quantity",
                    "Erase its fill history",
                ],
                1,
                "Order state records both executed and remaining quantity.",
                "trend",
            ),
        ],
    ),
    (
        "web3",
        "Web3 & crypto economics",
        "Apply financial rigor to on-chain markets.",
        "Tokenomics · DeFi · Crypto execution",
        "Advanced",
        "crypto",
        [
            (
                "Tokenomics & monetary theory",
                "Separate protocol activity from tokenholder value",
                "A protocol can be useful without distributing economic value to its token. Examine issuance, unlocks, fee routing, burns, governance rights, and who bears operating costs. Nominal staking yield includes compensation for dilution and risk.",
                r"MV=PY",
                "A staking token pays 8% more units while total token supply grows 6%. A simple dilution-adjusted unit yield is 1.08/1.06 − 1, about 1.89%, before price changes, fees, slashing, and taxes. This is not a risk-free return.",
                "Read the actual economic rights and contract controls. Never treat proof-of-stake yield as literally risk-free: validator, slashing, liquidity, governance, and smart-contract risks remain.",
                "An 8% staking yield with 6% supply growth implies approximately:",
                [
                    "8% dilution-adjusted yield",
                    "1.89% dilution-adjusted unit yield",
                    "A guaranteed 2% dollar return",
                ],
                1,
                "Adjust the units by total supply growth: 1.08 / 1.06 − 1.",
                "amm",
            ),
            (
                "AMMs & impermanent loss",
                "Derive swap output from the invariant",
                "A constant-product pool quotes trades from reserves rather than matching an order book. A large swap moves the marginal price. Trading fees change the effective input, while liquidity providers bear exposure to relative price movements.",
                r"\Delta y=\frac{y\,\Delta x(1-f)}{x+\Delta x(1-f)},\qquad IL(k)=\frac{2\sqrt{k}}{1+k}-1",
                "A pool contains 10 ETH and 20,000 USDC. Selling 1 ETH with no fee returns 20,000/11, about 1,818.18 USDC. The average execution price is worse than the initial 2,000 USDC marginal price. If the external price doubles, full-range impermanent loss is about 5.72% relative to holding.",
                "Use the AMM simulator to vary trade size, fees, and relative price. Full-range IL omits fee income. Concentrated positions need separate piecewise inventory accounting inside and outside their price ranges.",
                "A larger trade relative to reserves generally causes:",
                ["Less price impact", "More price impact", "No price impact"],
                1,
                "The reserve curve becomes less favorable as the trade moves along it.",
                "amm",
            ),
            (
                "Crypto arbitrage & market neutrality",
                "A hedged position still has several kinds of risk",
                "Cash-and-carry pairs a long spot position with a short derivative. Positive funding may compensate the short, but the rate can reverse. Delta neutrality does not eliminate liquidation, basis, collateral, custody, or venue risk.",
                r"\mathrm{NetCarry}\approx\mathrm{Funding}-\mathrm{Borrow}-\mathrm{Fees}-\mathrm{BasisChange}",
                "At a constant 0.01% funding rate every eight hours, a simple annualized rate is 0.0001 × 3 × 365 = 10.95%. This assumes unchanged rates, no fees, and no compounding; it is not a forward yield guarantee.",
                "Stress collateral in a price gap, include liquidation rules, and avoid relying on transfers between venues during a crisis. Study MEV as an execution cost and protection problem; no adversarial trading is executed by this platform.",
                "Delta neutrality removes:",
                [
                    "All investment risk",
                    "First-order directional exposure, approximately",
                    "Exchange default risk",
                ],
                1,
                "Other risks remain even when spot-price sensitivity is hedged.",
                "funding",
            ),
            (
                "Crypto execution engineering",
                "Track nonces, confirmations, and transaction costs",
                "On-chain execution is an asynchronous state machine. A submitted transaction can remain pending, be replaced, or be removed by a reorganization. Nonces order an account’s transactions; a nonce manager must coordinate concurrent senders.",
                r"\mathrm{EffectiveGasPrice}=\min(\mathrm{MaxFee},\mathrm{BaseFee}+\mathrm{PriorityFee})",
                "With a base fee of 20 gwei, a priority fee of 2 gwei, and a max fee of 30 gwei, the effective price is 22 gwei. If the base fee rises above the cap, the transaction cannot be included on those terms. A higher tip still cannot guarantee inclusion.",
                "Persist transaction intents before signing, reconcile receipts, and choose a confirmation policy. Keep keys outside lesson code. The local course provides simulation only and never requests a wallet seed phrase.",
                "A priority fee guarantees next-block inclusion:",
                ["Yes", "No", "Only for swaps"],
                1,
                "Inclusion also depends on fee caps, block capacity, ordering, and network conditions.",
                "amm",
            ),
            (
                "Crypto stress testing",
                "Model liquidity loss and collateral shortfalls",
                "A stress test asks what happens under an adverse scenario rather than estimating its likelihood. Model a rapid price drop, collateral haircuts, widening spreads, and the inability to rebalance. Correlations and liquidity often deteriorate together.",
                r"\mathrm{HealthFactor}=\frac{\mathrm{CollateralValue}\times\mathrm{LiquidationThreshold}}{\mathrm{DebtValue}}",
                "Collateral worth $10,000, a liquidation threshold of 80%, and debt of $5,000 imply a health factor of 1.6. A 50% collateral-price drop lowers it to 0.8, before interest and fees, potentially triggering liquidation.",
                "Use the flash-crash scenario and evaluate the path to liquidation, not merely the final price. For LP positions compare fee income with inventory loss, gas, and execution slippage.",
                "A health factor below one commonly indicates:",
                [
                    "Excess collateral",
                    "Potential liquidation eligibility",
                    "A guaranteed profitable arbitrage",
                ],
                1,
                "Collateral adjusted by the liquidation threshold no longer covers debt.",
                "liquidation",
            ),
        ],
    ),
]
base = 'def strategy(data):\n    # Signal at the close; execution at the next open.\n    return data["close"] > data["sma_50"]\n'
codes = {
    "valuation": 'price = 60\nintrinsic_value = 100\nmargin = 1 - price / intrinsic_value\nprint("Margin of safety:", round(margin * 100, 2), "%")\n',
    "coverage": 'ebit = 90\ninterest = 30\nprint("Interest coverage:", ebit / interest)\n',
    "earnings": 'earnings = [2, 3, 4, 3, 3]\nprint("Normalized EPS:", sum(earnings) / len(earnings))\n',
    "ncav": 'cash = 40\nreceivables = 60\ninventory = 80\nliabilities = 70\nshares = 10\nncav = (cash + receivables + inventory - liabilities) / shares\nprint("NCAV / share:", round(ncav, 2))\nprint("Screen price:", round(ncav * 2 / 3, 2))\n',
    "graham": 'eps = 4\ngrowth = 5\nbond_yield = 4.4\nvalue = eps * (8.5 + 2 * growth) * 4.4 / bond_yield\nprint("Graham value:", round(value, 2))\n',
    "dcf": 'cash_flow = 5\ndiscount_rate = 0.07\ngrowth = 0.02\nprint("Perpetuity value:", cash_flow / (discount_rate - growth))\n',
    "kelly": 'probability = 0.55\npayoff = 1\nkelly = (probability * payoff - (1 - probability)) / payoff\nprint("Half Kelly:", round(kelly / 2, 4))\n',
    "amm": 'from math import sqrt\nx = 10\ny = 20000\ntrade = 1\nfee = 0.003\noutput = y * trade * (1 - fee) / (x + trade * (1 - fee))\nratio = 2\nil = 2 * sqrt(ratio) / (1 + ratio) - 1\nprint("Swap output (USDC):", round(output, 2))\nprint("Impermanent loss (%):", round(il * 100, 2))\n',
    "funding": 'funding_rate = 0.0001\nprint("Simple annual carry (%):", funding_rate * 3 * 365 * 100)\n',
    "liquidation": 'collateral = 10000\nthreshold = 0.8\ndebt = 5000\ncrash = 0.5\nprint("Initial health:", collateral * threshold / debt)\nprint("Stressed health:", collateral * (1 - crash) * threshold / debt)\n',
}
catalog = []
for index, (slug, title, description, source, level, icon, lessons) in enumerate(tracks, 1):
    modules = []
    for j, (
        name,
        subtitle,
        intro,
        formula,
        example,
        protocol,
        question,
        options,
        answer,
        explanation,
        kind,
    ) in enumerate(lessons, 1):
        code = (
            codes.get(kind, "")
            + ("\n" if kind in codes else "")
            + (base.replace(" > ", " < ") if kind == "mean_reversion" else base)
        )
        modules.append(
            {
                "id": f"{index}.{j}",
                "title": name,
                "subtitle": subtitle,
                "minutes": 12 + (j * 3) % 13,
                "content": f"## The idea\n\n{intro}\n\n$$\n{formula}\n$$\n\n## A worked example\n\n{example}\n\n## Research protocol\n\n{protocol}\n\n### In the sandbox\n\nRun the lesson template, then change one assumption at a time. Record the parameter, the observed change, and whether the result supports your original claim. All default price paths are synthetic, and the accompanying trend strategy demonstrates execution mechanics. Its returns do not validate the lesson’s valuation thesis.",
                "formula": formula,
                "exercise": {
                    "question": question,
                    "options": options,
                    "answer": answer,
                    "explanation": explanation,
                },
                "code": code,
                "kind": kind,
            }
        )
    catalog.append(
        {
            "id": slug,
            "number": index,
            "title": title,
            "description": description,
            "source": source,
            "level": level,
            "icon": icon,
            "modules": modules,
        }
    )
attach_exams(catalog)
for index, expanded in [
    (0, build_security_analysis()),
    (1, build_quantitative_analysis()),
    (2, build_econometrics()),
    (3, build_strategy_lab()),
    (4, build_stock_bots()),
    (5, build_web3()),
]:
    # Preserve the first exercise and its answer key for legacy saved submissions.
    original = {m["id"]: m for m in catalog[index]["modules"]}
    for module in expanded["modules"]:
        if module["id"] in original:
            exercise = original[module["id"]]["exercise"]
            module["exercise"] = exercise
            module["exercises"][0] = exercise
    catalog[index] = expanded
catalog.append(build_stock_ml())
catalog.insert(0, build_foundations())
catalog.insert(2, build_news_to_markets())
catalog.insert(
    next(i for i, track in enumerate(catalog) if track["id"] == "security-analysis"),
    build_intelligent_investor(),
)
catalog.insert(
    next(i for i, track in enumerate(catalog) if track["id"] == "stock-bots") + 1,
    build_c_hpc_trading(),
)
catalog.append(build_algorithm_evaluation())
attach_references(catalog)
attach_real_world_cases(catalog)
output = Path(__file__).resolve().parents[2] / "content/catalog/curriculum.json"
output.parent.mkdir(exist_ok=True)
# Dev reloaders and image builders must see either the old or complete new catalog.
with NamedTemporaryFile("w", encoding="utf-8", dir=output.parent, delete=False) as pending:
    pending.write(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")
temporary = Path(pending.name)
try:
    temporary.chmod(0o644)
    temporary.replace(output)
finally:
    temporary.unlink(missing_ok=True)
