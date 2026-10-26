#include "analytics.hpp"

#include <cmath>
#include <limits>
#include <vector>

#include "common.hpp"
#include "parallel.hpp"

namespace quanta::analytics {

namespace {

constexpr double kMissing = std::numeric_limits<double>::quiet_NaN();

void check_series(const double* values, std::int64_t n, std::int32_t period, const double* out) {
  require(n >= 0 && n <= 100000000, "series length out of range");
  require(n == 0 || (values && out), "series buffers are missing");
  require(period >= 1 && period <= 100000, "indicator period out of range");
}

// Python's max(x, 0.0): the first argument wins a tie, so -0.0 stays -0.0.
double at_least_zero(double x) { return 0.0 > x ? 0.0 : x; }

}  // namespace

// Rolling mean, with no value until the window is full.
void sma(const double* values, std::int64_t n, std::int32_t period, double* out) {
  check_series(values, n, period, out);
  double total = 0.0;
  for (std::int64_t i = 0; i < n; ++i) {
    total += values[i];
    if (i >= period) total -= values[i - period];
    out[i] = i >= period - 1 ? total / static_cast<double>(period) : kMissing;
  }
}

// Seeded with the first full simple average, then exponentially smoothed.
void ema(const double* values, std::int64_t n, std::int32_t period, double* out) {
  check_series(values, n, period, out);
  const double alpha = 2.0 / static_cast<double>(period + 1);
  double total = 0.0;
  double previous = 0.0;
  bool seeded = false;
  for (std::int64_t i = 0; i < n; ++i) {
    total += values[i];
    if (i < period - 1) {
      out[i] = kMissing;
      continue;
    }
    previous = seeded ? alpha * values[i] + (1.0 - alpha) * previous
                      : total / static_cast<double>(period);
    seeded = true;
    out[i] = previous;
  }
}

// Wilder smoothing, matching the definition the courses teach.
void rsi(const double* values, std::int64_t n, std::int32_t period, double* out) {
  check_series(values, n, period, out);
  const auto p = static_cast<double>(period);
  double gain = 0.0;
  double loss = 0.0;
  for (std::int64_t i = 0; i < n; ++i) {
    if (i == 0) {
      out[i] = kMissing;
      continue;
    }
    const double change = values[i] - values[i - 1];
    if (i <= period) {
      gain += at_least_zero(change) / p;
      loss += at_least_zero(-change) / p;
    } else {
      gain = (gain * static_cast<double>(period - 1) + at_least_zero(change)) / p;
      loss = (loss * static_cast<double>(period - 1) + at_least_zero(-change)) / p;
    }
    if (i < period) out[i] = kMissing;
    else if (loss == 0.0) out[i] = gain != 0.0 ? 100.0 : 50.0;
    else out[i] = 100.0 - 100.0 / (1.0 + gain / loss);
  }
}

void macd(const double* values, std::int64_t n, std::int32_t fast, std::int32_t slow,
          std::int32_t signal, double* line, double* signal_line, double* histogram) {
  check_series(values, n, fast, line);
  check_series(values, n, slow, signal_line);
  check_series(values, n, signal, histogram);
  std::vector<double> quick(static_cast<std::size_t>(n)), slack(static_cast<std::size_t>(n));
  ema(values, n, fast, quick.data());
  ema(values, n, slow, slack.data());
  std::int64_t offset = 0;
  for (std::int64_t i = 0; i < n; ++i) {
    const bool missing = std::isnan(quick[i]) || std::isnan(slack[i]);
    line[i] = missing ? kMissing : quick[i] - slack[i];
    if (missing) ++offset;
  }
  // The signal smooths only the values that exist, so it starts after the line does.
  for (std::int64_t i = 0; i < offset; ++i) signal_line[i] = kMissing;
  ema(line + offset, n - offset, signal, signal_line + offset);
  for (std::int64_t i = 0; i < n; ++i) {
    histogram[i] = std::isnan(line[i]) || std::isnan(signal_line[i]) ? kMissing
                                                                      : line[i] - signal_line[i];
  }
}

void mark_to_market(const MarkInput& in, const MarkOutput& out) {
  const std::int64_t bars = in.bars;
  require(bars >= 0 && bars <= 100000000, "window length out of range");
  if (bars == 0) return;
  require(in.times && out.equity && out.gross && out.level, "mark-to-market buffers are missing");
  require(in.symbols >= 1 && in.closes, "mark-to-market needs every symbol's closes");
  require(in.cash_events >= 0 && (in.cash_events == 0 || (in.cash_times && in.cash_values)),
          "cash events are missing");
  require(in.fill_count >= 0 && (in.fill_count == 0 || (in.fill_symbol && in.fill_quantity && in.fill_time)),
          "fills are missing");
  for (std::int32_t s = 0; s < in.symbols; ++s) require(in.closes[s] != nullptr, "a symbol's closes are missing");

  // np.searchsorted(times, t): the first bar at or after t.
  auto position = [&](std::int64_t stamp) {
    std::int64_t low = 0, high = bars;
    while (low < high) {
      const std::int64_t mid = low + (high - low) / 2;
      if (in.times[mid] < stamp) low = mid + 1;
      else high = mid;
    }
    return low;
  };

  // The cash balance on each bar is the last ledger entry, in ledger order, that
  // had already happened by then.
  std::vector<std::int64_t> owner(static_cast<std::size_t>(bars), -1);
  for (std::int64_t k = 0; k < in.cash_events; ++k) {
    const std::int64_t at = position(in.cash_times[k]);
    if (at < bars && k > owner[at]) owner[at] = k;
  }
  std::vector<double> cash(static_cast<std::size_t>(bars));
  std::int64_t latest = -1;
  for (std::int64_t t = 0; t < bars; ++t) {
    if (owner[t] > latest) latest = owner[t];
    cash[t] = latest >= 0 ? in.cash_values[latest] : in.opening;
  }

  // Fills that land inside the window, in order, and the order in which each
  // symbol first appears: the gross sum adds symbols in that order.
  struct Leg {
    std::int64_t at;
    double quantity;
    std::int32_t symbol;
    std::int32_t slot;
  };
  std::vector<Leg> legs;
  std::vector<std::int32_t> slot_of(static_cast<std::size_t>(in.symbols), -1);
  std::int32_t slots = 0;
  bool ordered = true;
  for (std::int64_t f = 0; f < in.fill_count; ++f) {
    const std::int32_t symbol = in.fill_symbol[f];
    require(symbol >= 0 && symbol < in.symbols, "a fill names an unknown symbol");
    const std::int64_t at = position(in.fill_time[f]);
    if (at >= bars) continue;
    if (slot_of[symbol] < 0) slot_of[symbol] = slots++;
    if (!legs.empty() && at < legs.back().at) ordered = false;
    legs.push_back(Leg{at, static_cast<double>(in.fill_quantity[f]), symbol, slot_of[symbol]});
  }

  // Each bar is independent of every other, so the window splits across
  // workers; every bar still adds its fills in fill order.
  const std::int64_t chunk = 2048;
  const std::int64_t chunks = (bars + chunk - 1) / chunk;
  parallel_for(chunks, in.workers, [&](std::int64_t c) {
    std::vector<double> by_slot(static_cast<std::size_t>(slots));
    const std::int64_t first = c * chunk;
    const std::int64_t stop = std::min(bars, first + chunk);
    for (std::int64_t t = first; t < stop; ++t) {
      double holdings = 0.0;
      for (auto& v : by_slot) v = 0.0;
      for (const Leg& leg : legs) {
        if (leg.at > t) {
          if (ordered) break;
          continue;
        }
        const double value = leg.quantity * in.closes[leg.symbol][t];
        holdings = holdings + value;
        by_slot[leg.slot] = by_slot[leg.slot] + value;
      }
      double gross = 0.0;
      for (std::int32_t s = 0; s < slots; ++s) gross = gross + std::fabs(by_slot[s]);
      out.equity[t] = cash[t] + holdings;
      out.gross[t] = gross;
      double level = 0.0;
      for (std::int32_t s = 0; s < in.symbols; ++s) level = level + in.closes[s][t] / in.closes[s][0];
      out.level[t] = level / static_cast<double>(in.symbols);
    }
  });
}

}  // namespace quanta::analytics
