---
title: "`dry-initializer` — `option :x`, `param :y` (альтернатива initialize)"
hot: false
links:
  - { t: "dry-initializer", u: "https://dry-rb.org/gems/dry-initializer/" }
---
Убирает бойлерплейт `def initialize(a, b:, c: 1); @a = a; ...; end` + `attr_reader`.

```ruby
class CreateWithdrawal
  extend Dry::Initializer

  param  :user                                # позиционный, обязательный
  option :params                              # keyword, обязательный
  option :fee_sat,   default: -> { 1000 }      # дефолт — proc
  option :node,      default: -> { BitcoinNode.new }, reader: :private
  option :amount,    type: Dry::Types["coercible.integer"]   # приведение/проверка
  option :notify,    optional: true           # nil допустим, без дефолта
end

CreateWithdrawal.new(user, params: p).call
```

- Генерирует `initialize` и ридеры (публичные по умолчанию; `reader: :private` / `false`).
- `default:` всегда proc — вычисляется на каждом вызове (нет общего мутабельного дефолта).
- `type:` — любой dry-type или объект с `call`.
- `as:` — переименовать ивар; `optional: true` vs `default:`.
- В `dry-validation` Contract и `dry-operation` уже встроен (`option :repo`).

Альтернативы: `Data.define` для чистых значений; обычный `initialize` с kwargs для 1–2 аргументов — не тащить гем ради этого.

## Фраза для собеса

«`option`/`param` вместо ручного initialize с дефолтами и типами; удобно для сервисов с инъекцией зависимостей».
