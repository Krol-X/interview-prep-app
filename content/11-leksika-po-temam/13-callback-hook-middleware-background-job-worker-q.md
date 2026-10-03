---
title: "callback, hook, middleware, background job, worker, queue, scheduler"
hot: false
sub: "2. Код и архитектура"
---
- **callback** — *an after_save callback*; **hook** — то же, более общо: *a lifecycle hook, a git hook.*
- **middleware** — *Rack middleware, Sidekiq server middleware.*
- **background job** — фоновая задача; **worker** — процесс/класс, который её выполняет; **queue** — очередь: *enqueue a job, the job is picked up by a worker from the default queue.*
- **scheduler / cron** — *a scheduled job runs every hour.*
- **to enqueue / to dequeue**, **to process**, **to retry**, **dead set**.
- **asynchronously / in the background**: *we send emails asynchronously.*

> On save, a callback enqueues a job; a Sidekiq worker picks it up from the queue and processes it in the background, with retries on failure.
