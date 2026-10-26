#include "libm.hpp"

#include <math.h>

namespace quanta::libm {

double (*volatile exp_fn)(double) = ::exp;
double (*volatile log_fn)(double) = ::log;
double (*volatile log1p_fn)(double) = ::log1p;
double (*volatile pow_fn)(double, double) = ::pow;
double (*volatile sin_fn)(double) = ::sin;
double (*volatile cos_fn)(double) = ::cos;

}  // namespace quanta::libm
