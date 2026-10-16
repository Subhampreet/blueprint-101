# blueprint-101

System design notes for product company interviews: concepts in depth, hand-drawn (Excalidraw style) architecture diagrams, 15 full case studies, runnable from-scratch builds, and an interactive reader with labs, flashcards and progress tracking.

> Live reader: [blueprint-101.vercel.app](https://blueprint-101.vercel.app) (or open `site/index.html` locally).

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
site/                  Static interactive reader (no build step needed to view; deploy this folder)
site/assets/           Generated copy of assets/diagrams so the deployed site is self-contained
docs/                  prd.md (what the reader is for) and design.md (the visual system)
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

Built on and cross-checked against [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer), [karanpratapsingh/system-design](https://github.com/karanpratapsingh/system-design) and [ashishps1/awesome-system-design-resources](https://github.com/ashishps1/awesome-system-design-resources). The reader's structure (concepts, case studies, builds, labs) is inspired by [fanout.sh](https://fanout.sh/system/overview). See [Resources](notes/13-resources/01-resources.md) for books, papers and engineering blogs.

## Index

<!-- index:start -->
**96 notes, 126 hand-drawn diagrams, 306 interview flashcards, 10 interactive labs.**

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
| [The HLD Process (From Prompt to Architecture)](notes/01-fundamentals/05-hld-process.md) | A step-by-step method for high-level design: personas and use cases, component identification, data flow diagrams, technology stack selection, deployment architecture, scalability planning and cost, with a worked example. |

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
| [Communication Patterns (Sync, Async, Streaming, Batch)](notes/04-networking-apis/06-communication-patterns.md) | Synchronous request-response vs asynchronous messaging, pub/sub, event-driven, streaming and batch processing, with when to use each, their failure modes, and how to mix them in one design. |
| [IP Addressing, Subnetting and Routing (BGP, OSPF, NAT)](notes/04-networking-apis/07-ip-addressing-routing.md) | IPv4 and IPv6 addressing, CIDR and subnet math with worked examples, private ranges and special addresses, NAT types and DHCP, routing tables and longest prefix match, OSPF, IS-IS, RIP and BGP in depth, anycast, multicast with IGMP, and MPLS. |
| [Protocol Deep Dives (TCP, UDP, ICMP, ARP, Email, FTP)](notes/04-networking-apis/08-protocol-deep-dives.md) | TCP header fields, flags, sequence numbers, retransmission timeouts, connection setup and teardown, congestion control (Reno, CUBIC, BBR) and QoS; UDP header and use cases; ICMP, ARP, IGMP; SMTP, POP3 and IMAP; FTP vs SFTP. |
| [Network Performance, Monitoring and Troubleshooting](notes/04-networking-apis/09-network-troubleshooting.md) | Bandwidth, latency, jitter, loss and congestion explained; TCP tuning (window scaling, slow start, MTU); the essential tools with example commands; a layered troubleshooting method; and bottleneck identification for slow or failing services. |
| [Wireless and Mobile Networking for System Design](notes/04-networking-apis/10-mobile-wireless-networking.md) | Wi-Fi standards, channels and security, cellular generations, mobile IP and handoffs, and how to design APIs and apps for mobile networks with batching, compression, bandwidth adaptation, offline support and battery-friendly networking. |

### Architecture Patterns

_Microservices, event-driven, CQRS, hexagonal, serverless_

| Note | What you will learn |
|---|---|
| [Monolith vs Microservices](notes/05-architecture/01-monolith-vs-microservices.md) | Monolith, modular monolith and microservices compared, how to draw service boundaries, communication styles, database per service, service discovery, service mesh, distributed tracing, and the real costs of going distributed. |
| [Event-Driven Architecture, CQRS and Event Sourcing](notes/05-architecture/02-event-driven-cqrs-event-sourcing.md) | Event sources, brokers and processors, event types (notification, state transfer, sourcing), CQRS read/write separation, event sourcing with snapshots and projections, and when each pattern is worth its complexity. |
| [Architecture Styles (Layered, Hexagonal, Clean, Serverless)](notes/05-architecture/03-architecture-styles.md) | Layered, hexagonal (ports and adapters), clean and onion architecture for structuring code; serverless and FaaS with cold starts, pricing and limits; and when each style fits. |
| [Cloud and Integration Patterns Catalog](notes/05-architecture/04-cloud-integration-patterns.md) | A catalog of the integration patterns (message queue, publish-subscribe, event-driven, saga, strangler fig, API gateway, adapter, facade) and cloud design patterns (circuit breaker, retry, timeout, bulkhead, queue-based load leveling, throttling, leader election, scheduler-agent-supervisor, priority queue, competing consumers, claim check, dead letter queue) with when to use each. |

### Reliability and Operations

_Resilience, observability, DR, deployment, cost_

| Note | What you will learn |
|---|---|
| [Resilience Patterns](notes/06-reliability-ops/01-resilience-patterns.md) | Timeouts, retries with exponential backoff and jitter, circuit breakers, bulkheads, load shedding, backpressure, queue-based load leveling, graceful degradation and fallbacks, and how they combine. |
| [Observability (Metrics, Logs, Traces, Alerting)](notes/06-reliability-ops/02-observability.md) | The three pillars and how to correlate them, golden signals, RED and USE, structured logging and log levels, distributed tracing and sampling, SLO-based alerting, dashboards and incident response. |
| [Disaster Recovery and Multi-Region](notes/06-reliability-ops/03-disaster-recovery-multi-region.md) | RTO and RPO, backup types and the 3-2-1 rule, DR strategies from backup-and-restore to active-active, multi-region data replication, failover testing and game days. |
| [Deployment, Infrastructure and Cost](notes/06-reliability-ops/04-deployment-and-cost.md) | Containers and Kubernetes basics, CI/CD, blue-green, canary and rolling deploys, feature flags, autoscaling, configuration management, and cost estimation and optimization (compute, storage, data transfer, reserved and spot). |
| [Cost Estimation and Optimization](notes/06-reliability-ops/05-cost-optimization.md) | How to estimate the monthly cost of a design (compute, storage, data transfer, managed services, licensing) with a worked example, then cut it with right-sizing, commitments, spot, autoscaling policies, storage tiering, database, CDN and data transfer optimization. |

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
| [Database Schema Design (Tables, Keys, Indexes, Migrations)](notes/08-lld/05-database-schema-design.md) | A practical guide to designing relational schemas for LLD rounds and real systems: table and column design, types and constraints, primary and foreign keys, B-tree, hash and full-text indexes, normalization vs denormalization trade-offs and safe schema evolution, with a worked e-commerce schema. |
| [API Implementation and Service Integration (with Code)](notes/08-lld/06-api-and-service-integration.md) | Implementing APIs properly (endpoint design, request validation, a consistent error format, offset, cursor and keyset pagination, filtering, versioning, OpenAPI and rate limiting) and integrating services with retries, timeouts, circuit breakers, bulkheads, dependency injection and configuration management. |
| [Performance Optimization (Algorithms, Memory, CPU, I/O)](notes/08-lld/07-performance-optimization.md) | Big O time and space complexity, memory management and garbage collection, finding leaks with profilers, CPU caches, branch prediction and SIMD, I/O buffering, batching and streaming, and practical tips for object creation, strings and collections. |
| [Testing and Code Quality](notes/08-lld/08-testing-and-quality.md) | The testing pyramid, unit, integration, contract and end-to-end tests, performance, load, stress and soak testing, chaos engineering, meaningful test coverage, continuous integration, and code quality tooling (linters, static analysis, coverage). |
| [Logging and Debugging](notes/08-lld/09-logging-and-debugging.md) | Structured logging, log levels and what to log, log aggregation pipelines, debug and performance logging, error tracking with stack traces and source maps, and a systematic debugging method for production issues. |

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
| [Design an Authentication System (Login, SSO, Tokens)](notes/09-case-studies/16-authentication-system.md) | Sign up and login with password, MFA and passkeys, OAuth 2.1/OIDC token issuance, short-lived JWTs with rotating refresh tokens, revocation, key rotation, session management across devices, brute-force and credential-stuffing defense, and SSO for enterprise customers. |
| [Design a Recommendation Engine](notes/09-case-studies/17-recommendation-engine.md) | End-to-end recommender design: data collection, offline training of retrieval and ranking models, embeddings and approximate nearest neighbour search, online candidate generation, ranking and re-ranking under 100 ms, feature stores, cold start, feedback loops, and A/B testing. |
| [Design an Ad Server (Targeting, Auction, Pacing)](notes/09-case-studies/18-ad-server.md) | Serving ads in about 100 ms: candidate selection with targeting indexes, click and conversion prediction, auctions (second price, first price, quality-weighted), budget pacing and frequency capping, impression and click tracking, fraud filtering, and billing. |
| [Design a Web Search Engine](notes/09-case-studies/19-search-engine.md) | Crawling, parsing and deduplication, building a sharded inverted index, link analysis (PageRank), query processing with spell correction and expansion, two-stage ranking, result caching, freshness with tiered indexes, and serving at Google-like scale. |

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
| [GraphQL Deep Dive (Schema, N+1, Caching, Federation)](notes/10-advanced/07-graphql-deep-dive.md) | Designing GraphQL schemas, solving N+1 with DataLoader and query planning, limiting query cost, implementing subscriptions for real-time updates, caching strategies (persisted queries, CDN, response and entity caches), and federating a graph across teams with a gateway. |
| [WebSocket Deep Dive (Protocol, Rooms, Scaling)](notes/10-advanced/08-websocket-deep-dive.md) | The WebSocket upgrade handshake and frame format, connection management with heartbeats and reconnection, broadcasting and room management over pub/sub, fallbacks (long polling, SSE), scaling to millions of connections, and Socket.IO vs native WebSocket. |

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
| [Build: Mini URL Shortener (End-to-End Capstone)](notes/11-builds/08-mini-url-shortener.md) | A small but complete service in one standard-library Python file that combines the other builds (SQLite with WAL, an LRU cache, a token bucket rate limiter, scrambled base62 ids, input validation, metrics with latency percentiles), plus how you would take it to production. |

### Practice

_Estimation, database, networking and cost drills plus a question bank_

| Note | What you will learn |
|---|---|
| [Practice: Scalability Estimation Problems](notes/12-practice/01-estimation-problems.md) | Twelve back-of-the-envelope problems with worked answers (QPS, storage, bandwidth, cache, servers, connections) to build speed and confidence before interviews. |
| [Practice: Database Optimization Challenges](notes/12-practice/02-database-optimization-challenges.md) | Ten realistic database performance problems (slow queries, wrong indexes, N+1, deep pagination, lock contention, hot rows, replication lag, bloat, connection storms, scaling writes) with step-by-step solutions. |
| [Practice: Networking Troubleshooting Scenarios](notes/12-practice/03-networking-troubleshooting-scenarios.md) | Ten production networking incidents (DNS, TLS, timeouts, MTU, load balancer health checks, NAT exhaustion, cross-region latency, WebSocket drops, packet loss, CORS) with a diagnosis path and fix for each. |
| [Practice: Cost Optimization Exercises](notes/12-practice/04-cost-optimization-exercises.md) | Eight cost scenarios with worked reasoning (egress-heavy media, idle dev environments, over-provisioned databases, NAT charges, log volume, GPU inference, analytics scans, reserved vs spot) to practise estimating and cutting cloud bills. |
| [Practice: System Design Question Bank](notes/12-practice/05-design-question-bank.md) | Fifty commonly asked system design questions grouped by difficulty and pattern, each with the core challenge to focus on and links to the notes that cover it, plus a mock interview routine. |

### Resources

_Books, papers, blogs and the source repos_

| Note | What you will learn |
|---|---|
| [Curated Resources](notes/13-resources/01-resources.md) | The three source repositories this collection builds on, plus books, papers, engineering blogs, video channels, practice platforms and diagramming tools, grouped by what each is best for. |
<!-- index:end -->

---

## Syllabus Checklist

The full topic list lives in [PLAN.md](PLAN.md). Every topic there is covered by the notes above; tick items off in PLAN.md as you go.

### Table of Contents
1. [Fundamentals](PLAN.md#fundamentals)
2. [Core Concepts](PLAN.md#core-concepts)
3. [Scalability & Performance](PLAN.md#scalability--performance)
4. [Data Management](PLAN.md#data-management)
5. [System Architecture Patterns](PLAN.md#system-architecture-patterns)
6. [Networking & Communication](PLAN.md#networking--communication)
7. [Security & Compliance](PLAN.md#security--compliance)
8. [High-Level Design (HLD)](PLAN.md#high-level-design-hld)
9. [Low-Level Design (LLD)](PLAN.md#low-level-design-lld)
10. [Real-World Case Studies](PLAN.md#real-world-case-studies)
11. [Advanced Topics](PLAN.md#advanced-topics)
12. [Design Patterns & Principles](PLAN.md#design-patterns--principles)



