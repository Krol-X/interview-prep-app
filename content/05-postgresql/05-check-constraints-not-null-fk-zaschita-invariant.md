---
title: "CHECK constraints, NOT NULL, FK — защита инвариантов на уровне БД"
hot: true
links:
  - { t: "PostgreSQL docs — Constraints", u: "https://www.postgresql.org/docs/current/ddl-constraints.html" }
---
Валидации в Rails работают только через Rails: `update_all`, `insert_all`, консоль, другой сервис, гонка — всё обходит. Инварианты, которые **никогда** не должны нарушаться, — в БД.

```ruby
# миграция
t.bigint  :balance_sat, null: false, default: 0
t.string  :status,      null: false
t.references :wallet,   null: false, foreign_key: true
add_check_constraint :wallets, "balance_sat >= 0", name: "balance_non_negative"
add_check_constraint :withdrawals, "amount_sat > 0", name: "amount_positive"
add_check_constraint :withdrawals, "status IN ('pending','processing','sent','failed')", name: "status_valid"
add_index :withdrawals, :txid, unique: true, where: "txid IS NOT NULL"
add_exclusion_constraint ...  # пересечение интервалов (бронирования)
```

- **NOT NULL** — на всё, что обязательно. `nil` в коде — источник половины багов.
- **FK** (`foreign_key: true`) — нет осиротевших строк; `on_delete: :cascade/:nullify/:restrict`.
- **CHECK** — `balance >= 0` поймает любую гонку списания последним рубежом: `ActiveRecord::StatementInvalid` (`PG::CheckViolation`) вместо отрицательного баланса.
- **UNIQUE** — единственная настоящая защита от дублей.
- На живой таблице: `validate: false` / `NOT VALID` → проверить данные → `validate_constraint`, чтобы не держать lock.

Rails ловит нарушения как исключения: `RecordNotUnique`, `InvalidForeignKey`, `StatementInvalid`. Дублируй AR-валидацией для человекочитаемой ошибки, но источник правды — constraint.

## Фраза для собеса

«Валидации — для UX, constraints — для инвариантов: NOT NULL, FK, UNIQUE, CHECK на баланс и статус; они защищают и от гонок, и от чужого кода».
