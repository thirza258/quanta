// Exact decimal arithmetic with the semantics of Python's decimal module under
// its default context: 28 significant digits, ROUND_HALF_EVEN, signed zeros.
//
// Money in the engine is integer cents, but the account rules multiply cents by
// configured rates (slippage, spread, participation, a trailing percentage, a
// borrow rate) and divide totals by quantities. The Python engine did that in
// Decimal, and stored runs carry the results, so this type reproduces Decimal
// exactly rather than approximately: the same 28-digit rounding after every
// operation, the same rounding modes for quantize, the same sign on a zero.
// It follows the General Decimal Arithmetic specification as CPython's
// _pydecimal implements it, which is what the differential tests compare to.
#pragma once

#include <cstdint>
#include <string>
#include <string_view>

#include "u256.hpp"

namespace quanta {

enum class Rounding { Down, HalfUp, HalfEven, Ceiling };

struct Dec {
  bool negative = false;  // also set for negative zero
  U256 coefficient;
  std::int32_t exponent = 0;

  static Dec parse(std::string_view text);  // Decimal(str): exact, no rounding
  static Dec of(std::int64_t value);        // Decimal(int)
  static Dec cents(std::int64_t value);     // value / 100, exactly
  static Dec of_double(double value);       // Decimal(str(float)): the shortest repr

  bool is_zero() const { return coefficient.is_zero(); }
  int digits() const;    // len(str(coefficient))
  int adjusted() const;  // exponent of the most significant digit

  std::string str() const;  // str(Decimal)
};

int compare(const Dec& a, const Dec& b);
inline bool operator<(const Dec& a, const Dec& b) { return compare(a, b) < 0; }
inline bool operator>(const Dec& a, const Dec& b) { return compare(a, b) > 0; }
inline bool operator<=(const Dec& a, const Dec& b) { return compare(a, b) <= 0; }
inline bool operator>=(const Dec& a, const Dec& b) { return compare(a, b) >= 0; }
inline bool operator==(const Dec& a, const Dec& b) { return compare(a, b) == 0; }
inline bool operator!=(const Dec& a, const Dec& b) { return compare(a, b) != 0; }

// Context arithmetic: the exact result, rounded to 28 significant digits.
Dec add(const Dec& a, const Dec& b);
Dec sub(const Dec& a, const Dec& b);
Dec mul(const Dec& a, const Dec& b);
Dec div(const Dec& a, const Dec& b);
Dec neg(const Dec& a);  // unary minus: -Decimal('0') is Decimal('0')
Dec abs(const Dec& a);

inline Dec operator+(const Dec& a, const Dec& b) { return add(a, b); }
inline Dec operator-(const Dec& a, const Dec& b) { return sub(a, b); }
inline Dec operator*(const Dec& a, const Dec& b) { return mul(a, b); }
inline Dec operator/(const Dec& a, const Dec& b) { return div(a, b); }
inline Dec operator-(const Dec& a) { return neg(a); }

// Python's max(a, b) and min(a, b): the first argument wins a tie.
inline const Dec& max_of(const Dec& a, const Dec& b) { return b > a ? b : a; }
inline const Dec& min_of(const Dec& a, const Dec& b) { return b < a ? b : a; }

// Decimal.quantize(Decimal(10) ** exponent, rounding). Throws when the result
// would need more than 28 digits, as Decimal raises InvalidOperation.
Dec quantize(const Dec& value, std::int32_t exponent, Rounding rounding);
Dec to_integral_down(const Dec& value);
std::int64_t to_int64(const Dec& value);  // int(Decimal): truncates toward zero

// money(): str(value.quantize(Decimal("0.01"), ROUND_HALF_UP)).
std::string money(const Dec& value);
// Integer cents of a value already quantized to hundredths.
std::int64_t cents_of(const Dec& value);

}  // namespace quanta
