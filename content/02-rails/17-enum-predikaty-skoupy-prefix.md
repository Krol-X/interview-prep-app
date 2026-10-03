---
title: "`enum`: предикаты, скоупы, `_prefix`"
hot: false
links:
  - { t: "Rails API — ActiveRecord::Enum", u: "https://api.rubyonrails.org/classes/ActiveRecord/Enum.html" }
---
```ruby
class Withdrawal < ApplicationRecord
  enum :status, { pending: 0, processing: 1, sent: 2, failed: 3 }, prefix: true, default: :pending
end

w.status                 # "sent" (строка)
w.status_sent?           # предикат (с prefix: true; без — w.sent?)
w.status_sent!           # update!(status: :sent) — без валидаций? нет, с ними, но без проверки перехода
Withdrawal.status_sent   # scope
Withdrawal.not_status_sent
Withdrawal.statuses      # { "pending" => 0, ... }
where(status: :sent)     # можно символом
```

- Хранить **integer** с явным маппингом (не массив — порядок сломается при вставке). Строковый enum (`{ sent: "sent" }`) — читаемее в БД, чуть больше места; в Postgres можно native enum type, но миграции сложнее.
- `prefix`/`suffix` — обязательно, если у модели несколько enum или имена конфликтуют (`active?` уже есть).
- Невалидное значение → `ArgumentError` при присвоении, не ошибка валидации. Для формы — `validates :status, inclusion:` + `validate: true` опция (7.1).
- Enum **не проверяет переходы**: `failed → sent` пройдёт. Для state machine — guard-методы или gem (`aasm`, `statesman`).
- Rails 7: синтаксис `enum :status, {...}`; старый `enum status: {...}` deprecated в 7.2+.

## Фраза для собеса

«Enum на integer с явным маппингом и prefix; даёт предикаты и скоупы, но переходы между состояниями не контролирует — это пишу сам».
