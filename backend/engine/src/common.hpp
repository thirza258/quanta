// Shared error types and checked integer arithmetic for the simulator engine.
#pragma once

#include <cstdint>
#include <stdexcept>
#include <string>

namespace quanta {

// The pedantic build rejects a bare __int128; the extension keyword keeps the
// type available on GCC and Clang without turning the warning off globally.
__extension__ typedef unsigned __int128 u128;
__extension__ typedef __int128 i128;

// Invalid input or a broken invariant. It crosses the C boundary as a message;
// the caller never receives a partially written result alongside it.
class Error : public std::runtime_error {
 public:
  using std::runtime_error::runtime_error;
};

// A refused order or account action. The message is shown to the learner as-is,
// so it has to match the wording the Python engine used.
class DomainError : public Error {
 public:
  using Error::Error;
};

[[noreturn]] inline void fail(const std::string& message) { throw Error(message); }

inline void require(bool condition, const char* message) {
  if (!condition) fail(message);
}

// Every multiplication that could leave int64 goes through one of these, so an
// overflow is reported instead of wrapping into a plausible-looking number.
inline std::int64_t checked_add(std::int64_t a, std::int64_t b) {
  std::int64_t out;
  if (__builtin_add_overflow(a, b, &out)) fail("integer overflow in addition");
  return out;
}

inline std::int64_t checked_sub(std::int64_t a, std::int64_t b) {
  std::int64_t out;
  if (__builtin_sub_overflow(a, b, &out)) fail("integer overflow in subtraction");
  return out;
}

inline std::int64_t checked_mul(std::int64_t a, std::int64_t b) {
  std::int64_t out;
  if (__builtin_mul_overflow(a, b, &out)) fail("integer overflow in multiplication");
  return out;
}

}  // namespace quanta
