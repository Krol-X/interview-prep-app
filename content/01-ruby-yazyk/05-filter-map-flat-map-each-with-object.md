---
title: "`filter_map`, `flat_map`, `each_with_object`"
hot: true
links:
  - { t: "Ruby docs — Enumerable#filter_map", u: "https://docs.ruby-lang.org/en/master/Enumerable.html#method-i-filter_map" }
  - { t: "Ruby docs — Enumerable#each_with_object", u: "https://docs.ruby-lang.org/en/master/Enumerable.html#method-i-each_with_object" }
---
```ruby
# filter_map — map + отбросить nil и false. Один проход вместо двух.
txids = withdrawals.filter_map { _1[:txid] }
# == withdrawals.map { _1[:txid] }.compact, но compact не убирает false

# flat_map — map + разворачивание одного уровня
orders.flat_map(&:items)        # [[a,b],[c]] → [a,b,c]

# each_with_object — свернуть в объект-аккумулятор без return из блока
by_id = users.each_with_object({}) { |u, h| h[u.id] = u }
```

`each_with_object(obj)` vs `reduce(obj)`: в `reduce` блок обязан **вернуть** аккумулятор (легко забыть), в `each_with_object` объект передаётся по ссылке и мутируется. Для хешей и массивов — `each_with_object`; для чисел и строк (иммутабельных) — `reduce`.

`flat_map` разворачивает ровно один уровень; `flatten` — все.

## Фраза для собеса

«`filter_map` — когда из map часть результатов надо выкинуть; `flat_map` — когда каждый элемент даёт список; `each_with_object` — когда собираю хеш».
