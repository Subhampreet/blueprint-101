from sketch import Diagram


def interview_flow():
    d = Diagram("interview-flow", "A 45 minute system design interview")
    steps = [
        ("s1", "1. Requirements", "functional + NFRs, 5 min", "blue"),
        ("s2", "2. Estimation", "QPS, storage, 3 to 5 min", "cyan"),
        ("s3", "3. API design", "core endpoints, 5 min", "green"),
        ("s4", "4. Data model", "entities + store, 5 min", "yellow"),
    ]
    for i, (id, l, s, c) in enumerate(steps):
        d.box(id, 40 + i * 230, 100, 180, 74, l, s, color=c)
    d.box("s5", 730, 260, 180, 74, "5. High level", "boxes + arrows, 10 min", color="violet")
    d.box("s6", 500, 260, 180, 74, "6. Deep dives", "bottlenecks, 10 to 15 min", color="orange")
    d.box("s7", 270, 260, 180, 74, "7. Wrap up", "failures, evolution, 3 min", color="pink")
    for a, b in (("s1", "s2"), ("s2", "s3"), ("s3", "s4")):
        d.arrow(a, b)
    d.arrow("s4", "s5", fs="b", ts="t")
    d.arrow("s5", "s6")
    d.arrow("s6", "s7")
    d.note("tip", 30, 250, 200, 96, "Think out loud.\nName trade-offs.\nCheck in every step.")
    return d


def estimation_pipeline():
    d = Diagram("estimation-pipeline", "Back of the envelope: one chain of multiplications")
    d.box("dau", 40, 110, 150, 64, "DAU", "e.g. 100M users", color="blue")
    d.box("rpd", 270, 110, 160, 64, "Requests / day", "DAU x actions", color="cyan")
    d.box("qps", 510, 110, 150, 64, "Average QPS", "/ 86,400 (~10^5)", color="green")
    d.box("peak", 740, 110, 150, 64, "Peak QPS", "x 2 to 10", color="orange")
    d.box("srv", 970, 110, 150, 64, "Servers", "peak / per box QPS", color="violet")
    d.box("spd", 270, 280, 160, 64, "Storage / day", "writes x object size", color="yellow")
    d.box("tot", 510, 280, 150, 64, "Total storage", "x retention x replicas", color="yellow")
    d.box("bw", 740, 280, 150, 64, "Bandwidth", "QPS x response size", color="pink")
    d.box("mem", 970, 280, 150, 64, "Cache memory", "20% of daily reads", color="red")
    d.arrow("dau", "rpd")
    d.arrow("rpd", "qps")
    d.arrow("qps", "peak")
    d.arrow("peak", "srv")
    d.arrow("rpd", "spd", fs="b", ts="t", label="write share")
    d.arrow("spd", "tot")
    d.arrow("peak", "bw", fs="b", ts="t")
    d.arrow("qps", "mem", via=[(585, 230), (1045, 230)], ts="t", dashed=True, label="80/20 rule", label_pos=0.7)
    return d


def hld_vs_lld():
    d = Diagram("hld-vs-lld", "HLD draws the city, LLD draws one building")
    d.zone("hz", 20, 70, 520, 330, "High Level Design", color="blue")
    d.user("c", 50, 150, "Client")
    d.box("gw", 150, 150, 130, 60, "API Gateway", color="violet")
    d.box("os", 340, 110, 150, 60, "Order Service", color="blue")
    d.box("ps", 340, 210, 150, 60, "Payment Service", color="blue")
    d.db("db", 170, 290, 110, 90, "Orders DB")
    d.queue("q", 340, 310, 160, 56, "Events")
    d.arrow("c", "gw")
    d.arrow("gw", "os")
    d.arrow("gw", "ps")
    d.arrow("os", "db", fs="l", via=[(305, 140), (305, 300)])
    d.arrow("ps", "q", fs="b", ts="t")
    d.zone("lz", 620, 70, 470, 330, "Low Level Design", color="green")
    d.box("cls1", 650, 110, 200, 96, "OrderService", "+ place(cart)\n+ cancel(id)", color="white")
    d.box("cls2", 880, 110, 180, 96, "<<interface>>\nPaymentGateway", "+ charge(amt)", color="yellow")
    d.box("cls3", 650, 270, 200, 96, "Order", "- id, items, state\n+ transition(e)", color="white")
    d.box("cls4", 880, 270, 180, 96, "StripeGateway", "implements", color="white")
    d.arrow("cls1", "cls2", label="uses")
    d.arrow("cls1", "cls3", label="creates")
    d.arrow("cls4", "cls2", dashed=True, label="impl")
    d.arrow("os", "cls1", via=[(570, 140)], dashed=True, color="#e8590c", label="zoom in", label_pos=0.3)
    return d


def cap_triangle():
    d = Diagram("cap-triangle", "CAP: under a partition you pick C or A")
    d.ellipse("c", 330, 60, 160, 80, "Consistency", color="blue")
    d.ellipse("a", 70, 330, 160, 80, "Availability", color="green")
    d.ellipse("p", 590, 330, 190, 80, "Partition\ntolerance", color="orange")
    d.line("c", "a", label="CA: single node RDBMS\n(not a real distributed choice)")
    d.line("c", "p", label="CP: etcd, ZooKeeper,\nHBase, Spanner")
    d.line("a", "p", label="AP: Cassandra, DynamoDB,\nCouchDB, Riak")
    d.note("n", 280, 460, 290, 74, "P is not optional on a real network,\nso the real choice is CP vs AP.")
    return d


def cap_partition():
    d = Diagram("cap-partition", "What a partition forces you to decide")
    d.user("u1", 40, 120, "Writer", "x = 2")
    d.db("n1", 210, 110, 140, 100, "Node A", "x = 2", color="blue")
    d.db("n2", 560, 110, 140, 100, "Node B", "x = 1 (stale)", color="blue")
    d.user("u2", 790, 120, "Reader", "read x")
    d.arrow("u1", "n1", label="write")
    d.line("n1", "n2", label="network partition", dashed=True, color="#e03131")
    d.arrow("u2", "n2", label="read")
    d.note("cp", 150, 290, 300, 92, "CP choice: Node B refuses\n(error or timeout) until it can\nconfirm it has the latest x.", color="blue")
    d.note("ap", 500, 290, 300, 92, "AP choice: Node B answers x = 1.\nAlways up, maybe stale.\nReconcile after the heal.", color="green")
    return d


def pacelc():
    d = Diagram("pacelc", "PACELC: the trade-off exists even without failures")
    d.diamond("p", 60, 140, 170, 110, "Partition?")
    d.box("pa", 440, 60, 200, 64, "Availability", "serve possibly stale", color="green")
    d.box("pc", 440, 150, 200, 64, "Consistency", "reject or block", color="blue")
    d.box("el", 440, 270, 200, 64, "Latency", "answer from nearest replica", color="yellow")
    d.box("ec", 440, 360, 200, 64, "Consistency", "wait for quorum / leader", color="blue")
    d.arrow("p", "pa", label="yes, then A", label_pos=0.45)
    d.arrow("p", "pc", label="or C", label_pos=0.45)
    d.arrow("p", "el", label="else, then L", label_pos=0.45)
    d.arrow("p", "ec", label="or C", label_pos=0.45)
    d.note("ex", 710, 120, 290, 220,
           "PA/EL: Cassandra, DynamoDB\n(default settings)\n\nPC/EC: Spanner, etcd,\nbanking ledgers\n\nPA/EC: MongoDB (majority\nreads), many caches differ")
    return d


def scaling():
    d = Diagram("scaling-vertical-horizontal", "Vertical vs horizontal scaling")
    d.zone("vz", 20, 70, 400, 300, "Scale up (vertical)", color="orange")
    d.box("s1", 50, 200, 90, 60, "2 vCPU", "8 GB", color="orange")
    d.box("s2", 220, 140, 170, 180, "32 vCPU", "256 GB RAM\nNVMe", color="orange")
    d.arrow("s1", "s2", label="bigger box")
    d.zone("hz", 470, 70, 480, 300, "Scale out (horizontal)", color="blue")
    d.box("lb", 500, 190, 130, 64, "Load\nBalancer", color="violet")
    for i in range(3):
        d.box("n%d" % i, 730, 100 + i * 90, 160, 60, "Node %d" % (i + 1), "4 vCPU", color="blue")
        d.arrow("lb", "n%d" % i)
    d.note("t", 120, 400, 700, 74, "Vertical: simple, no code change, hard ceiling, single point of failure.\n"
           "Horizontal: near linear growth + redundancy, needs stateless services and data partitioning.")
    return d


def latency_breakdown():
    d = Diagram("latency-breakdown", "Where the milliseconds of one request go")
    items = [
        ("dns", "DNS lookup", "0 to 50 ms", "cyan"),
        ("tcp", "TCP + TLS", "1 to 3 RTT", "blue"),
        ("lb", "LB / gateway", "~1 ms", "violet"),
        ("app", "App logic", "1 to 20 ms", "green"),
        ("data", "Cache / DB", "0.5 to 50 ms", "yellow"),
        ("ret", "Response", "size / bandwidth", "orange"),
    ]
    for i, (id, l, s, c) in enumerate(items):
        d.box(id, 40 + i * 175, 120, 150, 70, l, s, color=c)
        if i:
            d.arrow(items[i - 1][0], id)
    d.note("n", 40, 250, 470, 96, "Latency = time for ONE request.\nThroughput = requests finished per second.\nLittle's law: in-flight = throughput x latency.")
    d.note("n2", 560, 250, 520, 96, "Biggest wins usually: avoid round trips,\nkeep connections warm, cache close to the user,\nparallelize independent calls.", color="green")
    return d


def availability():
    d = Diagram("availability-series-parallel", "Availability of composed components")
    d.zone("sz", 20, 70, 520, 220, "In series: multiply", color="red")
    d.box("a", 50, 140, 130, 64, "LB", "99.99%", color="violet")
    d.box("b", 220, 140, 130, 64, "App", "99.9%", color="blue")
    d.box("c", 390, 140, 120, 64, "DB", "99.9%", color="green")
    d.arrow("a", "b")
    d.arrow("b", "c")
    d.text("st", 50, 230, "0.9999 x 0.999 x 0.999 = 99.79%\n(about 18 hours down per year)", size=15)
    d.zone("pz", 590, 70, 450, 220, "In parallel: 1 - product of failure", color="green")
    d.box("p1", 620, 110, 150, 56, "Replica A", "99.9%", color="green")
    d.box("p2", 620, 200, 150, 56, "Replica B", "99.9%", color="green")
    d.text("pt", 800, 140, "1 - (0.001 x 0.001)\n= 99.9999%", size=15)
    return d


def build():
    return [interview_flow(), estimation_pipeline(), hld_vs_lld(), cap_triangle(),
            cap_partition(), pacelc(), scaling(), latency_breakdown(), availability()]
