---
title: "Комиссии: sat/vB, mempool, RBF, CPFP, пыль, minrelayfee"
hot: true
links:
  - { t: "mempool.space Signet — fees/recommended", u: "https://mempool.space/signet/docs/api/rest#get-recommended-fees" }
  - { t: "BIP125 — Replace-by-Fee", u: "https://github.com/bitcoin/bips/blob/master/bip-0125.mediawiki" }
  - { t: "Bitcoin Optech — Fee bumping (RBF/CPFP)", u: "https://bitcoinops.org/en/topics/fee-bumping/" }
---
- **Комиссия = Σвходов − Σвыходов.** Не поле, а остаток; забыл сдачу — всё майнеру.
- Платишь за **место в блоке**, не за сумму: `fee = vbytes × rate`, единица — **sat/vB**. Блок ограничен 4M weight units.
- **Mempool** — очередь неподтверждённых; майнер берёт сверху по sat/vB. Ставка — рыночная: пусто → 1 sat/vB, пик → сотни.
- **minrelayfee** 1 sat/vB — узлы не ретранслируют дешевле (это *policy*, не консенсус — 0-fee транзакция валидна, но не дойдёт до майнера).
- **Пыль (dust)** — выход, который дороже потратить, чем он стоит: ~546 sat P2PKH, ~294 sat P2WPKH. Такую сдачу не создавай — оставь в комиссии.
- **RBF** (BIP125) — заменить застрявшую транзакцию той же с большей комиссией (входы те же, fee выше хотя бы на minrelay × size). Нужен `sequence < 0xfffffffe`; с Core 28 full-RBF по умолчанию.
- **CPFP** — потратить выход застрявшей новой транзакцией с большой комиссией; майнер возьмёт обе как пакет. Работает, когда ты получатель.
- Застрявшая транзакция выбрасывается из mempool через ~2 недели (по умолчанию), UTXO снова свободны.

Размеры для оценки (1 вход, 2 выхода): P2WPKH ≈ **141 vB**, P2TR ≈ 111, P2PKH ≈ 226. Каждый доп. P2WPKH-вход +68, выход +31.

```
GET https://mempool.space/signet/api/v1/fees/recommended
{"fastestFee":1,"halfHourFee":1,"hourFee":1,"economyFee":1,"minimumFee":1}
```
Signet почти всегда 1 sat/vB. Бонус в тестовом: `fee = max(vsize × fastestFee, vsize × 1)`; размер — `tx.vsize` после сборки с фиктивной подписью или оценка по числу входов/выходов.

## Фраза для собеса

«Комиссия — остаток входов над выходами, рынок за vbytes; застряла — RBF или CPFP; сдачу меньше пыли не делаю».
