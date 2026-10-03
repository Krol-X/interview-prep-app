---
title: "Rails credentials / ENV, `.env`"
hot: false
links:
  - { t: "Rails Guides — Custom Credentials", u: "https://guides.rubyonrails.org/security.html#custom-credentials" }
  - { t: "gem dotenv", u: "https://github.com/bkeepers/dotenv" }
---
Секреты (ключи API, приватный ключ кошелька, пароли БД) — **не в git**.

**ENV** — 12-factor, стандарт для Docker/Heroku/K8s:
```ruby
ENV.fetch("BITCOIN_WIF")           # fetch — упасть сразу, если не задан
ENV.fetch("FEE_SAT", "1000").to_i  # дефолт
```
В dev — `.env` через gem dotenv (файл в `.gitignore`, `.env.example` — в репо с пустыми значениями). Плюсы: платформа-независимо, легко ротировать. Минусы: видны в `ps`/дампах окружения, нет структуры.

**Rails credentials** — зашифрованный YAML в репо, ключ отдельно:
```
bin/rails credentials:edit --environment production   # config/credentials/production.yml.enc + .key
Rails.application.credentials.dig(:bitcoin, :wif)
```
Ключ — через `RAILS_MASTER_KEY` ENV на сервере. Плюсы: структура, версионируется вместе с кодом. Минусы: один ключ на всё, ротация = перешифровать, в контейнерах всё равно нужен ENV для ключа.

Практика: инфраструктурные (DATABASE_URL, REDIS_URL) — ENV; прикладные — либо-либо, лишь бы последовательно. Не логировать (`filter_parameters`), не коммитить `.key`, в тестовом задании — `.env.example` + README.

## Фраза для собеса

«Секреты в ENV через `fetch` или в credentials с мастер-ключом из ENV; в репо — только `.env.example`».
