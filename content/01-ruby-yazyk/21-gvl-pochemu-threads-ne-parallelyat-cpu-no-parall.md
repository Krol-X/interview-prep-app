---
title: "GVL: почему threads не параллелят CPU, но параллелят IO; `Mutex`"
hot: true
links:
  - { t: "Ruby docs — Thread", u: "https://docs.ruby-lang.org/en/master/Thread.html" }
  - { t: "Ruby docs — Ractor", u: "https://docs.ruby-lang.org/en/master/Ractor.html" }
---
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
