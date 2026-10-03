---
title: "Concerns — когда ок, когда зло"
hot: false
links:
  - { t: "Rails API — ActiveSupport::Concern", u: "https://api.rubyonrails.org/classes/ActiveSupport/Concern.html" }
  - { t: "DHH — Put chubby models on a diet with concerns", u: "https://signalvnoise.com/posts/3372-put-chubby-models-on-a-diet-with-concerns" }
---
```ruby
module Trackable
  extend ActiveSupport::Concern
  included do
    has_many :events, as: :trackable
    scope :tracked, -> { where(tracked: true) }
  end
  class_methods do
    def track_all! = update_all(tracked: true)
  end
  def track!(kind) = events.create!(kind:)
end
class Withdrawal < ApplicationRecord; include Trackable; end
```

`Concern` решает две вещи: `included do` выполняет DSL (ассоциации, скоупы) в контексте класса, и зависимости между concern'ами работают.

**Ок**, когда это настоящее горизонтальное поведение, которое включают **несколько** моделей и которое не лезет в их внутренности: soft-delete, slug, tokens, auditing, `Searchable`.

**Зло**, когда:
- concern один и используется одной моделью — это просто порезанный файл; логика размазана, `grep` по методу ведёт в три места;
- concern обращается к полям/методам хоста, которых сам не объявляет — скрытая связь, модуль нельзя понять изолированно;
- через него тестируют «модель похудела», а поведение не выделено в объект.

Альтернатива — composition: сервис/value object/отдельный класс с явной зависимостью. Проще тестировать и читать.

## Фраза для собеса

«Concern — для поведения, общего для нескольких моделей и самодостаточного; для декомпозиции одной жирной модели лучше объекты».
