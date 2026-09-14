#include "quanta.h"

int q_generate(QBar *bars, size_t count, uint32_t seed) {
    if (!bars || count == 0 || count > Q_MAX_BARS)
        return 0;
    int64_t close = 10000;
    for (size_t i = 0; i < count; ++i) {
        /* Unsigned wrap is intentional and defined; no shared RNG state. */
        seed = seed * UINT32_C(1664525) + UINT32_C(1013904223);
        int64_t open = close + (int64_t)(seed % 101U) - 50;
        if (open < 100)
            open = 100;
        seed = seed * UINT32_C(1664525) + UINT32_C(1013904223);
        close = open + (int64_t)(seed % 201U) - 100;
        if (close < 100)
            close = 100;
        bars[i] = (QBar){open, close};
    }
    return 1;
}

int q_target(QAccount *a, int64_t target, int64_t price, int64_t fee) {
    if (!a || a->cash < 0 || a->cash > Q_MAX_CASH || a->shares < 0 ||
        a->shares > Q_MAX_SHARES || target < 0 || target > Q_MAX_SHARES || price <= 0 ||
        price > Q_MAX_PRICE || fee < 0 || fee > Q_MAX_CASH)
        return 0;
    int64_t delta = target - a->shares;
    if (delta == 0)
        return 1; /* Repeating an already-filled target is a no-op. */
    /* Validated maxima bound this product by 10^15, below INT64_MAX. */
    int64_t amount = (delta > 0 ? delta : -delta) * price;
    int64_t cash;
    if (delta > 0) {
        if (amount > a->cash || fee > a->cash - amount)
            return 0;
        cash = a->cash - amount - fee;
    } else {
        cash = a->cash + amount; /* At most 10^12 + 10^15. */
        if (cash < fee || cash - fee > Q_MAX_CASH)
            return 0;
        cash -= fee;
    }
    *a = (QAccount){cash, target};
    return 1;
}

QResult q_backtest(const QBar *bars, size_t count, size_t window) {
    QResult result = {.window = window};
    if (!bars || count == 0 || count > Q_MAX_BARS || window == 0 || window > count)
        return result;
    /* Validate once per trial, before touching the ledger. Include this cost
       in the benchmark; hoisting it is an assignment, not an invisible shortcut. */
    for (size_t i = 0; i < count; ++i)
        if (bars[i].open <= 0 || bars[i].open > Q_MAX_PRICE || bars[i].close <= 0 ||
            bars[i].close > Q_MAX_PRICE)
            return result;
    QAccount account = {1000000, 0};
    int64_t pending = 0, sum = 0;
    for (size_t i = 0; i < count; ++i) {
        if (account.shares != pending) {
            if (!q_target(&account, pending, bars[i].open, 5))
                return result;
            ++result.fills;
        }
        sum += bars[i].close;
        if (i >= window)
            sum -= bars[i - window].close;
        /* Compare without division/rounding. Both sides <= about 10^15. */
        pending = i + 1 >= window && bars[i].close * (int64_t)window > sum ? 1 : 0;
    }
    result.equity = account.cash + account.shares * bars[count - 1].close;
    result.ok = 1;
    return result;
}

int q_equal(const QResult *a, const QResult *b, size_t count) {
    if (!a || !b)
        return 0;
    for (size_t i = 0; i < count; ++i)
        if (a[i].window != b[i].window || a[i].equity != b[i].equity ||
            a[i].fills != b[i].fills || a[i].ok != b[i].ok)
            return 0;
    return 1;
}
