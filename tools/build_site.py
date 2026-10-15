"""
Compile notes/ into site/content.js for the interactive reader, and refresh the
generated index section of README.md.

    python3 tools/build_site.py

The site loads content.js with a plain <script> tag, so it works from file://
as well as from any static host. Diagrams are copied into site/assets/ so the site
is self-contained (Vercel serves site/ as its root directory).
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


CORE_WEEK = [
    "00-start-here/01-interview-framework", "00-start-here/02-back-of-envelope", "01-fundamentals/02-cap-pacelc",
    "01-fundamentals/03-scalability-performance", "02-building-blocks/02-load-balancing", "02-building-blocks/03-caching",
    "02-building-blocks/07-message-queues", "02-building-blocks/08-rate-limiting", "03-data/04-replication",
    "03-data/05-sharding-partitioning", "04-networking-apis/03-api-design", "09-case-studies/01-url-shortener",
    "09-case-studies/02-twitter-news-feed", "09-case-studies/04-whatsapp-chat", "09-case-studies/08-notification-system",
]
CORE_MONTH = CORE_WEEK + [
    "01-fundamentals/01-what-is-system-design", "01-fundamentals/04-availability-reliability", "02-building-blocks/01-dns",
    "02-building-blocks/04-cdn", "02-building-blocks/05-proxies-api-gateway", "02-building-blocks/06-consistent-hashing",
    "02-building-blocks/09-unique-id-generation", "02-building-blocks/10-object-storage-and-search",
    "03-data/01-sql-acid-transactions", "03-data/02-indexes-storage-engines", "03-data/03-nosql-choosing-a-database",
    "03-data/06-distributed-transactions", "04-networking-apis/01-networking-fundamentals", "04-networking-apis/02-http-tls",
    "04-networking-apis/04-realtime-communication", "05-architecture/01-monolith-vs-microservices",
    "05-architecture/02-event-driven-cqrs-event-sourcing", "06-reliability-ops/01-resilience-patterns",
    "06-reliability-ops/02-observability", "07-security/01-authn-authz", "09-case-studies/03-instagram",
    "09-case-studies/05-youtube-netflix", "09-case-studies/06-uber-ride-hailing", "09-case-studies/07-dropbox-google-drive",
    "09-case-studies/10-payment-system", "09-case-studies/11-ecommerce-flash-sale", "09-case-studies/12-typeahead-autocomplete",
    "11-builds/01-lru-cache", "11-builds/02-rate-limiters",
]

PLANS = [
    {"id": "1-week", "title": "1 Week", "schedule": "2 hours daily", "notes": CORE_WEEK,
     "blurb": "The highest-yield concepts plus the four designs asked most often. For an interview next week."},
    {"id": "1-month", "title": "1 Month", "schedule": "6 hours weekly", "notes": CORE_MONTH,
     "blurb": "All-round coverage of building blocks, data, APIs, reliability and eleven case studies."},
    {"id": "3-months", "title": "3 Months", "schedule": "6 hours weekly", "notes": None,
     "blurb": "Everything in the repo, including LLD, advanced topics and every from-scratch build."},
]

# practice sets built around the products each company is known for
COMPANIES = [
    ("meta", "Meta", "#0866ff", ["09-case-studies/02-twitter-news-feed", "09-case-studies/03-instagram", "09-case-studies/04-whatsapp-chat",
                                 "09-case-studies/12-typeahead-autocomplete", "09-case-studies/13-distributed-cache", "09-case-studies/15-ad-click-aggregator"]),
    ("google", "Google", "#ea4335", ["09-case-studies/09-google-docs", "09-case-studies/05-youtube-netflix", "09-case-studies/12-typeahead-autocomplete",
                                     "09-case-studies/14-web-crawler", "10-advanced/01-consensus-and-clocks", "02-building-blocks/10-object-storage-and-search"]),
    ("amazon", "Amazon", "#ff9900", ["09-case-studies/11-ecommerce-flash-sale", "09-case-studies/10-payment-system", "09-case-studies/08-notification-system",
                                     "03-data/04-replication", "02-building-blocks/07-message-queues", "09-case-studies/01-url-shortener"]),
    ("uber", "Uber", "#16a34a", ["09-case-studies/06-uber-ride-hailing", "10-advanced/04-geospatial-indexing", "04-networking-apis/04-realtime-communication",
                                 "09-case-studies/10-payment-system", "10-advanced/02-stream-batch-processing"]),
    ("netflix", "Netflix", "#e50914", ["09-case-studies/05-youtube-netflix", "02-building-blocks/04-cdn", "06-reliability-ops/01-resilience-patterns",
                                       "06-reliability-ops/02-observability", "06-reliability-ops/03-disaster-recovery-multi-region"]),
    ("stripe", "Stripe", "#635bff", ["09-case-studies/10-payment-system", "03-data/06-distributed-transactions", "02-building-blocks/08-rate-limiting",
                                     "04-networking-apis/03-api-design", "07-security/02-encryption-data-network-security"]),
    ("microsoft", "Microsoft", "#00a4ef", ["09-case-studies/09-google-docs", "09-case-studies/04-whatsapp-chat", "07-security/01-authn-authz",
                                           "05-architecture/01-monolith-vs-microservices", "09-case-studies/13-distributed-cache"]),
    ("linkedin", "LinkedIn", "#0a66c2", ["09-case-studies/02-twitter-news-feed", "09-case-studies/12-typeahead-autocomplete", "09-case-studies/08-notification-system",
                                         "10-advanced/02-stream-batch-processing", "10-advanced/05-ml-system-design"]),
    ("airbnb", "Airbnb", "#ff385c", ["09-case-studies/11-ecommerce-flash-sale", "09-case-studies/10-payment-system", "10-advanced/04-geospatial-indexing",
                                     "02-building-blocks/10-object-storage-and-search", "03-data/06-distributed-transactions"]),
    ("dropbox", "Dropbox", "#0061fe", ["09-case-studies/07-dropbox-google-drive", "02-building-blocks/10-object-storage-and-search",
                                       "02-building-blocks/06-consistent-hashing", "03-data/02-indexes-storage-engines"]),
    ("slack", "Slack / Discord", "#7c3aed", ["09-case-studies/04-whatsapp-chat", "04-networking-apis/04-realtime-communication",
                                             "02-building-blocks/07-message-queues", "03-data/05-sharding-partitioning", "09-case-studies/08-notification-system"]),
    ("atlassian", "Atlassian", "#0052cc", ["09-case-studies/09-google-docs", "05-architecture/01-monolith-vs-microservices", "03-data/05-sharding-partitioning",
                                           "07-security/01-authn-authz", "06-reliability-ops/04-deployment-and-cost"]),
    ("flipkart", "Flipkart", "#2874f0", ["09-case-studies/11-ecommerce-flash-sale", "09-case-studies/10-payment-system", "02-building-blocks/03-caching",
                                         "02-building-blocks/08-rate-limiting", "09-case-studies/12-typeahead-autocomplete"]),
    ("swiggy", "Swiggy / Zomato", "#fc8019", ["09-case-studies/06-uber-ride-hailing", "10-advanced/04-geospatial-indexing", "09-case-studies/08-notification-system",
                                              "09-case-studies/10-payment-system", "04-networking-apis/04-realtime-communication"]),
]


def sync_site_assets():
    """Copy diagrams into site/assets so the site works when deployed with site/ as its root."""
    import shutil
    src = os.path.join(ROOT, "assets", "diagrams")
    dst = os.path.join(ROOT, "site", "assets", "diagrams")
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


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
        "plans": [dict(p, notes=p["notes"] or [s for sec in sections for s in sec["notes"]]) for p in PLANS],
        "companies": [{"id": i, "name": n, "color": c, "notes": ns} for i, n, c, ns in COMPANIES],
    }
    missing = [s for p in payload["plans"] for s in p["notes"] if s not in notes] + \
              [s for c in payload["companies"] for s in c["notes"] if s not in notes]
    if missing:
        raise SystemExit("unknown note slugs in plans/companies: %s" % ", ".join(sorted(set(missing))))
    sync_site_assets()
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
