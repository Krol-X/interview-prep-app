---
title: "README на английском: как запустить, что реализовано, что упрощено, txid примера"
hot: false
links:
  - { t: "Make a README", u: "https://www.makeareadme.com/" }
---
README читают до кода. Структура на одну страницу, на английском:

```
# Signet wallet CLI

Minimal command-line Bitcoin Signet wallet in Ruby: generates a key, shows balance, sends sBTC.

## Quick start
    bundle install
    ruby wallet.rb address          # prints tb1q..., creates data/wallet.wif on first run
    ruby wallet.rb balance
    ruby wallet.rb send <address> <amount_btc>
  or with Docker: docker compose run wallet balance

## Example transaction
  https://mempool.space/signet/tx/<txid>   ← реальный, подтверждённый

## How it works
  key (WIF, data/) → address (P2WPKH) → UTXOs via mempool.space API →
  inputs: all UTXOs → outputs: recipient + change (if above dust) → sign (BIP143) → broadcast
  Fee: fixed 1000 sat (or `--dynamic` = vsize × recommended rate)
  All amounts are integer satoshis.

## Handled cases
  - insufficient funds (including fee), invalid/non-signet address, dust change, API errors (3 retries)
  - key is never overwritten / logged; file mode 600

## Simplifications & what I'd do next
  - single key, no HD wallet; public API instead of own node; spends all UTXOs (no coin selection);
    no RBF; unconfirmed change is spent (flag to disable)

## Tests
    bundle exec rspec      # builder logic + mocked HTTP, no network

## Decisions
  bitcoinrb over bitcoin-ruby: maintained, native signet params, SegWit/Taproot support
```

Что важно: команда запуска копипастом работает; ссылка на настоящий txid; честный список упрощений — это зрелость, а не слабость; обоснование выбора библиотеки одной строкой.
