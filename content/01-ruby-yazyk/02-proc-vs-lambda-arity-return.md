---
title: "`Proc` vs `lambda`: arity, `return`"
hot: true
links:
  - { t: "Ruby docs — Proc (раздел Lambda and non-lambda semantics)", u: "https://docs.ruby-lang.org/en/master/Proc.html#class-Proc-label-Lambda+and+non-lambda+semantics" }
  - { t: "Ruby Guides — Procs & Lambdas", u: "https://www.rubyguides.com/2016/02/ruby-procs-and-lambdas/" }
---
Оба — объекты класса `Proc`. Отличий ровно два.

## 1. Строгость к аргументам (arity)

```ruby
l = ->(a, b) { [a, b] }
l.call(1)          # ArgumentError
p = proc { |a, b| [a, b] }
p.call(1)          # [1, nil]  — недостающие nil, лишние отбрасываются
```

Lambda ведёт себя как метод. Proc — как блок: мягко распаковывает аргументы (поэтому `each { |k, v| }` работает с парами).

## 2. Поведение `return`

```ruby
def with_lambda
  l = -> { return 1 }
  l.call
  2            # вернёт 2 — return вышел только из лямбды
end

def with_proc
  p = proc { return 1 }
  p.call
  2            # никогда не выполнится — return вышел из метода
end
```

`return` в proc возвращает из **окружающего метода**. Если метод уже завершился — `LocalJumpError`.

## Что такое блок

Блок — не объект, а синтаксис передачи кода в метод. `&block` превращает его в Proc. `yield` вызывает блок без создания объекта (быстрее).

## Фраза для собеса

«Lambda проверяет число аргументов и `return` из неё локальный; proc — нет, и `return` выходит из метода. Проверить можно `.lambda?`».

## Ловушка

`Proc.new`, `proc {}`, `&block` — все не-лямбды. `->() {}`, `lambda {}` и `method(:x).to_proc` — лямбды.
