G = "10-grammatika-tolko-to-chto-realno-nuzhno-na-sobese/"
EG = "https://www.englishpage.com/verbpage/"
CAM = "https://dictionary.cambridge.org/grammar/british-grammar/"
def g(name, links, body):
    return (G + name, (links, body))

ITEMS = dict([
g("01-past-simple-dlya-zakonchennogo-opyta-i-worked-at.md", [("englishpage — Simple Past", EG + "simplepast.html")], """
**Правило**: действие закончено, время известно или подразумевается (прошлая работа, конкретный проект, баг, который починил). Форма: V2 / V-ed; вопрос и отрицание через **did** + V1.

- *I worked at Sovtech for a year.* — уже не работаю.
- *I migrated the frontend from React to Vue 3.*
- *We found the bug in the callback and moved the enqueue after commit.*
- *Did you use Sidekiq there? — No, we didn't; we used Laravel queues.*

**Всё о прошлых местах работы — Past Simple.** Это 70% твоего рассказа о себе.

Типичная ошибка: *I have worked at Sovtech in 2025* → `in 2025` = конкретное время → **I worked**.

Неправильные глаголы, которые точно понадобятся: *build–built, write–wrote, find–found, take–took, make–made, lead–led, leave–left, spend–spent, break–broke, run–ran, set up–set up, deal with–dealt with.*
"""),
g("02-present-perfect-dlya-opyta-voobsche-i-rezultata-.md", [("englishpage — Present Perfect", EG + "presentperfect.html")], """
**Правило**: опыт «в жизни вообще» без указания времени, или результат, важный сейчас. Форма: **have/has + V3**.

- *I've worked with PostgreSQL for three years.* — и сейчас работаю (for/since → продолжается).
- *I've used Docker on every project since 2023.*
- *I've just finished the test task.* — результат: вот он.
- *Have you ever worked with Ruby commercially? — Not yet, but I've built two projects in it.*

Маркеры: *ever, never, just, already, yet, so far, for, since, recently.*

Типичная ошибка: ставить Present Perfect с конкретным временем: *I've migrated the app last year* → **I migrated**. Ещё одна: *I have worked there for a year* про место, откуда ушёл → **I worked there for a year**.

Полезное: *«I haven't used it in production, but I've read the docs»* — честная формула для незнакомых технологий.
"""),
g("03-raznica-i-worked-there-uzhe-ushel-vs-i-ve-worked.md", [("Cambridge — Present perfect simple or past simple?", CAM + "present-perfect-simple-or-past-simple")], """
Одна разница, которая слышна интервьюеру сразу:

| | значение | пример |
|---|---|---|
| **I worked there for a year** | период закончен, ты ушёл | *I worked at Victorum for six months.* |
| **I've worked there since June** | начал в июне и **всё ещё там** | *I've worked as a freelancer since March.* |
| **I've been working on it for two weeks** | процесс продолжается, акцент на длительности | *I've been working on the test task for two weeks.* |

Про все три прошлых места — **worked**. Про текущее состояние (ищу работу, учу Ruby) — Present Perfect / Continuous:
- *I've been learning Ruby seriously for about six months.*
- *I've been looking for a Ruby position since I left Sovtech.*

Типичная ошибка русскоговорящих: *I work there for a year* (Present Simple с длительностью) — так не говорят; либо *worked*, либо *have worked*.

Тест для себя: можно добавить «и до сих пор»? → Perfect. Нельзя → Past Simple.
"""),
g("04-present-simple-dlya-faktov-i-kak-rabotaet-kod-th.md", [("englishpage — Simple Present", EG + "simplepresent.html")], """
**Правило**: факты, регулярные действия и — главное для тебя — **как работает код/система**. Объяснение любой архитектуры идёт в Present Simple.

- *The wallet fetches UTXOs from the API and sums their values.*
- *The worker retries on failure with exponential backoff.*
- *Sidekiq stores jobs in Redis.*
- *Each input references a previous output.*

Не забывать **-s** в 3-м лице: *the method return**s***, *it raise**s** an error*, *the job run**s***. Это самая частая слышимая ошибка.

Вопрос — через **does**: *How does the fee get calculated? What does the callback do?*

Типичная ошибка: описывать систему в Present Continuous (*the worker is retrying*) — это означает «прямо сейчас, в данный момент», а не «так устроено».

Про себя: *I work mostly on the backend. I prefer explicit code. I write tests first when the logic is tricky.*
"""),
g("05-present-continuous-dlya-sejchas-v-processe-i-m-c.md", [("englishpage — Present Continuous", EG + "presentcontinuous.html")], """
**Правило**: действие в процессе сейчас или в этот период жизни; временное состояние. Форма: **am/is/are + V-ing**.

- *I'm currently learning dry-rb.*
- *I'm looking for a Ruby position.*
- *I'm working on the exchange demo this week.*
- *The team is migrating to Rails 8.* — процесс идёт.

Также — ближайшие планы с датой: *I'm meeting the team on Friday.*

Не употреблять с глаголами состояния: *know, understand, like, want, prefer, believe, need* → *I'm understanding* ✗ → **I understand**.

Типичная ошибка: *I'm working at Sovtech* про прошлое место → **I worked**. Про текущее: *I'm not working anywhere right now — I'm preparing for interviews and building projects.*
"""),
g("06-past-continuous-dlya-fona-v-istorii-pro-bag-whil.md", [("englishpage — Past Continuous", EG + "pastcontinuous.html")], """
**Правило**: длительный фон в прошлом, на котором произошло короткое событие. Форма: **was/were + V-ing**. Идеально для STAR-истории.

- *While I **was debugging** the notifications module, I **noticed** that the job ran before the commit.*
- *We **were migrating** the frontend when the API contract **changed**.*
- *I **was looking** at the logs and **saw** that all duplicates came within the same second.*

Схема: **was doing** (фон) + **did** (событие). Связки: *while, when, as*.

Типичная ошибка: оба глагола в Continuous (*while I was debugging I was noticing*) — событие должно быть в Past Simple.

Не нужен для последовательности действий: *I checked the logs, found the pattern, and fixed the callback* — всё Past Simple.
"""),
g("07-used-to-dlya-proshlyh-privychek-i-used-to-write-.md", [("Cambridge — used to", CAM + "used-to")], """
**Правило**: регулярно делал в прошлом, сейчас — нет. Форма: **used to + V1** (одинаково для всех лиц).

- *I used to write PHP every day; now I prefer Ruby.*
- *We used to deploy manually, then we set up CI.*
- *I used to put all the logic in controllers — Laravel taught me not to.*

Отрицание и вопрос: *didn't use to*, *Did you use to…?* (без -d).

Не путать:
- **be used to + V-ing** — привык к чему-то: *I'm used to working remotely.*
- **get used to** — привыкать: *It took me a week to get used to Ruby blocks.*

Хорошо звучит в «why Ruby»: *I used to think PHP was enough. Then I took a Rails course and saw how much shorter the same code could be.*
"""),
g("08-buduschee-will-dlya-reshenij-na-hodu-i-ll-check-.md", [("englishpage — Simple Future", EG + "simplefuture.html")], """
Два будущих, разный смысл:

**will** — решение в момент речи, обещание, предсказание:
- *I'll check that and get back to you.*
- *I'll send the repository link tonight.*
- *That will probably cause a race condition.*

**going to** — план, намерение, уже решено:
- *I'm going to add a fee estimator next.*
- *I'm going to focus on Ruby for the next few years.*

**Present Continuous** — договорённость с датой: *I'm starting on Monday.*

Типичные ошибки:
- *I will* в придаточных времени/условия: *when I **will** finish* ✗ → *when I **finish***; *if it **will** fail* ✗ → *if it **fails***.
- Русская калька «я буду делать» → *I will be doing*: не надо, просто *I'll do*.

На собесе чаще всего нужно: *I'll…* как реакция («сделаю») и *I'm going to…* в ответ на «what's next».
"""),
g("09-first-conditional-realnoe-buduschee-if-the-balan.md", [("englishpage — Conditionals", "https://www.englishpage.com/conditional/conditionalintro.html")], """
**Правило**: реальная ситуация с вероятным следствием. **If + Present Simple, will / Present Simple / imperative.**

- *If the balance is insufficient, the method raises an error.* — описание кода (Present + Present = zero conditional, «всегда так»).
- *If the API is down, we'll retry three times.*
- *If the change is below dust, it goes to the fee.*
- *If you give me a minute, I'll check the docs.*

Главное: **в if-части НЕТ will**. *If the balance **will be** insufficient* ✗.

Варианты союза: *unless* (= if not): *Unless the transaction confirms, the funds stay in the UTXO.* *as long as, provided that, in case.*

Для описания системы — zero conditional (оба Present): «всякий раз когда». Для планов и «что будет» — first (will).
"""),
g("10-second-conditional-gipoteza-dlya-voprosov-chto-b.md", [("englishpage — Conditionals", "https://www.englishpage.com/conditional/conditionalintro.html")], """
**Правило**: гипотеза, нереальное/маловероятное сейчас, вежливый ответ на «что бы вы сделали». **If + Past Simple, would + V1.**

- *If I had more time, I would add a fee estimator.*
- *If this were production, I'd use my own node instead of a public API.*
- *If two requests came in at the same time, they would try to spend the same UTXO — so I'd add a lock.*
- *What would you do if the job failed halfway? — I'd make it idempotent and let it retry.*

Это **самая нужная форма на техсобесе** — все вопросы «how would you…» требуют ответа через *I would / I'd*.

Детали: *were* для всех лиц в формальной речи (*if I were you*), но *was* тоже ок. Сокращение *I'd* = *I would* (в этой конструкции).

Типичная ошибка: *If I would have more time* ✗ — would не ставится в if-часть.
"""),
g("11-third-conditional-redko-odna-forma-if-we-had-use.md", [("englishpage — Conditionals", "https://www.englishpage.com/conditional/conditionalintro.html")], """
**Правило**: нереальное прошлое — «если бы тогда сделали иначе». **If + Past Perfect (had + V3), would have + V3.** Нужна одна форма — для вывода из истории про баг.

- *If we had used a unique index, the duplicates wouldn't have happened.*
- *If I had checked the logs earlier, I would have found it in an hour instead of a day.*
- *If we hadn't enqueued the job inside the transaction, there would have been no race.*

Произносится с редукциями: *If we'd used… it wouldn't've happened.*

Когда применять: один раз в STAR-истории, в части «Learning». Больше — звучит как сожаление.

Не путать с second: *If I had more time* (сейчас, гипотеза) vs *If I had had more time* (тогда, прошлое).
"""),
g("12-should-rekomendaciya-we-should-enqueue-the-job-a.md", [("Cambridge — should", CAM + "should")], """
**should + V1** — рекомендация, «правильно было бы». Мягче, чем *must*, профессиональнее, чем *need to*.

- *We should enqueue the job after commit, not inside the transaction.*
- *Jobs should be idempotent.*
- *You should probably add an index on that column.*
- *The fee shouldn't be a constant — it should come from config.*

Прошлое (критика задним числом): **should have + V3** — *We should have used a unique constraint from the start.*

В code review: *«I think this should be extracted into a service»* — стандартная формула. *Might want to* — ещё мягче: *You might want to memoize this.*

Типичная ошибка: *should to do* ✗; *should be do* ✗ → *should do / should be done*.
"""),
g("13-might-could-neuverennost-it-might-be-a-race-cond.md", [("Cambridge — may, might, could", CAM + "modality-forms")], """
Говорить о гипотезе, не утверждая — ключевой навык при дебаге вслух.

- *It might be a race condition.* — возможно.
- *This could cause a double spend if two workers pick the same UTXO.*
- *The slowness may be due to N+1.*
- *It could also be the index not being used — I'd check EXPLAIN.*

Градация уверенности: *must be* (почти уверен) → *should be / probably* → *might / may / could* (возможно) → *can't be* (исключено).

Прошлое: **might have + V3** — *The job might have run before the commit.*

Полезная формула: *«It might be X, but I'd need to check Y to be sure.»* — показывает мышление, а не гадание.

Типичная ошибка: *can be* в значении «возможно» (*it can be a race condition*) — для конкретного случая лучше *could/might*; *can* — про общую способность.
"""),
g("14-must-have-to-obyazatelnost-arguments-must-be-jso.md", [("Cambridge — must / have to", CAM + "have-to-and-must")], """
Обязательность и правила системы.

- **must** — правило, требование (формально, в документации): *Arguments must be JSON-serializable. The output must not be below dust.*
- **have to** — внешняя необходимость, разговорно: *I had to rewrite the module because the API changed. We have to wait for one confirmation.*
- **need to** — нейтрально: *You need to sign each input separately.*

Отрицания — **разный смысл**:
- *must not* = запрещено: *You must not log the private key.*
- *don't have to* = не обязательно: *You don't have to run your own node for Signet.*

Прошлое: только **had to** (*must* в прошлом нет). *We had to add a lock.*

Типичная ошибка: *must to* ✗; *I must did* ✗.
"""),
g("15-would-dlya-vezhlivosti-i-would-say-i-d-approach-.md", [("Cambridge — would", CAM + "would")], """
**would** смягчает утверждение — звучит обдуманно, а не категорично. На собесе это основной регистр.

- *I would say the main challenge was concurrency.*
- *I'd approach it this way: first…, then…*
- *I'd argue that a service object is cleaner here.*
- *I wouldn't put that logic in a callback.*
- *Would you mind if I think out loud?*

Сравни: *The main challenge was X* (утверждение) vs *I'd say the main challenge was X* (мнение, открытое к обсуждению).

Также — привычное действие в прошлом: *At Sovtech we would deploy every Friday.* (= used to).

Формула для «как бы ты решил»: **I'd start by … Then I'd … Finally I'd …**

Типичная ошибка: *I would like to say* перед каждой фразой — один раз нормально, постоянно — тяжеловесно. Чаще — просто *I'd say*.
"""),
g("16-passiv-dlya-opisaniya-sistemy-the-transaction-is.md", [("Cambridge — Passive", CAM + "passive-voice")], """
**be + V3**. Когда важно *что происходит*, а не *кто делает* — описание пайплайна, формата, правил.

- *The transaction is signed and broadcast.*
- *The fee is calculated as inputs minus outputs.*
- *Jobs are stored in Redis and picked up by workers.*
- *The key is never written to logs.*
- *Each block is linked to the previous one by its hash.*

Прошлое: *The bug was introduced in a refactor. The module was rewritten in Vue 3.*
Модальные: *must be verified, can be replaced, should be extracted.*

Не злоупотреблять про себя: *The migration was done by me* ✗ → **I did the migration**. Своё — активом, систему — пассивом.

Типичная ошибка: пропускать **be**: *the transaction signed* ✗ (это звучит как «транзакция подписала») → *is signed*.
"""),
g("17-otnositelnye-pridatochnye-the-output-that-hasn-t.md", [("Cambridge — Relative clauses", CAM + "relative-clauses")], """
Нужны для определений: «X — это Y, который…».

- *A UTXO is an output **that** hasn't been spent yet.*
- *The key **which** controls the funds never leaves the machine.*
- *The worker **that** picks up the job checks the status first.*
- *The person **who** reviewed my code suggested a service object.*
- *The place **where** the race happened was the callback.*

**that / which** — для предметов (в разговоре *that* чаще), **who** — для людей, **whose** — чей, **where** — где.

Можно опускать, если местоимение — дополнение: *the bug (that) I found*, *the approach (which) I chose*.

Типичные ошибки: *the key what controls* ✗; *the output which it hasn't been spent* ✗ (лишнее it).

Формула определения на собесе: **«X is a Y that Z»** — *«Escrow is a multisig output that needs two of three signatures.»*
"""),
g("18-gerundij-posle-predlogov-responsible-for-buildin.md", [("Cambridge — Verb patterns", CAM + "verb-patterns-verb-ing-or-infinitive")], """
После **предлога — всегда -ing**. Это звучит в каждом рассказе о себе.

- *responsible **for** building the notifications module*
- *experience **in** developing REST APIs*
- *instead **of** using a callback, I moved it to a service*
- *interested **in** working on payment systems*
- *good **at** debugging*
- *before/after **deploying**, we run smoke tests*
- *thanks to / by / without + -ing: by adding an index, without breaking the API*

Отдельно: **look forward to + -ing** (*to* тут предлог): *I'm looking forward to hearing from you.*

Также -ing после: *enjoy, avoid, consider, suggest, keep, finish, mind*: *I enjoy writing Ruby. I'd suggest extracting a class. Avoid putting logic in callbacks.*

Типичная ошибка: *responsible for build* ✗, *experience in develop* ✗, *instead of to use* ✗.
"""),
g("19-infinitiv-celi-i-added-a-lock-to-prevent-double-.md", [("Cambridge — to + infinitive of purpose", CAM + "infinitive-to-or-without-to")], """
Объяснить **зачем** — через *to + V1*. Каждое решение в тестовом объясняется этой формой.

- *I added a lock **to prevent** double spending.*
- *I moved the enqueue after commit **to avoid** the race.*
- *We used WebMock **to keep** tests offline.*
- *I chose bitcoinrb **to get** native Signet support.*

Формальнее: *in order to*, отрицание: *so as not to / in order not to*: *I kept amounts as integers in order not to lose precision.*

Альтернатива — *so that + clause*: *I made the job idempotent **so that** retries are safe.*

Глаголы с инфинитивом: *decide, want, plan, need, try, manage, expect, hope*: *I decided to use a service object. I managed to reproduce it.*

Типичная ошибка: *for to prevent* ✗, *for prevent* ✗, *for preventing* (допустимо только про назначение предмета: *a tool for testing*).
"""),
g("20-sravneniya-faster-than-the-same-as-as-simple-as-.md", [("Cambridge — Comparison", CAM + "comparison-adjectives-bigger-biggest-more-interesting")], """
Сравнивать решения — половина технических ответов.

- *Ruby is more expressive **than** PHP.*
- *P2WPKH inputs are about half **as** large **as** P2PKH ones.*
- *It's **the same as** before, just in a service object.*
- *This is **as simple as** it gets.*
- *Sidekiq is **much** faster **than** DelayedJob because it's in-memory.*
- *The second approach is **slightly / far / a lot** more reliable.*
- *The less logic in callbacks, the easier it is to test.*

Формы: короткие прилагательные **-er / -est** (*faster, simpler*), длинные — **more / most** (*more reliable*). Неправильные: *good–better–best, bad–worse–worst, far–further.*

Типичные ошибки: *more faster* ✗, *than* ↔ *then* (*faster then* ✗), *the same like* ✗ → **the same as**, *different than/from* (оба ок в US/UK).

Усилители: *much, far, a lot, significantly* + сравнительная; *slightly, a bit* — чуть.
"""),
g("21-artikli-minimum-a-pri-pervom-upominanii-the-kogd.md", [("Cambridge — Articles", CAM + "a-an-and-the")], """
Не добиться идеала — добиться отсутствия грубых ошибок.

**a / an** — один из многих, впервые упомянут, исчисляемое в ед.ч.: *I built **a** wallet. There was **a** race condition.*
**the** — конкретный, уже упомянутый или единственный: ***The** wallet stores **the** key in **a** file.* *the database, the API, the team* (понятно, какие).
**без артикля** — множественное в общем смысле и неисчисляемые: *jobs, tests, workers; money, code, experience, advice, information, software, feedback.*

Шпаргалка:
- *I have experience in Ruby* (не *an experience*)
- *I wrote code / tests* (не *a code*)
- *the first / the last / the same / the main*
- *at work, in production, on GitHub, in Ruby* — без артикля
- *a lot of, a few, a bit*

Типичные грубые: *I am developer* → **a** developer; *I worked in the Sovtech* → без *the* перед названиями; *the Ruby* ✗.

Если сомневаешься между *a* и *the* — выбери *the*: ошибка менее заметна.
"""),
g("22-poryadok-slov-v-voprosah-could-you-tell-me-how-t.md", [("Cambridge — Indirect questions", CAM + "questions-wh-questions")], """
Два типа вопросов — два порядка слов.

**Прямой** — инверсия (вспомогательный глагол перед подлежащим):
- *How does the team work? Where is the code deployed? Did you use Sidekiq?*

**Косвенный** (после *Could you tell me…, I wonder…, Do you know…*) — **прямой порядок**, без do/does:
- *Could you tell me how the team works?* (не *how does the team work*)
- *I'd like to know what the stack looks like.*
- *Can you explain why the job failed?*
- *I'm not sure if/whether it's thread-safe.*

Косвенный — вежливее; свои вопросы к ним задавай так.

Типичные ошибки русскоговорящих:
- *How it works?* ✗ → **How does it work?** (прямой нуждается в does)
- *Could you tell me how does it work?* ✗ → **how it works**
- *What means this?* ✗ → **What does this mean?**
- *You use Sidekiq?* — понятно, но лучше **Do you use Sidekiq?**
"""),
g("23-i-am-agree-i-agree.md", [], """
*agree* — **глагол**, не прилагательное. Не нужен *am/is/are*.

- ✗ *I am agree with you.*
- ✓ **I agree** with you. / **I agree that** we need a lock.
- ✓ *I don't agree* / *I disagree* (мягче: *I'm not sure I agree.*)
- ✓ *I totally / partly agree.*
- Вопрос: *Do you agree?* (не *Are you agree?*)

Прошлое: *We agreed to extract a service.* / *agreed on the approach.*

Та же ошибка с другими глаголами: *I am understand* ✗ → *I understand*; *I am think* ✗ → *I think*.

Если нужно именно прилагательное: *I'm fine with that. I'm on board. That works for me.*
"""),
g("24-depends-from-depends-on.md", [], """
Калька с «зависит от». В английском — **depend on**.

- ✗ *It depends from the load.*
- ✓ **It depends on** the load.
- ✓ *It depends on how many UTXOs the address has.*
- ✓ *That depends.* — коротко, с паузой, потом объяснить.

Та же логика в однокоренных: *dependent on, dependency on*.

Соседние предлоги, где тоже ошибаются:
- *rely on* (не *rely to*)
- *consist of* (не *consist from*)
- *responsible for* (не *responsible of*)
- *interested in* (не *interested on*)
- *wait for* (не *wait*): *I waited for one confirmation.*
- *listen to, explain to, belong to.*

Формула на собесе: **«It depends on X. If X, I'd …; otherwise …»** — показывает, что ты видишь условия.
"""),
g("25-advices-informations-knowledges-advice-informati.md", [("Cambridge — Nouns: countable and uncountable", CAM + "nouns-countable-and-uncountable")], """
Эти существительные **не имеют множественного** и не берут *a/an*:

*advice, information, knowledge, experience* (как опыт вообще), *feedback, software, hardware, code, money, work, research, progress, equipment, news, documentation, evidence.*

- ✗ *He gave me some advices.* → ✓ *some advice / a piece of advice*
- ✗ *I have an experience with Rails.* → ✓ *I have experience with Rails* (но: *it was a good experience* — конкретный случай, можно)
- ✗ *many informations* → ✓ *a lot of information*
- ✗ *a code* → ✓ *code / a piece of code / a snippet*
- ✗ *a work* (работа как место) → ✓ *a job*; *work* — деятельность
- ✗ *researches* → ✓ *research / studies*
- ✗ *knowledges* → ✓ *knowledge*
- ✗ *feedbacks* → ✓ *feedback / comments*

Глагол в ед.ч.: *The documentation **is** good. The news **is** out.*

Количество: *much / little / a lot of / some / a bit of* — не *many / few / a*.
"""),
g("26-in-the-last-year-last-year-on-the-project-in-on-.md", [], """
Время:
- **last year / last week / last month** — без *in*, без *the*: *I left Sovtech last year.* (= в прошлом году)
- **in the last year** = за последние 12 месяцев до сейчас (Present Perfect): *In the last year I've shifted to Ruby.*
- **this year, next week, yesterday, two years ago** — без предлога.
- *in 2025, in June, on Monday, at 10 am, for a year, since June.*

Проекты:
- ***on** a project* — работать над: *I worked on a CRM project.*
- ***in** a project* — быть частью: *I was involved in the migration project.* (оба встречаются)
- ***at** a company*: *at Sovtech*, не *in Sovtech*.
- ***in** a team*: *in a team of three.*

Другое:
- *at work, in production, on the backend/frontend, in Ruby, on GitHub, in the database, on the server.*

Типичное: *in the last job* → **at my last job / in my last role**.
"""),
g("27-i-have-27-years-i-m-27.md", [], """
Возраст, состояние, ощущения — через **be**, не *have*.

- ✗ *I have 27 years.* → ✓ **I'm 27.** / *I'm 27 years old.*
- ✗ *I have hungry / cold / afraid.* → ✓ *I'm hungry / cold / afraid.*
- ✗ *I have right.* → ✓ *I'm right.*
- ✗ *I have luck.* → ✓ *I'm lucky.*

Но **have** там, где русский говорит иначе:
- *I have a question / a suggestion / a concern.*
- *have experience, have a look, have a call, have lunch.*

На собесе возраст не спрашивают; но *«how many years of experience»* → **I have three years of experience** / **I've been doing this for three years**.

Опыт: *I have three years of commercial experience in backend development, mostly PHP, now Ruby.*
"""),
g("28-explain-me-explain-to-me-explain-it.md", [], """
*explain* не берёт косвенное дополнение без *to*.

- ✗ *Can you explain me how it works?*
- ✓ *Can you **explain to me** how it works?*
- ✓ *Can you **explain** how it works?* (просто убрать «мне» — чаще всего так)
- ✓ *Let me **explain**.* / *Let me explain the flow.*
- ✓ *I'll explain it **to** the team.*

Та же группа глаголов — **to** перед человеком: *describe to, suggest to, say to, mention to, recommend to, introduce to, announce to.*
- ✗ *He suggested me to use a lock.* → ✓ *He suggested (that) I use a lock.* / *He suggested using a lock.*
- ✗ *Say me…* → ✓ *Tell me…* (**tell** — без *to*: *tell me, show me, give me, ask me*).

Запомнить пару: **tell me / explain to me**.
"""),
g("29-discuss-about-discuss.md", [], """
*discuss* — переходный глагол, объект идёт сразу.

- ✗ *Let's discuss about the architecture.*
- ✓ *Let's **discuss** the architecture.*
- ✓ *We discussed how to handle retries.*
- ✓ существительное — с about: *a discussion **about** the architecture*; *talk **about** / speak **about*** — тоже ок.

Та же ошибка — лишний предлог после:
- *answer the question* (не *answer to*)
- *enter the room / the market* (не *enter in*)
- *contact me* (не *contact with*)
- *approach the problem* (не *approach to* — глагол), но *an approach to the problem* (сущ.)
- *attend a meeting* (не *attend to*)
- *reach the limit* (не *reach to*)
- *affect performance* (не *affect on*; но *have an effect on*)

Формулы: *«Could we discuss the salary range at the next stage?»*, *«Happy to discuss tradeoffs.»*
"""),
g("30-i-didn-t-went-i-didn-t-go.md", [], """
После **did / didn't** — **базовая форма** глагола. Прошедшее время уже выражено в *did*.

- ✗ *I didn't went to the standup.* → ✓ *I didn't **go**.*
- ✗ *Did you used Sidekiq?* → ✓ *Did you **use** Sidekiq?*
- ✗ *It didn't worked.* → ✓ *It didn't **work**.*
- ✗ *Why did it failed?* → ✓ *Why did it **fail**?*

Та же логика с модальными и **to**: *can go, should go, to go, must be* — всегда V1.
- ✗ *I could fixed it* → *I could fix it* / *I could have fixed it* (прошлое).
- ✗ *I want to went* → *I want to go*.

Контроль: услышал от себя *did/didn't/can/should/to* → следующий глагол без -ed/-s.

Отдельно: **-s** после *does*: ✗ *Does it works?* → ✓ *Does it work?*
"""),
g("31-how-it-works-how-does-it-work.md", [], """
Прямой вопрос требует вспомогательного глагола.

- ✗ *How it works?* → ✓ **How does it work?**
- ✗ *What this means?* → ✓ **What does this mean?**
- ✗ *Why you chose Ruby?* → ✓ **Why did you choose Ruby?**
- ✗ *Where you store the key?* → ✓ **Where do you store the key?**

Но без вспомогательного, когда вопросительное слово — **подлежащее**: *What happens if…? Who wrote this? Which job failed?*

И без вспомогательного в **косвенных**: *Could you explain how it works? I'm not sure what this means.*

С **be** — просто инверсия: *Is it thread-safe? Where is the config? What is the fee?*

Статья «How it works» в README — не вопрос, нормально. В речи: *Let me explain how it works.* (косвенный порядок) — ок.

Три вопроса для тренировки: *How does Sidekiq store jobs? Why does the fee depend on size? What does the callback do?*
"""),
g("32-actual-aktualnyj-current-relevant.md", [], """
**actual** = фактический, реальный (в противоположность предполагаемому). Не «актуальный».

- ✗ *the actual version of Rails* → ✓ **the current / latest version**
- ✗ *Is this task still actual?* → ✓ *Is this task still **relevant** / still **open**?*
- ✗ *actual information* → ✓ ***up-to-date** information*
- ✓ *The actual fee was lower than estimated.* — фактическая.
- ✓ *Actually, I've changed my mind.* — «на самом деле / вообще-то».

Другие ложные друзья:
- *accurate* = точный (не аккуратный → *neat, careful*)
- *eventually* = в конце концов (не «эвентуально»)
- *sympathetic* = сочувствующий (не симпатичный → *nice, likeable*)
- *magazine* = журнал (магазин → *shop, store*)
- *data* = данные (дата → *date*)
- *fabric* = ткань (фабрика → *factory*)
- *concrete* = конкретный ок, но чаще *specific*: *a specific example*.
"""),
g("33-control-proveryat-check-verify.md", [], """
**control** = управлять, контролировать (иметь власть). Не «проверять».

- ✗ *I control the input.* → ✓ *I **validate** / **check** the input.*
- ✗ *We control the tests before merge.* → ✓ *We **run** / **check** the tests.*
- ✓ *The platform controls one of the three keys.* — владеет/управляет.
- ✓ *version control, access control* — управление.

Градация «проверять»:
- **check** — посмотреть, убедиться (разговорно): *Let me check the logs.*
- **verify** — удостовериться формально: *The node verifies the signature.*
- **validate** — проверить на соответствие правилам: *validate the address format.*
- **test** — тестировать.
- **review** — просмотреть (код, документ).
- **make sure / ensure** — убедиться/обеспечить: *Make sure the job is idempotent.*

Фраза: *«I'd double-check that»* — перепроверил бы.
"""),
g("34-realize-realizovat-implement.md", [], """
**realize** = осознать, понять. Не «реализовать».

- ✗ *I realized the notifications module.* → ✓ *I **implemented** / **built** / **developed** the notifications module.*
- ✓ *I realized the job ran before the commit.* — понял.

Глаголы для «сделал фичу», по оттенку:
- **implement** — реализовать по спецификации
- **build / develop** — создать
- **design** — спроектировать
- **ship / deliver** — довести до пользователей
- **set up** — настроить (CI, Docker)
- **integrate** — подключить внешнее
- **introduce** — ввести практику (*introduced code review*)
- **rewrite / refactor / migrate** — переделать

Ещё кальки: *«реализация»* → **implementation**; *«проект»* (чертёж) → *design*, (работа) → *project*; *«функционал»* → **functionality / features** (не *functional*).

В CV: *Implemented, Built, Designed, Migrated, Introduced, Reduced, Set up* — глаголы-действия в начале пункта.
"""),
g("35-make-a-decision-ok-no-do-a-decision-net-do-resea.md", [("Cambridge — do or make?", CAM + "do-or-make")], """
Устойчивые пары — учить списком, логики мало.

**make** (создать результат): *make a decision, make a mistake, make sense, make progress, make a change, make an effort, make a suggestion, make money, make a call (решение/звонок), make it work.*

**do** (процесс, деятельность): *do research, do a code review, do the migration, do my best, do business, do a task, do testing, do homework.*

- ✗ *do a decision* → ✓ *make a decision*
- ✗ *make research* → ✓ *do research*
- ✗ *make a code review* → ✓ *do / review the code*
- ✗ *make a mistake* ✓ (это правильно!) / *do a mistake* ✗
- *It makes sense.* / *It doesn't make sense to me.* — фраза дня.

Другие коллокации, которые звучат на собесе: *take responsibility, take ownership, take a look, take time; pay attention; run tests, run a migration; raise an error, raise a concern; solve / fix a problem; meet a deadline; set a goal; reach an agreement; have a call / a meeting.*
"""),
])
