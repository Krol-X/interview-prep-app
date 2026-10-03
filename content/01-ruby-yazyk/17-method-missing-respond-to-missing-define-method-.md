---
title: "`method_missing` + `respond_to_missing?`, `define_method`, `send`/`public_send`"
hot: true
links:
  - { t: "Ruby docs — BasicObject#method_missing", u: "https://docs.ruby-lang.org/en/master/BasicObject.html#method-i-method_missing" }
  - { t: "Ruby docs — Module#define_method", u: "https://docs.ruby-lang.org/en/master/Module.html#method-i-define_method" }
---
```ruby
class Proxy
  def method_missing(name, *args, &blk)
    return super unless name.to_s.start_with?("find_by_")
    find(name.to_s.delete_prefix("find_by_"), *args)
  end

  def respond_to_missing?(name, include_private = false)
    name.to_s.start_with?("find_by_") || super
  end
end
```

- `method_missing` вызывается, когда метод не найден во всей цепочке. **Всегда** вызывать `super` для чужих имён — иначе проглотишь опечатки и получишь nil вместо `NoMethodError`.
- `respond_to_missing?` — пара к нему, иначе `respond_to?` и `method(:x)` врут.
- Медленно: промах по всей цепочке + разбор имени на каждый вызов. Часто комбинируют: первый раз через `method_missing`, и тут же `define_method`, чтобы дальше было быстро (так делал старый ActiveRecord).

```ruby
%w[sent failed].each do |st|
  define_method("#{st}?") { status == st }    # метод с замыканием; быстрее method_missing
end
```

`send`/`public_send`: вызов по имени. `public_send` уважает private — предпочтительнее с внешними данными. `send` ломает инкапсуляцию, допустимо в тестах и внутри класса.

## Фраза для собеса

«`method_missing` всегда в паре с `respond_to_missing?` и `super`; где можно — лучше `define_method`, он быстрее и виден интроспекции».
