"""Circuit breaker with a rolling window of outcomes, failure-rate threshold and half-open probes."""

import time
from collections import deque


class CircuitOpenError(Exception):
    pass


class CircuitBreaker:
    CLOSED, OPEN, HALF_OPEN = "closed", "open", "half_open"

    def __init__(self, window=20, min_calls=10, failure_rate=0.5, cooldown=30.0,
                 half_open_probes=3, clock=time.monotonic):
        self.window, self.min_calls, self.failure_rate = window, min_calls, failure_rate
        self.cooldown, self.half_open_probes, self.clock = cooldown, half_open_probes, clock
        self.state, self.opened_at = self.CLOSED, 0.0
        self.outcomes = deque(maxlen=window)   # True = success
        self.probe_successes = 0

    def _transition(self, state):
        self.state = state
        if state == self.OPEN:
            self.opened_at = self.clock()
        if state in (self.CLOSED, self.HALF_OPEN):
            self.outcomes.clear()
            self.probe_successes = 0

    def call(self, fn, *args, fallback=None, **kwargs):
        if self.state == self.OPEN:
            if self.clock() - self.opened_at >= self.cooldown:
                self._transition(self.HALF_OPEN)
            else:
                if fallback is not None:
                    return fallback()
                raise CircuitOpenError("circuit open, failing fast")
        try:
            result = fn(*args, **kwargs)
        except Exception:
            self._record(False)
            if fallback is not None:
                return fallback()
            raise
        self._record(True)
        return result

    def _record(self, ok: bool):
        if self.state == self.HALF_OPEN:
            if not ok:
                self._transition(self.OPEN)          # one failed probe reopens
                return
            self.probe_successes += 1
            if self.probe_successes >= self.half_open_probes:
                self._transition(self.CLOSED)
            return
        self.outcomes.append(ok)
        if len(self.outcomes) >= self.min_calls:
            failures = self.outcomes.count(False) / len(self.outcomes)
            if failures >= self.failure_rate:
                self._transition(self.OPEN)


if __name__ == "__main__":
    now = [0.0]
    cb = CircuitBreaker(window=10, min_calls=5, failure_rate=0.5, cooldown=30, half_open_probes=2,
                        clock=lambda: now[0])
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        raise ConnectionError("downstream timeout")

    for _ in range(5):
        cb.call(flaky, fallback=lambda: "cached")
    assert cb.state == CircuitBreaker.OPEN
    before = calls["n"]
    assert cb.call(flaky, fallback=lambda: "cached") == "cached"
    assert calls["n"] == before                     # open: downstream not called at all

    now[0] += 31                                    # cooldown elapsed: half-open probes
    assert cb.call(lambda: "ok") == "ok" and cb.state == CircuitBreaker.HALF_OPEN
    assert cb.call(lambda: "ok") == "ok" and cb.state == CircuitBreaker.CLOSED
    print("circuit_breaker: all checks passed")
