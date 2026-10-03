---
title: "request / response, endpoint, payload, serialization, status code"
hot: false
sub: "2. Код и архитектура"
---
- **request / response** — *the request body, the response headers.*
- **endpoint** — *the POST /exchanges endpoint.*
- **payload** — тело данных: *the JSON payload.*
- **serialization / to serialize / deserialize** — *we serialize the model to JSON.*
- **status code** — *returns a 422 (four twenty-two) for validation errors, 201 (two-oh-one) on create.*
- **to hit an endpoint** (разг.) — обратиться: *the frontend hits the rates endpoint.*
- **rate limit, timeout, retry, idempotency key.**
- **REST / RESTful, resource, route, params.**

> The form posts to the exchanges endpoint; the controller validates the payload and returns 422 with errors or 201 with the serialized exchange.

Числа: 200 «two hundred», 404 «four-oh-four», 500 «five hundred».
