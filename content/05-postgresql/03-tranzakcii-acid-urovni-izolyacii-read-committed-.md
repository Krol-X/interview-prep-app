---
title: "Транзакции: ACID, уровни изоляции (Read Committed по умолчанию, Repeatable Read, Serializable)"
hot: true
links:
  - { t: "PostgreSQL docs — Transaction Isolation", u: "https://www.postgresql.org/docs/current/transaction-iso.html" }
---
**ACID**: Atomicity (всё или ничего), Consistency (constraints соблюдены), Isolation (параллельные транзакции не видят промежуточного), Durability (COMMIT → на диске, WAL).

Уровни изоляции в Postgres (MVCC — читатели не блокируют писателей):

| Уровень | Что видит транзакция | Аномалии |
|---|---|---|
| **Read Committed** (дефолт) | каждый запрос видит данные, закоммиченные к его началу | non-repeatable read, phantom: два SELECT в одной транзакции могут отличаться |
| **Repeatable Read** | снимок на момент первого запроса, всю транзакцию | нет phantom (в PG); при конфликте записи — `serialization failure`, надо повторить |
| **Serializable** | как будто транзакции шли по очереди | ловит все аномалии; больше откатов `40001` → retry-логика обязательна |

`Read Uncommitted` в PG = Read Committed.

Практика:
- Read Committed + явные блокировки (`FOR UPDATE`) или атомарные UPDATE — стандарт для денег. «Прочитал баланс, потом списал» на Read Committed — гонка, уровень изоляции сам по себе её не решает (на RR/Serializable второй упадёт, и его надо повторить).
- `ActiveRecord::Base.transaction(isolation: :serializable)` + `rescue ActiveRecord::SerializationFailure → retry`.
- Долгие транзакции мешают VACUUM и держат блокировки.
- `SELECT` без транзакции — autocommit, каждый запрос сам себе транзакция.

## Фраза для собеса

«По умолчанию Read Committed — каждый запрос видит свежий коммит; для инвариантов денег не полагаюсь на изоляцию, а беру FOR UPDATE или условный UPDATE».
