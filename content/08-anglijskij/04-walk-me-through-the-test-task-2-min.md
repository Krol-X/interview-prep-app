---
title: "Walk me through the test task — 2 мин"
hot: true
links:
  - { t: "Bitcoin Optech — Glossary (термины на английском)", u: "https://bitcoinops.org/en/topics/" }
---
Отвечать как **поток данных**, не как список файлов. Рисовать в воздухе: ключ → адрес → UTXO → транзакция → сеть.

> It's a command-line Signet wallet in Ruby with three commands: address, balance, and send.
>
> On first run it generates a private key with SecureRandom, stores it as WIF in a data directory with 600 permissions, and never overwrites it. From the key I derive a native SegWit address — P2WPKH, `tb1q`.
>
> Balance is the sum of unspent outputs for that address. I fetch them from the mempool.space Signet API — each UTXO is a txid, an output index, and a value in satoshis. All amounts in the app are integers; floats only appear when formatting output.
>
> For send, I take the UTXOs as inputs, create one output to the recipient and a change output back to my address — unless the change would be dust, in which case it goes to the fee. The fee is inputs minus outputs: fixed at a thousand satoshis, or optionally vsize times the recommended rate. Before building anything I check that the inputs cover amount plus fee and give a precise error if not.
>
> Each input is signed separately with the SegWit sighash — which commits to the input amount — and the witness is the signature plus the public key. Then I broadcast the hex to the API and print the txid. There's a confirmed example in the README.
>
> I kept it simple on purpose: one key, no HD wallet, no coin selection, public API instead of my own node. Tests cover the builder logic — change, dust, insufficient funds — with HTTP mocked.

≈220 слов, 2 минуты. Дальше ждут вопросов — см. «Своё тестовое: объяснить каждый шаг».

Слова, которые должны звучать естественно: *unspent output, derive, sign, broadcast, change, dust, fee rate, confirmation, witness*.
