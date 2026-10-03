---
title: "ActiveJob vs нативный Sidekiq"
hot: true
links:
  - { t: "Rails Guides — Active Job Basics", u: "https://guides.rubyonrails.org/active_job_basics.html" }
  - { t: "Sidekiq wiki — Active Job", u: "https://github.com/sidekiq/sidekiq/wiki/Active-Job" }
---
**ActiveJob** — абстракция Rails над очередями. Один API, адаптер подставляется (`:sidekiq`, `:solid_queue`, `:async`, `:test`).

```ruby
class ProcessWithdrawalJob < ApplicationJob
  queue_as :critical
  retry_on Timeout::Error, wait: :polynomially_longer, attempts: 5
  discard_on ActiveRecord::RecordNotFound
  def perform(withdrawal) = ...        # можно передать модель — GlobalID
end
ProcessWithdrawalJob.perform_later(withdrawal)
ProcessWithdrawalJob.set(wait: 5.minutes).perform_later(...)
```

**Нативный Sidekiq::Job** — напрямую, без прослойки:
```ruby
class ProcessWithdrawalWorker
  include Sidekiq::Job
  sidekiq_options queue: :critical, retry: 5
  def perform(withdrawal_id) = ...     # только JSON-примитивы
end
```

| | ActiveJob | Sidekiq::Job |
|---|---|---|
| Аргументы | GlobalID, Date/Time, символы | только JSON |
| Скорость | медленнее (сериализация, обёртки) ×2–5 | быстрее |
| Опции Sidekiq | часть недоступна (`sidekiq_retry_in`, batches, unique) | все |
| Retry | `retry_on` в Ruby, иначе Sidekiq default | встроенный backoff, retry/dead set в UI |
| Смена бэкенда | адаптер | переписывать |
| `deliver_later`, Turbo | через ActiveJob | — |

Практика: мейлеры и Rails-интеграции идут через ActiveJob в любом случае; свои тяжёлые/критичные джобы на Sidekiq часто пишут нативно. Rails 7.2+ `enqueue_after_transaction_commit` — только для ActiveJob.

## Фраза для собеса

«ActiveJob — переносимость и интеграция с Rails, нативный Sidekiq — скорость и полный доступ к его фичам; в одном приложении могут жить оба».
