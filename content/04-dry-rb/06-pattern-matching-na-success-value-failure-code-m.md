---
title: "Паттерн-матчинг на `Success(value)` / `Failure[:code, msg]`"
hot: true
links:
  - { t: "dry-monads — Pattern matching", u: "https://dry-rb.org/gems/dry-monads/1.6/pattern-matching/" }
---
`Success`/`Failure` реализуют `deconstruct`/`deconstruct_keys`, поэтому матчатся в `case/in`:

```ruby
case CreateWithdrawal.new.call(params)
in Success(Withdrawal => w)                 # Success с проверкой класса
  render json: w, status: :created
in Failure[:insufficient_funds, need, have] # Failure с массивом — деструктуризация по позициям
  render json: { error: "need #{need}, have #{have}" }, status: 422
in Failure[:validation, errors]
  render json: { errors: }, status: 400
in Failure(ActiveRecord::RecordNotFound)    # Failure с объектом-исключением
  head :not_found
in Failure(err)                             # всё остальное
  Rails.error.report(err); head :internal_server_error
end
```

- `Success(x)` — круглые скобки: одно значение. `Failure[:code, *rest]` — квадратные: деструктуризация массива. Для хеша: `Success({ txid:, fee: })`.
- Без `else` непокрытый случай → `NoMatchingPatternError`. Это хорошо: добавил новый код ошибки в сервис — тесты контроллера упадут, пока не обработаешь.
- Конвенция `Failure[:symbol, payload]` делает ветки читаемыми и greppable.
- Матчить можно и на `Maybe`: `in Some(v)` / `in None`.

## Фраза для собеса

«Результат разбираю `case/in`: `Success(v)` и `Failure[:code, data]`; отсутствие `else` заставляет обработать каждый код ошибки».
