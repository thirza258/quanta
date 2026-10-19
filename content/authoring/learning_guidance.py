"""Original teaching introductions and plain-language support for the course builders.

Keep these explanations separate from assessment keys and runnable worksheets.
The catalog generator applies them once, after assembling the complete curriculum.
"""

import re

from lab_workshop import COURSE_GUIDE as LAB_GUIDE
from simulator_workshop import COURSE_GUIDE as SIMULATOR_GUIDE

COURSE_GUIDES = {
    "simulator-workshop": SIMULATOR_GUIDE,
    "lab-workshop": LAB_GUIDE,
    "trading-fundamentals": (
        "Your starting point for financial markets: master shares, market mechanics, order execution, returns, business statements, and risk management.",
        "Start here if financial news, ticker charts, and investing terminology feel unfamiliar or overwhelming. This course is designed to guide you step-by-step from foundational principles to practical market decisions—with zero prior finance, math, or programming experience required.\n\nYou will follow an investment decision from the ground up across four structured units:\n• Unit 1 (Ownership & Financial Foundations): Distinguish saving, investing, and trading, and discover what owning a share of common equity really means.\n• Unit 2 (Market Structure & Order Mechanics): Trace how orders route through brokers and exchanges to become trades, read live bid-ask quotes, and choose the right order instruction (market, limit, stop).\n• Unit 3 (Returns, Costs & Financial Analysis): Calculate true net returns after all fees and dividends, understand how compounding and losses work, and learn how to read core financial statements to evaluate a business before buying.\n• Unit 4 (Risk Controls & Trading Plan Design): Protect your capital using disciplined position sizing and diversification, avoid common behavioral traps, and draft your very first structured paper-trading plan.\n\nEvery lesson features step-by-step worked examples using simple numbers and relatable everyday analogies. Work through the numbers with a calculator or on paper, test your understanding with interactive practice questions, and review key terms in each lesson's glossary. Interactive Python code snippets are provided for hands-on experimentation, but you can complete the entire course without writing code.",
    ),
    "trading-ethics": (
        "Master duties of loyalty, resolve conflicts of interest, protect market integrity against manipulation, and build your own auditable personal trading charter.",
        "The most difficult challenges in financial markets are rarely pure mathematical calculations. They are high-pressure moments where personal profit and ethical duty pull in opposite directions—and where market noise tempts you to compromise your principles. This course prepares you in advance, establishing rigorous ethical frameworks so your choices are already settled before temptation arises.\n\nAcross four structured units, you will examine real-world market dilemmas through primary regulatory standards (CFA Institute, SEC, FINRA, ESMA) and concrete arithmetic:\n• Unit 1 (Duty, conflict and disclosure): Establish agency relationships and the fiduciary duty of loyalty, expose hidden trailer fees and calculate total cost of ownership, disclose material personal conflicts prominently, and enforce strict client trading priority over personal accounts.\n• Unit 2 (Market integrity): Master the two-prong test for material non-public information (MNPI), distinguish legitimate mosaic research from insider trading, identify manipulative quoting patterns (spoofing, layering, wash trading), expose predatory pump-and-dump exit liquidity math, and measure best execution using implementation shortfall.\n• Unit 3 (Conduct in automated and quantitative work): Enforce human accountability for algorithmic systems, configure pre-trade risk controls and emergency kill switches, eliminate p-hacking and multiple-testing bias in backtests, ensure dataset provenance and point-in-time vintage hygiene, and present GIPS-compliant performance records net of all fees.\n• Unit 4 (Care, refusal and record): Separate objective risk capacity from emotional risk tolerance, detect Ponzi structures and refuse unauthorized instructions, build auditable written escalation trails, and draft your own operational, checkable trading charter.\n\nEvery scenario, company, and rupiah amount in this course is invented to illustrate real regulatory standards and quantitative dilemmas. This course is for educational purposes and does not constitute legal or compliance advice; regulatory obligations depend on your specific jurisdiction, license, and role. By the end, you will synthesize your learning into a personal written charter of auditable rules that you can check after every trading day.",
    ),
    "intelligent-investor": (
        "Build patient investing habits, understand the risks you can afford, and write a practical investment plan inspired by The Intelligent Investor.",
        "Before choosing individual stocks, it helps to understand the person making the decisions: you. This course connects investing habits with practical choices about goals, available cash, diversification, fees, and how to respond when prices move. A careful investor needs a process they can maintain through uncertainty.\n\nEach lesson connects one idea from the book's themes to an original everyday example. First explain the choice in ordinary language, then work through the calculation, and finally add a decision rule to your My notebook page. For example, a discussion of losses should lead you to explain which money you can leave invested and which money you may need soon. Build the plan gradually; you do not need to decide everything in the first lesson.",
    ),
    "security-analysis": (
        "Learn to read a company's accounts, estimate a range of values, and judge whether its securities offer enough protection for the price.",
        "A share price tells you what someone is asking. It does not tell you what the business can earn or what would remain for investors if it ran into trouble. This course teaches you to build that picture from evidence, following Graham and Dodd's approach to security analysis.\n\nStart by identifying the investment you are examining: a lender's claim, a preferred share, or common ownership. Then look at the cash, earnings, assets, and obligations that support it. The worked examples show how changing an assumption changes an estimate. Keep a separate note of facts, assumptions, and unanswered questions. By the end, you will bring those notes together in an investment committee case and explain why the evidence supports your conclusion.",
    ),
    "news-to-markets": (
        "Turn a financial headline into a clear research question. Trace its effect on a company's accounts, estimated value, and possible market reaction.",
        "A headline can describe an important event without telling you what it means for a particular company. This course slows down the reasoning between reading the news and forming an investment view. You will check the source, understand the size and timing of the change, and follow its possible effects on sales, costs, cash flow, and value.\n\nWork through each case in three passes. First write what the source actually establishes. Next calculate the possible business effect using clearly stated assumptions. Finally explain what remains uncertain and what investors may already have expected. Indonesian inflation, interest-rate, and rupiah examples help you practise the same method in a familiar setting. Keep your evidence and your interpretation in separate parts of the research memo.",
    ),
    "statistical-foundations": (
        "Build the maths needed for investment research, from cash flows and probability to regression, risk measurement, and testing a strategy.",
        "Investment research often uses numbers to answer questions that remain uncertain. How much is a future payment worth today? How much can a return vary? Does a pattern in a sample give us a good reason to expect it again? This course develops the tools for answering those questions one step at a time.\n\nBefore using an equation, identify the question and write what each input measures. Follow the small worked example, check its units, and explain the result in a sentence. Later units build on those habits when you fit models and evaluate strategies. If a result looks precise, ask which assumptions produced that precision. The optional worksheets let you change one input and see why the answer changes.",
    ),
    "econometrics": (
        "Use data to study returns, market relationships, and changing risk. Learn to fit models, check their assumptions, and explain what the results support.",
        "Econometrics uses statistical models to study economic and financial data. The difficult part is often choosing a question the data can answer. A relationship that describes past returns may be useful for one purpose and inadequate for predicting the future or explaining cause and effect.\n\nYou will move from a written research question to a dated dataset, a fitted model, and a careful interpretation. Reproduce the simple calculations before using the larger project. Then inspect what the model misses: unusual observations, changing volatility, related errors over time, or missing influences. Your final research file should let another person follow your choices and understand both the result and its limits.",
    ),
    "strategy-lab": (
        "Turn an investment idea into testable rules. Build a portfolio, account for trading costs, and examine whether the results support your idea.",
        "An investment idea becomes a strategy only when another person could follow its rules and reach the same decisions. This course takes you through that translation: define the idea, choose data that was available at the time, create a signal, decide what to hold, and record how trades change the portfolio.\n\nFor each strategy family, start with the reason it might work and the reason it might fail. Follow the worked calculation, then use the project to inspect individual holdings, trades, and costs. Compare the result with a simple alternative over the same period. A useful research result may be a clear reason to reject an idea; the goal is to reach a conclusion you can explain and reproduce.",
    ),
    "stock-bots": (
        "Build a paper-trading bot step by step, from signals and order handling to risk controls, recovery, and supervised AI research tools.",
        "A trading bot does more than produce buy and sell signals. It must know what information it has received, which orders are still active, how much money is committed, and what to do when something fails. This course teaches you to make those decisions explicit before automating them.\n\nBegin with a small paper-trading system and follow one event all the way through it: new data, a signal, a risk check, an order, and a recorded fill. Later lessons add multiple assets, machine-learning predictions, AI research, and recovery after interruptions. At each stage, test ordinary behavior and failure cases. Keep a written explanation of what the system is allowed to do and how you know it obeys those limits.",
    ),
    "c-hpc-trading": (
        "Rebuild a trading research engine in C. Learn memory management, reliable calculations, performance measurement, and parallel experiments.",
        "Once a research program works, the next question may be how to run larger experiments efficiently. This course introduces C through that practical problem. You will learn how a program stores data, owns memory, processes events, and measures its own performance.\n\nStart with a correct sequential version and keep its results as a reference. Compile each worksheet, predict its output, and explain any difference before changing the implementation. Later, compare faster versions using the same inputs and checks. Separate the speed of one part of the program from the time taken by the whole job. The aim is a faster program whose results and behavior you can still account for.",
    ),
    "web3": (
        "Understand hashes, signatures, and blockchains. Build a local coin and token, then examine their supply rules, permissions, and trading mechanics.",
        "A blockchain is easier to understand when you can inspect the steps that change its records. This course starts with bytes, hashes, and digital signatures, then uses those building blocks to create and validate transactions in small local projects. You will see how ownership, balances, and supply rules become checks in code.\n\nWork through the toy examples before moving to the complete coin and token projects. For each operation, write who is allowed to request it, what must be true first, and which balances or records should change. Later lessons connect those rules to liquidity pools, fees, and failure scenarios. You can do the exercises locally without connecting a wallet or using real funds.",
    ),
    "stock-machine-learning": (
        "Build and evaluate a stock-prediction workflow, from cleaning data and creating features to training, testing, and monitoring a model.",
        "A machine-learning model learns patterns from examples. In stock research, the examples must also respect time: information used to make a prediction must have been available before the outcome. A convincing training score is only one small part of a useful research process.\n\nYou will follow the full workflow in order: define the prediction, clean the data, build inputs and targets, separate training from evaluation, fit a simple baseline, and compare alternatives. The worked examples explain what each step contributes. When a model improves, investigate why. When you save it, save the preprocessing and data assumptions too, so that a new prediction uses the same method you evaluated.",
    ),
    "algorithm-evaluation": (
        "Evaluate a completed trading algorithm and write a clear report covering returns, costs, risk, benchmarks, uncertainty, and computing performance.",
        "A result is useful only when a reader can understand how it was produced and what it supports. This final course helps you turn a completed algorithm project into a report that another person can check. Begin with the question, the data period, the comparison, and the rules you promised to use.\n\nNext, reconcile the exported cash and portfolio values before calculating performance. Work through returns, drawdowns, costs, and uncertainty, then choose tables and charts that make those findings clear. Finish by explaining the strongest evidence, the main weaknesses, and what further work is needed. Treat the report as an argument supported by records, rather than a collection of attractive numbers.",
    ),
}

# The first lesson in each unit supplies the conceptual bridge to its new topic.
# Beginner lessons each introduce a distinct topic, so each has its own bridge.
UNIT_INTRODUCTIONS = {
    "0.1": "Before looking at charts or numbers, think of money as having a specific job to do. Some money must be preserved for near-term expenses or emergencies, while other money can be invested for goals years away. Saving, investing, and trading are three fundamentally different ways of putting capital to work: saving prioritizes capital preservation; investing focuses on long-term wealth compounding through business growth; trading seeks to capture short-term price fluctuations. Before calculating any return, start by understanding your financial goal, your timeframe, and the uncertainty involved.",
    "0.2": "Imagine dividing a growing business into many equal ownership slices—each slice is a share of stock. The number of shares you hold divided by the total shares outstanding determines your exact ownership percentage. Crucially, the price of one individual share is a completely separate question from what the entire company is worth. Keeping ownership fraction, individual share price, and total company market capitalization distinct will make all the concepts in this lesson intuitive and easy to follow.",
    "0.3": "Buying a share of stock is not like buying an item from a store, where your money goes directly to the manufacturer. When you trade in stock markets, the company only receives funding once—during its primary-market offering when new shares are issued. After that, existing shares trade between investors on the secondary market. Your broker, the exchange, market makers, and clearinghouses coordinate behind the scenes to execute and settle each transaction. Follow where the money flows in this lesson to understand how modern markets actually function.",
    "0.4": "The price you see on a financial chart is simply a historical record of the most recent trade—it is not a guaranteed menu price for your next transaction. To understand what price you will actually pay or receive right now, you need to look at current buyers (the Bid) and current sellers (the Ask), along with the quantity available at each price level. This lesson explains how bid-ask quotes work, how to read candlestick bars (OHLCV), and how to select the right order instruction for your goals.",
    "0.5": "A stock rising from $100 to $110 looks like a straightforward 10% gain, but your true financial outcome depends on what actually enters and leaves your account. Brokerage commissions, exchange fees, bid-ask spreads, and cash dividends all impact the bottom line. Furthermore, sequential investment returns multiply through time rather than simply adding up—meaning that losing 10% after gaining 10% leaves you with less money than you started with. This lesson walks you through true net return accounting and the essential mathematics of compounding.",
    "0.6": "Before buying shares in any company, ask yourself a foundational question: How does this business actually make money? Does it sell products for more than it costs to produce them, and does it actually collect cash from its customers? Financial statements provide the answers. The Income Statement acts as a movie of operating profitability over time, the Balance Sheet gives a point-in-time snapshot of assets and debts, and the Cash Flow Statement acts as the ultimate reality check on cash in the bank.",
    "0.7": "In financial textbooks, risk is often defined as price volatility. In the real world, however, true risk is the danger of permanent loss of capital that you cannot afford. Position sizing answers: 'Given my account size and where I plan to exit if my idea is wrong, exactly how many shares should I buy?' Diversification asks: 'If one investment runs into trouble, will my other assets protect me, or will they all crash together?' This lesson teaches you how to size positions systematically and plan for market gaps before committing capital.",
    "0.8": "You have now mastered the foundational vocabulary of stocks, markets, quotes, returns, financial statements, and risk management. The final step is uniting these tools into a structured, testable paper-trading plan. A written plan acts as an objective pre-commitment contract with yourself: it defines your thesis, order instructions, stop-loss, and invalidating conditions before market emotions take over. This lesson guides you through drafting your first plan and choosing your next advanced course.",
    "11.1": "Being an intelligent investor does not mean predicting every price movement. It means making decisions you can explain and managing the emotions that might pull you away from your plan. Begin with a familiar situation: two people make money decisions and receive different outcomes. We need to examine their reasons and circumstances before deciding which process was better.",
    "11.5": "A portfolio should serve a person's needs. Start this unit by separating upcoming spending from longer-term goals and considering how a loss would affect each one. Willingness to take risk describes how you feel; capacity to take risk depends on what your finances can withstand. These questions give diversification and a margin of safety a practical purpose.",
    "11.9": "Choosing a product is easier after you have decided what role it should play. An allocation policy describes how the portfolio divides its money and why that division suits the goal. The lessons in this unit connect that policy to rebalancing, fund costs, and regular contributions. Write the policy in language you could still understand during a stressful market.",
    "11.13": "Independent judgment begins with checking a claim. A headline earnings number, a confident adviser, or a recent gain can all seem persuasive, but each needs supporting evidence. In this unit, practise asking where a number came from, who benefits from a recommendation, and what would change your view. Those questions lead into the final written investor policy.",
    "1.1": "A security gives its owner a particular claim on a business. A lender may be owed interest and repayment; a common shareholder receives what remains after other obligations. Before estimating value, identify the claim you are examining. Then separate the quoted market price from your own estimate of what supports that claim. The margin-of-safety calculation becomes meaningful only after that groundwork.",
    "1.2": "A promised payment matters only if the borrower can make it. When analysing a bond, begin with the cash and recurring earnings available to meet its obligations. Then consider what happens in a weak year and which creditors have priority. Coverage ratios help organize the evidence, but understanding the business and the contract explains why the ratios matter.",
    "1.11": "Some securities sit between ordinary debt and common shares. Their names can sound reassuring, but the contract determines what the holder can receive and when. In this unit, follow the payment rights first, then examine conversion or participation features. Separate a payment that has been promised from cash the holder can actually expect to collect.",
    "1.13": "Common shareholders own the part of the business left after other claims. Their outcome depends on more than this year's profit: management may pay a dividend, retain cash, issue new shares, or repurchase existing ones. Follow how each choice changes the resources of the business and the interest held by each shareholder. Keep total company amounts separate from per-share amounts.",
    "1.3": "Reported profit can include both ordinary business activity and unusual events. To estimate earning power, ask which parts are likely to continue. The process is called normalization. Work from the reported figure and record each adjustment so another reader can challenge it. Apply the same reasoning to unusual gains and unusual losses instead of selecting only favorable adjustments.",
    "1.4": "Assets listed in accounts are not necessarily worth their recorded amounts in a sale. Some cash may be needed to keep operating, some customers may not pay, and some inventory may sell at a discount. This unit asks what could remain for shareholders after those realities and all obligations are considered. Follow the order of deductions carefully.",
    "1.20": "A comparison is useful when the numbers describe similar things. Before comparing two companies, check their accounting choices, debts, share counts, and business conditions. A low ratio may reflect an attractive price, a weaker business, or a mismatched calculation. This unit turns separate valuation observations into a decision with explicit reasons and a plan for review.",
    "1.5": "The final unit connects the earlier business analysis to additional valuation tools and a complete case. A formula can help you explore an assumption, but it cannot choose that assumption for you. Keep the historical method, later extensions, and your own estimates clearly identified. Use more than one view of the business to investigate disagreement between results.",
    "8.1": "Before deciding whether news is good or bad for a stock, turn the headline into a question you can investigate. What was actually announced, how large is it relative to the business, and what must happen before it affects cash? The worked example separates a contract's headline value from the revenue it might contribute in one year.",
    "8.5": "Company news becomes easier to interpret when you can place it in the accounts. More sales may bring more profit, but they may also require additional inventory or leave customers owing more money. Follow the path from revenue to expenses, profit, and cash. Each step gives you a different question to ask of an earnings release.",
    "8.9": "Economic releases describe a particular quantity over a particular period. A price level, a monthly change, and an annual inflation rate answer different questions. Before interpreting the headline number, identify its units, comparison period, and revision status. Then consider how that change could reach a company through customers, costs, financing, or currency exposure.",
    "8.13": "The same event can help one business and hurt another. A rise in an input price may support a producer's sales while increasing a manufacturer's costs. Follow the chain of suppliers, customers, contracts, and timing before describing the effect. This unit develops that chain into a map you can use when comparing companies in an industry.",
    "8.17": "Once you understand a business effect, you still need to connect it to value and price. An improvement may already have been expected, and a price move may include other influences. Keep three questions separate: what changed in the business, what changed in your estimate, and what changed in the market. The lessons show how to examine each with an appropriate comparison.",
    "8.21": "A research memo should let someone retrace your reasoning. Begin with the question and the dated sources, then show the calculation, alternatives, and conclusion. In this unit, you will bring the earlier steps together and review where AI can assist. Every important claim should remain connected to evidence that a reader can inspect.",
    "2.1": "Receiving money today and receiving the same amount later are different because money available now can be put to use. Present value translates future payments into an equivalent amount today under a chosen rate. Begin by drawing a timeline. Place each payment on its own date before using the equation; the timing explains the exponent in the calculation.",
    "2.7": "Before fitting a model, make sure the observations mean what you think they mean. A price, a return, and a cash payment are different kinds of data. This unit asks you to label dates, units, and calculation choices, then inspect the distribution. Those simple habits prevent a sophisticated calculation from answering the wrong question.",
    "2.9": "New evidence should change a belief according to how informative it is. A warning that appears often in healthy businesses carries different information from one that is rare there. Start with the base rate, then compare how often the observation occurs under each possibility. The worked example shows how those pieces combine into an updated probability.",
    "2.2": "A probability distribution is a model of possible outcomes and how likely they are. It helps you calculate and simulate, but its shape also makes assumptions about extreme events and dependence. Begin by asking what quantity is being modelled. A distribution for prices is not automatically suitable for returns, losses, or the number of events.",
    "2.3": "A sample gives you evidence about a larger process, but another sample would usually produce a different estimate. This unit explains how to describe that variation. Start by distinguishing the spread of individual observations from uncertainty in their average. Then examine what changes when observations are related over time or selected in a biased way.",
    "2.4": "A research claim needs a comparison against what could happen without the effect you propose. Hypothesis testing makes that comparison explicit. Write the null hypothesis in words before calculating a statistic, then consider how many ideas you tried. A surprising result from one planned test and the best result from many searches carry different evidence.",
    "2.5": "Regression summarizes a relationship between variables. In a simple return model, it asks how an asset's return tends to vary with a market measure. First understand the axes and units, then interpret the slope and intercept. Only after that should you examine uncertainty or use the model to make a prediction.",
    "2.15": "Several influences can move together. Multiple regression tries to describe one relationship while accounting for other included variables. That makes the meaning of a coefficient conditional on the model. This unit asks you to inspect which variables are included, how much they overlap, and whether the available data can separate their effects reliably.",
    "2.17": "Financial observations arrive in time order, and yesterday's conditions may affect today's outcome. That dependence changes how you estimate uncertainty and evaluate a forecast. Begin by looking for persistence, trends, and changes in variability. A model that describes one period well may need different assumptions in another period.",
    "2.19": "Machine learning chooses a rule from examples to improve a stated objective. Before selecting a complex method, define what you want to predict and how success will be measured on later data. The central challenge is learning a pattern that remains useful beyond the examples used to fit it. This unit connects that challenge to validation and simple comparisons.",
    "2.21": "A research dataset is the result of many choices: sources, identifiers, timestamps, adjustments, and missing-value rules. Each choice can change what the model appears to know. Follow one observation from its source to its final model input. The aim is a record that another person could rebuild without accidentally adding information from the future.",
    "2.23": "An investment's return may reflect several common influences. Factor models organize those influences so you can describe exposure, attribution, and portfolio risk. Start with the meaning and units of each factor. Then ask which part of the return the model explains and which part remains unexplained under its assumptions.",
    "2.25": "A risk number summarizes a particular feature of possible losses. It cannot describe every way a portfolio could fail. Begin by identifying the time horizon and the part of the loss distribution being summarized. This unit combines tail measures with scenarios so that a compact statistic is accompanied by an explanation of the losses it may miss.",
    "2.27": "A backtest recreates decisions using historical or simulated observations. To be useful, it must respect the information and trading opportunities available at each point in time. Follow the decision clock before reading the final performance chart. Then inspect costs, comparisons, and the record of earlier trials that led you to the chosen strategy.",
    "3.6": "Before choosing a regression, say exactly what you want to learn from the data. The estimand is that target quantity, such as an average difference or a slope under a specified model. Describing a relationship, predicting a later outcome, and explaining a cause are different tasks. This lesson uses a small return model to make that distinction concrete.",
    "3.9": "A fitted coefficient is an estimate from one sample. Inference asks how much that estimate might vary and which claims the evidence can support. Begin with the assumptions behind the standard error. The next lessons examine how unequal error variation, time dependence, and model choices can change your interpretation even when the fitted coefficient stays the same.",
    "3.13": "A time series can contain trends, persistence, and changes in its behavior. Those features affect which models and comparisons make sense. Start by asking whether the series fluctuates around a reasonably stable pattern or keeps moving away from it. The distinction guides how you transform the data and how you judge forecasts on later periods.",
    "3.2": "Two series can move together for a while without having a stable long-run relationship. Cointegration examines a more specific possibility: a combination of the series may behave more stably than either alone. Work through the assumptions before interpreting a spread as a trading opportunity. Later lessons connect adjustment and changing volatility to the same need for careful diagnosis.",
    "3.20": "A portfolio can appear to perform well because it carries exposures that a simple benchmark does not show. Factor models help you identify those exposures and examine what remains. Start with dated, consistently measured returns and factors. Then interpret coefficients, uncertainty, and changes in exposure before deciding what a positive intercept means.",
    "3.23": "Observing several companies over time gives you two sources of variation: differences between companies and changes within each company. Panel methods use that structure, but they still need assumptions about omitted influences and related errors. Begin by identifying which comparison a model is making. The later causal methods build on that habit of stating the comparison explicitly.",
    "3.4": "Research credibility depends on how the evidence was produced as well as the final estimate. In this unit, connect downside measures with uncertainty, repeated testing, and selection decisions. Ask whether an apparently strong result survives a realistic description of the data and the research process. Keep unsuccessful trials visible when explaining why one model was selected.",
    "3.29": "The project units ask you to move from understanding an equation to producing an analysis another person can repeat. Start with a written question, preserve the data and configuration, and calculate a small case independently. When the program produces an answer, compare it with that reference before interpreting the larger output.",
    "4.5": "A strategy begins with a reason a repeatable rule might produce a useful result. That reason must become specific decisions about information, timing, holdings, and costs. If those decisions remain vague, it is difficult to tell whether a result supports the original idea. Start this unit by writing a claim that could be rejected by evidence.",
    "4.9": "A strategy can only act on information that existed at the decision time. Historical databases often include later corrections, changed company lists, or adjusted prices. Trace when each input became available before using it in a signal. This unit explains how to build a usable research dataset while keeping those timing and coverage choices visible.",
    "4.1": "A screening rule narrows a list of companies using measurable conditions. It does not complete the investment analysis. For value and quality strategies, begin by explaining what each accounting measure represents and when it was published. Then follow the path from the screen to an actual holding, including the reasons a seemingly cheap company may remain a poor candidate.",
    "4.15": "Trend and momentum strategies use past price behavior to form a rule. The timing and measurement choices determine what that rule actually does. Start with one asset and one decision date, calculate the signal by hand, and identify the earliest possible trade. Then compare how ranking assets, skipping recent periods, and rebalancing change the resulting portfolio.",
    "4.3": "A pairs strategy studies the relationship between two assets and may trade their relative movement. Similar-looking charts do not by themselves establish a reliable relationship. Begin with the economic connection, the statistical assumptions, and the costs of trading both sides. The following lessons show why borrowing, timing, and a broken relationship can matter as much as the initial signal.",
    "4.4": "A prediction becomes part of a strategy only after you decide how it changes holdings. A model may rank stocks or estimate a return, but the portfolio also needs sizing, constraints, timing, and costs. In this unit, follow the prediction through those decisions. Evaluate the complete process on later data and compare it with simpler rules.",
    "4.25": "Several attractive signals can still produce a concentrated or unaffordable portfolio. Portfolio construction decides how much to hold and how the positions interact. Start with a small set of proposed weights, then check cash, exposure limits, and the effect of trading costs. Accounting for the resulting trades lets you verify that the strategy you measured is the one you intended.",
    "4.29": "The final research stage asks whether the selected strategy deserves further work. Keep the evaluation period separate from the trials used to choose it. Then challenge the result with reasonable changes to assumptions, parameters, and execution conditions. A defensible conclusion explains what passed, what failed, and which parts of the idea remain untested.",
    "5.6": "Before writing the bot's loop, describe one complete decision in words. Which data arrives, what rule uses it, what checks can reject a trade, and what record proves what happened? Those details are the specification. This first unit connects the research idea to an event-driven system, where each new event can update state or trigger a carefully defined action.",
    "5.2": "A rule-based bot makes decisions from explicit conditions. Its simplicity can make the behavior easier to inspect, but the rule still needs evidence and realistic execution assumptions. Work through one signal at a time and record when it becomes known. Then examine how turnover, costs, and the chosen comparison affect the research result.",
    "5.12": "Submitting an order and receiving a fill are separate events. Between them, quotes may change, quantities may run out, and cancellation requests may race with execution. This unit follows the life of an order and the cash it commits. Use a small paper ledger to check that every accepted fill changes balances exactly once.",
    "5.4": "A trading system needs rules for when it must refuse an otherwise valid signal. Those rules depend on positions, cash, outstanding orders, data quality, and operating limits. Begin by writing the condition that must always hold, then test a case that tries to break it. Later lessons explain how to halt and resume without losing track of existing commitments.",
    "5.18": "A model's target describes an outcome that becomes known after the prediction. If a future outcome overlaps the period used for another example, an ordinary data split can accidentally share information. Draw the timeline of each example before fitting a model. This unit connects those time boundaries to baselines, thresholds, and monitoring.",
    "5.3": "An AI research tool can summarize or extract information, but the trading system still needs explicit rules for accepting its output. Start with a narrow task and a source the result can be checked against. Distinguish a model's suggestion from the authority to change an account or submit an order. The following lessons make that distinction testable.",
    "5.25": "A system must keep behaving predictably when work arrives faster than it can be processed or when a request fails. Queues, retries, and saved state are ways to manage those situations. Follow one event through an interruption and restart. The important question is whether it is lost, duplicated, or recovered with the same meaning.",
    "5.33": "Historical market records include changes in the instruments themselves. Splits, dividends, trading sessions, and company membership can all affect prices and eligibility. Begin by deciding what each record represents and how it should change the bot's state. This unit extends that accounting discipline into order-book replay and multiple-asset execution.",
    "5.37": "Different strategy families create different patterns of exposure and trading. A ranked portfolio, a pairs trade, and a market maker need different assumptions about positions and execution. Start with the economic idea and a small worked decision. Then ask how the system behaves when a relationship changes, liquidity falls, or inventory becomes unbalanced.",
    "5.41": "A strong evaluation must account for how the strategy was chosen. Reusing periods, overlapping labels, and selecting the best of many trials can make evidence look stronger than it is. This unit organizes the research timeline and records the search process. It also checks whether the strategy can be implemented under the costs and borrowing assumptions it needs.",
    "5.45": "Advanced models need evaluation at the level of the task they perform. A classifier, a retrieval system, and an evidence summary can fail in different ways. Define the expected output and a checkable reference for each task. Then examine errors, uncertainty, and situations where the system should decline to produce an actionable answer.",
    "5.29": "The final projects combine research, execution, and recovery into a system another person can inspect. Begin with the smallest complete run and keep its inputs, events, and balances. Add the acceptance checks before expanding the workload. Your final record should explain both a successful run and what happens when a planned failure is introduced.",
    "9.1": "C gives you more direct control over memory and execution, which also makes you responsible for more details. Begin by preserving the behavior of the program you already understand. Define its inputs, outputs, timing, and accounting rules before trying to make it faster. The first example shows why speeding up one component does not produce the same speedup for the whole job.",
    "9.5": "A fast program still needs well-defined data. At the input boundary, check what each record contains, whether timestamps are ordered, and how invalid values are handled. Then consider how records are arranged in memory and processed over time. This unit connects data layout to both performance and the chronological meaning of a trading decision.",
    "9.9": "Optimization begins with measurement. A timing result depends on the workload, the clock, setup costs, and variation between runs. Start by repeating a known calculation and checking that every run still produces the expected output. Then identify where the time goes. This gives you evidence for choosing an improvement and judging whether it helped.",
    "9.13": "Parallel work is easiest to reason about when tasks can run independently. Several parameter experiments may share read-only data while keeping their results separate. Start by identifying what each worker owns and when its output becomes visible. The next lessons explain synchronization, reproducible random seeds, and how to combine results without changing their meaning.",
    "9.17": "More advanced hardware does not make every workload faster. Work must be arranged so that the benefit of parallel arithmetic outweighs setup, movement, and coordination costs. Begin with the size and structure of the job, then account for the whole path through the system. Keep numerical checks alongside timing results as you explore vector, accelerator, and distributed designs.",
    "9.21": "The last unit returns to the system's promises under difficult conditions. An account update must remain consistent even when an order is rejected or a process stops. Write the before-and-after state and identify which changes must happen together. Use replay and failure cases to check that the optimized system still follows the original trading and accounting rules.",
    "6.6": "Computers work with bytes. Text, transaction records, and numbers must be encoded into bytes before a cryptographic operation can process them. A hash produces a digest from those exact bytes. Begin with a tiny input you can inspect; a space or newline is still part of the input. This precision is the foundation for later signatures and transaction checks.",
    "6.10": "A ledger records who owns what and which changes are allowed. A coin system needs rules for validating transfers and agreeing on the accepted history. Start with balances, signatures, and the conditions for one valid transaction. Then examine what a whole block changes and how a node should reject an invalid history.",
    "6.14": "A token is a program with rules for balances, transfers, and permissions. To understand it, separate the displayed amount from the integer units stored by the program. Then follow which caller can request each operation and which state changes result. This unit builds and tests a local token so you can inspect those rules directly.",
    "6.1": "Supply numbers and trading prices describe different parts of a token system. Issuance and distribution rules affect who can hold tokens and when, while market mechanisms determine how trades occur. Begin by checking that the supply accounting adds up. Then trace a small trade through the liquidity pool and identify the costs and risks it creates.",
    "6.4": "A valid transaction may still face uncertain timing, ordering, or execution costs. Other parts of a system may also rely on external prices, bridges, or administrators. Follow the transaction through those dependencies and ask what each one is trusted to do. This unit turns those assumptions into failure scenarios and checks on the resulting state.",
    "6.21": "A working local demonstration is only part of a complete system description. Someone reviewing it also needs to understand supply changes, recovery rules, permissions, and the evidence behind its claims. In the final unit, assemble those details into a reviewable record. Be precise about what the code implements and which decisions remain a proposed policy.",
    "7.1": "Before training a model, define the prediction in terms of a real decision and a timeline. What information is available now, what outcome will be measured later, and how could the prediction be used? A clear target makes the rest of the workflow easier to check. This lesson follows a short return period so you can see where inputs end and outcomes begin.",
    "7.5": "Features are the inputs a model sees; labels are the outcomes it learns to predict. Both need dates and a clear definition. Start with one row, identify the last information available, and draw the future interval used for its label. This unit then shows how to split and preprocess rows without letting later information reach training decisions.",
    "7.9": "Training adjusts a model to improve an objective on a set of examples. Begin with a simple baseline so you can tell whether extra complexity adds useful evidence. Work through the meaning of the loss function before comparing algorithms. A model that fits training data closely still needs a separate evaluation on later observations.",
    "7.13": "Choosing a model is itself a research decision. Trying many settings and reporting only the best score can hide how much selection took place. This unit separates model selection from final evaluation and explains what different metrics measure. Follow a prediction into the decision and cost assumptions before interpreting a better score as an investment improvement.",
    "7.17": "When a model makes mistakes, the average score may hide where they occur. Inspect errors by date, stock, and condition, and compare them with data quality and the model's inputs. This unit uses diagnosis to choose a specific repair. Change one justified part of the workflow and evaluate it again under the same rules.",
    "7.21": "A saved model is only useful if new inputs are prepared in the same way as the inputs used during evaluation. Preserve the preprocessing, feature definitions, and version information alongside the fitted model. This final unit follows a prediction into a monitored workflow, where changed data and delayed outcomes can inform a later review.",
    "10.1": "Before seeing the final result, write down what the evaluation will measure and what would count as a failure. This agreement is the evaluation contract. It gives the report a stable reference when a result looks attractive or disappointing. The worked example shows why a profitable run can still fail a rule that was part of the original plan.",
    "10.5": "Performance measures summarize a sequence of cash and portfolio values. Before calculating them, confirm that the values use the same dates, units, and treatment of contributions and costs. Then examine growth, variability, and drawdowns as separate questions. Each measure should be accompanied by a sentence explaining what it tells the reader.",
    "10.9": "A result can look convincing because the research process favored it. The challenge stage asks what happens on later data, under nearby assumptions, or after considering the earlier trials. Begin by separating the period used to choose the algorithm from the period used to evaluate it. Keep that distinction visible in every comparison and conclusion.",
    "10.13": "A clear report helps a reader move from evidence to a decision. Choose tables and charts according to the question they answer, then label their units, periods, and assumptions. The final lessons connect those displays to attribution and a written conclusion. Explain which findings are well supported and which still require further investigation.",
}

# These passages explain the actual numbers and conclusions in the existing case.
# They are inserted inside the worked-example section, before the next topic.
WORKED_EXPLANATIONS = {
    "0.1": """### Step-by-step breakdown of the calculation

1. **Identify the starting capital**: Maya begins by investing $200. This initial outlay is our baseline comparison point and serves as the denominator in our return calculation.
2. **Calculate the dollar gain or loss**: If she sells the asset for $220, subtract the starting capital from the ending proceeds: $220 − $200 = $20. Maya made a $20 dollar profit.
3. **Compute the percentage return**: Divide the $20 gain by the $200 initial capital: $20 / $200 = 0.10. Multiply by 100 to express this as a percentage: **+10%**. In plain language, Maya earned 10 cents for every dollar she committed over this holding period.
4. **Follow the loss scenario**: If the price falls and she sells for $170 instead, her net change is $170 − $200 = −$30. Dividing −$30 by the original $200 gives −0.15, or **−15%**. Notice that the denominator remains the original $200 baseline.

These introductory numbers deliberately exclude transaction fees and dividends so you can master the core return formula first. Later lessons will layer in those cash flows. Always state the exact timeframe when reporting returns, because a 10% return in one month represents a completely different performance pace than 10% over five years.""",
    "0.2": """### Step-by-step breakdown of ownership math

Let's address three distinct questions using Harbor Foods:

1. **What is the entire company's equity worth on the open market?**
   Multiply all 1,000,000 shares outstanding by the quoted share price of $20. This gives the **$20 million market capitalization**. This figure represents the aggregate value that the public market assigns to all common shares today; it does not mean the company has $20 million sitting in a bank vault.
2. **What fraction of the business does Maya own?**
   Divide Maya's 100 shares by the 1,000,000 total shares outstanding: 100 / 1,000,000 = 0.0001, which equals **0.01%** (one hundredth of one percent). Owning shares gives you a proportionate claim on corporate earnings and voting rights, but not the right to take company physical property.
3. **What is Maya's holding worth, and what dividend does she receive?**
   - Market value of holding: 100 shares × $20 = **$2,000**.
   - Dividend payout: A declared $0.50 cash dividend per share yields 100 × $0.50 = **$50.00** in cash, paid directly into her brokerage account before taxes.

Finally, compare the second company with 100 million shares trading at $2. While its $2 share price appears "cheaper" at first glance, its total market capitalization is $200 million (100,000,000 × $2). The market values that second company at ten times the overall value of Harbor Foods! Always multiply share price by share count before comparing company valuations.""",
    "0.3": """### Step-by-step breakdown: Follow the money

Notice how the cash moves differently across the two transactions:

1. **Transaction 1 (Primary Market - Capital Formation)**:
   Harbor Foods creates and issues 100,000 brand-new shares at $20 each. Multiplying 100,000 by $20 yields **$2 million** before underwriting costs. Because Harbor Foods is the issuing entity, that $2 million flows directly into the company's corporate treasury to fund new business operations, factories, or hiring.
2. **Transaction 2 (Secondary Market - Share Trading)**:
   Maya purchases 50 existing shares from Leo at $21 each through a stock broker. The total trade value is 50 × $21 = **$1,050**. Here, Leo is the seller. Maya's $1,050 payment goes through the clearinghouse to Leo (minus broker commissions). Harbor Foods receives **zero dollars** from this trade, because no new shares were created—existing shares merely changed owners.

This distinction explains why a stock can trade millions of shares every day without the company receiving continuous cash injections. The secondary market provides liquidity and price discovery for existing owners, which in turn makes investors willing to fund companies in the primary market in the first place.""",
    "0.4": """### Step-by-step breakdown: Reading the quote from both sides

Let's dissect the fictional quote (Bid: $49.90 for 100 shares | Ask: $50.10 for 80 shares):

1. **Understand who is on each side**:
   - The **Bid ($49.90)** is the highest price a prospective buyer is currently willing to pay. If you want to sell immediately, this is your price.
   - The **Ask ($50.10)** is the lowest price a prospective seller is currently willing to accept. If you want to buy immediately, this is your price.
2. **Calculate the Bid-Ask Spread**:
   $$\\text{Spread} = \\text{Ask} - \\text{Bid} = \\$50.10 - \\$49.90 = \\$0.20 \\text{ per share}$$
3. **Calculate the round-trip cost of immediate execution**:
   If you buy 10 shares at the market ask ($50.10), you pay $501.00. If you immediately turn around and sell those 10 shares at the market bid ($49.90), you receive $499.00. Even though quotes didn't move, you lost **$2.00** ($0.20 × 10 shares). This is the cost of crossing the spread for immediate execution.
4. **Why displayed quantity (depth) matters**:
   The ask quote only offers 80 shares at $50.10. If you submit a market order to buy 200 shares, the first 80 shares will fill at $50.10, but the remaining 120 shares must fill at higher available asks on the order book (e.g., $50.15, $50.25). This price slippage raises your average purchase price above the initial quote.

A limit order protects you against this slippage by setting a strict price cap, but at the risk that the order might not fill if sellers refuse to meet your price.""",
    "0.5": """### Build the return from cash movements

To avoid confusion when calculating investment returns, set up two clear columns tracking all cash movements: money paid out versus money received.

1. **Cash Outlay (Money Paid Out at Entry)**:
   - Share purchase: 10 shares × $100 = $1,000
   - Brokerage entry fee: $2
   - **Total initial outlay = $1,002**. This total cash outlay is the initial outlay used in the denominator of our net return calculation.
2. **Cash Inflows (Money Received During Holding and Exit)**:
   - Gross sale proceeds: 10 shares × $110 = $1,100
   - Minus brokerage exit fee: −$2
   - **Net sale proceeds = $1,098**
   - Plus cash dividends received while holding: **+$10**
   - **Total cash received = $1,098 + $10 = $1,108**
3. **Calculate Net Profit and Net Return**:
   - Dollar net profit = Total cash received − Initial outlay = $1,108 − $1,002 = **$106**
   - Net percentage return = $106 / $1,002 ≈ 0.1058, or **10.58%** before taxes.

Notice that looking only at the share price move ($100 to $110, or +10%) would miss the $10 in dividends and the $4 in total brokerage fees. Tracking complete cash flows gives your true financial return.

Once you can account for a single holding period, remember that sequential periods multiply through compounding: a 10% gain followed by a 10% loss results in a net 1% loss ($100 × 1.10 × 0.90 = $99), proving that percentage losses hurt more than equal percentage gains help.""",
    "0.6": """### Step-by-step breakdown: Connecting accounting to business reality

Let's trace Cedar Tools' numbers to see how the statements connect:

1. **Calculate Earnings Per Share (EPS)**:
   Cedar Tools generated $12 million in sales revenue and finished with $2 million in Net Income after all expenses. Divide Net Income by the 1,000,000 weighted-average diluted shares:
   $$\\text{EPS} = \\frac{\\$2,000,000}{1,000,000 \\text{ shares}} = \\$2.00 \\text{ per share}$$
   Always use Net Income—not revenue—to calculate earnings per share.
2. **Calculate the Price-to-Earnings Ratio (P/E)**:
   With shares trading at $30, divide the share price by EPS:
   $$\\text{P/E} = \\frac{\\$30}{\\$2.00} = 15$$
   In ordinary language, investors are willing to pay $15 today for every $1 of Cedar Tools' current annual net earnings.
3. **Examine the Balance Sheet Equity**:
   $$\\text{Book Equity} = \\text{Assets} − \\text{Liabilities} = \\$15\\text{M} − \\$9\\text{M} = \\$6\\text{M}$$
   Book equity represents the net accounting residual of the business. It is a historical accounting calculation, not a guarantee of liquidation value.
4. **The Critical Reality Check: Operating Cash Flow**:
   Now compare the $2 million reported Net Income with the **$0.4 million in Operating Cash Flow**. Why the $1.6 million gap? Cedar Tools may have recorded sales to customers who have not yet paid (building up accounts receivable). This is not necessarily fraud, but it warrants careful investigation into customer collection times and inventory turnover before assuming the reported profit is healthy.""",
    "0.7": """### Step-by-step breakdown: Sizing a position around risk

Let's walk through how professional risk management determines trade size:

1. **Establish your risk budget**:
   In a $10,000 paper trading account, you decide to risk at most 1% of your total capital on this single idea:
   $$\\text{Risk Budget} = 1\\% \\times \\$10,000 = \\$100$$
2. **Determine risk per share**:
   You plan to buy at $50 and place a stop-loss exit trigger at $48.
   $$\\text{Risk Per Share} = \\$50 − \\$48 = \\$2.00$$
3. **Calculate position quantity**:
   $$\\text{Shares to Buy } (q) = \\frac{\\text{Risk Budget}}{\\text{Risk Per Share}} = \\frac{\\$100}{\\$2.00} = 50 \\text{ shares}$$
4. **Compare position value versus risk budget**:
   Buying 50 shares at $50 requires **$2,500** of cash (25% of your total account capital). However, your planned risk is strictly **$100** (1% of the account), because your plan is to exit if the stock drops to $48.
5. **The Market Gap Reality Check**:
   What happens if the company reports bad news overnight and opens the next morning at $45? Your stop order triggers and sells at $45. Your actual loss is:
   $$50 \\text{ shares} \\times (\\$50 − \\$45) = \\$250 \\text{ (2.5\\% of the account)}$$
   This proves that stop-loss orders help manage risk, but they do not eliminate overnight gap risk. Always consider whether your total position size ($2,500) is safe in a worst-case scenario.""",
    "0.8": """### Step-by-step breakdown: Designing a disciplined trading plan

Ari's paper-trading plan for Harbor Foods demonstrates how to turn vague sentiment into a structured, reviewable decision:

1. **Define the Hypothesis and Invalidating Evidence**:
   - Hypothesis: Customer collections will normalize, restoring operating cash flow.
   - Invalidating evidence: Another quarterly filing showing deteriorating receivables or negative operating cash flow. Defining what proves you wrong upfront prevents rationalizing a failing position later.
2. **Set Precise Order Instructions and Capital Limits**:
   - Instruction: Buy 10 shares using a **$20 Buy Limit**. Reserving $200 plus estimated fees.
   - Execution rule: If market sellers demand more than $20, the order stays unfilled. A disciplined trader accepts missing a trade rather than overpaying.
3. **Plan the Exit and Stress-Test Gap Risk**:
   - Base stop exit: Trigger at $18, representing a planned loss of 10 × ($20 − $18) = $20 before costs.
   - Gap stress test: In an unexpected gap down to $15, the loss becomes 10 × ($20 − $15) = $50. Knowing this worst-case number in advance ensures the trade size won't damage the account.
4. **Schedule the Review**:
   - Review date: After Harbor Foods releases its next audited quarterly report. Evaluate whether the thesis held true, whether the plan was followed, and record the outcome honestly regardless of profit or loss.""",
    "1.1": """### Read the margin of safety in plain language

In the equation, P is the price and V is the estimated value. Dividing P by V tells you what fraction of that estimate you would pay. Subtracting that fraction from 1 gives the discount. With P = $60 and V = $100, you would pay 60% of the estimate, leaving a 40% discount.

The important next step is changing the estimate. If V is only $75, the same $60 price is 80% of the estimate, leaving a 20% discount. The purchase price has not changed; the assumption about the business has. That is why a large-looking discount is only as useful as the value estimate underneath it.

To require a 30% discount to the $75 weak-case value, you can pay 70% of that value: 0.70 × $75 = $52.50. The current $60 price is above that limit. Saying that the base case passes and the conservative case fails describes those two calculations. It does not establish the probability of a loss or guarantee protection.""",
    "2.1": """### Move each payment back to today

At a 10% annual rate, $100 today grows to $110 after one year. To reverse that step, divide the one-year payment of $110 by 1.10. The result is $100 today.

The second payment is two years away. Reverse two periods of growth by dividing $121 by 1.10 twice, or by 1.10 squared. That also gives $100. Only after placing both payments on the same date should you add them: $100 + $100 = $200. Dividing $231 by 1.10 only once would treat both payments as arriving in one year.

The perpetuity calculation describes a different payment pattern that continues indefinitely under the stated growth assumption. Subtract 2% growth from the 7% required return to get 5%, or 0.05. Dividing next year's $5 payment by 0.05 gives $100. The result depends on that continuing pattern and on the required return remaining above the growth rate.""",
    "3.6": """### Translate the fitted equation into a sentence

The intercept contributes 0.1 percentage points in this model. The slope is 1.2, so a factor value of 2 percentage points contributes 1.2 × 2 = 2.4 percentage points. Adding the two parts gives a fitted mean of 2.5 percentage points.

“Fitted mean” describes what the estimated equation says for that input. It does not mean every observed return at that factor value must be 2.5. An observation can differ from the fitted mean, and a different sample can produce different coefficients.

The equation describes an association under the chosen model. To claim a causal effect, you would need additional reasoning about how the factor changes and which other influences are controlled. Writing the research question first helps you avoid treating a descriptive regression as evidence for a stronger claim.""",
    "4.5": """### Explain what would make the proposal fail

Cedar is proposing more than a ranking. The proposal includes which information is used, how many companies are held, the comparison portfolio, and the treatment of trading costs. Those details make the claim testable: another researcher can implement the same decisions and examine the same outcome.

Read the 6% gross advantage and 7% cost drag on the same return basis. Subtracting the drag leaves a net advantage of −1 percentage point. The ranking may have looked promising before costs, but this particular result fails the claim of an advantage after costs.

The 20-basis-point assumption is a cost per traded notional amount, meaning per dollar of the transactions it applies to. One basis point is 0.01 percentage points, so 20 basis points is 0.20%. Its effect over a full experiment also depends on how much trading occurs. Keep a per-trade cost assumption separate from the measured total effect on performance.""",
    "5.6": """### Connect the specification to the cost estimate

A 10% single-stock limit in a $100,000 paper portfolio allows at most $10,000 for that stock under the stated rule. It does not require the bot to use that entire amount. The timing rule is another separate condition: the signal uses completed daily bars and the target order is placed at the next eligible open.

Now examine the claimed benefit. One basis point is 0.01 percentage points. The estimated costs total 4 + 2 + 3 = 9 basis points. Subtracting them from 12 basis points of gross benefit leaves only 3 basis points, or 0.03 percentage points, under those assumptions.

If slippage rises to 6 basis points, the costs become 4 + 2 + 6 = 12 basis points. That uses up the entire estimated gross benefit. Writing this down before building the bot helps the team see which assumption matters and what needs stronger evidence. Faster execution code alone does not settle whether the research idea survives its costs.""",
    "6.6": """### Understand the two search problems

A 16-bit value has 2 to the power of 16 possible patterns, which is 65,536. A digest with only that many possible outputs must give the same output to some different inputs. A collision means finding any two different inputs with matching digests.

The birthday comparison concerns any matching pair among many samples. As the sample grows, each new sample can match any earlier one, so the number of possible pairs grows quickly. This is why the illustrative scale is around the square root of 65,536, or 256 samples. It is an order-of-magnitude guide, not a guarantee that sample 256 produces a collision.

Finding an input for one specified target digest is a different task: a match elsewhere is no help. Keeping those tasks separate prevents a misleading interpretation of hash strength. For the actual SHA-256 project, also check the input bytes carefully. The bytes for abc and the bytes for abc followed by a newline describe different inputs.""",
    "7.1": """### Put the prediction on a timeline

The notation t identifies the current day. Close t is the end of that day's observation period. Open t+1 is the next day's opening point, and open t+2 is the following day's opening point. In this task, features become available after close t, before the example's entry at open t+1.

The target measures the change from the entry value of 100 to the exit value of 102. Divide the gain of 2 by the starting value of 100 to get 0.02, or 2%. The regression target keeps that numerical return. The classification label keeps only whether it is positive.

A positive label loses information about the size of the gain. It also says nothing by itself about the cost of turning the prediction into a trade. This distinction explains why the course evaluates data timing, prediction quality, and trading results as connected but separate steps.""",
    "8.1": """### Slow down the headline's arithmetic

The $90 million figure is a maximum across three years. It is not stated as $90 million of revenue in the next year. If you spread the ceiling evenly for this illustration, divide $90 million by 3 to get $30 million per year.

To judge the size, compare annual amounts with annual amounts. Divide that $30 million by the company's existing $600 million annual revenue. The ratio is 0.05, or 5%. This gives you a scale for the question. It does not establish the actual delivery schedule or guarantee that the maximum amount will be earned.

Revenue is also different from profit and cash. The company may incur costs to perform the contract, receive payment later, or use capacity that would otherwise serve another customer. After checking the headline amount, investigate those terms before estimating the effect on earnings or value. The source supports an announced contract; your interpretation requires additional steps.""",
    "9.1": """### Time the whole job

Begin with the original total: 90 seconds of simulation plus 30 seconds of preparation equals 120 seconds. A three-times-faster simulation divides the simulation time by 3, reducing that part from 90 seconds to 30 seconds.

Preparation still takes 30 seconds in this example. Add the new parts to obtain 60 seconds for the whole job. The overall speedup is the old total divided by the new total: 120 / 60 = 2. The simulation itself is 3 times faster, while the complete job is 2 times faster.

This distinction helps you decide what to optimize next. As one part becomes faster, the unchanged parts make up more of the remaining time. Keep the same workload and correctness checks when comparing implementations, and state clearly which section of the program each timing describes.""",
    "10.1": """### Explain why profit does not settle the evaluation

A return measure answers how the portfolio grew over the chosen period under the stated accounting rules. A drawdown measure answers a different question: how far its value fell from an earlier peak along the way. A strategy can finish with a gain after experiencing a decline that the original plan did not allow.

Here, the 12% test return is favorable on its own, but the run also breaches the predeclared 10% drawdown limit. The evaluation must record both observations. Replacing the limit after seeing the result changes the question being evaluated.

A useful conclusion would explain the gain, the breached condition, and what further research could investigate. If the team proposes a different limit or a revised strategy, record it as a new proposal with its own evaluation. That keeps a later reader from mistaking a rule chosen after the result for a rule tested in advance.""",
    "11.1": """### Separate the decision from the outcome

Start with Rani's arithmetic. A 15% fall from wealth of 100 removes 15, leaving 85. That is a real loss in the example, even if her original process was careful. To assess whether she can continue, you need to know her goal, cash needs, and the loss scenario she planned for.

Dito's 20% gain is also an observed outcome. It does not supply the business analysis he skipped before buying. One favorable result cannot tell us whether the same approach would be dependable across other decisions.

The comparison is not a claim that a careful process prevents losses. It shows why a review should ask two questions: what happened, and whether the original choice used the available evidence responsibly. A decision journal preserves the second question by recording the reasons before the outcome is known.""",
}

# Definitions are selected from the lesson's own title, objective, and explanation.
# Existing lesson-specific definitions keep priority over these shared entries.
VOCABULARY = {
    "Inflation": "An increase in the overall price level over a stated period. A measured inflation rate describes a particular basket of prices; the change in one household's actual spending costs can differ.",
    "Purchasing power": "What an amount of money can buy. If the prices of the things you need rise faster than your available money, your purchasing power falls even though the currency amount may have increased.",
    "Temperament": "The habits and emotional responses you bring to a decision. In investing, it includes how you react to uncertainty, losses, gains, and pressure from other people.",
    "Incentive": "A reason someone may prefer one outcome over another, such as a fee, commission, or personal interest. Understanding an incentive helps you assess a recommendation alongside its evidence.",
    "Decision journal": "A record of your reasons, evidence, alternatives, and expectations written before an outcome is known. It helps you review the original decision without rewriting its history.",
    "KPI": "A key performance indicator: a measure used to track an aspect of a business. Check its definition and any changes before comparing the reported number across periods.",
    "Ledger": "A record of changes to cash, positions, or other balances. Each accepted transaction should explain how the balance before it becomes the balance after it.",
    "Schema": "The expected structure of a data record, including field names, types, and required values. Checking a schema catches structural errors before a calculation uses the data.",
    "Recovery": "Restoring a system to a consistent state after an interruption. It requires knowing which changes were accepted, which are pending, and which requests can be retried safely.",
    "Compiler": "A program that translates source code into a form the computer can execute. Its errors and warnings help identify problems before the resulting program is run.",
    "Thread": "An execution path within a process. Threads can work concurrently and share memory, so the program needs clear rules for accessing and changing shared data.",
    "Scheduling": "Choosing when and where pieces of work run. In parallel experiments, the scheduling choice affects how workers share the workload and how much coordination they need.",
    "Intrinsic value": "An estimate of what an investment is worth based on the business, its assets, cash flows, and obligations. It depends on assumptions and can differ from the current market price.",
    "Margin of safety": "The gap between the price paid and a conservative estimate of value. The gap can allow for some error in the estimate, but it cannot guarantee that the investment will avoid a loss.",
    "Seniority": "The order in which different investors and creditors have a claim on payments or assets. A claim that ranks ahead of another is senior to it.",
    "Collateral": "An asset pledged to support a debt. The protection depends on the lender's rights and what the asset could actually be recovered for.",
    "Covenant": "A condition in a borrowing agreement, such as a limit on additional debt. Check exactly how it is defined and what happens if it is breached.",
    "Earning power": "An estimate of the profit a business can sustain through ordinary operations. It requires separating recurring activity from unusual gains, losses, and temporary conditions.",
    "Liquidation": "The process of selling assets and settling obligations when a business or position is wound down. The cash left after costs and senior claims can differ from recorded asset values.",
    "Dilution": "A reduction in an existing holder's ownership fraction when the relevant total number of shares or tokens increases. The effect on value also depends on what the issuer receives and how it uses it.",
    "Working capital": "Resources tied up in day-to-day operations, such as inventory and money customers owe, considered alongside short-term obligations. A growing business may need cash here before it receives payment.",
    "Basis point": "One hundredth of a percentage point. For example, 20 basis points equals 0.20 percentage points, written as 0.002 when used as a decimal rate.",
    "Benchmark": "A comparison used to judge a result, such as a market index or a simple portfolio rule. Use the same period and consistent return and cost definitions for both sides of the comparison.",
    "Discount rate": "The rate used to translate a future payment into an equivalent value today. The chosen rate must fit the payment's timing and the assumptions about its risk and currency.",
    "Compounding": "Applying each period's return to the value left by the previous period. A later gain or loss is calculated on the updated balance, so adding percentages can give the wrong cumulative result.",
    "Present value": "The value today of a future payment under a chosen discount rate. Payments on different dates must each be moved to the same date before their values are added.",
    "Variance": "A measure of how widely values differ from their mean, based on squared deviations. Its units are squared; taking the square root gives the standard deviation in the original units.",
    "Covariance": "A measure of how two quantities vary together. It is positive when above-average values tend to occur together and negative when one tends to be above average as the other is below.",
    "Correlation": "A standardized measure of a linear relationship between two quantities. It describes association and does not, by itself, show that one quantity causes the other.",
    "Conditional probability": "The probability of an outcome when specified information is known. For example, the probability of distress among firms showing a warning can differ from the probability among all firms.",
    "Confidence interval": "An interval produced by a method intended to cover the fixed target a stated fraction of the time over repeated samples, under its assumptions. It describes sampling uncertainty, not a guaranteed range for a future outcome.",
    "Standard error": "An estimate of how much a fitted quantity, such as a sample mean or regression coefficient, would vary across samples. It differs from the spread of the individual observations.",
    "Null hypothesis": "The reference claim used in a statistical test, such as no difference or a zero coefficient. A test evaluates how compatible the observations are with that claim and its assumptions.",
    "Multiple testing": "Examining many statistical claims or strategy candidates. Searching more possibilities creates more opportunities to find an impressive result by chance, so the search process matters when interpreting the winner.",
    "Regression": "A model that relates an outcome to one or more inputs. The fitted coefficients describe the relationship under the model; they need separate checks before being used for prediction or causal explanation.",
    "Estimand": "The exact quantity a study aims to learn, such as an average effect for a stated group or a slope in a specified model. Defining it helps you choose suitable data and methods.",
    "Residual": "The difference between an observed outcome and the value fitted by a model. Inspecting residuals can reveal patterns that the model has not captured.",
    "Heteroskedasticity": "A situation in which the size of the model's errors varies across observations. Standard errors that assume constant error variance may then give a misleading impression of precision.",
    "Autocorrelation": "A relationship between a series and its earlier values, or between errors at different dates. It means observations may contain less independent information than their count suggests.",
    "Stationarity": "A stability property of a time series. In the weak form used in many models, its mean and variance are stable over time and covariance depends on the time gap, rather than the particular date.",
    "Cointegration": "A relationship in which a combination of nonstationary series is stationary under the stated model. Moving together visually or having a high correlation is not enough to establish it.",
    "Endogeneity": "A problem in which a model input is related to influences in the error term. The fitted association can then fail to identify the causal effect the researcher wants to measure.",
    "Shrinkage": "Deliberately pulling an estimate toward a simpler target to reduce sensitivity to sample noise. It trades some bias for potentially more stable estimates.",
    "Factor": "A measured influence used to describe returns or risk across investments, such as a market return or a defined style portfolio. Its meaning depends on how it is constructed.",
    "Alpha": "The intercept in a specified return model. A positive estimate can reflect sampling variation or model limitations as well as performance, so it requires context and an uncertainty estimate.",
    "Beta": "A slope measuring sensitivity to an input, often a market return. Its units and interpretation depend on the returns, period, and other terms included in the model.",
    "Volatility": "A measure of variability in returns, commonly based on their standard deviation. State the observation frequency and any annualization convention when comparing values.",
    "Drawdown": "The decline in portfolio value from an earlier peak to a later value. Drawdown depth, time spent below the peak, and recovery time describe different parts of the experience.",
    "Bootstrap": "A method that repeatedly resamples observed data to study how an estimate varies. Time-series data may need resampling in blocks to preserve relevant dependence.",
    "Backtest": "A simulation of how specified decisions would have behaved on historical or synthetic data. Its meaning depends on information timing, execution rules, costs, and how the strategy was selected.",
    "Point-in-time": "Using the version of information that was available at the decision date. Later corrections or revised records must not silently appear in an earlier simulated decision.",
    "Signal": "A value or rule output used to inform a decision. A signal becomes an actual trade only after the system applies timing, position, risk, and execution rules.",
    "Turnover": "A measure of how much a portfolio trades over a period. The definition and denominator must be stated because they affect comparisons and estimates of trading costs.",
    "Slippage": "The difference between a chosen reference price and the actual or assumed execution price. State the reference and sign convention, and avoid counting costs twice.",
    "Liquidity": "The ability to trade the required quantity within the desired time and price conditions. Displayed prices alone do not establish the cost of trading a larger amount.",
    "Notional": "The amount a rate or exposure calculation applies to, often price multiplied by quantity for a stock trade. It is different from the profit, margin posted, or risk budget.",
    "Rebalancing": "Trading to move a portfolio from its current holdings toward its chosen target weights. The decision should account for timing, costs, and any trading limits.",
    "Mean reversion": "The idea that a quantity tends to move back toward a reference level. You need to define that level and test whether the relationship remains stable enough for the intended use.",
    "Momentum": "A strategy idea based on persistence in past performance. The lookback period, ranking rule, delay, and execution assumptions determine what is actually being tested.",
    "Invariant": "A condition that must remain true as a program changes state. For example, a cash ledger should reconcile before and after every accepted trade.",
    "State machine": "A way to describe a system through named states and allowed transitions. An order might move from submitted to partially filled or cancelled, with explicit rules for each event.",
    "Backpressure": "A way to limit incoming work when a system cannot process it fast enough. It prevents queues from growing without a controlled response.",
    "Idempotency": "The property that retrying the same request does not apply its effect more than once. It matters when a request succeeds but the response is lost.",
    "Feature": "An input supplied to a model, such as a lagged return or a financial ratio. Its calculation and availability time are part of the model's definition.",
    "Label": "The outcome a model learns to predict. It needs a precise definition and an outcome period, so it can be kept separate from information available at prediction time.",
    "Baseline": "A simple, explicit starting method used for comparison. It helps you judge whether a more complex method adds useful evidence under the same evaluation rules.",
    "Regularization": "A method that discourages an overly complex fit, often through a penalty or constraint. Its setting should be chosen using training and validation data, separately from the final test.",
    "Calibration": "How closely predicted probabilities agree with observed frequencies across comparable predictions. A model can rank outcomes well while still giving poorly calibrated probabilities.",
    "Walk-forward": "An evaluation that repeatedly fits or selects a method using earlier data and then checks it on a later period. Each split must preserve the decision-time information boundary.",
    "Holdout": "Data reserved from the fitting or selection process for a separate evaluation. If its results are repeatedly used to improve the method, it no longer serves as an untouched final test.",
    "Data leakage": "Information entering a research step where it would not have been available or permitted. Future labels or preprocessing fitted on evaluation data can make a model appear more successful than it is.",
    "Inference": "In statistical analysis, drawing conclusions from data under stated assumptions. In machine learning deployment, the same word can mean running a fitted model on new inputs; check which meaning the lesson uses.",
    "Drift": "A change over time in input data, outcomes, or their relationship. A drift signal is a reason to investigate; it does not by itself prove that a model has become useless.",
    "Materiality": "How large and relevant a change is for the decision being examined. Compare the amount with an appropriate denominator and time period before judging its importance.",
    "Base effect": "The influence of the earlier comparison value on a reported growth rate. A high annual rate can partly reflect an unusually low value a year earlier.",
    "Cash flow": "Money moving into or out of a business or portfolio over a period. It can differ from accounting profit because recognition and payment happen at different times.",
    "Hash": "A digest calculated from an exact sequence of input bytes. Cryptographic hash functions are designed for security properties such as making collisions difficult to find; a digest is not encryption.",
    "Digital signature": "A cryptographic value used to check that a message was signed with the private key corresponding to a public key. The signed message and the verification rules determine what authorization it represents.",
    "Nonce": "A value used to distinguish requests or transactions according to a protocol's rules. In a transaction system, it can help prevent an accepted request from being replayed.",
    "Consensus": "The rules and process by which participating nodes agree on an accepted history or state. Its guarantees depend on the protocol's assumptions and failure model.",
    "Finality": "The conditions under which an accepted transaction or block is treated as settled by a protocol. Different systems provide different assumptions about whether and how that decision can change.",
    "Gas": "A measure of computational work used by the EVM to account for execution. Gas used, a gas limit, and the price paid per unit of gas are separate quantities.",
    "Allowance": "Permission recorded by a token contract for another address to spend up to a specified amount under the contract's rules. Approval and an actual transfer are separate operations.",
    "Pointer": "A C value that refers to an address. Before using it, the program must know that the referenced object is valid, accessible, and still alive.",
    "Ownership": "In memory management, responsibility for keeping an allocation alive and releasing it correctly. In an investing lesson, ownership instead describes the holder's legal or economic interest.",
    "Cache locality": "Arranging and accessing data so nearby or recently used values can be reused efficiently by the processor's cache. The benefit depends on the workload and access pattern.",
    "Data race": "Conflicting unsynchronized memory accesses from different threads where at least one access writes. In C, a data race can make the program's behavior undefined.",
    "Latency": "The time between a specified event and its response. State the start and end points, because processing time and complete end-to-end latency may differ.",
    "Throughput": "The amount of completed work per unit of time, such as experiments per second. Higher throughput does not automatically mean lower latency for one individual event.",
    "Speedup": "The original time divided by the new time for the same defined workload. A speedup for one component can differ from the speedup of the complete job.",
    "Reproducibility": "Keeping enough data, code, settings, and method detail for another run to reconstruct the reported result under the stated conditions.",
}


def vocabulary_for(lesson, course_id):
    """Prefer concepts named in the title over incidental words later in the text."""
    existing = list(lesson.get("terms", []))
    known = {item["term"].casefold() for item in existing}
    sections = [lesson["title"], lesson.get("objective", ""), lesson["content"]]
    text = " ".join(sections)
    model_courses = {
        "statistical-foundations",
        "econometrics",
        "strategy-lab",
        "stock-bots",
        "stock-machine-learning",
    }
    candidates = []
    for term, definition in VOCABULARY.items():
        if term.casefold() in known:
            continue
        # A transaction label or CPU feature is not a machine-learning concept.
        if term in {"Feature", "Label"} and course_id not in model_courses:
            continue
        if term == "Residual" and not re.search(r"\b(regression|fitted|OLS)\b", text, re.I):
            continue
        if term == "Factor" and not re.search(
            r"\b(factor (?:model|return|risk|exposure)|market factor|regression|CAPM)\b",
            text,
            re.I,
        ):
            continue
        if term == "Recovery" and course_id not in {"stock-bots", "c-hpc-trading", "web3"}:
            continue
        if term == "Ownership" and course_id != "c-hpc-trading":
            definition = "The rights held by the owner of an asset, share, or token. Check what those rights include: an ownership record alone does not establish a right to every payment, asset, or decision in the wider business or system."
        if term == "Benchmark" and course_id == "c-hpc-trading":
            definition = "A defined workload used to compare computing performance. Keep the inputs, correctness checks, hardware, build settings, and timed work clear so the measured difference has a useful meaning."
        pattern = re.compile(r"\b" + re.escape(term) + r"(?:s)?\b", re.I)
        for priority, section in enumerate(sections):
            if match := pattern.search(section):
                candidates.append((priority, match.start(), term, definition))
                break
    for _, _, term, definition in sorted(candidates)[: max(0, 4 - len(existing))]:
        existing.append({"term": term, "definition": definition})
    return existing


def attach_learning_guidance(catalog):
    """Expand lesson prose without modifying identifiers, equations, or grading."""
    lessons = {lesson["id"]: lesson for course in catalog for lesson in course["modules"]}
    assert set(COURSE_GUIDES) == {course["id"] for course in catalog}
    assert set(UNIT_INTRODUCTIONS) <= set(lessons)
    assert set(WORKED_EXPLANATIONS) <= set(lessons)
    course_titles = {course["id"]: course["title"] for course in catalog}

    def current_course_link(match):
        slug = match[1]
        title = course_titles.get(slug)
        return f"[{title}](/curriculum/{slug})" if title else match[0]

    for course in catalog:
        description, introduction = COURSE_GUIDES[course["id"]]
        course["description"] = description
        original_guide = course.get("readingGuide", "")
        # Separate the existing course logistics into readable paragraphs.
        guide_sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", original_guide)
        logistics = "\n\n".join(
            " ".join(guide_sentences[i : i + 2]) for i in range(0, len(guide_sentences), 2)
        )
        course["readingGuide"] = "\n\n".join(part for part in [introduction, logistics] if part)
        for lesson in course["modules"]:
            content = lesson["content"]
            if explanation := WORKED_EXPLANATIONS.get(lesson["id"]):
                marker = "## A worked example"
                assert marker in content, lesson["id"]
                start = content.index(marker) + len(marker)
                end = content.find("\n## ", start)
                if end < 0:
                    end = len(content)
                content = content[:end].rstrip() + "\n\n" + explanation + "\n" + content[end:]
            if introduction := UNIT_INTRODUCTIONS.get(lesson["id"]):
                content = "## Start with a simple picture\n\n" + introduction + "\n\n" + content
            content = content.replace("## Model and assumptions", "## Understand the idea")
            content = content.replace(
                "## Implementation and interpretation", "## Put the idea into practice"
            )
            content = content.replace("## Research protocol", "## Work through it yourself")
            content = re.sub(
                r"\[[^\]]+\]\(/curriculum/([a-z0-9-]+)\)", current_course_link, content
            )
            if lesson["id"] == "0.8":
                content = content.replace(
                    "| Business value and a margin of safety |",
                    "| Patient habits and an investment plan | "
                    "[The intelligent & careful investor](/curriculum/intelligent-investor) |\n"
                    "| Business value and a margin of safety |",
                )
            lesson["content"] = content
            terms = vocabulary_for(lesson, course["id"])
            if terms:
                lesson["terms"] = terms
