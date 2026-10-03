---
title: "Keyword args vs options hash, `**opts`, `...` forwarding"
hot: false
links:
  - { t: "Ruby docs — Methods: Keyword Arguments", u: "https://docs.ruby-lang.org/en/master/syntax/methods_rdoc.html#label-Keyword+Arguments" }
  - { t: "Ruby 3.0 — Separation of positional and keyword arguments", u: "https://www.ruby-lang.org/en/news/2019/12/12/separation-of-positional-and-keyword-arguments-in-ruby-3-0/" }
---
```ruby
# старый стиль
def send(to, opts = {}); fee = opts[:fee] || 1000; end     # опечатка в ключе — тишина

# keyword args
def send(to, amount:, fee: 1000, **rest)   # amount обязателен; fee с дефолтом; rest — остальное
send("tb1q...", amount: 5_000)
send("tb1q...", amout: 5_000)              # ArgumentError: unknown keyword — ловится сразу
```

Плюсы kwargs: самодокументируемые вызовы, проверка имён, порядок не важен, дефолты видны в сигнатуре.

Ruby 3: позиционные и keyword разделены. `h = {a: 1}; m(h)` — это позиционный хеш, не kwargs; нужно `m(**h)`. Это сломало много гемов при переходе с 2.7.

Делегирование:
```ruby
def wrapper(*args, **kwargs, &blk) = target(*args, **kwargs, &blk)
def wrapper(...) = target(...)       # 2.7+: всё как есть
def wrapper(*, **, &) = target(*, **, &)   # 3.2: анонимные
```

Shorthand (3.1): `Point.new(x:, y:)` = `Point.new(x: x, y: y)`.

## Фраза для собеса

«Keyword-аргументы вместо options hash: явные, с проверкой имён и дефолтами; для делегирования — `...`».
