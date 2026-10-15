from sketch import Diagram


def dip():
    d = Diagram("solid-dip", "Dependency inversion: both sides depend on the abstraction")
    d.zone("bad", 20, 70, 420, 260, "Before", color="red")
    d.box("os1", 50, 120, 170, 64, "OrderService", "high level", color="blue")
    d.box("my1", 250, 230, 170, 64, "MySQLOrderRepo", "low level detail", color="gray")
    d.arrow("os1", "my1", label="new MySQLOrderRepo()")
    d.zone("good", 480, 70, 620, 260, "After", color="green")
    d.box("os2", 510, 120, 170, 64, "OrderService", "high level", color="blue")
    d.box("port", 760, 120, 200, 64, "<<interface>>\nOrderRepository", color="yellow")
    d.box("my2", 660, 240, 170, 60, "MySQLOrderRepo", color="gray", size=16)
    d.box("mem", 870, 240, 170, 60, "InMemoryRepo", "tests", color="gray", size=16)
    d.arrow("os2", "port", label="depends on")
    d.arrow("my2", "port", dashed=True, label="implements")
    d.arrow("mem", "port", dashed=True)
    return d


def patterns():
    d = Diagram("design-patterns-gallery", "Three patterns you will use weekly")
    d.zone("s", 20, 70, 340, 340, "Strategy", color="blue")
    d.box("ctx", 50, 120, 280, 56, "PricingService", "strategy: DiscountPolicy", color="blue", size=16)
    d.box("i", 50, 210, 280, 50, "<<interface>> DiscountPolicy", color="yellow", size=15)
    d.box("a", 50, 300, 130, 56, "NoDiscount", color="white", size=15)
    d.box("b", 200, 300, 130, 56, "Festive20", color="white", size=15)
    d.arrow("ctx", "i")
    d.arrow("a", "i", dashed=True)
    d.arrow("b", "i", dashed=True)
    d.zone("o", 390, 70, 340, 340, "Observer", color="green")
    d.box("subj", 420, 120, 280, 56, "OrderPlaced publisher", "subscribe / notify", color="green", size=16)
    d.box("o1", 420, 230, 130, 50, "EmailObs", color="white", size=15)
    d.box("o2", 570, 230, 130, 50, "InventoryObs", color="white", size=15)
    d.box("o3", 495, 320, 130, 50, "AnalyticsObs", color="white", size=15)
    d.arrow("subj", "o1", label="notify")
    d.arrow("subj", "o2")
    d.arrow("subj", "o3", dashed=True)
    d.zone("dz", 760, 70, 340, 340, "Decorator", color="orange")
    d.box("d1", 790, 120, 280, 50, "RetryingClient", color="orange", size=16)
    d.box("d2", 810, 190, 240, 50, "CachingClient", color="yellow", size=16)
    d.box("d3", 830, 260, 200, 50, "HttpClient", color="white", size=16)
    d.arrow("d1", "d2", label="wraps")
    d.arrow("d2", "d3", label="wraps")
    d.text("dt", 790, 330, "same interface, behaviour\nadded layer by layer", size=14)
    return d


def producer_consumer():
    d = Diagram("producer-consumer", "Producer-consumer with a bounded blocking queue")
    for i in range(2):
        d.box("p%d" % i, 40, 90 + i * 110, 150, 64, "Producer %d" % (i + 1), color="blue")
    d.queue("q", 300, 140, 260, 70, "BlockingQueue(cap=100)")
    for i in range(3):
        d.box("c%d" % i, 680, 60 + i * 100, 150, 64, "Consumer %d" % (i + 1), color="green")
        d.arrow("q", "c%d" % i, label="take()" if i == 1 else "")
    d.arrow("p0", "q", label="put()")
    d.arrow("p1", "q")
    d.note("n", 260, 270, 340, 90, "Full queue: put() blocks (backpressure).\nEmpty queue: take() blocks.\nNo busy waiting, no lost wakeups.")
    return d


def deadlock():
    d = Diagram("deadlock-cycle", "Deadlock: a cycle in the wait-for graph")
    d.ellipse("t1", 80, 80, 170, 80, "Thread A", color="blue")
    d.ellipse("t2", 520, 280, 170, 80, "Thread B", color="orange")
    d.box("l1", 520, 90, 170, 60, "Lock 1 (account 7)", color="yellow", size=15)
    d.box("l2", 80, 290, 170, 60, "Lock 2 (account 9)", color="yellow", size=15)
    d.arrow("l1", "t1", label="held by")
    d.arrow("t1", "l2", label="waits for", dashed=True, color="#e03131")
    d.arrow("l2", "t2", label="held by")
    d.arrow("t2", "l1", label="waits for", dashed=True, color="#e03131")
    d.note("n", 760, 120, 300, 200, "Coffman conditions (all 4 needed):\n1 mutual exclusion\n2 hold and wait\n3 no preemption\n4 circular wait\n\nBreak one: e.g. lock in a\nglobal order (lower id first).")
    return d


def parking_lot():
    d = Diagram("parking-lot-classes", "Parking lot: core classes")
    d.box("lot", 40, 70, 230, 120, "ParkingLot", "- floors: List<Floor>\n- gates\n+ park(vehicle): Ticket\n+ unpark(ticket): Receipt", color="blue")
    d.box("floor", 340, 70, 230, 100, "Floor", "- spots: Map<Type, Spots>\n+ findSpot(type)", color="blue")
    d.box("spot", 640, 70, 220, 100, "ParkingSpot", "- id, type, occupied\n+ assign(v) / free()", color="blue")
    d.box("veh", 640, 240, 220, 90, "<<abstract>> Vehicle", "- plate, type", color="yellow")
    d.box("car", 600, 390, 130, 50, "Car", color="white", size=16)
    d.box("bike", 750, 390, 130, 50, "Motorbike", color="white", size=16)
    d.box("tkt", 340, 240, 230, 100, "Ticket", "- id, spot, vehicle\n- entryTime", color="green")
    d.box("fee", 40, 240, 230, 100, "<<interface>> FeeStrategy", "+ compute(ticket, exit)\nHourly | FlatWeekend", color="orange")
    d.box("pay", 40, 390, 230, 64, "PaymentProcessor", "card | cash | UPI", color="pink")
    d.arrow("lot", "floor", label="1..*")
    d.arrow("floor", "spot", label="1..*")
    d.arrow("spot", "veh", dashed=True, label="holds 0..1")
    d.arrow("car", "veh")
    d.arrow("bike", "veh")
    d.arrow("lot", "tkt", label="issues")
    d.arrow("lot", "fee", label="uses")
    d.arrow("fee", "pay", dashed=True)
    return d


def thread_pool():
    d = Diagram("thread-pool", "Thread pool: reuse a fixed set of workers")
    d.stack("sub", 30, 160, 150, 70, "submit(task)", color="blue")
    d.queue("q", 240, 160, 230, 70, "task queue (bounded)")
    for i in range(3):
        d.box("w%d" % i, 560, 70 + i * 95, 160, 60, "worker %d" % (i + 1), "loop: take + run", color="green", size=16)
        d.arrow("q", "w%d" % i)
    d.box("rej", 240, 300, 230, 60, "Rejection policy", "abort | caller runs | drop", color="red", size=16)
    d.arrow("sub", "q")
    d.arrow("q", "rej", dashed=True, label="when full")
    d.note("n", 790, 120, 270, 140, "Size CPU-bound pools near\n#cores; IO-bound pools\nlarger (cores x (1 + wait/\ncompute)). Bounded queue\n= backpressure.")
    return d


def build():
    return [dip(), patterns(), producer_consumer(), deadlock(), parking_lot(), thread_pool()]
