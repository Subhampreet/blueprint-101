---
title: "Practice: Database Optimization Challenges"
summary: Ten realistic database performance problems (slow queries, wrong indexes, N+1, deep pagination, lock contention, hot rows, replication lag, bloat, connection storms, scaling writes) with step-by-step solutions.
tags: [practice, database, sql, indexes, query-optimization, performance]
level: intermediate
time: 40 min
---

# Practice: Database Optimization Challenges

> **TL;DR**
> - Always start with evidence: `EXPLAIN ANALYZE`, slow query logs, `pg_stat_statements`, lock and replication views.
> - Most fixes are one of: the right composite index, fewer round trips, keyset pagination, shorter transactions, caching, or moving work off the hot path.
> - Scale writes last (sharding is expensive); exhaust cheaper options first.

Reference notes: [Indexes and Storage Engines](../03-data/02-indexes-storage-engines.md), [SQL, ACID and Transactions](../03-data/01-sql-acid-transactions.md), [Schema Design](../08-lld/05-database-schema-design.md).

## Challenges

<details>
<summary>1. `SELECT * FROM orders WHERE user_id = ? AND status = 'PAID' ORDER BY created_at DESC LIMIT 20` takes 800 ms on a 200M row table. There is an index on `user_id`. Fix it.</summary>

`EXPLAIN ANALYZE` likely shows the user_id index fetching thousands of rows, then filtering status and sorting. Create a composite index matching the query: `(user_id, status, created_at DESC)`. The DB seeks directly to the user and status and reads the first 20 rows already sorted: milliseconds. Optionally `INCLUDE` the selected columns for an index-only scan, and select only needed columns instead of `*`.

</details>

<details>
<summary>2. The orders page makes 1 query for orders and then 1 query per order for its items (N+1). Pages with 100 orders are slow. Fix it.</summary>

Batch: load items for all orders in one query (`WHERE order_id IN (...)` or `= ANY($1)`), then group in memory; or join and aggregate in SQL; in ORMs use eager loading (`select_related`/`prefetch_related`, `JOIN FETCH`); in GraphQL use DataLoader. 101 round trips become 2.

</details>

<details>
<summary>3. An admin list uses `OFFSET 500000 LIMIT 50` and times out. Fix it.</summary>

Offsets force the database to walk and discard 500k rows. Switch to keyset pagination: `WHERE (created_at, id) < (:last_created, :last_id) ORDER BY created_at DESC, id DESC LIMIT 50` with an index on `(created_at, id)`. If users really need page numbers, cap the maximum page or precompute.

</details>

<details>
<summary>4. Checkout errors spike with "deadlock detected" when two orders update the same inventory rows. What do you do?</summary>

Make every transaction lock rows in a consistent order (sort SKUs before updating), keep transactions short (no network calls inside), use atomic conditional updates (`UPDATE ... SET qty = qty - ? WHERE sku = ? AND qty >= ?`) instead of read-then-write, and retry the aborted transaction with backoff. For extreme hot SKUs, move the counter to Redis or pre-allocated stock buckets.

</details>

<details>
<summary>5. A viral post's like counter row receives 5,000 updates per second and everything touching it slows down. Fix it.</summary>

The single row is a hot spot with lock contention. Options: sharded counters (N rows per post, increment a random one, sum on read), buffering increments in Redis and flushing in batches (write-behind), or recording like events in an append-only table and aggregating asynchronously. Show approximate counts in the UI.

</details>

<details>
<summary>6. Users update their profile and then see old data. Reads go to replicas. How do you fix it without sending all reads to the primary?</summary>

Read-your-writes: route the user's reads to the primary for a short window after they write (flag in the session), or pass the write's LSN/GTID and read from a replica that has caught up to it, falling back to the primary. Monitor replica lag and remove lagging replicas from the pool.

</details>

<details>
<summary>7. Postgres performance degrades over weeks; tables are much bigger than their live data. What is happening?</summary>

Bloat from MVCC dead tuples that vacuum is not cleaning, often because of long-running transactions (holding back cleanup), autovacuum settings too lax for high-churn tables, or idle-in-transaction sessions. Find and kill long transactions, tune autovacuum per table (lower scale factors), and use `pg_repack` to reclaim space online.

</details>

<details>
<summary>8. After a deploy that scaled the app from 20 to 200 pods, the database falls over with "too many connections". Why and how to fix?</summary>

Each pod opened its own pool (200 pods x 20 connections = 4,000), far beyond what the DB can handle (Postgres forks a process per connection). Put a pooler (PgBouncer in transaction mode, RDS Proxy) in front, shrink per-pod pools (size them with Little's law), and cap autoscaling or add read replicas.

</details>

<details>
<summary>9. A reporting query scans the whole events table every hour and slows the production database. What do you do?</summary>

Move analytics off the OLTP primary: run it on a replica, or better, stream changes (CDC) into a warehouse/OLAP store and query there. Partition the events table by time so queries prune old partitions, and pre-aggregate with materialized views or rollup tables.

</details>

<details>
<summary>10. Write volume is growing 3x per year and the single primary is at 70% CPU on the largest instance. Walk through your options.</summary>

In order: optimize the top write queries and drop unused indexes; batch writes and move non-critical writes async via a queue; split by function (move a high-volume domain like events or logs to its own store, often a write-optimized one); archive cold data; then shard the remaining hot tables by a key that matches access (tenant or user id) using logical shards (Vitess/Citus) so you can rebalance later.

</details>

## Related

- [Indexes and Storage Engines](../03-data/02-indexes-storage-engines.md)
- [Replication](../03-data/04-replication.md)
- [Sharding](../03-data/05-sharding-partitioning.md)
- [Schema Design](../08-lld/05-database-schema-design.md)
