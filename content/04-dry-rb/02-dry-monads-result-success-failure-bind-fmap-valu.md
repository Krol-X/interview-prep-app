---
title: "`dry-monads`: `Result` — `Success`/`Failure`, `bind`, `fmap`, `value_or`, `or`"
hot: true
links:
  - { t: "dry-monads — Result", u: "https://dry-rb.org/gems/dry-monads/1.6/result/" }
---
```ruby
require "dry/monads"
include Dry::Monads[:result]

ok  = Success(42)
err = Failure(:not_found)              # любое значение: символ, строка, массив [:code, msg], объект

ok.success?  / ok.failure?
ok.value!                              # 42; на Failure — исключение UnwrapError
err.failure                            # :not_found
ok.value_or(0)                         # 42; у Failure вернёт 0

ok.fmap { _1 * 2 }                     # Success(84) — функция возвращает голое значение
ok.bind { |v| v > 0 ? Success(v) : Failure(:neg) }   # функция возвращает Result (можно «переключить рельсу»)
err.fmap { _1 * 2 }                    # Failure(:not_found) — блок не выполняется

err.or { |e| Success(default) }        # обработать ошибку, вернуть Result
err.or(Success(0))
ok.either(->(v) { ... }, ->(e) { ... })  # обе ветки
ok.to_maybe                            # Some(42)
Success(nil)                           # легально, но подозрительно
```

- `fmap` — map для успеха; `bind` (= `>>` / `flat_map`) — цепочка функций, возвращающих Result.
- `Failure` без `include Dry::Monads[:result]` в классе — не найдётся; включай модуль там, где используешь.
- Конвенция для ошибки: `Failure[:code, payload]` — удобно матчить. Или объект-ошибка с `#message`.
- `Try` оборачивает исключения в Result; `Task` — асинхронность; `List`.

## Фраза для собеса

«`Success/Failure`, `fmap` для чистой функции, `bind` для шага, который сам может упасть; достаю через pattern matching или `value_or`, не `value!`».
