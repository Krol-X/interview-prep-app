---
title: "`Enumerable`: `map`, `select`/`filter`, `reject`, `reduce`/`inject`, `sum`"
hot: true
links:
  - { t: "Ruby docs — Enumerable", u: "https://docs.ruby-lang.org/en/master/Enumerable.html" }
---
`Enumerable` — модуль, который даёт ~60 методов любому классу с `each`. `Array`, `Hash`, `Range`, `Set`, `Struct` — все его включают.

| Метод | Возвращает | Пример |
|---|---|---|
| `map` / `collect` | новый массив той же длины | `[1,2].map { _1 * 2 } # [2,4]` |
| `select` / `filter` | элементы, где блок истинен | `(1..6).select(&:even?)` |
| `reject` | где блок ложен | `list.reject(&:nil?)` |
| `reduce` / `inject` | одно значение | `[1,2,3].reduce(:+) # 6` |
| `sum` | сумма (точнее для float) | `prices.sum`, `items.sum(&:price)` |

`reduce(initial) { |acc, x| }` — аккумулятор. `reduce(:+)` — через символ. `sum` предпочтительнее `reduce(:+)`: для float использует суммирование Кахана и быстрее.

`filter` — алиас `select` (2.6+), добавлен ради привычки из JS.

Все они возвращают **новые объекты**; исходную коллекцию не меняют. Варианты с `!` (`select!`, `map!`) есть только у `Array`/`Hash`.

## Фраза для собеса

«Любой класс с `each` и `include Enumerable` получает map/select/reduce бесплатно; `sum` точнее и быстрее `reduce(:+)`».
