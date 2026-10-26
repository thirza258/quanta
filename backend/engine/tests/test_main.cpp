// Standalone tests for the simulator engine: hand-calculated golden fixtures,
// refusal of invalid input, and serial/parallel equality. They need no Python;
// the differential tests against the original Python live in
// backend/tests/test_engine_parity.py.
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <functional>
#include <string>
#include <vector>

#include "../src/analytics.hpp"
#include "../src/calendar.hpp"
#include "../src/common.hpp"
#include "../src/decimal.hpp"
#include "../src/engine.hpp"
#include "../src/json.hpp"
#include "../src/market.hpp"
#include "../src/numeric.hpp"
#include "../src/parallel.hpp"
#include "../src/rng.hpp"

namespace {

int failures = 0;
int checks = 0;

void check(bool ok, const char* what, int line) {
  ++checks;
  if (!ok) {
    ++failures;
    std::printf("FAIL line %d: %s\n", line, what);
  }
}

#define CHECK(cond) check((cond), #cond, __LINE__)
#define CHECK_EQ(a, b)                                                                   \
  do {                                                                                   \
    const auto lhs_ = (a);                                                               \
    const auto rhs_ = (b);                                                               \
    ++checks;                                                                            \
    if (!(lhs_ == rhs_)) {                                                               \
      ++failures;                                                                        \
      std::printf("FAIL line %d: %s == %s\n", __LINE__, #a, #b);                         \
    }                                                                                    \
  } while (0)

// Expect the body to throw quanta::Error (a refusal, never a wrapped value).
#define CHECK_THROWS(body)                     \
  do {                                         \
    bool thrown_ = false;                      \
    try {                                      \
      body;                                    \
    } catch (const quanta::Error&) {           \
      thrown_ = true;                          \
    }                                          \
    check(thrown_, "throws: " #body, __LINE__); \
  } while (0)

using quanta::Dec;
using quanta::Rounding;

std::string q(const char* value, Rounding mode) {
  return quanta::quantize(Dec::parse(value), -2, mode).str();
}

void decimal_fixtures() {
  // Division rounds to 28 significant digits, half to even.
  CHECK_EQ((Dec::of(1) / Dec::of(3)).str(), std::string("0.3333333333333333333333333333"));
  CHECK_EQ((Dec::of(1) / Dec::of(7)).str(), std::string("0.1428571428571428571428571429"));
  CHECK_EQ((Dec::of(2) / Dec::of(3)).str(), std::string("0.6666666666666666666666666667"));
  // One session's borrow on 1,000 shares at $50, 5% a year over 252 sessions.
  const Dec fee = Dec::of(50) * Dec::of(1000) * Dec::parse("0.05") / Dec::of(252);
  CHECK_EQ(fee.str(), std::string("9.920634920634920634920634921"));
  CHECK_EQ(quanta::money(fee), std::string("9.92"));
  // Rounding modes the ledger uses, including the sign a zero keeps.
  CHECK_EQ(q("2.675", Rounding::HalfUp), std::string("2.68"));
  CHECK_EQ(q("2.665", Rounding::HalfEven), std::string("2.66"));
  CHECK_EQ(q("-0.001", Rounding::HalfUp), std::string("-0.00"));
  CHECK_EQ(q("0.001", Rounding::Ceiling), std::string("0.01"));
  CHECK_EQ(q("-0.001", Rounding::Ceiling), std::string("-0.00"));
  CHECK_EQ(q("0.019", Rounding::Down), std::string("0.01"));
  CHECK_EQ(quanta::neg(Dec::parse("0")).str(), std::string("0"));
  CHECK_EQ((Dec::parse("-0") + Dec::parse("-0")).str(), std::string("-0"));
  CHECK_EQ((Dec::parse("1.00") - Dec::parse("1.00")).str(), std::string("0.00"));
  CHECK_EQ((Dec::parse("0.1") + Dec::parse("0.2")).str(), std::string("0.3"));
  CHECK_EQ((Dec::parse("1.5") * Dec::of(2)).str(), std::string("3.0"));
  CHECK_EQ(Dec::parse("1E+3").str(), std::string("1E+3"));
  CHECK_EQ(Dec::of_double(0.1 + 0.2).str(), std::string("0.30000000000000004"));
  CHECK_EQ(quanta::to_int64(Dec::parse("-7.9")), std::int64_t{-7});
  CHECK(Dec::parse("1.50") == Dec::parse("1.5"));
  CHECK(Dec::parse("-0.00") == Dec::parse("0"));
}

void rng_fixtures() {
  // numpy.random.PCG64([47, 0, 0x9E3779B9]).random_raw(3)
  quanta::Pcg64 raw({47, 0, 0x9E3779B9ULL});
  CHECK_EQ(raw.next64(), std::uint64_t{0xec4882b2cdfad3a3ULL});
  CHECK_EQ(raw.next64(), std::uint64_t{0x73510898ad287bd4ULL});
  CHECK_EQ(raw.next64(), std::uint64_t{0x25c0ac0d9b30dd8fULL});
  // numpy.random.default_rng([47, 0, 0x9E3779B9]).standard_normal(3)
  quanta::Pcg64 normal({47, 0, 0x9E3779B9ULL});
  CHECK_EQ(normal.standard_normal(), -0.6848037899987545);
  CHECK_EQ(normal.standard_normal(), -1.3493285827069257);
  CHECK_EQ(normal.standard_normal(), -0.29457148442263553);
  // random.Random(42): the values every Python user has seen.
  quanta::PythonRandom uniform(42);
  CHECK_EQ(uniform.random(), 0.6394267984578837);
  CHECK_EQ(uniform.random(), 0.025010755222666936);
  quanta::PythonRandom gauss(42);
  CHECK_EQ(gauss.gauss(0.0, 1.0), -0.14409032957792836);
  CHECK_EQ(gauss.gauss(0.0, 1.0), -0.1729036003315193);
  CHECK_EQ(gauss.randint(2000, 30000), std::int64_t{11012});
  CHECK_EQ(quanta::numeric::python_round_hundredths(2.675), std::int64_t{267});  // binary 2.67499..
  CHECK_EQ(quanta::numeric::python_round_hundredths(0.125), std::int64_t{12});   // exact tie, to even
  CHECK_EQ(quanta::numeric::python_round_hundredths(0.375), std::int64_t{38});
}

void calendar_fixtures() {
  using namespace quanta::calendar;
  // First session: Monday 6 January 2025, 09:30 EST.
  CHECK_EQ(session_open(0), std::int64_t{1736173800});
  CHECK_EQ(session_day(0), std::int64_t{20094});
  // Friday before daylight time starts, and the Monday after it has.
  CHECK_EQ(session_open(44), std::int64_t{1741357800});
  CHECK_EQ(session_open(45), std::int64_t{1741613400});
  CHECK_EQ(session_day(45), std::int64_t{20157});
  // And back to standard time in November.
  CHECK_EQ(session_open(214), std::int64_t{1761917400});
  CHECK_EQ(session_open(215), std::int64_t{1762180200});
  CHECK_EQ(iso_date(20157), std::string("2025-03-10"));
  std::int64_t day = 0;
  CHECK(parse_iso_date("2024-02-29", day) && day == days_from_civil(2024, 2, 29));
  CHECK(!parse_iso_date("2025-02-29", day));
  CHECK(!parse_iso_date("2025-13-01", day));
  CHECK(!parse_iso_date("2025-1-01", day));
  CHECK(!parse_iso_date("", day));
}

// ---------------------------------------------------------------------------
// Engine fixtures: small markets whose every figure is worked out by hand.

struct Fixture {
  std::vector<std::int32_t> cents[4];
  std::vector<std::int32_t> volume;
  std::vector<std::int64_t> time;
  std::vector<std::int32_t> day;

  // rows: open, high, low, close in dollars; volume; day offset from 20094.
  Fixture(std::initializer_list<std::vector<double>> rows) {
    std::int64_t stamp = 1736173800;
    for (const auto& r : rows) {
      for (int k = 0; k < 4; ++k) cents[k].push_back(static_cast<std::int32_t>(std::lround(r[k] * 100)));
      volume.push_back(static_cast<std::int32_t>(r[4]));
      day.push_back(20094 + static_cast<std::int32_t>(r[5]));
      time.push_back(stamp);
      stamp += 60;
    }
  }

  quanta::engine::Bars bars() const {
    quanta::engine::Bars b{};
    b.length = static_cast<std::int64_t>(time.size());
    for (int k = 0; k < 4; ++k) b.cents[k] = cents[k].data();
    b.volume_int = volume.data();
    b.time = time.data();
    b.day = day.data();
    return b;
  }
};

std::string order_json(const std::string& id, const std::string& side, const std::string& kind,
                       int quantity, const std::string& extra = "") {
  return "{\"id\":\"" + id + "\",\"symbol\":\"AAA\",\"side\":\"" + side + "\",\"kind\":\"" + kind +
         "\",\"tif\":\"GTC\",\"status\":\"working\",\"quantity\":" + std::to_string(quantity) +
         ",\"filled\":0,\"average\":\"0.00\",\"notional\":\"0.00\",\"fee_remaining\":\"1.00\","
         "\"triggered\":false,\"forced\":false,\"day\":\"2025-01-06\"" +
         extra + "}";
}

std::string request(const std::string& op, int cursor, const std::string& cash,
                    const std::string& positions, const std::string& orders,
                    const std::string& extra = "", const std::string& account = "cash",
                    const std::string& commission = "1") {
  return "{\"op\":\"" + op + "\",\"symbols\":[\"AAA\"],\"cursor\":" + std::to_string(cursor) +
         ",\"config\":{\"commission\":\"" + commission +
         "\",\"slippage_bps\":\"0\",\"spread_bps\":\"0\",\"participation\":\"1\",\"account\":\"" +
         account + "\"},\"margin\":{\"maintenance\":\"0.3\",\"borrow_rate\":\"0.05\",\"sessions_a_year\":252}" +
         ",\"cash\":\"" + cash + "\",\"realized\":\"0.00\",\"positions\":" + positions +
         ",\"orders\":[" + orders + "]" + extra + "}";
}

quanta::json::Value run(const Fixture& fixture, const std::string& text) {
  const quanta::engine::Bars bars = fixture.bars();
  return quanta::json::parse(quanta::engine::handle(text, &bars, 1));
}

std::string text(const quanta::json::Value& value, const char* key) {
  const auto* found = value.find(key);
  return found && found->type == quanta::json::Value::Type::String ? found->text : "<none>";
}

const quanta::json::Value* field(const quanta::json::Value& changes, std::int64_t order, const char* key) {
  for (const auto& entry : changes.items) {
    if (entry.items[0].integer != order) continue;
    for (const auto& pair : entry.items[1].items) {
      if (pair.items[0].text == key) return &pair.items[1];
    }
  }
  return nullptr;
}

const char* kAdvance = ",\"steps\":1,\"watch\":[],\"scheduled\":[]";

void round_trip_fixture() {
  // PRD SIM-AC-03: $100,000; buy 10 at $100 with a $1 fee, sell all 10 at $110
  // with a $1 fee. Cash $98,999 after entry and $100,098 after exit; $98 realized.
  const Fixture f{{100, 101, 99, 100, 1000, 0}, {100, 101, 99, 100, 1000, 0}, {110, 111, 109, 110, 1000, 0}};
  const auto validated = run(f, request("validate", 0, "100000.00", "[]", "",
                                        ",\"order\":" + order_json("b", "buy", "market", 10)));
  CHECK_EQ(text(validated, "reserve_price"), std::string("100.00"));
  CHECK(validated.find("error") == nullptr);

  const auto entry = run(f, request("advance", 0, "100000.00", "[]",
                                    order_json("b", "buy", "market", 10, ",\"reserve_price\":\"100.00\""), kAdvance));
  CHECK_EQ(text(entry, "cash"), std::string("98999.00"));
  const auto& position = entry.at("positions").items.at(0).items;
  CHECK_EQ(position.at(1).integer, std::int64_t{10});
  CHECK_EQ(position.at(2).text, std::string("1001.00"));
  const auto& fill = entry.at("fills").items.at(0);
  CHECK_EQ(text(fill, "price"), std::string("100.00"));
  CHECK_EQ(text(fill, "fee"), std::string("1.00"));
  CHECK_EQ(field(entry.at("orders"), 0, "status")->text, std::string("filled"));
  CHECK_EQ(field(entry.at("orders"), 0, "average")->text, std::string("100.00"));

  const auto exit = run(f, request("advance", 1, "98999.00", "[[\"AAA\",10,\"1001.00\"]]",
                                   order_json("s", "sell", "market", 10, ",\"reserve_price\":\"100.00\""), kAdvance));
  CHECK_EQ(text(exit, "cash"), std::string("100098.00"));
  CHECK_EQ(text(exit, "realized"), std::string("98.00"));
  CHECK_EQ(exit.at("positions").items.at(0).items.at(1).integer, std::int64_t{0});
  CHECK_EQ(exit.at("positions").items.at(0).items.at(2).text, std::string("0.00"));
  CHECK_EQ(text(exit.at("fills").items.at(0), "realized"), std::string("98.00"));
}

void short_fixtures() {
  // Short 100 at $50 with no commission: $105,000 cash, owing 100 shares
  // bought for -$5,000. Covering at $45 realizes $500.
  const Fixture f{{50, 50, 50, 50, 10000, 0}, {50, 50, 50, 50, 10000, 0}, {45, 45, 45, 45, 10000, 0}};
  const std::string zero_fee = ",\"reserve_price\":\"50.00\",\"fee_remaining\":\"0.00\"";
  std::string sell = order_json("s", "sell", "market", 100);
  sell.replace(sell.find(",\"fee_remaining\":\"1.00\""), 23, zero_fee);
  const auto opened = run(f, request("advance", 0, "100000.00", "[]", sell, kAdvance, "margin", "0"));
  CHECK_EQ(text(opened, "cash"), std::string("105000.00"));
  CHECK_EQ(opened.at("positions").items.at(0).items.at(1).integer, std::int64_t{-100});
  CHECK_EQ(opened.at("positions").items.at(0).items.at(2).text, std::string("-5000.00"));

  std::string buy = order_json("c", "buy", "market", 100);
  buy.replace(buy.find(",\"fee_remaining\":\"1.00\""), 23, zero_fee);
  const auto covered = run(f, request("advance", 1, "105000.00", "[[\"AAA\",-100,\"-5000.00\"]]", buy, kAdvance,
                                      "margin", "0"));
  CHECK_EQ(text(covered, "realized"), std::string("500.00"));
  CHECK_EQ(text(covered, "cash"), std::string("100500.00"));

  // Long 10 at $50 (cost $500), sell 30 at $60: $100 realized on the ten,
  // twenty shorted at $60 for a basis of -$1,200.
  const Fixture g{{50, 50, 50, 50, 10000, 0}, {60, 60, 60, 60, 10000, 0}};
  std::string cross = order_json("x", "sell", "market", 30);
  cross.replace(cross.find(",\"fee_remaining\":\"1.00\""), 23, ",\"reserve_price\":\"50.00\",\"fee_remaining\":\"0.00\"");
  const auto crossed = run(g, request("advance", 0, "99500.00", "[[\"AAA\",10,\"500.00\"]]", cross, kAdvance,
                                      "margin", "0"));
  CHECK_EQ(text(crossed, "realized"), std::string("100.00"));
  CHECK_EQ(crossed.at("positions").items.at(0).items.at(1).integer, std::int64_t{-20});
  CHECK_EQ(crossed.at("positions").items.at(0).items.at(2).text, std::string("-1200.00"));

  // The session ends between bars 1 and 2, so 1,000 borrowed shares at $50
  // accrue one session's fee: 50 x 1000 x 5% / 252 = $9.92.
  const Fixture h{{50, 50, 50, 50, 10000, 0}, {50, 50, 50, 50, 10000, 0}, {50, 50, 50, 50, 10000, 1}};
  const auto borrowed = run(h, request("advance", 0, "150000.00", "[[\"AAA\",-1000,\"-50000.00\"]]", "", kAdvance,
                                       "margin", "0"));
  CHECK_EQ(text(borrowed, "cash"), std::string("149990.08"));
  const auto& charge = borrowed.at("ledger").items.at(0);
  CHECK_EQ(text(charge, "id"), std::string("borrow:1"));
  CHECK_EQ(text(charge, "amount"), std::string("-9.92"));
}

void trailing_and_volume_fixtures() {
  // A 5% trail anchored at $100 stops at $95. A bar reaching $110 without
  // touching the stop ratchets the anchor to $110 and the stop to $104.50;
  // the next bar opens at $103, under the stop, and fills there.
  const Fixture f{{100, 100, 100, 100, 1000, 0}, {105, 110, 101, 108, 1000, 0}, {103, 104, 99, 100, 1000, 0}};
  const std::string trailing = order_json(
      "t", "sell", "trailing_stop", 10,
      ",\"trail_percent\":\"5\",\"trail_anchor\":\"100.00\",\"stop_price\":\"95.00\",\"reserve_price\":\"100.00\"");
  const auto ratchet = run(f, request("advance", 0, "1000.00", "[[\"AAA\",10,\"1000.00\"]]", trailing, kAdvance));
  CHECK_EQ(field(ratchet.at("orders"), 0, "trail_anchor")->text, std::string("110.00"));
  CHECK_EQ(field(ratchet.at("orders"), 0, "stop_price")->text, std::string("104.50"));
  CHECK_EQ(ratchet.at("fills").items.size(), std::size_t{0});
  const std::string armed = order_json(
      "t", "sell", "trailing_stop", 10,
      ",\"trail_percent\":\"5\",\"trail_anchor\":\"110.00\",\"stop_price\":\"104.50\",\"reserve_price\":\"100.00\"");
  const auto stopped = run(f, request("advance", 1, "1000.00", "[[\"AAA\",10,\"1000.00\"]]", armed, kAdvance));
  CHECK_EQ(text(stopped.at("fills").items.at(0), "price"), std::string("103.00"));

  // Ten shares of volume at full participation, two orders queued for 8 and 5:
  // the first takes 8, the second 2 now and 3 on the next bar, paying its
  // commission once.
  const Fixture v{{10, 10, 10, 10, 10, 0}, {10, 10, 10, 10, 10, 0}, {10, 10, 10, 10, 10, 0}};
  const std::string queued = order_json("a", "buy", "market", 8, ",\"reserve_price\":\"10.00\"") + "," +
                             order_json("b", "buy", "market", 5, ",\"reserve_price\":\"10.00\"");
  const auto shared = run(v, request("advance", 0, "1000.00", "[]", queued, kAdvance));
  CHECK_EQ(shared.at("fills").items.at(0).at("quantity").integer, std::int64_t{8});
  CHECK_EQ(shared.at("fills").items.at(1).at("quantity").integer, std::int64_t{2});
  CHECK_EQ(field(shared.at("orders"), 1, "status")->text, std::string("partially_filled"));
  CHECK_EQ(text(shared.at("fills").items.at(1), "fee"), std::string("1.00"));
  const std::string rest = order_json("b", "buy", "market", 5,
                                      ",\"reserve_price\":\"10.00\",\"notional\":\"20.00\",\"average\":\"10.00\"");
  std::string partly = rest;
  partly.replace(partly.find("\"filled\":0"), 10, "\"filled\":2");
  partly.replace(partly.find(",\"fee_remaining\":\"1.00\""), 23, ",\"fee_remaining\":\"0.00\"");
  partly.replace(partly.find("\"status\":\"working\""), 18, "\"status\":\"partially_filled\"");
  const auto finished = run(v, request("advance", 1, "898.00", "[[\"AAA\",10,\"102.00\"]]", partly, kAdvance));
  CHECK_EQ(finished.at("fills").items.at(0).at("quantity").integer, std::int64_t{3});
  CHECK_EQ(text(finished.at("fills").items.at(0), "fee"), std::string("0.00"));
  CHECK_EQ(field(finished.at("orders"), 0, "status")->text, std::string("filled"));
}

void refusals() {
  const Fixture f{{100, 101, 99, 100, 1000, 0}, {100, 101, 99, 100, 1000, 0}};
  // Overspending is refused with the learner-facing message, not an engine error.
  const auto broke = run(f, request("validate", 0, "50.00", "[]", "", ",\"order\":" + order_json("b", "buy", "market", 10)));
  CHECK_EQ(text(broke, "error"), std::string("Insufficient available cash, including fees and other working orders."));
  const auto naked = run(f, request("validate", 0, "50000.00", "[]", "", ",\"order\":" + order_json("s", "sell", "market", 10)));
  CHECK_EQ(text(naked, "error"), std::string("Insufficient available shares. This paper account is long-only."));
  // Malformed requests are engine errors.
  const auto bars = f.bars();
  CHECK_THROWS(quanta::engine::handle("{", &bars, 1));
  CHECK_THROWS(quanta::engine::handle("{\"op\":\"advance\"}", &bars, 1));
  CHECK_THROWS(quanta::engine::handle("{\"op\":\"teleport\",\"symbols\":[\"AAA\"],\"cursor\":0}", &bars, 1));
  CHECK_THROWS(run(f, request("advance", 0, "1.5", "[]", order_json("b", "buy", "market", -1), kAdvance)));
  CHECK_THROWS(run(f, request("advance", 0, "100.00", "[[\"AAA\",1]]", "", kAdvance)));
  // A cursor past the data is only an error once a bar has to be read, as in
  // Python: here a DAY order needs the cursor's calendar day.
  std::string day_order = order_json("d", "buy", "market", 1, ",\"reserve_price\":\"1.00\"");
  day_order.replace(day_order.find("\"GTC\""), 5, "\"DAY\"");
  CHECK_THROWS(run(f, request("advance", 7, "100.00", "[]", day_order, kAdvance)));
  CHECK_THROWS(quanta::json::parse("{\"a\":1.5}"));
  CHECK_THROWS(quanta::json::parse("[1,]"));
  CHECK_THROWS(quanta::json::parse("\"\\uD800\""));
  CHECK_THROWS(quanta::json::parse(std::string(100, '[') + std::string(100, ']')));
  CHECK_THROWS(Dec::parse("1.2.3"));
  CHECK_THROWS(Dec::parse(""));
  CHECK_THROWS(Dec::parse("1e"));
  CHECK_THROWS(Dec::parse("123456789012345678901234567890123456789"));
  CHECK_THROWS(Dec::of(1) / Dec::of(0));
  CHECK_THROWS(quanta::quantize(Dec::parse("1E+40"), -2, Rounding::HalfUp));
  CHECK_THROWS(quanta::to_int64(Dec::parse("1E+30")));
  CHECK_THROWS(quanta::PythonRandom(1).randbelow(0));
  CHECK_THROWS(quanta::checked_mul(INT64_MAX, 2));
}

// ---------------------------------------------------------------------------
// Market generation

struct Universe {
  std::vector<quanta::market::Company> companies;
  std::vector<quanta::market::Shock> shocks;
  std::vector<double> carry;
  std::int32_t sectors = 7;
};

Universe universe(int count) {
  Universe u;
  for (int j = 0; j < count; ++j) {
    u.companies.push_back({0.6 + 0.03 * j, 0.2 + 0.01 * j, 5000.0 + 700.0 * j, j % u.sectors});
    u.carry.push_back(20.0 + 3.5 * j);
  }
  quanta::Pcg64 rng({99});
  for (int k = 0; k < 600; ++k) {
    const auto scope = static_cast<std::int32_t>(rng.next64() % 3);
    const auto target = scope == 0 ? 0 : static_cast<std::int32_t>(rng.next64() % (scope == 1 ? u.sectors : count));
    u.shocks.push_back({scope, target, static_cast<std::int32_t>(rng.next64() % quanta::market::kBlockBars),
                        static_cast<std::int32_t>(20 + rng.next64() % 1200), rng.next64() % 2 ? 1 : -1,
                        static_cast<std::int32_t>(40 + rng.next64() % 400)});
  }
  return u;
}

struct Block {
  std::vector<std::int32_t> cents, volume;
  std::vector<double> carry;
};

Block generate(const Universe& u, std::uint64_t seed, std::int64_t first, int workers) {
  const auto count = static_cast<std::int32_t>(u.companies.size());
  Block out;
  out.cents.resize(static_cast<std::size_t>(count) * 4 * quanta::market::kBlockBars);
  out.volume.resize(static_cast<std::size_t>(count) * quanta::market::kBlockBars);
  out.carry.resize(static_cast<std::size_t>(count));
  quanta::market::generate_block({seed, first, u.companies.data(), count, u.sectors, u.carry.data(), u.shocks.data(),
                                  static_cast<std::int64_t>(u.shocks.size()), workers},
                                 {out.cents.data(), out.volume.data(), out.carry.data()});
  return out;
}

void generation_properties() {
  const Universe u = universe(40);
  const Block serial = generate(u, 2024, 63, 1);
  // Every bar is a well-formed candle: positive, high above both prints, low below.
  const std::int64_t bars = quanta::market::kBlockBars;
  bool candles = true;
  for (std::size_t j = 0; j < u.companies.size(); ++j) {
    const std::int32_t* c = serial.cents.data() + j * 4 * bars;
    for (std::int64_t i = 0; i < bars; ++i) {
      const std::int32_t o = c[i], h = c[bars + i], l = c[2 * bars + i], cl = c[3 * bars + i];
      candles = candles && l >= 1 && h >= o && h >= cl && l <= o && l <= cl;
    }
    candles = candles && serial.carry[j] == c[4 * bars - 1] / 100.0;
  }
  CHECK(candles);
  bool volumes = true;
  for (const std::int32_t v : serial.volume) volumes = volumes && v >= 100;
  CHECK(volumes);
  // The same block regenerated is identical, and independent of the worker
  // count: tasks write disjoint outputs and draw nothing themselves.
  for (int workers = 1; workers <= 32; ++workers) {
    const Block parallel = generate(u, 2024, 63, workers);
    CHECK(parallel.cents == serial.cents && parallel.volume == serial.volume && parallel.carry == serial.carry);
  }
  // A different block of the same seed is a different market.
  CHECK(generate(u, 2024, 84, 4).cents != serial.cents);

  std::vector<std::uint64_t> seeds = {47, 100050, 200053, 300056, 400059, 500062};
  std::vector<double> initial = {224, 418, 128, 245, 195, 530};
  std::vector<std::int32_t> reference_cents(6 * 4 * 6000), reference_volume(6 * 6000);
  quanta::market::legacy_paths(seeds.data(), initial.data(), 6, 1, reference_cents.data(), reference_volume.data());
  for (int workers = 2; workers <= 8; ++workers) {
    std::vector<std::int32_t> cents(6 * 4 * 6000), volume(6 * 6000);
    quanta::market::legacy_paths(seeds.data(), initial.data(), 6, workers, cents.data(), volume.data());
    CHECK(cents == reference_cents && volume == reference_volume);
  }

  // Invalid generator input is refused before anything is written.
  Universe bad = u;
  bad.carry[3] = 0.0;
  CHECK_THROWS(generate(bad, 1, 0, 2));
  bad = u;
  bad.shocks[5].scope = 3;
  CHECK_THROWS(generate(bad, 1, 0, 2));
  bad = u;
  bad.companies[2].sector = 99;
  CHECK_THROWS(generate(bad, 1, 0, 2));
}

void aggregation_fixture() {
  // Two sessions of four minutes each, read in two-minute buckets from the
  // middle of the first bucket.
  std::vector<std::int32_t> o = {100, 101, 102, 103, 200, 201, 202, 203};
  std::vector<std::int32_t> h = {110, 111, 112, 113, 210, 211, 212, 213};
  std::vector<std::int32_t> l = {90, 91, 92, 93, 190, 191, 192, 193};
  std::vector<std::int32_t> c = {105, 106, 107, 108, 205, 206, 207, 208};
  std::vector<std::int32_t> v = {1, 2, 3, 4, 5, 6, 7, 8};
  std::vector<std::int64_t> t = {0, 60, 120, 180, 1000, 1060, 1120, 1180};
  // Sessions of 390 bars in the engine's indexing: place them at 0..3 and 390..393.
  const std::int64_t n = 394;
  std::vector<std::int32_t> O(n), H(n), L(n), C(n), V(n);
  std::vector<std::int64_t> T(n), S(n);
  for (std::int64_t i = 0; i < n; ++i) S[i] = i / 390;
  for (int k = 0; k < 4; ++k) {
    O[k] = o[k], H[k] = h[k], L[k] = l[k], C[k] = c[k], V[k] = v[k], T[k] = t[k];
    O[390 + k] = o[4 + k], H[390 + k] = h[4 + k], L[390 + k] = l[4 + k], C[390 + k] = c[4 + k];
    V[390 + k] = v[4 + k], T[390 + k] = t[4 + k];
  }
  const quanta::market::Columns series{{O.data(), H.data(), L.data(), C.data()}, V.data(), T.data(), S.data(), n};
  std::vector<std::int64_t> bt(n), bv(n);
  std::vector<std::int32_t> b0(n), b1(n), b2(n), b3(n);
  const quanta::market::Buckets out{bt.data(), {b0.data(), b1.data(), b2.data(), b3.data()}, bv.data()};
  // [1, 4) inside session 0, then [390, 393) inside session 1.
  CHECK_EQ(quanta::market::aggregate(series, 1, 4, 2, false, out), std::int64_t{2});
  CHECK(bt[0] == 60 && b0[0] == 101 && b1[0] == 111 && b2[0] == 91 && b3[0] == 106 && bv[0] == 2);
  CHECK(bt[1] == 120 && b0[1] == 102 && b1[1] == 113 && b2[1] == 92 && b3[1] == 108 && bv[1] == 7);
  CHECK_EQ(quanta::market::aggregate(series, 1, 4, 2, true, out), std::int64_t{2});
  CHECK_EQ(bt[0], std::int64_t{0});  // aligned: the bucket's own boundary
  CHECK_EQ(quanta::market::aggregate(series, 390, 393, 390, false, out), std::int64_t{1});
  CHECK(b0[0] == 200 && b1[0] == 212 && b2[0] == 190 && b3[0] == 207 && bv[0] == 18);
  CHECK_THROWS(quanta::market::aggregate(series, 0, 4, 0, false, out));
}

void analytics_fixtures() {
  const std::vector<double> x = {1, 2, 3, 4, 5, 6, 7, 8};
  std::vector<double> out(x.size());
  quanta::analytics::sma(x.data(), 8, 3, out.data());
  CHECK(std::isnan(out[1]) && out[2] == 2.0 && out[7] == 7.0);
  quanta::analytics::ema(x.data(), 8, 3, out.data());
  CHECK(out[2] == 2.0 && out[3] == 3.0);  // seeded with the simple average, then smoothed
  quanta::analytics::rsi(x.data(), 8, 3, out.data());
  CHECK(std::isnan(out[2]) && out[3] == 100.0);  // gains only

  // Equity on every bar: opening cash until a fill, then cash plus holdings.
  const std::int64_t bars = 4;
  const std::int64_t times[] = {100, 200, 300, 400};
  const std::int64_t cash_times[] = {200};
  const double cash_values[] = {500.0};
  const std::int32_t fill_symbol[] = {0};
  const std::int64_t fill_quantity[] = {5};
  const std::int64_t fill_time[] = {200};
  const double closes0[] = {100, 100, 110, 120};
  const double closes1[] = {50, 25, 50, 100};
  const double* closes[] = {closes0, closes1};
  double equity[4], gross[4], level[4];
  quanta::analytics::mark_to_market({bars, times, 1000.0, 1, cash_times, cash_values, 1, fill_symbol, fill_quantity,
                                     fill_time, 2, closes, 1},
                                    {equity, gross, level});
  CHECK(equity[0] == 1000.0 && equity[1] == 1000.0 && equity[2] == 1050.0 && equity[3] == 1100.0);
  CHECK(gross[0] == 0.0 && gross[3] == 600.0);
  CHECK(level[0] == 1.0 && level[1] == 0.75 && level[3] == 1.6);
  // Any number of workers gives the same bars.
  std::vector<std::int64_t> long_times(50000), fills_t(300), fills_q(300);
  std::vector<std::int32_t> fills_s(300);
  std::vector<double> c0(50000), c1(50000), c2(50000);
  quanta::Pcg64 rng({5});
  for (std::size_t i = 0; i < long_times.size(); ++i) {
    long_times[i] = 1000 + 60 * static_cast<std::int64_t>(i);
    c0[i] = 50 + rng.standard_normal();
    c1[i] = 80 + rng.standard_normal();
    c2[i] = 20 + rng.standard_normal();
  }
  for (std::size_t k = 0; k < fills_t.size(); ++k) {
    fills_t[k] = 1000 + 60 * static_cast<std::int64_t>(k * 150);
    fills_q[k] = static_cast<std::int64_t>(rng.next64() % 200) - 100;
    fills_s[k] = static_cast<std::int32_t>(rng.next64() % 3);
  }
  const double* many[] = {c0.data(), c1.data(), c2.data()};
  std::vector<double> e1(50000), g1(50000), l1(50000);
  quanta::analytics::mark_to_market({50000, long_times.data(), 1e5, 0, nullptr, nullptr, 300, fills_s.data(),
                                     fills_q.data(), fills_t.data(), 3, many, 1},
                                    {e1.data(), g1.data(), l1.data()});
  for (int workers : {2, 3, 8, 16}) {
    std::vector<double> e(50000), g(50000), l(50000);
    quanta::analytics::mark_to_market({50000, long_times.data(), 1e5, 0, nullptr, nullptr, 300, fills_s.data(),
                                       fills_q.data(), fills_t.data(), 3, many, workers},
                                      {e.data(), g.data(), l.data()});
    CHECK(e == e1 && g == g1 && l == l1);
  }
}

void parallel_contract() {
  // An exception in one task is reported after every worker has joined, and
  // no task starts once one has failed.
  std::vector<int> seen(1000, 0);
  bool thrown = false;
  try {
    quanta::parallel_for(1000, 8, [&](std::int64_t task) {
      if (task == 500) quanta::fail("task 500 failed");
      seen[task] = 1;
    });
  } catch (const quanta::Error&) {
    thrown = true;
  }
  CHECK(thrown);
  std::vector<std::int64_t> squares(10000);
  quanta::parallel_for(10000, 16, [&](std::int64_t i) { squares[i] = i * i; });
  bool ok = true;
  for (std::int64_t i = 0; i < 10000; ++i) ok = ok && squares[i] == i * i;
  CHECK(ok);
}

}  // namespace

int main() {
  const std::pair<const char*, std::function<void()>> suites[] = {
      {"decimal", decimal_fixtures},
      {"random streams", rng_fixtures},
      {"calendar", calendar_fixtures},
      {"round trip (PRD SIM-AC-03)", round_trip_fixture},
      {"shorts, crossing zero, borrow", short_fixtures},
      {"trailing stop, shared volume", trailing_and_volume_fixtures},
      {"refusals", refusals},
      {"generation", generation_properties},
      {"aggregation", aggregation_fixture},
      {"analytics", analytics_fixtures},
      {"parallel contract", parallel_contract},
  };
  for (const auto& [name, suite] : suites) {
    const int before = failures;
    try {
      suite();
    } catch (const std::exception& error) {
      ++failures;
      std::printf("FAIL %s: unexpected exception: %s\n", name, error.what());
    }
    std::printf("%-34s %s\n", name, failures == before ? "ok" : "FAILED");
  }
  std::printf("%d checks, %d failed\n", checks, failures);
  return failures == 0 ? 0 : 1;
}
