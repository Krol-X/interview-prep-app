---
title: "Pattern matching: `case/in`, деконструкция хешей/массивов, `=>` rightward, guard"
hot: true
links:
  - { t: "Ruby docs — Pattern matching", u: "https://docs.ruby-lang.org/en/master/syntax/pattern_matching_rdoc.html" }
---
```ruby
case response
in { status: 200, body: { txid: String => txid } }
  txid
in { status: 400.., error: msg }
  raise ApiError, msg
in [first, *rest]                      # массив: первый и остальные
in Integer | Float => n if n > 0      # альтернатива + guard
else
  raise "unexpected"
end
```

- Хеши матчатся **частично**: лишние ключи не мешают. Массивы — точно по длине (кроме `*`).
- `=> name` привязывает значение; `^var` — использовать существующую переменную, а не связать новую.
- `case/in` без `else` при промахе бросает `NoMatchingPatternError` — это фича: явный контракт.
- Однострочный: `config => { host:, port: }` (бросает) и `value in { ok: true }` (bool).
- Свои классы: реализовать `deconstruct` (для массивного паттерна) и `deconstruct_keys(keys)` (для хешевого). `Struct`/`Data` уже умеют.

С dry-monads: `case result in Success(value) ... in Failure[:not_found, msg]`.

Где уместно: разбор JSON/API-ответов, result-объектов, AST. Где нет: простой `if x.is_a?`.

## Фраза для собеса

«`case/in` деконструирует хеши и массивы с привязкой переменных и guard'ами; хеши матчатся частично, отсутствие `else` — ошибка при промахе».
