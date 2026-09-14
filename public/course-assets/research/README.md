# Quantitative research and advanced bot lab

Original Quanta educational code. All default observations are synthetic; the script uses no broker, market feed, model API, or credentials.

Use Python 3.12+ and the accompanying pinned requirements in a fresh environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python quant_research_lab.py > research-report.json
```

The report contains actual OLS estimation with conventional and Newey–West HAC covariance, an Engle–Granger diagnostic on a planted synthetic relation, a fitted spread AR model, a fixed-parameter GARCH recursion, a stipulated covariance comparison, interval-purged splits, ranked targets, price-time ask matching, next-open multi-asset accounting, and evidence-set metrics.

| Component | Independent baseline check | Scope |
| --- | --- | --- |
| Factor fit | 270 training and 90 held-out rows; changing only held-out outcomes must leave coefficients and predictions unchanged | Conditional explanation using realized future factors, not an ex-ante factor forecast |
| Cointegration | Planted slope 1.5; fitted values and p-value are reported, not hardcoded | Full-sample synthetic diagnostic, no pairs execution |
| GARCH | Variances .04, .051, .0548 | Stipulated parameters; not maximum-likelihood fitting |
| Covariance | Sample variance .0415; shrunk .037; stressed volatility .25 | Fixed matrices and weights, no optimization |
| Purging | Origin 6 retains indices 0–3; origin 9 retains 0–6 | Strict label-end-before-origin rule |
| Ranking | B .4, A .4, cash .2; C is outside the eligible universe | Equal selected weights under a per-name cap |
| Ask queue | Three shares from `early`, two from `later`, average 100 | Price-time priority for displayed asks only |
| Next-open accounting | 1,100 cash buys ten shares at 110 and exits at 120: equity 1,200 before fees | Fractional long-only positions, immediate settlement, unlimited liquidity, conservative fee reserve |
| Evidence | Precision 2/3, recall .5 | Sets of externally labeled evidence IDs; no semantic truth verification |

For econometrics lessons 3.29–3.32, preserve the estimation configuration, data dictionary, report, negative control, and inference interpretation. For advanced bot lesson 5.48, create separate adverse cases for a long overlapping label, thin queue liquidity, higher execution costs, and an invented evidence identifier. Attach those results to the existing paper-bot dossier.

Never infer real profitability from these fixtures. The in-app Python worksheets reproduce small arithmetic cases and keep their sandbox in cash; the downloaded project runs the full local routines.

Primary references: [statsmodels regression](https://www.statsmodels.org/stable/regression.html), [Engle–Granger test](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.coint.html), [arch volatility models](https://arch.readthedocs.io/en/latest/univariate/univariate_volatility_modeling.html), [chronological splits](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html), [Alpaca order semantics](https://docs.alpaca.markets/us/docs/working-with-orders). These authors supply the referenced methods and documentation; Quanta's fixtures and explanations are original.
