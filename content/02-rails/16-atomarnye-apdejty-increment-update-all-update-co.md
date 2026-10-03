---
title: "Атомарные апдейты: `increment!`, `update_all`, `update_counters`"
hot: true
links:
  - { t: "Rails API — increment!", u: "https://api.rubyonrails.org/classes/ActiveRecord/Persistence.html#method-i-increment-21" }
  - { t: "Rails API — update_counters", u: "https://api.rubyonrails.org/classes/ActiveRecord/CounterCache/ClassMethods.html#method-i-update_counters" }
---
Read-modify-write в Ruby — гонка: два процесса прочитали 100, оба записали 90 вместо 80.

```ruby
# плохо
wallet.balance -= 10; wallet.save!

# атомарно — арифметика в SQL
wallet.increment!(:balance, -10)             # UPDATE ... SET balance = COALESCE(balance,0) - 10
Wallet.update_counters(id, balance: -10)     # то же без объекта
Wallet.where(id: id).update_all("balance = balance - 10")
Wallet.where(id: id, balance: 10..).update_all("balance = balance - 10")  # с условием → rowcount
```

- `increment!` — без валидаций и колбэков, `touch`-ит `updated_at`. Объект в памяти обновляет локально.
- `update_all` — вернёт число строк: `== 1` значит условие прошло. Это замена `with_lock` для простых случаев: одна команда, нет блокировки-ожидания.
- `update_all` принимает хеш или SQL-строку с placeholders: `update_all(["balance = balance - ?", amt])`.
- `upsert_all` — массовая вставка/обновление с `ON CONFLICT`.
- `touch_all`, `delete_all` — той же природы.

Всё это обходит колбэки — после `update_all` объекты в памяти устарели (`reload`).

## Фраза для собеса

«Арифметику — в SQL: `increment!` или `update_all` с условием и проверкой rowcount; это атомарно и не требует блокировки».
