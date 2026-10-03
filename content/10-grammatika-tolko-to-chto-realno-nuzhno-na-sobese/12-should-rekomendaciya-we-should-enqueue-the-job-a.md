---
title: "*should* — рекомендация: *We should enqueue the job after commit.*"
hot: false
sub: "Модальные"
links:
  - { t: "Cambridge — should", u: "https://dictionary.cambridge.org/grammar/british-grammar/should" }
---
**should + V1** — рекомендация, «правильно было бы». Мягче, чем *must*, профессиональнее, чем *need to*.

- *We should enqueue the job after commit, not inside the transaction.*
- *Jobs should be idempotent.*
- *You should probably add an index on that column.*
- *The fee shouldn't be a constant — it should come from config.*

Прошлое (критика задним числом): **should have + V3** — *We should have used a unique constraint from the start.*

В code review: *«I think this should be extracted into a service»* — стандартная формула. *Might want to* — ещё мягче: *You might want to memoize this.*

Типичная ошибка: *should to do* ✗; *should be do* ✗ → *should do / should be done*.
