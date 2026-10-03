---
title: "`each_cons`, `each_slice`, `chunk_while`, `slice_when`"
hot: true
links:
  - { t: "Ruby docs — Enumerable#each_cons", u: "https://docs.ruby-lang.org/en/master/Enumerable.html#method-i-each_cons" }
  - { t: "Ruby docs — Enumerable#chunk_while", u: "https://docs.ruby-lang.org/en/master/Enumerable.html#method-i-chunk_while" }
---
```ruby
[1,2,3,4].each_cons(2).to_a    # [[1,2],[2,3],[3,4]]  — скользящее окно
[1,2,3,4].each_slice(2).to_a   # [[1,2],[3,4]]        — разбиение на куски
```

`each_cons(n)` — для сравнения соседей: разрывы во времени, рост/падение, дубликаты подряд.
`each_slice(n)` — батчи для API, пагинация, `in_groups_of` без Rails.

```ruby
# chunk_while — группировать подряд идущие, пока условие между соседями истинно
[1,2,4,5,7].chunk_while { |a, b| b == a + 1 }.to_a   # [[1,2],[4,5],[7]]

# slice_when — то же, но условие описывает РАЗРЫВ
[1,2,4,5,7].slice_when { |a, b| b != a + 1 }.to_a    # то же самое
```

Пример из тестового: максимальный интервал между выводами —
`times.each_cons(2).map { |a, b| b - a }.max`.

Все четыре без блока возвращают `Enumerator`, можно цеплять `.map`, `.to_a`, `.lazy`.

## Фраза для собеса

«`each_cons` — окно, `each_slice` — батчи, `chunk_while`/`slice_when` — группы подряд идущих по условию между соседями».
