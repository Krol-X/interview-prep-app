---
title: "`find` vs `find_by` vs `where.first`; `find_each`/`in_batches`"
hot: true
links:
  - { t: "Rails Guides — Retrieving Objects", u: "https://guides.rubyonrails.org/active_record_querying.html#retrieving-objects-from-the-database" }
  - { t: "Rails Guides — Retrieving Multiple Objects in Batches", u: "https://guides.rubyonrails.org/active_record_querying.html#retrieving-multiple-objects-in-batches" }
---
```ruby
Withdrawal.find(5)            # по PK; RecordNotFound → в контроллере это 404
Withdrawal.find_by(txid: t)   # первый по условию или nil
Withdrawal.find_by!(txid: t)  # или RecordNotFound
Withdrawal.where(txid: t).first   # то же, что find_by, но добавит ORDER BY id
Withdrawal.where(txid: t).take    # без ORDER BY — что отдаст БД
```

Для внешних id (`params[:id]`) — `current_user.withdrawals.find(id)`: заодно авторизация и 404 вместо чужой записи.

Батчи — не грузить миллион объектов в память:
```ruby
Withdrawal.find_each(batch_size: 1000) { |w| ... }   # по PK, порядок игнорируется
Withdrawal.in_batches(of: 1000) { |rel| rel.update_all(...) }   # relation на батч
Withdrawal.in_batches.each_record { ... }
```

`find_each` отменяет `order`/`limit` (работает по id-курсору). Нужна сортировка — `in_batches(order: :desc)` или свой курсор.

`first`/`last` на relation без `order` — по PK. `first(3)` — массив. `exists?` дешевле `present?`/`any?` (не грузит записи).

## Фраза для собеса

«`find` — по PK с исключением, `find_by` — nil; большие выборки — `find_each`/`in_batches`, они идут по PK батчами и не держат всё в памяти».
