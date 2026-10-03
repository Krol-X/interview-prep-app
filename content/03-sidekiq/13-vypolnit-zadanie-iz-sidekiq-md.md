---
title: "Выполнить задание из sidekiq.md"
hot: false
links:
  - { t: "Sidekiq README", u: "https://github.com/sidekiq/sidekiq" }
---
Практика на 1.5–2 часа, без Rails. Проверяет всё, что выше.

**Сетап**: `docker run -p 6379:6379 redis`, Gemfile с `sidekiq`, `redis`, `rspec`.

**Воркер** `BroadcastTxWorker.perform(withdrawal_id)`:
- состояние в Redis-хеше `withdrawal:<id>` (`status`, `txid`);
- `fake_broadcast` — спит 0.5 с, в 30% случаев бросает `Timeout::Error`, иначе возвращает hex-txid;
- идемпотентность: `status == sent` → выход;
- атомарный захват `pending → processing` через `SET NX` на lock-ключ или Lua — и комментарий, почему `HGET`+`HSET` — гонка;
- `Timeout::Error` не глотать — пусть ретраит; `retry: 5`, свой `sidekiq_retry_in`;
- `sidekiq_retries_exhausted` → `status = failed`.

**Нагрузка** `enqueue.rb`: 20 выводов, каждый джоб поставить **дважды** (дабл-клик). После прогона — ровно один txid на каждый `sent`.

**Запуск**: `bundle exec sidekiq -r ./worker.rb -c 5`, Web UI через `rackup` с `Sidekiq::Web` — посмотреть retry set вживую.

**Тесты** (`Sidekiq::Testing.fake!`): джоб ставится; повторный `perform` для `sent` ничего не меняет.

Критерий «сделано»: можешь объяснить, что произойдёт, если убить процесс посреди `fake_broadcast`.
