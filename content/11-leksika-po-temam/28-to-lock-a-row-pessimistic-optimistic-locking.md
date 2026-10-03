---
title: "to lock a row, pessimistic / optimistic locking"
hot: false
sub: "4. База данных и тесты"
---
- **to lock a row / row-level lock** — *lock the exchange row with SELECT FOR UPDATE.*
- **pessimistic locking** — блокируем заранее: *pessimistic locking with lock! in Rails.*
- **optimistic locking** — проверяем версию при записи: *optimistic locking via a lock_version column; on conflict we retry.*
- **advisory lock** — *a Postgres advisory lock keyed by wallet id.*
- **to hold a lock / to block / to wait on a lock / lock timeout**.
- **contention** — *high contention on that row.*

> For spending UTXOs I'd use pessimistic locking: lock the wallet row, build and broadcast the transaction, commit. Optimistic locking would just make the second request fail, which is also acceptable for a demo.
