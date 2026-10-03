---
title: "bug, issue, flaky test, regression, root cause, to reproduce, steps to reproduce"
hot: false
sub: "3. Баги, отладка, конкурентность"
---
- **bug** — дефект; **issue** — проблема/тикет (шире); **defect** — формально.
- **flaky test** — тест, который падает иногда: *The test was flaky because of time zones.*
- **regression** — сломалось то, что работало: *The refactor introduced a regression.*
- **root cause** — первопричина: *The root cause was a job enqueued inside a transaction.* *root-cause analysis.*
- **to reproduce / steps to reproduce (repro)** — *I couldn't reproduce it locally.*
- **intermittent** — периодический; **consistent** — воспроизводится всегда.
- **workaround** — обход; **hotfix**; **to patch**.

> It was an intermittent bug with no clear steps to reproduce. Once I found the root cause — a race in the callback — the fix was small, and I added a test to prevent a regression.
