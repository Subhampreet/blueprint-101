"""
sketch.py: a tiny hand-drawn diagram engine.

Describe a diagram once with Python calls and get two outputs:
  1. an SVG that looks like it was sketched in Excalidraw (wobbly double
     strokes, pastel fills, handwritten font), used inside the notes
  2. a .excalidraw JSON file you can open at https://excalidraw.com to edit

Only the standard library is used, so it runs anywhere Python 3.8+ exists.

Example:
    d = Diagram("lb-basic", "Load balancer in front of app servers")
    d.user("u", 40, 160, "Clients")
    d.box("lb", 200, 140, 140, 60, "Load Balancer", color="violet")
    d.stack("app", 420, 130, 150, 80, "App servers", color="blue")
    d.arrow("u", "lb")
    d.arrow("lb", "app", label="round robin")
    d.save("assets/diagrams")
"""

import json
import math
import os
import random
import zlib

INK = "#1e1e1e"
MUTED = "#495057"
FONT = ("Virgil, Excalifont, 'Comic Sans MS', 'Chalkboard SE', "
        "'Segoe Print', 'Bradley Hand', cursive")

# Excalidraw default palette: (stroke accent, pastel fill)
COLORS = {
    "blue": ("#1971c2", "#a5d8ff"),
    "green": ("#2f9e44", "#b2f2bb"),
    "red": ("#e03131", "#ffc9c9"),
    "yellow": ("#f08c00", "#ffec99"),
    "violet": ("#6741d9", "#d0bfff"),
    "orange": ("#e8590c", "#ffd8a8"),
    "cyan": ("#0c8599", "#99e9f2"),
    "pink": ("#c2255c", "#fcc2d7"),
    "gray": ("#495057", "#e9ecef"),
    "white": ("#1e1e1e", "#ffffff"),
    "none": ("#1e1e1e", "transparent"),
}


def _fmt(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")


def text_width(s, size):
    """Rough width estimate for a handwritten font."""
    w = 0.0
    for ch in s:
        if ch in "il.,:;'|!":
            w += 0.3
        elif ch in "mwMW":
            w += 0.85
        elif ch.isupper():
            w += 0.66
        elif ch == " ":
            w += 0.33
        else:
            w += 0.55
    return w * size


class Rough:
    """Generates jittered SVG path data, similar in spirit to rough.js."""

    def __init__(self, seed, roughness=1.0):
        self.r = random.Random(seed)
        self.k = roughness

    def j(self, a):
        return self.r.uniform(-a, a) * self.k

    def line(self, x1, y1, x2, y2, passes=2):
        L = math.hypot(x2 - x1, y2 - y1) or 1.0
        nx, ny = -(y2 - y1) / L, (x2 - x1) / L
        end = min(1.6, 0.4 + L * 0.006)
        bow = min(2.6, 0.5 + L * 0.012)
        d = []
        for _ in range(passes):
            sx, sy = x1 + self.j(end), y1 + self.j(end)
            ex, ey = x2 + self.j(end), y2 + self.j(end)
            t = 0.5 + self.j(0.15)
            mx, my = sx + (ex - sx) * t, sy + (ey - sy) * t
            b = self.j(bow)
            d.append("M%s %s Q%s %s %s %s" % (
                _fmt(sx), _fmt(sy), _fmt(mx + nx * b), _fmt(my + ny * b),
                _fmt(ex), _fmt(ey)))
        return " ".join(d)

    def rrect(self, x, y, w, h, r):
        r = min(r, w / 2, h / 2)
        out = []
        for _ in range(2):
            J = lambda a=1.2: self.j(a)
            p = [
                ("M", x + r + J(), y + J()),
                ("Q", x + w / 2 + J(), y + J(1.8), x + w - r + J(), y + J()),
                ("Q", x + w + J(), y + J(), x + w + J(), y + r + J()),
                ("Q", x + w + J(1.8), y + h / 2 + J(), x + w + J(), y + h - r + J()),
                ("Q", x + w + J(), y + h + J(), x + w - r + J(), y + h + J()),
                ("Q", x + w / 2 + J(), y + h + J(1.8), x + r + J(), y + h + J()),
                ("Q", x + J(), y + h + J(), x + J(), y + h - r + J()),
                ("Q", x + J(1.8), y + h / 2 + J(), x + J(), y + r + J()),
                ("Q", x + J(), y + J(), x + r + J(2.5), y + J()),
            ]
            s = []
            for seg in p:
                s.append(seg[0] + " ".join(_fmt(v) for v in seg[1:]))
            out.append(" ".join(s))
        return out  # two independent passes

    def ellipse_pts(self, cx, cy, rx, ry, start=None, sweep=None, overshoot=True):
        if start is None:
            start = self.r.uniform(0, 2 * math.pi)
        if sweep is None:
            sweep = 2 * math.pi + (0.35 if overshoot else 0)
        n = max(10, int(abs(sweep) / (2 * math.pi) * 22))
        drift = self.j(0.025)
        pts = []
        for i in range(n + 1):
            a = start + sweep * i / n
            f = 1 + drift * i / n + self.j(0.006)
            pts.append((cx + rx * f * math.cos(a), cy + ry * f * math.sin(a)))
        return pts

    @staticmethod
    def smooth(pts, closed=False):
        """Catmull-Rom spline through points, as cubic bezier path data."""
        if len(pts) < 3:
            return "M%s %s L%s %s" % (_fmt(pts[0][0]), _fmt(pts[0][1]),
                                      _fmt(pts[-1][0]), _fmt(pts[-1][1]))
        d = ["M%s %s" % (_fmt(pts[0][0]), _fmt(pts[0][1]))]
        P = pts
        for i in range(len(P) - 1):
            p0 = P[i - 1] if i > 0 else P[i]
            p1, p2 = P[i], P[i + 1]
            p3 = P[i + 2] if i + 2 < len(P) else P[i + 1]
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            d.append("C%s %s %s %s %s %s" % (_fmt(c1[0]), _fmt(c1[1]), _fmt(c2[0]),
                                             _fmt(c2[1]), _fmt(p2[0]), _fmt(p2[1])))
        if closed:
            d.append("Z")
        return " ".join(d)


class Node:
    def __init__(self, id, kind, x, y, w, h, label="", sub="", color="white",
                 size=18, dashed=False, align="center", ink=None):
        self.id, self.kind = id, kind
        self.x, self.y, self.w, self.h = x, y, w, h
        self.label, self.sub = label, sub
        self.color, self.size, self.dashed = color, size, dashed
        self.align = align
        self.ink = ink

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2

    def anchor(self, side, offset=0.0):
        if side == "t":
            return (self.cx + offset, self.y)
        if side == "b":
            return (self.cx + offset, self.y + self.h)
        if side == "l":
            return (self.x, self.cy + offset)
        if side == "r":
            return (self.x + self.w, self.cy + offset)
        raise ValueError(side)

    def clip(self, tx, ty, gap=6):
        """Point on this node's border toward (tx, ty)."""
        dx, dy = tx - self.cx, ty - self.cy
        if dx == 0 and dy == 0:
            return self.cx, self.cy
        if self.kind in ("ellipse", "user_head"):
            rx, ry = self.w / 2 + gap, self.h / 2 + gap
            t = 1 / math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2)
            return self.cx + dx * t, self.cy + dy * t
        hw, hh = self.w / 2 + gap, self.h / 2 + gap
        tx_ = hw / abs(dx) if dx else float("inf")
        ty_ = hh / abs(dy) if dy else float("inf")
        t = min(tx_, ty_)
        return self.cx + dx * t, self.cy + dy * t


class Edge:
    def __init__(self, a, b, label="", dashed=False, both=False, fs=None, ts=None,
                 via=None, bend=0, color=None, head=True, label_pos=0.5,
                 fo=0.0, to=0.0, size=15):
        self.a, self.b, self.label = a, b, label
        self.dashed, self.both = dashed, both
        self.fs, self.ts, self.via = fs, ts, via or []
        self.bend, self.color, self.head = bend, color, head
        self.label_pos = label_pos
        self.fo, self.to = fo, to
        self.size = size


class Diagram:
    def __init__(self, name, title="", seed=None, roughness=1.0):
        self.name = name
        self.title = title
        self.nodes = {}
        self.order = []
        self.edges = []
        self.seed = seed if seed is not None else zlib.crc32(name.encode())
        self.roughness = roughness

    # ------------------------------------------------------------ nodes
    def _add(self, n):
        if n.id in self.nodes:
            raise ValueError("duplicate node id %s in %s" % (n.id, self.name))
        self.nodes[n.id] = n
        self.order.append(n)
        return n

    def box(self, id, x, y, w, h, label="", sub="", color="white", size=18, dashed=False):
        return self._add(Node(id, "box", x, y, w, h, label, sub, color, size, dashed))

    def stack(self, id, x, y, w, h, label="", sub="", color="blue", size=18):
        """A box with two shadow copies behind it: 'N instances'."""
        return self._add(Node(id, "stack", x, y, w, h, label, sub, color, size))

    def db(self, id, x, y, w, h, label="", sub="", color="green", size=17):
        return self._add(Node(id, "db", x, y, w, h, label, sub, color, size))

    def queue(self, id, x, y, w, h, label="", sub="", color="yellow", size=17):
        return self._add(Node(id, "queue", x, y, w, h, label, sub, color, size))

    def ellipse(self, id, x, y, w, h, label="", sub="", color="white", size=18):
        return self._add(Node(id, "ellipse", x, y, w, h, label, sub, color, size))

    def diamond(self, id, x, y, w, h, label="", sub="", color="yellow", size=16):
        return self._add(Node(id, "diamond", x, y, w, h, label, sub, color, size))

    def cloud(self, id, x, y, w, h, label="Internet", sub="", color="cyan", size=18):
        return self._add(Node(id, "cloud", x, y, w, h, label, sub, color, size))

    def user(self, id, x, y, label="Client", sub="", color="white", size=16):
        """Stick figure. (x, y) is the top-left of a 50x70 figure; label sits below."""
        return self._add(Node(id, "user", x, y, 50, 70, label, sub, color, size))

    def zone(self, id, x, y, w, h, label="", color="gray", size=16):
        return self._add(Node(id, "zone", x, y, w, h, label, "", color, size, dashed=True))

    def text(self, id, x, y, label, size=16, align="left", ink=None, w=None):
        lines = label.split("\n")
        tw = w or max(text_width(l, size) for l in lines)
        return self._add(Node(id, "text", x, y, tw, len(lines) * size * 1.3, label, "",
                              "none", size, align=align, ink=ink))

    def point(self, id, x, y):
        """Invisible anchor, used for sequence diagram messages and free arrows."""
        n = self._add(Node(id, "text", x, y, 0, 0, "", "", "none", 1))
        return n

    def lifeline(self, id, x, y, h, label, color="blue", w=140):
        """Sequence diagram participant: header box plus a dashed vertical line."""
        self.box(id, x - w / 2, y, w, 50, label, color=color, size=16)
        self.point(id + "_end", x, y + h)
        self.line(id, id + "_end", dashed=True, fs="b", color="#868e96")

    def msg(self, a_x, b_x, y, label, id, dashed=False, color=None):
        """Horizontal sequence message from x=a_x to x=b_x at height y."""
        self.point(id + "_a", a_x, y)
        self.point(id + "_b", b_x, y)
        self.arrow(id + "_a", id + "_b", label=label, dashed=dashed, color=color)

    def note(self, id, x, y, w, h, label, color="yellow", size=15):
        """Sticky note: a filled box with left-aligned small text."""
        return self._add(Node(id, "note", x, y, w, h, label, "", color, size, align="left"))

    # ------------------------------------------------------------ edges
    def arrow(self, a, b, label="", **kw):
        self.edges.append(Edge(a, b, label, **kw))

    def line(self, a, b, label="", **kw):
        kw.setdefault("head", False)
        self.edges.append(Edge(a, b, label, **kw))

    # ------------------------------------------------------------ geometry
    def _endpoints(self, e):
        A, B = self.nodes[e.a], self.nodes[e.b]
        if e.fs:
            p1 = A.anchor(e.fs, e.fo)
        else:
            tgt = e.via[0] if e.via else (B.anchor(e.ts, e.to) if e.ts else (B.cx, B.cy))
            p1 = A.clip(*tgt)
        if e.ts:
            p2 = B.anchor(e.ts, e.to)
        else:
            src = e.via[-1] if e.via else p1
            p2 = B.clip(*src)
        # pull anchored endpoints off the border a little
        def nudge(p, side, inward=False):
            g = 6
            dx, dy = {"t": (0, -g), "b": (0, g), "l": (-g, 0), "r": (g, 0)}[side]
            return (p[0] + dx, p[1] + dy)
        if e.fs:
            p1 = nudge(p1, e.fs)
        if e.ts:
            p2 = nudge(p2, e.ts)
        return p1, p2

    def bounds(self):
        xs, ys = [], []
        for n in self.order:
            w = n.w
            if n.kind == "user":
                w = max(n.w, text_width(n.label, n.size))
                xs += [n.cx - w / 2, n.cx + w / 2]
                ys += [n.y, n.y + n.h + n.size * 1.6 + (n.size if n.sub else 0)]
                continue
            if n.kind == "text":
                if n.align == "center":
                    xs += [n.x - w / 2, n.x + w / 2]
                else:
                    xs += [n.x, n.x + w]
                ys += [n.y, n.y + n.h]
                continue
            off = 12 if n.kind == "stack" else 0
            xs += [n.x, n.x + n.w + off]
            ys += [n.y - off, n.y + n.h]
        for e in self.edges:
            for p in e.via:
                xs.append(p[0])
                ys.append(p[1])
        pad = 28
        top = min(ys) - pad - (44 if self.title else 0)
        return min(xs) - pad, top, max(xs) + pad, max(ys) + pad

    # ------------------------------------------------------------ SVG
    def to_svg(self):
        R = Rough(self.seed, self.roughness)
        x0, y0, x1, y1 = self.bounds()
        W, H = x1 - x0, y1 - y0
        out = []
        out.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s %s %s %s" '
                   'width="%d" height="%d" font-family="%s">' % (
                       _fmt(x0), _fmt(y0), _fmt(W), _fmt(H), round(W), round(H),
                       FONT.replace('"', "'")))
        out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="14" fill="#ffffff"/>' % (
            _fmt(x0), _fmt(y0), _fmt(W), _fmt(H)))
        if self.title:
            out.append(self._text_svg(x0 + 26, y0 + 34, self.title, 22, INK, "start"))
            ux = x0 + 26
            out.append('<path d="%s" stroke="#e8590c" stroke-width="2.2" fill="none" '
                       'stroke-linecap="round"/>' % R.line(
                           ux, y0 + 44, ux + min(text_width(self.title, 22), W - 60), y0 + 44, 1))

        # zones first so they sit behind everything
        for n in self.order:
            if n.kind == "zone":
                out.append(self._node_svg(R, n))
        # edges under nodes so arrowheads stop at borders cleanly
        for e in self.edges:
            out.append(self._edge_svg(R, e))
        for n in self.order:
            if n.kind != "zone":
                out.append(self._node_svg(R, n))
        # edge labels on top
        for e in self.edges:
            if e.label:
                out.append(self._edge_label_svg(e))
        out.append("</svg>")
        return "\n".join(out)

    def _text_svg(self, x, y, s, size, fill, anchor="middle", baseline_center=False):
        lines = s.split("\n")
        lh = size * 1.25
        if baseline_center:
            y = y - (len(lines) - 1) * lh / 2 + size * 0.35
        parts = []
        for i, l in enumerate(lines):
            parts.append('<tspan x="%s" y="%s">%s</tspan>' % (
                _fmt(x), _fmt(y + i * lh), _esc(l)))
        return '<text font-size="%s" fill="%s" text-anchor="%s">%s</text>' % (
            _fmt(size), fill, anchor, "".join(parts))

    def _label_block(self, n, cx, cy):
        """Label + optional smaller sub label, centered on (cx, cy)."""
        out = []
        ll = n.label.split("\n") if n.label else []
        sl = n.sub.split("\n") if n.sub else []
        lh, sh = n.size * 1.25, n.size * 0.78 * 1.25
        total = len(ll) * lh + len(sl) * sh
        y = cy - total / 2 + n.size * 0.85
        for l in ll:
            out.append(self._text_svg(cx, y, l, n.size, INK))
            y += lh
        y += 0 if not sl else -lh + lh * 0.98
        for l in sl:
            out.append(self._text_svg(cx, y, l, n.size * 0.78, MUTED))
            y += sh
        return "".join(out)

    def _node_svg(self, R, n):
        stroke, fill = COLORS.get(n.color, COLORS["white"])
        sw = 1.7
        out = []

        def strokes(paths, color=INK, width=sw, dash=False):
            s = []
            for i, p in enumerate(paths):
                extra = ' stroke-dasharray="8 7"' if dash else ""
                s.append('<path d="%s" stroke="%s" stroke-width="%s" fill="none" '
                         'stroke-linecap="round" stroke-linejoin="round"%s/>' % (
                             p, color, _fmt(width if i == 0 else width * 0.8), extra))
            return "".join(s)

        def filled(path, color):
            if color == "transparent":
                return ""
            return '<path d="%s" fill="%s" stroke="none"/>' % (path, color)

        if n.kind in ("box", "note", "queue", "stack"):
            if n.kind == "stack":
                for k in (2, 1):
                    o = 6 * k
                    p = R.rrect(n.x + o, n.y - o, n.w, n.h, 10)
                    out.append(filled(p[0], fill))
                    out.append(strokes(p))
            p = R.rrect(n.x, n.y, n.w, n.h, 4 if n.kind == "note" else 10)
            out.append(filled(p[0], fill))
            out.append(strokes(p, dash=n.dashed and n.kind != "note"))
            if n.kind == "queue":
                # message slots on the right
                k = 4
                slot = min(16, n.w / 10)
                for i in range(1, k + 1):
                    xx = n.x + n.w - i * slot
                    out.append(strokes([R.line(xx, n.y + 6, xx, n.y + n.h - 6, 1)], width=1.3))
                cx = n.x + (n.w - k * slot) / 2
                out.append(self._label_block(n, cx, n.cy))
            elif n.kind == "note":
                lines = n.label.split("\n")
                lh = n.size * 1.3
                for i, l in enumerate(lines):
                    out.append(self._text_svg(n.x + 12, n.y + 12 + n.size + i * lh, l,
                                              n.size, INK, "start"))
            else:
                out.append(self._label_block(n, n.cx, n.cy))
        elif n.kind == "zone":
            p = R.rrect(n.x, n.y, n.w, n.h, 16)
            out.append('<path d="%s" fill="%s" fill-opacity="0.35" stroke="none"/>' % (
                p[0], fill if fill != "transparent" else "#ffffff"))
            out.append(strokes(p[:1], color=stroke, width=1.5, dash=True))
            out.append(self._text_svg(n.x + 14, n.y + n.size + 8, n.label, n.size, stroke, "start"))
        elif n.kind == "ellipse":
            pts = R.ellipse_pts(n.cx, n.cy, n.w / 2, n.h / 2)
            out.append(filled(R.smooth(R.ellipse_pts(n.cx, n.cy, n.w / 2, n.h / 2, 0,
                                                     2 * math.pi, False), True), fill))
            out.append(strokes([R.smooth(pts), R.smooth(R.ellipse_pts(n.cx, n.cy, n.w / 2, n.h / 2))]))
            out.append(self._label_block(n, n.cx, n.cy))
        elif n.kind == "diamond":
            cx, cy, hw, hh = n.cx, n.cy, n.w / 2, n.h / 2
            poly = "M%s %s L%s %s L%s %s L%s %s Z" % (
                _fmt(cx), _fmt(cy - hh), _fmt(cx + hw), _fmt(cy), _fmt(cx), _fmt(cy + hh),
                _fmt(cx - hw), _fmt(cy))
            out.append(filled(poly, fill))
            segs = [R.line(cx, cy - hh, cx + hw, cy), R.line(cx + hw, cy, cx, cy + hh),
                    R.line(cx, cy + hh, cx - hw, cy), R.line(cx - hw, cy, cx, cy - hh)]
            out.append(strokes([" ".join(segs)]))
            out.append(self._label_block(n, cx, cy))
        elif n.kind == "db":
            ry = min(14, n.h * 0.16)
            x, y, w, h = n.x, n.y, n.w, n.h
            body = "M%s %s L%s %s A%s %s 0 0 0 %s %s L%s %s A%s %s 0 0 0 %s %s Z" % (
                _fmt(x), _fmt(y + ry), _fmt(x), _fmt(y + h - ry), _fmt(w / 2), _fmt(ry),
                _fmt(x + w), _fmt(y + h - ry), _fmt(x + w), _fmt(y + ry), _fmt(w / 2), _fmt(ry),
                _fmt(x), _fmt(y + ry))
            out.append(filled(body, fill))
            top = R.smooth(R.ellipse_pts(x + w / 2, y + ry, w / 2, ry))
            bottom = R.smooth(R.ellipse_pts(x + w / 2, y + h - ry, w / 2, ry, 0, math.pi, False))
            sides = R.line(x, y + ry, x, y + h - ry) + " " + R.line(x + w, y + ry, x + w, y + h - ry)
            out.append(strokes([top, bottom, sides]))
            out.append(self._label_block(n, n.cx, n.cy + ry * 0.6))
        elif n.kind == "cloud":
            cx, cy, w, h = n.cx, n.cy, n.w, n.h
            # union of circles placed around an inner ellipse, traced by ray casting
            k = 7
            circles = []
            for i in range(k):
                a = -math.pi / 2 + 2 * math.pi * i / k
                circles.append((cx + math.cos(a) * w * 0.30, cy + math.sin(a) * h * 0.24,
                                min(w * 0.22, h * 0.36) * (1.0 if i % 2 == 0 else 0.86)))

            def boundary(jit):
                pts = []
                N = 96
                for i in range(N + 1):
                    t = 2 * math.pi * i / N
                    dx, dy = math.cos(t), math.sin(t)
                    # never fall inside the core ellipse
                    best = 1 / math.sqrt((dx / (w * 0.32)) ** 2 + (dy / (h * 0.27)) ** 2)
                    for (ox, oy, r) in circles:
                        fx, fy = cx - ox, cy - oy
                        b = fx * dx + fy * dy
                        c = fx * fx + fy * fy - r * r
                        disc = b * b - c
                        if disc >= 0:
                            best = max(best, -b + math.sqrt(disc))
                    best += R.j(jit)
                    pts.append((cx + dx * best, cy + dy * best))
                return pts
            out.append(filled(R.smooth(boundary(0), True), fill))
            out.append(strokes([R.smooth(boundary(0.6)), R.smooth(boundary(0.6))]))
            out.append(self._label_block(n, cx, cy))
        elif n.kind == "user":
            cx, y = n.cx, n.y
            head = R.smooth(R.ellipse_pts(cx, y + 12, 11, 11))
            out.append('<circle cx="%s" cy="%s" r="11" fill="%s"/>' % (
                _fmt(cx), _fmt(y + 12), "#ffffff" if fill == "#ffffff" else fill))
            body = " ".join([
                R.line(cx, y + 24, cx, y + 48, 1),
                R.line(cx - 18, y + 33, cx + 18, y + 33, 1),
                R.line(cx, y + 48, cx - 14, y + 68, 1),
                R.line(cx, y + 48, cx + 14, y + 68, 1),
            ])
            out.append(strokes([head]))
            out.append(strokes([body]))
            out.append(self._text_svg(cx, y + 70 + n.size * 1.15, n.label, n.size, INK))
            if n.sub:
                out.append(self._text_svg(cx, y + 70 + n.size * 2.25, n.sub, n.size * 0.8, MUTED))
        elif n.kind == "text":
            anchor = {"left": "start", "center": "middle", "right": "end"}[n.align]
            out.append(self._text_svg(n.x, n.y + n.size, n.label, n.size, n.ink or INK, anchor))
        return "".join(out)

    def _edge_path_points(self, e):
        p1, p2 = self._endpoints(e)
        pts = [p1] + list(e.via) + [p2]
        return pts

    def _edge_svg(self, R, e):
        pts = self._edge_path_points(e)
        color = e.color or INK
        stroke_w = 1.6
        paths = []
        if e.bend and len(pts) == 2:
            (x1, y1), (x2, y2) = pts
            L = math.hypot(x2 - x1, y2 - y1) or 1
            nx, ny = -(y2 - y1) / L, (x2 - x1) / L
            mx, my = (x1 + x2) / 2 + nx * e.bend, (y1 + y2) / 2 + ny * e.bend
            for _ in range(1 if e.dashed else 2):
                paths.append("M%s %s Q%s %s %s %s" % (
                    _fmt(x1 + R.j(1)), _fmt(y1 + R.j(1)), _fmt(mx + R.j(2)), _fmt(my + R.j(2)),
                    _fmt(x2), _fmt(y2)))
            tail_dir = (x2 - mx, y2 - my)
            head_dir = (x1 - mx, y1 - my)
        else:
            seg = []
            for i in range(len(pts) - 1):
                seg.append(R.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1],
                                  1 if e.dashed else 2))
            paths.append(" ".join(seg))
            tail_dir = (pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1])
            head_dir = (pts[0][0] - pts[1][0], pts[0][1] - pts[1][1])
        out = []
        dash = ' stroke-dasharray="7 6"' if e.dashed else ""
        for p in paths:
            out.append('<path d="%s" stroke="%s" stroke-width="%s" fill="none" '
                       'stroke-linecap="round"%s/>' % (p, color, stroke_w, dash))
        heads = []
        if e.head:
            heads.append((pts[-1], tail_dir))
        if e.both:
            heads.append((pts[0], head_dir))
        for (tx, ty), (dx, dy) in heads:
            L = math.hypot(dx, dy) or 1
            ux, uy = dx / L, dy / L
            s = 13
            a = math.radians(26)
            l1 = (tx - s * (ux * math.cos(a) - uy * math.sin(a)), ty - s * (uy * math.cos(a) + ux * math.sin(a)))
            l2 = (tx - s * (ux * math.cos(-a) - uy * math.sin(-a)), ty - s * (uy * math.cos(-a) + ux * math.sin(-a)))
            d = R.line(l1[0], l1[1], tx, ty, 1) + " " + R.line(l2[0], l2[1], tx, ty, 1)
            out.append('<path d="%s" stroke="%s" stroke-width="%s" fill="none" '
                       'stroke-linecap="round"/>' % (d, color, stroke_w + 0.2))
        return "".join(out)

    def _label_point(self, e):
        pts = self._edge_path_points(e)
        if e.bend and len(pts) == 2:
            (x1, y1), (x2, y2) = pts
            L = math.hypot(x2 - x1, y2 - y1) or 1
            nx, ny = -(y2 - y1) / L, (x2 - x1) / L
            return (x1 + x2) / 2 + nx * e.bend / 2, (y1 + y2) / 2 + ny * e.bend / 2
        # walk polyline to label_pos fraction
        lens = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
                for i in range(len(pts) - 1)]
        target = sum(lens) * e.label_pos
        for i, L in enumerate(lens):
            if target <= L or i == len(lens) - 1:
                t = target / L if L else 0
                return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t,
                        pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t)
            target -= L
        return pts[0]

    def _edge_label_svg(self, e):
        x, y = self._label_point(e)
        lines = e.label.split("\n")
        size = e.size
        w = max(text_width(l, size) for l in lines) + 10
        h = len(lines) * size * 1.25 + 4
        return ('<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="#ffffff" fill-opacity="0.92"/>'
                % (_fmt(x - w / 2), _fmt(y - h / 2), _fmt(w), _fmt(h)) +
                self._text_svg(x, y, e.label, size, e.color or MUTED, "middle", True))

    # ------------------------------------------------------------ Excalidraw
    def to_excalidraw(self):
        rnd = random.Random(self.seed)
        els = []
        ids = {}

        def base(id, type, x, y, w, h, stroke=INK, bg="transparent", **extra):
            e = {
                "id": id, "type": type, "x": round(x, 2), "y": round(y, 2),
                "width": round(w, 2), "height": round(h, 2), "angle": 0,
                "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid",
                "strokeWidth": 2, "strokeStyle": "solid", "roughness": 1, "opacity": 100,
                "groupIds": [], "frameId": None, "roundness": None,
                "seed": rnd.randint(1, 2 ** 31), "version": 1,
                "versionNonce": rnd.randint(1, 2 ** 31), "isDeleted": False,
                "boundElements": [], "updated": 1, "link": None, "locked": False,
            }
            e.update(extra)
            els.append(e)
            return e

        def text_el(id, x, y, s, size, container=None, align="center", color=INK):
            lines = s.split("\n")
            w = max(text_width(l, size) for l in lines)
            h = len(lines) * size * 1.25
            return base(id, "text", x, y, w, h, stroke=color, text=s, fontSize=size,
                        fontFamily=1, textAlign=align,
                        verticalAlign="middle" if container else "top",
                        containerId=container, originalText=s, lineHeight=1.25,
                        autoResize=True)

        if self.title:
            x0, y0, _, _ = self.bounds()
            text_el("title", x0 + 26, y0 + 12, self.title, 28, align="left")

        for n in self.order:
            stroke, fill = COLORS.get(n.color, COLORS["white"])
            label = n.label + ("\n" + n.sub if n.sub else "")
            if n.kind in ("box", "stack", "queue", "note", "db", "diamond", "ellipse", "cloud"):
                if n.kind == "stack":
                    g = "g-" + n.id
                    for k in (2, 1):
                        base(n.id + "-shadow%d" % k, "rectangle", n.x + 6 * k, n.y - 6 * k, n.w, n.h,
                             bg=fill, roundness={"type": 3}, groupIds=[g])
                t = {"diamond": "diamond", "ellipse": "ellipse", "cloud": "ellipse"}.get(n.kind, "rectangle")
                el = base(n.id, t, n.x, n.y, n.w, n.h, bg=fill,
                          roundness={"type": 3} if t == "rectangle" else {"type": 2},
                          strokeStyle="dashed" if n.dashed else "solid")
                if n.kind == "stack":
                    el["groupIds"] = ["g-" + n.id]
                if n.kind == "db":
                    ry = min(14, n.h * 0.16)
                    base(n.id + "-lid", "ellipse", n.x, n.y, n.w, ry * 2, bg=fill,
                         roundness={"type": 2})
                if label:
                    tid = n.id + "-label"
                    tx = text_el(tid, n.x, n.y, label, n.size * 1.1, container=n.id,
                                 align="left" if n.kind == "note" else "center")
                    tx["x"] = n.cx - tx["width"] / 2 if n.kind != "note" else n.x + 10
                    tx["y"] = n.cy - tx["height"] / 2
                    el["boundElements"].append({"type": "text", "id": tid})
                ids[n.id] = el
            elif n.kind == "zone":
                el = base(n.id, "rectangle", n.x, n.y, n.w, n.h, stroke=stroke,
                          bg="transparent", strokeStyle="dashed", roundness={"type": 3})
                text_el(n.id + "-label", n.x + 14, n.y + 8, n.label, n.size * 1.1, align="left",
                        color=stroke)
                ids[n.id] = el
            elif n.kind == "user":
                el = base(n.id, "ellipse", n.cx - 22, n.y, 44, 44, bg="#ffffff",
                          roundness={"type": 2})
                t = text_el(n.id + "-label", n.cx, n.y + 52, label, n.size * 1.1)
                t["x"] = n.cx - t["width"] / 2
                ids[n.id] = el
            elif n.kind == "text":
                if not n.label:
                    continue
                t = text_el(n.id, n.x, n.y, n.label, n.size * 1.1,
                            align={"left": "left", "center": "center", "right": "right"}[n.align])
                if n.align == "center":
                    t["x"] = n.x - t["width"] / 2

        for i, e in enumerate(self.edges):
            pts = self._edge_path_points(e)
            if e.bend and len(pts) == 2:
                (x1, y1), (x2, y2) = pts
                L = math.hypot(x2 - x1, y2 - y1) or 1
                nx, ny = -(y2 - y1) / L, (x2 - x1) / L
                pts = [pts[0], ((x1 + x2) / 2 + nx * e.bend * 0.5, (y1 + y2) / 2 + ny * e.bend * 0.5), pts[1]]
            ox, oy = pts[0]
            rel = [[round(px - ox, 2), round(py - oy, 2)] for px, py in pts]
            xs = [p[0] for p in rel]
            ys = [p[1] for p in rel]
            aid = "edge-%d" % i
            a = base(aid, "arrow" if e.head else "line", ox, oy, max(xs) - min(xs), max(ys) - min(ys),
                     stroke=e.color or INK, points=rel, lastCommittedPoint=None,
                     startArrowhead="arrow" if e.both else None,
                     endArrowhead="arrow" if e.head else None,
                     strokeStyle="dashed" if e.dashed else "solid",
                     roundness={"type": 2} if e.bend else None,
                     startBinding=None, endBinding=None, elbowed=False)
            for end, nid in (("startBinding", e.a), ("endBinding", e.b)):
                tgt = ids.get(nid)
                if tgt is not None:
                    a[end] = {"elementId": tgt["id"], "focus": 0, "gap": 6}
                    tgt["boundElements"].append({"type": "arrow", "id": aid})
            if e.label:
                lx, ly = self._label_point(e)
                tid = aid + "-label"
                t = text_el(tid, lx, ly, e.label, e.size * 1.1, container=aid)
                t["x"] = lx - t["width"] / 2
                t["y"] = ly - t["height"] / 2
                a["boundElements"].append({"type": "text", "id": tid})

        return {
            "type": "excalidraw", "version": 2, "source": "blueprint-101/tools/diagrams",
            "elements": els,
            "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
            "files": {},
        }

    # ------------------------------------------------------------ save
    def save(self, out_dir):
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, self.name + ".svg"), "w") as f:
            f.write(self.to_svg())
        src = os.path.join(out_dir, "excalidraw")
        os.makedirs(src, exist_ok=True)
        with open(os.path.join(src, self.name + ".excalidraw"), "w") as f:
            json.dump(self.to_excalidraw(), f, indent=1)


def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
