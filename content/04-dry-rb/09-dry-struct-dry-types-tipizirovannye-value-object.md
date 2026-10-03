---
title: "`dry-struct` + `dry-types`: типизированные value objects, `Types::Strict::String`, `.optional`"
hot: false
links:
  - { t: "dry-struct", u: "https://dry-rb.org/gems/dry-struct/" }
  - { t: "dry-types — Built-in types", u: "https://dry-rb.org/gems/dry-types/1.7/built-in-types/" }
---
```ruby
module Types
  include Dry.Types()
  SatAmount = Integer.constrained(gteq: 0)
  Address   = String.constrained(format: /\A(tb1|2|m|n)/)
  Status    = String.enum("pending", "sent", "failed")
end

class Utxo < Dry::Struct
  attribute :txid,  Types::Strict::String
  attribute :vout,  Types::Strict::Integer
  attribute :value, Types::SatAmount
  attribute? :address, Types::Address.optional      # attribute? — ключ может отсутствовать; .optional — может быть nil
end

u = Utxo.new(txid: "ab..", vout: 0, value: 5000)
u.value                     # 5000
Utxo.new(vout: "0")         # Dry::Struct::Error — Strict не приводит типы
u.new(value: 1)             # копия с изменением (иммутабельно)
u.to_h
```

- `Strict::*` — проверка без приведения; `Coercible::*` — `"5"` → 5; `Params::*` — приведение как из HTTP; `JSON::*`.
- `.optional` = `nil` допустим; `.default(0)`; `.constrained(...)`; `.enum(...)`; `Array.of(Utxo)`; `Hash.schema(...)`.
- `Dry::Struct` — иммутабельный value object с валидацией типов на входе. Сравни с `Data.define` — тот без типов; со `Struct` — тот мутабельный.
- `transform_keys(&:to_sym)` — принимать строковые ключи из JSON.

Где уместно: DTO из внешнего API (ответ mempool), конфиг, доменные значения (Money, Address). Не вместо AR-моделей.

## Фраза для собеса

«`Dry::Struct` — иммутабельный объект с типизированными атрибутами из dry-types; падает на входе, если данные не те, а не где-то глубже».
