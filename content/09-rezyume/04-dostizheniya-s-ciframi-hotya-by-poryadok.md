---
title: "Достижения с цифрами (хотя бы порядок)"
hot: false
links:
  - { t: "Harvard — Action verbs & resume bullets", u: "https://careerservices.fas.harvard.edu/resources/create-a-strong-resume/" }
---
Сейчас формулировки правильные по форме (глагол + результат), но без чисел читаются как шаблон. Число не обязано быть точным — порядок величины и честная оценка.

Было → стало:

> Реализовал миграцию ключевых модулей фронтенда с React на Vue 3 …, что ускорило время первичной загрузки
→ **Migrated 4 core CRM modules (~25 screens) from React to Vue 3; first-load time dropped from ~4s to ~1.5s** (code splitting, lazy routes).

> Спроектировал и разработал REST API … повысив пропускную способность сервиса
→ **Designed REST API (~30 endpoints) on Laravel; cut p95 latency on report endpoints from 2s to 300ms** by fixing N+1 and adding indexes.

> Спроектировал и внедрил модуль уведомлений …, устранив задержки
→ **Built real-time notifications module (Laravel + Vue); manager response time to new requests went from hours to minutes.**

> Помогал внедрять практику декомпозиции задач и код-ревью
→ **Introduced code review and task decomposition in a team of 3; regressions in release dropped noticeably** (если нет числа — так и написать «noticeably», но назвать команду и артефакт).

Откуда брать числа: Lighthouse до/после, логи APM, число эндпоинтов/таблиц/экранов (`git log`, роуты), размер команды, частота релизов. Если не помнишь — оцени и будь готов сказать «approximately».

Формула bullet'а: **глагол в прошедшем + что + масштаб + эффект**. Не больше 4 пунктов на место, самые сильные — первыми.
