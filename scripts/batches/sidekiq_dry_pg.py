W = "https://github.com/sidekiq/sidekiq/wiki/"
D = "https://dry-rb.org/gems/"
P = "https://www.postgresql.org/docs/current/"
ITEMS = {
# ───────── Sidekiq ─────────
"03-sidekiq/01-arhitektura-redis-ocheredi-processy-potoki-brpop.md": ([
  ("Sidekiq wiki — Getting Started", W + "Getting-Started"),
  ("Sidekiq wiki — Advanced Options (concurrency)", W + "Advanced-Options"),
], """
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
"""),

"03-sidekiq/02-perform-async-perform-in-perform-at.md": ([
  ("Sidekiq wiki — Scheduled Jobs", W + "Scheduled-Jobs"),
], """
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
"""),

"03-sidekiq/03-argumenty-tolko-json-primitivy-peredavat-id.md": ([
  ("Sidekiq wiki — Best Practices (#1 Make your job parameters small and simple)", W + "Best-Practices"),
], """
Аргументы сериализуются в JSON. Проходят: строки, числа, `true/false/nil`, массивы и хеши из них. **Не проходят**: AR-модели, символы (станут строками), `Date/Time` (станут строками), `Struct`, любые объекты.

```ruby
perform_async(withdrawal)          # → "#<Withdrawal:0x...>" или хеш атрибутов — в perform придёт мусор
perform_async(withdrawal.id)       # правильно
perform_async(status: :sent)       # ключ станет "status", значение "sent"
perform_async(Time.now)            # строка; парсить в perform
```

Sidekiq 7 в strict-режиме (`Sidekiq.strict_args!`, по умолчанию в dev/test) бросает `ArgumentError` на неJSON-аргументы — ловится на раннем этапе.

Почему id, а не объект:
- объект устареет: между enqueue и perform запись могла измениться; воркер должен прочитать **актуальное** состояние;
- маленький payload — Redis и память;
- в perform делаем `Withdrawal.find(id)` и обрабатываем `RecordNotFound` (запись удалили — выйти без ретрая).

Внутри `perform` хеши приходят со **строковыми** ключами: `opts["fee"]`, не `opts[:fee]`. Удобно: `opts = opts.symbolize_keys` или kwargs не использовать вовсе.

ActiveJob решает это GlobalID (`gid://app/Withdrawal/5`), но та же суть — передаётся ссылка, объект грузится в джобе.

## Фраза для собеса

«Только JSON-примитивы и передаю id: воркер читает свежую запись, payload маленький, а strict_args ловит ошибки сразу».
"""),

"03-sidekiq/04-retry-eksponencialnyj-backoff-retry-set-dead-set.md": ([
  ("Sidekiq wiki — Error Handling", W + "Error-Handling"),
], """
Исключение из `perform` → джоб попадает в **retry set** (sorted set в Redis по времени следующей попытки).

- По умолчанию **25 попыток** с экспоненциальной задержкой: `(count⁴ + 15 + rand(10) × (count+1))` секунд ≈ 15 с, 30 с, 1.5 мин… итого ~21 день.
- После исчерпания → **dead set** («морг»): хранится до 6 месяцев / 10 000 джобов; можно повторить вручную из Web UI.
- `retry: false` — сразу в dead? Нет: сразу **отбрасывается** (в dead попадает только `retry: 0`… на самом деле `retry: false` — исключение логируется, джоб пропадает; `retry: 0` — в dead). Проверь в своей версии в UI.
- Своя кривая: `sidekiq_retry_in { |count, ex| 10 * (count + 1) }`; вернуть `:discard` или `:kill` (7+) — прекратить/в морг для конкретных ошибок.
- `sidekiq_retries_exhausted { |job, ex| ... }` — последняя попытка провалилась: пометить запись failed, уведомить.
- Retry — не «ещё раз через секунду»: первая повторная попытка почти сразу, поэтому джоб **обязан быть идемпотентным**.
- Исключения, которые нет смысла ретраить (`RecordNotFound`, невалидный адрес) — ловить и выходить, или `:discard`.

Ошибки не глотать: `rescue => e; log; end` делает джоб «успешным» — ни retry, ни алертов.

## Фраза для собеса

«Упал — в retry set с экспоненциальным backoff, 25 попыток за ~3 недели, потом dead set; кривую и исчерпание настраиваю, безнадёжные ошибки не ретраю».
"""),

"03-sidekiq/06-after-commit-dlya-enqueue-ne-after-create.md": ([
  ("Sidekiq wiki — Problems and Troubleshooting (Cannot find ModelName with ID=12345)", W + "Problems-and-Troubleshooting"),
], """
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
"""),

"03-sidekiq/07-sidekiq-options-queue-retry-sidekiq-retry-in-sid.md": ([
  ("Sidekiq wiki — Advanced Options (Workers)", W + "Advanced-Options#workers"),
], """
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
"""),

"03-sidekiq/08-ocheredi-s-vesami-izolyaciya-kritichnyh-dzhobov.md": ([
  ("Sidekiq wiki — Advanced Options (Queues)", W + "Advanced-Options#queues"),
], """
```yaml
# config/sidekiq.yml
:concurrency: 10
:queues:
  - [critical, 6]     # вес: при выборе очереди critical проверяется в 6 раз чаще
  - [default, 3]
  - [low, 1]
```

Два режима:
- **Строгий приоритет** (`-q critical -q default`, без весов): `default` обрабатывается только когда `critical` пуст. Риск голодания low.
- **Веса** — вероятностная выборка; низкие очереди не голодают, но и не гарантирован порядок.

Веса не дают изоляции: 10 потоков заняты медленными `default`-джобами — `critical` ждёт свободного потока. Для **гарантии** — отдельный процесс только под критичную очередь:

```
sidekiq -q critical -c 5         # процесс 1: только деньги
sidekiq -q default -q low -c 10  # процесс 2: всё остальное
```

Принципы:
- Деньги / выводы — своя очередь и свой процесс; письма и отчёты не должны их блокировать.
- Медленные и тяжёлые (экспорт, импорт) — отдельная очередь с малым concurrency.
- Имена по SLA (`critical/default/low`) или по домену (`payouts/mailers`) — главное, последовательно.
- Мониторить **latency** очереди (возраст старейшего джоба), а не только размер.
- Очередь, в которую никто не слушает, — тихо копится. `Sidekiq::Queue.all`.

## Фраза для собеса

«Веса против голодания, но изоляция — только отдельным процессом на критичную очередь; слежу за latency, а не за размером».
"""),

"03-sidekiq/09-unique-jobs-gem-lock-v-bd-redis-set-nx.md": ([
  ("sidekiq-unique-jobs", "https://github.com/mhenrixon/sidekiq-unique-jobs"),
  ("Redis — SET NX", "https://redis.io/docs/latest/commands/set/"),
], """
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
"""),

"03-sidekiq/10-thread-safety-razmer-ar-pool-concurrency.md": ([
  ("Sidekiq wiki — Problems and Troubleshooting (connection pool)", W + "Problems-and-Troubleshooting"),
  ("Rails Guides — Threading and Code Execution", "https://guides.rubyonrails.org/threading_and_code_execution.html"),
], """
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
"""),

"03-sidekiq/11-testirovanie-fake-inline-jobs-drain-rspec-sideki.md": ([
  ("Sidekiq wiki — Testing", W + "Testing"),
  ("rspec-sidekiq", "https://github.com/wspurgin/rspec-sidekiq"),
], """
```ruby
# spec/rails_helper.rb
require "sidekiq/testing"
Sidekiq::Testing.fake!        # по умолчанию: джобы складываются в массив, не выполняются
RSpec.configure { |c| c.before { Sidekiq::Worker.clear_all } }
```

```ruby
it "enqueues processing after commit" do
  expect { create(:withdrawal) }
    .to change(ProcessWithdrawalWorker.jobs, :size).by(1)
  expect(ProcessWithdrawalWorker.jobs.last["args"]).to eq([Withdrawal.last.id])
end

it "processes" do
  create(:withdrawal)
  ProcessWithdrawalWorker.drain          # выполнить всё накопленное этого класса
  # Sidekiq::Worker.drain_all — все классы, включая порождённые
  expect(Withdrawal.last).to be_sent
end

it "runs perform directly" do
  ProcessWithdrawalWorker.new.perform(withdrawal.id)   # юнит-тест логики, без Redis
end

Sidekiq::Testing.inline! do             # выполнять сразу при perform_async
  create(:withdrawal)                   # осторожно: внутри транзакции запись «не видна» — fake! надёжнее
end
```

С `rspec-sidekiq`: `expect(Worker).to have_enqueued_sidekiq_job(id).in(5.minutes).on("critical")`.

Что тестировать: 1) что джоб ставится в нужный момент с нужными аргументами (после коммита!), 2) логику `perform` напрямую, 3) идемпотентность — вызвать `perform` дважды, результат один, 4) исчерпание ретраев — вызвать блок `sidekiq_retries_exhausted_block`.

ActiveJob: `have_enqueued_job`, `perform_enqueued_jobs { }`, `ActiveJob::Base.queue_adapter = :test`.

## Фраза для собеса

«`fake!` + `.jobs` для проверки постановки, `drain` или прямой `perform` для логики, второй вызов `perform` — для идемпотентности».
"""),

"03-sidekiq/12-graceful-shutdown-monitoring-latency-web-ui.md": ([
  ("Sidekiq wiki — Signals", W + "Signals"),
  ("Sidekiq wiki — Monitoring", W + "Monitoring"),
], """
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
"""),

"03-sidekiq/13-vypolnit-zadanie-iz-sidekiq-md.md": ([
  ("Sidekiq README", "https://github.com/sidekiq/sidekiq"),
], """
Практика на 1.5–2 часа, без Rails. Проверяет всё, что выше.

**Сетап**: `docker run -p 6379:6379 redis`, Gemfile с `sidekiq`, `redis`, `rspec`.

**Воркер** `BroadcastTxWorker.perform(withdrawal_id)`:
- состояние в Redis-хеше `withdrawal:<id>` (`status`, `txid`);
- `fake_broadcast` — спит 0.5 с, в 30% случаев бросает `Timeout::Error`, иначе возвращает hex-txid;
- идемпотентность: `status == sent` → выход;
- атомарный захват `pending → processing` через `SET NX` на lock-ключ или Lua — и комментарий, почему `HGET`+`HSET` — гонка;
- `Timeout::Error` не глотать — пусть ретраит; `retry: 5`, свой `sidekiq_retry_in`;
- `sidekiq_retries_exhausted` → `status = failed`.

**Нагрузка** `enqueue.rb`: 20 выводов, каждый джоб поставить **дважды** (дабл-клик). После прогона — ровно один txid на каждый `sent`.

**Запуск**: `bundle exec sidekiq -r ./worker.rb -c 5`, Web UI через `rackup` с `Sidekiq::Web` — посмотреть retry set вживую.

**Тесты** (`Sidekiq::Testing.fake!`): джоб ставится; повторный `perform` для `sent` ничего не меняет.

Критерий «сделано»: можешь объяснить, что произойдёт, если убить процесс посреди `fake_broadcast`.
"""),

# ───────── dry-rb ─────────
"04-dry-rb/01-zachem-yavnyj-potok-oshibok-vmesto-isklyuchenij-.md": ([
  ("dry-rb — dry-monads (Introduction)", D + "dry-monads/"),
  ("Railway Oriented Programming (Scott Wlaschin)", "https://fsharpforfunandprofit.com/rop/"),
], """
Проблема исключений для бизнес-ошибок: невидимы в сигнатуре (`create_withdrawal` может бросить что угодно), ломают поток управления, дороги, провоцируют `rescue => e` «на всякий случай».

Явный результат — функция **всегда возвращает** объект, который либо `Success(value)`, либо `Failure(error)`:

```ruby
def call(params)
  Success(params)
    .bind { validate(_1) }      # Success → идём дальше; Failure → проскакиваем до конца
    .bind { debit(_1) }
    .bind { enqueue(_1) }
end

case CreateWithdrawal.new.call(params)
in Success(withdrawal) then render json: withdrawal
in Failure[:insufficient_funds, msg] then render json: { error: msg }, status: 422
in Failure[:invalid, errors] then render json: errors, status: 400
end
```

Плюсы: ошибки — часть контракта и видны в коде; все ветки обрабатываются (pattern matching без `else` упадёт на новом коде ошибки); композиция шагов — «рельсы» (Railway): успех едет по одной, ошибка переводится на другую и доезжает до конца без `if`.

Исключения остаются для **неожиданного** (сеть упала, баг) — их не превращают в Failure повсеместно.

Когда не надо: CRUD без ветвлений, маленький скрипт — `Result` будет церемонией.

## Фраза для собеса

«Бизнес-ошибки — это ожидаемые исходы, им место в возвращаемом значении, а не в исключениях; Result делает их явными и композируемыми».
"""),

"04-dry-rb/02-dry-monads-result-success-failure-bind-fmap-valu.md": ([
  ("dry-monads — Result", D + "dry-monads/1.6/result/"),
], """
```ruby
require "dry/monads"
include Dry::Monads[:result]

ok  = Success(42)
err = Failure(:not_found)              # любое значение: символ, строка, массив [:code, msg], объект

ok.success?  / ok.failure?
ok.value!                              # 42; на Failure — исключение UnwrapError
err.failure                            # :not_found
ok.value_or(0)                         # 42; у Failure вернёт 0

ok.fmap { _1 * 2 }                     # Success(84) — функция возвращает голое значение
ok.bind { |v| v > 0 ? Success(v) : Failure(:neg) }   # функция возвращает Result (можно «переключить рельсу»)
err.fmap { _1 * 2 }                    # Failure(:not_found) — блок не выполняется

err.or { |e| Success(default) }        # обработать ошибку, вернуть Result
err.or(Success(0))
ok.either(->(v) { ... }, ->(e) { ... })  # обе ветки
ok.to_maybe                            # Some(42)
Success(nil)                           # легально, но подозрительно
```

- `fmap` — map для успеха; `bind` (= `>>` / `flat_map`) — цепочка функций, возвращающих Result.
- `Failure` без `include Dry::Monads[:result]` в классе — не найдётся; включай модуль там, где используешь.
- Конвенция для ошибки: `Failure[:code, payload]` — удобно матчить. Или объект-ошибка с `#message`.
- `Try` оборачивает исключения в Result; `Task` — асинхронность; `List`.

## Фраза для собеса

«`Success/Failure`, `fmap` для чистой функции, `bind` для шага, который сам может упасть; достаю через pattern matching или `value_or`, не `value!`».
"""),

"04-dry-rb/03-dry-monads-maybe-some-none-kogda-vmesto-nil.md": ([
  ("dry-monads — Maybe", D + "dry-monads/1.6/maybe/"),
], """
```ruby
include Dry::Monads[:maybe]

Maybe(user)                      # Some(user) или None() если nil
Maybe(user).fmap(&:wallet).fmap(&:address).value_or("—")
# вместо user&.wallet&.address || "—"

Some(5).bind { |x| x > 3 ? Some(x) : None() }
None().value_or { compute_default }
Maybe(h[:a]).to_result(:missing_a)       # Maybe → Result с указанием ошибки
```

Чем отличается от `&.`: цепочка с `&.` работает, но результат — всё тот же `nil` без информации; `Maybe` — явный тип «может отсутствовать», который нельзя случайно передать дальше как значение, и который конвертируется в `Result` с кодом ошибки.

Когда: возвращаемое значение функции, где отсутствие — нормальный исход (`find_rate(pair) → Maybe`), и когда эту «пустоту» дальше надо обрабатывать разными способами. Когда нет: `&.` достаточно; внутри простого метода; в AR-коде (`find_by` возвращает nil, и все к этому привыкли).

`Some(nil)` — невозможно (станет None). `Maybe(false)` — `Some(false)`: `Maybe` только про nil.

## Фраза для собеса

«`Maybe` — типизированный «может быть nil» с цепочкой `fmap` и переводом в `Result`; использую на границах, а не вместо каждого `&.`».
"""),

"04-dry-rb/04-dry-monads-do-notation-yield-vnutri-call-chitat-.md": ([
  ("dry-monads — Do notation", D + "dry-monads/1.6/do-notation/"),
], """
Цепочки `bind { bind { bind } }` вложены и плохо читаются. Do-notation делает их линейными:

```ruby
class CreateWithdrawal
  include Dry::Monads[:result, :do]

  def call(params)
    attrs  = yield validate(params)        # если Failure — метод НЕМЕДЛЕННО вернёт этот Failure
    wallet = yield find_wallet(attrs[:user_id])
    w      = yield debit_and_create(wallet, attrs)
    yield enqueue(w)
    Success(w)
  end

  private
  def validate(p)  = Contract.new.call(p).to_monad      # Success(hash) / Failure(result)
  def find_wallet(id) = Maybe(Wallet.find_by(id:)).to_result(:wallet_not_found)
  ...
end
```

- `yield` здесь — не блок метода: `include Dry::Monads[:do]` оборачивает `call` (и любые методы, объявленные после) так, что `yield Failure` прерывает выполнение и возвращает Failure наружу. `yield Success(v)` возвращает `v`.
- Читается как обычный императивный код: «получи, получи, получи, верни».
- Работает с `Result`, `Maybe`, `Try`, `Validation`.
- Если нужен Do только в конкретных методах: `include Dry::Monads::Do.for(:call, :other)`.
- Ловушка: внутри `transaction do ... end` блок `yield Failure` вернёт из метода, но блок транзакции при этом закоммитится — Failure не исключение. Решение: `transaction { ... }.tap { raise Rollback if failure }` или `dry-monads` + `raise ActiveRecord::Rollback` вручную, либо `dry-transaction`/`dry-operation` с поддержкой транзакций.

## Фраза для собеса

«Do-notation: `yield result` разворачивает Success или досрочно возвращает Failure — цепочка шагов читается линейно; помню про транзакции».
"""),

"04-dry-rb/05-dry-monads-try-dlya-oborachivaniya-isklyuchenij.md": ([
  ("dry-monads — Try", D + "dry-monads/1.6/try/"),
], """
`Try` — мост между миром исключений (гемы, HTTP, парсинг) и миром Result.

```ruby
include Dry::Monads[:try, :result]

Try { JSON.parse(body) }                        # Value(hash) или Error(JSON::ParserError)
Try[JSON::ParserError, KeyError] { ... }        # ловить только перечисленные; остальные пролетят
  .to_result                                    # → Success / Failure(exception)
  .or { |e| Failure[:bad_json, e.message] }

Try { api.broadcast(hex) }.to_result.fmap { |txid| txid.downcase }
```

- Без списка классов `Try` ловит `StandardError` — не `Exception`.
- `Value`/`Error` — свои обёртки; обычно сразу `.to_result` или `.to_maybe`.
- Полезно на границах: в адаптере к внешнему API, при парсинге ввода, при работе с гемом, который кидает.
- Не стоит оборачивать в `Try` всё подряд — баги (NoMethodError) должны падать и попадать в Sentry, а не превращаться в `Failure`, который кто-то проигнорирует. Перечисляй ожидаемые классы явно.

## Фраза для собеса

«`Try` ловит перечисленные исключения на границе и превращает в Result; баги не оборачиваю — им место в мониторинге».
"""),

"04-dry-rb/06-pattern-matching-na-success-value-failure-code-m.md": ([
  ("dry-monads — Pattern matching", D + "dry-monads/1.6/pattern-matching/"),
], """
`Success`/`Failure` реализуют `deconstruct`/`deconstruct_keys`, поэтому матчатся в `case/in`:

```ruby
case CreateWithdrawal.new.call(params)
in Success(Withdrawal => w)                 # Success с проверкой класса
  render json: w, status: :created
in Failure[:insufficient_funds, need, have] # Failure с массивом — деструктуризация по позициям
  render json: { error: "need #{need}, have #{have}" }, status: 422
in Failure[:validation, errors]
  render json: { errors: }, status: 400
in Failure(ActiveRecord::RecordNotFound)    # Failure с объектом-исключением
  head :not_found
in Failure(err)                             # всё остальное
  Rails.error.report(err); head :internal_server_error
end
```

- `Success(x)` — круглые скобки: одно значение. `Failure[:code, *rest]` — квадратные: деструктуризация массива. Для хеша: `Success({ txid:, fee: })`.
- Без `else` непокрытый случай → `NoMatchingPatternError`. Это хорошо: добавил новый код ошибки в сервис — тесты контроллера упадут, пока не обработаешь.
- Конвенция `Failure[:symbol, payload]` делает ветки читаемыми и greppable.
- Матчить можно и на `Maybe`: `in Some(v)` / `in None`.

## Фраза для собеса

«Результат разбираю `case/in`: `Success(v)` и `Failure[:code, data]`; отсутствие `else` заставляет обработать каждый код ошибки».
"""),

"04-dry-rb/07-dry-validation-contract-params-do-end-rule-x-res.md": ([
  ("dry-validation — Contracts", D + "dry-validation/1.10/"),
  ("dry-validation — Rules", D + "dry-validation/1.10/rules/"),
], """
```ruby
class WithdrawalContract < Dry::Validation::Contract
  params do                                      # схема: типы, приведение, обязательность
    required(:to_address).filled(:string)
    required(:amount_sat).filled(:integer, gt?: 0)
    optional(:email).maybe(:string, format?: /@/)
    required(:kyc).filled(:bool, eql?: true)
  end

  rule(:to_address) do                           # правила: бизнес-логика, кросс-полевые проверки
    key.failure("invalid signet address") unless Bitcoin.valid_address?(value)
  end

  rule(:amount_sat, :to_address) do
    key(:amount_sat).failure("exceeds limit") if values[:amount_sat] > MAX && values[:to_address].start_with?("tb1p")
  end
end

result = WithdrawalContract.new.call(params.to_unsafe_h)
result.success?         # true/false
result.to_h             # приведённые значения ("5" → 5)
result.errors.to_h      # { to_address: ["invalid signet address"] }
result.to_monad         # Success(values) / Failure(result) — для Do-notation
```

- `params` — для строк из HTTP (приводит типы); `json` — для JSON (строже); `schema` — без приведения.
- `rule` выполняется только если схема для этих ключей прошла — не надо проверять на nil.
- Зависимости в контракт: `option :repo` (dry-initializer внутри) — для проверок через БД.
- Сообщения — в YAML с i18n, или строкой на месте.
- Отличие от AR-валидаций: контракт не привязан к модели, проверяет **вход** (форма/API), а не состояние записи; один вход — один контракт.

## Фраза для собеса

«`params do` описывает форму и типы входа, `rule` — бизнес-правила; результат даёт приведённые значения и ошибки по ключам и конвертируется в Result».
"""),

"04-dry-rb/08-dry-schema-vs-dry-validation-raznica.md": ([
  ("dry-schema", D + "dry-schema/"),
  ("dry-validation — Introduction", D + "dry-validation/"),
], """
**dry-schema** — только структура: ключи, типы, приведение, простые предикаты (`filled?`, `gt?`, `format?`). Быстрый, без состояния, без доступа к другим полям.

```ruby
Schema = Dry::Schema.Params { required(:amount).filled(:integer, gt?: 0) }
Schema.call("amount" => "5").to_h   # { amount: 5 }
```

**dry-validation** — надстройка: `Contract` = схема (`params do`) **+ `rule`** с произвольной логикой, кросс-полевыми проверками, внешними зависимостями (репозиторий, текущий пользователь), макросами.

Когда что:
- Проверить форму JSON/конфига/ENV, параметров джоба → `dry-schema` достаточно.
- Валидация ввода с бизнес-правилами («адрес существует в сети», «сумма ≤ лимита пользователя») → `dry-validation`.

Оба отдают `result.errors.to_h` в одном формате; `Contract` внутри использует `dry-schema`, так что переход — добавить `rule`.

## Фраза для собеса

«Schema — форма и типы, Validation — schema плюс rules с бизнес-логикой и зависимостями».
"""),

"04-dry-rb/09-dry-struct-dry-types-tipizirovannye-value-object.md": ([
  ("dry-struct", D + "dry-struct/"),
  ("dry-types — Built-in types", D + "dry-types/1.7/built-in-types/"),
], """
```ruby
module Types
  include Dry.Types()
  SatAmount = Integer.constrained(gteq: 0)
  Address   = String.constrained(format: /\\A(tb1|2|m|n)/)
  Status    = String.enum("pending", "sent", "failed")
end

class Utxo < Dry::Struct
  attribute :txid,  Types::Strict::String
  attribute :vout,  Types::Strict::Integer
  attribute :value, Types::SatAmount
  attribute? :address, Types::Address.optional      # attribute? — ключ может отсутствовать; .optional — может быть nil
end

u = Utxo.new(txid: "ab..", vout: 0, value: 5000)
u.value                     # 5000
Utxo.new(vout: "0")         # Dry::Struct::Error — Strict не приводит типы
u.new(value: 1)             # копия с изменением (иммутабельно)
u.to_h
```

- `Strict::*` — проверка без приведения; `Coercible::*` — `"5"` → 5; `Params::*` — приведение как из HTTP; `JSON::*`.
- `.optional` = `nil` допустим; `.default(0)`; `.constrained(...)`; `.enum(...)`; `Array.of(Utxo)`; `Hash.schema(...)`.
- `Dry::Struct` — иммутабельный value object с валидацией типов на входе. Сравни с `Data.define` — тот без типов; со `Struct` — тот мутабельный.
- `transform_keys(&:to_sym)` — принимать строковые ключи из JSON.

Где уместно: DTO из внешнего API (ответ mempool), конфиг, доменные значения (Money, Address). Не вместо AR-моделей.

## Фраза для собеса

«`Dry::Struct` — иммутабельный объект с типизированными атрибутами из dry-types; падает на входе, если данные не те, а не где-то глубже».
"""),

"04-dry-rb/10-dry-initializer-option-x-param-y-alternativa-ini.md": ([
  ("dry-initializer", D + "dry-initializer/"),
], """
Убирает бойлерплейт `def initialize(a, b:, c: 1); @a = a; ...; end` + `attr_reader`.

```ruby
class CreateWithdrawal
  extend Dry::Initializer

  param  :user                                # позиционный, обязательный
  option :params                              # keyword, обязательный
  option :fee_sat,   default: -> { 1000 }      # дефолт — proc
  option :node,      default: -> { BitcoinNode.new }, reader: :private
  option :amount,    type: Dry::Types["coercible.integer"]   # приведение/проверка
  option :notify,    optional: true           # nil допустим, без дефолта
end

CreateWithdrawal.new(user, params: p).call
```

- Генерирует `initialize` и ридеры (публичные по умолчанию; `reader: :private` / `false`).
- `default:` всегда proc — вычисляется на каждом вызове (нет общего мутабельного дефолта).
- `type:` — любой dry-type или объект с `call`.
- `as:` — переименовать ивар; `optional: true` vs `default:`.
- В `dry-validation` Contract и `dry-operation` уже встроен (`option :repo`).

Альтернативы: `Data.define` для чистых значений; обычный `initialize` с kwargs для 1–2 аргументов — не тащить гем ради этого.

## Фраза для собеса

«`option`/`param` вместо ручного initialize с дефолтами и типами; удобно для сервисов с инъекцией зависимостей».
"""),

"04-dry-rb/11-dry-container-dry-auto-inject-di-odna-fraza.md": ([
  ("dry-container", D + "dry-container/"),
  ("dry-auto_inject", D + "dry-auto_inject/"),
  ("dry-system", D + "dry-system/"),
], """
**Контейнер** — реестр зависимостей по ключам:
```ruby
class App < Dry::Container
  register(:node)   { BitcoinNode.new(ENV.fetch("NODE_URL")) }
  register(:mempool, memoize: true) { MempoolClient.new }
end
App[:node]
```

**auto_inject** — автоматически передаёт зависимости в конструктор:
```ruby
Import = Dry::AutoInject(App)

class CreateWithdrawal
  include Import[:node, :mempool]     # добавит kwargs node:, mempool: с дефолтами из контейнера
  def call(...) = node.broadcast(...)
end

CreateWithdrawal.new                      # зависимости из контейнера
CreateWithdrawal.new(node: FakeNode.new)  # подмена в тесте — без моков и stub'ов классов
```

Зачем: явные зависимости вместо `BitcoinNode.new` внутри метода (который нельзя подменить без `allow(BitcoinNode).to receive(:new)`), единая точка конфигурации, ленивая инициализация.

**dry-system** — надстройка: автозагрузка компонентов из папок, провайдеры (`:db`, `:redis`), bootable-зависимости. В Rails обычно избыточно — Zeitwerk и инициализаторы уже есть; уместно в Hanami/roda-проектах.

## Фраза для собеса

«Контейнер — реестр зависимостей, auto_inject — подставляет их в конструктор; тесты подменяют через kwargs без моков классов».
"""),

"04-dry-rb/12-dry-transaction-dry-operation-pajplajn-shagov-od.md": ([
  ("dry-operation", D + "dry-operation/"),
  ("dry-transaction (legacy)", D + "dry-transaction/"),
], """
Формализованный сервис из шагов, где каждый возвращает `Result`, и Failure останавливает цепочку.

**dry-operation** (актуальный, 2024+):
```ruby
class CreateWithdrawal < Dry::Operation
  include Dry::Operation::Extensions::ActiveRecord     # transaction { } с откатом на Failure

  def call(input)
    attrs  = step validate(input)
    w = transaction do
      wallet = step lock_wallet(attrs)
      step debit(wallet, attrs)
      step create_record(wallet, attrs)
    end
    step enqueue(w)                                    # вне транзакции — после коммита
    w
  end

  private
  def validate(i) = WithdrawalContract.new.call(i).to_monad
  ...
end
```

`step` ≈ `yield` из Do-notation, но операция ещё умеет: оборачивать шаги в транзакцию с автооткатом при Failure (главная боль Do + AR), хуки `on_failure`, расширения для Sequel/ROM.

**dry-transaction** — предшественник с DSL `step :validate; map :x; tee :log`. Deprecated в пользу dry-operation; встречается в старых проектах — узнавать.

Альтернативы вне dry: `interactor` (context-объект, `rollback`), `trailblazer-operation` (тяжёлый), `ActiveInteraction`. Все про одно: явные шаги + явный результат.

## Фраза для собеса

«dry-operation — сервис из `step`-ов с Result и транзакцией, которая откатывается на Failure; dry-transaction — его устаревший предок».
"""),

"04-dry-rb/13-napisat-servis-createwithdrawal-na-do-result-s-3.md": ([
  ("dry-monads — Do notation", D + "dry-monads/1.6/do-notation/"),
], """
Упражнение на 40 минут. Напиши и прогони в консоли/спеке:

```ruby
class CreateWithdrawal
  include Dry::Monads[:result, :do]

  def initialize(contract: WithdrawalContract.new, fee_sat: 1_000)
    @contract, @fee_sat = contract, fee_sat
  end

  def call(user, raw_params)
    attrs = yield validate(raw_params)
    w     = yield debit(user, attrs)
    yield enqueue(w)
    Success(w)
  end

  private

  def validate(raw)
    r = @contract.call(raw)
    r.success? ? Success(r.to_h) : Failure[:validation, r.errors.to_h]
  end

  def debit(user, attrs)
    total = attrs[:amount_sat] + @fee_sat
    ActiveRecord::Base.transaction do
      wallet = user.wallet.lock!
      return Failure[:insufficient_funds, total, wallet.balance_sat] if wallet.balance_sat < total
      wallet.decrement!(:balance_sat, total)
      Success(wallet.withdrawals.create!(attrs.merge(fee_sat: @fee_sat, status: :pending)))
    end
  end

  def enqueue(w)
    ProcessWithdrawalWorker.perform_async(w.id)
    Success(w)
  rescue Redis::BaseError => e
    Failure[:queue_unavailable, e.message]
  end
end
```

Проверь себя:
1. Что вернёт `call`, если контракт не прошёл? Выполнится ли `debit`?
2. `return Failure` внутри `transaction do` — закоммитится ли транзакция? (Да — Failure не исключение. Здесь ок, потому что до списания; а если бы после?)
3. Напиши спек: три кейса через `case/in`.
4. Замени `yield`/Do на `dry-operation` со `step` и `transaction` — что стало проще?

Цель — не гем, а уметь обсуждать: где границы транзакции, когда enqueue, как тестировать без БД (инъекция контракта).
"""),

"04-dry-rb/14-umet-skazat-kogda-dry-rb-overkill.md": ([
  ("dry-rb", "https://dry-rb.org/"),
], """
Честный ответ ценится больше энтузиазма.

**Overkill**, когда:
- CRUD-приложение, где сценарий = «валидация модели → save». AR-валидации и `save!` достаточно, Result ничего не добавит.
- Команда не знает dry — ввод `yield`-магии Do-notation в чужой код создаёт барьер; конвенции Rails уже всем известны.
- Один-два сервиса. Ради них тащить 4 гема и слой типов — церемония.
- Нужно быстро: прототип, MVP, тестовое задание на вечер (но показать, что знаешь — плюс).
- Для dry-struct там, где хватит `Data.define`; для dry-initializer — где 2 аргумента.

**Оправдано**, когда:
- Много многошаговых сценариев с ветвлениями по ошибкам (платежи, выводы, обмены) — Result + pattern matching убирают вложенные `if`/исключения для потока.
- Вход из нескольких источников (API, формы, джобы) с разными правилами — контракты отделяют валидацию ввода от модели.
- Нужны строгие границы с внешним миром (DTO с типами из ответов нод/бирж).
- Проект без Rails (Hanami, roda) — dry там стандарт.

Компромисс в Rails-проекте: Result-объект свой (`Data.define(:ok?, :value, :error)`) или только `dry-monads` — без struct/container/system.

## Фраза для собеса

«dry-rb окупается на сложных сценариях и границах с внешним миром; в простом CRUD это лишний слой, и я бы начал с одних монад».
"""),

# ───────── PostgreSQL ─────────
"05-postgresql/01-indeksy-b-tree-unikalnye-sostavnye-poryadok-kolo.md": ([
  ("PostgreSQL docs — Indexes", P + "indexes.html"),
  ("Use The Index, Luke", "https://use-the-index-luke.com/"),
], """
**B-tree** — дефолт, для `=`, `<`, `>`, `BETWEEN`, `IN`, `ORDER BY`, `LIKE 'abc%'` (префикс). Не для `LIKE '%abc'`, не для функций над колонкой без функционального индекса.

```sql
CREATE INDEX idx ON withdrawals (wallet_id);
CREATE UNIQUE INDEX ON wallets (user_id);                      -- уникальность = защита от гонок
CREATE INDEX ON withdrawals (wallet_id, created_at DESC);       -- составной
CREATE INDEX ON withdrawals (status) WHERE status = 'pending';  -- partial: маленький, под конкретный запрос
CREATE INDEX ON users (lower(email));                           -- функциональный
```

**Порядок колонок в составном** — leftmost prefix: индекс `(a, b)` работает для `WHERE a=?` и `WHERE a=? AND b=?`, но **не** для `WHERE b=?`. Первой — колонка с `=`, потом диапазон/сортировка. `(wallet_id, created_at)` закроет «выводы кошелька, свежие сверху».

- Индекс ускоряет чтение, замедляет запись и занимает место. Не индексировать всё.
- FK-колонки Rails **не** индексирует автоматически (кроме `references` в миграции — тот ставит).
- Низкая селективность (булев флаг) — обычный индекс бесполезен, partial — полезен.
- Covering: `INCLUDE (amount)` — index-only scan без похода в таблицу.
- Другие типы: GIN (jsonb, массивы, full-text), GiST (геометрия, диапазоны), BRIN (огромные append-only по времени), Hash (только `=`, редко).
- `pg_stat_user_indexes` — неиспользуемые индексы; `REINDEX CONCURRENTLY` при раздувании.

## Фраза для собеса

«B-tree под равенство и диапазоны, в составном первой — колонка с равенством, уникальные — для инвариантов; partial — для статусов».
"""),

"05-postgresql/02-explain-analyze-prochitat-seq-scan-vs-index-scan.md": ([
  ("PostgreSQL docs — Using EXPLAIN", P + "using-explain.html"),
  ("explain.dalibo.com — визуализатор", "https://explain.dalibo.com/"),
], """
```sql
EXPLAIN ANALYZE SELECT * FROM withdrawals WHERE wallet_id = 5 ORDER BY created_at DESC LIMIT 20;
```
`EXPLAIN` — план без выполнения (оценки). `ANALYZE` — выполняет и показывает реальное время/строки. `(ANALYZE, BUFFERS)` — ещё и страницы диска/кэша. В Rails: `Withdrawal.where(...).explain(:analyze)`.

Читать **изнутри наружу**, снизу вверх:
```
Limit (actual time=0.05..0.09 rows=20 loops=1)
  -> Index Scan Backward using idx_w_wallet_created on withdrawals
       Index Cond: (wallet_id = 5)
```

| Узел | Что значит |
|---|---|
| **Seq Scan** | читает всю таблицу. Норма для маленьких таблиц или выборки большой доли строк; беда на миллионах |
| **Index Scan** | по индексу → за каждой строкой в таблицу. Хорош при малой выборке |
| **Index Only Scan** | всё из индекса, в таблицу не ходит (covering) |
| **Bitmap Heap Scan** | индекс → битовая карта страниц → таблица; средняя селективность |
| **Nested Loop / Hash Join / Merge Join** | способы join; Nested Loop с большим внутренним Seq Scan — красный флаг |
| **Sort** | сортировка в памяти/на диске (`external merge` — не хватило `work_mem`) |

На что смотреть: расхождение `rows=` оценки и факта (устарела статистика → `ANALYZE table`), Seq Scan там, где ждали индекс (нет индекса / функция над колонкой / тип не совпал / планировщик решил, что дешевле), `loops=` > 1 умножает время, `Filter:` с большим `Rows Removed` — индекс не покрывает условие.

## Фраза для собеса

«Читаю план изнутри, сравниваю оценку и факт строк, ищу Seq Scan и Rows Removed by Filter — это говорит, какого индекса не хватает».
"""),

"05-postgresql/03-tranzakcii-acid-urovni-izolyacii-read-committed-.md": ([
  ("PostgreSQL docs — Transaction Isolation", P + "transaction-iso.html"),
], """
**ACID**: Atomicity (всё или ничего), Consistency (constraints соблюдены), Isolation (параллельные транзакции не видят промежуточного), Durability (COMMIT → на диске, WAL).

Уровни изоляции в Postgres (MVCC — читатели не блокируют писателей):

| Уровень | Что видит транзакция | Аномалии |
|---|---|---|
| **Read Committed** (дефолт) | каждый запрос видит данные, закоммиченные к его началу | non-repeatable read, phantom: два SELECT в одной транзакции могут отличаться |
| **Repeatable Read** | снимок на момент первого запроса, всю транзакцию | нет phantom (в PG); при конфликте записи — `serialization failure`, надо повторить |
| **Serializable** | как будто транзакции шли по очереди | ловит все аномалии; больше откатов `40001` → retry-логика обязательна |

`Read Uncommitted` в PG = Read Committed.

Практика:
- Read Committed + явные блокировки (`FOR UPDATE`) или атомарные UPDATE — стандарт для денег. «Прочитал баланс, потом списал» на Read Committed — гонка, уровень изоляции сам по себе её не решает (на RR/Serializable второй упадёт, и его надо повторить).
- `ActiveRecord::Base.transaction(isolation: :serializable)` + `rescue ActiveRecord::SerializationFailure → retry`.
- Долгие транзакции мешают VACUUM и держат блокировки.
- `SELECT` без транзакции — autocommit, каждый запрос сам себе транзакция.

## Фраза для собеса

«По умолчанию Read Committed — каждый запрос видит свежий коммит; для инвариантов денег не полагаюсь на изоляцию, а беру FOR UPDATE или условный UPDATE».
"""),

"05-postgresql/05-check-constraints-not-null-fk-zaschita-invariant.md": ([
  ("PostgreSQL docs — Constraints", P + "ddl-constraints.html"),
], """
Валидации в Rails работают только через Rails: `update_all`, `insert_all`, консоль, другой сервис, гонка — всё обходит. Инварианты, которые **никогда** не должны нарушаться, — в БД.

```ruby
# миграция
t.bigint  :balance_sat, null: false, default: 0
t.string  :status,      null: false
t.references :wallet,   null: false, foreign_key: true
add_check_constraint :wallets, "balance_sat >= 0", name: "balance_non_negative"
add_check_constraint :withdrawals, "amount_sat > 0", name: "amount_positive"
add_check_constraint :withdrawals, "status IN ('pending','processing','sent','failed')", name: "status_valid"
add_index :withdrawals, :txid, unique: true, where: "txid IS NOT NULL"
add_exclusion_constraint ...  # пересечение интервалов (бронирования)
```

- **NOT NULL** — на всё, что обязательно. `nil` в коде — источник половины багов.
- **FK** (`foreign_key: true`) — нет осиротевших строк; `on_delete: :cascade/:nullify/:restrict`.
- **CHECK** — `balance >= 0` поймает любую гонку списания последним рубежом: `ActiveRecord::StatementInvalid` (`PG::CheckViolation`) вместо отрицательного баланса.
- **UNIQUE** — единственная настоящая защита от дублей.
- На живой таблице: `validate: false` / `NOT VALID` → проверить данные → `validate_constraint`, чтобы не держать lock.

Rails ловит нарушения как исключения: `RecordNotUnique`, `InvalidForeignKey`, `StatementInvalid`. Дублируй AR-валидацией для человекочитаемой ошибки, но источник правды — constraint.

## Фраза для собеса

«Валидации — для UX, constraints — для инвариантов: NOT NULL, FK, UNIQUE, CHECK на баланс и статус; они защищают и от гонок, и от чужого кода».
"""),

"05-postgresql/06-numeric-bigint-dlya-deneg-ne-float-real.md": ([
  ("PostgreSQL docs — Numeric Types", P + "datatype-numeric.html"),
], """
```sql
SELECT 0.1::float8 + 0.2::float8;        -- 0.30000000000000004
SELECT 0.1::numeric + 0.2::numeric;      -- 0.3
```

| Тип | Что это | Для денег |
|---|---|---|
| `real` / `float4`, `double precision` / `float8` | двоичная плавающая точка | **нет** — ошибки округления, `SUM` плывёт |
| `numeric(p, s)` / `decimal` | точная десятичная, произвольная точность | да: `numeric(16, 8)` для BTC, `numeric(12, 2)` для фиата |
| `bigint` | 64-бит целое | да: сатоши, центы. Самый быстрый и простой; так хранит сам Bitcoin |
| `integer` | 32-бит, до ~2.1 млрд | мало: 21 BTC в сатоши уже не влезет |
| `money` | legacy, зависит от locale | нет |

Выбор:
- Одна валюта с фиксированной дробностью (BTC → сат, USD → центы) — **bigint**. Арифметика целая, индексы компактны, нет вопросов округления. В Rails — `t.bigint :amount_sat`, в Ruby — Integer.
- Нужны дробные доли, разные валюты, проценты, курс — **numeric**. В Ruby приходит `BigDecimal`.
- `numeric` медленнее bigint и толще, но для OLTP это незаметно.

Курс USDT/BTC — `numeric(20, 10)`; комиссия 3% — считать в numeric/BigDecimal и округлять явно (`round(8, :down)`) в момент фиксации, а не хранить float.

## Фраза для собеса

«Деньги — bigint в минимальных единицах или numeric; float только в аналитике. В тестовом — сатоши целым числом».
"""),

"05-postgresql/07-jsonb-kogda-umestno-indeks-gin.md": ([
  ("PostgreSQL docs — JSON Types", P + "datatype-json.html"),
  ("PostgreSQL docs — jsonb indexing", P + "datatype-json.html#JSON-INDEXING"),
], """
`jsonb` — бинарный JSON с индексами и операторами (`json` — просто текст, почти не нужен).

```sql
ALTER TABLE withdrawals ADD COLUMN meta jsonb NOT NULL DEFAULT '{}';
SELECT * FROM withdrawals WHERE meta @> '{"source": "api"}';     -- содержит
SELECT meta->>'ip', meta->'utxos'->0 FROM withdrawals;           -- ->> текст, -> json
CREATE INDEX ON withdrawals USING gin (meta);                    -- для @>, ?, ?| ?&
CREATE INDEX ON withdrawals USING gin (meta jsonb_path_ops);     -- меньше, только @>
CREATE INDEX ON withdrawals ((meta->>'source'));                 -- b-tree на один ключ
```

Rails: `t.jsonb :meta`, атрибут — хеш со строковыми ключами; `where("meta @> ?", { source: "api" }.to_json)`; `store_accessor :meta, :source, :ip` — как обычные атрибуты.

**Уместно**: разнородные метаданные, сырые ответы внешних API (сохранить ответ ноды как есть), настройки с редкими ключами, схема которых меняется чаще миграций, логи событий.

**Не уместно**: то, по чему часто фильтруешь/джойнишь/агрегируешь, что участвует в constraints или FK, что имеет стабильную структуру — это колонки. JSONB не даёт NOT NULL на ключ, типизации, FK; обновление одного ключа переписывает всё значение (TOAST), статистика планировщика по ключам слабая.

Правило: если ключ стал нужен в `WHERE` в трёх местах — вынести в колонку.

## Фраза для собеса

«jsonb для схемы, которая меняется и редко фильтруется, с GIN-индексом под `@>`; всё, что в WHERE и constraints, — колонками».
"""),

"05-postgresql/08-advisory-locks-odna-fraza.md": ([
  ("PostgreSQL docs — Advisory Locks", P + "explicit-locking.html#ADVISORY-LOCKS"),
  ("gem with_advisory_lock", "https://github.com/ClosureTree/with_advisory_lock"),
], """
Блокировка **по произвольному числу/ключу**, не привязанная к строке. Приложение само договаривается, что значит ключ.

```sql
SELECT pg_advisory_lock(12345);          -- сессионная, ждёт; снять pg_advisory_unlock
SELECT pg_try_advisory_lock(12345);      -- не ждать, вернуть true/false
SELECT pg_advisory_xact_lock(12345);     -- транзакционная — снимется на COMMIT/ROLLBACK (безопаснее)
```

```ruby
Wallet.with_advisory_lock("sweep-utxos") { sweep! }     # gem; ключ хешируется в число
ActiveRecord::Base.connection.execute("SELECT pg_advisory_xact_lock(#{wallet.id})")
```

Когда: «только один процесс выполняет X» без строки, которую можно `FOR UPDATE` — cron-задача на нескольких серверах, пересчёт отчёта, миграция данных, единственный кошелёк-обменник, где все UTXO общие (твоё второе задание!). Замена Redis-lock, когда Redis нет или нужна транзакционность.

Нюансы: сессионный lock переживает транзакцию и теряется при обрыве соединения (хорошо); с PgBouncer в transaction-mode сессионные ломаются — брать `xact`. Ключ — bigint или пара int.

## Фраза для собеса

«Advisory lock — мьютекс в Postgres по числовому ключу; `xact`-вариант снимается с транзакцией, удобен для «один обработчик на ресурс без строки»».
"""),

"05-postgresql/09-migracii-bez-blokirovki-tablicy.md": ([
  ("strong_migrations — Checks", "https://github.com/ankane/strong_migrations#checks"),
  ("PostgreSQL docs — ALTER TABLE (notes on locks)", P + "sql-altertable.html#SQL-ALTERTABLE-NOTES"),
], """
`ALTER TABLE` берёт `ACCESS EXCLUSIVE` lock — на время операции таблица недоступна даже на чтение. Если перед ним стоит долгий `SELECT`, ALTER ждёт, а за ним выстраиваются все запросы → приложение встало.

Безопасно / опасно:

| Операция | Lock | Как безопасно |
|---|---|---|
| `add_column` nullable, с default (PG 11+) | мгновенно | ок |
| `add_column ... null: false` без default | переписывает таблицу | добавить nullable → бэкфилл → CHECK NOT VALID → validate → `change_column_null` |
| `add_index` | блокирует запись | `algorithm: :concurrently` + `disable_ddl_transaction!` |
| `add_foreign_key` | блокирует обе таблицы на валидацию | `validate: false` → `validate_foreign_key` отдельно |
| `add_check_constraint` | скан таблицы | `validate: false` → `validate_check_constraint` |
| `change_column` тип | переписывает | новая колонка → копировать батчами → переключить код → удалить старую |
| `rename_column` | быстро, но ломает работающий код | новая колонка + двойная запись, либо `alias_attribute`/`ignored_columns` в два деплоя |
| `remove_column` | быстро; старый код падает | сначала `self.ignored_columns += [...]`, деплой, потом удалить |
| бэкфилл `update_all` всей таблицы | долгая транзакция, lock на все строки | `in_batches` вне транзакции миграции |

Общее: `lock_timeout` (`SET lock_timeout = '5s'` в миграции) — лучше упасть и повторить, чем положить прод. Gem `strong_migrations` ругается на опасное и подсказывает замену.

## Фраза для собеса

«Любой ALTER ждёт exclusive lock: индексы concurrently, constraints NOT VALID + validate, колонки в несколько деплоев, бэкфилл батчами и lock_timeout».
"""),
}
