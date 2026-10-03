---
title: "`Struct`, `Data` (3.2), `OpenStruct` — когда что"
hot: true
links:
  - { t: "Ruby docs — Data", u: "https://docs.ruby-lang.org/en/master/Data.html" }
  - { t: "Ruby docs — Struct", u: "https://docs.ruby-lang.org/en/master/Struct.html" }
---
```ruby
Point = Struct.new(:x, :y, keyword_init: true)
p = Point.new(x: 1, y: 2); p.x = 5          # мутабельный, есть сеттеры, ==, to_a, to_h

Coord = Data.define(:lat, :lng)             # Ruby 3.2
c = Coord.new(lat: 1, lng: 2)               # иммутабельный: нет сеттеров, frozen
c.with(lat: 3)                              # копия с изменением
# Data требует все аргументы — забыл один → ArgumentError

require "ostruct"
o = OpenStruct.new(a: 1); o.b = 2           # произвольные поля через method_missing
```

Когда что:
- **`Data`** — value object: деньги, координаты, DTO из API. По умолчанию для новых классов-значений.
- **`Struct`** — когда нужна мутабельность или позиционные аргументы; быстрее Data на создание, но позволяет случайно изменить.
- **`OpenStruct`** — почти никогда в продакшене: медленный (method_missing + define на каждом объекте), ломает `respond_to?`, с 3.5 вынесен из stdlib в gem. Для прототипов и тестов.

Оба поддерживают pattern matching: `case c in {lat:, lng:}`.

## Фраза для собеса

«Для неизменяемых значений — `Data`, для мутабельных записей — `Struct`, `OpenStruct` — только в скриптах».
