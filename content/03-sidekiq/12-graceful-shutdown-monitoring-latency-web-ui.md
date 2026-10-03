---
title: "Graceful shutdown, мониторинг latency, Web UI"
hot: false
links:
  - { t: "Sidekiq wiki — Signals", u: "https://github.com/sidekiq/sidekiq/wiki/Signals" }
  - { t: "Sidekiq wiki — Monitoring", u: "https://github.com/sidekiq/sidekiq/wiki/Monitoring" }
---
**Shutdown**: `TERM` → Sidekiq перестаёт брать новые джобы, ждёт `-t 25` секунд (должно быть меньше, чем даёт оркестратор — Heroku 30 с, K8s `terminationGracePeriodSeconds`), недоделанные джобы **возвращает в очередь** (они выполнятся заново → идемпотентность). `TSTP` — «тихо» перестать брать джобы (перед деплоем), `TTIN` — дамп стеков потоков (зависло?).

**Web UI** (`/sidekiq`): очереди и их размер, retry/scheduled/dead с возможностью повторить/удалить, busy — что сейчас выполняется, история. Монтируется в routes, закрывать авторизацией (`authenticate :user, ->(u) { u.admin? }` или basic auth).

**Метрики, на которые смотреть**:
- **latency** очереди — сколько секунд ждёт старейший джоб (`Sidekiq::Queue.new("critical").latency`). Главная метрика: растёт → не хватает воркеров.
- размер retry и dead — рост = системная ошибка;
- busy / concurrency — утилизация;
- память процесса — пухнет → `MALLOC_ARENA_MAX=2`, jemalloc, `sidekiq-worker-killer`.
- Алерты: `sidekiq_alive`, Prometheus exporter, Datadog/NewRelic интеграции, Sentry на исключения.

Долгие джобы (> минут) — плохо: блокируют деплой, теряются при kill. Резать на батчи, прогресс сохранять.

## Фраза для собеса

«TERM — дождаться timeout и вернуть незавершённое в очередь; слежу за latency очередей и ростом retry/dead; UI закрыт авторизацией».
