# Harbor paper-bot lab

An original Quanta teaching project for **Algorithmic & AI stock bots**, lessons 5.29–5.32. All prices, companies, filings, and outcomes are fictional. Python 3.10+ and its standard library are sufficient. No credentials, network access, broker account, or AI provider are used.

## Run and inspect

Download `paper_bot_lab.py` into a local directory. Run:

```sh
python3 paper_bot_lab.py
```

The default run uses a temporary SQLite file, closes/reopens it during the replay, prints JSON, and removes the temporary directory. To keep your work, choose a new database filename:

```sh
python3 paper_bot_lab.py --db harbor.sqlite
python3 paper_bot_lab.py --db harbor.sqlite --report
```

The demo refuses to replay into a database that already contains orders. Use another filename for a fresh experiment. Import `PaperBot`, `ridge_walkforward`, and `validate_fact` to write your own fixtures.

## What actually runs

1. A fixed past-close rule proposes ten HBR shares. A later event fills four at $100; a duplicate event has no effect.
2. The process reopens the database. Six more shares fill at $99. Replaying the original fill has no effect.
3. A persistent halt blocks a new buy after another restart. A two-share reduction sells at $102 while new risk remains halted.
4. Two expanding-window ridge regressions fit artificial observations and predict the next row. Their training means and coefficients are computed from training rows only.
5. A fixed AI response fixture is checked against fictional source evidence and produces verified revenue and growth. This tests the validator, not a language model's accuracy.

Expected paper report at a $102 mark:

| Field | Expected |
| --- | ---: |
| Cash | 920939 cents ($9,209.39) |
| Shares | 8 |
| Equity | 1002539 cents ($10,025.39) |
| P&L | 2539 cents ($25.39) |
| Commissions | 61 cents ($0.61) |
| Fill records | 3 |
| Open orders | 0 |

The halt reason remains `incident rehearsal`. Ridge MSE is approximately `0.495982553`; its training-mean baseline MSE is `30.5`. Verified revenue is `120` USD million; computed growth is approximately `0.20`. These results do not estimate trading profitability.

## Model and policy assumptions

- One fictional symbol, long-only integer shares, integer-cent prices, immediate settlement, and no borrowing or leverage.
- Limit orders fill only on a later eligible market event, at its supplied price, if the limit permits it. Shared eligible volume caps the total fill across orders. Ordering is local creation order, not an exchange queue model.
- Five-basis-point commission is rounded upward to a cent for each fill. Buy reservations include a conservative per-share fee buffer to cover fragmented fills. Canceled remainders release reservations without changing existing inventory.
- Illustrative limits: 100 shares, $5,000 projected name notional, 500 ms quote freshness, and a supplied session-open flag. There is no exchange calendar. Existing holdings can move past a notional cap due to price changes; the lab gates new orders and does not automatically liquidate them.
- Stable IDs reject conflicting payload reuse. SQLite transactions keep local ledger changes atomic. Local idempotency does not guarantee exactly-once submission to an external broker.
- Cancellation is synchronous in this matcher. Actual broker cancel races, uncertain external writes, market impact, queue priority, slippage beyond the stipulated event, corporate actions, settlement, and market-data licensing require separate work.
- The artificial ML example has six rows, two evaluation predictions, fixed penalty one, and no stock-return data. It is a pipeline fixture, not meaningful evidence of market skill.
- The AI validator accepts only the specified revenue field and exact evidence contract. It does not parse arbitrary filings, perform RAG, call a provider, or expose a trading tool.

## Exercises and acceptance

Create separate fixtures for duplicate and conflicting identities, a partial fill followed by cancellation, insufficient fee-inclusive cash, a price that cannot fill the limit, future/stale quotes, a closed session, a restart while halted, and an explicit resume. Capture state before and after each rejected action.

For ML, reproduce the two fold predictions and show that changing the final held-out outcome changes only its evaluation error. For AI, test unknown source, unavailable source, wrong unit, wrong issuer, nonfinite number, missing field, and extra instruction field.

Submit the decision contract, data/feature dictionary, order-state diagram, risk policy, split manifest, evidence-test matrix, runbook, output, and completed lesson 5.32 rubric. Passing the multiple-choice final does not grade this dossier. Cash/share conservation, deduplication, persistent halts, and source validation are mandatory acceptance conditions.

## References and attribution

The code, fixtures, and course assignments are original Quanta material. Related primary sources:

- [Alpaca: working with orders](https://docs.alpaca.markets/us/docs/working-with-orders) — order identities and lifecycle terminology; this lab is not an Alpaca adapter.
- [Alpaca: paper trading](https://docs.alpaca.markets/us/docs/paper-trading) — simulation limitations to consider when reviewing paper results.
- [Python Software Foundation: sqlite3](https://docs.python.org/3/library/sqlite3.html) — local transactions and connection behavior.
- [scikit-learn contributors: common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html) — training-only transformations and evaluation leakage.
- [Anthropic: building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — bounded workflows and tool interfaces.

References identify related methods and do not imply affiliation or endorsement. Follow each source's license when reusing its text or code; attribution alone is not reproduction permission.
