---
title: "Scopes vs class methods; chaining; `merge`"
hot: false
links:
  - { t: "Rails Guides — Scopes", u: "https://guides.rubyonrails.org/active_record_querying.html#scopes" }
---
```ruby
scope :sent,   -> { where(status: "sent") }
scope :recent, ->(n = 10) { order(created_at: :desc).limit(n) }
scope :by_user, ->(u) { joins(:wallet).where(wallets: { user_id: u.id }) }

def self.big = where("amount_sat >= ?", 1_000_000)   # то же как класс-метод
```

Разница одна, но важная: scope **всегда возвращает relation** — если лямбда вернула `nil`/`false`, scope отдаст `all`, цепочка не сломается. Класс-метод вернёт то, что вернёт. Для условных веток (`return unless x`) scope безопаснее; для сложной логики с несколькими путями — класс-метод читается лучше.

Цепочки ленивы: SQL уходит при итерации/`to_a`/`first`/`count`. Можно собирать условно:
```ruby
rel = Withdrawal.all
rel = rel.sent if params[:sent]
rel = rel.where(created_at: range) if range
```

`merge` — применить скоуп другой модели через join:
```ruby
Withdrawal.joins(:wallet).merge(Wallet.active)
```

`default_scope` — почти всегда зло: невидим, ломает `find`, требует `unscoped`. Исключение — soft delete, и то спорно.

`scope` с тем же именем, что ассоциация/колонка — конфликт. `where.not`, `or` (5+), `rewhere`, `unscope(:order)`.

## Фраза для собеса

«Scope всегда возвращает relation, поэтому безопасен в цепочках; `merge` переносит scope через join; `default_scope` избегаю».
