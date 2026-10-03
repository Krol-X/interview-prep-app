---
title: "Валидации: `validates`, custom validator, `valid?` vs `validate!`, контексты"
hot: false
links:
  - { t: "Rails Guides — Active Record Validations", u: "https://guides.rubyonrails.org/active_record_validations.html" }
---
```ruby
class Withdrawal < ApplicationRecord
  validates :to_address, presence: true, format: { with: /\A(tb1|2|m|n)/ }
  validates :amount, numericality: { greater_than: 0, only_integer: true }
  validates :status, inclusion: { in: STATUSES }
  validates :txid, uniqueness: true, allow_nil: true     # + unique index в БД!
  validate :enough_balance, on: :create                  # кастомный метод

  private
  def enough_balance
    errors.add(:amount, :insufficient, message: "exceeds balance") if amount > wallet.balance
  end
end
```

- `valid?` — прогоняет валидации, заполняет `errors`, возвращает bool. `invalid?` — наоборот.
- `validate!` — то же, но бросает `RecordInvalid`.
- `errors.add(:base, ...)` — ошибка не к полю. `errors.full_messages`, `errors[:amount]`, `errors.details`.
- Контексты: `on: :create`, свои — `valid?(:payout)`, `save(context: :payout)`.
- Условия: `if: :foreign?`, `unless: -> { draft? }`.
- Выносимый валидатор: `class AddressValidator < ActiveModel::EachValidator; def validate_each(record, attr, value)`. Подключается `validates :to_address, address: true`.
- `uniqueness` **не атомарна** (SELECT потом INSERT) — гонка. Обязателен unique index; ловить `RecordNotUnique`.

Валидации работают только в Ruby: `update_column`, `update_all`, `insert_all`, `delete` их обходят.

## Фраза для собеса

«Валидации — в модели, но инварианты дублирую constraint'ами в БД: uniqueness без индекса — гонка».
