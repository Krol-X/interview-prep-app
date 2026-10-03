---
title: "block, miner, mempool, fee rate (sats per vbyte), to get stuck, to bump the fee (RBF)"
hot: false
sub: "5. Bitcoin (твоё тестовое + их продукт)"
links:
  - { t: "Bitcoin Optech — Fee bumping", u: "https://bitcoinops.org/en/topics/fee-bumping/" }
---
- **block** — *a block every ten minutes.* **block height**.
- **miner / to mine / mining** — *miners pick transactions by fee rate.*
- **mempool** — *the transaction sits in the mempool until it's mined.*
- **fee rate, sats per vbyte** («сатс пер ви-байт»): *one sat per vbyte on Signet.*
- **to get stuck** — застрять: *a low-fee transaction can get stuck.*
- **to bump the fee (RBF)** — *bump the fee with replace-by-fee.* **CPFP — child pays for parent**.
- **confirmation / to confirm**, **block subsidy**, **halving**, **hash rate**, **difficulty**.

> If a transaction gets stuck because the fee rate was too low, you can bump the fee with RBF or, if you're the receiver, use CPFP.
