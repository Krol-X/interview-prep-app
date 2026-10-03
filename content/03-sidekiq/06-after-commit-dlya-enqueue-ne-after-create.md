---
title: "`after_commit` для enqueue, не `after_create`"
hot: true
links:
  - { t: "Sidekiq wiki — Problems and Troubleshooting (Cannot find ModelName with ID=12345)", u: "https://github.com/sidekiq/sidekiq/wiki/Problems-and-Troubleshooting" }
---
Самый частый production-баг с Sidekiq.

```ruby
after_create :enqueue          # джоб в Redis ДО COMMIT
# Sidekiq забирает за ~1 мс → Withdrawal.find(id) → RecordNotFound,
# потому что транзакция Rails ещё не закоммичена и запись никому не видна

after_create_commit :enqueue   # после COMMIT — запись гарантированно есть
```

Почему это коварно: с retry джоб через 15 секунд найдёт запись и отработает — «иногда в логах RecordNotFound» годами никто не чинит. А с `retry: false` — просто теряется.

То же для: `after_save` + `deliver_later`, любые внешние вызовы (HTTP, Slack) из `after_save`/`after_create`.

Правила:
- `after_commit on: [:create]` / `after_create_commit`, `after_update_commit`, `after_save_commit` (6.1).
- В сервисе с явной транзакцией — enqueue **после** блока `transaction do ... end`, или `ActiveRecord.after_all_transactions_commit { ... }` (7.2).
- ActiveJob в Rails 7.2: `config.active_job.enqueue_after_transaction_commit = :default/:always` — откладывает автоматически. Для нативного Sidekiq — нет.
- Тесты с транзакционными фикстурами: Rails 5+ корректно вызывает `after_commit` в тестах, но `Sidekiq::Testing.inline!` внутри транзакции всё равно может не увидеть запись — используй `fake!`.

## Фраза для собеса

«Enqueue — побочный эффект наружу, он должен ждать COMMIT: `after_create_commit`, а в сервисе — после блока транзакции».
