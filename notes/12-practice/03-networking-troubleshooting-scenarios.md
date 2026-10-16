---
title: "Practice: Networking Troubleshooting Scenarios"
summary: Ten production networking incidents (DNS, TLS, timeouts, MTU, load balancer health checks, NAT exhaustion, cross-region latency, WebSocket drops, packet loss, CORS) with a diagnosis path and fix for each.
tags: [practice, networking, troubleshooting, dns, tls, latency]
level: intermediate
time: 40 min
---

# Practice: Networking Troubleshooting Scenarios

> **TL;DR**
> - Walk the layers: DNS, TCP connect, TLS, server time, transfer, client.
> - Ask "what changed?" first (deploys, certificates, DNS, config, traffic).
> - Prove the hypothesis with a tool (`dig`, `nc`, `openssl s_client`, `curl -w`, `mtr`, `tcpdump`) before fixing.

Reference: [Network Troubleshooting](../04-networking-apis/09-network-troubleshooting.md).

## Scenarios

<details>
<summary>1. After migrating to a new load balancer, half your users still hit the old one for hours. Why?</summary>

DNS caching. The old record had a long TTL (say 24 hours), so resolvers and clients keep the old IP until it expires; some clients ignore TTLs entirely. Fix: lower TTL to 60 s a day before migrations, keep the old endpoint working (or proxying) during the transition, then raise the TTL again. Check with `dig` against several public resolvers.

</details>

<details>
<summary>2. At midnight UTC every API call from mobile apps starts failing with TLS errors; browsers are fine. What happened?</summary>

Likely a certificate issue: the certificate expired or was rotated to a chain missing an intermediate (browsers can fetch missing intermediates, many mobile HTTP stacks cannot), or the app pins an old certificate/key. Check with `openssl s_client -showcerts`, fix the chain, automate renewal with monitoring on expiry, and pin to a CA or backup keys rather than one leaf.

</details>

<details>
<summary>3. Requests between two services intermittently take exactly 3 or 9 seconds longer than usual. What does that pattern suggest?</summary>

Retransmission timeouts: a dropped SYN is retried after ~1 s, then 2 s (exponential), giving characteristic 1, 3, 7 second delays (or a resolver timeout of a few seconds for DNS). Look for SYN drops (full accept queue, conntrack table full, overloaded NAT or firewall) with `ss`, `netstat -s` and packet captures. Also check DNS resolution time in `curl -w`.

</details>

<details>
<summary>4. Small requests through the site-to-site VPN work; file uploads hang forever. Why?</summary>

Path MTU black hole: the tunnel reduces the usable MTU, large packets need fragmentation, and blocked ICMP "fragmentation needed" messages mean the sender never shrinks them. Fix with TCP MSS clamping on the tunnel or allowing ICMP type 3 code 4. Confirm with `ping -M do -s 1472` style tests.

</details>

<details>
<summary>5. During a deploy, the load balancer marks all instances unhealthy and returns 503s, even though they are serving fine. Why?</summary>

The health check is wrong for the new version: a changed path or port, a dependency check that fails during startup (DB migrations, cache warmup), timeouts shorter than startup time, or readiness and liveness mixed up. Fix the health endpoint (shallow liveness, readiness that tolerates non-critical dependencies), add startup probes and slow-start, and enable fail-open/panic thresholds.

</details>

<details>
<summary>6. Services in private subnets start failing to call a third-party API at peak with connection errors. Nothing changed in code. What do you check?</summary>

NAT gateway limits: a NAT has a cap on simultaneous connections to the same destination IP and port, and port allocation errors appear under bursts without connection reuse. Check NAT metrics (port allocation errors), add keep-alive and pooling, spread across multiple NAT gateways/IPs, and use private endpoints for cloud services.

</details>

<details>
<summary>7. The app in Europe is slow because it calls a database in us-east for every request. Quick wins?</summary>

Each call pays ~80 to 100 ms RTT. Cut round trips (batch queries, avoid N+1), cache read-mostly data in-region, add a read replica in the EU region for reads, make writes async where possible, and long term deploy the app and its data together per region (or route EU users to a region that owns their data).

</details>

<details>
<summary>8. WebSocket connections drop after exactly 60 seconds of inactivity. Why?</summary>

An intermediary idle timeout (load balancer idle timeout often defaults to 60 s; NATs and proxies have their own). Send ping/pong heartbeats more frequently than the shortest idle timeout (for example every 25 to 30 s), or raise the LB idle timeout, and make clients reconnect with backoff.

</details>

<details>
<summary>9. Throughput between two data centers is 50 Mbps on a 1 Gbps link with 80 ms RTT. Why, and how do you fix it?</summary>

Window-limited TCP: throughput is at most window / RTT. 50 Mbps x 80 ms is about 500 KB in flight, suggesting small socket buffers or no window scaling. Increase buffers to the bandwidth-delay product (1 Gbps x 80 ms = 10 MB), confirm window scaling, use parallel streams, and consider BBR if there is random loss. Verify with `iperf3` and `ss -ti`.

</details>

<details>
<summary>10. The browser console shows "blocked by CORS policy" for API calls, but curl works. What is wrong?</summary>

CORS is enforced only by browsers. The API response lacks the right `Access-Control-Allow-Origin` for the page's origin, or the preflight `OPTIONS` request is not handled (often blocked by auth middleware or the API gateway), or credentials are sent with a wildcard origin. Fix the CORS config for the specific origins, methods and headers, and allow unauthenticated preflights.

</details>

## Related

- [Network Troubleshooting](../04-networking-apis/09-network-troubleshooting.md)
- [Protocol Deep Dives](../04-networking-apis/08-protocol-deep-dives.md)
- [DNS](../02-building-blocks/01-dns.md)
- [HTTP and TLS](../04-networking-apis/02-http-tls.md)
