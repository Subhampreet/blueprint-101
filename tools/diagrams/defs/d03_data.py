from sketch import Diagram


def isolation_anomalies():
    d = Diagram("isolation-lost-update", "Lost update: two transactions, one overwritten")
    d.box("t1", 40, 90, 170, 56, "Txn A", color="blue")
    d.box("t2", 520, 90, 170, 56, "Txn B", color="orange")
    d.db("db", 290, 80, 150, 100, "stock = 10")
    steps = [
        (190, "A reads stock = 10", "blue"), (250, "B reads stock = 10", "orange"),
        (310, "A writes 10 - 1 = 9", "blue"), (370, "B writes 10 - 1 = 9", "orange"),
    ]
    for i, (y, t, c) in enumerate(steps):
        d.box("s%d" % i, 200 if c == "blue" else 380, y, 170, 44, t, color=c, size=15)
    d.note("n", 40, 440, 650, 74, "Two items sold, stock shows 9. Fix: SELECT ... FOR UPDATE, atomic\nUPDATE stock = stock - 1 WHERE stock > 0, optimistic version check, or SERIALIZABLE.")
    return d


def btree_vs_lsm():
    d = Diagram("btree-vs-lsm", "B-tree vs LSM-tree storage engines")
    d.zone("bz", 20, 70, 470, 380, "B+ tree (Postgres, MySQL InnoDB)", color="blue")
    d.box("root", 175, 110, 160, 50, "root: [40 | 80]", color="blue", size=15)
    d.box("i1", 45, 210, 130, 50, "[10 | 25]", color="blue", size=15)
    d.box("i2", 190, 210, 130, 50, "[50 | 65]", color="blue", size=15)
    d.box("i3", 335, 210, 130, 50, "[90 | 99]", color="blue", size=15)
    d.arrow("root", "i1")
    d.arrow("root", "i2")
    d.arrow("root", "i3")
    d.box("leaf", 45, 310, 420, 50, "leaf pages: sorted keys + rows, linked for range scans", color="white", size=14)
    d.arrow("i2", "leaf")
    d.text("bt", 45, 385, "update in place, 3 to 4 page reads per lookup\nfast reads, random writes, WAL for crash safety", size=14)
    d.zone("lz", 530, 70, 560, 380, "LSM tree (Cassandra, RocksDB, HBase)", color="green")
    d.box("w", 560, 110, 120, 50, "write", color="white")
    d.box("wal", 560, 200, 120, 50, "WAL", "append only", color="yellow", size=16)
    d.box("mem", 740, 110, 160, 56, "Memtable", "sorted, in RAM", color="orange")
    d.box("l0", 740, 220, 160, 46, "SSTables L0", color="green", size=15)
    d.box("l1", 740, 290, 200, 46, "L1 (compacted)", color="green", size=15)
    d.box("l2", 740, 360, 260, 46, "L2 (bigger, older)", color="green", size=15)
    d.arrow("w", "wal")
    d.arrow("w", "mem")
    d.arrow("mem", "l0", label="flush when full")
    d.arrow("l0", "l1", label="compaction", label_pos=0.4)
    d.arrow("l1", "l2")
    d.note("bf", 960, 110, 130, 110, "reads check\nmemtable,\nthen SSTables\n(Bloom filters\nskip most)", size=13)
    return d


def replication_modes():
    d = Diagram("replication-topologies", "Replication topologies")
    d.zone("sl", 20, 70, 330, 330, "Single leader", color="blue")
    d.db("l", 120, 110, 120, 90, "Leader", "reads + writes", color="blue")
    d.db("f1", 40, 280, 110, 90, "Follower", "reads", color="cyan")
    d.db("f2", 210, 280, 110, 90, "Follower", "reads", color="cyan")
    d.arrow("l", "f1", label="WAL stream")
    d.arrow("l", "f2")
    d.zone("ml", 380, 70, 330, 330, "Multi leader", color="orange")
    d.db("m1", 395, 150, 105, 90, "Leader", "region A", color="orange")
    d.db("m2", 590, 150, 105, 90, "Leader", "region B", color="orange")
    d.arrow("m1", "m2", both=True, bend=-50, label="async both ways")
    d.text("mt", 410, 280, "writes in both regions\nneed conflict resolution:\nLWW, merge, CRDTs", size=15)
    d.zone("ll", 740, 70, 350, 330, "Leaderless (Dynamo style)", color="green")
    d.user("c", 890, 110, "Client")
    d.db("n1", 760, 280, 95, 85, "N1", color="green")
    d.db("n2", 870, 280, 95, 85, "N2", color="green")
    d.db("n3", 980, 280, 95, 85, "N3", color="gray")
    d.arrow("c", "n1", label="W")
    d.arrow("c", "n2", label="W")
    d.arrow("c", "n3", dashed=True, label="down")
    return d


def sync_async():
    d = Diagram("sync-vs-async-replication", "Synchronous vs asynchronous replication")
    d.user("c", 30, 140, "Client")
    d.db("ld", 200, 120, 140, 100, "Leader")
    d.db("sf", 470, 50, 150, 100, "Sync follower", "must ack", color="blue")
    d.db("af", 470, 230, 150, 100, "Async follower", "may lag", color="gray")
    d.arrow("c", "ld", label="1. write")
    d.arrow("ld", "sf", label="2. replicate")
    d.arrow("sf", "ld", label="3. ack", bend=55, dashed=True)
    d.arrow("ld", "af", label="later", dashed=True)
    d.arrow("ld", "c", label="4. OK", bend=70, dashed=True)
    d.note("n", 680, 90, 330, 170, "Sync: no data loss on leader\nfailure, but write latency +1 RTT\nand writes stall if follower dies.\nSemi-sync: 1 sync + rest async.\nAsync: fast, but a failover can\nlose the last seconds of writes.")
    return d


def quorum():
    d = Diagram("quorum-rw", "Quorum: R + W > N means read and write sets overlap")
    d.zone("w", 40, 80, 500, 175, "W = 3 acknowledged the write (v2)", color="green")
    d.zone("r", 370, 100, 520, 175, "R = 3 replicas read", color="blue")
    for i in range(5):
        col = "green" if i < 3 else "white"
        d.db("n%d" % i, 60 + i * 170, 135, 120, 90, "Replica %d" % (i + 1), "v2" if i < 3 else "v1", color=col)
    d.box("rd", 470, 330, 260, 64, "Reader", "sees v1, v1, v2: returns v2", color="blue")
    for i in (2, 3, 4):
        d.arrow("n%d" % i, "rd", dashed=True)
    d.note("n", 40, 430, 850, 74, "N = 5, W = 3, R = 3: 3 + 3 > 5, so at least one replica in every read set has v2.\nThe reader picks the highest version and can fix stale replicas (read repair).")
    return d


def sharding_strategies():
    d = Diagram("sharding-strategies", "Sharding strategies")
    d.zone("r", 20, 70, 340, 320, "Range", color="blue")
    d.box("ra", 50, 120, 280, 50, "Shard 1: A to H", color="blue", size=16)
    d.box("rb", 50, 190, 280, 50, "Shard 2: I to Q", color="blue", size=16)
    d.box("rc", 50, 260, 280, 50, "Shard 3: R to Z", color="blue", size=16)
    d.text("rt", 50, 330, "+ range scans  - hot spots\n(time keys hit the last shard)", size=14)
    d.zone("h", 390, 70, 340, 320, "Hash", color="green")
    d.box("hk", 420, 120, 280, 50, "shard = hash(user_id) % N", color="white", size=16)
    for i in range(3):
        d.box("h%d" % i, 420 + i * 95, 210, 85, 50, "S%d" % (i + 1), color="green", size=16)
        d.arrow("hk", "h%d" % i)
    d.text("ht", 420, 330, "+ even spread  - no range scans,\nresharding moves data (use consistent hashing)", size=14)
    d.zone("dr", 760, 70, 340, 320, "Directory / lookup", color="orange")
    d.box("dir", 790, 120, 280, 70, "Lookup service", "tenant_42 -> shard 7", color="orange")
    d.box("d1", 790, 230, 130, 50, "Shard 7", color="orange", size=16)
    d.box("d2", 940, 230, 130, 50, "Shard 9", color="orange", size=16)
    d.arrow("dir", "d1")
    d.arrow("dir", "d2", dashed=True)
    d.text("dt", 790, 330, "+ flexible moves, per tenant placement\n- extra hop, lookup must be HA", size=14)
    return d


def two_pc():
    d = Diagram("two-phase-commit", "Two-phase commit (2PC)")
    d.box("co", 330, 50, 200, 64, "Coordinator", "txn manager", color="violet")
    d.db("p1", 90, 230, 150, 100, "Participant A", "orders DB")
    d.db("p2", 360, 230, 150, 100, "Participant B", "payments DB")
    d.db("p3", 630, 230, 150, 100, "Participant C", "inventory DB")
    for p in ("p1", "p2", "p3"):
        d.arrow("co", p, label="1. prepare" if p == "p2" else "")
        d.arrow(p, "co", label="2. vote yes" if p == "p3" else "", bend=-45, dashed=True)
    d.note("n", 840, 80, 270, 230, "Phase 2: all yes -> COMMIT,\nany no -> ABORT.\n\nBlocking: if the coordinator\ndies after prepare, participants\nhold locks and cannot decide\nalone. Latency = 2 round trips\n+ fsyncs at every step.")
    return d


def saga():
    d = Diagram("saga-orchestration", "Saga (orchestrated) with compensations")
    d.box("orc", 370, 40, 250, 64, "Order Saga Orchestrator", "state machine", color="violet")
    steps = [("s1", "Create order", "PENDING", "blue"), ("s2", "Reserve stock", "inventory svc", "green"),
             ("s3", "Charge card", "payment svc", "yellow"), ("s4", "Confirm order", "APPROVED", "blue")]
    for i, (id, l, s, c) in enumerate(steps):
        d.box(id, 40 + i * 250, 180, 200, 64, l, s, color=c)
        if i:
            d.arrow(steps[i - 1][0], id)
    d.arrow("orc", "s1", dashed=True)
    d.arrow("orc", "s3", dashed=True)
    comps = [("c1", "Cancel order", "red"), ("c2", "Release stock", "red")]
    d.box("c1", 40, 330, 200, 60, "Cancel order", "compensation", color="red")
    d.box("c2", 290, 330, 200, 60, "Release stock", "compensation", color="red")
    d.arrow("s3", "c2", label="card declined", color="#e03131", ts="r", fs="b", via=[(640, 360)])
    d.arrow("c2", "c1", color="#e03131")
    return d


def outbox():
    d = Diagram("transactional-outbox", "Transactional outbox: state change + event, atomically")
    d.box("svc", 40, 140, 160, 70, "Order service", color="blue")
    d.zone("tx", 250, 70, 300, 230, "one DB transaction", color="green")
    d.db("orders", 270, 110, 120, 90, "orders", color="green")
    d.db("ob", 410, 110, 120, 90, "outbox", "event rows", color="yellow")
    d.box("relay", 630, 140, 170, 70, "Relay / CDC", "Debezium, poller", color="orange")
    d.queue("k", 860, 140, 170, 70, "Kafka")
    d.arrow("svc", "orders", label="INSERT order", label_pos=0.35)
    d.arrow("svc", "ob", label="INSERT event", fs="b", via=[(120, 260), (470, 260)], ts="b")
    d.arrow("ob", "relay", label="read log")
    d.arrow("relay", "k", label="publish")
    d.note("n", 630, 260, 400, 74, "At least once publish, so consumers dedupe by event_id.\nNo 2PC between DB and broker needed.")
    return d


def oltp_olap():
    d = Diagram("data-platform", "Modern data platform: OLTP to OLAP")
    d.db("oltp", 30, 110, 140, 100, "OLTP DBs", "Postgres, MySQL")
    d.box("ev", 30, 260, 140, 60, "Events / logs", color="pink")
    d.queue("k", 220, 180, 190, 64, "Kafka, CDC")
    d.box("lake", 450, 90, 190, 74, "Data lake", "S3 + Parquet\nIceberg / Delta", color="cyan")
    d.box("etl", 450, 250, 190, 74, "Transform", "Spark, dbt, Flink", color="orange")
    d.db("wh", 710, 120, 170, 110, "Warehouse", "Snowflake, BigQuery,\nRedshift", color="violet")
    d.box("bi", 950, 80, 150, 56, "BI dashboards", color="yellow")
    d.box("ml", 950, 170, 150, 56, "ML features", color="yellow")
    d.box("rev", 950, 260, 150, 56, "Reverse ETL", color="yellow")
    d.arrow("oltp", "k")
    d.arrow("ev", "k")
    d.arrow("k", "lake", label="raw (bronze)")
    d.arrow("lake", "etl")
    d.arrow("etl", "wh", label="clean, modeled")
    d.arrow("wh", "bi")
    d.arrow("wh", "ml")
    d.arrow("wh", "rev")
    return d


def star_schema():
    d = Diagram("star-schema", "Star schema: facts in the middle, dimensions around")
    d.box("f", 330, 170, 230, 120, "fact_sales", "date_key, product_key,\nstore_key, customer_key,\nqty, amount", color="yellow")
    d.box("dd", 60, 60, 190, 74, "dim_date", "day, month, quarter", color="blue")
    d.box("dp", 640, 60, 190, 74, "dim_product", "name, category, brand", color="green")
    d.box("ds", 60, 330, 190, 74, "dim_store", "city, region", color="orange")
    d.box("dc", 640, 330, 190, 74, "dim_customer", "segment, SCD type 2", color="pink")
    for x in ("dd", "dp", "ds", "dc"):
        d.line("f", x)
    return d


def build():
    return [isolation_anomalies(), btree_vs_lsm(), replication_modes(), sync_async(), quorum(),
            sharding_strategies(), two_pc(), saga(), outbox(), oltp_olap(), star_schema()]
