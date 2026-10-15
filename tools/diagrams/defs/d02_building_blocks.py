import math

from sketch import Diagram


def dns_resolution():
    d = Diagram("dns-resolution", "DNS resolution for www.example.com")
    d.user("u", 30, 200, "Browser", "+ OS cache")
    d.box("res", 190, 200, 210, 74, "Recursive resolver", "ISP / 8.8.8.8 / 1.1.1.1", color="cyan")
    d.box("root", 640, 60, 170, 64, "Root server", "knows .com servers", color="gray")
    d.box("tld", 640, 200, 170, 64, ".com TLD server", "knows example.com NS", color="yellow")
    d.box("auth", 640, 340, 170, 64, "Authoritative NS", "example.com zone", color="green")
    d.arrow("u", "res", label="1. query", label_pos=0.45)
    d.arrow("res", "root", label="2. where is .com?", bend=-10)
    d.arrow("res", "tld", label="3. where is example.com?")
    d.arrow("res", "auth", label="4. A record?", bend=10)
    d.arrow("auth", "res", label="5. 93.184.216.34, TTL 300", fs="l", ts="b", via=[(295, 372)], dashed=True, label_pos=0.3)
    d.note("n", 880, 160, 260, 120, "Every hop caches by TTL.\nMost lookups stop at the\nbrowser, OS or resolver\ncache: 0 to 5 ms.")
    return d


def lb_overview():
    d = Diagram("lb-overview", "Load balancer: one address, many healthy servers")
    d.user("u1", 30, 90, "Users")
    d.box("dns", 150, 100, 120, 56, "DNS", "lb.example.com", color="cyan")
    d.box("lb1", 330, 60, 150, 60, "LB (active)", "VIP 10.0.0.10", color="violet")
    d.box("lb2", 330, 170, 150, 60, "LB (standby)", "VRRP heartbeat", color="gray")
    for i in range(3):
        d.box("s%d" % i, 600, 30 + i * 90, 150, 60, "Server %d" % (i + 1),
              "healthy" if i < 2 else "failing check", color="blue" if i < 2 else "red")
        d.arrow("lb1", "s%d" % i, dashed=(i == 2), color="#e03131" if i == 2 else None)
    d.arrow("u1", "dns", label="resolve")
    d.arrow("dns", "lb1")
    d.line("lb1", "lb2", dashed=True, label="heartbeat")
    d.note("hc", 330, 290, 300, 80, "Health check: GET /healthz every 5s,\n3 failures = remove, 2 passes = add back")
    return d


def lb_l4_l7():
    d = Diagram("lb-l4-vs-l7", "Layer 4 vs Layer 7 load balancing")
    d.zone("z4", 20, 70, 470, 320, "L4: sees IP + port only", color="blue")
    d.user("c4", 40, 180, "Client")
    d.box("l4", 160, 180, 130, 64, "L4 LB", "TCP/UDP", color="blue")
    d.box("a4", 350, 110, 120, 56, "Server A", color="white")
    d.box("b4", 350, 250, 120, 56, "Server B", color="white")
    d.arrow("c4", "l4", label="TCP SYN")
    d.arrow("l4", "a4", label="conn 1")
    d.arrow("l4", "b4", label="conn 2")
    d.text("t4", 40, 330, "Fast, protocol agnostic, cannot read URLs\nor cookies, may terminate TLS or pass it through", size=14)
    d.zone("z7", 530, 70, 560, 320, "L7: reads HTTP (path, headers, cookies)", color="violet")
    d.user("c7", 550, 180, "Client")
    d.box("l7", 700, 180, 130, 64, "L7 LB", "terminates TLS", color="violet")
    d.box("api", 890, 100, 180, 56, "/api/* pool", color="green")
    d.box("img", 890, 190, 180, 56, "/images/* pool", color="yellow")
    d.box("can", 890, 280, 180, 56, "canary (x-beta: 1)", color="orange")
    d.arrow("c7", "l7", label="GET /api", label_pos=0.45)
    d.arrow("l7", "api", label="path")
    d.arrow("l7", "img")
    d.arrow("l7", "can", label="header")
    return d


def gslb():
    d = Diagram("gslb-geo-routing", "Global load balancing with GeoDNS / anycast")
    d.user("eu", 40, 40, "User in Berlin")
    d.user("in", 40, 260, "User in Mumbai")
    d.box("gdns", 230, 160, 170, 74, "GeoDNS / GSLB", "geo + health + latency", color="cyan")
    d.zone("r1", 480, 40, 270, 150, "eu-west", color="blue")
    d.box("lbeu", 510, 90, 200, 70, "Regional LB", "healthy", color="blue")
    d.zone("r2", 480, 230, 270, 150, "ap-south", color="green")
    d.box("lbin", 510, 280, 200, 70, "Regional LB", "healthy", color="green")
    d.arrow("eu", "gdns", label="api.example.com?", label_pos=0.6)
    d.arrow("in", "gdns")
    d.arrow("gdns", "lbeu", label="EU IP")
    d.arrow("gdns", "lbin", label="APAC IP")
    d.note("n", 790, 120, 250, 160, "If ap-south fails health\nchecks, GSLB answers\nwith eu-west instead.\nFailover speed is bounded\nby DNS TTL (keep it 30 to 60s).")
    return d


def cache_aside():
    d = Diagram("cache-aside", "Cache-aside (lazy loading): the default pattern")
    d.box("app", 60, 160, 160, 74, "Application", color="blue")
    d.box("cache", 420, 50, 170, 74, "Cache", "Redis / Memcached", color="red")
    d.db("db", 430, 250, 150, 110, "Database")
    d.arrow("app", "cache", label="1. GET key", bend=-45)
    d.arrow("cache", "app", label="2. miss (nil)", bend=-45, dashed=True)
    d.arrow("app", "db", label="3. SELECT", bend=-45)
    d.arrow("db", "app", label="4. row", bend=-45, dashed=True)
    d.arrow("app", "cache", label="5. SET key TTL", fs="t", ts="l", via=[(140, 87)], label_pos=0.5)
    d.note("n", 660, 120, 330, 150, "Read: cache first, DB on miss,\nthen populate.\nWrite: update DB, then DELETE\nthe key (not SET), so the next\nread reloads fresh data.")
    return d


def cache_write_strategies():
    d = Diagram("cache-write-strategies", "Write-through vs write-behind vs write-around")
    d.zone("wt", 20, 70, 330, 340, "Write-through", color="blue")
    d.box("a1", 50, 120, 120, 56, "App", color="blue")
    d.box("c1", 210, 120, 120, 56, "Cache", color="red")
    d.db("d1", 210, 240, 120, 100, "DB")
    d.arrow("a1", "c1", label="write")
    d.arrow("c1", "d1", label="sync write")
    d.text("t1", 40, 355, "ack after BOTH. consistent,\nslower writes", size=14)
    d.zone("wb", 380, 70, 330, 340, "Write-behind (write-back)", color="orange")
    d.box("a2", 410, 120, 120, 56, "App", color="blue")
    d.box("c2", 570, 120, 120, 56, "Cache", color="red")
    d.queue("q2", 560, 220, 130, 50, "buffer")
    d.db("d2", 410, 240, 110, 100, "DB")
    d.arrow("a2", "c2", label="write")
    d.arrow("c2", "q2")
    d.arrow("q2", "d2", label="async batch", dashed=True)
    d.text("t2", 400, 355, "ack from cache. fast,\nrisk of loss on crash", size=14)
    d.zone("wa", 740, 70, 330, 340, "Write-around", color="green")
    d.box("a3", 770, 120, 120, 56, "App", color="blue")
    d.box("c3", 930, 120, 120, 56, "Cache", color="red")
    d.db("d3", 770, 240, 120, 100, "DB")
    d.arrow("a3", "d3", label="write")
    d.arrow("a3", "c3", label="reads only", dashed=True)
    d.text("t3", 760, 355, "cache filled on read.\ngood for write once data", size=14)
    return d


def cache_layers():
    d = Diagram("cache-layers", "Multi-level caching on a request path")
    items = [("br", "Browser", "Cache-Control\nhit: 0 ms", "white"), ("cdn", "CDN edge", "static + some API\nhit: 5 to 30 ms", "cyan"),
             ("gw", "Gateway", "response cache\nhit: ~1 ms", "violet"), ("app", "App", "in-process LRU\nhit: ~0.1 ms", "blue"),
             ("rd", "Redis", "shared cache\nhit: 0.5 to 1 ms", "red")]
    for i, (id, l, s, c) in enumerate(items):
        d.box(id, 30 + i * 175, 105, 150, 80, l, s, color=c)
        if i:
            d.arrow(items[i - 1][0], id)
    d.db("db", 910, 95, 130, 100, "DB", "miss: 1 to 50 ms")
    d.arrow("rd", "db")
    d.note("n", 200, 240, 560, 70, "Each layer absorbs traffic so the next one sees less.\nEach layer is one more place that can serve stale data.")
    return d


def cache_stampede():
    d = Diagram("cache-stampede", "Cache stampede and single-flight protection")
    d.zone("bad", 20, 70, 450, 290, "Without protection", color="red")
    d.stack("r1", 50, 160, 120, 70, "1,000 req", "same hot key", color="gray")
    d.box("c1", 220, 110, 110, 56, "Cache", "expired!", color="red")
    d.db("d1", 340, 220, 110, 110, "DB", "1,000 queries", color="red")
    d.arrow("r1", "c1", label="miss")
    d.arrow("r1", "d1", label="all reload", label_pos=0.4)
    d.zone("good", 510, 70, 560, 290, "With lock / single-flight", color="green")
    d.stack("r2", 540, 160, 120, 70, "1,000 req", color="gray")
    d.box("c2", 720, 100, 150, 64, "Cache", "stale value served", color="green")
    d.box("lk", 720, 230, 150, 60, "Lock holder", "SET NX lock", color="yellow")
    d.db("d2", 940, 210, 110, 110, "DB", "1 query", color="green")
    d.arrow("r2", "c2", label="999 wait or stale")
    d.arrow("r2", "lk", label="1 wins")
    d.arrow("lk", "d2")
    d.arrow("lk", "c2", label="refill", dashed=True)
    return d


def cdn():
    d = Diagram("cdn-push-pull", "CDN: edge PoPs in front of an origin")
    d.box("origin", 430, 50, 200, 74, "Origin", "S3 bucket / web servers", color="green")
    d.box("shield", 430, 170, 200, 60, "Origin shield", "regional mid-tier cache", color="cyan")
    pops = [("p1", "PoP Frankfurt", 120), ("p2", "PoP Mumbai", 430), ("p3", "PoP Virginia", 740)]
    for id, l, x in pops:
        d.box(id, x, 290, 200, 60, l, "edge cache", color="blue")
        d.arrow(id, "shield", dashed=True, label="miss" if id == "p2" else "")
    d.user("u1", 195, 400, "EU users")
    d.user("u2", 505, 400, "India users")
    d.user("u3", 815, 400, "US users")
    d.arrow("u1", "p1")
    d.arrow("u2", "p2")
    d.arrow("u3", "p3")
    d.arrow("shield", "origin", dashed=True, label="pull on miss")
    d.note("push", 720, 40, 300, 100, "Push CDN: you upload to the CDN\nahead of time (big, rarely\nchanging files, releases).\nPull CDN: edge fetches on first miss.")
    return d


def proxies():
    d = Diagram("forward-vs-reverse-proxy", "Forward proxy vs reverse proxy")
    d.zone("f", 20, 70, 500, 230, "Forward proxy: acts for CLIENTS", color="orange")
    d.user("c1", 40, 140, "Employee")
    d.box("fp", 170, 150, 140, 64, "Forward proxy", "egress filter", color="orange")
    d.cloud("net", 350, 130, 150, 100, "Internet")
    d.arrow("c1", "fp")
    d.arrow("fp", "net")
    d.zone("r", 560, 70, 520, 230, "Reverse proxy: acts for SERVERS", color="violet")
    d.cloud("net2", 580, 130, 140, 100, "Internet")
    d.box("rp", 760, 150, 140, 64, "Reverse proxy", "TLS, cache, LB", color="violet")
    d.stack("srv", 950, 150, 110, 64, "Servers", color="blue")
    d.arrow("net2", "rp")
    d.arrow("rp", "srv")
    return d


def api_gateway():
    d = Diagram("api-gateway", "API gateway: one front door for many services")
    d.user("web", 30, 80, "Web")
    d.user("mob", 30, 230, "Mobile")
    d.box("gw", 220, 110, 200, 170, "API Gateway",
          "authN (JWT)\nrate limiting\nrouting + versioning\nrequest aggregation\nTLS, logging, metrics", color="violet")
    d.box("us", 540, 50, 150, 56, "User svc", color="blue")
    d.box("os", 540, 140, 150, 56, "Order svc", color="blue")
    d.box("ps", 540, 230, 150, 56, "Payment svc", color="blue")
    d.box("auth", 220, 330, 200, 56, "Auth / IdP", "token validation keys", color="yellow")
    d.arrow("web", "gw")
    d.arrow("mob", "gw")
    d.arrow("gw", "us")
    d.arrow("gw", "os")
    d.arrow("gw", "ps")
    d.arrow("gw", "auth", dashed=True, label="JWKS (cached)")
    d.note("bff", 740, 110, 270, 120, "BFF variant: one gateway\nper client type (web BFF,\nmobile BFF) shaping\nresponses for that client.")
    return d


def hash_ring():
    d = Diagram("consistent-hash-ring", "Consistent hashing: keys walk clockwise to the next node")
    cx, cy, r = 330, 300, 190
    d.ellipse("ring", cx - r, cy - r, 2 * r, 2 * r, "", color="none")
    nodes = [("A", 20, "blue"), ("B", 130, "green"), ("C", 220, "orange"), ("D", 300, "violet")]
    for name, deg, col in nodes:
        a = math.radians(deg - 90)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        d.box("n" + name, x - 48, y - 24, 96, 48, "Node " + name, color=col)
    keys = [("k1", 60, "k1"), ("k2", 175, "k2"), ("k3", 265, "k3"), ("k4", 345, "k4")]
    for id, deg, label in keys:
        a = math.radians(deg - 90)
        x, y = cx + (r - 70) * math.cos(a), cy + (r - 70) * math.sin(a)
        d.ellipse(id, x - 26, y - 18, 52, 36, label, color="yellow", size=15)
    d.arrow("k1", "nB", bend=-20)
    d.arrow("k2", "nC", bend=-20)
    d.arrow("k3", "nD", bend=-20)
    d.arrow("k4", "nA", bend=-20)
    d.note("n", 600, 150, 340, 230, "hash(key) and hash(node) share\none ring (0 to 2^32).\nA key belongs to the first node\nclockwise from it.\n\nAdd node E between A and B:\nonly keys in (A, E] move.\nAbout 1/N of keys move,\nnot almost all of them.")
    return d


def virtual_nodes():
    d = Diagram("consistent-hash-vnodes", "Virtual nodes smooth out the ring")
    cx, cy, r = 260, 260, 170
    d.ellipse("ring", cx - r, cy - r, 2 * r, 2 * r, "", color="none")
    cols = {"A": "blue", "B": "green", "C": "orange"}
    order = ["A", "B", "C", "B", "A", "C", "A", "C", "B"]
    for i, n in enumerate(order):
        a = math.radians(i * 40 - 90)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        d.box("v%d" % i, x - 30, y - 18, 60, 36, "%s%d" % (n, order[:i + 1].count(n)), color=cols[n], size=15)
    d.note("n", 500, 120, 380, 220, "Each physical node owns many\npositions (100 to 256 vnodes).\n\n+ load evens out statistically\n+ a dead node's load spreads over\n  all survivors, not one neighbour\n+ weight big machines with more vnodes\n- bigger routing table")
    return d


def queue_models():
    d = Diagram("queue-vs-pubsub", "Point-to-point queue vs publish-subscribe")
    d.zone("q", 20, 70, 500, 280, "Queue: each message to ONE consumer", color="yellow")
    d.box("p1", 40, 180, 110, 60, "Producer", color="blue")
    d.queue("mq", 190, 180, 160, 60, "orders")
    d.box("w1", 400, 110, 100, 50, "Worker 1", color="green")
    d.box("w2", 400, 190, 100, 50, "Worker 2", color="green")
    d.box("w3", 400, 270, 100, 50, "Worker 3", color="green")
    d.arrow("p1", "mq")
    d.arrow("mq", "w1", label="m1")
    d.arrow("mq", "w2", label="m2")
    d.arrow("mq", "w3", label="m3")
    d.zone("ps", 560, 70, 520, 280, "Pub/Sub: each message to EVERY subscriber group", color="violet")
    d.box("p2", 580, 180, 110, 60, "Publisher", color="blue")
    d.queue("t", 730, 180, 140, 60, "topic")
    d.box("s1", 920, 100, 140, 50, "Email svc", color="pink")
    d.box("s2", 920, 185, 140, 50, "Analytics", color="pink")
    d.box("s3", 920, 270, 140, 50, "Search indexer", color="pink")
    d.arrow("p2", "t")
    d.arrow("t", "s1", label="m1")
    d.arrow("t", "s2", label="m1")
    d.arrow("t", "s3", label="m1")
    return d


def kafka():
    d = Diagram("kafka-partitions", "Kafka: partitions, offsets and consumer groups")
    d.box("prod", 30, 170, 130, 64, "Producers", "key = user_id", color="blue")
    d.zone("topic", 210, 60, 430, 330, "topic: orders (3 partitions, RF=3)", color="yellow")
    for i in range(3):
        d.box("p%d" % i, 240, 110 + i * 90, 370, 60, "P%d  | 0 | 1 | 2 | 3 | 4 | 5 | ..." % i,
              "append only log, ordered within partition", color="yellow", size=16)
        d.arrow("prod", "p%d" % i)
    d.zone("g1", 690, 60, 210, 330, "group: billing", color="green")
    d.box("c1", 715, 110, 160, 56, "consumer 1", "P0, P1", color="green")
    d.box("c2", 715, 250, 160, 56, "consumer 2", "P2", color="green")
    d.zone("g2", 930, 60, 180, 330, "group: analytics", color="pink")
    d.box("c3", 950, 175, 140, 60, "consumer", "P0, P1, P2", color="pink")
    d.arrow("p0", "c1")
    d.arrow("p1", "c1")
    d.arrow("p2", "c2")
    d.arrow("p2", "c3", dashed=True, fs="b", via=[(425, 420), (1020, 420)], ts="b", label="independent offsets", label_pos=0.55)
    return d


def rate_limiter_placement():
    d = Diagram("rate-limiter-placement", "Distributed rate limiter at the gateway")
    d.user("c", 30, 150, "Client", "API key k1")
    d.box("gw", 190, 150, 170, 74, "API Gateway", "limiter middleware", color="violet")
    d.box("redis", 190, 320, 170, 64, "Redis", "INCR + EXPIRE / Lua", color="red")
    d.box("rules", 420, 320, 170, 64, "Rules config", "100 req/min per key", color="yellow")
    d.stack("svc", 470, 150, 150, 74, "Services", color="blue")
    d.arrow("c", "gw", label="request")
    d.arrow("gw", "redis", label="check + count", both=True)
    d.arrow("rules", "gw", dashed=True, label="cached rules")
    d.arrow("gw", "svc", label="allowed")
    d.arrow("gw", "c", label="429 + Retry-After", fs="t", ts="t", via=[(275, 100), (55, 100)], color="#e03131", label_pos=0.45)
    return d


def token_bucket():
    d = Diagram("token-bucket", "Token bucket: refill at rate r, burst up to capacity b")
    d.box("refill", 60, 70, 200, 56, "Refill r tokens/s", color="green")
    d.box("bucket", 80, 180, 160, 150, "Bucket", "capacity b = 10\n\n7 tokens left", color="yellow")
    d.user("req", 360, 200, "Request")
    d.box("ok", 560, 140, 170, 56, "token taken, 200", color="green")
    d.box("no", 560, 270, 170, 56, "empty, 429", color="red")
    d.arrow("refill", "bucket")
    d.arrow("req", "bucket", label="take 1")
    d.arrow("req", "ok", label="tokens > 0")
    d.arrow("req", "no", label="tokens = 0")
    return d


def snowflake():
    d = Diagram("snowflake-id", "Snowflake ID: 64 bits, roughly time ordered")
    parts = [("s", "0", "sign", 50, "gray"), ("t", "41 bits timestamp", "ms since custom epoch (69 years)", 470, "blue"),
             ("dc", "5 bits", "datacenter", 110, "green"), ("w", "5 bits", "worker", 110, "orange"),
             ("seq", "12 bits", "sequence", 170, "violet")]
    x = 30
    for id, l, s, w, c in parts:
        d.box(id, x, 120, w, 80, l, s, color=c, size=16)
        x += w + 6
    d.note("n", 30, 250, 900, 74, "4,096 IDs per ms per worker = ~4M IDs/s per worker. No coordination at generation time.\nSorted by time across workers only roughly: clock skew can reorder IDs from different machines.")
    return d


def object_storage():
    d = Diagram("object-storage", "Object storage (S3 style): metadata and data split")
    d.user("c", 30, 160, "Client")
    d.box("api", 160, 160, 180, 64, "API / front end", "PUT/GET bucket/key", color="violet")
    d.db("meta", 420, 40, 160, 110, "Metadata", "key -> chunk ids,\nsize, ACL, version", color="yellow")
    d.stack("data", 420, 240, 170, 80, "Storage nodes", "chunks, erasure coded", color="green")
    d.arrow("c", "api")
    d.arrow("api", "meta", label="1. lookup / commit")
    d.arrow("api", "data", label="2. read / write chunks")
    d.note("n", 660, 100, 330, 160, "Immutable objects, flat namespace.\nDurability via replication (3x) or\nerasure coding (e.g. 10+4) across\nracks and AZs. Big uploads use\nmultipart + presigned URLs, so\nbytes skip your app servers.")
    return d


def inverted_index():
    d = Diagram("inverted-index", "Inverted index: term -> posting list")
    d.box("d1", 30, 70, 230, 56, "doc1: red fast car", color="white")
    d.box("d2", 30, 150, 230, 56, "doc2: fast blue bike", color="white")
    d.box("d3", 30, 230, 230, 56, "doc3: red bike", color="white")
    d.box("an", 320, 140, 150, 74, "Analyzer", "tokenize, lowercase,\nstem, stopwords", color="cyan")
    rows = [("red", "doc1, doc3"), ("fast", "doc1, doc2"), ("bike", "doc2, doc3"), ("car", "doc1"), ("blue", "doc2")]
    for i, (t, p) in enumerate(rows):
        d.box("t%d" % i, 540, 50 + i * 62, 100, 46, t, color="yellow", size=16)
        d.box("p%d" % i, 670, 50 + i * 62, 170, 46, p, color="green", size=16)
        d.arrow("t%d" % i, "p%d" % i)
    for i in (1, 2, 3):
        d.arrow("d%d" % i, "an")
    d.arrow("an", "t2")
    d.note("q", 880, 120, 210, 120, "query: red AND bike\n= intersect lists\n= doc3\nrank with BM25")
    return d


def build():
    return [dns_resolution(), lb_overview(), lb_l4_l7(), gslb(), cache_aside(), cache_write_strategies(),
            cache_layers(), cache_stampede(), cdn(), proxies(), api_gateway(), hash_ring(), virtual_nodes(),
            queue_models(), kafka(), rate_limiter_placement(), token_bucket(), snowflake(),
            object_storage(), inverted_index()]
