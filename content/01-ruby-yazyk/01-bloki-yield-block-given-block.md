---
title: "Блоки, `yield`, `block_given?`, `&block`"
hot: true
links:
  - { t: "Ruby docs — Calling Methods: Block Argument", u: "https://docs.ruby-lang.org/en/master/syntax/calling_methods_rdoc.html#label-Block+Argument" }
  - { t: "Ruby docs — Methods: yield", u: "https://docs.ruby-lang.org/en/master/syntax/methods_rdoc.html#label-Block+Argument" }
---
Блок — кусок кода, который передаётся методу **синтаксически**, а не как объект. Любой метод может принять блок, даже не объявляя его.

```ruby
def twice
  return enum_for(:twice) unless block_given?   # идиома: без блока вернуть Enumerator
  yield 1
  yield 2
end

twice { |x| puts x }
```

- `yield` — вызвать блок, передав аргументы. Быстрее, чем `block.call`, т.к. не создаётся объект Proc.
- `block_given?` — передали ли блок. Без проверки `yield` упадёт с `LocalJumpError`.
- `&block` в сигнатуре — материализовать блок в `Proc`, чтобы сохранить или передать дальше.
- `&` при вызове — обратное: `arr.each(&my_proc)`.

```ruby
def wrap(&block)        # block — Proc
  log { block.call }    # можно передать дальше
end
```

Блок видит локальные переменные места, где написан (замыкание), и может их менять.

## Фраза для собеса

«Блок — это не объект, а синтаксис; `yield` вызывает его напрямую, `&block` превращает в Proc, когда блок нужно сохранить или передать».
