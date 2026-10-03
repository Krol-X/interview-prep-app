---
title: "maintainable, readable, testable, reusable, scalable, robust"
hot: false
sub: "2. Код и архитектура"
---
Прилагательные про качество кода — как аргументы в обсуждении:

- **maintainable** — легко поддерживать; **readable** — читаемый; **testable** — тестируемый (*injected dependencies make it testable*); **reusable** — переиспользуемый; **scalable** — масштабируемый; **robust** — устойчивый к ошибкам; **reliable** — надёжный; **predictable**; **explicit** vs **implicit** («magic»); **consistent**; **idiomatic** (*idiomatic Ruby*).
- Существительные: *maintainability, readability, reliability.*
- Антонимы: *brittle* (хрупкий), *fragile*, *tightly coupled*, *convoluted* (запутанный), *hacky*.

> I'd extract it into a service: it's more testable, the controller stays readable, and the logic becomes reusable from the admin panel.
