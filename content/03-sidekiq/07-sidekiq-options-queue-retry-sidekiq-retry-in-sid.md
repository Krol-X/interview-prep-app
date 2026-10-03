---
title: "`sidekiq_options`: queue, retry, `sidekiq_retry_in`, `sidekiq_retries_exhausted`"
hot: false
links:
  - { t: "Sidekiq wiki — Advanced Options (Workers)", u: "https://github.com/sidekiq/sidekiq/wiki/Advanced-Options#workers" }
---
```ruby
class ProcessWithdrawalWorker
  include Sidekiq::Job
  sidekiq_options queue: :critical,     # очередь (по умолчанию :default)
                  retry: 5,             # число попыток (true = 25, false = нет)
                  backtrace: 20,        # сохранять строки backtrace в retry/dead (память!)
                  dead: false,          # не класть в морг после исчерпания
                  tags: ["payout"]      # видны в UI

  sidekiq_retry_in do |count, exception|
    case exception
    when InvalidAddress then :discard       # не ретраить
    when NodeDown       then 60 * (count + 1)
    else                     nil            # дефолтная кривая
    end
  end

  sidekiq_retries_exhausted do |job, ex|
    Withdrawal.find_by(id: job["args"].first)&.update!(status: :failed)
    Sentry.capture_exception(ex)
  end

  def perform(id) = ...
end
```

- Опции — на класс; переопределить на вызов: `Worker.set(queue: :low).perform_async`.
- `queue` — можно динамически: `set(queue: user.vip? ? :vip : :default)`.
- `backtrace: true` сохраняет весь стек в Redis — на тысячах retry это мегабайты; лучше число строк или ловить в Sentry.
- `lock:` / `unique_for:` — только с `sidekiq-unique-jobs` или Enterprise.
- Глобально: `config/sidekiq.yml` — `:concurrency`, `:queues`, `:timeout`, `:max_retries`.

## Фраза для собеса

«`sidekiq_options` задаёт очередь и retry; `sidekiq_retry_in` — своя кривая и discard для безнадёжных ошибок; `retries_exhausted` — финальная обработка».
