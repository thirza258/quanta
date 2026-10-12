"""Research extensions for Trading ethics & market conduct.

Each entry maps a lesson ID to (body, sources). A source is
(kind, authors, year, title, url, what it contributes); see research_depth.py.
Every figure was checked against a verbatim snippet from its source before merging.
"""

NOTES = {
    "12.1": (
        r"""The lesson's rule has a long legal ancestry. In SEC v. Capital Gains Research Bureau, the U.S. Supreme Court read the Investment Advisers Act as showing a congressional intent to eliminate, or at least to expose, every conflict that might incline an adviser, consciously or unconsciously, to give advice that was not disinterested. It refused to make the SEC prove an intent to injure or an actual injury to clients, the legal counterpart of the lesson's point that a client doing well does not excuse an undisclosed benefit. Regulation Best Interest is the parallel rule for broker-dealers recommending to retail customers (registered advisers answer to the Advisers Act instead): act in the customer's best interest when recommending, without putting the firm's or representative's own interest ahead. The SEC's adopting release adds a limit that the lesson's arithmetic needs: cost must be considered but is not the only factor, and the standard does not necessarily require the lowest-cost option. A dearer Fund B is therefore not automatically a breach; what is tested is whether the payment was identified and kept from driving the choice.

Evidence on how payments reach advice is uncomfortable. In an audit, Mullainathan, Noeth and Schoar sent trained auditors to advisers carrying portfolios that either served or cut against the advisers' interests. The advisers failed to de-bias clients, often reinforced biases that suited them, and pushed actively managed, higher-fee funds even when the client began with a diversified, low-fee portfolio. Surveying retirement-account research, the White House Council of Economic Advisers estimated in 2015 that conflicted advice lowers returns by roughly 1 percentage point a year, about $17 billion annually, while saying its conclusions were subject to uncertainty.

The lesson's gap is also one percentage point: 1.20% against 0.20%, or Rp5 million a year on Rp500 million, with Rp2 million going to the adviser. That shows scale only: the Council's figure is a return shortfall, the lesson's a fee difference.

Exercise: restate any recommendation as if both products paid the adviser the same. If the case for the dearer one no longer stands, the payment was doing the work.""",
        [
            ('official', 'U.S. Supreme Court', 1963, 'Securities and Exchange Commission v. Capital Gains Research Bureau, Inc.', 'https://www.law.cornell.edu/supremecourt/text/375/180',
             'The leading adviser-fiduciary decision: conflicts must be eliminated or exposed, and the SEC need not prove intent to injure or actual injury.'),
            ('official', 'U.S. SEC', 2019, 'Regulation Best Interest: The Broker-Dealer Standard of Conduct', 'https://www.federalregister.gov/documents/2019/07/12/2019-12164/regulation-best-interest-the-broker-dealer-standard-of-conduct',
             'Rule text and adopting release for the broker-dealer best-interest standard, including its statement that cost matters but is not dispositive.'),
            ('paper', 'Mullainathan, Noeth & Schoar', 2012, 'The Market for Financial Advice: An Audit Study', 'https://doi.org/10.3386/w17929',
             'Audit study in which advisers reinforced biases that served their own interests and pushed higher-fee active funds.'),
            ('official', 'Council of Economic Advisers', 2015, 'The Effects of Conflicted Investment Advice on Retirement Savings', 'https://obamawhitehouse.archives.gov/sites/default/files/docs/cea_coi_report_final.pdf',
             'Government literature review that puts a rough annual price on conflicted retirement advice and states its own uncertainty.'),
        ],
    ),
    "12.2": (
        r"""The lesson says to disclose early and in plain view. The research shows why that is necessary but not sufficient. On the rule side, the SEC's order approving FINRA Rule 2241 describes what a research report must say when it is published: whether the analyst or a household member has a financial interest in the subject company's securities, including long or short positions and options, and the nature of that interest. For the analyst's own interest the description sets no size threshold, while a firm's holding is flagged at 1% of a class of common equity, and a catch-all covers any other material conflict. The lesson's Pelita holding, 15% of the author's portfolio, would therefore be disclosable whatever its size to the firm.

Psychology adds a warning. Cain, Loewenstein and Moore showed that people generally do not discount advice from a conflicted adviser enough even when the conflict is disclosed, and that disclosure can increase the bias because advisers feel morally licensed to exaggerate. Sah, Loewenstein and Cain reported six experiments in which disclosure also raised the pressure to comply, because advisees felt obliged to satisfy the adviser's personal interests. That pressure fell when the disclosure came from an external source rather than the adviser, when it was not common knowledge between the two, or when the advisee could change their mind later. Onuchic's theoretical model adds a design problem: mandated transparency about a seller's motives can discourage the seller from sharing, or even acquiring, information about the product's value.

These are laboratory and model results, not measurements of real research notes, so read them as cautions. An inference, not a finding, is that a disclosure line is a minimum: who delivers it, and whether the reader can still act differently afterwards, matter as much as where it sits.

Exercise: write the first sentence of a Pelita Manufaktur note so that it states the long position, its weight in the author's portfolio and the purchase date before any recommendation. Then add a pointer to a public source the reader can check without relying on you.""",
        [
            ('official', 'U.S. SEC', 2015, 'Order Approving a Proposed Rule Change, as Modified by Amendment No. 1 Thereto, To Adopt FINRA Rule 2241 (Research Analysts and Research Reports) in the Consolidated FINRA Rulebook', 'https://www.federalregister.gov/documents/2015/07/22/2015-17971/self-regulatory-organizations-financial-industry-regulatory-authority-inc-order-approving-a-proposed',
             "Describes the research-report disclosures FINRA Rule 2241 requires, including the analyst's financial interest, the 1% firm-ownership trigger and the catch-all for other material conflicts."),
            ('paper', 'Cain, Loewenstein & Moore', 2005, 'The Dirt on Coming Clean: Perverse Effects of Disclosing Conflicts of Interest', 'https://doi.org/10.1086/426699',
             "Shows that recipients under-discount disclosed conflicts and that disclosure can make advisers' advice more biased."),
            ('paper', 'Sah, Loewenstein & Cain', 2013, 'The burden of disclosure: Increased compliance with distrusted advice', 'https://doi.org/10.1037/a0030527',
             'Six experiments showing disclosure can raise pressure on advisees to comply, and which arrangements reduce that pressure.'),
            ('arxiv', 'Onuchic', 2021, 'Advisors with Hidden Motives', 'https://arxiv.org/abs/2103.07446',
             'A model of an adviser whose payoff depends on which product is sold, with a result on how mandated transparency about motives changes what the adviser shares.'),
        ],
    ),
    "12.3": (
        r"""Regulators already ask for the discipline this lesson teaches. Article 24 of the EU's MiFID II directive says information on all costs and charges, including third-party payments, must be aggregated so that the client can see the overall cost and its cumulative effect on return. An inducement is allowed only if it is designed to enhance the quality of the service and does not impair the duty to act in the client's best interest, and its existence, nature and amount must be disclosed before the service is provided. Firms giving independent advice or managing portfolios may not keep third-party payments at all, apart from minor non-monetary benefits that are disclosed.

The research shows why visibility matters. Barber, Odean and Zheng studied 30 years of mutual fund flows. Flows fell with front-end loads but showed no relation to operating expenses, a result they attribute to marketing and advertising costs often embedded in those expenses. Christoffersen, Evans and Musto found that brokers' shares of sales loads and other revenue had significant effects on funds' inflows, particularly for unaffiliated brokers, and that load sharing, but not revenue sharing, predicted poor performance. Read together, these studies suggest that investors respond to the charges they can see, and that payments to intermediaries can steer money whether or not the client has understood them.

The cumulative effect is easy to compute. Levine shows that an annual fee of ε% of assets for N years costs almost N×ε% of the final value, compared with an identical investment paying no fee:

$$
1-(1-\varepsilon)^{N} \approx N\varepsilon
$$

For the lesson's 1.74% a year and N = 10, the shortcut gives 17.4% and the exact figure is 16.1%. If turnover rises to four times a year, total cost becomes 2.34% and the ten-year shortfall about 21.1%. These are illustrations rather than findings, and they treat every cost as a yearly share of assets.

Exercise: put your own total cost and horizon into the formula, then compare the shortfall with the benefit you expect from the extra turnover or the dearer product.""",
        [
            ('official', 'European Parliament & Council of the EU', 2014, 'Directive 2014/65/EU (MiFID II), Article 24: General principles and information to clients', 'https://www.legislation.gov.uk/eudr/2014/65/article/24',
             'Article 24 of MiFID II, as reproduced by legislation.gov.uk: aggregated cost disclosure, the conditions for inducements, and the ban on keeping third-party payments in independent advice and portfolio management.'),
            ('paper', 'Barber, Odean & Zheng', 2005, 'Out of Sight, Out of Mind: The Effects of Expenses on Mutual Fund Flows', 'https://doi.org/10.1086/497042',
             'Thirty years of fund flows: investors respond to salient front-end loads but not to operating expenses.'),
            ('paper', 'Christoffersen, Evans & Musto', 2013, 'What Do Consumers’ Fund Flows Maximize? Evidence from Their Brokers’ Incentives', 'https://doi.org/10.1111/j.1540-6261.2012.01798.x',
             'Shows that the payments brokers receive from funds influence where investor money goes, and that load sharing and revenue sharing predict performance differently.'),
            ('arxiv', 'Levine', 2021, 'Investment AUM Fee Costs: Evaluating a Simple Formula', 'https://arxiv.org/abs/2107.00837',
             'Derives and tests the shortcut that an annual percentage fee over N years costs almost N times the fee rate in final value.'),
        ],
    ),
    "12.4": (
        r"""The legal floor differs by type of firm and is thinner than the lesson's controls. For broker-dealers, FINRA Rule 5270, carried over from NASD interpretation IM-2110-3, restricts trading in the same security or a related instrument, for an account in which a member or associated person has an interest, while holding material non-public information about an imminent block order. The earlier interpretation treated 10,000 shares or more as generally a block, so the lesson's 400,000-share order is 40 times that level. Exceptions apply only where the member can demonstrate that the trade was unrelated to the information. For investment advisers, Rule 204A-1 requires access persons to report holdings and transactions, with quarterly transaction reports due within 30 days after quarter-end, and requires pre-approval only for IPOs and limited offerings. A report that late cannot stop a purchase made ahead of a client order, so pre-clearance and blackouts for ordinary shares are firm policy beyond the minimum.

The lesson's second control, a pre-committed plan, can also be gamed. Jagolinzer found that insiders' sales under Rule 10b5-1 plans systematically followed positive and preceded negative firm performance, earning abnormal returns larger than colleagues without plans. The SEC's 2022 adopting release cites that study among others, and its amendments added a cooling-off period: directors and officers wait the later of 90 days after adoption or two business days after the quarter's results are filed, capped at 120 days, while other persons wait 30 days.

Front-running also needs no dishonest employee. Daian and co-authors documented bots on decentralized exchanges that pay high fees to be ordered ahead of ordinary users' trades, which they describe as anticipating and exploiting those trades. An inference, not a finding of that paper: wherever the profit comes from knowing an order is pending, a control must remove the knowledge or the opportunity.

Exercise: apply the lesson's two-business-day buffer to a desk order running Tuesday and Wednesday. The blackout runs from the previous Friday to the following Friday, six business days. Then list which of your own personal trades in covered names last quarter would have fallen inside such a window.""",
        [
            ('official', 'U.S. SEC', 2012, 'Order Approving Proposed Rule Change, as Modified by Amendment No. 1, To Adopt Existing NASD IM-2110-3 as New FINRA Rule 5270 (Front Running of Block Transactions) With Changes in the Consolidated FINRA Rulebook', 'https://www.federalregister.gov/documents/2012/09/10/2012-22139/self-regulatory-organizations-financial-industry-regulatory-authority-inc-order-approving-proposed',
             'Describes what the front-running rule covers, the 10,000-share block benchmark inherited from NASD IM-2110-3, and the requirement that excepted trades be demonstrably unrelated.'),
            ('official', 'U.S. SEC', 2004, 'Investment adviser codes of ethics, Rule 204A-1 under the Investment Advisers Act (17 CFR 275.204A-1)', 'https://www.ecfr.gov/current/title-17/chapter-II/part-275/section-275.204A-1',
             'Current rule text: what a code of ethics must require of access persons, including quarterly transaction reports and pre-approval only for IPOs and limited offerings.'),
            ('official', 'U.S. SEC', 2022, 'Insider Trading Arrangements and Related Disclosures', 'https://www.federalregister.gov/documents/2022/12/29/2022-27675/insider-trading-arrangements-and-related-disclosures',
             'The adopting release for the 2022 Rule 10b5-1 amendments: the studies it cites and the cooling-off periods it added.'),
            ('paper', 'Jagolinzer', 2009, "SEC Rule 10b5-1 and Insiders' Strategic Trade", 'https://doi.org/10.1287/mnsc.1080.0928',
             "Evidence that insiders' sales under Rule 10b5-1 plans were well timed relative to later firm performance."),
            ('arxiv', 'Daian et al.', 2019, 'Flash Boys 2.0: Frontrunning, Transaction Reordering, and Consensus Instability in Decentralized Exchanges', 'https://arxiv.org/abs/1904.05234',
             "Documents bots that pay for priority ahead of other users' pending trades, a mechanical form of front-running."),
        ],
    ),
    "12.5": (
        r"""The lesson's m = ΔR/R is a magnitude screen, not the legal test. In Basic v. Levinson the Supreme Court adopted the standard of a substantial likelihood that a reasonable investor would view a fact as significantly altering the total mix of information. For contingent or speculative events it described materiality as a balancing of the indicated probability that the event occurs against its anticipated magnitude. In our reading, Rp72 billion is the example's magnitude and the word "plausibly" carries its probability.

Regulation FD gives a yardstick for the second test. It binds issuers, not recipients, but it counts disclosure as public only through a Form 8-K or another method reasonably designed for broad, non-exclusionary distribution. A fact passed among a few people fails that description, however many they are.

Ahern's data on illegal tipping show how such facts travel: information moved through family, friends and geographic proximity, tips from corporate executives reached buy-side investors on average after three links, and the traders earned 35% over 21 days. Our inference: after three links a fact has lost its source and sounds like gossip.

Researchers look for the footprint in prices. Pham and Ausloos ran an event study of abnormal returns before first merger announcements, using London Stock Exchange data for 2008-2012 and 2015-2019. They found the returns reduced after the Financial Services Act 2012 and insignificant in 2015-2019, and concluded that the UK regulator is efficient. Our inference: no run-up could also mean better concealment.

Exercise: for the lesson's halt, draw the chain of who told whom and mark any public link. Then, for a past announcement, subtract the index return from the stock's four-day pre-announcement return.""",
        [
            ('official', 'U.S. Supreme Court', 1988, 'Basic Inc. v. Levinson', 'https://www.law.cornell.edu/supremecourt/text/485/224',
             'Adopts the TSC Industries reasonable-investor standard for Rule 10b-5 and describes materiality of contingent events as a balance of probability and magnitude.'),
            ('official', 'U.S. SEC', 2000, 'Regulation FD, selective disclosure (17 CFR 243.100 to 243.102)', 'https://www.ecfr.gov/current/title-17/chapter-II/part-243/section-243.101',
             'Current rule text: public disclosure means a Form 8-K or another method reasonably designed to give broad, non-exclusionary distribution to the public.'),
            ('paper', 'Ahern', 2017, 'Information networks: Evidence from illegal insider trading tips', 'https://doi.org/10.1016/j.jfineco.2017.03.009',
             'Hand-collected data on illegal tipping networks: how inside information moves through social ties, how many links it takes to reach investors, and what the traders earned.'),
            ('arxiv', 'Pham & Ausloos', 2020, "Insider trading in the run-up to merger announcements. Before and after the UK's Financial Services Act 2012", 'https://arxiv.org/abs/2012.11594',
             'Event study of abnormal returns before first merger announcements on London data, used here as a measure of the footprint left by trading on non-public information.'),
        ],
    ),
    "12.6": (
        r"""The lesson's ratios are evidence of intent, and intent is the legal test. U.S. futures law prohibits bidding or offering with the intent to cancel before execution. The CFTC reads that as requiring intent beyond recklessness, excuses cancellations made in a good-faith attempt to trade, denies a partial fill automatic protection, and says a single instance can violate the rule if the intent was prohibited. It weighs trading patterns and fill characteristics together with the other facts and circumstances.

The regulator's ratio also differs from the lesson's. Under EU Delegated Regulation 2017/566 a venue computes, in number terms, (total orders ÷ total transactions) − 1 for each member and instrument, counting submission, modification and cancellation messages as orders. Its stated aim is to stop algorithms contributing to disorderly trading, so a breach is a market-quality flag, not evidence of intent (our inference). On that definition the example's ratio is at least (950 ÷ 15) − 1, about 62.3, and rises with its cancellations and modifications.

JPMorgan's 2020 CFTC order shows the supervisory side. From at least 2008 through 2016, traders placed hundreds of thousands of orders intending to cancel them, and the firm's futures broker was found to have failed to supervise despite internal surveillance alerts and exchange inquiries. Total monetary relief was $920.2 million. A flagged ratio starts an investigation; it does not end one.

Detection research treats flags as triage: Kularatnam and Stathaki train a weakly supervised model to flag suspicious order-book sequences, then send flagged states to expert assessment, reporting only preliminary results.

Exercise: write down the purpose of each frequently cancelled order type in your strategy, then recompute your ratio on the venue's definition.""",
        [
            ('official', 'U.S. CFTC', 2013, 'Antidisruptive Practices Authority', 'https://www.federalregister.gov/documents/2013/05/28/2013-12365/antidisruptive-practices-authority',
             'Interpretive guidance on the statutory spoofing ban: the intent standard, good-faith cancellations, partial fills, single instances, and the practices and patterns the Commission weighs.'),
            ('official', 'U.S. CFTC', 2020, 'CFTC Orders JPMorgan to Pay Record $920 Million for Spoofing and Manipulation', 'https://www.cftc.gov/PressRoom/PressReleases/8260-20',
             "Enforcement example: the period, the scale of the orders, the money ordered, and the finding that the firm's supervision failed despite surveillance alerts."),
            ('official', 'European Commission', 2016, 'Commission Delegated Regulation (EU) 2017/566 on the ratio of unexecuted orders to transactions', 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32017R0566',
             'Defines the venue ratio of unexecuted orders to transactions, its formula and counting rules, and the disorderly-trading purpose behind it.'),
            ('arxiv', 'Kularatnam & Stathaki', 2024, 'Detecting and Triaging Spoofing using Temporal Convolutional Networks', 'https://arxiv.org/abs/2403.13429',
             'Workshop paper that treats order-book flags as triage for expert review rather than as findings; preliminary results only.'),
        ],
    ),
    "12.7": (
        r"""The lesson's 37.5 days says the promoters cannot sell at ordinary volume. Aggarwal and Wu's evidence suggests how the exit becomes possible. In SEC manipulation cases, manipulators were typically plausibly informed parties such as insiders and brokers; manipulation raised volatility, liquidity and returns; prices rose through the campaign and fell afterwards; and prices and liquidity were higher when manipulators sold than when they bought. Their model adds that more information seekers mean more competition for shares, which makes it easier for the manipulator to trade. Our inference: the denominator is not fixed, because the campaign itself raises volume, so measure the ratio on pre-promotion volume.

The same condition appears in crypto. La Morgia and co-authors note that many cryptocurrencies have low liquidity and are therefore highly prone to manipulation, and they analyse pump-and-dump schemes organised by communities over the Internet.

The law's floor is disclosure. In SEC v. Capital Gains Research Bureau the Court held that scalping, buying shortly before recommending a security and selling after the rise that follows, operates as a fraud on clients, and that the SEC may obtain an injunction requiring full disclosure of the practice. Securities Act section 17(b) makes it unlawful to publicise a security for consideration from an issuer, underwriter or dealer without disclosing the receipt and the amount. Its text does not reach an unpaid holder who plans to sell. The lesson's rule against trading against your own message is stricter than either (our reading).

Exercise: for a promoted ticker, estimate the promoter's holding divided by pre-promotion average daily volume, and write down who paid for the message.""",
        [
            ('paper', 'Aggarwal & Wu', 2006, 'Stock Market Manipulations', 'https://doi.org/10.1086/503652',
             'Theory and evidence from SEC enforcement actions on who manipulates, how prices and liquidity move through a campaign, and why prices are highest when manipulators sell.'),
            ('arxiv', 'La Morgia, Mei, Sassi & Stefa', 2020, 'Pump and Dumps in the Bitcoin Era: Real Time Detection of Cryptocurrency Market Manipulations', 'https://arxiv.org/abs/2005.06610',
             'Analysis of Internet pump-and-dump groups in cryptocurrency markets, where low liquidity makes coins prone to manipulation, with a real-time detector.'),
            ('official', 'U.S. Supreme Court', 1963, 'Securities and Exchange Commission v. Capital Gains Research Bureau, Inc.', 'https://www.law.cornell.edu/supremecourt/text/375/180',
             'Defines scalping, holds that it operates as a fraud on clients, and that the SEC may obtain an injunction requiring full disclosure of the practice.'),
            ('official', 'U.S. Congress', 1933, 'Securities Act of 1933, section 17: fraudulent interstate transactions (15 U.S.C. 77q)', 'https://www.law.cornell.edu/uscode/text/15/77q',
             'Statute text of the anti-touting provision in subsection (b): disclosure of paid promotion, and what it does not cover.'),
        ],
    ),
    "12.8": (
        r"""Two public data sets feed the lesson's review, and neither suffices alone. Under Rule 605, market centers and brokers must publish monthly statistics on market and marketable limit orders by size, including price improvement, effective and realised spreads and execution speed. The rule itself warns that these figures alone are not a reliable basis for judging whether a broker obtained the most favourable terms reasonably available. Under Rule 606, brokers must publish quarterly, for their top venues and by order type, the net payment for order flow, fees and rebates, and must describe terms that may influence routing. One set shows outcomes, the other incentives.

Battalio and co-authors show why they belong together. They identified retail brokers that seemingly route to maximise order-flow payments, selling market orders and sending limit orders to venues paying large rebates, and found that limit-order execution quality was negatively related to the rebate or fee level. Çetin and Danilova's model, in which liquidity providers are risk averse, reaches a different conclusion for marketable orders: routing them to wholesalers is preferred by all retail traders. Our inference: a payment is neither neutral nor uniformly harmful, so the review must be split by order type.

Our second inference concerns the lesson's formula, which as written costs only filled shares. A venue that fills a limit order only when the price runs away can look cheap on its fills, so record the unfilled quantity too.

Exercise: under Rule 606(b), ask your broker for the venues that handled your orders in the past six months, then compute the lesson's shortfall by venue and order type.""",
        [
            ('paper', 'Battalio, Corwin & Jennings', 2016, 'Can Brokers Have It All? On the Relation between Make-Take Fees and Limit Order Execution Quality', 'https://doi.org/10.1111/jofi.12422',
             'Evidence that brokers whose routing seems to maximise order-flow payments and liquidity rebates deliver worse limit-order execution quality as rebates rise.'),
            ('arxiv', 'Çetin & Danilova', 2022, 'Order routing and market quality: Who benefits from internalisation?', 'https://arxiv.org/abs/2212.07827',
             'Theoretical models of internalisation versus open-exchange routing; a result that depends on risk-averse liquidity providers and concerns marketable orders only.'),
            ('official', 'U.S. SEC', 2024, 'Rule 605 of Regulation NMS: disclosure of order execution information (17 CFR 242.605)', 'https://www.ecfr.gov/current/title-17/chapter-II/part-242/section-242.605',
             "Current rule text: the monthly execution-quality statistics, their breakdown by order type and size, and the rule's own caution about what they cannot show."),
            ('official', 'U.S. SEC', 2018, 'Rule 606 of Regulation NMS: disclosure of order routing information (17 CFR 242.606)', 'https://www.ecfr.gov/current/title-17/chapter-II/part-242/section-242.606',
             "Current rule text: quarterly routing reports with payment for order flow, fees and rebates by venue and order type, and a customer's right to a six-month routing history."),
        ],
    ),
    "12.9": (
        r"""The lesson's gap is written into the rules. Rule 15c3-5 requires brokers with market access to reject erroneous orders that exceed price or size parameters on an order-by-order basis or over a short period of time, or that indicate duplicative orders, and the firm's chief executive must certify the controls annually. EU Delegated Regulation 2017/589 goes further. Its Article 15 adds maximum message limits and repeated-execution throttles that disable the trading system after a pre-set number of repeats until a designated staff member re-enables it. Our reading: 23 identical orders of Rp90 million are what a throttle or message cap exists to stop before the loss limit does.

Accountability is built in. Article 5 has a person designated by senior management authorise each deployment or substantial update, and Article 12 requires the ability to cancel all unexecuted orders immediately and to identify the algorithm and the trader, desk or client behind each order.

Deployment risk is real: Knight Capital reported in August 2012 that its installation of trading software led it to send numerous erroneous orders, at a realised pre-tax loss of approximately $440 million; that was the firm's early figure, and the SEC's later order, cited in this lesson's case, puts the loss at more than $460 million.

Rejection rather than alerting matters because of speed. Johnson and co-authors found 18,520 ultrafast price extremes between 2006 and 2011 in a sub-second regime where humans cannot respond quickly enough. Our inference: a control that waits for someone to read an alert acts after the damage.

Exercise: add a messages-per-second cap and a repeat throttle to the lesson's desk, name who may re-enable it, and replay the defective release to see where it now stops.""",
        [
            ('official', 'U.S. SEC', 2010, 'Risk management controls for brokers or dealers with market access (17 CFR 240.15c3-5)', 'https://www.ecfr.gov/current/title-17/chapter-II/part-240/section-240.15c3-5',
             'Current rule text: aggregate credit and capital thresholds, rejection of erroneous orders by price or size over a short period, duplicative-order checks, and annual chief executive certification.'),
            ('official', 'European Commission', 2016, 'Commission Delegated Regulation (EU) 2017/589 on organisational requirements for algorithmic trading', 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32017R0589',
             'Pre-trade controls including message limits and execution throttles, kill functionality, order-level attribution to an algorithm and trader, and designated authorisation of deployments.'),
            ('official', 'U.S. SEC', 2013, 'Regulation Systems Compliance and Integrity', 'https://www.federalregister.gov/documents/2013/03/25/2013-05888/regulation-systems-compliance-and-integrity',
             "Proposing release that quotes Knight Capital's own report that a trading-software installation produced erroneous orders and a loss of about $440 million."),
            ('arxiv', 'Johnson et al.', 2012, 'Financial black swans driven by ultrafast machine ecology', 'https://arxiv.org/abs/1202.1448',
             'Counts sub-second extreme price events and argues that in this regime humans cannot respond or intervene quickly enough.'),
        ],
    ),
    "12.10": (
        r"""The lesson's arithmetic is a small version of a field-wide problem. Harvey and co-authors argue that after hundreds of papers and factors the usual significance criteria no longer make sense. Their cutoffs run from the first tests in 1967, and they conclude that a new factor now needs a t-statistic above 3.0 and that most claimed findings in financial economics are likely false. For scale, the lesson's adjusted threshold of 0.00125 matches a normal critical value of about 3.23 (two-sided), and its reported p = 0.01 only about 2.58. That comparison is ours; their method is not a plain division by the trial count.

Bailey and co-authors add the length of the sample. For Sharpe ratios, with five years of data no more than 45 independent configurations should be tried, or an in-sample Sharpe ratio of 1 is almost guaranteed while the expected out-of-sample ratio is zero; on two years, seven independent trials suffice. Holding these limits against the lesson's 40 p-value tests is an inference, since the statistics differ, but it shows that 40 trials can be tolerable on one history and reckless on another.

They also doubt a holdout when the researcher has seen the full sample anyway, and point to Leinweber and Sisk, who announced a strategy and said they would publish results six months later, on data not yet observed.

Trial counts do not catch leakage: a 2026 preprint by Gençay reports a deliberately leaky oracle with a Sharpe ratio of 35 that passed deflated-Sharpe and overfitting-probability tests completely.

Exercise: list every configuration, universe and date window behind your best backtest, divide 0.05 by that count, and compare your history length with the five-year, 45-trial limit.""",
        [
            ('paper', 'Harvey, Liu & Zhu', 2015, '… and the Cross-Section of Expected Returns', 'https://doi.org/10.1093/rfs/hhv059',
             'Field-wide multiple-testing study of the factor literature: historical significance cutoffs since 1967, a t-statistic hurdle above 3.0 for a new factor, and the conclusion that most claimed findings are likely false.'),
            ('paper', 'Bailey, Borwein, López de Prado & Zhu', 2014, 'Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance', 'https://doi.org/10.1090/noti1105',
             "Shows how few trials produce a spuriously high Sharpe ratio, gives minimum backtest lengths for a given number of trials, and discusses holdout credibility. Figures here are read from the authors' hosted preprint."),
            ('arxiv', 'Gençay', 2026, 'What survives honest evaluation? Leakage-safe, search-aware assessment of LLM-driven trading strategy discovery', 'https://arxiv.org/abs/2608.27734',
             'Recent preprint that records every strategy evaluation, deflates results by the trial count, and shows that this correction does not detect look-ahead leakage.'),
        ],
    ),
    "12.11": (
        r"""The lesson's two tests have enforcement and measurement behind them. On permission, the SEC's September 2021 order against App Annie was its first action charging an alternative data provider with securities fraud. The order finds that companies shared confidential app data on a promise that it would be aggregated and anonymized, yet from late 2014 through mid-2018 App Annie used non-aggregated, non-anonymized data to alter its model-generated estimates and misdescribed this to the trading firms buying them. App Annie and its founder settled without admitting or denying the findings, with penalties of $10 million and $300,000. The order is against the seller and its founder. Our inference for a buyer: a licence is only as sound as the consents behind it, so record how each field was sourced.

On timing, Diebold and Rudebusch tested the composite index of leading indicators on the provisional and partially revised figures actually available at the time, with recursive out-of-sample forecasts, and found a substantial deterioration of forecasting performance. Our inference, against the lesson's 17 basis points: revisions fold in information that arrived later, so a signal can seem to work partly because of them.

The same trap now sits inside models. Glasserman and Lin point out that a backtest of a language-model strategy is biased if the model's training period overlaps the test period. In their headline-sentiment study, removing company identifiers improved in-sample results, which they read as a distraction effect larger than look-ahead bias; out-of-sample, look-ahead was not a concern.

Exercise: run one rule on the first-release vintage and on the latest revision. The gap shows how much of the result rests on information that revisions added later.""",
        [
            ('official', 'U.S. SEC', 2021, 'SEC Charges App Annie and its Founder with Securities Fraud', 'https://www.sec.gov/newsroom/press-releases/2021-176',
             'Press release on the first SEC enforcement action charging an alternative data provider with securities fraud: what the order finds about consents, misuse of confidential data and the penalties.'),
            ('paper', 'Diebold & Rudebusch', 1991, 'Forecasting Output with the Composite Leading Index: A Real-Time Analysis', 'https://doi.org/10.1080/01621459.1991.10475085',
             'A forecasting test redone on the provisional and partially revised data available at the time, showing a substantial loss of performance.'),
            ('arxiv', 'Glasserman & Lin', 2023, 'Assessing Look-Ahead Bias in Stock Return Predictions Generated By GPT Sentiment Analysis', 'https://arxiv.org/abs/2309.17322',
             "Shows that a language model's training window is an as-of date too: backtests that overlap it are biased, and anonymizing headlines is one remedy."),
        ],
    ),
    "12.12": (
        r"""Much of the lesson is written into the SEC's Marketing Rule for registered advisers' advertisements. Gross performance may be shown only with net performance of at least equal prominence, over the same period and with the same methodology. Results for a portfolio or composite (private funds excepted) need one-, five- and ten-year figures, equally prominent and ending no earlier than the latest calendar year-end; a seven-year-old portfolio shows one, five and seven, and the release bars highlighting whichever period looks best. Related performance must include all related portfolios unless excluding some leaves the results no higher in any material way. Hypothetical performance, defined to include backtests, needs policies ensuring relevance to the audience plus disclosure of criteria, assumptions, risks and limitations, because such figures can be readily optimized through hindsight.

Omission biases records too. Carhart and co-authors demonstrated theoretically that when survival depends on multiyear performance, survivorship bias typically grows with sample length, and in mutual fund data found the annual bias rising from 0.07% for 1-year samples to 1% beyond 15 years. Evans found incubated funds beat non-incubated funds by 3.5% risk-adjusted, but the edge vanished once they opened to the public, biasing returns unless fund-age or ticker-creation-date filters were applied. Our inference: start a record when the product became publicly investable. A 2026 arXiv preprint on India's NIFTY Smallcap 250, using a reconstructed membership list estimated 85-90% accurate historically, reports that testing only current members overstated annual returns by 4.94 percentage points.

Exercise: for the lesson's twelve-month record, list every account or fund ever run under the strategy and the date each became publicly investable; recompute the headline over all of them and see whether the 10% survives.""",
        [
            ('official', 'U.S. SEC', 2021, 'Investment Adviser Marketing', 'https://www.federalregister.gov/documents/2021/03/05/2020-28868/investment-adviser-marketing',
             'Adopting release and rule text for the Marketing Rule: net-versus-gross, the one-, five- and ten-year periods, and the hindsight rationale for restricting hypothetical and backtested performance.'),
            ('paper', 'Carhart, Carpenter, Lynch & Musto', 2002, 'Mutual Fund Survivorship', 'https://doi.org/10.1093/rfs/15.5.1439',
             'Shows theoretically and in fund data that survivorship bias in average performance grows with sample length, so dropped funds matter more in long records.'),
            ('paper', 'Evans', 2010, 'Mutual Fund Incubation', 'https://doi.org/10.1111/j.1540-6261.2010.01579.x',
             'Funds privately incubated outperform, then lose the edge when opened to the public, which biases returns unless the incubation period is filtered out.'),
            ('arxiv', 'Ranse', 2026, "Survivorship Bias in Emerging Market Small-Cap Indices: Evidence from India's NIFTY Smallcap 250", 'https://arxiv.org/abs/2603.19380',
             'A single-author preprint that sizes the overstatement from backtesting only current index members against all historical members.'),
        ],
    ),
    "12.13": (
        r"""Regulators already treat the lesson's two inputs as separate. Regulation Best Interest lists investment time horizon, liquidity needs and risk tolerance as distinct parts of a retail customer's investment profile. ESMA's MiFID II suitability guidelines file ability to bear losses under financial situation and risk tolerance under investment objectives, and want self-assessment counterbalanced by objective criteria: instead of asking whether clients believe they have enough funds, collect facts such as regular income and outstanding liabilities; instead of asking whether a client feels comfortable with risk, ask what level of loss over a given period the client would accept. The guidelines also name a future financial commitment, such as a property purchase or education fees, as relevant information, which is the lesson's dated obligation, and tell firms to resolve contradictions such as a prudent risk profile paired with ambitious objectives.

A recorded profile does not prove it was used. Foerster and co-authors, using Canadian household data, found that advisor fixed effects explained considerably more variation in portfolio risk than investor attributes including risk tolerance, age, horizon and sophistication; advised portfolios cost 2.5% a year, or 1.5% more than life cycle funds. Thompson and co-authors, in a 2021 preprint, test alignment by measuring the Know Your Client risk profile and the portfolio's risk on one value-at-risk scale, across over 50,000 accounts, 27,000 clients and 300 advisors.

Exercise: ask the lesson's client what loss over eighteen months they would accept, divide it by the assumed 30% fall, and compare the result with Rp180 million. The smaller figure is the risky allocation.""",
        [
            ('official', 'ESMA', 2023, 'Guidelines on certain aspects of the MiFID II suitability requirements', 'https://www.esma.europa.eu/sites/default/files/2023-04/ESMA35-43-3172_Guidelines_on_certain_aspects_of_the_MiFID_II_suitability_requirements.pdf',
             'EU supervisory guidance that separates ability to bear losses from risk tolerance and prescribes objective, factual questions in place of self-assessment.'),
            ('official', 'U.S. SEC', 2019, 'Regulation Best Interest (17 CFR 240.15l-1)', 'https://www.ecfr.gov/current/title-17/chapter-II/part-240/section-240.15l-1',
             'Rule text defining the retail customer investment profile, with time horizon, liquidity needs and risk tolerance listed as separate items.'),
            ('paper', 'Foerster, Linnainmaa, Melzer & Previtero', 2017, 'Retail Financial Advice: Does One Size Fit All?', 'https://doi.org/10.1111/jofi.12514',
             "Household data showing that the advisor, more than the client's recorded attributes, explains portfolio risk, and that this advice carried a higher cost."),
            ('arxiv', 'Thompson et al.', 2021, 'Measuring Financial Advice: aligning client elicited and revealed risk', 'https://arxiv.org/abs/2105.11892',
             "Puts a client's stated risk profile and the portfolio actually held on the same value-at-risk scale, using data from a Canadian dealership."),
        ],
    ),
    "12.14": (
        r"""Each of the lesson's two tests has a documented failure. On authority, Greshake and co-authors argue that LLM-integrated applications blur the line between data and instructions: an attacker injects prompts into data likely to be retrieved, and they demonstrated the attack on real systems, including Bing's GPT-4 powered Chat and code-completion engines, noting that effective mitigations were lacking. The lesson's "release funds" line inside a document is that attack in miniature. Our inference: whatever reads a file must not be the party that approves a payment, and approval must travel by a channel the file cannot influence. People face the same problem. The FBI's 2025 report counts 24,768 business email compromise complaints with more than $3 billion in reported losses, and notes that chat generators can quickly produce official-sounding emails mimicking a CEO while voice cloning can be used to request a wire payment. Our inference: tone, polish and apparent seniority establish nothing, so confirmation has to come from outside the message.

On arithmetic, Bartoletti and co-authors survey Ponzi schemes on Ethereum, where users are repaid only with new users' investments, so the scheme implodes soon after users stop joining. Their abstract calls such contracts "trustworthy" frauds: guaranteed to execute correctly, yet users still lose money. Checking that a promise will be executed is therefore a different test from checking that it can be met; in the lesson's scheme, the Rp420 million shortfall is the part only new deposits can fill.

Exercise: for the last payment instruction you handled, write down the channel that carried it and the separate channel that confirmed it. If they are the same, treat the instruction as unverified.""",
        [
            ('arxiv', 'Greshake et al.', 2023, "Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection", 'https://arxiv.org/abs/2302.12173',
             'Shows that instructions hidden in retrieved data can steer an LLM-integrated application, the automated version of a document that gives orders to whoever processes it.'),
            ('arxiv', 'Bartoletti, Carta, Cimoli & Saia', 2017, 'Dissecting Ponzi schemes on Ethereum: identification, analysis, and impact', 'https://arxiv.org/abs/1703.03779',
             'Survey of Ponzi schemes on Ethereum, where the payout rule is code that executes as written yet the scheme still depends on new users joining.'),
            ('official', 'FBI · Internet Crime Complaint Center', 2025, '2025 IC3 Annual Report', 'https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf',
             "Complaint counts and losses for business email compromise, plus the FBI's note on AI-written emails and cloned voices that mimic an executive."),
        ],
    ),
    "12.15": (
        r"""A dated written report has legal weight as well as practical value. SEC Rule 21F-4(b)(7) treats a report made to an entity's internal whistleblower, legal or compliance procedures as made on its own date, for award purposes, if the same information reaches the Commission within 120 days, and it puts the burden on the claimant to establish that effective date. The lesson's four months of silence is roughly that window: a dated summary lets the analyst show when the clock started, while a recollection of a conversation does not.

Internal reporting is not the whole picture. In Digital Realty Trust v. Somers the Supreme Court held that Dodd-Frank's anti-retaliation provision does not extend to a person who has not reported to the SEC, while describing Sarbanes-Oxley as covering reports to an internal supervisor. Our inference: escalate inside first, but check which protection each channel actually carries.

Insiders matter. Dyck, Morse and Zingales studied all reported fraud cases in large U.S. companies between 1996 and 2004 and found that detection did not rely on investors, the SEC or auditors but on employees, media and industry regulators; monetary incentives helped explain employee whistleblowing, while reputational incentives were generally weak. Ahmed-Rengers and co-authors, building on cases where whistleblowers were discovered, conclude that a whistleblower is often at the mercy of others' motivations and abilities, and that the main constraints are often institutional.

Exercise: for a concern you have raised or might raise, write the date, the recipient and where the retained copy sits; then add the date 120 days later and decide in advance what you would do if the response were still silence.""",
        [
            ('official', 'U.S. SEC', 2011, 'Other definitions (17 CFR 240.21F-4), SEC whistleblower rules', 'https://www.ecfr.gov/current/title-17/chapter-II/part-240/section-240.21F-4',
             'Rule text: an internal report counts as made on its own date if the same information goes to the SEC within 120 days, and the claimant must establish that date.'),
            ('official', 'U.S. Supreme Court', 2018, 'Digital Realty Trust, Inc. v. Somers', 'https://www.law.cornell.edu/supremecourt/text/16-1276',
             "Holds that Dodd-Frank's anti-retaliation protection does not reach someone who reported only internally, and contrasts Sarbanes-Oxley's wider coverage."),
            ('paper', 'Dyck, Morse & Zingales', 2010, 'Who Blows the Whistle on Corporate Fraud?', 'https://doi.org/10.1111/j.1540-6261.2010.01614.x',
             'Study of reported fraud cases in large U.S. companies, showing that employees and other non-standard actors, not auditors or the SEC, drive detection.'),
            ('arxiv', 'Ahmed-Rengers et al.', 2020, 'Snitches Get Stitches: On The Difficulty of Whistleblowing', 'https://arxiv.org/abs/2006.14407',
             'Security-engineering view of cases where whistleblowers were discovered, concluding that their position depends on others and that constraints are mostly institutional.'),
        ],
    ),
    "12.16": (
        r"""Three strands of research bear on the lesson's charter. On form, Sheeran and co-authors' meta-analysis of 642 independent tests found implementation intentions effective for cognitive, affective and behavioural outcomes, with effect sizes from 0.27 to 0.66, and larger when plans were contingent (if-then), when people were highly motivated, and when plans were rehearsed. The lesson's rule has that shape: if a position exceeds Rp20 million, then it is cut back to the limit. Our inference: rehearsal is the case for a scheduled review, and an aspiration such as "manage risk carefully" gives no cue to act on.

On judging outcomes, Baron and Hershey had subjects rate others' decisions, understanding that they held all the decision maker's relevant information, and found the thinking rated better, or the decision maker more competent, when the outcome was favourable, although those asked said outcomes should not count. This is the bias the lesson guards against with "a profitable breach is still a breach": the Rp26 million position that paid, and a loss taken while following the rules, will both read as verdicts on the rule unless the review uses what was known at the time.

On commitment, Hu and co-authors study a gambler with prospect-theory preferences who must decide when to stop. They find the problem time-inconsistent, compare precommitted with naive stopping strategies, and report that it is prevalent for a naive gambler never to stop a loss. A casino model is not a trading desk; our inference is only that a stop fixed in advance and one re-decided in the moment can differ.

Exercise: rewrite one charter rule as "if cue, then response" and record the date on which you will review it.""",
        [
            ('paper', 'Sheeran, Listrom & Gollwitzer', 2024, 'The when and how of planning: Meta-analysis of the scope and components of implementation intentions in 642 tests', 'https://doi.org/10.1080/10463283.2024.2334563',
             'Meta-analysis showing that if-then plans, strong motivation and rehearsal make implementation intentions work better, which bears on how a charter rule should be worded and reviewed.'),
            ('paper', 'Baron & Hershey', 1988, 'Outcome bias in decision evaluation', 'https://doi.org/10.1037/0022-3514.54.4.569',
             'Experiments showing that people judge the quality of a decision by its outcome even when they say they should not, the bias a charter review has to guard against.'),
            ('arxiv', 'Hu, Obłój & Zhou', 2021, 'When to Quit Gambling, if You Must!', 'https://arxiv.org/abs/2102.03157',
             'Model of a gambler deciding when to stop, contrasting precommitted with naive stopping strategies, and finding that a naive gambler often never stops a loss.'),
        ],
    ),
}
