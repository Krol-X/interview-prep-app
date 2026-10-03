---
title: "`SELECT ... FOR UPDATE`, `SKIP LOCKED` (очереди в БД), deadlocks"
hot: true
links:
  - { t: "PostgreSQL docs — Explicit Locking (row-level)", u: "https://www.postgresql.org/docs/current/explicit-locking.html#LOCKING-ROWS" }
  - { t: "Rails API — ActiveRecord::Locking::Pessimistic", u: "https://api.rubyonrails.org/classes/ActiveRecord/Locking/Pessimistic.html" }
---
## Пессимистичная блокировка

```sql
BEGIN;
SELECT * FROM wallets WHERE id = 1 FOR UPDATE;   -- строка заблокирована до COMMIT
UPDATE wallets SET balance = balance - 100 WHERE id = 1;
COMMIT;
```

Второй параллельный `FOR UPDATE` на ту же строку **ждёт**. Так решается check-then-act гонка при списании.

В Rails:
```ruby
wallet.with_lock do           # = transaction + reload(lock: true)
  raise Insufficient if wallet.balance < amount
  wallet.update!(balance: wallet.balance - amount)
end
```

## `SKIP LOCKED` — очередь на Postgres

```sql
SELECT * FROM jobs WHERE status = 'pending'
ORDER BY id LIMIT 1 FOR UPDATE SKIP LOCKED;
```

Воркеры не ждут друг друга — берут следующую незанятую строку. На этом построены Solid Queue, good_job, que.

## Deadlock

Транзакция A держит строку 1 и ждёт 2; B держит 2 и ждёт 1. Postgres обнаружит и убьёт одну (`PG::TRDeadlockDetected`).

Профилактика: **блокировать строки в одном и том же порядке** (например, `ORDER BY id`), держать транзакции короткими, не делать внешних вызовов внутри.

## Альтернатива без блокировки

```sql
UPDATE wallets SET balance = balance - 100
WHERE id = 1 AND balance >= 100;
-- проверить rowcount == 1
```
Атомарно, без `SELECT`. Плюс `CHECK (balance >= 0)` как последний рубеж.

## Фраза для собеса

«Для денег — `with_lock` или условный UPDATE с проверкой затронутых строк, плюс CHECK constraint. Для очередей — `FOR UPDATE SKIP LOCKED`».
