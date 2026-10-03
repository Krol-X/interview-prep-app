---
title: "Taproot: Schnorr, key path / script path, MAST, control block"
hot: true
links:
  - { t: "BIP340 — Schnorr Signatures", u: "https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki" }
  - { t: "BIP341 — Taproot", u: "https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki" }
  - { t: "learnmeabitcoin — Taproot", u: "https://learnmeabitcoin.com/technical/upgrades/taproot/" }
---
Taproot (ноябрь 2021, soft fork) = SegWit v1 выход `bc1p…`/`tb1p…`. Три идеи:

**1. Schnorr вместо ECDSA** (BIP340). Подпись 64 байта, линейна: ключи и подписи можно **складывать**. N участников → один агрегированный ключ и одна подпись (MuSig2). Снаружи multisig неотличим от обычного платежа.

**2. Один ключ снаружи, дерево скриптов внутри** (BIP341):
```
output_key = internal_key + hash(internal_key ‖ merkle_root) · G
```
- **Key path**: подпись Schnorr от `output_key` — «счастливый» сценарий, все согласны. Дёшево (~58 vB вход), приватно.
- **Script path**: раскрыть один лист дерева + **control block** (internal key + merkle-путь из хешей соседних веток). Узел пересчитывает корень, проверяет tweak, исполняет скрипт.

**3. MAST** — дерево альтернативных условий; при трате раскрывается только использованная ветка, остальные остаются хешами навсегда.

Escrow Hodl Hodl на Taproot выглядел бы так: internal key = агрегат(покупатель+продавец) для нормальной сделки; ветки A (покупатель+платформа) и B (продавец+платформа) на спор. Блокчейн увидит escrow только при споре, и только одну ветку.

Для тестового: bitcoinrb умеет `to_p2tr`; отправить на `tb1p` — просто другой выход. Подписывать P2TR-вход — Schnorr (`sign_tx` с `sig_version: :taproot`), если решишь использовать.

## Фраза для собеса

«Taproot: Schnorr-подписи складываются, выход — один ключ с подмешанным корнем дерева скриптов; тратится либо ключом, либо раскрытием одной ветки».
