---
title: "Задание: ресурс `Exchange` с валидацией, сервисом и тестами"
hot: false
sub: "практика · 20–40 мин"
---
В пустом Rails API-приложении (`rails new --api`) сделать ресурс `exchanges`:

1. Миграция: `amount_cents bigint not null`, `rate numeric(18,8) not null`, `status string not null default 'pending'`, `email string not null`, уникальный индекс по `idempotency_key`.
2. Модель: валидации (`amount_cents > 0`, `email` формат, `status` через `enum`), `scope :recent`, `before_validation` для нормализации email.
3. `POST /exchanges` создаёт запись через сервис-объект `Exchanges::Create` (не в контроллере); сервис возвращает результат `success?/error`. Контроллер отдаёт `201` или `422` с массивом ошибок.
4. `GET /exchanges/:id` с `show` через сериализатор (jbuilder или ручной `as_json` с allowlist полей) — поле `email` не отдаётся.
5. Повторный `POST` с тем же `idempotency_key` возвращает ту же запись, а не `422`.
6. Request-спеки на все три сценария: успех, невалидные данные, повтор ключа. N+1 отсутствует (проверить `bullet` или `strict_loading`).

Критерий: `rails test`/`rspec` зелёный, `rails routes` показывает только два маршрута.
