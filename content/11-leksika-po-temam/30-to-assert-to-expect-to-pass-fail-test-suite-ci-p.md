---
title: "to assert, to expect, to pass / fail, test suite, CI pipeline"
hot: false
sub: "4. База данных и тесты"
---
- **to assert / an assertion** — утверждать в тесте; в RSpec — **to expect**: *I expect the output count to be two.*
- **to pass / to fail** — *the test passes / fails*; **green / red**.
- **test suite** — весь набор: *the suite runs in forty seconds.*
- **CI pipeline** — *CI runs the suite on every push.* **to break the build** — сломать сборку.
- **to be covered by tests**, **test case**, **spec** (RSpec файл), **matcher**, **setup / teardown**, **before each**.
- **flaky**, **to skip / pending**.

> I set up a GitHub Actions pipeline: on every push it runs rubocop and the RSpec suite; a failing spec breaks the build.
