# Шаблон нового сезона FH6

Машинный шаблон определён в `data/season-state.schema.json`. Для смены сезона создать локальный `automation/new-season-input.json` и заполнить следующие разделы.

## Метаданные

- `seriesNumber`, `seriesSlug`, `seriesName`;
- `season`: `summer`, `autumn`, `winter` или `spring`;
- `seasonDisplay`: русское название;
- `startAt`, `endAt`, `lastContentUpdate`: ISO 8601 с `+07:00`;
- `reportTitle`;
- новый `archiveFile` вида `seasons/YYYY-MM-DD-series-NN-season.md`;
- новая папка `assetsDirectory` внутри `reports/assets/`;
- конкретная сезонная `fandomUrl` и официальная `officialPlaylistUrl`;
- фактические `expectedCardCount`, `expectedDailyItems` и лимит HTML.

## Карточки

Создать `activities` в точном игровом порядке. Для каждой карточки указать:

- последовательные `id` и `number`;
- `kind`, `title`, `points`;
- `conditionHtml`, `howHtml`, `tuneHtml`, `sourceHtml`;
- `visual.image`, `visual.icon`, позицию и источник;
- `completeness.condition`, `solution`, `vehicleTune`, `visual`;
- `missingFields`.

Допустимые статусы: `confirmed`, `community`, `preliminary`, `missing`, `not_applicable`.

Неизвестное фактическое поле оставлять пустым. Для него обязательны статус `missing`/`preliminary`, имя в `missingFields` и запись в `openItems` с причиной и следующим источником для проверки. Для точной игровой плитки разрешён сезонный fallback-файл, но статус остаётся предварительным до появления нужной плитки.

## Применение

1. Скачать все указанные визуалы.
2. Выполнить `automation/start_new_season.ps1 -InputPath automation/new-season-input.json -ValidateOnly`.
3. После успешной проверки запустить без `-ValidateOnly`.
4. Собрать portable-отчёт по `docs/WORKFLOW.md`.
5. Публиковать только после `STRUCTURE_OK`.
