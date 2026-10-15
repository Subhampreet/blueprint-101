from sketch import Diagram


def url_shortener():
    d = Diagram("case-url-shortener", "URL shortener: high level design")
    d.user("u", 20, 170, "Users")
    d.box("lb", 130, 170, 130, 64, "LB + API GW", "rate limits", color="violet")
    d.box("w", 330, 80, 170, 64, "Shorten service", "POST /urls", color="blue")
    d.box("r", 330, 270, 170, 64, "Redirect service", "GET /{code}", color="blue")
    d.box("kgs", 330, -20, 170, 64, "ID range allocator", "ZooKeeper / DB counter", color="orange")
    d.box("cache", 580, 270, 150, 64, "Redis cache", "code -> long URL", color="red")
    d.db("db", 600, 90, 150, 110, "URL store", "DynamoDB /\nCassandra")
    d.queue("k", 580, 400, 170, 56, "click events")
    d.box("an", 820, 380, 170, 74, "Analytics", "Flink -> OLAP", color="pink")
    d.arrow("u", "lb")
    d.arrow("lb", "w")
    d.arrow("lb", "r")
    d.arrow("w", "kgs", label="block of IDs")
    d.arrow("w", "db", label="write")
    d.arrow("r", "cache", label="1. get")
    d.arrow("cache", "db", label="2. miss", dashed=True)
    d.arrow("r", "k", dashed=True, label="async", fs="b", via=[(415, 428)])
    d.arrow("k", "an")
    d.arrow("r", "u", label="301/302 Location", fs="l", ts="b", via=[(45, 302)], dashed=True, label_pos=0.3)
    return d


def twitter_hld():
    d = Diagram("case-twitter-hld", "Twitter home timeline: write path and read path")
    d.user("u", 20, 190, "Users")
    d.box("gw", 130, 190, 130, 64, "API GW", color="violet")
    d.box("ts", 320, 60, 160, 64, "Tweet service", color="blue")
    d.box("tl", 320, 320, 160, 64, "Timeline service", "read path", color="blue")
    d.db("tdb", 560, 30, 150, 100, "Tweets DB", "sharded by tweet_id")
    d.queue("k", 320, 190, 170, 60, "tweet events")
    d.box("fo", 800, 183, 170, 74, "Fanout workers", "push to followers", color="orange")
    d.box("sg", 800, 30, 170, 64, "Social graph", "followers of X", color="green")
    d.box("tc", 800, 320, 170, 74, "Timeline cache", "Redis list per user\n(last 800 ids)", color="red")
    d.box("hy", 560, 320, 170, 74, "Merge celebs", "pull at read time", color="yellow")
    d.arrow("u", "gw")
    d.arrow("gw", "ts", label="POST tweet")
    d.arrow("gw", "tl", label="GET timeline")
    d.arrow("ts", "tdb")
    d.arrow("ts", "k")
    d.arrow("k", "fo")
    d.arrow("fo", "sg", label="who follows?")
    d.arrow("fo", "tc", label="LPUSH id")
    d.arrow("tl", "hy")
    d.arrow("hy", "tc", label="ids")
    d.arrow("hy", "tdb", dashed=True, label="hydrate +\ncelebrity tweets", fs="t", ts="b", label_pos=0.3)
    return d


def fanout_models():
    d = Diagram("case-fanout-models", "Fanout on write vs fanout on read vs hybrid")
    d.zone("w", 20, 70, 340, 320, "Push (fanout on write)", color="green")
    d.box("a", 120, 110, 140, 50, "Alice posts", color="blue", size=16)
    for i in range(3):
        d.box("f%d" % i, 40 + i * 105, 230, 95, 50, "feed %d" % (i + 1), color="red", size=15)
        d.arrow("a", "f%d" % i)
    d.text("wt", 40, 320, "+ reads are one cache lookup\n- celebrity with 50M followers =\n  50M writes per tweet", size=14)
    d.zone("r", 390, 70, 340, 320, "Pull (fanout on read)", color="blue")
    d.box("rd", 490, 110, 140, 50, "Bob opens app", color="blue", size=16)
    for i in range(3):
        d.box("p%d" % i, 410 + i * 105, 230, 95, 50, "user %d tweets" % (i + 1), color="yellow", size=13)
        d.arrow("rd", "p%d" % i, dashed=True)
    d.text("rt", 410, 320, "+ writes are cheap\n- every read merges N followees:\n  slow at p99", size=14)
    d.zone("h", 760, 70, 340, 320, "Hybrid (what Twitter did)", color="violet")
    d.box("h1", 790, 120, 280, 56, "normal users: push", color="green", size=16)
    d.box("h2", 790, 200, 280, 56, "celebrities (> ~100k): pull", color="yellow", size=16)
    d.box("h3", 790, 280, 280, 56, "merge at read, rank, cache", color="violet", size=16)
    d.arrow("h1", "h3", fs="r", ts="r", via=[(1090, 148), (1090, 308)])
    d.arrow("h2", "h3")
    return d


def instagram():
    d = Diagram("case-instagram", "Instagram: upload, process, serve, feed")
    d.user("u", 20, 170, "App")
    d.box("api", 140, 170, 150, 64, "Post service", "metadata", color="blue")
    d.box("s3", 140, 20, 150, 64, "Object storage", "originals", color="cyan")
    d.queue("q", 380, 20, 170, 64, "upload events")
    d.box("proc", 630, 10, 190, 84, "Image workers", "resize 150/320/640/1080\nWebP/AVIF, strip EXIF", color="orange")
    d.box("cdn", 900, 20, 150, 64, "CDN", color="cyan")
    d.db("pdb", 380, 160, 150, 100, "Posts DB", "sharded by user_id")
    d.box("feed", 630, 170, 190, 74, "Feed service", "fanout + ranking", color="violet")
    d.box("fc", 900, 170, 150, 74, "Feed cache", "per user ids", color="red")
    d.box("rank", 630, 310, 190, 64, "Ranking (ML)", "features + model", color="pink")
    d.box("like", 140, 310, 170, 64, "Likes / comments", "counters, sharded", color="green")
    d.arrow("u", "s3", label="1. presigned PUT")
    d.arrow("u", "api", label="2. create post")
    d.arrow("s3", "q")
    d.arrow("q", "proc")
    d.arrow("proc", "cdn", label="variants")
    d.arrow("api", "pdb")
    d.arrow("pdb", "feed", dashed=True, label="events")
    d.arrow("feed", "fc")
    d.arrow("feed", "rank", both=True)
    d.arrow("u", "like", dashed=True)
    d.arrow("cdn", "u", dashed=True, label="images", fs="t", ts="t", via=[(975, -20), (45, -20)], label_pos=0.5)
    return d


def chat():
    d = Diagram("case-chat", "WhatsApp style chat: connections, storage, delivery")
    d.user("a", 20, 60, "Alice")
    d.user("b", 20, 300, "Bob")
    d.stack("gw", 160, 160, 170, 80, "WS gateways", "hold sockets", color="blue")
    d.box("chat", 420, 160, 170, 80, "Chat service", "seq per conversation", color="green")
    d.db("msg", 730, 30, 160, 110, "Message store", "Cassandra:\n(conv_id, seq)")
    d.box("sess", 730, 190, 160, 64, "Session registry", "user -> gateway", color="red")
    d.box("grp", 420, 330, 170, 64, "Group service", "members (<= 1024)", color="yellow")
    d.box("push", 730, 310, 160, 74, "Push service", "APNs / FCM\nwhen offline", color="orange")
    d.box("media", 960, 190, 150, 74, "Media store", "encrypted blobs\n+ CDN", color="cyan")
    d.arrow("a", "gw", label="send (E2EE)", label_pos=0.65)
    d.arrow("gw", "chat")
    d.arrow("chat", "msg", label="1. persist")
    d.arrow("chat", "sess", label="2. where is Bob?")
    d.arrow("chat", "gw", label="3. deliver", bend=40)
    d.arrow("gw", "b")
    d.arrow("chat", "grp", dashed=True)
    d.arrow("chat", "push", dashed=True, label="offline")
    d.arrow("a", "media", dashed=True, label="upload encrypted media, send only a reference", fs="t", via=[(45, 0), (1035, 0)], ts="t")
    return d


def chat_receipts():
    d = Diagram("case-chat-receipts", "Message states: sent, delivered, read")
    d.lifeline("a", 120, 60, 420, "Alice", color="blue")
    d.lifeline("s", 480, 60, 420, "Server", color="green")
    d.lifeline("b", 840, 60, 420, "Bob", color="orange")
    d.msg(120, 480, 150, "msg (client_msg_id)", "m1")
    d.msg(480, 120, 195, "ack: SENT (one tick), seq=57", "m2", dashed=True)
    d.msg(480, 840, 250, "deliver seq=57", "m3")
    d.msg(840, 480, 300, "ack delivered", "m4", dashed=True)
    d.msg(480, 120, 345, "DELIVERED (two ticks)", "m5", dashed=True)
    d.msg(840, 480, 400, "read up to seq=57", "m6", dashed=True, color="#1971c2")
    d.msg(480, 120, 445, "READ (blue ticks)", "m7", dashed=True, color="#1971c2")
    return d


def youtube():
    d = Diagram("case-youtube", "Video platform: upload, transcode, deliver")
    d.user("c", 20, 70, "Creator")
    d.box("up", 140, 70, 160, 64, "Upload service", "resumable, chunked", color="blue")
    d.box("raw", 380, 70, 150, 64, "Raw storage", color="cyan")
    d.box("dag", 610, 50, 210, 104, "Transcoding DAG", "split -> encode ->\npackage HLS/DASH\n(many workers)", color="orange")
    d.box("enc", 900, 70, 160, 64, "Encoded segments", "240p ... 4K", color="cyan")
    d.box("cdn", 900, 230, 160, 74, "CDN / edge caches", "+ ISP appliances", color="cyan")
    d.user("v", 1130, 230, "Viewer")
    d.db("meta", 380, 230, 150, 100, "Video metadata", "title, status")
    d.box("play", 610, 230, 210, 74, "Playback API", "manifest + signed URLs", color="violet")
    d.box("views", 610, 370, 210, 64, "View counter", "Kafka -> aggregate", color="pink")
    d.box("rec", 380, 370, 150, 64, "Recommendations", color="pink")
    d.arrow("c", "up")
    d.arrow("up", "raw")
    d.arrow("raw", "dag")
    d.arrow("dag", "enc")
    d.arrow("enc", "cdn")
    d.arrow("cdn", "v")
    d.arrow("dag", "meta", dashed=True, label="status = ready")
    d.arrow("v", "play", label="watch", fs="b", via=[(1155, 340), (715, 340)], ts="b")
    d.arrow("play", "meta")
    d.arrow("play", "views", dashed=True)
    d.arrow("views", "rec", dashed=True)
    return d


def uber():
    d = Diagram("case-uber", "Ride hailing: location, matching, trips")
    d.user("dr", 20, 40, "Driver app")
    d.user("ri", 20, 300, "Rider app")
    d.stack("gw", 160, 160, 160, 80, "WS / API gateway", color="violet")
    d.box("loc", 400, 30, 180, 74, "Location service", "updates every 4 s", color="blue")
    d.box("geo", 660, 30, 190, 74, "Geo index", "Redis: H3 cell ->\nnearby drivers", color="red")
    d.box("match", 400, 170, 180, 74, "Matching / dispatch", "rank by ETA", color="green")
    d.box("eta", 660, 170, 190, 64, "ETA + routing", "road graph", color="yellow")
    d.box("price", 660, 270, 190, 64, "Pricing / surge", "supply vs demand", color="orange")
    d.box("trip", 400, 320, 180, 74, "Trip service", "state machine", color="blue")
    d.db("tdb", 660, 380, 170, 100, "Trips DB", "sharded by city")
    d.queue("k", 920, 120, 190, 100, "locations", size=15)
    d.arrow("dr", "gw", label="GPS pings")
    d.arrow("ri", "gw", label="request ride")
    d.arrow("gw", "loc")
    d.arrow("loc", "geo")
    d.arrow("loc", "k", dashed=True, fs="r", via=[(620, 67), (620, 10), (1000, 10)], ts="t")
    d.arrow("gw", "match")
    d.arrow("match", "geo", label="drivers near")
    d.arrow("match", "eta")
    d.arrow("match", "price", dashed=True)
    d.arrow("match", "trip")
    d.arrow("trip", "tdb")
    return d


def dropbox():
    d = Diagram("case-dropbox", "File sync: chunks, metadata, notifications")
    d.zone("cl", 20, 60, 220, 330, "Desktop client", color="gray")
    d.box("watch", 40, 100, 180, 56, "Watcher", "fs events", color="white", size=16)
    d.box("chunk", 40, 180, 180, 64, "Chunker", "4 MB blocks, SHA-256", color="white", size=16)
    d.box("ldb", 40, 270, 180, 64, "Local index", "SQLite", color="white", size=16)
    d.box("blk", 330, 90, 180, 74, "Block service", "dedupe by hash", color="blue")
    d.box("s3", 600, 90, 170, 74, "Block storage", "S3, immutable", color="cyan")
    d.box("meta", 330, 230, 180, 74, "Metadata service", "file -> block list,\nversions", color="green")
    d.db("mdb", 600, 220, 170, 100, "Metadata DB", "sharded by namespace")
    d.box("notif", 330, 370, 180, 64, "Notification svc", "long poll / WS", color="orange")
    d.user("other", 640, 370, "Other devices")
    d.arrow("watch", "chunk")
    d.arrow("chunk", "blk", label="1. upload missing\nblocks only")
    d.arrow("blk", "s3")
    d.arrow("chunk", "meta", label="2. commit\nblock list")
    d.arrow("meta", "mdb")
    d.arrow("meta", "notif", label="3. changed")
    d.arrow("notif", "other", label="4. pull changes")
    return d


def notifications():
    d = Diagram("case-notifications", "Notification system: fanout to many channels")
    d.box("src", 20, 160, 160, 74, "Producers", "order svc, marketing,\nsecurity alerts", color="gray")
    d.box("api", 250, 160, 170, 74, "Notification API", "validate, idempotency key", color="violet")
    d.box("pref", 250, 30, 170, 64, "Preferences", "opt-outs, quiet hours", color="yellow")
    d.box("tmpl", 480, 30, 170, 64, "Templates", "i18n, versions", color="yellow")
    d.box("rl", 250, 300, 170, 64, "Rate limit + dedupe", "per user / type", color="red")
    for i, (ch, prov) in enumerate((("push", "APNs / FCM"), ("email", "SES / SendGrid"), ("sms", "Twilio"), ("in-app", "WS + inbox DB"))):
        d.queue("q%d" % i, 520, 120 + i * 80, 150, 56, ch, size=15)
        d.box("w%d" % i, 720, 120 + i * 80, 150, 56, ch + " workers", color="green", size=15)
        d.box("p%d" % i, 920, 120 + i * 80, 160, 56, prov, color="cyan", size=15)
        d.arrow("api", "q%d" % i)
        d.arrow("q%d" % i, "w%d" % i)
        d.arrow("w%d" % i, "p%d" % i)
    d.arrow("src", "api")
    d.arrow("api", "pref", dashed=True)
    d.arrow("api", "tmpl", dashed=True)
    d.arrow("api", "rl", dashed=True)
    d.box("dlq", 720, 450, 150, 56, "Retry / DLQ", color="red", size=16)
    d.db("log", 920, 440, 160, 80, "Delivery log", "sent/opened")
    d.arrow("w3", "dlq", dashed=True)
    d.arrow("w3", "log", dashed=True)
    return d


def docs():
    d = Diagram("case-google-docs", "Collaborative editor: one session server per doc")
    d.user("a", 20, 40, "Editor A")
    d.user("b", 20, 260, "Editor B")
    d.box("gw", 150, 150, 150, 74, "WS gateway", "route by doc_id", color="violet")
    d.box("sess", 380, 130, 200, 110, "Doc session server", "OT transform or\nCRDT merge,\nassigns revision", color="green")
    d.db("ops", 670, 40, 160, 100, "Op log", "append only")
    d.db("snap", 670, 190, 160, 100, "Snapshots", "every N ops")
    d.box("pres", 380, 300, 200, 64, "Presence / cursors", "ephemeral, Redis", color="red")
    d.box("acl", 670, 330, 160, 64, "ACL service", "viewer/editor", color="yellow")
    d.arrow("a", "gw", label="op @rev 41")
    d.arrow("b", "gw", label="op @rev 41")
    d.arrow("gw", "sess")
    d.arrow("sess", "ops", label="persist rev 42, 43")
    d.arrow("sess", "snap", dashed=True)
    d.arrow("sess", "pres", dashed=True)
    d.arrow("gw", "acl", dashed=True, fs="b", via=[(225, 420), (750, 420)], ts="b")
    return d


def payments():
    d = Diagram("case-payments", "Payment system: idempotent orchestration + ledger")
    d.user("u", 20, 160, "Checkout")
    d.box("ps", 150, 160, 180, 80, "Payment service", "idempotency key,\nstate machine", color="violet")
    d.db("pdb", 150, 320, 180, 100, "Payments DB", "intent, attempts")
    d.box("risk", 450, 30, 170, 64, "Risk / fraud", "score", color="red")
    d.box("rt", 450, 160, 170, 80, "PSP router", "Stripe | Adyen |\nRazorpay", color="orange")
    d.box("psp", 750, 160, 160, 80, "External PSP", "card networks", color="gray")
    d.box("led", 450, 320, 170, 80, "Ledger service", "double entry,\nappend only", color="green")
    d.db("ldb", 750, 320, 160, 100, "Ledger DB", "strongly consistent")
    d.box("wh", 1030, 160, 160, 80, "Webhook handler", "verify signature,\ndedupe event id", color="blue")
    d.box("rec", 1030, 320, 160, 80, "Reconciliation", "daily PSP reports\nvs ledger", color="yellow")
    d.arrow("u", "ps", label="pay(order, key)")
    d.arrow("ps", "pdb")
    d.arrow("ps", "risk")
    d.arrow("ps", "rt")
    d.arrow("rt", "psp", label="authorize/capture")
    d.arrow("psp", "wh", label="async result")
    d.arrow("wh", "ps", dashed=True, fs="t", ts="t", via=[(1110, 125), (240, 125)], label="update status", label_pos=0.5)
    d.arrow("ps", "led", label="post entries")
    d.arrow("led", "ldb")
    d.arrow("rec", "ldb", dashed=True)
    return d


def flash_sale():
    d = Diagram("case-flash-sale", "E-commerce flash sale: protect inventory and the DB")
    d.user("u", 20, 160, "1M shoppers")
    d.box("cdn", 150, 60, 160, 64, "CDN", "static product page", color="cyan")
    d.box("wr", 150, 230, 160, 74, "Waiting room", "token, admit N/s", color="yellow")
    d.box("gw", 380, 230, 150, 74, "API GW", "rate limit per user", color="violet")
    d.box("inv", 650, 90, 190, 80, "Inventory (Redis)", "atomic DECR via Lua\nreserve with TTL", color="red")
    d.queue("q", 650, 270, 190, 64, "order requests")
    d.box("ord", 940, 265, 170, 74, "Order workers", "create order, pay", color="green")
    d.db("db", 940, 70, 170, 110, "Orders + stock DB", "source of truth")
    d.arrow("u", "cdn")
    d.arrow("u", "wr")
    d.arrow("wr", "gw", label="admitted")
    d.arrow("gw", "inv", label="reserve 1")
    d.arrow("gw", "q", label="if reserved")
    d.arrow("q", "ord")
    d.arrow("ord", "db")
    d.arrow("ord", "inv", dashed=True, label="release on\npay failure / TTL", label_pos=0.6)
    return d


def typeahead():
    d = Diagram("case-typeahead", "Typeahead: offline trie build, online top-k lookup")
    d.zone("off", 20, 60, 520, 210, "Offline (hourly / daily)", color="orange")
    d.box("logs", 40, 120, 140, 64, "Query logs", color="gray")
    d.box("agg", 210, 120, 150, 64, "Aggregate", "Spark: counts,\ndecay, filter", color="orange")
    d.box("build", 390, 120, 130, 64, "Build trie", "top-k per node", color="orange")
    d.arrow("logs", "agg")
    d.arrow("agg", "build")
    d.zone("on", 20, 300, 1060, 200, "Online (p99 < 50 ms)", color="blue")
    d.user("u", 40, 360, "User types")
    d.box("cdn", 170, 370, 150, 64, "Browser + CDN", "cache per prefix", color="cyan")
    d.box("svc", 390, 370, 170, 64, "Suggest service", "debounce, personalize", color="blue")
    d.stack("shards", 640, 360, 200, 74, "Trie shards", "by prefix range,\nin memory", color="green")
    d.box("store", 640, 120, 200, 74, "Snapshot store", "versioned tries", color="cyan")
    d.box("trend", 900, 360, 160, 74, "Trending", "stream: recent spikes", color="pink")
    d.arrow("build", "store")
    d.arrow("store", "shards", label="load")
    d.arrow("u", "cdn")
    d.arrow("cdn", "svc")
    d.arrow("svc", "shards")
    d.arrow("trend", "shards", dashed=True)
    return d


def dist_cache():
    d = Diagram("case-distributed-cache", "Distributed cache: client-side routing, replicated shards")
    d.stack("app", 30, 160, 170, 80, "App servers", "client lib: ring", color="blue")
    d.box("cfg", 30, 20, 170, 64, "Config / membership", "etcd / gossip", color="yellow")
    for i in range(3):
        y = 40 + i * 140
        d.box("p%d" % i, 330, y, 170, 64, "Shard %d primary" % (i + 1), "LRU, TTL", color="red")
        d.box("r%d" % i, 600, y, 170, 64, "Shard %d replica" % (i + 1), color="pink")
        d.arrow("app", "p%d" % i)
        d.arrow("p%d" % i, "r%d" % i, dashed=True, label="async" if i == 0 else "")
    d.arrow("cfg", "app", dashed=True, label="node list")
    d.note("n", 830, 100, 250, 200, "hash(key) -> ring -> shard.\nHot keys: local L1 cache,\nkey replication.\nFailover: promote replica,\nring update via config.")
    return d


def crawler():
    d = Diagram("case-web-crawler", "Web crawler: frontier, politeness, dedupe")
    d.box("seed", 20, 40, 140, 56, "Seed URLs", color="gray")
    d.box("front", 220, 30, 200, 80, "URL frontier", "priority queues ->\nper-host queues", color="yellow")
    d.stack("fetch", 500, 30, 180, 80, "Fetchers", "robots.txt, rate per host", color="blue")
    d.box("dns", 760, 40, 150, 56, "DNS cache", color="cyan")
    d.box("parse", 500, 200, 180, 64, "Parser", "HTML -> text, links", color="green")
    d.box("dup", 760, 200, 170, 64, "Content dedupe", "SimHash / hash", color="orange")
    d.box("store", 1000, 200, 150, 64, "Content store", "S3 / Bigtable", color="cyan")
    d.box("ext", 500, 340, 180, 64, "URL extractor", "normalize", color="green")
    d.box("seen", 220, 340, 200, 64, "URL seen?", "Bloom filter + DB", color="red")
    d.arrow("seed", "front")
    d.arrow("front", "fetch")
    d.arrow("fetch", "dns")
    d.arrow("fetch", "parse")
    d.arrow("parse", "dup")
    d.arrow("dup", "store", label="new content")
    d.arrow("parse", "ext")
    d.arrow("ext", "seen")
    d.arrow("seen", "front", label="new URLs")
    return d


def ad_clicks():
    d = Diagram("case-ad-click-aggregator", "Ad click aggregation: real time + batch reconcile")
    d.user("u", 20, 150, "Users")
    d.box("cs", 140, 150, 160, 64, "Click service", "redirect + log", color="blue")
    d.queue("k", 370, 150, 170, 64, "Kafka clicks")
    d.box("fl", 610, 140, 190, 84, "Flink", "dedupe, 1 min tumbling\nwindows per ad_id", color="orange")
    d.db("olap", 880, 130, 170, 110, "OLAP store", "Pinot / ClickHouse")
    d.box("dash", 880, 300, 170, 64, "Advertiser dashboard", color="violet")
    d.box("raw", 370, 300, 170, 64, "Raw log in S3", color="cyan")
    d.box("batch", 610, 300, 190, 64, "Daily batch job", "Spark recompute", color="green")
    d.arrow("u", "cs")
    d.arrow("cs", "k")
    d.arrow("k", "fl")
    d.arrow("fl", "olap", label="aggregates")
    d.arrow("olap", "dash")
    d.arrow("k", "raw", dashed=True)
    d.arrow("raw", "batch")
    d.arrow("batch", "olap", dashed=True, label="reconcile / correct")
    return d


def build():
    return [url_shortener(), twitter_hld(), fanout_models(), instagram(), chat(), chat_receipts(), youtube(),
            uber(), dropbox(), notifications(), docs(), payments(), flash_sale(), typeahead(), dist_cache(),
            crawler(), ad_clicks()]
