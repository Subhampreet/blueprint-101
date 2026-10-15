from sketch import Diagram


def osi():
    d = Diagram("osi-model", "OSI model vs TCP/IP model")
    layers = [
        ("7", "Application", "HTTP, DNS, SMTP, gRPC", "pink"),
        ("6", "Presentation", "TLS, encoding, compression", "pink"),
        ("5", "Session", "sessions, RPC dialogs", "pink"),
        ("4", "Transport", "TCP, UDP, QUIC", "orange"),
        ("3", "Network", "IP, ICMP, routing, BGP", "yellow"),
        ("2", "Data link", "Ethernet, MAC, switches, ARP", "green"),
        ("1", "Physical", "fiber, copper, radio", "blue"),
    ]
    for i, (n, l, s, c) in enumerate(layers):
        d.box("l" + n, 60, 80 + i * 66, 360, 56, "L%s  %s" % (n, l), s, color=c, size=17)
    d.box("app", 520, 80, 240, 188, "Application", "L5 to L7 collapsed", color="pink")
    d.box("tr", 520, 278, 240, 56, "Transport", color="orange")
    d.box("in", 520, 344, 240, 56, "Internet", color="yellow")
    d.box("li", 520, 410, 240, 122, "Link", "L1 + L2", color="green")
    d.note("lb", 820, 140, 250, 170, "Where devices live:\nL7: API gateway, L7 LB, WAF\nL4: L4 LB, NAT, firewalls\nL3: routers\nL2: switches")
    d.text("t1", 60, 56, "OSI (7 layers)", size=16, ink="#495057")
    d.text("t2", 520, 56, "TCP/IP (4 layers)", size=16, ink="#495057")
    return d


def tcp_handshake():
    d = Diagram("tcp-handshake", "TCP: 3-way handshake, data, 4-way close")
    d.lifeline("c", 150, 70, 560, "Client", color="blue")
    d.lifeline("s", 650, 70, 560, "Server", color="green")
    d.msg(150, 650, 160, "SYN  seq = x", "m1")
    d.msg(650, 150, 215, "SYN-ACK  seq = y, ack = x+1", "m2", dashed=True)
    d.msg(150, 650, 270, "ACK  ack = y+1", "m3")
    d.msg(150, 650, 340, "data (HTTP request)", "m4", color="#1971c2")
    d.msg(650, 150, 395, "data + ACK", "m5", dashed=True, color="#1971c2")
    d.msg(150, 650, 465, "FIN", "m6", color="#e03131")
    d.msg(650, 150, 515, "ACK", "m7", dashed=True)
    d.msg(650, 150, 565, "FIN", "m8", color="#e03131")
    d.msg(150, 650, 615, "ACK  (client waits TIME_WAIT)", "m9")
    d.note("n", 760, 150, 290, 140, "1 RTT before any data.\nTCP gives ordered, reliable,\nflow and congestion\ncontrolled byte streams.")
    return d


def tls13():
    d = Diagram("tls13-handshake", "TLS 1.3 handshake (1 RTT, 0-RTT on resumption)")
    d.lifeline("c", 150, 70, 380, "Client", color="blue")
    d.lifeline("s", 650, 70, 380, "Server", color="green")
    d.msg(150, 650, 170, "ClientHello + key share (ECDHE)", "m1")
    d.msg(650, 150, 240, "ServerHello + key share, cert, Finished", "m2", dashed=True)
    d.msg(150, 650, 310, "Finished + first encrypted request", "m3", color="#1971c2")
    d.msg(650, 150, 380, "encrypted response", "m4", dashed=True, color="#1971c2")
    d.note("n", 760, 150, 320, 200, "Both sides derive the same session\nkey from ephemeral ECDHE shares:\nforward secrecy.\nCert proves server identity\n(signed by a trusted CA).\nTLS 1.2 needed 2 RTT.")
    return d


def http_versions():
    d = Diagram("http-versions", "HTTP/1.1 vs HTTP/2 vs HTTP/3")
    d.zone("h1", 20, 70, 340, 300, "HTTP/1.1", color="gray")
    for i in range(3):
        d.box("h1c%d" % i, 50, 120 + i * 75, 280, 54, "TCP conn %d: req -> resp" % (i + 1), color="white", size=15)
    d.text("h1t", 40, 340, "one request at a time per connection,\nbrowsers open ~6 connections", size=14)
    d.zone("h2", 390, 70, 340, 300, "HTTP/2", color="blue")
    d.box("h2c", 420, 120, 280, 160, "one TCP connection", "streams 1, 3, 5, 7 interleaved\nbinary frames, HPACK headers", color="blue")
    d.text("h2t", 410, 300, "multiplexed, but one lost packet\nstalls ALL streams (TCP HOL)", size=14)
    d.zone("h3", 760, 70, 340, 300, "HTTP/3", color="green")
    d.box("h3c", 790, 120, 280, 160, "QUIC over UDP", "independent streams\nTLS 1.3 built in\n0-RTT resume, conn migration", color="green")
    d.text("h3t", 780, 300, "loss on one stream does not block\nothers; survives wifi -> 4G switch", size=14)
    return d


def realtime_options():
    d = Diagram("realtime-options", "Polling vs long polling vs SSE vs WebSocket")
    cols = [("Short polling", 40), ("Long polling", 320), ("SSE", 600), ("WebSocket", 880)]
    for i, (name, x) in enumerate(cols):
        d.text("t%d" % i, x + 110, 60, name, size=18, align="center")
        d.point("c%d" % i, x + 30, 100)
        d.point("ce%d" % i, x + 30, 430)
        d.point("s%d" % i, x + 190, 100)
        d.point("se%d" % i, x + 190, 430)
        d.line("c%d" % i, "ce%d" % i, dashed=True, color="#868e96")
        d.line("s%d" % i, "se%d" % i, dashed=True, color="#868e96")
        d.text("cl%d" % i, x + 30, 435, "client", size=13, align="center", ink="#495057")
        d.text("sl%d" % i, x + 190, 435, "server", size=13, align="center", ink="#495057")
    # short polling
    for k, y in enumerate((130, 230, 330)):
        d.msg(70, 230, y, "any news?", "sp%d" % k)
        d.msg(230, 70, y + 35, "no" if k < 2 else "yes!", "spr%d" % k, dashed=True)
    # long polling
    d.msg(350, 510, 130, "any news?", "lp1")
    d.text("lph", 430, 175, "held open...", size=13, align="center", ink="#868e96")
    d.msg(510, 350, 230, "event", "lp2", dashed=True, color="#2f9e44")
    d.msg(350, 510, 270, "any news?", "lp3")
    d.msg(510, 350, 370, "event", "lp4", dashed=True, color="#2f9e44")
    # SSE
    d.msg(630, 790, 130, "GET /stream", "ss1")
    for k, y in enumerate((200, 260, 320, 380)):
        d.msg(790, 630, y, "event", "sse%d" % k, dashed=True, color="#2f9e44")
    # websocket
    d.msg(910, 1070, 130, "HTTP Upgrade", "ws1")
    d.msg(1070, 910, 170, "101 Switching", "ws2", dashed=True)
    d.msg(910, 1070, 240, "msg", "ws3", color="#1971c2")
    d.msg(1070, 910, 290, "msg", "ws4", dashed=True, color="#2f9e44")
    d.msg(1070, 910, 340, "msg", "ws5", dashed=True, color="#2f9e44")
    d.msg(910, 1070, 390, "msg", "ws6", color="#1971c2")
    return d


def websocket_scaling():
    d = Diagram("websocket-scaling", "Scaling WebSockets: gateways + pub/sub + presence")
    d.user("a", 30, 60, "Alice")
    d.user("b", 30, 260, "Bob")
    d.box("lb", 170, 150, 130, 74, "L4/L7 LB", "upgrade aware", color="violet")
    d.stack("g1", 380, 60, 170, 70, "WS gateway 1", "Alice's socket", color="blue")
    d.stack("g2", 380, 250, 170, 70, "WS gateway 2", "Bob's socket", color="blue")
    d.box("reg", 640, 30, 200, 70, "Connection registry", "user -> gateway (Redis)", color="red")
    d.queue("ps", 640, 290, 200, 64, "Pub/Sub", color="yellow")
    d.box("svc", 640, 150, 200, 70, "Chat service", "persist, then route", color="green")
    d.arrow("a", "lb")
    d.arrow("b", "lb")
    d.arrow("lb", "g1")
    d.arrow("lb", "g2")
    d.arrow("g1", "reg", dashed=True, label="register")
    d.arrow("g1", "svc", label="send to Bob")
    d.arrow("svc", "ps", label="publish to gw2")
    d.arrow("ps", "g2", label="deliver")
    d.note("n", 900, 120, 220, 170, "Gateways hold sockets,\nno business logic.\nHeartbeats detect\ndead connections.\nClients reconnect with\nbackoff + resume token.")
    return d


def api_styles():
    d = Diagram("api-styles", "REST vs GraphQL vs gRPC")
    d.zone("r", 20, 70, 340, 300, "REST", color="green")
    d.box("r1", 50, 120, 280, 50, "GET /users/42", color="white", size=16)
    d.box("r2", 50, 185, 280, 50, "GET /users/42/posts?limit=10", color="white", size=15)
    d.box("r3", 50, 250, 280, 50, "GET /posts/9/comments", color="white", size=16)
    d.text("rt", 40, 320, "resources + HTTP verbs, cacheable,\nmay over/under fetch", size=14)
    d.zone("g", 390, 70, 340, 300, "GraphQL", color="pink")
    d.box("g1", 420, 120, 280, 160, "POST /graphql", "user(id: 42) {\n  name\n  posts(first: 10) {\n    title, comments { text }\n  }\n}", color="white")
    d.text("gt", 410, 300, "client picks fields, one round trip,\nwatch N+1 and query cost", size=14)
    d.zone("p", 760, 70, 340, 300, "gRPC", color="blue")
    d.box("p1", 790, 120, 280, 100, "service UserService {\n rpc GetUser(Req) returns (User);\n}", color="white", size=14)
    d.box("p2", 790, 235, 280, 50, "protobuf over HTTP/2, streams", color="white", size=15)
    d.text("pt", 780, 300, "typed contracts, codegen, fast;\nbest for service to service", size=14)
    return d


def build():
    return [osi(), tcp_handshake(), tls13(), http_versions(), realtime_options(), websocket_scaling(), api_styles()]
