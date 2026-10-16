---
title: Serialization and Compression
summary: JSON vs Protocol Buffers vs Avro vs MessagePack vs Thrift, schema evolution rules, and gzip vs Brotli vs zstd vs LZ4 for APIs, storage and streams.
tags: [serialization, protobuf, avro, json, compression, gzip, brotli, zstd]
level: intermediate
time: 15 min
---

# Serialization and Compression

> **TL;DR**
> - JSON is readable but large; Protobuf and Avro are compact binary formats with schemas.
> - Schemas must evolve safely: add optional fields, never reuse field numbers, use a schema registry for events.
> - Compress text over the network (Brotli for static, gzip/zstd for dynamic); LZ4/Snappy where speed matters most.
> - Do not compress already-compressed media.

Every byte you send or store is paid for in latency, bandwidth, CPU and money. Format choice also determines how safely you can **evolve** data over time.

## Serialization formats

| Format | Type | Schema | Size | Speed | Human readable | Typical use |
|---|---|---|---|---|---|---|
| **JSON** | Text | Optional (JSON Schema) | Large | Medium | Yes | Public REST APIs, configs, logs |
| **Protocol Buffers** | Binary | Required (`.proto`), field tags | Small | Fast | No | gRPC, internal RPC, storage |
| **Avro** | Binary | Required (JSON schema), writer schema needed to read | Very small (no field tags) | Fast | No | Kafka + Schema Registry, Hadoop/data lakes |
| **MessagePack** | Binary | None (JSON-like) | Smaller than JSON | Fast | No | Drop-in binary JSON (Redis, game state) |
| **Thrift** | Binary/compact | Required (IDL) | Small | Fast | No | Older RPC stacks (Facebook, Twitter) |
| **CBOR** | Binary | Optional | Small | Fast | No | IoT, WebAuthn |
| **Parquet / ORC** | Columnar binary | Embedded | Tiny with compression | Fast scans | No | Analytics storage |
| **FlatBuffers / Cap'n Proto** | Zero copy binary | Required | Small | Fastest reads (no parse step) | No | Games, mobile, latency critical |

Protobuf vs JSON for the same object is typically 3 to 10x smaller and several times faster to parse.

## Schema evolution

Data lives longer than code. Producers and consumers deploy at different times, so formats must be **backward compatible** (new readers read old data) and **forward compatible** (old readers read new data).

Protobuf rules:

- Never change a field's **tag number** or reuse a deleted tag (mark it `reserved`).
- Adding fields is safe (old readers skip unknown tags).
- Removing fields is safe if the tag is reserved and readers tolerate absence.
- Changing types is mostly unsafe (a few compatible pairs exist, like int32 and int64).

Avro rules:

- Readers resolve using both the **writer's schema** and the **reader's schema**, so new fields need **defaults**.
- A **Schema Registry** (Confluent, Apicurio, AWS Glue) stores schemas by ID; each Kafka message carries the schema ID, and the registry enforces compatibility modes (BACKWARD, FORWARD, FULL).

JSON: no enforcement by default, so rely on discipline: only add optional fields, ignore unknown fields, never repurpose a field.

## Compression

| Algorithm | Ratio | Speed | Where |
|---|---|---|---|
| **gzip / DEFLATE** | Good | Medium | Universal HTTP support, logs |
| **Brotli** | Better than gzip (~15 to 25% smaller for text) | Slow at high levels, fast decompress | Static web assets (precompress at build time), HTTP `br` |
| **zstd** | gzip-like or better ratio, much faster; tunable levels; dictionary support | Fast | Kafka, databases, backups, newer HTTP (`zstd` content encoding) |
| **LZ4 / Snappy** | Lower ratio | Very fast | Real time paths: Kafka, Cassandra, RocksDB blocks, RPC |
| **LZMA / xz** | Very high | Very slow | Archives, distribution packages |

Guidelines:

- Compress text responses over ~1 KB (`Accept-Encoding: br, gzip`). Do not compress already compressed media (JPEG, MP4, ZIP).
- Precompress static assets with Brotli at max level; dynamic responses at a moderate level.
- In Kafka, compress at the producer in batches (zstd or LZ4); bigger batches compress better.
- Columnar storage + compression (Parquet with zstd/Snappy) often gives 5 to 10x reduction for analytics data.
- Beware compression with secrets in HTTPS responses mixed with attacker controlled input (CRIME/BREACH style attacks).

## Interview questions

<details>
<summary>Why do Kafka pipelines often use Avro or Protobuf with a schema registry instead of JSON?</summary>

Smaller messages (cheaper storage, network and faster processing), enforced schemas that stop bad data at the producer, and controlled evolution: the registry checks compatibility before a new schema version is accepted, so producers cannot break consumers by renaming or removing fields.

</details>

<details>
<summary>You need to send 50 KB JSON responses to mobile clients on slow networks. What can you do?</summary>

Enable Brotli or gzip (often 5 to 10x smaller for JSON), trim fields (sparse fieldsets, pagination), avoid deeply repeated structures, consider a binary format (protobuf) for your own apps, cache with ETags so unchanged data returns 304, and batch requests to cut round trips.

</details>

## Related

- [API Design](03-api-design.md)
- [Message Queues](../02-building-blocks/07-message-queues.md)
- [Data Warehousing](../03-data/07-data-warehousing-analytics.md)
