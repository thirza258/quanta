// A 256-bit unsigned integer: enough room for the exact product of two
// 38-digit decimal coefficients, which is what correctly rounded decimal
// arithmetic needs before it rounds back to 28 digits.
#pragma once

#include <cstdint>

#include "common.hpp"

namespace quanta {

struct U256 {
  std::uint64_t w[4] = {0, 0, 0, 0};  // least significant limb first

  static U256 of(u128 value) {
    U256 out;
    out.w[0] = static_cast<std::uint64_t>(value);
    out.w[1] = static_cast<std::uint64_t>(value >> 64);
    return out;
  }

  bool is_zero() const { return (w[0] | w[1] | w[2] | w[3]) == 0; }
  bool fits_u128() const { return (w[2] | w[3]) == 0; }
  u128 low128() const { return (static_cast<u128>(w[1]) << 64) | w[0]; }

  int bit_length() const {
    for (int limb = 3; limb >= 0; --limb) {
      if (w[limb]) return limb * 64 + (64 - __builtin_clzll(w[limb]));
    }
    return 0;
  }

  bool bit(int index) const { return (w[index / 64] >> (index % 64)) & 1u; }
};

inline int compare(const U256& a, const U256& b) {
  for (int limb = 3; limb >= 0; --limb) {
    if (a.w[limb] != b.w[limb]) return a.w[limb] < b.w[limb] ? -1 : 1;
  }
  return 0;
}

// Returns false when the sum does not fit.
inline bool add(const U256& a, const U256& b, U256& out) {
  u128 carry = 0;
  for (int limb = 0; limb < 4; ++limb) {
    const u128 total = static_cast<u128>(a.w[limb]) + b.w[limb] + carry;
    out.w[limb] = static_cast<std::uint64_t>(total);
    carry = total >> 64;
  }
  return carry == 0;
}

// a - b, for a >= b.
inline U256 sub(const U256& a, const U256& b) {
  U256 out;
  std::uint64_t borrow = 0;
  for (int limb = 0; limb < 4; ++limb) {
    const u128 subtrahend = static_cast<u128>(b.w[limb]) + borrow;
    const u128 minuend = a.w[limb];
    if (minuend >= subtrahend) {
      out.w[limb] = static_cast<std::uint64_t>(minuend - subtrahend);
      borrow = 0;
    } else {
      out.w[limb] = static_cast<std::uint64_t>((static_cast<u128>(1) << 64) + minuend - subtrahend);
      borrow = 1;
    }
  }
  return out;
}

// Returns false when the product does not fit.
inline bool mul(const U256& a, const U256& b, U256& out) {
  std::uint64_t result[8] = {0, 0, 0, 0, 0, 0, 0, 0};
  for (int i = 0; i < 4; ++i) {
    if (!a.w[i]) continue;
    u128 carry = 0;
    for (int j = 0; j < 4; ++j) {
      const u128 term = static_cast<u128>(a.w[i]) * b.w[j] + result[i + j] + carry;
      result[i + j] = static_cast<std::uint64_t>(term);
      carry = term >> 64;
    }
    result[i + 4] = static_cast<std::uint64_t>(carry);
  }
  for (int limb = 4; limb < 8; ++limb) {
    if (result[limb]) return false;
  }
  for (int limb = 0; limb < 4; ++limb) out.w[limb] = result[limb];
  return true;
}

inline U256 shift_left_one(const U256& a) {
  U256 out;
  out.w[3] = (a.w[3] << 1) | (a.w[2] >> 63);
  out.w[2] = (a.w[2] << 1) | (a.w[1] >> 63);
  out.w[1] = (a.w[1] << 1) | (a.w[0] >> 63);
  out.w[0] = a.w[0] << 1;
  return out;
}

// Quotient and remainder. The divisor must be non-zero and below 2^255, which
// the decimal layer guarantees by capping coefficients at 76 digits.
inline void divmod(const U256& a, const U256& b, U256& quotient, U256& remainder) {
  require(!b.is_zero(), "division by zero");
  if (a.fits_u128() && b.fits_u128()) {
    quotient = U256::of(a.low128() / b.low128());
    remainder = U256::of(a.low128() % b.low128());
    return;
  }
  quotient = U256{};
  remainder = U256{};
  for (int index = a.bit_length() - 1; index >= 0; --index) {
    remainder = shift_left_one(remainder);
    remainder.w[0] |= a.bit(index) ? 1u : 0u;
    if (compare(remainder, b) >= 0) {
      remainder = sub(remainder, b);
      quotient.w[index / 64] |= static_cast<std::uint64_t>(1) << (index % 64);
    }
  }
}

}  // namespace quanta
