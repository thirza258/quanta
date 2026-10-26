// A strict JSON reader and writer for the engine's request/response protocol.
//
// The protocol only carries integers, strings, booleans, null, arrays and
// objects: every decimal travels as a string, so no binary float ever stands in
// for an amount of money. A float in a request is rejected.
#pragma once

#include <cstdint>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

namespace quanta::json {

struct Value {
  enum class Type { Null, Bool, Int, String, Array, Object };
  Type type = Type::Null;
  bool boolean = false;
  std::int64_t integer = 0;
  std::string text;
  std::vector<Value> items;
  std::vector<std::pair<std::string, Value>> members;  // in document order

  bool is_null() const { return type == Type::Null; }
  const Value* find(std::string_view key) const;  // nullptr when absent

  // Typed access; throws quanta::Error naming the field on a type mismatch.
  const Value& at(std::string_view key) const;
  std::int64_t as_int(std::string_view what) const;
  bool as_bool(std::string_view what) const;
  const std::string& as_string(std::string_view what) const;
  const std::vector<Value>& as_array(std::string_view what) const;
};

Value parse(std::string_view text);

// Appends JSON text to a buffer. Keys and values are written in call order.
class Writer {
 public:
  Writer& begin_object();
  Writer& end_object();
  Writer& begin_array();
  Writer& end_array();
  Writer& key(std::string_view name);
  Writer& string(std::string_view value);
  Writer& integer(std::int64_t value);
  Writer& boolean(bool value);
  Writer& null();
  const std::string& text() const { return out_; }

 private:
  void separate();
  void quote(std::string_view value);
  std::string out_;
  std::vector<bool> first_;  // one flag per open container
  bool after_key_ = false;
};

}  // namespace quanta::json
