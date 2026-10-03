---
title: "Ключ не перезаписывается; не коммитится; не логируется"
hot: true
links:
  - { t: "OWASP — Secrets Management Cheat Sheet", u: "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html" }
---
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
