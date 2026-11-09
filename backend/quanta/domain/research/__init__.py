"""Research platform: the computation behind a registered experiment.

A run takes one strategy, one dataset and a declared parameter grid and tries
to disprove the result: out-of-sample validation, parameter robustness,
transaction-cost stress, benchmarks, overfitting statistics and a look-ahead
test, gathered into a red-team verdict. Every backtest here goes through
`quanta.domain.analytics.backtest`; nothing in this package re-implements
execution. Modules are pure: the service injects the sandbox runner, the data
and the progress callback, and owns persistence.
"""
