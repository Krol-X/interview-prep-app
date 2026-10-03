---
title: "method, class, module, inheritance, composition, interface, abstraction"
hot: false
sub: "2. Код и архитектура"
---
- **method / class / module** — *a class method, an instance method, a module mixed in with include.*
- **inheritance** — наследование: *inherits from ApplicationRecord*; **composition** — композиция: *I prefer composition over inheritance.*
- **interface** — контракт (в Ruby — duck typing): *as long as it responds to call, it fits the interface.*
- **abstraction** — *the right level of abstraction.*
- **encapsulation**, **polymorphism**, **duck typing**.
- **mixin** — модуль-примесь. **namespace** — пространство имён.
- **dependency injection** — *I inject the client so I can stub it in tests.*

> Instead of inheritance I'd use composition: a Wallet that has a KeyStore and a Client, both injected, so each piece is testable on its own.
