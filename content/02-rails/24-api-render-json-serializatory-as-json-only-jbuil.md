---
title: "API: `render json`, сериализаторы (`as_json(only:)`, jbuilder, blueprinter)"
hot: false
links:
  - { t: "Rails Guides — Using Rails for API-only Applications", u: "https://guides.rubyonrails.org/api_app.html" }
  - { t: "gem blueprinter", u: "https://github.com/procore-oss/blueprinter" }
---
```ruby
render json: withdrawal
# вызывает withdrawal.as_json → to_json. ВСЕ колонки, включая внутренние (wallet_id, lock_version…)

render json: withdrawal.as_json(only: [:id, :amount, :status], methods: [:total], include: { wallet: { only: :address } })
render json: { data: ..., meta: ... }, status: :created
head :no_content
```

Переопределять `as_json` в модели — быстро, но один формат на все эндпоинты. Лучше отдельный слой:

- **Blueprinter / Alba / Panko** — классы-сериализаторы: `WithdrawalBlueprint.render(w, view: :detailed)`. Быстрые, явные.
- **jbuilder** — шаблоны `.json.jbuilder` во views, удобно для вложенных структур, медленнее.
- **ActiveModel::Serializers** — исторический, полуживой.
- **JSON:API** (`jsonapi-serializer`) — если нужен стандарт.

Правила API:
- Явный белый список полей (приватные данные, внутренние id).
- Деньги — строкой или integer в минимальных единицах, не float в JSON.
- Статусы — `status:` HTTP-кодом + тело с ошибкой единого формата `{ error: { code:, message: } }`.
- `rescue_from ActiveRecord::RecordNotFound, with: :not_found` в `ApplicationController`.
- Пагинация (`pagy`), версионирование (`/api/v1`), `Content-Type: application/json`.
- `--api` режим: `ActionController::API`, без views/cookies/CSRF.

## Фраза для собеса

«`render json: model` отдаёт всё — всегда сериализатор с белым списком полей; ошибки — единым форматом и правильными кодами».
