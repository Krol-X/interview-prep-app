---
title: "`dry-schema` vs `dry-validation` — разница"
hot: false
links:
  - { t: "dry-schema", u: "https://dry-rb.org/gems/dry-schema/" }
  - { t: "dry-validation — Introduction", u: "https://dry-rb.org/gems/dry-validation/" }
---
**dry-schema** — только структура: ключи, типы, приведение, простые предикаты (`filled?`, `gt?`, `format?`). Быстрый, без состояния, без доступа к другим полям.

```ruby
Schema = Dry::Schema.Params { required(:amount).filled(:integer, gt?: 0) }
Schema.call("amount" => "5").to_h   # { amount: 5 }
```

**dry-validation** — надстройка: `Contract` = схема (`params do`) **+ `rule`** с произвольной логикой, кросс-полевыми проверками, внешними зависимостями (репозиторий, текущий пользователь), макросами.

Когда что:
- Проверить форму JSON/конфига/ENV, параметров джоба → `dry-schema` достаточно.
- Валидация ввода с бизнес-правилами («адрес существует в сети», «сумма ≤ лимита пользователя») → `dry-validation`.

Оба отдают `result.errors.to_h` в одном формате; `Contract` внутри использует `dry-schema`, так что переход — добавить `rule`.

## Фраза для собеса

«Schema — форма и типы, Validation — schema плюс rules с бизнес-логикой и зависимостями».
