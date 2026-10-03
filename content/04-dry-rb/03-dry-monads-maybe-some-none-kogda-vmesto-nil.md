---
title: "`dry-monads`: `Maybe` — `Some`/`None`, когда вместо `nil`"
hot: false
links:
  - { t: "dry-monads — Maybe", u: "https://dry-rb.org/gems/dry-monads/1.6/maybe/" }
---
```ruby
include Dry::Monads[:maybe]

Maybe(user)                      # Some(user) или None() если nil
Maybe(user).fmap(&:wallet).fmap(&:address).value_or("—")
# вместо user&.wallet&.address || "—"

Some(5).bind { |x| x > 3 ? Some(x) : None() }
None().value_or { compute_default }
Maybe(h[:a]).to_result(:missing_a)       # Maybe → Result с указанием ошибки
```

Чем отличается от `&.`: цепочка с `&.` работает, но результат — всё тот же `nil` без информации; `Maybe` — явный тип «может отсутствовать», который нельзя случайно передать дальше как значение, и который конвертируется в `Result` с кодом ошибки.

Когда: возвращаемое значение функции, где отсутствие — нормальный исход (`find_rate(pair) → Maybe`), и когда эту «пустоту» дальше надо обрабатывать разными способами. Когда нет: `&.` достаточно; внутри простого метода; в AR-коде (`find_by` возвращает nil, и все к этому привыкли).

`Some(nil)` — невозможно (станет None). `Maybe(false)` — `Some(false)`: `Maybe` только про nil.

## Фраза для собеса

«`Maybe` — типизированный «может быть nil» с цепочкой `fmap` и переводом в `Result`; использую на границах, а не вместо каждого `&.`».
