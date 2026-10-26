#include "engine.hpp"

#include <algorithm>
#include <map>
#include <optional>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "calendar.hpp"
#include "common.hpp"
#include "decimal.hpp"
#include "json.hpp"

namespace quanta::engine {

namespace {

// ---------------------------------------------------------------------------
// Account state

enum class Kind { Market, Limit, Stop, StopLimit, TrailingStop };
enum class Status { Working, PartiallyFilled, Filled, Canceled, Expired, Rejected, Held, Other };
// Any role other than "stop" and "target" is still a role: it marks a bracket
// leg when an interrupt asks, but only "stop" goes first in the bar.
enum class Role { None, Target, Stop, Other };

// Fields the engine can write on an order. They are reported in the order each
// was first assigned, which is the order Python inserts a key the order did not
// have yet.
enum class Field {
  ReservePrice,
  Triggered,
  TrailAnchor,
  StopPrice,
  Status,
  Reason,
  Quantity,
  Activates,
  Notional,
  Filled,
  Average,
  FeeRemaining,
};

struct Order {
  std::string id;
  std::string symbol;
  int column = -1;  // index of the symbol's bars, -1 when the run has none
  std::string side;
  bool buy = false;   // side == "buy"
  bool sell = false;  // side == "sell"
  Kind kind = Kind::Market;
  bool day_order = false;  // tif == "DAY"
  Status status = Status::Other;
  std::string status_text;
  std::int64_t quantity = 0;
  std::int64_t filled = 0;
  std::optional<Dec> limit_price, stop_price, trail_percent, trail_anchor;
  std::optional<Dec> average, notional, fee_remaining, reserve_price;
  std::optional<bool> triggered;
  bool forced = false;
  std::optional<std::int64_t> activates;
  bool has_day = false;
  std::int64_t day = 0;
  Role role = Role::None;
  std::string parent_id;  // empty when the order has none
  std::string oco_group;
  std::string reason;
  std::vector<Field> touched;
  // Set on buy-ins the engine raises itself; they are reported whole.
  bool raised = false;
  std::int64_t time = 0;
  std::string day_text;
};

struct Position {
  std::string symbol;
  std::int64_t quantity = 0;
  Dec cost;
  bool changed = false;  // reported back only when a fill touched it
};

struct Fill {
  std::size_t order = 0;
  std::int64_t quantity = 0;
  Dec price, fee, realized;
  std::int64_t time = 0;
};

struct LedgerEntry {
  bool borrow = false;
  std::size_t fill = 0;
  std::int64_t time = 0;
  std::int64_t cursor = 0;
  Dec amount, cash;
};

struct State {
  std::int64_t cursor = 0;
  Dec cash, realized;
  bool cash_changed = false;
  bool realized_changed = false;
  bool margin = false;
  std::optional<Dec> commission, slippage, spread, participation;
  Dec maintenance, borrow_rate;
  std::int64_t sessions_a_year = 252;
  std::vector<Position> positions;
  std::vector<Order> orders;
  std::size_t reported = 0;  // orders that came in with the request
  std::vector<Fill> fills;
  std::vector<LedgerEntry> ledger;
  std::unordered_map<std::string, std::size_t> first_by_id;
};

bool is_open(Status s) { return s == Status::Working || s == Status::PartiallyFilled; }
bool is_live(Status s) { return s == Status::Held || is_open(s); }

const char* status_name(Status s) {
  switch (s) {
    case Status::Working: return "working";
    case Status::PartiallyFilled: return "partially_filled";
    case Status::Filled: return "filled";
    case Status::Canceled: return "canceled";
    case Status::Expired: return "expired";
    case Status::Rejected: return "rejected";
    case Status::Held: return "held";
    case Status::Other: return "";
  }
  return "";
}

Status parse_status(const std::string& text) {
  static const std::pair<const char*, Status> names[] = {
      {"working", Status::Working},   {"partially_filled", Status::PartiallyFilled},
      {"filled", Status::Filled},     {"canceled", Status::Canceled},
      {"expired", Status::Expired},   {"rejected", Status::Rejected},
      {"held", Status::Held},
  };
  for (const auto& [name, status] : names) {
    if (text == name) return status;
  }
  return Status::Other;
}

void touch(Order& order, Field field) {
  if (std::find(order.touched.begin(), order.touched.end(), field) == order.touched.end()) {
    order.touched.push_back(field);
  }
}

void set_status(Order& order, Status status) {
  order.status = status;
  order.status_text = status_name(status);
  touch(order, Field::Status);
}

void set_reason(Order& order, std::string reason) {
  order.reason = std::move(reason);
  touch(order, Field::Reason);
}

const Dec& required(const std::optional<Dec>& value, const char* name) {
  if (!value) fail(std::string("order or config field '") + name + "' is missing");
  return *value;
}

const Dec kZero = Dec::of(0);
const Dec kOne = Dec::of(1);
const Dec kTwo = Dec::of(2);
const Dec kHundred = Dec::of(100);
const Dec kTenThousand = Dec::of(10000);
const Dec kCent = Dec::parse("0.01");

Dec money_value(const Dec& value) { return quantize(value, -2, Rounding::HalfUp); }

std::int64_t position_quantity(const State& s, const std::string& symbol) {
  for (const Position& p : s.positions) {
    if (p.symbol == symbol) return p.quantity;
  }
  return 0;
}

Position& position_for(State& s, const std::string& symbol) {
  for (Position& p : s.positions) {
    if (p.symbol == symbol) return p;
  }
  s.positions.push_back(Position{symbol, 0, Dec::parse("0.00"), true});
  return s.positions.back();
}

int first_index(const State& s, const std::string& id) {
  const auto found = s.first_by_id.find(id);
  return found == s.first_by_id.end() ? -1 : static_cast<int>(found->second);
}

// ---------------------------------------------------------------------------
// Market data

struct Bar {
  Dec open, high, low, close, volume;
  double close_float = 0.0;
  std::int64_t time = 0;
  std::int32_t day = 0;
};

class Market {
 public:
  // A market with no symbols serves the operations that never read a bar:
  // reservations and retiring orphaned exits.
  Market(const Bars* bars, std::int32_t count, std::vector<std::string> names)
      : bars_(bars), names_(std::move(names)) {
    require(count >= 0 && static_cast<std::size_t>(count) == names_.size(),
            "symbols do not match the bars supplied");
    require(count == 0 || bars != nullptr, "bars are missing");
    for (std::int32_t i = 0; i < count; ++i) {
      const Bars& b = bars[i];
      require(b.length >= 1 && b.time && b.day, "every symbol needs times and days");
      require(b.volume_int || b.volume_float, "every symbol needs a volume column");
      for (int k = 0; k < 4; ++k) require(b.cents[k] || b.values[k], "every symbol needs prices");
      index_.emplace(names_[i], i);
    }
  }

  int column(const std::string& symbol) const {
    const auto found = index_.find(symbol);
    return found == index_.end() ? -1 : found->second;
  }

  const std::vector<std::string>& names() const { return names_; }
  std::int64_t length(int column) const { return bars_[column].length; }

  Dec price(int column, int field, std::int64_t index) const {
    check(column, index);
    const Bars& b = bars_[column];
    if (b.cents[field]) return Dec::cents(b.cents[field][index]);
    return Dec::of_double(b.values[field][index]);
  }

  double close_float(int column, std::int64_t index) const {
    check(column, index);
    const Bars& b = bars_[column];
    if (b.cents[3]) return static_cast<double>(b.cents[3][index]) / 100.0;
    return b.values[3][index];
  }

  std::int64_t time(int column, std::int64_t index) const {
    check(column, index);
    return bars_[column].time[index];
  }

  std::int32_t day(int column, std::int64_t index) const {
    check(column, index);
    return bars_[column].day[index];
  }

  Bar bar(int column, std::int64_t index) const {
    check(column, index);
    const Bars& b = bars_[column];
    Bar out;
    out.open = price(column, 0, index);
    out.high = price(column, 1, index);
    out.low = price(column, 2, index);
    out.close = price(column, 3, index);
    out.volume = b.volume_int ? Dec::of(b.volume_int[index]) : Dec::of_double(b.volume_float[index]);
    out.close_float = close_float(column, index);
    out.time = b.time[index];
    out.day = b.day[index];
    return out;
  }

 private:
  void check(int column, std::int64_t index) const {
    require(column >= 0 && static_cast<std::size_t>(column) < names_.size(), "unknown symbol column");
    require(index >= 0 && index < bars_[column].length, "bar index out of range");
  }

  const Bars* bars_;
  std::vector<std::string> names_;
  std::unordered_map<std::string, int> index_;
};

int column_of(const Market& m, const Order& order) {
  if (order.column < 0) throw DomainError("This stock is unavailable in this run.");
  (void)m;
  return order.column;
}

// symbol -> close at the cursor, for every symbol in the run, in run order.
using Marks = std::vector<std::pair<std::string, Dec>>;

Marks marks(const Market& m, std::int64_t cursor) {
  Marks out;
  out.reserve(m.names().size());
  for (std::size_t i = 0; i < m.names().size(); ++i) {
    out.emplace_back(m.names()[i], m.price(static_cast<int>(i), 3, cursor));
  }
  return out;
}

const Dec* mark_of(const Marks& prices, const std::string& symbol) {
  for (const auto& [name, price] : prices) {
    if (name == symbol) return &price;
  }
  return nullptr;
}

// ---------------------------------------------------------------------------
// Reservations and margin

struct Reserved {
  Dec cash;
  std::vector<std::pair<std::string, std::int64_t>> shares;  // in insertion order

  std::int64_t shares_of(const std::string& symbol) const {
    for (const auto& [name, count] : shares) {
      if (name == symbol) return count;
    }
    return 0;
  }

  void add_shares(const std::string& symbol, std::int64_t count) {
    for (auto& [name, held] : shares) {
      if (name == symbol) {
        held += count;
        return;
      }
    }
    shares.emplace_back(symbol, count);
  }
};

// Cash and shares already committed to working orders.
//
// Legs of one OCO group are alternatives, not additions: only one can ever
// fill, so the group reserves the largest of its legs. Excluding an order
// excludes its whole group, so re-validating one leg does not count the shares
// its sibling is holding against it.
Reserved reservations(const State& s, const std::string* exclude) {
  std::unordered_set<std::string> excluded;
  if (exclude && !exclude->empty()) {
    excluded.insert(*exclude);
    const int target = first_index(s, *exclude);
    if (target >= 0 && !s.orders[target].oco_group.empty()) {
      for (const Order& o : s.orders) {
        if (o.oco_group == s.orders[target].oco_group) excluded.insert(o.id);
      }
    }
  }
  Dec cash = kZero;
  struct Group {
    std::string symbol, key;
    std::int64_t remaining;
  };
  std::vector<Group> groups;
  std::vector<std::pair<std::string, Dec>> sell_prices;
  std::vector<std::pair<std::string, std::vector<std::pair<Dec, std::int64_t>>>> buys;
  for (const Order& order : s.orders) {
    if (excluded.count(order.id) || !is_open(order.status)) continue;
    const std::int64_t remaining = order.quantity - order.filled;
    if (order.buy) {
      // The commission is owed either way; the stock itself may not be.
      cash = cash + required(order.fee_remaining, "fee_remaining");
      auto found = std::find_if(buys.begin(), buys.end(),
                                [&](const auto& entry) { return entry.first == order.symbol; });
      if (found == buys.end()) {
        buys.emplace_back(order.symbol, std::vector<std::pair<Dec, std::int64_t>>{});
        found = buys.end() - 1;
      }
      found->second.emplace_back(required(order.reserve_price, "reserve_price"), remaining);
    } else {
      const std::string& key = order.oco_group.empty() ? order.id : order.oco_group;
      auto group = std::find_if(groups.begin(), groups.end(), [&](const Group& g) {
        return g.symbol == order.symbol && g.key == key;
      });
      if (group == groups.end()) {
        groups.push_back(Group{order.symbol, key, 0});
        group = groups.end() - 1;
      }
      group->remaining = std::max(group->remaining, remaining);
      const Dec& price = required(order.reserve_price, "reserve_price");
      auto existing = std::find_if(sell_prices.begin(), sell_prices.end(),
                                   [&](const auto& entry) { return entry.first == order.symbol; });
      if (existing == sell_prices.end()) sell_prices.emplace_back(order.symbol, price);
      else existing->second = price;
    }
  }
  for (const auto& [symbol, legs] : buys) {
    // Buying back borrowed stock returns something the account already owes. It
    // commits no new capital, so a short that moved against the account stays
    // closable at the moment that matters most.
    std::int64_t owed = std::max<std::int64_t>(0, -position_quantity(s, symbol));
    for (const auto& [price, remaining] : legs) {
      const std::int64_t covering = std::min(remaining, owed);
      owed -= covering;
      cash = cash + price * Dec::of(remaining - covering);
    }
  }
  Reserved out;
  for (const Group& group : groups) {
    // Only the part of a sale covered by stock already held reserves stock. The
    // rest is borrowed, and consumes buying power at its full value.
    const std::int64_t held = std::max<std::int64_t>(0, position_quantity(s, group.symbol));
    const std::int64_t covered =
        std::min(group.remaining, std::max<std::int64_t>(0, held - out.shares_of(group.symbol)));
    out.add_shares(group.symbol, covered);
    const std::int64_t borrowed = group.remaining - covered;
    if (borrowed) {
      const auto price = std::find_if(sell_prices.begin(), sell_prices.end(),
                                      [&](const auto& entry) { return entry.first == group.symbol; });
      cash = cash + price->second * Dec::of(borrowed);
    }
  }
  out.cash = cash;
  return out;
}

// Account equity and the gross value of everything it is carrying. A short
// counts at the value owed, not at minus it.
std::pair<Dec, Dec> exposure(const State& s, const Marks& prices) {
  Dec equity = s.cash;
  Dec gross = kZero;
  for (const Position& position : s.positions) {
    if (!position.quantity) continue;
    const Dec* price = mark_of(prices, position.symbol);
    if (!price) continue;
    const Dec value = *price * Dec::of(position.quantity);
    equity = equity + value;
    gross = gross + abs(value);
  }
  return {equity, gross};
}

// Twice equity less what is carried, at 50% initial margin. A cash account is
// bounded by its cash instead.
Dec buying_power(const State& s, const Marks& prices) {
  const auto [equity, gross] = exposure(s, prices);
  if (!s.margin) return s.cash;
  return max_of(kZero, equity * kTwo - gross);
}

Dec capital(const State& s, const Market& m) {
  if (!s.margin) return s.cash;
  return buying_power(s, marks(m, s.cursor));
}

bool has_shorts(const State& s) {
  for (const Position& p : s.positions) {
    if (p.quantity < 0) return true;
  }
  return false;
}

Dec borrow_fee(const State& s, const Marks& prices) {
  Dec total = kZero;
  for (const Position& position : s.positions) {
    if (position.quantity >= 0) continue;
    const Dec* price = mark_of(prices, position.symbol);
    if (!price) continue;
    total = total + (*price * Dec::of(-position.quantity) * s.borrow_rate) / Dec::of(s.sessions_a_year);
  }
  return quantize(total, -2, Rounding::HalfUp);
}

// Equity below the maintenance requirement on what the account carries.
bool called(const State& s, const Marks& prices) {
  if (!s.margin || !has_shorts(s)) return false;
  const auto [equity, gross] = exposure(s, prices);
  return gross > kZero && equity < s.maintenance * gross;
}

// ---------------------------------------------------------------------------
// Order rules

void validate_order(State& s, const Market& m, Order& order, const std::string* exclude) {
  const int column = column_of(m, order);
  const Dec mark = m.price(column, 3, s.cursor);
  const bool limited = order.kind == Kind::Limit || order.kind == Kind::StopLimit;
  const bool stopped = order.kind == Kind::Stop || order.kind == Kind::StopLimit;
  if (limited && !order.limit_price) throw DomainError("A limit price is required.");
  if (stopped && !order.stop_price) throw DomainError("A stop trigger price is required.");
  if (order.kind == Kind::TrailingStop) {
    if (!order.trail_percent) throw DomainError("A trailing stop needs a trail percentage.");
    if (!order.sell) throw DomainError("This paper account trails stops on exits only.");
  } else if (order.trail_percent) {
    throw DomainError("Only a trailing stop accepts a trail percentage.");
  }
  if (!limited && order.limit_price) throw DomainError("This order type does not accept a limit price.");
  if (!stopped && order.kind != Kind::TrailingStop && order.stop_price) {
    throw DomainError("This order type does not accept a stop price.");
  }
  Dec reserve = order.limit_price ? *order.limit_price
                                  : max_of(mark, order.stop_price ? *order.stop_price : mark);
  if (!limited) {
    const Dec friction =
        (required(s.slippage, "slippage_bps") + required(s.spread, "spread_bps") / kTwo) / kTenThousand;
    reserve = reserve * (friction + kOne);
  }
  reserve = quantize(reserve, -2, Rounding::Ceiling);
  order.reserve_price = reserve;
  touch(order, Field::ReservePrice);

  const Reserved reserved = reservations(s, exclude);
  const std::int64_t remaining = order.quantity - order.filled;
  // A cash account can spend its cash. A margin account can spend its buying
  // power: short proceeds sit in the cash balance and are owed back.
  const Dec capacity = s.margin ? buying_power(s, marks(m, s.cursor)) : s.cash;
  const std::int64_t held = position_quantity(s, order.symbol);
  const Dec& fee = required(order.fee_remaining, "fee_remaining");
  if (order.buy) {
    std::int64_t queued = 0;
    for (const Order& other : s.orders) {
      if (other.id != order.id && other.buy && other.symbol == order.symbol && is_open(other.status)) {
        queued += other.quantity - other.filled;
      }
    }
    // Returning borrowed stock needs no buying power.
    const std::int64_t covering = std::min(remaining, std::max<std::int64_t>(0, -held - queued));
    const std::int64_t opening = remaining - covering;
    if (reserve * Dec::of(opening) + fee > capacity - reserved.cash) {
      throw DomainError(s.margin
                            ? "Insufficient buying power, including fees and other working orders."
                            : "Insufficient available cash, including fees and other working orders.");
    }
    return;
  }
  const std::int64_t available = std::max<std::int64_t>(0, held) - reserved.shares_of(order.symbol);
  const std::int64_t borrowed = remaining - available;
  if (borrowed <= 0) return;
  if (!s.margin) throw DomainError("Insufficient available shares. This paper account is long-only.");
  // A short consumes buying power at the full value of the stock borrowed.
  if (reserve * Dec::of(borrowed) + fee > capacity - reserved.cash) {
    throw DomainError("Insufficient margin to borrow this stock, including other working orders.");
  }
}

void set_money(Order& order, Field field, std::optional<Dec>& slot, const Dec& value) {
  slot = money_value(value);
  touch(order, field);
}

// Ratchet a trailing stop, after this bar has been tested against the old one.
void trail(Order& order, const Bar& bar) {
  const Dec percent = required(order.trail_percent, "trail_percent") / kHundred;
  const Dec anchor = max_of(order.trail_anchor ? *order.trail_anchor : bar.close, bar.high);
  set_money(order, Field::TrailAnchor, order.trail_anchor, anchor);
  set_money(order, Field::StopPrice, order.stop_price,
            quantize(anchor * (kOne - percent), -2, Rounding::HalfUp));
}

bool triggered(const Order& order) {
  if (!order.triggered) fail("order field 'triggered' is missing");
  return *order.triggered;
}

void set_triggered(Order& order) {
  order.triggered = true;
  touch(order, Field::Triggered);
}

std::optional<Dec> execution_price(Order& order, const Bar& bar) {
  const bool buy = order.buy;
  if (order.kind == Kind::TrailingStop) {
    if (!triggered(order)) {
      const Dec& stop = required(order.stop_price, "stop_price");
      if (bar.low > stop) return std::nullopt;
      set_triggered(order);
      return min_of(bar.open, stop);
    }
    return bar.open;
  }
  if ((order.kind == Kind::Stop || order.kind == Kind::StopLimit) && !triggered(order)) {
    const Dec& stop = required(order.stop_price, "stop_price");
    if (buy ? bar.high < stop : bar.low > stop) return std::nullopt;
    set_triggered(order);
    // The intrabar path is unknown. Trigger now; earliest fill next bar.
    if (order.kind == Kind::StopLimit) return std::nullopt;
    return buy ? max_of(bar.open, stop) : min_of(bar.open, stop);
  }
  if (order.kind == Kind::Limit || order.kind == Kind::StopLimit) {
    const Dec& limit = required(order.limit_price, "limit_price");
    // A touch alone does not fill a passive order in this conservative bar model.
    if (buy ? bar.open <= limit : bar.open >= limit) {
      return buy ? min_of(bar.open, limit) : max_of(bar.open, limit);
    }
    if (buy ? bar.low < limit : bar.high > limit) return limit;
    return std::nullopt;
  }
  return bar.open;
}

// Bring a held exit to life on the bar after the entry it protects filled.
void arm(Order& leg, const Order& parent, std::int64_t cursor) {
  set_status(leg, Status::Working);
  leg.activates = cursor + 1;
  touch(leg, Field::Activates);
  set_reason(leg, "Working: the entry it protects has filled.");
  if (leg.kind == Kind::TrailingStop && !leg.trail_anchor) {
    const Dec anchor = required(parent.average, "average");
    set_money(leg, Field::TrailAnchor, leg.trail_anchor, anchor);
    const Dec percent = required(leg.trail_percent, "trail_percent") / kHundred;
    set_money(leg, Field::StopPrice, leg.stop_price,
              quantize(anchor * (kOne - percent), -2, Rounding::HalfUp));
  }
}

// Size a bracket's exits to the shares its entry is actually holding open, and
// cancel them when there is nothing left to protect.
void rebalance(State& s, std::size_t index, std::int64_t cursor) {
  const std::string parent_id =
      s.orders[index].parent_id.empty() ? s.orders[index].id : s.orders[index].parent_id;
  const int parent = first_index(s, parent_id);
  std::vector<std::size_t> legs;
  for (std::size_t i = 0; i < s.orders.size(); ++i) {
    if (!s.orders[i].parent_id.empty() && s.orders[i].parent_id == parent_id) legs.push_back(i);
  }
  if (parent < 0 || legs.empty()) return;
  std::int64_t still_open = s.orders[parent].filled;
  for (const std::size_t leg : legs) still_open -= s.orders[leg].filled;
  for (const std::size_t i : legs) {
    Order& leg = s.orders[i];
    const Order& entry = s.orders[parent];
    if (!is_live(leg.status)) continue;
    if (still_open > 0) {
      leg.quantity = leg.filled + still_open;
      touch(leg, Field::Quantity);
      if (leg.status == Status::Held) arm(leg, entry, cursor);
    } else if (is_open(entry.status)) {
      // Flat for now, but more shares are coming and will need protecting.
      leg.quantity = leg.filled;
      touch(leg, Field::Quantity);
      set_reason(leg, "Idle: waiting for the rest of the entry to fill.");
    } else {
      std::string reason = entry.filled
                               ? std::string("Canceled: this bracket has nothing left to protect.")
                               : "Canceled: the entry it was attached to was " + entry.status_text + ".";
      set_status(leg, Status::Canceled);
      set_reason(leg, std::move(reason));
    }
  }
}

void retire_orphans(State& s) {
  std::vector<std::string> parents;
  std::unordered_set<std::string> seen;
  for (const Order& o : s.orders) {
    if (!o.parent_id.empty() && seen.insert(o.parent_id).second) parents.push_back(o.parent_id);
  }
  for (const std::string& parent_id : parents) {
    const int parent = first_index(s, parent_id);
    if (parent >= 0) rebalance(s, static_cast<std::size_t>(parent), s.cursor);
  }
}

// Stops first: when a bar covers both legs, the conservative reading is that
// the stop went first.
std::vector<std::size_t> sequence(const State& s) {
  std::vector<std::size_t> out;
  out.reserve(s.orders.size());
  for (std::size_t i = 0; i < s.orders.size(); ++i) {
    if (s.orders[i].role == Role::Stop) out.push_back(i);
  }
  for (std::size_t i = 0; i < s.orders.size(); ++i) {
    if (s.orders[i].role != Role::Stop) out.push_back(i);
  }
  return out;
}

bool session_end(const Market& m, std::int64_t cursor) {
  require(!m.names().empty(), "this operation needs market data");
  if (cursor + 1 >= m.length(0)) return true;
  return m.day(0, cursor) != m.day(0, cursor + 1);
}

void register_order(State& s, Order order) {
  s.first_by_id.emplace(order.id, s.orders.size());
  s.orders.push_back(std::move(order));
}

// A market order the account did not ask for, to close a called position.
void buy_in(State& s, const Market& m, const std::string& symbol, std::int64_t quantity,
            const std::string& reason) {
  const int column = m.column(symbol);
  if (column < 0) throw DomainError("This stock is unavailable in this run.");
  Order order;
  order.id = "buyin:" + symbol + ":" + std::to_string(s.cursor);
  order.symbol = symbol;
  order.column = column;
  order.side = "buy";
  order.buy = true;
  order.kind = Kind::Market;
  order.quantity = quantity;
  order.status = Status::Working;
  order.status_text = "working";
  order.average = Dec::parse("0.00");
  order.notional = Dec::parse("0.00");
  order.fee_remaining = money_value(required(s.commission, "commission"));
  order.reserve_price = money_value(Dec::of_double(m.close_float(column, s.cursor) * 2.0));
  order.triggered = false;
  order.forced = true;
  order.activates = s.cursor + 1;
  order.time = m.time(column, s.cursor);
  order.day_text = calendar::iso_date(m.day(column, s.cursor));
  order.has_day = true;
  order.day = m.day(column, s.cursor);
  order.reason = reason;
  order.raised = true;
  register_order(s, std::move(order));
}

// End-of-session financing, then the maintenance check, on the balance the
// account actually has after paying its bills.
void settle_margin(State& s, const Market& m) {
  if (!s.margin) return;
  const Marks prices = marks(m, s.cursor);
  if (session_end(m, s.cursor)) {
    const Dec fee = borrow_fee(s, prices);
    if (fee > kZero) {
      s.cash = money_value(s.cash - fee);
      s.cash_changed = true;
      LedgerEntry entry;
      entry.borrow = true;
      entry.time = m.time(0, s.cursor);
      entry.cursor = s.cursor;
      entry.amount = money_value(-fee);
      entry.cash = s.cash;
      s.ledger.push_back(entry);
    }
  }
  if (!called(s, prices)) return;
  const std::int64_t percent = to_int64(s.maintenance * kHundred);
  const std::string reason = "Bought in: account equity fell under the " + std::to_string(percent) +
                             "% maintenance requirement on its borrowed stock.";
  std::vector<std::pair<std::string, std::int64_t>> short_positions;
  for (const Position& p : s.positions) {
    if (p.quantity < 0) short_positions.emplace_back(p.symbol, p.quantity);
  }
  for (const auto& [symbol, quantity] : short_positions) {
    std::int64_t pending = 0;
    for (const Order& o : s.orders) {
      if (o.forced && o.symbol == symbol && is_open(o.status)) pending += o.quantity - o.filled;
    }
    const std::int64_t outstanding = -quantity - pending;
    if (outstanding > 0) buy_in(s, m, symbol, outstanding, reason);
  }
}

struct Watch {
  bool fill = false, bracket = false, margin_call = false;
  bool any = false;
};

std::optional<std::string> interrupt(const State& s, std::size_t fills_before, std::size_t orders_before,
                                     const std::map<std::int64_t, std::string>& scheduled,
                                     const Watch& watch) {
  if (watch.fill || watch.bracket) {
    for (std::size_t k = fills_before; k < s.fills.size(); ++k) {
      const Fill& fill = s.fills[k];
      const Order& filled = s.orders[fill.order];
      const int first = first_index(s, filled.id);
      const Role role = first >= 0 ? s.orders[first].role : Role::None;
      if (role != Role::None && watch.bracket) {
        return std::string("Your ") + (role == Role::Target ? "target" : "stop") + " leg filled " +
               std::to_string(fill.quantity) + " " + filled.symbol + ".";
      }
      if (watch.fill) {
        return "Your order filled: " + filled.side + " " + std::to_string(fill.quantity) + " " +
               filled.symbol + " at " + fill.price.str() + ".";
      }
    }
  }
  if (watch.margin_call && s.orders.size() > orders_before) {
    for (std::size_t k = orders_before; k < s.orders.size(); ++k) {
      if (s.orders[k].forced) return s.orders[k].reason;
    }
  }
  const auto found = scheduled.find(s.cursor);
  if (found != scheduled.end()) return found->second;
  return std::nullopt;
}

std::optional<std::string> advance(State& s, const Market& m, std::int64_t steps,
                                   const std::map<std::int64_t, std::string>& scheduled,
                                   const Watch& watch) {
  require(!m.names().empty(), "advancing the clock needs market data");
  const std::int64_t last = m.length(0) - 1;
  std::optional<std::string> stop;
  const std::int64_t rounds = std::min(steps, last - s.cursor);
  for (std::int64_t round = 0; round < rounds; ++round) {
    const std::size_t fills_before = s.fills.size();
    const std::size_t orders_before = s.orders.size();
    s.cursor += 1;
    std::vector<std::pair<std::string, std::int64_t>> used;
    auto used_by = [&](const std::string& symbol) -> std::int64_t& {
      for (auto& [name, count] : used) {
        if (name == symbol) return count;
      }
      used.emplace_back(symbol, 0);
      return used.back().second;
    };
    // A bar is a pure function of its symbol and the cursor, so each symbol's is
    // read once per step however many orders it has.
    std::vector<std::optional<Bar>> read(m.names().size());
    for (const std::size_t index : sequence(s)) {
      Order& order = s.orders[index];
      if (!is_open(order.status)) continue;
      if (order.activates && s.cursor < *order.activates) continue;
      const int column = column_of(m, order);
      if (!read[column]) read[column] = m.bar(column, s.cursor);
      const Bar& bar = *read[column];
      if (order.day_order && !(order.has_day && order.day == bar.day)) {
        set_status(order, Status::Expired);
        set_reason(order, "DAY order expired at the session boundary.");
        continue;
      }
      const std::optional<Dec> quoted = execution_price(order, bar);
      if (!quoted) {
        if (order.kind == Kind::TrailingStop) trail(order, bar);
        continue;
      }
      const Dec friction =
          (required(s.slippage, "slippage_bps") + required(s.spread, "spread_bps") / kTwo) / kTenThousand;
      Dec price = *quoted * (order.buy ? friction + kOne : kOne - friction);
      if (order.kind == Kind::Limit || order.kind == Kind::StopLimit) {
        const Dec& limit = *order.limit_price;
        price = order.buy ? min_of(price, limit) : max_of(price, limit);
      }
      price = max_of(kCent, money_value(price));
      const std::int64_t capacity = to_int64(bar.volume * required(s.participation, "participation"));
      std::int64_t& taken = used_by(order.symbol);
      std::int64_t quantity =
          std::min(order.quantity - order.filled, std::max<std::int64_t>(0, capacity - taken));
      if (!quantity) continue;
      const Dec fee = required(order.fee_remaining, "fee_remaining");
      std::int64_t held = position_quantity(s, order.symbol);
      if (order.buy) {
        const Reserved reserved = reservations(s, &order.id);
        // Buying back borrowed stock is never refused for cash; the balance going
        // negative is the debt the margin call answers.
        const std::int64_t covering = std::max<std::int64_t>(0, std::min(quantity, -held));
        const Dec funds = capital(s, m) - reserved.cash - fee;
        const std::int64_t opening = funds > kZero ? to_int64(to_integral_down(funds / price)) : 0;
        quantity = std::min(quantity, checked_add(covering, std::max<std::int64_t>(0, opening)));
        if (quantity == 0) {
          set_status(order, Status::Rejected);
          set_reason(order, order.forced ? "The execution price gap exceeded available buying power."
                                         : "The execution price gap exceeded available cash.");
          continue;
        }
      }
      if (order.sell && held >= quantity && !s.margin) {
        const Reserved reserved = reservations(s, &order.id);
        if (s.cash + price * Dec::of(quantity) - fee < reserved.cash) {
          set_status(order, Status::Rejected);
          set_reason(order, "Sale proceeds and available cash cannot cover the commission.");
          continue;
        }
      }
      Position& position = position_for(s, order.symbol);
      // Cost is signed: what a long paid, or minus what a short was paid, so
      // value - cost is the unrealized result in both directions.
      held = position.quantity;
      Dec cost = position.cost;
      const std::int64_t direction = order.buy ? 1 : -1;
      const Dec flow = order.buy ? -price : price;
      // A fill can close one position and open the opposite one.
      const std::int64_t magnitude = held < 0 ? -held : held;
      const std::int64_t closing =
          (held && ((held > 0) != (direction > 0))) ? std::min(quantity, magnitude) : 0;
      const std::int64_t opening = quantity - closing;
      Dec realized = kZero;
      if (closing) {
        // All cost is allocated on the final exit so rounding cannot leave a residue.
        const Dec basis = closing == magnitude
                              ? cost
                              : money_value(cost * Dec::of(closing) / Dec::of(magnitude));
        realized = flow * Dec::of(closing) - basis - fee;
        cost = cost - basis;
        held += direction * closing;
        s.realized = money_value(s.realized + realized);
        s.realized_changed = true;
      }
      if (opening) {
        // Opening carries the fee only when no closing leg already did.
        cost = cost + (-flow * Dec::of(opening) + (closing ? kZero : fee));
        held += direction * opening;
      }
      position.quantity = held;
      position.cost = money_value(cost);
      position.changed = true;
      const Dec notional = price * Dec::of(quantity);
      const Dec change = flow * Dec::of(quantity) - fee;
      s.cash = money_value(s.cash + change);
      s.cash_changed = true;
      set_money(order, Field::Notional, order.notional, required(order.notional, "notional") + notional);
      order.filled += quantity;
      touch(order, Field::Filled);
      set_money(order, Field::Average, order.average, *order.notional / Dec::of(order.filled));
      order.fee_remaining = Dec::parse("0.00");
      touch(order, Field::FeeRemaining);
      set_status(order, order.filled == order.quantity ? Status::Filled : Status::PartiallyFilled);
      if (!order.forced) {
        // A buy-in keeps the reason it was raised for: it is the only record of
        // why the account bought something it never asked for.
        set_reason(order, "Filled on the next eligible bar, subject to shared volume participation.");
      }
      taken += quantity;
      // An entry that filled arms its exits; an exit that filled resizes its
      // siblings. Both are the same recomputation over the group.
      rebalance(s, index, s.cursor);
      Fill fill;
      fill.order = index;
      fill.quantity = quantity;
      fill.price = price;
      fill.fee = money_value(fee);
      fill.realized = money_value(realized);
      fill.time = bar.time;
      s.fills.push_back(fill);
      LedgerEntry entry;
      entry.fill = s.fills.size() - 1;
      entry.time = bar.time;
      entry.amount = money_value(change);
      entry.cash = s.cash;
      s.ledger.push_back(entry);
      // Reserve the remaining quantity at the current estimate; close it if it
      // is no longer affordable.
      Order& after = s.orders[index];
      if (is_open(after.status) && !after.forced) {
        try {
          validate_order(s, m, after, &after.id);
        } catch (const DomainError&) {
          set_status(after, Status::Canceled);
          set_reason(after, "Remaining quantity canceled: insufficient buying power after the gap fill.");
        }
      }
    }
    settle_margin(s, m);
    if (!scheduled.empty() || watch.any) {
      stop = interrupt(s, fills_before, orders_before, scheduled, watch);
      if (stop && !stop->empty()) break;
    }
  }
  retire_orphans(s);
  // At a session's last known bar, DAY orders cannot remain working overnight.
  const std::int64_t cursor = s.cursor;
  for (Order& order : s.orders) {
    if (!is_open(order.status) || !order.day_order) continue;
    const int column = order.column;
    require(column >= 0, "a working order names a symbol the run does not carry");
    if (cursor == last || m.day(column, cursor) != m.day(column, cursor + 1)) {
      set_status(order, Status::Expired);
      set_reason(order, "DAY order expired at the end of its session.");
    }
  }
  retire_orphans(s);
  if (stop && stop->empty()) stop.reset();
  return stop;
}

// ---------------------------------------------------------------------------
// Request parsing and response writing

std::optional<Dec> optional_decimal(const json::Value& object, std::string_view key) {
  const json::Value* value = object.find(key);
  if (!value || value->is_null()) return std::nullopt;
  return Dec::parse(value->as_string(key));
}

std::string optional_text(const json::Value& object, std::string_view key) {
  const json::Value* value = object.find(key);
  if (!value || value->is_null()) return {};
  return value->as_string(key);
}

Kind parse_kind(const std::string& text) {
  if (text == "limit") return Kind::Limit;
  if (text == "stop") return Kind::Stop;
  if (text == "stop_limit") return Kind::StopLimit;
  if (text == "trailing_stop") return Kind::TrailingStop;
  return Kind::Market;
}

Order parse_order(const json::Value& value, const Market& m) {
  require(value.type == json::Value::Type::Object, "every order must be an object");
  Order o;
  o.id = value.at("id").as_string("id");
  o.symbol = value.at("symbol").as_string("symbol");
  o.column = m.column(o.symbol);
  o.side = value.at("side").as_string("side");
  o.buy = o.side == "buy";
  o.sell = o.side == "sell";
  o.kind = parse_kind(value.at("kind").as_string("kind"));
  o.day_order = value.at("tif").as_string("tif") == "DAY";
  o.status_text = value.at("status").as_string("status");
  o.status = parse_status(o.status_text);
  o.quantity = value.at("quantity").as_int("quantity");
  o.filled = value.at("filled").as_int("filled");
  require(o.quantity >= 0 && o.quantity <= 1000000000000LL, "order quantity out of range");
  require(o.filled >= 0 && o.filled <= 1000000000000LL, "filled quantity out of range");
  o.limit_price = optional_decimal(value, "limit_price");
  o.stop_price = optional_decimal(value, "stop_price");
  o.trail_percent = optional_decimal(value, "trail_percent");
  o.trail_anchor = optional_decimal(value, "trail_anchor");
  o.average = optional_decimal(value, "average");
  o.notional = optional_decimal(value, "notional");
  o.fee_remaining = optional_decimal(value, "fee_remaining");
  o.reserve_price = optional_decimal(value, "reserve_price");
  if (const json::Value* t = value.find("triggered"); t && !t->is_null()) o.triggered = t->as_bool("triggered");
  if (const json::Value* f = value.find("forced"); f && !f->is_null()) o.forced = f->as_bool("forced");
  if (const json::Value* a = value.find("activates"); a && !a->is_null()) o.activates = a->as_int("activates");
  const std::string day = optional_text(value, "day");
  o.has_day = calendar::parse_iso_date(day, o.day);
  const std::string role = optional_text(value, "role");
  o.role = role.empty() ? Role::None : role == "stop" ? Role::Stop : role == "target" ? Role::Target : Role::Other;
  o.parent_id = optional_text(value, "parent_id");
  o.oco_group = optional_text(value, "oco_group");
  return o;
}

State parse_state(const json::Value& request, const Market& m) {
  // The bounds below are what keep every integer sum in the engine inside
  // int64: at most a million orders of at most 10^12 shares, positions within
  // 10^15. Anything outside them is corrupt state, refused rather than wrapped.
  State s;
  s.cursor = request.at("cursor").as_int("cursor");
  require(s.cursor >= 0 && s.cursor <= 1000000000, "cursor out of range");
  const json::Value& config = request.at("config");
  s.commission = optional_decimal(config, "commission");
  s.slippage = optional_decimal(config, "slippage_bps");
  s.spread = optional_decimal(config, "spread_bps");
  s.participation = optional_decimal(config, "participation");
  s.margin = optional_text(config, "account") == "margin";
  const json::Value& rules = request.at("margin");
  s.maintenance = Dec::parse(rules.at("maintenance").as_string("maintenance"));
  s.borrow_rate = Dec::parse(rules.at("borrow_rate").as_string("borrow_rate"));
  s.sessions_a_year = rules.at("sessions_a_year").as_int("sessions_a_year");
  require(s.sessions_a_year > 0, "sessions_a_year must be positive");
  s.cash = Dec::parse(request.at("cash").as_string("cash"));
  s.realized = Dec::parse(request.at("realized").as_string("realized"));
  for (const json::Value& entry : request.at("positions").as_array("positions")) {
    const auto& fields = entry.as_array("position");
    require(fields.size() == 3, "a position is [symbol, quantity, cost]");
    const std::int64_t quantity = fields[1].as_int("position quantity");
    require(quantity >= -1000000000000000LL && quantity <= 1000000000000000LL,
            "position quantity out of range");
    s.positions.push_back(Position{fields[0].as_string("position symbol"), quantity,
                                   Dec::parse(fields[2].as_string("position cost")), false});
  }
  const auto& orders = request.at("orders").as_array("orders");
  require(orders.size() <= 1000000, "too many orders");
  for (const json::Value& entry : orders) register_order(s, parse_order(entry, m));
  s.reported = s.orders.size();
  return s;
}

void write_money(json::Writer& w, const std::optional<Dec>& value) {
  if (value) w.string(value->str());
  else w.null();
}

void write_field(json::Writer& w, const Order& o, Field field) {
  w.begin_array();
  switch (field) {
    case Field::ReservePrice: w.string("reserve_price"); write_money(w, o.reserve_price); break;
    case Field::Triggered: w.string("triggered"); w.boolean(o.triggered.value_or(false)); break;
    case Field::TrailAnchor: w.string("trail_anchor"); write_money(w, o.trail_anchor); break;
    case Field::StopPrice: w.string("stop_price"); write_money(w, o.stop_price); break;
    case Field::Status: w.string("status"); w.string(o.status_text); break;
    case Field::Reason: w.string("reason"); w.string(o.reason); break;
    case Field::Quantity: w.string("quantity"); w.integer(o.quantity); break;
    case Field::Activates:
      w.string("activates");
      if (o.activates) w.integer(*o.activates);
      else w.null();
      break;
    case Field::Notional: w.string("notional"); write_money(w, o.notional); break;
    case Field::Filled: w.string("filled"); w.integer(o.filled); break;
    case Field::Average: w.string("average"); write_money(w, o.average); break;
    case Field::FeeRemaining: w.string("fee_remaining"); write_money(w, o.fee_remaining); break;
  }
  w.end_array();
}

// A buy-in, whole, in the key order the Python engine built it.
void write_raised(json::Writer& w, const Order& o) {
  w.begin_object();
  w.key("id").string(o.id);
  w.key("symbol").string(o.symbol);
  w.key("side").string(o.side);
  w.key("kind").string("market");
  w.key("quantity").integer(o.quantity);
  w.key("limit_price").null();
  w.key("stop_price").null();
  w.key("trail_percent").null();
  w.key("tif").string("GTC");
  w.key("filled").integer(o.filled);
  w.key("status").string(o.status_text);
  w.key("average");
  write_money(w, o.average);
  w.key("notional");
  write_money(w, o.notional);
  w.key("fee_remaining");
  write_money(w, o.fee_remaining);
  w.key("reserve_price");
  write_money(w, o.reserve_price);
  w.key("triggered").boolean(o.triggered.value_or(false));
  w.key("forced").boolean(true);
  w.key("activates");
  if (o.activates) w.integer(*o.activates);
  else w.null();
  w.key("time").integer(o.time);
  w.key("day").string(o.day_text);
  w.key("note").string("");
  w.key("lesson").string("");
  w.key("reason").string(o.reason);
  w.end_object();
}

void write_state(json::Writer& w, const State& s) {
  w.key("cursor").integer(s.cursor);
  // Only what changed goes back, so a stored value is never rewritten in a
  // different but equal spelling.
  w.key("cash");
  if (s.cash_changed) w.string(s.cash.str());
  else w.null();
  w.key("realized");
  if (s.realized_changed) w.string(s.realized.str());
  else w.null();
  w.key("positions").begin_array();
  for (const Position& p : s.positions) {
    if (!p.changed) continue;
    w.begin_array().string(p.symbol).integer(p.quantity).string(p.cost.str()).end_array();
  }
  w.end_array();
  w.key("orders").begin_array();
  for (std::size_t i = 0; i < s.reported; ++i) {
    const Order& o = s.orders[i];
    if (o.touched.empty()) continue;
    w.begin_array().integer(static_cast<std::int64_t>(i)).begin_array();
    for (const Field field : o.touched) write_field(w, o, field);
    w.end_array().end_array();
  }
  w.end_array();
  w.key("raised").begin_array();
  for (std::size_t i = s.reported; i < s.orders.size(); ++i) write_raised(w, s.orders[i]);
  w.end_array();
  w.key("fills").begin_array();
  for (const Fill& f : s.fills) {
    w.begin_object();
    w.key("order").integer(static_cast<std::int64_t>(f.order));
    w.key("quantity").integer(f.quantity);
    w.key("price").string(f.price.str());
    w.key("fee").string(f.fee.str());
    w.key("realized").string(f.realized.str());
    w.key("time").integer(f.time);
    w.end_object();
  }
  w.end_array();
  w.key("ledger").begin_array();
  for (const LedgerEntry& e : s.ledger) {
    w.begin_object();
    if (e.borrow) {
      w.key("id").string("borrow:" + std::to_string(e.cursor));
      w.key("time").integer(e.time);
      w.key("type").string("borrow_fee");
      w.key("description").string("Stock borrow fee on short positions");
      w.key("amount").string(e.amount.str());
      w.key("cash").string(e.cash.str());
    } else {
      w.key("fill").integer(static_cast<std::int64_t>(e.fill));
      w.key("amount").string(e.amount.str());
      w.key("cash").string(e.cash.str());
    }
    w.end_object();
  }
  w.end_array();
}

std::vector<std::string> symbol_names(const json::Value& request) {
  std::vector<std::string> names;
  for (const json::Value& name : request.at("symbols").as_array("symbols")) {
    names.push_back(name.as_string("symbol"));
  }
  return names;
}

std::string refused(const std::string& message) {
  json::Writer w;
  w.begin_object().key("error").string(message).end_object();
  return w.text();
}

std::string op_validate(const json::Value& request, State& s, const Market& m) {
  const json::Value& which = request.at("order");
  const std::string exclude = optional_text(request, "exclude");
  const std::string* excluded = exclude.empty() ? nullptr : &exclude;
  Order candidate;
  Order* order;
  if (which.type == json::Value::Type::Int) {
    const std::int64_t index = which.integer;
    require(index >= 0 && static_cast<std::size_t>(index) < s.orders.size(), "order index out of range");
    order = &s.orders[static_cast<std::size_t>(index)];
  } else {
    candidate = parse_order(which, m);
    order = &candidate;
  }
  std::string error;
  try {
    validate_order(s, m, *order, excluded);
  } catch (const DomainError& refusal) {
    error = refusal.what();
  }
  json::Writer w;
  w.begin_object();
  if (order->reserve_price && std::find(order->touched.begin(), order->touched.end(),
                                        Field::ReservePrice) != order->touched.end()) {
    w.key("reserve_price").string(order->reserve_price->str());
  }
  if (!error.empty()) w.key("error").string(error);
  w.end_object();
  return w.text();
}

std::string op_advance(const json::Value& request, State& s, const Market& m) {
  const std::int64_t steps = request.at("steps").as_int("steps");
  require(steps >= 0 && steps <= 100000000, "steps out of range");
  Watch watch;
  for (const json::Value& kind : request.at("watch").as_array("watch")) {
    const std::string& name = kind.as_string("watch");
    watch.any = true;
    if (name == "fill") watch.fill = true;
    if (name == "bracket") watch.bracket = true;
    if (name == "margin_call") watch.margin_call = true;
  }
  std::map<std::int64_t, std::string> scheduled;
  for (const json::Value& entry : request.at("scheduled").as_array("scheduled")) {
    const auto& pair = entry.as_array("scheduled stop");
    require(pair.size() == 2, "a scheduled stop is [bar, reason]");
    scheduled.emplace(pair[0].as_int("scheduled bar"), pair[1].as_string("scheduled reason"));
  }
  const std::optional<std::string> stop = advance(s, m, steps, scheduled, watch);
  json::Writer w;
  w.begin_object();
  write_state(w, s);
  w.key("stop");
  if (stop) w.string(*stop);
  else w.null();
  w.end_object();
  return w.text();
}

std::string op_retire(State& s) {
  retire_orphans(s);
  json::Writer w;
  w.begin_object();
  write_state(w, s);
  w.end_object();
  return w.text();
}

std::string op_reservations(const json::Value& request, const State& s) {
  const std::string exclude = optional_text(request, "exclude");
  const Reserved reserved = reservations(s, exclude.empty() ? nullptr : &exclude);
  json::Writer w;
  w.begin_object().key("cash").string(reserved.cash.str()).key("shares").begin_array();
  for (const auto& [symbol, count] : reserved.shares) w.begin_array().string(symbol).integer(count).end_array();
  w.end_array().end_object();
  return w.text();
}

// The account snapshot's figures: what is reserved, what is free, what the
// account is worth and carrying, and what each position is worth.
std::string op_account(const State& s, const Market& m) {
  const Reserved reserved = reservations(s, nullptr);
  std::vector<std::pair<std::string, std::int64_t>> covering;
  for (const Order& o : s.orders) {
    if (!o.buy || !is_open(o.status)) continue;
    auto found = std::find_if(covering.begin(), covering.end(),
                              [&](const auto& entry) { return entry.first == o.symbol; });
    if (found == covering.end()) covering.emplace_back(o.symbol, o.quantity - o.filled);
    else found->second += o.quantity - o.filled;
  }
  auto covering_of = [&](const std::string& symbol) -> std::int64_t {
    for (const auto& [name, count] : covering) {
      if (name == symbol) return count;
    }
    return 0;
  };
  Dec equity = s.cash;
  Dec gross = kZero;
  json::Writer w;
  w.begin_object();
  w.key("positions").begin_array();
  for (const Position& p : s.positions) {
    if (!p.quantity) continue;
    const int column = m.column(p.symbol);
    if (column < 0) throw DomainError("This stock is unavailable in this run.");
    const Dec mark = m.price(column, 3, s.cursor);
    const Dec value = mark * Dec::of(p.quantity);
    equity = equity + value;
    gross = gross + abs(value);
    const std::int64_t free_shares = std::max<std::int64_t>(0, p.quantity) - reserved.shares_of(p.symbol);
    w.begin_object();
    w.key("symbol").string(p.symbol);
    w.key("mark").string(money(mark));
    w.key("market_value").string(money(value));
    w.key("average").string(money(p.cost / Dec::of(p.quantity)));
    w.key("unrealized").string(money(value - p.cost));
    w.key("available").integer(free_shares);
    w.key("short").boolean(p.quantity < 0);
    w.key("closable").integer(p.quantity > 0 ? free_shares
                                             : std::max<std::int64_t>(0, -p.quantity - covering_of(p.symbol)));
    w.end_object();
  }
  w.end_array();
  w.key("reserved").string(money(reserved.cash));
  w.key("available").string(money(s.cash - reserved.cash));
  w.key("equity").string(money(equity));
  w.key("gross_exposure").string(money(gross));
  w.key("buying_power").string(money(max_of(kZero, buying_power(s, marks(m, s.cursor)) - reserved.cash)));
  w.end_object();
  return w.text();
}

// An exit that cannot be right is refused before it is accepted.
std::string op_bracket(const json::Value& request) {
  if (request.at("side").as_string("side") != "buy") {
    return refused(
        "Attached exits are available on buy entries. A short entry cannot carry them yet; "
        "place its stop as a separate order.");
  }
  const auto take_profit = optional_decimal(request, "take_profit");
  const auto stop_loss = optional_decimal(request, "stop_loss");
  const auto stop_loss_trail = optional_decimal(request, "stop_loss_trail");
  if (stop_loss && stop_loss_trail) return refused("A stop leg takes either a fixed price or a trail, not both.");
  const auto limit_price = optional_decimal(request, "limit_price");
  const auto stop_price = optional_decimal(request, "stop_price");
  const Dec reference = limit_price ? *limit_price
                        : stop_price ? *stop_price
                                     : Dec::parse(request.at("mark").as_string("mark"));
  if (take_profit && *take_profit <= reference) return refused("A take-profit has to sit above the entry it protects.");
  if (stop_loss && *stop_loss >= reference) return refused("A stop-loss has to sit below the entry it protects.");
  return "{}";
}

// A new trailing stop starts from where the market is now.
std::string op_trailing(const json::Value& request) {
  const Dec close = Dec::parse(request.at("close").as_string("close"));
  const Dec percent = Dec::parse(request.at("trail_percent").as_string("trail_percent"));
  json::Writer w;
  w.begin_object();
  w.key("trail_anchor").string(money(close));
  w.key("stop_price").string(money(close * (kOne - percent / kHundred)));
  w.end_object();
  return w.text();
}

}  // namespace

std::string handle(std::string_view text, const Bars* bars, std::int32_t count) {
  const json::Value request = json::parse(text);
  const std::string& op = request.at("op").as_string("op");
  if (op == "bracket") return op_bracket(request);
  if (op == "trailing") return op_trailing(request);
  const Market market(bars, count, symbol_names(request));
  State state = parse_state(request, market);
  if (op == "reservations") return op_reservations(request, state);
  if (op == "retire") return op_retire(state);
  try {
    if (op == "validate") return op_validate(request, state, market);
    if (op == "advance") return op_advance(request, state, market);
    if (op == "account") return op_account(state, market);
  } catch (const DomainError& refusal) {
    return refused(refusal.what());
  }
  fail("unknown engine operation '" + op + "'");
}

}  // namespace quanta::engine
