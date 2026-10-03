---
title: "Аргументы только JSON-примитивы; передавать `id`"
hot: true
links:
  - { t: "Sidekiq wiki — Best Practices (#1 Make your job parameters small and simple)", u: "https://github.com/sidekiq/sidekiq/wiki/Best-Practices" }
---
Аргументы сериализуются в JSON. Проходят: строки, числа, `true/false/nil`, массивы и хеши из них. **Не проходят**: AR-модели, символы (станут строками), `Date/Time` (станут строками), `Struct`, любые объекты.

```ruby
perform_async(withdrawal)          # → "#<Withdrawal:0x...>" или хеш атрибутов — в perform придёт мусор
perform_async(withdrawal.id)       # правильно
perform_async(status: :sent)       # ключ станет "status", значение "sent"
perform_async(Time.now)            # строка; парсить в perform
```

Sidekiq 7 в strict-режиме (`Sidekiq.strict_args!`, по умолчанию в dev/test) бросает `ArgumentError` на неJSON-аргументы — ловится на раннем этапе.

Почему id, а не объект:
- объект устареет: между enqueue и perform запись могла измениться; воркер должен прочитать **актуальное** состояние;
- маленький payload — Redis и память;
- в perform делаем `Withdrawal.find(id)` и обрабатываем `RecordNotFound` (запись удалили — выйти без ретрая).

Внутри `perform` хеши приходят со **строковыми** ключами: `opts["fee"]`, не `opts[:fee]`. Удобно: `opts = opts.symbolize_keys` или kwargs не использовать вовсе.

ActiveJob решает это GlobalID (`gid://app/Withdrawal/5`), но та же суть — передаётся ссылка, объект грузится в джобе.

## Фраза для собеса

«Только JSON-примитивы и передаю id: воркер читает свежую запись, payload маленький, а strict_args ловит ошибки сразу».
