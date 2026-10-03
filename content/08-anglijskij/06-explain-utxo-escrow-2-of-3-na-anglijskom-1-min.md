---
title: "Explain UTXO / escrow 2-of-3 на английском — 1 мин"
hot: false
links:
  - { t: "learnmeabitcoin — UTXO", u: "https://learnmeabitcoin.com/technical/transaction/utxo/" }
---
Два мини-объяснения по 30–40 секунд. Простыми словами, как коллеге-вебщику.

**UTXO**
> Bitcoin doesn't have account balances. It has a log of transactions, and each transaction consumes some previous outputs and creates new ones. An output that hasn't been consumed yet is a UTXO — an unspent transaction output — basically a coin with a value and a spending condition attached. Your "balance" is just the sum of UTXOs your key can unlock. When you pay, you spend whole UTXOs as inputs, create an output to the recipient, and send the remainder back to yourself as change. Whatever you don't assign to an output becomes the miner's fee.

**2-of-3 escrow**
> On Hodl Hodl the seller doesn't send bitcoin to the platform. They lock it in a multisig output that requires two signatures out of three keys: the buyer's, the seller's, and the platform's. In a normal trade the buyer and seller sign together and the platform isn't involved. If there's a dispute, the platform signs with whichever side is right. But the platform alone has only one key, so it can never take the funds — it's an arbiter, not a custodian. Technically it's a P2SH output with a two-of-three CHECKMULTISIG script.

Отработать слова: *consume, unlock, remainder, lock funds, arbiter, custodian, dispute, output index*.

Если собеседник кивает — остановиться. Если спрашивает «and how does the script know?» — рассказать про redeem script и хеш.
