---
title: "Ассоциации: `has_many through`, `inverse_of`, `dependent:`, polymorphic"
hot: false
links:
  - { t: "Rails Guides — Active Record Associations", u: "https://guides.rubyonrails.org/association_basics.html" }
---
```ruby
class User < ApplicationRecord
  has_one  :wallet, dependent: :destroy
  has_many :withdrawals, through: :wallet
end
class Wallet < ApplicationRecord
  belongs_to :user                   # обязателен по умолчанию (Rails 5+); optional: true
  has_many :withdrawals, dependent: :restrict_with_error, inverse_of: :wallet
end
```

- `has_many :through` — связь через промежуточную модель; работает и для many-to-many с явной join-моделью (предпочтительнее `has_and_belongs_to_many`).
- `dependent:` — `:destroy` (колбэки, по одному), `:delete_all` (один SQL, без колбэков), `:nullify`, `:restrict_with_error`/`:restrict_with_exception`. Без него — осиротевшие строки или FK-ошибка. FK в БД — обязательно.
- `inverse_of` — чтобы `wallet.withdrawals.first.wallet` был тем же объектом, а не новым запросом; Rails угадывает в простых случаях, с `through`/`foreign_key`/scope — укажи явно.
- `polymorphic: true` — `belongs_to :commentable, polymorphic: true` + `commentable_type`/`commentable_id`. FK в БД невозможен — минус.
- `counter_cache: true` — денормализованный счётчик, обновляется колбэками.
- Scope на ассоциации: `has_many :sent_withdrawals, -> { where(status: "sent") }, class_name: "Withdrawal"`.
- `belongs_to` добавляет presence-валидацию; `has_many` — нет.

Запросы: `user.withdrawals` — lazy relation; `.build`/`.create` проставят FK; `<<` сохраняет сразу.

## Фраза для собеса

«`through` для связей через модель, `dependent` + FK в БД обязательно, `inverse_of` явно там, где Rails не угадает».
