---
title: "`find`/`detect`, `any?`/`all?`/`none?`, `count` с блоком"
hot: false
links:
  - { t: "Ruby docs — Enumerable#find", u: "https://docs.ruby-lang.org/en/master/Enumerable.html#method-i-find" }
---
```ruby
list.find { _1.id == 5 }        # первый подходящий или nil (detect — алиас)
list.find_index { ... }         # его индекс

list.any? { _1.failed? }        # есть хоть один
list.all?(&:valid?)             # все
list.none?(&:nil?)              # ни одного
list.one? { ... }               # ровно один

list.count                      # размер
list.count(&:hot?)              # сколько удовлетворяют
list.count("x")                 # сколько равны аргументу
```

Паттерн-аргумент (2.5+): `any?(Integer)`, `all?(/re/)`, `none?(nil)` — через `===`.

Ловушки:
- `[].all?` → `true`, `[].any?` → `false` (вакуумная истина).
- `any?` без блока проверяет истинность элементов: `[nil, false].any?` → `false`.
- `find` останавливается на первом совпадении; `select.first` — пройдёт всё.
- В Rails `User.find { }` — это Enumerable на загруженных записях, а `User.find(id)` — SQL. `where(...).exists?` вместо `any?`, чтобы не грузить все строки.

## Фраза для собеса

«`find` возвращает элемент или nil и останавливается на первом; `any?/all?/none?` — предикаты, помню про пустую коллекцию».
