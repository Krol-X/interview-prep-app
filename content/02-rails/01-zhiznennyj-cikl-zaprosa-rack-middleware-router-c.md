---
title: "Жизненный цикл запроса: Rack → middleware → router → controller → view/render"
hot: true
links:
  - { t: "Rails Guides — Rails on Rack", u: "https://guides.rubyonrails.org/rails_on_rack.html" }
  - { t: "Rails Guides — Action Controller Overview", u: "https://guides.rubyonrails.org/action_controller_overview.html" }
---
```
Puma (сервер) → Rack env (хеш запроса)
  → middleware stack (~20 штук: логгер, сессии, cookies, CSRF, ExecutorRails, ...)
    → ActionDispatch::Routing (config/routes.rb) → контроллер#action
      → before_action → action → render/redirect → after_action
    ← ответ [status, headers, body] через middleware обратно
```

- **Rack** — интерфейс: объект с `call(env)` возвращает `[status, headers, body]`. Rails-приложение — тоже Rack-приложение. `rails middleware` покажет стек.
- **Router** сопоставляет метод+путь, кладёт `params[:id]` и т.п. `resources :withdrawals` даёт 7 маршрутов.
- **Контроллер**: один экземпляр на запрос. `params` — `ActionController::Parameters`. Один `render`/`redirect_to` на action (иначе `DoubleRenderError`); без явного — рендерит шаблон по имени action.
- **Executor/Reloader** — middleware, который оборачивает запрос: отдаёт AR-соединение в пул, перезагружает код в dev.
- Исключение → `ActionDispatch::ShowExceptions` → страница 500/404 (`rescue_from` в контроллере — раньше).

Ответ в API-режиме (`rails new --api`): урезанный стек без cookies/sessions/flash.

## Фраза для собеса

«Puma → Rack middleware → роутер → контроллер → колбэки → action → render; всё, что между сервером и роутером — middleware, туда же можно вставить своё».
