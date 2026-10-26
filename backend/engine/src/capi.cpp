// The C boundary: argument checks, exception capture and buffer handover.
#include <cstdlib>
#include <cstring>
#include <exception>
#include <string>
#include <vector>

#include "../include/quanta_sim.h"
#include "analytics.hpp"
#include "common.hpp"
#include "decimal.hpp"
#include "engine.hpp"
#include "market.hpp"
#include "numeric.hpp"
#include "parallel.hpp"
#include "rng.hpp"

namespace {

thread_local std::string last_error;

int workers_or_default(std::int32_t workers) {
  return workers > 0 ? workers : quanta::default_workers();
}

// Runs a body, turning any exception into an error code and a message. Nothing
// escapes into the caller's runtime.
template <class Body>
int guarded(Body&& body) {
  try {
    body();
    last_error.clear();
    return 0;
  } catch (const quanta::DomainError& error) {
    last_error = error.what();
    return 2;
  } catch (const std::exception& error) {
    last_error = error.what();
    return 1;
  } catch (...) {
    last_error = "unknown engine failure";
    return 1;
  }
}

}  // namespace

extern "C" {

int qs_abi_version(void) { return QS_ABI_VERSION; }

const char* qs_last_error(void) { return last_error.c_str(); }

int qs_generate_block(uint64_t seed, int64_t first_session, const qs_company* companies,
                      int32_t company_count, int32_t sector_count, const double* carry,
                      const qs_shock* shocks, int64_t shock_count, int32_t workers, int32_t* cents,
                      int32_t* volume, double* carry_out) {
  return guarded([&] {
    quanta::require(companies != nullptr && company_count > 0, "companies are missing");
    std::vector<quanta::market::Company> roster(static_cast<std::size_t>(company_count));
    for (int32_t j = 0; j < company_count; ++j) {
      roster[j] = {companies[j].beta, companies[j].volatility, companies[j].volume, companies[j].sector};
    }
    quanta::require(shock_count >= 0 && (shock_count == 0 || shocks), "shocks are missing");
    std::vector<quanta::market::Shock> schedule(static_cast<std::size_t>(shock_count));
    for (int64_t k = 0; k < shock_count; ++k) {
      const qs_shock& s = shocks[k];
      schedule[k] = {s.scope, s.target, s.index, s.points, s.sign, s.span};
    }
    quanta::market::BlockInput input{seed,        first_session, roster.data(),   company_count,
                                     sector_count, carry,         schedule.data(), shock_count,
                                     workers_or_default(workers)};
    quanta::market::BlockOutput output{cents, volume, carry_out};
    quanta::market::generate_block(input, output);
  });
}

int qs_session_calendar(int64_t first_session, int64_t sessions, int64_t* time, int32_t* day) {
  return guarded([&] { quanta::market::session_calendar(first_session, sessions, time, day); });
}

int qs_legacy_paths(const uint64_t* seeds, const double* initial, int32_t count, int32_t workers,
                    int32_t* cents, int32_t* volume) {
  return guarded([&] {
    quanta::market::legacy_paths(seeds, initial, count, workers_or_default(workers), cents, volume);
  });
}

int qs_aggregate(const int32_t* open, const int32_t* high, const int32_t* low, const int32_t* close,
                 const int32_t* volume, const int64_t* time, const int64_t* session, int64_t length,
                 int64_t start, int64_t stop, int32_t per_bucket, int32_t aligned, int64_t* out_time,
                 int32_t* out_open, int32_t* out_high, int32_t* out_low, int32_t* out_close,
                 int64_t* out_volume, int64_t* count) {
  return guarded([&] {
    quanta::require(open && high && low && close && count, "aggregate buffers are missing");
    quanta::require(out_time && out_open && out_high && out_low && out_close && out_volume,
                    "aggregate outputs are missing");
    const quanta::market::Columns series{{open, high, low, close}, volume, time, session, length};
    const quanta::market::Buckets buckets{out_time, {out_open, out_high, out_low, out_close}, out_volume};
    *count = quanta::market::aggregate(series, start, stop, per_bucket, aligned != 0, buckets);
  });
}

int qs_engine(const char* request, size_t length, const qs_bars* bars, int32_t count, char** response,
              size_t* response_length) {
  return guarded([&] {
    quanta::require(request && response && response_length, "engine buffers are missing");
    quanta::require(count >= 0 && count <= 100000, "symbol count out of range");
    std::vector<quanta::engine::Bars> columns(static_cast<std::size_t>(count));
    for (int32_t i = 0; i < count; ++i) {
      const qs_bars& b = bars[i];
      columns[i] = {b.length,
                    {b.cents[0], b.cents[1], b.cents[2], b.cents[3]},
                    {b.values[0], b.values[1], b.values[2], b.values[3]},
                    b.volume_int,
                    b.volume_float,
                    b.time,
                    b.day};
    }
    const std::string text = quanta::engine::handle(std::string_view(request, length),
                                                    count ? columns.data() : nullptr, count);
    char* buffer = static_cast<char*>(std::malloc(text.size() + 1));
    quanta::require(buffer != nullptr, "out of memory");
    std::memcpy(buffer, text.data(), text.size());
    buffer[text.size()] = '\0';
    *response = buffer;
    *response_length = text.size();
  });
}

void qs_free(char* pointer) { std::free(pointer); }

int qs_sma(const double* values, int64_t n, int32_t period, double* out) {
  return guarded([&] { quanta::analytics::sma(values, n, period, out); });
}

int qs_ema(const double* values, int64_t n, int32_t period, double* out) {
  return guarded([&] { quanta::analytics::ema(values, n, period, out); });
}

int qs_rsi(const double* values, int64_t n, int32_t period, double* out) {
  return guarded([&] { quanta::analytics::rsi(values, n, period, out); });
}

int qs_macd(const double* values, int64_t n, int32_t fast, int32_t slow, int32_t signal,
            double* line, double* signal_line, double* histogram) {
  return guarded(
      [&] { quanta::analytics::macd(values, n, fast, slow, signal, line, signal_line, histogram); });
}

int qs_mark_to_market(int64_t bars, const int64_t* times, double opening, int64_t cash_events,
                      const int64_t* cash_times, const double* cash_values, int64_t fill_count,
                      const int32_t* fill_symbol, const int64_t* fill_quantity,
                      const int64_t* fill_time, int32_t symbols, const double* const* closes,
                      int32_t workers, double* equity, double* gross, double* level) {
  return guarded([&] {
    const quanta::analytics::MarkInput input{bars,       times,       opening,       cash_events,
                                             cash_times, cash_values, fill_count,    fill_symbol,
                                             fill_quantity, fill_time, symbols,      closes,
                                             workers_or_default(workers)};
    quanta::analytics::mark_to_market(input, {equity, gross, level});
  });
}

int qs_decimal(const char* op, const char* a, const char* b, char* out, size_t capacity) {
  return guarded([&] {
    using quanta::Dec;
    quanta::require(op && a && out && capacity > 0, "decimal buffers are missing");
    const std::string name(op);
    const Dec x = Dec::parse(a);
    auto other = [&] {
      quanta::require(b != nullptr, "second operand is missing");
      return Dec::parse(b);
    };
    std::string result;
    if (name == "add") result = (x + other()).str();
    else if (name == "sub") result = (x - other()).str();
    else if (name == "mul") result = (x * other()).str();
    else if (name == "div") result = (x / other()).str();
    else if (name == "neg") result = (-x).str();
    else if (name == "abs") result = quanta::abs(x).str();
    else if (name == "cmp") result = std::to_string(quanta::compare(x, other()));
    else if (name == "half_up") result = quanta::quantize(x, -2, quanta::Rounding::HalfUp).str();
    else if (name == "ceiling") result = quanta::quantize(x, -2, quanta::Rounding::Ceiling).str();
    else if (name == "down") result = quanta::quantize(x, -2, quanta::Rounding::Down).str();
    else if (name == "integral") result = quanta::to_integral_down(x).str();
    else if (name == "int") result = std::to_string(quanta::to_int64(x));
    else if (name == "str") result = x.str();
    else quanta::fail("unknown decimal operation");
    quanta::require(result.size() < capacity, "decimal result does not fit the buffer");
    std::memcpy(out, result.c_str(), result.size() + 1);
  });
}

int qs_round_hundredths(double value, int64_t* out) {
  return guarded([&] { *out = quanta::numeric::python_round_hundredths(value); });
}

int qs_standard_normals(const uint64_t* entropy, int32_t words, int64_t n, double* out) {
  return guarded([&] {
    quanta::require(words > 0 && entropy && out && n >= 0, "normal draw buffers are missing");
    quanta::Pcg64 rng(std::vector<std::uint64_t>(entropy, entropy + words));
    for (int64_t i = 0; i < n; ++i) out[i] = rng.standard_normal();
  });
}

int qs_python_random(uint64_t seed, int64_t n, double* uniforms, double* gauss, int64_t* integers) {
  return guarded([&] {
    quanta::require(uniforms && gauss && integers && n >= 0, "random buffers are missing");
    quanta::PythonRandom rng(seed);
    for (int64_t i = 0; i < n; ++i) {
      uniforms[i] = rng.random();
      gauss[i] = rng.gauss(0.0, 1.0);
      integers[i] = rng.randint(2000, 30000);
    }
  });
}

}  // extern "C"
