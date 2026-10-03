---
title: "tradeoff, overhead, overkill, boilerplate, technical debt"
hot: false
sub: "2. Код и архитектура"
---
- **tradeoff** — компромисс: *It's a tradeoff between simplicity and flexibility.* *make / weigh tradeoffs.*
- **overhead** — накладные расходы: *a service object adds a bit of overhead but pays off.*
- **overkill** — избыточно: *dry-rb would be overkill for a CLI.*
- **boilerplate** — шаблонный код: *Rails removes a lot of boilerplate.*
- **technical debt / tech debt** — *we took on some tech debt to ship faster and paid it back later.*
- **premature optimization**, **over-engineering**, **YAGNI**, **good enough**.
- **the cost of / the benefit of**.

> Using a transaction object here is a tradeoff: more boilerplate up front, but much less overhead when the flow grows. For a demo it might be overkill — I'd mention it in the README instead.
