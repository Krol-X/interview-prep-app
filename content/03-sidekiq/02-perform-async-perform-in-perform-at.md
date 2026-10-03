---
title: "`perform_async`, `perform_in`, `perform_at`"
hot: false
links:
  - { t: "Sidekiq wiki — Scheduled Jobs", u: "https://github.com/sidekiq/sidekiq/wiki/Scheduled-Jobs" }
---
```ruby
ProcessWithdrawalWorker.perform_async(withdrawal.id)          # сразу в очередь
ProcessWithdrawalWorker.perform_in(5.minutes, withdrawal.id)   # через интервал
ProcessWithdrawalWorker.perform_at(1.hour.from_now, withdrawal.id)
ProcessWithdrawalWorker.set(queue: :low, retry: 2).perform_async(id)   # переопределить опции
ProcessWithdrawalWorker.perform_bulk([[1], [2], [3]])           # пачкой, один round-trip
ProcessWithdrawalWorker.new.perform(id)                         # синхронно, без Redis (отладка/тест)
```

- `perform_async` возвращает `jid` (строка) — можно сохранить для трекинга.
- Отложенные джобы лежат в Redis sorted set `schedule`; точность — секунды (поллер). Не для «ровно в 00:00:00».
- Enqueue — побочный эффект наружу: делать после COMMIT (`after_commit`), иначе воркер может не найти запись.
- `perform_in(0)` ≈ `perform_async`, но через scheduled set — медленнее.
- Периодические задачи (cron) — не часть OSS Sidekiq: `sidekiq-cron`, `sidekiq-scheduler` или Enterprise.
- Нельзя передать блок, объект, lambda — только то, что сериализуется в JSON.

## Фраза для собеса

«`perform_async` — сейчас, `perform_in/at` — через scheduled set с точностью до секунд; ставлю после коммита и передаю только id».
