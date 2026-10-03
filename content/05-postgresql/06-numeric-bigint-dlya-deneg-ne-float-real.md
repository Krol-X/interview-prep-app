---
title: "`numeric`/`bigint` для денег, не `float`/`real`"
hot: true
links:
  - { t: "PostgreSQL docs — Numeric Types", u: "https://www.postgresql.org/docs/current/datatype-numeric.html" }
---
```sql
SELECT 0.1::float8 + 0.2::float8;        -- 0.30000000000000004
SELECT 0.1::numeric + 0.2::numeric;      -- 0.3
```

| Тип | Что это | Для денег |
|---|---|---|
| `real` / `float4`, `double precision` / `float8` | двоичная плавающая точка | **нет** — ошибки округления, `SUM` плывёт |
| `numeric(p, s)` / `decimal` | точная десятичная, произвольная точность | да: `numeric(16, 8)` для BTC, `numeric(12, 2)` для фиата |
| `bigint` | 64-бит целое | да: сатоши, центы. Самый быстрый и простой; так хранит сам Bitcoin |
| `integer` | 32-бит, до ~2.1 млрд | мало: 21 BTC в сатоши уже не влезет |
| `money` | legacy, зависит от locale | нет |

Выбор:
- Одна валюта с фиксированной дробностью (BTC → сат, USD → центы) — **bigint**. Арифметика целая, индексы компактны, нет вопросов округления. В Rails — `t.bigint :amount_sat`, в Ruby — Integer.
- Нужны дробные доли, разные валюты, проценты, курс — **numeric**. В Ruby приходит `BigDecimal`.
- `numeric` медленнее bigint и толще, но для OLTP это незаметно.

Курс USDT/BTC — `numeric(20, 10)`; комиссия 3% — считать в numeric/BigDecimal и округлять явно (`round(8, :down)`) в момент фиксации, а не хранить float.

## Фраза для собеса

«Деньги — bigint в минимальных единицах или numeric; float только в аналитике. В тестовом — сатоши целым числом».
