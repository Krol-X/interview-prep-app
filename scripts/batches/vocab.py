L = "11-leksika-po-temam/"
F = "12-frazy-svyazki/"
K = "13-kak-povtoryat/"
CD = "https://dictionary.cambridge.org/dictionary/english/"
OPT = "https://bitcoinops.org/en/topics/"
def v(name, body, links=None):
    return (L + name, (links or [], body))
def f(name, body):
    return (F + name, ([], body))
def k(name, body, links=None):
    return (K + name, (links or [], body))

ITEMS = dict([
# ───── 11 лексика ─────
v("01-background-experience-in-with-i-specialize-in.md", """
- **background** — профессиональный бэкграунд, откуда ты. *My background is in PHP and Laravel.* / *I come from a PHP background.*
- **experience in** + область: *experience in backend development*; **experience with** + инструмент: *experience with PostgreSQL, with Docker*.
- **I specialize in** — *I specialize in backend APIs and database design.*
- *years of experience*: *three years of commercial experience*.

> I have a background in PHP; my experience is mostly in backend development with Laravel and PostgreSQL, and I'm now specializing in Ruby.

Не: *experience of working* (брит., ок, но реже), *an experience* (неисчисл.), *I'm specialist in* → *I'm a specialist in / I specialize in*.
"""),
v("02-full-stack-developer-back-end-front-end.md", """
- **full-stack developer** (через дефис как прилагательное; *I do full stack* — без).
- **back-end / backend**, **front-end / frontend** — оба написания ок; произносится «бэк-энд».
- *on the backend / on the frontend*: *I mostly work on the backend.*
- *server-side / client-side* — синонимы в описании кода.

> I'm a full-stack developer, but about seventy percent of my work has been on the backend. On the frontend I've done Vue and TypeScript.

Роли: *backend engineer, software engineer, developer* (взаимозаменяемы в вакансиях), *team lead, tech lead, CTO*.
"""),
v("03-i-was-responsible-for-my-main-focus-was-i-was-in.md", """
Описание обязанностей — три уровня вовлечённости:

- **I was responsible for** + -ing / noun — отвечал (владел): *I was responsible for the notifications module and the REST API.*
- **My main focus was** — основное: *My main focus was the migration to Vue 3.*
- **I was involved in** — участвовал (не владел): *I was involved in code reviews and architecture discussions.*
- **I owned** — сильнее, «моя зона»: *I owned the notifications feature end to end.*
- **I contributed to** — вносил вклад: *I contributed to the design of the API.*

Избегать «I was doing» для обязанностей (звучит как временное). Избегать *I did everything* — конкретизировать.
"""),
v("04-to-migrate-to-refactor-to-maintain-to-ship-to-de.md", """
- **migrate** (from X to Y): *I migrated the frontend from React to Vue 3.* *migration* — и о БД (*run a migration*).
- **refactor** — менять структуру, не поведение: *I refactored the controller into service objects.*
- **maintain** — поддерживать: *I maintained a legacy CRM.* *maintenance*.
- **ship** — выпустить пользователям (разговорно, ценится): *We shipped the feature in two weeks.*
- **deliver** — сдать результат: *I delivered the module on time.*
- **deploy** — выкатить на сервер: *We deployed every Friday.* *deployment, rollout, rollback*.
- **roll out / roll back** — развернуть / откатить.

> I shipped the notifications module, then spent two months maintaining and refactoring legacy parts of the CRM.
"""),
v("05-legacy-code-internal-tool-crm-system-in-house.md", """
- **legacy code** — старый код без тестов/документации. *Most of the CRM was legacy code with no tests.*
- **internal tool** — для сотрудников, не клиентов: *an internal tool for managers.*
- **CRM system** — произносится по буквам «си-ар-эм».
- **in-house** — разработано внутри компании: *an in-house CRM*, *in-house team* (vs *outsourced*).
- **greenfield** (с нуля) vs **brownfield** (существующий проект).
- **monolith / microservices / modular monolith**.

> It was an in-house CRM — an internal tool used by about fifty managers. A lot of legacy code, so a big part of the job was understanding it before changing anything.
"""),
v("06-to-leave-a-company-the-project-ended-contract-en.md", """
Нейтральные формулировки для «почему ушёл»:

- **I left the company** (не *I went out from*). *I left Sovtech in June.*
- **the project ended / wrapped up** — проект завершился: *It was a fixed-scope project, and it wrapped up in May.*
- **my contract ended** — контракт закончился.
- **I was looking for growth / for a backend-focused role / for a change of stack**.
- **the role turned into maintenance** — работа свелась к поддержке.
- **I decided to move on** — решил двигаться дальше (мягко).
- Избегать: *I was fired* (если не так), *the company was bad*, *quit* (резко; лучше *left*).

> The project wrapped up, and I decided it was the right moment to move to Ruby properly rather than take another PHP contract.
"""),
v("07-a-gap-in-my-cv-between-jobs-freelance-contract-w.md", """
- **a gap in my CV / résumé** — перерыв: *There's a short gap between the two jobs.*
- **between jobs** — вежливо о «безработный»: *I'm between jobs at the moment.*
- **freelance / contract work** — *I did some contract work for a client.*
- **a bounded / fixed-scope engagement** — проект с определённым концом.
- **a career break** — осознанный перерыв.
- **side project / pet project** — своё.

> The gap you see was contract work — a systems project for one client — plus the time I spent going deep into Ruby and building the wallet.

CV (брит.) = résumé (амер.); в разговоре — *CV* понятно всем.
"""),
v("08-strengths-weaknesses-to-improve-to-pick-up-a-lan.md", """
- **strengths / weaknesses** — *My main strength is debugging — I'm patient with hard bugs.* Слабость — реальную + что делаешь: *A weakness is that I sometimes over-engineer; I've learned to ship the simple version first.*
- **to improve** — *I'm working to improve my spoken English.*
- **to pick up** — быстро освоить: *I picked up Vue in a couple of weeks.* *pick up a language / a tool*.
- **to get up to speed** — войти в курс: *It took me about two weeks to get up to speed on the codebase.*
- **to ramp up** — то же, про онбординг.
- **a learning curve** — *dry-rb has a steep learning curve.*
- **area for growth** — вежливо о слабости.

> I pick up new stacks quickly — I got up to speed on Ruby in a few months of evenings — but I'd say spoken English is still an area for growth.
"""),
v("09-i-m-comfortable-with-i-m-familiar-with-i-have-ha.md", """
Шкала уверенности в технологии (честность важнее бравады):

- **I have hands-on experience with** — работал руками, в проде: *hands-on experience with Laravel and PostgreSQL.*
- **I'm comfortable with** — уверенно пользуюсь: *I'm comfortable with Docker and CI.*
- **I'm familiar with** — знаком, но не глубоко: *I'm familiar with Sidekiq from docs and a small project.*
- **I've touched / I've played with** — пробовал: *I've played with dry-rb.*
- **I haven't used it in production, but** — честная формула.
- **I'm proficient in** — свободно (сильно; осторожно).
- **I know my way around** — ориентируюсь: *I know my way around Linux.*

> I'm comfortable with Rails basics, familiar with Sidekiq, and I've started using dry-rb in the test task — not in production yet.
"""),
v("10-junior-middle-mid-level-senior.md", """
- **junior / mid-level / senior** — в англоязычных компаниях «**middle**» почти не говорят, говорят **mid-level** (или просто *developer*). *Middle* поймут, но звучит по-СНГшному.
- **staff / principal** — выше senior (большие компании).
- **lead** — ведущий, с людьми.
- *I'd position myself as a mid-level backend developer.*
- *I'm applying for a mid-level position.*
- *in terms of seniority* — по уровню.

> In PHP I'm solidly mid-level; in Ruby I'm newer, but the fundamentals transfer — the gap is ecosystem knowledge, not engineering.
"""),
v("11-to-implement-to-design-to-break-down-a-task-to-d.md", """
- **implement** — реализовать (не *realize*): *I implemented the exchange flow.*
- **design** — спроектировать: *I designed the schema / the API.*
- **break down a task** — декомпозировать: *I break a feature down into small PRs.*
- **decouple** — разделить зависимости: *I decoupled the notification logic from the model.*
- **extract (a service / a class / a method)** — вынести: *I extracted the fee calculation into its own class.*
- **split / merge** — разбить / слить.
- **abstract away** — скрыть за абстракцией: *The client abstracts away the HTTP details.*
- **wire up** — подключить/связать: *wire up the worker to the queue.*

> I'd break the task down: first the wallet class, then the HTTP client, then wire them up in the CLI.
"""),
v("12-method-class-module-inheritance-composition-inte.md", """
- **method / class / module** — *a class method, an instance method, a module mixed in with include.*
- **inheritance** — наследование: *inherits from ApplicationRecord*; **composition** — композиция: *I prefer composition over inheritance.*
- **interface** — контракт (в Ruby — duck typing): *as long as it responds to call, it fits the interface.*
- **abstraction** — *the right level of abstraction.*
- **encapsulation**, **polymorphism**, **duck typing**.
- **mixin** — модуль-примесь. **namespace** — пространство имён.
- **dependency injection** — *I inject the client so I can stub it in tests.*

> Instead of inheritance I'd use composition: a Wallet that has a KeyStore and a Client, both injected, so each piece is testable on its own.
"""),
v("13-callback-hook-middleware-background-job-worker-q.md", """
- **callback** — *an after_save callback*; **hook** — то же, более общо: *a lifecycle hook, a git hook.*
- **middleware** — *Rack middleware, Sidekiq server middleware.*
- **background job** — фоновая задача; **worker** — процесс/класс, который её выполняет; **queue** — очередь: *enqueue a job, the job is picked up by a worker from the default queue.*
- **scheduler / cron** — *a scheduled job runs every hour.*
- **to enqueue / to dequeue**, **to process**, **to retry**, **dead set**.
- **asynchronously / in the background**: *we send emails asynchronously.*

> On save, a callback enqueues a job; a Sidekiq worker picks it up from the queue and processes it in the background, with retries on failure.
"""),
v("14-request-response-endpoint-payload-serialization-.md", """
- **request / response** — *the request body, the response headers.*
- **endpoint** — *the POST /exchanges endpoint.*
- **payload** — тело данных: *the JSON payload.*
- **serialization / to serialize / deserialize** — *we serialize the model to JSON.*
- **status code** — *returns a 422 (four twenty-two) for validation errors, 201 (two-oh-one) on create.*
- **to hit an endpoint** (разг.) — обратиться: *the frontend hits the rates endpoint.*
- **rate limit, timeout, retry, idempotency key.**
- **REST / RESTful, resource, route, params.**

> The form posts to the exchanges endpoint; the controller validates the payload and returns 422 with errors or 201 with the serialized exchange.

Числа: 200 «two hundred», 404 «four-oh-four», 500 «five hundred».
"""),
v("15-edge-case-corner-case-happy-path-fallback-defaul.md", """
- **happy path** — основной сценарий без ошибок: *I built the happy path first.*
- **edge case** — граничный случай: *zero balance is an edge case.* **corner case** — редкое сочетание условий.
- **fallback** — запасной вариант: *if the rate API fails, we fall back to a cached rate.* (глагол — *fall back on/to*).
- **default** — *the default queue, by default*.
- **to handle** — обрабатывать: *handle the error / the case*.
- **to gracefully degrade**, **fail fast**, **fail loudly**.
- **guard clause** — ранний return.

> I covered the happy path and the main edge cases: insufficient funds, dust change, API down — with a fallback to a cached fee rate.
"""),
v("16-maintainable-readable-testable-reusable-scalable.md", """
Прилагательные про качество кода — как аргументы в обсуждении:

- **maintainable** — легко поддерживать; **readable** — читаемый; **testable** — тестируемый (*injected dependencies make it testable*); **reusable** — переиспользуемый; **scalable** — масштабируемый; **robust** — устойчивый к ошибкам; **reliable** — надёжный; **predictable**; **explicit** vs **implicit** («magic»); **consistent**; **idiomatic** (*idiomatic Ruby*).
- Существительные: *maintainability, readability, reliability.*
- Антонимы: *brittle* (хрупкий), *fragile*, *tightly coupled*, *convoluted* (запутанный), *hacky*.

> I'd extract it into a service: it's more testable, the controller stays readable, and the logic becomes reusable from the admin panel.
"""),
v("17-tradeoff-overhead-overkill-boilerplate-technical.md", """
- **tradeoff** — компромисс: *It's a tradeoff between simplicity and flexibility.* *make / weigh tradeoffs.*
- **overhead** — накладные расходы: *a service object adds a bit of overhead but pays off.*
- **overkill** — избыточно: *dry-rb would be overkill for a CLI.*
- **boilerplate** — шаблонный код: *Rails removes a lot of boilerplate.*
- **technical debt / tech debt** — *we took on some tech debt to ship faster and paid it back later.*
- **premature optimization**, **over-engineering**, **YAGNI**, **good enough**.
- **the cost of / the benefit of**.

> Using a transaction object here is a tradeoff: more boilerplate up front, but much less overhead when the flow grows. For a demo it might be overkill — I'd mention it in the README instead.
"""),
v("18-it-s-a-matter-of-it-depends-on-the-downside-is-t.md", """
Рамки для аргументированного ответа:

- **It's a matter of** — вопрос чего-то: *It's a matter of priorities / of taste / of scale.*
- **It depends on** — *It depends on the load and the team size.*
- **The downside is… / The upside (benefit) is…** — *The downside is more files; the upside is each one is testable.*
- **On the one hand… on the other hand…**
- **The main advantage / drawback** — *The main drawback of callbacks is hidden side effects.*
- **In exchange for / at the cost of** — *simpler code at the cost of flexibility.*
- **worth it / not worth it** — *The extra abstraction isn't worth it here.*

> It depends on the scale. For a demo, a callback is fine; the downside is it's hard to test, so in a real app I'd move it to a service.
"""),
v("19-bug-issue-flaky-test-regression-root-cause-to-re.md", """
- **bug** — дефект; **issue** — проблема/тикет (шире); **defect** — формально.
- **flaky test** — тест, который падает иногда: *The test was flaky because of time zones.*
- **regression** — сломалось то, что работало: *The refactor introduced a regression.*
- **root cause** — первопричина: *The root cause was a job enqueued inside a transaction.* *root-cause analysis.*
- **to reproduce / steps to reproduce (repro)** — *I couldn't reproduce it locally.*
- **intermittent** — периодический; **consistent** — воспроизводится всегда.
- **workaround** — обход; **hotfix**; **to patch**.

> It was an intermittent bug with no clear steps to reproduce. Once I found the root cause — a race in the callback — the fix was small, and I added a test to prevent a regression.
"""),
v("20-to-investigate-to-track-down-to-narrow-down-to-i.md", """
Глаголы процесса расследования (для STAR-истории):

- **investigate** — исследовать: *I started investigating the logs.*
- **track down** — выследить: *I tracked it down to a callback.*
- **narrow down** — сузить: *I narrowed it down to two possible causes.*
- **isolate** — изолировать: *I isolated the problem in a small script.*
- **figure out** — разобраться: *I figured out that the job ran before the commit.*
- **dig into** — копнуть: *I dug into the Sidekiq source.*
- **rule out** — исключить: *I ruled out the network by checking latency.*
- **turn out** — оказаться: *It turned out to be a race condition.*
- **pin down** — точно определить.

> I narrowed it down by timestamps, ruled out the frontend, and tracked it down to the enqueue inside the transaction.
"""),
v("21-stack-trace-log-breakpoint-to-step-through.md", """
- **stack trace / backtrace** — *The stack trace pointed to the serializer.*
- **log / logs / logging** — *I added logging around the call.* *log level: debug, info, warn, error.*
- **breakpoint** — точка останова: *I set a breakpoint in the callback.* (*binding.irb / byebug / pry*)
- **to step through** — пройти по шагам: *I stepped through the code in the debugger.*
- **to inspect** — посмотреть значение: *inspect the variable.*
- **to print-debug** (*puts debugging*) — честно и нормально.
- **exception / error / to raise / to rescue**, **to swallow an exception** (проглотить — плохо).
- **to crash / to hang / to time out**.

> The stack trace wasn't helpful, so I added logging, set a breakpoint, and stepped through the callback until I saw the job being enqueued before the commit.
"""),
v("22-race-condition-concurrency-thread-safe-lock-dead.md", """
- **race condition** — гонка: *Two requests spent the same UTXO — a classic race condition.*
- **concurrency** — параллелизм (одновременность); **parallelism** — реально одновременно на ядрах.
- **thread-safe** — *Sidekiq workers run in threads, so the code must be thread-safe.*
- **lock / to lock / to acquire a lock / to release** — *acquire a row lock with SELECT FOR UPDATE.*
- **deadlock** — взаимная блокировка; **contention** — конкуренция за ресурс.
- **atomic / atomically** — *the update must be atomic.*
- **mutex, semaphore, critical section**.
- **to serialize access** — выстроить в очередь.

> Since several workers could pick the same UTXOs, I serialized access with a lock so the spend is atomic — otherwise you'd get a double spend rejected by the network.
"""),
v("23-to-retry-idempotent-at-least-once-delivery-dupli.md", """
- **to retry / a retry / retries** — *Sidekiq retries failed jobs with exponential backoff.*
- **idempotent / idempotency** — повтор не меняет результат: *The job is idempotent, so retries are safe.* (произн. «ай-дем-потент»)
- **at-least-once delivery** — хотя бы один раз (значит, возможны дубли); **exactly-once** — практически недостижимо; **at-most-once**.
- **duplicate / to duplicate / deduplication** — *a unique index prevents duplicates.*
- **double spend** — двойная трата (биткоин): *the network rejects a double spend.*
- **backoff**, **dead letter / dead set**, **poison message**.

> Because delivery is at-least-once, the worker has to be idempotent — I check the status before acting and rely on a unique constraint to reject duplicates.
"""),
v("24-memory-leak-timeout-bottleneck-latency-throughpu.md", """
- **memory leak** — утечка: *a memory leak in a long-running worker.* **memory bloat** — рост памяти без утечки.
- **timeout / to time out** — *the request timed out after 30 seconds.*
- **bottleneck** — узкое место: *the database was the bottleneck.*
- **latency** — задержка (*p95 latency*); **throughput** — пропускная способность (*requests per second*).
- **to scale up / out** — вертикально / горизонтально.
- **to profile / profiler**, **hot path**, **to cache / cache hit / miss**, **to optimize**.
- **under load**, **load testing**, **spike**.

> Under load the bottleneck was N+1 queries; eager loading brought p95 latency from two seconds to three hundred milliseconds and doubled throughput.
"""),
v("25-it-turned-out-that-the-problem-was-that-as-a-res.md", """
Связки для рассказа о расследовании:

- **It turned out that…** — оказалось: *It turned out that the job ran before the commit.*
- **The problem was that…** — *The problem was that the record didn't exist yet.*
- **As a result, …** — в результате: *As a result, the job retried and created a duplicate.*
- **That's why / which is why** — *which is why I moved it to after_commit.*
- **Once I realized that, …** — как только понял.
- **In the end / eventually** — в конце концов.
- **Looking back, …** — оглядываясь назад.
- **The fix was to…** — *The fix was to add a unique index.*

> It turned out the enqueue happened inside the transaction. As a result, the worker couldn't find the record and retried. The fix was to enqueue after commit; looking back, I'd also add the unique index from day one.
"""),
v("26-table-column-index-unique-constraint-foreign-key.md", """
- **table / column / row** — *a column on the exchanges table.*
- **index** — *add an index on user_id*; **composite index** — составной; **partial index**.
- **unique constraint / unique index** — *a unique constraint on (event_id, recipient_id).*
- **foreign key** — *a foreign key to users.*
- **primary key**, **nullable / NOT NULL**, **default value**, **check constraint**.
- **migration** — *write / run / roll back a migration.*
- **schema** — *the schema is in schema.rb.*
- **to normalize / denormalize**.

> I'd enforce it at the database level — a unique index rather than a Rails validation, because the validation can't protect against two concurrent inserts.
"""),
v("27-query-n-1-problem-eager-loading-to-join-transact.md", """
- **query** — запрос: *a slow query*; **to query** — *we query the UTXO set.*
- **N+1 problem** («эн-плюс-уан») — *a classic N+1 in the index action.*
- **eager loading** — *I fixed it with eager loading — includes.* **lazy loading** — противоположность.
- **to join / a join** — *join the users table.*
- **transaction** — *wrap it in a transaction*; **to commit / to roll back / rollback**.
- **isolation level** — *read committed is the default in Postgres.*
- **to explain a query / query plan** — *I looked at the query plan with EXPLAIN ANALYZE.*
- **sequential scan vs index scan**.

> The query plan showed a sequential scan; after adding an index it switched to an index scan, and the N+1 went away with includes.
"""),
v("28-to-lock-a-row-pessimistic-optimistic-locking.md", """
- **to lock a row / row-level lock** — *lock the exchange row with SELECT FOR UPDATE.*
- **pessimistic locking** — блокируем заранее: *pessimistic locking with lock! in Rails.*
- **optimistic locking** — проверяем версию при записи: *optimistic locking via a lock_version column; on conflict we retry.*
- **advisory lock** — *a Postgres advisory lock keyed by wallet id.*
- **to hold a lock / to block / to wait on a lock / lock timeout**.
- **contention** — *high contention on that row.*

> For spending UTXOs I'd use pessimistic locking: lock the wallet row, build and broadcast the transaction, commit. Optimistic locking would just make the second request fail, which is also acceptable for a demo.
"""),
v("29-unit-test-integration-test-coverage-mock-stub-fi.md", """
- **unit test** — один класс/метод изолированно; **integration test** — несколько компонентов вместе; **end-to-end (e2e) / system test** — весь поток.
- **coverage** — покрытие: *we had about 80% coverage.*
- **mock** — объект с ожиданиями (*expect(client).to receive(:broadcast)*); **stub** — подмена ответа (*allow(...).to receive(...).and_return(...)*); **double** — фейковый объект в RSpec.
- **fixture** — заготовленные данные (JSON, YAML); **factory** — генератор объектов (FactoryBot).
- **to isolate / to mock out the network** — *I mocked out HTTP with WebMock.*
- **test pyramid**, **TDD**, **red-green-refactor**.

> The builder is covered by unit tests on fixture UTXOs; the HTTP client has integration tests with WebMock stubs, so the suite runs without network.
"""),
v("30-to-assert-to-expect-to-pass-fail-test-suite-ci-p.md", """
- **to assert / an assertion** — утверждать в тесте; в RSpec — **to expect**: *I expect the output count to be two.*
- **to pass / to fail** — *the test passes / fails*; **green / red**.
- **test suite** — весь набор: *the suite runs in forty seconds.*
- **CI pipeline** — *CI runs the suite on every push.* **to break the build** — сломать сборку.
- **to be covered by tests**, **test case**, **spec** (RSpec файл), **matcher**, **setup / teardown**, **before each**.
- **flaky**, **to skip / pending**.

> I set up a GitHub Actions pipeline: on every push it runs rubocop and the RSpec suite; a failing spec breaks the build.
"""),
v("31-private-key-public-key-address-to-derive-to-gene.md", """
- **private key** — *The private key never leaves the machine.* **public key** — *derived from the private key.*
- **address** — *a Signet address starting with tb1q.*
- **to derive** — вывести математически: *the address is derived from the public key hash.*
- **to generate** — *generate a key with a secure random source.*
- **seed / seed phrase / mnemonic** — *a 12-word seed phrase.* **HD wallet** (hierarchical deterministic), **derivation path**.
- **WIF** — Wallet Import Format. **keypair**.
- **to store / to back up / to encrypt the key**.

> On first run the CLI generates a private key, stores it as WIF, and derives a P2WPKH address from the public key.
""", [("Bitcoin Optech — Glossary", OPT)]),
v("32-to-sign-signature-to-verify-to-broadcast-to-conf.md", """
- **to sign (a transaction / an input)** — *each input is signed separately.* **signature** — *a 64-byte Schnorr signature.*
- **to verify** — *nodes verify the signature against the public key.*
- **to broadcast** — отправить в сеть: *I broadcast the raw transaction via the API.* (past: *broadcast*, не *broadcasted* — оба встречаются)
- **to confirm / confirmation** — *the transaction got its first confirmation after ten minutes.* **unconfirmed / pending**.
- **to be included in a block / to be mined**.
- **raw transaction / hex**, **txid**.

> I sign each input, broadcast the hex, get the txid back, and the transaction is confirmed once it's included in a block.
"""),
v("33-transaction-input-output-unspent-output-utxo-cha.md", """
- **transaction (tx)** — *a transaction consumes inputs and creates outputs.*
- **input / output** — *one input, two outputs: recipient and change.*
- **unspent transaction output (UTXO)** — произносится «ю-ти-экс-оу» или «ютксо»: *the balance is the sum of UTXOs.*
- **change** — сдача: *the change goes back to my address.*
- **fee** — *the fee is inputs minus outputs.* **fee rate**.
- **dust** — *an output below dust isn't relayed.*
- **to consume / to spend an output**, **output index (vout)**, **previous output**, **coin selection**.

> A UTXO is an unspent output; to pay, I consume UTXOs as inputs, create an output to the recipient, send the remainder back as change, and the difference is the fee.
"""),
v("34-to-spend-to-fund-to-lock-funds-escrow-multisig-t.md", """
- **to spend** — тратить (выход); **to fund** — пополнить: *I funded the address from a faucet.*
- **to lock funds (in escrow)** — *the seller locks the bitcoin in escrow.*
- **escrow** («эскроу») — *a multisig escrow.* **to release funds** — выпустить.
- **multisig, two-of-three** — *a two-of-three multisig: any two keys can spend.*
- **custodial / non-custodial** — *Hodl Hodl is non-custodial — it never holds users' funds.* **custody, custodian**.
- **arbiter / arbitration / dispute** — *in a dispute the platform acts as arbiter.*
- **counterparty**, **settlement**, **to settle a trade**.

> The seller funds a two-of-three escrow; in a normal trade both parties sign and the funds are released; in a dispute the platform co-signs — non-custodial, because the platform alone can't spend.
"""),
v("35-block-miner-mempool-fee-rate-sats-per-vbyte-to-g.md", """
- **block** — *a block every ten minutes.* **block height**.
- **miner / to mine / mining** — *miners pick transactions by fee rate.*
- **mempool** — *the transaction sits in the mempool until it's mined.*
- **fee rate, sats per vbyte** («сатс пер ви-байт»): *one sat per vbyte on Signet.*
- **to get stuck** — застрять: *a low-fee transaction can get stuck.*
- **to bump the fee (RBF)** — *bump the fee with replace-by-fee.* **CPFP — child pays for parent**.
- **confirmation / to confirm**, **block subsidy**, **halving**, **hash rate**, **difficulty**.

> If a transaction gets stuck because the fee rate was too low, you can bump the fee with RBF or, if you're the receiver, use CPFP.
""", [("Bitcoin Optech — Fee bumping", OPT + "fee-bumping/")]),
v("36-mainnet-testnet-signet-faucet-test-coins.md", """
- **mainnet** — *real bitcoin on mainnet.*
- **testnet / Signet / regtest** — *I built it against Signet.* *regtest — a local chain where you mine blocks on demand.*
- **faucet** — кран: *I got test coins from a faucet.*
- **test coins / sBTC / tBTC** — *Signet coins have no value.*
- **node / full node / to run a node**, **block explorer** (*mempool.space*).
- **chain / network parameters / address prefix**.

> I used Signet because it's stable and predictable: blocks every ten minutes, no spam, test coins from a faucet, and a public explorer to verify the transaction.
"""),
v("37-script-spending-condition-witness-segwit-taproot.md", """
- **script / locking script / unlocking script** — *the output's locking script defines the spending condition.*
- **spending condition** — *a signature from this key, or two of three.*
- **witness** — данные подписи в SegWit: *the witness holds the signature and the public key.*
- **SegWit (Segregated Witness)** — *SegWit moved signatures out of the transaction body.* **native SegWit / bech32**.
- **Taproot** — *Taproot adds Schnorr signatures and script trees.* **key path / script path**.
- **soft fork / hard fork** — *both were soft forks — backward compatible.*
- **opcode**, **redeem script**, **P2SH / P2WPKH / P2TR** (по буквам).

> Each output has a spending condition expressed as a script; with SegWit the signature lives in the witness, which is why fees are lower, and Taproot makes multisig look like a single-key spend.
"""),
v("38-hash-to-hash-digest-checksum-to-encode-bech32.md", """
- **hash / to hash** — *hash the public key with SHA-256 then RIPEMD-160.* **hash160**.
- **digest** — результат хеша. **preimage** — прообраз.
- **checksum** — *bech32 includes a checksum that catches typos.*
- **to encode / to decode** — *encode the hash as bech32; decode the address to get the script.*
- **base58 / bech32 / hex** — *hex string, base58check.*
- **collision**, **one-way function**, **to commit to** (криптографически): *the sighash commits to the input amount.*
- **double SHA-256**, **Merkle root / Merkle tree**.

> The address is a bech32 encoding of the public key hash plus a checksum, so a typo is caught before anything is sent.
"""),
v("39-code-review-pull-request-to-merge-to-approve-to-.md", """
- **code review** — *I do code review daily.* **to review a PR**.
- **pull request (PR) / merge request (MR)** — *I opened a PR / submitted a PR.*
- **to merge** — *merged into main*; **to approve** — *I approved it with two minor comments*; **to request changes**; **to leave a comment / a nit** (мелочь).
- **to rebase / to squash / to resolve conflicts**, **branch / main / feature branch**.
- **LGTM** — looks good to me. **blocking / non-blocking comment**.
- **to address feedback** — учесть замечания: *I addressed the review comments and re-requested review.*

> I keep PRs small — one logical change — so review is fast; when I review, I separate blocking issues from nits.
"""),
v("40-sprint-standup-backlog-ticket-estimate-deadline.md", """
- **sprint** — *two-week sprints*; **sprint planning / retro(spective) / review**.
- **standup / daily** — *a 10-minute standup.*
- **backlog** — *groomed / prioritized backlog*; **backlog grooming / refinement**.
- **ticket / issue / task / story** — *I picked up a ticket.*
- **estimate / to estimate** — *I estimated it at two days / three story points.*
- **deadline** — *we met / missed the deadline.* **scope / scope creep**.
- **blocker / to be blocked on**, **to unblock**, **to push back** (возразить), **to prioritize**.

> I estimate in days rather than points; if I'm blocked, I raise it at standup the same day instead of waiting.
"""),
v("41-to-pair-to-onboard-to-document-to-sync-with.md", """
- **to pair (program) / pairing** — *I paired with a colleague on the tricky part.*
- **to onboard / onboarding** — *I onboarded two developers onto the CRM.*
- **to document / documentation / docs** — *I documented the setup in the README.*
- **to sync with** — созвониться/согласовать: *I synced with the PM on scope.*
- **to hand over / handover**, **to mentor**, **to share knowledge / knowledge sharing**.
- **to follow up** — вернуться к вопросу: *I'll follow up by email.*
- **to loop someone in** — подключить к обсуждению.

> I documented the architecture decisions so onboarding doesn't depend on me, and I'm happy to pair when something's unclear.
"""),
v("42-remote-async-communication-time-zone-overlap-hou.md", """
- **remote / fully remote / hybrid** — *I've worked fully remote for the last two years.*
- **async communication** — *I'm comfortable with async — written updates, clear PR descriptions.*
- **time zone** — *I'm in UTC+3.* **overlap hours** — *I can guarantee four to five overlap hours with CET.*
- **availability**, **working hours**, **to be online / reachable**.
- **written communication**, **to over-communicate** (положительно в remote).
- **contractor / B2B / invoice**: *I can work as a contractor and invoice monthly.*

> I'm in UTC+3, so there's a full overlap with European hours; I prefer async by default and calls for anything that needs a real discussion.
"""),
v("43-stack-tooling-workflow-release-cycle.md", """
- **stack / tech stack** — *Our stack was Laravel, Postgres, Redis, Vue.*
- **tooling** — инструменты вокруг: *linter, formatter, CI — the tooling in Ruby is mature.*
- **workflow** — *a PR-based workflow with review and CI.* **git flow / trunk-based**.
- **release cycle** — *a weekly release cycle*; **to cut a release**, **to deploy to staging / production**, **feature flags**.
- **environment (env)** — *dev, staging, prod.*
- **dependencies / to upgrade / to bump a version**, **lockfile**.

> What does your workflow look like — trunk-based or feature branches, and how long is the release cycle?
"""),

# ───── 12 фразы-связки ─────
f("01-that-s-a-good-question-let-me-think-for-a-second.md", """
**Когда**: вопрос неожиданный, нужны 3–5 секунд. Фраза занимает паузу и звучит естественно (носители так и говорят).

- *That's a good question. Let me think for a second.*
- *Hmm, let me think.*
- *Good question — give me a moment.*

Не злоупотреблять: один раз за интервью «good question» — нормально, три — заметно. Варианты: *Let me structure this. Let me think out loud.*

После паузы — начать с рамки: *«There are two things here…»* или *«The short answer is…»*.
"""),
f("02-could-you-rephrase-that-please.md", """
**Когда**: не понял формулировку (а не смысл). Нормально и ожидаемо для неносителя.

- *Sorry, could you rephrase that, please?*
- *Could you say that again?*
- *Sorry, I didn't catch the last part.*
- *Do you mean X or Y?*

Не говорить *«What?»* / *«Repeat»* — резко. Не кивать, не поняв, — ответ мимо вопроса хуже переспроса.

Можно переспросить два раза; на третий — *«Let me answer what I think you're asking, and correct me if I'm off.»*
"""),
f("03-just-to-make-sure-i-understand-are-you-asking-ab.md", """
**Когда**: вопрос понят, но неоднозначен. Уточнение показывает инженерное мышление (clarify requirements).

- *Just to make sure I understand — are you asking about how I'd design it, or how I actually did it?*
- *Just to clarify, you mean in production or in the test task?*
- *So the question is … — right?*

Полезно и для выигрыша времени: пока переформулируешь, мозг уже ищет ответ.

Пара: уточнение (*just to make sure*) + подтверждение интервьюера (*exactly*) + ответ.
"""),
f("04-if-i-understood-correctly-you-mean.md", """
**Когда**: пересказать вопрос своими словами перед ответом — особенно длинный или с акцентом.

- *If I understood correctly, you mean the case when two workers pick the same job?*
- *If I got it right, you're asking why I chose a public API over my own node.*
- *Let me make sure I've got this: …*

Если ошибся — интервьюер поправит, и ты избежал ответа на неправильный вопрос.

Грамматика: *understood* (Past Simple) — нормально; *if I understand correctly* — тоже ок.
"""),
f("05-there-are-two-things-here-first-second.md", """
**Когда**: вопрос составной или ответ многослойный. Структура держит тебя и слушателя.

- *There are two things here. First, … Second, …*
- *I'd split this into two parts: the design and the tradeoffs.*
- *Two points. One — …; two — …*
- *First… then… finally…*

Называть число заранее (*two things*) — и держать слово: не «two things», а потом пять.

Хорошо для «why did you leave» (две причины), «how does it work» (ключ → транзакция → сеть), tradeoff'ов (плюс / минус).
"""),
f("06-the-short-answer-is-the-longer-answer-is.md", """
**Когда**: есть простой ответ и нюансы. Сначала суть — интервьюер решит, нужны ли детали.

- *The short answer is yes. The longer answer is that it depends on whether the job is idempotent.*
- *Short answer: no. Longer answer: …*
- *In short, … If you want the details, …*

Это самая полезная связка для технических вопросов: не даёт утонуть в деталях до того, как сказана суть.

Антипаттерн: начинать с «it depends» без короткого ответа.
"""),
f("07-in-my-experience.md", """
**Когда**: даёшь мнение, подкреплённое практикой, без претензии на универсальность.

- *In my experience, callbacks are where hidden bugs live.*
- *In my experience, a unique index catches what a validation misses.*
- *From what I've seen, …*
- *What worked for me was …*

Мягче, чем *«callbacks are bad»*, и сильнее, чем *«I think»*. Готовит почву для примера: *In my experience… For instance, at Sovtech…*

Не говорить *«by my experience»*, *«on my experience»* — только **in**.
"""),
f("08-typically-i-would-but-it-depends-on.md", """
**Когда**: вопрос «как бы ты сделал» — дать дефолт и условие.

- *Typically I would use a service object, but it depends on how much logic there is.*
- *By default I'd go with Sidekiq, but it depends on whether Redis is already in the stack.*
- *My usual approach is …, unless …*
- *Normally … — in this case, though, …*

Формула: **дефолт + условие + что меняется**. Показывает опыт (есть дефолт) и гибкость (есть условие).

Грамматика: *would* в обеих частях или Present Simple — не мешать с *will*.
"""),
f("09-i-haven-t-used-it-in-production-but-as-i-underst.md", """
**Когда**: спрашивают о технологии, которую знаешь теоретически (dry-rb, Sidekiq Pro, Taproot).

- *I haven't used it in production, but as I understand it, …*
- *I've only used it in a side project, but the idea is …*
- *I know it at the level of docs and a small experiment: …*
- *I haven't worked with it directly, but it's similar to X, which I have used.*

Честность + демонстрация, что всё-таки знаешь. Намного лучше, чем притвориться и провалиться на уточняющем вопросе.

Дальше — *«and I'd be happy to go deeper if that's a big part of the role»*.
"""),
f("10-i-m-not-100-sure-but-i-d-guess.md", """
**Когда**: не уверен в факте, но можешь рассуждать.

- *I'm not 100% sure, but I'd guess it's about 150 vbytes.*
- *I might be wrong, but I believe Sidekiq retries 25 times by default.*
- *Off the top of my head, …* (навскидку)
- *If I remember correctly, …*
- *Don't quote me on this, but …* (разговорно)

Произношение: *100%* — «a hundred percent».

Это **не** «I don't know» — ты даёшь ответ с оговоркой. Если ошибся — оговорка тебя защищает; если прав — плюс.
"""),
f("11-i-d-need-to-look-that-up-but-my-approach-would-b.md", """
**Когда**: не помнишь деталь (API, опцию, синтаксис), но знаешь, как решить.

- *I'd need to look that up, but my approach would be to …*
- *I don't remember the exact option, but it's in the Sidekiq config — something like retry: false.*
- *I'd check the docs for the exact signature; the idea is …*
- *I'd google the specifics, but conceptually …*

Интервьюер проверяет мышление, не память. Фраза переводит разговор с «помнишь ли» на «понимаешь ли».

*look up* — посмотреть в справочнике: *look it up* (местоимение между).
"""),
f("12-i-haven-t-dealt-with-that-specific-case-here-s-h.md", """
**Когда**: ситуация незнакома — но ты можешь рассуждать от первых принципов.

- *I haven't dealt with that specific case. Here's how I'd think about it: …*
- *I haven't hit that one. Let me reason about it.*
- *That's new to me. My first step would be to …*
- *I'd start by …, then …*

Дальше — рассуждать **вслух**: что проверил бы, какие гипотезы, как исключал бы. Это и есть ответ.

*deal with — dealt with* (неправильный глагол). *hit* — разг. «сталкивался».
"""),
f("13-let-me-walk-you-through-the-flow.md", """
**Когда**: просят объяснить, как работает (тестовое, система, баг). Сигнал: «сейчас будет структура, не перебивайте 1–2 минуты».

- *Let me walk you through the flow.*
- *Let me walk you through what happens when a user submits the form.*
- *I'll go step by step.*
- *At a high level, … Now in more detail: …*

Дальше — *first / then / after that / finally*, Present Simple, активные глаголы: *the controller validates…, the service builds…, the worker broadcasts…*

*walk someone through* — провести через; очень частотное в техразговоре.
"""),
f("14-the-main-challenge-was.md", """
**Когда**: рассказ о проекте/баге — выделить главную трудность (интервьюеры именно это и слушают).

- *The main challenge was concurrency — two requests could spend the same UTXO.*
- *The tricky part was estimating the size before signing.*
- *What made it hard was that it only happened under load.*
- *The hardest part wasn't the code — it was reproducing the bug.*

После — что сделал: *…so I …*. Challenge без решения — жалоба.

*challenge* — нейтральное, профессиональное; *problem* — ок; *difficulty* — реже.
"""),
f("15-i-decided-to-because.md", """
**Когда**: объяснить решение. Каждое «почему так» в тестовом — этой формулой.

- *I decided to use bitcoinrb because it's maintained and has native Signet support.*
- *I went with P2WPKH because it's cheaper and the default in modern wallets.*
- *I chose to spend all UTXOs for simplicity; the downside is privacy.*
- *I opted for a fixed fee to keep the first version simple.*

Формула: **решение + причина + (минус, который осознаю)**. Третья часть отличает зрелого разработчика.

*decided to + V1*, *went with + noun*, *chose to + V1*, *opted for + noun*.
"""),
f("16-if-i-had-more-time-i-d.md", """
**Когда**: «что бы улучшил» — second conditional. Показать, что видишь, чего не хватает.

- *If I had more time, I'd add an HD wallet and coin selection.*
- *Given more time, I would run my own node instead of a public API.*
- *The next thing I'd do is …*
- *With another day, I'd …*

Список готовить заранее (3 пункта): для части 1 — HD wallet, coin selection, RBF; для части 2 — очередь на отправку, идемпотентность, мониторинг.

Не: *If I would have more time* ✗.
"""),
f("17-one-thing-i-simplified-is.md", """
**Когда**: самому назвать упрощение до того, как его найдут. Снимает вопрос и показывает честность.

- *One thing I simplified is that I spend all UTXOs instead of doing coin selection.*
- *I deliberately kept it simple: one key, no encryption.*
- *I cut a corner here — the rate is fetched on the frontend, which I wouldn't do in production.*
- *This is a known limitation: …*

Формула: **упрощение + почему (срок/демо) + как бы сделал правильно**.

*cut a corner / corners* — срезать угол; *deliberately* — намеренно; *known limitation*.
"""),
f("18-does-that-answer-your-question.md", """
**Когда**: закончил ответ и не уверен, что попал. Возвращает ход интервьюеру, вместо того чтобы продолжать говорить.

- *Does that answer your question?*
- *Is that what you were asking?*
- *Did I cover what you wanted?*
- *Was that the level of detail you were after?*

После — **тишина**. Самая частая ошибка — продолжать говорить, заполняя паузу. Пауза — это их ход.

Если «not quite» — *«Okay, let me try again — what part should I focus on?»*
"""),
f("19-i-can-go-into-more-detail-if-you-d-like.md", """
**Когда**: дал краткий ответ, есть глубина в запасе. Предложить, не навязывать.

- *I can go into more detail if you'd like.*
- *Happy to dig deeper into any part of that.*
- *I can show the code if that helps.*
- *There's more to it, but that's the gist.*

Это пара к «the short answer is…»: короткий ответ → предложение углубиться → интервьюер выбирает.

*the gist* — суть; *if you'd like* = *if you would like*, вежливее, чем *if you want*.
"""),

# ───── 13 как повторять ─────
k("01-den-1-vremena-tipichnye-oshibki-progovorit-po-2-.md", """
**Задача дня**: пройти раздел «Грамматика» (35 пунктов) и по каждой форме **сказать вслух два предложения о себе**. Не писать — говорить.

Порядок:
1. Времена 01–08 (30 мин): Past Simple про каждое место работы, Present Perfect про навыки, Present Simple — как работает твой wallet, Continuous — что делаешь сейчас.
2. Conditionals 09–11 (15 мин): три предложения про тестовое: *if the balance…*, *if I had more time…*, *if I had used…*.
3. Модальные + пассив 12–16 (15 мин).
4. Ошибки 23–35 (20 мин): прочитать список, затем попросить кого-то (или себя на записи) ловить *I am agree, depends from, how it works?*.

Критерий: каждый пункт отмечен в приложении, 2 предложения прозвучали. Записать на телефон минуту «о себе» — переслушать, пометить ошибки времён.
"""),
k("02-den-2-leksika-1-2-sostavit-rasskaz-o-sebe-zasa.md".replace("zasa", "zapisa"), """
**Задача дня**: лексика блоки «О себе и опыте» (01–10) и «Код и архитектура» (11–18) → собрать **Tell me about yourself** (90 сек) и **Why Ruby / crypto / Hodl Hodl**.

1. Прочитать 01–18 (30 мин), выписать 15 слов, которых не было в активе.
2. Написать рассказ о себе по структуре из раздела «Английский → Tell me about yourself» — своими словами, с 10 словами из списка (20 мин).
3. **Записать на диктофон** три раза: с бумажкой, с опорными точками, без ничего (20 мин).
4. Переслушать последнюю запись: длина ≤ 100 сек? Есть ли *I am agree / actual / realize*? Времена про прошлые места — Past Simple?
5. То же для «Why did you leave» — три ответа по 20 секунд.

Критерий: запись без бумажки укладывается в 90–100 секунд и не содержит пунктов из списка ошибок.
"""),
k("03-den-3-leksika-3-4-rasskazat-istoriyu-pro-bag-sta.md", """
**Задача дня**: блоки «Отладка» (19–25) и «База данных / тесты» (26–30) → **история про баг по STAR** на 90 секунд.

1. Прочитать 19–30 (25 мин). Обратить внимание на глаголы расследования: *narrow down, track down, rule out, turn out*.
2. Выбрать реальный баг (лучше про гонку/дубли — их домен). Расписать STAR по строчке на букву (10 мин).
3. Рассказать вслух с таймером; записать. Цель — 80–100 секунд, минимум 5 слов из блока отладки, одно *while I was …ing*, одно *it turned out that*, одно *if we had …* в конце.
4. Второй дубль — ответить на вероятные вопросы: *How did you find it? Why didn't tests catch it? What did you change in your process?*

Критерий: история звучит без запинок, есть цифра в Result и одно предложение Learning.
"""),
k("04-den-4-leksika-5-obyasnit-utxo-i-escrow-vsluh-na-.md", """
**Задача дня**: блок «Биткоин» (31–38) → объяснить **UTXO**, **escrow 2-of-3** и **walk me through the test task** на английском.

1. Прочитать 31–38 (20 мин), проговорить произношение: *UTXO, SegWit, bech32, Schnorr, escrow, idempotent, vbyte*.
2. UTXO за 40 секунд — без бумажки, записать. Проверить: *consume, unlock, change, fee, remainder*.
3. Escrow за 40 секунд: *lock funds, two of three, arbiter, non-custodial, dispute*.
4. Walk me through the test task — 2 минуты по тексту из раздела «Английский». Записать, переслушать: Present Simple, -s в 3-м лице, *to + V1* для «зачем».
5. Ответить вслух на 5 вопросов из «Своё тестовое: объяснить каждый шаг»: *why P2WPKH, why all UTXOs, what if timeout after broadcast, how did you estimate the size, what would you change for production*.

Критерий: три записи, в каждой нет пауз длиннее 3 секунд.
"""),
k("05-den-5-frazy-svyazki-otvetit-na-5-sluchajnyh-vopr.md", """
**Задача дня**: раздел «Фразы-связки» (19 штук) → отвечать на случайные вопросы, вплетая связки.

1. Прочитать все 19 (15 мин), выучить наизусть 8 «спасательных»: *could you rephrase, just to make sure, the short answer is, in my experience, I haven't used it in production but, I'm not 100% sure but, let me walk you through, does that answer your question*.
2. Взять 5 вопросов наугад (из любого раздела приложения: Ruby, Rails, Sidekiq, Postgres, Bitcoin). На каждый — ответ 60–90 секунд **с минимум тремя связками**. Записать.
3. Переслушать: связки звучат естественно или вставлены? Есть ли структура (*two things / first-second*)? Закончен ли ответ (*does that answer…*)?
4. Бонус: попросить друга/ChatGPT-голос задать вопросы вразнобой и один раз перебить — потренировать *«sorry, could you repeat the last part»*.

Критерий: 5 записей, в каждой ≥ 3 связки, ни одного ответа длиннее 2 минут.
"""),
k("06-kazhdyj-den-slushat-10-min-chego-to-tehnicheskog.md", """
**Каждый день, 10–15 минут**: слушать английскую техническую речь — чтобы вопрос интервьюера не звучал как шум.

Что слушать (под их домен):
- **Remote Ruby** / **The Bike Shed** (thoughtbot) — разговорный Ruby/Rails, естественный темп.
- **Rails World / RubyConf** доклады на YouTube — с субтитрами, потом без.
- **Stephan Livera Podcast**, **Bitcoin Optech recap** — биткоин-терминология в живой речи.
- **Chat with Lightning / What Bitcoin Did** — проще, разговорно.
- Любой мок-интервью «Rails interview questions» на YouTube — формат вопросов.

Как: первые дни — с субтитрами, с 3-го дня — без; после каждого — пересказать 3 предложения вслух о том, что услышал. Записать 2–3 выражения, которые понравились, в заметки.

Критерий: день без прослушивания = день пропущен. Неделя — и вопросы перестают «проскакивать мимо».
""", [("The Bike Shed", "https://bikeshed.thoughtbot.com/"), ("Remote Ruby", "https://www.remoteruby.com/"), ("Bitcoin Optech newsletters", "https://bitcoinops.org/en/newsletters/")]),
])
