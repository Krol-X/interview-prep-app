# prep — чеклист повторения как документация

Vue 3 + Vite. Контент — markdown-файлы в `content/`, собираются на этапе сборки.

```
content/
  01-ruby-yazyk/
    _section.md            # title, group — метаданные раздела
    02-proc-vs-lambda.md   # один пункт
```

Пункт:

```md
---
title: "`Proc` vs `lambda`: arity, `return`"
hot: true                 # важное — точка в списке, фильтр «только важное»
sub: "Времена"            # необязательная подгруппа внутри раздела
links:
  - { t: "Ruby docs — Proc", u: "https://docs.ruby-lang.org/en/master/Proc.html" }
---
Текст в markdown. Пустой файл = пункт есть, содержимое ещё не написано («todo» в списке).
```

Порядок разделов и пунктов — по имени файла (префикс `NN-`).

```
npm i
npm run dev        # http://localhost:5173
npm run build      # dist/ — статический, можно открыть с любого хостинга
npm run scaffold   # пересоздать недостающие файлы из старых interview-prep/*.md
```

Прогресс хранится в localStorage под ключом `prep-v2`.

## Деплой на Render (бесплатно, Static Site)

1. Запушить папку в GitHub (`git init && git add . && git commit -m init`, создать репо, `git push`).
2. На render.com: **New → Blueprint** → выбрать репозиторий → Render подхватит `render.yaml`.
   Либо вручную: **New → Static Site**, Build Command `npm ci && npm run build`, Publish Directory `dist`.
3. Готово: `https://interview-prep-xxxx.onrender.com`. Каждый push в main пересобирает сайт.

Прогресс (галочки) хранится в `localStorage` браузера — на сервере ничего не нужно.
Если открываешь с нескольких устройств, прогресс не синхронизируется: это ограничение localStorage, а не хостинга.
