---
title: "`dry-container` / `dry-auto_inject` — DI, одна фраза"
hot: false
links:
  - { t: "dry-container", u: "https://dry-rb.org/gems/dry-container/" }
  - { t: "dry-auto_inject", u: "https://dry-rb.org/gems/dry-auto_inject/" }
  - { t: "dry-system", u: "https://dry-rb.org/gems/dry-system/" }
---
**Контейнер** — реестр зависимостей по ключам:
```ruby
class App < Dry::Container
  register(:node)   { BitcoinNode.new(ENV.fetch("NODE_URL")) }
  register(:mempool, memoize: true) { MempoolClient.new }
end
App[:node]
```

**auto_inject** — автоматически передаёт зависимости в конструктор:
```ruby
Import = Dry::AutoInject(App)

class CreateWithdrawal
  include Import[:node, :mempool]     # добавит kwargs node:, mempool: с дефолтами из контейнера
  def call(...) = node.broadcast(...)
end

CreateWithdrawal.new                      # зависимости из контейнера
CreateWithdrawal.new(node: FakeNode.new)  # подмена в тесте — без моков и stub'ов классов
```

Зачем: явные зависимости вместо `BitcoinNode.new` внутри метода (который нельзя подменить без `allow(BitcoinNode).to receive(:new)`), единая точка конфигурации, ленивая инициализация.

**dry-system** — надстройка: автозагрузка компонентов из папок, провайдеры (`:db`, `:redis`), bootable-зависимости. В Rails обычно избыточно — Zeitwerk и инициализаторы уже есть; уместно в Hanami/roda-проектах.

## Фраза для собеса

«Контейнер — реестр зависимостей, auto_inject — подставляет их в конструктор; тесты подменяют через kwargs без моков классов».
