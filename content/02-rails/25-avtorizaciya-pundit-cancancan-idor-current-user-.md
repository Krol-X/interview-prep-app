---
title: "Авторизация: Pundit/CanCanCan; IDOR (`current_user.records.find`)"
hot: true
links:
  - { t: "Pundit", u: "https://github.com/varvet/pundit" }
  - { t: "OWASP — IDOR", u: "https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html" }
---
Аутентификация — *кто ты*. Авторизация — *что тебе можно*. Самая частая дыра — **IDOR**: `Withdrawal.find(params[:id])` отдаёт чужую запись, достаточно перебрать id.

```ruby
# IDOR
@w = Withdrawal.find(params[:id])
# Фикс — скоупить через владельца: чужой id → 404
@w = current_user.withdrawals.find(params[:id])
```

Для ролей и правил — Pundit:
```ruby
class WithdrawalPolicy < ApplicationPolicy
  def show?    = record.user == user || user.admin?
  def create?  = user.verified?
  class Scope < Scope
    def resolve = user.admin? ? scope.all : scope.where(user:)
  end
end

# контроллер
def show
  @w = authorize Withdrawal.find(params[:id])     # NotAuthorizedError → rescue_from → 403
end
def index
  @ws = policy_scope(Withdrawal)
end
after_action :verify_authorized      # забыл authorize → ошибка в dev/test
```

CanCanCan — альтернатива: одна `Ability` с `can :read, Withdrawal, user_id: user.id`; удобно для простых CRUD, хуже масштабируется.

Ещё: не доверять `params[:user_id]`; проверять права и в джобах/сервисах, не только в контроллере; admin-функции — отдельный namespace + проверка роли.

## Фраза для собеса

«Записи всегда через `current_user.xxx.find` — чужое становится 404; правила — в policy-объектах с `verify_authorized`».
