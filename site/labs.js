/* Interactive labs. Each lab: { blurb, render(root) }. Pure simulation functions are
   exposed on Labs._sim so they can be unit tested outside the browser. */
(function () {
  "use strict";

  // ------------------------------------------------------------ formatting
  function fmtNum(n, d) {
    if (!isFinite(n)) return "inf";
    var a = Math.abs(n), u = [[1e12, "T"], [1e9, "B"], [1e6, "M"], [1e3, "k"]];
    for (var i = 0; i < u.length; i++) if (a >= u[i][0]) return (n / u[i][0]).toFixed(d === undefined ? 1 : d).replace(/\.0$/, "") + u[i][1];
    return a >= 100 ? Math.round(n).toString() : (+n.toFixed(d === undefined ? 1 : d)).toString();
  }
  function fmtBytes(b) {
    var u = ["B", "KB", "MB", "GB", "TB", "PB", "EB"], i = 0;
    while (b >= 1000 && i < u.length - 1) { b /= 1000; i++; }
    return (b >= 100 ? Math.round(b) : +b.toFixed(1)) + " " + u[i];
  }
  function fmtDur(sec) {
    if (sec < 1e-6) return +(sec * 1e9).toFixed(1) + " ns";
    if (sec < 1e-3) return +(sec * 1e6).toFixed(1) + " µs";
    if (sec < 1) return +(sec * 1e3).toFixed(1) + " ms";
    if (sec < 120) return +sec.toFixed(1) + " s";
    if (sec < 7200) return +(sec / 60).toFixed(1) + " min";
    if (sec < 172800) return +(sec / 3600).toFixed(1) + " h";
    if (sec < 63072000) return +(sec / 86400).toFixed(1) + " days";
    return +(sec / 31536000).toFixed(1) + " years";
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var SERIES = ["var(--series-1)", "var(--series-2)", "var(--series-3)", "var(--series-4)", "var(--series-5)"];

  // ------------------------------------------------------------ deterministic rng + hash
  function rng(seed) {
    var s = seed >>> 0 || 1;
    return function () { s ^= s << 13; s ^= s >>> 17; s ^= s << 5; return ((s >>> 0) % 1e9) / 1e9; };
  }
  function fnv(str) {
    var h = 0x811c9dc5;
    for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 0x01000193); }
    h ^= h >>> 15; h = Math.imul(h, 0x2c1b3c6d); h ^= h >>> 12;
    return h >>> 0;
  }

  // ------------------------------------------------------------ UI helpers
  function h(html) { var t = document.createElement("template"); t.innerHTML = html.trim(); return t.content.firstChild; }

  function slider(root, o, onChange) {
    var f = h('<div class="field"><label><span>' + esc(o.label) + '</span><b></b></label><input type="range"></div>');
    var input = f.querySelector("input"), out = f.querySelector("b");
    input.min = o.min; input.max = o.max; input.step = o.step || 1;
    var toVal = o.log ? function (x) { return Math.round(Math.pow(10, x)); } : function (x) { return +x; };
    var fromVal = o.log ? function (v) { return Math.log10(v); } : function (v) { return v; };
    if (o.log) { input.min = Math.log10(o.min); input.max = Math.log10(o.max); input.step = 0.01; }
    input.value = fromVal(o.value);
    input.setAttribute("aria-label", o.label);
    var api = {
      get: function () { return toVal(input.value); },
      set: function (v) { input.value = fromVal(v); show(); },
      el: f
    };
    function show() { out.textContent = (o.fmt || fmtNum)(api.get()); }
    input.addEventListener("input", function () { show(); onChange(); });
    show();
    root.appendChild(f);
    return api;
  }

  function seg(root, label, options, value, onChange) {
    var f = h('<div class="field"><label><span>' + esc(label) + '</span></label><div class="seg" role="group"></div></div>');
    var box = f.querySelector(".seg"), cur = value;
    options.forEach(function (o) {
      var b = h('<button type="button">' + esc(o[1]) + "</button>");
      b.dataset.v = o[0];
      if (o[0] === cur) b.classList.add("on");
      b.addEventListener("click", function () {
        cur = o[0];
        box.querySelectorAll("button").forEach(function (x) { x.classList.toggle("on", x.dataset.v === cur); });
        onChange(cur);
      });
      box.appendChild(b);
    });
    root.appendChild(f);
    return { get: function () { return cur; } };
  }

  function kpis(root, items) {
    root.innerHTML = items.map(function (k) {
      return '<div class="kpi"><span>' + esc(k[0]) + "</span><b>" + k[1] + "</b>" + (k[2] ? "<small>" + k[2] + "</small>" : "") + "</div>";
    }).join("");
  }

  var tipEl = null;
  function tip(e, html) {
    if (html === null && !tipEl) return;
    if (!tipEl) { tipEl = h('<div class="tip" role="status"></div>'); document.body.appendChild(tipEl); }
    if (html === null) { tipEl.style.display = "none"; return; }
    tipEl.innerHTML = html;
    tipEl.style.display = "block";
    var x = e.clientX + 14, y = e.clientY + 14, w = tipEl.offsetWidth;
    if (x + w > window.innerWidth - 8) x = e.clientX - w - 14;
    tipEl.style.left = x + "px"; tipEl.style.top = y + "px";
  }
  function hideTip() { tip(null, null); }

  function legend(series) {
    if (series.length < 2) return "";
    return '<div class="legend">' + series.map(function (s) { return '<span><i style="background:' + s.color + '"></i>' + esc(s.name) + "</span>"; }).join("") + "</div>";
  }

  // vertical bars, grouped or stacked. series: [{name,color,values}]
  function barChart(root, o) {
    var W = o.width || 640, H = o.height || 240, P = { l: 52, r: 12, t: 12, b: 34 };
    var cats = o.categories, n = cats.length, series = o.series;
    var totals = cats.map(function (_, i) {
      return o.stacked ? series.reduce(function (a, s) { return a + s.values[i]; }, 0) : Math.max.apply(null, series.map(function (s) { return s.values[i]; }));
    });
    var max = o.max || Math.max(1e-9, Math.max.apply(null, totals)) * 1.1;
    var iw = W - P.l - P.r, ih = H - P.t - P.b, band = iw / n;
    var gap = 2, groupW = Math.min(o.barMax || 56, band * 0.72);
    var svg = ['<svg class="chart" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="' + esc(o.title || "bar chart") + '">'];
    for (var g = 0; g <= 4; g++) {
      var gy = P.t + ih - (ih * g) / 4;
      svg.push('<line class="grid" x1="' + P.l + '" x2="' + (W - P.r) + '" y1="' + gy + '" y2="' + gy + '"/>');
      svg.push('<text x="' + (P.l - 6) + '" y="' + (gy + 4) + '" text-anchor="end">' + esc((o.yFmt || fmtNum)((max * g) / 4)) + "</text>");
    }
    cats.forEach(function (c, i) {
      var x0 = P.l + band * i + (band - groupW) / 2, acc = 0;
      series.forEach(function (s, si) {
        var v = s.values[i], bh = Math.max(0, (v / max) * ih), x, w, y;
        if (o.stacked) { w = groupW; x = x0; y = P.t + ih - ((acc + v) / max) * ih; acc += v; bh = Math.max(0, bh - (acc > v ? gap : 0)); }
        else { w = (groupW - gap * (series.length - 1)) / series.length; x = x0 + si * (w + gap); y = P.t + ih - bh; }
        if (v > 0) {
          var r = Math.min(4, w / 2, bh);
          svg.push('<path data-tip="' + esc(c + " &middot; " + s.name + ": " + (o.vFmt || o.yFmt || fmtNum)(v)) + '" fill="' + (s.colors ? s.colors[i] : s.color) + '" d="M' + x + " " + (y + bh) +
            "V" + (y + r) + "Q" + x + " " + y + " " + (x + r) + " " + y + "H" + (x + w - r) + "Q" + (x + w) + " " + y + " " + (x + w) + " " + (y + r) + "V" + (y + bh) + 'Z"/>');
        }
      });
      if (!o.hideLabels || i % (o.labelEvery || 1) === 0) {
        svg.push('<text x="' + (P.l + band * i + band / 2) + '" y="' + (H - 12) + '" text-anchor="middle">' + esc(c) + "</text>");
      }
    });
    svg.push('<line class="axis" x1="' + P.l + '" x2="' + (W - P.r) + '" y1="' + (P.t + ih) + '" y2="' + (P.t + ih) + '"/></svg>');
    root.innerHTML = (o.title ? '<h3 style="margin:0 0 4px;font-size:15px">' + esc(o.title) + "</h3>" : "") + legend(series) + svg.join("");
    root.querySelectorAll("[data-tip]").forEach(function (p) {
      p.addEventListener("mousemove", function (e) { tip(e, p.getAttribute("data-tip")); });
      p.addEventListener("mouseleave", hideTip);
    });
  }

  // multi-series line chart with crosshair tooltip
  function lineChart(root, o) {
    var W = o.width || 640, H = o.height || 260, P = { l: 52, r: 90, t: 14, b: 34 };
    var xs = o.x, iw = W - P.l - P.r, ih = H - P.t - P.b;
    var maxY = o.maxY || Math.max.apply(null, o.series.map(function (s) { return Math.max.apply(null, s.values); })) * 1.08 || 1;
    var minX = xs[0], maxX = xs[xs.length - 1];
    function X(v) { return P.l + ((v - minX) / (maxX - minX || 1)) * iw; }
    function Y(v) { return P.t + ih - (v / maxY) * ih; }
    var svg = ['<svg class="chart" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="' + esc(o.title || "line chart") + '">'];
    for (var g = 0; g <= 4; g++) {
      var gy = P.t + ih - (ih * g) / 4;
      svg.push('<line class="grid" x1="' + P.l + '" x2="' + (P.l + iw) + '" y1="' + gy + '" y2="' + gy + '"/>');
      svg.push('<text x="' + (P.l - 6) + '" y="' + (gy + 4) + '" text-anchor="end">' + esc((o.yFmt || fmtNum)((maxY * g) / 4)) + "</text>");
    }
    for (var t = 0; t < xs.length; t += Math.ceil(xs.length / 6)) {
      svg.push('<text x="' + X(xs[t]) + '" y="' + (H - 12) + '" text-anchor="middle">' + esc((o.xFmt || fmtNum)(xs[t])) + "</text>");
    }
    o.series.forEach(function (s) {
      svg.push('<path fill="none" stroke="' + s.color + '" stroke-width="2" stroke-linejoin="round" d="' +
        s.values.map(function (v, i) { return (i ? "L" : "M") + X(xs[i]).toFixed(1) + " " + Y(v).toFixed(1); }).join("") + '"/>');
      var last = s.values[s.values.length - 1];
      svg.push('<text x="' + (P.l + iw + 6) + '" y="' + (Y(last) + 4) + '" style="fill:var(--text)">' + esc(s.name) + "</text>");
    });
    if (o.marker !== undefined) {
      svg.push('<line x1="' + X(o.marker) + '" x2="' + X(o.marker) + '" y1="' + P.t + '" y2="' + (P.t + ih) + '" stroke="var(--text-3)" stroke-dasharray="4 4"/>');
    }
    svg.push('<line class="cross" x1="0" x2="0" y1="' + P.t + '" y2="' + (P.t + ih) + '" stroke="var(--text-3)" style="display:none"/>');
    svg.push('<rect x="' + P.l + '" y="' + P.t + '" width="' + iw + '" height="' + ih + '" fill="transparent" class="hit"/>');
    svg.push('<line class="axis" x1="' + P.l + '" x2="' + (P.l + iw) + '" y1="' + (P.t + ih) + '" y2="' + (P.t + ih) + '"/></svg>');
    root.innerHTML = (o.title ? '<h3 style="margin:0 0 4px;font-size:15px">' + esc(o.title) + "</h3>" : "") + legend(o.series) + svg.join("");
    var svgEl = root.querySelector("svg"), cross = root.querySelector(".cross"), hit = root.querySelector(".hit");
    hit.addEventListener("mousemove", function (e) {
      var r = svgEl.getBoundingClientRect(), px = ((e.clientX - r.left) / r.width) * W;
      var i = 0, best = Infinity;
      xs.forEach(function (x, j) { var d = Math.abs(X(x) - px); if (d < best) { best = d; i = j; } });
      cross.setAttribute("x1", X(xs[i])); cross.setAttribute("x2", X(xs[i])); cross.style.display = "";
      tip(e, "<b>" + esc((o.xFmt || fmtNum)(xs[i])) + "</b><br>" + o.series.map(function (s) {
        return esc(s.name) + ": " + esc((o.yFmt || fmtNum)(s.values[i]));
      }).join("<br>"));
    });
    hit.addEventListener("mouseleave", function () { cross.style.display = "none"; hideTip(); });
  }

  function layout(root, controlsTitle) {
    root.innerHTML = '<div class="lab-grid"><div class="panel controls"><h3>' + esc(controlsTitle || "Inputs") + '</h3></div><div class="out"></div></div>';
    return { controls: root.querySelector(".controls"), out: root.querySelector(".out") };
  }

  var running = [];
  function loop(fn) {
    var alive = true, last = performance.now();
    function frame(now) {
      if (!alive) return;
      fn(Math.min(0.1, (now - last) / 1000));
      last = now;
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
    running.push(function () { alive = false; });
  }

  var Labs = {
    _stop: function () { running.forEach(function (f) { f(); }); running = []; hideTip(); },
    _sim: {}
  };

  // ================================================================ 1. estimator
  function estimate(p) {
    var day = 86400;
    var writesDay = p.dau * p.writes, readsDay = p.dau * p.reads;
    var wqps = writesDay / day, rqps = readsDay / day;
    var peakR = rqps * p.peak, peakW = wqps * p.peak;
    var storageDay = writesDay * p.sizeKB * 1000;
    var storageTotal = storageDay * 365 * p.years * p.replication;
    var egress = peakR * p.respKB * 1000;
    var cache = readsDay * (p.cachePct / 100) * p.respKB * 1000;
    var servers = Math.ceil((peakR + peakW) / p.perServer * 1.3);
    return { wqps: wqps, rqps: rqps, peakR: peakR, peakW: peakW, storageDay: storageDay, storageTotal: storageTotal, egress: egress, cache: cache, servers: servers };
  }
  Labs._sim.estimate = estimate;

  Labs.estimator = {
    blurb: "Turn DAU and per-user behaviour into QPS, peak load, storage, bandwidth, cache size and server count, with the arithmetic shown.",
    render: function (root) {
      var L = layout(root, "Assumptions");
      var presets = {
        twitter: { dau: 150e6, writes: 2, reads: 20, sizeKB: 0.5, respKB: 10, years: 5, replication: 3, peak: 3, cachePct: 20, perServer: 5000 },
        url: { dau: 30e6, writes: 0.1, reads: 10, sizeKB: 0.5, respKB: 0.5, years: 5, replication: 3, peak: 5, cachePct: 20, perServer: 10000 },
        chat: { dau: 500e6, writes: 40, reads: 40, sizeKB: 0.2, respKB: 0.5, years: 2, replication: 3, peak: 2, cachePct: 5, perServer: 20000 }
      };
      var s = {};
      seg(L.controls, "Preset", [["twitter", "Twitter"], ["url", "URL shortener"], ["chat", "Chat app"]], "twitter", function (v) {
        Object.keys(presets[v]).forEach(function (k) { s[k].set(presets[v][k]); });
        update();
      });
      var p = presets.twitter;
      s.dau = slider(L.controls, { label: "Daily active users", min: 1e4, max: 2e9, value: p.dau, log: true }, update);
      s.writes = slider(L.controls, { label: "Writes per user per day", min: 0.1, max: 100, step: 0.1, value: p.writes }, update);
      s.reads = slider(L.controls, { label: "Reads per user per day", min: 1, max: 500, value: p.reads }, update);
      s.sizeKB = slider(L.controls, { label: "Stored size per write (KB)", min: 0.1, max: 5000, step: 0.1, value: p.sizeKB, fmt: function (v) { return v + " KB"; } }, update);
      s.respKB = slider(L.controls, { label: "Response size per read (KB)", min: 0.1, max: 2000, step: 0.1, value: p.respKB, fmt: function (v) { return v + " KB"; } }, update);
      s.years = slider(L.controls, { label: "Retention (years)", min: 1, max: 10, value: p.years }, update);
      s.replication = slider(L.controls, { label: "Replication factor", min: 1, max: 5, value: p.replication }, update);
      s.peak = slider(L.controls, { label: "Peak / average", min: 1, max: 10, step: 0.5, value: p.peak, fmt: function (v) { return v + "x"; } }, update);
      s.cachePct = slider(L.controls, { label: "Hot data to cache (% of daily reads)", min: 1, max: 50, value: p.cachePct, fmt: function (v) { return v + "%"; } }, update);
      s.perServer = slider(L.controls, { label: "QPS one server handles", min: 100, max: 100000, value: p.perServer, log: true }, update);
      L.out.innerHTML = '<div class="kpis"></div><div class="callout" id="verdict"></div><div class="explain"></div>';
      function update() {
        var v = {};
        Object.keys(s).forEach(function (k) { v[k] = s[k].get(); });
        var r = estimate(v);
        kpis(L.out.querySelector(".kpis"), [
          ["Write QPS (avg / peak)", fmtNum(r.wqps) + " / " + fmtNum(r.peakW)],
          ["Read QPS (avg / peak)", fmtNum(r.rqps) + " / " + fmtNum(r.peakR)],
          ["Read:write ratio", fmtNum(v.reads / v.writes) + ":1"],
          ["New data per day", fmtBytes(r.storageDay)],
          ["Total storage", fmtBytes(r.storageTotal), v.years + " years x RF " + v.replication],
          ["Peak egress", fmtBytes(r.egress) + "/s", fmtNum(r.egress * 8 / 1e9, 1) + " Gbps"],
          ["Cache memory", fmtBytes(r.cache)],
          ["App servers", r.servers, "with 30% headroom"]
        ]);
        var notes = [];
        if (r.storageTotal > 20e12) notes.push("Storage will not fit on one machine: plan sharding and tiered storage.");
        if (r.peakW > 5000) notes.push("Peak writes exceed a single relational primary comfortably: consider sharding or a write-optimized store.");
        if (r.peakR > 20000) notes.push("Read-heavy at scale: cache aggressively and add read replicas.");
        if (r.egress > 1e9) notes.push("More than 1 GB/s egress: put a CDN in front for static and media content.");
        if (!notes.length) notes.push("Modest scale: a single primary database with replicas and a cache is likely enough.");
        L.out.querySelector("#verdict").innerHTML = notes.join("<br>");
        L.out.querySelector(".explain").textContent =
          "writes/day  = " + fmtNum(v.dau) + " x " + v.writes + " = " + fmtNum(v.dau * v.writes) + "\n" +
          "write QPS   = writes/day / 86,400 = " + fmtNum(r.wqps) + "  (peak x" + v.peak + " = " + fmtNum(r.peakW) + ")\n" +
          "read QPS    = " + fmtNum(v.dau) + " x " + v.reads + " / 86,400 = " + fmtNum(r.rqps) + "  (peak " + fmtNum(r.peakR) + ")\n" +
          "storage/day = writes/day x " + v.sizeKB + " KB = " + fmtBytes(r.storageDay) + "\n" +
          "total       = storage/day x 365 x " + v.years + " x " + v.replication + " = " + fmtBytes(r.storageTotal) + "\n" +
          "egress      = peak read QPS x " + v.respKB + " KB = " + fmtBytes(r.egress) + "/s\n" +
          "cache       = reads/day x " + v.cachePct + "% x " + v.respKB + " KB = " + fmtBytes(r.cache) + "\n" +
          "servers     = (peak reads + peak writes) / " + fmtNum(v.perServer) + " x 1.3 = " + r.servers;
      }
      update();
    }
  };

  // ================================================================ 2. availability
  function systemAvailability(rows) {
    return rows.reduce(function (acc, r) { return acc * (1 - Math.pow(1 - r.a / 100, r.k)); }, 1);
  }
  Labs._sim.systemAvailability = systemAvailability;

  Labs.availability = {
    blurb: "Compose components in series and add replicas in parallel to see the resulting nines and downtime budget.",
    render: function (root) {
      var L = layout(root, "Request path (in series)");
      var rows = [
        { name: "DNS", a: 99.99, k: 1 }, { name: "Load balancer", a: 99.99, k: 2 },
        { name: "App servers", a: 99.9, k: 3 }, { name: "Cache", a: 99.9, k: 1 }, { name: "Database", a: 99.95, k: 1 }
      ];
      var list = h("<div></div>");
      L.controls.appendChild(list);
      var add = h('<button class="btn small" type="button">+ Add component</button>');
      add.onclick = function () { rows.push({ name: "Service " + (rows.length + 1), a: 99.9, k: 1 }); draw(); };
      L.controls.appendChild(add);
      L.controls.appendChild(h('<p class="lab-note">Availability in %, and how many independent replicas serve that hop (any one replica is enough).</p>'));
      L.out.innerHTML = '<div class="kpis"></div><div class="panel"><table class="data-table"><thead><tr><th>Component</th><th>Single</th><th>Replicas</th><th>Effective</th><th>Downtime / year</th></tr></thead><tbody></tbody></table></div><div class="callout" id="tipbox"></div>';
      function draw() {
        list.innerHTML = "";
        rows.forEach(function (r, i) {
          var row = h('<div class="field" style="grid-template-columns:1fr 84px 60px 28px;align-items:center;display:grid;gap:6px">' +
            '<input type="text" aria-label="Name"><input type="number" step="0.001" min="50" max="99.99999" aria-label="Availability percent">' +
            '<input type="number" min="1" max="9" aria-label="Replicas"><button class="icon-btn" aria-label="Remove" type="button">&times;</button></div>');
          var inputs = row.querySelectorAll("input");
          inputs[0].value = r.name; inputs[1].value = r.a; inputs[2].value = r.k;
          inputs[0].oninput = function () { r.name = this.value; calc(); };
          inputs[1].oninput = function () { r.a = Math.min(99.99999, Math.max(0, +this.value || 0)); calc(); };
          inputs[2].oninput = function () { r.k = Math.max(1, Math.min(9, +this.value || 1)); calc(); };
          row.querySelector("button").onclick = function () { rows.splice(i, 1); draw(); };
          list.appendChild(row);
        });
        calc();
      }
      function calc() {
        var A = systemAvailability(rows), down = (1 - A) * 365 * 86400;
        var nines = A >= 1 ? "inf" : (-Math.log10(1 - A)).toFixed(2);
        kpis(L.out.querySelector(".kpis"), [
          ["System availability", (A * 100).toFixed(4) + "%"], ["Nines", nines],
          ["Downtime per year", fmtDur(down)], ["Downtime per month", fmtDur(down / 12)]
        ]);
        var worst = null;
        L.out.querySelector("tbody").innerHTML = rows.map(function (r) {
          var eff = 1 - Math.pow(1 - r.a / 100, r.k);
          if (!worst || eff < worst.eff) worst = { name: r.name, eff: eff };
          return "<tr><td>" + esc(r.name) + "</td><td>" + r.a + "%</td><td>" + r.k + "</td><td>" + (eff * 100).toFixed(5) + "%</td><td>" + fmtDur((1 - eff) * 365 * 86400) + "</td></tr>";
        }).join("");
        L.out.querySelector("#tipbox").innerHTML = worst ? "Weakest link: <b>" + esc(worst.name) + "</b>. Adding a replica there helps most, as long as replicas fail independently (different AZs, staggered deploys)." : "";
      }
      draw();
    }
  };

  // ================================================================ 3. load balancer simulator
  function makeLB(alg, servers, r) {
    var rr = 0;
    return function (key) {
      if (alg === "rr") { rr = (rr + 1) % servers.length; return servers[rr]; }
      if (alg === "random") return servers[Math.floor(r() * servers.length)];
      if (alg === "least") return servers.reduce(function (a, b) { return b.q < a.q ? b : a; });
      if (alg === "p2c") { var a = servers[Math.floor(r() * servers.length)], b = servers[Math.floor(r() * servers.length)]; return a.q <= b.q ? a : b; }
      return servers[fnv(key) % servers.length];       // ip hash
    };
  }

  function lbStep(state, dt) {
    // Poisson arrivals over dt, each server is a FIFO queue with exponential service.
    var s = state, t0 = s.t, t1 = s.t + dt;
    while (true) {
      if (s.nextArrival > t1) break;
      var t = s.nextArrival;
      s.servers.forEach(function (sv) { drain(sv, t); });
      var key = "client-" + Math.floor(s.r() * (s.hotKeys ? 20 : 1000));
      var sv = s.pick(key);
      var start = Math.max(t, sv.freeAt), svc = -Math.log(1 - s.r()) / (s.baseRate * sv.speed);
      sv.freeAt = start + svc;
      sv.queue.push(sv.freeAt);
      sv.q = sv.queue.length;
      sv.served++;
      s.lat.push(sv.freeAt - t);
      if (s.lat.length > 3000) s.lat.shift();
      s.nextArrival = t - Math.log(1 - s.r()) / s.arrival;
    }
    s.servers.forEach(function (sv) { drain(sv, t1); });
    s.t = t1;
    function drain(sv, now) { while (sv.queue.length && sv.queue[0] <= now) sv.queue.shift(); sv.q = sv.queue.length; }
    return t0;
  }
  function percentile(arr, p) {
    if (!arr.length) return 0;
    var a = arr.slice().sort(function (x, y) { return x - y; });
    return a[Math.min(a.length - 1, Math.floor(a.length * p))];
  }
  Labs._sim.lb = { makeLB: makeLB, step: lbStep, percentile: percentile };

  function newLbState(alg, n, slowSpeed, arrival, hotKeys) {
    var r = rng(42), servers = [];
    for (var i = 0; i < n; i++) servers.push({ name: "S" + (i + 1), speed: i === n - 1 ? slowSpeed : 1, queue: [], q: 0, freeAt: 0, served: 0 });
    return { t: 0, r: r, servers: servers, pick: makeLB(alg, servers, r), baseRate: 25, arrival: arrival, nextArrival: 0, lat: [], hotKeys: hotKeys };
  }

  Labs["load-balancer"] = {
    blurb: "Live simulation: five servers, one of them slower. Switch algorithms and watch queues and tail latency react.",
    render: function (root) {
      var L = layout(root, "Traffic and algorithm");
      var state;
      var alg = seg(L.controls, "Algorithm", [["rr", "Round robin"], ["random", "Random"], ["least", "Least conn"], ["p2c", "Power of 2"], ["hash", "IP hash"]], "rr", reset);
      var load = slider(L.controls, { label: "Offered load (% of capacity)", min: 30, max: 98, value: 75, fmt: function (v) { return v + "%"; } }, reset);
      var slow = slider(L.controls, { label: "Slow server speed", min: 0.2, max: 1, step: 0.05, value: 0.5, fmt: function (v) { return Math.round(v * 100) + "%"; } }, reset);
      var hot = seg(L.controls, "Client keys", [["spread", "1,000 clients"], ["hot", "20 clients (NAT)"]], "spread", reset);
      L.controls.appendChild(h('<p class="lab-note">Each server is a FIFO queue serving 25 req/s (the slow one less). Simulated time runs 5x faster than real time.</p>'));
      L.out.innerHTML = '<div class="kpis"></div><div class="panel"><div id="lbBars"></div></div><div class="callout" id="lbNote"></div>';
      function reset() {
        var n = 5, cap = 25 * (n - 1 + slow.get());
        state = newLbState(alg.get(), n, slow.get(), cap * load.get() / 100, hot.get() === "hot");
      }
      reset();
      var acc = 0;
      loop(function (dt) {
        lbStep(state, dt * 5);
        acc += dt;
        if (acc < 0.2) return;
        acc = 0;
        var p50 = percentile(state.lat, 0.5), p99 = percentile(state.lat, 0.99);
        kpis(L.out.querySelector(".kpis"), [
          ["Simulated time", fmtDur(state.t)], ["p50 latency", fmtDur(p50)], ["p99 latency", fmtDur(p99)],
          ["Requests served", fmtNum(state.servers.reduce(function (a, s) { return a + s.served; }, 0))]
        ]);
        barChart(L.out.querySelector("#lbBars"), {
          title: "Requests waiting in each server's queue", categories: state.servers.map(function (s) { return s.name + (s.speed < 1 ? " (slow)" : ""); }),
          series: [{ name: "Queued", color: SERIES[0], values: state.servers.map(function (s) { return s.q; }) }],
          max: Math.max(10, Math.max.apply(null, state.servers.map(function (s) { return s.q; })) * 1.2), height: 220
        });
        var a = alg.get(), msg = {
          rr: "Round robin ignores load: the slow server receives the same share as the others and its queue grows, which drives up p99.",
          random: "Random spreads load evenly on average but still ignores queue depth, so the slow server's queue builds up.",
          least: "Least connections sends new work to the shortest queue, so the slow server automatically gets less traffic.",
          p2c: "Power of two choices samples two servers and picks the less loaded: near least-connections quality without global state.",
          hash: "IP hash pins each client to a server. With few clients (NAT), load becomes very uneven."
        }[a];
        L.out.querySelector("#lbNote").textContent = msg;
      });
    }
  };

  // ================================================================ 4. hash ring
  function ringOwner(ring, key) {
    var h = fnv(key), lo = 0, hi = ring.length;
    while (lo < hi) { var mid = (lo + hi) >> 1; if (ring[mid].pos <= h) lo = mid + 1; else hi = mid; }
    return ring[lo % ring.length].node;
  }
  function buildRing(nodes, vnodes) {
    var ring = [];
    nodes.forEach(function (n) { for (var i = 0; i < vnodes; i++) ring.push({ pos: fnv(n + "#" + i), node: n }); });
    return ring.sort(function (a, b) { return a.pos - b.pos; });
  }
  Labs._sim.ring = { build: buildRing, owner: ringOwner };

  Labs["hash-ring"] = {
    blurb: "Add and remove nodes on a consistent hash ring, tune virtual nodes, and compare keys moved against modulo hashing.",
    render: function (root) {
      var L = layout(root, "Ring");
      var names = ["A", "B", "C", "D", "E"], nodes = ["A", "B", "C"];
      var KEYS = [];
      for (var i = 0; i < 2000; i++) KEYS.push("key-" + i);
      var prevOwner = null, moved = null, modMoved = null;
      var v = slider(L.controls, { label: "Virtual nodes per server", min: 1, max: 200, value: 1 }, function () { prevOwner = null; moved = null; draw(); });
      var btns = h('<div class="seg"><button type="button" id="add">+ Add node</button><button type="button" id="rem">- Remove node</button></div>');
      L.controls.appendChild(btns);
      L.controls.appendChild(h('<p class="lab-note">2,000 sample keys. Up to 5 nodes (one fixed color each). With 1 vnode, arcs are very uneven; try 100+.</p>'));
      btns.querySelector("#add").onclick = function () { if (nodes.length < 5) change(nodes.concat(names[nodes.length])); };
      btns.querySelector("#rem").onclick = function () { if (nodes.length > 1) change(nodes.slice(0, -1)); };
      L.out.innerHTML = '<div class="kpis"></div><div class="panel" style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px;align-items:center"><div id="ringSvg"></div><div id="dist"></div></div>';
      function owners() { var ring = buildRing(nodes, v.get()); return KEYS.map(function (k) { return ringOwner(ring, k); }); }
      function change(next) {
        var before = owners(), n0 = nodes.length;
        nodes = next;
        var after = owners();
        moved = after.filter(function (o, i) { return o !== before[i]; }).length / KEYS.length;
        modMoved = KEYS.filter(function (k) { var x = fnv(k); return x % n0 !== x % nodes.length; }).length / KEYS.length;
        draw();
      }
      function color(n) { return SERIES[names.indexOf(n)]; }
      function draw() {
        var ring = buildRing(nodes, v.get()), own = KEYS.map(function (k) { return ringOwner(ring, k); });
        var R = 120, C = 150, svg = ['<svg class="chart" viewBox="0 0 300 300" role="img" aria-label="Hash ring"><circle cx="150" cy="150" r="120" fill="none" stroke="var(--border)" stroke-width="10"/>'];
        KEYS.slice(0, 400).forEach(function (k, i) {
          var a = (fnv(k) / 4294967296) * 2 * Math.PI - Math.PI / 2;
          svg.push('<circle cx="' + (C + (R - 22) * Math.cos(a)).toFixed(1) + '" cy="' + (C + (R - 22) * Math.sin(a)).toFixed(1) + '" r="2.2" fill="' + color(own[i]) + '"/>');
        });
        if (ring.length <= 300) {
          ring.forEach(function (p) {
            var a = (p.pos / 4294967296) * 2 * Math.PI - Math.PI / 2;
            svg.push('<circle cx="' + (C + R * Math.cos(a)).toFixed(1) + '" cy="' + (C + R * Math.sin(a)).toFixed(1) + '" r="' + (ring.length > 60 ? 3 : 6) +
              '" fill="' + color(p.node) + '" stroke="var(--surface)" stroke-width="2"/>');
          });
        }
        svg.push("</svg>");
        L.out.querySelector("#ringSvg").innerHTML = svg.join("");
        var counts = nodes.map(function (n) { return own.filter(function (o) { return o === n; }).length; });
        barChart(L.out.querySelector("#dist"), {
          title: "Keys per node", categories: nodes.map(function (n) { return "Node " + n; }), height: 230, width: 360,
          series: [{ name: "Keys", color: SERIES[0], colors: nodes.map(color), values: counts }]
        });
        var ideal = KEYS.length / nodes.length, worst = Math.max.apply(null, counts) / ideal;
        kpis(L.out.querySelector(".kpis"), [
          ["Nodes / ring positions", nodes.length + " / " + ring.length],
          ["Most loaded vs ideal", worst.toFixed(2) + "x"],
          ["Keys moved by last change", moved === null ? "n/a" : (moved * 100).toFixed(1) + "%", "consistent hashing"],
          ["Modulo hashing would move", modMoved === null ? "n/a" : (modMoved * 100).toFixed(1) + "%", "hash % N"]
        ]);
      }
      draw();
    }
  };

  // ================================================================ 5. rate limiter
  function makeLimiter(kind, limit, windowS) {
    var st = { tokens: limit, last: 0, counts: {}, log: [] };
    return {
      state: st,
      allow: function (t) {
        if (kind === "token") {
          st.tokens = Math.min(limit, st.tokens + (t - st.last) * (limit / windowS));
          st.last = t;
          if (st.tokens >= 1) { st.tokens -= 1; return true; }
          return false;
        }
        if (kind === "fixed") {
          var b = Math.floor(t / windowS);
          if ((st.counts[b] || 0) >= limit) return false;
          st.counts[b] = (st.counts[b] || 0) + 1;
          return true;
        }
        if (kind === "log") {
          while (st.log.length && st.log[0] <= t - windowS) st.log.shift();
          if (st.log.length >= limit) return false;
          st.log.push(t);
          return true;
        }
        var cur = Math.floor(t / windowS), el = (t % windowS) / windowS;
        var est = (st.counts[cur] || 0) + (st.counts[cur - 1] || 0) * (1 - el);
        if (est >= limit) return false;
        st.counts[cur] = (st.counts[cur] || 0) + 1;
        return true;
      }
    };
  }
  Labs._sim.makeLimiter = makeLimiter;

  Labs["rate-limiter"] = {
    blurb: "Fire traffic at four rate limiting algorithms and watch what gets accepted or rejected over time, including the fixed-window boundary burst.",
    render: function (root) {
      var L = layout(root, "Limiter");
      var lim, t = 0, buckets = [], BUCKET = 0.5, SPAN = 40, pending = 0;
      var kind = seg(L.controls, "Algorithm", [["token", "Token bucket"], ["fixed", "Fixed window"], ["log", "Sliding log"], ["counter", "Sliding counter"]], "token", reset);
      var limit = slider(L.controls, { label: "Limit (requests per window)", min: 1, max: 50, value: 10 }, reset);
      var win = slider(L.controls, { label: "Window (seconds)", min: 1, max: 20, value: 5, fmt: function (v) { return v + " s"; } }, reset);
      var rate = slider(L.controls, { label: "Background traffic (req/s)", min: 0, max: 20, step: 0.5, value: 3 }, function () {});
      var b = h('<div class="seg"><button type="button" id="one">Send 1</button><button type="button" id="burst">Burst 20</button><button type="button" id="edge">Burst at window edge</button></div>');
      L.controls.appendChild(b);
      b.querySelector("#one").onclick = function () { pending += 1; };
      b.querySelector("#burst").onclick = function () { pending += 20; };
      b.querySelector("#edge").onclick = function () {
        var w = win.get(), toEdge = w - (t % w) - 0.3;
        setTimeout(function () { pending += limit.get(); setTimeout(function () { pending += limit.get(); }, 500); }, Math.max(0, toEdge) * 1000);
      };
      L.controls.appendChild(h('<p class="lab-note">"Burst at window edge" sends a full limit just before a window boundary and another just after: fixed window lets both through.</p>'));
      L.out.innerHTML = '<div class="kpis"></div><div class="panel"><div id="rlChart"></div></div>';
      function reset() { lim = makeLimiter(kind.get(), limit.get(), win.get()); buckets = []; }
      reset();
      var acc = 0, redraw = 0, totalOk = 0, totalNo = 0;
      loop(function (dt) {
        t += dt;
        acc += dt * rate.get();
        var n = pending;
        pending = 0;
        while (acc >= 1) { n++; acc -= 1; }
        var bi = Math.floor(t / BUCKET);
        if (!buckets.length || buckets[buckets.length - 1].i !== bi) buckets.push({ i: bi, ok: 0, no: 0 });
        var cur = buckets[buckets.length - 1];
        for (var k = 0; k < n; k++) {
          if (lim.allow(t + k * 1e-4)) { cur.ok++; totalOk++; } else { cur.no++; totalNo++; }
        }
        while (buckets.length > SPAN / BUCKET) buckets.shift();
        if ((redraw += dt) < 0.25) return;
        redraw = 0;
        var st = lim.state, k2 = kind.get();
        kpis(L.out.querySelector(".kpis"), [
          ["Accepted", fmtNum(totalOk)], ["Rejected (429)", fmtNum(totalNo)],
          ["Limit", limit.get() + " / " + win.get() + " s", "= " + (limit.get() / win.get()).toFixed(1) + " req/s average"],
          k2 === "token" ? ["Tokens in bucket", st.tokens.toFixed(1) + " / " + limit.get()] : k2 === "log" ? ["Timestamps stored", st.log.length] : ["Window", "#" + Math.floor(t / win.get())]
        ]);
        var cats = buckets.map(function (x) { return (x.i * BUCKET).toFixed(0) + "s"; });
        barChart(L.out.querySelector("#rlChart"), {
          title: "Requests per 0.5 s", stacked: true, categories: cats, hideLabels: true, labelEvery: 10, height: 240, barMax: 14,
          series: [{ name: "Accepted", color: SERIES[2], values: buckets.map(function (x) { return x.ok; }) },
                   { name: "Rejected", color: SERIES[1], values: buckets.map(function (x) { return x.no; }) }]
        });
      });
    }
  };

  // ================================================================ 6. cache eviction
  function zipfTrace(n, items, s, scan, seed) {
    var r = rng(seed || 3), cdf = [], sum = 0, i;
    for (i = 1; i <= items; i++) { sum += 1 / Math.pow(i, s); cdf.push(sum); }
    var trace = [], scanId = 0;
    for (i = 0; i < n; i++) {
      if (scan && i % 1000 >= 700) { trace.push("scan-" + scanId++); continue; }
      var u = r() * sum, lo = 0, hi = cdf.length - 1;
      while (lo < hi) { var mid = (lo + hi) >> 1; if (cdf[mid] < u) lo = mid + 1; else hi = mid; }
      trace.push("item-" + lo);
    }
    return trace;
  }
  function simulateCache(trace, cap, policy) {
    var hits = 0, map = new Map(), freq = new Map(), r = rng(11), order = [];
    for (var i = 0; i < trace.length; i++) {
      var k = trace[i];
      if (map.has(k)) {
        hits++;
        if (policy === "lru") { map.delete(k); map.set(k, 1); }
        if (policy === "lfu") freq.set(k, freq.get(k) + 1);
        continue;
      }
      if (map.size >= cap) {
        var victim;
        if (policy === "lru" || policy === "fifo") victim = map.keys().next().value;
        else if (policy === "random") { if (!order.length) order = Array.from(map.keys()); var j = Math.floor(r() * order.length); victim = order[j]; order.splice(j, 1); }
        else { var best = Infinity; map.forEach(function (_, key) { var f = freq.get(key); if (f < best) { best = f; victim = key; } }); }
        map.delete(victim);
        freq.delete(victim);
      }
      map.set(k, 1);
      freq.set(k, 1);
      if (policy === "random" && order.length) order.push(k);
    }
    return hits / trace.length;
  }
  Labs._sim.cache = { zipfTrace: zipfTrace, simulate: simulateCache };

  Labs.cache = {
    blurb: "Replay a skewed access pattern through LRU, LFU, FIFO and Random caches, and find the knee of the hit-ratio curve.",
    render: function (root) {
      var L = layout(root, "Workload");
      var cap = slider(L.controls, { label: "Cache capacity (items)", min: 10, max: 500, step: 10, value: 100 }, update);
      var skew = slider(L.controls, { label: "Popularity skew (Zipf s)", min: 0.3, max: 1.6, step: 0.1, value: 1.0 }, update);
      var items = slider(L.controls, { label: "Distinct items", min: 200, max: 5000, step: 100, value: 1000 }, update);
      var scan = seg(L.controls, "Background scans", [["no", "Off"], ["yes", "30% one-time scans"]], "no", update);
      L.controls.appendChild(h('<p class="lab-note">8,000 requests. Scans model a batch job reading many items once, which pollutes LRU.</p>'));
      L.out.innerHTML = '<div class="kpis"></div><div class="panel" id="cBars"></div><div class="panel" id="cCurve" style="margin-top:14px"></div>';
      var POL = [["lru", "LRU"], ["lfu", "LFU"], ["fifo", "FIFO"], ["random", "Random"]];
      var timer = null;
      function update() { clearTimeout(timer); timer = setTimeout(run, 60); }
      function run() {
        var trace = zipfTrace(8000, items.get(), skew.get(), scan.get() === "yes");
        var at = POL.map(function (p) { return simulateCache(trace, cap.get(), p[0]); });
        kpis(L.out.querySelector(".kpis"), POL.map(function (p, i) { return [p[1] + " hit ratio", (at[i] * 100).toFixed(1) + "%"]; }));
        barChart(L.out.querySelector("#cBars"), {
          title: "Hit ratio at " + cap.get() + " items", categories: POL.map(function (p) { return p[1]; }), height: 200, max: 1,
          yFmt: function (v) { return Math.round(v * 100) + "%"; },
          series: [{ name: "Hit ratio", color: SERIES[0], values: at }]
        });
        var sizes = [];
        for (var c = 10; c <= 500; c += 30) sizes.push(c);
        lineChart(L.out.querySelector("#cCurve"), {
          title: "Hit ratio vs cache size", x: sizes, marker: cap.get(), maxY: 1, yFmt: function (v) { return Math.round(v * 100) + "%"; },
          xFmt: function (v) { return v + " items"; },
          series: POL.slice(0, 3).map(function (p, i) { return { name: p[1], color: SERIES[i], values: sizes.map(function (s) { return simulateCache(trace, s, p[0]); }) }; })
        });
      }
      run();
    }
  };

  // ================================================================ 7. quorum
  function quorum(n, r, w, failed) {
    var alive = n - failed;
    return { writeOk: alive >= w, readOk: alive >= r, overlap: r + w > n, tolW: n - w, tolR: n - r };
  }
  Labs._sim.quorum = quorum;

  Labs.quorum = {
    blurb: "Pick N, R and W, fail some replicas, and see when reads overlap the latest write and when the system stops accepting requests.",
    render: function (root) {
      var L = layout(root, "Replication settings");
      var n = slider(L.controls, { label: "Replicas (N)", min: 1, max: 9, value: 3 }, clamp);
      var w = slider(L.controls, { label: "Write quorum (W)", min: 1, max: 9, value: 2 }, clamp);
      var r = slider(L.controls, { label: "Read quorum (R)", min: 1, max: 9, value: 2 }, clamp);
      var f = slider(L.controls, { label: "Failed replicas", min: 0, max: 9, value: 0 }, clamp);
      L.out.innerHTML = '<div class="kpis"></div><div class="panel"><div id="qViz"></div><div class="legend"><span><i style="background:' + SERIES[2] + '"></i>acknowledged the write (W)</span><span><i style="background:' + SERIES[0] + '"></i>queried by the read (R)</span><span><i style="background:var(--surface-2)"></i>failed</span></div></div><div class="callout" id="qMsg"></div>';
      function clamp() {
        var N = n.get();
        if (w.get() > N) w.set(N);
        if (r.get() > N) r.set(N);
        if (f.get() > N) f.set(N);
        draw();
      }
      function draw() {
        var N = n.get(), W = w.get(), R = r.get(), F = f.get(), q = quorum(N, R, W, F);
        kpis(L.out.querySelector(".kpis"), [
          ["Writes", q.writeOk ? "available" : "blocked", "need " + W + " of " + (N - F) + " alive"],
          ["Reads", q.readOk ? "available" : "blocked", "need " + R + " of " + (N - F) + " alive"],
          ["R + W > N", q.overlap ? "yes: overlap" : "no: may read stale", R + " + " + W + " vs " + N],
          ["Failures tolerated", "writes " + q.tolW + ", reads " + q.tolR]
        ]);
        var svg = ['<svg class="chart" viewBox="0 0 ' + (N * 90 + 20) + ' 130" role="img" aria-label="Replicas">'];
        for (var i = 0; i < N; i++) {
          var dead = i >= N - F, inW = i < W, inR = i >= N - R - F && i < N - F;
          var x = 20 + i * 90;
          svg.push('<rect x="' + x + '" y="20" width="70" height="80" rx="10" fill="' + (dead ? "var(--surface-2)" : inW ? SERIES[2] : "var(--surface)") +
            '" stroke="' + (inR ? SERIES[0] : "var(--border)") + '" stroke-width="' + (inR ? 4 : 1.5) + '"' + (dead ? ' stroke-dasharray="5 4"' : "") + "/>");
          svg.push('<text x="' + (x + 35) + '" y="64" text-anchor="middle" style="fill:' + (inW && !dead ? "#fff" : "var(--text)") + ';font-weight:600">' + (dead ? "down" : "v" + (inW ? 2 : 1)) + "</text>");
          svg.push('<text x="' + (x + 35) + '" y="120" text-anchor="middle">R' + (i + 1) + "</text>");
        }
        L.out.querySelector("#qViz").innerHTML = svg.join("") + "</svg>";
        var msg = !q.writeOk ? "Too many replicas are down to collect " + W + " write acks: writes fail (or a sloppy quorum hands them to other nodes)." :
          !q.overlap ? "R + W <= N: a read can land entirely on replicas that missed the latest write and return stale data. Faster, but only eventually consistent." :
          "Every read set intersects every write set, so at least one replica in each read has the latest version. Pick the highest version and read-repair the rest.";
        L.out.querySelector("#qMsg").textContent = msg;
      }
      draw();
    }
  };

  // ================================================================ 8. retry storm
  function retrySim(policy, clients, downFor, capacity, horizon, seed) {
    var r = rng(seed || 5), BUCKET = 0.1, nb = Math.ceil(horizon / BUCKET);
    var attempts = new Array(nb).fill(0), pending = [], done = 0, lastDone = 0, total = 0;
    for (var c = 0; c < clients; c++) pending.push({ t: r() * 0.2, n: 0, prev: 0.1 });
    for (var b = 0; b < nb; b++) {
      var t0 = b * BUCKET, t1 = t0 + BUCKET, now = pending.filter(function (p) { return p.t < t1; });
      pending = pending.filter(function (p) { return p.t >= t1; });
      var cap = t0 >= downFor ? capacity * BUCKET : 0;
      attempts[b] = now.length;
      total += now.length;
      for (var i = 0; i < now.length; i++) {
        var p = now[i];
        if (cap > 0 && r() < cap / now.length) { done++; lastDone = t1; continue; }
        p.n++;
        var base = 0.1, max = 10, delay;
        if (policy === "fixed") delay = 1;
        else if (policy === "exp") delay = Math.min(max, base * Math.pow(2, p.n));
        else if (policy === "full") delay = r() * Math.min(max, base * Math.pow(2, p.n));
        else { delay = Math.min(max, base + r() * (p.prev * 3 - base)); p.prev = delay; }
        p.t = t1 + delay;
        pending.push(p);
      }
    }
    return { attempts: attempts, done: done, total: total, lastDone: lastDone, peak: Math.max.apply(null, attempts) / BUCKET };
  }
  Labs._sim.retrySim = retrySim;

  Labs.retry = {
    blurb: "A dependency goes down and 1,000 clients retry. Compare fixed intervals, exponential backoff and jitter by the load they create during recovery.",
    render: function (root) {
      var L = layout(root, "Scenario");
      var POL = [["fixed", "Fixed 1 s"], ["exp", "Exponential"], ["full", "Exp + full jitter"], ["decor", "Decorrelated jitter"]];
      var pol = seg(L.controls, "Retry policy", POL, "exp", draw);
      var clients = slider(L.controls, { label: "Clients", min: 100, max: 5000, step: 100, value: 1000 }, draw);
      var down = slider(L.controls, { label: "Outage length", min: 1, max: 15, value: 5, fmt: function (v) { return v + " s"; } }, draw);
      var cap = slider(L.controls, { label: "Capacity after recovery (req/s)", min: 100, max: 5000, step: 100, value: 1000 }, draw);
      L.controls.appendChild(h('<p class="lab-note">Requests above capacity fail and retry again. Backoff base 100 ms, cap 10 s.</p>'));
      L.out.innerHTML = '<div class="kpis"></div><div class="panel" id="rChart"></div><div class="panel" style="margin-top:14px"><table class="data-table"><thead><tr><th>Policy</th><th>Total attempts</th><th>Peak load</th><th>All recovered by</th></tr></thead><tbody></tbody></table></div>';
      function draw() {
        var H = 30, res = retrySim(pol.get(), clients.get(), down.get(), cap.get(), H);
        kpis(L.out.querySelector(".kpis"), [
          ["Total attempts", fmtNum(res.total), "for " + fmtNum(clients.get()) + " requests"],
          ["Peak load", fmtNum(res.peak) + " req/s", "capacity " + fmtNum(cap.get())],
          ["Clients recovered", fmtNum(res.done) + " / " + fmtNum(clients.get())],
          ["Last success at", res.done ? res.lastDone.toFixed(1) + " s" : "n/a"]
        ]);
        var cats = res.attempts.map(function (_, i) { return (i / 10).toFixed(0) + "s"; });
        barChart(L.out.querySelector("#rChart"), {
          title: "Attempts per 100 ms (outage ends at " + down.get() + " s)", categories: cats, hideLabels: true, labelEvery: 20, height: 240, barMax: 6,
          series: [{ name: "Attempts", color: SERIES[0], values: res.attempts }]
        });
        L.out.querySelector("tbody").innerHTML = POL.map(function (p) {
          var x = retrySim(p[0], clients.get(), down.get(), cap.get(), H);
          return "<tr><td>" + p[1] + "</td><td>" + fmtNum(x.total) + "</td><td>" + fmtNum(x.peak) + "/s</td><td>" + (x.done === clients.get() ? x.lastDone.toFixed(1) + " s" : "not within 30 s") + "</td></tr>";
        }).join("");
      }
      draw();
    }
  };

  // ================================================================ 9. fanout calculator
  function fanout(p) {
    var tweetsS = (p.dau * p.tweets) / 86400, loadsS = (p.dau * p.loads) / 86400;
    var celebTweetsS = tweetsS * (p.celebPct / 100), normalTweetsS = tweetsS - celebTweetsS;
    return {
      tweetsS: tweetsS, loadsS: loadsS,
      push: { writes: normalTweetsS * p.followers + celebTweetsS * p.celebFollowers, reads: loadsS },
      pull: { writes: tweetsS, reads: loadsS * p.following },
      hybrid: { writes: normalTweetsS * p.followers + celebTweetsS, reads: loadsS * (1 + p.celebsFollowed) }
    };
  }
  Labs._sim.fanout = fanout;

  Labs.fanout = {
    blurb: "Compare fanout-on-write, fanout-on-read and the hybrid model for a Twitter-like timeline in operations per second.",
    render: function (root) {
      var L = layout(root, "Workload");
      var s = {
        dau: slider(L.controls, { label: "Daily active users", min: 1e5, max: 1e9, value: 2e8, log: true }, draw),
        tweets: slider(L.controls, { label: "Posts per user per day", min: 0.1, max: 20, step: 0.1, value: 2 }, draw),
        loads: slider(L.controls, { label: "Timeline loads per user per day", min: 1, max: 100, value: 20 }, draw),
        followers: slider(L.controls, { label: "Avg followers (normal users)", min: 10, max: 2000, value: 200 }, draw),
        following: slider(L.controls, { label: "Avg accounts followed", min: 10, max: 2000, value: 300 }, draw),
        celebPct: slider(L.controls, { label: "Posts from celebrities (%)", min: 0, max: 20, step: 0.5, value: 2, fmt: function (v) { return v + "%"; } }, draw),
        celebFollowers: slider(L.controls, { label: "Avg celebrity followers", min: 1e5, max: 2e8, value: 2e7, log: true }, draw),
        celebsFollowed: slider(L.controls, { label: "Celebrities followed per user", min: 0, max: 100, value: 10 }, draw)
      };
      L.out.innerHTML = '<div class="kpis"></div><div class="panel" id="fW"></div><div class="panel" id="fR" style="margin-top:14px"></div><div class="callout" id="fMsg"></div>';
      function draw() {
        var p = {};
        Object.keys(s).forEach(function (k) { p[k] = s[k].get(); });
        var r = fanout(p);
        kpis(L.out.querySelector(".kpis"), [
          ["Posts per second", fmtNum(r.tweetsS)], ["Timeline loads per second", fmtNum(r.loadsS)],
          ["Push: timeline inserts/s", fmtNum(r.push.writes)], ["Pull: reads/s", fmtNum(r.pull.reads)]
        ]);
        var cats = ["Push", "Pull", "Hybrid"];
        barChart(L.out.querySelector("#fW"), { title: "Write side: timeline inserts per second", categories: cats, height: 190,
          series: [{ name: "Inserts/s", color: SERIES[0], values: [r.push.writes, r.pull.writes, r.hybrid.writes] }] });
        barChart(L.out.querySelector("#fR"), { title: "Read side: storage lookups per second", categories: cats, height: 190,
          series: [{ name: "Lookups/s", color: SERIES[1], values: [r.push.reads, r.pull.reads, r.hybrid.reads] }] });
        var celebShare = (r.push.writes - r.hybrid.writes) / r.push.writes;
        L.out.querySelector("#fMsg").innerHTML = "Celebrities cause <b>" + Math.round(celebShare * 100) + "%</b> of push fanout writes. " +
          "The hybrid skips their fanout and pays only " + p.celebsFollowed + " extra lookups per timeline load.";
      }
      draw();
    }
  };

  // ================================================================ 10. latency numbers
  var LAT = [
    ["L1 cache reference", 1e-9], ["Branch mispredict", 3e-9], ["L2 cache reference", 4e-9], ["Mutex lock/unlock", 17e-9],
    ["Main memory reference", 100e-9], ["Compress 1 KB (zstd)", 2e-6], ["Read 1 MB from memory", 3e-6],
    ["SSD random read", 16e-6], ["Read 1 MB from NVMe SSD", 50e-6], ["Datacenter round trip", 500e-6],
    ["Read 1 MB from HDD", 1e-3], ["HDD seek", 5e-3], ["US East to US West round trip", 60e-3],
    ["US to Europe round trip", 100e-3], ["US to India round trip", 230e-3], ["TCP + TLS 1.3 setup across an ocean", 450e-3]
  ];
  Labs.latency = {
    blurb: "The latency numbers every engineer should know, on a log scale, with a human-scale mode where 1 ns becomes 1 second.",
    render: function (root) {
      var L = layout(root, "View");
      var mode = seg(L.controls, "Scale", [["real", "Real time"], ["human", "1 ns = 1 s"]], "real", draw);
      L.controls.appendChild(h('<p class="lab-note">Bars use a logarithmic axis: each grid step is 10x. Hover a bar for the exact value.</p>'));
      L.out.innerHTML = '<div class="panel" id="latChart"></div>';
      function draw() {
        var human = mode.get() === "human", W = 700, rowH = 26, P = 250, H = LAT.length * rowH + 30;
        var lo = Math.log10(1e-9), hi = Math.log10(1), iw = W - P - 20;
        var svg = ['<svg class="chart" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="Latency numbers">'];
        for (var e = -9; e <= 0; e++) {
          var gx = P + ((e - lo) / (hi - lo)) * iw;
          svg.push('<line class="grid" x1="' + gx + '" x2="' + gx + '" y1="0" y2="' + (H - 24) + '"/>');
          if (e % 3 === 0) svg.push('<text x="' + gx + '" y="' + (H - 8) + '" text-anchor="middle">' + fmtDur(human ? Math.pow(10, e) * 1e9 : Math.pow(10, e)) + "</text>");
        }
        LAT.forEach(function (row, i) {
          var v = row[1], wv = ((Math.log10(v) - lo) / (hi - lo)) * iw + 4, y = i * rowH + 4;
          var label = human ? fmtDur(v * 1e9) : fmtDur(v);
          svg.push('<text x="' + (P - 8) + '" y="' + (y + 15) + '" text-anchor="end" style="fill:var(--text)">' + esc(row[0]) + "</text>");
          svg.push('<rect data-tip="' + esc(row[0] + ": " + label) + '" x="' + P + '" y="' + (y + 3) + '" width="' + wv.toFixed(1) + '" height="16" rx="4" fill="' + SERIES[0] + '"/>');
          svg.push('<text x="' + (P + wv + 6) + '" y="' + (y + 15) + '">' + esc(label) + "</text>");
        });
        L.out.querySelector("#latChart").innerHTML = svg.join("") + "</svg>";
        L.out.querySelectorAll("[data-tip]").forEach(function (p) {
          p.addEventListener("mousemove", function (ev) { tip(ev, p.getAttribute("data-tip")); });
          p.addEventListener("mouseleave", hideTip);
        });
      }
      draw();
    }
  };

  window.Labs = Labs;
})();
