---
title: "Practice: Scalability Estimation Problems"
summary: Twelve back-of-the-envelope problems with worked answers (QPS, storage, bandwidth, cache, servers, connections) to build speed and confidence before interviews.
tags: [practice, estimation, qps, storage, bandwidth]
level: core
time: 45 min
lab: estimator
---

# Practice: Scalability Estimation Problems

> **TL;DR**
> - Do each problem on paper in under 3 minutes before opening the answer.
> - Round aggressively: 1 day is about 10^5 seconds, 1M/day is about 12/s, 1B/day is about 12k/s.
> - Always finish with "so what": the design decision the number drives.

Reference: [Back of the Envelope](../00-start-here/02-back-of-envelope.md). You can check answers with the **Capacity Estimator** lab.

## Problems

<details>
<summary>1. A chat app has 50M DAU sending 40 messages a day each. What are average and peak write QPS?</summary>

50M x 40 = 2B messages/day. 2B / 10^5 s = **20k writes/s average**. With a 3x peak factor, **~60k/s**. So what: a single relational primary will not take this; use a write-optimized store partitioned by conversation (Cassandra/ScyllaDB/DynamoDB) and a log like Kafka in front.

</details>

<details>
<summary>2. Those messages average 200 bytes with 100 bytes of metadata, kept for 2 years with replication factor 3. How much storage?</summary>

2B/day x 300 B = 600 GB/day. x 730 days = ~440 TB. x 3 replicas = **~1.3 PB** (plus index overhead, say 1.5 PB). So what: many nodes and tiered storage; consider moving messages older than 90 days to cheaper storage.

</details>

<details>
<summary>3. A photo app gets 10M uploads/day at 2 MB average and stores 4 resized variants totalling 1 MB. What is daily storage and upload bandwidth?</summary>

10M x 3 MB = **30 TB/day** stored (before replication or erasure coding). Upload: 10M x 2 MB = 20 TB/day / 10^5 s = **200 MB/s average** (~1.6 Gbps), peak 3x ~600 MB/s. So what: uploads go straight to object storage via presigned URLs, not through app servers.

</details>

<details>
<summary>4. Those photos are viewed 100x more than uploaded, served at an average 200 KB. What egress do you need?</summary>

1B views/day x 200 KB = 200 TB/day = **~2.3 GB/s average** (~18 Gbps), peak maybe 7 GB/s. So what: this must come from a CDN with a high hit ratio; origin should see only a few percent.

</details>

<details>
<summary>5. You want to cache 20% of daily reads for a service with 5k read QPS and 2 KB responses. How much memory?</summary>

5k x 10^5 = 500M reads/day. 20% = 100M x 2 KB = **200 GB**, plus ~30% overhead = ~260 GB. So what: a small Redis cluster (for example 4 to 6 shards of 64 GB) with replicas. Check by measuring hit ratio vs size later.

</details>

<details>
<summary>6. A service handles 20k RPS at 50 ms average latency. How many requests are in flight, and how many instances with 200 worker threads each?</summary>

Little's law: 20,000 x 0.05 s = **1,000 concurrent requests**. With 200 threads per instance at, say, 70% target utilization: 1,000 / 140 = ~8 instances, so run **10 to 12** for headroom and AZ failures.

</details>

<details>
<summary>7. A URL shortener creates 200M links/month. How many characters of base62 do you need for 10 years?</summary>

200M x 12 x 10 = 24B links. 62^6 = 56.8B (enough, but tight with growth and scrambling headroom); 62^7 = 3.5T. **Use 7 characters.**

</details>

<details>
<summary>8. 5M drivers send GPS pings every 4 seconds, 100 bytes each. What is the write rate and how much would you keep for 30 days of trip history?</summary>

5M / 4 = **1.25M pings/s**. Per day: 1.25M x 10^5 = 125B pings x 100 B = 12.5 TB/day; 30 days = **375 TB**. So what: latest location lives in memory (Redis/geo index); history is sampled (keep 1 in 4 outside trips) and written in batches to cheap storage.

</details>

<details>
<summary>9. A video platform receives 500 hours of uploads per minute. How much raw storage per day?</summary>

500 h/min x 1,440 min = 720k hours/day. At ~1 GB per hour of 1080p source = **~720 TB/day raw**, plus encoded renditions (~1.5x). So what: cold source tiers, erasure coding, and transcoding capacity planned in GPU/CPU hours.

</details>

<details>
<summary>10. Notifications: 200M users get 5 pushes/day, delivered within 8 waking hours. What send rate do you need, and what is the bottleneck?</summary>

1B pushes / (8 x 3,600 s) = **~35k/s average**, campaigns spiking to 10x. The bottleneck is provider rate limits (APNs/FCM per-app limits) and fanout from campaigns, so you need per-channel queues, pacing and priority separation.

</details>

<details>
<summary>11. A search index has 10B documents with 1 KB of indexable text each. Roughly how big is the inverted index?</summary>

Raw text ~10 TB. A compressed inverted index with positions is typically 30 to 50% of the raw text: **~3 to 5 TB**, times replicas (say 3) = 10 to 15 TB of serving storage, spread across hundreds of shards. So what: document-partitioned shards in memory/SSD with replicas for query throughput.

</details>

<details>
<summary>12. Your API must serve 99.95% availability. How much downtime per month is that, and what does it imply?</summary>

0.05% of 30 days = 0.0005 x 43,200 min = **~21.6 minutes/month**. Implies: multi-AZ redundancy, automated failover, no manual steps in recovery, careful deploys (canaries, fast rollback), and alerting that detects problems within a couple of minutes.

</details>

## Related

- [Back of the Envelope](../00-start-here/02-back-of-envelope.md)
- [Cost Optimization Exercises](04-cost-optimization-exercises.md)
- [Design Question Bank](05-design-question-bank.md)
