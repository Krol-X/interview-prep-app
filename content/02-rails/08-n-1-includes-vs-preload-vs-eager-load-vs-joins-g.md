---
title: "N+1: `includes` vs `preload` vs `eager_load` vs `joins`; gem `bullet`"
hot: true
links:
  - { t: "Rails Guides — Eager Loading Associations", u: "https://guides.rubyonrails.org/active_record_querying.html#eager-loading-associations" }
  - { t: "gem bullet", u: "https://github.com/flyerhzm/bullet" }
---
N+1: один запрос за списком, потом по запросу на каждую связь в цикле.

```ruby
Withdrawal.limit(50).each { |w| w.wallet.user.email }   # 1 + 50 + 50 запросов
Withdrawal.includes(wallet: :user).limit(50)            # 3 запроса
```

| Метод | SQL | Когда |
|---|---|---|
| `preload` | отдельный `SELECT ... WHERE id IN (...)` на каждую связь | по умолчанию; не умеет фильтровать по связи |
| `eager_load` | один `LEFT OUTER JOIN` | когда нужно `where`/`order` по полям связи |
| `includes` | сам выбирает: preload, а при `references`/`where` по связи — eager_load | дефолт, но менее предсказуем |
| `joins` | `INNER JOIN`, **не загружает** связь | фильтрация/агрегация без доступа к объектам связи |

```ruby
Withdrawal.joins(:wallet).where(wallets: { user_id: 1 })     # фильтр, wallet не загружен
Withdrawal.includes(:wallet).where(wallets: { user_id: 1 })  # → eager_load автоматически
Withdrawal.preload(:wallet).merge(Wallet.active)             # ошибка: нет join
```

- `has_many` с `eager_load` умножает строки — Rails дедуплицирует, но тяжелее.
- `strict_loading` (6.1+): `Withdrawal.strict_loading.first.wallet` → исключение при ленивой загрузке. Можно включить на модель или глобально в dev/test.
- gem `bullet` — ловит N+1 и лишние includes в dev.
- `exists?`/`size` vs `count`: `size` использует загруженную коллекцию, `count` всегда SQL.

## Фраза для собеса

«`preload` — отдельные запросы, `eager_load` — JOIN, `includes` выбирает сам; `joins` для фильтра без загрузки. В dev — bullet или strict_loading».
