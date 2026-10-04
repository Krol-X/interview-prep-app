---
title: "Задание: валидация формы и `Do`-нотация в сервисе"
hot: false
sub: "практика · 20–40 мин"
---
1. `dry-schema`/`dry-validation` контракт `ExchangeContract`: `amount` (Decimal, 0 < x ≤ 30), `address` (строка, кастомное правило `signet_address?` для префиксов `m/n/2/tb1q`), `email`, `kyc` (должен быть `true`). Ошибки — с ключами полей, пригодными для вывода под инпутами.
2. Сервис `CreateExchange` на `dry-monads` с `Do`-нотацией: валидация → расчёт суммы (`Success`/`Failure(:rate_unavailable)`) → сохранение → постановка задачи. Любой `Failure` прерывает цепочку, тип ошибки сохраняется.
3. `dry-struct` для результата расчёта: `amount_usdt`, `fee_usdt`, `amount_sat`, `rate`; типы строгие (`Types::Strict::Integer` для сатоши).
4. Вызывающий код использует `case result in Success(…) / Failure[:validation, errors] / Failure(:rate_unavailable)` — все ветки обработаны.
5. Спеки на контракт (5 невалидных случаев) и на сервис (успех + каждый из `Failure`).

Критерий: ни одного `raise` для бизнес-ошибок, ни одного `if result.success?` — только pattern matching.
