---
title: Study Roadmap (10 weeks)
summary: A week-by-week path through every note, lab, build and case study in this repo, with what you should be able to do after each phase.
tags: [roadmap, plan, interview]
level: core
time: 10 min
---

# Study Roadmap

About 8 to 10 hours a week for 10 weeks. Each phase ends with something you can **do**, not just something you read. Track progress with the checkboxes in the interactive site (they persist in your browser).

## Phase 1: Foundations (Weeks 1 to 2)

| Read | Practice |
|---|---|
| [Interview Framework](01-interview-framework.md) | Write the 7-step template from memory |
| [Back of the Envelope](02-back-of-envelope.md) | **Capacity Estimator** lab: estimate Twitter, YouTube, WhatsApp |
| [What is System Design](../01-fundamentals/01-what-is-system-design.md) | List FR/NFRs for 5 products |
| [CAP, PACELC, Consistency](../01-fundamentals/02-cap-pacelc.md) | **Quorum Explorer** lab |
| [Scalability, Latency, Throughput](../01-fundamentals/03-scalability-performance.md) | Little's law exercises |
| [Availability and SLOs](../01-fundamentals/04-availability-reliability.md) | **Availability Calculator** lab |
| [Networking Fundamentals](../04-networking-apis/01-networking-fundamentals.md), [HTTP and TLS](../04-networking-apis/02-http-tls.md), [DNS](../02-building-blocks/01-dns.md) | Explain "what happens when you type a URL" in 3 minutes |

**You can now**: scope a problem, estimate it, and reason about consistency and availability trade-offs with numbers.

## Phase 2: Core building blocks (Weeks 3 to 4)

| Read | Practice |
|---|---|
| [Load Balancing](../02-building-blocks/02-load-balancing.md) | **Load Balancer Simulator** lab, [build](../11-builds/06-load-balancer.md) |
| [Caching](../02-building-blocks/03-caching.md), [CDN](../02-building-blocks/04-cdn.md) | **Cache Simulator** lab, [LRU build](../11-builds/01-lru-cache.md) |
| [API Design](../04-networking-apis/03-api-design.md), [Proxies and Gateway](../02-building-blocks/05-proxies-api-gateway.md) | Write APIs for 3 case studies |
| [Rate Limiting](../02-building-blocks/08-rate-limiting.md) | **Rate Limiter Playground** lab, [build](../11-builds/02-rate-limiters.md) |
| [Consistent Hashing](../02-building-blocks/06-consistent-hashing.md) | **Hash Ring** lab, [build](../11-builds/03-consistent-hash-ring.md) |
| [Message Queues](../02-building-blocks/07-message-queues.md), [Real Time](../04-networking-apis/04-realtime-communication.md) | Explain at-least-once + idempotency |
| [Unique IDs](../02-building-blocks/09-unique-id-generation.md), [Object Storage and Search](../02-building-blocks/10-object-storage-and-search.md) | |

**You can now**: draw a correct high level design for most products and justify each box.

## Phase 3: Data (Weeks 5 to 6)

| Read | Practice |
|---|---|
| [SQL, ACID, Transactions](../03-data/01-sql-acid-transactions.md), [Indexes and Storage Engines](../03-data/02-indexes-storage-engines.md) | [LSM build](../11-builds/05-lsm-kv-store.md) |
| [NoSQL and Choosing a Database](../03-data/03-nosql-choosing-a-database.md) | Pick a store for 10 access patterns |
| [Replication](../03-data/04-replication.md), [Sharding](../03-data/05-sharding-partitioning.md) | Choose shard keys for 5 systems |
| [Distributed Transactions](../03-data/06-distributed-transactions.md), [Warehousing](../03-data/07-data-warehousing-analytics.md) | Design a saga for checkout |

**You can now**: go deep on the data layer, the most common deep dive.

## Phase 4: Architecture, reliability, security (Week 7)

[Monolith vs Microservices](../05-architecture/01-monolith-vs-microservices.md), [Event-Driven and CQRS](../05-architecture/02-event-driven-cqrs-event-sourcing.md), [Architecture Styles](../05-architecture/03-architecture-styles.md), [Resilience Patterns](../06-reliability-ops/01-resilience-patterns.md) ([circuit breaker build](../11-builds/07-circuit-breaker.md), **Retry Storm** lab), [Observability](../06-reliability-ops/02-observability.md), [DR and Multi-Region](../06-reliability-ops/03-disaster-recovery-multi-region.md), [Deployment and Cost](../06-reliability-ops/04-deployment-and-cost.md), [AuthN/AuthZ](../07-security/01-authn-authz.md), [Encryption and Security](../07-security/02-encryption-data-network-security.md).

**You can now**: answer the senior-level follow-ups: failures, rollouts, multi-region, security, cost.

## Phase 5: Case studies (Weeks 8 to 9)

Do each one **yourself first** (45 minutes, timer on, talk out loud or write), then read the note and diff your answer.

1. [URL Shortener](../09-case-studies/01-url-shortener.md)
2. [Twitter News Feed](../09-case-studies/02-twitter-news-feed.md) (+ **Fanout Calculator** lab)
3. [Instagram](../09-case-studies/03-instagram.md)
4. [WhatsApp / Slack Chat](../09-case-studies/04-whatsapp-chat.md)
5. [YouTube / Netflix](../09-case-studies/05-youtube-netflix.md)
6. [Uber](../09-case-studies/06-uber-ride-hailing.md)
7. [Dropbox](../09-case-studies/07-dropbox-google-drive.md)
8. [Notification System](../09-case-studies/08-notification-system.md)
9. [Google Docs](../09-case-studies/09-google-docs.md)
10. [Payment System](../09-case-studies/10-payment-system.md)
11. [E-commerce Flash Sale](../09-case-studies/11-ecommerce-flash-sale.md)
12. [Typeahead and Search](../09-case-studies/12-typeahead-autocomplete.md)
13. [Distributed Cache](../09-case-studies/13-distributed-cache.md)
14. [Web Crawler](../09-case-studies/14-web-crawler.md)
15. [Ad Click Aggregator](../09-case-studies/15-ad-click-aggregator.md)

## Phase 6: LLD and advanced (Week 10, then ongoing)

- LLD: [OOP and SOLID](../08-lld/01-oop-solid-principles.md), [Design Patterns](../08-lld/02-design-patterns.md), [Concurrency](../08-lld/03-concurrency.md), [Parking Lot](../08-lld/04-lld-parking-lot.md).
- Advanced: [Consensus and Clocks](../10-advanced/01-consensus-and-clocks.md), [Stream and Batch](../10-advanced/02-stream-batch-processing.md), [Probabilistic Structures](../10-advanced/03-probabilistic-data-structures.md) ([Bloom build](../11-builds/04-bloom-filter.md)), [Geospatial](../10-advanced/04-geospatial-indexing.md), [ML Systems](../10-advanced/05-ml-system-design.md), [Blockchain](../10-advanced/06-blockchain-basics.md).
- Daily: 15 minutes of **Flashcards** in the site (every note's interview questions become cards).
- Weekly: one mock interview with a peer; read one engineering blog post or paper from [Resources](../12-resources/01-resources.md).

## The week before an interview

- Re-read the [Interview Framework](01-interview-framework.md) and your own notes on mistakes.
- Re-do 4 case studies most likely for that company (social: feed/chat; marketplace: payments/flash sale/Uber; infra: cache/rate limiter/queue).
- Practice drawing fast: the diagrams here are built from 6 shapes (box, stack, cylinder, queue, actor, zone). Use the same vocabulary on Excalidraw during the interview.
