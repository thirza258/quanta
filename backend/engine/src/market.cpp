#include "market.hpp"

#include <algorithm>
#include <climits>
#include <cmath>
#include <vector>

#include "calendar.hpp"
#include "common.hpp"
#include "libm.hpp"
#include "numeric.hpp"
#include "parallel.hpp"
#include "rng.hpp"

namespace quanta::market {

namespace {

constexpr double kMarketVol = 0.15;
constexpr double kSectorVol = 0.11;
constexpr double kSectorLoad = 0.62;
constexpr double kPoint = 0.0001;  // one point is one basis point
constexpr std::uint64_t kBlockStream = 0x9E3779B9ULL;
constexpr std::int64_t kOpenings = kBlockSessions;

using Series = std::vector<double>;

// Every expression below is written in the order numpy evaluates the Python
// it replaces, one rounding per operation: (a * b) * c is not a * (b * c) in
// floating point, and the build disables fused multiply-add for the same reason.

// U-shaped intraday profile: busiest at the open, firm again into the close.
Series shape(double floor, double open_weight, double open_scale, double close_weight,
             double close_scale) {
  Series out(kBlockBars);
  for (std::int64_t i = 0; i < kBlockBars; ++i) {
    const std::int64_t minute = i % kSessionBars;
    const double opening = libm::exp(static_cast<double>(-minute) / open_scale);
    const double closing =
        libm::exp(static_cast<double>(-(kSessionBars - 1 - minute)) / close_scale);
    out[i] = (floor + open_weight * opening) + close_weight * closing;
  }
  return out;
}

// Rescale a positive multiplier to unit mean square.
void unit(Series& series) {
  const auto n = static_cast<std::int64_t>(series.size());
  Series squares(series.size());
  for (std::int64_t i = 0; i < n; ++i) squares[i] = series[i] * series[i];
  const double scale = std::sqrt(numeric::mean(squares.data(), n));
  for (std::int64_t i = 0; i < n; ++i) series[i] = series[i] / scale;
}

// AR(1) log-variance over one column, normalized to unit mean square: the
// quiet and busy stretches of the market factor.
Series persistence(const Series& noise, double phi) {
  const auto n = static_cast<std::int64_t>(noise.size());
  Series level(noise.size(), 0.0);
  for (std::int64_t t = 1; t < n; ++t) level[t] = phi * level[t - 1] + noise[t];
  Series multiplier(noise.size());
  for (std::int64_t t = 0; t < n; ++t) multiplier[t] = libm::exp(level[t]);
  unit(multiplier);
  return multiplier;
}

// The same process for every company at once, stored [bar][company]. numpy
// averages a C-ordered 2-D array over axis 0 by adding whole rows in turn, so
// each column's mean square accumulates bar by bar from zero.
Series persistence(const Series& noise, std::int64_t rows, std::int64_t columns, double phi) {
  Series level(noise.size(), 0.0);
  for (std::int64_t t = 1; t < rows; ++t) {
    for (std::int64_t j = 0; j < columns; ++j) {
      level[t * columns + j] = phi * level[(t - 1) * columns + j] + noise[t * columns + j];
    }
  }
  Series multiplier(noise.size());
  for (std::size_t i = 0; i < noise.size(); ++i) multiplier[i] = libm::exp(level[i]);
  std::vector<double> total(static_cast<std::size_t>(columns), 0.0);
  for (std::int64_t t = 0; t < rows; ++t) {
    for (std::int64_t j = 0; j < columns; ++j) {
      const double value = multiplier[t * columns + j];
      total[j] = total[j] + value * value;
    }
  }
  std::vector<double> scale(static_cast<std::size_t>(columns));
  for (std::int64_t j = 0; j < columns; ++j) {
    scale[j] = std::sqrt(total[j] / static_cast<double>(rows));
  }
  for (std::int64_t t = 0; t < rows; ++t) {
    for (std::int64_t j = 0; j < columns; ++j) {
      multiplier[t * columns + j] = multiplier[t * columns + j] / scale[j];
    }
  }
  return multiplier;
}

double magnitude_of(const Shock& shock) {
  return static_cast<double>(shock.points < 0 ? -shock.points : shock.points) * kPoint;
}

// Spread `amount` over an exponentially decaying window from `start`.
void drift(Series& target, std::int64_t start, std::int64_t span, double amount) {
  const std::int64_t end = std::min<std::int64_t>(kBlockBars, start + span);
  if (end <= start) return;
  const double scale = std::max(static_cast<double>(span) / 3.0, 1.0);
  Series weights(static_cast<std::size_t>(end - start));
  for (std::int64_t k = 0; k < end - start; ++k) {
    weights[k] = libm::exp(static_cast<double>(-k) / scale);
  }
  const double total = numeric::sum(weights.data(), end - start);
  if (total == 0.0) return;
  for (std::int64_t k = 0; k < end - start; ++k) {
    target[start + k] += amount * (weights[k] / total);
  }
}

// A scored shock: 58% on the bar the headline is dated, the rest drifting after.
void impulse(Series& target, const Shock& shock) {
  const double magnitude = magnitude_of(shock);
  const double sign = static_cast<double>(shock.sign);
  target[shock.index] += (0.58 * magnitude) * sign;
  drift(target, shock.index + 1, shock.span, (0.42 * magnitude) * sign);
}

// Raise modeled volatility and traded volume around a shock, then decay.
void excite(Series& volatility, Series& activity, std::int64_t index, double magnitude,
            std::int64_t span, double scale) {
  const std::int64_t stop = std::min<std::int64_t>(kBlockBars, index + span);
  const double weight = (scale * magnitude) / 0.02;
  const double vol_amount = std::min(3.0, weight);
  const double vlm_amount = std::min(6.0, 2.2 * weight);
  const double vol_decay = std::max(static_cast<double>(span) / 4.0, 1.0);
  const double vlm_decay = std::max(static_cast<double>(span) / 5.0, 1.0);
  for (std::int64_t k = 0; k < stop - index; ++k) {
    volatility[index + k] += vol_amount * libm::exp(static_cast<double>(-k) / vol_decay);
  }
  for (std::int64_t k = 0; k < stop - index; ++k) {
    activity[index + k] += vlm_amount * libm::exp(static_cast<double>(-k) / vlm_decay);
  }
}

std::int32_t printed(double value) {
  const double scaled = std::nearbyint(std::max(value, 0.01) * 100.0);
  require(std::isfinite(scaled) && scaled <= static_cast<double>(INT32_MAX),
          "a generated price left the int32 cent range");
  return static_cast<std::int32_t>(scaled);
}

std::int32_t traded(double value) {
  const double rounded = std::max(std::nearbyint(value), 100.0);
  require(std::isfinite(rounded) && rounded <= static_cast<double>(INT32_MAX),
          "a generated volume left the int32 range");
  return static_cast<std::int32_t>(rounded);
}

void validate(const BlockInput& in, const BlockOutput& out) {
  require(in.companies && in.carry && out.cents && out.volume && out.carry,
          "block generation needs every input and output buffer");
  require(in.company_count > 0 && in.company_count <= 4096, "company count out of range");
  require(in.sector_count > 0 && in.sector_count <= 4096, "sector count out of range");
  require(in.first_session >= 0 && in.first_session <= 4000000, "first session out of range");
  require(in.shock_count >= 0 && in.shock_count <= 10000000, "shock count out of range");
  require(in.shock_count == 0 || in.shocks, "shocks are missing");
  for (std::int32_t j = 0; j < in.company_count; ++j) {
    const Company& c = in.companies[j];
    require(std::isfinite(c.beta) && std::fabs(c.beta) <= 100, "company beta out of range");
    require(std::isfinite(c.volatility) && c.volatility >= 0 && c.volatility <= 100,
            "company volatility out of range");
    require(std::isfinite(c.volume) && c.volume >= 0 && c.volume <= 1e9,
            "company volume out of range");
    require(c.sector >= 0 && c.sector < in.sector_count, "company sector out of range");
    require(std::isfinite(in.carry[j]) && in.carry[j] > 0 && in.carry[j] < 2e7,
            "opening price out of range");
  }
  for (std::int64_t k = 0; k < in.shock_count; ++k) {
    const Shock& s = in.shocks[k];
    require(s.scope >= 0 && s.scope <= 2, "shock scope must be market, sector or company");
    require(s.scope != 1 || (s.target >= 0 && s.target < in.sector_count), "shock sector out of range");
    require(s.scope != 2 || (s.target >= 0 && s.target < in.company_count),
            "shock company out of range");
    require(s.index >= 0 && s.index < kBlockBars, "shock bar outside the block");
    require(s.points >= -1000000 && s.points <= 1000000, "shock points out of range");
    require(s.sign == 1 || s.sign == -1, "shock sign must be +1 or -1");
    require(s.span >= 0 && s.span <= 1000000, "shock span out of range");
  }
}

}  // namespace

void generate_block(const BlockInput& in, const BlockOutput& out) {
  validate(in, out);
  const std::int64_t bars = kBlockBars;
  const std::int64_t companies = in.company_count;
  const std::int64_t sectors = in.sector_count;

  Series price_shape = shape(0.55, 1.35, 45.0, 0.85, 55.0);
  unit(price_shape);
  const Series volume_shape = shape(0.50, 1.80, 35.0, 1.10, 40.0);
  const double per_bar = 1.0 / std::sqrt(static_cast<double>(252 * kSessionBars));

  // The market and sector shock paths are read by every company, so they are
  // built first. A company's own path, volatility and volume are built inside
  // its task below; each array still sees its shocks in schedule order.
  Series market_story(bars, 0.0);
  std::vector<Series> sector_story(static_cast<std::size_t>(sectors), Series(bars, 0.0));
  for (std::int64_t k = 0; k < in.shock_count; ++k) {
    const Shock& shock = in.shocks[k];
    if (shock.scope == 0) impulse(market_story, shock);
    if (shock.scope == 1) impulse(sector_story[shock.target], shock);
  }

  // Every draw happens here, on one stream, in the order the Python generator
  // made them. The stream is sequential by construction: the ziggurat consumes
  // a variable number of words per normal, so no draw can be located without
  // making the ones before it.
  Pcg64 rng({in.seed, static_cast<std::uint64_t>(in.first_session), kBlockStream});
  Series market_level_noise(bars);
  for (auto& v : market_level_noise) v = rng.normal(0.0, 0.055);
  Series market_draws(bars);
  for (auto& v : market_draws) v = rng.standard_normal();
  Series gap_draws(kOpenings);
  for (auto& v : gap_draws) v = rng.standard_normal();
  std::vector<Series> sector_draws(static_cast<std::size_t>(sectors), Series(bars));
  for (auto& series : sector_draws) {
    for (auto& v : series) v = rng.standard_normal();
  }
  Series cluster_noise(static_cast<std::size_t>(bars * companies));
  for (auto& v : cluster_noise) v = rng.normal(0.0, 0.05);
  Series idio_draws(static_cast<std::size_t>(bars * companies));
  for (auto& v : idio_draws) v = rng.standard_normal();
  struct Draws {
    Series gap, upper, lower, turnover;
  };
  std::vector<Draws> draws(static_cast<std::size_t>(companies));
  for (auto& d : draws) {
    d.gap.resize(kOpenings);
    for (auto& v : d.gap) v = rng.standard_normal();
    d.upper.resize(bars);
    for (auto& v : d.upper) v = rng.standard_normal();
    d.lower.resize(bars);
    for (auto& v : d.lower) v = rng.standard_normal();
    d.turnover.resize(bars);
    for (auto& v : d.turnover) v = rng.normal(0.0, 0.35);
  }

  // One market factor, one factor per sector, then company-specific noise.
  const double market_vol = kMarketVol * per_bar;
  const Series market_persistence = persistence(market_level_noise, 0.985);
  Series market_noise(bars);
  for (std::int64_t i = 0; i < bars; ++i) {
    market_noise[i] = ((market_vol * price_shape[i]) * market_persistence[i]) * market_draws[i];
  }
  // Overnight gaps carry more of the move than a single minute inside a session.
  for (std::int64_t k = 0; k < kOpenings; ++k) {
    market_noise[k * kSessionBars] += (2.6 * market_vol) * gap_draws[k];
  }
  std::vector<Series> sector_noise(static_cast<std::size_t>(sectors), Series(bars));
  for (std::int64_t s = 0; s < sectors; ++s) {
    for (std::int64_t i = 0; i < bars; ++i) {
      sector_noise[s][i] = ((kSectorVol * per_bar) * price_shape[i]) * sector_draws[s][i];
    }
  }
  const Series clustering = persistence(cluster_noise, bars, companies, 0.992);

  // Companies are independent from here on. Each task reads the shared series
  // above and writes only its own slice of the outputs.
  parallel_for(companies, in.workers, [&](std::int64_t j) {
    const Company& company = in.companies[j];
    const Draws& d = draws[j];
    Series own_story(bars, 0.0), volatility(bars, 0.0), activity(bars, 0.0);
    for (std::int64_t k = 0; k < in.shock_count; ++k) {
      const Shock& shock = in.shocks[k];
      const double magnitude = magnitude_of(shock);
      if (shock.scope == 2 && shock.target == j) {
        impulse(own_story, shock);
        excite(volatility, activity, shock.index, magnitude, shock.span, 1.0);
      } else if (shock.scope == 1 && shock.target == company.sector) {
        excite(volatility, activity, shock.index, magnitude, shock.span, 0.7);
      } else if (shock.scope == 0) {
        excite(volatility, activity, shock.index, magnitude, std::min(shock.span, 200), 0.9);
      }
    }

    Series excited(bars);
    for (std::int64_t i = 0; i < bars; ++i) excited[i] = 1.0 + volatility[i];
    unit(excited);
    const Series& sector_path = sector_noise[company.sector];
    const Series& sector_shock = sector_story[company.sector];
    Series factors(bars), story(bars);
    for (std::int64_t i = 0; i < bars; ++i) {
      factors[i] = company.beta * market_noise[i] + kSectorLoad * sector_path[i];
      story[i] = (company.beta * market_story[i] + kSectorLoad * sector_shock[i]) + own_story[i];
    }
    // Calibrated in annualized volatility and carved out of the company's own
    // budget, so a stock's realized volatility stays near its stated level.
    const double budget = libm::pow(company.volatility * per_bar, 2.0);
    const double spare = (budget - numeric::var(factors.data(), bars)) -
                         numeric::var(story.data(), bars);
    const double idio = std::sqrt(spare >= 0.25 * budget ? spare : 0.25 * budget);

    Series returns(bars);
    for (std::int64_t i = 0; i < bars; ++i) {
      const double noise = (((idio * price_shape[i]) * clustering[i * companies + j]) * excited[i]) *
                           idio_draws[i * companies + j];
      returns[i] = (factors[i] + story[i]) + noise;
    }
    for (std::int64_t k = 0; k < kOpenings; ++k) {
      const std::int64_t i = k * kSessionBars;
      returns[i] += ((1.9 * idio) * excited[i]) * d.gap[k];
    }
    // Remove the Ito drift so a flat expectation stays flat over the block.
    const double drift_correction = 0.5 * numeric::var(returns.data(), bars);
    for (std::int64_t i = 0; i < bars; ++i) {
      returns[i] = std::min(std::max(returns[i] - drift_correction, -0.25), 0.25);
    }

    const double opened = in.carry[j];
    std::int32_t* cents = out.cents + j * 4 * bars;
    std::int32_t* volume = out.volume + j * bars;
    double cumulative = 0.0;
    double previous = opened;
    for (std::int64_t i = 0; i < bars; ++i) {
      cumulative = i == 0 ? returns[0] : cumulative + returns[i];
      const double close = opened * libm::exp(cumulative);
      // Part of each bar's move is already present at its opening print, and
      // most of an overnight move is, which is what makes a gap look like one.
      const double share = i % kSessionBars == 0 ? 0.78 : 0.26;
      const double open = previous * libm::exp(share * returns[i]);
      const double span = std::fabs(returns[i]) + (idio * price_shape[i]) * 0.9;
      const double upper = (std::fabs(d.upper[i]) * span) * 0.55;
      const double lower = (std::fabs(d.lower[i]) * span) * 0.55;
      const double high = std::max(open, close) * (1.0 + upper);
      const double low = std::min(open, close) * (1.0 - lower);
      const double turnover =
          (((company.volume * volume_shape[i]) * (1.0 + activity[i])) * libm::exp(d.turnover[i])) *
          (1.0 + 6.0 * std::fabs(returns[i]));
      cents[i] = printed(open);
      cents[bars + i] = printed(high);
      cents[2 * bars + i] = printed(low);
      cents[3 * bars + i] = printed(close);
      volume[i] = traded(turnover);
      previous = close;
    }
    // The next block opens where this one closed, to the cent that was printed.
    out.carry[j] = static_cast<double>(cents[3 * bars + bars - 1]) / 100.0;
  });
}

void session_calendar(std::int64_t first_session, std::int64_t sessions, std::int64_t* time,
                      std::int32_t* day) {
  require(time && day, "calendar buffers are missing");
  require(first_session >= 0 && sessions >= 0 && first_session + sessions <= 4000000,
          "session range out of bounds");
  for (std::int64_t s = 0; s < sessions; ++s) {
    const std::int64_t opening = calendar::session_open(first_session + s);
    const auto date = static_cast<std::int32_t>(calendar::session_day(first_session + s));
    for (std::int64_t m = 0; m < kSessionBars; ++m) {
      time[s * kSessionBars + m] = opening + 60 * m;
      day[s * kSessionBars + m] = date;
    }
  }
}

void legacy_paths(const std::uint64_t* seeds, const double* initial, std::int32_t count,
                  int workers, std::int32_t* cents, std::int32_t* volume) {
  require(seeds && initial && cents && volume, "legacy buffers are missing");
  require(count > 0 && count <= 64, "legacy symbol count out of range");
  for (std::int32_t j = 0; j < count; ++j) {
    require(std::isfinite(initial[j]) && initial[j] > 0 && initial[j] < 1e6,
            "legacy starting price out of range");
  }
  // Each symbol has its own stream, so the symbols are independent tasks.
  parallel_for(count, workers, [&](std::int64_t j) {
    PythonRandom rng(seeds[j]);
    double price = initial[j];
    std::int32_t* row = cents + j * 4 * kLegacyBars;
    for (std::int64_t i = 0; i < kLegacyBars; ++i) {
      const double deviation = i % kSessionBars ? 0.0008 : 0.006;
      const double opening = price * libm::exp(rng.gauss(0.0, deviation));
      const double closing = opening * libm::exp(rng.gauss(0.000015, 0.0018));
      const double high = std::max(opening, closing) * (1.0 + rng.random() * 0.0015);
      const double low = std::min(opening, closing) * (1.0 - rng.random() * 0.0015);
      const double values[4] = {opening, high, low, closing};
      for (int k = 0; k < 4; ++k) {
        const std::int64_t hundredths = numeric::python_round_hundredths(values[k]);
        require(hundredths >= 0 && hundredths <= INT32_MAX, "legacy price out of range");
        row[k * kLegacyBars + i] = static_cast<std::int32_t>(hundredths);
      }
      volume[j * kLegacyBars + i] = static_cast<std::int32_t>(rng.randint(2000, 30000));
      price = closing;
    }
  });
}

std::int64_t aggregate(const Columns& series, std::int64_t start, std::int64_t stop,
                       std::int32_t per_bucket, bool aligned, const Buckets& out) {
  require(per_bucket > 0 && per_bucket <= kSessionBars, "bucket size out of range");
  require(start >= 0 && stop <= series.length, "bucket window outside the series");
  require(series.time && series.session && series.volume, "series columns are missing");
  if (stop <= start) return 0;
  std::int64_t count = -1;
  std::int64_t last_key = 0;
  std::int64_t last = start;
  for (std::int64_t i = start; i < stop; ++i) {
    const std::int64_t minute = i % kSessionBars;
    const std::int64_t key = series.session[i] * kSessionBars + minute / per_bucket;
    if (count < 0 || key != last_key) {
      if (count >= 0) out.cents[3][count] = series.cents[3][last];
      ++count;
      last_key = key;
      out.time[count] = aligned ? series.time[i] - (minute % per_bucket) * 60 : series.time[i];
      out.cents[0][count] = series.cents[0][i];
      out.cents[1][count] = series.cents[1][i];
      out.cents[2][count] = series.cents[2][i];
      out.volume[count] = series.volume[i];
    } else {
      out.cents[1][count] = std::max(out.cents[1][count], series.cents[1][i]);
      out.cents[2][count] = std::min(out.cents[2][count], series.cents[2][i]);
      out.volume[count] += series.volume[i];
    }
    last = i;
  }
  out.cents[3][count] = series.cents[3][last];
  return count + 1;
}

}  // namespace quanta::market
