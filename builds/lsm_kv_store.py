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
