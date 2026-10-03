---
title: "`Symbol#to_proc` (`&:name`), numbered params `_1`, `it` (3.4)"
hot: true
links:
  - { t: "Ruby docs — Symbol#to_proc", u: "https://docs.ruby-lang.org/en/master/Symbol.html#method-i-to_proc" }
  - { t: "Ruby 3.4 release notes — `it`", u: "https://www.ruby-lang.org/en/news/2024/12/25/ruby-3-4-0-released/" }
---
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
