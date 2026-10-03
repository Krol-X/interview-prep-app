---
title: "`dry-monads`: `Try` для оборачивания исключений"
hot: false
links:
  - { t: "dry-monads — Try", u: "https://dry-rb.org/gems/dry-monads/1.6/try/" }
---
`Try` — мост между миром исключений (гемы, HTTP, парсинг) и миром Result.

```ruby
include Dry::Monads[:try, :result]

Try { JSON.parse(body) }                        # Value(hash) или Error(JSON::ParserError)
Try[JSON::ParserError, KeyError] { ... }        # ловить только перечисленные; остальные пролетят
  .to_result                                    # → Success / Failure(exception)
  .or { |e| Failure[:bad_json, e.message] }

Try { api.broadcast(hex) }.to_result.fmap { |txid| txid.downcase }
```

- Без списка классов `Try` ловит `StandardError` — не `Exception`.
- `Value`/`Error` — свои обёртки; обычно сразу `.to_result` или `.to_maybe`.
- Полезно на границах: в адаптере к внешнему API, при парсинге ввода, при работе с гемом, который кидает.
- Не стоит оборачивать в `Try` всё подряд — баги (NoMethodError) должны падать и попадать в Sentry, а не превращаться в `Failure`, который кто-то проигнорирует. Перечисляй ожидаемые классы явно.

## Фраза для собеса

«`Try` ловит перечисленные исключения на границе и превращает в Result; баги не оборачиваю — им место в мониторинге».
