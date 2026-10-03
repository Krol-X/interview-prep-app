---
title: "`where` безопасно: placeholders, hash-условия; SQL injection"
hot: true
links:
  - { t: "Rails Guides — Conditions / SQL injection", u: "https://guides.rubyonrails.org/active_record_querying.html#pure-string-conditions" }
  - { t: "Rails Guides — Security: SQL Injection", u: "https://guides.rubyonrails.org/security.html#sql-injection" }
---
```ruby
# ОПАСНО — интерполяция в SQL
Withdrawal.where("status = '#{params[:status]}'")
# params[:status] = "' OR 1=1 --"  → все строки
# params[:status] = "'; DROP TABLE withdrawals; --"

# Безопасно
Withdrawal.where(status: params[:status])                  # хеш-условие: экранируется, типизируется
Withdrawal.where("amount > ?", params[:min])               # позиционный placeholder
Withdrawal.where("amount > :min AND fee < :max", min: 1, max: 9)   # именованный
Withdrawal.where(created_at: 1.day.ago..)                  # range → BETWEEN / >=
Withdrawal.where(status: %w[sent failed])                  # IN (...)
Withdrawal.where.not(txid: nil)                            # IS NOT NULL
```

Что ещё инъекционно: `order(params[:sort])`, `pluck(params[:col])`, `select("...")`, `joins("...")`, `group`, `having`, `find_by_sql`. Для динамических имён колонок — белый список: `order(SORTS.fetch(params[:sort], :id))`. Или `sanitize_sql_like` для LIKE, `Arel.sql` — только для заведомо константных строк (явно помечаешь «я проверил»).

Хеш-условия и placeholders заодно приводят типы: `where(id: "5abc")` → 5, а строка в SQL — нет.

## Фраза для собеса

«Никакой интерполяции в SQL: хеш-условия или placeholders; `order`/`select` с пользовательским вводом — только через белый список».
