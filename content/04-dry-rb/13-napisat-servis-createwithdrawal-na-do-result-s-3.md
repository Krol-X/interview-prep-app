---
title: "Написать сервис `CreateWithdrawal` на `Do` + `Result` с 3 шагами (validate → debit → enqueue)"
hot: false
links:
  - { t: "dry-monads — Do notation", u: "https://dry-rb.org/gems/dry-monads/1.6/do-notation/" }
---
Упражнение на 40 минут. Напиши и прогони в консоли/спеке:

```ruby
class CreateWithdrawal
  include Dry::Monads[:result, :do]

  def initialize(contract: WithdrawalContract.new, fee_sat: 1_000)
    @contract, @fee_sat = contract, fee_sat
  end

  def call(user, raw_params)
    attrs = yield validate(raw_params)
    w     = yield debit(user, attrs)
    yield enqueue(w)
    Success(w)
  end

  private

  def validate(raw)
    r = @contract.call(raw)
    r.success? ? Success(r.to_h) : Failure[:validation, r.errors.to_h]
  end

  def debit(user, attrs)
    total = attrs[:amount_sat] + @fee_sat
    ActiveRecord::Base.transaction do
      wallet = user.wallet.lock!
      return Failure[:insufficient_funds, total, wallet.balance_sat] if wallet.balance_sat < total
      wallet.decrement!(:balance_sat, total)
      Success(wallet.withdrawals.create!(attrs.merge(fee_sat: @fee_sat, status: :pending)))
    end
  end

  def enqueue(w)
    ProcessWithdrawalWorker.perform_async(w.id)
    Success(w)
  rescue Redis::BaseError => e
    Failure[:queue_unavailable, e.message]
  end
end
```

Проверь себя:
1. Что вернёт `call`, если контракт не прошёл? Выполнится ли `debit`?
2. `return Failure` внутри `transaction do` — закоммитится ли транзакция? (Да — Failure не исключение. Здесь ок, потому что до списания; а если бы после?)
3. Напиши спек: три кейса через `case/in`.
4. Замени `yield`/Do на `dry-operation` со `step` и `transaction` — что стало проще?

Цель — не гем, а уметь обсуждать: где границы транзакции, когда enqueue, как тестировать без БД (инъекция контракта).
