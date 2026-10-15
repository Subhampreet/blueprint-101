from sketch import Diagram


def raft():
    d = Diagram("raft-log-replication", "Raft: leader election and log replication")
    d.zone("el", 20, 70, 430, 330, "Election (term 5)", color="violet")
    d.ellipse("f", 40, 120, 150, 70, "Follower", "timeout 150-300 ms", color="gray")
    d.ellipse("c", 260, 120, 160, 70, "Candidate", "votes for self", color="yellow")
    d.ellipse("l", 150, 290, 150, 70, "Leader", "heartbeats", color="green")
    d.arrow("f", "c", label="no heartbeat")
    d.arrow("c", "l", label="majority votes")
    d.arrow("l", "f", label="higher term\nseen", dashed=True, bend=50)
    d.zone("rep", 490, 70, 610, 330, "Replication", color="green")
    d.box("ld", 520, 120, 260, 56, "Leader log: 1 2 3 4 [5]", color="green", size=16)
    d.box("f1", 820, 110, 250, 50, "F1: 1 2 3 4 [5]  ack", color="white", size=15)
    d.box("f2", 820, 180, 250, 50, "F2: 1 2 3 4 [5]  ack", color="white", size=15)
    d.box("f3", 820, 250, 250, 50, "F3: 1 2 3  (behind)", color="gray", size=15)
    d.box("f4", 820, 320, 250, 50, "F4: down", color="red", size=15)
    for x in ("f1", "f2", "f3", "f4"):
        d.arrow("ld", x, dashed=(x == "f4"))
    d.note("n", 520, 230, 260, 140, "Entry 5 is committed when\na majority (3 of 5) stored it.\nThen apply to state machine\nand reply to the client.")
    return d


def clocks():
    d = Diagram("vector-clocks", "Vector clocks detect concurrent updates")
    for i, (n, y) in enumerate((("A", 100), ("B", 220), ("C", 340))):
        d.text("n%d" % i, 30, y - 12, "Node " + n, size=17)
        d.point("s%d" % i, 120, y)
        d.point("e%d" % i, 1020, y)
        d.line("s%d" % i, "e%d" % i, color="#868e96")
    evs = [("a1", 200, 100, "[1,0,0]"), ("a2", 420, 100, "[2,0,0]"), ("b1", 520, 220, "[2,1,0]"),
           ("c1", 360, 340, "[0,0,1]"), ("b2", 760, 220, "[2,2,1]"), ("a3", 700, 100, "[3,0,0]")]
    for id, x, y, lbl in evs:
        d.ellipse(id, x - 45, y - 20, 90, 40, lbl, color="yellow", size=14)
    d.arrow("a2", "b1", label="send")
    d.arrow("c1", "b2", label="send", label_pos=0.4)
    d.note("n", 760, 380, 330, 110, "[3,0,0] vs [2,2,1]: neither >= the\nother in every slot, so A's write and\nB's write are CONCURRENT.\nKeep both (siblings) or merge.")
    return d


def mapreduce():
    d = Diagram("mapreduce", "MapReduce word count")
    d.box("in", 20, 160, 150, 90, "Input splits", "HDFS / S3 blocks", color="gray")
    for i in range(3):
        d.box("m%d" % i, 230, 60 + i * 110, 150, 64, "Map %d" % (i + 1), "emit (word, 1)", color="blue")
        d.arrow("in", "m%d" % i)
    d.zone("sh", 430, 40, 200, 380, "Shuffle + sort", color="orange")
    d.text("st", 450, 320, "partition by\nhash(word) % R,\nsort by key", size=14)
    for i in range(2):
        d.box("r%d" % i, 680, 100 + i * 140, 150, 64, "Reduce %d" % (i + 1), "sum counts", color="green")
        for j in range(3):
            d.line("m%d" % j, "r%d" % i, color="#adb5bd")
    d.box("out", 900, 160, 150, 90, "Output", "part files", color="cyan")
    d.arrow("r0", "out")
    d.arrow("r1", "out")
    return d


def lambda_kappa():
    d = Diagram("lambda-kappa", "Lambda vs Kappa architecture")
    d.zone("l", 20, 70, 560, 330, "Lambda", color="orange")
    d.queue("ls", 40, 200, 130, 60, "events")
    d.box("bl", 220, 110, 160, 64, "Batch layer", "Spark, exact,\nrecompute all", color="blue")
    d.box("sl", 220, 280, 160, 64, "Speed layer", "Flink, recent,\napproximate", color="green")
    d.box("sv", 420, 195, 140, 70, "Serving", "merge views", color="violet")
    d.arrow("ls", "bl")
    d.arrow("ls", "sl")
    d.arrow("bl", "sv")
    d.arrow("sl", "sv")
    d.zone("k", 620, 70, 480, 330, "Kappa", color="green")
    d.queue("ks", 640, 200, 150, 60, "replayable log")
    d.box("sp", 830, 190, 140, 80, "Stream job v1", "and v2 replaying\nfrom offset 0", color="green")
    d.box("ksv", 990, 200, 90, 60, "Serving", color="violet", size=15)
    d.arrow("ks", "sp")
    d.arrow("sp", "ksv")
    d.text("kt", 640, 320, "one code path; reprocess by replaying\nthe log into a new table, then switch", size=14)
    return d


def bloom():
    d = Diagram("bloom-filter", "Bloom filter: k hashes into an m-bit array")
    bits = "0 1 0 1 1 0 0 1 0 1 0 0 1 0 1 0".split()
    for i, b in enumerate(bits):
        d.box("b%d" % i, 60 + i * 56, 210, 50, 50, b, color="green" if b == "1" else "white", size=17)
    d.box("x", 120, 70, 170, 56, 'add("cat")', color="blue", size=16)
    d.box("y", 600, 70, 190, 56, 'contains("dog")?', color="orange", size=16)
    d.arrow("x", "b1", label="h1")
    d.arrow("x", "b4", label="h2")
    d.arrow("x", "b7", label="h3")
    d.arrow("y", "b9", dashed=True)
    d.arrow("y", "b12", dashed=True)
    d.arrow("y", "b13", dashed=True, color="#e03131")
    d.note("n", 60, 300, 880, 74, "Any bit = 0  ->  definitely not present.   All bits = 1  ->  probably present (false positive possible).\nm = -n ln(p) / (ln 2)^2 bits, k = (m/n) ln 2.  ~10 bits per item gives ~1% false positives. No deletes (use counting variant).")
    return d


def count_min():
    d = Diagram("count-min-sketch", "Count-Min Sketch: d rows of w counters")
    rows = [[3, 0, 7, 1, 0, 4, 2, 0], [0, 5, 1, 0, 7, 0, 3, 2], [2, 0, 0, 8, 1, 0, 7, 1]]
    for r, row in enumerate(rows):
        d.text("h%d" % r, 30, 128 + r * 70, "h%d" % (r + 1), size=17)
        for c, v in enumerate(row):
            hot = (r, c) in ((0, 2), (1, 4), (2, 6))
            d.box("c%d_%d" % (r, c), 90 + c * 70, 110 + r * 70, 62, 52, str(v), color="yellow" if hot else "white", size=17)
    d.note("n", 680, 110, 380, 190, "add(x): increment one counter\nper row (column = h_i(x)).\nestimate(x) = MIN over rows\n= min(7, 7, 7) = 7.\nNever underestimates; error\n<= e/w x total with prob 1-e^-d.")
    return d


def geohash():
    d = Diagram("geohash-quadtree", "Geohash grid vs quadtree")
    d.zone("g", 20, 70, 470, 380, "Geohash: fixed grid, prefix = area", color="blue")
    labels = ["tdr1", "tdr3", "tdr9", "tdr0", "tdr2", "tdr8", "tdqb", "tdqc", "tdqf"]
    for i, l in enumerate(labels):
        r, c = divmod(i, 3)
        d.box("g%d" % i, 60 + c * 130, 120 + r * 100, 120, 90, l, color="cyan" if i == 4 else "white", size=17)
    d.text("gt", 60, 425, "search the cell + 8 neighbours", size=14)
    d.zone("q", 520, 70, 580, 380, "Quadtree: split dense cells", color="green")
    d.box("q1", 560, 120, 240, 150, "sparse (1 node)", color="white", size=16)
    d.box("q2", 810, 120, 240, 150, "", color="white")
    for i in range(4):
        r, c = divmod(i, 2)
        d.box("q2_%d" % i, 820 + c * 115, 130 + r * 68, 105, 60, "dense" if i == 0 else "", color="green" if i == 0 else "white", size=14)
    d.box("q3", 560, 280, 240, 150, "", color="white")
    d.box("q4", 810, 280, 240, 150, "sparse", color="white", size=16)
    d.text("qt", 560, 435, "leaf when <= K points (e.g. 100 drivers)", size=14)
    return d


def ml_serving():
    d = Diagram("ml-platform", "ML platform: features, training, serving, monitoring")
    d.box("src", 20, 160, 150, 70, "Events + DBs", color="gray")
    d.box("fp", 230, 60, 180, 70, "Feature pipelines", "batch + streaming", color="orange")
    d.db("off", 470, 20, 170, 100, "Offline store", "history for training")
    d.box("on", 470, 160, 170, 64, "Online store", "Redis, low latency", color="red")
    d.box("tr", 720, 20, 170, 74, "Training", "pipelines, GPUs", color="blue")
    d.box("reg", 950, 20, 150, 74, "Model registry", "versions, lineage", color="yellow")
    d.box("srv", 720, 160, 170, 74, "Model serving", "Triton / TF Serving\nshadow, canary", color="violet")
    d.user("app", 1000, 150, "Product API")
    d.box("mon", 720, 300, 170, 74, "Monitoring", "drift, latency,\nbusiness metrics", color="pink")
    d.box("ab", 470, 300, 170, 74, "A/B testing", "experiment service", color="green")
    d.arrow("src", "fp")
    d.arrow("fp", "off")
    d.arrow("fp", "on")
    d.arrow("off", "tr")
    d.arrow("tr", "reg")
    d.arrow("reg", "srv", label="deploy")
    d.arrow("on", "srv", label="features")
    d.arrow("app", "srv", both=True, label="predict")
    d.arrow("srv", "mon", dashed=True)
    d.arrow("ab", "srv", dashed=True, label="variant")
    return d


def recsys():
    d = Diagram("recsys-funnel", "Recommendation funnel: retrieve, rank, re-rank")
    stages = [("cat", "Catalog", "100M items", 520, "gray"), ("ret", "Candidate generation", "~1,000 items\nANN on embeddings, co-visitation,\nfollowed creators, trending", 440, "blue"),
              ("rank", "Ranking", "~100 items, heavy model\n(predict click, watch time)", 340, "orange"),
              ("rr", "Re-ranking + filters", "diversity, freshness,\nbusiness rules, seen", 240, "green"), ("out", "Feed", "10 to 20 shown", 150, "violet")]
    y = 60
    for id, l, s, w, c in stages:
        d.box(id, 300 - w / 2 + 260, y, w, 70 if id not in ("ret",) else 90, l, s, color=c, size=17)
        y += 110 if id != "ret" else 130
    for a, b in (("cat", "ret"), ("ret", "rank"), ("rank", "rr"), ("rr", "out")):
        d.arrow(a, b)
    d.note("n", 880, 160, 230, 180, "Each stage is cheaper\nper item than the next.\nBudget: tens of ms total.\nFeatures from an online\nfeature store.")
    return d


def blockchain():
    d = Diagram("blockchain", "Blockchain: hash-linked blocks")
    for i in range(3):
        x = 40 + i * 340
        d.box("b%d" % i, x, 100, 280, 170, "Block %d" % (100 + i),
              "prev_hash: %s...\nmerkle_root: 9c%d1...\nnonce / validator sig\ntxs: [t1, t2, ...]" % (("00a7", "3f9e", "b21c")[i], i),
              color=("blue", "green", "yellow")[i])
        if i:
            d.arrow("b%d" % (i - 1), "b%d" % i, label="hash(prev)")
    d.note("n", 40, 320, 960, 74, "Changing any old transaction changes its block hash, which breaks every later prev_hash link.\nConsensus (PoW / PoS / BFT) decides which chain of blocks everyone accepts.")
    return d


def build():
    return [raft(), clocks(), mapreduce(), lambda_kappa(), bloom(), count_min(), geohash(), ml_serving(),
            recsys(), blockchain()]
