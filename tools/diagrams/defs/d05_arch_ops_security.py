from sketch import Diagram


# ---------------------------------------------------------------- architecture

def monolith_vs_micro():
    d = Diagram("monolith-vs-microservices", "Monolith vs microservices")
    d.zone("m", 20, 70, 380, 330, "Monolith: one deployable", color="orange")
    d.box("mono", 60, 120, 300, 180, "App", "users | catalog | orders\npayments | notifications\nshared memory calls", color="orange")
    d.db("mdb", 140, 310, 140, 80, "One DB", color="green")
    d.arrow("mono", "mdb")
    d.zone("ms", 440, 70, 660, 420, "Microservices: independently deployable", color="blue")
    d.box("gw", 470, 210, 120, 60, "Gateway", color="violet")
    svcs = [("u", "Users", 150), ("o", "Orders", 240), ("p", "Payments", 330)]
    for id, l, y in svcs:
        d.box(id, 650, y - 25, 140, 54, l, color="blue")
        d.db(id + "db", 840, y - 32, 100, 70, l[:-1] + " DB", color="green", size=14)
        d.arrow("gw", id)
        d.arrow(id, id + "db")
    d.queue("bus", 640, 420, 300, 50, "event bus (Kafka)", size=15)
    d.arrow("p", "bus", dashed=True, label="PaymentDone")
    return d


def service_discovery():
    d = Diagram("service-discovery", "Client-side vs server-side service discovery")
    d.zone("c", 20, 70, 500, 300, "Client-side (Eureka, Consul, gRPC xDS)", color="blue")
    d.box("ca", 40, 170, 130, 64, "Service A", "LB library", color="blue")
    d.box("reg", 230, 100, 160, 64, "Registry", "Consul / Eureka", color="yellow")
    d.stack("cb", 260, 240, 140, 64, "Service B", color="green")
    d.arrow("ca", "reg", label="1. lookup B")
    d.arrow("ca", "cb", label="2. call an instance")
    d.arrow("cb", "reg", dashed=True, label="register +\nheartbeat")
    d.zone("s", 560, 70, 540, 300, "Server-side (K8s Service, ALB, mesh)", color="violet")
    d.box("sa", 580, 170, 130, 64, "Service A", color="blue")
    d.box("lb", 770, 170, 140, 64, "LB / proxy", "b.svc.cluster.local", color="violet")
    d.stack("sb", 960, 170, 120, 64, "Service B", color="green")
    d.box("reg2", 770, 290, 140, 56, "Registry", "kube API / etcd", color="yellow", size=16)
    d.arrow("sa", "lb")
    d.arrow("lb", "sb")
    d.arrow("reg2", "lb", dashed=True, label="endpoints")
    return d


def service_mesh():
    d = Diagram("service-mesh", "Service mesh: sidecar proxies + control plane")
    d.box("cp", 330, 40, 260, 70, "Control plane", "Istiod: config, certs, policy", color="violet")
    for i, (x, name) in enumerate(((60, "Orders"), (380, "Payments"), (700, "Inventory"))):
        d.zone("pod%d" % i, x, 170, 260, 150, "pod", color="gray")
        d.box("app%d" % i, x + 20, 220, 110, 70, name, "app", color="blue")
        d.box("sc%d" % i, x + 140, 220, 100, 70, "Envoy", "sidecar", color="orange")
        d.line("app%d" % i, "sc%d" % i, label="localhost", size=12)
        d.arrow("cp", "sc%d" % i, dashed=True)
    d.arrow("sc0", "app1", label="mTLS, retries,\ntimeouts", fs="b", ts="b", via=[(250, 360), (435, 360)])
    d.arrow("sc1", "app2", label="metrics + traces", fs="b", ts="b", via=[(570, 360), (755, 360)])
    return d


def strangler():
    d = Diagram("strangler-fig", "Strangler fig migration")
    d.user("u", 30, 140, "Clients")
    d.box("proxy", 170, 140, 160, 74, "Routing facade", "gateway / proxy", color="violet")
    d.box("legacy", 430, 60, 210, 90, "Legacy monolith", "shrinking", color="gray")
    d.box("new1", 430, 200, 210, 60, "New: Catalog svc", color="green")
    d.box("new2", 430, 280, 210, 60, "New: Checkout svc", color="green")
    d.arrow("u", "proxy")
    d.arrow("proxy", "legacy", label="everything else")
    d.arrow("proxy", "new1", label="/catalog/*")
    d.arrow("proxy", "new2", label="/checkout/*")
    d.note("n", 700, 90, 300, 160, "Move one capability at a time.\nShadow traffic, compare results,\nflip the route, keep rollback.\nData: CDC from legacy DB until\nthe new service owns it.")
    return d


def cqrs():
    d = Diagram("cqrs", "CQRS: separate write model and read models")
    d.user("u", 30, 160, "Client")
    d.box("cmd", 170, 70, 170, 70, "Command API", "PlaceOrder, Cancel", color="orange")
    d.box("qry", 170, 270, 170, 70, "Query API", "GET order views", color="blue")
    d.box("dom", 400, 70, 170, 70, "Domain model", "validates invariants", color="orange")
    d.db("wdb", 640, 50, 140, 110, "Write DB", "normalized", color="orange")
    d.queue("ev", 640, 200, 160, 60, "events / CDC")
    d.box("proj", 860, 190, 150, 80, "Projector", "updates views", color="violet")
    d.db("rdb", 400, 250, 170, 110, "Read stores", "denormalized:\nSQL view, Elastic,\nRedis", color="blue")
    d.arrow("u", "cmd")
    d.arrow("u", "qry")
    d.arrow("cmd", "dom")
    d.arrow("dom", "wdb")
    d.arrow("wdb", "ev")
    d.arrow("ev", "proj")
    d.arrow("proj", "rdb", via=[(935, 330)], label="eventually consistent", label_pos=0.6)
    d.arrow("qry", "rdb")
    return d


def event_sourcing():
    d = Diagram("event-sourcing", "Event sourcing: the log is the source of truth")
    d.box("cmd", 40, 140, 160, 64, "Command", "Withdraw 30", color="orange")
    d.box("agg", 260, 140, 170, 64, "Account aggregate", "rebuilt from events", color="blue")
    d.zone("es", 490, 60, 380, 250, "Event store (append only, account 42)", color="yellow")
    evs = ["1 AccountOpened", "2 Deposited 100", "3 Withdrawn 20", "4 Withdrawn 30  (new)"]
    for i, e in enumerate(evs):
        d.box("e%d" % i, 515, 100 + i * 50, 330, 40, e, color="white" if i < 3 else "green", size=15)
    d.box("snap", 515, 320, 330, 46, "snapshot @ v3: balance 80", color="cyan", size=15)
    d.arrow("cmd", "agg")
    d.arrow("agg", "e3", label="append if version = 3", label_pos=0.4)
    d.arrow("e0", "agg", dashed=True, label="replay", fs="l", ts="t", via=[(345, 120)])
    d.box("p1", 940, 90, 160, 56, "Balance view", color="violet")
    d.box("p2", 940, 180, 160, 56, "Audit / fraud", color="violet")
    d.box("p3", 940, 270, 160, 56, "Analytics", color="violet")
    for p in ("p1", "p2", "p3"):
        d.arrow("es", p, dashed=True)
    return d


def hexagonal():
    d = Diagram("hexagonal-architecture", "Hexagonal architecture (ports and adapters)")
    d.ellipse("outer", 230, 70, 520, 380, "", color="none")
    d.ellipse("core", 360, 170, 260, 180, "Domain core", "entities, use cases,\nno framework imports", color="yellow")
    d.box("pin", 300, 110, 130, 50, "port: OrderUseCase", color="green", size=13)
    d.box("pout", 560, 360, 150, 50, "port: OrderRepository", color="green", size=13)
    d.box("pout2", 560, 110, 150, 50, "port: PaymentGateway", color="green", size=13)
    d.box("rest", 30, 90, 160, 56, "REST controller", "driving adapter", color="blue")
    d.box("cli", 30, 200, 160, 56, "CLI / tests", "driving adapter", color="blue")
    d.box("kafka", 30, 310, 160, 56, "Kafka consumer", "driving adapter", color="blue")
    d.box("pg", 790, 360, 170, 56, "Postgres adapter", "driven adapter", color="orange")
    d.box("stripe", 790, 90, 170, 56, "Stripe adapter", "driven adapter", color="orange")
    d.box("fake", 790, 230, 170, 56, "In-memory fake", "for unit tests", color="orange")
    d.arrow("rest", "pin")
    d.arrow("cli", "pin")
    d.arrow("kafka", "core")
    d.arrow("pout", "pg", dashed=True, label="implements", label_pos=0.6)
    d.arrow("pout2", "stripe", dashed=True)
    d.arrow("pout", "fake", dashed=True)
    return d


def serverless():
    d = Diagram("serverless", "Serverless: event driven functions on managed services")
    d.user("u", 30, 70, "Client")
    d.box("gw", 160, 80, 150, 60, "API Gateway", color="violet")
    d.box("fn1", 380, 80, 160, 60, "Function", "create order", color="orange")
    d.db("ddb", 620, 60, 140, 100, "DynamoDB", "on demand")
    d.box("s3", 160, 250, 150, 60, "S3 upload", color="cyan")
    d.box("fn2", 380, 250, 160, 60, "Function", "make thumbnails", color="orange")
    d.queue("q", 620, 250, 160, 60, "SQS")
    d.box("fn3", 850, 250, 160, 60, "Function", "send email", color="orange")
    d.arrow("u", "gw")
    d.arrow("gw", "fn1")
    d.arrow("fn1", "ddb")
    d.arrow("s3", "fn2", label="ObjectCreated")
    d.arrow("fn2", "q")
    d.arrow("q", "fn3", label="batch of 10")
    d.note("n", 830, 50, 260, 120, "Pay per invocation,\nscale to zero, no servers.\nWatch: cold starts, 15 min\nlimit, DB connections.")
    return d


# ---------------------------------------------------------------- reliability

def circuit_breaker():
    d = Diagram("circuit-breaker", "Circuit breaker state machine")
    d.ellipse("closed", 60, 160, 200, 110, "CLOSED", "calls flow,\ncount failures", color="green")
    d.ellipse("open", 460, 40, 200, 110, "OPEN", "fail fast /\nfallback", color="red")
    d.ellipse("half", 460, 280, 200, 110, "HALF-OPEN", "allow a few\ntrial calls", color="yellow")
    d.arrow("closed", "open", label="failure rate > 50%\nin last 20 calls")
    d.arrow("open", "half", label="after 30 s\ncooldown", bend=-70)
    d.arrow("half", "closed", label="trials succeed")
    d.arrow("half", "open", label="trial fails", bend=-70)
    d.note("n", 780, 130, 300, 160, "Protects the caller (threads,\nlatency) and gives the failing\ndependency room to recover.\nPair with timeouts, retries\nwith jitter, and fallbacks.")
    return d


def bulkhead():
    d = Diagram("bulkhead", "Bulkheads: isolate resources per dependency")
    d.zone("svc", 20, 70, 300, 320, "Service instance", color="blue")
    rows = [("payments", "20 threads", "green", "Payments API", "healthy"),
            ("search", "10 threads, ALL BUSY", "red", "Search API", "slow (5 s)"),
            ("profile", "10 threads", "green", "Profile API", "healthy")]
    for i, (name, sub, col, dep, dsub) in enumerate(rows):
        y = 120 + i * 90
        d.box("p%d" % i, 50, y, 240, 64, "Pool: " + name, sub, color=col)
        d.box("d%d" % i, 480, y, 180, 64, dep, dsub, color=col)
        d.arrow("p%d" % i, "d%d" % i, color="#e03131" if col == "red" else None)
    d.note("n", 720, 140, 330, 150, "A slow search dependency can\nexhaust only its own pool.\nCheckout and profile keep working.\nSame idea: separate connection\npools, queues, even clusters (cells).")
    return d


def retry_backoff():
    d = Diagram("retry-backoff-jitter", "Retries: exponential backoff with jitter")
    d.zone("a", 20, 70, 520, 270, "No jitter: synchronized retry storms", color="red")
    for k, x in enumerate((60, 160, 320)):
        d.stack("ra%d" % k, x, 160, 70, 60, "1000", color="red", size=15)
    d.text("ta", 60, 250, "t=1s          t=2s                  t=4s\nevery client retries at the same instant", size=14)
    d.zone("b", 580, 70, 520, 270, "Full jitter: retries spread out", color="green")
    xs = [610, 650, 700, 760, 810, 880, 930, 1000, 1040]
    for k, x in enumerate(xs):
        d.box("rb%d" % k, x, 160 + (k % 3) * 22, 36, 40, "", color="green")
    d.text("tb", 610, 250, "sleep = random(0, min(cap, base * 2^attempt))", size=14)
    d.note("n", 200, 370, 720, 74, "Retry only idempotent or idempotency-keyed calls, cap attempts (3 to 5),\nuse a retry budget (e.g. retries <= 10% of requests), honour Retry-After.")
    return d


def observability():
    d = Diagram("observability-pipeline", "Observability: metrics, logs, traces")
    d.stack("svc", 30, 160, 150, 80, "Services", "OpenTelemetry SDK", color="blue")
    d.box("col", 260, 160, 170, 80, "OTel Collector", "sample, enrich,\nbatch, route", color="violet")
    d.box("m", 520, 60, 200, 64, "Metrics", "Prometheus / Mimir", color="green")
    d.box("l", 520, 170, 200, 64, "Logs", "Loki / Elasticsearch", color="yellow")
    d.box("t", 520, 280, 200, 64, "Traces", "Tempo / Jaeger", color="orange")
    d.box("g", 800, 120, 170, 64, "Dashboards", "Grafana", color="cyan")
    d.box("al", 800, 240, 170, 64, "Alerting", "SLO burn -> pager", color="red")
    d.arrow("svc", "col")
    d.arrow("col", "m")
    d.arrow("col", "l")
    d.arrow("col", "t")
    d.arrow("m", "g")
    d.arrow("l", "g")
    d.arrow("t", "g")
    d.arrow("m", "al")
    d.note("n", 30, 300, 420, 90, "Correlate everything with trace_id:\nlog lines carry it, metrics carry exemplars,\ntraces link to logs.")
    return d


def trace_waterfall():
    d = Diagram("trace-waterfall", "One distributed trace (spans as a waterfall)")
    spans = [
        ("GET /checkout (gateway)", 0, 640, 0, "violet"),
        ("auth.verify", 20, 60, 1, "blue"),
        ("cart.get", 90, 120, 1, "blue"),
        ("redis GET cart:42", 100, 30, 2, "red"),
        ("pricing.quote", 220, 260, 1, "orange"),
        ("postgres SELECT promos", 240, 210, 2, "green"),
        ("payment.authorize", 490, 140, 1, "yellow"),
    ]
    for i, (name, start, dur, depth, col) in enumerate(spans):
        d.box("s%d" % i, 260 + start, 80 + i * 52, max(dur, 30), 40, "", color=col)
        d.text("n%d" % i, 30 + depth * 20, 88 + i * 52, name, size=15)
    for k in range(5):
        d.text("ax%d" % k, 260 + k * 160, 448, "%d ms" % (k * 100), size=14, ink="#868e96", align="center")
    d.note("n", 260, 490, 420, 70, "pricing waits on a slow promo query:\nthat is where to optimize.")
    return d


def multi_region():
    d = Diagram("multi-region", "Multi-region: active-passive vs active-active")
    d.zone("ap", 20, 70, 520, 330, "Active-passive (warm standby)", color="orange")
    d.box("gd1", 180, 100, 180, 56, "DNS / GSLB", color="cyan")
    d.zone("r1", 40, 190, 220, 190, "us-east (active)", color="green")
    d.box("a1", 70, 230, 160, 50, "App fleet", color="blue", size=16)
    d.db("d1", 90, 295, 120, 75, "Primary", size=15)
    d.zone("r2", 300, 190, 220, 190, "us-west (standby)", color="gray")
    d.box("a2", 330, 230, 160, 50, "Scaled down", color="gray", size=16)
    d.db("d2", 350, 295, 120, 75, "Replica", color="gray", size=15)
    d.arrow("gd1", "a1")
    d.arrow("gd1", "a2", dashed=True, label="on failover", label_pos=0.35)
    d.arrow("d1", "d2", dashed=True, label="async")
    d.zone("aa", 580, 70, 520, 330, "Active-active", color="green")
    d.box("gd2", 750, 100, 180, 56, "Anycast / GSLB", color="cyan")
    d.zone("r3", 600, 190, 220, 190, "eu-west", color="green")
    d.box("a3", 630, 230, 160, 50, "App fleet", color="blue", size=16)
    d.db("d3", 650, 295, 120, 75, "Local DB", size=15)
    d.zone("r4", 860, 190, 220, 190, "ap-south", color="green")
    d.box("a4", 890, 230, 160, 50, "App fleet", color="blue", size=16)
    d.db("d4", 910, 295, 120, 75, "Local DB", size=15)
    d.arrow("gd2", "a3")
    d.arrow("gd2", "a4")
    d.arrow("d3", "d4", both=True, label="replicate,\nresolve conflicts")
    return d


def deploy_strategies():
    d = Diagram("deployment-strategies", "Blue-green vs canary vs rolling")
    d.zone("bg", 20, 70, 340, 300, "Blue-green", color="blue")
    d.box("lb1", 110, 110, 160, 50, "Router", color="violet", size=16)
    d.stack("blue", 40, 230, 120, 60, "Blue v1", "idle", color="blue", size=16)
    d.stack("green", 210, 230, 120, 60, "Green v2", "live", color="green", size=16)
    d.arrow("lb1", "green", label="100%")
    d.arrow("lb1", "blue", dashed=True, label="rollback")
    d.zone("cn", 390, 70, 340, 300, "Canary", color="orange")
    d.box("lb2", 480, 110, 160, 50, "Router", color="violet", size=16)
    d.stack("v1", 410, 230, 120, 60, "v1", "95%", color="blue", size=16)
    d.box("v2", 590, 230, 120, 60, "v2 canary", "5%, watch SLOs", color="orange", size=16)
    d.arrow("lb2", "v1", label="95%")
    d.arrow("lb2", "v2", label="5%")
    d.zone("rl", 760, 70, 340, 300, "Rolling", color="green")
    for i in range(4):
        d.box("r%d" % i, 790 + (i % 2) * 150, 120 + (i // 2) * 90, 130, 60, "pod %d" % (i + 1), "v2" if i < 2 else "v1",
              color="green" if i < 2 else "blue", size=16)
    d.text("rt", 790, 310, "replace a batch at a time\n(maxSurge / maxUnavailable)", size=14)
    return d


# ---------------------------------------------------------------- security

def oauth_pkce():
    d = Diagram("oauth-auth-code-pkce", "OAuth 2.0 authorization code flow with PKCE")
    d.lifeline("u", 110, 60, 560, "User + browser", color="white", w=150)
    d.lifeline("app", 470, 60, 560, "Client app", color="blue")
    d.lifeline("as", 850, 60, 560, "Auth server", color="violet")
    d.lifeline("api", 1200, 60, 560, "Resource API", color="green")
    d.msg(110, 470, 140, "1. click Login", "m1")
    d.msg(470, 850, 190, "2. redirect /authorize + code_challenge", "m2")
    d.msg(850, 110, 240, "3. login page, MFA, consent", "m3", dashed=True)
    d.msg(110, 850, 290, "4. credentials + approve", "m4")
    d.msg(850, 470, 340, "5. redirect back with ?code=abc", "m5", dashed=True)
    d.msg(470, 850, 400, "6. POST /token  code + code_verifier", "m6")
    d.msg(850, 470, 450, "7. access_token (+ refresh, id_token)", "m7", dashed=True)
    d.msg(470, 1200, 520, "8. GET /data  Authorization: Bearer", "m8", color="#2f9e44")
    d.msg(1200, 470, 570, "9. 200 data", "m9", dashed=True, color="#2f9e44")
    return d


def jwt_structure():
    d = Diagram("jwt-structure", "JWT: header.payload.signature")
    d.box("h", 40, 100, 260, 130, "Header", '{ "alg": "RS256",\n  "kid": "key-2024-06" }', color="red")
    d.box("p", 330, 100, 330, 130, "Payload (claims)", '{ "sub": "user_42",\n  "iss": "auth.example.com",\n  "aud": "api", "exp": 1735689600,\n  "scope": "orders:read" }', color="violet")
    d.box("s", 690, 100, 330, 130, "Signature", "RS256(base64url(header) + '.' +\nbase64url(payload), private key)", color="blue")
    d.note("n", 40, 270, 980, 74, "Signed, NOT encrypted: anyone can read the payload. Verify signature (public key from JWKS), exp, iss, aud.\nShort expiry (5 to 15 min) + refresh tokens, because a stateless JWT cannot be revoked before it expires.")
    return d


def network_zones():
    d = Diagram("network-zones", "Defense in depth: network zones in a VPC")
    d.cloud("net", 20, 160, 160, 110, "Internet")
    d.box("edge", 230, 170, 170, 90, "Edge", "CDN + WAF +\nDDoS protection", color="red")
    d.zone("vpc", 440, 50, 760, 380, "VPC", color="gray")
    d.zone("pub", 460, 90, 200, 320, "Public subnet (DMZ)", color="orange")
    d.box("alb", 490, 180, 140, 70, "Load balancer", color="violet")
    d.zone("prv", 720, 90, 210, 320, "Private subnet", color="blue")
    d.stack("app", 750, 180, 140, 70, "App servers", color="blue")
    d.zone("iso", 990, 90, 190, 320, "Isolated subnet", color="green")
    d.db("db", 1020, 165, 130, 100, "Database", "no internet")
    d.arrow("net", "edge")
    d.arrow("edge", "alb", label="443 only")
    d.arrow("alb", "app", label="SG: from LB")
    d.arrow("app", "db", label="SG: 5432\nfrom app")
    return d


def envelope_encryption():
    d = Diagram("envelope-encryption", "Envelope encryption with a KMS")
    d.box("kms", 380, 40, 220, 80, "KMS / HSM", "master key (KEK)\nnever leaves", color="violet")
    d.box("app", 60, 200, 180, 70, "Application", color="blue")
    d.box("dek", 380, 200, 220, 70, "Data key (DEK)", "plaintext in memory only", color="yellow")
    d.db("store", 800, 170, 220, 130, "Storage", "ciphertext\n+ encrypted DEK", color="green")
    d.arrow("app", "kms", label="1. GenerateDataKey", label_pos=0.4)
    d.arrow("kms", "dek", label="2. DEK + DEK encrypted by KEK")
    d.arrow("dek", "store", label="3. AES-GCM encrypt data")
    d.note("n", 60, 330, 960, 74, "Decrypt: send encrypted DEK to KMS -> get DEK -> decrypt locally. Rotating the KEK re-wraps DEKs,\nnot all the data. KMS calls are audited and permissioned per key.")
    return d


def build():
    return [monolith_vs_micro(), service_discovery(), service_mesh(), strangler(), cqrs(), event_sourcing(),
            hexagonal(), serverless(), circuit_breaker(), bulkhead(), retry_backoff(), observability(),
            trace_waterfall(), multi_region(), deploy_strategies(), oauth_pkce(), jwt_structure(),
            network_zones(), envelope_encryption()]
