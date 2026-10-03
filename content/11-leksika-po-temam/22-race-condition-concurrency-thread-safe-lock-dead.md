---
title: "race condition, concurrency, thread-safe, lock, deadlock, atomic"
hot: false
sub: "3. Баги, отладка, конкурентность"
---
- **race condition** — гонка: *Two requests spent the same UTXO — a classic race condition.*
- **concurrency** — параллелизм (одновременность); **parallelism** — реально одновременно на ядрах.
- **thread-safe** — *Sidekiq workers run in threads, so the code must be thread-safe.*
- **lock / to lock / to acquire a lock / to release** — *acquire a row lock with SELECT FOR UPDATE.*
- **deadlock** — взаимная блокировка; **contention** — конкуренция за ресурс.
- **atomic / atomically** — *the update must be atomic.*
- **mutex, semaphore, critical section**.
- **to serialize access** — выстроить в очередь.

> Since several workers could pick the same UTXOs, I serialized access with a lock so the spend is atomic — otherwise you'd get a double spend rejected by the network.
