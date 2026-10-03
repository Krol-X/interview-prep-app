---
title: "edge case, corner case, happy path, fallback, default"
hot: false
sub: "2. Код и архитектура"
---
- **happy path** — основной сценарий без ошибок: *I built the happy path first.*
- **edge case** — граничный случай: *zero balance is an edge case.* **corner case** — редкое сочетание условий.
- **fallback** — запасной вариант: *if the rate API fails, we fall back to a cached rate.* (глагол — *fall back on/to*).
- **default** — *the default queue, by default*.
- **to handle** — обрабатывать: *handle the error / the case*.
- **to gracefully degrade**, **fail fast**, **fail loudly**.
- **guard clause** — ранний return.

> I covered the happy path and the main edge cases: insufficient funds, dust change, API down — with a fallback to a cached fee rate.
