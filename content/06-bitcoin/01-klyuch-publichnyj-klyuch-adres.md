---
title: "Ключ → публичный ключ → адрес"
hot: true
links:
  - { t: "Mastering Bitcoin, гл. 4 — Keys and Addresses", u: "https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch04_keys.adoc" }
  - { t: "learnmeabitcoin — Private key / Public key / Address", u: "https://learnmeabitcoin.com/technical/keys/" }
  - { t: "bitcoinrb — README", u: "https://github.com/chaintope/bitcoinrb" }
---
```
приватный ключ  ──(умножение на кривой secp256k1)──▶  публичный ключ  ──(hash160 / bech32)──▶  адрес
   256 бит случайности          односторонне            33 байта (сжатый)                      tb1q...
```

- **Приватный ключ** — случайное число 1..n (~2²⁵⁶). Никуда не отправляется. Форматы: hex, **WIF** (base58 с префиксом сети и checksum — так его хранят кошельки и так сохранишь ты).
- **Публичный ключ** — точка на кривой `priv × G`. Обратно не вычислить (ECDLP). Из него проверяют подписи.
- **Адрес** — не ключ, а **инструкция получателю, какое условие траты записать в выход**. P2WPKH: `bech32(hrp, 0, hash160(pubkey))`. Префикс `tb1q` — Signet/testnet, `bc1q` — mainnet. Checksum внутри ловит опечатки.
- Один приватный ключ → разные адреса в разных сетях (hrp/префикс другой) и разные типы (P2PKH `m...`, P2WPKH `tb1q...`, P2TR `tb1p...`).
- HD-кошельки (BIP32/39/44): seed-фраза 12 слов → мастер-ключ → дерево ключей по пути `m/84'/1'/0'/0/0`. Для тестового один ключ достаточно.

```ruby
Bitcoin.chain_params = :signet
key = Bitcoin::Key.generate            # SecureRandom внутри
key.to_wif                             # сохранить в файл
key.to_p2wpkh                          # tb1q...
Bitcoin::Key.from_wif(File.read(path)) # восстановить
```

Генерировать **только** CSPRNG (`SecureRandom`): все реальные взломы — слабая энтропия, не перебор 2²⁵⁶.

## Фраза для собеса

«Приватный — случайное число, публичный — точка на кривой, адрес — хеш публичного ключа в bech32 с префиксом сети; из адреса сеть понимает условие траты».
