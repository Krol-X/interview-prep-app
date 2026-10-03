---
title: "P2PKH / P2SH / P2WPKH / P2WSH / P2TR — одной фразой каждый + префиксы mainnet/signet"
hot: true
links:
  - { t: "learnmeabitcoin — Script / locking scripts", u: "https://learnmeabitcoin.com/technical/script/" }
  - { t: "Mastering Bitcoin, гл. 7 — Authorization and Authentication", u: "https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch07_authorization-authentication.adoc" }
---
Каждый выход = сумма + **условие траты** (locking script). Типы — это шаблоны условия.

| Тип | Условие | Mainnet | Signet | С какого года |
|---|---|---|---|---|
| **P2PKH** | покажи pubkey с таким hash160 + ECDSA-подпись | `1...` | `m.../n...` | 2009 |
| **P2SH** | покажи скрипт с таким hash160 и данные, на которых он даст true | `3...` | `2...` | 2012 (BIP16) |
| **P2WPKH** | то же, что P2PKH, но данные в witness | `bc1q...` (42 симв.) | `tb1q...` | 2017 (BIP141) |
| **P2WSH** | то же, что P2SH, но в witness; hash sha256 | `bc1q...` (62 симв.) | `tb1q...` | 2017 |
| **P2TR** | Schnorr-подпись ключом (key path) или скрипт из дерева (script path) | `bc1p...` | `tb1p...` | 2021 (BIP341) |
| P2SH-P2WPKH | SegWit, завёрнутый в P2SH для совместимости | `3...` | `2...` | переходный |

- Тип входа (что тратишь) и тип выхода (куда шлёшь) независимы: тратишь свой P2WPKH, платишь на P2TR — нормально.
- Подписываешь по правилам **тратимого** UTXO; создаёшь выход по правилам **адреса получателя** — библиотека сделает по префиксу.
- Размер и комиссия: P2PKH вход ~148 vB, P2WPKH ~68, P2TR ~58.
- В тестовом задании 2 валидировать «P2PKH, P2SH, P2WPKH» для signet: префиксы `m/n`, `2`, `tb1q`. `tb1p` — решить явно.

## Фраза для собеса

«PKH — ключ, SH — скрипт, W — то же в witness, TR — Taproot с ключом или деревом скриптов; префикс адреса говорит, какой шаблон условия записать в выход».
