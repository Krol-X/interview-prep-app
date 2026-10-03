---
title: "Колбэки AR: порядок, `after_save` vs `after_commit`, `after_create_commit`"
hot: true
links:
  - { t: "Rails Guides — Active Record Callbacks", u: "https://guides.rubyonrails.org/active_record_callbacks.html" }
  - { t: "Rails Guides — Transaction Callbacks", u: "https://guides.rubyonrails.org/active_record_callbacks.html#transaction-callbacks" }
---
## Порядок при `save` новой записи

```
before_validation → after_validation
before_save → around_save
  before_create → around_create → [INSERT] → after_create
after_save
[COMMIT]
after_commit / after_rollback
```

Всё до `after_save` включительно выполняется **внутри транзакции**. `after_commit` — после неё.

## Почему это важно

```ruby
after_create :enqueue_job        # плохо
after_create_commit :enqueue_job # правильно

def enqueue_job
  ProcessWorker.perform_async(id)
end
```

С `after_create` джоб уходит в Redis до COMMIT. Воркер может взять его раньше, чем запись видна другим соединениям → `RecordNotFound`. С ретраями «само починится», и баг годами живёт незамеченным.

То же касается: отправки писем, HTTP-вызовов, пушей — любых побочных эффектов наружу.

## Особенности `after_commit`

- Срабатывает один раз на внешнюю транзакцию, даже если `save` вложен в `transaction do ... end`.
- Исключение внутри `after_commit` **не откатывает** транзакцию — она уже закоммичена. Оно логируется (или пробрасывается, зависит от версии/настройки).
- В тестах с транзакционными фикстурами `after_commit` раньше не вызывался; с Rails 5+ вызывается.

## Rails 7.2+

`config.active_job.enqueue_after_transaction_commit` — ActiveJob сам откладывает `perform_later` до коммита. Для нативного Sidekiq это не действует.

## Фраза для собеса

«Всё, что уходит за пределы БД — в `after_commit`. Всё, что меняет саму запись — в `before_*`».
