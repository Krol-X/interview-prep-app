---
title: "Индексы: B-tree, уникальные, составные (порядок колонок), partial"
hot: true
links:
  - { t: "PostgreSQL docs — Indexes", u: "https://www.postgresql.org/docs/current/indexes.html" }
  - { t: "Use The Index, Luke", u: "https://use-the-index-luke.com/" }
---
**B-tree** — дефолт, для `=`, `<`, `>`, `BETWEEN`, `IN`, `ORDER BY`, `LIKE 'abc%'` (префикс). Не для `LIKE '%abc'`, не для функций над колонкой без функционального индекса.

```sql
CREATE INDEX idx ON withdrawals (wallet_id);
CREATE UNIQUE INDEX ON wallets (user_id);                      -- уникальность = защита от гонок
CREATE INDEX ON withdrawals (wallet_id, created_at DESC);       -- составной
CREATE INDEX ON withdrawals (status) WHERE status = 'pending';  -- partial: маленький, под конкретный запрос
CREATE INDEX ON users (lower(email));                           -- функциональный
```

**Порядок колонок в составном** — leftmost prefix: индекс `(a, b)` работает для `WHERE a=?` и `WHERE a=? AND b=?`, но **не** для `WHERE b=?`. Первой — колонка с `=`, потом диапазон/сортировка. `(wallet_id, created_at)` закроет «выводы кошелька, свежие сверху».

- Индекс ускоряет чтение, замедляет запись и занимает место. Не индексировать всё.
- FK-колонки Rails **не** индексирует автоматически (кроме `references` в миграции — тот ставит).
- Низкая селективность (булев флаг) — обычный индекс бесполезен, partial — полезен.
- Covering: `INCLUDE (amount)` — index-only scan без похода в таблицу.
- Другие типы: GIN (jsonb, массивы, full-text), GiST (геометрия, диапазоны), BRIN (огромные append-only по времени), Hash (только `=`, редко).
- `pg_stat_user_indexes` — неиспользуемые индексы; `REINDEX CONCURRENTLY` при раздувании.

## Фраза для собеса

«B-tree под равенство и диапазоны, в составном первой — колонка с равенством, уникальные — для инвариантов; partial — для статусов».
