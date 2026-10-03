---
title: "`==` vs `eql?` vs `equal?`, `hash` для ключей"
hot: true
links:
  - { t: "Ruby docs — Object#== / eql? / equal?", u: "https://docs.ruby-lang.org/en/master/Object.html#method-i-eql-3F" }
---
| Метод | Смысл | Кто переопределяет |
|---|---|---|
| `equal?` | тот же объект (identity) | никогда |
| `==` | равенство по значению | да, свои классы |
| `eql?` | строгое равенство без приведения типов; используется Hash | вместе с `hash` |
| `===` | «подходит под» — для `case/when` | Range, Regexp, Class, Proc |

```ruby
1 == 1.0     # true
1.eql? 1.0   # false  — поэтому h[1] и h[1.0] разные ключи
"a".equal?("a")  # false — два объекта
```

Свой класс как ключ хеша или в `Set`/`uniq` — нужны **оба**:

```ruby
class Money
  def ==(o) = o.is_a?(Money) && cents == o.cents && currency == o.currency
  alias eql? ==
  def hash = [cents, currency].hash     # равные объекты → равный hash
end
```

Без `hash` два равных `Money` попадут в разные бакеты, и `uniq` их не схлопнет. `Struct`/`Data` делают это автоматически.

`===` в `case`: `when Integer` → `Integer === x` → `is_a?`; `when 1..5` → `include?`; `when /re/` → `match?`; `when ->(x) { x > 0 }` → `call`.

## Фраза для собеса

«`==` — значение, `equal?` — идентичность, `eql?`+`hash` — для ключей хеша; переопределяю `==`, алиасю `eql?` и считаю `hash` по тем же полям».
