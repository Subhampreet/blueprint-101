"""Diagrams for the syllabus-coverage notes: HLD process, networking deep dives,
cloud patterns, LLD topics, extra case studies, GraphQL/WebSocket and the capstone build."""

from sketch import Diagram


# ---------------------------------------------------------------- HLD process

def hld_process():
    d = Diagram("hld-process", "The HLD process: from a vague prompt to a defensible design")
    steps = [("s1", "Scope", "personas, use cases,\nFR + NFR", "blue"), ("s2", "Estimate", "QPS, storage,\nbandwidth", "cyan"),
             ("s3", "Components", "identify the boxes", "green"), ("s4", "Data flow", "how requests and\ndata move", "yellow")]
    for i, (id, l, s, c) in enumerate(steps):
        d.box(id, 30 + i * 240, 90, 190, 84, l, s, color=c)
        if i:
            d.arrow(steps[i - 1][0], id)
    steps2 = [("s5", "Tech stack", "choose per access\npattern", "violet"), ("s6", "Deployment", "regions, AZs,\nclusters", "orange"),
              ("s7", "Scale + resilience", "replicas, shards,\nfailure modes", "pink"), ("s8", "Cost + evolve", "bill, 10x plan", "gray")]
    for i, (id, l, s, c) in enumerate(steps2):
        d.box(id, 750 - i * 240, 260, 190, 84, l, s, color=c)
        if i:
            d.arrow(steps2[i - 1][0], id)
    d.arrow("s4", "s5", fs="b", ts="t")
    d.note("n", 30, 400, 940, 60, "Iterate: a deep dive (step 7) often sends you back to the data model or the tech choice. That is expected.")
    return d


def dfd():
    d = Diagram("data-flow-diagram", "Data flow diagram (level 1): ride booking")
    d.box("rider", 20, 90, 130, 60, "Rider", "external entity", color="white")
    d.box("driver", 20, 300, 130, 60, "Driver", "external entity", color="white")
    d.box("psp", 900, 300, 140, 60, "Payment provider", "external", color="white", size=16)
    d.ellipse("p1", 250, 70, 190, 100, "1.0 Request ride", color="blue", size=16)
    d.ellipse("p2", 520, 180, 190, 100, "2.0 Match driver", color="green", size=16)
    d.ellipse("p3", 250, 290, 190, 100, "3.0 Track trip", color="yellow", size=16)
    d.ellipse("p4", 690, 300, 170, 100, "4.0 Charge fare", color="orange", size=16)
    d.db("d1", 520, 30, 160, 90, "D1 Trips", color="green", size=15)
    d.db("d2", 790, 140, 170, 90, "D2 Driver locations", color="red", size=15)
    d.arrow("rider", "p1", label="pickup, drop")
    d.arrow("p1", "d1", label="trip REQUESTED")
    d.arrow("p1", "p2", label="trip id")
    d.arrow("d2", "p2", label="nearby drivers")
    d.arrow("p2", "driver", label="offer", via=[(610, 420), (85, 420)], ts="b", label_pos=0.6)
    d.arrow("driver", "p3", label="GPS pings")
    d.arrow("p3", "p4", label="distance, time")
    d.arrow("p4", "psp", label="charge")
    return d


def deployment():
    d = Diagram("deployment-architecture", "Deployment architecture: one region, three AZs")
    d.user("u", 20, 170, "Users")
    d.box("cdn", 130, 80, 150, 60, "CDN + WAF", color="cyan")
    d.box("dns", 130, 260, 150, 60, "DNS / GSLB", color="cyan")
    d.zone("region", 330, 30, 760, 430, "Region ap-south-1", color="gray")
    d.box("alb", 360, 190, 150, 64, "Load balancer", "multi-AZ", color="violet")
    for i, az in enumerate(("AZ a", "AZ b", "AZ c")):
        x = 560 + i * 175
        d.zone("az%d" % i, x, 70, 160, 360, az, color="blue")
        d.stack("pods%d" % i, x + 18, 130, 120, 64, "K8s pods", "api, workers", color="blue", size=15)
        d.arrow("alb", "pods%d" % i, via=[(x + 78, 250)], ts="b")
    d.db("pg0", 578, 300, 120, 90, "Postgres", "primary", size=15)
    d.db("pg1", 753, 300, 120, 90, "Postgres", "sync standby", color="gray", size=15)
    d.box("redis", 928, 310, 120, 60, "Redis", "replica set", color="red", size=15)
    d.line("pg0", "pg1", dashed=True, label="sync")
    d.arrow("u", "cdn")
    d.arrow("u", "dns")
    d.arrow("cdn", "alb")
    d.arrow("dns", "alb", dashed=True)
    return d


def comm_patterns():
    d = Diagram("communication-patterns", "Request-response, async messaging, streaming and batch")
    d.zone("rr", 20, 70, 260, 260, "Request-response (sync)", color="blue")
    d.box("a1", 40, 120, 90, 50, "Client", color="white", size=15)
    d.box("b1", 170, 120, 90, 50, "Service", color="blue", size=15)
    d.arrow("a1", "b1", label="call", bend=-25)
    d.arrow("b1", "a1", label="reply", bend=-25, dashed=True)
    d.text("t1", 40, 250, "caller waits;\nsimple, but coupled", size=14)
    d.zone("as", 300, 70, 260, 260, "Async messaging", color="yellow")
    d.box("a2", 320, 120, 90, 50, "Producer", color="white", size=15)
    d.queue("q2", 320, 200, 220, 46, "queue / topic", size=15)
    d.box("b2", 450, 120, 90, 50, "Consumer", color="green", size=15)
    d.arrow("a2", "q2")
    d.arrow("q2", "b2")
    d.text("t2", 320, 270, "fire and forget;\ndecoupled, eventual", size=14)
    d.zone("st", 580, 70, 260, 260, "Streaming", color="green")
    d.box("a3", 600, 120, 220, 46, "events: e1 e2 e3 e4 ...", color="white", size=15)
    d.box("b3", 600, 200, 220, 46, "continuous processing", color="green", size=15)
    d.arrow("a3", "b3")
    d.text("t3", 600, 270, "unbounded, low latency;\nwindows + state", size=14)
    d.zone("bt", 860, 70, 260, 260, "Batch", color="orange")
    d.box("a4", 880, 120, 220, 46, "yesterday's data (bounded)", color="white", size=14)
    d.box("b4", 880, 200, 220, 46, "nightly job", color="orange", size=15)
    d.arrow("a4", "b4")
    d.text("t4", 880, 270, "high throughput,\nminutes to hours late", size=14)
    return d


# ---------------------------------------------------------------- networking deep dives

def subnetting():
    d = Diagram("subnetting-cidr", "Subnetting 10.0.1.0/24 into four /26 subnets")
    d.box("parent", 180, 70, 640, 70, "10.0.1.0/24", "256 addresses, mask 255.255.255.0", color="blue")
    subs = [("10.0.1.0/26", ".0 to .63", "public AZ a"), ("10.0.1.64/26", ".64 to .127", "public AZ b"),
            ("10.0.1.128/26", ".128 to .191", "private AZ a"), ("10.0.1.192/26", ".192 to .255", "private AZ b")]
    for i, (c, r, u) in enumerate(subs):
        d.box("s%d" % i, 20 + i * 250, 220, 220, 84, c, r + "\n" + u, color=("cyan", "cyan", "green", "green")[i], size=17)
        d.arrow("parent", "s%d" % i)
    d.note("n", 20, 350, 970, 74, "Borrow 2 host bits: /24 -> /26 gives 2^2 = 4 subnets of 2^(32-26) = 64 addresses.\nUsable hosts = 64 - 2 (network and broadcast); AWS reserves 5 per subnet, so 59.")
    return d


def bgp():
    d = Diagram("bgp-autonomous-systems", "BGP: autonomous systems exchange reachability")
    d.zone("as1", 20, 70, 300, 260, "AS 64500 (your company)", color="blue")
    d.box("r1", 50, 120, 110, 56, "Edge router", color="blue", size=15)
    d.box("r2", 180, 220, 110, 56, "Edge router", color="blue", size=15)
    d.line("r1", "r2", label="iBGP", dashed=True)
    d.zone("as2", 400, 40, 300, 180, "AS 3356 (transit ISP)", color="orange")
    d.box("t1", 480, 100, 140, 56, "ISP router", color="orange", size=15)
    d.zone("as3", 400, 250, 300, 180, "AS 13335 (CDN)", color="green")
    d.box("t2", 480, 310, 140, 56, "Peer router", color="green", size=15)
    d.zone("as4", 780, 120, 300, 200, "AS 15169 (cloud)", color="violet")
    d.box("t3", 860, 190, 140, 56, "Edge", color="violet", size=15)
    d.arrow("r1", "t1", both=True, label="eBGP")
    d.arrow("r2", "t2", both=True, label="eBGP peering")
    d.arrow("t1", "t3", both=True, label="eBGP")
    d.note("n", 20, 450, 1060, 74, "Advertisement: 'AS 64500 can reach 203.0.113.0/24, path [64500]'. Each AS prepends itself.\nRoute selection: highest local-pref, then shortest AS path, then lowest MED, then eBGP over iBGP, then lowest router id.")
    return d


def tcp_header():
    d = Diagram("tcp-header", "TCP header (20 bytes without options)")
    rows = [
        [("Source port", 16, "blue"), ("Destination port", 16, "blue")],
        [("Sequence number", 32, "green")],
        [("Acknowledgment number", 32, "green")],
        [("Offset", 4, "gray"), ("Rsvd", 4, "gray"), ("Flags", 8, "orange"), ("Window size", 16, "yellow")],
        [("Checksum", 16, "pink"), ("Urgent pointer", 16, "gray")],
        [("Options (MSS, window scale, SACK, timestamps) 0 to 40 bytes", 32, "violet")],
    ]
    W = 900
    for r, row in enumerate(rows):
        x = 40
        for c, (label, bits, col) in enumerate(row):
            w = W * bits / 32
            sub = "%d bits" % bits if w > 100 else ""
            d.box("h%d_%d" % (r, c), x, 80 + r * 62, w - 4, 54, label, sub, color=col, size=15 if w > 200 else 13)
            x += w
    for b, x in ((0, 40), (15, 40 + W * 15 / 32), (16, 40 + W / 2), (31, 40 + W * 31 / 32)):
        d.text("ax%d" % b, x, 56, str(b), size=13, ink="#868e96")
    d.note("fl", 40, 470, 900, 50, "Flags (8 bits): CWR ECE URG ACK PSH RST SYN FIN.  Offset = header length in 32-bit words.")
    return d


def tcp_cwnd():
    d = Diagram("tcp-congestion-window", "TCP congestion window over time (Reno style)")
    d.point("o", 60, 360)
    d.point("xe", 980, 360)
    d.point("ye", 60, 60)
    d.arrow("o", "xe")
    d.arrow("o", "ye")
    d.text("xl", 900, 370, "time (RTTs)", size=14, ink="#495057")
    d.text("yl", 70, 50, "cwnd", size=14, ink="#495057")
    pts = [(60, 350), (120, 340), (170, 310), (210, 250), (240, 170), (300, 150), (360, 130), (420, 110),
           (430, 230), (500, 210), (570, 190), (640, 170), (650, 350), (690, 330), (730, 290), (760, 240), (800, 225), (860, 205), (920, 185)]
    d.point("p0", *pts[0])
    d.point("pn", *pts[-1])
    d.line("p0", "pn", via=pts[1:-1], color="#1971c2")
    d.point("ss1", 60, 240)
    d.point("ss2", 980, 240)
    d.line("ss1", "ss2", dashed=True, color="#e8590c", label="ssthresh", label_pos=0.95)
    d.text("a1", 120, 270, "slow start:\ndoubles per RTT", size=13)
    d.text("a2", 290, 90, "congestion avoidance:\n+1 MSS per RTT", size=13)
    d.text("a3", 440, 250, "3 dup ACKs:\nhalve (fast recovery)", size=13)
    d.text("a4", 660, 120, "timeout:\nback to 1 MSS", size=13)
    return d


def email_flow():
    d = Diagram("email-protocols", "How an email travels: SMTP to send, IMAP/POP3 to read")
    d.user("a", 20, 90, "Alice", "mail app")
    d.box("msa", 160, 100, 150, 64, "Submission", "SMTP 587 + auth", color="blue")
    d.box("mta1", 400, 100, 150, 64, "Sender MTA", "relay", color="blue")
    d.box("dns", 400, 250, 150, 56, "DNS MX lookup", color="cyan", size=16)
    d.box("mta2", 680, 100, 170, 64, "Receiver MTA", "SPF, DKIM, DMARC", color="green")
    d.db("box", 930, 90, 130, 90, "Mailbox", color="green")
    d.user("b", 1180, 90, "Bob", "mail app")
    d.arrow("a", "msa", label="SMTP")
    d.arrow("msa", "mta1")
    d.arrow("mta1", "dns", dashed=True)
    d.arrow("mta1", "mta2", label="SMTP 25 (TLS)")
    d.arrow("mta2", "box", label="deliver")
    d.arrow("b", "box", label="IMAP 993 / POP3 995", label_pos=0.45)
    return d


def troubleshooting():
    d = Diagram("network-troubleshooting-flow", "Troubleshooting 'the site is slow or down'")
    nodes = [("q1", "DNS resolves?", "dig api.example.com"), ("q2", "TCP connects?", "nc -vz host 443"),
             ("q3", "TLS OK?", "openssl s_client"), ("q4", "TTFB fast?", "curl -w timings")]
    for i, (id, l, s) in enumerate(nodes):
        d.diamond(id, 40 + i * 250, 80, 190, 110, l, s, size=15)
        if i:
            d.arrow(nodes[i - 1][0], id, label="yes")
    fixes = [("f1", "Fix DNS: records,\nTTL, resolver", "red"), ("f2", "Firewall / SG,\nroutes, LB health", "red"),
             ("f3", "Cert expiry, SNI,\ncipher mismatch", "red"), ("f4", "Server side: CPU, DB,\nlocks, GC, deps", "orange")]
    for i, (id, l, c) in enumerate(fixes):
        d.box(id, 40 + i * 250, 260, 190, 74, l, color=c, size=15)
        d.arrow(nodes[i][0], id, label="no" if i < 3 else "no: trace it")
    d.box("ok", 1040, 100, 150, 70, "Client side:\npayload, render,\nnetwork path", color="green", size=14)
    d.arrow("q4", "ok", label="yes")
    d.note("n", 40, 380, 1150, 60, "Then check loss and latency per hop (mtr), bandwidth (iperf), and packet captures (tcpdump) for retransmits and resets.")
    return d


def mobile():
    d = Diagram("mobile-networking", "Mobile networking: radio, carrier core, handoffs")
    d.user("p", 20, 150, "Phone", "app")
    d.box("wifi", 150, 60, 150, 60, "Wi-Fi AP", "802.11ax", color="cyan")
    d.box("cell1", 150, 260, 150, 60, "Cell tower A", "5G / LTE", color="blue")
    d.box("cell2", 340, 330, 150, 60, "Cell tower B", "handoff", color="blue")
    d.box("core", 420, 180, 180, 74, "Carrier core", "NAT, IP anchor", color="violet")
    d.cloud("net", 660, 150, 170, 120, "Internet")
    d.box("api", 900, 170, 160, 74, "Your API", "QUIC keeps the\nconnection on IP change", color="green")
    d.arrow("p", "wifi", dashed=True)
    d.arrow("p", "cell1")
    d.arrow("cell1", "cell2", dashed=True, label="moving")
    d.arrow("cell1", "core")
    d.arrow("cell2", "core")
    d.arrow("wifi", "net", via=[(560, 90)])
    d.arrow("core", "net")
    d.arrow("net", "api")
    return d


# ---------------------------------------------------------------- cloud / integration patterns

def claim_check():
    d = Diagram("claim-check-pattern", "Claim check: send a reference, not the payload")
    d.box("prod", 30, 140, 150, 64, "Producer", "50 MB video", color="blue")
    d.box("store", 260, 30, 170, 64, "Object storage", "s3://bucket/vid-77", color="cyan")
    d.queue("q", 300, 170, 230, 60, "queue: {ref: vid-77}", size=15)
    d.box("cons", 620, 140, 150, 64, "Consumer", color="green")
    d.arrow("prod", "store", label="1. upload")
    d.arrow("prod", "q", label="2. tiny message", label_pos=0.4)
    d.arrow("q", "cons", label="3. receive")
    d.arrow("cons", "store", label="4. fetch by ref", dashed=True)
    return d


def competing_consumers():
    d = Diagram("competing-consumers-priority", "Competing consumers with a priority queue")
    d.box("p", 30, 150, 140, 64, "Producers", color="blue")
    d.queue("hi", 250, 80, 200, 56, "high priority", size=15)
    d.queue("lo", 250, 230, 200, 56, "low priority", size=15)
    d.stack("w1", 550, 70, 150, 64, "Workers x 8", "reserved for high", color="green")
    d.stack("w2", 550, 230, 150, 64, "Workers x 4", "low, scale on lag", color="yellow")
    d.arrow("p", "hi", label="OTP, payments")
    d.arrow("p", "lo", label="reports, emails")
    d.arrow("hi", "w1")
    d.arrow("lo", "w2")
    d.arrow("hi", "w2", dashed=True, label="steal when idle", label_pos=0.6)
    d.note("n", 780, 120, 280, 120, "Each message goes to one\nworker. Add workers to scale.\nSeparate pools stop bulk\nwork starving urgent work.")
    return d


def scheduler_agent():
    d = Diagram("scheduler-agent-supervisor", "Scheduler, agent, supervisor")
    d.box("sch", 40, 140, 170, 74, "Scheduler", "plans steps of\na workflow", color="violet")
    d.db("state", 300, 20, 160, 100, "State store", "step, status,\ndeadline")
    d.stack("ag", 300, 220, 170, 74, "Agents", "call remote services", color="blue")
    d.box("sup", 560, 120, 170, 74, "Supervisor", "finds stuck or\nfailed steps", color="orange")
    d.box("ext", 560, 260, 170, 60, "Remote services", color="gray", size=16)
    d.arrow("sch", "state", label="write plan")
    d.arrow("sch", "ag", label="dispatch")
    d.arrow("ag", "state", label="update", fs="t", ts="b")
    d.arrow("ag", "ext")
    d.arrow("sup", "state", label="scan timeouts")
    d.arrow("sup", "sch", label="retry / compensate", via=[(645, 330), (125, 330)], ts="b", dashed=True)
    return d


# ---------------------------------------------------------------- cost

def autoscaling():
    d = Diagram("autoscaling-loop", "Autoscaling control loop")
    d.box("m", 40, 120, 170, 70, "Metrics", "CPU 78%, RPS/pod,\nqueue lag", color="green")
    d.box("pol", 290, 120, 190, 70, "Policy", "target 60% CPU", color="violet")
    d.box("ctl", 560, 120, 170, 70, "Controller", "HPA / ASG", color="blue")
    d.stack("fleet", 810, 115, 170, 74, "Fleet", "6 -> 8 instances", color="blue")
    d.arrow("m", "pol")
    d.arrow("pol", "ctl", label="desired = 8")
    d.arrow("ctl", "fleet", label="scale out")
    d.arrow("fleet", "m", label="new load per instance", via=[(895, 270), (125, 270)], ts="b", dashed=True)
    d.note("n", 290, 300, 440, 74, "Scale out fast, scale in slowly (cooldown).\nScheduled + predictive scaling for known peaks.")
    return d


# ---------------------------------------------------------------- LLD

def er_diagram():
    d = Diagram("er-diagram-ecommerce", "Schema design: an e-commerce core (crow's foot in words)")
    d.box("users", 30, 60, 230, 130, "users", "PK id bigint\nemail citext UNIQUE\ncreated_at timestamptz", color="blue")
    d.box("orders", 360, 60, 260, 150, "orders", "PK id bigint\nFK user_id -> users\nstatus enum, total_cents\nidx (user_id, created_at)", color="yellow")
    d.box("items", 360, 290, 260, 130, "order_items", "PK (order_id, line_no)\nFK product_id\nqty int CHECK > 0\nprice_cents (snapshot)", color="orange")
    d.box("products", 30, 290, 230, 130, "products", "PK id bigint\nsku UNIQUE\nprice_cents, attrs jsonb", color="green")
    d.box("pay", 720, 60, 250, 130, "payments", "PK id\nFK order_id\nidempotency_key UNIQUE\nstatus, amount_cents", color="pink")
    d.arrow("users", "orders", label="1 to many")
    d.arrow("orders", "items", label="1 to many")
    d.arrow("products", "items", label="1 to many")
    d.arrow("orders", "pay", label="1 to many (retries)")
    return d


def pagination():
    d = Diagram("pagination-offset-vs-keyset", "Offset vs keyset (cursor) pagination")
    d.zone("off", 20, 70, 500, 300, "OFFSET 100000 LIMIT 20", color="red")
    d.box("o1", 50, 120, 440, 60, "DB reads and throws away 100,000 rows", color="red", size=16)
    d.box("o2", 50, 200, 440, 60, "new rows shift pages: duplicates / skips", color="red", size=16)
    d.text("ot", 50, 300, "page 5,000 is slow; fine for small admin tables", size=14)
    d.zone("ks", 560, 70, 520, 300, "WHERE (created_at, id) < (cursor) LIMIT 20", color="green")
    d.box("k1", 590, 120, 460, 60, "index seek straight to the cursor position", color="green", size=16)
    d.box("k2", 590, 200, 460, 60, "stable under inserts; constant time per page", color="green", size=16)
    d.text("kt", 590, 300, "cursor = base64({created_at, id}); no jump to page N", size=14)
    return d


def testing_pyramid():
    d = Diagram("testing-pyramid", "The testing pyramid (and what sits beside it)")
    layers = [("e2e", "End-to-end / UI", "few, slow, brittle", 220, "red"), ("int", "Integration + contract", "real DB, broker, API contracts", 380, "orange"),
              ("comp", "Component / service", "one service, fakes for neighbours", 540, "yellow"), ("unit", "Unit", "many, fast, isolated", 700, "green")]
    y = 70
    for id, l, s, w, c in layers:
        d.box(id, 400 - w / 2, y, w, 70, l, s, color=c)
        y += 82
    d.note("side", 780, 90, 300, 250, "Beside the pyramid:\n- performance + load tests\n- stress + soak tests\n- chaos experiments\n- security scans (SAST, deps)\n- canary analysis in prod\n\nRun fast tests on every commit,\nslow ones before deploy.")
    return d


def memory_hierarchy():
    d = Diagram("memory-hierarchy", "Memory hierarchy: why data locality matters")
    levels = [("reg", "Registers", "< 1 ns", 160, "violet"), ("l1", "L1 cache (64 KB)", "1 ns", 260, "blue"),
              ("l2", "L2 cache (1 MB)", "4 ns", 360, "cyan"), ("l3", "L3 cache (32 MB)", "15 ns", 460, "green"),
              ("ram", "RAM (64 GB)", "100 ns", 560, "yellow"), ("ssd", "NVMe SSD", "20 to 100 µs", 660, "orange"), ("net", "Network / other DC", "0.5 to 150 ms", 760, "red")]
    y = 60
    for id, l, s, w, c in levels:
        d.box(id, 450 - w / 2, y, w, 52, l + "   " + s, color=c, size=16)
        y += 62
    d.note("n", 880, 120, 230, 220, "Sequential access and\ncompact structs keep data\nin cache lines (64 bytes).\nPointer chasing (linked\nlists, maps of objects)\nmisses cache.")
    return d


def error_tracking():
    d = Diagram("error-tracking-flow", "From a crash to a fix: error tracking and debugging")
    d.box("app", 30, 130, 160, 70, "App / browser", "exception", color="blue")
    d.box("sdk", 250, 130, 170, 70, "Tracking SDK", "stack, breadcrumbs,\nrelease, user", color="violet")
    d.box("svc", 480, 130, 180, 70, "Error tracker", "group by fingerprint", color="orange")
    d.box("sm", 480, 20, 180, 60, "Source maps / symbols", color="gray", size=15)
    d.box("alert", 720, 60, 170, 60, "Alert + issue", "new or regressed", color="red", size=15)
    d.box("trace", 720, 200, 170, 60, "Logs + trace", "via trace_id", color="green", size=15)
    d.arrow("app", "sdk")
    d.arrow("sdk", "svc")
    d.arrow("sm", "svc", label="de-minify")
    d.arrow("svc", "alert")
    d.arrow("svc", "trace", label="jump to context")
    return d


# ---------------------------------------------------------------- case studies

def auth_system():
    d = Diagram("case-auth-system", "Authentication system: login, tokens, sessions")
    d.user("u", 20, 150, "User", "web / mobile")
    d.box("gw", 150, 150, 150, 70, "API gateway", "verifies JWT\n(JWKS cached)", color="violet")
    d.box("idp", 380, 40, 190, 80, "Auth service", "OIDC / OAuth 2.1\nlogin, MFA, passkeys", color="blue")
    d.db("udb", 650, 20, 150, 100, "Users + creds", "argon2id hashes")
    d.box("tok", 380, 180, 190, 70, "Token service", "sign RS256, rotate keys", color="green")
    d.box("sess", 650, 170, 150, 70, "Session store", "refresh tokens,\nrevocations (Redis)", color="red")
    d.box("kms", 870, 180, 150, 56, "KMS / HSM", "signing keys", color="gray", size=16)
    d.box("risk", 650, 300, 150, 60, "Risk engine", "rate limit, bot score", color="orange", size=15)
    d.stack("svc", 150, 300, 150, 64, "Services", color="blue")
    d.arrow("u", "gw")
    d.arrow("gw", "idp", label="/login")
    d.arrow("idp", "udb")
    d.arrow("idp", "tok")
    d.arrow("tok", "sess")
    d.arrow("tok", "kms", dashed=True)
    d.arrow("idp", "risk", dashed=True, via=[(475, 330)])
    d.arrow("gw", "svc", label="user id in header")
    return d


def recommendation():
    d = Diagram("case-recommendation-engine", "Recommendation engine: offline training, online serving")
    d.zone("off", 20, 60, 520, 330, "Offline (hours / daily)", color="orange")
    d.box("logs", 40, 110, 140, 60, "Interaction logs", color="gray", size=15)
    d.box("feat", 210, 110, 140, 60, "Feature jobs", color="orange", size=16)
    d.box("train", 380, 110, 140, 60, "Train models", "two-tower, ranker", color="orange", size=15)
    d.box("emb", 210, 250, 140, 60, "Item embeddings", color="cyan", size=15)
    d.box("ann", 380, 250, 140, 60, "ANN index", "HNSW / ScaNN", color="cyan", size=15)
    d.arrow("logs", "feat")
    d.arrow("feat", "train")
    d.arrow("train", "emb", label="export")
    d.arrow("emb", "ann")
    d.zone("on", 580, 60, 520, 330, "Online (< 100 ms)", color="blue")
    d.user("u", 600, 230, "User")
    d.box("cand", 720, 100, 160, 64, "Candidates", "ANN + co-visit\n+ trending", color="blue", size=15)
    d.box("fs", 920, 100, 160, 64, "Feature store", "online", color="red", size=15)
    d.box("rank", 720, 230, 160, 64, "Ranker", "GPU / CPU model", color="violet", size=15)
    d.box("rr", 920, 230, 160, 64, "Re-rank + filter", "diversity, rules", color="green", size=15)
    d.arrow("u", "cand")
    d.arrow("cand", "rank")
    d.arrow("fs", "rank", dashed=True)
    d.arrow("rank", "rr")
    d.arrow("ann", "cand", label="nearest items", via=[(560, 280), (560, 132)], ts="l", dashed=True)
    return d


def ad_server():
    d = Diagram("case-ad-server", "Ad serving: select, auction, pace, track (all in ~100 ms)")
    d.user("u", 20, 150, "Page / app", "ad slot")
    d.box("as", 150, 150, 160, 70, "Ad server", "request: user, slot,\ncontext", color="violet")
    d.box("tgt", 380, 40, 180, 70, "Targeting index", "inverted index on\ngeo, interest, device", color="blue")
    d.box("pred", 380, 160, 180, 70, "pCTR / pCVR model", "score candidates", color="orange")
    d.box("auc", 620, 160, 170, 70, "Auction", "bid x pCTR,\nsecond price", color="yellow")
    d.box("pace", 620, 40, 170, 70, "Budget pacing", "spend vs plan,\nfrequency caps", color="red")
    d.box("ev", 850, 160, 170, 70, "Impression + click\ntracking", color="green", size=15)
    d.queue("k", 850, 290, 170, 56, "Kafka events", size=15)
    d.box("bill", 620, 290, 170, 56, "Billing + reports", color="gray", size=15)
    d.arrow("u", "as")
    d.arrow("as", "tgt", label="candidates")
    d.arrow("as", "pred")
    d.arrow("pred", "auc")
    d.arrow("pace", "auc", label="eligible?", dashed=True)
    d.arrow("auc", "ev", label="winner")
    d.arrow("ev", "k")
    d.arrow("k", "bill")
    d.arrow("k", "pace", label="spend updates", via=[(1060, 318), (1060, 75)], ts="r", dashed=True, label_pos=0.6)
    return d


def search_engine():
    d = Diagram("case-search-engine", "Web search engine: crawl, index, serve")
    d.box("crawl", 20, 80, 150, 64, "Crawler", "frontier, fetchers", color="gray")
    d.box("parse", 210, 80, 150, 64, "Parse + dedupe", color="orange", size=16)
    d.box("idx", 400, 80, 170, 64, "Indexer", "tokens -> postings", color="orange")
    d.box("rank0", 210, 200, 150, 64, "Link graph", "PageRank, quality", color="yellow")
    d.stack("shards", 620, 70, 180, 80, "Index shards", "doc-partitioned,\nreplicated", color="green")
    d.user("u", 1010, 210, "Searcher")
    d.box("qp", 840, 200, 150, 70, "Query service", "spell, synonyms,\ncache", color="violet")
    d.box("l2", 620, 260, 180, 70, "Rank stage 2", "learned ranker\non top 1,000", color="blue")
    d.arrow("crawl", "parse")
    d.arrow("parse", "idx")
    d.arrow("parse", "rank0", dashed=True)
    d.arrow("rank0", "idx", dashed=True, label="static score")
    d.arrow("idx", "shards")
    d.arrow("u", "qp")
    d.arrow("qp", "shards", label="scatter")
    d.arrow("shards", "l2", label="gather top k")
    d.arrow("l2", "qp", label="results")
    return d


# ---------------------------------------------------------------- GraphQL / WebSocket

def graphql_federation():
    d = Diagram("graphql-federation", "GraphQL federation with DataLoader batching")
    d.user("c", 20, 150, "Client", "one query")
    d.box("router", 160, 140, 190, 84, "GraphQL router", "query plan, auth,\ncomplexity limit", color="violet")
    d.box("u", 440, 40, 170, 64, "Users subgraph", color="blue")
    d.box("o", 440, 160, 170, 64, "Orders subgraph", color="blue")
    d.box("p", 440, 280, 170, 64, "Products subgraph", color="blue")
    d.box("dl", 690, 280, 190, 70, "DataLoader", "collect ids in a tick,\none batched query", color="yellow")
    d.db("pdb", 1030, 270, 130, 90, "Products DB")
    d.arrow("c", "router")
    d.arrow("router", "u")
    d.arrow("router", "o")
    d.arrow("router", "p")
    d.arrow("p", "dl")
    d.arrow("dl", "pdb", label="WHERE id IN (...)")
    d.note("n", 690, 60, 390, 120, "Without DataLoader: 1 query for orders\n+ N queries for their products (N+1).\nWith it: 1 + 1.")
    return d


def websocket_frames():
    d = Diagram("websocket-handshake-rooms", "WebSocket: upgrade handshake, frames and rooms")
    d.lifeline("c", 90, 60, 330, "Client", color="blue")
    d.lifeline("s", 570, 60, 330, "Server", color="green")
    d.msg(90, 570, 150, "GET /ws  Upgrade: websocket, Sec-WebSocket-Key", "m1")
    d.msg(570, 90, 200, "101 Switching Protocols, Sec-WebSocket-Accept", "m2", dashed=True)
    d.msg(90, 570, 260, "text frame (opcode 0x1, masked)", "m3", color="#1971c2")
    d.msg(570, 90, 310, "text frame / ping (0x9)", "m4", dashed=True, color="#2f9e44")
    d.msg(90, 570, 360, "pong (0xA), close (0x8)", "m5")
    d.zone("rooms", 700, 60, 450, 330, "Rooms over pub/sub", color="violet")
    d.box("g1", 730, 110, 160, 56, "Gateway 1", "room:42 x 3 sockets", color="blue", size=14)
    d.box("g2", 730, 300, 160, 56, "Gateway 2", "room:42 x 5 sockets", color="blue", size=14)
    d.queue("ps", 940, 200, 190, 56, "channel room:42", size=14)
    d.arrow("g1", "ps", label="publish")
    d.arrow("ps", "g2", label="fan out")
    return d


# ---------------------------------------------------------------- capstone build

def mini_shortener():
    d = Diagram("build-mini-shortener", "Capstone build: a mini URL shortener in one Python file")
    d.user("c", 20, 140, "curl / browser")
    d.box("http", 170, 140, 160, 70, "HTTP server", "stdlib http.server", color="violet")
    d.box("rl", 400, 40, 170, 64, "Token bucket", "per client IP", color="red")
    d.box("svc", 400, 150, 170, 64, "Shortener", "base62 + scramble", color="blue")
    d.box("cache", 650, 40, 160, 64, "LRU cache", "code -> URL", color="red")
    d.db("db", 650, 150, 160, 100, "SQLite", "WAL mode")
    d.box("met", 400, 290, 170, 60, "/metrics", "hits, misses, p99", color="green")
    d.arrow("c", "http")
    d.arrow("http", "rl", label="allow?")
    d.arrow("http", "svc")
    d.arrow("svc", "cache")
    d.arrow("svc", "db")
    d.arrow("http", "met", dashed=True)
    return d


def build():
    return [hld_process(), dfd(), deployment(), comm_patterns(), subnetting(), bgp(), tcp_header(), tcp_cwnd(),
            email_flow(), troubleshooting(), mobile(), claim_check(), competing_consumers(), scheduler_agent(),
            autoscaling(), er_diagram(), pagination(), testing_pyramid(), memory_hierarchy(), error_tracking(),
            auth_system(), recommendation(), ad_server(), search_engine(), graphql_federation(), websocket_frames(),
            mini_shortener()]
