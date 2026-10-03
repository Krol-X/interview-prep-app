---
title: "Locking: `with_lock`/`lock!` (pessimistic), `lock_version` (optimistic)"
hot: true
links:
  - { t: "Rails Guides — Locking Records for Update", u: "https://guides.rubyonrails.org/active_record_querying.html#locking-records-for-update" }
  - { t: "Rails API — Locking::Optimistic", u: "https://api.rubyonrails.org/classes/ActiveRecord/Locking/Optimistic.html" }
---
**Пессимистичная** — блокируем строку в БД, конкуренты ждут.

```ruby
wallet.with_lock do                 # transaction + reload(lock: true) → SELECT ... FOR UPDATE
  raise Insufficient if wallet.balance < amount
  wallet.update!(balance: wallet.balance - amount)
end
Wallet.lock.find(id)                # FOR UPDATE внутри своей транзакции
Wallet.lock("FOR UPDATE SKIP LOCKED")
```

Когда: деньги, счётчики, очереди — короткая критическая секция, конфликты часты. Минусы: ждут, возможны deadlock'и (блокируй в одном порядке).

**Оптимистичная** — колонка `lock_version`; `UPDATE ... WHERE id = ? AND lock_version = ?`; если 0 строк — `StaleObjectError`.

```ruby
# миграция: t.integer :lock_version, default: 0, null: false
w = Withdrawal.find(1)   # lock_version 3
w.update!(note: "x")     # ok → 4
# параллельно другой с version 3: StaleObjectError
```

Когда: редкие конфликты, длинные формы редактирования (пользователь думает минуту), нет смысла держать блокировку. Нужно ловить и показывать «запись изменена, обновите».

Оба — на уровне одной строки. Для «только один процесс делает X» — advisory lock или unique-строка.

## Фраза для собеса

«Для денег — `with_lock` (FOR UPDATE), короткая секция; для редактирования форм — `lock_version` и обработка StaleObjectError».
