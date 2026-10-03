---
title: "ActionMailer: `deliver_now` vs `deliver_later`"
hot: true
links:
  - { t: "Rails Guides — Action Mailer Basics", u: "https://guides.rubyonrails.org/action_mailer_basics.html" }
---
```ruby
UserMailer.withdrawal_sent(user, withdrawal).deliver_now     # синхронно, прямо сейчас, в этом потоке
UserMailer.withdrawal_sent(user, withdrawal).deliver_later   # через ActiveJob в очередь
UserMailer.with(user:, withdrawal:).withdrawal_sent.deliver_later(wait: 1.minute)
```

- `deliver_now` блокирует запрос на время SMTP (сотни мс — секунды); при падении почты падает запрос; внутри транзакции — письмо уйдёт, а транзакция может откатиться.
- `deliver_later` сериализует аргументы через GlobalID (модели → `gid://app/User/1`), в джобе загружает заново. Запись должна быть **закоммичена** → вызывать из `after_commit`, не `after_save`. Если запись удалят до отправки — `DeserializationError`.
- `deliver_later` требует настроенного `queue_adapter` (Sidekiq/Solid Queue); с `:async` в dev письма шлются в потоке процесса и теряются при рестарте.
- Параметры лучше через `.with(...)` (параметризованные мейлеры) — и шаблон, и `params` одинаково.
- Тесты: `assert_enqueued_email_with`, `have_enqueued_mail`, `ActionMailer::Base.deliveries` при `delivery_method = :test`; `perform_enqueued_jobs` чтобы прогнать.
- Preview: `test/mailers/previews` → `/rails/mailers`.

## Фраза для собеса

«Из приложения — `deliver_later` из `after_commit`; `deliver_now` — только в джобе или консоли».
