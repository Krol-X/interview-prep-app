---
title: "Сервисные объекты / interactors / form objects — где логика, не в контроллере"
hot: true
links:
  - { t: "thoughtbot — Skinny Controllers, Skinny Models", u: "https://thoughtbot.com/blog/skinny-controllers-skinny-models" }
  - { t: "dry-rb — dry-monads", u: "https://dry-rb.org/gems/dry-monads/" }
---
Где жить логике «создать вывод: списать, записать, поставить джоб»? Не в контроллере (не тестируется без HTTP, не переиспользуется) и не в модели (модель начинает знать про Sidekiq, почту, другие модели — «god object»).

**Service object** — класс с одной публичной операцией:
```ruby
class CreateWithdrawal
  Result = Data.define(:success?, :withdrawal, :error)

  def initialize(user:, params:) = (@user, @params = user, params)

  def call
    ActiveRecord::Base.transaction do
      wallet = @user.wallet.lock!
      return Result.new(false, nil, :insufficient) if wallet.balance < total
      wallet.decrement!(:balance, total)
      w = wallet.withdrawals.create!(@params.merge(status: :pending))
      ProcessWithdrawalWorker.perform_async(w.id)   # лучше after_commit
      Result.new(true, w, nil)
    end
  end
end
```
Контроллер: вызвать, по результату `render`/`redirect`. Тест — чистый Ruby.

- Возвращать результат-объект, не bool и не исключения для ожидаемых исходов. dry-monads `Success/Failure` — стандартный вариант.
- **Form object** — когда форма не 1:1 с моделью (регистрация = user + wallet + соглашение): `include ActiveModel::Model`, валидации, `save` создаёт всё.
- **Query object** — сложная выборка в классе с `call` → relation.
- **Policy** — авторизация (Pundit). **Presenter/Decorator** — логика отображения. **Interactor/Operation** (gem interactor, dry-operation, trailblazer) — сервис с шагами и откатом.

Модель остаётся для: валидаций, скоупов, простых методов над своими данными.

## Фраза для собеса

«Контроллер тонкий, модель про свои данные, сценарии — в сервисах с явным результатом; формы не 1:1 — form object».
