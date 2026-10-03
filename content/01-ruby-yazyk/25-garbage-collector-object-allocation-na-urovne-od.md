---
title: "Garbage collector, object allocation — на уровне одной фразы"
hot: false
links:
  - { t: "Ruby docs — GC", u: "https://docs.ruby-lang.org/en/master/GC.html" }
  - { t: "Ruby docs — ObjectSpace", u: "https://docs.ruby-lang.org/en/master/ObjectSpace.html" }
---
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
