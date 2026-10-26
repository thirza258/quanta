// Desk analytics: chart overlays and the account marked to market on every bar.
//
// The indicator recurrences are the ones the courses teach, evaluated in the
// same floating-point order as the Python loops they replace. A missing value
// (an indicator still warming up) is NaN; callers turn it back into None.
#pragma once

#include <cstdint>

namespace quanta::analytics {

void sma(const double* values, std::int64_t n, std::int32_t period, double* out);
void ema(const double* values, std::int64_t n, std::int32_t period, double* out);
void rsi(const double* values, std::int64_t n, std::int32_t period, double* out);
void macd(const double* values, std::int64_t n, std::int32_t fast, std::int32_t slow,
          std::int32_t signal, double* line, double* signal_line, double* histogram);

// The account's equity on every observed bar, its gross exposure, and the
// equal-weighted index the benchmark follows.
struct MarkInput {
  std::int64_t bars;            // window length
  const std::int64_t* times;    // window timestamps, ascending
  double opening;               // opening cash
  std::int64_t cash_events;     // ledger entries with a time, in ledger order
  const std::int64_t* cash_times;
  const double* cash_values;
  std::int64_t fill_count;      // fills in order, whose symbol is in the run
  const std::int32_t* fill_symbol;
  const std::int64_t* fill_quantity;  // signed: buys positive
  const std::int64_t* fill_time;
  std::int32_t symbols;
  const double* const* closes;  // per symbol, the window's closes
  int workers;
};

struct MarkOutput {
  double* equity;  // [bars]
  double* gross;   // [bars]
  double* level;   // [bars] equal-weighted index rebased to the window start
};

void mark_to_market(const MarkInput& input, const MarkOutput& output);

}  // namespace quanta::analytics
