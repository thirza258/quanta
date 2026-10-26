// Random streams that reproduce numpy's and CPython's bit for bit.
//
// A generated market is a pure function of its seed, and runs already stored in
// the database hold cursors, orders and fills against bars the Python engine
// produced. Replacing the engine is only safe if every draw is the same, so these
// are transcriptions of the published algorithms rather than "equivalent" ones:
//
// - numpy.random.default_rng(entropy): SeedSequence pool mixing (after Melissa
//   O'Neill's seed_seq_fe), PCG64 (XSL-RR output, 128-bit LCG) and numpy's
//   ziggurat standard normal.
// - random.Random(seed): MT19937 seeded through init_by_array, with CPython's
//   53-bit random(), Box-Muller gauss() and getrandbits-based randint().
#pragma once

#include <cstdint>
#include <vector>

#include "common.hpp"

namespace quanta {

class Pcg64 {
 public:
  // Entropy as numpy coerces a list of non-negative Python ints: each value is
  // split into 32-bit words, least significant first, and the lists concatenated.
  explicit Pcg64(const std::vector<std::uint64_t>& entropy);

  std::uint64_t next64();
  double next_double();
  double standard_normal();
  // Generator.normal(loc, scale): loc + scale * z, evaluated in that order.
  double normal(double loc, double scale) { return loc + scale * standard_normal(); }

 private:
  u128 state_ = 0;
  u128 increment_ = 0;
};

class PythonRandom {
 public:
  // random.Random(seed) for a non-negative int seed.
  explicit PythonRandom(std::uint64_t seed);

  std::uint32_t next32();
  double random();
  double gauss(double mu, double sigma);
  std::uint32_t getrandbits(int bits);
  std::uint64_t randbelow(std::uint64_t n);
  std::int64_t randint(std::int64_t low, std::int64_t high);

 private:
  static constexpr int kStateSize = 624;
  std::uint32_t mt_[kStateSize];
  int index_ = kStateSize + 1;
  bool has_gauss_ = false;
  double gauss_next_ = 0.0;

  void init_genrand(std::uint32_t seed);
  void init_by_array(const std::uint32_t* key, std::size_t length);
};

}  // namespace quanta
