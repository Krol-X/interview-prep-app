---
title: "JSONB: когда уместно, индекс GIN"
hot: false
links:
  - { t: "PostgreSQL docs — JSON Types", u: "https://www.postgresql.org/docs/current/datatype-json.html" }
  - { t: "PostgreSQL docs — jsonb indexing", u: "https://www.postgresql.org/docs/current/datatype-json.html#JSON-INDEXING" }
---
`jsonb` — бинарный JSON с индексами и операторами (`json` — просто текст, почти не нужен).

```sql
ALTER TABLE withdrawals ADD COLUMN meta jsonb NOT NULL DEFAULT '{}';
SELECT * FROM withdrawals WHERE meta @> '{"source": "api"}';     -- содержит
SELECT meta->>'ip', meta->'utxos'->0 FROM withdrawals;           -- ->> текст, -> json
CREATE INDEX ON withdrawals USING gin (meta);                    -- для @>, ?, ?| ?&
CREATE INDEX ON withdrawals USING gin (meta jsonb_path_ops);     -- меньше, только @>
CREATE INDEX ON withdrawals ((meta->>'source'));                 -- b-tree на один ключ
```

Rails: `t.jsonb :meta`, атрибут — хеш со строковыми ключами; `where("meta @> ?", { source: "api" }.to_json)`; `store_accessor :meta, :source, :ip` — как обычные атрибуты.

**Уместно**: разнородные метаданные, сырые ответы внешних API (сохранить ответ ноды как есть), настройки с редкими ключами, схема которых меняется чаще миграций, логи событий.

**Не уместно**: то, по чему часто фильтруешь/джойнишь/агрегируешь, что участвует в constraints или FK, что имеет стабильную структуру — это колонки. JSONB не даёт NOT NULL на ключ, типизации, FK; обновление одного ключа переписывает всё значение (TOAST), статистика планировщика по ключам слабая.

Правило: если ключ стал нужен в `WHERE` в трёх местах — вынести в колонку.

## Фраза для собеса

«jsonb для схемы, которая меняется и редко фильтруется, с GIN-индексом под `@>`; всё, что в WHERE и constraints, — колонками».
