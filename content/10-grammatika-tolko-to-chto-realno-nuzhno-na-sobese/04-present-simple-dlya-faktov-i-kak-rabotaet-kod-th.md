---
title: "**Present Simple** для фактов и как работает код: *The wallet fetches UTXOs. The worker retries on failure.*"
hot: false
sub: "Времена (90% разговора)"
links:
  - { t: "englishpage — Simple Present", u: "https://www.englishpage.com/verbpage/simplepresent.html" }
---
**Правило**: факты, регулярные действия и — главное для тебя — **как работает код/система**. Объяснение любой архитектуры идёт в Present Simple.

- *The wallet fetches UTXOs from the API and sums their values.*
- *The worker retries on failure with exponential backoff.*
- *Sidekiq stores jobs in Redis.*
- *Each input references a previous output.*

Не забывать **-s** в 3-м лице: *the method return**s***, *it raise**s** an error*, *the job run**s***. Это самая частая слышимая ошибка.

Вопрос — через **does**: *How does the fee get calculated? What does the callback do?*

Типичная ошибка: описывать систему в Present Continuous (*the worker is retrying*) — это означает «прямо сейчас, в данный момент», а не «так устроено».

Про себя: *I work mostly on the backend. I prefer explicit code. I write tests first when the logic is tricky.*
