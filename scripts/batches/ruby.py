R = "https://docs.ruby-lang.org/en/master/"
ITEMS = {
"01-ruby-yazyk/01-bloki-yield-block-given-block.md": ([
  ("Ruby docs — Calling Methods: Block Argument", R + "syntax/calling_methods_rdoc.html#label-Block+Argument"),
  ("Ruby docs — Methods: yield", R + "syntax/methods_rdoc.html#label-Block+Argument"),
], """
Блок — кусок кода, который передаётся методу **синтаксически**, а не как объект. Любой метод может принять блок, даже не объявляя его.

```ruby
def twice
  return enum_for(:twice) unless block_given?   # идиома: без блока вернуть Enumerator
  yield 1
  yield 2
end

twice { |x| puts x }
```

- `yield` — вызвать блок, передав аргументы. Быстрее, чем `block.call`, т.к. не создаётся объект Proc.
- `block_given?` — передали ли блок. Без проверки `yield` упадёт с `LocalJumpError`.
- `&block` в сигнатуре — материализовать блок в `Proc`, чтобы сохранить или передать дальше.
- `&` при вызове — обратное: `arr.each(&my_proc)`.

```ruby
def wrap(&block)        # block — Proc
  log { block.call }    # можно передать дальше
end
```

Блок видит локальные переменные места, где написан (замыкание), и может их менять.

## Фраза для собеса

«Блок — это не объект, а синтаксис; `yield` вызывает его напрямую, `&block` превращает в Proc, когда блок нужно сохранить или передать».
"""),

"01-ruby-yazyk/03-symbol-to-proc-name-numbered-params-1-it-3-4.md": ([
  ("Ruby docs — Symbol#to_proc", R + "Symbol.html#method-i-to_proc"),
  ("Ruby 3.4 release notes — `it`", "https://www.ruby-lang.org/en/news/2024/12/25/ruby-3-4-0-released/"),
], """
Три способа написать короткий блок с одним аргументом:

```ruby
users.map(&:name)          # Symbol#to_proc: вызвать метод :name у каждого
users.map { _1.name }      # numbered params, Ruby 2.7
users.map { it.name }      # `it`, Ruby 3.4
```

`&:name` работает так: `&` просит объект стать Proc → `Symbol#to_proc` возвращает `proc { |obj, *args| obj.send(:name, *args) }`.

Ограничения `&:sym`: нельзя передать аргументы (`map(&:round(2))` не бывает) и нельзя обратиться к внешней переменной.

`_1`/`_2` — для двух аргументов (`hash.map { "#{_1}=#{_2}" }`). `it` — только один. Нельзя смешивать `it` и `_1` в одном блоке; если в блоке есть явный `|x|`, они недоступны.

Стиль: для одной короткой операции — `&:sym`; для выражения — `it`; если блок длиннее строки — обычное имя.

## Фраза для собеса

«`&:name` — это `Symbol#to_proc`, удобно для одного вызова метода; `it` и `_1` — неявные параметры для коротких блоков».
"""),

"01-ruby-yazyk/04-enumerable-map-select-filter-reject-reduce-injec.md": ([
  ("Ruby docs — Enumerable", R + "Enumerable.html"),
], """
`Enumerable` — модуль, который даёт ~60 методов любому классу с `each`. `Array`, `Hash`, `Range`, `Set`, `Struct` — все его включают.

| Метод | Возвращает | Пример |
|---|---|---|
| `map` / `collect` | новый массив той же длины | `[1,2].map { _1 * 2 } # [2,4]` |
| `select` / `filter` | элементы, где блок истинен | `(1..6).select(&:even?)` |
| `reject` | где блок ложен | `list.reject(&:nil?)` |
| `reduce` / `inject` | одно значение | `[1,2,3].reduce(:+) # 6` |
| `sum` | сумма (точнее для float) | `prices.sum`, `items.sum(&:price)` |

`reduce(initial) { |acc, x| }` — аккумулятор. `reduce(:+)` — через символ. `sum` предпочтительнее `reduce(:+)`: для float использует суммирование Кахана и быстрее.

`filter` — алиас `select` (2.6+), добавлен ради привычки из JS.

Все они возвращают **новые объекты**; исходную коллекцию не меняют. Варианты с `!` (`select!`, `map!`) есть только у `Array`/`Hash`.

## Фраза для собеса

«Любой класс с `each` и `include Enumerable` получает map/select/reduce бесплатно; `sum` точнее и быстрее `reduce(:+)`».
"""),

"01-ruby-yazyk/05-filter-map-flat-map-each-with-object.md": ([
  ("Ruby docs — Enumerable#filter_map", R + "Enumerable.html#method-i-filter_map"),
  ("Ruby docs — Enumerable#each_with_object", R + "Enumerable.html#method-i-each_with_object"),
], """
```ruby
# filter_map — map + отбросить nil и false. Один проход вместо двух.
txids = withdrawals.filter_map { _1[:txid] }
# == withdrawals.map { _1[:txid] }.compact, но compact не убирает false

# flat_map — map + разворачивание одного уровня
orders.flat_map(&:items)        # [[a,b],[c]] → [a,b,c]

# each_with_object — свернуть в объект-аккумулятор без return из блока
by_id = users.each_with_object({}) { |u, h| h[u.id] = u }
```

`each_with_object(obj)` vs `reduce(obj)`: в `reduce` блок обязан **вернуть** аккумулятор (легко забыть), в `each_with_object` объект передаётся по ссылке и мутируется. Для хешей и массивов — `each_with_object`; для чисел и строк (иммутабельных) — `reduce`.

`flat_map` разворачивает ровно один уровень; `flatten` — все.

## Фраза для собеса

«`filter_map` — когда из map часть результатов надо выкинуть; `flat_map` — когда каждый элемент даёт список; `each_with_object` — когда собираю хеш».
"""),

"01-ruby-yazyk/06-each-cons-each-slice-chunk-while-slice-when.md": ([
  ("Ruby docs — Enumerable#each_cons", R + "Enumerable.html#method-i-each_cons"),
  ("Ruby docs — Enumerable#chunk_while", R + "Enumerable.html#method-i-chunk_while"),
], """
```ruby
[1,2,3,4].each_cons(2).to_a    # [[1,2],[2,3],[3,4]]  — скользящее окно
[1,2,3,4].each_slice(2).to_a   # [[1,2],[3,4]]        — разбиение на куски
```

`each_cons(n)` — для сравнения соседей: разрывы во времени, рост/падение, дубликаты подряд.
`each_slice(n)` — батчи для API, пагинация, `in_groups_of` без Rails.

```ruby
# chunk_while — группировать подряд идущие, пока условие между соседями истинно
[1,2,4,5,7].chunk_while { |a, b| b == a + 1 }.to_a   # [[1,2],[4,5],[7]]

# slice_when — то же, но условие описывает РАЗРЫВ
[1,2,4,5,7].slice_when { |a, b| b != a + 1 }.to_a    # то же самое
```

Пример из тестового: максимальный интервал между выводами —
`times.each_cons(2).map { |a, b| b - a }.max`.

Все четыре без блока возвращают `Enumerator`, можно цеплять `.map`, `.to_a`, `.lazy`.

## Фраза для собеса

«`each_cons` — окно, `each_slice` — батчи, `chunk_while`/`slice_when` — группы подряд идущих по условию между соседями».
"""),

"01-ruby-yazyk/07-group-by-partition-tally-zip-min-by-max-by-sort-.md": ([
  ("Ruby docs — Enumerable#tally", R + "Enumerable.html#method-i-tally"),
  ("Ruby docs — Enumerable#partition", R + "Enumerable.html#method-i-partition"),
], """
```ruby
list.group_by(&:status)        # { "sent" => [...], "failed" => [...] }
list.partition { _1.big? }     # [[big...], [small...]]  — ровно две группы
list.map(&:status).tally       # { "sent" => 10, "failed" => 2 }  (2.7+)
list.tally_by(&:status)        # то же короче (3.1+)

[1,2].zip([:a,:b])             # [[1,:a],[2,:b]]
keys.zip(values).to_h          # быстрый способ собрать хеш

list.max_by(&:fee)             # элемент с максимальным fee (не само значение)
list.min_by(2, &:fee)          # два минимальных
list.sort_by { [-_1.priority, _1.created_at] }   # многоключевая сортировка
```

`sort_by` вычисляет ключ один раз на элемент (Schwartzian transform) — быстрее `sort { |a,b| ... }` при дорогом ключе. Для обратного порядка по числу — минус; по строкам — `.reverse` или `sort_by { ... }.reverse`.

`partition` vs `group_by`: когда групп ровно две и важны обе — `partition` (деструктуризация `big, small = ...`).

## Фраза для собеса

«`tally` считает частоты, `group_by` раскладывает по ключу, `partition` делит на два, `max_by` возвращает элемент, а не значение».
"""),

"01-ruby-yazyk/08-find-detect-any-all-none-count-s-blokom.md": ([
  ("Ruby docs — Enumerable#find", R + "Enumerable.html#method-i-find"),
], """
```ruby
list.find { _1.id == 5 }        # первый подходящий или nil (detect — алиас)
list.find_index { ... }         # его индекс

list.any? { _1.failed? }        # есть хоть один
list.all?(&:valid?)             # все
list.none?(&:nil?)              # ни одного
list.one? { ... }               # ровно один

list.count                      # размер
list.count(&:hot?)              # сколько удовлетворяют
list.count("x")                 # сколько равны аргументу
```

Паттерн-аргумент (2.5+): `any?(Integer)`, `all?(/re/)`, `none?(nil)` — через `===`.

Ловушки:
- `[].all?` → `true`, `[].any?` → `false` (вакуумная истина).
- `any?` без блока проверяет истинность элементов: `[nil, false].any?` → `false`.
- `find` останавливается на первом совпадении; `select.first` — пройдёт всё.
- В Rails `User.find { }` — это Enumerable на загруженных записях, а `User.find(id)` — SQL. `where(...).exists?` вместо `any?`, чтобы не грузить все строки.

## Фраза для собеса

«`find` возвращает элемент или nil и останавливается на первом; `any?/all?/none?` — предикаты, помню про пустую коллекцию».
"""),

"01-ruby-yazyk/09-lenivye-perechisleniya-lazy-enumerator-each-entr.md": ([
  ("Ruby docs — Enumerator::Lazy", R + "Enumerator/Lazy.html"),
  ("Ruby docs — Enumerator", R + "Enumerator.html"),
], """
Обычные `map`/`select` жадные: каждый создаёт полный промежуточный массив. `lazy` делает цепочку поэлементной.

```ruby
(1..Float::INFINITY).lazy.map { _1 * 2 }.select { _1 % 3 == 0 }.first(3)
# => [6, 12, 18]  — без lazy зависло бы на бесконечном map
```

Когда полезно: бесконечные/очень большие последовательности, чтение файла построчно, пагинация API, когда нужно `first(n)` после фильтров.

`Enumerator` — объект-итератор. Создать:
```ruby
e = Enumerator.new { |y| y << 1; y << 2 }   # y — Yielder
e.next   # 1 — внешняя итерация
[1,2,3].each   # без блока → Enumerator
```

Идиома `return enum_for(:method) unless block_given?` делает свой метод совместимым с цепочками (`my_each.with_index`).

`each_entry` — редкий; для объектов, чей `each` отдаёт несколько значений, собирает их в массив. Знать, что есть.

`lazy` дороже на маленьких коллекциях — накладные расходы на каждый элемент. Применять, когда есть реальная причина.

## Фраза для собеса

«`lazy` превращает цепочку в конвейер по одному элементу — нужен для бесконечных последовательностей и ранней остановки; на малых массивах только замедлит».
"""),

"01-ruby-yazyk/10-comparable-i-enumerable-v-svoem-klasse-each.md": ([
  ("Ruby docs — Comparable", R + "Comparable.html"),
  ("Ruby docs — Enumerable", R + "Enumerable.html"),
], """
Два модуля-«миксина», которые дают много методов за реализацию одного.

```ruby
class Money
  include Comparable
  attr_reader :cents
  def initialize(cents) = @cents = cents
  def <=>(other) = cents <=> other.cents   # -1, 0, 1 или nil
end

Money.new(5) < Money.new(10)     # true
[m3, m1, m2].sort.first          # sort использует <=>
m.between?(a, b); m.clamp(a, b)
```

`Comparable` даёт `< <= == >= > between? clamp` из одного `<=>`. Внимание: он переопределяет `==` через `<=>` — объекты равны, если `<=>` вернул 0.

```ruby
class Wallet
  include Enumerable
  def each(&block)
    return enum_for(:each) unless block
    @utxos.each(&block)
  end
end

wallet.sum(&:value); wallet.select(&:confirmed?); wallet.min_by(&:value); wallet.lazy
```

`Enumerable` даёт всё — map/select/sort_by/include?/first/to_a — из одного `each`. `each` должен `yield`-ить элементы по одному.

## Фраза для собеса

«Реализую `<=>` и включаю `Comparable` — получаю сравнения и sort; реализую `each` и включаю `Enumerable` — получаю всю коллекционную алгебру».
"""),

"01-ruby-yazyk/11-struct-data-3-2-openstruct-kogda-chto.md": ([
  ("Ruby docs — Data", R + "Data.html"),
  ("Ruby docs — Struct", R + "Struct.html"),
], """
```ruby
Point = Struct.new(:x, :y, keyword_init: true)
p = Point.new(x: 1, y: 2); p.x = 5          # мутабельный, есть сеттеры, ==, to_a, to_h

Coord = Data.define(:lat, :lng)             # Ruby 3.2
c = Coord.new(lat: 1, lng: 2)               # иммутабельный: нет сеттеров, frozen
c.with(lat: 3)                              # копия с изменением
# Data требует все аргументы — забыл один → ArgumentError

require "ostruct"
o = OpenStruct.new(a: 1); o.b = 2           # произвольные поля через method_missing
```

Когда что:
- **`Data`** — value object: деньги, координаты, DTO из API. По умолчанию для новых классов-значений.
- **`Struct`** — когда нужна мутабельность или позиционные аргументы; быстрее Data на создание, но позволяет случайно изменить.
- **`OpenStruct`** — почти никогда в продакшене: медленный (method_missing + define на каждом объекте), ломает `respond_to?`, с 3.5 вынесен из stdlib в gem. Для прототипов и тестов.

Оба поддерживают pattern matching: `case c in {lat:, lng:}`.

## Фраза для собеса

«Для неизменяемых значений — `Data`, для мутабельных записей — `Struct`, `OpenStruct` — только в скриптах».
"""),

"01-ruby-yazyk/12-pattern-matching-case-in-dekonstrukciya-heshej-m.md": ([
  ("Ruby docs — Pattern matching", R + "syntax/pattern_matching_rdoc.html"),
], """
```ruby
case response
in { status: 200, body: { txid: String => txid } }
  txid
in { status: 400.., error: msg }
  raise ApiError, msg
in [first, *rest]                      # массив: первый и остальные
in Integer | Float => n if n > 0      # альтернатива + guard
else
  raise "unexpected"
end
```

- Хеши матчатся **частично**: лишние ключи не мешают. Массивы — точно по длине (кроме `*`).
- `=> name` привязывает значение; `^var` — использовать существующую переменную, а не связать новую.
- `case/in` без `else` при промахе бросает `NoMatchingPatternError` — это фича: явный контракт.
- Однострочный: `config => { host:, port: }` (бросает) и `value in { ok: true }` (bool).
- Свои классы: реализовать `deconstruct` (для массивного паттерна) и `deconstruct_keys(keys)` (для хешевого). `Struct`/`Data` уже умеют.

С dry-monads: `case result in Success(value) ... in Failure[:not_found, msg]`.

Где уместно: разбор JSON/API-ответов, result-объектов, AST. Где нет: простой `if x.is_a?`.

## Фраза для собеса

«`case/in` деконструирует хеши и массивы с привязкой переменных и guard'ами; хеши матчатся частично, отсутствие `else` — ошибка при промахе».
"""),

"01-ruby-yazyk/13-hash-fetch-vs-dig-transform-values-to-h-s-blokom.md": ([
  ("Ruby docs — Hash", R + "Hash.html"),
], """
```ruby
h = { a: 1 }
h[:b]                  # nil — тихо
h.fetch(:b)            # KeyError — громко; для обязательных ключей (ENV.fetch("DB_URL"))
h.fetch(:b, 0)         # дефолт
h.fetch(:b) { compute } # ленивый дефолт

deep = { user: { wallet: { balance: 5 } } }
deep.dig(:user, :wallet, :balance)   # 5; nil, если любой уровень отсутствует
deep[:user][:nope][:x]               # NoMethodError на nil

h.transform_values { _1 * 2 }        # новый хеш, те же ключи
h.transform_keys(&:to_s)             # строки ↔ символы
h.filter_map / h.select { |k, v| }   # select на хеше возвращает хеш
h.sum { |k, v| v }
list.to_h { |x| [x.id, x] }          # to_h с блоком — пары
h.each_with_object({}) { |(k, v), acc| ... }   # деструктуризация пары
```

Default proc — ловушка:
```ruby
Hash.new([])      # ОДИН общий массив на все ключи — h[:a] << 1 засоряет всех
Hash.new { |h, k| h[k] = [] }   # правильно
```

Хеши упорядочены (с 1.9) по порядку вставки. Ключи-строки `dup`-аются и замораживаются при вставке.

## Фраза для собеса

«`fetch` для обязательного, `dig` для вложенного без nil-проверок, `transform_values` вместо map+to_h, и помню про общий объект в `Hash.new([])`».
"""),

"01-ruby-yazyk/14-stroki-frozen-string-literal-freeze-dup-interpol.md": ([
  ("Ruby docs — String", R + "String.html"),
  ("Ruby 3.4 — chilled strings (release notes)", "https://www.ruby-lang.org/en/news/2024/12/25/ruby-3-4-0-released/"),
], """
Строки в Ruby **мутабельны** (`<<`, `upcase!`, `[]=`). Это отличает их от JS/Python.

```ruby
# frozen_string_literal: true     ← магический комментарий в начале файла
s = "abc"; s << "d"               # FrozenError
s = +"abc"                        # +str — размороженная копия (dup)
s = "abc".dup
```

- `freeze` — делает объект иммутабельным (поверхностно: `[a, b].freeze` не замораживает элементы).
- `frozen?` — проверка. Литералы-символы, числа, nil — всегда frozen.
- Зачем: одинаковые frozen-литералы дедуплицируются в памяти, меньше аллокаций; и защита от случайной мутации константы (`API_URL << "/v2"`).
- Ruby 3.4: литералы без комментария — «chilled»: мутация даёт warning, в будущем — ошибка. Привыкай писать комментарий везде (RuboCop требует).

Интерполяция `"#{a}#{b}"` создаёт одну новую строку — быстрее, чем `a + b` (две аллокации) и читабельнее. `<<` мутирует на месте — лучший вариант в циклах накопления.

Кодировка: `"é".bytesize` → 2, `.length` → 1; `force_encoding` не конвертирует, `encode` — да.

## Фраза для собеса

«Строки мутабельны, поэтому ставлю `frozen_string_literal`; для сборки строк — интерполяция или `<<`, не `+` в цикле».
"""),

"01-ruby-yazyk/15-moduli-include-vs-extend-vs-prepend-method-looku.md": ([
  ("Ruby docs — Module#prepend", R + "Module.html#method-i-prepend"),
  ("Ruby docs — Module#ancestors", R + "Module.html#method-i-ancestors"),
], """
```ruby
module Loud; def hi = "HI " + super; end

class A; include Loud; end   # методы модуля — экземплярам, в цепочке ПОСЛЕ класса
class B; extend Loud;  end   # методы модуля — самому объекту B (как класс-методы)
class C; prepend Loud; end   # экземплярам, но в цепочке ПЕРЕД классом
```

Порядок поиска метода (`ancestors`):

```
C.ancestors  # [Loud, C, Object, Kernel, BasicObject]   ← prepend: модуль раньше класса
A.ancestors  # [A, Loud, Object, Kernel, BasicObject]   ← include: модуль после
```

`super` идёт по этой цепочке вправо. Поэтому `prepend` — способ обернуть существующий метод (логирование, кэш) без alias_method-хаков: модульный `hi` вызовется первым и через `super` дойдёт до C#hi.

`extend` на объекте — добавить методы одному экземпляру: `obj.extend(Mod)`.

Идиома «и то и другое»:
```ruby
module Mod
  def self.included(base) = base.extend(ClassMethods)
  module ClassMethods; ...; end
end
```
В Rails это `ActiveSupport::Concern` с `class_methods do`.

Singleton-класс: `extend` = `include` в singleton-класс объекта. `def self.x` живёт там же.

## Фраза для собеса

«`include` добавляет методы экземплярам после класса, `prepend` — перед (для обёрток через super), `extend` — самому объекту; `ancestors` показывает порядок».
"""),

"01-ruby-yazyk/16-self-singleton-metody-class-self.md": ([
  ("Ruby docs — Singleton class (Object#singleton_class)", R + "Object.html#method-i-singleton_class"),
], """
`self` — текущий объект. Меняется в зависимости от места:

```ruby
class Foo
  self            # Foo (класс)
  def bar; self; end     # экземпляр
  def self.baz; self; end   # Foo — singleton-метод класса
end
```

У **каждого объекта** есть скрытый singleton-класс, где живут методы только этого объекта. «Методы класса» — это singleton-методы объекта-класса.

```ruby
class Foo
  class << self        # открыть singleton-класс Foo
    def a; end         # == def self.a
    private            # работает для класс-методов (private def self.x — нет)
    def b; end
    attr_accessor :config   # класс-уровневый аксессор
  end
end

obj = "x"
def obj.shout = upcase + "!"   # singleton-метод одного объекта
obj.singleton_methods          # [:shout]
```

Когда `class << self`: несколько класс-методов подряд, нужен `private`/`attr_*` на уровне класса. Для 1–2 методов — `def self.x` читается лучше.

Неявный `self`: вызов `foo` без получателя = `self.foo` (ищет метод, потом локальную переменную — нет, наоборот: сначала локальную переменную). `self.name = x` — обязательно с `self`, иначе создастся локальная переменная.

## Фраза для собеса

«Класс-методы — это singleton-методы объекта-класса; `class << self` открывает его singleton-класс, где работают `private` и `attr_accessor`».
"""),

"01-ruby-yazyk/17-method-missing-respond-to-missing-define-method-.md": ([
  ("Ruby docs — BasicObject#method_missing", R + "BasicObject.html#method-i-method_missing"),
  ("Ruby docs — Module#define_method", R + "Module.html#method-i-define_method"),
], """
```ruby
class Proxy
  def method_missing(name, *args, &blk)
    return super unless name.to_s.start_with?("find_by_")
    find(name.to_s.delete_prefix("find_by_"), *args)
  end

  def respond_to_missing?(name, include_private = false)
    name.to_s.start_with?("find_by_") || super
  end
end
```

- `method_missing` вызывается, когда метод не найден во всей цепочке. **Всегда** вызывать `super` для чужих имён — иначе проглотишь опечатки и получишь nil вместо `NoMethodError`.
- `respond_to_missing?` — пара к нему, иначе `respond_to?` и `method(:x)` врут.
- Медленно: промах по всей цепочке + разбор имени на каждый вызов. Часто комбинируют: первый раз через `method_missing`, и тут же `define_method`, чтобы дальше было быстро (так делал старый ActiveRecord).

```ruby
%w[sent failed].each do |st|
  define_method("#{st}?") { status == st }    # метод с замыканием; быстрее method_missing
end
```

`send`/`public_send`: вызов по имени. `public_send` уважает private — предпочтительнее с внешними данными. `send` ломает инкапсуляцию, допустимо в тестах и внутри класса.

## Фраза для собеса

«`method_missing` всегда в паре с `respond_to_missing?` и `super`; где можно — лучше `define_method`, он быстрее и виден интроспекции».
"""),

"01-ruby-yazyk/18-isklyucheniya-standarderror-vs-exception-retry-e.md": ([
  ("Ruby docs — Exception (иерархия)", R + "Exception.html"),
  ("Ruby docs — exceptions syntax", R + "syntax/exceptions_rdoc.html"),
], """
```
Exception
├── NoMemoryError, SignalException (Interrupt), SystemExit, ScriptError (LoadError, SyntaxError)
└── StandardError          ← `rescue` без класса ловит ТОЛЬКО это
    ├── ArgumentError, TypeError, NameError → NoMethodError
    ├── RuntimeError (raise "str"), IOError, KeyError, ZeroDivisionError
    └── свои ошибки
```

`rescue Exception` ловит Ctrl-C, `exit`, нехватку памяти — процесс нельзя остановить. Почти всегда ошибка. `rescue => e` = `rescue StandardError => e`.

```ruby
class App::Error < StandardError; end          # базовый класс приложения
class InsufficientFunds < App::Error
  def initialize(need, have) = super("need #{need}, have #{have}")
end

attempts = 0
begin
  api.call
rescue Timeout::Error => e
  attempts += 1
  retry if attempts < 3            # повторить begin-блок
  raise                            # re-raise тот же объект с backtrace
ensure
  conn.close                       # всегда; не ставь здесь return — он подавит исключение
end
```

- `raise CustomError, "msg"` / `raise CustomError.new(...)`. `raise` без аргументов внутри rescue — повторно бросить текущее.
- `e.cause` — предыдущее исключение, если бросили новое внутри rescue.
- `rescue` в теле метода без `begin` — допустимо. `rescue ... else` — ветка, если исключения не было.
- Исключения — для исключительных ситуаций; для ожидаемых исходов (валидация) — Result/bool, не raise.

## Фраза для собеса

«Ловлю `StandardError` или конкретнее, свои ошибки наследую от него; `rescue Exception` — почти всегда баг; `retry` для повторов, `ensure` для освобождения ресурсов».
"""),

"01-ruby-yazyk/19-vs-eql-vs-equal-hash-dlya-klyuchej.md": ([
  ("Ruby docs — Object#== / eql? / equal?", R + "Object.html#method-i-eql-3F"),
], """
| Метод | Смысл | Кто переопределяет |
|---|---|---|
| `equal?` | тот же объект (identity) | никогда |
| `==` | равенство по значению | да, свои классы |
| `eql?` | строгое равенство без приведения типов; используется Hash | вместе с `hash` |
| `===` | «подходит под» — для `case/when` | Range, Regexp, Class, Proc |

```ruby
1 == 1.0     # true
1.eql? 1.0   # false  — поэтому h[1] и h[1.0] разные ключи
"a".equal?("a")  # false — два объекта
```

Свой класс как ключ хеша или в `Set`/`uniq` — нужны **оба**:

```ruby
class Money
  def ==(o) = o.is_a?(Money) && cents == o.cents && currency == o.currency
  alias eql? ==
  def hash = [cents, currency].hash     # равные объекты → равный hash
end
```

Без `hash` два равных `Money` попадут в разные бакеты, и `uniq` их не схлопнет. `Struct`/`Data` делают это автоматически.

`===` в `case`: `when Integer` → `Integer === x` → `is_a?`; `when 1..5` → `include?`; `when /re/` → `match?`; `when ->(x) { x > 0 }` → `call`.

## Фраза для собеса

«`==` — значение, `equal?` — идентичность, `eql?`+`hash` — для ключей хеша; переопределяю `==`, алиасю `eql?` и считаю `hash` по тем же полям».
"""),

"01-ruby-yazyk/20-mutable-default-argument-shared-state-array-new-.md": ([
  ("Ruby docs — Array.new", R + "Array.html#method-c-new"),
], """
```ruby
Array.new(3, [])         # [[], [], []] — но это ОДИН и тот же массив трижды
grid = Array.new(3, []); grid[0] << 1
grid                     # [[1], [1], [1]]

Array.new(3) { [] }      # три разных — блок вызывается для каждого
Hash.new([])             # тот же эффект: общий дефолт для всех ключей
Hash.new { |h, k| h[k] = [] }
```

В отличие от Python, дефолтные аргументы метода в Ruby вычисляются **при каждом вызове**, так что `def f(a = [])` безопасен. Проблема именно в `Array.new(n, obj)` и `Hash.new(obj)`, где объект создаётся один раз.

Другие источники разделяемого состояния:
- константы-массивы/хеши без `freeze` — любой может `<<`;
- класс-переменные `@@x` — общие для всей иерархии наследников;
- строковые литералы без frozen_string_literal, которые кто-то мутирует;
- `dup` поверхностный: `h.dup[:list] << x` меняет оригинал. Глубокая копия — `Marshal.load(Marshal.dump(h))` или явно.

Многопоточность: любой общий мутабельный объект без `Mutex` — гонка (Sidekiq, Puma).

## Фраза для собеса

«`Array.new(3, [])` даёт один общий объект — нужен блок; константы замораживаю; `dup` поверхностный».
"""),

"01-ruby-yazyk/21-gvl-pochemu-threads-ne-parallelyat-cpu-no-parall.md": ([
  ("Ruby docs — Thread", R + "Thread.html"),
  ("Ruby docs — Ractor", R + "Ractor.html"),
], """
**GVL** (Global VM Lock, раньше GIL) — в MRI одновременно Ruby-код выполняет только один поток процесса.

- **CPU-bound** задачи (парсинг, вычисления): потоки не ускорят, время сложится. Нужны процессы (Puma workers, `fork`) или Ractor.
- **IO-bound** (HTTP, БД, файлы): во время ожидания IO поток **отпускает** GVL, другие работают. Поэтому Sidekiq с 10 потоками и Puma с 5 нормально параллелят запросы к БД.

```ruby
threads = urls.map { |u| Thread.new { fetch(u) } }
threads.each(&:value)        # IO параллелится, итого ≈ время самого долгого запроса
```

Что это значит на практике:
- Sidekiq concurrency — про IO; для тяжёлого CPU — меньше потоков, больше процессов.
- AR connection pool ≥ число потоков, иначе `ConnectionTimeoutError`.
- Потоки всё равно требуют thread-safety: GVL переключается между байткод-инструкциями, `@count += 1` не атомарен. Для общего состояния — `Mutex`, `Queue`, `Concurrent::*`.
- Переключение каждые ~100 мс (timeslice) или на блокирующем IO.

Ractor (3.0+) — изолированные акторы без общей памяти, настоящий параллелизм, но экосистема пока слабая. JRuby/TruffleRuby — без GVL.

## Фраза для собеса

«GVL пускает один поток на Ruby-код, но отпускается на IO — потому потоки годятся для сети и БД, а для CPU нужны процессы; и потоки всё равно требуют Mutex».
"""),

"01-ruby-yazyk/22-integer-proizvolnoj-dliny-bigdecimal-rational-po.md": ([
  ("Ruby docs — BigDecimal", "https://ruby.github.io/bigdecimal/"),
  ("Floating-point guide", "https://floating-point-gui.de/"),
], """
```ruby
0.1 + 0.2 == 0.3        # false  (0.30000000000000004)
2**100                  # 1267650600228229401496703205376 — Integer без переполнения
```

Float — двоичная дробь, десятичные 0.1 не представимы точно. Ошибки накапливаются: `100.times.sum { 0.1 }` ≠ 10.

Варианты для денег:
- **Integer в минимальных единицах** — сатоши, центы. Самый простой и быстрый, так устроен сам Bitcoin. Для твоего тестового — только так.
- **`BigDecimal("0.1")`** — десятичная арифметика произвольной точности. Создавать из **строки**, не из float (`BigDecimal(0.1)` уже содержит ошибку). В БД — `numeric`.
- **`Rational(1, 3)`** — точные дроби, редко.

```ruby
require "bigdecimal/util"
"19.99".to_d * 3        # 0.5997e2
btc = 150_000           # sat
btc.fdiv(100_000_000)   # только для отображения
format("%.8f", btc / 1e8)
```

Float допустим для статистики и отображения. Сравнение float — через `be_within` в тестах, через эпсилон в коде.

## Фраза для собеса

«Деньги — Integer в минимальных единицах или BigDecimal из строки; Float — только для отображения. Integer в Ruby не переполняется».
"""),

"01-ruby-yazyk/23-keyword-args-vs-options-hash-opts-forwarding.md": ([
  ("Ruby docs — Methods: Keyword Arguments", R + "syntax/methods_rdoc.html#label-Keyword+Arguments"),
  ("Ruby 3.0 — Separation of positional and keyword arguments", "https://www.ruby-lang.org/en/news/2019/12/12/separation-of-positional-and-keyword-arguments-in-ruby-3-0/"),
], """
```ruby
# старый стиль
def send(to, opts = {}); fee = opts[:fee] || 1000; end     # опечатка в ключе — тишина

# keyword args
def send(to, amount:, fee: 1000, **rest)   # amount обязателен; fee с дефолтом; rest — остальное
send("tb1q...", amount: 5_000)
send("tb1q...", amout: 5_000)              # ArgumentError: unknown keyword — ловится сразу
```

Плюсы kwargs: самодокументируемые вызовы, проверка имён, порядок не важен, дефолты видны в сигнатуре.

Ruby 3: позиционные и keyword разделены. `h = {a: 1}; m(h)` — это позиционный хеш, не kwargs; нужно `m(**h)`. Это сломало много гемов при переходе с 2.7.

Делегирование:
```ruby
def wrapper(*args, **kwargs, &blk) = target(*args, **kwargs, &blk)
def wrapper(...) = target(...)       # 2.7+: всё как есть
def wrapper(*, **, &) = target(*, **, &)   # 3.2: анонимные
```

Shorthand (3.1): `Point.new(x:, y:)` = `Point.new(x: x, y: y)`.

## Фраза для собеса

«Keyword-аргументы вместо options hash: явные, с проверкой имён и дефолтами; для делегирования — `...`».
"""),

"01-ruby-yazyk/24-refinements-znat-chto-est.md": ([
  ("Ruby docs — Refinements", R + "syntax/refinements_rdoc.html"),
], """
Monkey-patching (`class String; def shout; end; end`) меняет класс **глобально** — для всех гемов и всего процесса. Refinements — то же, но с ограниченной областью видимости.

```ruby
module Shout
  refine String do
    def shout = upcase + "!"
  end
end

using Shout          # действует до конца файла/класса, где написано
"hi".shout           # "HI!"
```

В другом файле без `using` — `NoMethodError`. Не влияет на `send`, `respond_to?`, `method_missing` (не видят refinements).

На практике используются редко: ActiveSupport патчит ядро напрямую (`5.minutes`), а в своём коде обычно проще написать хелпер или сервис, чем расширять `String`. Знать, что есть, и объяснить, почему это безопаснее monkey-patch — достаточно.

## Фраза для собеса

«Refinements — monkey-patch с лексической областью через `using`; на практике редкость, обычно лучше сервис или модуль».
"""),

"01-ruby-yazyk/25-garbage-collector-object-allocation-na-urovne-od.md": ([
  ("Ruby docs — GC", R + "GC.html"),
  ("Ruby docs — ObjectSpace", R + "ObjectSpace.html"),
], """
MRI: mark & sweep, **поколенческий** (2.1+) и **инкрементальный** (2.2+). Молодые объекты проверяются часто (minor GC), пережившие несколько циклов — редко (major GC). Компактификация (`GC.compact`, 2.7+) борется с фрагментацией.

Что это значит для кода:
- Каждая строка, массив, хеш, блок-как-Proc — аллокация. Меньше мусора в горячих циклах → реже GC → быстрее. Отсюда `frozen_string_literal`, `<<` вместо `+`, `each` вместо `map` когда результат не нужен, `yield` вместо `&block`.
- Память процесса **не возвращается** ОС после GC — она остаётся в куче Ruby. Поэтому долгоживущие воркеры «пухнут»: `MALLOC_ARENA_MAX=2`, jemalloc, перезапуск по памяти (`sidekiq-worker-killer`, Puma worker killer).
- Утечка в Ruby — обычно не GC, а живая ссылка: растущий глобальный хеш, кэш без лимита, подписки.

Посмотреть:
```ruby
GC.stat[:total_allocated_objects]
GC.count
ObjectSpace.count_objects
# gem memory_profiler, derailed_benchmarks
```

## Фраза для собеса

«Поколенческий mark & sweep; пишу код с меньшим числом аллокаций в горячих местах, а раздувание воркеров лечу лимитом памяти и jemalloc».
"""),
}
