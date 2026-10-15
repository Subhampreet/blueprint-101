"""Bloom filter sized from expected items and target false positive rate."""

import hashlib
import math


class BloomFilter:
    def __init__(self, expected_items: int, fp_rate: float = 0.01):
        self.m = max(8, int(-expected_items * math.log(fp_rate) / (math.log(2) ** 2)))   # bits
        self.k = max(1, round(self.m / expected_items * math.log(2)))                    # hashes
        self.bits = bytearray((self.m + 7) // 8)
        self.count = 0

    def _positions(self, item: str):
        # double hashing: h_i = h1 + i * h2, standard trick to derive k hashes from 2
        d = hashlib.sha256(item.encode()).digest()
        h1, h2 = int.from_bytes(d[:8], "big"), int.from_bytes(d[8:16], "big") | 1
        return ((h1 + i * h2) % self.m for i in range(self.k))

    def add(self, item: str):
        for p in self._positions(item):
            self.bits[p >> 3] |= 1 << (p & 7)
        self.count += 1

    def __contains__(self, item: str) -> bool:
        return all(self.bits[p >> 3] & (1 << (p & 7)) for p in self._positions(item))

    def estimated_fp_rate(self) -> float:
        return (1 - math.exp(-self.k * self.count / self.m)) ** self.k


if __name__ == "__main__":
    n = 100_000
    bf = BloomFilter(expected_items=n, fp_rate=0.01)
    for i in range(n):
        bf.add(f"url-{i}")
    assert all(f"url-{i}" in bf for i in range(n))              # no false negatives ever
    trials = 100_000
    fps = sum(f"other-{i}" in bf for i in range(trials))
    observed = fps / trials
    assert observed < 0.02, observed
    print(f"bloom_filter: m={bf.m} bits ({bf.m / 8 / 1024:.0f} KB), k={bf.k}, "
          f"observed FP={observed:.3%}, predicted={bf.estimated_fp_rate():.3%}")
