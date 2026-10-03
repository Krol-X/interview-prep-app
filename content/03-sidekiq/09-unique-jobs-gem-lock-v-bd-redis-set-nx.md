---
title: "Unique jobs (gem / lock в БД / Redis `SET NX`)"
hot: true
links:
  - { t: "sidekiq-unique-jobs", u: "https://github.com/mhenrixon/sidekiq-unique-jobs" }
  - { t: "Redis — SET NX", u: "https://redis.io/docs/latest/commands/set/" }
---
Задача: «не более одного джоба на withdrawal #5 одновременно». OSS Sidekiq этого не делает (в Enterprise — `unique_for:`).

**Gem sidekiq-unique-jobs**
```ruby
sidekiq_options lock: :until_executed, on_conflict: :log, lock_args_method: ->(args) { [args.first] }
```
Стратегии: `until_executing` (пока не начался), `until_executed` (пока не закончился), `while_executing` (один одновременно, остальные ждут). Удобно, но сложная конфигурация и свои баги при падениях Redis.

**Redis lock руками**
```ruby
def perform(id)
  key = "lock:withdrawal:#{id}"
  return unless Sidekiq.redis { |r| r.set(key, jid, nx: true, ex: 600) }   # NX — только если нет
  begin
    ...
  ensure
    Sidekiq.redis { |r| r.del(key) if r.get(key) == jid }   # снять только свой
  end
end
```
TTL обязателен — иначе крэш оставит вечный lock. Снять «только свой» корректно через Lua, но для практики достаточно.

**Lock в БД** — самый надёжный для денег: статус-машина с атомарным переходом `UPDATE ... WHERE status='pending'` (rowcount 1 — я владелец) или `SELECT ... FOR UPDATE SKIP LOCKED`. Переживает потерю Redis.

Дедуп на enqueue (не ставить второй) и уникальность выполнения — разные задачи; для денег нужна вторая.

## Фраза для собеса

«Для критичного — атомарный переход статуса в БД; для остального `SET NX` с TTL или sidekiq-unique-jobs».
