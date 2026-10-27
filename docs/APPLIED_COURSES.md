# Expanded applied courses

The catalog now has nine courses, **216 lessons, 436 practice questions, 400 exam questions, and 52 assessments**. Original beginner, book-course, strategy, simulator, saved-work, and attribution behavior remains available.

| Route | Lessons / units | Practice | Checkpoints + final | Final threshold |
| --- | --- | --- | --- | --- |
| `/curriculum/stock-bots` | 48 / 12 | 96 | 11 + 48 questions | 39/48; version 3 |
| `/curriculum/econometrics` | 32 / 8 | 64 | 7 + 32 questions | 26/32; version 2 |
| `/curriculum/web3` | 24 / 6 | 48 | 5 + 24 questions | 20/24; version 2 |
| `/curriculum/stock-machine-learning` | 24 / 6 | 48 | 5 + 24 questions | 20/24; version 1 |

Checkpoints contain four independent transfer questions and require three correct. Every applied lesson has a worked case, display equation, guided worksheet, two practice items, assignment and worked solution, and named primary references. The common source footer covers course, lesson, and exam routes.

## Machine learning for stocks: twelve hours

Each of 24 lessons allocates 30 minutes: eight for lesson/primary reading, eight for reproducing the calculation, and fourteen for the project assignment and review. Six two-hour units cover data quality; features/labels/splits; training; selection/evaluation; diagnosis/repair; and inference/monitoring/capstone. This is an active-study estimate, with assessment time additional.

The [project source and guide](../content/projects/stock-ml/README.md) implement real ridge, random forest, and logistic fits. The flow is synthetic raw observations → validated and audited data → dated features/labels → purged chronological partitions → training-only preprocessing → validation selection → development refit → held-out metrics → saved pipelines/model card → trusted local batch inference. Latest eligible feature rows can be scored without future labels.

The report preserves unsuccessful models, mean/prior baselines, undefined metric conventions, calibration bins, descriptive input shifts, and a declared opportunity-return proxy. Neural/boosting extensions, nested walk-forward experiments, post-hoc calibration, feature inspection, and dependent uncertainty are explicit learner assignments; the default project does not pretend to have executed them. No hosted inference or broker authority is created.

## Econometrics and advanced algorithms

Econometrics expands the original five identities into 40 ordered lessons in ten units covering estimands, dated financial data, OLS, sampling uncertainty, heteroskedasticity, HAC, specification, stationarity, ARIMA, VAR, cointegration, error correction, GARCH/asymmetry, factor models, portfolio estimation, shrinkage/PCA, panel fixed effects, IV/2SLS, DiD, binary outcomes, tails, bootstrap, and selection, then an advanced pair of units: maximum likelihood and the Wald/LR/score trinity, GMM and Hansen's J, GRS/Fama–MacBeth/Shanken asset-pricing tests, persistent-predictor (Stambaugh) bias, structural breaks and Markov switching, the Kalman filter for time-varying beta, quantile regression for conditional VaR, and extreme value theory.

The [research project guide](../public/course-assets/research/README.md) distinguishes actual OLS/HAC and cointegration estimation from fixed-parameter GARCH and stipulated covariance scenarios. It also supports the bot expansion's universe ranking, queue matching, strict interval purging, fractional long-only next-open accounting, and evidence-set evaluation. Conditional factor explanation with realized future factors is explicitly not an ex-ante forecast.

## Cryptography and coin creation

The [coin project guide](../content/projects/web3/README.md) includes a standard-library Node native chain and a locked Solidity/ERC-20 project. The native chain uses Ed25519, SHA-256 commitments, account nonces, a small proof-of-work fixture, atomic rejection, independent replay, and a capped issuance rule. It omits a public peer network and fork choice.

The token test compiles the original CedarCoin wrapper with OpenZeppelin, deploys into an in-process EVM, checks metadata/supply/transfers/finite allowances, rejects invalid spending, and matches runtime bytes to compilation. There is no external RPC, public deployment, wallet connection, sale, or market pool. Source attribution and dependency licenses remain visible in the downloadable guide.

## Authoring and verification commands

```sh
python3 content/authoring/curriculum.py
python3 content/scripts/package_projects.py
npm test
npm run test:api
npm run build
backend/.venv/bin/python -m pip install -r content/projects/stock-ml/requirements.txt
backend/.venv/bin/python -m unittest discover -s content/projects/stock-ml -v
npm ci --ignore-scripts --prefix content/projects/web3
npm test --prefix content/projects/web3
TEST_URL=http://127.0.0.1:8088 npm run test:e2e
```

The catalog generator preserves legacy first-practice keys for retained IDs. Bot final versions 1/2 and econometrics/Web3 version 1 remain historical and cannot satisfy the expanded final. Project grading is separate from automatic concept-exam grading. See [verification evidence](VERIFICATION.md) for actual runs and any limitations.
