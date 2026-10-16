---
title: "Build: Load Balancer Strategies and Simulation"
summary: Round robin, smooth weighted round robin, least connections, power of two choices and IP hash, plus a discrete-event simulation that shows why load-aware algorithms win when one backend is slow.
tags: [build, load-balancer, simulation, algorithms]
level: intermediate
time: 20 min
lab: load-balancer
---

# Build: Load Balancer Strategies and Simulation

> **TL;DR**
> - Five balancing strategies plus a queueing simulation with one slow server.
> - Round robin lets the slow server's queue explode; least connections and power of two choices route around it.
> - Smooth weighted round robin interleaves picks instead of sending bursts.

Theory: [Load Balancing](../02-building-blocks/02-load-balancing.md).

## Code

Runnable file: [`builds/load_balancer.py`](../../builds/load_balancer.py).

<!-- code: builds/load_balancer.py -->
```python
"""Load balancing strategies plus a tiny discrete-event simulation comparing them."""

import heapq
import itertools
import random
import zlib


class Backend:
    def __init__(self, name: str, speed: float = 1.0, weight: int = 1):
        self.name, self.speed, self.weight = name, speed, weight
        self.active = 0          # in-flight requests
        self.healthy = True


class RoundRobin:
    def __init__(self, backends):
        self.backends, self.it = backends, itertools.cycle(range(len(backends)))

    def pick(self, _key=None):
        for _ in range(len(self.backends)):
            b = self.backends[next(self.it)]
            if b.healthy:
                return b
        raise RuntimeError("no healthy backends")


class WeightedRoundRobin:
    """Smooth weighted round robin (the NGINX algorithm)."""

    def __init__(self, backends):
        self.backends, self.current = backends, {b.name: 0 for b in backends}

    def pick(self, _key=None):
        live = [b for b in self.backends if b.healthy]
        total = sum(b.weight for b in live)
        for b in live:
            self.current[b.name] += b.weight
        best = max(live, key=lambda b: self.current[b.name])
        self.current[best.name] -= total
        return best


class LeastConnections:
    def __init__(self, backends):
        self.backends = backends

    def pick(self, _key=None):
        return min((b for b in self.backends if b.healthy), key=lambda b: b.active / b.weight)


class PowerOfTwoChoices:
    def __init__(self, backends, rng=None):
        self.backends, self.rng = backends, rng or random.Random(7)

    def pick(self, _key=None):
        live = [b for b in self.backends if b.healthy]
        a, b = self.rng.sample(live, 2) if len(live) > 1 else (live[0], live[0])
        return a if a.active <= b.active else b


class IPHash:
    def __init__(self, backends):
        self.backends = backends

    def pick(self, key):
        live = [b for b in self.backends if b.healthy]
        return live[zlib.crc32(key.encode()) % len(live)]


def simulate(strategy_cls, n_requests=20_000, arrival_rate=50.0, seed=1):
    """Poisson arrivals; each backend is a FIFO queue with exponential service times
    (fast backends serve 25 req/s, the slow one 12.5 req/s). Returns p99 latency in seconds."""
    rng = random.Random(seed)
    backends = [Backend("fast-%d" % i, speed=1.0) for i in range(4)] + [Backend("slow", speed=0.5)]
    lb = strategy_cls(backends)
    free_at = {b.name: 0.0 for b in backends}
    events, t, latencies = [], 0.0, []
    for i in range(n_requests):
        t += rng.expovariate(arrival_rate)
        while events and events[0][0] <= t:              # complete finished requests
            _, _, done = heapq.heappop(events)
            done.active -= 1
        b = lb.pick("client-%d" % rng.randrange(1000))
        b.active += 1
        start = max(t, free_at[b.name])                  # wait behind queued work
        finish = start + rng.expovariate(25.0 * b.speed)
        free_at[b.name] = finish
        heapq.heappush(events, (finish, i, b))
        latencies.append(finish - t)
    latencies.sort()
    return latencies[int(len(latencies) * 0.99)]


if __name__ == "__main__":
    bs = [Backend("a", weight=5), Backend("b", weight=1), Backend("c", weight=1)]
    wrr = WeightedRoundRobin(bs)
    picks = [wrr.pick().name for _ in range(7)]
    assert picks.count("a") == 5 and picks[:3] != ["a", "a", "a"]    # smooth, not bursty

    for cls in (RoundRobin, IPHash, LeastConnections, PowerOfTwoChoices):
        print(f"{cls.__name__:>18}: p99 = {simulate(cls) * 1000:7.1f} ms")
    assert simulate(LeastConnections) < simulate(RoundRobin)
    print("load_balancer: all checks passed")
```
<!-- /code -->

## Output

```text
        RoundRobin: p99 =   949.0 ms
            IPHash: p99 =   678.5 ms
  LeastConnections: p99 =   217.8 ms
 PowerOfTwoChoices: p99 =   313.4 ms
```

Five backends, one of them half as fast. Round robin keeps sending the slow backend its full share, so a queue builds there and the tail explodes. Least connections and power of two choices notice the queue and route around it.

## Notes

- **Smooth weighted round robin** (used by NGINX) interleaves picks (`a a b a c a a` rather than `a a a a a b c`), avoiding micro-bursts to heavy backends.
- **Power of two choices** gets most of the benefit of least connections with no global view: perfect for many independent LB nodes.
- The simulation models each backend as a FIFO queue with exponential service times (an M/M/1 queue per backend).

## Interview questions

<details>
<summary>Why does power of two choices work almost as well as least connections?</summary>

Picking the less loaded of two random backends exponentially reduces the maximum load compared with a single random choice (from about log n / log log n to log log n in balls-into-bins analysis). It needs no shared global state, so each of many load balancers can make good decisions independently using only local or slightly stale load information.

</details>

## Related

- [Load Balancing](../02-building-blocks/02-load-balancing.md)
- [Scalability and Little's Law](../01-fundamentals/03-scalability-performance.md)
