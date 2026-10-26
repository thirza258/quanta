// Replays an engine call corpus recorded from the Python test suite (see
// backend/tests/engine_corpus.py) and requires every response to be
// byte-identical. `make replay CORPUS=path` builds it with AddressSanitizer and
// UndefinedBehaviorSanitizer, so the sanitizers run over every request the
// differential tests and the API tests made, not only the fixtures in
// test_main.cpp.
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <iterator>
#include <string>
#include <unordered_map>
#include <vector>

#include "../src/common.hpp"
#include "../src/engine.hpp"

namespace {

struct Column {
  std::int64_t length = 0;
  std::vector<std::int32_t> cents[4];
  std::vector<double> values[4];
  std::vector<std::int32_t> volume_int;
  std::vector<double> volume_float;
  std::vector<std::int64_t> time;
  std::vector<std::int32_t> day;
};

struct Market {
  std::vector<Column> columns;
  std::vector<quanta::engine::Bars> bars;
};

class Reader {
 public:
  explicit Reader(std::string data) : data_(std::move(data)) {}
  bool done() const { return position_ >= data_.size(); }

  template <class T>
  T value() {
    T out;
    take(&out, sizeof out);
    return out;
  }

  template <class T>
  void array(std::vector<T>& out, std::int64_t count) {
    quanta::require(count >= 0 && count < (1LL << 34), "corpus array length out of range");
    out.resize(static_cast<std::size_t>(count));
    take(out.data(), out.size() * sizeof(T));
  }

  std::string bytes(std::uint64_t count) {
    quanta::require(count <= data_.size() - position_, "corpus truncated");
    std::string out = data_.substr(position_, count);
    position_ += count;
    return out;
  }

 private:
  void take(void* out, std::size_t count) {
    quanta::require(count <= data_.size() - position_, "corpus truncated");
    std::memcpy(out, data_.data() + position_, count);
    position_ += count;
  }

  std::string data_;
  std::size_t position_ = 0;
};

Market read_market(Reader& in) {
  Market market;
  const auto symbols = in.value<std::uint32_t>();
  market.columns.resize(symbols);
  for (auto& column : market.columns) {
    in.bytes(in.value<std::uint32_t>());  // the symbol's name; requests carry their own
    column.length = in.value<std::int64_t>();
    const auto price_kind = in.value<std::uint8_t>();
    const auto volume_kind = in.value<std::uint8_t>();
    for (int k = 0; k < 4; ++k) {
      if (price_kind == 0) in.array(column.cents[k], column.length);
      else in.array(column.values[k], column.length);
    }
    if (volume_kind == 0) in.array(column.volume_int, column.length);
    else in.array(column.volume_float, column.length);
    in.array(column.time, column.length);
    in.array(column.day, column.length);
  }
  for (const auto& column : market.columns) {
    quanta::engine::Bars bars{};
    bars.length = column.length;
    for (int k = 0; k < 4; ++k) {
      bars.cents[k] = column.cents[k].empty() ? nullptr : column.cents[k].data();
      bars.values[k] = column.values[k].empty() ? nullptr : column.values[k].data();
    }
    bars.volume_int = column.volume_int.empty() ? nullptr : column.volume_int.data();
    bars.volume_float = column.volume_float.empty() ? nullptr : column.volume_float.data();
    bars.time = column.time.data();
    bars.day = column.day.data();
    market.bars.push_back(bars);
  }
  return market;
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    std::fprintf(stderr, "usage: %s corpus-file\n", argv[0]);
    return 2;
  }
  std::ifstream file(argv[1], std::ios::binary);
  if (!file) {
    std::fprintf(stderr, "cannot open %s\n", argv[1]);
    return 2;
  }
  Reader in{std::string(std::istreambuf_iterator<char>(file), std::istreambuf_iterator<char>())};
  if (in.bytes(8) != "QSCORP01") {
    std::fprintf(stderr, "%s is not an engine corpus\n", argv[1]);
    return 2;
  }
  std::unordered_map<std::uint32_t, Market> markets;
  std::size_t calls = 0, mismatches = 0;
  while (!in.done()) {
    const auto kind = in.value<char>();
    if (kind == 'M') {
      const auto id = in.value<std::uint32_t>();
      markets[id] = read_market(in);
      continue;
    }
    quanta::require(kind == 'C', "unknown corpus record");
    const auto id = in.value<std::uint32_t>();
    const std::string request = in.bytes(in.value<std::uint64_t>());
    const std::string expected = in.bytes(in.value<std::uint64_t>());
    const Market* market = nullptr;
    if (id != 0xFFFFFFFFu) {
      const auto found = markets.find(id);
      quanta::require(found != markets.end(), "call names an unrecorded market");
      market = &found->second;
    }
    const std::string actual = quanta::engine::handle(
        request, market ? market->bars.data() : nullptr,
        market ? static_cast<std::int32_t>(market->bars.size()) : 0);
    ++calls;
    if (actual != expected) {
      if (++mismatches <= 5) {
        std::printf("call %zu differs\n  expected %.300s\n  actual   %.300s\n", calls, expected.c_str(),
                    actual.c_str());
      }
    }
  }
  std::printf("%zu calls over %zu markets replayed, %zu mismatched\n", calls, markets.size(), mismatches);
  return mismatches == 0 ? 0 : 1;
}
