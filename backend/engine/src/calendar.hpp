// The generated market's clock: weekday sessions of 390 one-minute bars,
// 09:30-16:00 America/New_York, from Monday 6 January 2025. Exchange holidays
// are not observed.
//
// Only the New York offset for a weekday session is ever needed, and from 2007
// onwards it follows one rule: daylight time from the second Sunday of March to
// the first Sunday of November. zoneinfo applies the same rule to dates past the
// end of its transition table, so the timestamps agree for as long as a run can
// be replayed.
#pragma once

#include <cstdint>
#include <string>
#include <string_view>

namespace quanta::calendar {

constexpr std::int64_t kSessionBars = 390;
constexpr std::int64_t kOpeningSeconds = 9 * 3600 + 30 * 60;

// Days since 1970-01-01 of a proleptic Gregorian date, and back.
std::int64_t days_from_civil(std::int64_t year, unsigned month, unsigned day);
void civil_from_days(std::int64_t days, std::int64_t& year, unsigned& month, unsigned& day);

// Monday == 0, as Python's date.weekday().
int weekday(std::int64_t days);

// The calendar day of a weekday session counted from 6 January 2025.
std::int64_t session_day(std::int64_t session);

// Seconds to add to New York wall time to reach UTC, for a time of day between
// 02:00 and midnight on the given day.
std::int64_t utc_minus_local(std::int64_t days);

// UTC epoch seconds of a session's 09:30 opening print.
std::int64_t session_open(std::int64_t session);

// "YYYY-MM-DD", as date.isoformat() writes it.
std::string iso_date(std::int64_t days);
bool parse_iso_date(std::string_view text, std::int64_t& days);

}  // namespace quanta::calendar
