---
title: "Суммы в integer сатоши"
hot: true
links:
  - { t: "Bitcoin Wiki — Satoshi (unit)", u: "https://en.bitcoin.it/wiki/Satoshi_(unit)" }
---
1 BTC = 100 000 000 сатоши. Сеть, API и библиотеки работают в **сатоши целым числом**. Float — только на границе с человеком.

```ruby
SAT_PER_BTC = 100_000_000

def to_sat(btc_str)  = (BigDecimal(btc_str) * SAT_PER_BTC).to_i     # ввод пользователя: строка → BigDecimal → Integer
def to_btc(sat)      = format("%.8f", Rational(sat, SAT_PER_BTC))    # вывод

to_sat("0.00001")    # 1000 — комиссия из задания
to_sat("0.1")        # 10_000_000
(0.1 * 1e8).to_i     # 10000000 — повезло; (0.29 * 1e8).to_i → 28999999 — нет
```

- Парсить ввод через `BigDecimal(str)` или `Rational`, никогда `Float(str) * 1e8`.
- Внутри — `Integer`: UTXO `value`, `amount`, `fee`, `change`. Проверки `inputs >= amount + fee` целые.
- Mempool API отдаёт `value` в сатоши; `bitcoinrb` `Bitcoin::TxOut.new(value: sat)` — тоже.
- Второе задание: курс USDT/BTC — `BigDecimal`, результат умножения → `.floor` до сатоши в пользу обменника; комиссия 3% — `(amount * 3 / 100)` на BigDecimal, округление явное.
- В Postgres — `bigint`. В JSON — число (сатоши) или строка BTC, не float.
- Тест: `expect(to_sat("0.29")).to eq(29_000_000)` — ловит float-баг.

## Фраза для собеса

«Все суммы — Integer в сатоши; ввод парсю через BigDecimal, Float нигде, кроме форматирования вывода».
