---
title: "`Comparable` и `Enumerable` в своём классе (`<=>`, `each`)"
hot: false
links:
  - { t: "Ruby docs — Comparable", u: "https://docs.ruby-lang.org/en/master/Comparable.html" }
  - { t: "Ruby docs — Enumerable", u: "https://docs.ruby-lang.org/en/master/Enumerable.html" }
---
Два модуля-«миксина», которые дают много методов за реализацию одного.

```ruby
class Money
  include Comparable
  attr_reader :cents
  def initialize(cents) = @cents = cents
  def <=>(other) = cents <=> other.cents   # -1, 0, 1 или nil
end

Money.new(5) < Money.new(10)     # true
[m3, m1, m2].sort.first          # sort использует <=>
m.between?(a, b); m.clamp(a, b)
```

`Comparable` даёт `< <= == >= > between? clamp` из одного `<=>`. Внимание: он переопределяет `==` через `<=>` — объекты равны, если `<=>` вернул 0.

```ruby
class Wallet
  include Enumerable
  def each(&block)
    return enum_for(:each) unless block
    @utxos.each(&block)
  end
end

wallet.sum(&:value); wallet.select(&:confirmed?); wallet.min_by(&:value); wallet.lazy
```

`Enumerable` даёт всё — map/select/sort_by/include?/first/to_a — из одного `each`. `each` должен `yield`-ить элементы по одному.

## Фраза для собеса

«Реализую `<=>` и включаю `Comparable` — получаю сравнения и sort; реализую `each` и включаю `Enumerable` — получаю всю коллекционную алгебру».
