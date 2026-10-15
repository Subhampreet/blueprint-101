/* Blueprint 101 reader: routing, rendering, progress, search, flashcards, gallery. */
(function () {
  "use strict";

  var DATA = window.BLUEPRINT;
  var main = document.getElementById("main");
  if (!DATA) {
    main.innerHTML = '<div class="callout bad">content.js is missing. Run <code>python3 tools/build_site.py</code> first.</div>';
    return;
  }

  // ------------------------------------------------------------ storage (never throws)
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem("bp-" + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem("bp-" + k, JSON.stringify(v)); } catch (e) { /* private mode */ } }
  };
  var done = store.get("done", {});
  var collapsed = store.get("collapsed", {});

  // ------------------------------------------------------------ helpers
  var ORDER = [];
  DATA.sections.forEach(function (s) { s.notes.forEach(function (n) { ORDER.push(n); }); });
  var SECTION = {};
  DATA.sections.forEach(function (s) { SECTION[s.id] = s; });

  function el(html) { var t = document.createElement("template"); t.innerHTML = html.trim(); return t.content.firstChild; }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function slugify(s) { return s.toLowerCase().trim().replace(/<[^>]+>/g, "").replace(/[^\w\s-]/g, "").replace(/\s+/g, "-"); }
  function noteHref(slug, anchor) { return "#/note/" + slug + (anchor ? "~" + anchor : ""); }
  function pct(a, b) { return b ? Math.round((a / b) * 100) : 0; }
  function doneCount(slugs) { return slugs.filter(function (s) { return done[s]; }).length; }
  function normalize(path) {
    var parts = [], segs = path.split("/");
    for (var i = 0; i < segs.length; i++) {
      if (segs[i] === "..") parts.pop();
      else if (segs[i] !== "." && segs[i] !== "") parts.push(segs[i]);
    }
    return parts.join("/");
  }

  // ------------------------------------------------------------ sidebar
  function renderNav(activeSlug) {
    var nav = document.getElementById("nav");
    nav.innerHTML = "";
    DATA.sections.forEach(function (sec) {
      var c = doneCount(sec.notes);
      var wrap = el('<div class="nav-section' + (collapsed[sec.id] ? " collapsed" : "") + '"></div>');
      var btn = el('<button aria-expanded="' + !collapsed[sec.id] + '"><span>' + esc(sec.title) +
        '</span><span class="count">' + c + "/" + sec.notes.length + "</span></button>");
      btn.addEventListener("click", function () {
        collapsed[sec.id] = !collapsed[sec.id];
        store.set("collapsed", collapsed);
        wrap.classList.toggle("collapsed");
        btn.setAttribute("aria-expanded", !collapsed[sec.id]);
      });
      var ul = document.createElement("ul");
      sec.notes.forEach(function (slug) {
        var n = DATA.notes[slug];
        ul.appendChild(el('<li><a href="' + noteHref(slug) + '" class="' + (slug === activeSlug ? "active" : "") + '">' +
          '<span class="dot' + (done[slug] ? " done" : "") + '">' + (done[slug] ? "&#10003;" : "") + "</span>" +
          "<span>" + esc(n.title.replace(/^Build: /, "").replace(/^Design an? /, "")) + "</span></a></li>"));
      });
      wrap.appendChild(btn);
      wrap.appendChild(ul);
      nav.appendChild(wrap);
    });
    var total = ORDER.length, d = doneCount(ORDER);
    document.getElementById("progressCard").innerHTML =
      '<div class="row"><span>Your progress</span><span><b>' + d + "</b> / " + total + " notes</span></div>" +
      '<div class="bar"><span style="width:' + pct(d, total) + '%"></span></div>';
  }

  // ------------------------------------------------------------ overview
  function renderOverview() {
    var cards = DATA.notes, total = ORDER.length;
    var qa = ORDER.reduce(function (a, s) { return a + cards[s].qa.length; }, 0);
    var last = store.get("last", null);
    var html = '<section class="hero"><div class="eyebrow">System design, end to end</div>' +
      "<h1>Notes, diagrams, case studies and labs for product company interviews.</h1>" +
      "<p>Concepts in depth, hand-drawn architecture diagrams, " + DATA.sections[9].notes.length +
      " full interview walkthroughs, from-scratch builds you can run, and interactive labs that let you feel the trade-offs.</p>" +
      '<div class="cta-row"><a class="btn primary" href="' + noteHref("00-start-here/01-interview-framework") + '">Start with the interview framework</a>' +
      '<a class="btn" href="#/roadmap">10 week roadmap</a><a class="btn" href="#/labs">Open the labs</a></div></section>' +
      '<div class="stats">' +
      '<div class="stat"><b>' + total + "</b><span>notes</span></div>" +
      '<div class="stat"><b>' + DATA.diagrams.length + "</b><span>hand-drawn diagrams</span></div>" +
      '<div class="stat"><b>' + qa + "</b><span>interview flashcards</span></div>" +
      '<div class="stat"><b>' + DATA.labs.length + "</b><span>interactive labs</span></div></div>";
    if (last && cards[last]) {
      html += '<a class="card continue" style="max-width:560px" href="' + noteHref(last) + '"><span class="eyebrow">Continue where you left off</span><h3>' +
        esc(cards[last].title) + "</h3><p>" + esc(cards[last].summary) + "</p></a>";
    }
    html += '<h2 class="section-title">The course</h2><div class="grid-cards">';
    DATA.sections.forEach(function (sec) {
      var d = doneCount(sec.notes);
      html += '<a class="card" href="#/section/' + sec.id + '"><h3>' + esc(sec.title) + "</h3><p>" + esc(sec.blurb) + "</p>" +
        '<div class="bar"><span style="width:' + pct(d, sec.notes.length) + '%"></span></div>' +
        '<div class="meta"><span>' + sec.notes.length + " notes</span><span>" + pct(d, sec.notes.length) + "% done</span></div></a>";
    });
    html += '</div><h2 class="section-title">Interactive labs</h2><div class="grid-cards">';
    DATA.labs.forEach(function (lab) {
      html += '<a class="card" href="#/lab/' + lab.id + '"><h3>' + esc(lab.title) + "</h3><p>" + esc((window.Labs[lab.id] || {}).blurb || "") + "</p></a>";
    });
    html += "</div>";
    main.innerHTML = html;
  }

  function renderSection(id) {
    var sec = SECTION[id];
    if (!sec) return notFound();
    var html = '<div class="crumbs"><a href="#/">Overview</a> / ' + esc(sec.title) + "</div>" +
      '<section class="hero"><h1>' + esc(sec.title) + "</h1><p>" + esc(sec.blurb) + "</p></section><div class=\"grid-cards\">";
    sec.notes.forEach(function (slug, i) {
      var n = DATA.notes[slug];
      html += '<a class="card" href="' + noteHref(slug) + '"><span class="eyebrow">' + (i + 1) + (done[slug] ? " &middot; done" : "") + "</span><h3>" +
        esc(n.title) + "</h3><p>" + esc(n.summary) + '</p><div class="meta"><span>' + esc(n.time) + "</span><span>" + n.qa.length + " questions</span></div></a>";
    });
    main.innerHTML = html + "</div>";
  }

  // ------------------------------------------------------------ note page
  function rewrite(container, slug) {
    var dir = "notes/" + slug.split("/")[0] + "/";
    container.querySelectorAll("a[href]").forEach(function (a) {
      var href = a.getAttribute("href");
      if (/^[a-z]+:/i.test(href)) { a.target = "_blank"; a.rel = "noopener"; return; }
      if (href.charAt(0) === "#") { a.setAttribute("href", noteHref(slug, href.slice(1))); return; }
      var parts = href.split("#"), path = normalize(dir + parts[0]);
      var m = path.match(/^notes\/(.+)\.md$/);
      if (m && DATA.notes[m[1]]) a.setAttribute("href", noteHref(m[1], parts[1]));
      else { a.setAttribute("href", "../" + path); a.target = "_blank"; }
    });
    container.querySelectorAll("img").forEach(function (img) {
      var path = normalize(dir + img.getAttribute("src"));
      img.setAttribute("src", "../" + path);
      img.loading = "lazy";
      var name = (path.match(/diagrams\/([\w-]+)\.svg$/) || [])[1];
      if (!name) return;
      var fig = el('<figure class="diagram"></figure>');
      img.parentNode.replaceChild(fig, img);
      if (fig.parentNode.tagName === "P" && fig.parentNode.childNodes.length === 1) fig.parentNode.replaceWith(fig);
      fig.appendChild(img);
      fig.appendChild(el("<figcaption><span>" + esc(img.alt) + '</span><a href="../assets/diagrams/excalidraw/' + name +
        '.excalidraw" download>Edit in Excalidraw</a><a href="../assets/diagrams/' + name + '.svg" target="_blank">Open SVG</a></figcaption>'));
      img.addEventListener("click", function () { lightbox(img.src); });
    });
    container.querySelectorAll("h2, h3").forEach(function (h) {
      h.id = slugify(h.textContent);
      h.appendChild(el('<a class="anchor" href="' + noteHref(slug, h.id) + '">#</a>'));
    });
  }

  function lightbox(src) {
    var lb = el('<div class="lightbox" role="dialog" aria-label="Diagram"><img alt="" src="' + src + '"></div>');
    lb.addEventListener("click", function () { lb.remove(); });
    document.body.appendChild(lb);
  }

  function renderNote(slug, anchor) {
    var n = DATA.notes[slug];
    if (!n) return notFound();
    store.set("last", slug);
    var sec = SECTION[n.section], idx = ORDER.indexOf(slug);
    var prev = ORDER[idx - 1], next = ORDER[idx + 1];
    var wrap = el('<div class="note-wrap"><article></article><aside class="toc"></aside></div>');
    var art = wrap.firstChild;
    art.innerHTML = '<div class="crumbs"><a href="#/">Overview</a> / <a href="#/section/' + sec.id + '">' + esc(sec.title) + "</a></div>" +
      '<header class="note-head"><h1>' + esc(n.title) + '</h1><p class="summary">' + esc(n.summary) + "</p>" +
      '<div class="chips">' + (n.time ? '<span class="chip">&#9201; ' + esc(n.time) + "</span>" : "") +
      (n.level ? '<span class="chip">' + esc(n.level) + "</span>" : "") +
      n.tags.slice(0, 6).map(function (t) { return '<span class="chip">#' + esc(t) + "</span>"; }).join("") + "</div>" +
      '<div class="note-actions"><button class="btn small' + (done[slug] ? " done" : "") + '" id="doneBtn">' + (done[slug] ? "&#10003; Completed" : "Mark as done") + "</button>" +
      (n.lab ? '<a class="btn small" href="#/lab/' + n.lab + '">&#9881; Open the lab</a>' : "") +
      (n.qa.length ? '<a class="btn small" href="#/flashcards/' + slug + '">&#9851; Practice ' + n.qa.length + " flashcards</a>" : "") +
      '<a class="btn small" href="https://github.com/Subhampreet/blueprint-101/blob/main/notes/' + slug + '.md" target="_blank" rel="noopener">View on GitHub</a></div></header>' +
      '<div class="prose"></div><nav class="pager">' +
      (prev ? '<a href="' + noteHref(prev) + '"><small>Previous</small>' + esc(DATA.notes[prev].title) + "</a>" : "<span></span>") +
      (next ? '<a class="next" href="' + noteHref(next) + '"><small>Next</small>' + esc(DATA.notes[next].title) + "</a>" : "") + "</nav>";
    var prose = art.querySelector(".prose");
    prose.innerHTML = window.Markdown.toHtml(n.md);
    rewrite(prose, slug);
    var toc = wrap.lastChild, heads = prose.querySelectorAll("h2");
    if (heads.length > 2) {
      toc.innerHTML = "<h4>On this page</h4>" + Array.prototype.map.call(heads, function (h) {
        return '<a href="' + noteHref(slug, h.id) + '" data-id="' + h.id + '">' + esc(h.textContent.replace(/#$/, "")) + "</a>";
      }).join("");
    }
    main.innerHTML = "";
    main.appendChild(wrap);
    art.querySelector("#doneBtn").addEventListener("click", function () {
      done[slug] = !done[slug];
      if (!done[slug]) delete done[slug];
      store.set("done", done);
      renderNote(slug);
      renderNav(slug);
    });
    if (anchor) {
      var target = document.getElementById(anchor);
      if (target) target.scrollIntoView();
    } else window.scrollTo(0, 0);
    spyToc(toc, heads);
  }

  function spyToc(toc, heads) {
    if (!("IntersectionObserver" in window) || !heads.length) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        toc.querySelectorAll("a").forEach(function (a) { a.classList.toggle("on", a.dataset.id === e.target.id); });
      });
    }, { rootMargin: "0px 0px -75% 0px" });
    heads.forEach(function (h) { io.observe(h); });
  }

  // ------------------------------------------------------------ search
  var modal = document.getElementById("searchModal"), input = document.getElementById("searchInput"),
    results = document.getElementById("searchResults"), sel = 0;
  var INDEX = ORDER.map(function (slug) {
    var n = DATA.notes[slug];
    return { slug: slug, title: n.title.toLowerCase(), tags: n.tags.join(" ").toLowerCase(), heads: n.headings.join(" | ").toLowerCase(),
      summary: n.summary.toLowerCase(), text: n.text.toLowerCase(), headings: n.headings };
  });

  function search(q) {
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return [];
    return INDEX.map(function (d) {
      var score = 0;
      for (var i = 0; i < terms.length; i++) {
        var t = terms[i], s = 0;
        if (d.title.indexOf(t) >= 0) s += 10;
        if (d.tags.indexOf(t) >= 0) s += 6;
        if (d.heads.indexOf(t) >= 0) s += 4;
        if (d.summary.indexOf(t) >= 0) s += 3;
        if (d.text.indexOf(t) >= 0) s += 1 + Math.min(3, d.text.split(t).length - 2) * 0.3;
        if (!s) return null;
        score += s;
      }
      var head = d.headings.filter(function (h) { return terms.some(function (t) { return h.toLowerCase().indexOf(t) >= 0; }); })[0];
      return { d: d, score: score, head: head };
    }).filter(Boolean).sort(function (a, b) { return b.score - a.score; }).slice(0, 12);
  }

  function highlight(text, q) {
    var out = esc(text);
    q.toLowerCase().split(/\s+/).filter(Boolean).forEach(function (t) {
      out = out.replace(new RegExp("(" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig"), "<mark>$1</mark>");
    });
    return out;
  }

  function drawResults() {
    var q = input.value, r = search(q);
    sel = 0;
    if (!q.trim()) { results.innerHTML = '<div class="empty">Type to search titles, tags, headings and full text.</div>'; return; }
    if (!r.length) { results.innerHTML = '<div class="empty">No notes match "' + esc(q) + '".</div>'; return; }
    results.innerHTML = r.map(function (x, i) {
      var n = DATA.notes[x.d.slug];
      return '<a class="' + (i === 0 ? "sel" : "") + '" href="' + noteHref(x.d.slug, x.head ? slugify(x.head) : "") + '">' + highlight(n.title, q) +
        "<small>" + esc(SECTION[n.section].title) + (x.head ? " &rsaquo; " + highlight(x.head, q) : "") + "</small></a>";
    }).join("");
  }

  function openSearch() { modal.hidden = false; input.value = ""; drawResults(); input.focus(); }
  function closeSearch() { modal.hidden = true; }
  document.getElementById("searchBtn").addEventListener("click", openSearch);
  modal.addEventListener("click", function (e) { if (e.target === modal) closeSearch(); });
  results.addEventListener("click", closeSearch);
  input.addEventListener("input", drawResults);
  input.addEventListener("keydown", function (e) {
    var items = results.querySelectorAll("a");
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      if (!items.length) return;
      items[sel].classList.remove("sel");
      sel = (sel + (e.key === "ArrowDown" ? 1 : items.length - 1)) % items.length;
      items[sel].classList.add("sel");
      items[sel].scrollIntoView({ block: "nearest" });
    } else if (e.key === "Enter" && items[sel]) {
      location.hash = items[sel].getAttribute("href");
      closeSearch();
    }
  });
  document.addEventListener("keydown", function (e) {
    var typing = /input|textarea|select/i.test((e.target || {}).tagName || "");
    if ((e.key === "/" && !typing) || (e.key.toLowerCase() === "k" && (e.metaKey || e.ctrlKey))) { e.preventDefault(); openSearch(); }
    if (e.key === "Escape") { closeSearch(); var lb = document.querySelector(".lightbox"); if (lb) lb.remove(); }
  });

  // ------------------------------------------------------------ flashcards (Leitner boxes)
  function renderFlashcards(filter) {
    var boxes = store.get("boxes", {});
    var all = [];
    ORDER.forEach(function (slug) {
      DATA.notes[slug].qa.forEach(function (c, i) { all.push({ id: slug + "#" + i, slug: slug, q: c.q, a: c.a }); });
    });
    var scope = filter || store.get("fc-scope", "all");
    var cards = all.filter(function (c) {
      return scope === "all" || c.slug === scope || c.slug.indexOf(scope + "/") === 0;
    });
    // lowest box first, then stable shuffle so sessions vary
    var seed = Date.now() % 997;
    cards.sort(function (a, b) {
      var d = (boxes[a.id] || 1) - (boxes[b.id] || 1);
      return d || ((a.id.length * seed) % 7) - ((b.id.length * seed) % 7);
    });
    var i = 0, flipped = false;
    var opts = '<option value="all">All sections (' + all.length + ")</option>" + DATA.sections.map(function (s) {
      var n = all.filter(function (c) { return c.slug.indexOf(s.id + "/") === 0; }).length;
      return n ? '<option value="' + s.id + '"' + (scope === s.id ? " selected" : "") + ">" + esc(s.title) + " (" + n + ")</option>" : "";
    }).join("") + (DATA.notes[scope] ? '<option value="' + scope + '" selected>' + esc(DATA.notes[scope].title) + "</option>" : "");
    main.innerHTML = '<div class="crumbs"><a href="#/">Overview</a> / Flashcards</div><section class="hero"><h1>Flashcards</h1>' +
      "<p>Every interview question in the notes, as a spaced repetition deck. Click the card or press Space to reveal, then rate yourself. Cards you miss come back first.</p></section>" +
      '<div class="fc-toolbar"><select id="fcScope" aria-label="Deck">' + opts + '</select><span class="lab-note" id="fcCount"></span></div>' +
      '<div class="flashcard" id="card" tabindex="0" role="button" aria-label="Flashcard, press space to flip"></div>' +
      '<div class="fc-actions"><button class="btn" id="again">&#8634; Again <kbd>1</kbd></button><button class="btn primary" id="good">Got it <kbd>2</kbd></button>' +
      '<button class="btn" id="skip">Skip <kbd>&rarr;</kbd></button></div><div class="boxes" id="boxes"></div>';
    var cardEl = document.getElementById("card");
    function draw() {
      if (!cards.length) { cardEl.innerHTML = '<div class="q">No cards in this deck.</div>'; return; }
      var c = cards[i % cards.length], n = DATA.notes[c.slug];
      cardEl.innerHTML = '<div class="label">Question ' + ((i % cards.length) + 1) + " of " + cards.length + " &middot; box " + (boxes[c.id] || 1) + "</div>" +
        '<div class="q">' + esc(c.q) + '</div><div class="src">from <a href="' + noteHref(c.slug) + '">' + esc(n.title) + "</a></div>" +
        (flipped ? '<div class="a prose">' + window.Markdown.toHtml(c.a) + "</div>" : '<p class="lab-note" style="margin-top:28px">Think through your answer out loud, then reveal.</p>');
      var counts = [0, 0, 0, 0, 0];
      cards.forEach(function (x) { counts[(boxes[x.id] || 1) - 1]++; });
      document.getElementById("boxes").innerHTML = counts.map(function (n, b) { return "<span>Box " + (b + 1) + ": " + n + "</span>"; }).join("") +
        '<span title="Box 1 = new or missed, box 5 = solid">mastered: ' + counts[4] + "</span>";
      document.getElementById("fcCount").textContent = cards.length + " cards";
    }
    function rate(good) {
      if (!cards.length) return;
      var c = cards[i % cards.length];
      boxes[c.id] = good ? Math.min(5, (boxes[c.id] || 1) + 1) : 1;
      store.set("boxes", boxes);
      i++; flipped = false; draw();
    }
    cardEl.addEventListener("click", function (e) { if (e.target.tagName !== "A") { flipped = !flipped; draw(); } });
    document.getElementById("again").onclick = function () { rate(false); };
    document.getElementById("good").onclick = function () { rate(true); };
    document.getElementById("skip").onclick = function () { i++; flipped = false; draw(); };
    document.getElementById("fcScope").onchange = function (e) { store.set("fc-scope", e.target.value); location.hash = "#/flashcards"; renderFlashcards(e.target.value); };
    document.onkeydown = function (e) {
      if (!location.hash.match(/^#\/flashcards/) || !modal.hidden) return;
      if (e.key === " ") { e.preventDefault(); flipped = !flipped; draw(); }
      if (e.key === "1") rate(false);
      if (e.key === "2") rate(true);
      if (e.key === "ArrowRight") { i++; flipped = false; draw(); }
    };
    draw();
  }

  // ------------------------------------------------------------ diagrams gallery
  function renderDiagrams() {
    main.innerHTML = '<div class="crumbs"><a href="#/">Overview</a> / Diagrams</div><section class="hero"><h1>Diagram gallery</h1>' +
      "<p>All " + DATA.diagrams.length + " hand-drawn diagrams. Each one has an editable <code>.excalidraw</code> source: download it and open it at excalidraw.com to remix.</p></section>" +
      '<div class="gallery">' + DATA.diagrams.map(function (d) {
        var used = d.notes.map(function (s) { return '<a href="' + noteHref(s) + '">' + esc(DATA.notes[s].title) + "</a>"; }).join(", ");
        return '<figure><img loading="lazy" alt="' + esc(d.name) + '" src="../assets/diagrams/' + d.name + '.svg"><figcaption><b>' + esc(d.name) + "</b>" +
          (used ? "<span>Used in " + used + "</span>" : "") + '<a href="../assets/diagrams/excalidraw/' + d.name + '.excalidraw" download>Download .excalidraw</a></figcaption></figure>';
      }).join("") + "</div>";
    main.querySelectorAll(".gallery img").forEach(function (img) { img.addEventListener("click", function () { lightbox(img.src); }); });
  }

  // ------------------------------------------------------------ labs
  function renderLabs() {
    main.innerHTML = '<div class="crumbs"><a href="#/">Overview</a> / Labs</div><section class="hero"><h1>Interactive labs</h1>' +
      "<p>Move the sliders and watch the trade-offs. Every lab is tied to the notes that explain it.</p></section><div class=\"grid-cards\">" +
      DATA.labs.map(function (lab) {
        return '<a class="card" href="#/lab/' + lab.id + '"><h3>' + esc(lab.title) + "</h3><p>" + esc((window.Labs[lab.id] || {}).blurb || "") + "</p></a>";
      }).join("") + "</div>";
  }

  function renderLab(id) {
    var lab = DATA.labs.filter(function (l) { return l.id === id; })[0], impl = window.Labs[id];
    if (!lab || !impl) return notFound();
    var related = lab.notes.map(function (s) { return '<a href="' + noteHref(s) + '">' + esc(DATA.notes[s].title) + "</a>"; }).join(" &middot; ");
    main.innerHTML = '<div class="lab"><div class="crumbs"><a href="#/">Overview</a> / <a href="#/labs">Labs</a></div>' +
      '<section class="hero" style="margin-bottom:22px"><h1>' + esc(lab.title) + "</h1><p>" + esc(impl.blurb) + "</p>" +
      (related ? '<p class="lab-note" style="margin-top:8px">Read: ' + related + "</p>" : "") + '</section><div id="labRoot"></div></div>';
    impl.render(document.getElementById("labRoot"));
  }

  function notFound() {
    main.innerHTML = '<section class="hero"><h1>Not found</h1><p>That page does not exist. <a href="#/">Back to the overview</a>.</p></section>';
  }

  // ------------------------------------------------------------ router
  function route() {
    if (window.Labs && window.Labs._stop) window.Labs._stop();
    document.onkeydown = null;
    var h = decodeURIComponent(location.hash.replace(/^#\/?/, "")), active = null, m;
    document.querySelectorAll(".top-links a").forEach(function (a) {
      var t = a.getAttribute("href").replace(/^#\/?/, "");
      a.classList.toggle("active", t ? h.indexOf(t) === 0 : !h);
    });
    if (!h) renderOverview();
    else if ((m = h.match(/^note\/([^~]+)(?:~(.*))?$/))) { active = m[1]; renderNote(m[1], m[2]); }
    else if (h === "roadmap") { active = "00-start-here/03-study-roadmap"; renderNote(active); }
    else if ((m = h.match(/^section\/(.+)$/))) renderSection(m[1]);
    else if ((m = h.match(/^flashcards(?:\/(.+))?$/))) renderFlashcards(m[1]);
    else if (h === "diagrams") renderDiagrams();
    else if (h === "labs") renderLabs();
    else if ((m = h.match(/^lab\/(.+)$/))) renderLab(m[1]);
    else notFound();
    renderNav(active);
    document.getElementById("sidebar").classList.remove("open");
    if (!(m && m[2])) main.focus({ preventScroll: true });
  }

  document.getElementById("menuBtn").addEventListener("click", function () { document.getElementById("sidebar").classList.toggle("open"); });
  document.getElementById("themeBtn").addEventListener("click", function () {
    var cur = document.documentElement.getAttribute("data-theme") ||
      (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    var next = cur === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try { localStorage.setItem("bp-theme", next); } catch (e) { /* ignore */ }
  });
  window.addEventListener("hashchange", route);
  route();
})();
