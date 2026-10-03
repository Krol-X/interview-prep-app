---
title: "Бонус: динамическая комиссия через `fees/recommended` × vbytes"
hot: false
links:
  - { t: "mempool.space — GET /v1/fees/recommended", u: "https://mempool.space/signet/docs/api/rest#get-recommended-fees" }
  - { t: "Bitcoin Optech — Transaction size calculator", u: "https://bitcoinops.org/en/tools/calc-size/" }
---
`fee = vsize × rate`. Две части: узнать rate и узнать vsize **до** того, как транзакция подписана (размер зависит от подписей).

```ruby
rate = client.recommended_fees.fetch("fastestFee")   # sat/vB; Signet → 1

# Способ 1: оценка по формуле (P2WPKH)
def estimate_vsize(n_in, n_out) = 10.5 + n_in * 68 + n_out * 31     # overhead + входы + выходы
# Способ 2: собрать с фиктивными подписями (72-байтовые нули) и спросить tx.vsize
# Способ 3: подписать, измерить, пересобрать с точной комиссией (ещё одна подпись — дёшево)

fee = [(vsize * rate).ceil, vsize * 1].max            # не ниже minrelay 1 sat/vB
```

Курица и яйцо со сдачей: наличие change-выхода меняет размер. Алгоритм:
1. Выбрать входы.
2. Посчитать vsize **с** выходом сдачи, fee.
3. `change = inputs − amount − fee`.
4. `change < dust` → убрать выход сдачи, пересчитать vsize/fee (стало меньше), остаток в комиссию.
5. `change < 0` → добавить вход, повторить.

Разумные границы: `rate` clamp между 1 и, скажем, 200 sat/vB — защита от сломанного API. Флаг `--fee-rate N` для ручного override. В выводе показать: `fee: 141 sat (141 vB × 1 sat/vB)`.

Для второго задания комиссия фиксирована 0.000006 — но вынести в конфиг, не в константу.

## Фраза для собеса

«Беру рекомендованную ставку, оцениваю vsize по числу входов/выходов, умножаю, не опускаюсь ниже 1 sat/vB и пересчитываю, если сдача ушла в пыль».
