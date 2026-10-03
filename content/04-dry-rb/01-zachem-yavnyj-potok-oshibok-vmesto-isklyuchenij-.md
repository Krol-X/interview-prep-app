---
title: "Зачем: явный поток ошибок вместо исключений, композиция"
hot: true
links:
  - { t: "dry-rb — dry-monads (Introduction)", u: "https://dry-rb.org/gems/dry-monads/" }
  - { t: "Railway Oriented Programming (Scott Wlaschin)", u: "https://fsharpforfunandprofit.com/rop/" }
---
Проблема исключений для бизнес-ошибок: невидимы в сигнатуре (`create_withdrawal` может бросить что угодно), ломают поток управления, дороги, провоцируют `rescue => e` «на всякий случай».

Явный результат — функция **всегда возвращает** объект, который либо `Success(value)`, либо `Failure(error)`:

```ruby
def call(params)
  Success(params)
    .bind { validate(_1) }      # Success → идём дальше; Failure → проскакиваем до конца
    .bind { debit(_1) }
    .bind { enqueue(_1) }
end

case CreateWithdrawal.new.call(params)
in Success(withdrawal) then render json: withdrawal
in Failure[:insufficient_funds, msg] then render json: { error: msg }, status: 422
in Failure[:invalid, errors] then render json: errors, status: 400
end
```

Плюсы: ошибки — часть контракта и видны в коде; все ветки обрабатываются (pattern matching без `else` упадёт на новом коде ошибки); композиция шагов — «рельсы» (Railway): успех едет по одной, ошибка переводится на другую и доезжает до конца без `if`.

Исключения остаются для **неожиданного** (сеть упала, баг) — их не превращают в Failure повсеместно.

Когда не надо: CRUD без ветвлений, маленький скрипт — `Result` будет церемонией.

## Фраза для собеса

«Бизнес-ошибки — это ожидаемые исходы, им место в возвращаемом значении, а не в исключениях; Result делает их явными и композируемыми».
