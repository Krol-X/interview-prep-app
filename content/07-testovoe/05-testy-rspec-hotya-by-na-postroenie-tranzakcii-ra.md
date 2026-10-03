---
title: "Тесты RSpec хотя бы на построение транзакции / расчёт сдачи"
hot: true
links:
  - { t: "RSpec — документация", u: "https://rspec.info/documentation/" }
  - { t: "WebMock", u: "https://github.com/bblimke/webmock" }
---
Не покрытие ради покрытия — три-четыре теста, которые показывают, что ты думаешь о правильных вещах.

```ruby
# spec/tx_builder_spec.rb — чистая логика, без сети
RSpec.describe Wallet::TxBuilder do
  let(:key)   { Bitcoin::Key.generate }
  let(:utxos) { [utxo(100_000, 0), utxo(50_000, 1)] }     # хелпер: txid, vout, value, script

  it "creates payment and change outputs" do
    tx = described_class.new(key).build(utxos, to: dest, amount: 90_000, fee: 1_000)
    expect(tx.in.size).to eq(2)
    expect(tx.out.map(&:value)).to contain_exactly(90_000, 59_000)
  end

  it "omits dust change" do
    tx = ...build(utxos, to: dest, amount: 148_900, fee: 1_000)   # сдача 100 sat
    expect(tx.out.size).to eq(1)
  end

  it "raises on insufficient funds including fee" do
    expect { ...build(utxos, to: dest, amount: 149_500, fee: 1_000) }
      .to raise_error(Wallet::InsufficientFunds, /need 150500/)
  end

  it "produces valid signatures" do
    tx = ...
    expect(tx.verify_input_sig(0, utxos[0].script_pubkey, amount: utxos[0].value)).to be true
  end
end

# spec/mempool_client_spec.rb — HTTP замокан
stub_request(:get, %r{/address/.+/utxo}).to_return(body: fixture("utxos.json"))
stub_request(:post, %r{/tx}).to_return(status: 400, body: "min relay fee not met")
```

- `WebMock.disable_net_connect!` в `spec_helper` — тесты не ходят в интернет.
- Фикстура с реальным ответом mempool (сохранить JSON один раз).
- `to_sat("0.29") == 29_000_000` — тест на float.
- Если осталось время: интеграционный тег `:signet`, который реально отправляет — выключен по умолчанию.
- `bundle exec rspec` в CI (GitHub Actions, 15 строк) — бонус.
