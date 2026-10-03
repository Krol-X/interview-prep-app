---
title: "mainnet / testnet / signet / regtest"
hot: false
links:
  - { t: "BIP325 — Signet", u: "https://github.com/bitcoin/bips/blob/master/bip-0325.mediawiki" }
  - { t: "Bitcoin Core — Signet docs", u: "https://en.bitcoin.it/wiki/Signet" }
  - { t: "mempool.space Signet", u: "https://mempool.space/signet" }
---
Один код Bitcoin Core, четыре сети — **отдельные блокчейны** с разным genesis, magic bytes, портами и префиксами адресов. Монеты не пересекаются физически: транзакция signet в mainnet невалидна по формату.

| Сеть | Для чего | Как получить монеты | Особенности |
|---|---|---|---|
| **mainnet** | настоящие деньги | купить/намайнить | `bc1…`, `1…`, `3…`; порт 8333 |
| **testnet3/4** | публичный полигон | faucet, майнинг (легко) | `tb1…`, `m/n…`, `2…`; сброс сложности, если блок не найден 20 мин; хаос от мощных майнеров; testnet3 перезапущен как testnet4 в 2024 |
| **signet** | публичный полигон, твоё тестовое | только faucet | блок валиден, если **подписан** ключом оператора (BIP325) → нет гонки майнеров, ровно 10 мин, нет спама; те же префиксы, что testnet; кастомные signet'ы для экспериментов |
| **regtest** | локальная песочница | `generatetoaddress 101 <addr>` | блоки по команде, мгновенно; `bcrt1…`; для юнит- и интеграционных тестов |

Для разработки: логика → regtest (быстро, детерминированно), интеграция → signet (похоже на прод, стабильно), демо → signet.

```ruby
Bitcoin.chain_params = :signet      # bitcoinrb; :mainnet / :testnet / :regtest
```
Mempool API: `mempool.space/signet/api/...`, faucet: `signetfaucet.com`, кошелёк: `electrum --signet`.

## Фраза для собеса

«Signet — тестовая сеть, где блоки подписывает оператор: предсказуемая и без спама, в отличие от testnet; regtest — локальная, блоки по команде».
