#include "numeric.hpp"

#include <cmath>
#include <vector>

#include "common.hpp"

namespace quanta::numeric {

namespace {
constexpr std::int64_t kBlockSize = 128;  // numpy's PW_BLOCKSIZE
}

double pairwise_sum(const double* a, std::int64_t n) {
  if (n < 8) {
    double res = 0.0;
    for (std::int64_t i = 0; i < n; ++i) res += a[i];
    return res;
  }
  if (n <= kBlockSize) {
    double r[8];
    for (int j = 0; j < 8; ++j) r[j] = a[j];
    std::int64_t i = 8;
    for (; i < n - (n % 8); i += 8) {
      for (int j = 0; j < 8; ++j) r[j] += a[i + j];
    }
    double res = ((r[0] + r[1]) + (r[2] + r[3])) + ((r[4] + r[5]) + (r[6] + r[7]));
    for (; i < n; ++i) res += a[i];
    return res;
  }
  // Divide by two, keeping the first half a multiple of the unroll factor.
  std::int64_t n2 = n / 2;
  n2 -= n2 % 8;
  return pairwise_sum(a, n2) + pairwise_sum(a + n2, n - n2);
}

double var(const double* a, std::int64_t n) {
  const double average = mean(a, n);
  std::vector<double> squares(static_cast<std::size_t>(n));
  for (std::int64_t i = 0; i < n; ++i) {
    const double deviation = a[i] - average;
    squares[static_cast<std::size_t>(i)] = deviation * deviation;
  }
  return sum(squares.data(), n) / static_cast<double>(n);
}

std::int64_t python_round_hundredths(double x) {
  require(std::isfinite(x), "cannot round a non-finite price");
  if (x == 0.0) return 0;
  int exponent = 0;
  const double fraction = std::frexp(x, &exponent);
  // x == mantissa * 2^(exponent - 53), with the mantissa a 53-bit integer.
  const auto mantissa = static_cast<std::int64_t>(std::ldexp(fraction, 53));
  const bool negative = mantissa < 0;
  const u128 scaled = static_cast<u128>(negative ? -mantissa : mantissa) * 100u;
  const int shift = 53 - exponent;
  u128 quotient;
  if (shift <= 0) {
    // |x| >= 2^53 is already an integer, and every integer is its own rounding.
    require(shift > -10, "price is too large to round");
    quotient = scaled << -shift;
  } else if (shift >= 127) {
    quotient = 0;
  } else {
    quotient = scaled >> shift;
    const u128 remainder = scaled - (quotient << shift);
    const u128 half = static_cast<u128>(1) << (shift - 1);
    if (remainder > half || (remainder == half && (quotient & 1u))) quotient += 1;
  }
  require(quotient < (static_cast<u128>(1) << 53), "price is too large to round");
  const auto hundredths = static_cast<std::int64_t>(quotient);
  return negative ? -hundredths : hundredths;
}

}  // namespace quanta::numeric
