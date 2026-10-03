---
title: "`dry-monads`: `Do` notation (`yield` внутри `call`) — читать и писать"
hot: true
links:
  - { t: "dry-monads — Do notation", u: "https://dry-rb.org/gems/dry-monads/1.6/do-notation/" }
---
Цепочки `bind { bind { bind } }` вложены и плохо читаются. Do-notation делает их линейными:

```ruby
class CreateWithdrawal
  include Dry::Monads[:result, :do]

  def call(params)
    attrs  = yield validate(params)        # если Failure — метод НЕМЕДЛЕННО вернёт этот Failure
    wallet = yield find_wallet(attrs[:user_id])
    w      = yield debit_and_create(wallet, attrs)
    yield enqueue(w)
    Success(w)
  end

  private
  def validate(p)  = Contract.new.call(p).to_monad      # Success(hash) / Failure(result)
  def find_wallet(id) = Maybe(Wallet.find_by(id:)).to_result(:wallet_not_found)
  ...
end
```

- `yield` здесь — не блок метода: `include Dry::Monads[:do]` оборачивает `call` (и любые методы, объявленные после) так, что `yield Failure` прерывает выполнение и возвращает Failure наружу. `yield Success(v)` возвращает `v`.
- Читается как обычный императивный код: «получи, получи, получи, верни».
- Работает с `Result`, `Maybe`, `Try`, `Validation`.
- Если нужен Do только в конкретных методах: `include Dry::Monads::Do.for(:call, :other)`.
- Ловушка: внутри `transaction do ... end` блок `yield Failure` вернёт из метода, но блок транзакции при этом закоммитится — Failure не исключение. Решение: `transaction { ... }.tap { raise Rollback if failure }` или `dry-monads` + `raise ActiveRecord::Rollback` вручную, либо `dry-transaction`/`dry-operation` с поддержкой транзакций.

## Фраза для собеса

«Do-notation: `yield result` разворачивает Success или досрочно возвращает Failure — цепочка шагов читается линейно; помню про транзакции».
