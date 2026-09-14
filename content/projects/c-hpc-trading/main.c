#define _POSIX_C_SOURCE 200809L
#include "quanta.h"
#include <errno.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static double now(void) {
    struct timespec t;
    if (clock_gettime(CLOCK_MONOTONIC, &t) != 0) {
        perror("clock_gettime");
        exit(1);
    }
    return (double)t.tv_sec + (double)t.tv_nsec / 1e9;
}
static int argument(const char *s, size_t maximum, size_t *value) {
    if (!s || !*s)
        return 0;
    for (const char *p = s; *p; ++p)
        if (*p < '0' || *p > '9')
            return 0;
    errno = 0;
    char *end;
    unsigned long n = strtoul(s, &end, 10);
    if (errno || *end || n == 0 || n > maximum)
        return 0;
    *value = (size_t)n;
    return 1;
}
int main(int argc, char **argv) {
    size_t threads = 4, count = 200000;
    if (argc > 3 || (argc > 1 && !argument(argv[1], Q_MAX_THREADS, &threads)) ||
        (argc > 2 && !argument(argv[2], Q_MAX_BARS, &count)) || count < 65) {
        fputs("Usage: ./quanta-bot [threads 1..32] [bars 65..1000000]\n", stderr);
        return 2;
    }
    QBar *bars = malloc(count * sizeof(*bars));
    if (!bars || !q_generate(bars, count, 42)) {
        free(bars);
        return 1;
    }
    size_t windows[64];
    QResult serial[64], parallel[64];
    for (size_t i = 0; i < 64; ++i)
        windows[i] = i + 2;
    /* Untimed warmup. Five paired repetitions, alternating order. */
    if (!q_sweep(bars, count, windows, 64, threads, parallel)) {
        free(bars);
        return 1;
    }
    puts("Synthetic research benchmark; initial cash=1000000 cents; fee=5 cents/fill");
    printf("bars=%zu jobs=64 threads=%zu seed=42 compiler=%s\n", count, threads,
           __VERSION__);
    for (size_t r = 0; r < 5; ++r) {
        double serial_s = 0, parallel_s = 0;
        for (size_t j = 0; j < 2; ++j) {
            int use_parallel = (r + j) % 2 != 0;
            double start = now();
            int ok = q_sweep(bars, count, windows, 64, use_parallel ? threads : 1,
                             use_parallel ? parallel : serial);
            double elapsed = now() - start;
            if (!ok) {
                free(bars);
                return 1;
            }
            if (use_parallel)
                parallel_s = elapsed;
            else
                serial_s = elapsed;
        }
        if (!q_equal(serial, parallel, 64)) {
            fputs("RESULT MISMATCH\n", stderr);
            free(bars);
            return 1;
        }
        printf("repeat=%zu serial_ms=%.3f parallel_ms=%.3f speedup=%.3f equal=yes\n",
               r + 1, serial_s * 1000, parallel_s * 1000,
               parallel_s > 0 ? serial_s / parallel_s : 0);
    }
    puts("window,equity_cents,fills");
    for (size_t i = 0; i < 64; ++i)
        printf("%zu,%" PRId64 ",%zu\n", serial[i].window, serial[i].equity,
               serial[i].fills);
    free(bars);
    return 0;
}
