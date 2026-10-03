---
title: "Docker"
hot: false
links:
  - { t: "Docker docs — Dockerfile best practices", u: "https://docs.docker.com/build/building/best-practices/" }
  - { t: "Official Ruby image", u: "https://hub.docker.com/_/ruby" }
---
```dockerfile
# Dockerfile
FROM ruby:3.3-slim
RUN apt-get update -qq && apt-get install -y --no-install-recommends build-essential libssl-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY Gemfile Gemfile.lock ./
RUN bundle config set --local without 'development test' && bundle install --jobs 4
COPY . .
RUN useradd -m app && chown -R app /app
USER app
ENTRYPOINT ["ruby", "wallet.rb"]
CMD ["balance"]
```

```yaml
# docker-compose.yml
services:
  wallet:
    build: .
    volumes:
      - ./data:/app/data        # ключ живёт на хосте, переживает пересборку
    environment:
      WALLET_PATH: /app/data/wallet.wif
      MEMPOOL_URL: https://mempool.space/signet/api
```

```
docker compose run --rm wallet address
docker compose run --rm wallet send tb1q... 0.0001
```

- Слои: Gemfile копируется и `bundle install` до `COPY . .` — кэш не сбрасывается при каждом изменении кода.
- `slim`, не `alpine` для Ruby (musl + нативные гемы = боль); `build-essential` нужен для `secp256k1`/`openssl` в bitcoinrb — либо multi-stage, чтобы не тащить компилятор в финальный образ.
- Не root. Ключ — только через volume, не в образе (`.dockerignore`: `data/`, `.env`, `.git`).
- `.dockerignore` обязателен, иначе в контекст попадёт всё.
- Для второго задания — добавить `db: postgres:16`, `redis`, `web` с `depends_on` и `healthcheck`.
