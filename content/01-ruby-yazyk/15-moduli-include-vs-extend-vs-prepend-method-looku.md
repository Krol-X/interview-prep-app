---
title: "Модули: `include` vs `extend` vs `prepend`, method lookup (ancestors)"
hot: true
links:
  - { t: "Ruby docs — Module#prepend", u: "https://docs.ruby-lang.org/en/master/Module.html#method-i-prepend" }
  - { t: "Ruby docs — Module#ancestors", u: "https://docs.ruby-lang.org/en/master/Module.html#method-i-ancestors" }
---
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
