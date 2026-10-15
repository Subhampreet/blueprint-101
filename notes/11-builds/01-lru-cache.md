---
title: "Build: LRU Cache"
summary: An O(1) LRU cache with a hash map and doubly linked list, TTL support, thread safety and hit/miss stats, plus how real caches approximate LRU.
tags: [build, lru, cache, data-structures, lld]
level: core
time: 20 min
lab: cache
---

# Build: LRU Cache

Asked as an LLD/coding question ("LeetCode 146") and as the core of [distributed cache design](../09-case-studies/13-distributed-cache.md).

## Design

- **Hash map** `key -> node` gives O(1) lookup.
- **Doubly linked list** ordered by recency: head = most recently used, tail = least recently used. Moving a node to the head and removing the tail are O(1) because each node knows its neighbours.
- **Sentinel** head and tail nodes remove edge cases for empty lists.
- **TTL**: store `expires_at`; check lazily on `get` (real systems also sweep in the background).
- **Thread safety**: one lock around each operation (Redis avoids locks by being single threaded; Caffeine uses lock-free buffers and batching).

```text
head <-> [c] <-> [a] <-> [b] <-> tail
          MRU                LRU   (evict b when full)
```

## Code

Runnable file: [`builds/lru_cache.py`](../../builds/lru_cache.py) (`python3 builds/lru_cache.py` runs the checks).

<!-- code: builds/lru_cache.py -->
```python
"""LRU cache with O(1) get/put: hash map + doubly linked list, optional TTL, thread safe."""

import threading
import time


class _Node:
    __slots__ = ("key", "value", "expires_at", "prev", "next")

    def __init__(self, key=None, value=None, expires_at=None):
        self.key, self.value, self.expires_at = key, value, expires_at
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity: int, clock=time.monotonic):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity, self.clock = capacity, clock
        self.map = {}
        self.head, self.tail = _Node(), _Node()      # sentinels: head.next is most recent
        self.head.next, self.tail.prev = self.tail, self.head
        self.lock = threading.Lock()
        self.hits = self.misses = self.evictions = 0

    # -- linked list helpers -------------------------------------------------
    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node):
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    # -- public API ----------------------------------------------------------
    def get(self, key, default=None):
        with self.lock:
            node = self.map.get(key)
            if node is None:
                self.misses += 1
                return default
            if node.expires_at is not None and node.expires_at <= self.clock():
                self._unlink(node)
                del self.map[key]
                self.misses += 1
                return default
            self._unlink(node)
            self._push_front(node)                    # mark as most recently used
            self.hits += 1
            return node.value

    def put(self, key, value, ttl: float = None):
        expires_at = self.clock() + ttl if ttl is not None else None
        with self.lock:
            node = self.map.get(key)
            if node is not None:
                node.value, node.expires_at = value, expires_at
                self._unlink(node)
                self._push_front(node)
                return
            if len(self.map) >= self.capacity:
                lru = self.tail.prev                  # least recently used
                self._unlink(lru)
                del self.map[lru.key]
                self.evictions += 1
            node = _Node(key, value, expires_at)
            self.map[key] = node
            self._push_front(node)

    def delete(self, key) -> bool:
        with self.lock:
            node = self.map.pop(key, None)
            if node is None:
                return False
            self._unlink(node)
            return True

    def __len__(self):
        return len(self.map)

    def keys_mru_to_lru(self):
        out, node = [], self.head.next
        while node is not self.tail:
            out.append(node.key)
            node = node.next
        return out


if __name__ == "__main__":
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1                 # a becomes most recent
    c.put("c", 3)                          # evicts b
    assert c.get("b") is None
    assert c.keys_mru_to_lru() == ["c", "a"]

    now = [100.0]
    t = LRUCache(10, clock=lambda: now[0])
    t.put("session", "x", ttl=5)
    assert t.get("session") == "x"
    now[0] += 6
    assert t.get("session") is None        # expired
    print("lru_cache: all checks passed", {"hits": c.hits, "misses": c.misses, "evictions": c.evictions})
```
<!-- /code -->

## Complexity

| Operation | Time | Space |
|---|---|---|
| get | O(1) | |
| put (including eviction) | O(1) | |
| total | | O(capacity) |

## How production caches differ

- **Approximate LRU**: Redis samples N random keys (default 5) and evicts the least recently used among them: no linked list overhead, nearly LRU hit rates.
- **Better policies**: LFU with decay, ARC, 2Q, W-TinyLFU (Caffeine) resist scan pollution and keep frequently used items.
- **Size-aware eviction**: evict by bytes, not count.
- **Concurrency**: segmented/striped locks or lock-free read buffers.

Compare policies on real access patterns in the **Cache Simulator** lab.

## Interview questions

<details>
<summary>Why a doubly linked list instead of a singly linked list?</summary>

To unlink an arbitrary node in O(1) you need its predecessor. A doubly linked node knows both neighbours; with a singly linked list you would need to scan to find the previous node (O(n)).

</details>

<details>
<summary>How would you make this LFU instead?</summary>

Keep `key -> (value, freq)` plus a map `freq -> doubly linked list of keys` and track `min_freq`. On access, move the key from list `freq` to `freq + 1` (updating `min_freq` if the old list empties). On eviction, remove the LRU node from the `min_freq` list. All operations stay O(1).

</details>

## Related

- [Caching](../02-building-blocks/03-caching.md)
- [Distributed Cache](../09-case-studies/13-distributed-cache.md)
