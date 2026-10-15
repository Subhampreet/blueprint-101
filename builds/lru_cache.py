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
