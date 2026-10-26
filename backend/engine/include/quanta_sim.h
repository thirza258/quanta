/*
 * Quanta simulator engine: the C interface the Python API loads with ctypes.
 *
 * Every function returns 0 on success. On failure it returns a nonzero code and
 * qs_last_error() describes the problem on the calling thread; output buffers
 * are then unspecified and must be discarded. No function keeps a pointer it
 * was given after it returns, and none holds global mutable state, so calls on
 * different threads are independent.
 */
#ifndef QUANTA_SIM_H
#define QUANTA_SIM_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define QS_ABI_VERSION 1

int qs_abi_version(void);
const char* qs_last_error(void);

/* One listed company's generator parameters. */
typedef struct {
  double beta;
  double volatility;
  double volume;
  int32_t sector;
  int32_t reserved;
} qs_company;

/* A scored headline's price shock: scope 0 market, 1 sector, 2 company. */
typedef struct {
  int32_t scope;
  int32_t target;
  int32_t index;
  int32_t points;
  int32_t sign;
  int32_t span;
} qs_shock;

/* One block of 21 sessions x 390 bars. cents is [company][4][8190] (open, high,
 * low, close), volume is [company][8190], carry_out the closing price each
 * company opens the next block on. */
int qs_generate_block(uint64_t seed, int64_t first_session, const qs_company* companies,
                      int32_t company_count, int32_t sector_count, const double* carry,
                      const qs_shock* shocks, int64_t shock_count, int32_t workers, int32_t* cents,
                      int32_t* volume, double* carry_out);

/* Minute stamps and New York calendar days for consecutive weekday sessions. */
int qs_session_calendar(int64_t first_session, int64_t sessions, int64_t* time, int32_t* day);

/* The original six-symbol generator: cents is [symbol][4][6000], volume [symbol][6000]. */
int qs_legacy_paths(const uint64_t* seeds, const double* initial, int32_t count, int32_t workers,
                    int32_t* cents, int32_t* volume);

/* Coarser bars from minute observations [start, stop). Returns the bucket count
 * in *count. Output arrays need room for stop - start buckets. */
int qs_aggregate(const int32_t* open, const int32_t* high, const int32_t* low, const int32_t* close,
                 const int32_t* volume, const int64_t* time, const int64_t* session, int64_t length,
                 int64_t start, int64_t stop, int32_t per_bucket, int32_t aligned, int64_t* out_time,
                 int32_t* out_open, int32_t* out_high, int32_t* out_low, int32_t* out_close,
                 int64_t* out_volume, int64_t* count);

/* One symbol's bars for the execution engine: cents or float prices. */
typedef struct {
  int64_t length;
  const int32_t* cents[4];
  const double* values[4];
  const int32_t* volume_int;
  const double* volume_float;
  const int64_t* time;
  const int32_t* day;
} qs_bars;

/* Run one engine request (JSON) against the given bars. The response is
 * allocated by the engine; release it with qs_free. */
int qs_engine(const char* request, size_t length, const qs_bars* bars, int32_t count,
              char** response, size_t* response_length);
void qs_free(char* pointer);

/* Indicator series; NaN marks a value still warming up. */
int qs_sma(const double* values, int64_t n, int32_t period, double* out);
int qs_ema(const double* values, int64_t n, int32_t period, double* out);
int qs_rsi(const double* values, int64_t n, int32_t period, double* out);
int qs_macd(const double* values, int64_t n, int32_t fast, int32_t slow, int32_t signal,
            double* line, double* signal_line, double* histogram);

/* Equity, gross exposure and the equal-weighted index on every bar of a window. */
int qs_mark_to_market(int64_t bars, const int64_t* times, double opening, int64_t cash_events,
                      const int64_t* cash_times, const double* cash_values, int64_t fill_count,
                      const int32_t* fill_symbol, const int64_t* fill_quantity,
                      const int64_t* fill_time, int32_t symbols, const double* const* closes,
                      int32_t workers, double* equity, double* gross, double* level);

/* Test hooks: the primitives the differential tests compare against Python. */
int qs_decimal(const char* op, const char* a, const char* b, char* out, size_t capacity);
int qs_round_hundredths(double value, int64_t* out);
int qs_standard_normals(const uint64_t* entropy, int32_t words, int64_t n, double* out);
int qs_python_random(uint64_t seed, int64_t n, double* uniforms, double* gauss, int64_t* integers);

#ifdef __cplusplus
}
#endif

#endif /* QUANTA_SIM_H */
