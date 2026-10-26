// Generated market data: the news-driven factor model and the original six paths.
//
// Both are pure functions of a run's stored seed and reproduce the Python
// generators they replace to the cent, so runs already in the database replay
// against exactly the bars they were traded on.
#pragma once

#include <cstdint>

namespace quanta::market {

constexpr std::int64_t kSessionBars = 390;
constexpr std::int64_t kBlockSessions = 21;
constexpr std::int64_t kBlockBars = kSessionBars * kBlockSessions;  // 8190
constexpr std::int64_t kLegacyBars = 6000;

// One listed company's generator parameters, in universe order.
struct Company {
  double beta;
  double volatility;  // annualized
  double volume;      // typical shares per minute
  std::int32_t sector;
};

// A scored headline's price shock, as the newsroom scheduled it. Scope 0 moves
// the market factor, 1 a sector (target = sector index), 2 one company (target =
// company index). Index is the bar within the block; points are basis points.
struct Shock {
  std::int32_t scope;
  std::int32_t target;
  std::int32_t index;
  std::int32_t points;
  std::int32_t sign;
  std::int32_t span;
};

struct BlockInput {
  std::uint64_t seed;
  std::int64_t first_session;
  const Company* companies;
  std::int32_t company_count;
  std::int32_t sector_count;
  const double* carry;  // opening price per company: the previous block's last close
  const Shock* shocks;
  std::int64_t shock_count;
  int workers;
};

struct BlockOutput {
  std::int32_t* cents;   // [company][open, high, low, close][bar]
  std::int32_t* volume;  // [company][bar]
  double* carry;         // [company] closing price, to the printed cent
};

// Generate one block of 21 sessions. Throws quanta::Error on invalid input; the
// outputs are then unspecified and must not be used.
void generate_block(const BlockInput& input, const BlockOutput& output);

// Minute stamps (UTC epoch seconds) and calendar days for consecutive sessions.
void session_calendar(std::int64_t first_session, std::int64_t sessions, std::int64_t* time,
                      std::int32_t* day);

// The original six-symbol generator: 6000 minute bars per symbol, each symbol on
// its own random.Random(seed) stream. Cents are round(x, 2) * 100.
void legacy_paths(const std::uint64_t* seeds, const double* initial, std::int32_t count,
                  int workers, std::int32_t* cents, std::int32_t* volume);

// One columnar series, read-only.
struct Columns {
  const std::int32_t* cents[4];  // open, high, low, close
  const std::int32_t* volume;
  const std::int64_t* time;
  const std::int64_t* session;
  std::int64_t length;
};

struct Buckets {
  std::int64_t* time;
  std::int32_t* cents[4];
  std::int64_t* volume;
};

// Group observations [start, stop) into bars of `per_bucket` minutes, anchored
// to each session's open. A bucket is stamped with its first observation, or,
// when `aligned` is set, with the boundary it starts on even if the window
// begins inside it (the stamping the original six-path chart used). Returns the
// bucket count; outputs need room for stop - start buckets.
std::int64_t aggregate(const Columns& series, std::int64_t start, std::int64_t stop,
                       std::int32_t per_bucket, bool aligned, const Buckets& out);

}  // namespace quanta::market
