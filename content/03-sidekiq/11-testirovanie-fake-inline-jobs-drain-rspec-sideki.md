---
title: "Тестирование: `fake!`, `inline!`, `.jobs`, `drain`, rspec-sidekiq"
hot: true
links:
  - { t: "Sidekiq wiki — Testing", u: "https://github.com/sidekiq/sidekiq/wiki/Testing" }
  - { t: "rspec-sidekiq", u: "https://github.com/wspurgin/rspec-sidekiq" }
---
```ruby
# spec/rails_helper.rb
require "sidekiq/testing"
Sidekiq::Testing.fake!        # по умолчанию: джобы складываются в массив, не выполняются
RSpec.configure { |c| c.before { Sidekiq::Worker.clear_all } }
```

```ruby
it "enqueues processing after commit" do
  expect { create(:withdrawal) }
    .to change(ProcessWithdrawalWorker.jobs, :size).by(1)
  expect(ProcessWithdrawalWorker.jobs.last["args"]).to eq([Withdrawal.last.id])
end

it "processes" do
  create(:withdrawal)
  ProcessWithdrawalWorker.drain          # выполнить всё накопленное этого класса
  # Sidekiq::Worker.drain_all — все классы, включая порождённые
  expect(Withdrawal.last).to be_sent
end

it "runs perform directly" do
  ProcessWithdrawalWorker.new.perform(withdrawal.id)   # юнит-тест логики, без Redis
end

Sidekiq::Testing.inline! do             # выполнять сразу при perform_async
  create(:withdrawal)                   # осторожно: внутри транзакции запись «не видна» — fake! надёжнее
end
```

С `rspec-sidekiq`: `expect(Worker).to have_enqueued_sidekiq_job(id).in(5.minutes).on("critical")`.

Что тестировать: 1) что джоб ставится в нужный момент с нужными аргументами (после коммита!), 2) логику `perform` напрямую, 3) идемпотентность — вызвать `perform` дважды, результат один, 4) исчерпание ретраев — вызвать блок `sidekiq_retries_exhausted_block`.

ActiveJob: `have_enqueued_job`, `perform_enqueued_jobs { }`, `ActiveJob::Base.queue_adapter = :test`.

## Фраза для собеса

«`fake!` + `.jobs` для проверки постановки, `drain` или прямой `perform` для логики, второй вызов `perform` — для идемпотентности».
