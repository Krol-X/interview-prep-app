---
title: "Rack middleware — написать своё за 5 строк"
hot: false
links:
  - { t: "Rails Guides — Rails on Rack", u: "https://guides.rubyonrails.org/rails_on_rack.html" }
  - { t: "Rack spec", u: "https://github.com/rack/rack/blob/main/SPEC.rdoc" }
---
Middleware — объект, который получает следующее приложение в `initialize` и обрабатывает `call(env)`:

```ruby
class RequestTimer
  def initialize(app) = @app = app

  def call(env)
    start = Process.clock_gettime(Process::CLOCK_MONOTONIC)
    status, headers, body = @app.call(env)       # передать дальше по цепочке
    headers["X-Runtime-Ms"] = ((Process.clock_gettime(Process::CLOCK_MONOTONIC) - start) * 1000).round(1).to_s
    [status, headers, body]
  end
end

# config/application.rb
config.middleware.use RequestTimer
config.middleware.insert_before Rack::Runtime, RequestTimer
config.middleware.delete Rack::ETag
```

- `env` — хеш: `REQUEST_METHOD`, `PATH_INFO`, `HTTP_*` заголовки, `rack.input`. Удобно обернуть: `req = Rack::Request.new(env)`.
- Можно не вызывать `@app` — вернуть ответ сразу (maintenance mode, rate limit, блок по IP): `return [503, {"content-type"=>"text/plain"}, ["down"]]`.
- `body` должен отвечать на `each` (массив строк) и желательно `close`.
- Один экземпляр на процесс — **без состояния в иварах** (многопоточность Puma).
- `rails middleware` — список. Rails сам — тоже middleware-стек поверх роутера.

Примеры из жизни: `Rack::Attack` (rate limit), `Rack::Cors`, request id, свой logger, трассировка.

## Фраза для собеса

«Класс с `initialize(app)` и `call(env)`, возвращающий `[status, headers, body]`; вставляется через `config.middleware`; без состояния в экземпляре».
