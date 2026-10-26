#include "json.hpp"

#include <cstdio>

#include "common.hpp"

namespace quanta::json {

namespace {

constexpr int kMaxDepth = 64;

class Parser {
 public:
  explicit Parser(std::string_view text) : text_(text) {}

  Value document() {
    Value out = value(0);
    skip_space();
    require(position_ == text_.size(), "unexpected text after the JSON document");
    return out;
  }

 private:
  std::string_view text_;
  std::size_t position_ = 0;

  void skip_space() {
    while (position_ < text_.size()) {
      const char c = text_[position_];
      if (c != ' ' && c != '\n' && c != '\r' && c != '\t') break;
      ++position_;
    }
  }

  char peek() {
    skip_space();
    require(position_ < text_.size(), "unexpected end of JSON");
    return text_[position_];
  }

  void expect(std::string_view word) {
    require(text_.substr(position_, word.size()) == word, "malformed JSON literal");
    position_ += word.size();
  }

  Value value(int depth) {
    require(depth < kMaxDepth, "JSON nested too deeply");
    const char c = peek();
    Value out;
    if (c == '{') {
      out.type = Value::Type::Object;
      ++position_;
      if (peek() == '}') {
        ++position_;
        return out;
      }
      for (;;) {
        require(peek() == '"', "JSON object keys must be strings");
        std::string name = string();
        require(peek() == ':', "missing ':' in JSON object");
        ++position_;
        out.members.emplace_back(std::move(name), value(depth + 1));
        const char next = peek();
        ++position_;
        if (next == '}') return out;
        require(next == ',', "missing ',' in JSON object");
      }
    }
    if (c == '[') {
      out.type = Value::Type::Array;
      ++position_;
      if (peek() == ']') {
        ++position_;
        return out;
      }
      for (;;) {
        out.items.push_back(value(depth + 1));
        const char next = peek();
        ++position_;
        if (next == ']') return out;
        require(next == ',', "missing ',' in JSON array");
      }
    }
    if (c == '"') {
      out.type = Value::Type::String;
      out.text = string();
      return out;
    }
    if (c == 't') {
      expect("true");
      out.type = Value::Type::Bool;
      out.boolean = true;
      return out;
    }
    if (c == 'f') {
      expect("false");
      out.type = Value::Type::Bool;
      return out;
    }
    if (c == 'n') {
      expect("null");
      return out;
    }
    out.type = Value::Type::Int;
    out.integer = integer();
    return out;
  }

  std::int64_t integer() {
    bool negative = false;
    if (text_[position_] == '-') {
      negative = true;
      ++position_;
    }
    require(position_ < text_.size() && text_[position_] >= '0' && text_[position_] <= '9',
            "malformed JSON number");
    std::int64_t magnitude = 0;
    while (position_ < text_.size() && text_[position_] >= '0' && text_[position_] <= '9') {
      magnitude = checked_add(checked_mul(magnitude, 10), text_[position_] - '0');
      ++position_;
    }
    if (position_ < text_.size()) {
      const char c = text_[position_];
      require(c != '.' && c != 'e' && c != 'E',
              "decimals travel as strings; a JSON float is not accepted");
    }
    return negative ? -magnitude : magnitude;
  }

  unsigned hex4() {
    require(position_ + 4 <= text_.size(), "truncated \\u escape");
    unsigned out = 0;
    for (int i = 0; i < 4; ++i) {
      const char c = text_[position_++];
      out <<= 4;
      if (c >= '0' && c <= '9') out |= static_cast<unsigned>(c - '0');
      else if (c >= 'a' && c <= 'f') out |= static_cast<unsigned>(c - 'a' + 10);
      else if (c >= 'A' && c <= 'F') out |= static_cast<unsigned>(c - 'A' + 10);
      else fail("malformed \\u escape");
    }
    return out;
  }

  static void append_utf8(std::string& out, unsigned code) {
    if (code < 0x80) {
      out += static_cast<char>(code);
    } else if (code < 0x800) {
      out += static_cast<char>(0xC0 | (code >> 6));
      out += static_cast<char>(0x80 | (code & 0x3F));
    } else if (code < 0x10000) {
      out += static_cast<char>(0xE0 | (code >> 12));
      out += static_cast<char>(0x80 | ((code >> 6) & 0x3F));
      out += static_cast<char>(0x80 | (code & 0x3F));
    } else {
      out += static_cast<char>(0xF0 | (code >> 18));
      out += static_cast<char>(0x80 | ((code >> 12) & 0x3F));
      out += static_cast<char>(0x80 | ((code >> 6) & 0x3F));
      out += static_cast<char>(0x80 | (code & 0x3F));
    }
  }

  std::string string() {
    ++position_;  // opening quote
    std::string out;
    for (;;) {
      require(position_ < text_.size(), "unterminated JSON string");
      const char c = text_[position_++];
      if (c == '"') return out;
      if (static_cast<unsigned char>(c) < 0x20) fail("control character in JSON string");
      if (c != '\\') {
        out += c;
        continue;
      }
      require(position_ < text_.size(), "unterminated JSON escape");
      const char e = text_[position_++];
      switch (e) {
        case '"': out += '"'; break;
        case '\\': out += '\\'; break;
        case '/': out += '/'; break;
        case 'b': out += '\b'; break;
        case 'f': out += '\f'; break;
        case 'n': out += '\n'; break;
        case 'r': out += '\r'; break;
        case 't': out += '\t'; break;
        case 'u': {
          unsigned code = hex4();
          if (code >= 0xD800 && code <= 0xDBFF) {
            require(text_.substr(position_, 2) == "\\u", "unpaired surrogate in JSON string");
            position_ += 2;
            const unsigned low = hex4();
            require(low >= 0xDC00 && low <= 0xDFFF, "unpaired surrogate in JSON string");
            code = 0x10000 + ((code - 0xD800) << 10) + (low - 0xDC00);
          } else {
            require(code < 0xDC00 || code > 0xDFFF, "unpaired surrogate in JSON string");
          }
          append_utf8(out, code);
          break;
        }
        default:
          fail("unknown escape in JSON string");
      }
    }
  }
};

std::string field(std::string_view what) { return std::string(what); }

}  // namespace

const Value* Value::find(std::string_view key) const {
  for (const auto& member : members) {
    if (member.first == key) return &member.second;
  }
  return nullptr;
}

const Value& Value::at(std::string_view key) const {
  require(type == Type::Object, "expected a JSON object");
  const Value* found = find(key);
  if (!found) fail("missing field '" + field(key) + "'");
  return *found;
}

std::int64_t Value::as_int(std::string_view what) const {
  if (type != Type::Int) fail("'" + field(what) + "' must be an integer");
  return integer;
}

bool Value::as_bool(std::string_view what) const {
  if (type != Type::Bool) fail("'" + field(what) + "' must be true or false");
  return boolean;
}

const std::string& Value::as_string(std::string_view what) const {
  if (type != Type::String) fail("'" + field(what) + "' must be a string");
  return text;
}

const std::vector<Value>& Value::as_array(std::string_view what) const {
  if (type != Type::Array) fail("'" + field(what) + "' must be an array");
  return items;
}

Value parse(std::string_view text) { return Parser(text).document(); }

void Writer::separate() {
  if (after_key_) {
    after_key_ = false;
    return;
  }
  if (!first_.empty()) {
    if (!first_.back()) out_ += ',';
    first_.back() = false;
  }
}

Writer& Writer::begin_object() {
  separate();
  out_ += '{';
  first_.push_back(true);
  return *this;
}

Writer& Writer::end_object() {
  out_ += '}';
  first_.pop_back();
  return *this;
}

Writer& Writer::begin_array() {
  separate();
  out_ += '[';
  first_.push_back(true);
  return *this;
}

Writer& Writer::end_array() {
  out_ += ']';
  first_.pop_back();
  return *this;
}

Writer& Writer::key(std::string_view name) {
  separate();
  quote(name);
  out_ += ':';
  after_key_ = true;
  return *this;
}

Writer& Writer::string(std::string_view value) {
  separate();
  quote(value);
  return *this;
}

void Writer::quote(std::string_view value) {
  out_ += '"';
  for (const char c : value) {
    const auto u = static_cast<unsigned char>(c);
    if (c == '"') out_ += "\\\"";
    else if (c == '\\') out_ += "\\\\";
    else if (u < 0x20) {
      char buffer[8];
      std::snprintf(buffer, sizeof buffer, "\\u%04x", u);
      out_ += buffer;
    } else {
      out_ += c;  // UTF-8 bytes pass through unchanged
    }
  }
  out_ += '"';
}

Writer& Writer::integer(std::int64_t value) {
  separate();
  out_ += std::to_string(value);
  return *this;
}

Writer& Writer::boolean(bool value) {
  separate();
  out_ += value ? "true" : "false";
  return *this;
}

Writer& Writer::null() {
  separate();
  out_ += "null";
  return *this;
}

}  // namespace quanta::json
