---
title: "Задание: `Enumerable` + `Comparable` на своём классе"
hot: false
sub: "практика · 20–40 мин"
---
Написать класс `Ledger` — журнал записей `{date:, amount:, memo:}`:

1. `Ledger` включает `Enumerable`; реализован только `each`.
2. Запись — `Struct` или `Data` с `Comparable` по `amount`.
3. Метод `balance_by(:month)` возвращает хеш `{"2026-03" => сумма}` одной цепочкой Enumerable без промежуточных переменных.
4. Метод `each` без блока возвращает `Enumerator`; `ledger.lazy.select { … }.first(3)` работает на бесконечном источнике.
5. `ledger.frozen? == true` после `#freeze`, попытка добавить запись падает с `FrozenError`.
6. Рефайнмент `refine String` с методом `to_money` (строка `"1 234,50"` → `Integer` копеек), подключён только внутри `Ledger`.

Критерий: `ruby ledger.rb` печатает баланс по месяцам, `ruby -w` без предупреждений, нет ни одного `each` с ручным накоплением в массив.
