// The paper-trading execution engine: order validation, cash and share
// reservations, bar-by-bar fills, attached exits, trailing stops, margin
// financing and buy-ins, and the events that stop a replay.
//
// It is a transcription of the Python engine it replaces, rule for rule and in
// the same order, so an account replayed through either one ends in the same
// state to the cent and the same reason string.
#pragma once

#include <cstdint>
#include <string>
#include <string_view>

namespace quanta::engine {

// One symbol's bars as the caller hands them over. Prices are either integer
// cents (generated markets) or floats (imported datasets); a float is read the
// way Python's Decimal(str(x)) reads it.
struct Bars {
  std::int64_t length;
  const std::int32_t* cents[4];  // open, high, low, close; null when `values` is used
  const double* values[4];
  const std::int32_t* volume_int;  // exactly one of the two volume columns is set
  const double* volume_float;
  const std::int64_t* time;
  const std::int32_t* day;  // New York calendar day (days since 1970-01-01)
};

// Handle one JSON request and return the JSON response. A refused action is a
// normal response, {"error": message}; malformed input throws quanta::Error.
std::string handle(std::string_view request, const Bars* bars, std::int32_t count);

}  // namespace quanta::engine
