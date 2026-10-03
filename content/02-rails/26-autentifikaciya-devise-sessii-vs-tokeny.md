---
title: "Аутентификация: Devise, сессии vs токены"
hot: false
links:
  - { t: "Devise", u: "https://github.com/heartcombo/devise" }
  - { t: "Rails Guides — Security: Sessions", u: "https://guides.rubyonrails.org/security.html#sessions" }
  - { t: "Rails 8 authentication generator", u: "https://github.com/rails/rails/blob/main/railties/lib/rails/generators/rails/authentication/USAGE" }
---
**Сессии (cookie)** — классический web: после логина `session[:user_id] = user.id`; Rails хранит сессию в подписанной+зашифрованной cookie (`cookie_store`). Защита CSRF обязательна (`protect_from_forgery`, токен в формах). Логаут = удалить ключ. Подходит для серверного рендера и SPA на том же домене.

**Токены** — для API и мобильных: клиент шлёт `Authorization: Bearer <token>`.
- Opaque token в БД (`has_secure_token`, хранить хеш) — можно отозвать, просто.
- JWT — самодостаточный, stateless, не отзывается до истечения (нужен короткий TTL + refresh token). Не хранить в нём секреты.
CSRF не актуален, но XSS опаснее: токен в `localStorage` уязвим; `httpOnly` cookie + SameSite — компромисс.

Инструменты:
- **Devise** — всё из коробки: регистрация, подтверждение, восстановление, lockable, `has_secure_password` под капотом (bcrypt). Много магии, сложно кастомизировать.
- **Rails 8 `bin/rails generate authentication`** — минимальный встроенный генератор: сессии в БД, bcrypt, сброс пароля. Прозрачный код в проекте.
- `has_secure_password` руками — для API достаточно 30 строк.

Гигиена: bcrypt/argon2, никаких plaintext, ограничение попыток, `secure`/`httpOnly`/`SameSite` cookie, ротация сессии при логине (`reset_session`).

## Фраза для собеса

«Сессии в cookie + CSRF для web; токены для API — opaque с хешем в БД или короткоживущий JWT; пароли только через bcrypt».
