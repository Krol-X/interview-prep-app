---
title: "`saved_change_to_X?`, `X_previously_changed?`, dirty tracking"
hot: true
links:
  - { t: "Rails API — ActiveModel::Dirty", u: "https://api.rubyonrails.org/classes/ActiveModel/Dirty.html" }
---
Dirty tracking — модель помнит, что изменилось с момента загрузки.

| До `save` (в before_*, валидациях) | После `save` (в after_save/after_commit) |
|---|---|
| `status_changed?` | `saved_change_to_status?` |
| `status_was` | `status_before_last_save` |
| `status_change` → `["pending","sent"]` | `saved_change_to_status` → `["pending","sent"]` |
| `changed?`, `changes`, `changed_attributes` | `saved_changes`, `saved_changes?` |

Ключевой паттерн — реагировать на **переход**, а не на состояние:

```ruby
after_commit :notify, if: -> { saved_change_to_status?(to: "sent") }
# а не: if: -> { status == "sent" } — сработает при каждом сохранении в sent
```

`will_save_change_to_x?` — синоним `x_changed?`, явно про «в этом save».

Rails 5.1 переименовал: раньше в `after_save` работали `x_changed?` (и это сбивало), теперь там нужны `saved_change_to_*`. Старые имена в after-колбэках — deprecated/неверный результат.

`restore_attributes`, `reload` — сбросить изменения. `update_columns` dirty не трогает.

## Фраза для собеса

«В before — `x_changed?`, в after — `saved_change_to_x?`; с `to:` ловлю конкретный переход, а не состояние».
