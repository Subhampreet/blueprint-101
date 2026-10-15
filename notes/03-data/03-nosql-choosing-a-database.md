---
title: NoSQL Families and Choosing a Database
summary: Key-value, document, wide-column, graph, time-series, search and vector databases, how to model data around access patterns, and a decision framework for picking a store in an interview.
tags: [nosql, dynamodb, cassandra, mongodb, redis, graph, timeseries, vector]
level: core
time: 35 min
---

# NoSQL Families and Choosing a Database

"NoSQL" is a loose label for databases that relax the relational model (fixed schema, joins, multi-row transactions) to gain something specific: horizontal scale, flexible schema, low latency, or a data model that fits the problem better. There is no "NoSQL vs SQL" winner. There is **the right store for an access pattern**.

## The families

### Key-value stores

`get(key) -> value`, `put(key, value)`, sometimes TTL, atomic counters, conditional writes.

- **Examples**: Redis, Memcached (in memory); DynamoDB, Riak, etcd, FoundationDB, RocksDB (persistent).
- **Strengths**: predictable single digit ms (or sub ms) latency at any scale, trivially partitionable by key.
- **Weaknesses**: no queries beyond the key (unless secondary indexes are provided), no joins.
- **Use for**: sessions, caches, shopping carts, feature flags, rate limit counters, user preferences, idempotency keys.

### Document stores

JSON-like documents grouped in collections; query by fields; secondary indexes; documents can nest related data.

- **Examples**: MongoDB, Couchbase, CouchDB, Firestore/Firebase, Amazon DocumentDB.
- **Strengths**: flexible schema, data that is read together is stored together (no joins for the common case), rich queries.
- **Weaknesses**: joins across documents are awkward; large documents that grow forever are a trap; multi-document transactions exist (MongoDB 4+) but cost more.
- **Use for**: product catalogs with varied attributes, content management, user profiles, event payloads.

### Wide-column stores

Rows identified by a **partition key**, with many columns sorted by **clustering keys** within the partition. Think "a distributed sorted map of maps".

- **Examples**: Cassandra, ScyllaDB, HBase, Google Bigtable, (DynamoDB's data model is similar).
- **Strengths**: massive write throughput, linear horizontal scaling, multi-datacenter replication (Cassandra), efficient range reads within a partition.
- **Weaknesses**: queries must match the primary key design; no joins, limited secondary indexes; you **model one table per query**.
- **Use for**: time series, messaging (messages by conversation), activity feeds, IoT, audit logs, anything write heavy with known query patterns.

Cassandra modeling example (chat messages):

```sql
CREATE TABLE messages_by_conversation (
  conversation_id uuid,
  bucket          int,          -- e.g. month number, to bound partition size
  message_id      timeuuid,
  sender_id       uuid,
  body            text,
  PRIMARY KEY ((conversation_id, bucket), message_id)
) WITH CLUSTERING ORDER BY (message_id DESC);
```

Partition key `(conversation_id, bucket)` spreads data and bounds partition size; clustering by `message_id DESC` makes "latest 50 messages" a single sequential read.

### Graph databases

Nodes and edges with properties; queries traverse relationships (Cypher, Gremlin, SPARQL).

- **Examples**: Neo4j, Amazon Neptune, JanusGraph, TigerGraph, Dgraph.
- **Strengths**: multi-hop queries (friends of friends, shortest paths, fraud rings) that would need many self joins in SQL.
- **Weaknesses**: harder to shard, smaller ecosystem, often unnecessary.
- **Use for**: recommendations, fraud detection, knowledge graphs, access control graphs, network topology.

Note: many huge social graphs (Facebook TAO, Twitter FlockDB) are **not** graph databases; they are sharded key-value/SQL stores with adjacency lists, because their queries are mostly one hop ("who do I follow?").

### Time-series databases

Optimized for append-heavy, timestamped data and time range aggregation with downsampling and retention.

- **Examples**: Prometheus (pull based metrics), InfluxDB, TimescaleDB (Postgres extension), VictoriaMetrics, M3, ClickHouse (general OLAP but great at this), Druid, Apache Pinot.
- **Use for**: metrics, monitoring, IoT sensors, financial ticks, analytics events.
- Watch **cardinality** (number of unique label combinations): high cardinality labels (user ID) can explode memory in Prometheus style systems.

### Search engines

Inverted indexes for full text, relevance ranking, faceting. Elasticsearch, OpenSearch, Solr, Typesense, Meilisearch. A derived store, not a source of truth. See [Object Storage and Search](../02-building-blocks/10-object-storage-and-search.md).

### Vector databases

Store embedding vectors and answer **approximate nearest neighbour** (ANN) queries ("the 10 items most similar to this vector") using indexes like **HNSW** or **IVF-PQ**.

- **Examples**: Pinecone, Weaviate, Milvus, Qdrant, Chroma; also pgvector (Postgres), Elasticsearch/OpenSearch kNN, Redis vector search.
- **Use for**: semantic search, RAG (retrieval for LLMs), recommendations, image similarity, dedupe.
- Trade-offs: recall vs latency vs memory; metadata filtering combined with ANN is the hard part; often hybrid search (BM25 + vectors) works best.

### NewSQL / distributed SQL

SQL and ACID transactions with automatic sharding and consensus replication: **Google Spanner, CockroachDB, YugabyteDB, TiDB**. Higher per-write latency (consensus), but you keep relational modeling at scale.

## BASE recap

Many NoSQL stores favour **B**asically **A**vailable, **S**oft state, **E**ventual consistency. Several are tunable: DynamoDB offers strongly consistent reads (at 2x cost) and transactions; Cassandra offers per query consistency levels (`ONE`, `QUORUM`, `LOCAL_QUORUM`, `ALL`); MongoDB offers read/write concerns. See [CAP and Consistency](../01-fundamentals/02-cap-pacelc.md).

## Modeling for NoSQL: access patterns first

Relational modeling starts from entities and normalizes; NoSQL modeling starts from **queries**:

1. List every access pattern with its frequency and latency target ("get last 20 orders for user, 2k/s, p99 20 ms").
2. Choose partition keys that spread load evenly **and** let each query hit one partition.
3. Denormalize: duplicate data into multiple tables/items shaped for each query.
4. Keep partitions bounded (bucket by time if they grow without limit).

DynamoDB single table design example:

| PK | SK | Attributes |
|---|---|---|
| `USER#42` | `PROFILE` | name, email |
| `USER#42` | `ORDER#2024-06-01#9001` | total, status |
| `USER#42` | `ORDER#2024-06-03#9002` | total, status |
| `ORDER#9001` | `ITEM#1` | sku, qty |

"Get user and recent orders" is one `Query(PK = USER#42)`; Global Secondary Indexes (GSIs) add alternate access patterns (by order status, by email).

## Decision framework

Ask these in order:

1. **Do I need multi-entity transactions and strong integrity?** Relational (or distributed SQL at large scale).
2. **What is the read/write ratio and scale?** Huge write ingest with simple key access: wide column. Mostly key lookups at huge scale with low latency: key value (DynamoDB).
3. **What do queries look like?** Ad hoc and joins: SQL. Known, few patterns: NoSQL modeled per query. Text relevance: search engine. Similarity: vector DB. Multi hop relationships: graph DB. Time range aggregates: time series / OLAP.
4. **Consistency needs?** Invariants need strong consistency; feeds and counters do not.
5. **Operational reality**: managed service available? Team expertise? Cost at expected scale?

| Use case | Good default | Why |
|---|---|---|
| Users, orders, payments, inventory | PostgreSQL / MySQL | Transactions, constraints, joins |
| Session store, cache, leaderboard | Redis | In memory, data structures, TTL |
| Shopping cart at Amazon scale | DynamoDB | Key access, high availability |
| Chat messages, activity feed storage | Cassandra / ScyllaDB / DynamoDB | Write heavy, partition by conversation/user |
| Product catalog with varied attributes | MongoDB or Postgres JSONB | Flexible schema |
| Full text product search | Elasticsearch / OpenSearch | Relevance, facets |
| Metrics and monitoring | Prometheus + long term TSDB, or ClickHouse | Time series compression and aggregation |
| Social graph (1 hop) | Sharded MySQL / KV adjacency lists | Simple, scalable |
| Fraud rings, recommendations (multi hop) | Neo4j / Neptune | Traversals |
| Semantic search, RAG | pgvector at small scale, dedicated vector DB at large | ANN indexes |
| Files, images, video | Object storage (S3) + metadata DB | Cheap, durable |
| Analytics over billions of rows | Snowflake / BigQuery / ClickHouse | Columnar OLAP |

**Polyglot persistence** (several stores, each for what it does best) is normal in large systems; just be honest that each extra store adds operational cost and a consistency problem between stores (solved with CDC/events).

## Interview questions

<details>
<summary>Why not just use MongoDB for everything since it is "web scale"?</summary>

Document stores shine when data accessed together is stored together and when schemas vary. They are weaker for highly relational data with many cross entity queries and invariants (payments, inventory across items), where you would reimplement joins and transactions in application code. Choose by access pattern and consistency need, not by popularity.

</details>

<details>
<summary>How do you pick a partition key in Cassandra or DynamoDB?</summary>

It must (1) have high cardinality and roughly uniform traffic so load spreads across nodes, (2) let your main queries be answered by reading one partition, and (3) keep each partition bounded in size (add a time bucket if needed). Avoid keys like `country` or `date` alone (hot partitions) and avoid patterns where all new writes go to one key (current hour).

</details>

<details>
<summary>When would you choose a wide-column store over a relational DB for chat messages?</summary>

When write volume and data size exceed what a single primary (even sharded manually) handles comfortably, access is almost always "recent messages in conversation X" (a perfect partition + clustering key fit), and you value multi-region availability over joins and ad hoc queries. Discord famously moved messages from MongoDB to Cassandra and later to ScyllaDB for this reason.

</details>

## Related

- [Indexes and Storage Engines](02-indexes-storage-engines.md)
- [Replication](04-replication.md)
- [Sharding and Partitioning](05-sharding-partitioning.md)
- [ML System Design (vector search)](../10-advanced/05-ml-system-design.md)
