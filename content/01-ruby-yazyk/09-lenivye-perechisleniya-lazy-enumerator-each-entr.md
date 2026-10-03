---
title: "Ленивые перечисления: `lazy`, `Enumerator`, `each_entry`, `first(n)` на бесконечном"
hot: false
links:
  - { t: "Ruby docs — Enumerator::Lazy", u: "https://docs.ruby-lang.org/en/master/Enumerator/Lazy.html" }
  - { t: "Ruby docs — Enumerator", u: "https://docs.ruby-lang.org/en/master/Enumerator.html" }
---
Обычные `map`/`select` жадные: каждый создаёт полный промежуточный массив. `lazy` делает цепочку поэлементной.

```ruby
(1..Float::INFINITY).lazy.map { _1 * 2 }.select { _1 % 3 == 0 }.first(3)
# => [6, 12, 18]  — без lazy зависло бы на бесконечном map
```

Когда полезно: бесконечные/очень большие последовательности, чтение файла построчно, пагинация API, когда нужно `first(n)` после фильтров.

`Enumerator` — объект-итератор. Создать:
```ruby
e = Enumerator.new { |y| y << 1; y << 2 }   # y — Yielder
e.next   # 1 — внешняя итерация
[1,2,3].each   # без блока → Enumerator
```

Идиома `return enum_for(:method) unless block_given?` делает свой метод совместимым с цепочками (`my_each.with_index`).

`each_entry` — редкий; для объектов, чей `each` отдаёт несколько значений, собирает их в массив. Знать, что есть.

`lazy` дороже на маленьких коллекциях — накладные расходы на каждый элемент. Применять, когда есть реальная причина.

## Фраза для собеса

«`lazy` превращает цепочку в конвейер по одному элементу — нужен для бесконечных последовательностей и ранней остановки; на малых массивах только замедлит».
