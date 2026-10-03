---
title: "private key, public key, address, to derive, to generate, seed"
hot: false
sub: "5. Bitcoin (твоё тестовое + их продукт)"
links:
  - { t: "Bitcoin Optech — Glossary", u: "https://bitcoinops.org/en/topics/" }
---
- **private key** — *The private key never leaves the machine.* **public key** — *derived from the private key.*
- **address** — *a Signet address starting with tb1q.*
- **to derive** — вывести математически: *the address is derived from the public key hash.*
- **to generate** — *generate a key with a secure random source.*
- **seed / seed phrase / mnemonic** — *a 12-word seed phrase.* **HD wallet** (hierarchical deterministic), **derivation path**.
- **WIF** — Wallet Import Format. **keypair**.
- **to store / to back up / to encrypt the key**.

> On first run the CLI generates a private key, stores it as WIF, and derives a P2WPKH address from the public key.
