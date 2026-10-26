CXX ?= c++
CXXFLAGS ?= -O2 -g
# The numeric flags are part of the parity contract, not tuning: fused
# multiply-add and fast-math reassociation would change results in the last
# place, and the generated market is only identical if every operation rounds
# exactly as numpy and CPython round it.
WARN = -std=c++17 -Wall -Wextra -Werror -pedantic
NUMERIC = -ffp-contract=off -fno-fast-math
BASE = $(WARN) $(NUMERIC) -pthread

BUILD = build
UNAME := $(shell uname -s)
ifeq ($(UNAME),Darwin)
  LIBRARY = $(BUILD)/libquanta_sim.dylib
  SHARED = -dynamiclib -install_name @rpath/libquanta_sim.dylib
else
  LIBRARY = $(BUILD)/libquanta_sim.so
  SHARED = -shared -Wl,-soname,libquanta_sim.so
endif

SOURCES = src/analytics.cpp src/calendar.cpp src/capi.cpp src/decimal.cpp src/engine.cpp \
          src/json.cpp src/libm.cpp src/market.cpp src/numeric.cpp src/rng.cpp
HEADERS = $(wildcard src/*.hpp) include/quanta_sim.h
TESTS = tests/test_main.cpp

.PHONY: all test sanitize replay bench clean

all: $(LIBRARY)

$(LIBRARY): $(SOURCES) $(HEADERS) | $(BUILD)
	$(CXX) $(BASE) $(CXXFLAGS) -fPIC $(SHARED) $(SOURCES) -o $@

$(BUILD)/quanta-sim-test: $(TESTS) $(SOURCES) $(HEADERS) | $(BUILD)
	$(CXX) $(BASE) $(CXXFLAGS) $(TESTS) $(SOURCES) -o $@

test: $(BUILD)/quanta-sim-test
	./$(BUILD)/quanta-sim-test

# AddressSanitizer and UndefinedBehaviorSanitizer over the same tests. Needs a
# compiler that ships both runtimes; the ordinary build does not.
sanitize: $(TESTS) $(SOURCES) $(HEADERS) | $(BUILD)
	$(CXX) $(BASE) -O1 -g -fno-omit-frame-pointer -fsanitize=address,undefined \
	  -fno-sanitize-recover=all $(TESTS) $(SOURCES) -o $(BUILD)/quanta-sim-sanitize
	./$(BUILD)/quanta-sim-sanitize

# Replays every engine call a Python test run recorded (QUANTA_ENGINE_CORPUS)
# through the sanitizer build, requiring byte-identical responses.
replay: tests/replay.cpp $(SOURCES) $(HEADERS) | $(BUILD)
	@test -n "$(CORPUS)" || { echo "usage: make replay CORPUS=path/to/corpus"; exit 2; }
	$(CXX) $(BASE) -O1 -g -fno-omit-frame-pointer -fsanitize=address,undefined \
	  -fno-sanitize-recover=all tests/replay.cpp $(SOURCES) -o $(BUILD)/quanta-sim-replay
	./$(BUILD)/quanta-sim-replay $(CORPUS)

$(BUILD)/quanta-sim-bench: bench/bench.cpp $(SOURCES) $(HEADERS) | $(BUILD)
	$(CXX) $(BASE) -O2 bench/bench.cpp $(SOURCES) -o $@

bench: $(BUILD)/quanta-sim-bench
	./$(BUILD)/quanta-sim-bench

$(BUILD):
	mkdir -p $(BUILD)

clean:
	rm -rf $(BUILD)
