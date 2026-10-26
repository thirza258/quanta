// Deterministic data parallelism over independent tasks.
#pragma once

#include <algorithm>
#include <atomic>
#include <cstdint>
#include <exception>
#include <mutex>
#include <system_error>
#include <thread>
#include <vector>

namespace quanta {

// Run fn(task) for every task in [0, tasks) on the calling thread plus up to
// workers - 1 more.
//
// Tasks must read shared inputs only and write outputs no other task touches.
// Under that contract the result cannot depend on which thread ran which task or
// in what order they finished, which is exactly what the serial/parallel
// equality tests assert. The calling thread always takes part, so a worker the
// system refuses to start costs speed, never completeness. The first exception
// thrown by any task is rethrown once every started thread has joined; nothing
// is reported as finished while a worker is still writing.
template <class Fn>
void parallel_for(std::int64_t tasks, int workers, Fn&& fn) {
  if (tasks <= 0) return;
  const std::int64_t wanted = std::min<std::int64_t>(std::max(workers, 1), tasks);
  std::atomic<std::int64_t> next{0};
  std::atomic<bool> failed{false};
  std::exception_ptr error;
  std::mutex error_lock;
  auto drain = [&]() {
    for (;;) {
      if (failed.load(std::memory_order_relaxed)) return;
      const std::int64_t task = next.fetch_add(1, std::memory_order_relaxed);
      if (task >= tasks) return;
      try {
        fn(task);
      } catch (...) {
        std::lock_guard<std::mutex> guard(error_lock);
        if (!error) error = std::current_exception();
        failed.store(true, std::memory_order_relaxed);
        return;
      }
    }
  };
  std::vector<std::thread> threads;
  threads.reserve(static_cast<std::size_t>(wanted - 1));
  for (std::int64_t i = 1; i < wanted; ++i) {
    try {
      threads.emplace_back(drain);
    } catch (const std::system_error&) {
      break;  // run the remaining share on the threads that did start
    }
  }
  drain();
  for (auto& thread : threads) thread.join();
  if (error) std::rethrow_exception(error);
}

// Workers to use when the caller does not say: what the hardware reports, but
// never more than the work can use. A container limited to two CPUs may still
// report every core on the host, so callers pass an explicit count there.
inline int default_workers() {
  const unsigned reported = std::thread::hardware_concurrency();
  return reported == 0 ? 1 : static_cast<int>(std::min(reported, 8u));
}

}  // namespace quanta
