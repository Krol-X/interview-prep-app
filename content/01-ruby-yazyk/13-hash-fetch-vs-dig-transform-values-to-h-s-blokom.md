---
title: "`Hash`: `fetch` vs `[]`, `dig`, `transform_values`, `to_h` с блоком, default proc"
hot: false
links:
  - { t: "Ruby docs — Hash", u: "https://docs.ruby-lang.org/en/master/Hash.html" }
---
```ruby
h = { a: 1 }
h[:b]                  # nil — тихо
h.fetch(:b)            # KeyError — громко; для обязательных ключей (ENV.fetch("DB_URL"))
h.fetch(:b, 0)         # дефолт
h.fetch(:b) { compute } # ленивый дефолт

deep = { user: { wallet: { balance: 5 } } }
deep.dig(:user, :wallet, :balance)   # 5; nil, если любой уровень отсутствует
deep[:user][:nope][:x]               # NoMethodError на nil

h.transform_values { _1 * 2 }        # новый хеш, те же ключи
h.transform_keys(&:to_s)             # строки ↔ символы
h.filter_map / h.select { |k, v| }   # select на хеше возвращает хеш
h.sum { |k, v| v }
list.to_h { |x| [x.id, x] }          # to_h с блоком — пары
h.each_with_object({}) { |(k, v), acc| ... }   # деструктуризация пары
```

Default proc — ловушка:
```ruby
Hash.new([])      # ОДИН общий массив на все ключи — h[:a] << 1 засоряет всех
Hash.new { |h, k| h[k] = [] }   # правильно
```

Хеши упорядочены (с 1.9) по порядку вставки. Ключи-строки `dup`-аются и замораживаются при вставке.

## Фраза для собеса

«`fetch` для обязательного, `dig` для вложенного без nil-проверок, `transform_values` вместо map+to_h, и помню про общий объект в `Hash.new([])`».
