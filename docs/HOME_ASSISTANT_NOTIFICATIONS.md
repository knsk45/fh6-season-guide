# Уведомления через Home Assistant

После полной ежедневной проверки FH6-задача вызывает существующий push-сервис Home Assistant и отправляет один итог:

- `UpdateRequired` — содержимое Steam-зеркала отличается от последней подтверждённой публикации; в чат «Сводка сезона» приходит запрос на подтверждение;
- `UpToDate` — содержательных изменений нет, подтверждение не требуется;
- `CheckBlocked` — аудит, публикация GitHub Pages или проверка Steam не завершились надёжно.

Изменение одного `lastContentUpdate` не считается содержательным изменением Steam. Точное время ежедневной проверки остаётся в основном HTML-отчёте; Steam содержит постоянную ссылку на него.

## Доступ

Публичный FH6-репозиторий не хранит URL Home Assistant, токен или имя мобильного устройства. Локальная конфигурация находится в игнорируемом Git файле:

`automation/runs/home-assistant-notification.local.json`

Она указывает на соседний секрет `Home Assistant/secrets/home_assistant.local.json` и на уже существующую службу `notify.mobile_app_kns_iphone_15_pro_max`. Токен читается только в памяти процесса и не выводится в журнал.

## Ручная проверка

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File automation/send_home_assistant_notification.ps1 -Status UpToDate -RunId manual-test
```

Повтор с той же парой `Status` / `RunId` не отправляет дубликат. Изменение конфигурации Home Assistant для этого механизма не требуется.
