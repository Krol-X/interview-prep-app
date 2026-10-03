---
title: "Advisory locks — одна фраза"
hot: false
links:
  - { t: "PostgreSQL docs — Advisory Locks", u: "https://www.postgresql.org/docs/current/explicit-locking.html#ADVISORY-LOCKS" }
  - { t: "gem with_advisory_lock", u: "https://github.com/ClosureTree/with_advisory_lock" }
---
Блокировка **по произвольному числу/ключу**, не привязанная к строке. Приложение само договаривается, что значит ключ.

```sql
SELECT pg_advisory_lock(12345);          -- сессионная, ждёт; снять pg_advisory_unlock
SELECT pg_try_advisory_lock(12345);      -- не ждать, вернуть true/false
SELECT pg_advisory_xact_lock(12345);     -- транзакционная — снимется на COMMIT/ROLLBACK (безопаснее)
```

```ruby
Wallet.with_advisory_lock("sweep-utxos") { sweep! }     # gem; ключ хешируется в число
ActiveRecord::Base.connection.execute("SELECT pg_advisory_xact_lock(#{wallet.id})")
```

Когда: «только один процесс выполняет X» без строки, которую можно `FOR UPDATE` — cron-задача на нескольких серверах, пересчёт отчёта, миграция данных, единственный кошелёк-обменник, где все UTXO общие (твоё второе задание!). Замена Redis-lock, когда Redis нет или нужна транзакционность.

Нюансы: сессионный lock переживает транзакцию и теряется при обрыве соединения (хорошо); с PgBouncer в transaction-mode сессионные ломаются — брать `xact`. Ключ — bigint или пара int.

## Фраза для собеса

«Advisory lock — мьютекс в Postgres по числовому ключу; `xact`-вариант снимается с транзакцией, удобен для «один обработчик на ресурс без строки»».
