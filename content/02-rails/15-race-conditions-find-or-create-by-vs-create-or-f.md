---
title: "Race conditions: `find_or_create_by` vs `create_or_find_by` + unique index"
hot: true
links:
  - { t: "Rails API — create_or_find_by", u: "https://api.rubyonrails.org/classes/ActiveRecord/Relation.html#method-i-create_or_find_by" }
---
Check-then-act — два запроса между проверкой и действием успевают оба.

```ruby
Wallet.find_or_create_by(user_id: 1)
# A: SELECT → нет;  B: SELECT → нет;  A: INSERT;  B: INSERT  → два кошелька
```

Защита — только на уровне БД:

1. **Unique index** `add_index :wallets, :user_id, unique: true` — второй INSERT упадёт с `RecordNotUnique`.
2. **`create_or_find_by`** (Rails 6+): INSERT первым, при нарушении уникальности — SELECT. Требует индекса. Минус: сжигает значение sequence, внутри транзакции уронит её (используй savepoint).
3. Или `find_or_create_by` + `rescue ActiveRecord::RecordNotUnique; retry`.
4. `upsert`/`insert_all(..., unique_by:)` — `ON CONFLICT DO UPDATE` одним SQL.

Другие гонки того же вида:
- `if wallet.balance >= x then update` → `with_lock` или условный UPDATE с проверкой rowcount.
- `validates :x, uniqueness: true` → всегда + unique index.
- `counter += 1; save` → `increment!` / `update_counters`.
- «проверил, что джоб не идёт, запустил» → unique job / lock в Redis `SET NX`.
- Два запроса на вывод одних UTXO → очередь с concurrency 1 или lock.

Тест на гонку: два потока с барьером, или просто обосновать индексом.

## Фраза для собеса

«Любое «проверил — сделал» двумя запросами — гонка; лечу unique index + `create_or_find_by`, `with_lock` или атомарным UPDATE».
