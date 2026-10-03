---
title: "UTXO; вход = txid + vout; сдача; fee = inputs − outputs"
hot: true
links:
  - { t: "Mastering Bitcoin, гл. 6 — Transactions (бесплатно на GitHub)", u: "https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch06_transactions.adoc" }
  - { t: "learnmeabitcoin — UTXO", u: "https://learnmeabitcoin.com/technical/transaction/utxo/" }
  - { t: "mempool.space Signet API — address/:addr/utxo", u: "https://mempool.space/signet/docs/api/rest#get-address-utxo" }
---
В биткоине нет балансов. Есть журнал транзакций; каждая **уничтожает** старые выходы (входы) и **создаёт** новые (выходы).

**UTXO** — unspent transaction output: выход, который ещё не использован как вход. Баланс адреса = сумма его UTXO.

## Транзакция на пальцах

```
Входы:   txid A, vout 0   70 000 sat
         txid B, vout 1   50 000 sat
                         ───────
                         120 000
Выходы:  получателю       90 000
         сдача себе       29 000
                         ───────
                         119 000
Комиссия = 120 000 − 119 000 = 1 000 sat   (нигде не записана, остаток)
```

- Вход ссылается на **конкретный выход** прошлой транзакции: `txid` + `vout` (индекс), не на адрес.
- UTXO тратится **целиком**. Хочешь меньше — явно создай выход со сдачей себе. Забыл — остаток уйдёт майнеру.
- Комиссия — не поле, а арифметическая разница.

## Для тестового

```
GET /api/address/{addr}/utxo
[{ "txid": "...", "vout": 0, "value": 100000, "status": { "confirmed": true } }]
```

Суммы в **сатоши, integer**. Не Float. Сдача меньше «пыли» (~546 sat P2PKH / ~294 sat P2WPKH) — не создавай выход, оставь майнеру.

## Аналогия для веба

Event sourcing: блокчейн — лог событий, набор UTXO — вычисленное текущее состояние.

## Фраза для собеса

«Кошелёк не тратит с адреса — он тратит конкретные UTXO, подписывая каждый вход, и обязан явно вернуть себе сдачу».
