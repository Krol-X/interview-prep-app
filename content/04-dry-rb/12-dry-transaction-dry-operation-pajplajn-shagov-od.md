---
title: "`dry-transaction` / `dry-operation` — пайплайн шагов, одна фраза"
hot: false
links:
  - { t: "dry-operation", u: "https://dry-rb.org/gems/dry-operation/" }
  - { t: "dry-transaction (legacy)", u: "https://dry-rb.org/gems/dry-transaction/" }
---
Формализованный сервис из шагов, где каждый возвращает `Result`, и Failure останавливает цепочку.

**dry-operation** (актуальный, 2024+):
```ruby
class CreateWithdrawal < Dry::Operation
  include Dry::Operation::Extensions::ActiveRecord     # transaction { } с откатом на Failure

  def call(input)
    attrs  = step validate(input)
    w = transaction do
      wallet = step lock_wallet(attrs)
      step debit(wallet, attrs)
      step create_record(wallet, attrs)
    end
    step enqueue(w)                                    # вне транзакции — после коммита
    w
  end

  private
  def validate(i) = WithdrawalContract.new.call(i).to_monad
  ...
end
```

`step` ≈ `yield` из Do-notation, но операция ещё умеет: оборачивать шаги в транзакцию с автооткатом при Failure (главная боль Do + AR), хуки `on_failure`, расширения для Sequel/ROM.

**dry-transaction** — предшественник с DSL `step :validate; map :x; tee :log`. Deprecated в пользу dry-operation; встречается в старых проектах — узнавать.

Альтернативы вне dry: `interactor` (context-объект, `rollback`), `trailblazer-operation` (тяжёлый), `ActiveInteraction`. Все про одно: явные шаги + явный результат.

## Фраза для собеса

«dry-operation — сервис из `step`-ов с Result и транзакцией, которая откатывается на Failure; dry-transaction — его устаревший предок».
