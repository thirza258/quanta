#ifndef QUANTA_H
#define QUANTA_H
#include <stddef.h>
#include <stdint.h>

/* All prices/cash are integer cents. Synthetic, long/cash research only. */
#define Q_MAX_BARS 1000000U
#define Q_MAX_PRICE INT64_C(1000000000)
#define Q_MAX_CASH INT64_C(1000000000000)
#define Q_MAX_SHARES INT64_C(1000000)
#define Q_MAX_JOBS 256U
#define Q_MAX_THREADS 32U

typedef struct {
    int64_t open, close;
} QBar;
typedef struct {
    int64_t cash, shares;
} QAccount;
typedef struct {
    size_t window;
    int64_t equity;
    size_t fills;
    int ok;
} QResult;

int q_generate(QBar *bars, size_t count, uint32_t seed);
/* Rejected targets leave the account unchanged. Fee is cents per fill. */
int q_target(QAccount *account, int64_t target, int64_t price, int64_t fee);
/* Signal at close t can only execute at open t+1; no forced final fill. */
QResult q_backtest(const QBar *bars, size_t count, size_t window);
/* Each worker owns disjoint result indices; input bars stay immutable. */
int q_sweep(const QBar *bars, size_t count, const size_t *windows, size_t jobs,
            size_t threads, QResult *results);
int q_equal(const QResult *a, const QResult *b, size_t count);
#endif
