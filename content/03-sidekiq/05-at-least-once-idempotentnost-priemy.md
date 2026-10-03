---
title: "At-least-once → идемпотентность; приёмы"
hot: true
links:
  - { t: "Sidekiq wiki — Best Practices", u: "https://github.com/sidekiq/sidekiq/wiki/Best-Practices" }
  - { t: "Sidekiq wiki — Error Handling", u: "https://github.com/sidekiq/sidekiq/wiki/Error-Handling" }
---
Sidekiq гарантирует доставку **хотя бы один раз**, не ровно один. Джоб может выполниться дважды:

- упал на середине → retry;
- процесс убит после выполнения, но до подтверждения;
- дабл-клик / двойной enqueue из-за `after_create` без commit.

Вывод: **повторный запуск с теми же аргументами не должен менять результат.**

## Приёмы

**Проверка состояния перед действием**
```ruby
return if withdrawal.sent?
```

**Атомарный захват**
```ruby
updated = Withdrawal.where(id: id, status: "pending").update_all(status: "processing")
return unless updated == 1   # кто-то уже взял
```

**Идемпотентный ключ наружу** — внешнему API передаётся `idempotency_key` (Stripe-стиль); повторный вызов возвращает тот же результат.

**Сохранить результат до побочного эффекта** — записать txid в БД сразу после получения, до отправки уведомлений; при повторе — увидеть и выйти.

**Разделить фазы** — отправка денег и уведомление в Slack — разные джобы. Падение второго не должно ретраить первый.

## Анти-паттерн

```ruby
def perform(id)
  ...
rescue => e
  Rails.logger.error(e)   # проглотили — Sidekiq считает успехом, retry не будет
end
```

Либо не ловить, либо re-raise после пометки.

## Фраза для собеса

«Делаю джобы идемпотентными: проверяю статус, захватываю его атомарным UPDATE, внешние вызовы — с idempotency key, а побочные эффекты — в отдельные джобы».
