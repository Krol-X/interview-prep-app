---
title: "to implement, to design, to break down (a task), to decouple, to extract (a service)"
hot: false
sub: "2. Код и архитектура"
---
- **implement** — реализовать (не *realize*): *I implemented the exchange flow.*
- **design** — спроектировать: *I designed the schema / the API.*
- **break down a task** — декомпозировать: *I break a feature down into small PRs.*
- **decouple** — разделить зависимости: *I decoupled the notification logic from the model.*
- **extract (a service / a class / a method)** — вынести: *I extracted the fee calculation into its own class.*
- **split / merge** — разбить / слить.
- **abstract away** — скрыть за абстракцией: *The client abstracts away the HTTP details.*
- **wire up** — подключить/связать: *wire up the worker to the queue.*

> I'd break the task down: first the wallet class, then the HTTP client, then wire them up in the CLI.
