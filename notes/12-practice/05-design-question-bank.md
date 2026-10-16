---
title: "Practice: System Design Question Bank"
summary: Fifty commonly asked system design questions grouped by difficulty and pattern, each with the core challenge to focus on and links to the notes that cover it, plus a mock interview routine.
tags: [practice, interview, questions, mock]
level: core
time: 20 min
---

# Practice: System Design Question Bank

> **TL;DR**
> - Practise by **pattern**, not by memorizing answers: feeds, real time, storage, correctness, search, infrastructure primitives.
> - For each question, time yourself (45 minutes), then compare with the linked notes and write down what you missed.
> - Do at least two full mocks with another person before the real interview.

## How to practise

1. Pick a question; set a 45 minute timer; follow the [Interview Framework](../00-start-here/01-interview-framework.md) out loud or on a whiteboard (Excalidraw).
2. Afterwards, open the related notes, list gaps (requirements you skipped, a missing component, a weak deep dive).
3. Re-do the same question a week later from memory.
4. Mix in [estimation](01-estimation-problems.md), [database](02-database-optimization-challenges.md), [networking](03-networking-troubleshooting-scenarios.md) and [cost](04-cost-optimization-exercises.md) drills on other days.

## Warm-up (start here)

| Question | Core challenge | Read |
|---|---|---|
| URL shortener | ID generation, read-heavy caching, 301 vs 302 | [URL Shortener](../09-case-studies/01-url-shortener.md), [Mini build](../11-builds/08-mini-url-shortener.md) |
| Pastebin | Object storage for blobs, expiry | [Object Storage](../02-building-blocks/10-object-storage-and-search.md) |
| Rate limiter | Algorithms, distributed counters, failure policy | [Rate Limiting](../02-building-blocks/08-rate-limiting.md) |
| Unique ID generator | Snowflake, clock skew | [Unique IDs](../02-building-blocks/09-unique-id-generation.md) |
| Key-value store / distributed cache | Partitioning, replication, eviction | [Distributed Cache](../09-case-studies/13-distributed-cache.md), [Consistent Hashing](../02-building-blocks/06-consistent-hashing.md) |
| Leaderboard | Sorted sets, sharded top-k | [Caching](../02-building-blocks/03-caching.md), [Probabilistic structures](../10-advanced/03-probabilistic-data-structures.md) |
| Parking lot (LLD) | Classes, patterns, concurrency | [LLD Parking Lot](../08-lld/04-lld-parking-lot.md) |

## Core (most frequently asked)

| Question | Core challenge | Read |
|---|---|---|
| Twitter / news feed | Fanout, celebrities, timeline cache | [Twitter](../09-case-studies/02-twitter-news-feed.md) |
| Instagram | Media pipeline, ranked feed | [Instagram](../09-case-studies/03-instagram.md) |
| WhatsApp / Messenger | Connections, ordering, delivery receipts | [Chat](../09-case-studies/04-whatsapp-chat.md) |
| Slack / Discord | Channels, large rooms, history | [Chat](../09-case-studies/04-whatsapp-chat.md), [WebSocket Deep Dive](../10-advanced/08-websocket-deep-dive.md) |
| YouTube / Netflix | Upload, transcoding, ABR, CDN | [Video](../09-case-studies/05-youtube-netflix.md) |
| Uber / Lyft | Location ingestion, geo index, matching | [Uber](../09-case-studies/06-uber-ride-hailing.md), [Geospatial](../10-advanced/04-geospatial-indexing.md) |
| Dropbox / Google Drive | Chunking, dedupe, sync | [Dropbox](../09-case-studies/07-dropbox-google-drive.md) |
| Notification system | Multi-channel, priority, dedupe | [Notifications](../09-case-studies/08-notification-system.md) |
| Typeahead | Trie with top-k, offline build | [Typeahead](../09-case-studies/12-typeahead-autocomplete.md) |
| Web crawler | Frontier, politeness, dedupe | [Crawler](../09-case-studies/14-web-crawler.md) |
| E-commerce checkout / flash sale | Inventory correctness, spikes | [Flash Sale](../09-case-studies/11-ecommerce-flash-sale.md) |
| Payment system | Idempotency, ledger, reconciliation | [Payments](../09-case-studies/10-payment-system.md) |
| Authentication / SSO | Tokens, sessions, MFA | [Auth System](../09-case-studies/16-authentication-system.md) |
| Yelp / nearby places | Geohash or quadtree proximity search | [Geospatial](../10-advanced/04-geospatial-indexing.md) |
| Hotel / ticket booking | Seat holds, double booking | [SQL locking](../03-data/01-sql-acid-transactions.md), [Concurrency](../08-lld/03-concurrency.md) |

## Advanced (senior and staff)

| Question | Core challenge | Read |
|---|---|---|
| Google Docs | OT vs CRDT, session servers | [Google Docs](../09-case-studies/09-google-docs.md) |
| Search engine | Sharded inverted index, ranking | [Search Engine](../09-case-studies/19-search-engine.md) |
| Recommendation engine | Retrieval + ranking, features | [Recommendations](../09-case-studies/17-recommendation-engine.md) |
| Ad server | Auction, pacing, tracking | [Ad Server](../09-case-studies/18-ad-server.md) |
| Ad click aggregator / top-k | Exactly-once streaming | [Ad Clicks](../09-case-studies/15-ad-click-aggregator.md) |
| Metrics / monitoring system | Time-series ingestion, rollups | [Observability](../06-reliability-ops/02-observability.md), [Stream Processing](../10-advanced/02-stream-batch-processing.md) |
| Distributed message queue (Kafka) | Partitioned logs, replication, consumer groups | [Message Queues](../02-building-blocks/07-message-queues.md) |
| Distributed lock service | Consensus, leases, fencing | [Consensus](../10-advanced/01-consensus-and-clocks.md) |
| Job scheduler (cron at scale) | Leader election, at-least-once, idempotency | [Cloud Patterns](../05-architecture/04-cloud-integration-patterns.md) |
| Multi-region active-active service | Conflict resolution, routing | [DR and Multi-Region](../06-reliability-ops/03-disaster-recovery-multi-region.md) |
| Object storage (S3) | Metadata vs data, erasure coding | [Object Storage](../02-building-blocks/10-object-storage-and-search.md) |
| API gateway | Routing, auth, rate limits | [API Gateway](../02-building-blocks/05-proxies-api-gateway.md) |
| Live streaming (Twitch) | Low-latency HLS, chat fanout | [Video](../09-case-studies/05-youtube-netflix.md) |
| Stock exchange / order matching | Ordering, low latency, determinism | [Consensus and Clocks](../10-advanced/01-consensus-and-clocks.md) |
| Online judge (LeetCode) | Sandboxed execution queue | [Cloud Patterns](../05-architecture/04-cloud-integration-patterns.md) |

## Mock interview routine

- **Interviewer role**: pick a question, give vague requirements, push on one deep dive, inject a failure ("the cache cluster just died"), and score with the rubric in the [Interview Framework](../00-start-here/01-interview-framework.md).
- **Candidate role**: drive the structure, state numbers and trade-offs, check in every few minutes.
- Swap roles; one mock a week for the month before interviews.

## Related

- [Interview Framework](../00-start-here/01-interview-framework.md)
- [Study Roadmap](../00-start-here/03-study-roadmap.md)
- [Resources](../13-resources/01-resources.md)
