---
title: Curated Resources
summary: The three source repositories this collection builds on, plus books, papers, engineering blogs, video channels, practice platforms and diagramming tools, grouped by what each is best for.
tags: [resources, books, papers, blogs]
level: core
time: 10 min
---

# Curated Resources

> **TL;DR**
> - Start with the three source repositories, then Designing Data-Intensive Applications for depth.
> - Read the classic papers in order: GFS, MapReduce, Bigtable, Dynamo, Kafka, Raft, Spanner.
> - Engineering blogs show how real companies solved these problems; practise with mocks and Excalidraw.

## Source repositories this collection builds on

| Repository | Best for |
|---|---|
| [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) | The classic primer: performance vs scalability, CAP, consistency/availability patterns, DNS, CDN, LB, databases, caching, async, latency numbers, solved interview questions with diagrams, and Anki flashcard decks |
| [karanpratapsingh/system-design](https://github.com/karanpratapsingh/system-design) | A full course in chapters (networking, databases, distributed systems, architecture patterns) with clear explanations and case studies (URL shortener, WhatsApp, Twitter, Netflix, Uber) |
| [ashishps1/awesome-system-design-resources](https://github.com/ashishps1/awesome-system-design-resources) | A curated index of free articles per concept, interview problems by difficulty, must-read engineering articles and papers |

## Books

| Book | Why read it |
|---|---|
| *Designing Data-Intensive Applications* (Martin Kleppmann) | The single best book on storage, replication, partitioning, transactions, consistency and stream processing. Chapters 5 to 9 are interview gold. |
| *System Design Interview* Vol 1 and 2 (Alex Xu, Sahn Lam) | Interview-shaped walkthroughs of the common questions |
| *Understanding Distributed Systems* (Roberto Vitillo) | Short, practical tour of distributed systems for engineers |
| *Database Internals* (Alex Petrov) | Storage engines and distributed database algorithms in depth |
| *Site Reliability Engineering* and *The Site Reliability Workbook* (Google, free at sre.google) | SLOs, error budgets, alerting, incident response |
| *Release It!* (Michael Nygard) | Stability patterns (circuit breakers, bulkheads) from production failures |
| *Building Microservices* (Sam Newman) | Service boundaries, decomposition, data, deployment |
| *Head First Design Patterns* / *Refactoring.Guru* (online) | Approachable LLD pattern references |

## Papers worth reading (in this order)

1. The Google File System (2003)
2. MapReduce (2004)
3. Bigtable (2006)
4. Dynamo: Amazon's Highly Available Key-value Store (2007)
5. Kafka: a Distributed Messaging System for Log Processing (2011)
6. In Search of an Understandable Consensus Algorithm (Raft, 2014)
7. Spanner: Google's Globally Distributed Database (2012)
8. The Tail at Scale (2013)
9. TAO: Facebook's Distributed Data Store for the Social Graph (2013)
10. Time, Clocks, and the Ordering of Events in a Distributed System (Lamport, 1978)
11. End-to-End Arguments in System Design (1984)
12. Large-scale cluster management at Google with Borg (2015)

## Engineering blogs

| Company | Notable topics |
|---|---|
| Netflix Tech Blog | Chaos engineering, Open Connect CDN, microservices resilience, encoding |
| Uber Engineering | H3, Schemaless, ringpop, dispatch, Kafka at scale |
| Meta Engineering | TAO, memcache at scale, f4 storage, live video |
| Discord Engineering | Storing trillions of messages (Cassandra to ScyllaDB), Elixir fanout |
| Stripe Engineering | Idempotency, API design and versioning, rate limiters |
| Cloudflare Blog | DNS, DDoS, anycast, edge compute, sliding window rate limiting |
| Slack Engineering | Vitess migration, real-time messaging infrastructure |
| Shopify Engineering | Modular monolith, flash sale resilience, pods |
| Dropbox Tech | Magic Pocket storage, sync engine rewrite |
| Instagram / Pinterest / Airbnb / LinkedIn engineering blogs | Sharding Postgres/MySQL, feeds, search, data platforms |
| AWS Architecture Blog and Builders' Library | Timeouts, retries and backoff with jitter, static stability, cell-based architecture |
| High Scalability, ByteByteGo | Architecture summaries and newsletters |

## Practice

- Mock interviews with peers (take turns as interviewer using the rubric in the [Interview Framework](../00-start-here/01-interview-framework.md)).
- Hello Interview, Exponent, interviewing.io for guided practice and real mocks.
- [fanout.sh](https://fanout.sh/system/overview): concept notes, case studies, from-scratch builds and interactive labs (the inspiration for the reader in this repo).
- The interactive site in this repo: labs, flashcards, progress tracking.

## Diagramming tools

- [Excalidraw](https://excalidraw.com): hand-drawn style whiteboard, the look used by every diagram here. Every diagram in `assets/diagrams/excalidraw/` opens directly in Excalidraw (File, Open) for editing.
- [draw.io / diagrams.net](https://app.diagrams.net): precise boxes-and-arrows with cloud icon sets.
- Most remote interviews use Excalidraw or a built-in whiteboard: practice drawing a full design in under 10 minutes.
