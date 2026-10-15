# blueprint-101

System design notes for product company interviews: concepts in depth, hand-drawn (Excalidraw style) architecture diagrams, 15 full case studies, runnable from-scratch builds, and an interactive reader with labs, flashcards and progress tracking.

> Open the interactive reader: `site/index.html` (or the GitHub Pages site once Pages is enabled for this repo).

## What is inside

| | |
|---|---|
| **Notes** (`notes/`) | 71 detailed notes from fundamentals to consensus, each ending with interview questions and answers |
| **Diagrams** (`assets/diagrams/`) | 99 hand-drawn SVG diagrams, each with an editable `.excalidraw` source in `assets/diagrams/excalidraw/` |
| **Case studies** (`notes/09-case-studies/`) | URL shortener, Twitter, Instagram, WhatsApp/Slack, YouTube/Netflix, Uber, Dropbox, notifications, Google Docs, payments, flash sale, typeahead, distributed cache, web crawler, ad click aggregator |
| **Builds** (`builds/`) | Runnable Python: LRU cache, rate limiters, consistent hash ring, Bloom filter, LSM key-value store, load balancer simulation, circuit breaker |
| **Interactive site** (`site/`) | Reader with search, progress tracking, spaced-repetition flashcards from every Q&A, a diagram gallery and 10 labs (capacity estimator, availability, load balancer, hash ring, rate limiter, cache eviction, quorum, retry storms, feed fanout, latency numbers) |

## How to use it

1. **Read on GitHub**: start with [the interview framework](notes/00-start-here/01-interview-framework.md) and the [10 week roadmap](notes/00-start-here/03-study-roadmap.md).
2. **Use the interactive reader**: open `site/index.html` in a browser, or serve the repo root:

   ```bash
   python3 -m http.server 8000
   # then visit http://localhost:8000/site/
   ```

   Progress, flashcard boxes and theme are saved in your browser's local storage.
3. **Run the builds**: `python3 builds/lru_cache.py` (each file runs its own checks).
4. **Edit a diagram**: open any file from `assets/diagrams/excalidraw/` at [excalidraw.com](https://excalidraw.com) (File, Open).

## Repository layout

```text
notes/                 Markdown notes, one folder per section (front matter: title, summary, tags, level, time, lab)
assets/diagrams/       Rendered SVG diagrams used by the notes
assets/diagrams/excalidraw/   Editable .excalidraw sources for every diagram
builds/                Runnable from-scratch implementations with self-checks
site/                  Static interactive reader (no build step needed to view)
tools/diagrams/        Hand-drawn diagram engine (sketch.py) + diagram definitions (defs/)
tools/build_site.py    Compiles notes into site/content.js and refreshes the index below
tools/sync_builds.py   Embeds builds/*.py into the build notes
tools/check_notes.py   Lints front matter, links, images and the no-long-dash style rule
```

## Working on the content

```bash
python3 tools/diagrams/build.py     # re-render diagrams (SVG + .excalidraw) from tools/diagrams/defs/
python3 tools/sync_builds.py        # copy builds/*.py into the build notes
python3 tools/build_site.py         # rebuild site/content.js and the index in this README
python3 tools/check_notes.py        # lint everything (exit code 1 on problems)
```

To add a note, create `notes/<section>/<nn>-<slug>.md` with front matter like the existing notes, end it with an `## Interview questions` section of `<details>` blocks (they become flashcards automatically), and run the commands above. To add a diagram, add a function in `tools/diagrams/defs/` using the same small vocabulary (box, stack, db, queue, user, cloud, zone, note, arrow).

## Sources and inspiration

Built on and cross-checked against [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer), [karanpratapsingh/system-design](https://github.com/karanpratapsingh/system-design) and [ashishps1/awesome-system-design-resources](https://github.com/ashishps1/awesome-system-design-resources). The reader's structure (concepts, case studies, builds, labs) is inspired by [fanout.sh](https://fanout.sh/system/overview). See [Resources](notes/12-resources/01-resources.md) for books, papers and engineering blogs.

## Index

<!-- index:start -->
**71 notes, 99 hand-drawn diagrams, 205 interview flashcards, 10 interactive labs.**

### Start Here

_How to approach the interview, estimate, and plan your prep_

| Note | What you will learn |
|---|---|
| [The System Design Interview Framework](notes/00-start-here/01-interview-framework.md) | A repeatable 45 minute script for any design question, what interviewers grade, and the signals that separate a mid level answer from a senior one. |
| [Back of the Envelope Estimation](notes/00-start-here/02-back-of-envelope.md) | Numbers every engineer should know, a fast estimation method for QPS, storage, bandwidth and servers, and two fully worked examples. |
| [Study Roadmap (10 weeks)](notes/00-start-here/03-study-roadmap.md) | A week-by-week path through every note, lab, build and case study in this repo, with what you should be able to do after each phase. |

### Fundamentals

_Requirements, CAP, scaling, latency, availability_

| Note | What you will learn |
|---|---|
| [What is System Design (HLD vs LLD, Requirements)](notes/01-fundamentals/01-what-is-system-design.md) | What system design covers, how HLD differs from LLD, how to write functional and non functional requirements, and the trade-off mindset behind every design. |
| [CAP, PACELC and Consistency Models](notes/01-fundamentals/02-cap-pacelc.md) | What CAP really says (and does not), PACELC for the normal case, and the consistency spectrum from linearizable to eventual with the session guarantees interviewers ask about. |
| [Scalability, Latency and Throughput](notes/01-fundamentals/03-scalability-performance.md) | Latency vs throughput, percentiles and tail latency, Little's law, vertical vs horizontal scaling, stateless services, and how to find and remove bottlenecks. |
| [Availability, Reliability and SLOs](notes/01-fundamentals/04-availability-reliability.md) | Nines and downtime budgets, series vs parallel availability math, SLI/SLO/SLA and error budgets, redundancy patterns, and how to remove single points of failure. |

### Building Blocks

_DNS, load balancers, caches, CDNs, queues, IDs, storage_

| Note | What you will learn |
|---|---|
| [DNS (Domain Name System)](notes/02-building-blocks/01-dns.md) | How a name becomes an IP, record types, TTL and caching trade-offs, DNS based load balancing, GeoDNS, failover and DNSSEC. |
| [Load Balancing](notes/02-building-blocks/02-load-balancing.md) | Why load balancers exist, L4 vs L7, every common algorithm with its failure mode, health checks, sticky sessions, LB high availability and global load balancing. |
| [Caching](notes/02-building-blocks/03-caching.md) | Where caches live, cache-aside vs read/write-through vs write-behind, eviction policies, invalidation, stampedes, hot keys, consistency between cache and DB, and Redis vs Memcached. |
| [Content Delivery Networks (CDN)](notes/02-building-blocks/04-cdn.md) | How CDNs cut latency and origin load, push vs pull, cache keys and headers, invalidation, origin shielding, video and image delivery, and edge compute. |
| [Proxies, API Gateway and BFF](notes/02-building-blocks/05-proxies-api-gateway.md) | Forward vs reverse proxies, what an API gateway does (and should not do), Backend for Frontend, sidecars and how gateways relate to load balancers and service meshes. |
| [Consistent Hashing](notes/02-building-blocks/06-consistent-hashing.md) | Why hash mod N breaks when nodes change, the hash ring, virtual nodes, replication on the ring, and alternatives like rendezvous, jump hash and Maglev. |
| [Message Queues, Pub/Sub and Event Streams](notes/02-building-blocks/07-message-queues.md) | Why async messaging exists, queues vs pub/sub vs logs, Kafka internals, delivery semantics and idempotency, ordering, backpressure, DLQs, and choosing between Kafka, RabbitMQ, SQS and friends. |
| [Rate Limiting and Throttling](notes/02-building-blocks/08-rate-limiting.md) | Why and where to rate limit, token bucket, leaky bucket, fixed window, sliding log and sliding window counter compared, distributed limiting with Redis, and the full "design a rate limiter" answer. |
| [Unique ID Generation](notes/02-building-blocks/09-unique-id-generation.md) | Requirements for IDs in distributed systems, auto increment, UUIDv4 vs UUIDv7, ULID, Snowflake, ticket servers and range allocation, and what each costs in ordering, index locality and coordination. |
| [Object Storage and Search Engines](notes/02-building-blocks/10-object-storage-and-search.md) | Blob vs block vs file storage, how S3 style object stores work, presigned and multipart uploads, and how search engines (Elasticsearch / OpenSearch) index, rank, shard and stay in sync with the database. |

### Data

_SQL, NoSQL, indexes, replication, sharding, transactions, analytics_

| Note | What you will learn |
|---|---|
| [Relational Databases, ACID and Transactions](notes/03-data/01-sql-acid-transactions.md) | ACID in practice, isolation levels and the anomalies each one allows, MVCC, locking and deadlocks, optimistic vs pessimistic concurrency, schema design and normalization. |
| [Indexes, Storage Engines and Query Optimization](notes/03-data/02-indexes-storage-engines.md) | B+ trees vs LSM trees, index types (composite, covering, partial, hash, GIN, full text), reading EXPLAIN plans, slow query workflow, and the cost every index adds to writes. |
| [NoSQL Families and Choosing a Database](notes/03-data/03-nosql-choosing-a-database.md) | Key-value, document, wide-column, graph, time-series, search and vector databases, how to model data around access patterns, and a decision framework for picking a store in an interview. |
| [Replication](notes/03-data/04-replication.md) | Single-leader, multi-leader and leaderless replication, sync vs async, replication lag and the bugs it causes, failover and split brain, quorums, conflict resolution (LWW, vector clocks, CRDTs) and change data capture. |
| [Sharding and Partitioning](notes/03-data/05-sharding-partitioning.md) | Vertical vs horizontal partitioning, range vs hash vs directory sharding, choosing a shard key, hot spots and celebrities, cross-shard queries and transactions, secondary indexes, and resharding without downtime. |
| [Distributed Transactions, Sagas and Idempotency](notes/03-data/06-distributed-transactions.md) | Why cross-service transactions are hard, 2PC and its blocking problem, sagas (choreography vs orchestration) with compensations, the transactional outbox, idempotency keys, and exactly-once in practice. |
| [Data Warehousing and Analytics](notes/03-data/07-data-warehousing-analytics.md) | OLTP vs OLAP, columnar storage, ETL vs ELT, warehouse layers, star and snowflake schemas, slowly changing dimensions, data lakes and lakehouses, and the modern data stack. |

### Networking and APIs

_TCP/IP, HTTP, TLS, REST, GraphQL, gRPC, real time_

| Note | What you will learn |
|---|---|
| [Networking Fundamentals (OSI, TCP, UDP, QUIC, IP)](notes/04-networking-apis/01-networking-fundamentals.md) | The OSI and TCP/IP models, IP addressing and subnetting, NAT, TCP handshake, flow and congestion control, UDP and QUIC, plus the network tools and performance terms you need in interviews. |
| [HTTP, HTTPS and TLS](notes/04-networking-apis/02-http-tls.md) | HTTP/1.1 vs HTTP/2 vs HTTP/3, methods and status codes, headers and caching (Cache-Control, ETag), CORS, and how TLS works including certificates, forward secrecy and mTLS. |
| [API Design (REST, GraphQL, gRPC)](notes/04-networking-apis/03-api-design.md) | Designing resource oriented REST APIs, pagination, filtering, versioning, idempotency and error formats; GraphQL schemas, N+1 and DataLoader, federation; gRPC with protobuf and streaming; and how to choose. |
| [Real Time Communication (Polling, SSE, WebSockets)](notes/04-networking-apis/04-realtime-communication.md) | Short polling, long polling, Server-Sent Events, WebSockets and WebRTC compared, and how to scale millions of persistent connections with gateways, pub/sub, presence and reconnection. |
| [Serialization and Compression](notes/04-networking-apis/05-serialization-compression.md) | JSON vs Protocol Buffers vs Avro vs MessagePack vs Thrift, schema evolution rules, and gzip vs Brotli vs zstd vs LZ4 for APIs, storage and streams. |

### Architecture Patterns

_Microservices, event-driven, CQRS, hexagonal, serverless_

| Note | What you will learn |
|---|---|
| [Monolith vs Microservices](notes/05-architecture/01-monolith-vs-microservices.md) | Monolith, modular monolith and microservices compared, how to draw service boundaries, communication styles, database per service, service discovery, service mesh, distributed tracing, and the real costs of going distributed. |
| [Event-Driven Architecture, CQRS and Event Sourcing](notes/05-architecture/02-event-driven-cqrs-event-sourcing.md) | Event sources, brokers and processors, event types (notification, state transfer, sourcing), CQRS read/write separation, event sourcing with snapshots and projections, and when each pattern is worth its complexity. |
| [Architecture Styles (Layered, Hexagonal, Clean, Serverless)](notes/05-architecture/03-architecture-styles.md) | Layered, hexagonal (ports and adapters), clean and onion architecture for structuring code; serverless and FaaS with cold starts, pricing and limits; and when each style fits. |

### Reliability and Operations

_Resilience, observability, DR, deployment, cost_

| Note | What you will learn |
|---|---|
| [Resilience Patterns](notes/06-reliability-ops/01-resilience-patterns.md) | Timeouts, retries with exponential backoff and jitter, circuit breakers, bulkheads, load shedding, backpressure, queue-based load leveling, graceful degradation and fallbacks, and how they combine. |
| [Observability (Metrics, Logs, Traces, Alerting)](notes/06-reliability-ops/02-observability.md) | The three pillars and how to correlate them, golden signals, RED and USE, structured logging and log levels, distributed tracing and sampling, SLO-based alerting, dashboards and incident response. |
| [Disaster Recovery and Multi-Region](notes/06-reliability-ops/03-disaster-recovery-multi-region.md) | RTO and RPO, backup types and the 3-2-1 rule, DR strategies from backup-and-restore to active-active, multi-region data replication, failover testing and game days. |
| [Deployment, Infrastructure and Cost](notes/06-reliability-ops/04-deployment-and-cost.md) | Containers and Kubernetes basics, CI/CD, blue-green, canary and rolling deploys, feature flags, autoscaling, configuration management, and cost estimation and optimization (compute, storage, data transfer, reserved and spot). |

### Security

_AuthN/AuthZ, OAuth, JWT, encryption, network security, compliance_

| Note | What you will learn |
|---|---|
| [Authentication and Authorization](notes/07-security/01-authn-authz.md) | Authentication methods and MFA, sessions vs tokens, JWT structure and pitfalls, OAuth 2.0 flows (with PKCE), OpenID Connect, SAML and SSO, and RBAC vs ABAC vs ACL vs ReBAC for authorization. |
| [Encryption, Data, API and Network Security, Compliance](notes/07-security/02-encryption-data-network-security.md) | Symmetric vs asymmetric crypto, hashing and password storage, key management and envelope encryption, E2EE, data protection (PII, masking, retention), API security (OWASP), network security (firewalls, WAF, DDoS, zero trust) and compliance regimes. |

### Low-Level Design

_SOLID, design patterns, concurrency, worked LLD_

| Note | What you will learn |
|---|---|
| [OOP, SOLID and Design Principles](notes/08-lld/01-oop-solid-principles.md) | The four OOP pillars, each SOLID principle with a before/after example, DRY, KISS, YAGNI, POLA, composition over inheritance, coupling and cohesion, and error handling design. |
| [Design Patterns (Creational, Structural, Behavioral)](notes/08-lld/02-design-patterns.md) | The GoF patterns that matter in interviews with intent, a compact code sketch and a real use case each, plus object pool, null object and common anti-patterns. |
| [Concurrency and Parallelism](notes/08-lld/03-concurrency.md) | Threads vs processes, thread pools, locks, semaphores, monitors, race conditions, deadlocks and how to prevent them, async/await and coroutines, reactive streams and backpressure, plus the concurrency patterns used in LLD rounds. |
| [LLD Walkthrough: Parking Lot](notes/08-lld/04-lld-parking-lot.md) | A complete low-level design interview answer for a multi-floor parking lot, with requirements, class model, patterns, concurrency-safe allocation, fee strategies and runnable Python code. |

### Case Studies

_Full interview walkthroughs of real products_

| Note | What you will learn |
|---|---|
| [Design a URL Shortener (TinyURL / bit.ly)](notes/09-case-studies/01-url-shortener.md) | Short code generation (hash vs counter vs pre-generated keys), base62 math, read-heavy caching, 301 vs 302, analytics pipeline, custom aliases, expiry and abuse prevention. |
| [Design Twitter / X (Home Timeline)](notes/09-case-studies/02-twitter-news-feed.md) | Tweet storage, follow graph, fanout-on-write vs fanout-on-read and the hybrid for celebrities, timeline caching, ranking, real-time updates, search, notifications, and abuse prevention. |
| [Design Instagram](notes/09-case-studies/03-instagram.md) | Photo upload with presigned URLs, async image processing into multiple resolutions, CDN delivery, feed generation and ranking, likes and comments at scale, stories with TTL, and storage optimization. |
| [Design WhatsApp / Slack / Discord (Chat)](notes/09-case-studies/04-whatsapp-chat.md) | Persistent connections, message ordering with per-conversation sequence numbers, delivery guarantees and receipts, offline delivery and sync, group fanout, presence, media, end-to-end encryption, and Slack-style channels and threads. |
| [Design YouTube / Netflix (Video Streaming)](notes/09-case-studies/05-youtube-netflix.md) | Resumable uploads, a parallel transcoding DAG, adaptive bitrate streaming (HLS/DASH), CDN and ISP edge caching, playback APIs with signed URLs, view counting, recommendations and viewing analytics. |
| [Design Uber / Lyft (Ride Hailing)](notes/09-case-studies/06-uber-ride-hailing.md) | High-frequency driver location ingestion, geospatial indexing (geohash, H3, quadtrees), matching and dispatch, ETA, surge pricing, the trip state machine, rider-driver communication, payments and analytics. |
| [Design Dropbox / Google Drive (File Sync)](notes/09-case-studies/07-dropbox-google-drive.md) | Chunking and content hashing, block dedupe, metadata vs block storage, delta sync, change notifications, conflict handling, versioning, sharing and permissions. |
| [Design a Notification System](notes/09-case-studies/08-notification-system.md) | Multi-channel delivery (push, email, SMS, in-app), preferences and quiet hours, templating, prioritization, rate limiting, deduplication, retries with DLQs, provider failover, and delivery tracking. |
| [Design Google Docs / Notion (Collaborative Editing)](notes/09-case-studies/09-google-docs.md) | Real-time collaboration with Operational Transformation vs CRDTs, a session server per document, revision logs and snapshots, presence and cursors, offline edits, version history, access control and rich text. |
| [Design a Payment System (Stripe-like checkout)](notes/09-case-studies/10-payment-system.md) | Payment intents and state machines, idempotency keys, PSP integration and routing, double-entry ledgers, webhooks, reconciliation, refunds, wallets, fraud checks, PCI scope, and exactly-once money movement. |
| [Design an E-commerce Platform and Flash Sale](notes/09-case-studies/11-ecommerce-flash-sale.md) | Product catalog, search, cart, inventory reservation, order management with sagas, payments, recommendations, and surviving a flash sale with waiting rooms, atomic stock decrements and queue-based order processing. |
| [Design Search Autocomplete (Typeahead) and a Search Engine](notes/09-case-studies/12-typeahead-autocomplete.md) | Tries with precomputed top-k, offline aggregation of query logs, sharding by prefix, caching at every layer, trending and personalization, plus how a full search engine indexes and ranks. |
| [Design a Distributed Cache (Redis / Memcached cluster)](notes/09-case-studies/13-distributed-cache.md) | Single-node cache internals (hash map, LRU, TTL, memory management), partitioning with consistent hashing or slots, replication and failover, client vs proxy routing, hot keys, consistency with the database, and operational concerns. |
| [Design a Web Crawler](notes/09-case-studies/14-web-crawler.md) | URL frontier with prioritization and per-host politeness, distributed fetchers, robots.txt, DNS caching, URL and content deduplication with Bloom filters and SimHash, spider traps, recrawl scheduling and storage. |
| [Design an Ad Click Aggregator (and Top-K)](notes/09-case-studies/15-ad-click-aggregator.md) | High-volume event ingestion, stream aggregation with windows and watermarks, exactly-once counting, late and duplicate events, OLAP serving, Lambda-style batch reconciliation, and top-k heavy hitters. |

### Advanced Topics

_Consensus, clocks, streaming, sketches, geo, ML systems_

| Note | What you will learn |
|---|---|
| [Consensus, Leader Election and Clocks](notes/10-advanced/01-consensus-and-clocks.md) | Why consensus is hard (FLP, failure models), Paxos and Raft, leader election with leases and fencing, quorum systems, Byzantine fault tolerance, logical clocks (Lamport, vector), happens-before, physical clock sync (NTP, TrueTime), and session consistency guarantees. |
| [Big Data, Batch and Stream Processing](notes/10-advanced/02-stream-batch-processing.md) | MapReduce, Hadoop and Spark for batch; Kafka, Flink, Spark Streaming and Storm for streams; windows, watermarks and exactly-once state; Lambda vs Kappa architectures; and data pipeline orchestration with Airflow, Prefect and dbt. |
| [Probabilistic Data Structures](notes/10-advanced/03-probabilistic-data-structures.md) | Bloom filters, counting and cuckoo filters, HyperLogLog for cardinality, Count-Min Sketch for frequencies and heavy hitters, t-digest for percentiles, and MinHash/SimHash for similarity, with the math and where each shows up in system design. |
| [Geospatial Indexing (Geohash, Quadtree, S2, H3)](notes/10-advanced/04-geospatial-indexing.md) | Proximity search ("find nearby"), why plain lat/lng indexes fail, geohash, quadtrees, R-trees, Google S2 and Uber H3, and how Yelp, Uber and delivery apps use them. |
| [Machine Learning in System Design and MLOps](notes/10-advanced/05-ml-system-design.md) | ML infrastructure end to end, feature stores, training pipelines, model serving (real-time vs batch), versioning and registries, recommendation engines, A/B testing and experiment management, monitoring and drift, plus vector search for RAG. |
| [Blockchain and Distributed Ledgers (Interview Level)](notes/10-advanced/06-blockchain-basics.md) | Blockchain architecture, Merkle trees, consensus mechanisms (PoW, PoS, DPoS, BFT), smart contracts, cryptocurrency transactions, and scalability solutions (Layer 2, rollups, sharding), with the system design trade-offs. |

### Builds

_From-scratch implementations you can run_

| Note | What you will learn |
|---|---|
| [Build: LRU Cache](notes/11-builds/01-lru-cache.md) | An O(1) LRU cache with a hash map and doubly linked list, TTL support, thread safety and hit/miss stats, plus how real caches approximate LRU. |
| [Build: Rate Limiters](notes/11-builds/02-rate-limiters.md) | Token bucket, fixed window, sliding log and sliding window counter implemented with an injectable clock, with tests that demonstrate the boundary burst problem. |
| [Build: Consistent Hash Ring](notes/11-builds/03-consistent-hash-ring.md) | A hash ring with virtual nodes, weighted nodes and Dynamo-style preference lists, plus a test showing about 1/N keys move when a node joins versus about 90% with modulo hashing. |
| [Build: Bloom Filter](notes/11-builds/04-bloom-filter.md) | A Bloom filter sized from expected items and false positive rate, using double hashing to derive k hash functions, with a test that measures the real false positive rate. |
| [Build: LSM Key-Value Store](notes/11-builds/05-lsm-kv-store.md) | A tiny log-structured merge tree with a write-ahead log, memtable, immutable SSTables with sparse indexes, tombstones, compaction and crash recovery. |
| [Build: Load Balancer Strategies and Simulation](notes/11-builds/06-load-balancer.md) | Round robin, smooth weighted round robin, least connections, power of two choices and IP hash, plus a discrete-event simulation that shows why load-aware algorithms win when one backend is slow. |
| [Build: Circuit Breaker](notes/11-builds/07-circuit-breaker.md) | A circuit breaker with a rolling outcome window, minimum call volume, failure-rate threshold, cooldown, half-open probes and fallbacks, tested with a fake clock. |

### Resources

_Books, papers, blogs and the source repos_

| Note | What you will learn |
|---|---|
| [Curated Resources](notes/12-resources/01-resources.md) | The three source repositories this collection builds on, plus books, papers, engineering blogs, video channels, practice platforms and diagramming tools, grouped by what each is best for. |
<!-- index:end -->

---

## Syllabus Checklist

The original topic list for this repo. Tick items off as you go; every topic is covered in the notes above.

### Table of Contents
1. [Fundamentals](#fundamentals)
2. [Core Concepts](#core-concepts)
3. [Scalability & Performance](#scalability--performance)
4. [Data Management](#data-management)
5. [System Architecture Patterns](#system-architecture-patterns)
6. [Networking & Communication](#networking--communication)
7. [Security & Compliance](#security--compliance)
8. [High-Level Design (HLD)](#high-level-design-hld)
9. [Low-Level Design (LLD)](#low-level-design-lld)
10. [Real-World Case Studies](#real-world-case-studies)
11. [Advanced Topics](#advanced-topics)
12. [Design Patterns & Principles](#design-patterns--principles)

---

## Fundamentals

### System Design Basics
- [ ] What is System Design
- [ ] HLD vs LLD - Key Differences
- [ ] Design Requirements & Constraints
  - Functional Requirements
  - Non-Functional Requirements
  - Performance Requirements
  - Scalability Requirements
- [ ] CAP Theorem
  - Consistency
  - Availability
  - Partition Tolerance
- [ ] Throughput vs Latency
- [ ] Horizontal vs Vertical Scaling
- [ ] Trade-offs in System Design

### Core Metrics & Measurements
- [ ] Requests Per Second (RPS)
- [ ] Queries Per Second (QPS)
- [ ] Transactions Per Second (TPS)
- [ ] Availability & Uptime (9s)
- [ ] Latency Distribution (P50, P99, P99.9)
- [ ] Bandwidth & Throughput
- [ ] Cost Estimation
- [ ] Storage Estimation

---

## Core Concepts

### Load Balancing
- [ ] What is Load Balancing
- [ ] Load Balancing Algorithms
  - Round Robin
  - Least Connections
  - IP Hash
  - Weighted Load Balancing
  - Random
- [ ] Hardware Load Balancers vs Software Load Balancers
- [ ] Sticky Sessions
- [ ] Health Checks
- [ ] Session Persistence
- [ ] Layer 4 vs Layer 7 Load Balancing
- [ ] Global Load Balancing
- [ ] Geo-routing & Geo-steering

### API Design
- [ ] REST API Design
  - HTTP Methods (GET, POST, PUT, DELETE, PATCH)
  - Status Codes (2xx, 3xx, 4xx, 5xx)
  - Idempotency
  - Pagination
  - Filtering & Sorting
  - HATEOAS
  - Versioning
- [ ] GraphQL
  - Queries
  - Mutations
  - Subscriptions
  - Schema Design
  - N+1 Query Problems
- [ ] gRPC
  - Protocol Buffers
  - Streaming
  - Performance Benefits
- [ ] Rate Limiting & Throttling
  - Token Bucket Algorithm
  - Sliding Window
  - Leaky Bucket
- [ ] API Gateway Pattern
- [ ] API Security
  - Authentication
  - Authorization
  - API Keys
  - OAuth 2.0

### Communication Patterns
- [ ] Synchronous Communication
- [ ] Asynchronous Communication
- [ ] Pub/Sub Pattern
- [ ] Request-Response Pattern
- [ ] Batch Processing
- [ ] Streaming Data
- [ ] Event-Driven Architecture

---

## Scalability & Performance

### Caching
- [ ] Caching Strategies
  - Cache-Aside (Lazy Loading)
  - Write-Through
  - Write-Behind (Write-Back)
  - Refresh-Ahead
- [ ] Cache Invalidation
  - Time-Based Expiration (TTL)
  - Event-Based Invalidation
  - LRU Eviction
- [ ] Multi-Level Caching
  - Browser Cache
  - CDN Cache
  - Application Cache
  - Database Cache
- [ ] Cache Layers
  - In-Memory Caching (Redis, Memcached)
  - Distributed Caching
  - Cache Coherence
- [ ] Cache Busting Strategies
- [ ] Cache Stampede & Solutions
- [ ] Cache Warming

### Content Delivery
- [ ] Content Delivery Networks (CDN)
  - Edge Servers
  - Origin Servers
  - Cache Headers
  - Purging & Invalidation
- [ ] Static vs Dynamic Content
- [ ] Video Streaming & Adaptive Bitrate
- [ ] Image Optimization
  - Compression
  - Responsive Images
  - Progressive Loading

### Database Optimization
- [ ] Query Optimization
  - Indexing Strategies
  - Query Execution Plans
  - EXPLAIN Analysis
- [ ] Connection Pooling
- [ ] Read Replicas
- [ ] Sharding & Partitioning
- [ ] Denormalization
- [ ] Query Caching
- [ ] Slow Query Logs

### Compression & Serialization
- [ ] Data Compression
  - Gzip
  - Brotli
  - LZMA
- [ ] Serialization Formats
  - JSON
  - Protocol Buffers
  - Avro
  - MessagePack
  - Thrift

---

## Data Management

### Relational Databases
- [ ] ACID Properties
  - Atomicity
  - Consistency
  - Isolation
  - Durability
- [ ] Transaction Management
- [ ] Locking & Deadlocks
- [ ] Distributed Transactions
  - 2-Phase Commit (2PC)
  - Saga Pattern
- [ ] Database Scaling
  - Vertical Scaling
  - Horizontal Scaling (Sharding)
  - Read Replicas
  - Multi-Master Replication
- [ ] Common SQL Databases
  - PostgreSQL
  - MySQL
  - Oracle
  - SQL Server
- [ ] Schema Design
  - Normalization
  - Denormalization
  - Foreign Keys
  - Indexes

### NoSQL Databases
- [ ] Document Databases
  - MongoDB
  - CouchDB
  - Firebase
- [ ] Key-Value Stores
  - Redis
  - Memcached
  - DynamoDB
- [ ] Column-Family Stores
  - Cassandra
  - HBase
- [ ] Search Engines
  - Elasticsearch
  - Solr
  - OpenSearch
- [ ] Time-Series Databases
  - InfluxDB
  - Prometheus
  - TimescaleDB
- [ ] Graph Databases
  - Neo4j
  - Amazon Neptune
- [ ] Vector Databases
  - Pinecone
  - Weaviate
  - Milvus
- [ ] BASE Properties
  - Basically Available
  - Soft State
  - Eventually Consistent
- [ ] Consistency Models
  - Strong Consistency
  - Eventual Consistency
  - Causal Consistency

### Data Replication & Synchronization
- [ ] Master-Slave Replication
- [ ] Master-Master Replication
- [ ] Quorum-Based Replication
- [ ] Consistency Levels
  - Strong Consistency
  - Weak Consistency
  - Eventual Consistency
- [ ] Conflict Resolution
- [ ] Replication Lag
- [ ] Change Data Capture (CDC)
- [ ] Data Synchronization Tools
  - Kafka
  - Debezium
  - AWS DMS

### Data Warehousing & Analytics
- [ ] Data Warehouse Architecture
  - Staging Area
  - Integration Layer
  - Presentation Layer
- [ ] OLTP vs OLAP
- [ ] ETL vs ELT
- [ ] Data Marts
- [ ] Fact Tables & Dimension Tables
- [ ] Star Schema & Snowflake Schema
- [ ] Slowly Changing Dimensions (SCD)
- [ ] Data Lakes
- [ ] Modern Data Stack
  - Snowflake
  - BigQuery
  - Redshift
  - Apache Iceberg
  - Delta Lake

---

## System Architecture Patterns

### Monolithic Architecture
- [ ] Characteristics
- [ ] Advantages
- [ ] Disadvantages
- [ ] When to Use

### Microservices Architecture
- [ ] Core Concepts
- [ ] Service Boundary Definition
- [ ] Service Communication
  - REST
  - gRPC
  - Messaging
- [ ] Database Per Service
- [ ] Distributed Tracing
- [ ] Service Mesh
  - Istio
  - Linkerd
- [ ] API Gateway
- [ ] Service Discovery
- [ ] Challenges & Solutions
  - Distributed Transactions
  - Debugging
  - Monitoring
  - Deployment Complexity

### Serverless Architecture
- [ ] Function-as-a-Service (FaaS)
- [ ] AWS Lambda
- [ ] Azure Functions
- [ ] Google Cloud Functions
- [ ] Cold Start Problem
- [ ] Warm Start Optimization
- [ ] Pricing Model
- [ ] Limitations & Constraints
- [ ] Best Use Cases

### Event-Driven Architecture
- [ ] Event Sources
- [ ] Event Processors
- [ ] Event Brokers
- [ ] Event Streaming
- [ ] CQRS (Command Query Responsibility Segregation)
- [ ] Event Sourcing
- [ ] Saga Pattern for Distributed Transactions

### CQRS Pattern
- [ ] Separation of Read & Write
- [ ] Query Model vs Domain Model
- [ ] Eventual Consistency
- [ ] Benefits & Trade-offs
- [ ] Implementation Patterns

### Hexagonal Architecture (Ports & Adapters)
- [ ] Core Domain
- [ ] Ports
- [ ] Adapters
- [ ] Benefits for Testability

---

## Networking & Communication

### OSI Model & TCP/IP Stack
- [ ] Layer 1: Physical Layer
- [ ] Layer 2: Data Link Layer
  - MAC Addresses
  - Switches
- [ ] Layer 3: Network Layer
  - IP Addresses (IPv4, IPv6)
  - Routing
  - ICMP
  - Subnetting
- [ ] Layer 4: Transport Layer
  - TCP (Transmission Control Protocol)
    - Three-Way Handshake
    - Flow Control
    - Congestion Control
    - Delayed ACK
  - UDP (User Datagram Protocol)
  - QUIC
- [ ] Layer 5: Session Layer
- [ ] Layer 6: Presentation Layer
- [ ] Layer 7: Application Layer
  - HTTP/HTTPS
  - DNS
  - SMTP
  - FTP

### HTTP & HTTPS
- [ ] HTTP/1.1
  - Persistent Connections
  - Pipelining
  - Limitations
- [ ] HTTP/2
  - Multiplexing
  - Server Push
  - Header Compression
- [ ] HTTP/3
  - QUIC Protocol
  - Connection Establishment
  - 0-RTT Resumption
- [ ] HTTPS/TLS
  - SSL/TLS Handshake
  - Certificate Authority
  - Encryption Algorithms
  - Perfect Forward Secrecy
- [ ] Request Methods
- [ ] Status Codes
- [ ] Headers & Metadata
- [ ] Caching Headers (Cache-Control, ETag, Last-Modified)
- [ ] CORS (Cross-Origin Resource Sharing)

### DNS (Domain Name System)
- [ ] DNS Resolution Process
  - Recursive Queries
  - Iterative Queries
  - Authoritative Nameservers
- [ ] DNS Record Types
  - A Record
  - AAAA Record
  - CNAME Record
  - MX Record
  - NS Record
  - SOA Record
  - TXT Record
  - SRV Record
- [ ] DNS Caching
- [ ] DNS Propagation
- [ ] DNS Failover
- [ ] GeoDNS
- [ ] DNSSEC

### Networking Performance
- [ ] Bandwidth Utilization
- [ ] Latency
  - Network Latency
  - Application Latency
  - Perceived Latency
- [ ] Jitter
- [ ] Packet Loss
- [ ] Network Congestion
- [ ] TCP Tuning
  - Window Scaling
  - TCP Slow Start
  - MTU Size
- [ ] Network Monitoring Tools
  - tcpdump
  - Wireshark
  - netstat
  - ss
- [ ] Troubleshooting Network Issues

### VPN & Tunneling
- [ ] VPN Concepts
- [ ] Tunneling Protocols
  - IPSec
  - OpenVPN
  - WireGuard
- [ ] Site-to-Site VPN
- [ ] Client-to-Site VPN

### Load Balancing Deep Dive
- [ ] L4 Load Balancing
- [ ] L7 Load Balancing
- [ ] Software Load Balancers
  - NGINX
  - HAProxy
  - Envoy
- [ ] Health Checks & Failover
- [ ] Connection Pooling

---

## Security & Compliance

### Authentication & Authorization
- [ ] Authentication Methods
  - Username/Password
  - Multi-Factor Authentication (MFA)
  - Biometric Authentication
- [ ] OAuth 2.0
  - Authorization Code Flow
  - Implicit Flow
  - Client Credentials Flow
  - Resource Owner Password Credentials Flow
- [ ] OpenID Connect (OIDC)
- [ ] SAML
- [ ] JWT (JSON Web Token)
  - Token Structure
  - Signature Verification
  - Expiration & Refresh
- [ ] Session Management
  - Session Tokens
  - Cookie-Based Sessions
  - Stateless Sessions
- [ ] Single Sign-On (SSO)
- [ ] Authorization Patterns
  - Role-Based Access Control (RBAC)
  - Attribute-Based Access Control (ABAC)
  - Access Control Lists (ACL)

### Encryption & Hashing
- [ ] Symmetric Encryption
  - AES
  - DES
  - 3DES
- [ ] Asymmetric Encryption
  - RSA
  - ECC
- [ ] Hashing
  - MD5 (deprecated)
  - SHA-1 (deprecated)
  - SHA-256
  - SHA-3
  - bcrypt
  - scrypt
  - PBKDF2
- [ ] Key Management
  - Key Rotation
  - Key Escrow
  - Hardware Security Modules (HSM)
- [ ] End-to-End Encryption
- [ ] TLS/SSL Deep Dive

### API Security
- [ ] API Authentication
- [ ] API Authorization
- [ ] Rate Limiting
- [ ] Input Validation
- [ ] Output Encoding
- [ ] CORS Configuration
- [ ] API Versioning for Security
- [ ] API Key Management

### Data Security
- [ ] Data Classification
- [ ] Data Encryption at Rest
- [ ] Data Encryption in Transit
- [ ] Database Security
  - Encryption
  - Access Control
  - Audit Logging
- [ ] Personally Identifiable Information (PII) Protection
- [ ] Data Masking & Anonymization
- [ ] Data Retention & Deletion
- [ ] Backup & Disaster Recovery

### Network Security
- [ ] Firewalls
  - Stateless Firewalls
  - Stateful Firewalls
  - Web Application Firewalls (WAF)
- [ ] DDoS Protection
  - Rate Limiting
  - IP Blocking
  - Behavioral Analysis
- [ ] Intrusion Detection Systems (IDS)
- [ ] Intrusion Prevention Systems (IPS)
- [ ] VPN Security
- [ ] Network Segmentation
- [ ] Zero Trust Architecture

### Compliance & Regulations
- [ ] GDPR (General Data Protection Regulation)
- [ ] CCPA (California Consumer Privacy Act)
- [ ] HIPAA (Health Insurance Portability & Accountability Act)
- [ ] PCI DSS (Payment Card Industry Data Security Standard)
- [ ] SOC 2 Compliance
- [ ] ISO 27001
- [ ] NIST Cybersecurity Framework
- [ ] Audit Trails & Logging

---

## High-Level Design (HLD)

### HLD Components
- [ ] System Boundaries & Scope
- [ ] User Personas
- [ ] Use Cases & Workflows
- [ ] Functional Requirements
- [ ] Non-Functional Requirements
- [ ] Constraints & Assumptions

### Architecture Design
- [ ] System Diagram & Architecture Visualization
- [ ] Component Identification
  - Frontend
  - API Gateway
  - Services
  - Databases
  - Cache
  - Message Queues
  - Search Engines
  - CDN
- [ ] Data Flow Diagrams
- [ ] Component Interactions
- [ ] Technology Stack Selection
  - Programming Languages
  - Frameworks
  - Databases
  - Message Brokers
  - Infrastructure
- [ ] Deployment Architecture
  - Containerization (Docker)
  - Orchestration (Kubernetes)
  - Cloud Providers (AWS, GCP, Azure)

### Scalability Planning
- [ ] Horizontal Scaling Strategy
- [ ] Vertical Scaling Strategy
- [ ] Database Scaling
  - Read Replicas
  - Sharding
  - Partitioning
- [ ] Caching Strategy
- [ ] Content Delivery Strategy

### Resilience & Fault Tolerance
- [ ] Redundancy
- [ ] Failover Strategies
- [ ] Circuit Breaker Pattern
- [ ] Retry Logic & Exponential Backoff
- [ ] Timeout Management
- [ ] Bulkhead Pattern
- [ ] Graceful Degradation

### Monitoring & Observability
- [ ] Metrics Collection
- [ ] Logging Strategy
- [ ] Distributed Tracing
- [ ] Alerting
- [ ] Dashboards
- [ ] Incident Response

### Cost Estimation
- [ ] Infrastructure Costs
- [ ] Compute Costs
- [ ] Storage Costs
- [ ] Data Transfer Costs
- [ ] Licensing Costs

---

## Low-Level Design (LLD)

### Code Architecture
- [ ] Design Patterns
- [ ] SOLID Principles
  - Single Responsibility Principle
  - Open-Closed Principle
  - Liskov Substitution Principle
  - Interface Segregation Principle
  - Dependency Inversion Principle
- [ ] DRY (Don't Repeat Yourself)
- [ ] KISS (Keep It Simple, Stupid)
- [ ] YAGNI (You Aren't Gonna Need It)
- [ ] Package & Module Structure
- [ ] Class Design
- [ ] Method Design
- [ ] Error Handling & Exception Propagation

### Database Schema Design
- [ ] Table Design
- [ ] Column Types & Constraints
- [ ] Primary Keys & Foreign Keys
- [ ] Indexes
  - B-Tree Indexes
  - Hash Indexes
  - Full-Text Indexes
- [ ] Normalization vs Denormalization Trade-offs
- [ ] Schema Evolution & Migrations

### API Implementation
- [ ] Endpoint Design
- [ ] Request/Response Validation
- [ ] Error Response Format
- [ ] Pagination Implementation
  - Offset-Based Pagination
  - Cursor-Based Pagination
  - Keyset Pagination
- [ ] Filtering & Sorting
- [ ] Versioning Strategy
- [ ] Documentation (OpenAPI/Swagger)
- [ ] Rate Limiting Implementation

### Service Integration
- [ ] Service-to-Service Communication
- [ ] Retry Strategies
  - Exponential Backoff
  - Jitter
  - Max Retries
- [ ] Timeout Handling
- [ ] Circuit Breaker Implementation
- [ ] Bulkhead Pattern
- [ ] Dependency Injection
- [ ] Configuration Management

### Concurrency & Parallelism
- [ ] Threads & Processes
- [ ] Thread Pools
- [ ] Synchronization
  - Locks
  - Semaphores
  - Monitors
- [ ] Race Conditions
- [ ] Deadlock Prevention
- [ ] Async/Await
- [ ] Promise Handling
- [ ] Coroutines
- [ ] Reactive Programming
- [ ] Backpressure Handling

### Performance Optimization
- [ ] Algorithm Optimization
  - Time Complexity
  - Space Complexity
  - Big O Notation
- [ ] Memory Management
  - Garbage Collection
  - Memory Leaks
  - Profiling
- [ ] CPU Optimization
  - CPU Caching
  - Branch Prediction
  - SIMD
- [ ] I/O Optimization
  - Buffering
  - Batching
  - Streaming
- [ ] Object Creation Optimization
- [ ] String Handling Optimization
- [ ] Collection Usage Optimization

### Testing & Quality
- [ ] Unit Testing
- [ ] Integration Testing
- [ ] End-to-End Testing
- [ ] Performance Testing
- [ ] Load Testing
- [ ] Stress Testing
- [ ] Chaos Engineering
- [ ] Test Coverage
- [ ] Continuous Integration
- [ ] Code Quality Tools
  - Linters
  - Static Analysis
  - Code Coverage Tools

### Logging & Debugging
- [ ] Structured Logging
- [ ] Log Levels
- [ ] Log Aggregation
- [ ] Debug Logging
- [ ] Performance Logging
- [ ] Error Tracking
- [ ] Stack Traces
- [ ] Source Maps

---

## Real-World Case Studies

### Social Media Platforms

#### Twitter / X
- [ ] Core Features
  - Tweet Creation & Storage
  - Tweet Retrieval & Timeline
  - Retweets & Quotes
  - Likes & Favorites
  - Follow System
  - Notifications
- [ ] Challenges
  - Massive Concurrent Reads
  - Timeline Fanout Problem
  - Real-Time Updates
  - Global Distribution
  - Abuse Prevention
- [ ] Architectural Solutions
  - Timeline Service
  - Tweet Service
  - User Service
  - Graph Database for Follows
  - Caching Strategies
  - Fanout Models
    - Push Model
    - Pull Model
    - Hybrid Model
  - Real-Time Messaging (WebSocket)
  - Search (Elasticsearch)
- [ ] Scalability Lessons
  - Database Sharding
  - Cache Hierarchies
  - Asynchronous Processing
  - Event Streaming

#### Instagram
- [ ] Core Features
  - Photo Upload & Storage
  - Feed Generation
  - Like & Comment System
  - Story Management
  - Direct Messaging
  - Push Notifications
  - Search & Discovery
- [ ] Challenges
  - Image Processing at Scale
  - Real-Time Updates
  - Feed Ranking & Personalization
  - Relationship Fanout
  - Storage Optimization
- [ ] Architectural Solutions
  - Image Service
    - Upload Handling
    - Image Processing
    - Multi-Resolution Storage
    - CDN Distribution
  - Feed Service
    - Ranking Algorithm
    - Caching Strategies
    - Fanout Optimization
  - Comment & Like Service
    - Sharding Strategy
    - Aggregation
  - Graph Database for Relationships
  - Recommendations Engine
  - Real-Time Notifications
- [ ] Scalability Lessons
  - Eventual Consistency
  - Caching Strategies
  - Asynchronous Processing
  - Data Normalization

### Messaging Platforms
- [ ] WhatsApp / Signal
  - End-to-End Encryption
  - Message Delivery Guarantees
  - Group Messaging
  - File Sharing
- [ ] Slack / Microsoft Teams
  - Channel Management
  - Message History
  - Rich Media Handling
  - Bot Integration
  - Threading

### E-Commerce Platforms
- [ ] Product Catalog
- [ ] Shopping Cart
- [ ] Order Management
- [ ] Payment Processing
- [ ] Inventory Management
- [ ] Recommendation Engine

### Video Streaming Platforms
- [ ] Netflix / YouTube
  - Video Ingestion
  - Transcoding
  - Adaptive Bitrate Streaming
  - Content Delivery
  - Recommendation Engine
  - Viewing Analytics

### Rideshare Platforms
- [ ] Uber / Lyft
  - Real-Time Geolocation
  - Matching Algorithm
  - Pricing Calculation
  - Driver/Rider Communication
  - Payment Processing
  - Analytics

### Collaboration Tools
- [ ] Google Docs / Notion
  - Real-Time Collaboration
  - Conflict Resolution
  - Version Control
  - Access Control
  - Rich Text Editing

---

## Advanced Topics

### Distributed Systems
- [ ] Consensus Algorithms
  - Paxos
  - Raft
  - Byzantine Fault Tolerance
- [ ] Distributed Consensus Problems
  - Leader Election
  - State Replication
  - Quorum Systems
- [ ] Vector Clocks & Logical Clocks
- [ ] Happens-Before Relationship
- [ ] Eventual Consistency Guarantees
  - Read Your Write
  - Monotonic Read
  - Causal Consistency
- [ ] Distributed Deadlock Detection
- [ ] Clock Synchronization
  - NTP (Network Time Protocol)
  - Atomic Clocks
  - Clock Skew Issues

### Big Data & Stream Processing
- [ ] Batch Processing
  - MapReduce
  - Spark
  - Hadoop
- [ ] Stream Processing
  - Apache Kafka
  - Apache Flink
  - Apache Storm
  - Spark Streaming
- [ ] Lambda Architecture
- [ ] Kappa Architecture
- [ ] Data Pipelines
  - ETL Orchestration
  - Airflow
  - Prefect
  - dbt

### Machine Learning in Systems Design
- [ ] ML Infrastructure
- [ ] Feature Stores
- [ ] Model Serving
  - TensorFlow Serving
  - Triton Server
  - Model Versioning
- [ ] Real-Time Predictions
- [ ] Batch Predictions
- [ ] Recommendation Engines
  - Collaborative Filtering
  - Content-Based Filtering
  - Hybrid Approaches
- [ ] A/B Testing Infrastructure
- [ ] Experiment Management

### Blockchain & Distributed Ledger
- [ ] Blockchain Architecture
- [ ] Consensus Mechanisms
  - Proof of Work (PoW)
  - Proof of Stake (PoS)
  - Delegated Proof of Stake
- [ ] Smart Contracts
- [ ] Cryptocurrency Systems
- [ ] Scalability Solutions
  - Layer 2 Solutions
  - Sharding

### GraphQL Deep Dive
- [ ] Schema Design
- [ ] Query Optimization
  - N+1 Problem Solutions
  - DataLoader
  - Query Planning
- [ ] Subscription Implementation
- [ ] Real-Time Updates
- [ ] Caching Strategies
- [ ] Federation & Composition
- [ ] Gateway Implementation

### WebSocket & Real-Time Communication
- [ ] WebSocket Protocol
- [ ] Connection Management
- [ ] Broadcasting
- [ ] Room Management
- [ ] Fallback Mechanisms
  - Long Polling
  - Server-Sent Events (SSE)
- [ ] Scaling WebSocket Connections
  - Horizontal Scaling
  - Sticky Sessions
  - Message Broadcasting
- [ ] Socket.io vs Native WebSocket

### Machine Learning Operations (MLOps)
- [ ] Model Training Pipeline
- [ ] Model Deployment
- [ ] Model Monitoring
- [ ] Model Versioning
- [ ] A/B Testing
- [ ] Feature Stores
- [ ] Data Quality
- [ ] Model Drift Detection

### Cost Optimization
- [ ] Infrastructure Cost Analysis
- [ ] Resource Utilization
- [ ] Reserved Instances
- [ ] Spot Instances
- [ ] Auto-Scaling Policies
- [ ] Database Cost Optimization
- [ ] CDN Cost Optimization
- [ ] Data Transfer Optimization

### Disaster Recovery & Business Continuity
- [ ] RTO (Recovery Time Objective)
- [ ] RPO (Recovery Point Objective)
- [ ] Backup Strategies
  - Full Backup
  - Incremental Backup
  - Differential Backup
  - Continuous Backup
- [ ] Disaster Recovery Plans
- [ ] Failover Testing
- [ ] Geographic Redundancy
- [ ] Data Center Failover

---

## Design Patterns & Principles

### Architectural Patterns
- [ ] MVC (Model-View-Controller)
- [ ] MVP (Model-View-Presenter)
- [ ] MVVM (Model-View-ViewModel)
- [ ] Clean Architecture
- [ ] Layered Architecture
- [ ] Onion Architecture
- [ ] Screaming Architecture

### Creational Patterns
- [ ] Singleton
- [ ] Factory
- [ ] Abstract Factory
- [ ] Builder
- [ ] Prototype
- [ ] Object Pool

### Structural Patterns
- [ ] Adapter
- [ ] Decorator
- [ ] Facade
- [ ] Flyweight
- [ ] Proxy
- [ ] Bridge
- [ ] Composite

### Behavioral Patterns
- [ ] Observer
- [ ] Strategy
- [ ] Command
- [ ] State
- [ ] Template Method
- [ ] Iterator
- [ ] Mediator
- [ ] Chain of Responsibility
- [ ] Visitor

### Concurrency Patterns
- [ ] Active Object
- [ ] Monitor Object
- [ ] Thread Pool
- [ ] Producer-Consumer
- [ ] Reader-Writer Lock
- [ ] Double-Checked Locking
- [ ] Copy-On-Write

### Integration Patterns
- [ ] Message Queue
- [ ] Publish-Subscribe
- [ ] Event-Driven
- [ ] Saga Pattern
  - Choreography
  - Orchestration
- [ ] Strangler Fig Pattern
- [ ] API Gateway Pattern
- [ ] Adapter Pattern
- [ ] Facade Pattern

### Cloud Design Patterns
- [ ] Circuit Breaker
- [ ] Retry Pattern
- [ ] Timeout Pattern
- [ ] Bulkhead Pattern
- [ ] Queue-Based Load Leveling
- [ ] Throttling Pattern
- [ ] Leader Election
- [ ] Scheduler-Agent-Supervisor
- [ ] Priority Queue Pattern
- [ ] Competing Consumers
- [ ] Claim-Check Pattern
- [ ] Dead Letter Queue

### SOLID Principles
- [ ] SRP (Single Responsibility Principle)
- [ ] OCP (Open-Closed Principle)
- [ ] LSP (Liskov Substitution Principle)
- [ ] ISP (Interface Segregation Principle)
- [ ] DIP (Dependency Inversion Principle)

### Other Principles
- [ ] DRY (Don't Repeat Yourself)
- [ ] KISS (Keep It Simple, Stupid)
- [ ] YAGNI (You Aren't Gonna Need It)
- [ ] POLA (Principle of Least Astonishment)
- [ ] Composition Over Inheritance
- [ ] Coupling & Cohesion
- [ ] Convention Over Configuration
- [ ] Explicit is Better Than Implicit

---

## Must-Know Networking Concepts (Detailed)

### IP Addressing & Subnetting
- [ ] IPv4 Addressing
  - Decimal Notation
  - CIDR Notation
  - Private IP Ranges
  - Special IPs (Loopback, Broadcast, Multicast)
- [ ] IPv6 Addressing
  - Hexadecimal Notation
  - IPv6 Advantages
  - IPv6 Adoption Challenges
- [ ] Subnetting
  - Subnet Masks
  - Calculating Subnets
  - VLSM (Variable Length Subnet Masking)
- [ ] Network Address Translation (NAT)
  - Static NAT
  - Dynamic NAT
  - Port Forwarding
- [ ] DHCP (Dynamic Host Configuration Protocol)

### Routing & BGP
- [ ] Routing Basics
  - Routing Tables
  - Default Route
  - Route Priority
- [ ] Routing Protocols
  - RIP (Routing Information Protocol)
  - OSPF (Open Shortest Path First)
  - ISIS (Intermediate System to Intermediate System)
  - BGP (Border Gateway Protocol)
- [ ] BGP Deep Dive
  - Autonomous Systems
  - BGP Peers & Sessions
  - Route Advertisements
  - BGP Attributes
  - Route Selection
  - BGP Communities
- [ ] Multicast Routing
- [ ] MPLS (Multiprotocol Label Switching)

### Congestion Control & Flow Control
- [ ] TCP Congestion Control
  - Slow Start
  - Congestion Avoidance
  - Fast Retransmit
  - Fast Recovery
  - NewReno
  - CUBIC
  - BBR
- [ ] Flow Control (TCP Window)
- [ ] Buffering & Queueing
- [ ] Quality of Service (QoS)
  - Traffic Shaping
  - Traffic Policing
  - Prioritization

### Network Monitoring & Troubleshooting
- [ ] Network Metrics
  - Bandwidth
  - Latency
  - Jitter
  - Packet Loss
  - Throughput
- [ ] Monitoring Tools
  - tcpdump
  - Wireshark
  - netstat / ss
  - iftop
  - iperf
  - mtr
  - ping
  - traceroute
  - nslookup / dig
- [ ] Packet Analysis
- [ ] Bottleneck Identification
- [ ] Performance Tuning

### Firewalling & Network Security
- [ ] Firewall Types
  - Packet Filtering
  - Stateful Inspection
  - Application Proxy
  - Next-Generation Firewalls (NGFW)
- [ ] Access Control Lists (ACLs)
- [ ] Network Zones
  - DMZ (Demilitarized Zone)
  - Internal Network
  - External Network
- [ ] VPN Technologies
  - IPSec
  - OpenVPN
  - WireGuard
  - Proxying
- [ ] DDoS Protection
  - Rate Limiting
  - IP Reputation
  - Behavioral Analysis
  - Anycast Routing
  - Scrubbing Centers

### Service Discovery & Naming
- [ ] DNS Deep Dive
  - Root Nameservers
  - TLD Nameservers
  - Authoritative Nameservers
  - DNS Caching
  - DNS TTL
  - DNS Propagation
- [ ] Advanced DNS
  - DNSSEC
  - DNS Query Types
  - Zone Transfers
  - DNS Failover
  - GeoDNS
  - Weighted DNS
- [ ] Service Discovery Protocols
  - mDNS (Multicast DNS)
  - Zeroconf
  - Consul
  - Eureka
- [ ] Service Meshes
  - Istio
  - Linkerd

### Load Balancing (Network Level)
- [ ] Layer 4 Load Balancing
  - TCP/UDP Level
  - Connection Persistence
  - Performance Characteristics
- [ ] Layer 7 Load Balancing
  - HTTP-Aware
  - Header-Based Routing
  - Path-Based Routing
  - Hostname-Based Routing
- [ ] Load Balancing Algorithms
  - Round Robin
  - Least Connections
  - IP Hash
  - Consistent Hashing
  - Weighted Load Balancing
- [ ] Sticky Sessions / Session Affinity
- [ ] Health Checks
  - TCP Connection Tests
  - HTTP Probes
  - Interval & Timeout Configuration
- [ ] Global Load Balancing
  - Geo-Routing
  - Latency-Based Routing
  - Failover Strategies
- [ ] Load Balancer High Availability
  - Active-Passive
  - Active-Active
  - Keepalive Protocols

### Protocol Deep Dives
- [ ] TCP Protocol
  - TCP Header Structure
  - Connection Establishment (3-Way Handshake)
  - Data Transmission
  - Connection Termination (4-Way Handshake)
  - TCP Options
  - TCP Flags (SYN, ACK, FIN, RST)
  - Sequence Numbers & Acknowledgments
  - Retransmission Timeout (RTO)
- [ ] UDP Protocol
  - UDP Header Structure
  - Connectionless Communication
  - Checksum (optional)
  - Use Cases
- [ ] ICMP (Internet Control Message Protocol)
  - Echo Request/Reply (ping)
  - Unreachable Messages
  - Time Exceeded
  - Redirect
- [ ] IGMP (Internet Group Management Protocol)
- [ ] ARP (Address Resolution Protocol)
  - ARP Request/Reply
  - ARP Spoofing
  - Gratuitous ARP
- [ ] SMTP, POP3, IMAP
- [ ] FTP & SFTP

### Wireless & Mobile Networking
- [ ] WiFi (802.11)
  - Standards (802.11a/b/g/n/ac/ax)
  - Channels & Frequencies
  - SSID Broadcasting
  - Security (WEP, WPA, WPA2, WPA3)
- [ ] Cellular Networks
  - 2G, 3G, 4G, 5G
  - Mobile IP
  - Handoff Mechanisms
- [ ] Mobile Data Optimization
  - Connection Pooling
  - Request Batching
  - Bandwidth Adaptation
  - Battery Optimization

### Edge Computing & CDN
- [ ] CDN Architecture
  - Origin Servers
  - Edge Servers
  - Point of Presence (PoP)
  - Regional Distribution
- [ ] Content Distribution Strategies
  - Push CDN
  - Pull CDN
  - Hybrid
- [ ] Cache Headers & Invalidation
- [ ] GeoDNS & Geo-Steering
- [ ] Edge Computing Platforms
  - Cloudflare Workers
  - AWS Lambda@Edge
  - Akamai EdgeWorkers

---

## Study & Implementation Roadmap

### Phase 1: Fundamentals (Week 1-2)
- [ ] Complete Fundamentals & Core Concepts sections
- [ ] Understand CAP Theorem & Trade-offs
- [ ] Learn Load Balancing basics
- [ ] Master Networking Basics (OSI Model, TCP/IP)

### Phase 2: Core Technologies (Week 3-4)
- [ ] Databases (SQL & NoSQL)
- [ ] Caching Strategies
- [ ] API Design
- [ ] Networking Deep Dive

### Phase 3: Architecture Patterns (Week 5-6)
- [ ] Monolithic vs Microservices
- [ ] Event-Driven Architecture
- [ ] CQRS & Event Sourcing
- [ ] Design Patterns

### Phase 4: System Design at Scale (Week 7-8)
- [ ] HLD Design Process
- [ ] LLD Design Process
- [ ] Real-World Case Studies
- [ ] Advanced Topics

### Phase 5: Practical Implementation (Week 9-10)
- [ ] Build a small system end-to-end
- [ ] Implement caching layer
- [ ] Set up monitoring & observability
- [ ] Performance optimization

### Phase 6: Specialization (Ongoing)
- [ ] Choose specialization area
- [ ] Deep dive into advanced topics
- [ ] Stay updated with latest technologies

---

## Resources & References

### Key Topics for Interview Preparation
- [ ] Design YouTube / Netflix
- [ ] Design Instagram Feed
- [ ] Design Twitter Timeline
- [ ] Design Uber / Lyft
- [ ] Design Slack / Discord
- [ ] Design Dropbox / Google Drive
- [ ] Design Notification System
- [ ] Design Rate Limiter
- [ ] Design URL Shortener
- [ ] Design Distributed Cache
- [ ] Design Search Engine
- [ ] Design Payment System
- [ ] Design Authentication System
- [ ] Design Recommendation Engine
- [ ] Design Ad Server

### Practice Domains
- [ ] System Design Interview Questions
- [ ] Networking Troubleshooting Scenarios
- [ ] Database Optimization Challenges
- [ ] Scalability Estimation Problems
- [ ] Cost Optimization Exercises

---

