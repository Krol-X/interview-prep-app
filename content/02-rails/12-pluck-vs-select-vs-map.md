---
title: "`pluck` vs `select` vs `map`"
hot: true
links:
  - { t: "Rails API — pluck", u: "https://api.rubyonrails.org/classes/ActiveRecord/Calculations.html#method-i-pluck" }
---
```ruby
Withdrawal.where(status: "sent").map(&:txid)
# SELECT withdrawals.* → строит 10 000 AR-объектов → берёт поле. Медленно, память.

Withdrawal.where(status: "sent").pluck(:txid)
# SELECT txid FROM ... → массив строк. Без объектов. В разы быстрее.
Withdrawal.pluck(:id, :txid)       # [[1,"a"],[2,"b"]]
Withdrawal.pick(:txid)             # pluck + limit 1

Withdrawal.select(:id, :txid)
# SELECT id, txid → AR-объекты только с этими полями; остальные → MissingAttributeError
# Relation остаётся цепляемой: .select(...).where(...).order(...)
Withdrawal.select("wallet_id, SUM(fee) AS total").group(:wallet_id)   # агрегаты как атрибуты
```

| | Возвращает | Объекты | Цепляется дальше |
|---|---|---|---|
| `map` | массив | да, полные | нет |
| `pluck` | массив значений | нет | нет (терминальный) |
| `select` | relation | да, частичные | да |
| `ids` | массив id | нет | нет |

`pluck` на уже загруженной коллекции (`user.withdrawals.pluck`) всё равно пойдёт в БД — если записи уже загружены, `map` дешевле. `distinct.pluck`, `pluck` с `joins` — `pluck("wallets.address")`.

## Фраза для собеса

«Нужны только значения — `pluck`; нужны объекты, но не все поля или подзапрос — `select`; `map` — только на уже загруженной коллекции».
