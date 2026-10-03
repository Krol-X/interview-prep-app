---
title: "Happy path: ключ → баланс → отправка в Signet"
hot: true
links:
  - { t: "mempool.space Signet API", u: "https://mempool.space/signet/docs/api/rest" }
  - { t: "Signet faucet", u: "https://signetfaucet.com/" }
  - { t: "Electrum (запуск с --signet)", u: "https://electrum.org/#download" }
---
Сначала — сквозной сценарий без украшений. Всё остальное после.

```
$ ruby wallet.rb address        # генерирует ключ при первом запуске, печатает tb1q...
$ # → signetfaucet.com, вставить адрес, подождать блок (~10 мин)
$ ruby wallet.rb balance        # 10000 sat (0.0001 sBTC)
$ ruby wallet.rb send tb1q<electrum> 4000
  txid: 3f1a...                  # → mempool.space/signet/tx/3f1a...
```

Минимальный скелет:
```
wallet.rb            # CLI: разбор команд
lib/wallet/key_store.rb      # load_or_generate(path) → Bitcoin::Key
lib/wallet/mempool_client.rb # utxos(addr), broadcast(hex), fees — Net::HTTP или Faraday
lib/wallet/tx_builder.rb     # build(utxos, to:, amount:, fee:, change:) → Bitcoin::Tx (подписанный)
lib/wallet/cli.rb
```

Порядок работы: 1) ключ + адрес → faucet; 2) `utxos` → баланс; 3) `tx_builder` с одним UTXO на хардкоде → подпись → `broadcast`; 4) только теперь — валидации, ошибки, тесты, Docker, динамическая комиссия.

Проверка подписи до отправки: `tx.to_hex` → вставить в decoder (blockcypher / `bitcoin-cli decoderawtransaction`) — видно входы/выходы; если `POST /tx` вернул `non-mandatory-script-verify-flag` — подпись/sighash неверны; `bad-txns-in-belowout` — выходы больше входов; `min relay fee not met` — комиссия < 1 sat/vB.

Ссылку на успешный txid — в README.
