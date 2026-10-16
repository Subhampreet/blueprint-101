---
title: "Build: Bloom Filter"
summary: A Bloom filter sized from expected items and false positive rate, using double hashing to derive k hash functions, with a test that measures the real false positive rate.
tags: [build, bloom-filter, probabilistic]
level: intermediate
time: 15 min
---

# Build: Bloom Filter

> **TL;DR**
> - Size the bit array and hash count from the expected item count and target false positive rate.
> - Double hashing derives k positions from one digest; about 10 bits per item gives 1% false positives.
> - No false negatives, ever; deletes need a counting variant.

Theory: [Probabilistic Data Structures](../10-advanced/03-probabilistic-data-structures.md#bloom-filter-have-i-seen-this).

## Code

Runnable file: [`builds/bloom_filter.py`](../../builds/bloom_filter.py).

<!-- code: builds/bloom_filter.py -->
```python
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
```
<!-- /code -->

## Output

```text
bloom_filter: m=958505 bits (117 KB), k=7, observed FP=0.984%, predicted=1.004%
```

100,000 items in 117 KB with a 1% false positive rate. A Python `set` of the same strings uses several MB.

## Notes

- **Double hashing** (`h1 + i * h2`) derives k independent-enough hashes from one SHA-256 digest (Kirsch and Mitzenmacher), which is much cheaper than k separate hash functions.
- `h2 | 1` keeps the step odd so positions do not collapse.
- Sizing formulas: `m = -n ln p / (ln 2)^2`, `k = (m/n) ln 2`.
- No `remove`: clearing a bit could delete other items. Use a counting Bloom filter or a cuckoo filter if you need deletes.

## Interview questions

<details>
<summary>Where would you put a Bloom filter in a system design?</summary>

In front of an expensive lookup where most answers are "not present": LSM storage engines (skip SSTables), caches (stop cache penetration for non-existent keys), web crawlers (seen URLs), username availability pre-checks, and CDN one-hit-wonder filtering.

</details>

## Related

- [Web Crawler](../09-case-studies/14-web-crawler.md)
- [Indexes and Storage Engines](../03-data/02-indexes-storage-engines.md)
