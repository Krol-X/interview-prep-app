G = "https://guides.rubyonrails.org/"
A = "https://api.rubyonrails.org/classes/"
ITEMS = {
"02-rails/01-zhiznennyj-cikl-zaprosa-rack-middleware-router-c.md": ([
  ("Rails Guides — Rails on Rack", G + "rails_on_rack.html"),
  ("Rails Guides — Action Controller Overview", G + "action_controller_overview.html"),
], """
```
Puma (сервер) → Rack env (хеш запроса)
  → middleware stack (~20 штук: логгер, сессии, cookies, CSRF, ExecutorRails, ...)
    → ActionDispatch::Routing (config/routes.rb) → контроллер#action
      → before_action → action → render/redirect → after_action
    ← ответ [status, headers, body] через middleware обратно
```

- **Rack** — интерфейс: объект с `call(env)` возвращает `[status, headers, body]`. Rails-приложение — тоже Rack-приложение. `rails middleware` покажет стек.
- **Router** сопоставляет метод+путь, кладёт `params[:id]` и т.п. `resources :withdrawals` даёт 7 маршрутов.
- **Контроллер**: один экземпляр на запрос. `params` — `ActionController::Parameters`. Один `render`/`redirect_to` на action (иначе `DoubleRenderError`); без явного — рендерит шаблон по имени action.
- **Executor/Reloader** — middleware, который оборачивает запрос: отдаёт AR-соединение в пул, перезагружает код в dev.
- Исключение → `ActionDispatch::ShowExceptions` → страница 500/404 (`rescue_from` в контроллере — раньше).

Ответ в API-режиме (`rails new --api`): урезанный стек без cookies/sessions/flash.

## Фраза для собеса

«Puma → Rack middleware → роутер → контроллер → колбэки → action → render; всё, что между сервером и роутером — middleware, туда же можно вставить своё».
"""),

"02-rails/02-strong-params-require-permit-mass-assignment.md": ([
  ("Rails Guides — Strong Parameters", G + "action_controller_overview.html#strong-parameters"),
], """
Mass assignment — `Model.new(params)` присваивает все переданные поля. Без фильтра пользователь пришлёт `admin: true` или `balance: 1e9` (GitHub, 2012).

```ruby
def withdrawal_params
  params.require(:withdrawal).permit(:to_address, :amount)
end
```

- `require(:key)` — ключ обязан быть, иначе `ParameterMissing` → 400.
- `permit(...)` — белый список. Непермиченные ключи молча отбрасываются (в dev — лог, можно `config.action_controller.action_on_unpermitted_parameters = :raise`).
- Массивы и вложенность: `permit(:name, tags: [], address: [:city, :zip])`. Произвольный хеш — `permit(meta: {})`.
- Никогда не пермить `status`, `user_id`, `fee`, `role` — то, что назначает сервер. Присваивать явно: `Withdrawal.new(withdrawal_params.merge(user: current_user))`.
- `params.expect(withdrawal: [:to_address, :amount])` — Rails 8, require+permit одной строкой и устойчивее к мусору в параметрах.

`params[:x]` без permit — ок для чтения одиночных значений (`params[:id]`), проблема только в передаче всего хеша в модель.

## Фраза для собеса

«Белый список через `permit`, серверные поля назначаю явно, а не из параметров; mass assignment без фильтра — это как `admin: true` в форме».
"""),

"02-rails/04-saved-change-to-x-x-previously-changed-dirty-tra.md": ([
  ("Rails API — ActiveModel::Dirty", A + "ActiveModel/Dirty.html"),
], """
Dirty tracking — модель помнит, что изменилось с момента загрузки.

| До `save` (в before_*, валидациях) | После `save` (в after_save/after_commit) |
|---|---|
| `status_changed?` | `saved_change_to_status?` |
| `status_was` | `status_before_last_save` |
| `status_change` → `["pending","sent"]` | `saved_change_to_status` → `["pending","sent"]` |
| `changed?`, `changes`, `changed_attributes` | `saved_changes`, `saved_changes?` |

Ключевой паттерн — реагировать на **переход**, а не на состояние:

```ruby
after_commit :notify, if: -> { saved_change_to_status?(to: "sent") }
# а не: if: -> { status == "sent" } — сработает при каждом сохранении в sent
```

`will_save_change_to_x?` — синоним `x_changed?`, явно про «в этом save».

Rails 5.1 переименовал: раньше в `after_save` работали `x_changed?` (и это сбивало), теперь там нужны `saved_change_to_*`. Старые имена в after-колбэках — deprecated/неверный результат.

`restore_attributes`, `reload` — сбросить изменения. `update_columns` dirty не трогает.

## Фраза для собеса

«В before — `x_changed?`, в after — `saved_change_to_x?`; с `to:` ловлю конкретный переход, а не состояние».
"""),

"02-rails/05-validacii-validates-custom-validator-valid-vs-va.md": ([
  ("Rails Guides — Active Record Validations", G + "active_record_validations.html"),
], """
```ruby
class Withdrawal < ApplicationRecord
  validates :to_address, presence: true, format: { with: /\\A(tb1|2|m|n)/ }
  validates :amount, numericality: { greater_than: 0, only_integer: true }
  validates :status, inclusion: { in: STATUSES }
  validates :txid, uniqueness: true, allow_nil: true     # + unique index в БД!
  validate :enough_balance, on: :create                  # кастомный метод

  private
  def enough_balance
    errors.add(:amount, :insufficient, message: "exceeds balance") if amount > wallet.balance
  end
end
```

- `valid?` — прогоняет валидации, заполняет `errors`, возвращает bool. `invalid?` — наоборот.
- `validate!` — то же, но бросает `RecordInvalid`.
- `errors.add(:base, ...)` — ошибка не к полю. `errors.full_messages`, `errors[:amount]`, `errors.details`.
- Контексты: `on: :create`, свои — `valid?(:payout)`, `save(context: :payout)`.
- Условия: `if: :foreign?`, `unless: -> { draft? }`.
- Выносимый валидатор: `class AddressValidator < ActiveModel::EachValidator; def validate_each(record, attr, value)`. Подключается `validates :to_address, address: true`.
- `uniqueness` **не атомарна** (SELECT потом INSERT) — гонка. Обязателен unique index; ловить `RecordNotUnique`.

Валидации работают только в Ruby: `update_column`, `update_all`, `insert_all`, `delete` их обходят.

## Фраза для собеса

«Валидации — в модели, но инварианты дублирую constraint'ами в БД: uniqueness без индекса — гонка».
"""),

"02-rails/06-save-vs-save-update-vs-update-vs-update-attribut.md": ([
  ("Rails API — ActiveRecord::Persistence", A + "ActiveRecord/Persistence.html"),
], """
| Метод | Валидации | Колбэки | updated_at | При ошибке |
|---|---|---|---|---|
| `save` / `update(attrs)` | да | да | да | `false` |
| `save!` / `update!` | да | да | да | `RecordInvalid` |
| `update_attribute(:a, v)` | **нет** | да | да | false |
| `update_column(s)` | нет | **нет** | **нет** | — (прямой SQL) |
| `update_all` (relation) | нет | нет | нет | число строк |
| `touch` | нет | after_touch | да | — |
| `increment!` / `decrement!` | нет | нет | да | — (атомарный UPDATE) |

Правила:
- В сервисах и джобах — `!`-версии: ошибку нельзя молча потерять. Без `!` — в контроллере, когда ветвишься по результату.
- `update_attribute` — «пропустить валидации, но оставить колбэки». Почти всегда это запах: валидации нужны. Исключение — служебные поля.
- `update_column` — для технических записей (счётчики, last_seen_at), когда колбэки и валидации нежелательны и ты точно знаешь, что делаешь. Не триггерит dirty.
- `update_all` — массово, одним SQL, без загрузки объектов: `Withdrawal.where(status: "pending").update_all(status: "expired")`.

Для денег: `increment!(:balance, amount)` или `update_all("balance = balance + ?")` — атомарно, вместо read-modify-write.

## Фраза для собеса

«В бизнес-логике `save!`/`update!`; `update_column(s)` и `update_all` — обход валидаций и колбэков, применяю осознанно».
"""),

"02-rails/07-associacii-has-many-through-inverse-of-dependent.md": ([
  ("Rails Guides — Active Record Associations", G + "association_basics.html"),
], """
```ruby
class User < ApplicationRecord
  has_one  :wallet, dependent: :destroy
  has_many :withdrawals, through: :wallet
end
class Wallet < ApplicationRecord
  belongs_to :user                   # обязателен по умолчанию (Rails 5+); optional: true
  has_many :withdrawals, dependent: :restrict_with_error, inverse_of: :wallet
end
```

- `has_many :through` — связь через промежуточную модель; работает и для many-to-many с явной join-моделью (предпочтительнее `has_and_belongs_to_many`).
- `dependent:` — `:destroy` (колбэки, по одному), `:delete_all` (один SQL, без колбэков), `:nullify`, `:restrict_with_error`/`:restrict_with_exception`. Без него — осиротевшие строки или FK-ошибка. FK в БД — обязательно.
- `inverse_of` — чтобы `wallet.withdrawals.first.wallet` был тем же объектом, а не новым запросом; Rails угадывает в простых случаях, с `through`/`foreign_key`/scope — укажи явно.
- `polymorphic: true` — `belongs_to :commentable, polymorphic: true` + `commentable_type`/`commentable_id`. FK в БД невозможен — минус.
- `counter_cache: true` — денормализованный счётчик, обновляется колбэками.
- Scope на ассоциации: `has_many :sent_withdrawals, -> { where(status: "sent") }, class_name: "Withdrawal"`.
- `belongs_to` добавляет presence-валидацию; `has_many` — нет.

Запросы: `user.withdrawals` — lazy relation; `.build`/`.create` проставят FK; `<<` сохраняет сразу.

## Фраза для собеса

«`through` для связей через модель, `dependent` + FK в БД обязательно, `inverse_of` явно там, где Rails не угадает».
"""),

"02-rails/08-n-1-includes-vs-preload-vs-eager-load-vs-joins-g.md": ([
  ("Rails Guides — Eager Loading Associations", G + "active_record_querying.html#eager-loading-associations"),
  ("gem bullet", "https://github.com/flyerhzm/bullet"),
], """
N+1: один запрос за списком, потом по запросу на каждую связь в цикле.

```ruby
Withdrawal.limit(50).each { |w| w.wallet.user.email }   # 1 + 50 + 50 запросов
Withdrawal.includes(wallet: :user).limit(50)            # 3 запроса
```

| Метод | SQL | Когда |
|---|---|---|
| `preload` | отдельный `SELECT ... WHERE id IN (...)` на каждую связь | по умолчанию; не умеет фильтровать по связи |
| `eager_load` | один `LEFT OUTER JOIN` | когда нужно `where`/`order` по полям связи |
| `includes` | сам выбирает: preload, а при `references`/`where` по связи — eager_load | дефолт, но менее предсказуем |
| `joins` | `INNER JOIN`, **не загружает** связь | фильтрация/агрегация без доступа к объектам связи |

```ruby
Withdrawal.joins(:wallet).where(wallets: { user_id: 1 })     # фильтр, wallet не загружен
Withdrawal.includes(:wallet).where(wallets: { user_id: 1 })  # → eager_load автоматически
Withdrawal.preload(:wallet).merge(Wallet.active)             # ошибка: нет join
```

- `has_many` с `eager_load` умножает строки — Rails дедуплицирует, но тяжелее.
- `strict_loading` (6.1+): `Withdrawal.strict_loading.first.wallet` → исключение при ленивой загрузке. Можно включить на модель или глобально в dev/test.
- gem `bullet` — ловит N+1 и лишние includes в dev.
- `exists?`/`size` vs `count`: `size` использует загруженную коллекцию, `count` всегда SQL.

## Фраза для собеса

«`preload` — отдельные запросы, `eager_load` — JOIN, `includes` выбирает сам; `joins` для фильтра без загрузки. В dev — bullet или strict_loading».
"""),

"02-rails/09-scopes-vs-class-methods-chaining-merge.md": ([
  ("Rails Guides — Scopes", G + "active_record_querying.html#scopes"),
], """
```ruby
scope :sent,   -> { where(status: "sent") }
scope :recent, ->(n = 10) { order(created_at: :desc).limit(n) }
scope :by_user, ->(u) { joins(:wallet).where(wallets: { user_id: u.id }) }

def self.big = where("amount_sat >= ?", 1_000_000)   # то же как класс-метод
```

Разница одна, но важная: scope **всегда возвращает relation** — если лямбда вернула `nil`/`false`, scope отдаст `all`, цепочка не сломается. Класс-метод вернёт то, что вернёт. Для условных веток (`return unless x`) scope безопаснее; для сложной логики с несколькими путями — класс-метод читается лучше.

Цепочки ленивы: SQL уходит при итерации/`to_a`/`first`/`count`. Можно собирать условно:
```ruby
rel = Withdrawal.all
rel = rel.sent if params[:sent]
rel = rel.where(created_at: range) if range
```

`merge` — применить скоуп другой модели через join:
```ruby
Withdrawal.joins(:wallet).merge(Wallet.active)
```

`default_scope` — почти всегда зло: невидим, ломает `find`, требует `unscoped`. Исключение — soft delete, и то спорно.

`scope` с тем же именем, что ассоциация/колонка — конфликт. `where.not`, `or` (5+), `rewhere`, `unscope(:order)`.

## Фраза для собеса

«Scope всегда возвращает relation, поэтому безопасен в цепочках; `merge` переносит scope через join; `default_scope` избегаю».
"""),

"02-rails/10-where-bezopasno-placeholders-hash-usloviya-sql-i.md": ([
  ("Rails Guides — Conditions / SQL injection", G + "active_record_querying.html#pure-string-conditions"),
  ("Rails Guides — Security: SQL Injection", G + "security.html#sql-injection"),
], """
```ruby
# ОПАСНО — интерполяция в SQL
Withdrawal.where("status = '#{params[:status]}'")
# params[:status] = "' OR 1=1 --"  → все строки
# params[:status] = "'; DROP TABLE withdrawals; --"

# Безопасно
Withdrawal.where(status: params[:status])                  # хеш-условие: экранируется, типизируется
Withdrawal.where("amount > ?", params[:min])               # позиционный placeholder
Withdrawal.where("amount > :min AND fee < :max", min: 1, max: 9)   # именованный
Withdrawal.where(created_at: 1.day.ago..)                  # range → BETWEEN / >=
Withdrawal.where(status: %w[sent failed])                  # IN (...)
Withdrawal.where.not(txid: nil)                            # IS NOT NULL
```

Что ещё инъекционно: `order(params[:sort])`, `pluck(params[:col])`, `select("...")`, `joins("...")`, `group`, `having`, `find_by_sql`. Для динамических имён колонок — белый список: `order(SORTS.fetch(params[:sort], :id))`. Или `sanitize_sql_like` для LIKE, `Arel.sql` — только для заведомо константных строк (явно помечаешь «я проверил»).

Хеш-условия и placeholders заодно приводят типы: `where(id: "5abc")` → 5, а строка в SQL — нет.

## Фраза для собеса

«Никакой интерполяции в SQL: хеш-условия или placeholders; `order`/`select` с пользовательским вводом — только через белый список».
"""),

"02-rails/11-find-vs-find-by-vs-where-first-find-each-in-batc.md": ([
  ("Rails Guides — Retrieving Objects", G + "active_record_querying.html#retrieving-objects-from-the-database"),
  ("Rails Guides — Retrieving Multiple Objects in Batches", G + "active_record_querying.html#retrieving-multiple-objects-in-batches"),
], """
```ruby
Withdrawal.find(5)            # по PK; RecordNotFound → в контроллере это 404
Withdrawal.find_by(txid: t)   # первый по условию или nil
Withdrawal.find_by!(txid: t)  # или RecordNotFound
Withdrawal.where(txid: t).first   # то же, что find_by, но добавит ORDER BY id
Withdrawal.where(txid: t).take    # без ORDER BY — что отдаст БД
```

Для внешних id (`params[:id]`) — `current_user.withdrawals.find(id)`: заодно авторизация и 404 вместо чужой записи.

Батчи — не грузить миллион объектов в память:
```ruby
Withdrawal.find_each(batch_size: 1000) { |w| ... }   # по PK, порядок игнорируется
Withdrawal.in_batches(of: 1000) { |rel| rel.update_all(...) }   # relation на батч
Withdrawal.in_batches.each_record { ... }
```

`find_each` отменяет `order`/`limit` (работает по id-курсору). Нужна сортировка — `in_batches(order: :desc)` или свой курсор.

`first`/`last` на relation без `order` — по PK. `first(3)` — массив. `exists?` дешевле `present?`/`any?` (не грузит записи).

## Фраза для собеса

«`find` — по PK с исключением, `find_by` — nil; большие выборки — `find_each`/`in_batches`, они идут по PK батчами и не держат всё в памяти».
"""),

"02-rails/12-pluck-vs-select-vs-map.md": ([
  ("Rails API — pluck", A + "ActiveRecord/Calculations.html#method-i-pluck"),
], """
```ruby
Withdrawal.where(status: "sent").map(&:txid)
# SELECT withdrawals.* → строит 10 000 AR-объектов → берёт поле. Медленно, память.

Withdrawal.where(status: "sent").pluck(:txid)
# SELECT txid FROM ... → массив строк. Без объектов. В разы быстрее.
Withdrawal.pluck(:id, :txid)       # [[1,"a"],[2,"b"]]
Withdrawal.pick(:txid)             # pluck + limit 1

Withdrawal.select(:id, :txid)
# SELECT id, txid → AR-объекты только с этими полями; остальные → MissingAttributeError
# Relation остаётся цепляемой: .select(...).where(...).order(...)
Withdrawal.select("wallet_id, SUM(fee) AS total").group(:wallet_id)   # агрегаты как атрибуты
```

| | Возвращает | Объекты | Цепляется дальше |
|---|---|---|---|
| `map` | массив | да, полные | нет |
| `pluck` | массив значений | нет | нет (терминальный) |
| `select` | relation | да, частичные | да |
| `ids` | массив id | нет | нет |

`pluck` на уже загруженной коллекции (`user.withdrawals.pluck`) всё равно пойдёт в БД — если записи уже загружены, `map` дешевле. `distinct.pluck`, `pluck` с `joins` — `pluck("wallets.address")`.

## Фраза для собеса

«Нужны только значения — `pluck`; нужны объекты, но не все поля или подзапрос — `select`; `map` — только на уже загруженной коллекции».
"""),

"02-rails/13-tranzakcii-transaction-nested-requires-new-chto-.md": ([
  ("Rails API — ActiveRecord::Transactions", A + "ActiveRecord/Transactions/ClassMethods.html"),
], """
```ruby
ActiveRecord::Base.transaction do
  wallet.debit!(total)
  withdrawal.save!
end
# любое исключение → ROLLBACK и re-raise; вернулось нормально → COMMIT
```

- Используй `!`-методы внутри: `save` вернёт false и транзакция **закоммитится** с частичными данными.
- `raise ActiveRecord::Rollback` — откатить без пробрасывания наружу (транзакция вернёт nil).
- Внутри транзакции не делать HTTP, не слать джобы и письма — всё внешнее в `after_commit` или после блока. Долгая транзакция держит блокировки.

Вложенность:
```ruby
Model.transaction do
  Model.transaction do          # НЕ новая транзакция — та же самая
    raise ActiveRecord::Rollback # проглочен внутренним блоком, внешняя закоммитится!
  end
end

Model.transaction do
  Model.transaction(requires_new: true) do   # SAVEPOINT — откатится только он
    raise ActiveRecord::Rollback
  end
end
```

Один `transaction` = одна БД-транзакция на соединение. Соединение привязано к потоку — в Thread внутри блока транзакции не будет.

`after_commit` на модели срабатывает после внешнего COMMIT. `transaction(isolation: :serializable)` — задать уровень.

Rails 7.2: `ActiveRecord.after_all_transactions_commit { }` и `transaction.after_commit { }` — колбэк на саму транзакцию, не на модель.

## Фраза для собеса

«Внутри транзакции — только `!`-методы и только БД; вложенный `transaction` без `requires_new` — та же транзакция, `Rollback` там проглотится».
"""),

"02-rails/14-locking-with-lock-lock-pessimistic-lock-version-.md": ([
  ("Rails Guides — Locking Records for Update", G + "active_record_querying.html#locking-records-for-update"),
  ("Rails API — Locking::Optimistic", A + "ActiveRecord/Locking/Optimistic.html"),
], """
**Пессимистичная** — блокируем строку в БД, конкуренты ждут.

```ruby
wallet.with_lock do                 # transaction + reload(lock: true) → SELECT ... FOR UPDATE
  raise Insufficient if wallet.balance < amount
  wallet.update!(balance: wallet.balance - amount)
end
Wallet.lock.find(id)                # FOR UPDATE внутри своей транзакции
Wallet.lock("FOR UPDATE SKIP LOCKED")
```

Когда: деньги, счётчики, очереди — короткая критическая секция, конфликты часты. Минусы: ждут, возможны deadlock'и (блокируй в одном порядке).

**Оптимистичная** — колонка `lock_version`; `UPDATE ... WHERE id = ? AND lock_version = ?`; если 0 строк — `StaleObjectError`.

```ruby
# миграция: t.integer :lock_version, default: 0, null: false
w = Withdrawal.find(1)   # lock_version 3
w.update!(note: "x")     # ok → 4
# параллельно другой с version 3: StaleObjectError
```

Когда: редкие конфликты, длинные формы редактирования (пользователь думает минуту), нет смысла держать блокировку. Нужно ловить и показывать «запись изменена, обновите».

Оба — на уровне одной строки. Для «только один процесс делает X» — advisory lock или unique-строка.

## Фраза для собеса

«Для денег — `with_lock` (FOR UPDATE), короткая секция; для редактирования форм — `lock_version` и обработка StaleObjectError».
"""),

"02-rails/15-race-conditions-find-or-create-by-vs-create-or-f.md": ([
  ("Rails API — create_or_find_by", A + "ActiveRecord/Relation.html#method-i-create_or_find_by"),
], """
Check-then-act — два запроса между проверкой и действием успевают оба.

```ruby
Wallet.find_or_create_by(user_id: 1)
# A: SELECT → нет;  B: SELECT → нет;  A: INSERT;  B: INSERT  → два кошелька
```

Защита — только на уровне БД:

1. **Unique index** `add_index :wallets, :user_id, unique: true` — второй INSERT упадёт с `RecordNotUnique`.
2. **`create_or_find_by`** (Rails 6+): INSERT первым, при нарушении уникальности — SELECT. Требует индекса. Минус: сжигает значение sequence, внутри транзакции уронит её (используй savepoint).
3. Или `find_or_create_by` + `rescue ActiveRecord::RecordNotUnique; retry`.
4. `upsert`/`insert_all(..., unique_by:)` — `ON CONFLICT DO UPDATE` одним SQL.

Другие гонки того же вида:
- `if wallet.balance >= x then update` → `with_lock` или условный UPDATE с проверкой rowcount.
- `validates :x, uniqueness: true` → всегда + unique index.
- `counter += 1; save` → `increment!` / `update_counters`.
- «проверил, что джоб не идёт, запустил» → unique job / lock в Redis `SET NX`.
- Два запроса на вывод одних UTXO → очередь с concurrency 1 или lock.

Тест на гонку: два потока с барьером, или просто обосновать индексом.

## Фраза для собеса

«Любое «проверил — сделал» двумя запросами — гонка; лечу unique index + `create_or_find_by`, `with_lock` или атомарным UPDATE».
"""),

"02-rails/16-atomarnye-apdejty-increment-update-all-update-co.md": ([
  ("Rails API — increment!", A + "ActiveRecord/Persistence.html#method-i-increment-21"),
  ("Rails API — update_counters", A + "ActiveRecord/CounterCache/ClassMethods.html#method-i-update_counters"),
], """
Read-modify-write в Ruby — гонка: два процесса прочитали 100, оба записали 90 вместо 80.

```ruby
# плохо
wallet.balance -= 10; wallet.save!

# атомарно — арифметика в SQL
wallet.increment!(:balance, -10)             # UPDATE ... SET balance = COALESCE(balance,0) - 10
Wallet.update_counters(id, balance: -10)     # то же без объекта
Wallet.where(id: id).update_all("balance = balance - 10")
Wallet.where(id: id, balance: 10..).update_all("balance = balance - 10")  # с условием → rowcount
```

- `increment!` — без валидаций и колбэков, `touch`-ит `updated_at`. Объект в памяти обновляет локально.
- `update_all` — вернёт число строк: `== 1` значит условие прошло. Это замена `with_lock` для простых случаев: одна команда, нет блокировки-ожидания.
- `update_all` принимает хеш или SQL-строку с placeholders: `update_all(["balance = balance - ?", amt])`.
- `upsert_all` — массовая вставка/обновление с `ON CONFLICT`.
- `touch_all`, `delete_all` — той же природы.

Всё это обходит колбэки — после `update_all` объекты в памяти устарели (`reload`).

## Фраза для собеса

«Арифметику — в SQL: `increment!` или `update_all` с условием и проверкой rowcount; это атомарно и не требует блокировки».
"""),

"02-rails/17-enum-predikaty-skoupy-prefix.md": ([
  ("Rails API — ActiveRecord::Enum", A + "ActiveRecord/Enum.html"),
], """
```ruby
class Withdrawal < ApplicationRecord
  enum :status, { pending: 0, processing: 1, sent: 2, failed: 3 }, prefix: true, default: :pending
end

w.status                 # "sent" (строка)
w.status_sent?           # предикат (с prefix: true; без — w.sent?)
w.status_sent!           # update!(status: :sent) — без валидаций? нет, с ними, но без проверки перехода
Withdrawal.status_sent   # scope
Withdrawal.not_status_sent
Withdrawal.statuses      # { "pending" => 0, ... }
where(status: :sent)     # можно символом
```

- Хранить **integer** с явным маппингом (не массив — порядок сломается при вставке). Строковый enum (`{ sent: "sent" }`) — читаемее в БД, чуть больше места; в Postgres можно native enum type, но миграции сложнее.
- `prefix`/`suffix` — обязательно, если у модели несколько enum или имена конфликтуют (`active?` уже есть).
- Невалидное значение → `ArgumentError` при присвоении, не ошибка валидации. Для формы — `validates :status, inclusion:` + `validate: true` опция (7.1).
- Enum **не проверяет переходы**: `failed → sent` пройдёт. Для state machine — guard-методы или gem (`aasm`, `statesman`).
- Rails 7: синтаксис `enum :status, {...}`; старый `enum status: {...}` deprecated в 7.2+.

## Фраза для собеса

«Enum на integer с явным маппингом и prefix; даёт предикаты и скоупы, но переходы между состояниями не контролирует — это пишу сам».
"""),

"02-rails/18-migracii-obratimye-indeksy-algorithm-concurrentl.md": ([
  ("Rails Guides — Active Record Migrations", G + "active_record_migrations.html"),
  ("gem strong_migrations — список опасных операций", "https://github.com/ankane/strong_migrations"),
], """
```ruby
class AddTxidToWithdrawals < ActiveRecord::Migration[7.2]
  disable_ddl_transaction!                        # нужно для concurrently
  def change
    add_column :withdrawals, :txid, :string
    add_index  :withdrawals, :txid, unique: true, algorithm: :concurrently
  end
end
```

- `change` обратим для стандартных операций; `remove_column` без типа и `execute` — нет → `up`/`down` или `reversible do |dir|`.
- `add_index ... algorithm: :concurrently` — без блокировки таблицы на запись (Postgres). Нельзя внутри транзакции → `disable_ddl_transaction!`. Один индекс на миграцию.
- Миграция ≠ данные: бэкфилл — отдельной миграцией или rake-таской батчами (`in_batches`), не в той же транзакции.

Zero-downtime добавить NOT NULL колонку:
1. `add_column` nullable (с `default` в PG 11+ мгновенно);
2. деплой кода, который пишет поле;
3. бэкфилл батчами;
4. `add_check_constraint ... NOT VALID` → `validate_check_constraint` → `change_column_null`.

Опасно без подготовки: `rename_column` (сломает старый код во время деплоя), `change_column` типа (переписывает таблицу), `remove_column` (сначала `ignored_columns`), `add_foreign_key` без `validate: false`.

`schema.rb` vs `structure.sql` — второй, если есть PG-специфика (triggers, enum types). Модели в миграциях не использовать (изменятся) — голый SQL или локальный класс.

## Фраза для собеса

«Индексы — `concurrently` без DDL-транзакции, NOT NULL — через nullable + бэкфилл + constraint; strong_migrations подсказывает опасное».
"""),

"02-rails/19-keshirovanie-fragment-rails-cache-fetch-russian-.md": ([
  ("Rails Guides — Caching with Rails", G + "caching_with_rails.html"),
], """
```ruby
Rails.cache.fetch(["rate", :usdt_btc], expires_in: 30.seconds) do
  RateApi.fetch     # выполнится только при промахе
end
Rails.cache.write/read/delete/exist?
Rails.cache.fetch(key, race_condition_ttl: 5.seconds)   # защита от thundering herd
```

Стора: `:memory_store` (dev, не делится между процессами), `:redis_cache_store` (prod), `:solid_cache_store` (Rails 8, в БД), `:null_store` (test).

**Ключи**: модель отвечает `cache_key_with_version` → `"withdrawals/5-20240101120000"` — `updated_at` внутри ключа = инвалидация через `touch`. Массив `["v2", user, page]` соберётся сам.

**Fragment caching** во view: `<% cache withdrawal do %> ... <% end %>`. **Russian doll** — вложенные фрагменты: внешний ключ зависит от `updated_at` родителя, дочерние `touch: true` на `belongs_to` поднимают изменение наверх. Меняется один ребёнок — перерисовывается только он и родительская обёртка.

- `collection: true` в `render partial:` + кэш → multi-get.
- HTTP-кэш: `fresh_when(withdrawal)` / `stale?` → 304 по ETag/Last-Modified.
- Low-level: мемоизация `@x ||=` (на один объект/запрос), `RequestStore`/`ActiveSupport::CurrentAttributes` (на запрос).
- Инвалидация — главная боль: ключ со временем/версией лучше явных `delete`.

## Фраза для собеса

«`Rails.cache.fetch` с ключом, в который входит версия/updated_at; во view — фрагменты по `cache_key_with_version` и `touch: true` вверх».
"""),

"02-rails/20-servisnye-obekty-interactors-form-objects-gde-lo.md": ([
  ("thoughtbot — Skinny Controllers, Skinny Models", "https://thoughtbot.com/blog/skinny-controllers-skinny-models"),
  ("dry-rb — dry-monads", "https://dry-rb.org/gems/dry-monads/"),
], """
Где жить логике «создать вывод: списать, записать, поставить джоб»? Не в контроллере (не тестируется без HTTP, не переиспользуется) и не в модели (модель начинает знать про Sidekiq, почту, другие модели — «god object»).

**Service object** — класс с одной публичной операцией:
```ruby
class CreateWithdrawal
  Result = Data.define(:success?, :withdrawal, :error)

  def initialize(user:, params:) = (@user, @params = user, params)

  def call
    ActiveRecord::Base.transaction do
      wallet = @user.wallet.lock!
      return Result.new(false, nil, :insufficient) if wallet.balance < total
      wallet.decrement!(:balance, total)
      w = wallet.withdrawals.create!(@params.merge(status: :pending))
      ProcessWithdrawalWorker.perform_async(w.id)   # лучше after_commit
      Result.new(true, w, nil)
    end
  end
end
```
Контроллер: вызвать, по результату `render`/`redirect`. Тест — чистый Ruby.

- Возвращать результат-объект, не bool и не исключения для ожидаемых исходов. dry-monads `Success/Failure` — стандартный вариант.
- **Form object** — когда форма не 1:1 с моделью (регистрация = user + wallet + соглашение): `include ActiveModel::Model`, валидации, `save` создаёт всё.
- **Query object** — сложная выборка в классе с `call` → relation.
- **Policy** — авторизация (Pundit). **Presenter/Decorator** — логика отображения. **Interactor/Operation** (gem interactor, dry-operation, trailblazer) — сервис с шагами и откатом.

Модель остаётся для: валидаций, скоупов, простых методов над своими данными.

## Фраза для собеса

«Контроллер тонкий, модель про свои данные, сценарии — в сервисах с явным результатом; формы не 1:1 — form object».
"""),

"02-rails/21-concerns-kogda-ok-kogda-zlo.md": ([
  ("Rails API — ActiveSupport::Concern", A + "ActiveSupport/Concern.html"),
  ("DHH — Put chubby models on a diet with concerns", "https://signalvnoise.com/posts/3372-put-chubby-models-on-a-diet-with-concerns"),
], """
```ruby
module Trackable
  extend ActiveSupport::Concern
  included do
    has_many :events, as: :trackable
    scope :tracked, -> { where(tracked: true) }
  end
  class_methods do
    def track_all! = update_all(tracked: true)
  end
  def track!(kind) = events.create!(kind:)
end
class Withdrawal < ApplicationRecord; include Trackable; end
```

`Concern` решает две вещи: `included do` выполняет DSL (ассоциации, скоупы) в контексте класса, и зависимости между concern'ами работают.

**Ок**, когда это настоящее горизонтальное поведение, которое включают **несколько** моделей и которое не лезет в их внутренности: soft-delete, slug, tokens, auditing, `Searchable`.

**Зло**, когда:
- concern один и используется одной моделью — это просто порезанный файл; логика размазана, `grep` по методу ведёт в три места;
- concern обращается к полям/методам хоста, которых сам не объявляет — скрытая связь, модуль нельзя понять изолированно;
- через него тестируют «модель похудела», а поведение не выделено в объект.

Альтернатива — composition: сервис/value object/отдельный класс с явной зависимостью. Проще тестировать и читать.

## Фраза для собеса

«Concern — для поведения, общего для нескольких моделей и самодостаточного; для декомпозиции одной жирной модели лучше объекты».
"""),

"02-rails/22-actionmailer-deliver-now-vs-deliver-later.md": ([
  ("Rails Guides — Action Mailer Basics", G + "action_mailer_basics.html"),
], """
```ruby
UserMailer.withdrawal_sent(user, withdrawal).deliver_now     # синхронно, прямо сейчас, в этом потоке
UserMailer.withdrawal_sent(user, withdrawal).deliver_later   # через ActiveJob в очередь
UserMailer.with(user:, withdrawal:).withdrawal_sent.deliver_later(wait: 1.minute)
```

- `deliver_now` блокирует запрос на время SMTP (сотни мс — секунды); при падении почты падает запрос; внутри транзакции — письмо уйдёт, а транзакция может откатиться.
- `deliver_later` сериализует аргументы через GlobalID (модели → `gid://app/User/1`), в джобе загружает заново. Запись должна быть **закоммичена** → вызывать из `after_commit`, не `after_save`. Если запись удалят до отправки — `DeserializationError`.
- `deliver_later` требует настроенного `queue_adapter` (Sidekiq/Solid Queue); с `:async` в dev письма шлются в потоке процесса и теряются при рестарте.
- Параметры лучше через `.with(...)` (параметризованные мейлеры) — и шаблон, и `params` одинаково.
- Тесты: `assert_enqueued_email_with`, `have_enqueued_mail`, `ActionMailer::Base.deliveries` при `delivery_method = :test`; `perform_enqueued_jobs` чтобы прогнать.
- Preview: `test/mailers/previews` → `/rails/mailers`.

## Фраза для собеса

«Из приложения — `deliver_later` из `after_commit`; `deliver_now` — только в джобе или консоли».
"""),

"02-rails/23-activejob-vs-nativnyj-sidekiq.md": ([
  ("Rails Guides — Active Job Basics", G + "active_job_basics.html"),
  ("Sidekiq wiki — Active Job", "https://github.com/sidekiq/sidekiq/wiki/Active-Job"),
], """
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
"""),

"02-rails/24-api-render-json-serializatory-as-json-only-jbuil.md": ([
  ("Rails Guides — Using Rails for API-only Applications", G + "api_app.html"),
  ("gem blueprinter", "https://github.com/procore-oss/blueprinter"),
], """
```ruby
render json: withdrawal
# вызывает withdrawal.as_json → to_json. ВСЕ колонки, включая внутренние (wallet_id, lock_version…)

render json: withdrawal.as_json(only: [:id, :amount, :status], methods: [:total], include: { wallet: { only: :address } })
render json: { data: ..., meta: ... }, status: :created
head :no_content
```

Переопределять `as_json` в модели — быстро, но один формат на все эндпоинты. Лучше отдельный слой:

- **Blueprinter / Alba / Panko** — классы-сериализаторы: `WithdrawalBlueprint.render(w, view: :detailed)`. Быстрые, явные.
- **jbuilder** — шаблоны `.json.jbuilder` во views, удобно для вложенных структур, медленнее.
- **ActiveModel::Serializers** — исторический, полуживой.
- **JSON:API** (`jsonapi-serializer`) — если нужен стандарт.

Правила API:
- Явный белый список полей (приватные данные, внутренние id).
- Деньги — строкой или integer в минимальных единицах, не float в JSON.
- Статусы — `status:` HTTP-кодом + тело с ошибкой единого формата `{ error: { code:, message: } }`.
- `rescue_from ActiveRecord::RecordNotFound, with: :not_found` в `ApplicationController`.
- Пагинация (`pagy`), версионирование (`/api/v1`), `Content-Type: application/json`.
- `--api` режим: `ActionController::API`, без views/cookies/CSRF.

## Фраза для собеса

«`render json: model` отдаёт всё — всегда сериализатор с белым списком полей; ошибки — единым форматом и правильными кодами».
"""),

"02-rails/25-avtorizaciya-pundit-cancancan-idor-current-user-.md": ([
  ("Pundit", "https://github.com/varvet/pundit"),
  ("OWASP — IDOR", "https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html"),
], """
Аутентификация — *кто ты*. Авторизация — *что тебе можно*. Самая частая дыра — **IDOR**: `Withdrawal.find(params[:id])` отдаёт чужую запись, достаточно перебрать id.

```ruby
# IDOR
@w = Withdrawal.find(params[:id])
# Фикс — скоупить через владельца: чужой id → 404
@w = current_user.withdrawals.find(params[:id])
```

Для ролей и правил — Pundit:
```ruby
class WithdrawalPolicy < ApplicationPolicy
  def show?    = record.user == user || user.admin?
  def create?  = user.verified?
  class Scope < Scope
    def resolve = user.admin? ? scope.all : scope.where(user:)
  end
end

# контроллер
def show
  @w = authorize Withdrawal.find(params[:id])     # NotAuthorizedError → rescue_from → 403
end
def index
  @ws = policy_scope(Withdrawal)
end
after_action :verify_authorized      # забыл authorize → ошибка в dev/test
```

CanCanCan — альтернатива: одна `Ability` с `can :read, Withdrawal, user_id: user.id`; удобно для простых CRUD, хуже масштабируется.

Ещё: не доверять `params[:user_id]`; проверять права и в джобах/сервисах, не только в контроллере; admin-функции — отдельный namespace + проверка роли.

## Фраза для собеса

«Записи всегда через `current_user.xxx.find` — чужое становится 404; правила — в policy-объектах с `verify_authorized`».
"""),

"02-rails/26-autentifikaciya-devise-sessii-vs-tokeny.md": ([
  ("Devise", "https://github.com/heartcombo/devise"),
  ("Rails Guides — Security: Sessions", G + "security.html#sessions"),
  ("Rails 8 authentication generator", "https://github.com/rails/rails/blob/main/railties/lib/rails/generators/rails/authentication/USAGE"),
], """
**Сессии (cookie)** — классический web: после логина `session[:user_id] = user.id`; Rails хранит сессию в подписанной+зашифрованной cookie (`cookie_store`). Защита CSRF обязательна (`protect_from_forgery`, токен в формах). Логаут = удалить ключ. Подходит для серверного рендера и SPA на том же домене.

**Токены** — для API и мобильных: клиент шлёт `Authorization: Bearer <token>`.
- Opaque token в БД (`has_secure_token`, хранить хеш) — можно отозвать, просто.
- JWT — самодостаточный, stateless, не отзывается до истечения (нужен короткий TTL + refresh token). Не хранить в нём секреты.
CSRF не актуален, но XSS опаснее: токен в `localStorage` уязвим; `httpOnly` cookie + SameSite — компромисс.

Инструменты:
- **Devise** — всё из коробки: регистрация, подтверждение, восстановление, lockable, `has_secure_password` под капотом (bcrypt). Много магии, сложно кастомизировать.
- **Rails 8 `bin/rails generate authentication`** — минимальный встроенный генератор: сессии в БД, bcrypt, сброс пароля. Прозрачный код в проекте.
- `has_secure_password` руками — для API достаточно 30 строк.

Гигиена: bcrypt/argon2, никаких plaintext, ограничение попыток, `secure`/`httpOnly`/`SameSite` cookie, ротация сессии при логине (`reset_session`).

## Фраза для собеса

«Сессии в cookie + CSRF для web; токены для API — opaque с хешем в БД или короткоживущий JWT; пароли только через bcrypt».
"""),

"02-rails/27-rails-credentials-env-env.md": ([
  ("Rails Guides — Custom Credentials", G + "security.html#custom-credentials"),
  ("gem dotenv", "https://github.com/bkeepers/dotenv"),
], """
Секреты (ключи API, приватный ключ кошелька, пароли БД) — **не в git**.

**ENV** — 12-factor, стандарт для Docker/Heroku/K8s:
```ruby
ENV.fetch("BITCOIN_WIF")           # fetch — упасть сразу, если не задан
ENV.fetch("FEE_SAT", "1000").to_i  # дефолт
```
В dev — `.env` через gem dotenv (файл в `.gitignore`, `.env.example` — в репо с пустыми значениями). Плюсы: платформа-независимо, легко ротировать. Минусы: видны в `ps`/дампах окружения, нет структуры.

**Rails credentials** — зашифрованный YAML в репо, ключ отдельно:
```
bin/rails credentials:edit --environment production   # config/credentials/production.yml.enc + .key
Rails.application.credentials.dig(:bitcoin, :wif)
```
Ключ — через `RAILS_MASTER_KEY` ENV на сервере. Плюсы: структура, версионируется вместе с кодом. Минусы: один ключ на всё, ротация = перешифровать, в контейнерах всё равно нужен ENV для ключа.

Практика: инфраструктурные (DATABASE_URL, REDIS_URL) — ENV; прикладные — либо-либо, лишь бы последовательно. Не логировать (`filter_parameters`), не коммитить `.key`, в тестовом задании — `.env.example` + README.

## Фраза для собеса

«Секреты в ENV через `fetch` или в credentials с мастер-ключом из ENV; в репо — только `.env.example`».
"""),

"02-rails/28-rack-middleware-napisat-svoe-za-5-strok.md": ([
  ("Rails Guides — Rails on Rack", G + "rails_on_rack.html"),
  ("Rack spec", "https://github.com/rack/rack/blob/main/SPEC.rdoc"),
], """
Middleware — объект, который получает следующее приложение в `initialize` и обрабатывает `call(env)`:

```ruby
class RequestTimer
  def initialize(app) = @app = app

  def call(env)
    start = Process.clock_gettime(Process::CLOCK_MONOTONIC)
    status, headers, body = @app.call(env)       # передать дальше по цепочке
    headers["X-Runtime-Ms"] = ((Process.clock_gettime(Process::CLOCK_MONOTONIC) - start) * 1000).round(1).to_s
    [status, headers, body]
  end
end

# config/application.rb
config.middleware.use RequestTimer
config.middleware.insert_before Rack::Runtime, RequestTimer
config.middleware.delete Rack::ETag
```

- `env` — хеш: `REQUEST_METHOD`, `PATH_INFO`, `HTTP_*` заголовки, `rack.input`. Удобно обернуть: `req = Rack::Request.new(env)`.
- Можно не вызывать `@app` — вернуть ответ сразу (maintenance mode, rate limit, блок по IP): `return [503, {"content-type"=>"text/plain"}, ["down"]]`.
- `body` должен отвечать на `each` (массив строк) и желательно `close`.
- Один экземпляр на процесс — **без состояния в иварах** (многопоточность Puma).
- `rails middleware` — список. Rails сам — тоже middleware-стек поверх роутера.

Примеры из жизни: `Rack::Attack` (rate limit), `Rack::Cors`, request id, свой logger, трассировка.

## Фраза для собеса

«Класс с `initialize(app)` и `call(env)`, возвращающий `[status, headers, body]`; вставляется через `config.middleware`; без состояния в экземпляре».
"""),

"02-rails/29-config-eager-load-autoloading-zeitwerk-odna-fraz.md": ([
  ("Rails Guides — Autoloading and Reloading Constants", G + "autoloading_and_reloading_constants.html"),
], """
**Zeitwerk** (Rails 6+) — автозагрузчик: имя файла ↔ имя константы. `app/services/create_withdrawal.rb` → `CreateWithdrawal`; `app/models/btc/wallet.rb` → `Btc::Wallet`. Не нужно `require` своих файлов. Любая папка в `app/` — корень неймспейса (`app/services/` не даёт префикс `Services::`).

- Несовпадение имени → `NameError: uninitialized constant` или «expected file to define constant». Проверка: `bin/rails zeitwerk:check`.
- Акронимы: `app/lib/api_client.rb` → `ApiClient`; хочешь `APIClient` — `inflect.acronym "API"`.
- `lib/` не автозагружается по умолчанию; Rails 7.1 — `config.autoload_lib(ignore: %w[tasks])`.

**eager_load**:
- `false` (dev/test): константы грузятся при первом обращении, код перезагружается при изменении файла (Reloader).
- `true` (prod): всё загружается при старте — ошибки видны сразу, нет паузы на первом запросе, copy-on-write память для форков Puma. В CI тоже стоит включить, чтобы ловить ошибки загрузки.

Перезагрузка в dev: `reload!` в консоли; объекты, созданные до перезагрузки, принадлежат старым классам — `===` может удивить.

## Фраза для собеса

«Zeitwerk грузит константы по именам файлов без require; `eager_load` в prod — всё при старте, в dev — лениво с перезагрузкой».
"""),

"02-rails/30-rails-7-7-1-7-2-8-chto-novogo-hotwire-normalizes.md": ([
  ("Rails 7.1 release notes", G + "7_1_release_notes.html"),
  ("Rails 7.2 release notes", G + "7_2_release_notes.html"),
  ("Rails 8.0 release notes", G + "8_0_release_notes.html"),
], """
Знать на уровне «что появилось и зачем»:

**7.0** — Hotwire (Turbo + Stimulus) вместо SPA по умолчанию; import maps без Node; `load_async` для параллельных запросов; encrypted attributes (`encrypts :wif`); `ActiveRecord::Base.transaction` + `after_commit` стали надёжнее.

**7.1** — `normalizes :email, with: ->(e) { e.strip.downcase }`; `generates_token_for :password_reset, expires_in: 15.minutes`; `ActiveRecord::Base.with` (CTE); композитные первичные ключи; `config.autoload_lib`; Dockerfile в `rails new`; `authenticate_by` против timing-атак; `Rails.error.report`; async queries.

**7.2** — dev-контейнеры; `enqueue_after_transaction_commit` для ActiveJob; browser version guard (`allow_browser`); Rate limiting в контроллерах (`rate_limit to: 10, within: 1.minute`); `ActiveRecord.after_all_transactions_commit`; Puma threads по умолчанию 3; YJIT включён по умолчанию.

**8.0** — «Solid trifecta»: Solid Queue (джобы в БД, замена Sidekiq для небольших проектов), Solid Cache, Solid Cable; Kamal 2 для деплоя; Propshaft вместо Sprockets; встроенный генератор аутентификации; `params.expect`; SQLite готов к prod.

Если спросят «что нравится из нового» — выбрать одно и обосновать: например, `normalizes` убирает `before_validation`-бойлерплейт, `rate_limit` — зачем Rack::Attack для простых случаев.

## Фраза для собеса

«7.1 — normalizes и token generation, 7.2 — rate limit и enqueue after commit, 8 — Solid Queue/Cache и встроенная аутентификация».
"""),
}
