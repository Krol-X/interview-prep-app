---
title: "unit test, integration test, coverage, mock, stub, fixture, factory"
hot: false
sub: "4. База данных и тесты"
---
- **unit test** — один класс/метод изолированно; **integration test** — несколько компонентов вместе; **end-to-end (e2e) / system test** — весь поток.
- **coverage** — покрытие: *we had about 80% coverage.*
- **mock** — объект с ожиданиями (*expect(client).to receive(:broadcast)*); **stub** — подмена ответа (*allow(...).to receive(...).and_return(...)*); **double** — фейковый объект в RSpec.
- **fixture** — заготовленные данные (JSON, YAML); **factory** — генератор объектов (FactoryBot).
- **to isolate / to mock out the network** — *I mocked out HTTP with WebMock.*
- **test pyramid**, **TDD**, **red-green-refactor**.

> The builder is covered by unit tests on fixture UTXOs; the HTTP client has integration tests with WebMock stubs, so the suite runs without network.
