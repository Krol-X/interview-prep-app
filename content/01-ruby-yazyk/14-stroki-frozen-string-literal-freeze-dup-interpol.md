---
title: "Строки: frozen string literal, `freeze`, `dup`, интерполяция vs `+`"
hot: true
links:
  - { t: "Ruby docs — String", u: "https://docs.ruby-lang.org/en/master/String.html" }
  - { t: "Ruby 3.4 — chilled strings (release notes)", u: "https://www.ruby-lang.org/en/news/2024/12/25/ruby-3-4-0-released/" }
---
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
