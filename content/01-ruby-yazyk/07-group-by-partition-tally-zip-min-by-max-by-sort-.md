---
title: "`group_by`, `partition`, `tally`, `zip`, `min_by`/`max_by`, `sort_by`"
hot: true
links:
  - { t: "Ruby docs — Enumerable#tally", u: "https://docs.ruby-lang.org/en/master/Enumerable.html#method-i-tally" }
  - { t: "Ruby docs — Enumerable#partition", u: "https://docs.ruby-lang.org/en/master/Enumerable.html#method-i-partition" }
---
```ruby
list.group_by(&:status)        # { "sent" => [...], "failed" => [...] }
list.partition { _1.big? }     # [[big...], [small...]]  — ровно две группы
list.map(&:status).tally       # { "sent" => 10, "failed" => 2 }  (2.7+)
list.tally_by(&:status)        # то же короче (3.1+)

[1,2].zip([:a,:b])             # [[1,:a],[2,:b]]
keys.zip(values).to_h          # быстрый способ собрать хеш

list.max_by(&:fee)             # элемент с максимальным fee (не само значение)
list.min_by(2, &:fee)          # два минимальных
list.sort_by { [-_1.priority, _1.created_at] }   # многоключевая сортировка
```

`sort_by` вычисляет ключ один раз на элемент (Schwartzian transform) — быстрее `sort { |a,b| ... }` при дорогом ключе. Для обратного порядка по числу — минус; по строкам — `.reverse` или `sort_by { ... }.reverse`.

`partition` vs `group_by`: когда групп ровно две и важны обе — `partition` (деструктуризация `big, small = ...`).

## Фраза для собеса

«`tally` считает частоты, `group_by` раскладывает по ключу, `partition` делит на два, `max_by` возвращает элемент, а не значение».
