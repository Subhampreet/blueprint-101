/* Blueprint 101 reader: routing, pages, progress, search, flashcards, gallery.
   Product and design rules live in docs/prd.md and docs/design.md. */
(function () {
  "use strict";

  var DATA = window.BLUEPRINT;
  var main = document.getElementById("main");
  var GH = "https://github.com/Subhampreet/blueprint-101/blob/main/";
  if (!DATA) {
    main.innerHTML = '<div class="callout bad">content.js is missing. Run <code>python3 tools/build_site.py</code> first.</div>';
    return;
  }

  // ------------------------------------------------------------ icons (24px stroke icons)
  var ICONS = {
    rocket: "M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09zM12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2zM9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5",
    book: "M4 19.5A2.5 2.5 0 0 1 6.5 17H20M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z",
    blocks: "M4 4h6v6H4zM14 4h6v6h-6zM14 14h6v6h-6zM4 14h6v6H4z",
    database: "M12 3c4.42 0 8 1.34 8 3s-3.58 3-8 3-8-1.34-8-3 3.58-3 8-3zM20 12c0 1.66-3.58 3-8 3s-8-1.34-8-3M4 6v12c0 1.66 3.58 3 8 3s8-1.34 8-3V6",
    globe: "M12 2a10 10 0 1 0 0 20a10 10 0 1 0 0-20zM2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z",
    layers: "M12 2 2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5",
    activity: "M22 12h-4l-3 9L9 3l-3 9H2",
    shield: "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z",
    code: "M16 18l6-6-6-6M8 6l-6 6 6 6",
    briefcase: "M3 7h18v13H3zM16 20V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v15",
    cpu: "M5 5h14v14H5zM9 9h6v6H9zM9 2v3M15 2v3M9 19v3M15 19v3M19 9h3M19 15h3M2 9h3M2 15h3",
    wrench: "M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z",
    library: "M16 6l4 14M12 6v14M8 8v12M4 4v16",
    calendar: "M3 5h18v16H3zM16 3v4M8 3v4M3 10h18",
    flask: "M9 3h6M10 3v6L4.5 19.5A1 1 0 0 0 5.4 21h13.2a1 1 0 0 0 .9-1.5L14 9V3M7 15h10",
    cards: "M3 8h13v13H3zM8 3h13v13",
    image: "M3 3h18v18H3zM8.5 10a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zM21 15l-5-5L5 21",
    search: "M11 4a7 7 0 1 0 0 14a7 7 0 1 0 0-14zM20 20l-4-4",
    sun: "M12 8a4 4 0 1 0 0 8a4 4 0 1 0 0-8zM12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41",
    moon: "M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9z",
    chevron: "M9 18l6-6-6-6",
    check: "M20 6 9 17l-5-5",
    menu: "M4 6h16M4 12h16M4 18h16",
    clock: "M12 2a10 10 0 1 0 0 20a10 10 0 1 0 0-20zM12 6v6l4 2",
    target: "M12 2a10 10 0 1 0 0 20a10 10 0 1 0 0-20zM12 6a6 6 0 1 0 0 12a6 6 0 1 0 0-12zM12 10a2 2 0 1 0 0 4a2 2 0 1 0 0-4z",
    home: "M3 10.5 12 3l9 7.5V21H3zM9 21v-7h6v7",
    external: "M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6",
    download: "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3",
    pen: "M12 20h9M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4z",
    user: "M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 3a4 4 0 1 0 0 8a4 4 0 1 0 0-8z",
    bookmark: "M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z",
    lock: "M5 11h14v10H5zM8 11V7a4 4 0 0 1 8 0v4",
    flame: "M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.07-2.14-.22-4.05 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.15.43-2.29 1-3a2.5 2.5 0 0 0 2.5 2.5z",
    upload: "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12",
    trash: "M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6"
  };
  var GITHUB = '<svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>';
  function icon(name) {
    return '<span class="ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="' + ICONS[name] + '"/></svg></span>';
  }
  var SECTION_ICON = {
    "00-start-here": "rocket", "01-fundamentals": "book", "02-building-blocks": "blocks", "03-data": "database",
    "04-networking-apis": "globe", "05-architecture": "layers", "06-reliability-ops": "activity", "07-security": "shield",
    "08-lld": "code", "09-case-studies": "briefcase", "10-advanced": "cpu", "11-builds": "wrench", "12-practice": "target", "13-resources": "library"
  };

  // ------------------------------------------------------------ storage (never throws)
  // Everything a learner owns lives in localStorage under "bp-*" keys: it survives refreshes and browser restarts,
  // stays on this device, and never leaves it. Export/import moves it between browsers.
  var store = {
    ok: (function () { try { localStorage.setItem("bp-probe", "1"); localStorage.removeItem("bp-probe"); return true; } catch (e) { return false; } })(),
    get: function (k, d) { try { var v = localStorage.getItem("bp-" + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem("bp-" + k, JSON.stringify(v)); } catch (e) { /* private mode or quota */ } },
    del: function (k) { try { localStorage.removeItem("bp-" + k); } catch (e) { /* ignore */ } }
  };
  // learner data: what export, import and reset act on (theme, open sidebar sections and deck choice are preferences)
  var USER_KEYS = ["profile", "done", "boxes", "saved", "activity", "memo", "last"];
  var profile, done, saved, activity, memo, openSections;
  function loadState() {
    profile = store.get("profile", null);         // { name, since }
    done = store.get("done", {});                 // slug -> completion time (ms); older data stores true
    saved = store.get("saved", {});               // slug -> time saved for later
    activity = store.get("activity", {});         // "YYYY-MM-DD" -> actions that day (completions, flashcard reviews)
    memo = store.get("memo", {});                 // slug -> personal notes
    openSections = store.get("open", { "00-start-here": true });
  }
  loadState();

  function dayKey(d) { return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2); }
  function bump() { var k = dayKey(new Date()); activity[k] = (activity[k] || 0) + 1; store.set("activity", activity); }
  function streak() {
    var d = new Date(), n = 0;
    if (!activity[dayKey(d)]) d.setDate(d.getDate() - 1);            // today not started yet: the streak is still alive
    while (activity[dayKey(d)]) { n++; d.setDate(d.getDate() - 1); }
    return n;
  }
  function bestStreak() {
    var days = Object.keys(activity).sort(), best = 0, run = 0, prev = null;
    days.forEach(function (k) {
      var t = new Date(k + "T00:00:00");
      run = prev && Math.round((t - prev) / 864e5) === 1 ? run + 1 : 1;
      best = Math.max(best, run); prev = t;
    });
    return best;
  }
  function firstName() { return profile && profile.name ? profile.name.split(/\s+/)[0] : ""; }
  function initials() { return profile && profile.name ? profile.name.trim().split(/\s+/).slice(0, 2).map(function (w) { return w.charAt(0); }).join("").toUpperCase() : ""; }
  function saveProfile(name) {
    profile = { name: String(name || "").trim().slice(0, 40), since: (profile && profile.since) || new Date().toISOString() };
    store.set("profile", profile);
    // ask the browser not to evict our data under storage pressure (granted silently or ignored)
    try { if (navigator.storage && navigator.storage.persist) navigator.storage.persist(); } catch (e) { /* ignore */ }
    paintAvatar();
  }

  // ------------------------------------------------------------ helpers
  var ORDER = [];
  DATA.sections.forEach(function (s) { s.notes.forEach(function (n) { ORDER.push(n); }); });
  var SECTION = {}, PLAN = {}, COMPANY = {};
  DATA.sections.forEach(function (s) { SECTION[s.id] = s; });
  (DATA.plans || []).forEach(function (p) { PLAN[p.id] = p; });
  (DATA.companies || []).forEach(function (c) { COMPANY[c.id] = c; });

  function el(html) { var t = document.createElement("template"); t.innerHTML = html.trim(); return t.content.firstChild; }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function slugify(s) { return s.toLowerCase().trim().replace(/<[^>]+>/g, "").replace(/[^\w\s-]/g, "").replace(/\s+/g, "-"); }
  function noteHref(slug, anchor) { return "#/note/" + slug + (anchor ? "~" + anchor : ""); }
  function pct(a, b) { return b ? Math.round((a / b) * 100) : 0; }
  function doneCount(slugs) { return slugs.filter(function (s) { return done[s]; }).length; }
  function shortTitle(t) { return t.replace(/^Build: /, "").replace(/^Design an? /, "").replace(/^"|"$/g, ""); }
  function normalize(path) {
    var parts = [];
    path.split("/").forEach(function (seg) {
      if (seg === "..") parts.pop();
      else if (seg !== "." && seg !== "") parts.push(seg);
    });
    return parts.join("/");
  }
  function progressBar(d, t) { return '<div class="bar" role="progressbar" aria-valuenow="' + pct(d, t) + '" aria-valuemin="0" aria-valuemax="100"><span style="width:' + pct(d, t) + '%"></span></div>'; }
  function statusDot(slug) { return '<span class="status' + (done[slug] ? " done" : "") + '">' + (done[slug] ? icon("check") : "") + "</span>"; }
  function page(html) { main.innerHTML = '<div class="page">' + html + "</div>"; window.scrollTo(0, 0); }

  // ------------------------------------------------------------ sidebar
  function renderSidebar(route) {
    var side = document.getElementById("sidebar");
    var activeNote = route.note, total = ORDER.length, d = doneCount(ORDER);
    if (activeNote && DATA.notes[activeNote]) openSections[DATA.notes[activeNote].section] = true;
    var cs = SECTION["09-case-studies"];
    var links = [
      ["#/", "home", "Get started", "", route.key === "home"],
      ["#/plans", "calendar", "Study plans", (DATA.plans || []).length, route.key === "plans"],
      ["#/section/09-case-studies", "briefcase", "Case studies", cs ? cs.notes.length : "", route.key === "section/09-case-studies"],
      ["#/labs", "flask", "Interactive labs", DATA.labs.length, route.key === "labs"],
      ["#/flashcards", "cards", "Flashcards", "", route.key === "flashcards"],
      ["#/diagrams", "image", "Diagram gallery", DATA.diagrams.length, route.key === "diagrams"]
    ];
    var html = '<a class="side-progress' + (route.key === "profile" ? " active" : "") + '" href="#/profile"><div class="row"><span>' + (firstName() ? esc(firstName()) + "'s progress" : "Your progress") +
      "</span><span><b>" + d + "</b> / " + total + "</span></div>" + progressBar(d, total) + "</a>" +
      '<div class="side-group">' + links.map(function (l) {
        return '<a class="side-link' + (l[4] ? " active" : "") + '" href="' + l[0] + '">' + icon(l[1]) + "<span>" + l[2] + '</span><span class="count">' + l[3] + "</span></a>";
      }).join("") + '</div><div class="side-group"><p class="side-label">Notes</p>';
    DATA.sections.forEach(function (sec) {
      var c = doneCount(sec.notes);
      html += '<div class="side-section' + (openSections[sec.id] ? " open" : "") + '" data-id="' + sec.id + '"><button type="button" aria-expanded="' + !!openSections[sec.id] + '">' +
        icon(SECTION_ICON[sec.id] || "book") + "<span>" + esc(sec.title) + '</span><span class="count" style="margin-left:auto;font-size:12px;color:var(--text-3);font-weight:400">' + c + "/" + sec.notes.length +
        '</span><svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="' + ICONS.chevron + '"/></svg></button><ul>' +
        sec.notes.map(function (slug) {
          return '<li><a href="' + noteHref(slug) + '" class="' + (slug === activeNote ? "active" : "") + '">' + statusDot(slug) + "<span>" + esc(shortTitle(DATA.notes[slug].title)) + "</span></a></li>";
        }).join("") + "</ul></div>";
    });
    side.innerHTML = html + "</div>";
    side.querySelectorAll(".side-section > button").forEach(function (b) {
      b.addEventListener("click", function () {
        var box = b.parentNode, id = box.dataset.id;
        openSections[id] = !openSections[id];
        store.set("open", openSections);
        box.classList.toggle("open");
        b.setAttribute("aria-expanded", !!openSections[id]);
      });
    });
    var act = side.querySelector("li a.active");
    if (act && act.scrollIntoView) act.scrollIntoView({ block: "nearest" });
  }

  // ------------------------------------------------------------ get started (home)
  function collectionProgress() {
    var items = [];
    (DATA.plans || []).forEach(function (p) { items.push({ kind: "plan", id: p.id, title: p.title + " study plan", notes: p.notes, href: "#/plan/" + p.id }); });
    DATA.sections.forEach(function (s) { items.push({ kind: "section", id: s.id, title: s.title, notes: s.notes, href: "#/section/" + s.id }); });
    return items;
  }

  function nextNote(notes) { return notes.filter(function (s) { return !done[s]; })[0] || notes[0]; }

  var LOCAL_NOTE = icon("lock") + " Saved only in this browser on this device. No account and no server: nothing leaves your machine.";

  // home strip: a name form for new visitors, a personal summary for returning ones
  function welcomeStrip() {
    if (!profile || !profile.name) {
      return '<section class="card welcome"><div class="welcome-main"><span class="icon-tile brand">' + icon("user") + "</span><div><h3>Track your progress</h3>" +
        "<p>Add your name to start. Completed notes, flashcard boxes, bookmarks, personal notes and your daily streak are remembered across refreshes and restarts.</p></div></div>" +
        '<form class="name-form" id="welcomeForm"><input type="text" id="welcomeName" maxlength="40" placeholder="Your name" autocomplete="given-name" aria-label="Your name" required>' +
        '<button class="btn primary" type="submit">Start tracking</button></form><p class="local-note">' + LOCAL_NOTE + ' <a href="#/profile">Learn more</a></p></section>';
    }
    var last = store.get("last", null), d = doneCount(ORDER), s = streak(), nSaved = Object.keys(saved).filter(function (k) { return DATA.notes[k]; }).length;
    return '<section class="card welcome back"><div class="welcome-main"><span class="avatar lg">' + esc(initials()) + "</span><div><h3>Welcome back, " + esc(firstName()) + "</h3>" +
      '<div class="pills" style="margin-top:8px"><span class="pill brand">' + icon("flame") + " <b>" + s + "</b> day streak</span><span class=\"pill\"><b>" + d + "</b> / " + ORDER.length + " notes done</span>" +
      '<span class="pill">' + icon("bookmark") + " <b>" + nSaved + "</b> saved</span></div></div></div>" +
      '<div class="cta">' + (last && DATA.notes[last] ? '<a class="btn primary" href="' + noteHref(last) + '">Continue: ' + esc(shortTitle(DATA.notes[last].title)) + " " + icon("chevron") + "</a>" : "") +
      '<a class="btn" href="#/profile">' + icon("user") + " Your progress</a></div></section>";
  }
  function wireWelcome() {
    var f = document.getElementById("welcomeForm");
    if (!f) return;
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var v = document.getElementById("welcomeName").value.trim();
      if (!v) return;
      saveProfile(v);
      route();
    });
  }

  // one-time prompt the first time a learner marks something complete without a profile
  function askName(then) {
    var box = el('<div class="modal" role="dialog" aria-modal="true" aria-labelledby="askTitle"><form class="modal-box" id="askForm">' +
      '<span class="icon-tile brand">' + icon("user") + '</span><h2 id="askTitle">Start tracking your progress</h2>' +
      "<p>What should we call you? Your progress, flashcards, bookmarks and notes will be remembered next time you visit.</p>" +
      '<input type="text" id="askName" maxlength="40" placeholder="Your name" autocomplete="given-name" aria-label="Your name">' +
      '<p class="local-note">' + LOCAL_NOTE + " Clearing site data or using a private window removes it, so export a backup from Your progress.</p>" +
      '<div class="modal-actions"><button class="btn" type="button" id="askSkip">Not now</button><button class="btn primary" type="submit">Start tracking</button></div></form></div>');
    function close(name) {
      saveProfile(name);                     // an empty name still records the choice, so we never ask twice
      box.remove();
      then();
    }
    box.querySelector("#askForm").addEventListener("submit", function (e) { e.preventDefault(); close(box.querySelector("#askName").value); });
    box.querySelector("#askSkip").addEventListener("click", function () { close(""); });
    box.addEventListener("keydown", function (e) { if (e.key === "Escape") { e.stopPropagation(); close(""); } });
    document.body.appendChild(box);
    box.querySelector("#askName").focus();
  }

  function renderHome() {
    var total = ORDER.length, qa = ORDER.reduce(function (a, s) { return a + DATA.notes[s].qa.length; }, 0);
    var html = '<section class="hero-card"><span class="pill brand">' + icon("rocket") + " System design interview prep</span>" +
      '<h1 style="margin-top:16px">Get <span class="grad">started</span></h1>' +
      "<p>The one-stop page to prepare for system design interviews at product companies: deep notes, hand-drawn diagrams, real case studies, runnable builds and interactive labs.</p>" +
      '<div class="cta"><a class="btn primary" href="' + noteHref("00-start-here/01-interview-framework") + '">Start the interview playbook ' + icon("chevron") + "</a>" +
      '<a class="btn" href="#/plans">' + icon("calendar") + " Pick a study plan</a></div>" +
      '<div class="hero-stats"><div><b>' + total + "</b><span>in-depth notes</span></div><div><b>" + DATA.diagrams.length + "</b><span>hand-drawn diagrams</span></div><div><b>" +
      qa + "</b><span>interview questions</span></div><div><b>" + DATA.labs.length + "</b><span>interactive labs</span></div></div></section>" + welcomeStrip();

    // resume cards: in-progress collections, otherwise the first two to begin with
    var prog = collectionProgress().map(function (c) { c.d = doneCount(c.notes); c.p = pct(c.d, c.notes.length); return c; });
    var inProg = prog.filter(function (c) { return c.d > 0 && c.d < c.notes.length; }).sort(function (a, b) { return b.p - a.p; }).slice(0, 2);
    if (inProg.length < 2) {
      prog.filter(function (c) { return (c.id === "1-week" || c.id === "00-start-here") && inProg.indexOf(c) < 0; }).forEach(function (c) { if (inProg.length < 2) inProg.push(c); });
    }
    html += '<div class="grid c2" style="margin-top:16px">' + inProg.map(function (c) {
      return '<div class="card resume"><div class="pct">' + c.p + "<small>%</small></div><div><h3>" + esc(c.title) + '</h3><div class="sub">' + c.d + " / " + c.notes.length + " notes</div>" + progressBar(c.d, c.notes.length) +
        '</div><a class="btn small" href="' + noteHref(nextNote(c.notes)) + '">' + (c.d ? "Resume" : "Start") + "</a></div>";
    }).join("") + "</div>";

    // recommended preparation
    var steps = [
      { n: 1, icon: "rocket", title: "System Design Interview Playbook", desc: "How the interview runs, what is graded, and how to estimate. Read this first.", href: noteHref("00-start-here/01-interview-framework"), notes: SECTION["00-start-here"].notes },
      { n: 2, icon: "target", title: "Blueprint 15", chip: ["brand", "Highest yield"], desc: "The 15 notes that cover the concepts and designs asked most often: caching, queues, sharding, replication, feeds and chat.", href: "#/plan/1-week", notes: PLAN["1-week"].notes },
      { n: 3, icon: "briefcase", title: "Case study walkthroughs", chip: ["", "Practice"], desc: SECTION["09-case-studies"].notes.length + " full interview answers, from URL shortener to search engine. Attempt each one yourself before reading it.", href: "#/section/09-case-studies", notes: SECTION["09-case-studies"].notes },
      { n: 4, icon: "cpu", title: "Advanced deep dives", chip: ["violet", "If you're a senior engineer"], desc: "Consensus, clocks, stream processing, probabilistic structures, geospatial and ML systems for the follow-up questions.", href: "#/section/10-advanced", notes: SECTION["10-advanced"].notes }
    ];
    html += '<section class="block"><div class="block-head"><div><h2>Recommended preparation</h2><p>Not sure where to start? This path works for most people.</p></div></div><div class="timeline">' +
      steps.map(function (s) {
        var complete = doneCount(s.notes) === s.notes.length;
        return '<a class="step' + (complete ? " done" : "") + '" href="' + s.href + '"><span class="num">' + (complete ? icon("check") : s.n) + '</span><span class="icon-tile">' + icon(s.icon) +
          "</span><span><h3>" + esc(s.title) + (s.chip ? ' <span class="chip ' + s.chip[0] + '">' + esc(s.chip[1]) + "</span>" : "") + "</h3><p>" + esc(s.desc) + '</p></span><span class="go">' + icon("chevron") + "</span></a>";
      }).join("") + '<div class="timeline-foot">With extra time, drill the Practice section (estimation, databases, networking, cost) and keep going with the focus areas, labs and builds below.</div></div></section>';

    // study plans
    html += '<section class="block"><div class="block-head"><div><h2>Study plans</h2><p>Prepare the best you can within any timeline.</p></div><a class="btn small" href="#/plans">All plans</a></div><div class="grid c3">' +
      (DATA.plans || []).map(planCard).join("") + "</div></section>";

    // companies
    html += '<section class="block"><div class="block-head"><div><h2>Company practice sets</h2><p>Designs and topics built around the products each company is known for.</p></div></div><div class="grid c4">' +
      (DATA.companies || []).map(function (c) {
        return '<a class="card company" href="#/company/' + c.id + '"><span class="logo" style="background:' + c.color + '">' + esc(c.name.charAt(0)) + "</span><span><h3>" + esc(c.name) + '</h3><span class="sub">' + c.notes.length + " topics &middot; " + doneCount(c.notes) + " done</span></span></a>";
      }).join("") + "</div></section>";

    // focus areas
    html += '<section class="block"><div class="block-head"><div><h2>Focus areas</h2><p>Deep dive into the topics that system design rounds probe.</p></div></div><div class="grid c3">' +
      DATA.sections.filter(function (s) { return s.id !== "13-resources"; }).map(function (s) {
        var d = doneCount(s.notes);
        return '<a class="card focus" href="#/section/' + s.id + '"><span class="icon-tile">' + icon(SECTION_ICON[s.id]) + '</span><span class="body"><h3>' + esc(s.title) + "</h3><p>" + esc(s.blurb) +
          '</p><span class="count">' + d + " / " + s.notes.length + " notes</span>" + progressBar(d, s.notes.length) + "</span></a>";
      }).join("") + "</div></section>";

    // practice formats
    var formats = [
      ["#/labs", "flask", "Interactive labs", DATA.labs.length + " simulations", "Move sliders and watch load balancers, caches, quorums and rate limiters react."],
      ["#/flashcards", "cards", "Flashcards", qa + " questions", "Every interview question in the notes as a spaced repetition deck."],
      ["#/section/11-builds", "wrench", "From-scratch builds", SECTION["11-builds"].notes.length + " builds", "Runnable Python for LRU, rate limiters, hash rings, Bloom filters, an LSM store and more."],
      ["#/diagrams", "image", "Diagram gallery", DATA.diagrams.length + " diagrams", "Every architecture sketch, each with an editable Excalidraw source."],
      ["#/section/12-practice", "target", "Practice drills", "40+ drills", "Estimation, database optimization, networking troubleshooting and cost exercises with worked answers."],
      ["#/note/12-practice/05-design-question-bank", "briefcase", "Question bank", "50 questions", "The most asked design questions by difficulty, each linked to the notes that answer it."]
    ];
    html += '<section class="block"><div class="block-head"><div><h2>Practice formats</h2><p>Different ways to make it stick.</p></div></div><div class="grid c3">' +
      formats.map(function (f) {
        return '<a class="card" href="' + f[0] + '"><span class="icon-tile brand">' + icon(f[1]) + "</span><h3>" + f[2] + "</h3><p>" + f[4] + '</p><div class="foot"><span>' + f[3] + "</span>" + icon("chevron") + "</div></a>";
      }).join("") + "</div></section>";
    page(html);
    wireWelcome();
  }

  function planCard(p) {
    var d = doneCount(p.notes);
    return '<a class="card" href="#/plan/' + p.id + '"><div style="display:flex;justify-content:space-between;align-items:center"><span class="icon-tile">' + icon("calendar") +
      '</span><span class="chip brand">' + pct(d, p.notes.length) + "% done</span></div><h3>" + esc(p.title) + "</h3><p>" + esc(p.blurb) + "</p>" +
      '<div class="plan-meta"><div><span>Notes</span><b>' + p.notes.length + '</b></div><div><span>Recommended schedule</span><b>' + esc(p.schedule) + "</b></div></div></a>";
  }

  // ------------------------------------------------------------ list pages
  function noteList(slugs, showSection) {
    return '<div class="list">' + slugs.map(function (slug) {
      var n = DATA.notes[slug];
      return '<a class="row-item" href="' + noteHref(slug) + '">' + statusDot(slug) + "<span><h3>" + esc(n.title) + "</h3><p>" + esc(n.summary) + '</p></span><span class="meta">' +
        (showSection ? '<span class="chip">' + esc(SECTION[n.section].title) + "</span>" : "") + icon("clock") + esc(n.time) + "</span></a>";
    }).join("") + "</div>";
  }

  function listPage(o) {
    var d = doneCount(o.notes);
    page('<div class="crumbs"><a href="#/">Get started</a> / ' + o.crumb + "</div>" +
      '<div class="page-head"><div class="list-head"><span class="icon-tile' + (o.brandIcon ? " brand" : "") + '" style="width:48px;height:48px">' + (o.logo || icon(o.icon)) + "</span>" +
      '<div style="flex:1;min-width:240px"><h1 style="margin:0">' + esc(o.title) + "</h1></div></div><p>" + esc(o.desc) + "</p>" +
      '<div class="pills">' + o.pills.map(function (p) { return '<span class="pill">' + p + "</span>"; }).join("") + "</div>" +
      '<div class="list-head" style="margin-top:22px"><div class="progress"><div class="row"><span>Progress</span><span>' + d + " / " + o.notes.length + "</span></div>" + progressBar(d, o.notes.length) + "</div>" +
      '<a class="btn primary" href="' + noteHref(nextNote(o.notes)) + '">' + (d ? "Continue" : "Start") + " " + icon("chevron") + "</a></div></div>" +
      noteList(o.notes, o.showSection));
  }

  function renderSection(id) {
    var s = SECTION[id];
    if (!s) return notFound();
    var mins = s.notes.reduce(function (a, n) { return a + (parseInt(DATA.notes[n].time, 10) || 0); }, 0);
    listPage({ crumb: esc(s.title), icon: SECTION_ICON[id], title: s.title, desc: s.blurb, notes: s.notes,
      pills: ["<b>" + s.notes.length + "</b> notes", "<b>" + Math.round(mins / 60 * 10) / 10 + "</b> hours", "<b>" + s.notes.reduce(function (a, n) { return a + DATA.notes[n].qa.length; }, 0) + "</b> questions"] });
  }

  function renderPlan(id) {
    var p = PLAN[id];
    if (!p) return notFound();
    listPage({ crumb: '<a href="#/plans">Study plans</a> / ' + esc(p.title), icon: "calendar", brandIcon: true, title: p.title + " study plan", desc: p.blurb, notes: p.notes, showSection: true,
      pills: ["<b>" + p.notes.length + "</b> notes", "Recommended schedule: <b>" + esc(p.schedule) + "</b>"] });
  }

  function renderPlans() {
    page('<div class="crumbs"><a href="#/">Get started</a> / Study plans</div><div class="page-head"><h1>Study plans</h1><p>Pick the plan that matches the time you have. Progress is shared across plans: a note done in one counts everywhere.</p></div>' +
      '<div class="grid c3">' + (DATA.plans || []).map(planCard).join("") + "</div>" +
      '<section class="block"><div class="block-head"><div><h2>Company practice sets</h2><p>Short, targeted lists.</p></div></div><div class="grid c4">' +
      (DATA.companies || []).map(function (c) {
        return '<a class="card company" href="#/company/' + c.id + '"><span class="logo" style="background:' + c.color + '">' + esc(c.name.charAt(0)) + "</span><span><h3>" + esc(c.name) + '</h3><span class="sub">' + c.notes.length + " topics</span></span></a>";
      }).join("") + "</div></section>");
  }

  function renderCompany(id) {
    var c = COMPANY[id];
    if (!c) return notFound();
    listPage({ crumb: '<a href="#/plans">Practice sets</a> / ' + esc(c.name), logo: '<span class="logo" style="background:' + c.color + ';width:100%;height:100%">' + esc(c.name.charAt(0)) + "</span>",
      title: c.name + " practice set", desc: "Designs and building blocks around the products " + c.name + " is known for. Work through them in order, then do a timed mock of the first case study.",
      notes: c.notes, showSection: true, pills: ["<b>" + c.notes.length + "</b> topics"] });
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
      else { a.setAttribute("href", GH + path); a.target = "_blank"; a.rel = "noopener"; }   // builds/, tools/ ... live on GitHub
    });
    container.querySelectorAll("img").forEach(function (img) {
      var path = normalize(dir + img.getAttribute("src"));                 // assets/diagrams/x.svg
      img.setAttribute("src", path);                                        // site/assets is a synced copy
      img.loading = "lazy";
      img.decoding = "async";
      var name = (path.match(/diagrams\/([\w-]+)\.svg$/) || [])[1];
      if (!name) return;
      var fig = el('<figure class="diagram"><div class="frame"></div></figure>');
      var p = img.parentNode;
      p.replaceChild(fig, img);
      if (p.tagName === "P" && p.childNodes.length === 1) p.parentNode.replaceChild(fig, p);
      fig.firstChild.appendChild(img);
      fig.appendChild(el("<figcaption><span>" + esc(img.alt) + '</span><a href="assets/diagrams/excalidraw/' + name + '.excalidraw" download>' + icon("pen") +
        ' Edit in Excalidraw</a><a href="assets/diagrams/' + name + '.svg" target="_blank" rel="noopener">' + icon("external") + " Open SVG</a></figcaption>"));
      img.addEventListener("click", function () { lightbox(img.src); });
    });
    container.querySelectorAll("figcaption .ic").forEach(function (i) { i.style.width = "14px"; i.style.height = "14px"; i.style.verticalAlign = "-2px"; });
    var first = container.querySelector("blockquote");
    if (first && /^TL;DR/.test((first.querySelector("strong") || {}).textContent || "")) {
      first.classList.add("tldr");
      var label = first.querySelector("p");
      if (label && label.textContent.trim() === "TL;DR") label.outerHTML = '<p class="tldr-label">' + icon("target") + " Key takeaways</p>";
    }
    container.querySelectorAll("h2, h3").forEach(function (h) {
      h.id = slugify(h.textContent);
      h.appendChild(el('<a class="anchor" href="' + noteHref(slug, h.id) + '" aria-label="Link to section">#</a>'));
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
    var sec = SECTION[n.section], idx = ORDER.indexOf(slug), prev = ORDER[idx - 1], next = ORDER[idx + 1];
    var wrap = el('<div class="note-wrap"><article></article><aside class="toc" aria-label="On this page"></aside></div>');
    var art = wrap.firstChild;
    art.innerHTML = '<div class="crumbs"><a href="#/">Get started</a> / <a href="#/section/' + sec.id + '">' + esc(sec.title) + "</a></div>" +
      '<header class="note-head"><h1>' + esc(n.title) + '</h1><p class="summary">' + esc(n.summary) + "</p>" +
      '<div class="chips">' + (n.time ? '<span class="chip">' + icon("clock") + esc(n.time) + "</span>" : "") +
      (n.level ? '<span class="chip brand">' + esc(n.level) + "</span>" : "") +
      n.tags.slice(0, 5).map(function (t) { return '<span class="chip">' + esc(t) + "</span>"; }).join("") + "</div>" +
      '<div class="note-actions"><button class="btn small' + (done[slug] ? " done" : " primary") + '" id="doneBtn">' + icon("check") + (done[slug] ? " Completed" : " Mark complete") + "</button>" +
      '<button class="btn small' + (saved[slug] ? " done" : "") + '" id="saveBtn" aria-pressed="' + !!saved[slug] + '">' + icon("bookmark") + (saved[slug] ? " Saved" : " Save for later") + "</button>" +
      (n.lab ? '<a class="btn small" href="#/lab/' + n.lab + '">' + icon("flask") + " Open the lab</a>" : "") +
      (n.qa.length ? '<a class="btn small" href="#/flashcards/' + slug + '">' + icon("cards") + " " + n.qa.length + " flashcards</a>" : "") +
      '<a class="btn small" href="' + GH + "notes/" + slug + '.md" target="_blank" rel="noopener">' + GITHUB.replace("<svg", '<svg width="15" height="15"') + " GitHub</a></div></header>" +
      '<div class="prose"></div>' +
      '<section class="memo"><div class="memo-head"><h4>' + icon("pen") + ' My notes</h4><span class="memo-status" id="memoStatus">' + (memo[slug] ? "Saved in this browser" : "Private to this browser") + "</span></div>" +
      '<textarea id="memoText" rows="4" maxlength="20000" placeholder="Jot down what to remember, a mnemonic, or what tripped you up in a mock.">' + esc(memo[slug] || "") + "</textarea></section>" +
      '<nav class="pager">' +
      (prev ? '<a href="' + noteHref(prev) + '"><small>Previous</small>' + esc(DATA.notes[prev].title) + "</a>" : "<span></span>") +
      (next ? '<a class="next" href="' + noteHref(next) + '"><small>Next</small>' + esc(DATA.notes[next].title) + "</a>" : "") + "</nav>";
    art.querySelectorAll(".note-actions .ic, .chips .ic").forEach(function (i) { i.style.width = "15px"; i.style.height = "15px"; });
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
    function refresh() { var y = window.scrollY; renderNote(slug); window.scrollTo(0, y); renderSidebar({ note: slug, key: "note" }); }
    art.querySelector("#doneBtn").addEventListener("click", function () {
      if (done[slug]) { delete done[slug]; store.set("done", done); return refresh(); }
      function complete() { done[slug] = Date.now(); store.set("done", done); bump(); refresh(); }
      if (!profile && store.ok) askName(complete); else complete();
    });
    art.querySelector("#saveBtn").addEventListener("click", function () {
      if (saved[slug]) delete saved[slug]; else saved[slug] = Date.now();
      store.set("saved", saved);
      refresh();
    });
    var memoText = art.querySelector("#memoText"), memoStatus = art.querySelector("#memoStatus");
    memoText.addEventListener("input", function () {          // localStorage writes are synchronous and cheap: save every keystroke
      var v = memoText.value;
      if (v.trim()) memo[slug] = v; else delete memo[slug];
      store.set("memo", memo);
      memoStatus.textContent = store.ok ? "Saved in this browser" : "Storage is blocked: notes will not be kept";
    });
    if (anchor) { var t = document.getElementById(anchor); if (t) t.scrollIntoView(); else window.scrollTo(0, 0); }
    else window.scrollTo(0, 0);
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
    if (!q.trim()) { results.innerHTML = '<div class="empty">Search titles, tags, headings and full text of every note.</div>'; return; }
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
    if ((e.key === "/" && !typing) || ((e.key || "").toLowerCase() === "k" && (e.metaKey || e.ctrlKey))) { e.preventDefault(); openSearch(); }
    if (e.key === "Escape") { closeSearch(); closeMenu(); var lb = document.querySelector(".lightbox"); if (lb) lb.remove(); }
  });

  // ------------------------------------------------------------ flashcards (Leitner boxes)
  function renderFlashcards(filter) {
    var boxes = store.get("boxes", {}), all = [];
    ORDER.forEach(function (slug) {
      DATA.notes[slug].qa.forEach(function (c, i) { all.push({ id: slug + "#" + i, slug: slug, q: c.q, a: c.a }); });
    });
    var scope = filter || store.get("fc-scope", "all");
    var cards = all.filter(function (c) { return scope === "all" || c.slug === scope || c.slug.indexOf(scope + "/") === 0; });
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
    page('<div class="crumbs"><a href="#/">Get started</a> / Flashcards</div><div class="page-head"><h1>Flashcards</h1>' +
      "<p>Every interview question in the notes as a spaced repetition deck. Reveal with a click or Space, then rate yourself. Missed cards come back first.</p></div>" +
      '<div class="fc-toolbar"><select id="fcScope" aria-label="Deck">' + opts + '</select><span class="lab-note" id="fcCount"></span></div>' +
      '<div class="flashcard" id="card" tabindex="0" role="button" aria-label="Flashcard, press space to flip"></div>' +
      '<div class="fc-actions"><button class="btn" id="again">Again <kbd>1</kbd></button><button class="btn primary" id="good">Got it <kbd>2</kbd></button>' +
      '<button class="btn" id="skip">Skip <kbd>&rarr;</kbd></button></div><div class="boxes" id="boxes"></div>');
    var cardEl = document.getElementById("card");
    function draw() {
      if (!cards.length) { cardEl.innerHTML = '<div class="q">No cards in this deck.</div>'; return; }
      var c = cards[i % cards.length], n = DATA.notes[c.slug];
      cardEl.innerHTML = '<div class="label"><span class="chip brand">Box ' + (boxes[c.id] || 1) + "</span>Question " + ((i % cards.length) + 1) + " of " + cards.length + "</div>" +
        '<div class="q">' + esc(c.q) + '</div><div class="src">From <a href="' + noteHref(c.slug) + '">' + esc(n.title) + "</a></div>" +
        (flipped ? '<div class="a prose">' + window.Markdown.toHtml(c.a) + "</div>" : '<p class="lab-note" style="margin-top:32px">Answer out loud first, then reveal.</p>');
      var counts = [0, 0, 0, 0, 0];
      cards.forEach(function (x) { counts[(boxes[x.id] || 1) - 1]++; });
      document.getElementById("boxes").innerHTML = counts.map(function (n, b) { return "<span>Box " + (b + 1) + ": " + n + "</span>"; }).join("");
      document.getElementById("fcCount").textContent = cards.length + " cards";
    }
    function rate(good) {
      if (!cards.length) return;
      var c = cards[i % cards.length];
      boxes[c.id] = good ? Math.min(5, (boxes[c.id] || 1) + 1) : 1;
      store.set("boxes", boxes);
      bump();
      i++; flipped = false; draw();
    }
    cardEl.addEventListener("click", function (e) { if (e.target.tagName !== "A") { flipped = !flipped; draw(); } });
    document.getElementById("again").onclick = function () { rate(false); };
    document.getElementById("good").onclick = function () { rate(true); };
    document.getElementById("skip").onclick = function () { i++; flipped = false; draw(); };
    document.getElementById("fcScope").onchange = function (e) { store.set("fc-scope", e.target.value); location.hash = "#/flashcards"; renderFlashcards(e.target.value); };
    document.onkeydown = function (e) {
      if (!/^#\/flashcards/.test(location.hash) || !modal.hidden) return;
      if (e.key === " ") { e.preventDefault(); flipped = !flipped; draw(); }
      if (e.key === "1") rate(false);
      if (e.key === "2") rate(true);
      if (e.key === "ArrowRight") { i++; flipped = false; draw(); }
    };
    draw();
  }

  // ------------------------------------------------------------ diagrams gallery
  function renderDiagrams() {
    page('<div class="crumbs"><a href="#/">Get started</a> / Diagrams</div><div class="page-head"><h1>Diagram gallery</h1>' +
      "<p>All " + DATA.diagrams.length + " hand-drawn diagrams. Download any <code>.excalidraw</code> source and open it at excalidraw.com to remix it.</p></div>" +
      '<div class="gallery">' + DATA.diagrams.map(function (d) {
        var used = d.notes.map(function (s) { return '<a href="' + noteHref(s) + '">' + esc(shortTitle(DATA.notes[s].title)) + "</a>"; }).join(", ");
        return '<figure><div class="thumb"><img loading="lazy" decoding="async" alt="' + esc(d.name) + '" src="assets/diagrams/' + d.name + '.svg"></div><figcaption><b>' + esc(d.name) + "</b>" +
          (used ? "<span>Used in " + used + "</span>" : "") + '<a href="assets/diagrams/excalidraw/' + d.name + '.excalidraw" download>Download .excalidraw</a></figcaption></figure>';
      }).join("") + "</div>");
    main.querySelectorAll(".gallery img").forEach(function (img) { img.addEventListener("click", function () { lightbox(img.src); }); });
  }

  // ------------------------------------------------------------ labs
  var LAB_ICON = { estimator: "target", availability: "activity", "load-balancer": "blocks", "hash-ring": "globe", "rate-limiter": "shield",
    cache: "database", quorum: "layers", retry: "clock", fanout: "briefcase", latency: "cpu" };
  function renderLabs() {
    page('<div class="crumbs"><a href="#/">Get started</a> / Labs</div><div class="page-head"><h1>Interactive labs</h1>' +
      "<p>Move the sliders and watch the trade-offs. Every lab links to the notes that explain it.</p></div><div class=\"grid c3\">" +
      DATA.labs.map(function (lab) {
        return '<a class="card" href="#/lab/' + lab.id + '"><span class="icon-tile brand">' + icon(LAB_ICON[lab.id] || "flask") + "</span><h3>" + esc(lab.title) + "</h3><p>" +
          esc((window.Labs[lab.id] || {}).blurb || "") + '</p><div class="foot"><span>Open lab</span>' + icon("chevron") + "</div></a>";
      }).join("") + "</div>");
  }

  function renderLab(id) {
    var lab = DATA.labs.filter(function (l) { return l.id === id; })[0], impl = window.Labs[id];
    if (!lab || !impl) return notFound();
    var related = lab.notes.map(function (s) { return '<a href="' + noteHref(s) + '">' + esc(DATA.notes[s].title) + "</a>"; }).join(" &middot; ");
    main.innerHTML = '<div class="lab"><div class="crumbs"><a href="#/">Get started</a> / <a href="#/labs">Labs</a></div>' +
      '<div class="page-head" style="margin-bottom:24px"><h1>' + esc(lab.title) + "</h1><p>" + esc(impl.blurb) + "</p>" +
      (related ? '<p class="lab-note" style="margin-top:10px">Read: ' + related + "</p>" : "") + '</div><div id="labRoot"></div></div>';
    window.scrollTo(0, 0);
    impl.render(document.getElementById("labRoot"));
  }

  // ------------------------------------------------------------ your progress (profile, stats, data controls)
  function fmtDate(t) { try { return new Date(t).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" }); } catch (e) { return ""; } }

  function heatmap(weeks) {
    var today = new Date(); today.setHours(0, 0, 0, 0);
    var start = new Date(today); start.setDate(start.getDate() - (weeks - 1) * 7 - today.getDay());   // columns start on Sunday
    var cells = "", activeDays = 0;
    for (var t = new Date(start); t <= today; t.setDate(t.getDate() + 1)) {
      var k = dayKey(t), n = activity[k] || 0, lv = !n ? 0 : n < 3 ? 1 : n < 6 ? 2 : n < 10 ? 3 : 4;
      if (n) activeDays++;
      cells += '<i class="l' + lv + '" title="' + fmtDate(t) + ": " + (n ? n + (n === 1 ? " action" : " actions") : "no activity") + '"></i>';
    }
    return '<div class="heat-wrap"><div class="heat" role="img" aria-label="' + activeDays + " active days in the last " + weeks + ' weeks">' + cells + "</div></div>" +
      '<div class="heat-legend"><span>' + activeDays + " active days in the last " + weeks + ' weeks</span><span class="scale">Less <i class="l0"></i><i class="l1"></i><i class="l2"></i><i class="l3"></i><i class="l4"></i> More</span></div>';
  }

  function miniList(slugs, empty, meta) {
    if (!slugs.length) return '<div class="empty">' + empty + "</div>";
    return '<div class="list">' + slugs.map(function (slug) {
      var n = DATA.notes[slug];
      return '<a class="row-item compact" href="' + noteHref(slug) + '">' + statusDot(slug) + "<span><h3>" + esc(shortTitle(n.title)) + "</h3>" + (meta ? "<p>" + meta(slug) + "</p>" : "") +
        '</span><span class="meta"><span class="chip">' + esc(SECTION[n.section].title) + "</span></span></a>";
    }).join("") + "</div>";
  }

  function renderProfile() {
    var d = doneCount(ORDER), boxes = store.get("boxes", {});
    var totalCards = ORDER.reduce(function (a, s) { return a + DATA.notes[s].qa.length; }, 0);
    var reviewed = Object.keys(boxes).length, mastered = Object.keys(boxes).filter(function (id) { return boxes[id] >= 5; }).length;
    var mins = ORDER.filter(function (s) { return done[s]; }).reduce(function (a, s) { return a + (parseInt(DATA.notes[s].time, 10) || 0); }, 0);
    var byTime = function (obj) { return Object.keys(obj).filter(function (s) { return DATA.notes[s]; }).sort(function (a, b) { return (+obj[b] || 0) - (+obj[a] || 0); }); };
    var savedList = byTime(saved), recent = byTime(done).slice(0, 6), memos = byTime(memo).filter(function (s) { return memo[s]; });
    var named = profile && profile.name;

    var html = '<div class="crumbs"><a href="#/">Get started</a> / Your progress</div>' +
      '<div class="page-head profile-head"><span class="avatar xl">' + (named ? esc(initials()) : icon("user")) + '</span><div style="flex:1;min-width:240px">' +
      "<h1>" + (named ? esc(profile.name) : "Your progress") + "</h1><p>" + (profile && profile.since ? "Learning since " + fmtDate(profile.since) + "." : "Add your name to personalise this page.") + "</p>" +
      '<form class="name-form" id="nameForm"><input type="text" id="nameInput" maxlength="40" placeholder="Your name" autocomplete="given-name" aria-label="Your name" value="' + esc(named ? profile.name : "") + '">' +
      '<button class="btn" type="submit">' + (named ? "Update name" : "Save name") + "</button></form></div></div>";

    html += store.ok
      ? '<div class="callout local">' + icon("lock") + "<div><b>Your progress lives in this browser.</b> It is saved in local storage on this device, so it survives refreshes, closing the tab and restarting the browser. " +
        "It does not follow you to another browser or device, and it is erased if you clear this site's data or use a private window. Export a backup to keep a copy or move it. " +
        '<span id="persistState"></span></div></div>'
      : '<div class="callout bad">' + icon("lock") + "<div><b>Your browser is blocking storage</b> (a private window or strict privacy settings), so progress resets when this tab closes. Open the site in a normal window to keep it.</div></div>";

    html += '<div class="grid kpis" style="margin-top:20px">' +
      '<div class="kpi"><span>Notes completed</span><b>' + d + " / " + ORDER.length + "</b><small>" + pct(d, ORDER.length) + "% of the syllabus</small></div>" +
      '<div class="kpi"><span>Day streak</span><b>' + streak() + "</b><small>Best: " + bestStreak() + " days</small></div>" +
      '<div class="kpi"><span>Flashcards mastered</span><b>' + mastered + " / " + totalCards + "</b><small>" + reviewed + " reviewed at least once</small></div>" +
      '<div class="kpi"><span>Reading completed</span><b>' + Math.round(mins / 6) / 10 + " h</b><small>Estimated from note lengths</small></div></div>";

    html += '<section class="block"><div class="block-head"><div><h2>Activity</h2><p>Each square is a day; completing a note or rating a flashcard counts. Keep the streak alive with one action a day.</p></div></div>' +
      '<div class="card">' + heatmap(26) + "</div></section>";

    html += '<div class="grid c2 block">' +
      '<section><div class="block-head"><div><h2>Saved for later</h2><p>' + savedList.length + ' notes bookmarked.</p></div></div>' +
      miniList(savedList, "Nothing saved yet. Use " + icon("bookmark") + " Save for later on any note.", function (s) { return "Saved " + fmtDate(saved[s]); }) + "</section>" +
      '<section><div class="block-head"><div><h2>Recently completed</h2><p>Your last finished notes.</p></div></div>' +
      miniList(recent, "No notes completed yet. Start with the <a href=\"" + noteHref("00-start-here/01-interview-framework") + "\">interview playbook</a>.",
        function (s) { return +done[s] > 1 ? "Completed " + fmtDate(done[s]) : "Completed"; }) + "</section></div>";

    html += '<section class="block"><div class="block-head"><div><h2>By section</h2><p>Where you are strong and what is left.</p></div></div><div class="sec-progress">' +
      DATA.sections.map(function (s) {
        var c = doneCount(s.notes);
        return '<a href="#/section/' + s.id + '">' + icon(SECTION_ICON[s.id] || "book") + "<span>" + esc(s.title) + "</span>" + progressBar(c, s.notes.length) + "<b>" + c + "/" + s.notes.length + "</b></a>";
      }).join("") + "</div></section>";

    if (memos.length) {
      html += '<section class="block"><div class="block-head"><div><h2>My notes</h2><p>Personal notes you wrote on ' + memos.length + " topics.</p></div></div>" +
        miniList(memos, "", function (s) { var t = memo[s].replace(/\s+/g, " ").trim(); return esc(t.length > 140 ? t.slice(0, 140) + "..." : t); }) + "</section>";
    }

    html += '<section class="block"><div class="block-head"><div><h2>Your data</h2><p>Back up your progress, move it to another browser, or start fresh.</p></div></div>' +
      '<div class="card data-actions"><div class="data-row"><div><h3>Export backup</h3><p>Download a small JSON file with your name, completed notes, flashcard boxes, bookmarks, notes and streak.</p></div>' +
      '<button class="btn primary" id="exportBtn">' + icon("download") + " Export</button></div>" +
      '<div class="data-row"><div><h3>Import backup</h3><p>Load a file exported from Blueprint 101 on another browser or device. It replaces the progress here.</p></div>' +
      '<button class="btn" id="importBtn">' + icon("upload") + ' Import</button><input type="file" id="importFile" accept="application/json,.json" hidden></div>' +
      '<div class="data-row"><div><h3>Reset progress</h3><p>Erase your name, progress, flashcards, bookmarks and notes from this browser. Theme and layout preferences stay.</p></div>' +
      '<button class="btn danger" id="resetBtn">' + icon("trash") + " Reset</button></div>" +
      '<div id="dataMsg" role="status" aria-live="polite"></div></div></section>';
    page(html);

    document.getElementById("nameForm").addEventListener("submit", function (e) {
      e.preventDefault();
      saveProfile(document.getElementById("nameInput").value);
      route();
    });
    document.getElementById("exportBtn").addEventListener("click", exportData);
    document.getElementById("importBtn").addEventListener("click", function () { document.getElementById("importFile").click(); });
    document.getElementById("importFile").addEventListener("change", function (e) {
      var f = e.target.files && e.target.files[0];
      if (f) importData(f);
      e.target.value = "";
    });
    document.getElementById("resetBtn").addEventListener("click", function () {
      if (!window.confirm("Erase all progress, flashcards, bookmarks and notes from this browser? Export a backup first if you might want them back.")) return;
      USER_KEYS.forEach(store.del);
      loadState(); paintAvatar(); route();
    });
    var ps = document.getElementById("persistState");
    if (ps && navigator.storage && navigator.storage.persisted) {
      navigator.storage.persisted().then(function (on) {
        if (on) ps.textContent = "This browser has also marked the data as persistent, so it will not be evicted to free space.";
      }).catch(function () { /* ignore */ });
    }
  }

  function dataMsg(kind, text) {
    var m = document.getElementById("dataMsg");
    if (m) m.innerHTML = '<div class="callout ' + kind + '" style="margin-top:14px">' + esc(text) + "</div>";
  }

  function exportData() {
    var data = {};
    USER_KEYS.forEach(function (k) { var v = store.get(k, null); if (v !== null) data[k] = v; });
    var json = JSON.stringify({ app: "blueprint-101", version: 1, exported: new Date().toISOString(), data: data }, null, 2);
    var a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([json], { type: "application/json" }));
    a.download = "blueprint-101-progress-" + dayKey(new Date()) + ".json";
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 0);
    dataMsg("good", "Backup downloaded. Keep the file somewhere safe, then use Import on any other browser to continue there.");
  }

  // keep only well-formed values for notes that exist, so a hand-edited or old file cannot break the app
  function cleanBackup(obj) {
    if (!obj || obj.app !== "blueprint-101" || typeof obj.data !== "object" || !obj.data) throw new Error("This is not a Blueprint 101 backup file.");
    var src = obj.data, out = {};
    function map(o, keyOk, val) {
      var r = {};
      if (o && typeof o === "object") Object.keys(o).forEach(function (k) { if (keyOk(k)) { var v = val(o[k]); if (v !== undefined) r[k] = v; } });
      return r;
    }
    var isNote = function (k) { return !!DATA.notes[k]; };
    var stamp = function (v) { return typeof v === "number" && isFinite(v) ? v : v ? 1 : undefined; };
    if (src.profile && typeof src.profile === "object") out.profile = { name: String(src.profile.name || "").slice(0, 40), since: String(src.profile.since || new Date().toISOString()) };
    out.done = map(src.done, isNote, stamp);
    out.saved = map(src.saved, isNote, stamp);
    out.memo = map(src.memo, isNote, function (v) { return typeof v === "string" && v.trim() ? v.slice(0, 20000) : undefined; });
    out.boxes = map(src.boxes, function (k) { var m = k.match(/^(.+)#\d+$/); return !!(m && DATA.notes[m[1]]); },
      function (v) { v = parseInt(v, 10); return v >= 1 && v <= 5 ? v : undefined; });
    out.activity = map(src.activity, function (k) { return /^\d{4}-\d\d-\d\d$/.test(k); },
      function (v) { v = parseInt(v, 10); return v > 0 ? Math.min(v, 1000) : undefined; });
    if (isNote(src.last)) out.last = src.last;
    return out;
  }

  function importData(file) {
    var reader = new FileReader();
    reader.onload = function () {
      var data;
      try { data = cleanBackup(JSON.parse(reader.result)); } catch (e) { return dataMsg("bad", e instanceof SyntaxError ? "That file is not valid JSON." : e.message); }
      var n = Object.keys(data.done).length;
      if (!window.confirm("Replace the progress in this browser with this backup (" + n + " notes completed" + (data.profile && data.profile.name ? ", " + data.profile.name : "") + ")?")) return;
      USER_KEYS.forEach(function (k) { if (data[k] !== undefined) store.set(k, data[k]); else store.del(k); });
      loadState(); paintAvatar(); route();
      dataMsg("good", "Backup imported: " + n + " completed notes restored.");
    };
    reader.onerror = function () { dataMsg("bad", "Could not read that file."); };
    reader.readAsText(file);
  }

  function notFound() {
    page('<div class="page-head"><h1>Not found</h1><p>That page does not exist. <a href="#/">Back to Get started</a>.</p></div>');
  }

  // ------------------------------------------------------------ chrome: menu, theme
  var sidebar = document.getElementById("sidebar"), scrim = document.getElementById("scrim");
  function closeMenu() { sidebar.classList.remove("open"); scrim.hidden = true; }
  document.getElementById("menuBtn").innerHTML = icon("menu");
  document.getElementById("menuBtn").addEventListener("click", function () {
    var open = !sidebar.classList.contains("open");
    sidebar.classList.toggle("open", open);
    scrim.hidden = !open;
  });
  scrim.addEventListener("click", closeMenu);
  document.getElementById("ghLink").innerHTML = GITHUB;
  document.querySelectorAll("[data-icon]").forEach(function (e) { e.outerHTML = icon(e.getAttribute("data-icon")); });

  var themeBtn = document.getElementById("themeBtn");
  function currentTheme() {
    return document.documentElement.getAttribute("data-theme") ||
      (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  }
  function paintThemeBtn() { themeBtn.innerHTML = icon(currentTheme() === "dark" ? "sun" : "moon"); }
  themeBtn.addEventListener("click", function () {
    var next = currentTheme() === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try { localStorage.setItem("bp-theme", next); } catch (e) { /* ignore */ }
    paintThemeBtn();
  });
  paintThemeBtn();

  function paintAvatar() {
    var b = document.getElementById("meBtn");
    if (!b) return;
    var ini = initials();
    b.innerHTML = ini ? '<span class="avatar">' + esc(ini) + "</span>" : icon("user");
    b.setAttribute("aria-label", profile && profile.name ? profile.name + ": your progress" : "Your progress");
    b.title = profile && profile.name ? profile.name : "Your progress";
  }
  paintAvatar();

  // another tab changed our data: reload it and redraw, unless the learner is typing here
  window.addEventListener("storage", function (e) {
    if (e.key === "bp-theme" && e.newValue) { document.documentElement.setAttribute("data-theme", e.newValue); paintThemeBtn(); return; }
    if (e.key !== null && String(e.key).indexOf("bp-") !== 0) return;
    loadState(); paintAvatar();
    var a = document.activeElement;
    if (a && /input|textarea/i.test(a.tagName)) return;
    if (/^#\/flashcards/.test(location.hash)) return;                 // keep the current card in place
    var y = window.scrollY; route(); window.scrollTo(0, y);
  });

  // ------------------------------------------------------------ router
  function route() {
    if (window.Labs && window.Labs._stop) window.Labs._stop();
    document.onkeydown = null;
    var h = decodeURIComponent(location.hash.replace(/^#\/?/, "")), m, r = { key: h || "home" };
    document.querySelectorAll(".top-links a").forEach(function (a) {
      var t = a.getAttribute("data-match");
      a.classList.toggle("active", t ? h.indexOf(t) === 0 : !h);
    });
    if (!h) renderHome();
    else if ((m = h.match(/^note\/([^~]+)(?:~(.*))?$/))) { r.note = m[1]; r.key = "note"; renderNote(m[1], m[2]); }
    else if (h === "roadmap") { r.note = "00-start-here/03-study-roadmap"; renderNote(r.note); }
    else if ((m = h.match(/^section\/(.+)$/))) renderSection(m[1]);
    else if (h === "plans") renderPlans();
    else if ((m = h.match(/^plan\/(.+)$/))) { r.key = "plans"; renderPlan(m[1]); }
    else if ((m = h.match(/^company\/(.+)$/))) { r.key = "plans"; renderCompany(m[1]); }
    else if ((m = h.match(/^flashcards(?:\/(.+))?$/))) { r.key = "flashcards"; renderFlashcards(m[1]); }
    else if (h === "profile") renderProfile();
    else if (h === "diagrams") renderDiagrams();
    else if (h === "labs") renderLabs();
    else if ((m = h.match(/^lab\/(.+)$/))) { r.key = "labs"; renderLab(m[1]); }
    else notFound();
    renderSidebar(r);
    closeMenu();
    if (!(r.note && m && m[2])) main.focus({ preventScroll: true });
  }

  window.addEventListener("hashchange", route);
  route();
})();
