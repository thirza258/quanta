#include "quanta.h"
#include <pthread.h>
#include <stdlib.h>

typedef struct {
    const QBar *bars;
    size_t count;
    const size_t *windows;
    size_t jobs, stride, first;
    QResult *results;
} Worker;

static void *work(void *arg) {
    Worker *w = arg;
    for (size_t i = w->first; i < w->jobs; i += w->stride)
        w->results[i] = q_backtest(w->bars, w->count, w->windows[i]);
    return NULL;
}

int q_sweep(const QBar *bars, size_t count, const size_t *windows, size_t jobs,
            size_t threads, QResult *results) {
    if (!bars || !windows || !results || count == 0 || count > Q_MAX_BARS ||
        jobs == 0 || jobs > Q_MAX_JOBS || threads == 0 || threads > Q_MAX_THREADS)
        return 0;
    for (size_t i = 0; i < jobs; ++i)
        if (!windows[i] || windows[i] > count)
            return 0;
    if (threads > jobs)
        threads = jobs;
    pthread_t ids[Q_MAX_THREADS];
    Worker workers[Q_MAX_THREADS];
    QResult scratch[Q_MAX_JOBS] = {0};
    size_t started = 0;
    for (size_t i = 0; i < threads; ++i) {
        workers[i] = (Worker){bars, count, windows, jobs, threads, i, scratch};
        if (threads == 1) {
            work(&workers[i]);
            break;
        }
        if (pthread_create(&ids[i], NULL, work, &workers[i]) != 0)
            break;
        ++started;
    }
    for (size_t i = 0; i < started; ++i) {
        /* A join failure violates this function's thread-lifetime invariant.
           Do not return while workers might still reference its stack. */
        if (pthread_join(ids[i], NULL) != 0)
            abort();
    }
    if (threads > 1 && started != threads)
        return 0;
    for (size_t i = 0; i < jobs; ++i)
        if (!scratch[i].ok)
            return 0;
    for (size_t i = 0; i < jobs; ++i)
        results[i] = scratch[i];
    return 1;
}
