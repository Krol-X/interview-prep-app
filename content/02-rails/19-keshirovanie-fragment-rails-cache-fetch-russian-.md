---
title: "Кэширование: fragment, `Rails.cache.fetch`, russian doll, cache keys"
hot: false
links:
  - { t: "Rails Guides — Caching with Rails", u: "https://guides.rubyonrails.org/caching_with_rails.html" }
---
```ruby
Rails.cache.fetch(["rate", :usdt_btc], expires_in: 30.seconds) do
  RateApi.fetch     # выполнится только при промахе
end
Rails.cache.write/read/delete/exist?
Rails.cache.fetch(key, race_condition_ttl: 5.seconds)   # защита от thundering herd
```

Стора: `:memory_store` (dev, не делится между процессами), `:redis_cache_store` (prod), `:solid_cache_store` (Rails 8, в БД), `:null_store` (test).

**Ключи**: модель отвечает `cache_key_with_version` → `"withdrawals/5-20240101120000"` — `updated_at` внутри ключа = инвалидация через `touch`. Массив `["v2", user, page]` соберётся сам.

**Fragment caching** во view: `<% cache withdrawal do %> ... <% end %>`. **Russian doll** — вложенные фрагменты: внешний ключ зависит от `updated_at` родителя, дочерние `touch: true` на `belongs_to` поднимают изменение наверх. Меняется один ребёнок — перерисовывается только он и родительская обёртка.

- `collection: true` в `render partial:` + кэш → multi-get.
- HTTP-кэш: `fresh_when(withdrawal)` / `stale?` → 304 по ETag/Last-Modified.
- Low-level: мемоизация `@x ||=` (на один объект/запрос), `RequestStore`/`ActiveSupport::CurrentAttributes` (на запрос).
- Инвалидация — главная боль: ключ со временем/версией лучше явных `delete`.

## Фраза для собеса

«`Rails.cache.fetch` с ключом, в который входит версия/updated_at; во view — фрагменты по `cache_key_with_version` и `touch: true` вверх».
