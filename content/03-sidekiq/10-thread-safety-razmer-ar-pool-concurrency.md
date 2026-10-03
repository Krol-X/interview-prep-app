---
title: "Thread safety, размер AR pool ≥ concurrency"
hot: true
links:
  - { t: "Sidekiq wiki — Problems and Troubleshooting (connection pool)", u: "https://github.com/sidekiq/sidekiq/wiki/Problems-and-Troubleshooting" }
  - { t: "Rails Guides — Threading and Code Execution", u: "https://guides.rubyonrails.org/threading_and_code_execution.html" }
---
Sidekiq выполняет джобы в **потоках одного процесса**. Всё, что разделяется между потоками, должно быть thread-safe.

Опасно:
- Класс-переменные и константы-хеши, которые мутируются (`@@cache[key] = ...`, `CONFIG[:x] = ...`).
- Мемоизация на уровне класса (`def self.client = @client ||= Client.new`) — гонка при инициализации; чаще безобидно, но клиент должен быть сам thread-safe (Net::HTTP-инстанс — нет; Faraday с пулом — да).
- Глобальные объекты с состоянием: `Timecop`, `I18n.locale=` без блока (хотя он thread-local), `ENV[]=`.
- Гемы, не рассчитанные на потоки.

Безопасно: локальные переменные, ивары объекта, созданного в `perform`, `Concurrent::Map`, `Mutex`, `Thread.current[]`/`ActiveSupport::CurrentAttributes` (сбрасываются Sidekiq между джобами).

**Пул соединений**: каждый поток берёт соединение AR на время джоба.
```yaml
# database.yml
pool: <%= ENV.fetch("RAILS_MAX_THREADS", 10) %>   # ≥ sidekiq concurrency
```
Меньше → `ActiveRecord::ConnectionTimeoutError` под нагрузкой. Если джоб сам создаёт `Thread.new` — каждый потомок тоже возьмёт соединение (и надо `ActiveRecord::Base.connection_pool.with_connection`).

Redis-клиент Sidekiq — свой пул (`Sidekiq.redis { }`), размер = concurrency + 5.

Puma — та же история: `threads 5,5` → `pool: 5`.

## Фраза для собеса

«Джобы в потоках: никакого мутабельного состояния на уровне класса, а пул соединений БД — не меньше concurrency».
