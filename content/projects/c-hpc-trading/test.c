#include "quanta.h"
#include <assert.h>
#include <stdio.h>

int main(void) {
    QAccount a = {10000, 0};
    assert(q_target(&a, 2, 1000, 5) && a.cash == 7995 && a.shares == 2);
    assert(q_target(&a, 2, 1500, 5) && a.cash == 7995); /* no second fee */
    assert(!q_target(&a, 20, 1000, 5) && a.cash == 7995 && a.shares == 2);
    assert(!q_target(&a, INT64_MAX, INT64_MAX, 5) && a.cash == 7995);
    assert(!q_target(&a, -1, 1000, 5));
    assert(!q_target(&a, 0, 0, 5));
    assert(q_target(&a, 0, 1100, 5) && a.cash == 10190 && a.shares == 0);
    a = (QAccount){Q_MAX_CASH, 1};
    assert(!q_target(&a, 0, 1000, 5) && a.cash == Q_MAX_CASH && a.shares == 1);

    /* Close[1] crosses SMA, buy at open[2]=130, not close[1]=120.
       Sell at open[3]=90: 1,000,000 - 130 - 5 + 90 - 5 = 999,950. */
    QBar fixture[] = {{100, 100}, {100, 120}, {130, 80}, {90, 80}};
    QResult r = q_backtest(fixture, 4, 2);
    assert(r.ok && r.fills == 2 && r.equity == 999950);
    r = q_backtest(fixture, 2, 2);
    assert(r.ok && r.fills == 0 && r.equity == 1000000); /* terminal signal unfilled */
    r = q_backtest(fixture, 4, 4);
    assert(r.ok && r.fills == 0);
    assert(!q_backtest(fixture, 4, 0).ok);
    assert(!q_backtest(fixture, 4, 5).ok);
    fixture[3].close = -1;
    assert(!q_backtest(fixture, 4, 2).ok);
    fixture[3].close = Q_MAX_PRICE + 1;
    assert(!q_backtest(fixture, 4, 2).ok);

    QBar bars[2000], duplicate[2000];
    assert(q_generate(bars, 2000, 42) && q_generate(duplicate, 2000, 42));
    for (size_t i = 0; i < 2000; ++i)
        assert(bars[i].open == duplicate[i].open &&
               bars[i].close == duplicate[i].close);
    size_t windows[] = {2, 3, 5, 8, 13, 21, 34};
    QResult serial[7], parallel[7];
    assert(q_sweep(bars, 2000, windows, 7, 1, serial));
    for (size_t threads = 2; threads <= Q_MAX_THREADS; ++threads) {
        assert(q_sweep(bars, 2000, windows, 7, threads, parallel));
        assert(q_equal(serial, parallel, 7));
    }
    bars[10].open = 0;
    assert(!q_sweep(bars, 2000, windows, 7, 3, parallel));
    assert(q_equal(serial, parallel, 7)); /* failure publishes no partial result */
    assert(!q_sweep(bars, 2000, windows, 7, 0, parallel));
    assert(!q_sweep(bars, 2000, windows, 7, 33, parallel));
    puts("PASS: ledger, risk rejection, causality, warmup, bounds, seed, parallel "
         "equality and atomic publication");
    return 0;
}
