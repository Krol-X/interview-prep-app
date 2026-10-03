---
title: "hash, to hash, digest, checksum, to encode (bech32)"
hot: false
sub: "5. Bitcoin (твоё тестовое + их продукт)"
---
- **hash / to hash** — *hash the public key with SHA-256 then RIPEMD-160.* **hash160**.
- **digest** — результат хеша. **preimage** — прообраз.
- **checksum** — *bech32 includes a checksum that catches typos.*
- **to encode / to decode** — *encode the hash as bech32; decode the address to get the script.*
- **base58 / bech32 / hex** — *hex string, base58check.*
- **collision**, **one-way function**, **to commit to** (криптографически): *the sighash commits to the input amount.*
- **double SHA-256**, **Merkle root / Merkle tree**.

> The address is a bech32 encoding of the public key hash plus a checksum, so a typo is caught before anything is sent.
