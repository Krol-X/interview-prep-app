B = "https://github.com/bitcoinbook/bitcoinbook/blob/develop/"
L = "https://learnmeabitcoin.com/technical/"
M = "https://mempool.space/signet/docs/api/rest"
BIP = "https://github.com/bitcoin/bips/blob/master/"
ITEMS = {
# ───────── Bitcoin ─────────
"06-bitcoin/01-klyuch-publichnyj-klyuch-adres.md": ([
  ("Mastering Bitcoin, гл. 4 — Keys and Addresses", B + "ch04_keys.adoc"),
  ("learnmeabitcoin — Private key / Public key / Address", L + "keys/"),
  ("bitcoinrb — README", "https://github.com/chaintope/bitcoinrb"),
], """
```
приватный ключ  ──(умножение на кривой secp256k1)──▶  публичный ключ  ──(hash160 / bech32)──▶  адрес
   256 бит случайности          односторонне            33 байта (сжатый)                      tb1q...
```

- **Приватный ключ** — случайное число 1..n (~2²⁵⁶). Никуда не отправляется. Форматы: hex, **WIF** (base58 с префиксом сети и checksum — так его хранят кошельки и так сохранишь ты).
- **Публичный ключ** — точка на кривой `priv × G`. Обратно не вычислить (ECDLP). Из него проверяют подписи.
- **Адрес** — не ключ, а **инструкция получателю, какое условие траты записать в выход**. P2WPKH: `bech32(hrp, 0, hash160(pubkey))`. Префикс `tb1q` — Signet/testnet, `bc1q` — mainnet. Checksum внутри ловит опечатки.
- Один приватный ключ → разные адреса в разных сетях (hrp/префикс другой) и разные типы (P2PKH `m...`, P2WPKH `tb1q...`, P2TR `tb1p...`).
- HD-кошельки (BIP32/39/44): seed-фраза 12 слов → мастер-ключ → дерево ключей по пути `m/84'/1'/0'/0/0`. Для тестового один ключ достаточно.

```ruby
Bitcoin.chain_params = :signet
key = Bitcoin::Key.generate            # SecureRandom внутри
key.to_wif                             # сохранить в файл
key.to_p2wpkh                          # tb1q...
Bitcoin::Key.from_wif(File.read(path)) # восстановить
```

Генерировать **только** CSPRNG (`SecureRandom`): все реальные взломы — слабая энтропия, не перебор 2²⁵⁶.

## Фраза для собеса

«Приватный — случайное число, публичный — точка на кривой, адрес — хеш публичного ключа в bech32 с префиксом сети; из адреса сеть понимает условие траты».
"""),

"06-bitcoin/03-p2pkh-p2sh-p2wpkh-p2wsh-p2tr-odnoj-frazoj-kazhdy.md": ([
  ("learnmeabitcoin — Script / locking scripts", L + "script/"),
  ("Mastering Bitcoin, гл. 7 — Authorization and Authentication", B + "ch07_authorization-authentication.adoc"),
], """
Каждый выход = сумма + **условие траты** (locking script). Типы — это шаблоны условия.

| Тип | Условие | Mainnet | Signet | С какого года |
|---|---|---|---|---|
| **P2PKH** | покажи pubkey с таким hash160 + ECDSA-подпись | `1...` | `m.../n...` | 2009 |
| **P2SH** | покажи скрипт с таким hash160 и данные, на которых он даст true | `3...` | `2...` | 2012 (BIP16) |
| **P2WPKH** | то же, что P2PKH, но данные в witness | `bc1q...` (42 симв.) | `tb1q...` | 2017 (BIP141) |
| **P2WSH** | то же, что P2SH, но в witness; hash sha256 | `bc1q...` (62 симв.) | `tb1q...` | 2017 |
| **P2TR** | Schnorr-подпись ключом (key path) или скрипт из дерева (script path) | `bc1p...` | `tb1p...` | 2021 (BIP341) |
| P2SH-P2WPKH | SegWit, завёрнутый в P2SH для совместимости | `3...` | `2...` | переходный |

- Тип входа (что тратишь) и тип выхода (куда шлёшь) независимы: тратишь свой P2WPKH, платишь на P2TR — нормально.
- Подписываешь по правилам **тратимого** UTXO; создаёшь выход по правилам **адреса получателя** — библиотека сделает по префиксу.
- Размер и комиссия: P2PKH вход ~148 vB, P2WPKH ~68, P2TR ~58.
- В тестовом задании 2 валидировать «P2PKH, P2SH, P2WPKH» для signet: префиксы `m/n`, `2`, `tb1q`. `tb1p` — решить явно.

## Фраза для собеса

«PKH — ключ, SH — скрипт, W — то же в witness, TR — Taproot с ключом или деревом скриптов; префикс адреса говорит, какой шаблон условия записать в выход».
"""),

"06-bitcoin/04-segwit-witness-weight-vbytes-txid-vs-wtxid.md": ([
  ("BIP141 — Segregated Witness", BIP + "bip-0141.mediawiki"),
  ("learnmeabitcoin — SegWit / weight", L + "transaction/size/"),
], """
SegWit (2017, soft fork) **вынес данные подписи** из тела транзакции в отдельную структуру — witness.

Что это дало:
1. **Transaction malleability исправлена.** Раньше подпись входила в txid; её можно было слегка изменить (DER-кодирование), не ломая валидность, — txid менялся, и цепочки неподтверждённых транзакций (Lightning) ломались. Теперь:
   - `txid` = hash(транзакция **без** witness) — стабилен;
   - `wtxid` = hash(с witness) — используется в блоке для коммитмента witness-данных.
2. **Больше места в блоке через «вес»**: лимит не 1 МБ размера, а **4 000 000 weight units**.
   ```
   weight = 4 × (байты без witness) + 1 × (байты witness)
   vbytes = weight / 4
   ```
   Witness-байты в 4 раза дешевле → SegWit-транзакции платят меньше при той же логике (P2WPKH вход ~68 vB против ~148 у P2PKH). Эффективный размер блока — до ~4 МБ, типично ~1.5–2.
3. Версионирование witness-программ — путь к Taproot (v1) без нового форка формата.

Для тебя: комиссия считается в **sat/vB**; размер транзакции — `tx.vsize`; адреса `tb1q` — SegWit v0; старые узлы видят SegWit-выходы как «anyone can spend», но не майнят невалидные — поэтому это soft fork.

## Фраза для собеса

«SegWit перенёс подписи в witness: txid перестал зависеть от подписи, witness-байты весят ¼, отсюда vbytes и дешевле комиссии».
"""),

"06-bitcoin/05-taproot-schnorr-key-path-script-path-mast-contro.md": ([
  ("BIP340 — Schnorr Signatures", BIP + "bip-0340.mediawiki"),
  ("BIP341 — Taproot", BIP + "bip-0341.mediawiki"),
  ("learnmeabitcoin — Taproot", L + "upgrades/taproot/"),
], """
Taproot (ноябрь 2021, soft fork) = SegWit v1 выход `bc1p…`/`tb1p…`. Три идеи:

**1. Schnorr вместо ECDSA** (BIP340). Подпись 64 байта, линейна: ключи и подписи можно **складывать**. N участников → один агрегированный ключ и одна подпись (MuSig2). Снаружи multisig неотличим от обычного платежа.

**2. Один ключ снаружи, дерево скриптов внутри** (BIP341):
```
output_key = internal_key + hash(internal_key ‖ merkle_root) · G
```
- **Key path**: подпись Schnorr от `output_key` — «счастливый» сценарий, все согласны. Дёшево (~58 vB вход), приватно.
- **Script path**: раскрыть один лист дерева + **control block** (internal key + merkle-путь из хешей соседних веток). Узел пересчитывает корень, проверяет tweak, исполняет скрипт.

**3. MAST** — дерево альтернативных условий; при трате раскрывается только использованная ветка, остальные остаются хешами навсегда.

Escrow Hodl Hodl на Taproot выглядел бы так: internal key = агрегат(покупатель+продавец) для нормальной сделки; ветки A (покупатель+платформа) и B (продавец+платформа) на спор. Блокчейн увидит escrow только при споре, и только одну ветку.

Для тестового: bitcoinrb умеет `to_p2tr`; отправить на `tb1p` — просто другой выход. Подписывать P2TR-вход — Schnorr (`sign_tx` с `sig_version: :taproot`), если решишь использовать.

## Фраза для собеса

«Taproot: Schnorr-подписи складываются, выход — один ключ с подмешанным корнем дерева скриптов; тратится либо ключом, либо раскрытием одной ветки».
"""),

"06-bitcoin/06-multisig-2-of-3-escrow-hodl-hodl-narisovat-tabli.md": ([
  ("Hodl Hodl — FAQ: How does escrow work", "https://hodlhodl.com/pages/faq"),
  ("learnmeabitcoin — P2SH / multisig", L + "script/p2sh/"),
  ("BIP11 — M-of-N Standard Transactions", BIP + "bip-0011.mediawiki"),
], """
Multisig m-of-n: выход тратится, если предъявлено **m подписей из n заранее указанных ключей**.

```
redeem script:  2 <pk_buyer> <pk_seller> <pk_platform> 3 OP_CHECKMULTISIG
P2SH-адрес:     base58(hash160(redeem_script))  → 3... / signet 2...
при трате:      <sig_a> <sig_b> <redeem_script>   (+ OP_0 из-за бага CHECKMULTISIG)
```

Hodl Hodl: **некастодиальный** P2P-обмен. Продавец кладёт BTC в escrow — 2-of-3 с ключами покупателя, продавца и платформы. Платформа одна не может ничего, покупатель и продавец вместе — всё.

| Ситуация | Подписывают | Платформа нужна? |
|---|---|---|
| Сделка прошла нормально | продавец + покупатель | нет |
| Спор, прав покупатель | покупатель + платформа | да, арбитр |
| Спор, прав продавец | продавец + платформа | да |
| Платформа взломана/злонамеренна | 1 подпись из 2 нужных | не может украсть |
| Платформа исчезла | продавец + покупатель | не блокирует средства |

Почему это важно продукту: отсутствие кастодии = нет лицензионной нагрузки хранения чужих средств и нет single point of failure; арбитраж возможен без доступа к деньгам.

Варианты: P2SH (исторически), P2WSH (`tb1q` длинный, дешевле), Taproot с MuSig (ещё дешевле и приватнее — key path для согласия, ветки для спора). Ключи сторон генерируются на клиенте; платформа хранит только свой.

Уметь нарисовать на салфетке: три ключа → один адрес → две стрелки подписей → выход покупателю.

## Фраза для собеса

«Escrow — P2SH 2-of-3: ключи у покупателя, продавца и платформы; любые две подписи выпускают монеты, поэтому платформа — арбитр, а не хранитель».
"""),

"06-bitcoin/07-komissii-sat-vb-mempool-rbf-cpfp-pyl-minrelayfee.md": ([
  ("mempool.space Signet — fees/recommended", M + "#get-recommended-fees"),
  ("BIP125 — Replace-by-Fee", BIP + "bip-0125.mediawiki"),
  ("Bitcoin Optech — Fee bumping (RBF/CPFP)", "https://bitcoinops.org/en/topics/fee-bumping/"),
], """
- **Комиссия = Σвходов − Σвыходов.** Не поле, а остаток; забыл сдачу — всё майнеру.
- Платишь за **место в блоке**, не за сумму: `fee = vbytes × rate`, единица — **sat/vB**. Блок ограничен 4M weight units.
- **Mempool** — очередь неподтверждённых; майнер берёт сверху по sat/vB. Ставка — рыночная: пусто → 1 sat/vB, пик → сотни.
- **minrelayfee** 1 sat/vB — узлы не ретранслируют дешевле (это *policy*, не консенсус — 0-fee транзакция валидна, но не дойдёт до майнера).
- **Пыль (dust)** — выход, который дороже потратить, чем он стоит: ~546 sat P2PKH, ~294 sat P2WPKH. Такую сдачу не создавай — оставь в комиссии.
- **RBF** (BIP125) — заменить застрявшую транзакцию той же с большей комиссией (входы те же, fee выше хотя бы на minrelay × size). Нужен `sequence < 0xfffffffe`; с Core 28 full-RBF по умолчанию.
- **CPFP** — потратить выход застрявшей новой транзакцией с большой комиссией; майнер возьмёт обе как пакет. Работает, когда ты получатель.
- Застрявшая транзакция выбрасывается из mempool через ~2 недели (по умолчанию), UTXO снова свободны.

Размеры для оценки (1 вход, 2 выхода): P2WPKH ≈ **141 vB**, P2TR ≈ 111, P2PKH ≈ 226. Каждый доп. P2WPKH-вход +68, выход +31.

```
GET https://mempool.space/signet/api/v1/fees/recommended
{"fastestFee":1,"halfHourFee":1,"hourFee":1,"economyFee":1,"minimumFee":1}
```
Signet почти всегда 1 sat/vB. Бонус в тестовом: `fee = max(vsize × fastestFee, vsize × 1)`; размер — `tx.vsize` после сборки с фиктивной подписью или оценка по числу входов/выходов.

## Фраза для собеса

«Комиссия — остаток входов над выходами, рынок за vbytes; застряла — RBF или CPFP; сдачу меньше пыли не делаю».
"""),

"06-bitcoin/08-coinbase-tranzakciya-subsidiya-halving-21-mln.md": ([
  ("learnmeabitcoin — Coinbase transaction", L + "transaction/coinbase/"),
  ("Mastering Bitcoin, гл. 12 — Mining", B + "ch12_mining.adoc"),
], """
Первая транзакция каждого блока — **coinbase**: у неё нет входов, она создаёт новые монеты «из ничего» — единственное место в системе, где это разрешено. Майнер выписывает её сам себе.

```
выход coinbase ≤ субсидия(высота) + Σ комиссий всех транзакций блока
```
Больше — все узлы отвергнут блок, работа пропала. Выход coinbase нельзя тратить **100 блоков** (на случай reorg).

**Субсидия** — геометрическая прогрессия, зафиксирована в коде:

| Период | Субсидия | Событие |
|---|---|---|
| 2009 | 50 BTC | genesis |
| 2012 / 2016 / 2020 | 25 / 12.5 / 6.25 | халвинги каждые 210 000 блоков (~4 года) |
| апрель 2024 → ~2028 | **3.125 BTC** | текущая |
| ~2140 | 0 | последний сатоши; всего ≤ 21 000 000 BTC |

- Сумма ряда 50·210000·(1 + ½ + ¼ + …) = 21 млн. Не «кто-то решил», а арифметика.
- Доход майнера = субсидия + комиссии. Сейчас комиссии ~1–5% дохода; к 2140 останутся только они — открытый вопрос, хватит ли на безопасность (security budget).
- Поле `coinbase` (scriptSig) — произвольные байты: высота блока (BIP34), метки пулов, «Chancellor on brink of second bailout» в genesis.
- В Signet coinbase такая же, но монеты тестовые.

## Фраза для собеса

«Coinbase — транзакция без входов, которой майнер забирает субсидию плюс комиссии; субсидия делится пополам каждые 210 тыс. блоков, сумма сходится к 21 млн».
"""),

"06-bitcoin/09-pow-slozhnost-pochemu-proverka-deshevaya-reorg-i.md": ([
  ("Mastering Bitcoin, гл. 12 — Mining and Consensus", B + "ch12_mining.adoc"),
  ("learnmeabitcoin — Difficulty", L + "mining/difficulty/"),
], """
**Proof-of-Work**: найти `nonce`, чтобы `SHA256(SHA256(header))` был меньше **target**. Единственный способ — перебор; каждая попытка — лотерейный билет.

- **Проверка дешёвая**: один хеш заголовка (80 байт) — микросекунды. Поиск дорогой (~10²³ хешей на блок сейчас), проверка — нет. Асимметрия и есть смысл PoW: доказать затраты, которые любой проверит мгновенно.
- **Сложность** пересчитывается каждые 2016 блоков (~2 недели), чтобы среднее время блока держалось 10 минут при любой суммарной мощности. Больше майнеров → сложнее, награда не растёт.
- **Зачем**: защита истории. Каждый блок содержит хеш предыдущего; изменить старый блок — пересчитать PoW для него и всех следующих **быстрее, чем сеть наращивает цепочку**. Атакующему нужно > 50% хешрейта на длительное время.
- **Правило выбора цепочки**: валидная цепочка с наибольшей суммарной работой (не «самая длинная»). Узлы автоматически переключаются.
- **Reorg**: два майнера нашли блок почти одновременно → временная развилка; следующий блок решит, какая ветка выживет. Транзакции из проигравшего блока возвращаются в mempool (если не конфликтуют). Reorg на 1–2 блока — редко, но бывает; на 6 — практически никогда (отсюда «6 подтверждений»). Для мелких сумм хватает 1.
- **Подтверждения** = сколько блоков сверху. 0 — в mempool, может быть вытеснена/заменена (RBF). Биржи ждут 1–6 в зависимости от суммы.
- Signet: PoW номинальный, блоки дополнительно подписаны оператором — reorg'ов практически нет, блоки ровно каждые 10 мин.

## Фраза для собеса

«PoW — перебор хеша под target; проверить — один хеш, найти — триллионы; сложность держит 10 минут; побеждает цепочка с большей работой, поэтому ждут подтверждений».
"""),

"06-bitcoin/10-konsensus-vs-politika-soft-fork-vs-hard-fork.md": ([
  ("Bitcoin Optech — Soft fork activation", "https://bitcoinops.org/en/topics/soft-fork-activation/"),
  ("Bitcoin Core — Policy vs consensus (doc/policy)", "https://github.com/bitcoin/bitcoin/tree/master/doc/policy"),
], """
**Консенсус-правила** — что делает блок валидным: подписи верны, нет двойной траты, coinbase ≤ лимита, размер ≤ 4M WU, PoW под target, скрипты исполняются. Нарушил — **все** узлы отвергнут блок, навсегда. Менять можно только форком.

**Policy (политика)** — локальные правила узла о том, что *принимать в mempool и ретранслировать*: `minrelaytxfee` 1 sat/vB, лимит на dust, «стандартные» типы скриптов, размер транзакции ≤ 100 kvB, RBF-правила. Нарушил — транзакция не распространится, но если майнер включит её в блок, блок валиден. Каждый узел настраивает сам.

| | Soft fork | Hard fork |
|---|---|---|
| Правила | **ужесточаются** (что было невалидно, остаётся невалидным; часть валидного становится невалидным) | расширяются или меняются несовместимо |
| Старые узлы | принимают новые блоки (не понимая новые фичи) | отвергают новые блоки |
| Результат | одна цепочка | **раскол**: две цепочки с общей историей |
| Примеры | P2SH (2012), SegWit (2017), Taproot (2021) | Bitcoin Cash (2017), Bitcoin SV |

Как SegWit остался soft fork: новые выходы для старых узлов выглядят как «anyone can spend» — валидны по старым правилам; новые узлы требуют witness. Активация — сигнализация майнеров (BIP9) или по времени (BIP8/Speedy Trial для Taproot).

«Биткоин» = цепочка, которую выбрали экономические узлы (биржи, кошельки, пользователи), а не майнеры — социальный консенсус поверх технического.

## Фраза для собеса

«Консенсус — валидность блоков, общая для всех; политика — что я ретранслирую, локально. Soft fork ужесточает правила и совместим со старыми узлами, hard fork раскалывает цепь».
"""),

"06-bitcoin/11-mainnet-testnet-signet-regtest.md": ([
  ("BIP325 — Signet", BIP + "bip-0325.mediawiki"),
  ("Bitcoin Core — Signet docs", "https://en.bitcoin.it/wiki/Signet"),
  ("mempool.space Signet", "https://mempool.space/signet"),
], """
Один код Bitcoin Core, четыре сети — **отдельные блокчейны** с разным genesis, magic bytes, портами и префиксами адресов. Монеты не пересекаются физически: транзакция signet в mainnet невалидна по формату.

| Сеть | Для чего | Как получить монеты | Особенности |
|---|---|---|---|
| **mainnet** | настоящие деньги | купить/намайнить | `bc1…`, `1…`, `3…`; порт 8333 |
| **testnet3/4** | публичный полигон | faucet, майнинг (легко) | `tb1…`, `m/n…`, `2…`; сброс сложности, если блок не найден 20 мин; хаос от мощных майнеров; testnet3 перезапущен как testnet4 в 2024 |
| **signet** | публичный полигон, твоё тестовое | только faucet | блок валиден, если **подписан** ключом оператора (BIP325) → нет гонки майнеров, ровно 10 мин, нет спама; те же префиксы, что testnet; кастомные signet'ы для экспериментов |
| **regtest** | локальная песочница | `generatetoaddress 101 <addr>` | блоки по команде, мгновенно; `bcrt1…`; для юнит- и интеграционных тестов |

Для разработки: логика → regtest (быстро, детерминированно), интеграция → signet (похоже на прод, стабильно), демо → signet.

```ruby
Bitcoin.chain_params = :signet      # bitcoinrb; :mainnet / :testnet / :regtest
```
Mempool API: `mempool.space/signet/api/...`, faucet: `signetfaucet.com`, кошелёк: `electrum --signet`.

## Фраза для собеса

«Signet — тестовая сеть, где блоки подписывает оператор: предсказуемая и без спама, в отличие от testnet; regtest — локальная, блоки по команде».
"""),

"06-bitcoin/12-svoe-testovoe-obyasnit-kazhdyj-shag-i-kazhdoe-re.md": ([
  ("mempool.space Signet API", M),
  ("bitcoinrb wiki — Transaction", "https://github.com/chaintope/bitcoinrb/wiki"),
], """
На собесе попросят «расскажи, как работает» — и будут копать в каждое решение. Подготовь ответ на каждое.

**Поток**
1. Ключ: `Bitcoin::Key.generate` → WIF в файл с правами 600; при повторном запуске читаем, не перезаписываем. *Почему SecureRandom? Почему не seed-фраза?*
2. Адрес: `key.to_p2wpkh` → `tb1q…`. *Почему P2WPKH, а не P2PKH? (дешевле, современно) Почему не P2TR? (валидация адресов в задании 2 просит P2PKH/P2SH/P2WPKH)*
3. Баланс: `GET /address/{addr}/utxo` → сумма `value`. *Считаешь неподтверждённые? Как показываешь?*
4. Сборка: входы = все UTXO (по подсказке) или минимально достаточные; выходы = получатель + сдача, если сдача > dust. *Почему все UTXO? (консолидация, простота) Минус? (размер, приватность)*
5. Комиссия: фиксированная 1000 сат или `vsize × rate`. *Как оценил размер до подписи?*
6. Подпись: для каждого входа `sighash` по правилам BIP143 (SegWit v0), `key.sign`, witness = `[sig, pubkey]`. *Что именно подписывается? (хеш транзакции с amount входа) Почему amount входит в sighash для SegWit?*
7. Отправка: `POST /tx` с hex → txid. *Что если 400? Что если timeout после отправки — она ушла или нет? (проверить `GET /tx/{txid}`)*
8. Проверка: txid в mempool.space, через ~10 мин — подтверждение.

**Решения, которые будут обсуждать**
- Integer сатоши везде. Пыль. Проверка `inputs >= amount + fee` до сборки.
- Гонка двух запусков подряд: второй увидит те же UTXO (первые ещё в mempool) → double spend reject. Как бы решал в сервисе? (lock, очередь, учёт собственных неподтверждённых).
- Что ты упростил и как бы сделал в проде (HD-кошелёк, своя нода вместо публичного API, coin selection, RBF).
- Тесты: сборка транзакции на фикстурных UTXO без сети; HTTP через WebMock.

Отрепетируй на английском за 2 минуты — см. раздел English.
"""),

# ───────── Тестовое ─────────
"07-testovoe/01-happy-path-klyuch-balans-otpravka-v-signet.md": ([
  ("mempool.space Signet API", M),
  ("Signet faucet", "https://signetfaucet.com/"),
  ("Electrum (запуск с --signet)", "https://electrum.org/#download"),
], """
Сначала — сквозной сценарий без украшений. Всё остальное после.

```
$ ruby wallet.rb address        # генерирует ключ при первом запуске, печатает tb1q...
$ # → signetfaucet.com, вставить адрес, подождать блок (~10 мин)
$ ruby wallet.rb balance        # 10000 sat (0.0001 sBTC)
$ ruby wallet.rb send tb1q<electrum> 4000
  txid: 3f1a...                  # → mempool.space/signet/tx/3f1a...
```

Минимальный скелет:
```
wallet.rb            # CLI: разбор команд
lib/wallet/key_store.rb      # load_or_generate(path) → Bitcoin::Key
lib/wallet/mempool_client.rb # utxos(addr), broadcast(hex), fees — Net::HTTP или Faraday
lib/wallet/tx_builder.rb     # build(utxos, to:, amount:, fee:, change:) → Bitcoin::Tx (подписанный)
lib/wallet/cli.rb
```

Порядок работы: 1) ключ + адрес → faucet; 2) `utxos` → баланс; 3) `tx_builder` с одним UTXO на хардкоде → подпись → `broadcast`; 4) только теперь — валидации, ошибки, тесты, Docker, динамическая комиссия.

Проверка подписи до отправки: `tx.to_hex` → вставить в decoder (blockcypher / `bitcoin-cli decoderawtransaction`) — видно входы/выходы; если `POST /tx` вернул `non-mandatory-script-verify-flag` — подпись/sighash неверны; `bad-txns-in-belowout` — выходы больше входов; `min relay fee not met` — комиссия < 1 sat/vB.

Ссылку на успешный txid — в README.
"""),

"07-testovoe/02-klyuch-ne-perezapisyvaetsya-ne-kommititsya-ne-lo.md": ([
  ("OWASP — Secrets Management Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html"),
], """
Проверяющий посмотрит на это первым делом — компания про хранение ключей.

- **Не перезаписывать**: `File.exist?(path) ? load : generate_and_save`. Перезапись = потеря средств. Можно отдельную команду `init --force` с подтверждением.
- **Атомарная запись**: во временный файл → `File.rename`. Крэш посреди записи не оставит полуфайл.
- **Права**: `File.write(path, wif, perm: 0o600)` + `File.chmod`. Директория `data/` с 700.
- **Не в git**: `data/` и `*.wif`/`.env` в `.gitignore`; в репо — `.env.example`. Проверить `git log -p` перед отправкой — не засветил ли случайно.
- **Не логировать и не печатать**: ни WIF, ни hex приватного ключа — ни в `puts`, ни в исключениях (`inspect` у `Bitcoin::Key` может содержать приватник — не выводить объект целиком). `--verbose` печатает hex *транзакции*, не ключа.
- **Путь из ENV/конфига**: `ENV.fetch("WALLET_PATH", "data/wallet.wif")` — в Docker монтируется volume.
- Бонус: шифрование файла паролем (`OpenSSL::Cipher` AES-256-GCM, ключ из `PBKDF2`/`scrypt`), пароль через `IO.console.getpass`. Написать в README как «что бы сделал дальше», если не успел.
- Для проверки «дошло ли»: `ruby wallet.rb address` печатает только адрес.

В README одной строкой: где лежит ключ, как бэкапить, что перезапуск не создаёт новый.
"""),

"07-testovoe/03-summy-v-integer-satoshi.md": ([
  ("Bitcoin Wiki — Satoshi (unit)", "https://en.bitcoin.it/wiki/Satoshi_(unit)"),
], """
1 BTC = 100 000 000 сатоши. Сеть, API и библиотеки работают в **сатоши целым числом**. Float — только на границе с человеком.

```ruby
SAT_PER_BTC = 100_000_000

def to_sat(btc_str)  = (BigDecimal(btc_str) * SAT_PER_BTC).to_i     # ввод пользователя: строка → BigDecimal → Integer
def to_btc(sat)      = format("%.8f", Rational(sat, SAT_PER_BTC))    # вывод

to_sat("0.00001")    # 1000 — комиссия из задания
to_sat("0.1")        # 10_000_000
(0.1 * 1e8).to_i     # 10000000 — повезло; (0.29 * 1e8).to_i → 28999999 — нет
```

- Парсить ввод через `BigDecimal(str)` или `Rational`, никогда `Float(str) * 1e8`.
- Внутри — `Integer`: UTXO `value`, `amount`, `fee`, `change`. Проверки `inputs >= amount + fee` целые.
- Mempool API отдаёт `value` в сатоши; `bitcoinrb` `Bitcoin::TxOut.new(value: sat)` — тоже.
- Второе задание: курс USDT/BTC — `BigDecimal`, результат умножения → `.floor` до сатоши в пользу обменника; комиссия 3% — `(amount * 3 / 100)` на BigDecimal, округление явное.
- В Postgres — `bigint`. В JSON — число (сатоши) или строка BTC, не float.
- Тест: `expect(to_sat("0.29")).to eq(29_000_000)` — ловит float-баг.

## Фраза для собеса

«Все суммы — Integer в сатоши; ввод парсю через BigDecimal, Float нигде, кроме форматирования вывода».
"""),

"07-testovoe/04-edge-cases-net-sredstv-nevalidnyj-adres-neskolko.md": ([
  ("mempool.space API — POST /tx (ошибки в теле ответа)", M + "#post-transaction"),
], """
Проверяющий попробует сломать. Пройди список сам:

**Вход**
- Невалидный адрес: не signet (`bc1q…`), опечатка в checksum, мусор → `Bitcoin::Script.parse_from_addr` бросит → понятная ошибка, exit code ≠ 0.
- Сумма: 0, отрицательная, не число, больше 8 знаков после точки, ниже dust (294 sat) → отказ до любых запросов.
- Отправка самому себе — допустимо, но бессмысленно; предупредить.

**Средства**
- Нет UTXO → «balance 0», не крэш на `sum` пустого массива.
- Хватает на сумму, но не на сумму + комиссию → сообщение с точными цифрами «need X, have Y».
- Несколько UTXO: входы собираются из всех (или по одному, пока не хватит); подпись на **каждый** вход со своим amount.
- Сдача < dust → не создавать выход, добавить к комиссии; написать об этом в выводе.
- Неподтверждённые UTXO (своя сдача от прошлой отправки): решить — тратить (ок для своих) или ждать; флаг `--allow-unconfirmed`.

**Сеть**
- API недоступен / 5xx / timeout → retry 2–3 раза с паузой, потом понятная ошибка. Таймауты на `Net::HTTP` явно (`open_timeout`, `read_timeout`).
- `POST /tx` вернул 400 с текстом → показать его (там причина: `bad-txns-inputs-missingorspent` — UTXO уже потрачен; `min relay fee` — комиссия мала).
- Timeout **после** отправки — транзакция могла уйти; перед повтором проверить `GET /tx/{txid}` (txid можно посчитать локально до отправки: `tx.txid`).

**Повторный запуск**
- Ключ не перезаписан; второй `send` подряд до подтверждения увидит те же UTXO → отказ от сети; обработать как «UTXO уже потрачен, подожди подтверждения».

Каждый пункт — одна строка в README «обработано / не обработано».
"""),

"07-testovoe/05-testy-rspec-hotya-by-na-postroenie-tranzakcii-ra.md": ([
  ("RSpec — документация", "https://rspec.info/documentation/"),
  ("WebMock", "https://github.com/bblimke/webmock"),
], """
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
"""),

"07-testovoe/06-readme-na-anglijskom-kak-zapustit-chto-realizova.md": ([
  ("Make a README", "https://www.makeareadme.com/"),
], """
README читают до кода. Структура на одну страницу, на английском:

```
# Signet wallet CLI

Minimal command-line Bitcoin Signet wallet in Ruby: generates a key, shows balance, sends sBTC.

## Quick start
    bundle install
    ruby wallet.rb address          # prints tb1q..., creates data/wallet.wif on first run
    ruby wallet.rb balance
    ruby wallet.rb send <address> <amount_btc>
  or with Docker: docker compose run wallet balance

## Example transaction
  https://mempool.space/signet/tx/<txid>   ← реальный, подтверждённый

## How it works
  key (WIF, data/) → address (P2WPKH) → UTXOs via mempool.space API →
  inputs: all UTXOs → outputs: recipient + change (if above dust) → sign (BIP143) → broadcast
  Fee: fixed 1000 sat (or `--dynamic` = vsize × recommended rate)
  All amounts are integer satoshis.

## Handled cases
  - insufficient funds (including fee), invalid/non-signet address, dust change, API errors (3 retries)
  - key is never overwritten / logged; file mode 600

## Simplifications & what I'd do next
  - single key, no HD wallet; public API instead of own node; spends all UTXOs (no coin selection);
    no RBF; unconfirmed change is spent (flag to disable)

## Tests
    bundle exec rspec      # builder logic + mocked HTTP, no network

## Decisions
  bitcoinrb over bitcoin-ruby: maintained, native signet params, SegWit/Taproot support
```

Что важно: команда запуска копипастом работает; ссылка на настоящий txid; честный список упрощений — это зрелость, а не слабость; обоснование выбора библиотеки одной строкой.
"""),

"07-testovoe/07-docker.md": ([
  ("Docker docs — Dockerfile best practices", "https://docs.docker.com/build/building/best-practices/"),
  ("Official Ruby image", "https://hub.docker.com/_/ruby"),
], """
```dockerfile
# Dockerfile
FROM ruby:3.3-slim
RUN apt-get update -qq && apt-get install -y --no-install-recommends build-essential libssl-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY Gemfile Gemfile.lock ./
RUN bundle config set --local without 'development test' && bundle install --jobs 4
COPY . .
RUN useradd -m app && chown -R app /app
USER app
ENTRYPOINT ["ruby", "wallet.rb"]
CMD ["balance"]
```

```yaml
# docker-compose.yml
services:
  wallet:
    build: .
    volumes:
      - ./data:/app/data        # ключ живёт на хосте, переживает пересборку
    environment:
      WALLET_PATH: /app/data/wallet.wif
      MEMPOOL_URL: https://mempool.space/signet/api
```

```
docker compose run --rm wallet address
docker compose run --rm wallet send tb1q... 0.0001
```

- Слои: Gemfile копируется и `bundle install` до `COPY . .` — кэш не сбрасывается при каждом изменении кода.
- `slim`, не `alpine` для Ruby (musl + нативные гемы = боль); `build-essential` нужен для `secp256k1`/`openssl` в bitcoinrb — либо multi-stage, чтобы не тащить компилятор в финальный образ.
- Не root. Ключ — только через volume, не в образе (`.dockerignore`: `data/`, `.env`, `.git`).
- `.dockerignore` обязателен, иначе в контекст попадёт всё.
- Для второго задания — добавить `db: postgres:16`, `redis`, `web` с `depends_on` и `healthcheck`.
"""),

"07-testovoe/08-bonus-dinamicheskaya-komissiya-cherez-fees-recom.md": ([
  ("mempool.space — GET /v1/fees/recommended", M + "#get-recommended-fees"),
  ("Bitcoin Optech — Transaction size calculator", "https://bitcoinops.org/en/tools/calc-size/"),
], """
`fee = vsize × rate`. Две части: узнать rate и узнать vsize **до** того, как транзакция подписана (размер зависит от подписей).

```ruby
rate = client.recommended_fees.fetch("fastestFee")   # sat/vB; Signet → 1

# Способ 1: оценка по формуле (P2WPKH)
def estimate_vsize(n_in, n_out) = 10.5 + n_in * 68 + n_out * 31     # overhead + входы + выходы
# Способ 2: собрать с фиктивными подписями (72-байтовые нули) и спросить tx.vsize
# Способ 3: подписать, измерить, пересобрать с точной комиссией (ещё одна подпись — дёшево)

fee = [(vsize * rate).ceil, vsize * 1].max            # не ниже minrelay 1 sat/vB
```

Курица и яйцо со сдачей: наличие change-выхода меняет размер. Алгоритм:
1. Выбрать входы.
2. Посчитать vsize **с** выходом сдачи, fee.
3. `change = inputs − amount − fee`.
4. `change < dust` → убрать выход сдачи, пересчитать vsize/fee (стало меньше), остаток в комиссию.
5. `change < 0` → добавить вход, повторить.

Разумные границы: `rate` clamp между 1 и, скажем, 200 sat/vB — защита от сломанного API. Флаг `--fee-rate N` для ручного override. В выводе показать: `fee: 141 sat (141 vB × 1 sat/vB)`.

Для второго задания комиссия фиксирована 0.000006 — но вынести в конфиг, не в константу.

## Фраза для собеса

«Беру рекомендованную ставку, оцениваю vsize по числу входов/выходов, умножаю, не опускаюсь ниже 1 sat/vB и пересчитываю, если сдача ушла в пыль».
"""),

# ───────── Английский: ответы ─────────
"08-anglijskij/01-tell-me-about-yourself-90-sek.md": ([
  ("Interviewing.io — Tell me about yourself", "https://interviewing.io/guides/hiring-process/tell-me-about-yourself"),
], """
Структура: **сейчас → как пришёл → почему здесь**. Не биография, а 90 секунд с мостиком к вакансии. Выучить не дословно, а опорными точками.

> I'm a full-stack developer with about three years of commercial experience, mostly on the backend. I started with PHP and Laravel, building and maintaining internal CRM systems — REST APIs, business modules, database design on PostgreSQL. On the frontend I've worked with Vue and TypeScript, including a migration from React to Vue 3.
>
> In between I spent almost a year on a systems project — adapting Plan 9 for a client — which gave me a lot of low-level debugging experience and comfort with C and virtualization.
>
> I've known Ruby for a while — I took a Rails course and I find the language much more expressive than PHP — and recently I decided to make it my main stack. Your test task was a good reason to go deep: I built a Signet wallet CLI from scratch, and that got me into UTXOs, SegWit, and how transactions are actually signed.
>
> What attracts me here is the combination: Ruby, a product where correctness with money really matters, and a non-custodial model that I find technically honest. I'd like to grow into a solid backend engineer in exactly this kind of domain.

Проверь: нет перечисления всех технологий подряд; есть одна конкретика на каждое место; последний абзац — про них, не про тебя; укладывается в 90 сек при спокойном темпе (≈200 слов).

Записать на диктофон 3 раза. На третий — без бумажки.
"""),

"08-anglijskij/02-why-ruby-why-crypto-why-hodl-hodl.md": ([
  ("Hodl Hodl — About", "https://hodlhodl.com/pages/about"),
], """
Три вопроса — один честный ответ, без пафоса про «revolution».

**Why Ruby?**
> I've been writing PHP for years and it pays the bills, but Ruby is the language I actually enjoy. Blocks, Enumerable, the way you can express intent in one readable line — it changes how you think about code. Rails conventions mean less bikeshedding and more product work. And the ecosystem around correctness — RSpec, dry-rb, strong typing where you want it — fits the kind of engineer I want to be.

**Why crypto?**
> Not the hype part. What interests me is that Bitcoin is a system where the rules are enforced by math and code rather than by an operator — and as an engineer, the constraints are fascinating: you can't roll back a transaction, you can't "fix it in the database", every edge case with money is real. Preparing your test task I spent evenings on UTXOs and signatures and genuinely enjoyed it.

**Why Hodl Hodl?**
> Non-custodial P2P with multisig escrow is, to me, the technically honest way to do an exchange: the platform never holds users' funds, it's an arbiter with one key out of three. That's a product where backend correctness and security are the product. Also — a small team, Ruby, and a domain I can keep learning in for years.

Если спросят «а не страшно, что крипта волатильна / регуляции»: *«I'm not here for the price. The engineering problems exist regardless.»*

Не говорить: «I want to earn in crypto», «always dreamed», ничего про инвестиции.
"""),

"08-anglijskij/03-why-did-you-leave-victorum-ip-plan-9-sovteh-po-2.md": ([
  ("The Muse — How to answer 'Why did you leave'", "https://www.themuse.com/advice/why-did-you-leave-your-last-job-interview-question-answer"),
], """
Правило: **коротко, без негатива о работодателе, с выводом**. 15–20 секунд на каждое. Интервьюер проверяет не причины, а зрелость.

**Victorum Group (6 мес, 2023–24)**
> It was a fixed-scope contract: I was brought in to extend an internal CRM — a notifications module and a few business modules. When the scope was delivered, the engagement ended. Short, but I shipped what I was hired for.

**ИП / Plan 9 (10 мес, 2024–25)**
> That was a research-style project — adapting Plan 9 for a client's requirements. It was fascinating technically, I did a lot of low-level debugging and prototyping in C, but it was a bounded project with a clear end, and it wasn't web development, which is where I want to build my career. So when it wrapped up I went back to backend.

**Совтех (13 мес, 2025–26)**
> I joined to migrate their CRM frontend to Vue 3 and build out the Laravel API. By the end of the year the major migration was done and the roadmap turned into maintenance. I realized I wanted two things: a deeper backend role, and to move to Ruby, which I'd been learning on the side. That's a change you can't make inside a PHP shop, so I left to make it properly.

Если спросят про паттерн «везде около года»:
> I see it. Two of those were bounded contracts by design. What I'm looking for now is the opposite — a place to stay and grow for years, which is part of why a product company appeals to me more than contract work.

Не оправдываться, не рассказывать про конфликты/зарплату/«токсичность». Пауза после ответа — не заполнять.
"""),

"08-anglijskij/04-walk-me-through-the-test-task-2-min.md": ([
  ("Bitcoin Optech — Glossary (термины на английском)", "https://bitcoinops.org/en/topics/"),
], """
Отвечать как **поток данных**, не как список файлов. Рисовать в воздухе: ключ → адрес → UTXO → транзакция → сеть.

> It's a command-line Signet wallet in Ruby with three commands: address, balance, and send.
>
> On first run it generates a private key with SecureRandom, stores it as WIF in a data directory with 600 permissions, and never overwrites it. From the key I derive a native SegWit address — P2WPKH, `tb1q`.
>
> Balance is the sum of unspent outputs for that address. I fetch them from the mempool.space Signet API — each UTXO is a txid, an output index, and a value in satoshis. All amounts in the app are integers; floats only appear when formatting output.
>
> For send, I take the UTXOs as inputs, create one output to the recipient and a change output back to my address — unless the change would be dust, in which case it goes to the fee. The fee is inputs minus outputs: fixed at a thousand satoshis, or optionally vsize times the recommended rate. Before building anything I check that the inputs cover amount plus fee and give a precise error if not.
>
> Each input is signed separately with the SegWit sighash — which commits to the input amount — and the witness is the signature plus the public key. Then I broadcast the hex to the API and print the txid. There's a confirmed example in the README.
>
> I kept it simple on purpose: one key, no HD wallet, no coin selection, public API instead of my own node. Tests cover the builder logic — change, dust, insufficient funds — with HTTP mocked.

≈220 слов, 2 минуты. Дальше ждут вопросов — см. «Своё тестовое: объяснить каждый шаг».

Слова, которые должны звучать естественно: *unspent output, derive, sign, broadcast, change, dust, fee rate, confirmation, witness*.
"""),

"08-anglijskij/05-a-bug-i-found-and-fixed-star-90-sek.md": ([
  ("STAR method", "https://www.themuse.com/advice/star-interview-method"),
], """
**STAR**: Situation (1 предложение) → Task → Action (основная часть, что делал *ты*) → Result (цифра или факт) → *Learning* (одно предложение). Выбери реальный баг, желательно про данные/конкурентность — это их домен.

Шаблон с твоего опыта (замени детали на настоящие):

> **S** — At Sovtech we had a CRM where managers sometimes saw duplicate notifications — the same event delivered two or three times. It was intermittent, maybe once a day, and nobody could reproduce it.
>
> **T** — I took it because it was annoying users and eroding trust in the system.
>
> **A** — I started from logs and found the duplicates always came within the same second. That pointed to concurrency, not logic. The notification was created in a model callback right after the record was saved, and the job that delivered it ran before the transaction committed — so when the job failed to find the record, it retried, and meanwhile a second code path had already created another notification. Two problems: a job enqueued inside a transaction, and no idempotency on the delivery side. I moved the enqueue to after commit, and added a unique key on event id plus recipient so a second insert would fail instead of duplicating.
>
> **R** — Duplicates went to zero; I verified over two weeks of logs. The fix was about twenty lines plus a migration.
>
> **L** — Since then I treat "enqueue after commit" and "make side effects idempotent" as defaults, not optimizations.

Если это было на Laravel — так и сказать (`dispatch` внутри transaction, `afterCommit`), суть та же и интервьюеру понятна.

Избегать: баг, где виноват кто-то другой; баг без твоих действий; история длиннее 90 секунд.
"""),

"08-anglijskij/06-explain-utxo-escrow-2-of-3-na-anglijskom-1-min.md": ([
  ("learnmeabitcoin — UTXO", L + "transaction/utxo/"),
], """
Два мини-объяснения по 30–40 секунд. Простыми словами, как коллеге-вебщику.

**UTXO**
> Bitcoin doesn't have account balances. It has a log of transactions, and each transaction consumes some previous outputs and creates new ones. An output that hasn't been consumed yet is a UTXO — an unspent transaction output — basically a coin with a value and a spending condition attached. Your "balance" is just the sum of UTXOs your key can unlock. When you pay, you spend whole UTXOs as inputs, create an output to the recipient, and send the remainder back to yourself as change. Whatever you don't assign to an output becomes the miner's fee.

**2-of-3 escrow**
> On Hodl Hodl the seller doesn't send bitcoin to the platform. They lock it in a multisig output that requires two signatures out of three keys: the buyer's, the seller's, and the platform's. In a normal trade the buyer and seller sign together and the platform isn't involved. If there's a dispute, the platform signs with whichever side is right. But the platform alone has only one key, so it can never take the funds — it's an arbiter, not a custodian. Technically it's a P2SH output with a two-of-three CHECKMULTISIG script.

Отработать слова: *consume, unlock, remainder, lock funds, arbiter, custodian, dispute, output index*.

Если собеседник кивает — остановиться. Если спрашивает «and how does the script know?» — рассказать про redeem script и хеш.
"""),

"08-anglijskij/07-3-voprosa-k-nim.md": ([
  ("Julia Evans — Questions I'm asking in interviews", "https://jvns.ca/blog/2013/12/30/questions-im-asking-in-interviews/"),
], """
Вопросы показывают, о чём ты думаешь. Выбрать 3, остальные — в запас. Не спрашивать то, что есть на сайте.

**Про код и процесс**
- *What does the codebase look like — a Rails monolith, several services? How old is it, and what's the Rails version?*
- *How do changes get to production — code review, CI, how often do you deploy?*
- *How do you test anything that touches real bitcoin — regtest, signet, a staging environment?*
- *What's the ratio of new features to maintenance right now?*

**Про команду**
- *How big is the engineering team, and who would I work with day to day?*
- *How is work distributed — do people own areas, or does everyone touch everything?*
- *What does the onboarding look like for the first month?*

**Про домен (показывает, что ты вник)**
- *Are you moving escrow to Taproot or P2WSH, or is P2SH still the practical choice?*
- *What's the hardest engineering problem you've dealt with in the last year?*

**Про роль**
- *What would a successful first three months look like for this position?*
- *Is the salary in USDT the only option, or are there alternatives for contractors in Belarus?* — на HR-этапе, не на техническом.

Не спрашивать первым делом про отпуск и график. Записать ответы — пригодятся на следующем этапе.
"""),

"08-anglijskij/08-frazy-spasateli-rephrase-let-me-think-i-haven-t-.md": ([
  ("Cambridge — Useful phrases for interviews", "https://www.cambridgeenglish.org/learning-english/"),
], """
Выучить **наизусть** до автоматизма — чтобы вылетали без раздумий, когда мозг занят вопросом.

**Не понял вопрос**
- *Sorry, could you rephrase that?*
- *Could you repeat the last part, please?*
- *Just to make sure I understand — you're asking about …, right?*

**Нужно время**
- *That's a good question. Let me think for a second.*
- *Let me structure this.*
- *Give me a moment — I want to answer this properly.*

**Не знаю**
- *I haven't used it in production, but as I understand it, …*
- *I'm not 100% sure, but I'd guess … — and here's how I'd check.*
- *I don't know that one. My approach would be to …*
- *I haven't hit that case. Let me reason about it.*

**Поправить себя**
- *Actually, let me correct that — …*
- *Wait, that's not quite right. What I meant is …*

**Проверить, что ответил**
- *Does that answer your question?*
- *Do you want me to go deeper into any part?*

**Закончить мысль, когда понесло**
- *…so, in short: …*
- *The bottom line is …*

Ключевое: *«I don't know»* + *«here's how I'd find out»* — это **нормальный** ответ, который ценят выше угадывания. Пауза в 3 секунды — не провал, в живом разговоре она не заметна.
"""),

# ───────── Резюме ─────────
"09-rezyume/01-dobavit-ruby-rails-kurs-pet-proekty-testovoe-hod.md": ([], """
Главная проблема текущего резюме: **ни слова про Ruby** на Ruby-позицию. HR-фильтр и ATS отсеят до собеса.

Куда вставить:

**Заголовок**: `Backend Developer (Ruby / PHP)` вместо `Middle Fullstack`. Не врать про годы Ruby — но заявить направление.

**Summary (3 строки под заголовком)**:
> Backend developer, 3 years commercial PHP/Laravel + Vue; moving to Ruby. Completed RoR course, building a Bitcoin Signet wallet CLI and exchange demo in Ruby (bitcoinrb, RSpec, Sidekiq). Strong in PostgreSQL, REST APIs, background jobs.

**Projects** (новый раздел, выше Education):
> **Signet wallet CLI & exchange demo** — Ruby 3.3, bitcoinrb, RSpec, Docker. CLI wallet (key management, UTXO selection, SegWit signing, fee estimation via mempool.space API) and a Rails demo of USDT→sBTC exchange with Sidekiq workers and admin panel. [github link]

**Skills**: Ruby, Rails, RSpec, Sidekiq — в начало списка. Честность: при вопросе «сколько Ruby в проде» — «commercially none yet; here's what I built and here's how fast I picked it up».

**Education / Courses**: «Ruby on Rails course (название, год)».

Эффект: ключевики для фильтра + доказуемый артефакт (репозиторий) + явно обозначенный переход, который объясняет, почему ты здесь.
"""),

"09-rezyume/02-navyki-pod-poziciyu-ubrat-virtualbox-wordpress-h.md": ([], """
Раздел «Навыки» сейчас — всё, что когда-либо трогал. Он должен отвечать на вопрос «подходит ли под вакансию», а не «что умеет».

**Убрать**: VirtualBox, QEMU, CMS WordPress, HTML5, CSS3, Tailwind, Svelte/SvelteKit, Nuxt, Bun, Elysia, SQLite, «Веб-программирование», Python (если не готов отвечать на вопросы по нему). Каждый лишний пункт размывает и провоцирует вопросы, на которые нет хороших ответов («хм, зачем разработчику VirtualBox?»).

**Оставить и сгруппировать**:
```
Backend:   Ruby, Rails, RSpec, Sidekiq, PHP, Laravel, REST API
Data:      PostgreSQL, Redis
Frontend:  TypeScript, Vue 3, React (basic)
Infra:     Docker, docker-compose, Git, GitHub Actions, Linux/Bash
Domain:    Bitcoin (UTXO, SegWit, multisig), bitcoinrb
```

Правило: 15–20 пунктов максимум, первые — те, что в вакансии. Если технология упомянута в навыках — она должна быть видна в опыте или проектах.

Для hh.ru ключевые слова важны для поиска; для английского PDF — читаемость. Можно два разных резюме.
"""),

"09-rezyume/03-ubrat-zhelaemuyu-zp-murino-sankt-peterburg.md": ([], """
Три поля, которые сейчас вредят:

- **«150 000 ₽ на руки»** — для иностранной компании нерелевантно и ставит якорь ниже рынка; для российских работодателей ограничивает торг. Убрать; обсуждать голосом, когда есть оффер.
- **«Проживает: Мурино»**, **«Готов работать удалённо: Санкт-Петербург»** — создаёт впечатление локального кандидата, противоречит фактическому положению. Для remote-позиции: `Location: Belarus (remote), UTC+3` и готовность к overlap с их часовым поясом.
- **Гражданство / разрешение на работу** — для международной компании достаточно `Citizenship: Belarus, Russia`; детали — на этапе оформления.

Также проверить: телефон с кодом страны, email без `list.ru` (завести `name.surname@gmail.com` или домен — мелочь, но влияет на восприятие), ссылка на GitHub с публичным репозиторием тестового, LinkedIn если есть.

Дата рождения/возраст — в английском CV не указывают.
"""),

"09-rezyume/04-dostizheniya-s-ciframi-hotya-by-poryadok.md": ([
  ("Harvard — Action verbs & resume bullets", "https://careerservices.fas.harvard.edu/resources/create-a-strong-resume/"),
], """
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
"""),

"09-rezyume/05-ubrat-realizovyval-biznes-logiku-konkretnye-modu.md": ([], """
«Реализовывал бизнес-логику», «разрабатывал новые модули», «расширял функционал», «исправлял ошибки» — это описание профессии, а не твоего вклада. Любой разработчик делает это ежедневно.

Замена — **назвать предмет**:

- «разрабатывал бизнес-модули CRM» → *какие именно*: «сделки и воронка продаж», «расчёт комиссий менеджеров», «импорт прайс-листов из Excel», «интеграция с 1С/телефонией».
- «реализовывал бизнес-логику на Laravel» → «модуль расчёта скидок с правилами по клиентским группам», «state machine заказа (7 статусов) с аудитом переходов».
- «исправлял ошибки и обеспечивал совместимость» → убрать совсем или заменить одним конкретным: «устранил гонку при параллельном создании заказов (unique constraint + retry)».
- «расширял базовый функционал CRM» → убрать, покрывается другими пунктами.

Проверка: по каждому пункту интервьюер может задать «расскажи подробнее» — и у тебя есть 2-минутная история с деталями. Если истории нет — пункт не нужен.

Для Plan 9: «изучал архитектуру», «участвовал в проверке гипотез», «проводил базовую отладку» — пять пунктов про одно. Сжать до двух конкретных: что именно настроил/собрал/нашёл.
"""),

"09-rezyume/06-plan-9-odna-fraza-chto-dalo.md": ([], """
10 месяцев не-веб между двумя веб-работами — интервьюер спросит. Если не объяснить, выглядит как провал в карьере или случайная подработка. Объяснить — выглядит как широта.

В резюме (одна строка после описания):
> *Takeaway: deep systems-level debugging, comfort with C, build toolchains and virtualization — skills I now apply to performance and infrastructure work in web backends.*

Устно (20 секунд):
> It was a research project adapting Plan 9 for a client. Not web, but it taught me to read unfamiliar systems from source, debug at the level of boot and build failures, and document reproducible steps for a team. I came back to backend with much more confidence in anything low-level — Docker, Linux, performance.

Сами пункты сжать с пяти до двух:
- *Set up reproducible test infrastructure (QEMU) with automated builds and smoke checks for experimental system images.*
- *Investigated and fixed build/boot failures in a C codebase; documented platform limitations and reproduction steps for the team.*

QEMU оставить в тексте опыта как контекст — но убрать из списка навыков.
"""),

"09-rezyume/07-anglijskaya-odnostranichnaya-pdf-versiya.md": ([
  ("Reactive Resume — бесплатный конструктор", "https://rxresu.me/"),
  ("Jake's Resume (LaTeX/Overleaf шаблон)", "https://www.overleaf.com/latex/templates/jakes-resume/syzfjbzwjncs"),
], """
hh.ru-экспорт иностранная компания читать не будет. Нужен **одностраничный PDF на английском**, без фото, без возраста, с GitHub.

Структура (сверху вниз):
```
Alexey Kondratenko
Backend Developer (Ruby / PHP)  ·  Belarus, remote (UTC+3)
email · telegram · github.com/… · linkedin

SUMMARY (3 строки)
SKILLS (5 строк, сгруппированные)
EXPERIENCE
  Sovtech — Full-stack Developer — Jun 2025 – Jun 2026 — 3–4 bullets с цифрами
  [ИП] — Systems Engineer (research project, Plan 9) — Aug 2024 – May 2025 — 2 bullets + takeaway
  Victorum Group — PHP Developer — Oct 2023 – Mar 2024 — 2–3 bullets
PROJECTS
  Signet wallet CLI & exchange demo (Ruby) — 2 строки + ссылка
EDUCATION
  Polotsk State University — Software Engineering, 2021 / 2023
LANGUAGES  Russian native · English B1 (working proficiency)
```

Правила: Past Simple для прошлых мест; одинаковый формат дат; названия компаний — латиницей; роль как её поймут там (`Systems Engineer`, не `Инженер-разработчик`); никаких «responsible for» — глаголы действия; шрифт 10–11pt, поля 1.5 см; PDF с именем `Kondratenko_Alexey_Backend_Ruby.pdf`.

Инструмент: Reactive Resume / Overleaf (Jake's template) / Google Docs → PDF. Прогнать через Grammarly или попросить проверить. Сохранить и `.docx` на случай, если попросят.
"""),

"09-rezyume/08-otvet-na-pochemu-3-mesta-po-godu-otrepetirovan.md": ([], """
Вопрос будет. Цель ответа — не оправдаться, а показать, что ты видишь паттерн и твой следующий шаг его ломает.

Структура: **признать → объяснить без негатива → переключить на будущее**. 30 секунд.

> I see the pattern, and I'd rather address it than pretend it's not there. Two of the three were bounded engagements by design — a contract to extend a CRM and a research project with a defined end. The third, Sovtech, was a full year where I shipped the main thing I was hired for, the Vue 3 migration, and then the work turned into maintenance.
>
> The common thread is that I was taking what was available, not choosing. This time I'm choosing: Ruby, a product company, a domain I actually want to go deep in. I'm not looking for another year — I'm looking for a place where the second and third year are more interesting than the first.

Что **не** говорить: «компания была плохая», «мало платили», «токсичный менеджер», «не было роста» (это звучит как претензия), «так получилось».

Если дожмут («а что гарантирует, что тут не уйдёшь?»):
> Nothing guarantees it — but you can look at what I did with your test task before anyone promised me anything. That's the level of interest I bring.

Отрепетировать вслух до состояния, когда ответ звучит спокойно, без защитной интонации. Это важнее формулировок.
"""),
}
