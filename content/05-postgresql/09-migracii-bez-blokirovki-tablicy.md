---
title: "Миграции без блокировки таблицы"
hot: false
links:
  - { t: "strong_migrations — Checks", u: "https://github.com/ankane/strong_migrations#checks" }
  - { t: "PostgreSQL docs — ALTER TABLE (notes on locks)", u: "https://www.postgresql.org/docs/current/sql-altertable.html#SQL-ALTERTABLE-NOTES" }
---
`ALTER TABLE` берёт `ACCESS EXCLUSIVE` lock — на время операции таблица недоступна даже на чтение. Если перед ним стоит долгий `SELECT`, ALTER ждёт, а за ним выстраиваются все запросы → приложение встало.

Безопасно / опасно:

| Операция | Lock | Как безопасно |
|---|---|---|
| `add_column` nullable, с default (PG 11+) | мгновенно | ок |
| `add_column ... null: false` без default | переписывает таблицу | добавить nullable → бэкфилл → CHECK NOT VALID → validate → `change_column_null` |
| `add_index` | блокирует запись | `algorithm: :concurrently` + `disable_ddl_transaction!` |
| `add_foreign_key` | блокирует обе таблицы на валидацию | `validate: false` → `validate_foreign_key` отдельно |
| `add_check_constraint` | скан таблицы | `validate: false` → `validate_check_constraint` |
| `change_column` тип | переписывает | новая колонка → копировать батчами → переключить код → удалить старую |
| `rename_column` | быстро, но ломает работающий код | новая колонка + двойная запись, либо `alias_attribute`/`ignored_columns` в два деплоя |
| `remove_column` | быстро; старый код падает | сначала `self.ignored_columns += [...]`, деплой, потом удалить |
| бэкфилл `update_all` всей таблицы | долгая транзакция, lock на все строки | `in_batches` вне транзакции миграции |

Общее: `lock_timeout` (`SET lock_timeout = '5s'` в миграции) — лучше упасть и повторить, чем положить прод. Gem `strong_migrations` ругается на опасное и подсказывает замену.

## Фраза для собеса

«Любой ALTER ждёт exclusive lock: индексы concurrently, constraints NOT VALID + validate, колонки в несколько деплоев, бэкфилл батчами и lock_timeout».
