---
title: "to retry, idempotent, at-least-once delivery, duplicate, double spend"
hot: false
sub: "3. Баги, отладка, конкурентность"
---
- **to retry / a retry / retries** — *Sidekiq retries failed jobs with exponential backoff.*
- **idempotent / idempotency** — повтор не меняет результат: *The job is idempotent, so retries are safe.* (произн. «ай-дем-потент»)
- **at-least-once delivery** — хотя бы один раз (значит, возможны дубли); **exactly-once** — практически недостижимо; **at-most-once**.
- **duplicate / to duplicate / deduplication** — *a unique index prevents duplicates.*
- **double spend** — двойная трата (биткоин): *the network rejects a double spend.*
- **backoff**, **dead letter / dead set**, **poison message**.

> Because delivery is at-least-once, the worker has to be idempotent — I check the status before acting and rely on a unique constraint to reject duplicates.
