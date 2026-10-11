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
        r"""Two clocks sit behind every event a bot receives. Akidau and co-authors, describing a model for processing unbounded and out-of-order data, define event time as when an event actually occurred and processing time as when the pipeline observes it. They stress that the skew between the two is inherent and keeps changing, and that a system usually lacks the knowledge to build a fully correct watermark, its running estimate of how complete the data is. A bot faces the same problem with a sharper edge, because a dashboard can quietly revise a late number but an order cannot be retracted. My inference is that the late-event rule belongs in the specification: say in advance what happens to an event that arrives after the decision it should have informed.

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
        r"""Treat the trading clock as data. The NYSE's published calendar lists Friday 3 July 2026 as a holiday (Independence Day observed) and early 1:00 p.m. Eastern closes on Friday 27 November and Thursday 24 December 2026. Sessions also differ by venue: the core session runs from 9:30 a.m. to 4:00 p.m., but NYSE Arca's early session starts at 4:00 a.m. and late trading runs until 8:00 p.m. My inference for Harbor: on an early-close day a completed daily bar exists three hours sooner than usual, so a calendar that assumes a 4:00 p.m. close delays the signal, and one that assumes a session on 3 July may mistake a missing bar for a zero return.

Feeds also stamp events with more than one clock. Bartlett and McCrary used the microsecond timestamps recorded by the two centralized processors that consolidate U.S. exchange quotes and trades. In a sample running from August 2015 to June 2016 they found average reporting latencies of 1.13 milliseconds for quotes and 22.84 milliseconds for trades, and they note that the exchanges' own participant timestamps were recorded only in milliseconds. Which clock a freshness limit such as the lesson's 750 milliseconds uses is therefore part of the data contract.

Documents have the same problem. Under the SEC's Regulation S-T, an electronic filing submitted after 5:30 p.m. Eastern is deemed filed on the next business day, although some insider and ownership forms get a 10 p.m. cutoff. A filing date is a legal label, not a clock reading, so a bot that stores only the date cannot say whether the document was readable at 10:00 a.m. that day. My suggestion: store the acceptance time when the source provides one, and otherwise treat the document as usable only after the full filing date has passed.

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
}
