#include "rng.hpp"

#include <array>
#include <cmath>

#include "libm.hpp"
#include "ziggurat_tables.hpp"

namespace quanta {

namespace {

// SeedSequence constants (numpy/random/bit_generator.pyx).
constexpr std::uint32_t kInitA = 0x43b0d7e5u;
constexpr std::uint32_t kMultA = 0x931e8875u;
constexpr std::uint32_t kInitB = 0x8b51f9ddu;
constexpr std::uint32_t kMultB = 0x58f38dedu;
constexpr std::uint32_t kMixMultL = 0xca01f9ddu;
constexpr std::uint32_t kMixMultR = 0x4973f715u;
constexpr int kXShift = 16;
constexpr int kPoolSize = 4;

std::uint32_t hashmix(std::uint32_t value, std::uint32_t& hash_const) {
  value ^= hash_const;
  hash_const *= kMultA;
  value *= hash_const;
  value ^= value >> kXShift;
  return value;
}

std::uint32_t mix(std::uint32_t x, std::uint32_t y) {
  std::uint32_t result = kMixMultL * x - kMixMultR * y;
  result ^= result >> kXShift;
  return result;
}

// SeedSequence(entropy).generate_state(4, np.uint64), as PCG64 asks for it.
std::array<std::uint64_t, 4> seed_state(const std::vector<std::uint64_t>& entropy) {
  std::vector<std::uint32_t> words;
  for (std::uint64_t value : entropy) {
    if (value == 0) {
      words.push_back(0);
      continue;
    }
    while (value > 0) {
      words.push_back(static_cast<std::uint32_t>(value & 0xffffffffu));
      value >>= 32;
    }
  }
  std::uint32_t pool[kPoolSize];
  std::uint32_t hash_const = kInitA;
  for (int i = 0; i < kPoolSize; ++i) {
    const std::uint32_t word = static_cast<std::size_t>(i) < words.size() ? words[i] : 0u;
    pool[i] = hashmix(word, hash_const);
  }
  for (int source = 0; source < kPoolSize; ++source) {
    for (int target = 0; target < kPoolSize; ++target) {
      if (source != target) pool[target] = mix(pool[target], hashmix(pool[source], hash_const));
    }
  }
  for (std::size_t source = kPoolSize; source < words.size(); ++source) {
    for (int target = 0; target < kPoolSize; ++target) {
      pool[target] = mix(pool[target], hashmix(words[source], hash_const));
    }
  }
  std::uint32_t state[8];
  std::uint32_t hash_b = kInitB;
  for (int i = 0; i < 8; ++i) {
    std::uint32_t value = pool[i % kPoolSize];
    value ^= hash_b;
    hash_b *= kMultB;
    value *= hash_b;
    value ^= value >> kXShift;
    state[i] = value;
  }
  std::array<std::uint64_t, 4> out{};
  for (int i = 0; i < 4; ++i) {
    out[i] = static_cast<std::uint64_t>(state[2 * i]) |
             (static_cast<std::uint64_t>(state[2 * i + 1]) << 32);
  }
  return out;
}

const u128 kPcgMultiplier =
    (static_cast<u128>(2549297995355413924ULL) << 64) | 4865540595714422341ULL;

}  // namespace

Pcg64::Pcg64(const std::vector<std::uint64_t>& entropy) {
  const auto seed = seed_state(entropy);
  const u128 initial_state = (static_cast<u128>(seed[0]) << 64) | seed[1];
  const u128 initial_sequence = (static_cast<u128>(seed[2]) << 64) | seed[3];
  increment_ = (initial_sequence << 1u) | 1u;
  state_ = 0;
  state_ = state_ * kPcgMultiplier + increment_;
  state_ += initial_state;
  state_ = state_ * kPcgMultiplier + increment_;
}

std::uint64_t Pcg64::next64() {
  state_ = state_ * kPcgMultiplier + increment_;
  const auto high = static_cast<std::uint64_t>(state_ >> 64);
  const auto low = static_cast<std::uint64_t>(state_);
  const std::uint64_t value = high ^ low;
  const unsigned rotation = static_cast<unsigned>(state_ >> 122u);
  return (value >> rotation) | (value << ((64u - rotation) & 63u));
}

double Pcg64::next_double() {
  return static_cast<double>(next64() >> 11) * (1.0 / 9007199254740992.0);
}

// numpy's random_standard_normal (numpy/random/src/distributions/distributions.c).
double Pcg64::standard_normal() {
  for (;;) {
    std::uint64_t r = next64();
    const int idx = static_cast<int>(r & 0xff);
    r >>= 8;
    const std::uint64_t sign = r & 0x1;
    const std::uint64_t rabs = (r >> 1) & 0x000fffffffffffffULL;
    double x = static_cast<double>(rabs) * ziggurat::wi[idx];
    if (sign & 0x1) x = -x;
    if (rabs < ziggurat::ki[idx]) return x;  // the common case
    if (idx == 0) {
      for (;;) {
        // 1 - U keeps log away from zero.
        const double xx = -ziggurat::kInvR * libm::log1p(-next_double());
        const double yy = -libm::log1p(-next_double());
        if (yy + yy > xx * xx) {
          return ((rabs >> 8) & 0x1) ? -(ziggurat::kR + xx) : ziggurat::kR + xx;
        }
      }
    }
    const double wedge = (ziggurat::fi[idx - 1] - ziggurat::fi[idx]) * next_double();
    if (wedge + ziggurat::fi[idx] < libm::exp(-0.5 * x * x)) return x;
  }
}

PythonRandom::PythonRandom(std::uint64_t seed) {
  // CPython splits abs(seed) into 32-bit words from the right; zero is one word.
  std::uint32_t key[2] = {static_cast<std::uint32_t>(seed & 0xffffffffu),
                          static_cast<std::uint32_t>(seed >> 32)};
  init_by_array(key, (seed >> 32) ? 2 : 1);
}

void PythonRandom::init_genrand(std::uint32_t seed) {
  mt_[0] = seed;
  for (int i = 1; i < kStateSize; ++i) {
    mt_[i] = 1812433253u * (mt_[i - 1] ^ (mt_[i - 1] >> 30)) + static_cast<std::uint32_t>(i);
  }
  index_ = kStateSize;
}

void PythonRandom::init_by_array(const std::uint32_t* key, std::size_t length) {
  init_genrand(19650218u);
  std::size_t i = 1;
  std::size_t j = 0;
  for (std::size_t k = (kStateSize > length ? kStateSize : length); k; --k) {
    mt_[i] = (mt_[i] ^ ((mt_[i - 1] ^ (mt_[i - 1] >> 30)) * 1664525u)) + key[j] +
             static_cast<std::uint32_t>(j);
    ++i;
    ++j;
    if (i >= kStateSize) {
      mt_[0] = mt_[kStateSize - 1];
      i = 1;
    }
    if (j >= length) j = 0;
  }
  for (std::size_t k = kStateSize - 1; k; --k) {
    mt_[i] = (mt_[i] ^ ((mt_[i - 1] ^ (mt_[i - 1] >> 30)) * 1566083941u)) -
             static_cast<std::uint32_t>(i);
    ++i;
    if (i >= kStateSize) {
      mt_[0] = mt_[kStateSize - 1];
      i = 1;
    }
  }
  mt_[0] = 0x80000000u;
}

std::uint32_t PythonRandom::next32() {
  constexpr int kM = 397;
  constexpr std::uint32_t kMatrixA = 0x9908b0dfu;
  constexpr std::uint32_t kUpper = 0x80000000u;
  constexpr std::uint32_t kLower = 0x7fffffffu;
  static const std::uint32_t mag01[2] = {0x0u, kMatrixA};
  if (index_ >= kStateSize) {
    int kk = 0;
    std::uint32_t y;
    for (; kk < kStateSize - kM; ++kk) {
      y = (mt_[kk] & kUpper) | (mt_[kk + 1] & kLower);
      mt_[kk] = mt_[kk + kM] ^ (y >> 1) ^ mag01[y & 0x1u];
    }
    for (; kk < kStateSize - 1; ++kk) {
      y = (mt_[kk] & kUpper) | (mt_[kk + 1] & kLower);
      mt_[kk] = mt_[kk + (kM - kStateSize)] ^ (y >> 1) ^ mag01[y & 0x1u];
    }
    y = (mt_[kStateSize - 1] & kUpper) | (mt_[0] & kLower);
    mt_[kStateSize - 1] = mt_[kM - 1] ^ (y >> 1) ^ mag01[y & 0x1u];
    index_ = 0;
  }
  std::uint32_t y = mt_[index_++];
  y ^= (y >> 11);
  y ^= (y << 7) & 0x9d2c5680u;
  y ^= (y << 15) & 0xefc60000u;
  y ^= (y >> 18);
  return y;
}

double PythonRandom::random() {
  const std::uint32_t a = next32() >> 5;
  const std::uint32_t b = next32() >> 6;
  return (a * 67108864.0 + b) * (1.0 / 9007199254740992.0);
}

double PythonRandom::gauss(double mu, double sigma) {
  double z;
  if (has_gauss_) {
    z = gauss_next_;
    has_gauss_ = false;
  } else {
    constexpr double kTwoPi = 2.0 * 3.141592653589793;
    const double x2pi = random() * kTwoPi;
    const double g2rad = std::sqrt(-2.0 * libm::log(1.0 - random()));
    z = libm::cos(x2pi) * g2rad;
    gauss_next_ = libm::sin(x2pi) * g2rad;
    has_gauss_ = true;
  }
  return mu + z * sigma;
}

std::uint32_t PythonRandom::getrandbits(int bits) {
  require(bits > 0 && bits <= 32, "getrandbits supports 1 to 32 bits");
  return next32() >> (32 - bits);
}

std::uint64_t PythonRandom::randbelow(std::uint64_t n) {
  require(n > 0 && n <= 0xffffffffULL, "randbelow supports 1 to 2^32 - 1");
  int bits = 0;
  for (std::uint64_t v = n; v; v >>= 1) ++bits;
  std::uint64_t r = getrandbits(bits);
  while (r >= n) r = getrandbits(bits);
  return r;
}

std::int64_t PythonRandom::randint(std::int64_t low, std::int64_t high) {
  require(high >= low, "empty range for randint");
  return low + static_cast<std::int64_t>(randbelow(static_cast<std::uint64_t>(high - low) + 1));
}

}  // namespace quanta
