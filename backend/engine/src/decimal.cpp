#include "decimal.hpp"

#include <algorithm>
#include <charconv>
#include <cmath>
#include <utility>

namespace quanta {

namespace {

constexpr int kPrecision = 28;
// Inputs are capped at 38 significant digits. Every intermediate the operations
// below form (an aligned sum, an exact product, a scaled dividend) then stays
// under 77 digits, inside 256 bits; anything larger is reported, never wrapped.
constexpr int kInputDigits = 38;
constexpr int kTableDigits = 77;
constexpr std::int64_t kMaxExponent = 1000000;

struct Powers {
  U256 value[kTableDigits + 1];
  Powers() {
    value[0] = U256::of(1);
    const U256 ten = U256::of(10);
    for (int k = 1; k <= kTableDigits; ++k) mul(value[k - 1], ten, value[k]);
  }
};

const U256& pow10(int k) {
  static const Powers table;
  require(k >= 0 && k <= kTableDigits, "decimal exponent outside the power table");
  return table.value[k];
}

int digit_count(const U256& c) {
  if (c.is_zero()) return 1;
  const int bits = c.bit_length();
  int k = ((bits - 1) * 1233) >> 12;  // floor((bits - 1) * log10(2)), never above it
  while (k + 1 <= kTableDigits && compare(c, pow10(k + 1)) >= 0) ++k;
  return k + 1;
}

U256 scale(const U256& c, std::int64_t places) {
  require(places >= 0 && places <= kTableDigits, "decimal alignment out of range");
  U256 out;
  require(mul(c, pow10(static_cast<int>(places)), out), "decimal coefficient exceeds 256 bits");
  return out;
}

U256 plus_one(const U256& c) {
  U256 out;
  require(add(c, U256::of(1), out), "decimal coefficient exceeds 256 bits");
  return out;
}

std::uint64_t mod_small(const U256& c, std::uint64_t m) {
  u128 remainder = 0;
  for (int limb = 3; limb >= 0; --limb) remainder = ((remainder << 64) | c.w[limb]) % m;
  return static_cast<std::uint64_t>(remainder);
}

U256 div_small(const U256& c, std::uint64_t d) {
  U256 out;
  u128 remainder = 0;
  for (int limb = 3; limb >= 0; --limb) {
    const u128 current = (remainder << 64) | c.w[limb];
    out.w[limb] = static_cast<std::uint64_t>(current / d);
    remainder = current % d;
  }
  return out;
}

std::int32_t checked_exponent(std::int64_t exponent) {
  require(exponent >= -kMaxExponent && exponent <= kMaxExponent, "decimal exponent out of range");
  return static_cast<std::int32_t>(exponent);
}

// Split a coefficient into the digits kept and the `drop` digits discarded.
void split(const U256& c, int drop, U256& kept, U256& rest) {
  if (drop <= 0) {
    kept = c;
    rest = U256{};
  } else if (drop > kTableDigits - 1) {
    kept = U256{};
    rest = c;
  } else {
    divmod(c, pow10(drop), kept, rest);
  }
}

// CPython's _round_* functions: 1 rounds the kept digits up, 0 means nothing was
// discarded, -1 truncates.
int decide(Rounding mode, bool negative, const U256& kept, const U256& rest, int drop) {
  if (rest.is_zero()) return 0;
  switch (mode) {
    case Rounding::Down:
      return -1;
    case Rounding::Ceiling:
      return negative ? -1 : 1;
    case Rounding::HalfUp:
    case Rounding::HalfEven: {
      // Below half whenever the discarded part is shorter than its own width.
      if (drop > kTableDigits - 1) return -1;
      const U256 half = div_small(pow10(drop), 2);
      const int c = compare(rest, half);
      if (c > 0) return 1;
      if (c < 0) return -1;
      if (mode == Rounding::HalfUp) return 1;
      return mod_small(kept, 2) == 1 ? 1 : -1;
    }
  }
  return -1;
}

// Decimal._fix under the default context: round to 28 significant digits.
Dec fix(Dec x) {
  checked_exponent(x.exponent);
  if (x.is_zero()) return x;
  const int length = digit_count(x.coefficient);
  if (length <= kPrecision) return x;
  const int drop = length - kPrecision;
  U256 kept, rest;
  split(x.coefficient, drop, kept, rest);
  std::int64_t exponent = static_cast<std::int64_t>(x.exponent) + drop;
  if (decide(Rounding::HalfEven, x.negative, kept, rest, drop) > 0) {
    kept = plus_one(kept);
    if (digit_count(kept) > kPrecision) {
      kept = div_small(kept, 10);
      ++exponent;
    }
  }
  x.coefficient = kept;
  x.exponent = checked_exponent(exponent);
  return x;
}

// Decimal._rescale: the same value at a given exponent, rounding if digits are lost.
Dec rescale(const Dec& x, std::int32_t exponent, Rounding mode) {
  if (x.is_zero()) return Dec{x.negative, U256{}, exponent};
  if (x.exponent >= exponent) {
    return Dec{x.negative, scale(x.coefficient, static_cast<std::int64_t>(x.exponent) - exponent),
               exponent};
  }
  U256 coefficient = x.coefficient;
  std::int64_t own = x.exponent;
  int length = digit_count(coefficient);
  std::int64_t keep = length + own - exponent;
  if (keep < 0) {
    // Far below the target: only its presence can matter to the rounding.
    coefficient = U256::of(1);
    own = static_cast<std::int64_t>(exponent) - 1;
    length = 1;
    keep = 0;
  }
  const int drop = static_cast<int>(length - keep);
  U256 kept, rest;
  split(coefficient, drop, kept, rest);
  if (decide(mode, x.negative, kept, rest, drop) == 1) kept = plus_one(kept);
  return Dec{x.negative, kept, exponent};
}

std::string coefficient_digits(const U256& c) {
  if (c.is_zero()) return "0";
  std::string out;
  U256 rest = c;
  const std::uint64_t chunk = 10000000000000000000ULL;  // 10^19
  while (!rest.is_zero()) {
    const std::uint64_t piece = mod_small(rest, chunk);
    rest = div_small(rest, chunk);
    std::string text = std::to_string(piece);
    if (!rest.is_zero()) text.insert(0, 19 - text.size(), '0');
    out.insert(0, text);
  }
  return out;
}

}  // namespace

int Dec::digits() const { return digit_count(coefficient); }

int Dec::adjusted() const { return exponent + digit_count(coefficient) - 1; }

Dec Dec::of(std::int64_t value) {
  Dec out;
  out.negative = value < 0;
  const u128 magnitude = value < 0 ? static_cast<u128>(-(value + 1)) + 1 : static_cast<u128>(value);
  out.coefficient = U256::of(magnitude);
  return out;
}

Dec Dec::cents(std::int64_t value) {
  Dec out = of(value);
  out.exponent = -2;
  return out;
}

Dec Dec::parse(std::string_view text) {
  std::size_t i = 0;
  const std::size_t n = text.size();
  Dec out;
  if (i < n && (text[i] == '+' || text[i] == '-')) {
    out.negative = text[i] == '-';
    ++i;
  }
  U256 coefficient;
  int significant = 0;
  int fraction = 0;
  bool any = false;
  bool dot = false;
  for (; i < n; ++i) {
    const char ch = text[i];
    if (ch == '.') {
      if (dot) fail("malformed decimal");
      dot = true;
      continue;
    }
    if (ch < '0' || ch > '9') break;
    any = true;
    if (dot) ++fraction;
    if (significant > 0 || ch != '0') {
      ++significant;
      require(significant <= kInputDigits, "decimal input has too many digits");
      U256 shifted;
      mul(coefficient, U256::of(10), shifted);
      add(shifted, U256::of(static_cast<u128>(ch - '0')), coefficient);
    }
  }
  if (!any) fail("malformed decimal");
  std::int64_t exponent = 0;
  if (i < n && (text[i] == 'e' || text[i] == 'E')) {
    ++i;
    bool negative_exponent = false;
    if (i < n && (text[i] == '+' || text[i] == '-')) {
      negative_exponent = text[i] == '-';
      ++i;
    }
    bool digits = false;
    for (; i < n && text[i] >= '0' && text[i] <= '9'; ++i) {
      digits = true;
      exponent = exponent * 10 + (text[i] - '0');
      require(exponent <= kMaxExponent, "decimal exponent out of range");
    }
    if (!digits) fail("malformed decimal");
    if (negative_exponent) exponent = -exponent;
  }
  if (i != n) fail("malformed decimal");
  out.coefficient = coefficient;
  out.exponent = checked_exponent(exponent - fraction);
  return out;
}

Dec Dec::of_double(double value) {
  require(std::isfinite(value), "a price or volume is not a finite number");
  char buffer[64];
  const auto result = std::to_chars(buffer, buffer + sizeof buffer, value);
  require(result.ec == std::errc(), "could not format a float");
  return parse(std::string_view(buffer, static_cast<std::size_t>(result.ptr - buffer)));
}

std::string Dec::str() const {
  const std::string digits = coefficient_digits(coefficient);
  const std::int64_t leftdigits = static_cast<std::int64_t>(exponent) + static_cast<std::int64_t>(digits.size());
  const std::int64_t dotplace = (exponent <= 0 && leftdigits > -6) ? leftdigits : 1;
  std::string intpart, fracpart;
  if (dotplace <= 0) {
    intpart = "0";
    fracpart = "." + std::string(static_cast<std::size_t>(-dotplace), '0') + digits;
  } else if (dotplace >= static_cast<std::int64_t>(digits.size())) {
    intpart = digits + std::string(static_cast<std::size_t>(dotplace) - digits.size(), '0');
  } else {
    intpart = digits.substr(0, static_cast<std::size_t>(dotplace));
    fracpart = "." + digits.substr(static_cast<std::size_t>(dotplace));
  }
  std::string tail;
  if (leftdigits != dotplace) {
    const std::int64_t e = leftdigits - dotplace;
    tail = std::string("E") + (e >= 0 ? "+" : "-") + std::to_string(e >= 0 ? e : -e);
  }
  return (negative ? "-" : "") + intpart + fracpart + tail;
}

int compare(const Dec& a, const Dec& b) {
  if (a.is_zero()) {
    if (b.is_zero()) return 0;
    return b.negative ? 1 : -1;
  }
  if (b.is_zero()) return a.negative ? -1 : 1;
  if (a.negative != b.negative) return a.negative ? -1 : 1;
  const int direction = a.negative ? -1 : 1;
  const int left = a.adjusted();
  const int right = b.adjusted();
  if (left != right) return left > right ? direction : -direction;
  U256 x = a.coefficient;
  U256 y = b.coefficient;
  if (a.exponent > b.exponent) x = scale(x, static_cast<std::int64_t>(a.exponent) - b.exponent);
  if (b.exponent > a.exponent) y = scale(y, static_cast<std::int64_t>(b.exponent) - a.exponent);
  const int c = quanta::compare(x, y);
  return c == 0 ? 0 : (c > 0 ? direction : -direction);
}

Dec add(const Dec& a, const Dec& b) {
  std::int32_t exponent = std::min(a.exponent, b.exponent);
  if (a.is_zero() && b.is_zero()) return fix(Dec{a.negative && b.negative, U256{}, exponent});
  if (a.is_zero()) {
    exponent = std::max<std::int64_t>(exponent, static_cast<std::int64_t>(b.exponent) - kPrecision - 1);
    return fix(rescale(b, exponent, Rounding::HalfEven));
  }
  if (b.is_zero()) {
    exponent = std::max<std::int64_t>(exponent, static_cast<std::int64_t>(a.exponent) - kPrecision - 1);
    return fix(rescale(a, exponent, Rounding::HalfEven));
  }
  // _normalize: align the exponents, replacing an operand too small to matter
  // except through rounding with the smallest value that has the same effect.
  Dec first = a;
  Dec second = b;
  Dec& larger = first.exponent < second.exponent ? second : first;
  Dec& smaller = first.exponent < second.exponent ? first : second;
  const int larger_length = digit_count(larger.coefficient);
  const int smaller_length = digit_count(smaller.coefficient);
  const std::int64_t floor =
      static_cast<std::int64_t>(larger.exponent) + std::min(-1, larger_length - kPrecision - 2);
  if (smaller_length + static_cast<std::int64_t>(smaller.exponent) - 1 < floor) {
    smaller.coefficient = U256::of(1);
    smaller.exponent = checked_exponent(floor);
  }
  larger.coefficient =
      scale(larger.coefficient, static_cast<std::int64_t>(larger.exponent) - smaller.exponent);
  larger.exponent = smaller.exponent;

  Dec result;
  result.exponent = first.exponent;
  if (first.negative != second.negative) {
    const int c = quanta::compare(first.coefficient, second.coefficient);
    if (c == 0) return fix(Dec{false, U256{}, exponent});  // equal and opposite
    const Dec& big = c > 0 ? first : second;
    const Dec& little = c > 0 ? second : first;
    result.negative = big.negative;
    result.coefficient = sub(big.coefficient, little.coefficient);
  } else {
    result.negative = first.negative;
    require(add(first.coefficient, second.coefficient, result.coefficient),
            "decimal coefficient exceeds 256 bits");
  }
  return fix(result);
}

Dec sub(const Dec& a, const Dec& b) {
  return add(a, Dec{!b.negative, b.coefficient, b.exponent});
}

Dec mul(const Dec& a, const Dec& b) {
  const bool negative = a.negative != b.negative;
  const std::int32_t exponent =
      checked_exponent(static_cast<std::int64_t>(a.exponent) + b.exponent);
  if (a.is_zero() || b.is_zero()) return fix(Dec{negative, U256{}, exponent});
  Dec out{negative, U256{}, exponent};
  require(mul(a.coefficient, b.coefficient, out.coefficient), "decimal product exceeds 256 bits");
  return fix(out);
}

Dec div(const Dec& a, const Dec& b) {
  const bool negative = a.negative != b.negative;
  if (b.is_zero()) fail(a.is_zero() ? "decimal division of zero by zero" : "decimal division by zero");
  if (a.is_zero()) {
    return fix(Dec{negative, U256{},
                   checked_exponent(static_cast<std::int64_t>(a.exponent) - b.exponent)});
  }
  const int shift = digit_count(b.coefficient) - digit_count(a.coefficient) + kPrecision + 1;
  std::int64_t exponent = static_cast<std::int64_t>(a.exponent) - b.exponent - shift;
  U256 quotient, remainder;
  if (shift >= 0) {
    divmod(scale(a.coefficient, shift), b.coefficient, quotient, remainder);
  } else {
    divmod(a.coefficient, scale(b.coefficient, -shift), quotient, remainder);
  }
  if (!remainder.is_zero()) {
    // Inexact: make sure the last digit can never be read as an exact tie.
    if (mod_small(quotient, 5) == 0) quotient = plus_one(quotient);
  } else {
    // Exact: get as close to the ideal exponent as the digits allow.
    const std::int64_t ideal = static_cast<std::int64_t>(a.exponent) - b.exponent;
    while (exponent < ideal && mod_small(quotient, 10) == 0) {
      quotient = div_small(quotient, 10);
      ++exponent;
    }
  }
  return fix(Dec{negative, quotient, checked_exponent(exponent)});
}

Dec neg(const Dec& a) {
  Dec out = a;
  out.negative = a.is_zero() ? false : !a.negative;
  return fix(out);
}

Dec abs(const Dec& a) {
  Dec out = a;
  out.negative = false;
  return fix(out);
}

Dec quantize(const Dec& value, std::int32_t exponent, Rounding rounding) {
  if (value.is_zero()) return fix(Dec{value.negative, U256{}, exponent});
  if (static_cast<std::int64_t>(value.adjusted()) - exponent + 1 > kPrecision) {
    fail("quantize result has too many digits for current context");
  }
  const Dec out = rescale(value, exponent, rounding);
  require(digit_count(out.coefficient) <= kPrecision,
          "quantize result has too many digits for current context");
  return fix(out);
}

Dec to_integral_down(const Dec& value) {
  if (value.exponent >= 0) return value;
  return rescale(value, 0, Rounding::Down);
}

std::int64_t to_int64(const Dec& value) {
  U256 magnitude;
  if (value.exponent >= 0) {
    magnitude = scale(value.coefficient, value.exponent);
  } else if (-static_cast<std::int64_t>(value.exponent) <= kTableDigits) {
    U256 rest;
    divmod(value.coefficient, pow10(-value.exponent), magnitude, rest);
  }
  require(magnitude.fits_u128() && magnitude.low128() <= static_cast<u128>(INT64_MAX),
          "decimal value does not fit in 64 bits");
  const auto out = static_cast<std::int64_t>(magnitude.low128());
  return value.negative ? -out : out;
}

std::string money(const Dec& value) { return quantize(value, -2, Rounding::HalfUp).str(); }

std::int64_t cents_of(const Dec& value) {
  const Dec exact = quantize(value, -2, Rounding::Down);
  require(exact == value, "value is not a whole number of cents");
  return to_int64(Dec{exact.negative, exact.coefficient, 0});
}

}  // namespace quanta
