---
title: "A bug I found and fixed — STAR, 90 сек"
hot: true
links:
  - { t: "STAR method", u: "https://www.themuse.com/advice/star-interview-method" }
---
**STAR**: Situation (1 предложение) → Task → Action (основная часть, что делал *ты*) → Result (цифра или факт) → *Learning* (одно предложение). Выбери реальный баг, желательно про данные/конкурентность — это их домен.

Шаблон с твоего опыта (замени детали на настоящие):

> **S** — At Sovtech we had a CRM where managers sometimes saw duplicate notifications — the same event delivered two or three times. It was intermittent, maybe once a day, and nobody could reproduce it.
>
> **T** — I took it because it was annoying users and eroding trust in the system.
>
> **A** — I started from logs and found the duplicates always came within the same second. That pointed to concurrency, not logic. The notification was created in a model callback right after the record was saved, and the job that delivered it ran before the transaction committed — so when the job failed to find the record, it retried, and meanwhile a second code path had already created another notification. Two problems: a job enqueued inside a transaction, and no idempotency on the delivery side. I moved the enqueue to after commit, and added a unique key on event id plus recipient so a second insert would fail instead of duplicating.
>
> **R** — Duplicates went to zero; I verified over two weeks of logs. The fix was about twenty lines plus a migration.
>
> **L** — Since then I treat "enqueue after commit" and "make side effects idempotent" as defaults, not optimizations.

Если это было на Laravel — так и сказать (`dispatch` внутри transaction, `afterCommit`), суть та же и интервьюеру понятна.

Избегать: баг, где виноват кто-то другой; баг без твоих действий; история длиннее 90 секунд.
