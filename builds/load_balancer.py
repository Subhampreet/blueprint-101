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
