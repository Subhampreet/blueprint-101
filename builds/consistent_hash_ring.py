"""Consistent hash ring with virtual nodes and replica selection."""

import bisect
import hashlib
from collections import Counter


def _hash(s: str) -> int:
    return int.from_bytes(hashlib.md5(s.encode()).digest()[:8], "big")


class HashRing:
    def __init__(self, nodes=(), vnodes: int = 160):
        self.vnodes = vnodes
        self._keys = []          # sorted vnode positions
        self._owner = {}         # position -> physical node
        for n in nodes:
            self.add(n)

    def add(self, node: str, weight: int = 1):
        for i in range(self.vnodes * weight):
            h = _hash(f"{node}#{i}")
            if h in self._owner:
                continue                       # astronomically rare collision
            bisect.insort(self._keys, h)
            self._owner[h] = node

    def remove(self, node: str):
        dead = [h for h, n in self._owner.items() if n == node]
        for h in dead:
            del self._owner[h]
            self._keys.pop(bisect.bisect_left(self._keys, h))

    def get(self, key: str) -> str:
        if not self._keys:
            raise LookupError("ring is empty")
        i = bisect.bisect(self._keys, _hash(key)) % len(self._keys)   # first vnode clockwise
        return self._owner[self._keys[i]]

    def preference_list(self, key: str, replicas: int):
        """Owner plus the next distinct physical nodes clockwise (Dynamo style)."""
        out, i = [], bisect.bisect(self._keys, _hash(key))
        distinct = len(set(self._owner.values()))
        while len(out) < min(replicas, distinct):
            node = self._owner[self._keys[i % len(self._keys)]]
            if node not in out:
                out.append(node)
            i += 1
        return out


if __name__ == "__main__":
    keys = [f"user:{i}" for i in range(100_000)]
    ring = HashRing([f"node{i}" for i in range(10)])
    before = {k: ring.get(k) for k in keys}

    load = Counter(before.values())
    spread = max(load.values()) / min(load.values())
    assert spread < 1.5, spread                       # vnodes keep load fairly even

    ring.add("node10")
    moved = sum(before[k] != ring.get(k) for k in keys)
    assert moved / len(keys) < 0.15, moved            # ~1/11 of keys move, not ~90%

    naive_moved = sum(hash(k) % 10 != hash(k) % 11 for k in keys)
    print(f"consistent hashing moved {moved / len(keys):.1%} of keys; modulo hashing would move "
          f"{naive_moved / len(keys):.1%}")

    pl = ring.preference_list("user:42", 3)
    assert len(set(pl)) == 3
    print("consistent_hash_ring: all checks passed")
