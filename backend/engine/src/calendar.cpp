#include "calendar.hpp"

#include <cstdio>

#include "common.hpp"

namespace quanta::calendar {

// Howard Hinnant's civil-date algorithms, valid across the proleptic Gregorian range.
std::int64_t days_from_civil(std::int64_t year, unsigned month, unsigned day) {
  year -= month <= 2;
  const std::int64_t era = (year >= 0 ? year : year - 399) / 400;
  const auto yoe = static_cast<unsigned>(year - era * 400);
  const unsigned doy = (153 * (month > 2 ? month - 3 : month + 9) + 2) / 5 + day - 1;
  const unsigned doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
  return era * 146097 + static_cast<std::int64_t>(doe) - 719468;
}

void civil_from_days(std::int64_t days, std::int64_t& year, unsigned& month, unsigned& day) {
  days += 719468;
  const std::int64_t era = (days >= 0 ? days : days - 146096) / 146097;
  const auto doe = static_cast<unsigned>(days - era * 146097);
  const unsigned yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
  const unsigned doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
  const unsigned mp = (5 * doy + 2) / 153;
  day = doy - (153 * mp + 2) / 5 + 1;
  month = mp < 10 ? mp + 3 : mp - 9;
  year = static_cast<std::int64_t>(yoe) + era * 400 + (month <= 2);
}

int weekday(std::int64_t days) {
  // 1970-01-01 was a Thursday.
  const std::int64_t shifted = (days + 3) % 7;
  return static_cast<int>(shifted < 0 ? shifted + 7 : shifted);
}

std::int64_t session_day(std::int64_t session) {
  require(session >= 0, "a session index cannot be negative");
  static const std::int64_t first = days_from_civil(2025, 1, 6);  // a Monday
  return first + (session / 5) * 7 + session % 5;
}

namespace {

std::int64_t nth_sunday(std::int64_t year, unsigned month, int nth) {
  const std::int64_t first = days_from_civil(year, month, 1);
  const int to_sunday = (6 - weekday(first) + 7) % 7;
  return first + to_sunday + 7 * (nth - 1);
}

}  // namespace

std::int64_t utc_minus_local(std::int64_t days) {
  std::int64_t year;
  unsigned month, day;
  civil_from_days(days, year, month, day);
  require(year >= 2007, "the New York offset rule is only defined here from 2007");
  const bool daylight = days >= nth_sunday(year, 3, 2) && days < nth_sunday(year, 11, 1);
  return daylight ? 4 * 3600 : 5 * 3600;
}

std::int64_t session_open(std::int64_t session) {
  const std::int64_t day = session_day(session);
  return day * 86400 + kOpeningSeconds + utc_minus_local(day);
}

std::string iso_date(std::int64_t days) {
  std::int64_t year;
  unsigned month, day;
  civil_from_days(days, year, month, day);
  require(year >= 1 && year <= 9999, "date outside the range Python can represent");
  char buffer[16];
  std::snprintf(buffer, sizeof buffer, "%04lld-%02u-%02u", static_cast<long long>(year), month, day);
  return buffer;
}

bool parse_iso_date(std::string_view text, std::int64_t& days) {
  if (text.size() != 10 || text[4] != '-' || text[7] != '-') return false;
  auto digits = [&](std::size_t from, std::size_t count, unsigned& out) {
    out = 0;
    for (std::size_t i = from; i < from + count; ++i) {
      if (text[i] < '0' || text[i] > '9') return false;
      out = out * 10 + static_cast<unsigned>(text[i] - '0');
    }
    return true;
  };
  unsigned year, month, day;
  if (!digits(0, 4, year) || !digits(5, 2, month) || !digits(8, 2, day)) return false;
  if (year < 1 || month < 1 || month > 12 || day < 1) return false;
  static const unsigned lengths[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
  const bool leap = (year % 4 == 0 && year % 100 != 0) || year % 400 == 0;
  const unsigned limit = lengths[month - 1] + (month == 2 && leap ? 1 : 0);
  if (day > limit) return false;
  days = days_from_civil(year, month, day);
  return true;
}

}  // namespace quanta::calendar
