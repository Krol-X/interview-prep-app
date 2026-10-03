---
title: "`save` vs `save!`, `update` vs `update!` vs `update_attribute` vs `update_column(s)`"
hot: true
links:
  - { t: "Rails API — ActiveRecord::Persistence", u: "https://api.rubyonrails.org/classes/ActiveRecord/Persistence.html" }
---
| Метод | Валидации | Колбэки | updated_at | При ошибке |
|---|---|---|---|---|
| `save` / `update(attrs)` | да | да | да | `false` |
| `save!` / `update!` | да | да | да | `RecordInvalid` |
| `update_attribute(:a, v)` | **нет** | да | да | false |
| `update_column(s)` | нет | **нет** | **нет** | — (прямой SQL) |
| `update_all` (relation) | нет | нет | нет | число строк |
| `touch` | нет | after_touch | да | — |
| `increment!` / `decrement!` | нет | нет | да | — (атомарный UPDATE) |

Правила:
- В сервисах и джобах — `!`-версии: ошибку нельзя молча потерять. Без `!` — в контроллере, когда ветвишься по результату.
- `update_attribute` — «пропустить валидации, но оставить колбэки». Почти всегда это запах: валидации нужны. Исключение — служебные поля.
- `update_column` — для технических записей (счётчики, last_seen_at), когда колбэки и валидации нежелательны и ты точно знаешь, что делаешь. Не триггерит dirty.
- `update_all` — массово, одним SQL, без загрузки объектов: `Withdrawal.where(status: "pending").update_all(status: "expired")`.

Для денег: `increment!(:balance, amount)` или `update_all("balance = balance + ?")` — атомарно, вместо read-modify-write.

## Фраза для собеса

«В бизнес-логике `save!`/`update!`; `update_column(s)` и `update_all` — обход валидаций и колбэков, применяю осознанно».
