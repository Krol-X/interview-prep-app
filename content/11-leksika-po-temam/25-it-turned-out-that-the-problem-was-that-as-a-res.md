---
title: "it turned out that…, the problem was that…, as a result…"
hot: false
sub: "3. Баги, отладка, конкурентность"
---
Связки для рассказа о расследовании:

- **It turned out that…** — оказалось: *It turned out that the job ran before the commit.*
- **The problem was that…** — *The problem was that the record didn't exist yet.*
- **As a result, …** — в результате: *As a result, the job retried and created a duplicate.*
- **That's why / which is why** — *which is why I moved it to after_commit.*
- **Once I realized that, …** — как только понял.
- **In the end / eventually** — в конце концов.
- **Looking back, …** — оглядываясь назад.
- **The fix was to…** — *The fix was to add a unique index.*

> It turned out the enqueue happened inside the transaction. As a result, the worker couldn't find the record and retried. The fix was to enqueue after commit; looking back, I'd also add the unique index from day one.
