---
title: "Strong params: `require`/`permit`, mass assignment"
hot: true
links:
  - { t: "Rails Guides — Strong Parameters", u: "https://guides.rubyonrails.org/action_controller_overview.html#strong-parameters" }
---
Mass assignment — `Model.new(params)` присваивает все переданные поля. Без фильтра пользователь пришлёт `admin: true` или `balance: 1e9` (GitHub, 2012).

```ruby
def withdrawal_params
  params.require(:withdrawal).permit(:to_address, :amount)
end
```

- `require(:key)` — ключ обязан быть, иначе `ParameterMissing` → 400.
- `permit(...)` — белый список. Непермиченные ключи молча отбрасываются (в dev — лог, можно `config.action_controller.action_on_unpermitted_parameters = :raise`).
- Массивы и вложенность: `permit(:name, tags: [], address: [:city, :zip])`. Произвольный хеш — `permit(meta: {})`.
- Никогда не пермить `status`, `user_id`, `fee`, `role` — то, что назначает сервер. Присваивать явно: `Withdrawal.new(withdrawal_params.merge(user: current_user))`.
- `params.expect(withdrawal: [:to_address, :amount])` — Rails 8, require+permit одной строкой и устойчивее к мусору в параметрах.

`params[:x]` без permit — ок для чтения одиночных значений (`params[:id]`), проблема только в передаче всего хеша в модель.

## Фраза для собеса

«Белый список через `permit`, серверные поля назначаю явно, а не из параметров; mass assignment без фильтра — это как `admin: true` в форме».
