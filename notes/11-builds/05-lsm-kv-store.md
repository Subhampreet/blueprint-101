---
title: "Build: LSM Key-Value Store"
summary: A tiny log-structured merge tree with a write-ahead log, memtable, immutable SSTables with sparse indexes, tombstones, compaction and crash recovery.
tags: [build, lsm, storage-engine, wal, sstable, compaction]
level: advanced
time: 30 min
---

# Build: LSM Key-Value Store

The storage engine idea behind Cassandra, RocksDB, LevelDB, HBase and Bigtable, in about 150 lines. Theory: [Indexes and Storage Engines](../03-data/02-indexes-storage-engines.md).

## Components

| Component | Role in this build | In real engines |
|---|---|---|
| **WAL** | Append + fsync every write before acknowledging; replayed on startup | Group commit, checksums, segment rotation |
| **Memtable** | Python dict, sorted on flush | Skip list or balanced tree |
| **SSTable** | Immutable sorted JSON-lines file + sparse index every 16 keys | Binary blocks, compression, Bloom filter, block cache |
| **Tombstone** | Delete marker that shadows older values | Same, removed at compaction after grace period |
| **Compaction** | Merge all SSTables, newest wins, drop tombstones | Size-tiered or leveled, runs in background threads |

## Code

Runnable file: [`builds/lsm_kv_store.py`](../../builds/lsm_kv_store.py).

<!-- code: builds/lsm_kv_store.py -->
```python
"""A tiny LSM-tree key value store: WAL + memtable + immutable SSTables + compaction.

Educational: single process, string keys and values, no concurrency control.
"""

import json
import os
import tempfile

TOMBSTONE = "\u0000__deleted__"


class SSTable:
    """Immutable sorted file: one JSON line per (key, value); sparse in-memory index."""

    def __init__(self, path: str, index_every: int = 16):
        self.path, self.index = path, []          # list of (key, byte offset)
        with open(path, "rb") as f:
            offset, i = 0, 0
            for line in f:
                if i % index_every == 0:
                    self.index.append((json.loads(line)[0], offset))
                offset += len(line)
                i += 1

    @staticmethod
    def write(path: str, items):
        with open(path, "w") as f:
            for k, v in items:                     # items must be sorted by key
                f.write(json.dumps([k, v]) + "\n")
        return SSTable(path)

    def get(self, key: str):
        start = 0
        for k, off in self.index:                  # find last indexed key <= key
            if k > key:
                break
            start = off
        with open(self.path, "rb") as f:
            f.seek(start)
            for line in f:
                k, v = json.loads(line)
                if k == key:
                    return v
                if k > key:
                    return None
        return None

    def items(self):
        with open(self.path) as f:
            for line in f:
                yield tuple(json.loads(line))


class LSMStore:
    def __init__(self, directory: str, memtable_limit: int = 1000):
        self.dir, self.limit = directory, memtable_limit
        os.makedirs(directory, exist_ok=True)
        self.memtable = {}
        self.sstables = []                         # newest first
        self.seq = 0
        self.wal_path = os.path.join(directory, "wal.log")
        self._replay_wal()
        self.wal = open(self.wal_path, "a")

    def _replay_wal(self):
        if os.path.exists(self.wal_path):          # crash recovery
            with open(self.wal_path) as f:
                for line in f:
                    k, v = json.loads(line)
                    self.memtable[k] = v

    def put(self, key: str, value: str):
        self.wal.write(json.dumps([key, value]) + "\n")
        self.wal.flush()
        os.fsync(self.wal.fileno())                # durable before acknowledging
        self.memtable[key] = value
        if len(self.memtable) >= self.limit:
            self.flush()

    def delete(self, key: str):
        self.put(key, TOMBSTONE)                   # deletes are writes too

    def get(self, key: str):
        if key in self.memtable:
            v = self.memtable[key]
            return None if v == TOMBSTONE else v
        for table in self.sstables:                # newest data wins
            v = table.get(key)
            if v is not None:
                return None if v == TOMBSTONE else v
        return None

    def flush(self):
        if not self.memtable:
            return
        self.seq += 1
        path = os.path.join(self.dir, f"sst-{self.seq:06d}.jsonl")
        self.sstables.insert(0, SSTable.write(path, sorted(self.memtable.items())))
        self.memtable = {}
        self.wal.close()
        self.wal = open(self.wal_path, "w")        # truncate: data is now in an SSTable

    def compact(self):
        """Merge all SSTables into one, keeping the newest value and dropping tombstones."""
        merged = {}
        for table in reversed(self.sstables):      # oldest first, newer overwrite
            merged.update(dict(table.items()))
        live = sorted((k, v) for k, v in merged.items() if v != TOMBSTONE)
        old = self.sstables
        self.seq += 1
        path = os.path.join(self.dir, f"sst-{self.seq:06d}.jsonl")
        self.sstables = [SSTable.write(path, live)]
        for t in old:
            os.remove(t.path)


if __name__ == "__main__":
    d = tempfile.mkdtemp()
    db = LSMStore(d, memtable_limit=100)
    for i in range(1000):
        db.put(f"k{i:04d}", f"v{i}")
    db.put("k0005", "updated")
    db.delete("k0006")
    assert db.get("k0005") == "updated" and db.get("k0006") is None and db.get("k0999") == "v999"
    tables_before = len(db.sstables)
    db.flush()
    db.compact()
    assert len(db.sstables) == 1 < tables_before
    assert db.get("k0005") == "updated" and db.get("k0006") is None

    db.put("after_compaction", "in memtable and WAL only")
    db.wal.close()
    recovered = LSMStore(d, memtable_limit=100)   # simulate a restart: WAL replay
    recovered.sstables = db.sstables
    assert recovered.get("after_compaction") == "in memtable and WAL only"
    print(f"lsm_kv_store: all checks passed ({tables_before} SSTables compacted into 1)")
```
<!-- /code -->

## Exercises to extend it

1. Add a **Bloom filter** per SSTable (reuse [`bloom_filter.py`](04-bloom-filter.md)) so `get` skips tables that cannot contain the key.
2. Add **range scans**: merge iterators over the memtable and all SSTables (a heap-based k-way merge).
3. Implement **leveled compaction**: L0 flushes, L1+ non-overlapping key ranges, compact one file at a time.
4. Persist the **manifest** (list of live SSTables) so recovery does not depend on in-memory state.
5. Add checksums to WAL records to detect torn writes.

## Interview questions

<details>
<summary>Why are deletes writes in an LSM tree?</summary>

SSTables are immutable, so you cannot remove a key from an older file. A tombstone record is written instead; it shadows older values during reads and is physically dropped during compaction (only after it has been merged past all older copies, otherwise the old value could resurface).

</details>

<details>
<summary>What is write amplification and why do LSM trees have it?</summary>

The ratio of bytes written to disk vs bytes written by the application. Each value is written to the WAL, then to an SSTable on flush, then rewritten during each compaction level it passes through. Leveled compaction can rewrite data 10x or more; the trade is sequential IO and good read performance.

</details>

## Related

- [Indexes and Storage Engines](../03-data/02-indexes-storage-engines.md)
- [SQL durability (WAL)](../03-data/01-sql-acid-transactions.md)
