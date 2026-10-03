---
title: "`dry-validation`: `Contract`, `params do ... end`, `rule(:x)`, `result.errors.to_h`"
hot: true
links:
  - { t: "dry-validation — Contracts", u: "https://dry-rb.org/gems/dry-validation/1.10/" }
  - { t: "dry-validation — Rules", u: "https://dry-rb.org/gems/dry-validation/1.10/rules/" }
---
```ruby
class WithdrawalContract < Dry::Validation::Contract
  params do                                      # схема: типы, приведение, обязательность
    required(:to_address).filled(:string)
    required(:amount_sat).filled(:integer, gt?: 0)
    optional(:email).maybe(:string, format?: /@/)
    required(:kyc).filled(:bool, eql?: true)
  end

  rule(:to_address) do                           # правила: бизнес-логика, кросс-полевые проверки
    key.failure("invalid signet address") unless Bitcoin.valid_address?(value)
  end

  rule(:amount_sat, :to_address) do
    key(:amount_sat).failure("exceeds limit") if values[:amount_sat] > MAX && values[:to_address].start_with?("tb1p")
  end
end

result = WithdrawalContract.new.call(params.to_unsafe_h)
result.success?         # true/false
result.to_h             # приведённые значения ("5" → 5)
result.errors.to_h      # { to_address: ["invalid signet address"] }
result.to_monad         # Success(values) / Failure(result) — для Do-notation
```

- `params` — для строк из HTTP (приводит типы); `json` — для JSON (строже); `schema` — без приведения.
- `rule` выполняется только если схема для этих ключей прошла — не надо проверять на nil.
- Зависимости в контракт: `option :repo` (dry-initializer внутри) — для проверок через БД.
- Сообщения — в YAML с i18n, или строкой на месте.
- Отличие от AR-валидаций: контракт не привязан к модели, проверяет **вход** (форма/API), а не состояние записи; один вход — один контракт.

## Фраза для собеса

«`params do` описывает форму и типы входа, `rule` — бизнес-правила; результат даёт приведённые значения и ошибки по ключам и конвертируется в Result».
