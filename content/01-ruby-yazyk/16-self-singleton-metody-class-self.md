---
title: "`self`, singleton-методы, `class << self`"
hot: false
links:
  - { t: "Ruby docs — Singleton class (Object#singleton_class)", u: "https://docs.ruby-lang.org/en/master/Object.html#method-i-singleton_class" }
---
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
