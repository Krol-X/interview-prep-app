---
title: "Rails 7/7.1/7.2/8 — что нового (Hotwire, `normalizes`, `generates_token_for`, Solid Queue)"
hot: false
links:
  - { t: "Rails 7.1 release notes", u: "https://guides.rubyonrails.org/7_1_release_notes.html" }
  - { t: "Rails 7.2 release notes", u: "https://guides.rubyonrails.org/7_2_release_notes.html" }
  - { t: "Rails 8.0 release notes", u: "https://guides.rubyonrails.org/8_0_release_notes.html" }
---
Знать на уровне «что появилось и зачем»:

**7.0** — Hotwire (Turbo + Stimulus) вместо SPA по умолчанию; import maps без Node; `load_async` для параллельных запросов; encrypted attributes (`encrypts :wif`); `ActiveRecord::Base.transaction` + `after_commit` стали надёжнее.

**7.1** — `normalizes :email, with: ->(e) { e.strip.downcase }`; `generates_token_for :password_reset, expires_in: 15.minutes`; `ActiveRecord::Base.with` (CTE); композитные первичные ключи; `config.autoload_lib`; Dockerfile в `rails new`; `authenticate_by` против timing-атак; `Rails.error.report`; async queries.

**7.2** — dev-контейнеры; `enqueue_after_transaction_commit` для ActiveJob; browser version guard (`allow_browser`); Rate limiting в контроллерах (`rate_limit to: 10, within: 1.minute`); `ActiveRecord.after_all_transactions_commit`; Puma threads по умолчанию 3; YJIT включён по умолчанию.

**8.0** — «Solid trifecta»: Solid Queue (джобы в БД, замена Sidekiq для небольших проектов), Solid Cache, Solid Cable; Kamal 2 для деплоя; Propshaft вместо Sprockets; встроенный генератор аутентификации; `params.expect`; SQLite готов к prod.

Если спросят «что нравится из нового» — выбрать одно и обосновать: например, `normalizes` убирает `before_validation`-бойлерплейт, `rate_limit` — зачем Rack::Attack для простых случаев.

## Фраза для собеса

«7.1 — normalizes и token generation, 7.2 — rate limit и enqueue after commit, 8 — Solid Queue/Cache и встроенная аутентификация».
