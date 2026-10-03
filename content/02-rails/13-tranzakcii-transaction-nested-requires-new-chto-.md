---
title: "Транзакции: `transaction`, nested + `requires_new`, что откатывает `rollback`"
hot: true
links:
  - { t: "Rails API — ActiveRecord::Transactions", u: "https://api.rubyonrails.org/classes/ActiveRecord/Transactions/ClassMethods.html" }
---
```ruby
ActiveRecord::Base.transaction do
  wallet.debit!(total)
  withdrawal.save!
end
# любое исключение → ROLLBACK и re-raise; вернулось нормально → COMMIT
```

- Используй `!`-методы внутри: `save` вернёт false и транзакция **закоммитится** с частичными данными.
- `raise ActiveRecord::Rollback` — откатить без пробрасывания наружу (транзакция вернёт nil).
- Внутри транзакции не делать HTTP, не слать джобы и письма — всё внешнее в `after_commit` или после блока. Долгая транзакция держит блокировки.

Вложенность:
```ruby
Model.transaction do
  Model.transaction do          # НЕ новая транзакция — та же самая
    raise ActiveRecord::Rollback # проглочен внутренним блоком, внешняя закоммитится!
  end
end

Model.transaction do
  Model.transaction(requires_new: true) do   # SAVEPOINT — откатится только он
    raise ActiveRecord::Rollback
  end
end
```

Один `transaction` = одна БД-транзакция на соединение. Соединение привязано к потоку — в Thread внутри блока транзакции не будет.

`after_commit` на модели срабатывает после внешнего COMMIT. `transaction(isolation: :serializable)` — задать уровень.

Rails 7.2: `ActiveRecord.after_all_transactions_commit { }` и `transaction.after_commit { }` — колбэк на саму транзакцию, не на модель.

## Фраза для собеса

«Внутри транзакции — только `!`-методы и только БД; вложенный `transaction` без `requires_new` — та же транзакция, `Rollback` там проглотится».
