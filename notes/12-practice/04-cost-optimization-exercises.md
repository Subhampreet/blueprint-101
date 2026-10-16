---
title: "Practice: Cost Optimization Exercises"
summary: Eight cost scenarios with worked reasoning (egress-heavy media, idle dev environments, over-provisioned databases, NAT charges, log volume, GPU inference, analytics scans, reserved vs spot) to practise estimating and cutting cloud bills.
tags: [practice, cost, finops, cloud]
level: intermediate
time: 30 min
---

# Practice: Cost Optimization Exercises

> **TL;DR**
> - Find the biggest line item first; optimizing a 2% cost is wasted effort.
> - Typical big wins: CDN hit ratio and media formats, right-sizing, commitments for the baseline, spot for batch, lifecycle rules, and turning off idle things.
> - Every saving has a trade-off (risk, latency, engineering time). Say it.

Prices are illustrative round numbers. Reference: [Cost Estimation and Optimization](../06-reliability-ops/05-cost-optimization.md).

## Exercises

<details>
<summary>1. A video startup's bill is 70% internet egress from object storage (no CDN). What do you do?</summary>

Put a CDN in front (often 50 to 80% cheaper per GB at volume, plus most traffic stops hitting origin), raise cache hit ratio with long TTLs and versioned URLs, use origin shielding, encode with more efficient codecs (AV1/HEVC for capable devices), serve adaptive bitrates so phones do not download 4K, and negotiate committed CDN pricing.

</details>

<details>
<summary>2. Dev and staging environments cost as much as production and run 24/7. Ideas?</summary>

Schedule them off outside working hours (about 70% of hours saved), scale to zero where possible (serverless, Cloud Run), use smaller instance types and single-AZ, share one staging cluster with namespaces, run on spot, and use ephemeral preview environments created per pull request and destroyed on merge.

</details>

<details>
<summary>3. Your primary database runs on a 64 vCPU instance at 12% average CPU and 30% peak. What should you consider?</summary>

Right-size to half (32 vCPU) after checking memory, IOPS and connection needs; buffer-pool fit matters more than CPU. Offload reads to a replica or cache if peak is read-driven, and buy a reserved instance or savings plan for the steady size. Keep headroom for failover and growth; test the smaller size under a load test.

</details>

<details>
<summary>4. NAT gateway charges are $40k/month. Most traffic is from pods to S3 and DynamoDB. Fix?</summary>

Add VPC gateway endpoints for S3 and DynamoDB (free for gateway endpoints) so that traffic bypasses the NAT entirely; add interface endpoints for other high-volume AWS services if their cost is lower than NAT processing; and cache or compress the remaining external calls.

</details>

<details>
<summary>5. Observability costs grew to 25% of infrastructure spend. What do you cut first?</summary>

Drop or sample high-volume, low-value logs (debug, health checks, successful request logs), reduce metric cardinality (remove user/request ids from labels), use tail-based trace sampling (keep errors and slow traces), shorten hot retention and archive to object storage, and set per-team budgets.

</details>

<details>
<summary>6. GPU inference for a recommendation model costs too much at 2,000 requests/s. Options?</summary>

Batch requests dynamically on the GPU, quantize or distill the model, cache scores for popular items and repeat users, run a cheaper first-stage model so the heavy one scores fewer candidates, autoscale with demand, use spot GPUs for non-latency-critical batch scoring, and check whether a CPU model with good features is nearly as accurate.

</details>

<details>
<summary>7. A BigQuery-style warehouse bill spiked because dashboards scan a 50 TB table every 5 minutes. Fix?</summary>

Partition the table by date and cluster by common filter columns so queries scan only recent partitions, build pre-aggregated rollup tables or materialized views for the dashboards, cache dashboard results, reduce refresh frequency, and set per-query byte limits or reservations.

</details>

<details>
<summary>8. Your web fleet runs 100 on-demand instances; traffic varies from 40 to 100 instances' worth daily. How should you buy capacity?</summary>

Commit (reserved/savings plan) to about 40 instances, the steady minimum. Cover the variable 40 to 100 with autoscaling on demand plus a slice of spot instances (diversified types, graceful interruption handling) for stateless capacity. Revisit commitment coverage monthly as the baseline grows.

</details>

## Related

- [Cost Estimation and Optimization](../06-reliability-ops/05-cost-optimization.md)
- [Estimation Problems](01-estimation-problems.md)
- [CDN](../02-building-blocks/04-cdn.md)
