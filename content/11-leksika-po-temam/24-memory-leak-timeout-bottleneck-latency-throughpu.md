---
title: "memory leak, timeout, bottleneck, latency, throughput"
hot: false
sub: "3. Баги, отладка, конкурентность"
---
- **memory leak** — утечка: *a memory leak in a long-running worker.* **memory bloat** — рост памяти без утечки.
- **timeout / to time out** — *the request timed out after 30 seconds.*
- **bottleneck** — узкое место: *the database was the bottleneck.*
- **latency** — задержка (*p95 latency*); **throughput** — пропускная способность (*requests per second*).
- **to scale up / out** — вертикально / горизонтально.
- **to profile / profiler**, **hot path**, **to cache / cache hit / miss**, **to optimize**.
- **under load**, **load testing**, **spike**.

> Under load the bottleneck was N+1 queries; eager loading brought p95 latency from two seconds to three hundred milliseconds and doubled throughput.
