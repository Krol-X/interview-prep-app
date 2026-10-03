---
title: "script, spending condition, witness, SegWit, Taproot, soft fork"
hot: false
sub: "5. Bitcoin (твоё тестовое + их продукт)"
---
- **script / locking script / unlocking script** — *the output's locking script defines the spending condition.*
- **spending condition** — *a signature from this key, or two of three.*
- **witness** — данные подписи в SegWit: *the witness holds the signature and the public key.*
- **SegWit (Segregated Witness)** — *SegWit moved signatures out of the transaction body.* **native SegWit / bech32**.
- **Taproot** — *Taproot adds Schnorr signatures and script trees.* **key path / script path**.
- **soft fork / hard fork** — *both were soft forks — backward compatible.*
- **opcode**, **redeem script**, **P2SH / P2WPKH / P2TR** (по буквам).

> Each output has a spending condition expressed as a script; with SegWit the signature lives in the witness, which is why fees are lower, and Taproot makes multisig look like a single-key spend.
