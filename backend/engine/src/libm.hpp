// The C library's transcendental functions, called at run time.
//
// The generated market has to match numpy and CPython bit for bit, and both of
// them evaluate exp, log, pow and the trigonometric functions through the C
// library while the program runs. A compiler may fold a call with a constant
// argument at build time, or rewrite pow(x, 2.0) as x * x; either answer can
// differ from the library's in the last place, and one cent of difference is a
// different market. Calling through pointers the optimizer cannot see through
// keeps every evaluation a real library call.
#pragma once

namespace quanta::libm {

extern double (*volatile exp_fn)(double);
extern double (*volatile log_fn)(double);
extern double (*volatile log1p_fn)(double);
extern double (*volatile pow_fn)(double, double);
extern double (*volatile sin_fn)(double);
extern double (*volatile cos_fn)(double);

inline double exp(double x) { return exp_fn(x); }
inline double log(double x) { return log_fn(x); }
inline double log1p(double x) { return log1p_fn(x); }
inline double pow(double x, double y) { return pow_fn(x, y); }
inline double sin(double x) { return sin_fn(x); }
inline double cos(double x) { return cos_fn(x); }

}  // namespace quanta::libm
