---
title: "`EXPLAIN ANALYZE` — прочитать Seq Scan vs Index Scan"
hot: true
links:
  - { t: "PostgreSQL docs — Using EXPLAIN", u: "https://www.postgresql.org/docs/current/using-explain.html" }
  - { t: "explain.dalibo.com — визуализатор", u: "https://explain.dalibo.com/" }
---
```sql
EXPLAIN ANALYZE SELECT * FROM withdrawals WHERE wallet_id = 5 ORDER BY created_at DESC LIMIT 20;
```
`EXPLAIN` — план без выполнения (оценки). `ANALYZE` — выполняет и показывает реальное время/строки. `(ANALYZE, BUFFERS)` — ещё и страницы диска/кэша. В Rails: `Withdrawal.where(...).explain(:analyze)`.

Читать **изнутри наружу**, снизу вверх:
```
Limit (actual time=0.05..0.09 rows=20 loops=1)
  -> Index Scan Backward using idx_w_wallet_created on withdrawals
       Index Cond: (wallet_id = 5)
```

| Узел | Что значит |
|---|---|
| **Seq Scan** | читает всю таблицу. Норма для маленьких таблиц или выборки большой доли строк; беда на миллионах |
| **Index Scan** | по индексу → за каждой строкой в таблицу. Хорош при малой выборке |
| **Index Only Scan** | всё из индекса, в таблицу не ходит (covering) |
| **Bitmap Heap Scan** | индекс → битовая карта страниц → таблица; средняя селективность |
| **Nested Loop / Hash Join / Merge Join** | способы join; Nested Loop с большим внутренним Seq Scan — красный флаг |
| **Sort** | сортировка в памяти/на диске (`external merge` — не хватило `work_mem`) |

На что смотреть: расхождение `rows=` оценки и факта (устарела статистика → `ANALYZE table`), Seq Scan там, где ждали индекс (нет индекса / функция над колонкой / тип не совпал / планировщик решил, что дешевле), `loops=` > 1 умножает время, `Filter:` с большим `Rows Removed` — индекс не покрывает условие.

## Фраза для собеса

«Читаю план изнутри, сравниваю оценку и факт строк, ищу Seq Scan и Rows Removed by Filter — это говорит, какого индекса не хватает».
