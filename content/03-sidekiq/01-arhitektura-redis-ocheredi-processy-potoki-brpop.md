---
title: "Архитектура: Redis-очереди, процессы, потоки, BRPOP"
hot: false
links:
  - { t: "Sidekiq wiki — Getting Started", u: "https://github.com/sidekiq/sidekiq/wiki/Getting-Started" }
  - { t: "Sidekiq wiki — Advanced Options (concurrency)", u: "https://github.com/sidekiq/sidekiq/wiki/Advanced-Options" }
---
```
perform_async → JSON → Redis LPUSH queue:critical
                                   ↓
sidekiq process ──BRPOP queue:critical queue:default──→ thread pool (concurrency N)
                                                            └→ perform(*args)
```

- **Клиент** (Rails-процесс): сериализует `[класс, args, jid, enqueued_at…]` в JSON и кладёт в Redis-список. Это быстро — один `LPUSH`.
- **Сервер** (`bundle exec sidekiq`): процесс с пулом потоков (`-c 10`). Главный цикл делает блокирующий `BRPOP` по очередям в порядке приоритета, отдаёт джоб свободному потоку.
- Один процесс = один Ruby VM, GVL общий → потоки параллелят IO, не CPU. Для CPU — несколько процессов (`sidekiqswarm` в Enterprise или просто несколько systemd-юнитов).
- Поток держит AR-соединение из пула на время джоба → `pool >= concurrency` в `database.yml`.
- Redis — единственное состояние: очереди, retry/scheduled/dead sets (sorted sets по времени), статистика. Потеря Redis = потеря очереди (кроме Pro `super_fetch`).
- Scheduled/retry: отдельный поток-поллер каждые ~5 с переносит из sorted set в очередь, когда пришло время.

Сравнение: Laravel queue:work — один процесс = один воркер; в Sidekiq один процесс = N потоков.

## Фраза для собеса

«Клиент пушит JSON в Redis-список, сервер забирает BRPOP и раздаёт потокам; потоки шарят GVL и пул соединений, поэтому concurrency ограничен IO и размером пула».
