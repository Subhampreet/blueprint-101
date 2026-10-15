---
title: "Build: Rate Limiters"
summary: Token bucket, fixed window, sliding log and sliding window counter implemented with an injectable clock, with tests that demonstrate the boundary burst problem.
tags: [build, rate-limiting, token-bucket, sliding-window]
level: core
time: 20 min
lab: rate-limiter
---

# Build: Rate Limiters

Four algorithms from [Rate Limiting](../02-building-blocks/08-rate-limiting.md), each a few lines. The clock is injected so tests are deterministic (a good habit for any time-based code).

## Code

Runnable file: [`builds/rate_limiters.py`](../../builds/rate_limiters.py).

<!-- code: builds/rate_limiters.py -->
```python
"""Four rate limiting algorithms with an injectable clock so they are easy to test."""

import time
from collections import defaultdict, deque


class TokenBucket:
    """Average `rate` requests/s, bursts up to `capacity`."""

    def __init__(self, rate: float, capacity: int, clock=time.monotonic):
        self.rate, self.capacity, self.clock = rate, capacity, clock
        self.state = {}                                  # key -> (tokens, last_ts)

    def allow(self, key: str, cost: float = 1.0) -> bool:
        now = self.clock()
        tokens, last = self.state.get(key, (self.capacity, now))
        tokens = min(self.capacity, tokens + (now - last) * self.rate)   # lazy refill
        allowed = tokens >= cost
        if allowed:
            tokens -= cost
        self.state[key] = (tokens, now)
        return allowed


class FixedWindow:
    """At most `limit` requests per window. Simple, but allows 2x bursts at window edges."""

    def __init__(self, limit: int, window: float, clock=time.monotonic):
        self.limit, self.window, self.clock = limit, window, clock
        self.counts = defaultdict(int)

    def allow(self, key: str) -> bool:
        bucket = (key, int(self.clock() // self.window))
        if self.counts[bucket] >= self.limit:
            return False
        self.counts[bucket] += 1
        return True


class SlidingLog:
    """Exact: keeps a timestamp per accepted request. Memory O(limit) per key."""

    def __init__(self, limit: int, window: float, clock=time.monotonic):
        self.limit, self.window, self.clock = limit, window, clock
        self.logs = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now, log = self.clock(), self.logs[key]
        while log and log[0] <= now - self.window:
            log.popleft()
        if len(log) >= self.limit:
            return False
        log.append(now)
        return True


class SlidingWindowCounter:
    """Approximates a sliding window with two fixed-window counters. O(1) memory."""

    def __init__(self, limit: int, window: float, clock=time.monotonic):
        self.limit, self.window, self.clock = limit, window, clock
        self.counts = defaultdict(int)

    def allow(self, key: str) -> bool:
        now = self.clock()
        current = int(now // self.window)
        elapsed = (now % self.window) / self.window
        estimate = self.counts[(key, current)] + self.counts[(key, current - 1)] * (1 - elapsed)
        if estimate >= self.limit:
            return False
        self.counts[(key, current)] += 1
        return True


if __name__ == "__main__":
    now = [0.0]
    clock = lambda: now[0]

    tb = TokenBucket(rate=1, capacity=3, clock=clock)
    assert [tb.allow("u") for _ in range(4)] == [True, True, True, False]   # burst of 3
    now[0] += 1.0
    assert tb.allow("u") and not tb.allow("u")                              # 1 token refilled

    now[0] = 0.0
    fw = FixedWindow(limit=5, window=60, clock=clock)
    now[0] = 59.9
    assert all(fw.allow("u") for _ in range(5))
    now[0] = 60.0
    assert all(fw.allow("u") for _ in range(5))       # boundary burst: 10 requests in 0.1 s

    now[0] = 59.9
    sl = SlidingLog(limit=5, window=60, clock=clock)
    assert all(sl.allow("u") for _ in range(5))
    now[0] = 60.0
    assert not sl.allow("u")                          # exact: no boundary burst

    now[0] = 0.0
    sw = SlidingWindowCounter(limit=10, window=60, clock=clock)
    assert sum(sw.allow("u") for _ in range(15)) == 10
    now[0] = 90.0                                     # halfway into next window: half of previous counts
    assert sum(sw.allow("u") for _ in range(10)) == 5
    print("rate_limiters: all checks passed")
```
<!-- /code -->

## What the tests show

- **Token bucket**: a burst of 3 is allowed immediately, then exactly 1 request per refilled token.
- **Fixed window**: 5 requests at 59.9 s and 5 more at 60.0 s all pass: 10 requests in 0.1 s against a "5 per minute" limit. That is the boundary burst.
- **Sliding log**: the same pattern is correctly rejected.
- **Sliding window counter**: halfway into the next window, half of the previous window's count still applies, so only 5 more requests pass.

## Making it distributed

In production the state lives in Redis and each check is one atomic Lua script (see the token bucket Lua in [Rate Limiting](../02-building-blocks/08-rate-limiting.md#distributed-rate-limiting)). Use the request's key (API key, user ID, IP) for sharding so each key's counters live on one Redis shard.

## Interview questions

<details>
<summary>Why inject the clock?</summary>

Time-dependent logic is otherwise hard to test (sleeps make tests slow and flaky). Passing a clock function lets tests move time forward deterministically, and also lets production use a monotonic clock that does not jump with NTP adjustments.

</details>

<details>
<summary>The fixed window counter keeps growing its dictionary. How do you fix memory use?</summary>

Delete or expire old buckets: only the current (and for sliding counters, the previous) window is needed. In Redis, set an `EXPIRE` of two windows on each counter key; in memory, prune buckets older than the previous window periodically.

</details>

## Related

- [Rate Limiting](../02-building-blocks/08-rate-limiting.md)
- [API Gateway](../02-building-blocks/05-proxies-api-gateway.md)
