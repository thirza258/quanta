import os
import time
from collections import deque
from threading import Lock

from fastapi import HTTPException


class RateLimiter:
    def __init__(self):
        self.records = {}
        self.lock = Lock()
        self.redis = None
        if os.getenv("REDIS_URL"):
            import redis

            self.redis = redis.Redis.from_url(os.environ["REDIS_URL"], socket_timeout=1)

    def check(self, key: str, maximum=30, seconds=60):
        now = time.time()
        if self.redis:
            # Atomic fixed-window count; fail closed on shared limiter outage.
            try:
                script = 'local n = redis.call("INCR", KEYS[1]); if n == 1 then redis.call("EXPIRE", KEYS[1], ARGV[1]) end; return n'
                n = self.redis.eval(script, 1, f"quanta:limit:{key}:{int(now // seconds)}", seconds)
                if n > maximum:
                    raise HTTPException(
                        429,
                        "Rate limit reached. Please try again shortly.",
                        headers={"Retry-After": str(seconds)},
                    )
                return
            except HTTPException:
                raise
            except Exception:
                raise HTTPException(
                    503, "Rate limiter unavailable. Please try again shortly."
                ) from None
        with self.lock:
            if len(self.records) > 10000:
                self.records = {
                    k: q for k, q in self.records.items() if q and q[-1] > now - seconds
                }
            queue = self.records.setdefault(key, deque())
            while queue and queue[0] <= now - seconds:
                queue.popleft()
            if len(queue) >= maximum:
                raise HTTPException(
                    429,
                    "Rate limit reached. Please try again shortly.",
                    headers={"Retry-After": str(seconds)},
                )
            queue.append(now)


limiter = RateLimiter()
