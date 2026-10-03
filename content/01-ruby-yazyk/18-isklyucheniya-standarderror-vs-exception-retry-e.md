---
title: "Исключения: `StandardError` vs `Exception`, `retry`, `ensure`, custom errors"
hot: true
links:
  - { t: "Ruby docs — Exception (иерархия)", u: "https://docs.ruby-lang.org/en/master/Exception.html" }
  - { t: "Ruby docs — exceptions syntax", u: "https://docs.ruby-lang.org/en/master/syntax/exceptions_rdoc.html" }
---
```
Exception
├── NoMemoryError, SignalException (Interrupt), SystemExit, ScriptError (LoadError, SyntaxError)
└── StandardError          ← `rescue` без класса ловит ТОЛЬКО это
    ├── ArgumentError, TypeError, NameError → NoMethodError
    ├── RuntimeError (raise "str"), IOError, KeyError, ZeroDivisionError
    └── свои ошибки
```

`rescue Exception` ловит Ctrl-C, `exit`, нехватку памяти — процесс нельзя остановить. Почти всегда ошибка. `rescue => e` = `rescue StandardError => e`.

```ruby
class App::Error < StandardError; end          # базовый класс приложения
class InsufficientFunds < App::Error
  def initialize(need, have) = super("need #{need}, have #{have}")
end

attempts = 0
begin
  api.call
rescue Timeout::Error => e
  attempts += 1
  retry if attempts < 3            # повторить begin-блок
  raise                            # re-raise тот же объект с backtrace
ensure
  conn.close                       # всегда; не ставь здесь return — он подавит исключение
end
```

- `raise CustomError, "msg"` / `raise CustomError.new(...)`. `raise` без аргументов внутри rescue — повторно бросить текущее.
- `e.cause` — предыдущее исключение, если бросили новое внутри rescue.
- `rescue` в теле метода без `begin` — допустимо. `rescue ... else` — ветка, если исключения не было.
- Исключения — для исключительных ситуаций; для ожидаемых исходов (валидация) — Result/bool, не raise.

## Фраза для собеса

«Ловлю `StandardError` или конкретнее, свои ошибки наследую от него; `rescue Exception` — почти всегда баг; `retry` для повторов, `ensure` для освобождения ресурсов».
