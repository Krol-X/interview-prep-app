---
title: "`config.eager_load`, autoloading Zeitwerk — одна фраза"
hot: false
links:
  - { t: "Rails Guides — Autoloading and Reloading Constants", u: "https://guides.rubyonrails.org/autoloading_and_reloading_constants.html" }
---
**Zeitwerk** (Rails 6+) — автозагрузчик: имя файла ↔ имя константы. `app/services/create_withdrawal.rb` → `CreateWithdrawal`; `app/models/btc/wallet.rb` → `Btc::Wallet`. Не нужно `require` своих файлов. Любая папка в `app/` — корень неймспейса (`app/services/` не даёт префикс `Services::`).

- Несовпадение имени → `NameError: uninitialized constant` или «expected file to define constant». Проверка: `bin/rails zeitwerk:check`.
- Акронимы: `app/lib/api_client.rb` → `ApiClient`; хочешь `APIClient` — `inflect.acronym "API"`.
- `lib/` не автозагружается по умолчанию; Rails 7.1 — `config.autoload_lib(ignore: %w[tasks])`.

**eager_load**:
- `false` (dev/test): константы грузятся при первом обращении, код перезагружается при изменении файла (Reloader).
- `true` (prod): всё загружается при старте — ошибки видны сразу, нет паузы на первом запросе, copy-on-write память для форков Puma. В CI тоже стоит включить, чтобы ловить ошибки загрузки.

Перезагрузка в dev: `reload!` в консоли; объекты, созданные до перезагрузки, принадлежат старым классам — `===` может удивить.

## Фраза для собеса

«Zeitwerk грузит константы по именам файлов без require; `eager_load` в prod — всё при старте, в dev — лениво с перезагрузкой».
