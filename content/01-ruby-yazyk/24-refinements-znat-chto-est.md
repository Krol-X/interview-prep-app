---
title: "Refinements — знать, что есть"
hot: false
links:
  - { t: "Ruby docs — Refinements", u: "https://docs.ruby-lang.org/en/master/syntax/refinements_rdoc.html" }
---
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
