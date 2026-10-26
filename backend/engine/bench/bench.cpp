// Repeatable timing for the simulator engine.
//
// Each parallel kernel runs serially and in parallel after one warm-up, then in
// five pairs whose order alternates, so drift in clock speed or cache state is
// not credited to either side. Every pair's outputs must be identical or the
// benchmark refuses to report. The execution engine is sequential by design (a
// bar's fills depend on the one before), so it is timed on its own.
//
// Usage: quanta-sim-bench [workers]
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>

#include "../src/analytics.hpp"
#include "../src/engine.hpp"
#include "../src/market.hpp"
#include "../src/parallel.hpp"
#include "../src/rng.hpp"

namespace {

using Clock = std::chrono::steady_clock;

double seconds_since(Clock::time_point start) {
  return std::chrono::duration<double>(Clock::now() - start).count();
}

double median(std::vector<double> values) {
  std::sort(values.begin(), values.end());
  return values[values.size() / 2];
}

// Times `run(workers)` serially and in parallel; `same` compares two outputs.
template <class Run, class Same>
void paired(const char* name, int workers, Run run, Same same) {
  auto timed = [&](int w, auto& out) {
    const auto start = Clock::now();
    out = run(w);
    return seconds_since(start);
  };
  decltype(run(1)) serial_out, parallel_out;
  timed(1, serial_out);
  timed(workers, parallel_out);
  if (!same(serial_out, parallel_out)) {
    std::printf("%s: serial and parallel results differ; refusing to report\n", name);
    std::exit(1);
  }
  std::vector<double> serial, parallel;
  for (int pair = 0; pair < 5; ++pair) {
    if (pair % 2 == 0) {
      serial.push_back(timed(1, serial_out));
      parallel.push_back(timed(workers, parallel_out));
    } else {
      parallel.push_back(timed(workers, parallel_out));
      serial.push_back(timed(1, serial_out));
    }
    if (!same(serial_out, parallel_out)) {
      std::printf("%s: pair %d differs; refusing to report\n", name, pair + 1);
      std::exit(1);
    }
  }
  std::printf("%s\n", name);
  for (int pair = 0; pair < 5; ++pair) {
    std::printf("  pair %d  serial %9.2f ms  parallel %9.2f ms  speedup %5.2fx\n", pair + 1,
                serial[pair] * 1e3, parallel[pair] * 1e3, serial[pair] / parallel[pair]);
  }
  const auto [lo, hi] = std::minmax_element(serial.begin(), serial.end());
  const auto [plo, phi] = std::minmax_element(parallel.begin(), parallel.end());
  std::printf("  median  serial %9.2f ms [%.2f-%.2f]  parallel %9.2f ms [%.2f-%.2f]  speedup %5.2fx\n",
              median(serial) * 1e3, *lo * 1e3, *hi * 1e3, median(parallel) * 1e3, *plo * 1e3, *phi * 1e3,
              median(serial) / median(parallel));
}

struct Block {
  std::vector<std::int32_t> cents, volume;
  std::vector<double> carry;
  bool operator==(const Block& o) const { return cents == o.cents && volume == o.volume && carry == o.carry; }
};

void bench_generation(int workers) {
  // The universe's shape: 32 companies, 12 sectors, a block's worth of shocks.
  std::vector<quanta::market::Company> companies;
  std::vector<double> carry;
  for (int j = 0; j < 32; ++j) {
    companies.push_back({0.6 + 0.04 * j, 0.18 + 0.012 * j, 8000.0 + 900.0 * j, j % 12});
    carry.push_back(25.0 + 7.0 * j);
  }
  std::vector<quanta::market::Shock> shocks;
  quanta::Pcg64 rng({7});
  for (int k = 0; k < 1500; ++k) {
    const auto scope = static_cast<std::int32_t>(rng.next64() % 3);
    shocks.push_back({scope, scope == 0 ? 0 : static_cast<std::int32_t>(rng.next64() % (scope == 1 ? 12 : 32)),
                      static_cast<std::int32_t>(rng.next64() % quanta::market::kBlockBars),
                      static_cast<std::int32_t>(30 + rng.next64() % 900), rng.next64() % 2 ? 1 : -1,
                      static_cast<std::int32_t>(40 + rng.next64() % 400)});
  }
  paired("block generation: 32 companies x 8,190 bars", workers, [&](int w) {
    Block out;
    out.cents.resize(32 * 4 * quanta::market::kBlockBars);
    out.volume.resize(32 * quanta::market::kBlockBars);
    out.carry.resize(32);
    quanta::market::generate_block({47, 0, companies.data(), 32, 12, carry.data(), shocks.data(),
                                    static_cast<std::int64_t>(shocks.size()), w},
                                   {out.cents.data(), out.volume.data(), out.carry.data()});
    return out;
  }, [](const Block& a, const Block& b) { return a == b; });
}

void bench_marking(int workers) {
  const std::int64_t bars = 200000;
  const int symbols = 32;
  const int fills = 2000;
  std::vector<std::int64_t> times(bars);
  std::vector<std::vector<double>> closes(symbols, std::vector<double>(bars));
  quanta::Pcg64 rng({11});
  for (std::int64_t i = 0; i < bars; ++i) {
    times[i] = 1736173800 + 60 * i;
    for (int s = 0; s < symbols; ++s) closes[s][i] = 50.0 + s + rng.standard_normal();
  }
  std::vector<const double*> rows;
  for (const auto& row : closes) rows.push_back(row.data());
  std::vector<std::int32_t> fill_symbol(fills);
  std::vector<std::int64_t> fill_quantity(fills), fill_time(fills);
  for (int k = 0; k < fills; ++k) {
    fill_symbol[k] = static_cast<std::int32_t>(rng.next64() % symbols);
    fill_quantity[k] = static_cast<std::int64_t>(rng.next64() % 400) - 200;
    fill_time[k] = times[static_cast<std::size_t>(k) * (bars / fills)];
  }
  paired("mark to market: 200,000 bars x 2,000 fills x 32 symbols", workers, [&](int w) {
    std::vector<double> equity(bars), gross(bars), level(bars);
    quanta::analytics::mark_to_market({bars, times.data(), 1e5, 0, nullptr, nullptr, fills, fill_symbol.data(),
                                       fill_quantity.data(), fill_time.data(), symbols, rows.data(), w},
                                      {equity.data(), gross.data(), level.data()});
    equity.insert(equity.end(), gross.begin(), gross.end());
    equity.insert(equity.end(), level.begin(), level.end());
    return equity;
  }, [](const std::vector<double>& a, const std::vector<double>& b) { return a == b; });
}

void bench_engine() {
  // 200 resting limit orders that never trade, plus a few that do, advanced a
  // full modeled week: the request that took the Python engine over a second.
  const std::int64_t bars = 2500;
  std::vector<std::int32_t> cents[4];
  std::vector<std::int32_t> volume(bars, 5000), day(bars);
  std::vector<std::int64_t> time(bars);
  quanta::Pcg64 rng({3});
  double price = 100.0;
  for (std::int64_t i = 0; i < bars; ++i) {
    price *= 1.0 + 0.001 * rng.standard_normal();
    const auto c = static_cast<std::int32_t>(price * 100);
    cents[0].push_back(c);
    cents[1].push_back(c + 20);
    cents[2].push_back(c - 20);
    cents[3].push_back(c);
    time[i] = 1736173800 + 60 * i;
    day[i] = 20094 + static_cast<std::int32_t>(i / 390);
  }
  quanta::engine::Bars series{};
  series.length = bars;
  for (int k = 0; k < 4; ++k) series.cents[k] = cents[k].data();
  series.volume_int = volume.data();
  series.time = time.data();
  series.day = day.data();
  std::string orders;
  for (int k = 0; k < 200; ++k) {
    if (k) orders += ",";
    const bool trades = k % 40 == 0;
    orders += "{\"id\":\"o" + std::to_string(k) +
              "\",\"symbol\":\"AAA\",\"side\":\"buy\",\"kind\":\"limit\",\"tif\":\"GTC\",\"status\":\"working\","
              "\"quantity\":5,\"filled\":0,\"limit_price\":\"" +
              std::string(trades ? "200.00" : "10.00") +
              "\",\"average\":\"0.00\",\"notional\":\"0.00\",\"fee_remaining\":\"1.00\",\"reserve_price\":\"" +
              std::string(trades ? "200.00" : "10.00") + "\",\"triggered\":false,\"forced\":false,\"day\":\"2025-01-06\"}";
  }
  const std::string request =
      "{\"op\":\"advance\",\"symbols\":[\"AAA\"],\"cursor\":499,\"config\":{\"commission\":\"1\","
      "\"slippage_bps\":\"2\",\"spread_bps\":\"2\",\"participation\":\"0.01\",\"account\":\"cash\"},"
      "\"margin\":{\"maintenance\":\"0.3\",\"borrow_rate\":\"0.05\",\"sessions_a_year\":252},"
      "\"cash\":\"100000.00\",\"realized\":\"0.00\",\"positions\":[],\"orders\":[" +
      orders + "],\"steps\":1950,\"watch\":[],\"scheduled\":[]}";
  std::string first = quanta::engine::handle(request, &series, 1);
  std::vector<double> runs;
  for (int k = 0; k < 5; ++k) {
    const auto start = Clock::now();
    const std::string again = quanta::engine::handle(request, &series, 1);
    runs.push_back(seconds_since(start));
    if (again != first) {
      std::printf("engine: repeated request gave a different answer; refusing to report\n");
      std::exit(1);
    }
  }
  std::printf("execution engine: 200 working orders advanced 1,950 bars (one thread)\n");
  for (int k = 0; k < 5; ++k) std::printf("  run %d  %9.2f ms\n", k + 1, runs[k] * 1e3);
  const auto [lo, hi] = std::minmax_element(runs.begin(), runs.end());
  std::printf("  median %9.2f ms [%.2f-%.2f], including JSON parsing and writing\n", median(runs) * 1e3, *lo * 1e3,
              *hi * 1e3);
}

}  // namespace

int main(int argc, char** argv) {
  const int workers = argc > 1 ? std::max(1, std::atoi(argv[1])) : quanta::default_workers();
  std::printf("compiler %s, %u hardware threads, %d workers\n", __VERSION__,
              std::thread::hardware_concurrency(), workers);
  bench_generation(workers);
  bench_marking(workers);
  bench_engine();
  return 0;
}
