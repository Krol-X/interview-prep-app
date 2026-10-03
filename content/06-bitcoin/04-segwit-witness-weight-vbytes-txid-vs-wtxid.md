---
title: "SegWit: witness, weight/vbytes, txid vs wtxid"
hot: true
links:
  - { t: "BIP141 — Segregated Witness", u: "https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki" }
  - { t: "learnmeabitcoin — SegWit / weight", u: "https://learnmeabitcoin.com/technical/transaction/size/" }
---
SegWit (2017, soft fork) **вынес данные подписи** из тела транзакции в отдельную структуру — witness.

Что это дало:
1. **Transaction malleability исправлена.** Раньше подпись входила в txid; её можно было слегка изменить (DER-кодирование), не ломая валидность, — txid менялся, и цепочки неподтверждённых транзакций (Lightning) ломались. Теперь:
   - `txid` = hash(транзакция **без** witness) — стабилен;
   - `wtxid` = hash(с witness) — используется в блоке для коммитмента witness-данных.
2. **Больше места в блоке через «вес»**: лимит не 1 МБ размера, а **4 000 000 weight units**.
   ```
   weight = 4 × (байты без witness) + 1 × (байты witness)
   vbytes = weight / 4
   ```
   Witness-байты в 4 раза дешевле → SegWit-транзакции платят меньше при той же логике (P2WPKH вход ~68 vB против ~148 у P2PKH). Эффективный размер блока — до ~4 МБ, типично ~1.5–2.
3. Версионирование witness-программ — путь к Taproot (v1) без нового форка формата.

Для тебя: комиссия считается в **sat/vB**; размер транзакции — `tx.vsize`; адреса `tb1q` — SegWit v0; старые узлы видят SegWit-выходы как «anyone can spend», но не майнят невалидные — поэтому это soft fork.

## Фраза для собеса

«SegWit перенёс подписи в witness: txid перестал зависеть от подписи, witness-байты весят ¼, отсюда vbytes и дешевле комиссии».
