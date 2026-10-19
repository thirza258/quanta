"""Research extensions for Algorithmic & AI stock bots.

Each entry maps a lesson ID to (body, sources). A source is
(kind, authors, year, title, url, what it contributes); see research_depth.py.
Every figure was checked against a verbatim snippet from its source before merging.
"""

NOTES = {
    "5.6": (
        r"""A decision contract should state how many alternatives will be tried, because that count changes what a good result means. Bailey, Borwein, López de Prado and Zhu make the point with a random walk. They generated 1,000 daily prices, about four years, searched a mesh of 8,800 combinations of entry day, holding period, stop loss and side, and the best combination showed an annualized Sharpe ratio of 1.27 even though the series contains no pattern. Their rule of thumb is that five years of data supports no more than 45 independent configurations before a skill-less winner with a Sharpe ratio near 1 becomes almost guaranteed, and they describe that length as necessary but not sufficient.

Edges also fade once they are known. McLean and Pontiff studied 97 predictors taken from published papers and found portfolio returns 26% lower out of sample and 58% lower after publication. As an illustration of our own, not a forecast, a 58% haircut on Harbor's 12 basis points of gross benefit leaves about 5, already below the 9 basis points of assumed costs.

The cost line is an assumption about a particular trader. Frazzini, Israel and Moskowitz used nearly a trillion dollars of one large manager's live trades across 19 developed equity markets from 1998 to 2011 and found actual costs under a tenth of earlier estimates. They attribute the gap to two things: earlier studies priced the average investor, and the portfolios they tested were not designed with costs in mind. That manager is far larger and more sophisticated than a paper bot, so its numbers are not a template for Harbor. They do show that 9 basis points needs a named trader, size and portfolio design behind it.

Exercise: add three lines to Harbor's contract before any code exists. State the maximum number of variants you will compare, the history length that supports that number, and a pessimistic case that combines a decay haircut with 6 basis points of slippage. If the idea fails the pessimistic case, do not write the loop.""",
        [
            ('paper', 'Bailey, Borwein, López de Prado & Zhu', 2014, 'Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance', 'https://doi.org/10.1090/noti1105',
             'Shows with a random-walk experiment and a minimum-backtest-length rule how the number of configurations tried inflates in-sample Sharpe ratios.'),
            ('paper', 'McLean & Pontiff', 2016, 'Does Academic Research Destroy Stock Return Predictability?', 'https://doi.org/10.1111/jofi.12365',
             'Measures how much the returns of 97 published predictors fall out of sample and after publication.'),
            ('paper', 'Frazzini, Israel & Moskowitz', 2012, 'Trading Costs of Asset Pricing Anomalies', 'https://doi.org/10.2139/ssrn.2294498',
             'Live institutional trade data showing actual costs far below earlier estimates, and why estimates depend on who trades and how portfolios are built.'),
        ],
    ),
    "5.1": (
        r"""Two clocks sit behind every event a bot receives. Akidau and co-authors, describing a model for processing unbounded and out-of-order data, define event time as when an event actually occurred and processing time as when the pipeline observes it. They stress that the skew between the two is inherent and keeps changing, and that a system usually lacks the knowledge to build a fully correct watermark, its running estimate of how complete the data is. A bot faces the same problem with a sharper edge, because a dashboard can quietly revise a late number but an order cannot be retracted. Our inference is that the late-event rule belongs in the specification: say in advance what happens to an event that arrives after the decision it should have informed.

Identity needs the same discipline. The FIX standard for electronic order messages requires a client order ID to be unique within a single trading day and advises firms that trade across days to embed a date in it. A separate PossResend field marks a message that may carry information already sent under another sequence number. Harbor's key of strategy version, symbol and decision timestamp fits that pattern, but each broker's guarantee has its own scope, so read the adapter's contract.

Replay and live trading also differ more than the pipeline diagram suggests. QuantConnect's LEAN documentation says algorithm events fire synchronously in backtests, while in live trading order events fire immediately from the brokerage thread, asynchronously. Its own example is a limit order on hourly data that fills between bars. The ABIDES simulator of Byrd and co-authors makes such timing visible instead: every agent talks to the exchange through messages with configurable network latencies, in a design modelled on Nasdaq's ITCH and OUCH protocols.

Exercise: replay the feed E101, E101, E102 three ways. Run it in order, with the duplicate delayed until after E102, and with a simulated crash between broker acceptance and the stored acknowledgement. Each run should end with exactly two intents and the same ledger. Any difference exposes a hidden dependence on arrival order or on in-memory state.""",
        [
            ('paper', 'Akidau et al.', 2015, 'The Dataflow Model', 'https://doi.org/10.14778/2824032.2824076',
             'Defines event time versus processing time for out-of-order streams and explains why completeness estimates (watermarks) are heuristic.'),
            ('docs', 'FIX Trading Community', None, 'ClOrdID field definition, FIX Latest', 'https://fiximate.fixtrading.org/en/FIX.Latest/tag11.html',
             'Standard definition of the client order ID, including the day-level uniqueness requirement and the advice to embed a date.'),
            ('docs', 'QuantConnect', None, 'Algorithm Engine', 'https://www.quantconnect.com/docs/v2/writing-algorithms/key-concepts/algorithm-engine',
             'Documents how one engine triggers events synchronously in backtests but fires order events asynchronously in live trading.'),
            ('arxiv', 'Byrd, Hybinette & Balch', 2019, 'ABIDES: Towards High-Fidelity Market Simulation for AI Research', 'https://arxiv.org/abs/1904.12066',
             'A discrete-event market simulator in which agents interact only through messages with configurable latencies, modelled on Nasdaq protocols.'),
        ],
    ),
    "5.7": (
        r"""Treat the trading clock as data. The NYSE's published calendar lists Friday 3 July 2026 as a holiday (Independence Day observed) and early 1:00 p.m. Eastern closes on Friday 27 November and Thursday 24 December 2026. Sessions also differ by venue: the core session runs from 9:30 a.m. to 4:00 p.m., but NYSE Arca's early session starts at 4:00 a.m. and late trading runs until 8:00 p.m. Our inference for Harbor: on an early-close day a completed daily bar exists three hours sooner than usual, so a calendar that assumes a 4:00 p.m. close delays the signal, and one that assumes a session on 3 July may mistake a missing bar for a zero return.

Feeds also stamp events with more than one clock. Bartlett and McCrary used the microsecond timestamps recorded by the two centralized processors that consolidate U.S. exchange quotes and trades. In a sample running from August 2015 to June 2016 they found average reporting latencies of 1.13 milliseconds for quotes and 22.84 milliseconds for trades, and they note that the exchanges' own participant timestamps were recorded only in milliseconds. Which clock a freshness limit such as the lesson's 750 milliseconds uses is therefore part of the data contract.

Documents have the same problem. Under the SEC's Regulation S-T, an electronic filing submitted after 5:30 p.m. Eastern is deemed filed on the next business day, although some insider and ownership forms get a 10 p.m. cutoff. A filing date is a legal label, not a clock reading, so a bot that stores only the date cannot say whether the document was readable at 10:00 a.m. that day. Our suggestion: store the acceptance time when the source provides one, and otherwise treat the document as usable only after the full filing date has passed.

Exercise: extend Harbor's fixtures with a bar on Friday 27 November 2026 that completes at 1:00 p.m., a Friday 3 July 2026 with no session, and a filing accepted at 6:00 p.m. Eastern. For each, write down whether the bot abstains, delays or labels the result research-only, and which timestamp it used.""",
        [
            ('official', 'NYSE', None, 'Holidays & Trading Hours', 'https://www.nyse.com/trade/hours-calendars',
             "The exchange's own 2026 to 2028 holiday and early-close schedule, with session windows for each NYSE venue."),
            ('paper', 'Bartlett & McCrary', 2016, 'How Rigged Are Stock Markets?: Evidence From Microsecond Timestamps', 'https://doi.org/10.3386/w22551',
             "Uses the SIPs' microsecond timestamps to measure how late consolidated quotes and trades are reported compared with exchange direct feeds."),
            ('official', 'U.S. SEC · eCFR', None, '17 CFR 232.13: Date of filing; adjustment of filing date', 'https://www.ecfr.gov/current/title-17/chapter-II/part-232/section-232.13',
             'The rule that fixes when an electronic EDGAR filing counts as filed, including the 5:30 p.m. Eastern cutoff and its exceptions.'),
        ],
    ),
    "5.8": (
        r"""Start with what a window counts. The pandas documentation says a rolling window given as an offset, such as twenty days, defaults to a minimum of 1 observation, while an integer window defaults to its full size. Both can be called a twenty-day average, but by default only the integer version has a warm-up state: the offset version returns a one-close "average" on the first day. The default window also includes its last point, the current bar. Our inference is that a feature specification should state the minimum observations and whether the current bar is inside the window.

Kaufman and co-authors define leakage as information about the prediction target entering the data when it should not legitimately be there, and they propose a data-management approach they call learn-predict separation. For a bot, "legitimately" means stamped before the decision time, so the lesson's final close of 104 is off limits to an earlier decision. A prefix test follows (our suggestion): compute each feature on the full history, then again on the history cut at the decision time. Any difference signals leakage or a revised past.

Research and live code can also drift apart. Google's Rules of Machine Learning define training-serving skew as a difference between performance during training and during serving, and list three causes: different data handling in the two pipelines, a change in the data between training and serving, and a feedback loop. Rule #29 says to save the features used at serving time and log them for training. Rule #37 says the same example at training and at serving should give exactly the same result, so a discrepancy probably indicates an engineering error. Pineau and co-authors, reporting on the NeurIPS 2019 reproducibility program, define reproducibility as obtaining similar results from the same code and data; the lesson's fixture applies that definition to a single feature.

Exercise: log Harbor's live feature vector with its version, replay the same closes through the research function, and require identical values, including a missing day and the first warm-up bar.""",
        [
            ('docs', 'pandas', None, 'pandas.DataFrame.rolling', 'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html',
             'Documents the min_periods defaults for offset and integer windows and the closed argument that decides whether the current bar is inside a rolling window.'),
            ('paper', 'Kaufman, Rosset, Perlich & Stitelman', 2012, 'Leakage in data mining', 'https://doi.org/10.1145/2382577.2382579',
             'Defines leakage as information that should not be legitimately available and proposes a learn-predict separation in data management.'),
            ('docs', 'Google', None, 'Rules of Machine Learning: Best Practices for ML Engineering', 'https://developers.google.com/machine-learning/guides/rules-of-ml',
             'Defines training-serving skew, recommends logging serving-time features for training (Rule #29) and treats a train/serve mismatch as an engineering error (Rule #37).'),
            ('arxiv', 'Pineau et al.', 2020, 'Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program)', 'https://arxiv.org/abs/2003.12206',
             'Defines reproducibility as similar results from the same code and data and reports a code policy, community challenge and checklist used to promote it.'),
        ],
    ),
    "5.2": (
        r"""Treat the broker's open quantity as the pending term in the lesson's formula. The FIX standard defines CumQty as the total quantity filled and LeavesQty as the quantity open for further execution, equal to OrderQty minus CumQty unless the order has reached a state that ends it: Canceled, DoneForTheDay, Expired, Calculated or Rejected. For Harbor's 50-share buy with 20 filled, that is 30. A cancel request still awaiting an answer is not on that list, so our inference is that its open quantity stays until the broker reports Canceled. Test it: held plus open quantity is 170 before and after the partial fill, and only a confirmed cancel moves the shortfall from 30 to 60.

A rule-based bot also needs conditions that a program can evaluate, and the research record shows why. Lo and co-authors observed that chart patterns are often in the eye of the beholder, so they replaced chart reading with nonparametric kernel regression and applied it to U.S. stocks from 1962 to 1996. They compared the unconditional distribution of daily returns with the distribution conditioned on indicators such as head-and-shoulders and double bottoms, and found that over the 31-year sample several indicators provided incremental information and might have some practical value. Our inference is that Harbor's benchmark should follow the same design (returns after the rule fires against returns on all dates, under identical costs), and that information in a return distribution must still survive turnover.

Turnover is where that is decided. Gerhold and co-authors study a long-horizon investor facing small proportional costs and show that, to first order, the liquidity premium, the model's measure of what illiquidity costs the investor, equals the spread times share turnover times a universal constant. Our inference is that a no-trade band acts on the turnover factor, so its width belongs in the specification, fixed before any results are seen.

Exercise: replay the 200/120/50/20 sequence with a delayed cancel confirmation, and assert that the projected holding changes only when a broker report arrives.""",
        [
            ('docs', 'FIX Trading Community', None, 'LeavesQty field definition, FIX Latest', 'https://fiximate.fixtrading.org/en/FIX.Latest/tag151.html',
             'Standard definition of open order quantity as OrderQty minus CumQty, with the list of terminal order states in which it may be zero.'),
            ('paper', 'Lo, Mamaysky & Wang', 2000, 'Foundations of Technical Analysis: Computational Algorithms, Statistical Inference, and Empirical Implementation', 'https://doi.org/10.1111/0022-1082.00265',
             'Turns subjective chart patterns into an algorithm and compares conditional with unconditional return distributions for U.S. stocks over 1962 to 1996.'),
            ('arxiv', 'Gerhold, Guasoni, Muhle-Karbe & Schachermayer', 2011, 'Transaction Costs, Trading Volume, and the Liquidity Premium', 'https://arxiv.org/abs/1108.1167',
             'Shows that, to first order, the cost of illiquidity in a small-cost model equals the spread times share turnover times a universal constant.'),
        ],
    ),
    "5.9": (
        r"""Breakouts have a long evidence trail and a long list of ways to fool yourself. Brock and co-authors tested a moving-average rule and a trading-range break, the breakout in this lesson, on the Dow Jones index from 1897 to 1986. They judged both against bootstrapped null models (a random walk, an AR(1), GARCH-M and exponential GARCH), found that buy signals produced higher returns than sell signals, and reported negative returns after sell signals. Two habits are worth copying: split outcomes by signal state, and measure a rule against simulated series that contain no edge.

George and Hwang found that nearness to the 52-week high explains a large portion of the profits from momentum investing in stocks and dominates past returns as a forecaster, without long-run reversal. Their variable is a distance, whereas the lesson's rule keeps one bit: above or below the prior maximum times (1 + b). Our inference is that a bot should log the distance as well, then test whether a banded or sized response beats the yes-or-no one at equal turnover.

Potters and Bouchaud solved a simple trend-following model exactly. Its profit per trade has an asymmetric, option-like distribution, the average gain per trade is exactly zero, and the fraction of winning trades falls from one half at low volatility to zero at high volatility. They conclude that win rate indicates trading style, not reliability. Our inference is that a win rate under one half is not a defect by itself, and that a good-looking payoff needs a null to beat.

Exercise: simulate driftless random-walk prices at a low and a high volatility, run the 0.5% and 1.5% breakouts, and record average gross gain per trade, win fraction and turnover. Then charge 15 bps per notional equivalent and compare the result with the real-data run.""",
        [
            ('paper', 'Brock, Lakonishok & LeBaron', 1992, 'Simple Technical Trading Rules and the Stochastic Properties of Stock Returns', 'https://doi.org/10.1111/j.1540-6261.1992.tb04681.x',
             'Tests moving-average and trading-range-break rules on the Dow Jones index from 1897 to 1986 against four bootstrapped null models, comparing returns after buy and sell signals.'),
            ('paper', 'George & Hwang', 2004, 'The 52-Week High and Momentum Investing', 'https://doi.org/10.1111/j.1540-6261.2004.00695.x',
             "Shows that nearness to the 52-week high explains much of momentum profit and dominates past returns, with no long-run reversal; a distance-based cousin of the lesson's prior-high breakout."),
            ('arxiv', 'Potters & Bouchaud', 2005, 'Trend followers lose more often than they gain', 'https://arxiv.org/abs/physics/0508104',
             'Solves a simple trend-following model exactly: asymmetric profit per trade, zero average gain, and a win fraction that reflects trading style rather than reliability.'),
        ],
    ),
    "5.10": (
        r"""Why would a displacement close? Nagel gives one answer for short-term equity reversals: their returns proxy for the pay from supplying liquidity, and that pay is highly predictable from the VIX, with expected returns and conditional Sharpe ratios spiking in market turmoil. Our inference is that part of what a stretched-spread trade earns is a fee for standing in when liquidity is scarce, and that the spread that keeps stretching is likeliest to appear in the same periods. Tag every entry with a volatility regime and report results by regime as well as in total.

A z-score also inherits the error of the estimates behind it. Elliott and co-authors modelled a pair's spread as a mean-reverting Gaussian Markov chain observed in Gaussian noise, and compared the calibrated model's predictions with later observations to decide trades; our inference is that a raw z-score treats the noisy observation as the true state. Holý and Černý add that the parameters of a mean-reverting spread are never known exactly and are estimated from finite samples, and they quantify the loss against a trader who knows them. With the lesson's numbers, a training mean of 11 instead of 10 puts a spread of 14 at a z-score of 1.5, exactly on Harbor's threshold, so a half-standard-deviation error is enough to remove the signal.

Exercise: simulate a mean-reverting spread with a known mean, estimate the mean and scale from short, medium and long windows, and trade the 1.5 rule with estimated and true parameters; record how the gap in net result shrinks with window length. Then shift the true mean by two standard deviations halfway through and record how long the position stays open without a time stop.""",
        [
            ('paper', 'Nagel', 2012, 'Evaporating Liquidity', 'https://doi.org/10.1093/rfs/hhs066',
             'Interprets short-term reversal returns as pay for liquidity provision and shows that this pay is predictable from the VIX and spikes in turmoil.'),
            ('paper', 'Elliott, van der Hoek & Malcolm', 2005, 'Pairs trading', 'https://doi.org/10.1080/14697680500149370',
             "Models a pair's spread as a mean-reverting Gaussian Markov chain observed in noise and compares model predictions with later observations to decide trades."),
            ('arxiv', 'Holý & Černý', 2021, "Bertram's Pairs Trading Strategy with Bounded Risk", 'https://arxiv.org/abs/2102.04160',
             'Treats estimation error in the parameters of a mean-reverting spread as critical in practice and quantifies the loss against a trader who knows them exactly.'),
        ],
    ),
    "5.11": (
        r"""An engine's timing convention is a documented assumption, and Backtrader states its own. The current data has already happened, so a rule that tests an examined close cannot expect a fill at that close; a market order executes at the next bar's opening price. That is the lesson's 100 signal and 102 fill. Its slippage page shows a cost silently vanishing: in the sample run, a 1.5% slippage setting changed no fill price until slip_open was switched on, and even then a buy on a bar whose open equalled its high could not be pushed above that high. Our inference is that a bot should assert, for each simulated market buy, that fill price minus the raw next open equals the declared slippage unless the bar's high caps it, and that the ledger fee is commission alone. A failure exposes skipped or doubled costs, and the cap makes simulated slippage smaller than declared on such bars.

Holdout discipline needs a count as well as a rule. Dwork and co-authors describe analysis as adaptive: hypotheses and parameters are chosen after seeing earlier results, and they warn that a holdout consulted again and again, each choice informed by the last answer, can easily end up overfit itself. Their algorithm lets a large number of adaptively chosen hypotheses be validated while provably avoiding overfitting. For a bot, our suggestion is a ledger of every look at the final segment, with the segment reclassified as development data once the declared budget is spent.

Park and Irwin surveyed technical trading studies: of 95 modern ones, 56 reported positive results, 20 negative and 19 mixed, with profits documented at least until the early 1990s. They also note that most studies suffer from data snooping, hindsight selection of rules, and weak estimates of risk and transaction costs. A majority-positive tally says little when the weaknesses are shared (our inference).

Exercise: rerun Harbor's trade three ways, filled at the 100 signal close, at the 102 next open, and one bar later, with slippage counted once, and report which line of the order trace each change moves.""",
        [
            ('docs', 'Backtrader', None, 'Orders - Creation/Execution', 'https://www.backtrader.com/docu/order-creation-execution/order-creation-execution/',
             "Documents that a backtest cannot fill an order at the close it just examined and that market orders use the next bar's opening price."),
            ('docs', 'Backtrader', None, 'Broker - Slippage', 'https://www.backtrader.com/docu/slippage/slippage/',
             "Shows in a sample run that a slippage setting moved no next-open fills until slip_open was switched on, and that slipped prices are capped at the bar's high or low unless slip_out is set."),
            ('arxiv', 'Dwork et al.', 2015, 'Generalization in Adaptive Data Analysis and Holdout Reuse', 'https://arxiv.org/abs/1506.02629',
             'Shows that adaptively reusing a holdout set overfits it and gives an algorithm that validates many adaptively chosen hypotheses while provably avoiding overfitting.'),
            ('paper', 'Park & Irwin', 2007, 'What Do We Know About the Profitability of Technical Analysis?', 'https://doi.org/10.1111/j.1467-6419.2007.00519.x',
             'Surveys 95 modern technical-trading studies and lists the shared testing problems: data snooping, ex post rule selection and weak risk and cost estimates.'),
        ],
    ),
    "5.12": (
        r"""Perold defined implementation shortfall as the profit on a paper portfolio, which trades at benchmark prices, minus the profit on the real one. Against the bid-ask midpoint it is what Hasbrouck's lecture notes call the effective cost: for Harbor's buy, the lesson's 12 bps. The notes define price improvement for a buy as the offer minus the fill price, so a 100.12 fill against a 100.10 offer scores −0.02. Our inference: the extra 2 bps came from a quote that moved before arrival or from depth that ran out, and only an arrival-time quote and the book's size can tell which.

Impact needs a second quote. Realized cost uses the midpoint five minutes after the trade, and price impact is effective cost minus realized cost, the midpoint's move in the trade's direction. If Harbor's midpoint is still 100.00 five minutes later, all 12 bps is realized cost; if it has reached 100.12, all 12 bps is impact. Bouchaud, Farmer and Lillo define market impact as the average response of prices to trades and review evidence that it decays slowly. Our inference: five minutes is a convention, not the line between temporary and permanent. Overlap distorts it. In the notes' example, three quick trades that each move the midpoint by $0.10, all measured against the same later midpoint, show impacts of $0.30, $0.20 and $0.10.

Unfilled orders need the same care. In the notes' experiment, market buys pay the $0.05 half-spread while the limit buys that fill show −$0.05, so limits seem to win. Complete each unfilled limit at the final offer and the notes' eight-path random walk gives an average of 10.00 for a limit one cent below the offer, the same as a market order.

Exercise: replay a path where each fill moves the midpoint by one basis point, with three fills seconds apart. A naive markout reports an average of 2 basis points; make it return 1, then reproduce the eight-path result as a unit test.""",
        [
            ('paper', 'Perold', 1988, 'The implementation shortfall', 'https://doi.org/10.3905/jpm.1988.409150',
             'Origin of implementation shortfall: the gap between a paper portfolio traded at benchmark prices and the portfolio actually implemented.'),
            ('docs', 'Hasbrouck', 2015, 'Securities Trading: Principles and Procedures, Chapter 8: Transaction costs (lecture notes)', 'https://pages.stern.nyu.edu/~jhasbrou/Teaching/POST%202015%20Spring/classNotes/STPPTradingCosts.pdf',
             'Lecture notes defining effective cost, realized cost, price impact and price improvement, with worked examples of overlapping markouts and of limit orders that fail to fill.'),
            ('arxiv', 'Bouchaud, Farmer & Lillo', 2008, 'How markets slowly digest changes in supply and demand', 'https://arxiv.org/abs/0809.0822',
             'Review of theory and evidence on market impact, including its slow decay with time, which limits what any single markout horizon can reveal.'),
        ],
    ),
    "5.13": (
        r"""The FIX Trading Community's order-state document tabulates the lesson's cancellation race. Scenario B.1.b follows a 10,000-share order: 2,000 fill, a cancel request goes out, 3,000 more fill while it is in flight, the broker confirms Pending Cancel, another 1,000 fill, and the final report is Canceled with 6,000 filled. ExecType gives the reason a report was sent; OrdStatus gives the order's status after that event. When an order is in several states at once, the highest-precedence state is reported, and Pending Cancel outranks Filled even though the standard stresses that it does not indicate cancellation.

That precedence rule is the trap. In scenario B.1.c the last 5,000 shares fill while the cancel is pending, so the report carrying them shows Pending Cancel, not Filled, and a Cancel Reject with reason 0, too late to cancel, follows. Our inference: an adapter that books shares when it sees a Filled or Partially Filled status will lose that fill, so book from the trade reports and treat a too-late reject as an ordinary outcome. Scenario B.1.d adds a second surprise: a cancel request may name an order the broker has not yet acknowledged, so Pending Cancel can arrive before New, and a transition table that insists on New first would reject legal traffic.

These races are common. Aquilina, Budish and O'Neill used exchange message data, which, unlike limit order book data, include failed attempts to trade or cancel. They found latency-arbitrage races about once a minute per symbol for FTSE 100 stocks, a modal race lasting 5 to 10 millionths of a second, and about 20% of trading volume involved. Cartea and co-authors, modelling marketable orders under latency, note that delay leaves a liquidity provider with no guarantee of withdrawing a stale quote before it is picked off. A one-millisecond round trip is 100 to 200 times the modal race, so a bot cannot count on its cancel arriving first.

Exercise: scale B.1.b, B.1.c and B.1.d to 100 shares and replay each three ways: in order, with one fill delivered twice, and with the cancel reject ahead of the last fill. Every variant should end with the same position and no open commitment.""",
        [
            ('docs', 'FIX Trading Community', 2023, 'Order State Changes, FIX Latest as of EP284', 'https://www.fixtrading.org/wp-content/uploads/download-manager-files/FIX-Latest-as-of-EP284-Order-State-Changes.pdf',
             "The standard's own scenario tables for cancels that cross fills, with the OrdStatus precedence rule and the cancel-for-unacknowledged-order case."),
            ('paper', "Aquilina, Budish & O'Neill", 2021, 'Quantifying the High-Frequency Trading “Arms Race”', 'https://doi.org/10.1093/qje/qjab032',
             'Exchange message data that include failed trades and cancels, used to measure how often and how fast latency races for stale quotes occur.'),
            ('arxiv', 'Cartea, Jaimungal & Sánchez-Betancourt', 2019, 'Latency and Liquidity Risk', 'https://arxiv.org/abs/1908.03281',
             'Models how exchange latency removes any guarantee that an order, or the withdrawal of a stale quote, lands before the book changes.'),
        ],
    ),
    "5.14": (
        r"""TWAP and VWAP differ in which clock they follow, and Kato makes the link precise. Adding an explicit trading-volume process to the Almgren–Chriss execution model, he shows that a risk-neutral trader's optimal schedule is VWAP, trading in proportion to volume, when the day's total volume is known in advance. He calls that case unrealistic but a useful benchmark, and with constant volume it reduces to equal slices, which is TWAP. For a schedule fixed in advance, his optimum weights each interval by the harmonic mean of volume, 1/E[1/v], rather than the average. Our inference: in that model an erratic bucket earns a smaller share than its average volume implies. A bucket equally likely to trade 2,000 or 6,000 shares averages 4,000 but has a harmonic mean of 3,000.

Białkowski, Darolles and Le Fol attack the forecast itself. They split intraday volume into a part that follows the market's evolution and a stock-specific pattern, applied the model to CAC 40 stocks, and let the VWAP strategy adjust during the day to track the end-of-day VWAP better. For Harbor, recompute the remaining targets from volume already seen, never from volume yet to come.

Participation rules have their own failure mode. On 6 May 2010 a 75,000-contract E-Mini sell program ran through an algorithm that targeted 9% of the previous minute's volume, without regard to price or time. The same trader's earlier program of that size took more than 5 hours; this one finished in 20 minutes. In the 14 seconds from 2:45:13, high-frequency traders traded over 27,000 contracts, about 49 percent of volume, while adding only about 200 net. Our inference: a rule of ρ times observed volume speeds up exactly when observed volume is least informative. A 5% cap on a bucket that suddenly prints 8,000 shares allows 400, so add an absolute cap and a price limit.

Exercise: if the lesson's 4,000-share bucket is its 40% bucket, the day trades 10,000 shares and a 5% cap can complete only 500 of the 1,000. Check that feasibility first, then replay a bucket with doubled volume.""",
        [
            ('arxiv', 'Kato', 2014, 'VWAP Execution as an Optimal Strategy', 'https://arxiv.org/abs/1408.6118',
             'Adds a trading-volume process to the Almgren–Chriss model and shows when VWAP is optimal, why exact VWAP needs future volume, and how forecast volume enters a fixed schedule.'),
            ('paper', 'Białkowski, Darolles & Le Fol', 2008, 'Improving VWAP strategies: A dynamic volume approach', 'https://doi.org/10.1016/j.jbankfin.2007.09.023',
             'Decomposes intraday volume into a market-wide and a stock-specific part so that a VWAP schedule can be adjusted during the day to track the closing VWAP.'),
            ('official', 'U.S. CFTC & SEC staffs', 2010, 'Findings Regarding the Market Events of May 6, 2010', 'https://www.cftc.gov/sites/default/files/idc/groups/public/%40otherif/documents/ifdocs/staff-findings050610.pdf',
             'The joint staff report on how a sell algorithm that targeted a share of recent volume, with no price or time limit, interacted with recycled volume.'),
        ],
    ),
    "5.5": (
        r"""Start with the number type. The Python documentation shows that 0.1 + 0.1 + 0.1 − 0.3 is exactly zero in decimal arithmetic but about 5.55 × 10⁻¹⁷ in binary floating point, that such residues block reliable equality tests and can accumulate, and that decimal is therefore preferred in accounting applications with strict equality invariants. Harbor's checks are equalities: $5,998 plus $4,040 must equal $10,038 to the cent. Integer cents or Decimal remove the residue but not the rounding policy. The module offers eight rounding modes and defaults to half-even, so a half-cent-per-share fee on a 41-share fill is $0.205, booked as $0.20 under half-even and $0.21 under half-up. One cent per tie is enough to break reconciliation with a broker statement, so name the mode in the adapter contract.

Next, test the equalities after every transition by letting a tool choose the sequences. Hypothesis's rule-based state machines take primitive actions, search for sequences that fail, and run invariants after every step. Useful invariants for Harbor: cash and shares each equal their opening balance plus the signed fill flows, with fees deducted from cash; reserved cash covers the price cap times the open quantity plus the fee buffer; replaying any fill changes nothing. A failing sequence it finds is a ready-made replay.

A correct ledger can still hold an unrealistic fill rule. Huang, Lehalle and Rosenbaum treat the book as a queueing system whose order-flow intensities depend only on its current state, and use it to compute execution probabilities of passive orders and as a market simulator. Our inference: a mock that fills Harbor's pending 60 shares whenever a trade prints at its price ignores the queue ahead. Add a property test that the fill probability never rises as the queue ahead grows.

Exercise: write the three invariants and the monotonicity property as one state machine, run it over many generated sequences, then kill the process between booking cash and booking shares and check that the ledger still balances.""",
        [
            ('docs', 'Python Software Foundation', None, 'decimal: Decimal fixed-point and floating-point arithmetic', 'https://docs.python.org/3/library/decimal.html',
             'Documents why binary floats break equality tests in accounting code, the eight rounding modes and the half-even default.'),
            ('docs', 'Hypothesis', None, 'Stateful tests', 'https://hypothesis.readthedocs.io/en/latest/stateful.html',
             'Rule-based state machines that generate sequences of actions and check invariants after every step.'),
            ('arxiv', 'Huang, Lehalle & Rosenbaum', 2013, 'Simulating and analyzing order book data: The queue-reactive model', 'https://arxiv.org/abs/1312.0563',
             'Models the order book as a state-dependent queueing system, used for execution probabilities of passive orders and as a market simulator.'),
        ],
    ),
    "5.4": (
        r"""MacLean, Thorp and Ziemba summarise the trade-off in Kelly sizing: the criterion maximises the limiting exponential growth rate of wealth, but its suggested wagers may be very large, so it can be very risky in the short term. For processes well approximated in continuous time, growth drops to the risk-free rate at exactly twice the Kelly wager and keeps falling beyond it. For the lesson's even-money bet with a true probability of 0.51, true Kelly is 2%. Our calculation of expected log growth per bet gives +0.020% at a 2% stake, about zero at 4%, −0.025% at 5% and −0.30% at 10%. Half Kelly sized from the 0.55 estimate is a 5% stake, already past break-even.

A halt is a drawdown rule, and Busseti, Ryu and Boyd treat drawdown directly, measured from starting wealth. They bound by β the probability that wealth ever falls to a fraction α of its start. The bound holds when the expected value of the growth factor raised to the power −λ is at most 1, with λ = log β / log α; in their simulations such bets beat fractional Kelly at the same drawdown risk. For a halt 30% below starting equity (α = 0.7) tolerated with probability 0.1, applying that bound to Harbor's even-money bet gives a stake cap of about 2.7% when p = 0.55 and about 0.5% when p = 0.51. In our simulation of 4,000 bets per path at p = 0.55, that halt was touched on about 9% of paths at 2.7%, 32% at 5% and 66% at 10%; a halt measured from the running peak fires at least as often.

Market-wide circuit breakers trigger at 7%, 13% and 20% declines in the S&P 500; the first two pause trading for 15 minutes before 3:25 p.m., the third ends the day. A single stock pauses for five minutes if it stays at its price band for 15 seconds, and no trade can occur outside the band. Our inference: copy the graded thresholds and fixed pauses for Harbor's halts, name who may resume, and do not assume a stop fills beyond a band.

Exercise: simulate the three stakes at p = 0.55 and p = 0.51 and count how often the halt fires.""",
        [
            ('book', 'MacLean, Thorp & Ziemba', 2011, 'Good and Bad Properties of the Kelly Criterion', 'https://doi.org/10.1142/9789814293501_0039',
             'Summarises why Kelly maximises long-run growth yet can be very risky in the short term, and what happens to growth when stakes exceed the Kelly wager.'),
            ('arxiv', 'Busseti, Ryu & Boyd', 2016, 'Risk-Constrained Kelly Gambling', 'https://arxiv.org/abs/1603.06183',
             'Turns a drawdown limit into a bet-size constraint, with a bound on the probability that wealth ever falls to a given fraction of its starting value.'),
            ('official', 'U.S. SEC · Investor.gov', None, 'Stock Market Circuit Breakers', 'https://www.investor.gov/introduction-investing/investing-basics/glossary/stock-market-circuit-breakers',
             "The SEC's plain-language summary of market-wide and single-stock circuit breakers: trigger levels, pause lengths and price bands."),
        ],
    ),
    "5.15": (
        r"""The SEC's market access rule is explicit about what counts. Its adopting release says brokers should measure credit and capital thresholds against orders entered, counting the exposure of open orders that have not yet executed. That exposure may be discounted for the chance of execution only where sound risk models back the discount, and a firm relying on them should monitor their accuracy. Harbor has no such model, so its $5,000 pending buy counts at face value. Illustration: a 50% discount lifts the room for a new buy from $3,000 to $5,500, and if everything filled the name would end at 22.5%. The release also splits an aggregate limit: $1,000,000 across five venues may become $200,000 each, provided each assumes the others are full. Our inference: fixed slices of Harbor's 20% name limit, one per strategy, avoid a shared counter at the price of idle budget.

Shared counters invite races. Berenson and co-authors describe write skew: one transaction reads x and y, which satisfy a constraint, a second reads both and writes x, then the first writes y, and the constraint may break. Their bank example lets balances go negative while the joint sum stays non-negative, and snapshot isolation allows the anomaly. Our inference: two $2,000 buys, each leaving the name at 19%, can both pass checks made on separate order rows and sit at 21% together. Under first-committer-wins, a shared reservation row that every acceptance updates makes the second commit abort.

Exercise: submit both buys concurrently a thousand times; exactly one must be accepted every time. Then revalue the name 23% higher after the pending buy fills; the breach should raise a review, not rewrite the acceptance record.""",
        [
            ('official', 'U.S. SEC', 2010, 'Risk Management Controls for Brokers or Dealers with Market Access', 'https://www.sec.gov/files/rules/final/2010/34-63241.pdf',
             'Adopting release for Rule 15c3-5: thresholds are measured on orders entered including open orders, execution-likelihood discounts need monitored models, and an aggregate limit may be split into venue sub-limits.'),
            ('arxiv', 'Berenson et al.', 2007, 'A Critique of ANSI SQL Isolation Levels', 'https://arxiv.org/abs/cs/0701157',
             'Defines read skew and write skew, the way two transactions that each respect a constraint can jointly break it, and shows that snapshot isolation still admits write skew.'),
        ],
    ),
    "5.16": (
        r"""The CFTC's 2013 concept release, which asks questions rather than imposing rules, lists pre-trade controls as separate layers. A price collar stops orders priced outside an acceptable band from reaching the book or trading at extreme levels, and collars can be dynamic, following prices and volatility. A maximum order size caps quantity at a preset "fat finger" limit. The release also asks about reasonability checks on incoming market data. Harbor's price cap makes its cash arithmetic safe, but cash alone would still accept a typo the account can afford, so quantity needs its own bound (our inference).

Bailis and co-authors ask when an invariant survives concurrent updates without coordination. For counters, a greater-than threshold survives increments but not decrements, and a less-than threshold survives decrements but not increments. Our reading: Harbor's three invariants sit on the unsafe side: cash ≥ 0 under buy reservations, fills ≤ authorized quantity under new fills, and sell reservations ≤ owned shares under new reservations. So only steps that move a counter toward its bound need serialized handling; cancels and deposits do not.

Claessen and Hughes describe QuickCheck properties as functions tested on random input, with custom generators and pitfalls to avoid. Our inference: a gate's pitfall is vacuity, because uniform random orders are mostly rejected. Exercise: generate thousands of boundary orders, assert that every accepted one keeps cash ≥ 0, and count rejections by reason; a reason that never fires is untested. Nine shares at the $100 cap with 10 bps commission cost $900.90, yet 9 × 100 × (1 + 10/10000) evaluates to 900.8999999999999 in Python floats, so keep money in integer cents or Decimal with a stated rounding rule.""",
        [
            ('official', 'U.S. CFTC', 2013, 'Concept Release on Risk Controls and System Safeguards for Automated Trading Environments', 'https://www.federalregister.gov/documents/2013/09/12/2013-22185/concept-release-on-risk-controls-and-system-safeguards-for-automated-trading-environments',
             'Describes price collars, maximum order sizes and market-data reasonability checks as distinct pre-trade controls for automated trading, and poses questions about each.'),
            ('arxiv', 'Bailis et al.', 2014, 'Coordination Avoidance in Database Systems (Extended Version)', 'https://arxiv.org/abs/1402.2237',
             'Invariant confluence decides which application invariants need coordination; for counter thresholds, the update direction decides the answer.'),
            ('paper', 'Claessen & Hughes', 2000, 'QuickCheck', 'https://doi.org/10.1145/351240.351266',
             'Introduces property-based testing: properties are functions checked on automatically generated random inputs, with custom generators for constrained data.'),
        ],
    ),
    "5.17": (
        r"""A halt is a state with its own traffic, not silence. Corwin and Lipson found that on the NYSE, order submissions and cancellations rise markedly during halts, that much of the reopening book consists of orders entered during the halt, and that quoted depth is unusually thin around halts. Our inference: Harbor's halted state must keep processing acknowledgements, cancels and late fills, and a resume should wait for a fresh quote.

Xu and co-authors followed 203 Shanghai-listed stocks from August 2009 to August 2011. Absolute return, trading volume and, around intraday halts, the bid-ask spread all peaked after a halt and then relaxed along a power law. Our inference: add spread normalization to the resumption checklist, and restart with reduced size caps rather than full limits.

The lesson's trigger is a fixed floor 2.5% below the session start, at $97,500. Grossman and Zhou study a floor that ratchets with the peak: wealth must stay above a fixed fraction of its running maximum, and for constant relative risk aversion the optimal risky investment is proportional to the surplus above that floor. If equity first rose to $102,000, a 2.5% floor under the peak would sit at $99,450. Our reading: surplus-scaled exposure shrinks smoothly toward the limit in theory; gaps and fees make the latched halt the backstop.

Exercise: replay 100,000 → 97,400 → 98,000. The halt must latch at 2.6%, survive the rebound and a restart, process a fill that arrives while halted, and refuse an unreviewed resume.""",
        [
            ('paper', 'Corwin & Lipson', 2000, 'Order Flow and Liquidity around NYSE Trading Halts', 'https://doi.org/10.1111/0022-1082.00267',
             'Shows that order submissions and cancellations rise during NYSE halts, that the reopening book is largely built during the halt, and that depth is thin around halts.'),
            ('arxiv', 'Xu, Zhang & Liu', 2013, 'Short-term Market Reaction after Trading Halts in Chinese Stock Market', 'https://arxiv.org/abs/1309.1138',
             "Measures return, volume and spread after 203 stocks' halts on the Shanghai Stock Exchange, finding a sharp peak followed by power-law relaxation."),
            ('paper', 'Grossman & Zhou', 1993, 'Optimal Investment Strategies for Controlling Drawdowns', 'https://doi.org/10.1111/j.1467-9965.1993.tb00044.x',
             'Derives the optimal risky investment under a floor tied to the running maximum of wealth, with exposure proportional to the surplus above the floor.'),
        ],
    ),
    "5.18": (
        r"""Overlap costs twice: it leaks across the split and it shrinks the honest sample. A label spanning h steps and sampled every step shares h − 1 steps with its neighbour. In the lesson's split the surviving labels, ending at 7 and 9, still share the step from 6 to 7. Richardson and Stock derived a different asymptotic theory for statistics built on multi-year returns, since the standard approximations behaved badly; it matched finite-sample distributions far better and made the data look much more compatible with no mean reversion. Hodrick's Monte Carlo analysis found the Hansen–Hodrick procedure biased at long horizons while the alternatives did better. Our arithmetic: 250 daily rows with 5-day labels hold only 50 non-overlapping windows, so report 50 beside any corrected statistic, because the corrections themselves have finite-sample problems.

Shuffling rows is no remedy. Roberts and co-authors found that ignoring dependence in cross-validation seriously underestimates predictive error, and recommend block validation wherever dependence exists, even when the residuals look uncorrelated. Rabinowicz and Rosset give a criterion for when standard cross-validation stays suitable under correlation, and a bias-corrected estimator for when it does not. Our inference: in a forward-only split, purging at the cutoff is the whole job; an embargo after the validation block matters only when later rows also train.

Exercise: run the whole pipeline, scaler included, on a simulated random walk. Skill above the training-mean baseline under shuffled folds, but not under purged walk-forward splits, measures the leak; after the fix, scores should sit at or below zero.""",
        [
            ('paper', 'Richardson & Stock', 1989, 'Drawing inferences from statistics based on multiyear asset returns', 'https://doi.org/10.1016/0304-405X%2889%2990086-X',
             'Develops asymptotic theory for statistics built on multi-year returns, because the usual approximations performed poorly in finite samples.'),
            ('paper', 'Hodrick', 1992, 'Dividend Yields and Expected Stock Returns: Alternative Procedures for Inference and Measurement', 'https://doi.org/10.1093/rfs/5.3.351',
             'Monte Carlo comparison of inference procedures for long-horizon forecasting, finding the Hansen–Hodrick procedure biased at long horizons.'),
            ('paper', 'Roberts et al.', 2017, 'Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure', 'https://doi.org/10.1111/ecog.02881',
             'Shows that random cross-validation underestimates predictive error on dependent data and recommends blocked splits wherever dependence exists.'),
            ('arxiv', 'Rabinowicz & Rosset', 2019, 'Cross-Validation for Correlated Data', 'https://arxiv.org/abs/1904.02438',
             'Gives a criterion for when standard cross-validation is suitable under correlation and a bias-corrected estimator for when it is not.'),
        ],
    ),
    "5.19": (
        r"""Welch and Goyal found that the proposed predictors of the equity premium had by and large forecast badly for 30 years, judged in sample or out of sample, and looked unstable. The yardstick, as Campbell and Thompson describe it, was a simple forecast based on the historical average return: the lesson's training mean. Campbell and Thompson's working paper found that two output rules improve out-of-sample performance: zero out a regression coefficient whose sign is wrong, and floor negative forecasts at zero.

Scale is the useful part. They judge an out-of-sample R² against the squared Sharpe ratio S². With a monthly S² of 1.2%, an R² of 0.25% for the earnings-price ratio lifts a mean-variance investor's average portfolio return by a proportional 0.25/1.2 = 21%. Harbor's two rows give an R² of 90% against the zero baseline, so they establish nothing. Their stock weight was confined to between 0 and 150%, and predictable variation produces no portfolio gain while an upper limit binds: test the capped policy, not the raw forecast.

Babiak and Baruník score neural-network forecasts against linear regressions by certainty-equivalent return and Sharpe ratio, and report gains that survive transaction costs and borrowing and short-selling constraints. Our reading: climb a ladder of baselines, training mean then linear then nonlinear, and score every rung with the same capped, costed policy.

Exercise: report R² against the training mean, clip negative forecasts, apply the cap, then subtract the 6 bps cost; claim nothing from a step you skipped.""",
        [
            ('paper', 'Welch & Goyal', 2008, 'A Comprehensive Look at The Empirical Performance of Equity Premium Prediction', 'https://doi.org/10.1093/rfs/hhm014',
             'Re-examines the predictors proposed for the equity premium and finds poor, unstable in-sample and out-of-sample performance against simple benchmarks.'),
            ('paper', 'Campbell & Thompson', 2005, 'Predicting the Equity Premium Out of Sample: Can Anything Beat the Historical Average?', 'https://doi.org/10.3386/w11468',
             'NBER working paper: sign restrictions on coefficients and forecasts, an out-of-sample R² judged against the squared Sharpe ratio, and portfolio weights bounded between 0 and 150%.'),
            ('arxiv', 'Babiak & Baruník', 2020, 'Deep Learning, Predictability, and Optimal Portfolio Returns', 'https://arxiv.org/abs/2009.03394',
             'Scores deep-learning return forecasts against linear regressions by certainty-equivalent return and Sharpe ratio, with transaction costs and portfolio constraints.'),
        ],
    ),
    "5.20": (
        r"""Early stopping is where the lesson's checkpoint rule meets library behavior, and XGBoost's API reference lists several traps. Its native training function stops once the validation metric has gone the stated number of rounds without improving, uses the last entry of the evaluation list, and returns the model from the last iteration, not the best one. With the lesson's losses and a patience of two, training halts after checkpoint five, and a plain call to the booster's predict uses all five rounds, including the two that made validation worse. The documented remedies are a save_best option that drops the rounds after the best one, or slicing the model, but slicing removes the best_iteration attribute, so Harbor's own manifest must record the chosen round. Because the last evaluation entry decides stopping, a test set appended for monitoring would become the stopping criterion, which breaks the lesson's rule that the final test never tunes anything.

Constraints deserve similar suspicion. LightGBM's documentation says the monotone-constraint vector must list every feature in order, so a reordered or inserted column can move a constraint onto a different feature (our inference), and it describes the default method as over-constraining the predictions. The wider case for boosted trees has limits too. Grinsztajn and co-authors found tree-based models still state of the art on medium-sized tabular data, about ten thousand samples, across a 45-dataset benchmark, but they removed stream-like data and time series, so the result cannot vouch for a market model by itself.

Exercise: save the chosen round, feature order and constraint vector beside the model, reload it in a clean process, and require predictions to equal those of the first three rounds. Then sweep the quality score across its observed range with the other inputs fixed and assert that predictions never fall.""",
        [
            ('docs', 'XGBoost contributors', None, 'XGBoost Python API Reference', 'https://xgboost.readthedocs.io/en/stable/python/python_api.html',
             'Version 3.4.2 documentation: native early stopping uses the last evaluation set and returns the last-iteration model; slicing a booster drops best_iteration; the save_best option keeps only rounds up to the best one.'),
            ('docs', 'LightGBM contributors', None, 'LightGBM Parameters', 'https://lightgbm.readthedocs.io/en/stable/Parameters.html',
             'Version 4.7.0 documentation: the monotone-constraint vector must cover all features in order, and the default constraint method over-constrains predictions.'),
            ('arxiv', 'Grinsztajn, Oyallon & Varoquaux', 2022, 'Why do tree-based models still outperform deep learning on tabular data?', 'https://arxiv.org/abs/2207.08815',
             'A 45-dataset benchmark of tree models against neural networks, with an analysis of why trees do well and an explicit exclusion of time series.'),
        ],
    ),
    "5.21": (
        r"""The lesson's 0.55 threshold treats a model score as a probability, and the calibration literature says to check that for boosted trees. Niculescu-Mizil and Caruana compared learning methods on eight binary problems and found that maximum-margin methods such as boosted trees and stumps push probability mass away from 0 and 1, a sigmoid-shaped distortion; after calibration, boosted trees, random forests and SVMs gave the best probabilities. Whether a current log-loss library shows the same distortion is something a reliability table must answer (our inference). They also explain why a calibrator needs its own data: a model that separates its training cases perfectly teaches a sigmoid that outputs just a 0,1 function. Calibration-set size matters too: below roughly 200 to 1000 cases, Platt scaling beat isotonic regression for all nine methods they plotted, because isotonic is less constrained. A bot's calibration window of a few hundred trades may sit in that range (our inference).

Elkan frames the decision step. The best action has the lowest expected cost under the model's probabilities, and any two-class cost matrix has essentially one degree of freedom for decisions, the threshold. He argues that rebalancing training classes has little effect on standard Bayesian and decision-tree learners, and recommends learning from the data as given and then computing decisions explicitly. With the lesson's payoffs of plus and minus 1, the break-even probability is (1 + cost) / 2, so a cost of 0.2 moves 0.55 to 0.60.

Drift alerts need triage as well. Rabanser and co-authors, working mainly on MNIST and CIFAR-10 images, note that distributions shift constantly and often benignly, and that target error cannot be computed without labels. Their best univariate detector tested the classifier's own softmax outputs, the analogue of Harbor's prediction distribution.

Exercise: bin Harbor's validation predictions with counts, fit a Platt sigmoid on a later window, recompute the threshold at costs 0.1 and 0.2, then replay a feature shift and a flipped outcome relationship. Only the first should alert before labels mature.""",
        [
            ('paper', 'Niculescu-Mizil & Caruana', 2005, 'Predicting good probabilities with supervised learning', 'https://doi.org/10.1145/1102351.1102430',
             'Compares how learning methods distort predicted probabilities, why calibration needs an independent set, and how Platt scaling and isotonic regression behave as calibration data shrinks.'),
            ('paper', 'Elkan', 2001, 'The Foundations of Cost-Sensitive Learning', 'https://cseweb.ucsd.edu/~elkan/rescale.pdf',
             'Shows how optimal decisions follow from a cost matrix and probability estimates, and why class rebalancing is a weak substitute for explicit decision thresholds.'),
            ('arxiv', 'Rabanser, Günnemann & Lipton', 2018, 'Failing Loudly: An Empirical Study of Methods for Detecting Dataset Shift', 'https://arxiv.org/abs/1810.11953',
             'Benchmarks shift detectors, separates benign from harmful shift, and shows why target error needs labels.'),
        ],
    ),
    "5.3": (
        r"""Parasuraman and co-authors give the lesson's three-way split a standard vocabulary. They divide automation into four function types, information acquisition, information analysis, decision and action selection, and action implementation, each of which can be set anywhere from fully manual to fully automatic, and they name automation reliability and the costs of decision and action consequences among their secondary criteria for judging a design. Mapped onto Harbor (our inference), a model can sit high on analysis, a proposal is decision selection, and the broker call is action implementation, which only the risk gate may reach.

The 0.9 attached to the 30% proposal deserves scrutiny of its own. Xiong and co-authors benchmarked ways of eliciting confidence from five language models on five types of datasets and found that verbalized confidence tends to be overconfident, with every method struggling on tasks that need professional knowledge. NIST's generative AI profile defines confabulation as confidently stated but erroneous content, and warns that automation bias, meaning excessive deference to automated systems, can exacerbate it. That is a reason to distrust a human reviewer who waves through whatever clears the gate (our inference).

A committee does not fix this by voting. Kim and co-authors evaluated over 350 language models and found that on one leaderboard dataset two models agree 60% of the time when both are wrong, and that larger, more accurate models have highly correlated errors even across providers. NIST names the broader hazard algorithmic monocultures. Our suggestion is to count a committee as one opinion and to require independent evidence, such as a source identifier, before anything is accepted.

Exercise: replay the 30% proposal with the model's confidence low, at 0.9 and near certainty, and with one, three and five agreeing agents; the gate's output must not change. Then delete the revenue source identifier and require an abstention.""",
        [
            ('paper', 'Parasuraman, Sheridan & Wickens', 2000, 'A model for types and levels of human interaction with automation', 'https://doi.org/10.1109/3468.844354',
             'Four automation function types and a continuum of levels, with reliability and the cost of wrong decisions or actions as criteria; a vocabulary for what the AI may do versus what code must control.'),
            ('arxiv', 'Xiong et al.', 2023, 'Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs', 'https://arxiv.org/abs/2306.13063',
             'Benchmarks verbalized, sampled and aggregated confidence from five LLMs on five dataset types, finding overconfidence in verbalized confidence.'),
            ('official', 'NIST', 2024, 'Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)', 'https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf',
             'Defines confabulation, automation bias and algorithmic monocultures among generative AI risks.'),
            ('arxiv', 'Kim, Garg, Peng & Garg', 2025, 'Correlated Errors in Large Language Models', 'https://arxiv.org/abs/2506.07962',
             'Measures how often over 350 LLMs make the same mistakes, including models from different providers.'),
        ],
    ),
    "5.22": (
        r"""EDGAR's own API documentation shows where a research packet can leak the future. Its frames endpoint returns, for each company, the fact that was last filed and best fits the requested calendar period. A query run after Harbor's April 20 amendment would therefore serve the amended figure to an April 1 decision (our inference), so facts must be selected by filing date, not by period alone. The submissions endpoint holds at least a year of filings or the 1,000 most recent, whichever is more, and lists older filings in extra files, so a retriever that reads only the first object can call an old filing missing (our inference). The company-concept endpoint keeps a separate array of facts for each unit of measure, which turns a currency check into a lookup.

Index vintage matters just as much. Lewis and co-authors swapped the Wikipedia index behind a retrieval-augmented model between December 2016 and December 2018 and asked about 82 world leaders who had changed in between. The model answered 70% correctly with the 2016 index on 2016 leaders and 68% with the 2018 index on 2018 leaders, but only 12% and 4% when index and question disagreed. Answers followed the index, so the index snapshot belongs in the evidence record (our inference).

A citation needs its own test. Gao and co-authors' ALCE benchmark scores citation recall, whether the output is fully supported by the passages it cites, and citation precision, whether each citation is relevant, judging support with a natural-language-inference model. On ELI5 even the best models lacked complete citation support 50% of the time. Those are open-domain questions, not filings, but the check ports (our inference): test that each cited passage entails its claim.

Exercise: freeze the index as of March 1, April 1 and just after the April 20 amendment, and ask for prior-year revenue. Expect not found, the original 120 million, and the amendment as a separate later record. Then require every cited passage to entail its claim and to name the right issuer and period.""",
        [
            ('official', 'U.S. SEC', None, 'EDGAR Application Programming Interfaces (APIs)', 'https://www.sec.gov/search-filings/edgar-application-programming-interfaces',
             'Describes the submissions and XBRL endpoints: filing-history limits and extra files, per-unit fact arrays, last-filed frames and typical update delays.'),
            ('arxiv', 'Lewis et al.', 2020, 'Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks', 'https://arxiv.org/abs/2005.11401',
             "Introduces retrieval-augmented generation and shows by swapping a 2016 and a 2018 index that a model's answers follow the index it retrieves from."),
            ('arxiv', 'Gao, Yen, Yu & Chen', 2023, 'Enabling Large Language Models to Generate Text with Citations', 'https://arxiv.org/abs/2305.14627',
             'Benchmark that scores citation recall and precision with an entailment model; reports how often the best systems fail to fully support their answers with their citations.'),
        ],
    ),
    "5.23": (
        r"""Units are where a valid-looking number most often goes wrong, and the Inline XBRL specification shows how filings encode them. In financial statements a figure is commonly scaled for display in thousands, millions or billions, so the tagged element carries a scale attribute written as an exponent of ten: a value shown in thousands must be multiplied by 1,000 to give the stored fact, which is scale 3. A percentage shown as an integer is often stored as a decimal, and negative values are flagged by a separate sign attribute. For filings that carry these tags, the lesson's unit contract can be checked against the filing's own machine-readable scale and sign instead of the model's reading of a table header (our inference).

Syntax is a weaker guarantee than it sounds. Willard and Louf describe guided generation that constrains output with regular expressions and context-free grammars and guarantees the structure of the generated text. A grammar can force some number into the revenue field, so the schema also needs an explicit not-found branch (our inference).

Right answers can hide wrong inputs. Chen and co-authors built FinQA, 8,281 expert-annotated questions over S&P 500 earnings reports, and note that execution accuracy tends to overestimate performance because a model sometimes hits the correct answer by chance. In their 2021 baselines, generating the final number directly with the same architecture scored near zero, which they took as evidence that generating an executable reasoning program is necessary. By analogy (our inference), 20% growth should pass only if both revenue inputs trace to the filing, because 240 over 200 gives the same 20%.

Exercise: add that coincidence fixture, a pair of wrong-issuer inputs that still yields 20%, and require rejection on provenance rather than arithmetic. Then report false acceptances next to completeness.""",
        [
            ('docs', 'XBRL International', 2013, 'Inline XBRL Part 1: Specification 1.1', 'https://www.xbrl.org/Specification/inlineXBRL-part1/REC-2013-11-18/inlineXBRL-part1-REC-2013-11-18.html',
             "Defines the scale and sign attributes that connect a figure displayed in thousands or millions to its stored value, the machine-readable counterpart of the lesson's unit multiplier."),
            ('arxiv', 'Willard & Louf', 2023, 'Efficient Guided Generation for Large Language Models', 'https://arxiv.org/abs/2307.09702',
             'Constrains generation with regular expressions and grammars so the output structure is guaranteed, which fixes syntax but says nothing about whether a value is true.'),
            ('arxiv', 'Chen et al.', 2021, 'FinQA: A Dataset of Numerical Reasoning over Financial Data', 'https://arxiv.org/abs/2109.00122',
             'Expert-annotated numerical questions over earnings reports with gold reasoning programs; scores both execution and program accuracy because a right number can be a coincidence.'),
        ],
    ),
    "5.24": (
        r"""Debenedetti and co-authors built AgentDojo to measure agents that call tools over untrusted data: 97 tasks and 629 security test cases. Its simple tool filter, in which the model first restricts itself to the tools a task needs, lowered the attack success rate to 7.5%. It works when the user task needs only read access and the attack needs write access, which describes Harbor's research worker: with no transfer tool in its list, the cash-transfer instruction has nothing to call. It fails when the tools a task needs also suffice for the attack, which the authors count in 17% of their test cases.

Harbor's memo step is such a case. An injected line telling the model to rate a stock a strong buy needs no new tool, and the CaMeL defense, which separates control flow from untrusted data, lists attacks that affect neither flow, such as a summary that differs from its source, as outside its scope. Our inference: catching this falls to evidence validation and the unsupported-claim score, so keep a fixture for it.

Fixtures that run once also understate risk. NIST's Center for AI Standards and Innovation extended AgentDojo and found that attacks written for a newly upgraded model raised the success rate from 11% for the strongest baseline attack to 81%, and that repeating each attack 25 times raised the average from 57% to 80%. CaMeL's authors report solving 77% of AgentDojo tasks with what they describe as provable security, against 84% for an undefended system, so score utility beside the attack rate.

Exercise: run each prompt-injection fixture 25 times at production sampling settings and report the any-success rate per fixture. Assert on the call log and ledger, not on the prose: no tool outside the allowlist, no fifth call, and zero state changes.""",
        [
            ('arxiv', 'Debenedetti et al.', 2024, 'AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents', 'https://arxiv.org/abs/2406.13352',
             'A benchmark of 97 tasks and 629 security test cases for tool-calling agents, with the tool-filter defense and an account of when it fails.'),
            ('arxiv', 'Debenedetti et al.', 2025, 'Defeating Prompt Injections by Design', 'https://arxiv.org/abs/2503.18813',
             'CaMeL keeps untrusted data out of control flow and checks policies at tool calls; its stated non-goals include text-to-text attacks.'),
            ('official', 'NIST · CAISI', 2025, 'Technical Blog: Strengthening AI Agent Hijacking Evaluations', 'https://www.nist.gov/news-events/news/2025/01/technical-blog-strengthening-ai-agent-hijacking-evaluations',
             'Shows that fixed single-attempt hijacking tests understate risk compared with adaptive attacks and repeated attempts.'),
        ],
    ),
    "5.25": (
        r"""Little proved that, under stationarity and finite means, the mean number of units in a system equals the arrival rate times the mean time each unit spends there: L = λW. Our inference: queue depth divided by the consumer's throughput estimates how old the newest accepted event is when served. At 80 events a second and a five-second freshness limit, a backlog above 5 × 80 = 400 events serves stale work. With the 20-a-second surplus, an unbounded queue that starts empty crosses 400 after 20 seconds, while a 200-slot queue caps the wait at 200 ÷ 80 = 2.5 seconds.

Retries can keep an overload alive after its cause has gone, a pattern called metastable failure. Alvaro and co-authors modelled a request-response server and found a queue length beyond which average latency exceeds the client timeout; the retries this triggers tend to keep a filled queue full. Huang and co-authors studied 22 metastable failures from 11 organisations: retry policy sustained more than 50% of them, and recovery often required reducing load. The lesson's 1, 2 and 4 second delays put the third retry at 7 seconds, after a five-second decision has expired.

Amazon's Builders' Library supplies the remedies. A timeout does not prove that side effects failed to happen, so it treats calls with side effects as safe to retry only when idempotent; for orders, our inference is a stable client identifier plus reconciliation first. It also limits retries locally with a token bucket shared by all calls: they may retry while tokens last, then at a fixed rate.

Exercise: feed 100 events a second to an 80-a-second consumer for a minute. Drop non-fill events older than five seconds at dequeue, and check that no fill is lost and retries stay inside the bucket.""",
        [
            ('paper', 'Little', 1961, 'A Proof for the Queuing Formula: L = λ W', 'https://doi.org/10.1287/opre.9.3.383',
             'States L = λW for the mean number in a queueing system, the arrival rate and the mean time in the system, under stationarity and finite means.'),
            ('arxiv', 'Alvaro et al.', 2025, 'Formal Analysis of Metastable Failures in Software Systems', 'https://arxiv.org/abs/2510.03551',
             'Models a request-response server with a queue, timeouts and retries, and locates the queue length where retries keep a filled queue full.'),
            ('paper', 'Huang et al.', 2022, 'Metastable Failures in the Wild', 'https://www.usenix.org/conference/osdi22/presentation/huang-lexiang',
             'Studies 22 metastable failures from 11 organisations in public incident reports; retry policy is the most common sustaining effect.'),
            ('docs', "Amazon Web Services · Builders' Library", None, 'Timeouts, retries, and backoff with jitter', 'https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/',
             'Engineering guidance on idempotency before retrying calls with side effects, and on limiting retries locally with a token bucket.'),
        ],
    ),
    "5.26": (
        r"""SQLite's documentation separates two failures that a restart test can blur. Transactions are durable across application crashes under every setting. A transaction committed in WAL mode with synchronous=NORMAL, though, might roll back after a power loss or system crash, and FULL in rollback mode is not necessarily durable across a power loss. By its matrix, only synchronous=FULL in WAL mode and synchronous=EXTRA are marked ACID. A test that kills the process and reopens the file exercises only the first case. Our inference: a halt flag lost to a power cut leaves a restarted bot willing to trade, so print journal_mode and synchronous at startup and keep the ledger on one of them.

Mohan and co-authors' ARIES recovery method repeats history on restart: it redoes missing updates before rolling back unfinished transactions, a log sequence number on each page shows which logged updates the page already holds, and logging stays bounded even if restart itself fails repeatedly. Our inference: a fill's unique identity plays the sequence number's role in Harbor's ledger, so replay onto a stale cache applies each fill at most once, and the recovery pass must itself survive a crash.

Pillai and co-authors traced the update protocols of eleven widely used systems in 2014 and found 60 vulnerabilities, because correctness depends on file-system behaviours they call persistence properties; for SQLite they report no durability in the default journal mode. Gu and co-authors note that the crash-state space grows exponentially with the operation count; their Pathfinder tests a small set of representative crash states, finding 18 bugs across 8 production-ready systems.

Exercise: kill the process before each statement of the fill update and just after the commit, reopen, and check that cash and positions match the fills table and the halt flag is unchanged; then kill it again during reconciliation.""",
        [
            ('paper', 'Mohan et al.', 1992, 'ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging', 'https://doi.org/10.1145/128765.128770',
             'Recovery with write-ahead logging that repeats history on restart, using per-page log sequence numbers to tell which logged updates are already applied.'),
            ('docs', 'SQLite contributors', None, 'PRAGMA Statements', 'https://www.sqlite.org/pragma.html#pragma_synchronous',
             'Documents what each synchronous setting guarantees in WAL and rollback-journal modes, separating application crashes from power loss.'),
            ('paper', 'Pillai et al.', 2014, 'All File Systems Are Not Created Equal: On the Complexity of Crafting Crash-Consistent Applications', 'https://www.usenix.org/conference/osdi14/technical-sessions/presentation/pillai',
             'Analyses the update protocols of eleven widely used systems, including SQLite, and finds 60 crash vulnerabilities tied to file-system behaviour.'),
            ('arxiv', 'Gu et al.', 2025, 'Scalable and Accurate Application-Level Crash-Consistency Testing via Representative Testing', 'https://arxiv.org/abs/2503.01390',
             'Pathfinder tests applications against representative crash states, since the full crash-state space grows exponentially with the operations.'),
        ],
    ),
    "5.27": (
        r"""Dapper's authors held that monitoring should always be on, because unusual behaviour is often difficult or impossible to reproduce. Spans carry a span id and a parent id, every span in a trace shares one trace id, and when work is deferred or made asynchronous the callbacks store the trace context of their creator. Our inference: Harbor's correlation id must travel inside the queued event, or the consumer's log lines become orphans. Dapper sampled to keep overhead low in latency-sensitive services; an intent, order and fill trail is an audit record, and at 200 proposals a window it needs no sampling (our inference).

A process can look healthy while doing no useful work. Huang and co-authors, writing about gray failure in cloud systems, point to differential observability: the system's failure detectors may not notice problems even when applications are afflicted by them. The SRE book counts errors explicitly, implicitly (a success response with the wrong content) and by policy, and notes that white-box monitoring can reveal failures masked by retries. Our inference: an acknowledgement after the freshness limit is an error by policy, so alert on unknown-order age and log attempts per order beside the success rate.

Yan and co-authors analysed four years of incidents at a leading generative AI cloud provider. Of those incidents, 38.3% were reported by humans, and incidents that came with a troubleshooting guide were resolved more swiftly than those without one. Our suggestion: put the runbook link and the correlation ids in the alert itself.

Exercise: stop the feed for ten minutes while the process stays up, then record which alert fires first, how long after the last quote, and whether it names the runbook.""",
        [
            ('paper', 'Sigelman et al.', 2010, 'Dapper, a Large-Scale Distributed Systems Tracing Infrastructure', 'https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/',
             "Google's tracing design: trace, span and parent ids, with trace context carried through asynchronous callbacks, and the case for always-on monitoring."),
            ('paper', 'Huang et al.', 2017, 'Gray Failure', 'https://doi.org/10.1145/3102980.3103005',
             'Argues that failure detectors can miss problems that applications feel, a gap the authors call differential observability.'),
            ('docs', 'Google SRE', None, 'Monitoring Distributed Systems', 'https://sre.google/sre-book/monitoring-distributed-systems/',
             "The SRE book's chapter on symptoms versus causes, white-box and black-box monitoring, and errors defined explicitly, implicitly or by policy."),
            ('arxiv', 'Yan et al.', 2025, 'An Empirical Study of Production Incidents in Generative AI Cloud Services', 'https://arxiv.org/abs/2504.08865',
             'Four years of incidents at a leading generative AI cloud provider: who detects them, and how troubleshooting guides affect time to mitigate.'),
        ],
    ),
    "5.28": (
        r"""FINRA Regulatory Notice 15-09 is addressed to member firms and says its practices would not necessarily satisfy a firm's obligations by themselves, so treat it as a checklist to borrow. Several practices map onto the lesson's packet: change management that reviews test results and scales approvals to the change; testing independent of development and segregated from production, with records of protocols and results; archived code versions; a way to disable the algorithm in a minimal number of steps; and a pilot of limited size, increased only as results are confirmed. Our inference: the archive is the rollback target, and a gate with no recorded evidence or approver is a checkbox.

Google's SRE Workbook defines canarying as a partial, time-limited deployment of a change together with its evaluation, compares the canary with a control that keeps the old version, and calls before-and-after comparison risky. It reports that a majority of Google's incidents are triggered by binary or configuration pushes, and its example without a rollback option ends with a patch deployed mid-outage. Our inference: run the candidate beside the incumbent on the same frozen replay, compare decisions on identical bars, and treat a changed threshold or feature schema as a release.

Lindon and co-authors at Netflix treat canary tests as a common quality control gate and propose sequential tests that allow continuous monitoring while strictly controlling the false detection probability. A fixed-sample test checked after every fill offers no such guarantee (our inference), so write the stopping rule into the release record before the canary starts.

Exercise: make each gate a command that exits nonzero on failure and fail the persistent-halt gate on purpose; confirm the packet reads blocked despite a positive simulated return, then roll back to the archived build and reconcile before resuming.""",
        [
            ('official', 'FINRA', 2015, 'Regulatory Notice 15-09: Guidance on Effective Supervision and Control Practices for Firms Engaging in Algorithmic Trading Strategies', 'https://www.finra.org/rules-guidance/notices/15-09',
             'Regulator guidance on change management, independent testing, archived code, quick disablement and limited pilots for algorithmic strategies.'),
            ('docs', 'Google SRE', None, 'Canarying Releases', 'https://sre.google/workbook/canarying-releases/',
             'The SRE Workbook chapter on canary and control populations, metric choice, why before-and-after comparison is risky, and rollback.'),
            ('arxiv', 'Lindon, Sanden & Shirikian', 2022, 'Rapid Regression Detection in Software Deployments through Sequential Testing', 'https://arxiv.org/abs/2205.14762',
             'Sequential tests that let a canary be monitored continuously while controlling the false detection probability, shown on two Netflix case studies.'),
        ],
    ),
    "5.38": (
        r"""The hedge ratio carries more of the signal than it appears to. In the lesson's fit the residual is 3 at A = 80 and B = 50, but B costs 50 per unit, so a slope of 1.56 instead of 1.5 already erases it, and 1.6, which is also the dollar-neutral ratio 80/50, reverses it to −2: sell-the-spread becomes buy-the-spread on identical prices (our arithmetic). Compare the slope's standard error times the leg price with the entry threshold.

Clegg and Krauss let the "cointegrating" residual hold both a random walk and a mean-reverting component, and supply a likelihood-ratio test for it. On S&P 500 constituents from 1990 until 2015 they report annualized returns of more than 12% after transaction costs, well above classical distance-based or cointegration-based variants. Our inference: a rolling estimate of the random-walk share is a better invalidation signal than one stationarity test, since a spread with a large random-walk part can keep running against a position while no single test fails.

Krauss's survey sorts pairs research into five groups. The lesson's pipeline spans two, a cointegration stage that selects and hedges and a time-series stage that sets trading rules, so log failures per stage. Tadi and Kortchmeski take the look-back window from the half-life of the fitted mean reversion and count an order only when the quoted size is available, one or more periods after the signal. Our inference: applied to each leg separately, that rule yields one-leg fills, and the exposure they leave belongs in the report.

Exercise: plant a pair whose slope moves from 1.5 to 1.6 on a known date, compare a frozen slope with one refit over a half-life-sized window, and reject the short leg at random. Record periods to exit, loss while stale, and periods with one leg.""",
        [
            ('paper', 'Clegg & Krauss', 2018, 'Pairs trading with partial cointegration', 'https://doi.org/10.1080/14697688.2017.1370122',
             'Weakens cointegration so the residual can mix a random walk with a mean-reverting part, adds an estimation routine and likelihood-ratio test, and benchmarks it on S&P 500 constituents from 1990 until 2015.'),
            ('paper', 'Krauss', 2017, 'Statistical arbitrage pairs trading strategies: review and outlook', 'https://doi.org/10.1111/joes.12153',
             'Survey of pairs-trading frameworks in five groups (distance, cointegration, time-series, stochastic control, other), with profitability reviewed in the light of market frictions.'),
            ('arxiv', 'Tadi & Kortchmeski', 2021, 'Evaluation of Dynamic Cointegration-Based Pairs Trading Strategy in the Cryptocurrency Market', 'https://arxiv.org/abs/2109.10662',
             'Sets the look-back window from the half-life of a calibrated Ornstein-Uhlenbeck spread and backtests against best bid and ask quotes, counting an order only when the quoted size is available.'),
        ],
    ),
    "5.39": (
        r"""Barroso and Santa-Clara found that the risk of momentum is highly variable over time and predictable, and that managing it virtually eliminated crashes and nearly doubled the strategy's Sharpe ratio. Our inference: a target pays only while risk persists, and a dated estimate cannot see a jump coming. With the lesson's 5% estimate, the 1.2 cap and a 20-day equal-weight window, a 5% daily move lifts the estimate to about 18% and cuts the next scale to 0.54, but the move itself is taken at 1.2, a 6% loss, where the uncapped 2 would lose 10% (our arithmetic). On day one the cap, not the estimator, limits the damage, so the jump fixture should assert both.

Inverse volatility is not risk parity in general. Maillard, Roncalli and Teïletche make each component's risk contribution equal, maximizing the diversification of risk at least on an ex ante basis, and show that the resulting volatility lies between those of minimum-variance and equally weighted portfolios. For the lesson's two assets the constructions coincide at any correlation: weights proportional to 1/σ give each asset half of the variance (our arithmetic). The gap needs three assets. With 10% volatility each and two correlated at 0.9, inverse volatility gives thirds, yet the correlated pair supplies about 79% of the variance; equal-risk weights are about 30%, 30% and 41%. Griveau-Billion and co-authors propose a cyclical coordinate descent algorithm for high-dimensional risk parity that converges and stays fast with more than 500 assets.

Exercise: rerun the jump fixture with the cap at 1.2 and with none, and log each asset's variance share, its weight times its entry in Σw over total variance, for both weight sets. Equal shares should appear only for the equal-risk set, and only under the covariance estimate that produced it.""",
        [
            ('paper', 'Barroso & Santa-Clara', 2015, 'Momentum has its moments', 'https://doi.org/10.1016/j.jfineco.2014.11.010',
             'Finds the risk of momentum highly variable over time and predictable, and that scaling the strategy by its own risk virtually eliminates crashes and nearly doubles its Sharpe ratio.'),
            ('paper', 'Maillard, Roncalli & Teïletche', 2010, 'The Properties of Equally Weighted Risk Contribution Portfolios', 'https://doi.org/10.3905/jpm.2010.36.4.060',
             'Defines portfolios whose components contribute equal risk, ex ante, and shows their volatility lies between that of minimum-variance and equally weighted portfolios.'),
            ('arxiv', 'Griveau-Billion, Richard & Roncalli', 2013, 'A Fast Algorithm for Computing High-dimensional Risk Parity Portfolios', 'https://arxiv.org/abs/1311.4057',
             'Cyclical coordinate descent algorithm for risk parity problems that converges and stays fast on large covariance matrices (n > 500), compared with existing algorithms.'),
        ],
    ),
}
