---
title: "Миграции: обратимые, индексы `algorithm: :concurrently`, zero-downtime (добавить колонку → бэкфилл → NOT NULL)"
hot: true
links:
  - { t: "Rails Guides — Active Record Migrations", u: "https://guides.rubyonrails.org/active_record_migrations.html" }
  - { t: "gem strong_migrations — список опасных операций", u: "https://github.com/ankane/strong_migrations" }
---
```ruby
class AddTxidToWithdrawals < ActiveRecord::Migration[7.2]
  disable_ddl_transaction!                        # нужно для concurrently
  def change
    add_column :withdrawals, :txid, :string
    add_index  :withdrawals, :txid, unique: true, algorithm: :concurrently
  end
end
```

- `change` обратим для стандартных операций; `remove_column` без типа и `execute` — нет → `up`/`down` или `reversible do |dir|`.
- `add_index ... algorithm: :concurrently` — без блокировки таблицы на запись (Postgres). Нельзя внутри транзакции → `disable_ddl_transaction!`. Один индекс на миграцию.
- Миграция ≠ данные: бэкфилл — отдельной миграцией или rake-таской батчами (`in_batches`), не в той же транзакции.

Zero-downtime добавить NOT NULL колонку:
1. `add_column` nullable (с `default` в PG 11+ мгновенно);
2. деплой кода, который пишет поле;
3. бэкфилл батчами;
4. `add_check_constraint ... NOT VALID` → `validate_check_constraint` → `change_column_null`.

Опасно без подготовки: `rename_column` (сломает старый код во время деплоя), `change_column` типа (переписывает таблицу), `remove_column` (сначала `ignored_columns`), `add_foreign_key` без `validate: false`.

`schema.rb` vs `structure.sql` — второй, если есть PG-специфика (triggers, enum types). Модели в миграциях не использовать (изменятся) — голый SQL или локальный класс.

## Фраза для собеса

«Индексы — `concurrently` без DDL-транзакции, NOT NULL — через nullable + бэкфилл + constraint; strong_migrations подсказывает опасное».
