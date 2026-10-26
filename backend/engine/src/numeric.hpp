// Floating-point reductions and rounding, in the exact order numpy and CPython
// perform them.
//
// Floating-point addition is not associative, so "the sum" of an array is only
// reproducible if the additions happen in the same order. numpy reduces a
// contiguous 1-D float64 array by pairwise summation with eight accumulators;
// reducing a C-ordered 2-D array over axis 0 adds the rows one at a time. Both
// orders were checked against numpy 2.5.3 before this was written.
#pragma once

#include <cstdint>

namespace quanta::numeric {

// numpy's DOUBLE_pairwise_sum (numpy/_core/src/umath/loops_utils.h.src).
double pairwise_sum(const double* a, std::int64_t n);

// ndarray.sum(): the reduction starts from the additive identity.
inline double sum(const double* a, std::int64_t n) { return 0.0 + pairwise_sum(a, n); }

// ndarray.mean(): the sum, then one true division by the count.
inline double mean(const double* a, std::int64_t n) {
  return sum(a, n) / static_cast<double>(n);
}

// ndarray.var() with ddof=0: the mean, squared deviations, their mean.
double var(const double* a, std::int64_t n);

// round(x, 2) for a Python float, returned as the integer number of hundredths.
// CPython rounds the exact binary value of x to two places (ties to even) and
// reads that decimal back, so round(x, 2) == result / 100.0 exactly.
std::int64_t python_round_hundredths(double x);

}  // namespace quanta::numeric
