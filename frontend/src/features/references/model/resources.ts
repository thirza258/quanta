/**
 * Curated books, courses, data and tools for learning beyond Quanta, grouped by cost.
 * Every link and access statement was checked against the provider's own page on
 * RESOURCES_CHECKED. Prices change, so entries describe access terms, never prices.
 */
export type ResourceTier = "free" | "freemium" | "paid";
export type ResourceKind =
  | "book"
  | "course"
  | "documentation"
  | "data"
  | "research"
  | "platform"
  | "program";
export type ResourceLevel = "beginner" | "intermediate" | "advanced";
export type ResourceTopic =
  | "markets"
  | "statistics"
  | "machine-learning"
  | "strategies"
  | "microstructure"
  | "programming"
  | "hpc"
  | "crypto"
  | "data"
  | "careers";

export type LearningResource = {
  id: string;
  title: string;
  creator: string;
  kind: ResourceKind;
  tier: ResourceTier;
  level: ResourceLevel;
  topics: ResourceTopic[];
  description: string;
  /** How the material is obtained, as stated by the provider. */
  access: string;
  url: string;
  /** Quanta course IDs this resource extends. */
  courses: string[];
};

export const RESOURCES_CHECKED = "5 October 2026";

export const tierLabels: Record<ResourceTier, string> = {
  free: "Free",
  freemium: "Free with paid options",
  paid: "Paid",
};

export const tierDescriptions: Record<ResourceTier, string> = {
  free: "Read, watch, or download the full material at no cost. Some also sell print copies or certificates.",
  freemium:
    "A substantial free part, such as lectures, code, or a free account, with paid extras alongside.",
  paid: "Books, subscriptions, and professional programs that require a purchase or fee.",
};

export const kindLabels: Record<ResourceKind, string> = {
  book: "Book",
  course: "Course",
  documentation: "Documentation",
  data: "Data",
  research: "Research archive",
  platform: "Platform",
  program: "Program",
};

export const levelLabels: Record<ResourceLevel, string> = {
  beginner: "Beginner",
  intermediate: "Intermediate",
  advanced: "Advanced",
};

export const topicLabels: Record<ResourceTopic, string> = {
  markets: "Markets & investing",
  statistics: "Statistics & econometrics",
  "machine-learning": "Machine learning",
  strategies: "Strategies & portfolios",
  microstructure: "Market microstructure",
  programming: "Programming & tools",
  hpc: "High-performance computing",
  crypto: "Crypto & cryptography",
  data: "Data & research",
  careers: "Qualifications",
};

export const learningResources: LearningResource[] = [
  // Free
  {
    id: "fpp3",
    title: "Forecasting: Principles and Practice (3rd edition)",
    creator: "Rob J. Hyndman & George Athanasopoulos",
    kind: "book",
    tier: "free",
    level: "intermediate",
    topics: ["statistics"],
    description:
      "A practical forecasting textbook covering time-series graphics, decomposition, exponential smoothing, ARIMA, regression and forecast evaluation, with exercises in every chapter.",
    access: "Free online textbook.",
    url: "https://otexts.com/fpp3/",
    courses: ["econometrics", "statistical-foundations"],
  },
  {
    id: "isl",
    title: "An Introduction to Statistical Learning",
    creator: "James, Witten, Hastie, Tibshirani & Taylor",
    kind: "book",
    tier: "free",
    level: "beginner",
    topics: ["machine-learning", "statistics"],
    description:
      "An accessible introduction to the main statistical-learning methods, from linear models to tree ensembles. Read it before the machine-learning courses.",
    access: "Free download from the authors, in R and Python editions.",
    url: "https://www.statlearning.com/",
    courses: ["stock-machine-learning", "statistical-foundations"],
  },
  {
    id: "esl",
    title: "The Elements of Statistical Learning (2nd edition)",
    creator: "Trevor Hastie, Robert Tibshirani & Jerome Friedman",
    kind: "book",
    tier: "free",
    level: "advanced",
    topics: ["machine-learning", "statistics"],
    description:
      "The advanced companion to the introductory book, with the mathematics behind supervised and unsupervised learning methods.",
    access: "Free PDF from the authors (corrected 12th printing).",
    url: "https://hastie.su.domains/ElemStatLearn/",
    courses: ["stock-machine-learning"],
  },
  {
    id: "pml",
    title: "Probabilistic Machine Learning: An Introduction",
    creator: "Kevin P. Murphy",
    kind: "book",
    tier: "free",
    level: "advanced",
    topics: ["machine-learning"],
    description:
      "A modern probabilistic treatment of machine learning, from foundations to deep networks. Useful for understanding uncertainty, calibration and model comparison.",
    access:
      "Free draft PDF under a Creative Commons licence; hardcopy from MIT Press.",
    url: "https://probml.github.io/pml-book/book1.html",
    courses: ["stock-machine-learning"],
  },
  {
    id: "deep-learning",
    title: "Deep Learning",
    creator: "Ian Goodfellow, Yoshua Bengio & Aaron Courville",
    kind: "book",
    tier: "free",
    level: "advanced",
    topics: ["machine-learning"],
    description:
      "A comprehensive textbook on deep learning, from the mathematical background to modern practice. Read it before trusting any deep model on stock data.",
    access: "Free to read online; a print edition is sold separately.",
    url: "https://www.deeplearningbook.org/",
    courses: ["stock-machine-learning"],
  },
  {
    id: "mml",
    title: "Mathematics for Machine Learning",
    creator: "Marc Peter Deisenroth, A. Aldo Faisal & Cheng Soon Ong",
    kind: "book",
    tier: "free",
    level: "intermediate",
    topics: ["statistics", "machine-learning"],
    description:
      "Linear algebra, calculus, probability and optimization written for readers who want the mathematics behind regression, PCA and classifiers.",
    access: "Free PDF from the authors.",
    url: "https://mml-book.github.io/",
    courses: ["statistical-foundations", "stock-machine-learning"],
  },
  {
    id: "python-data-analysis",
    title: "Python for Data Analysis (3rd edition)",
    creator: "Wes McKinney",
    kind: "book",
    tier: "free",
    level: "beginner",
    topics: ["programming", "data"],
    description:
      "A practical guide to data analysis in Python centred on pandas: the loading, cleaning and reshaping work behind every backtest.",
    access:
      "Free Open Access HTML edition; print and e-book formats are sold separately.",
    url: "https://wesmckinney.com/book/",
    courses: ["strategy-lab", "stock-bots", "stock-machine-learning"],
  },
  {
    id: "quantecon",
    title: "QuantEcon lectures",
    creator: "Thomas J. Sargent & John Stachurski",
    kind: "course",
    tier: "free",
    level: "intermediate",
    topics: ["programming", "statistics"],
    description:
      "A lecture series on Python programming for economics and finance, with code you can run and adapt.",
    access: "Free online lectures.",
    url: "https://quantecon.org/lectures/",
    courses: ["statistical-foundations", "econometrics"],
  },
  {
    id: "causal-remix",
    title: "Causal Inference: The Remix",
    creator: "Scott Cunningham",
    kind: "book",
    tier: "free",
    level: "intermediate",
    topics: ["statistics"],
    description:
      "An accessible guide to research designs that separate cause from correlation: instrumental variables, difference-in-differences, regression discontinuity and more.",
    access: "Free online edition.",
    url: "https://mixtape.scunning.com/",
    courses: ["econometrics"],
  },
  {
    id: "tidy-finance",
    title: "Tidy Finance",
    creator: "Christoph Scheuch, Stefan Voigt, Patrick Weiss & Christoph Frey",
    kind: "book",
    tier: "free",
    level: "intermediate",
    topics: ["data", "strategies", "programming"],
    description:
      "Reproducible empirical finance in R and Python, covering factor construction, portfolio sorts and beta estimation, with the code behind every result.",
    access: "Open-source online book.",
    url: "https://www.tidy-finance.org/",
    courses: ["econometrics", "strategy-lab"],
  },
  {
    id: "damodaran",
    title: "Damodaran Online",
    creator: "Aswath Damodaran · NYU Stern",
    kind: "data",
    tier: "free",
    level: "intermediate",
    topics: ["markets", "data"],
    description:
      "Industry, regional and company-level data sets compiled by NYU Stern's Aswath Damodaran, useful as inputs and sanity checks for valuation work.",
    access: "Free data sets.",
    url: "https://pages.stern.nyu.edu/~adamodar/",
    courses: ["security-analysis", "news-to-markets", "intelligent-investor"],
  },
  {
    id: "algorithmica",
    title: "Algorithms for Modern Hardware",
    creator: "Sergey Slotin",
    kind: "book",
    tier: "free",
    level: "advanced",
    topics: ["hpc", "programming"],
    description:
      "How caches, branch prediction and SIMD shape real running time, with measured examples. A practical companion to the C and HPC course.",
    access: "Free online book.",
    url: "https://en.algorithmica.org/hpc/",
    courses: ["c-hpc-trading"],
  },
  {
    id: "modern-c",
    title: "Modern C",
    creator: "Jens Gustedt",
    kind: "book",
    tier: "free",
    level: "intermediate",
    topics: ["programming", "hpc"],
    description:
      "A contemporary textbook on the C language, now in a C23 edition, for programmers who want to write modern, standard C.",
    access:
      "Free download under a Creative Commons licence; a print version is sold separately.",
    url: "https://gustedt.gitlabpages.inria.fr/modern-c/",
    courses: ["c-hpc-trading"],
  },
  {
    id: "art-of-hpc",
    title: "The Art of HPC",
    creator: "Victor Eijkhout · TACC",
    kind: "book",
    tier: "free",
    level: "advanced",
    topics: ["hpc"],
    description:
      "Textbooks on scientific computing and parallel programming, including MPI and OpenMP.",
    access: "Free PDF and HTML editions; paper copies are for sale.",
    url: "https://theartofhpc.com/",
    courses: ["c-hpc-trading"],
  },
  {
    id: "drepper-memory",
    title: "What Every Programmer Should Know About Memory",
    creator: "Ulrich Drepper",
    kind: "book",
    tier: "free",
    level: "advanced",
    topics: ["hpc"],
    description:
      "The classic long paper on CPU caches, memory bandwidth and non-uniform memory access (NUMA). It explains why data layout can matter more than arithmetic in a research engine.",
    access: "Free PDF.",
    url: "https://www.akkadia.org/drepper/cpumemory.pdf",
    courses: ["c-hpc-trading"],
  },
  {
    id: "mastering-bitcoin",
    title: "Mastering Bitcoin (3rd edition)",
    creator: "Andreas M. Antonopoulos & David A. Harding",
    kind: "book",
    tier: "free",
    level: "intermediate",
    topics: ["crypto"],
    description:
      "A technical guide to how Bitcoin works, written for developers.",
    access:
      "Free to read on GitHub under a Creative Commons Attribution-ShareAlike licence.",
    url: "https://github.com/bitcoinbook/bitcoinbook",
    courses: ["web3"],
  },
  {
    id: "mastering-ethereum",
    title: "Mastering Ethereum (2nd edition)",
    creator: "Andreas M. Antonopoulos, Gavin Wood et al.",
    kind: "book",
    tier: "free",
    level: "intermediate",
    topics: ["crypto"],
    description:
      "A technical guide to Ethereum and smart contracts, written for developers, and a deeper reference for the Web3 course's token project.",
    access: "Free to read online under a Creative Commons licence.",
    url: "https://github.com/ethereumbook/ethereumbook",
    courses: ["web3"],
  },
  {
    id: "bitcoin-technologies",
    title: "Bitcoin and Cryptocurrency Technologies",
    creator: "Narayanan, Bonneau, Felten, Miller & Goldfeder",
    kind: "book",
    tier: "free",
    level: "intermediate",
    topics: ["crypto"],
    description:
      "A Princeton textbook on how cryptocurrencies achieve decentralization, covering mining incentives, anonymity, and the limits of each design choice.",
    access:
      "Free pre-publication draft; the published book is from Princeton University Press.",
    url: "https://bitcoinbook.cs.princeton.edu/",
    courses: ["web3"],
  },
  {
    id: "applied-crypto",
    title: "A Graduate Course in Applied Cryptography",
    creator: "Dan Boneh & Victor Shoup",
    kind: "book",
    tier: "free",
    level: "advanced",
    topics: ["crypto"],
    description:
      "Rigorous foundations of modern cryptography for learners who want the proofs behind the Web3 course's hashes and signatures.",
    access: "Free download from the authors.",
    url: "https://toc.cryptobook.us/",
    courses: ["web3"],
  },
  {
    id: "mit-18s096",
    title: "Topics in Mathematics with Applications in Finance",
    creator: "MIT OpenCourseWare · 18.S096",
    kind: "course",
    tier: "free",
    level: "advanced",
    topics: ["statistics", "markets"],
    description:
      "MIT's course on mathematical methods used in finance, with lecture notes, case studies, video lectures and assignments.",
    access: "Free lecture notes, video lectures and assignments.",
    url: "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/",
    courses: ["statistical-foundations", "econometrics"],
  },
  {
    id: "mit-15401",
    title: "Finance Theory I",
    creator: "MIT OpenCourseWare · 15.401",
    kind: "course",
    tier: "free",
    level: "beginner",
    topics: ["markets"],
    description:
      "MIT Sloan's introductory finance course, covering present value, risk and capital budgeting: a solid foundation for the valuation courses.",
    access: "Free readings, problem sets and exams.",
    url: "https://ocw.mit.edu/courses/15-401-finance-theory-i-fall-2008/",
    courses: [
      "trading-fundamentals",
      "intelligent-investor",
      "security-analysis",
    ],
  },
  {
    id: "missing-semester",
    title: "The Missing Semester of Your CS Education",
    creator: "MIT CSAIL",
    kind: "course",
    tier: "free",
    level: "beginner",
    topics: ["programming"],
    description:
      "The command line, version control, editors, debugging and automation, the tools that make research projects reproducible.",
    access: "Free lectures and notes.",
    url: "https://missing.csail.mit.edu/",
    courses: ["stock-bots", "c-hpc-trading"],
  },
  {
    id: "fast-ai",
    title: "Practical Deep Learning for Coders",
    creator: "fast.ai",
    kind: "course",
    tier: "free",
    level: "intermediate",
    topics: ["machine-learning", "programming"],
    description:
      "For people who can already code and want to apply deep learning and machine learning to practical problems, including deploying models.",
    access: "Free course.",
    url: "https://course.fast.ai/",
    courses: ["stock-machine-learning"],
  },
  {
    id: "scikit-learn",
    title: "scikit-learn User Guide",
    creator: "scikit-learn developers",
    kind: "documentation",
    tier: "free",
    level: "intermediate",
    topics: ["machine-learning", "programming"],
    description:
      "Authoritative documentation for pipelines, cross-validation, metrics and models. Its common-pitfalls page is required reading before any stock-prediction experiment.",
    access: "Free documentation.",
    url: "https://scikit-learn.org/stable/user_guide.html",
    courses: ["stock-machine-learning", "strategy-lab"],
  },
  {
    id: "statsmodels",
    title: "statsmodels documentation",
    creator: "statsmodels developers",
    kind: "documentation",
    tier: "free",
    level: "intermediate",
    topics: ["statistics", "programming"],
    description:
      "Regression, robust covariance, time-series models and statistical tests in Python, with worked examples that match the econometrics lessons.",
    access: "Free documentation.",
    url: "https://www.statsmodels.org/stable/index.html",
    courses: ["econometrics", "statistical-foundations"],
  },
  {
    id: "quantlib",
    title: "QuantLib",
    creator: "QuantLib project",
    kind: "documentation",
    tier: "free",
    level: "advanced",
    topics: ["programming", "markets"],
    description:
      "A free, open-source library for modelling, pricing and risk management of financial instruments, useful for going beyond the equities focus of Quanta.",
    access: "Free and open source.",
    url: "https://www.quantlib.org/",
    courses: [],
  },
  {
    id: "fred",
    title: "FRED · Federal Reserve Economic Data",
    creator: "Federal Reserve Bank of St. Louis",
    kind: "data",
    tier: "free",
    level: "beginner",
    topics: ["data", "markets"],
    description:
      "Economic time series on growth, inflation, employment, rates and more. Its companion ALFRED keeps earlier vintages for point-in-time research.",
    access: "Free data, with an API and an Excel add-in.",
    url: "https://fred.stlouisfed.org/",
    courses: ["news-to-markets", "econometrics"],
  },
  {
    id: "french-data",
    title: "Kenneth R. French Data Library",
    creator: "Kenneth R. French · Dartmouth",
    kind: "data",
    tier: "free",
    level: "intermediate",
    topics: ["data", "strategies"],
    description:
      "Factor and portfolio returns with documented construction methods: the standard inputs for factor regressions and strategy benchmarks.",
    access: "Free data downloads.",
    url: "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html",
    courses: ["lab-workshop", "econometrics", "strategy-lab"],
  },
  {
    id: "open-asset-pricing",
    title: "Open Source Asset Pricing",
    creator: "Andrew Y. Chen & Tom Zimmermann",
    kind: "data",
    tier: "free",
    level: "advanced",
    topics: ["data", "strategies"],
    description:
      "Test-asset returns and predictive signals replicated from the academic asset-pricing literature. Use it to check whether a published anomaly reproduces before you build on it.",
    access: "Free data and code.",
    url: "https://www.openassetpricing.com/",
    courses: ["strategy-lab", "stock-machine-learning"],
  },
  {
    id: "aqr-data",
    title: "AQR Data Sets",
    creator: "AQR Capital Management",
    kind: "data",
    tier: "free",
    level: "intermediate",
    topics: ["data", "strategies"],
    description:
      "Factor return series such as momentum indices and betting-against-beta factors, useful as independent benchmarks for strategy research.",
    access: "Free downloadable spreadsheets.",
    url: "https://www.aqr.com/Insights/Datasets",
    courses: ["strategy-lab"],
  },
  {
    id: "arxiv-qfin",
    title: "arXiv · Quantitative Finance",
    creator: "arXiv",
    kind: "research",
    tier: "free",
    level: "advanced",
    topics: ["data", "strategies", "microstructure"],
    description:
      "Preprints across portfolio management, trading and microstructure, statistical finance and risk. Many research extensions in Quanta's lessons cite papers from here.",
    access: "Free preprints.",
    url: "https://arxiv.org/archive/q-fin",
    courses: ["strategy-lab", "algorithm-evaluation"],
  },
  {
    id: "shiller-data",
    title: "Shiller data",
    creator: "Robert J. Shiller",
    kind: "data",
    tier: "free",
    level: "beginner",
    topics: ["data", "markets"],
    description:
      "Long historical series of U.S. stock prices, dividends, earnings and interest rates, including the cyclically adjusted price-earnings (CAPE) ratio.",
    access: "Free data downloads.",
    url: "https://shillerdata.com/",
    courses: ["intelligent-investor", "econometrics"],
  },
  {
    id: "worldquant-university",
    title: "WorldQuant University",
    creator: "WorldQuant University",
    kind: "program",
    tier: "free",
    level: "advanced",
    topics: ["careers", "strategies"],
    description:
      "Online degrees and credentials, including a master's programme in financial engineering, for learners who want a structured, assessed path after Quanta.",
    access: "Tuition-free accredited online degrees and credentials.",
    url: "https://www.wqu.edu/",
    courses: [],
  },
  {
    id: "sikapi",
    title: "SIKAPI · Sikapi Uangmu",
    creator: "Otoritas Jasa Keuangan (OJK)",
    kind: "course",
    tier: "free",
    level: "beginner",
    topics: ["markets"],
    description:
      "The financial-literacy portal of Indonesia's financial-services regulator (in Indonesian), covering financial planning, consumer protection and investment warnings.",
    access: "Free public portal.",
    url: "https://sikapiuangmu.ojk.go.id/",
    courses: ["trading-fundamentals", "trading-ethics", "intelligent-investor"],
  },
  // Free with paid options
  {
    id: "quantconnect",
    title: "QuantConnect",
    creator: "QuantConnect",
    kind: "platform",
    tier: "freemium",
    level: "intermediate",
    topics: ["strategies", "programming"],
    description:
      "A platform for researching and backtesting algorithmic strategies, built on its LEAN engine: a natural next step after the Strategy lab.",
    access: "Free sign-up; paid plans add more data and computing resources.",
    url: "https://www.quantconnect.com/pricing",
    courses: ["lab-workshop", "strategy-lab", "stock-bots"],
  },
  {
    id: "quantra",
    title: "Quantra",
    creator: "QuantInsti",
    kind: "course",
    tier: "freemium",
    level: "beginner",
    topics: ["strategies", "programming"],
    description:
      "Short interactive courses on algorithmic and quantitative trading.",
    access: "Some free courses and free previews; most courses are paid.",
    url: "https://quantra.quantinsti.com/",
    courses: ["simulator-workshop", "stock-bots", "trading-fundamentals"],
  },
  {
    id: "statistical-rethinking",
    title: "Statistical Rethinking (2024 lectures)",
    creator: "Richard McElreath",
    kind: "course",
    tier: "freemium",
    level: "intermediate",
    topics: ["statistics"],
    description:
      "A Bayesian data-analysis course that puts scientific and causal models first. The recorded lectures pair well with the hypothesis-testing lessons.",
    access:
      "Free recorded lectures and materials; the course follows the author's separately published book.",
    url: "https://github.com/rmcelreath/stat_rethinking_2024",
    courses: ["statistical-foundations"],
  },
  {
    id: "ml-for-trading",
    title: "Machine Learning for Trading (3rd edition) · code",
    creator: "Stefan Jansen",
    kind: "book",
    tier: "freemium",
    level: "advanced",
    topics: ["machine-learning", "strategies"],
    description:
      "Notebooks covering data sourcing, features, models and walk-forward evaluation for trading strategies, from data sourcing through to live execution.",
    access:
      "The code is free under the MIT licence; the book it accompanies is published separately.",
    url: "https://github.com/stefan-jansen/machine-learning-for-trading",
    courses: ["stock-machine-learning", "stock-bots"],
  },
  {
    id: "google-colab",
    title: "Google Colaboratory",
    creator: "Google Research",
    kind: "platform",
    tier: "freemium",
    level: "beginner",
    topics: ["programming", "machine-learning"],
    description:
      "Hosted Jupyter notebooks that need no setup, a convenient place to run the downloadable Python projects and machine-learning labs when your own machine is not ready.",
    access:
      "Free of charge with usage limits; paid plans remove some restrictions.",
    url: "https://research.google.com/colaboratory/faq.html",
    courses: ["lab-workshop", "stock-machine-learning", "strategy-lab"],
  },
  {
    id: "alpha-vantage",
    title: "Alpha Vantage",
    creator: "Alpha Vantage",
    kind: "data",
    tier: "freemium",
    level: "beginner",
    topics: ["data", "programming"],
    description:
      "Market-data APIs for stock prices, technical and economic indicators, and news sentiment, useful for practising data validation on real feeds.",
    access: "Free API key; premium keys are sold separately.",
    url: "https://www.alphavantage.co/",
    courses: ["stock-bots", "news-to-markets"],
  },
  // Paid
  {
    id: "coursera-financial-markets",
    title: "Financial Markets",
    creator: "Robert Shiller · Yale University on Coursera",
    kind: "course",
    tier: "paid",
    level: "beginner",
    topics: ["markets"],
    description:
      "Robert Shiller's introduction to risk, insurance, banks, and stock and bond markets, with a behavioural-finance perspective.",
    access:
      "Included with a Coursera Plus subscription; check the course page for any free access option.",
    url: "https://www.coursera.org/learn/financial-markets-global",
    courses: ["trading-fundamentals", "intelligent-investor"],
  },
  {
    id: "afml",
    title: "Advances in Financial Machine Learning",
    creator: "Marcos López de Prado · Wiley",
    kind: "book",
    tier: "paid",
    level: "advanced",
    topics: ["machine-learning", "strategies"],
    description:
      "Machine-learning research methods for finance: structuring financial data, research and supercomputing techniques, backtesting discoveries and avoiding false positives.",
    access: "Paid book.",
    url: "https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086",
    courses: ["stock-machine-learning", "strategy-lab", "algorithm-evaluation"],
  },
  {
    id: "econometrics-financial-markets",
    title: "The Econometrics of Financial Markets",
    creator: "John Y. Campbell, Andrew W. Lo & A. Craig MacKinlay",
    kind: "book",
    tier: "paid",
    level: "advanced",
    topics: ["statistics", "markets"],
    description:
      "Graduate econometrics for markets: return predictability and random-walk tests, microstructure, event studies, CAPM and APT, the term structure, and nonlinear models such as ARCH.",
    access: "Paid book from Princeton University Press.",
    url: "https://press.princeton.edu/books/hardcover/9780691043012/the-econometrics-of-financial-markets",
    courses: ["econometrics"],
  },
  {
    id: "cochrane-asset-pricing",
    title: "Asset Pricing (revised edition)",
    creator: "John H. Cochrane",
    kind: "book",
    tier: "paid",
    level: "advanced",
    topics: ["statistics", "strategies"],
    description:
      "A unified, stochastic-discount-factor view of asset pricing and the empirical methods used to test it.",
    access: "Paid book from Princeton University Press.",
    url: "https://press.princeton.edu/books/hardcover/9780691121376/asset-pricing",
    courses: ["econometrics", "strategy-lab"],
  },
  {
    id: "efficiently-inefficient",
    title: "Efficiently Inefficient",
    creator: "Lasse Heje Pedersen",
    kind: "book",
    tier: "paid",
    level: "intermediate",
    topics: ["strategies", "markets"],
    description:
      "How hedge-fund strategies such as value, momentum, arbitrage and macro actually make and lose money, illuminated by interviews with leading managers.",
    access: "Paid book from Princeton University Press.",
    url: "https://press.princeton.edu/books/hardcover/9780691166193/efficiently-inefficient",
    courses: ["strategy-lab"],
  },
  {
    id: "mostly-harmless",
    title: "Mostly Harmless Econometrics",
    creator: "Joshua D. Angrist & Jörn-Steffen Pischke",
    kind: "book",
    tier: "paid",
    level: "intermediate",
    topics: ["statistics"],
    description:
      "An empiricist's guide to regression, instrumental variables, difference-in-differences and inference, focused on what each design can and cannot identify.",
    access: "Paid book from Princeton University Press.",
    url: "https://press.princeton.edu/books/paperback/9780691120355/mostly-harmless-econometrics",
    courses: ["econometrics"],
  },
  {
    id: "csapp",
    title: "Computer Systems: A Programmer's Perspective (3rd edition)",
    creator: "Randal E. Bryant & David R. O'Hallaron",
    kind: "book",
    tier: "paid",
    level: "intermediate",
    topics: ["hpc", "programming"],
    description:
      "A systems textbook explaining how programs actually execute on hardware: background for the performance work in the C course.",
    access: "Paid textbook; the authors' site has companion material.",
    url: "https://csapp.cs.cmu.edu/",
    courses: ["c-hpc-trading"],
  },
  {
    id: "hull-derivatives",
    title: "Options, Futures, and Other Derivatives (11th edition)",
    creator: "John C. Hull · Pearson",
    kind: "book",
    tier: "paid",
    level: "intermediate",
    topics: ["markets"],
    description:
      "The standard derivatives text: futures, swaps, option strategies, binomial trees, Black-Scholes-Merton, the Greeks and volatility smiles.",
    access: "Paid textbook and eTextbook.",
    url: "https://www.pearson.com/en-us/subject-catalog/p/options-futures-and-other-derivatives/P200000005938",
    courses: [],
  },
  {
    id: "trades-quotes-prices",
    title: "Trades, Quotes and Prices",
    creator: "Bouchaud, Bonart, Donier & Gould · Cambridge University Press",
    kind: "book",
    tier: "paid",
    level: "advanced",
    topics: ["microstructure"],
    description:
      "Financial markets under the microscope: limit order books, price impact, liquidity and optimal execution, grounded in data.",
    access: "Paid book.",
    url: "https://www.cambridge.org/core/books/trades-quotes-and-prices/029A71078EE4C41C0D5D4574211AB1B5",
    courses: ["simulator-workshop", "stock-bots", "trading-fundamentals"],
  },
  {
    id: "cfa-program",
    title: "CFA Program",
    creator: "CFA Institute",
    kind: "program",
    tier: "paid",
    level: "advanced",
    topics: ["careers", "markets"],
    description:
      "The professional charter for investment analysts, with a curriculum that spans ethical standards and valuation.",
    access: "Paid exam program.",
    url: "https://www.cfainstitute.org/programs/cfa-program",
    courses: ["trading-ethics", "security-analysis", "statistical-foundations"],
  },
  {
    id: "cqf",
    title: "Certificate in Quantitative Finance (CQF)",
    creator: "CQF Institute",
    kind: "program",
    tier: "paid",
    level: "advanced",
    topics: ["careers", "machine-learning"],
    description:
      "A part-time professional qualification in quantitative finance whose syllabus includes risk and machine learning.",
    access: "Paid professional qualification.",
    url: "https://www.cqf.com/",
    courses: ["strategy-lab", "stock-machine-learning"],
  },
  {
    id: "frm",
    title: "Financial Risk Manager (FRM)",
    creator: "GARP",
    kind: "program",
    tier: "paid",
    level: "advanced",
    topics: ["careers", "statistics"],
    description:
      "A professional certification in risk management covering market, credit and operational risk and quantitative analysis.",
    access: "Paid exam program.",
    url: "https://www.garp.org/frm",
    courses: ["statistical-foundations", "algorithm-evaluation"],
  },
];
