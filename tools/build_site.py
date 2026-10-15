"""
Compile notes/ into site/content.js for the interactive reader, and refresh the
generated index section of README.md.

    python3 tools/build_site.py

The site loads content.js with a plain <script> tag, so it works from file://
as well as from any static host (GitHub Pages, Netlify, `python3 -m http.server`).
"""

import glob
import json
import os
import re
from datetime import date

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NOTES = os.path.join(ROOT, "notes")
OUT = os.path.join(ROOT, "site", "content.js")
README = os.path.join(ROOT, "README.md")

SECTIONS = {
    "00-start-here": ("Start Here", "How to approach the interview, estimate, and plan your prep"),
    "01-fundamentals": ("Fundamentals", "Requirements, CAP, scaling, latency, availability"),
    "02-building-blocks": ("Building Blocks", "DNS, load balancers, caches, CDNs, queues, IDs, storage"),
    "03-data": ("Data", "SQL, NoSQL, indexes, replication, sharding, transactions, analytics"),
    "04-networking-apis": ("Networking and APIs", "TCP/IP, HTTP, TLS, REST, GraphQL, gRPC, real time"),
    "05-architecture": ("Architecture Patterns", "Microservices, event-driven, CQRS, hexagonal, serverless"),
    "06-reliability-ops": ("Reliability and Operations", "Resilience, observability, DR, deployment, cost"),
    "07-security": ("Security", "AuthN/AuthZ, OAuth, JWT, encryption, network security, compliance"),
    "08-lld": ("Low-Level Design", "SOLID, design patterns, concurrency, worked LLD"),
    "09-case-studies": ("Case Studies", "Full interview walkthroughs of real products"),
    "10-advanced": ("Advanced Topics", "Consensus, clocks, streaming, sketches, geo, ML systems"),
    "11-builds": ("Builds", "From-scratch implementations you can run"),
    "12-resources": ("Resources", "Books, papers, blogs and the source repos"),
}

LABS = {
    "estimator": "Capacity Estimator",
    "availability": "Availability Calculator",
    "load-balancer": "Load Balancer Simulator",
    "hash-ring": "Consistent Hash Ring",
    "rate-limiter": "Rate Limiter Playground",
    "cache": "Cache Eviction Simulator",
    "quorum": "Quorum Explorer",
    "retry": "Retry Storm Visualizer",
    "fanout": "Feed Fanout Calculator",
    "latency": "Latency Numbers",
}


def parse_front_matter(text):
    end = text.index("\n---\n", 4)
    meta = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            v = [t.strip() for t in v[1:-1].split(",") if t.strip()]
        elif len(v) >= 2 and v[0] == v[-1] == '"':
            v = v[1:-1]
        meta[k.strip()] = v
    return meta, text[end + 5:]


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s).strip()


def extract_qa(body):
    qa = []
    for m in re.finditer(r"<details>\s*<summary>(.*?)</summary>(.*?)</details>", body, re.S):
        qa.append({"q": strip_tags(m.group(1)), "a": m.group(2).strip()})
    return qa


def plain_text(body):
    t = re.sub(r"```.*?```", " ", body, flags=re.S)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"[#*`|>_-]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def build():
    sections, notes, diagram_refs = [], {}, {}
    for folder in sorted(os.listdir(NOTES)):
        path = os.path.join(NOTES, folder)
        if not os.path.isdir(path):
            continue
        title, blurb = SECTIONS.get(folder, (folder, ""))
        sec = {"id": folder, "title": title, "blurb": blurb, "notes": []}
        for f in sorted(glob.glob(os.path.join(path, "*.md"))):
            slug = folder + "/" + os.path.basename(f)[:-3]
            meta, body = parse_front_matter(open(f, encoding="utf-8").read())
            for d in re.findall(r"assets/diagrams/([\w-]+)\.svg", body):
                diagram_refs.setdefault(d, [])
                if slug not in diagram_refs[d]:
                    diagram_refs[d].append(slug)
            notes[slug] = {
                "slug": slug,
                "section": folder,
                "title": meta.get("title", slug),
                "summary": meta.get("summary", ""),
                "tags": meta.get("tags", []),
                "level": meta.get("level", ""),
                "time": meta.get("time", ""),
                "lab": meta.get("lab", ""),
                "md": body,
                "headings": re.findall(r"^## (.+)$", body, re.M),
                "qa": extract_qa(body),
                "text": plain_text(body)[:6000],
            }
            sec["notes"].append(slug)
        sections.append(sec)

    diagrams = []
    for svg in sorted(glob.glob(os.path.join(ROOT, "assets", "diagrams", "*.svg"))):
        name = os.path.basename(svg)[:-4]
        diagrams.append({"name": name, "notes": diagram_refs.get(name, [])})

    payload = {
        "generated": date.today().isoformat(),
        "sections": sections,
        "notes": notes,
        "diagrams": diagrams,
        "labs": [{"id": k, "title": v, "notes": [s for s, n in notes.items() if n["lab"] == k]}
                 for k, v in LABS.items()],
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("/* generated by tools/build_site.py, do not edit by hand */\n")
        f.write("window.BLUEPRINT = ")
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    qa_total = sum(len(n["qa"]) for n in notes.values())
    print("site/content.js: %d notes, %d diagrams, %d flashcards" % (len(notes), len(diagrams), qa_total))
    update_readme(sections, notes, len(diagrams), qa_total)


def update_readme(sections, notes, n_diagrams, n_cards):
    start, end = "<!-- index:start -->", "<!-- index:end -->"
    text = open(README, encoding="utf-8").read()
    if start not in text:
        return
    lines = ["", "**%d notes, %d hand-drawn diagrams, %d interview flashcards, %d interactive labs.**" % (
        len(notes), n_diagrams, n_cards, len(LABS)), ""]
    for sec in sections:
        lines.append("### %s" % sec["title"])
        lines.append("")
        lines.append("_%s_" % sec["blurb"])
        lines.append("")
        lines.append("| Note | What you will learn |")
        lines.append("|---|---|")
        for slug in sec["notes"]:
            n = notes[slug]
            lines.append("| [%s](notes/%s.md) | %s |" % (n["title"], slug, n["summary"]))
        lines.append("")
    new = text[: text.index(start) + len(start)] + "\n".join(lines) + text[text.index(end):]
    open(README, "w", encoding="utf-8").write(new)
    print("README.md index refreshed")


if __name__ == "__main__":
    build()
