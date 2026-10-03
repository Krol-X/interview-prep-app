---
title: "query, N+1 problem, eager loading, to join, transaction, rollback, isolation level"
hot: false
sub: "4. База данных и тесты"
---
- **query** — запрос: *a slow query*; **to query** — *we query the UTXO set.*
- **N+1 problem** («эн-плюс-уан») — *a classic N+1 in the index action.*
- **eager loading** — *I fixed it with eager loading — includes.* **lazy loading** — противоположность.
- **to join / a join** — *join the users table.*
- **transaction** — *wrap it in a transaction*; **to commit / to roll back / rollback**.
- **isolation level** — *read committed is the default in Postgres.*
- **to explain a query / query plan** — *I looked at the query plan with EXPLAIN ANALYZE.*
- **sequential scan vs index scan**.

> The query plan showed a sequential scan; after adding an index it switched to an index scan, and the N+1 went away with includes.
